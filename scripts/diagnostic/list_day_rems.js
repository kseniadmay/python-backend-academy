const fs = require('fs');
const audit = JSON.parse(fs.readFileSync('all_days_audit.json', 'utf8'));

const dayRems = [];
audit.forEach((w, wIdx) => {
  w.days.forEach((d, dIdx) => {
    dayRems.push({
      num: wIdx * 7 + dIdx + 1,
      weekNum: wIdx + 1,
      id: d.dayId,
      text: d.dayText
    });
  });
});

console.log(`Found ${dayRems.length} day rems in weeks:`);
dayRems.forEach(d => console.log(`Day ${d.num} [${d.id}]: ${d.text.slice(0, 60)}`));
