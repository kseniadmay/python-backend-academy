const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare("SELECT * FROM sync2").all();
console.log('sync2 rows:');
for (const r of rows) {
  console.log(r._id, r.doc);
}
