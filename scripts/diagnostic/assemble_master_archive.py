import os
import re
import json
import zipfile
import shutil

remnote_python_zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
map_json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'
mastery_map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'
out_zip_path = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Mastery_Import_Ready.zip'

with open(map_json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

notes_map = renaming_map['notes']
cards_map = renaming_map['cards']

z_src = zipfile.ZipFile(remnote_python_zip_path)

def clean_dashes(text):
    return text.replace('—', '–')

# 1. Функция матчинга конспектов
def match_note(nf, first_line):
    bn = os.path.basename(nf)[:-3]
    clean_bn = re.sub(r'^\d+\.\s*', '', bn).strip()
    
    for k, v in notes_map.items():
        if k == clean_bn or k.lower() == clean_bn.lower() or k.replace('_', ' ') == clean_bn.replace('_', ' '):
            return v
            
    m = re.search(r'Перечитать конспект (.*?)→', first_line)
    if m:
        t = m.group(1).strip()
        t_clean = t.replace(':', '_').replace('–', '-').replace('—', '-')
        for k, v in notes_map.items():
            if k == t or k == t_clean or k.lower() == t.lower() or k.lower() == t_clean.lower():
                return v
                
    for k, v in notes_map.items():
        if k.startswith(clean_bn[:25]) or clean_bn.startswith(k[:25]):
            return v
            
    return None

# 2. Функция матчинга карточек
def match_card(cf):
    bn = os.path.basename(cf)[:-3]
    clean_bn = re.sub(r'^Ф-\d+\.\s*', '', bn).strip()
    for k, v in cards_map.items():
        if k == clean_bn or k.lower() == clean_bn.lower():
            return v
    return None

# 3. Подготовка контента конспекта
def build_clean_note(nf, new_k_title):
    text = z_src.read(nf).decode('utf-8')
    text = clean_dashes(text)
    raw_lines = text.splitlines()
    
    out_lines = []
    out_lines.append(f'# {new_k_title}')
    out_lines.append('- ')
    
    in_code_block = False
    for l in raw_lines:
        s = l.strip()
        if s.startswith('```'):
            in_code_block = not in_code_block
            out_lines.append(l)
            continue
            
        if not in_code_block:
            if s.startswith('##') or s.startswith('- ##'):
                h_text = s[4:].strip() if s.startswith('- ##') else s[2:].strip()
                if out_lines and out_lines[-1] != '- ':
                    out_lines.append('- ')
                out_lines.append(f'- ## {h_text}')
                continue
                
            if s == '-' or s == '' or s == '- ':
                if out_lines and out_lines[-1] != '- ':
                    out_lines.append('- ')
                continue
                
            if s.startswith('- '):
                out_lines.append(s)
            elif s:
                out_lines.append(f'- {s}')
        else:
            out_lines.append(l)
            
    return '\n'.join(out_lines) + '\n'

# 4. Подготовка контента карточки
def build_clean_card(cf, new_f_title):
    text = z_src.read(cf).decode('utf-8')
    text = clean_dashes(text)
    raw_lines = text.splitlines()
    
    out_lines = []
    out_lines.append(f'# {new_f_title}')
    out_lines.append('- ')
    
    for l in raw_lines:
        s = l.strip()
        if s.startswith('# '):
            continue
        if not s or s == '-' or s == '- ':
            continue
            
        if '>>' in s:
            parts = s.split('>>', 1)
            q = parts[0].strip()
            a = parts[1].strip()
            if q.startswith('- '): q = q[2:].strip()
            out_lines.append(f'- {q}→{a}')
        elif '→' in s:
            if not s.startswith('- '):
                out_lines.append(f'- {s}')
            else:
                out_lines.append(s)
        else:
            if s.startswith('- '):
                out_lines.append(s)
            else:
                out_lines.append(f'- {s}')
                
    return '\n'.join(out_lines) + '\n'

# 5. Подготовка Карты Мастерства со свободным пространством (воздухом)
with open(mastery_map_path, 'r', encoding='utf-8') as f:
    raw_map = f.read()

raw_map = clean_dashes(raw_map)
map_lines = raw_map.splitlines()

formatted_map_lines = []
# Верхний H1
formatted_map_lines.append('# 🎓 Карта Мастерства: Junior Python Backend Developer')
formatted_map_lines.append('- ')

for line in map_lines:
    s = line.strip()
    if s.startswith('# 🎓'):
        continue
        
    # Перед заголовками ## (Модули)
    if s.startswith('## ') or s.startswith('- ## '):
        if formatted_map_lines and formatted_map_lines[-1] != '- ':
            formatted_map_lines.append('- ')
        h = s[4:].strip() if s.startswith('- ## ') else s[2:].strip()
        formatted_map_lines.append(f'- ## {h}')
        formatted_map_lines.append('- ')
        continue
        
    # Перед заголовками ### (Юниты)
    if s.startswith('### ') or s.startswith('- ### '):
        if formatted_map_lines and formatted_map_lines[-1] != '- ':
            formatted_map_lines.append('- ')
        h = s[5:].strip() if s.startswith('- ### ') else s[3:].strip()
        formatted_map_lines.append(f'- ### {h}')
        formatted_map_lines.append('- ')
        continue
        
    # Перед скиллами
    if '⚡ **Skill ' in line:
        if formatted_map_lines and formatted_map_lines[-1] != '    - ' and formatted_map_lines[-1] != '- ':
            formatted_map_lines.append('    - ')
        formatted_map_lines.append(line)
        continue
        
    # Перед Unit Test
    if '🏆 **UNIT TEST' in line:
        if formatted_map_lines and formatted_map_lines[-1] != '- ':
            formatted_map_lines.append('- ')
        formatted_map_lines.append(line)
        formatted_map_lines.append('- ')
        continue
        
    # Пустые строки
    if s == '-' or s == '':
        if formatted_map_lines and formatted_map_lines[-1] != '- ' and formatted_map_lines[-1] != '    - ':
            formatted_map_lines.append('- ')
        continue
        
    formatted_map_lines.append(line)

final_map_text = '\n'.join(formatted_map_lines) + '\n'

# Сохраняем обновленную Карту Мастерства на диск
with open(mastery_map_path, 'w', encoding='utf-8') as f:
    f.write(final_map_text)
print('Карта Мастерства успешно оформлена с вертикальными отступами.')

# 6. Собираем ZIP-архив
if os.path.exists(out_zip_path):
    os.remove(out_zip_path)

module_renames = {
    '01 · 🐍 Python': '01 · 🐍 Python',
    '02 · 🌐 Web & Backend': '02 · 🌐 Web & Backend',
    '03 · 🧩 Алгоритмы': '03 · ⚡ Алгоритмы',
    '04 · 🗄️ Базы данных': '04 · 🗄️ Базы данных',
    '05 · 🏛️ Архитектура': '05 · 🏛️ Архитектура',
    '06 · ⚙️ Инфраструктура': '06 · 🚀 Инфраструктура',
}

added_files = 0
with zipfile.ZipFile(out_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
    # Добавляем Карту Мастерства
    z_out.writestr('Собеседования/00 · 🗺️ Карта Мастерства.md', final_map_text.encode('utf-8'))
    added_files += 1
    
    # Добавляем все конспекты и карточки
    for item in z_src.namelist():
        parts = item.split('/')
        if len(parts) < 4:
            continue
            
        orig_mod = parts[1]
        target_mod = module_renames.get(orig_mod, orig_mod)
        unit = parts[2]
        folder_type = parts[3] # 📚 Конспекты или 📇 Карточки
        filename = parts[-1]
        
        if 'Конспекты' in folder_type and filename.endswith('.md'):
            first_line = z_src.read(item).decode('utf-8').splitlines()[0]
            new_title = match_note(item, first_line)
            if not new_title:
                print('ERROR: Unmatched note:', item)
                continue
            content = build_clean_note(item, new_title)
            dest_path = f'Собеседования/{target_mod}/{unit}/📚 Конспекты/{new_title}.md'
            z_out.writestr(dest_path, content.encode('utf-8'))
            added_files += 1
            
        elif 'Карточки' in folder_type and filename.endswith('.md'):
            new_title = match_card(item)
            if not new_title:
                print('ERROR: Unmatched card:', item)
                continue
            content = build_clean_card(item, new_title)
            dest_path = f'Собеседования/{target_mod}/{unit}/📇 Карточки/{new_title}.md'
            z_out.writestr(dest_path, content.encode('utf-8'))
            added_files += 1

print(f'Архив собран успешно! Всего файлов в архиве: {added_files}')
