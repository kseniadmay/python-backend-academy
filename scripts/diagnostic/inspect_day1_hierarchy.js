async function run() {
  const res = await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    body: `(async () => {
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
      const tg = rem.getTinyGraph();
      const rc = tg.getRemCollection();
      const all = await rc.DatabaseStore.fetchAllImpl();
      
      function extractText(key) {
        if (!key) return '';
        if (typeof key === 'string') return key;
        if (Array.isArray(key)) return key.map(p => typeof p === 'string' ? p : (p.text || '')).join('');
        return '';
      }

      // Week 1 id = i2G5Z1gxlEaEf4Sz3
      const w1Kids = all.filter(r => r.parent === 'i2G5Z1gxlEaEf4Sz3').sort((a,b) => (a.f||'').localeCompare(b.f||''));
      const d1 = w1Kids[0];
      const d1Kids = all.filter(r => r.parent === d1._id).sort((a,b) => (a.f||'').localeCompare(b.f||''));

      return {
        w1Kids: w1Kids.map(k => ({ id: k._id, f: k.f, text: extractText(k.key) })),
        d1Kids: d1Kids.map(k => ({
          id: k._id,
          f: k.f,
          text: extractText(k.key),
          subKidsCount: all.filter(r => r.parent === k._id).length
        }))
      };
    })()`
  });
  console.log(JSON.stringify(await res.json(), null, 2));
}
run();
