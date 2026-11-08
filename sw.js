const CACHE_NAME = 'academy-pwa-v84';
const ASSETS_TO_CACHE = [
  './',
  'index.html',
  'academy.html',
  'manifest.json',
  'icon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') {
    return;
  }

  const url = new URL(event.request.url);

  // Не перехватываем сторонние домены
  if (url.origin !== self.location.origin) {
    return;
  }

  // Не кэшируем динамические API запросы и healthz
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/healthz')) {
    return;
  }

  // Стратегия Stale-While-Revalidate для мгновенного переключения и загрузки:
  // 1. Мгновенная отдача из локального кэша (0-5 мс) без ожидания сети
  // 2. Фоновое обновление кэша из сети (revalidate) без блокировки интерфейса
  // 3. Fallback на academy.html для навигационных запросов
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Фоновое обновление из сети
      const networkFetch = fetch(event.request)
        .then((networkResponse) => {
          if (
            networkResponse &&
            networkResponse.status === 200 &&
            networkResponse.type === 'basic'
          ) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // Сеть недоступна (оффлайн)
          if (event.request.mode === 'navigate') {
            return caches.match('academy.html');
          }
        });

      // Если ресурс уже есть в кэше — отдаём его МОЛНИЕНОСНО (0 мс ожидания)
      if (cachedResponse) {
        return cachedResponse;
      }

      // Если в кэше ресурса ещё нет (первое посещение) — ждём сетевого ответа
      return networkFetch.then((networkResponse) => {
        if (networkResponse) return networkResponse;
        if (event.request.mode === 'navigate') {
          return caches.match('academy.html');
        }
        return new Response('Offline', { status: 503, statusText: 'Offline' });
      });
    })
  );
});
