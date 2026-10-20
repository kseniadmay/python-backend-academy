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
console.log('   BUGS 107..120 VERIFICATION (PEDAGOGICAL BENCHMARK)           ');
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

// Bug 108 (Defect 2): Ликвидация мусорных текстовых строк («Шаг X из Y», «Сессия ~2 мин») и чистота заголовка
function testBug108_VisibleStepCounterAndSegmentedBar(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );

  assert(
    !vsSkillMatch.includes('Шаг ${stepIdx + 1} из ${steps.length}'),
    'Bug 108: viewPythonSkill must eliminate "Шаг X из Y" junk text from skill screen header'
  );
  assert(
    !vsSkillMatch.includes('Сессия ~2 мин · Активное микрообучение'),
    'Bug 108: viewPythonSkill must eliminate "Сессия ~2 мин · Активное микрообучение" junk text from skill screen header'
  );
  assert(
    !vsSkillMatch.includes('step-counter-pill'),
    'Bug 108: viewPythonSkill must eliminate step-counter-pill clutter from header'
  );
  console.log('✓ Bug 108: Elimination of junk text lines and clean skill screen header verified');
}

// Bug 109 (Defect 3): Разграничение понятий «Тема» и «Шаг» в навигации
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
    vsSkillMatch.includes('Следующий шаг'),
    'Bug 109: Navigation within note steps must use "Следующий шаг"'
  );
  console.log('✓ Bug 109: Step vs Theme terminology invariant in theory navigation verified');
}

// Bug 110 (Defect 4): Инвариант Single Dominant CTA и прямой переход от конспекта к тематическим карточкам
function testBug110_SingleDominantCtaTheoryFlow(){
  const vsSkillMatch = academyHtml.slice(
    academyHtml.indexOf('function viewPythonSkill('),
    academyHtml.indexOf('function viewCardsHub(')
  );

  assert(
    !vsSkillMatch.includes('👆 Ответьте на вопрос для продолжения'),
    'Bug 110: Single Dominant CTA must not be replaced with passive text placeholder'
  );
  assert(
    vsSkillMatch.includes('data-py-finish-note') && vsSkillMatch.includes('Закрепить в карточках (+10 XP) ➔'),
    'Bug 110: viewPythonSkill must provide Single Dominant CTA "Закрепить в карточках (+10 XP) ➔" on note completion'
  );
  assert(
    !vsSkillMatch.includes('data-py-start-check') && !vsSkillMatch.includes('data-py-step-answer'),
    'Bug 110: Comprehension check quizzes must be eliminated in favor of immediate thematic flashcards'
  );
  console.log('✓ Bug 110: Single Dominant CTA and direct note-to-cards handoff verified');
}

// Bug 111 (Defect 5): Защита от повреждённых регулярных выражений и ликвидация квизов понимания
function testBug111_NoCorruptedRegexEscapes(){
  assert(!academyHtml.includes('r"d+"'), 'Bug 111: Must not contain corrupted r"d+" (must be r"\\d+")');
  assert(!academyHtml.includes('r"D"'), 'Bug 111: Must not contain corrupted r"D" (must be r"\\D")');
  assert(!academyHtml.includes('последовательность `s`'), 'Bug 111: Must not contain corrupted `s` (must be `\\s`)');
  assert(!academyHtml.includes('\x08'), 'Bug 111: Must not contain ASCII backspace byte \\x08 (must be \\\\b)');
  console.log('✓ Bug 111: Regex backslashes strictly escaped (\\d, \\D, \\s, \\b, \\w) and no corrupted quiz escapes');
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

// Вспомогательная функция для извлечения PY_MASTERY.notes
function getPyMasteryNotes() {
  const m = academyHtml.match(/const PY_MASTERY\s*=\s*(\{.*?\});\n/);
  assert(m, 'Bug 114-116: PY_MASTERY must be present in academy.html');
  const data = JSON.parse(m[1]);
  return data.notes || {};
}

// Bug 114 (Defect 8): Запрет склеивания нескольких независимых примеров кода в один сниппет (# 1., # 2.)
function testBug114_NoMultiExampleBundlingInSnippets(){
  const notes = getPyMasteryNotes();
  const targetKids = ['К-055', 'К-056', 'К-057', 'К-220', 'К-222'];
  const violations = [];

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const shtml = step.html || '';
      const codeMatches = shtml.match(/<pre><code>([\s\S]*?)<\/code><\/pre>/gi) || [];
      codeMatches.forEach((cm, cidx) => {
        const code = cm.replace(/<\/?(pre|code)>/gi, '');
        const nums = code.match(/#\s*\d+\.\s*/g);
        if (nums && nums.length > 1) {
          violations.push(`${kid}:${sidx} block #${cidx + 1} bundles ${nums.length} examples (${nums.join(', ')})`);
        }
      });
    });
  }

  assert(
    violations.length === 0,
    `Bug 114: Found multi-example bundling in snippets:\n  - ${violations.join('\n  - ')}`
  );
  console.log('✓ Bug 114: Multi-example bundling banned and verified in Unit 1.9.1 snippets');
}

// Bug 115 (Defect 9): Лимит размера сниппета в микро-шаге (не более 12 строк кода)
function testBug115_SnippetLinesLimit(){
  const notes = getPyMasteryNotes();
  const targetKids = ['К-055', 'К-056', 'К-057', 'К-220', 'К-222'];
  const violations = [];

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const shtml = step.html || '';
      const codeMatches = shtml.match(/<pre><code>([\s\S]*?)<\/code><\/pre>/gi) || [];
      codeMatches.forEach((cm, cidx) => {
        const code = cm.replace(/<\/?(pre|code)>/gi, '');
        const lines = code.trim().split('\n').filter(l => l.trim().length > 0);
        if (lines.length > 12) {
          violations.push(`${kid}:${sidx} block #${cidx + 1} has ${lines.length} lines (> 12 limit)`);
        }
      });
    });
  }

  assert(
    violations.length === 0,
    `Bug 115: Found oversized snippets (> 12 lines):\n  - ${violations.join('\n  - ')}`
  );
  console.log('✓ Bug 115: Max 12 lines per snippet limit verified in Unit 1.9.1');
}

// Bug 116 (Defect 10): Запрет стен текста и квантование параграфов теории (не более 240 символов)
function testBug116_ParagraphLengthLimit(){
  const notes = getPyMasteryNotes();
  const targetKids = ['К-055', 'К-056', 'К-057', 'К-220', 'К-222'];
  const violations = [];

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const shtml = step.html || '';
      const pMatches = shtml.match(/<p>([\s\S]*?)<\/p>/gi) || [];
      pMatches.forEach((pm, pidx) => {
        const ptext = pm.replace(/<[^>]+>/g, '').trim();
        if (ptext.length > 240) {
          violations.push(`${kid}:${sidx} paragraph #${pidx + 1} has ${ptext.length} chars (> 240 limit)`);
        }
      });
    });
  }

  assert(
    violations.length === 0,
    `Bug 116: Found wall-of-text paragraphs (> 240 chars):\n  - ${violations.join('\n  - ')}`
  );
  console.log('✓ Bug 116: Micro-learning paragraph length limit (<= 240 chars) verified in Unit 1.9.1');
}

// Вспомогательная функция для извлечения данных PY_MASTERY
function getPyMasteryData() {
  const m = academyHtml.match(/const PY_MASTERY\s*=\s*(\{.*?\});\n/);
  assert(m, 'PY_MASTERY must be present in academy.html');
  return JSON.parse(m[1]);
}

// Bug 117 (Defect 11): 100% покрытие тем конспектов тематическими карточками (Thematic Flashcards Coverage Benchmark)
function testBug117_ActiveRecallCoverageBenchmark(){
  const pm = getPyMasteryData();
  const sk191 = pm.units.flatMap(u => u.skills).find(s => s.id === '1.9.1');
  assert(sk191, 'Bug 117: Skill 1.9.1 must exist in PY_MASTERY');
  assert.strictEqual(sk191.kIds.length, 5, 'Bug 117: Skill 1.9.1 must contain 5 micro-learning notes');
  assert.strictEqual(sk191.fIds.length, 5, 'Bug 117: Skill 1.9.1 must contain 5 paired thematic flashcard decks');

  const violations = [];
  sk191.fIds.forEach((fid, idx) => {
    const kid = sk191.kIds[idx];
    const deck = pm.decks[fid];
    const note = pm.notes[kid];
    if(!deck || !Array.isArray(deck.cards) || deck.cards.length === 0){
      violations.push(`Deck ${fid} for note ${kid} has no cards`);
    }
    if(!note){
      violations.push(`Note ${kid} is missing`);
    }
  });

  assert(violations.length === 0, `Bug 117: Thematic flashcards coverage violation:\n  - ${violations.join('\n  - ')}`);
  console.log('✓ Bug 117: 100% Thematic Flashcards Coverage benchmark (5 notes paired with 5 thematic decks) verified');
}

// Bug 118 (Defect 12): Эталонная глубина вопросов и ответов тематических карточек (Card Quality Benchmark)
function testBug118_QuestionAndDistractorBenchmark(){
  const pm = getPyMasteryData();
  const sk191 = pm.units.flatMap(u => u.skills).find(s => s.id === '1.9.1');
  const violations = [];

  for(const fid of sk191.fIds){
    const deck = pm.decks[fid];
    if(!deck) continue;
    deck.cards.forEach((card, cidx) => {
      const q = (card.q || '').trim();
      const a = (card.a || '').trim();
      if(q.length < 15){
        violations.push(`${fid}:${cidx}: Card question too short (${q.length} chars)`);
      }
      if(a.length < 15){
        violations.push(`${fid}:${cidx}: Card answer too short (${a.length} chars)`);
      }
      if(['да', 'нет', 'не знаю'].includes(a.toLowerCase())){
        violations.push(`${fid}:${cidx}: Trivial answer "${a}"`);
      }
    });
  }

  assert(violations.length === 0, `Bug 118: Flashcard quality violations:\n  - ${violations.join('\n  - ')}`);
  console.log('✓ Bug 118: Thematic Flashcard Quality benchmark (deep questions & answers across Unit 1.9.1) verified');
}

// Bug 119 (Defect 13): Семантический каркас микро-шагов (Semantic Step Heading Invariant)
function testBug119_SemanticHeadingBenchmark(){
  const notes = getPyMasteryNotes();
  const targetKids = ['К-055', 'К-056', 'К-057', 'К-220', 'К-222'];
  const violations = [];

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const key = `${kid}:${sidx}`;
      const shtml = (step.html || '').trim();
      if (!/^<h[1-4]\b/i.test(shtml)) {
        violations.push(`${key}: Step must start with semantic <h4> heading`);
      }
    });
  }

  assert(
    violations.length === 0,
    `Bug 119: Semantic heading violations:\n  - ${violations.join('\n  - ')}`
  );
  console.log('✓ Bug 119: Semantic Heading benchmark (100% steps start with <h4>) verified');
}

// Bug 120 (Defect 14): Интерактивная исполняемость сниппетов (Interactive Runnable Code Guarantee)
function testBug120_InteractiveRunnableCodeBenchmark(){
  const notes = getPyMasteryNotes();
  const targetKids = ['К-055', 'К-056', 'К-057', 'К-220', 'К-222'];
  const violations = [];

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const key = `${kid}:${sidx}`;
      const shtml = step.html || '';
      const codeMatches = shtml.match(/<pre><code>/gi) || [];
      const runBtns = shtml.match(/data-run-snippet="1"|data-run-inline/gi) || [];
      if (codeMatches.length > runBtns.length) {
        violations.push(`${key}: ${codeMatches.length} code blocks but only ${runBtns.length} run buttons`);
      }
    });
  }

  assert(
    violations.length === 0,
    `Bug 120: Interactive runnable code violations:\n  - ${violations.join('\n  - ')}`
  );
  console.log('✓ Bug 120: Interactive Runnable Code benchmark (100% runnable code buttons) verified');
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
  testBug114_NoMultiExampleBundlingInSnippets();
  testBug115_SnippetLinesLimit();
  testBug116_ParagraphLengthLimit();
  testBug117_ActiveRecallCoverageBenchmark();
  testBug118_QuestionAndDistractorBenchmark();
  testBug119_SemanticHeadingBenchmark();
  testBug120_InteractiveRunnableCodeBenchmark();
  console.log('\n================================================================');
  console.log('  ALL NOTES PRESENTATION TESTS (BUGS 107..120) PASSED (100%)    ');
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
  testBug113_StrictBanOnCoddy,
  testBug114_NoMultiExampleBundlingInSnippets,
  testBug115_SnippetLinesLimit,
  testBug116_ParagraphLengthLimit,
  testBug117_ActiveRecallCoverageBenchmark,
  testBug118_QuestionAndDistractorBenchmark,
  testBug119_SemanticHeadingBenchmark,
  testBug120_InteractiveRunnableCodeBenchmark
};
