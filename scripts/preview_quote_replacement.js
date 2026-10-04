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

function isJsonBlock(lines) {
  const text = lines.map(l => l.trim()).filter(l => l.length > 0).join('\n');
  if (text.startsWith('{') && text.endsWith('}')) {
    try {
      JSON.parse(text);
      return true;
    } catch (e) {
      // maybe valid JSON with trailing commas or comments?
      if (/^\{\s*"[\w-]+":/.test(text)) return true;
    }
  }
  if (text.startsWith('[') && text.endsWith(']')) {
    try {
      JSON.parse(text);
      return true;
    } catch (e) {
      if (/^\[\s*"/.test(text)) return true;
    }
  }
  return false;
}

function replaceQuotesInCodeLine(line) {
  if (line.includes('"""') || line.includes("'''")) {
    return line;
  }
  if (/^\s*(CMD|ENTRYPOINT|VOLUME)\s*\[/.test(line)) {
    return line;
  }
  // Also keep HTML/XML attribute double quotes intact if detected
  if (/<[a-zA-Z0-9_-]+(\s+[^>]*)?>/.test(line) && line.includes('="')) {
    return line;
  }
  // Regex for double quoted strings
  const regex = /([rubfRUBF]{0,2})"((?:[^"\\]|\\.)*)"/g;

  return line.replace(regex, (match, prefix, content) => {
    // If inside content there is an unescaped single quote, keep double quotes
    if (/(?:[^\\]|^)'/.test(content)) {
      return match;
    }
    const newContent = content.replace(/\\"/g, '"');
    return `${prefix}'${newContent}'`;
  });
}

let modifiedCount = 0;
let diffSamples = [];

for (const f of files) {
  const content = fs.readFileSync(f, 'utf8');
  const lines = content.split(/\r?\n/);
  let inCode = false;
  let blockLines = [];
  let blockStartIdx = -1;
  let fileModified = false;
  
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim().startsWith('```')) {
      if (inCode) {
        // end of code block
        if (!isJsonBlock(blockLines)) {
          for (let b = 0; b < blockLines.length; b++) {
            const orig = blockLines[b];
            const replaced = replaceQuotesInCodeLine(orig);
            if (replaced !== orig) {
              lines[blockStartIdx + 1 + b] = replaced;
              fileModified = true;
              if (diffSamples.length < 20) {
                diffSamples.push({ file: path.basename(f), line: blockStartIdx + 1 + b + 1, before: orig, after: replaced });
              }
            }
          }
        }
        blockLines = [];
      } else {
        blockStartIdx = i;
      }
      inCode = !inCode;
      continue;
    }
    if (inCode) {
      blockLines.push(l);
    }
  }
  
  if (fileModified) {
    modifiedCount++;
  }
}

console.log('Total files:', files.length);
console.log('Files that will be modified:', modifiedCount);
console.log('\n--- 20 Sample Diffs: ---');
diffSamples.forEach(d => {
  console.log(`[${d.file}:${d.line}]`);
  console.log('  - ', d.before);
  console.log('  + ', d.after);
});
