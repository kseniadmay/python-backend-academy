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
    const schedule = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\parsed_schedule.json', 'utf8'));
    
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(async () => {
          const schedule = ${JSON.stringify(schedule)};
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
          
          function norm(s) {
            return (s || '').toLowerCase().replace(/[^a-zа-яё0-9]/gi, ' ').replace(/\\s+/g, ' ').trim();
          }
          
          // Build day-to-items map
          const dayItems = {};
          for (let d = 1; d <= 42; d++) {
            dayItems[d] = { theory: [], coding: [], checklist: [] };
          }
          for (const w of schedule.weeks) {
            for (const d of w.days) {
              for (const s of d.sections) {
                for (const item of s.items) {
                  const clean = item.replace(/^-\\s*(\\[\\s*\\]\\s*)?/, '').trim();
                  const n = norm(clean);
                  if (s.type === 'theory') dayItems[d.num].theory.push(n);
                  else if (s.type === 'coding') dayItems[d.num].coding.push(n);
                  else if (s.type === 'checklist') dayItems[d.num].checklist.push(n);
                }
              }
            }
          }
          
          // Build parent -> children map
          const childrenMap = {};
          for (const r of all) {
            if (r.parent) {
              if (!childrenMap[r.parent]) childrenMap[r.parent] = [];
              childrenMap[r.parent].push(r);
            }
          }
          
          // For every parent rem, see what its children are and calculate match score with each day's theory/coding/checklist
          const parentScores = [];
          for (const [pId, kids] of Object.entries(childrenMap)) {
            const pRem = all.find(r => r._id === pId);
            if (!pRem) continue;
            const pText = extractText(pRem.key);
            
            // kid texts
            const kidTexts = kids.map(k => norm(extractText(k.key)));
            
            const scores = [];
            for (let d = 1; d <= 42; d++) {
              let tMatches = 0;
              for (const kt of kidTexts) {
                if (kt.length > 5 && dayItems[d].theory.some(it => it.includes(kt.slice(0, 20)) || kt.includes(it.slice(0, 20)))) {
                  tMatches++;
                }
              }
              let cMatches = 0;
              for (const kt of kidTexts) {
                if (kt.length > 5 && dayItems[d].coding.some(it => it.includes(kt.slice(0, 20)) || kt.includes(it.slice(0, 20)))) {
                  cMatches++;
                }
              }
              let chMatches = 0;
              for (const kt of kidTexts) {
                if (kt.length > 5 && dayItems[d].checklist.some(it => it.includes(kt.slice(0, 20)) || kt.includes(it.slice(0, 20)))) {
                  chMatches++;
                }
              }
              if (tMatches > 0) scores.push({ day: d, type: 'theory', score: tMatches, totalKids: kids.length, dayItemsCount: dayItems[d].theory.length });
              if (cMatches > 0) scores.push({ day: d, type: 'coding', score: cMatches, totalKids: kids.length, dayItemsCount: dayItems[d].coding.length });
              if (chMatches > 0) scores.push({ day: d, type: 'checklist', score: chMatches, totalKids: kids.length, dayItemsCount: dayItems[d].checklist.length });
            }
            if (scores.length > 0) {
              parentScores.push({
                parentId: pId,
                parentText: pText.slice(0, 70),
                parentCurrentParent: pRem.parent,
                kidsCount: kids.length,
                scores
              });
            }
          }
          
          return {
            totalCandidateParents: parentScores.length,
            parentScores
          };
        })()`,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    fs.writeFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\match_scores.json', JSON.stringify(msg.result.result.value, null, 2), 'utf8');
    console.log('Saved match_scores.json');
    ws.close();
  }
};
