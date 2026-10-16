const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const baseDir = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям';
const downloadsBase = 'C:\\Users\\fury6\\Downloads\\База_знаний_по_модулям';
const desktopZip = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям.zip';
const downloadsZip = 'C:\\Users\\fury6\\Downloads\\База_знаний_Junior_Python_по_модулям.zip';

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
  // Keep HTML/XML attribute double quotes intact
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

let modifiedFiles = 0;

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  const eol = content.includes('\r\n') ? '\r\n' : '\n';
  let fileChanged = false;

  // Specific fix for file 05: remove buggy ternary swap line
  if (path.basename(file) === '05. args kwargs и распаковка в Python.md') {
    if (content.includes('x, y = y, x if False else (1, 2)')) {
      content = content.replace(
        'x, y = y, x if False else (1, 2)  # распаковка используется и для swap:\r\na, b = 1, 2\r\na, b = b, a                     # обмен значениями без временной переменной',
        '# распаковка используется и для swap (обмен значениями без временной переменной):\r\na, b = 1, 2\r\na, b = b, a'
      );
      content = content.replace(
        'x, y = y, x if False else (1, 2)  # распаковка используется и для swap:\na, b = 1, 2\na, b = b, a                     # обмен значениями без временной переменной',
        '# распаковка используется и для swap (обмен значениями без временной переменной):\na, b = 1, 2\na, b = b, a'
      );
      fileChanged = true;
    }
  }

  const lines = content.split(/\r?\n/);
  let inCode = false;
  let blockLines = [];
  let blockStartIdx = -1;

  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim().startsWith('```')) {
      if (inCode) {
        // End of code block
        if (!isJsonBlock(blockLines)) {
          for (let b = 0; b < blockLines.length; b++) {
            const orig = blockLines[b];
            const replaced = replaceQuotesInCodeLine(orig);
            if (replaced !== orig) {
              lines[blockStartIdx + 1 + b] = replaced;
              fileChanged = true;
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

  if (fileChanged) {
    fs.writeFileSync(file, lines.join(eol), 'utf8');
    modifiedFiles++;
  }
}

console.log(`Updated ${modifiedFiles} files.`);

console.log('Syncing desktop to downloads...');
fs.cpSync(baseDir, downloadsBase, { recursive: true, force: true });

console.log('Re-creating module zip archives...');
const moduleDirs = fs.readdirSync(baseDir, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name);

for (const mod of moduleDirs) {
  const modPath = path.join(baseDir, mod);
  const zipPath = path.join(baseDir, `${mod}.zip`);
  if (fs.existsSync(zipPath)) fs.unlinkSync(zipPath);
  execSync(`powershell -Command "Compress-Archive -Path '${modPath}' -DestinationPath '${zipPath}' -Force"`);
}

console.log('Re-creating desktop and downloads global zip archives...');
if (fs.existsSync(desktopZip)) fs.unlinkSync(desktopZip);
execSync(`powershell -Command "Compress-Archive -Path '${baseDir}' -DestinationPath '${desktopZip}' -Force"`);
fs.copyFileSync(desktopZip, downloadsZip);

console.log('Done!');
