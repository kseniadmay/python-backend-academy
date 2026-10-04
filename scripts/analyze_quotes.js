const fs = require('fs');
const path = require('path');

const baseDir = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям';

function walk(dir) {
  let res = [];
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, item.name);
    if (item.isDirectory()) res = res.concat(walk(full));
    else if (item.name.endsWith('.md')) res.push(full);
  }
  return res;
}

const files = walk(baseDir);
let filesWithDoubleQuotesInCode = 0;
let totalBlocks = 0;
let sampleOccurrences = [];

for (const f of files) {
  const content = fs.readFileSync(f, 'utf8');
  const lines = content.split(/\r?\n/);
  let inCode = false;
  let fileHasDbl = false;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim().startsWith('```')) {
      inCode = !inCode;
      if (inCode) totalBlocks++;
      continue;
    }
    if (inCode && l.includes('"')) {
      fileHasDbl = true;
      if (sampleOccurrences.length < 10) {
        sampleOccurrences.push({ file: path.basename(f), lineNum: i + 1, line: l });
      }
    }
  }
  if (fileHasDbl) filesWithDoubleQuotesInCode++;
}

console.log('Total files:', files.length);
console.log('Total code blocks:', totalBlocks);
console.log('Files with double quotes in code blocks:', filesWithDoubleQuotesInCode);
console.log('Sample occurrences:', sampleOccurrences);
