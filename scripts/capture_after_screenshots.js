const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const academyUrl = 'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/academy.html';
const outDir = path.join(__dirname, '..', 'design_mockups');

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
    // 1. Get new page target
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
    await send('Runtime.enable');

    const tasks = [
      {
        name: 'after_01_desk_dark_dashboard.png',
        route: '#/',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: Дашборд с 7-Track матрицей, SRS виджетом и сгруппированным сайдбаром'
      },
      {
        name: 'after_02_desk_light_dashboard.png',
        route: '#/',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'light',
        desc: 'Десктоп: Дашборд в светлой теме 60/30/10'
      },
      {
        name: 'after_04_desk_skill_1_1_1.png',
        route: '#/python/skill/1.1.1',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: Двухколоночный Split View (Теория 60% + Лаборатория 40% и схема CPython памяти)'
      },
      {
        name: 'after_05_desk_practice_ide.png',
        route: '#/practice',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: IDE с панелью быстрых токенов, гаттером номеров строк и чипсами'
      },
      {
        name: 'after_06_desk_mock_interview.png',
        route: '#/mock',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: Собеседование с 20-мин круговым SVG-таймером, чатом Tech Lead и STAR'
      },
      {
        name: 'after_07_desk_flashcards.png',
        route: '#/cards',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: 3D-карточки со Stories-style segmented progress bar'
      },
      {
        name: 'after_08_desk_skill_tree_map.png',
        route: '#/map',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: Карта навыков с ровными эшелонами без наложения процентов'
      },
      {
        name: 'after_09_desk_python_boss.png',
        route: '#/python/boss',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: Финальный Босс с сегментированной шкалой Boss HP Bar'
      },
      {
        name: 'after_10_mob_practice_ide.png',
        route: '#/practice',
        width: 390, height: 844, dsf: 2, mobile: true, theme: 'dark',
        desc: 'Мобильный: Практика IDE с горизонтальными чипсами и липким Accessory Bar'
      },
      {
        name: 'after_11_mob_mock_interview.png',
        route: '#/mock',
        width: 390, height: 844, dsf: 2, mobile: true, theme: 'dark',
        desc: 'Мобильный: Собеседование с круговым SVG-таймером и чистым экраном'
      },
      {
        name: 'after_12_mob_flashcards.png',
        route: '#/cards',
        width: 390, height: 844, dsf: 2, mobile: true, theme: 'dark',
        desc: 'Мобильный: 3D-карточки без оверлея кнопки замечания и со Stories-баром'
      },
      {
        name: 'after_14_mob_light_dashboard.png',
        route: '#/',
        width: 390, height: 844, dsf: 2, mobile: true, theme: 'light',
        desc: 'Мобильный: Дашборд в светлой теме с мини-матрицей 7 направлений'
      },
      {
        name: 'after_15_desk_coddy_path.png',
        route: '#/path',
        width: 1440, height: 900, dsf: 1, mobile: false, theme: 'dark',
        desc: 'Десктоп: 3D Serpentine S-Curve Path с плоскими гексагонами и плавающим поповером Coddy'
      },
      {
        name: 'after_16_mob_coddy_path.png',
        route: '#/path',
        width: 390, height: 844, dsf: 2, mobile: true, theme: 'dark',
        desc: 'Мобильный: Вертикальная 3D-тропа приключения со скроллом и якорными поповерами'
      },
      {
        name: 'after_17_mob_coddy_ide_tabs.png',
        route: '#/practice',
        width: 390, height: 844, dsf: 2, mobile: true, theme: 'dark',
        desc: 'Мобильный: 4-вкладочная IDE Coddy [Справка] [Задача] [Код] [Решение] с плавающей 3D-кнопкой'
      }
    ];

    for (const t of tasks) {
      console.log(`Capturing: ${t.name}...`);
      await send('Emulation.setDeviceMetricsOverride', {
        width: t.width,
        height: t.height,
        deviceScaleFactor: t.dsf,
        mobile: t.mobile
      });

      const fullUrl = `${academyUrl}${t.route}`;
      await send('Page.navigate', { url: fullUrl });
      await sleep(1200);

      if (t.theme) {
        await send('Runtime.evaluate', {
          expression: `document.documentElement.setAttribute('data-theme', '${t.theme}'); localStorage.setItem('academy_theme', '${t.theme}'); true;`
        });
        await sleep(300);
      }

      // Small scroll reset
      await send('Runtime.evaluate', { expression: `window.scrollTo(0, 0); true;` });
      await sleep(200);

      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
      const buf = Buffer.from(shot.data, 'base64');
      const targetFile = path.join(outDir, t.name);
      fs.writeFileSync(targetFile, buf);
      console.log(`✓ Saved: ${t.name} (${(buf.length / 1024).toFixed(1)} KB)`);
    }

    ws.close();
    console.log('All screenshots captured successfully!');
  } finally {
    proc.kill();
  }
}

run().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
