const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.getTargets'
  }));
};

let sessionId = null;

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
    sessionId = msg.result.sessionId;
    const schedule = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));
    
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
            const schedule = ${JSON.stringify(schedule)};
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
            
            // 1. Identify Week rems
            const weekMap = {};
            for (const r of all) {
              const kStr = JSON.stringify(r.key || '');
              const wm = kStr.match(/Неделя\\s*(\\d+)/);
              if (wm) {
                const wNum = parseInt(wm[1]);
                if (wNum >= 1 && wNum <= 6 && !kStr.includes('REVIEW') && !kStr.includes('Чек-лист') && !kStr.includes('Оглавление')) {
                  weekMap[wNum] = r._id;
                }
              }
            }
            
            // 2. Identify Day rems (1..42)
            const dayMap = {};
            for (const r of all) {
              const kStr = JSON.stringify(r.key || '');
              const dm = kStr.match(/День\\s*0?(\\d+)/);
              if (dm) {
                const dNum = parseInt(dm[1]);
                if (dNum >= 1 && dNum <= 42) {
                  if (!dayMap[dNum] || (kStr.includes('###') || kStr.includes(' · '))) {
                    dayMap[dNum] = r._id;
                  }
                }
              }
            }
            
            // 3. Reparent Weeks under root (f: a10..a60)
            for (let w = 1; w <= 6; w++) {
              const wId = weekMap[w];
              if (wId) {
                await rc.update(wId, {
                  $set: { parent: rootId, f: 'a' + (w + 2) }
                });
              }
            }
            
            // 4. Reparent Days under Weeks (7 days per week)
            for (let d = 1; d <= 42; d++) {
              const dId = dayMap[d];
              const wNum = Math.ceil(d / 7);
              const wId = weekMap[wNum];
              const dayIndexInWeek = ((d - 1) % 7) + 1;
              if (dId && wId) {
                await rc.update(dId, {
                  $set: { parent: wId, f: 'a' + dayIndexInWeek }
                });
              }
            }
            
            // 5. Item to day mapping from schedule
            const itemToDay = [];
            for (const w of schedule.weeks) {
              for (const d of w.days) {
                for (const s of d.sections) {
                  for (const it of s.items) {
                    const clean = it.replace(/^-\\s*(\\[\\s*\\]\\s*)?/, '').trim();
                    const norm = normalize(clean);
                    if (norm.length > 4) {
                      itemToDay.push({ norm, day: d.num, secType: s.type });
                    }
                  }
                }
              }
            }
            
            // 6. Reparent Task sections and Theory sections to their days
            const taskParents = new Set();
            const theoryParents = new Set();
            for (const r of all) {
              const s = JSON.stringify(r.key || '');
              if (s.includes('Уровень ')) {
                taskParents.add(r.parent);
              } else if (r.apu && r.apu.t && !s.includes('Уровень ') && !s.includes('День ') && !s.includes('Неделя ')) {
                theoryParents.add(r.parent);
              }
            }
            
            let reparentedTasks = 0;
            for (const secId of taskParents) {
              const kids = childrenMap[secId] || [];
              const votes = {};
              for (const k of kids) {
                const kNorm = normalize(extractText(k.key));
                for (const item of itemToDay) {
                  if (item.secType === 'coding' && (item.norm.includes(kNorm) || kNorm.includes(item.norm) || item.norm.slice(0, 25) === kNorm.slice(0, 25))) {
                    votes[item.day] = (votes[item.day] || 0) + 1;
                  }
                }
              }
              let bestDay = null;
              let maxVotes = 0;
              for (const [d, cnt] of Object.entries(votes)) {
                if (cnt > maxVotes) { maxVotes = cnt; bestDay = parseInt(d); }
              }
              if (bestDay && dayMap[bestDay]) {
                await rc.update(secId, {
                  $set: { parent: dayMap[bestDay], f: 'a2' }
                });
                reparentedTasks++;
              }
            }
            
            let reparentedTheories = 0;
            for (const secId of theoryParents) {
              const kids = childrenMap[secId] || [];
              const votes = {};
              for (const k of kids) {
                const kNorm = normalize(extractText(k.key));
                for (const item of itemToDay) {
                  if (item.secType === 'theory' && (item.norm.includes(kNorm) || kNorm.includes(item.norm) || item.norm.slice(0, 25) === kNorm.slice(0, 25))) {
                    votes[item.day] = (votes[item.day] || 0) + 1;
                  }
                }
              }
              let bestDay = null;
              let maxVotes = 0;
              for (const [d, cnt] of Object.entries(votes)) {
                if (cnt > maxVotes) { maxVotes = cnt; bestDay = parseInt(d); }
              }
              if (bestDay && dayMap[bestDay]) {
                await rc.update(secId, {
                  $set: { parent: dayMap[bestDay], f: 'a1' }
                });
                reparentedTheories++;
              }
            }
            
            // 7. Reparent Review Standouts & Checklists
            for (const r of all) {
              const txt = extractText(r.key);
              if (txt.includes('Стенд-аут') || txt.includes('Чек-лист готовности') || txt.includes('Итоговый чек-лист')) {
                let targetDay = null;
                if (txt.includes('Неделя 1')) targetDay = 7;
                else if (txt.includes('Неделя 2')) targetDay = 14;
                else if (txt.includes('Неделя 3')) targetDay = 21;
                else if (txt.includes('Неделя 4')) targetDay = 28;
                else if (txt.includes('Неделя 5')) targetDay = 35;
                else if (txt.includes('Неделя 6') || txt.includes('42 дней') || txt.includes('финал')) targetDay = 42;
                
                if (targetDay && dayMap[targetDay]) {
                  const fIndex = txt.includes('Стенд-аут') ? 'a3' : 'a4';
                  await rc.update(r._id, {
                    $set: { parent: dayMap[targetDay], f: fIndex }
                  });
                }
              }
            }
            
            // 8. Clean up root: detach all other rems from rootId (set parent to null)
            const validRootIds = new Set([
              ...Object.values(weekMap),
              '5EhHktCkqZL4GB6wE' // Subtitle
            ]);
            
            // Also keep intro rems: "Как читать" and "Оглавление"
            for (const r of all) {
              const txt = extractText(r.key);
              if (txt.includes('Как читать это расписание') || txt.includes('Оглавление')) {
                validRootIds.add(r._id);
                // set order before weeks
                await rc.update(r._id, { $set: { parent: rootId, f: 'a0' + (txt.includes('Как читать') ? '1' : '2') } });
              }
            }
            
            // Make sure "42 дня · Сентябрь – Октябрь 2026" is first
            await rc.update('5EhHktCkqZL4GB6wE', { $set: { parent: rootId, f: 'a00' } });
            
            // Unlink any other rem directly hanging under rootId
            let unlinkedFromRoot = 0;
            const freshAll = await ds.fetchAllImpl();
            for (const r of freshAll) {
              if (r.parent === rootId && !validRootIds.has(r._id)) {
                await rc.update(r._id, {
                  $set: { parent: null }
                });
                unlinkedFromRoot++;
              }
            }
            
            // 9. Inspect final root children
            const finalAll = await ds.fetchAllImpl();
            const finalRootKids = finalAll.filter(r => r.parent === rootId);
            
            // Sort by f
            finalRootKids.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
            
            // Inspect children of Week 1
            const w1Kids = finalAll.filter(r => r.parent === weekMap[1]);
            w1Kids.sort((a, b) => (a.f || '').localeCompare(b.f || ''));
            
            return JSON.stringify({
              success: true,
              reparentedTasks,
              reparentedTheories,
              unlinkedFromRoot,
              finalRootKidsCount: finalRootKids.length,
              finalRootKids: finalRootKids.map(k => ({ id: k._id, f: k.f, text: extractText(k.key) })),
              week1DaysCount: w1Kids.length,
              week1Days: w1Kids.map(k => ({ id: k._id, f: k.f, text: extractText(k.key) }))
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
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\final_hierarchy_result.json', msg.result.result.value);
    console.log('HIERARCHY RESULT:');
    console.log(msg.result.result.value);
    ws.close();
  }
};