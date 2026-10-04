const marked = require('marked');

const md = `---

────────────────────────────────────────────────────────────────

- ## Header

\`\`\`python
print(1)
\`\`\`

Paragraph text`;

console.log(marked.lexer(md));
