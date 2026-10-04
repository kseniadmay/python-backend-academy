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
            if (!rem) return JSON.stringify({ error: 'rem not found' });
            
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
            
            function normalize(str) {
              return (str || '')
                .toLowerCase()
                .replace(/[^a-zа-яё0-9]/gi, ' ')
                .replace(/\\s+/g, ' ')
                .trim();
            }
            
            const candidateRems = all.filter(r => !descendants.has(r._id) && r._id !== rootId);
            
            const normIndex = new Map();
            for (const r of candidateRems) {
              const raw = extractText(r.key);
              if (raw && raw.length > 3) {
                const norm = normalize(raw);
                if (!normIndex.has(norm)) normIndex.set(norm, r._id);
              }
            }
            
            let matched = 0;
            let unmatched = 0;
            const samplesUnmatched = [];
            
            for (const r of docRems) {
              const kStr = JSON.stringify(r.key || '');
              if (kStr.includes('se0t1PxtnIsLC14tQ')) {
                let brokenText = '';
                if (Array.isArray(r.key)) {
                  for (const p of r.key) {
                    if (p && p.qId === 'se0t1PxtnIsLC14tQ') {
                      brokenText = p.text;
                      break;
                    }
                  }
                }
                
                const normTarget = normalize(brokenText);
                let foundId = normIndex.get(normTarget);
                
                if (!foundId && normTarget.length > 10) {
                  for (const [normK, id] of normIndex.entries()) {
                    if (normK.includes(normTarget) || normTarget.includes(normK)) {
                      foundId = id;
                      break;
                    }
                  }
                }
                
                if (foundId) {
                  matched++;
                } else {
                  unmatched++;
                  if (samplesUnmatched.length < 10) {
                    samplesUnmatched.push({ remId: r._id, brokenText, normTarget });
                  }
                }
              }
            }
            
            return JSON.stringify({
              totalBroken: matched + unmatched,
              matched,
              unmatched,
              samplesUnmatched
            }, null, 2);
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
    console.log(msg.result.result.value);
    ws.close();
  }
};