const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
function resolveFullText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) return key.map(p => typeof p === 'string' ? p : (p.text || '')).join('');
  return '';
}
const rootKids = allRems.filter(r => r.parent === 'GwREY4bq5eQvPyeAB').sort((a,b) => (a.f||'').localeCompare(b.f||''));
console.log('Root kids count:', rootKids.length);
rootKids.forEach((k, i) => console.log(`[${i}] id=${k._id} f=${k.f} text="${resolveFullText(k.key).slice(0, 60)}"`));
