const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  ws.send(JSON.stringify({ id: 1, method: 'Target.getTargets' }));
};

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    const target = msg.result.targetInfos.find(t => t.url && t.url.includes('GwREY4bq5eQvPyeAB'));
    ws.send(JSON.stringify({
      id: 2,
      method: 'Target.attachToTarget',
      params: { targetId: target.targetId, flatten: true }
    }));
  }
  if (msg.id === 2) {
    const sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
            const rootId = 'GwREY4bq5eQvPyeAB';
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
            const ds = rc.DatabaseStore;
            const all = await ds.fetchAllImpl();
            
            // Build tree descendants of rootId
            const descendants = new Set();
            const queue = [rootId];
            const childrenMap = {};
            for (const r of all) {
              if (r.parent) {
                if (!childrenMap[r.parent]) childrenMap[r.parent] = [];
                childrenMap[r.parent].push(r);
              }
            }
            while (queue.length > 0) {
              const cur = queue.shift();
              const kids = childrenMap[cur] || [];
              for (const k of kids) {
                if (!descendants.has(k._id)) {
                  descendants.add(k._id);
                  queue.push(k._id);
                }
              }
            }
            
            const docRems = all.filter(r => descendants.has(r._id) || r._id === rootId);
            const broken = docRems.filter(r => JSON.stringify(r.key || '').includes('se0t1PxtnIsLC14tQ'));
            
            return JSON.stringify(broken.map(b => ({
              id: b._id,
              parent: b.parent,
              key: b.key
            })), null, 2);
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\broken_14.json', msg.result.result.value);
    console.log('Saved broken_14.json');
    ws.close();
  }
};