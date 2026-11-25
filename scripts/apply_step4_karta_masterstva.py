# -*- coding: utf-8 -*-
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

def apply_step4():
    print("=== STEP 4: SYNCHRONIZING КАРТА МАСТЕРСТВА (20 UNITS ECHELON 1) ===")
    
    karta_path = os.path.join(_ROOT, 'knowledge_base', '00 · 🗺️ Карта Мастерства.md')
    with open(karta_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Section 2.2 description
    old_ech_block = r'''2. **🚨 Эшелон 1 · Скрининг и база (Первая очередь — 14 юнитов, 43 навыка)**:
   - То, без чего не пройти первичное тех-интервью и лайвкодинг:
   - `01 · 🐍 Python`: Юниты `1.1` (Коллекции и срезы), `1.2` (Функции и замыкания), `1.3` (Исключения, генераторы, `with`), `1.4` (ООП: классы и наследование), `1.9` (Модули, `venv`, `logging`, `pytest`).
   - `02 · 🌐 Web`: Юниты `2.2` (HTTP/1.1–3, методы, статус-коды, TLS), `2.3` (REST API, JSON, пагинация, идемпотентность).
   - `04 · ⚡ Алгоритмы`: Юниты `4.1` (Big-O), `4.2` (Массивы, два указателя, скользящее окно), `4.4` (Хэш-таблицы, устройство `dict` и `set`).
   - `05 · 🗄️ Базы данных`: Юниты `5.1` (Реляционная модель, 1NF–3NF), `5.2` (`SELECT`, `WHERE`, `GROUP BY`, `HAVING`), `5.3` (`JOIN`, подзапросы, CTE, оконные функции).
   - `07 · 🚀 Инфраструктура`: Юнит `7.1` (Git, ветки, `merge` vs `rebase`, Pull Request).
3. **🔥 Эшелон 2 · Тех-ядро и параллельные ветви стека (Вторая очередь — 17 юнитов, 44 навыка)**:
   - Углублённый Python (`1.5` dunder/`@property`/`dataclass`, `1.6` `typing`/Generics, `1.7` Память и GC, `1.8` GIL/потоки/`asyncio`), сети и безопасность (`2.1` TCP/IP и DNS, `2.4` CORS/CSRF/XSS/SQLi), транзакции и индексы БД (`5.4` ACID, изоляция, MVCC, B-Tree, `EXPLAIN`), основы Docker и тестирования (`7.2`, `7.6`), аутентификация и слоистая архитектура (`3.5` JWT/OAuth2/RBAC/BOLA, `3.6` Service/Repository/UoW) + **выбор главной ударной ветки стека**:'''

    new_ech_block = r'''2. **🚨 Эшелон 1 · BigTech-скрининг · Железный фундамент (Первая очередь — 20 юнитов, 55 навыков)**:
   - Первичный бескомпромиссный отбор BigTech (Яндекс, Авито, Т-Банк, Ozon):
   - `01 · 🐍 Python Core`: Юниты `1.1` (Коллекции и срезы), `1.2` (Функции и замыкания), `1.3` (Исключения, генераторы, `with`), `1.4` (ООП: классы и наследование), `1.8` (Конкурентность: GIL, Event Loop, threading vs asyncio), `1.9` (Модули, `venv`, `logging`, `pytest`).
   - `02 · 🌐 Web & HTTP`: Юниты `2.1` (Сетевой фундамент: TCP/IP, DNS, сокеты), `2.2` (HTTP/1.1–3, методы, статус-коды, TLS), `2.3` (REST API, JSON, пагинация, идемпотентность), `2.4` (Веб-безопасность: CORS, CSRF, XSS, SQLi).
   - `04 · ⚡ Алгоритмы`: Юниты `4.1` (Big-O), `4.2` (Массивы, два указателя, скользящее окно), `4.3` (Стек, очередь FIFO/LIFO, deque), `4.4` (Хэш-таблицы, устройство `dict` и `set`), `4.6` (Бинарный поиск, рекурсия, базовые сортировки).
   - `05 · 🗄️ Базы данных`: Юниты `5.1` (Реляционная модель, 1NF–3NF), `5.2` (`SELECT`, `WHERE`, `GROUP BY`, `HAVING`), `5.3` (`JOIN`, подзапросы, CTE, оконные функции), `5.4` (Транзакции: ACID, уровни изоляции, B-Tree индексы).
   - `07 · 🚀 Инфраструктура`: Юнит `7.1` (Git, ветки, `merge` vs `rebase`, Pull Request).
3. **🔥 Эшелон 2 · Тех-ядро и параллельные ветви стека (Вторая очередь — 11 юнитов, 33 навыка)**:
   - Углублённый Python (`1.5` dunder/`@property`/`dataclass`, `1.6` `typing`/Generics, `1.7` Память и GC), основы контейнеризации и CI (`7.2` Docker основы, `7.6` очереди и логирование), аутентификация и слоистая архитектура (`3.5` JWT/OAuth2/RBAC/BOLA, `3.6` Service/Repository/UoW) + **выбор главной ударной ветки стека**:'''

    if old_ech_block in content:
        content = content.replace(old_ech_block, new_ech_block, 1)
        print("1. Updated Echelon overview section in Карта Мастерства")
    else:
        print("WARNING: Old echelon overview block not matched exactly, trying regex...")
        # fallback with regex
        content = re.sub(
            r'2\.\s+\*\*🚨 Эшелон 1.*?(?=4\.\s+\*\*⚡ Эшелон 3)',
            new_ech_block + "\n",
            content,
            flags=re.DOTALL
        )

    # 2. Update unit headers for the 6 promoted units
    promoted_replacements = {
        r'(### 📘 Юнит 1.8 · Конкурентность\s*\n\s*- 🎯 \*\*Эшелон собеседования\*\*: )[^\n]+':
            r'\1🚨 Эшелон 1 · Скрининг и база (BigTech-скрининг · Многопоточность и Event Loop)',
        r'(### 📘 Юнит 2.1 · Сетевой фундамент\s*\n\s*- 🎯 \*\*Эшелон собеседования\*\*: )[^\n]+':
            r'\1🚨 Эшелон 1 · Скрининг и база (BigTech-скрининг · Сетевой фундамент)',
        r'(### 📘 Юнит 2.4 · Веб-безопасность\s*\n\s*- 🎯 \*\*Эшелон собеседования\*\*: )[^\n]+':
            r'\1🚨 Эшелон 1 · Скрининг и база (BigTech-скрининг · Веб-безопасность)',
        r'(### 📘 Юнит 4.3 · Списки стек очередь\s*\n\s*- 🎯 \*\*Эшелон собеседования\*\*: )[^\n]+':
            r'\1🚨 Эшелон 1 · Скрининг и база (BigTech-скрининг · Стек и очередь)',
        r'(### 📘 Юнит 4.6 · Поиск сортировки DP\s*\n\s*- 🎯 \*\*Эшелон собеседования\*\*: )[^\n]+':
            r'\1🚨 Эшелон 1 · Скрининг и база (BigTech-скрининг · Бинарный поиск и сортировки)',
        r'(### 📘 Юнит 5.4 · Транзакции\s*\n\s*- 🎯 \*\*Эшелон собеседования\*\*: )[^\n]+':
            r'\1🚨 Эшелон 1 · Скрининг и база (BigTech-скрининг · ACID и транзакции)',
    }

    headers_patched = 0
    for pat, repl in promoted_replacements.items():
        if re.search(pat, content):
            content = re.sub(pat, repl, content, count=1)
            headers_patched += 1

    print(f"2. Updated {headers_patched} unit headers to Echelon 1")

    with open(karta_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("3. Successfully saved 00 · 🗺️ Карта Мастерства.md")

if __name__ == '__main__':
    apply_step4()
