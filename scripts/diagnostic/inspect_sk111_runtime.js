const puppeteer = require('puppeteer-core');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  const filePath = 'file:///' + path.resolve('academy.html').replace(/\\/g, '/');
  await page.goto(filePath, { waitUntil: 'domcontentloaded' });

  const data = await page.evaluate(() => {
    const s = PY_SKILLS_BY_ID['1.1.1'];
    const notes = (s.kIds || []).map(k => {
      const n = ALL_NOTES_COMBINED[k] || {};
      return { id: k, title: n.title || k };
    });
    const decks = (s.fIds || []).map(f => {
      const d = ALL_DECKS_COMBINED[f] || {};
      return { id: f, title: d.title || f };
    });
    const tasks = (s.taskIds || []).map(t => {
      const task = IDE_TASKS_BY_ID[t] || {};
      return { id: t, title: task.title || ('Задача #' + t) };
    });
    return { title: s.title, notes, decks, tasks };
  });

  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})();
