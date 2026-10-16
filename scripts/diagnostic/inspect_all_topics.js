const fs = require('fs');

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

      const topicIds = [
        '31DthKFeDUSFy8kIf', '9KxSKro6nlcoZCCBl', '0IpA4W3iyh9beq2Lh', 'K7J5Um8xr3O9heMxv',
        'AF7cK0oKUkcbdDR5Z', '1N3Socza2f94IRoE7', 'WTbFgiLCgSV8e2dnM', 'JDHEgCaLJVcaFr6is',
        'phwIImGVeXttAUYbA', 'bKQUp0bNb8cGiR7dr', '0jnGYoC4LMlS3P7ON', '5rkqcmMAyUbN0Vke8',
        'eTrJWkIVfPITVMoj3', 't1o58b5THG5vNSk9e', '5sEstc4mdKN7snoYP', 'VQXkbYN5T2BxFrduz',
        'UXutSmCbGvgUzVro7', 'SxOTF6YHeTDvMCPs7', 'ItFWzl1GPSQTj5ZRj', 'pFqVPTMSofWEKJ2Oh',
        'CeEHOA7zOu4eXEqj5', 'GbaXHnwGsSSc2ZNhQ', 'q7aXpevG2kiUKso1V', '1ROIV9i19u72vTJ53',
        'Hw3wSc2uAA72QttKW', '22z7fvTiWF6fncggu', 'PpGxSbpK9Sx1hsGTU', 'IqO2rjYVySNwkPM59',
        'cdDFn7vCzjjSdTUn7', '1JcnnCZd8qEAC0raX', 'An5a4v3ArfqIdEobr', '61qPBRQJFa1jZUl86',
        'wfiThaYeDbVnPErjI', 'E8NC56N8tFfJL4FeN'
      ];

      return topicIds.map(id => {
        const r = all.find(x => x._id === id);
        return {
          id,
          text: r ? extractText(r.key) : 'NOT FOUND'
        };
      });
    })()`
  });
  const data = await res.json();
  data.value.forEach((t, idx) => {
    console.log(`[${idx+1}] [${t.id}]: "${t.text.replace(/\n/g, '\\n')}"`);
  });
}
run();
