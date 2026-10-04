const fs = require('fs');
const filePath = 'C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md';
let content = fs.readFileSync(filePath, 'utf8');

content = content.replace(
  '    - Интервальное повторение RemNote по всем модулям (фильтр "Stale" и "Growing"), без нового материала',
  '    - [ ] Интервальное повторение RemNote по всем модулям (фильтр "Stale" и "Growing"), без нового материала'
);

content = content.replace(
  '    - Комплексное повторение ключевых концепций Web & Backend, БД, Архитектуры и Инфраструктуры',
  '    - [ ] Комплексное повторение ключевых концепций Web & Backend, БД, Архитектуры и Инфраструктуры'
);

content = content.replace(
  '    - Прошёл весь путь: Python → Web & Backend → Алгоритмы → БД → Архитектура → Инфраструктура',
  '    - [ ] Прошёл весь путь: Python → Web & Backend → Алгоритмы → БД → Архитектура → Инфраструктура'
);

content = content.replace(
  '    - Закрыл разгрузочные дни (7, 14, 21, 28, 35) без долгов на сегодня',
  '    - [ ] Закрыл разгрузочные дни (7, 14, 21, 28, 35) без долгов на сегодня'
);

fs.writeFileSync(filePath, content, 'utf8');
console.log('Final fixes applied to markdown file.');
