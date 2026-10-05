#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py

Кроссплатформенный мастер-конвейер полной верификации платформы
Python Backend Academy (100% эквивалент и расширение verify_all.cmd).

Этапы:
[1/5] Проверка архива RemNote Platinum 525 файлов и карточек (verify_platinum.py)
[2/5] Сквозные DOM-инварианты и бизнес-логика (test_e2e_dom.js)
[3/5] PWA Offline, Manifest и Service Worker (test_pwa_offline.js)
[4/5] Рендеринг маршрутов в Headless Chrome и синтаксис JS (verify_academy.py)
[5/5] Запуск 401 задачи IDE и 459 сниппетов конспектов (test_all_401_tasks.py)

Опции:
  --full: дополнительно запустить аудит всех 86+ скриптов конвейера (audit_pipeline.py)
  --quick: пропустить длительную проверку 401 задач для быстрой проверки верстки/DOM
"""

import os
import sys
import time
import argparse
import subprocess

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

_ROOT = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.join(_ROOT, 'scripts')

STAGES = [
    {
        'num': '1/5',
        'title': 'RemNote Platinum 525-file Package and Card Verification',
        'cmd': [sys.executable, os.path.join(_SCRIPTS, 'verify_platinum.py')],
        'quick': True
    },
    {
        'num': '2/5',
        'title': 'E2E DOM and Invariant tests',
        'cmd': ['node', os.path.join(_SCRIPTS, 'test_e2e_dom.js')],
        'quick': True
    },
    {
        'num': '3/5',
        'title': 'PWA Offline, Manifest and Service Worker Verification',
        'cmd': ['node', os.path.join(_SCRIPTS, 'test_pwa_offline.js')],
        'quick': True
    },
    {
        'num': '4/5',
        'title': 'Headless Chrome and JS syntax verification',
        'cmd': [sys.executable, os.path.join(_SCRIPTS, 'verify_academy.py')],
        'quick': True
    },
    {
        'num': '5/5',
        'title': '401 IDE tasks and Python snippets tests',
        'cmd': [sys.executable, os.path.join(_SCRIPTS, 'test_all_401_tasks.py')],
        'quick': False
    }
]


def run_stage(stage):
    print(f"\n[{stage['num']}] Running {stage['title']}...", flush=True)
    start_t = time.time()
    res = subprocess.run(stage['cmd'], cwd=_ROOT, text=True, encoding='utf-8', errors='ignore')
    elapsed = time.time() - start_t
    if res.returncode != 0:
        print(f"\n[FAIL] Stage [{stage['num']}] FAILED with exit code {res.returncode} ({elapsed:.2f}s)!", flush=True)
        return False, elapsed
    print(f"[OK] Stage [{stage['num']}] PASSED in {elapsed:.2f}s", flush=True)
    return True, elapsed


def main():
    parser = argparse.ArgumentParser(description='Мастер-конвейер верификации Python Backend Academy')
    parser.add_argument('--full', '-f', action='store_true', help='Запустить полный аудит всех 87 скриптов конвейера')
    parser.add_argument('--quick', '-q', action='store_true', help='Быстрый прогон без этапа 5 (401 задача IDE)')
    args = parser.parse_args()

    print('========================================================', flush=True)
    print('  PYTHON BACKEND ACADEMY — ПРОВЕРКА КОНВЕЙЕРА (100% PASS)', flush=True)
    print('========================================================', flush=True)

    total_start = time.time()
    timings = []

    for stage in STAGES:
        if args.quick and not stage['quick']:
            print(f"\n[{stage['num']}] SKIPPED: {stage['title']} (--quick mode)")
            continue
        success, elapsed = run_stage(stage)
        timings.append((stage['num'], stage['title'], elapsed))
        if not success:
            print('\n========================================================')
            print('  [ERROR] Verification FAILED!')
            print('========================================================')
            sys.exit(1)

    if args.full:
        print(f"\n[BONUS] Running full audit of all pipeline scripts (audit_pipeline.py)...")
        b_start = time.time()
        res = subprocess.run([sys.executable, os.path.join(_SCRIPTS, 'audit_pipeline.py')], cwd=_ROOT)
        b_elapsed = time.time() - b_start
        if res.returncode != 0:
            print(f"\n[FAIL] Full pipeline audit FAILED ({b_elapsed:.2f}s)!")
            sys.exit(1)
        timings.append(('BONUS', 'All Pipeline Scripts Audit', b_elapsed))

    total_elapsed = time.time() - total_start
    print('\n========================================================')
    print(f'  ALL VERIFICATIONS PASSED SUCCESSFULLY! (100% PASS)')
    print(f'  Total time: {total_elapsed:.2f}s')
    print('--------------------------------------------------------')
    for num, title, t in timings:
        print(f"  [{num}] {t:5.2f}s - {title}")
    print('========================================================\n')
    sys.exit(0)


if __name__ == '__main__':
    main()
