#!/usr/bin/env node
'use strict';

/**
 * test_mobile_perf_guard.js
 *
 * Автоматический страж мобильного отклика (INP Guard) и бюджета стейта:
 * 1. Статический контроль CSS (touch-action, contain), GPU-анимаций искр и UTF-8 чтения HTTP body.
 * 2. Бюджет размера (< 250 КБ) и чистоты (0 символов U+FFFD) после санитизации в клиенте и server.js.
 * 3. Мобильный рендер (innerWidth = 390): пропуск скрытого десктопного сайдбара, in-place обновление .tabbar, потолок времени render().
 * 4. In-place переключение шагов теории, карточек SRS и защита от двойного render() на hashchange.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const { rootDir, getTestContext, assertCanonicalEtalonSync } = require('./test_helpers');

const ctx = getTestContext();
const htmlRaw = ctx.etalonyHtmlRaw;
const htmlNorm = ctx.etalonyHtml;
const serverPath = path.join(rootDir, 'scripts', 'server.js');
const serverJs = fs.readFileSync(serverPath, 'utf8');

// =========================================================================
// 1. Статический контроль эталона и server.js
// =========================================================================
assertCanonicalEtalonSync();

const touchActionMatch = htmlNorm.match(/a,\s*button,[\s\S]*?\.tabbar__item[\s\S]*?\{[^}]*touch-action\s*:\s*manipulation/i);
assert(touchActionMatch, 'CSS обязан задавать touch-action:manipulation для интерактивных элементов и .tabbar__item');

const containMatch = htmlNorm.match(/\.dash-horizon[\s\S]*?\.srs-note-card-clean\s*\{[^}]*contain\s*:\s*layout\s+style/i);
assert(containMatch, 'CSS обязан задавать contain:layout style для изолированных контейнеров (.srs-note-card-clean)');

const sparksStart = htmlNorm.indexOf('function triggerSparksBurst(');
assert(sparksStart !== -1, 'Не найдена функция triggerSparksBurst');
const sparksEnd = htmlNorm.indexOf('\nfunction ', sparksStart + 30);
const sparksBody = htmlNorm.slice(sparksStart, sparksEnd !== -1 ? sparksEnd : sparksStart + 5000);
assert(!sparksBody.includes('drop-shadow('), 'В SVG-искрах triggerSparksBurst запрещён дорогой filter:drop-shadow(...)');
assert(!sparksBody.includes('brightness('), 'В keyframe-анимациях triggerSparksBurst запрещён покадровый filter:brightness(...)');

const readBodyStart = serverJs.indexOf('function readRequestBody(');
assert(readBodyStart !== -1, 'В scripts/server.js не найдена функция readRequestBody');
const readBodyEnd = serverJs.indexOf('function syncAuthorized(', readBodyStart);
const readBodyFn = serverJs.slice(readBodyStart, readBodyEnd !== -1 ? readBodyEnd : readBodyStart + 800);
assert(readBodyFn.includes('Buffer.concat('), 'readRequestBody в scripts/server.js обязан декодировать тело через Buffer.concat(...)');
assert(!/body\s*\+=\s*chunk/.test(readBodyFn), 'readRequestBody не должен склеивать Buffer-чанки строковым body += chunk');

// =========================================================================
// 2. Синтетический стресс-слепок с порчей U+FFFD + опциональный живой дамп
// =========================================================================
const dirtyState = {
  xp: 4250,
  streak: 14,
  readNotes: ['\uFFFD\uFFFD-001', 'К-001', '\uFFFD-004'],
  reviewedDecks: ['\uFFFD-001', '\uFFFD\uFFFD-005'],
  noteSrs: {
    ['\uFFFD'.repeat(500) + '-004']: { step: 2, interval: 7, lastReview: '2026-11-20' },
    'К-004': { step: 1, interval: 3, lastReview: '2026-11-10' }
  },
  cardSrs: {
    ['\uFFFD'.repeat(20) + '-025:3']: { reps: 3, interval: 10, lastReview: '2026-11-25' },
    'Ф-025:3': { reps: 1, interval: 1, lastReview: '2026-11-15' }
  },
  cardRatings: {
    '\uFFFD-025:3': 4,
    'Ф-025:3': 2
  },
  completedNoteSteps: {
    '\uFFFD-004:1': true
  },
  unlockedChunks: {
    ['skill:' + '\uFFFD'.repeat(100) + '-005:1:2']: true,
    'lesson:1.1:0:1': true
  },
  readingPositions: {
    '1.1.1': {
      kId: '\uFFFD-001',
      fId: '\uFFFD-001',
      deckId: '\uFFFD-001',
      deckPositions: {
        '\uFFFD-001': { sessionLearned: 5 }
      }
    }
  },
  cardsHubPos: {
    deckId: '\uFFFD-002',
    dueQueue: [
      { deckId: '\uFFFD-002', cardIdx: 1 },
      { deckId: 'Ф-002', cardIdx: 1 }
    ]
  },
  bugReports: [
    {
      text: '\uFFFD'.repeat(55000) + 'Баг отступа на мобилке',
      context: '\uFFFD#/path',
      timestamp: '2026-11-27T12:00:00Z'
    },
    {
      text: '\uFFFD\uFFFD\u0007',
      context: 'empty',
      timestamp: '2026-11-27T12:01:00Z'
    }
  ]
};

// Проверка server.js sanitizeAcademyStateServer
const srvFnMatch = serverJs.match(/function sanitizeServerKey[\s\S]*?\nfunction readRequestBody/);
assert(srvFnMatch, 'В scripts/server.js должна присутствовать sanitizeAcademyStateServer');
const srvCtx = { console };
vm.createContext(srvCtx);
vm.runInContext(srvFnMatch[0].replace(/\nfunction readRequestBody$/, ''), srvCtx);

const srvCleaned = srvCtx.sanitizeAcademyStateServer(JSON.parse(JSON.stringify(dirtyState)));
const srvJson = JSON.stringify(srvCleaned);
const srvBytes = Buffer.byteLength(srvJson, 'utf8');
assert.strictEqual((srvJson.match(/\uFFFD/g) || []).length, 0, 'server.js оставил U+FFFD в dirtyState');
assert(srvBytes < 250 * 1024, `Размер стейта после server.js санитизации превысил 250 КБ: ${srvBytes}`);
assert.strictEqual(srvCleaned.xp, 4250);
assert.strictEqual(srvCleaned.streak, 14);
assert.deepStrictEqual(Array.from(srvCleaned.readNotes), ['К-001', 'К-004']);
assert.deepStrictEqual(Array.from(srvCleaned.reviewedDecks), ['Ф-001', 'Ф-005']);
assert.strictEqual(srvCleaned.noteSrs['К-004'].step, 2);
assert.strictEqual(srvCleaned.cardSrs['Ф-025:3'].reps, 3);
assert.strictEqual(srvCleaned.cardRatings['Ф-025:3'], 4);
assert.strictEqual(srvCleaned.completedNoteSteps['К-004:1'], true);
assert.strictEqual(srvCleaned.unlockedChunks['skill:К-005:1:2'], true);
assert.strictEqual(srvCleaned.unlockedChunks['lesson:1.1:0:1'], true);
assert.strictEqual(srvCleaned.bugReports.length, 1);
assert.strictEqual(srvCleaned.bugReports[0].text, 'Баг отступа на мобилке');

const liveDumpPath = path.join(rootDir, 'data', 'phone_live_state_dump.json');
let liveAcademyRaw = null;
if (fs.existsSync(liveDumpPath)) {
  const dump = JSON.parse(fs.readFileSync(liveDumpPath, 'utf8'));
  liveAcademyRaw = typeof dump.academy_state_v1 === 'string'
    ? JSON.parse(dump.academy_state_v1)
    : dump.academy_state_v1;
  const liveSrv = srvCtx.sanitizeAcademyStateServer(JSON.parse(JSON.stringify(liveAcademyRaw)));
  const liveSrvJson = JSON.stringify(liveSrv);
  assert.strictEqual((liveSrvJson.match(/\uFFFD/g) || []).length, 0, 'server.js оставил U+FFFD в живом дампе');
  assert(Buffer.byteLength(liveSrvJson, 'utf8') < 250 * 1024, 'Стейт живого дампа в server.js превысил 250 КБ');
}

// =========================================================================
// 3. Запуск клиентского SPA в Node VM при innerWidth = 390
// =========================================================================
const inlineScripts = [];
const scriptRe = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let sm;
while ((sm = scriptRe.exec(htmlRaw)) !== null) {
  const attrs = sm[1] || '';
  if (/\bsrc\s*=|\btype\s*=\s*["']application\/json["']/i.test(attrs)) continue;
  inlineScripts.push(sm[2]);
}

function makeFakeElement(tag, id, cls) {
  const attrs = new Map();
  if (id) attrs.set('id', id);
  if (cls) attrs.set('class', cls);
  const classSet = new Set((cls || '').split(/\s+/).filter(Boolean));
  const el = {
    tagName: (tag || 'DIV').toUpperCase(),
    id: id || '',
    isConnected: true,
    dataset: {},
    style: { setProperty() {}, removeProperty() {} },
    children: [],
    _innerHTML: '',
    textContent: '',
    value: '',
    offsetWidth: 360,
    scrollHeight: 120,
    classList: {
      add(...cs) { cs.forEach(c => classSet.add(c)); },
      remove(...cs) { cs.forEach(c => classSet.delete(c)); },
      toggle(c, force) {
        const on = force === undefined ? !classSet.has(c) : !!force;
        if (on) classSet.add(c); else classSet.delete(c);
        return on;
      },
      contains(c) { return classSet.has(c); }
    },
    get className() { return Array.from(classSet).join(' '); },
    set className(v) {
      classSet.clear();
      String(v || '').split(/\s+/).filter(Boolean).forEach(c => classSet.add(c));
    },
    get innerHTML() { return el._innerHTML; },
    set innerHTML(val) { el._innerHTML = String(val || ''); },
    getAttribute(k) { return attrs.has(k) ? attrs.get(k) : null; },
    setAttribute(k, v) { attrs.set(k, String(v)); },
    removeAttribute(k) { attrs.delete(k); },
    hasAttribute(k) { return attrs.has(k); },
    addEventListener() {},
    removeEventListener() {},
    appendChild(c) { el.children.push(c); return c; },
    insertAdjacentElement() {},
    remove() {},
    scrollIntoView() {},
    closest() { return null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    animate() { return { onfinish: null }; }
  };
  return el;
}

const byId = new Map();
function ensureId(id, tag = 'div', cls = '') {
  if (!byId.has(id)) byId.set(id, makeFakeElement(tag, id, cls));
  return byId.get(id);
}

const viewRoot = ensureId('view-root', 'div');
const navDesktop = ensureId('nav-desktop', 'div');
const sidebarHero = ensureId('sidebar-hero-action-container', 'div');
ensureId('streak-num-d', 'span');
ensureId('streak-num-m', 'span');
ensureId('topbar-sound-btn', 'button');

let tabbarHtmlWrites = 0;
const tabbarEl = makeFakeElement('nav', '', 'tabbar');
tabbarEl._tabItems = [];
Object.defineProperty(tabbarEl, 'innerHTML', {
  get() { return tabbarEl._innerHTML; },
  set(v) {
    tabbarHtmlWrites += 1;
    tabbarEl._innerHTML = String(v || '');
    const routes = [];
    const rRe = /data-route="([^"]+)"/g;
    let rm;
    while ((rm = rRe.exec(tabbarEl._innerHTML)) !== null) routes.push(rm[1]);
    tabbarEl._tabItems = routes.map(rt => {
      const item = makeFakeElement('a', '', 'tabbar__item');
      item.setAttribute('data-route', rt);
      const wrap = makeFakeElement('span', '', 'tabbar__icon-wrap');
      item.querySelector = sel => sel === '.tabbar__icon-wrap' ? wrap : null;
      return item;
    });
  }
});
tabbarEl.querySelectorAll = sel => sel === '.tabbar__item' ? tabbarEl._tabItems : [];

const theoryCard = makeFakeElement('div', '', 'srs-note-card-clean');
const theoryH2Span = makeFakeElement('span', '', '');
const theoryCtaBtn = makeFakeElement('button', '', 'btn-glass-emerald btn-dock-cta-single');
const theorySrStep = makeFakeElement('span', '', 'sr-only');
const theoryFeed = makeFakeElement('div', 'py-theory-text', 'scroll-feed');
const theoryBeads = makeFakeElement('div', 'py-quanta-beads', 'dock-quanta-beads-row');
theoryFeed.closest = sel => sel === '.srs-note-card-clean' ? theoryCard : null;
theoryCard.querySelector = sel => {
  if (sel === 'h2 > span' || sel === 'h2') return theoryH2Span;
  if (sel === '.btn-dock-cta-single') return theoryCtaBtn;
  return null;
};

const srsCard = makeFakeElement('div', 'srs-active-card', 'fc-card');
const srsFront = makeFakeElement('div', '', 'fc-card-front');
const srsBack = makeFakeElement('div', '', 'fc-card-back');
srsCard.querySelector = sel => sel === '.fc-card-front' ? srsFront : (sel === '.fc-card-back' ? srsBack : null);

const lsStore = new Map();
const initialSeed = liveAcademyRaw || dirtyState;
lsStore.set('academy_state_v1', JSON.stringify(initialSeed));
const localStorageObj = {
  getItem(k) { return lsStore.has(k) ? lsStore.get(k) : null; },
  setItem(k, v) { lsStore.set(k, String(v)); },
  removeItem(k) { lsStore.delete(k); },
  get length() { return lsStore.size; },
  key(i) { return Array.from(lsStore.keys())[i] || null; }
};

const listeners = {};
const docEl = {
  classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
  setAttribute() {},
  getAttribute() { return null; },
  removeAttribute() {}
};

const sandbox = {
  console,
  Math,
  Date,
  JSON,
  Array,
  Object,
  String,
  Number,
  Boolean,
  RegExp,
  Map,
  Set,
  WeakMap,
  Error,
  Promise,
  parseInt,
  parseFloat,
  isNaN,
  isFinite,
  encodeURIComponent,
  decodeURIComponent,
  setTimeout: () => 1,
  clearTimeout: () => {},
  setInterval: () => 1,
  clearInterval: () => {},
  requestAnimationFrame: cb => { if (cb) cb(0); return 1; },
  performance: { now: () => Number(process.hrtime.bigint()) / 1e6 },
  localStorage: localStorageObj,
  sessionStorage: localStorageObj,
  location: { hash: '#/', pathname: '/academy.html', href: 'http://localhost:8000/academy.html#/' },
  history: { replaceState() {}, pushState() {} },
  navigator: { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile' },
  AudioContext: null,
  webkitAudioContext: null,
  fetch: () => Promise.resolve({ ok: false, status: 503, json: async () => ({}) }),
  matchMedia: () => ({ matches: false, addListener() {}, addEventListener() {} }),
  document: {
    documentElement: docEl,
    body: makeFakeElement('body', '', ''),
    activeElement: null,
    readyState: 'complete',
    createElement: tag => makeFakeElement(tag),
    getElementById(id) {
      if (id === 'py-theory-text') return /id="py-theory-text"/.test(viewRoot._innerHTML) ? theoryFeed : null;
      if (id === 'py-quanta-beads') return /id="py-quanta-beads"/.test(viewRoot._innerHTML) ? theoryBeads : null;
      if (id === 'srs-active-card') return /id="srs-active-card"/.test(viewRoot._innerHTML) ? srsCard : null;
      return ensureId(id, 'div');
    },
    querySelector(sel) {
      if (sel === '.echelon-clean-meta .sr-only') return theorySrStep;
      if (sel === '.sprint-finish-celebration, .sprint-celebration-banner, .step-check-box') return null;
      if (sel === '.tabbar') return tabbarEl;
      return null;
    },
    querySelectorAll(sel) {
      if (sel === '.tabbar') return [tabbarEl];
      return [];
    },
    addEventListener(ev, fn) { (listeners[ev] = listeners[ev] || []).push(fn); }
  },
  innerWidth: 390,
  innerHeight: 844,
  scrollY: 0,
  scrollTo() {},
  name: JSON.stringify({ v: 1, s: dirtyState }),
  addEventListener(ev, fn) { (listeners[ev] = listeners[ev] || []).push(fn); }
};
sandbox.window = sandbox;
sandbox.self = sandbox;
sandbox.globalThis = sandbox;

vm.createContext(sandbox);
for (const code of inlineScripts) {
  vm.runInContext(code, sandbox);
}

// Проверяем клиентскую санитизацию грязного dirtyState (и live dump, если был загружен)
const clientJson = JSON.stringify(sandbox.state);
assert.strictEqual((clientJson.match(/\uFFFD/g) || []).length, 0, 'Клиентский state сохранил U+FFFD');
assert(Buffer.byteLength(clientJson, 'utf8') < 250 * 1024, 'Клиентский state превысил бюджет 250 КБ');
assert(sandbox.state.xp >= dirtyState.xp, 'Клиентская санитизация потеряла xp');

const explicitSanitized = sandbox.sanitizeAcademyState(JSON.parse(JSON.stringify(dirtyState)));
const explicitJson = JSON.stringify(explicitSanitized);
assert.strictEqual((explicitJson.match(/\uFFFD/g) || []).length, 0, 'sanitizeAcademyState оставил U+FFFD');
assert(Buffer.byteLength(explicitJson, 'utf8') < 250 * 1024, 'sanitizeAcademyState превысил 250 КБ');
assert.strictEqual(explicitSanitized.noteSrs['К-004'].step, 2);
assert.strictEqual(explicitSanitized.cardSrs['Ф-025:3'].reps, 3);
assert.strictEqual(explicitSanitized.completedNoteSteps['К-004:1'], true);
assert.strictEqual(explicitSanitized.unlockedChunks['skill:К-005:1:2'], true);

// Сбрасываем таббар-счётчик после стартовых инициализаций и проверяем чистые маршруты на 390px
tabbarHtmlWrites = 0;
navDesktop._innerHTML = '';
sidebarHero._innerHTML = '';

for (const route of ['#/', '#/path', '#/python/skill/1.1.1', '#/cards']) {
  sandbox.location.hash = route;
  sandbox.render(); // прогрев
  const t0 = Number(process.hrtime.bigint());
  for (let i = 0; i < 5; i++) sandbox.render();
  const avgMs = (Number(process.hrtime.bigint()) - t0) / 1e6 / 5;
  assert(avgMs < 30, `Слишком медленный render(${route}) на 390px: ${avgMs.toFixed(2)} ms (потолок 30 ms)`);
}

assert.strictEqual(navDesktop._innerHTML, '', 'При 390px #nav-desktop не должен перестраиваться');
assert.strictEqual(sidebarHero._innerHTML, '', 'При 390px #sidebar-hero-action-container не должен перестраиваться');
assert.strictEqual(sandbox.__desktopSidebarNeedsSync, true, 'При 390px должен выставляться __desktopSidebarNeedsSync = true');
assert(tabbarHtmlWrites <= 1, `.tabbar.innerHTML не должен перезаписываться на каждом переходе (записей: ${tabbarHtmlWrites})`);

// =========================================================================
// 4. Проверка in-place переходов и защиты от двойного render()
// =========================================================================
function makeTapEvent(matchMap) {
  const mkNode = (selMatched) => ({
    getAttribute: (k) => (matchMap[selMatched] && matchMap[selMatched][k] !== undefined) ? matchMap[selMatched][k] : null,
    hasAttribute: (k) => !!(matchMap[selMatched] && matchMap[selMatched][k] !== undefined),
    setAttribute() {},
    removeAttribute() {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    closest: (sel) => (matchMap[sel] !== undefined ? mkNode(sel) : null)
  });
  return {
    isTrusted: true,
    preventDefault() {},
    stopPropagation() {},
    target: {
      closest(sel) {
        for (const key of Object.keys(matchMap)) {
          if (sel === key || sel.split(',').map(s => s.trim()).includes(key)) {
            return mkNode(key);
          }
        }
        return null;
      }
    }
  };
}

let rootHtmlWrites = 0;
Object.defineProperty(viewRoot, 'innerHTML', {
  get() { return viewRoot._innerHTML; },
  set(val) { rootHtmlWrites += 1; viewRoot._innerHTML = String(val || ''); }
});

// Доводим до конца extended-click хендлер 1 нейтральным кликом, чтобы window.patch* гарантированно экспортировались
(listeners.click || []).forEach(fn => fn(makeTapEvent({ '.nonexistent-noop': {} })));

// А) Теория навыка: шаги обязаны переключаться in-place с 0 перезаписей #view-root
sandbox.location.hash = '#/python/skill/1.1.1';
sandbox.render();
assert(/id="py-theory-text"/.test(viewRoot._innerHTML), 'На #/python/skill/1.1.1 ожидался блок #py-theory-text');

rootHtmlWrites = 0;
(listeners.click || []).forEach(fn => fn(makeTapEvent({ '[data-py-step]': { 'data-py-step': '0' } })));
(listeners.click || []).forEach(fn => fn(makeTapEvent({ '[data-py-next-step]': { 'data-py-next-step': '1' } })));
(listeners.click || []).forEach(fn => fn(makeTapEvent({ '[data-py-jump-step]': { 'data-py-jump-step': '0' } })));
assert.strictEqual(sandbox.patchPySkillTheoryStepInPlace(), true, 'patchPySkillTheoryStepInPlace() обязан возвращать true');
assert.strictEqual(rootHtmlWrites, 0, 'Смена шагов теории обязана идти in-place без перестройки #view-root');

// Б) Карточки в навыке и в центре #/cards
(listeners.click || []).forEach(fn => fn(makeTapEvent({ '[data-py-tab]': { 'data-py-tab': 'cards' } })));
if (/id="srs-active-card"/.test(viewRoot._innerHTML)) {
  rootHtmlWrites = 0;
  assert.strictEqual(sandbox.patchPySkillCardInPlace(), true, 'patchPySkillCardInPlace() обязан возвращать true');
  assert.strictEqual(rootHtmlWrites, 0, 'patchPySkillCardInPlace() не должен перестраивать #view-root');
}

sandbox.location.hash = '#/cards';
sandbox.render();
if (/id="srs-active-card"/.test(viewRoot._innerHTML)) {
  rootHtmlWrites = 0;
  assert.strictEqual(sandbox.patchSrsActiveCardInPlace(), true, 'patchSrsActiveCardInPlace() обязан возвращать true');
  assert.strictEqual(rootHtmlWrites, 0, 'patchSrsActiveCardInPlace() не должен перестраивать #view-root');
}

// В) Переход по .tabbar__item + немедленный hashchange = строго 1 рендер
sandbox.location.hash = '#/';
sandbox.render();
rootHtmlWrites = 0;
(listeners.click || []).forEach(fn => fn(makeTapEvent({ '.tabbar__item': { 'data-route': '/path' } })));
assert.strictEqual(sandbox.location.hash, '#/path');
assert.strictEqual(rootHtmlWrites, 1, 'Клик .tabbar__item должен немедленно выполнить ровно 1 render()');
(listeners.hashchange || []).forEach(fn => fn());
assert.strictEqual(rootHtmlWrites, 1, 'Сразу следующий hashchange не должен запускать дублирующий render()');

console.log('✓ [Pre-Commit] Мобильный отклик (INP Guard) и бюджет стейта проверены со 100% успехом.');
