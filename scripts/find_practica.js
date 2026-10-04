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
          
          function extractText(key) {
            if (!key) return '';
            if (typeof key === 'string') return key;
            if (Array.isArray(key)) {
              return key.map(part => typeof part === 'string' ? part : (part.text || (part.textOfDeletedRem ? part.textOfDeletedRem.join(' ') : ''))).join('');
            }
            return '';
          }
          
          const matching = all.filter(r => {
            const t = extractText(r.key);
            return t === 'Практика' || t.startsWith('Практика') || t === 'Теория' || t === 'База знаний';
          });
          
          return matching.map(r => ({
            id: r._id,
            parent: r.parent,
            text: extractText(r.key),
            type: r.type,
            kidsCount: all.filter(k => k.parent === r._id).length
          }));
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    console.log(JSON.stringify(msg.result.result.value, null, 2));
    ws.close();
  }
};
