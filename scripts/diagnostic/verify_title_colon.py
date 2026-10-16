import zipfile
import re

# Проверим, как назывались конспекты в оригинале RemNote:
orig_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
with zipfile.ZipFile(orig_zip) as z:
    for n in z.namelist():
        if '01. Структуры данных' in n:
            text = z.read(n).decode('utf-8')
            first_line = text.splitlines()[0]
            print('RemNote_Python line 1:', repr(first_line))
            # Извлекаем название из "Перечитать конспект <Название>→"
            m = re.search(r'Перечитать конспект (.*?)→', first_line)
            if m:
                print('Название конспекта внутри текста:', repr(m.group(1).strip()))
