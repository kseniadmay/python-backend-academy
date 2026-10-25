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
python -m unittest discover backend/tests

# Сборка ассетов и валидация данных:
python scripts/build.py

# Сквозная проверка платформы:
python verify_all.py --quick
```

## Структура проекта

- `academy.html` — автономное одностраничное приложение.
- `backend/` — сервер на FastAPI (`core`, `schemas`, `services`, `api`).
- `data/content/` — база данных курса (задачи, конспекты, колоды).
- `frontend/` — модульные стили и скрипты интерфейса.
- `scripts/` — сборщик (`build.py`) и утилиты.
- `tests/` — регрессионные тесты.

## Лицензия

[MIT](LICENSE)
