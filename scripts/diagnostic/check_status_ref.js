const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check how RemNote handles todo status in other rems or if there are any completed todos
const rows = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%YZV9qYAyWScZ6YvkC%'").all();
console.log('YZV9qYAyWScZ6YvkC references:', rows.length);
for (const r of rows) {
  console.log(r._id, r.doc);
}
