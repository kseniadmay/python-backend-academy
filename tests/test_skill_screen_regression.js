/**
 * test_skill_screen_regression.js
 * Тотальный регрессионный сьют проверок экрана навыка (viewPythonSkill, #/python/skill/*).
 * Проверяет соответствие каноническим инвариантам AGENTS.md, workspace-rule.md и эталонам платформы.
 * Охватывает Баги 121..127 (7 системных дефектов и инвариантов архитектуры).
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const academyPath = path.join(rootDir, 'academy.html');

console.log('================================================================');
console.log('   SKILL SCREEN VISUAL & PEDAGOGICAL REGRESSION SUITE           ');
console.log('   BUGS 121..127 VERIFICATION (CANONICAL BENCHMARK)             ');
console.log('================================================================\n');

assert(fs.existsSync(academyPath), `academy.html missing at ${academyPath}`);
const academyHtml = fs.readFileSync(academyPath, 'utf-8');

// 1. Bug 121 (Defect 1): Полный запрет технического упоминания «Coddy» в классах и разметке сплит-режима практики
function testBug121_NoCoddyMentionInSkillLayout(){
  assert(
    !academyHtml.includes('practice-coddy-split'),
    'Bug 121: Class "practice-coddy-split" violates strict ban on technical Coddy mentions in AGENTS.md. Must be replaced with "practice-atomic-split"'
  );
  assert(
    academyHtml.includes('practice-atomic-split'),
    'Bug 121: .practice-atomic-split must be defined and used for split practice view'
  );
  console.log('✓ Bug 121: Strict ban on technical Coddy mentions in skill practice layout verified');
}

// 2. Bug 122 (Defect 2): Устранение деформации и аномального горизонтального растягивания плашки опыта .xp-float-particle
function testBug122_XpFloatParticleNoStretch(){
  const cssMatch = academyHtml.slice(
    academyHtml.indexOf('.xp-float-particle{'),
    academyHtml.indexOf('@keyframes float-up-fade')
  );
  assert(
    cssMatch.includes('right:auto') || cssMatch.includes('width:max-content') || cssMatch.includes('white-space:nowrap'),
    'Bug 122: .xp-float-particle must not have fixed right:24px conflicting with inline left positioning'
  );
  console.log('✓ Bug 122: Anti-stretching invariant for .xp-float-particle floating XP pill verified');
}

// 3. Bug 123 (Defect 3): Прямой переход от конспекта к тематическим карточкам (Direct Note-to-Cards Pipeline)
function testBug123_DirectNoteToCardsTransition(){
  const pfnMatch = academyHtml.slice(
    academyHtml.indexOf("const pfn = e.target.closest('[data-py-finish-note]');"),
    academyHtml.indexOf('// (Comprehension check handlers completely removed')
  );
  assert(
    pfnMatch.includes("pySkillViewState.tab = 'cards';"),
    'Bug 123: data-py-finish-note must switch pySkillViewState.tab to "cards" directly'
  );
  assert(
    pfnMatch.includes('pySkillViewState.sessionFid = null;'),
    'Bug 123: data-py-finish-note must reset sessionFid to start thematic deck at card 1'
  );
  console.log('✓ Bug 123: Direct note-to-cards pedagogical pipeline verified');
}

// 4. Bug 124 (Defect 4): Single Dominant CTA на финише конспекта для перехода к карточкам
function testBug124_SingleDominantCtaToCards(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );
  assert(
    vsSkillMatch.includes('Закрепить в карточках (+10 XP) ➔') &&
    vsSkillMatch.includes('data-py-finish-note="${activeK}"'),
    'Bug 124: At the final step of theory, Single Dominant CTA must say "Закрепить в карточках (+10 XP) ➔"'
  );
  assert(
    !vsSkillMatch.includes('data-py-start-check'),
    'Bug 124: Outdated comprehension check CTA data-py-start-check must be eliminated'
  );
  console.log('✓ Bug 124: Single dominant CTA to thematic flashcards verified');
}

// 5. Bug 125 (Defect 5): Ликвидация технического кода юнита «Урок 1.1» в рубежном зачёте и тултипе нити точек
function testBug125_CleanHumanExamMilestoneTitle(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );
  assert(
    !vsSkillMatch.includes('title="Рубежный зачёт урока ${sk.unitId}"'),
    'Bug 125: examDot title must not output technical unit ID like "Урок 1.1", must use clean topic title "Рубежный зачёт: ${cleanUnitTitleVal}"'
  );
  assert(
    !vsSkillMatch.includes("activeItemTitle = 'Рубежный зачёт урока ' + sk.unitId;"),
    'Bug 125: activeItemTitle for exam tab must not output technical unit ID like "Урок 1.1"'
  );
  assert(
    vsSkillMatch.includes('title="Рубежный зачёт: ${escapeHtmlStr(cleanUnitTitleVal)}"'),
    'Bug 125: examDot title must output clean human title'
  );
  console.log('✓ Bug 125: Clean human milestone title and zero technical unit ID leak in dots necklace verified');
}

// 6. Bug 126 (Defect 6): Ликвидация чипсов-спойлеров со 100% готовым кодом задачи в режиме практики
function testBug126_NoSolutionSpoilerQuickTokens(){
  const btsMatch = academyHtml.slice(
    academyHtml.indexOf('function buildTaskSpecDetails('),
    academyHtml.indexOf('function viewPythonSkill(')
  );
  assert(
    !btsMatch.includes("if(sol.includes('original[::-1]')) tokens.push('original[::-1]');"),
    'Bug 126: buildTaskSpecDetails must not push compound solution expressions like "original[::-1]" as quickTokens. Only atomic syntax tokens are permitted'
  );
  assert(
    !btsMatch.includes("if(sol.includes('reversed_list')) tokens.push('reversed_list');"),
    'Bug 126: buildTaskSpecDetails must not push target variable names like "reversed_list" as quickTokens'
  );
  console.log('✓ Bug 126: Pedagogical atomic quick tokens invariant (zero solution spoiler chips) verified');
}

// 7. Bug 127 (Defect 7): Полное упразднение проверок понимания в пользу тематических карточек и SRS
function testBug127_ComprehensionChecksEliminated(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );
  assert(
    !vsSkillMatch.includes('stepCheckHTML'),
    'Bug 127: stepCheckHTML must be completely removed from viewPythonSkill'
  );
  assert(
    !vsSkillMatch.includes('data-py-step-answer'),
    'Bug 127: data-py-step-answer must be completely removed from viewPythonSkill'
  );
  console.log('✓ Bug 127: Complete elimination of comprehension check quizzes in favor of thematic flashcards and SRS verified');
}

// Экспорт и запуск всех тестов
function runAllSkillScreenRegressionTests(){
  testBug121_NoCoddyMentionInSkillLayout();
  testBug122_XpFloatParticleNoStretch();
  testBug123_DirectNoteToCardsTransition();
  testBug124_SingleDominantCtaToCards();
  testBug125_CleanHumanExamMilestoneTitle();
  testBug126_NoSolutionSpoilerQuickTokens();
  testBug127_ComprehensionChecksEliminated();
  console.log('\n================================================================');
  console.log('  ALL 7 SKILL SCREEN REGRESSION TESTS (BUGS 121..127) PASSED!   ');
  console.log('================================================================\n');
}

if (require.main === module) {
  try {
    runAllSkillScreenRegressionTests();
  } catch (err) {
    console.error('\n[REGRESSION ASSERTION FAILED]');
    console.error(err.message);
    process.exit(1);
  }
}

module.exports = {
  runAllSkillScreenRegressionTests,
  testBug121_NoCoddyMentionInSkillLayout,
  testBug122_XpFloatParticleNoStretch,
  testBug123_DirectNoteToCardsTransition,
  testBug124_SingleDominantCtaToCards,
  testBug125_CleanHumanExamMilestoneTitle,
  testBug126_NoSolutionSpoilerQuickTokens,
  testBug127_ComprehensionChecksEliminated
};
