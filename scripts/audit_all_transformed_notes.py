import zipfile
import re
import textwrap

def clean_dashes(text):
    return text.replace('—', '–')

def fix_slice_colons(text):
    def rep(match):
        prefix = match.group(1).strip()
        suffix = match.group(2).strip()
        if prefix and suffix:
            return f'[{prefix} : : {suffix}]'
        elif prefix:
            return f'[{prefix} : :]'
        elif suffix:
            return f'[: : {suffix}]'
        else:
            return '[: :]'
    
    res = re.sub(r'\[([^\]]*?)::([^\]]*?)\]', rep, text)
    res = re.sub(r'`\s*::\s*`', '`[: :]`', res)
    res = res.replace("'{python,sql}'::TEXT[]", "CAST('{python,sql}' AS TEXT[])")
    res = res.replace("'::TEXT[]", "' AS TEXT[])")
    return res

def transform_note_to_flat_level(raw_text):
    text = clean_dashes(raw_text)
    lines = text.splitlines()
    
    out = []
    in_code = False
    code_lines = []
    
    for line in lines:
        s = line.strip()
        
        # 1. Пропускаем верхний дублирующий H1
        if re.match(r'^(?:-\s*)?#\s+', s):
            continue
            
        # 2. Пропускаем остаточную статистику интервального повторения
        if re.search(r'Было \d+ повторен', s) or re.search(r'повторени[яйе] \+\d+д', s):
            continue
            
        # 3. Пропускаем артефакты точки перед кодом
        if s in ('- .', '.', '- ..'):
            continue
            
        # 4. Пропускаем хлебные крошки тегов
        if re.match(r'^(?:-\s*)?\[[\'"].*?[\'"]', s):
            continue
            
        # 5. Обработка блоков кода
        if s.startswith('```'):
            in_code = not in_code
            if not in_code:
                # Завершаем блок кода: дедентируем собранные строки
                dedented = textwrap.dedent('\n'.join(code_lines)).splitlines()
                out.append('```python')
                for cl in dedented:
                    out.append(fix_slice_colons(cl))
                out.append('```')
                code_lines = []
            continue
            
        if in_code:
            code_lines.append(line)
            continue
            
        # 6. Пропускаем пустые строки и пустые буллеты
        if s in ('-', '- ', ''):
            continue
            
        # 7. Карточка повторения в начале
        if 'Перечитать конспект' in s:
            rep_match = re.search(r'Перечитать конспект[:\s]*(.*?)(?:→|>>)(.*)', s)
            if rep_match:
                q = rep_match.group(1).strip()
                a = rep_match.group(2).strip()
                out.append(f'- 📖 Перечитать конспект: {q} >> {a}')
                continue
                
        # 8. Заголовки (H2 и H3) — делаем их буллетами верхнего уровня (- ## и - ###)
        h_match = re.match(r'^(?:-\s*)?(#{2,3})\s+(.*)', s)
        if h_match:
            hashes = h_match.group(1)
            h_title = fix_slice_colons(h_match.group(2).strip())
            out.append(f'- {hashes} {h_title}')
            continue
            
        # 9. Обычный контент: убираем глубокую вложенность
        clean_content = re.sub(r'^\s*-\s*', '', s).strip()
        clean_content = fix_slice_colons(clean_content)
        
        # Специальный кейс для параметров среза, если они склеены
        if 'start – индекс' in clean_content and 'stop – индекс' in clean_content:
            out.append('- `start` – индекс, с которого начинается срез (включительно).')
            out.append('- `stop` – индекс, на котором срез заканчивается (не включительно).')
            out.append('- `step` – шаг между элементами.')
            out.append('- Любой из трёх параметров можно опустить – тогда подставляется значение по умолчанию.')
            continue
            
        out.append(f'- {clean_content}')

    # Если вдруг файл закончился с незакрытым кодом:
    if in_code and code_lines:
        dedented = textwrap.dedent('\n'.join(code_lines)).splitlines()
        out.append('```python')
        for cl in dedented:
            out.append(fix_slice_colons(cl))
        out.append('```')

    return '\n'.join(out) + '\n'

z = zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip')
notes = [n for n in z.namelist() if '📚 Конспекты' in n and n.endswith('.md')]

print(f"Auditing all {len(notes)} notes...")
issues = []
for nf in notes:
    raw = z.read(nf).decode('utf-8')
    res = transform_note_to_flat_level(raw)
    
    # Проверка 1: непарные кавычки кода
    ticks = res.count('```')
    if ticks % 2 != 0:
        issues.append(f"Odd backticks ({ticks}) in {nf}")
        
    # Проверка 2: точки перед кодом
    if '\n- .\n' in res or '\n.\n' in res:
        issues.append(f"Leftover dot in {nf}")
        
    # Проверка 3: стрелка → в карточке повторения
    if 'Перечитать конспект' in res and '→' in res.split('Перечитать конспект')[1].splitlines()[0]:
        issues.append(f"Leftover arrow in flashcard in {nf}")
        
    # Проверка 4: остались ли глубокие отступы перед дефисами
    for l in res.splitlines():
        if re.match(r'^\s+-\s+', l):
            issues.append(f"Indented bullet in {nf}: {l[:40]}")
            break

print(f"Total issues found: {len(issues)}")
for iss in issues[:10]:
    print(" ", iss)
