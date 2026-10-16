const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => ws.send(JSON.stringify({ id: 1, method: 'Target.getTargets' }));

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    const target = msg.result.targetInfos.find(t => t.url && t.url.includes('GwREY4bq5eQvPyeAB'));
    if (!target) { console.error('Target not found'); ws.close(); return; }
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
          if (!rem) return { error: 'rem not found' };
          const tg = rem.getTinyGraph();
          const rc = tg.getRemCollection();
          const ds = rc.DatabaseStore;
          const all = await ds.fetchAllImpl();
          const rootId = 'GwREY4bq5eQvPyeAB';
          
          function getText(r) {
            if (!r || !r.key) return '';
            return r.key.map(k => typeof k === 'string' ? k : (k.text || k.name || k.textOfDeletedRem || '')).join('');
          }
          
          const rootKids = all.filter(r => r.parent === rootId).sort((a,b) => (a.f||'').localeCompare(b.f||''));
          
          return rootKids.map(k => {
            const subKids = all.filter(r => r.parent === k._id).sort((a,b) => (a.f||'').localeCompare(b.f||''));
            return {
              id: k._id,
              f: k.f,
              text: getText(k).slice(0, 60),
              subKidsCount: subKids.length,
              subKids: subKids.map(sk => {
                const subSub = all.filter(r => r.parent === sk._id).sort((a,b) => (a.f||'').localeCompare(b.f||''));
                return {
                  id: sk._id,
                  f: sk.f,
                  text: getText(sk).slice(0, 60),
                  subSubCount: subSub.length,
                  subSub: subSub.map(ssk => ({
                    id: ssk._id,
                    f: ssk.f,
                    text: getText(ssk).slice(0, 60),
                    childrenCount: all.filter(r => r.parent === ssk._id).length
                  }))
                };
              })
            };
          });
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\current_tree.json', JSON.stringify(msg.result.result.value, null, 2), 'utf8');
    console.log('Saved current tree structure');
    ws.close();
  }
};
