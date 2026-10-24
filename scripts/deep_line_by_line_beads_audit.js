const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const academyPath = path.resolve(__dirname, '..', 'academy.html');
const text = fs.readFileSync(academyPath, 'utf-8');

console.log('========================================================================');
console.log('   DEEP LINE-BY-LINE BEADS AUDIT (ECHELON 1 & ECHELON 2)                ');
console.log('========================================================================\n');

// 1. Extract CANONICAL_NOTE_DECKS_MAP
const mMap = text.match(/const CANONICAL_NOTE_DECKS_MAP\s*=\s*({[\s\S]*?});/);
assert(mMap, 'CANONICAL_NOTE_DECKS_MAP missing from academy.html');
const sandbox = {};
vm.runInNewContext('map = ' + mMap[1], sandbox);
const canonicalMap = sandbox.map;
console.log(`✓ CANONICAL_NOTE_DECKS_MAP: loaded ${Object.keys(canonicalMap).length} entries.`);

// 2. Extract Masteries
function extractMastery(name) {
  const regex = new RegExp(`const ${name}\\s*=\\s*({[\\s\\S]*?});\\s*(?:const|let|var|function)`, 'm');
  const m = text.match(regex);
  assert(m, `${name} missing from academy.html`);
  return JSON.parse(m[1]);
}

const masteries = {
  PY: extractMastery('PY_MASTERY'),
  WEB: extractMastery('WEB_MASTERY'),
  BACKEND: extractMastery('BACKEND_MASTERY'),
  ALGO: extractMastery('ALGO_MASTERY'),
  DB: extractMastery('DB_MASTERY'),
  INFRA: extractMastery('INFRA_MASTERY')
};

const allNotes = {};
const allDecks = {};
const allUnits = [];
const allUnitTests = {};

Object.values(masteries).forEach(m => {
  if (m.notes) Object.assign(allNotes, m.notes);
  if (m.decks) Object.assign(allDecks, m.decks);
  if (m.units) allUnits.push(...m.units);
  if (m.unitTests) Object.assign(allUnitTests, m.unitTests);
});

console.log(`✓ Loaded ${Object.keys(allNotes).length} notes, ${Object.keys(allDecks).length} decks, ${allUnits.length} units, ${Object.keys(allUnitTests).length} unit tests.`);

// Extract IDE_TASKS_BY_ID or tasks
let ideTasks = {};
const mTasks = text.match(/const IDE_TASKS_BY_ID\s*=\s*({[\s\S]*?});/);
if (mTasks) {
  try {
    const sBox = {};
    vm.runInNewContext('tasks = ' + mTasks[1], sBox);
    ideTasks = sBox.tasks;
    console.log(`✓ IDE_TASKS_BY_ID: loaded ${Object.keys(ideTasks).length} tasks.`);
  } catch(e) {
    console.log(`Warning parsing IDE_TASKS_BY_ID: ${e.message}`);
  }
}

// Units definitions
const echelon1Units = ['1.1', '1.2', '1.3', '1.4', '1.9', '2.1', '2.2', '2.3', '4.1', '4.2', '5.1', '5.2', '5.3', '5.4'];
const echelon2Units = ['1.5', '1.6', '1.7', '1.8', '2.1', '2.4', '3.1', '3.2', '3.3', '3.5', '3.6', '4.3', '4.6', '5.4', '5.5', '7.2', '7.6'];

function auditDetailedEchelon(echelonNum, unitIds) {
  console.log(`\n========================================================================`);
  console.log(`   AUDITING ECHELON ${echelonNum} (${unitIds.length} UNITS) LINE BY LINE`);
  console.log(`========================================================================`);

  let totalSkills = 0;
  let totalNotes = 0;
  let totalDecks = 0;
  let totalTasks = 0;
  let totalExams = 0;
  let issues = [];

  for (const uid of unitIds) {
    const unit = allUnits.find(u => u.id === uid);
    if (!unit) {
      issues.push(`Unit ${uid} not found in allUnits`);
      continue;
    }

    const unitTest = allUnitTests[unit.id];
    const hasExam = unitTest && Array.isArray(unitTest.questions) && unitTest.questions.length > 0;
    if (hasExam) totalExams++;
    else issues.push(`Unit ${uid} has NO unitTest / exam questions!`);

    console.log(`\n------------------------------------------------------`);
    console.log(`[Unit ${unit.id}] ${unit.title} (Рубежный зачёт: ${hasExam ? unitTest.questions.length : 0} вопросов)`);
    console.log(`------------------------------------------------------`);

    for (const skill of unit.skills) {
      totalSkills++;
      const kIds = skill.kIds || [];
      const fIds = skill.fIds || [];
      const tIds = skill.taskIds || [];

      totalNotes += kIds.length;
      totalDecks += fIds.length;
      totalTasks += tIds.length;

      // 1. Check fIds === decks
      if (!Array.isArray(skill.decks) || JSON.stringify(skill.fIds) !== JSON.stringify(skill.decks)) {
        issues.push(`Skill ${skill.id}: fIds and decks arrays mismatch!`);
      }

      // 2. Check each note exists and has steps
      kIds.forEach(kid => {
        const n = allNotes[kid];
        if (!n) issues.push(`Skill ${skill.id}: Note ${kid} missing from allNotes!`);
        else if (!Array.isArray(n.steps) || n.steps.length === 0) {
          issues.push(`Skill ${skill.id}: Note ${kid} has no steps!`);
        }
      });

      // 3. Check each deck exists and has cards
      fIds.forEach(fid => {
        const d = allDecks[fid];
        if (!d) issues.push(`Skill ${skill.id}: Deck ${fid} missing from allDecks!`);
        else if (!Array.isArray(d.cards) || d.cards.length === 0) {
          issues.push(`Skill ${skill.id}: Deck ${fid} has no cards!`);
        }
      });

      // 4. Check each task exists
      tIds.forEach(tid => {
        if (Object.keys(ideTasks).length > 0 && !ideTasks[tid]) {
          issues.push(`Skill ${skill.id}: Task ID ${tid} missing from IDE_TASKS_BY_ID!`);
        }
      });

      // 5. Check pairwise beads sequence: Note -> Decks
      const coveredFids = new Set();
      console.log(`  🔹 Skill [${skill.id}] ${skill.title}:`);

      kIds.forEach((kid, kIdx) => {
        const n = allNotes[kid] || {};
        const matchedFids = (canonicalMap[kid] || []).filter(f => fIds.includes(f));
        if (matchedFids.length === 0) {
          issues.push(`Skill ${skill.id}: Note ${kid} has NO matching decks in skill.fIds!`);
        }
        matchedFids.forEach(f => coveredFids.add(f));

        const deckListStr = matchedFids.map(f => {
          const d = allDecks[f] || {};
          return `📇 [${f}] "${d.title}" (${d.cards ? d.cards.length : 0} карт)`;
        }).join(' + ');

        console.log(`     [Бусина теории ${kIdx+1}] 🟢 [${kid}] "${n.title}" (${n.steps ? n.steps.length : 0} шагов)`);
        console.log(`        └─► [Бусина карточек] ${deckListStr || '⚠️ НЕТ КОЛОДЫ'}`);
      });

      // 6. Check orphan decks (decks in fIds not mapped to any note in this skill)
      const orphanFids = fIds.filter(f => !coveredFids.has(f));
      if (orphanFids.length > 0) {
        issues.push(`Skill ${skill.id}: Orphan decks found: ${JSON.stringify(orphanFids)}`);
        console.log(`     ⚠️ СИРОТСКИЕ КОЛОДЫ: ${JSON.stringify(orphanFids)}`);
      }

      // 7. Check IDE task beads
      console.log(`     [Бусины практики IDE: ${tIds.length}] Задачи: ${tIds.join(', ')}`);
    }
    console.log(`  🎓 [Рубежная бусина] Зачёт по юниту ${unit.id}: "${unitTest ? unitTest.title : ''}" (${hasExam ? unitTest.questions.length : 0} вопросов)`);
  }

  console.log(`\n========================================================================`);
  console.log(`ECHELON ${echelonNum} STATS:`);
  console.log(`  Units: ${unitIds.length}, Skills: ${totalSkills}, Notes: ${totalNotes}, Decks: ${totalDecks}, Tasks: ${totalTasks}, Unit Tests: ${totalExams}`);
  console.log(`  Total issues found: ${issues.length}`);
  if (issues.length > 0) {
    console.log(`  ISSUES:`);
    issues.forEach((iss, i) => console.log(`    ${i+1}. ${iss}`));
  } else {
    console.log(`  🟢 100% PERFECT: 0 ISSUES, 0 MISMATCHES, 0 ORPHANS!`);
  }
  console.log(`========================================================================\n`);
  return issues;
}

const issuesE1 = auditDetailedEchelon(1, echelon1Units);
const issuesE2 = auditDetailedEchelon(2, echelon2Units);

assert.strictEqual(issuesE1.length, 0, `Echelon 1 has ${issuesE1.length} issues!`);
assert.strictEqual(issuesE2.length, 0, `Echelon 2 has ${issuesE2.length} issues!`);
console.log('🏆 LINE-BY-LINE AUDIT COMPLETE: BOTH ECHELONS ARE 100% PERFECT!');
