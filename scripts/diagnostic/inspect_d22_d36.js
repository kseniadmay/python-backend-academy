const fs = require('fs');
const audit = JSON.parse(fs.readFileSync('all_days_audit.json', 'utf8'));

function checkDay(dayNum) {
  let found = null;
  audit.forEach(w => {
    w.days.forEach(d => {
      const dm = d.dayText.match(/День\s*0?(\d+)/);
      if (dm && parseInt(dm[1]) === dayNum) found = d;
    });
  });
  return found;
}

console.log('=== Day 22 Children ===');
const d22 = checkDay(22);
if (d22) {
  d22.kids.forEach((k, i) => {
    console.log(`[${i}] id=${k.id} f=${k.f} type=${k.type} count=${k.subSubCount}: "${k.text}"`);
  });
}

console.log('\n=== Day 36 Children ===');
const d36 = checkDay(36);
if (d36) {
  d36.kids.forEach((k, i) => {
    console.log(`[${i}] id=${k.id} f=${k.f} type=${k.type} count=${k.subSubCount}: "${k.text}"`);
  });
}
