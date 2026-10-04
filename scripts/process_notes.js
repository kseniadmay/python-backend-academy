const fs = require('fs');
const path = require('path');

const baseDir = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям';

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir, { withFileTypes: true });
  for (const item of list) {
    const full = path.join(dir, item.name);
    if (item.isDirectory()) {
      results = results.concat(walk(full));
    } else if (item.name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

const files = walk(baseDir);
console.log(`Processing ${files.length} markdown files in ${baseDir}...`);

let totalRemovedReps = 0;
let totalReplacedColons = 0;
let modifiedFilesCount = 0;

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const eol = content.includes('\r\n') ? '\r\n' : '\n';
  const lines = content.split(/\r?\n/);
  
  let fileModified = false;
  const newLines = [];
  
  for (const line of lines) {
    // Check if line is a "Было N повторений" line
    if (/^\s*-\s*Было\s+\d+\s+повторен/i.test(line)) {
      totalRemovedReps++;
      fileModified = true;
      continue; // exclude this line
    }
    
    // Check if line has "Перечитать конспект:"
    if (/(Перечитать\s+конспект)\s*:\s*/i.test(line)) {
      const newLine = line.replace(/(Перечитать\s+конспект)\s*:\s*/gi, '$1 ');
      if (newLine !== line) {
        totalReplacedColons++;
        fileModified = true;
        newLines.push(newLine);
        continue;
      }
    }
    
    newLines.push(line);
  }
  
  if (fileModified) {
    modifiedFilesCount++;
    fs.writeFileSync(file, newLines.join(eol), 'utf8');
  }
}

console.log(`Finished processing:`);
console.log(`- Files modified: ${modifiedFilesCount}`);
console.log(`- Repetition lines removed: ${totalRemovedReps}`);
console.log(`- Colons after 'Перечитать конспект' removed: ${totalReplacedColons}`);
