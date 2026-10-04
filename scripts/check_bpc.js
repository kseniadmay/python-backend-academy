const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"bpc\":%' LIMIT 50").all();
console.log('Docs with bpc:', rows.length);
const bpcKeys = new Set();
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.bpc) {
    Object.keys(doc.bpc).forEach(k => bpcKeys.add(k));
    if (doc.bpc.t) {
      console.log('FOUND bpc.t:', r._id, r.doc);
    }
  }
}
console.log('All bpc keys found:', Array.from(bpcKeys));
