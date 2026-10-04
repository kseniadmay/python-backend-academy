const http = require('http');
const fs = require('fs');

const devToolsPortFile = 'C:\\Users\\fury6\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const [port, browserPath] = fs.readFileSync(devToolsPortFile, 'utf8').trim().split('\n');
const wsUrl = `ws://127.0.0.1:${port.trim()}${browserPath.trim()}`;
console.log('Connecting to Chrome at', wsUrl);

const ws = new WebSocket(wsUrl);
let targetSessionId = null;
let targetInfo = null;
let msgId = 10;
const pending = new Map();
let serverStarted = false;

ws.onopen = () => {
  console.log('WebSocket to Chrome opened');
  ws.send(JSON.stringify({ id: 1, method: 'Target.getTargets' }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id === 1) {
    targetInfo = msg.result.targetInfos.find(t => t.url && t.url.includes('GwREY4bq5eQvPyeAB'));
    if (!targetInfo) {
      console.error('Target not found!');
      return;
    }
    console.log('Attaching to target:', targetInfo.targetId, targetInfo.title);
    ws.send(JSON.stringify({
      id: 2,
      method: 'Target.attachToTarget',
      params: { targetId: targetInfo.targetId, flatten: true }
    }));
  } else if (msg.id === 2 && !serverStarted) {
    serverStarted = true;
    targetSessionId = msg.result.sessionId;
    console.log('Attached with sessionId:', targetSessionId);
    startServer();
  } else if (pending.has(msg.id)) {
    const resolve = pending.get(msg.id);
    pending.delete(msg.id);
    resolve(msg);
  }
};

function sendCDP(method, params = {}) {
  return new Promise((resolve) => {
    const id = msgId++;
    pending.set(id, resolve);
    ws.send(JSON.stringify({
      sessionId: targetSessionId,
      id,
      method,
      params
    }));
  });
}

function startServer() {
  const server = http.createServer(async (req, res) => {
    if (req.method === 'GET' && req.url === '/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, target: targetInfo, sessionId: targetSessionId }));
      return;
    }
    if (req.method === 'POST' && req.url === '/eval') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', async () => {
        try {
          const resp = await sendCDP('Runtime.evaluate', {
            expression: body,
            awaitPromise: true,
            returnByValue: true
          });
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify(resp.result ? resp.result.result : resp));
        } catch (e) {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }
    if (req.method === 'POST' && req.url === '/screenshot') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', async () => {
        try {
          const { path } = JSON.parse(body || '{}');
          await sendCDP('Page.enable');
          const resp = await sendCDP('Page.captureScreenshot', { format: 'png' });
          if (resp.result && resp.result.data) {
            fs.writeFileSync(path, Buffer.from(resp.result.data, 'base64'));
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ ok: true, savedTo: path }));
          } else {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Screenshot failed', resp }));
          }
        } catch (e) {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }
    res.writeHead(404);
    res.end();
  });

  server.listen(9999, '127.0.0.1', () => {
    console.log('Chrome bridge server listening on http://127.0.0.1:9999');
  });
}
