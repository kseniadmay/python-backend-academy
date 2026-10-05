import re, subprocess, json, os
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.normpath(os.path.join(_HERE, '..', 'academy.html'))
assert os.path.isfile(HTML_PATH), f"academy.html missing: {HTML_PATH}"

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
if os.path.exists(js_tmp):
    try: os.remove(js_tmp)
    except Exception: pass
assert res.returncode == 0, f"JS syntax error:\n{res.stderr}"
print("1. [PASS] node --check passed with 0 syntax errors!")

# 2. Verify real Headless Chrome renders <main id="view-root"> across routes and produces 0 console errors
import tempfile
from concurrent.futures import ThreadPoolExecutor

chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
base_uri = Path(HTML_PATH).as_uri()
chrome_flags = [
    chrome_exe, '--headless', '--no-sandbox', '--disable-gpu',
    '--disable-background-networking', '--disable-sync', '--disable-default-apps',
    '--allow-file-access-from-files',
    '--enable-logging=stderr', '--dump-dom'
]

routes = [
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
]

def verify_single_route(item):
    route, expected_sub = item
    with tempfile.TemporaryDirectory() as td:
        c_res = subprocess.run(
            chrome_flags + [f'--user-data-dir={td}', route],
            capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        assert c_res.returncode == 0, f"Chrome failed with code {c_res.returncode} on {route}"
        c_errors = [line for line in c_res.stderr.splitlines() if 'ERROR:CONSOLE' in line or 'Uncaught ' in line]
        assert not c_errors, f"Console error in Chrome for {route}:\n" + "\n".join(c_errors)
        out = c_res.stdout
        m = re.search(r'<main id="view-root">([\s\S]*?)</main>', out)
        assert m and len(m.group(1).strip()) > 200, f"Empty <main id='view-root'> in Chrome for {route}"
        assert expected_sub in m.group(1), f"Missing {expected_sub!r} in Chrome DOM for {route}"
        return f"2. [PASS] Real Headless Chrome rendered {route} (0 console errors, {len(m.group(1))} chars in #view-root)"

with ThreadPoolExecutor(max_workers=5) as executor:
    for msg in executor.map(verify_single_route, routes):
        print(msg)

# 3. Verify real Headless Chrome renders standalone IDE trainer (Практика кода — тренажёр с IDE.html)
ide_path = os.path.normpath(os.path.join(_HERE, '..', 'Практика кода — тренажёр с IDE.html'))
if os.path.isfile(ide_path):
    ide_uri = Path(ide_path).as_uri()
    ide_res = subprocess.run(
        chrome_flags + [ide_uri],
        capture_output=True, text=True, encoding='utf-8', errors='ignore'
    )
    assert ide_res.returncode == 0, f"Chrome failed on standalone IDE with code {ide_res.returncode}"
    ide_c_errors = [line for line in ide_res.stderr.splitlines() if 'ERROR:CONSOLE' in line or 'Uncaught ' in line]
    assert not ide_c_errors, f"Console error in Chrome for standalone IDE:\n" + "\n".join(ide_c_errors)
    ide_out = ide_res.stdout
    assert 'Все уровни' in ide_out and '401' in ide_out, f"Missing 'Все уровни' or '401' in IDE HTML render"
    assert 'task-grid' in ide_out or 'task-card' in ide_out, "Missing task grid/cards in IDE HTML render"
    assert 'editorHost' in ide_out or 'CodeMirror' in ide_out, "Missing editor container in IDE HTML render"
    print(f"3. [PASS] Real Headless Chrome rendered standalone IDE trainer (0 console errors, {len(ide_out)} chars)")

# 4. Verify Python_Backend_Academy_Project.zip structure and integrity
import zipfile
zip_path = os.path.normpath(os.path.join(_HERE, '..', 'Python_Backend_Academy_Project.zip'))
if os.path.isfile(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()
        assert len(namelist) >= 545, f"Expected >= 545 files in project zip, got {len(namelist)}"
        required_in_zip = [
            'academy.html',
            'Практика кода — тренажёр с IDE.html',
            'manifest.json',
            'icon.svg',
            'sw.js',
            'RemNote_Python_Mastery_FIXED.zip',
            'README.md',
            'scripts/assemble_academy.py',
            'scripts/test_e2e_dom.js',
            'scripts/test_all_401_tasks.py'
        ]
        for req in required_in_zip:
            assert req in namelist, f"Missing required file '{req}' inside Python_Backend_Academy_Project.zip"
        # Validate nested RemNote zip integrity
        rem_bytes = zf.read('RemNote_Python_Mastery_FIXED.zip')
        import io
        with zipfile.ZipFile(io.BytesIO(rem_bytes)) as rzf:
            r_names = rzf.namelist()
            assert len(r_names) == 525, f"Expected 525 files inside nested RemNote zip, got {len(r_names)}"
    print(f"4. [PASS] Project archive Python_Backend_Academy_Project.zip verified ({len(namelist)} items, nested RemNote 525 items)!")


