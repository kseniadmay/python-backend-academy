const fs = require('fs');

const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
const sched = JSON.parse(fs.readFileSync('parsed_schedule.json', 'utf8'));

function extractText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(part => {
      if (typeof part === 'string') return part;
      if (part && typeof part === 'object') {
        return part.text || (part.textOfDeletedRem ? part.textOfDeletedRem.join(' ') : '');
      }
      return '';
    }).join('');
  }
  return '';
}

function norm(s) {
  return (s || '').toLowerCase().replace(/[^a-zа-яё0-9]/gi, ' ').replace(/\s+/g, ' ').trim();
}

// Map rems by id and parent
const remById = new Map();
const childrenByParent = new Map();
allRems.forEach(r => {
  remById.set(r._id, r);
  if (r.parent) {
    if (!childrenByParent.has(r.parent)) childrenByParent.set(r.parent, []);
    childrenByParent.get(r.parent).push(r);
  }
});

const rootId = 'GwREY4bq5eQvPyeAB';
const rootKids = childrenByParent.get(rootId) || [];

// Weeks
const weekMap = new Map(); // weekNum -> rem
for (const r of rootKids) {
  const t = extractText(r.key);
  const wm = t.match(/Неделя\s*(\d+)/);
  if (wm) {
    const wNum = parseInt(wm[1]);
    weekMap.set(wNum, r);
  }
}

// Days
const dayMap = new Map(); // dayNum -> rem
for (let wNum = 1; wNum <= 6; wNum++) {
  const wRem = weekMap.get(wNum);
  if (!wRem) continue;
  const wKids = childrenByParent.get(wRem._id) || [];
  for (const dRem of wKids) {
    const t = extractText(dRem.key);
    const dm = t.match(/День\s*0?(\d+)/);
    if (dm) {
      const dNum = parseInt(dm[1]);
      dayMap.set(dNum, dRem);
    }
  }
}

console.log(`Weeks identified: ${weekMap.size}/6`);
console.log(`Days identified: ${dayMap.size}/42`);

// Schedule days
const schedDays = new Map();
sched.weeks.forEach(w => {
  w.days.forEach(d => {
    schedDays.set(d.num, d);
  });
});

// Candidate sections in DB
// We want to match sections whose children match day items
const report = [];

for (let d = 1; d <= 42; d++) {
  const sDay = schedDays.get(d);
  const dRem = dayMap.get(d);
  if (!sDay || !dRem) {
    console.log(`Day ${d} missing!`);
    continue;
  }
  
  const curKids = childrenByParent.get(dRem._id) || [];
  
  // Schedule sections
  const theorySec = sDay.sections.find(s => s.type === 'theory');
  const codingSec = sDay.sections.find(s => s.type === 'coding');
  const standoutSec = sDay.sections.find(s => s.type === 'standout');
  const checkSec = sDay.sections.find(s => s.type === 'checklist');
  
  const tItems = theorySec ? theorySec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  const cItems = codingSec ? codingSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  const sItems = standoutSec ? standoutSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  const chItems = checkSec ? checkSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  
  // Find matching sections among ALL rems in DB
  function findBestSection(expectedItems, typeName) {
    if (expectedItems.length === 0) return null;
    let best = null;
    let maxMatches = 0;
    
    // Check all parents with children
    for (const [pId, kids] of childrenByParent.entries()) {
      const pRem = remById.get(pId);
      if (!pRem) continue;
      const pText = extractText(pRem.key);
      
      // If it's a Week or Day or Root or Document, skip
      if (pId === rootId || weekMap.has(pId)) continue;
      
      let matches = 0;
      for (const k of kids) {
        const kt = norm(extractText(k.key));
        if (kt.length < 5) continue;
        if (expectedItems.some(it => it.includes(kt.slice(0, 20)) || kt.includes(it.slice(0, 20)))) {
          matches++;
        }
      }
      
      // Preference to current kids of dRem or rems whose title contains typeName
      let bonus = 0;
      if (pRem.parent === dRem._id) bonus += 0.5;
      if (typeName === 'theory' && (pText.includes('Теория') || pText.includes('🌅'))) bonus += 0.2;
      if (typeName === 'coding' && (pText.includes('Кодинг') || pText.includes('💻') || pText.includes('Вечерний'))) bonus += 0.2;
      if (typeName === 'checklist' && (pText.includes('Чек-лист') || pText.includes('✅'))) bonus += 0.2;
      if (typeName === 'standout' && (pText.includes('Стенд-аут') || pText.includes('🎯'))) bonus += 0.2;
      
      const totalScore = matches + bonus;
      if (matches >= Math.min(2, expectedItems.length) && (!best || totalScore > best.score)) {
        best = {
          id: pId,
          text: pText,
          parent: pRem.parent,
          score: totalScore,
          matches,
          kidsCount: kids.length,
          expectedCount: expectedItems.length
        };
      }
    }
    return best;
  }
  
  const bestT = findBestSection(tItems, 'theory');
  const bestC = findBestSection(cItems, 'coding');
  const bestS = findBestSection(sItems, 'standout');
  const bestCh = findBestSection(chItems, 'checklist');
  
  report.push({
    dayNum: d,
    dayId: dRem._id,
    dayText: extractText(dRem.key),
    curKidsCount: curKids.length,
    curKids: curKids.map(k => ({ id: k._id, text: extractText(k.key).slice(0, 40), subCount: (childrenByParent.get(k._id)||[]).length })),
    bestTheory: bestT,
    bestCoding: bestC,
    bestStandout: bestS,
    bestChecklist: bestCh
  });
}

fs.writeFileSync('day_sections_report.json', JSON.stringify(report, null, 2), 'utf8');
console.log('Saved day_sections_report.json');

let perfectDays = 0;
report.forEach(r => {
  const tOk = !r.bestTheory || r.bestTheory.matches > 0;
  const cOk = !r.bestCoding || r.bestCoding.matches > 0;
  if (tOk && cOk) perfectDays++;
  console.log(`Day ${r.dayNum}: T=${r.bestTheory ? r.bestTheory.id + ' (' + r.bestTheory.matches + '/' + r.bestTheory.expectedCount + ')' : 'NONE'} | C=${r.bestCoding ? r.bestCoding.id + ' (' + r.bestCoding.matches + '/' + r.bestCoding.expectedCount + ')' : 'NONE'} | CurKids=${r.curKidsCount}`);
});
console.log(`Matched days: ${perfectDays}/42`);
