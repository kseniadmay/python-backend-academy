const fs = require('fs');

const ast = JSON.parse(fs.readFileSync('local_file_ast.json', 'utf8'));
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

const remById = new Map();
allRems.forEach(r => remById.set(r._id, r));

function resolveText(key, depth = 0) {
  if (!key || depth > 3) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(part => {
      if (typeof part === 'string') return part;
      if (part && typeof part === 'object') {
        if (part.text) return part.text;
        if (part.textOfDeletedRem) return part.textOfDeletedRem.join(' ');
        if (part.i === 'q' && part._id) {
          const target = remById.get(part._id);
          if (target) return resolveText(target.key, depth + 1);
        }
      }
      return '';
    }).join('');
  }
  return '';
}

function norm(s) {
  return (s || '').toLowerCase().replace(/[^a-zа-яё0-9]/gi, ' ').replace(/\s+/g, ' ').trim();
}

// Build index of all rems by normalized text
const remsByNorm = new Map();
allRems.forEach(r => {
  const t = norm(resolveText(r.key));
  if (t.length > 5) {
    if (!remsByNorm.has(t)) remsByNorm.set(t, []);
    remsByNorm.get(t).push(r);
  }
});

let totalItems = 0;
let mappedItems = 0;
const unmappedItems = [];

ast.weeks.forEach(w => {
  w.days.forEach(d => {
    d.sections.forEach(s => {
      s.items.forEach(it => {
        totalItems++;
        // Clean markdown link: e.g. "- [ ] [global и nonlocal...]()" -> "global и nonlocal..."
        let clean = it.replace(/^-\s*(\[\s*\]\s*)?/, '').trim();
        // remove animal emoji
        clean = clean.replace(/^[🥚🐣🦊🐺🐯🐉👑⏱️🎯✅]\s*/, '').trim();
        clean = clean.replace(/^Уровень\s*\d+\s*·\s*/, '').trim();
        clean = clean.replace(/#\w+$/, '').trim();
        const linkMatch = clean.match(/\[(.*?)\]\(\)/);
        const targetTitle = linkMatch ? linkMatch[1] : clean;
        const n = norm(targetTitle);
        
        let found = null;
        if (remsByNorm.has(n)) {
          found = remsByNorm.get(n)[0];
        } else {
          // fuzzy match
          const sub = n.slice(0, 25);
          for (const [k, list] of remsByNorm.entries()) {
            if (k.includes(sub) || sub.includes(k.slice(0, 25))) {
              found = list[0];
              break;
            }
          }
        }
        if (found) {
          mappedItems++;
        } else {
          unmappedItems.push({ day: d.num, item: it, targetTitle });
        }
      });
    });
  });
});

console.log(`Total items in local file: ${totalItems}`);
console.log(`Mapped items to RemNote rems: ${mappedItems}`);
console.log(`Unmapped items count: ${unmappedItems.length}`);
if (unmappedItems.length > 0) {
  console.log('Sample unmapped items (first 10):');
  unmappedItems.slice(0, 10).forEach(u => console.log(`  Day ${u.day}: "${u.targetTitle}"`));
}
