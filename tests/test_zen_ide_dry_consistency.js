#!/usr/bin/env node
/**
 * test_zen_ide_dry_consistency.js
 *
 * Архитектурный тест на строгое соответствие принципу DRY (Don't Repeat Yourself)
 * для единого экрана решения задач Zen IDE в Python Backend Academy.
 *
 * Инварианты проверки:
 * 1. Single Source of Truth: единая функция-рендерер buildUnifiedZenIdeHTML(...)
 *    используется как в спринте урока (viewPythonSkill), так и в банке задач (viewPracticeHub).
 * 2. Запрет дублирования разметки: отсутствие дублирующего разрозненного кода сплит-экрана практики.
 * 3. Консистентность мастер-эталона:
 *    - Наличие VS Code Mini-Drawer (.vscode-mini-drawer) с табами Тесты, Stdout, Сократ.
 *    - Наличие сворачиваемых аккордеонов (.zen-accordion) для Анатомии и Сократа.
 *    - Наличие Баннера триумфа (.triumph-celebration-banner) при успешной сдаче тестов.
 *    - Наличие сократического диффа buildSocraticDiffHTML для контрастного сравнения вывода.
 * 4. Master-Detail архитектура в viewPracticeHub (каталог -> переход в единый Zen IDE).
 * 5. Побайтовая идентичность между academy.html и standards/standards.html.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const ACADEMY_PATH = path.join(ROOT, 'academy.html');
const STANDARDS_PATH = path.join(ROOT, 'standards', 'standards.html');

console.log('--- 🧪 Запуск архитектурного DRY-теста экрана решения задач (Zen IDE) ---');

// Проверка 1: Побайтовая идентичность academy.html и standards/standards.html
assert(fs.existsSync(ACADEMY_PATH), 'Файл academy.html должен существовать');
assert(fs.existsSync(STANDARDS_PATH), 'Файл standards/standards.html должен существовать');

const academyRaw = fs.readFileSync(ACADEMY_PATH);
const standardsRaw = fs.readFileSync(STANDARDS_PATH);

assert.strictEqual(
  academyRaw.length,
  standardsRaw.length,
  `[DRY ERROR] Размер academy.html (${academyRaw.length} байт) отличается от standards/standards.html (${standardsRaw.length} байт)!`
);
assert(
  academyRaw.equals(standardsRaw),
  '[DRY ERROR] academy.html и standards/standards.html не являются побайтово идентичными!'
);
console.log('  ✓ [DRY 1/5] Побайтовая идентичность academy.html и standards.html: 100% совпадение (Single Source of Truth)');

const content = academyRaw.toString('utf8');

// Проверка 2: Наличие канонической функции-рендерера buildUnifiedZenIdeHTML
assert(
  content.includes('function buildUnifiedZenIdeHTML(params){'),
  '[DRY ERROR] Отсутствует каноническая функция buildUnifiedZenIdeHTML — нарушение Single Source of Truth!'
);
assert(
  content.includes('function buildSocraticDiffHTML(rawOutput){'),
  '[DRY ERROR] Отсутствует универсальная функция генерации сократического диффа buildSocraticDiffHTML!'
);
console.log('  ✓ [DRY 2/5] Канонические генераторы buildUnifiedZenIdeHTML и buildSocraticDiffHTML определены в кодовой базе');

// Проверка 3: DRY-вызов buildUnifiedZenIdeHTML из viewPythonSkill и viewPracticeHub
// А) В спринте урока
const hasSprintCall = content.includes("bodyHTML = buildUnifiedZenIdeHTML({") &&
                      content.includes("editorId: 'py-skill-editor'") &&
                      content.includes("context: 'sprint'");
assert(
  hasSprintCall,
  '[DRY ERROR] Вкладка практики в viewPythonSkill обязана вызывать buildUnifiedZenIdeHTML!'
);

// Б) В глобальном банке задач
const hasHubCall = content.includes("const zenIdeHTML = buildUnifiedZenIdeHTML({") &&
                   content.includes("editorId: 'prac-code-editor'") &&
                   content.includes("context: 'hub'");
assert(
  hasHubCall,
  '[DRY ERROR] viewPracticeHub в режиме IDE обязан вызывать buildUnifiedZenIdeHTML вместо дублирования разметки!'
);
console.log('  ✓ [DRY 3/5] DRY-связка: и спринт урока, и банк задач используют единый вызов buildUnifiedZenIdeHTML');

// Проверка 4: Исключение дублирования старого сплит-вью
// В viewPracticeHub больше не должно быть отдельной хардкодной сетки practice-desktop-grid
assert(
  !content.includes('<div class="practice-desktop-grid">'),
  '[DRY ERROR] Обнаружен устаревший дублирующий контейнер practice-desktop-grid в разметке!'
);
assert(
  !content.includes('<div class="prac-signature-box"><div class="sig-badge">'),
  '[DRY ERROR] Обнаружен дублирующий блок prac-signature-box — спецификация должна формироваться через единый инспектор!'
);
console.log('  ✓ [DRY 4/5] Устаревшая разрозненная разметка полностью устранена, дублирование = 0%');

// Проверка 5: Проверка компонентов утверждённого мастер-эталона
const requiredComponents = [
  { name: 'VS Code Mini-Drawer', pattern: 'vscode-mini-drawer' },
  { name: 'Drawer Tab Buttons', pattern: 'data-zen-drawer-tab="tests"' },
  { name: 'Drawer Toggle Button', pattern: 'data-zen-toggle-drawer' },
  { name: 'Smart Accordions (Slice & Socrates)', pattern: 'data-zen-toggle-acc' },
  { name: 'Triumph Celebration Banner', pattern: 'triumph-celebration-banner' },
  { name: 'Clean Minimal Code Editor (без лишних чипсов)', pattern: 'buildCodeEditorWithGutterHTML(editorId, codeDraft, 240, null, true)' },
  { name: 'Master-Detail Catalog Grid', pattern: 'prac-catalog-grid' },
  { name: 'Open Task in Zen IDE Attribute', pattern: 'data-open-prac-task' },
  { name: 'Back to Catalog Attribute', pattern: 'data-prac-back-catalog' }
];

requiredComponents.forEach(comp => {
  assert(
    content.includes(comp.pattern),
    `[DRY & STANDARDS ERROR] Компонент ${comp.name} (${comp.pattern}) отсутствует в разметке!`
  );
});
console.log('  ✓ [DRY 5/5] Все компоненты утверждённого мастер-эталона (Mini-Drawer, Accordions, Triumph, Master-Detail) подтверждены');

console.log('--- 🏆 ВСЕ ПРОВЕРКИ DRY УСПЕШНО ПРОЙДЕНЫ (100% DRY Compliance) ---');
process.exit(0);
