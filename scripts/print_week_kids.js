const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
function resolveFullText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) return key.map(p => typeof p === 'string' ? p : (p.text || '')).join('');
  return '';
}
const weekIds = [
  'i2G5Z1gxlEaEf4Sz3',
  'YvCOnToaalzIwm2MY',
  'gFKS7LUxkNdmTlwmy',
  'ms4eHbXFhOQLYTFmN',
  'xGQiIy44gskxNmv3u',
  'ucZRFaKMYsiOa6VKW'
];

weekIds.forEach((wId, idx) => {
  const kids = allRems.filter(r => r.parent === wId).sort((a,b) => (a.f||'').localeCompare(b.f||''));
  console.log(`\nWeek ${idx+1} (${wId}) kids count: ${kids.length}`);
  kids.forEach((k, i) => console.log(`  [${i}] id=${k._id} f=${k.f} text="${resolveFullText(k.key).slice(0, 50)}"`));
});
