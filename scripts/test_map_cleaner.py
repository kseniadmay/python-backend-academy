import re

map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'

with open(map_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Очищаем тире
text = text.replace('—', '–')

lines = text.splitlines()
out = []

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # 1. Пропускаем верхний дублирующий заголовок H1 и пустые буллеты под ним
    if stripped.startswith('# 🎓'):
        i += 1
        continue
    if stripped == '-' or stripped == '- ':
        i += 1
        continue
        
    # 2. Цитата "Как устроена программа"
    if 'Как устроена программа' in stripped:
        out.append('> **Как устроена программа**:')
        i += 1
        while i < len(lines) and (lines[i].strip().startswith('-') or lines[i].strip().startswith('>')):
            s = lines[i].strip()
            if s.startswith('- ') or s.startswith('> - ') or s.startswith('>- '):
                # убираем маркеры
                content = re.sub(r'^(?:>\s*)?-\s*', '', s)
                out.append(f'> - {content}')
            i += 1
        out.append('') # Пустая строка для воздуха
        continue
        
    # 3. Заголовки H2 (## ...)
    if stripped.startswith('## ') or stripped.startswith('- ## '):
        h_text = stripped[4:].strip() if stripped.startswith('- ## ') else stripped[2:].strip()
        out.append('')
        out.append(f'## {h_text}')
        out.append('')
        i += 1
        continue
        
    # 4. Заголовки H3 (### ...)
    if stripped.startswith('### ') or stripped.startswith('- ### '):
        h_text = stripped[5:].strip() if stripped.startswith('- ### ') else stripped[3:].strip()
        out.append('')
        out.append(f'### {h_text}')
        out.append('')
        i += 1
        continue
        
    # 5. Прогресс по модулям (- [ ] **01 · ...)
    if re.match(r'^(?:-\s*)?\[\s*\]\s*\*\*\d{2}\s*·', stripped):
        m_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out.append(f'- {m_item}')
        i += 1
        continue
        
    # 6. Блок "Как отмечать прогресс" (1., 2.)
    if re.match(r'^\d+\.\s*\*\*', stripped) or re.match(r'^(?:-\s*)?\d+\.\s*\*\*', stripped):
        num_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out.append(num_item)
        i += 1
        continue
    if 'Прочитали конспект' in stripped or 'Когда все навыки' in stripped or 'Мы проводим' in stripped or 'После успешной сдачи' in stripped:
        c_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out.append(f'   - {c_item}')
        i += 1
        continue

    # 7. Навыки (⚡ **Skill ...)
    if '⚡ **Skill ' in stripped:
        skill_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out.append('')
        out.append(f'- {skill_item}')
        i += 1
        continue
        
    # 8. Подпункты навыка (📖 Конспект теории, 📇 Карточки RemNote, 💻 Практика, 🎯 Критерий)
    if any(icon in stripped for icon in ['📖 **Конспект', '📇 **Карточки', '💻 **Практика', '🎯 **Критерий']):
        sub_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out.append(f'  - {sub_item}')
        i += 1
        continue
        
    # 9. Ссылки на конспекты и карточки ([[...]])
    if stripped.startswith('- [[') or stripped.startswith('[[') or ('[[' in stripped and ']]' in stripped and not stripped.startswith('###') and not stripped.startswith('##')):
        link_item = stripped
        if link_item.startswith('- '):
            link_item = link_item[2:].strip()
        out.append(f'    - {link_item}')
        i += 1
        continue
        
    # 10. UNIT TEST (🏆 **UNIT TEST ...)
    if '🏆 **UNIT TEST' in stripped:
        test_item = re.sub(r'^(?:-\s*)?', '', stripped)
        out.append('')
        out.append(f'- {test_item}')
        out.append('')
        i += 1
        continue
        
    # Любые другие строки
    if stripped:
        out.append(stripped)
    else:
        # Не допускаем более одной пустой строки подряд
        if out and out[-1] != '':
            out.append('')
            
    i += 1

# Убираем лишние пустые строки в начале и конце
cleaned_lines = []
for l in out:
    if not cleaned_lines and l == '':
        continue
    if cleaned_lines and cleaned_lines[-1] == '' and l == '':
        continue
    cleaned_lines.append(l)

final_text = '\n'.join(cleaned_lines) + '\n'

with open(r'C:\Users\fury6\.gemini\antigravity\scratch\formatted_map_preview.md', 'w', encoding='utf-8') as f:
    f.write(final_text)

print('Preview of formatted map saved! First 70 lines:\n')
for line in cleaned_lines[:70]:
    print(line)
