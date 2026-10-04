const fs = require('fs');

const ast = JSON.parse(fs.readFileSync('local_file_ast.json', 'utf8'));
const exactMap = JSON.parse(fs.readFileSync('exact_42_days_map.json', 'utf8'));

// Topic map
const topicMap = {
  1: '31DthKFeDUSFy8kIf',
  2: '9KxSKro6nlcoZCCBl',
  3: '0IpA4W3iyh9beq2Lh',
  4: 'K7J5Um8xr3O9heMxv',
  8: 'AF7cK0oKUkcbdDR5Z',
  9: '1N3Socza2f94IRoE7',
  10: 'WTbFgiLCgSV8e2dnM',
  11: 'JDHEgCaLJVcaFr6is',
  12: 'phwIImGVeXttAUYbA',
  13: 'bKQUp0bNb8cGiR7dr',
  15: '0jnGYoC4LMlS3P7ON',
  16: '5rkqcmMAyUbN0Vke8',
  17: 'eTrJWkIVfPITVMoj3',
  18: 't1o58b5THG5vNSk9e',
  19: '5sEstc4mdKN7snoYP',
  20: 'VQXkbYN5T2BxFrduz',
  22: 'UXutSmCbGvgUzVro7',
  23: 'SxOTF6YHeTDvMCPs7',
  24: 'ItFWzl1GPSQTj5ZRj',
  25: 'pFqVPTMSofWEKJ2Oh',
  26: 'CeEHOA7zOu4eXEqj5',
  27: 'GbaXHnwGsSSc2ZNhQ',
  29: 'q7aXpevG2kiUKso1V',
  30: '1ROIV9i19u72vTJ53',
  31: 'Hw3wSc2uAA72QttKW',
  32: '22z7fvTiWF6fncggu',
  33: 'PpGxSbpK9Sx1hsGTU',
  34: 'IqO2rjYVySNwkPM59',
  36: 'cdDFn7vCzjjSdTUn7',
  37: '1JcnnCZd8qEAC0raX',
  38: 'An5a4v3ArfqIdEobr',
  39: '61qPBRQJFa1jZUl86',
  40: 'wfiThaYeDbVnPErjI',
  41: 'E8NC56N8tFfJL4FeN'
};

async function execute() {
  const payload = {
    ast,
    exactMap,
    topicMap
  };

  const code = `(async () => {
    try {
      const { ast, exactMap, topicMap } = ${JSON.stringify(payload)};
      
      const el = document.querySelector('[data-rem-id]');
      const fiberKey = Object.keys(el || {}).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
      let curr = el ? el[fiberKey] : null;
      let rem = null;
      while (curr) {
        if (curr.memoizedProps && curr.memoizedProps.rem && curr.memoizedProps.rem.getTinyGraph) {
          rem = curr.memoizedProps.rem;
          break;
        }
        curr = curr.return;
      }
      if (!rem) return { error: 'rem not found' };
      
      const tg = rem.getTinyGraph();
      const rc = tg.getRemCollection();
      const all = await rc.DatabaseStore.fetchAllImpl();
      const remById = new Map();
      all.forEach(r => remById.set(r._id, r));
      
      function extractText(key) {
        if (!key) return '';
        if (typeof key === 'string') return key;
        if (Array.isArray(key)) {
          return key.map(p => typeof p === 'string' ? p : (p.text || (p.textOfDeletedRem ? p.textOfDeletedRem.join(' ') : ''))).join('');
        }
        return '';
      }

      const now = Date.now();
      let operations = 0;

      // 1. Fix TOC styling (unset H2)
      const tocIds = ['Tjh5dy8ht48Box2te', 'EwBSIwFkVhKgGf0ia', 'PbOCjt2aRSZt6ZvwU', 'agUOhBd0lYhBQWDFp', 'NIgtLiD1MkLn2rMM5', '1nEwuP2BzBvf6d4y0', 'jRuK0K3l0m2WSaDEr'];
      for (let i = 0; i < tocIds.length; i++) {
        const tId = tocIds[i];
        await rc.update(tId, {
          $set: { parent: 'sKMQGofj7WYX3gsrt', f: 'a' + (i + 1) },
          $unset: { ps: true, psh: true, apu: true, aph: true }
        });
        operations++;
      }

      // 2. Rules under "Как читать это расписание"
      const ruleIds = ['sg4EKHSyf5ljrsA1A', '6VkE0AEt18JPo4scJ', 'KZyRktW0PRU4efS4k', '3AluFrydbWIHwuzDg'];
      for (let i = 0; i < ruleIds.length; i++) {
        await rc.update(ruleIds[i], {
          $set: { parent: '3wGp1954eti6HY9Ej', f: 'a' + (i + 1) }
        });
        operations++;
      }

      // 3. For each day (Day 01..42)
      for (const w of ast.weeks) {
        for (const d of w.days) {
          const m = exactMap.find(x => x.dayNum === d.num);
          if (!m || !m.dayId) continue;
          
          // Clean title
          await rc.update(m.dayId, {
            $set: { key: [d.title] }
          });
          operations++;

          // Clean Topic
          if (d.topic && topicMap[d.num]) {
            const topId = topicMap[d.num];
            await rc.update(topId, {
              $set: {
                parent: m.dayId,
                f: 'a0',
                key: [d.topic]
              },
              $unset: { ps: true, psh: true, apu: true, aph: true }
            });
            operations++;
          }

          // Theory
          if (m.theoryId) {
            const tSec = d.sections.find(s => s.type === 'theory');
            const tTitle = tSec ? tSec.title : 'Теория:';
            await rc.update(m.theoryId, {
              $set: {
                parent: m.dayId,
                f: 'a1',
                key: [tTitle]
              },
              $unset: { ps: true, psh: true }
            });
            operations++;

            // Ensure kids of theory have checkboxes & clean links
            const tKids = all.filter(r => r.parent === m.theoryId);
            for (const tk of tKids) {
              const kStr = JSON.stringify(tk.key || '');
              if (kStr.includes('⏱️') || kStr.includes('Не обязательно')) continue;
              
              const updateObj = {
                apu: {
                  ...(tk.apu || {}),
                  t: { v: true, ',u': now },
                  i: { v: false, ',u': now }
                }
              };
              // Link resolution
              if (Array.isArray(tk.key)) {
                updateObj.key = tk.key.map(part => {
                  if (part && typeof part === 'object' && part.i === 'q' && part._id) {
                    const tr = remById.get(part._id);
                    const title = tr ? extractText(tr.key) : '';
                    if (title) {
                      return { ...part, text: title, textOfDeletedRem: [title] };
                    }
                  }
                  return part;
                });
              }
              await rc.update(tk._id, { $set: updateObj });
              operations++;
            }
          }

          // Coding
          if (m.codingId) {
            const cSec = d.sections.find(s => s.type === 'coding');
            const cTitle = cSec ? cSec.title : 'Кодинг:';
            await rc.update(m.codingId, {
              $set: {
                parent: m.dayId,
                f: 'a2',
                key: [cTitle]
              },
              $unset: { ps: true, psh: true }
            });
            operations++;

            // Ensure kids of coding have checkboxes & clean links
            const cKids = all.filter(r => r.parent === m.codingId);
            for (const ck of cKids) {
              const kStr = JSON.stringify(ck.key || '');
              if (kStr.includes('⏱️') || kStr.includes('Не обязательно') || kStr.includes('🎯')) continue;

              const updateObj = {
                apu: {
                  ...(ck.apu || {}),
                  t: { v: true, ',u': now },
                  i: { v: false, ',u': now }
                }
              };
              if (Array.isArray(ck.key)) {
                updateObj.key = ck.key.map(part => {
                  if (part && typeof part === 'object' && part.i === 'q' && part._id) {
                    const tr = remById.get(part._id);
                    const title = tr ? extractText(tr.key) : '';
                    if (title) {
                      return { ...part, text: title, textOfDeletedRem: [title] };
                    }
                  }
                  return part;
                });
              }
              await rc.update(ck._id, { $set: updateObj });
              operations++;
            }
          }

          // Standout
          if (m.standoutId) {
            const sSec = d.sections.find(s => s.type === 'standout');
            const sTitle = sSec ? sSec.title : '🎯 Стенд-аут (15 минут · код-ревью):';
            await rc.update(m.standoutId, {
              $set: {
                parent: m.dayId,
                f: 'a3',
                key: [sTitle]
              },
              $unset: { ps: true, psh: true }
            });
            operations++;
          }

          // Checklist
          if (m.checklistId) {
            const chSec = d.sections.find(s => s.type === 'checklist');
            const chTitle = chSec ? chSec.title : '✅ Чек-лист готовности:';
            const fVal = m.standoutId ? 'a4' : 'a3';
            await rc.update(m.checklistId, {
              $set: {
                parent: m.dayId,
                f: fVal,
                key: [chTitle]
              },
              $unset: { ps: true, psh: true }
            });
            operations++;

            // Ensure kids of checklist have checkboxes
            const chKids = all.filter(r => r.parent === m.checklistId);
            for (const chk of chKids) {
              await rc.update(chk._id, {
                $set: {
                  apu: {
                    ...(chk.apu || {}),
                    t: { v: true, ',u': now },
                    i: { v: false, ',u': now }
                  }
                }
              });
              operations++;
            }
          }
        }
      }

      return {
        success: true,
        operations
      };
    } catch (e) {
      return { error: e.message, stack: e.stack };
    }
  })()`;

  console.log('Sending full update to Chrome via bridge...');
  const res = await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    body: code
  });
  console.log(await res.json());
}

execute();
