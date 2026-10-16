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
    const schedule = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));
    
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
            const schedule = ${JSON.stringify(schedule)};
            const rootId = 'GwREY4bq5eQvPyeAB';
            
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
            
            // 1. FIX 3 SPECIAL CARDS
            const explicitMap = {
              '1JwGqKipydOrnvO0U': {
                id: 'ytDIt4nG8L0CY6xKp',
                title: 'SSH'
              },
              'GSN9PNOgmPGAxAh2l': {
                id: '7Zhy22Jt7aKxXFz1o',
                title: '__str__ и __repr__: два представления одного объекта'
              },
              'tmgSokpZlUbzas89u': {
                id: 'JAXdkYxTTBSG9wxD4',
                title: '__dict__ и __slots__: как Python хранит атрибуты объектов'
              }
            };
            
            for (const [remId, target] of Object.entries(explicitMap)) {
              await rc.update(remId, {
                $set: {
                  key: [{
                    i: 'q',
                    _id: target.id,
                    text: target.title,
                    textOfDeletedRem: [target.title]
                  }],
                  apu: { t: { v: true, ',u': Date.now() } },
                  ps: { t_s: { v: { v: ['Unfinished'], s: 'Unfinished' }, ',u': Date.now() } }
                }
              });
            }
            
            // 2. IDENTIFY WEEKS AND DAYS
            const weekMap = {};
            const dayMap = {};
            for (const r of all) {
              const kStr = JSON.stringify(r.key || '');
              const wm = kStr.match(/Неделя\\s*(\\d+)/);
              if (wm) {
                const wNum = parseInt(wm[1]);
                if (wNum >= 1 && wNum <= 6 && !kStr.includes('REVIEW') && !kStr.includes('Чек-лист') && !kStr.includes('Оглавление')) {
                  weekMap[wNum] = r._id;
                }
              }
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
            
            // 3. REPARENT WEEKS UNDER ROOT
            for (let w = 1; w <= 6; w++) {
              const wId = weekMap[w];
              if (wId) {
                await rc.update(wId, {
                  $set: { parent: rootId, f: 'a' + w }
                });
              }
            }
            
            // 4. REPARENT DAYS UNDER WEEKS
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
            
            // 5. MAP ITEM TO DAY FROM SCHEDULE
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
            
            // Children map
            const childrenMap = {};
            for (const r of all) {
              if (r.parent) {
                if (!childrenMap[r.parent]) childrenMap[r.parent] = [];
                childrenMap[r.parent].push(r);
              }
            }
            
            // 6. REPARENT SECTIONS (CODING & THEORY)
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
            
            let reparentedTaskSec = 0;
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
                reparentedTaskSec++;
              }
            }
            
            let reparentedTheorySec = 0;
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
                reparentedTheorySec++;
              }
            }
            
            // 7. REPARENT STANDOUTS AND CHECKLISTS FOR REVIEW DAYS
            let reparentedReview = 0;
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
                  reparentedReview++;
                }
              }
            }
            
            // 8. REMOVE BROKEN/MERGED ORPHAN REMS ON ROOT
            const validRootIds = new Set([
              ...Object.values(weekMap),
              '5EhHktCkqZL4GB6wE' // Subtitle
            ]);
            
            const currentRootChildren = all.filter(r => r.parent === rootId);
            let cleanedOrphans = 0;
            for (const r of currentRootChildren) {
              const txt = extractText(r.key);
              if (txt.includes('Как читать это расписание') || txt.includes('Оглавление')) {
                validRootIds.add(r._id);
                continue;
              }
              if (!validRootIds.has(r._id)) {
                // Remove corrupted glued import rems or empty placeholders
                await rc.remove(r._id);
                cleanedOrphans++;
              }
            }
            
            // 9. VERIFY RESULT
            const freshAll = await ds.fetchAllImpl();
            const finalRootKids = freshAll.filter(r => r.parent === rootId);
            
            return JSON.stringify({
              success: true,
              reparentedTaskSec,
              reparentedTheorySec,
              reparentedReview,
              cleanedOrphans,
              finalRootKidsCount: finalRootKids.length,
              finalRootKids: finalRootKids.map(k => extractText(k.key))
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
    if (msg.error || (msg.result && msg.result.exceptionDetails)) {
      console.error('Error:', JSON.stringify(msg, null, 2));
    } else {
      console.log('RESTRUCTURING RESULT:');
      console.log(msg.result.result.value);
    }
    ws.close();
  }
};