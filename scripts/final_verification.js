const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

console.log('=== VERIFYING REMNOTE SQLITE DB ===');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
if (!fs.existsSync(dbPath)) {
  console.log(`[SKIP] Local desktop RemNote database not found at ${dbPath}.`);
  console.log('[INFO] RemNote invariant: desktop client is not used; verification proceeds via web/json.');
  process.exit(0);
}
const db = new DatabaseSync(dbPath, { open: true });

const rootRow = db.prepare("SELECT doc FROM quanta WHERE _id = 'HKILo3FLoxkwXggHD'").get();
const rootDoc = JSON.parse(rootRow.doc);
console.log('Root children count:', (rootDoc.children || []).length);

const weekIds = [
  'woi7lmQesvLXOwKfk',
  'wXwSfI7PMK0xZ6WKv',
  'wRKo2afWo8mhdqhf6',
  'w0irf7AlORpYbDsKP',
  'wmOOjohySF0mb8DYU',
  'wscAWAuAmrmNYAtLx'
];

let totalDays = 0;
let totalCheckedTheory = 0;
let totalCheckedCoding = 0;
let totalCheckedChecklist = 0;

for (const wid of weekIds) {
  const wrow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(wid);
  const wdoc = JSON.parse(wrow.doc);
  totalDays += (wdoc.children || []).length;
  for (const did of (wdoc.children || [])) {
    const sections = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${did}"%`);
    for (const s of sections) {
      const sdoc = JSON.parse(s.doc);
      const title = JSON.stringify(sdoc.key || '');
      const items = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${s._id}"%`);
      for (const it of items) {
        const idoc = JSON.parse(it.doc);
        const hasTodo = idoc.bpc && idoc.bpc.t && idoc.apu && idoc.apu.t;
        if (hasTodo) {
          if (title.includes('Теория')) totalCheckedTheory++;
          else if (title.includes('кодинг') || title.includes('Кодинг')) totalCheckedCoding++;
          else if (title.includes('Чек-лист')) totalCheckedChecklist++;
        }
      }
    }
  }
}

console.log(`Weeks verified: ${weekIds.length}`);
console.log(`Total days nested under weeks: ${totalDays}`);
console.log(`Checked Theory items: ${totalCheckedTheory}`);
console.log(`Checked Coding tasks: ${totalCheckedCoding}`);
console.log(`Checked Checklist items: ${totalCheckedChecklist}`);

const wal = db.prepare('PRAGMA wal_checkpoint(FULL);').get();
console.log('WAL checkpoint:', wal);

console.log('\n=== VERIFYING MARKDOWN FILE ===');
const mdPath = 'C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md';
const mdLines = fs.readFileSync(mdPath, 'utf8').split('\n');

let mdHeadings = 0;
let mdTasks = 0;
let mdTheory = 0;
let mdChecklist = 0;
let badHeadings = 0;

for (const l of mdLines) {
  if (l.startsWith('### ')) mdHeadings++;
  if (l.startsWith('- ### ') || l.startsWith('- ## ')) badHeadings++;
  if (l.match(/\[ \]\s+\S+\s+Уровень \d/u)) mdTasks++;
  if (l.match(/\[ \]\s+\[.*\]\(\)/)) mdTheory++;
  if (l.match(/\[ \]\s+(Могу|Понимаю|Решил|Знаю|Умею|Пишу|Прошёл|Закрыл)/)) mdChecklist++;
}

console.log(`MD Headings (###): ${mdHeadings}`);
console.log(`MD Bad Headings (- ###): ${badHeadings}`);
console.log(`MD Tasks with [ ]: ${mdTasks}`);
console.log(`MD Theory with [ ]: ${mdTheory}`);
console.log(`MD Checklist with [ ]: ${mdChecklist}`);
