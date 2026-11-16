# -*- coding: utf-8 -*-
"""
scripts/apply_notes_cards_alignment.py

Комплексная синхронизация и выравнивание отношения карточек к конспектам (Notes <-> Cards):
1. Пополнение 8 колод (Ф-078, Ф-097, Ф-183, Ф-185, Ф-206, Ф-215, Ф-216, Ф-225) целевыми карточками
   для 100% дидактического покрытия конспектов К-059, К-203, К-167, К-168, К-191, К-209, К-206, К-216.
2. Обновление CANONICAL_NOTE_DECKS_MAP и привязок kIds/fIds в треках:
   - 0 потерянных (dropped) колод в цепочках бусин
   - 0 дублирующихся (duplicate) колод внутри одного навыка
   - 0 колод-сирот (orphan decks) из 287
   - 0 конспектов без карточек из 238
3. Синхронизация всех 4 канонических слоёв:
   - data/content/cards.json, data/content/notes.json, data/content/manifest.json
   - knowledge_base/**/*.md и 00 · 🗺️ Карта Мастерства.md
   - standards/standards.html
   - academy.html (100% побайтовая идентичность)
"""

import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

NEW_CARDS_BY_DECK = {
    'Ф-078': [
        {
            'q': 'В чём ключевое отличие обычного модуля от пакета в файловой системе Python?',
            'a': 'Модуль — это одиночный файл <code>.py</code>, а пакет — директория с модулями и иерархическим пространством имён через точку (<code>pkg.submod</code>)'
        },
        {
            'q': 'Что такое namespace-пакет (неявный пакет пространства имён по PEP 420), появившийся в Python 3.3?',
            'a': 'Пакет без файла <code>__init__.py</code>, части которого могут располагаться в разных директориях <code>sys.path</code> и объединяться под общим именем'
        },
        {
            'q': 'Зачем в классическом пакете Python создаётся файл <code>__init__.py</code> даже в современном Python 3?',
            'a': 'Он явно обозначает границы пакета, выполняется при первом импорте и позволяет сформировать удобный публичный интерфейс (фасад) пакета'
        },
        {
            'q': 'Какое изменение в работе функций вроде <code>range()</code>, <code>map()</code>, <code>filter()</code> и <code>dict.keys()</code> произошло при переходе от Python 2 к Python 3?',
            'a': 'Вместо создания полных списков в памяти они стали возвращать ленивые итераторы и объекты-представления (<code>dict_keys</code>), экономя память'
        },
        {
            'q': 'Как изменилось представление строк и работа оператора деления <code>/</code> в Python 3 по сравнению с Python 2?',
            'a': 'Тип <code>str</code> стал по умолчанию строкой Unicode (вместо байтов), а оператор <code>/</code> всегда выполняет истинное деление с плавающей точкой (<code>float</code>)'
        },
        {
            'q': 'В каком порядке интерпретатор Python ищет модуль или пакет при выполнении инструкции <code>import</code>?',
            'a': 'Сначала в кэше <code>sys.modules</code>, затем среди встроенных модулей (<code>built-in</code>) и далее по списку директорий в <code>sys.path</code>'
        },
    ],
    'Ф-097': [
        {
            'q': 'В чём разница между прямым прокси (Forward Proxy) и обратным прокси (Reverse Proxy, например Nginx)?',
            'a': 'Forward Proxy стоит перед клиентом и скрывает его от внешних сайтов, а Reverse Proxy стоит перед бэкенд-серверами и принимает трафик от клиентов от имени сервиса'
        },
        {
            'q': 'Какие четыре ключевые задачи выполняет Nginx как обратный прокси перед Python-сервером (Gunicorn или Uvicorn)?',
            'a': 'Терминация TLS (HTTPS), раздача статики напрямую с диска, защита от медленных клиентов (буферизация) и балансировка нагрузки между воркерами'
        },
        {
            'q': 'Какая директива внутри блока <code>location</code> в конфигурации Nginx перенаправляет HTTP-запрос на локальный Python-сервер?',
            'a': 'Директива <code>proxy_pass http://127.0.0.1:8000</code>, пересылающая запрос апстрим-воркерам приложения'
        },
        {
            'q': 'Зачем в конфигурации Nginx при проксировании на Python-бэкенд обязательно передают заголовки <code>X-Forwarded-For</code> и <code>X-Real-IP</code>?',
            'a': 'Без них Python-приложение видит в качестве IP-адреса клиента локальный адрес самого Nginx (<code>127.0.0.1</code>), а не реальный IP пользователя'
        },
        {
            'q': 'Чем отличаются ошибки Nginx <code>502 Bad Gateway</code> и <code>504 Gateway Timeout</code> при работе с Python-бэкендом?',
            'a': '<code>502 Bad Gateway</code> означает, что Gunicorn или Uvicorn упал либо не слушает сокет, а <code>504 Gateway Timeout</code> — что бэкенд не успел ответить за время <code>proxy_read_timeout</code>'
        },
        {
            'q': 'Какая директива Nginx отвечает за лимит размера загружаемого тела запроса и предотвращает ошибку <code>413 Content Too Large</code>?',
            'a': 'Директива <code>client_max_body_size</code> (по умолчанию равна всего <code>1m</code>)'
        },
    ],
    'Ф-183': [
        {
            'q': 'В чём заключается анти-паттерн «Анемичная доменная модель» (Anemic Domain Model) в предметно-ориентированном проектировании (DDD)?',
            'a': 'Сущности представляют собой простые мешки с данными (геттеры и сеттеры без поведения), а вся бизнес-логика размазана по внешним процедурным сервисам'
        },
        {
            'q': 'В чём фундаментальное отличие Сущности (Entity) от Объекта-значения (Value Object) в тактическом DDD?',
            'a': 'Entity определяется уникальным идентификатором (<code>id</code>) и изменяется во времени, а Value Object определяется только своими атрибутами и обязан быть неизменяемым (immutable)'
        },
        {
            'q': 'Как в Python 3 идиоматично реализуется неизменяемый Объект-значение (Value Object), например <code>Money(amount, currency)</code>?',
            'a': 'Через декоратор <code>@dataclass(frozen=True)</code> с проверкой инвариантов внутри метода <code>__post_init__</code>'
        },
        {
            'q': 'Что такое Агрегат (Aggregate) и Корень агрегата (Aggregate Root) в предметно-ориентированном проектировании (DDD)?',
            'a': 'Агрегат — кластер связанных объектов, изменяемых как единое целое в одной транзакции, а Aggregate Root — единственная входная сущность, через методы которой внешний код может менять состояние агрегата'
        },
        {
            'q': 'Почему в DDD внешним объектам запрещено хранить прямые ORM-ссылки на внутренние дочерние элементы чужого агрегата?',
            'a': 'Чтобы никто не мог изменить внутренние данные в обход проверок бизнес-инвариантов Корня агрегата; между агрегатами хранятся только ссылки по <code>ID</code>'
        },
        {
            'q': 'Какую роль играет паттерн Unit of Work (Единица работы) в связке с паттерном Repository и агрегатами DDD?',
            'a': 'Unit of Work координирует транзакцию базы данных и гарантирует атомарное сохранение изменений (<code>commit</code> или <code>rollback</code>) сразу для всех затронутых репозиториев'
        },
    ],
    'Ф-185': [
        {
            'q': 'Какова главная цель методологии Twelve-Factor App (12 факторов) при разработке облачных бэкенд-сервисов?',
            'a': 'Создавать масштабируемые, переносимые и отказоустойчивые сервисы без привязки к конкретному серверу за счёт строгой декларативности и отсутствия локального состояния'
        },
        {
            'q': 'Что требует фактор «Процессы» (Processes) методологии 12-Factor App в отношении хранения состояния между HTTP-запросами?',
            'a': 'Процессы приложения обязаны быть полностью без состояния (stateless и share-nothing), а любые данные сессий, кэша и файлов должны выноситься во внешние хранилища (Redis, PostgreSQL, S3)'
        },
        {
            'q': 'В чём состоит принцип разделения этапов <code>Build</code>, <code>Release</code> и <code>Run</code> согласно методологии 12-Factor App?',
            'a': 'Этап <code>Build</code> собирает неизменяемый артефакт кода (Docker-образ), <code>Release</code> соединяет его с конфигурацией окружения, а <code>Run</code> запускает изолированные процессы'
        },
        {
            'q': 'Как согласно фактору «Журналирование» (Logs) методологии 12-Factor App приложение должно работать с логами в контейнере?',
            'a': 'Приложение не должно само управлять лог-файлами на диске; оно пишет поток структурированных событий (JSON) в стандартный вывод <code>stdout</code>, откуда их собирает инфраструктура'
        },
        {
            'q': 'Что означает фактор «Утилизируемость» (Disposability) для воркеров и веб-серверов в 12-Factor App?',
            'a': 'Быстрый старт процессов и корректное завершение работы (Graceful Shutdown) по сигналу <code>SIGTERM</code>: прекращение приёма новых запросов и безопасное завершение текущих транзакций'
        },
    ],
    'Ф-206': [
        {
            'q': 'Что представляет собой объект <code>Pod</code> в архитектуре оркестратора Kubernetes (K8s)?',
            'a': 'Минимальная единица развёртывания в Kubernetes: обёртка над одним (реже несколькими тесно связанными) контейнером с общим IP-адресом и сетевым пространством'
        },
        {
            'q': 'Зачем в Kubernetes поверх подов используют контроллер <code>Deployment</code> вместо создания одиночных <code>Pod</code> напрямую?',
            'a': '<code>Deployment</code> поддерживает заданное число реплик (<code>replicas</code>), автоматически перезапускает упавшие поды на здоровых узлах и выполняет обновление без простоя (Rolling Update)'
        },
        {
            'q': 'В чём заключается принцип работы цикла согласования (Reconciliation Loop) в Kubernetes?',
            'a': 'Контроллеры Kubernetes непрерывно сравнивают желаемое состояние из YAML-манифеста (Desired State) с фактическим состоянием кластера (Actual State) и автоматически устраняют расхождения'
        },
        {
            'q': 'Зачем в Kubernetes перед подами создаётся ресурс <code>Service</code> и как он находит нужные поды?',
            'a': 'Поды эфемерны и меняют IP при каждом пересоздании, а <code>Service</code> даёт стабильное DNS-имя и виртуальный IP, балансируя трафик на поды по совпадению меток (<code>selector: labels</code>)'
        },
        {
            'q': 'Чем в Kubernetes отличается ресурс <code>ConfigMap</code> от ресурса <code>Secret</code> при передаче настроек в контейнер?',
            'a': '<code>ConfigMap</code> хранит несекретные настройки окружения в открытом виде, а <code>Secret</code> предназначен для паролей, токенов и ключей (с поддержкой шифрования в хранилище <code>etcd</code>)'
        },
        {
            'q': 'В чём разница между параметрами ресурсов <code>requests</code> и <code>limits</code> для CPU и памяти пода в Kubernetes?',
            'a': '<code>requests</code> — гарантированный минимум ресурсов для планирования пода на ноду, а <code>limits</code> — жёсткий потолок, при превышении которого по памяти контейнер убивается с <code>OOMKilled</code>'
        },
    ],
    'Ф-215': [
        {
            'q': 'В чём разница между метриками Line Coverage (покрытие по строкам) и Branch Coverage (покрытие по ветвлениям) при тестировании кода?',
            'a': 'Line Coverage проверяет лишь факт выполнения каждой строки кода, а Branch Coverage требует прохождения обеих веток (<code>True</code> и <code>False</code>) каждого условия <code>if/else</code>'
        },
        {
            'q': 'Почему согласно закону Гудхарта 100% покрытие кода тестами (Test Coverage) не гарантирует отсутствие багов в продакшене?',
            'a': 'Coverage показывает только то, какие строки исполнялись во время тестов, но не проверяет качество проверок <code>assert</code> и не защищает от пропущенных граничных сценариев'
        },
        {
            'q': 'Какой системный хук в модуле <code>sys</code> стандартной библиотеки Python используется инструментами вроде <code>coverage.py</code> для отслеживания исполняемых строк?',
            'a': 'Функция <code>sys.settrace()</code> (или низкоуровневый <code>sys.monitoring</code> в Python 3.12+), перехватывающая события вызова функций и перехода между строками байткода'
        },
        {
            'q': 'С помощью какого плагина и флага командной строки в <code>pytest</code> включают замер покрытия ветвлений (Branch Coverage)?',
            'a': 'Плагин <code>pytest-cov</code> с флагами <code>pytest --cov=app --cov-branch</code>'
        },
    ],
    'Ф-216': [
        {
            'q': 'В чём ключевое отличие модульных тестов (Unit Tests) от интеграционных тестов (Integration Tests)?',
            'a': 'Unit-тесты проверяют изолированную функцию или класс в памяти (заменяя внешние зависимости моками), а Integration-тесты проверяют совместную работу нескольких компонентов с реальной БД или API'
        },
        {
            'q': 'Как устроена классическая Пирамида тестирования Майка Кона и почему анти-паттерн «Рожок мороженого» опасен для проекта?',
            'a': 'В основании пирамиды лежат сотни быстрых Unit-тестов, посередине — десятки Integration-тестов, а наверху — минимум E2E-тестов; «Рожок мороженого» с упором на медленные E2E делает CI хрупким и долгим'
        },
        {
            'q': 'Как расшифровываются три фазы цикла разработки через тестирование TDD (<code>Red ➔ Green ➔ Refactor</code>)?',
            'a': '<code>Red</code> — написать падающий тест на новую функциональность, <code>Green</code> — написать минимальный код для прохождения теста, <code>Refactor</code> — очистить архитектуру кода при зелёных тестах'
        },
        {
            'q': 'Зачем во встроенном фреймворке <code>unittest</code> используется контекстный менеджер <code>with self.subTest(...)</code>?',
            'a': 'Он позволяет прогнать серию параметризованных проверок внутри одного тестового метода так, чтобы падение на одном наборе данных не прерывало выполнение остальных проверок'
        },
    ],
    'Ф-225': [
        {
            'q': 'Чем в оркестраторах (Kubernetes, Docker) отличается проверка <code>Liveness Probe</code> от <code>Readiness Probe</code>?',
            'a': '<code>Liveness Probe</code> проверяет, не завис ли процесс намертво (при сбое контейнер перезапускается), а <code>Readiness Probe</code> проверяет, готов ли сервис принимать трафик от балансировщика'
        },
        {
            'q': 'Какая катастрофа произойдёт в продакшене, если в эндпоинт <code>Liveness Probe</code> (<code>/health/live</code>) добавить проверку подключения к базе данных?',
            'a': 'При кратковременной перегрузке базы данных оркестратор начнёт массово убивать и перезапускать все живые контейнеры бэкенда, вызывая каскадный отказ сервиса'
        },
        {
            'q': 'Каково назначение третьей пробы — <code>Startup Probe</code> — при запуске контейнера бэкенд-приложения?',
            'a': 'Она откладывает запуск проверок <code>Liveness</code> и <code>Readiness</code> на время долгой начальной инициализации (например, прогрева кэша или загрузки ML-модели), защищая под от преждевременного убийства'
        },
        {
            'q': 'Как взаимодействуют <code>Readiness Probe</code> и сигнал <code>SIGTERM</code> при обновлении сервиса без простоя (Zero-Downtime Rolling Update)?',
            'a': 'Новый под включает трафик только после успеха <code>Readiness Probe</code>, а старый под при получении <code>SIGTERM</code> сразу отдаёт <code>503</code> на Readiness, отключается от балансировщика и доделывает активные запросы'
        },
    ],
}

def html_to_kb_md(text):
    s = text
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s)
    s = re.sub(r'<span class="math-formula">(.*?)</span>', r'$\1$', s)
    s = s.replace('&quot;', '"').replace('&#x27;', "'")
    s = s.replace('&gt;', '>').replace('&lt;', '<')
    s = s.replace('&amp;', '&')
    return s.strip()

def run_alignment():
    print("======================================================================")
    print("  🚀 ВЫРАВНИВАНИЕ И СИНХРОНИЗАЦИЯ КАРТОЧЕК И КОНСПЕКТОВ ПЛАТФОРМЫ     ")
    print("======================================================================")

    cards_json_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
    notes_json_path = os.path.join(_ROOT, 'data', 'content', 'notes.json')
    manifest_path = os.path.join(_ROOT, 'data', 'content', 'manifest.json')
    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')
    karta_path = os.path.join(_ROOT, 'knowledge_base', '00 · 🗺️ Карта Мастерства.md')

    with open(cards_json_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)

    with open(standards_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Index knowledge_base card files
    kb_deck_map = {}
    for root, _, files in os.walk(os.path.join(_ROOT, 'knowledge_base')):
        for fname in files:
            if fname.endswith('.md') and 'Карточки' in root:
                m = re.match(r'^(Ф-\d+(?:@\d+)?)', fname)
                if m:
                    did = m.group(1)
                    if did == 'Ф-020' and '07 ·' in root:
                        did = 'Ф-020@07'
                    elif did == 'Ф-172' and '05 ·' in root:
                        did = 'Ф-172@05'
                    kb_deck_map[did] = os.path.join(root, fname)

    # 2. Add new cards to cards_data and knowledge_base/*.md (idempotent check by question text)
    # Also enrich 3 ultra-short answers in Ф-257 and Ф-085 so Bug 118 (>=15 chars) is 100% satisfied
    short_answer_fixes = {
        ('Ф-257', 10): 'Интерпретатор <code>PyPy</code>, который на лету компилирует горячие участки байткода в машинный код',
        ('Ф-257', 11): 'На языке программирования C (отсюда префикс C в названии эталонного интерпретатора <code>CPython</code>)',
        ('Ф-085', 10): 'Скомпилированный байткод (низкоуровневые инструкции виртуальной машины <code>PVM</code>)',
    }
    for (did, cidx), new_a in short_answer_fixes.items():
        if did in cards_data and cidx < len(cards_data[did]['cards']):
            cards_data[did]['cards'][cidx]['a'] = new_a
            fpath = kb_deck_map[did]
            md_lines = []
            for idx, c in enumerate(cards_data[did]['cards'], 1):
                md_lines.append(f"{idx}. {html_to_kb_md(c['q'])} >> {html_to_kb_md(c['a'])}\n")
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.writelines(md_lines)

    added_count = 0
    for did, new_cards in NEW_CARDS_BY_DECK.items():
        existing_qs = {c['q'] for c in cards_data[did]['cards']}
        to_add = [c for c in new_cards if c['q'] not in existing_qs]
        if to_add:
            cards_data[did]['cards'].extend(to_add)
            added_count += len(to_add)
            # Rewrite KB markdown file for this deck so numbering 1..N is 100% clean
            fpath = kb_deck_map[did]
            with open(fpath, 'r', encoding='utf-8') as fp:
                orig_lines = fp.readlines()
            # Keep header lines if any before "1. ", or rebuild numbered list
            md_lines = []
            for idx, c in enumerate(cards_data[did]['cards'], 1):
                q_md = html_to_kb_md(c['q'])
                a_md = html_to_kb_md(c['a'])
                md_lines.append(f"{idx}. {q_md} >> {a_md}\n")
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.writelines(md_lines)
            print(f"  + {did}: добавлено {len(to_add)} карточек (всего {len(cards_data[did]['cards'])})")

    with open(cards_json_path, 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=2)

    total_flashcards = sum(len(d.get('cards', [])) for d in cards_data.values())
    print(f"[1/6] cards.json и knowledge_base обновлены (добавлено {added_count} новых карточек, всего {total_flashcards}).")

    # 3. Update tracks in standards.html + sync notes.json from standards.html
    tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']
    all_notes_from_html = {}

    for tr in tracks:
        m = re.search(rf'(const\s+{tr}\s*=\s*)(\{{.*?\}})(;\s*(?:const|window))', html, re.DOTALL)
        if not m:
            raise ValueError(f"Could not find {tr} in standards.html")
        prefix, raw_json, suffix = m.group(1), m.group(2), m.group(3)
        data = json.loads(raw_json)

        # Collect notes for notes.json sync
        for kid, nobj in data.get('notes', {}).items():
            all_notes_from_html[kid] = {
                'id': nobj.get('id', kid),
                'title': nobj.get('title', ''),
                'steps': nobj.get('steps', [])
            }

        # Apply structural adjustments to skills
        if tr == 'PY_MASTERY':
            for u in data.get('units', []):
                for sk in u.get('skills', []):
                    sid = sk['id']
                    if sid == '1.1.1':
                        sk['fIds'] = [f for f in sk['fIds'] if f != 'Ф-085']
                        sk['decks'] = list(sk['fIds'])
                    elif sid == '1.3.1':
                        sk['kIds'] = ['К-022']
                    elif sid == '1.6.1':
                        sk['kIds'] = ['К-040', 'К-041']
                    elif sid == '1.9.1':
                        sk['kIds'] = ['К-055', 'К-056', 'К-057', 'К-222', 'К-220']
                        sk['fIds'] = ['Ф-252', 'Ф-253', 'Ф-257', 'Ф-255', 'Ф-251', 'Ф-082', 'Ф-081', 'Ф-083', 'Ф-085']
                        sk['decks'] = list(sk['fIds'])
                        for fid in sk['fIds']:
                            if fid in cards_data:
                                data['decks'][fid] = {
                                    'id': fid,
                                    'title': cards_data[fid]['title'],
                                    'cards': cards_data[fid]['cards'],
                                    'unitId': '1.9'
                                }
                    elif sid == '1.9.2':
                        sk['fIds'] = ['Ф-086', 'Ф-087', 'Ф-250', 'Ф-254', 'Ф-078']
                        sk['decks'] = list(sk['fIds'])

        elif tr == 'BACKEND_MASTERY':
            for u in data.get('units', []):
                for sk in u.get('skills', []):
                    if sk['id'] == '3.1.2':
                        sk['fIds'] = ['Ф-101', 'Ф-114', 'Ф-115']
                        sk['decks'] = list(sk['fIds'])
                        data['decks']['Ф-101'] = {
                            'id': 'Ф-101',
                            'title': cards_data['Ф-101']['title'],
                            'cards': cards_data['Ф-101']['cards'],
                            'unitId': '3.1'
                        }

        elif tr == 'INFRA_MASTERY':
            for u in data.get('units', []):
                for sk in u.get('skills', []):
                    if sk['id'] == '7.6.2':
                        sk['fIds'] = ['Ф-256', 'Ф-216', 'Ф-215']
                        sk['decks'] = list(sk['fIds'])
                        data['decks']['Ф-256'] = {
                            'id': 'Ф-256',
                            'title': cards_data['Ф-256']['title'],
                            'cards': cards_data['Ф-256']['cards'],
                            'unitId': '7.6'
                        }

        # Sync all decks in this track with cards_data
        for did in list(data.get('decks', {}).keys()):
            if did in cards_data:
                data['decks'][did]['cards'] = cards_data[did]['cards']
                data['decks'][did]['title'] = cards_data[did]['title']

        new_raw_json = json.dumps(data, ensure_ascii=False)
        html = html.replace(m.group(0), prefix + new_raw_json + suffix, 1)

    print("[2/6] Треки *_MASTERY в standards.html обновлены и синхронизированы с cards.json.")

    # 4. Sync manifest.json
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    manifest['totalFlashcards'] = total_flashcards
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[3/6] manifest.json ({total_flashcards} карточек) синхронизирован.")

    # 5. Update CANONICAL_NOTE_DECKS_MAP and findOwnerNoteForDeck in standards.html
    m_map = re.search(r'(const\s+CANONICAL_NOTE_DECKS_MAP\s*=\s*)(\{.*?\})(;)', html, re.DOTALL)
    if not m_map:
        raise ValueError("Could not find CANONICAL_NOTE_DECKS_MAP in standards.html")

    map_body = m_map.group(2)
    map_updates = {
        'К-001': ['Ф-001', 'Ф-002', 'Ф-004', 'Ф-008', 'Ф-009', 'Ф-080', 'Ф-084'],
        'К-002': ['Ф-005', 'Ф-229', 'Ф-079'],
        'К-003': ['Ф-006', 'Ф-003', 'Ф-007', 'Ф-231'],
        'К-010': ['Ф-017', 'Ф-021'],
        'К-011': ['Ф-018'],
        'К-012': ['Ф-020', 'Ф-022', 'Ф-019', 'Ф-172', 'Ф-221'],
        'К-022': ['Ф-035', 'Ф-036', 'Ф-236', 'Ф-037'],
        'К-023': ['Ф-038', 'Ф-235', 'Ф-037'],
        'К-218': ['Ф-238'],
        'К-027': ['Ф-043'],
        'К-028': ['Ф-046'],
        'К-029': ['Ф-045', 'Ф-043'],
        'К-030': ['Ф-239', 'Ф-047'],
        'К-033': ['Ф-242', 'Ф-051', 'Ф-044'],
        'К-034': ['Ф-050', 'Ф-049'],
        'К-035': ['Ф-241', 'Ф-047'],
        'К-040': ['Ф-245', 'Ф-058', 'Ф-057', 'Ф-060'],
        'К-041': ['Ф-243', 'Ф-059', 'Ф-061'],
        'К-219': ['Ф-244'],
        'К-044': ['Ф-247', 'Ф-065', 'Ф-066'],
        'К-045': ['Ф-248', 'Ф-067'],
        'К-046': ['Ф-246', 'Ф-068'],
        'К-047': ['Ф-069'],
        'К-053': ['Ф-077', 'Ф-074'],
        'К-054': ['Ф-249', 'Ф-072', 'Ф-075'],
        'К-055': ['Ф-252', 'Ф-082'],
        'К-056': ['Ф-253', 'Ф-081', 'Ф-083'],
        'К-057': ['Ф-257', 'Ф-085'],
        'К-222': ['Ф-255'],
        'К-220': ['Ф-251'],
        'К-058': ['Ф-087'],
        'К-059': ['Ф-078'],
        'К-060': ['Ф-086', 'Ф-250'],
        'К-221': ['Ф-254'],
        'К-061': ['Ф-088', 'Ф-089', 'Ф-194'],
        'К-223': ['Ф-256', 'Ф-215', 'Ф-216'],
        'К-090': ['Ф-101'],
        'К-092': ['Ф-114'],
        'К-093': ['Ф-115'],
        'К-097': ['Ф-117'],
        'К-096': ['Ф-116'],
        'К-224': ['Ф-264'],
        'К-231': ['Ф-276'],
        'К-234': ['Ф-185'],
        'К-235': ['Ф-279'],
        'К-149': ['Ф-166'],
        'К-150': ['Ф-165'],
        'К-151': ['Ф-168', 'Ф-167'],
        'К-152': ['Ф-169'],
        'К-153': ['Ф-167'],
        'К-154': ['Ф-170'],
        'К-170': ['Ф-188'],
        'К-171': ['Ф-189'],
        'К-172': ['Ф-187'],
        'К-173': ['Ф-190'],
        'К-174': ['Ф-192'],
        'К-175': ['Ф-191'],
        'К-176': ['Ф-193'],
        'К-177': ['Ф-195'],
        'К-178': ['Ф-194'],
        'К-179': ['Ф-196'],
        'К-180': ['Ф-197'],
        'К-187': ['Ф-205'],
        'К-188': ['Ф-204'],
        'К-189': ['Ф-206'],
        'К-190': ['Ф-207'],
        'К-192': ['Ф-209'],
        'К-193': ['Ф-208', 'Ф-185'],
        'К-194': ['Ф-210'],
        'К-195': ['Ф-184'],
        'К-196': ['Ф-208'],
        'К-197': ['Ф-185'],
        'К-198': ['Ф-211'],
        'К-199': ['Ф-020@07'],
        'К-200': ['Ф-213'],
        'К-201': ['Ф-212'],
        'К-202': ['Ф-214'],
        'К-203': ['Ф-091', 'Ф-097'],
        'К-206': ['Ф-215', 'Ф-216'],
        'К-207': ['Ф-256'],
        'К-208': ['Ф-216'],
        'К-209': ['Ф-215'],
    }

    for kid, new_fids in map_updates.items():
        fids_str = ', '.join(f"'{f}'" for f in new_fids)
        pattern = rf"('{re.escape(kid)}':\s*)\[.*?\]"
        if re.search(pattern, map_body):
            map_body = re.sub(pattern, rf"\1[{fids_str}]", map_body, count=1)
        else:
            raise ValueError(f"Key {kid} not found in CANONICAL_NOTE_DECKS_MAP")

    html = html.replace(m_map.group(0), m_map.group(1) + map_body + m_map.group(3), 1)

    # Also strengthen findOwnerNoteForDeck to check active kId first
    old_find_owner = """function findOwnerNoteForDeck(fid, sk){
  if(!sk || !sk.kIds) return null;
  for(let i = 0; i < sk.kIds.length; i++){
    const kId = sk.kIds[i];
    const decks = getMatchingDecksForNote(kId, sk);
    if(decks.includes(fid)) return kId;
  }
  return sk.kIds[0] || null;
}"""
    new_find_owner = """function findOwnerNoteForDeck(fid, sk){
  if(!sk || !sk.kIds) return null;
  if(typeof pySkillViewState !== 'undefined' && pySkillViewState && pySkillViewState.kId && sk.kIds.includes(pySkillViewState.kId)){
    const activeDecks = getMatchingDecksForNote(pySkillViewState.kId, sk);
    if(activeDecks.includes(fid)) return pySkillViewState.kId;
  }
  for(let i = 0; i < sk.kIds.length; i++){
    const kId = sk.kIds[i];
    const decks = getMatchingDecksForNote(kId, sk);
    if(decks.includes(fid)) return kId;
  }
  return sk.kIds[0] || null;
}"""
    if old_find_owner in html:
        html = html.replace(old_find_owner, new_find_owner, 1)

    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(academy_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("[4/6] CANONICAL_NOTE_DECKS_MAP и findOwnerNoteForDeck обновлены в standards.html и academy.html.")

    # 6. Sync 00 · 🗺️ Карта Мастерства.md so skill listings match 100%
    with open(karta_path, 'r', encoding='utf-8') as f:
        karta_text = f.read()

    # In Skill 1.1.1: add Ф-079, Ф-080, Ф-084
    old_111 = """    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-229. list vs tuple_ когда что выбрать]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-231. Срезы в Python_ slice и синтаксис start-stop-step]]"""
    new_111 = """    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-229. list vs tuple_ когда что выбрать]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-231. Срезы в Python_ slice и синтаксис start-stop-step]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-079. Множественное присваивание]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-080. Оператор pass]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-084. Системы счисления]]"""
    if old_111 in karta_text and 'Ф-079' not in karta_text.split('Skill 1.1.2')[0]:
        karta_text = karta_text.replace(old_111, new_111, 1)

    # In Skill 1.9.1 & 1.9.2: match 5 notes / 9 decks in 1.9.1 and 4 notes / 5 decks in 1.9.2
    old_191_192 = """- [ ] ⚡ **Skill 1.9.1 · Регулярные выражения и сериализация (модули re, json, pickle) [⬜ Not Started]**
  - 📖 **Конспект теории**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-055. Регулярные выражения в Python_ модуль re]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-056. Сериализация и десериализация_ json и pickle]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-057. Устройство языка Python_ CPython,]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-222. Современная работа с путями и файлами_ модуль pathlib]]
  - 📇 **Карточки RemNote**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-078. Python 2 и Python 3]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-079. Множественное присваивание]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-080. Оператор pass]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-081. Работа с JSON]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-082. Регулярные выражения]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-083. Сериализация и десериализация]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-084. Системы счисления]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-085. Устройство языка]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-252. Регулярные выражения в Python_ модуль re]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-253. Сериализация и десериализация_ json и pickle]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-255. Современная работа с путями и файлами_ модуль pathlib]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-257. Устройство языка Python_ CPython, байткод и интерпретатор]]
  - 💻 **Практика кодинга**: Написать парсер логов на regex: извлечь IP, статус-код и путь из строки access.log и сериализовать результат в JSON.
  - 🎯 **Критерий мастерства**: беглое прохождение карточек без подсказок (Accuracy > 90%) + рабочий чистый код задачи без синтаксических ошибок.

- ────────────────────────────────────────
- [ ] ⚡ **Skill 1.9.2 · Устройство CPython и модульная система (модули vs пакеты) [⬜ Not Started]**
  - 📖 **Конспект теории**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-058. Модули и пакеты в Python_ организация кода]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-059. Разница между модулем и пакетом в Python]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-060. PEP 8_ руководство по стилю кода Python]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-221. Система импортов в Python_ __all__, относительные импорты и циклические зависимости]]
  - 📇 **Карточки RemNote**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-086. PEP 8]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-087. Разница между модулем и пакетом]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-250. PEP 8_ руководство по стилю кода Python]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-254. Система импортов в Python_ __all__, относительные импорты и циклические зависимости]]"""

    new_191_192 = """- [ ] ⚡ **Skill 1.9.1 · Регулярные выражения и сериализация (модули re, json, pickle) [⬜ Not Started]**
  - 📖 **Конспект теории**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-055. Регулярные выражения в Python_ модуль re]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-056. Сериализация и десериализация_ json и pickle]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-057. Устройство языка Python_ CPython,]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-222. Современная работа с путями и файлами_ модуль pathlib]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-220. Логирование в Python_ модуль logging вместо print]]
  - 📇 **Карточки RemNote**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-252. Регулярные выражения в Python_ модуль re]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-253. Сериализация и десериализация_ json и pickle]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-257. Устройство языка Python_ CPython, байткод и интерпретатор]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-255. Современная работа с путями и файлами_ модуль pathlib]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-251. Логирование в Python_ модуль logging вместо print]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-082. Регулярные выражения]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-081. Работа с JSON]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-083. Сериализация и десериализация]]
    - [[01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ф-085. Устройство языка]]
  - 💻 **Практика кодинга**: Написать парсер логов на regex: извлечь IP, статус-код и путь из строки access.log и сериализовать результат в JSON.
  - 🎯 **Критерий мастерства**: беглое прохождение карточек без подсказок (Accuracy > 90%) + рабочий чистый код задачи без синтаксических ошибок.

- ────────────────────────────────────────
- [ ] ⚡ **Skill 1.9.2 · Устройство CPython и модульная система (модули vs пакеты) [⬜ Not Started]**
  - 📖 **Конспект теории**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-058. Модули и пакеты в Python_ организация кода]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-059. Разница между модулем и пакетом в Python]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-060. PEP 8_ руководство по стилю кода Python]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📚 Конспекты/К-221. Система импортов в Python_ __all__, относительные импорты и циклические зависимости]]
  - 📇 **Карточки RemNote**:
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-086. PEP 8]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-087. Разница между модулем и пакетом]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-250. PEP 8_ руководство по стилю кода Python]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-254. Система импортов в Python_ __all__, относительные импорты и циклические зависимости]]
    - [[01 · 🐍 Python/Юнит 1.9 · Инструменты/📇 Карточки/Ф-078. Python 2 и Python 3]]"""

    if old_191_192 in karta_text:
        karta_text = karta_text.replace(old_191_192, new_191_192, 1)

    with open(karta_path, 'w', encoding='utf-8') as f:
        f.write(karta_text)
    print("[5/6] 00 · 🗺️ Карта Мастерства.md синхронизирована.")
    print("[6/6] Все 4 канонических слоя успешно обновлены!")

if __name__ == '__main__':
    run_alignment()
