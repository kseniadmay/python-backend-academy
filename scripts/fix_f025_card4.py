# -*- coding: utf-8 -*-
import json
import re
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

new_q = "Какой результат вернёт вызов <code>[f() for f in funcs]</code>?\n\n```python\nfuncs = [lambda x=i: x for i in range(3)]\n[f() for f in funcs]\n```"

# 1. cards.json
cards_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
with open(cards_path, 'r', encoding='utf-8') as f:
    cards_data = json.load(f)

cards_data['Ф-025']['cards'][3]['q'] = new_q
with open(cards_path, 'w', encoding='utf-8') as f:
    json.dump(cards_data, f, ensure_ascii=False, indent=2)

# 2. knowledge_base
kb_path = os.path.join(_ROOT, 'knowledge_base', '01 · 🐍 Python', 'Юнит 1.2 · Функции', '📇 Карточки', 'Ф-025. Замыкание.md')
with open(kb_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 3. standards.html & academy.html
st_path = os.path.join(_ROOT, 'standards', 'standards.html')
ac_path = os.path.join(_ROOT, 'academy.html')
with open(st_path, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'(const\s+PY_MASTERY\s*=\s*)(\{.*?\})(;\s*(?:const|window))', html, re.DOTALL)
prefix = m.group(1)
data = json.loads(m.group(2))
suffix = m.group(3)

data['decks']['Ф-025']['cards'][3]['q'] = new_q
new_html = html.replace(m.group(0), prefix + json.dumps(data, ensure_ascii=False) + suffix, 1)

with open(st_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
with open(ac_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Ф-025 card #4 successfully updated across all layers!")
