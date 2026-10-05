#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_pipeline.py

Скрипт сквозного аудита и верификации всех тестовых и сборочных скриптов
проекта Python Backend Academy.

Возможности:
- Авто-обнаружение всех скриптов по паттернам test_*, verify_*, check_*, audit_*.
- Параллельное выполнение через ThreadPoolExecutor (флаг --parallel, по умолчанию 4 воркера).
- Наглядный вывод прогресса, таймингов и цветовая индикация.
- Фильтрация по имени (--filter).
- Возврат кода 0 только при 100% успешном прохождении всех скриптов.
"""

import os
import sys
import time
import glob
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

_CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS_DIR = os.path.join(_CWD, 'scripts')

PATTERNS = [
    'test_*.py', 'test_*.js',
    'verify_*.py', 'verify_*.js',
    'check_*.py',
    'audit_*.py', 'audit_*.js'
]

HEAVY_SCRIPTS = {
    'test_all_401_tasks.py': 80,
    'verify_academy.py': 70,
    'audit_pipeline.py': 0  # исключаем сам себя из рекурсивного аудита
}


def discover_scripts(filter_sub=None):
    found = set()
    for pat in PATTERNS:
        for f in glob.glob(os.path.join(_SCRIPTS_DIR, pat)):
            base = os.path.basename(f)
            if base == 'audit_pipeline.py':
                continue
            if filter_sub and filter_sub.lower() not in base.lower():
                continue
            found.add(base)
    return sorted(found)


def run_single_script(script_name, verbose=False):
    full_path = os.path.join(_SCRIPTS_DIR, script_name)
    is_js = script_name.endswith('.js')
    cmd = ['node', full_path] if is_js else [sys.executable, full_path]

    timeout = HEAVY_SCRIPTS.get(script_name, 15)

    start = time.time()
    try:
        res = subprocess.run(
            cmd,
            cwd=_CWD,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='ignore'
        )
        elapsed = time.time() - start
        if res.returncode == 0:
            return {
                'name': script_name,
                'status': 'PASS',
                'code': 0,
                'time': elapsed,
                'out': res.stdout,
                'err': ''
            }
        else:
            err_line = (res.stderr or res.stdout).strip().split('\n')[-1]
            return {
                'name': script_name,
                'status': 'FAIL',
                'code': res.returncode,
                'time': elapsed,
                'out': res.stdout,
                'err': err_line[:140]
            }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return {
            'name': script_name,
            'status': 'TIMEOUT',
            'code': -1,
            'time': elapsed,
            'out': '',
            'err': f'Timeout exceeded ({timeout}s)'
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            'name': script_name,
            'status': 'ERROR',
            'code': -2,
            'time': elapsed,
            'out': '',
            'err': str(e)[:140]
        }


def main():
    parser = argparse.ArgumentParser(description='Сквозной аудит всех тестовых скриптов конвейера.')
    parser.add_argument('--filter', type=str, default=None, help='Фильтр по имени скрипта')
    parser.add_argument('--parallel', '-p', action='store_true', default=True, help='Параллельный запуск (по умолчанию включён)')
    parser.add_argument('--workers', '-w', type=int, default=4, help='Количество воркеров (по умолчанию 4)')
    parser.add_argument('--sequential', '-s', action='store_true', help='Последовательный запуск вместо параллельного')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод результатов каждого теста')
    args = parser.parse_args()

    scripts = discover_scripts(args.filter)
    total = len(scripts)
    if total == 0:
        print("Не найдено скриптов для проверки.")
        sys.exit(0)

    use_parallel = args.parallel and not args.sequential and total > 1
    workers = min(args.workers, total) if use_parallel else 1

    print('========================================================')
    print(f'  АУДИТ КОНВЕЙЕРА: {total} скриптов (Воркеры: {workers if use_parallel else 1})')
    print('========================================================')

    results = []
    start_total = time.time()

    if use_parallel:
        # Для параллельного запуска сначала запускаем тяжёлые скрипты, чтобы они не задерживали хвост
        sorted_scripts = sorted(scripts, key=lambda s: 0 if s in HEAVY_SCRIPTS else 1)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_script = {executor.submit(run_single_script, s, args.verbose): s for s in sorted_scripts}
            done_count = 0
            for future in as_completed(future_to_script):
                r = future.result()
                results.append(r)
                done_count += 1
                status_icon = '✓' if r['status'] == 'PASS' else '✗'
                print(f"[{done_count:02d}/{total:02d}] {status_icon} {r['name']:<35} {r['status']:<7} ({r['time']:.2f}s)")
                if r['status'] != 'PASS' and r['err']:
                    print(f"       └── Ошибка: {r['err']}")
    else:
        for idx, s in enumerate(scripts, 1):
            r = run_single_script(s, args.verbose)
            results.append(r)
            status_icon = '✓' if r['status'] == 'PASS' else '✗'
            print(f"[{idx:02d}/{total:02d}] {status_icon} {r['name']:<35} {r['status']:<7} ({r['time']:.2f}s)")
            if r['status'] != 'PASS' and r['err']:
                print(f"       └── Ошибка: {r['err']}")

    total_time = time.time() - start_total
    passed = [r for r in results if r['status'] == 'PASS']
    failed = [r for r in results if r['status'] in ('FAIL', 'ERROR')]
    timed_out = [r for r in results if r['status'] == 'TIMEOUT']

    print('\n========================================================')
    print(f'ИТОГ АУДИТА: {len(passed)}/{total} PASS (Успех: {len(passed)/total*100:.1f}%)')
    print(f'Общее время выполнения: {total_time:.2f}s')
    print('========================================================')

    if failed:
        print('\n[ОШИБКИ]')
        for f in failed:
            print(f"- {f['name']} (код {f['code']}): {f['err']}")

    if timed_out:
        print('\n[ТАЙМАУТЫ]')
        for t in timed_out:
            print(f"- {t['name']}")

    if len(passed) == total:
        print('\n✓ 100% ВСЕХ СКРИПТОВ КОНВЕЙЕРА УСПЕШНО ПРОЙДЕНЫ!\n')
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
