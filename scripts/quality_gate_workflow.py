#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/quality_gate_workflow.py

Агентский конвейер для run_workflow: выполняет L1/L2-проверки через scripts/quality_gate.py,
распределяет смысловой аудит L3 по параллельным агентам (без внешних API-ключей)
и собирает итоговый паспорт качества в data/quality_ledger.json и data/quality_report.md.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _resolve_python() -> str:
    """Находит системный интерпретатор Python из PATH, минуя заглушку WindowsApps."""
    for name in ('python', 'python3'):
        candidate = shutil.which(name)
        if candidate and 'WindowsApps' not in candidate:
            return candidate
    return sys.executable


tier = str(args.get('tier', '1'))
skills = args.get('skills')
limit = args.get('limit')
force = bool(args.get('force', False))
agent_model = str(args.get('model', 'inherit'))

python_exe = _resolve_python()
base_cmd = [python_exe, 'scripts/quality_gate.py', '--tier', tier]
if skills:
    base_cmd.extend(['--skills', str(skills)])
if limit is not None:
    base_cmd.extend(['--limit', str(limit)])

with tempfile.TemporaryDirectory() as tmp_dir:
    tmp_path = Path(tmp_dir)
    queue_file = tmp_path / 'l3_queue.json'
    results_file = tmp_path / 'l3_results.json'

    phase('L1 + L2 и сбор очереди L3')
    export_cmd = list(base_cmd)
    if force:
        export_cmd.append('--force')
    export_cmd.extend(['--export-l3-queue', str(queue_file)])

    exp_proc = subprocess.run(export_cmd, capture_output=True, text=True, encoding='utf-8')
    if exp_proc.stdout:
        log(exp_proc.stdout.strip())
    if exp_proc.returncode != 0:
        raise RuntimeError(f'Ошибка export-l3-queue (код {exp_proc.returncode}): {exp_proc.stderr}')

    queue = json.loads(queue_file.read_text(encoding='utf-8'))
    items = queue.get('items', [])
    log(f'Навыков в очереди на смысловой аудит L3: {len(items)}')

    evaluations: dict = {}
    if items:
        phase('L3 Смысловой аудит агентами')
        system_prompt = queue['system_prompt']
        schema = queue['schema']

        def _make_agent(item: dict):
            prompt = (
                f'{system_prompt}\n\n'
                'ИНСТРУКЦИЯ ПО РАБОТЕ:\n'
                '- Все материалы навыка (Конспекты, Карточки, Практика, Рубежный тест) полностью приведены ниже.\n'
                '- НЕ читай файлы в репозитории и НЕ запускай дополнительные инструменты исследования.\n'
                '- Проанализируй материалы целиком и сразу верни структурированный итог строго через инструмент `finish` на русском языке.\n\n'
                f'{item["payload"]}'
            )
            return agent(
                prompt=prompt,
                schema=schema,
                role=f'Аудит {item["skill_id"]}',
                type_name='research',
                model=agent_model,
            )

        raw_results = await parallel(items, _make_agent)
        for item, res in zip(items, raw_results):
            res_obj = dict(res) if isinstance(res, dict) else json.loads(str(res))
            res_obj['model'] = f'antigravity-workflow/{agent_model}'
            evaluations[item['skill_id']] = res_obj
    else:
        log('Все выбранные навыки уже имеют актуальную L3-оценку в кэше.')

    phase('Импорт L3 и сборка паспорта')
    results_file.write_text(json.dumps({'results': evaluations}, ensure_ascii=False, indent=2), encoding='utf-8')
    import_cmd = list(base_cmd) + ['--import-l3-results', str(results_file)]
    imp_proc = subprocess.run(import_cmd, capture_output=True, text=True, encoding='utf-8')
    if imp_proc.stdout:
        print(imp_proc.stdout)
    if imp_proc.stderr:
        log(imp_proc.stderr.strip())
    if imp_proc.returncode != 0:
        raise RuntimeError(f'Ошибка import-l3-results (код {imp_proc.returncode}): {imp_proc.stderr}')
