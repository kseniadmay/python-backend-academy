const fs = require('fs');
const filePath = 'C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md';
const content = fs.readFileSync(filePath, 'utf8');
const lines = content.split('\n');

const newLines = [];

for (let i = 0; i < lines.length; i++) {
  let line = lines[i];

  // 1. Fix headings starting with "- ###" or "- ##"
  if (line.startsWith('- ###')) {
    line = line.substring(2);
  } else if (line.startsWith('- ##')) {
    line = line.substring(2);
  }

  // 2. Fix unindented subheadings in days 05-07, 14, 21, 28, 35 (were "    - 🌅" or "    - 💻")
  if (line.startsWith('    - 🌅') || line.startsWith('    - 💻')) {
    line = line.substring(4);
  }

  // 3. Fix Day 04 coding tasks (were "- 🥚 Уровень 1 ...") -> indent to "    - [ ] 🥚 Уровень 1 ..."
  if (/^- \S+\s+Уровень \d/u.test(line)) {
    const match = line.match(/^- (.*)/);
    line = '    - [ ] ' + match[1];
  }

  // 4. Fix items that have 8 spaces in days 05-07, 14, 21, 28, 35 (were "        - ...")
  if (line.startsWith('        - ')) {
    let rest = line.substring(10);
    // If it doesn't already have [ ] or [x]
    if (!rest.startsWith('[ ] ') && !rest.startsWith('[x] ')) {
      // Don't add checkbox to timer note or stand-out header
      if (rest.startsWith('⏱️') || rest.startsWith('🎯') || rest.startsWith('Закрепление')) {
        line = '    - ' + rest;
      } else {
        line = '    - [ ] ' + rest;
      }
    } else {
      line = '    - ' + rest;
    }
  }

  // 5. Fix items with 4 spaces that are tasks or theory without checkboxes
  if (line.startsWith('    - ') && !line.startsWith('    - [ ] ') && !line.startsWith('    - [x] ')) {
    let rest = line.substring(6);
    // If it's a task with level emoji
    if (/\S+\s+Уровень \d/u.test(rest)) {
      line = '    - [ ] ' + rest;
    }
    // If it's a link [Topic]() or [🐍 Python]()
    else if (rest.match(/^\[.*\]\(\)/)) {
      line = '    - [ ] ' + rest;
    }
    // If it's a checklist item
    else if (rest.startsWith('Могу ') || rest.startsWith('Понимаю ') || rest.startsWith('Решил ') || rest.startsWith('Знаю ') || rest.startsWith('Умею ') || rest.startsWith('Пишу ')) {
      line = '    - [ ] ' + rest;
    }
  }

  // 6. Fix checklist items with 8 spaces or more: "        - Могу..."
  if (line.match(/^\s{6,16}-\s+(Могу|Понимаю|Решил|Знаю|Умею|Пишу)/)) {
    const match = line.match(/^\s+-\s+(.*)/);
    if (match) {
      line = '    - [ ] ' + match[1];
    }
  }

  // 7. Fix standalone checklist header "✅ **Чек-лист"
  if (line.startsWith('✅ **Чек-лист')) {
    line = '- ' + line;
  }

  // 8. Fix standout items in review days: "        - Найдите баг:" -> "    - [ ] Найдите баг:"
  if (line.match(/^\s+-\s+(Найдите баг|System Design Lite)/)) {
    const match = line.match(/^\s+-\s+(.*)/);
    line = '    - [ ] ' + match[1];
  }

  // 9. Fix standout header: "            - 🎯 **Стенд-аут" -> "    - 🎯 **Стенд-аут"
  if (line.match(/^\s+-\s+🎯/)) {
    const match = line.match(/^\s+-\s+(🎯.*)/);
    line = '    - ' + match[1];
  }

  newLines.push(line);
}

// Write the cleanly formatted file
fs.writeFileSync(filePath, newLines.join('\n'), 'utf8');
console.log('Successfully written formatted file:', filePath);

// Let's check statistics
let countTasks = 0;
let countTheory = 0;
let countChecklist = 0;

for (const l of newLines) {
  if (l.match(/\[ \]\s+\S+\s+Уровень \d/u)) countTasks++;
  if (l.match(/\[ \]\s+\[.*\]\(\)/)) countTheory++;
  if (l.match(/\[ \]\s+(Могу|Понимаю|Решил|Знаю|Умею|Пишу)/)) countChecklist++;
}

console.log('Count tasks with checkbox:', countTasks);
console.log('Count theory with checkbox:', countTheory);
console.log('Count checklist with checkbox:', countChecklist);
