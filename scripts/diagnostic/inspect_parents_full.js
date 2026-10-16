const fs = require('fs');
const audit = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parents_audit.json', 'utf8'));
const parsed = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));
const daysMap = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\days_map.json', 'utf8'));

console.log('Task parents count:', audit.tasksParentCount);
console.log('Theory parents count:', audit.theoryParentCount);

// Let's inspect each task parent in audit.taskParents
const taskParentsList = Object.values(audit.taskParents);
const theoryParentsList = Object.values(audit.theoryParents);

console.log('\nTask Parents:');
taskParentsList.forEach(p => {
  console.log(`[${p.id}] parent=${p.parentOfParent} tasks=${p.tasksCount} text="${p.text.slice(0, 50)}"`);
});

console.log('\nTheory Parents:');
theoryParentsList.forEach(p => {
  console.log(`[${p.id}] parent=${p.parentOfParent} theories=${p.theoriesCount} text="${p.text.slice(0, 50)}"`);
});