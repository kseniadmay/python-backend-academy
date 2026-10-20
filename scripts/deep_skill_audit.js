'use strict';
const path = require('path');
const fs = require('fs');
const os = require('os');

const pwPath = path.join(os.homedir(), '.pba-visual-deps', 'node_modules', 'playwright-core');
const { chromium } = require(pwPath);

function findBrowser() {
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium'
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  const macPwCache = path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright');
  if (fs.existsSync(macPwCache)) {
    for (const d of fs.readdirSync(macPwCache)) {
      const exe = path.join(macPwCache, d, 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium');
      if (fs.existsSync(exe)) return exe;
    }
  }
  return null;
}

const OUT_DIR = path.join(__dirname, 'visual_report', 'skill_audit');
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

(async () => {
  const browser = await chromium.launch({
    executablePath: findBrowser(),
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
  });

  const url = 'file://' + path.resolve(__dirname, '..', 'academy.html') + '#/python/skill/1.1.1';
  const findings = [];
  const consoleMessages = [];

  // Helper to test page
  async function auditViewport(vpName, vpConfig) {
    console.log(`\n=== Auditing Viewport: ${vpName} ===`);
    const ctx = await browser.newContext({
      viewport: { width: vpConfig.width, height: vpConfig.height },
      deviceScaleFactor: vpConfig.dpr || 1,
      isMobile: !!vpConfig.isMobile,
      hasTouch: !!vpConfig.hasTouch
    });

    const page = await ctx.newPage();
    page.on('console', msg => {
      consoleMessages.push({ vp: vpName, type: msg.type(), text: msg.text() });
    });
    page.on('pageerror', err => {
      findings.push({ severity: 'CRITICAL', text: `Page error in ${vpName}: ${err.message}` });
    });

    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);

    // 1. Check overflow
    const scrollW = await page.evaluate(() => document.documentElement.scrollWidth);
    if (scrollW > vpConfig.width) {
      findings.push({ severity: 'HIGH', text: `${vpName} has horizontal overflow: scrollWidth=${scrollW} > ${vpConfig.width}` });
    }

    // Capture Theory Initial
    await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_01_theory_init.png`) });

    // Audio bar toggle test
    const audioBtn = await page.$('[data-toggle-audio]');
    if (audioBtn) {
      await audioBtn.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_02_audio_bar.png`) });
      // close audio bar
      const audioClose = await page.$('[data-audio-close]');
      if (audioClose) await audioClose.click();
      await page.waitForTimeout(200);
    }

    // Step progression test
    console.log('Testing Theory steps...');
    const stepNextBtn = await page.$('[data-py-next-step], [data-chunk-more="py"], [data-py-start-check]');
    if (stepNextBtn) {
      await stepNextBtn.click();
      await page.waitForTimeout(400);
      await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_03_theory_step2.png`) });
    }

    // Check if comprehension check can be activated
    const checkBtn = await page.$('[data-py-start-check]');
    if (checkBtn) {
      await checkBtn.click();
      await page.waitForTimeout(400);
      await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_04_theory_check_options.png`) });

      // Click wrong answer first
      const answers = await page.$$('[data-py-step-answer]');
      if (answers.length > 1) {
        await answers[1].click();
        await page.waitForTimeout(400);
        await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_05_theory_check_wrong_bottomsheet.png`) });
      }
    }

    // Reload page to get clean state for cards
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(600);

    // 2. Cards Tab
    console.log('Testing Cards Tab...');
    const cardDot = await page.$('[data-py-select-f]');
    if (cardDot) {
      await cardDot.click();
      await page.waitForTimeout(400);
      await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_06_card_question.png`) });

      // Flip card
      const flipBtn = await page.$('[data-py-flip-card]');
      if (flipBtn) {
        await flipBtn.click();
        await page.waitForTimeout(400);
        await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_07_card_answer.png`) });

        // Check if "← Назад к предыдущей" button is present and visible
        const prevBtn = await page.$('[data-py-prev-card]');
        if (!prevBtn) {
          findings.push({ severity: 'HIGH', text: `${vpName}: [data-py-prev-card] button missing on card answer face` });
        }

        // Rate card Good
        const rateGood = await page.$('[data-py-rate-card="3"]');
        if (rateGood) {
          await rateGood.click();
          await page.waitForTimeout(400);
          await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_08_card_next.png`) });
        }
      }
    }

    // 3. Practice / Code Tab
    console.log('Testing Practice Tab...');
    const taskDot = await page.$('[data-py-select-task]');
    if (taskDot) {
      await taskDot.click();
      await page.waitForTimeout(600);
      await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_09_practice_init.png`) });

      // Test Socratic Hint (visible in spec pane)
      const hintBtn = await page.$('[data-py-task-hint]');
      if (hintBtn) {
        await hintBtn.click();
        await page.waitForTimeout(300);
        await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_10_practice_hint_expanded.png`) });
      }

      if (vpConfig.isMobile) {
        // On mobile, switch to code tab
        const codeTabBtn = await page.$('[data-py-practice-tab="code"], .practice-mobile-cta');
        if (codeTabBtn) {
          await codeTabBtn.click();
          await page.waitForTimeout(400);
          await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_11_practice_mob_code.png`) });
        }
      }

      // Test Run solution (fail state)
      const runBtn = await page.$('.btn-check-solution');
      if (runBtn) {
        await page.click('.btn-check-solution');
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_12_practice_fail.png`) });

        // Fill correct solution
        await page.evaluate(() => {
          const ed = document.getElementById('py-skill-editor');
          if (ed) {
            ed.value = 'original = [1, 2, 3, 4, 5]\nreversed_list = original[::-1]';
            ed.dispatchEvent(new Event('input', { bubbles: true }));
          }
        });
        await page.waitForTimeout(300);
        await page.click('.btn-check-solution');
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(OUT_DIR, `${vpName}_13_practice_pass.png`) });
      }
    }

    // Check DOM for technical codes, coddy mentions, etc.
    const textIssues = await page.evaluate(() => {
      const issues = [];
      const bodyText = document.body.innerText;
      if (/К-\d+/i.test(bodyText)) issues.push('Found technical note ID К-xxx in visible text');
      if (/Ф-\d+/i.test(bodyText)) issues.push('Found technical deck ID Ф-xxx in visible text');
      if (/Юнит\s*\d+\.\d+/i.test(bodyText)) issues.push('Found technical unit ID "Юнит X.Y" in visible text');
      if (/Задача\s*#\d+/i.test(bodyText)) issues.push('Found technical task ID "Задача #X" in visible text');
      if (/Coddy|Кодди/i.test(document.body.innerHTML)) issues.push('Found mention of Coddy/Кодди in DOM');
      return issues;
    });

    for (const iss of textIssues) {
      findings.push({ severity: 'HIGH', text: `${vpName}: ${iss}` });
    }

    await ctx.close();
  }

  await auditViewport('desktop', { width: 1440, height: 900 });
  await auditViewport('mobile', { width: 390, height: 844, dpr: 2, isMobile: true, hasTouch: true });

  await browser.close();

  console.log('\n================ AUDIT SUMMARY ================');
  console.log('Console errors:', consoleMessages.filter(m => m.type === 'error'));
  console.log('Findings:', findings);

  fs.writeFileSync(path.join(OUT_DIR, 'findings.json'), JSON.stringify({ consoleMessages, findings }, null, 2));
  console.log(`Report generated in ${OUT_DIR}`);
})();
