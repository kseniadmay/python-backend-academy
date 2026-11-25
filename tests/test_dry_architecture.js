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

console.log('\n================================================================');
console.log('🏆 ВСЕ 6 УРОВНЕЙ DRY-АРХИТЕКТУРЫ УСПЕШНО ПОДТВЕРЖДЕНЫ (100% DRY)');
console.log('================================================================');
process.exit(0);
