const fs = require('fs');
const s = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\weeks_summary.json', 'utf8'));
s.weeksSummary.forEach(w => {
  console.log(`Week ${w.week} (${w.daysCount} days): ${w.days.map(d => d.text.slice(0, 20)).join(', ')}`);
});
console.log('\nReview Days:');
s.reviewDays.forEach(r => {
  console.log(`Day ${r.day}: ${r.matches.map(m => `[${m.id} parent=${m.parent} "${m.text.slice(0, 35)}"]`).join('; ')}`);
});