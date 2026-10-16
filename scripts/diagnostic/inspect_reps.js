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
console.log('Total files found:', files.length);

for (const f of files) {
  const content = fs.readFileSync(f, 'utf8');
  if (/было\s+\d*\s*повторен/i.test(content)) {
    console.log('\n--- File:', f);
    const lines = content.split(/\r?\n/);
    lines.forEach((l, i) => {
      if (/было\s+\d*\s*повторен/i.test(l)) {
        console.log(`Line ${i+1}: [${l}]`);
        console.log('Context:');
        console.log(lines.slice(Math.max(0, i - 2), i + 3).map((x, j) => `  ${i - 2 + j + 1}: ${x}`).join('\n'));
      }
    });
    break; // just check one file
  }
}
