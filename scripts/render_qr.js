const path = require('path');
const cri = require(path.join('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\python_trainer', 'node_modules', 'chrome-remote-interface'));
const fs = require('fs');
const vm = require('vm');
const { spawn } = require('child_process');

const OUT = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\837a7fb7-8b1d-4564-8eeb-49f6242e6dba\\';

const sandbox = {};
vm.runInNewContext(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\python_trainer\\src\\qr.js', 'utf8'), sandbox);
const tunnelUrl = 'https://rna-review-feelings-gives.trycloudflare.com/academy.html#/';
const svgContent = sandbox.OfflineQR.generateSVG(tunnelUrl, 320);

const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 24px;
    background: #0d1016;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 440px;
    box-sizing: border-box;
  }
  .card {
    background: #1B1E15;
    border: 1px solid #33362A;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .title {
    font-size: 20px;
    font-weight: 700;
    color: #ECEDE2;
    margin-bottom: 6px;
  }
  .subtitle {
    font-size: 13px;
    color: #8B8D80;
    margin-bottom: 18px;
  }
  .qr-box {
    margin-bottom: 16px;
    border-radius: 12px;
    overflow: hidden;
  }
  .badge {
    background: rgba(116, 172, 130, 0.12);
    color: #74AC82;
    border: 1px solid rgba(116, 172, 130, 0.28);
    font-size: 12px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 999px;
  }
</style>
</head>
<body>
  <div class="card">
    <div class="title">🎓 Python Backend Academy</div>
    <div class="subtitle">Наведите камеру смартфона для входа</div>
    <div class="qr-box">${svgContent}</div>
    <div class="badge">🔒 Защищённый туннель HTTPS (PWA)</div>
  </div>
</body>
</html>`;

const tmpHtml = 'C:\\Users\\fury6\\AppData\\Local\\Temp\\real_qr_card.html';
fs.writeFileSync(tmpHtml, html, 'utf8');

const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--disable-gpu', '--remote-debugging-port=9229',
    '--user-data-dir=C:\\Users\\fury6\\AppData\\Local\\Temp\\chrome_real_qr',
    '--window-size=440,560', '--no-first-run'
], { stdio: 'ignore' });

setTimeout(async () => {
    let client;
    try {
        client = await cri({ port: 9229 });
        const { Page, Emulation } = client;
        await Page.enable();
        await Emulation.setDeviceMetricsOverride({
            width: 440,
            height: 560,
            deviceScaleFactor: 2,
            mobile: false
        });

        await Page.navigate({ url: 'file:///' + tmpHtml.replace(/\\/g, '/') });
        await Page.loadEventFired();
        await new Promise(r => setTimeout(r, 1200));

        const s = await Page.captureScreenshot({ format: 'png' });
        fs.writeFileSync(OUT + 'real_academy_qr.png', Buffer.from(s.data, 'base64'));
        console.log('real_academy_qr.png generated!');
    } catch(e) {
        console.error('Error:', e);
    } finally {
        if (client) client.close();
        chrome.kill();
    }
}, 2000);
