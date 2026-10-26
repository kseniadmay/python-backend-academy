# -*- coding: utf-8 -*-
"""
Тестовый комплекс реляционной базы данных и фикстур платформы (SQLite).
Проверяет целостность схемы, внешние ключи, транзакции, индексы,
инварианты сохранения черновиков IDE и алгоритм интервального повторения SRS.
"""

import json
import os
import sqlite3
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tests.fixtures.fixture_factory import (
    create_test_db,
    seed_canonical_content,
    make_fresh_user_fixture,
    make_intermediate_user_fixture,
    make_advanced_user_fixture,
    make_conflict_user_fixture,
    make_corrupted_user_fixture,
)
from backend.app.schemas.progress import ProgressBundle


class TestBackendDatabase(unittest.TestCase):
    """Набор тестов реляционной структуры SQLite и фабрики фикстур."""

    def setUp(self) -> None:
        """Инициализация изолированной in-memory тестовой БД перед каждым тестом."""
        self.conn = create_test_db(':memory:')
        seed_canonical_content(self.conn)

    def tearDown(self) -> None:
        """Закрытие соединения с БД."""
        self.conn.close()

    def test_schema_tables_exist(self) -> None:
        """Проверка создания всех 9 канонических таблиц схемы."""
        expected_tables = {
            'users', 'modules', 'units', 'tasks',
            'user_progress', 'srs_cards', 'ide_drafts',
            'sync_revisions', 'feedback_reports'
        }
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        existing_tables = {row[0] for row in cursor.fetchall()}
        self.assertTrue(expected_tables.issubset(existing_tables), f'Missing tables: {expected_tables - existing_tables}')

    def test_foreign_key_enforcement(self) -> None:
        """Проверка соблюдения целостности связей: вставка зависимой записи с некорректным FK вызывает IntegrityError."""
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO tasks (id, unit_id, title, level, solution_code, test_code) VALUES (?, ?, ?, ?, ?, ?);",
                (999, 'non_existent_unit', 'Test Task', 1, 'pass', 'assert True')
            )

    def test_canonical_modules_and_units_integrity(self) -> None:
        """Проверка наполнения 7 каноническими направлениями и их эшелонами."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, slug, echelon FROM modules ORDER BY order_num;')
        modules = cursor.fetchall()
        self.assertEqual(len(modules), 7)
        self.assertEqual(modules[0]['slug'], 'python')
        self.assertEqual(modules[0]['echelon'], 1)
        self.assertEqual(modules[6]['slug'], 'infra')
        self.assertEqual(modules[6]['echelon'], 4)

        # Проверка связей с юнитами
        cursor.execute("SELECT COUNT(*) FROM units WHERE module_id = '01';")
        python_units_count = cursor.fetchone()[0]
        self.assertEqual(python_units_count, 9)

    def test_non_destructive_peeking_ide_drafts(self) -> None:
        """
        Инвариант 1.16.2: Неразрушающий возврат по бусинам (Non-Destructive Peeking).
        Черновик кода пользователя в Zen IDE обязан надежно сохраняться в БД и возвращаться без потерь.
        """
        cursor = self.conn.cursor()
        # Создаем тестового пользователя
        cursor.execute(
            "INSERT INTO users (username, email, xp, streak) VALUES ('alex_dev', 'alex@example.com', 100, 2);"
        )
        user_id = cursor.lastrowid

        student_code = 'class StrictDescriptor:\n    # Незаконченное решение студента\n    def __get__(self, inst, owner):\n        return 42'

        # Сохранение черновика
        cursor.execute(
            "INSERT INTO ide_drafts (user_id, task_id, draft_code) VALUES (?, ?, ?);",
            (user_id, 4, student_code)
        )
        self.conn.commit()

        # Чтение черновика при повторном открытии задачи
        cursor.execute("SELECT draft_code FROM ide_drafts WHERE user_id = ? AND task_id = ?;", (user_id, 4))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['draft_code'], student_code)

    def test_srs_daily_due_stream_algorithm(self) -> None:
        """
        Проверка выборки Pure Daily Due Stream в БД SQLite:
        выбираются строго карточки с due_date <= today.
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES ('srs_learner', 'srs@example.com');")
        user_id = cursor.lastrowid

        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Добавляем 3 карточки: просроченную, сегодняшнюю и будущую
        cards_data = [
            (user_id, 'Ф-001', 0, 2.5, 1, 1, yesterday.isoformat()),
            (user_id, 'Ф-001', 1, 2.5, 1, 1, today.isoformat()),
            (user_id, 'Ф-002', 0, 2.5, 3, 2, tomorrow.isoformat()),
        ]
        cursor.executemany(
            "INSERT INTO srs_cards (user_id, deck_id, card_idx, ease_factor, interval_days, repetitions, due_date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);",
            cards_data
        )
        self.conn.commit()

        # Запрос суточной очереди повторения
        cursor.execute(
            "SELECT deck_id, card_idx, due_date FROM srs_cards "
            "WHERE user_id = ? AND due_date <= ? ORDER BY due_date ASC;",
            (user_id, today.isoformat())
        )
        due_cards = cursor.fetchall()
        self.assertEqual(len(due_cards), 2, 'В суточную очередь должны попасть только просроченные и сегодняшние карточки')
        self.assertEqual(due_cards[0]['deck_id'], 'Ф-001')
        self.assertEqual(due_cards[0]['card_idx'], 0)

    def test_acid_transaction_atomic_rollback(self) -> None:
        """Проверка атомарного отката транзакции при возникновении сбоя."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, email, xp) VALUES ('tx_user', 'tx@example.com', 500);")
        user_id = cursor.lastrowid
        self.conn.commit()

        try:
            # Начинаем составное обновление: начисление XP и попытка записи с ошибкой FK
            cursor.execute("UPDATE users SET xp = xp + 100 WHERE id = ?;", (user_id,))
            cursor.execute(
                "INSERT INTO user_progress (user_id, unit_id, status) VALUES (?, 'invalid_unit_999', 'mastered');",
                (user_id,)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()

        # Проверяем, что XP не изменился (откатился)
        cursor.execute("SELECT xp FROM users WHERE id = ?;", (user_id,))
        xp = cursor.fetchone()['xp']
        self.assertEqual(xp, 500, 'При ошибке транзакция обязана полностью откатиться')

    def test_fixture_factory_fresh_state_validation(self) -> None:
        """Валидация фикстуры чистого новичка: 0 XP, streak 0, Friendly 0 XP."""
        fresh = make_fresh_user_fixture()
        bundle = ProgressBundle.model_validate(fresh)
        self.assertEqual(bundle.academyState.get('xp'), 0)
        self.assertEqual(bundle.academyState.get('streak'), 0)
        self.assertEqual(len(bundle.academyState.get('completedLessons', [])), 0)

    def test_fixture_factory_intermediate_state_validation(self) -> None:
        """Валидация фикстуры продвигающегося студента: стрик 7, закрытые уроки и карточки."""
        inter = make_intermediate_user_fixture()
        bundle = ProgressBundle.model_validate(inter)
        self.assertEqual(bundle.academyState.get('xp'), 1250)
        self.assertEqual(bundle.academyState.get('streak'), 7)
        self.assertIn('1.1', bundle.academyState.get('completedLessons', []))
        self.assertIn('3', bundle.ideDrafts)

    def test_fixture_factory_corrupted_state_detection(self) -> None:
        """Проверка детекции поврежденных данных фикстуры make_corrupted_user_fixture."""
        corrupted = make_corrupted_user_fixture()
        with self.assertRaises(Exception):
            ProgressBundle.model_validate(corrupted)


if __name__ == '__main__':
    unittest.main()
