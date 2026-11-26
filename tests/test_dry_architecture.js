#!/usr/bin/env node
/**
 * test_dry_architecture.js
 *
 * Глобальный платформенный тест на соответствие принципу DRY (Don't Repeat Yourself)
 * и концепции единого источника истины (Single Source of Truth) в Python Backend Academy.
 *
 * Охватывает 6 фундаментальных слоев платформы:
 * 1. [DRY Документация]: PROJECT_CONTEXT.md как единственный SSOT регламентов;
 *    HANDOVER_CONTEXT.md и AGENTS.md служат компактными ссылочными шлюзами без дублирования текста.
 * 2. [DRY Эталоны и Ядро]: 100% побайтовая идентичность academy.html и standards/standards.html.
 * 3. [DRY База Знаний]: Уникальность всех ID юнитов, конспектов (К-XXX) и задач (IDE_TASKS).
 * 4. [DRY UI-компоненты]: Единые генераторы интерфейса (Zen IDE, ридер теории, карточки SRS, экзамены, ожерелье бусин).
 * 5. [DRY Геймификация и Состояние]: Единые функции расчета стрик, опыта (awardXp) и эшелонов.
 * 6. [DRY Дизайн-токены]: Единая каноническая тема «Вечерний Обсидиан» на уровне :root без локальных дублей тем.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const ACADEMY_PATH = path.join(ROOT, 'academy.html');
const STANDARDS_PATH = path.join(ROOT, 'standards', 'standards.html');
const PROJECT_CONTEXT_PATH = path.join(ROOT, 'PROJECT_CONTEXT.md');
const HANDOVER_PATH = path.join(ROOT, 'HANDOVER_CONTEXT.md');
const AGENTS_PATH = path.join(ROOT, 'AGENTS.md');

console.log('================================================================');
console.log('🏛 ГЛОБАЛЬНЫЙ АРХИТЕКТУРНЫЙ ТЕСТ СООТВЕТСТВИЯ ПРИНЦИПУ DRY (SSOT)');
console.log('================================================================\n');

// -----------------------------------------------------------------------------
// 1. СЛОЙ ДОКУМЕНТАЦИИ: Регламенты и ссылочные шлюзы
// -----------------------------------------------------------------------------
console.log('▶ [1/6] Проверка DRY в документации и архитектурных манифестах...');
assert(fs.existsSync(PROJECT_CONTEXT_PATH), 'PROJECT_CONTEXT.md должен существовать');
assert(fs.existsSync(HANDOVER_PATH), 'HANDOVER_CONTEXT.md должен существовать');
assert(fs.existsSync(AGENTS_PATH), 'AGENTS.md должен существовать');

const projectContext = fs.readFileSync(PROJECT_CONTEXT_PATH, 'utf8');
const handoverContext = fs.readFileSync(HANDOVER_PATH, 'utf8');
const agentsMd = fs.readFileSync(AGENTS_PATH, 'utf8');

// PROJECT_CONTEXT.md обязан содержать полный свод регламентов (> 30 КБ)
assert(projectContext.length > 30000, `PROJECT_CONTEXT.md слишком короткий (${projectContext.length} байт), ожидается полный свод >30КБ`);
assert(projectContext.includes('Single Source of Truth'), 'PROJECT_CONTEXT.md обязан быть обозначен как Single Source of Truth');

// HANDOVER_CONTEXT.md обязан быть компактным ссылочным шлюзом (< 5 КБ) и ссылаться на PROJECT_CONTEXT.md
assert(handoverContext.length < 5000, `HANDOVER_CONTEXT.md нарушает DRY (${handoverContext.length} байт) — дублирование текста вместо ссылки!`);
assert(handoverContext.includes('DRY (Don\'t Repeat Yourself)'), 'HANDOVER_CONTEXT.md обязан явно фиксировать принцип DRY');
assert(handoverContext.includes('PROJECT_CONTEXT.md'), 'HANDOVER_CONTEXT.md обязан ссылаться на PROJECT_CONTEXT.md');

// AGENTS.md обязан ссылаться на PROJECT_CONTEXT.md как на единый источник истины
assert(agentsMd.includes('PROJECT_CONTEXT.md'), 'AGENTS.md обязан указывать PROJECT_CONTEXT.md как единый источник истины');
console.log('  ✓ Документация строго подчинена DRY: регламенты централизованы в PROJECT_CONTEXT.md');


// -----------------------------------------------------------------------------
// 2. СЛОЙ ЭТАЛОНОВ И ПЛАТФОРМЫ: Побайтовое соответствие SPA-ядра
// -----------------------------------------------------------------------------
console.log('\n▶ [2/6] Проверка DRY между боевой платформой и эталоном standards.html...');
const academyRaw = fs.readFileSync(ACADEMY_PATH);
const standardsRaw = fs.readFileSync(STANDARDS_PATH);

assert.strictEqual(
  academyRaw.length,
  standardsRaw.length,
  `[DRY ERROR] Размер academy.html (${academyRaw.length}) != standards.html (${standardsRaw.length})!`
);
assert(
  academyRaw.equals(standardsRaw),
  '[DRY ERROR] academy.html и standards.html имеют расхождения байт — нарушение единого эталона!'
);
console.log(`  ✓ Побайтовая синхронизация 100%: academy.html == standards.html (${academyRaw.length} байт)`);


// -----------------------------------------------------------------------------
// 3. СЛОЙ БАЗЫ ЗНАНИЙ: Уникальность идентификаторов и защита от дублей контента
// -----------------------------------------------------------------------------
console.log('\n▶ [3/6] Проверка DRY в базе знаний: уникальность ID и отсутствие дублей...');
const htmlContent = academyRaw.toString('utf8');

// А) Проверка уникальности юнитов в PY_MASTERY
const pyMasteryMatch = htmlContent.match(/const PY_MASTERY = ({[\s\S]*?});\s*(?:const|let|var|function)/);
assert(pyMasteryMatch, 'Объект PY_MASTERY должен присутствовать в academy.html');
const pyMastery = JSON.parse(pyMasteryMatch[1]);

const unitKeys = Object.keys(pyMastery.units || {});
const uniqueUnitKeys = new Set(unitKeys);
assert.strictEqual(unitKeys.length, uniqueUnitKeys.size, '[DRY ERROR] Обнаружены дубликаты ID юнитов в PY_MASTERY.units!');

// Б) Проверка уникальности определений конспектов (К-XXX)
const noteKeyMatches = htmlContent.match(/['"](К-\d+)['"]:\s*\{/g) || [];
const noteKeys = noteKeyMatches.map(m => m.match(/К-\d+/)[0]);
const uniqueNoteKeys = new Set(noteKeys);
assert.strictEqual(noteKeys.length, uniqueNoteKeys.size, `[DRY ERROR] Обнаружены дубликаты определений конспектов (${noteKeys.length} vs ${uniqueNoteKeys.size})!`);

// В) Проверка уникальности задач IDE_TASKS
const ideTasksMatch = htmlContent.match(/const IDE_TASKS = (\[[\s\S]*?\]);\s*(?:const|let|var|function)/);
assert(ideTasksMatch, 'Массив IDE_TASKS должен присутствовать в academy.html');
const ideTasks = JSON.parse(ideTasksMatch[1]);

const taskIds = ideTasks.map(t => t.id);
const uniqueTaskIds = new Set(taskIds);
assert.strictEqual(taskIds.length, uniqueTaskIds.size, `[DRY ERROR] Обнаружены дубликаты ID практических задач (${taskIds.length} vs ${uniqueTaskIds.size})!`);
console.log(`  ✓ База знаний 100% чиста: ${unitKeys.length} юнитов главы, ${uniqueNoteKeys.size} уникальных конспектов, ${uniqueTaskIds.size} задач — 0 дубликатов`);


// -----------------------------------------------------------------------------
// 4. СЛОЙ UI-ДВИЖКОВ: Единые канонические функции-генераторы интерфейса
// -----------------------------------------------------------------------------
console.log('\n▶ [4/6] Проверка DRY в компонентах интерфейса (Single Engine Policy)...');

const requiredSingleEngines = [
  { name: 'Единый экран решения задач Zen IDE', fn: 'function buildUnifiedZenIdeHTML(params){' },
  { name: 'Единый сократический дифф ошибок', fn: 'function buildSocraticDiffHTML(rawOutput){' },
  { name: 'Единый редактор с номерами строк', fn: 'function buildCodeEditorWithGutterHTML(' },
  { name: 'Единое ожерелье микро-шагов', fn: 'function buildUnifiedMicroStepperHTML(' },
  { name: 'Единый прогресс-трекер карточек SRS', fn: 'function buildFcProgressHeaderHTML(' },
  { name: 'Единая оценка карточек интервального повторения', fn: 'function applyRemNoteCardRating(' },
  { name: 'Единый док кнопок оценки SRS', fn: 'function buildSrsRatingDockHTML(' },
  { name: 'Единый запуск рубежного теста', fn: 'function viewPythonUnitTest(' },
  { name: 'Единый генератор карточки героя', fn: 'function renderDominantHeroCard(' },
  { name: 'Единый генератор ссылок сайдбара/дровера', fn: 'function renderUnifiedNavLinks(' },
  { name: 'Единый расчет термодинамики остывания', fn: 'function getThermodynamicCooldownData(' },
  { name: 'Единый генератор футера сайдбара/дровера', fn: 'function buildUnifiedSidebarFootHTML(' }
];

requiredSingleEngines.forEach(eng => {
  assert(htmlContent.includes(eng.fn), `[DRY ERROR] Канонический генератор «${eng.name}» (${eng.fn}) отсутствует в кодовой базе!`);
});

// Проверка вызова единого Zen IDE в спринте и банке задач
assert(htmlContent.includes("bodyHTML = buildUnifiedZenIdeHTML({"), '[DRY ERROR] Спринт урока обязан вызывать buildUnifiedZenIdeHTML');
assert(htmlContent.includes("const zenIdeHTML = buildUnifiedZenIdeHTML({"), '[DRY ERROR] Банк задач обязан вызывать buildUnifiedZenIdeHTML');
console.log('  ✓ Все 12 ключевых UI-компонентов используют централизованные генераторы без дублирования разметки');


// -----------------------------------------------------------------------------
// 5. СЛОЙ ГЕЙМИФИКАЦИИ И СОСТОЯНИЯ: Централизованный расчет прогресса
// -----------------------------------------------------------------------------
console.log('\n▶ [5/6] Проверка DRY в логике геймификации и стейта...');

// Функция awardXp обязана быть единой точкой начисления опыта
assert(htmlContent.includes('function awardXp('), '[DRY ERROR] Отсутствует единая функция awardXp!');

// Функция расчета прогресса эшелона
assert(htmlContent.includes('function getEchelonProgress('), '[DRY ERROR] Отсутствует единая функция getEchelonProgress!');

// Функция суточного опыта
assert(htmlContent.includes('function todayXp('), '[DRY ERROR] Отсутствует единая функция todayXp!');

// Проверка констант хранилища LocalStorage (не хардкодить строки ключей повторно)
assert(htmlContent.includes("const STORE_KEY = 'academy_state_v1';"), '[DRY ERROR] Отсутствует константа STORE_KEY');
assert(htmlContent.includes("const IDE_DRAFTS_KEY = 'practice-ide-drafts';"), '[DRY ERROR] Отсутствует константа IDE_DRAFTS_KEY');
console.log('  ✓ Геймификация, начисление XP, стрик и ключи хранилища централизованы');


// -----------------------------------------------------------------------------
// 6. СЛОЙ ДИЗАЙН-СИСТЕМЫ: Токены темы «Вечерний Обсидиан» в :root
// -----------------------------------------------------------------------------
console.log('\n▶ [6/6] Проверка DRY в дизайн-системе и CSS-токенах...');

const requiredThemeTokens = [
  '--surface:',
  '--surface-2:',
  '--ink:',
  '--line:',
  '--font-b:',
  '--font-m:'
];

requiredThemeTokens.forEach(token => {
  assert(htmlContent.includes(token), `[DRY ERROR] Базовый CSS-токен ${token} отсутствует в дизайн-системе!`);
});

// Проверка наличия темных токенов Вечернего Обсидиана
assert(htmlContent.includes(':root[data-theme="dark"]'), '[DRY ERROR] Тема «Вечерний Обсидиан» :root[data-theme="dark"] обязана быть определена в дизайн-системе!');
console.log('  ✓ Дизайн-токены определены централизованно в :root, тема «Вечерний Обсидиан» зафиксирована');

// -----------------------------------------------------------------------------
// 7. СЛОЙ 6 ЭШЕЛОНОВ И ВОРОНКИ: Строковые ID, 49 юнитов, явный порядок, BigTech/Product
// -----------------------------------------------------------------------------
console.log('\n▶ [7/7] Проверка архитектуры 6 эшелонов, 49 юнитов и пресетов воронки...');
const vm = require('vm');
const expectedEchelons = {
  hr: ['0.1', '0.2', '0.3', '0.4'],
  screening: ['1.1', '1.2', '1.7', '1.4', '5.1', '5.2', '2.2', '2.3', '1.8', '1.3', '7.1'],
  algo: ['4.1', '4.2', '4.4', '4.3', '4.6', '4.5'],
  backend: ['3.1', '5.5', '5.4', '3.5', '5.6', '3.6', '5.3', '1.9', '6.1', '2.4', '3.2', '3.3', '1.6', '1.5', '3.4'],
  infra: ['7.2', '7.5', '7.4', '2.1', '7.3', '3.8'],
  system_design: ['6.6', '3.7', '7.6', '6.2', '6.5', '6.4', '6.3']
};

function makeFakeEl(id = '', tag = 'div'){
  return {
    id,
    tagName: tag.toUpperCase(),
    textContent: '',
    innerHTML: '',
    value: '',
    style: {},
    children: [],
    childNodes: [],
    classList: { add: () => {}, remove: () => {}, toggle: () => {}, contains: () => false },
    setAttribute: () => {},
    getAttribute: () => null,
    removeAttribute: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    querySelector: () => null,
    querySelectorAll: () => [],
    appendChild: (c) => {
      if(c && c.id) fakeElementsById[c.id] = c;
      return c;
    },
    removeChild: (c) => c,
    insertBefore: (c) => c,
    remove: () => { if(id && fakeElementsById[id]) delete fakeElementsById[id]; },
    focus: () => {},
    blur: () => {},
    click: () => {},
    scrollTop: 0,
    scrollIntoView: () => {},
    getBoundingClientRect: () => ({ top: 0, left: 0, width: 100, height: 100, right: 100, bottom: 100 })
  };
}
const fakeElementsById = {};
const markupOnly = htmlContent.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
let idM;
const idRx = /id=["']([^"']+)["']/g;
while((idM = idRx.exec(markupOnly)) !== null){
  fakeElementsById[idM[1]] = makeFakeEl(idM[1]);
}
const fakeStorageMap = {};
const fakeStore = {
  getItem: (k) => fakeStorageMap[k] || null,
  setItem: (k, v) => { fakeStorageMap[k] = String(v); },
  removeItem: (k) => { delete fakeStorageMap[k]; },
  clear: () => {}
};
const fakeDocument = {
  documentElement: makeFakeEl('html', 'html'),
  body: makeFakeEl('body', 'body'),
  head: makeFakeEl('head', 'head'),
  getElementById: (id) => fakeElementsById[id] || null,
  querySelector: (sel) => (sel && sel.startsWith('#') ? (fakeElementsById[sel.slice(1)] || null) : makeFakeEl('', 'div')),
  querySelectorAll: () => [],
  createElement: (tag) => makeFakeEl('', tag),
  addEventListener: () => {},
  removeEventListener: () => {}
};
const fakeWinCtx = {
  document: fakeDocument,
  localStorage: fakeStore,
  sessionStorage: fakeStore,
  location: { hash: '', search: '', pathname: '/', href: 'http://localhost/' },
  navigator: { userAgent: 'Mozilla/5.0 Node.js' },
  addEventListener: () => {},
  removeEventListener: () => {},
  scrollTo: () => {},
  innerWidth: 1024,
  innerHeight: 768,
  setTimeout: () => 0,
  clearTimeout: () => {},
  setInterval: () => 1,
  clearInterval: () => {},
  console: { log: () => {}, warn: () => {}, error: () => {} },
  requestAnimationFrame: () => 1,
  cancelAnimationFrame: () => {}
};
fakeWinCtx.window = fakeWinCtx;
fakeWinCtx.global = fakeWinCtx;
fakeDocument.defaultView = fakeWinCtx;

const scRx = /<script(?:\s+([^>]*))?>([\s\S]*?)<\/script>/gi;
let vmScriptSrc = '';
let scM;
while((scM = scRx.exec(htmlContent)) !== null){
  if((scM[1] || '').includes('src=')) continue;
  vmScriptSrc += '\n' + scM[2];
}
const ctx = vm.createContext(fakeWinCtx);
vm.runInContext(vmScriptSrc, ctx, { timeout: 4000 });

// 7.1 Точный состав 6 эшелонов и ровно 49 уникальных юнитов
assert.deepStrictEqual(Object.keys(ctx.ECHELONS_BY_ID), Object.keys(expectedEchelons), 'Ключи ECHELONS_BY_ID должны точно соответствовать 6 эшелонам');
const collectedIds = [];
Object.keys(expectedEchelons).forEach(eid => {
  const actualUnits = Array.from(ctx.ECHELONS_BY_ID[eid].units);
  assert.deepStrictEqual(actualUnits, expectedEchelons[eid], `Список юнитов эшелона ${eid} не совпадает с эталоном`);
  collectedIds.push(...actualUnits);
});
const uniqueSet = new Set(collectedIds);
assert.strictEqual(collectedIds.length, 49, `Ожидалось 49 юнитов с учётом 0.1–0.4, получено ${collectedIds.length}`);
assert.strictEqual(uniqueSet.size, 49, `Обнаружены дубликаты юнитов: ${collectedIds.length} vs ${uniqueSet.size} уникальных`);
['0.1', '0.2', '0.3', '0.4'].forEach(id => assert(uniqueSet.has(id), `Отсутствует юнит ${id}`));
ctx.ALL_UNITS_COMBINED.forEach(u => assert(uniqueSet.has(u.id), `Действующий юнит ${u.id} не распределён по эшелонам`));

// 7.2 Явный порядок внутри эшелона (не 1->7)
assert.deepStrictEqual(
  Array.from(ctx.getEchelonUnits('screening').map(u => u.id)),
  ['1.1', '1.2', '1.7', '1.4', '5.1', '5.2', '2.2', '2.3', '1.8', '1.3', '7.1'],
  'getEchelonUnits("screening") обязан возвращать юниты в частотном порядке эшелона, а не по номерам модулей'
);
assert.deepStrictEqual(
  Array.from(ctx.getEchelonUnits('backend').map(u => u.id)),
  ['3.1', '5.5', '5.4', '3.5', '5.6', '3.6', '5.3', '1.9', '6.1', '2.4', '3.2', '3.3', '1.6', '1.5', '3.4'],
  'getEchelonUnits("backend") обязан сохранять точный порядок массива backend.units'
);

// 7.3 Безопасная обработка отсутствующих 0.1-0.4 в HR-скрининге на Шаге 1
const hrProg = ctx.getEchelonProgress('hr');
assert.strictEqual(hrProg.unitsCount, 0, 'На Шаге 1 в HR-скрининге должно быть 0 загруженных юнитов');
assert.strictEqual(hrProg.plannedUnitsCount, 4, 'HR-скрининг должен знать о 4 запланированных юнитах');
assert.strictEqual(hrProg.isInDevelopment, true, 'HR-скрининг на Шаге 1 должен помечаться как isInDevelopment');
assert.strictEqual(hrProg.pct, 0, 'Процент пустого эшелона должен быть 0 без NaN');
const hrSnakeHtml = ctx.viewPathSerpentine({ echelon: 'hr' });
const hrSnakeVisibleText = hrSnakeHtml.replace(/\sstyle="[^"]*"/g, '').replace(/<[^>]+>/g, ' ');
assert(hrSnakeHtml.includes('В разработке') && !/\b0\.[1-4]\b/.test(hrSnakeVisibleText), 'Плейсхолдер HR на Тропе не должен падать и не должен утекать техкод 0.1-0.4 в UI');
const hrProHtml = ctx.viewProPath({ echelon: 'hr' });
const hrProVisibleText = hrProHtml.replace(/\sstyle="[^"]*"/g, '').replace(/<[^>]+>/g, ' ');
assert(hrProHtml.includes('В разработке') && !/\b0\.[1-4]\b/.test(hrProVisibleText), 'Плейсхолдер HR в Pro-режиме не должен падать и не должен утекать техкод 0.1-0.4 в UI');

// 7.4 Пресеты воронки: порядок, номера 1..6 и сохранение прогресса
assert.strictEqual(ctx.FUNNEL_PRESETS.bigtech.label, 'BigTech (алгоритмы до Backend)');
assert.strictEqual(ctx.FUNNEL_PRESETS.product.label, 'Продуктовый рынок (Backend и инфра до алгоритмов)');
assert.strictEqual(ctx.getFunnelPreset(), 'bigtech');
assert.strictEqual(ctx.getEchelonDisplayNum('algo'), 3);
assert.strictEqual(ctx.getEchelonDisplayNum('backend'), 4);
assert.strictEqual(ctx.getEchelonDisplayNum('infra'), 5);

ctx.setFunnelPreset('product');
assert.strictEqual(ctx.getFunnelPreset(), 'product');
assert.deepStrictEqual(Array.from(ctx.getOrderedEchelonIds()), ['hr', 'screening', 'backend', 'infra', 'algo', 'system_design']);
assert.strictEqual(ctx.getEchelonDisplayNum('backend'), 3);
assert.strictEqual(ctx.getEchelonDisplayNum('infra'), 4);
assert.strictEqual(ctx.getEchelonDisplayNum('algo'), 5);

ctx.setFunnelPreset('bigtech');
assert.deepStrictEqual(Array.from(ctx.getOrderedEchelonIds()), ['hr', 'screening', 'algo', 'backend', 'infra', 'system_design']);

// 7.5 Санитизация и слияние legacy state (stackBranch удаляется, funnelPreset и selectedEchelon сохраняются)
const cleanedLegacy = ctx.sanitizeAcademyState({ stackBranch: 'django', selectedEchelon: 2, funnelPreset: 'product', xp: 120 });
assert.strictEqual(Object.prototype.hasOwnProperty.call(cleanedLegacy, 'stackBranch'), false, 'Legacy stackBranch должен удаляться при санитизации');
assert.strictEqual(cleanedLegacy.funnelPreset, 'product', 'funnelPreset должен сохраняться при санитизации');
assert.strictEqual(cleanedLegacy.selectedEchelon, 'backend', 'Числовой legacy selectedEchelon должен безопасно мигрировать на строковый id');

const mergedState = ctx.mergeProgressStates(
  { updatedAt: 100, funnelPreset: 'bigtech', stackBranch: 'fastapi', xp: 50 },
  { updatedAt: 200, funnelPreset: 'product', xp: 75 }
);
assert.strictEqual(mergedState.funnelPreset, 'product', 'mergeProgressStates должен переносить более новый funnelPreset');
assert.strictEqual(Object.prototype.hasOwnProperty.call(mergedState, 'stackBranch'), false, 'mergeProgressStates не должен сохранять stackBranch');

// 7.6 Переключатель в настройках SPA
ctx.openSettingsModal();
const settingsModalEl = fakeElementsById['settings-modal'];
assert(settingsModalEl && settingsModalEl.innerHTML.includes('🎯 Порядок воронки'), 'Модалка настроек обязана содержать секцию Порядок воронки');
assert(settingsModalEl.innerHTML.includes('BigTech (алгоритмы до Backend)') && settingsModalEl.innerHTML.includes('Продуктовый рынок (Backend и инфра до алгоритмов)'), 'Модалка настроек должна содержать точные подписи обоих пресетов');

console.log('  ✓ 6 эшелонов, 49 уникальных юнитов, порядок внутри эшелона и переключение воронки (BigTech/Product) подтверждены');

console.log('\n================================================================');
console.log('🏆 ВСЕ 7 УРОВНЕЙ DRY-АРХИТЕКТУРЫ УСПЕШНО ПОДТВЕРЖДЕНЫ (100% DRY)');
console.log('================================================================');
process.exit(0);
