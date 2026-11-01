'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
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

const playwright = resolveDep('playwright-core');
const ROOT = path.resolve(__dirname, '..');
const PORT = 8896;

const server = http.createServer((req, res) => {
  let reqPath = decodeURIComponent(req.url.split('?')[0]);
  if (reqPath === '/') reqPath = '/academy.html';
  const filePath = path.join(ROOT, reqPath);
  if (!fs.existsSync(filePath)) {
    res.statusCode = 404;
    res.end('Not found');
    return;
  }
  const ext = path.extname(filePath).toLowerCase();
  const mime = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml'
  }[ext] || 'application/octet-stream';
  res.setHeader('Content-Type', mime);
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, async () => {
  try {
    const browser = await playwright.chromium.launch({
      headless: true,
      channel: 'chrome'
    });

    const context = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 2
    });

    const ARTIFACT_DIR = path.normalize("C:/Users/fury6/.gemini/antigravity/brain/9476de61-b82f-4118-8a83-496832cde446");
    const outDir = path.join(__dirname, 'screenshots_output');
    [ARTIFACT_DIR, outDir].forEach(d => { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }); });

    const page = await context.newPage();

    await page.goto(`http://localhost:${PORT}/academy.html#/cards`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);

    // Задаем сессию повторения как у пользователя: очередь из 19 карточек колоды Ф-001, позиция 1 (Карточка 2)
    await page.evaluate(() => {
      cardsHubState.dueMode = true;
      cardsHubState.dueQueue = Array.from({length: 19}, (_, i) => ({deckId: 'Ф-001', cardIdx: i}));
      cardsHubState.duePos = 1;
      cardsHubState.completed = false;
      cardsHubState.flipped = false;
      if (typeof render === 'function') render();
    });
    await page.waitForTimeout(600);

    async function saveShot(fileName) {
      const p1 = path.join(ARTIFACT_DIR, fileName);
      const p2 = path.join(outDir, fileName);
      await page.screenshot({ path: p1 });
      fs.copyFileSync(p1, p2);
      console.log(`Saved ${fileName}`);
    }

    // 1. Десктоп лицо карточки
    await saveShot('cards_front_desktop.png');

    // 2. Десктоп переворот карточки
    await page.evaluate(() => {
      cardsHubState.flipped = true;
      if (typeof render === 'function') render();
    });
    await page.waitForTimeout(600);
    await saveShot('cards_back_desktop.png');

    // 3. Мобильный экран
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => {
      cardsHubState.flipped = false;
      if (typeof render === 'function') render();
    });
    await page.waitForTimeout(600);
    await saveShot('cards_front_mobile.png');

    // 4. Мобильный экран ответ
    await page.evaluate(() => {
      cardsHubState.flipped = true;
      if (typeof render === 'function') render();
    });
    await page.waitForTimeout(600);
    await saveShot('cards_back_mobile.png');

    await browser.close();
  } catch(err) {
    console.error('Error during screenshots:', err);
  } finally {
    server.close();
    process.exit(0);
  }
});
