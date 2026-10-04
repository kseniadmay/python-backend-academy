const fs = require('fs');

const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
const exactMap = JSON.parse(fs.readFileSync('exact_42_days_map.json', 'utf8'));

const remById = new Map();
const childrenByParent = new Map();
allRems.forEach(r => {
  remById.set(r._id, r);
  if (r.parent) {
    if (!childrenByParent.has(r.parent)) childrenByParent.set(r.parent, []);
    childrenByParent.get(r.parent).push(r);
  }
});

const dayIds = new Set(exactMap.map(m => m.dayId));
const validChildIds = new Set();
exactMap.forEach(m => {
  if (m.theoryId) validChildIds.add(m.theoryId);
  if (m.codingId) validChildIds.add(m.codingId);
  if (m.checklistId) validChildIds.add(m.checklistId);
  if (m.standoutId) validChildIds.add(m.standoutId);
});

// Identify all rems currently parented to any day
const strayRems = [];
for (const dayId of dayIds) {
  const curKids = childrenByParent.get(dayId) || [];
  for (const k of curKids) {
    if (!validChildIds.has(k._id)) {
      strayRems.push(k);
    }
  }
}

console.log(`Total stray rems currently under days: ${strayRems.length}`);

// Categorize stray rems
const kbDocs = [];
const regularStrays = [];

for (const r of strayRems) {
  if (r.type === 1 || r._id === 'CXxvzLVYN33te4fvq') {
    kbDocs.push(r);
  } else {
    regularStrays.push(r);
  }
}

console.log(`KB Documents mistakenly under days: ${kbDocs.length}`);
console.log(`Duplicate/orphan sections under days: ${regularStrays.length}`);

console.log('\nSample KB docs to restore to root/theory:');
kbDocs.forEach(d => {
  console.log(`  - [${d._id}] type=${d.type}`);
});

console.log('\nSimulation summary:');
console.log(`- 42 Days will each have 2 children (Theory, Coding), review days will have 3-4.`);
console.log(`- ${kbDocs.length} KB documents will be restored.`);
console.log(`- ${regularStrays.length} orphan/duplicate sections will be detached from days.`);
