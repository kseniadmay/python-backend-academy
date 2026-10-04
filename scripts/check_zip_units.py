import zipfile
import re

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(remnote_python_zip) as z:
    paths = z.namelist()
    modules = set()
    units = set()
    for p in paths:
        parts = p.split('/')
        if len(parts) >= 2 and parts[1].startswith('0'):
            modules.add(parts[1])
        if len(parts) >= 3 and parts[2].startswith('Юнит '):
            units.add((parts[1], parts[2]))
            
    print('Modules in RemNote_Python.zip:')
    for m in sorted(modules):
        print(' ', m)
        
    print(f'\nTotal Units in RemNote_Python.zip: {len(units)}')
    for m, u in sorted(units, key=lambda x: [int(n) for n in re.findall(r'\d+', x[1])]):
        print(f'  {m} -> {u}')
