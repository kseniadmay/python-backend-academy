const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const desktopBase = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям';
const downloadsBase = 'C:\\Users\\fury6\\Downloads\\База_знаний_по_модулям';
const desktopZip = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям.zip';
const downloadsZip = 'C:\\Users\\fury6\\Downloads\\База_знаний_Junior_Python_по_модулям.zip';

console.log('1. Syncing desktop folder to downloads folder...');
fs.cpSync(desktopBase, downloadsBase, { recursive: true, force: true });
console.log('   Sync complete.');

console.log('2. Updating 6 module zip archives inside desktop folder...');
const moduleDirs = fs.readdirSync(desktopBase, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name);

for (const mod of moduleDirs) {
  const modPath = path.join(desktopBase, mod);
  const zipPath = path.join(desktopBase, `${mod}.zip`);
  if (fs.existsSync(zipPath)) {
    fs.unlinkSync(zipPath);
  }
  console.log(`   Archiving module: ${mod}...`);
  // Use PowerShell Compress-Archive
  execSync(`powershell -Command "Compress-Archive -Path '${modPath}' -DestinationPath '${zipPath}' -Force"`);
}

console.log('3. Updating global zip archives...');
if (fs.existsSync(desktopZip)) fs.unlinkSync(desktopZip);
console.log('   Creating desktop global zip...');
execSync(`powershell -Command "Compress-Archive -Path '${desktopBase}' -DestinationPath '${desktopZip}' -Force"`);

console.log('   Copying to downloads global zip...');
fs.copyFileSync(desktopZip, downloadsZip);

console.log('All archives successfully updated!');
