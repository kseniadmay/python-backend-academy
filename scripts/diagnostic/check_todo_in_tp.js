const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"dDXVp6F6fL6FkmSK6\"%' LIMIT 20").all();
console.log('Found rows with Todo in doc:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.parent === 'dDXVp6F6fL6FkmSK6' || doc._id === 'dDXVp6F6fL6FkmSK6') continue;
  console.log(`\nID: ${r._id}, key: ${JSON.stringify(doc.key)}`);
  console.log('tp:', JSON.stringify(doc.tp));
  console.log('t:', JSON.stringify(doc.t));
  console.log('full doc snippet:', r.doc.substring(0, 300));
}
