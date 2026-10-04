const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
const exactMap = JSON.parse(fs.readFileSync('exact_42_days_map.json', 'utf8'));

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

[1, 2, 6, 7, 22, 42].forEach(dayNum => {
  const m = exactMap.find(x => x.dayNum === dayNum);
  console.log(`\n================== Day ${dayNum} ==================`);
  console.log(`Theory [${m.theoryId}]:`);
  const tKids = allRems.filter(r => r.parent === m.theoryId);
  tKids.forEach(k => console.log(`  - [${k.apu ? 'TODO' : ' '}] ${resolveFullText(k.key)}`));
  
  console.log(`Coding [${m.codingId}]:`);
  const cKids = allRems.filter(r => r.parent === m.codingId);
  cKids.forEach(k => console.log(`  - [${k.apu ? 'TODO' : ' '}] ${resolveFullText(k.key)}`));
  
  if (m.checklistId) {
    console.log(`Checklist [${m.checklistId}]:`);
    const chKids = allRems.filter(r => r.parent === m.checklistId);
    chKids.forEach(k => console.log(`  - [${k.apu ? 'TODO' : ' '}] ${resolveFullText(k.key)}`));
  }
});
