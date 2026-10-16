const fs = require('fs');
const filePath = 'C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md';
if (!fs.existsSync(filePath)) {
  console.log('[SKIP] Downloaded schedule markdown not found. Scratch test skipped.');
  process.exit(0);
}
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
  if (line.match(/^- ([🥚🐣🦊🐺🐯🐉👑] Уровень \d.*)/)) {
    const match = line.match(/^- ([🥚🐣🦊🐺🐯🐉👑] Уровень \d.*)/);
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
    if (rest.match(/^[🥚🐣🦊🐺🐯🐉👑] Уровень \d/)) {
      line = '    - [ ] ' + rest;
    }
    // If it's a link [Topic]() or [🐍 Python]()
    else if (rest.match(/^\[.*\]\(\)/)) {
      line = '    - [ ] ' + rest;
    }
    // If it's a checklist item under Checklist header
    else if (rest.startsWith('Могу ') || rest.startsWith('Понимаю ') || rest.startsWith('Решил ') || rest.startsWith('Знаю ') || rest.startsWith('Умею ') || rest.startsWith('Пишу ')) {
      line = '    - [ ] ' + rest;
    }
  }

  // 6. Fix checklist items with 8 spaces: "        - Могу..."
  if (line.startsWith('        - ') || line.match(/^\s{8,12}-\s+(Могу|Понимаю|Решил|Знаю|Умею|Пишу)/)) {
    const match = line.match(/^\s+-\s+(.*)/);
    if (match) {
      line = '    - [ ] ' + match[1];
    }
  }

  // 7. Fix standalone checklist header "✅ **Чек-лист"
  if (line.startsWith('✅ **Чек-лист')) {
    line = '- ' + line;
  }

  newLines.push(line);
}

console.log('Processed lines:', newLines.length);

// Let's inspect Day 04, 05, 06, 07
console.log('\n--- Lines 80-120 ---');
for (let i = 80; i < 120; i++) {
  console.log((i+1) + ': ' + newLines[i]);
}
