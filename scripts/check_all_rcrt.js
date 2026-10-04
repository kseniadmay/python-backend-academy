const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"rcrt\":%'").all();
console.log('Docs with rcrt:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.rcrt) {
    console.log(`${r._id}: rcrt="${doc.rcrt}", key=${JSON.stringify(doc.key)}`);
  }
}
