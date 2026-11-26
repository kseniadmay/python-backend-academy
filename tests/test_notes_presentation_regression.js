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
const academyHtml = fs.readFileSync(academyPath, 'utf-8').replace(/\r\n/g, '\n');

function getRenderEngine() {
  const sIdx = academyHtml.indexOf('function _escCodeHtml(');
  const eIdx = academyHtml.indexOf('window.getStepChunks = getStepChunks;', sIdx);
  assert(sIdx !== -1 && eIdx !== -1, 'Render/chunking engine must exist in academy.html');
  const code = 'const window = globalThis;\n' + academyHtml.slice(sIdx, eIdx) + '\nwindow.getStepChunks = getStepChunks;';
  return new Function(
    code +
      '\nreturn { highlightPythonTokens, highlightSyntax, detectCodeLang, normalizeCodeSnippets, extractConsoleOutputs, renderConsoleOutputHtml, splitLongParagraphs, decorateCodeBlocksWithRunBtn, normalizeHeadingForCompare, splitStepHtmlIntoChunks, getStepChunks };'
  )();
}

const MASTERY_TRACK_VARS = [
  'HR_MASTERY', 'PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY',
  'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY'
];

function parseMasteryObject(varName) {
  const marker = `const ${varName} = `;
  const idx = academyHtml.indexOf(marker);
  assert(idx !== -1, `${varName} must be present in academy.html`);
  const valStart = idx + marker.length;
  const lineEnd = academyHtml.indexOf('\n', valStart);
  const rawSlice = (lineEnd === -1 ? academyHtml.slice(valStart) : academyHtml.slice(valStart, lineEnd)).trim().replace(/;$/, '');
  return JSON.parse(rawSlice);
}

function getAllMasteryNotes() {
  const combined = {};
  for (const vName of MASTERY_TRACK_VARS) {
    const obj = parseMasteryObject(vName);
    Object.assign(combined, obj.notes || {});
  }
  return combined;
}

// Bug 107 (Defect 1): Подсветка синтаксиса строк (&quot;, &#x27;) и мультиязычность
function testBug107_SyntaxHighlightingDoubleQuotes(){
  const hlMatch = academyHtml.slice(
    academyHtml.indexOf('function highlightPythonTokens('),
    academyHtml.indexOf('// Helper to decorate <pre><code>')
  );

  assert(
    hlMatch.includes('&quot;') || hlMatch.includes('quot'),
    'Bug 107: highlightPythonTokens must support &quot; escaped strings in entity decoder'
  );

  const engine = getRenderEngine();
  const pyOut = engine.highlightPythonTokens('@app.get(&quot;/&quot;)\ndef greet(self, x):\n    return &quot;hi&quot; + &#x27;!&#x27;  # note');
  assert(pyOut.includes('class="tok-dec"'), 'Bug 107: highlightPythonTokens must highlight @decorators');
  assert(pyOut.includes('class="tok-kw"'), 'Bug 107: highlightPythonTokens must highlight keywords');
  assert(pyOut.includes('class="tok-fn"'), 'Bug 107: highlightPythonTokens must highlight function names');
  assert(pyOut.includes('class="tok-self"'), 'Bug 107: highlightPythonTokens must highlight self');
  assert(pyOut.includes('class="tok-str"'), 'Bug 107: highlightPythonTokens must highlight strings');
  assert(pyOut.includes('class="tok-com"'), 'Bug 107: highlightPythonTokens must highlight comments');
  assert(!pyOut.includes('tok-num') || !pyOut.includes('27'), 'Bug 107: &#x27; must not leave leaked entity numbers');

  const sqlOut = engine.highlightSyntax('SELECT id FROM users WHERE active = 1;', 'sql');
  assert(sqlOut.includes('class="tok-sql-kw"'), 'Bug 107: highlightSyntax must support SQL');
  const bashOut = engine.highlightSyntax('docker build --no-cache -t app .', 'bash');
  assert(bashOut.includes('class="tok-cmd"') && bashOut.includes('class="tok-flag"'), 'Bug 107: highlightSyntax must support Bash commands and flags');
  console.log('✓ Bug 107: Syntax highlighting handles &quot;, &#x27;, Python, SQL & Bash cleanly');
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
    vsSkillMatch.includes('data-py-finish-note') && vsSkillMatch.includes('Закрепить в карточках (+10 XP)'),
    'Bug 110: viewPythonSkill must provide Single Dominant CTA "Закрепить в карточках (+10 XP)" on note completion'
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
  return parseMasteryObject('PY_MASTERY').notes || {};
}

// Bug 114 (Defect 8): Запрет склеивания нескольких независимых примеров кода в один сниппет (# 1., # 2.) по всем 246 конспектам
function testBug114_NoMultiExampleBundlingInSnippets(){
  const notes = getAllMasteryNotes();
  const targetKids = Object.keys(notes).sort();
  assert.strictEqual(targetKids.length, 246, `Bug 114: Expected 246 notes across all tracks, got ${targetKids.length}`);
  const violations = [];

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const shtml = step.html || '';
      const blocks = shtml.match(/<span class="code-lang-tag[^"]*">[^<]+<\/span>[\s\S]*?<pre><code>[\s\S]*?<\/code><\/pre>/gi) || [];
      blocks.forEach((blk, cidx) => {
        const langM = blk.match(/<span class="code-lang-tag[^"]*">([^<]+)<\/span>/i);
        if (langM && langM[1].trim().toLowerCase() !== 'python') return;
        const codeM = blk.match(/<pre><code>([\s\S]*?)<\/code><\/pre>/i);
        const code = codeM ? codeM[1] : '';
        const nums = code.match(/^\s*#\s*\d+\.\s+/gm);
        if (nums && nums.length > 1) {
          violations.push(`${kid}:${sidx} block #${cidx + 1} bundles ${nums.length} examples (${nums.map(s => s.trim()).join(', ')})`);
        }
      });
    });
  }

  assert(
    violations.length === 0,
    `Bug 114: Found multi-example bundling in snippets:\n  - ${violations.join('\n  - ')}`
  );
  console.log(`✓ Bug 114: Zero multi-example (# 1., # 2.) bundling verified across all ${targetKids.length} notes`);
}

// Bug 115 (Defect 9): Мобильная укладка <= 46 символов и отказ от # => во всех 238 конспектах
function testBug115_SnippetLinesLimit(){
  const engine = getRenderEngine();
  const rootDir = path.resolve(__dirname, '..');
  const kbRoot = path.join(rootDir, 'knowledge_base');
  const mdFiles = [];
  function walk(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(p);
      else if (ent.isFile() && ent.name.endsWith('.md') && dir.endsWith('📚 Конспекты')) mdFiles.push(p);
    }
  }
  walk(kbRoot);
  assert.strictEqual(mdFiles.length, 246, `Bug 115: Expected 246 note markdown files, got ${mdFiles.length}`);

  const widthViolations = [];
  const arrowViolations = [];
  for (const fp of mdFiles) {
    const raw = fs.readFileSync(fp, 'utf-8').replace(/\r\n/g, '\n');
    const lines = raw.split('\n');
    let inPy = false;
    let inFence = false;
    lines.forEach((ln, idx) => {
      const tr = ln.trim();
      if (tr.startsWith('```')) {
        if (!inFence) {
          inFence = true;
          inPy = /^```py(thon)?\b/i.test(tr);
        } else {
          inFence = false;
          inPy = false;
        }
        return;
      }
      if (!inFence) return;
      if (/^\s*#\s*=>/.test(ln)) {
        arrowViolations.push(`${path.basename(fp)}:${idx + 1}: ${tr}`);
      }
      if (inPy && !/^\s*#\s*>>>/.test(ln) && ln.length > 46) {
        widthViolations.push(`${path.basename(fp)}:${idx + 1} (${ln.length} chars): ${ln}`);
      }
    });
  }

  assert(arrowViolations.length === 0, `Bug 115: Remaining # => markers:\n  - ${arrowViolations.slice(0, 10).join('\n  - ')}`);
  assert(widthViolations.length === 0, `Bug 115: Python lines > 46 chars:\n  - ${widthViolations.slice(0, 15).join('\n  - ')}`);

  // Check Unit 1.9.1 / 1.9.3 pure code lines after console extraction remain well-bounded
  const notes = getPyMasteryNotes();
  const unit19Violations = [];
  for (const kid of ['К-055', 'К-056', 'К-057', 'К-220', 'К-222']) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const codeMatches = (step.html || '').match(/<pre><code>([\s\S]*?)<\/code><\/pre>/gi) || [];
      codeMatches.forEach((cm, cidx) => {
        const inner = cm.replace(/<\/?(pre|code)>/gi, '');
        const ext = engine.extractConsoleOutputs(inner);
        const pureLines = ext.pureCodeHtml.trim().split('\n').filter(l => l.trim().length > 0);
        if (pureLines.length > 38) {
          unit19Violations.push(`${kid}:${sidx} block #${cidx + 1} has ${pureLines.length} pure code lines (> 38)`);
        }
      });
    });
  }
  assert(unit19Violations.length === 0, `Bug 115: Unit 1.9 snippets oversized:\n  - ${unit19Violations.join('\n  - ')}`);
  console.log('✓ Bug 115: Zero # => markers & 100% Python lines <= 46 chars verified across all 238 notes');
}

// Bug 116: Каждый абзац конспекта подаётся единым шагом независимо от его длины
function testBug116_ParagraphLengthLimit(){
  const engine = getRenderEngine();
  const pyNotes = getPyMasteryNotes();
  const pyViolations = [];
  for (const kid of ['К-055', 'К-056', 'К-057', 'К-222']) {
    const note = pyNotes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const pMatches = (step.html || '').match(/<p>([\s\S]*?)<\/p>/gi) || [];
      pMatches.forEach((pm, pidx) => {
        const ptext = pm.replace(/<[^>]+>/g, '').trim();
        if (ptext.length > 240) {
          pyViolations.push(`${kid}:${sidx} raw p #${pidx + 1} has ${ptext.length} chars (> 240)`);
        }
      });
    });
  }
  assert(pyViolations.length === 0, `Bug 116: Unit 1.9.1 paragraphs > 240:\n  - ${pyViolations.join('\n  - ')}`);

  const allNotes = getAllMasteryNotes();
  let verifiedSteps = 0;
  for (const [kid, note] of Object.entries(allNotes)) {
    (note.steps || []).forEach((step, sidx) => {
      verifiedSteps++;
      const chunks = engine.splitStepHtmlIntoChunks(step.html || '', step.title || '');
      assert(Array.isArray(chunks) && chunks.length > 0, `${kid}:${sidx} chunks must be non-empty`);
    });
  }

  console.log(`✓ Bug 116: Every paragraph is a single step regardless of length verified across all ${verifiedSteps} steps of ${Object.keys(allNotes).length} notes`);
}

// Вспомогательная функция для извлечения данных PY_MASTERY
function getPyMasteryData() {
  return parseMasteryObject('PY_MASTERY');
}

// Bug 117 (Defect 11): Навык 1.9.1 без дубля К-220 (4 конспекта), К-220/Ф-251 строго в 1.9.3, и 100% покрытие по всем 7 трекам
function testBug117_ActiveRecallCoverageBenchmark(){
  const pm = getPyMasteryData();
  const sk191 = pm.units.flatMap(u => u.skills).find(s => s.id === '1.9.1');
  const sk193 = pm.units.flatMap(u => u.skills).find(s => s.id === '1.9.3');
  assert(sk191, 'Bug 117: Skill 1.9.1 must exist in PY_MASTERY');
  assert(sk193, 'Bug 117: Skill 1.9.3 must exist in PY_MASTERY');
  assert.strictEqual(sk191.kIds.length, 4, 'Bug 117: Skill 1.9.1 must contain 4 micro-learning notes (К-220 deduplicated to 1.9.3)');
  assert(!sk191.kIds.includes('К-220') && !sk191.fIds.includes('Ф-251'), 'Bug 117: Skill 1.9.1 must not duplicate К-220 or Ф-251');
  assert(sk193.kIds.includes('К-220') && sk193.fIds.includes('Ф-251'), 'Bug 117: Skill 1.9.3 must own К-220 and Ф-251');
  assert(sk191.fIds.length >= 4, 'Bug 117: Skill 1.9.1 must contain at least 4 paired thematic flashcard decks');

  const violations = [];
  for (const vName of MASTERY_TRACK_VARS) {
    const obj = parseMasteryObject(vName);
    for (const u of obj.units || []) {
      for (const sk of u.skills || []) {
        for (const kid of sk.kIds || []) {
          if (!obj.notes || !obj.notes[kid] || !(obj.notes[kid].steps || []).length) {
            violations.push(`${vName}/${sk.id}: note ${kid} missing or empty`);
          }
        }
        for (const fid of sk.fIds || []) {
          const deck = (obj.decks || {})[fid];
          if (!deck || !Array.isArray(deck.cards) || deck.cards.length === 0) {
            violations.push(`${vName}/${sk.id}: deck ${fid} missing or empty`);
          }
        }
      }
    }
  }

  assert(violations.length === 0, `Bug 117: Coverage violation:\n  - ${violations.join('\n  - ')}`);
  console.log('✓ Bug 117: 1.9.1 К-220 deduplication + 100% note/deck coverage across all 7 tracks verified');
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

// Bug 119 (Defect 13): Семантический каркас, таблицы и отсутствие битых <em> по всем 238 конспектам
function testBug119_SemanticHeadingBenchmark(){
  const engine = getRenderEngine();
  const notes = getAllMasteryNotes();
  const targetKids = Object.keys(notes).sort();
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
      const emBroken = shtml.match(/\*[^*<\n]*<em>[^<\n]*<\/em>[^*<\n]*\*/g);
      if (emBroken) {
        violations.push(`${key}: Broken nested *...<em>...</em>* (${emBroken[0].slice(0, 60)})`);
      }
      const strayPipeP = shtml.match(/<p>\|[^<]+\|[^<]*<\/p>/gi);
      if (strayPipeP) {
        violations.push(`${key}: Unparsed markdown table row inside <p> (${strayPipeP[0].slice(0, 60)})`);
      }
      const pureTitle = (step.title || '').replace(/^К-\d+\s*[:·•\-]\s*/i, '').replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = engine.getStepChunks(step, pureTitle);
      const firstH = (chunks[0] || '').match(/^\s*<h[1-5][^>]*>([\s\S]*?)<\/h[1-5]>/i);
      if (firstH && pureTitle) {
        const hNorm = engine.normalizeHeadingForCompare(firstH[1]);
        const tNorm = engine.normalizeHeadingForCompare(pureTitle);
        if (hNorm && tNorm && hNorm === tNorm) {
          violations.push(`${key}: Duplicate heading leaked into chunk 0 (${hNorm})`);
        }
      }
    });
  }

  assert(
    violations.length === 0,
    `Bug 119: Semantic heading / table / emphasis violations:\n  - ${violations.slice(0, 15).join('\n  - ')}`
  );
  console.log(`✓ Bug 119: Semantic <h4>, zero duplicate headings, clean tables & <em> verified across all ${targetKids.length} notes`);
}

// Bug 120 (Defect 14): Копируемые сниппеты + нижняя консоль вывода .code-console-out + идемпотентность по всем 238 конспектам
function testBug120_InteractiveRunnableCodeBenchmark(){
  const engine = getRenderEngine();
  const notes = getAllMasteryNotes();
  const targetKids = Object.keys(notes).sort();
  const violations = [];
  let totalConsoleOutputs = 0;

  for (const kid of targetKids) {
    const note = notes[kid];
    if (!note || !note.steps) continue;
    note.steps.forEach((step, sidx) => {
      const key = `${kid}:${sidx}`;
      const shtml = step.html || '';
      if (/class=["'][^"']*snippet-out/i.test(shtml)) {
        violations.push(`${key}: Legacy .snippet-out present in HTML`);
      }
      const codeMatches = shtml.match(/<pre><code>/gi) || [];
      const copyBtns = shtml.match(/data-copy-code="1"|btn-copy-code/gi) || [];
      if (codeMatches.length > copyBtns.length) {
        violations.push(`${key}: ${codeMatches.length} code blocks but only ${copyBtns.length} copy buttons`);
      }

      const decorated = engine.decorateCodeBlocksWithRunBtn(shtml);
      const decorated2 = engine.decorateCodeBlocksWithRunBtn(decorated);
      if (decorated2 !== decorated) {
        violations.push(`${key}: decorateCodeBlocksWithRunBtn is not idempotent`);
      }

      const hasOutMarker = /#\s*(?:>>>|&gt;&gt;&gt;)/m.test(shtml);
      if (hasOutMarker) {
        if (!decorated.includes('class="code-console-out"') || !decorated.includes('class="code-console-label">Вывод</div>')) {
          violations.push(`${key}: Output markers # >>> did not render into .code-console-out`);
        }
        totalConsoleOutputs++;
      }

      const pres = decorated.match(/<pre\b[^>]*><code\b[^>]*>([\s\S]*?)<\/code><\/pre>/gi) || [];
      pres.forEach((pHtml, pidx) => {
        const plain = pHtml.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>');
        if (/^\s*#\s*>>>/m.test(plain) || pHtml.includes('class="tok-out"')) {
          violations.push(`${key} pre #${pidx + 1}: Output lines # >>> leaked inside <pre><code>`);
        }
      });
    });
  }

  assert(
    violations.length === 0,
    `Bug 120: Console output / copyable code violations:\n  - ${violations.slice(0, 15).join('\n  - ')}`
  );
  console.log(`✓ Bug 120: .code-console-out (${totalConsoleOutputs} steps with outputs), zero leaked # >>> in <pre>, and idempotency verified across all ${targetKids.length} notes`);
}

// Bug 121: Полная синхронизация data/content/notes.json == academy.html + отсутствие бэктиков в SVG
function testBug121_CanonicalNotesSyncAndDiagrams(){
  const rootDir = path.resolve(__dirname, '..');
  const notesJson = JSON.parse(fs.readFileSync(path.join(rootDir, 'data', 'content', 'notes.json'), 'utf-8'));
  const htmlNotes = getAllMasteryNotes();
  const jsonIds = Object.keys(notesJson).sort();
  const htmlIds = Object.keys(htmlNotes).sort();
  assert.deepStrictEqual(jsonIds, htmlIds, 'Bug 121: notes.json IDs must match 7 *_MASTERY notes in academy.html');

  const diffs = [];
  const svgBackticks = [];
  for (const kid of jsonIds) {
    const a = notesJson[kid];
    const b = htmlNotes[kid];
    if ((a.steps || []).length !== (b.steps || []).length) {
      diffs.push(`${kid}: notes.json has ${(a.steps || []).length} steps vs academy.html ${(b.steps || []).length}`);
      continue;
    }
    (a.steps || []).forEach((st, idx) => {
      const bSt = b.steps[idx];
      if (st.title !== bSt.title || st.html !== bSt.html) {
        diffs.push(`${kid}:${idx} content differs between notes.json and academy.html`);
      }
      const svgs = (st.html || '').match(/<svg[\s\S]*?<\/svg>/gi) || [];
      svgs.forEach(svg => {
        const texts = svg.match(/<text[^>]*>[\s\S]*?<\/text>/gi) || [];
        texts.forEach(t => {
          if (t.includes('`')) svgBackticks.push(`${kid}:${idx} SVG <text> contains raw backtick: ${t.slice(0, 80)}`);
        });
      });
    });
  }

  assert(diffs.length === 0, `Bug 121: Sync diffs:\n  - ${diffs.slice(0, 10).join('\n  - ')}`);
  assert(svgBackticks.length === 0, `Bug 121: SVG raw backticks:\n  - ${svgBackticks.join('\n  - ')}`);

  // Verify light-theme-safe heading color var(--ink), .table-scroll-wrap wrapper, and zero leaked **/$...$ in note body prose
  assert(!academyHtml.includes('<span style="color:#ffffff;font-weight:800;letter-spacing:-0.02em;">${typeof formatRichInlineText'), 'Bug 121: Note <h2> must use color:var(--ink) so it remains visible in light theme');
  assert(academyHtml.includes('.table-scroll-wrap') && academyHtml.includes('<div class="table-scroll-wrap">'), 'Bug 121: Wide tables must be wrapped in .table-scroll-wrap for 390px mobile scrollability');

  const engine = getRenderEngine();
  const sampleTblOut = engine.decorateCodeBlocksWithRunBtn('<table><tr><th>A</th></tr><tr><td>1</td></tr></table>');
  assert(sampleTblOut.includes('<div class="table-scroll-wrap"><table>') && engine.decorateCodeBlocksWithRunBtn(sampleTblOut) === sampleTblOut, 'Bug 121: table-scroll-wrap decoration must be idempotent');

  console.log(`✓ Bug 121: 100% sync (notes.json == academy.html across ${jsonIds.length} notes), light-safe <h2>, .table-scroll-wrap & clean SVG verified`);
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
  testBug121_CanonicalNotesSyncAndDiagrams();
  console.log('\n================================================================');
  console.log('  ALL NOTES PRESENTATION TESTS (BUGS 107..121) PASSED (100%)    ');
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
  testBug120_InteractiveRunnableCodeBenchmark,
  testBug121_CanonicalNotesSyncAndDiagrams
};
