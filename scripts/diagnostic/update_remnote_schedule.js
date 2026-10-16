const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const TODO_POWERUP_ID = 'dDXVp6F6fL6FkmSK6';
const ROOT_DOC_ID = 'HKILo3FLoxkwXggHD';

const WEEKS = [
  { id: 'woi7lmQesvLXOwKfk', days: ['dsBQo2KJpv1uOemNo', 'ddp4L0aEptZdz4azk', 'd5ZJ8eulRd6noc4OI', 'dhUYFs4tDGBfYqOGf', 'd5D0lgRKx2IW5Y8zR', 'd4uwj7I4FA3pHBHNC', 'dRIPIwbAsDwOIwIKa'] },
  { id: 'wXwSfI7PMK0xZ6WKv', days: ['dIrzcC6eSTrc2ZHeJ', 'dgmeAC8pxBZgmsC0T', 'dfDWPYETEv3CYM3yP', 'dmUmN1OeLwhjq0HrG', 'dTq8xJLXW5MdolGkv', 'dsGPWzyeWvo6FuJHw', 'dOk9Uve4YcyHXCuNk'] },
  { id: 'wRKo2afWo8mhdqhf6', days: ['duQsMtSLZesQ4vTns', 'dRsrNbkIzTmL5HNon', 'dzAps1mHlTJ9gvDub', 'dZHAe5VVWZjfYWjJI', 'dUvB7gKvcS7fRe5xi', 'deqAjEVgLPP0Pnxt5', 'dkojbk8YUzkahzYhN'] },
  { id: 'w0irf7AlORpYbDsKP', days: ['diNr1eF027lxJo7x7', 'dL5sPrLV1XL2MWB32', 'dgJiNCZtqByNyvfaD', 'doUtplEVy6mzKqPgU', 'dILB9NxZwQlxtSKeE', 'd86g0NEoYBJeoq78x', 'dY64Wj7CCRokMM37M'] },
  { id: 'wmOOjohySF0mb8DYU', days: ['d9JjZCTaNr03x6oEx', 'dPfZ1DPFqY4i2qIKt', 'dZaD7F6KPb591eJCV', 'dIERijF7HTjEE4pXE', 'dUUxn6yMK27B0h7mJ', 'dcKfyPSzX4ZuOoeeV', 'dctQmYnb0ZqOeZT1y'] },
  { id: 'wscAWAuAmrmNYAtLx', days: ['d8XHqCA2632HaDB2f', 'dBwKR3tnfXVkUf11W', 'dWjRca7DwczZpqwrA', 'dFXCKLaD64m6NPsCn', 'dOZf8MYnqF31r5Giy', 'dXmNdjQQFM4ngXfmc', 'dVfPfvAFa3vzLHVBj'] }
];

const ROOT_DIRECT_CHILDREN = [
  's5bLWt7eAAaNnlcTj', // 42 дня
  'hhTf3rWnxzQXioQxv', // Как читать это расписание
  'cAnud4fq8bfVEp3E8', // Оглавление
  'woi7lmQesvLXOwKfk', // Неделя 1
  'wXwSfI7PMK0xZ6WKv', // Неделя 2
  'wRKo2afWo8mhdqhf6', // Неделя 3
  'w0irf7AlORpYbDsKP', // Неделя 4
  'wmOOjohySF0mb8DYU', // Неделя 5
  'wscAWAuAmrmNYAtLx'  // Неделя 6
];

const nowTs = Date.now();
console.log(`Starting RemNote update at ${new Date(nowTs).toISOString()} (ts=${nowTs})...`);

db.exec('BEGIN TRANSACTION;');

try {
  // 1. Update Root document HKILo3FLoxkwXggHD
  const rootRow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(ROOT_DOC_ID);
  const rootDoc = JSON.parse(rootRow.doc);
  rootDoc.children = ROOT_DIRECT_CHILDREN;
  rootDoc.u = nowTs;
  rootDoc.p = nowTs;
  rootDoc['children,u'] = nowTs;
  db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(rootDoc), ROOT_DOC_ID);
  console.log(`Updated root doc ${ROOT_DOC_ID} with ${ROOT_DIRECT_CHILDREN.length} direct children.`);

  // 2. Update Weeks and Day hierarchies
  let daysMoved = 0;
  for (const w of WEEKS) {
    const weekRow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(w.id);
    if (!weekRow) {
      console.error(`Week doc not found: ${w.id}`);
      continue;
    }
    const weekDoc = JSON.parse(weekRow.doc);
    weekDoc.parent = ROOT_DOC_ID;
    weekDoc.children = w.days;
    weekDoc.u = nowTs;
    weekDoc.p = nowTs;
    weekDoc['children,u'] = nowTs;
    weekDoc['parent,u'] = nowTs;
    db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(weekDoc), w.id);

    // Update each Day under this week
    for (let i = 0; i < w.days.length; i++) {
      const dayId = w.days[i];
      const dayRow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(dayId);
      if (!dayRow) {
        console.error(`Day doc not found: ${dayId}`);
        continue;
      }
      const dayDoc = JSON.parse(dayRow.doc);
      dayDoc.parent = w.id;
      dayDoc['parent,u'] = nowTs;
      dayDoc.u = nowTs;
      dayDoc.p = nowTs;
      db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(dayDoc), dayId);
      daysMoved++;
    }
  }
  console.log(`Updated 6 weeks and moved ${daysMoved} days into their respective weeks.`);

  // 3. Add Todo checkboxes to Theory, Practice, and Checklist items
  let theoryTagged = 0;
  let codingTagged = 0;
  let checklistTagged = 0;

  const allDayIds = WEEKS.flatMap(w => w.days);
  for (const dayId of allDayIds) {
    const sections = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${dayId}"%`);
    for (const s of sections) {
      const sdoc = JSON.parse(s.doc);
      const title = JSON.stringify(sdoc.key || '');
      const items = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${s._id}"%`);

      for (const it of items) {
        const itemDoc = JSON.parse(it.doc);
        // Add Todo powerup
        itemDoc.tp = itemDoc.tp || {};
        itemDoc.tp[TODO_POWERUP_ID] = { t: false, ",u": nowTs };
        itemDoc.bpc = itemDoc.bpc || {};
        itemDoc.bpc.t = {};
        itemDoc['bpc,u'] = nowTs;
        itemDoc.apu = itemDoc.apu || {};
        itemDoc.apu.t = { v: true, ",u": nowTs };
        itemDoc.u = nowTs;
        itemDoc.p = nowTs;

        db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(itemDoc), it._id);

        if (title.includes('Теория')) theoryTagged++;
        else if (title.includes('кодинг') || title.includes('Кодинг')) codingTagged++;
        else if (title.includes('Чек-лист')) checklistTagged++;
      }
    }
  }

  console.log(`Tagged items with Todo checkboxes:`);
  console.log(`  Theory items: ${theoryTagged}`);
  console.log(`  Coding tasks: ${codingTagged}`);
  console.log(`  Checklist items: ${checklistTagged}`);

  // 4. Update sync2 metadata table as required by remnote-sync rules
  const syncRow = db.prepare("SELECT doc FROM sync2 WHERE _id = 'quanta'").get();
  if (syncRow) {
    const syncDoc = JSON.parse(syncRow.doc);
    syncDoc.lastSync = nowTs - 2000;
    syncDoc.lastSyncFullBatchDoneTime = nowTs - 2000;
    db.prepare("UPDATE sync2 SET doc = ? WHERE _id = 'quanta'").run(JSON.stringify(syncDoc));
    console.log(`Rolled back sync2.quanta lastSync to ${nowTs - 2000}`);
  }

  db.exec('COMMIT;');
  console.log('Transaction COMMITTED successfully.');

  // 5. PRAGMA wal_checkpoint(FULL)
  const walRes = db.prepare('PRAGMA wal_checkpoint(FULL);').get();
  console.log('WAL Checkpoint result:', walRes);

} catch (err) {
  db.exec('ROLLBACK;');
  console.error('ERROR during RemNote update, transaction rolled back:', err);
  process.exit(1);
}
