/* Разведочные скриншоты #/path (текущее рабочее дерево, file://-режим песочницы).
 * Запуск: node scripts/_tropa_recon.js
 * Выход: scripts/visual_report/tropa_recon/*.png + сводка JS-ошибок в консоль.
 */
const fs = require('fs');
const path = require('path');
const os = require('os');
const { pathToFileURL } = require('url');

const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');
function resolveDep(name) {
  try { return require(name); } catch (e) { /* дальше */ }
  const p = path.join(DEPS_DIR, 'node_modules', name);
  if (fs.existsSync(p)) return require(p);
  return null;
}
const pw = resolveDep('playwright-core');
if (!pw) throw new Error('playwright-core не найден в ' + DEPS_DIR);

function findBrowser() {
  const candidates = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe'
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  throw new Error('Не найден Chrome/Edge');
}

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'scripts', 'visual_report', 'tropa_recon');
fs.mkdirSync(OUT, { recursive: true });
const URL_BASE = pathToFileURL(path.join(ROOT, 'academy.html')).href;

async function newPage(browser, ctxOpts) {
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }, ctxOpts || {}));
  const page = await ctx.newPage();
  return { ctx, page };
}

(async () => {
  const browser = await pw.chromium.launch({ executablePath: findBrowser(), headless: true });
  const errors = [];
  const shots = [];

  async function snap(name, { viewport, seed, actions }) {
    const { ctx, page } = await newPage(browser, { viewport: { width: viewport[0], height: viewport[1] }, deviceScaleFactor: viewport[2] || 1 });
    page.on('pageerror', e => errors.push(`[${name}] pageerror: ${e.message}`));
    page.on('console', m => { if (m.type() === 'error') errors.push(`[${name}] console.error: ${m.text()}`); });
    if (seed) await page.addInitScript(seed);
    await page.goto(`${URL_BASE}#/path`, { waitUntil: 'load' }).catch(e => errors.push(`[${name}] goto: ${e.message}`));
    await page.waitForTimeout(1600);
    if (actions) { try { await actions(page); } catch (e) { errors.push(`[${name}] action: ${e.message.split('\n')[0]}`); } }
    const file = path.join(OUT, `${name}.png`);
    await page.screenshot({ path: file });
    shots.push(name);
    // горизонтальный overflow
    const ovf = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth).catch(() => 'n/a');
    console.log(`[ok] ${name}  overflowX=${ovf}`);
    await ctx.close();
  }

  const clearState = `try{localStorage.clear();sessionStorage.clear();}catch(e){}`;

  // 1. Десктоп: верх тропы (баннер главы + первые ноды, новичок)
  await snap('d1_top_newcomer', { viewport: [1440, 900], seed: clearState });

  // 2. Десктоп: активная нода в центре (пузырь НАЧАТЬ/ПРОДОЛЖИТЬ)
  await snap('d2_active_node', {
    viewport: [1440, 900], seed: clearState,
    actions: async (page) => {
      await page.evaluate(() => {
        const n = document.querySelector('.hex-3d-node.hex-node--active') || document.querySelector('.hex-3d-node');
        if (n) n.scrollIntoView({ block: 'center' });
      });
      await page.waitForTimeout(700);
    }
  });

  // 3. Десктоп: поповер заблокированной ноды
  await snap('d3_popover_locked', {
    viewport: [1440, 900], seed: clearState,
    actions: async (page) => {
      await page.evaluate(() => {
        const n = document.querySelector('.hex-3d-node[data-unit-id="1.3"]');
        if (n) { n.scrollIntoView({ block: 'center' }); }
      });
      await page.waitForTimeout(500);
      await page.click('.hex-3d-node[data-unit-id="1.3"]').catch(() => {});
      await page.waitForTimeout(600);
    }
  });

  // 4. Мобайл 390: верх
  await snap('m1_top_newcomer', { viewport: [390, 844, 2], seed: clearState });

  // 5. Мобайл 390: середина тропы (заблокированные ноды + ветка челленджа)
  await snap('m2_mid_trail', {
    viewport: [390, 844, 2], seed: clearState,
    actions: async (page) => {
      await page.evaluate(() => {
        const n = document.querySelector('.hex-challenge-node') || document.querySelectorAll('.hex-3d-node')[8];
        if (n) n.scrollIntoView({ block: 'center' });
      });
      await page.waitForTimeout(700);
    }
  });

  // 6. Десктоп: середина курса (сидированный прогресс, глава 2 активна)
  const seeded = `try{
    localStorage.clear();
    localStorage.setItem('academy_state_v1', JSON.stringify({
      xp: 520, streak: 6, lastVisit: new Date().toDateString(),
      dailyXpByDate: {}, completedLessons: [], completedTasks: [],
      readNotes: [], reviewedDecks: [], passedUnitTests: ['1.1','1.2','1.3','1.4'],
      mastered: [], theme: 'dark'
    }));
    localStorage.setItem('academy-obsidian-v2','1');
  }catch(e){}`;
  await snap('d4_seeded_midcourse', {
    viewport: [1440, 900], seed: seeded,
    actions: async (page) => {
      await page.evaluate(() => {
        const n = document.querySelector('.hex-3d-node.hex-node--active');
        if (n) n.scrollIntoView({ block: 'center' });
      });
      await page.waitForTimeout(700);
    }
  });

  await browser.close();
  console.log('\n=== Кадры ===');
  shots.forEach(s => console.log('  ' + path.join('scripts', 'visual_report', 'tropa_recon', s + '.png')));
  console.log('\n=== JS-ошибки: ' + errors.length + ' ===');
  errors.slice(0, 20).forEach(e => console.log('  ' + e));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
