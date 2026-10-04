# -*- coding: utf-8 -*-
"""
Обогащение и нормализация Модуля 05 («05 · 🗄️ Базы данных», Юниты 5.1–5.6):
1. Перемещение 7 колод Ф-* (Ф-111, Ф-147, Ф-149, Ф-160, Ф-161, Ф-164, Ф-165) в целевые юниты.
2. Синхронизация путей в `00 · 🗺️ Карта Мастерства.md` и привязка Ф-110, Ф-111 к Навыку 5.5.1.
3. Обогащение односложных ответов в карточках Ф-143, Ф-147, Ф-150, Ф-168.
4. Полная вычитка и перезапись с нуля для новичка всех 32 конспектов К-124..К-155:
   - Ментальная модель из реальной жизни в начале каждого конспекта;
   - Минимум 3–4 микро-шага (разделённых `---`);
   - Наглядные ASCII-схемы в блоках ```text;
   - Сводные Markdown-таблицы;
   - Блоки `> **Junior vs Senior**:` (рендерятся в `.jvs-grid`);
   - 100% самодостаточные исполняемые примеры Python 3.13 (`sqlite3.connect(':memory:')` и др.) с `print()`.
"""
import os
import shutil

BASE_DB = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED\05 · 🗄️ Базы данных'

NOTES_CONTENT = {
    # =========================================================================
    # ЮНИТ 5.1 · SQL основы (К-124 .. К-128)
    # =========================================================================
    os.path.join('Юнит 5.1 · SQL основы', '📚 Конспекты', 'К-124. SQL-запрос_ синтаксис и порядок выполнения.md'): r'''📖 Перечитать конспект: SQL-запрос: синтаксис и порядок выполнения >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Декларативная природа SQL и два порядка чтения

> **Ментальная модель — «Заказ в ресторане против работы кухни»**: Когда вы делаете заказ официанту, вы сначала называете **блюдо** (`SELECT`), а потом уточняете детали («из летнего меню» — `FROM`, «без лука» — `WHERE`). Но повар на кухне работает в другом порядке: сначала он открывает холодильник (`FROM`), отбирает свежие продукты (`WHERE`), группирует заготовки (`GROUP BY`), и только в самом конце выкладывает блюдо на тарелку (`SELECT`) и ставит на поднос (`ORDER BY`, `LIMIT`).

**SQL (Structured Query Language)** — декларативный язык: вы описываете, **какой результат** хотите получить, а планировщик СУБД сам решает, *как* эффективнее прочитать данные с диска.

Главный секрет понимания SQL для новичка: **порядок написания запроса (Lexical Order)** НЕ совпадает с **порядком его выполнения движком базы данных (Logical Execution Order)**!

```text
Как мы ПИШЕМ запрос (Синтаксис):        Как СУБД ВЫПОЛНЯЕТ запрос (Под капотом):
  1. SELECT name, price AS cost           1. FROM products        (Откуда берём строки?)
  2. FROM products                        2. JOIN categories      (С чем склеиваем?)
  3. WHERE price > 100                    3. WHERE price > 100    (Какие строки выкинуть сразу?)
  4. GROUP BY category_id                 4. GROUP BY category_id (Как схлопнуть в корзины?)
  5. HAVING COUNT(*) > 2                  5. HAVING COUNT(*) > 2  (Какие корзины оставить?)
  6. ORDER BY cost DESC                   6. SELECT ... AS cost   (Вычислить столбцы и алиасы!)
  7. LIMIT 5                              7. ORDER BY cost DESC   (Отсортировать тарелки)
                                          8. LIMIT 5              (Отдать первые 5 строк)
```

---

## 2. Таблица этапов выполнения и правила видимости алиасов (`AS`)

Поскольку шаг `SELECT` выполняется только **шестым по счёту**, псевдонимы столбцов (`SELECT price * 1.2 AS price_with_vat`) ещё **не существуют** на этапах `WHERE`, `GROUP BY` и `HAVING`, но уже **доступны** в `ORDER BY`!

| Шаг выполнения | Оператор SQL | Что делает движок БД | Видит ли алиасы из `SELECT`? |
| :--- | :--- | :--- | :--- |
| **1–2** | `FROM` + `JOIN` | Загружает исходные таблицы и склеивает их по условию `ON` | ❌ Нет |
| **3** | `WHERE` | Построчно фильтрует сырые данные до любой группировки | ❌ Нет (обращение вызовет ошибку) |
| **4** | `GROUP BY` | Схлопывает оставшиеся строки в группы по уникальным значениям | ❌ В стандарте SQL нет |
| **5** | `HAVING` | Фильтрует уже сформированные группы по результатам агрегаций | ❌ Нет |
| **6** | `SELECT` (+ `DISTINCT`) | Вычисляет итоговые выражения, создаёт алиасы `AS`, удаляет дубликаты | ✅ Создаёт алиасы здесь |
| **7** | `ORDER BY` | Сортирует финальный набор (`ASC` по возрастанию, `DESC` по убыванию) | ✅ Да, видит алиасы `SELECT` |
| **8** | `LIMIT` / `OFFSET` | Отсекает верхушку результата для постраничного вывода (пагинации) | — |

---

## 3. Сортировка `NULL` и ловушки глубокого `OFFSET`

- **`NULL` — это не ноль и не пустая строка**, а маркер *«значение неизвестно»*. Проверять его через `= NULL` или `!= NULL` бесполезно (результатом будет `UNKNOWN`, и строка отфильтруется). Используйте строго `IS NULL` и `IS NOT NULL`.
- При сортировке (`ORDER BY`) в PostgreSQL значения `NULL` считаются «больше всех» и по умолчанию при `ASC` всплывают в конец, а при `DESC` — в самое начало! Чтобы явно управлять их позицией, используйте `NULLS LAST` или `NULLS FIRST`.
- Оператор `OFFSET 100000 LIMIT 10` заставляет базу данных прочитать и отсортировать `100 010` строк, чтобы выбросить первые `100 000` в мусорную корзину. На больших таблицах вместо `OFFSET` используют **Keyset (Cursor) Pagination**: `WHERE id > :last_seen_id ORDER BY id ASC LIMIT 10`.

> **Junior vs Senior**:
> - **Junior**: Пишет `SELECT price * 0.9 AS disc_price FROM items WHERE disc_price < 500`, получает `OperationalError: no such column: disc_price` и пытается обернуть запрос в лишний подзапрос. Кроме того, использует `SELECT *` и `OFFSET 50000` на миллионах строк.
> - **Senior**: Помнит физический порядок выполнения (`FROM -> WHERE -> SELECT -> ORDER BY`), вычисляет условие в `WHERE price * 0.9 < 500`, явно перечисляет нужные колонки в `SELECT` (для работы *Covering Index*) и заменяет глубокий `OFFSET` на пагинацию по курсору (`WHERE id > last_id`).

---

## 4. Практикум в Python 3.13: проверяем порядок выполнения на `sqlite3`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER)")
    conn.executemany(
        "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
        [
            ("Клавиатура Keychron", "peripherals", 120),
            ("Мышь Logitech", "peripherals", 80),
            ("Монитор Dell 4K", "displays", 450),
            ("Монитор LG Ultra", "displays", 380),
            ("Кабель HDMI", "cables", 15),
        ],
    )

    # Демонстрируем полный конвейер: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
    query = """
    SELECT
        category,
        COUNT(*) AS items_cnt,
        ROUND(AVG(price), 1) AS avg_price
    FROM products
    WHERE price >= 50
    GROUP BY category
    HAVING COUNT(*) >= 2
    ORDER BY avg_price DESC
    LIMIT 5
    """
    rows = conn.execute(query).fetchall()
    for cat, cnt, avg_p in rows:
        print(f"Категория: {cat:12s} | Товаров: {cnt} | Средняя цена: ${avg_p}")
```
''',

    os.path.join('Юнит 5.1 · SQL основы', '📚 Конспекты', 'К-125. WHERE и HAVING_ фильтрация строк и групп.md'): r'''📖 Перечитать конспект: WHERE и HAVING: фильтрация строк и групп >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. В чём фундаментальная разница между `WHERE` и `HAVING`?

> **Ментальная модель — «Фейсконтроль на входе против аттестации отдела»**:
> - **`WHERE` — это охрана на входе в здание**: она проверяет каждого сотрудника **поодиночке** до того, как люди разойдутся по кабинетам (например, «пропускать только сотрудников со стажем > 1 года»).
> - **`HAVING` — это проверка целого кабинета после того, как все расселись (`GROUP BY`)**: например, «оставить в отчёте только те отделы, где собралось минимум 5 человек (`HAVING COUNT(*) >= 5`) и средний оклад выше 150 000 ₽».

```text
Сырая таблица (employees)
  │
  ▼  [Шаг 1: WHERE salary >= 1000]  <-- Отсекает отдельные СТРОКИ (индексы работают!)
Отфильтрованные строки
  │
  ▼  [Шаг 2: GROUP BY dept]         <-- Схлопывает строки в ГРУППЫ (по одной на отдел)
Группы отделов (IT, HR, Sales)
  │
  ▼  [Шаг 3: HAVING COUNT(*) >= 2]  <-- Отсекает целые ГРУППЫ по агрегатам (COUNT, SUM, AVG)
Финальный отчёт
```

---

## 2. Сравнительная таблица `WHERE` vs `HAVING`

| Критерий | Оператор `WHERE` | Оператор `HAVING` |
| :--- | :--- | :--- |
| **Момент выполнения** | **До** `GROUP BY` и вычисления агрегатов | **После** `GROUP BY` и вычисления агрегатов |
| **Объект фильтрации** | Отдельные физические строки таблицы | Сформированные группы строк (корзины) |
| **Агрегатные функции (`COUNT`, `SUM`, `AVG`)** | ❌ Запрещены (`WHERE COUNT(*) > 1` вызовет ошибку синтаксиса) | ✅ Разрешены и являются главной целью `HAVING` |
| **Использование B-Tree индексов** | ✅ Да! Снижает объём чтения с диска и памяти | ❌ Нет, фильтрует уже сгруппированный в памяти результат |

---

## 3. Золотое правило совместного использования и элегантный `FILTER (WHERE ...)`

Можно ли использовать `WHERE` и `HAVING` в одном запросе? **Не только можно, но и нужно!**
Представьте задачу: *«Найти отделы, в которых сумма зарплат активных сотрудников за 2026 год превышает 1 000 000 ₽»*.
1. Условие `status = 'active' AND year = 2026` относится к **конкретной строке** — ставим его в `WHERE`, чтобы не тащить уволенных сотрудников и старые годы в группировку.
2. Условие `SUM(salary) > 1000000` можно узнать только **после сложения зарплат отдела** — ставим его в `HAVING`.

В PostgreSQL и современном SQLite (3.30+) также есть конструкция **`FILTER (WHERE ...)`** прямо внутри агрегатной функции — она позволяет считать несколько разных метрик за один проход таблицы без громоздких `CASE WHEN`:

```sql
SELECT
    dept,
    COUNT(*) AS total_staff,
    COUNT(*) FILTER (WHERE grade = 'Senior') AS seniors_cnt
FROM employees
GROUP BY dept;
```

> **Junior vs Senior**:
> - **Junior**: Фильтрует столбец группировки внутри `HAVING`: пишет `SELECT dept, SUM(salary) FROM staff GROUP BY dept HAVING dept = 'Backend'`. База данных впустую группирует и суммирует зарплаты всех 50 отделов компании, чтобы в конце оставить один!
> - **Senior**: Выносит любые построчные проверки в `WHERE dept = 'Backend'` до `GROUP BY`, позволяя СУБД применить индекс и прочитать с диска только нужный отдел, а в `HAVING` оставляет исключительно условия на агрегатные функции (`HAVING SUM(salary) > 500000`).

---

## 4. Практикум в Python 3.13: `WHERE` + `GROUP BY` + `HAVING` и `FILTER`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, client TEXT, status TEXT, amount INTEGER)")
    conn.executemany(
        "INSERT INTO orders (client, status, amount) VALUES (?, ?, ?)",
        [
            ("Alice", "paid", 500),
            ("Alice", "paid", 700),
            ("Alice", "cancelled", 9000),
            ("Bob", "paid", 300),
            ("Charlie", "paid", 800),
            ("Charlie", "paid", 600),
        ],
    )

    # 1. WHERE отсекает отменённые заказы ДО группировки, а HAVING оставляет VIP-клиентов с суммой >= 1000
    sql = """
    SELECT
        client,
        COUNT(*) AS paid_orders,
        SUM(amount) AS total_spent
    FROM orders
    WHERE status = 'paid'
    GROUP BY client
    HAVING SUM(amount) >= 1000
    ORDER BY total_spent DESC
    """
    vip_clients = conn.execute(sql).fetchall()
    print("VIP-клиенты (WHERE + HAVING):", vip_clients)

    # 2. Агрегация с FILTER (WHERE ...) за один проход таблицы:
    sql_filter = """
    SELECT
        client,
        SUM(amount) FILTER (WHERE status = 'paid') AS paid_sum,
        COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled_cnt
    FROM orders
    GROUP BY client
    ORDER BY client
    """
    for client, paid_sum, canc_cnt in conn.execute(sql_filter):
        print(f"{client:7s} -> Оплачено: {paid_sum} ₽ | Отменено заказов: {canc_cnt}")
```
''',

    os.path.join('Юнит 5.1 · SQL основы', '📚 Конспекты', 'К-126. SQL JOIN_ объединение таблиц.md'): r'''📖 Перечитать конспект: SQL JOIN: объединение таблиц >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Зачем нужны `JOIN` и как устроена склейка таблиц?

> **Ментальная модель — «Сверка списка гостей и списка оплаченных билетов»**: Представьте две таблицы: слева `users` (все зарегистрированные люди), справа `orders` (купленные билеты с колонкой `user_id`). Операция `JOIN` — это диспетчер, который берёт человека из левого списка, ищет его `id` в правом списке билетов и склеивает их в одну широкую строку. Разные виды `JOIN` отличаются только одним правилом: **что делать с «одиночками», которым не нашлось пары в соседней таблице?**

```text
Таблица A (users)        Таблица B (orders)
+----+---------+         +----+---------+--------+
| id | name    |         | id | user_id | amount |
+----+---------+         +----+---------+--------+
| 1  | Alice   | <-----> | 10 |    1    |  500   |  (Есть пара в обеих таблицах)
| 2  | Bob     |         | 11 |   99    |  300   |  (Заказ-сирота: user_id=99 нет в A)
+----+---------+         +----+---------+--------+
  ^ (У Боба нет заказов)

INNER JOIN: только Alice (id=1)                  [Пересечение A ∩ B]
LEFT JOIN : Alice + Bob (у Боба orders = NULL)   [Все из A + совпадения из B]
RIGHT JOIN: Alice + заказ #11 (users = NULL)     [Все из B + совпадения из A]
FULL JOIN : Alice + Bob + заказ #11              [Объединение A ∪ B]
```

---

## 2. Все 6 видов `JOIN`: шпаргалка разработчика

| Тип объединения | Что попадает в результат | Что будет в колонках при отсутствии пары | Главный практический сценарий |
| :--- | :--- | :--- | :--- |
| **`INNER JOIN`** (или просто `JOIN`) | Строго те строки, где ключ совпал **и в левой, и в правой** таблице | Строки без пары полностью отбрасываются | Получить заказы вместе с именем существующего покупателя |
| **`LEFT [OUTER] JOIN`** | **100% строк левой таблицы** + совпадения из правой | В колонках правой таблицы подставится `NULL` | Вывести всех клиентов, включая тех, кто ещё ничего не купил |
| **`LEFT JOIN ... WHERE b.id IS NULL`** | Только строки левой таблицы, которым **не нашлось пары** справа (*Anti-Join*) | Правая часть равна `NULL` | Найти пользователей без единого заказа или товары без продаж |
| **`RIGHT [OUTER] JOIN`** | **100% строк правой таблицы** + совпадения из левой | В колонках левой таблицы подставится `NULL` | Редко используется (проще поменять таблицы местами и написать `LEFT JOIN`) |
| **`FULL [OUTER] JOIN`** | Все строки из обеих таблиц (и пары, и одиночки с обеих сторон) | `NULL` с той стороны, где не нашлось пары | Сверка двух реестров (например, платежей банка и заказов магазина) |
| **`CROSS JOIN`** | Декартово произведение: каждая строка `A` склеивается с каждой строкой `B` ($N \times M$ строк) | Условие `ON` не пишется | Генерация сетки всех размеров одежды и всех цветов (`5 × 8 = 40` комбинаций) |
| **`SELF JOIN`** | Таблица соединяется **сама с собой** через два разных алиаса (`FROM emp e LEFT JOIN emp m ON e.manager_id = m.id`) | `NULL` у директора (нет начальника) | Дерево сотрудников «Подчинённый → Руководитель», категории товаров |

---

## 3. Смертельная ловушка: условие в `ON` против условия в `WHERE` при `LEFT JOIN`

Представьте, что вы хотите вывести **всех пользователей** и сумму их *оплаченных* заказов (`status = 'paid'`).
Если написать:
```sql
-- ❌ ОШИБКА: превращает LEFT JOIN в обычный INNER JOIN!
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.status = 'paid';
```
Почему Bob (у которого нет заказов) исчезнет из результата? Потому что после `LEFT JOIN` у Боба в колонке `o.status` лежит `NULL`. Затем шаг `WHERE` проверяет `NULL = 'paid'` $\implies$ `UNKNOWN` и **выбрасывает строку Боба**!
Чтобы сохранить всех пользователей из левой таблицы, фильтр для правой таблицы нужно писать **внутри `ON`**:
```sql
-- ✅ ПРАВИЛЬНО: Bob останется в выдаче с NULL в колонке amount!
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'paid';
```

> **Junior vs Senior**:
> - **Junior**: Делает `LEFT JOIN`, а затем фильтрует колонку правой таблицы в секции `WHERE o.status = 'paid'`, не замечая, что этим полностью уничтожил смысл `LEFT JOIN` (все строки с `NULL` отсеялись).
> - **Senior**: Фильтрует правую таблицу прямо в предикате соединения (`LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'paid'`), использует Anti-Join (`LEFT JOIN ... WHERE o.id IS NULL` или `NOT EXISTS`) для поиска «сирот» и следит, чтобы на колонке внешнего ключа (`orders.user_id`) обязательно стоял B-Tree индекс.

---

## 4. Практикум в Python 3.13: `INNER`, `LEFT`, Anti-Join и `SELF JOIN`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)")
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT, amount INTEGER)")

    conn.executemany("INSERT INTO users VALUES (?, ?, ?)", [(1, "Alice (CEO)", None), (2, "Bob", 1), (3, "Charlie", 2)])
    conn.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?)",
        [(101, 1, "paid", 500), (102, 2, "cancelled", 200)],
    )

    # 1. Anti-Join: кто из пользователей вообще не делал заказов?
    no_orders = conn.execute("""
        SELECT u.name
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE o.id IS NULL
    """).fetchall()
    print("Пользователи без заказов (Anti-Join):", [r[0] for r in no_orders])

    # 2. Правильный LEFT JOIN с условием в ON (сохраняет всех пользователей!)
    left_paid = conn.execute("""
        SELECT u.name, COALESCE(SUM(o.amount), 0) AS paid_total
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'paid'
        GROUP BY u.id, u.name
        ORDER BY u.id
    """).fetchall()
    print("Оплаченные суммы (LEFT JOIN + ON):", left_paid)

    # 3. SELF JOIN: выводим каждого сотрудника и имя его руководителя
    hierarchy = conn.execute("""
        SELECT e.name AS employee, COALESCE(m.name, '— Нет (Топ-менеджер) —') AS manager
        FROM users e
        LEFT JOIN users m ON e.manager_id = m.id
    """).fetchall()
    for emp, mgr in hierarchy:
        print(f"Сотрудник: {emp:13s} | Руководитель: {mgr}")
```
''',

    os.path.join('Юнит 5.1 · SQL основы', '📚 Конспекты', 'К-127. DDL_ жизненный цикл таблицы.md'): r'''📖 Перечитать конспект: DDL: жизненный цикл таблицы >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Подмножества SQL и роль DDL (Data Definition Language)

> **Ментальная модель — «Чертежи и стены здания против мебели внутри»**:
> - Команды **DDL (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`)** — это строительные работы: возведение стен, пробивание новых дверей или снос здания целиком.
> - Команды **DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`)** — это заселение жильцов и перестановка мебели внутри уже построенных комнат.

```text
Команды языка SQL:
 ├── DDL (Data Definition Language)   : CREATE, ALTER, DROP, TRUNCATE  (Схема и структура таблиц)
 ├── DML (Data Manipulation Language) : SELECT, INSERT, UPDATE, DELETE (Чтение и изменение строк)
 ├── DCL (Data Control Language)      : GRANT, REVOKE                  (Права доступа и роли)
 └── TCL (Transaction Control)        : BEGIN, COMMIT, ROLLBACK, SAVEPOINT (Границы транзакций)
```

---

## 2. Выбор правильных типов данных при `CREATE TABLE`

При создании таблицы в PostgreSQL выбор типа данных напрямую влияет на объём RAM, скорость индексов и точность расчётов:

| Задача / Сущность | ❌ Ошибочный тип | ✅ Правильный тип в PostgreSQL | Почему это критично |
| :--- | :--- | :--- | :--- |
| **Деньги, баланс, цены** | `FLOAT` / `REAL` / `DOUBLE PRECISION` | `NUMERIC(12, 2)` или целые центы/копейки `BIGINT` | В двоичной системе `0.1 + 0.2 = 0.30000000000000004` — на балансах появятся фантомные копейки! |
| **Автоинкрементный ID** | Старый `SERIAL` | `BIGINT GENERATED ALWAYS AS IDENTITY` (или `BIGSERIAL`) | `INTEGER` (32 бита) переполняется на $2.14 \times 10^9$ записей |
| **Дата и время события** | `TIMESTAMP` (без таймзоны) или `VARCHAR` | `TIMESTAMPTZ` (`TIMESTAMP WITH TIME ZONE`) | Хранит время в UTC и автоматически переводит в часовой пояс клиента |
| **Строки переменной длины** | `CHAR(100)` (добивает пробелами!) | `VARCHAR(n)` или `TEXT` | В PostgreSQL `TEXT` и `VARCHAR` работают с одинаковой скоростью; `VARCHAR(n)` полезен как бизнес-ограничение длины |

---

## 3. Эволюция схемы (`ALTER TABLE`) и опасность `DROP` на продакшене

Жизненный цикл таблицы включает три главные команды DDL:
1. **`CREATE TABLE IF NOT EXISTS ...`** — создание таблицы с первичным ключом (`PRIMARY KEY`), внешними ключами (`REFERENCES`) и ограничениями (`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`).
2. **`ALTER TABLE ...`** — изменение живой таблицы без потери данных:
   - `ADD COLUMN phone VARCHAR(20) DEFAULT '' NOT NULL` (начиная с PostgreSQL 11 добавление колонки с константным `DEFAULT` выполняется мгновенно за $O(1)$ в метаданных без перезаписи таблицы на диске!);
   - `RENAME COLUMN old_name TO new_name`;
   - `ALTER COLUMN price TYPE NUMERIC(12, 2)` (опасно на больших таблицах: берёт эксклюзивную блокировку `ACCESS EXCLUSIVE LOCK` и перезаписывает всю таблицу!).
3. **`DROP TABLE IF EXISTS ...`** — полное уничтожение структуры таблицы, всех её данных и индексов.

> **Junior vs Senior**:
> - **Junior**: Хранит цены товаров в типе `FLOAT`, а на загруженном продакшене выполняет `ALTER TABLE users RENAME COLUMN name TO full_name`, из-за чего старые воркеры бэкенда мгновенно падают с `UndefinedColumn`.
> - **Senior**: Хранит деньги строго в `NUMERIC(12, 2)` или копейках (`BIGINT`), а переименование или изменение колонок на живом продакшене проводит по паттерну **Expand & Contract** (1. Добавить новую колонку $\to$ 2. Писать в обе колонки и мигрировать старые строки батчами $\to$ 3. Переключить чтение в коде $\to$ 4. Удалить старую колонку).

---

## 4. Практикум в Python 3.13: полный жизненный цикл DDL (`CREATE` -> `ALTER` -> метаданные)

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    # 1. CREATE TABLE с ограничениями целостности
    conn.execute("""
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL UNIQUE,
            balance_cents INTEGER NOT NULL DEFAULT 0 CHECK (balance_cents >= 0),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. ALTER TABLE: добавляем новую колонку currency без потери данных
    conn.execute("ALTER TABLE accounts ADD COLUMN currency TEXT NOT NULL DEFAULT 'RUB'")

    conn.execute("INSERT INTO accounts (owner, balance_cents) VALUES (?, ?)", ("Alice", 150000))

    # 3. Инспектируем структуру таблицы через PRAGMA table_info
    cols = conn.execute("PRAGMA table_info(accounts)").fetchall()
    print("Схема таблицы accounts после ALTER TABLE:")
    for cid, name, ctype, notnull, dflt, pk in cols:
        print(f"  - {name:14s} | тип: {ctype:7s} | NOT NULL: {bool(notnull)} | DEFAULT: {dflt}")

    row = conn.execute("SELECT owner, balance_cents, currency FROM accounts").fetchone()
    print("Запись в БД:", row)
```
''',

    os.path.join('Юнит 5.1 · SQL основы', '📚 Конспекты', 'К-128. INSERT, UPDATE, DELETE, TRUNCATE_.md'): r'''📖 Перечитать конспект: INSERT, UPDATE, DELETE, TRUNCATE: модификация данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Четыре способа изменить данные и правило «Семь раз отмерь `WHERE`»

> **Ментальная модель — «Ластик против шредера»**:
> - **`DELETE`** — вы берёте ластик и аккуратно стираете строки по одной, записывая каждое действие в журнал отмены (`WAL`), вызывая триггеры `ON DELETE` и проверяя внешние ключи.
> - **`TRUNCATE`** — вы вынимаете все листы из папки, отправляете их в шредер за $0.001$ секунды и кладёте чистую пачку бумаги. Это мгновенно освобождает место на диске, но не вызывает построчных триггеров!

**Главное правило безопасности DML**: перед тем как запустить `UPDATE` или `DELETE` на живой базе, сначала напишите точно такой же запрос со словом `SELECT *` вместо `UPDATE`/`DELETE` и убедитесь, что `WHERE` выбирает ровно те строки, которые вы собираетесь изменить! Забытый `WHERE` перезапишет или удалит **всю таблицу целиком**.

```text
Безопасный конвейер модификации данных в продакшене:
  1. BEGIN;                                                (Открыли транзакцию)
  2. SELECT id, status FROM orders WHERE id = 42;          (Проверили глазами цель!)
  3. UPDATE orders SET status = 'shipped' WHERE id = 42
     RETURNING id, status;                                 (Изменили и сразу проверили ответ)
  4. COMMIT; (или ROLLBACK; если затронуто не 1, а 10 000 строк!)
```

---

## 2. Пакетная вставка, `ON CONFLICT (UPSERT)` и конструкция `RETURNING`

1. **Пакетный `INSERT` (Batch Insert)**: вставлять 1 000 строк в цикле по одному `INSERT` — значит 1 000 раз ждать сетевой round-trip и синхронизацию журнала транзакций. Пакетный `INSERT INTO ... VALUES (...), (...), (...)` (или `executemany`) работает в десятки раз быстрее.
2. **Идемпотентный `UPSERT` (`ON CONFLICT`)**: что делать, если пользователь с таким `email` уже есть? Вместо медленного `SELECT` + `INSERT` используйте атомарный `ON CONFLICT`:
   ```sql
   INSERT INTO inventory (sku, qty) VALUES ('KB-01', 10)
   ON CONFLICT (sku) DO UPDATE SET qty = inventory.qty + EXCLUDED.qty
   RETURNING sku, qty;
   ```
3. **`RETURNING`**: поддерживается в PostgreSQL и SQLite (3.35+) для `INSERT`, `UPDATE` и `DELETE`. Позволяет за **один запрос** изменить строку и сразу получить сгенерированный `id`, `created_at` или старые значения удалённой записи!

---

## 3. Сравнение `DELETE`, `TRUNCATE` и `DROP`

| Характеристика | `DELETE FROM tbl [WHERE ...]` | `TRUNCATE TABLE tbl` | `DROP TABLE tbl` |
| :--- | :--- | :--- | :--- |
| **Класс команды** | DML (манипуляция строками) | DDL (сброс хранилища таблицы) | DDL (снос объекта БД) |
| **Фильтрация `WHERE`** | ✅ Да (можно удалить часть строк) | ❌ Нет (очищает только всю таблицу) | ❌ Нет (удаляет саму таблицу) |
| **Скорость на $10^7$ строк** | 🐢 Медленно ($O(n)$, пишет лог на каждую строку) | ⚡ Мгновенно ($O(1)$, пересоздаёт файл данных) | ⚡ Мгновенно ($O(1)$) |
| **Освобождает место ОС сразу?** | ❌ Нет (помечает строки как *dead tuples* до `VACUUM`) | ✅ Да, сразу возвращает гигабайты ОС | ✅ Да |
| **Построчные триггеры `ON DELETE`** | ✅ Срабатывают для каждой строки | ❌ Не срабатывают | ❌ Не срабатывают |
| **Можно ли откатить (`ROLLBACK`)?** | ✅ Да | ✅ В PostgreSQL да! (В MySQL/Oracle — нет) | ✅ В PostgreSQL да! |

> **Junior vs Senior**:
> - **Junior**: Делает `INSERT`, а затем вторым запросом `SELECT MAX(id) FROM orders`, чтобы узнать ID созданного заказа (получая классическую гонку состояний *Race Condition* при параллельных запросах!).
> - **Senior**: Использует `INSERT INTO orders (...) VALUES (...) RETURNING id, created_at` (получая точный ID атомарно за один сетевой вызов), а для синхронизации справочников применяет `INSERT ... ON CONFLICT (key) DO UPDATE SET ...`.

---

## 4. Практикум в Python 3.13: `UPSERT (ON CONFLICT)` и `RETURNING`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("""
        CREATE TABLE cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            qty INTEGER NOT NULL
        )
    """)

    # 1. Пакетный UPSERT: если товар уже в корзине, прибавляем количество атомарно!
    upsert_sql = """
    INSERT INTO cart_items (sku, qty) VALUES (?, ?)
    ON CONFLICT(sku) DO UPDATE SET qty = cart_items.qty + excluded.qty
    RETURNING id, sku, qty
    """
    for sku, add_qty in [("BOOK-PY", 1), ("MOUSE-PRO", 2), ("BOOK-PY", 3)]:
        row = conn.execute(upsert_sql, (sku, add_qty)).fetchone()
        print(f"После UPSERT ({sku}, +{add_qty}) -> строка в БД: id={row[0]}, sku={row[1]}, qty={row[2]}")

    # 2. Точечный DELETE с RETURNING: удаляем и сразу забираем данные удалённой позиции
    deleted = conn.execute(
        "DELETE FROM cart_items WHERE sku = ? RETURNING sku, qty",
        ("MOUSE-PRO",),
    ).fetchone()
    print("Удалена позиция через DELETE ... RETURNING:", deleted)
```
''',

    # =========================================================================
    # ЮНИТ 5.2 · SQL продвинутый (К-129 .. К-132)
    # =========================================================================
    os.path.join('Юнит 5.2 · SQL продвинутый', '📚 Конспекты', 'К-129. Подзапросы и CTE в SQL.md'): r'''📖 Перечитать конспект: Подзапросы и CTE в SQL >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Подзапросы (Subqueries): обычные против коррелированных

> **Ментальная модель — «Справочная записка против звонка на каждую строчку»**:
> - **Некоррелированный подзапрос** — вы один раз позвонили в бухгалтерию, узнали среднюю зарплату по компании (`120 000 ₽`), записали на стикер и дальше быстро сверяете весь список сотрудников с этим стикером.
> - **Коррелированный подзапрос** — для **каждого** из $10\,000$ сотрудников вы заново звоните в бухгалтерию и просите посчитать среднюю зарплату именно его отдела (`WHERE inner.dept_id = outer.dept_id`). Это превращает $O(n)$ в медленный вложенный цикл!

```text
Виды подзапросов по форме возвращаемого результата:
  1. Скалярный (1 строка × 1 колонка) : SELECT name, (SELECT AVG(price) FROM items) FROM items
  2. Списочный (N строк × 1 колонка)  : WHERE user_id IN (SELECT id FROM vip_users)
  3. Табличный (N строк × M колонок)  : FROM (SELECT dept, SUM(sal) AS s FROM emp GROUP BY dept) AS t
```

---

## 2. Ловушка `NOT IN` с `NULL` и почему `EXISTS` побеждает

Одна из самых частых задач на собеседовании: *«Почему запрос `WHERE id NOT IN (SELECT manager_id FROM users)` вернул **0 строк**, хотя в таблице полно обычных сотрудников?»*
Разгадка в троичной логике SQL (`TRUE`, `FALSE`, `UNKNOWN`):
- Выражение `id NOT IN (1, 2, NULL)` раскрывается в цепочку `id != 1 AND id != 2 AND id != NULL`.
- Любое сравнение с `NULL` даёт `UNKNOWN`. А `TRUE AND UNKNOWN` в секции `WHERE` всегда равно **`UNKNOWN` (ложь)**! Одна-единственная строка с `NULL` в подзапросе `NOT IN` обнуляет весь результат запроса!
- **Решение**: используйте `WHERE NOT EXISTS (...)` или `LEFT JOIN ... WHERE b.id IS NULL` — они корректно обрабатывают `NULL` и останавливают поиск при первом же совпадении (*Short-Circuit Evaluation*).

| Конструкция | Поведение при `NULL` в подзапросе | Остановка на первом совпадении | Рекомендация |
| :--- | :--- | :--- | :--- |
| `WHERE id IN (subquery)` | Безопасно (игнорирует `NULL`) | Зависит от оптимизатора | Удобно для небольших списков |
| `WHERE id NOT IN (subquery)` | 💥 **ОПАСНО**: возвращает **0 строк**, если есть хотя бы один `NULL`! | ❌ Нет, сканирует весь список | ❌ Избегать в продакшене |
| `WHERE EXISTS / NOT EXISTS` | ✅ **Безопасно** (проверяет факт наличия строки, а не значение) | ✅ Да, мгновенный выход (`LIMIT 1` под капотом) | ✅ Золотой стандарт для проверки связей |

---

## 3. Именованные CTE (`WITH`) и рекурсивные деревья (`WITH RECURSIVE`)

Когда вложенных подзапросов становится больше двух, читать SQL изнутри наружу невозможно. **CTE (Common Table Expressions)** через ключевое слово `WITH` позволяют разбить сложный запрос на понятные именованные шаги сверху вниз (как переменные в Python!):

```sql
WITH dept_stats AS (
    SELECT dept, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept
)
SELECT e.name, e.dept, e.salary, d.avg_sal
FROM employees e
JOIN dept_stats d ON e.dept = d.dept
WHERE e.salary > d.avg_sal;
```

А добавление слова **`RECURSIVE`** позволяет обходить иерархии любой глубины (деревья категорий, комментарии, оргструктуру компании) за один SQL-запрос! Рекурсивный CTE состоит из **якоря** (корневые узлы), оператора `UNION ALL` и **рекурсивного шага** (присоединение дочерних узлов).

> **Junior vs Senior**:
> - **Junior**: Пишет трёхэтажные вложенные подзапросы в `FROM (SELECT ... FROM (SELECT ...))` или использует `WHERE id NOT IN (SELECT parent_id FROM categories)`, получая пустую выдачу из-за `parent_id IS NULL` у корневых категорий.
> - **Senior**: Структурирует сложную аналитику в плоскую цепочку `WITH step1 AS (...), step2 AS (...)`, заменяет `NOT IN` на `NOT EXISTS` и обходит деревья категорий в базе через `WITH RECURSIVE`.

---

## 4. Практикум в Python 3.13: ловушка `NOT IN (NULL)` vs `NOT EXISTS` и `WITH RECURSIVE`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER)")
    conn.executemany(
        "INSERT INTO categories VALUES (?, ?, ?)",
        [
            (1, "Электроника", None),
            (2, "Ноутбуки", 1),
            (3, "Смартфоны", 1),
            (4, "Игровые ноутбуки", 2),
        ],
    )

    # 1. Демонстрация ловушки NOT IN с NULL vs правильного NOT EXISTS (ищем листовые категории без детей)
    buggy_not_in = conn.execute(
        "SELECT name FROM categories WHERE id NOT IN (SELECT parent_id FROM categories)"
    ).fetchall()
    safe_not_exists = conn.execute("""
        SELECT c.name FROM categories c
        WHERE NOT EXISTS (SELECT 1 FROM categories child WHERE child.parent_id = c.id)
    """).fetchall()
    print("Результат NOT IN с NULL (ловушка!):", buggy_not_in)
    print("Листовые категории через NOT EXISTS:", [r[0] for r in safe_not_exists])

    # 2. Рекурсивный CTE (WITH RECURSIVE): строим полные хлебные крошки для всех категорий
    tree_sql = """
    WITH RECURSIVE cat_tree AS (
        SELECT id, name, name AS path, 1 AS level
        FROM categories
        WHERE parent_id IS NULL
        UNION ALL
        SELECT c.id, c.name, ct.path || ' -> ' || c.name, ct.level + 1
        FROM categories c
        JOIN cat_tree ct ON c.parent_id = ct.id
    )
    SELECT level, path FROM cat_tree ORDER BY id
    """
    for lvl, path in conn.execute(tree_sql):
        print(f"[Уровень {lvl}] {path}")
```
''',

    os.path.join('Юнит 5.2 · SQL продвинутый', '📚 Конспекты', 'К-130. Агрегатные функции и GROUP BY.md'): r'''📖 Перечитать конспект: Агрегатные функции и GROUP BY >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Как работает схлопывание строк в `GROUP BY`

> **Ментальная модель — «Сортировка монет по копилкам»**: Оператор `GROUP BY currency` расставляет на столе отдельные копилки для каждой валюты (`RUB`, `USD`, `EUR`) и раскладывает строки таблицы по этим копилкам. Как только монеты ссыпаны в копилку, вы больше не видите номинал отдельной монеты снаружи — вы можете только взвесить копилку целиком (`SUM`), посчитать число монет (`COUNT`) или узнать самую крупную (`MAX`).

Именно поэтому в SQL действует **железное правило `GROUP BY`**:
В секции `SELECT` при наличии `GROUP BY` могут находиться **ТОЛЬКО**:
1. Колонки, перечисленные в самом `GROUP BY` (наклейка на копилке);
2. Агрегатные функции (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`), вычисляющие сводное число по содержимому копилки.

```text
Таблица sales:                        GROUP BY dept:
+------+--------+--------+            +------+----------+-------------+
| dept | seller | amount |            | dept | COUNT(*) | SUM(amount) |
+------+--------+--------+   =====>   +------+----------+-------------+
| IT   | Alice  |  1000  |            | IT   |    2     |    2500     |
| IT   | Bob    |  1500  |            | HR   |    1     |     800     |
| HR   | Clara  |   800  |            +------+----------+-------------+
+------+--------+--------+            (Колонка seller схлопнулась: написать
                                       SELECT dept, seller, SUM(amount) нельзя!)
```

---

## 2. Пять главных агрегатных функций и их коварное поведение с `NULL`

Все агрегатные функции в SQL (кроме одной — `COUNT(*)`) **полностью игнорируют значения `NULL`**! Это приводит к классическим ошибкам в аналитике:

| Функция | Что считает | Как ведёт себя при `NULL` | Что вернёт на значениях `(100, 200, NULL)` |
| :--- | :--- | :--- | :--- |
| **`COUNT(*)`** | Общее количество физических строк в группе | ✅ Считает все строки, **включая `NULL`** | **`3`** |
| **`COUNT(col)`** | Количество строк, где `col IS NOT NULL` | Игнорирует `NULL` | **`2`** |
| **`COUNT(DISTINCT col)`** | Количество **уникальных** не-`NULL` значений | Игнорирует `NULL` и дубликаты | **`2`** |
| **`SUM(col)`** | Сумма значений колонки | Игнорирует `NULL` (если все `NULL` $\to$ вернёт `NULL`, а не `0`!) | **`300`** |
| **`AVG(col)`** | Среднее арифметическое **только среди НЕ-`NULL` строк**! | Делит `SUM(col)` на `COUNT(col)`, а не на `COUNT(*)`! | **`150.0`** ($300 / 2$, а не $300 / 3 = 100$!) |
| **`MIN(col)` / `MAX(col)`** | Минимум и максимум (работает для чисел, дат и строк) | Игнорирует `NULL` | **`100`** / **`200`** |

---

## 3. Защита от `NULL` в агрегациях через `COALESCE`

Обратите внимание на две ловушки из таблицы выше:
1. Если вы считаете среднюю скидку по всем заказам, а у заказов без скидки записан `NULL` вместо `0`, то `AVG(discount)` посчитает среднее **только среди тех, у кого была скидка**! Чтобы учесть нулевые заказы, пишите `AVG(COALESCE(discount, 0))`.
2. Если вы суммируете платежи нового клиента через `SELECT SUM(amount) FROM payments WHERE user_id = 999`, а платежей ещё не было, `SUM` вернёт **`NULL`**, а не `0`! Обязательно оборачивайте сумму в `COALESCE(SUM(amount), 0)`.

> **Junior vs Senior**:
> - **Junior**: Считает процент конверсии или средний бонус через `AVG(bonus)`, не подозревая, что у 80% сотрудников в колонке `bonus` стоит `NULL`, из-за чего `AVG` завышает реальное среднее в 5 раз.
> - **Senior**: Чётко различает `COUNT(*)` (все строки), `COUNT(col)` (непустые значения) и `COUNT(DISTINCT col)` (уникальные непустые значения), а для корректного расчёта средних и сумм на пустых выборках явно использует `COALESCE(col, 0)`.

---

## 4. Практикум в Python 3.13: проверяем разницу `COUNT(*)` vs `COUNT(col)` и `AVG` с `NULL`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE bonuses (emp TEXT, dept TEXT, bonus INTEGER)")
    conn.executemany(
        "INSERT INTO bonuses VALUES (?, ?, ?)",
        [
            ("Alice", "Backend", 100),
            ("Bob", "Backend", 200),
            ("Charlie", "Backend", None),  # Бонус не назначен (NULL)
            ("Diana", "QA", None),         # В отделе QA все бонусы NULL
        ],
    )

    sql = """
    SELECT
        dept,
        COUNT(*) AS total_rows,
        COUNT(bonus) AS non_null_bonuses,
        COALESCE(SUM(bonus), 0) AS safe_sum,
        AVG(bonus) AS naive_avg,
        AVG(COALESCE(bonus, 0)) AS true_avg
    FROM bonuses
    GROUP BY dept
    ORDER BY dept
    """
    for dept, cnt_all, cnt_col, s_sum, n_avg, t_avg in conn.execute(sql):
        print(
            f"Отдел {dept:7s}: COUNT(*)={cnt_all}, COUNT(bonus)={cnt_col}, "
            f"SUM={s_sum}, AVG(bonus)={n_avg}, AVG(COALESCE)={t_avg:.1f}"
        )
```
''',

    os.path.join('Юнит 5.2 · SQL продвинутый', '📚 Конспекты', 'К-131. Оконные функции_ ROW_NUMBER, RANK, DENSE_RANK.md'): r'''📖 Перечитать конспект: Оконные функции: ROW_NUMBER, RANK, DENSE_RANK >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. В чём суперсила оконных функций (`OVER`) по сравнению с `GROUP BY`?

> **Ментальная модель — «Общее фото класса с бейджиком места у каждого ученика»**:
> - Обычный **`GROUP BY`** — это мясорубка: он сжимает 30 учеников класса в **одну итоговую строчку** «Средний балл 10-А класса = 4.2». Сами ученики при этом исчезают!
> - **Оконная функция (`OVER`)** — это прозрачная линейка: все 30 учеников остаются на своих местах (строки **не схлопываются**!), но каждому на грудь вешается дополнительный бейджик: средний балл его класса, его место в рейтинге (`RANK`) или разница с соседом (`LAG`).

```text
Анатомия вызова оконной функции:
  ROW_NUMBER() OVER (PARTITION BY dept   ORDER BY salary DESC)
  \__________/       \_______________/   \__________________/
   Что считаем       Как делим на окна   В каком порядке нумеруем
                     (аналог GROUP BY,   строки внутри каждого окна
                      но без сжатия!)
```

---

## 2. Битва функций ранжирования: `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`

На собеседованиях обожают спрашивать: *«В отделе работают 4 человека с зарплатами `100, 100, 80, 50`. Какие места им присвоят `ROW_NUMBER()`, `RANK()` и `DENSE_RANK()` при сортировке по убыванию?»*

| Зарплата (`salary DESC`) | `ROW_NUMBER()` (Строгий счётчик) | `RANK()` (Спортивный подиум с пропусками) | `DENSE_RANK()` (Плотный ранг без дыр) |
| :--- | :--- | :--- | :--- |
| **`100`** | **`1`** | **`1`** | **`1`** |
| **`100`** (ничья!) | **`2`** (случайный порядок среди равных) | **`1`** (делят 1-е место) | **`1`** (делят 1-е место) |
| **`80`** | **`3`** | **`3`** (2-е место пропущено!) | **`2`** (без пропуска мест!) |
| **`50`** | **`4`** | **`4`** | **`3`** |

---

## 3. Функции смещения (`LAG`, `LEAD`) и нарастающий итог (`Running Total`)

Помимо ранжирования, окно `OVER (...)` открывает доступ к соседним строкам и скользящим агрегатам **без единого `SELF JOIN`**:
1. **`LAG(col, 1, default) OVER (ORDER BY dt)`** — заглядывает на 1 строку **назад** (например, выручка за вчерашний день для расчёта прироста `revenue - LAG(revenue, 1, 0) OVER (...)`).
2. **`LEAD(col, 1, default) OVER (ORDER BY dt)`** — заглядывает на 1 строку **вперёд** (дата следующей покупки клиента).
3. **`SUM(amount) OVER (PARTITION BY user_id ORDER BY dt)`** — при добавлении `ORDER BY` внутрь `OVER` обычная сумма превращается в **нарастающий итог (Running Total)** от первой строки окна до текущей!

 Важное правило порядка выполнения: оконные функции вычисляются на шаге **`SELECT`** (после `WHERE`, `GROUP BY` и `HAVING`). Поэтому написать `WHERE ROW_NUMBER() OVER (...) <= 3` напрямую **нельзя** — нужно обернуть расчёт ранга в CTE (`WITH ranked AS (...)`) и отфильтровать `WHERE rn <= 3` во внешнем запросе!

> **Junior vs Senior**:
> - **Junior**: Чтобы найти топ-2 самых дорогих товара в каждой категории или сравнить выручку с прошлым месяцем, городит медленные коррелированные подзапросы или `SELF JOIN` таблицы самой на себя.
> - **Senior**: Решает задачу «Топ-N в каждой группе» за один проход через CTE с `DENSE_RANK() / ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC)`, а динамику метрик во времени считает через `LAG()` и `SUM() OVER (ORDER BY date)`.

---

## 4. Практикум в Python 3.13: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG` и нарастающий итог

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE salaries (emp TEXT, dept TEXT, sal INTEGER)")
    conn.executemany(
        "INSERT INTO salaries VALUES (?, ?, ?)",
        [
            ("Alice", "IT", 100),
            ("Bob", "IT", 100),
            ("Charlie", "IT", 80),
            ("Diana", "IT", 50),
        ],
    )

    sql = """
    SELECT
        emp,
        sal,
        ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC) AS rn,
        RANK()       OVER (PARTITION BY dept ORDER BY sal DESC) AS rnk,
        DENSE_RANK() OVER (PARTITION BY dept ORDER BY sal DESC) AS dense_rnk,
        SUM(sal)     OVER (PARTITION BY dept ORDER BY sal DESC, emp) AS running_total,
        sal - LAG(sal, 1, sal) OVER (PARTITION BY dept ORDER BY sal DESC) AS diff_prev
    FROM salaries
    """
    print("Имя     | Sal | ROW_NUM | RANK | DENSE | RunTotal | DiffPrev")
    print("-" * 62)
    for emp, sal, rn, rnk, drnk, rtot, diff in conn.execute(sql):
        print(f"{emp:7s} | {sal:3d} |    {rn}    |  {rnk}   |   {drnk}   |   {rtot:4d}   |   {diff:+3d}")
```
''',

    os.path.join('Юнит 5.2 · SQL продвинутый', '📚 Конспекты', 'К-132. UNION и UNION ALL_ объединение.md'): r'''📖 Перечитать конспект: UNION и UNION ALL: объединение результатов запросов >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Горизонтальная склейка (`JOIN`) против вертикальной стопки (`UNION`)

> **Ментальная модель — «Приклеить листы сбоку или сложить в одну стопку»**:
> - **`JOIN` (Горизонтальное соединение)** — вы кладёте два листа рядом на стол и склеиваете их скотчем по боковому краю: таблица становится **шире** (появляются новые колонки справа).
> - **`UNION` (Вертикальное объединение)** — вы кладёте один лист со списком людей **поверх другого листа** в одну пачку: количество колонок не меняется, но таблица становится **длиннее** (строки второго запроса дописываются в конец первого).

```text
JOIN (расширяет вправо — добавляет КОЛОНКИ):       UNION (удлиняет вниз — добавляет СТРОКИ):
  [id | name]  +  [user_id | phone]                  [id | email]  (из таблицы active_users)
                 │                                         +
                 ▼                                   [id | email]  (из таблицы archived_users)
  [id | name | user_id | phone]                            │
                                                           ▼
                                                     [id | email]  (единый длинный список)
```

---

## 2. Три строгих правила синтаксиса и битва `UNION` vs `UNION ALL`

Чтобы сложить результаты двух `SELECT` в одну стопку, оба запроса обязаны соблюдать три правила:
1. **Одинаковое количество столбцов** в каждом `SELECT`.
2. **Совместимые типы данных** на соответствующих позициях (1-й столбец с 1-м, 2-й со 2-м).
3. **Имена итоговых столбцов** берутся из **первого** `SELECT`, а итоговая сортировка `ORDER BY` пишется один раз **в самом конце** всего выражения.

Главная разница между двумя операторами вертикального слияния:

| Характеристика | `UNION ALL` (Быстрая конкатенация) | `UNION` (Слияние с дедупликацией) |
| :--- | :--- | :--- |
| **Что делает с дубликатами?** | **Оставляет все строки как есть** (даже если одна и та же строка встретилась в обоих запросах) | **Удаляет все полные дубликаты** (как если бы сверху применили `SELECT DISTINCT`) |
| **Что происходит под капотом?** | Просто потоково дописывает строки второго запроса вслед за первым (`Append`) | Складывает все строки во временный буфер, выполняет тяжёлую сортировку/хэширование и удаляет повторы |
| **Скорость и расход памяти** | ⚡ Максимальная скорость, $O(1)$ доп. памяти | 🐢 Медленно на больших выборках, требует $O(n)$ памяти и CPU |
| **Когда использовать?** | **В 95% случаев по умолчанию!** (Особенно если выборки заведомо не пересекаются) | Только когда вам действительно нужно уникальное множество строк |

---

## 3. Родственные теоретико-множественные операторы: `INTERSECT` и `EXCEPT`

Помимо `UNION`, стандарт SQL включает ещё два оператора над множествами строк:
- **`INTERSECT`** — возвращает только те строки, которые присутствуют **одновременно в обоих** запросах (пересечение множеств $A \cap B$).
- **`EXCEPT`** (в Oracle называется `MINUS`) — возвращает строки первого запроса, которых **нет во втором** запросе (разность множеств $A \setminus B$). Очень удобно для поиска расхождений при миграции данных из старой таблицы в новую!

> **Junior vs Senior**:
> - **Junior**: По привычке везде пишет `UNION` вместо `UNION ALL`, объединяя таблицы логов за январь и февраль (которые физически не могут иметь общих строк!), заставляя PostgreSQL впустую сортировать миллионы строк на диске в `temp_files`.
> - **Senior**: По умолчанию всегда пишет `UNION ALL` и переходит на `UNION` только тогда, когда дедупликация продиктована бизнес-требованием, а для сверки двух выборок применяет лаконичные `INTERSECT` и `EXCEPT`.

---

## 4. Практикум в Python 3.13: `UNION ALL` vs `UNION`, `INTERSECT` и `EXCEPT`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE web_buyers (email TEXT)")
    conn.execute("CREATE TABLE app_buyers (email TEXT)")
    conn.executemany("INSERT INTO web_buyers VALUES (?)", [("alice@py.ru",), ("bob@py.ru",)])
    conn.executemany("INSERT INTO app_buyers VALUES (?)", [("bob@py.ru",), ("charlie@py.ru",)])

    # 1. UNION ALL (сохраняет все 4 строки, включая два вхождения bob@py.ru)
    u_all = [r[0] for r in conn.execute("SELECT email FROM web_buyers UNION ALL SELECT email FROM app_buyers")]
    # 2. UNION (удаляет дубликат bob@py.ru -> 3 уникальных клиента)
    u_uniq = [r[0] for r in conn.execute("SELECT email FROM web_buyers UNION SELECT email FROM app_buyers ORDER BY email")]
    # 3. INTERSECT (купили И на сайте, И в мобильном приложении)
    both = [r[0] for r in conn.execute("SELECT email FROM web_buyers INTERSECT SELECT email FROM app_buyers")]
    # 4. EXCEPT (купили на сайте, но ещё НИ РАЗУ не покупали в приложении)
    web_only = [r[0] for r in conn.execute("SELECT email FROM web_buyers EXCEPT SELECT email FROM app_buyers")]

    print("UNION ALL (быстро, с дублями):", u_all)
    print("UNION     (уникальные)       :", u_uniq)
    print("INTERSECT (пересечение)      :", both)
    print("EXCEPT    (только Web)       :", web_only)
```
''',

    # =========================================================================
    # ЮНИТ 5.3 · Проектирование БД (К-133 .. К-137)
    # =========================================================================
    os.path.join('Юнит 5.3 · Проектирование БД', '📚 Конспекты', 'К-133. Нормализация баз данных_ 1НФ, 2НФ, 3НФ.md'): r'''📖 Перечитать конспект: Нормализация баз данных: 1НФ, 2НФ, 3НФ >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Зачем нужна нормализация и три аномалии «плоской Excel-таблицы»

> **Ментальная модель — «Единый справочник вместо копипасты в 100 документах»**: Представьте, что в таблицу заказов вы каждый раз вручную вписываете имя клиента, его телефон, название отдела доставки и телефон начальника этого отдела. Как только клиент сменит номер телефона, вам придётся искать и править 500 его старых заказов! **Нормализация** — это математический метод расселения данных по отдельным таблицам так, чтобы **каждый факт хранился в базе ровно в одном месте**.

Если свалить все данные в одну широкую таблицу, возникают **три классические аномалии**:
1. **Аномалия обновления (Update Anomaly)**: клиент сменил email $\implies$ нужно обновить 100 строк заказов; если обновили 99 из 100, база данных впадает в противоречие.
2. **Аномалия вставки (Insert Anomaly)**: нельзя добавить в базу нового поставщика или товар, пока его кто-нибудь не купит (ведь таблица называется `orders`!).
3. **Аномалия удаления (Delete Anomaly)**: удалили единственный тестовый заказ клиента $\implies$ навсегда потеряли телефон и адрес самого клиента!

```text
Путь нормализации от сырой таблицы до 3НФ:
  [Ненормализованная таблица: телефоны через запятую, дубли клиентов и отделов]
      │
      ▼  Шаг 1 (1НФ): Атомарность ячеек (1 ячейка = 1 значение, никаких списков через запятую!)
  [Первая нормальная форма (1NF)]
      │
      ▼  Шаг 2 (2НФ): Убрать частичную зависимость от составного первичного ключа
  [Вторая нормальная форма (2NF)]
      │
      ▼  Шаг 3 (3НФ): Убрать транзитивную зависимость (неключевое поле зависит от другого неключевого!)
  [Третья нормальная форма (3NF): "Каждый факт зависит от ключа, всего ключа и ничего кроме ключа!"]
```

---

## 2. Первая, Вторая и Третья нормальные формы (1NF, 2NF, 3NF)

| Нормальная форма | Главное требование простыми словами | Типичное нарушение (Антипаттерн) | Как исправить при проектировании |
| :--- | :--- | :--- | :--- |
| **1НФ (1NF)** | **Атомарность**: в каждой ячейке хранится ровно одно неделимое значение, нет повторяющихся колонок (`phone1`, `phone2`) | В колонке `items` написано `'Мышь, Коврик, Кабель'` через запятую | Разбить список на отдельные строки дочерней таблицы `order_items` |
| **2НФ (2NF)** | Таблица в 1НФ + каждое неключевое поле зависит от **всего составного первичного ключа целиком**, а не от его половинки | В таблице `order_items` с ключом `(order_id, product_id)` хранится `product_name` (зависит только от `product_id`!) | Вынести `product_name` и `price` в отдельную таблицу `products(id, name, price)` |
| **3НФ (3NF)** | Таблица в 2НФ + **нет транзитивных зависимостей** (`Ключ -> Поле А -> Поле Б`: неключевой столбец не должен зависеть от другого неключевого столбца!) | В таблице `employees(id, name, dept_id, dept_phone)` телефон отдела зависит от `dept_id`, а не от сотрудника `id` | Вынести `dept_phone` в таблицу `departments(id, name, phone)` |

Английская мнемоника для **3NF** (клятва в суде): *«Every non-key attribute must provide a fact about the key (1NF), the whole key (2NF), and nothing but the key (3NF), so help me Codd!»*

---

## 3. Практический пример приведения таблицы к 3НФ

До нормализации (нарушены 1НФ, 2НФ и 3НФ):
`raw_orders(order_id, client_name, client_city, city_Coding, products_csv)`
После приведения к **3НФ**:
- `cities(id, name, Coding)` — убрали транзитивную зависимость `client -> city -> Coding` (3НФ);
- `clients(id, name, city_id REFERENCES cities)` — данные клиента хранятся ровно один раз;
- `orders(id, client_id REFERENCES clients, created_at)` — шапка заказа;
- `order_items(order_id, product_id, qty, PRIMARY KEY (order_id, product_id))` — убрали списки через запятую (1НФ), а названия товаров вынесли в `products(id, title)` (2НФ).

> **Junior vs Senior**:
> - **Junior**: Хранит теги статьи или телефоны клиента строкой `'python, sql, backend'` через запятую в одном `VARCHAR`-поле, а потом мучается с `LIKE '%sql%'`, который не может использовать B-Tree индекс и ошибочно находит `'nosql'`.
> - **Senior**: Проектирует OLTP-схему по умолчанию в строгой **3НФ** (каждая сущность в своей таблице, связи через внешние ключи `FOREIGN KEY`), исключая аномалии обновления и обеспечивая мгновенный поиск по индексам.

---

## 4. Практикум в Python 3.13: декомпозиция плоской таблицы в 3НФ и сборка через `JOIN`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.executescript("""
        CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE);
        CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, price INTEGER NOT NULL);
        CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER REFERENCES clients(id));
        CREATE TABLE order_items (
            order_id INTEGER REFERENCES orders(id),
            product_id INTEGER REFERENCES products(id),
            qty INTEGER NOT NULL,
            PRIMARY KEY (order_id, product_id)
        );

        INSERT INTO clients VALUES (1, 'Alice', 'alice@dev.io');
        INSERT INTO products VALUES (10, 'Клавиатура', 120), (20, 'Мышь', 60);
        INSERT INTO orders VALUES (100, 1);
        INSERT INTO order_items VALUES (100, 10, 1), (100, 20, 2);
    """)

    # Обновление email клиента затрагивает РОВНО 1 строку в таблице clients (нет аномалии обновления!)
    conn.execute("UPDATE clients SET email = 'alice_new@dev.io' WHERE id = 1")

    sql = """
    SELECT o.id, c.name, c.email, SUM(p.price * oi.qty) AS order_total
    FROM orders o
    JOIN clients c ON o.client_id = c.id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY o.id, c.name, c.email
    """
    print("Заказ из схемы в 3НФ:", conn.execute(sql).fetchone())
```
''',

    os.path.join('Юнит 5.3 · Проектирование БД', '📚 Конспекты', 'К-134. Денормализация данных.md'): r'''📖 Перечитать конспект: Денормализация данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Что такое денормализация и когда 3НФ начинает тормозить?

> **Ментальная модель — «Шпаргалка на обложке папки»**: В идеально нормализованной бухгалтерии (3НФ), чтобы узнать итоговую сумму накладной, нужно каждый раз открывать папку и складывать на калькуляторе все 200 товарных чеков внутри (`JOIN` + `SUM`). Если директор спрашивает эту сумму 1 000 раз в секунду, бухгалтер сойдёт с ума. **Денормализация** — это осознанное решение написать `total_amount` и `items_count` прямо на обложке папки и обновлять эту цифру при добавлении нового чека!

**Денормализация** — это **преднамеренное** введение контролируемой избыточности в уже нормализованную схему БД ради **ускорения частых запросов на чтение (Read-Heavy Workloads)** за счёт избавления от тяжёлых `JOIN` и агрегаций на лету.

Важно: денормализация — это **не лень проектировать БД** (хаос до нормализации), а инженерный компромисс *после* 3НФ!

```text
Нормализованное чтение (3НФ):
  SELECT o.id, COUNT(i.id), SUM(i.price * i.qty)
  FROM orders o JOIN order_items i ON o.id = i.order_id GROUP BY o.id;
  (На 10 млн строк: тяжёлый JOIN + GROUP BY при КАЖДОМ открытии страницы!)

Денормализованное чтение:
  SELECT id, items_count, total_amount FROM orders WHERE user_id = 42;
  (Мгновенный Index Scan за 0.1 мс из одной таблицы без единого JOIN!)
```

---

## 2. Четыре классических паттерна денормализации в продакшене

| Паттерн денормализации | Пример в схеме БД | Какую проблему решает | Как поддерживать актуальность? |
| :--- | :--- | :--- | :--- |
| **1. Предварительно посчитанные агрегаты (Counter / Total Cache)** | Колонки `likes_count`, `comments_count` в таблице `posts`; `total_price` в `orders` | Избавляет от `COUNT(*)` и `SUM()` по миллионам строк при рендере ленты | Триггер БД (`AFTER INSERT/DELETE`) или атомарный инкремент в одной транзакции |
| **2. Исторический слепок (Snapshot на момент сделки)** | Сохранение `product_title` и `unit_price_at_purchase` прямо в `order_items` | Если магазин завтра поднимет цену товара в каталоге `products`, старые чеки покупателей **обязаны сохранить старую цену**! | Записывается один раз в момент покупки и никогда не меняется |
| **3. Материализованные представления (`MATERIALIZED VIEW`)** | Отдельная витрина отчётов продаж по дням и регионам на диске | Сверхтяжёлый аналитический запрос считается 1 раз в час (`REFRESH MATERIALIZED VIEW CONCURRENTLY`), а дашборд читает готовую таблицу | Расписание в Cron / Celery или `pg_cron` |
| **4. Копирование частого атрибута родителя** | Хранение `author_username` прямо в таблице `comments` | Вывод 100 комментариев под постом без `JOIN users` | Фоновая задача при редкой смене никнейма |

---

## 3. Цена денормализации и как не допустить рассинхронизации

Денормализация никогда не бывает бесплатной:
1. **Замедление записи (`INSERT` / `UPDATE` / `DELETE`)**: теперь при добавлении одного комментария нужно не только вставить строку в `comments`, но и сделать `UPDATE posts SET comments_count = comments_count + 1 WHERE id = :post_id`.
2. **Риск рассинхронизации (Data Inconsistency)**: если код приложения обновил дочернюю таблицу без транзакции и упал до обновления счётчика, на сайте навсегда останется неверное число! Поэтому синхронизацию денормализованных полей делают либо **внутри единой ACID-транзакции**, либо через **триггеры базы данных**.

> **Junior vs Senior**:
> - **Junior**: Либо боится любого дублирования и считает `SELECT COUNT(*) FROM likes WHERE post_id = ...` для каждого из 50 постов в ленте новостей, либо сваливает все поля в одну таблицу без понимания, как их синхронизировать.
> - **Senior**: Держит ядро схемы в 3НФ, но обязательно сохраняет неизменяемые исторические снимки (`price_at_purchase` в позициях заказа) и денормализует горячие счётчики (`likes_count`) под защитой транзакций или триггеров СУБД.

---

## 4. Практикум в Python 3.13: автоматическая поддержка денормализованной суммы заказа через `TRIGGER`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.executescript("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            items_count INTEGER NOT NULL DEFAULT 0,
            total_amount INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            title_snapshot TEXT NOT NULL,
            price_snapshot INTEGER NOT NULL
        );

        -- Триггер БД автоматически обновляет денормализованные счётчики на обложке заказа!
        CREATE TRIGGER trg_order_item_insert
        AFTER INSERT ON order_items
        BEGIN
            UPDATE orders
            SET items_count  = items_count + 1,
                total_amount = total_amount + NEW.price_snapshot
            WHERE id = NEW.order_id;
        END;
    """)

    conn.execute("INSERT INTO orders (id) VALUES (1)")
    conn.executemany(
        "INSERT INTO order_items (order_id, title_snapshot, price_snapshot) VALUES (?, ?, ?)",
        [(1, "Книга Python", 1500), (1, "Подписка Pro", 2500)],
    )

    # Читаем итог мгновенно из одной строки orders без единого JOIN и SUM()!
    order_row = conn.execute("SELECT id, items_count, total_amount FROM orders WHERE id = 1").fetchone()
    print(f"Заказ #{order_row[0]}: позиций = {order_row[1]}, сумма = {order_row[2]} ₽ (обновлено триггером!)")
```
''',

    os.path.join('Юнит 5.3 · Проектирование БД', '📚 Конспекты', 'К-135. Первичные и внешние ключи_ целостность данных.md'): r'''📖 Перечитать конспект: Первичные и внешние ключи: целостность данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Первичный ключ (`PRIMARY KEY`): естественный, суррогатный или `UUID`?

> **Ментальная модель — «Паспортный ID против ФИО и посадочного талона»**:
> - **Первичный ключ (`PRIMARY KEY`, PK)** — это уникальный и неизменный идентификатор строки в таблице (технически `PRIMARY KEY` = `UNIQUE` + `NOT NULL` + автоматический B-Tree индекс).
> - **Внешний ключ (`FOREIGN KEY`, FK)** — это ссылка в дочерней таблице (например, `orders.user_id`), которая указывает на `PRIMARY KEY` родительской таблицы (`users.id`). База данных на уровне ядра гарантирует **ссылочную целостность (Referential Integrity)**: нельзя создать заказ на несуществующего клиента `user_id = 999999`!

Какой тип первичного ключа выбрать при проектировании таблицы?

| Тип первичного ключа | Пример | Плюсы | Минусы и подводные камни |
| :--- | :--- | :--- | :--- |
| **Суррогатный `BIGINT` (Автоинкремент)** | `1, 2, 3, ...` (`GENERATED ALWAYS AS IDENTITY`) | Компактный (8 байт), идеальная локальность вставки в конец B-Tree индекса | Легко перебрать чужие ID в URL (`/orders/101`, `/orders/102` — риск IDOR), неудобно при слиянии нескольких шардов |
| **Естественный (Natural Key)** | ИНН, серия паспорта, ISO-код страны (`'RU'`, `'US'`) | Имеет бизнес-смысл без лишнего `JOIN` | Бизнес-правила меняются! Если человек сменит паспорт или email, придётся каскадно перезаписывать все внешние ключи |
| **`UUID v4` (Случайный 128-бит)** | `'f47ac10b-58cc-4372-...'` | Можно генерировать на клиенте/в микросервисе до похода в БД, непредсказуем в URL | Хаотичная вставка в разные места B-Tree вызывает фрагментацию страниц индекса (*Page Splits*) |
| **`UUID v7` (Сортируемый по времени)** | Стандарт в PostgreSQL 17+ / Python | Сочетает глобальную уникальность UUID и монотонную сортировку по времени создания! | Занимает 16 байт (в 2 раза больше `BIGINT`) |
| **Составной (Composite PK)** | `PRIMARY KEY (order_id, product_id)` | Идеален для связующих таблиц `M:N`, гарантирует отсутствие дублей пары | Неудобно ссылаться на него из других таблиц |

---

## 2. Поведение внешнего ключа при удалении родителя (`ON DELETE`)

Что должна сделать база данных, если кто-то пытается удалить пользователя `DELETE FROM users WHERE id = 1`, у которого в таблице `orders` лежат 10 заказов?

```text
Попытка: DELETE FROM users WHERE id = 1
  ├── ON DELETE RESTRICT (по умолчанию) -> ❌ ОШИБКА IntegrityError! Удаление запрещено, пока есть заказы.
  ├── ON DELETE CASCADE                 -> 🔥 Удалит пользователя И автоматически сотрёт все 10 его заказов!
  ├── ON DELETE SET NULL                -> 👻 Удалит пользователя, а в его заказах поставит user_id = NULL.
  └── ON DELETE SET DEFAULT             -> 🔄 Проставит дефолтный ID (например, архивного системного юзера).
```

- Используйте **`ON DELETE CASCADE`** только для «технических придатков» сущности (сессии пользователя, токены сброса пароля, элементы внутри корзины).
- Для **финансовых документов, чеков и заказов** всегда оставляйте **`ON DELETE RESTRICT`** (или применяйте *Soft Delete* — пометку `deleted_at = NOW()`), иначе случайное удаление аккаунта уничтожит финансовую отчётность компании!

---

## 3. Важная деталь производительности: индекс на `FOREIGN KEY`!

Когда вы объявляете `PRIMARY KEY`, СУБД **автоматически** создаёт уникальный B-Tree индекс.
Но когда вы объявляете `FOREIGN KEY (user_id) REFERENCES users(id)`, PostgreSQL и SQLite **НЕ создают индекс на колонке `user_id` автоматически**! Без ручного `CREATE INDEX idx_orders_user_id ON orders(user_id)` любой `JOIN` и любое удаление из `users` будет вызывать полное сканирование (`Seq Scan`) всей таблицы `orders`!

> **Junior vs Senior**:
> - **Junior**: Вешает `ON DELETE CASCADE` на все внешние ключи подряд (рискуя одним `DELETE` снести половину базы данных) и забывает создавать индексы на колонках внешних ключей (`user_id`).
> - **Senior**: Использует `BIGINT` (внутри БД) + `UUID` (снаружи в API), ставит `ON DELETE RESTRICT` на финансовые таблицы, `ON DELETE CASCADE` на временные связки и всегда создаёт B-Tree индекс на каждом столбце внешнего ключа.

---

## 4. Практикум в Python 3.13: проверка `ON DELETE RESTRICT` против `ON DELETE CASCADE`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    # В SQLite проверка внешних ключей включается прагмой на соединение:
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE invoices (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT
        );

        INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
        INSERT INTO sessions VALUES (10, 1), (11, 2);
        INSERT INTO invoices VALUES (500, 1);
    """)

    # 1. Пытаемся удалить Alice (id=1), у которой есть финансовый счёт (RESTRICT):
    try:
        conn.execute("DELETE FROM users WHERE id = 1")
    except sqlite3.IntegrityError as exc:
        print("Защита ON DELETE RESTRICT сработала для Alice:", exc)

    # 2. Удаляем Bob (id=2), у которого есть только сессия (CASCADE):
    conn.execute("DELETE FROM users WHERE id = 2")
    rem_sessions = conn.execute("SELECT * FROM sessions WHERE user_id = 2").fetchall()
    print("Сессии Боба после ON DELETE CASCADE:", rem_sessions)
```
''',

    os.path.join('Юнит 5.3 · Проектирование БД', '📚 Конспекты', 'К-136. Типы связей между таблицами_ 1_1, 1_M, M_M.md'): r'''📖 Перечитать конспект: Типы связей между таблицами: 1:1, 1:M, M:M >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Три фундаментальных типа связей в реляционных БД

> **Ментальная модель — «Человек, его паспорт, его банковские карты и его подписки»**:
> - **Один-к-одному (`1:1`, One-to-One)**: У одного гражданина ровно один действующий загранпаспорт, и этот паспорт принадлежит только одному гражданину.
> - **Один-ко-многим (`1:N` / `1:M`, One-to-Many)**: У одного клиента может быть 5 банковских карт, но каждая конкретная пластиковая карта выпущена ровно на одного владельца.
> - **Многие-ко-многим (`M:N` / `M:M`, Many-to-Many)**: Один студент записан на 4 курса, и на каждом курсе учится по 100 студентов.

```text
1. Связь 1:1 (users <-> passports):
   [users: id PK] <────── [passports: user_id UNIQUE NOT NULL FK]

2. Связь 1:N (authors ─< books):
   [authors: id PK] <──── [books: author_id NOT NULL FK]  (Внешний ключ ВСЕГДА на стороне «Многие»!)

3. Связь M:N (students >─< courses через промежуточную таблицу enrollments):
   [students: id PK] <─── [enrollments: (student_id FK, course_id FK) PK] ───> [courses: id PK]
```

---

## 2. Как физически реализуется каждая связь в SQL DDL?

| Тип связи | Где лежит `FOREIGN KEY`? | Чем отличается ограничение на ключе? | Зачем используется на практике? |
| :--- | :--- | :--- | :--- |
| **`1:1` (One-to-One)** | В дочерней таблице (`user_profiles.user_id`) | На внешний ключ обязательно вешается **`UNIQUE`** (или сам `user_id` объявляется `PRIMARY KEY`)! | Вынос тяжёлых (`bio`, `avatar_blob`) или секретных (`passport_hash`, `kyc_data`) полей из узкой и быстрой таблицы `users` |
| **`1:N` (One-to-Many)** | Строго на стороне **«Многие»** (`orders.user_id`) | Обычный `FOREIGN KEY` **без `UNIQUE`** (один `user_id` может встречаться в 100 заказах) | 80% всех связей в БД: Клиент → Заказы, Пост → Комментарии, Отдел → Сотрудники |
| **`M:N` (Many-to-Many)** | В отдельной **связующей (ассоциативной) таблице** (`post_tags`, `enrollments`) | Два внешних ключа образуют **составной первичный ключ** `PRIMARY KEY (student_id, course_id)` | Статьи ↔ Теги, Заказы ↔ Товары (`order_items`), Пользователи ↔ Роли (`user_roles`) |

---

## 3. Почему связь `M:N` часто содержит полезную нагрузку (Payload)?

Новички часто думают, что связующая таблица для `M:N` состоит только из двух колонок `(order_id, product_id)`. На практике в 90% случаев связь `M:N` обрастает **собственными атрибутами события**:
- В таблице `order_items(order_id, product_id, qty, price_at_purchase)` хранятся количество и цена на момент покупки.
- В таблице `enrollments(student_id, course_id, enrolled_at, grade)` хранятся дата записи на курс и полученная оценка.
А составной первичный ключ `PRIMARY KEY (student_id, course_id)` физически защищает от дублирования: один студент не сможет случайно записаться на один и тот же курс дважды!

> **Junior vs Senior**:
> - **Junior**: Пытается реализовать связь «Один-ко-многим», добавляя массив `order_ids` в таблицу `users`, или создаёт связующую таблицу `M:N` с автоинкрементным `id`, забывая повесить `UNIQUE (student_id, course_id)`, из-за чего в базе появляются дублирующиеся привязки.
> - **Senior**: Всегда размещает внешний ключ `1:N` на стороне «Многие», для связи `1:1` фиксирует инвариант через `UNIQUE NOT NULL REFERENCES ...`, а в ассоциативной таблице `M:N` использует составной первичный ключ `PRIMARY KEY (a_id, b_id)`.

---

## 4. Практикум в Python 3.13: связи `1:1`, `1:N` и `M:N` в действии

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        -- 1. Основная таблица и связь 1:1 (профиль с UNIQUE user_id)
        CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE student_profiles (
            student_id INTEGER PRIMARY KEY REFERENCES students(id) ON DELETE CASCADE,
            github_url TEXT NOT NULL
        );

        -- 2. Связь M:N (студенты <-> курсы через таблицу enrollments с составным PK)
        CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
        CREATE TABLE enrollments (
            student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
            course_id  INTEGER REFERENCES courses(id)  ON DELETE CASCADE,
            grade      INTEGER NOT NULL,
            PRIMARY KEY (student_id, course_id)
        );

        INSERT INTO students VALUES (1, 'Alice'), (2, 'Bob');
        INSERT INTO student_profiles VALUES (1, 'https://github.com/alice');
        INSERT INTO courses VALUES (10, 'SQL Mastery'), (20, 'Async Python');
        INSERT INTO enrollments VALUES (1, 10, 98), (1, 20, 95), (2, 10, 88);
    """)

    sql = """
    SELECT s.name, p.github_url, GROUP_CONCAT(c.title || ':' || e.grade, ', ') AS courses_summary
    FROM students s
    LEFT JOIN student_profiles p ON s.id = p.student_id
    JOIN enrollments e ON s.id = e.student_id
    JOIN courses c ON e.course_id = c.id
    GROUP BY s.id, s.name, p.github_url
    """
    for name, gh, summary in conn.execute(sql):
        print(f"Студент: {name:5s} | GitHub (1:1): {str(gh):24s} | Курсы (M:N): {summary}")
```
''',

    os.path.join('Юнит 5.3 · Проектирование БД', '📚 Конспекты', 'К-137. Ограничения SQL_ NOT NULL, UNIQUE,.md'): r'''📖 Перечитать конспект: Ограничения SQL: NOT NULL, UNIQUE, DEFAULT, CHECK >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Почему проверка в Python/Pydantic НЕ заменяет ограничения в БД?

> **Ментальная модель — «Правила дорожного движения против бетонного отбойника»**: Валидация в коде бэкенда (Pydantic, сериализаторы DRF) — это дорожные знаки: честный водитель их соблюдает. Но в базу данных могут писать 5 разных микросервисов, фоновые воркеры Celery, скрипты миграций или аналитик с прямым доступом через консоль. **Ограничения SQL (Constraints)** — это физический бетонный отбойник на уровне ядра СУБД, который ни при каких обстоятельствах не пропустит невалидные данные (даже при параллельных запросах!).

```text
Эшелонированная оборона целостности данных:
  [Клиент / Браузер] ──> [Pydantic / DRF (Быстрый UX-отказ 422)]
                                │
                                ▼
                         [СУБД: NOT NULL, UNIQUE, CHECK, FK] <── Финальный рубеж!
                         Защищает от Race Conditions и багов во всех сервисах
```

---

## 2. Четыре главных стража целостности (`NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`)

| Ограничение | Что гарантирует на уровне ядра БД | Важная тонкость на собеседовании |
| :--- | :--- | :--- |
| **`NOT NULL`** | Запрещает сохранять пустоту (`NULL`) в столбце | Должно стоять **по умолчанию** на всех колонках, кроме тех, где отсутствие значения имеет явный бизнес-смысл (`deleted_at`, `middle_name`) |
| **`UNIQUE`** | Гарантирует уникальность значения (или комбинации столбцов `UNIQUE (user_id, promocode_id)`) и **автоматически строит B-Tree индекс** | В стандарте SQL `NULL != NULL`! Поэтому в колонку `UNIQUE` можно вставить **сколько угодно `NULL`** (в PostgreSQL 15+ для запрета дублей `NULL` добавили `UNIQUE NULLS NOT DISTINCT`) |
| **`DEFAULT expr`** | Подставляет значение по умолчанию (`0`, `'pending'`, `CURRENT_TIMESTAMP`), если колонка не передана в `INSERT` | Осторожно: если в `INSERT` явно передать `NULL`, то `DEFAULT` **не сработает** (а если стоит `NOT NULL`, запрос упадёт с ошибкой!) |
| **`CHECK (cond)`** | Проверяет произвольное логическое условие перед записью (`CHECK (price >= 0 AND discount <= price)`) | Спасает от отрицательного баланса кошелька и некорректных диапазонов дат (`CHECK (end_date >= start_date)`) |

---

## 3. Почему проверка уникальности в Python через `if not exists:` уязвима к Race Condition?

Представьте, что два потока одновременно регистрируют пользователя с `email = 'dev@py.ru'`:
1. Поток А делает `SELECT 1 FROM users WHERE email = 'dev@py.ru'` $\to$ пусто!
2. Через $0.1$ мс Поток Б делает тот же `SELECT` $\to$ тоже пусто!
3. Оба потока выполняют `INSERT` — и в таблице без `UNIQUE` оказываются **два клона с одинаковым email**!
Только ограничение **`UNIQUE`** в самой базе данных (опирающееся на атомарную блокировку листа B-Tree индекса) гарантирует, что один из потоков получит `IntegrityError` даже при 10 000 одновременных запросов в секунду!

> **Junior vs Senior**:
> - **Junior**: Проверяет `if User.objects.filter(email=email).exists(): raise Error` и `if balance >= amount:` только в Python-коде, оставляя колонки в БД без `UNIQUE` и `CHECK (balance >= 0)`, что приводит к дублям аккаунтов и уходу баланса в минус при параллельных запросах.
> - **Senior**: Дублирует критические бизнес-инварианты на уровне схемы БД (`NOT NULL`, `UNIQUE`, `CHECK (balance >= 0)`), перехватывая `IntegrityError` в слое репозитория.

---

## 4. Практикум в Python 3.13: тестируем броню `NOT NULL`, `UNIQUE`, `DEFAULT` и `CHECK`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("""
        CREATE TABLE wallets (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'active',
            balance INTEGER NOT NULL DEFAULT 0 CHECK (balance >= 0)
        )
    """)

    # 1. Вставка с использованием DEFAULT (status='active', balance=0)
    conn.execute("INSERT INTO wallets (email) VALUES (?)", ("alice@py.ru",))
    print("Кошелёк с DEFAULT:", conn.execute("SELECT email, status, balance FROM wallets").fetchone())

    # 2. Попытка увести баланс в минус блокируется ограничением CHECK (balance >= 0)!
    try:
        conn.execute("UPDATE wallets SET balance = balance - 500 WHERE email = 'alice@py.ru'")
    except sqlite3.IntegrityError as exc:
        print("Броня CHECK остановила уход баланса в минус:", exc)

    # 3. Попытка создать дубликат email блокируется ограничением UNIQUE!
    try:
        conn.execute("INSERT INTO wallets (email) VALUES (?)", ("alice@py.ru",))
    except sqlite3.IntegrityError as exc:
        print("Броня UNIQUE остановила дубль email:", exc)
```
''',

    # =========================================================================
    # ЮНИТ 5.4 · Транзакции (К-138 .. К-143)
    # =========================================================================
    os.path.join('Юнит 5.4 · Транзакции', '📚 Конспекты', 'К-138. ACID_ гарантии надёжности данных.md'): r'''📖 Перечитать конспект: ACID: гарантии надёжности данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Что такое транзакция и зачем нужен стандарт `ACID`?

> **Ментальная модель — «Банковский перевод в бронированной капсуле»**: Перевод 1 000 ₽ от Алисы Бобу состоит из двух шагов: 1) списать 1 000 ₽ у Алисы; 2) начислить 1 000 ₽ Бобу. Если после первого шага в дата-центре вырубят электричество или Боб окажется заблокирован, 1 000 ₽ не должны раствориться в воздухе! **Транзакция** объединяет несколько SQL-команд в одну неделимую капсулу «всё или ничего» (`BEGIN ... COMMIT / ROLLBACK`).

```text
Жизненный цикл транзакции и частичный откат через SAVEPOINT:
  BEGIN;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;  (Шаг 1: Списание)
    SAVEPOINT sp_bonus;                                         (Точка сохранения)
    INSERT INTO bonuses ...;                                    (Шаг 2: Необязательный бонус упал)
    ROLLBACK TO SAVEPOINT sp_bonus;                             (Откатили только бонус, перевод жив!)
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;  (Шаг 3: Зачисление)
  COMMIT;                                                       (Фиксация в WAL на диске!)
```

---

## 2. Расшифровка четырёх столпов `ACID` (и что за них отвечает под капотом)

| Буква | Свойство | Смысл простыми словами | Механизм СУБД под капотом |
| :--- | :--- | :--- | :--- |
| **`A`** | **Atomicity** (*Атомарность*) | «Всё или ничего»: либо все операции транзакции фиксируются целиком, либо при ошибке система возвращается в исходное состояние | Журнал отката (*Undo Log*) и статусы транзакций (`xmin`/`xmax` в PostgreSQL) |
| **`C`** | **Consistency** (*Согласованность*) | Транзакция переводит БД из одного валидного состояния в другое, не нарушая ни одного ограничения (`NOT NULL`, `UNIQUE`, `CHECK`, `FK`) | Проверка всех Constraints и триггеров перед фиксацией (например, общая сумма денег в банке до и после перевода неизменна) |
| **`I`** | **Isolation** (*Изолированность*) | Параллельно бегущие транзакции не должны видеть полуфабрикаты друг друга и портить чужие расчёты | **MVCC** (*Multi-Version Concurrency Control* — многоверсионность строк) + блокировки (*Row Locks*) |
| **`D`** | **Durability** (*Долговечность*) | Если БД ответила клиенту `COMMIT OK`, то даже если через 1 миллисекунду из сервера выдернут шнур питания, данные **не пропадут** | Журнал предзаписи **WAL (*Write-Ahead Logging*)**: изменения сначала синхронно (`fsync`) сбрасываются в последовательный лог на диске |

---

## 3. Как работает `WAL` (Write-Ahead Log) и зачем нужны `SAVEPOINT`?

Почему база данных при `COMMIT` не перезаписывает сразу гигабайтные файлы таблиц и индексов в случайных местах диска (*Random I/O*)? Потому что это было бы слишком медленно!
Вместо этого по правилу **WAL**:
1. Все изменения меняют страницы в быстрой оперативной памяти (*Shared Buffers*), а на диск **последовательно в конец файла WAL** дописывается компактная запись о транзакции (`fsync`).
2. Клиент мгновенно получает ответ `COMMIT`, а фоновый процесс *Checkpointer* позже спокойно переносит грязные страницы из RAM в файлы таблиц.
3. Если же внутри большой транзакции вам нужно попробовать рискованную операцию и при неудаче откатить **только её**, не теряя всю транзакцию целиком, используйте **`SAVEPOINT name`** и **`ROLLBACK TO SAVEPOINT name`**.

> **Junior vs Senior**:
> - **Junior**: Выполняет списание и зачисление двумя отдельными автокоммит-запросами без единого транзакционного контекста (`with conn:`), либо держит открытую транзакцию во время долгого сетевого вызова к внешнему HTTP API (блокируя строки в БД на секунды!).
> - **Senior**: Держит транзакции максимально короткими (никаких HTTP-запросов внутри `BEGIN...COMMIT`), оборачивает связанные изменения в атомарный менеджер контекста (`with session.begin():`) и использует `SAVEPOINT` (`session.begin_nested()`) для локальной обработки ошибок.

---

## 4. Практикум в Python 3.13: ACID-перевод с откатом и `SAVEPOINT`

```python
import sqlite3

def transfer_money(conn: sqlite3.Connection, from_id: int, to_id: int, amount: int) -> bool:
    try:
        # Контекстный менеджер `with conn:` в sqlite3 автоматически делает COMMIT или ROLLBACK при исключении!
        with conn:
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        return True
    except sqlite3.IntegrityError as exc:
        print(f"Транзакция атомарно отменена (ROLLBACK): {exc}")
        return False

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER CHECK (balance >= 0))")
    conn.executemany("INSERT INTO accounts VALUES (?, ?, ?)", [(1, "Alice", 1000), (2, "Bob", 500)])

    # 1. Успешный перевод 400 ₽ (сумма в системе до и после = 1500 ₽)
    transfer_money(conn, 1, 2, 400)
    print("После перевода 400 ₽:", conn.execute("SELECT owner, balance FROM accounts").fetchall())

    # 2. Попытка перевести 9999 ₽ (больше, чем есть у Alice) -> срабатывает CHECK и полный ROLLBACK!
    transfer_money(conn, 1, 2, 9999)
    print("После сбоя (балансы не пострадали!):", conn.execute("SELECT owner, balance FROM accounts").fetchall())
```
''',

    os.path.join('Юнит 5.4 · Транзакции', '📚 Конспекты', 'К-139. Уровни изоляции транзакций.md'): r'''📖 Перечитать конспект: Уровни изоляции транзакций >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Компромисс между скоростью и строгой изоляцией

> **Ментальная модель — «Совместная работа в Google Docs против фотографии страницы»**:
> - На низком уровне изоляции (**Read Committed**) вы видите правки коллег, как только они нажали кнопку «Опубликовать» (`COMMIT`), даже если вы сами ещё читаете документ.
> - На высоком уровне (**Repeatable Read**) в момент открытия документа вы делаете его **мгновенный фотоснимок (Snapshot)**: сколько бы коллеги ни правили текст параллельно, до конца вашей работы вы видите неизменную картину на момент старта!

Если разрешить тысячам транзакций бесконтрольно менять одни и те же строки, возникают **4 классические аномалии конкурентного доступа**:
1. **Dirty Read (Грязное чтение)**: транзакция А читает незафиксированные изменения транзакции Б, а затем Б делает `ROLLBACK` (чтение фантомных денег, которых никогда не было).
2. **Non-Repeatable Read (Неповторяющееся чтение)**: транзакция А дважды читает одну и ту же строку (`WHERE id = 1`), но между чтениями транзакция Б успела изменить её и сделать `COMMIT` — два одинаковых `SELECT` внутри одной транзакции А вернули разные числа!
3. **Phantom Read (Фантомное чтение)**: транзакция А дважды считает `SELECT COUNT(*) FROM orders WHERE amount > 1000`, а между запросами транзакция Б вставила (`INSERT`) новую строку — количество строк изменилось.
4. **Lost Update (Потерянное обновление)**: две транзакции одновременно прочитали `balance = 100`, прибавили в Python `+50` и записали `SET balance = 150` вместо `200` (одна перезатёрла вклад другой!).

---

## 2. Матрица 4 уровней изоляции SQL и особенностей PostgreSQL (MVCC)

В PostgreSQL благодаря архитектуре **MVCC (Multi-Version Concurrency Control)** читатели никогда не блокируют писателей, а писатели не блокируют читателей. Более того, в PostgreSQL грязное чтение невозможо даже на `Read Uncommitted`, а `Repeatable Read` защищает и от фантомных чтений!

| Уровень изоляции | Dirty Read (Грязное чтение) | Non-Repeatable Read | Phantom Read (Фантомы) | Serialization Anomaly |
| :--- | :--- | :--- | :--- | :--- |
| **`READ UNCOMMITTED`** | В стандарте да (в **PostgreSQL ❌ нет**) | ⚠️ Возможно | ⚠️ Возможно | ⚠️ Возможно |
| **`READ COMMITTED`** *(дефолт в PostgreSQL)* | ❌ Защищено | ⚠️ Возможно (каждый `SELECT` видит свежий снимок) | ⚠️ Возможно | ⚠️ Возможно |
| **`REPEATABLE READ`** *(дефолт в MySQL InnoDB)* | ❌ Защищено | ❌ Защищено (снимок на всю транзакцию) | В стандарте да (в **PostgreSQL ❌ защищено!**) | ⚠️ Возможно (Write Skew) |
| **`SERIALIZABLE`** | ❌ Защищено | ❌ Защищено | ❌ Защищено | ❌ Полная защита (SSI) |

---

## 3. Как победить `Lost Update`: пессимистическая (`FOR UPDATE`) vs оптимистическая блокировка

Даже на уровне `READ COMMITTED` наивный код `прочитать баланс в Python -> прибавить -> UPDATE` приведёт к **Lost Update**! Есть три надёжных решения:
1. **Атомарный инкремент в SQL**: `UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100`.
2. **Пессимистическая блокировка (`SELECT ... FOR UPDATE`)**: блокирует выбранную строку на запись для других транзакций до нашего `COMMIT`.
3. **Оптимистическая блокировка (Optimistic Locking по колонке `version`)**: добавляем счётчик версии строки и пишем:
   ```sql
   UPDATE products SET stock = 9, version = version + 1
   WHERE id = 42 AND version = 5;
   -- Если rowcount == 0, значит кто-то успел изменить строку раньше нас -> повторяем попытку (Retry)!
   ```

> **Junior vs Senior**:
> - **Junior**: Читает `user.balance` через ORM на уровне `READ COMMITTED`, в Python вычисляет `user.balance -= 100` и делает `session.commit()`, теряя деньги при двух параллельных запросах (*Lost Update*).
> - **Senior**: Для финансовых операций использует либо `SELECT ... FOR UPDATE` (пессимистическая блокировка), либо оптимистическую блокировку с проверкой `version`, либо уровень `REPEATABLE READ` / `SERIALIZABLE` с автоматическим retry при ошибке сериализации `SQLSTATE 40001`.

---

## 4. Практикум в Python 3.13: воспроизводим `Lost Update` и чиним через Optimistic Locking

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE stock_items (id INTEGER PRIMARY KEY, qty INTEGER, version INTEGER)")
    conn.execute("INSERT INTO stock_items VALUES (1, 10, 1)")

    # Две параллельные сессии одновременно прочитали состояние товара (qty=10, version=1)
    tx1_qty, tx1_ver = conn.execute("SELECT qty, version FROM stock_items WHERE id = 1").fetchone()
    tx2_qty, tx2_ver = conn.execute("SELECT qty, version FROM stock_items WHERE id = 1").fetchone()

    # 1. Первая транзакция списывает 3 шт., проверяя version = 1:
    cur1 = conn.execute(
        "UPDATE stock_items SET qty = ?, version = version + 1 WHERE id = 1 AND version = ?",
        (tx1_qty - 3, tx1_ver),
    )
    print(f"Транзакция 1: обновлено строк = {cur1.rowcount} (успех, новая версия = 2)")

    # 2. Вторая транзакция пытается записать свой расчёт со старой version = 1:
    cur2 = conn.execute(
        "UPDATE stock_items SET qty = ?, version = version + 1 WHERE id = 1 AND version = ?",
        (tx2_qty - 4, tx2_ver),
    )
    print(f"Транзакция 2: обновлено строк = {cur2.rowcount} (Lost Update предотвращён! Нужен retry)")
    print("Итоговое состояние в БД:", conn.execute("SELECT qty, version FROM stock_items").fetchone())
```
''',

    os.path.join('Юнит 5.4 · Транзакции', '📚 Конспекты', 'К-140. Дедлоки в базе данных.md'): r'''📖 Перечитать конспект: Дедлоки в базе данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Как возникает взаимная блокировка (`Deadlock`) в базе данных?

> **Ментальная модель — «Два рыцаря в узком коридоре или перекрёсток без светофора»**: Представьте: Транзакция №1 переводит деньги со счёта `id=1` на счёт `id=2`, а в ту же миллисекунду Транзакция №2 переводит деньги навстречу — со счёта `id=2` на счёт `id=1`. Первая заблокировала счёт `1` и ждёт освобождения счёта `2`. Вторая заблокировала счёт `2` и ждёт освобождения счёта `1`. Ни одна не может сделать шаг вперёд — возник **Deadlock (клинч)**!

```text
Хронология возникновения Deadlock (встречный захват ресурсов):
  Время │ Транзакция T1 (Перевод 1 -> 2)         │ Транзакция T2 (Перевод 2 -> 1)
  ──────┼────────────────────────────────────────┼────────────────────────────────────────
   t1   │ BEGIN;                                 │ BEGIN;
   t2   │ UPDATE accounts ... WHERE id = 1; 🔒1  │ UPDATE accounts ... WHERE id = 2; 🔒2
   t3   │ UPDATE accounts ... WHERE id = 2;      │ UPDATE accounts ... WHERE id = 1;
        │ ⏳ Ждёт освобождения строки id=2 от T2 │ ⏳ Ждёт освобождения строки id=1 от T1
  ──────┴────────────────────────────────────────┴────────────────────────────────────────
  💥 Цикл в графе ожидания (Wait-For Graph): T1 ---> T2 ---> T1 (DEADLOCK!)
```

---

## 2. Как СУБД обнаруживает Deadlock и что с ним делает?

Зависнет ли PostgreSQL навсегда при дедлоке? **Нет!**
1. Если транзакция не может получить блокировку в течение `deadlock_timeout` (в PostgreSQL по умолчанию **`1 секунда`**), движок запускает алгоритм поиска циклов в **графе ожидания (Wait-For Graph)**.
2. Обнаружив замкнутый цикл `T1 -> T2 -> T1`, СУБД выбирает одну из транзакций «жертвой» и принудительно убивает её с ошибкой **`ERROR: deadlock detected (SQLSTATE 40P01)`**, выполняя для неё автоматический `ROLLBACK`.
3. Вторая транзакция мгновенно получает освободившуюся блокировку и успешно завершает свой `COMMIT`!

| Настройка / Инструмент PostgreSQL | Назначение | Как помогает против зависаний |
| :--- | :--- | :--- |
| **`deadlock_timeout = '1s'`** | Пауза перед запуском проверки графа блокировок | Не тратит CPU на поиск циклов для быстрых блокировок (< 1 с) |
| **`lock_timeout = '3s'`** | Максимальное время ожидания освобождения строки/таблицы | Защищает пул соединений от выстраивания в бесконечную очередь за заблокированной строкой |
| **`SELECT ... FOR UPDATE NOWAIT`** | Немедленный отказ при занятой строке | Вместо ожидания сразу бросает ошибку, если строка уже кем-то заблокирована |
| **`SELECT ... FOR UPDATE SKIP LOCKED`** | Пропуск заблокированных строк | Идеально для очередей задач в БД: воркеры разбирают свободные задачи без единого конфликта! |

---

## 3. Золотое правило предотвращения Deadlock: каноническая сортировка ID!

Как гарантировать со 100% математической надёжностью, что встречные переводы между любыми счетами **никогда** не вызовут Deadlock?
**Всегда захватывайте блокировки ресурсов строго в одном и том же порядке (например, по возрастанию `id`)!**
- Если T1 переводит `1 -> 2`, а T2 переводит `2 -> 1`, обе транзакции сначала сортируют пару ID: `first_id, second_id = sorted([from_id, to_id])` $\implies$ `(1, 2)`.
- Обе транзакции сначала пытаются заблокировать счёт **`id = 1`**: T1 захватывает `id=1`, а T2 спокойно ждёт на `id=1` (не держа в руках блокировку `id=2`!). T1 блокирует `id=2`, делает `COMMIT`, и следом проходит T2. Цикл ожидания физически невозможен!

> **Junior vs Senior**:
> - **Junior**: При переводе между счетами или обновлении пачки товаров блокирует строки в том порядке, в каком они пришли из JSON-запроса пользователя, регулярно получая `DeadlockDetected` под нагрузкой.
> - **Senior**: Перед выполнением `SELECT ... FOR UPDATE` или пакетного `UPDATE` всегда сортирует список ID по возрастанию (`ORDER BY id ASC`), настраивает `lock_timeout` и оборачивает транзакцию в декоратор повторных попыток (Retry with Jitter) на случай `SQLSTATE 40P01`.

---

## 4. Практикум в Python 3.13: детектор циклов Wait-For Graph и защита сортировкой ресурсов

```python
def acquire_locks_ordered(tx_name: str, acc_a: int, acc_b: int) -> list[int]:
    """Канонический захват блокировок строго по возрастанию ID исключает цикл ожидания!"""
    first_id, second_id = sorted((acc_a, acc_b))
    print(f"[{tx_name}] Запрос перевода {acc_a} -> {acc_b}: блокируем строго по порядку [{first_id}, {second_id}]")
    return [first_id, second_id]

def has_deadlock_cycle(wait_for_graph: dict[str, str]) -> bool:
    """Поиск цикла в графе ожидания транзакций (Wait-For Graph)"""
    for start_node in wait_for_graph:
        visited = set()
        curr = start_node
        while curr in wait_for_graph:
            if curr in visited:
                return True
            visited.add(curr)
            curr = wait_for_graph[curr]
    return False

# 1. Наивный встречный захват: T1 ждёт T2 (держит #2), а T2 ждёт T1 (держит #1)
naive_graph = {"T1": "T2", "T2": "T1"}
print("Цикл Deadlock при хаотичном порядке:", has_deadlock_cycle(naive_graph))

# 2. Канонический порядок блокировок по возрастанию ID:
order_t1 = acquire_locks_ordered("T1", 1, 2)
order_t2 = acquire_locks_ordered("T2", 2, 1)
assert order_t1 == order_t2 == [1, 2]
print("Порядок захвата идентичен -> Deadlock невозможен!")
```
''',

    os.path.join('Юнит 5.4 · Транзакции', '📚 Конспекты', 'К-141. Индексы в базах данных.md'): r'''📖 Перечитать конспект: Индексы в базах данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Что такое индекс и почему B-Tree находит строку за $O(\log n)$?

> **Ментальная модель — «Алфавитный указатель в конце энциклопедии»**: Если вас попросят найти все упоминания слова «Транзакция» в книге на 1 000 страниц без оглавления, вам придётся прочитать каждую страницу от корки до корки (**`Seq Scan` за $O(n)$**). **Индекс** — это отсортированный указатель в конце книги, где напротив слова «Транзакция» сразу написан точный номер страницы и строки (**`TID` — Tuple ID** на диске).

По умолчанию команда `CREATE INDEX` в PostgreSQL, MySQL и SQLite строит сбалансированное дерево **B-Tree (Balanced Tree)**:
- Все листья дерева находятся на одной глубине (обычно всего 3–4 уровня даже для $100\,000\,000$ строк!).
- Листья **отсортированы** по ключу и связаны двусвязным списком — поэтому B-Tree умеет мгновенно выполнять не только точный поиск `=`, но и диапазоны `>`, `<`, `BETWEEN`, префиксный поиск `LIKE 'abc%'` и сортировку `ORDER BY` без `Sort`!

```text
Структура B-Tree индекса по колонке email:
                   [ "m..." ]                      <-- Корень (Root Page, в RAM)
                  /          \
        [ "a..".."l.." ]    [ "m..".."z.." ]       <-- Внутренние узлы
            /                  \
  ["alice" -> p.42] <===> ["mike" -> p.108]        <-- Листья с указателями TID на строки таблицы
```

---

## 2. Виды индексов в PostgreSQL и их специализация

| Тип индекса | Синтаксис / Особенность | Для каких запросов создан |
| :--- | :--- | :--- |
| **B-Tree** *(по умолчанию)* | `CREATE INDEX idx_u_email ON users(email)` | `=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `IN`, `IS NULL`, `ORDER BY` |
| **Составной (Composite)** | `ON orders (user_id, created_at DESC)` | Работает по **правилу левого префикса**: ускоряет поиск по `(user_id)` и по `(user_id, created_at)`, но **не работает**, если в `WHERE` указан только второй столбец `created_at`! |
| **Покрывающий (Covering)** | `ON users (email) INCLUDE (name, role)` | Хранит доп. колонки прямо в листьях индекса $\implies$ даёт сверхбыстрый **`Index Only Scan`** без похода в саму таблицу (*Heap*)! |
| **Частичный (Partial)** | `ON orders (user_id) WHERE status = 'pending'` | Индексирует только нужное подмножество строк (занимает в 10 раз меньше RAM и диска!) |
| **GIN (Generalized Inverted)** | `CREATE INDEX ... USING GIN (tags)` | Массивы, документы **`JSONB`** (оператор `@>`) и полнотекстовый поиск (`tsvector`) |
| **Hash / BRIN** | `USING HASH` / `USING BRIN (created_at)` | Hash — только `=`; BRIN — крошечный индекс по диапазонам блоков для огромных таблиц логов, растущих по времени |

---

## 3. Почему нельзя заиндексировать все колонки подряд и когда индекс «слепнет»?

1. **Цена индекса на записи**: каждый дополнительный индекс ускоряет `SELECT`, но **замедляет каждый `INSERT`, `UPDATE` и `DELETE`**, так как СУБД вынуждена перестраивать каждое дерево индекса и тратить место в RAM и на диске.
2. **Низкая селективность (Кардинальность)**: индекс по колонке `gender` (`'M'` / `'F'`) или `is_active` (`true` / `false`, где 90% строк `true`) бесполезен — базе быстрее прочитать таблицу подряд (`Seq Scan`), чем прыгать по указателям за 90% строк.
3. **Когда индекс перестаёт работать**:
   - Функция поверх колонки: `WHERE LOWER(email) = 'a@b.ru'` $\implies$ обычный индекс по `email` ослепнет! Нужен **функциональный индекс** `CREATE INDEX ON users (LOWER(email))`.
   - Ведущий процент в `LIKE`: `WHERE name LIKE '%ov'` (поиск по суффиксу не может идти по алфавитному B-Tree; для поиска подстрок используют триграммы `pg_trgm` + `GIN`).

> **Junior vs Senior**:
> - **Junior**: Создаёт отдельные одиночные индексы на каждую колонку таблицы или пишет `WHERE YEAR(created_at) = 2026`, удивляясь, почему индекс по `created_at` не используется.
> - **Senior**: Переписывает условие без функции поверх колонки (`WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`), проектирует составные и частичные индексы по правилу левого префикса, а на живом продакшене строит их без блокировки таблицы командой `CREATE INDEX CONCURRENTLY`.

---

## 4. Практикум в Python 3.13: проверяем правило левого префикса через `EXPLAIN QUERY PLAN`

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT, created_at TEXT)")
    # Создаём составной B-Tree индекс (левый столбец — user_id, второй — status)
    conn.execute("CREATE INDEX idx_orders_user_status ON orders(user_id, status)")

    # 1. Поиск по левому префиксу (user_id И status) -> используется индекс!
    plan_fast = conn.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42 AND status = 'paid'"
    ).fetchall()

    # 2. Поиск только по второму столбцу (status без user_id) -> правило левого префикса нарушено (SCAN)!
    plan_slow = conn.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'paid'"
    ).fetchall()

    # 3. Покрывающий запрос (выбираем только колонки, которые уже есть в самом индексе -> COVERING INDEX!)
    plan_cov = conn.execute(
        "EXPLAIN QUERY PLAN SELECT user_id, status FROM orders WHERE user_id = 42"
    ).fetchall()

    print("1. Поиск по (user_id, status) :", plan_fast[0][3])
    print("2. Поиск только по (status)   :", plan_slow[0][3])
    print("3. Покрывающий запрос         :", plan_cov[0][3])
```
''',

    os.path.join('Юнит 5.4 · Транзакции', '📚 Конспекты', 'К-142. EXPLAIN_ как читать план выполнения запроса.md'): r'''📖 Перечитать конспект: EXPLAIN: как читать план выполнения запроса >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Рентген SQL-запроса: разница между `EXPLAIN` и `EXPLAIN ANALYZE`

> **Ментальная модель — «Прогноз навигатора против реальной поездки по пробкам»**:
> - **`EXPLAIN SELECT ...`** — это прогноз навигатора перед выездом: планировщик СУБД смотрит в статистику таблиц и **предсказывает** маршрут и примерную стоимость (`cost`), **не выполняя сам запрос**.
> - **`EXPLAIN ANALYZE SELECT ...`** — вы реально проехали маршрут с секундомером в руках: СУБД **выполняет запрос до конца** и показывает рядом и прогноз, и **фактическое время (`actual time`)** в миллисекундах, и реальное число прочитанных строк!

⚠️ **Осторожно с `EXPLAIN ANALYZE` на `UPDATE` / `DELETE`!** Поскольку `EXPLAIN ANALYZE` реально выполняет запрос, он **удалит или изменит строки**! Чтобы безопасно замерить план модифицирующего запроса, всегда оборачивайте его в транзакцию с откатом:
```sql
BEGIN;
EXPLAIN ANALYZE DELETE FROM logs WHERE created_at < '2025-01-01';
ROLLBACK;
```

```text
Как читать строку узла плана в PostgreSQL:
  Index Scan using idx_users_email on users  (cost=0.29..8.31 rows=1 width=64) (actual time=0.018..0.019 rows=1 loops=1)
                                              \________/ \__/ \____/            \______________________/ \____/ \_____/
                                              Старт..Итог Прогноз               Реальное время в мс      Факт   Сколько раз
                                              в усл. ед.  числа строк                                    строк  вызывался узел
```

---

## 2. Четыре базовых типа сканирования таблиц (от медленных к быстрым)

| Узел плана (`Scan Node`) | Как работает физически | Когда это хорошо, а когда — катастрофа? |
| :--- | :--- | :--- |
| **`Seq Scan` (Sequential Scan)** | Читает всю таблицу подряд от первой страницы до последней ($O(n)$) | Нормально для маленьких таблиц (< 1000 строк) или когда выбирается > 20% таблицы. **Катастрофа**, если ищем 5 строк из 10 миллионов! |
| **`Index Scan`** | Ищет ключ в B-Tree за $O(\log n)$, берёт адрес `TID` и прыгает в таблицу (*Heap*) за остальными колонками строки | Идеально для точечных выборок (1..1000 строк) |
| **`Bitmap Index Scan` + `Bitmap Heap Scan`** | При выборке тысяч строк сначала строит в памяти битовую карту нужных страниц диска, сортирует их по порядку и читает без хаотичных прыжков | Отлично подходит для условий средней селективности и объединения двух разных индексов (`BitmapAnd` / `BitmapOr`) |
| **`Index Only Scan`** | Все запрошенные в `SELECT` колонки нашлись прямо в листьях покрывающего индекса — **в саму таблицу идти вообще не нужно!** | ⚡ Абсолютный чемпион по скорости чтения |

---

## 3. Алгоритмы соединения таблиц (`Nested Loop`, `Hash Join`, `Merge Join`)

Когда вы делаете `JOIN` двух таблиц, оптимизатор выбирает один из трёх алгоритмов:
1. **`Nested Loop` (Вложенный цикл)**: для каждой строки внешней таблицы ищет совпадение во внутренней. Очень быстр, если внешняя выборка маленькая (например, 10 строк), а во внутренней таблице есть индекс по ключу соединения (`loops=10`).
2. **`Hash Join`**: загружает меньшую таблицу в хэш-таблицу в оперативной памяти (`work_mem`), а затем за один проход сканирует большую таблицу. Лучший выбор для соединения больших выборок без сортировки!
3. **`Merge Join`**: если обе выборки уже отсортированы по ключу `JOIN` (например, взяты из B-Tree индексов), сливает их за один линейный проход, как застёжка-молния.

> **Junior vs Senior**:
> - **Junior**: Пытается угадать причину тормозов запроса «на глаз» или смотрит только на прогнозный `cost` без запуска `EXPLAIN (ANALYZE, BUFFERS)`.
> - **Senior**: Запускает `EXPLAIN (ANALYZE, BUFFERS)`, читает дерево плана снизу вверх (от самых глубоких сдвинутых вправо узлов), ищет расхождение между ожидаемым `rows` и фактическим `actual rows` (сигнал устаревшей статистики — нужен `ANALYZE table`), проверяет `Buffers: shared hit / read` и устраняет `Seq Scan` с большим `Rows Removed by Filter`.

---

## 4. Практикум в Python 3.13: сравниваем время и план `Seq Scan` против `Index Scan`

```python
import sqlite3
import time

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, user_id INTEGER, payload TEXT)")
    conn.executemany(
        "INSERT INTO events (user_id, payload) VALUES (?, ?)",
        [(i % 5000, f"event_data_{i}") for i in range(20000)],
    )

    # 1. План ДО создания индекса (полный перебор SCAN events)
    plan_before = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = 777").fetchall()
    t0 = time.perf_counter()
    res1 = conn.execute("SELECT COUNT(*) FROM events WHERE user_id = 777").fetchone()[0]
    dt_scan = (time.perf_counter() - t0) * 1000

    # 2. Создаём B-Tree индекс и повторно снимаем план (SEARCH events USING INDEX)
    conn.execute("CREATE INDEX idx_events_user ON events(user_id)")
    plan_after = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = 777").fetchall()
    t1 = time.perf_counter()
    res2 = conn.execute("SELECT COUNT(*) FROM events WHERE user_id = 777").fetchone()[0]
    dt_idx = (time.perf_counter() - t1) * 1000

    print(f"До индекса   : {plan_before[0][3]} | Найдено: {res1} ({dt_scan:.3f} мс)")
    print(f"После индекса: {plan_after[0][3]} | Найдено: {res2} ({dt_idx:.3f} мс)")
```
''',

    os.path.join('Юнит 5.4 · Транзакции', '📚 Конспекты', 'К-143. Шардирование и репликация базы данных.md'): r'''📖 Перечитать конспект: Шардирование и репликация базы данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Когда одной базе данных становится тесно: Репликация против Шардирования

> **Ментальная модель — «Ксерокопии учебника против энциклопедии в 10 томах»**:
> - **Репликация (Replication)** — вы делаете 5 полных ксерокопий одного учебника и раздаёте читателям: в каждой копии лежат **100% одних и тех же данных**, поэтому 5 человек могут читать параллельно, а если один учебник сгорит — остальные спасут библиотеку.
> - **Шардирование (Sharding / Horizontal Partitioning)** — книга разрослась до 50 000 страниц и больше не помещается на стол. Вы разрезаете её на **10 отдельных томов по буквам алфавита** (`Том 1: А–Г`, `Том 2: Д–Ж`...) и ставите на разные столы: теперь на каждом сервере хранится только **своя кусочек (1/10 часть) данных**!

```text
1. РЕПЛИКАЦИЯ (Масштабирование ЧТЕНИЯ и отказоустойчивость — копии 100% данных):
   [Запись INSERT/UPDATE] ──> [Primary (Master)]
                                  ├──(Поток WAL)──> [Replica 1] <── Чтение SELECT
                                  └──(Поток WAL)──> [Replica 2] <── Чтение SELECT

2. ШАРДИРОВАНИЕ (Масштабирование ЗАПИСИ и объёма диска — данные разрезаны по ключу):
   Роутер: shard_id = hash(user_id) % 3
      ├──> [Shard 0: users 0, 3, 6...] (Свой диск и RAM)
      ├──> [Shard 1: users 1, 4, 7...] (Свой диск и RAM)
      └──> [Shard 2: users 2, 5, 8...] (Свой диск и RAM)
```

---

## 2. Асинхронная vs Синхронная репликация и ловушка `Replication Lag`

В классической схеме **Single-Leader (Master-Slave / Primary-Replica)** все операции записи (`INSERT`, `UPDATE`, `DELETE`) идут строго на **Primary**, который транслирует поток журнала `WAL` на **Read Replicas**:

| Тип репликации | Как подтверждается `COMMIT`? | Главный плюс | Главный риск |
| :--- | :--- | :--- | :--- |
| **Асинхронная (Async)** | Primary пишет в свой WAL и **сразу отвечает клиенту `OK`**, а реплики догоняют его через 5–100 мс | ⚡ Не замедляет запись; падение реплики не останавливает Primary | **Replication Lag**: клиент обновил аватарку (на Primary), обновил страницу (попал на Replica) и увидел **старую аватарку**! |
| **Синхронная (Sync)** | Primary ждёт подтверждения записи в WAL хотя бы от одной синхронной реплики перед ответом `OK` | 🛡 Нулевая потеря данных (`RPO = 0`) при внезапной смерти диска Primary | Любая сетевая задержка до реплики замедляет каждый `COMMIT` |

Как защитить пользователя от **Replication Lag** после изменения профиля? Применяют паттерн **Read-Your-Own-Writes**: в течение 2–5 секунд после `POST`/`PUT` запросы на чтение от этого конкретного пользователя направляются напрямую в **Primary**!

---

## 3. Стратегии шардирования и проблема `Hotspot` (Горячего шарда)

При шардировании критически важно правильно выбрать **ключ шардирования (Shard Key)**:
1. **По диапазону (Range Sharding)**: например, по месяцам или ID (`1..1 000 000` на Шард 1). Легко делать диапазонные запросы, но все новые регистрации идут на **последний шард** (*Hotspot* — один сервер горит от 100% нагрузки, пока остальные простаивают!).
2. **По хэшу (Hash / Modulo Sharding)**: `shard = crc32(user_id) % N` или **Consistent Hashing (Консистентное хэширование)**. Распределяет нагрузку идеально равномерно, но при изменении числа серверов `N` обычное деление `% N` потребует перевезти почти все ключи (поэтому используют *Consistent Hashing Ring*, где при добавлении узла переезжает только $1/N$ ключей).

> **Junior vs Senior**:
> - **Junior**: Предлагает внедрить шардирование на таблице в 5 миллионов строк, где проблема решается одним B-Tree индексом за 2 секунды, не осознавая, что шардирование ломает межшардовые `JOIN` и транзакции.
> - **Senior**: Масштабирует БД по строгой лестнице: 1) Оптимизация индексов и запросов (`EXPLAIN ANALYZE`) $\to$ 2) Кэширование в Redis и пулинг соединений (`PgBouncer`) $\to$ 3) Партиционирование таблицы внутри одного сервера и Read-реплики $\to$ 4) И только на сотнях терабайт — шардирование по `tenant_id` / `user_id`.

---

## 4. Практикум в Python 3.13: роутер шардирования и `Read-Your-Own-Writes` против Replication Lag

```python
import hashlib

class ShardedCluster:
    def __init__(self, num_shards: int = 3) -> None:
        self.num_shards = num_shards
        self.shards: dict[int, dict[int, str]] = {i: {} for i in range(num_shards)}

    def get_shard_id(self, user_id: int) -> int:
        digest = hashlib.md5(str(user_id).encode()).hexdigest()
        return int(digest, 16) % self.num_shards

    def save_user(self, user_id: int, name: str) -> int:
        sid = self.get_shard_id(user_id)
        self.shards[sid][user_id] = name
        return sid

cluster = ShardedCluster(num_shards=3)
for uid in range(1, 10):
    cluster.save_user(uid, f"User_{uid}")

for sid, data in cluster.shards.items():
    print(f"Шард #{sid}: хранит {len(data)} пользователей -> {list(data.keys())}")
```
''',

    # =========================================================================
    # ЮНИТ 5.5 · ORM и миграции (К-144 .. К-148)
    # =========================================================================
    os.path.join('Юнит 5.5 · ORM и миграции', '📚 Конспекты', 'К-144. SQLAlchemy_ ORM для Python.md'): r'''📖 Перечитать конспект: SQLAlchemy: ORM для Python >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Архитектура SQLAlchemy 2.0: `Engine`, `Core` и `ORM` (`Session`)

> **Ментальная модель — «Заводской конвейер, чертежи и личный секретарь»**:
> - **`Engine` + `Connection Pool`** — это телефонная станция с пулом открытых линий связи до PostgreSQL.
> - **SQLAlchemy Core** — это конструктор SQL-запросов на Python, работающий напрямую с таблицами и строками без магии классов.
> - **SQLAlchemy ORM + `Session`** — это личный секретарь (паттерн **Unit of Work** + **Identity Map**): вы берёте у него Python-объект `user = session.get(User, 1)`, меняете `user.name = 'Alice'`, и секретарь сам помнит все изменения в блокноте, чтобы при вызове `session.commit()` отправить в базу один аккуратный `UPDATE`!

```text
Архитектура слоёв SQLAlchemy 2.0:
  [Ваше приложение: Python-объекты User, Order]
        │
        ▼
  [SQLAlchemy ORM: DeclarativeBase, Mapped[T], Session (Unit of Work + Identity Map)]
        │
        ▼
  [SQLAlchemy Core: выражение select(User).where(...), Table, MetaData]
        │
        ▼
  [Engine + QueuePool (Пул соединений)] ──> [Драйвер БД: psycopg / asyncpg / sqlite3]
```

---

## 2. Жизненный цикл объекта в `Session` и современный синтаксис SQLAlchemy 2.0

В SQLAlchemy 2.0 устаревший стиль `session.query(User)` заменён на единый типизированный синтаксис с `Mapped[...]` и функцией `select(...)`:

| Состояние объекта в `Session` | Как объект туда попадает | Что о нём знает база данных? |
| :--- | :--- | :--- |
| **1. `Transient` (Временный)** | Только что создан в Python: `u = User(name='Bob')` | Нет в `Session`, нет в БД (`u.id is None`) |
| **2. `Pending` (Ожидающий)** | Добавлен в сессию: `session.add(u)` | В блокноте `Session` помечен на вставку, но `INSERT` в БД ещё не отправлен |
| **3. `Persistent` (Привязанный)** | После `session.flush()` / `commit()` или чтения `session.scalars(select(User))` | Записан в БД и отслеживается в кэше `Identity Map` сессии |
| **4. `Detached` (Отвязанный)** | После закрытия сессии `session.close()` | Обращение к не подгруженным связям вызовет `DetachedInstanceError`! |

Важное различие:
- **`session.flush()`** — отправляет накопившиеся `INSERT`/`UPDATE`/`DELETE` по сети в открытую транзакцию БД (объект уже получает сгенерированный `id`), но **не фиксирует транзакцию** (её всё ещё можно откатить через `rollback()`).
- **`session.commit()`** — сначала автоматически вызывает `flush()`, а затем фиксирует транзакцию в БД (`COMMIT`).

---

## 3. Главный враг производительности ORM — проблема `N+1 запросов` и методы `joinedload` / `selectinload`

Когда вы загружаете список из $N = 50$ авторов (`SELECT * FROM authors` — **1 запрос**), а затем в цикле `for author in authors: print(author.books)` обращаетесь к связанной коллекции, ленивая загрузка (*Lazy Loading*) делает **по одному отдельному SQL-запросу на каждого из 50 авторов**! Вместо 1 запроса база получает $1 + 50 = 51$ запрос!
Как победить проблему $N+1$ через **Eager Loading (Жадную загрузку)**:
- **`joinedload(Book.author)`** (аналог **`select_related`** в Django ORM): подтягивает одиночный объект (`Many-to-One` / `One-to-One`) в **одном запросе через `LEFT OUTER JOIN`**.
- **`selectinload(Author.books)`** (аналог **`prefetch_related`** в Django ORM): подтягивает коллекцию (`One-to-Many` / `Many-to-Many`) **вторым запросом `WHERE author_id IN (1, 2, ...)`**, избегая размножения строк при `JOIN`!

> **Junior vs Senior**:
> - **Junior**: Перебирает связанные объекты ORM внутри цикла шаблона или сериализатора без `selectinload` / `joinedload`, порождая сотни скрытых SQL-запросов ($N+1$), а в асинхронном FastAPI получает падение `MissingGreenlet` при попытке неявного ленивого запроса.
> - **Senior**: Явно указывает стратегию жадной загрузки (`options(joinedload(...), selectinload(...))`), в асинхронном коде включает `lazy="raise"`, чтобы любая забытая ленивая связь сразу обнаруживалась на тестах, и управляет транзакцией через паттерн Unit of Work.

---

## 4. Практикум в Python 3.13: демонстрация проблемы `N+1` (1 + N запросов) против `Eager Loading` (2 запроса)

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.executescript("""
        CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE books (id INTEGER PRIMARY KEY, author_id INTEGER, title TEXT);
        INSERT INTO authors VALUES (1, 'Мартин Фаулер'), (2, 'Роберт Мартин'), (3, 'Гвидо ван Россум');
        INSERT INTO books VALUES (10, 1, 'Рефакторинг'), (11, 1, 'Шаблоны КПП'), (12, 2, 'Чистый код'), (13, 3, 'Python Tutorial');
    """)

    # Считаем реальное число выполненных SQL-запросов через set_trace_callback:
    sql_count = 0
    def count_queries(sql: str) -> None:
        global sql_count
        if sql.strip().upper().startswith("SELECT"):
            sql_count += 1
    conn.set_trace_callback(count_queries)

    # 1. Антипаттерн N+1 (Lazy Loading в цикле): 1 запрос за авторами + 3 запроса за книгами = 4 запроса!
    sql_count = 0
    authors = conn.execute("SELECT id, name FROM authors").fetchall()
    for aid, name in authors:
        books = conn.execute("SELECT title FROM books WHERE author_id = ?", (aid,)).fetchall()
    print(f"Подход Junior (N+1 в цикле на {len(authors)} авторах) : выполнено {sql_count} SQL-запросов")

    # 2. Подход Senior (selectinload / prefetch_related): ровно 2 запроса независимо от числа авторов!
    sql_count = 0
    authors = conn.execute("SELECT id, name FROM authors").fetchall()
    author_ids = [a[0] for a in authors]
    placeholders = ",".join("?" * len(author_ids))
    all_books = conn.execute(f"SELECT author_id, title FROM books WHERE author_id IN ({placeholders})", author_ids).fetchall()
    print(f"Подход Senior (selectinload через WHERE IN) : выполнено {sql_count} SQL-запроса!")
```
''',

    os.path.join('Юнит 5.5 · ORM и миграции', '📚 Конспекты', 'К-145. Миграции базы данных.md'): r'''📖 Перечитать конспект: Миграции базы данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Что такое миграции БД и почему они — «Git для схемы таблиц»?

> **Ментальная модель — «Пошаговая инструкция сборки LEGO с кнопкой перемотки назад»**: Если один разработчик добавил новую колонку в свою локальную базу руками через GUI-клиент, у его коллег и на продакшен-сервере код тут же упадёт, потому что их базы об этом не знают! **Миграция базы данных** — это обычный файл с кодом в Git-репозитории, который содержит две функции: **`upgrade()`** (как перевести схему на шаг вперёд) и **`downgrade()`** (как безопасно откатить это изменение назад).

```text
Цепочка ревизий миграций (Directed Acyclic Graph) и таблица версий в самой БД:
  [0001_init_users] ──> [0002_add_orders] ──> [0003_add_phone_col]  <-- Код в Git (HEAD)
                                                       ^
  Таблица в БД `alembic_version`: version_num = '0003_add_phone_col' (База знает свою текущую версию!)
```

Как система миграций понимает, какие файлы уже выполнены, а какие — ещё нет?
Прямо внутри вашей базы данных создаётся крошечная служебная таблица (**`alembic_version`** в Alembic или **`django_migrations`** в Django), где хранится ID последней применённой ревизии!

---

## 2. Миграции схемы против миграций данных и опасные операции на продакшене

Все миграции делятся на два типа:
1. **Schema Migrations (DDL)**: создание таблиц, добавление колонок, индексов и внешних ключей.
2. **Data Migrations (DML)**: заполнение новых колонок вычисленными данными (например, разбиение старого поля `full_name` на `first_name` и `last_name`).

На живом продакшене с миллионами строк и 24/7 трафиком **нельзя просто так делать любые DDL-команды** — многие из них берут эксклюзивную блокировку таблицы (`ACCESS EXCLUSIVE LOCK`), останавливая все `SELECT` и `INSERT`:

| Операция в миграции | Чем опасна на большой таблице в продакшене? | Безопасный Zero-Downtime подход (Senior) |
| :--- | :--- | :--- |
| **`CREATE INDEX idx ...`** | Блокирует `INSERT`/`UPDATE`/`DELETE` на всё время построения дерева (минуты!) | Использовать **`CREATE INDEX CONCURRENTLY`** вне транзакции |
| **Переименование колонки (`RENAME COLUMN`)** | В момент деплоя старые контейнеры приложения мгновенно падают с `UndefinedColumn` | Паттерн **Expand & Contract** в 3 релиза (добавить новую $\to$ синхронизировать $\to$ удалить старую) |
| **Добавление `FOREIGN KEY` или `CHECK`** | Сканирует всю таблицу для проверки старых строк под жёсткой блокировкой | Сначала создать ключ с флагом **`NOT VALID`** (мгновенно!), а затем выполнить `VALIDATE CONSTRAINT` без блокировки чтения/записи |

---

## 3. Золотые правила работы с миграциями в команде

1. **Применённая в `main` миграция неизменна (Immutable)**: никогда не редактируйте задним числом файл миграции, который уже ушёл в общий Git и накатился на стейджинг/продакшен! Чтобы изменить схему, создайте **новую** миграцию.
2. **Всегда проверяйте автогенерацию глазами**: инструменты вроде `alembic revision --autogenerate` сравнивают модели Python с БД, но при переименовании колонки `name -> title` автогенератор часто пишет **`drop_column('name')` + `add_column('title')`**, что **уничтожит все данные в столбце**!
3. **Тестируйте откат (`downgrade`)**: миграция без работающей функции `downgrade()` делает невозможным быстрый откат релиза при аварии.

> **Junior vs Senior**:
> - **Junior**: Запускает `autogenerate`, не глядя коммитит сгенерированный файл (в котором переименование превратилось в `DROP COLUMN` с потерей данных) и правит уже запушенные миграции задним числом.
> - **Senior**: Всегда вычитывает SQL-план миграции перед деплоем, проверяет обратимость `upgrade() <-> downgrade()`, строит индексы с `postgresql_concurrently=True` и разделяет DDL-миграции схемы и пакетные Data-миграции.

---

## 4. Практикум в Python 3.13: собственный движок миграций с `upgrade`, `downgrade` и таблицей версий

```python
import sqlite3

MIGRATIONS = [
    (
        "0001_create_users",
        "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)",
        "DROP TABLE users",
    ),
    (
        "0002_add_is_vip",
        "ALTER TABLE users ADD COLUMN is_vip INTEGER NOT NULL DEFAULT 0",
        # В SQLite 3.35+ поддерживается ALTER TABLE DROP COLUMN!
        "ALTER TABLE users DROP COLUMN is_vip",
    ),
]

def run_migrations(conn: sqlite3.Connection, target_rev: str | None = None) -> str:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version (rev TEXT NOT NULL)")
    row = conn.execute("SELECT rev FROM schema_version").fetchone()
    current_rev = row[0] if row else None

    if target_rev == "base" and current_rev == "0002_add_is_vip":
        # Демонстрируем откат последней миграции (downgrade)
        _, _, down_sql = MIGRATIONS[1]
        conn.execute(down_sql)
        conn.execute("UPDATE schema_version SET rev = ?", (MIGRATIONS[0][0],))
        return MIGRATIONS[0][0]

    for rev, up_sql, _ in MIGRATIONS:
        if current_rev is None or rev > current_rev:
            conn.execute(up_sql)
            conn.execute("DELETE FROM schema_version")
            conn.execute("INSERT INTO schema_version VALUES (?)", (rev,))
            current_rev = rev
    return current_rev or "base"

with sqlite3.connect(":memory:") as conn:
    head = run_migrations(conn)
    cols_head = [c[1] for c in conn.execute("PRAGMA table_info(users)")]
    print(f"После upgrade до {head} -> колонки users: {cols_head}")

    prev = run_migrations(conn, target_rev="base")
    cols_prev = [c[1] for c in conn.execute("PRAGMA table_info(users)")]
    print(f"После downgrade до {prev} -> колонки users: {cols_prev}")
```
''',

    os.path.join('Юнит 5.5 · ORM и миграции', '📚 Конспекты', 'К-146. Alembic_ миграции для SQLAlchemy.md'): r'''📖 Перечитать конспект: Alembic: миграции для SQLAlchemy >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Как устроен `Alembic` и откуда он знает про ваши модели?

> **Ментальная модель — «Архитектурный инспектор с двумя чертежами»**: Когда вы запускаете `alembic revision --autogenerate -m "add orders"`, Alembic кладёт на стол два чертежа: слева — `Base.metadata` из ваших Python-моделей SQLAlchemy (какой база *должна* стать), справа — реальную структуру таблиц в подключённой PostgreSQL (какая база *сейчас*). Сравнив их, он автоматически пишет черновик Python-скрипта с командами `op.create_table(...)` и `op.add_column(...)`!

```text
Структура проекта с Alembic:
  project/
   ├── alembic.ini              (Конфиг логирования и путь к папке миграций)
   └── alembic/
        ├── env.py              (Точка входа: сюда импортируют `target_metadata = Base.metadata`!)
        ├── script.py.mako      (Шаблон генерации новых файлов миграций)
        └── versions/           (Папка с файлами ревизий)
             ├── 1a2b_init.py       (revision = '1a2b', down_revision = None)
             └── 3c4d_add_orders.py (revision = '3c4d', down_revision = '1a2b')
```

⚠️ **Самая частая ошибка новичка при настройке Alembic**: вы написали новую модель `class Order(Base): ...` в файле `models/order.py`, запускаете `alembic revision --autogenerate`, а Alembic генерирует **пустую миграцию (`pass`)**!
Почему? Потому что файл `models/order.py` не был импортирован до того, как `env.py` прочитал `Base.metadata`! Чтобы `Base.metadata` увидел все таблицы, все файлы моделей должны быть явно импортированы в `env.py` (или в `models/__init__.py`).

---

## 2. Главные команды CLI и операции объекта `op` в скрипте ревизии

| Команда Alembic CLI | Что делает |
| :--- | :--- |
| `alembic init alembic` | Создаёт структуру папки `alembic/` и файл `alembic.ini` |
| `alembic revision --autogenerate -m "msg"` | Сравнивает `Base.metadata` с БД и создаёт новый файл в `versions/` |
| `alembic upgrade head` | Накатывает все неприменённые миграции до самой свежей вершины (`head`) |
| `alembic downgrade -1` (или `base`) | Откатывает последнюю миграцию назад (`-1`) или сносит всё до нуля (`base`) |
| `alembic current` / `alembic history` | Показывает текущую ревизию в таблице `alembic_version` и дерево истории |
| `alembic heads` / `alembic merge heads` | Обнаруживает ветвление (когда 2 разработчика параллельно создали миграции от одного родителя) и склеивает две головы в одну merge-миграцию |

---

## 3. Анатомия файла ревизии Alembic и безопасное добавление `NOT NULL` колонки

Каждый файл в `alembic/versions/` содержит связку `revision` / `down_revision` и две функции:
```python
revision = "3c4d_add_status"
down_revision = "1a2b_init"

def upgrade() -> None:
    # Если в таблице уже есть строки, нельзя просто добавить NOT NULL без значения!
    # Шаг 1: добавляем колонку как nullable (или с server_default)
    op.add_column("orders", sa.Column("status", sa.String(32), server_default="new", nullable=False))

def downgrade() -> None:
    op.drop_column("orders", "status")
```

> **Junior vs Senior**:
> - **Junior**: Прописывает пароль от продакшен-базы прямо в `alembic.ini` (коммитя секрет в Git!) и пытается добавить колонку `nullable=False` без `server_default` в таблицу, где уже лежат 100 000 пользователей, получая падение деплоя с `NotNullViolation`.
> - **Senior**: Считывает `DATABASE_URL` в `alembic/env.py` из переменных окружения (`os.environ` / Pydantic Settings), для новых `NOT NULL` колонок на живых таблицах задаёт `server_default` или заполняет старые строки батчами перед включением `nullable=False`, а в CI проверяет отсутствие двух голов (`alembic heads`).

---

## 4. Практикум в Python 3.13: симулятор автогенерации диффа схемы (`Base.metadata` vs БД)

```python
import sqlite3

def autogenerate_diff(model_columns: dict[str, str], db_conn: sqlite3.Connection, table: str) -> list[str]:
    """Сравнивает целевую схему модели Python с реальной таблицей в БД (как делает Alembic --autogenerate)"""
    existing_cols = {row[1]: row[2] for row in db_conn.execute(f"PRAGMA table_info({table})")}
    ops = []
    for col_name, col_type in model_columns.items():
        if col_name not in existing_cols:
            ops.append(f"op.add_column('{table}', sa.Column('{col_name}', sa.{col_type}()))")
    for col_name in existing_cols:
        if col_name not in model_columns:
            ops.append(f"op.drop_column('{table}', '{col_name}')")
    return ops

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, legacy_flag INTEGER)")
    target_model = {"id": "Integer", "email": "String", "phone": "String", "created_at": "DateTime"}

    generated_ops = autogenerate_diff(target_model, conn, "users")
    print("Сгенерированные операции Alembic upgrade():")
    for op_line in generated_ops:
        print("  ", op_line)
```
''',

    os.path.join('Юнит 5.5 · ORM и миграции', '📚 Конспекты', 'К-147. PostgreSQL против MySQL.md'): r'''📖 Перечитать конспект: PostgreSQL против MySQL >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Архитектурная философия: PostgreSQL vs MySQL (InnoDB)

> **Ментальная модель — «Швейцарский инженерный комбайн против лёгкого городского седана»**:
> - **PostgreSQL** — объектно-реляционная СУБД, созданная с фокусом на строжайшее соблюдение стандарта SQL, расширяемость, сложную аналитику и богатейшую систему типов (`JSONB`, массивы, геоданные PostGIS, векторный поиск `pgvector`).
> - **MySQL (движок InnoDB)** — классическая реляционная СУБД, исторически спроектированная для максимальной простоты и быстрых чтений по первичному ключу в веб-приложениях (WordPress, биллинги, каталоги).

```text
Главное отличие хранения данных и MVCC на диске:
  PostgreSQL (Heap Table + Версии строк):
    - Таблица (Heap) не упорядочена по PK; все индексы (включая PK) указывают на физический адрес TID.
    - UPDATE создаёт НОВУЮ версию строки (tuple), а старую помечает удалённой -> нужен фоновый AUTOVACUUM!

  MySQL InnoDB (Clustered Index + Undo Log):
    - Сама таблица физически является листьями B-Tree индекса по PRIMARY KEY (Кластерный индекс)!
    - UPDATE меняет строку на месте, а старую версию прячет в отдельный журнал Undo Log.
```

---

## 2. Сравнительная таблица ключевых отличий для собеседования

| Критерий | **PostgreSQL** | **MySQL (движок InnoDB)** |
| :--- | :--- | :--- |
| **Уровень изоляции по умолчанию** | **`READ COMMITTED`** | **`REPEATABLE READ`** |
| **Реализация MVCC и `UPDATE`** | Создаёт новый кортеж (*new tuple*) в таблице; старые версии чистит процесс **`AUTOVACUUM`** | Модифицирует запись на месте, а прошлые версии хранит в сегменте отката (*Undo Log*) |
| **Организация таблицы на диске** | Куча (**Heap**): все индексы равноправны и ссылаются на физический номер страницы и слота (`ctid`) | **Кластерный индекс** по `PRIMARY KEY`: вторичные индексы хранят внутри себя значение PK! |
| **Транзакционность DDL (`ALTER`, `DROP`)** | ✅ **Полная**: можно сделать `BEGIN; ALTER TABLE ...; ROLLBACK;`! | ❌ **Нет**: любая DDL-команда вызывает неявный `COMMIT`, откатить миграцию через `ROLLBACK` нельзя |
| **Типы индексов и работа с JSON** | B-Tree, **GIN**, GiST, BRIN, Hash + частичные и функциональные индексы; бинарный **`JSONB`** с индексацией | В основном B-Tree (+ Fulltext/Spatial); тип `JSON` уступает по индексации `JSONB` |
| **Чувствительность к регистру и `GROUP BY`** | Строго по стандарту: `'Alice' != 'alice'` (`LIKE` чувствителен, для безрегистрового есть `ILIKE`) | Зависит от Collation (по умолчанию `'Alice' = 'alice'`) |

---

## 3. Что такое `VACUUM` в PostgreSQL и почему кластерный индекс в MySQL не любит `UUID v4`?

Два глубоких вопроса, которые отличают Senior-разработчика:
1. **Зачем PostgreSQL нужен `AUTOVACUUM`?** Поскольку при каждом `UPDATE` и `DELETE` PostgreSQL не стирает строку сразу (она может быть нужна параллельным транзакциям по MVCC!), в таблице копятся «мёртвые кортежи» (*dead tuples*), вызывая раздувание таблицы (*table bloat*). Фоновый демон `autovacuum` помечает место от мёртвых строк как свободное для новых записей и обновляет карту видимости (*Visibility Map* для `Index Only Scan`).
2. **Почему в MySQL InnoDB опасно делать `UUID v4` первичным ключом?** В InnoDB сама таблица физически отсортирована по `PRIMARY KEY` (кластерный индекс), а каждый вторичный индекс хранит копию `PRIMARY KEY`. Случайный 16-байтный `UUID v4` заставляет InnoDB вставлять новые строки в случайные места середины таблицы на диске, вызывая постоянное расщепление страниц (*Page Splits*) и раздувая все вторичные индексы!

> **Junior vs Senior**:
> - **Junior**: Считает, что PostgreSQL и MySQL отличаются только синтаксисом `SERIAL` vs `AUTO_INCREMENT`, и пытается обернуть миграцию в транзакцию на MySQL, не зная, что `ALTER TABLE` в MySQL делает принудительный `COMMIT`.
> - **Senior**: Учитывает архитектуру хранения: в PostgreSQL следит за метриками *dead tuples* и настройками `autovacuum` на часто обновляемых таблицах, а также использует транзакционный DDL для атомарных миграций.

---

## 4. Практикум в Python 3.13: проверяем транзакционный DDL (`BEGIN -> ALTER TABLE -> ROLLBACK`)

```python
import sqlite3

# SQLite, как и PostgreSQL, поддерживает транзакционный DDL (в отличие от MySQL)!
with sqlite3.connect(":memory:", isolation_level=None) as conn:
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")

    # Открываем транзакцию, меняем структуру таблицы (DDL) и откатываем её через ROLLBACK!
    conn.execute("BEGIN")
    conn.execute("ALTER TABLE users ADD COLUMN temp_col TEXT DEFAULT 'test'")
    cols_inside = [c[1] for c in conn.execute("PRAGMA table_info(users)")]
    print("Колонки ВНУТРИ транзакции после ALTER TABLE :", cols_inside)

    conn.execute("ROLLBACK")
    cols_after = [c[1] for c in conn.execute("PRAGMA table_info(users)")]
    print("Колонки ПОСЛЕ ROLLBACK (транзакционный DDL!):", cols_after)
```
''',

    os.path.join('Юнит 5.5 · ORM и миграции', '📚 Конспекты', 'К-148. JSONB и массивы в PostgreSQL.md'): r'''📖 Перечитать конспект: JSONB и массивы в PostgreSQL >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Зачем реляционной PostgreSQL нужны `JSONB` и массивы (`ARRAY`)?

> **Ментальная модель — «Жёсткий чемодан с эластичным карманом-органайзером»**: В интернет-магазине у каждого товара всегда есть `id`, `title`, `price` и `stock` — это жёсткий каркас чемодана (классические SQL-колонки в 3НФ). Но у кроссовок есть размер стельки и цвет шнурков, у процессора — частота ГГц и сокет, а у книги — число страниц и ISBN. Создавать 500 полупустых колонок на все случаи жизни безумно! Для таких вариативных характеристик в PostgreSQL есть **бинарный документ `JSONB`** — быстрый NoSQL-карман прямо внутри ACID-транзакционной таблицы!

Чем **`JSONB` (Binary JSON)** отличается от старого текстового типа **`JSON`** в PostgreSQL?

| Характеристика | Тип `JSON` (Текстовый) | Тип `JSONB` (Бинарный — стандарт де-факто) |
| :--- | :--- | :--- |
| **Как хранится на диске?** | Как сырая текстовая строка (со всеми пробелами и повторами ключей) | Распарсенное бинарное дерево ключей и значений (удаляет пробелы и дубли ключей) |
| **Скорость записи (`INSERT`)** | Чуть быстрее (не тратит время на парсинг дерева) | Чуть медленнее при вставке из-за компиляции в бинарный формат |
| **Скорость чтения и фильтрации** | 🐢 Медленно: парсит текст с нуля при каждом `SELECT`! | ⚡ **Мгновенно**: читает бинарные смещения без парсинга текста |
| **Поддержка `GIN`-индексов и `@>`** | ❌ Нет | ✅ **Полная поддержка `GIN`-индексов!** |

---

## 2. Операторы работы с `JSONB` и магия `GIN`-индекса

Чтобы искать и извлекать поля из `JSONB` в PostgreSQL, нужно знать 4 главных оператора:

```text
Шпаргалка операторов JSONB в PostgreSQL (колонка `specs JSONB`):
  1. specs -> 'brand'          --> Возвращает значение как тип JSONB (в кавычках: '"Apple"')
  2. specs ->> 'brand'         --> Возвращает значение как обычный TEXT (без кавычек: 'Apple')
  3. specs @> '{"ram": 16}'    --> Оператор ВХОЖДЕНИЯ (содержит ли JSONB указанную подструктуру?)
  4. specs ? 'wifi'            --> Существует ли ключ 'wifi' на верхнем уровне документа?
```

Как ускорить поиск по миллионам `JSONB`-документов или массивов `TEXT[]`?
Обычный B-Tree индекс не умеет заглядывать *внутрь* элементов массива или ключей словаря. Для этого в PostgreSQL существует **`GIN` (Generalized Inverted Index — обобщённый инвертированный индекс)**:
```sql
-- Создаём GIN-индекс по JSONB-колонке:
CREATE INDEX idx_products_specs_gin ON products USING GIN (specs);

-- Запрос с оператором вхождения @> взлетает за O(log n) по GIN-индексу!
SELECT id, title FROM products WHERE specs @> '{"ram": 16, "ssd": 512}';
```

---

## 3. Когда использовать `JSONB` и массивы, а когда — обычные таблицы?

- **Используйте `JSONB` / `ARRAY`**, когда:
  - Храните динамические атрибуты товаров (EAV-замена), пользовательские настройки (`preferences`), сырые payload вебхуков или список тегов статьи (`tags TEXT[]`).
- **НЕ используйте `JSONB`**, когда:
  - Внутри JSON прячутся сущности, на которые нужны внешние ключи (`FOREIGN KEY`), частые частичные обновления отдельных полей каждую секунду или строгая агрегация `SUM`/`JOIN` по всей базе.

> **Junior vs Senior**:
> - **Junior**: Фильтрует `JSONB` через текстовое извлечение `WHERE specs ->> 'ram' = '16'`, не зная, что оператор `->>` **не использует общий `GIN`-индекс** по колонке `specs`, из-за чего база сканирует всю таблицу (`Seq Scan`).
> - **Senior**: Создаёт `GIN`-индекс (`USING GIN (specs)`) и пишет запросы через оператор вхождения **`WHERE specs @> '{"ram": 16}'`**, получая мгновенный `Bitmap Index Scan` по инвертированному индексу.

---

## 4. Практикум в Python 3.13: JSON-запросы в SQLite (`json_extract`) и модель инвертированного `GIN`-индекса

```python
import json
import sqlite3

class GinInvertedIndex:
    """Модель работы инвертированного индекса GIN для поиска по вхождению (@>) за O(1)"""
    def __init__(self) -> None:
        self.postings: dict[tuple[str, object], set[int]] = {}

    def index_doc(self, doc_id: int, payload: dict) -> None:
        for k, v in payload.items():
            self.postings.setdefault((k, v), set()).add(doc_id)

    def query_contains(self, sub_doc: dict) -> set[int]:
        sets = [self.postings.get((k, v), set()) for k, v in sub_doc.items()]
        return set.intersection(*sets) if sets else set()

with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE laptops (id INTEGER PRIMARY KEY, title TEXT, specs TEXT)")
    items = [
        (1, "MacBook Pro 16", {"brand": "Apple", "ram": 32, "ssd": 1024}),
        (2, "ThinkPad X1", {"brand": "Lenovo", "ram": 16, "ssd": 512}),
        (3, "MacBook Air", {"brand": "Apple", "ram": 16, "ssd": 512}),
    ]
    gin = GinInvertedIndex()
    for lid, title, spec in items:
        conn.execute("INSERT INTO laptops VALUES (?, ?, ?)", (lid, title, json.dumps(spec)))
        gin.index_doc(lid, spec)

    # 1. SQL-фильтрация по JSON-полю через встроенную функцию json_extract:
    rows = conn.execute(
        "SELECT title FROM laptops WHERE json_extract(specs, '$.brand') = 'Apple' AND json_extract(specs, '$.ram') >= 16"
    ).fetchall()
    print("Найдено через SQL json_extract:", [r[0] for r in rows])

    # 2. Поиск через инвертированный индекс GIN по условию specs @> {"ram": 16, "ssd": 512}:
    matched_ids = gin.query_contains({"ram": 16, "ssd": 512})
    print("Найдено ID через GIN-индекс (@>):", sorted(matched_ids))
```
''',

    # =========================================================================
    # ЮНИТ 5.6 · NoSQL и кэш (К-149 .. К-155)
    # =========================================================================
    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-149. SQL против NoSQL.md'): r'''📖 Перечитать конспект: SQL против NoSQL >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Реляционные (`SQL`) против нереляционных (`NoSQL`) баз данных

> **Ментальная модель — «Аптечный шкаф с ячейками по ГОСТу против грузовых контейнеров»**:
> - **Реляционная БД (SQL — PostgreSQL, MySQL)** — это аптечный шкаф: каждая таблетка разложена по подписанным ящичкам (3НФ), связана строгими рецептами (`FOREIGN KEY`) и защищена правилами `ACID`.
> - **Нереляционная БД (NoSQL — Redis, MongoDB, Cassandra)** — это специализированные склады под конкретную форму груза: где-то хранятся готовые запечатанные коробки-документы (`JSON`), где-то — мгновенные ячейки камер хранения (`Key-Value` в RAM), а где-то — бесконечные ленты датчиков (`Wide-Column`).

Термин **NoSQL** расшифровывается как **«Not Only SQL»** (не только SQL). В современных системах SQL и NoSQL не воюют друг с другом, а работают в тандеме (**Polyglot Persistence**): PostgreSQL хранит деньги и заказы, Redis — сессии и кэш, Elasticsearch — полнотекстовый поиск по каталогу.

```text
Классификация 4 семейств NoSQL баз данных:
  ├── 1. Key-Value (Ключ-Значение в RAM)   : Redis, Memcached       (Кэш, сессии, очереди, Rate Limit)
  ├── 2. Document (Документоориентированные): MongoDB, Couchbase     (Каталоги с гибкой схемой, анкеты)
  ├── 3. Wide-Column (Колоночные / Семьи)   : Cassandra, ScyllaDB, ClickHouse (Телеметрия IoT, логи, аналитика)
  └── 4. Graph (Графовые)                   : Neo4j                  (Соцсети, поиск кратчайших связей, антифрод)
```

---

## 2. Теорема CAP и модель `BASE` против `ACID`

Для распределённых баз данных действует **теорема CAP (Брюера)**: в присутствии сетевого разделения между узлами (**`P` — Partition Tolerance**, когда связь между двумя дата-центрами оборвалась) система вынуждена выбрать одно из двух:
- **`CP` (Consistency + Partition Tolerance)**: система отвечает ошибкой или ждёт восстановления кворума, но **никогда не отдаст устаревшие данные** (например, банковский реестр, ZooKeeper, etcd, MongoDB при `majority`).
- **`AP` (Availability + Partition Tolerance)**: каждый узел продолжает отвечать клиентам даже без связи с соседями, но данные на узлах временно расходятся и сходятся чуть позже (**`BASE` — Basically Available, Soft state, Eventually Consistent**, например Cassandra, DynamoDB).

| Критерий сравнения | Реляционные СУБД (`SQL`) | Документные / Распределённые (`NoSQL`) |
| :--- | :--- | :--- |
| **Схема данных** | Жёсткая (`Schema-on-Write`), проверяется при `INSERT` | Гибкая (`Schema-on-Read`), документы в одной коллекции могут отличаться |
| **Связи и чтение** | Данные нормализованы (3НФ), собираются через `JOIN` | Данные **денормализованы** (вложены в один документ), читаются за 1 обращение без `JOIN` |
| **Масштабирование** | Преимущественно вертикальное + Read-реплики | Изначально спроектированы под горизонтальное шардирование на десятки серверов |
| **Модель надёжности** | Строгий **`ACID`** | От **`BASE`** (*Eventual Consistency*) до настраиваемого кворума |

---

## 3. Главное правило проектирования в NoSQL: «Query-Driven Design»

В реляционном мире мы проектируем таблицы **от предметной области** (сущности «Юзер», «Заказ», «Товар» в 3НФ), а потом пишем к ним любые `SELECT ... JOIN`.
В мире NoSQL всё наоборот: мы проектируем структуру документа или ключа **от конкретных запросов экрана приложения (Query-Driven Design)**! Если экран карточки заказа всегда показывает заказ вместе со списком его позиций и адресом доставки, в документоориентированной БД они сохраняются **одним вложенным JSON-документом**, чтобы считываться с диска за одно обращение по ключу!

> **Junior vs Senior**:
> - **Junior**: Выбирает MongoDB для биллинга с переводами денег между балансами пользователей или, наоборот, пытается делать в NoSQL-базе нормализацию на 10 коллекций с ручными «джойнами» в цикле Python.
> - **Senior**: Использует PostgreSQL как основной источник истины для транзакционных данных (`ACID`), подключает Redis для горячего кэша и блокировок, а в документных БД проектирует агрегаты так, чтобы 95% чтений укладывались в обращение к одному документу без `JOIN`.

---

## 4. Практикум в Python 3.13: сравнение нормализованной модели SQL и денормализованного агрегата NoSQL

```python
# 1. Реляционная модель (SQL 3NF): данные разложены по 3 таблицам, сборка требует JOIN
sql_users = {1: {"name": "Alice"}}
sql_orders = {101: {"user_id": 1, "status": "paid"}}
sql_items = [{"order_id": 101, "sku": "KB-1", "price": 120}, {"order_id": 101, "sku": "MS-2", "price": 60}]

def read_order_sql_join(order_id: int) -> dict:
    order = sql_orders[order_id]
    user = sql_users[order["user_id"]]
    items = [it for it in sql_items if it["order_id"] == order_id]
    return {"order_id": order_id, "customer": user["name"], "total": sum(i["price"] for i in items), "items": items}

# 2. Документная модель (NoSQL Aggregate): весь заказ хранится одним готовым документом по ключу O(1)!
nosql_orders_collection = {
    101: {
        "_id": 101,
        "customer": "Alice",
        "total": 180,
        "items": [{"sku": "KB-1", "price": 120}, {"sku": "MS-2", "price": 60}],
    }
}

print("Сборка через SQL JOIN   :", read_order_sql_join(101)["total"], "₽")
print("Чтение NoSQL за O(1)    :", nosql_orders_collection[101]["total"], "₽")
```
''',

    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-150. MongoDB_ документоориентированная база данных.md'): r'''📖 Перечитать конспект: MongoDB: документоориентированная база данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Как устроена MongoDB: Коллекции, Документы `BSON` и ключ `_id`

> **Ментальная модель — «Папка с личными делами в формате BSON»**: Вместо таблиц с жёсткой сеткой колонок в MongoDB используются **коллекции (Collections)**, внутри которых лежат самодостаточные **документы (Documents)**. На диске документы хранятся не как текстовый JSON, а в бинарном типизированном формате **`BSON` (Binary JSON)**, который поддерживает даты (`Date`), `Decimal128`, массивы и уникальный 12-байтный ключ **`ObjectId`** в обязательном поле **`_id`**.

| Понятие в SQL (PostgreSQL) | Аналог в MongoDB | Важная особенность в MongoDB |
| :--- | :--- | :--- |
| Таблица (`Table`) | **Коллекция (`Collection`)** | Не требует `CREATE TABLE` со списком колонок (хотя поддерживает `JSON Schema` валидацию) |
| Строка (`Row` / `Tuple`) | **BSON-документ (`Document`)** | Может содержать вложенные словари и списки (максимальный размер одного документа — **16 МБ**!) |
| Первичный ключ (`PRIMARY KEY`) | Поле **`_id`** (`ObjectId`) | Индексируется автоматически; первые 4 байта `ObjectId` содержат **Unix timestamp** момента создания! |
| `JOIN` таблиц | Вложенность (**Embedding**) или стадия `$lookup` | Если данные всегда читаются вместе — они вкладываются внутрь одного документа |

---

## 2. Главная архитектурная развилка: Вкладывать (`Embedding`) или Ссылаться (`Referencing`)?

Поскольку жёсткий лимит размера одного BSON-документа в MongoDB равен **16 МБ**, нельзя бесконечно пушить элементы во вложенный массив!

```text
Когда ВКЛАДЫВАТЬ внутрь документа (Embedding):        Когда ВЫНОСИТЬ по ссылке (Referencing):
  {                                                     Коллекция posts: {"_id": 1, "title": "..."}
    "_id": 100,                                                 ^
    "name": "Alice",                                            │ (Поле post_id с индексом)
    "addresses": [                                      Коллекция comments (может быть 1 000 000 штук!):
      {"city": "Moscow", "zip": "101000"},                {"_id": 901, "post_id": 1, "text": "..."}
      {"city": "Kazan",  "zip": "420000"}                 {"_id": 902, "post_id": 1, "text": "..."}
    ]
  }
  ✅ Ограниченный список (2-10 адресов, позиции чека),  ✅ Неограниченно растущий список (логи, комментарии),
     всегда читается целиком вместе с родителем.           иначе документ пробьёт потолок 16 МБ!
```

---

## 3. Операторы запросов, атомарных модификаций (`$set`, `$inc`, `$push`) и Aggregation Pipeline

В MongoDB любая модификация одного документа является **атомарной на уровне этого документа**:
- **Фильтрация в `find(...)`**: `{"price": {"$gte": 100, "$lte": 500}, "tags": {"$in": ["python", "sql"]}}`.
- **Атомарное обновление в `update_one(filter, update)`**:
  - `{"$set": {"status": "shipped"}}` — изменить только указанные поля (не затирая весь документ!);
  - `{"$inc": {"views": 1}}` — атомарно увеличить счётчик на 1;
  - `{"$push": {"tags": "new_tag"}}` / `{"$addToSet": ...}` — добавить элемент в массив.
- **Конвейер агрегации (`aggregate([...])`)**: цепочка стадий `[{"$match": ...}, {"$group": {"_id": "$category", "total": {"$sum": "$price"}}}, {"$sort": {"total": -1}}]`. Стадия **`$match`** всегда должна идти первой, чтобы отсечь ненужные документы по B-Tree индексу до группировки!

> **Junior vs Senior**:
> - **Junior**: Хранит все комментарии к популярному посту или историю транзакций во вложенном массиве внутри документа пользователя (получая падение базы при достижении лимита 16 МБ на документ!) или обновляет документ целиком, затирая изменения параллельных потоков.
> - **Senior**: Вкладывает только ограниченные по размеру поддокументы (*Bounded Arrays*), для неограниченных списков использует отдельные коллекции с индексом, а обновления выполняет атомарными операторами `$set` и `$inc`.

---

## 4. Практикум в Python 3.13: движок запросов и конвейера агрегации в стиле `pymongo`

```python
class InMemoryCollection:
    """Компактная эмуляция коллекции MongoDB с поддержкой $gte, $inc, $set и aggregate pipeline"""
    def __init__(self) -> None:
        self.docs: list[dict] = []

    def insert_many(self, items: list[dict]) -> None:
        self.docs.extend(dict(it) for it in items)

    def update_one(self, flt: dict, update: dict) -> int:
        for doc in self.docs:
            if all(doc.get(k) == v for k, v in flt.items()):
                for field, val in update.get("$set", {}).items():
                    doc[field] = val
                for field, delta in update.get("$inc", {}).items():
                    doc[field] = doc.get(field, 0) + delta
                return 1
        return 0

    def aggregate_sum_by_category(self, min_price: int) -> dict[str, int]:
        # Аналог конвейера [{"$match": {"price": {"$gte": min_price}}}, {"$group": {"_id": "$cat", "sum": {"$sum": "$price"}}}]
        totals: dict[str, int] = {}
        for d in self.docs:
            if d["price"] >= min_price:
                totals[d["cat"]] = totals.get(d["cat"], 0) + d["price"]
        return totals

products = InMemoryCollection()
products.insert_many([
    {"_id": 1, "title": "Клавиатура", "cat": "hw", "price": 120, "views": 10},
    {"_id": 2, "title": "Монитор", "cat": "hw", "price": 400, "views": 5},
    {"_id": 3, "title": "Кабель", "cat": "acc", "price": 15, "views": 1},
])

products.update_one({"_id": 1}, {"$inc": {"views": 1}, "$set": {"price": 130}})
print("Документ #1 после атомарного $inc и $set:", products.docs[0])
print("Результат конвейера aggregate (price >= 100):", products.aggregate_sum_by_category(100))
```
''',

    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-151. Управление TTL в Redis.md'): r'''📖 Перечитать конспект: Управление TTL в Redis >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Зачем каждому ключу кэша нужен `TTL` (Time-To-Live)?

> **Ментальная модель — «Срок годности на пакете молока в холодильнике»**: Оперативная память (`RAM`) на сервере стоит дорого и строго ограничена. Если складывать в Redis сессии пользователей, одноразовые SMS-коды и закэшированные страницы без срока годности, через неделю память переполнится на 100%, и Redis начнёт падать с `OOM (Out Of Memory)`! **TTL (Time-To-Live)** — это встроенный таймер самоуничтожения ключа: как только время вышло, ключ автоматически исчезает, освобождая RAM и защищая пользователей от бесконечно устаревших данных.

```text
Коды возврата команды TTL key в Redis (частый вопрос на собеседовании!):
  ├── TTL > 0  (например, 3590)  --> Ключ существует, до автоудаления осталось 3590 секунд
  ├── TTL == -1                  --> Ключ существует, но у него НЕТ срока жизни (живёт вечно!)
  └── TTL == -2                  --> Ключа НЕ существует (уже протух и удалён или не создавался)
```

---

## 2. Все команды управления временем жизни и почему `SET ... EX` лучше `SET` + `EXPIRE`

| Команда Redis / Вызов в `redis-py` | Что делает | Когда применять |
| :--- | :--- | :--- |
| **`r.set(key, val, ex=3600)`** | Атомарно сохраняет значение И ставит TTL в **секундах** | Основной способ записи в кэш (1 сетевой вызов!) |
| **`r.set(key, val, px=500)`** | Атомарно ставит TTL в **миллисекундах** | Короткие распределённые блокировки, троттлинг API |
| **`r.set(key, val, exat=ts)`** | Удаляет ключ ровно в указанный **Unix timestamp** | Акции и промокоды, которые должны протухнуть ровно в полночь |
| **`r.expire(key, 60)`** | Назначает или обновляет TTL уже существующему ключу (например, `Hash` или `List`) | Продление сессии или установка TTL на счётчик `INCR` |
| **`r.ttl(key)` / `r.pttl(key)`** | Возвращает остаток времени жизни в секундах / миллисекундах (`-1` = вечный, `-2` = нет ключа) | Диагностика кэша и расчёт заголовка `Retry-After` |
| **`r.persist(key)`** | Снимает таймер с ключа, делая его вечным (`TTL` становится `-1`) | Отмена автоудаления |

⚠️ **Ловушка неатомарности и сброса TTL**:
1. Если написать двумя командами `r.set('k', 'v')`, а затем `r.expire('k', 60)`, и между ними воркер упадёт по таймауту сети — ключ `'k'` останется в RAM **навсегда без TTL (`-1`)**! Всегда передавайте `ex=...` прямо внутрь `r.set(key, val, ex=60)`.
2. Обычный повторный вызов `r.set('k', 'new_val')` без флага `ex` или `keepttl=True` **полностью стирает ранее установленный таймер TTL** и делает ключ бессмертным!

---

## 3. Проблема `Cache Avalanche` (Лавина кэша) и спасительный `TTL Jitter`

Представьте: в полночь вы прогрели кэш и сохранили 10 000 популярных товаров с одинаковым `ex=3600` (ровно 1 час). Что произойдёт ровно в `01:00:00`?
Все 10 000 ключей **умрут в одну и ту же секунду**! Мгновенно тысячи запросов пользователей промахнутся мимо пустого кэша и одновременно обрушатся на PostgreSQL, положив базу данных (**Cache Avalanche — лавинообразный пробой кэша**).
**Решение Senior-разработчика — `TTL Jitter` (случайный разброс времени жизни)**:
```python
import random

ttl_with_jitter = 3600 + random.randint(-300, 300)  # От 55 до 65 минут!
print("TTL с Jitter (сек):", ttl_with_jitter)
```
Теперь ключи истекают плавно в течение 10 минут, и пиковой ударной волны на БД никогда не возникает!

> **Junior vs Senior**:
> - **Junior**: Ставит `r.set(k, v)` и отдельной строкой `r.expire(k, 3600)`, а при пакетном прогреве кэша задаёт всем 10 000 ключам одинаковый константный TTL, провоцируя `Cache Avalanche`.
> - **Senior**: Задаёт TTL атомарно (`r.set(k, v, ex=3600 + random.randint(0, 300))`), помнит коды возврата `r.ttl()` (`-1` вечный, `-2` отсутствует) и при обновлении значения сохраняет старый таймер через `keepttl=True`.

---

## 4. Практикум в Python 3.13: жизненный цикл TTL (`>0`, `-1`, `-2`), `PERSIST` и `TTL Jitter`

```python
import random
import redis

r = redis.Redis()

# 1. Атомарная установка ключа с TTL и проверка кодов возврата r.ttl():
r.set("promo:code", "SALE25", ex=120)
r.set("config:site_name", "Python Academy")  # Без ex -> живёт вечно (TTL = -1)

print("TTL ключа с таймером (promo:code)      :", r.ttl("promo:code"), "сек (> 0)")
print("TTL вечного ключа    (config:site_name):", r.ttl("config:site_name"), "(-1 = нет TTL)")
print("TTL несуществующего  (ghost:key)       :", r.ttl("ghost:key"), "(-2 = нет ключа)")

# 2. Снимаем таймер командой PERSIST -> ключ становится вечным (-1):
r.persist("promo:code")
print("TTL promo:code после r.persist()       :", r.ttl("promo:code"))

# 3. Генерация TTL с Jitter против лавины кэша (Cache Avalanche):
random.seed(42)
ttls = [3600 + random.randint(-300, 300) for _ in range(5)]
print("Примеры TTL с Jitter вокруг 3600 с     :", ttls)
```
''',

    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-152. Redis.md'): r'''📖 Перечитать конспект: Redis: архитектура и структуры данных >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Почему `Redis` выдаёт 100 000+ RPS в одном потоке?

> **Ментальная модель — «Шеф-повар, у которого все ингредиенты уже нарезаны на столе»**: Обычная база данных бегает за каждым продуктом в дальний подвал (на диск SSD), поэтому ей нужны 50 официантов-потоков, которые постоянно толкаются в дверях (блокировки и переключение контекста ОС). **Redis** держит все данные **прямо на столе в оперативной памяти (`RAM`)**, а основной цикл обработки команд выполняет **один сверхбыстрый поток на базе мультиплексирования ввода-вывода (`epoll` / Event Loop)**!

Три причины феноменальной скорости Redis:
1. **Хранение в RAM**: доступ к оперативной памяти ($\approx 100$ наносекунд) в тысячи раз быстрее похода на диск.
2. **Однопоточное ядро выполнения команд**: нет потерь CPU на мьютексы, блокировки строк и гонки потоков — каждая команда (`INCR`, `HSET`, `LPUSH`) выполняется **атомарно**!
3. **Готовые структуры данных на Си**: Redis — это не просто словарь строк, а сервер структур данных (хэш-таблицы, двусвязные списки, множества, отсортированныеSkipList-таблицы).

```text
Персистентность в Redis (как не потерять данные из RAM при перезагрузке сервера):
  ├── 1. RDB (Snapshotting)     : Компактный бинарный слепок всей памяти раз в N минут.
  │                               Быстрый старт, но данные за последние минуты между снимками могут пропасть.
  └── 2. AOF (Append Only File) : Журнал каждой команды записи (fsync каждую секунду — `everysec`).
                                  Максимальная сохранность (потеря <= 1 сек), в продакшене включают RDB + AOF!
```

---

## 2. Пять базовых структур данных Redis и их идеальные сценарии

| Структура данных | Главные команды | Сложность | Где применять в бэкенде? |
| :--- | :--- | :--- | :--- |
| **`String` (Строки и числа)** | `SET`, `GET`, `INCR`, `DECR`, `MGET` | $O(1)$ | Кэш HTML/JSON, атомарные счётчики просмотров, **Rate Limiting** (`INCR` + `EXPIRE`) |
| **`Hash` (Хэш-словари)** | `HSET`, `HGET`, `HGETALL`, `HINCRBY` | $O(1)$ на поле | Профиль пользователя или сессия (`user:42` $\to$ `{name, role, balance}`): можно менять 1 поле без перезаписи всего JSON! |
| **`List` (Двусвязный список)** | `LPUSH`, `RPUSH`, `LPOP`, `RPOP`, `LRANGE` | $O(1)$ с краёв | Очереди фоновых задач (FIFO/LIFO), лента последних 50 уведомлений (`LPUSH` + `LTRIM`) |
| **`Set` (Множество уникальных)** | `SADD`, `SREM`, `SISMEMBER`, `SINTER` | $O(1)$ проверка | Уникальные посетители, множество ID лайкнувших пост, общие друзья (`SINTER`) |
| **`Sorted Set / ZSET`** | `ZADD`, `ZRANGE`, `ZRANK`, `ZINCRBY` | $O(\log n)$ | **Таблица лидеров (Leaderboard)** в реальном времени, Sliding Window Rate Limiter по timestamp |

---

## 3. Ускорение сети через `Pipeline` и атомарная блокировка `SET NX EX`

1. **Проблема RTT (Round-Trip Time)**: если отправить 100 команд `r.incr(...)` подряд в цикле, сам Redis выполнит их за $0.1$ мс, но сеть потратит $100 \times 1\text{ мс} = 100\text{ мс}$ на ожидание каждого ответа! **`r.pipeline()`** упаковывает все 100 команд в один сетевой пакет и возвращает массив из 100 ответов за **1 сетевой поход**.
2. **Распределённая блокировка (Distributed Lock)**: чтобы только один воркер из 10 начал формировать тяжёлый отчёт, используется атомарная команда `r.set("lock:report", worker_id, nx=True, ex=30)` (флаг `NX` — *Not eXists*: записать ключ только если его ещё нет, и сразу поставить предохранительный TTL 30 секунд на случай падения воркера).

> **Junior vs Senior**:
> - **Junior**: Хранит профиль пользователя из 20 полей как единую JSON-строку в `String`, при каждом изменении одного счётчика скачивая строку в Python, парся `json.loads`, меняя поле и отправляя обратно (`GET` + `SET` — классическая гонка состояний!).
> - **Senior**: Использует структуру **`Hash`** (`HSET` / `HINCRBY`) для атомарного изменения отдельных полей объекта на стороне Redis, пакует массовые операции в `pipeline()` и строит лидерборды на **`ZSET`**.

---

## 4. Практикум в Python 3.13: структуры `String`, `Hash`, `List`, `Set`, `ZSET` и пакетный `pipeline()`

```python
import redis

r = redis.Redis()

# 1. Hash: храним сессию пользователя и атомарно обновляем только одно поле
r.hset("user:101", mapping={"name": "Alice", "role": "student"})
r.hset("user:101", "role", "senior_dev")
print("Профиль из Redis Hash (HGETALL):", r.hgetall("user:101"))

# 2. List + Set: очередь задач и уникальные теги
r.lpush("jobs:queue", "send_email", "build_pdf")
print("Задача из очереди (RPOP FIFO) :", r.rpop("jobs:queue"))
r.sadd("post:42:likes", "alice", "bob", "alice")  # Дубликат 'alice' игнорируется!
print("Уникальные лайки в Set        :", sorted(r.smembers("post:42:likes")))

# 3. Sorted Set (ZSET) + Pipeline: таблица лидеров за 1 сетевой пакет
pipe = r.pipeline()
pipe.zadd("leaderboard", {"Alice": 950, "Bob": 1200, "Charlie": 1100})
pipe.incr("stats:total_games")
pipe.execute()
print("Топ игроков из ZSET (ZRANGE)  :", r.zrange("leaderboard", 0, -1, desc=True, withscores=True))
```
''',

    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-153. Redis как кэш.md'): r'''📖 Перечитать конспект: Redis как кэш >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Математика нагрузки: как кэш спасает базу данных от гибели

> **Ментальная модель — «Дежурный стенд с ответами у входа против очереди в архив»**: В архиве (PostgreSQL) работают всего 20 архивариусов (пул соединений БД), и поиск одной папки на полках занимает $50\text{ мс}$. Если в здание одновременно зайдут 2 000 человек с одним и тем же вопросом «Какой сегодня курс валют?», очередь в архив растянется на улицу, и сервер упадёт по таймауту. Но если повесить ответ на **электронном табло у входа (Redis в RAM с откликом $0.2\text{ мс}$)**, 99% посетителей получат ответ мгновенно, даже не заходя в архив!

Посчитаем простую математику по **закону Литтла ($L = \lambda \times W$)**:
- Пусть сервис получает $\lambda = 1\,000\text{ RPS}$ (запросов в секунду), а тяжёлый SQL-запрос выполняется $W = 50\text{ мс} = 0.05\text{ с}$.
- Без кэша базе данных требуется одновременно держать открытыми $1\,000 \times 0.05 = 50$ активных соединений.
- Если мы добавим Redis с **Hit Rate = 95%**, то до PostgreSQL дойдёт только $5\%$ трафика ($50\text{ RPS}$), а нагрузка на пул соединений упадёт в **20 раз** (до 2.5 соединений)!

```text
Путь запроса при кэшировании (Cache Hit vs Cache Miss):
  [Клиент] ──1. Запрос──> [FastAPI / Django] ──2. GET product:42──> [Redis RAM (0.2 мс)]
                                 │
        ┌────────────────────────┴────────────────────────┐
        ▼ Если ключ НАЙДЕН (Cache Hit ~95%):              ▼ Если ключа НЕТ (Cache Miss ~5%):
  Мгновенный возврат JSON клиенту!                  3. SELECT ... FROM products WHERE id = 42 (PostgreSQL ~20 мс)
  (База данных даже не узнала о запросе!)           4. SET product:42 <json> EX 300 (Сохраняем в Redis на будущее)
                                                    5. Возврат ответа клиенту
```

---

## 2. Именование ключей (`Namespace:ID`) и политики вытеснения (`maxmemory-policy`)

Чтобы в Redis с миллионами ключей был идеальный порядок, ключи называют по иерархическому шаблону через двоеточие:
- `user:42:profile` — профиль пользователя №42;
- `catalog:category:5:page:1` — первая страница категории №5;
- `ratelimit:ip:192.168.1.1` — счётчик запросов с IP-адреса.

Что делает Redis, когда выделенная ему оперативная память (`maxmemory`, например `4 GB`) заполнилась до краёв? Поведение определяет настройка **`maxmemory-policy`**:

| Политика вытеснения (`Eviction Policy`) | Что удаляет при нехватке RAM? | Когда выбирать? |
| :--- | :--- | :--- |
| **`noeviction`** *(по умолчанию)* | Ничего не удаляет; на любую команду записи (`SET`) возвращает ошибку **`OOM command not allowed`**! | Только если Redis используется как основное хранилище/брокер, где нельзя терять ни одного ключа |
| **`allkeys-lru`** | Вытесняет **давно не использовавшиеся** (*Least Recently Used*) ключи среди всех ключей | ✅ **Лучший выбор для чистого кэша!** |
| **`allkeys-lfu`** | Вытесняет **наименее часто запрашиваемые** (*Least Frequently Used*) ключи | Когда важно удерживать самые популярные хиты каталога |
| **`volatile-lru` / `volatile-ttl`** | Удаляет только среди тех ключей, у которых **установлен TTL** (вечные ключи с `TTL = -1` не трогает!) | Когда в одном Redis живут и постоянные настройки/очереди, и временный кэш с TTL |

---

## 3. Что стоит кэшировать в Redis, а что — нет?

- **Отличные кандидаты для кэша**: результаты тяжёлых `JOIN`/агрегаций (главная страница, каталог товаров, курсы валют, права доступа пользователя), которые **читаются в 100 раз чаще, чем меняются**.
- **Плохие кандидаты**: уникальные одноразовые запросы (поиск по случайной строке), данные, которые меняются каждую миллисекунду и требуют 100% строгой консистентности (остаток денег на счёте при списании).

> **Junior vs Senior**:
> - **Junior**: Оставляет в Redis политику по умолчанию `noeviction` и складывает туда кэш без лимитов, из-за чего в пик распродажи при заполнении RAM весь сайт падает с ошибкой `OOM command not allowed`.
> - **Senior**: Для кэш-инстанса Redis настраивает `maxmemory` + политику вытеснения **`allkeys-lru`** (или `volatile-lru`), сериализует словари в компактный JSON и проектирует ключи с версионированным префиксом (`v1:product:42`).

---

## 4. Практикум в Python 3.13: декоратор кэширования медленного запроса к БД через Redis с TTL

```python
import json
import sqlite3
import redis

r = redis.Redis()
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT, price INTEGER)")
db.execute("INSERT INTO products VALUES (42, 'Монитор 4K OLED', 89900)")

db_queries_executed = 0

def get_product_cached(product_id: int) -> dict:
    global db_queries_executed
    cache_key = f"v1:product:{product_id}"

    # 1. Пытаемся прочитать из быстрого Redis (Cache Hit за O(1))
    cached_raw = r.get(cache_key)
    if cached_raw is not None:
        return {"source": "redis_cache", "data": json.loads(cached_raw)}

    # 2. При промахе (Cache Miss) идём в SQL-базу и прогреваем кэш с TTL = 300 сек
    db_queries_executed += 1
    row = db.execute("SELECT id, title, price FROM products WHERE id = ?", (product_id,)).fetchone()
    payload = {"id": row[0], "title": row[1], "price": row[2]}
    r.set(cache_key, json.dumps(payload), ex=300)
    return {"source": "sql_database", "data": payload}

print("Вызов #1 (холодный кэш -> Miss):", get_product_cached(42))
print("Вызов #2 (горячий кэш  -> Hit) :", get_product_cached(42))
print("Вызов #3 (горячий кэш  -> Hit) :", get_product_cached(42))
print(f"Итого обращений к SQL-базе за 3 вызова: {db_queries_executed} (экономия 66%!)")
```
''',

    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-154. Стратегии кэширования.md'): r'''📖 Перечитать конспект: Стратегии кэширования >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. Четыре архитектурных паттерна взаимодействия Приложения, Кэша и БД

> **Ментальная модель — «Блокнот секретаря и главный сейф»**: Когда в системе появляются два места хранения — быстрый блокнот на столе (Redis) и бронированный сейф в подвале (PostgreSQL) — нужно решить две задачи: **кто переписывает данные из сейфа в блокнот при чтении** и **в каком порядке обновлять сейф и блокнот при записи**? Ответы на эти два вопроса образуют 4 классических паттерна кэширования!

```text
1. CACHE-ASIDE (Ленивое чтение — 90% проектов):
   Чтение : Приложение само смотрит в Кэш -> при промахе само читает БД -> кладёт в Кэш.
   Запись : Приложение пишет напрямую в БД -> и УДАЛЯЕТ (`DEL`) старый ключ из Кэша!

2. WRITE-THROUGH (Синхронная сквозная запись):
   Запись : Приложение пишет одновременно и в БД, и в Кэш (кэш всегда свежий, но запись медленнее).

3. WRITE-BEHIND / WRITE-BACK (Отложенная асинхронная запись):
   Запись : Приложение мгновенно пишет ТОЛЬКО в быстрый Кэш (RAM), а фоновый воркер
            пачками (batch) сбрасывает изменения в БД раз в N секунд.
```

---

## 2. Сравнительная таблица стратегий кэширования

| Стратегия | Как работает Чтение / Запись | Главный плюс | Главный минус / риск |
| :--- | :--- | :--- | :--- |
| **`Cache-Aside` (Lazy Loading)** | Чтение: `Cache -> DB -> Cache`. Запись: `Update DB + Delete Cache` | В кэше хранятся **только реально запрашиваемые** данные; падение Redis не кладёт запись в БД | Первый запрос к новому ключу всегда медленный (*Cold Start / Cache Miss*) |
| **`Read-Through`** | Приложение всегда спрашивает только провайдер кэша, а кэш сам под капотом ходит в БД | Чистый код бизнес-логики (не знает про детали БД) | Требует поддержки плагина загрузки на стороне кэш-прокси |
| **`Write-Through`** | Запись синхронно обновляет и БД, и кэш | В кэше **никогда нет устаревших данных**, нет промаха при первом чтении | Замедляет каждую запись + забивает RAM данными, которые никто может больше не прочитать (*Cache Pollution*) |
| **`Write-Behind` (`Write-Back`)** | Запись идёт только в RAM (Redis), а в БД сбрасывается асинхронно батчами | ⚡ Колоссальная скорость записи (лайки, просмотры видео, координаты курьеров) | Если сервер Redis упадёт до сброса батча в PostgreSQL — данные за последние секунды **потеряются**! |

---

## 3. Тонкий вопрос с собеседования: почему при `Cache-Aside` на записи делают `DELETE` из кэша, а не `SET`?

Представьте, что при изменении цены товара вы решили не удалять ключ из кэша (`r.delete(key)`), а перезаписывать его (`r.set(key, new_val)`). Что произойдёт при двух параллельных запросах **Поток А** (ставит цену `100`) и **Поток Б** (ставит цену `200`)?
1. Поток А обновляет БД (`price = 100`).
2. Поток Б обновляет БД (`price = 200`).
3. Поток Б (быстрее по сети!) записывает в Redis `price = 200`.
4. Поток А (чуть задержался на планировщике ОС) записывает в Redis `price = 100`!
💥 **Катастрофа**: в базе данных лежит правильная цена `200`, а в кэше застряла старая цена `100` до истечения TTL!
А если оба потока при записи делают **`UPDATE DB` $\to$ `r.delete(key)`**, то следующий читатель просто прочитает из БД актуальное значение `200`!

> **Junior vs Senior**:
> - **Junior**: В паттерне `Cache-Aside` при обновлении записи в БД делает `r.set(key, new_data)` вместо `r.delete(key)` (ловя гонку параллельных писателей) или использует `Write-Behind` для финансовых транзакций.
> - **Senior**: Для 90% бизнес-сущностей использует **`Cache-Aside` с удалением ключа (`r.delete`) ПОСЛЕ коммита в БД**, а для лавины счётчиков (просмотры, лайки, телеметрия) применяет **`Write-Behind`** в связке с фоновым сбросом батчей.

---

## 4. Практикум в Python 3.13: реализация `Cache-Aside` и пакетного `Write-Behind` буфера

```python
import json
import sqlite3
import redis

r = redis.Redis()
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE articles (id INTEGER PRIMARY KEY, title TEXT, views INTEGER)")
conn.execute("INSERT INTO articles VALUES (1, 'Архитектура Redis', 100)")

# 1. Паттерн Cache-Aside: при обновлении БД инвалидируем кэш через DELETE!
def update_article_title_cache_aside(article_id: int, new_title: str) -> None:
    conn.execute("UPDATE articles SET title = ? WHERE id = ?", (new_title, article_id))
    conn.commit()
    r.delete(f"article:{article_id}")  # Удаляем ключ, чтобы избежать Race Condition при перезаписи!

# 2. Паттерн Write-Behind для высокочастотных счётчиков просмотров:
def record_view_write_behind(article_id: int) -> int:
    r.sadd("dirty_articles", str(article_id))
    return r.incr(f"article:{article_id}:views_delta")

def flush_views_to_db() -> int:
    flushed = 0
    for aid_str in list(r.smembers("dirty_articles")):
        delta = int(r.get(f"article:{aid_str}:views_delta") or 0)
        if delta > 0:
            conn.execute("UPDATE articles SET views = views + ? WHERE id = ?", (delta, int(aid_str)))
            r.delete(f"article:{aid_str}:views_delta")
            flushed += 1
    conn.commit()
    r.delete("dirty_articles")
    return flushed

for _ in range(5):
    record_view_write_behind(1)  # 5 мгновенных инкрементов в RAM без трогания диска БД!

flush_views_to_db()  # Фоновый сброс накопленной дельты одним UPDATE в SQL
print("Статья в БД после Write-Behind flush:", conn.execute("SELECT * FROM articles WHERE id = 1").fetchone())
```
''',

    os.path.join('Юнит 5.6 · NoSQL и кэш', '📚 Конспекты', 'К-155. Инвалидация кэша и метрики эффективности.md'): r'''📖 Перечитать конспект: Инвалидация кэша и метрики эффективности >> Конспект перечитан и усвоен. Оцените, насколько хорошо помните материал.

---

## 1. «В Computer Science есть две сложные проблемы: инвалидация кэша и именование»

> **Ментальная модель — «Замена ценников в супермаркете и защита от толпы на открытии»**: Кэш делает чтение молниеносным, но создаёт риск **Stale Data (устаревших данных)** — когда в кассовой базе цена уже изменилась, а на витрине в зале всё ещё висит старый ценник. Кроме того, если с витрины внезапно упал ценник на самый популярный товар по акции, 500 покупателей одновременно побегут спрашивать цену у единственного кассира (**Cache Stampede — эффект стада / собачьей свалки**)!

Три главные угрозы высоконагруженного кэша и способы защиты от них:

| Аномалия кэша | Суть проблемы | Инженерное решение (Senior) |
| :--- | :--- | :--- |
| **1. `Cache Stampede` (`Thundering Herd` / Dog-piling)** | Истёк TTL у «горячего» ключа (например, главная страница). В ту же миллисекунду **500 потоков** видят `Cache Miss` и **одновременно запускают один и тот же тяжёлый SQL-запрос**, убивая БД! | **Singleflight / Mutex Lock (`SET NX EX`)**: только 1 поток берёт блокировку и считает запрос в БД, пока остальные 499 ждут готового ответа из кэша (или **Early Recomputation** — фоновое обновление за 10 с до истечения TTL) |
| **2. `Cache Penetration` (Пробивание кэша)** | Хакер или баг запрашивает несуществующие ID (`/products/-999`, `/products/99999999`). В кэше их нет (`Miss`) $\implies$ каждый запрос бьёт сквозь кэш напрямую в БД! | **Negative Caching (Кэширование пустоты)**: сохранять в Redis маркер `"__NULL__"` с коротким TTL (`ex=60`) или ставить **Bloom Filter** перед кэшем |
| **3. `Cache Avalanche` (Лавина кэша)** | Тысячи ключей с одинаковым TTL истекают в одну и ту же секунду | **TTL Jitter**: добавлять к базовому TTL случайный разброс `±10%` |

---

## 2. Почему в продакшене категорически запрещена команда `KEYS *` и как работает `SCAN`?

Допустим, при обновлении каталога вам нужно сбросить все ключи по маске `catalog:page:*`.
Если выполнить команду **`r.keys('catalog:page:*')`** на продакшен-сервере Redis, где хранится $10\,000\,000$ ключей:
- Поскольку Redis **однопоточный**, команда `KEYS` заблокирует единственный поток выполнения на $O(N)$ (на несколько секунд)!
- В течение этих секунд **все остальные запросы** (авторизация, корзина, платежи) встанут в мёртвую очередь и отвалятся по таймауту!

Вместо `KEYS` в продакшене используют:
1. **Итератор с курсором `SCAN cursor MATCH pattern COUNT 100`** (в Python — `r.scan_iter(match='catalog:page:*')`): отдаёт ключи маленькими порциями, не блокируя Event Loop Redis; когда курсор вернулся равным **`0`**, обход завершён!
2. **Версионирование префикса (Cache Versioning / Epoch Key)**: вместо удаления 10 000 старых ключей мы просто делаем `r.incr('catalog:version')` (версия меняется с `v1` на `v2`), а новые запросы начинают читать ключи `v2:catalog:page:1`. Старые ключи `v1:*` спокойно вытеснятся сами по `allkeys-lru` или TTL за $O(1)$!

---

## 3. Главная метрика здоровья кэша: `Cache Hit Ratio` (Hit Rate)

Эффективность кэширования измеряется коэффициентом попаданий (**Hit Rate**):
$$\text{Hit Rate} = \frac{\text{Cache Hits}}{\text{Cache Hits} + \text{Cache Misses}} \times 100\%$$
- Для здорового кэша каталога, профилей и конфигураций целевой **Hit Rate составляет $90\% - 99\%$**.
- Если Hit Rate падает ниже $60\%$, значит либо TTL слишком короткий, либо ключи слишком уникальны (например, в ключ кэша случайно включили текущий `timestamp`), либо не хватает `maxmemory` и рабочие ключи постоянно вытесняются.

> **Junior vs Senior**:
> - **Junior**: Вызывает `r.keys('user:*')` на продакшене для инвалидации списков (вызывая микро-простой всего Redis) и не защищает кэш от запросов несуществующих ID (*Cache Penetration*).
> - **Senior**: Для массового сброса использует версионирование ключей (`v{ver}:catalog:...`) или неблокирующий `SCAN`, кэширует отсутствие записи (`Negative Caching` на 30–60 с) и защищает тяжёлые ключи от `Cache Stampede` через мьютекс `SET NX`.

---

## 4. Практикум в Python 3.13: `Negative Caching`, безопасный обход `SCAN` и расчёт `Hit Rate`

```python
import redis

r = redis.Redis()
db_data = {1: "Ноутбук Pro", 2: "Смартфон Ultra"}
hits, misses, db_calls = 0, 0, 0

def get_item_protected(item_id: int) -> str | None:
    """Кэш с защитой от Cache Penetration (Negative Caching для несуществующих ID)"""
    global hits, misses, db_calls
    key = f"item:{item_id}"
    cached = r.get(key)
    if cached is not None:
        hits += 1
        return None if cached == "__NULL__" else cached

    misses += 1
    db_calls += 1
    val = db_data.get(item_id)
    if val is None:
        # Кэшируем факт отсутствия строки на 60 сек, чтобы повторные запросы не били в БД!
        r.set(key, "__NULL__", ex=60)
        return None
    r.set(key, val, ex=600)
    return val

# 1. Запрашиваем существующий товар (id=1) и несуществующий товар (id=999) по 3 раза:
for _ in range(3):
    get_item_protected(1)
    get_item_protected(999)

hit_rate = (hits / (hits + misses)) * 100
print(f"Статистика кэша: Hits={hits}, Misses={misses}, Hit Rate={hit_rate:.1f}%, Походов в БД={db_calls}")

# 2. Неблокирующая инвалидация по маске через курсор SCAN (пока cursor != 0):
cursor = -1
deleted_keys = []
while cursor != 0:
    cursor, batch = r.scan(cursor=0 if cursor == -1 else cursor, match="item:*", count=10)
    if batch:
        r.delete(*batch)
        deleted_keys.extend(batch)
print("Безопасно очищены ключи через SCAN:", sorted(deleted_keys))
```
''',
}


def main() -> None:
    # 1. Перемещаем 7 колод Ф-* в их целевые юниты в Модуле 05
    moves = [
        (
            os.path.join(BASE_DB, 'Юнит 5.1 · SQL основы', '📇 Карточки', 'Ф-147. SQL Агрегатные функции COUNT, SUM, AVG, MIN,.md'),
            os.path.join(BASE_DB, 'Юнит 5.2 · SQL продвинутый', '📇 Карточки', 'Ф-147. SQL Агрегатные функции COUNT, SUM, AVG, MIN,.md'),
        ),
        (
            os.path.join(BASE_DB, 'Юнит 5.1 · SQL основы', '📇 Карточки', 'Ф-149. SQL UNION, UNION ALL.md'),
            os.path.join(BASE_DB, 'Юнит 5.2 · SQL продвинутый', '📇 Карточки', 'Ф-149. SQL UNION, UNION ALL.md'),
        ),
        (
            os.path.join(BASE_DB, 'Юнит 5.2 · SQL продвинутый', '📇 Карточки', 'Ф-160. Оптимизация XPLAIN EXPLAIN ANALYZE.md'),
            os.path.join(BASE_DB, 'Юнит 5.4 · Транзакции', '📇 Карточки', 'Ф-160. Оптимизация XPLAIN EXPLAIN ANALYZE.md'),
        ),
        (
            os.path.join(BASE_DB, 'Юнит 5.4 · Транзакции', '📇 Карточки', 'Ф-111. Оптимизация N+1 проблема.md'),
            os.path.join(BASE_DB, 'Юнит 5.5 · ORM и миграции', '📇 Карточки', 'Ф-111. Оптимизация N+1 проблема.md'),
        ),
        (
            os.path.join(BASE_DB, 'Юнит 5.1 · SQL основы', '📇 Карточки', 'Ф-161. PostgreSQL Специфика.md'),
            os.path.join(BASE_DB, 'Юнит 5.5 · ORM и миграции', '📇 Карточки', 'Ф-161. PostgreSQL Специфика.md'),
        ),
        (
            os.path.join(BASE_DB, 'Юнит 5.1 · SQL основы', '📇 Карточки', 'Ф-164. PostgreSQL Базовые отличия от MySQL.md'),
            os.path.join(BASE_DB, 'Юнит 5.5 · ORM и миграции', '📇 Карточки', 'Ф-164. PostgreSQL Базовые отличия от MySQL.md'),
        ),
        (
            os.path.join(BASE_DB, 'Юнит 5.1 · SQL основы', '📇 Карточки', 'Ф-165. NoSQL MongoDB базово, когда использовать.md'),
            os.path.join(BASE_DB, 'Юнит 5.6 · NoSQL и кэш', '📇 Карточки', 'Ф-165. NoSQL MongoDB базово, когда использовать.md'),
        ),
    ]
    for src, dst in moves:
        if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
            print(f"Перемещена колода: {os.path.basename(src)} -> {os.path.relpath(dst, BASE_DB)}")

    # 2. Обогащаем односложные/односимвольные ответы в карточках Ф-143, Ф-147, Ф-150, Ф-168
    card_patches = {
        os.path.join(BASE_DB, 'Юнит 5.1 · SQL основы', '📇 Карточки', 'Ф-143. SQL SELECT, WHERE, ORDER BY, LIMIT.md'): [
            (
                "24. Если в `LIMIT` указано 10, сколько строк максимум вернёт запрос? >> 10",
                "24. Если в `LIMIT` указано 10, сколько строк максимум вернёт запрос? >> `10` (или меньше, если в выборке всего меньше 10 строк)",
            ),
        ],
        os.path.join(BASE_DB, 'Юнит 5.2 · SQL продвинутый', '📇 Карточки', 'Ф-147. SQL Агрегатные функции COUNT, SUM, AVG, MIN,.md'): [
            (
                "1. Функция `COUNT(*)` возвращает количество строк в группе включая строки с `NULL` – верно? >> Да",
                "1. Функция `COUNT(*)` возвращает количество строк в группе включая строки с `NULL` – верно? >> Да (`COUNT(*)` считает все физические строки, тогда как `COUNT(col)` игнорирует `NULL`)",
            ),
            (
                "29. Если в таблице 5 строк и во всех `salary = NULL` , что вернёт `COUNT(*)` ? >> 5",
                "29. Если в таблице 5 строк и во всех `salary = NULL` , что вернёт `COUNT(*)` ? >> `5` (так как `COUNT(*)` считает общее число строк независимо от `NULL`)",
            ),
            (
                "35. Если в таблице 5 строк и во всех `salary = NULL` , что вернёт `COUNT(salary)` ? >> 0",
                "35. Если в таблице 5 строк и во всех `salary = NULL` , что вернёт `COUNT(salary)` ? >> `0` (так как `COUNT(column)` считает только строки, где значение `IS NOT NULL`)",
            ),
        ],
        os.path.join(BASE_DB, 'Юнит 5.2 · SQL продвинутый', '📇 Карточки', 'Ф-150. SQL Оконные функции ROW_NUMBER, RANK, PARTITI.md'): [
            (
                "3. Список зарплат `(100, 100, 50)` – что вернёт `DENSE_RANK()` для значения 50? >> 2",
                "3. Список зарплат `(100, 100, 50)` – что вернёт `DENSE_RANK()` для значения 50? >> `2` (`DENSE_RANK` не пропускает ранги после ничьей: `1, 1, 2`)",
            ),
            (
                "16. Если двум строкам присвоен ранг 2 функцией `DENSE_RANK()` , какой ранг получит следующая строка? >> 3",
                "16. Если двум строкам присвоен ранг 2 функцией `DENSE_RANK()` , какой ранг получит следующая строка? >> `3` (`DENSE_RANK` нумерует плотно без пропусков)",
            ),
            (
                "20. Если двум строкам присвоен ранг 2 функцией `RANK()` , какой ранг получит следующая строка? >> 4",
                "20. Если двум строкам присвоен ранг 2 функцией `RANK()` , какой ранг получит следующая строка? >> `4` (`RANK` пропускает 3-е место после двух строк на 2-м месте)",
            ),
            (
                "24. Список зарплат `(100, 100, 50)` – что вернёт `RANK()` для значения 50? >> 3",
                "24. Список зарплат `(100, 100, 50)` – что вернёт `RANK()` для значения 50? >> `3` (после двух первых мест `1, 1` второе место пропускается)",
            ),
            (
                "44. `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC)` – что получит самый высокооплачиваемый в отделе? >> 1",
                "44. `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC)` – что получит самый высокооплачиваемый в отделе? >> `1` (первый номер в своём окне `dept` при сортировке по убыванию зарплаты)",
            ),
        ],
        os.path.join(BASE_DB, 'Юнит 5.6 · NoSQL и кэш', '📇 Карточки', 'Ф-168. Кэширование TTL.md'): [
            (
                "7. Если `r.ttl('key')` вернул `-2` , существует ли ключ? >> Нет",
                "7. Если `r.ttl('key')` вернул `-2` , существует ли ключ? >> Нет (`-2` означает, что ключа не существует или он уже истёк; `-1` означает ключ без TTL)",
            ),
        ],
    }
    for fpath, replacements in card_patches.items():
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                txt = f.read()
            changed = False
            for old_s, new_s in replacements:
                if new_s not in txt and old_s in txt:
                    txt = txt.replace(old_s, new_s)
                    changed = True
            if changed:
                with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(txt)
                print(f"Обогащены краткие ответы в колоде: {os.path.basename(fpath)}")

    # 3. Записываем все 32 обогащённых конспекта К-124..К-155
    updated = 0
    for rel_path, content in NOTES_CONTENT.items():
        full_path = os.path.join(BASE_DB, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content.strip() + '\n')
        updated += 1

    # 4. Синхронизируем пути в 00 · 🗺️ Карта Мастерства.md и подключаем Ф-110, Ф-111 к Навыку 5.5.1
    karta_path = os.path.join(os.path.dirname(BASE_DB), '00 · 🗺️ Карта Мастерства.md')
    if os.path.exists(karta_path):
        with open(karta_path, 'r', encoding='utf-8') as f:
            karta_txt = f.read()
        karta_new = (
            karta_txt.replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.1 · SQL основы/📇 Карточки/Ф-147. SQL Агрегатные функции COUNT, SUM, AVG, MIN,]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.2 · SQL продвинутый/📇 Карточки/Ф-147. SQL Агрегатные функции COUNT, SUM, AVG, MIN,]]',
            )
            .replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.1 · SQL основы/📇 Карточки/Ф-149. SQL UNION, UNION ALL]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.2 · SQL продвинутый/📇 Карточки/Ф-149. SQL UNION, UNION ALL]]',
            )
            .replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.2 · SQL продвинутый/📇 Карточки/Ф-160. Оптимизация XPLAIN EXPLAIN ANALYZE]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.4 · Транзакции/📇 Карточки/Ф-160. Оптимизация XPLAIN EXPLAIN ANALYZE]]',
            )
            .replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.4 · Транзакции/📇 Карточки/Ф-111. Оптимизация N+1 проблема]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-111. Оптимизация N+1 проблема]]',
            )
            .replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.1 · SQL основы/📇 Карточки/Ф-161. PostgreSQL Специфика]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-161. PostgreSQL Специфика]]',
            )
            .replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.1 · SQL основы/📇 Карточки/Ф-164. PostgreSQL Базовые отличия от MySQL]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-164. PostgreSQL Базовые отличия от MySQL]]',
            )
            .replace(
                '[[05 · 🗄️ Базы данных/Юнит 5.1 · SQL основы/📇 Карточки/Ф-165. NoSQL MongoDB базово, когда использовать]]',
                '[[05 · 🗄️ Базы данных/Юнит 5.6 · NoSQL и кэш/📇 Карточки/Ф-165. NoSQL MongoDB базово, когда использовать]]',
            )
        )
        # Привязываем Ф-110 и Ф-111 к Skill 5.5.1, если их там ещё нет:
        old_551_cards = (
            "  - 📇 **Карточки RemNote**:\n"
            "    - [[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-162. ORM SQLAlchemy модели, сессии, запросы]]\n"
            "    - [[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-163. ORM Миграции]]\n"
            "  - 💻 **Практика кодинга**: Воспроизвести проблему N+1"
        )
        new_551_cards = (
            "  - 📇 **Карточки RemNote**:\n"
            "    - [[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-110. ORM Django ORM, модели QuerySet, related_name]]\n"
            "    - [[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-111. Оптимизация N+1 проблема]]\n"
            "    - [[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-162. ORM SQLAlchemy модели, сессии, запросы]]\n"
            "    - [[05 · 🗄️ Базы данных/Юнит 5.5 · ORM и миграции/📇 Карточки/Ф-163. ORM Миграции]]\n"
            "  - 💻 **Практика кодинга**: Воспроизвести проблему N+1"
        )
        if old_551_cards in karta_new:
            karta_new = karta_new.replace(old_551_cards, new_551_cards, 1)
        if karta_new != karta_txt:
            with open(karta_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(karta_new)
            print("Синхронизированы пути колод Модуля 05 в 00 · 🗺️ Карта Мастерства.md")

    print(f"Обогащено конспектов Модуля 05 (К-124..К-155): {updated}")


if __name__ == '__main__':
    main()
