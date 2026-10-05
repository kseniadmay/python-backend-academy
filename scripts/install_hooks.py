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
# Git pre-commit hook: быстрая проверка синтаксиса (< 0.5с)

# Попытка запустить быстрый валидатор на Python (если python/python3 доступен)
PYTHON_BIN=""
if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

if [ -n "$PYTHON_BIN" ] && [ -f "scripts/quick_precommit_check.py" ]; then
  "$PYTHON_BIN" scripts/quick_precommit_check.py
  exit $?
fi

# Fallback: чистая shell-проверка если Python недоступен в текущей сессии shell
js_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.js$')
for f in $js_files; do
  if [ -f "$f" ]; then
    node --check "$f" || { echo "[HOOK ERROR] Ошибка синтаксиса JS в $f"; exit 1; }
  fi
done

json_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.json$')
for f in $json_files; do
  if [ -f "$f" ]; then
    node -e "JSON.parse(require('fs').readFileSync('$f', 'utf8'))" || { echo "[HOOK ERROR] Ошибка синтаксиса JSON в $f"; exit 1; }
  fi
done

echo "✓ [Pre-Commit] Синтаксическая проверка пройдена (fallback mode)."
exit 0
"""

PRE_COMMIT_BAT = """@echo off
rem Git pre-commit hook for Windows cmd
python "%~dp0..\\..\\scripts\\quick_precommit_check.py"
if errorlevel 1 exit /b 1
exit /b 0
"""

QUICK_CHECK_PY = r'''#!/usr/bin/env python3
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
'''


def install():
    if not os.path.isdir(_HOOKS_DIR):
        print(f"Каталог хуков не найден: {_HOOKS_DIR}")
        return False

    # 1. Shell pre-commit hook (Git Bash / Linux / macOS)
    hook_path = os.path.join(_HOOKS_DIR, 'pre-commit')
    with open(hook_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PRE_COMMIT_SHELL)

    # Make executable on Unix/Git Bash
    try:
        os.chmod(hook_path, 0o755)
    except Exception:
        pass

    # 2. Windows batch pre-commit hook (cmd / GUI tools)
    bat_hook_path = os.path.join(_HOOKS_DIR, 'pre-commit.bat')
    with open(bat_hook_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(PRE_COMMIT_BAT)

    # 3. Quick check script for windows/cross-platform
    quick_py_path = os.path.join(_ROOT, 'scripts', 'quick_precommit_check.py')
    with open(quick_py_path, 'w', encoding='utf-8') as f:
        f.write(QUICK_CHECK_PY)

    print(f"✓ Git pre-commit hook успешно установлен в {hook_path}")
    print(f"✓ Git pre-commit.bat успешно установлен в {bat_hook_path}")
    print(f"✓ Вспомогательный скрипт сохранён в {quick_py_path}")
    return True


if __name__ == '__main__':
    install()
