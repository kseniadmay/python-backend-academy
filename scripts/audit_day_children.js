const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
if (!fs.existsSync(devToolsPortFile)) {
  console.log('[SKIP] Chrome DevToolsActivePort not found. Live browser audit skipped.');
  process.exit(0);
}
setTimeout(() => {
  console.log('[SKIP] Live Chrome audit timed out.');
  process.exit(0);
}, 3000);
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.attachToTarget',
    params: { targetId: '51B0D7B7180A1C1995B5B01ED2D6E6F9', flatten: true }
  }));
};

let sessionId = null;

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.error || !msg.result) {
    console.log('[SKIP] Chrome DevTools target unavailable. Scratch test skipped.');
    process.exit(0);
  }
  if (msg.id === 1) {
    sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
            const firstRem = document.querySelector('[data-rem-id]');
            const fiberKey = Object.keys(firstRem || {}).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
            let curr = firstRem ? firstRem[fiberKey] : null;
            let rem = null;
            while (curr) {
              if (curr.memoizedProps && curr.memoizedProps.rem) {
                rem = curr.memoizedProps.rem;
                break;
              }
              curr = curr.return;
            }
            const tg = rem.getTinyGraph();
            const rc = tg.getRemCollection();
            const ds = rc.DatabaseStore;
            const all = await ds.fetchAllImpl();
            
            const rootId = 'GwREY4bq5eQvPyeAB';
            
            // Build parent -> children map
            const childrenMap = {};
            for (const r of all) {
              if (r.parent) {
                if (!childrenMap[r.parent]) childrenMap[r.parent] = [];
                childrenMap[r.parent].push(r);
              }
            }
            
            // Map days
            const dayMap = {};
            for (const r of all) {
              const kStr = JSON.stringify(r.key || '');
              const m = kStr.match(/День\\s*0?(\\d+)/);
              if (m) {
                const dayNum = parseInt(m[1]);
                if (dayNum >= 1 && dayNum <= 42) {
                  if (!dayMap[dayNum] || (kStr.includes('###') || kStr.includes(' · '))) {
                    dayMap[dayNum] = r._id;
                  }
                }
              }
            }
            
            const audit = {};
            for (let i = 1; i <= 42; i++) {
              const dId = dayMap[i];
              if (!dId) {
                audit[i] = { found: false };
                continue;
              }
              const kids = childrenMap[dId] || [];
              audit[i] = {
                found: true,
                id: dId,
                kidsCount: kids.length,
                kids: kids.map(k => ({
                  id: k._id,
                  keyStr: JSON.stringify(k.key || '').slice(0, 60),
                  subKidsCount: (childrenMap[k._id] || []).length
                }))
              };
            }
            
            return JSON.stringify(audit, null, 2);
          } catch (e) {
            return JSON.stringify({ error: e.message, stack: e.stack });
          }
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }

  if (msg.id === 2) {
    if (msg.error || (msg.result && msg.result.exceptionDetails)) {
      console.error('Eval error:', JSON.stringify(msg));
    } else {
      fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\day_children_audit.json', msg.result.result.value);
      console.log('Saved day children audit.');
    }
    ws.close();
  }
};