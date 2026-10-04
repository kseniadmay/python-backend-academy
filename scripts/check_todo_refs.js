const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Search for any occurrence of 'dDXVp6F6fL6FkmSK6' in quanta where _id != 'dDXVp6F6fL6FkmSK6'
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%dDXVp6F6fL6FkmSK6%' AND _id != 'dDXVp6F6fL6FkmSK6' LIMIT 10").all();
console.log('Found rows referencing Todo ID:', rows.length);
for (const r of rows) {
  console.log(`\n--- _id: ${r._id} ---`);
  console.log(r.doc);
}
