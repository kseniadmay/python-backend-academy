const http = require('http');

function evalCDP(jsCode) {
  return new Promise((resolve, reject) => {
    const req = http.request('http://127.0.0.1:9999/eval', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.write(jsCode);
    req.end();
  });
}

async function findScroller() {
  const code = `(() => {
    const allDivs = Array.from(document.querySelectorAll('*'));
    const scrollable = allDivs.filter(el => {
      const style = window.getComputedStyle(el);
      return (style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
    });
    return scrollable.map(el => ({
      tagName: el.tagName,
      className: el.className,
      id: el.id,
      scrollHeight: el.scrollHeight,
      clientHeight: el.clientHeight,
      scrollTop: el.scrollTop
    }));
  })()`;

  const res = await evalCDP(code);
  console.log('Scrollable elements:', res);
}

findScroller();
