const fs = require('fs');

const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');

const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.attachToTarget',
    params: {
      targetId: '51B0D7B7180A1C1995B5B01ED2D6E6F9',
      flatten: true
    }
  }));
};

let sessionId = null;

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Runtime.evaluate',
      params: {
        expression: `(() => {
          const els = Array.from(document.querySelectorAll('[data-rem-id]'));
          return els.map(el => ({
            id: el.getAttribute('data-rem-id'),
            tag: el.tagName,
            text: el.innerText.trim().substring(0, 100),
            className: el.className
          }));
        })()`,
        returnByValue: true
      }
    }));
  }

  if (msg.id === 2) {
    const list = msg.result.result.value;
    console.log('Rem elements on page:', list.length);
    list.slice(0, 25).forEach((item, idx) => {
      console.log(`${idx + 1}. [${item.id}] <${item.tag}>: "${item.text}"`);
    });
    ws.close();
  }
};
