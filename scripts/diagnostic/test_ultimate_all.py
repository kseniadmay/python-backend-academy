import re, zipfile, textwrap

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
    res = re.sub(r'\[\s*:\s*:\s*\]', '[: :]', res)
    res = res.replace("'{python,sql}'::TEXT[]", "CAST('{python,sql}' AS TEXT[])")
    res = res.replace("'::TEXT[]", "' AS TEXT[])")
    return res

def build_ultimate_flat_note(raw_text):
    text = clean_dashes(raw_text)
    lines = text.splitlines()
    
    out = []
    in_code = False
    code_lines = []
    
    for line in lines:
        s = line.strip()
        
        # 1. Пропускаем дублирующий H1
        if re.match(r'^(?:-\s*)?#\s+', s):
            continue
            
        # 2. Пропускаем статистику повторений
        if re.search(r'Было \d+ повторен', s) or re.search(r'повторени[яйе] \+\d+д', s):
            continue
            
        # 3. Пропускаем точки перед кодом
        if s in ('- .', '.', '- ..'):
            continue
            
        # 4. Пропускаем хлебные крошки тегов
        if re.match(r'^(?:-\s*)?\[[\'\"].*?[\'\"]', s):
            continue
            
        # 5. Блоки кода
        if s.startswith('```'):
            in_code = not in_code
            if not in_code:
                dedented = textwrap.dedent('\n'.join(code_lines)).splitlines()
                if out and out[-1] != '':
                    out.append('')
                out.append('```python')
                for cl in dedented:
                    out.append(fix_slice_colons(cl))
                out.append('```')
                out.append('')
                code_lines = []
            continue
            
        if in_code:
            code_lines.append(line)
            continue
            
        # 6. Пропускаем пустые строки и пустые дефисы
        if s in ('-', '- ', ''):
            continue
            
        # 7. Карточка повторения в начале (строго флешкарта без буллета)
        if 'Перечитать конспект' in s:
            rep_match = re.search(r'Перечитать конспект[:\s]*(.*?)(?:→|>>)(.*)', s)
            if rep_match:
                q = rep_match.group(1).strip()
                a = rep_match.group(2).strip()
                out.append(f'📖 Перечитать конспект: {q} >> {a}')
                out.append('')
                continue
                
        # 8. Заголовки разделов (H2 / H3) -> оформляем жирным БЕЗ '#'
        h_match = re.match(r'^(?:-\s*)?#{2,3}\s+(.*)', s)
        if h_match:
            h_title = fix_slice_colons(h_match.group(1).strip())
            if out and out[-1] != '':
                out.append('')
            out.append(f'**{h_title}**')
            out.append('')
            continue
            
        # 9. Очищаем текст от начального '- '
        content = re.sub(r'^\s*-\s*', '', s).strip()
        content = fix_slice_colons(content)
        
        # Специальный кейс для параметров среза
        if 'start – индекс' in content and 'stop – индекс' in content:
            if out and out[-1] != '':
                out.append('')
            out.append('- `start` – индекс, с которого начинается срез (включительно).')
            out.append('- `stop` – индекс, на котором срез заканчивается (не включительно).')
            out.append('- `step` – шаг между элементами.')
            out.append('')
            out.append('Любой из трёх параметров можно опустить – тогда подставляется значение по умолчанию.')
            out.append('')
            continue
            
        # 10. Определение списков
        is_bullet = False
        if content.startswith(('•', '- ')):
            is_bullet = True
            content = re.sub(r'^(?:•|-)\s*', '', content)
        elif content.startswith(('**Быстрые операции', '**Медленные операции', '**Преимущества', '**Недостатки', '**Плюсы', '**Минусы')):
            is_bullet = True
        elif re.match(r'^\d+\.\s+', content):
            is_bullet = True
            
        if is_bullet:
            out.append(f'- {content}')
        else:
            if out and out[-1] != '' and not out[-1].startswith('- '):
                out.append('')
            out.append(content)
            out.append('')

    if in_code and code_lines:
        dedented = textwrap.dedent('\n'.join(code_lines)).splitlines()
        if out and out[-1] != '':
            out.append('')
        out.append('```python')
        for cl in dedented:
            out.append(fix_slice_colons(cl))
        out.append('```')
        out.append('')

    cleaned = []
    for l in out:
        if not cleaned and l == '':
            continue
        if cleaned and cleaned[-1] == '' and l == '':
            continue
        cleaned.append(l)

    return '\n'.join(cleaned) + '\n'

z = zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip')
notes = [n for n in z.namelist() if 'Конспекты' in n and n.endswith('.md')]
print(f'Total notes found: {len(notes)}')

for code in ['К-001', 'К-002', 'К-009', 'К-047', 'К-079']:
    sample = [n for n in notes if code in n][0]
    res = build_ultimate_flat_note(z.read(sample).decode('utf-8'))
    print(f'=== PREVIEW {code} (First 25 lines) ===')
    for i, l in enumerate(res.splitlines()[:25]):
        print(f'{i+1:2d}: {l}')
    print('-'*50)
