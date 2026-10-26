# -*- coding: utf-8 -*-
"""
Фабрика тестовых данных и фикстур для Python Backend Academy.

Предоставляет утилиты для:
1. Инициализации и наполнения реляционной SQLite БД (in-memory или на диске).
2. Генерации канонических состояний пользователя:
   - Fresh (чистый старт, День 1, 0 XP);
   - Intermediate (Глава 1, активный стрик, карточки SRS due today);
   - Advanced (высокий уровень, 4 эшелона, черновики Zen IDE);
   - Conflict (устаревший baseUpdatedAt для проверки 409 Conflict);
   - Corrupted (повреждённая структура для проверки отказоустойчивости);
   - V1 Legacy & V2 Legacy (устаревшие версии схем для проверки миграции).
3. Функций миграции и валидации легаси-бандлов в схему v3.
4. Экспорта и импорта состояний между JSON-бандлом платформы и реляционной БД.
"""

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

_CURRENT_DIR = Path(__file__).resolve().parent
_SCHEMA_PATH = _CURRENT_DIR / 'test_db_schema.sql'


def get_schema_sql() -> str:
    """Возвращает SQL DDL схему тестовой базы данных."""
    with open(_SCHEMA_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def create_test_db(db_path: str = ':memory:') -> sqlite3.Connection:
    """
    Создаёт SQLite базу данных и применяет каноническую DDL-схему.
    Автоматически включает режим PRAGMA foreign_keys = ON и busy_timeout.
    Если база создаётся на диске, включает режим WAL.
    """
    if db_path != ':memory:':
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')

    if db_path != ':memory:':
        conn.execute('PRAGMA journal_mode = WAL;')

    schema_sql = get_schema_sql()
    conn.executescript(schema_sql)
    conn.commit()
    return conn


def seed_canonical_content(conn: sqlite3.Connection) -> None:
    """
    Наполняет тестовую базу 7 каноническими модулями и начальными юнитами.
    """
    modules_data = [
        ('01', 'python', 'Python Core & CPython Memory', 1, 1),
        ('02', 'web', 'Web, HTTP & Protocols', 1, 2),
        ('03', 'backend', 'Asyncio, FastAPI & Highload', 2, 3),
        ('04', 'algorithms', 'Algorithms & Data Structures', 2, 4),
        ('05', 'databases', 'PostgreSQL, SQLAlchemy & Redis', 3, 5),
        ('06', 'architecture', 'Clean Architecture, DDD & Patterns', 3, 6),
        ('07', 'infra', 'Docker, CI/CD & Linux Systems', 4, 7),
    ]

    units_data = [
        ('1.1', '01', 'Память, переменные и базовые типы', 'memory-basics', 1, 13),
        ('1.2', '01', 'Функции, замыкания и декораторы', 'functions-closures', 2, 8),
        ('1.3', '01', 'Генераторы, итераторы и itertools', 'generators-iterators', 3, 7),
        ('1.4', '01', 'ООП, MRO и протоколы данных', 'oop-protocols', 4, 8),
        ('1.5', '01', 'Исключения, менеджеры контекста и EAFP', 'exceptions-context', 5, 8),
        ('1.6', '01', 'Дескрипторы и метаклассы', 'descriptors-metaclasses', 6, 8),
        ('1.7', '01', 'CPython internals и модель памяти', 'cpython-internals', 7, 8),
        ('1.8', '01', 'Многопоточность, GIL и конкурентность', 'gil-concurrency', 8, 8),
        ('1.9', '01', 'Статическая типизация и MyPy', 'typing-mypy', 9, 8),
        ('2.1', '02', 'HTTP/1.1, HTTP/2 и семантика запросов', 'http-semantics', 1, 5),
        ('3.1', '03', 'Модель Asyncio Event Loop & Coroutines', 'asyncio-core', 1, 6),
        ('5.1', '05', 'Реляционная модель и SQL DDL/DML', 'sql-basics', 1, 6),
    ]

    tasks_data = [
        (1, '1.1', 'Срезы и инверсия строки', 1, 'def reverse_str(s):\n    return s[::-1]', 'assert reverse_str("hello") == "olleh"'),
        (2, '1.1', 'Генераторы списков и фильтрация четных', 1, 'def evens(nums):\n    return [n for n in nums if n % 2 == 0]', 'assert evens([1, 2, 3, 4]) == [2, 4]'),
        (3, '1.2', 'Декоратор измерения времени', 2, 'def timing_decorator(fn):\n    def wrapper(*args, **kw):\n        return fn(*args, **kw)\n    return wrapper', 'assert callable(timing_decorator(lambda: 42))'),
        (4, '1.6', 'Строгий валидирующий дескриптор', 3, 'class NonNegative:\n    def __set_name__(self, owner, name):\n        self.name = name\n    def __set__(self, instance, value):\n        if value < 0:\n            raise ValueError("Must be non-negative")\n        instance.__dict__[self.name] = value\n    def __get__(self, instance, owner):\n        return instance.__dict__.get(self.name, 0)', 'class Account:\n    val = NonNegative()\na = Account()\na.val = 10\nassert a.val == 10'),
    ]

    cursor = conn.cursor()
    cursor.executemany(
        'INSERT OR IGNORE INTO modules (id, slug, title, echelon, order_num) VALUES (?, ?, ?, ?, ?);',
        modules_data
    )
    cursor.executemany(
        'INSERT OR IGNORE INTO units (id, module_id, title, slug, order_num, total_skills) VALUES (?, ?, ?, ?, ?, ?);',
        units_data
    )
    cursor.executemany(
        'INSERT OR IGNORE INTO tasks (id, unit_id, title, level, solution_code, test_code) VALUES (?, ?, ?, ?, ?, ?);',
        tasks_data
    )
    conn.commit()


def make_fresh_user_fixture() -> Dict[str, Any]:
    """Генерирует состояние чистого новичка (День 1, 0 XP, онбординг)."""
    return {
        'schemaVersion': 3,
        'exportedAt': '2026-10-26T12:00:00.000Z',
        'academyState': {
            'schemaVersion': 3,
            'xp': 0,
            'streak': 0,
            'bestStreak': 0,
            'lastVisit': 'Mon Oct 26 2026',
            'theme': 'dark',
            'dailyGoal': 50,
            'dailyXpByDate': {},
            'completedLessons': [],
            'completedTasks': [],
            'readNotes': [],
            'reviewedDecks': [],
            'passedUnitTests': [],
            'cards': {},
            'diag': {'isFinished': False, 'score': 0, 'gaps': []}
        },
        'ideStatus': {},
        'ideDrafts': {}
    }


def make_intermediate_user_fixture() -> Dict[str, Any]:
    """Генерирует состояние студента середины Главы 1 (Python Core)."""
    today_str = time.strftime('%Y-%m-%d')
    return {
        'schemaVersion': 3,
        'exportedAt': '2026-10-26T12:00:00.000Z',
        'academyState': {
            'schemaVersion': 3,
            'xp': 1250,
            'streak': 7,
            'bestStreak': 7,
            'lastVisit': 'Mon Oct 26 2026',
            'theme': 'dark',
            'dailyGoal': 50,
            'dailyXpByDate': {today_str: 65},
            'completedLessons': ['1.1', '1.2', '1.3'],
            'completedTasks': [1, 2],
            'readNotes': ['К-001', 'К-002', 'К-003', 'К-004', 'К-005'],
            'reviewedDecks': ['Ф-001', 'Ф-002'],
            'passedUnitTests': ['1.1', '1.2'],
            'cards': {
                'Ф-001_c0': {'interval': 1, 'reps': 1, 'ease': 2.5, 'dueDate': today_str, 'lastRating': 2},
                'Ф-001_c1': {'interval': 3, 'reps': 2, 'ease': 2.6, 'dueDate': today_str, 'lastRating': 3},
                'Ф-002_c0': {'interval': 1, 'reps': 1, 'ease': 2.5, 'dueDate': today_str, 'lastRating': 1}
            },
            'diag': {'isFinished': True, 'score': 78, 'gaps': ['descriptors', 'gil']}
        },
        'ideStatus': {'1': 'passed', '2': 'passed'},
        'ideDrafts': {
            '3': 'def timing_decorator(fn):\n    # Черновик студента\n    pass'
        }
    }


def make_advanced_user_fixture() -> Dict[str, Any]:
    """Генерирует состояние продвинутого студента (Эшелон 4, 9400 XP, сданные рубежные зачеты)."""
    return {
        'schemaVersion': 3,
        'exportedAt': '2026-10-26T12:00:00.000Z',
        'academyState': {
            'schemaVersion': 3,
            'xp': 9400,
            'streak': 24,
            'bestStreak': 30,
            'lastVisit': 'Mon Oct 26 2026',
            'theme': 'dark',
            'dailyGoal': 100,
            'dailyXpByDate': {'2026-10-25': 120, '2026-10-26': 180},
            'completedLessons': ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '2.1', '3.1', '5.1'],
            'completedTasks': [1, 2, 3, 4],
            'readNotes': ['К-001', 'К-002', 'К-003', 'К-014', 'К-022', 'К-026'],
            'reviewedDecks': ['Ф-001', 'Ф-002', 'Ф-025', 'Ф-037', 'Ф-041'],
            'passedUnitTests': ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '2.1', '3.1'],
            'cards': {},
            'diag': {'isFinished': True, 'score': 95, 'gaps': []}
        },
        'ideStatus': {'1': 'passed', '2': 'passed', '3': 'passed', '4': 'passed'},
        'ideDrafts': {
            '4': 'class NonNegative:\n    def __set_name__(self, owner, name):\n        self.name = name'
        }
    }


def make_conflict_user_fixture(base_time: int = 1000) -> Dict[str, Any]:
    """Генерирует конфликтный запрос синхронизации для проверки HTTP 409 Conflict."""
    return {
        'bundle': {
            'academyState': {'xp': 500, 'streak': 2},
            'ideStatus': {'1': 'passed'},
            'ideDrafts': {}
        },
        'baseUpdatedAt': base_time,
        'device': 'conflict-mobile-test',
        'clientId': 'conflict-client-test'
    }


def make_corrupted_user_fixture() -> Dict[str, Any]:
    """Генерирует поврежденный бандл для тестирования валидации схем Pydantic."""
    return {
        'schemaVersion': 'INVALID_VERSION',
        'academyState': 'NOT_A_DICT',
        'ideStatus': None
    }


def make_v1_legacy_user_fixture() -> Dict[str, Any]:
    """
    Генерирует профиль устаревшей схемы v1 (ранние версии платформы):
    - schemaVersion = 1
    - Отсутствует блок ideDrafts (неразрушающий возврат ещё не был внедрён)
    - Отсутствует passedUnitTests
    - Плоский массив карточек
    """
    return {
        'schemaVersion': 1,
        'xp': 450,
        'streak': 3,
        'completedLessons': ['1.1', '1.2'],
        'completedTasks': [1],
        'theme': 'dark'
    }


def make_v2_legacy_user_fixture() -> Dict[str, Any]:
    """
    Генерирует профиль переходной схемы v2:
    - schemaVersion = 2
    - academyState отделён от ideStatus, но ideDrafts отсутствует
    """
    return {
        'schemaVersion': 2,
        'academyState': {
            'schemaVersion': 2,
            'xp': 800,
            'streak': 5,
            'completedLessons': ['1.1', '1.2', '1.3'],
            'completedTasks': [1, 2],
            'readNotes': ['К-001', 'К-002']
        },
        'ideStatus': {'1': 'passed', '2': 'passed'}
    }


def migrate_legacy_progress_bundle(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Канонический адаптер миграции устаревших профилей (v1 / v2) в актуальную схему v3.
    Гарантирует 100% сохранение XP, стрика, закрытых уроков и безопасную инициализацию ideDrafts.
    """
    if not isinstance(raw, dict):
        raise ValueError('Raw data must be a dictionary')

    version = raw.get('schemaVersion', 1)

    # 1. Миграция схемы v1 -> v3
    if version == 1 or 'academyState' not in raw:
        academy_state = {
            'schemaVersion': 3,
            'xp': int(raw.get('xp', 0)),
            'streak': int(raw.get('streak', 0)),
            'bestStreak': int(raw.get('bestStreak', raw.get('streak', 0))),
            'lastVisit': str(raw.get('lastVisit', '')),
            'theme': str(raw.get('theme', 'dark')),
            'dailyGoal': 50,
            'dailyXpByDate': raw.get('dailyXpByDate', {}),
            'completedLessons': list(raw.get('completedLessons', [])),
            'completedTasks': list(raw.get('completedTasks', [])),
            'readNotes': list(raw.get('readNotes', [])),
            'reviewedDecks': list(raw.get('reviewedDecks', [])),
            'passedUnitTests': list(raw.get('passedUnitTests', [])),
            'cards': raw.get('cards', {}),
            'diag': raw.get('diag', {'isFinished': False, 'score': 0, 'gaps': []})
        }
        return {
            'schemaVersion': 3,
            'exportedAt': time.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'academyState': academy_state,
            'ideStatus': dict(raw.get('ideStatus', {})),
            'ideDrafts': {}
        }

    # 2. Миграция схемы v2 -> v3
    if version == 2:
        academy_state = dict(raw.get('academyState', {}))
        academy_state['schemaVersion'] = 3
        if 'passedUnitTests' not in academy_state:
            academy_state['passedUnitTests'] = []
        return {
            'schemaVersion': 3,
            'exportedAt': raw.get('exportedAt', time.strftime('%Y-%m-%dT%H:%M:%S.000Z')),
            'academyState': academy_state,
            'ideStatus': dict(raw.get('ideStatus', {})),
            'ideDrafts': dict(raw.get('ideDrafts', {}))
        }

    # 3. Схема v3
    return raw


def export_all_fixtures_to_disk() -> None:
    """Записывает канонические JSON-фикстуры на диск в директорию fixtures."""
    fixtures = {
        'user_progress_fresh.json': make_fresh_user_fixture(),
        'user_progress_intermediate.json': make_intermediate_user_fixture(),
        'user_progress_advanced.json': make_advanced_user_fixture(),
        'user_progress_conflict.json': make_conflict_user_fixture(),
        'user_progress_corrupted.json': make_corrupted_user_fixture(),
        'user_progress_v1_legacy.json': make_v1_legacy_user_fixture(),
        'user_progress_v2_legacy.json': make_v2_legacy_user_fixture(),
    }

    for filename, data in fixtures.items():
        target = _CURRENT_DIR / filename
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    export_all_fixtures_to_disk()
    print('Канонические тестовые фикстуры (включая v1 и v2 legacy) успешно экспортированы на диск.')
