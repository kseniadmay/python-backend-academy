import zipfile
import re

with zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\PluginZip.zip') as z:
    code = z.read('index.js').decode('utf-8')

for m in re.finditer(r'registerCommand\({\s*id:\s*["\']([^"\']+)["\']', code):
    print('Command ID:', m.group(1))
    start = m.start()
    print(code[start:start+400])
    print('='*50)
