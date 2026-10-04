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
            
            // 1. Detach the 14 corrupted glued import rems
            const corruptedIds = [
              '8zQL5XB4676y6fFkQ', 'AF7cK0oKUkcbdDR5Z', 'GbaXHnwGsSSc2ZNhQ',
              'P1PVOjSloZJxhvlGT', 'VqTvY7SEXIPuLq6jD', 'XkqPzVE1KSqOgUCqk',
              'bGSpu4v0wYxkrJzXH', 'bKQUp0bNb8cGiR7dr', 'cdDFn7vCzjjSdTUn7',
              'h4gyfkTXuDoRuL503', 'iOM2kA22fOUYiN0Bm', 'inJ2SPNZl3VEZGgeO',
              'uEvfGT9GT5Un6y8Pn', 'wpggjSqLo5WSORb5Q'
            ];
            for (const cId of corruptedIds) {
              await rc.update(cId, { $set: { parent: null } });
            }
            
            // 2. Check and fix dead links in doc:
            const deadRemIds = ['29OHO6hclobDVj4f0', '9uebMwvep4LcHm9kj', 'GSN9PNOgmPGAxAh2l', 'a2Nyn4unhUd6hesEi', 'h9jKHTzSoaJrtP393', 'n4HrzpGvWjJoy1Du0'];
            const allMap = new Map(all.map(r => [r._id, r]));
            const fixedDead = [];
            
            for (const dId of deadRemIds) {
              const r = allMap.get(dId);
              if (!r) continue;
              const txt = extractText(r.key);
              const norm = normalize(txt);
              // Find matching rem in all
              let found = null;
              for (const candidate of all) {
                if (candidate._id === dId) continue;
                const cNorm = normalize(extractText(candidate.key));
                if (cNorm === norm || (norm.length > 8 && cNorm.includes(norm))) {
                  found = candidate;
                  break;
                }
              }
              if (found) {
                const clean = txt.replace(/^[🥚🐣🦊🐺🐯🐉👑]\s*Уровень\s*\d+\s*·\s*/, '').trim();
                const isTask = txt.includes('Уровень ');
                const levelMatch = txt.match(/^([🥚🐣🦊🐺🐯🐉👑]\s*Уровень\s*\d+\s*·\s*)/);
                const prefix = levelMatch ? levelMatch[1] : '';
                
                let newKey;
                if (isTask) {
                  newKey = [
                    prefix,
                    { i: 'q', _id: found._id, text: clean, textOfDeletedRem: [clean] },
                    ' #Разминка'
                  ];
                } else {
                  newKey = [
                    { i: 'q', _id: found._id, text: clean, textOfDeletedRem: [clean] }
                  ];
                }
                await rc.update(dId, { $set: { key: newKey } });
                fixedDead.push({ dId, targetId: found._id, text: clean });
              }
            }
            
            // 3. Re-verify tree descendants of GwREY4bq5eQvPyeAB
            const rootId = 'GwREY4bq5eQvPyeAB';
            const freshAll = await ds.fetchAllImpl();
            const descendants = new Set();
            const queue = [rootId];
            const childrenMap = {};
            for (const r of freshAll) {
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
            
            const docRems = freshAll.filter(r => descendants.has(r._id) || r._id === rootId);
            const remainingBrokenInDoc = docRems.filter(r => JSON.stringify(r.key || '').includes('se0t1PxtnIsLC14tQ'));
            
            return JSON.stringify({
              detachedCorruptedCount: corruptedIds.length,
              fixedDead,
              remainingBrokenInDocCount: remainingBrokenInDoc.length,
              totalDocRems: docRems.length
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
  if (msg.id === 3) {
    console.log('CLEANUP & FIX RESULT:');
    console.log(msg.result.result.value);
    ws.close();
  }
};