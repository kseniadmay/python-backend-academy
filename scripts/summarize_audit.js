const fs = require('fs');
const audit = JSON.parse(fs.readFileSync('all_days_audit.json', 'utf8'));

audit.forEach(w => {
  console.log(`\n=== ${w.weekText} (${w.days.length} days) ===`);
  w.days.forEach((d, idx) => {
    console.log(`  [Day ${idx+1}] ${d.dayText.slice(0, 50)} (id=${d.dayId}, kids=${d.kidsCount})`);
    if (d.kidsCount > 2) {
      d.kids.forEach(k => {
        console.log(`     - [${k.id}] f=${k.f} type=${k.type} count=${k.subSubCount}: "${k.text.slice(0, 45)}"`);
      });
    }
  });
});
