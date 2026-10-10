with open('academy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Ищем обработчик кликов по документу
idx = text.find("document.addEventListener('click'")
if idx == -1:
    idx = text.find('document.addEventListener("click"')
print('Click listener at:', idx)

# Посмотрим, где обрабатываются data-py-select-k, data-py-select-f, data-py-select-task
for ev in ['data-py-select-k', 'data-py-select-f', 'data-py-select-task', 'data-py-select-exam']:
    pos = text.find(f"closest('[{ev}]')", idx)
    if pos == -1:
        pos = text.find(f'closest("[{ev}]")', idx)
    print(f"{ev}: {pos}")
    if pos != -1:
        print(text[pos-40:pos+300])
        print('-'*40)
