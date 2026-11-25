'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

const ROOT = path.resolve(__dirname, '..');
const HTML_FILE = path.join(ROOT, 'academy.html');
const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');

function resolveDep(name) {
  try { return require(name); } catch (e) {}
  const p = path.join(DEPS_DIR, 'node_modules', name);
  if (fs.existsSync(p)) return require(p);
  return null;
}

const { chromium, devices } = resolveDep('playwright-core') || require('playwright-core');

function findBrowser() {
  const candidates = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  return candidates[0];
}

(async () => {
  const browser = await chromium.launch({
    executablePath: findBrowser(),
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files']
  });

  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const fileUrl = 'file:///' + HTML_FILE.replace(/\\/g, '/');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  // Set accordion open initially as in user screenshot
  await page.evaluate(() => {
    const acc = document.querySelector('.dash-accordion');
    if (acc) {
      acc.setAttribute('open', '');
      if (window.state) window.state.dashAccordionOpen = true;
    }
  });

  console.log('--- Desktop test ---');
  let isOpen = await page.evaluate(() => document.querySelector('.dash-accordion').hasAttribute('open'));
  console.log('Initially open:', isOpen);

  // Now click collapse button at bottom
  console.log('Clicking .dash-accordion-collapse-btn...');
  await page.click('.dash-accordion-collapse-btn');
  await page.waitForTimeout(300);

  isOpen = await page.evaluate(() => document.querySelector('.dash-accordion').hasAttribute('open'));
  console.log('Open after collapseBtn click:', isOpen);

  // Now open it again
  console.log('Clicking summary to reopen...');
  await page.click('.dash-accordion-summary');
  await page.waitForTimeout(300);
  isOpen = await page.evaluate(() => document.querySelector('.dash-accordion').hasAttribute('open'));
  console.log('Open after summary click:', isOpen);

  // Now click summary to close it!
  console.log('Clicking summary to close...');
  await page.click('.dash-accordion-summary');
  await page.waitForTimeout(300);
  isOpen = await page.evaluate(() => document.querySelector('.dash-accordion').hasAttribute('open'));
  console.log('Open after summary close click:', isOpen);

  await browser.close();
})();
