import os
import zipfile
import re
import hashlib

desktop_zip = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED.zip'
docs_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python_Mastery_FIXED.zip'

assert os.path.exists(desktop_zip), "Desktop zip missing!"
assert os.path.exists(docs_zip), "Docs zip missing!"

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

hash_desktop = file_hash(desktop_zip)
hash_docs = file_hash(docs_zip)
print(f"Desktop SHA256: {hash_desktop}")
print(f"Docs SHA256:    {hash_docs}")
assert hash_desktop == hash_docs, "Zip files differ in checksum!"

z = zipfile.ZipFile(desktop_zip)
names = z.namelist()
print(f"Total files in archive: {len(names)}")

notes = [n for n in names if '📚 Конспекты' in n and n.endswith('.md')]
cards = [n for n in names if '📇 Карточки' in n and n.endswith('.md')]
maps = [n for n in names if 'Карта Мастерства' in n]

print(f"Notes count: {len(notes)} (expected: 216)")
print(f"Cards count: {len(cards)} (expected: 226)")
print(f"Map count:   {len(maps)} (expected: 1)")

assert len(notes) == 216, f"Expected 216 notes, got {len(notes)}"
assert len(cards) == 226, f"Expected 226 cards, got {len(cards)}"
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
