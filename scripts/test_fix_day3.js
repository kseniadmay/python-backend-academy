const http = require('http');

function evalCDP(jsCode) {
  return new Promise((resolve, reject) => {
    const req = http.request('http://127.0.0.1:9999/eval', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.write(jsCode);
    req.end();
  });
}

async function fixDay3() {
  const code = `(async () => {
    const el = document.querySelector('[data-rem-id]');
    const fiberKey = Object.keys(el || {}).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
    let curr = el ? el[fiberKey] : null;
    let rem = null;
    while (curr) {
      if (curr.memoizedProps && curr.memoizedProps.rem && curr.memoizedProps.rem.getTinyGraph) {
        rem = curr.memoizedProps.rem;
        break;
      }
      curr = curr.return;
    }
    const tg = rem.getTinyGraph();
    const rc = tg.getRemCollection();
    
    const updRes = await rc.update('0IpA4W3iyh9beq2Lh', {
      $set: {
        key: ['__dict__, __slots__, dataclasses, namedtuple, super()']
      }
    });

    const targetRem = await rc.getRemById('0IpA4W3iyh9beq2Lh');
    const text = await targetRem.text();
    return JSON.stringify({ updRes, key: targetRem.key, text });
  })()`;

  const res = await evalCDP(code);
  console.log('Fix Day 3 result:', res);
}

fixDay3();
