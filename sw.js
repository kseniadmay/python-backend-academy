const CACHE_NAME = 'academy-pwa-v98';
const ASSETS_TO_CACHE = [
  './',
  'index.html',
  'academy.html',
  'manifest.json',
  'icon.svg'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
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

  // Network-First для главного HTML-документа, чтобы обновления кода применялись немедленно
  if (event.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname.endsWith('/')) {
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) return cachedResponse;
            return caches.match('academy.html');
          });
        })
    );
    return;
  }

  // Stale-While-Revalidate для статичных ресурсов (иконки, манифест)
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
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
        .catch(() => {});

      if (cachedResponse) {
        return cachedResponse;
      }

      return networkFetch.then((networkResponse) => {
        if (networkResponse) return networkResponse;
        return new Response('Offline', { status: 503, statusText: 'Offline' });
      });
    })
  );
});
