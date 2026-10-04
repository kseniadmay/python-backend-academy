import zipfile
import re

with zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\PluginZip.zip') as z:
    code = z.read('index.js').decode('utf-8')
    
# Найдем функцию Ue или создание документов
pos = code.find('function Ue')
if pos != -1:
    print('Found function Ue:')
    print(code[pos:pos+500])
else:
    # Поищем regex заголовков
    for m in re.finditer(r'#\{1,6\}', code):
        start = max(0, m.start() - 100)
        end = min(len(code), m.end() + 200)
        print(code[start:end])
        print('---')
