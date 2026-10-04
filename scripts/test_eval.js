const http = require('http');

function evalInPage(code) {
  return new Promise((resolve, reject) => {
    const req = http.request('http://127.0.0.1:9999/eval', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.write(code);
    req.end();
  });
}

async function run() {
  const code = `
    (async () => {
      const doc = await rc.getRemById('GwREY4bq5eQvPyeAB');
      const text = await doc.text();
      return text;
    })()
  `;
  const res = await evalInPage(code);
  console.log('Result:', res);
}

run();
