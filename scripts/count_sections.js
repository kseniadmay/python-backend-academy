const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

function extractText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(part => {
      if (typeof part === 'string') return part;
      if (part && typeof part === 'object') {
        return part.text || (part.textOfDeletedRem ? part.textOfDeletedRem.join(' ') : '');
      }
      return '';
    }).join('');
  }
  return '';
}

const theories = [];
const codings = [];
const checklists = [];
const standouts = [];

allRems.forEach(r => {
  const t = extractText(r.key).trim();
  if (t.startsWith('Теория') || t.startsWith('🌅')) theories.push({ id: r._id, parent: r.parent, text: t.slice(0, 60) });
  else if (t.startsWith('Кодинг') || t.startsWith('💻') || t.startsWith('Вечерний')) codings.push({ id: r._id, parent: r.parent, text: t.slice(0, 60) });
  else if (t.includes('Чек-лист') || t.startsWith('✅')) checklists.push({ id: r._id, parent: r.parent, text: t.slice(0, 60) });
  else if (t.includes('Стенд-аут') || t.startsWith('🎯')) standouts.push({ id: r._id, parent: r.parent, text: t.slice(0, 60) });
});

console.log(`Theories: ${theories.length}`);
console.log(`Codings: ${codings.length}`);
console.log(`Checklists: ${checklists.length}`);
console.log(`Standouts: ${standouts.length}`);
