const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rcrtMap = {};
const rows = db.prepare("SELECT doc FROM quanta LIMIT 1000").all();
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.rcrt !== undefined) {
    rcrtMap[doc.rcrt] = (rcrtMap[doc.rcrt] || 0) + 1;
  }
}
console.log('rcrt values:', rcrtMap);
