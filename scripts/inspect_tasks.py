import json
with open(r'C:\Users\fury6\Downloads\Практика кода — тренажёр с IDE.html', encoding='utf-8') as f:
    lines = f.readlines()
tasks = json.loads(lines[317].strip()[len('const TASKS = '):-1])
for t in tasks[239:320]:
    print(f"#{t['id']} [L{t['level']}] {t['title']}")
