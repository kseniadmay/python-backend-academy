const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
if (!fs.existsSync(dbPath)) {
  console.error('DB not found:', dbPath);
  process.exit(1);
}

const db = new DatabaseSync(dbPath, { open: true });

// Check root doc HKILo3FLoxkwXggHD
const stmt = db.prepare('SELECT doc FROM quanta WHERE _id = ?');
const row = stmt.get('HKILo3FLoxkwXggHD');
if (!row) {
  console.error('Root doc HKILo3FLoxkwXggHD not found!');
  process.exit(1);
}

const rootDoc = JSON.parse(row.doc);
console.log('Root doc found:');
console.log('Key:', JSON.stringify(rootDoc.key));
console.log('Children count:', (rootDoc.children || []).length);

// Let's inspect the children
const childIds = rootDoc.children || [];
const childrenStmt = db.prepare('SELECT _id, doc FROM quanta WHERE _id IN (' + childIds.map(() => '?').join(',') + ')');
const childRows = childrenStmt.all(...childIds);
const childMap = {};
for (const r of childRows) {
  childMap[r._id] = JSON.parse(r.doc);
}

console.log('\nTop-level children:');
childIds.forEach((id, idx) => {
  const doc = childMap[id];
  const text = doc ? (doc.key ? JSON.stringify(doc.key) : '(no key)') : '(missing)';
  console.log(`${idx + 1}. [${id}] children=${(doc && doc.children || []).length}: ${text.substring(0, 80)}`);
});
