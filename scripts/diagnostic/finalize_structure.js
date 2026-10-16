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
            if (!rem) return JSON.stringify({ error: 'rem not found' });
            
            const tg = rem.getTinyGraph();
            const rc = tg.getRemCollection();
            const ds = rc.DatabaseStore;
            
            // 1. Attach 5 review days to their respective weeks
            const reviewLinks = [
              { dayId: 'Zr08REWGATxtsCUoY', weekId: 'i2G5Z1gxlEaEf4Sz3', f: 'a7' }, // Day 07 -> Week 1
              { dayId: 't4tkDifkEZGZhSV7X', weekId: 'YvCOnToaalzIwm2MY', f: 'a7' }, // Day 14 -> Week 2
              { dayId: 'c2mpprEZRTzKRJwWn', weekId: 'gFKS7LUxkNdmTlwmy', f: 'a7' }, // Day 21 -> Week 3
              { dayId: '9CSqUag62ySNRpVbK', weekId: 'ms4eHbXFhOQLYTFmN', f: 'a7' }, // Day 28 -> Week 4
              { dayId: 'Sa2NV96RJQCer4jVy', weekId: 'xGQiIy44gskxNmv3u', f: 'a7' }  // Day 35 -> Week 5
            ];
            for (const r of reviewLinks) {
              await rc.update(r.dayId, { $set: { parent: r.weekId, f: r.f } });
            }
            
            // 2. Clean up duplicates on root:
            // Keep exactly 1 "Как читать" and 1 "Оглавление"
            const keepRootIds = new Set([
              '5EhHktCkqZL4GB6wE', // Subtitle (f: a0)
              '3wGp1954eti6HY9Ej', // Как читать это расписание (f: a1)
              'sKMQGofj7WYX3gsrt', // 🗂️ Оглавление (f: a2)
              'i2G5Z1gxlEaEf4Sz3', // Week 1 (f: a3)
              'YvCOnToaalzIwm2MY', // Week 2 (f: a4)
              'gFKS7LUxkNdmTlwmy', // Week 3 (f: a5)
              'ms4eHbXFhOQLYTFmN', // Week 4 (f: a6)
              'xGQiIy44gskxNmv3u', // Week 5 (f: a7)
              'ucZRFaKMYsiOa6VKW'  // Week 6 (f: a8)
            ]);
            
            await rc.update('5EhHktCkqZL4GB6wE', { $set: { parent: rootId, f: 'a0' } });
            await rc.update('3wGp1954eti6HY9Ej', { $set: { parent: rootId, f: 'a1' } });
            await rc.update('sKMQGofj7WYX3gsrt', { $set: { parent: rootId, f: 'a2' } });
            
            const all = await ds.fetchAllImpl();
            let unlinkedDuplicates = 0;
            for (const r of all) {
              if (r.parent === rootId && !keepRootIds.has(r._id)) {
                await rc.update(r._id, { $set: { parent: null } });
                unlinkedDuplicates++;
              }
            }
            
            // 3. Verify final structure
            const freshAll = await ds.fetchAllImpl();
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
            
            const finalRoot = freshAll.filter(r => r.parent === rootId);
            finalRoot.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
            
            const weekStats = [
              { num: 1, id: 'i2G5Z1gxlEaEf4Sz3' },
              { num: 2, id: 'YvCOnToaalzIwm2MY' },
              { num: 3, id: 'gFKS7LUxkNdmTlwmy' },
              { num: 4, id: 'ms4eHbXFhOQLYTFmN' },
              { num: 5, id: 'xGQiIy44gskxNmv3u' },
              { num: 6, id: 'ucZRFaKMYsiOa6VKW' }
            ].map(w => {
              const kids = freshAll.filter(r => r.parent === w.id);
              kids.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
              return {
                week: w.num,
                count: kids.length,
                days: kids.map(k => extractText(k.key).slice(0, 30))
              };
            });
            
            return JSON.stringify({
              success: true,
              unlinkedDuplicates,
              finalRootCount: finalRoot.length,
              finalRoot: finalRoot.map(k => ({ id: k._id, f: k.f, text: extractText(k.key) })),
              weekStats
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
    console.log('FINAL STRUCTURE RESULT:');
    console.log(msg.result.result.value);
    ws.close();
  }
};