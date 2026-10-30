#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py

Кроссплатформенный мастер-конвейер верификации данных, синтаксиса и задач
платформы Python Backend Academy (без UI/DOM и браузерных тестов).

Этапы:
[1/3] Проверка архива RemNote Platinum 525 файлов и карточек (verify_platinum.py)
[2/3] Проверка идентичности эталона и синтаксиса JS/архива (verify_academy.py)
[3/3] Запуск 401 задачи IDE и 459 сниппетов конспектов (test_all_401_tasks.py)

Опции:
  --full: дополнительно запустить аудит всех Python-скриптов конвейера (audit_pipeline.py)
  --quick: быстрый прогон без этапа 3 (401 задача IDE)
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
        'num': '1/3',
        'title': 'RemNote Platinum 525-file Package and Card Verification',
        'cmd': [sys.executable, os.path.join(_SCRIPTS, 'verify_platinum.py')],
        'quick': True
    },
    {
        'num': '2/3',
        'title': 'Canonical Benchmark and JS Syntax Verification',
        'cmd': [sys.executable, os.path.join(_SCRIPTS, 'verify_academy.py')],
        'quick': True
    },
    {
        'num': '3/3',
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
    parser = argparse.ArgumentParser(description='Мастер-конвейер верификации Python Backend Academy (без UI-тестов)')
    parser.add_argument('--full', '-f', action='store_true', help='Запустить полный аудит Python-скриптов конвейера')
    parser.add_argument('--quick', '-q', action='store_true', help='Быстрый прогон без этапа 3 (401 задача IDE)')
    args = parser.parse_args()

    print('========================================================', flush=True)
    print('  PYTHON BACKEND ACADEMY — ПРОВЕРКА КОНВЕЙЕРА (NO UI)', flush=True)
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
        print(f"\n[BONUS] Running full audit of pipeline Python scripts (audit_pipeline.py)...")
        b_start = time.time()
        res = subprocess.run([sys.executable, os.path.join(_SCRIPTS, 'audit_pipeline.py')], cwd=_ROOT)
        b_elapsed = time.time() - b_start
        if res.returncode != 0:
            print(f"\n[FAIL] Full pipeline audit FAILED ({b_elapsed:.2f}s)!")
            sys.exit(1)
        timings.append(('BONUS', 'All Pipeline Python Scripts Audit', b_elapsed))

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