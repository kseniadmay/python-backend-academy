const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check Day 07 (dRIPIwbAsDwOIwIKa)
const d7 = db.prepare("SELECT doc FROM quanta WHERE _id = 'dRIPIwbAsDwOIwIKa'").get();
console.log('Day 07 doc:', d7 ? d7.doc : 'null');

const children = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"parent\":\"dRIPIwbAsDwOIwIKa\"%'").all();
console.log('Day 07 children:', children.length);
for (const c of children) {
  const doc = JSON.parse(c.doc);
  console.log(' ', c._id, JSON.stringify(doc.key));
  const subs = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${c._id}"%`);
  for (const s of subs) {
    const sdoc = JSON.parse(s.doc);
    console.log('    ', s._id, JSON.stringify(sdoc.key));
  }
}
