const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const children = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"parent\":\"HKILo3FLoxkwXggHD\"%'").all();
console.log('Total children under HKILo3FLoxkwXggHD:', children.length);
for (const c of children) {
  const doc = JSON.parse(c.doc);
  console.log(`${c._id}: ${JSON.stringify(doc.key).substring(0, 70)}`);
}
