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
            
            // Weeks
            const weeks = [
              { num: 1, id: 'i2G5Z1gxlEaEf4Sz3' },
              { num: 2, id: 'YvCOnToaalzIwm2MY' },
              { num: 3, id: 'gFKS7LUxkNdmTlwmy' },
              { num: 4, id: 'ms4eHbXFhOQLYTFmN' },
              { num: 5, id: 'xGQiIy44gskxNmv3u' },
              { num: 6, id: 'ucZRFaKMYsiOa6VKW' }
            ];
            
            const weeksSummary = weeks.map(w => {
              const kids = all.filter(r => r.parent === w.id);
              kids.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
              return {
                week: w.num,
                id: w.id,
                daysCount: kids.length,
                days: kids.map(k => ({ id: k._id, f: k.f, text: extractText(k.key).slice(0, 60) }))
              };
            });
            
            // Also find where Review days (07, 14, 21, 28, 35, 42) are
            const reviewDays = [7, 14, 21, 28, 35, 42].map(d => {
              const found = all.filter(r => extractText(r.key).includes('День ' + (d < 10 ? '0' + d : d)) || extractText(r.key).includes('День ' + d));
              return {
                day: d,
                matches: found.map(f => ({ id: f._id, parent: f.parent, text: extractText(f.key).slice(0, 60) }))
              };
            });
            
            return JSON.stringify({ weeksSummary, reviewDays }, null, 2);
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\weeks_summary.json', msg.result.result.value);
    console.log('Saved weeks summary.');
    ws.close();
  }
};