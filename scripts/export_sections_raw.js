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
            
            // Build parent -> children map
            const childrenMap = {};
            for (const r of all) {
              if (r.parent) {
                if (!childrenMap[r.parent]) childrenMap[r.parent] = [];
                childrenMap[r.parent].push(r);
              }
            }
            
            // Days Map
            const dayMap = {};
            for (const r of all) {
              const kStr = JSON.stringify(r.key || '');
              const m = kStr.match(/День\\s*0?(\\d+)/);
              if (m) {
                const dayNum = parseInt(m[1]);
                if (dayNum >= 1 && dayNum <= 42) {
                  if (!dayMap[dayNum] || (kStr.includes('###') || kStr.includes(' · '))) {
                    dayMap[dayNum] = r._id;
                  }
                }
              }
            }
            
            // Build list of all tasks and theories with their day from text
            // In RemNote, each day has some text or we can map each task by its text
            const taskParents = new Set();
            const theoryParents = new Set();
            for (const r of all) {
              const s = JSON.stringify(r.key || '');
              if (s.includes('Уровень ')) {
                taskParents.add(r.parent);
              } else if (s.includes('se0t1PxtnIsLC14tQ')) {
                theoryParents.add(r.parent);
              }
            }
            
            const taskSections = Array.from(taskParents).map(id => {
              const kids = childrenMap[id] || [];
              return {
                id,
                text: extractText(all.find(x => x._id === id)?.key),
                kidsCount: kids.length,
                kidsText: kids.map(k => extractText(k.key))
              };
            });
            
            const theorySections = Array.from(theoryParents).map(id => {
              const kids = childrenMap[id] || [];
              return {
                id,
                text: extractText(all.find(x => x._id === id)?.key),
                kidsCount: kids.length,
                kidsText: kids.map(k => extractText(k.key))
              };
            });
            
            return JSON.stringify({
              dayMap,
              taskSections,
              theorySections
            });
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\sections_raw.json', msg.result.result.value);
    console.log('Saved sections_raw.json');
    ws.close();
  }
};