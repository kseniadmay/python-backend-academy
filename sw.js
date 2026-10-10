const CACHE_NAME = 'academy-pwa-v29';
const ASSETS_TO_CACHE = [
  './',
  'index.html',
  'academy.html',
  'Практика кода — тренажёр с IDE.html',
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
  // Only handle GET requests for local assets
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  // Skip external APIs like github.com
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => {
        // Network failed (offline / PC off) - return cached
        return cachedResponse;
      });

      // Stale-while-revalidate: return cached instantly if available, else network
      return cachedResponse || fetchPromise;
    })
  );
});
