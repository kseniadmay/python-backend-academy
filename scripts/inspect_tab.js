const fs = require('fs');

const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');

const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  // Attach to target
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
    console.log('Attached to RemNote tab! SessionId:', sessionId);

    // Evaluate location.href and document.title
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Runtime.evaluate',
      params: {
        expression: 'JSON.stringify({ href: window.location.href, title: document.title })',
        returnByValue: true
      }
    }));
  }

  if (msg.id === 2) {
    console.log('Page info:', JSON.parse(msg.result.result.value));
    ws.close();
  }
};
