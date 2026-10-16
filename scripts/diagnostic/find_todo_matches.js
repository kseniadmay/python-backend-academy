const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%dDXVp6F6fL6FkmSK6%'").all();
console.log('Total matches for dDXVp6F6fL6FkmSK6:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.parent !== 'dDXVp6F6fL6FkmSK6' && r._id !== 'dDXVp6F6fL6FkmSK6') {
    console.log('Match non-child:', r._id, r.doc);
  }
}
