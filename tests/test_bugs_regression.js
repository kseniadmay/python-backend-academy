/**
 * test_bugs_regression.js
 * Автоматические регрессионные тесты для предотвращения повторения багов 1..30.
 */

'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const remnoteDir = path.join(rootDir, 'RemNote_Python_Mastery_FIXED');
const academyPath = path.join(rootDir, 'academy.html');
const etalonyPath = path.join(rootDir, 'Эталоны', 'Эталоны.html');

console.log('================================================================');
console.log('   REGRESSION TEST SUITE: BUGS 1..30 VERIFICATION               ');
console.log('================================================================\n');

assert(fs.existsSync(academyPath), `academy.html missing`);
assert(fs.existsSync(etalonyPath), `Эталоны.html missing`);

const academyHtml = fs.readFileSync(academyPath, 'utf-8');
const etalonyHtml = fs.readFileSync(etalonyPath, 'utf-8');

// 0. Строгая идентичность канонических файлов
assert.strictEqual(academyHtml, etalonyHtml, 'academy.html и Эталоны.html обязаны быть строго побайтово идентичны!');
console.log('✓ Invariant 0: academy.html === Эталоны.html (100% MATCH)');

// 1. Bug 1: Ф-002 card 5: корректность all() и генераторного выражения без списковых скобок
const f002Path = path.join(remnoteDir, '01 · 🐍 Python', 'Юнит 1.1 · Базовый синтаксис', '📇 Карточки', 'Ф-002. Методы проверки вхождения подмножества.md');
assert(fs.existsSync(f002Path), 'Ф-002.md missing');
const f002Content = fs.readFileSync(f002Path, 'utf-8');
assert(f002Content.includes('all(x > 0 for x in [1, 2, 3])'), 'Ф-002 card 5 must use generator expression all(x > 0 for x in ...) without list brackets');
assert(f002Content.includes('`short-circuit`'), 'Ф-002 card 5 must format short-circuit in code backticks');
assert(academyHtml.includes('all(x &gt; 0 for x in [1, 2, 3])'), 'academy.html must contain generator expression all(x > 0 for x in [1, 2, 3]) in Ф-002');
console.log('✓ Bug 1 (Ф-002 card 5): lazy generator all() and formatted short-circuit verified');

// 2. Bug 2: Ф-004 card 6: фокус на цикле for и протоколе итерации
const f004Path = path.join(remnoteDir, '01 · 🐍 Python', 'Юнит 1.1 · Базовый синтаксис', '📇 Карточки', 'Ф-004. Последовательности.md');
assert(fs.existsSync(f004Path), 'Ф-004.md missing');
const f004Content = fs.readFileSync(f004Path, 'utf-8');
assert(f004Content.includes('Итерация через цикл `for` (обход `for item in sequence:`)'), 'Ф-004 card 6 must clearly state iteration through for loop');
assert(academyHtml.includes('Итерация через цикл <code>for</code> (обход <code>for item in sequence:</code>)'), 'academy.html must contain clarified for loop explanation in Ф-004');
console.log('✓ Bug 2 (Ф-004 card 6): for loop iteration answer verified');

// 3. Bug 3: Ф-007 card 12: инлайн форматирование кода в ответе карточки join()
const f007Path = path.join(remnoteDir, '01 · 🐍 Python', 'Юнит 1.1 · Базовый синтаксис', '📇 Карточки', 'Ф-007. Строковые методы split() и join().md');
assert(fs.existsSync(f007Path), 'Ф-007.md missing');
const f007Content = fs.readFileSync(f007Path, 'utf-8');
assert(f007Content.includes('Пустую строку `""` (вызов `"".join([\'h\', \'i\'])`)'), 'Ф-007 card 12 must wrap join call in backticks in markdown');
assert(academyHtml.includes('Пустую строку <code>&quot;&quot;</code> (вызов <code>&quot;&quot;.join([&#x27;h&#x27;, &#x27;i&#x27;])</code>)'), 'academy.html must contain code tags for join() call in Ф-007');
assert(academyHtml.includes('Guaranteed markdown backticks conversion to <code> tags'), 'formatRichInlineText must guarantee markdown backtick conversion even when other tags exist');
console.log('✓ Bug 3 (Ф-007 card 12): inline code formatting in card answer verified');

// 4. Bug 4: Ф-009 card 2: подробное пояснение к sorted(arr) vs arr.sort()
const f009Path = path.join(remnoteDir, '04 · ⚡ Алгоритмы', 'Юнит 4.1 · Сложность', '📇 Карточки', 'Ф-009. Сложность Сложность основных операций для lis.md');
assert(fs.existsSync(f009Path), 'Ф-009.md missing');
const f009Content = fs.readFileSync(f009Path, 'utf-8');
assert(f009Content.includes('Пример и пояснение: `sorted([3, 1, 2])` создаёт и возвращает **новый** отсортированный список `[1, 2, 3]`'), 'Ф-009 card 2 must contain explicit code example and explanation in markdown');
assert(f009Content.includes('не меняя исходный (в отличие от `arr.sort()`, который сортирует список на месте за $O(1)$ по доп. памяти)'), 'Ф-009 card 2 must explain difference with arr.sort() in-place');
assert(academyHtml.includes('<code>sorted([3, 1, 2])</code> создаёт и возвращает <strong>новый</strong> отсортированный список <code>[1, 2, 3]</code>'), 'academy.html must contain formatted code example in Ф-009 card 2');
console.log('✓ Bug 4 (Ф-009 card 2): code example and explanation for sorted() vs sort() verified');

// 5. Bug 5: Ф-009 card 3: объяснение различия O(len(s1)) разности s1 - s2 от O(min(n, m)) пересечения
assert(f009Content.includes('Разъяснение: $O(\\min(n, m))$ применяется для пересечения `s1 & s2`'), 'Ф-009 card 3 must explicitly explain why difference is not O(min(n, m))');
assert(academyHtml.includes('Разъяснение: <span class=\\"math-formula\\">O(min(n, m))</span> применяется для пересечения <code>s1 &amp; s2</code>'), 'academy.html must contain difference vs intersection clarification in Ф-009 card 3');
console.log('✓ Bug 5 (Ф-009 card 3): explanation for O(len(s1)) vs O(min(n, m)) verified');

// 6, 7, 8. Bugs 6-8: Ф-009 cards 13 & 14: форматирование формул O(min(n, m)) и O(n + m) с пояснениями
assert(f009Content.includes('13. Сложность `s1 & s2` (пересечение множеств)? >> $O(\\min(n, m))$ — алгоритм итерируется по меньшему'), 'Ф-009 card 13 must format formula and algorithm description');
assert(f009Content.includes('14. Сложность `s1 | s2` (объединение множеств)? >> $O(n + m)$ — копирует все уникальные элементы'), 'Ф-009 card 14 must format formula and algorithm description');
assert(academyHtml.includes('<span class=\\"math-formula\\">O(min(n, m))</span> — алгоритм итерируется по меньшему из двух множеств'), 'academy.html must render card 13 with .math-formula');
assert(academyHtml.includes('<span class=\\"math-formula\\">O(n + m)</span> — копирует все уникальные элементы обоих множеств'), 'academy.html must render card 14 with .math-formula');
console.log('✓ Bugs 6, 7, 8 (Ф-009 cards 13 & 14): math formula formatting and descriptions verified');

// 9. Bug 9: Защита мобильных вкладок от наложения (overflow-x, nowrap, flex: 1 1 0, min-width: 0)
assert(academyHtml.includes('overflow-x: auto;') && academyHtml.includes('flex-wrap: nowrap;') && academyHtml.includes('min-width: 0;'), 'CSS must prevent tab collision with overflow-x: auto and flex-wrap: nowrap');
console.log('✓ Bug 9: Mobile tabs anti-collision and zero-overlap layout verified');

// 10. Bug 10: Разделение первого шага конспекта К-001 на 2 независимых микро-шага
const k001Path = path.join(remnoteDir, '01 · 🐍 Python', 'Юнит 1.1 · Базовый синтаксис', '📚 Конспекты', 'К-001. Структуры данных Python_ list, dict, set.md');
assert(fs.existsSync(k001Path), 'К-001.md missing');
const k001Content = fs.readFileSync(k001Path, 'utf-8');
assert(k001Content.includes('## Почему выбор структуры данных важен'), 'К-001 must contain separate section for why data structures matter');
assert(k001Content.includes('## List: динамический массив и порядок элементов'), 'К-001 must contain separate section for List dynamic array');

// Проверяем скомпилированный объект К-001 в academyHtml
const k001Match = academyHtml.match(/"К-001":\s*(\{[^}]*"steps":\s*\[.*?\]\s*\})/s);
assert(k001Match, 'academy.html must contain parsed К-001 object');
const k001Obj = JSON.parse(k001Match[1]);
assert.strictEqual(k001Obj.steps.length, 8, `К-001 must have exactly 8 steps after split, got ${k001Obj.steps.length}`);
assert.strictEqual(k001Obj.steps[0].title, 'Почему выбор структуры данных важен', 'Step 1 must be Why data structures matter');
assert.strictEqual(k001Obj.steps[1].title, 'List: динамический массив и порядок элементов', 'Step 2 must be List: dynamic array and ordering');
console.log('✓ Bug 10: Split K-001 step 1 into 2 distinct steps verified (8 steps total)');

// 11, 13. Bugs 11 & 13: Убрать верхнюю кнопку багов, оставить нижнюю плавающую
assert(!academyHtml.includes('id="bug-report-btn-m"'), 'Top bug button must be removed from header');
assert(!academyHtml.includes('class="topbar-help-btn bug-topbar-btn"'), 'Top bug button must be removed from theory topbar');
assert(academyHtml.includes('.bug-topbar-btn, #bug-report-btn-m { display: none !important; }'), 'CSS must strictly hide top bug buttons');
assert(academyHtml.includes('.bug-fab-btn'), 'Bottom floating ladybug button (FAB) must remain preserved');
console.log('✓ Bugs 11 & 13: Top duplicate bug button removed, bottom FAB preserved');

// 12. Bug 12: Длинная строка items.insert заменена на скроллящийся многострочный блок
assert(!academyHtml.includes('<p><code>items = [1, 2, 3, 4, 5]; items.insert(0, 0)'), 'Inline unscrollable items.insert snippet must be replaced');
assert(academyHtml.includes('items = [1, 2, 3, 4, 5]\\nitems.insert(0, 0)') || academyHtml.includes('items = [1, 2, 3, 4, 5]\\\\nitems.insert(0, 0)'), 'Items snippet must be multiline');
console.log('✓ Bug 12: items.insert responsive multiline block formatting verified');

// 14. Bug 14: В блоке кода словаря сделаны отступы строк для читаемости
assert(academyHtml.includes('# O(1) — мгновенный доступ по ключу') && academyHtml.includes('value = d[&#x27;key&#x27;]') && academyHtml.includes('# O(1) — добавление новой пары'), 'Dict code block in K-001 must have spaced lines and comments');
console.log('✓ Bug 14: Dict code block spacing and line-by-line comments verified');

// 15, 16. Bugs 15 & 16: Построчный разбор работы наивного и быстрого алгоритмов поиска дубликатов
assert(academyHtml.includes('# Строка 1: фиксируем опорный элемент от первого до конца') || academyHtml.includes('Шаг 1: перебираем опорный элемент'), 'Duplicate search code must contain line-by-line comment scaffolding');
assert(academyHtml.includes('Построчный разбор работы алгоритма:'), 'Theory step must introduce line-by-line algorithm walkthrough');
console.log('✓ Bugs 15 & 16: Line-by-line scaffolding for duplicate search algorithms verified');

// 17, 18. Bugs 17 & 18: Модалка финиша конспекта, «Продолжить чтение конспектов» и чистое название без К-001
assert(academyHtml.includes('📖 Продолжить чтение конспектов ➔'), 'Finish celebration modal must offer explicit button to continue reading next note');
assert(academyHtml.includes('data-py-select-k="${nextKid}"'), 'Continue reading button must target next note ID');
assert(academyHtml.includes('cleanTitle = rawTitle.replace'), 'Celebration title must strip raw technical note IDs like К-001');
console.log('✓ Bugs 17 & 18: Sprint finish celebration modal with continue reading button & clean titles verified');

// 19. Bug 19: Убрать технические мусорные обозначения на #/ и соблюдать Home = Journey
assert(!academyHtml.includes('Это каркас: карта навыков уже живая'), 'Old technical placeholder text must be stripped from dashboard');
assert(academyHtml.includes("if(route === '/'){\n    root.innerHTML = (state.pathViewMode === 'pro') ? viewProPath() : viewPathSerpentine();") || academyHtml.includes("if(route === '/'){\r\n    root.innerHTML = (state.pathViewMode === 'pro') ? viewProPath() : viewPathSerpentine();"), 'Root route #/ must directly render the main journey path (Home = Journey)');
console.log('✓ Bug 19: Root route cleaned from technical placeholders, Home = Journey enforced');

// 20. Bug 20: К-004 step 2: 'в сравнении с list', а не 'со'
const k004Path = path.join(remnoteDir, '01 · 🐍 Python', 'Юнит 1.1 · Базовый синтаксис', '📚 Конспекты', 'К-004. frozenset_ неизменяемое множество.md');
assert(fs.existsSync(k004Path), 'К-004.md missing');
const k004Content = fs.readFileSync(k004Path, 'utf-8');
assert(k004Content.includes('Как и `tuple` в сравнении с `list`'), 'К-004.md must say "в сравнении с list"');
assert(academyHtml.includes('в сравнении с <code>list') || academyHtml.includes('в сравнении с `list`'), 'academy.html must contain proper grammar "в сравнении с list" in К-004');
console.log('✓ Bug 20: K-004 "в сравнении с list" grammar verified');

// 21. Bug 21: Реактивное обновление счетчика +XP за сутки и удаление захардкоженного fallback || 55
assert(!academyHtml.includes('⚡ +${dayXpVal || 55} XP'), 'Bug 21: fallback || 55 must be removed');
assert(academyHtml.includes("document.querySelectorAll('.sprint-xp-pill').forEach"), 'Bug 21: awardXp must reactively update sprint-xp-pill in DOM');
console.log('✓ Bug 21: Reactive daily XP sprint pill update and removal of hardcoded fallback 55 verified');

// 22. Bug 22: Отступы строк и пояснения к сложности операций в К-004
assert(academyHtml.includes('# O(len(a) + len(b)) — объединение') && academyHtml.includes('# O(min(len(a), len(b))) — пересечение'), 'Bug 22: operations in K-004 must have line breaks and comments');
const k004ContentUpdated = fs.readFileSync(k004Path, 'utf-8');
assert(k004ContentUpdated.includes('# O(len(a) + len(b)) — объединение'), 'Bug 22: K-004.md must have spaced operation lines with comments');
console.log('✓ Bug 22: K-004 step 3 operations code block spacing and comments verified');

// 23. Bug 23: Компактные отступы между блоками теории (.feed-chunk + .feed-chunk)
assert(academyHtml.includes('padding-top:8px;margin-top:0;') && academyHtml.includes('.feed-chunk p{margin:0 0 8px;'), 'Bug 23: feed-chunk spacing must be compact (8px instead of 14px)');
console.log('✓ Bug 23: Theory feed-chunk compact spacing verified');

// 24. Bug 24: Подсветка синтаксиса в блоках кода конспектов (highlightPythonTokens до snippet-wrap check)
assert(academyHtml.includes('s = s.replace(/<pre><code>([\\s\\S]*?)<\\/code><\\/pre>/g') && academyHtml.includes('highlightPythonTokens(codeInner)'), 'Bug 24: decorateCodeBlocksWithRunBtn must highlight python tokens before snippet-wrap check');
console.log('✓ Bug 24: Syntax highlighting in theory code snippets verified');

// 25. Bug 25: Мобильная читаемость кода в К-005 step 6 (длинные комментарии вынесены на строки над кодом)
const k005Path = path.join(remnoteDir, '01 · 🐍 Python', 'Юнит 1.1 · Базовый синтаксис', '📚 Конспекты', 'К-005. args kwargs и распаковка в Python.md');
assert(fs.existsSync(k005Path), 'К-005.md missing');
const k005Content = fs.readFileSync(k005Path, 'utf-8');
assert(k005Content.includes('# При слиянии словарей overrides перезатирает совпадающие ключи:') && k005Content.includes('# Аналогично для объединения списков через *:'), 'Bug 25: long comments in K-005 step 6 must be placed on separate lines for mobile display');
assert(academyHtml.includes('# При слиянии словарей overrides перезатирает совпадающие ключи:') && academyHtml.includes('config = {**defaults, **overrides}'), 'Bug 25: academy.html must have comments on separate lines in K-005');
console.log('✓ Bug 25: K-005 step 6 mobile code block readability verified');

// 26. Bug 26: Очистка тултипов dot-jewel конспектов от технических префиксов К-\d+
assert(academyHtml.includes("cleanNoteTitle = (n.title || kId).replace(/^К-\\d+\\s*[:·•\\-]\\s*/i, '').trim();") && academyHtml.includes("title=\"${escapeHtmlStr(cleanNoteTitle)}\""), 'Bug 26: dot-jewel title must strip technical prefix К-\\d+');
console.log('✓ Bug 26: Strip technical prefix К-\\d+ from note dots and titles verified');

// 27. Bug 27: Ясное и дидактичное условие задачи #258 про хэшируемость кортежа vs изменяемый список
assert(academyHtml.includes('"id": 258') && academyHtml.includes("TypeError: unhashable type: 'list'") && academyHtml.includes('point_tuple: \\"запись в кэше\\"'), 'Bug 27: task 258 must clearly explain tuple hashability vs mutable list with explicit steps');
console.log('✓ Bug 27: Task 258 tuple hashability and dictionary key invariants verified');

// 28, 30. Bugs 28 & 30: Красивые блоки кода с подсветкой в вопросах рубежного теста
assert(academyHtml.includes('formatQuizQuestionPromptHTML(rawText)') && academyHtml.includes('highlightPythonTokens(escapeHtmlStr(codePart))') && academyHtml.includes('quiz-question-code'), 'Bug 28 & 30: quiz question code block must be syntax-highlighted in formatQuizQuestionPromptHTML');
assert(academyHtml.includes('Что выведет следующий код?\\n\\na = [1, 2]\\nb = a\\nb += [3]\\nprint(len(a))'), 'Bug 30: question 1 in unit test 1.1 must be formatted as readable multiline code block');
console.log('✓ Bugs 28 & 30: Syntax-highlighted code blocks in unit test questions verified');

// 29. Bug 29: Двухфазный выбор ответов в рубежном тесте (pending selection -> осознанное нажатие кнопки «Ответить»)
assert(academyHtml.includes('quiz-opt--pending') && academyHtml.includes('data-ut-confirm') && academyHtml.includes('Ответить'), 'Bug 29: unit test must have two-phase selection with pending state and explicit Ответить button');
console.log('✓ Bug 29: Unit test two-phase selection (think before answer) verified');

console.log('\n================================================================');
console.log('  ALL 30 REGRESSION TESTS PASSED! (0 FAILURES, ZERO RECURRENCE) ');
console.log('================================================================\n');
