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
    if (!target) {
      console.error('Target not found');
      ws.close();
      return;
    }
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
            
            // Build tree descendants of rootId
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
            
            // 1. Root audit
            const rootDirectKids = all.filter(r => r.parent === rootId);
            rootDirectKids.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
            
            // 2. Weeks audit
            const weekRems = rootDirectKids.filter(r => extractText(r.key).startsWith('Неделя '));
            const weeksDetail = weekRems.map((w, idx) => {
              const days = all.filter(r => r.parent === w._id);
              days.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
              return {
                weekIndex: idx + 1,
                id: w._id,
                title: extractText(w.key),
                daysCount: days.length,
                days: days.map(d => {
                  const dKids = all.filter(r => r.parent === d._id);
                  dKids.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
                  return {
                    id: d._id,
                    title: extractText(d.key),
                    sectionsCount: dKids.length,
                    sections: dKids.map(s => {
                      const sKids = all.filter(r => r.parent === s._id);
                      return {
                        id: s._id,
                        title: extractText(s.key).slice(0, 40),
                        itemsCount: sKids.length
                      };
                    })
                  };
                })
              };
            });
            
            // 3. Task & Theory counts in document
            const tasksInDoc = docRems.filter(r => extractText(r.key).includes('Уровень '));
            const tasksWithTodo = tasksInDoc.filter(r => r.apu && r.apu.t && r.apu.t.v);
            
            // Broken links audit in document
            const brokenInDoc = docRems.filter(r => JSON.stringify(r.key || '').includes('se0t1PxtnIsLC14tQ'));
            
            // Valid links check: check if _id in "q" exists in all
            const allIds = new Set(all.map(r => r._id));
            let validLinks = 0;
            let deadLinks = 0;
            const deadLinkSamples = [];
            
            for (const r of docRems) {
              if (Array.isArray(r.key)) {
                for (const p of r.key) {
                  if (p && p.i === 'q' && p._id) {
                    if (allIds.has(p._id)) {
                      validLinks++;
                    } else {
                      deadLinks++;
                      deadLinkSamples.push({ remId: r._id, targetId: p._id, text: p.text });
                    }
                  }
                }
              }
            }
            
            // 4. Animal emojis audit
            const invalidEmojis = [];
            const animalRegex = /^(🥚|🐣|🦊|🐺|🐯|🐉|👑)\s*Уровень\s*[1-7]/;
            for (const t of tasksInDoc) {
              const txt = extractText(t.key).trim();
              if (!animalRegex.test(txt)) {
                invalidEmojis.push({ id: t._id, text: txt.slice(0, 50) });
              }
            }
            
            // 5. Review days audit (7, 14, 21, 28, 35, 42)
            const reviewDayNums = [7, 14, 21, 28, 35, 42];
            const reviewAudit = [];
            for (const wd of weeksDetail) {
              for (const d of wd.days) {
                const match = d.title.match(/День\s*0?(\d+)/);
                if (match && reviewDayNums.includes(parseInt(match[1]))) {
                  const dayNum = parseInt(match[1]);
                  const codingSec = d.sections.find(s => s.title.toLowerCase().includes('кодинг'));
                  const checklistSec = d.sections.find(s => s.title.toLowerCase().includes('чек-лист'));
                  reviewAudit.push({
                    dayNum,
                    title: d.title,
                    codingItems: codingSec ? codingSec.itemsCount : 0,
                    checklistItems: checklistSec ? checklistSec.itemsCount : 0
                  });
                }
              }
            }
            
            return JSON.stringify({
              rootChildrenCount: rootDirectKids.length,
              rootChildren: rootDirectKids.map(k => extractText(k.key)),
              weeksCount: weekRems.length,
              totalDaysInWeeks: weeksDetail.reduce((acc, w) => acc + w.daysCount, 0),
              weeksSummary: weeksDetail.map(w => ({ week: w.weekIndex, title: w.title, days: w.daysCount })),
              totalTasksInDoc: tasksInDoc.length,
              tasksWithTodoCount: tasksWithTodo.length,
              brokenLinksCount: brokenInDoc.length,
              validLinksCount: validLinks,
              deadLinksCount: deadLinks,
              deadLinkSamples,
              invalidEmojisCount: invalidEmojis.length,
              reviewAudit
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\independent_audit_report.json', msg.result.result.value);
    console.log('AUDIT REPORT SAVED.');
    ws.close();
  }
};