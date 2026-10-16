import zipfile
import re

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        if 'Карточки' in name and name.endswith('.md'):
            txt = z.read(name).decode('utf-8')
            in_code = False
            for line_no, line in enumerate(txt.splitlines(), 1):
                if line.strip().startswith('```'):
                    in_code = not in_code
                    continue
                if in_code:
                    continue
                # Убираем инлайн-код
                clean = re.sub(r'`[^`]*`', '', line)
                if '::' in clean:
                    print(f'{name}:{line_no}: {line}')
