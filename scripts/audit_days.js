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
            
            // Build tree descendants of GwREY4bq5eQvPyeAB
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
            
            function extractText(key) {
              if (!key) return '';
              if (typeof key === 'string') return key;
              if (Array.isArray(key)) {
                return key.map(part => {
                  if (typeof part === 'string') return part;
                  if (part && typeof part === 'object') {
                    return part.text || (part.textOfDeletedRem ? part.textOfDeletedRem.join(' ') : '');
                  }
                  return '';
                }).join('');
              }
              return '';
            }
            
            // Find all days: 1 to 42
            const daysFound = {};
            for (const r of docRems) {
              const txt = extractText(r.key);
              const m = txt.match(/День\s*0?(\d+)/i);
              if (m) {
                const dayNum = parseInt(m[1]);
                if (dayNum >= 1 && dayNum <= 42) {
                  // check if it's the title of the day
                  if (!daysFound[dayNum]) daysFound[dayNum] = [];
                  daysFound[dayNum].push({ id: r._id, parent: r.parent, text: txt });
                }
              }
            }
            
            return JSON.stringify({
              daysFoundSummary: Object.keys(daysFound).map(k => ({ day: k, count: daysFound[k].length, items: daysFound[k] })),
              totalFoundDaysCount: Object.keys(daysFound).length
            }, null, 2);
          } catch (e) {
            return JSON.stringify({ error: e.message });
          }
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }

  if (msg.id === 2) {
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\days_audit.json', msg.result.result.value);
    console.log('Saved days audit. Total days found:');
    const parsed = JSON.parse(msg.result.result.value);
    console.log(parsed.totalFoundDaysCount);
    ws.close();
  }
};