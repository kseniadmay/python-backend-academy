const fs = require('fs');
const path = require('path');

const leveldbDir = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\IndexedDB\\https_www.remnote.com_0.indexeddb.leveldb';
const files = fs.readdirSync(leveldbDir);
const targetId = 'GwREY4bq5eQvPyeAB';

let readOk = 0;
let errors = 0;

for (const file of files) {
  const filePath = path.join(leveldbDir, file);
  try {
    const buf = fs.readFileSync(filePath);
    readOk++;
    if (buf.includes(targetId)) {
      console.log(`MATCH in ${file}! Size: ${buf.length}`);
    }
    if (buf.includes('69d8425df107d8b00ed6ddb9')) {
      console.log(`Found workspace ID 69d8425df107d8b00ed6ddb9 in ${file}`);
    }
  } catch (e) {
    errors++;
  }
}
console.log(`Read ok: ${readOk}, errors: ${errors}`);
