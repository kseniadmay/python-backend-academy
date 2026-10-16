import zipfile
import os

zip_fixed = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNoteExport_Fury-Inf_md_2026-09-24_06-38_FIXED.zip'
zip_python = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(zip_fixed) as zf, zipfile.ZipFile(zip_python) as zp:
    fixed_cards = {os.path.basename(n): n for n in zf.namelist() if 'Карточки' in n and n.endswith('.md')}
    python_cards = {os.path.basename(n): n for n in zp.namelist() if 'Карточки' in n and n.endswith('.md')}
    
    print(f'Fixed cards count: {len(fixed_cards)}')
    print(f'Python cards count: {len(python_cards)}')
    
    missing = set(python_cards.keys()) - set(fixed_cards.keys())
    print(f'Missing in fixed: {len(missing)}')
    if missing:
        print('Sample missing:', list(missing)[:5])
