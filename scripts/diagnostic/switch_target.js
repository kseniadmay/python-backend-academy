const fs = require('fs');
const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  // Close old error tab
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.closeTarget',
    params: { targetId: '51B0D7B7180A1C1995B5B01ED2D6E6F9' }
  }));
};

ws.onmessage = async (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    console.log('Old target closed:', msg.result);
    // Connect to new target
    ws.send(JSON.stringify({
      id: 2,
      method: 'Target.attachToTarget',
      params: { targetId: 'EACF2DEC831193C2BF4A35C5F0DF5C41', flatten: true }
    }));
  }
  if (msg.id === 2) {
    const sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 3,
      method: 'Runtime.evaluate',
      params: {
        expression: `(() => {
          const els = Array.from(document.querySelectorAll('[data-rem-id]'));
          return JSON.stringify({
            title: document.title,
            elsCount: els.length
          });
        })()`,
        returnByValue: true
      }
    }));
  }
  if (msg.id === 3) {
    console.log('New tab state:', msg.result.result.value);
    ws.close();
  }
};