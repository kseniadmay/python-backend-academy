const marked = require('marked');

const md = `📖 Перечитать конспект: frozenset_ неизменяемое множество >> Конспект перечитан и усвоен.

---

- ## frozenset – неизменяемая версия set

**\`frozenset\`** – то же множество (уникальные элементы, быстрая проверка на вхождение через хэш-таблицу), но неизменяемое после создания: нет \`add()\`, \`remove()\`, \`update()\`.

\`\`\`python
s = {1, 2, 3}
s.add(4)  # OK – обычный set изменяемый
print(s)  # {1, 2, 3, 4}

fs = frozenset([1, 2, 3])
fs.add(4)  # AttributeError: 'frozenset' object has no attribute 'add'
\`\`\`

---

- ## Главная практическая причина существования – хэшируемость

Как и \`tuple\` в сравнении со \`list\`, \`frozenset\` в сравнении с \`set\` неизменяем – а значит, хэшируем.`;

const tokens = marked.lexer(md);
console.log("Tokens count:", tokens.length);
tokens.forEach((t, i) => {
    console.log(`[${i}] type: ${t.type}, depth: ${t.depth || ''}, text: ${JSON.stringify((t.text || '').slice(0, 60))}`);
    if (t.items) {
        t.items.forEach(it => console.log(`    item: ${JSON.stringify(it.text.slice(0, 60))}`));
    }
});
