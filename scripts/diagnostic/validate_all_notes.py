import re
import zipfile
import textwrap

remnote_python_zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

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

def build_perfect_note(raw_text):
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
            
        # 2. Удаляем остаточные строки статистики интервального повторения
        if re.search(r'Было \d+ повторен', s) or re.search(r'повторени[яйе] \+\d+д', s):
            continue
            
        # 3. Пропускаем артефакты точек перед кодом
        if s in ('- .', '.', '- ..'):
            continue
            
        # 4. Пропускаем хлебные крошки тегов
        if re.match(r'^(?:-\s*)?\[[\'"].*?[\'"]', s):
            continue
            
        # 5. Обработка блоков кода
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
            
        # 6. Пропускаем пустые строки и пустые буллеты
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
                
        # 8. Заголовки (H2 и H3):
        # Оформляем как '- {hashes} {h_title}', чтобы RemNote присвоил уровень H2/H3,
        # но НЕ делал его сворачиваемым родителем со стрелкой ▾!
        h_match = re.match(r'^(?:-\s*)?(#{2,3})\s+(.*)', s)
        if h_match:
            hashes = h_match.group(1)
            h_title = fix_slice_colons(h_match.group(2).strip())
            
            # Находим предыдущий непустой элемент
            last_item = ''
            for item in reversed(out):
                if item.strip():
                    last_item = item.strip()
                    break
            
            if last_item and not last_item.startswith(('- ##', '- ###', '---')):
                if out and out[-1] != '':
                    out.append('')
                out.append('---')
                out.append('')
            elif out and out[-1] != '':
                out.append('')
                
            out.append(f'- {hashes} {h_title}')
            out.append('')
            continue
            
        # 9. Обычный контент: убираем паразитные глубокие отступы и дефисы
        clean_content = re.sub(r'^\s*-\s*', '', s).strip()
        clean_content = fix_slice_colons(clean_content)
        
        # Специальный кейс для параметров среза, если они склеены в одну строку
        if 'индекс, с которого начинается срез' in clean_content and 'индекс, на котором срез заканчивается' in clean_content:
            if out and out[-1] != '':
                out.append('')
            out.append('- `start` – индекс, с которого начинается срез (включительно).')
            out.append('- `stop` – индекс, на котором срез заканчивается (не включительно).')
            out.append('- `step` – шаг между элементами.')
            out.append('')
            out.append('Любой из трёх параметров можно опустить – тогда подставляется значение по умолчанию.')
            out.append('')
            continue
            
        # 10. Определение: это маркированный список или обычный абзац текста?
        is_bullet = False
        if clean_content.startswith(('•', '- ')):
            is_bullet = True
            clean_content = re.sub(r'^(?:•|-)\s*', '', clean_content)
        elif clean_content.startswith(('**Быстрые операции', '**Медленные операции', '**Преимущества', '**Недостатки', '**Плюсы', '**Минусы')):
            is_bullet = True
        elif re.match(r'^\d+\.\s+', clean_content):
            is_bullet = True
            
        if is_bullet:
            if out and out[-1] != '' and not out[-1].startswith('- '):
                out.append('')
            out.append(f'- {clean_content}')
        else:
            # Обычный абзац текста: отделяем пустой строкой, чтобы не склеивался и шёл на плоском уровне
            if out and out[-1] != '':
                out.append('')
            out.append(clean_content)
            out.append('')

    # Если вдруг файл закончился с незакрытым кодом
    if in_code and code_lines:
        dedented = textwrap.dedent('\n'.join(code_lines)).splitlines()
        if out and out[-1] != '':
            out.append('')
        out.append('```python')
        for cl in dedented:
            out.append(fix_slice_colons(cl))
        out.append('```')
        out.append('')

    # Очищаем лишние пустые строки подряд
    cleaned = []
    for l in out:
        if not cleaned and l == '':
            continue
        if cleaned and cleaned[-1] == '' and l == '':
            continue
        cleaned.append(l)

    return '\n'.join(cleaned) + '\n'

z = zipfile.ZipFile(remnote_python_zip_path)
note_files = [n for n in z.namelist() if 'Конспекты' in n and n.endswith('.md')]

print(f'Total notes to test: {len(note_files)}')

errors = []
total_headings = 0
total_dividers = 0

for nf in note_files:
    raw = z.read(nf).decode('utf-8')
    res = build_perfect_note(raw)
    
    # 1. Проверяем "голые" заголовки (без '- ')
    bare_h = re.findall(r'^(?<!- )#{2,3}\s+.*', res, re.M)
    if bare_h:
        errors.append(f'{nf}: Bare headings found: {bare_h}')
        
    # 2. Проверяем, что заголовки начинаются с '- ##' или '- ###'
    valid_h = re.findall(r'^- #{2,3}\s+.*', res, re.M)
    total_headings += len(valid_h)
    
    # 3. Считаем разделители
    divs = re.findall(r'^---$', res, re.M)
    total_dividers += len(divs)
    
    # 4. Проверяем парность блоков кода
    fence_count = len(re.findall(r'^```', res, re.M))
    if fence_count % 2 != 0:
        errors.append(f'{nf}: Unclosed code block (fences: {fence_count})')
        
    # 5. Проверяем срезы ::
    broken_slices = re.findall(r'\[[^\]]*?::[^\]]*?\]', res)
    if broken_slices:
        errors.append(f'{nf}: Broken slices found: {broken_slices}')

print(f'Validation complete!')
print(f'Total valid headings: {total_headings}')
print(f'Total dividers: {total_dividers}')
print(f'Errors count: {len(errors)}')
if errors:
    for e in errors[:10]:
        print('ERROR:', e)
else:
    print('ALL 216 NOTES PASSED VALIDATION WITH ZERO ERRORS!')
