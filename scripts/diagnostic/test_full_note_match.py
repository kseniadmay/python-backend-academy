import zipfile
import json
import os
import re

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
map_json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'

with open(map_json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

notes_map = renaming_map['notes']

def match_note(nf, first_line):
    bn = os.path.basename(nf)[:-3]
    clean_bn = re.sub(r'^\d+\.\s*', '', bn).strip()
    
    # Прямое совпадение
    for k, v in notes_map.items():
        if k == clean_bn or k.lower() == clean_bn.lower() or k.replace('_', ' ') == clean_bn.replace('_', ' '):
            return v
            
    # Совпадение по первой строке
    m = re.search(r'Перечитать конспект (.*?)→', first_line)
    if m:
        t = m.group(1).strip()
        t_clean = t.replace(':', '_').replace('–', '-').replace('—', '-')
        for k, v in notes_map.items():
            if k == t or k == t_clean or k.lower() == t.lower() or k.lower() == t_clean.lower():
                return v
                
    # Префиксное совпадение
    for k, v in notes_map.items():
        if k.startswith(clean_bn[:25]) or clean_bn.startswith(k[:25]):
            return v
            
    return None

with zipfile.ZipFile(remnote_python_zip) as z:
    note_files = [n for n in z.namelist() if 'Конспекты' in n and n.endswith('.md')]
    unmatched = []
    matched_names = set()
    for nf in note_files:
        first_line = z.read(nf).decode('utf-8').splitlines()[0]
        v = match_note(nf, first_line)
        if v:
            matched_names.add(v)
        else:
            unmatched.append((nf, first_line))
            
    print(f'Matched unique notes: {len(matched_names)} out of {len(note_files)}')
    print(f'Unmatched count: {len(unmatched)}')
    if unmatched:
        for u in unmatched:
            print(' ', u)
