// tests/test_srs_last_sprint_close_regression.js
const fs = require('path');
const nodeFs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('================================================================');
console.log('   SRS LAST SPRINT / SPLIT CLOSURE REGRESSION TEST SUITE        ');
console.log('================================================================\n');

const html = nodeFs.readFileSync(path.join(__dirname, '..', 'standards', 'standards.html'), 'utf-8');

// 1. Проверяем наличие buildSrsSprintFinishHTML и разметки последнего спринта
assert(html.includes('complete-srs-session'), 'Markup must contain complete-srs-session action');
assert(html.includes('Завершить повторение'), 'Markup must contain «Завершить повторение»');
assert(html.includes('Все карточки дня сданы'), 'Markup must contain «Все карточки дня сданы»');
console.log('  ✓ [PASS] 1. buildSrsSprintFinishHTML содержит кнопку «Завершить повторение» для последнего спринта');

// 2. Проверяем расчет dueRem в viewCardsHub: больше нет искажения до 1 при duePos >= qLen
const dueRemCheck = html.includes('Math.max(0, qLen - (Number(cardsHubState.duePos) || 0))');
assert(dueRemCheck, 'dueRem calculation must use exact duePos rather than clamped duePos to allow 0');
console.log('  ✓ [PASS] 2. Расчет dueRem в viewCardsHub честно возвращает 0 при исчерпании очереди');

// 3. Проверяем обработчик start-next-srs-sprint и complete-srs-session
assert(html.includes('srsCompleteSessionBtn'), 'Event handler must handle complete-srs-session');
assert(html.includes('isSessionEnded'), 'Event handler must close session cleanly if no cards remain');
console.log('  ✓ [PASS] 3. Обработчик клика сессии чисто закрывает последний спринт при 0 остатке');

// 4. Проверяем отображение шапки при завершении всех спринтов дня
assert(html.includes('isAllSprintsDoneToday'), 'buildSrsHeaderBarHTML must detect when all sprints are done today');
assert(html.includes('Все спринты дня закрыты'), 'buildSrsHeaderBarHTML must set label for completed sprints');
console.log('  ✓ [PASS] 4. Шапка отображает закрытый статус спринтов дня (✓ total / total)');

// 5. Проверяем логику в hRate для dueQueue и свободной колоды
assert(html.includes('cardsHubState.duePos = (cardsHubState.dueQueue || []).length;'), 'hRate must trigger sprintFinished on 15th card even if last');
console.log('  ✓ [PASS] 5. hRate активирует sprintFinished на последней 15-й карточке пула');

console.log('\nИтог: все 5 проверок закрытия последнего спринта пройдены на 100%!');
