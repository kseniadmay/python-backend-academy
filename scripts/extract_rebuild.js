const fs = require('fs');
const file = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\3994ccaf-0f12-4688-aa5a-f379cf78c408\\.system_generated\\logs\\transcript.jsonl';
const content = fs.readFileSync(file, 'utf8');

for (const line of content.split('\n')) {
  if (line.includes('Complete script to rebuild RemNote 42-day schedule')) {
    const obj = JSON.parse(line);
    const code = obj.tool_calls[0].args.CodeContent;
    console.log(code.substring(0, 1000));
  }
}
