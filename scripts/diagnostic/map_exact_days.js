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

// Map the 6 weeks from root GwREY4bq5eQvPyeAB
const rootId = 'GwREY4bq5eQvPyeAB';
const rootKids = childrenByParent.get(rootId) || [];
const weekRems = [];
for (const r of rootKids) {
  const t = resolveFullText(r.key);
  const wm = t.match(/Неделя\s*(\d+)/);
  if (wm) {
    weekRems.push({ num: parseInt(wm[1]), id: r._id, text: t });
  }
}
weekRems.sort((a,b) => a.num - b.num);

// Map the 42 days under each week
const dayRems = [];
weekRems.forEach(w => {
  const kids = (childrenByParent.get(w.id) || []).filter(k => {
    const t = resolveFullText(k.key);
    return t.includes('День') || t.includes('REVIEW');
  });
  kids.forEach((d, idx) => {
    dayRems.push({
      dayNum: (w.num - 1) * 7 + idx + 1,
      weekNum: w.num,
      dayId: d._id,
      text: resolveFullText(d.key),
      kids: childrenByParent.get(d._id) || []
    });
  });
});

console.log(`Total Day Rems in Weeks: ${dayRems.length}`);

// For each Day, find the clean sections:
// 1. Theory
// 2. Coding
// 3. (If Review day) Checklist & Standout
const dayPlans = [];

for (const d of dayRems) {
  let sDay = null;
  sched.weeks.forEach(w => w.days.forEach(sd => { if (sd.num === d.dayNum) sDay = sd; }));
  
  const expTheory = sDay.sections.find(s => s.type === 'theory');
  const expCoding = sDay.sections.find(s => s.type === 'coding');
  const expChecklist = sDay.sections.find(s => s.type === 'checklist');
  const expStandout = sDay.sections.find(s => s.type === 'standout');
  
  const tItems = expTheory ? expTheory.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  const cItems = expCoding ? expCoding.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  const chItems = expChecklist ? expChecklist.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  const stItems = expStandout ? expStandout.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [];
  
  function findBestMatch(exp, typeFilter) {
    if (exp.length === 0) return null;
    let best = null;
    for (const [pId, kids] of childrenByParent.entries()) {
      if (pId === rootId || pId === '0QFP2VCcxja5X9WWU' || pId === 'CXxvzLVYN33te4fvq') continue;
      const pRem = remById.get(pId);
      if (!pRem) continue;
      const pText = resolveFullText(pRem.key);
      
      // typeFilter
      if (typeFilter === 'theory' && !pText.includes('Теория') && !pText.includes('🌅') && !pText.includes('Закрепление')) continue;
      if (typeFilter === 'coding' && !pText.includes('Кодинг') && !pText.includes('💻') && !pText.includes('Вечерний')) continue;
      if (typeFilter === 'checklist' && !pText.includes('Чек-лист') && !pText.includes('✅')) continue;
      if (typeFilter === 'standout' && !pText.includes('Стенд-аут') && !pText.includes('🎯')) continue;
      
      const kidTexts = kids.map(k => norm(resolveFullText(k.key)));
      let matches = 0;
      for (const e of exp) {
        const eSub = e.slice(0, 20);
        if (kidTexts.some(kt => kt.includes(eSub) || e.includes(kt.slice(0, 20)))) matches++;
      }
      
      if (matches > 0 && (!best || matches > best.matches || (matches === best.matches && pRem.parent === d.dayId))) {
        best = { id: pId, text: pText, parent: pRem.parent, matches, expected: exp.length, kidsCount: kids.length };
      }
    }
    return best;
  }
  
  const bestT = findBestMatch(tItems, 'theory');
  const bestC = findBestMatch(cItems, 'coding');
  const bestCh = findBestMatch(chItems, 'checklist');
  const bestSt = findBestMatch(stItems, 'standout');
  
  dayPlans.push({
    dayNum: d.dayNum,
    weekNum: d.weekNum,
    dayId: d.dayId,
    dayText: d.text.slice(0, 50),
    currentKids: d.kids.map(k => ({ id: k._id, text: resolveFullText(k.key).slice(0, 40), kidsCount: (childrenByParent.get(k._id)||[]).length })),
    bestTheory: bestT,
    bestCoding: bestC,
    bestChecklist: bestCh,
    bestStandout: bestSt
  });
}

fs.writeFileSync('day_clean_plans.json', JSON.stringify(dayPlans, null, 2), 'utf8');

dayPlans.forEach(p => {
  const tOk = p.bestTheory ? `T:${p.bestTheory.id}(${p.bestTheory.matches}/${p.bestTheory.expected})` : 'T:NONE';
  const cOk = p.bestCoding ? `C:${p.bestCoding.id}(${p.bestCoding.matches}/${p.bestCoding.expected})` : 'C:NONE';
  const chOk = p.bestChecklist ? `Ch:${p.bestChecklist.id}(${p.bestChecklist.matches}/${p.bestChecklist.expected})` : '';
  const curCount = p.currentKids.length;
  console.log(`Day ${p.dayNum < 10 ? '0' + p.dayNum : p.dayNum}: ${tOk} | ${cOk} | ${chOk} | curKids=${curCount}`);
});
