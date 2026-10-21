/**
 * test_dashboard_regression.js
 * Тотальный регрессионный сьют проверок экрана дашборда (viewDashboard, #/).
 * Проверяет соответствие каноническим инвариантам AGENTS.md, workspace-rule.md и эталонам платформы.
 * Охватывает Баги 134..136 (устранение тайминга 2 мин, закрепление «Продолжить дальше», отказ от хардкода, лаконичные формулировки).
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const academyPath = path.join(rootDir, 'academy.html');

console.log('================================================================');
console.log('   DASHBOARD VISUAL & ERGONOMIC REGRESSION SUITE                ');
console.log('   BUGS 134..136 VERIFICATION (CANONICAL BENCHMARK)             ');
console.log('================================================================\n');

assert(fs.existsSync(academyPath), `academy.html missing at ${academyPath}`);
const academyHtml = fs.readFileSync(academyPath, 'utf-8');

// 1. Bug 134 (Defect 1): Устранение тайминга (2 мин) из кнопок действия и лаконичная формулировка CTA
function testBug134_SingleDominantCtaLabelNo2MinAndContinueFurther(){
  assert(
    !academyHtml.includes("'Начать дальше (2 мин)'"),
    'Bug 134: academy.html must not contain "Начать дальше (2 мин)"'
  );
  assert(
    !academyHtml.includes("'Продолжить дальше (2 мин)'"),
    'Bug 134: academy.html must not contain "Продолжить дальше (2 мин)"'
  );
  assert(
    !academyHtml.includes('Повторить карточки (2 мин)'),
    'Bug 134: cocoon-focus-cta must not contain "(2 мин)" in cards label'
  );
  assert(
    !academyHtml.includes('Решить задачу в IDE (2 мин)'),
    'Bug 134: cocoon-focus-cta must not contain "(2 мин)" in IDE task label'
  );
  assert(
    academyHtml.includes("const ctaLabel = 'Продолжить';") ||
    academyHtml.includes("const ctaLabel = 'Продолжить дальше';"),
    'Bug 134: ctaLabel in viewDashboard must use concise "Продолжить"'
  );
  console.log('✓ Bug 134: Single Dominant CTA without (2 мин) timing and with concise "Продолжить" verified');
}

// 2. Bug 135 (Defect 2): Разграничение статусов «освоено» vs «закрыто» и согласование рода в аккордеоне тем
function testBug135_AccordionStatusMasteredVsLockedSemantics(){
  assert(
    !academyHtml.includes('${curUnitDoneCount} из ${curUnitTotal} тем закрыто'),
    'Bug 135: accordionStatusText must not label mastered topics as "тем закрыто"'
  );
  assert(
    !academyHtml.includes('${curUnitDoneCount}/${curUnitTotal} закрыто'),
    'Bug 135: accordionMobStatusText must not label mastered topics as "закрыто"'
  );
  assert(
    !academyHtml.includes('1 в фокусе · ${lockedCount} закрыто'),
    'Bug 135: accordion must not use neuter "закрыто" for feminine plural topics'
  );
  assert(
    academyHtml.includes('${curUnitDoneCount} из ${curUnitTotal} тем освоено'),
    'Bug 135: accordionStatusText must label mastered topics as "тем освоено"'
  );
  assert(
    academyHtml.includes('${curUnitDoneCount}/${curUnitTotal} освоено'),
    'Bug 135: accordionMobStatusText must label mastered topics as "освоено"'
  );
  assert(
    academyHtml.includes('1 в фокусе · ${lockedCount} закрыты'),
    'Bug 135: accordion status must use correct plural agreement "закрыты"'
  );
  console.log('✓ Bug 135: Accordion status mastered vs locked semantics and correct plural agreement verified');
}

// 3. Bug 136 (Defect 3): Полный отказ от хардкода и динамические счетчики в дашборде
function testBug136_ZeroHardcodingAndLaconicPhrasingInDashboard(){
  assert(
    !academyHtml.includes("Модуль 1 · ${curUnitDone === 0 ? 'Старт темы 1' : `${curUnitDone} из ${curUnitTotal} тем`}"),
    'Bug 136: echelon-mp-counter must not hardcode "Модуль 1" for unit-level topic counter'
  );
  assert(
    !academyHtml.includes('· Старт с темы 1'),
    'Bug 136: echelon-mp-counter must not use redundant "с" in start label'
  );
  assert(
    !academyHtml.includes("title: 'Карточки: list & tuple'"),
    'Bug 136: cardList must not hardcode cards titles for unit 1.1'
  );
  assert(
    !academyHtml.includes('Дневная цель: ${tXp} / ${dailyGoal} XP (${goalPct}%)'),
    'Bug 136: daily goal title must not duplicate percentage when goalPct badge is already present'
  );
  console.log('✓ Bug 136: Zero hardcoding and dynamic counters across dashboard verified');
}

// 4. Bug 137 (Defect 4): Первичная лаконичность Жадного Дескриптора и ликвидация тавтологий
function testBug137_GreedyDescriptorConciseness(){
  assert(
    !academyHtml.includes('Темы раздела:'),
    'Bug 137: accordion must not use forbidden term "раздел" (Decision 16 & AGENTS.md)'
  );
  assert(
    academyHtml.includes('<span class="dash-accordion-title-desk">Темы: ${escapeHtmlStr(cleanUnitTitle)}</span>'),
    'Bug 137: accordion title must use concise "Темы: ..."'
  );
  assert(
    !academyHtml.includes('2-минутный'),
    'Bug 137: dashboard must strictly eliminate all leaked "2-минутный" mentions'
  );
  assert(
    academyHtml.includes('Карта навыков ➔'),
    'Bug 137: accordion map link must use concise "Карта навыков ➔"'
  );
  assert(
    academyHtml.includes('<span class="echelon-label-full">Готовность к тех-скринингу</span>'),
    'Bug 137: echelon header must use concise "Готовность к тех-скринингу" without triple "Старт"'
  );
  console.log('✓ Bug 137: Greedy Descriptor conciseness, zero tautologies and unified terms verified');
}

// 5. Bug 138 (Defect 5): Бескомпромиссная лаконичность Жадного Дескриптора (Decision 45)
function testBug138_ExtremeConcisenessAndZeroVerbalClutter(){
  assert(
    !academyHtml.includes('Ждёт первого шага · Цель: 50 XP'),
    'Bug 138: echelon xp badge must not duplicate daily goal or prompt'
  );
  assert(
    !academyHtml.includes('Колода: ${escapeHtmlStr(cleanTitle)}'),
    'Bug 138: SRS preview must eliminate redundant "Колода:" label'
  );
  assert(
    academyHtml.includes('🔥 ${currentStreakVal} дн.'),
    'Bug 138: streak badge must eliminate redundant "Серия:" label'
  );
  assert(
    academyHtml.includes('Тема 1 из ${curUnitTotal}') &&
    academyHtml.includes('${curUnitDone === 0 ? `Тема 1 из ${curUnitTotal}` : `${curUnitDone} из ${curUnitTotal} тем`}') &&
    !academyHtml.includes('Тема 1 из ${curUnitTotal} · Старт'),
    'Bug 138: echelon topic counter must not duplicate unit title'
  );
  assert(
    !academyHtml.includes('Дневная цель: ${tXp}'),
    'Bug 138: goal title must use unified "Цель дня" вместо "Дневная цель"'
  );
  console.log('✓ Bug 138: Extreme conciseness, zero duplicate labels and streamlined typography verified');
}

// 6. Bug 139 (Defect 6): Радикальное очищение топбара эшелона и лаконичность дашборда (Decision 46)
function testBug139_GreedyDescriptorPhaseTwoDashboardConciseness(){
  assert(
    !academyHtml.includes('class="echelon-subrow-xp"'),
    'Bug 139: redundant daily xp subrow must be eliminated from echelon topbar markup'
  );
  assert(
    !academyHtml.includes('<span class="topbar-help-text">О модуле</span>'),
    'Bug 139: duplicate "О модуле" docs button must be eliminated from echelon topbar'
  );
  assert(
    !academyHtml.includes('class="echelon-foot-desc-desk"') && !academyHtml.includes('class="echelon-foot-desc-mob"'),
    'Bug 139: tautological "Допуск к первому скринингу" footer under progress bar must be eliminated'
  );
  assert(
    academyHtml.includes('topbar-audio-btn'),
    'Bug 139: single audio companion briefing button must be preserved in echelon topbar'
  );
  assert(
    academyHtml.includes('echelon-tier-tag'),
    'Bug 139: echelon tier tag must be cleanly placed beside readiness rank'
  );
  console.log('✓ Bug 139: Greedy Descriptor Phase Two dashboard conciseness verified');
}


// 7. Bug 140 (Defect 7): Третья фаза лаконичности дашборда по канону Жадного Дескриптора (Decision 47)
function testBug140_GreedyDescriptorPhaseThreeDashboardPerfection(){
  assert(
    !academyHtml.includes('· Старт`'),
    'Bug 140: redundant "· Старт" pleonasm must be eliminated from echelon topic counter'
  );
  assert(
    academyHtml.includes('Первый шаг продлит серию до 🔥 <b>${currentStreakVal + 1} дн.</b>'),
    'Bug 140: streak hint must follow proper Russian grammar with "до"'
  );
  assert(
    academyHtml.includes('Тех-скрининг'),
    'Bug 140: mobile echelon label must use compact "Тех-скрининг"'
  );
  assert(
    academyHtml.includes('До открытия: ${remainingSteps}&nbsp;${stepsText} (+10&nbsp;XP)'),
    'Bug 140: closed SRS preview must dynamically reflect remaining steps'
  );
  console.log('✓ Bug 140: Greedy Descriptor Phase Three dashboard perfection verified');
}

// 8. Bug 141 (Defect 8): Четвертая фаза лаконичности по канону Жадного Дескриптора (Decision 48)
function testBug141_GreedyDescriptorPhaseFourMobileFoldAndSrsBalance(){
  assert(
    academyHtml.includes('class="echelon-title-group"'),
    'Bug 141: echelon title group class must be present for mobile single-line alignment'
  );
  assert(
    academyHtml.includes('class="srs-clean-footer meta"'),
    'Bug 141: srs-clean-footer must be present to balance desktop void in empty SRS card'
  );
  assert(
    academyHtml.includes('srs-deck-title-desk') && academyHtml.includes('srs-deck-title-mob'),
    'Bug 141: responsive srs deck titles must protect against mobile truncation'
  );
  assert(
    academyHtml.includes('.srs-clean-footer { display: flex !important; }'),
    'Bug 141: srs-clean-footer must be active on desktop and hidden on mobile'
  );
  console.log('✓ Bug 141: Greedy Descriptor Phase Four mobile fold and SRS balance verified');
}

testBug134_SingleDominantCtaLabelNo2MinAndContinueFurther();
testBug135_AccordionStatusMasteredVsLockedSemantics();
testBug136_ZeroHardcodingAndLaconicPhrasingInDashboard();
testBug137_GreedyDescriptorConciseness();
testBug138_ExtremeConcisenessAndZeroVerbalClutter();
testBug139_GreedyDescriptorPhaseTwoDashboardConciseness();
testBug140_GreedyDescriptorPhaseThreeDashboardPerfection();
testBug141_GreedyDescriptorPhaseFourMobileFoldAndSrsBalance();

console.log('================================================================');
console.log('  ALL DASHBOARD REGRESSION TESTS (BUGS 134..141) PASSED (100%)  ');
console.log('================================================================\n');
