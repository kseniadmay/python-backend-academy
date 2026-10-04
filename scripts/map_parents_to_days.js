const fs = require('fs');
const parentsAudit = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parents_audit.json', 'utf8'));
const parsed = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));

// Build mapping of task title -> dayNum
function normalize(str) {
  return (str || '')
    .toLowerCase()
    .replace(/[^a-zа-яё0-9]/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

const taskToDay = [];
for (const w of parsed.weeks) {
  for (const d of w.days) {
    for (const s of d.sections) {
      if (s.type === 'coding') {
        for (const it of s.items) {
          const clean = it.replace(/^-\s*(\[\s*\]\s*)?/, '').trim();
          const norm = normalize(clean);
          if (norm.length > 5) {
            taskToDay.push({ norm, day: d.num });
          }
        }
      }
    }
  }
}

const theoryToDay = [];
for (const w of parsed.weeks) {
  for (const d of w.days) {
    for (const s of d.sections) {
      if (s.type === 'theory') {
        for (const it of s.items) {
          const clean = it.replace(/^-\s*(\[\s*\]\s*)?/, '').trim();
          const norm = normalize(clean);
          if (norm.length > 5) {
            theoryToDay.push({ norm, day: d.num });
          }
        }
      }
    }
  }
}

// We also need all items in database to look up what tasks are inside each parent
// Let's create the script that runs in Chrome CDP and does this accurate mapping