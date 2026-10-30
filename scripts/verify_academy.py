#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_academy.py

Быстрая проверка целостности сборки и синтаксиса (без Headless Chrome и UI/DOM-тестов):
1. Идентичность academy.html и standards/standards.html (Canonical Benchmark Invariant).
2. Проверка синтаксиса встроенных JS-скриптов через node --check.
3. Проверка структуры архива academy_backup.zip (если присутствует).
"""
import re
import subprocess
import os
import sys
import shutil
import zipfile
import io

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.normpath(os.path.join(_HERE, '..', 'academy.html'))
ETALON_PATH = os.path.normpath(os.path.join(_HERE, '..', 'standards', 'standards.html'))
IDE_PATH = os.path.normpath(os.path.join(_HERE, '..', 'practice_ide.html'))
INDEX_PATH = os.path.normpath(os.path.join(_HERE, '..', 'index.html'))

assert os.path.isfile(HTML_PATH), f"academy.html missing: {HTML_PATH}"
assert os.path.isfile(ETALON_PATH), f"standards/standards.html missing: {ETALON_PATH}"

with open(HTML_PATH, encoding='utf-8') as f1, open(ETALON_PATH, encoding='utf-8') as f2:
    assert f1.read() == f2.read(), "academy.html and standards.html must be strictly identical (Canonical Benchmark Invariant)!"


def check_html_inline_scripts(html_file, label):
    if shutil.which('node') is None:
        return 0
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
c_etalon = check_html_inline_scripts(ETALON_PATH, 'standards.html')
c_ide = check_html_inline_scripts(IDE_PATH, 'practice_ide.html') if os.path.isfile(IDE_PATH) else 0
c_idx = check_html_inline_scripts(INDEX_PATH, 'index.html') if os.path.isfile(INDEX_PATH) else 0
print(f"1. [PASS] Syntax check passed across {c_acad + c_etalon + c_ide + c_idx} scripts (academy: {c_acad}, etalon: {c_etalon}, IDE: {c_ide}, index: {c_idx})!", flush=True)

zip_path = os.path.normpath(os.path.join(_HERE, '..', 'academy_backup.zip'))
if os.path.isfile(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()
        assert len(namelist) >= 545, f"Expected >= 545 files in project zip, got {len(namelist)}"
        required_in_zip = [
            'academy.html',
            'practice_ide.html',
            'standards/standards.html',
            'manifest.json',
            'icon.svg',
            'sw.js',
            'knowledge_base.zip',
            'README.md',
            'scripts/assemble_academy.py',
            'scripts/test_all_401_tasks.py'
        ]
        for req in required_in_zip:
            assert req in namelist, f"Missing required file '{req}' inside academy_backup.zip"
        rem_bytes = zf.read('knowledge_base.zip')
        with zipfile.ZipFile(io.BytesIO(rem_bytes)) as rzf:
            r_names = rzf.namelist()
            assert len(r_names) in (525, 526), f"Expected 525 or 526 files inside nested RemNote zip, got {len(r_names)}"
    print(f"2. [PASS] Project archive academy_backup.zip verified ({len(namelist)} items, nested RemNote 525 items)!", flush=True)