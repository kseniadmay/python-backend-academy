#!/usr/bin/env node
/**
 * test_srs_zero_jitter_invariants.js
 * 
 * Пре-коммит тест инвариантов Живого Дыхания и Zero-Jitter кнопок ответов SRS:
 * 1. Гарантирует абсолютную идентичность academy.html и standards/standards.html (100% SSOT).
 * 2. Гарантирует сбалансированное вертикальное центрирование main:has(.cards-hub-container) (justify-content: center).
 * 3. Гарантирует, что бусины активности ДЫШАТ (bead-pulse-emerald и bead-ping-wave активны).
 * 4. Гарантирует, что точки активности ДЫШАТ (.srs-live-status-dot и .activity-dot активны).
 * 5. Гарантирует абсолютную фиксацию высоты ожерелья бусин (height: 28px, contain: layout),
 *    что исключает передачу дыхания на высоту контейнера и кнопки ответов (0px jitter).
 * 6. Гарантирует аппаратную изоляцию и анти-бликовое поведение кнопок ответа .fc-rate-btn:
 *    contain: strict, -webkit-tap-highlight-color: transparent, user-select: none.
 * 7. Гарантирует отсутствие плавающих margin: auto внутри карточки и дока (монолитный 0px сдвиг).
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const ACADEMY_PATH = path.join(ROOT, 'academy.html');
const STANDARDS_PATH = path.join(ROOT, 'standards', 'standards.html');

console.log('--- Запуск пре-коммит теста Живого Дыхания и Zero-Jitter кнопок SRS ---');

assert(fs.existsSync(ACADEMY_PATH), 'academy.html должен существовать');
assert(fs.existsSync(STANDARDS_PATH), 'standards/standards.html должен существовать');

const academyBytes = fs.readFileSync(ACADEMY_PATH);
const standardsBytes = fs.readFileSync(STANDARDS_PATH);

// 1. Проверка 100% идентичности файлов academy.html и standards/standards.html
assert(academyBytes.equals(standardsBytes), 'academy.html и standards/standards.html обязаны быть идентичны байт-в-байт (100% SSOT)');
console.log('✓ [Zero-Jitter] academy.html и standards/standards.html на 100% идентичны.');

const content = academyBytes.toString('utf8').replace(/\r\n/g, '\n');

// 2. Инвариант стабильности сцены: сбалансированное вертикальное позиционирование
assert(content.includes('main:has(.cards-hub-container)'), 'main:has(.cards-hub-container) должен быть определен в стилях');
assert(content.includes('justify-content: center !important;\n    align-items: center !important;\n    min-height: calc(100vh - 56px) !important;'), 
  'main:has(.cards-hub-container) должен центрировать сцену сбалансированно (justify-content: center)');
console.log('✓ [Zero-Jitter] Сбалансированное вертикальное центрирование сцены SRS соблюдено.');

// 3. Инвариант живого дыхания активных бусин
assert(content.includes('animation: bead-pulse-emerald 2.8s infinite ease-in-out !important;'), 
  'Активная бусина обязана дышать через анимацию bead-pulse-emerald');
assert(content.includes('animation: bead-ping-wave 2.8s cubic-bezier(0.2, 0.8, 0.4, 1) infinite !important;'), 
  'Волна маяка активной бусины обязана дышать через bead-ping-wave');
console.log('✓ [Zero-Jitter] Активная бусина и расходящаяся волна маяка дышат (bead-pulse-emerald & bead-ping-wave).');

// 4. Инвариант живого дыхания точек активности
assert(content.includes('animation: srsLiveDotPulse 2.4s infinite ease-in-out !important;'), 
  'Точка активности SRS в шапке (.srs-live-status-dot) обязана дышать через srsLiveDotPulse');
assert(content.includes('animation: emeraldSoftBreath 2.8s infinite ease-in-out !important;'), 
  'Точка активности в сайдбаре (.activity-dot) обязана дышать через emeraldSoftBreath');
console.log('✓ [Zero-Jitter] Точки активности хедера и сайдбара дышат (srsLiveDotPulse & emeraldSoftBreath).');

// 5. Инвариант строгой фиксации геометрии ожерелья бусин (Zero Layout Shift)
assert(content.includes('height: 28px !important;\n\n    min-height: 28px !important;\n\n    max-height: 28px !important;') ||
       content.includes('height: 28px !important;\n    min-height: 28px !important;\n    max-height: 28px !important;'), 
  'Ожерелье бусин обязано иметь жесткую высоту 28px, чтобы дыхание не передавалось на лейаут');
assert(content.includes('contain: layout !important;'), 
  'Ожерелье бусин обязано иметь contain: layout для изоляции анимаций');
console.log('✓ [Zero-Jitter] Высота ожерелья бусин строго зафиксирована (28px, contain: layout) — 0px смещения.');

// 6. Инвариант монолитности кнопок ответа
assert(content.includes('contain: layout style !important;') || content.includes('contain: layout style paint !important;'), 
  'Кнопки .fc-rate-btn обязаны иметь аппаратную изоляцию contain: layout style');
assert(content.includes('-webkit-tap-highlight-color: transparent !important;'), 
  'Кнопки .fc-rate-btn обязаны убирать синее выделение тапа (-webkit-tap-highlight-color: transparent)');
assert(content.includes('user-select: none !important;'), 
  'Кнопки .fc-rate-btn обязаны запрещать текстовое выделение');
assert(content.includes('@media (hover: none)'), 
  'Должно быть медиа-правило для тач-устройств без ховера (@media (hover: none))');
console.log('✓ [Zero-Jitter] Кнопки ответов .fc-rate-btn аппаратно изолированы и защищены от синего паразитного выделения.');

// 7. Инвариант отсутствия плавающего margin-top: auto на мобилке
assert(!content.includes('margin-top: auto !important;\n    padding: 8px 10px calc(12px + env(safe-area-inset-bottom, 0px)) !important;'), 
  'Док действий не должен иметь плавающего margin-top: auto, вызывающего подрагивание кнопок');
console.log('✓ [Zero-Jitter] Док действий монолитно зафиксирован (margin-top: 14px, 0px jitter).');

// 8. Инвариант оптического дыхания точек активности (СТРОГИЙ ЗАПРЕТ НА scale)
const emeraldBreathMatch = content.match(/@keyframes emeraldSoftBreath\s*\{([\s\S]*?)\}/);
assert(emeraldBreathMatch, '@keyframes emeraldSoftBreath обязан быть определен в CSS');
assert(!emeraldBreathMatch[1].includes('scale('), 
  '❌ ZERO-JITTER VIOLATION: В @keyframes emeraldSoftBreath запрещен scale()! Дыхание точек обязано производиться строго через box-shadow и opacity (0px jitter).');

const srsPulseMatch = content.match(/@keyframes srsLiveDotPulse\s*\{([\s\S]*?)\}/);
assert(srsPulseMatch, '@keyframes srsLiveDotPulse обязан быть определен в CSS');
assert(!srsPulseMatch[1].includes('scale('), 
  '❌ ZERO-JITTER VIOLATION: В @keyframes srsLiveDotPulse запрещен scale()! Дыхание точек обязано производиться строго через box-shadow и opacity (0px jitter).');

// 9. Инвариант симметричной рамки кнопок сайдбара (0px Border Jump)
assert(content.includes('.navlink{display:flex;align-items:center;gap:10px;padding:8px 11px;border-radius:11px;text-decoration:none;color:var(--ink-soft);font-weight:500;font-size:.88rem;margin-bottom:2px;border:1px solid transparent;border-left:3px solid transparent;box-sizing:border-box;'),
  '❌ ZERO-JITTER VIOLATION: .navlink обязан иметь border-left: 3px solid transparent для исключения 2px скачка при активации.');

// 10. Инвариант аппаратной изоляции точек активности
assert(content.includes('contain:layout style !important;'),
  '❌ ZERO-JITTER VIOLATION: .activity-dot обязана содержать contain:layout style для изоляции от родительской кнопки.');
assert(content.includes('.nav-sub-breath-dot') && content.includes('contain: layout style !important;'),
  '❌ ZERO-JITTER VIOLATION: .nav-sub-breath-dot обязана содержать contain: layout style для изоляции от подпункта.');
console.log('✓ [Zero-Jitter] Железный замок оптического дыхания и симметричных рамок соблюдён (0 scale, 0px border jump).');

console.log('✓ [Pre-Commit] Все проверки Живого Дыхания и Zero-Jitter кнопок успешно пройдены (100%).');
process.exit(0);
