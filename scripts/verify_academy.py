import re, subprocess, json, os
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_UNPACKED_HTML = os.path.normpath(os.path.join(_HERE, '..', 'academy.html'))
HTML_PATH = _UNPACKED_HTML if os.path.isfile(_UNPACKED_HTML) else r'C:\Users\fury6\Downloads\Telegram Desktop\academy.html'

with open(HTML_PATH, encoding='utf-8') as f:
    html = f.read()

# 1. Extract main inline <script> and check syntax with node --check
scripts = re.findall(r'<script>([\s\S]*?)</script>', html)
assert len(scripts) == 1, f"Expected 1 inline script, found {len(scripts)}"
js_code = scripts[0]

js_tmp = os.path.join(_HERE, 'extracted_academy.js')
with open(js_tmp, 'w', encoding='utf-8') as f:
    f.write(js_code)

res = subprocess.run(['node', '--check', js_tmp], capture_output=True, text=True)
assert res.returncode == 0, f"JS syntax error:\n{res.stderr}"
print("1. [PASS] node --check passed with 0 syntax errors!")

# 2. Verify real Headless Chrome renders <main id="view-root"> across routes
chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
base_uri = Path(HTML_PATH).as_uri()
for route, expected_sub in [
    (base_uri, 'Правило 2 минут: Быстрый микро-шаг'),
    (base_uri + '#/python', 'Матрица Мастерства Python'),
    (base_uri + '#/web', 'Матрица Мастерства Web'),
    (base_uri + '#/backend', 'Матрица Мастерства Backend'),
    (base_uri + '#/algorithms', 'Матрица Мастерства Алгоритмы'),
    (base_uri + '#/databases', 'Матрица Мастерства Базы данных'),
    (base_uri + '#/architecture', 'Матрица Мастерства Архитектура'),
    (base_uri + '#/infra', 'Матрица Мастерства Инфраструктура'),
    (base_uri + '#/infra/boss', 'Аудитор продакшен-инфраструктуры'),
    (base_uri + '#/mock', 'Симулятор собеседования'),
    (base_uri + '#/map', 'Карта навыков'),
    (base_uri + '#/practice', 'Практика кода'),
    (base_uri + '#/cards', 'Центр 3D Флеш-карточек'),
]:
    out = subprocess.check_output(
        [chrome_exe, '--headless', '--no-sandbox', '--disable-gpu', '--dump-dom', route],
        text=True, encoding='utf-8', errors='ignore'
    )
    m = re.search(r'<main id="view-root">([\s\S]*?)</main>', out)
    assert m and len(m.group(1).strip()) > 200, f"Empty <main id='view-root'> in Chrome for {route}"
    assert expected_sub in m.group(1), f"Missing {expected_sub!r} in Chrome DOM for {route}"
    print(f"2. [PASS] Real Headless Chrome rendered {route} ({len(m.group(1))} chars in #view-root)")

