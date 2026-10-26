# 📦 Тестовая база данных и фикстуры (Test Database & Fixtures)

В данном каталоге сосредоточена эталонная база реляционных данных и канонических фикстур для тестирования бэкенда, API и механизмов сохранения прогресса платформы Python Backend Academy.

---

## 🗄️ Состав каталога

1. **`test_db_schema.sql`**  
   Канонический DDL-скрипт SQLite со строгой типизацией, поддержкой внешних ключей (`PRAGMA foreign_keys = ON`) и индексацией:
   - `users`: профили пользователей, стрик, опыт (XP), тема оформления;
   - `modules`: 7 направлений платформы (Python Core, Web, Backend, Algo, DB, Arch, Infra);
   - `units`: 45 тем академической тропы;
   - `tasks`: 401 задача Zen IDE с уровнями сложности и эталонными решениями;
   - `user_progress`: статус прохождения тем, баллы и рубежные зачеты;
   - `srs_cards`: карточки интервального повторения (ease factor, interval, reps, due date);
   - `ide_drafts`: черновики кода в Zen IDE (инвариант *Non-Destructive Peeking*);
   - `sync_revisions`: аудит синхронизации и защита от *Lost Update (409 Conflict Guard)*;
   - `feedback_reports`: очередь обратной связи и отчетов об ошибках.

2. **`fixture_factory.py`**  
   Фабрика тестовых данных на чистом Python:
   - `create_test_db(db_path=':memory:')`: создание БД (с поддержкой режима WAL для дисковых баз) и накат схемы;
   - `seed_canonical_content(conn)`: наполнение модулями, юнитами и базовыми задачами;
   - `migrate_legacy_progress_bundle(raw)`: адаптер бесшовной миграции устаревших схем v1 / v2 в каноническую схему v3;
   - `make_fresh_user_fixture()`: новичок первого дня (0 XP, пустой стрик, без ошибок);
   - `make_intermediate_user_fixture()`: активный студент Главы 1 (1250 XP, стрик 7, очередь SRS);
   - `make_advanced_user_fixture()`: студент 4-го эшелона (9400 XP, сданные рубежные тесты);
   - `make_conflict_user_fixture()`: устаревший `baseUpdatedAt` для проверки HTTP 409;
   - `make_corrupted_user_fixture()`: поврежденная структура для стресс-тестов валидации;
   - `make_v1_legacy_user_fixture()`: слепок устаревшей схемы v1 (без `ideDrafts`);
   - `make_v2_legacy_user_fixture()`: слепок схемы v2 (без `ideDrafts`);
   - `export_all_fixtures_to_disk()`: синхронная выгрузка JSON-файлов на диск.

3. **Канонические JSON-фикстуры (8 файлов)**:
   - `user_progress_fresh.json`: состояние чистого старта;
   - `user_progress_intermediate.json`: состояние уверенного продвижения;
   - `user_progress_advanced.json`: продвинутое состояние студента;
   - `user_progress_conflict.json`: сценарий конфликта версий;
   - `user_progress_corrupted.json`: сценарий некорректного формата;
   - `user_progress_v1_legacy.json`: устаревший профиль версии 1;
   - `user_progress_v2_legacy.json`: устаревший профиль версии 2;
   - `user_progress_backup.json`: архивный слепок боевого состояния.

---

## 🚀 Запуск тестов базы данных

```bash
# Тесты реляционной структуры, ACID и SRS
python -m unittest tests/test_backend_database.py

# Стресс-тесты конкурентности (WAL), миграции схем и лимитов памяти
python -m unittest tests/test_backend_concurrency.py

# Полный прогон всех бэкенд-тестов (29 тестов)
python -m unittest tests/test_backend_api.py
```
