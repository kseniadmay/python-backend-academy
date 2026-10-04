const { execSync } = require('child_process');
const fs = require('fs');

const dbPath = 'C:\\Users\\fury6\\remnote\\remnote-6a7345f0a3f205110d2692d2\\remnote.db';

function querySql(sql) {
  const res = execSync(`sqlite3 "${dbPath}" "${sql.replace(/"/g, '""')}"`, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  return res.trim().split('\n').filter(Boolean);
}

console.log('--- Checking knowledge_base_data: ---');
try {
  const kb = querySql('SELECT doc FROM knowledge_base_data;');
  kb.forEach(k => {
    const obj = JSON.parse(k);
    console.log('KB Data keys:', Object.keys(obj));
    if (obj.defaultSchedulerId) console.log('defaultSchedulerId:', obj.defaultSchedulerId);
    if (obj.settings) console.log('settings:', obj.settings);
  });
} catch (e) {
  console.log('Error:', e.message);
}

console.log('\n--- Checking user_data: ---');
try {
  const ud = querySql('SELECT doc FROM user_data;');
  ud.forEach(u => {
    const obj = JSON.parse(u);
    console.log('User Data keys:', Object.keys(obj));
    if (obj.selectedSchedulerId) console.log('selectedSchedulerId:', obj.selectedSchedulerId);
    if (obj.installedPlugins) console.log('installedPlugins:', obj.installedPlugins);
  });
} catch (e) {
  console.log('Error:', e.message);
}

console.log('\n--- Checking plugins in quanta: ---');
try {
  // Search for plugins in quanta
  const plugins = querySql("SELECT id, substr(doc, 1, 300) FROM quanta WHERE doc LIKE '%plugin%' LIMIT 20;");
  console.log(`Found ${plugins.length} quanta with 'plugin':`);
  plugins.forEach(p => console.log('  ', p));
} catch (e) {
  console.log('Error:', e.message);
}
