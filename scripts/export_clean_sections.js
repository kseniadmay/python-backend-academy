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
            
            // Build tree descendants of GwREY4bq5eQvPyeAB ONLY
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
            const docRems = all.filter(r => descendants.has(r._id));
            
            // In docRems, find tasks
            const tasks = docRems.filter(r => extractText(r.key).includes('Уровень '));
            const theories = docRems.filter(r => {
              const s = JSON.stringify(r.key || '');
              return s.includes('se0t1PxtnIsLC14tQ') && !extractText(r.key).includes('Уровень ');
            });
            
            // Parents of tasks in docRems
            const taskParents = {};
            for (const t of tasks) {
              if (!taskParents[t.parent]) taskParents[t.parent] = [];
              taskParents[t.parent].push(t);
            }
            
            // Parents of theories in docRems
            const theoryParents = {};
            for (const th of theories) {
              if (!theoryParents[th.parent]) theoryParents[th.parent] = [];
              theoryParents[th.parent].push(th);
            }
            
            const taskSections = Object.keys(taskParents).map(pId => {
              const p = all.find(x => x._id === pId);
              return {
                id: pId,
                parent: p ? p.parent : null,
                text: p ? extractText(p.key) : null,
                count: taskParents[pId].length,
                kidsSample: taskParents[pId].map(k => extractText(k.key))
              };
            });
            
            const theorySections = Object.keys(theoryParents).map(pId => {
              const p = all.find(x => x._id === pId);
              return {
                id: pId,
                parent: p ? p.parent : null,
                text: p ? extractText(p.key) : null,
                count: theoryParents[pId].length,
                kidsSample: theoryParents[pId].map(k => extractText(k.key))
              };
            });
            
            return JSON.stringify({
              totalDocRems: docRems.length,
              tasksCount: tasks.length,
              theoriesCount: theories.length,
              taskSections,
              theorySections
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\doc_clean_sections.json', msg.result.result.value);
    console.log('Saved doc_clean_sections.json');
    ws.close();
  }
};