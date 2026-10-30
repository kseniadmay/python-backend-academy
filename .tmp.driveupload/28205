'use strict';
const path = require('path');
const fs = require('fs');
const { resolveDep, findBrowser, VIEWPORTS } = require('./visual_test');

async function capture() {
  const pw = resolveDep('playwright-core');
  if (!pw) {
    throw new Error('playwright-core is not installed');
  }
  const { chromium } = pw;

  const browser = await chromium.launch({
    executablePath: findBrowser(),
    headless: true
  });

  const outDir = path.join(__dirname, 'visual_report');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const htmlUrl = 'file://' + path.resolve(__dirname, '..', 'academy.html') + '#/python/skill/1.9.1';

  // 1. Mobile viewport (390x844 - iPhone 14)
  const mobileContext = await browser.newContext(VIEWPORTS.mobile);
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(htmlUrl, { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(1000);

  const mobPath1 = path.join(outDir, 'skill_1_9_1_quantized_step0_mobile.png');
  await mobilePage.screenshot({ path: mobPath1, fullPage: false });
  console.log('Saved mobile screenshot:', mobPath1);

  // 2. Desktop viewport (1440x900)
  const desktopContext = await browser.newContext(VIEWPORTS.desktop);
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

if (require.main === module) {
  capture().catch(err => {
    console.error('Capture error:', err);
    process.exit(1);
  });
}

module.exports = { capture };
