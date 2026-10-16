const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ?').all('%"parent":"HKILo3FLoxkwXggHD"%');
console.log('Count of items with parent HKILo3FLoxkwXggHD:', rows.length);
for (const r of rows.slice(0, 20)) {
  const doc = JSON.parse(r.doc);
  console.log(`_id: ${r._id}, key: ${JSON.stringify(doc.key).substring(0, 60)}, children: ${(doc.children || []).length}`);
}
