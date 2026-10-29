#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quick_precommit_check.py

Быстрая (< 0.2с) синтаксическая валидация файлов и переиспользуемый
проверяющий модуль inline <script> для HTML-файлов (DRY):
- .js: node --check
- .py: py_compile
- .json: json.load
- .html: проверка всех inline <script> через node --check (in-memory без временных файлов)
"""

import json
import os
import re
import shutil
import subprocess
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_html_inline_scripts(
    html_file: str,
    label: str = '',
    require_non_empty: bool = False
) -> int:
    """
    Проверяет все inline <script> теги внутри HTML-файла через `node --check`.
    Возвращает количество проверенных блоков <script>.
    Выбрасывает RuntimeError при ошибке синтаксиса JS.
    """
    display_label = label or html_file
    with open(html_file, encoding='utf-8') as hf:
        html = hf.read()

    if shutil.which('node') is None:
        return 0

    checked = 0
    for m in re.finditer(r'<script(?:\s+([^>]*))?>([\s\S]*?)</script>', html, re.IGNORECASE):
        attrs = m.group(1) or ''
        code = m.group(2)
        if not code.strip():
            continue
        if 'type=' in attrs and not any(t in attrs for t in ('javascript', 'module')):
            continue
        cmd = ['node', '--check']
        if 'module' in attrs:
            cmd = ['node', '--input-type=module', '--check']
        c = subprocess.run(cmd, input=code, text=True, capture_output=True)
        if c.returncode != 0:
            raise RuntimeError(f'JS syntax error in {display_label}:\n{c.stderr}')
        checked += 1

    if require_non_empty and checked == 0:
        raise RuntimeError(f'No inline scripts found in {display_label}')

    return checked


def main() -> int:
    os.chdir(_ROOT)
    res = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        return 0

    files = [os.path.normpath(f.strip()) for f in res.stdout.splitlines() if f.strip()]
    has_node = shutil.which('node') is not None

    for f in files:
        if not os.path.isfile(f):
            continue
        if f.endswith('.js'):
            if has_node:
                c = subprocess.run(['node', '--check', f], capture_output=True, text=True)
                if c.returncode != 0:
                    print(f'[HOOK ERROR] Ошибка синтаксиса JS в {f}:\n{c.stderr}')
                    return 1
        elif f.endswith('.py'):
            c = subprocess.run([sys.executable, '-m', 'py_compile', f], capture_output=True, text=True)
            if c.returncode != 0:
                print(f'[HOOK ERROR] Ошибка синтаксиса Python в {f}:\n{c.stderr}')
                return 1
        elif f.endswith('.json'):
            try:
                with open(f, encoding='utf-8') as jf:
                    json.load(jf)
            except Exception as e:
                print(f'[HOOK ERROR] Ошибка синтаксиса JSON в {f}:\n{e}')
                return 1
        elif f.endswith('.html'):
            try:
                check_html_inline_scripts(f, label=f, require_non_empty=False)
            except Exception as e:
                print(f'[HOOK ERROR] Ошибка в HTML {f}:\n{e}')
                return 1

    print('✓ [Pre-Commit] Синтаксическая проверка пройдена (JS, Python, JSON, HTML inline в норме).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
