const fs = require('fs');

const p = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\48fa7d53-7b2c-4c44-96ef-b5b6bc72ba4b\\.system_generated\\logs\\transcript.jsonl';
const lines = fs.readFileSync(p, 'utf8').split('\n').filter(Boolean);

for (let i = 25; i < lines.length; i++) {
  try {
    const o = JSON.parse(lines[i]);
    if (o.type === 'USER_INPUT') {
      console.log(`\n--- STEP ${i} USER ---`);
      console.log(o.content);
    } else if (o.type === 'PLANNER_RESPONSE' && o.content) {
      console.log(`\n--- STEP ${i} AI ---`);
      console.log(o.content.slice(0, 300));
    }
  } catch (_) {}
}
