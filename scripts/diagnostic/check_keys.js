const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check what fields are in quanta docs
const allKeys = new Set();
const rows = db.prepare("SELECT doc FROM quanta LIMIT 200").all();
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  Object.keys(doc).forEach(k => allKeys.add(k));
}
console.log('All doc keys:', Array.from(allKeys));
