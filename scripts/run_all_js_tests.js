const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const testDir = path.resolve(__dirname, '..', 'tests');
const files = fs.readdirSync(testDir).filter(f => f.endsWith('.js') && f.startsWith('test_'));

for(const file of files){
    try {
        console.log(`Running ${file}...`);
        const out = execSync(`node ${path.join(testDir, file)}`, { encoding: 'utf-8', cwd: path.resolve(__dirname, '..') });
        console.log(`  PASS: ${file}`);
    } catch(err) {
        console.log(`  FAIL: ${file} -> ${err.message.slice(0, 150)}`);
    }
}
