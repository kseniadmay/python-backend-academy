const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

// Check how Day 01 and Day 05 look in DB under HKILo3FLoxkwXggHD
const days = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE '%parent\":\"HKILo3FLoxkwXggHD%' AND doc LIKE '%День %'").all();
console.log('Total days under HKILo3FLoxkwXggHD:', days.length);

for (const d of days.slice(0, 5)) {
  const doc = JSON.parse(d.doc);
  console.log(`\n=== Day: ${JSON.stringify(doc.key)} (_id: ${d._id}) ===`);
  const children = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${d._id}"%`);
  for (const c of children) {
    const cdoc = JSON.parse(c.doc);
    console.log(`  Section: ${JSON.stringify(cdoc.key)} (tp: ${JSON.stringify(cdoc.tp)})`);
    const subchildren = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${c._id}"%`);
    for (const sc of subchildren.slice(0, 3)) {
      const scdoc = JSON.parse(sc.doc);
      console.log(`    Item: ${JSON.stringify(scdoc.key)} (tp: ${JSON.stringify(scdoc.tp)}, t: ${scdoc.t})`);
    }
  }
}
