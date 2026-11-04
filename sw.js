const CACHE_NAME = 'academy-pwa-v72';
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

  // Не кэшируем API запросы и healthz
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/healthz')) {
    return;
  }

  // Network-First с быстрым адаптивным таймаутом (1200ms) для мобильных сетей
  event.respondWith(
    new Promise((resolve) => {
      let isSettled = false;

      const timer = setTimeout(() => {
        caches.match(event.request).then((cached) => {
          if (cached && !isSettled) {
            isSettled = true;
            resolve(cached);
          } else if (event.request.mode === 'navigate' && !isSettled) {
            caches.match('academy.html').then((acadCached) => {
              if (acadCached && !isSettled) {
                isSettled = true;
                resolve(acadCached);
              }
            });
          }
        });
      }, 1200);

      fetch(event.request)
        .then((networkResponse) => {
          clearTimeout(timer);
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
          if (!isSettled) {
            isSettled = true;
            resolve(networkResponse);
          }
        })
        .catch(() => {
          clearTimeout(timer);
          if (!isSettled) {
            isSettled = true;
            caches.match(event.request).then((cachedResponse) => {
              if (cachedResponse) {
                return resolve(cachedResponse);
              }
              if (event.request.mode === 'navigate') {
                return resolve(caches.match('academy.html'));
              }
              resolve(new Response('Offline', { status: 503, statusText: 'Offline' }));
            });
          }
        });
    })
  );
});
