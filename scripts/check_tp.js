const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check docs with non-empty tp
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"tp\":{%' LIMIT 30").all();
console.log('Docs with tp:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.tp && Object.keys(doc.tp).length > 0) {
    console.log(r._id, 'tp:', JSON.stringify(doc.tp), 'key:', JSON.stringify(doc.key).substring(0, 40));
  }
}
