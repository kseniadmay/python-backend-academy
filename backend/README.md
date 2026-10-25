# ⚡ Сервисное ядро FastAPI (`backend/`)

Модульный бэкенд платформы **Python Backend Academy**, построенный по принципам Clean Architecture на базе **FastAPI**, **Pydantic V2** и **Python 3.13**.

---

## 🏗️ Архитектура слоёв

```text
backend/
├── app/
│   ├── api/          # HTTP контроллеры и роутеры
│   │   ├── v1/       # Современный Content & Sync API v1
│   │   └── legacy_compat.py  # Эндпоинты обратной совместимости (/api/sync, /healthz)
│   ├── core/         # Конфигурация (Pydantic Settings), безопасность и сетевые утилиты
│   ├── schemas/      # Pydantic v2 схемы валидации данных и DTO
│   ├── services/     # Бизнес-логика (ContentService, SyncService, FeedbackService)
│   └── main.py       # Точка инициализации FastAPI приложения, Lifespan и CORS
├── tests/            # Модульные тесты API (100% PASS)
├── requirements.txt  # Зависимости бэкенда (fastapi, uvicorn, pydantic-settings)
└── run.py            # Точка входа для запуска локального сервера разработки
```

---

## 🚀 Быстрый запуск

```bash
# Через скрипт в корне:
start_fastapi.cmd

# Либо через Python:
python -m backend.run
```

- **Swagger UI**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- **ReDoc**: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)
- **Health Check**: [http://127.0.0.1:8080/api/v1/health](http://127.0.0.1:8080/api/v1/health)
