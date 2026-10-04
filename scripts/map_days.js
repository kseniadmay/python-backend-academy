const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
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
            
            // Map days: 1 to 42
            const dayMap = {};
            for (const r of docRems) {
              const kStr = JSON.stringify(r.key || '');
              const m = kStr.match(/День\\s*0?(\\d+)/);
              if (m) {
                const dayNum = parseInt(m[1]);
                if (dayNum >= 1 && dayNum <= 42) {
                  // Only consider if it looks like a day header (not checklist reference)
                  if (!dayMap[dayNum] || (kStr.includes('###') || kStr.includes(' · '))) {
                    dayMap[dayNum] = { id: r._id, parent: r.parent, key: r.key, keyStr: kStr.slice(0, 80) };
                  }
                }
              }
            }
            
            // Weeks
            const weekMap = {};
            for (const r of docRems) {
              const kStr = JSON.stringify(r.key || '');
              const m = kStr.match(/Неделя\\s*(\\d+)/);
              if (m) {
                const wNum = parseInt(m[1]);
                if (wNum >= 1 && wNum <= 6 && !kStr.includes('REVIEW') && !kStr.includes('Чек-лист') && !kStr.includes('Оглавление')) {
                  weekMap[wNum] = { id: r._id, parent: r.parent, key: r.key, keyStr: kStr.slice(0, 80) };
                }
              }
            }
            
            return JSON.stringify({
              daysFound: Object.keys(dayMap).length,
              dayMap,
              weeksFound: Object.keys(weekMap).length,
              weekMap
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\days_map.json', msg.result.result.value);
    const res = JSON.parse(msg.result.result.value);
    console.log('Days found:', res.daysFound);
    console.log('Weeks found:', res.weeksFound);
    ws.close();
  }
};