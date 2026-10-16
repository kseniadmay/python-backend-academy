const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

function resolveFullText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) return key.map(p => typeof p === 'string' ? p : (p.text || '')).join('');
  return '';
}

const topics = [
  'LEGB, срезы, генераторы, yield, lambda',
  'Декораторы, замыкания, functools.wraps',
  'dict',
  'C3-линеаризация',
  'Методы, статусы, заголовки',
  'Архитектурные ограничения, версии',
  'MTV, QuerySet, Admin',
  'Сериализаторы, роутинг, DI',
  'JWT, OAuth2, сессии',
  'CORS, CSRF, XSS',
  'Big O, оценка роста',
  'Статический массив, два указателя',
  'Узлы, указатели, LIFO/FIFO',
  'Иерархии и структуры мгновенного доступа',
  'Представление графа',
  'Классика перед живым кодингом',
  'SELECT, WHERE, JOIN',
  'Подзапросы, CTE',
  'Нормализация, ключи',
  'ACID, изоляция, дедлоки',
  'SQLAlchemy, миграции',
  'MongoDB, Redis, стратегии',
  'SOLID, DRY, KISS, YAGNI',
  'Separation of Concerns',
  'Singleton, Factory',
  'Strategy, Observer',
  'Decorator, Repository',
  'Сборка недели',
  'Ветки, merge/rebase',
  'Image, Container, Dockerfile',
  'Multi-stage, реестры',
  'Пайплайны, раннеры',
  'CLI, процессы, файлы',
  'Celery, pytest, логирование',
  'ФИНАЛЬНЫЙ ЭКЗАМЕН'
];

let foundCount = 0;
topics.forEach(t => {
  const m = allRems.filter(r => resolveFullText(r.key).toLowerCase().includes(t.toLowerCase().slice(0, 15)));
  if (m.length > 0) foundCount++;
  console.log(`Topic "${t.slice(0, 25)}": ${m.length > 0 ? 'FOUND (' + m[0]._id + ')' : 'NOT FOUND'}`);
});
console.log(`Total found topics: ${foundCount}/${topics.length}`);
