const fs = require('fs');
const md = fs.readFileSync('C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md', 'utf8');

const lines = md.split('\n');

const schedule = {
  header: [],
  weeks: []
};

let currentWeek = null;
let currentDay = null;
let currentSection = null;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trimEnd();
  
  // Check week
  const weekMatch = line.match(/^## Неделя (\d+)[^·]*·\s*(.*)/);
  if (weekMatch) {
    currentWeek = {
      num: parseInt(weekMatch[1]),
      title: line.replace(/^##\s*/, ''),
      days: []
    };
    schedule.weeks.push(currentWeek);
    currentDay = null;
    currentSection = null;
    continue;
  }
  
  // Check day
  const dayMatch = line.match(/^###\s*(.*День\s*(\d+).*)/i);
  if (dayMatch) {
    const dayNum = parseInt(dayMatch[2]);
    currentDay = {
      num: dayNum,
      rawTitle: line.replace(/^###\s*/, ''),
      topics: [],
      sections: []
    };
    if (currentWeek) {
      currentWeek.days.push(currentDay);
    }
    currentSection = null;
    continue;
  }
  
  if (!currentWeek) {
    schedule.header.push(line);
    continue;
  }
  
  if (currentDay) {
    // Check section within day
    if (line.match(/^-\s*(\*\*)?Теория/i) || line.match(/^-\s*🌅\s*(\*\*)?Теория/i)) {
      currentSection = {
        type: 'theory',
        title: line.replace(/^-\s*/, ''),
        items: []
      };
      currentDay.sections.push(currentSection);
    } else if (line.match(/^-\s*(\*\*)?Кодинг/i) || line.match(/^-\s*💻\s*(\*\*)?Вечерний кодинг/i) || line.match(/^-\s*(\*\*)?Вечерний кодинг/i)) {
      currentSection = {
        type: 'coding',
        title: line.replace(/^-\s*/, ''),
        items: []
      };
      currentDay.sections.push(currentSection);
    } else if (line.match(/^-\s*🎯\s*(\*\*)?Стенд-аут/i)) {
      currentSection = {
        type: 'standout',
        title: line.replace(/^-\s*/, ''),
        items: []
      };
      currentDay.sections.push(currentSection);
    } else if (line.match(/^-\s*✅\s*(\*\*)?Чек-лист/i) || line.match(/^-\s*✅\s*(\*\*)?Итоговый чек-лист/i)) {
      currentSection = {
        type: 'checklist',
        title: line.replace(/^-\s*/, ''),
        items: []
      };
      currentDay.sections.push(currentSection);
    } else if (currentSection && line.trim().startsWith('- [ ]')) {
      currentSection.items.push(line.trim());
    } else if (currentSection && line.trim().startsWith('-') && !line.trim().startsWith('---')) {
      currentSection.items.push(line.trim());
    } else if (!currentSection && line.trim().length > 0 && !line.startsWith('#')) {
      currentDay.topics.push(line.trim());
    }
  }
}

fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', JSON.stringify(schedule, null, 2));
console.log('Parsed weeks:', schedule.weeks.length);
schedule.weeks.forEach(w => {
  console.log('Week ' + w.num + ': ' + w.days.length + ' days (' + w.days.map(d => d.num).join(', ') + ')');
});