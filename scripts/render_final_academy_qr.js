const path = require('path');
const cri = require(path.join('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\python_trainer', 'node_modules', 'chrome-remote-interface'));
const fs = require('fs');
const vm = require('vm');
const { spawn } = require('child_process');

const OUT = 'C:\\Users\\fury6\\.gemini\\antigravity\\brain\\837a7fb7-8b1d-4564-8eeb-49f6242e6dba\\';

const sandbox = {};
vm.runInNewContext(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\python_trainer\\src\\qr.js', 'utf8'), sandbox);
const liveUrl = 'https://kseniadmay.github.io/python-backend-academy/';
const svgContent = sandbox.OfflineQR.generateSVG(liveUrl, 300);

const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 32px 24px;
    background: #0d1016;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 480px;
    box-sizing: border-box;
  }
  .card {
    background: #1B1E15;
    border: 1px solid #33362A;
    border-radius: 24px;
    padding: 28px 24px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    box-sizing: border-box;
  }
  .badge-top {
    background: rgba(116, 172, 130, 0.15);
    color: #74AC82;
    border: 1px solid rgba(116, 172, 130, 0.35);
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 999px;
    margin-bottom: 14px;
  }
  .title {
    font-size: 22px;
    font-weight: 700;
    color: #ECEDE2;
    margin-bottom: 6px;
  }
  .subtitle {
    font-size: 13.5px;
    color: #8B8D80;
    margin-bottom: 20px;
    line-height: 1.45;
  }
  .qr-box {
    background: #FFFFFF;
    padding: 16px;
    border-radius: 20px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
    margin-bottom: 20px;
    display: inline-block;
  }
  .stats-row {
    display: flex;
    gap: 12px;
    width: 100%;
    margin-bottom: 18px;
  }
  .stat-pill {
    flex: 1;
    background: #21241A;
    border: 1px solid #33362A;
    border-radius: 12px;
    padding: 10px;
  }
  .stat-val {
    font-size: 17px;
    font-weight: 700;
    color: #74AC82;
  }
  .stat-lbl {
    font-size: 11px;
    color: #8B8D80;
    margin-top: 2px;
  }
  .url-text {
    font-family: monospace;
    font-size: 12px;
    color: #DA9C63;
    background: #21241A;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #33362A;
    word-break: break-all;
  }
</style>
</head>
<body>
  <div class="card">
    <div class="badge-top">🟢 Доступно 24/7 без включенного ПК</div>
    <div class="title">🎓 Python Backend Academy</div>
    <div class="subtitle">Отсканируйте камерой смартфона для входа.<br>Ваш текущий прогресс сохранён и активен!</div>
    
    <div class="stats-row">
      <div class="stat-pill">
        <div class="stat-val">409 XP</div>
        <div class="stat-lbl">Опыт</div>
      </div>
      <div class="stat-pill">
        <div class="stat-val" style="color:#DA9C63;">3 дня 🔥</div>
        <div class="stat-lbl">Стрик</div>
      </div>
      <div class="stat-pill">
        <div class="stat-val" style="color:#ECEDE2;">30/31</div>
        <div class="stat-lbl">Тест сдан</div>
      </div>
    </div>

    <div class="qr-box">${svgContent}</div>
    <div class="url-text">${liveUrl}</div>
  </div>
</body>
</html>`;

const tmpHtml = 'C:\\Users\\fury6\\AppData\\Local\\Temp\\final_academy_qr_card.html';
fs.writeFileSync(tmpHtml, html, 'utf8');

const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--disable-gpu', '--remote-debugging-port=9235',
    '--user-data-dir=C:\\Users\\fury6\\AppData\\Local\\Temp\\chrome_final_qr',
    '--window-size=480,680', '--no-first-run'
], { stdio: 'ignore' });

setTimeout(async () => {
    let client;
    try {
        client = await cri({ port: 9235 });
        const { Page, Emulation } = client;
        await Page.enable();
        await Emulation.setDeviceMetricsOverride({
            width: 480,
            height: 680,
            deviceScaleFactor: 2,
            mobile: false
        });

        await Page.navigate({ url: 'file:///' + tmpHtml.replace(/\\/g, '/') });
        await Page.loadEventFired();
        await new Promise(r => setTimeout(r, 1200));

        const s = await Page.captureScreenshot({ format: 'png' });
        fs.writeFileSync(OUT + 'academy_24_7_qr.png', Buffer.from(s.data, 'base64'));
        console.log('academy_24_7_qr.png generated successfully!');
    } catch(e) {
        console.error('Error:', e);
    } finally {
        if (client) client.close();
        chrome.kill();
    }
}, 2000);
