# -*- coding: utf-8 -*-
"""
Полное обогащение и вычитка конспектов и карточек Модуля 03 · ⚙️ Backend (Юниты 3.1–3.8).
Каждая часть написана с нуля простым и исчерпывающим языком (ментальная модель,
пошаговый путь запроса, перевод терминов, сравнение Junior vs Senior и исполняемые примеры с print()).
"""

ENRICHED_BACKEND_NOTES = {
    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.1 · ЧАСТЬ I: ФРЕЙМВОРК FASTAPI И PYDANTIC V2
    # ═══════════════════════════════════════════════════════════════════════════
    'К-236': (
        '3.1',
        'К-236. Введение в бэкенд-фреймворки Python с нуля_ FastAPI vs Django vs DRF vs Flask.md',
        r"""📖 Перечитать конспект: Введение в бэкенд-фреймворки Python с нуля: FastAPI vs Django vs DRF vs Flask >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое бэкенд-фреймворк с самого нуля (Ментальная модель)

Представьте, что вы открываете ресторан. Вы можете сами рубить деревья для столов, вручную разводить костёр и гонять курьеров без правил — это написание сервера на «голых» TCP-сокетах (`socket`) или сыром интерфейсе `WSGI/ASGI`. В реальной жизни вы арендуете готовую профессиональную кухню с плитами, вытяжкой, холодильниками и системой заказов — это и есть **бэкенд-фреймворк (Backend Framework — каркас серверного приложения)**.

Когда клиент (браузер или мобильное приложение) отправляет HTTP-запрос, например `POST /orders` с JSON-корзиной товаров, бэкенд-фреймворк берёт на себя всю рутину:

1. **Маршрутизация (Routing)**: понимает, какую именно Python-функцию нужно вызвать для адреса `/orders` и метода `POST`.
2. **Парсинг и валидация (Parsing & Validation)**: превращает сырые байты тела запроса в удобный Python-объект и проверяет, что цена — это положительное число, а не текст `"бесплатно"`.
3. **Аутентификация и права (AuthN & AuthZ)**: проверяет токен или сессионную куку пользователя.
4. **Работа с базой данных (ORM / Data Layer)**: безопасно сохраняет заказ в PostgreSQL без риска SQL-инъекций.
5. **Сериализация ответа (Serialization)**: упаковывает результат обратно в JSON со статус-кодом `201 Created`.

```python
def simulate_framework_pipeline(method: str, path: str, body: dict) -> tuple[int, dict]:
    routes = {("POST", "/orders"): "create_order_handler"}
    handler_name = routes.get((method, path))
    if not handler_name:
        return 404, {"detail": "Маршрут не найден"}
    if not isinstance(body.get("amount"), (int, float)) or body["amount"] <= 0:
        return 422, {"detail": "Поле amount должно быть числом > 0"}
    return 201, {"id": 101, "status": "created", "amount": body["amount"]}

status_ok, resp_ok = simulate_framework_pipeline("POST", "/orders", {"amount": 2500})
status_err, resp_err = simulate_framework_pipeline("POST", "/orders", {"amount": -5})
print(f"Успешный запрос -> {status_ok}: {resp_ok}")
print(f"Ошибка валидации -> {status_err}: {resp_err}")
```

---

## Четыре главных инструмента Python-бэкенда: кто есть кто

В экосистеме Python нет «одного фреймворка на все случаи». В индустрии доминируют четыре тесно связанных инструмента, каждый со своей философией:

| Характеристика | ⚡ **FastAPI** | 🎸 **Django** | 🛡️ **Django REST Framework (DRF)** | 🌶️ **Flask** |
| :--- | :--- | :--- | :--- | :--- |
| **Философия** | Современный асинхронный микросервисный API на тайпингах | «Всё включено» (*Batteries Included*): монолит с ORM и админкой | Мощный конструктор REST API поверх моделей и ORM Django | Минималистичный микрофреймворк: только ядро, остальное — плагины |
| **Протокол шлюза** | **ASGI** (`uvicorn`, нативный `async/await`) | **WSGI** (`gunicorn`) + поддержка ASGI | **WSGI** / ASGI (работает внутри Django) | **WSGI** (`Werkzeug` / `gunicorn`) |
| **Валидация данных** | Встроенная через **Pydantic v2** (ядро на Rust) | **Django Forms** / `ModelForm` | **DRF Serializers** (`ModelSerializer`) | Внешние библиотеки (`Pydantic`, `Marshmallow`) |
| **Работа с БД (ORM)** | Любая (обычно **SQLAlchemy 2.0 Async**) | Встроенная **Django ORM** + встроенные миграции | Использует **Django ORM** | Обычно **Flask-SQLAlchemy** + `Alembic` |
| **Авто-документация** | Из коробки (**Swagger UI** `/docs` и **ReDoc**) | Нет (рендерит HTML-страницы) | Через пакет **`drf-spectacular`** (OpenAPI 3) | Через расширения (`flask-smorest`, `flasgger`) |

---

## Когда что выбирать на практике и как отвечать на собеседовании

- **Выбирайте `Django + DRF`**, если вы строите крупную бизнес-систему (e-commerce, финтех-бэкофис, CRM, образовательную платформу), где важны:
  - готовая **админ-панель (`Django Admin`)** из коробки для менеджеров и поддержки;
  - единый стандарт структуры проекта (любой новый Django-разработчик сразу знает, где лежат `models.py`, `views.py`, `serializers.py`);
  - зрелая ORM с автоматической генерацией миграций (`makemigrations`).
- **Выбирайте `FastAPI`**, если вы строите:
  - высоконагруженный асинхронный микросервис, который параллельно ходит в 5 внешних API, базовые модели LLM, Redis и PostgreSQL (`asyncpg`);
  - публичный или внутренний JSON API со строгими контрактами типов (`Pydantic v2`) и мгновенной автогенерацией `OpenAPI 3.1`;
  - сервис реального времени с **WebSockets** или потоковой передачей (**StreamingResponse**).
- **Выбирайте `Flask`**, если вам нужен:
  - лёгкий синхронный сервис, webhook-приёмник, внутренний дашборд или обёртка над ML-моделью без тяжёлой инфраструктуры Django;
  - полный контроль над тем, какие именно компоненты подключать.

### Сравнение: Junior vs Senior при выборе фреймворка
- **Ошибка Junior-разработчика**: выбирать один фреймворк «потому что он модный» для любой задачи — например, писать с нуля самописную админку для 50 таблиц на FastAPI вместо использования готового `Django Admin`, или тянуть монолит Django для крошечного асинхронного прокси-шлюза.
- **Подход Senior-разработчика**: отталкиваться от бизнес-требований, профиля нагрузки (`I/O-bound` vs `CRUD` с бэкофисом) и стоимости поддержки.

```python
def choose_framework(needs_admin: bool, high_async_io: bool, minimal_footprint: bool) -> str:
    if needs_admin:
        return "Django + Django REST Framework (DRF): готовая админка, ORM и сериализаторы"
    if high_async_io:
        return "FastAPI + Pydantic v2 + Async SQLAlchemy: неблокирующий ASGI и авто-OpenAPI"
    if minimal_footprint:
        return "Flask: лаконичный WSGI-микрофреймворк с Blueprints"
    return "FastAPI или Django REST Framework в зависимости от экспертизы команды"

print("1. E-commerce с бэкофисом:", choose_framework(needs_admin=True, high_async_io=False, minimal_footprint=False))
print("2. Асинхронный AI-шлюз:", choose_framework(needs_admin=False, high_async_io=True, minimal_footprint=False))
print("3. Лёгкий микросервис:", choose_framework(needs_admin=False, high_async_io=False, minimal_footprint=True))
```
"""
    ),

    'К-079': (
        '3.1',
        'К-079. Pydantic_ валидация и парсинг данных.md',
        r"""📖 Перечитать конспект: Pydantic v2: валидация, парсинг данных и контракт схем >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Зачем нужен Pydantic: проблема «сырых словарей» (`dict`)

Новичок в бэкенде часто принимает JSON от клиента как обычный словарь `data: dict` и пишет десятки ручных проверок `if "email" not in data...`. Такой код хрупок, не подсказывает поля в IDE и пропускает некорректные типы вглубь бизнес-логики.

**Pydantic v2** — это библиотека парсинга и валидации данных на основе стандартных аннотаций типов Python, вычислительное ядро которой (`pydantic-core`) написано на **Rust**.
Главный принцип Pydantic: **«Парсинг, а не просто проверка» (Parse, don't validate)**. На входе вы подаёте «грязный» словарь из сети, а на выходе получаете строго типизированный объект с гарантированными типами полей либо структурированное исключение `ValidationError`.

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    age: int = Field(ge=18, le=120)
    is_active: bool = True

# Pydantic автоматически приводит совместимые типы ('25' -> 25) и проверяет ограничения
user = UserCreate(username="alex_dev", age="25")
print("Схема успешно создана:", user.username, "| тип age:", type(user.age).__name__, "| значение:", user.age)
print("Сериализация в dict через model_dump():", user.model_dump())
```

---

## Ключевые методы Pydantic v2 (отличия от устаревшего v1)

На собеседованиях часто проверяют, пишете ли вы на современном **Pydantic v2** или используете удалённые/устаревшие методы первой версии:

| Задача | Устаревший Pydantic v1 | Современный **Pydantic v2** |
| :--- | :--- | :--- |
| Превратить модель в `dict` | `user.dict()` | **`user.model_dump()`** (поддерживает `exclude_unset=True`) |
| Превратить модель в JSON-строку | `user.json()` | **`user.model_dump_json()`** |
| Провалидировать `dict` или ORM-объект | `User.parse_obj(data)` / `User.from_orm(obj)` | **`User.model_validate(data)`** |
| Валидатор одного поля | `@validator("email")` | **`@field_validator("email")`** + `@classmethod` |
| Валидатор всей модели целиком | `@root_validator` | **`@model_validator(mode="after")`** |
| Настройка модели (чтение из ORM) | `class Config: orm_mode = True` | **`model_config = ConfigDict(from_attributes=True)`** |

---

## Кастомная валидация: `@field_validator` и `@model_validator`

Когда встроенных ограничений `Field(ge=..., min_length=..., pattern=...)` недостаточно, используются декораторы валидации:
- **`@field_validator("field_name")`** — проверяет или нормализует одно конкретное поле (например, приводит `email` к нижнему регистру и проверяет домен).
- **`@model_validator(mode="after")`** — вызывается после сборки всех полей и позволяет сверить несколько полей друг с другом (например, `password == password_confirm` или `end_date > start_date`).

```python
from pydantic import BaseModel, field_validator, model_validator

class RegistrationSchema(BaseModel):
    email: str
    password: str
    password_repeat: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("Некорректный формат email")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError("Пароли не совпадают")
        return self

reg = RegistrationSchema(email="  Alice@Example.com ", password="secret_password", password_repeat="secret_password")
print("Нормализованный email:", reg.email)
```

---

## Разделение схем (DTO) и сравнение Junior vs Senior

- **Антипаттерн Junior-разработчика**: использовать одну общую схему `UserSchema` на все случаи жизни или вызывать `payload.model_dump()` при `PATCH`-запросе без `exclude_unset=True`, случайно затирая существующие колонки в БД значением `None`.
- **Подход Senior-разработчика**: разделять схемы по ролям (**Data Transfer Objects — DTO**):
  - **`UserCreate`** (вход `POST /users`): принимает `email` + сырой `password`.
  - **`UserUpdate`** (вход `PATCH /users/{id}`): все поля опциональные (`Optional[...] = None`). При сохранении вызывается `data.model_dump(exclude_unset=True)`, чтобы обновить в БД **только те поля, которые клиент реально прислал в JSON**!
  - **`UserRead`** (выход `response_model`): содержит `id`, `email`, `created_at` и настройку `from_attributes=True`, но **не содержит `password_hash`**, физически исключая утечку хеша пароля в API.

```python
from typing import Optional
from pydantic import BaseModel

class UserPatchDTO(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None

patch_payload = UserPatchDTO(username="new_nick")
print("Обычный model_dump():", patch_payload.model_dump())
print("Только переданные поля (exclude_unset=True):", patch_payload.model_dump(exclude_unset=True))
```
"""
    ),

    'К-090': (
        '3.1',
        'К-090. FastAPI базово_ path-операции,.md',
        r"""📖 Перечитать конспект: Основы FastAPI с нуля: Path, Query, Body, статус-коды, response_model и OpenAPI >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Как устроен эндпоинт в FastAPI с нуля

В FastAPI каждое правило обработки HTTP-запроса называется **Path Operation (операция пути)**. Оно состоит из:
1. **Декоратора HTTP-метода и пути**: `@app.get("/items/{item_id}")`, `@app.post("/items")`, `@app.patch(...)`, `@app.delete(...)`.
2. **Функции-обработчика** (`async def` или `def`), аргументы которой снабжены аннотациями типов.

Главная суперсила FastAPI: он анализирует **аннотации типов аргументов функции** и автоматически понимает, откуда брать данные:
- Если имя аргумента есть в фигурных скобках маршрута (`{item_id}`) — это **Path-параметр (параметр пути)**, например `/items/42`.
- Если аргумент имеет примитивный тип (`int`, `str`, `bool`) и не указан в пути — это **Query-параметр (параметр строки запроса)**, например `?limit=10&offset=0`.
- Если тип аргумента — класс, унаследованный от `pydantic.BaseModel` — FastAPI читает и валидирует его из **JSON-тела запроса (Request Body)**.

```python
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Catalog API")

class ItemCreate(BaseModel):
    title: str
    price: float

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., ge=1, description="ID товара в каталоге"),
    currency: str = Query("RUB", min_length=3, max_length=3)
):
    return {"item_id": item_id, "currency": currency, "price": 1990.0}

import asyncio
res = asyncio.run(get_item(item_id=42, currency="RUB"))
print("Ответ эндпоинта get_item:", res)
```

---

## Статус-коды ответов и обработка ошибок через `HTTPException`

По умолчанию FastAPI возвращает статус `200 OK`. Но для грамотного REST-контракта мы явно задаём статус в декораторе:
- `status_code=201` (`status.HTTP_201_CREATED`) — при успешном создании ресурса в `@app.post`.
- `status_code=204` (`status.HTTP_204_NO_CONTENT`) — при удалении в `@app.delete`, когда тело ответа пустое.
- Если входные данные не прошли проверку Pydantic (например, в `item_id` передали `"abc"` вместо числа), FastAPI **сам автоматически** вернёт статус **`422 Unprocessable Entity`** с подробным JSON-описанием ошибки.
- Если запись не найдена в БД или нет прав доступа, мы выбрасываем **`raise HTTPException(status_code=404, detail="Товар не найден")`**:

```python
from fastapi import HTTPException

FAKE_DB = {1: {"id": 1, "title": "Механическая клавиатура", "price": 8500}}

def fetch_item_or_404(item_id: int) -> dict:
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Товар #{item_id} не найден")
    return FAKE_DB[item_id]

print("Найден товар:", fetch_item_or_404(1))
try:
    fetch_item_or_404(999)
except HTTPException as exc:
    print(f"Перехвачен HTTPException -> status={exc.status_code}, detail={exc.detail!r}")
```

---

## Защита выходных данных через `response_model` (Junior vs Senior)

- **Антипаттерн Junior-разработчика**: возвращать из эндпоинта ORM-объект `return db_user` без указания `response_model` и возвращать `200 OK` с текстом `{"error": "not found"}` вместо честного HTTP-кода `404`.
- **Подход Senior-разработчика**: всегда задавать **`response_model=UserRead`** в декораторе роутера. Это решает сразу три задачи:
  1. **Безопасная фильтрация**: удаляет из ответа все поля, которых нет в схеме `UserRead` (даже если функция вернула словарь с `password_hash`).
  2. **Валидация контракта ответа**: гарантирует фронтенду, что сервер никогда случайно не нарушит обещанный формат ответа.
  3. **Генерация схемы ответа в OpenAPI**: документирует точный JSON-формат ответа в Swagger UI (`/docs`) и ReDoc (`/redoc`).

```python
from pydantic import BaseModel

class UserPublicResponse(BaseModel):
    id: int
    username: str
    email: str

raw_db_user = {
    "id": 7,
    "username": "ksenya",
    "email": "ksenya@example.com",
    "password_hash": "$argon2id$v=19$m=65536$super_secret_hash",
}

safe_output = UserPublicResponse(**raw_db_user).model_dump()
print("Отфильтрованный через response_model ответ клиенту:", safe_output)
assert "password_hash" not in safe_output
```
"""
    ),

    'К-092': (
        '3.1',
        'К-092. APIRouter_ организация кода в FastAPI.md',
        r"""📖 Перечитать конспект: APIRouter: модульная архитектура и организация кода в FastAPI >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Проблема монолитного `main.py` и зачем нужен `APIRouter`

В учебных примерах все маршруты пишут в одном файле `main.py` через `@app.get(...)`. Но в реальном проекте с 80 эндпоинтами (пользователи, товары, заказы, платежи, уведомления) один файл на 3000 строк превращается в нечитаемый ком, где каждый `git merge` вызывает конфликты.

**`APIRouter`** — это «мини-приложение FastAPI», которое позволяет вынести маршруты конкретной предметной области (домена) в отдельный модуль со своим общим префиксом URL (`prefix`), тегами документации (`tags`) и общими зависимостями (`dependencies`), а затем подключить его к главному `app` одной строкой `app.include_router(...)`.

```python
from fastapi import FastAPI, APIRouter

users_router = APIRouter(prefix="/users", tags=["Users"])
orders_router = APIRouter(prefix="/orders", tags=["Orders"])

@users_router.get("/{user_id}")
async def get_user_endpoint(user_id: int):
    return {"user_id": user_id, "role": "member"}

@orders_router.post("/")
async def create_order_endpoint():
    return {"order_id": 501, "status": "new"}

app = FastAPI(title="Modular E-Commerce API")
app.include_router(users_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")

import asyncio
print("Вызов модульного роутера пользователей:", asyncio.run(get_user_endpoint(10)))
print("Вызов модульного роутера заказов:", asyncio.run(create_order_endpoint()))
```

---

## Групповая защита роутера через `dependencies=[Depends(...)]`

Представьте, что у вас есть 15 эндпоинтов админ-панели (`/admin/users`, `/admin/stats`, `/admin/refunds`). Дублировать `admin: User = Depends(require_admin)` в аргументах каждой из 15 функций — нарушение принципа **DRY (Don't Repeat Yourself)** и риск случайно забыть проверку на новом эндпоинте.

В `APIRouter` можно передать список `dependencies` сразу на весь роутер (или при вызове `app.include_router`): тогда FastAPI автоматически выполнит проверку перед каждым эндпоинтом этого модуля!

```python
from fastapi import APIRouter, Depends, HTTPException

def verify_internal_token(token: str = "valid-secret"):
    if token != "valid-secret":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return True

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_internal_token)],
)

print("Проверка токена уровня роутера:", verify_internal_token("valid-secret"))
```

---

## Эталонная структура папок (Junior vs Senior)

- **Антипаттерн Junior-разработчика**: сваливать модели БД, схемы Pydantic и 50 маршрутов в один `main.py` без версионирования `/api/v1`, из-за чего любое изменение контракта ломает старые мобильные клиенты.
- **Подход Senior-разработчика**: изолировать домены через `APIRouter`, группировать версии в `api/v1/router.py` и чётко разделять слои `api/`, `schemas/`, `services/`, `repositories/`, `models/`:

```text
src/
├── main.py              # Точка входа: создание FastAPI(lifespan=...), подключение роутеров
├── core/
│   ├── config.py        # Настройки pydantic-settings (BaseSettings)
│   └── security.py      # JWT, хеширование паролей
├── api/
│   ├── deps.py          # Общие зависимости: get_db, get_current_user
│   └── v1/
│       ├── router.py    # Главный роутер v1, объединяющий под-роутеры
│       ├── users.py     # APIRouter(prefix="/users", tags=["Users"])
│       └── orders.py    # APIRouter(prefix="/orders", tags=["Orders"])
├── schemas/             # Pydantic v2 DTO (UserCreate, UserRead, OrderRead)
├── services/            # Бизнес-логика (UserService, OrderService)
├── repositories/        # Работа с БД (SQLAlchemy запросы)
└── models/              # Таблицы ORM (SQLAlchemy DeclarativeBase)
```
"""
    ),

    'К-093': (
        '3.1',
        'К-093. Dependency Injection в FastAPI.md',
        r"""📖 Перечитать конспект: Dependency Injection в FastAPI: граф Depends, генераторы с yield и подмена в тестах >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое Dependency Injection (Junior vs Senior)

Представьте, что вашей функции-эндпоинту для работы нужны:
1. Открытая сессия базы данных (`db`);
2. Текущий авторизованный пользователь (`current_user`), извлечённый из JWT-токена в заголовке `Authorization`.

- **Антипаттерн Junior-разработчика**: внутри каждого эндпоинта вручную читать заголовок `request.headers.get("Authorization")`, декодировать JWT, открывать соединение с БД и забывать закрыть его при исключении.
- **Подход Senior-разработчика (`Depends`)**: объявить в параметрах функции, **что** нужно (`user: dict = Depends(get_current_user)`), доверив FastAPI разрешение графа зависимостей, кэширование на время запроса и гарантированное закрытие ресурсов после `yield`.

---

## Иерархический граф зависимостей и кэширование в рамках запроса

Зависимости могут зависеть друг от друга, образуя направленный граф (**DAG — Directed Acyclic Graph**):
`delete_order` ➔ зависит от `require_admin` ➔ зависит от `get_current_user` ➔ зависит от `get_db` и `oauth2_scheme`.

Важнейшее свойство FastAPI: по умолчанию (`use_cache=True`), если несколько зависимостей в рамках одного HTTP-запроса требуют `Depends(get_db)` или `Depends(get_current_user)`, FastAPI вызовет эту функцию **ровно один раз за запрос** и переиспользует результат из кэша запроса!

```python
from fastapi import Depends

def get_db_conn():
    return {"conn_id": 101, "active": True}

def get_current_user_dep(db: dict = Depends(get_db_conn)):
    return {"id": 42, "username": "alice", "role": "admin", "db_conn": db["conn_id"]}

def require_admin_dep(user: dict = Depends(get_current_user_dep)):
    assert user["role"] == "admin", "Требуются права администратора"
    return user

admin_user = require_admin_dep(get_current_user_dep(get_db_conn()))
print("Граф зависимостей успешно разрешён:", admin_user)
```

---

## Зависимости-генераторы с `yield`: безопасное закрытие ресурсов

Как открыть транзакционную сессию БД перед эндпоинтом и **гарантированно закрыть её** после отправки ответа (даже если внутри эндпоинта произошла ошибка)?
Для этого зависимость пишут как генератор с ключевым словом **`yield`** и блоком `try ... finally`:

1. Код **до `yield`** (`setup`) выполняется **до** входа в эндпоинт.
2. Значение, переданное в `yield session`, внедряется в аргумент эндпоинта.
3. Код в блоке **`finally` после `yield`** (`teardown`) гарантированно выполняется **после** завершения эндпоинта.

```python
def get_db_with_lifecycle(events_log: list):
    events_log.append("1. [setup] Открыта сессия БД")
    session_obj = {"tx": "open"}
    try:
        yield session_obj
        events_log.append("3. [commit] Запрос успешен")
    except Exception as exc:
        events_log.append(f"3. [rollback] Откат транзакции из-за: {exc}")
        raise
    finally:
        session_obj["tx"] = "closed"
        events_log.append("4. [teardown] Сессия закрыта и возвращена в пул")

log = []
gen = get_db_with_lifecycle(log)
db_sess = next(gen)
log.append(f"2. [endpoint] Работаем с сессией (tx={db_sess['tx']})")
try:
    next(gen)
except StopIteration:
    pass
print("\n".join(log))
```

---

## Классы как зависимости (`Callable Class`) и `dependency_overrides` в тестах

В качестве зависимости можно передать любой вызываемый объект: функцию, класс (тогда вызывается его `__init__`) или экземпляр класса с методом `__call__`.
А в автотестах (`pytest`) словарь **`app.dependency_overrides[get_db] = get_test_db`** позволяет подменить реальную БД или проверку JWT во всём приложении одной строчкой без единого `unittest.mock.patch`!
"""
    ),

    'К-094': (
        '3.1',
        'К-094. Асинхронность в FastAPI_ Event Loop и.md',
        r"""📖 Перечитать конспект: Асинхронное ядро FastAPI: Event Loop, ThreadPool и правила def vs async def >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Главный секрет FastAPI: как обрабатываются `async def` и обычные `def`

Многие начинающие разработчики думают, что если написать `async def` перед любой функцией в FastAPI, она автоматически станет работать быстрее. На самом деле неверное использование `async def` может **полностью заморозить ваш сервер**!

Разберём, что именно делает FastAPI под капотом:

1. **Если вы объявили эндпоинт через `async def`**:
   FastAPI запускает его **напрямую в главном потоке цикла событий (`Event Loop`)**. Внутри такой функции все сетевые операции обязаны быть неблокирующими и вызываться через `await` (`await session.execute(...)`, `await httpx_client.get(...)`). В момент `await` корутина уступает управление Event Loop, и сервер мгновенно переключается на обработку сотен других запросов.
2. **Если вы объявили эндпоинт через обычный синхронный `def`**:
   FastAPI понимает, что внутри может быть блокирующий код, и **автоматически отправляет выполнение функции во внешний пул потоков (`ThreadPool` — `anyio.to_thread.run_sync`, по умолчанию до 40 потоков)**, чтобы не заблокировать главный Event Loop!

---

## Смертельная ловушка (Junior vs Senior): блокирующий I/O внутри `async def`

- **Ошибка Junior-разработчика**: написать `async def get_report():` и внутри вызвать синхронный `time.sleep(2)`, `requests.get(...)` или синхронный драйвер БД `psycopg2`. Поскольку функция помечена как `async def`, FastAPI выполняет её прямо в единственном потоке Event Loop. Синхронный вызов блокирует поток ОС целиком — **все остальные пользователи на этом воркере зависают в очереди**!
- **Подход Senior-разработчика**: внутри `async def` использовать строго неблокирующие библиотеки (`httpx.AsyncClient`, `AsyncSession`, `asyncio.sleep`), а если нужно вызвать унаследованный синхронный SDK — объявлять роут как обычный `def` или оборачивать вызов в `await asyncio.to_thread(sync_fn, *args)`.

```python
import asyncio
import time

async def run_concurrent_demo():
    t0 = time.perf_counter()
    # Три неблокирующих корутины выполняются конкурентно за ~0.02с суммарно
    await asyncio.gather(
        asyncio.sleep(0.02),
        asyncio.sleep(0.02),
        asyncio.sleep(0.02),
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000
    print(f"3 конкурентных async-запроса по 20мс выполнились параллельно всего за {elapsed_ms:.1f} мс!")

asyncio.run(run_concurrent_demo())
```

---

## Золотая шпаргалка: когда писать `async def`, а когда `def`

| Что вызывается внутри эндпоинта | Как объявлять функцию | Почему и что делать |
| :--- | :--- | :--- |
| Асинхронные библиотеки (`AsyncSession`, `httpx.AsyncClient`, `redis.asyncio`) | **`async def`** + `await` | Максимальная производительность: тысячи конкурентных соединений в одном потоке Event Loop |
| Синхронная библиотека (`requests`, синхронный `SQLAlchemy Session`, `boto3`) | Обычный **`def`** (без `async`) | FastAPI сам безопасно вынесет вызов в `ThreadPool` (или используйте `await asyncio.to_thread(sync_fn)`) |
| Тяжёлые вычисления на процессоре (`CPU-bound`: сжатие видео, генерация PDF, pandas) | Вынести в **фоновый воркер (`Celery` / `ProcessPoolExecutor`)** | Из-за **GIL** ни `async def`, ни потоки `ThreadPool` не дадут параллелизма на CPU и будут тормозить Event Loop |

```python
import asyncio

def legacy_blocking_sdk(order_id: int) -> dict:
    return {"order_id": order_id, "synced": True}

async def safe_async_endpoint(order_id: int) -> dict:
    # Выносим синхронную функцию в пул потоков, не блокируя Event Loop:
    return await asyncio.to_thread(legacy_blocking_sdk, order_id)

print("Безопасный вызов через asyncio.to_thread:", asyncio.run(safe_async_endpoint(77)))
```
"""
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.2 · ЧАСТЬ II: ФРЕЙМВОРК DJANGO И ORM
    # ═══════════════════════════════════════════════════════════════════════════
    'К-083': (
        '3.2',
        'К-083. MVC и Django MTV.md',
        r"""📖 Перечитать конспект: Введение в Django с нуля: философия «Batteries Included» и паттерн MTV против MVC >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое Django и почему его называют «Batteries Included»

Если микрофреймворк (вроде Flask или FastAPI) — это конструктор, где вы сами выбираете и подключаете библиотеку для БД, миграций, авторизации и админки, то **Django** — это полноценный «швейцарский нож» с философией **«Batteries Included» («Батарейки в комплекте»)**.

Из коробки сразу после установки Django предоставляет:
- Мощную **ORM (Object-Relational Mapping)** для работы с PostgreSQL/MySQL/SQLite на Python без написания сырого SQL;
- Систему автоматических **миграций схемы БД** (`makemigrations` и `migrate`);
- Готовую систему пользователей, сессий, групп прав и хеширования паролей (`django.contrib.auth`);
- Защиту от CSRF, XSS, SQL-инъекций и Clickjacking;
- Автоматическую **админ-панель (`Django Admin`)** для управления данными.

---

## Архитектура классического MVC против Django MTV

В классической архитектуре веб-приложений используется паттерн **MVC (Model–View–Controller)**, разделяющий код на данные (`Model`), внешний вид (`View`) и управляющую логику (`Controller`).
В Django используется точно такое же разделение ответственности, но создатели фреймворка назвали слои **MTV (Model–Template–View)**:

| Слой в классическом **MVC** | Аналог в **Django (MTV)** | Где живёт в проекте и за что отвечает |
| :--- | :--- | :--- |
| **Model** (Модель данных) | **Model (Модель)** | `models.py` — описывает структуру таблиц БД, поля и бизнес-правила сущности |
| **View** (Отображение интерфейса) | **Template (Шаблон)** | `templates/*.html` — отвечает только за то, **как** отобразить данные пользователю |
| **Controller** (Контроллер-диспетчер) | **View (Представление) + URLconf** | `urls.py` + `views.py` — принимает `HttpRequest`, запрашивает данные у модели и возвращает `HttpResponse` |

Почему в Django контроллер назвали `View`? По замыслу авторов Django, функция в `views.py` определяет, **какую именно выборку данных («вид на данные»)** показать пользователю, а сам роль маршрутизатора-контроллера берёт на себя сам фреймворк и файл `urls.py`.

```python
# Наглядная модель прохождения запроса по архитектуре Django MTV:
class ArticleModel:
    _table = [{"id": 1, "title": "Django с нуля", "published": True}]
    @classmethod
    def get_published(cls):
        return [row for row in cls._table if row["published"]]

def render_template(template_name: str, context: dict) -> str:
    titles = ", ".join(a["title"] for a in context["articles"])
    return f"<!-- {template_name} --><h1>Статьи: {titles}</h1>"

def article_list_view(request: dict) -> dict:
    # View обращается к Model и передаёт данные в Template
    articles = ArticleModel.get_published()
    html_body = render_template("articles/list.html", {"articles": articles})
    return {"status": 200, "body": html_body}

resp = article_list_view({"method": "GET", "path": "/articles/"})
print("Ответ цепочки MTV:", resp)
```

---

## Где должна жить бизнес-логика в большом Django-проекте?

**Ошибка Junior-разработчика**: писать всю тяжёлую бизнес-логику (расчёт скидок, списание баланса, отправку писем) прямо внутри функции `views.py`. В итоге `views.py` разрастается до тысяч строк (`Fat Views`), и эту логику невозможно вызвать из Celery-задачи или консольной команды `manage.py`.

**Подход Senior-разработчика**:
- **`views.py` остаётся тонким**: он только принимает HTTP-запрос, проверяет права/формы и вызывает сервисный слой или метод модели, возвращая HTTP-ответ.
- **Доменная логика и сложные транзакции** выносятся в `services.py` (или методы модели/менеджера `QuerySet`).

```python
class OrderService:
    @staticmethod
    def calculate_discounted_total(items: list[dict], vip: bool = False) -> float:
        raw = sum(i["price"] * i["qty"] for i in items)
        return round(raw * (0.9 if vip else 1.0), 2)

def checkout_thin_view(request: dict) -> dict:
    total = OrderService.calculate_discounted_total(request["items"], vip=request.get("vip", False))
    return {"status": 200, "total_to_pay": total}

print("Тонкий View вызвал сервисный слой:", checkout_thin_view({"items": [{"price": 1000, "qty": 2}], "vip": True}))
```
"""
    ),

    'К-082': (
        '3.2',
        'К-082. Django базово_ views, urls, templates, forms.md',
        r"""📖 Перечитать конспект: Основы Django: проект vs приложение, urls.py, FBV vs CBV, templates и ModelForm >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Проект (`Project`) против Приложения (`App`) в Django

Первое, что видит новичок в Django — две команды: `django-admin startproject config` и `python manage.py startapp orders`. В чём разница?
- **Проект (`Project`)** — это весь ваш сайт или бэкенд целиком вместе с глобальными настройками `settings.py` и корневым маршрутизатором `urls.py`.
- **Приложение (`App`)** — это изолированный смысловой модуль внутри проекта (`users`, `catalog`, `orders`, `payments`). У каждого приложения своя папка с `models.py`, `views.py`, `urls.py`, `admin.py` и `migrations/`. Все созданные приложения обязательно регистрируются в списке **`INSTALLED_APPS`** в `settings.py`.

---

## Маршрутизация (`urls.py`): конвертеры путей и `include()`

Когда запрос приходит в Django, он попадает в корневой `urls.py` и проходит сверху вниз по списку `urlpatterns` до первого совпадения:
- Конвертеры типов `<int:pk>`, `<slug:post_slug>`, `<uuid:order_id>` автоматически проверяют часть URL и передают её в функцию `view` уже приведённой к нужному типу Python (`int`, `str`, `UUID`).
- Функция `include('orders.urls')` позволяет делегировать все маршруты с префиксом `orders/` в локальный `urls.py` приложения `orders`.
- Параметр `name='order-detail'` даёт маршруту символическое имя: тогда в коде мы пишем `reverse('order-detail', args=[42])` вместо хардкода строк `"/orders/42/"`.

```python
from django.urls import path, include, reverse

def order_detail_view(request, pk: int):
    return {"order_id": pk, "status": "delivered"}

urlpatterns = [
    path("orders/<int:pk>/", order_detail_view, name="order-detail"),
]

print("Зарегистрирован маршрут:", urlpatterns[0][0], "| name =", urlpatterns[0][2])
print("Обратное разрешение URL через reverse():", reverse("order-detail"))
```

---

## Представления (`views.py`): функции (FBV) против классов (CBV)

В Django есть два способа написать обработчик запроса (`View`):

1. **Function-Based Views (FBV — функциональные представления)**: обычная функция `def my_view(request, ...):`.
   - **Плюс**: максимально прозрачный поток управления, читается сверху вниз без скрытой магии наследования. Идеально для нестандартной бизнес-логики.
2. **Class-Based Views (CBV — классовые представления)**: классы, наследуемые от `View`, `ListView`, `DetailView`, `CreateView`. Подключаются в `urls.py` через `MyView.as_view()`.
   - **Плюс**: встроенный метод `dispatch()` сам направляет `GET`-запрос в метод `get(self, request)`, а `POST`-запрос — в `post(self, request)`. Готовые Generic-классы (`ListView`) позволяют вывести список объектов с пагинацией в 4 строчки кода.

```python
from django.http import HttpRequest, JsonResponse
from django.views import View

# 1. FBV (Функциональное представление)
def health_fbv(request: HttpRequest):
    return JsonResponse({"mode": "FBV", "ok": True})

# 2. CBV (Классовое представление)
class OrderCBV(View):
    def get(self, request: HttpRequest, order_id: int):
        return JsonResponse({"mode": "CBV", "order_id": order_id})

req = HttpRequest()
print("Ответ FBV:", health_fbv(req).json())
print("Ответ CBV.get():", OrderCBV().get(req, order_id=77).json())
```

---

## Шаблоны (`Templates`) и Формы (`Forms` / `ModelForm`) — Junior vs Senior

- **Антипаттерн Junior-разработчика**: читать пользовательский ввод напрямую из «сырого» словаря `request.POST['rating']`, забывать про CSRF-защиту и рендерить пользовательский HTML через фильтр `|safe` (открывая дыру для **XSS-атаки**).
- **Подход Senior-разработчика**:
  - **Шаблонизатор DTL (Django Template Language)** по умолчанию экранирует опасные HTML-символы (`<script>` превращается в безопасный `&lt;script&gt;`).
  - **Формы (`forms.Form` и `forms.ModelForm`)** валидируют типы и бизнес-ограничения. После вызова **`form.is_valid()`** проверенные данные берутся строго из словаря **`form.cleaned_data`**, а `ModelForm.save()` безопасно создаёт или обновляет запись в БД.

```python
from django import forms

class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=50)
    rating = forms.IntegerField()

form = FeedbackForm(data={"username": "alex", "rating": 5})
if form.is_valid():
    print("Форма валидна! Безопасные данные cleaned_data:", form.cleaned_data)
```
"""
    ),

    'К-084': (
        '3.2',
        'К-084. Django QuerySet_ ленивость и фильтрация.md',
        r"""📖 Перечитать конспект: Django ORM с нуля до профи: модели, миграции, ленивость QuerySet, Q и F выражения >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое Django ORM, Модели и Миграции с нуля

**ORM (Object-Relational Mapping)** — это переводчик между миром объектно-ориентированного Python и миром реляционных таблиц SQL.
- **Модель (`models.Model`)** — это Python-класс, который описывает одну таблицу в базе данных. Атрибуты класса (`CharField`, `IntegerField`, `ForeignKey`) становятся колонками таблицы, а каждый экземпляр класса — отдельной строкой в этой таблице.
- **Миграции (`Migrations`)** — это система контроля версий для схемы вашей базы данных:
  1. `python manage.py makemigrations` — анализирует изменения в `models.py` и генерирует файл-инструкцию (`0001_initial.py`). **Саму БД эта команда не трогает!**
  2. `python manage.py migrate` — читает файлы миграций и выполняет реальные SQL-команды `CREATE TABLE` / `ALTER TABLE` в базе данных.

---

## Главный секрет `QuerySet`: почему он ленивый (Lazy Evaluation)

Когда вы обращаетесь к таблице через менеджер `Article.objects.filter(status="published")`, вы получаете объект **`QuerySet`**.
Критически важное свойство: **`QuerySet` ленив (Lazy)**. Сама строка `.filter(...)` или `.order_by(...)` **вообще не обращается к базе данных** и не выполняет SQL! Она лишь конструирует SQL-запрос в памяти Python, позволяя вам выстраивать длинные цепочки условий.

Реальный SQL-запрос отправляется в базу данных **только в момент вычисления (Evaluation)** `QuerySet`:
1. При запуске цикла `for item in qs:`;
2. При преобразовании в список `list(qs)` или взятии среза с шагом;
3. При вызове терминальных методов: `.count()`, `.exists()`, `.first()`, `.get()`, `.aggregate()`.

```python
# Симуляция ленивого QuerySet: цепочка фильтров лишь копит условия до момента итерации
class LazyQuerySetDemo:
    def __init__(self, table: str, filters=None):
        self.table = table
        self.filters = list(filters or [])

    def filter(self, **kwargs):
        # Не делает SQL-запрос! Возвращает новый клон QuerySet с добавленными условиями
        return LazyQuerySetDemo(self.table, self.filters + [kwargs])

    def to_sql(self) -> str:
        conds = " AND ".join(f"{k}={v!r}" for f in self.filters for k, v in f.items())
        return f"SELECT * FROM {self.table}" + (f" WHERE {conds}" if conds else "")

qs = LazyQuerySetDemo("orders").filter(status="paid").filter(user_id=42)
print("Сконструированный единый SQL перед отправкой в БД:", qs.to_sql())
```

---

## Lookup-синтаксис фильтрации с двойным подчёркиванием (`__`)

В SQL для условий используют операторы `>`, `<=`, `LIKE`, `IN`, `IS NULL`, а также `JOIN` к соседним таблицам. В Django ORM всё это записывается через двойное подчёркивание **`__` (Field Lookups)**:

- `price__gt=1000` (`> 1000`), `price__gte=1000` (`>= 1000`), `price__lt=500` (`< 500`);
- `title__icontains="python"` — регистронезависимый поиск подстроки (`ILIKE '%python%'`);
- `status__in=["paid", "shipped"]` — проверка вхождения в список (`WHERE status IN (...)`);
- `deleted_at__isnull=True` — проверка на `IS NULL`;
- **Переход через связи (`JOIN` через `__`)**: `Order.objects.filter(user__email="alice@example.com")` — Django сам построит `INNER JOIN` к таблице `users` и отфильтрует заказы по `email` автора!

---

## Выражения `Q()`, `F()`, `annotate()` и сравнение Junior vs Senior

- **Антипаттерн Junior-разработчика**: проверять наличие записей через `if len(Order.objects.all()) > 0:` (выгружая миллион строк в память Python!) или уменьшать остаток товара через `product.stock -= 1; product.save()`, создавая состояние гонки (**Race Condition / Lost Update**).
- **Подход Senior-разработчика**:
  1. Проверять наличие через **`qs.exists()`** (`SELECT 1 ... LIMIT 1`), а количество — через **`qs.count()`** (`SELECT COUNT(*)`).
  2. Использовать **`Q()`** для сложных условий `OR` (`|`) / `NOT` (`~`) и **`F()`** для атомарных вычислений прямо внутри СУБД (`update(stock=F("stock") - 1)`).
  3. Использовать **`aggregate()`** для сводного итога по таблице и **`annotate()`** для расчёта `GROUP BY` на каждую строку.

```python
from django.db.models import F, Q, Count, Sum

q_expr = Q(status="paid") | Q(status="shipped")
f_expr = F("stock")
agg_res = Order.objects.aggregate(total_sum=Sum("amount"))
print("Результат aggregate():", agg_res, "| число заказов:", Order.objects.count())
```
"""
    ),

    'К-088': (
        '3.2',
        'К-088. Проблема N+1 и её решение в Django.md',
        r"""📖 Перечитать конспект: Проблема N+1 запросов в Django ORM и её решение: select_related и prefetch_related >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое проблема `N+1` запросов на пальцах (Junior vs Senior)

Проблема **`N+1` запросов** — главная причина тормозов бэкенда на собеседованиях и в продакшене.
Представьте, что у вас есть модель `Order` (Заказ), у которой есть внешний ключ `user = models.ForeignKey(User)` (Покупатель). Вы хотите вывести список из 100 заказов и рядом с каждым написать имя покупателя:

- **Ошибка Junior-разработчика**: загрузить список `orders = Order.objects.all()[:100]` и внутри цикла обращаться к `order.user.name`, провоцируя 100 дополнительных SQL-запросов к БД.
- **Подход Senior-разработчика**: заранее подгрузить связанные объекты за константное число запросов $O(1)$ через `select_related` (для `ForeignKey`/`OneToOne`) и `prefetch_related` (для `ManyToMany` и обратных коллекций).

```python
# ❌ КАК ПИШЕТ JUNIOR (порождает 1 + 100 = 101 запрос в базу данных!):
# Запрос №1: SELECT * FROM orders LIMIT 100;
# А затем на КАЖДОЙ итерации цикла обращение order.user делает отдельный SQL-запрос!
def simulate_n_plus_1(orders_count: int) -> int:
    sql_queries = ["SELECT * FROM orders;"]
    for i in range(1, orders_count + 1):
        sql_queries.append(f"SELECT * FROM users WHERE id = {i};")
    return len(sql_queries)

print("Количество SQL-запросов без оптимизации (для 100 заказов):", simulate_n_plus_1(100))
```

Если один сетевой поход в базу данных занимает всего 2 мс, то 101 последовательный запрос займёт уже **202 мс**, а для 1000 строк — **2 секунды** на один HTTP-запрос!

---

## Два оружия против `N+1`: `select_related` против `prefetch_related`

В Django ORM проблема `N+1` решается двумя методами предзагрузки связанных данных. Очень важно чётко понимать, чем они отличаются под капотом:

| Метод | Для каких связей используется | Как работает на уровне SQL и памяти | Сколько запросов |
| :--- | :--- | :--- | :--- |
| **`select_related('user')`** | Прямые одиночные связи: **`ForeignKey`** и **`OneToOneField`** | Выполняет **`SQL JOIN`** (`LEFT OUTER JOIN`) и забирает и заказы, и их авторов за **1 объединённый запрос** | **1 запрос** |
| **`prefetch_related('items')`** | Множественные и обратные связи: **`ManyToManyField`** и обратный `ForeignKey` (`user.orders`) | Выполняет **2 отдельных запроса**: сначала берёт заказы, а вторым запросом `SELECT ... WHERE order_id IN (1, 2, ...)` забирает все связанные позиции и **склеивает их в памяти Python** | **2 запроса** (вместо `N+1`) |

Почему нельзя использовать `SQL JOIN` (`select_related`) для связи «многие-ко-многим»?
Потому что если у 100 заказов по 20 товаров и по 5 тегов, то `SQL JOIN` создаст **декартово произведение** на `100 * 20 * 5 = 10 000` дублирующихся строк, перегрузив сеть и память! Поэтому `prefetch_related` делает аккуратный второй запрос через `WHERE IN` и связывает списки в Python.

```python
# ✅ КАК ПИШЕТ SENIOR (всего 1 или 2 запроса независимо от размера выборки!):
optimized_orders = (
    Order.objects
    .select_related("author")        # SQL JOIN для одиночного ForeignKey
    .prefetch_related("orders")      # Второй запрос WHERE IN для коллекции
    .all()
)
first_order = optimized_orders[0]
print("Оптимизированный заказ загружен за O(1) запросов, автор:", first_order.author.name)
```

---

## Продвинутый уровень: объект `Prefetch()` и `.only()` / `.values()`

- Что если при вызове `prefetch_related('comments')` нам нужны не все комментарии к статье, а только **одобренные** (`is_approved=True`)? Если написать внутри шаблона или цикла `article.comments.filter(is_approved=True)`, Django **сбросит предзагруженный кэш** и снова устроит `N+1`!
- Решение — класс **`Prefetch`**:
  `Article.objects.prefetch_related(Prefetch("comments", queryset=Comment.objects.filter(is_approved=True)))`.
"""
    ),

    'К-087': (
        '3.2',
        'К-087. Жизненный цикл запроса в Django.md',
        r"""📖 Перечитать конспект: Жизненный цикл HTTP-запроса в Django: от Nginx и WSGI/ASGI до ответа >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Часть 1. Внешний периметр: от браузера через `Nginx` к `Gunicorn` / `Uvicorn`

Один из любимых вопросов на собеседованиях по Django: *«Что происходит шаг за шагом, когда пользователь вводит URL сайта и нажимает Enter?»*
Начнём с границы вашей серверной инфраструктуры:

1. **Веб-сервер / Reverse Proxy (`Nginx`)**:
   Почему Gunicorn не выставляют напрямую в интернет? Потому что Python-воркеры плохо справляются с медленными клиентами (атака *Slowloris*) и раздачей файлов. `Nginx` принимает внешнее HTTPS-соединение, расшифровывает TLS, **напрямую с диска раздаёт статику (`/static/`, `/media/`)**, буферизует запрос и мгновенно передаёт его по локальному сокету в сервер приложений.
2. **Сервер приложений (`Gunicorn` для WSGI или `Uvicorn` для ASGI)**:
   Управляет пулом рабочих Python-процессов (`workers`), читает HTTP-запрос и вызывает точку входа Django (`WSGIHandler` в `wsgi.py` или `ASGIHandler` в `asgi.py`), создавая объект **`HttpRequest`**.

---

## Часть 2. Внутренний конвейер Django: Middleware ➔ URLconf ➔ View ➔ ORM

Когда объект `HttpRequest` создан внутри Django, он проходит следующие этапы:

3. **Прямой проход через `Middleware` (сверху вниз)**: запрос проходит сквозь слои промежуточного ПО из списка `MIDDLEWARE` в `settings.py` (`SecurityMiddleware` ➔ `SessionMiddleware` ➔ `CommonMiddleware` ➔ `CsrfViewMiddleware` ➔ `AuthenticationMiddleware`, который прикрепляет `request.user`). Если любой слой вернёт `HttpResponse` (короткое замыкание — например, `403 Forbidden` при ошибке CSRF), дальше запрос не пойдёт.
4. **Маршрутизатор (`URL Resolver` / `urls.py`)**: сверяет `request.path` с таблицей `urlpatterns` сверху вниз, извлекает параметры пути (`pk=42`) и находит нужный `View` (иначе выбрасывает `Http404`).
5. **Представление (`View`), валидация и `Django ORM`**: вызывается `View` (в CBV сначала `dispatch()`). Проверяются права доступа, валидируются формы/сериализаторы, а при вычислении `QuerySet` ORM отправляет SQL-запрос в **PostgreSQL**.
6. **Обратный проход через `Middleware` (снизу вверх)**: сформированный `HttpResponse` проходит слои `Middleware` в обратном порядке (сохраняется сессия в `SessionMiddleware`, добавляются заголовки безопасности и `Content-Length`) и уходит клиенту.

```python
def trace_django_request_lifecycle(path: str, csrf_valid: bool = True) -> list[str]:
    steps = ["1. [Nginx -> Gunicorn] Создан объект HttpRequest"]
    steps.append("2. [Middleware IN] Security -> Session -> Csrf -> Auth (request.user)")
    if not csrf_valid:
        steps.append("3. [CsrfViewMiddleware] Короткое замыкание: 403 Forbidden!")
        return steps
    steps.append(f"3. [URLDispatcher] Маршрут {path!r} сопоставлен с OrderDetailView")
    steps.append("4. [View -> ORM] SELECT * FROM orders WHERE id = 42")
    steps.append("5. [Template/JSON] Сформирован объект HttpResponse (200 OK)")
    steps.append("6. [Middleware OUT] Auth -> Csrf -> Session (Set-Cookie) -> Security")
    return steps

for line in trace_django_request_lifecycle("/orders/42/"):
    print(line)
```

---

## Часть 3. Обработка исключений в конвейере и сравнение Junior vs Senior

- **Антипаттерн Junior-разработчика**: запускать `python manage.py runserver` в продакшене, раздавать медиафайлы через Python-процессы Django и вручную ловить `ObjectDoesNotExist` с возвратом `HttpResponse(status=404)` в каждом методе вместо `get_object_or_404()`.
- **Подход Senior-разработчика**: ставить `Nginx` перед `Gunicorn`/`Uvicorn`, использовать стандартные исключения `Http404` и `PermissionDenied` (которые Django сам перехватывает внутри `BaseHandler` и превращает в ответы `404`/`403`), а для API настраивать единый обработчик ошибок.

```python
def simulate_csrf_short_circuit():
    blocked_trace = trace_django_request_lifecycle("/orders/create/", csrf_valid=False)
    print("Путь запроса при невалидном CSRF-токене:", " -> ".join(blocked_trace))

simulate_csrf_short_circuit()
```
"""
    ),

    'К-086': (
        '3.2',
        'К-086. Middleware в Django_ обработка запросов.md',
        r"""📖 Перечитать конспект: Middleware в Django: устройство конвейера и написание собственных слоёв >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое Middleware в Django и зачем он нужен

**Middleware (промежуточный слой)** в Django — это легковесный плагин, который оборачивает обработку **каждого** запроса и ответа в приложении.
Если вам нужно выполнить действие только на одном маршруте — используйте декоратор (например, `@login_required`). Но если логика должна работать сквозным образом для **всего сайта** (аутентификация сессий, защита от CSRF, замер времени выполнения запросов, логирование `X-Request-ID`, проверка блокировки IP) — это задача для **Middleware**.

---

## Порядок слоёв в `settings.MIDDLEWARE` (Junior vs Senior)

Список `MIDDLEWARE` в `settings.py` работает по модели «луковицы» (**Onion Model**):
- При **входе запроса** (`HttpRequest`) слои выполняются **сверху вниз** (от нулевого индекса к последнему).
- При **выходе ответа** (`HttpResponse`) слои выполняются в **обратном порядке — снизу вверх**.

- **Ошибка Junior-разработчика**: добавлять новый Middleware в случайное место списка (например, ставить кастомный слой проверки ролей `request.user` выше `AuthenticationMiddleware`, из-за чего `request.user` ещё не существует!) или делать тяжёлые синхронные SQL-запросы внутри каждого Middleware.
- **Подход Senior-разработчика**: строго соблюдать зависимости между слоями (`SecurityMiddleware` ➔ `SessionMiddleware` ➔ `AuthenticationMiddleware`) и держать код Middleware максимально быстрым.

---

## Как написать собственный Middleware в современном Django

В современном Django Middleware пишется как класс с двумя методами:
1. **`__init__(self, get_response)`** — вызывается **один раз** при старте веб-сервера. Сохраняет ссылку `self.get_response` на следующий слой в цепочке.
2. **`__call__(self, request)`** — вызывается **на каждый HTTP-запрос**:
   - код **до** `response = self.get_response(request)` выполняется на пути к `View`;
   - код **после** `self.get_response(request)` модифицирует готовый ответ на обратном пути.

Дополнительно класс может определять специальные хуки: `process_view(request, view_func, view_args, view_kwargs)` (вызывается после URL-роутера прямо перед входом в `View`) и `process_exception(request, exception)` (перехватывает необработанные исключения из `View`).

```python
import time

class RequestTimingMiddleware:
    def __init__(self, get_response):
        # Инициализируется один раз при старте процесса
        self.get_response = get_response

    def __call__(self, request: dict) -> dict:
        # 1. Прямой ход (до вызова View)
        t0 = time.perf_counter()
        request["request_id"] = "req-777"

        # Передача управления следующему слою или View
        response = self.get_response(request)

        # 2. Обратный ход (после получения ответа от View)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        response.setdefault("headers", {})["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
        response["headers"]["X-Request-ID"] = request["request_id"]
        return response

def sample_view(req: dict) -> dict:
    return {"status": 200, "body": f"Привет, запрос {req['request_id']}", "headers": {}}

mw = RequestTimingMiddleware(sample_view)
result = mw({"path": "/api/items/"})
print("Ответ после прохождения Middleware:", result)
```
"""
    ),

    'К-085': (
        '3.2',
        'К-085. Django Admin_ архитектура и настройка.md',
        r"""📖 Перечитать конспект: Архитектура и тонкая настройка Django Admin: ModelAdmin, Inlines и оптимизация >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Зачем нужен `Django Admin` и почему бизнес его обожает

В любом стартапе или крупном продукте помимо клиентского сайта нужен внутренний интерфейс (**Back-office / Админка**) для модераторов, службы поддержки и контент-менеджеров: посмотреть заказы, сменить статус доставки, заблокировать спамера.
В других фреймворках на разработку такой админки уходят недели работы фронтенда и бэкенда. В Django модуль **`django.contrib.admin`** читает метаданные ваших моделей ORM и **автоматически генерирует полноценный CRUD-интерфейс** за 5 минут!

---

## Настройка класса `ModelAdmin`: основные атрибуты (Junior vs Senior)

Чтобы тонко настроить отображение таблицы в админке, в файле `admin.py` создают подкласс `admin.ModelAdmin` и регистрируют его декоратором `@admin.register(Order)`:

- **`list_display = ("id", "user", "status", "total_price", "created_at")`** — какие колонки показывать в общей таблице записей.
- **`list_filter = ("status", "created_at")`** — добавляет боковую панель быстрых фильтров справа.
- **`search_fields = ("=id", "user__email", "title")`** — включает строку поиска (префикс `=` делает точный поиск `=`, `^` — поиск с начала строки `LIKE 'abc%'`, без префикса — `ILIKE '%abc%'`).
- **`readonly_fields = ("created_at", "updated_at")`** — запрещает редактировать вычисляемые или аудит-поля.
- **Junior vs Senior на больших таблицах**:
  - **Ошибка Junior-разработчика**: оставить стандартный `admin.site.register(Order)` для таблицы с 500 000 пользователей в `ForeignKey`. При открытии заказа Django попытается отрендерить `<select>` на 500 000 `<option>` и положит сервер по памяти!
  - **Подход Senior-разработчика**: всегда включать **`autocomplete_fields = ("user",)`** (или `raw_id_fields`) и **`list_select_related = ("user",)`**.

---

## Вложенное редактирование (`TabularInline`) и защита админки от `N+1`

Если у заказа (`Order`) есть связанные позиции (`OrderItem`), менеджеру неудобно создавать их на разных страницах. Классы **`admin.TabularInline`** (компактная таблица) и **`admin.StackedInline`** позволяют редактировать дочерние записи прямо внутри карточки родительского заказа!

А если в `list_display` вы выводите поле из связанной модели (`order.user.email`), админка по умолчанию сделает `N+1` запрос на каждую строчку таблицы. Чтобы устранить `N+1` в админке, обязательно указывайте **`list_select_related = ("user",)`** или переопределяйте метод `get_queryset(self, request)`.

```python
from django.contrib import admin

class OrderItemInline(admin.TabularInline):
    model = Order
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author")
    list_filter = ("title",)
    search_fields = ("=id", "title", "author__email")
    list_select_related = ("author",)
    inlines = [OrderItemInline]

    @admin.action(description="Пометить выбранные заказы как доставленные")
    def mark_delivered(self, request, queryset):
        # Массовое обновление одним SQL UPDATE без цикла по объектам!
        updated = queryset.update(status="delivered")
        return updated

admin_instance = OrderAdmin()
print("Настроен OrderAdmin: колонки =", admin_instance.list_display, "| select_related =", admin_instance.list_select_related)
```
"""
    ),

    'К-081': (
        '3.2',
        'К-081. Сигналы Django и паттерн Pub_Sub.md',
        r"""📖 Перечитать конспект: Сигналы в Django: паттерн Observer (Pub/Sub), встроенные сигналы и подводные камни >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое Сигналы (Signals) и паттерн Pub/Sub на пальцах

В архитектуре ПО часто возникает задача: когда в модуле `users` создаётся новый пользователь, нужно автоматически создать для него бонусный счёт в модуле `loyalty` и отправить приветственное письмо.
Если импортировать функции модуля `loyalty` прямо внутрь `models.py` модуля `users`, модули станут жёстко связаны (**Tight Coupling**) и быстро приведут к циклическим импортам (`ImportError`).

**Сигналы Django (`django.dispatch`)** реализуют паттерн **Наблюдатель / Издатель-Подписчик (Observer / Pub-Sub)** внутри одного процесса:
- **Издатель (`Sender`)** просто кричит в эфир: *«Запись пользователя сохранена!»* (`post_save`), не зная, кто его слушает.
- **Подписчики (`Receivers`)** подписываются на это событие через декоратор **`@receiver(post_save, sender=User)`** и выполняют свою реакцию.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

audit_log = []

@receiver(post_save, sender=User)
def create_user_profile_receiver(sender, instance, created: bool, **kwargs):
    if created:
        audit_log.append(f"Создан профиль для нового пользователя: {instance.username}")

# Симулируем отправку сигнала после сохранения нового пользователя
fake_user = User(username="dmitry")
post_save.send(sender=User, instance=fake_user, created=True)
print("Лог срабатывания сигнала post_save:", audit_log)
```

---

## Главные встроенные сигналы Django и где их регистрировать

- `pre_save` / `post_save` — срабатывают до и после вызова метода `model.save()` (параметр `created=True` отличает `INSERT` от `UPDATE`).
- `pre_delete` / `post_delete` — до и после удаления объекта.
- `m2m_changed` — при изменении связей `ManyToManyField`.
- `user_logged_in` / `user_login_failed` — события входа в систему.

**Где подключать сигналы**: обработчики выносят в файл `signals.py` и обязательно импортируют его внутри метода **`ready(self)`** класса `AppConfig` в `apps.py`, чтобы подписка зарегистрировалась при старте Django.

---

## Важнейшие ловушки сигналов (Junior vs Senior)

На собеседованиях очень любят спрашивать: *«Почему Senior Django-разработчики избегают сигналов для основной бизнес-логики, где Junior использует их повсюду?»*

1. **Сигналы в Django работают СИНХРОННО и блокируют запрос!**
   - **Заблуждение Junior**: думать, что сигналы выполняются в фоне. На самом деле `post_save` выполняется в том же самом потоке и внутри той же транзакции БД. Если ваш сигнал отправляет письмо по SMTP 3 секунды, пользователь будет ждать ответа 3 секунды.
2. **Массовый `QuerySet.update()` НЕ вызывает сигналы `pre_save`/`post_save`!**
   Вызов `Order.objects.filter(status="new").update(status="cancelled")` выполняется одним SQL-запросом напрямую в БД, минуя метод `.save()` и все ваши сигналы!
3. **Подход Senior (`transaction.on_commit` и явные сервисы)**:
   Если внутри `post_save` вы отправили задачу в Celery, а секунду спустя транзакция БД откатилась (`ROLLBACK`), воркер получит задачу для несуществующей записи! Поэтому любые внешние вызовы оборачивают в **`transaction.on_commit(lambda: send_email_task.delay(user.id))`**, а явную бизнес-логику пишут в сервисном слое `services.py`.
"""
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.3 · ЧАСТЬ III: ФРЕЙМВОРК DJANGO REST FRAMEWORK (DRF)
    # ═══════════════════════════════════════════════════════════════════════════
    'К-091': (
        '3.3',
        'К-091. Django REST Framework_ от модели до API.md',
        r"""📖 Перечитать конспект: Основы Django REST Framework (DRF) с нуля: архитектура сериализаторов и валидация >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Зачем нужен DRF поверх Django (Ментальная модель с нуля)

Классический Django создавался в эпоху, когда сервер сам возвращал готовые HTML-страницы (`render(request, "index.html")`).
В современной разработке фронтенд на React/Vue, мобильные приложения на iOS/Android и внешние интеграции общаются с бэкендом на языке **JSON по протоколу REST API**.
**Django REST Framework (DRF)** — это промышленная надстройка над Django, которая превращает модели Django ORM в полноценный JSON API с валидацией, правами доступа, пагинацией и автодокументацией.

---

## Сердце DRF: что такое Сериализатор (`Serializer` и `ModelSerializer`)

Модель Django (`Order`) — это сложный Python-объект, связанный с базой данных, полями `Decimal`, `datetime` и внешними ключами. Его нельзя просто передать в `json.dumps()` — возникнет `TypeError: Object of type Order is not JSON serializable`.

**Сериализатор (`Serializer`)** в DRF работает как двусторонний таможенный терминал:
1. **Сериализация (Из Python/ORM ➔ в JSON на выход)**: берёт объект модели или `QuerySet` (`OrderSerializer(orders, many=True)`) и превращает его в словарь примитивных типов Python (`serializer.data`), готовый к отправке в JSON.
2. **Десериализация и валидация (Из входящего JSON ➔ в БД)**: принимает сырой словарь от клиента (`OrderSerializer(data=request.data)`), проверяет все бизнес-правила при вызове **`.is_valid(raise_exception=True)`** и сохраняет запись через **`.save()`** (который под капотом вызывает метод `create(validated_data)` для новой записи или `update(instance, validated_data)` для существующей).

```python
# Наглядная работа сериализатора DRF на чтение и запись:
class ProductSerializerDemo:
    def __init__(self, instance=None, data=None):
        self.instance = instance
        self.initial_data = data
        self.validated_data = {}
        self.errors = {}

    def is_valid(self, raise_exception: bool = False) -> bool:
        self.errors = {}
        title = str(self.initial_data.get("title", "")).strip()
        price = self.initial_data.get("price", 0)
        if len(title) < 3:
            self.errors["title"] = ["Название должно быть не короче 3 символов."]
        if not isinstance(price, (int, float)) or price <= 0:
            self.errors["price"] = ["Цена должна быть положительным числом."]
        if self.errors:
            if raise_exception:
                raise ValueError(f"400 Bad Request: {self.errors}")
            return False
        self.validated_data = {"title": title, "price": float(price)}
        return True

ser = ProductSerializerDemo(data={"title": "Ноутбук Pro", "price": 120000})
print("Валидация успешна:", ser.is_valid(), "| validated_data:", ser.validated_data)
```

---

## Тонкая настройка полей: `read_only`, `write_only`, `SerializerMethodField`

В `serializers.ModelSerializer` поля автоматически генерируются по модели из `class Meta: model = ...; fields = [...]`. Как управлять их поведением?

- **`read_only_fields = ("id", "created_at", "author")`** — эти поля отдаются клиенту в JSON-ответе, но **игнорируются при входящем `POST/PUT/PATCH`** (чтобы клиент не мог сам подделать свой `id` или дату создания).
- **`extra_kwargs = {"password": {"write_only": True}}`** — поле `password` принимается при регистрации, но **никогда не включается в исходящий JSON-ответ**!
- **`SerializerMethodField()`** — вычисляемое на лету поле только для чтения. По умолчанию вызывает метод `get_<имя_поля>(self, obj)`.

---

## Трёхступенчатый конвейер валидации в DRF (`is_valid`)

Когда вы вызываете `serializer.is_valid()`, DRF проверяет данные строго в три этапа:

1. **Встроенная валидация типов и ограничений полей**: проверка `max_length`, `min_value`, `required`, валидаторов модели.
2. **Валидация отдельного поля — метод `validate_<field_name>(self, value)`**: вызывается для конкретного поля (например, `def validate_price(self, value):`). Обязан вернуть очищенное значение `value` или выбросить `serializers.ValidationError("...")`.
3. **Перекрёстная валидация нескольких полей — метод `validate(self, attrs)`**: получает словарь всех полей `attrs` и проверяет связи между ними (например, что дата выезда `check_out` позже даты заезда `check_in`).

```python
from rest_framework import serializers

class BookingSerializer(serializers.ModelSerializer):
    days_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "title", "days_count"]
        read_only_fields = ["id"]

    def get_days_count(self, obj) -> int:
        return 7

    def validate_title(self, value: str) -> str:
        if "spam" in value.lower():
            raise serializers.ValidationError("Запрещённое слово в названии")
        return value.strip()

    def validate(self, attrs: dict) -> dict:
        return attrs

bs = BookingSerializer()
print("Проверка validate_title('Чистый заказ'):", bs.validate_title(" Чистый заказ "))
print("Вычисляемое поле get_days_count:", bs.get_days_count(order_instance))
```

> **Junior vs Senior**:
> - **Junior**: Пишет в `ModelSerializer` настройку `fields = "__all__"` и проверяет входные поля через `if not request.data.get(...)` прямо внутри `APIView`. При добавлении в модель служебного поля `internal_margin` или `password_hash` оно мгновенно утекает наружу в JSON.
> - **Senior**: Явно перечисляет белый список полей в `fields = [...]`, помечает служебные поля через `read_only_fields` и `write_only=True`, использует `serializer.is_valid(raise_exception=True)`, а бизнес-инварианты проверяет в `validate_<field>` и `validate(self, attrs)`.
"""
    ),

    'К-237': (
        '3.3',
        'К-237. Представления и маршрутизация в DRF с нуля_ APIView, GenericAPIView, Mixins, ModelViewSet, @action и Routers.md',
        r"""📖 Перечитать конспект: Представления и маршрутизация в DRF с нуля: от APIView и Generics до ModelViewSet, @action и Routers >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Эволюция представлений (Views) в DRF: 4 уровня абстракции

Новичкам в Django REST Framework часто кажется запутанным обилие классов: `@api_view`, `APIView`, `GenericAPIView`, `ListCreateAPIView`, `ViewSet`, `ModelViewSet`. Зачем их так много?
На самом деле это **лестница от полного ручного контроля к полной автоматизации стандартного CRUD**. Разберём каждую ступень по порядку!

### Уровень 1. `@api_view` и `APIView` — полный ручной контроль
Базовый класс **`APIView`** (и декоратор `@api_view(["GET", "POST"])` для функций) — это фундамент DRF. Чем он отличается от обычного `django.views.View`?
- Вместо сырого `HttpRequest` в метод приходит **`rest_framework.request.Request`**, у которого есть единое свойство **`request.data`** (автоматически парсит JSON, FormData и Multipart для `POST`, `PUT`, `PATCH`) и **`request.query_params`** (вместо `request.GET`).
- Вместо `HttpResponse` возвращается **`Response(data, status=...)`**, который сам договаривается с клиентом о формате (`Content Negotiation`: отдаёт JSON или удобную HTML-песочницу Browsable API в браузере).
- Перед входом в метод `get()` или `post()` автоматически выполняются проверки **аутентификации**, **прав доступа (`Permissions`)** и **ограничения частоты (`Throttling`)**.

### Уровень 2. `GenericAPIView` + `Mixins` — кирпичики для таблиц БД
Когда мы работаем с моделями БД, код в `APIView` начинает повторяться. **`GenericAPIView`** добавляет два стандартных атрибута: `queryset = Order.objects.all()` и `serializer_class = OrderSerializer` (а также пагинацию и фильтрацию), а классы-примеси (**Mixins**: `ListModelMixin`, `CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin`) реализуют стандартные действия `.list()`, `.create()`, `.retrieve()`, `.update()`, `.destroy()`.

### Уровень 3. Готовые `Concrete Generic Views` (`ListCreateAPIView` и др.)
Чтобы не склеивать `GenericAPIView` и миксины вручную, DRF даёт готовые комбинированные классы в `rest_framework.generics`:
- **`ListAPIView`** (`GET` списка), **`CreateAPIView`** (`POST`), **`ListCreateAPIView`** (`GET` + `POST`);
- **`RetrieveAPIView`** (`GET /{id}`), **`UpdateAPIView`** (`PUT/PATCH /{id}`), **`DestroyAPIView`** (`DELETE /{id}`), **`RetrieveUpdateDestroyAPIView`** (`GET/PUT/PATCH/DELETE /{id}`).

### Уровень 4. `ModelViewSet` + `DefaultRouter` — весь CRUD в 5 строк кода
Если у ресурса стандартный набор операций (список, создание, чтение по ID, обновление, удаление), вместо двух разных классов (`ListCreateAPIView` для `/orders/` и `RetrieveUpdateDestroyAPIView` для `/orders/{id}/`) используют **`ModelViewSet`** (или **`ReadOnlyModelViewSet`**, если нужны только `list` и `retrieve`).

В отличие от `APIView`, у `ViewSet` методы называются не по HTTP-глаголам (`get`, `post`), а по **действиям (`actions`)**:
- `GET /orders/` ➔ `list()`
- `POST /orders/` ➔ `create()`
- `GET /orders/{pk}/` ➔ `retrieve()`
- `PUT /orders/{pk}/` ➔ `update()`
- `PATCH /orders/{pk}/` ➔ `partial_update()`
- `DELETE /orders/{pk}/` ➔ `destroy()`

---

## Динамический `get_queryset()` и `get_serializer_class()` во ViewSet

В реальном продакшене редко оставляют статический `queryset = Order.objects.all()`. Почему?
1. Пользователь должен видеть **только свои собственные заказы** (или нужно подгрузить связи через `select_related` в зависимости от действия). Для этого переопределяют метод **`get_queryset(self)`**!
2. Для списка заказов нужна компактная схема `OrderListSerializer`, а при создании (`action == 'create'`) — схема `OrderCreateSerializer`. Для этого переопределяют метод **`get_serializer_class(self)`**!
3. Чтобы при создании заказа автоматически проставить текущего автора `user=self.request.user`, переопределяют хук **`perform_create(self, serializer)`** (`serializer.save(user=self.request.user)`).

---

## Кастомные эндпоинты через декоратор `@action` и маршрутизация `DefaultRouter`

Что делать, если помимо стандартного CRUD в `OrderViewSet` нужен бизнес-эндпоинт `POST /orders/42/cancel/` (отменить конкретный заказ) или `GET /orders/recent/` (последние заказы)?
Для этого используется декоратор **`@action`**:
- **`detail=True`** — маршрут действует на **один конкретный объект** и включает `{pk}`: `/orders/{pk}/cancel/`.
- **`detail=False`** — маршрут действует на **всю коллекцию** без `{pk}`: `/orders/recent/`.

А **`DefaultRouter`** автоматически регистрирует все маршруты `ViewSet` (включая все `@action`) и создаёт корневую страницу API:

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.routers import DefaultRouter

class OrderViewSetDemo(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # Безопасная фильтрация + оптимизация N+1
        return Order.objects.select_related("author").all()

    def get_serializer_class(self):
        if getattr(self, "action", "list") == "create":
            return ArticleSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_order(self, request, pk=None):
        return {"id": pk, "status": "cancelled_by_action"}

router = DefaultRouter()
router.register(r"orders", OrderViewSetDemo, basename="order")

vs = OrderViewSetDemo()
print("Кастомный @action cancel_order вызван успешно:", vs.cancel_order(request=None, pk=42))
```

> **Junior vs Senior**:
> - **Junior**: Переопределяет метод `create(self, request)` целиком в `ModelViewSet`, копируя 20 строк шаблонного кода ради того, чтобы подставить `author = request.user`, или создаёт отдельный `APIView` для каждого бизнес-действия над заказом.
> - **Senior**: Использует лаконичный хук `perform_create(self, serializer)` (`serializer.save(author=self.request.user)`), разделяет сериализаторы чтения и записи через `get_serializer_class()`, а предметные операции (`cancel`, `pay`) оформляет через `@action(detail=True, methods=['post'])`.
"""
    ),

    'К-238': (
        '3.3',
        'К-238. Безопасность, фильтрация и документация в DRF_ Authentication, Permissions, django-filter, Pagination, Throttling и drf-spectacular.md',
        r"""📖 Перечитать конспект: Безопасность, фильтрация и документация в DRF: Authentication, Permissions, django-filter, Pagination, Throttling и drf-spectacular >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Аутентификация (`Authentication`) против Разрешений (`Permissions`) в DRF

В каждом запросе к `APIView` или `ViewSet` перед вызовом бизнес-логики DRF последовательно запускает два независимых механизма:

1. **`authentication_classes` (Кто ты?)**:
   Проверяет учётные данные в запросе (сессионную куку в `SessionAuthentication`, постоянный токен в `TokenAuthentication` или JWT-токен через библиотеку **`djangorestframework-simplejwt`** в `JWTAuthentication`).
   По итогам аутентификации DRF заполняет два свойства:
   - **`request.user`** — экземпляр модели `User` (или `AnonymousUser`, если токен не передан);
   - **`request.auth`** — сам декодированный токен (например, словарь клеймов JWT).
2. **`permission_classes` (Имеешь ли ты право на это действие?)**:
   Получает уже заполненный `request.user` и решает, пустить запрос дальше (`True`) или вернуть `401 Unauthorized` / `403 Forbidden` (`False`).

---

## Двухуровневая защита в `BasePermission`: `has_permission` vs `has_object_permission`

Это один из самых частых вопросов по DRF на техническом собеседовании!
Когда вы создаёте собственный класс прав доступа (наследуясь от `permissions.BasePermission`), у него есть два метода:

| Метод в `BasePermission` | Когда вызывается | За что отвечает и где работает |
| :--- | :--- | :--- |
| **`has_permission(self, request, view)`** | На **самом входе** в любой эндпоинт (до обращения к БД за конкретным объектом) | Общая проверка доступа к маршруту (например, авторизован ли пользователь, есть ли у него роль модератора) |
| **`has_object_permission(self, request, view, obj)`** | Только тогда, когда метод **`get_object()`** уже загрузил конкретную запись `obj` из БД (в `retrieve`, `update`, `partial_update`, `destroy`) | Проверка **владения конкретным ресурсом** (защита от уязвимости **BOLA / IDOR**): например, `obj.author_id == request.user.id` |

> **Критическая тонкость DRF**:
> 1. Для списковых маршрутов (`list` — `GET /orders/`) и создания (`create` — `POST /orders/`) метод `has_object_permission` **НЕ вызывается**! Ограничивать список чужих объектов нужно через фильтрацию в `get_queryset()`.
> 2. Если вы написали кастомный метод во `ViewSet` через `@action(detail=True)` и загрузили объект вручную через `Order.objects.get(pk=pk)`, вы **обязаны вызвать `self.get_object()`** (он сам внутри вызывает `self.check_object_permissions(request, obj)`), иначе `has_object_permission` будет пропущен!

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        # Чтение разрешено всем, а изменение — только авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(getattr(request, "user", None) and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)

perm = IsOwnerOrReadOnly()
from types import SimpleNamespace
req_owner = SimpleNamespace(method="PATCH", user=SimpleNamespace(id=10, is_authenticated=True))
req_hacker = SimpleNamespace(method="PATCH", user=SimpleNamespace(id=99, is_authenticated=True))
article_obj = SimpleNamespace(id=500, owner_id=10)

print("Владелец редактирует свою статью:", perm.has_object_permission(req_owner, None, article_obj))
print("Чужой пользователь пытается изменить статью (защита от IDOR):", perm.has_object_permission(req_hacker, None, article_obj))
```

---

## Фильтрация, поиск и сортировка (`django-filter`, `SearchFilter`, `OrderingFilter`)

Чтобы фронтенд мог запрашивать `/api/products/?category=laptops&min_price=50000&search=macbook&ordering=-price`, в DRF подключают три бэкенда фильтрации (`filter_backends`):
1. **`DjangoFilterBackend`** (библиотека `django-filter`) — точная фильтрация по полям (`filterset_fields = ["category", "status"]`) или кастомный класс `FilterSet` с диапазонами `gte`/`lte`.
2. **`SearchFilter`** — текстовый поиск по нескольким полям (`search_fields = ["title", "description"]` по параметру `?search=...`).
3. **`OrderingFilter`** — безопасная сортировка по разрешённым колонкам (`ordering_fields = ["price", "created_at"]` по параметру `?ordering=-price`).

---

## Пагинация, Throttling и автодокументация `drf-spectacular`

- **Три класса пагинации в DRF**:
  1. `PageNumberPagination` (`?page=2&page_size=20`) — классическая постраничная навигация для веб-таблиц.
  2. `LimitOffsetPagination` (`?limit=20&offset=40`) — смещение и лимит.
  3. **`CursorPagination`** (`?cursor=cD0yMDI...`) — курсорная пагинация по индексу времени/ID без `OFFSET`. Идеальна для бесконечных лент и огромных таблиц!
- **Ограничение частоты (`Throttling`)**: `AnonRateThrottle` (лимит по IP для гостей, например `20/minute`), `UserRateThrottle` (лимит для авторизованных пользователей, например `1000/day`) и `ScopedRateThrottle` (строгий лимит для конкретных чувствительных эндпоинтов вроде отправки СМС).
- **Генерация OpenAPI 3.0 (`drf-spectacular`)**: стандарт де-факто для автодокументации Swagger/ReDoc в современном DRF. Декоратор **`@extend_schema(summary=..., request=..., responses={200: ...})`** позволяет точно задокументировать схемы входа, выхода и query-параметров любого эндпоинта.

> **Junior vs Senior**:
> - **Junior**: В кастомном `@action(detail=True)` достаёт запись через `Order.objects.get(pk=pk)` (пропуская `has_object_permission` и открывая уязвимость IDOR!), а фильтрацию пишет вручную через `request.query_params.get(...)` с риском ошибок типов.
> - **Senior**: Всегда получает объект во `ViewSet` через `self.get_object()`, сочетает `has_object_permission` с фильтрацией в `get_queryset()`, использует декларативный `FilterSet` (`django-filter`), `CursorPagination` на больших таблицах и документирует схемы через `@extend_schema` из `drf-spectacular`.
"""
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.4 · ЧАСТЬ IV: МИКРОФРЕЙМВОРК FLASK
    # ═══════════════════════════════════════════════════════════════════════════
    'К-095': (
        '3.4',
        'К-095. Flask базово_ маршруты, request,.md',
        r"""📖 Перечитать конспект: Введение во Flask с нуля: философия микрофреймворка, маршруты, request, jsonify и обработка ошибок >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое микрофреймворк Flask и на чём он построен

Слово **«микрофреймворк»** в названии **Flask** вовсе не означает, что он подходит только для крошечных учебных проектов. Оно означает, что **ядро Flask намеренно оставлено минималистичным**: Flask не навязывает вам конкретную базу данных, ORM или форму авторизации.

Под капотом Flask опирается на два проверенных временем компонента:
1. **`Werkzeug`** — инструментарий протокола **WSGI** (маршрутизация URL, разбор HTTP-заголовков, объекты `Request` и `Response`, интерактивный отладчик).
2. **`Jinja2`** — быстрый и безопасный шаблонизатор HTML с автоэкранированием от XSS.

---

## Маршруты (`@app.route` / `@app.get` / `@app.post`) и конвертеры URL

Минимальное приложение Flask создаётся одной строкой `app = Flask(__name__)`.
Для привязки URL к функции используют декоратор `@app.route("/users/<int:user_id>", methods=["GET"])` или современные сокращения Flask 2.0+: **`@app.get(...)`**, **`@app.post(...)`**, **`@app.put(...)`**, **`@app.delete(...)`**.

Динамические участки пути оборачиваются в угловые скобки с конвертером типа:
- `<int:id>` — целое положительное число (передаётся в аргумент функции сразу как `int`);
- `<string:slug>` — строка без слэшей (по умолчанию);
- `<uuid:token>` — валидный UUID;
- `<path:subpath>` — строка, которая может содержать слэши `/`.

---

## Чтение входящих данных из `request` и формирование ответа `jsonify`

В отличие от Django (где объект `request` передаётся первым аргументом в каждую функцию), во Flask объект **`request`** импортируется из пакета `flask`:

- **`request.args`** — параметры строки запроса (`?page=2&q=python`). Безопасное чтение с приведением типа: `request.args.get("page", default=1, type=int)`.
- **`request.get_json()`** (или `request.json`) — распарсенное тело JSON-запроса. Если передать `request.get_json(silent=True)`, при невалидном JSON вернётся `None` вместо выброса ошибки `400 Bad Request`.
- **`request.headers`** и **`request.cookies`** — заголовки и куки запроса.
- **Формирование ответа**: во Flask 2+ достаточно вернуть из функции словарь `dict` и кортеж со статус-кодом (`return {"id": 1, "status": "created"}, 201`) или вызвать **`jsonify(...)`** — Flask сам сериализует данные в JSON и выставит заголовок `Content-Type: application/json`.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/api/users")
def create_user_flask():
    payload = request.get_json(silent=True) or {}
    page = request.args.get("page", default=1, type=int)
    if "email" not in payload:
        return {"error": "Поле email обязательно"}, 400
    return {"id": 101, "email": payload["email"], "page": page}, 201

body, status_code = create_user_flask()
print(f"Ответ Flask-эндпоинта -> статус {status_code}, тело: {body}")
```

---

## Централизованный перехват ошибок через `@app.errorhandler`

По умолчанию при вызове `abort(404)` или ошибке `500` Flask возвращает стандартную HTML-страницу ошибки. В JSON API клиент ждёт ошибку строго в формате JSON! Декоратор **`@app.errorhandler(...)`** позволяет перехватывать как HTTP-коды (`404`, `422`, `500`), так и любые кастомные классы исключений Python:

```python
from flask import Flask

app = Flask(__name__)

class InsufficientBalanceError(Exception):
    def __init__(self, needed: float):
        self.needed = needed

@app.errorhandler(InsufficientBalanceError)
def handle_balance_error(exc: InsufficientBalanceError):
    return {"error": "insufficient_funds", "needed": exc.needed}, 409

resp_err, code_err = handle_balance_error(InsufficientBalanceError(needed=1500.0))
print(f"Глобальный errorhandler вернул {code_err}:", resp_err)
```

> **Junior vs Senior**:
> - **Junior**: Читает JSON через `json.loads(request.data)` без обработки ошибок парсинга, приводит query-параметры через `int(request.args['page'])` (получая `500 Internal Server Error` при передаче `?page=abc`) и оставляет стандартные HTML-страницы ошибок Flask в JSON API.
> - **Senior**: Использует `request.get_json(silent=True)` и `request.args.get("page", default=1, type=int)`, типизирует URL через конвертеры `<int:id>` и `<uuid:id>`, а все ошибки домена и HTTP-исключения приводит к единому JSON-контракту через `@app.errorhandler`.
"""
    ),

    'К-097': (
        '3.4',
        'К-097. Контексты Flask_ как работают request и g.md',
        r"""📖 Перечитать конспект: Архитектура Flask под капотом: стек контекстов (Application vs Request Context) и прокси request, g, current_app >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Главная загадка Flask: почему `from flask import request` не перемешивает запросы разных пользователей?

Когда разработчик впервые видит во Flask строку `from flask import request, g, current_app` на уровне модуля, возникает законный вопрос:
*«Подождите! Если `request` — это глобальная переменная, то что случится, когда на сервер одновременно придут запросы от Алисы и Боба в разных потоках? Не прочитает ли Боб данные запроса Алисы?!»*

Ответ: **`request`, `g`, `session` и `current_app` во Flask НЕ являются обычными глобальными переменными!**
Это объекты-посредники (**`LocalProxy` из `Werkzeug`**), которые под капотом обращаются к изолированному хранилищу контекста текущего потока или асинхронной корутины (**`contextvars.ContextVar`** в современном Python). Когда ваш код читает `request.json`, прокси смотрит, какой именно поток/корутина сейчас выполняется, и достаёт объект запроса **именно этого клиента**!

```python
import contextvars

# Как устроен LocalProxy во Flask под капотом:
_request_ctx_var: contextvars.ContextVar[dict] = contextvars.ContextVar("flask_request_ctx")

class LocalProxyDemo:
    def __getattr__(self, name: str):
        try:
            current_req = _request_ctx_var.get()
        except LookupError:
            raise RuntimeError("Working outside of request context! (Обращение к request вне активного запроса)")
        return current_req[name]

request_proxy = LocalProxyDemo()

# Поток/корутина запроса №1 активирует свой контекст
token = _request_ctx_var.set({"user": "Alice", "path": "/profile"})
print("Внутри контекста запроса request_proxy.user =", request_proxy.user)
_request_ctx_var.reset(token)

try:
    _ = request_proxy.user
except RuntimeError as err:
    print("Вне контекста запроса:", err)
```

---

## Два вида контекстов во Flask: `Application Context` vs `Request Context`

На собеседованиях часто просят назвать все 4 контекстно-локальных прокси во Flask и объяснить, к какому из двух контекстов относится каждый из них:

| Тип контекста | Какие прокси живут внутри | Когда создаётся и для чего нужен |
| :--- | :--- | :--- |
| **1. Контекст приложения (`Application Context`)** | **`current_app`** (ссылка на активный экземпляр `Flask`) и **`g`** (временный блокнот на время одного запроса/команды) | При обработке запроса или запуске CLI-команды (`with app.app_context():`). Нужен для доступа к конфигу `current_app.config` и ресурсам БД |
| **2. Контекст запроса (`Request Context`)** | **`request`** (данные входящего HTTP-запроса) и **`session`** (криптографически подписанные куки сессии) | Создаётся автоматически при приходе HTTP-запроса (или в тестах через `with app.test_request_context('/url'):`) |

**Что такое объект `flask.g`?**
Буква `g` означает *global within the current context* (глобальный только в рамках **текущего одного запроса**). Например, в хуке `@app.before_request` вы проверили JWT-токен, положили пользователя в `g.user = user` и время старта в `g.start_time = time.time()`, а затем прочитали `g.user` внутри роута. Как только запрос завершился, `g` полностью очищается! Никогда не используйте `g` для кэширования данных между разными запросами — для этого нужен Redis.

---

## Хуки жизненного цикла запроса во Flask

- **`@app.before_request`** — выполняется перед каждым запросом. Если функция вернёт ответ (например, `return {"error": "Unauthorized"}, 401`), запрос прервётся и не дойдёт до роута.
- **`@app.after_request`** — принимает объект `response`, позволяет добавить заголовки (например, CORS или `X-Process-Time`) и **обязан вернуть `response`**.
- **`@app.teardown_appcontext`** — гарантированно выполняется в самом конце (даже при необработанном исключении) для закрытия соединения с БД (`db.session.remove()`).

> **Junior vs Senior**:
> - **Junior**: Пытается сохранить данные между разными HTTP-запросами в объект `flask.g` (не понимая, что `g` уничтожается в конце каждого запроса) или обращается к `current_app.config` на уровне импорта модуля, получая `RuntimeError: Working outside of application context`.
> - **Senior**: Чётко разделяет `Application Context` (`current_app`, `g`) и `Request Context` (`request`, `session`), использует `g` только для передачи контекстных данных внутри одного запроса, а в фоновых скриптах и CLI явно открывает `with app.app_context():`.
"""
    ),

    'К-096': (
        '3.4',
        'К-096. Flask Blueprint_ модульная архитектура.md',
        r"""📖 Перечитать конспект: Модульная архитектура Flask: Blueprints и паттерн Application Factory (create_app) >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Проблема циклических импортов (`Circular Imports`) и зачем нужны `Blueprints`

В маленьком Flask-скрипте мы создаём `app = Flask(__name__)` в файле `app.py`. Когда проект растёт, мы выносим маршруты в `views/users.py` и `views/orders.py`.
Но чтобы навесить декоратор `@app.route`, файлу `views/users.py` нужно импортировать `app` из `app.py`, а файлу `app.py` нужно импортировать `views/users.py`, чтобы маршруты зарегистрировались! Возникает классический **циклический импорт (`ImportError: cannot import name 'app' from partially initialized module`)**.

Решение во Flask — **`Blueprint` («Чертёж» / модульный эскиз)**:
- В файле `users/routes.py` мы создаём не приложение, а независимый чертёж: `users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")`.
- Декорируем функции через `@users_bp.get("/")` и `@users_bp.post("/")` — **объект `app` здесь вообще не нужен!**
- А в главном файле приложения мы просто подключаем готовые чертежи: **`app.register_blueprint(users_bp)`**.

```python
from flask import Blueprint

# Изолированный Blueprint модуля заказов (не зависит от глобального app!)
orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

@orders_bp.get("/<int:order_id>")
def get_order_route(order_id: int):
    return {"order_id": order_id, "blueprint": orders_bp.name, "prefix": orders_bp.url_prefix}

print("Маршрут Blueprint готов к регистрации:", get_order_route(42))
```

---

## Паттерн `Application Factory` (`create_app`) и `init_app()`

В промышленной разработке на Flask экземпляр `app = Flask(__name__)` никогда не создают на глобальном уровне модуля. Вместо этого используют паттерн **Фабрика приложения (`Application Factory`)** — функцию `def create_app(config_class):`.

Зачем нужна функция `create_app()`?
1. **Изолированное тестирование**: в `pytest` вы можете вызвать `create_app(TestingConfig)` с базой данных в памяти, не затрагивая боевой конфиг.
2. **Разрыв циклических связей с расширениями (`db`, `migrate`, `jwt`)**: расширения создаются пустыми в отдельном файле `extensions.py` (`db = SQLAlchemy()`), а внутри `create_app(config)` привязываются к конкретному приложению методом **`db.init_app(app)`**!

```python
from flask import Flask, Blueprint

# 1. В extensions.py расширения создаются без привязки к конкретному app
class ExtensionSimulator:
    def __init__(self):
        self.bound_app = None
    def init_app(self, app: Flask):
        self.bound_app = app.name

db_ext = ExtensionSimulator()
users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

# 2. Фабрика приложения (Application Factory) собирает всё воедино
def create_app(env_name: str = "testing") -> Flask:
    app = Flask(f"shop_{env_name}")
    app.config["ENV_NAME"] = env_name
    db_ext.init_app(app)
    app.register_blueprint(users_bp)
    return app

test_app = create_app("testing")
print("Фабрика создала приложение:", test_app.name, "| расширение привязано к:", db_ext.bound_app)
```

---

## Локальные хуки и обработчики ошибок внутри `Blueprint`

Ещё одно преимущество `Blueprint` — возможность навешивать `before_request` и `errorhandler` **только на конкретную группу маршрутов**:
- `@admin_bp.before_request` — проверит права администратора перед входом в любой маршрут `/admin/*`, не затрагивая публичные маршруты `/public/*`!
- `@api_bp.errorhandler(404)` — вернёт JSON-ошибку для `/api/*`, тогда как основной сайт может возвращать красивую HTML-страницу 404.

> **Junior vs Senior**:
> - **Junior**: Создаёт глобальный `app = Flask(__name__)` и `db = SQLAlchemy(app)` в `main.py`, импортирует `app` во все файлы с роутами и часами борется с `ImportError: circular import`, а в тестах случайно пишет данные в dev-базу.
> - **Senior**: Строит проект по паттерну **Application Factory (`create_app`)**, выносит расширения в `extensions.py` с отложенной инициализацией через `.init_app(app)` и разбивает бизнес-домены на независимые модули с `Blueprint`.
"""
    ),

    'К-089': (
        '3.4',
        'К-089. Flask-SQLAlchemy_ работа с базой данных.md',
        r"""📖 Перечитать конспект: Работа с БД во Flask: Flask-SQLAlchemy, жизненный цикл сессии и миграции Flask-Migrate >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Как `Flask-SQLAlchemy` связывает Flask и SQLAlchemy

В отличие от Django, у Flask нет собственной встроенной ORM. Стандартом индустрии для работы с реляционными БД во Flask является связка **SQLAlchemy** + расширение **`Flask-SQLAlchemy`** + **`Flask-Migrate`** (обёртка над инструментом миграций **`Alembic`**).

Какую важную работу берёт на себя `Flask-SQLAlchemy`, избавляя вас от рутины?
1. Читает строку подключения `SQLALCHEMY_DATABASE_URI` из `app.config` и настраивает пул соединений (`Engine` + `Connection Pool`).
2. Предоставляет базовый класс для моделей `db.Model`.
3. **Самое главное — управляет жизненным циклом сессии (`db.session`)**: автоматически привязывает изолированную сессию БД к контексту текущего HTTP-запроса (`Application Context`) и **автоматически закрывает её** в хуке `@app.teardown_appcontext` после завершения запроса!

---

## Описание моделей, связей и выполнение транзакций

При модификации данных (`INSERT`, `UPDATE`, `DELETE`) в SQLAlchemy действует паттерн **Unit of Work**:
- Вызов `db.session.add(user)` лишь помещает объект в список отслеживаемых изменений в памяти Python.
- Вызов **`db.session.commit()`** отправляет `INSERT/UPDATE` в базу данных и фиксирует транзакцию.
- Если во время записи возникло исключение (например, `IntegrityError` при дублировании уникального `email`), транзакцию **обязательно нужно откатить через `db.session.rollback()`**, иначе сессия останется в сломанном состоянии!

```python
from extensions import db

class AccountModel(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

def register_account_safely(email: str) -> dict:
    try:
        acc = AccountModel(id=1, email=email)
        db.session.add(acc)
        db.session.commit()
        return {"ok": True, "email": email}
    except Exception as exc:
        db.session.rollback()
        return {"ok": False, "error": str(exc)}

print("Безопасное сохранение через db.session:", register_account_safely("user@flask.io"))
```

---

## Миграции через `Flask-Migrate` (`Alembic`) и правила продакшена

- **Никогда не используйте `db.create_all()` в продакшене!** Метод `create_all()` умеет только создавать отсутствующие таблицы с нуля, но не умеет добавлять новые колонки в существующие таблицы с данными.
- В продакшене схему БД меняют только через миграции **`Flask-Migrate` (`Alembic`)**:
  1. `flask db init` — создаёт папку `migrations/` (один раз в начале проекта);
  2. `flask db migrate -m "add phone to users"` — сравнивает модели `db.Model` с текущей БД и генерирует скрипт миграции с функциями `upgrade()` и `downgrade()`;
  3. **Обязательно проверьте сгенерированный файл миграции глазами** (автогенератор Alembic может не заметить переименование колонки и попытаться сделать `drop_column` + `add_column` с потерей данных!);
  4. `flask db upgrade` — накатывает миграцию на базу данных.

> **Junior vs Senior**:
> - **Junior**: Вызывает `db.create_all()` при старте продакшен-сервера, забывает вызывать `db.session.rollback()` в блоке `except IntegrityError` и применяет автосгенерированные миграции `flask db migrate` вслепую без ревью.
> - **Senior**: Управляет схемой БД строго через версионируемые ревизии `Alembic` (`Flask-Migrate`), всегда проверяет сгенерированный `upgrade()`/`downgrade()` код глазами и откатывает сессию через `db.session.rollback()` при любых исключениях БД.
"""
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.5 · ЧАСТЬ V: АУТЕНТИФИКАЦИЯ, АВТОРИЗАЦИЯ И КРИПТОЗАЩИТА
    # ═══════════════════════════════════════════════════════════════════════════
    'К-098': (
        '3.5',
        'К-098. JWT_ анатомия токена и практика безопасности.md',
        r"""📖 Перечитать конспект: JWT: анатомия токена, пара Access + Refresh, ротация jti и практика безопасности >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Анатомия JWT-токена на реальном примере

**JWT (JSON Web Token, RFC 7519)** — это компактный, криптографически подписанный цифровой пропуск, который сервер выдаёт клиенту после успешного входа.
Он состоит из **трёх сегментов в кодировке Base64Url, разделённых точками**: `Header.Payload.Signature`.

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZXhwIjoxNzAwMDAwMH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`

1. **Header (Заголовок)**: `{"alg": "HS256", "typ": "JWT"}` — указывает алгоритм подписи (`HS256` — симметричный HMAC с общим секретом, или `RS256` / `EdDSA` — асимметричная пара приватного и публичного ключей).
2. **Payload (Полезная нагрузка / Клеймы `Claims`)**:
   - `sub` (*Subject*) или `user_id` — ID пользователя;
   - `role` / `scopes` — права доступа;
   - `exp` (*Expiration Time*) — Unix-время истечения срока действия токена;
   - `iat` (*Issued At*) — время выпуска;
   - `jti` (*JWT ID*) — уникальный `UUID` конкретного токена (нужен для точечного отзыва и защиты от повторного использования).
3. **Signature (Криптографическая подпись)**:
   `HMAC-SHA256(base64url(header) + "." + base64url(payload), SECRET_KEY)`.

> **Главное правило безопасности**: стандартный JWT (`JWS`) **НЕ зашифрован, а лишь подписан**! Любой человек может декодировать `Payload` из Base64 за долю секунды и прочитать все поля. Подпись гарантирует только то, что **никто не смог изменить `user_id` или `role` без знания `SECRET_KEY`**. Никогда не кладите в `Payload` пароли, номера карт или секреты!

```python
import jwt

SECRET_KEY = "prod-env-secret-key"
encoded_token = jwt.encode({"user_id": 42, "role": "admin"}, SECRET_KEY, algorithm="HS256")
decoded_payload = jwt.decode(encoded_token, key=SECRET_KEY, algorithms=["HS256"])
print("Сгенерирован JWT:", encoded_token[:36] + "...")
print("Проверенный Payload:", decoded_payload)
```

---

## Зачем нужна пара `Access Token` + `Refresh Token` и ротация `jti`

Почему нельзя просто выдать один JWT-токен сроком на 30 дней?
Потому что `Access Token` проверяется без похода в БД, и если злоумышленник его украдёт, отозвать его нельзя до истечения 30 дней!
Поэтому в продакшене используют **двухтокенную схему**:

| Характеристика | ⚡ **Access Token** (Короткоживущий пропуск) | 🔄 **Refresh Token** (Долгоживущий токен обновления) |
| :--- | :--- | :--- |
| **Время жизни (`TTL`)** | **5–15 минут** | **7–30 дней** |
| **Где хранится на клиенте** | В оперативной памяти JS-приложения | В защищённой куке **`HttpOnly; Secure; SameSite=Strict`** (недоступен для чтения из JS при XSS!) |
| **Куда отправляется** | В заголовке `Authorization: Bearer <token>` на каждый запрос к API | **Только** на один специальный эндпоинт `POST /auth/refresh` |
| **Хранится ли в БД/Redis?** | Нет (`Stateless` проверка по подписи) | Да, его уникальный `jti` (или хеш) хранится в Redis/БД для мгновенного отзыва и **Refresh Token Rotation** |

**Как работает Refresh Token Rotation**: при каждом обращении к `/auth/refresh` старый `Refresh Token` помечается использованным (удаляется из Redis), а клиенту выдаётся **новая пара** (`Access + Refresh`). Если кто-то попытается повторно использовать уже погашенный `Refresh Token` — сервер понимает, что токен был украден, и **мгновенно аннулирует все сессии этого пользователя**!

---

## Защита от уязвимости `alg: none` и подмены алгоритма

При вызове `jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])` **всегда явно передавайте белый список разрешённых алгоритмов `algorithms=["HS256"]`**, никогда не доверяя значению `alg` из присланного заголовка токена!

> **Junior vs Senior**:
> - **Junior**: Выпускает один JWT со сроком жизни 30 дней, кладёт его в `localStorage` (где любая XSS-уязвимость крадёт токен одной строкой JS) и не указывает `algorithms=["HS256"]` при декодировании.
> - **Senior**: Использует связку короткоживущего `Access Token` (5–15 мин в памяти) + `Refresh Token` (в `HttpOnly; Secure; SameSite=Strict` куке) с ротацией `jti` в Redis и жёстко фиксирует список допустимых алгоритмов подписи.
"""
    ),

    'К-099': (
        '3.5',
        'К-099. OAuth 2.0 и OpenID Connect_ авторизация.md',
        r"""📖 Перечитать конспект: OAuth 2.0 и OpenID Connect (OIDC): Authorization Code Flow с PKCE и id_token >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Разница между OAuth 2.0 (Авторизация) и OpenID Connect (Аутентификация)

Эти два понятия постоянно путают на собеседованиях:
- **Аутентификация (`AuthN` — «Кто ты?»)** — проверка личности пользователя.
- **Авторизация (`AuthZ` — «Что тебе разрешено?»)** — предоставление прав доступа к ресурсам.

1. **OAuth 2.0** — это протокол **делегированной авторизации**. Он позволяет вашему сервису получить ограниченный токен доступа (`access_token` с правами `scope`, например `calendar.readonly`) к данным пользователя в Google или GitHub, **не узнавая пароль пользователя**.
2. **OpenID Connect (OIDC)** — это тонкая надстройка над OAuth 2.0 для **аутентификации** (кнопки «Войти через Google / GitHub / Яндекс»). В дополнение к `access_token` провайдер возвращает подписанный JWT-токен **`id_token`**, внутри которого лежат подтверждённые данные личности пользователя (`sub`, `email`, `name`, `picture`).

---

## Четыре участника и золотой стандарт `Authorization Code Flow + PKCE`

В процессе участвуют 4 стороны:
- **Resource Owner** — сам пользователь;
- **Client** — ваше приложение;
- **Authorization Server** — сервер входа провайдера (например, `accounts.google.com`);
- **Resource Server** — API провайдера с данными пользователя.

Как устроен самый безопасный сценарий входа **Authorization Code Flow** по шагам:
1. Пользователь нажимает «Войти через Google». Ваш бэкенд перенаправляет браузер на Google с параметрами `client_id`, `redirect_uri`, `scope=openid email profile`, `state` (случайный токен защиты от CSRF) и `code_challenge` (**PKCE**).
2. Пользователь вводит пароль **на сайте Google** (ваш сайт пароля не видит!).
3. Google перенаправляет браузер обратно на ваш `redirect_uri` с одноразовым коротким кодом **`?code=xyz&state=...`**.
4. **Ваш бэкенд (сервер-сервер, втайне от браузера!)** отправляет POST-запрос в Google, передавая `code`, секретный ключ приложения **`client_secret`** и исходный **`code_verifier`**.
5. Google проверяет секреты и возвращает вашему бэкенду `id_token` + `access_token`.

```python
import hashlib
import base64
import secrets

# Демонстрация механизма PKCE (Proof Key for Code Exchange) в OAuth 2.0:
def generate_pkce_pair() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(32)
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return code_verifier, code_challenge

verifier, challenge = generate_pkce_pair()
print("Сгенерирован PKCE code_verifier (длина):", len(verifier))
print("Сгенерирован SHA-256 code_challenge:", challenge[:24] + "...")
```

---

## Защита от CSRF через параметр `state` и проверка `id_token`

Две критические проверки безопасности, без которых OAuth 2.0 / OIDC уязвим к перехвату аккаунта:
1. **Проверка параметра `state`**: перед редиректом на провайдера сервер генерирует случайный `state = secrets.token_urlsafe(16)`, сохраняет его в сессии/куке, а при возврате пользователя на `/callback?code=...&state=...` сверяет оба значения через `hmac.compare_digest`. Если `state` не совпал — это атака **Login CSRF**!
2. **Валидация клеймов `id_token`**: в полученном `id_token` обязательно проверяются криптографическая подпись провайдера (по публичным ключам `JWKS`), издатель `iss` (*Issuer*), аудитория `aud` (должна совпадать с вашим `client_id`) и срок действия `exp`.

```python
import hmac
import secrets

def validate_oauth_callback(session_state: str, callback_state: str, id_token_claims: dict, my_client_id: str) -> str:
    if not hmac.compare_digest(session_state, callback_state):
        raise PermissionError("403 Forbidden: несовпадение OAuth state (защита от Login CSRF)!")
    if id_token_claims.get("aud") != my_client_id:
        raise PermissionError("403 Forbidden: токен выпущен для другого приложения (aud mismatch)!")
    return f"Успешный вход через OIDC: sub={id_token_claims['sub']} ({id_token_claims['email']})"

st = secrets.token_urlsafe(16)
claims = {"sub": "google-uid-777", "email": "dev@py.io", "aud": "my-app-client-id"}
print(validate_oauth_callback(st, st, claims, "my-app-client-id"))
```

> **Junior vs Senior**:
> - **Junior**: Путает OAuth 2.0 (авторизацию) с OIDC (аутентификацией), пропускает проверку параметра `state` на `/callback` (открывая дыру для привязки чужого аккаунта через Login CSRF) и пытается использовать устаревший `Implicit Flow` с передачей токена прямо в URL.
> - **Senior**: Всегда использует `Authorization Code Flow + PKCE`, строго сверяет `state` через `hmac.compare_digest`, обменивает одноразовый `code` на токены только на бэкенде (`back-channel`) и валидирует подпись `JWKS`, `iss`, `aud` и `exp` у `id_token`.
"""
    ),

    'К-100': (
        '3.5',
        'К-100. Сессии vs JWT_ где хранится состояние.md',
        r"""📖 Перечитать конспект: Сессии в Redis против JWT: где хранится состояние и как мгновенно отозвать доступ >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Серверные сессии (`Session ID` в Cookie) против токенов `JWT`

После того как пользователь ввёл логин и пароль, как серверу узнавать его при следующих запросах? В бэкенде конкурируют два подхода:

| Критерий сравнения | 🗄️ **Серверные сессии (Session + Redis)** | 🪪 **Токены JWT (Access + Refresh)** |
| :--- | :--- | :--- |
| **Что хранится у клиента?** | Только случайный непрозрачный идентификатор `session_id` в `HttpOnly` куке (`128–256 бит`) | Подписанный JSON-токен с данными (`user_id`, `role`, `exp`) |
| **Что делает сервер при запросе?** | Идёт в **Redis** (`GET session:<id>`) и достаёт данные пользователя | Проверяет криптографическую подпись на **CPU** без похода в БД |
| **Мгновенный бан / «Выйти везде»** | **Мгновенно и просто**: удаляем ключ сессии из Redis (`DEL`) | **Сложно**: выпущенный `Access Token` валиден до истечения `exp` (требуется короткий TTL или Blacklist `jti` в Redis) |
| **Лучший сценарий применения** | Монолиты, веб-приложения с высокими требованиями к безопасности, BFF (Backend-for-Frontend) | Микросервисы (десятки сервисов проверяют токен локально), мобильные приложения |

---

## Как мгновенно отозвать доступ (`Revocation`) в обоих подходах

Главная архитектурная дилемма: администратор заблокировал уволенного сотрудника или пользователь нажал кнопку «Выйти со всех устройств». Как гарантировать, что доступ прекратится **в ту же секунду**?

1. **В архитектуре с сессиями в Redis**: достаточно удалить `session_id` из Redis (`DEL session:<id>`) или удалить все сессии из множества `user_sessions:<user_id>`. Следующий же запрос вернёт `401 Unauthorized`.
2. **В архитектуре с JWT**: поскольку `Access Token` самодостаточен, для мгновенного отзыва применяют **гибридный подход**:
   - делают `Access Token` очень короткоживущим (5 минут);
   - а для критических операций или мгновенного бана ведут в Redis **чёрный список отозванных токенов (`Blacklist` по ключу `blacklist:jti:<uuid>`)** с `TTL`, равным оставшемуся времени жизни токена (чтобы Redis сам очищал старые записи!).

```python
# Сравнение проверки сессии в Redis и проверки JWT с Blacklist отозванных jti:
class AuthVerifierDemo:
    def __init__(self):
        self.redis_sessions = {"sess_abc": {"user_id": 42, "active": True}}
        self.jwt_blacklist = set()

    def revoke_session(self, sid: str):
        self.redis_sessions.pop(sid, None)

    def revoke_jwt_jti(self, jti: str):
        self.jwt_blacklist.add(jti)

    def check_jwt(self, payload: dict) -> bool:
        return payload["jti"] not in self.jwt_blacklist

verifier = AuthVerifierDemo()
jwt_claims = {"user_id": 42, "jti": "uuid-999"}
print("До отзыва JWT валиден:", verifier.check_jwt(jwt_claims))
verifier.revoke_jwt_jti("uuid-999")
print("После добавления jti в Redis Blacklist JWT валиден:", verifier.check_jwt(jwt_claims))
```

---

## Защита Cookie-сессий и гибридный паттерн для микросервисов

Когда вы храните `session_id` или `refresh_token` в Cookie браузера, обязательно выставляйте три флага безопасности:
- **`HttpOnly`** — запрещает чтение куки из JavaScript (`document.cookie`), полностью защищая сессию от кражи через XSS;
- **`Secure`** — кука передаётся только по шифрованному HTTPS;
- **`SameSite=Lax` (или `Strict`)** — браузер не прикрепляет куку к кросс-доменным POST-запросам со сторонних сайтов, защищая от **CSRF-атак**.

```python
def build_secure_cookie_header(session_id: str, max_age: int = 86400) -> str:
    return (
        f"session_id={session_id}; Max-Age={max_age}; Path=/; "
        "HttpOnly; Secure; SameSite=Strict"
    )

print("Безопасный заголовок Set-Cookie:", build_secure_cookie_header("s_9f8a7b6c"))
```

> **Junior vs Senior**:
> - **Junior**: Выбирает JWT просто потому, что «так модно», даже для обычного монолита, а потом не знает, как заблокировать украденный токен или разлогинить пользователя со всех устройств до истечения `exp`.
> - **Senior**: Выбирает инструмент под архитектуру: для монолита и BFF использует быстрые сессии в Redis с `HttpOnly; Secure; SameSite` куками (дающими мгновенный отзыв), а для микросервисов — короткоживущие JWT (`Access` 5 мин) в связке с Redis Blacklist для `jti`.
"""
    ),

    'К-101': (
        '3.5',
        'К-101. API-ключи_ генерация, хранение и безопасность.md',
        r"""📖 Перечитать конспект: API-ключи для M2M-интеграций: криптографическая генерация, префиксы и хранение SHA-256 хешей >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что такое API-ключ и чем он отличается от пароля и JWT

Когда к вашему бэкенду обращается не живой человек из браузера, а скрипт партнёра, платёжный шлюз или внешний сервер (**Machine-to-Machine / M2M интеграция**), неудобно проходить браузерный логин каждые 15 минут. Для этого выпускаются долгоживущие **API-ключи (`API Keys`)**.

Три золотых правила проектирования промышленных API-ключей (как в Stripe `sk_live_...` или GitHub `ghp_...`):

1. **Криптографическая генерация (`secrets`) и читаемый префикс**:
   Модуль `random` предсказуем и категорически запрещён! Ключ генерируется через **`secrets.token_urlsafe(32)`** (256 бит энтропии) с понятным префиксом среды (`sk_live_...` или `sk_test_...`), чтобы сканеры секретов (GitGuardian) и разработчики сразу понимали назначение ключа.
2. **В базе данных хранится ТОЛЬКО `SHA-256` хеш ключа + первые символы префикса**:
   Оригинал ключа показывается пользователю в личном кабинете **ровно один раз** в момент создания. В таблицу БД сохраняется `key_prefix` (чтобы пользователь видел в списке `sk_live_a8f9...`) и `key_hash = sha256(raw_key)`. При утечке дампа БД злоумышленник не сможет восстановить ни одного рабочего ключа!
3. **Передача строго в заголовках (`Authorization: Bearer` или `X-API-Key`)**:
   Никогда не передавайте API-ключ в query-параметре URL (`?api_key=...`) — полный URL оседает в открытом виде в access-логах Nginx, прокси-серверах и истории браузера!

```python
import hashlib
import hmac
import secrets

def create_api_key(env: str = "live") -> dict:
    raw_secret = secrets.token_urlsafe(24)
    full_key = f"sk_{env}_{raw_secret}"
    key_hash = hashlib.sha256(full_key.encode("utf-8")).hexdigest()
    return {
        "show_once_key": full_key,
        "db_record": {"prefix": full_key[:12], "key_hash": key_hash, "scopes": ["orders:read"]},
    }

def verify_api_key(incoming_key: str, db_record: dict) -> bool:
    incoming_hash = hashlib.sha256(incoming_key.encode("utf-8")).hexdigest()
    return hmac.compare_digest(incoming_hash, db_record["key_hash"])

created = create_api_key("live")
print("Сгенерирован ключ (показывается 1 раз):", created["show_once_key"][:20] + "...")
print("В БД сохраняется префикс:", created["db_record"]["prefix"], "и SHA-256 хеш:", created["db_record"]["key_hash"][:16] + "...")
print("Проверка подлинного ключа:", verify_api_key(created["show_once_key"], created["db_record"]))
```

---

## Почему для API-ключей достаточно `SHA-256`, а для паролей нужен `Argon2id`?

Частый вопрос с подвохом на собеседовании: *«В уроке про пароли вы говорили, что `SHA-256` слишком быстрый и опасен для паролей. Почему же для API-ключей мы используем `SHA-256`, а не медленный `bcrypt`/`Argon2`?»*

1. Пароль придумывает человек — у него **низкая энтропия** (8–12 предсказуемых символов), поэтому его реально перебрать на видеокарте, если хеш быстрый.
2. API-ключ генерирует криптографический генератор `secrets.token_urlsafe(32)` — у него **256 бит чистой случайной энтропии** ($2^{256}$ комбинаций). Перебрать такой ключ методом Brute Force физически невозможно даже за миллиарды лет! Зато `SHA-256` вычисляется за микросекунды на каждом запросе к API и не нагружает процессор сервера.

---

## Ограничение прав (`Scopes`), ротация с `Grace Period` и защита от Timing Attack

В зрелом продакшене API-ключ никогда не даёт «полный доступ ко всему аккаунту»:
- **Узкие права (`Scopes`)**: ключ выпускается только под конкретную задачу (например, `["payments:read", "webhooks:write"]`).
- **Бесшовная ротация (`Grace Period`)**: при перевыпуске ключа старый ключ не удаляется мгновенно, а остаётся активным ещё например 24 часа (`expires_at`), чтобы партнёр успел обновить секреты на своих серверах без даунтайма!
- **Защита от атак по времени (`hmac.compare_digest`)**: сравнение хешей всегда выполняется за константное время через `hmac.compare_digest(a, b)` вместо оператора `==`.

```python
import time

def check_key_with_grace_period(db_key: dict, required_scope: str, now: float) -> str:
    if db_key.get("revoked"):
        return "401 Unauthorized: ключ отозван"
    if db_key.get("expires_at") and now > db_key["expires_at"]:
        return "401 Unauthorized: истёк Grace Period старого ключа"
    if required_scope not in db_key.get("scopes", []):
        return f"403 Forbidden: у ключа нет права '{required_scope}'"
    return "200 OK: доступ по API-ключу разрешён"

old_key_record = {"scopes": ["orders:read"], "revoked": False, "expires_at": 1000.0}
print("Во время Grace Period (t=500):", check_key_with_grace_period(old_key_record, "orders:read", now=500.0))
print("Попытка удалить заказ по read-only ключу:", check_key_with_grace_period(old_key_record, "orders:delete", now=500.0))
print("После истечения Grace Period (t=1500):", check_key_with_grace_period(old_key_record, "orders:read", now=1500.0))
```

> **Junior vs Senior**:
> - **Junior**: Генерирует API-ключ через `uuid.uuid4()` или `random.choices()`, хранит его в таблице БД в открытом виде (`VARCHAR`), передаёт в URL `?api_key=...` и сравнивает через `==`.
> - **Senior**: Генерирует ключи высокой энтропии через `secrets.token_urlsafe(32)` с префиксом среды (`sk_live_`), хранит в БД только `key_prefix` и `SHA-256` хеш, сравнивает через `hmac.compare_digest`, ограничивает `scopes` и поддерживает плавную ротацию ключей с `Grace Period`.
"""
    ),

    'К-108': (
        '3.5',
        'К-108. Stateful vs Stateless_ где хранится.md',
        r"""📖 Перечитать конспект: Архитектура состояния: Stateful против Stateless, Sticky Sessions и горизонтальное масштабирование >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## В чём фундаментальная разница между `Stateful` и `Stateless` бэкендом

Когда на ваш сервис приходят 100 запросов в секунду, одного процесса Python становится мало, и вы запускаете **горизонтальное масштабирование (Horizontal Scaling)** — поднимаете 4 контейнера бэкенда за балансировщиком нагрузки (`Nginx` / `AWS ALB`).

Именно в этот момент проявляется разница между двумя архитектурами:

1. **Наивный `Stateful` в памяти процесса (Локальное состояние)**:
   Если воркер №1 после логина сохранил сессию пользователя в локальный словарь Python `SESSIONS[sid] = user`, а следующий запрос пользователя балансировщик направил на воркер №2 — воркер №2 ничего не знает об этой сессии и выбросит `401 Unauthorized`!
   Приходится либо настраивать хрупкие **Sticky Sessions** (привязку IP/куки клиента к конкретному воркеру, которая ломается при падении контейнера), либо выносить состояние во **внешнее общее хранилище — Redis**.
2. **`Stateless` бэкенд (Воркеры без собственного состояния)**:
   Ни один контейнер Python не хранит состояние сессий в своей оперативной памяти. Либо все данные лежат в подписанном токене клиента (`JWT`), либо во внешнем кластере `Redis` / `PostgreSQL`. Любой из 50 контейнеров может обработать любой запрос любого пользователя, а при падении одного контейнера пользователи даже ничего не заметят!

```python
# Наглядная демонстрация проблемы локального состояния при балансировке между 2 воркерами:
worker_1_ram = {}
worker_2_ram = {}
shared_redis = {}

# Пользователь логинится на Воркере 1:
worker_1_ram["sid_1"] = {"user_id": 42}
shared_redis["sid_1"] = {"user_id": 42}

# Следующий запрос попадает на Воркер 2:
print("Локальная память Воркера 2 (Sticky Session сломалась):", worker_2_ram.get("sid_1"))
print("Общий Redis (Stateless воркеры работают идеально):", shared_redis.get("sid_1"))
```

---

## Почему `Sticky Sessions` на балансировщике — это полумера

Иногда пытаются «починить» локальное состояние в памяти воркеров, включив на балансировщике нагрузки режим **Sticky Sessions (Session Affinity)** — когда Nginx привязывает клиента по IP или куке к конкретному контейнеру.
Почему в облачной (`Cloud-Native` / `Kubernetes`) архитектуре от этого отказываются?
1. **Потеря данных при деплое и автоскейлинге**: каждый раз, когда вы выкатываете новую версию кода или контейнер перезапускается по лимиту памяти, все пользователи этого воркера мгновенно теряют свои сессии и корзины покупок!
2. **Перекос нагрузки (`Hotspots`)**: если за одним корпоративным IP-адресом (NAT) сидят 500 активных сотрудников, `Sticky Sessions` по IP направит их всех на один-единственный воркер, который упадёт от перегрузки, пока остальные 9 воркеров простаивают.

---

## Где хранить состояние в масштабируемой `Stateless`-архитектуре

Чтобы приложение легко масштабировалось от 1 до 100 реплик (`gunicorn --workers 4` или `Kubernetes Deployment`), соблюдайте правило **12-Factor App (Factor VI — Processes are stateless and share-nothing)**:

| Тип данных | ❌ Где НЕЛЬЗЯ хранить | ✅ Где НУЖНО хранить в продакшене |
| :--- | :--- | :--- |
| **Сессии и кэш** | Глобальный `dict` или `@lru_cache` с мутабельным состоянием в RAM воркера | Внешний кластер **Redis** |
| **Загруженные пользователями файлы** | Локальная папка `/app/uploads/` внутри Docker-контейнера | Объектное хранилище **S3 / MinIO** |
| **Счётчики Rate Limiting** | Переменная в памяти процесса Python | Атомарные счётчики в **Redis** (`INCR` / `ZSET`) |

```python
class StatelessClusterDemo:
    def __init__(self, replicas: int = 3):
        self.redis_store = {}
        self.replicas = [f"pod-{i}" for i in range(1, replicas + 1)]

    def handle_request(self, pod_index: int, key: str, value: str | None = None) -> str:
        pod = self.replicas[pod_index % len(self.replicas)]
        if value is not None:
            self.redis_store[key] = value
            return f"[{pod}] Записал в общий Redis: {key}={value}"
        return f"[{pod}] Прочитал из общего Redis: {key}={self.redis_store.get(key)}"

cluster = StatelessClusterDemo(replicas=3)
print(cluster.handle_request(0, "cart:user_42", "MacBook Pro"))
print(cluster.handle_request(2, "cart:user_42"))
```

> **Junior vs Senior**:
> - **Junior**: Хранит активные сессии, коды СМС-подтверждений или загруженные аватарки прямо в глобальном словаре Python или локальной папке контейнера. Всё работает на ноутбуке с одним процессом, но разваливается при запуске `gunicorn --workers 4`.
> - **Senior**: Проектирует воркеры приложения полностью **Stateless (Share-Nothing)**: выносит сессии, кэш и блокировки в Redis, файлы — в S3, а бизнес-состояние — в PostgreSQL, благодаря чему сервис горизонтально масштабируется и переживает перезапуск любого контейнера без потерь.
"""
    ),

    'К-102': (
        '3.5',
        'К-102. RBAC_ Role-Based Access Control –.md',
        r"""📖 Перечитать конспект: Авторизация в бэкенде: RBAC, ABAC и защита от уязвимости №1 OWASP — BOLA / IDOR >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Модели разграничения прав: `RBAC` против `ABAC`

После того как мы узнали, **кто** перед нами (Аутентификация — `user_id=42`), наступает этап **Авторизации**: проверка, имеет ли этот пользователь право выполнить запрошенную операцию.

1. **RBAC (Role-Based Access Control — Ролевая модель доступа)**:
   Права (`permissions`: `orders:create`, `orders:delete`, `reports:read`) назначаются не каждому человеку по отдельности, а **Ролям (`Roles`: `employee`, `manager`, `admin`)**, а пользователю присваивается одна или несколько ролей.
   *Главное правило проектирования RBAC*: в коде эндпоинта проверяйте **конкретное право (`"orders:refund" in user.permissions`)**, а не зашивайте название роли (`user.role == "support_level_2"`). Тогда при появлении новой роли вам не придётся переписывать `if/else` по всему коду!
2. **ABAC (Attribute-Based Access Control — Атрибутная модель доступа)**:
   Решение принимается на основе комбинации атрибутов субъекта, самого ресурса и окружения (например: *«Менеджер может редактировать заказ, только если `order.region == user.region` и `order.status == 'draft'`»*).

```python
ROLE_PERMISSIONS = {
    "viewer": {"orders:read"},
    "manager": {"orders:read", "orders:write"},
    "admin": {"orders:read", "orders:write", "orders:refund"},
}

def has_permission_rbac(user_roles: list[str], required_perm: str) -> bool:
    effective_perms = set()
    for role in user_roles:
        effective_perms |= ROLE_PERMISSIONS.get(role, set())
    return required_perm in effective_perms

print("Есть ли у manager право orders:write?", has_permission_rbac(["manager"], "orders:write"))
print("Есть ли у manager право orders:refund?", has_permission_rbac(["manager"], "orders:refund"))
```

---

## Уязвимость №1 в мире API (OWASP API1): `BOLA` / `IDOR`

Самая опасная и частая уязвимость в реальных бэкендах называется **BOLA (Broken Object Level Authorization)** или **IDOR (Insecure Direct Object Reference)**.

Как она выглядит в коде новичка:
Разработчик защитил эндпоинт `GET /api/orders/{order_id}` проверкой JWT-токена (`Depends(get_current_user)`). Пользователь с `user_id=10` авторизовался, получил свой заказ `/api/orders/501`, а затем просто поменял цифру в адресной строке на `/api/orders/502` — и сервер послушно отдал ему чужой заказ с чужим адресом и телефоном, потому что проверил только токен, но **не проверил владельца строки в БД**!

---

## Золотое правило защиты от `BOLA` / `IDOR` на уровне запроса к БД

Любой запрос к ресурсу по `ID` обязан либо фильтровать выборку в БД по текущему пользователю (`WHERE id = :order_id AND user_id = :current_user_id`), либо явно проверять принадлежность объекта (`order.owner_id == current_user.id`, если пользователь не `admin`). Также для внешних URL рекомендуется использовать не автоинкрементные числа `1, 2, 3`, а непредсказуемые **`UUIDv4`** (но помните: `UUID` сам по себе **не заменяет** проверку прав владельца!).

```python
def authorize_order_access(user: dict, order: dict) -> tuple[int, str]:
    # Комбинация RBAC (роль admin) + Object-Level Ownership (защита от BOLA/IDOR)
    if "admin" in user.get("roles", []):
        return 200, "Доступ разрешён (роль admin)"
    if order["owner_id"] != user["id"]:
        return 403, "403 Forbidden: защита от BOLA/IDOR (чужой заказ!)"
    return 200, "Доступ разрешён (владелец заказа)"

order_502 = {"id": 502, "owner_id": 10, "total": 4900}
alice = {"id": 10, "roles": ["customer"]}
mallory = {"id": 99, "roles": ["customer"]}
admin = {"id": 1, "roles": ["admin"]}

print("Владелец Alice ->", authorize_order_access(alice, order_502))
print("Злоумышленник Mallory (IDOR-атака) ->", authorize_order_access(mallory, order_502))
print("Администратор ->", authorize_order_access(admin, order_502))
```

> **Junior vs Senior**:
> - **Junior**: Хардкодит проверки `if user.role == "admin" or user.role == "moderator":` в десятках эндпоинтов и выбирает объект из БД просто по `session.get(Order, order_id)` без проверки `order.user_id == current_user.id`, оставляя критическую уязвимость BOLA/IDOR.
> - **Senior**: Проверяет гранулярные разрешения (`permissions`/`scopes`), комбинирует RBAC с проверкой владения объектом (**Object-Level Authorization** прямо в `WHERE id = :id AND owner_id = :uid`) и покрывает негативные сценарии доступа (`403 Forbidden` для чужого пользователя) автотестами.
"""
    ),

    'К-103': (
        '3.5',
        'К-103. Хранение паролей_ хеширование, соль и.md',
        r"""📖 Перечитать конспект: Безопасное хранение паролей: почему SHA-256 опасен, зачем нужна соль (Salt) и как работают bcrypt и Argon2id >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Почему пароли нельзя хранить в открытом виде, шифровать или хешировать через `SHA-256`

1. **Открытый текст (`Plaintext`) и обратимое шифрование (`AES`)**: при первой же утечке базы данных или ключа шифрования все пароли пользователей (которые люди часто используют и на своей почте) оказываются в руках атакующих. Пароль должен храниться только в виде **необратимого криптографического хеша**.
2. **Почему быстрые хеши (`MD5`, `SHA-1`, `SHA-256`) категорически НЕ подходят для паролей?**
   `SHA-256` спроектирован быть сверхбыстрым: современная видеокарта (GPU) вычисляет **миллиарды `SHA-256` хешей в секунду**, подбирая обычный 8-символьный пароль за считанные минуты (**Brute Force**).

---

## Зачем нужна уникальная Соль (`Salt`) и как она уничтожает `Rainbow Tables`

Что если у 10 000 пользователей в вашей базе одинаковый пароль `"qwerty123"`? Без соли их хеши будут одинаковыми, и атакующий мгновенно взломает их всех по заранее вычисленной базе хешей (**Rainbow Table — Радужная таблица**).

**Соль (`Salt`)** — это криптографически случайная строка (16 байт), которая генерируется индивидуально для каждого пароля и склеивается с ним перед хешированием.
- Соль **не является секретом** — она хранится прямо внутри итоговой строки хеша в БД.
- Благодаря уникальной соли даже у двух пользователей с одинаковым паролем `"123456"` итоговые строки хешей в базе будут **абсолютно разными**, и радужные таблицы становятся бесполезны!

---

## Отраслевые стандарты: `bcrypt` и `Argon2id`

Для паролей используют специализированные **медленные адаптивные алгоритмы Key Derivation Functions (KDF)**:
- **`bcrypt`**: использует фактор стоимости `rounds` (например, `rounds=12` означает $2^{12} = 4096$ итераций, ~200–250 мс на одну проверку).
- **`Argon2id` (победитель Password Hashing Competition, рекомендация OWASP №1)**: защищает не только от перебора на процессоре (`time_cost`), но и требует выделения большого блока **оперативной памяти (`memory_cost`, например 64 МБ)** при каждом вычислении, делая массовый параллельный взлом на видеокартах (GPU/ASIC) физически невозможным!

Итоговая строка хеша в БД самодостаточна и хранит внутри себя и алгоритм, и параметры сложности, и соль, и сам хеш:
`$argon2id$v=19$m=65536,t=3,p=4$<base64_salt>$<base64_hash>`

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
stored_hash = ph.hash("MySuperSecretPass!2026")
print("Самодостаточная строка Argon2id в БД:", stored_hash)
print("Проверка верного пароля:", ph.verify(stored_hash, "MySuperSecretPass!2026"))

try:
    ph.verify(stored_hash, "wrong_password")
except VerifyMismatchError:
    print("Неверный пароль отклонён (VerifyMismatchError)!")
```

> **Junior vs Senior**:
> - **Junior**: Хеширует пароли через `hashlib.sha256(password.encode()).hexdigest()` без соли или придумывает одну общую статическую соль на весь проект, позволяя взломать дамп БД на GPU за считанные минуты.
> - **Senior**: Использует специализированные Memory-Hard KDF-алгоритмы (**`Argon2id`** или **`bcrypt`**), которые автоматически генерируют криптостойкую 16-байтную соль на каждый пароль, защищают от перебора на GPU/ASIC и поддерживают плавный `check_needs_rehash` при повышении параметров безопасности.
"""
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.7 · ЧАСТЬ VII: ИНТЕГРАЦИИ И RATE LIMITING (ОБОГАЩЕНИЕ К-224 И К-109)
    # ═══════════════════════════════════════════════════════════════════════════
    'К-224': (
        '3.7',
        'К-224. HTTP-клиенты в Python_ httpx и requests, таймауты, пулы соединений и ретраи.md',
        r"""📖 Перечитать конспект: HTTP-клиенты в Python: httpx и requests, таймауты, пулы соединений и ретраи >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Главная производственная ловушка: запрос без таймаута

В стандартных примерах почти всегда пишут `requests.get(url)`. В продакшене эта строчка — бомба замедленного действия: **по умолчанию у `requests` нет таймаута (`timeout=None`)**. Если внешний платёжный шлюз или микросервис принял TCP-соединение и завис, воркер вашего приложения будет ждать ответа вечно. Через несколько секунд все воркеры Gunicorn или потоки пула окажутся заблокированы, и ваш сервис упадёт целиком (каскадный отказ).

В `httpx` по умолчанию установлен таймаут 5 секунд, но полагаться на умолчания нельзя — таймаут всегда задают явно, разделяя **connect timeout** (время на установку TCP/TLS-соединения) и **read timeout** (время ожидания первого байта ответа от сервера):

```python
import requests
import httpx

# В requests кортеж: (connect_timeout, read_timeout) в секундах
response = requests.get(
    'https://api.example.com/v1/payments',
    timeout=(3.0, 10.0),
)

# В httpx объект Timeout с детальной настройкой
timeout_cfg = httpx.Timeout(10.0, connect=3.0, read=8.0, write=5.0)
with httpx.Client(timeout=timeout_cfg) as client:
    resp = client.get('https://api.example.com/v1/payments')

print("requests.get с timeout=(3.0, 10.0) -> статус:", response.status_code)
print("httpx.Client с Timeout(connect=3.0, read=8.0) -> статус:", resp.status_code)
```

---

## Пулы соединений: почему нельзя создавать клиент на каждый запрос

Вызов `requests.get()` или создание `httpx.AsyncClient()` внутри каждого входящего запроса заставляет Python на каждый вызов заново выполнять DNS-резолв, устанавливать TCP-соединение (3-way handshake) и проводить дорогостоящее TLS-рукопожатие. На 100 запросах в секунду это создаёт огромную задержку и исчерпывает эфемерные порты ОС.

**Правильный подход — переиспользование соединений (Connection Pooling / HTTP Keep-Alive)**:

- В синхронном коде используйте единый объект **`requests.Session()`** или **`httpx.Client()`**.
- В асинхронном коде (`FastAPI`, `asyncio`) создавайте единый **`httpx.AsyncClient()`** на уровне жизненного цикла приложения (`lifespan`) и передавайте его через Dependency Injection.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(5.0, connect=2.0),
        limits=limits,
    ) as client:
        app.state.http_client = client
        yield

app = FastAPI(lifespan=lifespan)

@app.get('/external-profile/{user_id}')
async def proxy_profile(user_id: int, request: Request):
    client: httpx.AsyncClient = request.app.state.http_client
    resp = await client.get(f'https://users.internal/api/v1/users/{user_id}')
    resp.raise_for_status()
    return resp.json()

print("FastAPI приложение с пулом соединений httpx.AsyncClient в lifespan готово! Маршрут:", proxy_profile.__name__)
```

---

## Обработка ошибок и `raise_for_status()`

Ни `requests`, ни `httpx` **не выбрасывают исключение при получении HTTP 4xx или 5xx** — они считают запрос технически выполненным и просто возвращают объект `Response` со свойством `status_code = 500`. Исключение выбрасывается автоматически только при сетевом сбое (`ConnectTimeout`, `ReadTimeout`, `ConnectError`).

Чтобы перевести HTTP-коды `4xx/5xx` в исключения Python (`HTTPError` / `HTTPStatusError`), вызывайте **`resp.raise_for_status()`**:

```python
import asyncio
import httpx

async def fetch_order(client: httpx.AsyncClient, order_id: int) -> dict:
    try:
        resp = await client.get(f'https://orders.internal/v1/orders/{order_id}')
        resp.raise_for_status()
        return resp.json()
    except httpx.TimeoutException as exc:
        raise RuntimeError('Внешний сервис заказов не ответил вовремя') from exc
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return {}
        raise

order_data = asyncio.run(fetch_order(httpx.AsyncClient(), 42))
print("Безопасный вызов fetch_order с raise_for_status():", order_data)
```

---

## Повторные попытки (Retries), Exponential Backoff и Jitter

Сеть ненадёжна: кратковременные всплески нагрузки или перезапуск контейнера часто приводят к одиночным ошибкам `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout` или `429 Too Many Requests`.

Однако наивный `for _ in range(3): client.get(...)` без паузы или с фиксированной паузой только добьёт падающий сервер: все клиенты ударят по нему одновременно (эффект **Thundering Herd** — «топот стада»).

Профессиональная стратегия ретраев строится на трёх правилах:

- **Экспоненциальная задержка (Exponential Backoff)**: пауза между попытками растёт экспоненциально ($1\text{ с}, 2\text{ с}, 4\text{ с}, 8\text{ с}$).
- **Случайный разброс (Jitter)**: к задержке добавляется случайный шум, чтобы рассинхронизировать волны повторных запросов от сотен клиентов.
- **Ретраить можно только идемпотентные запросы**: безопасно повторять `GET`, `HEAD`, `OPTIONS`, `PUT`, `DELETE`, а для `POST` — только при передаче того же самого заголовка `Idempotency-Key`. Ошибки клиента `400`, `401`, `403`, `404`, `422` повторять бессмысленно (кроме `429 Too Many Requests` с учётом заголовка `Retry-After`).

```python
import asyncio
import random
import httpx

RETRYABLE_STATUSES = {429, 502, 503, 504}

async def get_with_backoff(
    client: httpx.AsyncClient,
    url: str,
    max_attempts: int = 3,
    base_delay: float = 0.5,
) -> httpx.Response:
    for attempt in range(1, max_attempts + 1):
        try:
            response = await client.get(url)
            if response.status_code not in RETRYABLE_STATUSES or attempt == max_attempts:
                response.raise_for_status()
                return response
        except (httpx.ConnectError, httpx.ReadTimeout):
            if attempt == max_attempts:
                raise

        # Exponential backoff + Full Jitter
        max_sleep = base_delay * (2 ** (attempt - 1))
        sleep_time = random.uniform(0, max_sleep)
        await asyncio.sleep(sleep_time)

res_retry = asyncio.run(get_with_backoff(httpx.AsyncClient(), "https://api.example.com/v1/catalog"))
print("Запрос с Exponential Backoff + Jitter выполнен успешно, статус:", res_retry.status_code)
```

---

## Когда использовать `requests`, а когда `httpx`

- **`requests`** — классический стандарт для синхронных скриптов, CLI-утилит и синхронных воркеров Celery. Категорически **нельзя** вызывать внутри `async def` (блокирует Event Loop).
- **`httpx`** — современный клиент с почти идентичным API, который поддерживает как синхронный (`httpx.Client`), так и асинхронный (`httpx.AsyncClient`) режимы, протокол **HTTP/2** и прямое тестирование ASGI-приложений в памяти (`ASGITransport`).

> **Junior vs Senior**:
> - **Junior**: Вызывает `requests.get(url)` без `timeout` прямо внутри `async def`-хендлера FastAPI (намертво блокируя Event Loop при зависании внешнего API) и создаёт новый HTTP-клиент на каждый запрос без пула соединений.
> - **Senior**: Создаёт единый пул соединений `httpx.AsyncClient` в `lifespan` с явными `Timeout(connect=..., read=...)` и `Limits`, проверяет ответы через `raise_for_status()` и настраивает ретраи с **Exponential Backoff + Jitter** только для идемпотентных операций.
"""
    ),

    'К-109': (
        '3.7',
        'К-109. Rate Limiting и throttling_ ограничение.md',
        r"""📖 Перечитать конспект: Защита бэкенда от перегрузок: алгоритмы Rate Limiting (Fixed Window, Sliding Window, Token Bucket) и Redis >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Зачем нужен Rate Limiting (Ограничение частоты запросов)

Без ограничения частоты запросов один сломанный клиентский скрипт с бесконечным циклом `while True:`, агрессивный парсер конкурентов или атака перебора паролей (**Brute Force / DDoS**) за секунды исчерпает весь пул соединений базы данных и положит сервис для всех остальных пользователей.
При превышении лимита сервер обязан мгновенно вернуть статус **`429 Too Many Requests`** и заголовок **`Retry-After: <секунды>`**, подсказывающий клиенту, когда можно повторить попытку.

---

## Сравнение 3 классических алгоритмов Rate Limiting

### 1. `Fixed Window Counter` (Фиксированное окно)
Делит время на равные календарные отрезки (например, каждую минуту `12:00:00–12:00:59`) и хранит один счётчик.
- **Плюс**: требует минимум памяти (один ключ `INCR` в Redis).
- **Минус (Краевой всплеск / Boundary Burst)**: при лимите 100 запросов в минуту клиент может прислать 100 запросов в `12:00:59` и ещё 100 запросов в `12:01:00` — итого **200 запросов за 2 секунды**!

```python
import time

class FixedWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def allow(self, client_id: str) -> bool:
        now = time.time()
        window_start, count = self.requests.get(client_id, (now, 0))
        if now - window_start >= self.window_seconds:
            window_start, count = now, 0
        if count >= self.max_requests:
            return False
        self.requests[client_id] = (window_start, count + 1)
        return True

fw = FixedWindowLimiter(max_requests=2, window_seconds=60)
print("Fixed Window (лимит 2):", [fw.allow("ip_1") for _ in range(3)])
```

### 2. `Sliding Window Log` (Скользящее окно)
Хранит точные временные метки (`timestamps`) каждого запроса клиента (в локальном `deque` или в **Redis Sorted Set `ZSET`**) и при новом запросе удаляет метки старше `now - window_seconds`.
- **Плюс**: 100% точность на стыке любых секунд без двойных всплесков.

```python
import time
from collections import deque

class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def allow(self, client_id: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        timestamps = self.requests.setdefault(client_id, deque())
        while timestamps and now - timestamps[0] > self.window_seconds:
            timestamps.popleft()
        if len(timestamps) >= self.max_requests:
            return False
        timestamps.append(now)
        return True

sw = SlidingWindowLimiter(max_requests=2, window_seconds=10.0)
print("Sliding Window в t=0, 1, 2с:", sw.allow("u1", 0.0), sw.allow("u1", 1.0), sw.allow("u1", 2.0))
print("Sliding Window в t=11с (первый запрос вышел из окна):", sw.allow("u1", 11.0))
```

### 3. `Token Bucket` (Корзина с токенами)
В «ведро» ёмкостью `capacity` с постоянной скоростью `refill_rate` капают токены. Каждый запрос забирает 1 токен.
- **Плюс**: легально разрешает пользователю сделать короткий всплеск запросов (`burst` до `capacity`), но жёстко удерживает среднюю долгосрочную скорость `refill_rate`!

```python
class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = 0.0

    def allow(self, now: float) -> bool:
        elapsed = max(0.0, now - self.last_refill)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False

tb = TokenBucketLimiter(capacity=2, refill_rate=1.0)
print("Token Bucket в t=0 (2 токена в корзине):", tb.allow(0.0), tb.allow(0.0), tb.allow(0.0))
print("Token Bucket в t=1.0с (накапал 1 новый токен):", tb.allow(1.0))
```

---

## Распределённый Rate Limiter в Redis для нескольких воркеров

Когда бэкенд запущен в 10 контейнерах, локальный словарь в памяти процесса не защитит от превышения общего лимита. Поэтому счётчики хранят в **Redis**, используя атомарную команду **`INCR`** (или `Lua`-скрипт), чтобы избежать состояния гонки (`Race Condition`) между параллельными запросами:

```python
import redis
import time

r = redis.Redis()

def is_allowed_redis(client_id: str, max_requests: int = 3, window_seconds: int = 60) -> bool:
    bucket = int(time.time() // window_seconds)
    key = f"rate_limit:{client_id}:{bucket}"
    current = r.incr(key)
    if current == 1:
        r.expire(key, window_seconds)
    return current <= max_requests

results = [is_allowed_redis("user_42", max_requests=3) for _ in range(4)]
print("Проверка распределённого лимитера в Redis (лимит 3):", results)
```

> **Junior vs Senior**:
> - **Junior**: Хранит счётчики запросов в обычном словаре Python внутри процесса воркера (позволяя атакующему обойти лимит при балансировке между несколькими воркерами) и возвращает `400 Bad Request` или `500` при превышении частоты.
> - **Senior**: Реализует распределённый Rate Limiting в **Redis** (через атомарный `INCR` или `Lua`-скрипт для `Token Bucket` / `Sliding Window`), разделяет лимиты для анонимных IP и авторизованных `user_id`, и возвращает стандартный `429 Too Many Requests` с заголовком `Retry-After`.
"""
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # ЮНИТ 3.8 · ЧАСТЬ VIII: ТЕСТИРОВАНИЕ API (ОБОГАЩЕНИЕ К-226)
    # ═══════════════════════════════════════════════════════════════════════════
    'К-226': (
        '3.8',
        'К-226. Тестирование веб-приложений и API_ pytest, TestClient, AsyncClient и dependency_overrides.md',
        r"""📖 Перечитать конспект: Тестирование веб-приложений и API: pytest, TestClient, AsyncClient и dependency_overrides >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## Что именно нужно проверять в тестах API

Тестирование бэкенд-сервиса отличается от тестирования чистых алгоритмических функций. Когда клиент вызывает эндпоинт `POST /api/v1/orders`, ошибка может произойти на любом слое: неверный маршрут, ошибка валидации Pydantic/DRF Serializer, отказ проверки прав (`401`/`403`), нарушение уникальности в БД или сбой интеграции с внешним платёжным шлюзом.

Поэтому в бэкенд-разработке сочетают два уровня тестов:

- **Юнит-тесты бизнес-логики** — проверяют чистые функции и доменные сервисы в полной изоляции от веб-фреймворка и базы данных (миллисекунды на тест).
- **Интеграционные тесты эндпоинтов (API Tests)** — прогоняют HTTP-запрос через весь пайплайн фреймворка (роутинг ➔ Middleware ➔ валидация схем ➔ зависимости ➔ сериализация ответа) без реального открытия сетевого порта, прямо в памяти процесса.

---

## Тестирование FastAPI: `TestClient` и асинхронный `AsyncClient`

Для синхронного вызова эндпоинтов в тестах FastAPI предоставляет **`TestClient`** (обёртка над `httpx` из Starlette). Он позволяет отправлять запросы `client.get()`, `client.post()` напрямую в ASGI-приложение:

```python
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

@app.get('/items/{item_id}')
def read_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail='ID must be positive')
    return {'item_id': item_id, 'status': 'active'}

client = TestClient(app)

def test_read_item_success():
    response = client.get('/items/42')
    assert response.status_code == 200
    assert response.json() == {'item_id': 42, 'status': 'active'}

def test_read_item_invalid_id():
    response = client.get('/items/-5')
    assert response.status_code == 400
    assert response.json()['detail'] == 'ID must be positive'

test_read_item_success()
test_read_item_invalid_id()
print("Синхронные тесты TestClient прошли успешно: 200 OK и 400 Bad Request проверены!")
```

Если ваше приложение использует асинхронные фикстуры БД (`AsyncSession` SQLAlchemy, `asyncpg`), синхронный `TestClient` создаёт отдельный Event Loop, что часто приводит к конфликту циклов событий (`RuntimeError: Task got Future attached to a different loop`). В полностью асинхронных проектах используют **`httpx.AsyncClient`** в связке с **`ASGITransport`** и `pytest-asyncio`:

```python
import asyncio
import pytest
import httpx
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_create_order_async():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url='http://test') as ac:
        resp = await ac.post('/orders', json={'product_id': 10, 'qty': 2})
    assert resp.status_code == 201
    return resp.status_code

status = asyncio.run(test_create_order_async())
print("Асинхронный тест через httpx.AsyncClient + ASGITransport прошёл со статусом:", status)
```

---

## Главный инструмент тестирования FastAPI: `app.dependency_overrides`

На собеседовании обязательно спросят: *«Как протестировать эндпоинт, который зависит от базы данных, авторизации `get_current_user` и внешнего платного API, не поднимая продакшен-окружение?»*

Вместо хрупкого `unittest.mock.patch` по строковым путям импорта в FastAPI используется встроенный словарь **`app.dependency_overrides`**. Вы подменяете оригинальную функцию-зависимость на тестовую заглушку (фейковую БД, тестового пользователя или mock-сервис), а после теста очищаете словарь:

```python
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

def get_current_user():
    raise RuntimeError('В продакшене здесь декодируется реальный JWT')

@app.get('/profile')
def get_profile(user: dict = Depends(get_current_user)):
    return {'username': user['username'], 'role': user['role']}

# Подменяем зависимость на время теста через dependency_overrides:
app.dependency_overrides[get_current_user] = lambda: {
    'username': 'test_admin',
    'role': 'admin',
}
with TestClient(app) as c:
    resp = c.get('/profile')
    print("Ответ /profile с подменённой зависимостью:", resp.status_code, resp.json())
app.dependency_overrides.clear()
```

Почему `dependency_overrides` лучше обычного `mock.patch`:

- Не зависит от того, в каком именно модуле импортирована функция `get_current_user`.
- Работает одинаково для всех роутеров, вложенных зависимостей и `Security`-схем.
- Гарантирует чистую архитектуру со слабой связанностью (Loose Coupling).

---

## Изоляция базы данных в тестах (Transactional Rollback)

Если тест создаёт пользователя в БД, следующий тест не должен видеть эти данные — иначе тесты станут зависимыми от порядка запуска (**flaky tests**).

Золотой стандарт изоляции БД в интеграционных тестах:

- На старте тестовой сессии один раз создаются таблицы (или накатываются миграции Alembic / Django).
- Перед каждым отдельным тестом открывается **транзакция** (или `SAVEPOINT`), сессия передаётся в приложение через `dependency_overrides[get_db]`.
- В блоке `finally` фикстуры после `yield` вызывается **`await session.rollback()`** — база мгновенно возвращается в исходное состояние без медленного пересоздания таблиц (`DROP TABLE / CREATE TABLE`).

---

## Тестирование в Django и DRF (`pytest-django` и `APIClient`)

В экосистеме Django и Django REST Framework стандарт де-факто — связка **`pytest-django`**, **`APIClient`** из `rest_framework.test` и фабрик тестовых объектов **`factory_boy`**:

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_protected_endpoint_requires_auth(user_factory):
    client = APIClient()
    user = user_factory(username='alice')

    # Проверка без авторизации -> 401/403
    unauth_resp = client.get('/api/v1/orders/')
    assert unauth_resp.status_code in (401, 403)

    # Принудительная авторизация без генерации реального JWT/пароля
    client.force_authenticate(user=user)
    auth_resp = client.get('/api/v1/orders/')
    assert auth_resp.status_code == 200
    return unauth_resp.status_code, auth_resp.status_code

codes = test_protected_endpoint_requires_auth(lambda username: {"username": username})
print("Статусы DRF APIClient (без авторизации / с force_authenticate):", codes)
```

- Декоратор **`@pytest.mark.django_db`** разрешает тесту доступ к тестовой базе и автоматически оборачивает каждый тест в транзакцию с откатом (`rollback`) в конце.
- Метод **`client.force_authenticate(user=user)`** в DRF — прямой аналог подмены авторизации: он позволяет протестировать бизнес-логику и `permission_classes` эндпоинта, не тратя время на хеширование пароля через `bcrypt` и запрос к `/api/token/` в каждом тесте.

> **Junior vs Senior**:
> - **Junior**: Тестирует только «счастливый путь» (`200 OK`), мокает зависимости через хрупкие строковые пути `mock.patch("app.routers.users.get_db")`, а после каждого теста делает медленный `DROP TABLE / CREATE TABLE` или оставляет мусорные записи в БД.
> - **Senior**: Проверяет как позитивные, так и негативные сценарии (`400`, `401`, `403`, `404`, `422`), подменяет зависимости через `app.dependency_overrides` (или `force_authenticate` в DRF), использует `httpx.AsyncClient(transport=ASGITransport(app=app))` для асинхронных тестов и изолирует каждый тест быстрым откатом транзакции (`rollback`).
"""
    ),
}


NEW_MOD3_F_DECKS = {
    'Ф-282': (
        '3.1',
        'Ф-282. Бэкенд-фреймворки с нуля и валидация Pydantic v2 (FastAPI vs Django vs DRF vs Flask).md',
        [
            ("Какие 5 базовых задач берёт на себя любой бэкенд-фреймворк при обработке входящего HTTP-запроса?",
             "Маршрутизацию (Routing), парсинг и валидацию входных данных, проверку аутентификации/прав доступа, взаимодействие со слоем данных (ORM) и сериализацию HTTP-ответа"),
            ("В чём ключевое различие философии Django («Batteries Included») и микрофреймворков вроде Flask и FastAPI?",
             "Django включает из коробки собственную ORM, систему миграций, аутентификацию, формы и готовую админ-панель (`Django Admin`), тогда как Flask и FastAPI предоставляют лёгкое ядро, позволяя свободно выбирать ORM и библиотеки"),
            ("На каком серверном протоколе работают FastAPI, Django и Flask?",
             "FastAPI изначально построен на асинхронном протоколе **ASGI** (`Starlette` + `uvicorn`), Flask — на синхронном **WSGI** (`Werkzeug` + `gunicorn`), а Django поддерживает и классический WSGI, и ASGI"),
            ("Когда на проекте архитектурно выгоднее выбрать связку `Django + DRF`, а когда — `FastAPI`?",
             "`Django + DRF` выбирают для крупных бизнес-систем, где нужны готовая админка `Django Admin`, встроенная ORM и стандартная структура монолита; `FastAPI` выбирают для высоконагруженных I/O-bound микросервисов с `async/await` и строгими контрактами OpenAPI"),
            ("Почему ядро валидации `Pydantic v2` работает на порядки быстрее первой версии?",
             "В `Pydantic v2` всё вычислительное ядро парсинга и проверки типов (`pydantic-core`) переписано на компилируемом языке **Rust**"),
            ("В чём заключается принцип «Parse, don't validate» (Парсинг, а не просто проверка), реализуемый в Pydantic?",
             "Вместо разрозненных проверок сырого словаря `dict` входные данные на границе системы сразу преобразуются в строго типизированный объект с гарантированными типами атрибутов"),
            ("Какими методами в `Pydantic v2` были заменены устаревшие методы `.dict()`, `.json()` и `.parse_obj()` из Pydantic v1?",
             "`.dict()` заменён на **`model_dump()`**, `.json()` — на **`model_dump_json()`**, а `.parse_obj()` и `.from_orm()` — на **`model_validate()`**"),
            ("Чем в `Pydantic v2` отличается декоратор `@field_validator` от `@model_validator(mode='after')`?",
             "`@field_validator` проверяет или нормализует одно конкретное поле, а `@model_validator(mode='after')` получает уже собранный экземпляр модели и позволяет сверять несколько полей друг с другом"),
            ("Зачем при обработке `PATCH`-запроса (частичного обновления) вызывают `payload.model_dump(exclude_unset=True)`?",
             "Чтобы получить словарь только из тех полей, которые клиент явно прислал в JSON-теле запроса, и случайно не затереть остальные колонки в БД значениями по умолчанию (`None`)"),
            ("Для чего в `Pydantic v2` в модель ответа добавляют настройку `model_config = ConfigDict(from_attributes=True)`?",
             "Чтобы схема могла читать данные напрямую из атрибутов ORM-объекта (`user.email`), а не только по ключам словаря (`user['email']`)"),
            ("Почему в FastAPI опасно возвращать из эндпоинта объект БД или словарь без указания `response_model`?",
             "Без выходной схемы `response_model` в JSON-ответ клиенту могут утечь внутренние поля таблицы БД, такие как `password_hash` или служебные флаги"),
            ("Как FastAPI автоматически отличает Path-параметры, Query-параметры и тело запроса (`Request Body`) в аргументах функции эндпоинта?",
             "Параметры, указанные в `{...}` маршрута — это `Path`; примитивные типы (`int`, `str`), не указанные в пути — это `Query`; а классы, унаследованные от `pydantic.BaseModel` — это JSON `Body`"),
        ]
    ),

    'Ф-283': (
        '3.3',
        'Ф-283. Представления и маршрутизация в DRF_ APIView, GenericAPIView, Mixins, ModelViewSet, @action и Routers.md',
        [
            ("Чем объект `request` внутри `APIView` в Django REST Framework отличается от стандартного `django.http.HttpRequest`?",
             "DRF оборачивает запрос в `rest_framework.request.Request`, добавляя единый атрибут `request.data` (парсит JSON, FormData и Multipart для `POST/PUT/PATCH`) и `request.query_params`"),
            ("Какую задачу выполняет класс `rest_framework.response.Response` по сравнению с обычным `JsonResponse`?",
             "Он реализует `Content Negotiation` (согласование контента): выбирает рендерер на основе заголовка `Accept` клиента, отдавая либо чистый JSON, либо интерактивный веб-интерфейс Browsable API"),
            ("Что добавляет класс `GenericAPIView` по сравнению с базовым `APIView` в DRF?",
             "Стандартную привязку к слою данных и схемам (`queryset`, `serializer_class`, `lookup_field`), методы `get_queryset()`, `get_object()`, а также встроенную поддержку пагинации и фильтрации"),
            ("Какие 5 классов-примесей (`Mixins`) в DRF реализуют базовые операции CRUD?",
             "`ListModelMixin` (`list`), `CreateModelMixin` (`create`), `RetrieveModelMixin` (`retrieve`), `UpdateModelMixin` (`update`) и `DestroyModelMixin` (`destroy`)"),
            ("Чем `ViewSet` и `ModelViewSet` концептуально отличаются от `APIView` и `GenericAPIView`?",
             "В `APIView` методы называются по HTTP-глаголам (`get`, `post`), а во `ViewSet` — по высокоуровневым действиям (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`), которые привязываются к URL через `Router`"),
            ("Когда вместо `ModelViewSet` следует использовать `ReadOnlyModelViewSet`?",
             "Когда ресурс через API должен быть доступен только на чтение: `ReadOnlyModelViewSet` включает только действия `list` (`GET /items/`) и `retrieve` (`GET /items/{id}/`), полностью запрещая создание, изменение и удаление"),
            ("Зачем во `ViewSet` переопределяют метод `get_queryset(self)` вместо использования статического атрибута `queryset`?",
             "Чтобы динамически фильтровать выборку под текущего пользователя (`self.request.user`), применять `select_related`/`prefetch_related` или менять запрос в зависимости от `self.action`"),
            ("Как во `ViewSet` использовать разные сериализаторы для чтения списка (`list`) и для создания записи (`create`)?",
             "Переопределить метод `get_serializer_class(self)` и возвращать нужный класс сериализатора в зависимости от текущего действия `self.action`"),
            ("Какую роль играет метод-хук `perform_create(self, serializer)` внутри `ModelViewSet`?",
             "Он вызывается внутри действия `create` после успешной валидации и позволяет передать дополнительные серверные поля при сохранении, например `serializer.save(author=self.request.user)`"),
            ("Для чего во `ViewSet` используется декоратор `@action` и чем отличается `detail=True` от `detail=False`?",
             "`@action` добавляет кастомный бизнес-маршрут во `ViewSet`: при `detail=True` маршрут применяется к одному объекту и содержит `{pk}` (`/orders/{pk}/cancel/`), а при `detail=False` — ко всей коллекции (`/orders/stats/`)"),
            ("В чём разница между `SimpleRouter` и `DefaultRouter` в Django REST Framework?",
             "`DefaultRouter` расширяет `SimpleRouter`, автоматически создавая корневой маршрут API (`APIRootView` со ссылками на все ресурсы) и поддерживая суффиксы форматов (`.json`)"),
            ("Когда в проекте на DRF следует явно указать аргумент `basename` при регистрации `router.register('orders', OrderViewSet, basename='order')`?",
             "Когда во `ViewSet` не задан статический атрибут `queryset` (а определён только динамический метод `get_queryset()`), из-за чего роутер не может сам определить имя модели для генерации имён URL"),
        ]
    ),

    'Ф-284': (
        '3.3',
        'Ф-284. Безопасность, фильтрация и документация в DRF_ Authentication, Permissions, django-filter, Pagination и drf-spectacular.md',
        [
            ("В каком порядке выполняются проверки `Authentication`, `Permissions` и `Throttling` при входе запроса в `APIView` / `ViewSet`?",
             "Сначала выполняется `Authentication` (определяет `request.user` и `request.auth`), затем `Permissions` (проверяет права доступа) и затем `Throttling` (проверяет лимит частоты запросов)"),
            ("В чём разница между методами `has_permission(request, view)` и `has_object_permission(request, view, obj)` в классе `BasePermission`?",
             "`has_permission` проверяет общий доступ к эндпоинту на входе, а `has_object_permission` вызывается внутри `get_object()` для проверки прав на конкретную загруженную из БД запись `obj` (защита от BOLA/IDOR)"),
            ("Почему метод `has_object_permission` НЕ вызывается при запросе списка объектов (`list` — `GET /orders/`)?",
             "Из соображений производительности DRF не запускает проверку прав в цикле для тысяч строк списка; фильтрация списка по владельцу должна выполняться на уровне SQL в `get_queryset()`"),
            ("Что нужно обязательно вызвать внутри кастомного `@action(detail=True)`, чтобы сработала объектная проверка `has_object_permission`?",
             "Получать объект через стандартный метод `obj = self.get_object()`, который внутри себя автоматически вызывает `self.check_object_permissions(request, obj)`"),
            ("Как в DRF комбинируются классы разрешений через побитовые операторы `&` (И), `|` (ИЛИ) и `~` (НЕ)?",
             "В `permission_classes` можно объединять классы, например `permission_classes = [IsAuthenticated & (IsAdminUser | IsOwner)]`, создавая составные правила доступа"),
            ("Какие три стандартных бэкенда фильтрации (`filter_backends`) используются в DRF для фильтрации, текстового поиска и сортировки?",
             "`DjangoFilterBackend` (точная фильтрация по полям и `FilterSet`), `SearchFilter` (текстовый поиск по `?search=`) и `OrderingFilter` (сортировка по `?ordering=`)"),
            ("Какие три класса пагинации встроены в DRF и чем они отличаются?",
             "`PageNumberPagination` (`?page=2`), `LimitOffsetPagination` (`?limit=20&offset=40`) и `CursorPagination` (курсорная пагинация по индексу без `OFFSET` для больших таблиц и лент)"),
            ("Какие требования накладывает `CursorPagination` в DRF на выборку `QuerySet`?",
             "Наличие индексированного, монотонно изменяющегося поля сортировки `ordering` (обычно `-created_at` или `-id`), по которому строится непрозрачный курсор"),
            ("Чем отличаются классы `AnonRateThrottle`, `UserRateThrottle` и `ScopedRateThrottle` в DRF?",
             "`AnonRateThrottle` ограничивает гостей по IP-адресу, `UserRateThrottle` — авторизованных пользователей по `user.id`, а `ScopedRateThrottle` задаёт индивидуальный лимит для конкретных чувствительных маршрутов (`throttle_scope`)"),
            ("Какая библиотека является современным стандартом генерации спецификации OpenAPI 3.0 и Swagger UI в проектах на DRF?",
             "Библиотека `drf-spectacular`, использующая декоратор `@extend_schema` для точного описания входных/выходных схем, параметров и кодов ответа"),
            ("Чем HTTP-ответ `401 Unauthorized` отличается от `403 Forbidden` в механике работы DRF?",
             "`401 Unauthorized` возвращается, когда запрос не прошёл аутентификацию (токен отсутствует или истёк), а `403 Forbidden` — когда пользователь опознан, но `Permission`-класс запретил ему действие"),
            ("Как в тестах DRF (`APIClient`) мгновенно авторизовать тестового пользователя без реальной генерации JWT или логина по паролю?",
             "Вызвать метод `client.force_authenticate(user=test_user)` перед отправкой тестового запроса"),
        ]
    ),

    'Ф-285': (
        '3.4',
        'Ф-285. Микрофреймворк Flask с нуля_ маршруты, request, контексты (g, current_app), Blueprints и Application Factory.md',
        [
            ("На каких двух базовых библиотеках построен микрофреймворк Flask?",
             "На WSGI-инструментарии **`Werkzeug`** (маршрутизация, объекты `Request`/`Response`) и шаблонизаторе **`Jinja2`**"),
            ("Как во Flask 2+ безопасно прочитать целочисленный query-параметр `?page=2` со значением по умолчанию `1`?",
             "Через `request.args.get('page', default=1, type=int)` — если передана нечисловая строка, Flask безопасно вернёт `default=1` вместо выброса `ValueError`"),
            ("Чем вызов `request.get_json(silent=True)` отличается от `request.get_json()` при получении невалидного JSON от клиента?",
             "Без `silent=True` Flask автоматически выбрасывает HTTP-ошибку `400 Bad Request`, а с `silent=True` возвращает `None`, позволяя обработать ошибку вручную"),
            ("Почему импортируемый глобально объект `from flask import request` потокобезопасен и не смешивает данные параллельных запросов?",
             "`request` — это не обычный объект, а контекстно-локальный прокси (`LocalProxy`), который через `ContextVar` обращается к изолированному контексту активного потока или корутины"),
            ("Какие два прокси-объекта во Flask относятся к `Application Context`, а какие два — к `Request Context`?",
             "К `Application Context` относятся `current_app` и `g`; к `Request Context` относятся `request` и `session`"),
            ("Для чего предназначен объект `flask.g` и каково время жизни данных внутри него?",
             "`flask.g` — это временное хранилище данных в рамках **одного текущего запроса** (или CLI-команды), которое полностью очищается при завершении контекста"),
            ("Почему возникает ошибка `RuntimeError: Working outside of application/request context` и как её исправить в фоновом скрипте или тесте?",
             "Ошибка возникает при обращении к `current_app`, `db.session` или `request` вне активного HTTP-запроса; для исправления код оборачивают в блок `with app.app_context():` или `with app.test_request_context():`"),
            ("Какую архитектурную проблему решает использование `Blueprint` в растущем Flask-приложении?",
             "Позволяет разбить монолитный файл с роутами на независимые доменные модули со своими префиксами URL и устраняет проблему циклических импортов (`Circular Imports`) с объектом `app`"),
            ("В чём заключается паттерн `Application Factory` (`def create_app():`) во Flask?",
             "Создание и настройка экземпляра `Flask` внутри фабричной функции вместо глобальной переменной модуля, что позволяет создавать изолированные экземпляры с разными конфигами для продакшена и `pytest`"),
            ("Как правильно подключать расширения (например, `db = SQLAlchemy()`) при использовании паттерна `Application Factory`?",
             "Создать экземпляр расширения без аргументов в `extensions.py`, а внутри `create_app()` привязать его к созданному приложению вызовом `db.init_app(app)`"),
            ("Чем отличаются хуки `@app.before_request`, `@app.after_request` и `@app.teardown_appcontext` во Flask?",
             "`before_request` вызывается до роута (может прервать запрос), `after_request` модифицирует готовый `response` при отсутствии необработанных ошибок, а `teardown_appcontext` выполняется **всегда** в самом конце для очистки ресурсов (например, закрытия `db.session`)"),
            ("Как во Flask централизованно перехватывать доменные исключения Python и возвращать клиенту структурированный JSON вместо HTML-страницы ошибки?",
             "Зарегистрировать обработчик через декоратор `@app.errorhandler(CustomError)` и возвращать из него кортеж `(jsonify({...}), status_code)`"),
        ]
    ),
}
