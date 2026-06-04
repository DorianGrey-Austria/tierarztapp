/**
 * VetScan Pro - Service Worker
 * Caches HTML tools, JS, and 3D models for offline use.
 */
const CACHE_NAME = 'vetscan-pro-v1';
const STATIC_ASSETS = [
  '/',
  '/vetscan-version-selector.html',
  '/vetscan-3d-viewer.html',
  '/vetscan-organ-explorer.html',
  '/vetscan-pathology-scanner.html',
  '/js/vetscan-shared.js',
  '/js/vetscan-pro.js',
];

// Install: cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first for HTML, cache-first for GLB/JS/CSS
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // GLB models: cache-first (they don't change often)
  if (url.pathname.endsWith('.glb')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // HTML/JS: network-first with cache fallback
  if (url.pathname.endsWith('.html') || url.pathname.endsWith('.js')) {
    event.respondWith(
      fetch(event.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => caches.match(event.request))
    );
    return;
  }

  // Everything else: network with cache fallback
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
