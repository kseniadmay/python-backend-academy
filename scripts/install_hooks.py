#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_hooks.py

Установщик легковесных Git-хуков (pre-commit) для защиты проекта
от синтаксических ошибок в JavaScript, Python и JSON.
Ссылается на единый канонический скрипт scripts/quick_precommit_check.py без дублирования его кода (DRY).
"""

import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HOOKS_DIR = os.path.join(_ROOT, '.git', 'hooks')
_QUICK_CHECK_PATH = os.path.join(_ROOT, 'scripts', 'quick_precommit_check.py')

PRE_COMMIT_SHELL = """#!/bin/sh
# Git pre-commit hook: быстрая проверка синтаксиса (< 0.5с)

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


def install() -> bool:
    if not os.path.isdir(_HOOKS_DIR):
        print(f'Каталог хуков не найден: {_HOOKS_DIR}')
        return False

    if not os.path.isfile(_QUICK_CHECK_PATH):
        raise FileNotFoundError(f'Канонический скрипт проверки не найден: {_QUICK_CHECK_PATH}')

    # 1. Shell pre-commit hook (Git Bash / Linux / macOS)
    hook_path = os.path.join(_HOOKS_DIR, 'pre-commit')
    with open(hook_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PRE_COMMIT_SHELL)

    try:
        os.chmod(hook_path, 0o755)
    except Exception:
        pass

    # 2. Windows batch pre-commit hook (cmd / GUI tools)
    bat_hook_path = os.path.join(_HOOKS_DIR, 'pre-commit.bat')
    with open(bat_hook_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(PRE_COMMIT_BAT)

    print(f'✓ Git pre-commit hook успешно установлен в {hook_path}')
    print(f'✓ Git pre-commit.bat успешно установлен в {bat_hook_path}')
    print(f'✓ Используется единый скрипт проверки: {_QUICK_CHECK_PATH}')
    return True


if __name__ == '__main__':
    install()
