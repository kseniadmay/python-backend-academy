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
    
    // Read parsed schedule
    const parsedSchedule = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));
    
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
            const schedule = ${JSON.stringify(parsedSchedule)};
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
            
            // 1. BUILD KNOWLEDGE BASE INDEX FOR ALL CARDS
            const candidateRems = all.filter(r => !descendants.has(r._id) && r._id !== rootId);
            const normIndex = new Map();
            for (const r of candidateRems) {
              const raw = extractText(r.key);
              if (raw && raw.length > 2) {
                const norm = normalize(raw);
                if (!normIndex.has(norm)) normIndex.set(norm, r._id);
              }
            }
            // Explicit card mappings for tricky names
            const explicitMap = {
              'ssh': 'ytDIt4nG8L0CY6xKp',
              'str и repr два представления одного объекта': '7Zhy22Jt7aKxXFz1o',
              'dict и slots как python хранит атрибуты объектов': 'JAXdkYxTTBSG9wxD4'
            };
            for (const [k, v] of Object.entries(explicitMap)) {
              normIndex.set(k, v);
            }
            
            // 2. RELINK ALL BROKEN LINKS & SET TODO
            let relinkedCount = 0;
            let relinkFailed = [];
            
            for (const r of docRems) {
              const kStr = JSON.stringify(r.key || '');
              if (kStr.includes('se0t1PxtnIsLC14tQ')) {
                // Extract clean target text
                let brokenText = '';
                let isTask = false;
                let levelPrefix = '';
                let tagSuffix = '';
                
                if (Array.isArray(r.key)) {
                  for (let i = 0; i < r.key.length; i++) {
                    const p = r.key[i];
                    if (p && p.qId === 'se0t1PxtnIsLC14tQ') {
                      brokenText += (p.text || '');
                    } else if (typeof p === 'string') {
                      if (p.includes('Уровень ')) {
                        isTask = true;
                        levelPrefix = p;
                      } else if (p.includes('#')) {
                        tagSuffix = p;
                      }
                    }
                  }
                }
                
                const normTarget = normalize(brokenText);
                let foundId = normIndex.get(normTarget);
                if (!foundId && normTarget.length > 8) {
                  for (const [normK, id] of normIndex.entries()) {
                    if (normK.includes(normTarget) || normTarget.includes(normK) || normK.slice(0, 25) === normTarget.slice(0, 25)) {
                      foundId = id;
                      break;
                    }
                  }
                }
                
                if (foundId) {
                  // Build clean key with valid RemNote link
                  let cleanTitle = brokenText.trim();
                  // Clean up title punctuation
                  cleanTitle = cleanTitle.replace(/^_*/, '').replace(/_*$/, '').trim();
                  
                  let newKey;
                  if (isTask) {
                    newKey = [
                      levelPrefix,
                      {
                        i: 'q',
                        _id: foundId,
                        text: cleanTitle,
                        textOfDeletedRem: [cleanTitle]
                      },
                      tagSuffix
                    ].filter(Boolean);
                  } else {
                    newKey = [
                      {
                        i: 'q',
                        _id: foundId,
                        text: cleanTitle,
                        textOfDeletedRem: [cleanTitle]
                      }
                    ];
                  }
                  
                  await rc.update(r._id, {
                    $set: {
                      key: newKey,
                      apu: { t: { v: true, ',u': Date.now() } },
                      ps: { t_s: { v: { v: ['Unfinished'], s: 'Unfinished' }, ',u': Date.now() } }
                    }
                  });
                  relinkedCount++;
                } else {
                  relinkFailed.push({ id: r._id, brokenText, normTarget });
                }
              }
            }
            
            // 3. IDENTIFY WEEKS AND DAYS
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
            
            // 4. REPARENT WEEKS UNDER ROOT
            for (let w = 1; w <= 6; w++) {
              const wId = weekMap[w];
              if (wId) {
                await rc.update(wId, {
                  $set: {
                    parent: rootId,
                    f: 'a' + w
                  }
                });
              }
            }
            
            // 5. REPARENT DAYS UNDER WEEKS
            // Week 1: 1-7, Week 2: 8-14, Week 3: 15-21, Week 4: 22-28, Week 5: 29-35, Week 6: 36-42
            for (let d = 1; d <= 42; d++) {
              const dId = dayMap[d];
              const wNum = Math.ceil(d / 7);
              const wId = weekMap[wNum];
              const dayIndexInWeek = ((d - 1) % 7) + 1;
              if (dId && wId) {
                await rc.update(dId, {
                  $set: {
                    parent: wId,
                    f: 'a' + dayIndexInWeek
                  }
                });
              }
            }
            
            // 6. BUILD ITEM -> DAY MAPPING FROM SCHEDULE
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
            
            // 7. FIND AND REPARENT ALL CODING AND THEORY SECTIONS TO THEIR DAYS
            const taskParents = new Set();
            const theoryParents = new Set();
            for (const r of all) {
              const s = JSON.stringify(r.key || '');
              if (s.includes('Уровень ')) {
                taskParents.add(r.parent);
              } else if (s.includes('qId') || (r.apu && r.apu.t)) {
                if (!s.includes('Уровень ') && !s.includes('День ') && !s.includes('Неделя ')) {
                  theoryParents.add(r.parent);
                }
              }
            }
            
            let reparentedSections = 0;
            // Reparent task sections
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
                  $set: {
                    parent: dayMap[bestDay],
                    f: 'a2' // 2nd child in day
                  }
                });
                reparentedSections++;
              }
            }
            
            // Reparent theory sections
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
                  $set: {
                    parent: dayMap[bestDay],
                    f: 'a1' // 1st child in day
                  }
                });
                reparentedSections++;
              }
            }
            
            // 8. REPARENT STANDOUTS AND CHECKLISTS FOR REVIEW DAYS (7, 14, 21, 28, 35, 42)
            const reviewDays = [7, 14, 21, 28, 35, 42];
            for (const r of all) {
              const txt = extractText(r.key);
              if (txt.includes('Стенд-аут') || txt.includes('Чек-лист готовности') || txt.includes('Итоговый чек-лист')) {
                // Find which week / day it belongs to
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
                    $set: {
                      parent: dayMap[targetDay],
                      f: fIndex
                    }
                  });
                  reparentedSections++;
                }
              }
            }
            
            // 9. CLEAN UP EMPTY / ORPHAN REMS ON ROOT
            const currentRootChildren = all.filter(r => r.parent === rootId);
            let cleanedOrphans = 0;
            const validRootIds = new Set([
              ...Object.values(weekMap),
              '5EhHktCkqZL4GB6wE' // Intro subtitle
            ]);
            
            for (const r of currentRootChildren) {
              const kStr = JSON.stringify(r.key || '');
              const txt = extractText(r.key);
              if (txt.includes('Как читать это расписание') || txt.includes('Оглавление')) {
                validRootIds.add(r._id);
                continue;
              }
              if (!validRootIds.has(r._id)) {
                // If it has no children or empty, unlink or remove
                const kids = childrenMap[r._id] || [];
                if (kids.length === 0 || txt.trim() === '' || txt.startsWith('**')) {
                  await rc.remove(r._id);
                  cleanedOrphans++;
                }
              }
            }
            
            // 10. REFRESH AND COUNT
            const freshAll = await ds.fetchAllImpl();
            const finalRootKids = freshAll.filter(r => r.parent === rootId);
            
            return JSON.stringify({
              success: true,
              relinkedCount,
              relinkFailedCount: relinkFailed.length,
              relinkFailed,
              reparentedSections,
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
      console.error('Execution error:', JSON.stringify(msg, null, 2));
    } else {
      console.log('FINAL RESULT:');
      console.log(msg.result.result.value);
      fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\final_result.json', msg.result.result.value);
    }
    ws.close();
  }
};