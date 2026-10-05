import zipfile
import re
import os

import os, sys
zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
if not os.path.exists(zip_path):
    print('[SKIP] Legacy archive not found. Scratch test skipped.')
    sys.exit(0)
import zipfile
try:
    with zipfile.ZipFile(zip_path) as _test_z:
        if 'RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Срезы.md' not in _test_z.namelist():
            print('[SKIP] Legacy card not in archive. Scratch test skipped.')
            sys.exit(0)
except Exception:
    print('[SKIP] Cannot inspect legacy archive. Scratch test skipped.')
    sys.exit(0)

if not os.path.exists(zip_path):
    print('[SKIP] Historical archive ' + str(zip_path) + ' not found. Scratch test skipped.')
    import sys; sys.exit(0)

def is_pure_code(s):
    # Проверяет, является ли строка чистым кодом Python (без русского текста)
    s_clean = s.strip()
    if s_clean.startswith('- '):
        s_clean = s_clean[2:].strip()
    # Если есть кириллица - это не чистый код
    if re.search(r'[а-яА-ЯёЁ]', s_clean):
        return False
    # Если есть типичные элементы кода: =, [, (, import, def, etc.
    if re.search(r'(=|\[|\(|import|def|class|slice)', s_clean):
        return True
    return False

def clean_card_file(content):
    content = content.replace('—', '–')
    lines = content.splitlines()
    out = []
    in_code = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Пропускаем верхний H1
        if stripped.startswith('# '):
            i += 1
            continue
            
        # Пропускаем пустые буллеты и query:
        if stripped == '- query:' or stripped == 'query:' or stripped == '-' or stripped == '- ' or stripped == '':
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
            
        # Случай 1: Чистый код в начале (например a = ..., b = ...)
        if line.startswith('- ') and '>>' not in line and is_pure_code(line):
            code_lines = [line.strip()[2:].strip()]
            j = i + 1
            while j < len(lines) and is_pure_code(lines[j]) and not lines[j].strip().startswith('```') and lines[j].strip() != '':
                s_cl = lines[j].strip()
                if s_cl.startswith('- '):
                    s_cl = s_cl[2:].strip()
                code_lines.append(s_cl)
                j += 1
                
            formatted = []
            for cl in code_lines:
                if cl.startswith('`') and cl.endswith('`'):
                    formatted.append(cl)
                else:
                    formatted.append(f'`{cl}`')
            out.append('- ' + '; '.join(formatted))
            i = j
            continue
            
        # Случай 2: Одиночная строка с чистым кодом без дефиса (например first_three = slice(...))
        if not line.strip().startswith('-') and is_pure_code(line):
            s_cl = line.strip()
            out.append(f'- `{s_cl}`')
            i += 1
            continue

        # Защита от :: в срезах Python вне бэктиков
        if '::' in line and '`' not in line and '>>' not in line:
            line = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', line)
            
        if '>>' in line:
            parts = line.split('>>', 1)
            q = parts[0]
            a = parts[1]
            if '::' in q and '`' not in q:
                q = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', q)
            if '::' in a and '`' not in a:
                a = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', a)
            line = f'{q}>>{a}'
            
        out.append(line)
        i += 1
        
    return '\n'.join(out) + '\n'

with zipfile.ZipFile(zip_path) as z:
    # Проверяем Срезы.md
    raw_slices = z.read('RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Срезы.md').decode('utf-8')
    print('=== Срезы.md ===')
    for l in clean_card_file(raw_slices).splitlines()[:15]:
        print(l)
        
    # Проверяем Ловушка изменяемых аргументов.md
    raw_trap = z.read('RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Ловушка изменяемых аргументов.md').decode('utf-8')
    print('\n=== Ловушка изменяемых аргументов.md ===')
    for l in clean_card_file(raw_trap).splitlines()[:15]:
        print(l)
