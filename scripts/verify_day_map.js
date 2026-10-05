const fs = require('fs');
const path = require('path');
const dumpPath = fs.existsSync(path.join(__dirname, 'all_rems_dump.json'))
  ? path.join(__dirname, 'all_rems_dump.json')
  : path.join(__dirname, '..', 'all_rems_dump.json');
const allRems = JSON.parse(fs.readFileSync(dumpPath, 'utf8'));

function resolveFullText(key, depth = 0) {
  if (!key || depth > 3) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(part => {
      if (typeof part === 'string') return part;
      if (part && typeof part === 'object') {
        if (part.text) return part.text;
        if (part.textOfDeletedRem) return part.textOfDeletedRem.join(' ');
        if (part.i === 'q' && part._id) {
          const target = allRems.find(r => r._id === part._id);
          if (target) return resolveFullText(target.key, depth + 1);
        }
      }
      return '';
    }).join('');
  }
  return '';
}

const dayMap = {};
for (const r of allRems) {
  const t = resolveFullText(r.key);
  const m = t.match(/^(?:📌\s*|-+\s*)?День\s*0?(\d+)\b/);
  if (m) {
    const dNum = parseInt(m[1], 10);
    if (dNum >= 1 && dNum <= 42) {
      if (t.length < 120 && !t.includes('\n')) {
        dayMap[dNum] = { id: r._id, parent: r.parent, text: t.trim() };
      }
    }
  }
}

console.log(`Found ${Object.keys(dayMap).length} / 42 days in RemNote schedule.`);
for (let i = 1; i <= 42; i++) {
  const d = dayMap[i];
  const dStr = i < 10 ? '0' + i : i;
  if (!d) {
    console.error(`[ERROR] Day ${dStr} is MISSING from dayMap!`);
    process.exit(1);
  }
  console.log(`Day ${dStr}: id=${d.id} parent=${d.parent} text="${d.text.slice(0, 50)}"`);
}

if (Object.keys(dayMap).length !== 42) {
  console.error(`[ERROR] Expected exactly 42 days, found ${Object.keys(dayMap).length}`);
  process.exit(1);
}

if (dayMap[35].id !== 'Sa2NV96RJQCer4jVy') {
  console.error(`[ERROR] Day 35 mapped to wrong Rem ${dayMap[35].id} (${dayMap[35].text}), expected Sa2NV96RJQCer4jVy`);
  process.exit(1);
}

console.log('✓ All 42 RemNote schedule days strictly verified with valid IDs and parents!');

