import zipfile

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(remnote_python_zip) as z:
    for n in z.namelist():
        if 'Карточки' in n and 'list comprehension' in n:
            text = z.read(n).decode('utf-8')
            lines = text.splitlines()
            new_lines = []
            new_lines.append('# Ф-001. list comprehension, dict comprehension и set')
            new_lines.append('- ')
            new_lines.extend(lines)
            print('SAMPLE TRANSFORMED CARD DECK:')
            print('\n'.join(new_lines[:12]))
            break
