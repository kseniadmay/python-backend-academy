const fs = require('fs');
const sections = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\root_sections_audit.json', 'utf8'));
const parsed = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));

// All tasks and theories in parsed schedule with their day
function normalize(str) {
  return (str || '')
    .toLowerCase()
    .replace(/[^a-zа-яё0-9]/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

const itemToDay = [];
for (const w of parsed.weeks) {
  for (const d of w.days) {
    for (const s of d.sections) {
      for (const it of s.items) {
        const clean = it.replace(/^-\s*(\[\s*\]\s*)?/, '').trim();
        const norm = normalize(clean);
        if (norm.length > 5) {
          itemToDay.push({ norm, day: d.num, secType: s.type });
        }
      }
    }
  }
}

console.log('Total indexable items in schedule:', itemToDay.length);

const matchedSections = [];
for (const sec of sections) {
  if (sec.kidsCount === 0) continue;
  let matchDay = null;
  let matchSec = null;
  
  for (const k of sec.sampleKids) {
    const kNorm = normalize(k);
    if (kNorm.length < 5) continue;
    for (const item of itemToDay) {
      if (item.norm.includes(kNorm) || kNorm.includes(item.norm) || (item.norm.slice(0, 20) === kNorm.slice(0, 20))) {
        matchDay = item.day;
        matchSec = item.secType;
        break;
      }
    }
    if (matchDay) break;
  }
  matchedSections.push({
    id: sec.id,
    kidsCount: sec.kidsCount,
    text: sec.text,
    matchDay,
    matchSec
  });
  console.log(`[${sec.id}] (${sec.kidsCount} kids) "${sec.text.slice(0, 40)}" -> Day ${matchDay} (${matchSec})`);
}

fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\matched_sections.json', JSON.stringify(matchedSections, null, 2));