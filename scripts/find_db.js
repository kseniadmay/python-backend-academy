const fs = require('fs');
const path = require('path');

const file = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\3994ccaf-0f12-4688-aa5a-f379cf78c408\\.system_generated\\logs\\transcript.jsonl';
if (fs.existsSync(file)) {
  const content = fs.readFileSync(file, 'utf8');
  for (const line of content.split('\n')) {
    if (line.includes('quanta') || line.includes('DatabaseSync') || line.includes('better-sqlite3')) {
      const idx = line.indexOf('DatabaseSync');
      if (idx !== -1) {
        console.log(line.substring(Math.max(0, idx - 50), Math.min(line.length, idx + 150)));
      }
    }
  }
}
