#!/usr/bin/env node
/**
 * test_dom_init_smoke.js
 *
 * Smoke-тест защиты от белых/пустых экранов при загрузке Академии (Blank Screen Guard).
 * Проверяет:
 * 1. Наличие всех обязательных элементов каркаса страницы в разметке (#view-root, #nav-desktop и др.).
 * 2. Отсутствие небезопасных "голых" обращений document.getElementById('X').<prop> к отсутствующим ID.
 * 3. Полную симуляцию выполнения скриптов при старте страницы:
 *    - Запуск скриптов без ReferenceError и TypeError.
 *    - Вызов render() без сбоев.
 *    - Гарантированное наполнение корневого контейнера #view-root контентом (проверка на 0 байт/пустой экран).
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

function runDomSmokeTest(htmlRelPath) {
  const rootDir = path.resolve(__dirname, '..');
  const fullPath = path.join(rootDir, htmlRelPath);

  if (!fs.existsSync(fullPath)) {
    return true; // Файл не существует (например, при выборочном тестировании)
  }

  const html = fs.readFileSync(fullPath, 'utf8');

  // 1. Извлекаем чистую разметку без скриптов
  const markup = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');

  const staticIds = new Set();
  const idRegex = /id=["']([^"']+)["']/g;
  let m;
  while ((m = idRegex.exec(markup)) !== null) {
    staticIds.add(m[1]);
  }

  // 2. Обязательные базовые ID каркаса
  const requiredShellIds = [
    'view-root',
    'nav-desktop',
    'theme-toggle-d',
    'streak-num-d',
    'topbar-pomo-pill-el',
    'topbar-pomo-time'
  ];

  for (const rid of requiredShellIds) {
    if (!staticIds.has(rid)) {
      throw new Error(`[BLANK SCREEN GUARD] Критический элемент каркаса #${rid} отсутствует в разметке ${htmlRelPath}!`);
    }
  }

  // 3. Создаем виртуальное DOM-окружение для изолированного тестирования
  function createFakeElement(id = '', tag = 'div') {
    return {
      id: id,
      tagName: tag.toUpperCase(),
      textContent: '',
      innerHTML: '',
      value: '',
      style: {},
      children: [],
      childNodes: [],
      firstChild: null,
      lastChild: null,
      classList: {
        add: () => {},
        remove: () => {},
        toggle: () => {},
        contains: () => false
      },
      setAttribute: () => {},
      getAttribute: () => null,
      removeAttribute: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      querySelector: () => null,
      querySelectorAll: () => [],
      appendChild: (c) => c,
      removeChild: (c) => c,
      insertBefore: (c) => c,
      remove: () => {},
      focus: () => {},
      blur: () => {},
      click: () => {},
      scrollIntoView: () => {},
      getBoundingClientRect: () => ({ top: 0, left: 0, width: 100, height: 100, right: 100, bottom: 100 })
    };
  }

  const elementsById = {};
  for (const id of staticIds) {
    elementsById[id] = createFakeElement(id);
  }

  const storage = {};
  const fakeStorage = {
    getItem: (k) => storage[k] || null,
    setItem: (k, v) => { storage[k] = String(v); },
    removeItem: (k) => { delete storage[k]; },
    clear: () => {}
  };

  const fakeDoc = {
    documentElement: createFakeElement('html', 'html'),
    body: createFakeElement('body', 'body'),
    head: createFakeElement('head', 'head'),
    getElementById: (id) => {
      // Если ID нет в статической разметке — возвращает NULL (симуляция реального браузера)
      return elementsById[id] || null;
    },
    querySelector: (sel) => {
      if (sel && sel.startsWith('#')) {
        const id = sel.slice(1);
        return elementsById[id] || null;
      }
      return createFakeElement('', 'div');
    },
    querySelectorAll: () => [createFakeElement('', 'div')],
    createElement: (tag) => createFakeElement('', tag),
    addEventListener: () => {},
    removeEventListener: () => {}
  };

  const fakeWin = {
    document: fakeDoc,
    localStorage: fakeStorage,
    sessionStorage: fakeStorage,
    location: { hash: '', search: '', pathname: '/', href: 'http://localhost/' },
    navigator: { userAgent: 'Mozilla/5.0 Node.js' },
    addEventListener: () => {},
    removeEventListener: () => {},
    scrollTo: () => {},
    innerWidth: 1024,
    innerHeight: 768,
    setTimeout: (fn) => setTimeout(fn, 0),
    clearTimeout: () => {},
    setInterval: () => 1,
    clearInterval: () => {},
    console: { log: () => {}, warn: () => {}, error: () => {} },
    requestAnimationFrame: (cb) => { cb(); return 1; },
    cancelAnimationFrame: () => {}
  };

  fakeWin.window = fakeWin;
  fakeWin.global = fakeWin;
  fakeDoc.defaultView = fakeWin;

  // Извлекаем код всех внутренних скриптов страницы
  const scriptRegex = /<script(?:\s+([^>]*))?>([\s\S]*?)<\/script>/gi;
  let allScripts = '';
  while ((m = scriptRegex.exec(html)) !== null) {
    const attrs = m[1] || '';
    if (attrs.includes('src=')) continue; // Пропускаем внешние CDN скрипты
    allScripts += '\n' + m[2];
  }

  const context = vm.createContext(fakeWin);

  try {
    vm.runInContext(allScripts, context, { timeout: 3500 });
  } catch (err) {
    throw new Error(`[RUNTIME INITIALIZATION ERROR] Ошибка при старте скриптов ${htmlRelPath}:\n${err.stack}`);
  }

  // 4. Проверяем вызов первичного рендера render()
  if (typeof context.render === 'function') {
    try {
      context.render();
    } catch (err) {
      throw new Error(`[RENDER SMOKE ERROR] Функция render() в ${htmlRelPath} упала с ошибкой:\n${err.stack}`);
    }
  }

  // 5. Проверяем, что #view-root наполнен контентом и не остался пустым
  const vr = elementsById['view-root'];
  if (vr && !vr.innerHTML && !vr.textContent) {
    throw new Error(`[BLANK SCREEN ERROR] После render() контейнер #view-root остался абсолютно пустым в ${htmlRelPath}!`);
  }

  return true;
}

try {
  runDomSmokeTest('academy.html');
  runDomSmokeTest('standards/standards.html');
  console.log('✓ [Pre-Commit] Тест инициализации DOM и защиты от пустых экранов пройден со 100% успехом.');
  process.exit(0);
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
