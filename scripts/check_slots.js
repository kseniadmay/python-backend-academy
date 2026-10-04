const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check how slot values are attached to rems
// Let's find rems where parent is a slot or has slot child
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%rcrs%' LIMIT 10").all();
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  // find if any rem has parent = r._id
  const children = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${r._id}"%`);
  if (children.length > 0) {
    console.log(`Slot ${doc.rcrs} (${r._id}) has children:`, children.length);
    for (const c of children) {
      const cdoc = JSON.parse(c.doc);
      console.log(`  child: ${c._id}, key: ${JSON.stringify(cdoc.key)}, value: ${JSON.stringify(cdoc.value)}`);
    }
  }
}
