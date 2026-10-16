const fs = require('fs');
const audit = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parents_audit.json', 'utf8'));
console.log('Task parent sections:', audit.tasksParentCount);
console.log('Theory parent sections:', audit.theoryParentCount);
console.log('\nTask Parents Sample:');
Object.values(audit.taskParents).slice(0, 15).forEach(p => {
  console.log(`  [${p.id}] parentOfParent=${p.parentOfParent} tasks=${p.tasksCount} text="${p.text.slice(0, 50)}"`);
});
console.log('\nTheory Parents Sample:');
Object.values(audit.theoryParents).slice(0, 15).forEach(p => {
  console.log(`  [${p.id}] parentOfParent=${p.parentOfParent} theories=${p.theoriesCount} text="${p.text.slice(0, 50)}"`);
});