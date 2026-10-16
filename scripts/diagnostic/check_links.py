import zipfile
import re
import os

zip_path = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Mastery_Import_Ready.zip'
map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'

with zipfile.ZipFile(zip_path) as z:
    all_files = set(z.namelist())

with open(map_path, 'r', encoding='utf-8') as f:
    text = f.read()

links = re.findall(r'\[\[(.*?)\]\]', text)
print(f'Total links found in Mastery Map: {len(links)}')

k_links = [l for l in links if l.startswith('К-')]
f_links = [l for l in links if l.startswith('Ф-')]
print(f'K-links: {len(k_links)}, F-links: {len(f_links)}')

# Проверяем, для каждого ли К и Ф есть соответствующий файл в архиве
name_to_path = {}
for path in all_files:
    if path.endswith('.md'):
        bn = os.path.basename(path)[:-3]
        name_to_path[bn] = path

missing_k = []
for k in k_links:
    if k not in name_to_path:
        missing_k.append(k)

missing_f = []
for f in f_links:
    if f not in name_to_path:
        missing_f.append(f)

print(f'Missing K files: {len(missing_k)}')
if missing_k:
    print('First 5 missing K:', missing_k[:5])

print(f'Missing F files: {len(missing_f)}')
if missing_f:
    print('First 5 missing F:', missing_f[:5])
