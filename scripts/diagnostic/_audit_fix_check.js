#!/usr/bin/env node
/* Одноразовый контроль правок по визуальному аудиту 06.10.2026 (V1–V28).
 * Снимает скриншоты исправленных мест в scripts/visual_report/audit_fixes/
 * и печатает пробы (DOM-проверки) по каждому фиксу. Режим file:// (песочница). */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');
const { pathToFileURL } = require('url');

const ROOT = path.resolve(__dirname, '..');
const OUT_DIR = path.join(__dirname, 'visual_report', 'audit_fixes');
const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');

function resolveDep(name) {
  try { return require(name); } catch (e) { /* try deps dir */ }
  const p = path.join(DEPS_DIR, 'node_modules', name);
  return fs.existsSync(p) ? require(p) : null;
}
function findBrowser() {
  for (const c of [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
  ]) if (fs.existsSync(c)) return c;
  throw new Error('Chrome/Edge not found');
}

const SEED9 = { schemaVersion: 3, passedUnitTests: ['1.1','1.2','1.3','1.4','1.5','1.6','1.7','1.8','1.9'], streak: 6, xp: 520, pathViewMode: 'game', lastRoute: '/path' };
const SEED14 = { schemaVersion: 3, passedUnitTests: ['1.4'], streak: 6, xp: 520, pathViewMode: 'game', lastRoute: '/path' };
const SEED_MID = { schemaVersion: 3, passedUnitTests: ['1.1','1.2','1.3','1.4'], streak: 6, xp: 520, pathViewMode: 'game', lastRoute: '/path' };

const FILE_URL = pathToFileURL(path.join(ROOT, 'academy.html')).href;

(async () => {
  const pw = resolveDep('playwright-core');
  if (!pw) { console.error('playwright-core недоступен'); process.exit(1); }
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await pw.chromium.launch({ executablePath: findBrowser(), headless: true });
  const outcomes = [];
  const note = (name, ok, detail) => { outcomes.push({ name, ok, detail }); console.log(`${ok ? 'OK  ' : 'BAD '} ${name} :: ${detail || ''}`); };

  async function makePage({ vp, seed, light }) {
    const ctx = await browser.newContext({
      viewport: { width: vp[0], height: vp[1] },
      deviceScaleFactor: vp[2] || 1,
      isMobile: vp[0] < 500, hasTouch: vp[0] < 500
    });
    const page = await ctx.newPage();
    const seedObj = Object.assign({}, light ? { theme: 'light' } : {}, seed || null);
    const init = [];
    if (seedObj) init.push(`try{localStorage.setItem('academy_state_v1', ${JSON.stringify(JSON.stringify(seedObj))});}catch(e){}`);
    init.push(`try{localStorage.setItem('academy-obsidian-v2','1');}catch(e){}`);
    await page.addInitScript(init.join('\n'));
    return { ctx, page };
  }

  // ---- V3: пузырь «НАЧАТЬ» vs лента главы (сид 1.1–1.9, активен 2.1)
  for (const [tag, vp] of [['d', [1440, 900]], ['m', [390, 844, 2]]]) {
    const { ctx, page } = await makePage({ vp, seed: SEED9 });
    await page.goto(FILE_URL + '#/path', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    await page.evaluate(() => { const n = document.querySelector('.hex-node--active'); if (n) n.scrollIntoView({ block: 'center' }); });
    await page.waitForTimeout(700);
    // зазор: низ ленты главы 2 vs верх пузыря активной ноды
    const gapInfo = await page.evaluate(() => {
      const active = document.querySelector('.hex-node--active');
      const bubble = document.querySelector('.hex-active-tooltip');
      if (!active || !bubble) return { err: 'нет активной ноды/пузыря' };
      const bb = bubble.getBoundingClientRect();
      const ribbons = Array.from(document.querySelectorAll('.path-chapter-ribbon')).map(r => r.getBoundingClientRect());
      const overlapping = ribbons.filter(r => !(r.bottom <= bb.top || r.top >= bb.bottom) && Math.abs(r.left + r.width / 2 - (bb.left + bb.width / 2)) < 260);
      return { bubbleTop: Math.round(bb.top), ribbonOverlap: overlapping.length, ribbons: ribbons.length };
    });
    await page.screenshot({ path: path.join(OUT_DIR, `fix_bubble_${tag}.png`) });
    note(`V3 bubble_${tag}`, gapInfo.ribbonOverlap === 0, JSON.stringify(gapInfo));
    await ctx.close();
  }

  // ---- V1 + V13: поповер — заголовок без дубля, CTA в вьюпорте (desktop)
  {
    const { ctx, page } = await makePage({ vp: [1440, 900], seed: SEED_MID });
    await page.goto(FILE_URL + '#/path', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    // нижний гекс: кликаем последнюю ноду (глубоко внизу) — проверяем и заголовок, и кламп
    const info = await page.evaluate(() => {
      const nodes = Array.from(document.querySelectorAll('.hex-3d-node'));
      const target = nodes[nodes.length - 1];
      if (!target) return { err: 'нет нод' };
      target.scrollIntoView({ block: 'center' });
      return new Promise(resolve => setTimeout(() => {
        target.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        const pop = document.querySelector('.path-popover');
        const title = document.getElementById('popover-title');
        const cta = document.getElementById('popover-cta-btn');
        const r = pop ? pop.getBoundingClientRect() : null;
        const ctaR = cta ? cta.getBoundingClientRect() : null;
        resolve({
          title: title ? title.textContent : null,
          popBottom: r ? Math.round(r.bottom) : null,
          popTop: r ? Math.round(r.top) : null,
          vh: window.innerHeight,
          ctaVisible: ctaR ? (ctaR.bottom <= window.innerHeight && ctaR.top >= 0) : null
        });
      }, 350));
    });
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_popover_d.png') });
    const dup = info.title && /^Юнит\s+[\d.]+:\s*Юнит\s+[\d.]+/.test(info.title);
    note('V1 popover title', info.title && !dup, 'title="' + info.title + '"');
    note('V13 popover clamp', info.ctaVisible === true, 'popBottom=' + info.popBottom + ' vh=' + info.vh);
    await ctx.close();
  }

  // ---- V2: светлая тема — done/active сегменты залиты
  for (const [tag, vp] of [['d', [1440, 900]], ['m', [390, 844, 2]]]) {
    const { ctx, page } = await makePage({ vp, seed: SEED_MID, light: true });
    await page.goto(FILE_URL + '#/path', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const seg = await page.evaluate(() => {
      const done = document.querySelector('.path-seg-bar.done');
      const active = document.querySelector('.path-seg-bar.active');
      const bg = el => el ? getComputedStyle(el).backgroundImage + '|' + getComputedStyle(el).backgroundColor : 'none';
      return { done: bg(done), active: bg(active) };
    });
    await page.evaluate(() => { const b = document.querySelector('.path-chapter-banner'); if (b) b.scrollIntoView({ block: 'center' }); });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT_DIR, `fix_light_seg_${tag}.png`) });
    note(`V2 light seg ${tag}`, /gradient|rgb\((2[0-9]{2}|1[5-9][0-9])/.test(seg.done) && seg.done !== 'none|rgba(0, 0, 0, 0)', JSON.stringify(seg).slice(0, 160));
    await ctx.close();
  }

  // ---- V4: таблица «Тестовые случаи» не срезана (desktop) + V14 docs (mobile)
  {
    const { ctx, page } = await makePage({ vp: [1440, 900] });
    await page.goto(FILE_URL + '#/practice', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const t = await page.evaluate(() => {
      const wrap = document.querySelector('.prac-testcases-wrapper');
      const table = document.querySelector('.prac-testcases-table');
      if (!wrap || !table) return { err: 'нет таблицы' };
      return { wrapW: wrap.clientWidth, tableW: table.scrollWidth, wrapScroll: wrap.scrollWidth };
    });
    await page.evaluate(() => { const el = document.querySelector('.prac-testcases-wrapper'); if (el) el.scrollIntoView({ block: 'center' }); });
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_practice_table_d.png') });
    note('V4 practice table', !t.err && t.tableW <= t.wrapW + 2, JSON.stringify(t));
    await ctx.close();
  }
  {
    const { ctx, page } = await makePage({ vp: [390, 844, 2] });
    await page.goto(FILE_URL + '#/docs', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const d = await page.evaluate(() => {
      const tables = Array.from(document.querySelectorAll('.docs-hub table'));
      const bad = tables.filter(tb => {
        let el = tb.parentElement;
        while (el && el !== document.body) {
          const st = getComputedStyle(el);
          if (st.overflowX === 'auto' || st.overflowX === 'scroll') return false; // скроллирующийся предок есть
          el = el.parentElement;
        }
        return tb.scrollWidth > (tb.parentElement.clientWidth || 99999) + 2;
      });
      const pageOverflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
      return { tables: tables.length, overflowingNoScroll: bad.length, pageOverflow };
    });
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_docs_m.png'), fullPage: false });
    note('V14 docs tables mobile', d.overflowingNoScroll === 0, JSON.stringify(d));
    await ctx.close();
  }

  // ---- V5: треки desktop — без строки «Навыков: … Конспектов: …»
  {
    const { ctx, page } = await makePage({ vp: [1440, 900] });
    await page.goto(FILE_URL + '#/algorithms', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const txt = await page.evaluate(() => document.body.innerText || '');
    note('V5 tracks desc gone', !/Конспектов: \d+ · Колод карточек/.test(txt), 'matches=' + (/Конспектов: \d+ · Колод карточек/.test(txt)));
    note('V16 chip wrap', !/Юнит 4\.[\d.]+ · \d+ \/ \d+ MP\s*\n\(/.test(txt), 'compact chip');
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_track_d.png') });
    await ctx.close();
  }

  // ---- V18/V28: дашборд — активность не «0 дней», матрица без нечитаемых глифов
  {
    const { ctx, page } = await makePage({ vp: [390, 844, 2], seed: SEED_MID });
    await page.goto(FILE_URL + '#/', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const info = await page.evaluate(() => {
      const txt = document.body.innerText || '';
      const sqs = Array.from(document.querySelectorAll('.dash-skill-row .m-sq'));
      const glyphed = sqs.filter(b => (b.textContent || '').trim().length > 0);
      return { zeroDays: /0 дней активности/.test(txt), squares: sqs.length, glyphed: glyphed.length, dash: /Мои результаты/.test(txt) };
    });
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_dash_m.png') });
    note('V18 active days', info.dash && !info.zeroDays, JSON.stringify(info));
    note('V28 clean squares', info.squares > 100 && info.glyphed === 0, `squares=${info.squares} glyphed=${info.glyphed}`);
    await ctx.close();
  }

  // ---- V27: рубежный тест с сидом «1.4 сдан» — бейдж «Сдано»
  {
    const { ctx, page } = await makePage({ vp: [1440, 900], seed: SEED14 });
    await page.goto(FILE_URL + '#/python/unittest/1.4', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const has = await page.evaluate(() => (document.body.innerText || '').includes('✓ Сдано'));
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_unittest_d.png') });
    note('V27 unittest badge', has, 'badge=' + has);
    await ctx.close();
  }

  // ---- V8/V20: скретчпад не режет строку; консоль лабы скрыта до запуска; светлая тема — светлый вывод
  {
    const { ctx, page } = await makePage({ vp: [390, 844, 2], light: true });
    await page.goto(FILE_URL + '#/python/skill/1.1.1', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1800);
    const info = await page.evaluate(() => {
      const ta = document.getElementById('skill-lab-scratchpad');
      const out = document.getElementById('skill-lab-output');
      return {
        taH: ta ? ta.clientHeight : null,
        taScrollH: ta ? ta.scrollHeight : null,
        outVisible: out ? getComputedStyle(out).display !== 'none' : null,
        outBg: out ? getComputedStyle(out).backgroundColor : null
      };
    });
    note('V8 scratchpad fits', info.taH !== null && info.taScrollH <= info.taH + 2, JSON.stringify(info));
    note('V20 lab console hidden', info.outVisible === false, 'display=' + (info.outVisible ? 'visible' : 'none'));
    await page.evaluate(() => { const ta = document.getElementById('skill-lab-scratchpad'); if (ta) ta.scrollIntoView({ block: 'center' }); });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_skill_light_m.png') });
    await ctx.close();
  }

  // ---- V15: песочница в светлой теме — светлый вывод
  {
    const { ctx, page } = await makePage({ vp: [1440, 900], light: true });
    await page.goto(FILE_URL + '#/sandbox', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const bg = await page.evaluate(() => { const o = document.getElementById('code-output'); return o ? getComputedStyle(o).backgroundColor : null; });
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_sandbox_light_d.png') });
    note('V15 sandbox light', bg === 'rgb(241, 245, 249)', 'bg=' + bg);
    await ctx.close();
  }

  // ---- V11: настройки mobile — «Сбросить прогресс» видна
  {
    const { ctx, page } = await makePage({ vp: [390, 844, 2] });
    await page.goto(FILE_URL + '#/', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1400);
    await page.evaluate(() => { const g = document.querySelector('.topbar [data-open-settings-modal]') || document.querySelector('[data-open-settings-modal]'); if (g) g.click(); });
    await page.waitForTimeout(600);
    const info = await page.evaluate(() => {
      const btn = document.getElementById('settings-reset-btn');
      if (!btn) return { err: 'нет кнопки' };
      const r = btn.getBoundingClientRect();
      return { top: Math.round(r.top), bottom: Math.round(r.bottom), vh: window.innerHeight, inView: r.top >= 0 && r.bottom <= window.innerHeight };
    });
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_settings_m.png') });
    note('V11 settings reset visible', info.inView === true, JSON.stringify(info));
    await ctx.close();
  }

  // ---- V12: автоскролл к активной ноде (mobile, сид 1.1–1.9)
  {
    const { ctx, page } = await makePage({ vp: [390, 844, 2], seed: SEED9 });
    await page.goto(FILE_URL + '#/path', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(2300);
    const info = await page.evaluate(() => {
      const n = document.querySelector('.hex-node--active');
      if (!n) return { err: 'нет ноды' };
      const r = n.getBoundingClientRect();
      return { top: Math.round(r.top), bottom: Math.round(r.bottom), vh: window.innerHeight, visible: r.top > 90 && r.bottom < window.innerHeight - 100 };
    });
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_scroll_m.png') });
    note('V12 active node visible', info.visible === true, JSON.stringify(info));
    await ctx.close();
  }

  // ---- V26/V24: босс HP nowrap, мок — без дубля «Задание:»
  {
    const { ctx, page } = await makePage({ vp: [390, 844, 2] });
    await page.goto(FILE_URL + '#/python/boss', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const hp = await page.evaluate(() => {
      const el = Array.from(document.querySelectorAll('.boss-hp-val')).find(x => x.offsetParent);
      if (!el) return { err: 'нет HP' };
      const r = el.getBoundingClientRect();
      return { h: Math.round(r.height), oneLine: r.height < 30 };
    });
    note('V26 boss HP one line', hp.oneLine === true, JSON.stringify(hp));
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_boss_m.png') });
    await ctx.close();
  }
  {
    const { ctx, page } = await makePage({ vp: [1440, 900] });
    await page.goto(FILE_URL + '#/mock', { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(1600);
    const m = await page.evaluate(() => {
      const h2 = document.querySelector('.microstep-card h2');
      if (!h2) return { err: 'нет заголовка' };
      const titleClean = (h2.textContent || '').trim().replace(/[.]$/, '');
      const theories = Array.from(document.querySelectorAll('.microstep-card .lesson-theory'));
      const dup = theories.filter(el => {
        let t = (el.textContent || '').replace(/\s+/g, ' ').trim();
        t = t.replace(/^(?:Задание|Задача)\s*[:·\-–—]?\s*/i, '').replace(/[.]$/, '');
        return t === titleClean;
      });
      return { total: theories.length, dupExact: dup.length };
    });
    note('V24 mock desc dedup', m.dupExact === 0, JSON.stringify(m));
    await page.screenshot({ path: path.join(OUT_DIR, 'fix_mock_d.png') });
    await ctx.close();
  }

  await browser.close();
  const bad = outcomes.filter(o => !o.ok);
  console.log(`\n=== ${outcomes.length - bad.length}/${outcomes.length} проверок OK ===`);
  process.exit(bad.length ? 2 : 0);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
