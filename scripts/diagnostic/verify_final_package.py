import os
import zipfile
import re
import hashlib

_here = os.path.dirname(os.path.abspath(__file__))
project_zip = os.path.normpath(os.path.join(_here, '..', 'RemNote_Python_Mastery_FIXED.zip'))

assert os.path.exists(project_zip), f"Project zip missing: {project_zip}"

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

h = file_hash(project_zip)
print(f"Archive SHA256: {h}")

z = zipfile.ZipFile(project_zip)
names = z.namelist()
print(f"Total files in archive: {len(names)}")

notes = [n for n in names if '📚 Конспекты' in n and n.endswith('.md')]
cards = [n for n in names if '📇 Карточки' in n and n.endswith('.md')]
maps = [n for n in names if 'Карта Мастерства' in n]

print(f"Notes count: {len(notes)} (expected: 238)")
print(f"Cards count: {len(cards)} (expected: 286)")
print(f"Map count:   {len(maps)} (expected: 1)")

assert len(notes) == 238, f"Expected 238 notes, got {len(notes)}"
assert len(cards) == 286, f"Expected 286 cards, got {len(cards)}"
assert len(maps) == 1, f"Expected 1 map, got {len(maps)}"

errors = []
total_headings = 0
total_dividers = 0

for nf in notes:
    content = z.read(nf).decode('utf-8')
    
    # 1. Заголовки с паразитным дефисом (- ## или - ###) - недопустимы
    bullet_h = re.findall(r'^- #{2,3}\s+.*', content, re.M)
    if bullet_h:
        errors.append(f"{nf}: Found bullet headings (- ##): {bullet_h}")
        
    # 2. Чистые валидные заголовки H2 / H3 без дефиса
    valid_h = re.findall(r'^#{2,3}\s+.*', content, re.M)
    total_headings += len(valid_h)
    
    # 3. Разделители
    divs = re.findall(r'^---$', content, re.M)
    total_dividers += len(divs)
    
    # 4. Проверка сбалансированности блоков кода
    fences = len(re.findall(r'^```', content, re.M))
    if fences % 2 != 0:
        errors.append(f"{nf}: Unbalanced code blocks (count: {fences})")
        
    # 5. Проверка срезов ::
    broken_slices = re.findall(r'\[[^\]]*?::[^\]]*?\]', content)
    if broken_slices:
        errors.append(f"{nf}: Broken slice syntax: {broken_slices}")

# Специальная проверка K-003
k003_path = [n for n in notes if 'К-003' in n][0]
k003_content = z.read(k003_path).decode('utf-8')
assert '- `start` – индекс' in k003_content, "K-003: start bullet missing"
assert '- `stop` – индекс' in k003_content, "K-003: stop bullet missing"
assert '- `step` – шаг' in k003_content, "K-003: step bullet missing"
assert '## Что такое срез' in k003_content, "K-003: ## Что такое срез missing"
assert '## Синтаксис `[start:stop:step]`' in k003_content, "K-003: ## Синтаксис missing"

# Специальная проверка K-004
k004_path = [n for n in notes if 'К-004' in n][0]
k004_content = z.read(k004_path).decode('utf-8')
assert '## frozenset – неизменяемая версия set' in k004_content, "K-004: ## frozenset missing"
assert '## Главная практическая причина существования – хэшируемость' in k004_content, "K-004: ## Главная missing"

print("\n--- DETAILED VERIFICATION RESULTS ---")
print(f"Total Clean Headings formatted as '##' / '###': {total_headings}")
print(f"Total Dividers '---': {total_dividers}")
print(f"Total Errors: {len(errors)}")

if errors:
    for e in errors:
        print("ERROR:", e)
    raise SystemExit(1)
else:
    print("ALL VERIFICATION CHECKS PASSED PERFECTLY!")
