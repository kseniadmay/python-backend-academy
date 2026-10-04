# -*- coding: utf-8 -*-
import ast, re
import extract_remnote_data as _erd
from test_all_401_tasks import full_env_code

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

    # Collect top-level functions, classes, and assigned variables
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

    # Extract any existing top-level assert statements or test_ functions from reference code
    top_asserts = [ast.get_source_segment(c, n) for n in tree.body if isinstance(n, ast.Assert)]
    test_fns = [n for n in fns if n.name.startswith('test_')]

    checks = []
    # 1. Always verify student code is not just empty/pass/starter stub
    # Check defined functions
    for fn in fns:
        fname = fn.name
        checks.append(f'assert "{fname}" in globals() and callable({fname}), "Функция {fname}() должна быть определена"')
        # Check that function body is not just `pass` or `...` (unless reference itself is abstract/pass like task 25/96)
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

    # 2. Check defined classes and their methods
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


    # 3. Check if task has def/class or is a top-level variable/script task
    last_def_idx = -1
    for idx_n, n in enumerate(tree.body):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            last_def_idx = idx_n

    if last_def_idx >= 0:
        # Reset any module-level mutable accumulator lists or FakeRedis state before running trailing driver block
        checks.append('if "r" in globals() and hasattr(r, "_store"): r._store.clear()')
        checks.append('if "r" in globals() and hasattr(r, "store"): r.store.clear()')
        checks.append('if "closed" in globals() and isinstance(closed, list): closed.clear()')
        checks.append('if "closed_resources" in globals() and isinstance(closed_resources, list): closed_resources.clear()')
        checks.append('if "sent_notifications" in globals() and isinstance(sent_notifications, list): sent_notifications.clear()')
        # Include the entire trailing driver block after the last def/class so both
        # student code (only implementing def/class) and full reference code are tested!
        trailing_nodes = tree.body[last_def_idx + 1:]
        for tn in trailing_nodes:
            seg = ast.get_source_segment(c, tn)
            if seg:
                checks.append(seg)
        # Also verify any variables assigned in trailing_nodes are not None (unless deleted in trailing_nodes)
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
        # Pure top-level variable/script task (88 tasks)
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
                # Check that variable is not left as an empty placeholder ""
                checks.append(f'assert {vname} != "__TODO__", "Заполните значение переменной {vname}"')
        for a_src in top_asserts:
            if a_src:
                checks.append(a_src)

    # 5. If there are test_ functions, run them via the pytest runner!
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

    # 6. Special cases for comment-only / expression-only tasks (7, 25, 111, 165, 296)
    if tid in (7, 111, 165):
        checks.append('assert len([l for l in __USER_CODE__.splitlines() if l.strip() and not l.strip().startswith("# Задач") and not l.strip().startswith("# Напишите ваше") and not l.strip().startswith("from ") and not l.strip().startswith("import ")]) >= 1, "Добавьте решение задачи"')
    elif tid == 25:
        checks.append('assert len([n for n in _ast.walk(_ast.parse(__USER_CODE__)) if isinstance(n, _ast.FunctionDef) and n.name in ("get_by_id", "save")]) >= 2, "Опишите методы get_by_id и save в интерфейсе UserRepository"')
    elif tid == 296:
        checks.append('assert "content" in globals() and "Первая строка" in str(content), "Файл notes.txt должен быть записан и прочитан в переменную content"')

    # 7. Functional behavioral tests for pure functions/classes where reference didn't have top-level calls
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
    import copy
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


if __name__ == '__main__':
    import __main__, sys

    __runner_ref_failures = []
    __runner_starter_false_positives = []
    __runner_syntax_errors = []

    MP_HELPER = '''
import multiprocessing as _mp, concurrent.futures as _cf
class _SyncPool:
    def __init__(self, *a, **kw): pass
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def map(self, fn, it): return [fn(x) for x in it]
    def apply(self, fn, args=()): return fn(*args)
    def submit(self, fn, *a, **kw):
        class _Fut:
            def result(self_f): return fn(*a, **kw)
        return _Fut()
_mp.Pool = _SyncPool
class _SyncProc:
    def __init__(self, target=None, args=()): self.t = target; self.a = args
    def start(self):
        if self.t: self.t(*self.a)
    def join(self): pass
_mp.Process = _SyncProc
_cf.ProcessPoolExecutor = _SyncPool
_cf.as_completed = lambda futs: list(futs)
'''
    __runner_ns = __main__.__dict__
    sys._prelude_loaded = False
    exec(full_env_code, __runner_ns)
    exec(MP_HELPER, __runner_ns)
    __runner_base_snap = dict(__runner_ns)

    for __runner_t in _erd.TASKS_381:
        __runner_tid = __runner_t['id']
        __runner_test_code = build_test_for_task(__runner_t)
        __runner_ref_code = clean_ref_code(__runner_tid, __runner_t['code'])
        __runner_starter = build_starter_for_task(__runner_t)

        try:
            ast.parse(__runner_starter)
        except SyntaxError as se:
            __runner_syntax_errors.append((__runner_tid, str(se)))

        # Test 1: Reference code MUST PASS
        for __runner_k in list(__runner_ns.keys()):
            if __runner_k not in __runner_base_snap and not __runner_k.startswith('__runner_'):
                __runner_ns.pop(__runner_k, None)
        __runner_ns.update(__runner_base_snap)
        __runner_ns['r'] = __runner_ns['_FakeRedis']()
        __runner_ns['__USER_CODE__'] = __runner_ref_code
        try:
            exec(__runner_ref_code + '\n' + __runner_test_code, __runner_ns)
        except Exception as __runner_ex:
            __runner_ref_failures.append((__runner_tid, type(__runner_ex).__name__, str(__runner_ex)[:100], __runner_t['title']))

        # Test 2: Starter code MUST FAIL (or for Task 96 where function is mocked, pass 'pass')
        for __runner_k in list(__runner_ns.keys()):
            if __runner_k not in __runner_base_snap and not __runner_k.startswith('__runner_'):
                __runner_ns.pop(__runner_k, None)
        __runner_ns.update(__runner_base_snap)
        __runner_ns['r'] = __runner_ns['_FakeRedis']()
        __runner_bad = "pass" if __runner_tid == 96 else __runner_starter
        __runner_ns['__USER_CODE__'] = __runner_bad
        try:
            exec(__runner_bad + '\n' + __runner_test_code, __runner_ns)
            __runner_starter_false_positives.append((__runner_tid, __runner_t['title'], __runner_bad))
        except Exception:
            pass

    print(f"Starter syntax errors (should be 0): {len(__runner_syntax_errors)}")
    print(f"Reference solutions passing: {len(_erd.TASKS_381) - len(__runner_ref_failures)} / {len(_erd.TASKS_381)}")
    for rf in __runner_ref_failures:
        print("  REF FAIL:", rf)
    print(f"Starter code false positives (should be 0): {len(__runner_starter_false_positives)}")
    for sfp in __runner_starter_false_positives[:25]:
        print("  FALSE POSITIVE:", sfp)





