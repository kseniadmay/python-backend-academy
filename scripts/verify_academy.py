import re, subprocess, json, os, sys, shutil, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.normpath(os.path.join(_HERE, '..', 'academy.html'))
IDE_PATH = os.path.normpath(os.path.join(_HERE, '..', 'Практика кода — тренажёр с IDE.html'))
INDEX_PATH = os.path.normpath(os.path.join(_HERE, '..', 'index.html'))
assert os.path.isfile(HTML_PATH), f"academy.html missing: {HTML_PATH}"

# 1. Syntax check with node --check (in-memory, 0 disk artifacts) across all entry points
def check_html_inline_scripts(html_file, label):
    with open(html_file, encoding='utf-8') as f:
        content = f.read()
    checked = 0
    for m in re.finditer(r'<script(?:\s+([^>]*))?>([\s\S]*?)</script>', content, re.IGNORECASE):
        attrs = m.group(1) or ''
        code = m.group(2)
        if not code.strip():
            continue
        if 'type=' in attrs and not any(t in attrs for t in ['javascript', 'module']):
            continue
        res = subprocess.run(['node', '--check'], input=code, text=True, capture_output=True)
        assert res.returncode == 0, f"JS syntax error in {label}:\n{res.stderr}"
        checked += 1
    assert checked > 0, f"No inline scripts found in {label}"
    return checked

c_acad = check_html_inline_scripts(HTML_PATH, 'academy.html')
c_ide = check_html_inline_scripts(IDE_PATH, 'Практика кода — тренажёр с IDE.html') if os.path.isfile(IDE_PATH) else 0
c_idx = check_html_inline_scripts(INDEX_PATH, 'index.html') if os.path.isfile(INDEX_PATH) else 0
print(f"1. [PASS] node --check passed with 0 syntax errors across {c_acad + c_ide + c_idx} scripts (academy: {c_acad}, IDE: {c_ide}, index: {c_idx})!", flush=True)

# 2. Discover Chrome executable across standard installation paths and PATH
def get_chrome_executable():
    candidates = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%PROGRAMFILES%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    for cmd in ('chrome', 'google-chrome', 'chromium'):
        p = shutil.which(cmd)
        if p:
            return p
    return candidates[0]

chrome_exe = get_chrome_executable()
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
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
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
if os.path.isfile(IDE_PATH):
    ide_uri = Path(IDE_PATH).as_uri()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td_ide:
        ide_res = subprocess.run(
            chrome_flags + [f'--user-data-dir={td_ide}', ide_uri],
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


