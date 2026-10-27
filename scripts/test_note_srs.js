/**
 * test_note_srs.js
 * Юнит-тесты движка интервального повторения прочитанных конспектов (график 1/3/7/21/30)
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

const rootDir = path.resolve(__dirname, '..');
const htmlPath = path.join(rootDir, 'standards', 'standards.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

// Извлекаем JS-код из standards.html
const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);
assert(scriptMatch, 'script tag must exist in standards.html');
const code = scriptMatch[1];

// Подготавливаем минимальную DOM/браузерную среду
const mockLocalStorage = {};
const makeElem = () => ({
  addEventListener: () => {},
  removeEventListener: () => {},
  setAttribute: () => {},
  getAttribute: () => null,
  hasAttribute: () => false,
  removeAttribute: () => {},
  textContent: '',
  innerHTML: '',
  style: {},
  classList: { add: () => {}, remove: () => {}, toggle: () => {}, contains: () => false },
  appendChild: () => {},
  removeChild: () => {},
  insertBefore: () => {},
  querySelector: () => null,
  querySelectorAll: () => []
});

const sandbox = {
  addEventListener: () => {},
  removeEventListener: () => {},
  scrollTo: () => {},
  matchMedia: () => ({ matches: false, addEventListener: () => {} }),
  document: {
    documentElement: { getAttribute: () => 'dark', setAttribute: () => {} },
    addEventListener: () => {},
    getElementById: (id) => makeElem(),
    querySelectorAll: () => [],
    querySelector: () => makeElem(),
    createElement: () => makeElem(),
    body: makeElem()
  },
  localStorage: {
    getItem: (k) => mockLocalStorage[k] || null,
    setItem: (k, v) => { mockLocalStorage[k] = String(v); },
    removeItem: (k) => { delete mockLocalStorage[k]; }
  },
  location: { hash: '#/' },
  navigator: { userAgent: 'NodeTest' },
  console: console,
  setTimeout: setTimeout,
  clearTimeout: clearTimeout,
  setInterval: () => 0,
  clearInterval: () => {},
  Date: Date,
  Math: Math,
  JSON: JSON,
  Array: Array,
  Object: Object,
  Set: Set,
  parseInt: parseInt
};
sandbox.window = sandbox;
vm.createContext(sandbox);

try {
  vm.runInContext(code, sandbox);
} catch (e) {
  console.error('VM Run Error:', e);
}

console.log('Testing Note Spaced Repetition Engine (1/3/7/21/30)...');

const NOTE_SRS_SCHEDULE = sandbox.window.NOTE_SRS_SCHEDULE;
const getNoteSrsInfo = sandbox.window.getNoteSrsInfo;
const registerNoteInitialRead = sandbox.window.registerNoteInitialRead;
const applyNoteReview = sandbox.window.applyNoteReview;
const getNoteSpacedRepetitionStats = sandbox.window.getNoteSpacedRepetitionStats;
const state = sandbox.window.state;

// 1. Проверка графика
assert(NOTE_SRS_SCHEDULE && NOTE_SRS_SCHEDULE.length === 5, 'NOTE_SRS_SCHEDULE must have length 5');
assert.deepStrictEqual(Array.from(NOTE_SRS_SCHEDULE), [1, 3, 7, 21, 30], 'NOTE_SRS_SCHEDULE must be exactly [1, 3, 7, 21, 30]');
console.log('✓ 1. Fixed Schedule 1/3/7/21/30 verified');

// 2. Инициализация конспекта
state.readNotes = ['К-001'];
state.noteSrs = {};

const info1 = getNoteSrsInfo('К-001');
assert(info1 !== null, 'getNoteSrsInfo must return info for read note');
assert.strictEqual(info1.step, 0, 'Initial step must be 0');
assert.strictEqual(info1.interval, 1, 'Initial interval must be 1 day');
assert.strictEqual(info1.nextInterval, 3, 'Next interval must be 3 days');
console.log('✓ 2. Initial read note registration verified (Step 0 -> 1 day)');

// 3. Шаг повторения: 1 -> 3 -> 7 -> 21 -> 30
applyNoteReview('К-001', true);
const info2 = getNoteSrsInfo('К-001');
assert.strictEqual(info2.step, 1, 'After 1st review, step must be 1');
assert.strictEqual(info2.interval, 3, 'After 1st review, interval must be 3 days');
assert.strictEqual(info2.nextInterval, 7, 'Next interval must be 7 days');

applyNoteReview('К-001', true);
const info3 = getNoteSrsInfo('К-001');
assert.strictEqual(info3.step, 2, 'After 2nd review, step must be 2');
assert.strictEqual(info3.interval, 7, 'After 2nd review, interval must be 7 days');
assert.strictEqual(info3.nextInterval, 21, 'Next interval must be 21 days');

applyNoteReview('К-001', true);
const info4 = getNoteSrsInfo('К-001');
assert.strictEqual(info4.step, 3, 'After 3rd review, step must be 3');
assert.strictEqual(info4.interval, 21, 'After 3rd review, interval must be 21 days');
assert.strictEqual(info4.nextInterval, 30, 'Next interval must be 30 days');

applyNoteReview('К-001', true);
const info5 = getNoteSrsInfo('К-001');
assert.strictEqual(info5.step, 4, 'After 4th review, step must be 4');
assert.strictEqual(info5.interval, 30, 'After 4th review, interval must be 30 days');
console.log('✓ 3. Progressive review ladder 1 -> 3 -> 7 -> 21 -> 30 days verified');

// 4. Сброс (Повторить снова)
applyNoteReview('К-001', false);
const infoReset = getNoteSrsInfo('К-001');
assert.strictEqual(infoReset.step, 0, 'After reset, step must return to 0');
assert.strictEqual(infoReset.interval, 1, 'After reset, interval must return to 1 day');
console.log('✓ 4. Review reset (repeat again in 1 day) verified');

// 5. Статистика очереди повторения
state.readNotes = ['К-001', 'К-002'];
state.noteSrs['К-001'].dueDate = '2026-10-20'; // в прошлом -> due today
state.noteSrs['К-002'] = { step: 1, interval: 3, dueDate: '2026-11-20', reviewCount: 1 }; // в будущем

const stats = getNoteSpacedRepetitionStats();
assert.strictEqual(stats.totalRead, 2, 'Total read notes must be 2');
assert.strictEqual(stats.dueCount, 1, 'Due count must be 1');
assert.strictEqual(stats.dueNotes[0].noteId, 'К-001', 'Due note must be К-001');
assert.strictEqual(stats.scheduledCount, 1, 'Scheduled count must be 1');
console.log('✓ 5. Queue statistics and due separation verified');

// 6. Неразрушающее слияние стейта
if(typeof sandbox.window.mergeProgressStates === 'function'){
  const stateA = { noteSrs: { 'К-001': { step: 0, interval: 1, lastReview: '2026-10-25' } } };
  const stateB = { noteSrs: { 'К-001': { step: 2, interval: 7, lastReview: '2026-10-27' }, 'К-002': { step: 1, interval: 3 } } };
  const merged = sandbox.window.mergeProgressStates(stateA, stateB);
  assert.strictEqual(merged.noteSrs['К-001'].step, 2, 'Merged noteSrs must preserve higher step');
  assert.strictEqual(merged.noteSrs['К-002'].step, 1, 'Merged noteSrs must include all notes from both states');
  console.log('✓ 6. Non-destructive state merge for noteSrs verified');
}

console.log('\n========================================================');
console.log('  ALL NOTE SRS TESTS PASSED SUCCESSFULLY (100%)');
console.log('========================================================');
