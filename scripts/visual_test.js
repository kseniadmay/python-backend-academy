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
 *        × состояния (новичок + сеедированный прогресс «середина курса»);
 *      плюс экраны автономного «Практика кода — тренажёр с IDE.html».
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
  const p = path.join(DEPS_DIR, 'node_modules', name);
  if (fs.existsSync(p)) return require(p);
  return null;
}

function ensureDeps() {
  let pw = resolveDep('playwright-core');
  let pm = resolveDep('pixelmatch');
  let pngjs = resolveDep('pngjs');
  if (pw && pm && pngjs) return { pw, pm, pngjs };
  console.log('[visual] Установка зависимостей в ' + DEPS_DIR + ' (один раз)...');
  fs.mkdirSync(DEPS_DIR, { recursive: true });
  const r = spawnSync('npm', ['install', '--prefix', DEPS_DIR, 'playwright-core@1.63.0', 'pixelmatch@5.3.0', 'pngjs@7.0.0', '--no-audit', '--no-fund', '--loglevel', 'error'], { stdio: 'inherit', shell: process.platform === 'win32' });
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
  throw new Error('Не найден Chrome/Edge для визуальных снимков');
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

// name → { hash, action: 'pro'|'mapPath'|null, seed: bool, viewports: [...] }
const SHOTS = [];
function add(name, def) { SHOTS.push(Object.assign({ name, viewports: ['desktop', 'mobile'] }, def)); }

add('dashboard', { hash: '#/' });
add('path_game', { hash: '#/path' });
add('path_pro', { hash: '#/path', action: 'pro' });
add('map_tree', { hash: '#/map' });
add('map_path', { hash: '#/map', action: 'mapPath' });
for (const t of TRACKS) add('track_' + t, { hash: '#/' + t });
add('skill_python_1_1_1', { hash: '#/python/skill/1.1.1' });
add('practice_hub', { hash: '#/practice' });
add('cards_hub', { hash: '#/cards' });
add('mock_interview', { hash: '#/mock' });
add('docs_hub', { hash: '#/docs' });
add('sandbox', { hash: '#/sandbox' });
// сеедированный прогресс «середина курса»
add('dashboard_seed', { hash: '#/', seed: true });
add('path_game_seed', { hash: '#/path', seed: true });
add('path_pro_seed', { hash: '#/path', action: 'pro', seed: true });
// автономный IDE-тренажёр (по одному кадру на viewport)
add('ide', { ide: true, viewports: ['desktop', 'mobile'] });

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
(async () => {
  const { pw, pm, pngjs } = ensureDeps();
  const { chromium } = pw;
  fs.mkdirSync(OUT_DIR, { recursive: true });
  if (UPDATE) fs.mkdirSync(BASELINE_DIR, { recursive: true });

  const shots = ONLY ? SHOTS.filter(s => s.name.includes(ONLY)) : SHOTS;
  if (!shots.length) { console.error('[visual] Ни один кадр не подходит под --only ' + ONLY); process.exit(1); }

  // Песочницы (например, ZCode) могут блокировать клиентские TCP-соединения на 127.0.0.1:
  // сервер поднимается, но браузер не может открыть страницу и goto зависает.
  // Проба loopback, при недоступности — работа напрямую через file:// (localStorage на file-origin работает).
  let srv = null;
  let FILE_MODE = process.env.PBA_FILE_URL === '1';
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
      return shot.ide
        ? `http://127.0.0.1:${PORT}/${encodeURIComponent('Практика кода — тренажёр с IDE.html')}`
        : `http://127.0.0.1:${PORT}/academy.html${shot.hash}`;
    }
    const file = shot.ide
      ? path.join(ROOT, 'Практика кода — тренажёр с IDE.html')
      : path.join(ROOT, 'academy.html');
    return pathToFileURL(file).href + (shot.ide ? '' : (shot.hash || ''));
  };

  const browser = await chromium.launch({ executablePath: findBrowser(), headless: true });
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

        const pageErrors = [];
        const consoleErrors = [];
        const failedRequests = [];
        page.on('pageerror', e => pageErrors.push(String((e && e.message) || e)));
        page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300)); });
        page.on('requestfailed', r => failedRequests.push(r.url().slice(-120) + ' :: ' + ((r.failure() && r.failure().errorText) || '')));
        page.on('response', r => { if (r.status() >= 400) failedRequests.push(r.url().slice(-120) + ' :: HTTP ' + r.status()); });

        const label = `${shot.name}_${vpName}`;
        try {
          await page.goto(pageUrl(shot), { waitUntil: 'load', timeout: 60000 });
        } catch (e) {
          results.push({ shot: label, status: 'FAIL', reason: 'навигация не удалась: ' + e.message });
          failures++; console.log(`[FAIL] ${label} :: навигация не удалась`);
          await page.close().catch(() => {});
          continue;
        }
        await page.evaluate(() => (document.fonts ? document.fonts.ready : null)).catch(() => {});

        if (shot.action === 'pro') {
          const sw = page.locator('[data-set-path-mode="pro"]').first();
          if (await sw.count()) await sw.click().catch(() => {});
        }
        if (shot.action === 'mapPath') {
          const mp = page.locator('[data-map-mode="path"]').first();
          if (await mp.count()) await mp.click().catch(() => {});
        }
        await page.waitForTimeout(RENDER_SETTLE_MS);

        // --- зонды
        const probe = await page.evaluate(() => ({
          hOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          htmlLen: document.body ? document.body.innerHTML.length : 0,
          textLen: document.body ? (document.body.innerText || '').length : 0
        })).catch(() => ({ hOverflow: -1, htmlLen: 0, textLen: 0 }));

        const issues = [];
        if (probe.htmlLen < 10000) issues.push(`подозрительно пустой рендер (htmlLen=${probe.htmlLen})`);
        if (probe.hOverflow > 0) issues.push(`горизонтальный overflow ${probe.hOverflow}px`);
        if (pageErrors.length) issues.push('JS-ошибки: ' + pageErrors.slice(0, 2).join(' | '));

        const file = path.join(OUT_DIR, `${label}.png`);
        await page.screenshot({ path: file }).catch(e => issues.push('скриншот не удался: ' + e.message));

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
})().catch(e => { console.error('[visual] Сбой прогона:', e); process.exit(1); });
