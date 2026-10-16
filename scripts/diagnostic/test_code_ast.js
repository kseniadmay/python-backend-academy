let marked;
try {
  marked = require('marked');
} catch (e) {
  console.log('[SKIP] Optional module "marked" not installed. Scratch test skipped.');
  process.exit(0);
}


const md = `---

────────────────────────────────────────────────────────────────

- ## Header

\`\`\`python
print(1)
\`\`\`

Paragraph text`;

console.log(marked.lexer(md));
