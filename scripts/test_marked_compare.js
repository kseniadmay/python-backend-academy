let marked;
try {
  marked = require('marked');
} catch (e) {
  console.log('[SKIP] Optional module "marked" not installed. Scratch test skipped.');
  process.exit(0);
}


console.log('=== TEST A: Plain Markdown ===');
const mdA = `
## Заголовок 1

Текст 1

Текст 2

## Заголовок 2

Текст 3
`;
console.log(JSON.stringify(marked.lexer(mdA), null, 2));

console.log('\n=== TEST B: Bulleted Markdown ===');
const mdB = `
- ## Заголовок 1
- Текст 1
- Текст 2
- ## Заголовок 2
- Текст 3
`;
console.log(JSON.stringify(marked.lexer(mdB), null, 2));
