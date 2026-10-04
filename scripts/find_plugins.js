const { execSync } = require('child_process');

const dbPath = 'C:\\Users\\fury6\\remnote\\remnote-6a7345f0a3f205110d2692d2\\remnote.db';

function run(sql) {
  return execSync(`sqlite3 "${dbPath}" "${sql}"`, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
}

// Check plugins or scheduler in quanta
const rows = run(`SELECT _id, doc FROM quanta WHERE doc LIKE '%plugin%' LIMIT 30;`).split('\n').filter(Boolean);
console.log(`Found ${rows.length} rows with 'plugin':`);
rows.forEach((r, i) => {
  const parts = r.split('|');
  const id = parts[0];
  const doc = parts.slice(1).join('|');
  try {
    const obj = JSON.parse(doc);
    console.log(`[${i+1}] id=${id} key=${JSON.stringify(obj.key)} pluginId=${obj.pluginId || ''} tag=${obj.tag || ''}`);
  } catch (e) {
    console.log(`[${i+1}] id=${id} raw=${doc.slice(0, 100)}`);
  }
});
