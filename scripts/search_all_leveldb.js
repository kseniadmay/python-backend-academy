const fs = require('fs');
const path = require('path');

const leveldbDir = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\IndexedDB\\https_www.remnote.com_0.indexeddb.leveldb';
const files = fs.readdirSync(leveldbDir).filter(f => f.endsWith('.log') || f.endsWith('.ldb'));

for (const f of files) {
  const buf = fs.readFileSync(path.join(leveldbDir, f));
  if (buf.includes('GwREY') || buf.includes('PyeAB')) {
    console.log(`FOUND ID IN ${f}!`);
  }
}
