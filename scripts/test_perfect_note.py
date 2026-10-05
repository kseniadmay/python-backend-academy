import os, sys
import zipfile
import re

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
if not os.path.exists(zip_path):
    print('[SKIP] Historical archive ' + str(zip_path) + ' not found. Scratch test skipped.')
    import sys; sys.exit(0)

def build_perfect_note(raw_text):
    text = raw_text.replace('—', '–')
    lines = text.splitlines()
    out = []
    in_code = False
    
    for line in lines:
        s = line.strip()
        
        # Пропускаем верхний дублирующий H1
        if s.startswith('# '):
            continue
            
        # Блоки кода
        if s.startswith('```'):
            in_code = not in_code
            out.append(line)
            continue
            
        if in_code:
            out.append(line)
            continue
            
        # Пропускаем пустые строки и пустые буллеты
        if s == '-' or s == '- ' or s == '':
            if out and out[-1] != '':
                out.append('')
            continue
            
        # Карточка повторения в начале
        if 'Перечитать конспект' in s:
            rep_match = re.search(r'Перечитать конспект (.*?)(?:→|>>)(.*)', s)
            if rep_match:
                q = rep_match.group(1).strip()
                a = rep_match.group(2).strip()
                out.append(f'- 📖 Перечитать конспект {q} >> {a}')
                out.append('')
                continue
                
        # Заголовки ##
        if s.startswith('##') or s.startswith('- ##'):
            h_text = s[4:].strip() if s.startswith('- ##') else s[2:].strip()
            if out and out[-1] != '':
                out.append('')
            out.append(f'## {h_text}')
            out.append('')
            continue
            
        # Заголовки ###
        if s.startswith('###') or s.startswith('- ###'):
            h_text = s[5:].strip() if s.startswith('- ###') else s[3:].strip()
            if out and out[-1] != '':
                out.append('')
            out.append(f'### {h_text}')
            out.append('')
            continue
            
        # Строки текста и списков
        # Если строка начинается с "- "
        if s.startswith('- '):
            content = s[2:].strip()
            # Проверяем, является ли это элементом списка (жирный текст, маркер, операция)
            # Если это обычный параграф текста, оформленный как буллет
            # В Markdown для RemNote: если это список с маркером (например - **Быстрые операции:**) - оставляем буллет!
            if content.startswith('**') or content.startswith('`') or re.match(r'^\d+\.', content) or content.startswith('•'):
                out.append(f'- {content}')
            else:
                # Обычный текст абзаца
                out.append(content)
        else:
            out.append(s)
            
    # Убираем лишние пустые строки подряд
    cleaned = []
    for l in out:
        if not cleaned and l == '':
            continue
        if cleaned and cleaned[-1] == '' and l == '':
            continue
        cleaned.append(l)
        
    return '\n'.join(cleaned) + '\n'

try:
    with zipfile.ZipFile(zip_path) as z:
        raw_k1 = z.read('RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📚 Конспекты/01. Структуры данных Python_ list, dict, set.md').decode('utf-8')
        perfect_k1 = build_perfect_note(raw_k1)
        print('=== PERFECT NOTE K-001 PREVIEW ===\n')
        print(perfect_k1[:1500])
except KeyError:
    print('[SKIP] Legacy note path not found in historical archive. Scratch test skipped.')
