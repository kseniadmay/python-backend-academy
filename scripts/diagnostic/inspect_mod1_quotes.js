const fs = require('fs');
const path = require('path');

const mod1 = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям\\01 · 🐍 Python Core & Advanced';

const files = fs.readdirSync(mod1).filter(f => f.endsWith('.md')).map(f => path.join(mod1, f));

console.log('Module 1 files:', files.length);

for (const f of files) {
  const content = fs.readFileSync(f, 'utf8');
  const lines = content.split(/\r?\n/);
  let inCode = false;
  let codeDbl = [];
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim().startsWith('```')) {
      inCode = !inCode;
      continue;
    }
    if (inCode && l.includes('"')) {
      codeDbl.push({ lineNum: i+1, line: l });
    }
  }
  if (codeDbl.length > 0) {
    console.log(`\nFile: ${path.basename(f)} (${codeDbl.length} lines with ")`);
    codeDbl.slice(0, 3).forEach(x => console.log(`  L${x.lineNum}: ${x.line}`));
  }
}
