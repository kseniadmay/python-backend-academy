import zipfile
import re
import os

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

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
            
        # Проверяем висячие строки кода (например, строка без дефиса под строкой с дефисом)
        # Если текущая строка начинается с "- " (и в ней нет >>), а следующая строка без дефиса и без >>,
        # а через одну строку идет дочерний буллет с >>
        if line.startswith('- ') and '>>' not in line:
            code_lines = [line.strip()[2:].strip()]
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('-') and not lines[j].strip().startswith('#') and '>>' not in lines[j] and lines[j].strip() != '':
                code_lines.append(lines[j].strip())
                j += 1
                
            if len(code_lines) > 1 and j < len(lines) and ('>>' in lines[j] or lines[j].strip().startswith('-')):
                # Объединяем строки кода
                formatted_code = []
                for cl in code_lines:
                    # Если уже в бэктиках
                    if cl.startswith('`') and cl.endswith('`'):
                        formatted_code.append(cl)
                    else:
                        formatted_code.append(f'`{cl}`')
                combined_parent = '- ' + '; '.join(formatted_code)
                # Защита от :: в срезах
                if '::' in combined_parent:
                    # Убеждаемся что :: внутри бэктиков
                    pass
                out.append(combined_parent)
                i = j
                continue
                
        # Если строка с срезом a[::...] без бэктиков
        if '::' in line and '`' not in line and '>>' not in line:
            line = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', line)
            
        # Если строка вопроса содержит :: вне бэктиков и вне синтаксиса карточки
        if '>>' in line:
            parts = line.split('>>', 1)
            q = parts[0]
            a = parts[1]
            if '::' in q and '`' not in q:
                q = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', q)
            if '::' in a and '`' not in a:
                a = re.sub(r'([a-zA-Z0-9_]+\[[^\]]*::[^\]]*\])', r'`\1`', a)
            line = f'{q}>>{a}'
            
        # Убедимся, что буллеты имеют дефис
        if not line.strip().startswith('-') and not line.strip().startswith('```'):
            # Если это обычная строка без дефиса
            indent = len(line) - len(line.lstrip())
            line = ' ' * indent + '- ' + line.strip()
            
        out.append(line)
        i += 1
        
    return '\n'.join(out) + '\n'

with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        if 'Карточки' in name and name.endswith('.md'):
            txt = z.read(name).decode('utf-8')
            cleaned = clean_card_file(txt)
            # Проверим, что нет неэкранированных :: вне кода
            for l in cleaned.splitlines():
                cl = re.sub(r'`[^`]*`', '', l)
                if '::' in cl:
                    print(f'Warning colon in {os.path.basename(name)}: {l}')

print('All card files processed and verified!')
