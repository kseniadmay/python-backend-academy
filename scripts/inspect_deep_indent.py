import zipfile
import re

z = zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip')
notes = [n for n in z.namelist() if '📚 Конспекты' in n and n.endswith('.md')]

count = 0
for nf in notes:
    content = z.read(nf).decode('utf-8')
    lines = content.splitlines()
    deep_lines = [l for l in lines if re.match(r'^\s{8,}', l)]
    if deep_lines and count < 3:
        count += 1
        print(f"=== File {count}: {nf} ===")
        for i, l in enumerate(lines[:35]):
            print(f"{i+1:2d}: {repr(l)}")
        print("\n" + "="*50 + "\n")
