const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

function resolveFullText(key, depth = 0) {
  if (!key || depth > 3) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(part => {
      if (typeof part === 'string') return part;
      if (part && typeof part === 'object') {
        if (part.text) return part.text;
        if (part.textOfDeletedRem) return part.textOfDeletedRem.join(' ');
        if (part.i === 'q' && part._id) {
          const target = allRems.find(r => r._id === part._id);
          if (target) return resolveFullText(target.key, depth + 1);
        }
      }
      return '';
    }).join('');
  }
  return '';
}

const d22Kids = allRems.filter(r => r.parent === 'sc8pMIDZUZ3JoNsYR');
console.log('Total kids in Day 22:', d22Kids.length);

const codingKids = d22Kids.filter(k => {
  const t = resolveFullText(k.key);
  return t.includes('Кодинг') || t.includes('💻');
});

console.log('Coding kids in Day 22:', codingKids.length);
codingKids.forEach(ck => {
  const subKids = allRems.filter(r => r.parent === ck._id);
  const sample = subKids.map(sk => resolveFullText(sk.key)).filter(x => x.length > 5).slice(0, 3);
  console.log(`\n[${ck._id}] "${resolveFullText(ck.key).slice(0, 60)}" (subKids: ${subKids.length})`);
  sample.forEach(s => console.log('   *', s.slice(0, 60)));
});
