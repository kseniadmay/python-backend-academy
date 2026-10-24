import json
import logging
import os
import sys
import time
from pathlib import Path

# Добавляем корень проекта и папку scripts в sys.path
_SCRIPTS_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _SCRIPTS_DIR.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from extract_remnote_data import (
    BASE_REMNOTE,
    TASKS_381,
    f_files_map,
    k_files_map,
    parse_f_deck,
    parse_k_note,
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('export_content')


def export_canonical_content() -> None:
    start_time = time.time()
    content_dir = _ROOT_DIR / 'data' / 'content'
    content_dir.mkdir(parents=True, exist_ok=True)

    logger.info('Начало экспорта и нормализации контента в %s', content_dir)

    # 1. Экспорт 401 задачи
    logger.info('Обработка 401 задачи тренажера...')
    tasks_list = []
    for t in TASKS_381:
        tasks_list.append({
            'id': t['id'],
            'title': t.get('title', ''),
            'level': t.get('level', 1),
            'tier': t.get('tier', '🥚 Уровень 1'),
            'topic': t.get('topic', '🐍 Python Core'),
            'desc': t.get('desc', ''),
            'initialCode': t.get('initialCode', ''),
            'solution': t.get('solution', ''),
            'hint': t.get('hint', ''),
            'tests': t.get('tests', '')
        })

    tasks_file = content_dir / 'tasks.json'
    with open(tasks_file, 'w', encoding='utf-8') as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=2)
    logger.info('✓ Сохранено %d задач в %s', len(tasks_list), tasks_file.name)

    # 2. Экспорт 238 конспектов (К-*)
    logger.info('Парсинг и квантование 238 конспектов...')
    notes_dict = {}
    for cid in sorted(k_files_map.keys()):
        parsed = parse_k_note(cid)
        notes_dict[cid] = parsed

    notes_file = content_dir / 'notes.json'
    with open(notes_file, 'w', encoding='utf-8') as f:
        json.dump(notes_dict, f, ensure_ascii=False, indent=2)
    logger.info('✓ Сохранено %d конспектов в %s', len(notes_dict), notes_file.name)

    # 3. Экспорт 286 колод флеш-карточек (Ф-*)
    logger.info('Парсинг 286 колод флеш-карточек...')
    cards_dict = {}
    total_card_items = 0
    for fid in sorted(f_files_map.keys()):
        # Если ключ содержит '@', передаем fid и module
        if '@' in fid:
            raw_fid, mod = fid.split('@', 1)
            parsed = parse_f_deck(raw_fid, module=mod)
        else:
            parsed = parse_f_deck(fid)
        cards_dict[fid] = parsed
        total_card_items += len(parsed.get('cards', []))

    cards_file = content_dir / 'cards.json'
    with open(cards_file, 'w', encoding='utf-8') as f:
        json.dump(cards_dict, f, ensure_ascii=False, indent=2)
    logger.info('✓ Сохранено %d колод (%d карточек) в %s', len(cards_dict), total_card_items, cards_file.name)

    # 4. Сводный манифест
    manifest = {
        'version': '1.0.0',
        'exportedAt': time.strftime('%Y-%m-%d %H:%M:%S'),
        'totalTasks': len(tasks_list),
        'totalNotes': len(notes_dict),
        'totalDecks': len(cards_dict),
        'totalFlashcards': total_card_items,
        'modules': [
            {'id': '01', 'title': 'Python Core', 'icon': '🐍'},
            {'id': '02', 'title': 'Web Technologies', 'icon': '🌐'},
            {'id': '03', 'title': 'Backend Architecture', 'icon': '⚙️'},
            {'id': '04', 'title': 'Algorithms & Data Structures', 'icon': '⚡'},
            {'id': '05', 'title': 'Databases & SQL', 'icon': '🗄️'},
            {'id': '06', 'title': 'Software Architecture', 'icon': '🏛️'},
            {'id': '07', 'title': 'Infrastructure & DevOps', 'icon': '🚀'},
        ]
    }
    manifest_file = content_dir / 'manifest.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    logger.info('✓ Сохранен манифест контента в %s', manifest_file.name)

    elapsed = time.time() - start_time
    logger.info('========================================================')
    logger.info('🎉 Экспорт и нормализация завершены за %.2f сек!', elapsed)
    logger.info('========================================================')


if __name__ == '__main__':
    export_canonical_content()
