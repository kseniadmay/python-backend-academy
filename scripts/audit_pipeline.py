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

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

_CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS_DIR = os.path.join(_CWD, 'scripts')

PATTERNS = [
    'test_*.py', 'test_*.js',
    'verify_*.py', 'verify_*.js',
    'check_*.py',
    'audit_*.py', 'audit_*.js',
    'quick_*.py'
]

HEAVY_SCRIPTS = {
    'test_all_401_tasks.py': 120,
    'verify_academy.py': 90,
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

    timeout = HEAVY_SCRIPTS.get(script_name, 35)

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
                'err': '',
                'full_err': ''
            }
        else:
            raw_err = (res.stderr or res.stdout).strip()
            err_line = raw_err.split('\n')[-1] if raw_err else f'Exit code {res.returncode}'
            return {
                'name': script_name,
                'status': 'FAIL',
                'code': res.returncode,
                'time': elapsed,
                'out': res.stdout,
                'err': err_line[:140],
                'full_err': raw_err
            }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return {
            'name': script_name,
            'status': 'TIMEOUT',
            'code': -1,
            'time': elapsed,
            'out': '',
            'err': f'Timeout exceeded ({timeout}s)',
            'full_err': f'Script timed out after {timeout} seconds'
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            'name': script_name,
            'status': 'ERROR',
            'code': -2,
            'time': elapsed,
            'out': '',
            'err': str(e)[:140],
            'full_err': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Сквозной аудит всех тестовых скриптов конвейера.')
    parser.add_argument('--filter', type=str, default=None, help='Фильтр по имени скрипта')
    parser.add_argument('--parallel', '-p', action='store_true', default=True, help='Параллельный запуск (по умолчанию включён)')
    parser.add_argument('--workers', '-w', type=int, default=4, help='Количество воркеров (по умолчанию 4)')
    parser.add_argument('--sequential', '-s', action='store_true', help='Последовательный запуск вместо параллельного')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод результатов и логов каждого теста')
    parser.add_argument('--fail-fast', '-f', action='store_true', help='Немедленно прервать прогон при первой ошибке')
    args = parser.parse_args()

    scripts = discover_scripts(args.filter)
    total = len(scripts)
    if total == 0:
        print("Не найдено скриптов для проверки.", flush=True)
        sys.exit(0)

    use_parallel = args.parallel and not args.sequential and total > 1
    workers = min(args.workers, total) if use_parallel else 1

    print('========================================================', flush=True)
    print(f'  АУДИТ КОНВЕЙЕРА: {total} скриптов (Воркеры: {workers if use_parallel else 1})', flush=True)
    print('========================================================', flush=True)

    results = []
    start_total = time.time()

    if use_parallel:
        sorted_scripts = sorted(scripts, key=lambda s: 0 if s in HEAVY_SCRIPTS else 1)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_script = {executor.submit(run_single_script, s, args.verbose): s for s in sorted_scripts}
            done_count = 0
            for future in as_completed(future_to_script):
                r = future.result()
                results.append(r)
                done_count += 1
                status_icon = '✓' if r['status'] == 'PASS' else '✗'
                print(f"[{done_count:02d}/{total:02d}] {status_icon} {r['name']:<35} {r['status']:<7} ({r['time']:.2f}s)", flush=True)
                if r['status'] != 'PASS':
                    print(f"       └── Ошибка: {r['err']}", flush=True)
                    if args.verbose and r.get('full_err'):
                        print(f"       └── Подробности:\n{r['full_err']}\n", flush=True)
                    if args.fail_fast:
                        print("\n[FAIL-FAST] Аудит прерван из-за сбоя теста.", flush=True)
                        break
    else:
        for idx, s in enumerate(scripts, 1):
            r = run_single_script(s, args.verbose)
            results.append(r)
            status_icon = '✓' if r['status'] == 'PASS' else '✗'
            print(f"[{idx:02d}/{total:02d}] {status_icon} {r['name']:<35} {r['status']:<7} ({r['time']:.2f}s)", flush=True)
            if r['status'] != 'PASS':
                print(f"       └── Ошибка: {r['err']}", flush=True)
                if args.verbose and r.get('full_err'):
                    print(f"       └── Подробности:\n{r['full_err']}\n", flush=True)
                if args.fail_fast:
                    print("\n[FAIL-FAST] Аудит прерван из-за сбоя теста.", flush=True)
                    break

    total_time = time.time() - start_total
    passed = [r for r in results if r['status'] == 'PASS']
    failed = [r for r in results if r['status'] in ('FAIL', 'ERROR')]
    timed_out = [r for r in results if r['status'] == 'TIMEOUT']

    print('\n========================================================', flush=True)
    print(f'ИТОГ АУДИТА: {len(passed)}/{total} PASS (Успех: {len(passed)/total*100:.1f}%)', flush=True)
    print(f'Общее время выполнения: {total_time:.2f}s', flush=True)
    print('========================================================', flush=True)

    if passed:
        print('\n[ТОП-5 САМЫХ ДЛИТЕЛЬНЫХ СКРИПТОВ]', flush=True)
        slowest = sorted(passed, key=lambda x: x['time'], reverse=True)[:5]
        for s in slowest:
            print(f"  {s['time']:5.2f}s - {s['name']}", flush=True)

    if failed:
        print('\n[ОШИБКИ]', flush=True)
        for f in failed:
            print(f"- {f['name']} (код {f['code']}): {f['err']}", flush=True)

    if timed_out:
        print('\n[ТАЙМАУТЫ]', flush=True)
        for t in timed_out:
            print(f"- {t['name']}", flush=True)

    if len(passed) == total:
        print('\n✓ 100% ВСЕХ СКРИПТОВ КОНВЕЙЕРА УСПЕШНО ПРОЙДЕНЫ!\n', flush=True)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
