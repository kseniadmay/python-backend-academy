const fs = require('fs');

const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const content = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const port = content[0].trim();
const browserPath = content[1].trim();

const wsUrl = `ws://127.0.0.1:${port}${browserPath}`;
console.log('Connecting to:', wsUrl);

const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  console.log('Connected to Chrome CDP!');
  // Request targets
  ws.send(JSON.stringify({
    id: 1,
    method: 'Target.getTargets'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.id === 1) {
    console.log('Received targets:', data.result.targetInfos.length);
    for (const t of data.result.targetInfos) {
      if (t.type === 'page') {
        console.log(`PAGE [${t.targetId}]: "${t.title}" -> ${t.url}`);
      }
    }
    ws.close();
  }
};

ws.onerror = (err) => {
  console.error('WS Error:', err);
};
