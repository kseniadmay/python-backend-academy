# PYTHON BACKEND ACADEMY

[![CI](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml/badge.svg)](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688)](https://fastapi.tiangolo.com/)
[![PWA: offline-ready](https://img.shields.io/badge/PWA-offline--ready-brightgreen)](#возможности)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Личный интерактивный тренажёр для системной подготовки к собеседованиям на позицию Python Backend-разработчика, собранный с помощью AI-инструментов.  
Проект объединяет клиентское SPA (HTML/JS/PWA), базу знаний в Markdown и локальный сервер на FastAPI.  
Поддерживает автономную работу в браузере, интервальное повторение карточек и проверку Python-задач в реальном времени.

## Стек технологий

- Python 3.13
- FastAPI 0.115+ / Uvicorn
- Pydantic v2 / pydantic-settings
- Vanilla JavaScript / HTML5 / CSS3 (PWA, Service Worker)
- Brython (исполнение Python-кода в браузере)
- Markdown / JSON (база знаний и файловое хранилище прогресса)
- `unittest` / Node.js (автотесты бэкенда, БД и JS-инвариантов)

## Возможности

### Основные функции

- **Практика в Zen IDE**: 404 задачи с автотестами и наводящими подсказками  
_Реализация:_ Brython в браузере или локальный FastAPI-раннер (`CodeRunnerService`)

- **Конспекты и теория**: 246 структурированных конспектов по 8 модулям курса (49 юнитов, 6 эшелонов)  
_Реализация:_ исходники в Markdown (`knowledge_base/`), сборка в SPA через `scripts/assemble_academy.py`

- **Интервальное повторение**: 295 колод карточек и график повторения прочитанных конспектов  
_Реализация:_ алгоритмы SuperMemo-2 / FSRS и сохранение прогресса на клиенте и сервере

- **Тренажёр собеседований**: пошаговый разбор задач с подсказками и проверкой решений  
_Реализация:_ эндпоинты `/api/v1/mock/*` и клиентские сценарии SPA

### Системные возможности

- **REST API и синхронизация**: выдача контента, прогресса, черновиков и перенос состояния между устройствами  
_Реализация:_ FastAPI + Pydantic v2 + Swagger/ReDoc

- **Автономная работа (PWA)**: запуск прямо из файла `academy.html` и работа без сети  
_Реализация:_ Service Worker (`sw.js`) и `manifest.json`

## Модули курса

0. **Карьера и HR** — ATS-резюме, витрина GitHub, самопрезентация, метод STAR, HR-скрининг и торг по офферу.
1. **Python Core** — модель памяти, структуры данных, итераторы, ООП, типизация.
2. **Web и протоколы** — HTTP/HTTPS, WebSockets, сокеты, REST API.
3. **Бэкенд и API** — FastAPI, Django, `asyncio`, Pydantic.
4. **Алгоритмы** — оценка сложности Big-O, поиск, структуры данных, графы.
5. **Базы данных** — PostgreSQL, транзакции, индексы, SQLAlchemy ORM.
6. **Архитектура** — принципы SOLID, слоистое разделение ответственности, паттерны проектирования.
7. **Инфраструктура** — Docker, CI/CD, Celery, Redis.

## Endpoints

### Контент и навигация

`GET /api/v1/content/summary` – сводка по материалам курса  
`GET /api/v1/content/modules` – список модулей и тем  
`GET /api/v1/content/tasks` – список практических задач  
`GET /api/v1/content/search` – поиск по базе знаний  
`GET /api/v1/path/overview` – обзор пути обучения по эшелонам  

### Интервальное повторение и конспекты

`GET /api/v1/srs/due` – карточки к повторению на сегодня  
`POST /api/v1/srs/rate` – оценка карточки и пересчёт интервала  
`GET /api/v1/notes/due` – конспекты к повторению  
`POST /api/v1/notes/progress` – сохранение прогресса чтения конспекта  

### Практика, синхронизация и состояние

`POST /api/v1/practice/run` – локальный запуск решения задачи  
`POST /api/v1/mock/evaluate` – проверка решения в режиме собеседования  
`GET /api/v1/sync` – получение сохранённого прогресса  
`POST /api/v1/sync` – отправка локального прогресса на сервер  
`GET /api/v1/health` – проверка доступности сервиса  

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/kseniadmay/python-backend-academy.git
cd python-backend-academy
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS
```

### 3. Установка зависимостей

```bash
# Зависимости для запуска сервера
pip install -r backend/requirements.txt

# Зависимости для разработки и запуска тестов (включая httpx и pytest)
pip install -r backend/requirements-dev.txt
```

### 4. Настройка переменных окружения (опционально)

```bash
cp .env.example .env
```

Для локального запуска настройки по умолчанию уже готовы: сервер слушает `127.0.0.1:8080`.

### 5. Запуск сервера (FastAPI)

```bash
python -m backend.run
```

На Windows также доступен скрипт `.\start_fastapi.cmd`.

> **Важно про безопасность:** встроенный `CodeRunnerService` (`/api/v1/practice/run` и `/api/v1/mock/evaluate`) — это строго локальный dev-инструмент, который выполняет Python-код через `exec()` без изолированной песочницы (sandbox) и жёстких ограничений окружения. Не используйте его в публичном доступе без отключения через `ALLOW_CODE_RUNNER=false`.

### Альтернативные режимы запуска

- **Без сервера (офлайн)**: откройте файл `academy.html` в любом современном браузере.
- **Со смартфона в локальной сети**: установите Node-зависимости (`npm install`) и запустите `node scripts/server.js` (на Windows — `.\start_mobile.cmd`).

## Документация API

После запуска сервера доступны:

- **Интерфейс тренажёра**: http://127.0.0.1:8080/
- **Swagger UI**: http://127.0.0.1:8080/docs
- **ReDoc**: http://127.0.0.1:8080/redoc
- **Health Check**: http://127.0.0.1:8080/api/v1/health

## Тестирование

```bash
# 40 модульных тестов FastAPI-бэкенда
python -m unittest discover -s backend/tests -v

# Все 48 Python-тестов (бэкенд + SQLite + конкурентность)
python -m unittest discover -s . -v

# Быстрая проверка базы знаний (542 файла), синтаксиса JS и эталона
python verify_all.py --quick

# Архитектурный тест соответствия принципу DRY
node tests/test_dry_architecture.js
```

## Архитектура

```text
┌───────────────────┐      ┌──────────────────────┐
│  knowledge_base/  │      │     data/content/    │
│ (542 .md файла)   │      │   (задачи, тесты)    │
└─────────┬─────────┘      └──────────┬───────────┘
          │                           │
          └─────────────┬─────────────┘
                        ▼ scripts/assemble_academy.py
┌─────────────────────────────────────────────────┐
│              ВЕБ-ЯДРО ПЛАТФОРМЫ (PWA)           │
│  academy.html + index.html + sw.js + Brython    │
└───────────────────────┬─────────────────────────┘
                        │ HTTP / JSON (/api/v1/*)
                        ▼
┌─────────────────────────────────────────────────┐
│                 FastAPI BACKEND                 │
│   api/v1 ─► schemas ─► services ─► JSON / data  │
└─────────────────────────────────────────────────┘
```

Компоненты:

- `academy.html` / `frontend/` – клиентское SPA, стили, логика обучения и локальное исполнение кода в Brython
- `knowledge_base/` и `data/content/` – исходные Markdown-конспекты, колоды карточек и 404 задачи
- `scripts/assemble_academy.py` – сборщик контента в единый автономный бандл и эталон
- `backend/` – сервер на FastAPI для выдачи контента, синхронизации прогресса и локального запуска кода

## Структура проекта

```text
python-backend-academy/
├── backend/                # Серверное ядро FastAPI
│   ├── app/
│   │   ├── api/            # Роутеры v1 и маршруты совместимости
│   │   ├── core/           # Настройки (Pydantic Settings), авторизация, утилиты
│   │   ├── schemas/        # Pydantic v2 схемы и DTO
│   │   ├── services/       # Бизнес-логика (Content, Sync, SRS, CodeRunner)
│   │   └── main.py         # Инициализация FastAPI и раздача статики
│   ├── tests/              # 40 модульных тестов бэкенда
│   ├── requirements.txt    # Runtime-зависимости сервера
│   ├── requirements-dev.txt# Зависимости для разработки и тестов
│   └── run.py              # Точка входа для локального запуска
├── knowledge_base/         # 542 Markdown-файла (246 конспектов, 295 колод, карта)
├── data/                   # Контент курса (content/) и файлы синхронизации
├── frontend/               # Модульный JS/CSS и собранные ассеты (dist/)
├── scripts/                # Скрипты сборки (build.py, assemble_academy.py) и проверки
├── standards/              # Канонический эталон вёрстки (standards.html)
├── tests/                  # Тесты БД, конкурентности и JS-регрессии
├── deploy/                 # Конфигурации systemd для развёртывания
├── docs/                   # Архитектурные спецификации
├── academy.html            # Главное клиентское SPA (100% синхронно с эталоном)
├── index.html              # Стартовый шлюз PWA
├── sw.js                   # Service Worker для офлайн-режима
├── manifest.json           # Метаданные PWA
├── verify_all.py           # Сквозная проверка базы знаний, JS и эталона
├── .env.example            # Шаблон переменных окружения
└── README.md               # Документация проекта
```

## Автор

GitHub: [@kseniadmay](https://github.com/kseniadmay)

## Лицензия

MIT License
