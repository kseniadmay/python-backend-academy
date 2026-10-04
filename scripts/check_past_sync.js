const fs = require('fs');
const file = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\3994ccaf-0f12-4688-aa5a-f379cf78c408\\.system_generated\\logs\\transcript.jsonl';
const content = fs.readFileSync(file, 'utf8');

for (const line of content.split('\n')) {
  if (line.includes('HKILo3FLoxkwXggHD')) {
    try {
      const obj = JSON.parse(line);
      if (obj.type === 'PLANNER_RESPONSE' || obj.type === 'TOOL_CALL') {
        console.log('--- FOUND ---');
        console.log((obj.content || JSON.stringify(obj.tool_calls || '')).substring(0, 300));
      }
    } catch(e) {}
  }
}
