const path = require('path');
const os = require('os');
const fs = require('fs');
const DEPS_DIR = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), '.pba-visual-deps'), 'pba-visual-deps');
const { chromium } = require(path.join(DEPS_DIR, 'node_modules', 'playwright-core'));

(async () => {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await chromium.launch({ executablePath: chromePath, headless: true });
  const page = await browser.newPage();
  const filePath = 'file://' + path.resolve('standards/standards.html').replace(/\\/g, '/');
  await page.goto(filePath, { waitUntil: 'load' });

  const extracted = await page.evaluate(() => {
    // 1. All notes combined
    const notes = window.ALL_NOTES_COMBINED || {};

    // 2. Build catalog tree: Track -> Unit -> Skill -> Notes
    const tracksCatalog = [];

    const trackKeys = ['python', 'web', 'backend', 'algorithms', 'databases', 'architecture', 'infra'];
    const trackNames = {
      python: '01 · 🐍 Python Core',
      web: '02 · 🌐 Web & HTTP',
      backend: '03 · ⚡ Backend & Asyncio',
      algorithms: '04 · 🧩 Алгоритмы & Структуры',
      databases: '05 · 🗄️ Базы данных & SQL',
      architecture: '06 · 🏛️ Архитектура & Паттерны',
      infra: '07 · 🚀 Инфраструктура & DevOps'
    };

    const masteryObjMap = {
      python: window.PY_MASTERY,
      web: window.WEB_MASTERY,
      backend: window.BACKEND_MASTERY,
      algorithms: window.ALGO_MASTERY,
      databases: window.DB_MASTERY,
      architecture: window.ARCH_MASTERY,
      infra: window.INFRA_MASTERY
    };

    const notesMeta = {};

    trackKeys.forEach(tKey => {
      const mast = masteryObjMap[tKey];
      if (!mast || !Array.isArray(mast.units)) return;

      const trackNode = {
        key: tKey,
        title: trackNames[tKey] || tKey,
        units: []
      };

      mast.units.forEach(u => {
        const cleanUTitle = (typeof window.cleanUnitTitle === 'function')
          ? window.cleanUnitTitle(u.id, u.title)
          : (u.title || '').replace(/^(?:Юнит|Урок|Модуль)\s+[\d.]+\s*[:·•\-–—]?\s*/i, '').trim();

        const uTier = (typeof window.getEffectiveUnitTier === 'function')
          ? window.getEffectiveUnitTier(u.id)
          : (u.tier || 1);

        const unitNode = {
          id: u.id,
          title: cleanUTitle || u.title,
          rawTitle: u.title,
          tier: uTier,
          skills: []
        };

        (u.skills || []).forEach(sk => {
          const rawSkTitle = (sk.title || '').replace(/^[\d.]+\s*[:·•\-]\s*/i, '').trim();
          const cleanSkTitle = rawSkTitle.split(/[:·•–—]/)[0].trim() || rawSkTitle;

          const skillNode = {
            id: sk.id,
            title: cleanSkTitle,
            rawTitle: sk.title,
            tier: uTier,
            kIds: sk.kIds || []
          };

          (sk.kIds || []).forEach(kid => {
            if (!notesMeta[kid]) {
              notesMeta[kid] = {
                noteId: kid,
                trackKey: tKey,
                trackTitle: trackNames[tKey] || tKey,
                unitId: u.id,
                unitTitle: cleanUTitle || u.title,
                skillId: sk.id,
                skillTitle: cleanSkTitle,
                tier: uTier
              };
            }
          });

          unitNode.skills.push(skillNode);
        });

        trackNode.units.push(unitNode);
      });

      tracksCatalog.push(trackNode);
    });

    return {
      totalNotes: Object.keys(notes).length,
      notes: notes,
      catalog: tracksCatalog,
      notesMeta: notesMeta
    };
  });

  console.log('Total notes extracted:', extracted.totalNotes);
  console.log('Tracks in catalog:', extracted.catalog.length);
  console.log('Notes with metadata:', Object.keys(extracted.notesMeta).length);

  fs.writeFileSync('scripts/extracted_catalog_data.json', JSON.stringify(extracted, null, 2), 'utf8');
  console.log('Saved to scripts/extracted_catalog_data.json');

  await browser.close();
})();
