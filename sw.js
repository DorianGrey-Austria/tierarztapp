/**
 * VetScan Pro - Service Worker (v2)
 * Precaches the app shell (all 19 learning tools, shared JS, manifest, icons,
 * offline fallback) and caches 3D models on demand for offline use.
 *
 * Strategy:
 *   - HTML/JS: network-first, fall back to cache, then offline.html
 *   - GLB models: cache-first (stable, large assets)
 *   - icons/manifest/other: cache-first with network refresh
 */
const CACHE_NAME = 'vetscan-pro-v2';

// App shell - precached on install so the whole tool suite works offline.
const PRECACHE = [
  'vetscan-version-selector.html',
  'offline.html',
  'manifest.json',
  'js/vetscan-shared.js',
  'js/vetscan-pro.js',
  // 19 registered professional learning tools
  'vetscan-clinical-exam.html',
  'vetscan-ddx-trainer.html',
  'vetscan-lab-interpreter.html',
  'vetscan-emergency-triage.html',
  'vetscan-pharma-calc.html',
  'vetscan-auscultation.html',
  'vetscan-radiology.html',
  'vetscan-surgical-approaches.html',
  'vetscan-pathology-cases.html',
  'vetscan-anatomy-layers.html',
  'vetscan-quick-reference.html',
  'vetscan-glossary.html',
  'vetscan-3d-viewer.html',
  'vetscan-organ-explorer.html',
  'vetscan-animated-showcase.html',
  'vetscan-pathology-scanner.html',
  'vetscan-parasite-atlas.html',
  'vetscan-bone-atlas.html',
  'vetscan-dashboard.html',
  // icons
  'assets/icons/favicon.svg',
  'assets/icons/favicon-32.png',
  'assets/icons/apple-touch-icon.png',
  'assets/icons/icon-192.png',
  'assets/icons/icon-512.png',
  'assets/icons/icon-maskable-512.png',
];

// Install: precache the app shell. Individual failures must not abort install.
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      Promise.all(PRECACHE.map(url =>
        cache.add(url).catch(() => { /* skip missing asset, keep install alive */ })
      ))
    )
  );
  self.skipWaiting();
});

// Activate: drop old cache versions.
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  // GLB models: cache-first (they don't change often).
  if (url.pathname.endsWith('.glb')) {
    event.respondWith(
      caches.match(request).then(cached => cached || fetch(request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      }))
    );
    return;
  }

  // HTML navigations / JS: network-first, cache fallback, then offline page.
  const isHTML = request.mode === 'navigate' || url.pathname.endsWith('.html');
  if (isHTML || url.pathname.endsWith('.js')) {
    event.respondWith(
      fetch(request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      }).catch(() =>
        caches.match(request).then(cached =>
          cached || (isHTML ? caches.match('offline.html') : undefined)
        )
      )
    );
    return;
  }

  // Everything else (icons, css, json): cache-first with network refresh.
  event.respondWith(
    caches.match(request).then(cached => cached || fetch(request).then(response => {
      if (response.ok && response.type === 'basic') {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
      }
      return response;
    }).catch(() => cached))
  );
});
