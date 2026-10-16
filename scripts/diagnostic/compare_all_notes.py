import zipfile
import re

orig_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
ready_zip = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Mastery_Import_Ready.zip'

z_orig = zipfile.ZipFile(orig_zip)
z_ready = zipfile.ZipFile(ready_zip)

orig_notes = [n for n in z_orig.namelist() if 'Конспекты' in n and n.endswith('.md')]
ready_notes = [n for n in z_ready.namelist() if 'Конспекты' in n and n.endswith('.md')]

print(f'Orig notes: {len(orig_notes)}, Ready notes: {len(ready_notes)}')

# Проверим, есть ли в Ready.zip артефакты типа "    - ." или "    - # ."
corrupted_count = 0
for n in ready_notes:
    text = z_ready.read(n).decode('utf-8')
    if '    - .' in text or '    - # .' in text or '        - ##' in text:
        corrupted_count += 1

print(f'Notes with broken indentation / dot-artifacts in Ready.zip: {corrupted_count} out of {len(ready_notes)}')

# Проверим пустые строки в оригинале
empty_bullet_count = 0
for n in orig_notes:
    text = z_orig.read(n).decode('utf-8')
    if '\n- \n' in text or '\n-\n' in text:
        empty_bullet_count += 1

print(f'Notes with empty spacer bullets (- ) in Orig: {empty_bullet_count} out of {len(orig_notes)}')
