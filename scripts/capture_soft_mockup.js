const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/design_mockups/full_screen_light_mirror.html#/python/skill/1.1.1';
const outPath = path.join(__dirname, '..', 'design_mockups', 'full_screen_light_soft.png');
const artifactPath = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\2b320042-cd74-466b-b716-1ee73a7ff7f2\\full_screen_light_soft.png';

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
    const newRes = await fetch('http://127.0.0.1:9222/json/new', { method: 'PUT' });
    const target = await newRes.json();
    console.log('Opened target:', target.id);

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

    console.log('Navigating to target...');
    await send('Page.navigate', { url: targetUrl });
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
    await sleep(1500);

    console.log('Capturing viewport screenshot...');
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(shot.data, 'base64');
    fs.writeFileSync(outPath, buf);
    console.log('Saved to:', outPath);

    fs.writeFileSync(artifactPath, buf);
    console.log('Saved to artifact:', artifactPath);

    ws.close();
  } catch (err) {
    console.error('Error during capture:', err);
  } finally {
    proc.kill();
  }
}

run();
