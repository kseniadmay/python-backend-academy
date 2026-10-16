# Скрипты конвейера Python Backend Academy

В этой директории расположены инструменты сборки курса, автотесты, модуль синхронизации прогресса и конвейер контроля качества.

---

## 1. Ядро сборки платформы (`academy.html`)

| Скрипт | Описание |
|---|---|
| `assemble_academy.py` | Главный мастер-сборщик: объединяет базу знаний RemNote, задачи IDE, рубежные тесты и SPA-шаблон в монолит `academy.html` |
| `academy.orig.html` | Базовый эталонный HTML-каркас SPA (стили «Вечерний Обсидиан», компоненты, плеер тестов и IDE) |
| `extract_remnote_data.py` | Экстрактор и валидатор 401 задачи кода и конспектов из исходных материалов |
| `build_python_mastery.py` | Конструктор матрицы компетенций и метаданных 28 навыков Python Core |
| `build_task_tests.py` | Генератор изолированных тест-кейсов и AST-проверок для тренажёра IDE |
| `generate_new_lessons.py` | Генератор микро-шагов теории и практических заданий |
| `sync_etalons.py` | Синхронизатор утверждённого билда `academy.html` с канонической папкой `Эталоны/` |

---

## 2. Обогащение треков и модулей платформы

Скрипты инкрементального обогащения конспектов и задач по направлениям бэкенда:
- `split_and_enrich_mod2.py` — Модуль 2: Web & HTTP
- `enrich_backend_mod3.py` — Модуль 3: FastAPI & Django Backend
- `enrich_algo_mod4.py` — Модуль 4: Алгоритмы и структуры данных
- `enrich_db_mod5.py` — Модуль 5: PostgreSQL, Индексы и ORM
- `enrich_arch_mod6.py` — Модуль 6: Архитектура, Clean Architecture, Паттерны
- `enrich_infra_mod7.py` — Модуль 7: Docker, CI/CD, Очереди Celery, Мониторинг

---

## 3. Конвейер верификации и автотесты

Вызываются через мастер-раннер в корне `python verify_all.py --quick`:

| Скрипт | Этап конвейера |
|---|---|
| `verify_platinum.py` | **[1/6]** Аудит 525 файлов Markdown базы RemNote (конспекты, колоды карточек, ссылки) |
| `tests/test_bugs_regression.js` | **[2/6]** Сквозные инварианты DOM, 80/80 регрессионных тестов и канонические эталоны |
| `test_pwa_offline.js` | **[3/6]** Проверка Service Worker (`sw.js`), кэширования и PWA Manifest |
| `verify_academy.py` | **[4/6]** Синтаксический аудит JS, запуск экранов в Headless Chrome без ошибок консоли |
| `test_all_401_tasks.py` | **[5/6]** Автопрогон всех 401 задач IDE и 459 сниппетов Python 3.13 в среде Brython |
| `visual_test.js` | **[6/6]** Снятие скриншотов всех маршрутов (десктоп/мобайл) и сравнение с `visual_baselines/` |
| `test_coddy_interface.js` | Комплексный стресс-тест философии Coddy (3D-тропа, свайпы, Single CTA) |
| `audit_pipeline.py` | Комплексный автоматический аудит и параллельный запуск всех тестов |
| `visual_baselines/` | Директория канонических скриншотов эталонов для pixel-diff |

---

## 4. Сервер синхронизации прогресса

- `server.js` — Легковесный Node.js сервер REST API для межплатформенной синхронизации прогресса (Desktop ↔ Mobile) с поддержкой локального JSON-хранилища (`data/progress_sync.json`) и облачной PostgreSQL (Neon).

---

## 5. Контроль качества Git

- `install_hooks.py` — Установка pre-commit хука валидации синтаксиса в `.git/hooks`.
- `quick_precommit_check.py` — Быстрый pre-commit аудит синтаксиса JS, Python, HTML и JSON.
