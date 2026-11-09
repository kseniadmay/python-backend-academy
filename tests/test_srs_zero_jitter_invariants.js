#!/usr/bin/env node
/**
 * test_srs_zero_jitter_invariants.js
 * 
 * Пре-коммит тест инвариантов Zero-Jitter и Zero-Flicker интерфейса SRS:
 * 1. Гарантирует абсолютную идентичность academy.html и standards/standards.html (100% SSOT).
 * 2. Гарантирует сбалансированное вертикальное позиционирование main:has(.cards-hub-container) (justify-content: center).
 * 3. Гарантирует стабильность точки активности .activity-dot в сайдбаре (animation: none, без "дыхания" со scale).
 * 4. Гарантирует стабильность точки активности .srs-live-status-dot в хедере (animation: none, contain: strict).
 * 5. Запрещает расходящиеся волны bead-ping-wave, пульсацию bead-pulse-emerald и srsBeadPulse на бусинах.
 * 6. Гарантирует аппаратную изоляцию и анти-бликовое поведение кнопок ответа .fc-rate-btn:
 *    contain: layout style paint, -webkit-tap-highlight-color: transparent, user-select: none.
 * 7. Запрещает бесконечные анимации box-shadow в оптических плашках сайдбара (cherryHeat, whiteHot, coldIron, rubyBud, goldenRose).
 * 8. Запрещает мерцание сетки кнопок srsFadeIn (.srs-rating-grid).
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

// 2. Инвариант стабильности сцены: сбалансированное вертикальное позиционирование без прилипания вверх
assert(content.includes('main:has(.cards-hub-container)'), 'main:has(.cards-hub-container) должен быть определен в стилях');
assert(content.includes('justify-content: center !important;\n    align-items: center !important;\n    min-height: calc(100vh - 56px) !important;'), 
  'main:has(.cards-hub-container) должен центрировать сцену сбалансированно (justify-content: center)');
console.log('✓ [Zero-Jitter] Сбалансированное вертикальное позиционирование сцены SRS соблюдено.');

// 3. Инвариант стабильности точки активности в сайдбаре (.activity-dot)
const actDotMatches = content.match(/\.activity-dot\s*\{[^}]+\}/g) || [];
assert(actDotMatches.length > 0, '.activity-dot должен быть определен в стилях');
for (const block of actDotMatches) {
  assert(block.includes('animation: none') || block.includes('animation:none'), `Блок .activity-dot обязан иметь animation: none: ${block}`);
}
assert(!content.includes('animation:emeraldSoftBreath 2.8s infinite'), 'Паразитное дыхание emeraldSoftBreath на .activity-dot должно быть отключено');
console.log('✓ [Zero-Jitter] Точка активности в сайдбаре (.activity-dot) стабильна: animation: none, без паразитного дыхания.');

// 4. Инвариант стабильности точки активности SRS (.srs-live-status-dot)
const liveDotMatches = content.match(/\.srs-live-status-dot\s*\{[^}]+\}/g) || [];
assert(liveDotMatches.length > 0, '.srs-live-status-dot должен быть определен в стилях');
for (const block of liveDotMatches) {
  assert(block.includes('animation: none') || block.includes('animation:none'), `Блок .srs-live-status-dot обязан иметь animation: none: ${block}`);
  assert(block.includes('contain: strict !important;'), `Блок .srs-live-status-dot обязан иметь contain: strict: ${block}`);
  assert(!block.includes('animation: srsLiveDotPulse'), `Блок .srs-live-status-dot не должен содержать animation: srsLiveDotPulse`);
}
console.log('✓ [Zero-Jitter] Точка активности SRS (.srs-live-status-dot) стабильна: animation: none, contain: strict.');

// 5. Инвариант стабильности бусин ожерелья: отсутствие bead-ping-wave, srsBeadPulse
assert(!content.includes('animation: bead-ping-wave'), 'bead-ping-wave со scale-расширением не должен использоваться на бусинах');
assert(!content.includes('animation: srsBeadPulse 2s infinite'), 'srsBeadPulse не должен вызываться на активных бусинах');
assert(content.includes('display: none !important;\n    content: none !important;\n    animation: none !important;'), 
  'Псевдоэлемент активной бусины должен быть скрыт (display: none !important)');
console.log('✓ [Zero-Jitter] Ожерелье бусин активно без паразитных волн и дерганий: bead-ping-wave и srsBeadPulse ликвидированы.');

// 6. Инвариант кнопок ответа: аппаратная изоляция и анти-выделение
assert(content.includes('contain: layout style paint !important;'), 'Кнопки .fc-rate-btn обязаны иметь аппаратную изоляцию contain: layout style paint');
assert(content.includes('-webkit-tap-highlight-color: transparent !important;'), 'Кнопки .fc-rate-btn обязаны убирать синее выделение тапа (-webkit-tap-highlight-color: transparent)');
assert(content.includes('user-select: none !important;'), 'Кнопки .fc-rate-btn обязаны запрещать текстовое выделение');
assert(content.includes('@media (hover: none)'), 'Должно быть медиа-правило для тач-устройств без ховера (@media (hover: none))');
console.log('✓ [Zero-Jitter] Кнопки ответов .fc-rate-btn аппаратно изолированы и защищены от синего паразитного выделения.');

// 7. Инвариант сайдбара: отсутствие бесконечных колебаний теней
assert(!content.includes('animation: cherryHeatIronDazzle 2.8s infinite'), 'cherryHeatIronDazzle не должен анимироваться с infinite в сайдбаре');
assert(!content.includes('animation: whiteHotMetalBreath 2.6s infinite'), 'whiteHotMetalBreath не должен анимироваться с infinite в сайдбаре');
console.log('✓ [Zero-Jitter] Плашки накала сайдбара переведены в стабильный статический благородный накал.');

// 8. Инвариант сетки кнопок: отсутствие анимации srsFadeIn
assert(!content.includes('animation: srsFadeIn 0.26s cubic-bezier(0.4, 0, 0.2, 1) both'), 'srsFadeIn не должен применяться к сетке кнопок .srs-rating-grid');
console.log('✓ [Zero-Jitter] Сетка кнопок оценок защищена от мерцания srsFadeIn.');

console.log('✓ [Pre-Commit] Все проверки Zero-Jitter & Zero-Flicker успешно пройдены (100%).');
process.exit(0);
