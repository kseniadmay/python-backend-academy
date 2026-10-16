const { execSync } = require('child_process');

const dbPath = 'C:\\Users\\fury6\\remnote\\remnote-6a7345f0a3f205110d2692d2\\remnote.db';

function run(sql) {
  try {
    return execSync(`sqlite3 "${dbPath}" "${sql}"`, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  } catch (e) {
    return 'Error: ' + e.message;
  }
}

console.log('--- Search 8080 or localhost in db: ---');
const tables = ['user_data', 'knowledge_base_data', 'quanta', 'key_value_store'];
for (const t of tables) {
  const q = `SELECT count(*) FROM ${t} WHERE doc LIKE '%8080%' OR doc LIKE '%localhost%';`;
  console.log(`${t}:`, run(q).trim());
}

console.log('\n--- Checking any installed plugins: ---');
for (const t of tables) {
  const q = `SELECT _id, doc FROM ${t} WHERE doc LIKE '%developerPlugin%' OR doc LIKE '%installedPlugins%' OR doc LIKE '%customScheduler%' LIMIT 5;`;
  const res = run(q).trim();
  if (res) {
    console.log(`Matches in ${t}:`);
    console.log(res.slice(0, 300));
  }
}
