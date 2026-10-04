const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Find recent docs modified today (Sept 16, 2026) or containing "День 01"
const rows = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ? LIMIT 30').all('%День 01%');
console.log('Found docs matching "День 01":', rows.length);
for (const r of rows) {
  try {
    const doc = JSON.parse(r.doc);
    const key = doc.key ? JSON.stringify(doc.key) : '(no key)';
    const parent = doc.parent;
    console.log(`ID: ${r._id}, parent: ${parent}, children: ${(doc.children || []).length}, key: ${key.substring(0, 100)}`);
  } catch (e) {
    console.log('Error parsing:', r._id, e.message);
  }
}

// Also check documents containing "42 дня"
const rows42 = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ? LIMIT 10').all('%42 дня%');
console.log('\nFound docs matching "42 дня":', rows42.length);
for (const r of rows42) {
  try {
    const doc = JSON.parse(r.doc);
    const key = doc.key ? JSON.stringify(doc.key) : '(no key)';
    console.log(`ID: ${r._id}, parent: ${doc.parent}, children: ${(doc.children || []).length}, key: ${key.substring(0, 100)}`);
  } catch (e) {}
}
