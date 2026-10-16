const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check docs with non-empty t array
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"t\":[%' LIMIT 20").all();
console.log('Docs with t array:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (Array.isArray(doc.t) && doc.t.length > 0) {
    console.log(r._id, 't:', JSON.stringify(doc.t), 'key:', JSON.stringify(doc.key).substring(0, 40));
  }
}
