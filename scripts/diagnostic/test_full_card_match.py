import zipfile
import json
import os
import re

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
map_json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'

with open(map_json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

cards_map = renaming_map['cards']

with zipfile.ZipFile(remnote_python_zip) as z:
    card_files = [n for n in z.namelist() if 'Карточки' in n and n.endswith('.md')]
    matched_cards = set()
    unmatched = []
    for cf in card_files:
        bn = os.path.basename(cf)[:-3]
        clean_bn = re.sub(r'^Ф-\d+\.\s*', '', bn).strip()
        matched = False
        for k, v in cards_map.items():
            if k == clean_bn or k.lower() == clean_bn.lower():
                matched_cards.add(v)
                matched = True
                break
        if not matched:
            unmatched.append(cf)
            
    print(f'Matched unique cards: {len(matched_cards)} out of {len(card_files)}')
    print(f'Unmatched count: {len(unmatched)}')
    if unmatched:
        for u in unmatched:
            print(' ', u)
