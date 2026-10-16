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

async function runPreFlight() {
  console.log('Launching headless browser:', executablePath);
  const browser = await chromium.launch({
    executablePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files']
  });

  const page = await browser.newPage({
    viewport: { width: 1440, height: 900 }
  });

  const errors = [];
  const warnings = [];

  page.on('pageerror', err => {
    errors.push(`PageError: ${err.message}`);
  });

  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(`ConsoleError: ${msg.text()}`);
    } else if (msg.type() === 'warning') {
      warnings.push(`ConsoleWarn: ${msg.text()}`);
    }
  });

  const fileUrl = 'file:///' + path.resolve(__dirname, '../academy.html').replace(/\\/g, '/');
  console.log('Navigating to:', fileUrl + '#/python/skill/1.1.1');
  await page.goto(fileUrl + '#/python/skill/1.1.1', { waitUntil: 'load' });
  await page.waitForTimeout(1000);

  const shotDir = path.resolve(__dirname, '../design_mockups');
  await page.screenshot({ path: path.join(shotDir, 'restored_skill_111_desktop.png') });
  console.log('Saved restored_skill_111_desktop.png');

  // Check dots-necklace presence
  const hasDots = await page.$('.dots-necklace');
  console.log('Has dots-necklace in DOM:', !!hasDots);

  // Switch to cards via jewel dot [data-py-select-f]
  console.log('Switching to cards via [data-py-select-f]...');
  await page.click('[data-py-select-f]');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(shotDir, 'restored_skill_cards_desktop.png') });
  console.log('Saved restored_skill_cards_desktop.png');

  // Switch to code practice via jewel dot [data-py-select-task]
  console.log('Switching to code via [data-py-select-task]...');
  await page.click('[data-py-select-task]');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(shotDir, 'restored_skill_code_desktop.png') });
  console.log('Saved restored_skill_code_desktop.png');

  // Test mobile viewport
  console.log('Testing mobile viewport 390x844...');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(fileUrl + '#/python/skill/1.1.1', { waitUntil: 'load' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(shotDir, 'restored_skill_111_mobile.png') });
  console.log('Saved restored_skill_111_mobile.png');

  await browser.close();

  console.log('-----------------------------------------');
  console.log('Zero-Error Pre-flight Check Summary:');
  console.log('Page errors:', errors.length);
  errors.forEach(e => console.log('  ❌', e));
  console.log('Warnings:', warnings.length);

  if (errors.length > 0) {
    process.exit(1);
  }
  console.log('Zero-Error Headless Chrome Pre-Flight 100% PERFECT (0 pageerror, 0 console.error)!');
}

runPreFlight().catch(err => {
  console.error(err);
  process.exit(1);
});
