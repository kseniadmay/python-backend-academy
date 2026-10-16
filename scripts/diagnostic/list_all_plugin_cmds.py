import zipfile
import re

with zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\PluginZip.zip') as z:
    code = z.read('index.js').decode('utf-8')

matches = list(re.finditer(r'registerCommand\({\s*id:\s*["\']([^"\']+)["\'],\s*name:\s*["\']([^"\']+)["\'],\s*action:\s*async\s*\(\)\s*=>\s*{([^}]+)}', code))
print('Total registered commands:', len(matches))
for m in matches:
    cid = m.group(1)
    name = m.group(2).encode('utf-8').decode('unicode_escape', errors='ignore')
    body = m.group(3)
    print(f'CMD: {cid} -> {name}')
    print(f'  ACTION: {body}')
    print('---')
