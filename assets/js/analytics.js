/* =============================================================
   CARLOUIS Gourmet — medición de conversiones

   CÓMO ACTIVARLO
   Poné abajo el ID de medición de Google Analytics (empieza con G-)
   y listo. Mientras esté vacío no se carga nada: ni script externo,
   ni cookies, ni aviso. El sitio funciona igual.

   Se obtiene en analytics.google.com → Administrar → Flujos de datos.
   ============================================================= */
(function () {
  'use strict';

  var GA_ID = '';   // <-- pegá aquí tu ID, por ejemplo 'G-XXXXXXXXXX'

  if (!GA_ID) return;

  var CONSENT_KEY = 'carlouis:analitica';

  /* ---------- Carga de Google Analytics ---------------------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  // Arranca con el consentimiento denegado: nada se envía hasta que acepten.
  gtag('consent', 'default', {
    ad_storage: 'denied',
    analytics_storage: 'denied',
    wait_for_update: 500
  });

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  gtag('js', new Date());
  gtag('config', GA_ID, { anonymize_ip: true });

  var otorgar = function () {
    gtag('consent', 'update', { analytics_storage: 'granted' });
  };

  try {
    if (localStorage.getItem(CONSENT_KEY) === 'si') otorgar();
  } catch (e) {}

  /* ---------- Aviso de cookies ------------------------------- */
  var yaDecidio = false;
  try { yaDecidio = !!localStorage.getItem(CONSENT_KEY); } catch (e) { yaDecidio = true; }

  if (!yaDecidio) {
    var aviso = document.createElement('div');
    aviso.className = 'cookie-aviso';
    aviso.setAttribute('role', 'dialog');
    aviso.setAttribute('aria-label', 'Aviso de cookies');
    aviso.innerHTML =
      '<p>Usamos cookies solo para saber qué páginas visitan y mejorar la tienda. ' +
      'No compartimos nada con terceros.</p>' +
      '<div class="cookie-aviso__btns">' +
        '<button type="button" class="btn btn--primary btn--sm" data-cookie="si">Aceptar</button>' +
        '<button type="button" class="btn btn--ghost btn--sm" data-cookie="no">Rechazar</button>' +
      '</div>';
    document.body.appendChild(aviso);

    aviso.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cookie]');
      if (!b) return;
      try { localStorage.setItem(CONSENT_KEY, b.dataset.cookie); } catch (err) {}
      if (b.dataset.cookie === 'si') otorgar();
      aviso.remove();
    });
  }

  /* ---------- Eventos que importan --------------------------- */
  // La conversión de este negocio es el mensaje de WhatsApp, no una compra
  // en línea. Eso es lo que se mide.

  var pagina = document.title.split('|')[0].trim();

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a, button');
    if (!a) return;
    var href = a.getAttribute('href') || '';

    // Agregar al pedido: solo cuál producto, sin montos
    if (a.hasAttribute('data-add')) {
      gtag('event', 'agregar_producto', { producto: a.dataset.name });
      return;
    }

    // Enviar el pedido: se cuenta cuántos se envían, no cuánto suman
    if (a.hasAttribute('data-send')) {
      var lineas = 0;
      try { lineas = JSON.parse(localStorage.getItem('carlouis:pedido') || '[]').length; } catch (err) {}
      gtag('event', 'pedido_enviado', { productos_distintos: lineas });
      return;
    }

    // Reseña en Google
    if (href.indexOf('g.page/r/') !== -1) {
      gtag('event', 'click_resena', { origen: pagina });
      return;
    }

    // Cualquier otro WhatsApp: consulta suelta
    if (href.indexOf('wa.me/') !== -1) {
      gtag('event', 'contacto_whatsapp', {
        origen: pagina,
        ubicacion: a.closest('.wa-float') ? 'flotante'
                 : a.closest('.site-header') ? 'menu'
                 : a.closest('.card') ? 'tarjeta_producto'
                 : a.closest('.cta') ? 'cta_final' : 'contenido'
      });
    }
  }, true);
})();
