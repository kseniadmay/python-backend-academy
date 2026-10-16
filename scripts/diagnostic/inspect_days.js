const http = require('http');

function evalInPage(code) {
  return new Promise((resolve, reject) => {
    const req = http.request('http://127.0.0.1:9999/eval', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.write(code);
    req.end();
  });
}

async function run() {
  const code = `
    (async () => {
      const doc = await rc.getRemById('GwREY4bq5eQvPyeAB');
      const weeks = await doc.getChildren();
      const results = [];
      for (const w of weeks) {
        const wText = await w.text();
        if (!wText.includes('Неделя')) continue;
        const days = await w.getChildren();
        for (const d of days) {
          const dText = await d.text();
          const children = await d.getChildren();
          const firstChild = children[0] ? await children[0].text() : null;
          results.push({
            week: wText.slice(0, 30),
            dayId: d._id,
            dayText: dText,
            firstChildId: children[0]?._id,
            firstChild: firstChild,
            childrenCount: children.length
          });
        }
      }
      return results;
    })()
  `;
  const res = await evalInPage(code);
  console.log(JSON.stringify(res.value, null, 2));
}

run();
