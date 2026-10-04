const fs = require('fs');

const content = fs.readFileSync('C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md', 'utf8');
const lines = content.split(/\r?\n/);

const ast = {
  title: '42 дня · Сентябрь – Октябрь 2026',
  rules: [],
  toc: [],
  weeks: []
};

let section = 'header';
let curWeek = null;
let curDay = null;
let curSubSec = null;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  if (!line) continue;

  if (line.includes('Как читать это расписание')) {
    section = 'rules';
    continue;
  }
  if (line.includes('Оглавление')) {
    section = 'toc';
    continue;
  }
  if (line.startsWith('## Неделя')) {
    section = 'week';
    const m = line.match(/##\s*Неделя\s*(\d+)\s*·\s*(.*)/);
    curWeek = {
      num: m ? parseInt(m[1]) : ast.weeks.length + 1,
      title: line.replace(/^##\s*/, '').trim(),
      days: []
    };
    ast.weeks.push(curWeek);
    curDay = null;
    curSubSec = null;
    continue;
  }
  if (line.startsWith('###')) {
    section = 'day';
    // Clean markdown bold markers from title
    const cleanTitle = line.replace(/^###\s*/, '').replace(/\*\*/g, '').trim();
    const dm = cleanTitle.match(/День\s*0?(\d+)/);
    curDay = {
      num: dm ? parseInt(dm[1]) : 0,
      title: cleanTitle,
      topic: null,
      sections: []
    };
    if (curWeek) curWeek.days.push(curDay);
    curSubSec = null;
    continue;
  }

  if (section === 'rules') {
    if (line.startsWith('-')) {
      ast.rules.push(line.replace(/^-\s*/, '').trim());
    }
  } else if (section === 'toc') {
    if (line.startsWith('-')) {
      ast.toc.push(line.replace(/^-\s*/, '').trim());
    }
  } else if (section === 'day' && curDay) {
    // Topic, or Section Header, or Item
    if (line.startsWith('- **Теория') || line.startsWith('- 🌅 **Теория') || line.startsWith('🌅 **Теория')) {
      curSubSec = {
        type: 'theory',
        title: line.replace(/^-\s*/, '').replace(/\*\*/g, '').trim(),
        items: []
      };
      curDay.sections.push(curSubSec);
    } else if (line.startsWith('- **Кодинг') || line.startsWith('- 💻 **Вечерний кодинг') || line.startsWith('💻 **Вечерний кодинг') || line.startsWith('**Кодинг')) {
      curSubSec = {
        type: 'coding',
        title: line.replace(/^-\s*/, '').replace(/\*\*/g, '').trim(),
        items: []
      };
      curDay.sections.push(curSubSec);
    } else if (line.startsWith('- ✅ **Чек-лист') || line.startsWith('✅ **Чек-лист') || line.startsWith('- ✅ Чек-лист') || line.startsWith('✅ Чек-лист')) {
      curSubSec = {
        type: 'checklist',
        title: line.replace(/^-\s*/, '').replace(/\*\*/g, '').trim(),
        items: []
      };
      curDay.sections.push(curSubSec);
    } else if (line.startsWith('🎯 **Стенд-аут') || line.startsWith('- 🎯 **Стенд-аут')) {
      curSubSec = {
        type: 'standout',
        title: line.replace(/^-\s*/, '').replace(/\*\*/g, '').trim(),
        items: []
      };
      curDay.sections.push(curSubSec);
    } else if (curSubSec) {
      // It's an item under current section
      curSubSec.items.push(line);
    } else {
      // It's a topic line before sections!
      const cleanTopic = line.replace(/^\*\*/, '').replace(/\*\*$/, '').trim();
      if (!curDay.topic) curDay.topic = cleanTopic;
      else curDay.topic += ' ' + cleanTopic;
    }
  }
}

console.log('Rules count:', ast.rules.length);
console.log('TOC count:', ast.toc.length);
console.log('Weeks count:', ast.weeks.length);
ast.weeks.forEach(w => {
  console.log(`\nWeek ${w.num} (${w.days.length} days):`);
  w.days.forEach(d => {
    const secs = d.sections.map(s => `${s.type}(${s.items.length})`).join(', ');
    console.log(`  Day ${d.num < 10 ? '0' + d.num : d.num}: "${d.title}" | Topic: "${d.topic ? d.topic.slice(0, 30) : 'none'}" | Secs: ${secs}`);
  });
});

fs.writeFileSync('local_file_ast.json', JSON.stringify(ast, null, 2), 'utf8');
