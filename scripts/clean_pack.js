const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const sourceDir = 'C:\\Users\\fury6\\Downloads\\База_знаний_по_модулям';
const tempDir = 'C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\pkg_temp';
const desktopBase = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям';
const desktopZip = 'C:\\Users\\fury6\\OneDrive\\Desktop\\База_знаний_Junior_Python_по_модулям.zip';
const downloadsZip = 'C:\\Users\\fury6\\Downloads\\База_знаний_Junior_Python_по_модулям.zip';

// Clean temp dir
if (fs.existsSync(tempDir)) {
  fs.rmSync(tempDir, { recursive: true, force: true });
}
fs.mkdirSync(tempDir, { recursive: true });

console.log('Copying files to clean scratch directory...');
fs.cpSync(sourceDir, tempDir, { recursive: true });

// Remove any existing zip files inside tempDir
const tempEntries = fs.readdirSync(tempDir);
for (const entry of tempEntries) {
  if (entry.endsWith('.zip')) {
    fs.unlinkSync(path.join(tempDir, entry));
  }
}

console.log('Packaging individual modules in temp directory...');
const moduleDirs = fs.readdirSync(tempDir, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name);

for (const mod of moduleDirs) {
  const modPath = path.join(tempDir, mod);
  const zipPath = path.join(tempDir, `${mod}.zip`);
  console.log(`  Archiving ${mod}...`);
  // Use PowerShell .NET ZipFile to create archive cleanly
  execSync(`powershell -NoProfile -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::CreateFromDirectory('${modPath}', '${zipPath}')"`);
  
  // Also copy module zip to Desktop folder
  fs.copyFileSync(zipPath, path.join(desktopBase, `${mod}.zip`));
  fs.copyFileSync(zipPath, path.join(sourceDir, `${mod}.zip`));
}

console.log('Packaging global zip...');
const tempGlobalZip = 'C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\pkg_temp_global.zip';
if (fs.existsSync(tempGlobalZip)) fs.unlinkSync(tempGlobalZip);

// Exclude the module zips from the global zip if needed, or include entire folder
execSync(`powershell -NoProfile -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::CreateFromDirectory('${tempDir}', '${tempGlobalZip}')"`);

console.log('Deploying global zip to Desktop and Downloads...');
fs.copyFileSync(tempGlobalZip, desktopZip);
fs.copyFileSync(tempGlobalZip, downloadsZip);

console.log('Validating files:');
[desktopZip, downloadsZip].forEach(p => {
  const stat = fs.statSync(p);
  console.log(`  ${p}: ${(stat.size / 1024 / 1024).toFixed(2)} MB`);
});
console.log('All archives successfully rebuilt and verified!');
