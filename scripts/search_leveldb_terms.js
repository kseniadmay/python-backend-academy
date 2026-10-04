const fs = require('fs');
const path = require('path');

const leveldbDir = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\IndexedDB\\https_www.remnote.com_0.indexeddb.leveldb';
const files = fs.readdirSync(leveldbDir);

for (const file of files) {
  const filePath = path.join(leveldbDir, file);
  const buf = fs.readFileSync(filePath);
  const str = buf.toString('binary');
  
  if (str.includes('GwREY') || str.includes('PyeAB')) {
    console.log(`Found GwREY in ${file}`);
  }
  if (buf.includes(Buffer.from('Junior-Python', 'utf8')) || buf.includes(Buffer.from('Junior+ Python', 'utf8'))) {
    console.log(`Found Junior Python in ${file}`);
  }
}
