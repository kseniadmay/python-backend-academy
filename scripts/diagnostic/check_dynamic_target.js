const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.getTargets'
  }));
};

let sessionId = null;

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    const target = msg.result.targetInfos.find(t => t.url && t.url.includes('GwREY4bq5eQvPyeAB'));
    if (!target) {
      console.error('Target not found!');
      ws.close();
      return;
    }
    console.log('Connecting to target:', target.targetId, target.title);
    ws.send(JSON.stringify({
      id: 2,
      method: 'Target.attachToTarget',
      params: { targetId: target.targetId, flatten: true }
    }));
  }
  if (msg.id === 2) {
    sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
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
            if (!rem) return JSON.stringify({ error: 'rem not found' });
            
            const tg = rem.getTinyGraph();
            const rc = tg.getRemCollection();
            const ds = rc.DatabaseStore;
            const all = await ds.fetchAllImpl();
            
            const rootId = 'GwREY4bq5eQvPyeAB';
            const rootKids = all.filter(r => r.parent === rootId);
            const broken = all.filter(r => JSON.stringify(r.key || '').includes('se0t1PxtnIsLC14tQ'));
            
            return JSON.stringify({
              totalAll: all.length,
              rootKidsCount: rootKids.length,
              brokenCount: broken.length
            });
          } catch (e) {
            return JSON.stringify({ error: e.message });
          }
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    console.log('Check result:', msg.result.result.value);
    ws.close();
  }
};