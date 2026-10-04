const fs = require('fs');

const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');

const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.attachToTarget',
    params: {
      targetId: '51B0D7B7180A1C1995B5B01ED2D6E6F9',
      flatten: true
    }
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
            const firstRem = document.querySelector('[data-rem-id="5EhHktCkqZL4GB6wE"]');
            const fiberKey = Object.keys(firstRem || {}).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
            let curr = firstRem ? firstRem[fiberKey] : null;
            let targetProps = null;
            while (curr) {
              if (curr.memoizedProps && curr.memoizedProps.remId === '5EhHktCkqZL4GB6wE' && curr.memoizedProps.rem) {
                targetProps = curr.memoizedProps;
                break;
              }
              curr = curr.return;
            }
            if (!targetProps) return JSON.stringify({ error: 'not found' });
            
            const rem = targetProps.rem;
            // Inspect the prototype of rem to see how it loads other rems
            const proto = Object.getPrototypeOf(rem);
            const asyncFind = Object.getOwnPropertyNames(proto).filter(m => m.toLowerCase().includes('byid') || m.toLowerCase().includes('getrem') || m.toLowerCase().includes('findrem'));
            
            // Also let's inspect window.syncedUserDataCollection or window.RemTinygraphObject
            const hasSynced = !!window.SyncedUserDataCollection;
            const hasTiny = !!window.RemTinygraphObject;
            
            const tg = rem.getTinyGraph ? rem.getTinyGraph() : (rem.tg ? rem.tg() : null);
            const rc = tg ? tg.getRemCollection() : null;
            // How does tg search or how does rc find?
            const ds = rc.DatabaseStore;
            const all = await ds.fetchAllImpl();
            const d4Keywords = [
              "иерархию классов с одиночным наследованием",
              "LoggingMixin",
              "diamond problem",
              "родите",
              "super() в цепочке",
              "миксинами и разрешите конфликт",
              "init_subclass",
              "паттерн Mixin для сериализации"
            ];
            const d4Matches = {};
            for (const kw of d4Keywords) {
              const found = all.filter(r => JSON.stringify(r.key || '').includes(kw));
              d4Matches[kw] = found.map(f => ({ id: f._id, key: f.key, parent: f.parent }));
            }
            return JSON.stringify({ d4Matches });
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
    if (msg.error) {
      console.error('Evaluate error:', msg.error);
    } else {
      console.log('DOM & Page inspection:', msg.result.result.value);
    }
    ws.close();
  }
};
