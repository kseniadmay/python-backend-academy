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
const etalonyPath = path.join(rootDir, 'Эталоны', 'Эталоны.html');

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

// Экспорт или прямой прогон
module.exports = {
  testCleanHumanUiDueMode,
  testZeroTrapNavigationDueMode,
  testGlassmorphismAestheticsDueMode,
  testRussianPluralizationCompletion,
  testSrsRatingDowngradeOnLapse,
  testLessonCardCounterOverflow,
  testCardsCheatSheetButton,
  testEnterKeyFlipErgonomics
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
    ['8. Клавиша Enter для переворота вопроса', testEnterKeyFlipErgonomics]
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
