const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const rows = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ?').all('%"parent":"dsBQo2KJpv1uOemNo"%');
console.log('Children of Day 01:', rows.length);
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  console.log(`_id: ${r._id}, key: ${JSON.stringify(doc.key)}, type: ${doc.type}, cr: ${doc.cr}`);
  // and children of this child
  const subrows = db.prepare('SELECT _id, doc FROM quanta WHERE doc LIKE ?').all(`%"parent":"${r._id}"%`);
  for (const sr of subrows) {
    const sdoc = JSON.parse(sr.doc);
    console.log(`    child: ${sr._id}, key: ${JSON.stringify(sdoc.key)}, type: ${sdoc.type}, cr: ${sdoc.cr}`);
  }
}
