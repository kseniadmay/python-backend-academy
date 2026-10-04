import re

with open(r'C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Searching for nav in HTML structure:')
for m in re.finditer(r'<nav[^>]*>', html):
    print('Nav tag:', m.group(0))

for m in re.finditer(r'id=["\']([^"\']*nav[^"\']*)["\']', html, re.I):
    print('Nav id:', m.group(0))

for m in re.finditer(r'class=["\']([^"\']*nav[^"\']*)["\']', html, re.I):
    print('Nav class:', m.group(0))

print('\nSearching for "Карта" in JS code:')
for m in re.finditer(r'.{0,50}Карта.{0,50}', html):
    snippet = m.group(0).strip()
    if 'Дашборд' in snippet or 'nav' in snippet or 'route' in snippet or 'menu' in snippet or 'icon' in snippet:
        print('Nav match:', snippet)
