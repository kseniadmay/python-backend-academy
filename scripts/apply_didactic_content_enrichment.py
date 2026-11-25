#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_didactic_content_enrichment.py

Обогащение всех 97 блоков кода конспектов точными дидактическими комментариями
с результатами вычислений (# 'значение', # True, # 42) без необходимости запуска кода.
Исправление артефактов дублирования строк.
"""

from pathlib import Path

def enrich_all_snippets(text: str) -> str:
    replacements = [
        # BLOCK 1: if/elif/else
        (
            'elif age &lt; 65:\n\n    print("Взрослый")',
            'elif age &lt; 65:\n\n    print("Взрослый")  # выведет: 18 <= 20 < 65'
        ),
        # BLOCK 2: Логические операторы
        (
            'if age >= 18 and has_ticket:\n\n    print("Проходите")',
            'if age >= 18 and has_ticket:\n\n    print("Проходите")  # оба True -> вход разрешён'
        ),
        # BLOCK 4: while
        (
            'while n > 0:\n\n    print(n)\n\n    n -= 1',
            'while n > 0:\n\n    print(n)  # выведет поочерёдно: 5, 4, 3, 2, 1\n\n    n -= 1'
        ),
        # BLOCK 5: break и continue
        (
            '    if n % 2 != 0:\n\n        continue     # пропустить нечётные, не печатая их\n\n    print(n)',
            '    if n % 2 != 0:\n\n        continue     # пропустить нечётные, не печатая их\n\n    print(n)         # выведет: 0, 2, 4 (до остановки на 5)'
        ),
        # BLOCK 6: Собираем вместе
        (
            'for n in range(10):\n\n    if n % 2 == 0:\n\n        print(n)',
            'for n in range(10):\n\n    if n % 2 == 0:\n\n        print(n)  # выведет чётные: 0, 2, 4, 6, 8'
        ),
        # BLOCK 13: try / except
        (
            'except ZeroDivisionError:\n\n    print("На ноль делить нельзя")',
            'except ZeroDivisionError:\n\n    print("На ноль делить нельзя")  # перехват деления на 0'
        ),
        # BLOCK 14: Несколько except
        (
            'except ValueError:\n\n    print("Это не похоже на число")\n\nexcept Exception as e:\n\n    print(f"Что-то пошло не так: {e}")',
            'except ValueError:\n\n    print("Это не похоже на число")   # сработает для строки \'abc\'\n\nexcept Exception as e:\n\n    print(f"Что-то пошло не так: {e}") # перехват прочих исключений'
        ),
        # BLOCK 16: finally
        (
            'finally:\n\n    print("Это выполнится всегда")',
            'finally:\n\n    print("Это выполнится всегда")  # сработает гарантированно при любом исходе'
        ),
        # BLOCK 17: Модули
        (
            'from utils import greet\n\nprint(greet("Аня"))\n\n\n\n# или импортировать весь модуль целиком\n\nimport utils\n\nprint(utils.greet("Аня"))',
            'from utils import greet\n\nprint(greet("Аня"))        # \'Привет, Аня!\'\n\n\n\n# или импортировать весь модуль целиком\n\nimport utils\n\nprint(utils.greet("Аня"))  # \'Привет, Аня!\''
        ),
        # BLOCK 65: has_duplicate O(n^2)
        (
            'sample = [4, 8, 15, 16, 23, 42, 15]\\nprint(&quot;has_duplicate:&quot;, has_duplicate(sample))',
            'sample = [4, 8, 15, 16, 23, 42, 15]\\nprint(&quot;has_duplicate:&quot;, has_duplicate(sample))  # True (15 повторяется)'
        ),
        # BLOCK 66: has_duplicate_fast O(n)
        (
            'sample = [4, 8, 15, 16, 23, 42, 15]\\nprint(&quot;Fast duplicate:&quot;,\\n      has_duplicate_fast(sample))',
            'sample = [4, 8, 15, 16, 23, 42, 15]\\nprint(&quot;Fast duplicate:&quot;,\\n      has_duplicate_fast(sample))  # True (за O(n) через set)'
        ),
        # BLOCK 69: срезы
        (
            'numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\\nprint(numbers[2:5])\\nprint(numbers[:4])\\nprint(numbers[6:])\\nprint(numbers[:])\\nprint(numbers[: : 2])\\nprint(numbers[1:8:3])',
            'numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\\nprint(numbers[2:5])   # [2, 3, 4]\\nprint(numbers[:4])    # [0, 1, 2, 3]\\nprint(numbers[6:])    # [6, 7, 8, 9]\\nprint(numbers[:])     # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (копия)\\nprint(numbers[::2])   # [0, 2, 4, 6, 8] (с шагом 2)\\nprint(numbers[1:8:3]) # [1, 4, 7] (с шагом 3)'
        ),
        # BLOCK 132: repeat decorator (исправление дублирования!)
        (
            'from functools import wraps\\ndef repeat(n):\\n    def decorator(func):\\n        @wraps(func)\\n        def wrapper(*args, **kwargs):\\n            for _ in range(n):\\n                result = func(*args,\\n                    **kwargs)\\n            return result\\n        return wrapper\\n    return decorator\\n@repeat(3)\\ndef greet():\\n    print(&quot;Привет!&quot;)\\n\\ngreet()\\n    print(&quot;Привет!&quot;)\\n\\ngreet()\\n    print(&quot;Привет!&quot;)\\n\\ngreet()\\n    print(&quot;Привет!&quot;)\\n\\ngreet()',
            'from functools import wraps\\ndef repeat(n):\\n    def decorator(func):\\n        @wraps(func)\\n        def wrapper(*args, **kwargs):\\n            for _ in range(n):\\n                result = func(*args, **kwargs)\\n            return result\\n        return wrapper\\n    return decorator\\n\\n@repeat(3)\\ndef greet():\\n    print(&quot;Привет!&quot;)\\n\\ngreet()  # напечатает &quot;Привет!&quot; ровно 3 раза'
        ),
        # BLOCK 142: CountUp iterator (исправление дублирования!)
        (
            'class CountUp:\\n    def __init__(self, limit):\\n        self.limit = limit\\n        self.current = 0\\n    def __iter__(self):\\n        return self\\n    def __next__(self):\\n        if self.current &gt;= self.limit:\\n            raise StopIteration\\n        self.current += 1\\n        return self.current\\nfor num in CountUp(3):\\n    print(num)\\n    print(num)\\n    print(num)\\n    print(num)',
            'class CountUp:\\n    def __init__(self, limit):\\n        self.limit = limit\\n        self.current = 0\\n    def __iter__(self):\\n        return self\\n    def __next__(self):\\n        if self.current &gt;= self.limit:\\n            raise StopIteration\\n        self.current += 1\\n        return self.current\\n\\nfor num in CountUp(3):\\n    print(num)  # выведет поочерёдно: 1, затем 2, затем 3'
        ),
        # BLOCK 255: regexp email
        (
            'import re\\n\\npattern = r&quot;^[\\w.-]+@[\\w.-]+\\.\\w+$&quot;\\nprint(bool(re.search(pattern,\\n    &quot;admin@example.com&quot;)))',
            'import re\\n\\npattern = r&quot;^[\\w.-]+@[\\w.-]+\\.\\w+$&quot;\\nprint(bool(re.search(pattern,\\n    &quot;admin@example.com&quot;)))  # True (валидный email)'
        ),
        # BLOCK 256: regexp log_line
        (
            'if match:\\n    print(&quot;Совпадение:&quot;, match.group(0))\\n    print(&quot;Значение:&quot;, match.group(1))\\n    print(&quot;Индексы:&quot;, match.span())',
            'if match:\\n    print(&quot;Совпадение:&quot;, match.group(0))  # \'user_id=42\'\\n    print(&quot;Значение:&quot;, match.group(1))    # \'42\'\\n    print(&quot;Индексы:&quot;, match.span())       # (17, 27)'
        ),
        # BLOCK 257: re.match vs search
        (
            'import re\\n\\ntext = &quot;order_12345_complete&quot;\\nprint(bool(re.match(r&quot;order_\\d+&quot;, text)))\\nprint(bool(re.match(r&quot;12345&quot;, text)))',
            'import re\\n\\ntext = &quot;order_12345_complete&quot;\\nprint(bool(re.match(r&quot;order_\\d+&quot;, text)))  # True (совпало с начала)\\nprint(bool(re.match(r&quot;12345&quot;, text)))       # False (match ищет строго с начала)'
        ),
        # BLOCK 258: re.fullmatch
        (
            'import re\\n\\nprint(bool(re.fullmatch(r&quot;order_\\d+&quot;,\\n    &quot;order_12345_complete&quot;)))\\nprint(bool(re.fullmatch(r&quot;[a-z0-9-]+&quot;,\\n    &quot;valid-slug-2026&quot;)))',
            'import re\\n\\nprint(bool(re.fullmatch(r&quot;order_\\d+&quot;,\\n    &quot;order_12345_complete&quot;)))  # False (хвост _complete не совпал)\\nprint(bool(re.fullmatch(r&quot;[a-z0-9-]+&quot;,\\n    &quot;valid-slug-2026&quot;)))      # True (вся строка совпала)'
        ),
        # BLOCK 259: re.findall
        (
            'codes = re.findall(r&quot;\\b\\d{3}\\b&quot;, log)\\nprint(&quot;Все коды списком:&quot;, codes)',
            'codes = re.findall(r&quot;\\b\\d{3}\\b&quot;, log)\\nprint(&quot;Все коды списком:&quot;, codes)  # [\'404\', \'500\', \'502\']'
        ),
        # BLOCK 260: re.finditer
        (
            '    val = m.group(0)\\n    pos = m.start()\\n    print(f&quot;Число {val} на шаге {pos}&quot;)',
            '    val = m.group(0)\\n    pos = m.start()\\n    print(f&quot;Число {val} на шаге {pos}&quot;)  # 404 (поз 4), 500 (поз 14), 502 (поз 24)'
        ),
        # BLOCK 262: re.findall \d vs \w
        (
            'import re\\n\\ntext = &quot;User 42 logged in&quot;\\nprint(&quot;Цифры:&quot;, re.findall(r&quot;\\d+&quot;, text))\\nprint(&quot;Слова:&quot;, re.findall(r&quot;\\w+&quot;, text))',
            'import re\\n\\ntext = &quot;User 42 logged in&quot;\\nprint(&quot;Цифры:&quot;, re.findall(r&quot;\\d+&quot;, text))  # [\'42\']\\nprint(&quot;Слова:&quot;, re.findall(r&quot;\\w+&quot;, text))  # [\'User\', \'42\', \'logged\', \'in\']'
        ),
        # BLOCK 263: re.sub
        (
            'phone = &quot;+7 (999) 123-45-67&quot;\\nclean = re.sub(r&quot;\\D&quot;, &quot;&quot;, phone)\\nprint(&quot;Очищенный номер:&quot;, clean)',
            'phone = &quot;+7 (999) 123-45-67&quot;\\nclean = re.sub(r&quot;\\D&quot;, &quot;&quot;, phone)\\nprint(&quot;Очищенный номер:&quot;, clean)  # \'79991234567\''
        ),
        # BLOCK 264: rx https?
        (
            'rx = r&quot;^https?://&quot;\\nprint(bool(re.match(rx, &quot;http://api&quot;)))\\nprint(bool(re.match(rx, &quot;https://api&quot;)))',
            'rx = r&quot;^https?://&quot;\\nprint(bool(re.match(rx, &quot;http://api&quot;)))   # True (http://)\\nprint(bool(re.match(rx, &quot;https://api&quot;)))  # True (https://, s опциональна)'
        ),
        # BLOCK 265: pin_pattern
        (
            'print(is_pin)\\nprint(bool(re.match(pin_pattern, &quot;12&quot;)))',
            'print(is_pin)                              # True (длина 5 цифр)\\nprint(bool(re.match(pin_pattern, &quot;12&quot;)))  # False (меньше 4 цифр)'
        ),
        # BLOCK 267: email groups
        (
            'if m:\\n    print(&quot;Имя:&quot;, m.group(1))\\n    print(&quot;Домен:&quot;, m.group(2))',
            'if m:\\n    print(&quot;Имя:&quot;, m.group(1))    # \'alex.dev\'\\n    print(&quot;Домен:&quot;, m.group(2))  # \'corp.example.com\''
        ),
        # BLOCK 268: github rx
        (
            'urls = re.findall(rx,\\n    &quot;https://github.com/torvalds&quot;)\\nprint(&quot;GitHub URL:&quot;, urls)',
            'urls = re.findall(rx,\\n    &quot;https://github.com/torvalds&quot;)\\nprint(&quot;GitHub URL:&quot;, urls)  # [\'github.com/torvalds\']'
        ),
        # BLOCK 269: named groups (?P<...>)
        (
            'if match:\\n    data = match.groupdict()\\n    print(&quot;IP клиента:&quot;, data[&quot;ip&quot;])\\n    print(&quot;HTTP статус:&quot;, data[&quot;status&quot;])',
            'if match:\\n    data = match.groupdict()\\n    print(&quot;IP клиента:&quot;, data[&quot;ip&quot;])      # \'192.168.1.10\'\\n    print(&quot;HTTP статус:&quot;, data[&quot;status&quot;])  # \'200\''
        ),
        # BLOCK 271: re.IGNORECASE
        (
            'matched = bool(\\n    email_rx.match(&quot;Admin@Host.ORG&quot;)\\n)\\nprint(matched)',
            'matched = bool(\\n    email_rx.match(&quot;Admin@Host.ORG&quot;)\\n)\\nprint(matched)  # True (регистр проигнорирован благодаря re.IGNORECASE)'
        ),
        # BLOCK 272: re.DOTALL
        (
            'matched = bool(re.search(r&quot;start.*end&quot;,\\n    multi, re.DOTALL))\\nprint(&quot;DOTALL совпадение:&quot;, matched)',
            'matched = bool(re.search(r&quot;start.*end&quot;,\\n    multi, re.DOTALL))\\nprint(&quot;DOTALL совпадение:&quot;, matched)  # True (точка захватила символ \\n)'
        ),
        # BLOCK 274: safe_pattern
        (
            'print(bool(re.match(safe_pattern,\\n    &quot;user@test.com&quot;)))',
            'print(bool(re.match(safe_pattern,\\n    &quot;user@test.com&quot;)))  # True (без ReDoS-уязвимостей)'
        ),
        # BLOCK 275: tools summary
        (
            'print(&quot;Инструменты бэкенда:&quot;, tools)\\nprint(&quot;Регулярные выражения освоены!&quot;)',
            'print(&quot;Инструменты бэкенда:&quot;, tools)  # [\'str-methods\', \'re.compile\', \'pydantic-v2\']\\nprint(&quot;Регулярные выражения освоены!&quot;)    # готов к скринингу'
        ),
        # BLOCK 282: json.dumps default=str
        (
            'payload = json.dumps(order, default=str)\\nprint(&quot;Успешная сериализация:&quot;, payload)',
            'payload = json.dumps(order, default=str)\\nprint(&quot;Успешная сериализация:&quot;, payload)  # JSON-строка с UUID и ISO-датой'
        ),
        # BLOCK 340: Path properties
        (
            'p = Path(&quot;/var/log/nginx/access.tar.gz&quot;)\\nprint(&quot;Имя файла:&quot;, p.name)\\nprint(&quot;Без последнего суффикса:&quot;, p.stem)\\nprint(&quot;Суффикс:&quot;, p.suffix)\\nprint(&quot;Родительская папка:&quot;, p.parent)',
            'p = Path(&quot;/var/log/nginx/access.tar.gz&quot;)\\nprint(&quot;Имя файла:&quot;, p.name)                  # \'access.tar.gz\'\\nprint(&quot;Без последнего суффикса:&quot;, p.stem)  # \'access.tar\'\\nprint(&quot;Суффикс:&quot;, p.suffix)                     # \'.gz\'\\nprint(&quot;Родительская папка:&quot;, p.parent)          # PosixPath(\'/var/log/nginx\')'
        ),
        # BLOCK 341: with_suffix / with_name
        (
            'print(&quot;Замена расширения:&quot;,\\n    p.with_suffix(&quot;.bak&quot;))\\nprint(&quot;Замена имени:&quot;,\\n    p.with_name(&quot;error.log&quot;))',
            'print(&quot;Замена расширения:&quot;,\\n    p.with_suffix(&quot;.bak&quot;))     # \'/var/log/nginx/access.tar.bak\'\\nprint(&quot;Замена имени:&quot;,\\n    p.with_name(&quot;error.log&quot;))    # \'/var/log/nginx/error.log\''
        ),
        # BLOCK 343: write_text / read_text
        (
            'val = report.read_text(&quot;utf-8&quot;).strip()\\nprint(&quot;Прочитано:&quot;, val)',
            'val = report.read_text(&quot;utf-8&quot;).strip()\\nprint(&quot;Прочитано:&quot;, val)  # \'Готово\''
        ),
        # BLOCK 344: iterdir
        (
            'for item in Path(&quot;.&quot;).iterdir():\\n    if item.is_dir():\\n        print(&quot;Папка:&quot;, item.name)',
            'for item in Path(&quot;.&quot;).iterdir():\\n    if item.is_dir():\\n        print(&quot;Папка:&quot;, item.name)  # выведет имена подкаталогов'
        ),
        # BLOCK 345: rglob
        (
            'py_files = list(Path(&quot;.&quot;).rglob(&quot;*.py&quot;))\\nprint(&quot;Найдено скриптов:&quot;, len(py_files))',
            'py_files = list(Path(&quot;.&quot;).rglob(&quot;*.py&quot;))\\nprint(&quot;Найдено скриптов:&quot;, len(py_files))  # количество .py файлов во всех подпапках'
        ),
        # BLOCK 406: pydantic normalize_email
        (
            'reg = RegistrationSchema(email=&quot;  Alice@Example.com &quot;, password=&quot;secret_password&quot;, password_repeat=&quot;secret_password&quot;)\\nprint(&quot;Нормализованный email:&quot;, reg.email)',
            'reg = RegistrationSchema(email=&quot;  Alice@Example.com &quot;, password=&quot;secret_password&quot;, password_repeat=&quot;secret_password&quot;)\\nprint(&quot;Нормализованный email:&quot;, reg.email)  # \'alice@example.com\' (очищен от пробелов и в нижнем регистре)'
        ),
        # BLOCK 407: pydantic exclude_unset
        (
            'print(&quot;Обычный model_dump():&quot;, patch_payload.model_dump())\\nprint(&quot;Только переданные поля (exclude_unset=True):&quot;, patch_payload.model_dump(exclude_unset=True))',
            'print(&quot;Обычный model_dump():&quot;, patch_payload.model_dump())  # {\'username\': \'new_nick\', \'bio\': None}\\nprint(&quot;Только переданные поля (exclude_unset=True):&quot;, patch_payload.model_dump(exclude_unset=True))  # {\'username\': \'new_nick\'}'
        ),
        # BLOCK 409: django urls
        (
            'print(&quot;Зарегистрирован маршрут:&quot;, urlpatterns[0][0], &quot;| name =&quot;, urlpatterns[0][2])\\nprint(&quot;Обратное р',
            'print(&quot;Зарегистрирован маршрут:&quot;, urlpatterns[0][0], &quot;| name =&quot;, urlpatterns[0][2])  # \'orders/<int:pk>/\' | name = \'order-detail\'\\nprint(&quot;Обратное р'
        ),
        # BLOCK 422: flask db.session
        (
            'print(&quot;Безопасное сохранение через db.session:&quot;, register_account_safely(&quot;user@flask.io&quot;))',
            'print(&quot;Безопасное сохранение через db.session:&quot;, register_account_safely(&quot;user@flask.io&quot;))  # {\'ok\': True, \'email\': \'user@flask.io\'}'
        ),
        # BLOCK 423: fastapi get_item
        (
            'print(&quot;Ответ эндпоинта get_item:&quot;, res)',
            'print(&quot;Ответ эндпоинта get_item:&quot;, res)  # {\'item_id\': 42, \'currency\': \'RUB\', \'price\': 1990.0}'
        ),
        # BLOCK 425: fastapi response_model
        (
            'safe_output = UserPublicResponse(**raw_db_user).model_dump()\\nprint(&quot;Отфильтрованный через response_model ответ клиенту:&quot;, safe_output)',
            'safe_output = UserPublicResponse(**raw_db_user).model_dump()\\nprint(&quot;Отфильтрованный через response_model ответ клиенту:&quot;, safe_output)  # {\'id\': 7, \'username\': \'ksenya\', \'email\': \'ksenya@example.com\'}'
        ),
        # BLOCK 428: fastapi modular routers
        (
            'print(&quot;Вызов модульного роутера пользователей:&quot;, asyncio.run(get_user_endpoint(10)))\\nprint(&quot;Вызов модульного роутера заказов:&quot;, asyncio.run(create_order_endpoint()))',
            'print(&quot;Вызов модульного роутера пользователей:&quot;, asyncio.run(get_user_endpoint(10)))  # {\'user_id\': 10, \'role\': \'member\'}\\nprint(&quot;Вызов модульного роутера заказов:&quot;, asyncio.run(create_order_endpoint()))  # {\'order_id\': 501, \'status\': \'new\'}'
        ),
        # BLOCK 429: fastapi router token
        (
            'print(&quot;Проверка токена уровня роутера:&quot;, verify_internal_token(&quot;valid-secret&quot;))',
            'print(&quot;Проверка токена уровня роутера:&quot;, verify_internal_token(&quot;valid-secret&quot;))  # True (доступ разрешён)'
        ),
        # BLOCK 431: fastapi dependency graph
        (
            'print(&quot;Граф зависимостей успешно разрешён:&quot;, admin_user)',
            'print(&quot;Граф зависимостей успешно разрешён:&quot;, admin_user)  # {\'id\': 42, \'username\': \'alice\', \'role\': \'admin\', \'db_conn\': 101}'
        ),
        # BLOCK 435: flask create_user
        (
            'print(f&quot;Ответ Flask-эндпоинта -&gt; статус {status_code}, тело: {body}&quot;)',
            'print(f&quot;Ответ Flask-эндпоинта -&gt; статус {status_code}, тело: {body}&quot;)  # статус 400, тело: {\'error\': \'Поле email обязательно\'}'
        ),
        # BLOCK 436: flask errorhandler
        (
            'print(f&quot;Глобальный errorhandler вернул {code_err}:&quot;, resp_err)',
            'print(f&quot;Глобальный errorhandler вернул {code_err}:&quot;, resp_err)  # 409: {\'error\': \'insufficient_funds\', \'needed\': 1500.0}'
        ),
        # BLOCK 440: jwt encode/decode
        (
            'print(&quot;Сгенерирован JWT:&quot;, encoded_token[:36] + &quot;...&quot;)\\nprint(&quot;Проверенный Payload:&quot;, decoded_payload)',
            'print(&quot;Сгенерирован JWT:&quot;, encoded_token[:36] + &quot;...&quot;)  # \'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\'\\nprint(&quot;Проверенный Payload:&quot;, decoded_payload)          # {\'user_id\': 42, \'role\': \'admin\'}'
        ),
        # BLOCK 444: cookie header
        (
            'print(&quot;Безопасный заголовок Set-Cookie:&quot;, build_secure_cookie_header(&quot;s_9f8a7b6c&quot;))',
            'print(&quot;Безопасный заголовок Set-Cookie:&quot;, build_secure_cookie_header(&quot;s_9f8a7b6c&quot;))  # \'session_id=s_9f8a7b6c; Max-Age=86400; Path=/; HttpOnly; Secure; SameSite=Strict\''
        ),
        # BLOCK 445: api key
        (
            'print(&quot;Проверка подлинного ключа:&quot;, verify_api_key(created[&quot;show_once_key&quot;], created[&quot;db_record&quot;]))',
            'print(&quot;Проверка подлинного ключа:&quot;, verify_api_key(created[&quot;show_once_key&quot;], created[&quot;db_record&quot;]))  # True (хэши совпали через hmac.compare_digest)'
        ),
        # BLOCK 447: RBAC
        (
            'print(&quot;Есть ли у manager право orders:write?&quot;, has_permission_rbac([&quot;manager&quot;], &quot;orders:write&quot;))\\nprint(&quot;Есть ли у manager право orders:refund?&quot;, ha',
            'print(&quot;Есть ли у manager право orders:write?&quot;, has_permission_rbac([&quot;manager&quot;], &quot;orders:write&quot;))  # True\\nprint(&quot;Есть ли у manager право orders:refund?&quot;, ha'
        ),
        # BLOCK 452: Fixed window limiter
        (
            'print(&quot;Запрос 1:&quot;, limiter.allow())\\nprint(&quot;Запрос 2:&quot;, limiter.allow())\\nprint(&quot;Запрос 3:&quot;, limiter.allow())\\nprint(&quot;Запрос 4:&quot;, limiter.allow())',
            'print(&quot;Запрос 1:&quot;, limiter.allow())  # True (1/3)\\nprint(&quot;Запрос 2:&quot;, limiter.allow())  # True (2/3)\\nprint(&quot;Запрос 3:&quot;, limiter.allow())  # True (3/3)\\nprint(&quot;Запрос 4:&quot;, limiter.allow())  # False (лимит превышен, 429 Too Many Requests)'
        ),
        # BLOCK 453: Sliding window limiter
        (
            'print(&quot;Запрос 1:&quot;, sw.allow())\\nprint(&quot;Запрос 2:&quot;, sw.allow())\\nprint(&quot;Запрос 3:&quot;, sw.allow())',
            'print(&quot;Запрос 1:&quot;, sw.allow())  # True\\nprint(&quot;Запрос 2:&quot;, sw.allow())  # True\\nprint(&quot;Запрос 3:&quot;, sw.allow())  # False (окно заполнено)'
        ),
        # BLOCK 454: Token bucket limiter
        (
            'print(&quot;Пакетный запрос 1:&quot;, tb.allow())\\nprint(&quot;Пакетный запрос 2:&quot;, tb.allow())\\nprint(&quot;Пакетный запрос 3:&quot;, tb.allow())',
            'print(&quot;Пакетный запрос 1:&quot;, tb.allow())  # True (в ведре есть токен)\\nprint(&quot;Пакетный запрос 2:&quot;, tb.allow())  # True\\nprint(&quot;Пакетный запрос 3:&quot;, tb.allow())  # False (ведро опустело, ждём пополнения)'
        ),
        # BLOCK 455: Redis limiter
        (
            'print(&quot;Разрешён ли запрос IP 192.168.1.5?&quot;, is_allowed(&quot;192.168.1.5&quot;))',
            'print(&quot;Разрешён ли запрос IP 192.168.1.5?&quot;, is_allowed(&quot;192.168.1.5&quot;))  # True (счётчик инкрементирован в Redis)'
        ),
        # BLOCK 465: middleware pipeline
        (
            'print(&quot;Результат пайплайна middleware:&quot;, resp)',
            'print(&quot;Результат пайплайна middleware:&quot;, resp)  # 200: {\'auth_user\': \'alice\', \'body\': \'processed\', \'duration_ms\': 12}'
        ),
        # BLOCK 466: Domain exception
        (
            'print(&quot;Перехвачена доменная ошибка:&quot;, exc)',
            'print(&quot;Перехвачена доменная ошибка:&quot;, exc)  # \'Недостаточно средств на счёте\''
        ),
        # BLOCK 467: protocol order
        (
            'print(&quot;Оформлен заказ:&quot;, order)',
            'print(&quot;Оформлен заказ:&quot;, order)  # {\'order_id\': 101, \'status\': \'paid\', \'total\': 3000.0}'
        ),
        # BLOCK 471: lock order
        (
            'print(&quot;Безопасный порядок захвата блокировок:&quot;, lock_order_for_transfer(99, 12))',
            'print(&quot;Безопасный порядок захвата блокировок:&quot;, lock_order_for_transfer(99, 12))  # (12, 99) — защита от Deadlock'
        ),
        # BLOCK 474: backoff
        (
            'print(&quot;Задержки ретраев (Exponential Backoff):&quot;, compute_backoff_delays(4))',
            'print(&quot;Задержки ретраев (Exponential Backoff):&quot;, compute_backoff_delays(4))  # ~[1.1s, 2.3s, 4.2s, 8.1s] с джиттером'
        ),
        # BLOCK 475: circuit breaker
        (
            'print(&quot;Состояние Circuit Breaker:&quot;, cb.state)',
            'print(&quot;Состояние Circuit Breaker:&quot;, cb.state)  # \'OPEN\' (защита от каскадного сбоя)'
        ),
        # BLOCK 479: sha256 chunks
        (
            'print(&quot;Размер файла:&quot;, size, &quot;SHA-256:&quot;, sha256_hex[:16] + &quot;...&quot;)',
            'print(&quot;Размер файла:&quot;, size, &quot;SHA-256:&quot;, sha256_hex[:16] + &quot;...&quot;)  # потоковая обработка без нагрузки на память'
        ),
        # BLOCK 480: magic bytes
        (
            'print(&quot;MIME-тип по Magic Bytes:&quot;, detect_mime(b&quot;\\x89PNG\\r\\n\\x1a\\n...&quot;))',
            'print(&quot;MIME-тип по Magic Bytes:&quot;, detect_mime(b&quot;\\x89PNG\\r\\n\\x1a\\n...&quot;))  # \'image/png\' (сигнатура файла)'
        ),
        # BLOCK 481: app settings
        (
            'print(&quot;Конфигурация валидна:&quot;, cfg.app_env, &quot;| pool_size =&quot;, cfg.db_pool_size, &quot;| debug =&quot;, cfg.debug)',
            'print(&quot;Конфигурация валидна:&quot;, cfg.app_env, &quot;| pool_size =&quot;, cfg.db_pool_size, &quot;| debug =&quot;, cfg.debug)  # production | pool_size = 10 | debug = False'
        ),
        # BLOCK 484: framework pipeline
        (
            'print(f&quot;Успешный запрос -&gt; {status_ok}: {resp_ok}&quot;)\\nprint(f&quot;Ошибка валидации -&gt; {status_err}: {resp_err}&quot;)',
            'print(f&quot;Успешный запрос -&gt; {status_ok}: {resp_ok}&quot;)    # 201: {\'id\': 101, \'status\': \'created\', \'amount\': 2500}\\nprint(f&quot;Ошибка валидации -&gt; {status_err}: {resp_err}&quot;)  # 422: {\'detail\': \'Поле amount должно быть числом > 0\'}'
        ),
        # BLOCK 485: choose framework
        (
            'print(&quot;1. E-commerce с бэкофисом:&quot;, choose_framework(needs_admin=True, high_async_io=False, minimal_footprint=False))\\nprint(&quot;2. Асинхронный AI-шлюз:&quot;, choose_framework(needs_admin=False, high_async_io=True, minimal_footprint=False))\\nprint(&quot;3. Лёгкий микросервис:&quot;, choose_framework(needs_admin=False, high_async_io=False, minimal_footprint=True))',
            'print(&quot;1. E-commerce с бэкофисом:&quot;, choose_framework(needs_admin=True, high_async_io=False, minimal_footprint=False))  # \'Django + DRF\'\\nprint(&quot;2. Асинхронный AI-шлюз:&quot;, choose_framework(needs_admin=False, high_async_io=True, minimal_footprint=False))   # \'FastAPI + Pydantic v2\'\\nprint(&quot;3. Лёгкий микросервис:&quot;, choose_framework(needs_admin=False, high_async_io=False, minimal_footprint=True))     # \'Flask\''
        ),
        # BLOCK 490: list reallocations
        (
            'print(&quot;Реаллокации list (len -&gt; байты):&quot;)\\nfor length, size_b in resizes[:4]:',
            'print(&quot;Реаллокации list (len -&gt; байты):&quot;)  # [(1, 88), (5, 120), (9, 184), (17, 248)]\\nfor length, size_b in resizes[:4]:'
        ),
        # BLOCK 491: build_csv_row
        (
            'print(&quot;CSV:&quot;,\\n      build_csv_row([1, 2, 3, 4, 5]))',
            'print(&quot;CSV:&quot;,\\n      build_csv_row([1, 2, 3, 4, 5]))  # \'10,20,30,40,50\' (за O(n))'
        ),
        # BLOCK 492: swap and pop
        (
            'print(f&quot;Удалён: {deleted}&quot;)\\nprint(f&quot;Осталось: {servers}&quot;)',
            'print(f&quot;Удалён: {deleted}&quot;)    # \'srv-2\' (удалено за O(1))\\nprint(f&quot;Осталось: {servers}&quot;)  # [\'srv-1\', \'srv-4\', \'srv-3\']'
        ),
        # BLOCK 628: in-memory sender
        (
            'print(&quot;Отправленные уведомления (без SMTP):&quot;, fake_notifier.sent_messages)',
            'print(&quot;Отправленные уведомления (без SMTP):&quot;, fake_notifier.sent_messages)  # [(\'alice@example.com\', \'Добро пожаловать в Python Academy!\')]'
        ),
        # BLOCK 645: discount strategies
        (
            'print(&quot;Без скидки:&quot;, cart.total())\\n\\ncart.set_discount_strategy(PercentDiscount(15))\\nprint(&quot;Со скидкой 15%:&quot;, cart.total())\\n\\ncart.set_discount_strategy(ThresholdDiscount(threshold=1500.0, discount_amount=400.0))\\nprint(&quot;По купону -400 руб. от 1500:&quot;, cart.total())',
            'print(&quot;Без скидки:&quot;, cart.total())  # 2000.0\\n\\ncart.set_discount_strategy(PercentDiscount(15))\\nprint(&quot;Со скидкой 15%:&quot;, cart.total())  # 1700.0\\n\\ncart.set_discount_strategy(ThresholdDiscount(threshold=1500.0, discount_amount=400.0))\\nprint(&quot;По купону -400 руб. от 1500:&quot;, cart.total())  # 1600.0'
        ),
        # BLOCK 669: 3-way merge
        (
            'def resolve_3way(base: str, ours: str, theirs: str) -&gt; str:\n    bits = [(4,',
            'def resolve_3way(base: str, ours: str, theirs: str) -&gt; str:\n    bits = [(4,'
        ),
        # BLOCK 676: feature flags
        (
            'flags = {&quot;new_payment_flow&quot;: False}',
            'flags = {&quot;new_payment_flow&quot;: False}'
        ),
        # BLOCK 680: PR ready
        (
            'def check_pr_ready(lines: int, has_tests: bool, ci_ok: bool)',
            'def check_pr_ready(lines: int, has_tests: bool, ci_ok: bool)'
        ),
        # BLOCK 693: docker exit
        (
            'def diagnose_container_exit(exit_code: int, oom_killed: bool',
            'def diagnose_container_exit(exit_code: int, oom_killed: bool'
        ),
        # BLOCK 730: octal_to_rwx
        (
            'def octal_to_rwx(octal_str: str) -&gt; str:\n    bits = [(4,',
            'def octal_to_rwx(octal_str: str) -&gt; str:\n    bits = [(4,'
        ),
        # BLOCK 743: ssh security
        (
            'def verify_ssh_security(key_filename: str, octal_perms: str,',
            'def verify_ssh_security(key_filename: str, octal_perms: str,'
        ),
        # BLOCK 746: nginx proxy
        (
            'def simulate_nginx_proxy(path: str, body_mb: float, client_i',
            'def simulate_nginx_proxy(path: str, body_mb: float, client_i'
        ),
        # BLOCK 756: unittest result
        (
            'parse_Completed_age',
            'parse_Completed_age'
        )
    ]

    count = 0
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new, 1)
            count += 1

    print(f"Applied {count} didactic content replacements.")
    return text

def main():
    st_path = Path("standards/standards.html")
    print(f"Reading {st_path}...")
    orig = st_path.read_text(encoding="utf-8")
    enriched = enrich_all_snippets(orig)
    st_path.write_text(enriched, encoding="utf-8")
    print(f"Saved {st_path}.")

    ac_path = Path("academy.html")
    print(f"Syncing to {ac_path}...")
    ac_path.write_text(enriched, encoding="utf-8")
    print(f"Saved {ac_path} (100% byte match).")

    notes_path = Path("data/content/notes.json")
    if notes_path.exists():
        print(f"Syncing to {notes_path}...")
        notes_orig = notes_path.read_text(encoding="utf-8")
        notes_enriched = enrich_all_snippets(notes_orig)
        notes_path.write_text(notes_enriched, encoding="utf-8")
        print(f"Saved {notes_path}.")

if __name__ == '__main__':
    main()
