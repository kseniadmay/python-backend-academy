/**
 * test_pwa_offline.js
 * 
 * Автоматизированный E2E-тест оффлайн-режима PWA, манифеста и Service Worker
 * для платформы Python Backend Academy.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const ROOT = path.join(__dirname, '..');

console.log('=== [PWA] Запуск верификации Progressive Web App и оффлайн-контура ===');

// 1. Проверка манифеста manifest.json
const manifestPath = path.join(ROOT, 'manifest.json');
assert(fs.existsSync(manifestPath), 'Файл manifest.json должен существовать в корне проекта');
const manifestRaw = fs.readFileSync(manifestPath, 'utf-8');
let manifest;
try {
  manifest = JSON.parse(manifestRaw);
} catch (e) {
  assert.fail(`Синтаксическая ошибка в manifest.json: ${e.message}`);
}

assert(manifest.name && manifest.name.includes('Python Backend Academy'), 'manifest.json: поле name должно содержать название платформы');
assert(manifest.short_name, 'manifest.json: поле short_name обязательно для установки PWA');
assert(manifest.start_url, 'manifest.json: поле start_url обязательно');
assert(manifest.display === 'standalone', `manifest.json: display должен быть "standalone", получено: ${manifest.display}`);
assert(manifest.theme_color, 'manifest.json: поле theme_color обязательно');
assert(manifest.background_color, 'manifest.json: поле background_color обязательно');
assert(Array.isArray(manifest.icons) && manifest.icons.length > 0, 'manifest.json: должен содержать массив icons');

manifest.icons.forEach((icon, idx) => {
  assert(icon.src, `manifest.json: icon[${idx}] должен содержать src`);
  assert(icon.sizes, `manifest.json: icon[${idx}] должен содержать sizes`);
  const iconPath = path.join(ROOT, icon.src);
  assert(fs.existsSync(iconPath), `manifest.json: файл иконки icon[${idx}].src ('${icon.src}') не найден на диске`);
});
console.log('✓ 1. manifest.json полностью валиден (standalone, metadata, иконки на диске)');

// 2. Проверка sw.js (синтаксис и кэшируемые ассеты)
const swPath = path.join(ROOT, 'sw.js');
assert(fs.existsSync(swPath), 'Файл sw.js должен существовать в корне проекта');
const swContent = fs.readFileSync(swPath, 'utf-8');

assert(swContent.includes('CACHE_NAME'), 'sw.js: должен определять CACHE_NAME');
assert(swContent.includes('ASSETS_TO_CACHE'), 'sw.js: должен определять список ASSETS_TO_CACHE');
assert(swContent.includes('self.addEventListener(\'install\''), 'sw.js: должен содержать обработчик install');
assert(swContent.includes('self.addEventListener(\'activate\''), 'sw.js: должен содержать обработчик activate');
assert(swContent.includes('self.addEventListener(\'fetch\''), 'sw.js: должен содержать обработчик fetch');

// Извлечение списка ассетов из sw.js
const assetsMatch = swContent.match(/const\s+ASSETS_TO_CACHE\s*=\s*\[([\s\S]*?)\];/);
assert(assetsMatch, 'sw.js: не удалось распарсить массив ASSETS_TO_CACHE');
const assetTokens = assetsMatch[1]
  .split(',')
  .map(s => s.trim().replace(/^['"]|['"]$/g, ''))
  .filter(Boolean);

assert(assetTokens.length >= 4, `Ожидалось >= 4 кэшируемых ассетов, найдено: ${assetTokens.length}`);

assetTokens.forEach(asset => {
  if (asset === './') return; // корень
  const diskPath = path.join(ROOT, asset);
  assert(fs.existsSync(diskPath), `Кэшируемый в sw.js ассет '${asset}' отсутствует на диске: ${diskPath}`);
});
console.log(`✓ 2. sw.js содержит валидный список из ${assetTokens.length} ассетов, все файлы проверены на диске`);

// 3. Проверка интеграции PWA в HTML (academy.html и index.html)
['academy.html', 'index.html'].forEach(htmlFile => {
  const filePath = path.join(ROOT, htmlFile);
  assert(fs.existsSync(filePath), `Файл ${htmlFile} должен существовать`);
  const content = fs.readFileSync(filePath, 'utf-8');
  assert(content.includes('rel="manifest"'), `${htmlFile} должен содержать <link rel="manifest">`);
  assert(content.includes('name="theme-color"'), `${htmlFile} должен содержать <meta name="theme-color">`);
  assert(content.includes('navigator.serviceWorker.register'), `${htmlFile} должен регистрировать sw.js`);
});
console.log('✓ 3. academy.html и index.html содержат корректные метатеги и регистрацию Service Worker');

// 4. Полноценная эмуляция жизненного цикла Service Worker и оффлайн-фоллбэка
const mockCacheStorage = new Map();
class MockCache {
  constructor(name) {
    this.name = name;
    this.store = new Map();
  }
  async addAll(urls) {
    for (const u of urls) {
      this.store.set(u, { status: 200, url: u, body: `mock-body-for-${u}` });
    }
  }
  async match(req) {
    const rawKey = typeof req === 'string' ? req : (req.url || '');
    let decodedKey = rawKey;
    try { decodedKey = decodeURI(rawKey); } catch (e) {}
    for (const [k, v] of this.store.entries()) {
      if (k === rawKey || rawKey.endsWith('/' + k) || (k === './' && rawKey.endsWith('/')) ||
          k === decodedKey || decodedKey.endsWith('/' + k) ||
          encodeURI(k) === rawKey || rawKey.endsWith('/' + encodeURI(k))) {
        return v;
      }
    }
    return null;
  }
  async put(req, resp) {
    const key = typeof req === 'string' ? req : (req.url || '');
    this.store.set(key, resp);
  }
}

const mockCaches = {
  open: async (name) => {
    if (!mockCacheStorage.has(name)) {
      mockCacheStorage.set(name, new MockCache(name));
    }
    return mockCacheStorage.get(name);
  },
  match: async (req) => {
    for (const c of mockCacheStorage.values()) {
      const match = await c.match(req);
      if (match) return match;
    }
    return null;
  },
  keys: async () => Array.from(mockCacheStorage.keys()),
  delete: async (name) => mockCacheStorage.delete(name)
};

const swEvents = {};
let claimedClients = false;
let skippedWaiting = false;

const mockSelf = {
  location: { origin: 'https://pwa-offline-test.local' },
  addEventListener: (name, fn) => {
    swEvents[name] = fn;
  },
  skipWaiting: async () => { skippedWaiting = true; },
  clients: {
    claim: async () => { claimedClients = true; }
  }
};

// Запуск кода sw.js в контексте mockServiceWorker
const vm = require('vm');
const swContext = {
  self: mockSelf,
  caches: mockCaches,
  URL: URL,
  decodeURI: decodeURI,
  encodeURI: encodeURI,
  console: console,
  setTimeout: setTimeout
};
vm.createContext(swContext);
vm.runInContext(swContent, swContext);

const activeCacheMatch = swContent.match(/CACHE_NAME\s*=\s*['"]([^'"]+)['"]/);
assert(activeCacheMatch, 'sw.js: не удалось определить CACHE_NAME');
const ACTIVE_CACHE_NAME = activeCacheMatch[1];

(async () => {
  // 4.1. Проверка install
  assert(typeof swEvents['install'] === 'function', 'sw.js должен зарегистрировать install');
  let installPromise = null;
  swEvents['install']({
    waitUntil: (p) => { installPromise = p; }
  });
  await installPromise;
  assert(skippedWaiting, 'Install должен вызывать self.skipWaiting()');
  const cacheActive = mockCacheStorage.get(ACTIVE_CACHE_NAME);
  assert(cacheActive, `Кэш ${ACTIVE_CACHE_NAME} должен быть создан при установке`);
  assert(cacheActive.store.size >= 5, `В кэш должно быть записано >= 5 ассетов, записано: ${cacheActive.store.size}`);
  console.log(`✓ 4.1. Install событие отработало: кэш ${ACTIVE_CACHE_NAME} инициализирован, skipWaiting() выполнен`);

  // 4.2. Проверка activate и ротации старых кэшей
  const obsoleteCacheName = 'academy-pwa-v1-obsolete';
  mockCacheStorage.set(obsoleteCacheName, new MockCache(obsoleteCacheName));
  assert(mockCacheStorage.has(obsoleteCacheName), 'Предусловие: старый кэш присутствует');
  let activatePromise = null;
  swEvents['activate']({
    waitUntil: (p) => { activatePromise = p; }
  });
  await activatePromise;
  assert(!mockCacheStorage.has(obsoleteCacheName), 'Activate должен удалять устаревшие версии кэша');
  assert(mockCacheStorage.has(ACTIVE_CACHE_NAME), `Актуальный кэш ${ACTIVE_CACHE_NAME} должен быть сохранён`);
  assert(claimedClients, 'Activate должен вызывать self.clients.claim()');
  console.log('✓ 4.2. Activate событие отработало: устаревшие кэши очищены, clients.claim() вызван');

  // 4.3. Проверка fetch в оффлайн-режиме (Network Failure -> Cache Fallback)
  assert(typeof swEvents['fetch'] === 'function', 'sw.js должен зарегистрировать fetch');
  
  // Симуляция оффлайна: глобальный fetch выбрасывает сетевую ошибку
  swContext.fetch = async () => {
    throw new TypeError('Failed to fetch (offline: device in airplane mode)');
  };

  async function testFetchOffline(requestUrl) {
    let respondWithPromise = null;
    const mockEvent = {
      request: {
        method: 'GET',
        url: requestUrl
      },
      respondWith: (p) => { respondWithPromise = p; }
    };
    swEvents['fetch'](mockEvent);
    assert(respondWithPromise, `fetch event для ${requestUrl} должен вызвать event.respondWith`);
    const resp = await respondWithPromise;
    assert(resp && resp.status === 200, `Оффлайн-запрос к ${requestUrl} должен вернуть 200 из кэша`);
    return resp;
  }

  const offRoot = await testFetchOffline('https://pwa-offline-test.local/');
  assert(offRoot.url === './' || offRoot.url.includes('/'), 'Оффлайн-запрос корня вернул кэш');

  const offAcademy = await testFetchOffline('https://pwa-offline-test.local/academy.html');
  assert(offAcademy.url.includes('academy.html'), 'Оффлайн-запрос academy.html вернул кэш');

  const offIdeTrainer = await testFetchOffline('https://pwa-offline-test.local/' + encodeURI('Практика кода — тренажёр с IDE.html'));
  assert(offIdeTrainer.url.includes('Практика кода') || decodeURI(offIdeTrainer.url).includes('Практика кода'), 'Оффлайн-запрос тренажёра с IDE вернул кэш');

  const offManifest = await testFetchOffline('https://pwa-offline-test.local/manifest.json');
  assert(offManifest.url.includes('manifest.json'), 'Оффлайн-запрос manifest.json вернул кэш');

  const offIcon = await testFetchOffline('https://pwa-offline-test.local/icon.svg');
  assert(offIcon.url.includes('icon.svg'), 'Оффлайн-запрос icon.svg вернул кэш');

  console.log('✓ 4.3. Оффлайн-режим (авиарежим) полностью подтверждён: все ключевые ассеты (включая тренажёр IDE) отдаются из кэша Service Worker при сбое сети!');

  // 4.4. Проверка фильтрации: POST и сторонние домены не перехватываются
  let postIntercepted = false;
  swEvents['fetch']({
    request: { method: 'POST', url: 'https://pwa-offline-test.local/api/sync' },
    respondWith: () => { postIntercepted = true; }
  });
  assert(!postIntercepted, 'POST-запросы не должны перехватываться сервис-воркером');

  let externalIntercepted = false;
  swEvents['fetch']({
    request: { method: 'GET', url: 'https://cdn.example.com/lib.js' },
    respondWith: () => { externalIntercepted = true; }
  });
  assert(!externalIntercepted, 'Внешние URL (cross-origin) не должны перехватываться локальным сервис-воркером');
  console.log('✓ 4.4. Фильтрация методов и cross-origin доменов работает корректно');

  console.log('\n========================================================');
  console.log('  [PASS] ВСЕ ТЕСТЫ PWA И ОФФЛАЙН-КОНТУРА УСПЕШНО ПРОЙДЕНЫ!');
  console.log('========================================================\n');
})();
