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
                seen_t = []
                for tok in tokens:
                    if len(tok) >= 3 and tok.lower() not in [x.lower() for x in seen_t]: seen_t.append(tok)
                important = seen_t[:7] if len(seen_t) <= 7 else (seen_t[:4] + seen_t[-3:])
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
    functional_extra.update({2: 'assert parse_form_urlencoded(b"username=alex&grant_type=password") == {"username": "alex", "grant_type": "password"}, "Функция должна возвращать словарь распакованных form-data параметров"', 6: 'assert parsed.scheme == "https" and parsed.path == "/v1/users" and params.get("role") == ["admin"] and params.get("page") == ["2"], "Проверьте разбор URL через urlparse и parse_qs"', 9: '_p = Point2D(3, 4); assert "3" in repr(_p) and "4" in repr(_p)', 10: 'assert any(isinstance(n, (_ast.Assert, _ast.With)) for n in _ast.walk(_fn_nodes_test_singleton_identity[0])), "Тестовая функция должна содержать проверку assert"', 11: 'class _DummyCur:\n    def __init__(self): self.queries = []\n    def execute(self, q, p=None): self.queries.append((q, p))\n    def __enter__(self): return self\n    def __exit__(self, *a): pass\nclass _DummyConn:\n    def __init__(self): self.cur = _DummyCur(); self.entered = False\n    def cursor(self): return self.cur\n    def __enter__(self): self.entered = True; return self\n    def __exit__(self, *a): pass\n_dc = _DummyConn()\ntransfer_funds(_dc, 1, 2, 100.0)\nassert len(_dc.cur.queries) >= 2 and "UPDATE" in _dc.cur.queries[0][0].upper(), "transfer_funds должна выполнять два UPDATE-запроса внутри транзакции"', 13: 'assert is_palindrome("А роза упала на лапу Азора") is True and is_palindrome("hello") is False', 15: '_tn = TreeNode(10); assert _tn.val == 10 and _tn.left is None', 16: 'assert analyze_complexity(4) == 36', 18: 'assert frequency_analysis(["a", "b", "a"])[0] == ("a", 2)', 19: 'assert main_diagonal == [1, 5, 9], "Главная диагональ матрицы 3x3 должна быть равна [1, 5, 9]"', 20: 'assert reversed_list == [5, 4, 3, 2, 1], "Список reversed_list должен быть равен [5, 4, 3, 2, 1]"', 28: 'assert user_payload() == {"username": "test_user", "email": "test@example.com"} and any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_create_user[0])), "Фикстура user_payload должна возвращать словарь пользователя, а тест — проверять его через assert"', 33: 'try:\n    UserCreate(username="bob", email="bob@example.com", password="short")\n    assert False, "Пароль короче 8 символов должен вызывать ValueError"\nexcept ValueError:\n    pass', 38: '@log_call\ndef _add(a, b): return a + b\nassert _add(2, 3) == 5', 39: 'assert sub == "Developer", "Переменная sub должна содержать срез последних 9 символов (\'Developer\')"', 49: 'assert apply_discount(100.0, 15.0) == 85.0', 65: 'assert is_anagram("listen", "silent") is True and is_anagram("rat", "car") is False', 66: 'assert evens == [2, 4, 6, 8, 10], "Список evens должен содержать только чётные числа [2, 4, 6, 8, 10]"', 68: 'assert any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_username_validator[0])), "Параметризованный тест должен содержать проверку assert"', 71: '_arr = [1, 1, 2, 2, 3]; _k = remove_duplicates(_arr); assert _k == 3 and _arr[:3] == [1, 2, 3]', 72: 'assert (p.x, p.y, p.z) == (1.0, 2.5, -0.5) and hasattr(Point, "_fields"), "Создайте namedtuple Point и экземпляр p = Point(1.0, 2.5, -0.5)"', 73: '_arr = [0, 1, 0, 3, 12]; move_zeroes(_arr); assert _arr == [1, 3, 12, 0, 0]', 74: '_u_res = asyncio.run(fetch_user(1))\nassert isinstance(_u_res, dict) and _u_res.get("id") == 1, "fetch_user(1) должна возвращать словарь пользователя с id=1"', 75: '_root = TreeNode(2, TreeNode(1), TreeNode(3)); assert inorder_traversal(_root) == [1, 2, 3]', 80: '_r = TreeNode(6, TreeNode(2), TreeNode(8)); assert lowest_common_ancestor(_r, _r.left, _r.right) is _r', 89: 'assert two_sum([2, 7, 11, 15], 9) == [0, 1]', 93: '@timer\ndef _compute_test(x): return x * 3\nassert _compute_test(7) == 21 and _compute_test.__name__ == "_compute_test", "Декоратор @timer должен возвращать результат функции и сохранять __name__ через @wraps"', 105: 'assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2], "top_k_frequent([1,1,1,2,2,3], 2) должна вернуть [1, 2]"', 108: '_r = TreeNode(1, TreeNode(2, TreeNode(3)), None); assert max_depth(_r) == 3', 110: '_c_test = make_counter(); assert [_c_test(), _c_test(), _c_test()] == [1, 2, 3], "make_counter() должна возвращать замыкание-счётчик, выдающее 1, 2, 3"', 118: 'class _FakeQ:\n    def filter_by(self, **kw):\n        class _R:\n            def first(self_r): return {"order_id": kw.get("id")}\n        return _R()\nclass _FakeDB:\n    def query(self, model): return _FakeQ()\n_q_obj = GetOrderByIdQuery(order_id=42)\nassert _q_obj.order_id == 42 and GetOrderByIdHandler(_FakeDB()).handle(_q_obj) == {"order_id": 42}, "Проверьте GetOrderByIdQuery(order_id) и GetOrderByIdHandler.handle()"', 120: 'assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]], "three_sum([-1, 0, 1, 2, -1, -4]) должна вернуть [[-1, -1, 2], [-1, 0, 1]]"', 125: 'assert merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6], "merge_k_sorted_lists должна сливать K отсортированных списков в один отсортированный"', 135: '@repeat(num_times=3)\ndef _ping_rep(lst): lst.append(1); return len(lst)\n_acc_r = []\nassert _ping_rep(_acc_r) == 3 and len(_acc_r) == 3, "Декоратор @repeat(3) должен вызывать функцию 3 раза"', 150: 'assert max_sub_array_of_size_k(3, [2, 1, 5, 1, 3, 2]) == 9, "max_sub_array_of_size_k(3, [2, 1, 5, 1, 3, 2]) должна вернуть 9"', 151: 'import io as _io, contextlib as _cl\n_buf_mro = _io.StringIO()\nwith _cl.redirect_stdout(_buf_mro):\n    Service().ping()\n_mro_lines = [l.strip() for l in _buf_mro.getvalue().splitlines() if l.strip()]\nassert _mro_lines == ["Service.ping", "MixinA.ping", "MixinB.ping", "Base.ping"], f"Цепочка вызовов super().ping() по MRO должна вывести Service -> MixinA -> MixinB -> Base, получено: {_mro_lines}"', 153: '_r = TreeNode(2, TreeNode(1), TreeNode(3)); assert is_valid_bst(_r) is True', 161: '_r = insert_into_bst(None, 5); _r = insert_into_bst(_r, 3); assert _r.val == 5 and _r.left.val == 3', 162: 'with redirect_stdout() as _cap_buf:\n    print("captured_text")\nassert _cap_buf.getvalue().strip() == "captured_text", "redirect_stdout() должен перехватывать вывод print в StringIO-буфер"', 164: '_ht = SimpleHashTable(size=4)\n_ht.put("a", 10); _ht.put("b", 20); _ht.put("a", 99)\nassert _ht.get("a") == 99 and _ht.get("b") == 20, "SimpleHashTable должна сохранять, обновлять и возвращать значения по ключу"', 173: 'assert length_of_longest_substring("abcabcbb") == 3 and length_of_longest_substring("bbbbb") == 1, "length_of_longest_substring(\'abcabcbb\') должна вернуть 3"', 177: 'assert Vector2D(1, 2) + Vector2D(3, 4) == Vector2D(4, 6) and Vector2D(1, 2) != Vector2D(1, 3), "Проверьте работу операторов __add__ и __eq__ в Vector2D"', 185: '_mf = MedianFinder()\n_mf.add_num(1); _mf.add_num(2)\nassert _mf.find_median() == 1.5\n_mf.add_num(3)\nassert _mf.find_median() == 2.0, "MedianFinder должен корректно находить медиану для чётного и нечётного числа элементов"', 195: 'class _DummyCur2:\n    def __init__(self): self.queries = []\n    def execute(self, q, p=None): self.queries.append((q, p))\n    def __enter__(self): return self\n    def __exit__(self, *a): pass\nclass _DummyConn2:\n    def __init__(self): self.cur = _DummyCur2()\n    def cursor(self): return self.cur\n    def __enter__(self): return self\n    def __exit__(self, *a): pass\n_dc2 = _DummyConn2()\nsafe_transfer(_dc2, 20, 10, 50.0)\nassert len(_dc2.cur.queries) >= 4 and _dc2.cur.queries[0][1] == (10,) and _dc2.cur.queries[1][1] == (20,), "safe_transfer должна блокировать счета через SELECT ... FOR UPDATE в порядке возрастания ID (сначала 10, затем 20)"', 197: 'assert greet("User") == "<b><i>Hello, User</i></b>" and greet.__name__ == "greet", "Функция greet должна быть обёрнута в @bold и @italic с сохранением __name__ через @wraps"', 198: '_r = TreeNode(1, TreeNode(2), TreeNode(2)); assert is_symmetric(_r) is True', 200: 'assert isinstance(stats, dict) and "total_bonus" in stats, "stats должен быть словарём результата User.objects.aggregate(total_bonus=...)"', 203: 'assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49, "max_area([1,8,6,2,5,4,8,3,7]) должна вернуть 49"', 207: '_r = TreeNode(2, TreeNode(1), TreeNode(3)); assert inorder_iterative(_r) == [1, 2, 3]', 209: 'assert getattr(StandardResultsPagination, "page_size", None) == 3 and getattr(StandardResultsPagination, "max_page_size", None) == 100 and StandardResultsPagination().paginate_queryset(list(range(1, 11)), query_params={"page": 2, "page_size": 3}) == [4, 5, 6], "Настройте атрибуты page_size=3, page_size_query_param=\'page_size\', max_page_size=100"', 210: 'assert topological_sort(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in ([0, 1, 2, 3], [0, 2, 1, 3]) and topological_sort(2, [[1, 0], [0, 1]]) == [], "topological_sort должна возвращать топологический порядок узлов или [] при цикле"', 217: '_pg = prime_generator(); assert [next(_pg) for _ in range(10)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], "prime_generator() должен генерировать простые числа 2, 3, 5, 7..."', 218: '_lru = LRUCache(2)\n_lru.put(1, 10); _lru.put(2, 20)\nassert _lru.get(1) == 10\n_lru.put(3, 30)\nassert _lru.get(2) == -1 and _lru.get(3) == 30, "LRUCache должен вытеснять давно не использованный ключ (2) при превышении capacity"', 220: 'assert min_sub_array_len(7, [2, 3, 1, 2, 4, 3]) == 2 and min_sub_array_len(100, [1, 2, 3]) == 0, "min_sub_array_len(7, [2,3,1,2,4,3]) должна вернуть 2"', 227: '_pq = PriorityQueue()\n_pq.push("low", 10); _pq.push("high", 1); _pq.push("mid", 5)\nassert [_pq.pop(), _pq.pop(), _pq.pop()] == ["high", "mid", "low"], "PriorityQueue.pop() должен извлекать элементы в порядке возрастания числа priority"', 230: 'class _DummySess: pass\n_tx = Transaction(_DummySess())\nassert _tx.__enter__() is _tx.session and _tx.__exit__(None, None, None) is True and _tx.__exit__(ValueError, ValueError("err"), None) is False, "Transaction.__exit__ должен возвращать True при успехе и False при исключении"', 245: 'assert Dog("Рекс").speak() == "Рекс лает" and Cat("Мурка").speak() == "Мурка мяукает" and Animal("Существо").speak() == "Существо издаёт звук", "Проверьте методы speak() у классов Animal, Dog и Cat"', 253: 'assert (x, y, z) == (10, 20, 30) and x == 10 and y == 20 and z == 30, "Кортеж должен быть распакован в переменные x=10, y=20, z=30"', 255: 'assert first_three == [10, 20, 30] and last_two == [50, 60], "first_three должен быть [:3], last_two должен быть [-2:]"', 256: 'assert squares == [1, 4, 9, 16, 25], "squares должен содержать список квадратов чисел [1, 4, 9, 16, 25]"', 257: 'assert retries == 3 and config.get("timeout") == 30, "retries должен получить дефолтное значение 3"', 258: 'assert isinstance(point_list, list) and point_list == [99, 20], "Список point_list должен содержать [99, 20]"\nassert isinstance(point_tuple, tuple) and point_tuple == (10, 20), "Кортеж point_tuple должен быть (10, 20)"\nassert isinstance(cache, dict) and cache.get(point_tuple) == "запись в кэше", "Словарь cache должен содержать point_tuple как ключ со значением \'запись в кэше\'"', 260: 'assert hasattr(match, "group") and match.group() == "alex@example.com", "Переменная match должна содержать объект совпадения re.Match для \'alex@example.com\'"', 261: 'assert isinstance(json_string, str) and json.loads(json_string) == data and restored == data, "Проверьте сериализацию json.dumps(data) и десериализацию json.loads(json_string)"', 262: 'assert add_item("apple") == ["apple"] and add_item("banana") == ["banana"], "Функция add_item не должна сохранять элементы между вызовами по умолчанию"', 263: 'assert isinstance(access_levels, dict) and access_levels.get(permissions_read) == "гость" and access_levels.get(permissions_admin) == "администратор", "Словарь access_levels должен сопоставлять permissions_read -> \'гость\' и permissions_admin -> \'администратор\'"', 264: 'assert isinstance(user, dict) and len(user) >= 2 and "items" in __USER_CODE__, "Определите непустой словарь user и переберите его через user.items()"', 265: 'assert list(CountUp(5)) == [1, 2, 3, 4, 5], "Итератор CountUp(5) должен выдавать числа [1, 2, 3, 4, 5]"', 266: 'assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8], "Генератор fibonacci(7) должен выдавать [0, 1, 1, 2, 3, 5, 8]"', 267: 'assert isinstance(shallow, list) and isinstance(deep, list) and deep == [[1, 2, 77], [3, 4]] and original[0][:2] == [1, 2] and 77 not in original[0], "Глубокая копия deep не должна изменять вложенный список original"', 270: 'assert greet("Мир", greeting="Хай") == "Хай, Мир!", "Декоратор trace должен возвращать результат вызова функции greet"', 274: 'assert hasattr(match, "groupdict") and match.groupdict() == {"date": "2026-09-17", "time": "14:23:01", "level": "ERROR", "message": "Database connection failed"}, "Переменная match должна быть результатом re.match(pattern, log_line)"', 280: 'assert errors == [{"date": "2026-09-17", "time": "14:23:01", "level": "ERROR", "message": "Database connection failed"}, {"date": "2026-09-17", "time": "14:23:07", "level": "ERROR", "message": "Timeout on external API"}], "parse_errors(log_lines) должна выдавать словари для записей с уровнем ERROR"', 283: 'assert is_valid_username("alex123") is True and is_valid_username("a") is False, "Имя пользователя должно валидироваться регулярным выражением"', 286: 'assert dict(grouped) == {"a": ["apple", "avocado"], "b": ["banana", "blueberry"], "c": ["cherry"]}, "Сгруппируйте слова по первой букве в defaultdict(list)"', 287: 'assert isinstance(binary_data, (bytes, bytearray)) and isinstance(restored, User) and restored.name == "Alex" and restored.age == 30, "Проверьте сериализацию объекта User через pickle.dumps и загрузку через pickle.loads"', 290: '_seq = Sequence([10, 20, 30, 40, 50]); assert len(_seq) == 5 and _seq[1] == 20 and _seq[1:4] == [20, 30, 40] and _seq[::-1] == [50, 40, 30, 20, 10], "Класс Sequence должен поддерживать len() и срезы через __getitem__"', 291: 'assert add(2, 3) == 5, "Функция add(a, b) должна возвращать сумму a + b"', 295: '_cfg, _errs = parse_config(["DEBUG=true", "# comment", "PORT=8080", "bad line"]); assert _cfg == {"DEBUG": "true", "PORT": "8080"} and len(_errs) == 1 and "bad line" in _errs[0], "Проверьте разбор валидных пар KEY=VALUE и сбор ошибок в parse_config()"', 297: 'assert isinstance(cart, list) and "banana" in cart and "cherry" in cart and "date" in cart and len(cart) >= 4, "Дополните список cart через append и extend"', 298: 'assert isinstance(data, list) and len(data) > 3 and any(isinstance(n, _ast.NamedExpr) for n in _ast.walk(_ast.parse(__USER_CODE__))), "Определите список data (длиной > 3) и используйте моржовый оператор :="', 299: 'assert best_name == "Bob" and best_score == 92, "Лучший студент должен быть best_name=\'Bob\', best_score=92"', 300: 'assert a == [1, 2, 3] and b is a and c == a and c is not a, "b должна ссылаться на тот же список (b = a), а c должна быть независимой копией (c = a.copy())"', 301: 'assert count == 3, "Количество непустых строк count должно быть равно 3"', 302: 'assert emails == ["alex@example.com", "nina@test.org"] and any(isinstance(n, _ast.NamedExpr) for n in _ast.walk(_ast.parse(__USER_CODE__))), "Список emails должен быть равен [\'alex@example.com\', \'nina@test.org\'] с использованием :="', 303: '_pl = Playlist(["Song A", "Song B", "Song C"]); assert len(_pl) == 3 and ("Song B" in _pl) is True and ("Song X" in _pl) is False and _pl[0] == "Song A", "Проверьте реализацию __len__, __contains__ и __getitem__ в классе Playlist"', 304: 'assert [tuple(r) for r in transposed] == [(1, 4), (2, 5), (3, 6)], "Транспонированная матрица должна содержать [(1, 4), (2, 5), (3, 6)]"', 305: 'assert merge_unique_lines("a.txt", "b.txt") == ["error: timeout", "error: 404", "error: 500"], "merge_unique_lines должна возвращать список уникальных непустых строк с сохранением порядка"', 306: 'assert hasattr(BankAccount, "_BankAccount__balance") or "_BankAccount__balance" in BankAccount(100).__dict__, "Атрибут баланса должен использовать name mangling __balance"', 307: '_tr = Tracked("demo"); assert isinstance(_tr, Tracked) and getattr(_tr, "name", None) == "demo", "__new__ должен возвращать super().__new__(cls), а __init__ — сохранять self.name = name"', 308: 'assert Temperature(0).to_fahrenheit() == 32.0 and Temperature(100).to_fahrenheit() == 212.0, "to_fahrenheit() должен переводить градусы Цельсия по формуле C * 9 / 5 + 32"', 309: 'assert callable(greet) and greet("мир") == "Привет, мир!", "Функция greet(name) должна возвращать приветственную строку"', 310: 'assert slow_square(4) == 16 and slow_square(4) == 16 and hasattr(slow_square, "cache_info") and slow_square.cache_info().hits >= 1, "Функция slow_square(n) должна возвращать n ** 2 и быть обёрнута в @lru_cache"', 313: 'assert len(funcs_broken) == 3 and [f() for f in funcs_broken] == [2, 2, 2] and len(funcs_fixed) == 3 and [f() for f in funcs_fixed] == [0, 1, 2], "funcs_broken должен возвращать [2, 2, 2], а funcs_fixed с lambda i=i: i — [0, 1, 2]"', 314: 'assert power(2, 3) == 8 and square(5) == 25 and cube(2) == 8, "power(base, exponent) должна возвращать base ** exponent, а square и cube — фиксировать exponent=2 и exponent=3 через partial"', 315: '_inc_fn = make_counter(); assert [_inc_fn(), _inc_fn()] == [1, 2] and counter >= 2, "increment_global() должна увеличивать глобальный counter, а make_counter() — возвращать замыкание с nonlocal count"', 316: '_acc = Account("Alex", 100); assert _acc.owner == "Alex" and _acc._balance == 100 and _acc._Account__pin == "1234", "В Account.__init__ задайте self.owner = owner, self._balance = balance и self.__pin = \'1234\'"', 317: '_pt = Point(1, 2); assert repr(_pt) == "Point(x=1, y=2)" and str(_pt) == "Point(x=1, y=2)", "Point.__repr__ должен возвращать \'Point(x=1, y=2)\'"', 318: 'assert Money(100) == Money(100) and getattr(Money, "__hash__", None) is None, "Переопределение __eq__ без __hash__ в Money должно обнулять __hash__"\nassert MoneyFixed(100) == MoneyFixed(100) and hash(MoneyFixed(100)) == hash(100), "В MoneyFixed должны быть согласованно реализованы __eq__ и __hash__"', 322: 'assert add(2, 3) == 5 and greet("Алекс") == "Привет, Алекс!", "Декоратор @announce должен возвращать результат декорируемой функции"', 323: 'assert add(5, 3) == 8 and sub(5, 3) == 2 and mul(5, 3) == 15, "Функции add, sub, mul должны возвращать сумму, разность и произведение"', 324: '_calls_324 = []\n@repeat(3)\ndef _test_rep324(): _calls_324.append(1)\n_test_rep324()\nassert len(_calls_324) == 3, "Декоратор @repeat(3) должен выполнять функцию 3 раза"', 325: '_d = make_multiplier(2); _t = make_multiplier(3); assert _d(5) == 10 and _t(5) == 15, "make_multiplier(factor) должна возвращать функцию, умножающую аргумент на factor"', 326: 'assert text().lower() == "<b><i>привет</i></b>", "Двойной декоратор @bold и @italic над text() должен вернуть \'<b><i>Привет</i></b>\'"', 327: 'assert list(only_positive(double_values(numbers(5)))) == [2, 4, 6, 8], "Конвейер генераторов only_positive(double_values(numbers(5))) должен выдавать [2, 4, 6, 8]"', 328: '_pr = primes(); assert [next(_pr) for _ in range(5)] == [2, 3, 5, 7, 11], "Бесконечный генератор primes() должен выдавать первые 5 простых чисел [2, 3, 5, 7, 11]"', 331: 'with DatabaseConnection() as _dbc:\n    assert getattr(_dbc, "connected", False) is True, "Внутри блока with атрибут db.connected должен быть True"\nassert getattr(_dbc, "connected", True) is False, "После выхода из блока with атрибут db.connected должен сбрасываться в False"', 335: 'assert hasattr(match, "group") and match.group("level") == "WARNING" and match.group("message") == "Диск заполнен на 90%", "Переменная match должна быть результатом re.match(pattern, log)"', 337: 'assert custom_encoder(datetime(2026, 9, 19, 10, 0)) == "2026-09-19T10:00:00", "custom_encoder должен сериализовать datetime через .isoformat()"', 339: 'assert sum_loop(10) == 45 and sum_builtin(10) == 45, "Функции sum_loop(n) и sum_builtin(n) должны возвращать сумму чисел от 0 до n-1"', 340: 'assert slow_function() == sum(i ** 2 for i in range(1000)), "slow_function() должна возвращать сумму квадратов чисел range(1000)"', 341: 'assert c1.count == 2 and c2.count == 1, "Счетчики независимых экземпляров c1 и c2 должны быть изолированы"', 342: '_res_obj = Resource("файл.txt"); assert getattr(_res_obj, "name", None) == "файл.txt", "В Resource.__init__ сохраните self.name = name"', 343: 'assert rex.bark() == Dog.bark(rex) == "Рекс гавкает!", "Вызов rex.bark() и Dog.bark(rex) должны возвращать одинаковый результат"', 344: '_sc = ShoppingCart(); _sc.add("хлеб"); assert repr(_sc) == "ShoppingCart([\'хлеб\'])", "Метод ShoppingCart.__repr__ должен возвращать строку вида ShoppingCart([\'хлеб\'])"', 345: 'assert repr(Age(25)) == "Age(25)"\ntry:\n    Age(-5)\n    assert False, "Отрицательный возраст должен вызывать ValueError"\nexcept ValueError:\n    pass', 350: 'assert isinstance(lst, list) and isinstance(tup, tuple) and hasattr(gen, "__next__") and sys.getsizeof(lst) > sys.getsizeof(gen), "Создайте список lst, кортеж tup и генераторное выражение gen на 1000 элементов"', 351: 'assert divide_safe(10, 2) == 5.0 and any(isinstance(n, _ast.With) for n in _ast.walk(_fn_nodes_test_divide_by_zero_raises[0])), "Реализуйте divide_safe и проверку через with pytest.raises(ValueError)"', 352: 'assert abs(calculate_tax(1.0) - 0.3) < 1e-6 and any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_calculate_tax_float_precision[0])), "Реализуйте calculate_tax и проверку через assert ... == pytest.approx(0.3)"', 353: '_gen_db = db_conn()\n_c_inst = next(_gen_db)\nassert _c_inst.closed is False and _c_inst.in_tx is True\ntry:\n    next(_gen_db)\nexcept StopIteration:\n    pass\nassert _c_inst.closed is True and _c_inst.in_tx is False, "Фикстура db_conn должна делать yield соединения, а после yield вызывать rollback() и close()"', 354: '_p_out = save_user_report(_MemPath("/tmp/t"), "alex", 95); assert _p_out.read_text() == "User: alex, Score: 95" and any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_save_user_report[0])), "save_user_report должна записывать \'User: <username>, Score: <score>\' в файл <username>.txt"', 355: 'assert get_api_dsn() == "https://localhost:8000/v1" and any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_get_api_dsn_custom_env[0])), "get_api_dsn() должна формировать URL из API_HOST и API_PORT, а тест — проверять подмену через monkeypatch.setenv"', 359: 'assert any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_large_refund_logs_warning[0])), "Тест test_large_refund_logs_warning должен проверять caplog через assert"', 360: 'assert parse_age(" 25 ") == 25 and any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_parse_age_valid[0])), "Реализуйте parse_age(raw) и проверку assert parse_age(raw_input) == expected"', 361: 'assert any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_admin_permissions[0])), "Фикстура make_user должна возвращать фабрику пользователей, а тест — проверять созданные словари через assert"', 362: '_mg = AsyncMock(spec=PaymentGateway)\n_mg.charge.return_value = {"transaction_id": "tx_99"}\nassert asyncio.run(checkout_order(_mg, 1, 500)) == "tx_99", "checkout_order должна вызывать await gateway.charge(...) и возвращать transaction_id"', 363: 'assert UserService().activate_user(1) is True and "create_autospec" in __USER_CODE__, "Реализуйте activate_user и создайте строгий мок через create_autospec(UserService, instance=True)"', 366: 'assert build_backup_path("/var/data/reports/monthly_2026.csv") == {"name": "monthly_2026.csv", "stem": "monthly_2026", "suffix": ".csv", "parent": "/var/data/reports", "backup": "/var/data/reports/monthly_2026_backup.bak"} and "with_suffix" in str(__USER_CODE__), "Функция build_backup_path должна разбирать путь и формировать backup-путь через with_suffix(\'.bak\')"', 374: 'assert flatten_batches([[1, 2], [], [3, 4, 5]]) == [1, 2, 3, 4, 5], "flatten_batches должна уплощать список батчей через chain.from_iterable"', 388: 'assert read_me({"id": 7, "role": "admin"}) == {"user_id": 7, "role": "admin"} and any(isinstance(n, _ast.Assert) for n in _ast.walk(_fn_nodes_test_read_me_with_dependency_override[0])), "Эндпоинт /me должен возвращать {\'user_id\': user[\'id\'], \'role\': user[\'role\']}"', 397: 'async def _test_asgi():\n    _ev = []\n    async def _send(e): _ev.append(e)\n    async def _r1(): return {"type": "lifespan.startup"}\n    await asgi_app({"type": "lifespan"}, _r1, _send)\n    async def _r2(): return {"type": "http.request"}\n    await asgi_app({"type": "http", "path": "/ping"}, _r2, _send)\n    return _ev\n_evs = asyncio.run(_test_asgi())\nassert any(e.get("type") == "lifespan.startup.complete" for e in _evs) and json.loads(_evs[-1]["body"].decode()) == {"path": "/ping", "db": True}, "asgi_app должна обрабатывать lifespan.startup и возвращать JSON с path и db"', 399: 'async def _test_ws_mgr():\n    _m = ConnectionManager()\n    _w1, _w2 = FakeWebSocket("A"), FakeWebSocket("B")\n    await _m.connect("r1", _w1); await _m.connect("r1", _w2)\n    await _m.broadcast("r1", "msg1")\n    _m.disconnect("r1", _w2)\n    await _m.broadcast("r1", "msg2")\n    return _w1.inbox, _w2.inbox\nassert asyncio.run(_test_ws_mgr()) == (["msg1", "msg2"], ["msg1"]), "Проверьте методы connect, disconnect и broadcast в ConnectionManager и FakeWebSocket"'})
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