const { execSync } = require('child_process');

const dbPath = 'C:\\Users\\fury6\\remnote\\remnote-6a7345f0a3f205110d2692d2\\remnote.db';

function run(sql) {
  return execSync(`sqlite3 "${dbPath}" "${sql}"`, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
}

console.log('--- key_value_store ---');
const kvs = run('SELECT * FROM key_value_store;').split('\n').filter(Boolean);
console.log('kvs count:', kvs.length);
kvs.forEach(k => console.log('  ', k.slice(0, 150)));

console.log('\n--- knowledge_base_data ---');
const kbd = run('SELECT * FROM knowledge_base_data;').split('\n').filter(Boolean);
console.log('kbd count:', kbd.length);
kbd.forEach(k => {
  try {
    const p = JSON.parse(k.split('|')[1]);
    console.log('  key:', p.key, 'value:', JSON.stringify(p.value).slice(0, 80));
  } catch (_) {
    console.log('  ', k.slice(0, 150));
  }
});

console.log('\n--- local_stored_data ---');
const lsd = run('SELECT * FROM local_stored_data;').split('\n').filter(Boolean);
console.log('lsd count:', lsd.length);
lsd.forEach(k => console.log('  ', k.slice(0, 150)));
