# Серверное ядро FastAPI (`backend/`)

Локальный бэкенд платформы **Python Backend Academy** на базе **FastAPI**, **Pydantic v2** и **Python 3.13** со слоистой структурой (`api` → `schemas` → `services` → `core`) и файловым JSON-хранилищем.

---

## Структура

```text
backend/
├── app/
│   ├── api/                # HTTP-роутеры
│   │   ├── v1/             # Content, SRS, Notes, Practice, Mock и Sync API v1
│   │   └── legacy_compat.py  # Эндпоинты обратной совместимости (/api/sync, /healthz)
│   ├── core/               # Конфигурация (Pydantic Settings), авторизация по токену, сетевые утилиты
│   ├── schemas/            # Pydantic v2 схемы валидации и DTO
│   ├── services/           # Бизнес-логика (ContentService, SyncService, SrsService, CodeRunnerService)
│   └── main.py             # FastAPI-приложение, Lifespan, CORS и раздача статики по allowlist
├── tests/                  # Модульные тесты REST API и проверок безопасности
├── requirements.txt        # Зависимости для запуска сервера
├── requirements-dev.txt    # Зависимости для запуска с нуля и тестирования (httpx, pytest)
└── run.py                  # Точка входа для локального запуска
```

---

## Быстрый запуск и тесты

```bash
# Установка зависимостей (включая тестовые):
pip install -r backend/requirements-dev.txt

# Запуск локального сервера (по умолчанию 127.0.0.1:8080):
python -m backend.run

# Запуск тестов бэкенда:
python -m unittest discover -s backend/tests -v
```

- **Swagger UI**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- **ReDoc**: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)
- **Health Check**: [http://127.0.0.1:8080/api/v1/health](http://127.0.0.1:8080/api/v1/health)

> **Предупреждение о безопасности:** `CodeRunnerService` (`/api/v1/practice/run` и `/api/v1/mock/evaluate`) исполняет код через встроенный `exec()` без песочницы (sandbox) и таймаутов. Используйте его только локально; в публичном окружении отключайте через `ALLOW_CODE_RUNNER=false`.
