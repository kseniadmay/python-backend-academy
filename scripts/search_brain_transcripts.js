const fs = require('fs');
const path = require('path');

const brain = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain';
const dirs = fs.readdirSync(brain);

const matches = [];

for (const d of dirs) {
  const tPath = path.join(brain, d, '.system_generated', 'logs', 'transcript.jsonl');
  if (fs.existsSync(tPath)) {
    try {
      const content = fs.readFileSync(tPath, 'utf8');
      if (content.includes('1/3/7') || content.includes('повторов') || content.includes('плагин') || content.includes('интервал')) {
        // find exact line or snippet
        const lines = content.split('\n');
        for (const l of lines) {
          if (l.includes('1/3/7') || (l.includes('плагин') && (l.includes('RemNote') || l.includes('повтор') || l.includes('режим') || l.includes('интервал')))) {
            matches.push({ conv: d, line: l.slice(0, 300) });
            break;
          }
        }
      }
    } catch (_) {}
  }
}

console.log(`Found ${matches.length} matches in conversations:`);
matches.forEach(m => {
  console.log(`\nConv: ${m.conv}`);
  console.log('Sample:', m.line);
});
