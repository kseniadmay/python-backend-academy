# Python Backend Academy

[![CI](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml/badge.svg)](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PWA: Offline Ready](https://img.shields.io/badge/PWA-offline--ready-blue.svg?style=flat-square)](#возможности)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

Личный интерактивный тренажёр для системной подготовки к собеседованиям на позицию Python Backend-разработчика. Проект собран с помощью AI-инструментов и объединяет клиентское JS/HTML SPA, базу знаний в Markdown и локальный бэкенд на FastAPI.

## Возможности

- **404 задачи с автотестами**: проверка кода прямо в браузере (Brython / WebAssembly) или через локальный FastAPI-раннер.
- **238 конспектов**: теория по ключевым темам бэкенда и вопросам собеседований.
- **287 колод карточек**: интервальное повторение по алгоритму SuperMemo-2 / FSRS.
- **Бэкенд на FastAPI**: REST API, синхронизация прогресса между устройствами и автодокументация Swagger.
- **Офлайн-режим (PWA)**: автономная работа без подключения к сети.

## Модули курса

1. **Python Core** — модель памяти, структуры данных, итераторы, ООП, типизация.
2. **Web и протоколы** — HTTP/HTTPS, WebSockets, сокеты, REST API.
3. **Бэкенд и API** — FastAPI, Django, асинхронный Python (`asyncio`), Pydantic.
4. **Алгоритмы** — оценка сложности Big-O, поиск, структуры данных, графы.
5. **Базы данных** — PostgreSQL, транзакции, индексы, SQLAlchemy ORM.
6. **Архитектура** — принципы SOLID, слоистое разделение ответственности, паттерны проектирования.
7. **Инфраструктура** — Docker, CI/CD, Celery, Redis.

## Быстрый запуск

### 1. Установка зависимостей и настройка

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r backend/requirements-dev.txt
```

При необходимости скопируйте `.env.example` в `.env` (для локального запуска достаточно настроек по умолчанию — сервер слушает `127.0.0.1:8080`).

### 2. Запуск с сервером (FastAPI)

```bash
python -m backend.run
```

На Windows также можно использовать `.\start_fastapi.cmd`. После запуска доступны:
- Интерфейс: [http://127.0.0.1:8080](http://127.0.0.1:8080)
- Документация Swagger: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

> **Важно про безопасность:** встроенный `CodeRunnerService` (`/api/v1/practice/run`, `/api/v1/mock/evaluate`) выполняет код через `exec()` без изолированной песочницы (sandbox) и таймаутов. Он рассчитан **только на локальный запуск** на собственной машине; при любом публичном размещении его нужно отключать через `ALLOW_CODE_RUNNER=false`.

### 3. Автономно (без сервера)

Откройте файл `academy.html` в любом браузере.

### 4. Со смартфона в локальной сети

Установите Node-зависимости (`npm install`) и запустите `node scripts/server.js` (на Windows — `.\start_mobile.cmd`). При наличии локального `scripts/cloudflared.exe` поддерживается проброс туннеля.

## Тестирование

```bash
# Модульные тесты FastAPI-бэкенда:
python -m unittest discover -s backend/tests -v

# Все Python-тесты (бэкенд + БД + конкурентность):
python -m unittest discover -s . -v

# Сборка и синхронизация ассетов:
python scripts/build.py

# Проверка базы знаний, синтаксиса JS и эталона:
python verify_all.py --quick
```

## Структура проекта

Веб-ядро находится в корне для работы Service Worker (Scope `/`), прямого открытия без сервера и раздачи через FastAPI.

```text
┌──────────────────────────────────────────────────────────────────┐
│                   КАНОНИЧЕСКИЙ ИСТОЧНИК ЗНАНИЙ                   │
│  📂 knowledge_base/  (526 .md файлов: конспекты, карты, колоды)  │
│  📂 data/content/    (задачи, тесты, JSON-эшелоны)               │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ scripts/assemble_academy.py
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                      ВЕБ-ЯДРО ПЛАТФОРМЫ (PWA)                    │
│  📄 academy.html          — Главное SPA (теория, карточки, IDE)  │
│  📄 index.html            — Быстрый PWA-шлюз                     │
│  ⚡ sw.js + manifest.json — Офлайн-кэш и установка как PWA       │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                         БЭКЕНД И СЕРВИСЫ                         │
│  📂 backend/              — FastAPI сервер (API, синхронизация)  │
└──────────────────────────────────────────────────────────────────┘
```

### Основные файлы и каталоги

| Файл / Папка | Назначение |
| :--- | :--- |
| **`academy.html`** | Главное клиентское SPA: все 7 модулей, конспекты, карточки, тесты и встроенная практика на 404 задачи. |
| **`index.html`** | Стартовая страница входа: регистрирует Service Worker и открывает `academy.html`. |
| **`sw.js` / `manifest.json` / `icon.svg`** | Офлайн-кэширование и метаданные PWA. |
| **`knowledge_base/`** | Исходные Markdown-файлы конспектов и колод, из которых собирается контент платформы. |
| **`backend/`** | Бэкенд на FastAPI (`core`, `schemas`, `services`, `api`). |
| **`data/`** | Данные курса (`content/`: задачи, конспекты, колоды; локальное хранилище синхронизации). |
| **`deploy/`** | Конфигурации systemd-сервисов и инструкции по развёртыванию. |
| **`docs/`** | Архитектурные спецификации и журнал решений. |
| **`frontend/`** | Модульные стили (`css/`), клиентские скрипты (`js/`) и бандл (`dist/`). |
| **`scripts/`** | Скрипты сборки (`build.py`, `assemble_academy.py`), валидаторы и вспомогательные утилиты. |
| **`tests/`** | Тесты БД, конкурентности и JS-регрессии. |
| **`verify_all.py`** | Сквозной скрипт проверки базы знаний, эталона, синтаксиса JS и задач. |
| **`PROJECT_CONTEXT.md` / `AGENTS.md`** | Правила и контекст проекта для разработки с AI-агентами. |

## Лицензия

[MIT](LICENSE)
