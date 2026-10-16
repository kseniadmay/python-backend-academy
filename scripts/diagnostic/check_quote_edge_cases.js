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

let nonPythonSnippets = [];
let tripleQuotes = [];
let innerSingleQuotes = [];

for (const f of files) {
  const content = fs.readFileSync(f, 'utf8');
  const lines = content.split(/\r?\n/);
  let inCode = false;
  let codeLines = [];
  
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim().startsWith('```')) {
      if (inCode) {
        // analyze code block
        const block = codeLines.join('\n');
        if (block.includes('"""')) {
          tripleQuotes.push({ file: path.basename(f), line: i });
        }
        if (block.includes('Dockerfile') || block.includes('docker run') || block.includes('CMD [') || block.includes('ENTRYPOINT [')) {
          nonPythonSnippets.push({ file: path.basename(f), reason: 'docker', sample: block.slice(0, 80) });
        }
        if (block.trim().startsWith('{') || block.trim().startsWith('[')) {
          // might be json
          if (block.includes('":')) {
            nonPythonSnippets.push({ file: path.basename(f), reason: 'json', sample: block.slice(0, 80) });
          }
        }
        codeLines = [];
      }
      inCode = !inCode;
      continue;
    }
    if (inCode) {
      codeLines.push(l);
      // check if line has "..." containing '
      const match = l.match(/"([^"\\]*(\\.[^"\\]*)*)"/g);
      if (match) {
        for (const m of match) {
          if (m.includes("'")) {
            innerSingleQuotes.push({ file: path.basename(f), line: l });
          }
        }
      }
    }
  }
}

console.log('Triple quotes count:', tripleQuotes.length);
console.log('Inner single quotes count:', innerSingleQuotes.length);
console.log('Sample inner single quotes:', innerSingleQuotes.slice(0, 5));
console.log('Non-python / JSON / Docker snippets count:', nonPythonSnippets.length);
console.log('Sample non-python:', nonPythonSnippets.slice(0, 5));
