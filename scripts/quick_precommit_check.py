#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quick_precommit_check.py

Быстрая (< 0.2с) синтаксическая валидация staged-файлов перед Git-коммитом:
- .js: node --check
- .py: py_compile
- .json: json.load
- .html: проверка всех inline <script> через node --check (in-memory без создания временных файлов на диске)
"""
import subprocess
import sys
import os
import re
import json

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

res = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'], capture_output=True, text=True)
if res.returncode != 0:
    sys.exit(0)

files = [os.path.normpath(f.strip()) for f in res.stdout.splitlines() if f.strip()]

for f in files:
    if not os.path.isfile(f):
        continue
    if f.endswith('.js'):
        c = subprocess.run(['node', '--check', f], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"[HOOK ERROR] Ошибка синтаксиса JS в {f}:\n{c.stderr}")
            sys.exit(1)
    elif f.endswith('.py'):
        c = subprocess.run([sys.executable, '-m', 'py_compile', f], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"[HOOK ERROR] Ошибка синтаксиса Python в {f}:\n{c.stderr}")
            sys.exit(1)
    elif f.endswith('.json'):
        try:
            with open(f, encoding='utf-8') as jf:
                json.load(jf)
        except Exception as e:
            print(f"[HOOK ERROR] Ошибка синтаксиса JSON в {f}:\n{e}")
            sys.exit(1)
    elif f.endswith('.html'):
        try:
            with open(f, encoding='utf-8') as hf:
                html = hf.read()
        except Exception as e:
            print(f"[HOOK ERROR] Не удалось прочитать HTML {f}:\n{e}")
            sys.exit(1)
        for m in re.finditer(r'<script(?:\s+([^>]*))?>([\s\S]*?)</script>', html, re.IGNORECASE):
            attrs = m.group(1) or ''
            code = m.group(2)
            if not code.strip():
                continue
            if 'type=' in attrs and not any(t in attrs for t in ['javascript', 'module']):
                continue
            c = subprocess.run(['node', '--check'], input=code, text=True, capture_output=True)
            if c.returncode != 0:
                print(f"[HOOK ERROR] Ошибка синтаксиса inline JS в {f}:\n{c.stderr}")
                sys.exit(1)

print("✓ [Pre-Commit] Синтаксическая проверка пройдена (JS, Python, JSON, HTML inline в норме).")
sys.exit(0)
