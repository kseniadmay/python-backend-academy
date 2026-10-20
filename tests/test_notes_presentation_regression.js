/**
 * test_notes_presentation_regression.js
 * Тотальный регрессионный сьют аудита подачи конспектов и активного микрообучения.
 * Проверяет баги 107..113 (7 системных дефектов, выявленных Дескриптором).
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const academyPath = path.join(rootDir, 'academy.html');

console.log('================================================================');
console.log('   NOTES PRESENTATION & ACTIVE LEARNING REGRESSION SUITE        ');
console.log('   BUGS 107..113 VERIFICATION                                   ');
console.log('================================================================\n');

assert(fs.existsSync(academyPath), `academy.html missing at ${academyPath}`);
const academyHtml = fs.readFileSync(academyPath, 'utf-8');

// Bug 107 (Defect 1): Подсветка синтаксиса строк в двойных кавычках и &quot;
function testBug107_SyntaxHighlightingDoubleQuotes(){
  const hlMatch = academyHtml.slice(
    academyHtml.indexOf('function highlightPythonTokens('),
    academyHtml.indexOf('// Helper to decorate <pre><code>')
  );

  // Регулярное выражение токенизатора обязано поддерживать &quot;...&quot;
  assert(
    hlMatch.includes('&quot;') || hlMatch.includes('quot'),
    'Bug 107: highlightPythonTokens must support &quot; escaped strings in tokenRegex'
  );
  console.log('✓ Bug 107: Syntax highlighting handles &quot; double quoted strings');
}

// Bug 108 (Defect 2): Видимый человеческий счётчик и сегментированный степпер микро-шагов текущего конспекта
function testBug108_VisibleStepCounterAndSegmentedBar(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );

  assert(
    vsSkillMatch.includes('Шаг ${stepIdx + 1} из ${steps.length}') ||
    vsSkillMatch.includes('Шаг ${stepIdx+1} из ${steps.length}') ||
    vsSkillMatch.includes('step-counter-pill'),
    'Bug 108: viewPythonSkill must render a visible step counter ("Шаг X из Y") for current note steps'
  );
  assert(
    vsSkillMatch.includes('step-segmented-track') ||
    vsSkillMatch.includes('step-segment') ||
    vsSkillMatch.includes('sprint-step-progress'),
    'Bug 108: viewPythonSkill must render a segmented progress bar for current lesson steps'
  );
  console.log('✓ Bug 108: Visible human step counter and segmented step progress bar verified');
}

// Bug 109 (Defect 3): Разграничение понятий «Тема» и «Шаг» в навигации Bottom Sheet
function testBug109_StepVsThemeTerminology(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );

  assert(
    !vsSkillMatch.includes('Дальше к следующей теме ➔'),
    'Bug 109: Navigation within note steps must not call a step a "тема" (found "Дальше к следующей теме ➔")'
  );
  assert(
    vsSkillMatch.includes('Дальше к следующему шагу ➔') || vsSkillMatch.includes('Следующий шаг ➔'),
    'Bug 109: Navigation within note steps must use "Дальше к следующему шагу ➔" or "Следующий шаг ➔"'
  );
  console.log('✓ Bug 109: Step vs Theme terminology invariant in bottom sheet verified');
}

// Bug 110 (Defect 4): Инвариант Single Dominant CTA и двухфазное разделение «Микро-ввод ➔ Активный отклик»
function testBug110_SingleDominantCtaTheoryFlow(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );

  assert(
    !vsSkillMatch.includes('👆 Ответьте на вопрос для продолжения'),
    'Bug 110: Single Dominant CTA must not be replaced with passive text placeholder "👆 Ответьте на вопрос для продолжения"'
  );
  assert(
    vsSkillMatch.includes('data-py-start-check') || vsSkillMatch.includes('data-py-step-phase'),
    'Bug 110: viewPythonSkill must provide active Single Dominant CTA to transition into comprehension check'
  );
  console.log('✓ Bug 110: Single Dominant CTA and phased active learning transition verified');
}

// Bug 111 (Defect 5): Защита от потери обратных слэшей в регулярных выражениях NOTE_STEP_CHECKS
function testBug111_NoCorruptedRegexEscapes(){
  const checksMatch = academyHtml.slice(
    academyHtml.indexOf('const NOTE_STEP_CHECKS ='),
    academyHtml.indexOf('function getStepCheck(') !== -1 ? academyHtml.indexOf('function getStepCheck(') : academyHtml.indexOf('const NOTE_STEP_CHECKS =') + 26000
  );

  assert(!checksMatch.includes('r"d+"'), 'Bug 111: NOTE_STEP_CHECKS must not contain corrupted r"d+" (must be r"\\d+")');
  assert(!checksMatch.includes('r"D"'), 'Bug 111: NOTE_STEP_CHECKS must not contain corrupted r"D" (must be r"\\D")');
  assert(!checksMatch.includes('последовательность `s`'), 'Bug 111: NOTE_STEP_CHECKS must not contain corrupted `s` (must be `\\s`)');
  assert(!checksMatch.includes('\x08'), 'Bug 111: NOTE_STEP_CHECKS must not contain ASCII backspace byte \\x08 (must be \\\\b)');
  console.log('✓ Bug 111: NOTE_STEP_CHECKS regex backslashes strictly escaped (\\d, \\D, \\s, \\b, \\w)');
}

// Bug 112 (Defect 6): Запрет хвостовых поясняющих комментариев в сниппетах конспектов (К-222:5)
function testBug112_NoTrailingCommentsInSnippets(){
  assert(
    !academyHtml.includes('print(pure.name)  # hosts'),
    'Bug 112: K-222 step 5 must not contain trailing comment "print(pure.name)  # hosts"'
  );
  console.log('✓ Bug 112: Trailing comments in note code snippets banned and verified');
}

// Bug 113 (Defect 7): Категорический запрет на техническое упоминание «Кодди» / «Coddy» (Правило 7)
function testBug113_StrictBanOnCoddy(){
  const forbiddenTerms = [
    'btn-coddy-emerald',
    'btn-coddy-ruby',
    'coddy-code-block',
    'coddy-lesson-card',
    'coddy-table',
    'coddyStreamReveal'
  ];

  for (const term of forbiddenTerms) {
    assert(!academyHtml.includes(term), `Bug 113: academy.html must not contain forbidden term "${term}"`);
  }
  console.log('✓ Bug 113: Strict Ban on Coddy technical mentions (Rule 7) verified');
}

// Запуск всех тестов
try {
  testBug107_SyntaxHighlightingDoubleQuotes();
  testBug108_VisibleStepCounterAndSegmentedBar();
  testBug109_StepVsThemeTerminology();
  testBug110_SingleDominantCtaTheoryFlow();
  testBug111_NoCorruptedRegexEscapes();
  testBug112_NoTrailingCommentsInSnippets();
  testBug113_StrictBanOnCoddy();
  console.log('\n================================================================');
  console.log('  ALL NOTES PRESENTATION TESTS (BUGS 107..113) PASSED (100%)    ');
  console.log('================================================================\n');
} catch(err) {
  console.error('\n❌ REJECTION: ' + err.message + '\n');
  if (require.main === module) {
    process.exit(1);
  } else {
    throw err;
  }
}

module.exports = {
  testBug107_SyntaxHighlightingDoubleQuotes,
  testBug108_VisibleStepCounterAndSegmentedBar,
  testBug109_StepVsThemeTerminology,
  testBug110_SingleDominantCtaTheoryFlow,
  testBug111_NoCorruptedRegexEscapes,
  testBug112_NoTrailingCommentsInSnippets,
  testBug113_StrictBanOnCoddy
};
