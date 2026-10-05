#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_hooks.py

Установщик легковесных Git-хуков (pre-commit) для защиты проекта
от синтаксических ошибок в JavaScript, Python и JSON.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HOOKS_DIR = os.path.join(_ROOT, '.git', 'hooks')

PRE_COMMIT_SHELL = """#!/bin/sh
# Git pre-commit hook: быстрая проверка синтаксиса (< 1с)

# 1. Проверка синтаксиса измененных JS файлов
js_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.js$')
for f in $js_files; do
  if [ -f "$f" ]; then
    node --check "$f" || { echo "[HOOK ERROR] Ошибка синтаксиса JS в $f"; exit 1; }
  fi
done

# 2. Проверка синтаксиса inline JS в academy.html (если он изменен)
if git diff --cached --name-only --diff-filter=ACM | grep -q 'academy.html'; then
  python -c "
import re, subprocess, os, sys
with open('academy.html', encoding='utf-8') as f:
    html = f.read()
scripts = re.findall(r'<script>([\\s\\S]*?)</script>', html)
if not scripts:
    sys.exit('Не найден тег <script> в academy.html')
tmp = 'tmp_hook_check.js'
with open(tmp, 'w', encoding='utf-8') as tf:
    tf.write(scripts[0])
res = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
if os.path.exists(tmp):
    os.remove(tmp)
if res.returncode != 0:
    print('[HOOK ERROR] Синтаксическая ошибка в academy.html inline JS:\\n' + res.stderr)
    sys.exit(1)
" || exit 1
fi

# 3. Проверка Python файлов через py_compile
py_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.py$')
for f in $py_files; do
  if [ -f "$f" ]; then
    python -m py_compile "$f" || { echo "[HOOK ERROR] Ошибка синтаксиса Python в $f"; exit 1; }
  fi
done

# 4. Проверка JSON файлов
json_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.json$')
for f in $json_files; do
  if [ -f "$f" ]; then
    node -e "JSON.parse(require('fs').readFileSync('$f', 'utf8'))" || { echo "[HOOK ERROR] Ошибка синтаксиса JSON в $f"; exit 1; }
  fi
done

echo "✓ [Pre-Commit] Синтаксическая проверка пройдена (JS, Python, JSON в норме)."
exit 0
"""

PRE_COMMIT_BAT = """@echo off
rem Git pre-commit hook for Windows cmd
python "%~dp0..\\..\\scripts\\quick_precommit_check.py"
if errorlevel 1 exit /b 1
exit /b 0
"""

QUICK_CHECK_PY = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, sys, os, re, json

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

res = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'], capture_output=True, text=True)
if res.returncode != 0:
    sys.exit(0)

files = [f.strip() for f in res.stdout.splitlines() if f.strip()]

for f in files:
    if f.endswith('.js') and os.path.isfile(f):
        c = subprocess.run(['node', '--check', f], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"[HOOK ERROR] Ошибка синтаксиса JS в {f}:\\n{c.stderr}")
            sys.exit(1)
    elif f.endswith('.py') and os.path.isfile(f):
        c = subprocess.run([sys.executable, '-m', 'py_compile', f], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"[HOOK ERROR] Ошибка синтаксиса Python в {f}:\\n{c.stderr}")
            sys.exit(1)
    elif f.endswith('.json') and os.path.isfile(f):
        try:
            with open(f, encoding='utf-8') as jf:
                json.load(jf)
        except Exception as e:
            print(f"[HOOK ERROR] Ошибка синтаксиса JSON в {f}:\\n{e}")
            sys.exit(1)
    elif f == 'academy.html' and os.path.isfile(f):
        with open(f, encoding='utf-8') as hf:
            html = hf.read()
        scripts = re.findall(r'<script>([\\s\\S]*?)</script>', html)
        if scripts:
            tmp = os.path.join(root, 'scripts', 'tmp_hook_check.js')
            with open(tmp, 'w', encoding='utf-8') as tf:
                tf.write(scripts[0])
            c = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except Exception: pass
            if c.returncode != 0:
                print(f"[HOOK ERROR] Ошибка синтаксиса inline JS в academy.html:\\n{c.stderr}")
                sys.exit(1)

print("✓ [Pre-Commit] Синтаксическая проверка пройдена (JS, Python, JSON в норме).")
sys.exit(0)
"""


def install():
    if not os.path.isdir(_HOOKS_DIR):
        print(f"Каталог хуков не найден: {_HOOKS_DIR}")
        return False

    hook_path = os.path.join(_HOOKS_DIR, 'pre-commit')
    with open(hook_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PRE_COMMIT_SHELL)

    # Make executable on Unix/Git Bash
    try:
        os.chmod(hook_path, 0o755)
    except Exception:
        pass

    # Quick check script for windows/cross-platform
    quick_py_path = os.path.join(_ROOT, 'scripts', 'quick_precommit_check.py')
    with open(quick_py_path, 'w', encoding='utf-8') as f:
        f.write(QUICK_CHECK_PY)

    print(f"✓ Git pre-commit hook успешно установлен в {hook_path}")
    print(f"✓ Вспомогательный скрипт сохранён в {quick_py_path}")
    return True


if __name__ == '__main__':
    install()
