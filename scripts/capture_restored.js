
const puppeteer = require('puppeteer-core');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  const fileUrl = 'file:///' + path.resolve('academy.html').replace(/\\/g, '/') + '#/path';
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: 'design_mockups/restored_3d_path.png' });
  console.log('Saved design_mockups/restored_3d_path.png');

  const skillUrl = 'file:///' + path.resolve('academy.html').replace(/\\/g, '/') + '#/python/skill/1.1.1';
  await page.goto(skillUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: 'design_mockups/restored_skill_111.png' });
  console.log('Saved design_mockups/restored_skill_111.png');

  await browser.close();
})();
