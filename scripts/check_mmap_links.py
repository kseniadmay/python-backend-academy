import json
import re

map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'
json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'

with open(map_path, 'r', encoding='utf-8') as f:
    text = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

notes_map = set(renaming_map['notes'].values())
cards_map = set(renaming_map['cards'].values())

k_links = re.findall(r'\[\[(К-\d+\.[^\]]+)\]\]', text)
f_links = re.findall(r'\[\[(Ф-\d+\.[^\]]+)\]\]', text)

print(f'Total K-links in Mastery Map: {len(k_links)}, unique: {len(set(k_links))}')
print(f'Total F-links in Mastery Map: {len(f_links)}, unique: {len(set(f_links))}')

unmatched_k = [l for l in set(k_links) if l not in notes_map]
unmatched_f = [l for l in set(f_links) if l not in cards_map]

print(f'Unmatched K-links: {len(unmatched_k)}')
if unmatched_k:
    print('Sample unmatched K:', unmatched_k[:5])
print(f'Unmatched F-links: {len(unmatched_f)}')
if unmatched_f:
    print('Sample unmatched F:', unmatched_f[:5])
