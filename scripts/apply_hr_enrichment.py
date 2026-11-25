import re

with open("standards/standards.html", "r", encoding="utf-8") as f:
    content = f.read()

orig_len = len(content)
print(f"Original file length: {orig_len}")

# =========================================================================
# 1. Enrich 18 keyword cards to have 4 distinct concepts
# =========================================================================

replacements = [
    # 1. hr-py-5
    (
        """    id: 'hr-py-5',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'В чём разница между операторами == и is?',
    keywords: ['== сравнивает значения (__eq__)', 'is сравнивает адреса памяти (id)', 'Сравнение с None'],""",
        """    id: 'hr-py-5',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'В чём разница между операторами == и is?',
    keywords: ['== сравнивает значения (__eq__)', 'is сравнивает адреса памяти (id)', 'Сравнение с синглтоном None (if x is None)', 'Идентичность объектов в куче'],"""
    ),
    # 2. hr-py-6
    (
        """    id: 'hr-py-6',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'Как работает блок try-except-finally и почему нельзя писать голый except:?',
    keywords: ['finally выполняется всегда', 'Голый except ловит KeyboardInterrupt и SystemExit', 'Ловить конкретные Exception'],""",
        """    id: 'hr-py-6',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'Как работает блок try-except-finally и почему нельзя писать голый except:?',
    keywords: ['finally выполняется всегда (cleanup)', 'Голый except ловит SystemExit и KeyboardInterrupt', 'Перехват конкретных Exception', 'Иерархия исключений Python'],"""
    ),
    # 3. hr-py-7
    (
        """    id: 'hr-py-7',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'Зачем нужны *args и **kwargs в функциях?',
    keywords: ['Переменное число аргументов', 'Позиционные кортежем (*args)', 'Именованные словарём (**kwargs)'],""",
        """    id: 'hr-py-7',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'Зачем нужны *args и **kwargs в функциях?',
    keywords: ['Переменное число аргументов', 'Позиционные кортежем (*args)', 'Именованные словарём (**kwargs)', 'Проброс аргументов в декораторы и super()'],"""
    ),
    # 4. hr-py-8
    (
        """    id: 'hr-py-8',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'Что такое менеджер контекста (конструкция with) и как он устроен?',
    keywords: ['Гарантированное освобождение ресурсов', 'Методы __enter__ и __exit__', 'Файлы, БД-сессии, транзакции'],""",
        """    id: 'hr-py-8',
    cat: 'py',
    catLabel: '🐍 Python',
    q: 'Что такое менеджер контекста (конструкция with) и как он устроен?',
    keywords: ['Гарантированное освобождение ресурсов', 'Магические методы __enter__ и __exit__', 'Файлы, БД-сессии, транзакции', 'Безопасная обработка исключений в блоке'],"""
    ),
    # 5. hr-web-2
    (
        """    id: 'hr-web-2',
    cat: 'web',
    catLabel: '🌐 Сети и Web',
    q: 'В чём разница между HTTP-методами GET и POST?',
    keywords: ['GET — чтение (идемпотентный)', 'POST — создание (не идемпотентный)', 'Параметры в URL vs тело запроса'],""",
        """    id: 'hr-web-2',
    cat: 'web',
    catLabel: '🌐 Сети и Web',
    q: 'В чём разница между HTTP-методами GET и POST?',
    keywords: ['GET: чтение ресурса (идемпотентный, безопасный)', 'POST: создание ресурса (не идемпотентный)', 'Параметры в Query string vs тело запроса', 'Кэширование браузером и прокси'],"""
    ),
    # 6. hr-web-3
    (
        """    id: 'hr-web-3',
    cat: 'web',
    catLabel: '🌐 Сети и Web',
    q: 'В чём разница между кодами ответов 401 Unauthorized и 403 Forbidden?',
    keywords: ['401 — аутентификация («Кто вы?»)', '403 — авторизация («У вас нет прав»)', 'Токен отсутствует vs токен есть, но роль не подходит'],""",
        """    id: 'hr-web-3',
    cat: 'web',
    catLabel: '🌐 Сети и Web',
    q: 'В чём разница между кодами ответов 401 Unauthorized и 403 Forbidden?',
    keywords: ['401 Unauthorized: аутентификация («Кто вы?»)', '403 Forbidden: авторизация («Недостаточно прав»)', 'Bearer JWT токен в заголовке Authorization', 'Ролевая модель доступа (RBAC)'],"""
    ),
    # 7. hr-web-4
    (
        """    id: 'hr-web-4',
    cat: 'web',
    catLabel: '🌐 Сети и Web',
    q: 'В чём разница между кодами 502 Bad Gateway и 504 Gateway Timeout?',
    keywords: ['502 — некорректный ответ бэкенда', '504 — таймаут ожидания бэкенда', 'Прокси (Nginx) и бэкенд (Gunicorn/FastAPI)'],""",
        """    id: 'hr-web-4',
    cat: 'web',
    catLabel: '🌐 Сети и Web',
    q: 'В чём разница между кодами 502 Bad Gateway и 504 Gateway Timeout?',
    keywords: ['502 Bad Gateway: сбой или недоступность бэкенда', '504 Gateway Timeout: таймаут ожидания ответа сервиса', 'Обратный прокси (Nginx / Ingress)', 'Таймауты в Gunicorn/Uvicorn/FastAPI'],"""
    ),
    # 8. hr-db-3
    (
        """    id: 'hr-db-3',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'В чём разница между условиями WHERE и HAVING в SQL?',
    keywords: ['WHERE фильтрует строки ДО группировки', 'HAVING фильтрует группы ПОСЛЕ GROUP BY', 'HAVING работает с агрегатами (COUNT, SUM)'],""",
        """    id: 'hr-db-3',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'В чём разница между условиями WHERE и HAVING в SQL?',
    keywords: ['WHERE: фильтрует строки ДО группировки', 'HAVING: фильтрует группы ПОСЛЕ GROUP BY', 'Агрегатные функции (COUNT, SUM, AVG) только в HAVING', 'Порядок выполнения фаз SQL-запроса'],"""
    ),
    # 9. hr-db-5
    (
        """    id: 'hr-db-5',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'Что такое первичный ключ (Primary Key) и внешний ключ (Foreign Key)?',
    keywords: ['Primary Key — уникальный идентификатор строки', 'Foreign Key — связь с Primary Key другой таблицы', 'Целостность данных'],""",
        """    id: 'hr-db-5',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'Что такое первичный ключ (Primary Key) и внешний ключ (Foreign Key)?',
    keywords: ['Primary Key: уникальный идентификатор строки', 'Foreign Key: ссылка на Primary Key другой таблицы', 'Обеспечение ссылочной целостности данных', 'Связи один-ко-многим и каскадное удаление (ON DELETE)'],"""
    ),
    # 10. hr-db-6
    (
        """    id: 'hr-db-6',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'Что такое проблема N+1 запросов в ORM и как с ней бороться?',
    keywords: ['1 запрос на список + N запросов на связанные сущности', 'Ленивая загрузка (Lazy Loading)', 'Жадная загрузка: select_related / joinedload'],""",
        """    id: 'hr-db-6',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'Что такое проблема N+1 запросов в ORM и как с ней бороться?',
    keywords: ['1 запрос на список + N запросов на связанные строки', 'Ленивая загрузка связей (Lazy Loading)', 'Жадная загрузка: select_related / joinedload', 'Оптимизация пула соединений и нагрузки на СУБД'],"""
    ),
    # 11. hr-db-7
    (
        """    id: 'hr-db-7',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'Зачем нужны миграции в базах данных (Alembic или Django Migrations)?',
    keywords: ['Версионирование схемы БД', 'Синхронизация окружений (dev, test, prod)', 'Откат изменений (downgrade)'],""",
        """    id: 'hr-db-7',
    cat: 'db',
    catLabel: '🗄️ Базы данных',
    q: 'Зачем нужны миграции в базах данных (Alembic или Django Migrations)?',
    keywords: ['Версионирование схемы БД в Git', 'Синхронизация окружений (dev, test, prod)', 'Откат изменений (downgrade / rollback)', 'Инструменты миграций: Alembic и Django'],"""
    ),
    # 12. hr-infra-4
    (
        """    id: 'hr-infra-4',
    cat: 'infra',
    catLabel: '🚀 Инфраструктура',
    q: 'Зачем нужны переменные окружения (.env) и почему их нельзя коммитить в Git?',
    keywords: ['Хранение секретов (пароли, API-ключи, токены)', 'Разделение кода и конфигурации (12 Factor App)', 'Безопасность'],""",
        """    id: 'hr-infra-4',
    cat: 'infra',
    catLabel: '🚀 Инфраструктура',
    q: 'Зачем нужны переменные окружения (.env) и почему их нельзя коммитить в Git?',
    keywords: ['Хранение секретов (пароли, API-ключи, JWT)', 'Принцип 12 Factor App (разметка конфигурации)', 'Файл .env в .gitignore', 'Библиотека pydantic-settings для типобезопасности'],"""
    ),
    # 13. hr-infra-5
    (
        """    id: 'hr-infra-5',
    cat: 'infra',
    catLabel: '🚀 Инфраструктура',
    q: 'Что такое CI/CD простыми словами?',
    keywords: ['Continuous Integration (автотесты и линтеры)', 'Continuous Deployment (автодеплой на сервер)', 'GitHub Actions / GitLab CI'],""",
        """    id: 'hr-infra-5',
    cat: 'infra',
    catLabel: '🚀 Инфраструктура',
    q: 'Что такое CI/CD простыми словами?',
    keywords: ['Continuous Integration (автотесты, линтеры, flake8)', 'Continuous Deployment (автоматический деплой)', 'Пайплайны в GitHub Actions / GitLab CI', 'Контроль регрессий перед слиянием PR'],"""
    ),
    # 14. hr-test-2
    (
        """    id: 'hr-test-2',
    cat: 'test',
    catLabel: '🧪 Тесты и Git',
    q: 'Что такое фикстуры в pytest и зачем они нужны?',
    keywords: ['Подготовка тестовых данных', 'Очистка ресурсов (yield/teardown)', 'Переиспользуемость (@pytest.fixture)'],""",
        """    id: 'hr-test-2',
    cat: 'test',
    catLabel: '🧪 Тесты и Git',
    q: 'Что такое фикстуры в pytest и зачем они нужны?',
    keywords: ['Подготовка тестовых данных и окружения', 'Гарантированная очистка ресурсов (генератор с yield)', 'Области видимости фикстур (scope: function, session)', 'Параметризация тестов (@pytest.mark.parametrize)'],"""
    ),
    # 15. hr-test-3
    (
        """    id: 'hr-test-3',
    cat: 'test',
    catLabel: '🧪 Тесты и Git',
    q: 'Что такое моки (Mock) в тестировании и когда их используют?',
    keywords: ['Имитация внешних сервисов', 'Изоляция unit-тестов', 'Независимость от сети (платёжки, почта, SMS)'],""",
        """    id: 'hr-test-3',
    cat: 'test',
    catLabel: '🧪 Тесты и Git',
    q: 'Что такое моки (Mock) в тестировании и когда их используют?',
    keywords: ['Имитация внешних сервисов (Mock, patch)', 'Изоляция unit-тестов от сети и БД', 'Проверка вызовов (assert_called_once_with)', 'Ускорение прогона тестового сьюта'],"""
    ),
    # 16. hr-puz-2
    (
        """    id: 'hr-puz-2',
    cat: 'puzzles',
    catLabel: '🧩 Микро-загадки',
    q: 'Как удалить дубликаты из списка, сохранив исходный порядок элементов?',
    keywords: ['list(dict.fromkeys(items))', 'Сложность O(n)', 'set() ломает порядок!'],""",
        """    id: 'hr-puz-2',
    cat: 'puzzles',
    catLabel: '🧩 Микро-загадки',
    q: 'Как удалить дубликаты из списка, сохранив исходный порядок элементов?',
    keywords: ['list(dict.fromkeys(items))', 'Линейная сложность O(n) по времени', 'Сохранение порядка вставки ключей (Python 3.7+)', 'set() разрушает порядок элементов'],"""
    ),
    # 17. hr-puz-5
    (
        """    id: 'hr-puz-5',
    cat: 'puzzles',
    catLabel: '🧩 Микро-загадки',
    q: 'Что выведет код: [lambda: i for i in range(3)][0]()?',
    keywords: ['Выведет 2!', 'Позднее связывание (Late Binding) в замыканиях', 'Переменная берётся в момент вызова, а не создания'],""",
        """    id: 'hr-puz-5',
    cat: 'puzzles',
    catLabel: '🧩 Микро-загадки',
    q: 'Что выведет код: [lambda: i for i in range(3)][0]()?',
    keywords: ['Выведет 2 (последнее значение счётчика)', 'Позднее связывание (Late Binding) в Python', 'Переменная считывается в момент вызова функции', 'Фиксация через дефолтный аргумент: lambda i=i: i'],"""
    ),
    # 18. hr-puz-6
    (
        """    id: 'hr-puz-6',
    cat: 'puzzles',
    catLabel: '🧩 Микро-загадки',
    q: 'Что выполнится быстрее: 1000 in set_obj или 1000 in list_obj (при 100 000 элементах) и почему?',
    keywords: ['in set_obj в разы быстрее', 'Хеш-таблица: O(1) в среднем', 'Список: O(n) полный перебор'],""",
        """    id: 'hr-puz-6',
    cat: 'puzzles',
    catLabel: '🧩 Микро-загадки',
    q: 'Что выполнится быстрее: 1000 in set_obj или 1000 in list_obj (при 100 000 элементах) и почему?',
    keywords: ['in set_obj в сотни раз быстрее списка', 'Хеш-таблица: поиск за константное время O(1)', 'Список: линейный перебор O(n)', 'Вычисление hash() и проверка коллизий'],"""
    ),
]

for idx, (old_text, new_text) in enumerate(replacements, 1):
    assert old_text in content, f"Replacement {idx} failed: old_text not found!"
    content = content.replace(old_text, new_text)
    print(f"[{idx}/18] Card keyword enrichment applied.")

# =========================================================================
# 2. Update nav capsule button to reflect 37 + 5 cards
# =========================================================================
old_nav_pill = '<button class="hr-nav-pill ${mockInterviewState.hrSubTab===' + "'terms'?'active':''}\" data-hr-subtab=\"terms\">🗂 2. Блиц-карточки (37)</button>"
new_nav_pill = '<button class="hr-nav-pill ${mockInterviewState.hrSubTab===' + "'terms'?'active':''}\" data-hr-subtab=\"terms\">🗂 2. Блиц-карточки (37 + 5)</button>"

assert old_nav_pill in content, "old_nav_pill not found!"
content = content.replace(old_nav_pill, new_nav_pill)
print("Nav pill updated: 🗂 2. Блиц-карточки (37 + 5).")

# Update empty weak zone button text to be dynamic
old_empty_btn = '<button class="btn btn-primary dominant-btn" data-hr-filter="all" style="padding:10px 24px;font-weight:800;">Показать все 37 карточек ➔</button>'
new_empty_btn = '<button class="btn btn-primary dominant-btn" data-hr-filter="all" style="padding:10px 24px;font-weight:800;">Показать все карточки (${allCards.length}) ➔</button>'
assert old_empty_btn in content, "old_empty_btn not found!"
content = content.replace(old_empty_btn, new_empty_btn)
print("Empty weak zone button text made dynamic.")

# =========================================================================
# 3. Save to standards/standards.html and sync academy.html
# =========================================================================
with open("standards/standards.html", "w", encoding="utf-8") as f:
    f.write(content)

new_len = len(content)
print(f"Updated standards/standards.html: length {new_len} (delta: {new_len - orig_len} bytes)")

with open("academy.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Synchronized byte-for-byte to academy.html.")
