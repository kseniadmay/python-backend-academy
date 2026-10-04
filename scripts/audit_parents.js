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
            
            // Build tree descendants of GwREY4bq5eQvPyeAB
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
            
            // Group tasks by their immediate parent
            const tasksByParent = {};
            for (const r of docRems) {
              if (JSON.stringify(r.key || '').includes('Уровень ')) {
                if (!tasksByParent[r.parent]) tasksByParent[r.parent] = [];
                tasksByParent[r.parent].push(r);
              }
            }
            
            // Group theories by their immediate parent
            const theoriesByParent = {};
            for (const r of docRems) {
              const s = JSON.stringify(r.key || '');
              if (s.includes('se0t1PxtnIsLC14tQ') && !s.includes('Уровень ')) {
                if (!theoriesByParent[r.parent]) theoriesByParent[r.parent] = [];
                theoriesByParent[r.parent].push(r);
              }
            }
            
            const parentsInfo = {};
            for (const pId of Object.keys(tasksByParent)) {
              const p = all.find(x => x._id === pId);
              parentsInfo[pId] = {
                id: pId,
                text: p ? extractText(p.key) : 'NOT FOUND',
                parentOfParent: p ? p.parent : 'NONE',
                tasksCount: tasksByParent[pId].length
              };
            }
            
            const theoryParentsInfo = {};
            for (const pId of Object.keys(theoriesByParent)) {
              const p = all.find(x => x._id === pId);
              theoryParentsInfo[pId] = {
                id: pId,
                text: p ? extractText(p.key) : 'NOT FOUND',
                parentOfParent: p ? p.parent : 'NONE',
                theoriesCount: theoriesByParent[pId].length
              };
            }
            
            return JSON.stringify({
              tasksParentCount: Object.keys(tasksByParent).length,
              theoryParentCount: Object.keys(theoriesByParent).length,
              taskParents: parentsInfo,
              theoryParents: theoryParentsInfo
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parents_audit.json', msg.result.result.value);
    console.log('Saved parents audit.');
    ws.close();
  }
};