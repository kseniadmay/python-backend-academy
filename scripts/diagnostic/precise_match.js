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

const theories = [];
const codings = [];
const checklists = [];
const standouts = [];

allRems.forEach(r => {
  const t = resolveFullText(r.key).trim();
  const kids = childrenByParent.get(r._id) || [];
  const kidsTexts = kids.map(k => norm(resolveFullText(k.key))).filter(x => x.length > 5);
  
  const obj = { id: r._id, parent: r.parent, text: t, kidsCount: kids.length, kidsTexts };
  
  if (t.startsWith('Теория') || t.startsWith('🌅') || t.includes('Теория дня')) theories.push(obj);
  if (t.startsWith('Кодинг') || t.startsWith('💻') || t.startsWith('Вечерний')) codings.push(obj);
  if (t.includes('Чек-лист') || t.startsWith('✅')) checklists.push(obj);
  if (t.includes('Стенд-аут') || t.startsWith('🎯')) standouts.push(obj);
});

console.log(`Candidates: Theories=${theories.length}, Codings=${codings.length}, Checklists=${checklists.length}, Standouts=${standouts.length}`);

// Schedule map
const schedDays = new Map();
sched.weeks.forEach(w => {
  w.days.forEach(d => {
    const tSec = d.sections.find(s => s.type === 'theory');
    const cSec = d.sections.find(s => s.type === 'coding');
    const chSec = d.sections.find(s => s.type === 'checklist');
    const stSec = d.sections.find(s => s.type === 'standout');
    
    schedDays.set(d.num, {
      num: d.num,
      rawTitle: d.rawTitle,
      theory: tSec ? tSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [],
      coding: cSec ? cSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [],
      checklist: chSec ? chSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : [],
      standout: stSec ? stSec.items.map(it => norm(it.replace(/^-\s*(\[\s*\]\s*)?/, ''))).filter(x => x.length > 5) : []
    });
  });
});

function scoreMatch(candidateKids, expectedItems) {
  if (expectedItems.length === 0 || candidateKids.length === 0) return 0;
  let matches = 0;
  for (const exp of expectedItems) {
    const expSub = exp.slice(0, 20);
    for (const cand of candidateKids) {
      if (cand.includes(expSub) || exp.includes(cand.slice(0, 20))) {
        matches++;
        break;
      }
    }
  }
  return matches;
}

const dayResults = [];
for (let d = 1; d <= 42; d++) {
  const sDay = schedDays.get(d);
  
  // Best Theory
  let bestT = null;
  theories.forEach(cand => {
    const m = scoreMatch(cand.kidsTexts, sDay.theory);
    if (m > 0 && (!bestT || m > bestT.matches || (m === bestT.matches && cand.kidsCount === sDay.theory.length))) {
      bestT = { id: cand.id, text: cand.text, parent: cand.parent, matches: m, expected: sDay.theory.length, kidsCount: cand.kidsCount };
    }
  });
  
  // Best Coding
  let bestC = null;
  codings.forEach(cand => {
    const m = scoreMatch(cand.kidsTexts, sDay.coding);
    if (m > 0 && (!bestC || m > bestC.matches || (m === bestC.matches && Math.abs(cand.kidsCount - sDay.coding.length) < Math.abs(bestC.kidsCount - sDay.coding.length)))) {
      bestC = { id: cand.id, text: cand.text, parent: cand.parent, matches: m, expected: sDay.coding.length, kidsCount: cand.kidsCount };
    }
  });
  
  // Best Checklist
  let bestCh = null;
  if (sDay.checklist.length > 0) {
    checklists.forEach(cand => {
      const m = scoreMatch(cand.kidsTexts, sDay.checklist);
      if (m > 0 && (!bestCh || m > bestCh.matches || (m === bestCh.matches && cand.kidsCount === sDay.checklist.length))) {
        bestCh = { id: cand.id, text: cand.text, parent: cand.parent, matches: m, expected: sDay.checklist.length, kidsCount: cand.kidsCount };
      }
    });
  }
  
  // Best Standout
  let bestSt = null;
  if (sDay.standout.length > 0) {
    standouts.forEach(cand => {
      const m = scoreMatch(cand.kidsTexts, sDay.standout);
      if (m > 0 && (!bestSt || m > bestSt.matches)) {
        bestSt = { id: cand.id, text: cand.text, parent: cand.parent, matches: m, expected: sDay.standout.length, kidsCount: cand.kidsCount };
      }
    });
  }
  
  dayResults.push({
    day: d,
    title: sDay.rawTitle,
    theory: bestT,
    coding: bestC,
    checklist: bestCh,
    standout: bestSt
  });
}

fs.writeFileSync('precise_match_results.json', JSON.stringify(dayResults, null, 2), 'utf8');

let fullyMatched = 0;
dayResults.forEach(r => {
  const tOk = r.theory && r.theory.matches === r.theory.expected;
  const cOk = r.coding && r.coding.matches >= Math.min(3, r.coding.expected);
  if (tOk && cOk) fullyMatched++;
  
  const tStr = r.theory ? `${r.theory.id} (${r.theory.matches}/${r.theory.expected})` : 'MISSING';
  const cStr = r.coding ? `${r.coding.id} (${r.coding.matches}/${r.coding.expected}, kids=${r.coding.kidsCount})` : 'MISSING';
  const chStr = r.checklist ? ` | Ch: ${r.checklist.id} (${r.checklist.matches}/${r.checklist.expected})` : '';
  const stStr = r.standout ? ` | St: ${r.standout.id} (${r.standout.matches}/${r.standout.expected})` : '';
  console.log(`Day ${r.day < 10 ? '0' + r.day : r.day}: T=${tStr} | C=${cStr}${chStr}${stStr}`);
});

console.log(`\nFully matched days: ${fullyMatched}/42`);
