import os
import re
import json
import zipfile
from collections import defaultdict

remnote_python_zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
map_json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'
mastery_map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'
out_zip_path = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Mastery_Import_Ready.zip'

with open(map_json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

notes_map = renaming_map['notes']
cards_map = renaming_map['cards']

# 1. Индексируем чистые файлы из RemNote_Python.zip
z_src = zipfile.ZipFile(remnote_python_zip_path)

def clean_dashes(text):
    return text.replace('—', '–')

def get_note_clean_content(nf, new_k_title):
    text = z_src.read(nf).decode('utf-8')
    text = clean_dashes(text)
    raw_lines = text.splitlines()
    
    out_lines = []
    # Заголовок документа
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
            # Заголовки ##
            if s.startswith('##') or s.startswith('- ##'):
                h_text = s[4:].strip() if s.startswith('- ##') else s[2:].strip()
                if out_lines and out_lines[-1] != '- ':
                    out_lines.append('- ')
                out_lines.append(f'- ## {h_text}')
                continue
                
            # Пустые строки
            if s == '-' or s == '' or s == '- ':
                if out_lines and out_lines[-1] != '- ':
                    out_lines.append('- ')
                continue
                
            # Обычные буллеты
            if s.startswith('- '):
                out_lines.append(s)
            elif s:
                out_lines.append(f'- {s}')
        else:
            out_lines.append(l)
            
    return '\n'.join(out_lines) + '\n'

def get_card_clean_content(cf, new_f_title):
    text = z_src.read(cf).decode('utf-8')
    text = clean_dashes(text)
    raw_lines = text.splitlines()
    
    out_lines = []
    out_lines.append(f'# {new_f_title}')
    out_lines.append('- ')
    
    for l in raw_lines:
        s = l.strip()
        # Пропускаем старый H1
        if s.startswith('# '):
            continue
        if not s or s == '-' or s == '- ':
            continue
            
        # Приводим к формату Вопрос?→Ответ или Вопрос >> Ответ
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

print('Функции подготовки контента готовы.')
