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
const PORT = 8899;

const ARTIFACT_DIR = path.normalize("C:/Users/fury6/.gemini/antigravity/brain/cf3546c7-fc77-498e-bc60-61304497ea18");
const LOCAL_OUT_DIR = path.join(ROOT, 'scripts', 'screenshots_output');

[ARTIFACT_DIR, LOCAL_OUT_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

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

async function saveElementShot(element, fileName) {
  if (!element) return;
  const p1 = path.join(ARTIFACT_DIR, fileName);
  const p2 = path.join(LOCAL_OUT_DIR, fileName);
  await element.screenshot({ path: p1 });
  fs.copyFileSync(p1, p2);
  console.log(`Saved element shot: ${fileName}`);
}

async function savePageShot(page, fileName) {
  const p1 = path.join(ARTIFACT_DIR, fileName);
  const p2 = path.join(LOCAL_OUT_DIR, fileName);
  await page.screenshot({ path: p1 });
  fs.copyFileSync(p1, p2);
  console.log(`Saved page shot: ${fileName}`);
}

server.listen(PORT, async () => {
  try {
    const browser = await playwright.chromium.launch({
      headless: true,
      channel: 'chrome'
    });

    const context = await browser.newContext({
      viewport: { width: 1440, height: 920 },
      deviceScaleFactor: 2
    });

    const page = await context.newPage();
    await page.goto(`http://localhost:${PORT}/academy.html#/cards`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);

    // 1. Снимок: Полный экран десктоп - Фаза 1 (Вопрос)
    await savePageShot(page, '01_full_desktop_phase1.png');

    // 2. Снимок: Левый сайдбар (.sidebar)
    const sidebar = await page.$('.sidebar');
    await saveElementShot(sidebar, '02_sidebar.png');

    // 3. Снимок: Верхняя панель Уровень 1 (.srs-unified-header-bar)
    const headerBar = await page.$('.srs-unified-header-bar');
    await saveElementShot(headerBar, '03_header_bar.png');

    // 4. Снимок: Контекстная строка Уровень 2 (.srs-deck-beads-bar: капсула колоды + бусины + счетчик)
    const deckBeadsBar = await page.$('.srs-deck-beads-bar');
    await saveElementShot(deckBeadsBar, '04_deck_beads_bar.png');

    // 5. Снимок: Карточка - лицевая сторона (.fc-card)
    const cardFront = await page.$('.fc-card');
    await saveElementShot(cardFront, '05_card_front.png');

    // 6. Снимок: Нижний док действий - Фаза 1 (.srs-action-dock, строго кнопка «Показать ответ»)
    const dockPhase1 = await page.$('.srs-action-dock');
    await saveElementShot(dockPhase1, '06_dock_phase1_cta.png');

    // ПЕРЕВОРОТ КАРТОЧКИ: Кликаем по кнопке «Показать ответ»
    console.log('Flipping card via click #btn-show-answer...');
    await page.click('#btn-show-answer');
    await page.waitForTimeout(500);

    // 7. Снимок: Карточка - оборотная сторона (.fc-card с ответом)
    const cardBack = await page.$('.fc-card');
    await saveElementShot(cardBack, '07_card_back.png');

    // 8. Снимок: Нижний док действий - Фаза 2 (.srs-action-dock: Трудно [1], Хорошо [2], Легко [3])
    const dockPhase2 = await page.$('.srs-action-dock');
    await saveElementShot(dockPhase2, '08_dock_phase2_ratings.png');

    // 9. Снимок: Полный экран десктоп - Фаза 2 (Ответ)
    await savePageShot(page, '09_full_desktop_phase2.png');

    console.log('SUCCESS: Exactly 9 verification screenshots saved!');
    await browser.close();
  } catch(err) {
    console.error('Error during capture:', err);
  } finally {
    server.close();
    process.exit(0);
  }
});
