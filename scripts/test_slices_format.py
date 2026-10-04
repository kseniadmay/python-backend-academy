import zipfile
import re

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(zip_path) as z:
    raw = z.read('RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Срезы.md').decode('utf-8')

# Очищаем длинные тире
raw = raw.replace('—', '–')

lines = raw.splitlines()
out = []
in_code = False

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Пропускаем # Заголовок
    if stripped.startswith('# '):
        i += 1
        continue
    # Пропускаем мусор
    if stripped == '- query:' or stripped == 'query:' or stripped == '-' or stripped == '- ':
        i += 1
        continue
        
    if stripped.startswith('```'):
        in_code = not in_code
        out.append(line)
        i += 1
        continue
        
    if in_code:
        out.append(line)
        i += 1
        continue
        
    # Проверяем строки кода срезов, которые идут без дефиса (продолжение родителя)
    # Например:
    # - a = [0, 1, 2, 3, 4, 5]
    #   b = a[1:4]
    #   - Какие индексы попадут...
    if line.startswith('- a = ') and i + 1 < len(lines) and lines[i+1].strip().startswith('b = '):
        part1 = line.strip()[2:].strip()
        part2 = lines[i+1].strip()
        # Оборачиваем в инлайн-код
        combined = f'- `{part1}`; `{part2}`'
        out.append(combined)
        i += 2
        continue
        
    if line.startswith('- first_three = '):
        part = line.strip()[2:].strip()
        out.append(f'- `{part}`')
        i += 1
        continue

    # Если в строке есть срез a[::...] вне бэктиков
    if '::' in line and '`' not in line and '>>' not in line:
        line = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', line)
        
    out.append(line)
    i += 1

result = '\n'.join(out)
print('RESULT FOR Срезы.md:\n')
print(result[:1500])
