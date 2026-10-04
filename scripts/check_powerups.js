const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check powerups: powerups usually have e: "u..." or type: 2 or rcrs
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%rcrs%' LIMIT 50").all();
console.log('Found rcrs rows:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  console.log(`${r._id} -> rcrs: ${doc.rcrs}, key: ${JSON.stringify(doc.key)}, parent: ${doc.parent}`);
}
