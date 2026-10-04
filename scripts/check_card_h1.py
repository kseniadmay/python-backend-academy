import zipfile

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(remnote_python_zip) as z:
    card_files = [n for n in z.namelist() if 'Карточки' in n and n.endswith('.md')]
    h1_count = 0
    for n in card_files:
        lines = z.read(n).decode('utf-8').splitlines()
        if lines and lines[0].startswith('# '):
            h1_count += 1
    print(f'Card files with # on line 1: {h1_count} out of {len(card_files)}')
