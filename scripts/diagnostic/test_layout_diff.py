import zipfile, re, textwrap

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
        if re.match(r'^(?:-\s*)?#\s+', s):
            continue
        if re.search(r'Было \d+ повторен', s) or re.search(r'повторени[яйе] \+\d+д', s):
            continue
        if s in ('- .', '.', '- ..'):
            continue
        if re.match(r'^(?:-\s*)?\[[\'\"].*?[\'\"]', s):
            continue
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
        if s in ('-', '- ', ''):
            continue
        if 'Перечитать конспект' in s:
            rep_match = re.search(r'Перечитать конспект[:\s]*(.*?)(?:→|>>)(.*)', s)
            if rep_match:
                q = rep_match.group(1).strip()
                a = rep_match.group(2).strip()
                out.append(f'📖 Перечитать конспект: {q} >> {a}')
                out.append('')
                continue
        h_match = re.match(r'^(?:-\s*)?(#{2,3})\s+(.*)', s)
        if h_match:
            hashes = h_match.group(1)
            h_title = fix_slice_colons(h_match.group(2).strip())
            last_item = ''
            for item in reversed(out):
                if item.strip():
                    last_item = item.strip()
                    break
            if last_item and not last_item.startswith(('##', '###', '---')):
                if out and out[-1] != '':
                    out.append('')
                out.append('---')
                out.append('')
            elif out and out[-1] != '':
                out.append('')
            out.append(f'{hashes} {h_title}')
            out.append('')
            continue
        clean_content = re.sub(r'^\s*-\s*', '', s).strip()
        clean_content = fix_slice_colons(clean_content)
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
            if out and out[-1] != '':
                out.append('')
            out.append(clean_content)
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
for cid in ['004', '216']:
    sf = [f for f in z.namelist() if cid in f and 'Конспекты' in f][0]
    res = build_perfect_note(z.read(sf).decode('utf-8'))
    print(f'=== RESULT FOR {cid} ===')
    for l in res.splitlines()[:25]:
        print(l)
