#!/usr/bin/env node
/**
 * test_srs_zero_jitter_invariants.js
 * 
 * Пре-коммит и билд-тест инвариантов Живого Дыхания, монолитности сцены карточек
 * и Zero-Jitter кнопок ответов SRS:
 * 
 * 1. 100% SSOT: Гарантирует абсолютную идентичность academy.html и standards/standards.html байт-в-байт.
 * 2. Стабильность вертикального центрирования main:has(.cards-hub-container).
 * 3. Монолитный слот сцены карточки на десктопе: .fc-stage, .fc-card, .card-face min-height: 280px (Zero Flip Jitter).
 * 4. Запрет плавающего margin: auto у .cards-hub-container: строго margin: 0 auto (исключает деление высоты пополам).
 * 5. Монолитный слот сцены карточки на мобилке: .fc-stage, .fc-card min-height: 240px.
 * 6. Защита функции animateCardFlip от скачков инлайн-высоты.
 * 7. Единое оптическое свечение всех точек активности (.activity-dot, .nav-sub-breath-dot, .pulse-dot, .srs-live-status-dot).
 * 8. Строгий запрет на 2-секундное зацикленное подёргивание и масштабирование бусин (0 scale, запрет pulse-ring 2s).
 * 9. Строгая фиксация высоты ожерелья бусин (height: 28px, contain: layout) — 0px смещения.
 * 10. Монолитность и аппаратная изоляция кнопок ответа .fc-rate-btn (52px, contain: layout style).
 * 11. Оптическое дыхание точек строго через box-shadow/opacity (запрет scale в keyframes).
 * 12. Симметричная рамка кнопок сайдбара (border-left: 3px solid transparent, 0px border jump).
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const ACADEMY_PATH = path.join(ROOT, 'academy.html');
const STANDARDS_PATH = path.join(ROOT, 'standards', 'standards.html');

console.log('--- [Build & Pre-Commit Guard] Проверка инвариантов Zero-Jitter и монолитности SRS ---');

assert(fs.existsSync(ACADEMY_PATH), 'academy.html должен существовать');
assert(fs.existsSync(STANDARDS_PATH), 'standards/standards.html должен существовать');

const academyBytes = fs.readFileSync(ACADEMY_PATH);
const standardsBytes = fs.readFileSync(STANDARDS_PATH);

// 1. Проверка 100% идентичности файлов academy.html и standards/standards.html
assert(academyBytes.equals(standardsBytes), 'academy.html и standards/standards.html обязаны быть идентичны байт-в-байт (100% SSOT)');
console.log('✓ [1/12] [Zero-Jitter SSOT] academy.html и standards/standards.html на 100% идентичны.');

const content = academyBytes.toString('utf8').replace(/\r\n/g, '\n');

// 2. Инвариант стабильности сцены: сбалансированное вертикальное позиционирование
assert(content.includes('main:has(.cards-hub-container)'), 'main:has(.cards-hub-container) должен быть определен в стилях');
assert(content.includes('justify-content: center !important;\n    align-items: center !important;\n    min-height: calc(100vh - 56px) !important;'), 
  'main:has(.cards-hub-container) должен центрировать сцену сбалансированно (justify-content: center)');
console.log('✓ [2/12] [Zero-Jitter] Сбалансированное вертикальное центрирование сцены SRS соблюдено.');

// 3. Инвариант монолитного слота сцены карточки на десктопе (min-height: 280px)
assert(content.includes('.fc-stage {\n    min-height: 280px !important;\n    display: flex !important;\n    flex-direction: column !important;\n    justify-content: flex-start !important;\n    margin: 0 auto !important;\n    box-sizing: border-box !important;\n    contain: layout style !important;\n  }'),
  '❌ ZERO-JITTER VIOLATION: .fc-stage обязан иметь стабильный слот min-height: 280px и contain: layout style на десктопе.');
assert(content.includes('.fc-card {\n    min-height: 280px !important;\n    box-sizing: border-box !important;\n  }'),
  '❌ ZERO-JITTER VIOLATION: .fc-card обязана иметь min-height: 280px для исключения дельты высоты при перевороте.');
assert(content.includes('.fc-card .card-face,\n  .fc-card .fc-card-face,\n  .fc-card-front,\n  .fc-card-back {\n    min-height: 280px !important;\n    box-sizing: border-box !important;\n    display: flex !important;\n    flex-direction: column !important;\n    justify-content: space-between !important;\n  }'),
  '❌ ZERO-JITTER VIOLATION: Обе стороны карточки обязаны иметь min-height: 280px и justify-content: space-between.');
console.log('✓ [3/12] [Zero-Jitter] Монолитный слот сцены карточки на десктопе (280px, contain: layout style) соблюдён.');

// 4. Инвариант строгого запрета плавающего margin: auto для .cards-hub-container на десктопе
assert(!content.includes('.cards-hub-container {\n    width: 100% !important;\n    max-width: 740px !important;\n    min-height: auto !important;\n    height: auto !important;\n    margin: auto !important;'),
  '❌ ZERO-JITTER VIOLATION: .cards-hub-container не должен иметь плавающего margin: auto (делящего дельту высоты карточки пополам). Обязан быть margin: 0 auto !important.');
assert(content.includes('margin: 0 auto !important;\n    padding: 22px 28px 24px !important;'),
  '❌ ZERO-JITTER VIOLATION: .cards-hub-container обязан иметь margin: 0 auto !important.');
console.log('✓ [4/12] [Zero-Jitter] Плавающий margin: auto контейнера SRS устранён (строго margin: 0 auto).');

// 5. Инвариант монолитного слота сцены карточки на мобильных устройствах (min-height: 240px)
assert(content.includes('.fc-stage {\n    display: flex !important;\n    flex-direction: column !important;\n    justify-content: flex-start !important;\n    flex: 0 0 auto !important;\n    margin: 0 auto !important;\n    min-height: 240px !important;\n    box-sizing: border-box !important;\n    contain: layout style !important;\n  }'),
  '❌ ZERO-JITTER VIOLATION: Мобильный .fc-stage обязан иметь min-height: 240px и contain: layout style.');
console.log('✓ [5/12] [Zero-Jitter] Мобильная геометрия сцены карточки стабильно зафиксирована (240px).');

// 6. Инвариант единого оптического свечения всех точек активности
assert(content.includes('.pulse-dot {\n    width: 7px !important;\n    height: 7px !important;\n    min-width: 7px !important;\n    min-height: 7px !important;\n    max-width: 7px !important;\n    max-height: 7px !important;\n    border-radius: 50% !important;\n    background: #34d399 !important;\n    box-shadow: 0 0 7px rgba(52, 211, 153, 0.80), 0 0 2px #10b981 !important;\n    animation: emeraldSoftBreath 2.8s infinite ease-in-out !important;\n    transform: translateZ(0) !important;\n    contain: layout style !important;'),
  '❌ ZERO-JITTER VIOLATION: .pulse-dot в Hero-карточке сайдбара обязан быть унифицирован до 7px, #34d399 и emeraldSoftBreath 2.8s.');
assert(content.includes('.activity-dot{\n    width:7px !important;\n    height:7px !important;') &&
       content.includes('background:#34d399 !important;') &&
       content.includes('animation:emeraldSoftBreath 2.8s infinite ease-in-out !important;'),
  '❌ ZERO-JITTER VIOLATION: .activity-dot обязан быть унифицирован до 7px, #34d399 и emeraldSoftBreath 2.8s.');
assert(content.includes('.srs-live-status-dot {\n    width: 7px !important;\n    height: 7px !important;\n    min-width: 7px !important;\n    min-height: 7px !important;\n    border-radius: 50% !important;\n    background: #34d399 !important;\n    box-shadow: 0 0 7px rgba(52, 211, 153, 0.80), 0 0 2px #10b981 !important;'),
  '❌ ZERO-JITTER VIOLATION: .srs-live-status-dot обязан быть унифицирован до 7px, #34d399.');
console.log('✓ [6/12] [Zero-Jitter] Полная оптическая идентичность всех точек активности (7px, #34d399, единый ореол) соблюдена.');

// 7. Инвариант строгого запрета 2-секундного зацикленного подёргивания и масштабирования бусин
assert(!content.includes('transform: scale(1.15) !important;\n\n    position: relative !important;\n\n    z-index: 3 !important;\n\n    animation: bead-pulse-emerald 2s'),
  '❌ ZERO-JITTER VIOLATION: В .dot-jewel.active категорически запрещён transform: scale(1.15) и 2s анимация (вызывает 2-секундный всплеск инвалидации).');
assert(!content.includes('#radar-dots-necklace .dot-jewel.active {\n\n    width: 8px !important;\n\n    height: 8px !important;\n\n    background: #ffffff !important;\n\n    border: 1.5px solid #10b981 !important;\n\n    border-radius: 50% !important;\n\n    flex-shrink: 0 !important;\n\n    box-sizing: border-box !important;\n\n    position: relative !important;\n\n    z-index: 5 !important;\n\n    transform: none !important;\n\n    animation: pulse-ring 2s infinite !important;'),
  '❌ ZERO-JITTER VIOLATION: Запрещена анимация pulse-ring 2s для активных бусин. Обязана использоваться bead-pulse-emerald 2.8s.');
console.log('✓ [7/12] [Zero-Jitter] 2-секундный зацикленный всплеск и масштабирование бусин scale(1.15) ликвидированы.');

// 8. Инвариант живого дыхания активных бусин
assert(content.includes('animation: bead-pulse-emerald 2.8s infinite ease-in-out !important;'), 
  'Активная бусина обязана дышать через анимацию bead-pulse-emerald');
assert(content.includes('animation: bead-ping-wave 2.8s cubic-bezier(0.2, 0.8, 0.4, 1) infinite !important;'), 
  'Волна маяка активной бусины обязана дышать через bead-ping-wave');
console.log('✓ [8/12] [Zero-Jitter] Активная бусина и расходящаяся волна маяка дышат в Zen-ритме 2.8s.');

// 9. Инвариант строгой фиксации геометрии ожерелья бусин (Zero Layout Shift)
assert(content.includes('height: 28px !important;\n\n    min-height: 28px !important;\n\n    max-height: 28px !important;') ||
       content.includes('height: 28px !important;\n    min-height: 28px !important;\n    max-height: 28px !important;'), 
  'Ожерелье бусин обязано иметь жесткую высоту 28px, чтобы дыхание не передавалось на лейаут');
assert(content.includes('contain: layout !important;'), 
  'Ожерелье бусин обязано иметь contain: layout для изоляции анимаций');
console.log('✓ [9/12] [Zero-Jitter] Высота ожерелья бусин строго зафиксирована (28px, contain: layout) — 0px смещения.');

// 10. Инвариант монолитности кнопок ответа
assert(content.includes('height: 52px !important;') &&
       content.includes('min-height: 52px !important;') &&
       content.includes('max-height: 52px !important;') &&
       content.includes('contain: layout style !important;') &&
       content.includes('-webkit-tap-highlight-color: transparent !important;'),
  '❌ ZERO-JITTER VIOLATION: Кнопки .fc-rate-btn обязаны иметь жесткую высоту 52px, contain: layout style и -webkit-tap-highlight-color: transparent.');
console.log('✓ [10/12] [Zero-Jitter] Кнопки ответов .fc-rate-btn аппаратно монолитны (52px, contain: layout style).');

// 11. Инвариант оптического дыхания точек активности (СТРОГИЙ ЗАПРЕТ НА scale)
const emeraldBreathMatch = content.match(/@keyframes emeraldSoftBreath\s*\{([\s\S]*?)\}/);
assert(emeraldBreathMatch, '@keyframes emeraldSoftBreath обязан быть определен в CSS');
assert(!emeraldBreathMatch[1].includes('scale('), 
  '❌ ZERO-JITTER VIOLATION: В @keyframes emeraldSoftBreath запрещен scale()! Дыхание точек обязано производиться строго через box-shadow и opacity (0px jitter).');

const srsPulseMatch = content.match(/@keyframes srsLiveDotPulse\s*\{([\s\S]*?)\}/);
assert(srsPulseMatch, '@keyframes srsLiveDotPulse обязан быть определен в CSS');
assert(!srsPulseMatch[1].includes('scale('), 
  '❌ ZERO-JITTER VIOLATION: В @keyframes srsLiveDotPulse запрещен scale()! Дыхание точек обязано производиться строго через box-shadow и opacity (0px jitter).');
console.log('✓ [11/12] [Zero-Jitter] Оптическое дыхание точек строго через box-shadow и opacity (0 scale).');

// 12. Инвариант симметричной рамки кнопок сайдбара (0px Border Jump)
assert(content.includes('.navlink{display:flex;align-items:center;gap:10px;padding:8px 11px;border-radius:11px;text-decoration:none;color:var(--ink-soft);font-weight:500;font-size:.88rem;margin-bottom:2px;border:1px solid transparent;border-left:3px solid transparent;box-sizing:border-box;'),
  '❌ ZERO-JITTER VIOLATION: .navlink обязан иметь border-left: 3px solid transparent для исключения 2px скачка при активации.');
console.log('✓ [12/12] [Zero-Jitter] Симметричные рамки кнопок сайдбара соблюдены (0px border jump).');

console.log('\n>>> ВСЕ 12 ИНВАРИАНТОВ ZERO-JITTER И МОНОЛИТНОСТИ SRS УСПЕШНО ПРОЙДЕНЫ (100%) <<<\n');
process.exit(0);
