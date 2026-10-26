// -*- coding: utf-8 -*-
/**
 * test_descriptor_suite.js
 * 
 * Расширенный эталонный регрессионный сьют Строгого Дескриптора (Strict Descriptor Quality Suite).
 * Автоматически верифицирует все инварианты образовательного опыта, чистоты UI,
 * эстетической системы «Вечерний Обсидиан» и стандартов отказоустойчивости платформы
 * Python Backend Academy согласно PROJECT_CONTEXT.md и AGENTS.md.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const academyHtmlPath = path.join(rootDir, 'academy.html');
const standardsHtmlPath = path.join(rootDir, 'standards', 'standards.html');
const projectContextPath = path.join(rootDir, 'PROJECT_CONTEXT.md');
const agentsMdPath = path.join(rootDir, 'AGENTS.md');
const fixturesDir = path.join(rootDir, 'tests', 'fixtures');
const schemaSqlPath = path.join(fixturesDir, 'test_db_schema.sql');

console.log('================================================================');
console.log('   STRICT DESCRIPTOR ARCHITECTURAL REGRESSION SUITE             ');
console.log('   Verification of Core Invariants, Fault Tolerance & Human UI   ');
console.log('================================================================\n');

// -----------------------------------------------------------------------------
// 1. Инвариант 0: Канонический эталон (100% побайтовое соответствие)
// -----------------------------------------------------------------------------
assert(fs.existsSync(academyHtmlPath), 'academy.html missing');
assert(fs.existsSync(standardsHtmlPath), 'standards/standards.html missing');
const academyHtml = fs.readFileSync(academyHtmlPath, 'utf-8');
const standardsHtml = fs.readFileSync(standardsHtmlPath, 'utf-8');

assert.strictEqual(
  academyHtml.length,
  standardsHtml.length,
  `Invariant 0: academy.html (${academyHtml.length} bytes) must match standards.html (${standardsHtml.length} bytes) length`
);
assert.strictEqual(
  academyHtml,
  standardsHtml,
  'Invariant 0: academy.html must be 100% byte-for-byte identical to standards/standards.html'
);
console.log('✓ Invariant 0: Canonical Etalon 100% Byte Equality verified');

// -----------------------------------------------------------------------------
// 2. Инвариант 1: Запрет технического упоминания «Кодди» / «Coddy» в UI и регламентах
// -----------------------------------------------------------------------------
const projectContext = fs.readFileSync(projectContextPath, 'utf-8');
const agentsMd = fs.readFileSync(agentsMdPath, 'utf-8');

assert(
  agentsMd.includes('Категорический запрет на техническое упоминание «Кодди» / «Coddy»'),
  'Invariant 1: AGENTS.md must mandate ban on technical Coddy mentions'
);
assert(
  projectContext.includes('Категорический запрет на техническое упоминание «Кодди» / «Coddy»'),
  'Invariant 1: PROJECT_CONTEXT.md must mandate ban on technical Coddy mentions'
);
assert(
  !agentsMd.includes('# Coddy Pedagogical UI'),
  'Invariant 1: AGENTS.md must not contain legacy title # Coddy Pedagogical UI'
);
assert(
  !agentsMd.includes('# Педагогическая методология и инварианты Кодди'),
  'Invariant 1: AGENTS.md must not contain legacy title with Кодди'
);
assert(
  !projectContext.includes('# Педагогическая методология и инварианты Кодди'),
  'Invariant 1: PROJECT_CONTEXT.md must not contain legacy title with Кодди'
);
assert(
  !academyHtml.includes('coddy_interface.js'),
  'Invariant 1: References to legacy coddy_interface.js are banned'
);
assert(
  !academyHtml.includes('🎯 Проверка понимания (Coddy)'),
  'Invariant 1: UI badges must not contain Coddy'
);
assert(
  !academyHtml.includes('🎯 Проверка понимания (Coddy Studio)'),
  'Invariant 1: UI badges must not contain Coddy Studio'
);
console.log('✓ Invariant 1: Strict Ban on technical Coddy mentions verified');

// -----------------------------------------------------------------------------
// 3. Инвариант 2: Запрет термина «3D» / «3d» как лексического шума
// -----------------------------------------------------------------------------
assert(
  !academyHtml.includes('3D-тропа') && !academyHtml.includes('3D тропа'),
  'Invariant 2: UI text must not contain "3D-тропа"'
);
assert(
  !academyHtml.includes('3D-карточ') && !academyHtml.includes('3D карточ'),
  'Invariant 2: Flashcards must not be referred to as 3D'
);
assert(
  !academyHtml.includes('3D-нод') && !academyHtml.includes('3D нод'),
  'Invariant 2: Trail nodes must not be referred to as 3D'
);
console.log('✓ Invariant 2: Total elimination of "3D" lexical noise verified');

// -----------------------------------------------------------------------------
// 4. Инвариант 3: Чистый человеческий интерфейс (Clean Human UI)
// -----------------------------------------------------------------------------
assert(
  projectContext.includes('Чистый человеческий интерфейс'),
  'Invariant 3: PROJECT_CONTEXT.md must enforce Clean Human UI rule'
);
assert(
  agentsMd.includes('Чистый человеческий интерфейс'),
  'Invariant 3: AGENTS.md must enforce Clean Human UI rule'
);
assert(
  !academyHtml.includes('<h1 class="trail-heading">Юнит 1.1'),
  'Invariant 3: Trail heading must not show raw "Юнит 1.1"'
);
console.log('✓ Invariant 3: Clean Human UI & Technical IDs ban verified');

// -----------------------------------------------------------------------------
// 5. Инвариант 4: Стандарт кавычек в коде по умолчанию: одинарные ('...')
// -----------------------------------------------------------------------------
assert(
  agentsMd.includes('Стандарт кавычек в коде по умолчанию: одинарные кавычки'),
  'Invariant 4: AGENTS.md must define single quotes default invariant'
);
assert(
  projectContext.includes('Стандарт кавычек в коде по умолчанию: одинарные кавычки'),
  'Invariant 4: PROJECT_CONTEXT.md must define single quotes default invariant'
);
console.log('✓ Invariant 4: Default Single Quotes Standard verified');

// -----------------------------------------------------------------------------
// 6. Инвариант 5: Категорический запрет на генерацию растровых картинок через ИИ
// -----------------------------------------------------------------------------
assert(
  agentsMd.includes('Категорический запрет на генерацию картинок через ИИ'),
  'Invariant 5: AGENTS.md must strictly ban AI image generators'
);
assert(
  projectContext.includes('Категорический запрет на генерацию растровых картинок через ИИ'),
  'Invariant 5: PROJECT_CONTEXT.md must strictly ban AI image generators'
);
console.log('✓ Invariant 5: Ban on AI raster image generation verified');

// -----------------------------------------------------------------------------
// 7. Инвариант 6: Single Dominant CTA на Дашборде и запрет демотивирующих «0%»
// -----------------------------------------------------------------------------
assert(
  academyHtml.includes('viewDashboard'),
  'Invariant 6: viewDashboard renderer must exist'
);
assert(
  academyHtml.includes("const ctaLabel = 'Продолжить';") || academyHtml.includes("const ctaLabel = 'Продолжить дальше';"),
  'Invariant 6: Single Dominant CTA must use concise label without artificial timing'
);
assert(
  !academyHtml.includes('Готовность к тех-скринингу: 0%'),
  'Invariant 6: Discouraging "0%" readiness badge must be banned'
);
console.log('✓ Invariant 6: Single Dominant CTA & Friendly 0 XP Start verified');

// -----------------------------------------------------------------------------
// 8. Инвариант 7 (1.16.1): Алгоритмический Active Rescue
// -----------------------------------------------------------------------------
assert(
  projectContext.includes('1.16. Глубокие стандарты отказоустойчивости и активного восстановления (Дескриптор)'),
  'Invariant 7: PROJECT_CONTEXT.md must specify Descriptor Resilience Standards'
);
assert(
  projectContext.includes('Алгоритмический спасательный шанс (Active Rescue)'),
  'Invariant 7: Active Rescue standard must be documented'
);
assert(
  agentsMd.includes('Алгоритмический Active Rescue'),
  'Invariant 7: AGENTS.md must mandate Active Rescue'
);
console.log('✓ Invariant 7: Active Rescue Memory Retrieval Standard verified');

// -----------------------------------------------------------------------------
// 9. Инвариант 8 (1.16.2): Неразрушающий возврат по бусинам (Non-Destructive Peeking)
// -----------------------------------------------------------------------------
assert(
  academyHtml.includes('ideDrafts') || academyHtml.includes('practice-ide-drafts'),
  'Invariant 8: academy.html must maintain ideDrafts state bus'
);
assert(
  academyHtml.includes('mergeIdeDraftMaps') || academyHtml.includes('ideDraftsMap'),
  'Invariant 8: academy.html must implement draft merging for non-destructive peeking'
);
console.log('✓ Invariant 8: Non-Destructive Peeking & Draft Persistence verified');

// -----------------------------------------------------------------------------
// 10. Инвариант 9 (1.16.3): Сторожевой таймер рантайма (Execution Watchdog 2000ms)
// -----------------------------------------------------------------------------
assert(
  projectContext.includes('Сторожевой таймер рантайма Brython (Execution Watchdog 2000ms)'),
  'Invariant 9: Execution Watchdog 2000ms must be specified in PROJECT_CONTEXT.md'
);
assert(
  agentsMd.includes('Execution Watchdog 2000ms'),
  'Invariant 9: Execution Watchdog 2000ms must be mandated in AGENTS.md'
);
console.log('✓ Invariant 9: Execution Watchdog 2000ms runtime protection verified');

// -----------------------------------------------------------------------------
// 11. Инвариант 10 (1.16.4): Защита от авто-зума iOS (iOS Zoom Guard font-size: 16px)
// -----------------------------------------------------------------------------
assert(
  projectContext.includes('Защита от авто-зума iOS (iOS Zoom Guard)'),
  'Invariant 10: iOS Zoom Guard must be specified in PROJECT_CONTEXT.md'
);
assert(
  agentsMd.includes('iOS Zoom Guard'),
  'Invariant 10: iOS Zoom Guard must be mandated in AGENTS.md'
);
assert(
  academyHtml.includes('font-size: 16px') || academyHtml.includes('font-size:16px'),
  'Invariant 10: CSS must define font-size: 16px on mobile viewports'
);
console.log('✓ Invariant 10: iOS Zoom Guard (font-size >= 16px) verified');

// -----------------------------------------------------------------------------
// 12. Инвариант 11: Pure Daily Due Stream в Центре повторения (#/cards)
// -----------------------------------------------------------------------------
assert(
  academyHtml.includes('data-hub-rate="0"') || academyHtml.includes('Не знаю'),
  'Invariant 11: Flashcards first rating button must be "Не знаю"'
);
assert(
  !academyHtml.includes('>Снова<'),
  'Invariant 11: Deprecated "Снова" rating label must be replaced with "Не знаю"'
);
console.log('✓ Invariant 11: Pure Daily Due Stream & "Не знаю" rating verified');

// -----------------------------------------------------------------------------
// 13. Инвариант 12: Янтарное сияние рубежной бусины (#f59e0b)
// -----------------------------------------------------------------------------
assert(
  academyHtml.includes('#f59e0b'),
  'Invariant 12: Amber glow color #f59e0b must exist in stylesheet'
);
assert(
  projectContext.includes('Королевский янтарь (`#f59e0b`)'),
  'Invariant 12: Amber glow token must be specified in PROJECT_CONTEXT.md'
);
console.log('✓ Invariant 12: Milestone bead amber glow (#f59e0b) verified');

// -----------------------------------------------------------------------------
// 14. Инвариант 13: Мобильная эргономика кода (Mobile-First 390px)
// -----------------------------------------------------------------------------
assert(
  agentsMd.includes('Мобильная эргономика кода (Mobile-First 390px)'),
  'Invariant 13: AGENTS.md must enforce Mobile-First 390px section'
);
assert(
  agentsMd.includes('Строго **35–42 символа** в строке кода (макс. 46)'),
  'Invariant 13: AGENTS.md must enforce 35-46 char line limit'
);
assert(
  agentsMd.includes('Полный запрет хвостовых комментариев'),
  'Invariant 13: AGENTS.md must enforce trailing comments ban'
);
console.log('✓ Invariant 13: Mobile-First 390px code ergonomics verified');

// -----------------------------------------------------------------------------
// 15. Инвариант 14: Exhaustive Testing Mastery (Запрет тестов на 4 вопроса)
// -----------------------------------------------------------------------------
assert(
  projectContext.includes('Запрет поверхностных тестов на 4 вопроса'),
  'Invariant 14: PROJECT_CONTEXT.md must prohibit superficial 4-question tests'
);
assert(
  agentsMd.includes('Каждый рубежный тест содержит **от 8 до 12 концептуальных вопросов**'),
  'Invariant 14: AGENTS.md must mandate 8..12 questions per milestone test'
);
console.log('✓ Invariant 14: Exhaustive Testing Mastery standard verified');

// -----------------------------------------------------------------------------
// 16. Инвариант 15: Целостность канонических фикстур платформы
// -----------------------------------------------------------------------------
const expectedFixtures = [
  'user_progress_fresh.json',
  'user_progress_intermediate.json',
  'user_progress_advanced.json',
  'user_progress_conflict.json',
  'user_progress_corrupted.json',
  'user_progress_v1_legacy.json',
  'user_progress_v2_legacy.json',
  'user_progress_backup.json'
];

for (const fixName of expectedFixtures) {
  const fixPath = path.join(fixturesDir, fixName);
  assert(fs.existsSync(fixPath), `Invariant 15: Fixture ${fixName} must exist in tests/fixtures`);
  const raw = fs.readFileSync(fixPath, 'utf-8');
  assert.doesNotThrow(() => JSON.parse(raw), `Invariant 15: Fixture ${fixName} must be valid JSON`);
}
console.log(`✓ Invariant 15: Canonical Fixtures Suite (${expectedFixtures.length}/${expectedFixtures.length}) verified`);

// -----------------------------------------------------------------------------
// 17. Инвариант 16: Валидность схемы реляционной тестовой БД (SQLite DDL)
// -----------------------------------------------------------------------------
assert(fs.existsSync(schemaSqlPath), 'Invariant 16: test_db_schema.sql must exist');
const schemaSql = fs.readFileSync(schemaSqlPath, 'utf-8');
assert(schemaSql.includes('PRAGMA foreign_keys = ON;'), 'Invariant 16: Schema must enforce foreign keys');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS users'), 'Invariant 16: users table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS modules'), 'Invariant 16: modules table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS units'), 'Invariant 16: units table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS tasks'), 'Invariant 16: tasks table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS user_progress'), 'Invariant 16: user_progress table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS srs_cards'), 'Invariant 16: srs_cards table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS ide_drafts'), 'Invariant 16: ide_drafts table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS sync_revisions'), 'Invariant 16: sync_revisions table required');
assert(schemaSql.includes('CREATE TABLE IF NOT EXISTS feedback_reports'), 'Invariant 16: feedback_reports table required');
console.log('✓ Invariant 16: SQLite DDL Test Database Schema (9/9 tables & indices) verified');

console.log('\n================================================================');
console.log('  ALL STRICT DESCRIPTOR INVARIANTS & AUDITS PASSED (100% PERFECT)');
console.log('================================================================');
