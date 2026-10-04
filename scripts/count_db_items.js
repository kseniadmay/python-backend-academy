const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check days
const days = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%parent\":\"HKILo3FLoxkwXggHD%' AND doc LIKE '%День %'").all();
console.log('Total day nodes:', days.length);

let totalTheory = 0;
let totalCoding = 0;
let totalChecklist = 0;

for (const d of days) {
  const sections = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${d._id}"%`);
  for (const s of sections) {
    const sdoc = JSON.parse(s.doc);
    const title = JSON.stringify(sdoc.key || '');
    const items = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${s._id}"%`);
    if (title.includes('Теория')) {
      totalTheory += items.length;
    } else if (title.includes('кодинг') || title.includes('Кодинг')) {
      totalCoding += items.length;
    } else if (title.includes('Чек-лист')) {
      totalChecklist += items.length;
    }
  }
}

console.log('Total Theory items in DB:', totalTheory);
console.log('Total Coding tasks in DB:', totalCoding);
console.log('Total Checklist items in DB:', totalChecklist);
