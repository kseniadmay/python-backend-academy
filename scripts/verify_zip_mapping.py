import zipfile
import json
import os
import re

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
map_json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'

with open(map_json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

notes_map = renaming_map['notes']
cards_map = renaming_map['cards']

with zipfile.ZipFile(remnote_python_zip) as z:
    note_files = [n for n in z.namelist() if 'Конспекты' in n and n.endswith('.md')]
    card_files = [n for n in z.namelist() if 'Карточки' in n and n.endswith('.md')]
    
    print('Testing Notes mapping:')
    unmatched_notes = []
    for nf in note_files:
        bn = os.path.basename(nf)[:-3]
        clean_bn = re.sub(r'^\d+\.\s*', '', bn).strip()
        matched = False
        for k, v in notes_map.items():
            if k == clean_bn or k.lower() == clean_bn.lower() or k.replace('_', ' ') == clean_bn.replace('_', ' '):
                matched = True
                break
        if not matched:
            unmatched_notes.append((nf, clean_bn))
            
    print(f'Unmatched notes: {len(unmatched_notes)}')
    if unmatched_notes:
        for u in unmatched_notes[:5]:
            print(' ', u)
            
    print('\nTesting Cards mapping:')
    unmatched_cards = []
    for cf in card_files:
        bn = os.path.basename(cf)[:-3]
        clean_bn = re.sub(r'^Ф-\d+\.\s*', '', bn).strip()
        matched = False
        for k, v in cards_map.items():
            if k == clean_bn or k.lower() == clean_bn.lower():
                matched = True
                break
        if not matched:
            unmatched_cards.append((cf, clean_bn))
            
    print(f'Unmatched cards: {len(unmatched_cards)}')
    if unmatched_cards:
        for u in unmatched_cards[:5]:
            print(' ', u)
