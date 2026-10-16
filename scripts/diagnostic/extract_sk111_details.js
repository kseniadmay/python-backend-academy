const fs = require('fs');
const html = fs.readFileSync('academy.html', 'utf8');

// Извлечем заголовки конспектов К-001, К-002, К-003
['К-001', 'К-002', 'К-003'].forEach(k => {
  const re = new RegExp(`['"]${k}['"]\\s*:\\s*\\{\\s*id:\\s*['"]${k}['"],\\s*title:\\s*['"]([^'"]+)['"]`);
  const m = html.match(re);
  console.log(`Конспект ${k}:`, m ? m[1] : 'not found');
});

// Извлечем заголовки колод Ф-001 .. Ф-009
['Ф-001', 'Ф-002', 'Ф-003', 'Ф-004', 'Ф-005', 'Ф-006', 'Ф-007', 'Ф-008', 'Ф-009'].forEach(f => {
  const re = new RegExp(`['"]${f}['"]\\s*:\\s*\\{\\s*id:\\s*['"]${f}['"],\\s*title:\\s*['"]([^'"]+)['"]`);
  const m = html.match(re);
  console.log(`Колода ${f}:`, m ? m[1] : 'not found');
});

// Извлечем заголовки задач 20, 19, 39, 255, 258
[20, 19, 39, 255, 258].forEach(tid => {
  const re = new RegExp(`(?:id:\\s*${tid}|['"]?${tid}['"]?\\s*:\\s*\\{\\s*id:\\s*${tid})[\\s\\S]*?title:\\s*['"]([^'"]+)['"]`);
  const m = html.match(re);
  console.log(`Задача #${tid}:`, m ? m[1] : 'not found');
});
