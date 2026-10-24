# 🐍 PYTHON BACKEND ACADEMY

[![Live Platform](https://img.shields.io/badge/platform-Web%20%7C%20PWA%20%7C%20Mobile-blue)](https://python-backend-academy.onrender.com)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)]()
[![CI Pipeline](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml/badge.svg)](https://github.com/kseniadmay/python-backend-academy/actions)
[![Python](https://img.shields.io/badge/python-3.13%20%7C%20FastAPI%20%7C%20Pydantic%20v2-yellow)]()
[![Stack](https://img.shields.io/badge/stack-Clean%20Architecture%20%7C%20PostgreSQL%20%7C%20WASM-informational)]()
[![Verification](https://img.shields.io/badge/verification-100%25%20PASS-success)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Автономная интерактивная образовательная платформа и практическая лабораторная среда для ускоренной подготовки инженеров **Junior+ Python Backend Developer**.

Проект объединяет доказательную педагогику **Khan Academy**, философию активного микрообучения (3D-тропа `Home = Journey`, единый фокус `Single Dominant CTA`, нулевой порог входа «Правило 2 минут»), hands-on кодинг прямо в браузере и разнесённое повторение **SRS** (SuperMemo-2). 

Архитектура системы полностью декомпозирована по стандартам **Clean Architecture** на современном промышленном стеке **Python 3.13 / FastAPI / Pydantic V2**:
- Изолированные архитектурные слои (`core`, `schemas`, `services`, `api`);
- Строгая валидация DTO схем на базе ядра Pydantic V2;
- Интерактивная документация Swagger UI и ReDoc;
- Двусторонняя дельта-синхронизация прогресса с защитой от потерянных обновлений (**Lost-Update Guard**, HTTP 409 Conflict, LWW-Merge);
- Нормализованный слой канонических данных контента (`data/content/`);
- Модульная архитектура клиентских стилей («Вечерний Обсидиан», Zen Glassmorphism) и реактивный стейт;
- Детерминированный 4-этапный мастер-пайплайн сборки (`scripts/build.py`);
- Двухконтурный движок браузерного Python (Brython WASM < 50 мс с полифиллами FastAPI/Pydantic/Pytest + Pyodide Fallback);
- 100% герметичный офлайн-контур (Service Worker Cache API).

---

## 🚀 Быстрый старт

### 1. Серверное ядро FastAPI (Рекомендуется)
Запустите командный файл:
```cmd
.\start_fastapi.cmd
```
Или напрямую через модуль Python:
```bash
python -m backend.run
```
Сервис поднимется на порту `8080` (или `8765`), предоставив доступ к:
* Веб-платформе: **http://127.0.0.1:8080**
* Документации Swagger UI: **http://127.0.0.1:8080/docs**
* Спецификации ReDoc: **http://127.0.0.1:8080/redoc**
* OpenAPI схеме: **http://127.0.0.1:8080/openapi.json**

### 2. Доступ со смартфона / планшета (Wi-Fi + Cloudflare)
Запустите командный файл:
```cmd
.\start_mobile.cmd
```
*(Либо через ярлык `Запустить_с_Телефона.bat`).*  
Скрипт автоматически определит локальный IP-адрес в домашней сети, поднимет защищённый туннель Cloudflare и выведет в консоль QR-код со ссылкой для мгновенного входа с мобильного устройства.

### 3. Автономный локальный запуск (SPA Monolith)
Платформа полностью автономна и герметична. Дважды кликните по файлу `academy.html` или запустите локальный статический сервер:
```bash
python -m http.server 8080
```
Затем перейдите по адресу: [http://localhost:8080/academy.html#/](http://localhost:8080/academy.html#/)

### 4. Автономный тренажёр с IDE
Для концентрированной практики написания кода без теории откройте:  
`Практика кода — тренажёр с IDE.html` (401 задача, сплит-терминал, автотесты в браузере).

---

## 🛠️ Стек технологий

| Направление | Стек и технологии | Назначение |
| :--- | :--- | :--- |
| **Backend & Core API** | **Python 3.13**, **FastAPI 0.115+**, **Pydantic V2**, `uvicorn[standard]`, `pydantic-settings` | Промышленный асинхронный бэкенд, валидация DTO схем на Rust, OpenAPI/Swagger UI |
| **Архитектура** | **Clean Architecture** (`core/`, `schemas/`, `services/`, `api/v1/`) | Полная изоляция бизнес-правил, DTO-валидации и транспортных интерфейсов |
| **Слой данных** | Нормализованный JSON-слой (`data/content/`), Local JSON (`data/progress_sync.json`), **PostgreSQL** (Neon Cloud) | Канонический реестр (401 задача, 238 конспектов, 287 колод) и персистентность прогресса |
| **Frontend Модульный** | CSS3 Custom Properties («Вечерний Обсидиан», Zen Glassmorphism), типографика Onest/Golos Text, ES6+ Vanilla JS | Модульный фронтенд (`frontend/`), реактивный менеджер стейта (`state.js`), API-клиент (`api.js`) |
| **Frontend Монолит** | `academy.html`, `Эталоны/Эталоны.html` | Автономный дистрибутив и канонический Single Source of Truth интерфейса |
| **Python в браузере** | **Brython 3.13.0** (Primary, < 50 мс) + **Pyodide 0.26.4** (Fallback WASM) | Двухконтурный браузерный раннер Python с эмуляцией FastAPI, Pydantic, Pytest, SQLite, HTTPX |
| **Офлайн & PWA** | Service Worker (`sw.js`), Cache API, Web App Manifest (`manifest.json`) | 100% работоспособность платформы в авиарежиме без доступа к интернету |
| **Синхронизация** | Дельта-синхронизация, **Lost-Update Guard** (HTTP 409 Conflict), LWW Merge | Бесшовная синхронизация решённых задач и прогресса между ПК и смартфоном |
| **Геймификация и звук** | **Web Audio API** (процедурный синтезатор), **Web Speech Synthesis API** | Процедурные звуковые эффекты без MP3-файлов, озвучка теории и формулировок |
| **Пайплайн и сборка** | `scripts/build.py`, `scripts/export_canonical_content.py` | 4-этапная детерминированная сборка ассетов, валидация схем и контроль инвариантов |
| **Контроль качества** | `verify_all.py` (Headless Chrome CDP, AST, pixel-diff), `backend/tests/` (15/15 PASS) | Сквозной автоматический контроль отсутствия логических и визуальных регрессий |

---

## ✨ Ключевые возможности

### 1. 3D-Тропа обучения (Home = Journey)
- Единый образовательный маршрут из **42 учебных дней** и **28 ключевых навыков** бэкенда.
- Плавная кривая Безье, автоматическое центрирование на текущем уроке и всплывающая popover-инспекция тем.
- Принцип **Single Dominant CTA**: строго одно очевидное целевое действие на первом экране без когнитивной перегрузки.

### 2. Студия кода и тренажёр с IDE
- **401 практическая задача** с автоматической проверкой тестами в реальном времени.
- Консольный терминал, подсветка синтаксиса, горячие клавиши (`Ctrl+Enter`), сброс черновиков.
- Встроенные шимы для запуска тестов FastAPI, схем Pydantic V2, фикстур Pytest и транзакций SQLite прямо в браузере.

### 3. Интерактивные квантованные микро-конспекты
- **238 структурированных конспектов**, разбитых на порции по 1.5–2.5 минуты («Правило 2 минут»).
- Наглядная визуализация потоков данных (I/O Flow), анатомия структур данных и карточки контраста («Наивный подход» vs «Идиоматичный подход»).
- **Mobile-First**: строгий лимит длины строк кода (35–42 символа), запрет хвостовых комментариев и нулевой горизонтальный скролл на смартфонах.

### 4. Флешкарты интервального повторения (SRS)
- **287 тематических колод** (свыше 6000 карточек) на базе доказательного алгоритма **SuperMemo-2**.
- 3D-переворот карточек, всплывающие шпаргалки кода, горячие клавиши (`Пробел`, цифры `1..4`) и начисление опыта (+2 / +5 / +10 XP).

### 5. Рубежные экзамены и аттестация модулей
- Итоговые тестирования по каждому из 7 направлений бэкенда с проходным порогом 75%.
- Двухфазный выбор ответов («подумай перед фиксацией») и детальный разбор решений.

### 6. Мок-интервью с Сократическим наставником
- Симуляция технического скрининга и архитектурной секции собеседования на позицию Junior+ Backend Developer.
- 4-уровневый динамический скаффолдинг подсказок (наводящий вопрос ➔ концептуальный намёк ➔ псевдокод ➔ тактическая опора) с автоматическим сбросом при верном решении.

---

## 🏛️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Клиентский слой платформы                           │
│  • Автономный SPA Monolith (academy.html) / Модульный SPA (frontend/)       │
│  • 3D Serpentine Path, Студия IDE (401 задача), Флешкарты SRS, Reader       │
│  • Реактивное состояние (state.js) + Асинхронный API-клиент (api.js)        │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
        ┌─────────────────────────────┐ ┌─────────────────────────────┐
        │     Офлайн-кэш (sw.js)      │ │   Движок кода в браузере    │
        │   Hermetic Service Worker   │ │     (Brython / Pyodide)     │
        └──────────────┬──────────────┘ └─────────────────────────────┘
                       │
                       │ REST API (JSON / Bearer Token)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                  Сервисный бэкенд FastAPI (backend/app/)                    │
│                                                                             │
│  ├── core/       # AppConfig, Security, Network (CORS, SPA Static, Env)     │
│  ├── schemas/    # Pydantic V2 DTO (ProgressPayload, ContentDTO, Feedback)  │
│  ├── services/   # SyncService (Lost-Update Guard, LWW), Content, Feedback  │
│  └── api/        # Роутеры v1 (/sync, /content, /feedback, /health)         │
│                  # и Legacy адаптеры (/healthz, /api/sync, /api/bug-report) │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
               ┌───────┴───────┐               ┌───────┴───────┐
               ▼               ▼               ▼               ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │  Локальный  │ │ Облачная БД │ │ Канонический│ │ Скомпилиро- │
        │  JSON (dev) │ │  (Neon PG)  │ │   контент   │ │ ванный CSS  │
        │progress_sync│ │ DATABASE_URL│ │data/content/│ │(dist/bundle)│
        └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 📡 Справочник API

Сервер FastAPI предоставляет полнофункциональный REST API с автоматической валидацией через Pydantic V2 и интерактивной документацией:
- **Swagger UI:** `http://127.0.0.1:8080/docs`
- **ReDoc:** `http://127.0.0.1:8080/redoc`

### Основные эндпоинты (`/api/v1`)

| Метод | Маршрут | Описание | Коды ответов |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Проверка жизнеспособности сервиса | `200 OK` |
| `GET` | `/api/v1/sync` | Получение синхронизированного прогресса пользователя | `200 OK`, `401 Unauthorized` |
| `POST` | `/api/v1/sync` | Сохранение прогресса с защитой от перезаписи версий | `200 OK`, `409 Conflict` |
| `GET` | `/api/v1/content/summary` | Сводная статистика (число модулей, задач, заметок, колод) | `200 OK` |
| `GET` | `/api/v1/content/modules` | Реестр 7 образовательных модулей и матрицы навыков | `200 OK` |
| `GET` | `/api/v1/content/notes/{note_id}` | Получение конкретного конспекта с квантованными микро-шагами | `200 OK`, `404 Not Found` |
| `GET` | `/api/v1/content/cards/{deck_id}` | Получение колоды флеш-карточек интервального повторения | `200 OK`, `404 Not Found` |
| `GET` | `/api/v1/content/tasks` | Список задач с фильтрацией по уровню (`level`) и теме (`topic`) | `200 OK` |
| `GET` | `/api/v1/content/tasks/{task_id}` | Данные практической задачи: формулировка, стартовый код, автотесты | `200 OK`, `404 Not Found` |
| `GET` | `/api/v1/content/search?q=...` | Полнотекстовый поиск по конспектам и практическим задачам | `200 OK` |
| `GET` | `/api/v1/feedback` | Просмотр очереди отзывов и отчётов об ошибках | `200 OK` |
| `POST` | `/api/v1/feedback` | Отправка репорта об ошибке или отзыва с мобильного/десктопа | `200 OK`, `422 Unprocessable` |

### Роуты обратной совместимости (Legacy Fallbacks)

Для поддержки существующих клиентов и монолита реализованы адаптеры:
- `GET /healthz` и `GET /api/ping` ➔ `GET /api/v1/health`
- `GET /api/sync` и `POST /api/sync` ➔ `GET /api/v1/sync` и `POST /api/v1/sync`
- `POST /api/bug-report` ➔ `POST /api/v1/feedback`

---

## 🗺️ Клиентские маршруты платформы (SPA)

| Маршрут | Название экрана | Назначение и функциональность |
| :--- | :--- | :--- |
| `#/` или `#/path` | **3D-Тропа обучения** | Главный экран: 42 учебных дня, 28 навыков, единая кнопка Single Dominant CTA |
| `#/python` | **Модуль 1 · Python Core** | Базовый и продвинутый Python 3.13: память CPython, типы данных, итераторы, ООП |
| `#/web` | **Модуль 2 · Web & Protocols** | Сетевые протоколы: HTTP/HTTPS, DNS, сокеты, REST API архитектура |
| `#/backend` | **Модуль 3 · Backend & API** | FastAPI, Django, Pydantic V2, асинхронный Python (`asyncio`), фоновые задачи |
| `#/algorithms` | **Модуль 4 · Алгоритмы** | Оценка сложности Big-O, структуры данных, бинарный поиск, графы, деревья |
| `#/databases` | **Модуль 5 · Базы данных** | PostgreSQL, ACID-транзакции, уровни изоляции, B-Tree индексы, SQLAlchemy ORM |
| `#/architecture` | **Модуль 6 · Архитектура** | Clean Architecture, SOLID, паттерны GoF, CQRS, DDD, 12-Factor App |
| `#/infra` | **Модуль 7 · Инфраструктура** | Docker, мультистейдж сборки, CI/CD, очереди задач Celery, Redis, мониторинг |
| `#/practice` | **Студия кода IDE** | 401 практическая задача с автотестами, запуском Brython и консолью |
| `#/cards` | **SRS Тренажёр карточек** | Интервальное повторение флешкарт по алгоритму SuperMemo-2 |
| `#/mock` | **Мок-интервью** | Сократический диалог, технический скрининг и решение кейсов собеседования |
| `#/map` | **Карта Мастерства** | Интерактивная матрица компетенций и граф зависимостей навыков |

---

## 📂 Структура проекта

```text
Python_Backend_Academy/                 # Корень репозитория
├── academy.html                        # Главный автономный SPA Monolith (~8 МБ)
├── index.html                          # PWA-контейнер и загрузчик с сервис-воркером
├── sw.js                               # Service Worker герметичного офлайн-кэша
├── manifest.json                       # Манифест Progressive Web App
├── icon.svg                            # Векторная иконка платформы
│
├── start_fastapi.cmd                   # Быстрый запуск FastAPI бэкенда (Windows)
├── start_mobile.cmd                    # Запуск сервера мобильного доступа с туннелем
├── Запустить_с_Телефона.bat            # Ярлык для смартфона на рабочем столе
├── verify_all.py                       # Мастер-конвейер сквозной верификации (100% PASS)
├── verify_all.cmd                      # Быстрый запуск верификации (Windows)
│
├── backend/                            # Промышленный бэкенд на FastAPI (Clean Architecture)
│   ├── run.py                          # Точка входа сервера Uvicorn
│   ├── academy_fastapi.service         # Systemd unit для Linux production
│   ├── requirements.txt                # Зависимости бэкенда (FastAPI, Uvicorn, Pydantic V2)
│   ├── app/
│   │   ├── main.py                     # Инициализация FastAPI, CORS, SPA fallback, роутеры
│   │   ├── core/                       # Настройки (pydantic-settings), безопасность, сеть
│   │   ├── schemas/                    # Pydantic V2 DTO (прогресс, контент, отзывы, ответы)
│   │   ├── services/                   # SyncService (LWW, 409 guard), ContentService, Feedback
│   │   └── api/                        # Роутеры v1 и адаптеры обратной совместимости
│   └── tests/                          # Сьют интеграционных тестов бэкенда (15/15 PASS)
│       └── test_api.py                 # Проверка всех API роутов и защитных механизмов
│
├── frontend/                           # Модульное клиентское ядро платформы
│   ├── index.html                      # Модульный каркас SPA
│   ├── css/                            # 8 слоёв стилей «Вечерний Обсидиан» и Zen Glassmorphism
│   │   ├── variables.css               # Дизайн-токены, палитра и типографика
│   │   ├── base.css                    # Сброс стилей, базовые элементы
│   │   ├── glassmorphism.css           # Эффекты стекла, глубина, подсветка
│   │   ├── main.css                    # Входная точка импорта CSS-слоёв
│   │   └── components/                 # Стили компонентов (trail, ide, reader, cards, sidebar)
│   ├── dist/
│   │   └── bundle.css                  # Оптимизированный скомпилированный бандл стилей
│   └── js/
│       ├── api.js                      # Асинхронный HTTP-клиент с повторными запросами
│       └── state.js                    # Реактивный стейт-менеджер клиентского состояния
│
├── data/                               # Слой хранения данных и синхронизации
│   ├── content/                        # Нормализованные канонические базы данных контента
│   │   ├── manifest.json               # Манифест 7 образовательных модулей курса
│   │   ├── tasks.json                  # База 401 практической задачи с тестами
│   │   ├── notes.json                  # База 238 квантованных конспектов теории
│   │   └── cards.json                  # База 287 колод карточек интервального повторения
│   ├── progress_sync.json              # Локальный снимок синхронизированного прогресса
│   └── user_feedback_queue.json        # Очередь обратной связи и отчётов об ошибках
│
├── scripts/                            # Инструменты сборки, автотесты и пайплайны
│   ├── build.py                        # Детерминированный 4-этапный мастер-сборщик проекта
│   ├── export_canonical_content.py     # Экстрактор канонического контента из RemNote
│   ├── test_bugs_regression.js         # Регрессионный сьют 80 багов интерфейса
│   ├── test_pwa_offline.js             # Верификация офлайн-кэша PWA и манифеста
│   ├── verify_academy.py               # Рендеринг маршрутов в Headless Chrome CDP
│   ├── visual_test.js                  # Pixel-diff тестирование экранов с эталонами
│   └── server.js                       # Вспомогательный Node.js сервер синхронизации
│
├── tests/                              # Спецификации и регрессионные проверки
│   ├── test_bugs_regression.js         # 80 проверок инвариантов качества и верстки
│   ├── test_cards_trainer_regression.js# Тесты тренажера карточек памяти
│   ├── test_dashboard_regression.js    # Тесты информационных панелей и прогресса
│   └── test_pravki_spec.js             # Спецификация соответствия эталонам дизайна
│
├── Эталоны/                            # Канонические эталоны дизайна (Single Source of Truth)
│   ├── Эталоны.html                    # Утверждённый эталонный билд интерфейса платформы
│   └── README.md                       # Регламент неизменяемости дизайн-системы
│
├── RemNote_Python_Mastery_FIXED/       # Платиновая база знаний (525 файлов Markdown)
│   ├── 01 · 🐍 Python                  # 28 навыков Python Core
│   ├── 02 · 🌐 Web                     # Протоколы Web, HTTP, REST, сокеты
│   ├── 03 · ⚙️ Backend                 # FastAPI, Django, асинхронность и архитектура API
│   ├── 04 · ⚡ Алгоритмы                # Алгоритмы, структуры данных, оценка сложности
│   ├── 05 · 🗄️ Базы данных             # SQL, PostgreSQL, транзакции, индексы, ORM
│   ├── 06 · 🏛️ Архитектура             # Clean Architecture, паттерны проектирования, SOLID
│   ├── 07 · 🚀 Инфраструктура          # Docker, CI/CD, очереди Celery/Redis, мониторинг
│   └── 00 · 🗺️ Карта Мастерства.md     # Единая матрица компетенций курса
│
├── docs/                               # Продуктовая и техническая документация
├── requirements.txt                    # Зависимости окружения (0 сторонних pip для ядра)
└── render.yaml                         # Конфигурация облачного деплоя на Render
```

---

## 🧪 Тестирование и верификация качества

Проект обеспечен многоуровневым контролем качества (**100% PASS**):

```bash
# 1. Запуск детерминированного конвейера сборки (схемы, CSS, эталоны, инварианты):
python scripts/build.py

# 2. Интеграционное тестирование REST API бэкенда (15/15 PASS):
python -m unittest discover backend/tests

# 3. Экспресс-верификация платформы (база RemNote, 80 багов, PWA, Headless Chrome):
python verify_all.py --quick

# 4. Полный сквозной прогон верификации (включая все 401 задачу IDE и pixel-diff):
python verify_all.py

# 5. Экстракция и валидация канонического контента из Markdown-базы знаний:
python scripts/export_canonical_content.py

# 6. Регрессионный сьют 80 исправлений интерфейса:
node tests/test_bugs_regression.js

# 7. Проверка оффлайн-контура Service Worker и PWA:
node scripts/test_pwa_offline.js
```

---

## 💡 Примеры работы с API через cURL

### 1. Проверка работоспособности сервиса
```bash
curl -s http://localhost:8080/api/v1/health
```
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": 1729813200000
}
```

### 2. Сводная статистика образовательного контента
```bash
curl -s http://localhost:8080/api/v1/content/summary
```
```json
{
  "modules_count": 7,
  "tasks_count": 401,
  "notes_count": 238,
  "cards_count": 287
}
```

### 3. Полнотекстовый поиск по конспектам и задачам
```bash
curl -s "http://localhost:8080/api/v1/content/search?q=fastapi"
```

### 4. Сохранение прогресса (дельта-синхронизация с защитой от коллизий)
```bash
curl -X POST http://localhost:8080/api/v1/sync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer my-secret-token" \
  -d '{
    "device": "desktop_macbook",
    "updatedAt": 1729813200000,
    "version": 42,
    "bundle": {
      "xp": 480,
      "streak": 7,
      "completedNodes": ["python_1_1_1", "python_1_1_2"],
      "solvedTasks": [1, 2, 3, 4, 5]
    }
  }'
```

### 5. Отправка отзыва или сообщения об ошибке
```bash
curl -X POST http://localhost:8080/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "context": "cards_mobile",
    "description": "Кнопка SRS реагирует мгновенно, верстка стабильна",
    "device": "iphone_safari"
  }'
```

---

## ⚖️ Лицензия и авторство

- **Автор платформы:** [@kseniadmay](https://github.com/kseniadmay)
- **Лицензия:** [MIT License](LICENSE)
