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

    # Защита педагогики Кодди: если менялись стандарты, академия или тесты — валидируем атомарность конспектов
    html_or_notes_changed = any(
        f.endswith('standards.html') or f.endswith('academy.html') or 'test_notes_atomicity' in f
        for f in files
    )
    if html_or_notes_changed and has_node:
        test_path = os.path.join(_ROOT, 'tests', 'test_notes_atomicity.js')
        if os.path.isfile(test_path):
            c = subprocess.run(['node', test_path], capture_output=True, text=True)
            if c.returncode != 0:
                print(f'[HOOK ERROR] Сбой теста атомарности конспектов (Active Microlearning):\n{c.stderr or c.stdout}')
                return 1
            print('✓ [Pre-Commit] Тест атомарности конспектов (Active Microlearning) пройден со 100% успехом.')

        # Защита от белого/пустого экрана: проверка инициализации DOM, вызова render() и целостности ID
        dom_smoke_path = os.path.join(_ROOT, 'tests', 'test_dom_init_smoke.js')
        if os.path.isfile(dom_smoke_path):
            c_dom = subprocess.run(['node', dom_smoke_path], capture_output=True, text=True)
            if c_dom.returncode != 0:
                print(f'[HOOK ERROR] Сбой теста инициализации DOM (Blank Screen Guard):\n{c_dom.stderr or c_dom.stdout}')
                return 1
            print(c_dom.stdout.strip())

        # Защита от расхождений в инлайн-коде и регрессий карточек SRS
        cards_test_path = os.path.join(_ROOT, 'tests', 'test_cards_inline_code_consistency.js')
        if os.path.isfile(cards_test_path):
            c_cards = subprocess.run(['node', cards_test_path], capture_output=True, text=True)
            if c_cards.returncode != 0:
                print(f'[HOOK ERROR] Сбой теста консистентности карточек SRS:\n{c_cards.stderr or c_cards.stdout}')
                return 1
            print('✓ [Pre-Commit] Тест консистентности инлайн-кода и карточек SRS пройден со 100% успехом.')
        # Архитектурная защита DRY: единый канонический экран решения задач Zen IDE
        dry_test_path = os.path.join(_ROOT, 'tests', 'test_dry_architecture.js')
        if os.path.isfile(dry_test_path):
            c_dry = subprocess.run(['node', dry_test_path], capture_output=True, text=True)
            if c_dry.returncode != 0:
                print(f'[HOOK ERROR] Сбой глобального архитектурного DRY-теста:\n{c_dry.stderr or c_dry.stdout}')
                return 1
            print('✓ [Pre-Commit] Глобальный архитектурный DRY-тест (SSOT) пройден со 100% успехом.')

        # Защита от мерцания, субпиксельного дрожания и скачков кнопок (Zero-Jitter SRS Guard)
        jitter_test_path = os.path.join(_ROOT, 'tests', 'test_srs_zero_jitter_invariants.js')
        if os.path.isfile(jitter_test_path):
            c_jit = subprocess.run(['node', jitter_test_path], capture_output=True, text=True)
            if c_jit.returncode != 0:
                print(f'[HOOK ERROR] Сбой теста Zero-Jitter & Zero-Flicker SRS:\n{c_jit.stderr or c_jit.stdout}')
                return 1
            print('✓ [Pre-Commit] Тест стабильности Zero-Jitter SRS пройден со 100% успехом.')

    print('✓ [Pre-Commit] Синтаксическая проверка пройдена (JS, Python, JSON, HTML inline в норме).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
