import re

with open('academy.html', 'r', encoding='utf-8') as f:
    text = f.read()

decks = re.findall(r'["\'](Ф-\d+[^"\']*)["\']\s*:', text)
sample = sorted(list(set([d for d in decks if d.startswith('Ф-2')])))
print('Unique decks with Ф-2:', sample)
