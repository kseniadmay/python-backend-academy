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

// 42 Day rems
const rootId = 'GwREY4bq5eQvPyeAB';
const rootKids = childrenByParent.get(rootId) || [];
const weekRems = [];
for (const r of rootKids) {
  const t = resolveFullText(r.key);
  const wm = t.match(/Неделя\s*(\d+)/);
  if (wm) weekRems.push({ num: parseInt(wm[1]), id: r._id, text: t });
}
weekRems.sort((a,b) => a.num - b.num);

const dayRems = [];
weekRems.forEach(w => {
  const kids = (childrenByParent.get(w.id) || []).filter(k => {
    const t = resolveFullText(k.key);
    return t.includes('День') || t.includes('REVIEW') || t.includes('CAPSTONE');
  });
  kids.forEach((d, idx) => {
    dayRems.push({
      dayNum: (w.num - 1) * 7 + idx + 1,
      weekNum: w.num,
      dayId: d._id,
      text: resolveFullText(d.key)
    });
  });
});

// Candidate sections:
// Filter out multi-line glue rems (length > 120 or containing multiple \n or containing "День")
function isCandidateSection(r, type) {
  const t = resolveFullText(r.key).trim();
  if (t.length > 130) return false;
  if (t.includes('\n')) return false;
  if (t.includes('Неделя') && !t.includes('Чек-лист') && !t.includes('REVIEW')) return false;
  
  if (type === 'theory') {
    return t.startsWith('Теория') || t.startsWith('🌅') || t.includes('Закрепление сложных карточек') || t.includes('Теория дня');
  }
  if (type === 'coding') {
    return t.startsWith('Кодинг') || t.startsWith('💻') || t.startsWith('Вечерний кодинг');
  }
  if (type === 'checklist') {
    return t.includes('Чек-лист') || t.startsWith('✅');
  }
  if (type === 'standout') {
    return t.includes('Стенд-аут') || t.startsWith('🎯');
  }
  return false;
}

const candidateTheories = allRems.filter(r => isCandidateSection(r, 'theory')).map(r => ({
  id: r._id,
  text: resolveFullText(r.key).trim(),
  kids: (childrenByParent.get(r._id) || []).map(k => norm(resolveFullText(k.key))).filter(x => x.length > 5)
}));

const candidateCodings = allRems.filter(r => isCandidateSection(r, 'coding')).map(r => ({
  id: r._id,
  text: resolveFullText(r.key).trim(),
  kids: (childrenByParent.get(r._id) || []).map(k => norm(resolveFullText(k.key))).filter(x => x.length > 5)
}));

const candidateChecklists = allRems.filter(r => isCandidateSection(r, 'checklist')).map(r => ({
  id: r._id,
  text: resolveFullText(r.key).trim(),
  kids: (childrenByParent.get(r._id) || []).map(k => norm(resolveFullText(k.key))).filter(x => x.length > 5)
}));

const candidateStandouts = allRems.filter(r => isCandidateSection(r, 'standout')).map(r => ({
  id: r._id,
  text: resolveFullText(r.key).trim(),
  kids: (childrenByParent.get(r._id) || []).map(k => norm(resolveFullText(k.key))).filter(x => x.length > 5)
}));

console.log(`Clean candidates: Theories=${candidateTheories.length}, Codings=${candidateCodings.length}, Checklists=${candidateChecklists.length}, Standouts=${candidateStandouts.length}`);

// Schedule days
const schedDays = new Map();
sched.weeks.forEach(w => {
  w.days.forEach(d => {
    const tSec = d.sections.find(s => s.type === 'theory');
    const cSec = d.sections.find(s => s.type === 'coding');
    const chSec = d.sections.find(s => s.type === 'checklist');
    const stSec = d.sections.find(s => s.type === 'standout');
    
    schedDays.set(d.num, {
      num: d.num,
      theory: tSec ? tSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [],
      coding: cSec ? cSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [],
      checklist: chSec ? chSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [],
      standout: stSec ? stSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : []
    });
  });
});

function matchScore(candKids, expItems) {
  if (candKids.length === 0 || expItems.length === 0) return 0;
  let matches = 0;
  for (const exp of expItems) {
    const eSub = exp.slice(0, 20);
    for (const ck of candKids) {
      if (ck.includes(eSub) || exp.includes(ck.slice(0, 20))) {
        matches++;
        break;
      }
    }
  }
  return matches;
}

// Find optimal 1-to-1 matching for all 42 days!
const assignment = [];
const usedTheories = new Set();
const usedCodings = new Set();

for (let d = 1; d <= 42; d++) {
  const sDay = schedDays.get(d);
  const dRem = dayRems.find(r => r.dayNum === d);
  
  // Find best theory
  let bestT = null;
  for (const cand of candidateTheories) {
    const m = matchScore(cand.kids, sDay.theory);
    if (m > 0 && (!bestT || m > bestT.score || (m === bestT.score && Math.abs(cand.kids.length - sDay.theory.length) < Math.abs(bestT.cand.kids.length - sDay.theory.length)))) {
      bestT = { cand, score: m };
    }
  }
  
  // Find best coding
  let bestC = null;
  for (const cand of candidateCodings) {
    const m = matchScore(cand.kids, sDay.coding);
    if (m > 0 && (!bestC || m > bestC.score || (m === bestC.score && Math.abs(cand.kids.length - sDay.coding.length) < Math.abs(bestC.cand.kids.length - sDay.coding.length)))) {
      bestC = { cand, score: m };
    }
  }
  
  // Best checklist
  let bestCh = null;
  if (sDay.checklist.length > 0) {
    for (const cand of candidateChecklists) {
      const m = matchScore(cand.kids, sDay.checklist);
      if (m > 0 && (!bestCh || m > bestCh.score)) {
        bestCh = { cand, score: m };
      }
    }
  }
  
  // Best standout
  let bestSt = null;
  if (sDay.standout.length > 0) {
    for (const cand of candidateStandouts) {
      const m = matchScore(cand.kids, sDay.standout);
      if (m > 0 && (!bestSt || m > bestSt.score)) {
        bestSt = { cand, score: m };
      }
    }
  }
  
  assignment.push({
    dayNum: d,
    weekNum: Math.ceil(d / 7),
    dayId: dRem ? dRem.dayId : null,
    theory: bestT ? { id: bestT.cand.id, text: bestT.cand.text, matches: bestT.score, expected: sDay.theory.length, count: bestT.cand.kids.length } : null,
    coding: bestC ? { id: bestC.cand.id, text: bestC.cand.text, matches: bestC.score, expected: sDay.coding.length, count: bestC.cand.kids.length } : null,
    checklist: bestCh ? { id: bestCh.cand.id, text: bestCh.cand.text, matches: bestCh.score, expected: sDay.checklist.length, count: bestCh.cand.kids.length } : null,
    standout: bestSt ? { id: bestSt.cand.id, text: bestSt.cand.text, matches: bestSt.score, expected: sDay.standout.length, count: bestSt.cand.kids.length } : null
  });
}

fs.writeFileSync('clean_assignment.json', JSON.stringify(assignment, null, 2), 'utf8');

assignment.forEach(a => {
  const tStr = a.theory ? `${a.theory.id} (${a.theory.matches}/${a.theory.expected})` : 'MISSING';
  const cStr = a.coding ? `${a.coding.id} (${a.coding.matches}/${a.coding.expected})` : 'MISSING';
  const chStr = a.checklist ? ` | Ch: ${a.checklist.id} (${a.checklist.matches}/${a.checklist.expected})` : '';
  const stStr = a.standout ? ` | St: ${a.standout.id} (${a.standout.matches}/${a.standout.expected})` : '';
  console.log(`Day ${a.dayNum < 10 ? '0' + a.dayNum : a.dayNum}: T=${tStr} | C=${cStr}${chStr}${stStr}`);
});
