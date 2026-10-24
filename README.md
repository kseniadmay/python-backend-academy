# 🐍 Python Backend Academy

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live_Demo-onrender.com-4F46E5?style=for-the-badge&logo=render&logoColor=white)](https://python-backend-academy.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-100%25_PASS-10B981?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/kseniadmay/python-backend-academy/actions)

**Интерактивная среда подготовки инженеров Junior+ Python Backend Developer**  
*Доказательная педагогика Khan Academy · 3D-тропа microlearning · Hands-on кодинг в браузере*

[Быстрый старт](#-быстрый-старт) • [Архитектура](#-архитектура) • [Возможности](#-возможности) • [API & Swagger](#-api--документация) • [Тестирование](#-контроль-качества)

</div>

---

## ⚡ О проекте

**Python Backend Academy** — полнофункциональная лабораторная платформа для интенсивного погружения в бэкенд-разработку без долгой настройки локального окружения.

- 🎯 **Принцип Home = Journey**: 3D-тропа из 42 учебных дней и 28 компетенций с единым действием (*Single Dominant CTA*).
- 💻 **Hands-on IDE в браузере**: 401 практическая задача с мгновенной проверкой тестами на движке Brython 3.13 (WASM, запуск < 50 мс).
- 🧠 **Доказательное обучение**: квантованная теория (сессии по 2 мин), флешкарты с алгоритмом SuperMemo-2 (SRS) и сократические мок-интервью.
- ⚡ **Clean Architecture на FastAPI**: сервисный бэкенд на Python 3.13 с валидацией Pydantic V2, Swagger UI и двусторонней дельта-синхронизацией прогресса (Lost-Update Guard).

### 📊 Платформа в цифрах

| Модули | Дни программы | Практика (IDE) | Конспекты | SRS-колоды | Верификация |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **7 направлений** | **42 дня** | **401 задача** | **238 тем** | **287 колод** | **100% PASS** |

---

## 🚀 Быстрый старт

### 1. Серверный режим: FastAPI Core (Рекомендуется)
```cmd
.\start_fastapi.cmd
```
*или в консоли:* `python -m backend.run`  
- Платформа: [http://127.0.0.1:8080](http://127.0.0.1:8080)
- Swagger UI: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- ReDoc: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

### 2. Мобильный доступ (Wi-Fi + Cloudflare)
```cmd
.\start_mobile.cmd
```
Скрипт определяет локальный IP домашней сети, поднимает защищённый туннель Cloudflare и генерирует QR-код для смартфона/планшета.

### 3. Автономный офлайн-режим (PWA)
Дважды кликните по [`academy.html`](academy.html) или запустите локальный сервер:
```bash
python -m http.server 8080
```
Платформа на 100% герметична и работает без интернета через Service Worker Cache API.

---

## 🏛️ Архитектура

Проект спроектирован по принципам **Clean Architecture** с полным разделением ответственности:

```
┌─────────────────────────────────────────────────────────────┐
│                 Клиентский интерфейс (UI)                   │
│   Модульный SPA (frontend/)  •  Офлайн-монолит (academy.html)│
│   3D-Тропа Безье  •  Студия IDE  •  SuperMemo-2 SRS  •  PWA │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│      Офлайн-кэш (sw.js)     │ │   Движок Python в браузере  │
│    Service Worker Cache     │ │   Brython 3.13 / Pyodide    │
└──────────────┬──────────────┘ └─────────────────────────────┘
               │
               │ REST API / Bearer Token
               ▼
┌─────────────────────────────────────────────────────────────┐
│             FastAPI Backend Core (backend/app/)             │
│                                                             │
│   ├── core/      Конфигурация, безопасность, CORS           │
│   ├── schemas/   Pydantic V2 DTO со строгой валидацией      │
│   ├── services/  SyncService (Lost-Update Guard, LWW-Merge) │
│   │              ContentService (in-memory кэш 401 задачи)  │
│   └── api/       Маршрутизация v1 и адаптеры обратной сог.  │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
       ┌───────┴───────┐               ┌───────┴───────┐
       ▼               ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Локальный  │ │ Облачная БД │ │ Канонический│ │ Скомпилиро- │
│  JSON-снимок│ │  (Neon PG)  │ │   контент   │ │ ванный CSS  │
│progress_sync│ │ DATABASE_URL│ │data/content/│ │(dist/bundle)│
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 🗺️ Программа обучения

1. 🐍 **Python Core**: модель памяти CPython, изменяемость, итераторы, генераторы, ООП, тайпинг.
2. 🌐 **Web & Protocols**: HTTP/HTTPS, сокеты, заголовки, TCP/UDP, RESTful архитектура.
3. ⚙️ **Backend & API**: FastAPI, Django, асинхронный Python (`asyncio`), Pydantic V2.
4. ⚡ **Алгоритмы и структуры данных**: Big-O, бинарный поиск, связные списки, деревья, графы.
5. 🗄️ **Базы данных**: PostgreSQL, транзакции, ACID, уровни изоляции, B-Tree индексы, ORM.
6. 🏛️ **Архитектура ПО**: Clean Architecture, SOLID, шаблоны GoF, CQRS, 12-Factor App.
7. 🚀 **Инфраструктура**: Docker, multi-stage билды, CI/CD, очереди задач Celery, Redis.

---

## 📡 API & Документация

Сервер FastAPI автоматически генерирует спецификацию OpenAPI 3.1:

| Метод | Эндпоинт | Назначение |
| :--- | :--- | :--- |
| `GET` | `/docs` | Интерактивный Swagger UI |
| `GET` | `/api/v1/health` | Проверка жизнеспособности сервиса |
| `GET`/`POST` | `/api/v1/sync` | Дельта-синхронизация с защитой от коллизий (`409 Conflict`) |
| `GET` | `/api/v1/content/summary` | Сводная статистика по модулям, конспектам и задачам |
| `GET` | `/api/v1/content/modules` | Каталог 7 модулей и карты компетенций |
| `GET` | `/api/v1/content/tasks` | Список задач с фильтрацией (`?level=1..7&topic=...`) |
| `GET` | `/api/v1/content/search` | Полнотекстовый поиск по конспектам и практике (`?q=...`) |
| `POST` | `/api/v1/feedback` | Отправка отзывов и отчётов об ошибках |

*Для обратной совместимости также поддерживаются маршруты `/healthz`, `/api/sync` и `/api/bug-report`.*

---

## 📂 Структура репозитория

```text
Python_Backend_Academy/
├── academy.html                 # Главный автономный SPA Monolith (~8 МБ)
├── start_fastapi.cmd            # Запуск FastAPI бэкенда для Windows
├── start_mobile.cmd             # Запуск мобильного сервера с туннелем
├── verify_all.py                # Мастер-конвейер полной верификации (100% PASS)
│
├── backend/                     # Сервисный бэкенд на FastAPI (Clean Architecture)
│   ├── run.py                   # Точка входа сервера Uvicorn
│   ├── app/                     # Ядро: core, schemas (DTO), services, api/v1
│   └── tests/                   # Интеграционные тесты API (15/15 PASS)
│
├── frontend/                    # Модульное клиентское ядро платформы
│   ├── css/                     # 8 слоёв стилей «Вечерний Обсидиан» и Glassmorphism
│   ├── dist/bundle.css          # Оптимизированный скомпилированный бандл
│   └── js/                      # Модульная логика: api.js, state.js
│
├── data/content/                # Канонические данные: manifest, tasks, notes, cards
├── scripts/build.py             # Детерминированный сборщик и валидатор контента
├── tests/                       # Регрессионный сьют 80 багов и проверка эталонов
└── Эталоны/                     # Утверждённые канонические эталоны дизайна
```

---

## 🧪 Контроль качества

Проект покрыт многоуровневым конвейером автоматических проверок:

```bash
# 1. Детерминированная сборка и валидация данных Pydantic:
python scripts/build.py

# 2. Интеграционные тесты FastAPI бэкенда (15/15 PASS):
python -m unittest discover backend/tests

# 3. Экспресс-верификация (RemNote, 80 тестов DOM, PWA, Headless Chrome):
python verify_all.py --quick

# 4. Полный сквозной прогон всех 401 задач IDE и visual pixel-diff:
python verify_all.py
```

---

## ⚖️ Лицензия

Распространяется под лицензией [MIT](LICENSE).  
Автор: [@kseniadmay](https://github.com/kseniadmay)
