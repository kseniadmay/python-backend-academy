const fs = require('fs');
const path = require('path');

const leveldbDir = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\IndexedDB\\https_www.remnote.com_0.indexeddb.leveldb';
const buf = fs.readFileSync(path.join(leveldbDir, '015130.ldb'));

// Search for Junior Python in buffer and extract surroundings
let offset = 0;
const needle = Buffer.from('Junior');
while (true) {
  const idx = buf.indexOf(needle, offset);
  if (idx === -1) break;
  const start = Math.max(0, idx - 100);
  const end = Math.min(buf.length, idx + 200);
  const slice = buf.subarray(start, end);
  // printable ascii + utf8
  console.log('--- MATCH AT', idx, '---');
  console.log(slice.toString('utf8').replace(/[^\x20-\x7E\u0400-\u04FF]/g, '.'));
  offset = idx + needle.length;
}
