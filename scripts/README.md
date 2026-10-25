# 🛠️ Скрипты конвейера Python Backend Academy

Директория содержит мастер-сборщики курса, генераторы контента, валидаторы целостности и регрессионный сьют тестов.

---

## 🧭 Реестр активных инструментов

### 1. Ядро сборки и синхронизации
| Скрипт | Назначение |
|---|---|
| [`build.py`](build.py) | **Главный мастер-пайплайн сборки**: валидация JSON-схем, компиляция CSS, проверка побайтовой синхронизации эталонов |
| [`assemble_academy.py`](assemble_academy.py) | Конструктор монолитного SPA `academy.html` из исходных шаблонов и контента |
| [`export_canonical_content.py`](export_canonical_content.py) | Экспорт канонических данных из монолита в структурированные файлы `data/content/` |
| [`sync_etalons.py`](sync_etalons.py) | Синхронизация канонического эталона (`standards/standards.html`) |
| [`install_hooks.py`](install_hooks.py) | Установка Git pre-commit хуков локального контроля качества |

### 2. Экстракторы и генераторы контента
| Скрипт | Назначение |
|---|---|
| [`extract_remnote_data.py`](extract_remnote_data.py) | Экстрактор 401 задачи кода и конспектов из платиновой базы знаний RemNote |
| [`build_python_mastery.py`](build_python_mastery.py) | Конструктор матрицы компетенций и метаданных навыков Python Core |
| [`build_task_tests.py`](build_task_tests.py) | Генератор изолированных тест-кейсов и проверок для IDE |
| [`generate_new_lessons.py`](generate_new_lessons.py) | Генератор микро-шагов теории и практических заданий |
| `split_and_enrich_mod2.py` | Модуль 2: Сетевой фундамент, HTTP и REST API |
| `enrich_backend_mod3.py` | Модуль 3: FastAPI и Django Backend |
| `enrich_algo_mod4.py` | Модуль 4: Алгоритмы и структуры данных |
| `enrich_db_mod5.py` | Модуль 5: PostgreSQL, Индексы и ORM |
| `enrich_arch_mod6.py` | Модуль 6: Чистая архитектура, SOLID и паттерны |
| `enrich_infra_mod7.py` | Модуль 7: Docker, CI/CD, Celery и очереди |

### 3. Автоматический контроль качества и регрессия
| Скрипт | Назначение |
|---|---|
| [`quick_precommit_check.py`](quick_precommit_check.py) | Быстрая проверка синтаксиса и целостности перед коммитом |
| [`verify_academy.py`](verify_academy.py) | Валидатор целостности структуры SPA и отсутствия битых ссылок |
| [`verify_platinum.py`](verify_platinum.py) | Комплексная проверка платиновых инвариантов базы знаний |
| [`test_all_401_tasks.py`](test_all_401_tasks.py) | Прогон сквозного набора тестов для всех 401 задач тренажёра |
| [`audit_pipeline.py`](audit_pipeline.py) | Параллельный запуск всех этапов тестирования платформы |
| [`test_coddy_interface.js`](test_coddy_interface.js) | Стресс-тест эргономики интерфейса (тропа, свайпы, Single Dominant CTA) |
| [`test_pwa_offline.js`](test_pwa_offline.js) | Тестирование PWA, Service Worker и офлайн-кэширования |
| [`visual_test.js`](visual_test.js) | Визуальное регрессионное тестирование по 40 эталонным снимкам |
| [`audit_pedagogy_benchmark.js`](audit_pedagogy_benchmark.js) | Педагогический аудит плотности шагов и скаффолдинга |
| [`take_quantized_screenshots.js`](take_quantized_screenshots.js) | Снятие снимков экранов через Headless Chrome CDP |

### 4. Канонические шаблоны и локальный сервер
- `academy.orig.html` — Базовый эталонный HTML-каркас SPA
- `canonical_extra_css.css` — Канонический стилевой модуль оформления
- `canonical_template_js.js` — Ядро клиентского SPA-шаблонизатора
- `canonical_unit_tests.json` — Нормализованный реестр проверочных тестов
- `server.js` — Легковесный локальный Node.js сервер для PWA и синхронизации с мобильных устройств
- `visual_baselines/` — 40 эталонных скриншотов всех маршрутов для регрессионных тестов

---

## 🗄️ Архив
Исторические одноразовые скрипты миграций и специфические зонды вынесены в подкаталог [`archive/`](archive/):
- `archive/migrations/` — выполненные миграции данных и дескрипторов
- `archive/legacy_diagnostics/` — разовая отладка компонентов
