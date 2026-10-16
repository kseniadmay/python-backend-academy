const fs = require('fs');
const filePath = 'C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md';
const content = fs.readFileSync(filePath, 'utf8');
const lines = content.split('\n');

let inTheory = false;
let inCoding = false;
let inChecklist = false;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.startsWith('### ') || line.startsWith('## ')) {
    inTheory = false;
    inCoding = false;
    inChecklist = false;
  } else if (line.includes('**Теория')) {
    inTheory = true;
    inCoding = false;
    inChecklist = false;
  } else if (line.includes('**Кодинг') || line.includes('кодинг')) {
    inTheory = false;
    inCoding = true;
    inChecklist = false;
  } else if (line.includes('Чек-лист') || line.includes('чек-лист')) {
    inTheory = false;
    inCoding = false;
    inChecklist = true;
  } else if (line.startsWith('    - ') && !line.startsWith('    - [ ] ') && !line.startsWith('    - [x] ')) {
    if (!line.includes('⏱️') && !line.includes('🎯')) {
      console.log(`Line ${i+1} [Theory=${inTheory}, Coding=${inCoding}, Check=${inChecklist}]: ${line}`);
    }
  }
}
