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
      return {
        remProto: Object.getOwnPropertyNames(Object.getPrototypeOf(rem)).filter(m => !m.startsWith('_')).slice(0, 40),
        tgProto: Object.getOwnPropertyNames(Object.getPrototypeOf(tg)).filter(m => !m.startsWith('_')).slice(0, 40)
      };
    })()`
  });
  console.log(JSON.stringify(await res.json(), null, 2));
}
run();
