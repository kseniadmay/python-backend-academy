const fs = require('fs');

const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');

const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

const targetUrl = 'https://www.remnote.com/w/69d8425df107d8b00ed6ddb9/--Junior-Python-Backend-Developer-GwREY4bq5eQvPyeAB';

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

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    sessionId = msg.result.sessionId;
    console.log('Attached! Navigating to:', targetUrl);
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Page.navigate',
      params: { url: targetUrl }
    }));
  }

  if (msg.id === 2) {
    console.log('Navigation initiated. Waiting 4 seconds for page load...');
    setTimeout(() => {
      ws.send(JSON.stringify({
        sessionId,
        id: 3,
        method: 'Runtime.evaluate',
        params: {
          expression: `(() => {
            return {
              href: window.location.href,
              title: document.title,
              hasRemNote: !!window.RemNoteAPI || !!window.remnote,
              keys: Object.keys(window).filter(k => k.toLowerCase().includes('rem') || k.toLowerCase().includes('sync')),
              docTextPreview: document.body.innerText.substring(0, 300)
            };
          })()`,
          returnByValue: true
        }
      }));
    }, 4000);
  }

  if (msg.id === 3) {
    console.log('Result after navigation:', msg.result.result.value);
    ws.close();
  }
};
