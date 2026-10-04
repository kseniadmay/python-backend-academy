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

async function findC3() {
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
    
    const matches = all.filter(r => {
      const t = (r.key || []).map(x => typeof x === 'string' ? x : (x.text || '')).join('');
      return t.includes('C3-линеаризация');
    });

    return JSON.stringify(matches.map(m => ({
      id: m._id,
      parent: m.parent,
      f: m.f,
      text: (m.key || []).map(x => typeof x === 'string' ? x : (x.text || '')).join('')
    })));
  })()`;

  const res = await evalCDP(code);
  console.log(JSON.stringify(JSON.parse(res.value), null, 2));
}

findC3();
