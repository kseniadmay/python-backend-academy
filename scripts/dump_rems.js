const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => ws.send(JSON.stringify({ id: 1, method: 'Target.getTargets' }));

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    const target = msg.result.targetInfos.find(t => t.url && t.url.includes('GwREY4bq5eQvPyeAB'));
    ws.send(JSON.stringify({ id: 2, method: 'Target.attachToTarget', params: { targetId: target.targetId, flatten: true } }));
  }
  if (msg.id === 2) {
    const sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          const els = Array.from(document.querySelectorAll('[data-rem-id]'));
          let rem = null;
          for (const el of els) {
            const fiberKey = Object.keys(el || {}).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
            let curr = el ? el[fiberKey] : null;
            while (curr) {
              if (curr.memoizedProps && curr.memoizedProps.rem && curr.memoizedProps.rem.getTinyGraph) {
                rem = curr.memoizedProps.rem;
                break;
              }
              curr = curr.return;
            }
            if (rem) break;
          }
          const tg = rem.getTinyGraph();
          const rc = tg.getRemCollection();
          const all = await rc.DatabaseStore.fetchAllImpl();
          return all.map(r => ({
            _id: r._id,
            parent: r.parent,
            f: r.f,
            type: r.type,
            key: r.key,
            apu: r.apu ? true : false
          }));
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\all_rems_dump.json', JSON.stringify(msg.result.result.value), 'utf8');
    console.log('Saved all_rems_dump.json, count =', msg.result.result.value.length);
    ws.close();
  }
};
