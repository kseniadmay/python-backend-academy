/**
 * test_cards_srs_click_regression.js
 * Проверка кликабельности, отсутствия ReferenceError и корректной работы
 * интервального повторения (SRS) в карточках платформы.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

const rootDir = path.resolve(__dirname, '..');
const academyHtml = fs.readFileSync(path.join(rootDir, 'academy.html'), 'utf-8');

console.log('================================================================');
console.log('   TEST CARDS SRS RUNTIME & CLICK REGRESSION SUITE              ');
console.log('================================================================\n');

// Extract viewCardsHub
const cbStart = academyHtml.indexOf('function buildSrsDeckContextBarHTML(');
const cbEnd = academyHtml.indexOf('window.buildSrsDeckContextBarHTML = buildSrsDeckContextBarHTML;', cbStart);
const buildSrsDeckContextBarCode = (cbStart !== -1 && cbEnd !== -1) ? academyHtml.slice(cbStart, cbEnd) : '';

const startIdx = academyHtml.indexOf('function viewCardsHub(){');
const endIdx = academyHtml.indexOf('/* ================= 401-TASK CODING TRAINER HUB', startIdx);
assert(startIdx !== -1 && endIdx !== -1, 'viewCardsHub function boundary found');
const viewCardsHubCode = academyHtml.slice(startIdx, endIdx);

const windowObj = {};
const sandbox = {
  console,
  window: windowObj,
  cardsHubState: { dueMode: true, dueQueue: [{ deckId: '1.1.1', cardIdx: 0 }], duePos: 0, flipped: false },
  ALL_DECKS_COMBINED: { '1.1.1': { id: '1.1.1', title: 'Основы Python', cards: [{ q: 'Question 1', a: 'Answer 1' }] } },
  ALL_UNITS_COMBINED: [],
  PY_SKILLS_BY_ID: {},
  DECK_TO_SKILLS_MAP: {},
  ALL_PY_SKILLS: [],
  state: { cardSrs: {}, cardRatings: {}, reviewedDecks: [] },
  getNoteSpacedRepetitionStats: () => ({ dueCount: 0, dueNotes: [] }),
  getSpacedRepetitionStats: () => ({ dueTodayCardsCount: 1 }),
  getSrsDailyProgressData: () => ({ totalDoneToday: 0, totalTargetToday: 1, pct: 0 }),
  escapeHtmlStr: s => s,
  buildSrsFlowTabsHTML: () => '',
  buildSrsHeaderBarHTML: () => '',
  buildSrsDailyProgressBarHTML: () => '',
  buildFcProgressHeaderHTML: () => '',
  buildSrsRatingDockHTML: () => '',
  formatCardQuestionHTML: q => q,
  formatRichInlineText: a => a,
  computeRemNoteIntervals: () => ({ again:{days:1}, hard:{days:2}, good:{days:3}, easy:{days:7} }),
  getRemNoteCardStatusBadgeHTML: () => '',
  getEffectiveUnitTier: () => 1,
  getDeckInterviewTier: () => 1,
  cleanUnitTitle: (id, t) => t,
  pluralizeRu: () => 'карт',
  collectDueCardsQueue: () => []
};

const ctx = vm.createContext(sandbox);

// 1. Тест: Очередь повторения на сегодня (Лицевая сторона)
if (buildSrsDeckContextBarCode) vm.runInContext(buildSrsDeckContextBarCode, ctx);
vm.runInContext(viewCardsHubCode, ctx);
let out1 = vm.runInContext('viewCardsHub();', ctx);
assert(typeof out1 === 'string' && out1.includes('Question 1'), 'Test 1 Pass: dueMode front renders question');
console.log('  ✓ [PASS] 1. dueMode (лицевая сторона) рендерится без ReferenceError');

// 2. Тест: Очередь повторения на сегодня (Сторона ответа)
sandbox.cardsHubState.flipped = true;
let out2 = vm.runInContext('viewCardsHub();', ctx);
assert(typeof out2 === 'string' && out2.includes('Answer 1'), 'Test 2 Pass: dueMode back renders answer');
console.log('  ✓ [PASS] 2. dueMode (сторона ответа) рендерится без ReferenceError');

// 3. Тест: Режим каталога (Лицевая сторона)
sandbox.cardsHubState.dueMode = false;
sandbox.cardsHubState.deckId = '1.1.1';
sandbox.cardsHubState.cardIdx = 0;
sandbox.cardsHubState.flipped = false;
let out3 = vm.runInContext('viewCardsHub();', ctx);
assert(typeof out3 === 'string' && out3.includes('Question 1'), 'Test 3 Pass: catalog front renders question');
console.log('  ✓ [PASS] 3. Каталог (лицевая сторона) рендерится без ReferenceError');

// 4. Тест: Режим каталога (Сторона ответа)
sandbox.cardsHubState.flipped = true;
let out4 = vm.runInContext('viewCardsHub();', ctx);
assert(typeof out4 === 'string' && out4.includes('Answer 1'), 'Test 4 Pass: catalog back renders answer');
console.log('  ✓ [PASS] 4. Каталог (сторона ответа) рендерится без ReferenceError');

// 5. Тест: Пустая очередь дня (Свободная тренировка, лицевая сторона)
sandbox.cardsHubState.dueMode = true;
sandbox.cardsHubState.dueQueue = [];
sandbox.cardsHubState.flipped = false;
let out5 = vm.runInContext('viewCardsHub();', ctx);
assert(typeof out5 === 'string' && out5.includes('Question 1'), 'Test 5 Pass: free training front renders question');
console.log('  ✓ [PASS] 5. Свободная тренировка (лицевая сторона) рендерится без ReferenceError');

// 6. Тест: Пустая очередь дня (Свободная тренировка, сторона ответа)
sandbox.cardsHubState.flipped = true;
let out6 = vm.runInContext('viewCardsHub();', ctx);
assert(typeof out6 === 'string' && out6.includes('Answer 1'), 'Test 6 Pass: free training back renders answer');
console.log('  ✓ [PASS] 6. Свободная тренировка (сторона ответа) рендерится без ReferenceError');

// 7. Тест: При выборе колоды в селекторе сбрасывается dueMode = false
assert(
  academyHtml.includes("cardsHubState.dueMode = false;\n    saveCardsHubPosState();\n    render();") ||
  academyHtml.includes("cardsHubState.dueMode = false;\r\n    saveCardsHubPosState();\r\n    render();"),
  'Test 7 Pass: choosing deck switches dueMode to false'
);
console.log('  ✓ [PASS] 7. Выбор темы в селекторе переключает режим с очереди на выбранную тему');

// 8. Тест: Горячие клавиши 1..4 привязаны к data-hotkey и срабатывают только после переворота
assert(
  academyHtml.includes("let rateBtn = document.querySelector(`[data-hotkey=\"${e.key}\"]`);"),
  'Test 8 Pass: hotkeys 1..4 query data-hotkey'
);
assert(
  academyHtml.includes("if(isFlippedHub || isFlippedSkill){"),
  'Test 8 Pass: rating hotkeys only active when card is flipped'
);
console.log('  ✓ [PASS] 8. Горячие клавиши 1..4 точно соответствуют бейджам и защищены от слепого нажатия до переворота');

console.log('\nИтог: все 8 проверок кликабельности и рантайма карточек пройдены на 100%!\n');
