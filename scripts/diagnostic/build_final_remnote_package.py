import os
import re
import json
import zipfile
import textwrap

remnote_python_zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
map_json_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_renaming_map.json'
mastery_map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'
out_zip_flat = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED.zip'

with open(map_json_path, 'r', encoding='utf-8') as f:
    renaming_map = json.load(f)

notes_map = renaming_map['notes']
cards_map = renaming_map['cards']

z_src = zipfile.ZipFile(remnote_python_zip_path)

def clean_dashes(text):
    return text.replace('—', '–')

module_renames = {
    '01 · 🐍 Python': '01 · 🐍 Python',
    '02 · 🌐 Web & Backend': '02 · 🌐 Web & Backend',
    '03 · 🧩 Алгоритмы': '03 · ⚡ Алгоритмы',
    '04 · 🗄️ Базы данных': '04 · 🗄️ Базы данных',
    '05 · 🏛️ Архитектура': '05 · 🏛️ Архитектура',
    '06 · ⚙️ Инфраструктура': '06 · 🚀 Инфраструктура',
}

def fix_slice_colons(text):
    # Заменяет :: на : : в срезах Python, чтобы RemNote не превращал их в двусторонние карточки <->
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
    
    # 1. Срезы внутри квадратных скобок: [::2], [::-1], [::k], [1::2], etc.
    res = re.sub(r'\[([^\]]*?)::([^\]]*?)\]', rep, text)
    # 2. Одиночные срезы в обратных кавычках или тексте
    res = re.sub(r'`\s*::\s*`', '`[: :]`', res)
    # 3. SQL каст типов
    res = res.replace("'{python,sql}'::TEXT[]", "CAST('{python,sql}' AS TEXT[])")
    res = res.replace("'::TEXT[]", "' AS TEXT[])")
    return res

def match_note(nf, first_line):
    bn = os.path.basename(nf)[:-3]
    if re.match(r'^К-\d+', bn):
        return bn
    clean_bn = re.sub(r'^\d+\.\s*', '', bn).strip()
    
    for k, v in notes_map.items():
        if k == clean_bn or k.lower() == clean_bn.lower() or k.replace('_', ' ') == clean_bn.replace('_', ' '):
            return v
            
    m = re.search(r'Перечитать конспект (.*?)→', first_line)
    if not m:
        m = re.search(r'Перечитать конспект (.*?)(>>|→)', first_line)
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

def match_card(cf):
    bn = os.path.basename(cf)[:-3]
    if re.match(r'^Ф-\d+', bn):
        return bn
    clean_bn = re.sub(r'^Ф-\d+\.\s*', '', bn).strip()
    for k, v in cards_map.items():
        if k == clean_bn or k.lower() == clean_bn.lower():
            return v
    return None

# 1. Формируем словарь путей для ссылок
doc_name_to_rel_path = {}
for item in z_src.namelist():
    parts = item.split('/')
    if len(parts) < 4:
        continue
    orig_mod = parts[-4]
    target_mod = module_renames.get(orig_mod, orig_mod)
    unit = parts[-3]
    folder_type = parts[-2]
    filename = parts[-1]
    
    if 'Конспекты' in folder_type and filename.endswith('.md'):
        first_line = z_src.read(item).decode('utf-8').splitlines()[0]
        new_title = match_note(item, first_line)
        if new_title:
            doc_name_to_rel_path[new_title] = f'{target_mod}/{unit}/📚 Конспекты/{new_title}'
            
    elif 'Карточки' in folder_type and filename.endswith('.md'):
        new_title = match_card(item)
        if new_title:
            doc_name_to_rel_path[new_title] = f'{target_mod}/{unit}/📇 Карточки/{new_title}'

print(f'Total mapped documents for links: {len(doc_name_to_rel_path)}')

# 2. Идеальный конспект (строго один плоский уровень без паразитных родителей и лесенок)
def build_perfect_note(raw_text):
    # Исправление артефакта сдвоенных кавычек и дефисов перед кодом (например, в К-054)
    raw_text = re.sub(r'-\s+`{3}\r?\n-\s+`{3}', '```', raw_text)
    raw_text = re.sub(r'^-\s+`{3}', '```', raw_text, flags=re.M)
    
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
                clean_cl = []
                for cl in code_lines:
                    cl_strip = cl.strip()
                    if cl_strip.startswith('- '):
                        clean_cl.append(cl_strip[2:])
                    else:
                        clean_cl.append(cl)
                dedented = textwrap.dedent('\n'.join(clean_cl)).splitlines()
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
                
        # 8. Заголовки (H2 и H3) -> Разделитель --- и чистый ## Заголовок БЕЗ '-'
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
        # Отступы и буллеты делаем ТОЛЬКО там, где это реально перечисление/список!
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
        clean_cl = []
        for cl in code_lines:
            cl_strip = cl.strip()
            if cl_strip.startswith('- '):
                clean_cl.append(cl_strip[2:])
            else:
                clean_cl.append(cl)
        dedented = textwrap.dedent('\n'.join(clean_cl)).splitlines()
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


# 3. Идеальные карточки (строго нумерованный список без цитат и без broken code)
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

def clean_card_file(content):
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
        full_line = ' '.join([x.strip() for x in b])
        if full_line.startswith('- '):
            full_line = full_line[2:].strip()
        if '>>' in full_line:
            parts = full_line.split('>>', 1)
            q = parts[0].strip()
            a = parts[1].strip()
            out_cards.append((fix_slice_colons(q), fix_slice_colons(a)))
        else:
            # Если разделитель вопроса и ответа был оформлен через дефис (например: Вопрос? - Ответ)
            m_qa = re.search(r'^(.*?\?)\s*[-–—]\s*(.*)$', full_line)
            if m_qa:
                q = m_qa.group(1).strip()
                a = m_qa.group(2).strip()
                out_cards.append((fix_slice_colons(q), fix_slice_colons(a)))
                
    # Формируем финальный строго нумерованный список карточек (номер + карточка RemNote >>)
    numbered_lines = []
    for q, a in out_cards:
        clean_a = a.strip()
        if not clean_a:
            continue
        clean_q = re.sub(r'^\d+\.\s*', '', q).strip()
        idx = len(numbered_lines) + 1
        numbered_lines.append(f'{idx}. {clean_q} >> {clean_a}')
            
    return '\n'.join(numbered_lines) + '\n'

# 4. Обработка Карты Мастерства
with open(mastery_map_path, 'r', encoding='utf-8') as f:
    raw_map = f.read()

raw_map = clean_dashes(raw_map)

# Нормализуем все ссылки [[...]]
def replace_link(match):
    inner = match.group(1).strip()
    name = inner.split('/')[-1]
    if name in doc_name_to_rel_path:
        return f'[[{doc_name_to_rel_path[name]}]]'
    return match.group(0)

updated_map = re.sub(r'\[\[(.*?)\]\]', replace_link, raw_map)
lines = updated_map.splitlines()

out_map = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # 1. Пропускаем верхний дублирующий заголовок H1 и пустые буллеты
    if stripped.startswith('# 🎓') or stripped == '-' or stripped == '- ':
        i += 1
        continue
        
    # 2. Блок "Как устроена программа" (чистый плоский список без цитаты >)
    if 'Как устроена программа' in stripped:
        if out_map and out_map[-1] != '':
            out_map.append('')
        out_map.append('**Как устроена программа**:')
        i += 1
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith('##') or s.startswith('- ##') or s == '---':
                break
            if s.startswith('- ') or s.startswith('> - ') or s.startswith('>- '):
                content = re.sub(r'^(?:>\s*)?-\s*', '', s)
                out_map.append(f'- {content}')
            i += 1
        out_map.append('')
        out_map.append('---')
        out_map.append('')
        continue
        
    # 3. Заголовки H2 (Модули и сводка прогресса)
    if stripped.startswith('## ') or stripped.startswith('- ## '):
        h_text = stripped[4:].strip() if stripped.startswith('- ## ') else stripped[2:].strip()
        if out_map and out_map[-1] != '':
            out_map.append('')
        out_map.append('---')
        out_map.append('')
        out_map.append(f'## {h_text}')
        out_map.append('')
        i += 1
        continue
        
    # 4. Заголовки H3 (Юниты)
    if stripped.startswith('### ') or stripped.startswith('- ### '):
        h_text = stripped[5:].strip() if stripped.startswith('- ### ') else stripped[3:].strip()
        if out_map and out_map[-1] != '':
            out_map.append('')
        out_map.append('---')
        out_map.append('')
        out_map.append(f'### {h_text}')
        out_map.append('')
        i += 1
        continue
        
    # 5. Прогресс по модулям
    if re.match(r'^(?:-\s*)?\[\s*\]\s*\*\*\d{2}\s*·', stripped):
        m_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out_map.append(f'- {m_item}')
        i += 1
        continue
        
    # 6. Блок "Как отмечать прогресс" (плоский список из 2 пунктов без лишних ступеней)
    if 'В RemNote (на телефоне или компьютере)' in stripped:
        out_map.append('- **1. В RemNote (на телефоне или компьютере)**: прочитали конспект и прогнали карточки ➔ просто ставите галочку в чекбоксе навыка.')
        i += 1
        continue
    if 'На аттестации юнита (в чате)' in stripped:
        out_map.append('- **2. На аттестации юнита (в чате)**: когда все навыки юнита закрыты, вы пишете в чат *«Сдаю Unit Test X.Y»*. Мы проводим короткое собеседование по задаче аттестации, и после успешной сдачи обновляются счётчики в сводке.')
        i += 1
        continue
    if any(phrase in stripped for phrase in ['Прочитали конспект', 'Когда все навыки', 'Мы проводим', 'После успешной сдачи']):
        i += 1
        continue

    # 7. Навыки
    if '⚡ **Skill ' in stripped:
        skill_item = re.sub(r'^(?:-\s*)?', '', stripped)
        
        # Находим предыдущий непустой элемент
        prev_item = ''
        for p in reversed(out_map):
            if p.strip():
                prev_item = p.strip()
                break
                
        # Вставляем видимый разделитель для воздуха и четкого разделения в аутлайнере RemNote
        if prev_item and not prev_item.startswith('###') and '─' not in prev_item:
            if out_map and out_map[-1] != '':
                out_map.append('')
            out_map.append('- ────────────────────────────────────────')
            out_map.append('')
            
        out_map.append(f'- {skill_item}')
        i += 1
        continue
        
    # 8. Подпункты навыка (отступ строго 2 пробела)
    if any(icon in stripped for icon in ['📖 **Конспект', '📇 **Карточки', '💻 **Практика', '🎯 **Критерий']):
        sub_item = re.sub(r'^(?:-\s*)?', '', stripped)
        sub_item = sub_item.replace('<br>&nbsp;', '').replace('<br>', '').strip()
        out_map.append(f'  - {sub_item}')
        i += 1
        continue
        
    # 9. Ссылки на конспекты и карточки (отступ строго 4 пробела)
    if stripped.startswith('- [[') or stripped.startswith('[[') or ('[[' in stripped and ']]' in stripped and not stripped.startswith('###') and not stripped.startswith('##')):
        link_item = stripped
        if link_item.startswith('- '):
            link_item = link_item[2:].strip()
        out_map.append(f'    - {link_item}')
        i += 1
        continue
        
    # 10. UNIT TEST (с разделителем для воздуха перед тестом)
    if '🏆 **UNIT TEST' in stripped:
        test_item = re.sub(r'^(?:-\s*)?', '', stripped)
        if out_map and out_map[-1] != '':
            out_map.append('')
        out_map.append('- ────────────────────────────────────────')
        out_map.append('')
        out_map.append(f'- {test_item}')
        i += 1
        continue
        
    if stripped:
        out_map.append(stripped)
    else:
        if out_map and out_map[-1] != '':
            out_map.append('')
            
    i += 1

# Финальная очистка пустых строк и дублирующихся разделителей
final_lines = []
for l in out_map:
    s = l.strip()
    if s == '---':
        has_prev_divider = False
        for prev in reversed(final_lines):
            if prev.strip() == '---':
                has_prev_divider = True
                break
            elif prev.strip() != '':
                break
        if has_prev_divider:
            continue
        final_lines.append('---')
    else:
        final_lines.append(l)

cleaned_map_lines = []
for l in final_lines:
    if not cleaned_map_lines and l == '':
        continue
    if cleaned_map_lines and cleaned_map_lines[-1] == '' and l == '':
        continue
    cleaned_map_lines.append(l)

final_map_text = '\n'.join(cleaned_map_lines) + '\n'

with open(mastery_map_path, 'w', encoding='utf-8') as f:
    f.write(final_map_text)

# 5. Сборка архива
if os.path.exists(out_zip_flat):
    os.remove(out_zip_flat)

added = 0
with zipfile.ZipFile(out_zip_flat, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
    z_out.writestr('00 · 🗺️ Карта Мастерства.md', final_map_text.encode('utf-8'))
    added += 1
    
    for item in z_src.namelist():
        parts = item.split('/')
        if len(parts) < 4:
            continue
        orig_mod = parts[-4]
        target_mod = module_renames.get(orig_mod, orig_mod)
        unit = parts[-3]
        folder_type = parts[-2]
        filename = parts[-1]
        
        if 'Конспекты' in folder_type and filename.endswith('.md'):
            raw_c = z_src.read(item).decode('utf-8')
            first_line = raw_c.splitlines()[0]
            new_title = match_note(item, first_line)
            if not new_title:
                continue
            content = build_perfect_note(raw_c)
            dest_path = f'{target_mod}/{unit}/📚 Конспекты/{new_title}.md'
            z_out.writestr(dest_path, content.encode('utf-8'))
            added += 1
            
        elif 'Карточки' in folder_type and filename.endswith('.md'):
            new_title = match_card(item)
            if not new_title:
                continue
            raw_c = z_src.read(item).decode('utf-8')
            content = clean_card_file(raw_c)
            dest_path = f'{target_mod}/{unit}/📇 Карточки/{new_title}.md'
            z_out.writestr(dest_path, content.encode('utf-8'))
            added += 1

print(f'Архив RemNote_Python_Mastery_FIXED.zip успешно собран! Всего файлов: {added}')

import shutil
# Копируем архив в Документы\Обучение Python
doc_dir = r'C:\Users\fury6\OneDrive\Документы\Обучение Python'
target_fixed_in_docs = os.path.join(doc_dir, 'RemNote_Python_Mastery_FIXED.zip')
target_old_in_docs = os.path.join(doc_dir, 'RemNote_Python.zip')

shutil.copy2(out_zip_flat, target_fixed_in_docs)
print(f'Скопировано в: {target_fixed_in_docs}')

# Закрываем z_src
z_src.close()

# Переименовываем старый битый архив 2026-09-24, если он есть
corrupted_zip = os.path.join(doc_dir, 'RemNoteExport_Fury-Inf_md_2026-09-24_06-38_FIXED.zip')
if os.path.exists(corrupted_zip):
    corrupted_bak = corrupted_zip + '.OLD_BROKEN'
    if os.path.exists(corrupted_bak):
        os.remove(corrupted_bak)
    os.rename(corrupted_zip, corrupted_bak)
    print(f'Старый поврежденный архив переименован в: {corrupted_bak}')
