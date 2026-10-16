const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

const dbPath = 'C:/Users/fury6/remnote/remnote-69d8425df107d8b00ed6ddb9/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const docId = 'GwREY4bq5eQvPyeAB';
const row = db.prepare('SELECT _id, doc FROM quanta WHERE _id = ?').get(docId);
if (row) {
  const doc = JSON.parse(row.doc);
  console.log('FOUND document GwREY4bq5eQvPyeAB:');
  console.log('Key:', JSON.stringify(doc.key));
  console.log('Children count:', (doc.children || []).length);
  console.log('Doc preview:', JSON.stringify(doc).substring(0, 300));
} else {
  console.log('GwREY4bq5eQvPyeAB NOT FOUND in quanta table');
  const allDocs = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ? LIMIT 10').all('%Junior%');
  console.log('Docs with Junior:', allDocs.length);
  for (const d of allDocs) {
    console.log(d._id, JSON.parse(d.doc).key);
  }
}
