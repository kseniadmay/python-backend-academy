import json, re, os

with open(r'C:\Users\fury6\Downloads\Практика кода — тренажёр с IDE.html', encoding='utf-8') as f:
    lines = f.readlines()
tasks = json.loads(lines[317].strip()[len('const TASKS = '):-1])

base = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED'
with open(os.path.join(base, '00 · 🗺️ Карта Мастерства.md'), encoding='utf-8') as f:
    karta = f.read()

mod1_match = re.search(r'## 📁 01 · 🐍 Python(.*?)(?=## 📁 02 ·)', karta, re.S).group(1)
skill_blocks = re.split(r'- \[[ x]\] ⚡ \*\*Skill (1\.\d+\.\d+) · ([^\*]+)\*\*', mod1_match)[1:]

for i in range(0, len(skill_blocks), 3):
    sid = skill_blocks[i]
    stitle = re.sub(r'\s*\[.*?\]\s*$', '', skill_blocks[i+1]).strip()
    sbody = skill_blocks[i+2]
    prac = re.search(r'💻 \*\*Практика кодинга\*\*:\s*([^\n]+)', sbody).group(1).strip()
    # score tasks by word overlap
    words = set(re.findall(r'[a-zA-Zа-яА-ЯёЁ0-9_]{3,}', (stitle + ' ' + prac).lower()))
    scored = []
    for t in tasks:
        twords = set(re.findall(r'[a-zA-Zа-яА-ЯёЁ0-9_]{3,}', (t['title'] + ' ' + t['code']).lower()))
        scored.append((len(words & twords), t['id'], t['level'], t['title']))
    scored.sort(reverse=True)
    top3 = [(tid, lvl, tt) for sc, tid, lvl, tt in scored[:3]]
    print(f"{sid}: {prac[:55]}... -> {top3[0]} | {top3[1]}")
