const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Find any rem with tag or t property
const rows = db.prepare("SELECT doc FROM quanta WHERE doc LIKE '%\"tag\"%' OR doc LIKE '%\"tags\"%' OR doc LIKE '%\"t\"%' LIMIT 20").all();
for (const r of rows) {
  const doc = JSON.parse(r.doc);
  if (doc.tag || doc.tags || (Array.isArray(doc.t) && doc.t.length > 0)) {
    console.log(doc._id, 'key:', JSON.stringify(doc.key), 'tag:', doc.tag, 'tags:', doc.tags, 't:', doc.t, 'status:', doc.status);
  }
}
