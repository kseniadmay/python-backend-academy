const fs = require('fs');
const sched = JSON.parse(fs.readFileSync('parsed_schedule.json', 'utf8'));

console.log('Total weeks:', sched.weeks.length);
let totalDays = 0;
sched.weeks.forEach(w => {
  console.log(`\nWeek ${w.num}: ${w.title} (${w.days.length} days)`);
  w.days.forEach(d => {
    totalDays++;
    const secSummary = d.sections.map(s => `${s.type} (${s.items.length})`).join(', ');
    console.log(`  Day ${d.num}: "${d.rawTitle}" -> ${secSummary}`);
  });
});
console.log('\nTotal days in schedule:', totalDays);
