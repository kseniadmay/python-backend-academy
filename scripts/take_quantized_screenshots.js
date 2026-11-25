const path = require('path');
const fs = require('fs');
const os = require('os');

const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');

function resolveDep(name) {
  try { return require(name); } catch (e) {}
  const candidates = [
    path.join(DEPS_DIR, 'node_modules', name),
    path.join(os.homedir(), '.pba-visual-deps', 'node_modules', name),
    path.join(os.homedir(), '.pba-visual-deps', 'pba-visual-deps', 'node_modules', name)
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) return require(p);
  }
  return null;
}

const { chromium } = resolveDep('playwright-core');

async function capture() {
  const browser = await chromium.launch({
    executablePath: '/Users/fury/Library/Caches/ms-playwright/chromium-1148/chrome-mac/Chromium.app/Contents/MacOS/Chromium',
    headless: true
  });

  const outDir = path.join(__dirname, 'visual_report');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const htmlUrl = 'file://' + path.resolve(__dirname, '..', 'academy.html') + '#/python/skill/1.9.1';

  // 1. Mobile viewport (390x844 - iPhone 14)
  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(htmlUrl, { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(1000);

  const mobPath1 = path.join(outDir, 'skill_1_9_1_quantized_step0_mobile.png');
  await mobilePage.screenshot({ path: mobPath1, fullPage: false });
  console.log('Saved mobile screenshot:', mobPath1);

  // 2. Desktop viewport (1440x900)
  const desktopContext = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });
  const desktopPage = await desktopContext.newPage();
  await desktopPage.goto(htmlUrl, { waitUntil: 'networkidle' });
  await desktopPage.waitForTimeout(1000);

  const deskPath1 = path.join(outDir, 'skill_1_9_1_quantized_step0_desktop.png');
  await desktopPage.screenshot({ path: deskPath1, fullPage: false });
  console.log('Saved desktop screenshot:', deskPath1);

  // 3. Navigate to K-220 (Logging) step 1 (where the 28-line code was atomized)
  await desktopPage.evaluate(() => {
    location.hash = '#/python/skill/1.9.1';
    window.pySkillViewState = { sid: '1.9.1', kId: 'К-220', stepIdx: 1, chunkIdx: 0, tab: 'theory' };
    if (typeof renderApp === 'function') renderApp();
  });
  await desktopPage.waitForTimeout(800);
  const deskPath2 = path.join(outDir, 'skill_1_9_1_quantized_logging_desktop.png');
  await desktopPage.screenshot({ path: deskPath2, fullPage: false });
  console.log('Saved logging screenshot:', deskPath2);

  await browser.close();
}

capture().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
