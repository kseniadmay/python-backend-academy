const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const row = db.prepare("SELECT doc FROM quanta WHERE _id = 'dDXVp6F6fL6FkmSK6'").get();
console.log('Todo doc:', row ? row.doc : 'null');

// Find rems that reference this Todo doc in tag, or in doc:
const tagged = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%dDXVp6F6fL6FkmSK6%' LIMIT 10").all();
console.log('Tagged count:', tagged.length);
for (const t of tagged) {
  console.log(t._id, t.doc.substring(0, 150));
}
