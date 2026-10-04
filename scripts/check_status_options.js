const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check children of Status slot CT6ecdlVB4irYDsfl
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"parent\":\"CT6ecdlVB4irYDsfl\"%'").all();
console.log('Status options:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  console.log(r._id, JSON.stringify(doc.key), doc.f, doc.rcrs);
}
