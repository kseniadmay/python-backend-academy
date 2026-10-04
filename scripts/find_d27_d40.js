const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
const sched = JSON.parse(fs.readFileSync('parsed_schedule.json', 'utf8'));

const remById = new Map();
const childrenByParent = new Map();
allRems.forEach(r => {
  remById.set(r._id, r);
  if (r.parent) {
    if (!childrenByParent.has(r.parent)) childrenByParent.set(r.parent, []);
    childrenByParent.get(r.parent).push(r);
  }
});

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
          const target = remById.get(part._id);
          if (target) return resolveFullText(target.key, depth + 1);
        }
      }
      return '';
    }).join('');
  }
  return '';
}

function norm(s) {
  return (s || '').toLowerCase().replace(/[^a-zа-яё0-9]/gi, ' ').replace(/\s+/g, ' ').trim();
}

[27, 40].forEach(dayNum => {
  let sDay = null;
  sched.weeks.forEach(w => w.days.forEach(d => { if (d.num === dayNum) sDay = d; }));
  const tSec = sDay.sections.find(s => s.type === 'theory');
  const expItems = tSec ? tSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  
  console.log(`\n=== Day ${dayNum} expected theory (${expItems.length}) ===`);
  expItems.forEach(it => console.log('  exp:', it));
  
  // Find all parents with kids matching any expItems, excluding 0QFP2VCcxja5X9WWU
  const matches = [];
  for (const [pId, kids] of childrenByParent.entries()) {
    if (pId === '0QFP2VCcxja5X9WWU' || pId === 'GwREY4bq5eQvPyeAB') continue;
    const pRem = remById.get(pId);
    if (!pRem) continue;
    const pText = resolveFullText(pRem.key);
    
    let matchCount = 0;
    const kidTexts = kids.map(k => norm(resolveFullText(k.key)));
    for (const exp of expItems) {
      if (kidTexts.some(kt => kt.includes(exp.slice(0, 20)) || exp.includes(kt.slice(0, 20)))) {
        matchCount++;
      }
    }
    if (matchCount > 0) {
      matches.push({ id: pId, text: pText, parent: pRem.parent, matchCount, kidsCount: kids.length });
    }
  }
  console.log(`Candidate sections for Day ${dayNum}:`);
  matches.sort((a,b) => b.matchCount - a.matchCount).forEach(m => {
    console.log(`  id=${m.id} matches=${m.matchCount} kids=${m.kidsCount} parent=${m.parent} text="${m.text.slice(0, 50)}"`);
  });
});
