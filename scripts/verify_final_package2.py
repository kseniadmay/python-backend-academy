import zipfile
import re

import os
_here = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.normpath(os.path.join(_here, '..', 'RemNote_Python_Mastery_FIXED.zip'))

with zipfile.ZipFile(zip_path) as z:
    map_text = z.read('00 · 🗺️ Карта Мастерства.md').decode('utf-8')
    all_files = set(z.namelist())

    links = re.findall(r'\[\[(.*?)\]\]', map_text)
    print(f'Total links in Map: {len(links)}')

    valid = sum(1 for l in links if (l + '.md') in all_files)
    print(f'Valid links: {valid}/{len(links)}')

    # Смотрим Ф-006 Срезы
    slice_file = [n for n in all_files if 'Ф-006' in n][0]
    print(f'\nSample from {slice_file} (first 12 lines):')
    for line in z.read(slice_file).decode('utf-8').splitlines()[:12]:
        print(' ', line)
        
    # Смотрим Ловушку аргументов
    trap_file = [n for n in all_files if 'Ловушка' in n][0]
    print(f'\nSample from {trap_file} (lines with code):')
    for line in z.read(trap_file).decode('utf-8').splitlines()[2:9]:
        print(' ', line)
