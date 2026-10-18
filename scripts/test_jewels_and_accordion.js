/**
 * test_jewels_and_accordion.js
 * Автоматический Playwright-тест для проверки:
 * 1. Изолированного наведения на 13 бусин трекера (Zone 2) без паразитного перекрытия (13 из 13 PASS)
 * 2. Надёжного закрытия и открытия аккордеона (Zone 4) по шапке и по нижней кнопке
 */

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

const { chromium } = resolveDep('playwright-core') || require('playwright-core');

function findBrowser() {
  const candidates = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  const pwCache = path.join(process.env.LOCALAPPDATA || '', 'ms-playwright');
  if (fs.existsSync(pwCache)) {
    for (const d of fs.readdirSync(pwCache)) {
      const exe = path.join(pwCache, d, 'chrome-win', 'chrome.exe');
      if (fs.existsSync(exe)) return exe;
    }
  }
  return candidates[0];
}

(async () => {
  console.log('Запуск браузера для Playwright-тестирования...');
  const browserPath = findBrowser();
  assert(fs.existsSync(browserPath), 'Браузер не найден: ' + browserPath);

  const browser = await chromium.launch({
    executablePath: browserPath,
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files']
  });

  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const fileUrl = 'file:///' + HTML_FILE.replace(/\\/g, '/');
  await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1000);

  console.log('\n--- ТЕСТ 1: Проверка 13 бусин ожерелья трекера (Zone 2) ---');
  // Найдём все 13 бусин в кластерах дашборда
  const dotsLocator = page.locator('.tracker-cluster-dots .dot-jewel');
  const dotsCount = await dotsLocator.count();
  console.log(`Найдено бусин: ${dotsCount}`);
  assert.strictEqual(dotsCount, 13, `Ожидалось ровно 13 бусин, найдено: ${dotsCount}`);

  let passedDots = 0;
  for (let i = 0; i < dotsCount; i++) {
    const dot = dotsLocator.nth(i);
    const box = await dot.boundingBox();
    assert(box, `Бусина #${i+1} не имеет boundingBox`);

    // Наводим курсор точно в центр бусины
    const cx = box.x + box.width / 2;
    const cy = box.y + box.height / 2;
    await page.mouse.move(cx, cy);
    await page.waitForTimeout(100);

    // Проверяем, какой элемент под курсором
    const hoverInfo = await page.evaluate(({ cx, cy, i }) => {
      const el = document.elementFromPoint(cx, cy);
      const allDots = Array.from(document.querySelectorAll('.tracker-cluster-dots .dot-jewel'));
      const targetDot = allDots[i];
      const isTarget = (el === targetDot || targetDot.contains(el));
      
      // Проверяем matches(':hover') для всех бусин
      const hoveredIndices = [];
      allDots.forEach((d, idx) => {
        if (d.matches(':hover')) hoveredIndices.push(idx);
      });

      return {
        isTarget,
        hoveredIndices,
        elTag: el ? el.tagName : null,
        elClass: el ? el.className : null
      };
    }, { cx, cy, i });

    if (hoverInfo.isTarget && hoverInfo.hoveredIndices.length === 1 && hoverInfo.hoveredIndices[0] === i) {
      console.log(`Бусина #${i+1}: PASS (строго бусина #${i+1} получила :hover)`);
      passedDots++;
    } else {
      console.error(`Бусина #${i+1}: FAIL! Под курсором: ${hoverInfo.elTag}.${hoverInfo.elClass}, :hover получили бусины: ${JSON.stringify(hoverInfo.hoveredIndices)}`);
    }
  }

  console.log(`\nРезультат проверки бусин: ${passedDots} из 13 PASS!`);
  assert.strictEqual(passedDots, 13, 'Не все 13 бусин прошли тест на изолированный hover!');

  console.log('\n--- ТЕСТ 2: Проверка закрытия и открытия аккордеона тем (Zone 4) ---');
  const accordion = page.locator('.dash-accordion');
  const summary = page.locator('.dash-accordion-summary');
  const collapseBtn = page.locator('[data-collapse-dash-accordion]');

  // 1. Убедимся, что аккордеон открыт
  const isInitiallyOpen = await accordion.evaluate(el => el.hasAttribute('open'));
  if (!isInitiallyOpen) {
    console.log('Аккордеон был закрыт, открываем кликом по summary...');
    await summary.click();
    await page.waitForTimeout(200);
  }
  const isOpenAfterPrep = await accordion.evaluate(el => el.hasAttribute('open'));
  assert.strictEqual(isOpenAfterPrep, true, 'Аккордеон должен быть открыт перед проверкой закрытия');
  console.log('✓ Аккордеон открыт');

  // 2. Закрытие по нижней кнопке [data-collapse-dash-accordion]
  console.log('Кликаем по нижней кнопке "Свернуть темы модуля"...');
  await collapseBtn.click();
  await page.waitForTimeout(200);

  const isOpenAfterCollapse = await accordion.evaluate(el => el.hasAttribute('open'));
  const stateOpen1 = await page.evaluate(() => window.state ? window.state.dashAccordionOpen : null);
  console.log(`Состояние после нижней кнопки: open=${isOpenAfterCollapse}, state.dashAccordionOpen=${stateOpen1}`);
  assert.strictEqual(isOpenAfterCollapse, false, 'Аккордеон обязан закрыться после клика по нижней кнопке!');
  assert.strictEqual(stateOpen1, false, 'state.dashAccordionOpen обязан стать false!');
  console.log('✓ Закрытие по нижней кнопке успешно подтверждено!');

  // 3. Открытие по клику на summary
  console.log('Кликаем по summary для открытия...');
  await summary.click();
  await page.waitForTimeout(200);

  const isOpenAfterSummaryOpen = await accordion.evaluate(el => el.hasAttribute('open'));
  const stateOpen2 = await page.evaluate(() => window.state ? window.state.dashAccordionOpen : null);
  console.log(`Состояние после клика по summary: open=${isOpenAfterSummaryOpen}, state.dashAccordionOpen=${stateOpen2}`);
  assert.strictEqual(isOpenAfterSummaryOpen, true, 'Аккордеон обязан открыться после клика по summary!');
  assert.strictEqual(stateOpen2, true, 'state.dashAccordionOpen обязан стать true!');
  console.log('✓ Открытие по summary успешно подтверждено!');

  // 4. Закрытие по повторному клику на summary
  console.log('Кликаем по summary для закрытия...');
  await summary.click();
  await page.waitForTimeout(200);

  const isOpenAfterSummaryClose = await accordion.evaluate(el => el.hasAttribute('open'));
  const stateOpen3 = await page.evaluate(() => window.state ? window.state.dashAccordionOpen : null);
  console.log(`Состояние после второго клика по summary: open=${isOpenAfterSummaryClose}, state.dashAccordionOpen=${stateOpen3}`);
  assert.strictEqual(isOpenAfterSummaryClose, false, 'Аккордеон обязан закрыться после повторного клика по summary!');
  assert.strictEqual(stateOpen3, false, 'state.dashAccordionOpen обязан стать false!');
  console.log('✓ Закрытие по summary успешно подтверждено!');

  await browser.close();
  console.log('\n======================================================');
  console.log('   ВСЕ ТЕСТЫ PLAYWRIGHT УСПЕШНО ПРОЙДЕНЫ (100% PASS)  ');
  console.log('======================================================');
})().catch(err => {
  console.error('\nОШИБКА В ТЕСТЕ:', err);
  process.exit(1);
});
