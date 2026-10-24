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
const academyHtml = fs.readFileSync(academyPath, 'utf-8').replace(/\r\n/g, '\n');

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

// 8. Bug 128 (Defect 8): Полная ликвидация мусорных строк («Шаг 7 из 7», «Сессия ~2 мин») из шапки экрана навыка
function testBug128_JunkStepCounterLinesEliminated(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );
  assert(
    !vsSkillMatch.includes('Шаг ${stepIdx + 1} из ${steps.length}'),
    'Bug 128: "Шаг X из Y" junk text must be completely eliminated from skill screen header'
  );
  assert(
    !vsSkillMatch.includes('Сессия ~2 мин · Активное микрообучение'),
    'Bug 128: "Сессия ~2 мин · Активное микрообучение" junk text must be completely eliminated from skill screen header'
  );
  assert(
    !vsSkillMatch.includes('step-counter-pill'),
    'Bug 128: step-counter-pill class must be removed from skill header'
  );
  console.log('✓ Bug 128: Elimination of junk step counter lines and clean skill header verified');
}

// 9. Bug 129 (Defect 9): Архитектура парных точек тем (тематические карточки идут сразу после соответствующего конспекта)
function testBug129_PairedDotsArchitecture(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );
  assert(
    vsSkillMatch.includes('topicClusterDots'),
    'Bug 129: viewPythonSkill must build paired topicClusterDots sequence'
  );
  assert(
    vsSkillMatch.includes('dot-jewel dot-card'),
    'Bug 129: Card dots must use .dot-jewel.dot-card class to be visually paired with their note'
  );
  assert(
    !vsSkillMatch.includes('dots-topic-divider'),
    'Bug 129: Divider between topics of notes and cards must be removed (only practice stage divider remains)'
  );
  assert(
    vsSkillMatch.includes('<span class="dots-stage-divider" title="Переход к задачам в IDE"></span>'),
    'Bug 129: Stage divider with practice must be preserved'
  );
  console.log('✓ Bug 129: Paired dots architecture (cards immediately follow their note, zero intra-topic divider) verified');
}

// 10. Bug 130 (Defect 10): Сквозной переход от карточек к следующей теме или в практику IDE
function testBug130_IntraSkillCardsToNextTopicTransition(){
  const finishCardsHandler = academyHtml.slice(
    academyHtml.indexOf("const finishCardsBtn = e.target.closest('[data-py-finish-cards-btn]');"),
    academyHtml.indexOf("const prc = e.target.closest('[data-py-rate-card]');")
  );
  assert(
    finishCardsHandler.includes("pySkillViewState.tab = 'theory';") &&
    finishCardsHandler.includes('pySkillViewState.kId = nextKid;'),
    'Bug 130: Finishing cards must transition to next topic theory note when more topics exist'
  );
  assert(
    finishCardsHandler.includes("pySkillViewState.tab = 'code';"),
    'Bug 130: Finishing cards on the last topic must transition directly to IDE practice'
  );
  console.log('✓ Bug 130: Seamless intra-skill transition from cards to next topic theory verified');
}

// 11. Bug 131 (Defect 11): Верификация загрузки реального бэкапа прогресса пользователя (user_progress_backup.json)
function testBug131_UserProgressBackupLoad(){
  const backupPath = path.join(rootDir, 'tests', 'fixtures', 'user_progress_backup.json');
  assert(fs.existsSync(backupPath), `User backup fixture missing at ${backupPath}`);
  const raw = fs.readFileSync(backupPath, 'utf-8');
  const backup = JSON.parse(raw);
  assert(backup.academyState, 'Backup must contain valid academyState');
  assert(backup.academyState.xp >= 6000, `User XP must be >= 6000, got ${backup.academyState.xp}`);
  assert(backup.academyState.streak >= 15, `User streak must be >= 15, got ${backup.academyState.streak}`);
  assert(Array.isArray(backup.academyState.readNotes), 'readNotes must be an array');
  assert(Array.isArray(backup.academyState.reviewedDecks), 'reviewedDecks must be an array');
  assert(backup.academyState.readingPositions && backup.academyState.readingPositions['1.9.1'], 'Backup must preserve Skill 1.9.1 reading position');
  console.log('✓ Bug 131: Real user progress backup verified (XP: ' + backup.academyState.xp + ', Streak: ' + backup.academyState.streak + ' days)');
}

// 12. Bug 132 (Defect 12): Интерактивные кликабельные микро-точки шагов в футере карточки теории
function testBug132_FooterStepMicroStepper(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );
  assert(
    vsSkillMatch.includes('step-footer-stepper'),
    'Bug 132: viewPythonSkill must contain .step-footer-stepper in theory card footer'
  );
  assert(
    vsSkillMatch.includes('step-micro-dot'),
    'Bug 132: viewPythonSkill must render .step-micro-dot elements for step progress'
  );
  assert(
    vsSkillMatch.includes('data-py-jump-step'),
    'Bug 132: viewPythonSkill must support interactive step jumping via data-py-jump-step'
  );
  assert(
    !vsSkillMatch.includes('step-footer-pct'),
    'Bug 132: step-footer-pct badge must be removed from footer stepper'
  );
  assert(
    !vsSkillMatch.includes('step-footer-text'),
    'Bug 132: step-footer-text must be removed from footer stepper (only clean clickable dots remain)'
  );
  assert(
    academyHtml.includes('.step-micro-dot {') && academyHtml.includes('.step-micro-dot.active'),
    'Bug 132: CSS must include styling for .step-micro-dot and .step-micro-dot.active'
  );
  console.log('✓ Bug 132: Pure clickable step micro-dots (zero text/pill clutter) verified');
}

// Bug 133: Идеальное центрирование и равная ширина чанков (.feed-chunk) во избежание сдвига/ступеньки абзацев
function testBug133_FeedChunkFullWidthAlignment(){
  assert(
    academyHtml.includes('.feed-chunk{\n    width:100%;\n    box-sizing:border-box;') ||
    academyHtml.includes('.feed-chunk{width:100%;box-sizing:border-box;') ||
    academyHtml.includes('.feed-chunk{\n    width:100%;'),
    'Bug 133: .feed-chunk must have width:100% and box-sizing:border-box'
  );
  assert(
    academyHtml.includes('.feed-chunk.lesson-theory {\n    width:100%;\n    max-width: 760px;'),
    'Bug 133: .feed-chunk.lesson-theory must have width:100% to prevent flex content-shrink misalignment'
  );
  assert(
    academyHtml.includes('.scroll-feed{\n    display:flex;flex-direction:column;gap:0;\n    align-items:stretch;'),
    'Bug 133: .scroll-feed must enforce align-items:stretch for child chunks'
  );
  console.log('✓ Bug 133: Full-width alignment & zero horizontal offset across theory chunks verified');
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
  testBug128_JunkStepCounterLinesEliminated();
  testBug129_PairedDotsArchitecture();
  testBug130_IntraSkillCardsToNextTopicTransition();
  testBug131_UserProgressBackupLoad();
  testBug132_FooterStepMicroStepper();
  testBug133_FeedChunkFullWidthAlignment();
  console.log('\n================================================================');
  console.log('  ALL 13 SKILL SCREEN REGRESSION TESTS (BUGS 121..133) PASSED!  ');
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
  testBug127_ComprehensionChecksEliminated,
  testBug128_JunkStepCounterLinesEliminated,
  testBug129_PairedDotsArchitecture,
  testBug130_IntraSkillCardsToNextTopicTransition,
  testBug131_UserProgressBackupLoad,
  testBug132_FooterStepMicroStepper,
  testBug133_FeedChunkFullWidthAlignment
};
