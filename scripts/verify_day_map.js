const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

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
  const m = t.match(/День\s*0?(\d+)/);
  if (m) {
    const dNum = parseInt(m[1]);
    if (dNum >= 1 && dNum <= 42) {
      if (t.length < 120 && !t.includes('\n')) {
        dayMap[dNum] = { id: r._id, parent: r.parent, text: t.trim() };
      }
    }
  }
}

for (let i = 1; i <= 42; i++) {
  const d = dayMap[i];
  const dStr = i < 10 ? '0' + i : i;
  console.log(`Day ${dStr}: id=${d ? d.id : 'MISSING'} text="${d ? d.text.slice(0, 50) : ''}"`);
}
