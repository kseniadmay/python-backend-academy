import zipfile
import re

zip_path = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED.zip'
z = zipfile.ZipFile(zip_path, 'r')

print("=== 1. VERIFYING K-001 ===")
for n in z.namelist():
    if 'К-001' in n:
        c = z.read(n).decode('utf-8')
        print(f"File: {n}")
        for i, l in enumerate(c.splitlines()[:25]):
            print(f"  {i+1:2d}: {l}")
        break

print("\n=== 2. VERIFYING GRAPHS NOTE (K-009) ===")
for n in z.namelist():
    if 'графа' in n.lower() and 'конспекты' in n.lower():
        c = z.read(n).decode('utf-8')
        print(f"File: {n}")
        for i, l in enumerate(c.splitlines()[:25]):
            print(f"  {i+1:2d}: {l}")
        break

print("\n=== 3. VERIFYING CARD SAMPLE ===")
for n in z.namelist():
    if '📇 Карточки' in n and '01' in n:
        c = z.read(n).decode('utf-8')
        print(f"File: {n}")
        for i, l in enumerate(c.splitlines()[:15]):
            print(f"  {i+1:2d}: {l}")
        break

print("\n=== 4. VERIFYING MASTERY MAP AIR/DIVIDERS ===")
map_text = z.read('00 · 🗺️ Карта Мастерства.md').decode('utf-8')
divider_count = map_text.count('────────────────────────────────────────')
print(f"Dividers count in Mastery Map: {divider_count}")
for i, l in enumerate(map_text.splitlines()[:35]):
    if 'Skill' in l or '─' in l or 'Unit' in l:
        print(f"  {i+1:2d}: {l}")

print("\n=== 5. AUDIT ALL 217 NOTES IN TARGET ZIP ===")
notes = [n for n in z.namelist() if '📚 Конспекты' in n and n.endswith('.md')]
print(f"Total notes in target zip: {len(notes)}")

bad_indents = 0
bad_flashcards = 0
bad_dots = 0
odd_ticks = 0

for nf in notes:
    c = z.read(nf).decode('utf-8')
    in_code = False
    for l in c.splitlines():
        if l.strip().startswith('```'):
            in_code = not in_code
            continue
        if not in_code and re.match(r'^\s+-\s+', l):
            bad_indents += 1
            print(f"Indented line outside code in {nf}: {repr(l)}")
    
    first_line = c.splitlines()[0] if c.splitlines() else ''
    if 'Перечитать конспект' in first_line and '>>' not in first_line:
        bad_flashcards += 1
        print(f"Bad flashcard in {nf}: {first_line}")
        
    if '\n- .\n' in c or '\n.\n' in c:
        bad_dots += 1
        print(f"Dot artifact in {nf}")
        
    if c.count('```') % 2 != 0:
        odd_ticks += 1
        print(f"Odd backticks in {nf}")

print(f"Audit Summary for 216 notes:")
print(f"  Bad indents outside code: {bad_indents}")
print(f"  Bad flashcards (missing >>): {bad_flashcards}")
print(f"  Dot artifacts: {bad_dots}")
print(f"  Odd code backticks: {odd_ticks}")

z.close()
