'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const assert = require('assert');

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

  console.log('Testing mobile emulation (iPhone 12)...');
  const context = await browser.newContext({
    ...devices['iPhone 12'],
  });
  const page = await context.newPage();

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));

  const fileUrl = 'file:///' + HTML_FILE.replace(/\\/g, '/');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const acc = page.locator('.dash-accordion');
  const summary = page.locator('.dash-accordion-summary');
  const collapseBtn = page.locator('.dash-accordion-collapse-btn');

  console.log('Initial details open attribute:', await acc.evaluate(el => el.getAttribute('open')));

  console.log('Clicking summary to open...');
  await summary.tap();
  await page.waitForTimeout(300);
  console.log('After summary tap, details open attribute:', await acc.evaluate(el => el.getAttribute('open')));

  console.log('Clicking collapse button (tap)...');
  await collapseBtn.tap();
  await page.waitForTimeout(300);
  console.log('After collapseBtn tap, details open attribute:', await acc.evaluate(el => el.getAttribute('open')));

  console.log('Testing click via dispatchEvent or touch...');
  await summary.click();
  await page.waitForTimeout(300);
  console.log('After summary click, details open:', await acc.evaluate(el => el.getAttribute('open')));
  await collapseBtn.click();
  await page.waitForTimeout(300);
  console.log('After collapseBtn click, details open:', await acc.evaluate(el => el.getAttribute('open')));

  await browser.close();
})();
