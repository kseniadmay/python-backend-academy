let marked;
try {
  marked = require('marked');
} catch (e) {
  console.log('[SKIP] Optional module "marked" not installed. Scratch test skipped.');
  process.exit(0);
}


const md = `
- ## Dict: мгновенный поиск по ключу
- Словарь – структура «ключ – значение» на основе хэш-таблицы.
\`\`\`python
d['key']  # O(1) – мгновенный доступ
d['new'] = 10  # O(1) – добавление
\`\`\`
- Это называется **амортизированным O(1)**.
`;

console.log(JSON.stringify(marked.lexer(md), null, 2));
