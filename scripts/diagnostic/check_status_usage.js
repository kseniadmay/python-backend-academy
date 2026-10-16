const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check for any rems referencing YZV9qYAyWScZ6YvkC (Unfinished) or 07tMKid0201Q8cdiT (Finished)
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%YZV9qYAyWScZ6YvkC%' OR doc LIKE '%07tMKid0201Q8cdiT%'").all();
console.log('Matches for Unfinished/Finished IDs:', rows.length);
for (const r of rows) {
  console.log(r._id, r.doc.substring(0, 200));
}
