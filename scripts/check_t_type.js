const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare("SELECT doc FROM quanta WHERE doc LIKE '%\"t\":%' LIMIT 10").all();
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.t !== undefined) {
    console.log(doc._id, 't:', doc.t, typeof doc.t);
  }
}
