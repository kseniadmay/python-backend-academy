const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const docId = 'GwREY4bq5eQvPyeAB';
const row = db.prepare('SELECT _id, doc FROM quanta WHERE _id = ?').get(docId);
console.log('Lookup GwREY4bq5eQvPyeAB in quanta:', row ? row.doc : 'NOT FOUND');

if (!row) {
  // Check if it exists with LIKE
  const likeRows = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ?').all(`%${docId}%`);
  console.log('LIKE matches in quanta:', likeRows.length);
  for (const r of likeRows) {
    console.log(r._id, r.doc.substring(0, 100));
  }
}
