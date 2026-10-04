import zipfile
import re
import os

zip_path = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Mastery_Import_Ready.zip'
z = zipfile.ZipFile(zip_path)

all_files = z.namelist()
print(f'1. Total files in zip: {len(all_files)}')
assert len(all_files) == 443, f'Expected 443 files, got {len(all_files)}'

# 2. Модули
modules = sorted(list(set(f.split('/')[1] for f in all_files if '/' in f and f.split('/')[1].startswith('0') and not f.split('/')[1].endswith('.md'))))
print(f'2. Modules ({len(modules)}):', modules)
assert len(modules) == 6, f'Expected 6 modules, got {len(modules)}'
assert modules[0] == '01 · 🐍 Python'
assert modules[-1] == '06 · 🚀 Инфраструктура'

# 3. Конспекты и карточки
notes = [f for f in all_files if 'Конспекты' in f and f.endswith('.md')]
cards = [f for f in all_files if 'Карточки' in f and f.endswith('.md')]
print(f'3. Notes count: {len(notes)}, Cards count: {len(cards)}')
assert len(notes) == 216, f'Expected 216 notes, got {len(notes)}'
assert len(cards) == 226, f'Expected 226 cards, got {len(cards)}'

# 4. Проверка H1 заголовков во всех файлах
notes_without_h1 = []
for nf in notes:
    lines = z.read(nf).decode('utf-8').splitlines()
    if not lines or not lines[0].startswith('# К-'):
        notes_without_h1.append(nf)
print(f'4. Notes without valid H1: {len(notes_without_h1)}')
assert len(notes_without_h1) == 0, f'Notes without H1: {notes_without_h1[:5]}'

cards_without_h1 = []
for cf in cards:
    lines = z.read(cf).decode('utf-8').splitlines()
    if not lines or not lines[0].startswith('# Ф-'):
        cards_without_h1.append(cf)
print(f'5. Cards without valid H1: {len(cards_without_h1)}')
assert len(cards_without_h1) == 0, f'Cards without H1: {cards_without_h1[:5]}'

# 5. Проверка ссылок в Карте Мастерства
map_text = z.read('Собеседования/00 · 🗺️ Карта Мастерства.md').decode('utf-8')
k_links = re.findall(r'\[\[(К-\d+\.[^\]]+)\]\]', map_text)
f_links = re.findall(r'\[\[(Ф-\d+\.[^\]]+)\]\]', map_text)
all_links = k_links + f_links
print(f'6. Total links in Mastery Map: {len(all_links)} (K: {len(k_links)}, F: {len(f_links)})')
assert len(all_links) == 498, f'Expected 498 links, got {len(all_links)}'

# Проверяем, что каждая ссылка ведет на реальный файл с таким же H1
file_basenames = {os.path.basename(f)[:-3]: f for f in all_files if f.endswith('.md')}
broken_links = [l for l in all_links if l not in file_basenames]
print(f'7. Broken links: {len(broken_links)}')
assert len(broken_links) == 0, f'Broken links: {broken_links[:10]}'

# 6. Проверка отсутствия артефактов "    - ."
dot_artifacts = []
for f in all_files:
    text = z.read(f).decode('utf-8')
    for l in text.splitlines():
        if re.match(r'^\s*-\s*\.\s*$', l) or re.match(r'^\s*-\s*#\s*\.\s*$', l):
            dot_artifacts.append((f, l))
            break
print(f'8. Files with broken dot artifacts: {len(dot_artifacts)}')
assert len(dot_artifacts) == 0, f'Found dot artifacts in: {dot_artifacts[:5]}'

# 7. Проверка типографики (запрет длинных тире)
dash_errors = []
for f in all_files:
    text = z.read(f).decode('utf-8')
    if '—' in text:
        dash_errors.append(f)
print(f'9. Files with em-dashes (—): {len(dash_errors)}')
assert len(dash_errors) == 0, f'Found em-dashes in: {dash_errors[:5]}'

# 8. Проверка вертикальных разделителей в Карте Мастерства
empty_spacer_count = map_text.count('\n- \n') + map_text.count('\n    - \n')
print(f'10. Vertical spacer bullets in Mastery Map: {empty_spacer_count}')
assert empty_spacer_count > 50, f'Too few spacers: {empty_spacer_count}'

print('\n🎉 ВСЕ 10 ПРОВЕРОК АУДИТА УСПЕШНО ПРОЙДЕНЫ (10/10 PASSED)!')
