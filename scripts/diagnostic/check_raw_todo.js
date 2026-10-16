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
      const todo = all.find(r => r._id === '6xZRTSiIXfhY6fIDT'); // Day 01 Coding kid
      const day1Kids = all.filter(r => r.parent === '6xZRTSiIXfhY6fIDT');
      return {
        sampleKid: day1Kids[0] ? { _id: day1Kids[0]._id, apu: day1Kids[0].apu, key: day1Kids[0].key } : null
      };
    })()`
  });
  console.log(JSON.stringify(await res.json(), null, 2));
}
run();
