self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('sora-remote-v1').then((cache) => cache.addAll([
      '/', '/index.html', '/styles.css', '/app.js', '/manifest.webmanifest'
    ]))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith((async () => {
    try {
      const network = await fetch(event.request);
      return network;
    } catch {
      const cached = await caches.match(event.request, { ignoreSearch: true });
      return cached || Response.error();
    }
  })());
});

