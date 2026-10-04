const fs = require('fs');

async function run() {
  const structuralUpdates = JSON.parse(fs.readFileSync('all_structural_updates.json', 'utf8'));
  const exactMap = JSON.parse(fs.readFileSync('exact_42_days_map.json', 'utf8'));

  console.log('Sending updates to Chrome via persistent bridge...');

  const payload = {
    structuralUpdates,
    exactMap
  };

  const code = `(async () => {
    try {
      const data = ${JSON.stringify(payload)};
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

      // 1. Apply structural updates (Rules, TOC, Day titles, Topics, Sections)
      let appliedStruct = 0;
      for (const u of data.structuralUpdates) {
        await rc.update(u.id, u.update);
        appliedStruct++;
      }

      // 2. Ensure all items in Theory, Coding, Checklist have Todo checkboxes and clean links
      const sectionIds = new Set();
      data.exactMap.forEach(m => {
        if (m.theoryId) sectionIds.add(m.theoryId);
        if (m.codingId) sectionIds.add(m.codingId);
        if (m.checklistId) sectionIds.add(m.checklistId);
      });

      let updatedTodos = 0;
      let fixedLinks = 0;
      const now = Date.now();

      for (const r of all) {
        if (sectionIds.has(r.parent)) {
          const kStr = JSON.stringify(r.key || '');
          if (kStr.includes('⏱️') || kStr.includes('Не обязательно')) continue;

          // Check if needs Todo powerup
          const needsTodo = !r.apu || !r.apu.t || !r.apu.t.v;
          
          // Check if key has references that need text / textOfDeletedRem
          let needsKeyFix = false;
          let newKey = r.key;
          if (Array.isArray(r.key)) {
            newKey = r.key.map(part => {
              if (part && typeof part === 'object' && part.i === 'q' && part._id) {
                const targetRem = remById.get(part._id);
                if (targetRem) {
                  const title = extractText(targetRem.key);
                  if (title && (!part.text || !part.textOfDeletedRem)) {
                    needsKeyFix = true;
                    return {
                      ...part,
                      text: title,
                      textOfDeletedRem: [title]
                    };
                  }
                }
              }
              return part;
            });
          }

          const updateObj = {};
          if (needsTodo) {
            updateObj.apu = {
              ...(r.apu || {}),
              t: { v: true, ',u': now },
              i: { v: false, ',u': now }
            };
            updatedTodos++;
          }
          if (needsKeyFix) {
            updateObj.key = newKey;
            fixedLinks++;
          }

          if (Object.keys(updateObj).length > 0) {
            await rc.update(r._id, { $set: updateObj });
          }
        }
      }

      return {
        success: true,
        appliedStruct,
        updatedTodos,
        fixedLinks
      };
    } catch (e) {
      return { error: e.message, stack: e.stack };
    }
  })()`;

  const res = await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    body: code
  });

  const result = await res.json();
  console.log('Result:', JSON.stringify(result, null, 2));
}

run();
