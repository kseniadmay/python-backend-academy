import zipfile

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(remnote_python_zip) as z:
    note_files = [n for n in z.namelist() if 'Конспекты' in n and n.endswith('.md')]
    h1_count = 0
    read_count = 0
    for n in note_files:
        lines = z.read(n).decode('utf-8').splitlines()
        if lines and lines[0].startswith('# '):
            h1_count += 1
        if lines and 'Перечитать конспект' in lines[0]:
            read_count += 1
    print(f'Note files with # on line 1: {h1_count} out of {len(note_files)}')
    print(f'Note files with Перечитать конспект on line 1: {read_count} out of {len(note_files)}')
