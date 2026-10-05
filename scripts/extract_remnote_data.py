import os, re, glob, json, html, ast, copy, textwrap

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLOUD_ROOT = r'C:\Users\fury6\OneDrive\Python_Backend_Academy'
_REL_REMNOTE = os.path.normpath(os.path.join(_HERE, '..', 'RemNote_Python_Mastery_FIXED'))
_REL_IDE_HTML = os.path.normpath(os.path.join(_HERE, '..', 'Практика кода — тренажёр с IDE.html'))

BASE_REMNOTE = _REL_REMNOTE if os.path.isdir(_REL_REMNOTE) else os.path.join(_CLOUD_ROOT, 'RemNote_Python_Mastery_FIXED')
IDE_HTML_PATH = _REL_IDE_HTML if os.path.isfile(_REL_IDE_HTML) else (
    os.path.join(_CLOUD_ROOT, 'Практика кода — тренажёр с IDE.html')
    if os.path.isfile(os.path.join(_CLOUD_ROOT, 'Практика кода — тренажёр с IDE.html'))
    else r'C:\Users\fury6\Downloads\Практика кода — тренажёр с IDE.html'
)

# 1. Load and enrich all 401 tasks from Практика кода — тренажёр с IDE.html
TIER_MAP = {
    1: '🥚 Уровень 1',
    2: '🐣 Уровень 2',
    3: '🐢 Уровень 3',
    4: '🦊 Уровень 4',
    5: '🦅 Уровень 5',
    6: '🦁 Уровень 6',
    7: '👑 Уровень 7',
}

def clean_ref_code(tid, c):
    c = c.replace('20_000_000', '200').replace('1_000_000', '1000').replace('100_000', '100')
    c = c.replace('acc.balance = -10     # ValueError', 'try:\n    acc.balance = -10\nexcept ValueError as _e:\n    print("ValueError перехвачен:", _e)')
    c = c.replace('u.age = "25"  # TypeError', 'try:\n    u.age = "25"\nexcept TypeError as _e:\n    print("TypeError перехвачен:", _e)')
    c = c.replace('s.temperature = 100  # ValueError', 'try:\n    s.temperature = 100\nexcept ValueError as _e:\n    print("ValueError перехвачен:", _e)')
    c = c.replace('acc.withdraw(Money(200))    # InsufficientFundsError', 'try:\n    acc.withdraw(Money(200))\nexcept InsufficientFundsError as _e:\n    print("InsufficientFundsError перехвачен:", _e)')
    if tid == 336:
        c = c.replace('while not stop_event.is_set():', 'for _ in range(2):')
    return c

def build_test_for_task(t):
    tid = t['id']
    c = clean_ref_code(tid, t['code'])
    tree = ast.parse(c)

    fns = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    assigns = []
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Name):
                    assigns.append((tg.id, n.value))
                elif isinstance(tg, ast.Tuple):
                    for el in tg.elts:
                        if isinstance(el, ast.Name):
                            assigns.append((el.id, None))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            assigns.append((n.target.id, n.value))

    top_asserts = [ast.get_source_segment(c, n) for n in tree.body if isinstance(n, ast.Assert)]
    test_fns = [n for n in fns if n.name.startswith('test_')]

    checks = []
    for fn in fns:
        fname = fn.name
        checks.append(f'assert "{fname}" in globals() and callable({fname}), "Функция {fname}() должна быть определена"')
        ref_body_is_pass = (
            len(fn.body) == 1 and (
                isinstance(fn.body[0], ast.Pass) or
                (isinstance(fn.body[0], ast.Expr) and isinstance(fn.body[0].value, ast.Constant) and fn.body[0].value.value is Ellipsis)
            )
        )
        if not ref_body_is_pass:
            checks.append(
                f'_fn_nodes_{fname} = [n for n in _ast.walk(_ast.parse(__USER_CODE__)) if isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and n.name == "{fname}"]\n'
                f'assert _fn_nodes_{fname} and not (len(_fn_nodes_{fname}[0].body) == 1 and isinstance(_fn_nodes_{fname}[0].body[0], _ast.Pass)), "Реализуйте тело функции {fname}() (сейчас там только pass)"'
            )

    for cl in classes:
        cname = cl.name
        checks.append(f'assert "{cname}" in globals() and isinstance({cname}, type), "Класс {cname} должен быть определён"')
        ref_cl_is_pass = (
            len(cl.body) == 1 and (
                isinstance(cl.body[0], ast.Pass) or
                (isinstance(cl.body[0], ast.Expr) and isinstance(cl.body[0].value, ast.Constant) and cl.body[0].value.value is Ellipsis)
            )
        )
        if not ref_cl_is_pass:
            checks.append(
                f'_cl_def_{cname} = [n for n in _ast.walk(_ast.parse(__USER_CODE__)) if isinstance(n, _ast.ClassDef) and n.name == "{cname}"]\n'
                f'assert _cl_def_{cname} and not (len(_cl_def_{cname}[0].body) == 1 and isinstance(_cl_def_{cname}[0].body[0], _ast.Pass)), "Реализуйте тело класса {cname} (сейчас там только pass)"'
            )
        for item in cl.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                mname = item.name
                checks.append(f'assert hasattr({cname}, "{mname}"), "В классе {cname} должен быть метод/свойство {mname}"')
                ref_m_is_pass = (
                    len(item.body) == 1 and (
                        isinstance(item.body[0], ast.Pass) or
                        (isinstance(item.body[0], ast.Expr) and isinstance(item.body[0].value, ast.Constant) and item.body[0].value.value is Ellipsis)
                    )
                )
                if not ref_m_is_pass:
                    checks.append(
                        f'_cl_nodes_{cname}_{mname} = [m for n in _ast.walk(_ast.parse(__USER_CODE__)) if isinstance(n, _ast.ClassDef) and n.name == "{cname}" for m in n.body if isinstance(m, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and m.name == "{mname}"]\n'
                        f'assert _cl_nodes_{cname}_{mname} and not (len(_cl_nodes_{cname}_{mname}[0].body) == 1 and isinstance(_cl_nodes_{cname}_{mname}[0].body[0], _ast.Pass)), "Реализуйте метод {cname}.{mname}()"'
                    )

    last_def_idx = -1
    for idx_n, n in enumerate(tree.body):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            last_def_idx = idx_n

    if last_def_idx >= 0:
        checks.append('if "r" in globals() and hasattr(r, "_store"): r._store.clear()')
        checks.append('if "r" in globals() and hasattr(r, "store"): r.store.clear()')
        checks.append('if "closed" in globals() and isinstance(closed, list): closed.clear()')
        checks.append('if "closed_resources" in globals() and isinstance(closed_resources, list): closed_resources.clear()')
        checks.append('if "sent_notifications" in globals() and isinstance(sent_notifications, list): sent_notifications.clear()')
        trailing_nodes = tree.body[last_def_idx + 1:]
        for tn in trailing_nodes:
            seg = ast.get_source_segment(c, tn)
            if seg:
                checks.append(seg)
        deleted_vars = set()
        for tn in trailing_nodes:
            for sub in ast.walk(tn):
                if isinstance(sub, ast.Delete):
                    for dt in sub.targets:
                        if isinstance(dt, ast.Name):
                            deleted_vars.add(dt.id)
        for tn in trailing_nodes:
            if isinstance(tn, ast.Assign):
                for tg in tn.targets:
                    if isinstance(tg, ast.Name) and not tg.id.startswith('_') and tg.id not in deleted_vars:
                        if not (isinstance(tn.value, ast.Constant) and tn.value.value is None):
                            checks.append(f'assert "{tg.id}" in globals(), "Переменная {tg.id} должна быть вычислена"')
    else:
        deleted_vars = set()
        for tn in tree.body:
            for sub in ast.walk(tn):
                if isinstance(sub, ast.Delete):
                    for dt in sub.targets:
                        if isinstance(dt, ast.Name):
                            deleted_vars.add(dt.id)
        for vname, val_node in assigns:
            if vname.startswith('_') or vname in deleted_vars:
                continue
            checks.append(f'assert "{vname}" in globals() and {vname} is not None, "Переменная {vname} должна быть определена и не равна None"')
            if isinstance(val_node, ast.Constant) and isinstance(val_node.value, str) and len(val_node.value.strip()) > 5:
                raw_s = val_node.value.strip()
                tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*', raw_s)
                important = [tok for tok in tokens if len(tok) >= 3][:3]
                for tok in important:
                    checks.append(f'assert isinstance({vname}, str) and "{tok}".lower() in {vname}.lower(), "Строка {vname} должна содержать ключевой элемент \'{tok}\'"')
            else:
                checks.append(f'assert {vname} != "__TODO__", "Заполните значение переменной {vname}"')
        for a_src in top_asserts:
            if a_src:
                checks.append(a_src)

    if test_fns:
        checks.append('''
_t_list = [(k, v) for k, v in list(globals().items()) if k.startswith("test_") and callable(v)]
assert len(_t_list) > 0, "Должна быть определена тестовая функция test_*"
_fix_map = {k: v for k, v in list(globals().items()) if callable(v) and getattr(v, "_is_fixture", False)}
for _tn, _tf in _t_list:
    _cases = [({}, "")]
    if hasattr(_tf, "_parametrize"):
        _pnames, _pvals = _tf._parametrize
        _cases = []
        for _ix, _pv in enumerate(_pvals):
            _raw = _pv.values if hasattr(_pv, "values") else (_pv if isinstance(_pv, (tuple, list)) else (_pv,))
            _cases.append((dict(zip(_pnames, _raw)), f"[{_ix}]"))
    _sig = list(_inspect.signature(_tf).parameters.keys())
    for _cargs, _csuf in _cases:
        _tds = []
        _kw = dict(_cargs)
        for _p in _sig:
            if _p in _kw: continue
            if _p == "tmp_path": _kw[_p] = _MemPath("/tmp/pytest_sandbox")
            elif _p == "monkeypatch":
                _mp = _MonkeyPatch(); _kw[_p] = _mp; _tds.append(_mp.undo)
            elif _p == "caplog": _kw[_p] = _CapLog()
            elif _p in _fix_map:
                _r = _fix_map[_p]()
                if hasattr(_r, "__next__"):
                    _kw[_p] = next(_r)
                    _tds.append(lambda g=_r: next(g, None))
                else: _kw[_p] = _r
        try:
            _tf(**_kw)
        finally:
            for _td in reversed(_tds): _td()
'''.strip())

    if tid in (7, 111, 165):
        checks.append('assert len([l for l in __USER_CODE__.splitlines() if l.strip() and not l.strip().startswith("# Задач") and not l.strip().startswith("# Напишите ваше") and not l.strip().startswith("from ") and not l.strip().startswith("import ")]) >= 1, "Добавьте решение задачи"')
    elif tid == 25:
        checks.append('assert len([n for n in _ast.walk(_ast.parse(__USER_CODE__)) if isinstance(n, _ast.FunctionDef) and n.name in ("get_by_id", "save")]) >= 2, "Опишите методы get_by_id и save в интерфейсе UserRepository"')
    elif tid == 296:
        checks.append('assert "content" in globals() and "Первая строка" in str(content), "Файл notes.txt должен быть записан и прочитан в переменную content"')

    functional_extra = {
        5: '_st = Stack(); _st.push(42); assert _st.peek() == 42 and _st.pop() == 42 and _st.is_empty()',
        9: '_p = Point2D(3, 4); assert "3" in repr(_p) and "4" in repr(_p)',
        13: 'assert is_palindrome("А роза упала на лапу Азора") is True and is_palindrome("hello") is False',
        14: 'assert binary_search([1, 3, 5, 7, 9], 7) == 3 and binary_search([1, 3, 5], 2) == -1',
        15: '_tn = TreeNode(10); assert _tn.val == 10 and _tn.left is None',
        16: 'assert analyze_complexity(4) == 36',
        17: '_wa = WeatherAdapter(ThirdPartyWeatherService()); assert _wa.get_celsius("Moscow") == 25.0',
        18: 'assert frequency_analysis(["a", "b", "a"])[0] == ("a", 2)',
        22: 'assert is_valid_username("alex123") is True and is_valid_username("ab") is False',
        23: '_t_obj = Temperature(25); assert _t_obj.celsius == 25',
        31: '_g = build_adjacency_list(3, [(0, 1), (1, 2)]); assert 1 in _g[0] and 0 in _g[1]',
        34: 'assert CourierStrategy().calculate(2) > PostStrategy().calculate(2)',
        36: '_ln = ListNode(5); assert _ln.val == 5',
        38: '@log_call\ndef _add(a, b): return a + b\nassert _add(2, 3) == 5',
        40: 'assert ThreadSafeSingleton() is ThreadSafeSingleton()',
        43: '_u = User("alex", "alex@test.com", 25); assert _u.username == "alex"',
        47: '_em = EventEmitter(); _res = []; _em.on("ev", lambda x: _res.append(x)); _em.emit("ev", 99); assert _res == [99]',
        49: 'assert apply_discount(100.0, 15.0) == 85.0',
        52: 'assert EventFactory.create_event("user_signup", {})["notify"] is True',
        55: '_cq = CircularQueue(2); assert _cq.enqueue(1) and _cq.enqueue(2) and not _cq.enqueue(3) and _cq.dequeue()',
        56: '_repo = InMemoryUserRepository(); _repo.save({"id": 1, "name": "A"}); assert _repo.get_by_id(1)["name"] == "A"',
        64: '_ll = LinkedList(); _ll.insert_at_head(1); _ll.insert_at_tail(2); assert _ll.head.val == 1 and _ll.head.next.val == 2',
        65: 'assert is_anagram("listen", "silent") is True and is_anagram("rat", "car") is False',
        69: '_h = ListNode(1, ListNode(2, ListNode(3))); _r = remove_nth_from_end(_h, 1); assert _r.val == 1 and _r.next.val == 2 and _r.next.next is None',
        71: '_arr = [1, 1, 2, 2, 3]; _k = remove_duplicates(_arr); assert _k == 3 and _arr[:3] == [1, 2, 3]',
        73: '_arr = [0, 1, 0, 3, 12]; move_zeroes(_arr); assert _arr == [1, 3, 12, 0, 0]',
        75: '_root = TreeNode(2, TreeNode(1), TreeNode(3)); assert inorder_traversal(_root) == [1, 2, 3]',
        76: 'assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4] and search_range([5, 7], 6) == [-1, -1]',
        77: 'assert bfs({"A": ["B", "C"], "B": ["D"], "C": [], "D": []}, "A") == ["A", "B", "C", "D"]',
        80: '_r = TreeNode(6, TreeNode(2), TreeNode(8)); assert lowest_common_ancestor(_r, _r.left, _r.right) is _r',
        81: 'assert AppConfig() is AppConfig()',
        82: 'assert is_valid_brackets("()[]{}") is True and is_valid_brackets("(]") is False',
        89: 'assert two_sum([2, 7, 11, 15], 9) == [0, 1]',
        108: '_r = TreeNode(1, TreeNode(2, TreeNode(3)), None); assert max_depth(_r) == 3',
        114: '_h = ListNode(1, ListNode(2)); _rev = reverse_list(_h); assert _rev.val == 2 and _rev.next.val == 1',
        137: '_h = ListNode(1, ListNode(2, ListNode(3))); assert find_middle(_h).val == 2',
        153: '_r = TreeNode(2, TreeNode(1), TreeNode(3)); assert is_valid_bst(_r) is True',
        161: '_r = insert_into_bst(None, 5); _r = insert_into_bst(_r, 3); assert _r.val == 5 and _r.left.val == 3',
        179: '_h = ListNode(1, ListNode(2)); assert has_cycle(_h) is False',
        188: '_l1 = ListNode(1, ListNode(3)); _l2 = ListNode(2, ListNode(4)); _m = merge_two_lists(_l1, _l2); assert _m.val == 1 and _m.next.val == 2',
        198: '_r = TreeNode(1, TreeNode(2), TreeNode(2)); assert is_symmetric(_r) is True',
        207: '_r = TreeNode(2, TreeNode(1), TreeNode(3)); assert inorder_iterative(_r) == [1, 2, 3]',
    }
    if tid in functional_extra:
        checks.append(functional_extra[tid])

    return 'import ast as _ast\n' + '\n'.join(checks)

def build_starter_for_task(t):
    tid = t['id']
    c = clean_ref_code(tid, t['code'])
    tree = ast.parse(c)
    lines = [f"# Задача #{tid}: {t['title']}"]

    last_def_idx = -1
    for idx_n, n in enumerate(tree.body):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            last_def_idx = idx_n

    if last_def_idx >= 0:
        for idx_n, n in enumerate(tree.body[:last_def_idx + 1]):
            if isinstance(n, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
                seg = ast.get_source_segment(c, n)
                if seg:
                    lines.append(seg)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                n_copy = copy.deepcopy(n)
                n_copy.body = [ast.Pass()]
                unparsed = ast.unparse(n_copy).replace('\n    pass', '\n    # TODO: реализуйте функцию\n    pass')
                lines.append(unparsed + '\n')
            elif isinstance(n, ast.ClassDef):
                n_copy = copy.deepcopy(n)
                methods = [m for m in n_copy.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
                if methods and tid != 25:
                    new_body = []
                    for item in n_copy.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            item.body = [ast.Pass()]
                            new_body.append(item)
                    n_copy.body = new_body or [ast.Pass()]
                else:
                    n_copy.body = [ast.Pass()]
                unparsed = ast.unparse(n_copy)
                lines.append(unparsed + '\n')
    else:
        for n in tree.body:
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                seg = ast.get_source_segment(c, n)
                if seg:
                    lines.append(seg)
        seen_vars = []
        for n in tree.body:
            if isinstance(n, ast.Assign):
                for tg in n.targets:
                    if isinstance(tg, ast.Name) and not tg.id.startswith('_') and tg.id not in seen_vars:
                        seen_vars.append(tg.id)
                    elif isinstance(tg, ast.Tuple):
                        for el in tg.elts:
                            if isinstance(el, ast.Name) and not el.id.startswith('_') and el.id not in seen_vars:
                                seen_vars.append(el.id)
            elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and not n.target.id.startswith('_'):
                if n.target.id not in seen_vars:
                    seen_vars.append(n.target.id)
        if seen_vars:
            lines.append('# Заполните значения целевых переменных:')
            for v in seen_vars:
                lines.append(f'{v} = None  # TODO')
        else:
            lines.append('# Напишите ваше решение ниже:')

    return '\n'.join(lines)

_TASK_OVERRIDES = {
    20: {
        'title': 'Разворот списка срезом [::-1]',
        'desc': '<p><strong>Задание:</strong> Создайте исходный список чисел <code>original</code> и получите его инвертированную копию <code>reversed_list</code> с помощью шага среза <code>[::-1]</code>.</p>',
        'starter_header': '# Задача #20: Разворот списка срезом',
    }
}

with open(IDE_HTML_PATH, encoding='utf-8') as f:
    ide_content = f.read()
tasks_match = re.search(r'const TASKS = (\[[\s\S]*?\]);\n', ide_content)
if tasks_match:
    TASKS_381 = json.loads(tasks_match.group(1))
else:
    ide_lines = ide_content.split('\n')
    TASKS_381 = json.loads(ide_lines[317].strip()[len('const TASKS = '):-1])
for _t in TASKS_381:
    _lvl = _t.get('level', 1)
    _t['tier'] = TIER_MAP.get(_lvl, f'🥚 Уровень {_lvl}')
    _t['topic'] = '🐍 Python Core' if 240 <= _t['id'] <= 381 else '🌐 Backend & SQL'
    if _t['id'] in _TASK_OVERRIDES:
        _ov = _TASK_OVERRIDES[_t['id']]
        if 'title' in _ov: _t['title'] = _ov['title']
    _code = clean_ref_code(_t['id'], _t.get('code', ''))
    _t['code'] = _code
    _t['solution'] = _code
    _t['initialCode'] = build_starter_for_task(_t)
    if _t['id'] in _TASK_OVERRIDES and 'starter_header' in _TASK_OVERRIDES[_t['id']]:
        _hdr = _TASK_OVERRIDES[_t['id']]['starter_header']
        _t['initialCode'] = re.sub(r'^# Задача #\d+:.*', _hdr, _t['initialCode'])
    _doc_m = re.search(r'"""(.*?)"""', _code, re.S)
    if _t['id'] in _TASK_OVERRIDES and 'desc' in _TASK_OVERRIDES[_t['id']]:
        _t['desc'] = _TASK_OVERRIDES[_t['id']]['desc']
    else:
        _t['desc'] = f"<p><strong>Задание:</strong> {html.escape(_t['title'])}.</p>" + (
            f"<p class='meta'>{html.escape(_doc_m.group(1).strip())}</p>" if _doc_m else ""
        )
    _t['hint'] = f"Обрати внимание на сигнатуру и инварианты задачи «{_t['title']}» ({_t['tier']})."
    _t['tests'] = build_test_for_task(_t)

TASKS_BY_ID = {t['id']: t for t in TASKS_381}


_DECK_TITLE_OVERRIDES = {
    'Ф-009': 'Сложность: основные операции для list, dict, set',
    'Ф-032': 'Области видимости переменных: global и nonlocal',
    'Ф-050': 'ООП: Декораторы @classmethod, @staticmethod, @property',
    'Ф-072': 'Модуль asyncio, async/await, корутины и event loop',
    'Ф-073': 'Параллелизм: разница между CPU-bound и IO-bound',
    'Ф-091': 'Безопасность сети: HTTPS и протоколы TLS/SSL',
    'Ф-097': 'Веб-серверы: Middleware (промежуточные обработчики запросов и логов)',
    'Ф-128': 'Сложность: Временная и пространственная сложность',
    'Ф-131': 'Структуры данных: Связный список (односвязный, двусвязный)',
    'Ф-147': 'SQL: Агрегатные функции COUNT, SUM, AVG, MIN, MAX',
    'Ф-150': 'SQL: Оконные функции ROW_NUMBER, RANK, PARTITION BY',
    'Ф-152': 'Проектирование БД: Нормализация (1НФ, 2НФ, 3НФ)',
    'Ф-153': 'Проектирование БД: Первичный ключ, внешний ключ',
    'Ф-154': 'Проектирование БД: Связи 1:1, 1:N, M:N',
    'Ф-155': 'Проектирование БД: Уникальные ограничения, NOT NULL, CHECK',
    'Ф-158': 'Оптимизация: Индексы — что такое, виды, когда помогают',
    'Ф-169': 'NoSQL: Что такое Redis, кейсы использования, типы данных',
    'Ф-175': 'Принципы: Separation of Concerns (Разделение ответственности)',
    'Ф-176': 'Архитектура: Layered Architecture (Слоистая архитектура)',
    'Ф-020@07': 'Linux: Работа с файлами — ls, cd, cp, mv, rm, grep, find, права (chmod, chown)',
    'Ф-184': 'Linux: Переменные окружения (env, export, .env, python-dotenv)',
    'Ф-185': 'Безопасность: Хранение секретов (.env, переменные окружения, Vault)',
    'Ф-186': 'Очереди сообщений: Архитектура брокеров (RabbitMQ vs Apache Kafka)',
    'Ф-187': 'Git: Временное хранилище git stash (push, pop, apply, list)',
    'Ф-188': 'Git: Ветки и навигация (branch, switch, checkout, HEAD)',
    'Ф-189': 'Git: Слияние веток — git merge vs git rebase',
    'Ф-190': 'Git: Точечный перенос коммитов (git cherry-pick)',
    'Ф-191': 'Git: Анализ истории — git log, diff, blame, bisect',
    'Ф-192': 'Git: Конфликты слияния (Merge Conflicts) и их разрешение',
    'Ф-193': 'Git: Базовый цикл (init, clone, status, add, commit, push, pull)',
    'Ф-194': 'Документация проекта: Структура продакшен-файла README.md',
    'Ф-195': 'Git: Стратегии ветвления (Gitflow, GitHub Flow, Trunk-Based)',
    'Ф-196': 'Git: Командная работа — Pull Request и культура Code Review',
    'Ф-197': 'Git: Файл .gitignore — синтаксис, шаблоны и типичные исключения',
    'Ф-198': 'Docker: Dockerfile — FROM, WORKDIR, COPY, RUN, ENV, EXPOSE, CMD vs ENTRYPOINT',
    'Ф-199': 'Docker: Архитектура образов (Images), слоёв и контейнеров (Containers)',
    'Ф-200': 'Docker: Оркестрация сервисов в Docker Compose (docker-compose.yml)',
    'Ф-201': 'Docker: Основные команды CLI (run, ps, exec, logs, build, images)',
    'Ф-202': 'Docker: Контекст сборки и файл .dockerignore',
    'Ф-203': 'Docker: Контейнеры против виртуальных машин (Namespaces и cgroups)',
    'Ф-204': 'Docker: Реестры образов (Docker Hub, GHCR) и версионирование тегов',
    'Ф-205': 'Docker: Многоэтапная сборка (Multi-stage build) и оптимизация веса',
    'Ф-206': 'Docker: Сети (bridge, host, none) и встроенный DNS-резолвинг',
    'Ф-207': 'Docker: Volumes и монтирование данных (bind mounts vs named volumes)',
    'Ф-208': 'CI/CD: Конфигурация пайплайнов в GitHub Actions и GitLab CI',
    'Ф-209': 'CI/CD: Основы непрерывной интеграции (CI) и доставки (CD)',
    'Ф-210': 'CI/CD: Пайплайны и качество кода (lint → test → build → deploy)',
    'Ф-211': 'Linux: Базовые команды и навигация в терминале',
    'Ф-212': 'Linux: Потоки ввода-вывода (stdin, stdout, stderr), конвейеры (pipes |) и перенаправление (>, >>)',
    'Ф-213': 'Linux: Управление процессами и сигналами (ps, top, kill, SIGTERM vs SIGKILL)',
    'Ф-214': 'Linux: SSH и удалённый доступ (ключи, ~/.ssh/config, scp)',
    'Ф-215': 'Тестирование: Фреймворк pytest (фикстуры, параметризация, плагины)',
    'Ф-216': 'Тестирование: Стандартный модуль unittest и unittest.mock',
    'Ф-217': 'Очереди задач: Celery — воркеры, брокеры (Redis/RabbitMQ) и задачи (@app.task)',
    'Ф-218': 'Очереди задач: Отправка email, генерация отчётов и обработка файлов асинхронно',
    'Ф-219': 'Логирование и мониторинг: модуль logging, хендлеры и форматтеры',
    'Ф-220': 'Логирование и мониторинг: уровни логов (DEBUG, INFO, WARNING, ERROR, CRITICAL)',
    'Ф-221': 'Отладка и диагностика: стектрейсы, pdb, breakpoint() и логирование',
    'Ф-222': 'Фоновые задачи: FastAPI BackgroundTasks против очередей Celery',
    'Ф-223': 'Очереди задач: Интеграция Celery и Redis с проектом Django',
    'Ф-224': 'Логирование и мониторинг: трекинг ошибок в Sentry (DSN, breadcrumbs, контекст)',
    'Ф-225': 'Логирование и мониторинг: метрики Prometheus (Counter, Gauge, Histogram) и Health Checks',
}

_NOTE_TITLE_OVERRIDES = {
    'К-111': 'Статический и динамический массив: как работает память и list',
    'К-116': 'Куча (Heap): быстрый доступ к минимуму и модуль heapq',
    'К-123': 'Динамическое программирование: мемоизация и табуляция',
}

def _clean_display_title(s: str) -> str:
    s = s.replace('_:=_', '(:=):').replace('I_O', 'I/O').replace('async_await', 'async/await').replace('try_except_else_finally', 'try/except/else/finally')
    s = re.sub(r'(?<!_)_(?=\s|$)', ':', s)
    return s.strip()

# 2. Index all K-xxx and Ф-xxx files across RemNote_Python_Mastery_FIXED
k_files_map = {}
f_files_map = {}
f_files_by_relpath = {}
for root, dirs, files in os.walk(BASE_REMNOTE):
    dirs.sort()
    for fn in sorted(files):
        if fn.endswith('.md'):
            m = re.match(r'^([КФ]-\d+)\.\s*(.*)\.md$', fn)
            if m:
                cid, ctitle = m.group(1), _clean_display_title(m.group(2))
                full_p = os.path.join(root, fn)
                rel_p = os.path.relpath(full_p, BASE_REMNOTE).replace(os.sep, '/')
                mod_num = rel_p[:2]
                ctitle = _DECK_TITLE_OVERRIDES.get(f"{cid}@{mod_num}", _DECK_TITLE_OVERRIDES.get(cid, _NOTE_TITLE_OVERRIDES.get(cid, ctitle)))
                entry = {'id': cid, 'title': ctitle, 'path': full_p, 'relpath': rel_p, 'module': mod_num}
                if cid.startswith('К-'):
                    k_files_map[cid] = entry
                else:
                    f_files_by_relpath[rel_p] = entry
                    if cid not in f_files_map:
                        f_files_map[cid] = entry
                    else:
                        entry['id'] = f"{cid}@{mod_num}"
                        f_files_map[f"{cid}@{mod_num}"] = entry

print(f"Indexed {len(k_files_map)} K-notes and {len(f_files_map)} F-decks")

_LATEX_SUBS = [
    (r'\\implies', '⇒'),
    (r'\\iff', '⇔'),
    (r'\\to\b', '→'),
    (r'\\leftarrow\b', '←'),
    (r'\\approx', '≈'),
    (r'\\ll\b', '≪'),
    (r'\\gg\b', '≫'),
    (r'\\le\b', '≤'),
    (r'\\leq\b', '≤'),
    (r'\\ge\b', '≥'),
    (r'\\geq\b', '≥'),
    (r'\\neq\b', '≠'),
    (r'\\ne\b', '≠'),
    (r'\\times\b', '×'),
    (r'\\cdot\b', '·'),
    (r'\\infty\b', '∞'),
    (r'\\pm\b', '±'),
    (r'\\cap\b', '∩'),
    (r'\\cup\b', '∪'),
    (r'\\setminus\b', '∖'),
    (r'\\in\b', '∈'),
    (r'\\notin\b', '∉'),
    (r'\\lambda\b', 'λ'),
    (r'\\alpha\b', 'α'),
    (r'\\beta\b', 'β'),
    (r'\\Delta\b', 'Δ'),
    (r'\\Theta\b', 'Θ'),
    (r'\\Omega\b', 'Ω'),
    (r'\\ldots\b', '…'),
    (r'\\dots\b', '…'),
    (r'\\left\s*', ''),
    (r'\\right\s*', ''),
    (r'\\log_2\b', 'log₂'),
    (r'\\log\b', 'log'),
    (r'\\min\b', 'min'),
    (r'\\max\b', 'max'),
    (r'\\%', '%'),
    (r'\\_', '_'),
    (r'\\,', ' '),
]

def _format_latex_expr(expr: str) -> str:
    s = expr.strip()
    s = re.sub(r'\\text\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'(\1) / (\2)', s)
    s = re.sub(r'\\lfloor\s*(.*?)\s*\\rfloor', r'⌊\1⌋', s)
    s = re.sub(r'\\lceil\s*(.*?)\s*\\rceil', r'⌈\1⌉', s)
    for pat, repl in _LATEX_SUBS:
        s = re.sub(pat, repl, s)
    s = re.sub(r'\^\{([^{}]+)\}', lambda m: f'^{m.group(1)}' if len(m.group(1)) == 1 or m.group(1).isalnum() else f'^({m.group(1)})', s)
    s = re.sub(r'_\{([^{}]+)\}', r'_\1', s)
    s = re.sub(r'\^2(?!\d)', '²', s)
    s = re.sub(r'\^3(?!\d)', '³', s)
    return s

def _align_python_inline_comments(raw_code: str) -> str:
    lines = raw_code.splitlines()
    parsed = []
    for ln in lines:
        s = ln.rstrip()
        # Look for inline comment (# not at start of trimmed line, not inside quotes)
        in_sq = False
        in_dq = False
        esc = False
        hash_pos = -1
        for idx, ch in enumerate(s):
            if esc:
                esc = False
                continue
            if ch == '\\':
                esc = True
                continue
            if ch == "'" and not in_dq:
                in_sq = not in_sq
            elif ch == '"' and not in_sq:
                in_dq = not in_dq
            elif ch == '#' and not in_sq and not in_dq:
                if s[:idx].strip():
                    hash_pos = idx
                break
        if hash_pos > 0:
            code_part = s[:hash_pos].rstrip()
            comment_part = '# ' + s[hash_pos + 1:].strip()
            parsed.append((code_part, comment_part))
        else:
            parsed.append((s, None))
    code_lengths = [len(cp) for cp, cm in parsed if cm is not None]
    if len(code_lengths) >= 2:
        max_len = min(max(code_lengths), 64)
        out_lines = []
        for cp, cm in parsed:
            if cm is not None and len(cp) <= max_len:
                pad = ' ' * (max_len - len(cp) + 2)
                out_lines.append(f"{cp}{pad}{cm}")
            elif cm is not None:
                out_lines.append(f"{cp}  {cm}")
            else:
                out_lines.append(cp)
        return '\n'.join(out_lines)
    return raw_code

# 3. Markdown to HTML converter for K-notes (splits into micro-step chunks!)
def md_inline(text):
    # Escape HTML first
    text = html.escape(text)
    # Protect inline code `...` with placeholders before LaTeX processing
    code_stash = []
    def _save_code(m):
        code_stash.append(f'<code>{m.group(1)}</code>')
        return f'\x00CODE{len(code_stash) - 1}\x00'
    text = re.sub(r'`([^`\n]+)`', _save_code, text)
    # Convert $$...$$ and $...$ math expressions into clean readable text
    text = re.sub(r'\$\$([^\$]+)\$\$', lambda m: _format_latex_expr(m.group(1)), text)
    text = re.sub(r'\$([^$\n]+)\$', lambda m: _format_latex_expr(m.group(1)), text)
    # Bold **...**
    text = re.sub(r'\*\*([^\*\n]+)\*\*', r'<strong>\1</strong>', text)
    # Italic *...*
    text = re.sub(r'(?<!\*)\*([^\*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    # Restore inline code
    for idx, c_html in enumerate(code_stash):
        text = text.replace(f'\x00CODE{idx}\x00', c_html)
    # Clean stray spaces before punctuation after </code> and inside parens ( <code>...</code> )
    text = re.sub(r'</code>\s+([,.;:?!])', r'</code>\1', text)
    text = re.sub(r'\(\s+<code>', r'(<code>', text)
    text = re.sub(r'</code>\s+\)', r'</code>)', text)
    return text

_NON_PY_PREFIX_RE = re.compile(
    r'^(SELECT|FROM|INSERT|UPDATE|DELETE|CREATE|ALTER|GET |POST |PUT |PATCH |HEAD |OPTIONS |HTTP/|pip |poetry |uvicorn |gunicorn |django-admin |pytest |python |curl |git |docker |alembic )'
)

def _is_runnable_python(code_lang, raw_code):
    if not raw_code or code_lang not in ('python', 'py', ''):
        return False
    if _NON_PY_PREFIX_RE.match(raw_code):
        return False
    try:
        ast.parse(raw_code)
        return True
    except SyntaxError:
        return False

def md_chunk_to_html(md_chunk, ctx_blocks=None):
    if ctx_blocks is None:
        ctx_blocks = []
    lines = md_chunk.strip().split('\n')
    out = []
    in_code = False
    code_lang = ''
    code_buf = []
    in_ul = False
    in_table = False
    table_rows = []
    in_bq = False
    bq_lines = []
    chunk_title = ''

    def flush_ul():
        nonlocal in_ul
        if in_ul:
            out.append('</ul>')
            in_ul = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            out.append('<table>')
            for r_idx, row in enumerate(table_rows):
                cells = [c.strip() for c in row.strip('|').split('|')]
                if all(re.match(r'^[-:\s]+$', c) for c in cells if c):
                    continue
                tag = 'th' if r_idx == 0 else 'td'
                out.append('<tr>' + ''.join(f'<{tag}>{md_inline(c)}</{tag}>' for c in cells) + '</tr>')
            out.append('</table>')
            table_rows = []
            in_table = False

    def flush_bq():
        nonlocal in_bq, bq_lines
        if in_bq and bq_lines:
            jr_txt = ''
            sr_txt = ''
            other_lines = []
            for bl in bq_lines:
                m_jr = re.match(r'^[-*]?\s*\*\*Junior[^*]*\*\*:\s*(.*)', bl)
                m_sr = re.match(r'^[-*]?\s*\*\*Senior[^*]*\*\*:\s*(.*)', bl)
                if m_jr:
                    jr_txt = m_jr.group(1).strip()
                elif m_sr:
                    sr_txt = m_sr.group(1).strip()
                elif not re.match(r'^\*\*Junior\s+vs\s+Senior\*\*:?$', bl, re.I):
                    other_lines.append(bl)
            if jr_txt and sr_txt:
                if other_lines:
                    out.append('<div class="notice">' + '<br>'.join(md_inline(x) for x in other_lines) + '</div>')
                out.append(
                    f'<div class="jvs-grid">'
                    f'<div class="jvs-box jvs-box--jr"><span class="jvs-title">❌ Подход Junior</span>{md_inline(jr_txt)}</div>'
                    f'<div class="jvs-box jvs-box--sr"><span class="jvs-title">✅ Подход Senior</span>{md_inline(sr_txt)}</div>'
                    f'</div>'
                )
            else:
                out.append('<div class="notice">' + '<br>'.join(md_inline(x) for x in bq_lines) + '</div>')
            bq_lines = []
            in_bq = False

    for line in lines:
        if line.strip().startswith('```'):
            flush_ul()
            flush_table()
            flush_bq()
            if not in_code:
                in_code = True
                code_lang = line.strip()[3:].strip().lower()
                code_buf = []
            else:
                in_code = False
                raw_code = textwrap.dedent('\n'.join(code_buf)).strip()
                if not raw_code:
                    continue
                is_py = _is_runnable_python(code_lang, raw_code)
                if is_py or code_lang in ('python', 'py', ''):
                    raw_code = _align_python_inline_comments(raw_code)
                esc_code = html.escape(raw_code)
                if is_py:
                    ctx_str = '\n'.join(ctx_blocks)
                    ctx_attr = f' data-ctx="{html.escape(ctx_str, quote=True)}"' if ctx_str else ''
                    run_btn = f'<div class="code-run-bar"><span class="mono meta">{code_lang or "python"}</span><button type="button" class="btn-inline-run" data-run-snippet="1"{ctx_attr}>▶ Запустить код</button></div>'
                    indented_ctx = '\n'.join('    ' + l for l in raw_code.splitlines())
                    ctx_blocks.append(f"try:\n{indented_ctx}\n    pass\nexcept Exception:\n    pass")
                else:
                    run_btn = ''
                out.append(f'<div class="snippet-wrap">{run_btn}<pre><code>{esc_code}</code></pre><div class="snippet-out hidden"></div></div>')
            continue

        if in_code:
            code_buf.append(line)
            continue

        s = line.strip()
        if not s:
            flush_ul()
            flush_table()
            flush_bq()
            continue

        if s.startswith('>') and not s.startswith('>>>') and not s.startswith('>>'):
            flush_ul()
            flush_table()
            in_bq = True
            bq_content = s[1:].strip()
            if bq_content:
                bq_lines.append(bq_content)
            continue
        else:
            flush_bq()

        if s.startswith('|') and s.endswith('|'):
            flush_ul()
            in_table = True
            table_rows.append(s)
            continue
        else:
            flush_table()

        if s.startswith('# '):
            flush_ul()
            t = s[2:].strip()
            if not chunk_title:
                chunk_title = re.sub(r'^[^\wА-Яа-яЁё]*К-\d+\.\s*', '', t).strip() or t
            out.append(f'<h4>{md_inline(t)}</h4>')
        elif s.startswith('## '):
            flush_ul()
            t = s[3:].strip()
            if not chunk_title:
                chunk_title = t
            out.append(f'<h4>{md_inline(t)}</h4>')
        elif s.startswith('### '):
            flush_ul()
            t = s[4:].strip()
            if not chunk_title:
                chunk_title = t
            out.append(f'<h4>{md_inline(t)}</h4>')
        elif s.startswith('- ') or s.startswith('* '):
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{md_inline(s[2:].strip())}</li>')
        elif re.match(r'^\d+\.\s+', s):
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            item_txt = re.sub(r'^\d+\.\s+', '', s)
            out.append(f'<li>{md_inline(item_txt)}</li>')
        else:
            flush_ul()
            out.append(f'<p>{md_inline(s)}</p>')

    flush_ul()
    flush_table()
    flush_bq()
    if in_code and code_buf:
        raw_tail = textwrap.dedent('\n'.join(code_buf)).strip()
        if raw_tail:
            out.append(f'<pre><code>{html.escape(raw_tail)}</code></pre>')

    return chunk_title or 'Ключевая концепция', '\n'.join(out)

def parse_k_note(cid):
    info = k_files_map[cid]
    with open(info['path'], encoding='utf-8') as f:
        txt = f.read()
    # Strip RemNote header line
    m_hdr = re.match(r'^📖 Перечитать конспект:\s*(.*?)\s*>>.*?\n+', txt)
    raw_hdr_title = _clean_display_title(m_hdr.group(1).strip()) if m_hdr else info['title']
    clean_title = _NOTE_TITLE_OVERRIDES.get(cid, raw_hdr_title)
    txt = re.sub(r'^📖 Перечитать конспект:.*?\n+', '', txt).strip()
    txt = re.sub(r'^---\s*\n+', '', txt).strip()
    raw_chunks = [c.strip() for c in re.split(r'\n---\n', txt) if c.strip()]
    steps = []
    ctx_blocks = []
    for idx, rc in enumerate(raw_chunks):
        stitle, shtml = md_chunk_to_html(rc, ctx_blocks=ctx_blocks)
        if shtml.strip():
            steps.append({'title': stitle, 'html': shtml})
    if not steps:
        steps.append({'title': clean_title, 'html': f'<p>{md_inline(clean_title)}</p>'})
    return {'id': cid, 'title': clean_title, 'steps': steps}


def parse_f_deck(fid, module=None):
    key = f"{fid}@{module}" if (module and f"{fid}@{module}" in f_files_map) else fid
    info = f_files_map[key]
    cards = []
    with open(info['path'], encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '>>' in line:
                m_sep = re.match(r'^((?:[^`]|`[^`]*`)+?)>>(.*)$', line)
                if m_sep:
                    q, a = m_sep.group(1), m_sep.group(2)
                else:
                    q, a = line.split('>>', 1)
                q = re.sub(r'^\d+\.\s*', '', q).strip()
                a = a.strip()
                if q and a:
                    cards.append({'q': md_inline(q), 'a': md_inline(a)})
    return {'id': key, 'title': info['title'], 'cards': cards}

# Test parsing all Mod 01 notes & cards
mod1_k_ids = [f"К-{i:03d}" for i in range(1, 62)] + [f"К-{i:03d}" for i in range(217, 224)]
parsed_notes = {cid: parse_k_note(cid) for cid in mod1_k_ids if cid in k_files_map}
print("Parsed Mod 01 notes:", len(parsed_notes), "total steps:", sum(len(n['steps']) for n in parsed_notes.values()))
