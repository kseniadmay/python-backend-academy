const fs = require('fs');

const exactMap = JSON.parse(fs.readFileSync('exact_42_days_map.json', 'utf8'));
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

const childrenByParent = new Map();
allRems.forEach(r => {
  if (r.parent) {
    if (!childrenByParent.has(r.parent)) childrenByParent.set(r.parent, []);
    childrenByParent.get(r.parent).push(r);
  }
});

const sectionIds = new Set();
exactMap.forEach(m => {
  if (m.theoryId) sectionIds.add(m.theoryId);
  if (m.codingId) sectionIds.add(m.codingId);
  if (m.checklistId) sectionIds.add(m.checklistId);
});

const todoUpdates = [];
let alreadyTodo = 0;
let needsTodo = 0;

for (const secId of sectionIds) {
  const kids = childrenByParent.get(secId) || [];
  for (const k of kids) {
    // Check if it's a hint or note like "⏱️ Обязательно..."
    const kStr = JSON.stringify(k.key || '');
    if (kStr.includes('⏱️') || kStr.includes('Не обязательно')) continue;
    
    if (k.apu && k.apu.t && k.apu.t.v) {
      alreadyTodo++;
    } else {
      needsTodo++;
      todoUpdates.push({
        id: k._id,
        update: {
          $set: {
            apu: {
              t: { v: true, ',u': Date.now() },
              i: { v: false, ',u': Date.now() }
            }
          }
        }
      });
    }
  }
}

console.log(`Items in sections: Total=${alreadyTodo + needsTodo}, AlreadyTodo=${alreadyTodo}, NeedsTodo=${needsTodo}`);
fs.writeFileSync('all_todo_updates.json', JSON.stringify(todoUpdates, null, 2), 'utf8');
