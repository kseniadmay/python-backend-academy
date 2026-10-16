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

[27, 40].forEach(dayNum => {
  // Day rem
  const dRem = allRems.find(r => resolveFullText(r.key).includes(`День ${dayNum < 10 ? '0' + dayNum : dayNum}`) || resolveFullText(r.key).includes(`День ${dayNum}`));
  console.log(`\nDay ${dayNum} Rem: id=${dRem._id} text="${resolveFullText(dRem.key).slice(0, 50)}"`);
  const kids = allRems.filter(r => r.parent === dRem._id);
  console.log(`Kids (${kids.length}):`);
  kids.forEach(k => {
    console.log(` - id=${k._id} f=${k.f} text="${resolveFullText(k.key).slice(0, 60)}" (subKids: ${allRems.filter(r => r.parent === k._id).length})`);
    allRems.filter(r => r.parent === k._id).forEach(sk => {
      console.log(`     * id=${sk._id} text="${resolveFullText(sk.key).slice(0, 60)}"`);
    });
  });
});
