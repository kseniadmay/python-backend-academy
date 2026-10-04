import re
import zipfile

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
            if in_code:
                # Начало блока кода
                out.append('```python')
            else:
                # Конец блока кода
                out.append('```')
            continue
            
        if in_code:
            # Внутри кода: убираем только внешний паразитный отступ (если весь блок был со сдвигом 4-8 пробелов),
            # но сохраняем синтаксический отступ Python!
            out.append(fix_slice_colons(line))
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
        # Это гарантирует, что они не станут родителями со стрелкой ▾ и не сдвинут текст!
        h_match = re.match(r'^(?:-\s*)?(#{2,3})\s+(.*)', s)
        if h_match:
            hashes = h_match.group(1)
            h_title = fix_slice_colons(h_match.group(2).strip())
            out.append(f'- {hashes} {h_title}')
            continue
            
        # 9. Обычный контент: убираем глубокую вложенность (табы, 4-8-12 пробелов в начале)
        # Очищаем от начального "- " или других маркеров
        clean_content = re.sub(r'^\s*-\s*', '', s).strip()
        clean_content = fix_slice_colons(clean_content)
        
        # Специальный кейс для параметров среза, если они склеены
        if 'start – индекс' in clean_content and 'stop – индекс' in clean_content:
            out.append('- `start` – индекс, с которого начинается срез (включительно).')
            out.append('- `stop` – индекс, на котором срез заканчивается (не включительно).')
            out.append('- `step` – шаг между элементами.')
            out.append('- Любой из трёх параметров можно опустить – тогда подставляется значение по умолчанию.')
            continue
            
        # Каждый пункт конспекта оформляем на плоском нулевом уровне: "- {контент}"
        out.append(f'- {clean_content}')

    return '\n'.join(out) + '\n'

# Протестируем на К-001 и графах
z = zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip')

print("=== SAMPLE 1: K-001 ===")
raw1 = z.read('RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📚 Конспекты/01. Структуры данных Python_ list, dict, set.md').decode('utf-8')
res1 = transform_note_to_flat_level(raw1)
for i, l in enumerate(res1.splitlines()[:30]):
    print(f"{i+1:2d}: {l}")

print("\n=== SAMPLE 2: Графы (была лесенка с точками) ===")
# найдем файл графов
for n in z.namelist():
    if 'Структуры данных графа' in n:
        raw2 = z.read(n).decode('utf-8')
        res2 = transform_note_to_flat_level(raw2)
        for i, l in enumerate(res2.splitlines()[:30]):
            print(f"{i+1:2d}: {l}")
        break
