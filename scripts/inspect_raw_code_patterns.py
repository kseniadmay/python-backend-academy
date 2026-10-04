import zipfile
import re

z = zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip')
notes = [n for n in z.namelist() if '📚 Конспекты' in n and n.endswith('.md')]

code_patterns = []

for nf in notes:
    content = z.read(nf).decode('utf-8')
    lines = content.splitlines()
    for i, l in enumerate(lines):
        if l.strip().startswith('```'):
            # Посмотрим контекст вокруг: 2 строки до и 2 строки после
            prev = lines[max(0, i-2):i]
            post = lines[i:min(len(lines), i+4)]
            code_patterns.append((nf, prev, post))
            if len(code_patterns) >= 10:
                break
    if len(code_patterns) >= 10:
        break

print(f"Sample code patterns around ```:")
for nf, prev, post in code_patterns[:6]:
    print(f"--- In {nf.split('/')[-1]} ---")
    print("PREV:", [p.strip() for p in prev])
    print("CODE:", [p.strip() for p in post])
