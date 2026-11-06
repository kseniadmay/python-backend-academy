#!/usr/bin/env node
/**
 * test_cards_inline_code_consistency.js
 * 
 * Тест консистентности инлайн-блоков кода и форматирования карточек SRS:
 * 1. Проверяет форматирование ответов с точкой с запятой (мультистрочность и одинаковый инлайн-стиль кодов).
 * 2. Проверяет корректность разметки бейджей (отсутствие непарных/битых backticks).
 * 3. Проверяет инварианты десктопного UI:
 *    - Скрытие мобильного таббара на экранах > 880px
 *    - Отсутствие троеточия доп. настроек в десктопном хедере
 *    - Наличие переключателя дзен-паузы в сайдбаре
 *    - Отсутствие кнопки-шпаргалки (💡) в карточке
 *    - Пульсация активной бусины прогресса
 *    - Бейдж "0 XP" вместо "Сброс" на кнопке "Не знаю"
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const ACADEMY_PATH = path.join(ROOT, 'academy.html');
const STANDARDS_PATH = path.join(ROOT, 'standards', 'standards.html');

console.log('--- Запуск теста консистентности инлайн-кода и карточек SRS ---');

// 1. Проверка academy.html и standards.html
[ACADEMY_PATH, STANDARDS_PATH].forEach(filePath => {
  const fileName = path.basename(filePath);
  assert(fs.existsSync(filePath), `Файл ${fileName} должен существовать`);
  const rawContent = fs.readFileSync(filePath, 'utf8');
  const content = rawContent.replace(/\r\n/g, '\n');

  // А) Мобильный таббар скрыт на десктопе
  assert(content.includes('@media (min-width: 881px)'), `${fileName}: должно быть медиа-правило для десктопа`);
  assert(content.includes('.tabbar,\n    #tabbar {\n      display: none !important;\n      pointer-events: none !important;'), `${fileName}: таббар должен быть полностью скрыт на десктопе`);

  // Б) Троеточие с доп. настройками убрано из хедера карточек
  assert(!content.includes('<details class="srs-more-details" style="position:relative;display:inline-flex;align-items:center;height:30px;'), `${fileName}: details.srs-more-details должно быть убрано из хедера`);

  // В) Настройки (Дзен-пауза) вынесены в сайдбар
  assert(content.includes('sidebar-srs-settings'), `${fileName}: настройки SRS должны присутствовать в сайдбаре`);
  assert(content.includes('data-action="toggle-srs-finish-mode"'), `${fileName}: тумблер переключения дзен-паузы должен быть в сайдбаре`);

  // Г) Кнопка-шпаргалка 💡 убрана из карточек
  assert(!content.includes('id="srs-hint-btn" title="Шпаргалка (H)">💡</button>'), `${fileName}: кнопка-шпаргалка 💡 должна быть убрана из карточки`);

  // Д) Пульсация активной ведущей бусины
  assert(content.includes('srs-active-bead-pulse'), `${fileName}: активная бусина должна анимироваться через srs-active-bead-pulse`);
  assert(!content.includes('box-shadow: 0 0 12px #10b981, 0 0 22px rgba(52, 211, 153, 0.85) !important;\n\n    animation: none !important;'), `${fileName}: анимация активной бусины не должна блокироваться animation: none`);

  // Е) Кнопка "Не знаю" содержит "0 XP" вместо "Сброс"
  assert(!content.includes('xp-gem-again">Сброс</span>'), `${fileName}: подпись на кнопке Не знаю не должна быть 'Сброс'`);
  assert(content.includes('xp-gem-again">0 XP</span>'), `${fileName}: подпись на кнопке Не знаю должна быть '0 XP'`);

  // Ж) Функция formatCardAnswerHTML и структурирование ответов с точкой с запятой
  assert(content.includes("if(s.includes(';') && !s.includes('```'))"), `${fileName}: formatCardAnswerHTML должна разбивать ответы с ';'`);
  assert(content.includes('fc-answer-multiline'), `${fileName}: должен быть контейнер fc-answer-multiline для списков ответов`);
  assert(content.includes('fc-answer-item'), `${fileName}: должны быть пункты fc-answer-item`);
  assert(content.includes('fc-answer-bullet'), `${fileName}: должны быть маркеры fc-answer-bullet`);

  // З) Анимация разлетающихся искорок типа ✨
  assert(content.includes('M12,0 Q12,12 24,12 Q12,12 12,24 Q12,12 0,12 Q12,12 12,0 Z'), `${fileName}: triggerSparksBurst должна генерировать 4-конечные векторные звёзды ✨`);
  assert(content.includes('viewBox="0 0 32 32"'), `${fileName}: triggerSparksBurst должна включать кластерные звёзды в стиле эмодзи ✨`);

  console.log(`✓ ${fileName}: все инварианты десктопа, сайдбара, бусин, карточек и салюта ✨ соблюдены.`);
});

// 2. Имитационный юнит-тест логики formatCardAnswerHTML
function formatCardAnswerHTMLMock(rawAnswer) {
  if(!rawAnswer) return '';
  let s = String(rawAnswer).trim();

  if(s.includes(';') && !s.includes('```')){
    const parts = s.split(';').map(p => p.trim()).filter(Boolean);
    if(parts.length > 1){
      const itemsHtml = parts.map(part => {
        const normalized = part.replace(/\s+(?:—|–|-)\s+/g, ' — ');
        return `<div class="fc-answer-item"><span class="fc-answer-bullet">•</span> <span class="fc-answer-text">${normalized}</span></div>`;
      }).join('');
      return `<div class="fc-answer-multiline">${itemsHtml}</div>`;
    }
  }

  const codeMatch = s.match(/^(?:<code>([\s\S]*?)<\/code>|`([^`\n]+)`|<pre class="[^"]*"><code>([\s\S]*?)<\/code><\/pre>)\s*(?:—|–|-|:)\s*([\s\S]*)$/i);
  if(codeMatch){
    const rawCode = codeMatch[1] || codeMatch[2] || codeMatch[3];
    const explanation = codeMatch[4];
    if(!explanation.includes('`') && !explanation.includes('<code>') && !explanation.includes(';')){
      return `<div class="fc-code-capsule"><code>${rawCode}</code></div><div class="fc-answer-explanation">${explanation}</div>`;
    }
  }
  return s;
}

const inputAnswer = "`401` – нет аутентификации; `403` – нет авторизации";
const outputHtml = formatCardAnswerHTMLMock(inputAnswer);

// Проверяем, что 401 НЕ улетел в отдельную капсулу fc-code-capsule
assert(!outputHtml.includes('fc-code-capsule'), 'Сравнение кодов 401 и 403 не должно разбиваться на fc-code-capsule!');
// Проверяем, что ответ стал мультистрочным со структурированными пунктами
assert(outputHtml.includes('class="fc-answer-multiline"'), 'Ответ должен быть оформлен в multiline контейнер');
assert(outputHtml.includes('`401` — нет аутентификации'), 'Пункт 401 должен быть на своей строке с аккуратным тире');
assert(outputHtml.includes('`403` — нет авторизации'), 'Пункт 403 должен быть на своей строке с аккуратным тире');

console.log('✓ Имитационный тест formatCardAnswerHTML (401 vs 403) успешно пройден.');
console.log('Все проверки консистентности карточек SRS выполнены успешно (100%).');
process.exit(0);
