/* =============================================================
   CARLOUIS Gourmet — interacciones
   Archivo externo: la CSP del sitio es script-src 'self'.
   Todo es progresivo: sin JS la página sigue siendo usable.
   ============================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.remove('no-js');

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- Header pegajoso ------------------------------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Navegación móvil ------------------------------ */
  var toggle = document.querySelector('.nav__toggle');
  var menu = document.getElementById('nav-menu');

  if (toggle && menu) {
    var setMenu = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };

    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });

    // Cerrar con Escape y devolver el foco al botón
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });

    // Cerrar al tocar fuera del menú
    document.addEventListener('click', function (e) {
      if (toggle.getAttribute('aria-expanded') !== 'true') return;
      if (!menu.contains(e.target) && !toggle.contains(e.target)) setMenu(false);
    });

    // Cerrar al navegar o al volver a escritorio
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (m) {
      if (m.matches) setMenu(false);
    });
  }

  /* ---------- Reveal al hacer scroll ------------------------ */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (revealables.length) {
    if (reduceMotion.matches || !('IntersectionObserver' in window)) {
      revealables.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          // Escalona los hijos de un mismo contenedor para dar sensación de oleada
          var siblings = Array.prototype.filter.call(
            el.parentElement ? el.parentElement.children : [],
            function (n) { return n.hasAttribute && n.hasAttribute('data-reveal'); }
          );
          var index = siblings.indexOf(el);
          el.style.setProperty('--reveal-delay', Math.min(index, 6) * 70 + 'ms');
          el.classList.add('is-visible');
          observer.unobserve(el);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

      revealables.forEach(function (el) { observer.observe(el); });
    }
  }

  /* ---------- Carrusel -------------------------------------- */
  document.querySelectorAll('[data-carousel]').forEach(function (carousel) {
    var viewport = carousel.querySelector('.carousel__viewport');
    var slides = Array.prototype.slice.call(carousel.querySelectorAll('.carousel__slide'));
    var prev = carousel.querySelector('[data-carousel-prev]');
    var next = carousel.querySelector('[data-carousel-next]');
    var dotsWrap = carousel.querySelector('.carousel__dots');
    if (!viewport || slides.length < 2) return;

    var current = 0;
    var dots = [];

    // Pinta puntos y flechas según el índice. Se llama al hacer clic y también
    // al desplazar a mano: si dependiera solo del evento de scroll, los
    // controles se quedarían desfasados hasta que el navegador lo emitiera.
    var paint = function (i) {
      dots.forEach(function (d, n) { d.setAttribute('aria-current', String(n === i)); });
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === slides.length - 1;
    };

    var goTo = function (i) {
      current = Math.max(0, Math.min(i, slides.length - 1));
      viewport.scrollTo({
        left: slides[current].offsetLeft - viewport.offsetLeft,
        behavior: reduceMotion.matches ? 'auto' : 'smooth'
      });
      paint(current);
    };

    // Puntos de navegación
    var dots = [];
    if (dotsWrap) {
      slides.forEach(function (slide, i) {
        var li = document.createElement('li');
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'carousel__dot';
        b.setAttribute('aria-label', 'Ir al producto ' + (i + 1) + ' de ' + slides.length);
        b.addEventListener('click', function () { goTo(i); });
        li.appendChild(b);
        dotsWrap.appendChild(li);
        dots.push(b);
      });
    }

    var sync = function () {
      var mid = viewport.scrollLeft + viewport.clientWidth / 2;
      var best = 0, bestDist = Infinity;
      slides.forEach(function (slide, i) {
        var center = slide.offsetLeft - viewport.offsetLeft + slide.offsetWidth / 2;
        var dist = Math.abs(center - mid);
        if (dist < bestDist) { bestDist = dist; best = i; }
      });
      current = best;
      dots.forEach(function (d, i) {
        d.setAttribute('aria-current', String(i === best));
      });
      if (prev) prev.disabled = best === 0;
      if (next) next.disabled = best === slides.length - 1;
    };

    var raf;
    viewport.addEventListener('scroll', function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(sync);
    }, { passive: true });

    if (prev) prev.addEventListener('click', function () { goTo(current - 1); });
    if (next) next.addEventListener('click', function () { goTo(current + 1); });

    // Navegación por teclado
    viewport.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
    });

    sync();
  });

  /* ---------- Filtros del catálogo -------------------------- */
  var filterBar = document.querySelector('[data-filters]');
  if (filterBar) {
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-category]'));
    var counter = document.querySelector('[data-filter-count]');

    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('.filter');
      if (!btn) return;

      filterBar.querySelectorAll('.filter').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });

      var want = btn.dataset.filter;
      var shown = 0;
      items.forEach(function (item) {
        var match = want === 'todos' || item.dataset.category.split(' ').indexOf(want) !== -1;
        item.hidden = !match;
        if (match) shown++;
      });

      if (counter) {
        counter.textContent = shown === items.length
          ? 'Mostrando los ' + shown + ' productos'
          : 'Mostrando ' + shown + ' de ' + items.length + ' productos';
      }
    });
  }

  /* ---------- Año actual en el pie -------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* =========================================================
     PEDIDO POR WHATSAPP
     No hay backend: el pedido se guarda en localStorage y se
     envía como UN solo mensaje con todo y el total calculado.
     Sin JS, los botones siguen funcionando como enlace directo.
     ========================================================= */
  var WA_NUMBER = '50688252608';
  // Datos de pago que ve el cliente. Cambialos acá y se actualizan en todo el sitio.
  var SINPE_NUM = '8825 2608';
  var SINPE_NAME = 'CARLOUIS Gourmet';
  var STORE_KEY = 'carlouis:pedido';
  var addButtons = document.querySelectorAll('[data-add]');

  // Formato tico: punto como separador de miles (₡14.000), igual que el resto
  // del sitio. toLocaleString('es-CR') usa espacio y quedaba inconsistente.
  var money = function (n) {
    return '₡' + String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  };

  var load = function () {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) { return []; }
  };
  var save = function (items) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(items)); } catch (e) {}
  };

  var order = load();

  if (addButtons.length || order.length) {
    // ---- Construcción del DOM (solo si hay JS) ----
    var icon = function (id, cls) {
      return '<svg ' + (cls ? 'class="' + cls + '" ' : '') + 'aria-hidden="true"><use href="#i-' + id + '"/></svg>';
    };

    var fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'order-fab';
    fab.setAttribute('aria-haspopup', 'dialog');
    fab.innerHTML = icon('cart') + '<span>Mi pedido</span><span class="order-fab__count">0</span>';

    var backdrop = document.createElement('div');
    backdrop.className = 'order-backdrop';

    var panel = document.createElement('aside');
    panel.className = 'order-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-label', 'Tu pedido');
    panel.innerHTML =
      '<div class="order-panel__head">' +
        '<div>' +
          '<button class="order-back" type="button" aria-label="Volver a los productos">' + icon('left') + '</button>' +
          '<h2 data-panel-title>Tu pedido</h2>' +
        '</div>' +
        '<button class="order-close" type="button" aria-label="Cerrar el pedido">' + icon('close') + '</button>' +
      '</div>' +

      '<ul class="order-items"></ul>' +

      '<form class="order-form" hidden novalidate>' +
        '<p class="order-form__intro">Con estos datos coordinamos la entrega y te cotizamos el envío. ' +
          'Se envían dentro del mismo mensaje de WhatsApp.</p>' +
        '<div class="field">' +
          '<label for="cli-nombre">Nombre completo <span class="req">*</span></label>' +
          '<input type="text" id="cli-nombre" name="nombre" required maxlength="70" autocomplete="name" placeholder="Ej: Luis Rodríguez" />' +
        '</div>' +
        '<div class="field">' +
          '<label for="cli-tel">Teléfono <span class="req">*</span></label>' +
          '<input type="tel" id="cli-tel" name="telefono" required maxlength="20" inputmode="tel" autocomplete="tel" placeholder="Ej: 8825 2608" />' +
        '</div>' +
        '<div class="order-form__grid">' +
          '<div class="field">' +
            '<label for="cli-canton">Cantón <span class="req">*</span></label>' +
            '<input type="text" id="cli-canton" name="canton" required maxlength="50" autocomplete="address-level2" placeholder="Ej: Santa Ana" />' +
          '</div>' +
          '<div class="field">' +
            '<label for="cli-distrito">Distrito <span class="req">*</span></label>' +
            '<input type="text" id="cli-distrito" name="distrito" required maxlength="50" autocomplete="address-level3" placeholder="Ej: Pozos" />' +
          '</div>' +
        '</div>' +
        '<div class="field">' +
          '<label for="cli-direccion">Dirección exacta <span class="req">*</span></label>' +
          '<input type="text" id="cli-direccion" name="direccion" required maxlength="160" autocomplete="street-address" placeholder="Señas para llegar" />' +
          '<span class="hint">Entre más señas, más fácil la entrega.</span>' +
        '</div>' +
        '<div class="field">' +
          '<label for="cli-email">Correo electrónico <span class="hint">(opcional)</span></label>' +
          '<input type="email" id="cli-email" name="email" maxlength="100" inputmode="email" autocomplete="email" placeholder="vos@correo.com" />' +
        '</div>' +
      '</form>' +

      '<div class="order-panel__foot">' +
        '<p class="order-total"><span>Total a pagar</span> <span data-total>₡0</span></p>' +

        '<div class="order-pay" hidden>' +
          '<div class="sinpe">' +
            '<span class="sinpe__icon">' + icon('phone') + '</span>' +
            '<span>' +
              '<span class="sinpe__label">Pagá por SINPE Móvil</span>' +
              '<span class="sinpe__num">' + SINPE_NUM + '</span>' +
              '<span class="sinpe__name">' + SINPE_NAME + '</span>' +
            '</span>' +
          '</div>' +
        '</div>' +

        '<button class="btn btn--primary btn--block" type="button" data-next>' +
          'Continuar con mis datos ' + icon('arrow') + '</button>' +
        '<a class="btn btn--wa btn--block" data-send target="_blank" rel="noopener" href="#" hidden>' +
          icon('wa') + ' Enviar pedido por WhatsApp</a>' +
        '<p class="order-note" data-foot-note>El subtotal no incluye el envío.</p>' +
      '</div>';

    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    document.body.appendChild(fab);
    document.body.appendChild(backdrop);
    document.body.appendChild(panel);
    document.body.appendChild(toast);

    var listEl = panel.querySelector('.order-items');
    var formEl = panel.querySelector('.order-form');
    var totalEl = panel.querySelector('[data-total]');
    var sendEl = panel.querySelector('[data-send]');
    var nextEl = panel.querySelector('[data-next]');
    var backEl = panel.querySelector('.order-back');
    var payEl = panel.querySelector('.order-pay');
    var noteEl = panel.querySelector('[data-foot-note]');
    var titleEl = panel.querySelector('[data-panel-title]');
    var countEl = fab.querySelector('.order-fab__count');
    var lastFocus = null;
    var step = 1;

    // Los datos del cliente quedan en SU navegador para no tener que
    // reescribirlos en el próximo pedido. No se envían a ningún servidor:
    // viajan únicamente dentro del mensaje de WhatsApp que él mismo manda.
    var CLIENT_KEY = 'carlouis:cliente';
    var FIELDS = ['nombre', 'telefono', 'canton', 'distrito', 'direccion', 'email'];

    var loadClient = function () {
      try {
        var raw = localStorage.getItem(CLIENT_KEY);
        return raw ? JSON.parse(raw) : {};
      } catch (e) { return {}; }
    };
    var readForm = function () {
      var data = {};
      FIELDS.forEach(function (f) {
        var el = formEl.elements[f];
        data[f] = el ? el.value.trim() : '';
      });
      return data;
    };
    var saveClient = function () {
      try { localStorage.setItem(CLIENT_KEY, JSON.stringify(readForm())); } catch (e) {}
    };

    // Rellenar con lo guardado de la vez pasada
    (function () {
      var saved = loadClient();
      FIELDS.forEach(function (f) {
        if (saved[f] && formEl.elements[f]) formEl.elements[f].value = saved[f];
      });
    })();
    formEl.addEventListener('input', function () {
      saveClient();
      sendEl.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(buildMessage());
    });

    var total = function () {
      return order.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    };
    var count = function () {
      return order.reduce(function (s, i) { return s + i.qty; }, 0);
    };

    var buildMessage = function () {
      var lines = order.map(function (i) {
        return '• ' + i.qty + ' x ' + i.name + ' — ' + money(i.price * i.qty);
      });
      var msg = 'Hola CARLOUIS, quiero hacer este pedido:\n\n' + lines.join('\n') +
                '\n\nTotal a pagar: ' + money(total());

      var c = readForm();
      if (c.nombre || c.telefono) {
        msg += '\n\n--- Mis datos ---' +
               '\nNombre: ' + c.nombre +
               '\nTeléfono: ' + c.telefono +
               '\nCantón: ' + c.canton +
               '\nDistrito: ' + c.distrito +
               '\nDirección: ' + c.direccion;
        if (c.email) msg += '\nCorreo: ' + c.email;
      }

      msg += '\n\nVoy a pagar por SINPE Móvil al ' + SINPE_NUM + ' (' + SINPE_NAME + ').';
      return msg;
    };

    var render = function () {
      var n = count();
      countEl.textContent = String(n);
      fab.classList.toggle('is-active', n > 0);
      fab.setAttribute('aria-label', 'Ver tu pedido, ' + n + (n === 1 ? ' producto' : ' productos'));
      totalEl.textContent = money(total());
      sendEl.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(buildMessage());

      if (!order.length) {
        listEl.innerHTML = '<li class="order-empty">' + icon('cart') +
          '<p>Todavía no agregaste nada.<br>Explorá el catálogo y armá tu pedido.</p></li>';
        nextEl.disabled = true;
        return;
      }
      nextEl.disabled = false;

      listEl.innerHTML = order.map(function (i, idx) {
        return '<li class="order-item">' +
          '<img src="' + i.img + '" alt="" width="62" height="62" />' +
          '<div>' +
            '<p class="order-item__name">' + i.name + '</p>' +
            '<p class="order-item__price">' + money(i.price) + ' c/u</p>' +
            '<div class="order-item__row">' +
              '<div class="qty">' +
                '<button type="button" data-dec="' + idx + '" aria-label="Quitar uno de ' + i.name + '">' + icon('minus') + '</button>' +
                '<output aria-label="Cantidad de ' + i.name + '">' + i.qty + '</output>' +
                '<button type="button" data-inc="' + idx + '" aria-label="Agregar uno de ' + i.name + '">' + icon('plus') + '</button>' +
              '</div>' +
              '<button class="order-item__remove" type="button" data-del="' + idx + '" aria-label="Eliminar ' + i.name + ' del pedido">' + icon('trash') + '</button>' +
            '</div>' +
          '</div>' +
        '</li>';
      }).join('');
    };

    var toastTimer;
    var showToast = function (text) {
      toast.innerHTML = icon('check') + '<span>' + text + '</span>';
      toast.classList.add('is-visible');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { toast.classList.remove('is-visible'); }, 2200);
    };

    // Paso 1 = productos, paso 2 = datos del cliente + cómo se paga
    var goStep = function (n, focusField) {
      step = n;
      var datos = n === 2;
      listEl.hidden = datos;
      formEl.hidden = !datos;
      nextEl.hidden = datos;
      sendEl.hidden = !datos;
      payEl.hidden = !datos;
      noteEl.textContent = datos
        ? 'Al enviar se abre WhatsApp con el pedido y tus datos ya escritos.'
        : 'Mismo precio para cualquier parte del país.';
      backEl.classList.toggle('is-shown', datos);
      titleEl.textContent = datos ? 'Tus datos y pago' : 'Tu pedido';
      if (datos && focusField) formEl.elements.nombre.focus();
    };

    var openPanel = function () {
      lastFocus = document.activeElement;
      backdrop.classList.add('is-open');
      panel.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      goStep(1);
      panel.querySelector('.order-close').focus();
    };
    var closePanel = function () {
      backdrop.classList.remove('is-open');
      panel.classList.remove('is-open');
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    };

    // ---- Agregar desde las tarjetas ----
    addButtons.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        var name = btn.dataset.name;
        var price = parseInt(btn.dataset.price, 10);
        if (!name || !price) return;         // sin datos, deja pasar el enlace
        e.preventDefault();

        var existing = order.filter(function (i) { return i.name === name; })[0];
        if (existing) {
          existing.qty++;
        } else {
          var card = btn.closest('.card');
          var img = card ? card.querySelector('img') : null;
          order.push({
            name: name,
            price: price,
            qty: 1,
            img: img ? (img.currentSrc || img.src) : ''
          });
        }
        save(order);
        render();
        fab.classList.remove('is-bump');
        void fab.offsetWidth;               // reinicia la animación
        fab.classList.add('is-bump');
        showToast(name + ' agregado');
      });
    });

    // ---- Controles del panel ----
    fab.addEventListener('click', openPanel);
    backdrop.addEventListener('click', closePanel);
    panel.querySelector('.order-close').addEventListener('click', closePanel);

    listEl.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      var d = btn.dataset;
      if (d.inc !== undefined) order[+d.inc].qty++;
      else if (d.dec !== undefined) {
        var it = order[+d.dec];
        if (--it.qty <= 0) order.splice(+d.dec, 1);
      } else if (d.del !== undefined) order.splice(+d.del, 1);
      else return;
      save(order);
      render();
      if (!order.length) closePanel();
    });

    // Ir al paso de datos / volver
    nextEl.addEventListener('click', function () {
      if (!order.length) return;
      goStep(2, true);
    });
    backEl.addEventListener('click', function () {
      goStep(1);
      nextEl.focus();
    });

    // Enviar: primero validar los datos obligatorios
    sendEl.addEventListener('click', function (e) {
      if (!order.length) { e.preventDefault(); return; }

      sendEl.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(buildMessage());

      if (!formEl.checkValidity()) {
        e.preventDefault();
        formEl.reportValidity();
        var primero = formEl.querySelector(':invalid');
        if (primero) primero.focus();
        return;
      }

      saveClient();
      // Se vacía el pedido, pero los datos del cliente quedan para la próxima
      setTimeout(function () {
        order.length = 0;
        save(order);
        render();
        closePanel();
      }, 600);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) closePanel();
    });

    render();
  }

  /* ---------- Ampliar imagen de producto -------------------- */
  var zoomables = document.querySelectorAll('.card__media');
  if (zoomables.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Imagen ampliada del producto');
    lb.innerHTML =
      '<button class="lightbox__close" type="button" aria-label="Cerrar la imagen">' +
        '<svg aria-hidden="true"><use href="#i-close"/></svg></button>' +
      '<figure style="margin:0"><img alt="" /><figcaption></figcaption></figure>';
    document.body.appendChild(lb);

    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('figcaption');
    var lbLast = null;

    var closeLb = function () {
      lb.classList.remove('is-open');
      document.body.style.overflow = '';
      if (lbLast) lbLast.focus();
    };

    zoomables.forEach(function (media) {
      var img = media.querySelector('img');
      var card = media.closest('.card');
      if (!img || !card) return;
      var title = card.querySelector('h3');

      var zoom = document.createElement('button');
      zoom.type = 'button';
      zoom.className = 'card__zoom';
      zoom.setAttribute('aria-label', 'Ampliar la imagen de ' + (title ? title.textContent.trim() : 'este producto'));
      zoom.innerHTML = '<svg aria-hidden="true"><use href="#i-zoom"/></svg>';
      media.appendChild(zoom);

      zoom.addEventListener('click', function () {
        lbLast = zoom;
        lbImg.src = img.currentSrc || img.src;
        lbImg.alt = img.alt;
        lbCap.textContent = title ? title.textContent.trim() : '';
        lb.classList.add('is-open');
        document.body.style.overflow = 'hidden';
        lb.querySelector('.lightbox__close').focus();
      });
    });

    lb.addEventListener('click', function (e) {
      if (e.target === lb || e.target.closest('.lightbox__close')) closeLb();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lb.classList.contains('is-open')) closeLb();
    });
  }

  /* ---------- Imágenes opcionales --------------------------- */
  // Logos de terceros (sedes de ferias) que pueden no estar cargados todavía:
  // si el archivo falta, se oculta el bloque en vez de mostrar un icono roto.
  document.querySelectorAll('img[data-optional]').forEach(function (img) {
    img.addEventListener('error', function () {
      var host = img.closest('[data-optional-host]') || img;
      host.hidden = true;
    });
  });

  /* ---------- Volver arriba --------------------------------- */
  var toTop = document.createElement('button');
  toTop.type = 'button';
  toTop.className = 'to-top';
  toTop.setAttribute('aria-label', 'Volver al inicio de la página');
  toTop.innerHTML = '<svg aria-hidden="true"><use href="#i-up"/></svg>';
  document.body.appendChild(toTop);

  toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
  });
  window.addEventListener('scroll', function () {
    toTop.classList.toggle('is-visible', window.scrollY > 900);
  }, { passive: true });
})();
