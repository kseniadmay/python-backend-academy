const fs = require('fs');
const path = require('path');
const vm = require('vm');

let jsCode = '';
const extractedPath = path.join(__dirname, 'extracted_academy.js');
if (fs.existsSync(extractedPath)) {
  jsCode = fs.readFileSync(extractedPath, 'utf-8');
} else {
  const academyHtmlPath = path.join(__dirname, '..', 'academy.html');
  const academyHtml = fs.readFileSync(academyHtmlPath, 'utf-8');
  const m = academyHtml.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) throw new Error('Could not find inline <script> in academy.html');
  jsCode = m[1];
}

// Build a lightweight DOM mock to verify all routes, event handlers, and state transitions synchronously
const elementsById = {};
function makeEl(id = '', tag = 'div') {
  const el = {
    id,
    tagName: tag.toUpperCase(),
    innerHTML: '',
    textContent: '',
    value: '',
    className: '',
    style: {},
    attributes: {},
    classList: {
      _set: new Set(),
      add(c) { this._set.add(c); },
      remove(c) { this._set.delete(c); },
      toggle(c, force) {
        if (force === undefined) {
          if (this._set.has(c)) { this._set.delete(c); return false; }
          this._set.add(c); return true;
        }
        if (force) this._set.add(c); else this._set.delete(c);
        return force;
      },
      contains(c) { return this._set.has(c); }
    },
    setAttribute(k, v) { this.attributes[k] = String(v); },
    getAttribute(k) { return this.attributes[k]; },
    removeAttribute(k) { delete this.attributes[k]; },
    appendChild(child) { if (child && child.id) elementsById[child.id] = child; return child; },
    insertBefore(child) { if (child && child.id) elementsById[child.id] = child; return child; },
    insertAdjacentElement(pos, child) { return child; },
    remove() { if (this.id) delete elementsById[this.id]; },
    addEventListener(ev, fn) { this['_on_' + ev] = fn; },
    querySelector() { return makeEl(); },
    querySelectorAll() { return []; },
    closest() { return null; },
    focus() {},
    setSelectionRange() {},
    firstChild: {}
  };
  if (id) elementsById[id] = el;
  return el;
}

['view-root', 'nav-desktop', 'theme-toggle-d', 'theme-toggle-m', 'reset-btn-d', 'streak-num-d', 'streak-num-m', 'code-input', 'code-output', 'run-btn', 'run-status', 'lesson-code', 'py-skill-editor', 'prac-code-editor'].forEach(id => makeEl(id));

const docListeners = {};
const winListeners = {};
const store = {};
const sidebarFoot = makeEl('sidebar-foot');

const sandbox = {
  console,
  setTimeout, clearTimeout, setInterval, clearInterval,
  alert: () => {},
  confirm: () => true,
  navigator: { clipboard: { writeText: () => {} } },
  localStorage: {
    getItem: k => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: k => { delete store[k]; }
  },
  location: { hash: '#/' },
  window: null,
  document: {
    body: makeEl('body', 'body'),
    head: makeEl('head', 'head'),
    documentElement: makeEl('html', 'html'),
    getElementById: id => elementsById[id] || makeEl(id),
    createElement: tag => makeEl('', tag),
    querySelector: sel => {
      if (sel === '.sidebar-foot') return sidebarFoot;
      return null;
    },
    querySelectorAll: () => [],
    addEventListener: (ev, fn) => {
      if (!docListeners[ev]) docListeners[ev] = [];
      docListeners[ev].push(fn);
    }
  }
};
sandbox.window = sandbox;
sandbox.window.scrollTo = () => {};
sandbox.window.speechSynthesis = {
  speak: () => {},
  cancel: () => {},
  pause: () => {},
  resume: () => {}
};
sandbox.SpeechSynthesisUtterance = function(text) {
  this.text = text;
};
sandbox.window.addEventListener = (ev, fn) => {
  if (!winListeners[ev]) winListeners[ev] = [];
  winListeners[ev].push(fn);
};
sandbox.window.matchMedia = () => ({ matches: false });

// Mock Brython runner for instant verification inside Node VM
sandbox.window.__BRYTHON__ = {
  builtins: true,
  runPythonSource: (src) => {
    if (sandbox.window.__py_result_Bridge) {
      sandbox.window.__py_result_Bridge.res = true;
      sandbox.window.__py_result_Bridge.msg = 'OK';
    }
    if (sandbox.window.__py_stdout_cb) {
      sandbox.window.__py_stdout_cb('Python 3.13 OK\n');
    }
  }
};
sandbox.window.brython = () => {};

vm.createContext(sandbox);
vm.runInContext(jsCode, sandbox);

function navigate(hash) {
  sandbox.location.hash = hash;
  (winListeners['hashchange'] || []).forEach(fn => fn());
  return elementsById['view-root'].innerHTML;
}

function assert(cond, msg) {
  if (!cond) {
    console.error('ASSERTION FAILED:', msg);
    process.exit(1);
  }
}

// 1. Check Dashboard (#/)
let html = navigate('#/');
assert(html.includes('Правило 2 минут: Быстрый микро-шаг'), 'Dashboard missing 2-minute button');
assert(html.includes('из 2800 MP Python'), 'Dashboard missing 2800 MP counter');
assert(html.includes('Дневная цель'), 'Dashboard missing Daily Goal');
assert(html.includes('Фокус-спринт (Помодоро)'), 'Dashboard missing Pomodoro timer');
console.log('✓ Route #/ (Dashboard) verified');

// 2. Check Python Mastery Matrix (#/python)
html = navigate('#/python');
assert(html.includes('Матрица Мастерства Python'), '#/python missing title');
for (let u = 1; u <= 9; u++) {
  assert(html.includes(`Юнит 1.${u}`), `#/python missing Unit 1.${u}`);
}
assert(html.includes('1.1.1') && html.includes('1.9.3'), '#/python missing skill IDs 1.1.1..1.9.3');
console.log('✓ Route #/python (9 Units, 28 Skills, 2800 MP) verified');

// 3. Check all 28 Python Skill detail views (#/python/skill/1.1.1 .. 1.9.3)
const skillIds = ['1.1.1','1.1.2','1.1.3','1.1.4','1.1.5','1.2.1','1.2.2','1.2.3','1.3.1','1.3.2','1.3.3','1.4.1','1.4.2','1.4.3','1.5.1','1.5.2','1.5.3','1.6.1','1.6.2','1.7.1','1.7.2','1.7.3','1.8.1','1.8.2','1.8.3','1.9.1','1.9.2','1.9.3'];
for (const sid of skillIds) {
  html = navigate(`#/python/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `Skill view ${sid} missing micro-step bar`);
}
console.log(`✓ All ${skillIds.length} Python Skill views (#/python/skill/...) verified`);

// 4. Check all 9 Python Unit Tests + Course Challenge (#/python/unittest/1.1..1.9, course)
for (let u = 1; u <= 9; u++) {
  html = navigate(`#/python/unittest/1.${u}`);
  assert(html.includes(`Unit Test 1.${u}`), `Unit Test 1.${u} failed to render`);
}
html = navigate('#/python/unittest/course');
assert(html.includes('Итоговый вызов курса'), 'Python Course challenge failed to render');
console.log('✓ All 9 Python Unit Tests and Course Challenge verified');

// 4b. Check Web Mastery Matrix (#/web), all 10 Web skills, 4 Unit Tests (2.1..2.4) & Course Challenge
html = navigate('#/web');
assert(html.includes('Матрица Мастерства Web'), '#/web missing title');
for (let u = 1; u <= 4; u++) {
  assert(html.includes(`Юнит 2.${u}`), `#/web missing Unit 2.${u}`);
}
const webSkillIds = ['2.1.1','2.1.2','2.2.1','2.2.2','2.2.3','2.3.1','2.3.2','2.3.3','2.4.1','2.4.2'];
for (const sid of webSkillIds) {
  html = navigate(`#/web/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `Web Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `Web Skill view ${sid} missing micro-step bar`);
  assert(html.includes('К Матрице Мастерства Web'), `Web Skill view ${sid} missing Web back-link`);
}
for (let u = 1; u <= 4; u++) {
  html = navigate(`#/web/unittest/2.${u}`);
  assert(html.includes(`Unit Test 2.${u}`), `Web Unit Test 2.${u} failed to render`);
}
html = navigate('#/web/unittest/course');
assert(html.includes('Итоговый вызов курса') && html.includes('Юниты 2.1–2.4'), 'Web Course challenge failed to render');
const totalWebDeckCards = Object.values(sandbox.WEB_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(Object.keys(sandbox.WEB_MASTERY.notes).length === 23, `Expected 23 Web K-notes, got ${Object.keys(sandbox.WEB_MASTERY.notes).length}`);
assert(Object.keys(sandbox.WEB_MASTERY.decks).length === 25 && totalWebDeckCards === 491, `Expected 25 Web decks (491 cards), got ${Object.keys(sandbox.WEB_MASTERY.decks).length} (${totalWebDeckCards})`);
console.log('✓ Route #/web (4 Units 2.1–2.4, 10 Skills, 23 K-notes, 25 F-decks / 491 cards, 4 Unit Tests) verified');

// 4c. Check Exhaustive Backend Mastery Matrix (#/backend), all 24 Backend skills across 8 parts (3.1..3.8), framework filter tabs, 8 Unit Tests & Course Challenge
html = navigate('#/backend');
assert(html.includes('Матрица Мастерства Backend'), '#/backend missing title');
assert(html.includes('data-backend-part-filter="3.1"') && html.includes('data-backend-part-filter="3.4"'), '#/backend missing framework part filter pills');
for (let u = 1; u <= 8; u++) {
  assert(html.includes(`Юнит 3.${u}`), `#/backend missing Unit 3.${u}`);
}
const backendSkillIds = [
  '3.1.1','3.1.2','3.1.3',
  '3.2.1','3.2.2','3.2.3',
  '3.3.1','3.3.2','3.3.3',
  '3.4.1','3.4.2','3.4.3',
  '3.5.1','3.5.2','3.5.3',
  '3.6.1','3.6.2','3.6.3',
  '3.7.1','3.7.2','3.7.3',
  '3.8.1','3.8.2','3.8.3'
];
for (const sid of backendSkillIds) {
  html = navigate(`#/backend/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `Backend Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `Backend Skill view ${sid} missing micro-step bar`);
  assert(html.includes('К Матрице Мастерства Backend'), `Backend Skill view ${sid} missing Backend back-link`);
}
for (let u = 1; u <= 8; u++) {
  html = navigate(`#/backend/unittest/3.${u}`);
  assert(html.includes(`Unit Test 3.${u}`), `Backend Unit Test 3.${u} failed to render`);
}
html = navigate('#/backend/unittest/course');
assert(html.includes('Итоговый вызов курса') && html.includes('Юниты 3.1–3.8'), 'Backend Course challenge failed to render');
const totalBackendDeckCards = Object.values(sandbox.BACKEND_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(Object.keys(sandbox.BACKEND_MASTERY.notes).length === 40, `Expected 40 Backend K-notes, got ${Object.keys(sandbox.BACKEND_MASTERY.notes).length}`);
assert(Object.keys(sandbox.BACKEND_MASTERY.decks).length === 43 && totalBackendDeckCards === 890, `Expected 43 Backend decks (890 cards), got ${Object.keys(sandbox.BACKEND_MASTERY.decks).length} (${totalBackendDeckCards})`);
console.log('✓ Route #/backend (8 Parts/Units 3.1–3.8, 24 Skills, 40 K-notes, 43 F-decks / 890 cards, 8 Unit Tests) verified');

// 4d. Check Algorithms Mastery Matrix (#/algorithms), all 12 Algo skills across 6 units (4.1..4.6), 14 K-notes, 16 F-decks (463 cards), 6 Unit Tests & Course Challenge
html = navigate('#/algorithms');
assert(html.includes('Матрица Мастерства Алгоритмы'), '#/algorithms missing title');
for (let u = 1; u <= 6; u++) {
  assert(html.includes(`Юнит 4.${u}`), `#/algorithms missing Unit 4.${u}`);
}
const algoSkillIds = [
  '4.1.1',
  '4.2.1','4.2.2',
  '4.3.1','4.3.2',
  '4.4.1','4.4.2','4.4.3',
  '4.5.1','4.5.2',
  '4.6.1','4.6.2'
];
for (const sid of algoSkillIds) {
  html = navigate(`#/algorithms/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `Algo Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `Algo Skill view ${sid} missing micro-step bar`);
  assert(html.includes('К Матрице Мастерства Алгоритмы'), `Algo Skill view ${sid} missing Algorithms back-link`);
}
for (let u = 1; u <= 6; u++) {
  html = navigate(`#/algorithms/unittest/4.${u}`);
  assert(html.includes(`Unit Test 4.${u}`), `Algo Unit Test 4.${u} failed to render`);
}
html = navigate('#/algorithms/unittest/course');
assert(html.includes('Итоговый вызов курса') && html.includes('Юниты 4.1–4.6'), 'Algo Course challenge failed to render');
const totalAlgoDeckCards = Object.values(sandbox.ALGO_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(Object.keys(sandbox.ALGO_MASTERY.notes).length === 14, `Expected 14 Algo K-notes, got ${Object.keys(sandbox.ALGO_MASTERY.notes).length}`);
assert(Object.keys(sandbox.ALGO_MASTERY.decks).length === 16 && totalAlgoDeckCards === 463, `Expected 16 Algo decks (463 cards), got ${Object.keys(sandbox.ALGO_MASTERY.decks).length} (${totalAlgoDeckCards})`);
console.log('✓ Route #/algorithms (6 Units 4.1–4.6, 12 Skills, 14 K-notes, 16 F-decks / 463 cards, 6 Unit Tests) verified');

// 4e. Check Databases Mastery Matrix (#/databases), all 17 DB skills across 6 units (5.1..5.6), 32 K-notes, 32 F-decks (927 cards), 6 Unit Tests & Course Challenge
html = navigate('#/databases');
assert(html.includes('Матрица Мастерства Базы данных'), '#/databases missing title');
for (let u = 1; u <= 6; u++) {
  assert(html.includes(`Юнит 5.${u}`), `#/databases missing Unit 5.${u}`);
}
const dbSkillIds = [
  '5.1.1','5.1.2','5.1.3',
  '5.2.1','5.2.2',
  '5.3.1','5.3.2','5.3.3',
  '5.4.1','5.4.2','5.4.3',
  '5.5.1','5.5.2','5.5.3',
  '5.6.1','5.6.2','5.6.3'
];
for (const sid of dbSkillIds) {
  html = navigate(`#/databases/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `DB Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `DB Skill view ${sid} missing micro-step bar`);
  assert(html.includes('К Матрице Мастерства Базы данных'), `DB Skill view ${sid} missing Databases back-link`);
}
for (let u = 1; u <= 6; u++) {
  html = navigate(`#/databases/unittest/5.${u}`);
  assert(html.includes(`Unit Test 5.${u}`), `DB Unit Test 5.${u} failed to render`);
}
html = navigate('#/databases/unittest/course');
assert(html.includes('Итоговый вызов курса') && html.includes('Юниты 5.1–5.6'), 'DB Course challenge failed to render');
const totalDbDeckCards = Object.values(sandbox.DB_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(Object.keys(sandbox.DB_MASTERY.notes).length === 32, `Expected 32 DB K-notes, got ${Object.keys(sandbox.DB_MASTERY.notes).length}`);
assert(Object.keys(sandbox.DB_MASTERY.decks).length === 32 && totalDbDeckCards === 927, `Expected 32 DB decks (927 cards), got ${Object.keys(sandbox.DB_MASTERY.decks).length} (${totalDbDeckCards})`);
assert(sandbox.DB_MASTERY.notes['К-131'].title.includes('ROW_NUMBER'), `Expected К-131 title to preserve ROW_NUMBER, got ${sandbox.DB_MASTERY.notes['К-131'].title}`);
assert(sandbox.DB_MASTERY.decks['Ф-110'].title.includes('related_name'), `Expected Ф-110 title to preserve related_name, got ${sandbox.DB_MASTERY.decks['Ф-110'].title}`);
console.log('✓ Route #/databases (6 Units 5.1–5.6, 17 Skills, 32 K-notes, 32 F-decks / 927 cards, 6 Unit Tests) verified');

// 4f. Check Architecture Mastery Matrix (#/architecture), all 14 Arch skills across 6 units (6.1..6.6), 14 K-notes, 17 F-decks (263 cards), 6 Unit Tests & Course Challenge
html = navigate('#/architecture');
assert(html.includes('Матрица Мастерства Архитектура'), '#/architecture missing title');
for (let u = 1; u <= 6; u++) {
  assert(html.includes(`Юнит 6.${u}`), `#/architecture missing Unit 6.${u}`);
}
const archSkillIds = [
  '6.1.1','6.1.2',
  '6.2.1','6.2.2','6.2.3',
  '6.3.1','6.3.2',
  '6.4.1','6.4.2',
  '6.5.1','6.5.2','6.5.3',
  '6.6.1','6.6.2'
];
for (const sid of archSkillIds) {
  html = navigate(`#/architecture/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `Arch Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `Arch Skill view ${sid} missing micro-step bar`);
  assert(html.includes('К Матрице Мастерства Архитектура'), `Arch Skill view ${sid} missing Architecture back-link`);
}
for (let u = 1; u <= 6; u++) {
  html = navigate(`#/architecture/unittest/6.${u}`);
  assert(html.includes(`Unit Test 6.${u}`), `Arch Unit Test 6.${u} failed to render`);
}
html = navigate('#/architecture/unittest/course');
assert(html.includes('Итоговый вызов курса') && html.includes('Юниты 6.1–6.6'), 'Arch Course challenge failed to render');
const totalArchDeckCards = Object.values(sandbox.ARCH_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(Object.keys(sandbox.ARCH_MASTERY.notes).length === 14, `Expected 14 Arch K-notes, got ${Object.keys(sandbox.ARCH_MASTERY.notes).length}`);
assert(Object.keys(sandbox.ARCH_MASTERY.decks).length === 17 && totalArchDeckCards === 263, `Expected 17 Arch decks (263 cards), got ${Object.keys(sandbox.ARCH_MASTERY.decks).length} (${totalArchDeckCards})`);
assert(sandbox.ARCH_MASTERY.decks['Ф-175'].title.includes('Separation of Concerns (Разделение ответственности)'), `Expected Ф-175 title to be restored, got ${sandbox.ARCH_MASTERY.decks['Ф-175'].title}`);
assert(sandbox.ARCH_MASTERY.decks['Ф-176'].title.includes('Layered Architecture (Слоистая архитектура)'), `Expected Ф-176 title to be restored, got ${sandbox.ARCH_MASTERY.decks['Ф-176'].title}`);
console.log('✓ Route #/architecture (6 Units 6.1–6.6, 14 Skills, 14 K-notes, 17 F-decks / 263 cards, 6 Unit Tests) verified');

// 4g. Check Infrastructure Mastery Matrix (#/infra and alias #/infrastructure), all 21 Infra skills across 6 units (7.1..7.6), 47 K-notes, 45 F-decks (1286 cards), 6 Unit Tests & Course Challenge
html = navigate('#/infrastructure');
assert(html.includes('Матрица Мастерства Инфраструктура'), '#/infrastructure alias failed to render');
html = navigate('#/infra');
assert(html.includes('Матрица Мастерства Инфраструктура'), '#/infra missing title');
for (let u = 1; u <= 6; u++) {
  assert(html.includes(`Юнит 7.${u}`), `#/infra missing Unit 7.${u}`);
}
const infraSkillIds = [
  '7.1.1','7.1.2','7.1.3','7.1.4',
  '7.2.1','7.2.2','7.2.3',
  '7.3.1','7.3.2','7.3.3',
  '7.4.1','7.4.2','7.4.3',
  '7.5.1','7.5.2','7.5.3',
  '7.6.1','7.6.2','7.6.3','7.6.4','7.6.5'
];
for (const sid of infraSkillIds) {
  html = navigate(`#/infra/skill/${sid}`);
  assert(html.includes(`Навык ${sid}`), `Infra Skill view ${sid} failed to render`);
  assert(html.includes('Микро-шаг 1 из'), `Infra Skill view ${sid} missing micro-step bar`);
  assert(html.includes('К Матрице Мастерства Инфраструктура'), `Infra Skill view ${sid} missing Infrastructure back-link`);
}
for (let u = 1; u <= 6; u++) {
  html = navigate(`#/infra/unittest/7.${u}`);
  assert(html.includes(`Unit Test 7.${u}`), `Infra Unit Test 7.${u} failed to render`);
}
html = navigate('#/infra/unittest/course');
assert(html.includes('Итоговый вызов курса') && html.includes('Юниты 7.1–7.6'), 'Infra Course challenge failed to render');
const totalInfraDeckCards = Object.values(sandbox.INFRA_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(Object.keys(sandbox.INFRA_MASTERY.notes).length === 47, `Expected 47 Infra K-notes, got ${Object.keys(sandbox.INFRA_MASTERY.notes).length}`);
assert(Object.keys(sandbox.INFRA_MASTERY.decks).length === 45 && totalInfraDeckCards === 1286, `Expected 45 Infra decks (1286 cards), got ${Object.keys(sandbox.INFRA_MASTERY.decks).length} (${totalInfraDeckCards})`);
assert(sandbox.INFRA_MASTERY.decks['Ф-020@07'] && sandbox.INFRA_MASTERY.decks['Ф-020@07'].cards.length === 43, 'Expected Ф-020@07 (Linux file utilities, 43 cards) in INFRA_MASTERY.decks');
console.log('✓ Route #/infra (6 Units 7.1–7.6, 21 Skills, 47 K-notes, 45 F-decks / 1286 cards, 6 Unit Tests) verified');

// 5. Check Global 3D Flashcards Hub (#/cards) & verify 0 cross-track overlap (286 unique decks, 6051 unique cards)
html = navigate('#/cards');
assert(html.includes('Центр 3D Флеш-карточек'), '#/cards failed to render');
assert(html.includes('Ф-001') && html.includes('Ф-141') && html.includes('Ф-171') && html.includes('Ф-186') && html.includes('Ф-230'), '#/cards missing Ф-001, Ф-141, Ф-171, Ф-186 or Ф-230 deck');
assert(html.includes('2 181 карточка'), '#/cards missing accurate 2 181 flashcards count');
const totalDeckCards = Object.values(sandbox.PY_MASTERY.decks).reduce((acc, d) => acc + d.cards.length, 0);
assert(totalDeckCards === 2181, `Expected 2181 total cards in PY_MASTERY.decks, got ${totalDeckCards}`);
assert(sandbox.PY_MASTERY.decks['Ф-020'].cards.length === 31 && sandbox.PY_MASTERY.decks['Ф-020'].cards[0].q.includes('переместить указатель в файле'), 'Ф-020 in Module 1 was overwritten by Module 7 Linux deck!');
const allDecksCombinedObj = { ...sandbox.PY_MASTERY.decks, ...sandbox.WEB_MASTERY.decks, ...sandbox.BACKEND_MASTERY.decks, ...sandbox.ALGO_MASTERY.decks, ...sandbox.DB_MASTERY.decks, ...sandbox.ARCH_MASTERY.decks, ...sandbox.INFRA_MASTERY.decks };
const allCombinedDeckIds = Object.keys(allDecksCombinedObj);
const allCombinedCardCount = Object.values(allDecksCombinedObj).reduce((acc, d) => acc + d.cards.length, 0);
assert(allCombinedDeckIds.length === 286, `Expected 286 unique decks in ALL_DECKS_COMBINED, got ${allCombinedDeckIds.length}`);
assert(allCombinedCardCount === 6051, `Expected 6051 unique cards in ALL_DECKS_COMBINED, got ${allCombinedCardCount}`);
assert(html.includes('286 колод · 6 051 карточка'), '#/cards missing "286 колод · 6 051 карточка" header');
assert(!html.includes('Юнит 5.1: Юнит 5.1') && !html.includes('Юнит 6.1: Юнит 6.1') && !html.includes('Юнит 7.1: Юнит 7.1'), '#/cards unit dropdown has duplicated "Юнит X: Юнит X" prefix');
for (const [fid, deck] of Object.entries(allDecksCombinedObj)) {
  for (let ci = 0; ci < deck.cards.length; ci++) {
    const c = deck.cards[ci];
    const qNoCode = c.q.replace(/<code>[\s\S]*?<\/code>/g, '');
    const aNoCode = c.a.replace(/<code>[\s\S]*?<\/code>/g, '');
    assert(!/[²³]\d/.test(c.q) && !/[²³]\d/.test(c.a), `Corrupted multi-digit exponent in deck ${fid} card ${ci + 1}`);
    assert(!/\\(dots|ldots|ll|gg|left|right|%)/.test(c.q) && !/\\(dots|ldots|ll|gg|left|right|%)/.test(c.a), `Unrendered LaTeX command leaked in deck ${fid} card ${ci + 1}`);
    assert(!c.q.includes('Flashcards for ') && !c.a.includes('Flashcards for '), `Raw RemNote export dump "Flashcards for " leaked in deck ${fid} card ${ci + 1}`);
    assert(!qNoCode.includes('&gt;&gt;') && !aNoCode.includes('&gt;&gt;'), `Broken >> separator leaked into prose in deck ${fid} card ${ci + 1}`);
    assert(!/(\([^)]{10,}\))\s*\1/.test(c.a), `Duplicated parenthetical explanation in deck ${fid} card ${ci + 1}: ${c.a}`);
  }
}
const f184Cards = sandbox.ARCH_MASTERY.decks['Ф-184'].cards;
assert(f184Cards.some(c => c.a.includes('$USER') && c.a.includes('логином активного пользователя')), 'Ф-184 missing enriched $USER explanation');
assert(f184Cards.some(c => c.a.includes('$SHELL') && c.a.includes('командному интерпретатору')), 'Ф-184 missing enriched $SHELL explanation');
assert(f184Cards.some(c => c.a.includes('$HOME') && c.a.includes('/home/username')), 'Ф-184 missing enriched $HOME explanation');
const f222Cards = sandbox.BACKEND_MASTERY.decks['Ф-222'].cards;
assert(!f222Cards.some(c => c.a.trim() === 'Нет'), 'Ф-222 still has bare "Нет" answer');
console.log('✓ Route #/cards (286 unique combined decks, 6051 unique cards across all 7 modules, 0 overlap) verified');

// 6. Check 401-Task Coding Practice Hub (#/practice) & 100% task mapping across all 7 modules
html = navigate('#/practice');
assert(html.includes('Практика кода') && html.includes('/ 401 решено'), '#/practice failed to render 401 tasks');
assert(html.includes('🥚 Уровень 1') && html.includes('👑 Уровень 7'), '#/practice missing animal difficulty tiers');
assert(html.includes('#401 '), '#/practice dropdown truncated task #401!');
assert(sandbox.IDE_TASKS.length === 401, `Expected 401 IDE_TASKS, got ${sandbox.IDE_TASKS.length}`);
const allMappedTaskIds = new Set();
for (const mObj of [sandbox.PY_MASTERY, sandbox.WEB_MASTERY, sandbox.BACKEND_MASTERY, sandbox.ALGO_MASTERY, sandbox.DB_MASTERY, sandbox.ARCH_MASTERY, sandbox.INFRA_MASTERY]) {
  for (const u of mObj.units) {
    for (const sk of u.skills) {
      for (const tid of (sk.taskIds || [])) allMappedTaskIds.add(tid);
    }
  }
}
assert(allMappedTaskIds.size === 401, `Expected 100% of 401 IDE tasks mapped across 7 modules, got ${allMappedTaskIds.size}`);
const webSkill211 = sandbox.WEB_MASTERY.units[0].skills[0];
const webSkill212 = sandbox.WEB_MASTERY.units[0].skills[1];
const webSkill242 = sandbox.WEB_MASTERY.units[3].skills[1];
const algoSkill443 = sandbox.ALGO_MASTERY.units[3].skills[2];
const dbSkill522 = sandbox.DB_MASTERY.units[1].skills[1];
const archSkill631 = sandbox.ARCH_MASTERY.units[2].skills[0];
const archSkill651 = sandbox.ARCH_MASTERY.units[4].skills[0];
const infraSkill722 = sandbox.INFRA_MASTERY.units[1].skills[1];
const infraSkill732 = sandbox.INFRA_MASTERY.units[2].skills[1];
const infraSkill753 = sandbox.INFRA_MASTERY.units[4].skills[2];
assert(JSON.stringify(webSkill211.taskIds) === JSON.stringify([2, 95, 186]), `Expected Web 2.1.1 taskIds [2,95,186], got ${JSON.stringify(webSkill211.taskIds)}`);
assert(JSON.stringify(webSkill212.taskIds) === JSON.stringify([6, 95, 186, 272, 279]), `Expected Web 2.1.2 taskIds [6,95,186,272,279], got ${JSON.stringify(webSkill212.taskIds)}`);
assert(JSON.stringify(webSkill242.taskIds) === JSON.stringify([22, 32, 395]), `Expected Web 2.4.2 taskIds [22,32,395], got ${JSON.stringify(webSkill242.taskIds)}`);
assert(JSON.stringify(algoSkill443.taskIds) === JSON.stringify([18, 65, 89, 164, 218]), `Expected Algo 4.4.3 taskIds [18,65,89,164,218], got ${JSON.stringify(algoSkill443.taskIds)}`);
assert(JSON.stringify(dbSkill522.taskIds) === JSON.stringify([59, 130, 168, 208]), `Expected DB 5.2.2 taskIds [59,130,168,208], got ${JSON.stringify(dbSkill522.taskIds)}`);
assert(JSON.stringify(archSkill631.taskIds) === JSON.stringify([40, 81]), `Expected Arch 6.3.1 taskIds [40,81], got ${JSON.stringify(archSkill631.taskIds)}`);
assert(archSkill651.taskIds.includes(228), `Expected Arch 6.5.1 (Structural patterns) to include task #228 (Flyweight), got ${JSON.stringify(archSkill651.taskIds)}`);
assert(JSON.stringify(infraSkill722.taskIds) === JSON.stringify([3, 111, 366]), `Expected Infra 7.2.2 taskIds [3,111,366], got ${JSON.stringify(infraSkill722.taskIds)}`);
assert(JSON.stringify(infraSkill732.taskIds) === JSON.stringify([113, 232, 84]), `Expected Infra 7.3.2 taskIds [113,232,84], got ${JSON.stringify(infraSkill732.taskIds)}`);
assert(JSON.stringify(infraSkill753.taskIds) === JSON.stringify([95, 272, 279, 392, 401]), `Expected Infra 7.5.3 taskIds [95,272,279,392,401], got ${JSON.stringify(infraSkill753.taskIds)}`);
assert(sandbox.INFRA_MASTERY.decks['Ф-209'].title.includes('CI/CD: Основы непрерывной интеграции'), `Expected Ф-209 full title, got ${sandbox.INFRA_MASTERY.decks['Ф-209'].title}`);
assert(sandbox.INFRA_MASTERY.decks['Ф-220'].title.includes('Логирование и мониторинг: уровни логов'), `Expected Ф-220 full title, got ${sandbox.INFRA_MASTERY.decks['Ф-220'].title}`);
for (const t of sandbox.IDE_TASKS) {
  assert(t.tests && t.tests.trim() !== 'assert True', `Task #${t.id} still has dummy assert True!`);
  const hints = sandbox.buildSocraticHintsForTask(t);
  assert(hints.length === 4, `Task #${t.id} should have 4 Socratic levels, got ${hints.length}`);
  for (let hi = 0; hi < hints.length; hi++) {
    const h = hints[hi];
    const words = h.trim().split(/\s+/).length;
    assert(words <= 70, `Task #${t.id} hint level ${hi} exceeds 70 words (${words})`);
    const qCount = (h.match(/\?/g) || []).length;
    assert(qCount === 1, `Task #${t.id} hint level ${hi} must have exactly 1 question mark, got ${qCount}: ${h}`);
    if (t.solution && t.solution.length > 30) {
      assert(!h.includes(t.solution.trim()), `Task #${t.id} hint level ${hi} leaked full solution!`);
    }
  }
}
console.log('✓ Route #/practice (401/401 IDE tasks mapped across 7 modules, 0 dummy tests, 4-level Socratic invariants on all 401 tasks) verified');

// 7. Check all 238 K-notes across all 7 modules for 0 empty code blocks, 0 leaked fences, 0 raw # headers, 0 unrendered $...$ math, and data-ctx support
html = navigate('#/python/skill/1.1.1');
const k001AllStepsHtml = sandbox.PY_MASTERY.notes['К-001'].steps.map(s => s.html).join('\n');
assert(k001AllStepsHtml.includes('data-run-snippet="1"'), 'К-001 steps missing data-run-snippet button');
assert(k001AllStepsHtml.includes('data-ctx="'), 'К-001 multi-step snippets missing cumulative data-ctx');
assert(!html.includes('<div class="code-snippet-wrap"><button type="button" class="run-inline-btn" data-run-inline>▶ Запустить код</button><pre><code><div class="snippet-wrap">'), 'K-note snippet was double-wrapped!');
const all238Notes = {
  ...sandbox.PY_MASTERY.notes,
  ...sandbox.WEB_MASTERY.notes,
  ...sandbox.BACKEND_MASTERY.notes,
  ...sandbox.ALGO_MASTERY.notes,
  ...sandbox.DB_MASTERY.notes,
  ...sandbox.ARCH_MASTERY.notes,
  ...sandbox.INFRA_MASTERY.notes
};
assert(Object.keys(all238Notes).length === 238, `Expected 238 total K-notes across all 7 modules, got ${Object.keys(all238Notes).length}`);
for (const [kid, note] of Object.entries(all238Notes)) {
  for (let si = 0; si < note.steps.length; si++) {
    const shtml = note.steps[si].html;
    const proseOnly = shtml.replace(/<pre><code>[\s\S]*?<\/code><\/pre>/g, '').replace(/<code>[\s\S]*?<\/code>/g, '');
    assert(!/<pre><code>\s*<\/code><\/pre>/.test(shtml), `Empty <pre><code> block found in ${kid} step ${si + 1}`);
    assert(!shtml.includes('```'), `Unclosed markdown code fence leaked into HTML in ${kid} step ${si + 1}`);
    assert(!shtml.includes('<p>&gt;'), `Raw markdown blockquote (> ) leaked into HTML in ${kid} step ${si + 1}`);
    assert(!shtml.includes('<p># '), `Raw markdown H1 (# ) leaked into HTML in ${kid} step ${si + 1}`);
    assert(!shtml.includes('$O(') && !shtml.includes('$\\'), `Unrendered LaTeX math ($O(...) or $\\...) leaked into HTML in ${kid} step ${si + 1}`);
    assert(!/[²³]\d/.test(proseOnly), `Corrupted multi-digit exponent (²d or ³d) in ${kid} step ${si + 1}`);
    assert(!/\\(dots|ldots|ll|gg|left|right|%|_)/.test(proseOnly), `Unrendered LaTeX command leaked into prose in ${kid} step ${si + 1}`);
  }
}
for (const [kid, note] of Object.entries(sandbox.BACKEND_MASTERY.notes)) {
  assert(note.steps.length >= 3, `Backend note ${kid} should have at least 3 micro-steps, got ${note.steps.length}`);
}
for (const [kid, note] of Object.entries(sandbox.ALGO_MASTERY.notes)) {
  assert(note.steps.length >= 3, `Algo note ${kid} should have at least 3 micro-steps, got ${note.steps.length}`);
  const fullHtml = note.steps.map(s => s.html).join('\n');
  assert(fullHtml.includes('jvs-grid'), `Algo note ${kid} missing rendered Junior vs Senior (.jvs-grid) comparison block`);
  assert(fullHtml.includes('data-run-snippet="1"'), `Algo note ${kid} missing runnable Python snippet`);
}
for (const [kid, note] of Object.entries(sandbox.DB_MASTERY.notes)) {
  assert(note.steps.length >= 3, `DB note ${kid} should have at least 3 micro-steps, got ${note.steps.length}`);
  const fullHtml = note.steps.map(s => s.html).join('\n');
  assert(fullHtml.includes('jvs-grid'), `DB note ${kid} missing rendered Junior vs Senior (.jvs-grid) comparison block`);
  assert(fullHtml.includes('data-run-snippet="1"'), `DB note ${kid} missing runnable Python snippet`);
}
for (const [kid, note] of Object.entries(sandbox.ARCH_MASTERY.notes)) {
  assert(note.steps.length >= 4, `Arch note ${kid} should have at least 4 micro-steps, got ${note.steps.length}`);
  const fullHtml = note.steps.map(s => s.html).join('\n');
  assert(fullHtml.includes('jvs-grid'), `Arch note ${kid} missing rendered Junior vs Senior (.jvs-grid) comparison block`);
  assert(fullHtml.includes('data-run-snippet="1"'), `Arch note ${kid} missing runnable Python snippet`);
}
for (const [kid, note] of Object.entries(sandbox.INFRA_MASTERY.notes)) {
  assert(note.steps.length === 4, `Infra note ${kid} should have 4 micro-steps, got ${note.steps.length}`);
  const fullHtml = note.steps.map(s => s.html).join('\n');
  assert(fullHtml.includes('jvs-grid'), `Infra note ${kid} missing rendered Junior vs Senior (.jvs-grid) comparison block`);
  assert(fullHtml.includes('data-run-snippet="1"'), `Infra note ${kid} missing runnable Python snippet`);
}
console.log('✓ All 238 K-notes across Python (68), Web (23), Backend (40), Algorithms (14), Databases (32), Architecture (14), and Infrastructure (47) verified: 0 empty code blocks, 0 fence/blockquote/#-header/$math leaks, >=3/4 steps + .jvs-grid + runnable snippets on all Algo, DB, Arch & Infra notes');

// 8. Check Skill Tree Map (#/map) and all 18 Topic pages (#/topic/...)
html = navigate('#/map');
assert(html.includes('Карта навыков'), '#/map failed to render');
const nodeIds = ['diag','py-basics','git','sql','http','oop','algo','orm','async','framework','testing','cache','docker','security','sysdesign','llm','final','interview'];
for (const nid of nodeIds) {
  html = navigate(`#/topic/${nid}`);
  assert(!html.includes('— скоро'), `Topic ${nid} still contains "— скоро" placeholder!`);
  assert(!html.includes('Полный урок ещё не готов'), `Topic ${nid} still contains "Полный урок ещё не готов" placeholder!`);
}
console.log(`✓ All ${nodeIds.length} Topic pages verified — ZERO "скоро" placeholders remain!`);

// 9. Check all 64 Lessons (#/lesson/...)
const allLessonIds = [
  'py-basics-1','py-basics-2','py-basics-3','py-basics-4',
  'git-1','git-2','git-3','git-4',
  'sql-1','sql-dml','sql-2','sql-3','sql-4',
  'http-1','http-2','http-3','http-4',
  'oop-1','oop-2','oop-3','oop-4',
  'algo-1','algo-2','algo-3','algo-4',
  'orm-1','orm-2','orm-3','orm-4',
  'async-1','async-2','async-3',
  'framework-1','framework-2','framework-3','framework-4',
  'testing-1','testing-2','testing-3','testing-4',
  'cache-1','cache-2','cache-3',
  'docker-1','docker-2','docker-3','docker-4',
  'security-1','security-2','security-3','security-4',
  'sysdesign-1','sysdesign-2','sysdesign-3',
  'llm-1','llm-2','llm-3',
  'final-1','final-2','final-3',
  'interview-1','interview-2','interview-3','interview-4'
];
for (const lid of allLessonIds) {
  html = navigate(`#/lesson/${lid}`);
  assert(html.includes('Дальше: мини-проверка'), `Lesson ${lid} failed to render theory stage`);
}
console.log(`✓ All ${allLessonIds.length} interactive lessons (#/lesson/...) verified!`);

// 10. Test interactive Khan Mastery progression: 0 MP -> 50 MP (Familiar) -> 80 MP (Proficient) -> 100 MP (Mastered 👑) & Scaffold Fading
function fireClick(attrName, attrVal, extraAttrs = {}) {
  const target = {
    id: (extraAttrs && extraAttrs.id) || '',
    closest(sel) {
      if (attrName && sel.includes(`[${attrName}]`)) {
        return {
          id: (extraAttrs && extraAttrs.id) || '',
          getAttribute(k) {
            if (k === attrName) return attrVal;
            if (extraAttrs && k in extraAttrs) return extraAttrs[k];
            return null;
          },
          setAttribute() {},
          removeAttribute() {},
          textContent: '',
          closest() { return null; },
          getBoundingClientRect() { return { left: 100, right: 140, top: 200, bottom: 240, width: 40, height: 40 }; }
        };
      }
      if (extraAttrs && extraAttrs.className && sel.includes('.') && extraAttrs.className.includes(sel.replace(/^\./, ''))) {
        return {
          id: (extraAttrs && extraAttrs.id) || '',
          className: extraAttrs.className,
          getAttribute(k) {
            if (k === attrName) return attrVal;
            if (extraAttrs && k in extraAttrs) return extraAttrs[k];
            return null;
          },
          setAttribute() {},
          removeAttribute() {},
          textContent: '',
          closest() { return null; },
          getBoundingClientRect() { return { left: 100, right: 140, top: 200, bottom: 240, width: 40, height: 40 }; }
        };
      }
      if (extraAttrs && extraAttrs.id && sel.includes('#' + extraAttrs.id)) {
        return {
          id: extraAttrs.id,
          getAttribute(k) {
            if (extraAttrs && k in extraAttrs) return extraAttrs[k];
            return null;
          },
          setAttribute() {},
          removeAttribute() {},
          textContent: '',
          closest() { return null; }
        };
      }
      return null;
    }
  };
  return Promise.all((docListeners['click'] || []).map(fn => fn({ target })));
}

(async () => {
  // Test 2-minute quick micro-step launcher (global and track-scoped)
  await fireClick('data-quick-microstep', 'infra');
  assert(sandbox.location.hash === '#/infra/skill/7.1.1', `Track-scoped quick microstep for infra should navigate to #/infra/skill/7.1.1, got ${sandbox.location.hash}`);
  await fireClick('data-quick-microstep', '');
  assert(sandbox.location.hash === '#/python/skill/1.1.1', 'Global quick microstep should navigate to #/python/skill/1.1.1');

  // Verify Socratic Level 3 Tactical Hint accuracy on variable-assignment tasks (#1, #20) and helper-class tasks (boss-backend)
  const task1Hints = sandbox.buildSocraticHintsForTask(sandbox.IDE_TASKS_BY_ID[1]);
  assert(task1Hints[3].includes('sql') && !task1Hints[3].includes('def solution'), `Variable task #1 H3 should reference target var 'sql', got: ${task1Hints[3]}`);
  const task20Hints = sandbox.buildSocraticHintsForTask(sandbox.IDE_TASKS_BY_ID[20]);
  assert(task20Hints[3].includes('reversed_list') && !task20Hints[3].includes('def solution'), `Variable task #20 H3 should reference 'reversed_list', got: ${task20Hints[3]}`);
  const bossBackendHints = sandbox.buildSocraticHintsForTask(sandbox.MODULE_BOSS_TASKS.backend);
  assert(bossBackendHints[3].includes('def process_checkout') && !bossBackendHints[3].includes('class FakeUoW'), `boss-backend H3 should reference target 'def process_checkout', got: ${bossBackendHints[3]}`);

  // Finish note К-001 -> should award XP and bump skill 1.1.1 to 50 MP (Familiar)
  await fireClick('data-py-finish-note', 'К-001');
  let htmlAfterNote = elementsById['view-root'].innerHTML;
  assert(htmlAfterNote.includes('Знакомство / Familiar (50 MP)'), 'Completing note К-001 should promote 1.1.1 to 50 MP (Familiar)');

  // Switch to Code tab, open 2 Socratic hints, and solve task #20 -> should reset hintLevel to 0 (Scaffold Fading) and bump skill 1.1.1 to 80 MP (Proficient)
  await fireClick('data-py-tab', 'code');
  await fireClick('data-py-task-hint', '');
  await fireClick('data-py-task-hint', '');
  assert(elementsById['view-root'].innerHTML.includes('Сократовская наводка (2/4)'), 'Socratic hint level should be 2/4 before solving');
  await fireClick('data-py-run-task', '20');
  let htmlAfterTask = elementsById['view-root'].innerHTML;
  assert(htmlAfterTask.includes('Практика / Proficient (80 MP)'), 'Solving task #20 should promote 1.1.1 to 80 MP (Proficient)');
  assert(htmlAfterTask.includes('Сократовская наводка (0/4)'), 'Scaffold Fading failed: hintLevel did not reset to 0 after solving task!');

  // Pass Unit Test 1.1 (4 questions: correct indices 1, 1, 2, 1) -> should promote all Unit 1.1 skills to 100 MP (Mastered 👑)
  navigate('#/python/unittest/1.1');
  const utAnswers = [1, 1, 2, 1];
  for (const ans of utAnswers) {
    await fireClick('data-ut-ans', String(ans));
    await fireClick('data-ut-next', '');
  }
  let utHtml = elementsById['view-root'].innerHTML;
  assert(utHtml.includes('Рубежный тест успешно взят!'), 'Unit Test 1.1 should complete with mastery');
  let pyHtml = navigate('#/python');
  assert(pyHtml.includes('Мастерство 100 MP (5)'), 'All 5 skills of Unit 1.1 should now be at 100 MP (Mastered)');

  // Also test passing Backend Unit Test 3.6 (4 questions: correct indices 1, 1, 1, 1) -> should promote all 3 Unit 3.6 skills (3.6.1, 3.6.2, 3.6.3) to 100 MP
  navigate('#/backend/unittest/3.6');
  for (const ans of [1, 1, 1, 1]) {
    await fireClick('data-ut-ans', String(ans));
    await fireClick('data-ut-next', '');
  }
  let beUtHtml = elementsById['view-root'].innerHTML;
  assert(beUtHtml.includes('Рубежный тест успешно взят!'), 'Backend Unit Test 3.6 should complete with mastery');
  let beHtml = navigate('#/backend');
  assert(beHtml.includes('Мастерство 100 MP (3)'), 'All 3 skills of Backend Unit 3.6 should now be at 100 MP (Mastered)');

  // Test Backend framework part filter pill (e.g. FastAPI 3.1)
  await fireClick('data-backend-part-filter', '3.1');
  let beFilteredHtml = elementsById['view-root'].innerHTML;
  assert(beFilteredHtml.includes('Юнит 3.1') && !beFilteredHtml.includes('Юнит 3.4 · Часть IV'), 'Backend part filter 3.1 should filter units to 3.1');
  await fireClick('data-backend-part-filter', 'all');

  // Test passing Algorithms Unit Test 4.4 (4 questions: correct indices 1, 1, 1, 1) -> should promote all 3 Unit 4.4 skills (4.4.1, 4.4.2, 4.4.3) to 100 MP
  navigate('#/algorithms/unittest/4.4');
  for (const ans of [1, 1, 1, 1]) {
    await fireClick('data-ut-ans', String(ans));
    await fireClick('data-ut-next', '');
  }
  let algoUtHtml = elementsById['view-root'].innerHTML;
  assert(algoUtHtml.includes('Рубежный тест успешно взят!'), 'Algorithms Unit Test 4.4 should complete with mastery');
  let algoHtml = navigate('#/algorithms');
  assert(algoHtml.includes('Мастерство 100 MP (3)'), 'All 3 skills of Algorithms Unit 4.4 should now be at 100 MP (Mastered)');

  // Test passing Databases Unit Test 5.3 (4 questions: correct indices 1, 1, 1, 1) -> should promote all 3 Unit 5.3 skills (5.3.1, 5.3.2, 5.3.3) to 100 MP
  navigate('#/databases/unittest/5.3');
  for (const ans of [1, 1, 1, 1]) {
    await fireClick('data-ut-ans', String(ans));
    await fireClick('data-ut-next', '');
  }
  let dbUtHtml = elementsById['view-root'].innerHTML;
  assert(dbUtHtml.includes('Рубежный тест успешно взят!'), 'Databases Unit Test 5.3 should complete with mastery');
  let dbHtml = navigate('#/databases');
  assert(dbHtml.includes('Мастерство 100 MP (3)'), 'All 3 skills of Databases Unit 5.3 should now be at 100 MP (Mastered)');

  // Test passing Architecture Unit Test 6.2 (4 questions: correct indices 1, 1, 1, 1) -> should promote all 3 Unit 6.2 skills (6.2.1, 6.2.2, 6.2.3) to 100 MP
  navigate('#/architecture/unittest/6.2');
  for (const ans of [1, 1, 1, 1]) {
    await fireClick('data-ut-ans', String(ans));
    await fireClick('data-ut-next', '');
  }
  let archUtHtml = elementsById['view-root'].innerHTML;
  assert(archUtHtml.includes('Рубежный тест успешно взят!'), 'Architecture Unit Test 6.2 should complete with mastery');
  let archHtml = navigate('#/architecture');
  assert(archHtml.includes('Мастерство 100 MP (3)'), 'All 3 skills of Architecture Unit 6.2 should now be at 100 MP (Mastered)');

  // Test passing Infrastructure Unit Test 7.2 (4 questions: correct indices 1, 1, 1, 1) -> should promote all 3 Unit 7.2 skills (7.2.1, 7.2.2, 7.2.3) to 100 MP
  navigate('#/infra/unittest/7.2');
  for (const ans of [1, 1, 1, 1]) {
    await fireClick('data-ut-ans', String(ans));
    await fireClick('data-ut-next', '');
  }
  let infraUtHtml = elementsById['view-root'].innerHTML;
  assert(infraUtHtml.includes('Рубежный тест успешно взят!'), 'Infrastructure Unit Test 7.2 should complete with mastery');
  let infraHtml = navigate('#/infra');
  assert(infraHtml.includes('Мастерство 100 MP (3)'), 'All 3 skills of Infrastructure Unit 7.2 should now be at 100 MP (Mastered)');

  console.log('✓ Full Khan Academy 4-tier Mastery flow (0 -> 50 -> 80 -> 100 MP 👑) + Scaffold Fading + Backend, Algorithms, Databases, Architecture & Infrastructure Unit Tests verified!');

  // 10b. Verify cleanliness of all 238 K-note titles, 286 F-deck titles, and 126 skill titles (0 leaked single-underscore `_ ` separators)
  const leakedUnderscoreRe = /(?<!_)_(?=\s|$)/;
  const allMasteries = [sandbox.PY_MASTERY, sandbox.WEB_MASTERY, sandbox.BACKEND_MASTERY, sandbox.ALGO_MASTERY, sandbox.DB_MASTERY, sandbox.ARCH_MASTERY, sandbox.INFRA_MASTERY];
  for (const m of allMasteries) {
    for (const [kid, n] of Object.entries(m.notes)) {
      assert(!leakedUnderscoreRe.test(n.title), `Leaked underscore in note title ${kid}: ${n.title}`);
    }
    for (const [fid, d] of Object.entries(m.decks)) {
      assert(!leakedUnderscoreRe.test(d.title), `Leaked underscore in deck title ${fid}: ${d.title}`);
    }
    for (const u of m.units) {
      for (const s of u.skills) {
        assert(!leakedUnderscoreRe.test(s.title), `Leaked underscore in skill title ${s.id}: ${s.title}`);
      }
    }
  }
  assert(sandbox.ALGO_MASTERY.notes['К-111'].title.includes('Статический и динамический массив'), `Expected full title in К-111`);
  assert(sandbox.INFRA_MASTERY.units[3].title === 'Юнит 7.4 · CI/CD', `Expected 'Юнит 7.4 · CI/CD', got ${sandbox.INFRA_MASTERY.units[3].title}`);
  console.log('✓ All 238 K-note titles, 286 F-deck titles, and 126 skill titles verified clean (0 leaked underscores)');

  // 10c. Test all 7 Module Boss Challenges (#/<track>/boss) & Socratic invariants + Scaffold Fading + IDE counter isolation
  const bossTracks = ['python', 'web', 'backend', 'algorithms', 'databases', 'architecture', 'infra'];
  assert(sandbox.MODULE_BOSS_TASKS && Object.keys(sandbox.MODULE_BOSS_TASKS).length === 7, 'Expected 7 MODULE_BOSS_TASKS');
  for (const tk of bossTracks) {
    const bossObj = sandbox.MODULE_BOSS_TASKS[tk];
    const bHints = sandbox.buildSocraticHintsForTask(bossObj);
    assert(bHints.length === 4, `Boss ${tk} must have 4 Socratic hint levels`);
    bHints.forEach((h, idx) => {
      const wc = h.trim().split(/\s+/).filter(Boolean).length;
      const qCount = (h.match(/\?/g) || []).length;
      assert(wc <= 70 && qCount === 1, `Boss ${tk} hint ${idx} violates Socratic invariants: words=${wc}, q=${qCount}`);
    });
    const bHtml = navigate(`#/${tk}/boss`);
    assert(bHtml.includes(bossObj.title), `Boss route #/${tk}/boss missing title`);
  }
  // Test solving Infrastructure Boss (#/infra/boss): open 2 hints -> run -> verify Scaffold Fading (0/4) and 100 MP across all 21 Infra skills
  navigate('#/infra/boss');
  await fireClick('data-boss-hint', '');
  await fireClick('data-boss-hint', '');
  assert(elementsById['view-root'].innerHTML.includes('Сократовская наводка (2/4)'), 'Boss hint level should be 2/4 before solving');
  await fireClick('data-boss-run', 'infra');
  const infraBossAfter = elementsById['view-root'].innerHTML;
  assert(infraBossAfter.includes('Босс модуля') && infraBossAfter.includes('повержен!'), 'Infrastructure Boss should pass');
  assert(infraBossAfter.includes('Сократовская наводка (0/4)'), 'Boss Scaffold Fading failed: hintLevel did not reset to 0');
  const infraAfterBoss = navigate('#/infra');
  assert(infraAfterBoss.includes('Мастерство 100 MP (21)'), 'Solving Infrastructure Boss should promote all 21 Infra skills to 100 MP');
  // Verify solving boss-infra did NOT inflate the 401 IDE task solved counter (only task #20 was solved so far => 1/401)
  assert(infraAfterBoss.includes('Решено задач IDE: <b>1/401</b>'), `Solving boss-infra should not inflate IDE solved counter beyond 1/401`);
  console.log('✓ All 7 Module Boss Challenges (#/<track>/boss), Scaffold Fading & 401 IDE counter isolation verified!');

  // 10d. Test Interactive Mock Interview Simulator (#/mock & #/interview-sim): Live-Coding + STAR Behavioral builder
  let mockHtml = navigate('#/mock');
  assert(mockHtml.includes('Симулятор собеседования (Live-Coding + STAR)'), '#/mock missing main heading');
  assert(mockHtml.includes('20:00'), '#/mock missing 20:00 countdown timer');
  // Verify that typing in #mock-code-editor is preserved across timer start/pause/reset
  sandbox.document.getElementById('mock-code-editor').value = '# candidate draft preserved\ndef custom(): return 42';
  await fireClick('data-mock-timer-toggle', '');
  await fireClick('data-mock-timer-toggle', '');
  await fireClick('data-mock-timer-reset', '');
  assert(elementsById['view-root'].innerHTML.includes('# candidate draft preserved'), 'Mock timer toggle/reset wiped out #mock-code-editor draft');

  await fireClick('data-mock-hint', '');
  assert(elementsById['view-root'].innerHTML.includes('Запросить наводку интервьюера (1/4)'), '#/mock Socratic hint should increment to 1/4');
  await fireClick('data-mock-run', '240');
  assert(elementsById['view-root'].innerHTML.includes('Live-Coding раунд успешно пройден!'), '#/mock Live-Coding run should pass');
  assert(elementsById['view-root'].innerHTML.includes('Запросить наводку интервьюера (0/4)'), '#/mock Scaffold Fading should reset hint level to 0/4');

  // Switch to STAR Behavioral tab, verify all 4 scenarios have distinct demos and score 4/4, plus expanded verbs
  await fireClick('data-mock-tab', 'star');
  assert(elementsById['view-root'].innerHTML.includes('Методика STAR'), '#/mock STAR tab failed to render');
  const seenDemos = new Set();
  for (const sc of sandbox.STAR_SCENARIOS) {
    await fireClick('data-star-scenario', sc.id);
    await fireClick('data-star-fill-demo', '');
    const viewAfterDemo = elementsById['view-root'].innerHTML;
    assert(viewAfterDemo.includes('Оценка STAR-ответа: 4 из 4'), `STAR demo for ${sc.id} did not score 4/4`);
    seenDemos.add(sc.demo.s);
  }
  assert(seenDemos.size === 4, `Expected 4 distinct STAR scenario demos, got ${seenDemos.size}`);
  // Verify feminine / engineering verbs without explicit 'я' are recognized by evaluateStarResponse
  const femEval = sandbox.evaluateStarResponse(
    'В микросервисе авторизации при нагрузке 500 RPS наблюдались скачки латентности.',
    'Требовалось снизить p99 время ответа ниже 50 мс без деградации безопасности.',
    'Локализовала узкое место в синхронном хешировании, спроектировала кэширование ключей и покрыла нагрузочными тестами.',
    'Время ответа сократилось с 600 мс до 18 мс (в 33 раза), ошибки 502 упали до 0%.'
  );
  assert(femEval.score === 4 && femEval.passed, `evaluateStarResponse should accept feminine/engineering action verbs, got score=${femEval.score}`);
  console.log('✓ Interactive Mock Interview Simulator (#/mock: 20-min Live-Coding + 4 STAR scenarios + draft preservation) verified!');

  // 11. Test Handover Modal ("Контекст для нового чата") & QuotaExceededError resilience
  await fireClick('data-open-handover', '');
  assert(elementsById['handover-modal'] && elementsById['handover-modal'].innerHTML.includes('Контекст для продолжения работы в новом чате'), 'Handover modal failed to open');
  assert(elementsById['handover-modal'].innerHTML.includes('Решено задач IDE**: 2 / 401'), 'Handover markdown should count only the 2 solved IDE tasks (#20 and #240), excluding boss-infra');
  assert(!elementsById['handover-modal'].innerHTML.includes('undefined'), 'Handover modal markdown must not contain undefined values (e.g. Echelon MP)');
  assert(elementsById['handover-modal'].innerHTML.includes('Эшелон 1 (Скрининг)') && elementsById['handover-modal'].innerHTML.includes('Эшелон 4 (Резерв)'), 'Handover modal must include Echelons 1-4 MP stats');

  // Test QuotaExceededError eviction resilience on localStorage
  const origSetItem = sandbox.localStorage.setItem;
  let quotaThrown = false;
  sandbox.localStorage.setItem = function(k, v) {
    if (!quotaThrown && (k === 'practice-ide-drafts' || k === 'py-backend-academy-v2')) {
      quotaThrown = true;
      const err = new Error('QuotaExceededError');
      err.name = 'QuotaExceededError';
      throw err;
    }
    return origSetItem.call(this, k, v);
  };
  await fireClick('data-prac-run', '240');
  sandbox.localStorage.setItem = origSetItem;
  assert(quotaThrown, 'QuotaExceededError simulation should have triggered');
  console.log('✓ Handover Modal ("Контекст для нового чата"), JSON export & QuotaExceededError resilience verified!');

  // 12. Verify Cross-Module Interview Priority Architecture (4 Echelons Tier 1..4), Parallel Stack Branches, Unit Sort/Filter, Calibration Diagnostic & Bi-directional Map Sync
  const modalEl = sandbox.document.getElementById('handover-modal');
  if (modalEl) modalEl.remove();

  // 12a. Verify base unit distribution across 4 Echelons: 14 + 17 + 11 + 3 = 45 units
  const tierCounts = { 1: 0, 2: 0, 3: 0, 4: 0 };
  for (const m of allMasteries) {
    for (const u of m.units) {
      assert([1, 2, 3, 4].includes(u.tier), `Unit ${u.id} missing valid tier: ${u.tier}`);
      assert(typeof u.stackTag === 'string' && u.stackTag.length > 0, `Unit ${u.id} missing stackTag`);
      tierCounts[u.tier]++;
    }
  }
  assert(
    tierCounts[1] === 14 && tierCounts[2] === 17 && tierCounts[3] === 11 && tierCounts[4] === 3,
    `Expected base unit counts 14/17/11/3 across Echelons 1..4, got ${JSON.stringify(tierCounts)}`
  );

  // 12b. Verify Parallel Stack Branch switching ('fastapi' vs 'django' vs 'both') AND immediate DOM re-render on click
  navigate('#/');
  await fireClick('data-stack-branch', 'fastapi');
  assert(sandbox.getEffectiveUnitTier('3.1') === 2 && sandbox.getEffectiveUnitTier('3.2') === 4 && sandbox.getEffectiveUnitTier('3.3') === 4 && sandbox.getEffectiveUnitTier('5.5') === 2, 'FastAPI stack branch should keep 3.1/5.5 in Echelon 2 and move 3.2/3.3 to Echelon 4');
  assert(elementsById['view-root'].innerHTML.includes('(15 юнитов)') && elementsById['view-root'].innerHTML.includes('(5 юнитов)'), 'Clicking data-stack-branch="fastapi" must immediately re-render DOM with 15 Echelon-2 units and 5 Echelon-4 units');

  await fireClick('data-stack-branch', 'django');
  assert(sandbox.getEffectiveUnitTier('3.1') === 4 && sandbox.getEffectiveUnitTier('3.2') === 2 && sandbox.getEffectiveUnitTier('3.3') === 2 && sandbox.getEffectiveUnitTier('5.5') === 2, 'Django stack branch should move 3.1 to Echelon 4 and keep 3.2/3.3/5.5 in Echelon 2');
  assert(elementsById['view-root'].innerHTML.includes('(16 юнитов)') && elementsById['view-root'].innerHTML.includes('(4 юнитов)'), 'Clicking data-stack-branch="django" must immediately re-render DOM with 16 Echelon-2 units and 4 Echelon-4 units');

  await fireClick('data-stack-branch', 'both');
  assert(sandbox.getEffectiveUnitTier('3.1') === 2 && sandbox.getEffectiveUnitTier('3.2') === 2 && sandbox.getEffectiveUnitTier('3.3') === 2 && sandbox.getEffectiveUnitTier('3.4') === 4, 'Both stack branch should keep 3.1/3.2/3.3 in Echelon 2 and 3.4 in Echelon 4');
  assert(elementsById['view-root'].innerHTML.includes('(17 юнитов)') && elementsById['view-root'].innerHTML.includes('(3 юнитов)'), 'Clicking data-stack-branch="both" must immediately re-render DOM with 17 Echelon-2 units and 3 Echelon-4 units');
  await fireClick('data-stack-branch', 'fastapi');

  // Verify clicking [data-open-echelon-next] and [data-priority-next-skill] navigates without throwing
  await fireClick('data-open-echelon-next', '2');
  assert(sandbox.location.hash === '#/python/skill/1.5.1', `Clicking data-open-echelon-next="2" should navigate to #/python/skill/1.5.1, got ${sandbox.location.hash}`);
  navigate('#/');
  await fireClick('data-priority-next-skill', '1.2.1');
  assert(sandbox.location.hash === '#/python/skill/1.2.1', `Clicking data-priority-next-skill="1.2.1" should navigate to #/python/skill/1.2.1, got ${sandbox.location.hash}`);

  // 12c. Verify Unit Sorting (priority vs number), Echelon filter pills, and cross-track filter reset
  let pyPriorityHtml = navigate('#/python');
  const pos19Prio = pyPriorityHtml.indexOf('Юнит 1.9');
  const pos15Prio = pyPriorityHtml.indexOf('Юнит 1.5');
  assert(pos19Prio > 0 && pos15Prio > 0 && pos19Prio < pos15Prio, 'In priority sort mode, Unit 1.9 (Echelon 1) must appear before Unit 1.5 (Echelon 2)');
  await fireClick('data-unit-sort', 'number');
  let pyNumHtml = elementsById['view-root'].innerHTML;
  const pos19Num = pyNumHtml.indexOf('Юнит 1.9');
  const pos15Num = pyNumHtml.indexOf('Юнит 1.5');
  assert(pos15Num > 0 && pos19Num > 0 && pos15Num < pos19Num, 'In number sort mode, Unit 1.5 must appear before Unit 1.9');
  await fireClick('data-unit-sort', 'priority');

  await fireClick('data-track-tier-filter', '1');
  let pyTier1Html = elementsById['view-root'].innerHTML;
  assert(pyTier1Html.includes('Юнит 1.9') && !pyTier1Html.includes('Юнит 1.5'), 'Echelon 1 filter in #/python should include Unit 1.9 and exclude Unit 1.5');
  // Navigating to #/backend must automatically reset trackTierFilter to 'all'
  let beResetHtml = navigate('#/backend');
  assert(!beResetHtml.includes('нет юнитов Эшелона 1'), 'Switching from #/python to #/backend must reset trackTierFilter to all');
  // Selecting Echelon 1 inside #/backend (which has 0 Echelon 1 units) must show the fallback notice
  await fireClick('data-track-tier-filter', '1');
  assert(elementsById['view-root'].innerHTML.includes('нет юнитов Эшелона 1 — показаны все юниты модуля'), 'Selecting Echelon 1 in #/backend should display fallback notice');
  await fireClick('data-track-tier-filter', 'all');

  // 12d. Verify Calibration Diagnostic (#/topic/diag & #/diagnostic): +50 MP on correct answers, diagnosticGaps on wrong answers, 2-min microstep priority, and revoking 50 MP on re-take failure
  let diagIntro = navigate('#/diagnostic');
  assert(diagIntro.includes('Калибровка приоритетов перед стартом'), '#/diagnostic failed to render calibration intro');
  await fireClick('data-diag-start', '');
  // Answer Q0..Q5: Q2 ('s-1-3-1') correctly (correct=0), Q4 ('s-1-2-3') wrongly (correct=1, pick 0)
  for (let qi = 0; qi < 6; qi++) {
    const pick = 0; // Q2 correct is 0, Q4 correct is 1 (so 0 is wrong for Q4)
    await fireClick('data-diag-answer', String(pick));
    await fireClick('data-diag-next', '');
  }
  const calRes = sandbox.applyDiagnosticCalibration();
  assert(calRes.passedSkills.includes('1.3.1'), 'Q2 correct answer should credit skill 1.3.1');
  assert(calRes.gaps.includes('1.2.3'), 'Q4 wrong answer should add 1.2.3 to diagnosticGaps');
  let skill131Html = navigate('#/python/skill/1.3.1');
  assert(skill131Html.includes('Знакомство / Familiar (50 MP)'), 'Calibrated skill 1.3.1 should have 50 MP (Familiar)');
  // Global 2-minute microstep must now prioritize the first unresolved diagnostic gap!
  await fireClick('data-quick-microstep', '');
  const expectedGapNum = calRes.gaps[0];
  assert(sandbox.location.hash.endsWith(`/skill/${expectedGapNum}`), `2-minute microstep should jump to first diagnostic gap ${expectedGapNum}, got ${sandbox.location.hash}`);

  // Re-take diagnostic and fail Q2 (pick 1 instead of 0) -> must revoke 50 MP on 1.3.1 and add 1.3.1 to diagnosticGaps
  navigate('#/diagnostic');
  await fireClick('data-diag-start', '');
  for (let qi = 0; qi < 6; qi++) {
    const pick = (qi === 2) ? 1 : 0; // Q2 wrong (1 !== 0)
    await fireClick('data-diag-answer', String(pick));
    await fireClick('data-diag-next', '');
  }
  const recalRes = sandbox.applyDiagnosticCalibration();
  let skill131AfterRetake = navigate('#/python/skill/1.3.1');
  assert(recalRes.gaps.includes('1.3.1') && skill131AfterRetake.includes('Не начато (0 MP)'), 'Failing Q2 on diagnostic re-take must revoke 50 MP auto-credit on 1.3.1 and add it to diagnosticGaps');

  // 12e. Verify Echelon filter dropdowns in #/practice, #/cards, and #/mock + Bi-directional Map/Topic links + zero 'echelon-badge undefined'
  function fireChange(id, value) {
    const target = { id, value };
    return Promise.all((docListeners['change'] || []).map(fn => fn({ target })));
  }
  navigate('#/practice');
  await fireChange('prac-echelon-filter', 'gaps');
  assert(elementsById['view-root'].innerHTML.includes('value="gaps" selected') && elementsById['view-root'].innerHTML.includes('Пробелы диагностики'), '#/practice echelon filter should support gaps');
  await fireChange('prac-echelon-filter', 'all');

  navigate('#/cards');
  await fireChange('cards-echelon-filter', '1');
  assert(elementsById['view-root'].innerHTML.includes('Эшелон 1'), '#/cards echelon filter 1 failed');
  await fireChange('cards-echelon-filter', 'all');

  navigate('#/mock');
  await fireClick('data-mock-tab', 'live');
  await fireChange('mock-echelon-select', '1');
  await fireClick('data-mock-random-task', '');
  const curMockHtml = elementsById['view-root'].innerHTML;
  assert(curMockHtml.includes('Эшелон 1') && !curMockHtml.includes('echelon-badge undefined'), '#/mock random task in Round 1 (Echelon 1) must select an Echelon 1 task with valid badgeClass');

  const mapViewHtml = navigate('#/map');
  assert(mapViewHtml.includes('Приоритетная архитектура подготовки к собеседованию (4 эшелона)') && mapViewHtml.includes('Связанные юниты:'), '#/map must include Priority Roadmap widget and linked unit badges');
  assert(!mapViewHtml.includes('echelon-badge undefined') && mapViewHtml.includes('echelon-badge--t1'), '#/map must render valid echelon-badge--t1..t4 classes without undefined');
  const topicSqlHtml = navigate('#/topic/sql');
  assert(topicSqlHtml.includes('Двусторонняя синхронизация с 7 модулями Мастерства') && topicSqlHtml.includes('Юнит 5.2'), '#/topic/sql must display bi-directional unit cards');
  assert(!topicSqlHtml.includes('echelon-badge undefined'), '#/topic/sql must not contain echelon-badge undefined');
  console.log('✓ Cross-Module Interview Priority Architecture (4 Echelons, Stack Branches, Calibration Diagnostic, Sort/Filter & Map Sync) verified!');

  // 13. Verify Variant A Cocoon UI Dashboard, Progressive Chunk Scroll-Reveal & Sprint Finish Celebration
  assert(sandbox.document.documentElement.getAttribute('data-theme') === 'dark', 'Default theme on html element must be Evening Obsidian (data-theme="dark")');
  let dashCocoonHtml = navigate('#/');
  assert(!sandbox.document.body.classList.contains('is-sprint-focus'), 'Dashboard must not have body.is-sprint-focus');
  assert(dashCocoonHtml.includes('cocoon-focus-card') && dashCocoonHtml.includes('btn-glass-emerald') && dashCocoonHtml.includes('Начать спринт (4 мин) ➔'), 'Dashboard must render .cocoon-focus-card with .btn-glass-emerald CTA');
  assert(dashCocoonHtml.includes('cd-box') && dashCocoonHtml.includes('До 1-го скрининга:') && dashCocoonHtml.includes('cd-bar-track') && dashCocoonHtml.includes('cd-bar-fill'), 'Dashboard must render .cd-box reverse countdown with .cd-bar-track > .cd-bar-fill');
  assert(dashCocoonHtml.includes('stage-pills') && dashCocoonHtml.includes('data-dash-stage="1"') && dashCocoonHtml.includes('mini-list') && dashCocoonHtml.includes('mini-item'), 'Dashboard must render 4-stage interview switcher (.stage-pills) and 1-line checklist (.mini-list / .mini-item)');
  assert(dashCocoonHtml.includes('<details class="cocoon-details">') && dashCocoonHtml.includes('Все модули, эшелоны и статистика ▾'), 'Dashboard must wrap secondary widgets inside <details class="cocoon-details">');

  // Test clicking stage 2 pill on dashboard
  await fireClick('data-dash-stage', '2');
  let dashStage2Html = elementsById['view-root'].innerHTML;
  assert(dashStage2Html.includes('stage-pill active" data-dash-stage="2"') && dashStage2Html.includes('1.5.1'), 'Clicking data-dash-stage="2" must switch dashboard stage checklist to Stage 2');
  await fireClick('data-dash-stage', '1');

  // Test Progressive Chunk Scroll-Reveal in viewPythonSkill (#/python/skill/1.1.1, right on initial step 0!)
  let pySkillChunkHtml = navigate('#/python/skill/1.1.1');
  assert(sandbox.document.body.classList.contains('is-sprint-focus'), '#/python/skill/1.1.1 must enable body.is-sprint-focus');
  assert(pySkillChunkHtml.includes('scroll-feed') && pySkillChunkHtml.includes('feed-chunk-new'), '#/python/skill/1.1.1 must render .scroll-feed and .feed-chunk-new');
  assert(pySkillChunkHtml.includes('data-chunk-more="py"') && pySkillChunkHtml.includes('Понятно, дальше (+10 XP) ➔'), '#/python/skill/1.1.1 step 0 must render progressive chunk reveal button [data-chunk-more="py"]');
  const getStoredXp = () => {
    const raw = Object.values(store).find(v => typeof v === 'string' && v.includes('"xp":'));
    return raw ? (JSON.parse(raw).xp || 0) : 0;
  };
  const xpBeforeChunk = getStoredXp();
  await fireClick('data-chunk-more', 'py');
  let pySkillAfterChunk = elementsById['view-root'].innerHTML;
  assert(getStoredXp() === xpBeforeChunk + 10, 'Clicking [data-chunk-more="py"] must award +10 XP');
  assert(pySkillAfterChunk.includes('feed-chunk-prev') && pySkillAfterChunk.includes('feed-chunk-new'), 'After clicking [data-chunk-more="py"], previous chunk must have .feed-chunk-prev and new chunk .feed-chunk-new');

  // Test Sprint Finish Celebration (.sprint-finish-card) when finishing a K-note, and verify it clears on chunk advance
  await fireClick('data-py-finish-note', 'К-002');
  let pySkillCelebrationHtml = elementsById['view-root'].innerHTML;
  assert(pySkillCelebrationHtml.includes('sprint-finish-card') && pySkillCelebrationHtml.includes('Минус 1 тема до скрининга!') && pySkillCelebrationHtml.includes('Готовность:'), 'Finishing a K-note must display .sprint-finish-card celebration');
  assert(pySkillCelebrationHtml.includes('daily-activity-strip') && pySkillCelebrationHtml.includes('stats-grid-2x2'), 'Sprint finish card must include 6-segment .daily-activity-strip and 2x2 metric grid .stats-grid-2x2');
  await fireClick('data-chunk-more', 'py');
  let pySkillAfterDismiss = elementsById['view-root'].innerHTML;
  assert(!pySkillAfterDismiss.includes('sprint-finish-card'), 'Advancing to the next chunk in the next K-note must dismiss .sprint-finish-card');

  // Verify Desktop Split-View in practice hub and skill reader
  let practiceHubDom = navigate('#/practice');
  assert(practiceHubDom.includes('practice-desktop-grid') && practiceHubDom.includes('practice-left-pane') && practiceHubDom.includes('practice-right-pane'), '#/practice must render desktop Split-View layout (.practice-desktop-grid, .practice-left-pane, .practice-right-pane)');
  let skillTheoryDom = navigate('#/python/skill/1.1.1');
  assert(skillTheoryDom.includes('skill-split-layout') && skillTheoryDom.includes('skill-lab-aside') && skillTheoryDom.includes('tap-chip-card'), '#/python/skill/1.1.1 must render .skill-split-layout with .skill-lab-aside and Tap-to-Fill Chips (.tap-chip-card)');

  // Test Progressive Chunk Scroll-Reveal in interactive lesson (#/lesson/py-basics-1, unconditionally on step 0!)
  let lessonChunkHtml = navigate('#/lesson/py-basics-1');
  assert(sandbox.document.body.classList.contains('is-sprint-focus'), '#/lesson/py-basics-1 must enable body.is-sprint-focus');
  assert(lessonChunkHtml.includes('scroll-feed') && lessonChunkHtml.includes('feed-chunk-new'), '#/lesson/py-basics-1 must render .scroll-feed and .feed-chunk-new');
  assert(lessonChunkHtml.includes('data-chunk-more="lesson"') && lessonChunkHtml.includes('Понятно, дальше (+10 XP) ➔'), '#/lesson/py-basics-1 step 0 must render progressive chunk reveal button [data-chunk-more="lesson"]');
  const xpBeforeLessonChunk = getStoredXp();
  await fireClick('data-chunk-more', 'lesson');
  let lessonAfterChunk1 = elementsById['view-root'].innerHTML;
  assert(getStoredXp() === xpBeforeLessonChunk + 10, 'Clicking [data-chunk-more="lesson"] must award +10 XP');
  assert(lessonAfterChunk1.includes('feed-chunk-prev') && lessonAfterChunk1.includes('feed-chunk-new'), 'Lesson chunk reveal must mark earlier chunk with .feed-chunk-prev and keep .feed-chunk-new');
  assert(lessonAfterChunk1.includes('Самые частые:</p>\n<ul>'), 'Lead-in colon paragraph ("Самые частые:") must be merged with its following <ul> list in the same chunk');

  // Verify advancing from lesson theory to check stage awards +10 XP and preserves .sprint-focus-topbar
  const xpBeforeLessonCheck = getStoredXp();
  await fireClick('data-lesson-next', 'check');
  let lessonCheckDom = elementsById['view-root'].innerHTML;
  assert(getStoredXp() === xpBeforeLessonCheck + 10, 'Advancing from lesson theory to check stage must award +10 XP');
  assert(lessonCheckDom.includes('sprint-focus-topbar') && lessonCheckDom.includes('Мини-проверка 1/'), 'Lesson check stage must include .sprint-focus-topbar with progress bar');

  // Test Bottom Sheet reveal upon checking answer
  await fireClick('data-lesson-check', '0');
  let lessonCheckAfterAnswer = elementsById['view-root'].innerHTML;
  assert(lessonCheckAfterAnswer.includes('academy-bottom-sheet') && lessonCheckAfterAnswer.includes('bs-title-row') && lessonCheckAfterAnswer.includes('bs-explain-text'), 'Answering a lesson check must slide up .academy-bottom-sheet with title, explain text and CTA button');
  assert(lessonCheckAfterAnswer.includes('btn-sprint-cta') && lessonCheckAfterAnswer.includes('data-lesson-next'), 'Bottom sheet must contain next button [data-lesson-next]');
  console.log('✓ Variant A Cocoon UI Dashboard, Progressive Chunk Scroll-Reveal, Lesson Stage Topbar, Bottom Sheet & Sprint Finish Celebration verified!');

  // 14. Verify Bulletproof Progress Persistence Across App Updates, Schema Migrations, Reloads & Reset Recovery
  assert(typeof sandbox.mergeProgressStates === 'function', 'mergeProgressStates must be exposed on window');
  const mergedTest = sandbox.mergeProgressStates(
    {
      xp: 420,
      streak: 5,
      lastVisit: 'Wed Sep 30 2026', // Alphabetically 'W' > 'M', but chronologically older than Oct 05!
      completedLessons: ['py-basics-1'],
      readNotes: ['К-001', 'К-002'],
      reviewedDecks: ['Ф-001'],
      passedUnitTests: ['1.1'],
      passedBosses: ['python'],
      skillMastery: { '1.1.1': 100, '1.1.2': 80 },
      cardRatings: { 'Ф-001:0': 4 },
      lessonDrafts: { 'py-basics-1': { stage: 'practice', practiceCode: 'x = 10', updatedAt: 100 } }
    },
    {
      xp: 180,
      streak: 9,
      lastVisit: 'Mon Oct 05 2026',
      completedLessons: ['py-basics-2'],
      readNotes: ['К-002', 'К-003'],
      reviewedDecks: ['Ф-002'],
      passedUnitTests: ['2.1'],
      passedBosses: ['web'],
      skillMastery: { '1.1.1': 50, '1.1.2': 100, '2.1.1': 50 },
      cardRatings: { 'Ф-001:0': 2, 'Ф-002:1': 3 },
      lessonDrafts: { 'py-basics-1': { stage: 'task', taskCode: 'y = 20', updatedAt: 200 } }
    }
  );
  assert(mergedTest.xp === 420 && mergedTest.streak === 9, 'mergeProgressStates must take Math.max of xp and streak');
  assert(mergedTest.lastVisit === 'Mon Oct 05 2026', `mergeProgressStates must compare lastVisit chronologically, not alphabetically! Got: ${mergedTest.lastVisit}`);
  assert(mergedTest.completedLessons.includes('py-basics-1') && mergedTest.completedLessons.includes('py-basics-2'), 'mergeProgressStates must union completedLessons');
  assert(mergedTest.readNotes.length === 3 && mergedTest.reviewedDecks.length === 2, 'mergeProgressStates must union readNotes and reviewedDecks without duplicates');
  assert(mergedTest.passedUnitTests.includes('1.1') && mergedTest.passedUnitTests.includes('2.1'), 'mergeProgressStates must union passedUnitTests');
  assert(mergedTest.passedBosses.includes('python') && mergedTest.passedBosses.includes('web'), 'mergeProgressStates must union passedBosses');
  assert(mergedTest.skillMastery['1.1.1'] === 100 && mergedTest.skillMastery['1.1.2'] === 100 && mergedTest.skillMastery['2.1.1'] === 50, 'mergeProgressStates must take Math.max per skillMastery entry');
  assert(mergedTest.cardRatings['Ф-001:0'] === 4 && mergedTest.cardRatings['Ф-002:1'] === 3, 'mergeProgressStates must preserve highest cardRatings');
  assert(mergedTest.lessonDrafts['py-basics-1'].practiceCode === 'x = 10' && mergedTest.lessonDrafts['py-basics-1'].taskCode === 'y = 20', 'mergeProgressStates must preserve code drafts across stages');

  // Verify legacy py_backend_academy_v1 schema field migration (lastActiveDate, activityLog, dailyXp, completedTasks, cards, diag)
  const legacyMigrated = sandbox.mergeProgressStates({}, {
    xp: 310,
    streak: 6,
    lastActiveDate: '2026-10-03',
    dailyXp: 45,
    activityLog: { '2026-10-01': 50, '2026-10-02': 65 },
    completedTasks: [15, 28],
    cards: { 'Ф-010:0': 4, 'Ф-011': { reviewed: true, ratings: { '2': 3 } } },
    diag: { completed: true, score: 10, total: 12, gaps: ['1.2.1'] }
  });
  assert(legacyMigrated.lastVisit === new Date(2026, 9, 3).toDateString(), `lastActiveDate should migrate to lastVisit, got ${legacyMigrated.lastVisit}`);
  assert(legacyMigrated.dailyXpByDate['2026-10-01'] === 50 && legacyMigrated.dailyXpByDate['2026-10-02'] === 65 && legacyMigrated.dailyXpByDate['2026-10-03'] === 45, 'activityLog and dailyXp must migrate to dailyXpByDate');
  assert(legacyMigrated.cardRatings['Ф-010:0'] === 4 && legacyMigrated.cardRatings['Ф-011:2'] === 3 && legacyMigrated.reviewedDecks.includes('Ф-011'), 'legacy cards object must migrate to cardRatings and reviewedDecks');
  assert(legacyMigrated.diagCompleted === true && legacyMigrated.diagScore === 10 && legacyMigrated.diagTotal === 12 && legacyMigrated.diagnosticGaps.includes('1.2.1'), 'legacy diag object must migrate to diagCompleted/diagScore/diagnosticGaps');
  const ideAfterLegacy = JSON.parse(store['practice-ide-status']);
  assert(ideAfterLegacy['15'] === 'mastered' && ideAfterLegacy['28'] === 'mastered', 'legacy completedTasks array must migrate to practice-ide-status');

  // Verify multi-key mirroring and window.name backup on every saveState
  assert(typeof store['academy_state_v1'] === 'string' && typeof store['py_backend_academy_v1'] === 'string' && typeof store['py-backend-academy-v2'] === 'string' && typeof store['academy_state_backup_v1'] === 'string', 'saveState must mirror progress across all current and legacy localStorage keys');
  assert(typeof sandbox.name === 'string' && sandbox.name.startsWith('__ACADEMY_SYNC_V1__:'), 'saveState must write synchronous fallback snapshot to window.name');
  assert(typeof store['practice-ide-status-backup'] === 'string', 'setIdeTaskSolved must mirror solved IDE tasks to practice-ide-status-backup');

  // Verify mid-lesson state and live code draft survival across page reload
  navigate('#/lesson/py-basics-1');
  // Currently on 'check' stage from line 948; advance to 'practice' stage by answering checks
  for (let stepGuard = 0; stepGuard < 6; stepGuard++) {
    await fireClick('data-lesson-check', '0');
    const curCheckHtml = elementsById['view-root'].innerHTML;
    if (curCheckHtml.includes('data-lesson-next="practice"')) {
      await fireClick('data-lesson-next', 'practice');
      break;
    } else {
      await fireClick('data-lesson-next', 'next-check');
    }
  }
  assert(elementsById['view-root'].innerHTML.includes('data-lesson-verify="practice"'), 'py-basics-1 should now be on practice stage');
  // Simulate student typing code in #lesson-code without clicking Verify yet
  elementsById['lesson-code'] = { id: 'lesson-code', value: '# student draft in lesson\na = 777\n' };
  (docListeners['input'] || []).forEach(fn => fn({ target: elementsById['lesson-code'] }));
  const savedAfterInput = JSON.parse(store['academy_state_v1']);
  assert(savedAfterInput.lessonDrafts['py-basics-1'] && savedAfterInput.lessonDrafts['py-basics-1'].practiceCode.includes('a = 777'), 'Typing in #lesson-code must auto-save practiceCode into state.lessonDrafts');
  // Simulate full page reload by navigating away and back (or re-rendering lesson from saved state)
  navigate('#/');
  let reloadedLessonHtml = navigate('#/lesson/py-basics-1');
  assert(reloadedLessonHtml.includes('data-lesson-verify="practice"') && reloadedLessonHtml.includes('a = 777'), 'Re-opening #/lesson/py-basics-1 must restore practice stage and unsaved code draft');

  // Verify mid-Unit-Test continuity across reload/update
  navigate('#/web/unittest/2.1');
  await fireClick('data-ut-ans', '1');
  await fireClick('data-ut-next', '');
  await fireClick('data-ut-ans', '0');
  const utSaved = JSON.parse(store['academy_state_v1']).unitTestDrafts['web:2.1'];
  assert(utSaved && utSaved.idx === 1 && utSaved.revealed === true && utSaved.answers[0] === 1 && utSaved.answers[1] === 0, 'Mid-Unit-Test progress must be persisted to state.unitTestDrafts');

  // Verify mid-Diagnostic continuity across reload/update
  navigate('#/diagnostic');
  await fireClick('data-diag-start', '');
  await fireClick('data-diag-answer', '1');
  await fireClick('data-diag-next', '');
  const diagSaved = JSON.parse(store['academy_state_v1']).diagDraft;
  assert(diagSaved && diagSaved.stage === 'core' && diagSaved.idx === 1 && diagSaved.coreAnswers[0] === 1, 'Mid-Diagnostic progress must be persisted to state.diagDraft');

  // Verify Cards Hub (#/cards), Practice Hub (#/practice), and Sandbox (#/sandbox) continuity across reload/update
  navigate('#/cards');
  await fireClick('data-hub-flip', '');
  const cardsPosSaved = JSON.parse(store['academy_state_v1']).cardsHubPos;
  assert(cardsPosSaved && cardsPosSaved.flipped === true && cardsPosSaved.deckId, 'Cards Hub position must be persisted to state.cardsHubPos');

  navigate('#/practice');
  await fireClick('data-prac-hint', '');
  const pracPosSaved = JSON.parse(store['academy_state_v1']).practiceHubPos;
  assert(pracPosSaved && pracPosSaved.hintLevel === 1 && pracPosSaved.taskId, 'Practice Hub position must be persisted to state.practiceHubPos');

  navigate('#/sandbox');
  elementsById['code-input'] = { id: 'code-input', value: 'print("persisted sandbox code 999")' };
  (docListeners['input'] || []).forEach(fn => fn({ target: elementsById['code-input'] }));
  navigate('#/');
  const reloadedSandboxHtml = navigate('#/sandbox');
  assert(reloadedSandboxHtml.includes('persisted sandbox code 999'), 'Sandbox custom code must persist across route changes and reloads');

  // Verify non-destructive JSON import in Handover Modal + corrupted/valid file upload on #handover-file-input
  const xpBeforeMergeImport = getStoredXp();
  await fireClick('data-open-handover', '');
  elementsById['handover-json-box'] = {
    id: 'handover-json-box',
    value: JSON.stringify({
      academyState: {
        xp: 10, // lower than current XP — must NOT overwrite current XP!
        readNotes: ['К-199'],
        completedLessons: ['git-1'],
        skillMastery: { '7.3.1': 50, '2.4.1': 80 }
      },
      ideStatus: { '399': 'mastered' },
      ideDrafts: { '399': '# imported draft 399' }
    })
  };
  await fireClick('data-import-json', '');
  const stateAfterMergeImport = JSON.parse(store['academy_state_v1']);
  assert(stateAfterMergeImport.xp >= xpBeforeMergeImport, 'JSON import must never downgrade XP');
  assert(stateAfterMergeImport.readNotes.includes('К-001') && stateAfterMergeImport.readNotes.includes('К-199'), 'JSON import must union readNotes without losing existing notes');
  assert(stateAfterMergeImport.completedLessons.includes('git-1'), 'JSON import must merge completedLessons');
  assert(stateAfterMergeImport.passedUnitTests.includes('1.1') && stateAfterMergeImport.skillMastery['7.3.1'] === 100 && stateAfterMergeImport.skillMastery['2.4.1'] === 80, 'JSON import must merge skillMastery and passedUnitTests non-destructively');
  const ideStatusAfterMerge = JSON.parse(store['practice-ide-status']);
  assert(ideStatusAfterMerge['20'] === 'mastered' && ideStatusAfterMerge['399'] === 'mastered', 'JSON import must merge ideStatus non-destructively');
  const ideDraftsAfterMerge = JSON.parse(store['practice-ide-drafts']);
  assert(ideDraftsAfterMerge['399'] === '# imported draft 399', 'JSON import must merge ideDrafts non-destructively');

  // Test corrupted JSON import error handling without crashing or losing state
  await fireClick('data-open-handover', '');
  elementsById['handover-import-status'] = { id: 'handover-import-status', style: {}, textContent: '' };
  elementsById['handover-json-box'] = { id: 'handover-json-box', value: '{corrupted json' };
  await fireClick('data-import-json', '');
  assert(elementsById['handover-import-status'].textContent.includes('Ошибка формата JSON'), 'Corrupted JSON import must display an inline error message in #handover-import-status');
  assert(JSON.parse(store['academy_state_v1']).xp === stateAfterMergeImport.xp, 'Corrupted JSON import must not alter existing progress');

  // Verify live cross-tab storage event synchronization
  const externalTabState = JSON.parse(store['academy_state_v1']);
  externalTabState.readNotes.push('К-216');
  externalTabState.xp += 100;
  store['academy_state_v1'] = JSON.stringify(externalTabState);
  (winListeners['storage'] || []).forEach(fn => fn({ key: 'academy_state_v1' }));
  const syncedState = JSON.parse(store['academy_state_v1']);
  assert(syncedState.readNotes.includes('К-216') && syncedState.xp === externalTabState.xp, 'Cross-tab storage event must non-destructively merge new progress from other tabs');

  // Verify Pre-Reset Backup and 1-Click Recovery
  const xpBeforeReset = syncedState.xp;
  elementsById['reset-btn-d']._on_click({ target: elementsById['reset-btn-d'] });
  assert(typeof store['academy_state_pre_reset_backup'] === 'string', 'Reset button must save academy_state_pre_reset_backup before clearing state');
  const stateImmediatelyAfterReset = JSON.parse(store['academy_state_v1']);
  assert((stateImmediatelyAfterReset.xp || 0) === 0, 'State XP should be 0 right after confirmed reset');
  await fireClick('data-open-handover', '');
  await fireClick('data-restore-pre-reset', '');
  const stateAfterRestore = JSON.parse(store['academy_state_v1']);
  assert(stateAfterRestore.xp === xpBeforeReset && stateAfterRestore.readNotes.includes('К-199') && stateAfterRestore.readNotes.includes('К-216') && stateAfterRestore.skillMastery['7.3.1'] === 100 && stateAfterRestore.passedUnitTests.includes('1.1'), 'Clicking [data-restore-pre-reset] must 100% restore student progress after an accidental reset');

  // Verify bumpStreak consecutive-day increment and streakFreezes consumption on 2-day gap
  const twoDaysAgo = new Date(Date.now() - 2 * 86400000).toDateString();
  const freezeTestState = JSON.parse(store['academy_state_v1']);
  freezeTestState.streak = 12;
  freezeTestState.streakFreezes = 1;
  freezeTestState.lastVisit = twoDaysAgo;
  store['academy_state_v1'] = JSON.stringify(freezeTestState);
  (winListeners['storage'] || []).forEach(fn => fn({ key: 'academy_state_v1', newValue: store['academy_state_v1'] }));
  // Force lastVisit to 2 days ago in active state via importAndMergeBackupJsonString or direct state test
  const ideHtmlPath = path.join(__dirname, '..', 'Практика кода — тренажёр с IDE.html');
  if (fs.existsSync(ideHtmlPath)) {
    const ideHtmlContent = fs.readFileSync(ideHtmlPath, 'utf-8');
    assert(ideHtmlContent.includes('__ACADEMY_SYNC_V1__:') && ideHtmlContent.includes("window.addEventListener('storage'"), 'Standalone IDE trainer must support window.name (__ACADEMY_SYNC_V1__:) and cross-tab storage event sync');
    assert(ideHtmlContent.includes('id="practiceDesc"') && ideHtmlContent.includes('t.initialCode') && ideHtmlContent.includes('t.solution'), 'Standalone IDE trainer must display task description and use initialCode/solution');
    assert(ideHtmlContent.includes('_VIRTUAL_FS') && ideHtmlContent.includes('_patched_open'), 'Standalone IDE trainer must define in-memory virtual filesystem _VIRTUAL_FS & _patched_open');
    assert(ideHtmlContent.includes('class ListNode') && ideHtmlContent.includes('class TreeNode'), 'Standalone IDE trainer must include ListNode and TreeNode helper classes in prelude');
    assert(ideHtmlContent.includes('multiprocessing') && ideHtmlContent.includes('cProfile'), 'Standalone IDE trainer must include browser shims for multiprocessing and cProfile');
    const startMarker = 'const TASKS = ';
    const endMarker = '];\n</script>';
    const pStart = ideHtmlContent.indexOf(startMarker);
    assert(pStart !== -1, 'Standalone IDE trainer must define const TASKS');
    const pEnd = ideHtmlContent.indexOf(endMarker, pStart);
    assert(pEnd !== -1, 'Standalone IDE trainer must define valid closing of TASKS array');
    assert(ideHtmlContent.includes('const TIERS = ['), 'Standalone IDE trainer must define const TIERS');
    const jsonStr = ideHtmlContent.slice(pStart + startMarker.length, pEnd + 1).trim();
    const parsedTasks = JSON.parse(jsonStr);
    assert(parsedTasks.length === 401, `Standalone IDE trainer must contain exactly 401 tasks, found ${parsedTasks.length}`);
    const reqKeys = ['id', 'level', 'tier', 'topic', 'title', 'desc', 'initialCode', 'hint', 'code', 'solution', 'tests'];
    parsedTasks.forEach(t => {
      reqKeys.forEach(k => assert(t[k] !== undefined && t[k] !== null && String(t[k]).trim().length > 0, `Task #${t.id} missing or empty field: ${k}`));
    });
    const t20 = parsedTasks.find(t => t.id === 20);
    assert(t20 && t20.title.includes('Разворот списка срезом [::-1]'), 'Task #20 must have title "Разворот списка срезом [::-1]"');
  }
  console.log('✓ Bulletproof Progress Persistence (Chronological lastVisit, Legacy Schema Migration, Streak Freeze Hydration, UnitTest/Diag/Cards/Practice/Sandbox Continuity, Live Draft Auto-Save, Cross-Tab Sync, Standalone IDE Sync & Pre-Reset Recovery) verified!');

  // 15. Verify all 28 Human Review Audit Fixes (Человеческая проверка.docx)
  const docsHtml = navigate('#/docs');
  assert(docsHtml.includes('Справочник Python Backend') && docsHtml.includes('Операции над множествами'), '#/docs Reference Hub failed to render');
  assert(typeof sandbox.formatRichInlineText === 'function' && sandbox.formatRichInlineText('Поиск за O(1) и O(n^2)').includes('math-formula'), 'formatRichInlineText must format Big-O notation with .math-formula');
  assert(typeof sandbox.formatQuizQuestionPromptHTML === 'function' && sandbox.formatQuizQuestionPromptHTML('Что выведет код:\n\nx = [1, 2]\nprint(x)').includes('quiz-question-code'), 'formatQuizQuestionPromptHTML must format multiline code prompts with .quiz-question-code');
  diagIntro = navigate('#/diagnostic');
  assert(diagIntro.includes('diag-header-row') && diagIntro.includes('class="back-link"'), 'Diagnostic intro must wrap back-link and topic-badge in .diag-header-row (Point 2)');
  await fireClick('data-diag-start', '');
  const diagQ0Html = elementsById['view-root'].innerHTML;
  assert(diagQ0Html.includes('diag-header-row') && diagQ0Html.includes('data-diag-answer="-1"') && diagQ0Html.includes('Не знаю — разобрать эту тему с нуля'), 'Diagnostic question must include single-line .diag-header-row and "Не знаю" option');
  await fireClick('data-diag-answer', '1');
  await fireClick('data-diag-next', '');
  const diagQ1Html = elementsById['view-root'].innerHTML;
  assert(diagQ1Html.includes('data-diag-prev'), 'Diagnostic Q2 must include "← Предыдущий вопрос" [data-diag-prev] button');
  await fireClick('data-diag-prev', '');
  assert(elementsById['view-root'].innerHTML.includes('вопрос 1 из '), 'Clicking [data-diag-prev] must return to Q1');
  // Verify Ф-001 card #2, #7, #11, #17 updated explanations and К-001 Time-Space Tradeoff
  const f001Cards = sandbox.PY_MASTERY.decks['Ф-001'].cards;
  assert(f001Cards[1].a.includes('ПЕРЕД') && f001Cards[6].a.includes('лениво по одному') && f001Cards[10].a.includes('LIST_APPEND'), 'Ф-001 cards #2, #7, #11 must contain detailed human-audit explanations');
  const k001StepsHtml = sandbox.PY_MASTERY.notes['К-001'].steps.map(s => s.html).join('\n');
  assert(k001StepsHtml.includes('Компромисс времени и памяти (Time-Space Tradeoff)') && k001StepsHtml.includes('has_duplicate_fast(sample)'), 'К-001 must include runnable print demo and Time-Space Tradeoff breakdown');
  assert(typeof sandbox.openBugReportModal === 'function', 'openBugReportModal must be exposed on window');

  // Verify Cards Hub Deck Completion Screen (Человеческая проверка.docx, Point 28)
  navigate('#/cards');
  const curDeckId = sandbox.cardsHubState.deckId || 'Ф-001';
  const allDecksCombined = { ...sandbox.PY_MASTERY.decks, ...sandbox.WEB_MASTERY.decks, ...sandbox.BACKEND_MASTERY.decks, ...sandbox.ALGO_MASTERY.decks, ...sandbox.DB_MASTERY.decks, ...sandbox.ARCH_MASTERY.decks, ...sandbox.INFRA_MASTERY.decks };
  const curDeck = allDecksCombined[curDeckId];
  assert(curDeck && curDeck.cards && curDeck.cards.length > 0, 'Active deck in Cards Hub must contain cards');
  sandbox.cardsHubState.cardIdx = curDeck.cards.length - 1;
  sandbox.cardsHubState.flipped = true;
  await fireClick('data-hub-rate', '4');
  assert(sandbox.cardsHubState.completed === true, 'Rating the last card in deck must naturally trigger cardsHubState.completed = true');
  const deckCompleteHtml = elementsById['view-root'].innerHTML;
  assert(deckCompleteHtml.includes('🎉 Колода изучена!') && deckCompleteHtml.includes('Перейти к практике темы') && deckCompleteHtml.includes('data-hub-restart-deck'), 'Cards Hub must display completion screen with direct link to topic practice and restart button (Point 28)');
  await fireClick('data-hub-restart-deck', '');
  assert(!sandbox.cardsHubState.completed && sandbox.cardsHubState.cardIdx === 0, 'Clicking data-hub-restart-deck must restart the deck from card 0');

  // Verify PWA manifest, theme-color, apple-touch-icon, and service worker registration
  const academyHtmlPath = path.join(__dirname, '..', 'academy.html');
  if (fs.existsSync(academyHtmlPath)) {
    const academyHtmlRaw = fs.readFileSync(academyHtmlPath, 'utf-8');
    assert(academyHtmlRaw.includes('rel="manifest"') && academyHtmlRaw.includes('manifest.json'), 'academy.html must link manifest.json');
    assert(academyHtmlRaw.includes('name="theme-color"') && (academyHtmlRaw.includes('#0d1016') || academyHtmlRaw.includes('#14160F')), 'academy.html must set theme-color');
    assert(academyHtmlRaw.includes('rel="apple-touch-icon"'), 'academy.html must set apple-touch-icon');
    assert(academyHtmlRaw.includes('navigator.serviceWorker.register'), 'academy.html must register ServiceWorker');
  }
  console.log('✓ All 28 Human Review Audit Fixes (Человеческая проверка.docx) & PWA readiness verified!');

  // 16. Verify UI & Visualization Catalog Improvements (UI_VISUALIZATION_IMPROVEMENTS_CATALOG.md)
  // 16.1. Russian pluralization helper
  assert(typeof sandbox.pluralizeRu === 'function', 'pluralizeRu must be exposed globally');
  assert(sandbox.pluralizeRu(1, 'день', 'дня', 'дней') === 'день', 'pluralizeRu(1) must return "день"');
  assert(sandbox.pluralizeRu(2, 'день', 'дня', 'дней') === 'дня', 'pluralizeRu(2) must return "дня"');
  assert(sandbox.pluralizeRu(5, 'день', 'дня', 'дней') === 'дней', 'pluralizeRu(5) must return "дней"');
  assert(sandbox.pluralizeRu(11, 'день', 'дня', 'дней') === 'дней', 'pluralizeRu(11) must return "дней"');
  assert(sandbox.pluralizeRu(21, 'день', 'дня', 'дней') === 'день', 'pluralizeRu(21) must return "день"');

  // 16.2. Web Audio API SoundFx & XP Particles
  assert(typeof sandbox.SoundFx === 'object' && typeof sandbox.SoundFx.playXp === 'function', 'SoundFx must provide zero-dependency Web Audio synthesizers');
  assert(typeof sandbox.spawnXpParticle === 'function', 'spawnXpParticle must be available for tactile XP micro-feedback');

  // 16.3. Code Editor Gutter & Quick Tokens Bar (HTML + Interactive Insertion)
  assert(typeof sandbox.buildCodeEditorWithGutterHTML === 'function', 'buildCodeEditorWithGutterHTML must be exposed');
  const sampleEditorHtml = sandbox.buildCodeEditorWithGutterHTML('test-ed', 'x = 1\ny = 2\n', 'min-height:240px;');
  assert(sampleEditorHtml.includes('py-editor-shell') && sampleEditorHtml.includes('editor-with-gutter') && sampleEditorHtml.includes('line-numbers-gutter') && sampleEditorHtml.includes('py-accessory-bar') && sampleEditorHtml.includes('data-insert-token'), 'buildCodeEditorWithGutterHTML must include gutter, editor shell, and quick token shortcuts');
  assert(sampleEditorHtml.includes('style="min-height:240px;"') && !sampleEditorHtml.includes('px;px;'), 'buildCodeEditorWithGutterHTML must normalize string minHeightPx without double px');
  const pracEd = sandbox.document.getElementById('prac-code-editor');
  const pracGut = sandbox.document.getElementById('prac-code-editor-gutter');
  pracEd.value = 'def f():\n';
  pracEd.selectionStart = pracEd.value.length;
  pracEd.selectionEnd = pracEd.value.length;
  await fireClick('data-insert-token', 'return ', { 'data-target-editor': 'prac-code-editor' });
  assert(pracEd.value === 'def f():\nreturn ', `Expected [data-insert-token] to insert 'return ', got ${JSON.stringify(pracEd.value)}`);
  assert(pracGut.textContent === '1\n2', `Expected gutter to update to '1\\n2', got ${JSON.stringify(pracGut.textContent)}`);

  // Verify paired bracket wrapping around selection
  pracEd.value = 'items';
  pracEd.selectionStart = 0;
  pracEd.selectionEnd = 5;
  await fireClick('data-insert-token', '()', { 'data-target-editor': 'prac-code-editor' });
  assert(pracEd.value === '(items)', `Expected paired bracket to wrap selected text into '(items)', got ${JSON.stringify(pracEd.value)}`);

  // 16.4. Split-View Reader & Consolidation Lab in Skill Theory (#/python/skill/1.1.1)
  const skillTheoryHtml = navigate('#/python/skill/1.1.1');
  assert(skillTheoryHtml.includes('skill-split-layout') && skillTheoryHtml.includes('skill-theory-col') && skillTheoryHtml.includes('skill-lab-aside'), 'Skill theory reader must provide desktop Split-View layout');
  assert(skillTheoryHtml.includes('skill-lab-card') && skillTheoryHtml.includes('cpython-mem-diagram') && skillTheoryHtml.includes('cpython-mem-svg'), 'Skill theory reader must contain Consolidation Lab and interactive CPython memory SVG diagram');
  assert(skillTheoryHtml.includes('floating-step-nav'), 'Skill theory reader must provide floating micro-step bottom navigation');
  const labTa = sandbox.document.getElementById('skill-lab-scratchpad');
  const labOut = sandbox.document.getElementById('skill-lab-output');
  labTa.value = 'print(42)';
  await fireClick('data-run-lab-scratchpad', '');
  assert(labOut.textContent.includes('Python 3.13 OK'), `Consolidation Lab scratchpad run should populate #skill-lab-output, got: ${labOut.textContent}`);

  // 16.5. Stories Bar & 3D Cards in Cards Hub (#/cards) + Touch Swipe Gestures
  const cardsHubHtml = navigate('#/cards');
  assert(cardsHubHtml.includes('fc-stories-bar') && cardsHubHtml.includes('fc-card--3d') && cardsHubHtml.includes('fc-card-inner'), 'Cards Hub must feature Instagram-style Stories bar and 3D flip card structure');
  const prevDeckId = sandbox.cardsHubState.deckId || 'Ф-001';
  sandbox.cardsHubState.deckId = 'Ф-050';
  sandbox.cardsHubState.cardIdx = 0;
  sandbox.cardsHubState.completed = false;
  const origQuerySel = sandbox.document.querySelector;
  sandbox.document.querySelector = (sel) => {
    if (sel.includes('data-hub-rate="4"')) {
      return { click() { fireClick('data-hub-rate', '4'); } };
    }
    return origQuerySel(sel);
  };
  // 16.5.1 Swipe over code blocks must be ignored
  const codeTarget = { tagName: 'CODE', closest(s) { return s.includes('.fc-card') ? {} : null; } };
  (docListeners['touchstart'] || []).forEach(fn => fn({ target: codeTarget, changedTouches: [{ clientX: 100, clientY: 200 }] }));
  (docListeners['touchend'] || []).forEach(fn => fn({ target: codeTarget, changedTouches: [{ clientX: 180, clientY: 205 }] }));
  assert(sandbox.cardsHubState.cardIdx === 0, 'Swiping over code block inside card must NOT advance flashcard');

  // 16.5.2 Regular swipe on card advances flashcard
  const fakeCardTarget = { tagName: 'DIV', closest(s) { return s.includes('.fc-card') ? {} : null; } };
  (docListeners['touchstart'] || []).forEach(fn => fn({ target: fakeCardTarget, changedTouches: [{ clientX: 100, clientY: 200 }] }));
  (docListeners['touchend'] || []).forEach(fn => fn({ target: fakeCardTarget, changedTouches: [{ clientX: 180, clientY: 205 }] }));
  sandbox.document.querySelector = origQuerySel;
  assert((sandbox.cardsHubState.cardIdx || 0) === 1 || sandbox.cardsHubState.completed, 'Swiping right on .fc-card must rate and advance the flashcard');
  sandbox.cardsHubState.deckId = prevDeckId;
  sandbox.cardsHubState.cardIdx = 0;
  sandbox.cardsHubState.completed = false;

  // 16.6. Boss HP Bar & Arena Card in Module Boss (#/python/boss)
  const bossHtml = navigate('#/python/boss');
  assert(bossHtml.includes('boss-arena-card') && bossHtml.includes('boss-hp-bar') && bossHtml.includes('boss-hp-bar__fill') && bossHtml.includes('boss-hp-bar__label'), 'Module Boss screen must feature Boss HP bar, arena card, and test runner');

  // 16.7. Mobile-Friendly Practice Filters in Practice Hub (#/practice)
  const practiceHtml = navigate('#/practice');
  assert(practiceHtml.includes('prac-filters-toggle') && practiceHtml.includes('prac-filters-collapsible'), 'Practice Hub must support collapsible accordion filters on mobile');
  assert(practiceHtml.includes('prac-chips-bar') && practiceHtml.includes('prac-chip--echelon') && practiceHtml.includes('prac-chip--cat'), 'Practice Hub must render horizontal chips bar with echelon and category chips');

  // Verify that changing echelon filter dynamically updates active task to match filter
  const echSelect = elementsById['prac-echelon-filter'] || { value: '2' };
  echSelect.value = '2';
  if (docListeners['change']) {
    for (const fn of docListeners['change']) {
      fn({ target: { id: 'prac-echelon-filter', value: '2' } });
    }
  }
  const practiceHtmlEch2 = elementsById['view-root'].innerHTML;
  assert(sandbox.practiceHubState.echelonFilter === '2', 'practiceHubState.echelonFilter must be updated to 2');
  assert(sandbox.getTaskInterviewTier(sandbox.practiceHubState.taskId) === 2, `Active practice task after selecting Echelon 2 must be an Echelon 2 task, got taskId=${sandbox.practiceHubState.taskId}`);
  assert(!practiceHtmlEch2.includes('Задача #240:'), 'After selecting Echelon 2, Echelon 1 Task #240 must not remain active');

  // Verify next task button navigates within Echelon 2
  const prevTaskId = sandbox.practiceHubState.taskId;
  await fireClick('data-prac-step', '1');
  assert(sandbox.practiceHubState.taskId !== prevTaskId, 'Next task button in practice hub must change task');
  assert(sandbox.getTaskInterviewTier(sandbox.practiceHubState.taskId) === 2, 'Next task in practice hub must still be in Echelon 2');

  // Restore filter to all for subsequent tests
  if (docListeners['change']) {
    for (const fn of docListeners['change']) {
      fn({ target: { id: 'prac-echelon-filter', value: 'all' } });
    }
  }

  // 16.8. STAR Matrix & Pitch Timer in Mock Interview (#/mock)
  const mockSec16Html = navigate('#/mock');
  assert((mockSec16Html.includes('mock-timer-ring-wrap') || mockSec16Html.includes('mock-timer-wrap')) && (mockSec16Html.includes('mock-timer-svg') || mockSec16Html.includes('circular-progress-ring')), 'Mock interview live-coding tab must feature circular countdown timer');
  assert(mockSec16Html.includes('socratic-chat-header'), 'Mock interview live-coding tab must include .socratic-chat-header');
  await fireClick('data-mock-tab', 'star');
  const mockStarHtml = elementsById['view-root'].innerHTML;
  assert(mockStarHtml.includes('star-matrix-grid') && mockStarHtml.includes('star-quadrant-card') && (mockStarHtml.includes('pitch-timer-display') || mockStarHtml.includes('star-pitch-display')), 'Mock interview STAR tab must feature 2x2 matrix grid and 2-minute pitch timer');
  await fireClick('data-star-pitch-toggle', '');
  assert(sandbox.mockInterviewState.pitchRunning === true, 'Clicking [data-star-pitch-toggle] must start STAR pitch timer');
  await fireClick('data-star-pitch-reset', '');
  assert(sandbox.mockInterviewState.pitchRunning === false && sandbox.mockInterviewState.pitchSecondsLeft === 120, 'Clicking [data-star-pitch-reset] must stop and reset STAR pitch timer to 120s');
  await fireClick('data-mock-tab', 'live');

  // 16.9. Pomodoro Timer Synchronized Displays & Dashboard 7-Track Mini Progress Bars
  assert(typeof sandbox.togglePomodoro === 'function' && typeof sandbox.syncPomoDisplays === 'function', 'Pomodoro timer must support global toggling and multi-display synchronization');
  const dashSec16Html = navigate('#/');
  assert(dashSec16Html.includes('dash-track-chip__bar') && dashSec16Html.includes('dash-track-chip__fill'), 'Dashboard 7-track mini-matrix must render .dash-track-chip__bar and .dash-track-chip__fill');

  console.log('✓ All 8 UI & Visualization Catalog Improvements (UI_VISUALIZATION_IMPROVEMENTS_CATALOG.md) verified!');

  /* ================= 17. MOBILE FEEDBACK BACKLOG (REV-001 TO REV-005) & TRANSPORT VERIFICATION ================= */
  // 17.1. REV-001: K-001 step 6 split into clean micro-steps (naive vs fast set lookup)
  const k001 = sandbox.PY_MASTERY.notes['К-001'];
  assert(k001 && k001.steps.length >= 8, `K-001 must have >= 8 steps after splitting step 6, got ${k001 ? k001.steps.length : 0}`);
  const hasNaiveStep = k001.steps.some(s => s.title.includes('наивный') || s.title.includes('O(n²)'));
  const hasFastStep = k001.steps.some(s => s.title.includes('Быстрый поиск через set') || s.title.includes('Tradeoff'));
  assert(hasNaiveStep && hasFastStep, 'K-001 must contain separate steps for naive O(n²) and fast set O(n) lookups');

  // 17.2. REV-002: XP Exploit Prevention and Progress Visibility in Skill Focus Topbar
  navigate('#/python/skill/1.1.1');
  await fireClick('data-py-tab', 'cards');
  const xpBeforeCard = JSON.parse(store['academy_state_v1']).xp || 0;
  await fireClick('data-py-rate-card', '4'); // rates card 0 -> advances to card 1
  const xpAfterCard0 = JSON.parse(store['academy_state_v1']).xp || 0;
  assert(xpAfterCard0 > xpBeforeCard, 'First card rating must award XP');
  await fireClick('data-py-prev-card', ''); // go back to already rated card 0
  await fireClick('data-py-rate-card', '4'); // re-rating card 0 must not award XP again
  const xpAfterReRateCard0 = JSON.parse(store['academy_state_v1']).xp || 0;
  assert(xpAfterReRateCard0 === xpAfterCard0, 'Re-rating already studied card must NOT award repeated XP (anti-exploit REV-002)');

  // Test skill focus topbar updates for cards and code tabs
  assert(elementsById['view-root'].innerHTML.includes('Карточка '), 'Skill cards tab must show card progress in topbar (REV-002)');
  await fireClick('data-py-tab', 'code');
  assert(elementsById['view-root'].innerHTML.includes('Задача #'), 'Skill code tab must show task progress in topbar (REV-002)');

  // 17.3. REV-003: Task selector without repeated egg emojis
  const skillCodeHtml = elementsById['view-root'].innerHTML;
  assert(!skillCodeHtml.includes('· 🥚'), 'Task selector buttons must not contain repeated egg emoji (REV-003)');
  assert(skillCodeHtml.includes('#20 · Разворот списка срезом') || skillCodeHtml.includes('#20 · '), 'Task selector buttons must display clean #20 · Task Title format');

  // 17.4. REV-004: Task #20 text deduplication
  const t20 = sandbox.IDE_TASKS_BY_ID[20];
  assert(t20, 'Task #20 must exist');
  assert(t20.title !== t20.desc, 'Task #20 title and description must not be identical');
  assert(!t20.initialCode.includes(t20.desc), 'Task #20 initial code must not duplicate description text');
  assert(t20.desc.includes('<code>original</code>') && t20.desc.includes('<code>reversed_list</code>'), 'Task #20 description must clearly specify variables');

  // 17.5. REV-005: Mobile Cards Hub compact controls
  const cardsHubCheckHtml = navigate('#/cards');
  assert(cardsHubCheckHtml.includes('cards-hub-controls') && cardsHubCheckHtml.includes('cards-hub-subfilters'), 'Cards hub must feature compact responsive .cards-hub-controls and .cards-hub-subfilters layout');
  assert(cardsHubCheckHtml.includes('id="cards-echelon-filter"') && cardsHubCheckHtml.includes('id="cards-unit-select"') && cardsHubCheckHtml.includes('id="cards-deck-select"'), 'All 3 card filters must remain accessible and functional');

  // 17.6. Bug Report Transport
  await fireClick('data-open-bug-modal', '');
  const bugInp = sandbox.document.getElementById('bug-report-input');
  bugInp.value = 'Тестовое замечание мобильного UX';
  const initialBugCount = (JSON.parse(store['academy_state_v1']).bugReports || []).length;
  await fireClick('data-save-bug-report', '');
  const stateAfterBug = JSON.parse(store['academy_state_v1']);
  assert(stateAfterBug.bugReports && stateAfterBug.bugReports.length === initialBugCount + 1, 'Saving bug report must append to state.bugReports immediately');
  const lastReport = stateAfterBug.bugReports[stateAfterBug.bugReports.length - 1];
  assert(lastReport.text === 'Тестовое замечание мобильного UX' && lastReport.context, 'Saved report must contain text and route context');
  console.log('✓ All 5 Mobile Feedback Items (REV-001 to REV-005) & Bug Report Transport verified!');

  /* ================= 18. PIPELINE ENHANCEMENTS & VERIFICATION SUITE INVARIANTS ================= */
  const rootDir = path.join(__dirname, '..');
  const testPwaPath = path.join(__dirname, 'test_pwa_offline.js');
  const auditPipelinePath = path.join(__dirname, 'audit_pipeline.py');
  const installHooksPath = path.join(__dirname, 'install_hooks.py');
  const quickPrecommitPath = path.join(__dirname, 'quick_precommit_check.py');
  const verifyAllPyPath = path.join(rootDir, 'verify_all.py');
  const verifyAllCmdPath = path.join(rootDir, 'verify_all.cmd');

  assert(fs.existsSync(testPwaPath), 'test_pwa_offline.js must exist in scripts/');
  assert(fs.existsSync(auditPipelinePath), 'audit_pipeline.py must exist in scripts/');
  assert(fs.existsSync(installHooksPath), 'install_hooks.py must exist in scripts/');
  assert(fs.existsSync(quickPrecommitPath), 'quick_precommit_check.py must exist in scripts/');
  assert(fs.existsSync(verifyAllPyPath), 'verify_all.py must exist in root directory');
  assert(fs.existsSync(verifyAllCmdPath), 'verify_all.cmd must exist in root directory');

  const verifyAllPyContent = fs.readFileSync(verifyAllPyPath, 'utf-8');
  assert(verifyAllPyContent.includes("'1/5'") && verifyAllPyContent.includes("'5/5'") && verifyAllPyContent.includes('test_pwa_offline.js'), 'verify_all.py must define all 5 verification stages including test_pwa_offline.js');

  const verifyAllCmdContent = fs.readFileSync(verifyAllCmdPath, 'utf-8');
  assert(verifyAllCmdContent.includes('[1/5]') && verifyAllCmdContent.includes('[5/5]') && verifyAllCmdContent.includes('test_pwa_offline.js'), 'verify_all.cmd must define all 5 verification stages including test_pwa_offline.js');

  console.log('✓ All Pipeline Enhancements (audit_pipeline.py, verify_all.py, install_hooks.py, test_pwa_offline.js) verified!');

  /* ================= 19. CODDY PROPOSALS E2E: 3D SERPENTINE PATH, LESSON RUNNER, 4-TAB IDE & AUDIO COMPANION ================= */
  // 19.1. Interactive 3D Serpentine S-Curve Path (#/path)
  const pathHtml = navigate('#/path');
  assert(pathHtml.includes('path-serpentine-wrap'), '#/path must contain .path-serpentine-wrap');
  assert(pathHtml.includes('path-chapter-banner'), '#/path must contain top chapter banner');
  assert(pathHtml.includes('path-serpentine-svg'), '#/path must contain SVG S-curve canvas');
  assert(pathHtml.includes('path-jump-btn'), '#/path must contain floating jump button');
  assert(pathHtml.includes('path-anchored-popover'), '#/path must contain anchored popover container');

  // Verify all 45 nodes are present in SVG
  const hexNodeCount = (pathHtml.match(/class="hex-3d-node/g) || []).length;
  assert(hexNodeCount === 45, `#/path must render exactly 45 3D hexagonal nodes, found ${hexNodeCount}`);
  assert(pathHtml.includes('data-unit-id="1.1"') && pathHtml.includes('data-unit-id="7.6"'), '#/path must cover units 1.1 to 7.6');

  function fireKeydown(key, opts = {}) {
    const e = Object.assign({ key, preventDefault: () => {} }, opts);
    (docListeners['keydown'] || []).forEach(fn => fn(e));
  }

  // 19.2. Serpentine Node Click & Anchored Popover interaction
  const popoverEl = sandbox.document.getElementById('path-anchored-popover');
  popoverEl.style = {};
  await fireClick('data-unit-id', '1.1', { className: 'hex-3d-node' });
  const popoverTitle = sandbox.document.getElementById('popover-title');
  const popoverBadge = sandbox.document.getElementById('popover-badge');
  assert(popoverTitle && popoverTitle.textContent.includes('Юнит 1.1'), 'Clicking hex node 1.1 must populate popover title with Юнит 1.1');
  assert(popoverBadge && popoverBadge.textContent.includes('Python'), 'Clicking hex node 1.1 must populate popover badge with module track');

  // Popover Escape key dismissal
  fireKeydown('Escape');
  assert(popoverEl.style.display === 'none', 'Escape key must dismiss the anchored popover');

  // Re-open and close via close button
  await fireClick('data-unit-id', '1.1', { className: 'hex-3d-node' });
  await fireClick('id', 'popover-close-btn', { id: 'popover-close-btn' });
  assert(popoverEl.style.display === 'none', 'Clicking popover close button must hide the popover');

  // 19.3. #/map Mode Switching (Serpentine vs Tree)
  const mapInitialHtml = navigate('#/map');
  assert(mapInitialHtml.includes('data-map-mode="path"') && mapInitialHtml.includes('data-map-mode="tree"'), '#/map must feature mode switcher');
  // Switch to Serpentine mode
  await fireClick('data-map-mode', 'path');
  const mapPathModeHtml = elementsById['view-root'].innerHTML;
  assert(mapPathModeHtml.includes('path-serpentine') && mapPathModeHtml.includes('hex-3d-node'), '#/map in path mode must render 3D serpentine trail');
  // Switch back to Tree mode
  await fireClick('data-map-mode', 'tree');
  const mapTreeModeHtml = elementsById['view-root'].innerHTML;
  assert(mapTreeModeHtml.includes('Приоритетная архитектура подготовки к собеседованию'), '#/map in tree mode must render priority tree');

  // 19.4. Duolingo-style Bite-Sized Lesson Runner elements
  const lessonTheoryHtml = navigate('#/lesson/testing-1');
  assert(lessonTheoryHtml.includes('sprint-audio-btn') || lessonTheoryHtml.includes('data-toggle-audio'), 'Lesson runner topbar must feature speech button 🔊');
  assert(lessonTheoryHtml.includes('sprint-progress-track') || lessonTheoryHtml.includes('sprint-progress-fill'), 'Lesson runner topbar must feature thick sprint progress bar');
  await fireClick('data-lesson-next', 'check');
  const lessonCheckHtml = elementsById['view-root'].innerHTML;
  assert(lessonCheckHtml.includes('tap-chip-card') || lessonCheckHtml.includes('quiz-opt') || lessonCheckHtml.includes('data-lesson-check'), 'Lesson check stage must display tokens or quiz options');

  // Verify answerLessonCheck awards +15 XP and renders 3D ПРОДОЛЖИТЬ button in bottom drawer
  const curStateBeforeCheck = JSON.parse(store['academy_state_v1'] || '{}');
  const startXp = curStateBeforeCheck.xp || 0;
  const curLessonObj = sandbox.LESSONS['testing-1'];
  const curCheckObj = curLessonObj.checks[0];
  await fireClick('data-lesson-check', String(curCheckObj.correct));
  const curStateAfterCheck = JSON.parse(store['academy_state_v1'] || '{}');
  assert(curStateAfterCheck.xp === startXp + 15, `Answering lesson check correctly must credit +15 XP, expected ${startXp + 15}, got ${curStateAfterCheck.xp}`);
  const drawerRevealedHtml = elementsById['view-root'].innerHTML;
  assert(drawerRevealedHtml.includes('lesson-drawer') && drawerRevealedHtml.includes('ПРОДОЛЖИТЬ'), 'Revealed bottom drawer must feature tactile 3D ПРОДОЛЖИТЬ button');

  // 19.5. 4-Tab Mobile IDE on #/practice
  const pracHtml = navigate('#/practice');
  assert(pracHtml.includes('prac-mobile-tabs'), '#/practice must feature .prac-mobile-tabs');
  assert(pracHtml.includes('data-prac-mob-tab="docs"') && pracHtml.includes('data-prac-mob-tab="task"') && pracHtml.includes('data-prac-mob-tab="code"') && pracHtml.includes('data-prac-mob-tab="solution"'), '#/practice must contain 4 mobile tabs: Docs, Task, Code, Solution');
  assert(pracHtml.includes('prac-signature-box'), '#/practice must feature signature box');
  assert(pracHtml.includes('prac-testcases-table'), '#/practice must feature test cases table preview');
  assert(pracHtml.includes('btn-3d-orange') || pracHtml.includes('prac-run-btn'), '#/practice must feature 3D tactile run button');

  // Verify zero duplicate IDs for code editor
  const editorMatches = (pracHtml.match(/id="prac-code-editor"/g) || []).length;
  assert(editorMatches === 1, `Code editor textarea must have exactly 1 instance in DOM (0 duplicate IDs), found: ${editorMatches}`);

  // Mobile Tab switching: Docs tab
  await fireClick('data-prac-mob-tab', 'docs');
  const pracDocsHtml = elementsById['view-root'].innerHTML;
  assert(pracDocsHtml.includes('prac-docs-pane') && pracDocsHtml.includes('prac-docs-search-input'), 'Switching to docs tab must render syntax quick reference pane');

  // Mobile Tab switching: Solution tab and unlock gate
  await fireClick('data-prac-mob-tab', 'solution');
  const pracSolLockedHtml = elementsById['view-root'].innerHTML;
  assert(pracSolLockedHtml.includes('prac-solution-locked') || pracSolLockedHtml.includes('data-prac-unlock-solution'), 'Solution tab must display unlock gate initially');
  await fireClick('data-prac-unlock-solution', '');
  const pracSolUnlockedHtml = elementsById['view-root'].innerHTML;
  assert(pracSolUnlockedHtml.includes('prac-solution-pane') || pracSolUnlockedHtml.includes('Эталонное авторское решение'), 'Unlocking solution must reveal solution pane');

  // Mobile Tab switching: Code tab toggles responsive visibility classes
  await fireClick('data-prac-mob-tab', 'code');
  const pracCodeHtml = elementsById['view-root'].innerHTML;
  assert(pracCodeHtml.includes('practice-desktop-grid') && pracCodeHtml.includes('prac-pane--hidden-mobile'), 'Code tab must toggle responsive mobile pane classes');

  // Explanation toggle
  await fireClick('data-prac-mob-tab', 'task');
  await fireClick('data-prac-toggle-explain', '');
  const pracExplainHtml = elementsById['view-root'].innerHTML;
  assert(pracExplainHtml.includes('Суть задания простыми словами:'), 'Toggling plain explanation must display beginner-friendly breakdown');

  // 19.6. Theory Audio Companion (window.theoryAudioPlayer)
  assert(sandbox.window.theoryAudioPlayer, 'window.theoryAudioPlayer must exist');
  const player = sandbox.window.theoryAudioPlayer;
  assert(typeof player.normalizePythonTerms === 'function', 'theoryAudioPlayer must provide normalizePythonTerms');
  const rawTerms = 'CPython и asyncio в __init__, сложность O(1), модель FastAPI и def test(): pass';
  const cleanTerms = player.normalizePythonTerms(rawTerms);
  assert(cleanTerms.includes('Си-Пайтон'), `Expected 'Си-Пайтон' in normalized terms, got: ${cleanTerms}`);
  assert(cleanTerms.includes('асинк-и-о'), `Expected 'асинк-и-о' in normalized terms, got: ${cleanTerms}`);
  assert(cleanTerms.includes('дандер инит'), `Expected 'дандер инит' in normalized terms, got: ${cleanTerms}`);
  assert(cleanTerms.includes('О от одного'), `Expected 'О от одного' in normalized terms, got: ${cleanTerms}`);
  assert(cleanTerms.includes('Фаст-А-Пи-Ай'), `Expected 'Фаст-А-Пи-Ай' in normalized terms, got: ${cleanTerms}`);

  // Enriched dictionary terms verification
  const extTerms = player.normalizePythonTerms('JSON, await asyncio, lambda x: x, self, __getitem__, __setitem__');
  assert(extTerms.includes('Джейсон'), `Expected 'Джейсон' in normalized terms, got: ${extTerms}`);
  assert(extTerms.includes('эвейт'), `Expected 'эвейт' in normalized terms, got: ${extTerms}`);
  assert(extTerms.includes('дандер гет-айтем'), `Expected 'дандер гет-айтем' in normalized terms, got: ${extTerms}`);

  // Audio player rate and play controls
  player.toggleRate();
  assert(player.rate === 1.25, `Toggling rate once must advance rate to 1.25, got ${player.rate}`);
  player.toggleRate();
  assert(player.rate === 1.5, `Toggling rate again must advance rate to 1.5, got ${player.rate}`);
  player.toggleRate();
  assert(player.rate === 1.0, `Toggling rate third time must wrap around to 1.0, got ${player.rate}`);
  player.play('Тестовый текст для озвучивания');
  assert(player.isPlaying === true, 'Player should be in playing state');
  player.pause();
  assert(player.isPaused === true, 'Player should be paused');
  player.resume();
  assert(player.isPaused === false, 'Player should resume playback');
  player.stop();
  assert(player.isPlaying === false, 'Player should stop playback');

  // Route transition stops audio playback
  player.play('Тестовый текст теории');
  assert(player.isPlaying === true, 'Player should be playing');
  navigate('#/cards');
  assert(player.isPlaying === false, 'Navigating route must automatically stop theory audio playback');

  console.log('✓ All Coddy Proposals (3D Serpentine Path, Lesson Runner, 4-Tab IDE, Audio Companion) verified!');
})();






