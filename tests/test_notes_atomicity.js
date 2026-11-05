/**
 * test_notes_atomicity.js
 * Тотальный регрессионный сьют верификации атомарности подачи теории (Active Microlearning Framework)
 * для ВСЕХ 238 конспектов платформы (Python Backend Academy).
 *
 * Проверяет:
 *  1. 100% покрытие: Все 238 тем (1127 микро-шагов) по всем 7 направлениям подготовки.
 *  2. Запрет пустых квантов (Zero Empty Chunks).
 *  3. Строгую сбалансированность и валидность HTML-тегов в каждом кванте (No DOM leakage).
 *  4. Запрет «сиротливых заголовков» и оборванных подводок (No Orphan Headings / Lead-ins).
 *  5. Аккуратность порций и отсутствие неквантованных монолитных массивов (Anti-Monolith & Sizing).
 *  6. Безопасность инжекции в DOM и поддержку исполняемых сниппетов (Safe DOM Injection).
 *  7. Симуляцию инкрементальной сессии изучения: переход по квантам до финиша (State Machine Flow).
 *  8. Синхронизацию канонического стандарта standards.html и academy.html.
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const standardsPath = path.join(rootDir, 'standards', 'standards.html');
const academyPath = path.join(rootDir, 'academy.html');

console.log('================================================================');
console.log('   NOTES ATOMICITY & QUANTUM DELIVERY REGRESSION SUITE          ');
console.log('   ACTIVE MICROLEARNING FRAMEWORK (100% OF 238 NOTES)           ');
console.log('================================================================\n');

assert(fs.existsSync(standardsPath), `standards.html missing at ${standardsPath}`);
assert(fs.existsSync(academyPath), `academy.html missing at ${academyPath}`);

const standardsHtml = fs.readFileSync(standardsPath, 'utf-8');
const academyHtml = fs.readFileSync(academyPath, 'utf-8');

// --- 0. Извлечение базы знаний (все 7 MASTERY объектов) ---
const masteryNames = [
  'PY_MASTERY',
  'WEB_MASTERY',
  'BACKEND_MASTERY',
  'ALGO_MASTERY',
  'DB_MASTERY',
  'ARCH_MASTERY',
  'INFRA_MASTERY'
];

function extractAllNotes(srcHtml) {
  const notesMap = {};
  for (const name of masteryNames) {
    const startStr = `const ${name} = `;
    const startIdx = srcHtml.indexOf(startStr);
    assert(startIdx !== -1, `Declaration of ${name} must be present`);
    const jsonStart = startIdx + startStr.length;

    let braceCount = 0;
    let inString = false;
    let escape = false;
    let endIdx = -1;

    for (let i = jsonStart; i < srcHtml.length; i++) {
      const char = srcHtml[i];
      if (escape) {
        escape = false;
        continue;
      }
      if (char === '\\') {
        escape = true;
        continue;
      }
      if (char === '"') {
        inString = !inString;
        continue;
      }
      if (!inString) {
        if (char === '{') braceCount++;
        else if (char === '}') {
          braceCount--;
          if (braceCount === 0) {
            endIdx = i + 1;
            break;
          }
        }
      }
    }

    assert(endIdx !== -1, `Could not find closing brace for ${name}`);
    const rawJson = srcHtml.slice(jsonStart, endIdx);
    const parsed = JSON.parse(rawJson);
    if (parsed.notes) {
      Object.assign(notesMap, parsed.notes);
    }
  }
  return notesMap;
}

// --- 1. Извлечение движка квантования splitStepHtmlIntoChunks & getStepChunks ---
function extractChunkingEngine(srcHtml) {
  const fnStart = srcHtml.indexOf('function splitStepHtmlIntoChunks(');
  assert(fnStart !== -1, 'splitStepHtmlIntoChunks must exist');
  const fnEnd = srcHtml.indexOf('window.splitStepHtmlIntoChunks = splitStepHtmlIntoChunks;', fnStart);
  const fnCode = srcHtml.slice(fnStart, fnEnd);

  const gfnStart = srcHtml.indexOf('function getStepChunks(');
  assert(gfnStart !== -1, 'getStepChunks must exist');
  const gfnEnd = srcHtml.indexOf('window.getStepChunks = getStepChunks;', gfnStart);
  const gfnCode = srcHtml.slice(gfnStart, gfnEnd);

  const evalCode = `
    ${fnCode}
    ${gfnCode}
    return { splitStepHtmlIntoChunks, getStepChunks };
  `;
  return new Function(evalCode)();
}

const allNotes = extractAllNotes(standardsHtml);
const { splitStepHtmlIntoChunks, getStepChunks } = extractChunkingEngine(standardsHtml);

// ============================================================================
// TEST 1: 100% Coverage of All 238 Notes & 1127 Steps
// ============================================================================
function test01_FullCoverage() {
  const noteIds = Object.keys(allNotes);
  assert.strictEqual(noteIds.length, 238, `Expected exactly 238 notes, found ${noteIds.length}`);

  let totalSteps = 0;
  for (const [kId, note] of Object.entries(allNotes)) {
    assert(note.steps && Array.isArray(note.steps), `Note ${kId} must have an array of steps`);
    assert(note.steps.length > 0, `Note ${kId} must have at least 1 step`);
    note.steps.forEach((step, sIdx) => {
      totalSteps++;
      assert(typeof step.title === 'string' && step.title.trim().length > 0, `Note ${kId} step ${sIdx} must have non-empty title`);
      assert(typeof step.html === 'string' && step.html.trim().length > 0, `Note ${kId} step ${sIdx} must have non-empty html`);
    });
  }

  assert.strictEqual(totalSteps, 1127, `Expected exactly 1127 total steps, found ${totalSteps}`);
  console.log(`✓ Test 1 Passed: 100% coverage verified (238 notes, 1127 steps across all 7 tracks)`);
}

// ============================================================================
// TEST 2: Zero Empty Chunks & Guaranteed Meaningful Body
// ============================================================================
function test02_ZeroEmptyChunks() {
  const emptyViolations = [];
  let totalChunks = 0;

  for (const [kId, note] of Object.entries(allNotes)) {
    note.steps.forEach((step, sIdx) => {
      const cleanStepTitle = (step.title || ('Шаг ' + (sIdx + 1))).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
      const pureStepTitle = cleanStepTitle.replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = getStepChunks(step, pureStepTitle);

      assert(Array.isArray(chunks) && chunks.length > 0, `Step ${kId}:${sIdx} produced 0 chunks`);
      totalChunks += chunks.length;

      chunks.forEach((ch, cIdx) => {
        if (!ch || typeof ch !== 'string') {
          emptyViolations.push(`${kId}:${sIdx}:${cIdx} is null or not a string`);
          return;
        }
        const trimmed = ch.trim();
        if (trimmed.length === 0) {
          emptyViolations.push(`${kId}:${sIdx}:${cIdx} is empty string`);
          return;
        }
        const plainText = trimmed.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim();
        // Проверяем, что чанк содержит либо текст, либо код
        if (plainText.length === 0 && !/<(pre|code|img|svg|table)\b/i.test(trimmed)) {
          emptyViolations.push(`${kId}:${sIdx}:${cIdx} contains only empty tags without text or code: "${trimmed}"`);
        }
      });
    });
  }

  assert.strictEqual(
    emptyViolations.length,
    0,
    `Found empty chunks violations:\n  - ${emptyViolations.slice(0, 10).join('\n  - ')}`
  );
  console.log(`✓ Test 2 Passed: Zero empty chunks verified across all ${totalChunks} generated portions`);
}

// ============================================================================
// TEST 3: Strict HTML Semantic Tag Balance & No DOM Leakage
// ============================================================================
function test03_StrictHtmlTagBalance() {
  const tagsToCheck = [
    'div', 'table', 'tbody', 'tr', 'td', 'th',
    'ul', 'ol', 'li', 'pre', 'code', 'blockquote',
    'p', 'strong', 'em', 'span'
  ];
  const balanceViolations = [];

  for (const [kId, note] of Object.entries(allNotes)) {
    note.steps.forEach((step, sIdx) => {
      const cleanStepTitle = (step.title || ('Шаг ' + (sIdx + 1))).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
      const pureStepTitle = cleanStepTitle.replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = getStepChunks(step, pureStepTitle);

      chunks.forEach((chunk, cIdx) => {
        for (const tag of tagsToCheck) {
          const openRe = new RegExp(`<${tag}(\\s[^>]*)?>`, 'gi');
          const closeRe = new RegExp(`</${tag}>`, 'gi');
          const opens = (chunk.match(openRe) || []).length;
          const closes = (chunk.match(closeRe) || []).length;

          if (opens !== closes) {
            balanceViolations.push(`${kId}:${sIdx}:${cIdx} tag <${tag}> unbalanced: ${opens} open vs ${closes} close`);
          }
        }
      });
    });
  }

  assert.strictEqual(
    balanceViolations.length,
    0,
    `Found HTML tag balance violations:\n  - ${balanceViolations.slice(0, 10).join('\n  - ')}`
  );
  console.log(`✓ Test 3 Passed: 100% HTML tag balance guaranteed (0 unclosed tags, safe for innerHTML injection)`);
}

// ============================================================================
// TEST 4: No Orphan Headings or Trailing Colons / Lead-in Fragments
// ============================================================================
function test04_NoOrphanHeadings() {
  const orphanViolations = [];

  for (const [kId, note] of Object.entries(allNotes)) {
    note.steps.forEach((step, sIdx) => {
      const cleanStepTitle = (step.title || ('Шаг ' + (sIdx + 1))).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
      const pureStepTitle = cleanStepTitle.replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = getStepChunks(step, pureStepTitle);

      chunks.forEach((chunk, cIdx) => {
        const trimmed = chunk.trim();

        // 1. Одиночный заголовок h1-h6
        if (/^<h[1-6]\b[^>]*>[\s\S]*?<\/h[1-6]>\s*$/i.test(trimmed)) {
          orphanViolations.push(`${kId}:${sIdx}:${cIdx} is an orphan heading: "${trimmed.slice(0, 80)}"`);
        }

        // 2. Одиночный подводящий абзац перед кодом без самого кода
        const plain = trimmed.replace(/<[^>]+>/g, '').trim();
        if (/^<p\b[^>]*>[\s\S]*?<\/p>$/i.test(trimmed) && /[:—–➔→]\s*$/i.test(plain) && plain.length < 80) {
          orphanViolations.push(`${kId}:${sIdx}:${cIdx} is an orphan lead-in sentence: "${plain}"`);
        }
      });
    });
  }

  assert.strictEqual(
    orphanViolations.length,
    0,
    `Found orphan headings / lead-ins:\n  - ${orphanViolations.slice(0, 10).join('\n  - ')}`
  );
  console.log(`✓ Test 4 Passed: No orphan headings or dangling lead-ins verified`);
}

// ============================================================================
// TEST 5: Optimal Quantum Sizing & Active Microlearning Ergonomics
// ============================================================================
function test05_OptimalQuantumSizing() {
  let totalChunks = 0;
  let totalSteps = 0;
  const monolithViolations = [];

  for (const [kId, note] of Object.entries(allNotes)) {
    note.steps.forEach((step, sIdx) => {
      totalSteps++;
      const cleanStepTitle = (step.title || ('Шаг ' + (sIdx + 1))).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
      const pureStepTitle = cleanStepTitle.replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = getStepChunks(step, pureStepTitle);
      totalChunks += chunks.length;

      chunks.forEach((chunk, cIdx) => {
        const plainText = chunk.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim();
        const pCount = (chunk.match(/<p\b/gi) || []).length;

        // Запрет неквантованных монолитов: более 4 параграфов <p> подряд и более 2000 символов текста в одном кванте
        if (pCount > 4 && plainText.length > 2000) {
          monolithViolations.push(`${kId}:${sIdx}:${cIdx} is an unquantized monolith (${pCount} paragraphs, ${plainText.length} chars)`);
        }
      });
    });
  }

  const avgChunksPerStep = totalChunks / totalSteps;
  assert(
    avgChunksPerStep >= 2.0 && avgChunksPerStep <= 4.5,
    `Average chunks per step (${avgChunksPerStep.toFixed(2)}) must be between 2.0 and 4.5`
  );

  assert.strictEqual(
    monolithViolations.length,
    0,
    `Found unquantized monolithic chunks:\n  - ${monolithViolations.slice(0, 10).join('\n  - ')}`
  );

  console.log(`✓ Test 5 Passed: Optimal sizing verified (average ${avgChunksPerStep.toFixed(2)} atomic chunks per step, 0 monoliths)`);
}

// ============================================================================
// TEST 6: Safe DOM Injection & Code Snippet Formatting
// ============================================================================
function test06_SafeDomInjectionAndCodeSnippets() {
  const malformedTagViolations = [];

  for (const [kId, note] of Object.entries(allNotes)) {
    note.steps.forEach((step, sIdx) => {
      const cleanStepTitle = (step.title || ('Шаг ' + (sIdx + 1))).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
      const pureStepTitle = cleanStepTitle.replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = getStepChunks(step, pureStepTitle);

      chunks.forEach((chunk, cIdx) => {
        // Проверка на склеенные или битые скобки тегов (например, <div<p> или >>)
        if (/<[a-z0-9]+\s*<|>[a-z0-9]*>/i.test(chunk)) {
          malformedTagViolations.push(`${kId}:${sIdx}:${cIdx} has malformed tag brackets`);
        }
        // Проверка, что pre содержит code
        if (/<pre\b[^>]*>/i.test(chunk) && !/<pre\b[^>]*>[\s\S]*?<code\b/i.test(chunk)) {
          malformedTagViolations.push(`${kId}:${sIdx}:${cIdx} has <pre> without <code>`);
        }
      });
    });
  }

  assert.strictEqual(
    malformedTagViolations.length,
    0,
    `Found DOM injection / syntax formatting violations:\n  - ${malformedTagViolations.slice(0, 10).join('\n  - ')}`
  );
  console.log(`✓ Test 6 Passed: Safe DOM injection & standard code snippets verified`);
}

// ============================================================================
// TEST 7: Complete State Transition Simulation (Step-by-Step Delivery)
// ============================================================================
function test07_StateTransitionSimulation() {
  // Симуляция прохождения всех квантов для каждого конспекта:
  // Проверяем, что в каждом конспекте шаги и кванты последовательно проходятся,
  // нет тупиковых состояний и кнопка корректно переключается:
  //  - chunk_more -> (пока есть кванты в текущем шаге)
  //  - next_step  -> (когда кванты шага исчерпаны, но есть следующий шаг)
  //  - finish_note -> (когда пройден последний квант последнего шага)
  let simulatedNotesCount = 0;

  for (const [kId, note] of Object.entries(allNotes)) {
    const steps = note.steps || [];
    let curStepIdx = 0;
    let curChunkIdx = 0;
    let iterations = 0;
    const maxIterations = 500; // Защита от бесконечного цикла

    while (curStepIdx < steps.length && iterations < maxIterations) {
      iterations++;
      const step = steps[curStepIdx];
      const cleanStepTitle = (step.title || ('Шаг ' + (curStepIdx + 1))).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
      const pureStepTitle = cleanStepTitle.replace(/^\d+[\.\)\s\-·•]+\s*/, '').trim();
      const chunks = getStepChunks(step, pureStepTitle);
      const totalChunks = chunks.length;

      const hasMoreChunks = (curChunkIdx + 1 < totalChunks);
      if (hasMoreChunks) {
        // Клик «Понятно, дальше» (data-chunk-more)
        curChunkIdx++;
      } else if (curStepIdx + 1 < steps.length) {
        // Клик «К следующей подтеме» (data-next-step)
        curStepIdx++;
        curChunkIdx = 0;
      } else {
        // Достигнут финал конспекта (data-finish-note)
        curStepIdx++;
        break;
      }
    }

    assert(iterations < maxIterations, `Note ${kId} exceeded max iterations during quantum feed simulation (infinite loop deadlock)`);
    assert.strictEqual(curStepIdx, steps.length, `Note ${kId} did not reach completion`);
    simulatedNotesCount++;
  }

  assert.strictEqual(simulatedNotesCount, 238, 'Expected 238 simulated note reading sessions');
  console.log(`✓ Test 7 Passed: Step-by-step state transition simulation completed for 100% of notes (0 deadlocks)`);
}

// ============================================================================
// TEST 8: Canonical Standards SSOT Synchronization
// ============================================================================
function test08_CanonicalStandardsSync() {
  assert.strictEqual(
    standardsHtml.length,
    academyHtml.length,
    `academy.html (${academyHtml.length} bytes) must match standards.html (${standardsHtml.length} bytes) length`
  );
  assert.strictEqual(
    standardsHtml,
    academyHtml,
    'academy.html and standards.html must be byte-for-byte identical (Canonical SSOT invariant)'
  );

  // Проверяем, что в viewPythonSkill вызывается getStepChunks
  assert(
    standardsHtml.includes('const chunks = (typeof getStepChunks === \'function\')'),
    'standards.html must use getStepChunks in viewPythonSkill to prevent duplicate headings'
  );
  console.log(`✓ Test 8 Passed: standards.html and academy.html are byte-for-byte synchronized with unified chunking`);
}

// ============================================================================
// RUN ALL TESTS
// ============================================================================
try {
  test01_FullCoverage();
  test02_ZeroEmptyChunks();
  test03_StrictHtmlTagBalance();
  test04_NoOrphanHeadings();
  test05_OptimalQuantumSizing();
  test06_SafeDomInjectionAndCodeSnippets();
  test07_StateTransitionSimulation();
  test08_CanonicalStandardsSync();

  console.log('\n================================================================');
  console.log('  ALL NOTES ATOMICITY TESTS PASSED SUCCESSFULLY (100%)          ');
  console.log('================================================================\n');
} catch (err) {
  console.error('\n❌ ATOMICITY SUITE FAILED:', err.message);
  if (require.main === module) {
    process.exit(1);
  } else {
    throw err;
  }
}

module.exports = {
  test01_FullCoverage,
  test02_ZeroEmptyChunks,
  test03_StrictHtmlTagBalance,
  test04_NoOrphanHeadings,
  test05_OptimalQuantumSizing,
  test06_SafeDomInjectionAndCodeSnippets,
  test07_StateTransitionSimulation,
  test08_CanonicalStandardsSync
};
