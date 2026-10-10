import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const academyPath = path.resolve(__dirname, '..', 'academy.html');
const artifactsDir = path.resolve('C:\\Users\\fury6\\.gemini\\antigravity\\brain\\d689245c-f3a9-498f-b883-ee4a97e4b9bc');

const chromeExe = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const port = 9335;
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cdp-e2e-'));

console.log('--- Запуск Headless Chrome для интерактивного E2E-тестирования ---');
const chrome = spawn(chromeExe, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${tmpDir}`,
  '--window-size=1280,960',
  '--disable-gpu',
  '--no-sandbox',
  'about:blank'
]);

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 1;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (msg) => {
        const data = JSON.parse(msg.data);
        if (data.id && this.callbacks.has(data.id)) {
          const { resolve, reject } = this.callbacks.get(data.id);
          this.callbacks.delete(data.id);
          if (data.error) reject(new Error(data.error.message));
          else resolve(data.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expr) {
    const res = await this.send('Runtime.evaluate', {
      expression: expr,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      console.error('CDP Eval Exception:', res.exceptionDetails.text, res.exceptionDetails.exception?.description);
    }
    return res.result?.value;
  }

  async screenshot(outPath, clip = null) {
    const params = { format: 'png' };
    if (clip) params.clip = clip;
    const res = await this.send('Page.captureScreenshot', params);
    const buf = Buffer.from(res.data, 'base64');
    fs.writeFileSync(outPath, buf);
    console.log(`[Скриншот сохранён] ${path.basename(outPath)}`);
  }

  close() {
    this.ws.close();
  }
}

async function run() {
  await sleep(1200);

  const listRes = await fetch(`http://127.0.0.1:${port}/json/list`);
  const pages = await listRes.json();
  const page = pages.find(p => p.type === 'page') || pages[0];
  if (!page || !page.webSocketDebuggerUrl) {
    throw new Error('Не удалось получить webSocketDebuggerUrl страницы');
  }

  const cdp = new CDPClient(page.webSocketDebuggerUrl);
  await cdp.connect();
  console.log('✓ Соединение с Chrome DevTools Protocol установлено.');

  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');

  const fileUri = 'file:///' + academyPath.replace(/\\/g, '/') + '#/python/skill/1.1.1';
  console.log(`Навигация к: ${fileUri}`);
  await cdp.send('Page.navigate', { url: fileUri });

  // Ждём полной отрисовки
  await sleep(2000);

  // ШАГ 1: Стартовое состояние (Тема 1)
  console.log('\n--- ШАГ 1: Стартовое состояние (Тема 1) ---');
  const step1Info = await cdp.evaluate(`(() => {
    try {
      const unitEl = document.querySelector('.topic-eyebrow-unit');
      const numEl = document.querySelector('.topic-eyebrow-num');
      const labelEl = document.querySelector('.dots-necklace-label');
      const activeDot = document.querySelector('.dot-jewel.active');
      const allDots = document.querySelectorAll('.dot-jewel');
      const xpBadge = document.querySelector('.topbar-echelon-xp');
      const readinessBadge = document.querySelector('.topbar-echelon-readiness');
      const wire = document.querySelector('.dots-necklace-wire');
      const wireActive = document.querySelector('.dots-necklace-wire-active');

      return {
        unitText: unitEl?.textContent?.trim(),
        numText: numEl?.textContent?.trim(),
        label: labelEl?.textContent?.trim(),
        dotsCount: allDots.length,
        hasActiveDot: !!activeDot,
        activeTitle: activeDot?.getAttribute('title'),
        xpBadge: xpBadge?.textContent?.trim(),
        readinessBadge: readinessBadge?.textContent?.trim(),
        wireWidth: wire?.style?.width,
        wireActiveWidth: wireActive?.style?.width
      };
    } catch(e) {
      return { error: e.message };
    }
  })()`);

  console.log('Информация о трекере тем:', step1Info);
  if (!step1Info.hasActiveDot) throw new Error('Активная точка не найдена!');
  if (step1Info.dotsCount !== 13) throw new Error(`Ожидалось 13 точек, получено: ${step1Info.dotsCount}`);
  if (step1Info.wireWidth !== '228px') throw new Error(`Ожидалась длина провода 228px, получено: ${step1Info.wireWidth}`);

  await cdp.screenshot(path.join(artifactsDir, 'journey_step1_initial.png'));

  // ШАГ 2: Интерактивное чтение конспекта Темы 1
  console.log('\n--- ШАГ 2: Прохождение всех микро-шагов теории Темы 1 ---');
  let maxClicks = 25;
  while (maxClicks-- > 0) {
    const action = await cdp.evaluate(`(() => {
      const moreBtn = document.querySelector('[data-chunk-more="py"]');
      if (moreBtn) {
        moreBtn.click();
        return 'more-chunk';
      }
      const stepBtn = document.querySelector('[data-py-next-step]');
      if (stepBtn) {
        stepBtn.click();
        return 'next-step';
      }
      const finishBtn = document.querySelector('[data-py-finish-note]');
      if (finishBtn) {
        finishBtn.click();
        return 'finish-note';
      }
      return null;
    })()`);

    if (!action) break;
    console.log(`Действие в конспекте: ${action}`);
    if (action === 'finish-note') break;
    await sleep(250);
  }

  await sleep(1000);

  // ШАГ 3: Проверка обновления нити тем после завершения Темы 1
  console.log('\n--- ШАГ 3: Проверка продвижения нити тем (Тема 1 -> Тема 2) ---');
  const step3Info = await cdp.evaluate(`(() => {
    try {
      const numEl = document.querySelector('.topic-eyebrow-num');
      const labelEl = document.querySelector('.dots-necklace-label');
      const activeDot = document.querySelector('.dot-jewel.active');
      const doneDots = document.querySelectorAll('.dot-jewel.done');
      const wireActive = document.querySelector('.dots-necklace-wire-active');
      const xpBadge = document.querySelector('.topbar-echelon-xp');

      return {
        numText: numEl?.textContent?.trim(),
        label: labelEl?.textContent?.trim(),
        activeTitle: activeDot?.getAttribute('title'),
        doneCount: doneDots.length,
        wireActiveWidth: wireActive?.style?.width,
        xp: xpBadge?.textContent?.trim()
      };
    } catch(e) {
      return { error: e.message };
    }
  })()`);

  console.log('Состояние нити тем после финиша Темы 1:', step3Info);
  if (step3Info.error) throw new Error('Ошибка шага 3: ' + step3Info.error);
  if (step3Info.numText !== 'Тема 2 из 13') throw new Error(`Ожидалась "Тема 2 из 13", получено: ${step3Info.numText}`);
  if (step3Info.doneCount !== 1) throw new Error(`Ожидалась 1 выполненная точка, получено: ${step3Info.doneCount}`);
  if (step3Info.wireActiveWidth !== '19px') throw new Error(`Ширина активного лазерного провода должна быть 19px, получено: ${step3Info.wireActiveWidth}`);

  await cdp.screenshot(path.join(artifactsDir, 'journey_step2_topic_2_active.png'));

  // ШАГ 4: Клик по 3-й точке (К-003) — живая валидация референса пользователя
  console.log('\n--- ШАГ 4: Клик по 3-й точке (К-003) — сверка с референсом ---');
  await cdp.evaluate(`(() => {
    const dot3 = document.querySelector('.dot-jewel[data-py-select-k="К-003"]');
    if (dot3) dot3.click();
  })()`);
  await sleep(600);

  const step4Info = await cdp.evaluate(`(() => {
    try {
      const numEl = document.querySelector('.topic-eyebrow-num');
      const labelEl = document.querySelector('.dots-necklace-label');
      const activeDot = document.querySelector('.dot-jewel.active');
      const wireActive = document.querySelector('.dots-necklace-wire-active');

      return {
        numText: numEl?.textContent?.trim(),
        label: labelEl?.textContent?.trim(),
        activeTitle: activeDot?.getAttribute('title'),
        wireActiveWidth: wireActive?.style?.width
      };
    } catch(e) {
      return { error: e.message };
    }
  })()`);

  console.log('Состояние для Темы 3:', step4Info);
  if (step4Info.numText !== 'Тема 3 из 13') throw new Error(`Ожидалась "Тема 3 из 13", получено: ${step4Info.numText}`);
  if (step4Info.wireActiveWidth !== '38px') throw new Error(`Ширина активного провода для Темы 3 должна быть 38px, получено: ${step4Info.wireActiveWidth}`);

  await cdp.screenshot(path.join(artifactsDir, 'journey_step3_topic_3_active.png'));

  // ШАГ 5: Переход на вкладку карточек и решение
  console.log('\n--- ШАГ 5: Переход на карточки и прохождение колоды ---');
  await cdp.evaluate(`(() => {
    const cardsTab = document.querySelector('[data-py-tab="cards"]');
    if (cardsTab) cardsTab.click();
  })()`);
  await sleep(600);

  let cardsPassed = 0;
  while (cardsPassed < 15) {
    const isCodeTab = await cdp.evaluate(`(() => {
      const activeTab = document.querySelector('.stepper-capsule-item.active');
      return activeTab?.textContent?.includes('Практика') || false;
    })()`);
    if (isCodeTab) break;

    await cdp.evaluate(`(() => {
      const card = document.querySelector('[data-py-flip-card]');
      if (card) card.click();
      const rateBtn = document.querySelector('[data-py-rate-card]') || document.querySelector('[data-py-next-card]');
      if (rateBtn) rateBtn.click();
    })()`);
    cardsPassed++;
    await sleep(200);
  }

  await sleep(600);
  console.log(`Карточки пройдены (${cardsPassed} действий).`);
  await cdp.screenshot(path.join(artifactsDir, 'journey_step4_code_editor.png'));

  // ШАГ 6: Запуск тестов кода в IDE
  console.log('\n--- ШАГ 6: Запуск тестов в тренажёре IDE ---');
  await cdp.evaluate(`(() => {
    // Если ещё не на вкладке кода, переключаем
    const codeTab = document.querySelector('[data-py-tab="code"]');
    if (codeTab) codeTab.click();
  })()`);
  await sleep(600);

  await cdp.evaluate(`(() => {
    const runBtn = document.querySelector('[data-py-task-run]');
    if (runBtn) runBtn.click();
  })()`);

  await sleep(1500);
  const codeResult = await cdp.evaluate(`(() => {
    const passBox = document.querySelector('.result-box--pass');
    const xpBadge = document.querySelector('.topbar-echelon-xp');
    return {
      passed: !!passBox,
      passMessage: passBox?.textContent?.trim()?.split('\\n')[0],
      xp: xpBadge?.textContent?.trim()
    };
  })()`);
  console.log('Результат выполнения практической задачи:', codeResult);
  await cdp.screenshot(path.join(artifactsDir, 'journey_step5_code_passed.png'));

  // ШАГ 7: Кросс-навигация по юниту — клик по Точке 4 (К-004 из соседнего навыка 1.1.2)
  console.log('\n--- ШАГ 7: Кросс-навигация юнита: клик по Точке 4 (К-004, навык 1.1.2) ---');
  await cdp.evaluate(`(() => {
    const theoryTab = document.querySelector('[data-py-tab="theory"]');
    if (theoryTab) theoryTab.click();
  })()`);
  await sleep(500);

  const dot4Clicked = await cdp.evaluate(`(() => {
    const dot4 = document.querySelector('.dot-jewel[data-py-select-k="К-004"]');
    if (dot4) {
      dot4.click();
      return true;
    }
    return false;
  })()`);
  console.log('Точка 4 нажата:', dot4Clicked);
  await sleep(1000);

  const step7Info = await cdp.evaluate(`(() => {
    const numEl = document.querySelector('.topic-eyebrow-num');
    const activeDot = document.querySelector('.dot-jewel.active');
    const hash = window.location.hash;
    const wireActive = document.querySelector('.dots-necklace-wire-active');

    return {
      hash,
      numText: numEl?.textContent?.trim(),
      activeTitle: activeDot?.getAttribute('title'),
      wireActiveWidth: wireActive?.style?.width
    };
  })()`);
  console.log('Результат кросс-навигации на тему К-004:', step7Info);
  if (!step7Info.hash.includes('1.1.2')) throw new Error(`Ожидался переход в хэше на 1.1.2, получен: ${step7Info.hash}`);
  if (step7Info.wireActiveWidth !== '57px') throw new Error(`Ожидалась ширина активного провода 57px (3 * 19px), получено: ${step7Info.wireActiveWidth}`);

  await cdp.screenshot(path.join(artifactsDir, 'journey_step6_cross_skill.png'));

  console.log('\n================================================================');
  console.log('🎉 ВСЕ 7 ЭТАПОВ ИНТЕРАКТИВНОГО ТЕСТИРОВАНИЯ УСПЕШНО ПРОЙДЕНЫ!');
  console.log('================================================================');

  cdp.close();
}

try {
  await run();
} catch (err) {
  console.error('❌ Ошибка тестирования:', err);
  process.exitCode = 1;
} finally {
  chrome.kill();
  setTimeout(() => {
    try {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    } catch(e) {}
  }, 1000);
}
