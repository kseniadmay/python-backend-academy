import zipfile
import re

with zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\PluginZip.zip') as z:
    code = z.read('index.js').decode('utf-8')

matches = [m.start() for m in re.finditer(r'привязать', code, re.IGNORECASE)]
matches += [m.start() for m in re.finditer(r'ссылки программы', code, re.IGNORECASE)]

print('Matches:', len(matches))
for p in matches:
    start = max(0, p - 200)
    end = min(len(code), p + 800)
    print('--- MATCH ---')
    print(code[start:end])
