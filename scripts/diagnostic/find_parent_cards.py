import zipfile
import re
import os

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        if 'Карточки' in name and name.endswith('.md'):
            txt = z.read(name).decode('utf-8')
            lines = txt.splitlines()
            for i, line in enumerate(lines):
                # Ищем строки буллетов, у которых нет >>, но следующие строки имеют >>
                if line.strip().startswith('- ') and '>>' not in line:
                    if not line.strip().startswith('#') and 'query:' not in line:
                        # Посмотрим на следующие строки
                        next_lines = [lines[j].strip() for j in range(i+1, min(i+4, len(lines)))]
                        has_child_card = any('>>' in nl for nl in next_lines)
                        if has_child_card:
                            print(f'{os.path.basename(name)}: parent: {line.strip()[:60]} | next: {next_lines[0][:60]}')
