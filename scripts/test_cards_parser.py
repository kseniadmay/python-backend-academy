import zipfile
import re

z = zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip')

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

def is_code_line(s):
    s_cl = s.strip()
    if s_cl.startswith('- '):
        s_cl = s_cl[2:].strip()
    if not s_cl:
        return False
    if re.search(r'[а-яА-ЯёЁ]', s_cl):
        return False
    if re.search(r'(=|\[|\(|import|def|class|slice)', s_cl):
        return True
    return False

def clean_card_file_perfect(content):
    content = clean_dashes(content)
    lines = content.splitlines()
    
    # 1. Сгруппируем строки по логическим блокам
    blocks = []
    curr = []
    
    for line in lines:
        s = line.strip()
        if not s or s.startswith('#') or s in ('- query:', 'query:', '-'):
            continue
        # Пропускаем хлебные крошки тегов
        if re.match(r'^(?:-\s*)?\[[\'"].*?[\'"]', s):
            continue
            
        if line.startswith('- ') and not re.match(r'^\s{2,}', line):
            if curr:
                blocks.append(curr)
                curr = []
            curr.append(line[2:].strip())
        else:
            if curr:
                curr.append(line)
            else:
                curr.append(line)
    if curr:
        blocks.append(curr)
        
    out_cards = []
    
    for b in blocks:
        text_full = '\n'.join(b)
        
        # 1) Блок с fenced code block ```
        if '```' in text_full:
            q_part = []
            code_part = []
            ans_part = []
            state = 'q'
            for bline in b:
                bs = bline.strip()
                if bs.startswith('```'):
                    if state == 'q':
                        state = 'code'
                    else:
                        state = 'ans'
                    continue
                if state == 'q':
                    q_part.append(bs)
                elif state == 'code':
                    if bs:
                        code_part.append(bs)
                elif state == 'ans':
                    ans_part.append(bs)
                    
            q_str = ' '.join(q_part).strip()
            code_str = '; '.join(code_part).strip()
            ans_str = ' '.join(ans_part).strip()
            
            # Очищаем ведущий >> или - >>
            ans_str = re.sub(r'^(?:-\s*)?>>\s*', '', ans_str).strip()
            # Очищаем префикс "prompt - результат? -> answer"
            if 'результат?' in ans_str:
                m_ans = re.search(r'результат\?\s*(?:→|->)\s*(.*)', ans_str)
                if m_ans:
                    ans_str = m_ans.group(1).strip()
                    
            if code_str:
                # Оборачиваем код в бэктики
                code_formatted = f'`{code_str}`'
                if q_str.endswith('?'):
                    final_q = f'{q_str[:-1].strip()}: {code_formatted} ?'
                else:
                    final_q = f'{q_str} {code_formatted}'
            else:
                final_q = q_str
                
            out_cards.append((fix_slice_colons(final_q), fix_slice_colons(ans_str)))
            continue
            
        # 2) Блок с кодом в заголовке и вопросом под ним (например a = ..., b = ...)
        # Собираем все строки кода в начале блока
        code_lines = []
        q_lines = []
        in_code_prefix = True
        for bline in b:
            bs = bline.strip()
            if bs.startswith('- '):
                bs_no_dash = bs[2:].strip()
            else:
                bs_no_dash = bs
                
            if in_code_prefix and is_code_line(bs_no_dash) and '>>' not in bs:
                code_lines.append(bs_no_dash)
            else:
                in_code_prefix = False
                if bs:
                    q_lines.append(bs)
                    
        if code_lines and q_lines:
            setup_code = '; '.join(code_lines)
            setup_formatted = f'`{setup_code}`'
            for ql in q_lines:
                qs = ql.strip()
                if '>>' in qs:
                    parts = qs.split('>>', 1)
                    q = parts[0].strip()
                    if q.startswith('- '):
                        q = q[2:].strip()
                    a = parts[1].strip()
                    full_q = f'При {setup_formatted}: {q}'
                    out_cards.append((fix_slice_colons(full_q), fix_slice_colons(a)))
            continue
            
        # 3) Обычная карточка на 1-2 строки без кода
        # Соединяем в одну строку
        full_line = ' '.join([x.strip() for x in b])
        if full_line.startswith('- '):
            full_line = full_line[2:].strip()
        if '>>' in full_line:
            parts = full_line.split('>>', 1)
            q = parts[0].strip()
            a = parts[1].strip()
            out_cards.append((fix_slice_colons(q), fix_slice_colons(a)))
        else:
            if full_line:
                out_cards.append((fix_slice_colons(full_line), ''))
                
    # Формируем финальный строго нумерованный список
    numbered_lines = []
    for idx, (q, a) in enumerate(out_cards, 1):
        if a:
            numbered_lines.append(f'{idx}. {q} >> {a}')
        else:
            numbered_lines.append(f'{idx}. {q}')
            
    return '\n'.join(numbered_lines) + '\n'

# Test on 3 files
for fn in ['Переменные args и kwargs.md', 'Срезы.md', 'Ловушка изменяемых аргументов.md']:
    for name in z.namelist():
        if name.endswith('/' + fn):
            print('=== ' + fn + ' ===')
            res = clean_card_file_perfect(z.read(name).decode('utf-8'))
            for l in res.splitlines()[:6]:
                print(l)
