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
const PORT = 8898;

const ARTIFACT_DIR = path.normalize('C:/Users/fury6/.gemini/antigravity/brain/8bad31e5-2676-43cb-be75-4e08bd92f46f');
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

async function saveShot(page, fileName) {
  const p1 = path.join(ARTIFACT_DIR, fileName);
  const p2 = path.join(LOCAL_OUT_DIR, fileName);
  await page.screenshot({ path: p1 });
  fs.copyFileSync(p1, p2);
  console.log(`Saved screenshot: ${fileName}`);
}

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

    const page = await context.newPage();
    await page.goto(`http://localhost:${PORT}/academy.html#/cards`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);

    // 1. Действие 1: Старт сессии — Чтение вопроса карточки (лицевая сторона)
    console.log('Action 1: Question Front...');
    await saveShot(page, '01_srs_action_question_front.png');

    // 2. Действие 2: Раскрытие контекстного меню колоды и фильтров эшелонов
    console.log('Action 2: Deck Filter Details...');
    await page.click('.srs-deck-capsule-summary');
    await page.waitForTimeout(400);
    await saveShot(page, '02_srs_action_deck_selector.png');

    // Закрываем меню фильтров обратно
    await page.click('.srs-deck-capsule-summary');
    await page.waitForTimeout(300);

    // 3. Действие 3: Активация шпаргалки («Активное спасение» / Active Rescue Scaffold)
    console.log('Action 3: Active Rescue Hint...');
    await page.click('#srs-hint-btn');
    await page.waitForTimeout(500);
    await saveShot(page, '03_srs_action_rescue_hint.png');

    // Закрываем шпаргалку повторным кликом
    await page.click('#srs-hint-btn');
    await page.waitForTimeout(300);

    // 4. Действие 4: Фокус на кнопке действия «Показать ответ»
    console.log('Action 4: Show Answer Focus/Hover...');
    await page.hover('#btn-show-answer');
    await page.waitForTimeout(400);
    await saveShot(page, '04_srs_action_show_answer_focus.png');

    // 5. Действие 5: Переворот карточки и изучение ответа с кодом
    console.log('Action 5: Flipping card via click #btn-show-answer...');
    await page.click('#btn-show-answer');
    await page.waitForTimeout(600);
    await saveShot(page, '05_srs_action_answer_back.png');

    // 6. Действие 6: Оценка «Трудно (+2 XP)»
    console.log('Action 6: Rating Hard Hover...');
    await page.hover('.card-rating-btn--hard');
    await page.waitForTimeout(400);
    await saveShot(page, '06_srs_action_rating_hard.png');

    // 7. Действие 7: Оценка «Легко (+10 XP)»
    console.log('Action 7: Rating Easy Hover...');
    await page.hover('.card-rating-btn--easy');
    await page.waitForTimeout(400);
    await saveShot(page, '07_srs_action_rating_easy.png');

    // 8. Действие 8: Клик по оценке и переход к следующей карточке (продвижение по бусинам)
    console.log('Action 8: Clicking rating to advance to Card 2...');
    await page.click('.card-rating-btn--good');
    await page.waitForTimeout(600);
    await saveShot(page, '08_srs_action_next_card_progress.png');

    // 9. Действие 9: Дзен-экран завершения сессии повторения
    console.log('Action 9: Session Completed Screen...');
    await page.evaluate(() => {
      cardsHubState.completed = true;
      // Триггерим обновление через hashchange
      window.location.hash = '#/cards?status=done';
    });
    await page.waitForTimeout(600);
    await saveShot(page, '09_srs_action_session_completed.png');

    console.log('ALL_9_ACTIONS_CAPTURED_SUCCESSFULLY');
    await browser.close();
  } catch(err) {
    console.error('Error during capture:', err);
  } finally {
    server.close();
    process.exit(0);
  }
});
