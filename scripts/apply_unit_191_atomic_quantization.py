#!/usr/bin/env python3
"""
apply_unit_191_atomic_quantization.py
Генератор: Внедрение атомарного квантования и устранение мульти-примеров в конспектах Юнита 1.9.1 (Bugs 114..116).
"""

import sys
import os
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMY_PATH = os.path.join(ROOT, 'academy.html')
ETALON_DIR_PATH = os.path.join(ROOT, 'Эталоны', 'Эталоны.html')
ETALON_ROOT_PATH = os.path.join(ROOT, 'Эталоны.html')

with open(ACADEMY_PATH, 'r', encoding='utf-8') as f:
    academy_content = f.read()

m = re.search(r'const PY_MASTERY\s*=\s*(\{.*?\});\n', academy_content, re.DOTALL)
if not m:
    print('Error: PY_MASTERY not found in academy.html')
    sys.exit(1)

data = json.loads(m.group(1))

# Словарь новых атомарных HTML-конспектов для 27 шагов
REVISED_STEPS = {
    # ================= К-055: Регулярные выражения в Python =================
    ('К-055', 0): """<h4>Зачем нужны регулярные выражения: re vs строковые методы</h4>
<p><strong>Регулярное выражение (RegEx)</strong> — мини-язык шаблонов поиска в тексте (поиск IP, валидация почты, парсинг логов). В Python за них отвечает модуль <strong><code>re</code></strong>.</p>
<p>Правило скрининга: <strong>не используйте регулярки там, где достаточно методов <code>str</code></strong>. Проверка подстроки работает мгновенно и без компиляции автомата:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>text = &quot;admin@example.com&quot;

# Быстрый поиск подстроки и суффикса без regex:
print(&quot;@&quot; in text)
print(text.endswith(&quot;.com&quot;))</code></pre><div class="snippet-out hidden"></div></div>
<p>Модуль <strong><code>re</code></strong> нужен для нетривиальных динамических структур и диапазонов символов:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

pattern = r&quot;^[\w.-]+@[\w.-]+\.\w+$&quot;
print(bool(re.search(pattern, &quot;admin@example.com&quot;)))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 1): """<h4>re.search() — первое совпадение и объект Match</h4>
<p>Функция <strong><code>re.search(pattern, string)</code></strong> сканирует всю строку и возвращает объект <strong><code>Match</code></strong> для первого совпадения (или <code>None</code>, если совпадений нет).</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

log_line = &quot;2026-10-19 ERROR [user_id=42]: timeout&quot;
match = re.search(r&quot;user_id=(\d+)&quot;, log_line)

if match:
    print(&quot;Совпадение:&quot;, match.group(0))
    print(&quot;Значение:&quot;, match.group(1))
    print(&quot;Индексы:&quot;, match.span())</code></pre><div class="snippet-out hidden"></div></div>
<ul>
<li><strong><code>match.group(0)</code></strong> — весь совпавший фрагмент строки.</li>
<li><strong><code>match.start()</code> / <code>match.end()</code></strong> — начальный и конечный индексы среза в строке.</li>
<li><strong><code>match.span()</code></strong> — кортеж <code>(start, end)</code> для прямого взятия среза.</li>
</ul>""",

    ('К-055', 2): """<h4>re.match() vs re.fullmatch(): валидация префикса и полной строки</h4>
<p>Классическая ловушка первого скрининга — разница между <code>search</code>, <code>match</code> и <code>fullmatch</code>:</p>
<p><strong><code>re.match()</code></strong> проверяет совпадение только с начала строки:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

text = &quot;order_12345_complete&quot;
print(bool(re.match(r&quot;order_\d+&quot;, text)))
print(bool(re.match(r&quot;12345&quot;, text)))</code></pre><div class="snippet-out hidden"></div></div>
<p>Для валидации пользовательского ввода (URL slug, телефон, ID) всегда используйте <strong><code>re.fullmatch()</code></strong> — он требует совпадения всей строки целиком:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

print(bool(re.fullmatch(r&quot;order_\d+&quot;, &quot;order_12345_complete&quot;)))
print(bool(re.fullmatch(r&quot;[a-z0-9-]+&quot;, &quot;valid-slug-2026&quot;)))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 3): """<h4>re.findall() vs re.finditer(): память и ленивая обработка логов</h4>
<p>Когда нужно извлечь все совпадения из текста, используются две функции:</p>
<p><strong><code>re.findall()</code></strong> возвращает список <code>list</code>. Удобно для коротких строк, но требует O(N) RAM на больших файлах:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

log = &quot;ERR 404, WARN 500, ERR 502&quot;
codes = re.findall(r&quot;\b\d{3}\b&quot;, log)
print(&quot;Все коды списком:&quot;, codes)</code></pre><div class="snippet-out hidden"></div></div>
<p><strong><code>re.finditer()</code></strong> возвращает ленивый итератор объектов <code>Match</code>, обрабатывая записи по одной без всплеска памяти:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

log = &quot;ERR 404, WARN 500, ERR 502&quot;
for m in re.finditer(r&quot;\b\d{3}\b&quot;, log):
    print(f&quot;Число {m.group(0)} на позиции {m.start()}&quot;)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 5): """<h4>Классы символов: \\d, \\w, \\s и их отрицания \\D, \\W, \\S</h4>
<p>Управляющие последовательности определяют категории символов. Заглавная буква инвертирует класс:</p>
<p>Прямые классы — <strong><code>\\d</code></strong> (цифра), <strong><code>\\w</code></strong> (буква, цифра, <code>_</code>), <strong><code>\\s</code></strong> (пробел, таб):</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

text = &quot;User 42 logged in&quot;
print(&quot;Цифры:&quot;, re.findall(r&quot;\d+&quot;, text))
print(&quot;Слова:&quot;, re.findall(r&quot;\w+&quot;, text))</code></pre><div class="snippet-out hidden"></div></div>
<p>Отрицающие классы — <strong><code>\\D</code></strong> (не цифра), <strong><code>\\S</code></strong> (не пробел) идеальны для очистки данных:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

phone = &quot;+7 (999) 123-45-67&quot;
print(&quot;Очищенный номер:&quot;, re.sub(r&quot;\D&quot;, &quot;&quot;, phone))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 6): """<h4>Квантификаторы повторений: *, +, ? и точные диапазоны {n,m}</h4>
<p>Квантификатор указывает, сколько раз предшествующий символ или группа могут повторяться:</p>
<p>Символ <strong><code>?</code></strong> означает «0 или 1 раз» (опциональный элемент):</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

rx = r&quot;^https?://&quot;
print(bool(re.match(rx, &quot;http://api&quot;)))
print(bool(re.match(rx, &quot;https://api&quot;)))</code></pre><div class="snippet-out hidden"></div></div>
<p>Точный диапазон <strong><code>{n,m}</code></strong> задаёт допустимое число повторов (например, 4–6 цифр для PIN-кода):</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

pin_pattern = r&quot;^\d{4,6}$&quot;
print(bool(re.match(pin_pattern, &quot;12345&quot;)))
print(bool(re.match(pin_pattern, &quot;12&quot;)))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 8): """<h4>Группы захвата () и не захватывающие группы (?:...)</h4>
<p>Круглые скобки <strong><code>(...)</code></strong> группируют квантификаторы и захватывают фрагменты строки в группы:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

email = &quot;alex.dev@corp.example.com&quot;
m = re.search(r&quot;([\w.]+)@([\w.]+)&quot;, email)
if m:
    print(&quot;Имя:&quot;, m.group(1))
    print(&quot;Домен:&quot;, m.group(2))</code></pre><div class="snippet-out hidden"></div></div>
<p>Синтаксис <strong><code>(?:...)</code></strong> группирует токены для логики, но не сохраняет их в кортеж групп, экономя память:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

rx = r&quot;(?:https?://)?(github\.com/[\w-]+)&quot;
urls = re.findall(rx, &quot;https://github.com/torvalds&quot;)
print(&quot;GitHub URL:&quot;, urls)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 9): """<h4>Именованные группы (?P&lt;name&gt;...) и словарь .groupdict()</h4>
<p>В продакшен-коде обращение по номерам <code>group(1)</code> приводит к ошибкам при изменении шаблона.</p>
<p>Синтаксис <strong><code>(?P&lt;name&gt;...)</code></strong> даёт группе имя, а <strong><code>match.groupdict()</code></strong> возвращает удобный словарь:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

log = &quot;IP: 192.168.1.10 | STATUS: 200&quot;
rx = r&quot;IP: (?P&lt;ip&gt;[\d.]+) \| STATUS: (?P&lt;status&gt;\d+)&quot;
match = re.search(rx, log)

if match:
    data = match.groupdict()
    print(&quot;IP клиента:&quot;, data[&quot;ip&quot;])
    print(&quot;HTTP статус:&quot;, data[&quot;status&quot;])</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 11): """<h4>re.compile() и флаги компиляции: IGNORECASE, MULTILINE, DOTALL</h4>
<p>Функция <strong><code>re.compile()</code></strong> компилирует шаблон в объект <code>Pattern</code> в байткод регулярных выражений.</p>
<p>Предкомпиляция вне цикла ускоряет поиск в разы на миллионах строк:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

email_rx = re.compile(r&quot;^[a-z0-9_.-]+@[a-z0-9-]+\.[a-z]+$&quot;, re.IGNORECASE)
print(bool(email_rx.match(&quot;Admin@Host.ORG&quot;)))</code></pre><div class="snippet-out hidden"></div></div>
<p>Флаг <strong><code>re.DOTALL</code></strong> (или <code>re.S</code>) позволяет точке <code>.</code> сопоставлять переводы строк <code>\\n</code>:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

multi = &quot;start\\nhello world\\nend&quot;
matched = bool(re.search(r&quot;start.*end&quot;, multi, re.DOTALL))
print(&quot;DOTALL совпадение:&quot;, matched)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 12): """<h4>Безопасность на скрининге: катастрофический бэктрекинг (ReDoS)</h4>
<p><strong>ReDoS</strong> — уязвимость отказа в обслуживании через регулярные выражения. Движок CPython использует NFA с бэктрекингом.</p>
<p>При вложенных квантификаторах и несовпадающем суффиксе число шагов растёт экспоненциально:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code># Уязвимый шаблон с вложенными повторениями:
# rx = r&quot;(a+)+$&quot; на строке &quot;aaaaX&quot; заблокирует CPU!
bad_pattern = r&quot;^([a-zA-Z0-9]+_?)+$&quot;
print(&quot;Опасность: вложенные квантификаторы&quot;)</code></pre><div class="snippet-out hidden"></div></div>
<p>Безопасный шаблон не допускает неоднозначностей при ветвлении:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import re

safe_pattern = r&quot;^\\w+@\\w+\\.\\w+$&quot;
print(bool(re.match(safe_pattern, &quot;user@test.com&quot;)))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-055', 13): """<h4>Архитектурный выбор: когда использовать regex на практике</h4>
<p>Чек-лист Senior-интервьюера для первого технического скрининга:</p>
<ul>
<li><strong>Методы <code>str</code></strong> (<code>in</code>, <code>startswith</code>) — для статичных подстрок (без компиляции).</li>
<li><strong>Модуль <code>re</code></strong> — для динамических диапазонов, валидации форматов и поиска в логах.</li>
<li><strong><code>Pydantic v2</code></strong> — для валидации входных DTO в API на уровне архитектуры.</li>
</ul>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>tools = [&quot;str-methods&quot;, &quot;re.compile&quot;, &quot;pydantic-v2&quot;]
print(&quot;Инструменты бэкенда:&quot;, tools)
print(&quot;Регулярные выражения освоены!&quot;)</code></pre><div class="snippet-out hidden"></div></div>""",

    # ================= К-056: Сериализация и десериализация =================
    ('К-056', 0): """<h4>Что такое сериализация: сохранение состояния между процессами</h4>
<p><strong>Сериализация (Marshaling / Pickling)</strong> — преобразование структуры данных в памяти Python в байты или строку для сохранения на диск или передачи по сети.</p>
<p><strong>Десериализация (Unmarshaling)</strong> — обратное восстановление исходного объекта в памяти интерпретатора из байтов или текста.</p>
<p>Без сериализации данные живут только в RAM текущего процесса и исчезают при перезапуске сервера.</p>
<p>Форматы делятся на два типа: текстовые (JSON) для API и бинарные (Pickle, Protobuf) для внутреннего кеша.</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>user = {&quot;id&quot;: 42, &quot;username&quot;: &quot;admin&quot;}
# Объект в куче Python -&gt; Сериализация -&gt; Байт-поток
print(&quot;Исходный объект:&quot;, user, type(user))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-056', 1): """<h4>json.dumps() и json.loads(): строковая сериализация для API</h4>
<p>Модуль <strong><code>json</code></strong> преобразует объекты Python в стандартные строки JSON (JavaScript Object Notation):</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import json

user = {&quot;name&quot;: &quot;Алексей&quot;, &quot;roles&quot;: [&quot;admin&quot;, &quot;dev&quot;]}

# dumps сериализует dict в str:
raw_json = json.dumps(user, ensure_ascii=False)
print(&quot;JSON строка:&quot;, raw_json)

# loads восстанавливает dict из str:
parsed = json.loads(raw_json)
print(&quot;Имя пользователя:&quot;, parsed[&quot;name&quot;])</code></pre><div class="snippet-out hidden"></div></div>
<p>Параметр <code>ensure_ascii=False</code> сохраняет символы UTF-8 вместо экранированных <code>\\u0410...</code>.</p>""",

    ('К-056', 3): """<h4>Модуль pickle: бинарная сериализация объектов Python</h4>
<p>Модуль <strong><code>pickle</code></strong> — встроенный бинарный протокол Python. Он сериализует объекты (включая функции, классы и <code>set</code>), которые JSON не поддерживает:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import pickle

cache_entry = {&quot;perms&quot;: {&quot;read&quot;, &quot;write&quot;}, &quot;active&quot;: True}

# pickle.dumps возвращает bytes:
binary_blob = pickle.dumps(cache_entry)
print(&quot;Тип и размер:&quot;, type(binary_blob), len(binary_blob))

# pickle.loads восстанавливает set:
restored = pickle.loads(binary_blob)
print(&quot;Восстановлен set:&quot;, restored[&quot;perms&quot;])</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-056', 5): """<h4>Критическая опасность pickle: RCE через метод __reduce__</h4>
<p><strong>Главное правило безопасности</strong>: никогда не распаковывайте <code>pickle.loads()</code> из недоверенных источников (cookie, вебхуки, публичный API).</p>
<p>Метод <code>__reduce__</code> позволяет объекту вернуть вызываемый объект и аргументы для его вызова при десериализации.</p>
<p>Злоумышленник может передать команду <code>os.system('rm -rf /')</code>, которая выполнится на сервере мгновенно (Remote Code Execution).</p>
<p>Для внешнего API используйте строгие схемы <code>pydantic</code> и <code>json</code>, а pickle — только для доверенного внутреннего кеша.</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code># Демонстрация опасной структуры __reduce__:
class SafeDemo:
    def __reduce__(self):
        return (print, (&quot;Исполнение произвольного кода!&quot;,))

import pickle
blob = pickle.dumps(SafeDemo())
pickle.loads(blob)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-056', 6): """<h4>Кастомный энкодер json: сериализация datetime и UUID</h4>
<p>Стандартный <code>json.dumps()</code> выбрасывает <code>TypeError: Object of type datetime is not JSON serializable</code>.</p>
<p>Самый лаконичный способ — передать аргумент <code>default=str</code>, который преобразует неизвестные типы в строки:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from datetime import datetime
import json
import uuid

order = {&quot;id&quot;: uuid.uuid4(), &quot;created_at&quot;: datetime.now()}
payload = json.dumps(order, default=str)
print(&quot;Успешная сериализация:&quot;, payload)</code></pre><div class="snippet-out hidden"></div></div>""",

    # ================= К-057: CPython и байткод =================
    ('К-057', 1): """<h4>Путь от .py файла до выполнения: AST, байткод и PVM</h4>
<p>Python не компилируется в машинный код напрямую, а использует двухэтапный конвейер: компиляцию в байткод и исполнение виртуальной машиной.</p>
<p>Конвейер: <code>.py</code> ➔ парсер ➔ <strong>AST</strong> ➔ компилятор ➔ <strong>Байткод (.pyc)</strong> ➔ <strong>PVM (цикл eval)</strong>.</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import dis

# Дизассемблирование инструкций байткода функции:
def add(a, b):
    return a + b

dis.dis(add)</code></pre><div class="snippet-out hidden"></div></div>
<ul>
<li><strong>Парсер</strong> преобразует текст <code>.py</code> в синтаксическое дерево (<strong>AST</strong>).</li>
<li><strong>Компилятор</strong> превращает AST в платформонезависимый <strong>байткод</strong>.</li>
<li>Байткод кэшируется в папке <code>__pycache__</code> в файлах <code>.pyc</code> для ускорения импорта.</li>
<li><strong>PVM</strong> исполняет инструкции байткода в главном цикле.</li>
</ul>""",

    ('К-057', 3): """<h4>Почему Python называют медленным: CPU-bound vs I/O-bound</h4>
<p>Выполнение байткода виртуальной машиной поверх стека требует дополнительных инструкций процессора по сравнению с компилируемыми языками.</p>
<p>Динамическая типизация обязывает интерпретатор проверять тип каждого операнда и распаковывать структуры в куче при любой операции.</p>
<p>В бэкенде 95% времени тратится на ожидание I/O: сеть, SQL-запросы к PostgreSQL и Redis. Здесь скорость CPU не является узким местом.</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code># Бэкенд — это I/O bound архитектура:
pipeline = [&quot;HTTP&quot;, &quot;PostgreSQL&quot;, &quot;Redis&quot;, &quot;JSON&quot;]
print(&quot;Пайплайн ожидания ввода-вывода:&quot;, &quot; -&gt; &quot;.join(pipeline))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-057', 4): """<h4>Модель вычислений PVM: Stack-based Virtual Machine</h4>
<p>Виртуальная машина CPython построена по принципу стекового автомата (Stack-based VM). У неё нет именованных регистров процессора.</p>
<p>Каждый вызов функции создаёт объект кадра выполнения (frame), содержащий стек значений и массив локальных переменных:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code># Имитация работы стека PVM для (10 + 20):
stack = []
stack.append(10)          # LOAD_CONST 10
stack.append(20)          # LOAD_CONST 20
result = stack.pop() + stack.pop() # BINARY_OP
stack.append(result)      # STORE_FAST
print(&quot;Значение на вершине стека:&quot;, stack.pop())</code></pre><div class="snippet-out hidden"></div></div>""",

    # ================= К-222: pathlib =================
    ('К-222', 0): """<h4>Почему pathlib заменил os.path в современном Python</h4>
<p>В легаси-коде пути хранили в обычных строках <code>str</code> и склеивали через <code>os.path.join()</code>. Это приводило к ошибкам из-за слэшей Windows и Linux.</p>
<p>Модуль <strong><code>pathlib</code></strong> (PEP 428) представляет пути как полноценные объекты класса <code>Path</code> с перегруженным оператором деления <code>/</code>:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path

# Корень проекта и кроссплатформенный путь через /:
BASE_DIR = Path(&quot;.&quot;).resolve()
config_path = BASE_DIR / &quot;configs&quot; / &quot;app.yaml&quot;
print(&quot;Кроссплатформенный путь:&quot;, config_path)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-222', 1): """<h4>Анатомия объекта Path: разбор пути без split()</h4>
<p>Объект <code>Path</code> мгновенно разбирает путь на составляющие без строковых срезов и устаревших функций <code>os.path</code>:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path

p = Path(&quot;/var/log/nginx/access.tar.gz&quot;)
print(&quot;Имя файла:&quot;, p.name)
print(&quot;Без последнего суффикса:&quot;, p.stem)
print(&quot;Суффикс:&quot;, p.suffix)
print(&quot;Родительская папка:&quot;, p.parent)</code></pre><div class="snippet-out hidden"></div></div>
<p>Методы <code>with_suffix()</code> и <code>with_name()</code> возвращают новый неизменяемый объект с обновлённым именем:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path

p = Path(&quot;/var/log/nginx/access.tar.gz&quot;)
print(&quot;Замена расширения:&quot;, p.with_suffix(&quot;.bak&quot;))
print(&quot;Замена имени:&quot;, p.with_name(&quot;error.log&quot;))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-222', 3): """<h4>Чтение, запись и управление директориями</h4>
<p>Для небольших файлов <code>Path</code> позволяет прочитать или записать содержимое в одну строку с явной кодировкой UTF-8:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path

report = Path(&quot;output/reports/summary.txt&quot;)
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text(&quot;Отчёт готов\\n&quot;, encoding=&quot;utf-8&quot;)
print(&quot;Записано и прочитано:&quot;, report.read_text(encoding=&quot;utf-8&quot;).strip())</code></pre><div class="snippet-out hidden"></div></div>
<h4>Проверка статуса и метаданные пути</h4>
<ul>
<li><strong><code>.exists()</code></strong> — проверяет существование файла или папки на диске.</li>
<li><strong><code>.is_file()</code> / <code>.is_dir()</code></strong> — определяет тип объекта.</li>
<li><code>.is_symlink()</code> — определяет, является ли путь символической ссылкой.</li>
<li><strong><code>.stat()</code></strong> — возвращает метаданные: размер <code>st_size</code> в байтах, метку времени изменения (<code>st_mtime</code>).</li>
</ul>""",

    ('К-222', 4): """<h4>Поиск файлов и обход дерева: iterdir, glob, rglob</h4>
<p>Вместо устаревших <code>os.listdir()</code> и модуля <code>glob</code> объект <code>Path</code> предоставляет три ленивых генератора:</p>
<ul>
<li><strong><b><code>iterdir()</code></b></strong> — итерация по прямым потомкам директории (без рекурсии).</li>
<li><strong><code>glob(pattern)</code></strong> — поиск файлов по маске в текущей директории.</li>
<li><strong><b><code>rglob(pattern)</code></b></strong> — рекурсивный поиск по всему дереву подпапок (аналог <code>glob(&quot;**/*&quot;)</code>).</li>
</ul>
<p>Прямые потомки папки через <code>iterdir()</code>:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path

for item in Path(&quot;.&quot;).iterdir():
    if item.is_dir():
        print(&quot;Папка:&quot;, item.name)</code></pre><div class="snippet-out hidden"></div></div>
<p>Рекурсивный поиск файлов через <code>rglob()</code>:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path

py_files = list(Path(&quot;.&quot;).rglob(&quot;*.py&quot;))
print(&quot;Найдено скриптов:&quot;, len(py_files))</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-222', 5): """<h4>resolve() vs absolute() и архитектура PurePath vs Path</h4>
<p>В <code>pathlib</code> иерархия классов строго разделена на два уровня:</p>
<ul>
<li><strong><code>PurePath</code></strong> (<code>PurePosixPath</code>, <code>PureWindowsPath</code>) — вычислительные пути в памяти без дискового ввода-вывода (конструирование путей других ОС).</li>
<li><strong><code>Path</code></strong> (<code>PosixPath</code>, <code>WindowsPath</code>) — пути с системными вызовами (<code>exists()</code>, <code>mkdir()</code>, <code>read_text()</code>).</li>
</ul>
<p>Метод <strong><code>resolve()</code></strong> не просто строит абсолютный путь, но и физически раскрывает все симлинки и устраняет переходы <code>..</code>:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from pathlib import Path, PurePosixPath

# PurePath: работа в памяти без I/O:
pure = PurePosixPath(&quot;/etc/hosts&quot;)
print(&quot;Имя в PurePath:&quot;, pure.name)

# Path.resolve(): раскрывает symlinks:
target = Path(&quot;.&quot;).resolve()
print(&quot;Физический путь:&quot;, target)</code></pre><div class="snippet-out hidden"></div></div>""",

    # ================= К-220: logging =================
    ('К-220', 0): """<h4>Почему в продакшене используют logging, а не print()</h4>
<p>Вызов <code>print()</code> пишет неструктурированный текст в stdout: у него нет уровней важности, метаданных и таймстемпов.</p>
<p>Его нельзя отключить в продакшене без редактирования исходного кода, а в многопоточной среде вызовы print перемешиваются.</p>
<p>Стандартный модуль <strong><code>logging</code></strong> решает эти задачи через разделение уровней (DEBUG..CRITICAL), форматирование и маршрутизацию логов.</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

logging.basicConfig(level=logging.INFO, format=&quot;%(levelname)s: %(message)s&quot;)
logging.info(&quot;Сервер запущен и слушает порт 8000&quot;)
logging.warning(&quot;Высокая нагрузка на CPU&quot;)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-220', 1): """<h4>Четыре столпа архитектуры logging: Logger, Handler, Formatter, Filter</h4>
<p>Модуль <code>logging</code> разделяет ответственность на специализированные компоненты:</p>
<p><strong>1. Логгер: модульная точка входа</strong></p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

# 1. Логгер: модульная точка входа
logger = logging.getLogger(&quot;api.users&quot;)
logger.setLevel(logging.INFO)</code></pre><div class="snippet-out hidden"></div></div>
<p><strong>2. Форматтер сообщения</strong></p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

# 2. Форматтер сообщения
fmt = logging.Formatter(&quot;%(asctime)s [%(levelname)s] %(message)s&quot;)</code></pre><div class="snippet-out hidden"></div></div>
<p><strong>3. Консольный хендлер</strong></p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

# 3. Консольный хендлер
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(&quot;%(levelname)s: %(message)s&quot;))</code></pre><div class="snippet-out hidden"></div></div>
<p><strong>4. Хендлер ротации файла</strong></p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

# 4. Хендлер ротации файла
file_handler = logging.FileHandler(&quot;app.log&quot;, encoding=&quot;utf-8&quot;)</code></pre><div class="snippet-out hidden"></div></div>
<p><strong>5. Регистрация хендлеров</strong></p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code># 5. Регистрация хендлеров
logger.addHandler(console_handler)
logger.info(&quot;Пользователь авторизован&quot;)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-220', 2): """<h4>Иерархия по точкам и флаг propagate (почему логи дублируются)</h4>
<p>Имена логгеров образуют дерево по точкам: <code>app.payment</code> является дочерним по отношению к <code>app</code>, а тот — к корневому <code>root</code>.</p>
<p>По умолчанию включён атрибут <strong><code>logger.propagate = True</code></strong>. Сообщение передаётся вверх по цепочке к хендлерам предков.</p>
<p>Если повесить хендлер и на дочерний логгер, и на корневой root, лог напечатается дважды.</p>
<p>Решение: либо настраивать хендлеры только на корневом логгере, либо ставить <code>logger.propagate = False</code> на дочернем.</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

logger = logging.getLogger(&quot;app.billing&quot;)
# Запрет всплытия предотвращает дублирование сообщений:
logger.propagate = False
print(&quot;Propagate статус:&quot;, logger.propagate)</code></pre><div class="snippet-out hidden"></div></div>""",

    ('К-220', 3): """<h4>Логирование исключений: logger.exception() и exc_info=True</h4>
<p>В блоке <code>except</code> вызов <code>logger.error(e)</code> теряет ценный traceback ошибки. Для расследования инцидентов необходим полный стек вызовов.</p>
<p>Метод <strong><code>logger.exception()</code></strong> автоматически прикрепляет полный traceback к сообщению уровня ERROR:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>import logging

logger = logging.getLogger(&quot;db.connection&quot;)
try:
    1 / 0
except ZeroDivisionError:
    # logger.exception автоматически добавляет стек трейс:
    logger.exception(&quot;Сбой расчёта баланса&quot;)</code></pre><div class="snippet-out hidden"></div></div>
<p>В других уровнях (например, INFO) стек можно включить явно параметром <code>exc_info=True</code>.</p>""",

    ('К-220', 4): """<h4>Конфигурация через dictConfig и структурированные JSON-логи</h4>
<p>В реальных сервисах (FastAPI, Django, Celery) логирование настраивают декларативно через <strong><code>logging.config.dictConfig</code></strong>.</p>
<p>Словарь конфигурации задаёт форматтеры, хендлеры и корневой логгер в единой структуре:</p>
<div class="snippet-wrap"><div class="code-run-bar"><span class="mono meta">python</span><button type="button" class="btn-inline-run" data-run-snippet="1">▶ Запустить код</button></div><pre><code>from logging.config import dictConfig
import logging

dictConfig({
    &quot;version&quot;: 1,
    &quot;disable_existing_loggers&quot;: False,
    &quot;handlers&quot;: {&quot;stdout&quot;: {&quot;class&quot;: &quot;logging.StreamHandler&quot;}},
    &quot;root&quot;: {&quot;handlers&quot;: [&quot;stdout&quot;], &quot;level&quot;: &quot;INFO&quot;}
})
logging.getLogger().info(&quot;Сервер настроен через dictConfig&quot;)</code></pre><div class="snippet-out hidden"></div></div>"""
}

# Валидация всех новых шагов перед применением
print('--- ВАЛИДАЦИЯ НОВЫХ ШАГОВ ---')
validation_errors = []
for (kid, sidx), html in REVISED_STEPS.items():
    # 1. Multi-example check
    codes = re.findall(r'<pre><code>(.*?)</code></pre>', html, re.DOTALL)
    for cidx, c in enumerate(codes):
        nums = re.findall(r'#\s*\d+\.\s*', c)
        if len(nums) > 1:
            validation_errors.append(f'{kid}:{sidx} block #{cidx+1} has multiple numbered examples: {nums}')
        lines = [l for l in c.strip().split('\n') if l.strip()]
        if len(lines) > 12:
            validation_errors.append(f'{kid}:{sidx} block #{cidx+1} has {len(lines)} lines (> 12 limit)')
            
    # 2. Paragraph check
    paras = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
    for pidx, p in enumerate(paras):
        ptext = re.sub(r'<.*?>', '', p).strip()
        if len(ptext) > 240:
            validation_errors.append(f'{kid}:{sidx} p #{pidx+1} has {len(ptext)} chars (> 240 limit): "{ptext[:40]}..."')

if validation_errors:
    print('ОШИБКИ ВАЛИДАЦИИ:')
    for err in validation_errors:
        print('  ❌', err)
    sys.exit(1)
print(f'✓ Все {len(REVISED_STEPS)} обновлённых шагов успешно прошли проверку на лимиты строк (<=12), отсутствие мульти-примеров и длину параграфов (<=240)!')

# Применение правок к data['notes']
for (kid, sidx), html in REVISED_STEPS.items():
    data['notes'][kid]['steps'][sidx]['html'] = html
    print(f'  ✓ Обновлён {kid}:{sidx}')

new_json_str = json.dumps(data, ensure_ascii=False)

new_academy_content = academy_content[:m.start(1)] + new_json_str + academy_content[m.end(1):]

print(f'\nРазмер academy.html: было {len(academy_content)}, стало {len(new_academy_content)} байт')

# Сохранение в academy.html
with open(ACADEMY_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_academy_content)
print(f'✓ academy.html сохранён ({len(new_academy_content)} символов)')

# Синхронизация с Эталонами
with open(ETALON_DIR_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_academy_content)
print('✓ Эталоны/Эталоны.html синхронизирован')

with open(ETALON_ROOT_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_academy_content)
print('✓ Эталоны.html синхронизирован')

print('\n=========================================')
print('  КВАНТОВАНИЕ УСПЕШНО ПРИМЕНЕНО И СИНХРОНИЗИРОВАНО!')
print('=========================================')
