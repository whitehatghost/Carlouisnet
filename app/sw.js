/* CARLOUIS · Control — service worker
   -------------------------------------------------------------------------
   Guarda la app entera en el teléfono para que abra sin internet. Eso importa
   de verdad: se usa manejando, y en varias zonas del país la señal se cae.

   Los datos del negocio NO pasan por acá: viven en localStorage. Esto solo
   cachea los archivos de la app.

   Al cambiar cualquier archivo hay que subir VERSION, si no el teléfono
   sigue mostrando la versión vieja. */

var VERSION = 'carlouis-app-v5';

var ARCHIVOS = [
  './',
  './index.html',
  './app.css',
  './app.js',
  './productos.js',
  './manifest.webmanifest',
  '../assets/fonts/fraunces-latin.woff2',
  '../assets/fonts/karla-latin.woff2',
  '../assets/img/icon-192.png',
  '../assets/img/icon-512.png',
  '../assets/img/icon-180.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(VERSION).then(function (c) {
      // addAll falla entero si un archivo falla; se agregan de a uno para que
      // una fuente que no cargue no deje la app sin cachear.
      return Promise.all(ARCHIVOS.map(function (u) {
        return c.add(u).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (llaves) {
      return Promise.all(llaves.map(function (k) {
        if (k !== VERSION) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  var url = new URL(req.url);
  if (url.origin !== location.origin) return;   // Waze, Maps y WhatsApp van directo

  // Red primero y cache de respaldo: si hay señal se ve lo último publicado,
  // y si no hay, se ve lo guardado. Para una app que se usa en la calle esto
  // es mejor que cache-primero, que dejaría al teléfono pegado en una versión
  // vieja hasta que se reinstale.
  e.respondWith(
    fetch(req).then(function (res) {
      if (res && res.status === 200 && res.type === 'basic') {
        var copia = res.clone();
        caches.open(VERSION).then(function (c) { c.put(req, copia); });
      }
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || caches.match('./index.html');
      });
    })
  );
});
