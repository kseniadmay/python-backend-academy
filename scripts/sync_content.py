#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_content.py

Единый синхронизатор учебных материалов: переносит правки из data/content/
(notes.json, cards.json, tasks.json) и файлов рубежных тестов в канонический
standards/standards.html (с безопасной экранизацией safe_js_json) и побайтово
копирует результат в academy.html.
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import audit_content_acceptance as aca  # noqa: E402

ACADEMY_HTML = ROOT_DIR / 'academy.html'


def safe_js_json(obj: Any) -> str:
    """Сериализует JSON безопасно для встраивания внутрь <script> в HTML."""
    return (
        json.dumps(obj, ensure_ascii=False)
        .replace('</script', '<\\/script')
        .replace('</SCRIPT', '<\\/SCRIPT')
    )


def _replace_js_json_block(html_text: str, var_name: str, expected_first_char: str, updater) -> tuple[str, int]:
    """Декодирует const <var_name> = ..., применяет updater и сериализует обратно."""
    marker = f'const {var_name} ='
    idx = html_text.find(marker)
    if idx == -1:
        raise RuntimeError(f'{marker} не найден в {aca.STANDARDS_HTML}')
    start = html_text.find(expected_first_char, idx)
    if start == -1:
        raise RuntimeError(f'Не найдено начало JSON ({expected_first_char}) для {var_name}')
    decoder = json.JSONDecoder()
    obj, end = decoder.raw_decode(html_text, start)
    changed = updater(obj)
    if not changed:
        return html_text, 0
    serialized = safe_js_json(obj)
    return html_text[:start] + serialized + html_text[end:], changed


def main() -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Синхронизация notes/cards/tasks/unitTests в standards/standards.html и academy.html',
    )
    parser.add_argument('--notes', help='Список ID конспектов через запятую (например: К-001,К-002)')
    parser.add_argument('--all-notes', action='store_true', help='Синхронизировать все конспекты из notes.json')
    parser.add_argument('--decks', help='Список ID колод через запятую (например: Ф-005,Ф-092)')
    parser.add_argument('--all-decks', action='store_true', help='Синхронизировать все колоды из cards.json')
    parser.add_argument('--tasks', help='Список ID задач через запятую (например: 92,350)')
    parser.add_argument('--all-tasks', action='store_true', help='Синхронизировать все задачи из tasks.json')
    parser.add_argument('--unit-tests', dest='unit_tests_path', help='Путь к JSON вида {"unit_id": {...}}')
    args = parser.parse_args()

    note_ids = {s.strip() for s in args.notes.split(',') if s.strip()} if args.notes else set()
    deck_ids = {s.strip() for s in args.decks.split(',') if s.strip()} if args.decks else set()
    task_ids = {int(s.strip()) for s in args.tasks.split(',') if s.strip()} if args.tasks else set()

    if not any([args.all_notes, note_ids, args.all_decks, deck_ids, args.all_tasks, task_ids, args.unit_tests_path]):
        parser.print_help()
        return 1

    notes_data = json.loads((aca.CONTENT_DIR / 'notes.json').read_text(encoding='utf-8'))
    cards_data = json.loads((aca.CONTENT_DIR / 'cards.json').read_text(encoding='utf-8'))
    tasks_list = json.loads((aca.CONTENT_DIR / 'tasks.json').read_text(encoding='utf-8'))
    tasks_by_id = {t['id']: t for t in tasks_list}

    unit_tests_patch: dict[str, dict] = {}
    if args.unit_tests_path:
        ut_path = Path(args.unit_tests_path)
        if not ut_path.is_file():
            print(f'Ошибка: не найден файл тестов {ut_path}')
            return 1
        unit_tests_patch = json.loads(ut_path.read_text(encoding='utf-8'))

    html_text = aca.STANDARDS_HTML.read_text(encoding='utf-8')
    stats = {'notes': 0, 'decks': 0, 'tasks': 0, 'unit_tests': 0}

    if args.all_notes or note_ids or args.all_decks or deck_ids or unit_tests_patch:
        for m_name in aca.MASTERY_NAMES:
            def _update_mastery(obj: dict[str, Any]) -> int:
                changes = 0
                m_notes = obj.get('notes', {})
                target_notes = list(m_notes.keys()) if args.all_notes else sorted(note_ids)
                for kid in target_notes:
                    if kid in m_notes and kid in notes_data:
                        m_notes[kid] = notes_data[kid]
                        stats['notes'] += 1
                        changes += 1

                m_decks = obj.get('decks', {})
                target_decks = list(m_decks.keys()) if args.all_decks else sorted(deck_ids)
                for fid in target_decks:
                    if fid in m_decks and fid in cards_data:
                        m_decks[fid] = cards_data[fid]
                        stats['decks'] += 1
                        changes += 1

                if unit_tests_patch:
                    unit_ids_in_track = {u['id'] for u in obj.get('units', [])}
                    m_utests = obj.setdefault('unitTests', {})
                    for uid, ut_obj in unit_tests_patch.items():
                        if uid in unit_ids_in_track or uid in m_utests:
                            m_utests[uid] = ut_obj
                            stats['unit_tests'] += 1
                            changes += 1
                return changes

            html_text, _ = _replace_js_json_block(html_text, m_name, '{', _update_mastery)

    if args.all_tasks or task_ids:
        def _update_tasks(ide_arr: list[dict[str, Any]]) -> int:
            changes = 0
            for idx, existing in enumerate(ide_arr):
                tid = existing.get('id')
                if not (args.all_tasks or tid in task_ids):
                    continue
                src = tasks_by_id.get(tid)
                if not src:
                    continue
                merged = dict(existing)
                merged.update(src)
                merged['code'] = src['solution']
                ide_arr[idx] = merged
                stats['tasks'] += 1
                changes += 1
            return changes

        html_text, _ = _replace_js_json_block(html_text, 'IDE_TASKS', '[', _update_tasks)

    aca.STANDARDS_HTML.write_text(html_text, encoding='utf-8')
    shutil.copyfile(aca.STANDARDS_HTML, ACADEMY_HTML)
    assert aca.STANDARDS_HTML.read_bytes() == ACADEMY_HTML.read_bytes(), 'Ошибка побайтовой синхронизации academy.html!'

    print(
        f'Синхронизация завершена: notes={stats["notes"]}, decks={stats["decks"]}, '
        f'tasks={stats["tasks"]}, unitTests={stats["unit_tests"]} | standards.html == academy.html'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
