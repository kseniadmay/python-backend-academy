# 🧪 Автотесты и верификационный сьют платформы

В этой директории расположен сквозной набор автотестов, предотвращающий возникновение регрессий и проверяющий соблюдение утверждённых канонических эталонов интерфейса **Python Backend Academy**.

---

## 📋 Состав сьюта тестов

| Файл / Каталог | Описание |
|---|---|
| [`test_helpers.js`](test_helpers.js) | **Единый DRY-модуль тестового контекста**: централизованные пути, однократное кэшированное чтение `academy.html` / `standards.html` / `PROJECT_CONTEXT.md` / `AGENTS.md`, парсинг `PY_MASTERY` и проверка `Invariant 0`. |
| [`test_descriptor_suite.js`](test_descriptor_suite.js) | **Сьют Строгого Дескриптора (17 инвариантов)**: побайтовое соответствие эталонов, Clean Human UI, Active Rescue, Non-Destructive Peeking, Execution Watchdog 2000ms, iOS Zoom Guard 16px, Single Dominant CTA, запрет 3D/Coddy, фикстуры и DDL схемы. |
| [`test_backend_database.py`](test_backend_database.py) | **Тестовый комплекс реляционной базы данных (SQLite)**: валидация схемы 9 таблиц, ACID-транзакции, откат при сбоях, внешние ключи, индексация, алгоритм SRS и сохранение черновиков IDE. |
| [`test_backend_concurrency.py`](test_backend_concurrency.py) | **Стресс-тесты конкурентности и отказоустойчивости**: многопоточная запись в SQLite (режим WAL, 10 потоков без блокировок), миграция схем v1/v2 ➔ v3, краш-рекавери на диске и лимиты полезной нагрузки. |
| [`test_backend_api.py`](test_backend_api.py) | **Модульные тесты FastAPI API**: интеграционный запуск тестов REST API, синхронизации и сервисов из корня репозитория (29 тестов). |
| [`test_bugs_regression.js`](test_bugs_regression.js) | **Главный регрессионный сьют**: комплексный прогон всех 146 багов, канонических бенчмарков и сьюта Строгого Дескриптора со 100% PASS. |
| [`test_pravki_spec.js`](test_pravki_spec.js) | **Спецификация канонических эталонов интерфейса**: теория, флешкарты SRS, практика со сплит-вью, модалка рубежного теста, дашборд и микрообучение. |
| [`test_dashboard_regression.js`](test_dashboard_regression.js) | Регрессионный тест дашборда: лаконичный вид, кокон фокуса, сегментный прогресс и адаптивность. |
| [`test_cards_trainer_regression.js`](test_cards_trainer_regression.js) | Тестирование механики флешкарт: интервальное повторение SRS, перевороты, оценка «Не знаю» и начисление XP. |
| [`test_notes_presentation_regression.js`](test_notes_presentation_regression.js) | Контроль типографики ридера конспектов: Onest, отступы, подсветка синтаксиса и Single CTA. |
| [`test_skill_screen_regression.js`](test_skill_screen_regression.js) | Тестирование экрана навыков, цепи микро-шагов и дерева эшелонов. |
| [`test_server_api.js`](test_server_api.js) | Интеграционное тестирование Node.js сервера (`scripts/server.js`): REST API v1, синхронизация прогресса, очередь замечаний и редирект IDE. |
| [`fixtures/`](fixtures/) | **Каноническая база фикстур и DDL-схема тестовой БД**: `test_db_schema.sql`, `fixture_factory.py`, 8 эталонных профилей (fresh, intermediate, advanced, conflict, corrupted, v1_legacy, v2_legacy, backup). |

---

## 🚀 Запуск тестов

```bash
# 1. Запуск сьюта Строгого Дескриптора (17 архитектурных инвариантов)
node tests/test_descriptor_suite.js

# 2. Запуск полного инженерного бэкенд-комплекса (29 тестов: REST, SQLite, Concurrency WAL, Migrations)
python -m unittest tests/test_backend_api.py

# 3. Запуск комплексного регрессионного сьюта (163 проверки)
node tests/test_bugs_regression.js

# 4. Запуск полного конвейера верификации
python verify_all.py --quick
```
