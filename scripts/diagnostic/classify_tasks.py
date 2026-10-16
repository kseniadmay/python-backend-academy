import json, re

with open(r'C:\Users\fury6\Downloads\Практика кода — тренажёр с IDE.html', encoding='utf-8') as f:
    lines = f.readlines()
tasks = json.loads(lines[317].strip()[len('const TASKS = '):-1])

# Print all tasks that are Python core (Units 1.1 - 1.9)
keywords_u1 = [
    ('1.1', r'срез|\[:|tuple|namedtuple|Counter|defaultdict|deque|frozenset|args|kwargs|распаков|walrus|:=|zip\(|id\(|словар|множеств|append|extend|индекс|файл|open\('),
    ('1.2', r'lambda|map\(|filter\(|замыкан|closure|nonlocal|global|LEGB|декоратор|wraps|lru_cache|partial|functools|по умолчанию|mutable default'),
    ('1.3', r'итератор|__iter__|__next__|yield|генератор|chunk|contextmanager|__enter__|__exit__|contextlib|itertools'),
    ('1.4', r'Point2D|__repr__|__str__|__init__|__new__|isinstance|issubclass|инкапсуляц|dunder|__eq__|__lt__|__add__|__len__|__getitem__|BankAccount'),
    ('1.5', r'Mixin|миксин|MRO|mro\(\)|super\(\)|метакласс|metaclass|SingletonMeta|__slots__|дескриптор|__get__|__set__|@property|@classmethod|@staticmethod'),
    ('1.6', r'dataclass|__post_init__|Protocol|TypeVar|Generic|typing|match|case|Enum| docstring'),
    ('1.7', r'try|except|finally|исключен|Exception|Error|deepcopy|copy\.copy|getrefcount|gc\.|слабых ссылок|weakref|== и is'),
    ('1.8', r'asyncio|gather|create_task|Semaphore|Event Loop|threading|Lock|multiprocessing|GIL|CPU-bound|корутин|async with|Future|Queue'),
    ('1.9', r'regex|re\.|json\.|pickle|pathlib|logging|pytest|fixture|parametrize|mock|monkeypatch|caplog|venv|poetry|PEP 8|импорт|байткод|dis\.')
]

for unit_id, pat in keywords_u1:
    matches = [t for t in tasks if re.search(pat, t['title'] + '\n' + t['code'], re.I)]
    print(f"Unit {unit_id}: {len(matches)} tasks -> sample IDs {[m['id'] for m in matches[:8]]}")
