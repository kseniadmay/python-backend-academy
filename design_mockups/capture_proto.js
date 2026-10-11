const { spawn } = require('child_process');
const fs = require('fs');

async function runCapture() {
  const p = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9389',
    '--user-data-dir=C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\cdp_proto_test',
    '--window-size=1280,960', '--disable-gpu', 'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  const tabs = await (await fetch('http://127.0.0.1:9389/json/list')).json();
  const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 1;
  const send = (method, params = {}) => new Promise(res => {
    const cur = id++;
    const h = e => {
      const d = JSON.parse(e.data);
      if (d.id === cur) { ws.removeEventListener('message', h); res(d.result); }
    };
    ws.addEventListener('message', h);
    ws.send(JSON.stringify({ id: cur, method, params }));
  });

  const url = 'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/design_mockups/practice_redesign_options.html';
  await send('Page.navigate', { url });
  await new Promise(r => setTimeout(r, 1500));

  // 1. Variant 1 (Coddy Studio Pro)
  let s1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\design_mockups\\shot_variant_1_split.png', Buffer.from(s1.data, 'base64'));
  console.log('Saved shot_variant_1_split.png');

  // 2. Click Socratic hint in V1
  await send('Runtime.evaluate', { expression: `toggleHint('v1');` });
  await new Promise(r => setTimeout(r, 300));
  let s1_hint = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\design_mockups\\shot_variant_1_hint.png', Buffer.from(s1_hint.data, 'base64'));

  // 3. Variant 2 (Compact Minimalist)
  await send('Runtime.evaluate', { expression: `switchView('v2');` });
  await new Promise(r => setTimeout(r, 400));
  let s2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\design_mockups\\shot_variant_2_card.png', Buffer.from(s2.data, 'base64'));
  console.log('Saved shot_variant_2_card.png');

  // 4. Variant 3 (Visual Slice Studio with Anatomy Widget)
  await send('Runtime.evaluate', { expression: `switchView('v3'); toggleHint('v3');` });
  await new Promise(r => setTimeout(r, 400));
  let s3 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\design_mockups\\shot_variant_3_anatomy.png', Buffer.from(s3.data, 'base64'));
  console.log('Saved shot_variant_3_anatomy.png');

  p.kill();
  console.log('All real browser screenshots captured successfully!');
}

runCapture().catch(console.error);
