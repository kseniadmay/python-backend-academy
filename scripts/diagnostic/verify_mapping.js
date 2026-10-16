const fs = require('fs');
const raw = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\sections_raw.json', 'utf8'));
const parsed = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));

function normalize(str) {
  return (str || '')
    .toLowerCase()
    .replace(/[^a-zа-яё0-9]/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// Map task texts to day in schedule
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

// Map theory texts to day in schedule
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

console.log(`Loaded ${taskToDay.length} schedule tasks and ${theoryToDay.length} schedule theories.`);

// Map task sections
const taskSectionMapping = {};
for (const sec of raw.taskSections) {
  const votes = {};
  for (const kt of sec.kidsText) {
    const kNorm = normalize(kt);
    for (const t of taskToDay) {
      if (t.norm.includes(kNorm) || kNorm.includes(t.norm) || t.norm.slice(0, 25) === kNorm.slice(0, 25)) {
        votes[t.day] = (votes[t.day] || 0) + 1;
      }
    }
  }
  let bestDay = null;
  let maxVotes = 0;
  for (const [day, count] of Object.entries(votes)) {
    if (count > maxVotes) {
      maxVotes = count;
      bestDay = parseInt(day);
    }
  }
  taskSectionMapping[sec.id] = {
    secId: sec.id,
    day: bestDay,
    votes: maxVotes,
    kidsCount: sec.kidsCount,
    text: sec.text
  };
}

// Map theory sections
const theorySectionMapping = {};
for (const sec of raw.theorySections) {
  const votes = {};
  for (const kt of sec.kidsText) {
    const kNorm = normalize(kt);
    for (const t of theoryToDay) {
      if (t.norm.includes(kNorm) || kNorm.includes(t.norm) || t.norm.slice(0, 25) === kNorm.slice(0, 25)) {
        votes[t.day] = (votes[t.day] || 0) + 1;
      }
    }
  }
  let bestDay = null;
  let maxVotes = 0;
  for (const [day, count] of Object.entries(votes)) {
    if (count > maxVotes) {
      maxVotes = count;
      bestDay = parseInt(day);
    }
  }
  theorySectionMapping[sec.id] = {
    secId: sec.id,
    day: bestDay,
    votes: maxVotes,
    kidsCount: sec.kidsCount,
    text: sec.text
  };
}

// Check if all 42 days have task sections
const daysWithTasks = {};
for (const m of Object.values(taskSectionMapping)) {
  if (m.day) {
    if (!daysWithTasks[m.day]) daysWithTasks[m.day] = [];
    daysWithTasks[m.day].push(m);
  }
}

// Check if all 40 days have theory sections
const daysWithTheories = {};
for (const m of Object.values(theorySectionMapping)) {
  if (m.day) {
    if (!daysWithTheories[m.day]) daysWithTheories[m.day] = [];
    daysWithTheories[m.day].push(m);
  }
}

console.log('Unique days with task sections:', Object.keys(daysWithTasks).length);
console.log('Unique days with theory sections:', Object.keys(daysWithTheories).length);

const missingTaskDays = [];
for (let i = 1; i <= 42; i++) {
  if (!daysWithTasks[i]) missingTaskDays.push(i);
}
console.log('Missing task days:', missingTaskDays);

const missingTheoryDays = [];
for (let i = 1; i <= 42; i++) {
  // Day 34 and Day 42 might have special handling
  if (!daysWithTheories[i]) missingTheoryDays.push(i);
}
console.log('Missing theory days:', missingTheoryDays);

fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\section_to_day_mapping.json', JSON.stringify({
  taskSectionMapping,
  theorySectionMapping
}, null, 2));
console.log('Saved mapping.');