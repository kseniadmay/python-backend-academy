const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const artifactDir = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\2b320042-cd74-466b-b716-1ee73a7ff7f2';

const targets = [
  {
    url: 'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/design_mockups/full_screen_v1_airy.html#/python/skill/1.1.1',
    outLocal: path.join(__dirname, '..', 'design_mockups', 'full_screen_v1_airy.png'),
    outArtifact: path.join(artifactDir, 'full_screen_v1_airy.png'),
    name: 'Вариант 1 (Airy Minimal)'
  },
  {
    url: 'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/design_mockups/full_screen_v2_capsule.html#/python/skill/1.1.1',
    outLocal: path.join(__dirname, '..', 'design_mockups', 'full_screen_v2_capsule.png'),
    outArtifact: path.join(artifactDir, 'full_screen_v2_capsule.png'),
    name: 'Вариант 2 (Subtle Capsule)'
  }
];

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  console.log('Spawning Chrome...');
  const proc = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--disable-gpu',
    '--no-sandbox',
    '--hide-scrollbars',
    'about:blank'
  ]);

  await sleep(1500);

  try {
    for (const item of targets) {
      console.log(`Processing ${item.name}...`);
      const newRes = await fetch('http://127.0.0.1:9222/json/new', { method: 'PUT' });
      const target = await newRes.json();

      const ws = new WebSocket(target.webSocketDebuggerUrl);
      let msgId = 1;
      const pending = new Map();

      ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.id && pending.has(data.id)) {
          const { resolve, reject } = pending.get(data.id);
          pending.delete(data.id);
          if (data.error) reject(new Error(JSON.stringify(data.error)));
          else resolve(data.result);
        }
      };

      await new Promise((res, rej) => {
        ws.onopen = res;
        ws.onerror = rej;
      });

      function send(method, params = {}) {
        const id = msgId++;
        return new Promise((resolve, reject) => {
          pending.set(id, { resolve, reject });
          ws.send(JSON.stringify({ id, method, params }));
        });
      }

      await send('Page.enable');
      await send('Emulation.setDeviceMetricsOverride', {
        width: 1440,
        height: 960,
        deviceScaleFactor: 2,
        mobile: false
      });

      await send('Page.navigate', { url: item.url });
      await sleep(2500);

      await send('Runtime.evaluate', {
        expression: `
          document.documentElement.setAttribute('data-theme', 'light');
          if(typeof route === 'function') {
            window.location.hash = '#/python/skill/1.1.1';
            route();
          }
        `
      });
      await sleep(1500);

      const shot = await send('Page.captureScreenshot', { format: 'png' });
      const buf = Buffer.from(shot.data, 'base64');
      fs.writeFileSync(item.outLocal, buf);
      fs.writeFileSync(item.outArtifact, buf);
      console.log(`Saved ${item.name} to ${item.outArtifact}`);

      ws.close();
      await sleep(500);
    }
  } catch (err) {
    console.error('Error during captures:', err);
  } finally {
    proc.kill();
  }
}

run();
