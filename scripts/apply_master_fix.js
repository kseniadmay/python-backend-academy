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
    const exactMap = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\exact_42_days_map.json', 'utf8'));
    
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          try {
            const exactMap = ${JSON.stringify(exactMap)};
            const rootId = 'GwREY4bq5eQvPyeAB';
            const theoryRootId = '0QFP2VCcxja5X9WWU';
            
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
            const all = await rc.DatabaseStore.fetchAllImpl();
            
            // Build whitelist of valid sections per day
            const dayIds = new Set(exactMap.map(m => m.dayId));
            const validChildIds = new Set();
            
            exactMap.forEach(m => {
              if (m.theoryId) validChildIds.add(m.theoryId);
              if (m.codingId) validChildIds.add(m.codingId);
              if (m.checklistId) validChildIds.add(m.checklistId);
              if (m.standoutId) validChildIds.add(m.standoutId);
            });
            
            let detachedCount = 0;
            let kbRestoredCount = 0;
            let reparentedCount = 0;
            
            // 1. Detach or restore all stray rems currently under any day
            for (const r of all) {
              if (dayIds.has(r.parent) && !validChildIds.has(r._id)) {
                if (r.type === 1) {
                  // KB Document -> restore under Theory folder
                  await rc.update(r._id, { $set: { parent: theoryRootId } });
                  kbRestoredCount++;
                } else if (r._id === 'CXxvzLVYN33te4fvq') {
                  // Practice database root -> restore to null
                  await rc.update(r._id, { $set: { parent: null } });
                  kbRestoredCount++;
                } else {
                  // Stray duplicate or composite rem -> detach
                  await rc.update(r._id, { $set: { parent: null } });
                  detachedCount++;
                }
              }
            }
            
            // 2. Reparent valid sections strictly to their target day with precise fractional index
            for (const m of exactMap) {
              if (m.theoryId) {
                await rc.update(m.theoryId, { $set: { parent: m.dayId, f: 'a1' } });
                reparentedCount++;
              }
              if (m.codingId) {
                await rc.update(m.codingId, { $set: { parent: m.dayId, f: 'a2' } });
                reparentedCount++;
              }
              if (m.standoutId) {
                await rc.update(m.standoutId, { $set: { parent: m.dayId, f: 'a3' } });
                reparentedCount++;
              }
              if (m.checklistId) {
                const fVal = m.standoutId ? 'a4' : 'a3';
                await rc.update(m.checklistId, { $set: { parent: m.dayId, f: fVal } });
                reparentedCount++;
              }
            }
            
            // 3. Verify counts after update
            const allAfter = await rc.DatabaseStore.fetchAllImpl();
            const dayVerification = exactMap.map(m => {
              const kids = allAfter.filter(r => r.parent === m.dayId);
              return {
                dayNum: m.dayNum,
                dayId: m.dayId,
                kidsCount: kids.length
              };
            });
            
            return JSON.stringify({
              success: true,
              kbRestoredCount,
              detachedCount,
              reparentedCount,
              dayVerification
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
  if (msg.id === 3) {
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\master_fix_result.json', JSON.stringify(msg.result.result.value, null, 2), 'utf8');
    console.log('Master fix executed! Result:');
    console.log(msg.result.result.value);
    ws.close();
  }
};
