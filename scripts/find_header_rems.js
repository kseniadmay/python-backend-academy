const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

function resolveFullText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) return key.map(p => typeof p === 'string' ? p : (p.text || '')).join('');
  return '';
}

const queries = [
  'Теория дня — карточки',
  'Кодинг — вечер в IDE',
  'Дни разгрузки (7, 14',
  'Не успел за тайм-бокс',
  'Неделя 2 · 🌐',
  'Неделя 4 · 🗄️',
  'Неделя 5 · 🏛️',
  '📌 День 42'
];

queries.forEach(q => {
  const matches = allRems.filter(r => resolveFullText(r.key).includes(q));
  console.log(`\nQuery "${q}": matches=${matches.length}`);
  matches.forEach(m => console.log(`  id=${m._id} parent=${m.parent} text="${resolveFullText(m.key).slice(0, 60)}"`));
});
