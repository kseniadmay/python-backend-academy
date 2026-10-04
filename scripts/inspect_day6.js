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

async function inspectDay6() {
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
    const all = await rc.DatabaseStore.fetchAllImpl();
    
    // Day 06 id: SZAGTXB0Rxs2nCtD3
    const day6Kids = all.filter(r => r.parent === 'SZAGTXB0Rxs2nCtD3').sort((a, b) => (a.f || '').localeCompare(b.f || ''));
    return JSON.stringify(day6Kids.map(k => ({
      id: k._id,
      f: k.f,
      key: k.key,
      text: (k.key || []).map(x => typeof x === 'string' ? x : (x.text || '')).join('')
    })));
  })()`;

  const res = await evalCDP(code);
  console.log(JSON.stringify(JSON.parse(res.value), null, 2));
}

inspectDay6();
