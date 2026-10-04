import zipfile

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
with zipfile.ZipFile(remnote_python_zip) as z:
    names = z.namelist()
    notes = [n for n in names if 'Конспекты' in n and n.endswith('.md')]
    cards = [n for n in names if 'Карточки' in n and n.endswith('.md')]
    others = [n for n in names if not ('Конспекты' in n or 'Карточки' in n)]
    print('Total files:', len(names))
    print('Notes count:', len(notes))
    print('Cards count:', len(cards))
    print('Other files:', len(others))
    for o in others:
        print(' ', o)
