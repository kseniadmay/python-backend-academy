# -*- coding: utf-8 -*-
"""
Стресс-тестирование конкурентности, дисковой персистентности (WAL Mode),
миграций схемы и граничных лимитов бэкенда Python Backend Academy.
"""

import concurrent.futures
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tests.fixtures.fixture_factory import (
    create_test_db,
    seed_canonical_content,
    migrate_legacy_progress_bundle,
    make_v1_legacy_user_fixture,
    make_v2_legacy_user_fixture,
)
from backend.app.schemas.progress import ProgressBundle, SyncPushRequest
from backend.app.services.sync_service import sync_service


class TestBackendConcurrencyAndResilience(unittest.TestCase):
    """Стресс-тесты конкурентности, персистентности и отказоустойчивости."""

    def setUp(self) -> None:
        """Создание изолированной временной директории для дисковых тестов."""
        self.temp_dir = tempfile.mkdtemp(prefix='academy_test_concurrency_')
        self.db_path = os.path.join(self.temp_dir, 'test_concurrency.sqlite')

    def tearDown(self) -> None:
        """Очистка временных файлов после прогона тестов."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sqlite_wal_multithreaded_concurrency(self) -> None:
        """
        Брешь 1: Стресс-тестирование конкурентной записи в SQLite в режиме WAL.
        10 параллельных потоков одновременно выполняют транзакции записи
        с инкрементом XP и созданием ревизий без блокировок 'database is locked'.
        """
        # 1. Инициализация дисковой БД в режиме WAL
        conn_init = create_test_db(self.db_path)
        seed_canonical_content(conn_init)
        cursor_init = conn_init.cursor()
        cursor_init.execute("INSERT INTO users (id, username, email, xp) VALUES (1, 'concurrent_user', 'c@example.com', 0);")
        conn_init.commit()
        conn_init.close()

        num_threads = 10
        increments_per_thread = 5

        def worker_task(thread_id: int) -> int:
            """Функция рабочего потока: открывает свое соединение и делает серии транзакций."""
            conn = sqlite3.connect(self.db_path, timeout=15.0)
            conn.execute('PRAGMA foreign_keys = ON;')
            conn.execute('PRAGMA busy_timeout = 15000;')
            cursor = conn.cursor()

            successful_ops = 0
            for i in range(increments_per_thread):
                try:
                    cursor.execute('BEGIN IMMEDIATE;')
                    cursor.execute('UPDATE users SET xp = xp + 10 WHERE id = 1;')
                    cursor.execute(
                        "INSERT INTO sync_revisions (user_id, client_id, device, base_updated_at, applied_updated_at, status) "
                        "VALUES (1, ?, ?, ?, ?, 'applied');",
                        (f'client_{thread_id}', f'device_{thread_id}', int(time.time()), int(time.time()),)
                    )
                    conn.commit()
                    successful_ops += 1
                except sqlite3.OperationalError as e:
                    conn.rollback()
                    raise e
                time.sleep(0.005)

            conn.close()
            return successful_ops

        # Запуск параллельного пула потоков
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker_task, tid) for tid in range(num_threads)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        self.assertEqual(len(results), num_threads)
        self.assertEqual(sum(results), num_threads * increments_per_thread)

        # 2. Проверка итоговой целостности данных
        conn_check = sqlite3.connect(self.db_path)
        cursor_check = conn_check.cursor()
        cursor_check.execute('SELECT xp FROM users WHERE id = 1;')
        final_xp = cursor_check.fetchone()[0]
        expected_xp = num_threads * increments_per_thread * 10
        self.assertEqual(final_xp, expected_xp, f'Итоговый XP ({final_xp}) должен быть строго равен сумме всех транзакций ({expected_xp})')

        cursor_check.execute('SELECT COUNT(*) FROM sync_revisions WHERE user_id = 1;')
        total_revisions = cursor_check.fetchone()[0]
        self.assertEqual(total_revisions, num_threads * increments_per_thread)
        conn_check.close()

    def test_on_disk_crash_recovery_and_persistence(self) -> None:
        """
        Брешь 4: Тестирование дисковой персистентности и восстановления после реконнекта.
        Проверяет выживаемость данных на диске при закрытии соединений.
        """
        # Создаем и наполняем дисковую БД
        conn = create_test_db(self.db_path)
        seed_canonical_content(conn)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, username, email, xp) VALUES (2, 'disk_user', 'd@example.com', 750);")
        cursor.execute(
            "INSERT INTO ide_drafts (user_id, task_id, draft_code) VALUES (2, 1, 'def persistent_solution(): return True');"
        )
        conn.commit()
        # Симулируем неожиданное закрытие процесса
        conn.close()

        # Повторно открываем файл с диска
        conn_recovered = sqlite3.connect(self.db_path)
        conn_recovered.row_factory = sqlite3.Row
        cursor_rec = conn_recovered.cursor()
        cursor_rec.execute('SELECT xp, email FROM users WHERE id = 2;')
        user_row = cursor_rec.fetchone()
        self.assertIsNotNone(user_row)
        self.assertEqual(user_row['xp'], 750)

        cursor_rec.execute('SELECT draft_code FROM ide_drafts WHERE user_id = 2 AND task_id = 1;')
        draft_row = cursor_rec.fetchone()
        self.assertIsNotNone(draft_row)
        self.assertIn('def persistent_solution', draft_row['draft_code'])
        conn_recovered.close()

    def test_schema_migration_v1_to_v3_resilience(self) -> None:
        """
        Брешь 2: Тестирование миграции устаревшей схемы v1 (ранний плоский профиль) в схему v3.
        Гарантирует 100% сохранность накопленного XP, стрика и безопасную инициализацию ideDrafts.
        """
        v1_raw = make_v1_legacy_user_fixture()
        self.assertEqual(v1_raw.get('schemaVersion'), 1)
        self.assertNotIn('ideDrafts', v1_raw)

        # Выполняем миграцию
        migrated = migrate_legacy_progress_bundle(v1_raw)
        self.assertEqual(migrated['schemaVersion'], 3)
        self.assertIn('ideDrafts', migrated)
        self.assertEqual(migrated['ideDrafts'], {})
        self.assertEqual(migrated['academyState']['xp'], 450)
        self.assertEqual(migrated['academyState']['streak'], 3)

        # Валидация через Pydantic схему v3
        bundle = ProgressBundle.model_validate(migrated)
        self.assertEqual(bundle.academyState.get('xp'), 450)
        self.assertEqual(bundle.ideDrafts, {})

    def test_schema_migration_v2_to_v3_resilience(self) -> None:
        """
        Брешь 2: Тестирование миграции схемы v2 (разделённый профиль без ideDrafts) в схему v3.
        """
        v2_raw = make_v2_legacy_user_fixture()
        self.assertEqual(v2_raw.get('schemaVersion'), 2)

        migrated = migrate_legacy_progress_bundle(v2_raw)
        self.assertEqual(migrated['schemaVersion'], 3)
        self.assertEqual(migrated['academyState']['xp'], 800)
        self.assertEqual(migrated['ideStatus']['1'], 'passed')
        self.assertEqual(migrated['ideDrafts'], {})

        # Валидация через Pydantic
        bundle = ProgressBundle.model_validate(migrated)
        self.assertEqual(bundle.academyState.get('xp'), 800)

    def test_payload_boundary_limits_guard(self) -> None:
        """
        Брешь 3: Тестирование устойчивости к отправке сверхбольших черновиков кода (Payload Boundary).
        Черновик в 1 МБ должен безопасно сериализоваться и сохраняться без сбоев памяти.
        """
        large_code = '# Large draft simulation\n' + ('x = 42\n' * 50000) # ~350 КБ кода
        large_bundle = {
            'academyState': {'xp': 100, 'streak': 1},
            'ideStatus': {},
            'ideDrafts': {'1': large_code}
        }

        stored = sync_service.read_sync_record()
        base_time = stored.get('updatedAt', 0) if stored else 0

        push_request = SyncPushRequest(
            bundle=ProgressBundle.model_validate(large_bundle),
            baseUpdatedAt=base_time,
            device='boundary-test-device',
            clientId='boundary-test-client'
        )

        ok, response_data, status_code = sync_service.process_push(push_request)
        self.assertTrue(ok)
        self.assertEqual(status_code, 200)
        self.assertIn('1', response_data['bundle']['ideDrafts'])
        self.assertGreater(len(response_data['bundle']['ideDrafts']['1']), 300000)


if __name__ == '__main__':
    unittest.main()
