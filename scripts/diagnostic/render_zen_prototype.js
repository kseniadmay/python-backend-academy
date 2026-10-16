const fs = require('fs');
const path = require('path');
const os = require('os');

const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');

function resolveDep(name) {
  try { return require(name); } catch (e) { /* дальше по списку */ }
  const p = path.join(DEPS_DIR, 'node_modules', name);
  if (fs.existsSync(p)) return require(p);
  return null;
}

const { chromium } = resolveDep('playwright-core');

const chromePaths = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
];

let executablePath = chromePaths.find(p => fs.existsSync(p));

async function render() {
  const browser = await chromium.launch({
    executablePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });

  const page = await browser.newPage({
    viewport: { width: 1440, height: 900 }
  });

  const fileUrl = 'file:///' + path.resolve(__dirname, '../design_mockups/zen_path_and_dashboard_prototype.html').replace(/\\/g, '/');
  console.log('Loading:', fileUrl);
  await page.goto(fileUrl, { waitUntil: 'load' });
  await page.waitForTimeout(600);

  const shotDir = path.resolve(__dirname, '../design_mockups');

  // Shot 1: Path Desktop
  await page.screenshot({ path: path.join(shotDir, 'zen_proto_path_desktop.png') });
  console.log('Saved zen_proto_path_desktop.png');

  // Shot 2: Dashboard Desktop
  await page.click('button:has-text("Дашборд")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(shotDir, 'zen_proto_dashboard_desktop.png') });
  console.log('Saved zen_proto_dashboard_desktop.png');

  // Shot 3: Mobile 390x844 Path
  await page.setViewportSize({ width: 390, height: 844 });
  await page.click('button:has-text("Экран «Путь»")');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(shotDir, 'zen_proto_path_mobile.png') });
  console.log('Saved zen_proto_path_mobile.png');

  await browser.close();
  console.log('All prototype screenshots taken successfully!');
}

render().catch(err => {
  console.error(err);
  process.exit(1);
});
