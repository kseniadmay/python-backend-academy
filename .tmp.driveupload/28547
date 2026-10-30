#!/usr/bin/env node
/**
 * visual_test.js — Автоматическое визуальное тестирование платформы Python Backend Academy.
 *
 * Что делает (этап 6/6 конвейера verify_all.py):
 *   1. Поднимает локальный статический сервер на папке проекта.
 *   2. Снимает скриншоты ВСЕХ представлений проекта в матрице:
 *        маршруты academy.html (дашборд, #/path в game и pro, #/map в двух подрежимах,
 *        все 7 треков, страница юнита, #/practice, #/cards, #/mock, #/docs, #/sandbox)
 *        × viewport'ы (desktop 1440x900, mobile 390x844 @2x)
 *        × состояния (новичок + сеедированный прогресс «середина курса»).
 *   3. Для каждого кадра собирает зонды: JS-ошибки страницы (FAIL), горизонтальный
 *      overflow (FAIL), пустой рендер (FAIL), console.error и упавшие запросы (WARN).
 *   4. Сравнивает кадры с эталонами scripts/visual_baselines/ попиксельно
 *      (pixelmatch) и падает при расхождении > VISUAL_TOLERANCE_PCT.
 *
 * Режимы запуска:
 *   node scripts/visual_test.js            — прогон с сравнением (для конвейера)
 *   node scripts/visual_test.js --update   — переснять эталоны (после ОСОЗНАННЫХ правок UI)
 *   node scripts/visual_test.js --only foo — снять только кадры, чьё имя содержит "foo"
 *
 * Зависимости (playwright-core + pixelmatch + pngjs) ставятся автоматически
 * в %LOCALAPPDATA%\pba-visual-deps (вне OneDrive, node_modules не синхронизируется).
 * Браузер: системный Chrome/Edge — скачивание Chromium не требуется.
 */

'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');
const { pathToFileURL } = require('url');

const ROOT = path.resolve(__dirname, '..');
const PORT = 8793;
const OUT_DIR = path.join(__dirname, 'visual_report');
const BASELINE_DIR = path.join(__dirname, 'visual_baselines');
const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');
const VISUAL_TOLERANCE_PCT = 0.1; // % несовпавших пикселей, выше которого кадр считается ИЗМЕНИВШИМСЯ
const RENDER_SETTLE_MS = 1400;    // пауза на рендер маршрута (анимации отключены)

const UPDATE = process.argv.includes('--update');
const ONLY_IDX = process.argv.indexOf('--only');
const ONLY = ONLY_IDX >= 0 ? process.argv[ONLY_IDX + 1] : null;

// ---------------------------------------------------------------- зависимости
function resolveDep(name) {
  try { return require(name); } catch (e) { /* дальше по списку */ }
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

function ensureDeps() {
  let pw = resolveDep('playwright-core');
  let pm = resolveDep('pixelmatch');
  let pngjs = resolveDep('pngjs');
  if (pw && pm && pngjs) return { pw, pm, pngjs };
  console.log('[visual] Установка зависимостей в ' + DEPS_DIR + ' (один раз)...');
  fs.mkdirSync(DEPS_DIR, { recursive: true });
  const r = spawnSync('npm', ['install', '--prefix', DEPS_DIR, 'playwright-core@1.49.0', 'pixelmatch@5.3.0', 'pngjs@7.0.0', '--no-audit', '--no-fund', '--loglevel', 'error'], { stdio: 'inherit', shell: process.platform === 'win32' });
  if (r.status !== 0) throw new Error('npm install зависимостей не удался (код ' + r.status + ')');
  return {
    pw: resolveDep('playwright-core'),
    pm: resolveDep('pixelmatch'),
    pngjs: resolveDep('pngjs')
  };
}

// ---------------------------------------------------------------- браузер
function findBrowser() {
  const candidates = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Chromium.app/Contents/MacOS/Chromium'
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;

  // macOS ms-playwright cache
  const macPwCache = path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright');
  if (fs.existsSync(macPwCache)) {
    for (const d of fs.readdirSync(macPwCache)) {
      const exe = path.join(macPwCache, d, 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium');
      if (fs.existsSync(exe)) return exe;
    }
  }

  // Windows ms-playwright cache
  const pwCache = path.join(process.env.LOCALAPPDATA || '', 'ms-playwright');
  if (fs.existsSync(pwCache)) {
    for (const d of fs.readdirSync(pwCache)) {
      const exe = path.join(pwCache, d, 'chrome-win', 'chrome.exe');
      if (fs.existsSync(exe)) return exe;
    }
  }

  // Linux ms-playwright cache
  const linuxPwCache = path.join(os.homedir(), '.cache', 'ms-playwright');
  if (fs.existsSync(linuxPwCache)) {
    for (const d of fs.readdirSync(linuxPwCache)) {
      const exe = path.join(linuxPwCache, d, 'chrome-linux', 'chrome');
      if (fs.existsSync(exe)) return exe;
    }
  }

  throw new Error('Не найден Chrome/Edge/Chromium для визуальных снимков');
}

// ---------------------------------------------------------------- сервер
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.webp': 'image/webp', '.webmanifest': 'application/manifest+json',
  '.woff2': 'font/woff2', '.md': 'text/plain; charset=utf-8'
};
function serve() {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      let u = decodeURIComponent(req.url.split('?')[0]);
      if (u === '/api/sync') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, revision: 0 }));
        return;
      }
      if (u === '/favicon.ico') {
        const iconPath = path.join(ROOT, 'icon.svg');
        if (fs.existsSync(iconPath)) {
          res.writeHead(200, { 'Content-Type': 'image/svg+xml' });
          res.end(fs.readFileSync(iconPath));
          return;
        }
        res.writeHead(204);
        res.end();
        return;
      }
      let fp = u === '/' ? path.join(ROOT, 'academy.html') : path.join(ROOT, u);
      if (u.endsWith('/')) fp = path.join(ROOT, u, 'index.html');
      fs.readFile(fp, (err, data) => {
        if (err) { res.writeHead(404); res.end('nf'); return; }
        res.writeHead(200, { 'Content-Type': MIME[path.extname(fp).toLowerCase()] || 'application/octet-stream' });
        res.end(data);
      });
    });
    srv.listen(PORT, '127.0.0.1', () => resolve(srv));
  });
}

// ---------------------------------------------------------------- матрица кадров
const VIEWPORTS = {
  desktop: { width: 1440, height: 900, dpr: 1 },
  tablet: { width: 768, height: 1024, dpr: 1 },
  mobile: { width: 390, height: 844, dpr: 2, isMobile: true, hasTouch: true }
};

const SEED_STATE = {
  schemaVersion: 3,
  passedUnitTests: ['1.1', '1.2', '1.3', '1.4'],
  streak: 6,
  xp: 520,
  pathViewMode: 'game',
  lastRoute: '/path'
};

const TRACKS = ['python', 'web', 'backend', 'algorithms', 'databases', 'architecture', 'infra'];

// name → { hash, action: 'pro'|null, seed: bool, viewports: [...] }
const SHOTS = [];
function add(name, def) { SHOTS.push(Object.assign({ name, viewports: ['desktop', 'mobile'] }, def)); }

add('dashboard', { hash: '#/' });
add('path_game', { hash: '#/path' });
add('path_pro', { hash: '#/path', action: 'pro' });
for (const t of TRACKS) add('track_' + t, { hash: '#/' + t });
add('skill_python_1_1_1', { hash: '#/python/skill/1.1.1' });
add('practice_hub', { hash: '#/practice' });
add('cards_hub', { hash: '#/cards' });
add('mock_interview', { hash: '#/mock' });
add('docs_hub', { hash: '#/docs' });
add('sandbox', { hash: '#/sandbox' });
// стартовая модалка рубежного теста «Готовы начать тест?» (новичок; 1.5 нет в SEED_STATE — модалка показывается)
add('unittest_start_modal', { hash: '#/python/unittest/1.5' });
// сеедированный прогресс «середина курса»
add('dashboard_seed', { hash: '#/', seed: true });
add('path_game_seed', { hash: '#/path', seed: true });
add('path_pro_seed', { hash: '#/path', action: 'pro', seed: true });

// --- Светлая тема «Утренний Шёлк» (Morning Silk)
add('dashboard_light', { hash: '#/', theme: 'light', viewports: ['desktop', 'mobile'] });
add('path_game_light', { hash: '#/path', theme: 'light', viewports: ['desktop', 'mobile'] });
add('cards_hub_light', { hash: '#/cards', theme: 'light', viewports: ['desktop', 'mobile'] });
add('practice_hub_light', { hash: '#/practice', theme: 'light', viewports: ['desktop', 'mobile'] });

// --- Планшетные вьюпорты (Tablet 768px)
add('dashboard_tablet', { hash: '#/', viewports: ['tablet'] });
add('path_tablet', { hash: '#/path', viewports: ['tablet'] });

// --- Интерактивные состояния
add('path_popover_active', { hash: '#/path', action: 'open_popover', viewports: ['mobile', 'desktop'] });


// ---------------------------------------------------------------- пиксельный diff
function diffShots(pm, pngjs, currentPath, baselinePath, diffPath) {
  const { PNG } = pngjs;
  const a = PNG.sync.read(fs.readFileSync(currentPath));
  const b = PNG.sync.read(fs.readFileSync(baselinePath));
  if (a.width !== b.width || a.height !== b.height) {
    return { diffPct: 100, note: `размер изменился: ${b.width}x${b.height} -> ${a.width}x${a.height}` };
  }
  const numDiff = pm(a.data, b.data, null, a.width, a.height, { threshold: 0.1 });
  const total = a.width * a.height;
  // diff-карта: изменённые пиксели красным, совпавшие — прозрачным
  const diffPng = new PNG({ width: a.width, height: a.height });
  for (let i = 0; i < a.data.length; i += 4) {
    const same = Math.abs(a.data[i] - b.data[i]) + Math.abs(a.data[i + 1] - b.data[i + 1]) + Math.abs(a.data[i + 2] - b.data[i + 2]) < 30;
    if (same) { diffPng.data[i] = 0; diffPng.data[i + 1] = 0; diffPng.data[i + 2] = 0; diffPng.data[i + 3] = 60; }
    else { diffPng.data[i] = 255; diffPng.data[i + 1] = 0; diffPng.data[i + 2] = 0; diffPng.data[i + 3] = 255; }
  }
  fs.writeFileSync(diffPath, PNG.sync.write(diffPng));
  return { diffPct: +(numDiff / total * 100).toFixed(4) };
}

// ---------------------------------------------------------------- основной прогон
async function runVisualSuite() {
  const { pw, pm, pngjs } = ensureDeps();
  const { chromium } = pw;
  fs.mkdirSync(OUT_DIR, { recursive: true });
  if (UPDATE) fs.mkdirSync(BASELINE_DIR, { recursive: true });

  const shots = ONLY ? SHOTS.filter(s => s.name.includes(ONLY)) : SHOTS;
  if (!shots.length) { console.error('[visual] Ни один кадр не подходит под --only ' + ONLY); process.exit(1); }
  console.log(`[visual] Запуск конвейера (кадров: ${shots.length}, UPDATE=${UPDATE})...`);

  // Песочницы (например, ZCode) могут блокировать клиентские TCP-соединения на 127.0.0.1:
  // сервер поднимается, но браузер не может открыть страницу и goto зависает.
  // Проба loopback, при недоступности — работа напрямую через file:// (localStorage на file-origin работает).
  let srv = null;
  let FILE_MODE = process.env.PBA_FILE_URL === '1' || (process.env.PBA_FILE_URL !== '0' && process.platform === 'darwin');
  if (!FILE_MODE) {
    srv = await serve();
    const loopbackOk = await new Promise(res => {
      const rq = http.get(`http://127.0.0.1:${PORT}/`, r => { r.resume(); res(true); });
      rq.on('error', () => res(false));
      rq.setTimeout(4000, () => { rq.destroy(); res(false); });
    });
    if (!loopbackOk) {
      console.log('[visual] Loopback TCP недоступен (blocked by sandbox) — режим file://');
      FILE_MODE = true;
      await new Promise(r => srv.close(r));
      srv = null;
    }
  }
  const pageUrl = shot => {
    if (!FILE_MODE) {
      return `http://127.0.0.1:${PORT}/academy.html${shot.hash || ''}`;
    }
    const file = path.join(ROOT, 'academy.html');
    return pathToFileURL(file).href + (shot.hash || '');
  };

  const browser = await chromium.launch({
    executablePath: findBrowser(),
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
  });
  const results = [];
  let failures = 0;

  for (const vpName of Object.keys(VIEWPORTS)) {
    const vp = VIEWPORTS[vpName];

    // отдельный контекст на каждое состояние (новичок / сеед) — без накопления init-скриптов
    for (const seeded of [false, true]) {
      const ctx = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        deviceScaleFactor: vp.dpr,
        isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch
      });

      for (const shot of shots) {
        if (!!shot.seed !== seeded) continue; // кадр относится к другому состоянию (без seed = новичок)
        if (!shot.viewports.includes(vpName)) continue;

        // Своя страница на каждый кадр: повторный goto той же страницы отличается только
        // hash'ем — same-document навигация в Playwright с waitUntil:'load' зависает до таймаута.
        const page = await ctx.newPage();

        await page.addInitScript(seeded
          ? `try{localStorage.setItem('academy_state_v1', ${JSON.stringify(JSON.stringify(SEED_STATE))});}catch(e){}`
          : `try{localStorage.removeItem('academy_state_v1');}catch(e){}`);
        await page.addInitScript(`
          try {
            const _origScroll = Element.prototype.scrollIntoView;
            Element.prototype.scrollIntoView = function(arg) {
              if (typeof arg === 'object' && arg !== null) {
                return _origScroll.call(this, Object.assign({}, arg, { behavior: 'instant' }));
              }
              return _origScroll.call(this, arg);
            };
          } catch(e) {}
        `);

        const pageErrors = [];
        const consoleErrors = [];
        const failedRequests = [];
        page.on('pageerror', e => pageErrors.push(String((e && e.message) || e)));
        page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300)); });
        page.on('requestfailed', r => failedRequests.push(r.url().slice(-120) + ' :: ' + ((r.failure() && r.failure().errorText) || '')));
        page.on('response', r => { if (r.status() >= 400) failedRequests.push(r.url().slice(-120) + ' :: HTTP ' + r.status()); });

        const label = `${shot.name}_${vpName}`;
        console.log(`[visual] -> Кадр: ${label}`);
        try {
          await page.goto(pageUrl(shot), { waitUntil: 'load', timeout: 60000 });
        } catch (e) {
          results.push({ shot: label, status: 'FAIL', reason: 'навигация не удалась: ' + e.message });
          failures++; console.log(`[FAIL] ${label} :: навигация не удалась: ${e.message}\n${e.stack}`);
          await page.close().catch(() => {});
          continue;
        }
        await page.evaluate(() => (document.fonts ? document.fonts.ready : null)).catch(() => {});
        await page.addStyleTag({
          content: `
            *, *::before, *::after {
              animation-duration: 0s !important;
              animation-delay: -0.0001s !important;
              transition-duration: 0s !important;
              transition-delay: 0s !important;
              caret-color: transparent !important;
            }
          `
        }).catch(() => {});

        if (shot.theme) {
          await page.evaluate(t => {
            document.documentElement.setAttribute('data-theme', t);
            try {
              const st = JSON.parse(localStorage.getItem('py_backend_academy_v1') || '{}');
              st.theme = t;
              localStorage.setItem('py_backend_academy_v1', JSON.stringify(st));
            } catch(e) {}
          }, shot.theme).catch(() => {});
        }

        if (shot.action === 'pro') {
          await page.evaluate(() => {
            const btn = document.querySelector('.path-mode-btn[data-set-path-mode="pro"]');
            if (btn) {
              btn.click();
            } else {
              const gear = document.querySelector('.topbar [data-open-settings-modal]') || document.querySelector('[data-open-settings-modal]');
              if (gear) gear.click();
              const m = document.getElementById('settings-modal');
              const card = m && m.querySelector('[data-set-path-mode="pro"]');
              if (card) card.click();
            }
          }).catch(() => {});
          await page.keyboard.press('Escape').catch(() => {});
        }

        if (shot.action === 'open_popover') {
          await page.evaluate(() => {
            const node = document.querySelector('.hex-btn') || document.querySelector('[data-direct-unit]') || document.querySelector('.hex-node');
            if (node) node.click();
          }).catch(() => {});
          await page.waitForTimeout(600);
        }
        await page.waitForTimeout(RENDER_SETTLE_MS);

        // --- зонды
        const probe = await page.evaluate(() => {
          function getLum(r, g, b) {
            const a = [r, g, b].map(v => {
              v /= 255;
              return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
            });
            return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
          }
          function parseRgba(c) {
            const m = (c || '').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
            if (!m) return null;
            return { r: parseInt(m[1]), g: parseInt(m[2]), b: parseInt(m[3]), a: m[4] !== undefined ? parseFloat(m[4]) : 1 };
          }
          function getEffectiveBg(el) {
            let cur = el;
            while (cur && cur !== document.documentElement) {
              const s = window.getComputedStyle(cur);
              const c = parseRgba(s.backgroundColor);
              if (c && c.a > 0.3) return [c.r, c.g, c.b];
              cur = cur.parentElement;
            }
            const isDark = (document.documentElement.getAttribute('data-theme') || 'dark') === 'dark';
            return isDark ? [11, 15, 23] : [248, 250, 252];
          }

          let minRatio = 21;
          const els = Array.from(document.querySelectorAll('h1, h2, h3, .lesson-title, p'));
          for (const el of els.slice(0, 30)) {
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) continue;
            const s = window.getComputedStyle(el);
            if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') continue;
            const fg = parseRgba(s.color);
            if (!fg || fg.a === 0) continue;
            const bg = getEffectiveBg(el);
            const lumFg = getLum(fg.r, fg.g, fg.b);
            const lumBg = getLum(bg[0], bg[1], bg[2]);
            const ratio = (Math.max(lumFg, lumBg) + 0.05) / (Math.min(lumFg, lumBg) + 0.05);
            if (ratio < minRatio) minRatio = ratio;
          }
          return {
            hOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            htmlLen: document.body ? document.body.innerHTML.length : 0,
            textLen: document.body ? (document.body.innerText || '').length : 0,
            wcagMinRatio: Number(minRatio.toFixed(2))
          };
        }).catch(() => ({ hOverflow: -1, htmlLen: 0, textLen: 0, wcagMinRatio: 21 }));

        const issues = [];
        if (probe.htmlLen < 10000) issues.push(`подозрительно пустой рендер (htmlLen=${probe.htmlLen})`);
        if (probe.hOverflow > 0) issues.push(`горизонтальный overflow ${probe.hOverflow}px`);
        if (pageErrors.length) issues.push('JS-ошибки: ' + pageErrors.slice(0, 2).join(' | '));
        if (probe.wcagMinRatio < 4.5 && probe.htmlLen > 10000) issues.push(`WCAG AA contrast violation: min ratio ${probe.wcagMinRatio}:1 (< 4.5:1)`);

        const file = path.join(OUT_DIR, `${label}.png`);
        await page.screenshot({ path: file, animations: 'disabled' }).catch(e => issues.push('скриншот не удался: ' + e.message));

        let diffPct = null; const warns = [];
        const baseline = path.join(BASELINE_DIR, `${label}.png`);
        if (UPDATE) {
          if (fs.existsSync(file)) fs.copyFileSync(file, baseline);
        } else if (fs.existsSync(file)) {
          if (!fs.existsSync(baseline)) {
            warns.push('нет эталона');
          } else {
            try {
              const d = diffShots(pm, pngjs, file, baseline, path.join(OUT_DIR, `${label}.diff.png`));
              diffPct = d.diffPct;
              if (d.note) warns.push(d.note);
              if (d.diffPct > VISUAL_TOLERANCE_PCT) issues.push(`кадр изменился на ${d.diffPct}% (допуск ${VISUAL_TOLERANCE_PCT}%)`);
            } catch (e) { issues.push('pixel-diff не удался: ' + e.message); }
          }
        }

        if (consoleErrors.length) warns.push(`console.error x${consoleErrors.length}: ${consoleErrors[0]}`);
        if (failedRequests.length) warns.push(`упавших запросов x${failedRequests.length}: ${failedRequests[0]}`);

        const status = issues.length ? 'FAIL' : 'PASS';
        if (status === 'FAIL') failures++;
        results.push({
          shot: label, status, diffPct,
          overflow: probe.hOverflow, issues, warnings: warns,
          jsErrors: pageErrors.slice(), consoleErrors: consoleErrors.slice(), failedRequests: failedRequests.slice()
        });
        console.log(`[${status}] ${label}${diffPct !== null ? ' diff=' + diffPct + '%' : ''}${issues.length ? ' :: ' + issues.join('; ') : ''}`);
        await page.close().catch(() => {});
      }
      await ctx.close();
    }
  }

  await browser.close();
  if (srv) await new Promise(r => srv.close(r));

  fs.writeFileSync(path.join(OUT_DIR, 'report.json'), JSON.stringify({ generatedAt: new Date().toISOString(), update: UPDATE, tolerancePct: VISUAL_TOLERANCE_PCT, results }, null, 2));

  // --- отчёт markdown
  const passed = results.filter(r => r.status === 'PASS').length;
  const lines = [];
  lines.push(`# Визуальный отчёт — ${new Date().toLocaleString('ru-RU')}`);
  lines.push('');
  lines.push(`Режим: **${UPDATE ? 'переснятие эталонов (--update)' : 'сравнение с эталонами'}** · допуск: ${VISUAL_TOLERANCE_PCT}% · кадров: ${results.length} · PASS: ${passed} · FAIL: ${failures}`);
  lines.push('');
  lines.push('| Кадр | Статус | Pixel-diff | Проблемы | Предупреждения |');
  lines.push('|---|---|---|---|---|');
  for (const r of results) {
    lines.push(`| ${r.shot} | ${r.status} | ${r.diffPct !== null && r.diffPct !== undefined ? r.diffPct + '%' : '—'} | ${(r.issues || []).join('; ') || '—'} | ${(r.warnings || []).join('; ') || '—'} |`);
  }
  lines.push('');
  lines.push('Кадры и diff-карты: `scripts/visual_report/` · эталоны: `scripts/visual_baselines/`');
  fs.writeFileSync(path.join(OUT_DIR, 'report.md'), lines.join('\n'), 'utf-8');

  console.log(`\n[visual] Итог: ${passed}/${results.length} PASS, ${failures} FAIL. Отчёт: scripts/visual_report/report.md`);
  if (UPDATE) console.log('[visual] Эталоны обновлены. Закоммитьте scripts/visual_baselines/.');
  process.exit(failures ? 1 : 0);
}

if (require.main === module) {
  runVisualSuite().catch(e => { console.error('[visual] Сбой прогона:', e); process.exit(1); });
}

module.exports = { DEPS_DIR, resolveDep, ensureDeps, findBrowser, VIEWPORTS, runVisualSuite };
