const fs = require('fs');
const assign = JSON.parse(fs.readFileSync('clean_assignment.json', 'utf8'));

console.log('Day | DayId | TheoryId | CodingId | ChecklistId | StandoutId');
assign.forEach(a => {
  const dStr = a.dayNum < 10 ? '0' + a.dayNum : a.dayNum;
  const t = a.theory ? a.theory.id : 'NONE';
  const c = a.coding ? a.coding.id : 'NONE';
  const ch = a.checklist ? a.checklist.id : '-';
  const st = a.standout ? a.standout.id : '-';
  console.log(`${dStr} | ${a.dayId} | ${t} | ${c} | ${ch} | ${st}`);
});
