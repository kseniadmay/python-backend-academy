import os
import re
import zipfile
import hashlib

def run_platinum_audit():
    _here = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.normpath(os.path.join(_here, '..', 'RemNote_Python_Mastery_FIXED'))
    project_zip = os.path.normpath(os.path.join(_here, '..', 'RemNote_Python_Mastery_FIXED.zip'))
    
    if os.path.isdir(project_dir):
        names = []
        for root, _, files in os.walk(project_dir):
            for f in files:
                if f == '.DS_Store' or f.startswith('._'):
                    continue
                rel = os.path.relpath(os.path.join(root, f), project_dir).replace('\\', '/')
                names.append(rel)
        print(f"[OK] Source directory loaded: {project_dir}")
        read_content = lambda p: open(os.path.join(project_dir, p.replace('/', os.sep)), 'r', encoding='utf-8').read()
    elif os.path.exists(project_zip):
        with open(project_zip, 'rb') as f1:
            h1 = hashlib.sha256(f1.read()).hexdigest()
        print(f"[OK] Archive found ({project_zip})")
        print(f"[OK] SHA256: {h1}")
        z = zipfile.ZipFile(project_zip)
        names = z.namelist()
        read_content = lambda p: z.read(p).decode('utf-8')
    else:
        raise AssertionError(f"Neither dir ({project_dir}) nor zip ({project_zip}) found!")
    
    print(f"[OK] Total files: {len(names)} (expected 525)")
    assert len(names) == 525, f"Expected 525 files, got {len(names)}"
    
    notes = [n for n in names if '📚 Конспекты' in n and n.endswith('.md')]
    cards = [n for n in names if '📇 Карточки' in n and n.endswith('.md')]
    maps = [n for n in names if '00 · 🗺️ Карта Мастерства.md' in n]
    
    assert len(notes) == 238, f"Expected 238 notes, got {len(notes)}"
    assert len(cards) == 286, f"Expected 286 cards, got {len(cards)}"
    assert len(maps) == 1, f"Expected 1 map, got {len(maps)}"
    print(f"[OK] 238 Notes, 286 Cards, 1 Map verified")
    
    # 2. Глубокий аудит конспектов
    note_errors = []
    total_h2 = 0
    total_divs = 0
    total_flashcards = 0
    
    for nf in notes:
        content = read_content(nf)
        lines = content.splitlines()
        
        # а) Проверка первой строки: флешкарта без буллета
        if lines:
            first = lines[0].strip()
            if 'Перечитать конспект' in first:
                if first.startswith(('- ', '• ', '* ')):
                    note_errors.append(f"{nf}: Flashcard has bullet prefix: {first}")
                if '>>' not in first:
                    note_errors.append(f"{nf}: Flashcard missing '>>': {first}")
                total_flashcards += 1
                
        # б) Проверка заголовков: строго '## ' или '### ', без ведущего '- '
        bullet_headings = re.findall(r'^\s*-\s*#{2,3}\s+.*', content, re.M)
        if bullet_headings:
            note_errors.append(f"{nf}: Contains bullet headings: {bullet_headings}")
            
        clean_headings = re.findall(r'^#{2,3}\s+.*', content, re.M)
        total_h2 += len(clean_headings)
        
        # в) Проверка разделителей
        dividers = re.findall(r'^---$', content, re.M)
        total_divs += len(dividers)
        
        # г) Проверка сбалансированности блоков кода
        fences = len(re.findall(r'^```', content, re.M))
        if fences % 2 != 0:
            note_errors.append(f"{nf}: Unbalanced code blocks (count: {fences})")
            
        # д) Проверка отсутствия дефисов перед кодом внутри блоков кода
        in_c = False
        cur_lang = ''
        for line_no, l in enumerate(lines, 1):
            if l.startswith('```'):
                if not in_c:
                    in_c = True
                    cur_lang = l[3:].strip().lower()
                else:
                    in_c = False
                    cur_lang = ''
                continue
            if in_c and l.strip().startswith('- '):
                # В YAML, Markdown, diff и текстовых блоках списки на дефисах валидны
                if cur_lang in ('yaml', 'yml', 'markdown', 'md', 'text', 'txt', 'diff'):
                    continue
                # Допускаются только комментарии или специфические строки, но не артефакты списка
                if not re.search(r'#|//', l):
                    note_errors.append(f"{nf}:{line_no}: Code line starts with '- ': {l}")
                    
        # е) Проверка срезов Python (:: не должно вызывать карточку RemNote)
        broken_slices = re.findall(r'\[[^\]]*?::[^\]]*?\]', content)
        if broken_slices:
            note_errors.append(f"{nf}: Broken slice syntax: {broken_slices}")
            
    assert len(note_errors) == 0, f"Note errors found ({len(note_errors)}):\n" + "\n".join(note_errors[:10])
    print(f"[OK] Notes audit passed:")
    print(f"     Total Flashcards: {total_flashcards}")
    print(f"     Total Clean Headings: {total_h2}")
    print(f"     Total Dividers: {total_divs}")
    
    # 3. Глубокий аудит карточек
    card_errors = []
    total_qa = 0
    
    for cf in cards:
        content = read_content(cf)
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        
        expected_idx = 1
        in_code = False
        waiting_answer = False
        
        for line_no, l in enumerate(lines, 1):
            if l.startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            if waiting_answer:
                if '>>' in l:
                    waiting_answer = False
                    total_qa += 1
                continue
            if not re.match(r'^\d+\.\s+', l):
                card_errors.append(f"{cf}:{line_no}: Line not numbered: {l[:50]}")
                continue
                
            m_num = re.match(r'^(\d+)\.\s+(.*)', l)
            if m_num:
                num = int(m_num.group(1))
                if num != expected_idx:
                    card_errors.append(f"{cf}:{line_no}: Numbering sequence broken: expected {expected_idx}, got {num}")
                expected_idx += 1
                
            if '>>' in l:
                total_qa += 1
            else:
                waiting_answer = True
                
            # Проверка срезов в карточках
            broken_slices = re.findall(r'\[[^\]]*?::[^\]]*?\]', l)
            if broken_slices:
                card_errors.append(f"{cf}:{line_no}: Broken slice in card: {broken_slices}")
                
    assert len(card_errors) == 0, f"Card errors found ({len(card_errors)}):\n" + "\n".join(card_errors[:10])
    print(f"[OK] Cards audit passed: {total_qa} total flashcards strictly sequenced 1..N")
    
    # 4. Проверка Карты Мастерства
    map_content = read_content('00 · 🗺️ Карта Мастерства.md')
    assert len(map_content) > 50000, f"Map content too short: {len(map_content)}"
    
    # Проверка ссылок на конспекты и карточки
    link_targets = re.findall(r'\[.*?\]\((.*?\.md)\)', map_content)
    broken_links = [lt for lt in link_targets if lt not in names]
    assert len(broken_links) == 0, f"Broken links in Mastery Map: {broken_links[:10]}"
    print(f"[OK] Mastery Map audit passed: {len(link_targets)} valid relative links verified (0 broken)")
    
    print("\n========================================================")
    print("      PLATINUM CERTIFICATION SUCCESSFUL (100% PERFECT)  ")
    print("========================================================")

if __name__ == '__main__':
    run_platinum_audit()
