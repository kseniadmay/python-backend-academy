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
const academyHtml = fs.readFileSync(academyPath, 'utf-8').replace(/\r\n/g, '\n');

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

function testBug142_GreedyDescriptorTrailPerfection(){
  // 1. Zero "2 мин" in trail bubbles or buttons
  assert(
    !academyHtml.includes('НАЧАТЬ (2 МИН)'),
    'Bug 142: path bubble and popover must not contain (2 МИН)'
  );
  assert(
    !academyHtml.includes('ПРОДОЛЖИТЬ (2 МИН)'),
    'Bug 142: path bubble and pro hero CTA must not contain (2 МИН)'
  );
  // 2. No technical unit codes in popover title
  assert(
    academyHtml.includes('`Урок ${lessonNumInChap} · ${cleanUnitTitle(u.id, u.title)}`'),
    'Bug 142: popover title must use human lesson numbering instead of Юнит X.Y'
  );
  // 3. Clean Russian in popover status and skills label
  assert(
    academyHtml.includes('✅ Урок освоен на 100%') && academyHtml.includes('🔒 Откроется после предыдущих уроков'),
    'Bug 142: popover status must use polished human language'
  );
  assert(
    academyHtml.includes('Ключевые темы урока:'),
    'Bug 142: popover skills label must be clean without machine unit code'
  );
  // 4. No forbidden РАЗДЕЛ in pro-hero breadcrumbs
  assert(
    !academyHtml.includes('РАЗДЕЛ ${activeChap.num} · ГЛАВА'),
    'Bug 142: pro hero breadcrumbs must not use forbidden РАЗДЕЛ or tautology'
  );
  assert(
    academyHtml.includes('ПРОГРАММА › ГЛАВА ${activeChap.num}'),
    'Bug 142: pro hero breadcrumbs must be clean and canonical'
  );
  // 5. Mobile chapter visibility in banner
  assert(
    academyHtml.includes('.path-chapter-crumb-label .pcl-short') && academyHtml.includes('ГЛ. ${activeChapterNum}'),
    'Bug 142: mobile banner must preserve chapter indicator via responsive pcl-short'
  );
  // 6. Compact right rail SRS copy and echelon synchronization
  assert(
    academyHtml.includes('Очередь пуста. Пройдите первый урок, чтобы открыть карточки к скринингу.'),
    'Bug 142: right rail SRS empty state must be concise'
  );
  assert(
    academyHtml.includes('const { units: echUnits, chapters: echChapters } = (typeof getEchelonUnitsAndChapters === \'function\')'),
    'Bug 142: right rail must synchronize chapter units with active echelon'
  );
  assert(
    academyHtml.includes('<span>Набрано: <strong>${dailyXp} XP</strong></span>'),
    'Bug 142: daily goal summary in right rail must eliminate triple 50 XP repetition'
  );
  assert(
    academyHtml.includes('cleanChTitle'),
    'Bug 142: pro mode must strip duplicate Глава N: prefix from accordion title'
  );
  console.log('✓ Bug 142: Greedy Descriptor Trail perfection, zero noise and clean typography verified');
}

function testBug143_GreedyDescriptorTrailStepNavigationAndConciseness(){
  // 1. Zero (2 мин) in sidebar quickBtn
  assert(
    academyHtml.includes("quickBtn.innerHTML = '⚡ Микро-шаг';"),
    'Bug 143: sidebar quickBtn must be concise without (2 мин)'
  );
  assert(
    !academyHtml.includes('⚡ Быстрый микро-шаг (2 мин) ➔'),
    'Bug 143: track focus card button must be concise without (2 мин)'
  );
  // 2. Interactive step navigation in popover
  assert(
    academyHtml.includes('path-popover-steps-list') && academyHtml.includes('path-popover-step'),
    'Bug 143: popover must render interactive steps list for all lesson topics'
  );
  assert(
    academyHtml.includes('pps-marker') && academyHtml.includes('pps-title'),
    'Bug 143: popover steps must render status marker and topic title'
  );
  assert(
    academyHtml.includes("e.target.closest('.path-popover-step')"),
    'Bug 143: click listener must support direct jump via popover step'
  );
  // 3. Clean chapter title in gate cards without machine prefix
  assert(
    academyHtml.includes('cleanPrevTitle') && academyHtml.includes('cleanCurTitle'),
    'Bug 143: chapter gate cards must clean machine prefixes from chapter titles'
  );
  // 4. Disambiguated active bubble counter
  assert(
    academyHtml.includes('${unitSkillsMastered}/${unitTotalSkills} тем'),
    'Bug 143: active node bubble must label unit topics to avoid collision with chapter lessons'
  );
  // 5. Clean popover badge
  assert(
    academyHtml.includes('`Глава · ${trackTitleClean}`'),
    'Bug 143: popover badge must use clean human label without machine ТРЕК prefix'
  );
  console.log('✓ Bug 143: Greedy Descriptor Trail step navigation, interactive stepper and extreme conciseness verified');
}

function testBug144_EchelonTrailChapterMappingAndRightRailSync(){
  // 1. Correct chapter matching without slash mismatch in getEchelonUnitsAndChapters
  assert(
    academyHtml.includes("c.track === tr.key || c.track === (tr.routePrefix || '').replace(/^\\//, '')"),
    'Bug 144: getEchelonUnitsAndChapters must match c.track to tr.key to prevent all chapters defaulting to Chapter 1'
  );
  // 2. Removal of duplicate CSS block (lines 3260-3591)
  const pillBtnMatches = academyHtml.match(/\.path-echelon-pill-btn\s*\{/g) || [];
  assert.strictEqual(
    pillBtnMatches.length,
    1,
    'Bug 144: duplicate 332-line .path-echelon-pill-btn CSS block must be removed (expected exactly 1 definition)'
  );
  // 3. Pro hero breadcrumb preserves canonical breadcrumb
  assert(
    academyHtml.includes('ПРОГРАММА › ГЛАВА ${activeChap.num}'),
    'Bug 144: pro hero card must contain canonical chapter breadcrumb'
  );
  // 4. Right rail dynamic synchronization with active echelon
  assert(
    academyHtml.includes("const curProg = (typeof getEchelonProgress === 'function') ? getEchelonProgress(curTierNum) : null;") &&
    academyHtml.includes('const curPct = curProg ? curProg.pct : 0;'),
    'Bug 144: renderCoddyRightRail must dynamically compute progress for curTierNum instead of hardcoded Echelon 1'
  );
  assert(
    academyHtml.includes('${echUnits.length} тем'),
    'Bug 144: right rail radar widget link must dynamically display total echelon topics'
  );
  // 5. Mobile safe buffer in .path-serpentine-wrap
  assert(
    academyHtml.includes('padding: 12px 10px calc(160px + env(safe-area-inset-bottom, 24px));'),
    'Bug 144: .path-serpentine-wrap must include mobile bottom buffer to prevent tabbar collision'
  );
  console.log('✓ Bug 144: Echelon trail chapter mapping, right rail dynamic sync and zero duplicate CSS verified');
}

function testBug145_EchelonTrailSkillsAndPopoverAlignment(){
  // 1. Popover click handler scoped to active echelon
  assert(
    academyHtml.includes("const { units: echUnits, chapters: echChapters } = (typeof getEchelonUnitsAndChapters === 'function')") &&
    academyHtml.includes("const uChap = echChapters.find(cb => cb.units.some(x => x.id === uid));") &&
    academyHtml.includes("let activeIdx = echUnits.findIndex(x => {"),
    'Bug 145: popover node click handler must scope units, chapters and active index to current echelon'
  );
  // 2. Trail node chapter-scoped lesson numbering
  assert(
    academyHtml.includes("const uChap = chapterBreakpoints.find(cb => cb.units.some(x => x.id === u.id)) || curChapter;") &&
    academyHtml.includes("const lessonNumInChap = (uChap.units.findIndex(x => x.id === u.id) >= 0) ? (uChap.units.findIndex(x => x.id === u.id) + 1) : (i + 1);"),
    'Bug 145: viewPathSerpentine must compute lessonNumInChap within each unit chapter instead of defaulting to curChapter'
  );
  // 3. Challenge node accessible label and toast without technical unit codes
  assert(
    academyHtml.includes('Челлендж мастерства, проверка темы «${cleanUnitTitle(u.id, u.title)}»'),
    'Bug 145: challenge node aria-label must use clean human title without technical unit id'
  );
  assert(
    academyHtml.includes("showTactileToast('🔒 Челлендж откроется после прохождения предыдущих уроков')") &&
    !academyHtml.includes("showTactileToast('🔒 Челлендж откроется после прохождения предыдущих юнитов')"),
    'Bug 145: challenge node toast must use human term уроков instead of technical юнитов'
  );
  // 4. Service Worker cache increment
  const swContent = fs.readFileSync(path.join(rootDir, 'sw.js'), 'utf-8');
  assert(
    swContent.includes('academy-pwa-v57') || swContent.includes('academy-pwa-v58'),
    'Bug 145: Service Worker cache version must be incremented'
  );
  console.log('✓ Bug 145: Echelon trail skills and popover alignment across all tiers verified');
}

function testBug146_LessonCardResumePositionPersistence(){
  // 1. Reading position persistence saves sessionPos and deckPositions
  assert(
    academyHtml.includes('const curPos = (typeof pySkillViewState.sessionPos === \'number\')') &&
    academyHtml.includes('? pySkillViewState.sessionPos') &&
    academyHtml.includes('updatedDeckPositions[pySkillViewState.fId] = {') &&
    academyHtml.includes('sessionPos: curPos,') &&
    academyHtml.includes('cardIdx: curPos,'),
    'Bug 146: saveReadingPosition must persist sessionPos and per-deck deckPositions'
  );

  // 2. ensurePySkillState restores savedCardPos, sessionPos, sessionFid, and deckPositions
  assert(
    academyHtml.includes('const savedDeckInfo = (saved.deckPositions && saved.deckPositions[firstF]) || {};') &&
    academyHtml.includes('const savedCardPos = (typeof savedDeckInfo.sessionPos === \'number\')') &&
    academyHtml.includes('sessionPos: savedCardPos,') &&
    academyHtml.includes('sessionFid: firstF,'),
    'Bug 146: ensurePySkillState must restore cardIdx and sessionPos from saved readingPositions'
  );

  // 3. Intra-Session Loop initialization does not blindly reset sessionPos to 0
  assert(
    academyHtml.includes('const savedDeckInfo = (saved.deckPositions && saved.deckPositions[activeF]) || {};') &&
    academyHtml.includes('pySkillViewState.sessionPos = isDone ? cards.length : Math.max(0, Math.min(savedCardPos, Math.max(0, cards.length - 1)));') &&
    academyHtml.includes('pySkillViewState.cardIdx = pySkillViewState.sessionPos;'),
    'Bug 146: Intra-Session Loop must restore sessionPos from saved deck progress rather than hardcoding 0'
  );

  // 4. Dot switcher [data-py-select-f] does not unconditionally wipe cardIdx to 0
  assert(
    academyHtml.includes('const isDifferentDeck = (pySkillViewState.fId !== targetFid);') &&
    academyHtml.includes('} else if(pySkillViewState.sessionDone){') &&
    !academyHtml.includes('pySkillViewState.cardIdx = 0;\n    pySkillViewState.cardFlipped = false;\n    pySkillViewState.sprintCelebration = null;\n    saveReadingPosition();'),
    'Bug 146: [data-py-select-f] must not wipe cardIdx to 0 when clicking active deck'
  );

  // 5. Card rating and navigation event handlers keep cardIdx and sessionPos in sync
  assert(
    academyHtml.includes('pySkillViewState.sessionPos = qPos + 1;\n    pySkillViewState.cardIdx = pySkillViewState.sessionPos;\n    pySkillViewState.cardFlipped = false;') &&
    academyHtml.includes('pySkillViewState.sessionPos--;\n      pySkillViewState.cardIdx = pySkillViewState.sessionPos;'),
    'Bug 146: card handlers must keep sessionPos and cardIdx synchronized'
  );

  // 6. Service Worker cache increment to v58
  const swContent = fs.readFileSync(path.join(rootDir, 'sw.js'), 'utf-8');
  assert(
    swContent.includes('\'academy-pwa-v58\''),
    'Bug 146: Service Worker cache version must be incremented to academy-pwa-v58'
  );
  console.log('✓ Bug 146: Card position persistence, intra-session loop restore and SW v58 verified');
}

testBug134_SingleDominantCtaLabelNo2MinAndContinueFurther();
testBug135_AccordionStatusMasteredVsLockedSemantics();
testBug136_ZeroHardcodingAndLaconicPhrasingInDashboard();
testBug137_GreedyDescriptorConciseness();
testBug138_ExtremeConcisenessAndZeroVerbalClutter();
testBug139_GreedyDescriptorPhaseTwoDashboardConciseness();
testBug140_GreedyDescriptorPhaseThreeDashboardPerfection();
testBug141_GreedyDescriptorPhaseFourMobileFoldAndSrsBalance();
testBug142_GreedyDescriptorTrailPerfection();
testBug143_GreedyDescriptorTrailStepNavigationAndConciseness();
testBug144_EchelonTrailChapterMappingAndRightRailSync();
testBug145_EchelonTrailSkillsAndPopoverAlignment();
testBug146_LessonCardResumePositionPersistence();

console.log('================================================================');
console.log('  ALL DASHBOARD & TRAIL REGRESSION TESTS (BUGS 134..146) PASSED ');
console.log('================================================================\n');
