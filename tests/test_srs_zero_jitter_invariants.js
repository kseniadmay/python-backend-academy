#!/usr/bin/env node
/**
 * test_srs_zero_jitter_invariants.js
 * 
 * Пре-коммит тест инвариантов Zero-Jitter и Zero-Flicker интерфейса SRS:
 * 1. Гарантирует абсолютную идентичность academy.html и standards/standards.html (100% SSOT).
 * 2. Запрещает justify-content: center на main:has(.cards-hub-container), исключая вертикальные скачки экрана.
 * 3. Гарантирует стабильность точки активности .srs-live-status-dot (animation: none, contain: strict, без "дыхания" со scale).
 * 4. Запрещает расходящиеся волны bead-ping-wave и пульсацию bead-pulse-emerald на активных бусинах ожерелья.
 * 5. Гарантирует аппаратную изоляцию и анти-бликовое поведение кнопок ответа .fc-rate-btn:
 *    contain: layout style paint, -webkit-tap-highlight-color: transparent, user-select: none.
 * 6. Запрещает бесконечные анимации box-shadow в оптических плашках сайдбара (cherryHeatIronDazzle, whiteHotMetalBreath).
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const ACADEMY_PATH = path.join(ROOT, 'academy.html');
const STANDARDS_PATH = path.join(ROOT, 'standards', 'standards.html');

console.log('--- Запуск пре-коммит теста Zero-Jitter & Zero-Flicker SRS ---');

assert(fs.existsSync(ACADEMY_PATH), 'academy.html должен существовать');
assert(fs.existsSync(STANDARDS_PATH), 'standards/standards.html должен существовать');

const academyBytes = fs.readFileSync(ACADEMY_PATH);
const standardsBytes = fs.readFileSync(STANDARDS_PATH);

// 1. Проверка 100% идентичности файлов academy.html и standards/standards.html
assert(academyBytes.equals(standardsBytes), 'academy.html и standards/standards.html обязаны быть идентичны байт-в-байт (100% SSOT)');
console.log('✓ [Zero-Jitter] academy.html и standards/standards.html на 100% идентичны.');

const content = academyBytes.toString('utf8').replace(/\r\n/g, '\n');

// 2. Инвариант стабильности сцены: main:has(.cards-hub-container) не центрирует экран по вертикали
assert(!content.includes('main:has(.cards-hub-container) {\n    display: flex !important;\n    flex-direction: column !important;\n    justify-content: center'), 
  'main:has(.cards-hub-container) не должен содержать justify-content: center (вызывает скачки экрана при дыхании элементов)');
assert(content.includes('main:has(.cards-hub-container)'), 'main:has(.cards-hub-container) должен быть определен в стилях');
assert(content.includes('justify-content: flex-start !important;'), 'main:has(.cards-hub-container) должен использовать justify-content: flex-start');
console.log('✓ [Zero-Jitter] Вертикальное позиционирование экрана SRS зафиксировано (justify-content: flex-start).');

// 3. Инвариант стабильности точки активности: .srs-live-status-dot не имеет "дыхания" со scale
const liveDotMatches = content.match(/\.srs-live-status-dot\s*\{[^}]+\}/g) || [];
assert(liveDotMatches.length > 0, '.srs-live-status-dot должен быть определен в стилях');
for (const block of liveDotMatches) {
  assert(block.includes('animation: none !important;'), `Блок .srs-live-status-dot обязан иметь animation: none: ${block}`);
  assert(block.includes('contain: strict !important;'), `Блок .srs-live-status-dot обязан иметь contain: strict: ${block}`);
  assert(!block.includes('animation: srsLiveDotPulse'), `Блок .srs-live-status-dot не должен содержать animation: srsLiveDotPulse`);
}
console.log('✓ [Zero-Jitter] Точка активности SRS (.srs-live-status-dot) стабильна: animation: none, contain: strict.');

// 4. Инвариант стабильности бусин ожерелья: отсутствие bead-ping-wave со scale(2.2)
assert(!content.includes('animation: bead-ping-wave'), 'bead-ping-wave со scale-расширением не должен использоваться на бусинах');
assert(content.includes('.dot-jewel.active::after') || content.includes('.bead-active-leading::after'), 
  'Псевдоэлемент активной бусины должен быть явно определен');
assert(content.includes('display: none !important;\n    content: none !important;\n    animation: none !important;'), 
  'Псевдоэлемент активной бусины должен быть скрыт (display: none !important)');
console.log('✓ [Zero-Jitter] Ожерелье бусин активно без паразитных волн и дерганий: bead-ping-wave ликвидирован.');

// 5. Инвариант кнопок ответа: аппаратная изоляция и анти-выделение
assert(content.includes('contain: layout style paint !important;'), 'Кнопки .fc-rate-btn обязаны иметь аппаратную изоляцию contain: layout style paint');
assert(content.includes('-webkit-tap-highlight-color: transparent !important;'), 'Кнопки .fc-rate-btn обязаны убирать синее выделение тапа (-webkit-tap-highlight-color: transparent)');
assert(content.includes('user-select: none !important;'), 'Кнопки .fc-rate-btn обязаны запрещать текстовое выделение');
assert(content.includes('@media (hover: none)'), 'Должно быть медиа-правило для тач-устройств без ховера (@media (hover: none))');
console.log('✓ [Zero-Jitter] Кнопки ответов .fc-rate-btn аппаратно изолированы и защищены от синего паразитного выделения.');

// 6. Инвариант сайдбара: отсутствие бесконечных колебаний теней
assert(!content.includes('animation: cherryHeatIronDazzle 2.8s infinite'), 'cherryHeatIronDazzle не должен анимироваться с infinite в сайдбаре');
assert(!content.includes('animation: whiteHotMetalBreath 2.6s infinite'), 'whiteHotMetalBreath не должен анимироваться с infinite в сайдбаре');
console.log('✓ [Zero-Jitter] Плашки накала сайдбара переведены в стабильный статический благородный накал.');

console.log('✓ [Pre-Commit] Все проверки Zero-Jitter & Zero-Flicker успешно пройдены (100%).');
process.exit(0);
