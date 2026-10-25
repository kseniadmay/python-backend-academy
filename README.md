# Python Backend Academy

[![CI](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml/badge.svg)](https://github.com/kseniadmay/python-backend-academy/actions/workflows/ci.yml)
[![Tests: 100% Pass](https://img.shields.io/badge/tests-100%25%20passed-brightgreen.svg?style=flat-square)](#тестирование)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PWA: Offline Ready](https://img.shields.io/badge/PWA-offline--ready-blue.svg?style=flat-square)](#возможности)
[![Demo](https://img.shields.io/badge/Demo-Online-4F46E5.svg?style=flat-square&logo=render&logoColor=white)](https://python-backend-academy.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

Интерактивная платформа для изучения Python-бэкенда: практика в браузере, конспекты и интервальное повторение.

## Возможности

- **401 задача с автотестами**: проверка кода прямо в браузере (Brython / WebAssembly).
- **238 конспектов**: теория по ключевым темам бэкенда и вопросам собеседований.
- **287 колод карточек**: интервальное повторение по алгоритму SuperMemo-2.
- **Бэкенд на FastAPI**: REST API, синхронизация прогресса и автодокументация Swagger.
- **Офлайн-режим (PWA)**: автономная работа без подключения к сети.

## Модули курса

1. **Python Core** — модель памяти, структуры данных, итераторы, ООП, типизация.
2. **Web и протоколы** — HTTP/HTTPS, WebSockets, сокеты, REST API.
3. **Бэкенд и API** — FastAPI, Django, асинхронный Python (`asyncio`), Pydantic.
4. **Алгоритмы** — оценка сложности Big-O, поиск, структуры данных, графы.
5. **Базы данных** — PostgreSQL, транзакции, индексы, SQLAlchemy ORM.
6. **Архитектура** — Clean Architecture, SOLID, паттерны проектирования.
7. **Инфраструктура** — Docker, CI/CD, Celery, Redis.

## Быстрый запуск

### С сервером (FastAPI)
```cmd
.\start_fastapi.cmd
```
*Или:* `python -m backend.run`  
- Интерфейс: [http://127.0.0.1:8080](http://127.0.0.1:8080)
- Документация Swagger: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

### Автономно (без сервера)
Откройте файл `academy.html` в любом браузере.

### Со смартфона
Запустите `.\start_mobile.cmd` для доступа по локальной сети через Cloudflare.

## Тестирование

```bash
# Тесты REST API:
python -m unittest

# Сборка ассетов и валидация данных:
python scripts/build.py

# Сквозная проверка платформы:
python verify_all.py --quick
```

## Структура проекта и архитектурная связь файлов

Архитектура репозитория спроектирована по модели **Self-Contained Fullstack PWA**: веб-ядро находится в корне для бесшовной работы Service Worker (Scope `/`), прямого открытия без сервера и мгновенной раздачи через FastAPI.

```text
┌──────────────────────────────────────────────────────────────────┐
│                   КАНОНИЧЕСКИЙ ИСТОЧНИК ЗНАНИЙ                   │
│  📂 RemNote_Python_Mastery_FIXED/  (525 .md конспектов и карточек)│
│  📂 data/content/                  (задачи, тесты, JSON-эшелоны) │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ scripts/assemble_academy.py
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                      ВЕБ-ЯДРО ПЛАТФОРМЫ (PWA)                    │
│  📄 academy.html        — Главное SPA (теория, квизы, боссы)     │
│  📄 practice_ide.html   — Автономный тренажёр IDE (401 задача)   │
│  📄 index.html          — Быстрый PWA-шлюз                       │
│  ⚡ sw.js + manifest.json — Офлайн-кэш и установка как приложение │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                    СЕРВИСНЫЙ СЛОЙ И ДИСТРИБУЦИЯ                  │
│  📂 backend/            — FastAPI сервер (синхронизация, API)    │
│  📦 Project.zip         — Эталонный дистрибутивный слепок        │
└──────────────────────────────────────────────────────────────────┘
```

### Назначение файлов в корне

| Файл / Папка | Роль в проекте | Описание |
| :--- | :--- | :--- |
| **`academy.html`** | 🎓 **Ядро платформы** | Монолитное клиентское SPA: все 7 треков обучения, интерактивные конспекты, карточки и тесты. Не удалять. |
| **`practice_ide.html`** | 💻 **Песочница IDE** | Автономный тренажёр на 401 задачу с выполнением Python прямо в браузере (Brython 3.13) и редактором CodeMirror. |
| **`index.html`** | 🌐 **PWA Шлюз** | Стартовая точка входа: регистрирует Service Worker и открывает Академию. |
| **`sw.js`** | ⚡ **Service Worker** | Движок кеширования: гарантирует 100% работу платформы и тренажёра в режиме самолёта (без интернета). |
| **`manifest.json`** | 📱 **PWA Manifest** | Метаданные для установки Академии как нативного приложения на Android, iOS, Windows и macOS. |
| **`icon.svg`** | 🎨 **Ассет** | Векторная иконка платформы для PWA и браузерной вкладки. |
| **`RemNote_Python_Mastery_FIXED/`** | 📚 **База знаний** | 525 канонических Markdown-файлов конспектов и карточек, из которых собираются данные платформы. |
| **`Python_Backend_Academy_Project.zip`** | 📦 **Эталонный архив** | Автономный архив-слепок проекта для резервного копирования и дистрибуции. |
| **`start_fastapi.cmd`** | 🚀 **Запуск** | Скрипт старта FastAPI-бэкенда в один клик. |
| **`start_mobile.cmd`** | 📱 **Мобильный запуск** | Скрипт раздачи сервера в локальную сеть Wi-Fi для тестирования со смартфона. |
| **`verify_all.py` / `.cmd`** | ✅ **Верификация** | Сквозной пайплайн валидации: синтаксис, тесты API, 401 задача IDE и PWA-офлайн. |
| **`PROJECT_CONTEXT.md` / `AGENTS.md`** | 🤖 **AI-контекст** | Архитектурные правила, инварианты и регламенты для разработчиков и ИИ-агентов. |

### Подсистемы и каталоги

- `backend/` — сервисный бэкенд на FastAPI (`core`, `schemas`, `services`, `api`).
- `data/` — база данных курса (`content/`: задачи, конспекты, колоды; эшелоны).
- `deploy/` — конфигурации systemd сервисов и инструкции по развёртыванию.
- `docs/` — архитектурные спецификации, журнал решений дескриптора и бэклог.
- `frontend/` — модульные стили (`css/`), клиентские скрипты (`js/`) и сборка бандлов (`dist/`).
- `scripts/` — пайплайн сборки (`build.py`, `assemble_academy.py`), валидаторы и утилиты.
- `tests/` — модульные тесты бэкенда и регрессионный сьют.

## Лицензия

[MIT](LICENSE)
