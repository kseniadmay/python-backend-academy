const fs = require('fs');
const path = require('path');
const dumpPath = fs.existsSync(path.join(__dirname, 'all_rems_dump.json'))
  ? path.join(__dirname, 'all_rems_dump.json')
  : path.join(__dirname, '..', 'all_rems_dump.json');
const allRems = JSON.parse(fs.readFileSync(dumpPath, 'utf8'));

const remById = new Map();
allRems.forEach(r => remById.set(r._id, r));

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
          const target = remById.get(part._id);
          if (target) return resolveFullText(target.key, depth + 1);
        }
      }
      return '';
    }).join('');
  }
  return '';
}

const kids = allRems.filter(r => r.parent === '5ZDJKYuWr8stenQ0Q');
console.log('5ZDJKYuWr8stenQ0Q kids with resolved text:');
kids.forEach(k => console.log(' -', resolveFullText(k.key)));
