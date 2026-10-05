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

ws.onopen = () => ws.send(JSON.stringify({ id: 1, method: 'Target.getTargets' }));

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.error || !msg.result) {
    console.log('[SKIP] Chrome DevTools target unavailable. Scratch test skipped.');
    process.exit(0);
  }
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
          const rootId = 'GwREY4bq5eQvPyeAB';
          
          function extractText(key) {
            if (!key) return '';
            if (typeof key === 'string') return key;
            if (Array.isArray(key)) {
              return key.map(part => typeof part === 'string' ? part : (part.text || (part.textOfDeletedRem ? part.textOfDeletedRem.join(' ') : ''))).join('');
            }
            return '';
          }
          
          // Map weeks
          const weeks = all.filter(r => r.parent === rootId && extractText(r.key).includes('Неделя')).sort((a,b)=>(a.f||'').localeCompare(b.f||''));
          
          const report = [];
          for (const w of weeks) {
            const days = all.filter(r => r.parent === w._id).sort((a,b)=>(a.f||'').localeCompare(b.f||''));
            report.push({
              weekId: w._id,
              weekText: extractText(w.key),
              days: days.map(d => {
                const kids = all.filter(r => r.parent === d._id).sort((a,b)=>(a.f||'').localeCompare(b.f||''));
                return {
                  dayId: d._id,
                  dayText: extractText(d.key),
                  kidsCount: kids.length,
                  kids: kids.map(k => {
                    const subSub = all.filter(r => r.parent === k._id);
                    return {
                      id: k._id,
                      f: k.f,
                      type: k.type,
                      text: extractText(k.key),
                      subSubCount: subSub.length,
                      sampleSubSub: subSub.slice(0, 3).map(s => extractText(s.key).slice(0, 40))
                    };
                  })
                };
              })
            });
          }
          return report;
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\all_days_audit.json', JSON.stringify(msg.result.result.value, null, 2), 'utf8');
    console.log('Saved all_days_audit.json');
    ws.close();
  }
};
