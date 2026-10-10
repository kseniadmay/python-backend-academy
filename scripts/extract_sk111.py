with open('academy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Вытащим ALL_NOTES_COMBINED, ALL_DECKS_COMBINED, IDE_TASKS_BY_ID
# или напишем JS-скрипт для NodeJS, который распарсит и выведет всё точно
js_script = '''
const fs = require('fs');
const html = fs.readFileSync('academy.html', 'utf8');

// Найдем PY_MASTERY
const pyMasteryMatch = html.match(/PY_MASTERY\\s*=\\s*(\\{.*?\\});\\s*(?:const|let|var|function|Object)/s);
const pyMastery = JSON.parse(pyMasteryMatch[1]);
const sk111 = pyMastery.units[0].skills[0];

console.log('Skill 1.1.1:', sk111.title);
console.log('kIds:', sk111.kIds);
console.log('fIds:', sk111.fIds);
console.log('taskIds:', sk111.taskIds);
'''

with open('scripts/extract_sk111_details.js', 'w', encoding='utf-8') as f_out:
    f_out.write(js_script)
