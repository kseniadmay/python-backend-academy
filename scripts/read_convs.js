const fs = require('fs');

function dumpUserMessages(convId) {
  console.log(`\n================= CONV: ${convId} =================`);
  const p = `C:\\Users\\fury6\\.gemini\\antigravity\\brain\\${convId}\\.system_generated\\logs\\transcript.jsonl`;
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n').filter(Boolean);
  lines.forEach(l => {
    try {
      const obj = JSON.parse(l);
      if (obj.type === 'USER_INPUT' || (obj.content && obj.content.includes('<USER_REQUEST>'))) {
        console.log(`[USER ${obj.created_at}]`);
        console.log(obj.content);
        console.log('--------------------------------------------------');
      }
    } catch (_) {}
  });
}

dumpUserMessages('48fa7d53-7b2c-4c44-96ef-b5b6bc72ba4b');
dumpUserMessages('6ae89118-fd8e-4afb-b15c-4c5644a11c6d');
