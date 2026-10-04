const marked = require('marked');
const fs = require('fs');

const md = [
    '# К-001. Структуры данных Python_ list, dict, set',
    '',
    '- 📖 Перечитать конспект: Структуры данных Python: list, dict, set >> Конспект перечитан и усвоен.',
    '',
    '## Почему выбор структуры данных важен',
    '',
    'Программа идеально работает с десятью элементами – и зависает на десяти тысячах.',
    '',
    '## List: когда важен порядок',
    '',
    'Список – динамический массив. Идеален, когда нужно сохранить порядок элементов.',
    '',
    '- **Быстрые операции – O(1):** `arr.append(x)`.',
    '- **Медленные операции – O(n):** `arr.insert(0, x)`.',
    '',
    'Почему `insert(0, x)` медленный? Python сдвигает элементы.'
].join('\n');

const tokens = marked.lexer(md);
tokens.forEach(t => {
    console.log(t.type, t.depth || '', (t.text || '').slice(0, 50));
    if (t.items) t.items.forEach(it => console.log('  item:', it.text.slice(0, 40)));
});
