/**
 * test_cards_trainer_regression.js
 * Тотальный регрессионный сьют проверок тренажёра карточек и алгоритмов SRS платформы.
 * Проверяет соответствие каноническим инвариантам AGENTS.md и правилам проекта.
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const academyPath = path.join(rootDir, 'academy.html');
const etalonyPath = path.join(rootDir, 'standards', 'standards.html');

console.log('================================================================');
console.log('   FLASHCARDS & SRS TRAINER REGRESSION TEST SUITE               ');
console.log('================================================================\n');

assert(fs.existsSync(academyPath), `academy.html missing at ${academyPath}`);
const academyHtml = fs.readFileSync(academyPath, 'utf-8').replace(/\r\n/g, '\n');

// Тест-кейс 1: Запрет утечки технических ID колод (Ф-xxx) в режиме очереди повторения на сегодня
function testCleanHumanUiDueMode(){
  const dueModeMatch = academyHtml.slice(
    academyHtml.indexOf('if(cardsHubState.dueMode){'),
    academyHtml.indexOf('const allDeckIds = Object.keys(ALL_DECKS_COMBINED)')
  );
  assert(
    !dueModeMatch.includes('${item.deckId} ·'),
    'Defect 1: dueMode must not render technical deck ID ${item.deckId} in user UI'
  );
  assert(
    dueModeMatch.includes('${cleanDeckName}'),
    'Defect 1: dueMode must render clean human deck title without Ф-xxx prefix'
  );
}

// Тест-кейс 2: Защита от тупика навигации на ответе первой карточки (Zero-Trap Navigation on duePos === 0)
function testZeroTrapNavigationDueMode(){
  const dueModeMatch = academyHtml.slice(
    academyHtml.indexOf('if(cardsHubState.dueMode){'),
    academyHtml.indexOf('const allDeckIds = Object.keys(ALL_DECKS_COMBINED)')
  );
  const dueAnswerFace = dueModeMatch.slice(
    dueModeMatch.indexOf('cardsHubState.flipped ? (() => {'),
    dueModeMatch.indexOf('})() :')
  );
  assert(
    !dueAnswerFace.includes('disabled'),
    'Defect 2: data-hub-prev on answer side must not be disabled on duePos === 0'
  );
  assert(
    dueModeMatch.includes('data-hub-flip') && dueModeMatch.includes('fc-card--3d'),
    'Defect 2: card in dueMode must support flip interaction to return to question'
  );
}

// Тест-кейс 3: Сохранение 3D-эстетики и стиля Zen Glassmorphism в режиме очереди дня
function testGlassmorphismAestheticsDueMode(){
  const dueModeMatch = academyHtml.slice(
    academyHtml.indexOf('if(cardsHubState.dueMode){'),
    academyHtml.indexOf('const allDeckIds = Object.keys(ALL_DECKS_COMBINED)')
  );
  assert(
    !dueModeMatch.includes('class="fc-card ${cardsHubState.flipped ? \'flipped\' : \'\'}"'),
    'Defect 3: dueMode must not use non-existent .flipped class without 3D styles'
  );
  assert(
    dueModeMatch.includes('fc-card--3d') && dueModeMatch.includes('fc-card-inner'),
    'Defect 3: dueMode must use canonical .fc-card--3d and .fc-card-inner markup'
  );
}

// Тест-кейс 4: Корректная грамматическая плюрализация слова «карточка» при завершении колоды
function testRussianPluralizationCompletion(){
  assert(
    !academyHtml.includes('Все ${cards.length} карточек колоды'),
    'Defect 4: deck completion heading must not hardcode genitive plural "карточек" without pluralizeRu'
  );
  assert(
    academyHtml.includes("pluralizeRu(cards.length, 'карточка', 'карточки', 'карточек')"),
    'Defect 4: deck completion heading must format cards count using pluralizeRu'
  );
}

// Тест-кейс 5: Корректное сохранение актуальной оценки в SRS при забывании карточки (устранение Math.max бага)
function testSrsRatingDowngradeOnLapse(){
  const srsFnCode = academyHtml.slice(
    academyHtml.indexOf('function applyRemNoteCardRating'),
    academyHtml.indexOf('function getRemNoteCardStatusBadgeHTML')
  );
  assert(
    !srsFnCode.includes('Math.max(Number(state.cardRatings[cardKey]) || 0, g)'),
    'Defect 5: applyRemNoteCardRating must update state.cardRatings[cardKey] to latest grade g on lapse, not Math.max'
  );
}

// Тест-кейс 6: Защита от переполнения счётчика в сессионном цикле карточек урока («Карточка 6 из 5»)
function testLessonCardCounterOverflow(){
  const startIdx = academyHtml.indexOf('bodyHTML =', academyHtml.indexOf("} else if(pySkillViewState.tab === 'cards'){", 6056000));
  const endIdx = academyHtml.indexOf("} else if(pySkillViewState.tab === 'code'){", startIdx);
  const lessonCardsCode = academyHtml.slice(startIdx, endIdx);
  assert(
    !lessonCardsCode.includes('<span style="color:var(--ink-muted);font-weight:600;">Карточка ${qPos + 1} из ${cards.length}</span>'),
    'Defect 6: lesson cards counter must not render hardcoded "Карточка N из M" where N > M during error repetition loops'
  );
  assert(
    lessonCardsCode.includes('${cardCounterLabel}'),
    'Defect 6: lesson cards counter must use dynamic cardCounterLabel'
  );
}

// Тест-кейс 7: Наличие эталонной кнопки «💡 Шпаргалка» в Центре интервального повторения
function testCardsCheatSheetButton(){
  const hubCode = academyHtml.slice(
    academyHtml.indexOf('function viewCardsHub'),
    academyHtml.indexOf('/* ================= 401-TASK CODING TRAINER')
  );
  assert(
    hubCode.includes('Шпаргалка') || hubCode.includes('data-hub-cheatsheet'),
    'Defect 7: viewCardsHub must render reference cheat sheet action button according to canonical benchmark'
  );
}

// Тест-кейс 8: Горячая клавиша Enter для переворота карточки вопроса
function testEnterKeyFlipErgonomics(){
  const enterKeyMatch = academyHtml.slice(
    academyHtml.indexOf("if(e.key === 'Enter' && !e.ctrlKey && !e.metaKey){"),
    academyHtml.indexOf('// Register PWA Service Worker')
  );
  assert(
    enterKeyMatch.includes('flipBtn') || enterKeyMatch.includes('data-hub-flip'),
    'Defect 8: Enter key event handler must trigger card flip when on question side'
  );
}


// Тест-кейс 9: Отсутствие дублирования кнопки «💡 Шпаргалка» на экране завершения колоды
function testNoDuplicateCheatSheetInCompletedHub(){
  const start = academyHtml.indexOf('if(cardsHubState.completed && cards.length > 0){');
  const ret1 = academyHtml.indexOf('return `\n    <div class="container', start);
  const end = academyHtml.indexOf('return `\n    <div class="container', ret1 + 10);
  const completedBlock = academyHtml.slice(start, end);
  const matches = completedBlock.match(/data-hub-cheatsheet/g);
  assert(
    matches && matches.length === 1,
    `Defect 9: Completed deck screen must have exactly 1 cheatsheet button, found ${matches ? matches.length : 0}`
  );
}

// Тест-кейс 10: Мобильная эргономика селекторов фильтров (min-width: 0 против переполнения на 390px)
function testMobileSelectEllipsisNoOverflow(){
  assert(
    academyHtml.includes('.cards-hub-subfilters select{') &&
    academyHtml.includes('min-width:0 !important;width:100% !important;box-sizing:border-box !important;'),
    'Defect 10: .cards-hub-subfilters select must have min-width:0 and width:100% to prevent overflow on mobile'
  );
}

// Тест-кейс 11: Прогрессия интервалов SM-2 при повторных оценках «Трудно» (reps + 1)
function testHardRatingIntervalProgression(){
  const srsFnCode = academyHtml.slice(
    academyHtml.indexOf('function computeRemNoteIntervals'),
    academyHtml.indexOf('function applyRemNoteCardRating')
  );
  assert(
    !srsFnCode.includes('hard:  { days: hardDays,  ease: Math.max(1.30, +(ease - 0.15).toFixed(2)), reps: Math.max(1, reps)'),
    'Defect 11: computeRemNoteIntervals must not freeze reps at Math.max(1, reps) on hard rating'
  );
  assert(
    srsFnCode.includes('hard:  { days: hardDays,  ease: Math.max(1.30, +(ease - 0.15).toFixed(2)), reps: reps + 1'),
    'Defect 11: computeRemNoteIntervals must increment reps (reps + 1) on hard rating for interval progression'
  );
}

// Тест-кейс 12: Интерактивный Stories Bar в общем хабе колод и в режиме очереди дня
function testInteractiveStoriesBarInHubAndDue(){
  assert(
    academyHtml.includes('data-hub-goto-card="${i}"'),
    'Defect 12: buildFcStoriesBarHTML must render clickable data-hub-goto-card segments'
  );
  assert(
    academyHtml.includes('data-hub-goto-due='),
    'Defect 12: viewCardsHub dueMode must render clickable due stories bar'
  );
  assert(
    academyHtml.includes('cardsHubState.cardIdx = parseInt(hGotoCard.getAttribute'),
    'Defect 12: event handler must support direct jump via data-hub-goto-card'
  );
}

// Тест-кейс 13: Эргономичная подпись «← К вопросу» на стороне ответа карточки
function testAnswerFaceButtonLabel(){
  assert(
    academyHtml.includes('← К вопросу'),
    'Defect 13: card answer face must render unambiguous "← К вопросу" button'
  );
}

// Тест-кейс 14: Защита от блокировки кнопки «← К вопросу» на первой карточке в каталоге и уроке
function testZeroTrapNavigationAnswerFaceCatalogAndLesson(){
  // Каталог колод: сторона ответа
  const catalogAnswerMatch = academyHtml.slice(
    academyHtml.indexOf('cardsHubState.flipped ? (() => {', academyHtml.indexOf('function viewCardsHub')),
    academyHtml.indexOf('})() : `\n          <div style="margin-top:12px;display:flex;gap:10px;align-items:center;">', academyHtml.indexOf('function viewCardsHub'))
  );
  assert(
    !catalogAnswerMatch.includes('data-hub-prev ${cIdx===0?\'disabled\':\'\'}'),
    'Defect 14: data-hub-prev on answer face in catalog must not be disabled on cIdx === 0'
  );

  // Урок: сторона ответа
  const lessonAnswerMatch = academyHtml.slice(
    academyHtml.indexOf('pySkillViewState.cardFlipped ? `\n            <div class="fc-rate-row"'),
    academyHtml.indexOf('` : `\n            <div style="margin-top:12px;display:flex;gap:10px;align-items:center;">')
  );
  assert(
    !lessonAnswerMatch.includes('data-py-prev-card ${qPos === 0 ? \'disabled\' : \'\'}'),
    'Defect 14: data-py-prev-card on answer face in lesson must not be disabled on qPos === 0'
  );
}

// Тест-кейс 15: Лаконичные заголовки эшелонов для предотвращения обрезки селектора на мобильных
function testConciseEchelonLabels(){
  assert(
    academyHtml.includes('>🎯 Все 4 эшелона</option>'),
    'Defect 15: echelonOpts must render concise label "🎯 Все 4 эшелона" without bloated suffixes'
  );
  assert(
    academyHtml.includes('>🚨 Эшелон 1 · Скрининг и база</option>'),
    'Defect 15: echelonOpts must render concise label for Echelon 1'
  );
}

// Экспорт или прямой прогон
module.exports = {
  testCleanHumanUiDueMode,
  testZeroTrapNavigationDueMode,
  testGlassmorphismAestheticsDueMode,
  testRussianPluralizationCompletion,
  testSrsRatingDowngradeOnLapse,
  testLessonCardCounterOverflow,
  testCardsCheatSheetButton,
  testEnterKeyFlipErgonomics,
  testNoDuplicateCheatSheetInCompletedHub,
  testMobileSelectEllipsisNoOverflow,
  testHardRatingIntervalProgression,
  testInteractiveStoriesBarInHubAndDue,
  testAnswerFaceButtonLabel,
  testZeroTrapNavigationAnswerFaceCatalogAndLesson,
  testConciseEchelonLabels
};

if(require.main === module){
  console.log('Запуск тестов тренажёра карточек:');
  const tests = [
    ['1. Clean Human UI в dueMode', testCleanHumanUiDueMode],
    ['2. Zero-Trap навигация на duePos === 0', testZeroTrapNavigationDueMode],
    ['3. 3D Zen Glassmorphism в dueMode', testGlassmorphismAestheticsDueMode],
    ['4. Русская плюрализация при завершении', testRussianPluralizationCompletion],
    ['5. Снижение рейтинга в SRS при ошибке', testSrsRatingDowngradeOnLapse],
    ['6. Счётчик сессионного цикла урока', testLessonCardCounterOverflow],
    ['7. Кнопка «Шпаргалка» в хабе карточек', testCardsCheatSheetButton],
    ['8. Клавиша Enter для переворота вопроса', testEnterKeyFlipErgonomics],
    ['9. Нет дублирования шпаргалки в завершении', testNoDuplicateCheatSheetInCompletedHub],
    ['10. Мобильная эргономика селекторов колод', testMobileSelectEllipsisNoOverflow],
    ['11. Прогрессия интервалов SM-2 на «Трудно»', testHardRatingIntervalProgression],
    ['12. Интерактивный Stories Bar в каталоге и дне', testInteractiveStoriesBarInHubAndDue],
    ['13. Эргономичная подпись «← К вопросу»', testAnswerFaceButtonLabel],
    ['14. Zero-Trap «← К вопросу» в каталоге и уроке', testZeroTrapNavigationAnswerFaceCatalogAndLesson],
    ['15. Лаконичные метки эшелонов без переполнения', testConciseEchelonLabels]
  ];

  let failed = 0;
  for(const [name, fn] of tests){
    try{
      fn();
      console.log(`  ✓ [PASS] ${name}`);
    }catch(err){
      failed++;
      console.log(`  ✕ [FAIL] ${name}: ${err.message}`);
    }
  }
  console.log(`\nИтог: провалено ${failed} из ${tests.length} проверок (подтверждены дефекты для Генератора).\n`);
}
