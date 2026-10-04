const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Search for todo or checkbox in quanta
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%todo%' OR doc LIKE '%checkbox%' OR doc LIKE '%\"type\":1%' OR doc LIKE '%\"type\":2%' LIMIT 10").all();
console.log('Found rows:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  console.log(`_id: ${r._id}, type: ${doc.type}, cr: ${doc.cr}, status: ${doc.status}, todo: ${doc.todo}, key: ${JSON.stringify(doc.key).substring(0, 60)}`);
}
