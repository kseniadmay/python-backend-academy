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

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    sessionId = msg.result.sessionId;
    ws.send(JSON.stringify({
      sessionId,
      id: 2,
      method: 'Runtime.evaluate',
      params: {
        expression: `(() => {
          const docId = 'GwREY4bq5eQvPyeAB';
          const r = window.Rem ? (window.Rem.find ? window.Rem.find(docId) : (window.Rem.findOne ? window.Rem.findOne(docId) : null)) : null;
          return {
            remMethods: window.Rem ? Object.getOwnPropertyNames(window.Rem).slice(0, 30) : [],
            remPrototype: window.Rem && window.Rem.prototype ? Object.getOwnPropertyNames(window.Rem.prototype).slice(0, 30) : [],
            r: r ? { _id: r._id, key: r.key, text: r.text, children: r.children } : null
          };
        })()`,
        returnByValue: true
      }
    }));
  }

  if (msg.id === 2) {
    console.log('Rem object info:', msg.result.result.value);
    ws.close();
  }
};
