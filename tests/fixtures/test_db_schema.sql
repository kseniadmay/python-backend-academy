-- ==============================================================================
-- Каноническая схема реляционной тестовой базы данных Python Backend Academy
-- Стандарт: SQLite 3.35+ (WAL-mode, Foreign Keys ON, Strict Typing)
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    xp INTEGER NOT NULL DEFAULT 0,
    streak INTEGER NOT NULL DEFAULT 0,
    best_streak INTEGER NOT NULL DEFAULT 0,
    theme TEXT NOT NULL DEFAULT 'dark' CHECK(theme IN ('dark', 'light')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Таблица модулей (7 канонических направлений платформы)
CREATE TABLE IF NOT EXISTS modules (
    id TEXT PRIMARY KEY, -- '01', '02', ..., '07'
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    echelon INTEGER NOT NULL CHECK(echelon BETWEEN 1 AND 4),
    order_num INTEGER NOT NULL UNIQUE
);

-- 3. Таблица юнитов (45 тем академической тропы)
CREATE TABLE IF NOT EXISTS units (
    id TEXT PRIMARY KEY, -- '1.1', '1.2', ..., '7.6'
    module_id TEXT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    slug TEXT NOT NULL,
    order_num INTEGER NOT NULL,
    total_skills INTEGER NOT NULL DEFAULT 0
);

-- 4. Таблица практических задач (401 задача Zen IDE)
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY, -- 1..401
    unit_id TEXT NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 5),
    solution_code TEXT NOT NULL,
    test_code TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 5. Таблица прогресса пользователя по юнитам
CREATE TABLE IF NOT EXISTS user_progress (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    unit_id TEXT NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'not_started' CHECK(status IN ('not_started', 'in_progress', 'mastered')),
    mastered_skills INTEGER NOT NULL DEFAULT 0,
    unit_test_passed BOOLEAN NOT NULL DEFAULT 0,
    unit_test_score REAL NOT NULL DEFAULT 0.0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id)
);

-- 6. Таблица карточек интервального повторения (SRS-алгоритм)
CREATE TABLE IF NOT EXISTS srs_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    deck_id TEXT NOT NULL, -- Канонический ID колоды
    card_idx INTEGER NOT NULL,
    ease_factor REAL NOT NULL DEFAULT 2.5,
    interval_days INTEGER NOT NULL DEFAULT 0,
    repetitions INTEGER NOT NULL DEFAULT 0,
    due_date DATE NOT NULL,
    last_rating INTEGER DEFAULT NULL CHECK(last_rating IS NULL OR last_rating BETWEEN 0 AND 3),
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, deck_id, card_idx)
);

-- 7. Таблица черновиков кода в Zen IDE (Non-Destructive Peeking Invariant)
CREATE TABLE IF NOT EXISTS ide_drafts (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    draft_code TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, task_id)
);

-- 8. Таблица аудита синхронизации и защиты от Lost Update (409 Conflict Guard)
CREATE TABLE IF NOT EXISTS sync_revisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id TEXT NOT NULL,
    device TEXT NOT NULL,
    base_updated_at INTEGER NOT NULL,
    applied_updated_at INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('applied', 'conflict')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 9. Очередь обратной связи и отчетов об ошибках
CREATE TABLE IF NOT EXISTS feedback_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    context TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- Индексы для обеспечения производительности O(1) и O(log n)
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_units_module ON units(module_id);
CREATE INDEX IF NOT EXISTS idx_tasks_unit ON tasks(unit_id);
CREATE INDEX IF NOT EXISTS idx_tasks_level ON tasks(level);
CREATE INDEX IF NOT EXISTS idx_user_progress_status ON user_progress(user_id, status);
CREATE INDEX IF NOT EXISTS idx_srs_due_date ON srs_cards(user_id, due_date);
CREATE INDEX IF NOT EXISTS idx_srs_deck ON srs_cards(user_id, deck_id);
CREATE INDEX IF NOT EXISTS idx_sync_revisions_user ON sync_revisions(user_id, applied_updated_at DESC);
