# -*- coding: utf-8 -*-
import os, re, shutil
from enrich_backend_mod3 import ENRICHED_BACKEND_NOTES, NEW_MOD3_F_DECKS

BASE = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED'
OLD_MOD2 = os.path.join(BASE, '02 · 🌐 Web & Backend')
OLD_BACKEND_DIR = os.path.join(BASE, '02 · ⚙️ Backend')
WEB_DIR = os.path.join(BASE, '02 · 🌐 Web')
BACKEND_DIR = os.path.join(BASE, '03 · ⚙️ Backend')

def _force_remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, 0o777)
        func(path)
    except Exception:
        pass

# 0. Shift Modules 06->07, 05->06, 04->05, 03->04 on disk in reverse order (idempotent)
SHIFT_MODS = [
    ('06 · 🚀 Инфраструктура', '07 · 🚀 Инфраструктура', '6', '7'),
    ('05 · 🏛️ Архитектура',    '06 · 🏛️ Архитектура',    '5', '6'),
    ('04 · 🗄️ Базы данных',    '05 · 🗄️ Базы данных',    '4', '5'),
    ('03 · ⚡ Алгоритмы',      '04 · ⚡ Алгоритмы',      '3', '4'),
]
if os.path.isdir(os.path.join(BASE, '03 · ⚡ Алгоритмы')):
    for old_m, new_m, old_u, new_u in SHIFT_MODS:
        src_m = os.path.join(BASE, old_m)
        dst_m = os.path.join(BASE, new_m)
        if os.path.isdir(src_m):
            for entry in list(os.listdir(src_m)):
                full_e = os.path.join(src_m, entry)
                if os.path.isdir(full_e) and entry.startswith(f'Юнит {old_u}.'):
                    new_entry = entry.replace(f'Юнит {old_u}.', f'Юнит {new_u}.', 1)
                    os.rename(full_e, os.path.join(src_m, new_entry))
            if os.path.isdir(dst_m):
                shutil.rmtree(dst_m, onexc=_force_remove_readonly)
            os.rename(src_m, dst_m)
            print(f"Shifted module directory: {old_m} -> {new_m}")

WEB_UNITS = {
    '2.1': 'Юнит 2.1 · Сетевой фундамент',
    '2.2': 'Юнит 2.2 · HTTP-протокол и Real-Time',
    '2.3': 'Юнит 2.3 · REST API и веб-контракты',
    '2.4': 'Юнит 2.4 · Веб-безопасность',
}

BACKEND_UNITS = {
    '3.1': 'Юнит 3.1 · Часть I — Фреймворк FastAPI и Pydantic v2',
    '3.2': 'Юнит 3.2 · Часть II — Фреймворк Django и ORM',
    '3.3': 'Юнит 3.3 · Часть III — Фреймворк Django REST Framework (DRF)',
    '3.4': 'Юнит 3.4 · Часть IV — Микрофреймворк Flask',
    '3.5': 'Юнит 3.5 · Часть V — Аутентификация, авторизация и криптозащита',
    '3.6': 'Юнит 3.6 · Часть VI — Слоистая архитектура, транзакции и кэширование',
    '3.7': 'Юнит 3.7 · Часть VII — Отказоустойчивые интеграции, очереди и Rate Limiting',
    '3.8': 'Юнит 3.8 · Часть VIII — Файлы и S3, 12-Factor, Observability и тестирование API',
}

UNIT_LEGACY_TO_MOD3 = {
    '2.5': '3.1',
    '2.7': '3.5',
    '2.8': '3.6',
    '2.9': '3.7',
    '2.10': '3.8',
}

K_TARGET_UNIT = {
    # Web 2.1
    'К-062': ('web', '2.1'), 'К-063': ('web', '2.1'), 'К-064': ('web', '2.1'), 'К-065': ('web', '2.1'),
    # Web 2.2
    'К-066': ('web', '2.2'), 'К-067': ('web', '2.2'), 'К-068': ('web', '2.2'), 'К-069': ('web', '2.2'),
    'К-070': ('web', '2.2'), 'К-071': ('web', '2.2'), 'К-072': ('web', '2.2'), 'К-073': ('web', '2.2'),
    # Web 2.3
    'К-074': ('web', '2.3'), 'К-075': ('web', '2.3'), 'К-076': ('web', '2.3'), 'К-077': ('web', '2.3'),
    'К-078': ('web', '2.3'), 'К-080': ('web', '2.3'), 'К-225': ('web', '2.3'),
    # Web 2.4
    'К-104': ('web', '2.4'), 'К-105': ('web', '2.4'), 'К-106': ('web', '2.4'), 'К-107': ('web', '2.4'),
    # Backend 3.1 (Часть I — FastAPI и Pydantic v2)
    'К-236': ('backend', '3.1'), 'К-079': ('backend', '3.1'), 'К-090': ('backend', '3.1'),
    'К-092': ('backend', '3.1'), 'К-093': ('backend', '3.1'), 'К-094': ('backend', '3.1'),
    'К-227': ('backend', '3.1'),
    # Backend 3.2 (Часть II — Django и ORM)
    'К-083': ('backend', '3.2'), 'К-082': ('backend', '3.2'), 'К-084': ('backend', '3.2'),
    'К-088': ('backend', '3.2'), 'К-087': ('backend', '3.2'), 'К-086': ('backend', '3.2'),
    'К-085': ('backend', '3.2'), 'К-081': ('backend', '3.2'),
    # Backend 3.3 (Часть III — Django REST Framework / DRF)
    'К-091': ('backend', '3.3'), 'К-237': ('backend', '3.3'), 'К-238': ('backend', '3.3'),
    # Backend 3.4 (Часть IV — Микрофреймворк Flask)
    'К-095': ('backend', '3.4'), 'К-097': ('backend', '3.4'), 'К-096': ('backend', '3.4'),
    'К-089': ('backend', '3.4'),
    # Backend 3.5 (Часть V — Аутентификация, авторизация и криптозащита)
    'К-098': ('backend', '3.5'), 'К-099': ('backend', '3.5'), 'К-100': ('backend', '3.5'),
    'К-101': ('backend', '3.5'), 'К-108': ('backend', '3.5'), 'К-102': ('backend', '3.5'),
    'К-103': ('backend', '3.5'),
    # Backend 3.6 (Часть VI — Слоистая архитектура, транзакции и кэширование)
    'К-228': ('backend', '3.6'), 'К-229': ('backend', '3.6'), 'К-230': ('backend', '3.6'),
    # Backend 3.7 (Часть VII — Отказоустойчивые интеграции, очереди и Rate Limiting)
    'К-224': ('backend', '3.7'), 'К-231': ('backend', '3.7'), 'К-232': ('backend', '3.7'),
    'К-109': ('backend', '3.7'),
    # Backend 3.8 (Часть VIII — Файлы и S3, 12-Factor, Observability и тестирование API)
    'К-233': ('backend', '3.8'), 'К-234': ('backend', '3.8'), 'К-235': ('backend', '3.8'),
    'К-226': ('backend', '3.8'),
}

F_TARGET_UNIT = {
    # Web 2.1
    'Ф-258': ('web', '2.1'), 'Ф-259': ('web', '2.1'), 'Ф-260': ('web', '2.1'), 'Ф-261': ('web', '2.1'),
    # Web 2.2
    'Ф-090': ('web', '2.2'), 'Ф-091': ('web', '2.2'), 'Ф-092': ('web', '2.2'), 'Ф-093': ('web', '2.2'),
    'Ф-094': ('web', '2.2'), 'Ф-095': ('web', '2.2'), 'Ф-262': ('web', '2.2'), 'Ф-263': ('web', '2.2'),
    # Web 2.3
    'Ф-099': ('web', '2.3'), 'Ф-100': ('web', '2.3'), 'Ф-101': ('web', '2.3'), 'Ф-103': ('web', '2.3'),
    'Ф-104': ('web', '2.3'), 'Ф-126': ('web', '2.3'), 'Ф-265': ('web', '2.3'), 'Ф-266': ('web', '2.3'),
    # Web 2.4
    'Ф-122': ('web', '2.4'), 'Ф-123': ('web', '2.4'), 'Ф-124': ('web', '2.4'), 'Ф-125': ('web', '2.4'),
    # Backend 3.1 (FastAPI & Pydantic v2)
    'Ф-282': ('backend', '3.1'), 'Ф-102': ('backend', '3.1'), 'Ф-114': ('backend', '3.1'),
    'Ф-115': ('backend', '3.1'), 'Ф-280': ('backend', '3.1'), 'Ф-222': ('backend', '3.1'),
    'Ф-272': ('backend', '3.1'),
    # Backend 3.2 (Django & ORM)
    'Ф-105': ('backend', '3.2'), 'Ф-106': ('backend', '3.2'), 'Ф-267': ('backend', '3.2'),
    'Ф-268': ('backend', '3.2'), 'Ф-097': ('backend', '3.2'), 'Ф-109': ('backend', '3.2'),
    'Ф-108': ('backend', '3.2'), 'Ф-223': ('backend', '3.2'),
    # Backend 3.3 (DRF)
    'Ф-112': ('backend', '3.3'), 'Ф-283': ('backend', '3.3'), 'Ф-284': ('backend', '3.3'),
    # Backend 3.4 (Flask)
    'Ф-285': ('backend', '3.4'), 'Ф-117': ('backend', '3.4'), 'Ф-116': ('backend', '3.4'),
    'Ф-113': ('backend', '3.4'),
    # Backend 3.5 (AuthN, AuthZ, Passwords)
    'Ф-118': ('backend', '3.5'), 'Ф-119': ('backend', '3.5'), 'Ф-096': ('backend', '3.5'),
    'Ф-120': ('backend', '3.5'), 'Ф-281': ('backend', '3.5'), 'Ф-121': ('backend', '3.5'),
    'Ф-270': ('backend', '3.5'),
    # Backend 3.6 (Layered Arch, UoW, Transactions, Caching)
    'Ф-273': ('backend', '3.6'), 'Ф-274': ('backend', '3.6'), 'Ф-275': ('backend', '3.6'),
    # Backend 3.7 (Integrations, Queues, Rate Limiting)
    'Ф-264': ('backend', '3.7'), 'Ф-276': ('backend', '3.7'), 'Ф-277': ('backend', '3.7'),
    'Ф-271': ('backend', '3.7'),
    # Backend 3.8 (Files/S3, 12-Factor, Observability, API Testing)
    'Ф-278': ('backend', '3.8'), 'Ф-185': ('backend', '3.8'), 'Ф-279': ('backend', '3.8'),
    'Ф-269': ('backend', '3.8'),
}

# Create all target unit directories
for ukey, uname in WEB_UNITS.items():
    os.makedirs(os.path.join(WEB_DIR, uname, '📚 Конспекты'), exist_ok=True)
    os.makedirs(os.path.join(WEB_DIR, uname, '📇 Карточки'), exist_ok=True)

for ukey, uname in BACKEND_UNITS.items():
    os.makedirs(os.path.join(BACKEND_DIR, uname, '📚 Конспекты'), exist_ok=True)
    os.makedirs(os.path.join(BACKEND_DIR, uname, '📇 Карточки'), exist_ok=True)

# Find all existing files in 02* and 03* directories and move them to their canonical locations
existing_files = []
for mod_dir in [OLD_MOD2, WEB_DIR, OLD_BACKEND_DIR, BACKEND_DIR]:
    if os.path.isdir(mod_dir):
        for r, d, files in os.walk(mod_dir):
            for fn in files:
                if fn.endswith('.md'):
                    existing_files.append(os.path.join(r, fn))

PY_UNIT_1_8_CARDS = os.path.join(BASE, '01 · 🐍 Python', 'Юнит 1.8 · Конкурентность', '📇 Карточки')

for full_p in existing_files:
    fn = os.path.basename(full_p)
    m = re.match(r'^([КФ]-\d+)\.', fn)
    if not m:
        continue
    cid = m.group(1)
    if cid == 'Ф-075':
        dest = os.path.join(PY_UNIT_1_8_CARDS, fn)
        if os.path.abspath(full_p) != os.path.abspath(dest):
            shutil.move(full_p, dest)
    elif cid.startswith('К-') and cid in K_TARGET_UNIT:
        side, ukey = K_TARGET_UNIT[cid]
        base_dir = WEB_DIR if side == 'web' else BACKEND_DIR
        uname = WEB_UNITS[ukey] if side == 'web' else BACKEND_UNITS[ukey]
        dest = os.path.join(base_dir, uname, '📚 Конспекты', fn)
        if os.path.abspath(full_p) != os.path.abspath(dest):
            shutil.move(full_p, dest)
    elif cid.startswith('Ф-') and cid in F_TARGET_UNIT:
        side, ukey = F_TARGET_UNIT[cid]
        base_dir = WEB_DIR if side == 'web' else BACKEND_DIR
        uname = WEB_UNITS[ukey] if side == 'web' else BACKEND_UNITS[ukey]
        dest = os.path.join(base_dir, uname, '📇 Карточки', fn)
        if os.path.abspath(full_p) != os.path.abspath(dest):
            shutil.move(full_p, dest)

# Remove OLD_MOD2 and OLD_BACKEND_DIR if they exist
for legacy_dir in [OLD_MOD2, OLD_BACKEND_DIR]:
    if os.path.isdir(legacy_dir):
        shutil.rmtree(legacy_dir, onexc=_force_remove_readonly)
        if not os.path.isdir(legacy_dir):
            print("Removed legacy folder:", legacy_dir)

# Clean any leftover empty unit directories inside WEB_DIR and BACKEND_DIR
for mod_dir, valid_units in [(WEB_DIR, set(WEB_UNITS.values())), (BACKEND_DIR, set(BACKEND_UNITS.values()))]:
    for entry in os.listdir(mod_dir):
        p = os.path.join(mod_dir, entry)
        if os.path.isdir(p) and entry not in valid_units:
            shutil.rmtree(p, onexc=_force_remove_readonly)

# ─── WRITE 9 NEW EXHAUSTIVE BACKEND NOTES (К-227 .. К-235) ─────────────────


NEW_K_NOTES = {
    'К-227': (
        '2.5',
        'К-227. Промышленный FastAPI_ Lifespan, Middleware, Exception Handlers и BackgroundTasks.md',
        r"""📖 Перечитать конспект: Промышленный FastAPI: Lifespan, Middleware, Exception Handlers и BackgroundTasks >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Управление жизненным циклом приложения: `lifespan` и Graceful Shutdown

В продакшене бэкенд-сервис не может создавать пул соединений с PostgreSQL, клиент Redis или HTTP-сессию `httpx.AsyncClient` при каждом запросе — это приведёт к исчерпанию сокетов и деградации latency. Все тяжёлые ресурсы инициализируются один раз при старте воркера и корректно закрываются при его остановке (**Graceful Shutdown**).

В современном FastAPI (начиная с версий Starlette 0.20+) устаревшие хуки `@app.on_event("startup")` и `@app.on_event("shutdown")` заменены единым асинхронным контекстным менеджером **`lifespan`** на базе `@asynccontextmanager`:

```python
from contextlib import asynccontextmanager

class ResourcePool:
    def __init__(self):
        self.connected = False
        self.events = []

    def connect(self):
        self.connected = True
        self.events.append("pool_opened")

    def close(self):
        self.connected = False
        self.events.append("pool_closed")

@asynccontextmanager
async def lifespan_demo(pool: ResourcePool):
    # Код ДО yield выполняется один раз перед приёмом первого HTTP-запроса
    pool.connect()
    try:
        yield {"db_pool": pool}
    finally:
        # Код ПОСЛЕ yield гарантированно выполняется при получении SIGTERM (Graceful Shutdown)
        pool.close()

import asyncio

async def main():
    pool = ResourcePool()
    async with lifespan_demo(pool) as state:
        print("Внутри работы сервера, connected =", state["db_pool"].connected)
    print("После остановки сервера, события:", pool.events)

asyncio.run(main())
```

Почему `lifespan` через `yield` лучше отдельных событий `startup` и `shutdown`:

- Переменные и объекты, созданные при старте, находятся в одной области видимости с блоком очистки `finally` — не нужно плодить глобальные переменные модуля.
- Блок `finally` срабатывает даже в случае необработанного исключения при работе приложения, предотвращая утечку открытых транзакций и дескрипторов.

---

## Конвейер ASGI Middleware: порядок выполнения «луковицы» (Onion Model)

**Middleware (промежуточное ПО)** перехватывает каждый входящий HTTP-запрос до того, как он попадёт в роутер, и каждый исходящий ответ перед отправкой клиенту. Через Middleware реализуют:

- Генерацию и проброс сквозного `X-Request-ID` (Correlation ID);
- Замер времени обработки запроса (`X-Process-Time`) и запись access-логов;
- Проверку CORS-заголовков (`CORSMiddleware`) и защиту от атак Host Header Injection (`TrustedHostMiddleware`).

Middleware образуют вложенную цепочку («луковицу»): при входе запрос проходит слои снаружи внутрь, а ответ возвращается в **обратном порядке** — изнутри наружу:

```python
import time

def run_middleware_pipeline(request: dict, middlewares: list, handler):
    def build_chain(index: int):
        if index == len(middlewares):
            return handler
        current_mw = middlewares[index]
        next_call = build_chain(index + 1)
        return lambda req: current_mw(req, next_call)

    chain = build_chain(0)
    return chain(request)

def trace_mw(req: dict, call_next):
    req["trace"] = req.get("trace", []) + ["-> trace_in"]
    resp = call_next(req)
    resp["trace"].append("<- trace_out")
    return resp

def timing_mw(req: dict, call_next):
    req["trace"].append("-> timing_in")
    t0 = time.perf_counter()
    resp = call_next(req)
    resp["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 3)
    resp["trace"].append("<- timing_out")
    return resp

def endpoint(req: dict):
    return {"status": 200, "path": req["path"], "trace": req["trace"] + ["[endpoint]"]}

result = run_middleware_pipeline({"path": "/api/v1/orders"}, [trace_mw, timing_mw], endpoint)
print("Путь прохождения слоёв:", " ".join(result["trace"]))
```

> **Инженерный нюанс FastAPI**: метод `app.add_middleware(MiddlewareClass)` оборачивает текущее приложение снаружи. Поэтому Middleware, добавленный **последним** в коде, будет встречать входящий запрос **первым**! Кроме того, для высоконагруженных сервисов вместо `@app.middleware("http")` (`BaseHTTPMiddleware`, который буферизует тело ответа и создаёт накладные расходы) пишут чистый ASGI Middleware: класс с методом `async def __call__(self, scope, receive, send)`.

---

## Глобальные обработчики исключений (`Exception Handlers`) и чистый доменный слой

Грубая архитектурная ошибка — импортировать `fastapi.HTTPException` внутрь сервисного слоя (`services/`) или репозиториев БД (`repositories/`). Если бизнес-логика выбрасывает `HTTPException(status_code=404)`, вы больше не сможете вызвать этот сервис из консольной команды CLI, воркера Celery или gRPC-хендлера.

**Правильный паттерн**:
1. Сервисный слой выбрасывает чистые доменные исключения Python (например, `InsufficientFundsError`, `OrderNotFoundError`).
2. На уровне FastAPI регистрируются глобальные обработчики через `@app.exception_handler(DomainError)`, которые транслируют доменную ошибку в стандартный JSON-ответ по **RFC 7807 (Problem Details)**:

```python
class DomainError(Exception):
    pass

class InsufficientFundsError(DomainError):
    def __init__(self, account_id: int,deficit: int):
        self.account_id = account_id
        self.deficit = deficit

def domain_exception_handler(request_path: str, exc: DomainError) -> dict:
    if isinstance(exc, InsufficientFundsError):
        return {
            "status_code": 422,
            "body": {
                "type": "https://api.example.com/errors/insufficient-funds",
                "title": "Insufficient Funds",
                "status": 422,
                "detail": f"Account {exc.account_id} lacks {exc.deficit} USD",
                "instance": request_path,
            },
        }
    return {"status_code": 500, "body": {"title": "Internal Error"}}

err = InsufficientFundsError(account_id=77, deficit=150)
http_resp = domain_exception_handler("/api/v1/payments", err)
print("HTTP", http_resp["status_code"], "->", http_resp["body"]["detail"])
```

---

## `BackgroundTasks` в FastAPI vs распределённые очереди (`Celery` / `arq`)

Объект `BackgroundTasks` в FastAPI позволяет запланировать функцию, которая выполнится **после** того, как клиент получит HTTP-ответ (например, отправить приветственное письмо или записать событие аналитики):

- **Как работает внутри**: `BackgroundTasks` выполняется **в том же процессе и Event Loop** веб-воркера `uvicorn` (если функция `async def`, она запускается в Event Loop; если обычная `def`, она отправляется в `anyio.to_thread.run_sync`).
- **Критические ограничения**:
  1. Если под деплоем или из-за OOM Killer контейнер `uvicorn` перезапустится до завершения фоновой задачи — задача **бесследно пропадёт** (нет персистентного брокера и подтверждений `ack`).
  2. Нет встроенного механизма повторных попыток (`retry` с `Exponential Backoff`) и защиты от перегрузки CPU веб-воркера.
  3. **Ловушка сессии БД**: нельзя передавать в `BackgroundTasks` сессию `db: AsyncSession = Depends(get_db)`, созданную для запроса! К моменту старта фоновой задачи блок `yield` зависимости `get_db` уже завершится и закроет сессию. Фоновая задача обязана открывать собственную сессию через фабрику `async_session_maker()`.

> **Junior vs Senior**:
> - **Junior**: Создаёт пул БД и `httpx.AsyncClient` на уровне глобальных переменных модуля (без закрытия при остановке), выбрасывает `HTTPException` прямо из глубины бизнес-сервисов и передаёт сессию `db` из роута внутрь `BackgroundTasks`, получая `InterfaceError: connection is closed`.
> - **Senior**: Управляет ресурсами через `@asynccontextmanager def lifespan(app)`, транслирует чистые доменные исключения в HTTP-ответы по RFC 7807 через `@app.exception_handler`, а в фоновые задачи передаёт только `ID` сущности, открывая для них изолированную сессию БД.
"""
    ),

    'К-228': (
        '2.8',
        'К-228. Слоистая архитектура бэкенда_ Router, Service Layer, Repository и паттерн Unit of Work.md',
        r"""📖 Перечитать конспект: Слоистая архитектура бэкенда: Router, Service Layer, Repository и паттерн Unit of Work >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Антипаттерн «Толстый контроллер» (Fat Router / Fat View)

В учебных проектах весь код пишут прямо внутри функции эндпоинта FastAPI или Django View: там же валидируют входные данные, пишут `SELECT` и `INSERT` через SQLAlchemy, считают скидки, проверяют баланс и отправляют HTTP-запрос в платёжный шлюз.

К чему это приводит в реальном бэкенде через 3 месяца:

- **Дублирование бизнес-правил**: когда создание заказа нужно вызвать не только из REST API, но и из Telegram-бота или фоновой задачи Celery, код приходится копировать.
- **Невозможность быстрых юнит-тестов**: чтобы проверить расчёт скидки в 5 строк, приходится поднимать тестовую БД и HTTP-клиент.
- **Хрупкость при смене хранилища**: SQL-запросы размазаны по десяткам роутеров.

Решение — **слоистая архитектура (Layered / Clean Architecture)** с жёстким правилом направления зависимостей: внешние слои (HTTP, БД) зависят от бизнес-логики, а не наоборот.

---

## Четыре канонических слоя современного Python-бэкенда

Разделим ответственность на 4 чётких слоя:

1. **Presentation / Transport Layer (`Router` / `View`)**:
   - Принимает HTTP-запрос, валидирует входной JSON через Pydantic-схему (`DTO`), извлекает текущего пользователя из зависимости, вызывает `Service Layer` и возвращает HTTP-статус и выходную схему. **Никаких `session.execute(select(...))` в роутере быть не должно!**
2. **Application / Service Layer (`Service` / `Use Case`)**:
   - Оркестрирует бизнес-сценарий: проверяет доменные инварианты, обращается к одному или нескольким репозиториям внутри единой транзакции (`Unit of Work`), публикует доменные события.
3. **Domain Layer (`Entities` / `Value Objects` / `Domain Exceptions`)**:
   - Чистые Python-классы (`dataclass`) и правила предметной области без привязки к FastAPI или ORM.
4. **Infrastructure / Data Access Layer (`Repository`)**:
   - Инкапсулирует работу с конкретной БД (SQLAlchemy, `asyncpg`, Redis). Для сервиса репозиторий выглядит как коллекция доменных объектов с методами `.get_by_id()`, `.add()`, `.list_active()`.

---

## Паттерн Repository: отделение бизнес-логики от ORM

**Паттерн Репозиторий (Repository)** скрывает детали запросов к БД за единым интерфейсом (через `abc.ABC` или `typing.Protocol`). Благодаря этому в юнит-тестах мы мгновенно подменяем `SqlAlchemyOrderRepository` на `InMemoryOrderRepository` (на обычном `dict`) и прогоняем сотни тестов за 10 миллисекунд:

```python
from dataclasses import dataclass
from typing import Protocol, Optional

@dataclass
class Order:
    id: int
    user_id: int
    amount: int
    status: str = "NEW"

class OrderRepositoryProtocol(Protocol):
    def get(self, order_id: int) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...

class InMemoryOrderRepository:
    def __init__(self):
        self._storage: dict[int, Order] = {}

    def get(self, order_id: int) -> Optional[Order]:
        return self._storage.get(order_id)

    def save(self, order: Order) -> None:
        self._storage[order.id] = order

repo = InMemoryOrderRepository()
repo.save(Order(id=1, user_id=42, amount=2500))
print("Заказ из репозитория:", repo.get(1))
```

---

## Паттерн Unit of Work (Единица работы): атомарность бизнес-транзакции

Представьте сценарий оплаты заказа: сервис должен:
1. Списать деньги с баланса в `WalletRepository`;
2. Изменить статус заказа на `"PAID"` в `OrderRepository`;
3. Записать событие начисления бонусов в `OutboxRepository`.

Если каждый репозиторий будет делать `session.commit()` внутри своего метода, то при ошибке на шаге 2 деньги спишутся, а заказ останется неоплаченным! Репозитории **никогда не делают `commit()` сами** — они только выполняют `add()` / `flush()` в общей сессии.

Управлением границами транзакции занимается паттерн **Unit of Work (UoW)**, реализуемый в Python как контекстный менеджер (`__enter__` / `__exit__` или `__aenter__` / `__aexit__`):

```python
class FakeUnitOfWork:
    def __init__(self):
        self.wallets = {"user_1": 1000}
        self.orders = {"ord_9": "NEW"}
        self._snapshot = None
        self.committed = False

    def __enter__(self):
        # Сохраняем снимок состояния на случай rollback
        self._snapshot = (dict(self.wallets), dict(self.orders))
        self.committed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None or not self.committed:
            # Автоматический откат всех изменений, если случилось исключение или забыли commit()
            self.wallets, self.orders = self._snapshot

    def commit(self):
        self.committed = True

def pay_order_service(uow: FakeUnitOfWork, user_id: str, order_id: str, price: int):
    with uow:
        if uow.wallets[user_id] < price:
            raise ValueError("Недостаточно средств")
        uow.wallets[user_id] -= price
        uow.orders[order_id] = "PAID"
        uow.commit()

uow = FakeUnitOfWork()
try:
    pay_order_service(uow, "user_1", "ord_9", price=1500)
except ValueError as e:
    print("Ошибка оплаты:", e)
print("Состояние после отката:", uow.wallets, uow.orders)

pay_order_service(uow, "user_1", "ord_9", price=400)
print("Состояние после успешного commit:", uow.wallets, uow.orders)
```

Главное преимущество `Unit of Work`: бизнес-сервис явно объявляет транзакционную границу блоком `async with uow:`, а при любом необработанном исключении внутри блока `__aexit__` автоматически вызывает `await uow.rollback()`, гарантируя 100% консистентность данных.

> **Junior vs Senior**:
> - **Junior**: Пишет SQL-запросы (`session.execute(select(...))`), проверку прав, расчёт скидок и вызов `session.commit()` прямо внутри функции роутера FastAPI или в каждом методе репозитория по отдельности.
> - **Senior**: Строго разделяет `Transport Layer (Router)` ➔ `Service Layer` ➔ `Repository`, запрещает репозиториям вызывать `commit()` самостоятельно и управляет атомарностью всей бизнес-операции через контекстный менеджер **Unit of Work (`async with uow:`)**.
"""
    ),

    'К-229': (
        '2.8',
        'К-229. Управление транзакциями, пулы соединений и конкурентные блокировки (SELECT FOR UPDATE vs Optimistic Lock).md',
        r"""📖 Перечитать конспект: Управление транзакциями, пулы соединений и конкурентные блокировки (SELECT FOR UPDATE vs Optimistic Lock) >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Пул соединений (Connection Pool): почему бэкенд падает под нагрузкой

Установка нового соединения с PostgreSQL — дорогая операция (~15–30 мс): TCP 3-way handshake, TLS-рукопожатие, аутентификация, выделение отдельного серверного процесса `postgres` (около 5–10 МБ RAM на каждое соединение). Если 500 одновременных запросов откроют по новому соединению, база данных упадёт с ошибкой `FATAL: sorry, too many clients already`.

Поэтому SQLAlchemy использует **Connection Pool (`QueuePool`)** — пул заранее открытых соединений, которые выдаются запросам во временное пользование (checkout) и возвращаются обратно после завершения транзакции (checkin):

- **`pool_size=10`** — количество постоянных соединений, которые пул держит открытыми.
- **`max_overflow=20`** — сколько дополнительных временных соединений пул может открыть при пиковом всплеске нагрузки (в сумме до `10 + 20 = 30` соединений на один процесс воркера).
- **`pool_timeout=30`** — сколько секунд запрос ждёт свободного соединения из пула перед выбросом `TimeoutError`.
- **`pool_pre_ping=True`** — перед выдачей соединения из пула SQLAlchemy выполняет лёгкий `SELECT 1`, чтобы убедиться, что СУБД или файрвол не разорвали соединение по таймауту простоя.
- **`pool_recycle=1800`** — принудительно переоткрывать соединения старше 30 минут.

> **Золотое правило эксплуатации**: никогда не держите транзакцию БД открытой во время сетевого похода во внешний HTTP API (`httpx.post`)! Пока внешний сервис отвечает 3 секунды, ваше соединение из `QueuePool` заблокировано, и соседние запросы встают в очередь.

---

## Аномалия Lost Update (Потерянное обновление) в финансовом бэкенде

Представьте, что у пользователя на балансе `1000 ₽`. Два параллельных запроса одновременно покупают два товара по `600 ₽`:

1. Запрос A читает баланс: `balance = 1000`.
2. Запрос B в ту же миллисекунду читает баланс: `balance = 1000`.
3. Запрос A проверяет `1000 >= 600` и записывает `UPDATE accounts SET balance = 400`.
4. Запрос B проверяет `1000 >= 600` и записывает `UPDATE accounts SET balance = 400`.

Итог: пользователь купил два товара на `1200 ₽`, а списалось только `600 ₽`! Стандартный уровень изоляции PostgreSQL (**`READ COMMITTED`**) **не защищает** от этой гонки при паттерне «прочитал в Python ➔ посчитал ➔ записал обратно».

---

## Три промышленных способа защиты от гонок данных в БД

### 1. Атомарный `UPDATE` на стороне СУБД (Atomic Expressions)
Если изменение можно выразить формулой от текущего значения столбца (`F('balance') - amount` в Django или `Account.balance - amount` в SQLAlchemy), база сама наложит блокировку строки на время выполнения инструкции:

```sql
UPDATE accounts
SET balance = balance - 600
WHERE id = 42 AND balance >= 600
RETURNING balance;
```

### 2. Пессимистичная блокировка (`SELECT ... FOR UPDATE`)
Если бизнес-логика сложная (нужно прочитать строку, проверить несколько таблиц и затем обновить), при чтении используется **`SELECT ... FOR UPDATE`** (`with_for_update()` в SQLAlchemy / `select_for_update()` в Django). СУБД ставит эксклюзивную блокировку (`Row-Level Lock`) на выбранные строки до конца транзакции:

- Второй параллельный запрос, пытающийся сделать `SELECT ... FOR UPDATE` этой же строки, **встанет на паузу**, пока первая транзакция не сделает `COMMIT` или `ROLLBACK`.
- Модификатор **`NOWAIT`** мгновенно выбрасывает ошибку, если строка уже заблокирована (полезно для защиты от повторного клика по кнопке оплаты).
- Модификатор **`SKIP LOCKED`** пропускает заблокированные строки и берёт следующую свободную — это фундамент для построения очередей задач и бронирования билетов поверх PostgreSQL!

### 3. Оптимистичная блокировка (`Optimistic Concurrency Control`)
Если конфликты происходят редко, держать блокировки в БД невыгодно. В таблицу добавляется столбец версии **`version INT NOT NULL DEFAULT 1`**. При обновлении мы проверяем, что версия строки не изменилась с момента нашего чтения:

```python
class OptimisticAccountTable:
    def __init__(self, balance: int):
        self.balance = balance
        self.version = 1

    def read(self) -> tuple[int, int]:
        return self.balance, self.version

    def update_balance(self, new_balance: int, expected_version: int) -> bool:
        # Эквивалент: UPDATE accounts SET balance=:b, version=version+1 WHERE id=:id AND version=:expected_v
        if self.version != expected_version:
            return False  # rowcount == 0 -> Конфликт версий (StaleDataError)!
        self.balance = new_balance
        self.version += 1
        return True

acc = OptimisticAccountTable(balance=1000)
bal_a, ver_a = acc.read()
bal_b, ver_b = acc.read()

print("Воркер A обновил:", acc.update_balance(bal_a - 600, ver_a))
print("Воркер B с устаревшей версией:", acc.update_balance(bal_b - 600, ver_b))
print("Итоговый баланс:", acc.balance, "Версия:", acc.version)
```

---

## Как избежать взаимных блокировок (`Deadlocks`) при `SELECT FOR UPDATE`

Если Транзакция 1 переводит деньги со счёта `id=10` на счёт `id=20` (блокируя сначала `10`, затем `20`), а встречная Транзакция 2 в то же время переводит со счёта `id=20` на счёт `id=10` (блокируя сначала `20`, затем `10`), возникает **Deadlock (взаимная блокировка)**. СУБД обнаружит цикл в графе ожидания через ~1 секунду и убьёт одну из транзакций.

**Строгий инвариант предотвращения Deadlock**: всегда захватывайте блокировки ресурсов в **едином детерминированном порядке** (например, по возрастанию `id`: сначала `min(from_id, to_id)`, затем `max(from_id, to_id)`):

```python
def lock_order_for_transfer(from_account_id: int, to_account_id: int) -> list[int]:
    if from_account_id == to_account_id:
        raise ValueError("Нельзя перевести самому себе")
    return sorted([from_account_id, to_account_id])

print("Порядок блокировки для 20 -> 10:", lock_order_for_transfer(20, 10))
print("Порядок блокировки для 10 -> 20:", lock_order_for_transfer(10, 20))
```

> **Junior vs Senior**:
> - **Junior**: Читает баланс через обычный `SELECT`, вычитает сумму в Python (`user.balance -= amount`) и сохраняет обратно, позволяя параллельным запросам увести баланс в минус (Lost Update), а также делает долгие HTTP-запросы к внешним API прямо внутри открытой транзакции БД.
> - **Senior**: Защищает конкурентные изменения денег и остатков через `SELECT ... FOR UPDATE` (блокируя счета строго в порядке возрастания `ID` для защиты от Deadlock) или Optimistic Locking с колонкой `version`, настраивает `pool_pre_ping=True` и никогда не держит транзакцию открытой во время сетевых вызовов.
"""
    ),

    'К-230': (
        '2.8',
        'К-230. Прикладное кэширование на бэкенде_ Redis, Cache-Aside, защита от Cache Stampede и Distributed Locks.md',
        r"""📖 Перечитать конспект: Прикладное кэширование на бэкенде: Redis, Cache-Aside, защита от Cache Stampede и Distributed Locks >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Почему локальный `lru_cache` опасен в многопроцессном бэкенде

Декоратор `@functools.lru_cache` хранит кэш прямо в оперативной памяти конкретного Python-процесса. В продакшене бэкенд всегда запускается в нескольких экземплярах (например, 4 воркера Gunicorn/Uvicorn × 3 реплики Kubernetes = 12 независимых процессов):

- Если пользователь обновил профиль на Воркере №1, остальные 11 воркеров продолжат отдавать устаревшие данные из своей локальной памяти (**рассинхронизация состояния**).
- Если кэшировать объекты без жёсткого `maxsize` и TTL, память воркера утечёт (**Memory Leak / OOM**).

Поэтому для разделяемого кэша в бэкенде используют **Redis** — сверхбыстрое in-memory хранилище структур данных (`Strings`, `Hashes`, `Sets`, `Sorted Sets`), к которому обращаются все воркеры по сети с задержкой `< 1 мс`.

---

## Паттерны кэширования: `Cache-Aside`, `Write-Through` и инвалидация

Самый распространённый паттерн на бэкенде — **Cache-Aside (Ленивое кэширование)**:

1. При чтении сервис сначала ищет ключ в Redis (`GET product:42`).
2. Если ключ найден (**Cache Hit**) — данные сразу возвращаются клиенту без обращения к PostgreSQL.
3. Если ключа нет (**Cache Miss**) — сервис читает данные из БД, сохраняет их в Redis с обязательным временем жизни **`TTL` (`SET product:42 ... EX 300`)** и возвращает ответ.
4. При изменении данных в БД (`UPDATE`) сервис **удаляет ключ из кэша (`DEL product:42`)**, а не пытается обновить его на месте (чтобы избежать гонки двух параллельных записей).

```python
import time

class CacheAsideService:
    def __init__(self):
        self.redis: dict[str, tuple[dict, float]] = {}
        self.db = {42: {"id": 42, "title": "Python Book", "price": 1500}}
        self.db_queries = 0

    def get_product(self, product_id: int) -> dict:
        key = f"product:{product_id}"
        now = time.time()
        if key in self.redis:
            val, expires_at = self.redis[key]
            if now < expires_at:
                return val
        # Cache Miss -> идём в БД
        self.db_queries += 1
        data = dict(self.db[product_id])
        self.redis[key] = (data, now + 60.0)
        return data

    def update_price(self, product_id: int, new_price: int) -> None:
        self.db[product_id]["price"] = new_price
        # Инвалидация кэша через удаление ключа
        self.redis.pop(f"product:{product_id}", None)

svc = CacheAsideService()
print("1-й вызов (Miss):", svc.get_product(42)["price"], "DB queries:", svc.db_queries)
print("2-й вызов (Hit):", svc.get_product(42)["price"], "DB queries:", svc.db_queries)
svc.update_price(42, 1290)
print("После инвалидации:", svc.get_product(42)["price"], "DB queries:", svc.db_queries)
```

---

## Катастрофа `Cache Stampede` (Эффект стада / Dogpiling) и способы защиты

Представьте главную страницу маркетплейса, кэш которой живёт `TTL = 60` секунд, а тяжёлый SQL-запрос её пересчёта выполняется `2` секунды. В секунду `60.000` кэш протухает, и за эти 2 секунды на сервер прилетает **5 000 запросов**. Все 5 000 запросов видят `Cache Miss` и одновременно бьют тяжёлым `SELECT` в PostgreSQL, мгновенно укладывая базу данных!

Три инженерных метода защиты от **Cache Stampede**:

1. **Distributed Lock (Мьютекс на пересчёт)**: первый воркер, увидевший промах кэша, захватывает короткую блокировку `SET lock:homepage 1 NX EX 5` и пересчитывает данные, а остальные ждут или отдают слегка устаревшую копию (`Stale-While-Revalidate`).
2. **TTL Jitter (Случайный разброс времени жизни)**: если при прогреве мы сохраняем 10 000 товаров с одинаковым `TTL = 3600`, через час они протухнут в одну секунду. Добавление случайной дельты `ttl = 3600 + random.randint(-300, 300)` размазывает нагрузку во времени.
3. **Probabilistic Early Expiration (Алгоритм XFetch)**: воркер с небольшой вероятностью пересчитывает кэш *за несколько секунд до* его реального истечения, когда остаток `TTL` приближается к времени пересчёта.

---

## Распределённые блокировки в Redis (`SET NX PX`) и безопасное освобождение

Как гарантировать, что фоновая задача расчёта зарплаты или обработка вебхука запустится ровно на одном воркере из десяти? Используется атомарная команда Redis:

`SET lock_key unique_token NX PX 10000`

- **`NX` (Not Exists)** — установить ключ только в том случае, если его ещё нет.
- **`PX 10000`** — автоматически удалить блокировку через 10 000 мс (защита от вечного зависания, если воркер упал с `SIGKILL`).
- **`unique_token` (`uuid4`)** — уникальный идентификатор конкретного воркера.

**Критическая ловушка при снятии блокировки**: нельзя просто делать `DEL lock_key`! Если Воркер №1 завис на 12 секунд (GC pause), его блокировка истекла по TTL на 10-й секунде, и её уже захватил Воркер №2. Очнувшись, Воркер №1 сделает `DEL lock_key` и **удалит чужую блокировку Воркера №2**! Освобождение обязано атомарно (через Lua-скрипт в Redis) проверять, что `GET(lock_key) == my_unique_token`:

```python
class SafeRedisLockSimulator:
    def __init__(self):
        self.store: dict[str, str] = {}

    def acquire(self, key: str, token: str) -> bool:
        if key in self.store:
            return False
        self.store[key] = token
        return True

    def release_lua_atomic(self, key: str, token: str) -> bool:
        # Эмуляция атомарного Lua-скрипта: if redis.call("get", KEYS[1]) == ARGV[1] then return redis.call("del", KEYS[1])
        if self.store.get(key) == token:
            del self.store[key]
            return True
        return False

redis_sim = SafeRedisLockSimulator()
print("Воркер 1 захватил лок:", redis_sim.acquire("lock:payout", "worker_1_uuid"))
print("Воркер 2 пытается снять чужой лок:", redis_sim.release_lua_atomic("lock:payout", "worker_2_uuid"))
print("Воркер 1 снимает свой лок:", redis_sim.release_lua_atomic("lock:payout", "worker_1_uuid"))
```

> **Junior vs Senior**:
> - **Junior**: Кэширует изменяемые данные БД через `@lru_cache` в памяти воркера, сохраняет ключи в Redis без `TTL` и снимает распределённую блокировку простым `redis.delete(lock_key)` без проверки владельца токена.
> - **Senior**: Строит кэширование в Redis по паттерну **Cache-Aside** с инвалидацией через `DEL`, добавляет **TTL Jitter** и мьютексы против **Cache Stampede**, а распределённые блокировки захватывает через `SET key uuid NX PX ttl` и освобождает атомарным Lua-скриптом.
"""
    ),

    'К-231': (
        '2.9',
        'К-231. Отказоустойчивые интеграции_ Circuit Breaker, Exponential Backoff с Jitter и Webhooks с HMAC.md',
        r"""📖 Перечитать конспект: Отказоустойчивые интеграции: Circuit Breaker, Exponential Backoff с Jitter и Webhooks с HMAC >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Каскадные отказы и почему обычные ретраи убивают упавший сервис

В распределённой системе ваш бэкенд постоянно вызывает внешние сервисы по HTTP: платёжные шлюзы, СМС-провайдеров, микросервисы доставки. Если внешний сервис начал отвечать ошибкой `503 Service Unavailable` или зависать по таймауту, наивный цикл `for attempt in range(5): time.sleep(2)` создаёт две катастрофы:

1. **Retry Storm (Шторм повторных запросов)**: если все 20 воркеров вашего бэкенда начнут синхронно повторять запросы каждые 2 секунды, они умножат нагрузку на восстанавливающийся сервис в 5 раз и не дадут ему подняться.
2. **Исчерпание собственных потоков/воркеров (Cascading Failure)**: пока ваши воркеры ждут таймаутов от мёртвого внешнего API, ваш собственный сервис перестаёт отвечать даже на те запросы клиентов, где внешний API не нужен.

---

## Exponential Backoff + Full Jitter: правильная математика ретраев

Повторять запрос можно **только для идемпотентных операций** (или при передаче заголовка `Idempotency-Key`) и **только при временных (transient) сбоях**: сетевых таймаутах, `429 Too Many Requests`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`. Повторять запрос при `400 Bad Request`, `401 Unauthorized` или `422 Unprocessable Entity` бессмысленно.

Чтобы рассинхронизировать воркеры и снизить давление на внешний сервис, задержка между попытками растёт экспоненциально с добавлением случайного шума (**Full Jitter**):

$$t_{\text{sleep}} = \text{uniform}\left(0, \min\left(T_{\max}, T_{\text{base}} \cdot 2^{\text{attempt}}\right)\right)$$

```python
import random

def compute_backoff_delays(max_retries: int, base: float = 0.5, cap: float = 10.0, seed: int = 42) -> list[float]:
    rng = random.Random(seed)
    delays = []
    for attempt in range(max_retries):
        exp_ceil = min(cap, base * (2 ** attempt))
        sleep_sec = round(rng.uniform(0, exp_ceil), 3)
        delays.append(sleep_sec)
    return delays

print("Интервалы ожидания с Full Jitter (сек):", compute_backoff_delays(5))
```

В реальных проектах на Python эту логику не пишут вручную в каждом методе, а используют проверенную библиотеку **`tenacity`** (`@retry(wait=wait_random_exponential(multiplier=0.5, max=10), stop=stop_after_attempt(4))`).

---

## Паттерн Circuit Breaker (Автоматический выключатель)

Когда внешний сервис полностью лёг, ждать таймаута даже по 2 секунды на каждый запрос непозволительно. Паттерн **Circuit Breaker** работает как электрический автомат в щитке и имеет 3 состояния:

- **`CLOSED` (Замкнут — штатный режим)**: запросы проходят к внешнему сервису. Счётчик ошибок отслеживает сбои. Как только число ошибок подряд достигает порога `failure_threshold` (например, 5 ошибок), автомат «выбивает».
- **`OPEN` (Разомкнут — авария)**: все вызовы мгновенно (за `0 мс`, без сетевого запроса!) завершаются исключением `CircuitBreakerOpenError` или возвращают fallback-ответ (например, данные из кэша или сообщение «Оплата временно в очереди»).
- **`HALF_OPEN` (Полуоткрыт — проверка восстановления)**: по истечении `recovery_timeout` (например, через 30 секунд) автомат пропускает **один** пробный запрос. Если он успешен (`200 OK`) — автомат возвращается в `CLOSED` и сбрасывает счётчик; если снова ошибка — мгновенно возвращается в `OPEN`.

```python
class SimpleCircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.failures = 0
        self.opened_at = 0.0

    def call(self, func, now_ts: float):
        if self.state == "OPEN":
            if now_ts - self.opened_at >= self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise RuntimeError("CircuitBreaker is OPEN (fast fail)")

        try:
            result = func()
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold or self.state == "HALF_OPEN":
                self.state = "OPEN"
                self.opened_at = now_ts
            raise
        else:
            self.failures = 0
            self.state = "CLOSED"
            return result

cb = SimpleCircuitBreaker(failure_threshold=2, recovery_timeout=10.0)
for t in [1.0, 2.0]:
    try:
        cb.call(lambda: (_ for _ in ()).throw(ConnectionError("503")), now_ts=t)
    except Exception:
        pass
print("Состояние после 2 сбоев:", cb.state)
print("После ожидания 15 сек и успешного ответа:", cb.call(lambda: "200 OK", now_ts=17.0), "| state =", cb.state)
```

---

## Входящие и исходящие Webhooks: криптографическая подпись HMAC-SHA256

Когда платёжный шлюз (Stripe, ЮKassa) или GitHub присылает вашему бэкенду HTTP `POST /webhooks/payment` о том, что заказ №500 оплачен, **злоумышленник может узнать URL этого эндпоинта и прислать поддельный JSON `{"order_id": 500, "status": "succeeded"}`**.

Как убедиться, что вебхук прислал именно настоящий провайдер, и тело запроса не было изменено по пути?

1. У провайдера и вашего бэкенда есть общий секретный ключ `WEBHOOK_SECRET`.
2. Провайдер берёт **сырые байты тела запроса (`raw_body`)** (часто вместе с заголовком `X-Webhook-Timestamp` для защиты от **Replay Attack** — повторной отправки перехваченного пакета спустя час), вычисляет **`HMAC-SHA256`** и передаёт хеш в заголовке `X-Signature`.
3. Ваш бэкенд вычисляет HMAC от полученных сырых байтов тем же секретом и сравнивает подписи строго через **`hmac.compare_digest(a, b)`** (защита от **Timing Attack** — посимвольного подбора подписи по времени ответа сервера!):

```python
import hmac
import hashlib

def sign_webhook(secret: str, timestamp: str, raw_body: bytes) -> str:
    payload_to_sign = timestamp.encode("utf-8") + b"." + raw_body
    return hmac.new(secret.encode("utf-8"), payload_to_sign, hashlib.sha256).hexdigest()

def verify_webhook(secret: str, timestamp: str, raw_body: bytes, signature_header: str, now_ts: int, tolerance: int = 300) -> bool:
    if abs(now_ts - int(timestamp)) > tolerance:
        return False  # Защита от Replay Attack (пакет старше 5 минут)
    expected_sig = sign_webhook(secret, timestamp, raw_body)
    return hmac.compare_digest(expected_sig, signature_header)

secret = "whsec_live_987654321"
body = b'{"event":"payment.succeeded","order_id":500}'
sig = sign_webhook(secret, "1700000100", body)

print("Подлинная подпись:", verify_webhook(secret, "1700000100", body, sig, now_ts=1700000120))
print("Подделка суммы в теле:", verify_webhook(secret, "1700000100", b'{"event":"payment.succeeded","order_id":999}', sig, now_ts=1700000120))
print("Просроченный Replay-пакет:", verify_webhook(secret, "1700000100", body, sig, now_ts=1700000900))
```

> **Junior vs Senior**:
> - **Junior**: Делает наивный `for _ in range(5): time.sleep(1)` при любой ошибке внешнего API (вызывая Retry Storm и каскадное падение своего сервиса), а входящие платёжные вебхуки принимает без проверки криптографической подписи или сверяет подпись через `==`.
> - **Senior**: Применяет **Exponential Backoff + Full Jitter** в связке с **Circuit Breaker (`CLOSED`/`OPEN`/`HALF_OPEN`)**, а входящие вебхуки верифицирует по сырым байтам `raw_body` + `timestamp` через `HMAC-SHA256` и `hmac.compare_digest`.
"""
    ),

    'К-232': (
        '2.9',
        'К-232. Фоновые воркеры и очереди сообщений_ Celery, RabbitMQ, Kafka, Transactional Outbox и DLQ.md',
        r"""📖 Перечитать конспект: Фоновые воркеры и очереди сообщений: Celery, RabbitMQ, Kafka, Transactional Outbox и DLQ >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Зачем выносить задачи из HTTP-запроса в фоновые воркеры

Золотой стандарт отзывчивости веб-API — время ответа (latency p95) **до 100–200 мс**. Любая операция, которая:
- генерирует PDF-отчёт или ресайзит изображения (CPU-bound),
- отправляет письма по SMTP или стучится в медленные внешние API (I/O-bound),
- пересчитывает рекомендации для тысяч товаров или запускает ночную сверку по расписанию (Cron / `Celery Beat`),

должна выполняться **асинхронно вне HTTP-цикла**. Веб-сервер лишь сохраняет задачу в брокер сообщений и мгновенно возвращает клиенту **`202 Accepted`** с `task_id`.

---

## Гарантии доставки, `acks_late`, идемпотентность воркеров и Dead Letter Queue (DLQ)

В распределённых очередях (Celery поверх RabbitMQ/Redis) существует три теоретические гарантии доставки сообщений:
- **At-most-once (Не более одного раза)**: воркер забирает задачу и сразу удаляет её из очереди (`ack` до выполнения). Если воркер упадёт по OOM в середине расчёта — задача потеряна навсегда.
- **At-least-once (Хотя бы один раз — промышленный стандарт)**: воркер отправляет подтверждение `ACK` брокеру **только после успешного завершения функции** (в Celery за это отвечает настройка `task_acks_late = True`).
- **Следствие `At-least-once`**: если воркер выполнил задачу, но сеть моргнула прямо перед отправкой `ACK`, брокер вернёт задачу в очередь и отдаст другому воркеру! Поэтому **каждая фоновая задача обязана быть идемпотентной** (проверять по `event_id` или статусу в БД, не была ли она уже выполнена).

Что делать, если сообщение содержит битые данные («отравленное сообщение» — **Poison Pill**), из-за которых воркер падает при каждой попытке?
После исчерпания лимита повторов (`max_retries=3`) сообщение перенаправляется в специальную очередь **Dead Letter Queue (DLQ)** для разбора инженерами и алертинга, чтобы не блокировать обработку остальных задач.

---

## RabbitMQ vs Apache Kafka: когда выбрать брокер очередей, а когда лог событий

На собеседованиях постоянно спрашивают разницу между классическим брокером сообщений (**RabbitMQ**) и распределённым журналом событий (**Apache Kafka**):

| Характеристика | RabbitMQ (AMQP — Smart Broker, Dumb Consumer) | Apache Kafka (Event Log — Dumb Broker, Smart Consumer) |
| :--- | :--- | :--- |
| **Модель данных** | Очередь (Queue), из которой сообщение **удаляется** сразу после `ACK` от воркера | Неизменяемый упорядоченный лог на диске (Partition), где события хранятся днями/неделями |
| **Маршрутизация** | Гибкие `Exchange` (`direct`, `topic`, `fanout`, `headers`), приоритеты задач, индивидуальные задержки | Чтение подряд по смещению (`offset`) внутри партиции топика |
| **Масштабирование чтения** | Несколько воркеров разбирают одну очередь по кругу (Competing Consumers) | Независимые **Consumer Groups**: аналитика, антифрод и биллинг читают один и тот же топик параллельно со своим `offset` |
| **Главный сценарий** | Фоновые задачи (`Celery`), отправка писем, генерация файлов, сложная маршрутизация команд | Стриминг событий (`OrderCreated`), аудит, аналитические пайплайны, возможность «перемотать» (`replay`) историю событий назад |

---

## Проблема двойной записи (Dual Write) и паттерн Transactional Outbox

Представьте код сервиса создания заказа с антипаттерном двойной записи (`Dual Write`):

```python
# Демонстрация проблемы Dual Write (рассинхронизация БД и брокера при сбое сети):
def dual_write_antipattern(order_id: int, broker_down: bool = True) -> dict:
    db_orders = [order_id]  # 1. Заказ уже закоммичен в PostgreSQL
    broker_events = []
    try:
        if broker_down:
            raise ConnectionError("Брокер Kafka/RabbitMQ временно недоступен!")
        broker_events.append(f"OrderCreated:{order_id}")
    except ConnectionError as err:
        return {"db_orders": db_orders, "broker_events": broker_events, "error": str(err)}

print("Результат антипаттерна Dual Write:", dual_write_antipattern(101))
```

Что произошло? Шаг 1 (`db_session.commit()`) прошёл успешно, а за миллисекунду до шага 2 моргнула сеть до RabbitMQ/Kafka. Заказ создан в БД, но событие `OrderCreated` **никогда не попадёт в брокер** — склад не соберёт посылку, а чек не отправится! А если поменять шаги местами (сначала отправить в Kafka, потом сделать `commit`), то при ошибке `commit` в брокер улетит фантомное событие о несуществующем заказе.

Решение этой фундаментальной проблемы — паттерн **Transactional Outbox**:

1. В той же реляционной БД PostgreSQL создаётся таблица **`outbox_events`** (`id`, `topic`, `payload`, `status='PENDING'`, `created_at`).
2. Бизнес-сервис в **одной атомарной транзакции БД** вставляет строку в таблицу `orders` И строку в таблицу `outbox_events`. Либо сохранятся обе записи, либо ни одной!
3. Отдельный фоновый процесс (**Outbox Relay / Publisher** или CDC-коннектор Debezium) вычитывает пачки строк из `outbox_events` со статусом `PENDING` (используя `SELECT ... FOR UPDATE SKIP LOCKED`), отправляет их в Kafka/RabbitMQ и после подтверждения брокера помечает как `PUBLISHED`:

```python
class TransactionalOutboxSimulator:
    def __init__(self):
        self.orders_table = []
        self.outbox_table = []
        self.broker_published = []

    def create_order_atomic(self, order_id: int, total: int, fail_db: bool = False):
        staged_order = {"id": order_id, "total": total}
        staged_event = {"event_id": f"evt_{order_id}", "topic": "order.created", "payload": staged_order, "sent": False}
        if fail_db:
            raise RuntimeError("DB Transaction Rollback")
        # Оба изменения фиксируются в одной транзакции СУБД
        self.orders_table.append(staged_order)
        self.outbox_table.append(staged_event)

    def run_outbox_relay_worker(self):
        for evt in self.outbox_table:
            if not evt["sent"]:
                self.broker_published.append(evt["payload"])
                evt["sent"] = True

sim = TransactionalOutboxSimulator()
sim.create_order_atomic(order_id=101, total=4900)
sim.run_outbox_relay_worker()
print("Заказы в БД:", len(sim.orders_table), "| Доставлено в брокер:", sim.broker_published)
```

> **Junior vs Senior**:
> - **Junior**: Делает `db.commit()` и сразу за ним `celery_app.send_task(...)` или `kafka.send(...)` (теряя задачи при любом сетевом сбое брокера — проблема Dual Write) и пишет неидемпотентные воркеры, которые при повторной доставке списывают деньги дважды.
> - **Senior**: Гарантирует доставку событий через паттерн **Transactional Outbox**, включает `task_acks_late=True` с идемпотентной обработкой по `event_id` и настраивает **Dead Letter Queue (DLQ)** для изоляции сбойных сообщений.
"""
    ),

    'К-233': (
        '2.10',
        'К-233. Потоковая работа с файлами (Streaming) и объектные хранилища S3 (Presigned URLs, Multipart Upload).md',
        r"""📖 Перечитать конспект: Потоковая работа с файлами (Streaming) и объектные хранилища S3 (Presigned URLs, Multipart Upload) >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Почему нельзя читать загружаемый файл целиком в память (`await file.read()`)

Если пользователь загружает видеоролик или CSV-выгрузку размером `500 МБ`, а в вашем эндпоинте написано `data = await upload_file.read()`, Python выделит `500 МБ` непрерывного буфера в RAM. Достаточно 4 одновременных запросов от пользователей, чтобы контейнер с лимитом `2 ГБ RAM` был мгновенно убит ядром Linux (**OOM Killer — Exit Code 137**).

Правила безопасной работы с файлами на бэкенде:

1. **Потоковое чтение по чанкам (Chunked Streaming)**: читать и хешировать/пересылать файл фиксированными блоками по `64 КБ – 1 МБ` (`while chunk := await file.read(65536): ...`). При этом потребление памяти воркера остаётся константным **$O(1)$** независимо от того, весит файл `5 МБ` или `50 ГБ`.
2. **Генерация больших отчётов на лету (`StreamingResponse`)**: при выгрузке большого CSV/JSON-отчёта из БД данные отдаются через асинхронный генератор (`yield row_bytes`), чтобы не формировать гигантскую строку в оперативной памяти.

```python
import hashlib
import io

def stream_sha256_and_size(binary_stream: io.BytesIO, chunk_size: int = 16, max_bytes: int = 1024) -> tuple[str, int]:
    hasher = hashlib.sha256()
    total_bytes = 0
    while chunk := binary_stream.read(chunk_size):
        total_bytes += len(chunk)
        if total_bytes > max_bytes:
            raise ValueError(f"Превышен лимит размера файла: {max_bytes} байт")
        hasher.update(chunk)
    return hasher.hexdigest()[:16], total_bytes

stream = io.BytesIO(b"Python Backend Streaming Data " * 10)
digest, size = stream_sha256_and_size(stream, chunk_size=32, max_bytes=1000)
print(f"Потоковый расчёт: {size} байт, sha256[:16]={digest}")
```

---

## Безопасность загрузки файлов: проверка Magic Bytes и защита от Path Traversal

Никогда не доверяйте заголовку `Content-Type: image/png` и имени файла `file.filename`, которые прислал клиент:

- **Подмена расширения и MIME-типа**: злоумышленник может переименовать вредоносный скрипт `exploit.html` или `shell.py` в `avatar.png`. Настоящий формат файла проверяют по **первым байтам заголовка файла (Magic Bytes / File Signatures)**: например, любой настоящий PNG начинается с 8 байт `\x89PNG\r\n\x1a\n`, JPEG — с `\xff\xd8\xff`, а PDF — с `%PDF-`.
- **Атака Path Traversal (`../../etc/passwd`)**: если склеить путь сохранения через `os.path.join("/var/uploads", file.filename)`, а имя файла равно `"../../app/main.py"`, злоумышленник перезапишет исходный код сервера!
  - **Защита**: никогда не используйте пользовательское имя файла на диске или в бакете — генерируйте случайное имя **`f"{uuid.uuid4()}.png"`**, а оригинальное имя храните только как метаданные в таблице БД.

```python
MAGIC_SIGNATURES = {
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/jpeg": b"\xff\xd8\xff",
    "application/pdf": b"%PDF-",
}

def detect_safe_mime(header_bytes: bytes) -> str:
    for mime, sig in MAGIC_SIGNATURES.items():
        if header_bytes.startswith(sig):
            return mime
    raise ValueError("Неразрешённый или поддельный формат файла")

print("Проверка PNG:", detect_safe_mime(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"))
```

---

## Почему файлы нельзя хранить в локальной папке контейнера: объектные хранилища S3

В облачной инфраструктуре (Docker / Kubernetes) контейнеры **эфемерны и stateless**:
- При каждом деплое новой версии локальная файловая система контейнера пересоздаётся с нуля;
- Если запущено 3 реплики бэкенда, файл, сохранённый на диск Реплики №1, вернёт `404 Not Found`, когда следующий запрос попадёт на Реплику №2.

Поэтому все пользовательские файлы, аватарки, чеки и бэкапы хранят во внешнем **S3-совместимом объектном хранилище** (AWS S3, MinIO, Yandex Object Storage, Cloudflare R2), работая с ним из Python через библиотеки `boto3` или `aioboto3`.

---

## Архитектурный паттерн `Presigned URLs` (Предподписанные ссылки)

Если пропускать загрузку и скачивание гигабайтных файлов через Python-воркеры (`Клиент ➔ FastAPI ➔ S3`), воркеры будут заняты перекачкой байтов вместо обработки бизнес-запросов, а трафик удвоится.

В высоконагруженных системах используют **Presigned URLs**:
1. Клиент запрашивает у бэкенда разрешение на загрузку: `POST /api/v1/files/upload-ticket` (`{"filename": "report.pdf", "size": 4500000}`).
2. Бэкенд проверяет права пользователя, генерирует криптографически подписанный URL к S3 (`s3_client.generate_presigned_url('put_object', ...)`) со сроком жизни **5 минут** и возвращает его клиенту за `2 мс`.
3. Клиент загружает файл **напрямую в S3 (`PUT <presigned_url>`)**, полностью минуя Python-бэкенд!
4. Для очень больших файлов (`> 100 МБ`) применяется **S3 Multipart Upload**: файл режется клиентом на части по `5–10 МБ`, которые загружаются параллельно в несколько потоков, а при обрыве связи докачивается только упавший фрагмент.

> **Junior vs Senior**:
> - **Junior**: Вызывает `await file.read()` целиком в память (роняя воркер по OOM на первом же крупном видеофайле), доверяет расширению из `file.filename` и сохраняет загруженные файлы в локальную папку `./uploads/` внутри Docker-контейнера.
> - **Senior**: Обрабатывает потоки фиксированными чанками ($O(1)$ по памяти), проверяет бинарные сигнатуры **Magic Bytes**, генерирует ключи хранения через `uuid4()` и разгружает бэкенд с помощью прямых загрузок в **S3 по Presigned URLs** и **Multipart Upload**.
"""
    ),

    'К-234': (
        '2.10',
        'К-234. Конфигурация бэкенда по 12-Factor App_ pydantic-settings, валидация окружения и ротация секретов.md',
        r"""📖 Перечитать конспект: Конфигурация бэкенда по 12-Factor App: pydantic-settings, валидация окружения и ротация секретов >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Методология 12-Factor App: строгая изоляция конфигурации от кода

Третий принцип манифеста **The Twelve-Factor App** гласит: **конфигурация приложения должна храниться в переменных окружения (`Environment Variables`), а не в исходном коде**.

Один и тот же скомпилированный Docker-образ приложения должен без единой правки кода запускаться в окружениях `local`, `staging`, `ci` и `production`, получая адреса БД, лимиты пулов и секретные ключи из внешней среды.

**Почему разрозненные вызовы `os.getenv("DB_HOST")` по всему коду — это антипаттерн**:
1. `os.getenv()` всегда возвращает `str | None`: легко получить `"False"`, которая в Python при `bool("False")` вычисляется в **`True`**!
2. Если в `production` забыли передать переменную `STRIPE_WEBHOOK_SECRET`, вызов `os.getenv()` внутри редкого роутера упадёт только спустя неделю, когда первый клиент попытается оплатить заказ, вместо того чтобы заблокировать деплой на первой секунде старта.

---

## Типизированная конфигурация через `pydantic-settings` (`Fail-Fast` на старте)

Стандарт де-факто в современном Python-бэкенде — библиотека **`pydantic-settings`** (`BaseSettings`). Она собирает все переменные окружения в единый строго типизированный объект, автоматически приводит типы (`int`, `bool`, `PostgresDsn`, `SecretStr`) и **валидирует конфигурацию в момент старта процесса**:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class AppSettings:
    app_env: str
    db_dsn: str
    db_pool_size: int
    debug: bool
    jwt_secret: str

    @classmethod
    def from_env(cls, env: dict[str, str]) -> "AppSettings":
        missing = [k for k in ("DB_DSN", "JWT_SECRET") if not env.get(k)]
        if missing:
            raise ValueError(f"Fail-Fast: отсутствуют обязательные переменные окружения: {missing}")

        raw_debug = env.get("DEBUG", "false").strip().lower()
        if raw_debug not in ("true", "false", "1", "0"):
            raise ValueError(f"Некорректный булев флаг DEBUG={raw_debug!r}")
        debug = raw_debug in ("true", "1")

        app_env = env.get("APP_ENV", "production")
        if app_env == "production" and debug:
            raise ValueError("Критическая ошибка безопасности: DEBUG=True запрещён в production!")

        if len(env["JWT_SECRET"]) < 32:
            raise ValueError("JWT_SECRET должен быть не короче 32 символов")

        return cls(
            app_env=app_env,
            db_dsn=env["DB_DSN"],
            db_pool_size=int(env.get("DB_POOL_SIZE", "10")),
            debug=debug,
            jwt_secret=env["JWT_SECRET"],
        )

cfg = AppSettings.from_env({
    "APP_ENV": "production",
    "DB_DSN": "postgresql+asyncpg://app:pass@db:5432/orders",
    "JWT_SECRET": "super_secret_production_key_32_bytes_min!",
})
print("Конфигурация валидна:", cfg.app_env, "| pool_size =", cfg.db_pool_size, "| debug =", cfg.debug)
```

---

## Защита секретов от утечки в логи и трейсбеки (`SecretStr`)

Если хранить пароли от БД и API-ключи в обычных строках `str`, то при случайном `logger.info("Loaded config: %s", settings)` или при дампе локальных переменных в Sentry все боевые ключи окажутся в открытом виде в системе сбора логов (ELK / Grafana Loki).

Тип **`SecretStr`** из Pydantic маскирует значение при любом преобразовании в строку или `repr()`, выводя `'**********'`. Получить реальное значение можно только явным вызовом метода **`.get_secret_value()`** в месте установки сетевого соединения:

```python
class SecretStrDemo:
    def __init__(self, value: str):
        self._secret = value

    def get_secret_value(self) -> str:
        return self._secret

    def __repr__(self) -> str:
        return "SecretStr('**********')"

    def __str__(self) -> str:
        return "**********"

api_key = SecretStrDemo("sk_live_998877665544332211")
print(f"Безопасный вывод в лог: api_key={api_key!r}")
print("Явное извлечение для заголовка Authorization:", api_key.get_secret_value()[:10] + "...")
```

---

## Бесшовная ротация ключей (Zero-Downtime Secret Rotation) и инъекция настроек

Как сменить `JWT_SECRET` или ключ шифрования в продакшене так, чтобы не разлогинить одновременно 100 000 активных пользователей и не уронить сервис?
Применяется паттерн **Dual-Key Verification (Список активных ключей)**:

- В настройках задаётся список ключей `JWT_SECRETS = ["new_key_2026", "old_key_2025"]`.
- **Новые токены** всегда подписываются **первым (самым свежим)** ключом `JWT_SECRETS[0]`.
- **Проверка входящих токенов** пробует верифицировать подпись по очереди каждым ключом из списка `JWT_SECRETS`. Когда время жизни старых токенов (`TTL`) истечёт, старый ключ безопасно удаляется из списка.

> **Совет для тестирования**: никогда не импортируйте глобальный объект `settings` напрямую внутрь глубоких функций, если его нужно менять в тестах. Оборачивайте получение настроек в функцию `get_settings()` с `@lru_cache` и пробрасывайте через `Depends(get_settings)` — тогда в тестах вы легко подмените настройки через `app.dependency_overrides[get_settings]`.

> **Junior vs Senior**:
> - **Junior**: Разбрасывает вызовы `os.getenv(...)` по десяткам файлов, пишет `bool(os.getenv("DEBUG"))` (получая `True` для строки `"False"`!) и хранит пароли в обычных строках `str`, которые утекают в логи при первом же трейсбеке.
> - **Senior**: Валидирует всю конфигурацию по принципу **Fail-Fast** на старте приложения через `pydantic-settings` (`BaseSettings`), защищает секреты типом `SecretStr`, инъектирует настройки через `Depends(get_settings)` и предусматривает бесшовную ротацию ключей (`Dual-Key Verification`).
"""
    ),

    'К-235': (
        '2.10',
        'К-235. Наблюдаемость (Observability) бэкенда_ JSON-логи, Correlation ID (contextvars), метрики Prometheus и Health Checks.md',
        r"""📖 Перечитать конспект: Наблюдаемость (Observability) бэкенда: JSON-логи, Correlation ID (contextvars), метрики Prometheus и Health Checks >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Три столпа наблюдаемости (Three Pillars of Observability)

Когда в микросервисном бэкенде 1% заказов завершается ошибкой `500` или начинает тормозить, подключиться по SSH и читать текстовый файл глазами невозможно. Промышленная наблюдаемость опирается на три столпа:

1. **Логи (Structured Logs)** — дискретные записи о событиях в формате **JSON** (индексируются в Elasticsearch / OpenSearch / Grafana Loki).
2. **Метрики (Metrics)** — числовые временные ряды (`Prometheus` + `Grafana`), показывающие агрегированное здоровье системы в реальном времени (RPS, процент 5xx ошибок, квантили времени ответа `p50 / p95 / p99`, загрузка пула БД).
3. **Трейсы (Distributed Tracing / OpenTelemetry)** — сквозное дерево прохождения одного запроса через все микросервисы, базу данных и Redis с точным таймингом каждого участка (`Span`).

---

## Сквозной `Correlation ID` (`X-Request-ID`) в асинхронном Python через `contextvars`

В асинхронном сервере (`uvicorn` / `FastAPI`) один поток ОС одновременно обрабатывает сотни корутин. Если записывать в обычный текстовый лог строку `"Ошибка списания баланса"`, вы никогда не поймёте, к какому именно HTTP-запросу и пользователю она относится.

Для связывания всех логов одного запроса используется **Correlation ID (`X-Request-ID`)** и встроенный модуль **`contextvars`**:
- Middleware на входе читает заголовок `X-Request-ID` (или генерирует новый `uuid4`) и кладёт его в `ContextVar`.
- Значение `ContextVar` автоматически наследуется всеми вложенными `await`-вызовами этого запроса, но **полностью изолировано** от соседних параллельных корутин в том же Event Loop!
- JSON-форматтер логгера автоматически добавляет `request_id` в каждую запись лога.

```python
import asyncio
import contextvars
import json

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="system")

def log_json(level: str, event: str, **extra) -> str:
    record = {"level": level, "request_id": request_id_var.get(), "event": event, **extra}
    return json.dumps(record, ensure_ascii=False)

async def handle_request(req_id: str, user_id: int):
    token = request_id_var.set(req_id)
    try:
        await asyncio.sleep(0.01)
        print(log_json("INFO", "payment_started", user_id=user_id))
    finally:
        request_id_var.reset(token)

async def main():
    await asyncio.gather(
        handle_request("req-aaa-111", 10),
        handle_request("req-bbb-222", 20),
    )

asyncio.run(main())
```

---

## Метрики Prometheus (RED-метод) и опасность High Cardinality

Для мониторинга каждого бэкенд-сервиса применяется **метод RED**:
- **Rate** — количество запросов в секунду (`http_requests_total`);
- **Errors** — количество ошибочных ответов в секунду (`status=~"5.."` );
- **Duration** — распределение времени ответа (квантили `p95`, `p99`).

Четыре базовых типа метрик в **Prometheus**:
- **`Counter`** — монотонно растущий счётчик (сбрасывается только при рестарте процесса): число запросов, число ошибок, число отправленных писем.
- **`Gauge`** — датчик, значение которого может как расти, так и уменьшаться: текущее число активных WebSocket-соединений, размер очереди, объём занятой памяти.
- **`Histogram`** — раскладывает замеры (например, время ответа) по заранее заданным корзинам (`buckets`: `0.01s, 0.05s, 0.1s, 0.5s, 1.0s`), позволяя агрегировать квантили `p95` и `p99` со всех реплик сервиса.
- **`Summary`** — считает квантили прямо на клиенте (сложнее агрегировать между репликами).

> **Смертельная ошибка мониторинга — High Cardinality (Высокая кардинальность меток)**: никогда не передавайте в метки (`labels`) Prometheus `user_id`, `email`, `order_id` или сырой URL `/users/94812` вместо шаблона маршрута `/users/{id}`! Каждая уникальная комбинация меток создаёт новый временной ряд в RAM сервера Prometheus, что вызывает взрыв памяти и падение системы мониторинга.

---

## Проверки жизнеспособности в Kubernetes: `Liveness` vs `Readiness` Probes

Оркестратор контейнеров (Kubernetes) и балансировщик нагрузки (Nginx / Envoy) постоянно опрашивают два разных диагностических эндпоинта вашего бэкенда:

| Тип проверки | Эндпоинт | Что проверяет | Что делает оркестратор при ошибке (`503`) |
| :--- | :--- | :--- | :--- |
| **Liveness Probe** (Жив ли процесс?) | `GET /health/live` | Только то, что сам Python-процесс и его Event Loop не зависли в нативном дедлоке (возвращает `{"status": "alive"}` **без похода в БД!**) | **Убивает и перезапускает контейнер (`Restart Pod`)** |
| **Readiness Probe** (Готов ли принимать трафик?) | `GET /health/ready` | Проверяет доступность критических зависимостей: `SELECT 1` в PostgreSQL и `PING` в Redis с коротким таймаутом | **Временно убирает реплику из балансировщика трафика**, НЕ перезапуская контейнер |

**Почему категорически нельзя проверять базу данных внутри `Liveness Probe`**: если PostgreSQL моргнёт на 5 секунд или перегрузится, все 20 подов вашего бэкенда вернут `500` на `/health/live`, и Kubernetes одновременно **убьёт и отправит в рестарт весь ваш кластер**, устроив полный даунтайм и лавину переподключений при старте!

> **Junior vs Senior**:
> - **Junior**: Пишет неструктурированные `print()` в консоль без `request_id`, передаёт `user_id` в метки Prometheus (вызывая взрыв кардинальности) и проверяет подключение к БД внутри `Liveness Probe`, провоцируя каскадный рестарт всех подов при малейшей задержке СУБД.
> - **Senior**: Настраивает структурные JSON-логи со сквозным `Correlation ID` через `contextvars.ContextVar`, собирает RED-метрики в Prometheus по шаблонам маршрутов (`/users/{id}`) и чётко разделяет лёгкую проверку процесса (`Liveness`) и проверку готовности зависимостей БД/Redis (`Readiness`).
"""
    ),
}

for cid, (ukey, fn, content) in NEW_K_NOTES.items():
    target_ukey = UNIT_LEGACY_TO_MOD3.get(ukey, ukey)
    notes_dir = os.path.join(BACKEND_DIR, BACKEND_UNITS[target_ukey], '📚 Конспекты')
    for old_fn in os.listdir(notes_dir):
        if old_fn.startswith(cid + '.') and old_fn != fn:
            os.remove(os.path.join(notes_dir, old_fn))
    dest = os.path.join(notes_dir, fn)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

for cid, (ukey, fn, content) in ENRICHED_BACKEND_NOTES.items():
    target_ukey = UNIT_LEGACY_TO_MOD3.get(ukey, ukey)
    notes_dir = os.path.join(BACKEND_DIR, BACKEND_UNITS[target_ukey], '📚 Конспекты')
    for old_fn in os.listdir(notes_dir):
        if old_fn.startswith(cid + '.') and old_fn != fn:
            os.remove(os.path.join(notes_dir, old_fn))
    dest = os.path.join(notes_dir, fn)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

print(f"Wrote {len(NEW_K_NOTES)} base new notes + {len(ENRICHED_BACKEND_NOTES)} enriched/new Backend notes into 03 · ⚙️ Backend")

# ─── WRITE 8 NEW BACKEND FLASHCARD DECKS (Ф-272 .. Ф-279) ─────────────────

NEW_F_DECKS = {
    'Ф-272': (
        '2.5',
        'Ф-272. Промышленный FastAPI_ Lifespan, Middleware, Exception Handlers и BackgroundTasks.md',
        [
            ("Зачем в FastAPI используют асинхронный контекстный менеджер `lifespan` вместо создания клиентов БД и Redis глобально или внутри эндпоинта?",
             "Он инициализирует тяжёлые ресурсы (пулы БД, Redis, `httpx.AsyncClient`) один раз перед приёмом трафика (до `yield`) и гарантированно закрывает их при Graceful Shutdown (после `yield`)"),
            ("В каком порядке выполняются слои Middleware в FastAPI/Starlette для входящего запроса и исходящего ответа?",
             "По принципу «луковицы» (Onion Model): входящий запрос проходит слои снаружи внутрь (первым выполняется Middleware, добавленный последним через `app.add_middleware`), а ответ идёт в обратном порядке"),
            ("Почему в высоконагруженных ASGI-сервисах чистый ASGI Middleware (`async def __call__(self, scope, receive, send)`) предпочтительнее `@app.middleware('http')`?",
             "`BaseHTTPMiddleware` создаёт дополнительные накладные расходы, буферизует поток ответа и может конфликтовать с `contextvars` и потоковой передачей (`StreamingResponse`)"),
            ("Почему выбрасывать `fastapi.HTTPException` напрямую из функций сервисного слоя (`services/`) или репозиториев считается архитектурной ошибкой?",
             "Это жёстко привязывает бизнес-логику к HTTP-протоколу и мешает вызывать сервис из воркера Celery, CLI-команды или другого транспорта"),
            ("Как правильно транслировать доменные ошибки бизнес-логики в HTTP-ответы в FastAPI?",
             "Выбрасывать в сервисах чистые доменные исключения Python и перехватывать их на уровне транспортного слоя через `@app.exception_handler(DomainError)` с возвратом структуры по RFC 7807"),
            ("Чем встроенный `BackgroundTasks` в FastAPI принципиально отличается от очереди задач `Celery` или `arq`?",
             "`BackgroundTasks` выполняется в памяти того же процесса `uvicorn` без сохранения в брокере: при падении или рестарте контейнера задача бесследно теряется и не имеет механизма ретраев"),
            ("Почему в задачу `BackgroundTasks` нельзя передавать сессию базы данных `db: AsyncSession = Depends(get_db)`, открытую для обработки HTTP-запроса?",
             "Фоновая задача стартует после отправки ответа клиенту, когда блок `yield` зависимости `get_db` уже завершился и закрыл сессию; фоновая задача должна открывать свою сессию через фабрику"),
            ("Как сервер `uvicorn` осуществляет Graceful Shutdown при получении сигнала `SIGTERM` от Docker или Kubernetes?",
             "Перестаёт принимать новые соединения, дожидается завершения текущих активных запросов в пределах таймаута и затем выполняет секцию `finally` в `lifespan`"),
            ("Для чего в Pydantic-схемах ответа и декораторе роутера используется `response_model` отдельно от входной схемы `CreateSchema`?",
             "Чтобы гарантированно отфильтровать чувствительные поля (например, `password_hash`, внутренние флаги) и провалидировать контракт исходящего ответа"),
            ("Что произойдёт в FastAPI, если объявить эндпоинт как `async def`, но внутри него вызвать синхронный блокирующий `requests.get()` или `time.sleep()`?",
             "Блокирующий вызов заморозит единственный поток Event Loop всего воркера, и все остальные конкурентные запросы на этом воркере перестанут обрабатываться до завершения вызова"),
        ]
    ),

    'Ф-273': (
        '2.8',
        'Ф-273. Слоистая архитектура бэкенда_ Service Layer, Repository и Unit of Work.md',
        [
            ("В чём заключается антипаттерн «Толстый роутер» (Fat Controller / Fat View) в веб-разработке?",
             "В смешивании внутри функции HTTP-эндпоинта разбора параметров запроса, бизнес-логики, прямых SQL-запросов к БД и вызовов внешних сервисов"),
            ("За что отвечает транспортный слой (Router / View) в чистой слоистой архитектуре бэкенда?",
             "Только за приём HTTP-запроса, валидацию входных DTO-схем, вызов метода сервисного слоя и упаковку результата в HTTP-ответ с нужным статус-кодом"),
            ("Какую задачу решает паттерн Repository (Репозиторий) в слое доступа к данным?",
             "Абстрагирует бизнес-логику от конкретной ORM и СУБД, предоставляя сервису интерфейс коллекции доменных объектов (`get`, `add`, `list`)"),
            ("Как паттерн Repository ускоряет выполнение модульных тестов бизнес-логики?",
             "Позволяет подменить реальный `SqlAlchemyRepository` на легковесный `InMemoryRepository` (на базе `dict`) и тестировать сервисный слой за миллисекунды без запуска СУБД"),
            ("Почему методы репозитория (`repo.add()`, `repo.update()`) не должны самостоятельно вызывать `session.commit()`?",
             "Потому что один бизнес-сценарий может изменять данные сразу в нескольких репозиториях, и преждевременный `commit()` нарушит атомарность общей транзакции"),
            ("Какую проблему решает паттерн Unit of Work (Единица работы)?",
             "Координирует изменения в нескольких репозиториях в рамках единой атомарной транзакции БД, гарантируя общий `commit()` при успехе или полный `rollback()` при любой ошибке"),
            ("Почему в Python паттерн Unit of Work реализуют через протокол контекстного менеджера (`__enter__`/`__exit__` или `__aenter__`/`__aexit__`)?",
             "Метод `__aexit__` гарантированно перехватывает любое возникшее в блоке `async with uow:` исключение и автоматически вызывает `await uow.rollback()` и закрытие сессии"),
            ("В чём разница между `session.flush()` и `session.commit()` при работе репозитория внутри Unit of Work?",
             "`flush()` отправляет SQL-запросы в БД внутри открытой транзакции (позволяя получить сгенерированный `id`), но изменения ещё можно откатить; `commit()` необратимо фиксирует транзакцию"),
            ("Зачем разделять модели ORM (`SQLAlchemy Model`) и схемы API (`Pydantic DTO`)?",
             "Модель ORM отражает структуру таблиц хранения в БД, а схема DTO задаёт внешний контракт API; их смешивание приводит к утечке внутренних полей БД и ошибкам ленивой подгрузки (`DetachedInstanceError`)"),
            ("Как направлен вектор зависимостей между слоями в Чистой (Луковой / Гексагональной) архитектуре?",
             "Все зависимости направлены строго внутрь к бизнес-ядру: инфраструктура (БД, ORM) и транспорт (FastAPI) зависят от абстракций бизнес-логики, а домен не знает ни о веб-фреймворке, ни о SQL"),
        ]
    ),

    'Ф-274': (
        '2.8',
        'Ф-274. Транзакции на бэкенде, Connection Pool и блокировки (SELECT FOR UPDATE vs Optimistic Lock).md',
        [
            ("Почему бэкенд использует пул соединений (Connection Pool) вместо открытия нового подключения к PostgreSQL на каждый HTTP-запрос?",
             "Создание нового TCP/TLS-соединения и серверного процесса `postgres` занимает 15–30 мс и быстро исчерпывает лимит `max_connections` СУБД под нагрузкой"),
            ("Что задают параметры `pool_size` и `max_overflow` в `QueuePool` SQLAlchemy?",
             "`pool_size` определяет число постоянно удерживаемых соединений в пуле, а `max_overflow` — сколько дополнительных временных соединений пул может открыть при пике нагрузки"),
            ("Для чего в настройках движка SQLAlchemy включают флаг `pool_pre_ping=True`?",
             "Перед выдачей соединения из пула выполняется быстрая проверка (`SELECT 1`), чтобы автоматически переоткрыть соединение, если СУБД или сеть разорвали его по таймауту простоя"),
            ("Почему нельзя делать внешние сетевые вызовы (`httpx.post`) внутри открытой транзакции базы данных?",
             "Медленный внешний HTTP-запрос удерживает соединение из пула БД и строковые блокировки, что быстро приводит к исчерпанию `Connection Pool` и остановке всего сервиса"),
            ("В чём суть аномалии Lost Update (Потерянное обновление) при параллельном списании баланса в уровне изоляции `READ COMMITTED`?",
             "Две транзакции одновременно читают одно и то же начальное значение баланса в память Python, вычисляют остаток и перезаписывают результат друг друга"),
            ("Как работает пессимистичная блокировка `SELECT ... FOR UPDATE` в реляционной БД?",
             "Накладывает эксклюзивную строковую блокировку (`Row-Level Lock`) на выбранные записи до конца транзакции, заставляя другие транзакции ждать освобождения строки"),
            ("Чем отличаются модификаторы `FOR UPDATE NOWAIT` и `FOR UPDATE SKIP LOCKED` в PostgreSQL?",
             "`NOWAIT` мгновенно выбрасывает ошибку, если строка уже заблокирована, а `SKIP LOCKED` пропускает заблокированные строки и выбирает только свободные (идеально для разбора очередей)"),
            ("Как устроена оптимистичная блокировка (Optimistic Locking) без удержания блокировок в БД?",
             "В таблицу добавляется поле `version`; при обновлении проверяется `WHERE id = :id AND version = :read_version` с инкрементом версии — если `rowcount == 0`, значит данные изменил другой поток"),
            ("Когда оптимистичная блокировка эффективнее пессимистичной `SELECT FOR UPDATE`, а когда наоборот?",
             "Оптимистичная эффективнее при редких конфликтах и преобладании чтений; пессимистичная лучше при высокой конкуренции за одни и те же строки (например, горячий счёт), чтобы не делать десятки холостых ретраев"),
            ("Какое простое правило гарантированно предотвращает возникновение Deadlock при блокировке двух счетов в операции перевода?",
             "Всегда захватывать блокировки `SELECT ... FOR UPDATE` в строго детерминированном порядке, например по возрастанию первичного ключа (`ORDER BY id ASC`)"),
        ]
    ),

    'Ф-275': (
        '2.8',
        'Ф-275. Кэширование в бэкенде_ Redis, Cache-Aside, Cache Stampede и Distributed Locks.md',
        [
            ("Почему декоратор `@functools.lru_cache` не подходит для кэширования изменяемых бизнес-данных в продакшене с несколькими воркерами?",
             "Он хранит данные локально в RAM каждого отдельного процесса `uvicorn`/`gunicorn`, из-за чего при обновлении данных на одном воркере остальные продолжают отдавать устаревший кэш"),
            ("Как работает паттерн ленивого кэширования `Cache-Aside`?",
             "Приложение сначала ищет данные в Redis; при промахе (`Cache Miss`) читает их из БД, записывает в Redis с заданным `TTL` и возвращает клиенту, а при изменении данных в БД удаляет ключ из кэша"),
            ("Почему при обновлении записи в БД надёжнее удалить ключ из Redis (`DEL key`), чем перезаписывать его новым значением (`SET key`)?",
             "При двух параллельных `UPDATE` перезапись кэша может выполниться в обратном порядке (гонка потоков) и оставить в кэше устаревшее значение до конца TTL"),
            ("Что такое эффект `Cache Stampede` (Thundering Herd / Эффект стада) при истечении срока жизни популярного ключа?",
             "Ситуация, когда в момент истечения `TTL` тяжеловесного ключа сотни параллельных запросов одновременно получают `Cache Miss` и лавинообразно атакуют базу данных одинаковыми запросами"),
            ("Какими способами на бэкенде защищаются от `Cache Stampede`?",
             "Захватом распределённой блокировки (Distributed Lock) на пересчёт ключа одним воркером, отдачей слегка устаревшего значения (`Stale-While-Revalidate`) или ранним вероятностным обновлением"),
            ("Зачем к базовому времени жизни ключей в кэше добавляют случайное смещение — `TTL Jitter` (`ttl + random.randint(-60, 60)`)?",
             "Чтобы тысячи ключей, загруженных в кэш одновременно при старте или пакетном прогреве, не протухли в одну и ту же секунду и не вызвали пиковый удар по БД"),
            ("Как в Redis атомарно захватывается распределённая блокировка (Distributed Lock) на одном узле?",
             "Командой `SET lock_key unique_worker_token NX PX 10000`, которая создаёт ключ только при его отсутствии (`NX`) и задаёт автоудаление по таймауту (`PX`)"),
            ("Почему при снятии распределённой блокировки в Redis опасно вызывать просто `DEL lock_key` без проверки токена владельца?",
             "Если первый воркер завис дольше `TTL`, его блокировка уже истекла и досталась второму воркеру; простой `DEL` от первого воркера удалит чужую активную блокировку"),
            ("Как безопасно освободить распределённую блокировку в Redis?",
             "Выполнить атомарный Lua-скрипт, который проверяет `redis.call('get', KEYS[1]) == ARGV[1]` (совпадение уникального токена воркера) и только в этом случае вызывает `del`"),
            ("Что такое кэширование отрицательных результатов (Negative Caching) и от чего оно защищает?",
             "Кэширование факта отсутствия записи в БД (например, маркер `'NULL'` с коротким TTL 30–60 секунд), что защищает базу от повторных запросов по несуществующим ID"),
        ]
    ),

    'Ф-276': (
        '2.9',
        'Ф-276. Надёжные интеграции_ Circuit Breaker, Exponential Backoff с Jitter и Webhooks.md',
        [
            ("Почему при сбое внешнего API опасно делать мгновенные повторные запросы (Retries) в цикле с фиксированной паузой?",
             "Это вызывает Retry Storm (шторм повторных запросов): все воркеры синхронно умножают нагрузку на падающий сервис и блокируют собственные потоки"),
            ("В чём суть алгоритма `Exponential Backoff + Full Jitter` при повторных запросах?",
             "Максимальное окно ожидания удваивается с каждой попыткой ($2^n$), а реальная пауза выбирается случайно внутри этого окна, что рассинхронизирует воркеры"),
            ("При каких HTTP-статусах от внешнего сервиса имеет смысл делать автоматический Retry, а при каких — категорически нет?",
             "Ретраи делают при сетевых таймаутах, `429 Too Many Requests`, `502`, `503`, `504`; при клиентских ошибках `400`, `401`, `403`, `404`, `422` повторный запрос бессмысленен"),
            ("Какие три состояния имеет паттерн `Circuit Breaker` (Автоматический выключатель)?",
             "`CLOSED` (штатный пропуск запросов), `OPEN` (мгновенный отказ без обращения к сети после превышения порога ошибок) и `HALF_OPEN` (пропуск пробного запроса после таймаута)"),
            ("Какую главную пользу даёт перевод `Circuit Breaker` в состояние `OPEN` при падении внешнего платёжного или СМС-шлюза?",
             "Запросы завершаются мгновенно (`Fail-Fast` за 0 мс) вместо ожидания сетевых таймаутов, сохраняя пулы потоков и соединений вашего бэкенда живыми"),
            ("Как защитить эндпоинт приёма входящих вебхуков (`POST /webhooks/payment`) от поддельных запросов злоумышленников?",
             "Проверять криптографическую подпись `HMAC-SHA256`, вычисленную от сырых байтов тела запроса (`raw_body`) и временной метки с помощью общего секретного ключа"),
            ("Почему для сверки HMAC-подписи вебхука в Python необходимо использовать `hmac.compare_digest(a, b)` вместо оператора `==`?",
             "Оператор `==` выходит на первом несовпавшем байте, позволяя злоумышленнику угадать подпись побайтово по микросекундным разницам времени ответа (Timing Attack), а `compare_digest` работает за константное время"),
            ("Как защитить обработчик вебхуков от атаки повторного воспроизведения (`Replay Attack`), если злоумышленник перехватил валидный запрос?",
             "Включать `timestamp` в подписываемую строку, отклонять запросы старше допустимого окна (например, > 5 минут) и сохранять `event_id` обработанных вебхуков в БД/Redis"),
            ("Почему обработчик входящего вебхука должен быть строго идемпотентным?",
             "Внешние провайдеры (Stripe, ЮKassa, GitHub) используют доставку `at-least-once` и при любом таймауте сети отправят один и тот же вебхук повторно"),
            ("Как правильно организовать архитектуру приёма тяжёлых вебхуков на бэкенде?",
             "Быстро проверить HMAC-подпись, сохранить событие в БД/очередь и сразу вернуть провайдеру `200 OK`, а саму бизнес-обработку выполнить асинхронно в фоновом воркере"),
        ]
    ),

    'Ф-277': (
        '2.9',
        'Ф-277. Фоновые задачи и брокеры сообщений_ Celery, RabbitMQ, Kafka, Outbox и DLQ.md',
        [
            ("Какие задачи в бэкенде обязательно выносят из HTTP-обработчика в фоновые воркеры (`Celery` / `TaskIQ` / `arq`)?",
             "Генерацию отчётов и обработку медиафайлов, рассылку email/push-уведомлений, долгие интеграции со сторонними API и периодические задачи по расписанию"),
            ("Что означает гарантия доставки `At-least-once` в очередях сообщений и какое требование она накладывает на код воркера?",
             "Брокер гарантирует, что сообщение будет доставлено минимум один раз, но при сетевом сбое возможна повторная доставка — поэтому код воркера обязан быть идемпотентным"),
            ("За что отвечает настройка `task_acks_late = True` в Celery?",
             "Воркер отправляет подтверждение `ACK` брокеру только после полного выполнения задачи, а не в момент её получения, предотвращая потерю задачи при внезапном падении воркера"),
            ("Что такое `Dead Letter Queue (DLQ)` в архитектуре брокеров сообщений?",
             "Специальная карантинная очередь, куда брокер перенаправляет «отравленные» сообщения, которые не удалось обработать после исчерпания всех попыток `max_retries`"),
            ("В чём ключевое архитектурное отличие Apache Kafka от классического брокера очередей RabbitMQ?",
             "RabbitMQ удаляет сообщение из очереди сразу после `ACK` от получателя, а Kafka хранит события в неизменяемом дисковом логе партиций, позволяя разным `Consumer Groups` независимо читать и перематывать историю"),
            ("Как обеспечивается строгий порядок обработки событий в Apache Kafka?",
             "Порядок гарантируется только внутри одной партиции топика; чтобы все события одного заказа или пользователя шли строго по порядку, в качестве ключа партиционирования передают `order_id` или `user_id`"),
            ("В чём суть проблемы двойной записи (`Dual Write Problem`) при сохранении сущности в БД и отправке события в брокер?",
             "БД и брокер сообщений не имеют общей транзакции: если после `db.commit()` сервер упадёт перед отправкой в Kafka/RabbitMQ, система останется в неконсистентном состоянии"),
            ("Как паттерн `Transactional Outbox` решает проблему двойной записи?",
             "Событие для брокера записывается в специальную таблицу `outbox` той же БД в одной атомарной транзакции с бизнес-данными, а отдельный воркер-ретранслятор гарантированно доставляет записи из `outbox` в брокер"),
            ("Для чего в экосистеме Celery используется процесс `Celery Beat`?",
             "`Celery Beat` — это планировщик периодических задач (распределённый аналог `cron`), который по расписанию отправляет задачи в очередь для выполнения обычными воркерами"),
            ("Почему в качестве аргументов задачи `celery_task.delay(...)` следует передавать примитивный `id` записи, а не сериализованный объект ORM-модели?",
             "За время нахождения задачи в очереди состояние объекта в БД может измениться; воркер должен по `id` загрузить свежую актуальную версию строки прямо перед выполнением"),
        ]
    ),

    'Ф-278': (
        '2.10',
        'Ф-278. Работа с файлами на бэкенде_ Streaming, Magic Bytes и облачные хранилища S3.md',
        [
            ("Почему вызов `await upload_file.read()` без аргументов в эндпоинте загрузки файлов опасен для продакшен-сервера?",
             "Он целиком загружает весь файл в оперативную память (RAM), что при нескольких одновременных загрузках крупных файлов вызывает `MemoryError` или убийство контейнера `OOM Killer`"),
            ("Как реализовать подсчёт хеша или пересылку загружаемого файла с константным потреблением памяти $O(1)$?",
             "Читать поток фиксированными чанками в цикле (`while chunk := await file.read(65536): ...`), обрабатывая и освобождая каждый блок по мере поступления"),
            ("Для чего в FastAPI используется класс `StreamingResponse`?",
             "Для потоковой отдачи клиенту больших файлов или генерируемых на лету CSV/архивов через итератор/генератор без формирования всего тела ответа в памяти"),
            ("Почему при валидации загружаемых файлов нельзя доверять заголовку `Content-Type` и расширению из `file.filename`?",
             "Эти значения формируются на клиенте и легко подделываются злоумышленником; реальный тип файла необходимо проверять по сигнатуре первых байтов (**Magic Bytes**)"),
            ("В чём заключается уязвимость `Path Traversal` при сохранении файла и как её полностью исключить?",
             "Использование вредоносного имени вроде `../../app/main.py` позволяет перезаписать системные файлы; для защиты файлам при сохранении всегда присваивают сгенерированный `UUID`"),
            ("Почему пользовательские файлы нельзя хранить в локальной папке внутри Docker-контейнера бэкенда?",
             "Контейнеры эфемерны (файлы пропадут при пересборке/рестарте) и при горизонтальном масштабировании файл, сохранённый на одной реплике, будет недоступен остальным репликам"),
            ("Как работает архитектурный паттерн `Presigned URL` при загрузке и скачивании файлов из S3?",
             "Бэкенд проверяет права и генерирует временную криптографически подписанную ссылку в S3, по которой клиент сам загружает или скачивает файл напрямую в хранилище, не нагружая Python-воркеры"),
            ("Что такое `S3 Multipart Upload` и когда он применяется?",
             "Механизм загрузки больших файлов (от 100 МБ до терабайт) путём разбиения на независимые части, которые загружаются параллельно и позволяют докачать только сбойный фрагмент при обрыве сети"),
            ("Зачем при отдаче пользовательских файлов выставляют заголовки `Content-Disposition: attachment` и `X-Content-Type-Options: nosniff`?",
             "Чтобы запретить браузеру автоматически угадывать MIME-тип и исполнять загруженный пользователем файл как HTML/JavaScript (защита от Stored XSS)"),
            ("Какую роль играет `SpooledTemporaryFile` внутри `UploadFile` в FastAPI/Starlette?",
             "Небольшие файлы (до порогового размера ~1 МБ) хранятся в быстрой оперативной памяти, а при превышении порога автоматически сбрасываются во временный файл на диск"),
        ]
    ),

    'Ф-279': (
        '2.10',
        'Ф-279. Конфигурация 12-Factor App и Наблюдаемость (JSON-логи, Correlation ID, Prometheus, Health Checks).md',
        [
            ("В чём заключается 3-й принцип методологии `The Twelve-Factor App` относительно конфигурации сервиса?",
             "Вся конфигурация, меняющаяся между окружениями (`dev`, `stage`, `prod`), должна храниться в переменных окружения и быть строго отделена от исходного кода"),
            ("В чём главное преимущество использования `pydantic-settings` (`BaseSettings`) по сравнению с разрозненными вызовами `os.getenv()`?",
             "Принцип `Fail-Fast`: все переменные окружения собираются в единую схему, приводятся к строгим типам и валидируются в момент запуска приложения, мгновенно останавливая старт при ошибке"),
            ("Зачем для хранения паролей и API-ключей в моделях настроек используют тип `SecretStr` из Pydantic?",
             "`SecretStr` скрывает секретное значение маской `'**********'` при любом логировании, выводе `repr()` или отправке локальных переменных в трейсбек ошибок"),
            ("Почему в продакшене логи бэкенда пишут в структурированном JSON-формате в `stdout`, а не обычным текстом в локальные файлы?",
             "JSON-логи из `stdout` автоматически собираются агентами оркестратора и индексируются по полям (`level`, `request_id`, `user_id`, `duration_ms`) в системах вроде ELK или Grafana Loki"),
            ("Зачем нужен `Correlation ID` (`X-Request-ID`) и почему в асинхронном Python его хранят в `contextvars.ContextVar`?",
             "Он связывает все логи одного запроса сквозь слои и микросервисы, а `ContextVar` изолирует контекст каждой корутины внутри одного потока Event Loop"),
            ("Что означают три метрики метода `RED` для мониторинга веб-сервисов?",
             "`Rate` (число запросов в секунду), `Errors` (число ошибочных ответов в секунду) и `Duration` (распределение времени ответа — квантили `p95`, `p99`)"),
            ("Чем отличаются типы метрик `Counter`, `Gauge` и `Histogram` в Prometheus?",
             "`Counter` только монотонно растёт (число запросов), `Gauge` может расти и падать (активные соединения), а `Histogram` раскладывает замеры по корзинам (`buckets`) для расчёта квантилей `p95`/`p99`"),
            ("Почему в метки (`labels`) метрик Prometheus категорически нельзя передавать `user_id` или уникальные ID заказов?",
             "Это вызывает взрыв кардинальности (`High Cardinality`): каждая уникальная комбинация меток создаёт новый временной ряд в памяти Prometheus и приводит к его падению по OOM"),
            ("В чём принципиальная разница между `Liveness Probe` и `Readiness Probe` в Kubernetes?",
             "Падение `Liveness Probe` означает зависание процесса и ведёт к **перезапуску контейнера**, а падение `Readiness Probe` лишь **временно отключает подачу трафика** на эту реплику"),
            ("Почему проверка подключения к базе данных (`SELECT 1`) должна находиться в `Readiness Probe`, но ни в коем случае не в `Liveness Probe`?",
             "Если БД кратковременно станет недоступна, проверка внутри `Liveness Probe` заставит оркестратор одновременно убить и перезапустить все живые контейнеры бэкенда (каскадный даунтайм)"),
        ]
    ),

    'Ф-280': (
        '2.5',
        'Ф-280. Асинхронное ядро FastAPI_ Event Loop, Threadpool и неблокирующий I_O.md',
        [
            ("Как FastAPI исполняет path-операции, объявленные через `async def`, в отличие от обычных `def`?",
             "Корутины `async def` выполняются напрямую в главном потоке Event Loop (неблокирующе), а синхронные функции `def` автоматически выносятся в внешний пул потоков `anyio.to_thread.run_sync`"),
            ("Почему вызов синхронного драйвера `psycopg2` или `requests.get()` внутри `async def` эндпоинта критически опасен для производительности FastAPI?",
             "Синхронный блокирующий системный вызов замораживает единственный поток Event Loop, останавливая обработку всех остальных конкурентных запросов на этом воркере"),
            ("В каком случае в FastAPI-приложении правильнее объявить эндпоинт через обычный `def`, а не `async def`?",
             "Когда внутри обработчика используется синхронная библиотека без `await` (например, классический синхронный SQLAlchemy Session или `boto3`), чтобы FastAPI безопасно выполнил её в ThreadPool"),
            ("Какой лимит потоков по умолчанию используется в `anyio` ThreadPool внутри Starlette/FastAPI для синхронных `def`-эндпоинтов?",
             "По умолчанию 40 токенов (`CapacityLimiter(40)`); если все 40 потоков заняты долгими синхронными запросами, новые `def`-запросы встают в очередь ожидания"),
            ("Как выполнить тяжёлую синхронную функцию внутри `async def` эндпоинта, не блокируя Event Loop?",
             "Выгрузить её в пул потоков через `await asyncio.to_thread(sync_fn, *args)` или `await run_in_threadpool(sync_fn, *args)` из `starlette.concurrency`"),
            ("Почему для CPU-bound задач (генерация PDF, обработка изображений, ML-инференс) недостаточно даже `run_in_threadpool` в Python?",
             "Из-за GIL потоки внутри одного процесса Python не могут параллельно исполнять байткод на нескольких ядрах CPU и всё равно вытесняют поток Event Loop; нужен `ProcessPoolExecutor` или фоновый воркер Celery"),
            ("Что происходит с активными HTTP-соединениями при запуске `uvicorn` с флагом `--workers 4`?",
             "Мастер-процесс поднимает 4 независимых процесса ОС, каждый со своим собственным Python-интерпретатором, памятью и независимым циклом событий (`uvloop`)"),
            ("Что такое `uvloop` и почему он используется в продакшен-сборках `uvicorn[standard]`?",
             "Высокопроизводительная реализация цикла событий `asyncio` поверх C-библиотеки `libuv` (написанная на Cython), ускоряющая сетевой ввод-вывод в 2–4 раза по сравнению со стандартным Event Loop"),
            ("Почему создание нового `httpx.AsyncClient()` внутри каждого `async def` запроса является антипаттерном?",
             "На каждый запрос заново создаётся пул сокетов и выполняется полный TCP + TLS Handshake со сторонним сервером; клиент нужно создавать один раз в `lifespan` и переиспользовать"),
            ("Как в FastAPI параллельно выполнить три независимых асинхронных запроса к микросервисам внутри одного эндпоинта?",
             "Использовать `await asyncio.gather(req1(), req2(), req3())` или структурную конкурентность `async with asyncio.TaskGroup() as tg: ...` (Python 3.11+)"),
            ("В чём преимущество `asyncio.TaskGroup` (Python 3.11+) перед `asyncio.gather` при параллельных запросах в бэкенде?",
             "При падении одной из дочерних задач `TaskGroup` автоматически и гарантированно отменяет (`cancel()`) все остальные задачи группы, предотвращая утечку «осиротевших» корутин"),
            ("Как работает зависимость `Depends` в FastAPI, если сама функция зависимости объявлена как синхронный генератор `def get_db(): yield db`?",
             "Как вход в генератор (до `yield`), так и блок очистки (после `yield` / `finally`) автоматически выполняются в пуле потоков `run_in_threadpool`, не блокируя Event Loop"),
            ("Что произойдёт, если клиент оборвёт соединение (закроет вкладку) во время долгого `await` внутри эндпоинта FastAPI/Starlette?",
             "При попытке чтения/записи или проверке `await request.is_disconnected()` сервер обнаружит закрытие канала, а корутина может получить `asyncio.CancelledError`"),
            ("Почему при перехвате всех ошибок через `except Exception:` важно не проглотить `asyncio.CancelledError`?",
             "Хотя в Python 3.8+ `CancelledError` наследуется от `BaseException`, при использовании `try ... finally` или `BaseException` его перехват без повторного `raise` сломает корректную отмену задач и Graceful Shutdown"),
            ("Как в асинхронном эндпоинте FastAPI ограничить максимальное время ожидания ответа от внешней БД или API?",
             "Обернуть вызов в контекстный менеджер `async with asyncio.timeout(2.5): await fetch_data()` (Python 3.11+) или `await asyncio.wait_for(fetch_data(), timeout=2.5)`"),
            ("Почему в асинхронном SQLAlchemy (`AsyncSession`) запрещено использовать один и тот же экземпляр `AsyncSession` параллельно в нескольких задачах `asyncio.gather()`?",
             "`AsyncSession` не является корутино-безопасной (single-flight per connection): параллельные запросы на одной сессии вызовут `InvalidRequestError: This session is provisioning a new connection`"),
            ("Как правильно организовать кэширование контекста текущего запроса (например, `request_id` или `tenant_id`) в асинхронном приложении без явной передачи аргументов?",
             "Использовать `contextvars.ContextVar`, значение которой автоматически наследуется дочерними корутинами в рамках одного запроса и полностью изолировано от соседних запросов в Event Loop"),
        ]
    ),

    'Ф-281': (
        '2.7',
        'Ф-281. Архитектура сессий, Redis Session Store и API-ключей.md',
        [
            ("В чём фундаментальное архитектурное различие между `Stateful` (сессионной) и `Stateless` (токенной) аутентификацией?",
             "При `Stateful` сервер хранит состояние активной сессии в БД/Redis и сверяет `session_id` при каждом запросе, а при `Stateless` все данные пользователя и срок действия зашиты в криптографически подписанный токен"),
            ("Почему хранение серверных сессий в оперативной памяти процесса Python ломается при запуске нескольких воркеров `gunicorn`/`uvicorn`?",
             "Память процессов изолирована: если следующий запрос пользователя попадёт через балансировщик на другой воркер, тот не найдёт `session_id` и разлогинит пользователя"),
            ("Почему Redis является стандартом де-факто для централизованного хранилища серверных сессий (`Session Store`)?",
             "Redis хранит данные в RAM (задержка < 1 мс), разделяется всеми репликами бэкенда и поддерживает нативное автоудаление истёкших сессий через `TTL` (`EXPIRE`)"),
            ("Как реализовать скользящее продление сессии (`Sliding Expiration`) в Redis при активности пользователя?",
             "При каждом успешном запросе (или не чаще раза в N минут) обновлять время жизни ключа сессии командой `EXPIRE session:<id> 86400`"),
            ("В чём главное преимущество серверных сессий в Redis перед Stateless JWT при требовании мгновенного бана пользователя или кнопки «Выйти со всех устройств»?",
             "Удаление ключей сессии пользователя в Redis мгновенно закрывает доступ на всех сервисах, тогда как выпущенный Stateless JWT остаётся валидным до истечения своего `exp`"),
            ("Как организовать хранение сессий в Redis так, чтобы можно было за $O(1)$ показать пользователю список всех его активных устройств и завершить любое из них?",
             "Помимо ключей `session:<sid>`, хранить для каждого пользователя множество `user_sessions:<uid>` (Redis `SET` или `HASH`) со списком активных `sid` и метаданными устройства (IP, User-Agent)"),
            ("Что такое атака фиксации сессии (`Session Fixation`) и как бэкенд обязан от неё защищаться?",
             "Злоумышленник заранее подсовывает жертве известный `session_id` до входа; для защиты сервер обязан **перегенерировать новый `session_id`** сразу после успешного ввода логина и пароля"),
            ("Какой минимальный размер энтропии должен иметь идентификатор сессии `session_id` и чем его генерируют в Python?",
             "Не менее 128–256 бит криптографической случайности, генерируемой через `secrets.token_urlsafe(32)` (модуль `random` использовать категорически запрещено)"),
            ("Какие три атрибута безопасности обязательно выставляют для сессионной Cookie в браузере?",
             "`HttpOnly` (невидимость для `document.cookie` / защита от XSS), `Secure` (передача только по HTTPS) и `SameSite=Lax` или `Strict` (защита от CSRF)"),
            ("Что такое гибридная архитектура `Phantom Token` / `Reference Token` на API Gateway?",
             "Внешний клиент держит непрозрачный `session_id` (Opaque Token), а API Gateway при входе проверяет его в Redis и пробрасывает внутрь микросервисной сети короткоживущий подписанный JWT"),
            ("Чем машинная аутентификация по `API-ключам` отличается по назначению от пользовательских сессий и JWT?",
             "API-ключи предназначены для долгоживущих сервер-серверных интеграций (M2M / внешние разработчики), где нет интерактивного браузерного логина"),
            ("Почему API-ключи, как и пароли, категорически нельзя хранить в базе данных в открытом виде (plaintext)?",
             "При утечке дампа БД злоумышленник мгновенно получит действующие ключи доступа ко всем интеграциям клиентов; в БД хранят только криптографический хеш ключа (`SHA-256` / `HMAC`)"),
            ("Почему для проверки высокоэнтропийного API-ключа (256 бит случайности) достаточно быстрого хеша `SHA-256`, тогда как для паролей нужен медленный `Argon2`/`bcrypt`?",
             "Пароль придумывает человек (низкая энтропия, уязвим к перебору по словарю), а API-ключ из 32 случайных байт имеет $2^{256}$ комбинаций, что делает брутфорс математически невозможным"),
            ("Зачем в промышленных сервисах (Stripe `sk_live_...`, GitHub `ghp_...`) к API-ключам добавляют открытый префикс и короткий идентификатор ключа?",
             "Префикс позволяет сканерам секретов в Git автоматически находить утекшие ключи, а открытый `key_prefix` позволяет быстро найти запись в БД по индексу и показать пользователю, какой именно ключ используется (`sk_live_4f9a...`)"),
            ("Почему полное значение сгенерированного API-ключа показывается пользователю в интерфейсе ровно один раз при создании?",
             "Поскольку сервер сохраняет только необратимый хеш ключа и сразу отбрасывает исходную строку, восстановить и повторно показать полный ключ технически невозможно"),
            ("Как безопасно провести ротацию (`Key Rotation`) API-ключа в продакшен-интеграции без даунтайма (Zero-Downtime)?",
             "Разрешить одновременное существование старого и нового ключа на переходный период (Grace Period), переключить клиент на новый ключ и затем отозвать старый"),
            ("Почему для каждого API-ключа важно настраивать гранулярные области видимости (`Scopes`, например `orders:read`, `payments:write`) и собственный Rate Limit?",
             "Принцип минимальных привилегий (`Least Privilege`): даже если ключ одного скрипта или партнёра утечёт, злоумышленник не сможет выполнить разрушительные операции или положить весь сервис"),
        ]
    ),
}

all_new_f_decks = {}
all_new_f_decks.update(NEW_F_DECKS)
all_new_f_decks.update(NEW_MOD3_F_DECKS)

for fid, (ukey, fn, pairs) in all_new_f_decks.items():
    target_ukey = UNIT_LEGACY_TO_MOD3.get(ukey, ukey)
    cards_dir = os.path.join(BACKEND_DIR, BACKEND_UNITS[target_ukey], '📇 Карточки')
    for old_fn in os.listdir(cards_dir):
        if old_fn.startswith(fid + '.') and old_fn != fn:
            os.remove(os.path.join(cards_dir, old_fn))
    dest = os.path.join(cards_dir, fn)
    lines = [f"{idx}. {q} >> {a}" for idx, (q, a) in enumerate(pairs, 1)]
    with open(dest, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

print(f"Wrote {len(all_new_f_decks)} Backend flashcard decks (Ф-272 .. Ф-285)")

# ─── BUILD ACTUAL FILE stem MAP FOR 00 · 🗺️ Карта Мастерства.md ────────────

id_to_rel_stem = {}
for mod_dir in [WEB_DIR, BACKEND_DIR]:
    for r, d, files in os.walk(mod_dir):
        for fn in files:
            if fn.endswith('.md'):
                m = re.match(r'^([КФ]-\d+)\.', fn)
                if m:
                    cid = m.group(1)
                    rel_p = os.path.relpath(os.path.join(r, fn), BASE).replace('\\', '/')
                    if rel_p.endswith('.md'):
                        rel_p = rel_p[:-3]
                    id_to_rel_stem[cid] = rel_p

# Cross-module decks from Modules 01, 05 (Базы данных) and 06 (Архитектура)
id_to_rel_stem['Ф-075'] = '01 · 🐍 Python/Юнит 1.8 · Конкурентность/📇 Карточки/Ф-075. Async поддержка'
id_to_rel_stem['Ф-098'] = '06 · 🏛️ Архитектура/Юнит 6.6 · Архитектура/📇 Карточки/Ф-098. Архитектура REST vs GraphQL'
id_to_rel_stem['Ф-107'] = '06 · 🏛️ Архитектура/Юнит 6.2 · Слои приложения/📇 Карточки/Ф-107. Архитектура MVC MTV'
id_to_rel_stem['Ф-110'] = '05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-110. ORM Django ORM, модели QuerySet, related_name'
id_to_rel_stem['Ф-111'] = '05 · 🗄️ Базы данных/Юнит 5.4 · Транзакции/📇 Карточки/Ф-111. Оптимизация N+1 проблема'

WEB_CURRICULUM_SPEC = [
    ('2.1', 'Юнит 2.1 · Сетевой фундамент', [
        ('2.1.1', 'Сетевая модель и транспортные протоколы (OSI, TCP vs UDP, 3-way handshake)',
         ['К-062', 'К-063'], ['Ф-258', 'Ф-259'],
         'Разобрать 7 уровней модели OSI, 3-way handshake TCP и отличия потокового TCP от дейтаграммного UDP.'),
        ('2.1.2', 'Система доменных имён и сетевые сокеты (DNS-записи, модуль socket)',
         ['К-064', 'К-065'], ['Ф-260', 'Ф-261'],
         'Написать клиент-сервер обменивающийся сообщениями через низкоуровневые TCP/UDP сокеты и разобрать цепочку DNS-резолвинга.'),
    ]),
    ('2.2', 'Юнит 2.2 · HTTP-протокол и Real-Time', [
        ('2.2.1', 'Семантика HTTP: методы, заголовки и статус-коды (GET, POST, PUT, PATCH, DELETE, 1xx–5xx)',
         ['К-066', 'К-067', 'К-068'], ['Ф-092', 'Ф-093', 'Ф-094'],
         'Отправить и разобрать запросы GET, POST, PUT, PATCH, DELETE со статусами 200, 201, 204, 400, 404, 409, 422, 500.'),
        ('2.2.2', 'Безопасность транспорта и эволюция HTTP (HTTPS, TLS/SSL Handshake, HTTP/1.1 vs HTTP/2, Cookies)',
         ['К-069', 'К-070', 'К-071'], ['Ф-090', 'Ф-091', 'Ф-095'],
         'Разобрать TLS handshake, мультиплексирование потоков в HTTP/2 и атрибуты безопасности Cookie (HttpOnly, Secure, SameSite).'),
        ('2.2.3', 'Двусторонние соединения и серверные шлюзы Python (WebSocket, WSGI vs ASGI)',
         ['К-072', 'К-073'], ['Ф-262', 'Ф-263'],
         'Смоделировать HTTP Upgrade до WebSocket-соединения и сравнить синхронный интерфейс WSGI с событийным ASGI (scope, receive, send).'),
    ]),
    ('2.3', 'Юнит 2.3 · REST API и веб-контракты', [
        ('2.3.1', 'Архитектурные ограничения REST, именование ресурсов и сравнение с GraphQL',
         ['К-074', 'К-075', 'К-076'], ['Ф-098', 'Ф-099', 'Ф-100', 'Ф-126'],
         'Спроектировать канонический RESTful-контракт вложенных ресурсов и сравнить выборку данных с GraphQL.'),
        ('2.3.2', 'Жизненный цикл контракта: Версионирование API, Deprecation/Sunset и OpenAPI/Swagger',
         ['К-077', 'К-078'], ['Ф-101', 'Ф-103', 'Ф-104'],
         'Спроектировать стратегию версионирования API (/api/v1 vs заголовки) и спецификацию OpenAPI 3.1.'),
        ('2.3.3', 'Надёжность веб-контрактов: Идемпотентность (Idempotency-Key), пагинация (Offset vs Cursor) и RFC 7807',
         ['К-080', 'К-225'], ['Ф-265', 'Ф-266'],
         'Реализовать идемпотентный обработчик платежей с Idempotency-Key, курсорную пагинацию и формат ошибок RFC 7807 Problem Details.'),
    ]),
    ('2.4', 'Юнит 2.4 · Веб-безопасность', [
        ('2.4.1', 'Политика безопасности браузера: Same-Origin Policy, CORS (Preflight OPTIONS) и защита от CSRF',
         ['К-104', 'К-105'], ['Ф-122', 'Ф-123'],
         'Настроить строгую политику CORS для доверенных источников и защиту от межсайтовой подделки запроса (CSRF Token + SameSite).'),
        ('2.4.2', 'Защита от клиентских и серверных инъекций (XSS, Content-Security-Policy, SQL Injection)',
         ['К-106', 'К-107'], ['Ф-124', 'Ф-125'],
         'Продемонстрировать уязвимость SQL Injection на сырой конкатенации строк, закрыть её параметризованным запросом и экранировать XSS.'),
    ]),
]

BACKEND_CURRICULUM_SPEC = [
    ('3.1', 'Юнит 3.1 · Часть I — Фреймворк FastAPI и Pydantic v2', [
        ('3.1.1', 'Бэкенд-фреймворки с нуля (FastAPI vs Django vs DRF vs Flask) и валидация схем Pydantic v2',
         ['К-236', 'К-079'], ['Ф-282', 'Ф-102'],
         'Сравнить архитектурные модели бэкенд-фреймворков и создать схемы Pydantic v2 с кастомными валидаторами (@field_validator, @model_validator).'),
        ('3.1.2', 'Маршрутизация FastAPI с нуля: Path/Query/Body, response_model, APIRouter и Dependency Injection (Depends с yield)',
         ['К-090', 'К-092', 'К-093'], ['Ф-114', 'Ф-115'],
         'Спроектировать эндпоинты FastAPI с разделением входных/выходных схем, модульными APIRouter и внедрением зависимостей через Depends с yield.'),
        ('3.1.3', 'Асинхронное ядро и промышленный FastAPI: async def vs def, Lifespan, Middleware, Exception Handlers и BackgroundTasks',
         ['К-094', 'К-227'], ['Ф-280', 'Ф-222', 'Ф-272'],
         'Реализовать управление ресурсами через lifespan, конвейер ASGI Middleware, глобальные обработчики доменных ошибок и фоновые задачи.'),
    ]),
    ('3.2', 'Юнит 3.2 · Часть II — Фреймворк Django и ORM', [
        ('3.2.1', 'Архитектура Django с нуля: паттерн MTV, маршрутизация URLconf, Views (FBV vs CBV) и шаблонизатор DTL',
         ['К-083', 'К-082'], ['Ф-105', 'Ф-106', 'Ф-107'],
         'Спроектировать маршруты и представления Django по архитектуре MTV, сравнив функциональные (FBV) и классовые (CBV) представления.'),
        ('3.2.2', 'Django ORM и производительность запросов: модели, ленивость QuerySet, проблема N+1 (select_related / prefetch_related), F() и Q()',
         ['К-084', 'К-088'], ['Ф-110', 'Ф-111', 'Ф-267'],
         'Устранить проблему N+1 запросов через select_related и prefetch_related и выполнить атомарные обновления и сложные выборки через F() и Q().'),
        ('3.2.3', 'Внутреннее устройство Django: жизненный цикл HTTP-запроса, Middleware, Forms, Django Admin и Сигналы (Pub/Sub)',
         ['К-087', 'К-086', 'К-085', 'К-081'], ['Ф-268', 'Ф-097', 'Ф-109', 'Ф-108', 'Ф-223'],
         'Проследить 7 шагов пути запроса внутри Django, написать кастомный Middleware, настроить Django Admin и слабосвязанные обработчики сигналов.'),
    ]),
    ('3.3', 'Юнит 3.3 · Часть III — Фреймворк Django REST Framework (DRF)', [
        ('3.3.1', 'Сериализаторы DRF с нуля: Serializer vs ModelSerializer, двухэтапная валидация, source, SerializerMethodField и сохранение',
         ['К-091'], ['Ф-112'],
         'Реализовать ModelSerializer с полевой и объектной валидацией (validate_<field>, validate), вычисляемыми полями и переопределением create/update.'),
        ('3.3.2', 'Представления и маршрутизация в DRF: APIView, GenericAPIView, Mixins, ModelViewSet, @action и Routers',
         ['К-237'], ['Ф-283'],
         'Построить REST API на ModelViewSet с динамическим выбором сериализатора (get_serializer_class), кастомным @action и регистрацией в DefaultRouter.'),
        ('3.3.3', 'Безопасность, фильтрация и документация в DRF: Authentication, Permissions, django-filter, Pagination, Throttling и drf-spectacular',
         ['К-238'], ['Ф-284'],
         'Реализовать объектные права доступа (has_object_permission), фильтрацию выборки в get_queryset(), пагинацию и троттлинг запросов в DRF.'),
    ]),
    ('3.4', 'Юнит 3.4 · Часть IV — Микрофреймворк Flask', [
        ('3.4.1', 'Микрофреймворк Flask с нуля: философия Werkzeug/Jinja2, маршрутизация @app.route, объект request и формирование JSON-ответов',
         ['К-095'], ['Ф-285'],
         'Создать HTTP-обработчики во Flask с безопасным чтением query-параметров (request.args.get), JSON-тела и формированием ответов jsonify.'),
        ('3.4.2', 'Архитектура контекстов во Flask: Application Context (current_app, g) vs Request Context (request, session) и LocalProxy',
         ['К-097', 'К-096'], ['Ф-117', 'Ф-116'],
         'Продемонстрировать изоляцию состояния запроса в объекте flask.g и работу внутри блоков with app.app_context() и test_request_context().'),
        ('3.4.3', 'Модульная архитектура Flask в продакшене: Blueprints, паттерн Application Factory (create_app), хуки жизненного цикла и расширения',
         ['К-089'], ['Ф-113'],
         'Собрать модульное приложение Flask по паттерну Application Factory (create_app) с регистрацией Blueprints, init_app и глобальным errorhandler.'),
    ]),
    ('3.5', 'Юнит 3.5 · Часть V — Аутентификация, авторизация и криптозащита', [
        ('3.5.1', 'Токены и федеративный вход: анатомия JWT (Access + Refresh, ротация jti), OAuth 2.0 (Authorization Code + PKCE) и OIDC',
         ['К-098', 'К-099'], ['Ф-118', 'Ф-119'],
         'Реализовать выпуск, проверку и безопасную ротацию пары JWT-токенов (Access + Refresh) и генерацию пары PKCE для OAuth 2.0.'),
        ('3.5.2', 'Архитектура состояния и машинная аутентификация: Сессии в Redis vs JWT, Stateful vs Stateless и API-ключи с префиксами',
         ['К-100', 'К-101', 'К-108'], ['Ф-096', 'Ф-120', 'Ф-281'],
         'Спроектировать хранение серверных сессий в Redis и безопасную генерацию/проверку хешированных API-ключей с открытыми префиксами.'),
        ('3.5.3', 'Модели авторизации и криптозащита паролей: RBAC, ABAC, защита от BOLA/IDOR и хеширование (Argon2id, bcrypt, PBKDF2)',
         ['К-102', 'К-103'], ['Ф-121', 'Ф-270'],
         'Реализовать ролевую модель доступа (RBAC), проверку владения ресурсом (защита от IDOR) и хеширование паролей с уникальной солью.'),
    ]),
    ('3.6', 'Юнит 3.6 · Часть VI — Слоистая архитектура, транзакции и кэширование', [
        ('3.6.1', 'Слоистая архитектура бэкенда: разделение Transport (Router), Service Layer, Repository и паттерн Unit of Work (UoW)',
         ['К-228'], ['Ф-273'],
         'Разделить бэкенд на слои Transport, Service и Repository и реализовать транзакционный контекстный менеджер Unit of Work.'),
        ('3.6.2', 'Управление транзакциями, Connection Pool и конкурентные блокировки (SELECT FOR UPDATE vs Optimistic Locking)',
         ['К-229'], ['Ф-274'],
         'Защитить финансовую операцию от аномалии Lost Update с помощью пессимистичной (FOR UPDATE) и оптимистичной блокировки версий без дедлоков.'),
        ('3.6.3', 'Прикладное кэширование на бэкенде: Redis, стратегия Cache-Aside, защита от Cache Stampede и Distributed Locks',
         ['К-230'], ['Ф-275'],
         'Реализовать сервис кэширования Cache-Aside с инвалидацией, защитой от эффекта стада (Cache Stampede) и атомарным Redis Lock.'),
    ]),
    ('3.7', 'Юнит 3.7 · Часть VII — Отказоустойчивые интеграции, очереди и Rate Limiting', [
        ('3.7.1', 'Отказоустойчивые HTTP-интеграции: httpx, таймауты, Exponential Backoff с Jitter, Circuit Breaker и Webhooks с HMAC',
         ['К-224', 'К-231'], ['Ф-264', 'Ф-276'],
         'Реализовать HTTP-клиент с ретраями (Exponential Backoff + Jitter), автомат защиты Circuit Breaker и проверку HMAC-подписи вебхуков.'),
        ('3.7.2', 'Фоновые воркеры и брокеры сообщений: Celery, RabbitMQ vs Kafka, паттерн Transactional Outbox и Dead Letter Queue (DLQ)',
         ['К-232'], ['Ф-277'],
         'Реализовать идемпотентный фоновый воркер с очередью недоставленных сообщений (DLQ) и паттерн Transactional Outbox для гарантии доставки.'),
        ('3.7.3', 'Защита бэкенда от перегрузок и злоупотреблений: алгоритмы Rate Limiting (Token Bucket, Sliding Window, Redis INCR)',
         ['К-109'], ['Ф-271'],
         'Реализовать ограничитель частоты запросов (Rate Limiter) по алгоритмам Token Bucket и Sliding Window с заголовками Retry-After.'),
    ]),
    ('3.8', 'Юнит 3.8 · Часть VIII — Файлы и S3, 12-Factor, Observability и тестирование API', [
        ('3.8.1', 'Потоковая работа с файлами (Chunked Streaming), валидация Magic Bytes и облачные хранилища S3 (Presigned URLs)',
         ['К-233'], ['Ф-278'],
         'Реализовать потоковую обработку файла фиксированными чанками за O(1) памяти, проверку сигнатур Magic Bytes и генерацию Presigned URL.'),
        ('3.8.2', 'Конфигурация по 12-Factor App (pydantic-settings) и Наблюдаемость (JSON-логи, Correlation ID, Prometheus, Health Checks)',
         ['К-234', 'К-235'], ['Ф-185', 'Ф-279'],
         'Настроить Fail-Fast валидацию окружения, сквозной X-Request-ID через contextvars, сбор метрик RED и раздельные пробы Liveness/Readiness.'),
        ('3.8.3', 'Промышленное тестирование бэкенда и API: pytest, TestClient, AsyncClient, dependency_overrides и изоляция БД',
         ['К-226'], ['Ф-269'],
         'Написать интеграционные тесты эндпоинтов с подменой зависимостей через dependency_overrides и транзакционным откатом тестовой БД.'),
    ]),
]

def render_module_markdown(mod_header: str, units_spec: list) -> str:
    out = [f"## 📁 {mod_header}", "", "---", ""]
    for u_num, u_title, skills in units_spec:
        out.append(f"### 📘 {u_title}")
        out.append("")
        for s_num, s_title, k_ids, f_ids, practice_text in skills:
            out.append(f"- [ ] ⚡ **Skill {s_num} · {s_title} [⬜ Not Started]**")
            out.append("  - 📖 **Конспект теории**:")
            for kid in k_ids:
                out.append(f"    - [[{id_to_rel_stem[kid]}]]")
            out.append("  - 📇 **Карточки RemNote**:")
            for fid in f_ids:
                out.append(f"    - [[{id_to_rel_stem[fid]}]]")
            out.append(f"  - 💻 **Практика кодинга**: {practice_text}")
            out.append("  - 🎯 **Критерий мастерства**: беглое прохождение карточек без подсказок (Accuracy > 90%) + рабочий чистый код задачи без синтаксических ошибок.")
            out.append("")
            out.append("- ────────────────────────────────────────")
        out.append("")
        out.append(f"- 🏆 **UNIT TEST {u_num}**: Аттестационный срез и защита юнита в чате.")
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)

map_path = os.path.join(BASE, '00 · 🗺️ Карта Мастерства.md')
with open(map_path, 'r', encoding='utf-8') as f:
    map_text = f.read()

# 0. If Modules 03..06 in Карта Мастерства have not yet been shifted to 04..07, shift them in reverse order
if '## 📁 03 · ⚡ Алгоритмы' in map_text:
    for old_m, new_m, old_u, new_u in SHIFT_MODS:
        map_text = map_text.replace(old_m, new_m)
        map_text = re.sub(rf'\bЮнит {old_u}\.(\d+)', rf'Юнит {new_u}.\1', map_text)
        map_text = re.sub(rf'\bSkill {old_u}\.(\d+\.\d+)', rf'Skill {new_u}.\1', map_text)
        map_text = re.sub(rf'\bUNIT TEST {old_u}\.(\d+)', rf'UNIT TEST {new_u}.\1', map_text)

# 1. Update summary progress block for Modules 01..07
map_text = re.sub(
    r'- \[ \] \*\*01 · 🐍 Python\*\*.*?(?=\n---)',
    (
        '- [ ] **01 · 🐍 Python** – 0 из 9 юнитов (28 навыков)\n'
        '- [ ] **02 · 🌐 Web** – 0 из 4 юнитов (10 навыков)\n'
        '- [ ] **03 · ⚙️ Backend** – 0 из 8 юнитов (24 навыка)\n'
        '- [ ] **04 · ⚡ Алгоритмы** – 0 из 6 юнитов (12 навыков)\n'
        '- [ ] **05 · 🗄️ Базы данных** – 0 из 6 юнитов (17 навыков)\n'
        '- [ ] **06 · 🏛️ Архитектура** – 0 из 6 юнитов (14 навыков)\n'
        '- [ ] **07 · 🚀 Инфраструктура** – 0 из 6 юнитов (21 навык)'
    ),
    map_text,
    flags=re.S
)

# 2. Replace Module 02 + Module 03 sections between Module 01 and Module 04 · ⚡ Алгоритмы
new_mod2_mod3_md = (
    render_module_markdown('02 · 🌐 Web', WEB_CURRICULUM_SPEC)
    + "\n"
    + render_module_markdown('03 · ⚙️ Backend', BACKEND_CURRICULUM_SPEC)
)

pattern_mod2_3 = re.compile(r'## 📁 02 · 🌐 Web.*?(?=## 📁 04 · ⚡ Алгоритмы)', re.S)
assert pattern_mod2_3.search(map_text), "Could not locate Module 02/03 section in 00 · 🗺️ Карта Мастерства.md"
map_text = pattern_mod2_3.sub(new_mod2_mod3_md + "\n", map_text)

# 3. Update any cross-references in other modules (01, 05, 06, 07) that still point to old 02/03 paths
def fix_cross_links(match):
    inner = match.group(1)
    m_id = re.search(r'([КФ]-\d+)\.', inner)
    if m_id and m_id.group(1) in id_to_rel_stem and (inner.startswith('02 · ') or inner.startswith('03 · ⚙️')):
        return f"[[{id_to_rel_stem[m_id.group(1)]}]]"
    return match.group(0)

map_text = re.sub(r'\[\[((?:02|03) · [^\]]+)\]\]', fix_cross_links, map_text)

with open(map_path, 'w', encoding='utf-8') as f:
    f.write(map_text)

print("Updated 00 · 🗺️ Карта Мастерства.md with 02 · 🌐 Web (2.1–2.4) and 03 · ⚙️ Backend (3.1–3.8, 24 skills)!")

