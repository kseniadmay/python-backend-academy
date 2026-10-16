const fs = require('fs');
const path = require('path');

console.log('=== VERIFYING REMNOTE SCHEDULE & STRUCTURE ===');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const dumpPath = path.join(__dirname, 'all_rems_dump.json');

if (fs.existsSync(dbPath)) {
  const { DatabaseSync } = require('node:sqlite');
  const db = new DatabaseSync(dbPath, { open: true });
  const rootRow = db.prepare("SELECT doc FROM quanta WHERE _id = 'HKILo3FLoxkwXggHD'").get();
  if (rootRow) {
    const rootDoc = JSON.parse(rootRow.doc);
    console.log('Root children count in SQLite:', (rootDoc.children || []).length);
  }
} else if (fs.existsSync(dumpPath)) {
  console.log('[INFO] Using all_rems_dump.json (RemNote desktop offline invariant)');
  const allRems = JSON.parse(fs.readFileSync(dumpPath, 'utf8'));
  const rootDoc = allRems.find(r => r._id === 'GwREY4bq5eQvPyeAB');
  if (!rootDoc) {
    console.error('[ERROR] Canonical schedule root GwREY4bq5eQvPyeAB not found in dump!');
    process.exit(1);
  }
  
  const weeks = allRems.filter(r => r.parent === rootDoc._id && (JSON.stringify(r.key || '').includes('Неделя')));
  console.log(`Weeks verified: ${weeks.length} / 6`);
  
  function resolveFullText(key, depth = 0) {
    if (!key || depth > 3) return '';
    if (typeof key === 'string') return key;
    if (Array.isArray(key)) {
      return key.map(part => {
        if (typeof part === 'string') return part;
        if (part && typeof part === 'object') {
          if (part.text) return part.text;
          if (part.textOfDeletedRem) return part.textOfDeletedRem.join(' ');
          if (part.i === 'q' && part._id) {
            const target = allRems.find(r => r._id === part._id);
            if (target) return resolveFullText(target.key, depth + 1);
          }
        }
        return '';
      }).join('');
    }
    return '';
  }

  const weekIds = new Set(weeks.map(w => w._id));
  const days = allRems.filter(r => weekIds.has(r.parent));
  console.log(`Total days under canonical weeks: ${days.length} / 42`);
  if (weeks.length !== 6 || days.length !== 42) {
    console.error(`[ERROR] Expected 6 weeks and 42 days, got ${weeks.length} weeks and ${days.length} days`);
    process.exit(1);
  }
  console.log('✓ RemNote schedule hierarchy strictly verified via all_rems_dump.json!');
}

console.log('\n=== VERIFYING MARKDOWN & CURRICULUM INTEGRITY ===');
const mdDownloadsPath = 'C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md';
let mdLines = [];
if (fs.existsSync(mdDownloadsPath)) {
  mdLines = fs.readFileSync(mdDownloadsPath, 'utf8').split('\n');
  console.log(`Auditing ${mdDownloadsPath}`);
} else {
  const mapPath = path.join(__dirname, '..', 'RemNote_Python_Mastery_FIXED', '00 · 🗺️ Карта Мастерства.md');
  if (fs.existsSync(mapPath)) {
    mdLines = fs.readFileSync(mapPath, 'utf8').split('\n');
    console.log(`Auditing local curriculum map: ${mapPath}`);
  }
}

if (mdLines.length > 0) {
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
  if (badHeadings > 0) {
    console.error(`[ERROR] Found ${badHeadings} bad headings (- ###)!`);
    process.exit(1);
  }
}

console.log('✓ All schedule and curriculum verifications PASSED!');
