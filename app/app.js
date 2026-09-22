/* =========================================================================
   CARLOUIS · Control — herramienta interna
   -------------------------------------------------------------------------
   Todo corre en el teléfono. No hay servidor, no hay cuenta, no hay costo.
   Los datos viven en localStorage de ESTE aparato: no se sincronizan con
   otro teléfono y se pierden si se borran los datos del navegador. Por eso
   el respaldo manual (Resumen > Respaldo) no es un extra, es obligatorio.
   ========================================================================= */
(function () {
  'use strict';

  var LLAVE = 'carlouis.control.v1';

  /* ---------- utilidades ------------------------------------------------ */

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var vista = $('[data-vista]');

  // Todo lo que venga del usuario pasa por acá antes de entrar al HTML.
  function esc(t) {
    return String(t == null ? '' : t)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  var fmt = new Intl.NumberFormat('es-CR', { maximumFractionDigits: 0 });
  function money(n) { return '₡' + fmt.format(Math.round(n || 0)); }

  function hoyISO() {
    var d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }

  var MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
               'jul', 'ago', 'set', 'oct', 'nov', 'dic'];
  var DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

  function fechaCorta(iso) {
    if (!iso) return '';
    var p = iso.split('-');
    return Number(p[2]) + ' ' + MESES[Number(p[1]) - 1];
  }
  function fechaLarga(iso) {
    if (!iso) return '';
    var p = iso.split('-');
    var d = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
    return DIAS[d.getDay()] + ' ' + Number(p[2]) + ' de ' + MESES[Number(p[1]) - 1];
  }
  function id() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  }

  function aviso(texto) {
    var a = $('[data-aviso]');
    a.textContent = texto;
    a.hidden = false;
    clearTimeout(aviso._t);
    aviso._t = setTimeout(function () { a.hidden = true; }, 2600);
  }

  /* ---------- almacenamiento -------------------------------------------- */

  var VACIO = { v: 1, clientes: [], pedidos: [], gastos: [], rutas: [], ferias: [], stock: {} };
  var BD;

  // Llave de cifrado en memoria. Nunca se guarda en el teléfono: se deriva de
  // la clave cada vez que se abre la app. Si no hay clave puesta, queda null y
  // los datos se guardan en claro.
  var LLAVE_AES = null;

  function normalizar() {
    ['clientes', 'pedidos', 'gastos', 'rutas', 'ferias'].forEach(function (k) {
      if (!Array.isArray(BD[k])) BD[k] = [];
    });
    if (!BD.stock || typeof BD.stock !== 'object') BD.stock = {};
  }

  function hay(slug) { return Number(BD.stock[slug] || 0); }
  function moverStock(lineas, signo) {
    (lineas || []).forEach(function (l) {
      BD.stock[l.slug] = hay(l.slug) + signo * l.cant;
    });
  }
  function bajoStock() {
    return CATALOGO.filter(function (p) { return hay(p.slug) <= 3; });
  }

  function cargar() {
    try {
      var crudo = localStorage.getItem(LLAVE);
      var d = crudo ? JSON.parse(crudo) : null;
      // Si viene cifrado no se puede leer todavía: lo resuelve pedirClave().
      BD = (d && d.cifrado) ? JSON.parse(JSON.stringify(VACIO)) : (d || JSON.parse(JSON.stringify(VACIO)));
    } catch (e) {
      BD = JSON.parse(JSON.stringify(VACIO));
    }
    normalizar();
  }

  function estaCifrado() {
    try {
      var d = JSON.parse(localStorage.getItem(LLAVE) || 'null');
      return !!(d && d.cifrado);
    } catch (e) { return false; }
  }

  // Derivación lenta a propósito: 250.000 vueltas hacen que probar claves a
  // la fuerza sea caro aunque alguien se lleve el teléfono.
  function derivar(pin, salBase64) {
    var sal = Uint8Array.from(atob(salBase64), function (c) { return c.charCodeAt(0); });
    return crypto.subtle.importKey('raw', new TextEncoder().encode(pin),
                                   'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: 'PBKDF2', salt: sal, iterations: 250000, hash: 'SHA-256' },
          base, { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']);
      });
  }

  function b64(buf) {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(buf)));
  }
  function deB64(t) {
    return Uint8Array.from(atob(t), function (c) { return c.charCodeAt(0); });
  }

  function guardar() {
    try {
      if (!LLAVE_AES) {
        localStorage.setItem(LLAVE, JSON.stringify(BD));
        return;
      }
      // AES-GCM con vector nuevo en cada escritura, como debe ser.
      var iv = crypto.getRandomValues(new Uint8Array(12));
      var texto = new TextEncoder().encode(JSON.stringify(BD));
      crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, LLAVE_AES, texto)
        .then(function (ct) {
          var g = claveGuardada();
          localStorage.setItem(LLAVE, JSON.stringify({
            cifrado: true, sal: g.sal, iv: b64(iv), datos: b64(ct)
          }));
        })
        .catch(function () { aviso('No se pudo guardar'); });
    } catch (e) {
      aviso('No se pudo guardar. ¿Memoria llena?');
    }
  }

  function descifrarCon(llave) {
    var d = JSON.parse(localStorage.getItem(LLAVE) || 'null');
    if (!d || !d.cifrado) return Promise.resolve(true);
    return crypto.subtle.decrypt({ name: 'AES-GCM', iv: deB64(d.iv) }, llave, deB64(d.datos))
      .then(function (buf) {
        BD = JSON.parse(new TextDecoder().decode(buf));
        normalizar();
        return true;
      })
      .catch(function () { return false; });
  }

  var CATALOGO = window.CATALOGO || [];
  function cliente(cid) {
    for (var i = 0; i < BD.clientes.length; i++) {
      if (BD.clientes[i].id === cid) return BD.clientes[i];
    }
    return null;
  }
  function nombreCliente(cid) {
    if (!cid) return 'Venta en feria';
    var c = cliente(cid);
    return c ? c.nombre : 'Cliente borrado';
  }
  function feriaActiva() {
    for (var i = 0; i < BD.ferias.length; i++) {
      if (!BD.ferias[i].cerrada) return BD.ferias[i];
    }
    return null;
  }
  function ventasFeria(fid) {
    return BD.pedidos.filter(function (p) { return p.feriaId === fid; });
  }
  function gastosFeria(fid) {
    return BD.gastos.filter(function (g) { return g.feriaId === fid; });
  }

  /* ---------- hoja modal ------------------------------------------------ */

  var hoja = $('[data-hoja]');
  function abrirHoja(titulo, html, listo) {
    $('[data-hoja-titulo]').textContent = titulo;
    var cuerpo = $('[data-hoja-cuerpo]');
    cuerpo.innerHTML = html;
    hoja.hidden = false;
    document.body.style.overflow = 'hidden';
    if (listo) listo(cuerpo);
  }
  function cerrarHoja() {
    hoja.hidden = true;
    document.body.style.overflow = '';
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-hoja-cerrar]')) cerrarHoja();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !hoja.hidden) cerrarHoja();
  });

  /* ---------- geometría y ruta ------------------------------------------ */

  // Distancia en km sobre la superficie terrestre. Suficiente para ordenar
  // paradas: no calcula calles, pero para una ruta de ciudad el orden que
  // da la línea recta es casi siempre el orden correcto de manejo.
  function dist(a, b) {
    var R = 6371, rad = Math.PI / 180;
    var dLat = (b.lat - a.lat) * rad;
    var dLng = (b.lng - a.lng) * rad;
    var s = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(a.lat * rad) * Math.cos(b.lat * rad) *
            Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return 2 * R * Math.asin(Math.min(1, Math.sqrt(s)));
  }

  function largoRuta(pts, origen) {
    var t = 0, prev = origen || pts[0];
    for (var i = 0; i < pts.length; i++) { t += dist(prev, pts[i]); prev = pts[i]; }
    return t;
  }

  // Vecino más cercano y después 2-opt. Con 10 o 20 paradas esto da el
  // óptimo o queda muy cerca, y corre en milisegundos en un teléfono.
  function optimizar(pts, origen) {
    if (pts.length < 2) return pts.slice();
    var pend = pts.slice(), orden = [], act = origen || pend[0];
    while (pend.length) {
      var mejor = 0, md = Infinity;
      for (var i = 0; i < pend.length; i++) {
        var d = dist(act, pend[i]);
        if (d < md) { md = d; mejor = i; }
      }
      act = pend[mejor];
      orden.push(act);
      pend.splice(mejor, 1);
    }
    var mejoro = true, vueltas = 0;
    while (mejoro && vueltas < 60) {
      mejoro = false; vueltas++;
      for (var a = 0; a < orden.length - 1; a++) {
        for (var b = a + 1; b < orden.length; b++) {
          var cand = orden.slice(0, a)
            .concat(orden.slice(a, b + 1).reverse())
            .concat(orden.slice(b + 1));
          if (largoRuta(cand, origen) < largoRuta(orden, origen) - 1e-9) {
            orden = cand; mejoro = true;
          }
        }
      }
    }
    return orden;
  }

  function ubicacionActual() {
    return new Promise(function (res) {
      if (!navigator.geolocation) return res(null);
      navigator.geolocation.getCurrentPosition(
        function (p) { res({ lat: p.coords.latitude, lng: p.coords.longitude }); },
        function () { res(null); },
        { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 }
      );
    });
  }

  // Waze navega a UN destino por vez: no acepta paradas múltiples por enlace.
  // Por eso cada parada lleva su botón y el chofer va tocando el siguiente.
  function urlWaze(c) {
    if (c && c.lat != null && c.lng != null) {
      return 'https://www.waze.com/ul?ll=' + c.lat + ',' + c.lng + '&navigate=yes';
    }
    var q = [c && c.direccion, c && c.zona, 'Costa Rica'].filter(Boolean).join(', ');
    return 'https://www.waze.com/ul?q=' + encodeURIComponent(q) + '&navigate=yes';
  }

  // Google Maps sí acepta paradas intermedias, así que sirve para ver la
  // ruta completa de un vistazo. El tope son 9 paradas más el destino.
  function urlMapsRuta(lista, origen) {
    var conCoord = lista.filter(function (c) { return c.lat != null; });
    if (!conCoord.length) return null;
    var pto = function (c) { return c.lat + ',' + c.lng; };
    var destino = conCoord[conCoord.length - 1];
    var medias = conCoord.slice(0, -1).slice(0, 9);
    var u = 'https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=' + pto(destino);
    if (origen) u += '&origin=' + pto(origen);
    if (medias.length) u += '&waypoints=' + medias.map(pto).join('|');
    return u;
  }

  // Acepta pegar un enlace de Google Maps o Waze y le saca las coordenadas.
  function coordsDeTexto(txt) {
    if (!txt) return null;
    var pats = [
      /@(-?\d+\.\d+),(-?\d+\.\d+)/,                    // maps/@9.99,-84.1,17z
      /[?&]ll=(-?\d+\.\d+),\s*(-?\d+\.\d+)/,           // waze ?ll=
      /[?&]q=(-?\d+\.\d+),\s*(-?\d+\.\d+)/,            // ?q=lat,lng
      /[?&]query=(-?\d+\.\d+),\s*(-?\d+\.\d+)/,        // ?query=lat,lng
      /^\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*$/        // pegado a mano
    ];
    for (var i = 0; i < pats.length; i++) {
      var m = txt.match(pats[i]);
      if (m) {
        var la = parseFloat(m[1]), ln = parseFloat(m[2]);
        if (la >= -90 && la <= 90 && ln >= -180 && ln <= 180) return { lat: la, lng: ln };
      }
    }
    return null;
  }

  /* ---------- cálculos --------------------------------------------------- */

  function totalPedido(p) {
    return (p.lineas || []).reduce(function (s, l) { return s + l.precio * l.cant; }, 0);
  }

  // Un cliente puede abonar de a poco. `pagado` (booleano) es del formato
  // viejo y se respeta para no perder datos de pedidos ya guardados.
  function abonado(p) {
    if (p.pagado && !(p.pagos || []).length) return totalPedido(p);
    return (p.pagos || []).reduce(function (s, x) { return s + x.monto; }, 0);
  }
  function saldo(p) { return Math.max(0, totalPedido(p) - abonado(p)); }
  function estaPago(p) { return saldo(p) <= 0; }
  function enRango(iso, desde) { return iso >= desde; }

  function inicioSemana() {
    var d = new Date();
    d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }
  function inicioMes() { return hoyISO().slice(0, 7) + '-01'; }

  function ventas(desde) {
    return BD.pedidos
      .filter(function (p) { return p.estado !== 'cancelado' && enRango(p.fecha, desde); })
      .reduce(function (s, p) { return s + totalPedido(p); }, 0);
  }
  function gastos(desde) {
    return BD.gastos
      .filter(function (g) { return enRango(g.fecha, desde); })
      .reduce(function (s, g) { return s + g.monto; }, 0);
  }

  /* =======================================================================
     VISTAS
     ===================================================================== */

  var V = {};

  /* ---------- Hoy -------------------------------------------------------- */
  V.hoy = function () {
    var pend = BD.pedidos.filter(function (p) { return p.estado === 'pendiente'; });
    var sinPagar = BD.pedidos.filter(function (p) {
      return p.estado === 'entregado' && !estaPago(p);
    });
    var porCobrar = sinPagar.reduce(function (s, p) { return s + saldo(p); }, 0);
    var rutasHoy = BD.rutas.filter(function (r) { return r.fecha === hoyISO(); });

    var h = '<div class="seccion"><div class="cifras">' +
      '<div class="cifra"><b>' + money(ventas(inicioSemana())) + '</b><span>ventas esta semana</span></div>' +
      '<div class="cifra"><b>' + money(ventas(inicioMes())) + '</b><span>ventas este mes</span></div>' +
      '<div class="cifra' + (pend.length ? ' cifra--bad' : '') + '"><b>' + pend.length + '</b><span>pedidos pendientes</span></div>' +
      '<div class="cifra' + (porCobrar ? ' cifra--bad' : ' cifra--ok') + '"><b>' + money(porCobrar) + '</b><span>por cobrar</span></div>' +
      '</div></div>';

    // Lo que de verdad se pregunta uno: cuánto queda después de gastos.
    var gananciaMes = ventas(inicioMes()) - gastos(inicioMes());
    h += '<div class="seccion"><div class="cifra' +
      (gananciaMes >= 0 ? ' cifra--ok' : ' cifra--bad') + '" style="text-align:center">' +
      '<b style="font-size:2.1rem">' + money(gananciaMes) + '</b>' +
      '<span>le queda este mes, ya restando gastos</span></div></div>';

    // A quién hay que buscar hoy.
    var seguir = BD.clientes.map(function (c) {
      return { c: c, s: seguimiento(c) };
    }).filter(function (x) { return x.s.atrasado || x.s.deuda > 0; })
      .sort(function (a, b) { return b.s.deuda - a.s.deuda || b.s.dias - a.s.dias; });

    if (seguir.length) {
      h += '<div class="seccion"><h3>A quién buscar</h3>';
      seguir.slice(0, 4).forEach(function (x) {
        h += '<button class="tarjeta tarjeta--btn" data-ir="#/clientes/' + esc(x.c.id) + '">' +
          '<div class="fila fila--sep"><span class="tarjeta__t">' + esc(x.c.nombre) + '</span>' +
          (x.s.deuda > 0 ? '<span class="et et--sin">debe ' + money(x.s.deuda) + '</span>' : '') +
          '</div><p class="tarjeta__s">' +
          (x.s.atrasado ? 'Hace ' + x.s.dias + ' días que no compra, y suele pedir cada ' +
            x.s.ritmo : 'Tiene saldo pendiente') + '</p></button>';
      });
      if (seguir.length > 4) {
        h += '<p class="pista">y ' + (seguir.length - 4) + ' más en la lista de clientes.</p>';
      }
      h += '</div>';
    }

    var bajo = bajoStock();
    if (bajo.length) {
      h += '<div class="seccion"><button class="zona-btn" style="width:100%;' +
        'border-color:var(--bad)" data-ir="#/dinero"><b style="color:var(--bad)">' +
        'Se está acabando</b><span>' +
        bajo.slice(0, 3).map(function (p) {
          return esc(p.nombre) + ' (' + hay(p.slug) + ')';
        }).join(' \u00b7 ') +
        (bajo.length > 3 ? ' y ' + (bajo.length - 3) + ' más' : '') +
        '</span></button></div>';
    }

    var fAct = feriaActiva();
    h += '<div class="seccion">' + (fAct
      ? '<button class="zona-btn" style="width:100%;border-color:var(--gold-500)" data-ir="#/feria">' +
        '<b>' + esc(fAct.nombre) + ' \u2014 caja abierta</b>' +
        '<span><em>' + money(ventasFeria(fAct.id).reduce(function (s, p) {
          return s + totalPedido(p); }, 0)) + '</em> vendido \u00b7 tocá para seguir cobrando</span></button>'
      : '<button class="zona-btn" style="width:100%" data-ir="#/feria">' +
        '<b>Modo feria</b><span>Caja rápida para vender en el puesto</span></button>') +
      '</div>';

    h += '<div class="seccion"><div class="acciones">' +
      '<button class="btn" data-ir="#/pedidos/nuevo"><svg aria-hidden="true"><use href="#i-plus"/></svg> Pedido</button>' +
      '<button class="btn btn--sec" data-rapido><svg aria-hidden="true"><use href="#i-plus"/></svg> Cliente</button>' +
      '<button class="btn btn--sec" data-ir="#/gastos/nuevo"><svg aria-hidden="true"><use href="#i-plus"/></svg> Gasto</button>' +
      '</div></div>';

    if (rutasHoy.length) {
      h += '<div class="seccion"><h3>Ruta de hoy</h3>';
      rutasHoy.forEach(function (r) {
        var hechas = r.paradas.filter(function (p) { return p.hecho; }).length;
        h += '<button class="tarjeta tarjeta--btn" data-ir="#/rutas/' + r.id + '">' +
          '<p class="tarjeta__t">' + esc(r.nombre) + '</p>' +
          '<p class="tarjeta__s">' + hechas + ' de ' + r.paradas.length + ' entregas hechas</p>' +
          '</button>';
      });
      h += '</div>';
    }

    if (pend.length) {
      h += '<div class="seccion"><h3>Pendientes de entregar</h3>';
      pend.slice(0, 6).forEach(function (p) { h += tarjetaPedido(p); });
      h += '</div>';
    }

    if (!BD.clientes.length && !BD.pedidos.length) {
      h += '<div class="vacio"><p>Todavía no hay nada guardado.<br>Empezá agregando un cliente.</p>' +
        '<button class="btn" data-ir="#/clientes/nuevo">Agregar el primer cliente</button></div>';
    }
    return h;
  };

  // Días entre dos fechas ISO.
  function diasEntre(a, b) {
    return Math.round((new Date(b) - new Date(a)) / 86400000);
  }

  // Resumen de comportamiento de un cliente, con lo que ya está guardado.
  function seguimiento(c) {
    var peds = BD.pedidos
      .filter(function (p) { return p.clienteId === c.id && p.estado !== 'cancelado'; })
      .sort(function (a, b) { return a.fecha.localeCompare(b.fecha); });
    if (!peds.length) {
      return { nunca: true, dias: diasEntre(c.creado || hoyISO(), hoyISO()),
               deuda: 0, compras: 0, total: 0 };
    }
    var ultima = peds[peds.length - 1].fecha;
    var dias = diasEntre(ultima, hoyISO());
    // Ritmo propio: promedio de días entre compras. Con una sola compra no
    // hay ritmo todavía, así que se usa un mes como referencia.
    var ritmo = peds.length > 1
      ? diasEntre(peds[0].fecha, ultima) / (peds.length - 1)
      : 30;
    var deuda = peds.reduce(function (s2, p) { return s2 + saldo(p); }, 0);
    return {
      nunca: false, dias: dias, ritmo: Math.max(7, Math.round(ritmo)),
      atrasado: dias > ritmo * 1.6, deuda: deuda,
      compras: peds.length,
      total: peds.reduce(function (s2, p) { return s2 + totalPedido(p); }, 0),
      ultima: ultima
    };
  }

  /* ---------- Clientes --------------------------------------------------- */
  var filtroZona = '';
  var buscaCliente = '';

  V.clientes = function () {
    var zonas = [];
    BD.clientes.forEach(function (c) {
      if (c.zona && zonas.indexOf(c.zona) < 0) zonas.push(c.zona);
    });
    zonas.sort();

    var lista = BD.clientes.filter(function (c) {
      if (filtroZona && c.zona !== filtroZona) return false;
      if (buscaCliente) {
        var t = (c.nombre + ' ' + (c.tel || '') + ' ' + (c.direccion || '')).toLowerCase();
        if (t.indexOf(buscaCliente.toLowerCase()) < 0) return false;
      }
      return true;
    }).sort(function (a, b) {
      var za = a.zona || '\uffff', zb = b.zona || '\uffff';
      if (za !== zb) return za.localeCompare(zb, 'es');
      return a.nombre.localeCompare(b.nombre, 'es');
    });

    var h = '<div class="buscador"><input type="search" placeholder="Buscar cliente…" ' +
      'value="' + esc(buscaCliente) + '" data-buscar-cliente /></div>';

    if (zonas.length) {
      h += '<div class="filtros"><button class="chip" aria-pressed="' + (!filtroZona) +
        '" data-zona="">Todas</button>';
      zonas.forEach(function (z) {
        h += '<button class="chip" aria-pressed="' + (filtroZona === z) +
          '" data-zona="' + esc(z) + '">' + esc(z) + '</button>';
      });
      h += '</div>';
    }

    if (!lista.length) {
      h += '<div class="vacio"><p>' +
        (BD.clientes.length ? 'Ningún cliente con ese filtro.' : 'Todavía no hay clientes.') +
        '</p><button class="btn" data-rapido>Agregar cliente</button></div>';
    } else {
      var conTel = lista.filter(function (c) { return c.tel; });
      if (conTel.length > 1) {
        h += '<button class="btn btn--wa btn--g" data-mensajes="' + esc(filtroZona) + '" ' +
          'style="margin-bottom:1rem"><svg aria-hidden="true"><use href="#i-wa"/></svg> ' +
          'Mandar mensaje a estos ' + conTel.length +
          (filtroZona ? ' de ' + esc(filtroZona) : '') + '</button>';
      }
      var zonaActual = null;
      lista.forEach(function (c) {
        // Encabezado de grupo: solo cuando se está viendo todo, porque con un
        // filtro puesto todos son de la misma zona y sobraría.
        if (!filtroZona) {
          var z = c.zona || 'Sin zona';
          if (z !== zonaActual) {
            zonaActual = z;
            h += '<p class="grupo">' + esc(z) + '</p>';
          }
        }
        var sg = seguimiento(c);
        h += '<button class="tarjeta tarjeta--btn" data-ir="#/clientes/' + c.id + '">' +
          '<div class="fila fila--sep"><span class="tarjeta__t">' + esc(c.nombre) + '</span>' +
          (sg.deuda > 0 ? '<span class="et et--sin">debe ' + money(sg.deuda) + '</span>'
           : sg.atrasado ? '<span class="et et--pend">hace ' + sg.dias + ' días</span>'
           : c.lat == null ? '<span class="et et--sin">sin GPS</span>' : '') + '</div>' +
          '<p class="tarjeta__s">' + esc(c.zona || 'Sin zona') +
          (c.direccion ? ' · ' + esc(c.direccion.slice(0, 40)) : '') + '</p>' +
          (sg.total ? '<p class="tarjeta__s">' + sg.compras + ' compra' +
            (sg.compras === 1 ? '' : 's') + ' · ' + money(sg.total) + '</p>'
           : '<p class="tarjeta__s">Todavía no ha comprado</p>') +
          '</button>';
      });
    }
    h += '<button class="fab" data-rapido aria-label="Agregar cliente rápido">' +
      '<svg aria-hidden="true"><use href="#i-plus"/></svg></button>';
    return h;
  };

  V.clienteForm = function (cid) {
    var c = cid ? cliente(cid) : null;
    var v = c || { nombre: '', tel: '', zona: '', direccion: '', notas: '', lat: null, lng: null };
    return '<form data-form-cliente data-id="' + esc(cid || '') + '">' +
      '<div class="campo"><label for="f-nom">Nombre *</label>' +
      '<input id="f-nom" name="nombre" required value="' + esc(v.nombre) + '" /></div>' +
      '<div class="campo--duo">' +
        '<div class="campo"><label for="f-tel">Teléfono</label>' +
        '<input id="f-tel" name="tel" type="tel" inputmode="tel" value="' + esc(v.tel) + '" /></div>' +
        '<div class="campo"><label for="f-zona">Zona o cantón</label>' +
        '<input id="f-zona" name="zona" list="l-zonas" value="' + esc(v.zona) + '" />' +
        '<datalist id="l-zonas">' + zonasSugeridas() + '</datalist></div>' +
      '</div>' +
      '<div class="campo"><label for="f-dir">Dirección</label>' +
      '<textarea id="f-dir" name="direccion">' + esc(v.direccion) + '</textarea>' +
      '<p class="pista">Entre más señas, mejor encuentra Waze.</p></div>' +
      '<div class="campo"><label for="f-gps">Ubicación exacta (GPS)</label>' +
      '<input id="f-gps" name="coords" placeholder="Pegá un enlace de Maps o Waze" value="' +
        (v.lat != null ? v.lat + ',' + v.lng : '') + '" />' +
      '<div class="acciones"><button class="btn btn--sec btn--sm" type="button" data-gps>' +
      '<svg aria-hidden="true"><use href="#i-gps"/></svg> Usar mi ubicación</button></div>' +
      '<p class="pista">Sin esto el cliente igual entra a la ruta, pero no se puede ordenar por cercanía. ' +
      'Lo más fácil: tocar el botón cuando esté parqueado frente a la casa.</p></div>' +
      '<div class="campo"><label for="f-not">Notas</label>' +
      '<textarea id="f-not" name="notas">' + esc(v.notas) + '</textarea></div>' +
      '<button class="btn btn--g" type="submit">' + (c ? 'Guardar cambios' : 'Agregar cliente') + '</button>' +
      (c ? '<div class="acciones"><button class="btn btn--mal btn--g" type="button" data-borrar-cliente="' +
        esc(c.id) + '"><svg aria-hidden="true"><use href="#i-trash"/></svg> Borrar cliente</button></div>' : '') +
      '</form>';
  };

  function zonasSugeridas() {
    var base = ['Alajuela', 'Heredia', 'San José', 'Escazú', 'Santa Ana', 'Belén', 'Curridabat',
                'Cartago', 'Grecia', 'Atenas', 'Santo Domingo', 'Barva', 'Tibás', 'Moravia'];
    BD.clientes.forEach(function (c) { if (c.zona && base.indexOf(c.zona) < 0) base.push(c.zona); });
    return base.map(function (z) { return '<option value="' + esc(z) + '"></option>'; }).join('');
  }

  V.clienteDetalle = function (cid) {
    var c = cliente(cid);
    if (!c) return '<div class="vacio"><p>Ese cliente ya no existe.</p></div>';
    var peds = BD.pedidos.filter(function (p) { return p.clienteId === cid; })
      .sort(function (a, b) { return b.fecha.localeCompare(a.fecha); });
    var total = peds.filter(function (p) { return p.estado !== 'cancelado'; })
      .reduce(function (s, p) { return s + totalPedido(p); }, 0);

    var h = '<div class="tarjeta">' +
      '<p class="tarjeta__t">' + esc(c.nombre) + '</p>' +
      '<p class="tarjeta__s">' + esc(c.zona || 'Sin zona') + '</p>' +
      (c.direccion ? '<p class="tarjeta__s">' + esc(c.direccion) + '</p>' : '') +
      (c.notas ? '<p class="tarjeta__s">' + esc(c.notas) + '</p>' : '') +
      '<div class="acciones">' +
      (c.tel ? '<a class="btn btn--wa btn--sm" href="https://wa.me/506' +
        esc(c.tel.replace(/\D/g, '').slice(-8)) + '" target="_blank" rel="noopener">' +
        '<svg aria-hidden="true"><use href="#i-wa"/></svg> WhatsApp</a>' +
        '<a class="btn btn--sec btn--sm" href="tel:' + esc(c.tel) + '">' +
        '<svg aria-hidden="true"><use href="#i-phone"/></svg> Llamar</a>' : '') +
      '<a class="btn btn--waze btn--sm" href="' + esc(urlWaze(c)) + '" target="_blank" rel="noopener">' +
      '<svg aria-hidden="true"><use href="#i-nav"/></svg> Waze</a>' +
      '<button class="btn btn--sec btn--sm" data-ir="#/clientes/' + esc(cid) + '/editar">' +
      '<svg aria-hidden="true"><use href="#i-edit"/></svg> Editar</button>' +
      '</div></div>';

    var sg2 = seguimiento(c);
    h += '<div class="seccion"><div class="cifras">' +
      '<div class="cifra"><b>' + money(total) + '</b><span>total comprado</span></div>' +
      '<div class="cifra"><b>' + peds.length + '</b><span>pedidos</span></div>' +
      (sg2.nunca ? ''
        : '<div class="cifra"><b>' + sg2.dias + '</b><span>días desde la última</span></div>' +
          '<div class="cifra"><b>c/' + sg2.ritmo + '</b><span>días suele pedir</span></div>') +
      (sg2.deuda > 0
        ? '<div class="cifra cifra--bad"><b>' + money(sg2.deuda) + '</b><span>debe</span></div>' : '') +
      '</div>';

    if (sg2.atrasado && c.tel) {
      h += '<button class="btn btn--wa btn--g" style="margin-top:.7rem" ' +
        'data-recordar="' + esc(c.id) + '">' +
        '<svg aria-hidden="true"><use href="#i-wa"/></svg> ' +
        'Escribirle, ya se atrasó</button>';
    }
    h += '</div>';

    h += '<div class="seccion"><h3>Historial</h3>';
    if (!peds.length) h += '<div class="vacio"><p>Sin pedidos todavía.</p></div>';
    else peds.forEach(function (p) { h += tarjetaPedido(p, true); });
    h += '</div>';
    return h;
  };

  /* ---------- Pedidos ---------------------------------------------------- */
  var filtroPedido = 'pendiente';

  function tarjetaPedido(p, ocultarNombre) {
    var et = p.estado === 'pendiente' ? '<span class="et et--pend">pendiente</span>'
      : p.estado === 'cancelado' ? '<span class="et et--sin">cancelado</span>'
      : (estaPago(p) ? '<span class="et et--pag">pagado</span>'
         : abonado(p) ? '<span class="et et--entr">debe ' + money(saldo(p)) + '</span>'
         : '<span class="et et--entr">entregado</span>');
    var items = (p.lineas || []).reduce(function (s, l) { return s + l.cant; }, 0);
    return '<button class="tarjeta tarjeta--btn" data-ir="#/pedidos/' + p.id + '">' +
      '<div class="fila fila--sep"><span class="tarjeta__t">' +
      (ocultarNombre ? fechaCorta(p.fecha) : esc(nombreCliente(p.clienteId))) +
      '</span>' + et + '</div>' +
      '<p class="tarjeta__s">' + (ocultarNombre ? '' : fechaCorta(p.fecha) + ' · ') +
      items + ' unidad' + (items === 1 ? '' : 'es') + ' · <b>' + money(totalPedido(p)) + '</b></p>' +
      '</button>';
  }

  V.pedidos = function () {
    var lista = BD.pedidos.filter(function (p) {
      return filtroPedido === 'todos' ? true
        : filtroPedido === 'cobrar' ? (p.estado === 'entregado' && !estaPago(p))
        : p.estado === filtroPedido;
    }).sort(function (a, b) { return b.fecha.localeCompare(a.fecha); });

    var h = '<div class="filtros">' +
      [['pendiente', 'Pendientes'], ['cobrar', 'Por cobrar'],
       ['entregado', 'Entregados'], ['todos', 'Todos']].map(function (f) {
        return '<button class="chip" aria-pressed="' + (filtroPedido === f[0]) +
          '" data-fped="' + f[0] + '">' + f[1] + '</button>';
      }).join('') + '</div>';

    if (!lista.length) {
      h += '<div class="vacio"><p>No hay pedidos acá.</p>' +
        '<button class="btn" data-ir="#/pedidos/nuevo">Crear pedido</button></div>';
    } else {
      lista.forEach(function (p) { h += tarjetaPedido(p); });
    }
    h += '<button class="fab" data-ir="#/pedidos/nuevo" aria-label="Nuevo pedido">' +
      '<svg aria-hidden="true"><use href="#i-plus"/></svg></button>';
    return h;
  };

  var borrador = null;

  V.pedidoForm = function () {
    if (!BD.clientes.length) {
      return '<div class="vacio"><p>Primero hay que tener al menos un cliente.</p>' +
        '<button class="btn" data-ir="#/clientes/nuevo">Agregar cliente</button></div>';
    }
    if (!borrador) borrador = { clienteId: BD.clientes[0].id, fecha: hoyISO(), lineas: {}, notas: '' };

    var h = '<form data-form-pedido>' +
      '<div class="campo"><label for="p-cli">Cliente</label><select id="p-cli" name="clienteId">' +
      BD.clientes.slice().sort(function (a, b) { return a.nombre.localeCompare(b.nombre, 'es'); })
        .map(function (c) {
          return '<option value="' + esc(c.id) + '"' +
            (c.id === borrador.clienteId ? ' selected' : '') + '>' + esc(c.nombre) +
            (c.zona ? ' — ' + esc(c.zona) : '') + '</option>';
        }).join('') + '</select></div>' +
      '<div class="campo"><label for="p-fec">Fecha de entrega</label>' +
      '<input id="p-fec" name="fecha" type="date" value="' + esc(borrador.fecha) + '" /></div>';

    h += '<div class="seccion"><h3>Productos</h3>';
    var cats = [];
    CATALOGO.forEach(function (p) { if (cats.indexOf(p.cat) < 0) cats.push(p.cat); });
    cats.forEach(function (cat) {
      h += '<p class="mut" style="margin:.7rem 0 .2rem;font-weight:700">' + esc(cat) + '</p>';
      CATALOGO.filter(function (p) { return p.cat === cat; }).forEach(function (p) {
        var n = borrador.lineas[p.slug] || 0;
        h += '<div class="linea"><div><span class="linea__n">' + esc(p.nombre) + '</span>' +
          '<br><span class="mut">' + money(p.precio) + ' · ' + esc(p.unidad) + '</span></div>' +
          '<div class="contador">' +
          '<button type="button" data-cant="-" data-slug="' + esc(p.slug) + '" aria-label="Quitar uno">−</button>' +
          '<span data-n="' + esc(p.slug) + '">' + n + '</span>' +
          '<button type="button" data-cant="+" data-slug="' + esc(p.slug) + '" aria-label="Agregar uno">+</button>' +
          '</div><b data-sub="' + esc(p.slug) + '">' + (n ? money(n * p.precio) : '') + '</b></div>';
      });
    });
    h += '<div class="total"><span>Total</span><span data-total>' + money(totalBorrador()) + '</span></div></div>';

    h += '<div class="campo"><label for="p-not">Notas</label>' +
      '<textarea id="p-not" name="notas">' + esc(borrador.notas) + '</textarea></div>' +
      '<button class="btn btn--g" type="submit">Guardar pedido</button></form>';
    return h;
  };

  function totalBorrador() {
    var t = 0;
    CATALOGO.forEach(function (p) { t += (borrador.lineas[p.slug] || 0) * p.precio; });
    return t;
  }

  V.pedidoDetalle = function (pid) {
    var p = null;
    BD.pedidos.forEach(function (x) { if (x.id === pid) p = x; });
    if (!p) return '<div class="vacio"><p>Ese pedido ya no existe.</p></div>';
    var c = cliente(p.clienteId);

    var h = '<div class="tarjeta">' +
      '<div class="fila fila--sep"><span class="tarjeta__t">' + esc(nombreCliente(p.clienteId)) + '</span>' +
      (p.estado === 'pendiente' ? '<span class="et et--pend">pendiente</span>'
        : p.pagado ? '<span class="et et--pag">pagado</span>'
        : '<span class="et et--entr">entregado</span>') + '</div>' +
      '<p class="tarjeta__s">Entrega: ' + fechaLarga(p.fecha) + '</p>' +
      (c && c.direccion ? '<p class="tarjeta__s">' + esc(c.direccion) + '</p>' : '') +
      (p.notas ? '<p class="tarjeta__s">' + esc(p.notas) + '</p>' : '') + '</div>';

    // Abonos: se ven siempre que haya al menos uno, y el saldo queda grande
    // porque es el número que de verdad importa cuando se llega a cobrar.
    var pagos = p.pagos || [];
    if (pagos.length || abonado(p)) {
      h += '<div class="tarjeta"><p class="tarjeta__t">Pagos</p>';
      pagos.forEach(function (x, i) {
        h += '<div class="pago"><span>' + fechaCorta(x.fecha) + ' · ' + esc(x.metodo) + '</span>' +
          '<span><b>' + money(x.monto) + '</b> ' +
          '<button class="icono" data-borrar-pago="' + esc(p.id) + '|' + i + '" ' +
          'aria-label="Borrar este pago"><svg aria-hidden="true"><use href="#i-trash"/></svg></button>' +
          '</span></div>';
      });
      if (!pagos.length) h += '<div class="pago"><span>Marcado como pagado</span><b>' +
        money(abonado(p)) + '</b></div>';
      h += '<div class="saldo' + (estaPago(p) ? ' saldo--cero' : '') + '"><span>' +
        (estaPago(p) ? 'Pagado completo' : 'Falta') + '</span><span>' +
        (estaPago(p) ? '\\u2713' : money(saldo(p))) + '</span></div></div>';
    }

    h += '<div class="tarjeta">';
    (p.lineas || []).forEach(function (l) {
      h += '<div class="linea"><span class="linea__n">' + esc(l.nombre) + '</span>' +
        '<span class="mut">' + l.cant + ' × ' + money(l.precio) + '</span>' +
        '<b>' + money(l.cant * l.precio) + '</b></div>';
    });
    h += '<div class="total"><span>Total</span><span>' + money(totalPedido(p)) + '</span></div></div>';

    h += '<div class="acciones">';
    if (p.estado === 'pendiente') {
      h += '<button class="btn btn--ok btn--g" data-entregado="' + esc(p.id) + '">' +
        '<svg aria-hidden="true"><use href="#i-check"/></svg> Marcar entregado</button>';
    }
    if (!estaPago(p) && p.estado !== 'cancelado') {
      h += '<button class="btn btn--gold btn--g" data-cobrar="' + esc(p.id) + '">' +
        'Registrar un pago' + (abonado(p) ? ' (falta ' + money(saldo(p)) + ')' : '') + '</button>';
    }
    h += '</div><div class="acciones">';
    if (c && c.tel) {
      h += '<a class="btn btn--wa btn--sm" href="https://wa.me/506' +
        esc(c.tel.replace(/\D/g, '').slice(-8)) + '?text=' + encodeURIComponent(textoPedido(p)) +
        '" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg> Enviar detalle</a>';
    }
    if (c) {
      h += '<a class="btn btn--waze btn--sm" href="' + esc(urlWaze(c)) + '" target="_blank" rel="noopener">' +
        '<svg aria-hidden="true"><use href="#i-nav"/></svg> Waze</a>';
    }
    h += '<button class="btn btn--mal btn--sm" data-borrar-pedido="' + esc(p.id) + '">' +
      '<svg aria-hidden="true"><use href="#i-trash"/></svg> Borrar</button></div>';
    return h;
  };

  function textoPedido(p) {
    var t = 'Pedido CARLOUIS\n\n';
    (p.lineas || []).forEach(function (l) {
      t += l.cant + ' × ' + l.nombre + '  ' + money(l.cant * l.precio) + '\n';
    });
    t += '\nTotal: ' + money(totalPedido(p));
    t += '\nEntrega: ' + fechaLarga(p.fecha);
    t += '\n\nSINPE Móvil al 8825 2608';
    return t;
  }

  /* ---------- Rutas ------------------------------------------------------ */

  // Lo que pasa de verdad un lunes: "hoy voy para Alajuela". Un toque y la
  // ruta queda armada con los que compraron y están por recibir, ya ordenada.
  function zonasConPendientes() {
    var m = {};
    BD.pedidos.forEach(function (p) {
      if (p.estado !== 'pendiente') return;
      var c = cliente(p.clienteId);
      if (!c) return;
      var z = c.zona || 'Sin zona';
      if (!m[z]) m[z] = {};
      m[z][c.id] = true;
    });
    return Object.keys(m).map(function (z) {
      return { zona: z, ids: Object.keys(m[z]) };
    }).sort(function (a, b) { return b.ids.length - a.ids.length; });
  }

  V.rutas = function () {
    var lista = BD.rutas.slice().sort(function (a, b) { return b.fecha.localeCompare(a.fecha); });
    var h = '';

    h += '<button class="btn btn--g" data-ir="#/rutas/nueva" style="margin-bottom:1.2rem">' +
      '<svg aria-hidden="true"><use href="#i-plus"/></svg> Armar ruta escogiendo clientes</button>';

    var zp = zonasConPendientes();
    if (zp.length) {
      h += '<div class="seccion"><h3>¿Para dónde va hoy?</h3>' +
        '<p class="mut" style="margin:0 0 .7rem">Tocá una zona y le armo la ruta con los ' +
        'que están esperando pedido, ya ordenada.</p><div class="zonas">';
      zp.forEach(function (z) {
        h += '<button class="zona-btn" data-ruta-rapida="' + esc(z.zona) + '">' +
          '<b>' + esc(z.zona) + '</b>' +
          '<span><em>' + z.ids.length + '</em> cliente' + (z.ids.length === 1 ? '' : 's') +
          ' esperando</span></button>';
      });
      h += '</div></div>';
    }
    if (!lista.length) {
      h += '<div class="vacio"><p>Todavía no hay rutas.<br>' +
        'Una ruta es la lista de entregas de un día, ya ordenada para manejar menos.</p>' +
        '<button class="btn" data-ir="#/rutas/nueva">Armar una ruta</button></div>';
    } else {
      lista.forEach(function (r) {
        var hechas = r.paradas.filter(function (p) { return p.hecho; }).length;
        h += '<button class="tarjeta tarjeta--btn" data-ir="#/rutas/' + r.id + '">' +
          '<div class="fila fila--sep"><span class="tarjeta__t">' + esc(r.nombre) + '</span>' +
          (hechas === r.paradas.length && r.paradas.length
            ? '<span class="et et--entr">lista</span>' : '') + '</div>' +
          '<p class="tarjeta__s">' + fechaLarga(r.fecha) + ' · ' +
          hechas + ' de ' + r.paradas.length + ' entregas</p></button>';
      });
    }
    h += '<button class="fab" data-ir="#/rutas/nueva" aria-label="Nueva ruta">' +
      '<svg aria-hidden="true"><use href="#i-plus"/></svg></button>';
    return h;
  };

  V.rutaForm = function () {
    if (!BD.clientes.length) {
      return '<div class="vacio"><p>Primero hay que tener clientes.</p>' +
        '<button class="btn" data-ir="#/clientes/nuevo">Agregar cliente</button></div>';
    }
    var zonas = [];
    BD.clientes.forEach(function (c) { if (c.zona && zonas.indexOf(c.zona) < 0) zonas.push(c.zona); });
    zonas.sort();

    var pendientes = {};
    BD.pedidos.forEach(function (p) {
      if (p.estado === 'pendiente') pendientes[p.clienteId] = true;
    });

    var h = '<form data-form-ruta>' +
      '<div class="campo"><label for="r-nom">Nombre de la ruta</label>' +
      '<input id="r-nom" name="nombre" placeholder="Ruta Alajuela" required /></div>' +
      '<div class="campo"><label for="r-fec">Día</label>' +
      '<input id="r-fec" name="fecha" type="date" value="' + hoyISO() + '" /></div>';

    if (zonas.length) {
      h += '<div class="campo"><label>Marcar rápido por zona</label><div class="filtros">' +
        zonas.map(function (z) {
          return '<button class="chip" type="button" data-marcar-zona="' + esc(z) + '">' + esc(z) + '</button>';
        }).join('') +
        '<button class="chip" type="button" data-marcar-pend>Con pedido pendiente</button>' +
        '</div></div>';
    }

    h += '<div class="seccion"><h3>Clientes de esta ruta</h3>';
    BD.clientes.slice().sort(function (a, b) { return a.nombre.localeCompare(b.nombre, 'es'); })
      .forEach(function (c) {
        h += '<label class="linea" style="cursor:pointer">' +
          '<div><span class="linea__n">' + esc(c.nombre) + '</span>' +
          '<br><span class="mut">' + esc(c.zona || 'Sin zona') +
          (pendientes[c.id] ? ' · tiene pedido pendiente' : '') +
          (c.lat == null ? ' · sin GPS' : '') + '</span></div>' +
          '<span></span>' +
          '<input type="checkbox" name="cli" value="' + esc(c.id) + '" ' +
          'data-zona-cli="' + esc(c.zona || '') + '" data-pend-cli="' + (pendientes[c.id] ? '1' : '') + '" ' +
          'style="width:24px;height:24px" /></label>';
      });
    h += '</div><button class="btn btn--g" type="submit">Crear y ordenar la ruta</button></form>';
    return h;
  };

  V.rutaDetalle = function (rid) {
    var r = null;
    BD.rutas.forEach(function (x) { if (x.id === rid) r = x; });
    if (!r) return '<div class="vacio"><p>Esa ruta ya no existe.</p></div>';

    var clis = r.paradas.map(function (p) { return cliente(p.clienteId); });
    var conGPS = clis.filter(function (c) { return c && c.lat != null; });
    var km = conGPS.length > 1 ? largoRuta(conGPS) : 0;
    var hechas = r.paradas.filter(function (p) { return p.hecho; }).length;

    var h = '<div class="tarjeta"><p class="tarjeta__t">' + esc(r.nombre) + '</p>' +
      '<p class="tarjeta__s">' + fechaLarga(r.fecha) + ' · ' + r.paradas.length + ' paradas' +
      (km ? ' · ~' + km.toFixed(1) + ' km en línea recta' : '') + '</p>' +
      '<p class="tarjeta__s">' + hechas + ' entregadas, ' + (r.paradas.length - hechas) + ' por hacer</p>' +
      '<div class="acciones">' +
      '<button class="btn btn--sec btn--sm" data-reordenar="' + esc(r.id) + '">' +
      '<svg aria-hidden="true"><use href="#i-magic"/></svg> Buscar orden más corto</button>' +
      '<button class="btn btn--sec btn--sm" data-compartir-ruta="' + esc(r.id) + '">' +
      '<svg aria-hidden="true"><use href="#i-share"/></svg> Compartir</button>' +
      '</div>' +
      '<div class="acciones"><button class="btn btn--wa btn--g" data-avisar-ruta="' +
      esc(r.id) + '"><svg aria-hidden="true"><use href="#i-wa"/></svg> ' +
      'Avisarles a los de esta ruta</button></div>' +
      '</div>';

    var urlMaps = urlMapsRuta(conGPS);
    if (urlMaps) {
      h += '<a class="btn btn--g btn--gold" href="' + esc(urlMaps) + '" target="_blank" rel="noopener" ' +
        'style="margin-bottom:.9rem"><svg aria-hidden="true"><use href="#i-pin"/></svg> ' +
        'Ver la ruta completa en Google Maps</a>';
    }

    if (conGPS.length < r.paradas.length) {
      h += '<p class="pista" style="margin-bottom:.8rem">' +
        (r.paradas.length - conGPS.length) + ' cliente(s) sin GPS quedan de último y no se pueden ' +
        'ordenar por cercanía. Tocá el cliente y guardale la ubicación.</p>';
    }

    r.paradas.forEach(function (p, i) {
      var c = cliente(p.clienteId);
      if (!c) return;
      h += '<div class="parada' + (p.hecho ? ' parada--hecha' : '') + '">' +
        '<span class="parada__n">' + (p.hecho ? '✓' : i + 1) + '</span><div>' +
        '<p class="parada__nom">' + esc(c.nombre) + '</p>' +
        '<p class="parada__dir">' + esc(c.direccion || c.zona || 'Sin dirección') + '</p>' +
        '<div class="parada__btns">' +
        '<a class="btn btn--waze btn--sm" href="' + esc(urlWaze(c)) + '" target="_blank" rel="noopener">' +
        '<svg aria-hidden="true"><use href="#i-nav"/></svg> Navegar</a>' +
        (c.tel ? '<a class="btn btn--wa btn--sm" href="https://wa.me/506' +
          esc(c.tel.replace(/\D/g, '').slice(-8)) + '" target="_blank" rel="noopener">' +
          '<svg aria-hidden="true"><use href="#i-wa"/></svg></a>' : '') +
        '<button class="btn btn--sm ' + (p.hecho ? 'btn--sec' : 'btn--ok') + '" ' +
        'data-parada="' + esc(r.id) + '|' + esc(p.clienteId) + '">' +
        (p.hecho ? 'Desmarcar' : 'Entregado') + '</button>' +
        '</div></div></div>';
    });
    return h;
  };

  function textoRuta(r) {
    var t = r.nombre + ' — ' + fechaLarga(r.fecha) + '\n\n';
    r.paradas.forEach(function (p, i) {
      var c = cliente(p.clienteId);
      if (!c) return;
      t += (i + 1) + '. ' + c.nombre + '\n';
      if (c.direccion) t += '   ' + c.direccion + '\n';
      if (c.tel) t += '   Tel: ' + c.tel + '\n';
      t += '   ' + urlWaze(c) + '\n\n';
    });
    return t;
  }

  /* ---------- Ferias -----------------------------------------------------
     En una feria no hay clientes con nombre: hay gente que pasa, prueba y
     compra. Lo que se necesita es una caja rápida —tocar productos, cobrar,
     siguiente— y al final saber cuánto se vendió y si valió la pena el día.
     ---------------------------------------------------------------------- */

  var cajaFeria = {};   // slug -> cantidad, lo que lleva el cliente de turno

  function totalCaja() {
    var t = 0;
    CATALOGO.forEach(function (p) { t += (cajaFeria[p.slug] || 0) * p.precio; });
    return t;
  }

  V.feria = function () {
    var f = feriaActiva();

    if (!f) {
      var pasadas = BD.ferias.slice().sort(function (a, b) {
        return b.fecha.localeCompare(a.fecha);
      });
      var h = '<form data-form-feria><div class="campo">' +
        '<label for="fe-nom">¿En qué feria está?</label>' +
        '<input id="fe-nom" name="nombre" placeholder="Feria La Verbena" required /></div>' +
        '<div class="campo"><label for="fe-lug">Lugar</label>' +
        '<input id="fe-lug" name="lugar" placeholder="Plaza Real Alajuela" /></div>' +
        '<div class="campo"><label for="fe-fec">Día</label>' +
        '<input id="fe-fec" name="fecha" type="date" value="' + hoyISO() + '" /></div>' +
        '<button class="btn btn--g btn--gold" type="submit">Abrir la caja</button></form>';

      if (pasadas.length) {
        h += '<div class="seccion" style="margin-top:1.6rem"><h3>Ferias anteriores</h3>';
        pasadas.forEach(function (x) {
          var v = ventasFeria(x.id).reduce(function (s, p) { return s + totalPedido(p); }, 0);
          var g = gastosFeria(x.id).reduce(function (s, y) { return s + y.monto; }, 0);
          h += '<div class="tarjeta"><div class="fila fila--sep">' +
            '<div class="crece"><p class="tarjeta__t">' + esc(x.nombre) + '</p>' +
            '<p class="tarjeta__s">' + fechaCorta(x.fecha) + ' · ' +
            ventasFeria(x.id).length + ' ventas' + (g ? ' · gastos ' + money(g) : '') + '</p></div>' +
            '<b style="color:var(--ok)">' + money(v - g) + '</b></div></div>';
        });
        h += '</div>';
      }
      return h;
    }

    // Caja abierta
    var vendido = ventasFeria(f.id).reduce(function (s, p) { return s + totalPedido(p); }, 0);
    var nVentas = ventasFeria(f.id).length;
    var gastoF = gastosFeria(f.id).reduce(function (s, g) { return s + g.monto; }, 0);

    var h2 = '<div class="seccion"><div class="cifras">' +
      '<div class="cifra cifra--ok"><b>' + money(vendido) + '</b><span>vendido hoy</span></div>' +
      '<div class="cifra"><b>' + nVentas + '</b><span>ventas</span></div>' +
      '<div class="cifra"><b>' + money(nVentas ? vendido / nVentas : 0) + '</b><span>promedio</span></div>' +
      '<div class="cifra' + (vendido - gastoF >= 0 ? ' cifra--ok' : ' cifra--bad') + '"><b>' +
      money(vendido - gastoF) + '</b><span>neto del día</span></div>' +
      '</div></div>';

    h2 += '<div class="seccion"><h3>Caja</h3>';
    CATALOGO.forEach(function (p) {
      var n = cajaFeria[p.slug] || 0;
      h2 += '<div class="linea"><div><span class="linea__n">' + esc(p.nombre) + '</span>' +
        '<br><span class="mut">' + money(p.precio) + '</span></div>' +
        '<div class="contador">' +
        '<button type="button" data-caja="-" data-slug="' + esc(p.slug) + '" aria-label="Quitar uno">−</button>' +
        '<span data-cn="' + esc(p.slug) + '">' + n + '</span>' +
        '<button type="button" data-caja="+" data-slug="' + esc(p.slug) + '" aria-label="Agregar uno">+</button>' +
        '</div><b data-cs="' + esc(p.slug) + '">' + (n ? money(n * p.precio) : '') + '</b></div>';
    });
    h2 += '<div class="total"><span>A cobrar</span><span data-ctotal>' + money(totalCaja()) + '</span></div>';
    h2 += '<div class="acciones">' +
      '<button class="btn btn--ok btn--g" data-cobrar-feria>Cobrar y seguir</button></div>';
    h2 += '<div class="acciones">' +
      '<button class="btn btn--sec btn--sm" data-rapido>Anotar este cliente</button>' +
      '<button class="btn btn--sec btn--sm" data-gasto-feria>Anotar gasto de la feria</button>' +
      '<button class="btn btn--mal btn--sm" data-cerrar-feria>Cerrar la feria</button>' +
      '</div></div>';

    if (nVentas) {
      var porProd = {};
      ventasFeria(f.id).forEach(function (p) {
        (p.lineas || []).forEach(function (l) {
          porProd[l.nombre] = (porProd[l.nombre] || 0) + l.cant;
        });
      });
      h2 += '<div class="seccion"><h3>Lo que se ha vendido</h3><div class="tarjeta">';
      Object.keys(porProd).sort(function (a, b) { return porProd[b] - porProd[a]; })
        .forEach(function (k) {
          h2 += '<div class="linea"><span class="linea__n">' + esc(k) + '</span>' +
            '<span></span><b>' + porProd[k] + '</b></div>';
        });
      h2 += '</div></div>';
    }
    return h2;
  };

  /* ---------- Gastos ----------------------------------------------------- */
  var CATS_GASTO = ['Ingredientes', 'Frascos y empaque', 'Etiquetas', 'Combustible',
                    'Feria', 'Publicidad', 'Otro'];

  V.gastos = function () {
    var lista = BD.gastos.slice().sort(function (a, b) { return b.fecha.localeCompare(a.fecha); });
    var mes = gastos(inicioMes());
    var h = '<div class="seccion"><div class="cifras">' +
      '<div class="cifra cifra--bad"><b>' + money(mes) + '</b><span>gastos este mes</span></div>' +
      '<div class="cifra"><b>' + money(gastos(inicioSemana())) + '</b><span>esta semana</span></div>' +
      '</div></div>';

    if (!lista.length) {
      h += '<div class="vacio"><p>Sin gastos registrados.</p>' +
        '<button class="btn" data-ir="#/gastos/nuevo">Anotar un gasto</button></div>';
    } else {
      lista.forEach(function (g) {
        h += '<div class="tarjeta"><div class="fila fila--sep">' +
          '<div class="crece"><p class="tarjeta__t">' + esc(g.categoria) + '</p>' +
          '<p class="tarjeta__s">' + fechaCorta(g.fecha) +
          (g.descripcion ? ' · ' + esc(g.descripcion) : '') + '</p></div>' +
          '<b>' + money(g.monto) + '</b>' +
          '<button class="icono" data-borrar-gasto="' + esc(g.id) + '" aria-label="Borrar">' +
          '<svg aria-hidden="true"><use href="#i-trash"/></svg></button>' +
          '</div></div>';
      });
    }
    h += '<button class="fab" data-ir="#/gastos/nuevo" aria-label="Nuevo gasto">' +
      '<svg aria-hidden="true"><use href="#i-plus"/></svg></button>';
    return h;
  };

  V.gastoForm = function () {
    return '<form data-form-gasto>' +
      '<div class="campo"><label for="g-mon">Monto *</label>' +
      '<input id="g-mon" name="monto" type="number" inputmode="numeric" min="0" required /></div>' +
      '<div class="campo"><label for="g-cat">Categoría</label><select id="g-cat" name="categoria">' +
      CATS_GASTO.map(function (c) { return '<option>' + esc(c) + '</option>'; }).join('') +
      '</select></div>' +
      '<div class="campo"><label for="g-fec">Fecha</label>' +
      '<input id="g-fec" name="fecha" type="date" value="' + hoyISO() + '" /></div>' +
      '<div class="campo"><label for="g-des">Descripción</label>' +
      '<input id="g-des" name="descripcion" /></div>' +
      '<button class="btn btn--g" type="submit">Guardar gasto</button></form>';
  };

  V.stock = function () {
    var valor = CATALOGO.reduce(function (s2, p) { return s2 + hay(p.slug) * p.precio; }, 0);
    var unidades = CATALOGO.reduce(function (s2, p) { return s2 + hay(p.slug); }, 0);

    var h = '<div class="seccion"><div class="cifras">' +
      '<div class="cifra"><b>' + unidades + '</b><span>frascos en total</span></div>' +
      '<div class="cifra"><b>' + money(valor) + '</b><span>valor a precio de venta</span></div>' +
      '</div></div>';

    h += '<p class="mut">Se descuenta solo cuando se vende. Si entró producción, ' +
      'sumala acá con el más.</p>';

    CATALOGO.forEach(function (p) {
      var n = hay(p.slug);
      h += '<div class="linea"><div><span class="linea__n">' + esc(p.nombre) + '</span>' +
        '<br><span class="mut">' + money(p.precio) + '</span></div>' +
        '<div class="contador">' +
        '<button type="button" data-stock="-" data-slug="' + esc(p.slug) + '" ' +
        'aria-label="Quitar uno">−</button>' +
        '<span data-sn="' + esc(p.slug) + '" style="color:' +
        (n <= 0 ? 'var(--bad)' : n <= 3 ? 'var(--warn)' : 'inherit') + '">' + n + '</span>' +
        '<button type="button" data-stock="+" data-slug="' + esc(p.slug) + '" ' +
        'aria-label="Agregar uno">+</button>' +
        '</div>' +
        '<button class="btn btn--sec btn--sm" data-lote="' + esc(p.slug) + '">+ lote</button>' +
        '</div>';
    });
    return h;
  };

  /* ---------- Resumen ---------------------------------------------------- */
  var periodo = 'mes';

  V.resumen = function () {
    var desde = periodo === 'mes' ? inicioMes()
      : periodo === 'semana' ? inicioSemana() : '0000-01-01';
    var v = ventas(desde), g = gastos(desde), dif = v - g;

    var h = '<div class="filtros">' +
      [['semana', 'Esta semana'], ['mes', 'Este mes'], ['todo', 'Todo']].map(function (p) {
        return '<button class="chip" aria-pressed="' + (periodo === p[0]) +
          '" data-per="' + p[0] + '">' + p[1] + '</button>';
      }).join('') + '</div>';

    h += '<div class="cifras seccion">' +
      '<div class="cifra cifra--ok"><b>' + money(v) + '</b><span>ventas</span></div>' +
      '<div class="cifra cifra--bad"><b>' + money(g) + '</b><span>gastos</span></div>' +
      '<div class="cifra' + (dif >= 0 ? ' cifra--ok' : ' cifra--bad') + '"><b>' + money(dif) +
      '</b><span>diferencia</span></div></div>';

    // Productos más vendidos en el período
    var porProd = {};
    BD.pedidos.forEach(function (p) {
      if (p.estado === 'cancelado' || !enRango(p.fecha, desde)) return;
      (p.lineas || []).forEach(function (l) {
        if (!porProd[l.nombre]) porProd[l.nombre] = { cant: 0, monto: 0 };
        porProd[l.nombre].cant += l.cant;
        porProd[l.nombre].monto += l.cant * l.precio;
      });
    });
    var prods = Object.keys(porProd).map(function (k) {
      return { nombre: k, cant: porProd[k].cant, monto: porProd[k].monto };
    }).sort(function (a, b) { return b.monto - a.monto; });

    if (prods.length) {
      h += '<div class="seccion"><h3>Lo que más se vendió</h3><div class="tarjeta">';
      prods.slice(0, 8).forEach(function (p) {
        h += '<div class="linea"><span class="linea__n">' + esc(p.nombre) + '</span>' +
          '<span class="mut">' + p.cant + ' u</span><b>' + money(p.monto) + '</b></div>';
      });
      h += '</div></div>';
    }

    // Mejores clientes
    var porCli = {};
    BD.pedidos.forEach(function (p) {
      if (p.estado === 'cancelado' || !enRango(p.fecha, desde)) return;
      porCli[p.clienteId] = (porCli[p.clienteId] || 0) + totalPedido(p);
    });
    var clis = Object.keys(porCli).map(function (k) { return { id: k, monto: porCli[k] }; })
      .sort(function (a, b) { return b.monto - a.monto; });
    if (clis.length) {
      h += '<div class="seccion"><h3>Mejores clientes</h3><div class="tarjeta">';
      clis.slice(0, 8).forEach(function (c) {
        h += '<div class="linea"><span class="linea__n">' + esc(nombreCliente(c.id)) + '</span>' +
          '<span></span><b>' + money(c.monto) + '</b></div>';
      });
      h += '</div></div>';
    }

    // Cuánto entró por cada vía, para cuadrar caja contra banco.
    var porVia = {};
    BD.pedidos.forEach(function (p) {
      if (p.estado === 'cancelado') return;
      (p.pagos || []).forEach(function (x) {
        if (!enRango(x.fecha, desde)) return;
        porVia[x.metodo] = (porVia[x.metodo] || 0) + x.monto;
      });
    });
    var vias = Object.keys(porVia).sort(function (a, b) { return porVia[b] - porVia[a]; });
    var totalCobrado = vias.reduce(function (s2, k) { return s2 + porVia[k]; }, 0);

    h += '<div class="seccion"><h3>Cómo entró la plata</h3>';
    if (!vias.length) {
      h += '<div class="vacio"><p>Todavía no hay pagos registrados en este período.</p></div>';
    } else {
      h += '<div class="tarjeta">';
      vias.forEach(function (k) {
        var pct = Math.round(porVia[k] / totalCobrado * 100);
        h += '<div class="linea"><span class="linea__n">' + esc(k) + '</span>' +
          '<span class="mut">' + pct + '%</span><b>' + money(porVia[k]) + '</b></div>';
      });
      h += '<div class="total"><span>Cobrado</span><span>' + money(totalCobrado) + '</span></div>';
      h += '</div>';
      var pendiente = v - totalCobrado;
      if (pendiente > 0) {
        h += '<p class="pista">De ' + money(v) + ' vendidos, faltan por cobrar <b>' +
          money(pendiente) + '</b>.</p>';
      }
    }
    h += '</div>';

    h += '<div class="seccion"><h3>Respaldo</h3>' +
      '<div class="tarjeta"><p class="tarjeta__s">Los datos viven solo en este teléfono. ' +
      'Si se borran los datos del navegador o se cambia de aparato, se pierden. ' +
      'Guardá un respaldo seguido: el archivo se puede mandar por WhatsApp o correo.</p>' +
      '<div class="acciones">' +
      '<button class="btn btn--sec btn--sm" data-exportar>' +
      '<svg aria-hidden="true"><use href="#i-down"/></svg> Bajar respaldo</button>' +
      '<button class="btn btn--sec btn--sm" data-importar>' +
      '<svg aria-hidden="true"><use href="#i-up"/></svg> Restaurar</button>' +
      '</div>' +
      '<p class="pista">' + BD.clientes.length + ' clientes · ' + BD.pedidos.length +
      ' pedidos · ' + BD.gastos.length + ' gastos · ' + BD.rutas.length + ' rutas</p>' +
      '</div></div>';

    var tieneClave = !!claveGuardada();
    h += '<div class="seccion"><h3>Clave de entrada</h3><div class="tarjeta">' +
      '<p class="tarjeta__s">' + (tieneClave
        ? 'La app pide clave al abrir.'
        : 'La app abre directo. Si querés, podés ponerle una clave para que ' +
          'nadie más la abra si le prestás el teléfono.') + '</p>' +
      '<div class="acciones">' + (tieneClave
        ? '<button class="btn btn--sec btn--sm" data-quitar-clave>Quitar la clave</button>'
        : '<button class="btn btn--sec btn--sm" data-poner-clave>Poner una clave</button>') +
      '</div></div></div>';
    return h;
  };

  /* =======================================================================
     ENRUTADOR
     ===================================================================== */

  var TITULOS = {
    hoy: 'Hoy', clientes: 'Clientes', pedidos: 'Pedidos',
    rutas: 'Rutas', dinero: 'Dinero', gastos: 'Gastos'
  };

  // Qué mitad de "Dinero" se está viendo.
  var panelDinero = 'resumen';

  function pintar() {
    var ruta = (location.hash || '#/hoy').replace(/^#\//, '').split('/');
    var sec = ruta[0] || 'hoy', arg = ruta[1], sub = ruta[2];
    var html = '', titulo = TITULOS[sec] || 'CARLOUIS', atras = false;

    if (sec === 'hoy') html = V.hoy();
    else if (sec === 'clientes') {
      if (arg === 'nuevo') { html = V.clienteForm(); titulo = 'Nuevo cliente'; atras = true; }
      else if (arg && sub === 'editar') { html = V.clienteForm(arg); titulo = 'Editar cliente'; atras = true; }
      else if (arg) { html = V.clienteDetalle(arg); titulo = nombreCliente(arg); atras = true; }
      else html = V.clientes();
    } else if (sec === 'pedidos') {
      if (arg === 'nuevo') { html = V.pedidoForm(); titulo = 'Nuevo pedido'; atras = true; }
      else if (arg) { html = V.pedidoDetalle(arg); titulo = 'Pedido'; atras = true; }
      else html = V.pedidos();
    } else if (sec === 'rutas') {
      if (arg === 'nueva') { html = V.rutaForm(); titulo = 'Nueva ruta'; atras = true; }
      else if (arg) { html = V.rutaDetalle(arg); titulo = 'Ruta'; atras = true; }
      else html = V.rutas();
    } else if (sec === 'gastos') {
      if (arg === 'nuevo') { html = V.gastoForm(); titulo = 'Nuevo gasto'; atras = true; }
      else { location.replace('#/dinero'); return; }
    } else if (sec === 'feria') {
      html = V.feria();
      var fa = feriaActiva();
      titulo = fa ? fa.nombre : 'Feria';
      atras = true;
    } else if (sec === 'dinero') {
      html = '<div class="subtabs" style="grid-template-columns:1fr 1fr 1fr">' +
        '<button class="subtab" aria-pressed="' + (panelDinero === 'resumen') +
        '" data-panel="resumen">Resumen</button>' +
        '<button class="subtab" aria-pressed="' + (panelDinero === 'gastos') +
        '" data-panel="gastos">Gastos</button>' +
        '<button class="subtab" aria-pressed="' + (panelDinero === 'stock') +
        '" data-panel="stock">Inventario</button></div>' +
        (panelDinero === 'gastos' ? V.gastos()
         : panelDinero === 'stock' ? V.stock() : V.resumen());
    } else html = V.hoy();

    vista.innerHTML = html;
    $('[data-titulo]').textContent = titulo;
    $('[data-volver]').hidden = !atras;
    window.scrollTo(0, 0);

    Array.prototype.forEach.call(document.querySelectorAll('.tab'), function (t) {
      var destino = sec === 'gastos' ? 'dinero' : sec;
      if (t.getAttribute('href') === '#/' + destino) t.setAttribute('aria-current', 'page');
      else t.removeAttribute('aria-current');
    });
  }

  window.addEventListener('hashchange', pintar);
  $('[data-volver]').addEventListener('click', function () { history.back(); });

  function ir(h) { location.hash = h; }

  /* =======================================================================
     EVENTOS
     ===================================================================== */

  document.addEventListener('click', function (e) {
    var t = e.target;

    var btnIr = t.closest('[data-ir]');
    if (btnIr) { ir(btnIr.getAttribute('data-ir')); return; }

    var z = t.closest('[data-zona]');
    if (z) { filtroZona = z.getAttribute('data-zona'); pintar(); return; }

    var fp = t.closest('[data-fped]');
    if (fp) { filtroPedido = fp.getAttribute('data-fped'); pintar(); return; }

    var per = t.closest('[data-per]');
    if (per) { periodo = per.getAttribute('data-per'); pintar(); return; }

    // Contador de cantidades en el pedido
    var cant = t.closest('[data-cant]');
    if (cant) {
      var slug = cant.getAttribute('data-slug');
      var prod = null;
      CATALOGO.forEach(function (p) { if (p.slug === slug) prod = p; });
      var n = borrador.lineas[slug] || 0;
      n = cant.getAttribute('data-cant') === '+' ? n + 1 : Math.max(0, n - 1);
      if (n) borrador.lineas[slug] = n; else delete borrador.lineas[slug];
      $('[data-n="' + slug + '"]').textContent = n;
      $('[data-sub="' + slug + '"]').textContent = n ? money(n * prod.precio) : '';
      $('[data-total]').textContent = money(totalBorrador());
      return;
    }

    // GPS del cliente
    if (t.closest('[data-gps]')) {
      var boton = t.closest('[data-gps]');
      boton.textContent = 'Buscando…';
      ubicacionActual().then(function (u) {
        boton.innerHTML = '<svg aria-hidden="true"><use href="#i-gps"/></svg> Usar mi ubicación';
        if (!u) return aviso('No se pudo leer el GPS. ¿Diste permiso?');
        $('#f-gps').value = u.lat.toFixed(6) + ',' + u.lng.toFixed(6);
        aviso('Ubicación guardada');
      });
      return;
    }

    // Marcar clientes por zona al armar una ruta
    var mz = t.closest('[data-marcar-zona]');
    if (mz) {
      var zona = mz.getAttribute('data-marcar-zona');
      Array.prototype.forEach.call(document.querySelectorAll('[name="cli"]'), function (ch) {
        if (ch.getAttribute('data-zona-cli') === zona) ch.checked = true;
      });
      aviso('Marcados los de ' + zona);
      return;
    }
    if (t.closest('[data-marcar-pend]')) {
      Array.prototype.forEach.call(document.querySelectorAll('[name="cli"]'), function (ch) {
        if (ch.getAttribute('data-pend-cli')) ch.checked = true;
      });
      aviso('Marcados los que tienen pedido pendiente');
      return;
    }

    // Estados de pedido
    var ent = t.closest('[data-entregado]');
    if (ent) {
      var pid = ent.getAttribute('data-entregado');
      BD.pedidos.forEach(function (p) { if (p.id === pid) p.estado = 'entregado'; });
      guardar(); pintar(); aviso('Marcado como entregado');
      return;
    }
    var pag = t.closest('[data-pagado]');
    if (pag) {
      var pid2 = pag.getAttribute('data-pagado');
      BD.pedidos.forEach(function (p) { if (p.id === pid2) p.pagado = true; });
      guardar(); pintar(); aviso('Marcado como pagado');
      return;
    }

    // Parada entregada
    var par = t.closest('[data-parada]');
    if (par) {
      var pr = par.getAttribute('data-parada').split('|');
      BD.rutas.forEach(function (r) {
        if (r.id !== pr[0]) return;
        r.paradas.forEach(function (p) { if (p.clienteId === pr[1]) p.hecho = !p.hecho; });
      });
      guardar(); pintar();
      return;
    }

    // Reordenar ruta
    var reo = t.closest('[data-reordenar]');
    if (reo) {
      var rid = reo.getAttribute('data-reordenar');
      reo.textContent = 'Ordenando…';
      ubicacionActual().then(function (origen) {
        var mejora = null;
        BD.rutas.forEach(function (r) {
          if (r.id !== rid) return;
          mejora = ordenarRuta(r, origen);
        });
        guardar(); pintar();
        aviso(frasePorMejora(mejora));
      });
      return;
    }

    // Compartir ruta
    var comp = t.closest('[data-compartir-ruta]');
    if (comp) {
      var rid2 = comp.getAttribute('data-compartir-ruta'), ruta = null;
      BD.rutas.forEach(function (r) { if (r.id === rid2) ruta = r; });
      if (!ruta) return;
      var txt = textoRuta(ruta);
      if (navigator.share) {
        navigator.share({ title: ruta.nombre, text: txt }).catch(function () {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(txt).then(function () { aviso('Ruta copiada'); });
      }
      return;
    }

    // Borrados
    var bc = t.closest('[data-borrar-cliente]');
    if (bc) {
      var cid = bc.getAttribute('data-borrar-cliente');
      var usos = BD.pedidos.filter(function (p) { return p.clienteId === cid; }).length;
      if (!confirm('¿Borrar este cliente?' + (usos ? '\n\nTiene ' + usos + ' pedido(s) en el historial. Los pedidos NO se borran.' : ''))) return;
      BD.clientes = BD.clientes.filter(function (c) { return c.id !== cid; });
      BD.rutas.forEach(function (r) {
        r.paradas = r.paradas.filter(function (p) { return p.clienteId !== cid; });
      });
      guardar(); ir('#/clientes'); aviso('Cliente borrado');
      return;
    }
    var bp = t.closest('[data-borrar-pedido]');
    if (bp) {
      if (!confirm('¿Borrar este pedido?')) return;
      var pid3 = bp.getAttribute('data-borrar-pedido');
      BD.pedidos.forEach(function (p) { if (p.id === pid3) moverStock(p.lineas, 1); });
      BD.pedidos = BD.pedidos.filter(function (p) { return p.id !== pid3; });
      guardar(); ir('#/pedidos'); aviso('Pedido borrado');
      return;
    }
    var bg = t.closest('[data-borrar-gasto]');
    if (bg) {
      if (!confirm('¿Borrar este gasto?')) return;
      var gid = bg.getAttribute('data-borrar-gasto');
      BD.gastos = BD.gastos.filter(function (g) { return g.id !== gid; });
      guardar(); pintar();
      return;
    }

    // Sub-pestañas de Dinero
    var pan = t.closest('[data-panel]');
    if (pan) { panelDinero = pan.getAttribute('data-panel'); pintar(); return; }

    // Método de pago dentro de la hoja
    var met = t.closest('[data-metodo]');
    if (met) {
      Array.prototype.forEach.call(
        met.parentNode.querySelectorAll('[data-metodo]'),
        function (b) { b.setAttribute('aria-pressed', b === met); });
      return;
    }

    // Registrar un pago (total o abono)
    var cob = t.closest('[data-cobrar]');
    if (cob) { registrarPago(cob.getAttribute('data-cobrar')); return; }

    var bpg = t.closest('[data-borrar-pago]');
    if (bpg) {
      var pp = bpg.getAttribute('data-borrar-pago').split('|');
      BD.pedidos.forEach(function (p) {
        if (p.id === pp[0] && p.pagos) p.pagos.splice(Number(pp[1]), 1);
      });
      guardar(); pintar();
      return;
    }

    // Caja de feria: subir y bajar cantidades
    var cj = t.closest('[data-caja]');
    if (cj) {
      var cs = cj.getAttribute('data-slug'), cp = null;
      CATALOGO.forEach(function (p) { if (p.slug === cs) cp = p; });
      var cn = cajaFeria[cs] || 0;
      cn = cj.getAttribute('data-caja') === '+' ? cn + 1 : Math.max(0, cn - 1);
      if (cn) cajaFeria[cs] = cn; else delete cajaFeria[cs];
      $('[data-cn="' + cs + '"]').textContent = cn;
      $('[data-cs="' + cs + '"]').textContent = cn ? money(cn * cp.precio) : '';
      $('[data-ctotal]').textContent = money(totalCaja());
      return;
    }

    if (t.closest('[data-gps-rapido]')) {
      var bg2 = t.closest('[data-gps-rapido]');
      bg2.textContent = 'Buscando…';
      ubicacionActual().then(function (u) {
        if (!u) {
          bg2.innerHTML = '<svg aria-hidden="true"><use href="#i-gps"/></svg> Guardar dónde estoy ahora';
          return aviso('No se pudo leer el GPS');
        }
        $('#cr-c').value = u.lat.toFixed(6) + ',' + u.lng.toFixed(6);
        bg2.innerHTML = '<svg aria-hidden="true"><use href="#i-check"/></svg> Ubicación guardada';
        bg2.className = 'btn btn--ok btn--g';
      });
      return;
    }

    var rec = t.closest('[data-recordar]');
    if (rec) {
      var cr2 = cliente(rec.getAttribute('data-recordar'));
      if (!cr2 || !cr2.tel) return;
      var sg3 = seguimiento(cr2);
      var msg = 'Buenas ' + cr2.nombre + '! ¿Cómo va todo? Hace ' + sg3.dias +
        ' días del último pedido, ¿le llevo algo esta semana?';
      window.open('https://wa.me/506' + cr2.tel.replace(/\D/g, '').slice(-8) +
                  '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
      return;
    }

    if (t.closest('[data-rapido]')) { clienteRapido(); return; }

    var avr = t.closest('[data-avisar-ruta]');
    if (avr) { avisarRuta(avr.getAttribute('data-avisar-ruta')); return; }

    var msz = t.closest('[data-mensajes]');
    if (msz) { hojaMensajes(msz.getAttribute('data-mensajes')); return; }

    var plt = t.closest('[data-plantilla]');
    if (plt) {
      $('#ms-t').value = hojaMensajes._plantillas[Number(plt.getAttribute('data-plantilla'))];
      return;
    }

    var env = t.closest('[data-enviar]');
    if (env) {
      var cid2 = env.getAttribute('data-enviar');
      var c2 = cliente(cid2);
      if (!c2 || !c2.tel) return;
      var texto = ($('#ms-t') || {}).value || '';
      window.open('https://wa.me/506' + c2.tel.replace(/\D/g, '').slice(-8) +
                  '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
      yaEnviados[cid2] = true;
      var fila = document.querySelector('[data-msg-fila="' + cid2 + '"]');
      if (fila) {
        fila.style.opacity = '.5';
        env.className = 'btn btn--sec btn--sm';
        env.innerHTML = 'Enviado';
      }
      return;
    }

    var stk = t.closest('[data-stock]');
    if (stk) {
      var ss = stk.getAttribute('data-slug');
      BD.stock[ss] = hay(ss) + (stk.getAttribute('data-stock') === '+' ? 1 : -1);
      guardar();
      var celda = $('[data-sn="' + ss + '"]');
      celda.textContent = hay(ss);
      celda.style.color = hay(ss) <= 0 ? 'var(--bad)'
        : hay(ss) <= 3 ? 'var(--warn)' : 'inherit';
      return;
    }

    var lot = t.closest('[data-lote]');
    if (lot) {
      var ls = lot.getAttribute('data-lote');
      var cuanto = prompt('¿Cuántos frascos entraron?', '12');
      if (cuanto === null) return;
      var cn2 = Number(String(cuanto).replace(/[^0-9]/g, ''));
      if (!cn2) return;
      BD.stock[ls] = hay(ls) + cn2;
      guardar(); pintar(); aviso('Entraron ' + cn2);
      return;
    }

    if (t.closest('[data-cobrar-feria]')) { cobrarFeria(); return; }
    if (t.closest('[data-gasto-feria]')) { gastoDeFeria(); return; }
    if (t.closest('[data-cerrar-feria]')) { cerrarFeria(); return; }

    // Ruta rápida: "voy para Alajuela"
    var rr = t.closest('[data-ruta-rapida]');
    if (rr) { rutaRapida(rr.getAttribute('data-ruta-rapida')); return; }

    // Respaldo
    if (t.closest('[data-exportar]')) { exportar(); return; }
    if (t.closest('[data-importar]')) { importar(); return; }
  });

  document.addEventListener('input', function (e) {
    if (e.target.matches('[data-buscar-cliente]')) {
      buscaCliente = e.target.value;
      var pos = e.target.selectionStart;
      pintar();
      var campo = $('[data-buscar-cliente]');
      if (campo) { campo.focus(); campo.setSelectionRange(pos, pos); }
    }
  });

  /* ---------- envío de formularios --------------------------------------- */

  document.addEventListener('submit', function (e) {
    var f = e.target;

    if (f.matches('[data-form-cliente]')) {
      e.preventDefault();
      var cid = f.getAttribute('data-id');
      var co = coordsDeTexto(f.coords.value);
      var datos = {
        nombre: f.nombre.value.trim(),
        tel: f.tel.value.trim(),
        zona: f.zona.value.trim(),
        direccion: f.direccion.value.trim(),
        notas: f.notas.value.trim(),
        lat: co ? co.lat : null,
        lng: co ? co.lng : null
      };
      if (!datos.nombre) return;
      if (f.coords.value.trim() && !co) {
        aviso('No entendí esa ubicación; se guardó sin GPS');
      }
      if (cid) {
        BD.clientes.forEach(function (c) {
          if (c.id === cid) Object.keys(datos).forEach(function (k) { c[k] = datos[k]; });
        });
        guardar(); ir('#/clientes/' + cid);
      } else {
        datos.id = id();
        datos.creado = hoyISO();
        BD.clientes.push(datos);
        guardar(); ir('#/clientes/' + datos.id);
      }
      aviso('Cliente guardado');
      return;
    }

    if (f.matches('[data-form-pedido]')) {
      e.preventDefault();
      var lineas = [];
      CATALOGO.forEach(function (p) {
        var n = borrador.lineas[p.slug] || 0;
        if (n) lineas.push({ slug: p.slug, nombre: p.nombre, precio: p.precio, cant: n });
      });
      if (!lineas.length) return aviso('Agregá al menos un producto');
      var ped = {
        id: id(), clienteId: f.clienteId.value, fecha: f.fecha.value || hoyISO(),
        lineas: lineas, notas: f.notas.value.trim(), estado: 'pendiente', pagado: false
      };
      BD.pedidos.push(ped);
      moverStock(lineas, -1);
      borrador = null;
      guardar(); ir('#/pedidos/' + ped.id); aviso('Pedido guardado');
      return;
    }

    if (f.matches('[data-form-ruta]')) {
      e.preventDefault();
      var ids = Array.prototype.slice.call(f.querySelectorAll('[name="cli"]:checked'))
        .map(function (ch) { return ch.value; });
      if (!ids.length) return aviso('Marcá al menos un cliente');
      var r = {
        id: id(), nombre: f.nombre.value.trim() || 'Ruta', fecha: f.fecha.value || hoyISO(),
        paradas: ids.map(function (cid) { return { clienteId: cid, hecho: false }; })
      };
      BD.rutas.push(r);
      ubicacionActual().then(function (origen) {
        var mejora = ordenarRuta(r, origen);
        guardar(); ir('#/rutas/' + r.id);
        aviso(frasePorMejora(mejora));
      });
      return;
    }

    if (f.matches('[data-form-pago]')) {
      e.preventDefault();
      var m = Number(f.monto.value);
      if (!m || m <= 0) return aviso('Poné un monto');
      var sel = f.querySelector('[data-metodo][aria-pressed="true"]');
      aplicarPago(f.getAttribute('data-pedido'), m,
                  sel ? sel.getAttribute('data-metodo') : 'Otro');
      return;
    }

    if (f.matches('[data-form-rapido]')) {
      e.preventDefault();
      var nom = f.nombre.value.trim();
      if (!nom) return;
      var cr = coordsDeTexto(f.coords.value);
      var nuevo = {
        id: id(), nombre: nom, tel: f.tel.value.trim(), zona: f.zona.value.trim(),
        direccion: '', notas: '', creado: hoyISO(),
        lat: cr ? cr.lat : null, lng: cr ? cr.lng : null
      };
      BD.clientes.push(nuevo);
      guardar(); cerrarHoja(); pintar();
      aviso('Cliente guardado' + (cr ? ' con ubicación' : ''));
      return;
    }

    if (f.matches('[data-form-feria]')) {
      e.preventDefault();
      BD.ferias.push({
        id: id(), nombre: f.nombre.value.trim() || 'Feria',
        lugar: f.lugar.value.trim(), fecha: f.fecha.value || hoyISO(), cerrada: false
      });
      cajaFeria = {};
      guardar(); pintar(); aviso('Caja abierta');
      return;
    }

    if (f.matches('[data-form-cobro-feria]')) {
      e.preventDefault();
      var selF = f.querySelector('[data-metodo][aria-pressed="true"]');
      aplicarCobroFeria(selF ? selF.getAttribute('data-metodo') : 'Efectivo');
      return;
    }

    if (f.matches('[data-form-gasto-feria]')) {
      e.preventDefault();
      var mf = Number(f.monto.value);
      if (!mf || mf <= 0) return aviso('Poné un monto');
      var fa2 = feriaActiva();
      BD.gastos.push({
        id: id(), monto: mf, categoria: 'Feria', fecha: hoyISO(),
        descripcion: f.descripcion.value.trim() || 'Gasto de feria',
        feriaId: fa2 ? fa2.id : null
      });
      guardar(); cerrarHoja(); pintar(); aviso('Gasto guardado');
      return;
    }

    if (f.matches('[data-form-gasto]')) {
      e.preventDefault();
      var monto = Number(f.monto.value);
      if (!monto || monto < 0) return aviso('Poné un monto');
      BD.gastos.push({
        id: id(), monto: monto, categoria: f.categoria.value,
        fecha: f.fecha.value || hoyISO(), descripcion: f.descripcion.value.trim()
      });
      guardar(); ir('#/gastos'); aviso('Gasto guardado');
      return;
    }
  });

  // Ordena las paradas por cercanía. Las que no tienen GPS quedan al final,
  // en el orden en que se marcaron: no hay forma de ordenarlas sin coordenadas.
  function ordenarRuta(r, origen) {
    var con = [], sin = [];
    r.paradas.forEach(function (p) {
      var c = cliente(p.clienteId);
      if (c && c.lat != null) con.push({ p: p, lat: c.lat, lng: c.lng });
      else sin.push(p);
    });
    var antes = con.length > 1 ? largoRuta(con, origen) : 0;
    if (con.length > 1) con = optimizar(con, origen);
    var despues = con.length > 1 ? largoRuta(con, origen) : 0;
    r.paradas = con.map(function (x) { return x.p; }).concat(sin);
    return { antes: antes, despues: despues, ahorro: antes - despues };
  }

  // Frase corta para decir si valió la pena reordenar.
  function frasePorMejora(m) {
    if (!m || m.despues <= 0) return 'Ruta guardada';
    if (m.ahorro > 0.3) {
      return 'Quedó ' + m.ahorro.toFixed(1) + ' km más corta (' +
             Math.round(m.ahorro / m.antes * 100) + '% menos)';
    }
    return 'Ya estaba en el mejor orden: ' + m.despues.toFixed(1) + ' km';
  }

  function registrarPago(pid) {
    var p = null;
    BD.pedidos.forEach(function (x) { if (x.id === pid) p = x; });
    if (!p) return;
    var falta = saldo(p);

    // Hoja con botones grandes en vez de prompt(): se usa con el dedo, de pie
    // y a veces con el cliente enfrente. Lo normal es "pagó todo", así que ese
    // botón va de primero y resuelve el caso en un solo toque.
    abrirHoja('Registrar pago', '' +
      '<p class="mut" style="margin-top:0">' + esc(nombreCliente(p.clienteId)) +
      ' · falta <b>' + money(falta) + '</b></p>' +
      '<form data-form-pago data-pedido="' + esc(p.id) + '">' +
      '<div class="campo"><label for="pg-monto">¿Cuánto le pagó?</label>' +
      '<input id="pg-monto" name="monto" type="number" inputmode="numeric" min="1" ' +
      'value="' + falta + '" /></div>' +
      '<div class="campo"><label>¿Cómo pagó?</label><div class="subtabs" ' +
      'style="grid-template-columns:1fr 1fr 1fr 1fr">' +
      ['SINPE', 'Efectivo', 'Tarjeta', 'Transfer.'].map(function (m, i) {
        return '<button class="subtab" type="button" data-metodo="' + esc(m) + '" ' +
          'aria-pressed="' + (i === 0) + '">' + esc(m) + '</button>';
      }).join('') + '</div></div>' +
      '<button class="btn btn--g btn--ok" type="submit">Guardar pago</button>' +
      '</form>');
  }

  function aplicarPago(pid, monto, metodo) {
    var p = null;
    BD.pedidos.forEach(function (x) { if (x.id === pid) p = x; });
    if (!p) return;
    if (!p.pagos) p.pagos = [];
    p.pagos.push({ fecha: hoyISO(), monto: monto, metodo: metodo });
    if (p.estado === 'pendiente') p.estado = 'entregado';
    p.pagado = estaPago(p);
    guardar();
    cerrarHoja();
    pintar();
    aviso(estaPago(p) ? 'Pagado completo' : 'Abono guardado, falta ' + money(saldo(p)));
  }

  function cobrarFeria() {
    var f = feriaActiva();
    if (!f) return;
    var lineas = [];
    CATALOGO.forEach(function (p) {
      var n = cajaFeria[p.slug] || 0;
      if (n) lineas.push({ slug: p.slug, nombre: p.nombre, precio: p.precio, cant: n });
    });
    if (!lineas.length) return aviso('Tocá los productos que lleva');
    var tot = totalCaja();

    abrirHoja('Cobrar ' + money(tot), '' +
      '<form data-form-cobro-feria>' +
      '<div class="campo"><label>¿Cómo paga?</label><div class="subtabs" ' +
      'style="grid-template-columns:1fr 1fr 1fr 1fr">' +
      ['Efectivo', 'SINPE', 'Tarjeta', 'Transfer.'].map(function (m, i) {
        return '<button class="subtab" type="button" data-metodo="' + esc(m) + '" ' +
          'aria-pressed="' + (i === 0) + '">' + esc(m) + '</button>';
      }).join('') + '</div></div>' +
      '<button class="btn btn--g btn--ok" type="submit">Listo, cobrado</button></form>');

    cobrarFeria._lineas = lineas;
    cobrarFeria._total = tot;
    cobrarFeria._feria = f.id;
  }

  function aplicarCobroFeria(metodo) {
    BD.pedidos.push({
      id: id(), clienteId: null, feriaId: cobrarFeria._feria,
      fecha: hoyISO(), lineas: cobrarFeria._lineas, notas: '',
      estado: 'entregado', pagado: true,
      pagos: [{ fecha: hoyISO(), monto: cobrarFeria._total, metodo: metodo }]
    });
    moverStock(cobrarFeria._lineas, -1);
    var cobrado = cobrarFeria._total;
    cajaFeria = {};
    guardar();
    cerrarHoja();
    pintar();
    aviso('Cobrado ' + money(cobrado));
  }

  function gastoDeFeria() {
    if (!feriaActiva()) return;
    abrirHoja('Gasto de la feria', '' +
      '<form data-form-gasto-feria>' +
      '<div class="campo"><label for="gf-m">Monto</label>' +
      '<input id="gf-m" name="monto" type="number" inputmode="numeric" min="1" required /></div>' +
      '<div class="campo"><label for="gf-d">¿De qué?</label>' +
      '<input id="gf-d" name="descripcion" placeholder="Alquiler del puesto" /></div>' +
      '<button class="btn btn--g" type="submit">Guardar</button></form>');
  }

  function cerrarFeria() {
    var f = feriaActiva();
    if (!f) return;
    var v = ventasFeria(f.id).reduce(function (s, p) { return s + totalPedido(p); }, 0);
    var g = gastosFeria(f.id).reduce(function (s, x) { return s + x.monto; }, 0);
    if (!confirm('¿Cerrar ' + f.nombre + '?' + String.fromCharCode(10, 10) +
                 'Vendido: ' + money(v) + String.fromCharCode(10) +
                 'Gastos: ' + money(g) + String.fromCharCode(10) +
                 'Neto: ' + money(v - g) + String.fromCharCode(10, 10) +
                 'Después de cerrar no se puede seguir cobrando en esta feria.')) return;
    f.cerrada = true;
    cajaFeria = {};
    guardar();
    ir('#/hoy');
    aviso('Feria cerrada. Neto ' + money(v - g));
  }

  var yaEnviados = {};

  function hojaMensajes(zona) {
    var lista = BD.clientes.filter(function (c) {
      return c.tel && (!zona || c.zona === zona);
    }).sort(function (a, b) { return a.nombre.localeCompare(b.nombre, 'es'); });
    if (!lista.length) return aviso('Ninguno de esos tiene teléfono');

    var plantillas = [
      'Buenas! Esta semana ando por ' + (zona || 'la zona') +
        '. ¿Le llevo algo? Tengo toda la línea disponible.',
      'Buenas! Ya tengo listo lote nuevo de salsas. ¿Le aparto?',
      'Buenas! Este sábado estamos en la feria de Plaza Real Alajuela, de 6 a 1. Ahí le espero.'
    ];

    abrirHoja('Mensaje a ' + lista.length + (zona ? ' de ' + zona : ''), '' +
      '<div class="campo"><label for="ms-t">Mensaje</label>' +
      '<textarea id="ms-t" style="min-height:96px">' + esc(plantillas[0]) + '</textarea></div>' +
      '<div class="filtros">' + plantillas.map(function (p, i) {
        return '<button class="chip" type="button" data-plantilla="' + i + '">Texto ' + (i + 1) + '</button>';
      }).join('') + '</div>' +
      '<p class="pista">WhatsApp abre un chat por persona: no hay forma de mandarle a ' +
      'todos de un solo toque. Acá van en fila y se marcan los que ya salieron.</p>' +
      '<div data-lista-msg>' + lista.map(function (c) {
        return '<div class="linea" data-msg-fila="' + esc(c.id) + '">' +
          '<span class="linea__n">' + esc(c.nombre) + '</span><span></span>' +
          '<button class="btn btn--wa btn--sm" data-enviar="' + esc(c.id) + '">' +
          '<svg aria-hidden="true"><use href="#i-wa"/></svg> Enviar</button></div>';
      }).join('') + '</div>');

    hojaMensajes._plantillas = plantillas;
  }

  function avisarRuta(rid) {
    var r = null;
    BD.rutas.forEach(function (x) { if (x.id === rid) r = x; });
    if (!r) return;

    var lista = r.paradas.map(function (p) { return cliente(p.clienteId); })
      .filter(function (c) { return c && c.tel; });
    if (!lista.length) return aviso('Ninguno de esta ruta tiene teléfono');

    var cuando = r.fecha === hoyISO() ? 'hoy'
      : r.fecha === maniana() ? 'mañana'
      : 'el ' + fechaLarga(r.fecha);

    var textos = [
      'Buenas! Voy a andar por su zona ' + cuando + '. ¿Le llevo algo? Avíseme y se lo aparto.',
      'Buenas! Le confirmo que ' + cuando + ' le paso dejando el pedido.',
      'Buenas! Ya voy en camino, en un rato estoy por allá.'
    ];

    abrirHoja('Avisar a ' + lista.length + ' clientes', '' +
      '<div class="campo"><label for="ms-t">Mensaje</label>' +
      '<textarea id="ms-t" style="min-height:96px">' + esc(textos[0]) + '</textarea></div>' +
      '<div class="filtros">' +
      '<button class="chip" type="button" data-plantilla="0">Antes de salir</button>' +
      '<button class="chip" type="button" data-plantilla="1">Confirmar entrega</button>' +
      '<button class="chip" type="button" data-plantilla="2">Ya voy llegando</button>' +
      '</div>' +
      '<p class="pista">Cada toque abre el chat con el texto puesto. Los que ya ' +
      'salieron quedan marcados.</p>' +
      '<div>' + lista.map(function (c) {
        return '<div class="linea" data-msg-fila="' + esc(c.id) + '">' +
          '<span class="linea__n">' + esc(c.nombre) + '</span><span></span>' +
          '<button class="btn btn--wa btn--sm" data-enviar="' + esc(c.id) + '">' +
          '<svg aria-hidden="true"><use href="#i-wa"/></svg> Avisar</button></div>';
      }).join('') + '</div>');

    hojaMensajes._plantillas = textos;
  }

  function maniana() {
    var d = new Date();
    d.setDate(d.getDate() + 1);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }

  function clienteRapido() {
    abrirHoja('Cliente nuevo, rápido', '' +
      '<form data-form-rapido>' +
      '<div class="campo"><label for="cr-n">Nombre</label>' +
      '<input id="cr-n" name="nombre" required autocomplete="off" /></div>' +
      '<div class="campo"><label for="cr-t">Teléfono</label>' +
      '<input id="cr-t" name="tel" type="tel" inputmode="tel" /></div>' +
      '<div class="campo"><label for="cr-z">Zona</label>' +
      '<input id="cr-z" name="zona" list="l-zonas" />' +
      '<datalist id="l-zonas">' + zonasSugeridas() + '</datalist></div>' +
      '<input type="hidden" name="coords" id="cr-c" />' +
      '<div class="acciones"><button class="btn btn--sec btn--g" type="button" data-gps-rapido>' +
      '<svg aria-hidden="true"><use href="#i-gps"/></svg> Guardar dónde estoy ahora</button></div>' +
      '<p class="pista">Si estás en la casa del cliente, tocá eso y la ruta ya lo va a poder ' +
      'ordenar. La dirección se la ponés después con calma.</p>' +
      '<button class="btn btn--g" type="submit">Guardar cliente</button></form>');
  }

  function rutaRapida(zona) {
    var ids = {};
    BD.pedidos.forEach(function (p) {
      if (p.estado !== 'pendiente') return;
      var c = cliente(p.clienteId);
      if (c && (c.zona || 'Sin zona') === zona) ids[c.id] = true;
    });
    var lista = Object.keys(ids);
    if (!lista.length) return aviso('Nadie pendiente en ' + zona);
    var r = {
      id: id(), nombre: 'Ruta ' + zona, fecha: hoyISO(),
      paradas: lista.map(function (cid) { return { clienteId: cid, hecho: false }; })
    };
    BD.rutas.push(r);
    aviso('Armando la ruta…');
    ubicacionActual().then(function (origen) {
      var mejora = ordenarRuta(r, origen);
      guardar(); ir('#/rutas/' + r.id);
      aviso(lista.length + ' paradas · ' + frasePorMejora(mejora));
    });
  }

  /* ---------- respaldo --------------------------------------------------- */

  function exportar() {
    var blob = new Blob([JSON.stringify(BD, null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'carlouis-respaldo-' + hoyISO() + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    aviso('Respaldo descargado');
  }

  function importar() {
    var inp = document.createElement('input');
    inp.type = 'file';
    inp.accept = 'application/json,.json';
    inp.addEventListener('change', function () {
      var file = inp.files && inp.files[0];
      if (!file) return;
      var lector = new FileReader();
      lector.onload = function () {
        try {
          var datos = JSON.parse(lector.result);
          if (!datos || !Array.isArray(datos.clientes)) throw new Error('formato');
          if (!confirm('Esto reemplaza TODO lo que hay ahora.\n\n' +
              'El respaldo trae ' + datos.clientes.length + ' clientes y ' +
              (datos.pedidos || []).length + ' pedidos.\n\n¿Seguir?')) return;
          BD = datos;
          ['clientes', 'pedidos', 'gastos', 'rutas', 'ferias'].forEach(function (k) {
            if (!Array.isArray(BD[k])) BD[k] = [];
          });
          guardar(); pintar(); aviso('Respaldo restaurado');
        } catch (err) {
          aviso('Ese archivo no es un respaldo válido');
        }
      };
      lector.readAsText(file);
    });
    inp.click();
  }

  /* ---------- clave de entrada -------------------------------------------
     Es un candado de pantalla, no una caja fuerte: los datos viven en este
     teléfono y quien sepa de programación puede verlos con las herramientas
     del navegador. Sirve para lo que sí pasa en la vida real —que alguien
     agarre el teléfono desbloqueado y se ponga a ver— y para eso alcanza.
     Viene apagada: si nunca se activa, la app abre directo.
     ---------------------------------------------------------------------- */

  var LLAVE_PIN = 'carlouis.control.clave';

  function claveGuardada() {
    try { return JSON.parse(localStorage.getItem(LLAVE_PIN) || 'null'); }
    catch (e) { return null; }
  }

  function pedirClave() {
    var capa = document.createElement('div');
    capa.className = 'candado';
    capa.innerHTML =
      '<form class="candado__caja" data-form-clave>' +
      '<img class="candado__logo" src="../assets/img/logo.png" alt="CARLOUIS" ' +
      'width="146" height="42" />' +
      '<label for="c-pin">Clave</label>' +
      '<input id="c-pin" type="password" inputmode="numeric" autocomplete="current-password" ' +
      'pattern="[0-9]*" required autofocus />' +
      '<button class="btn btn--g" type="submit">Entrar</button>' +
      '<p class="candado__err" data-err hidden>Clave incorrecta</p>' +
      '</form>';
    document.body.appendChild(capa);
    document.body.style.overflow = 'hidden';

    capa.addEventListener('submit', function (e) {
      e.preventDefault();
      var g = claveGuardada();
      var pin = capa.querySelector('#c-pin').value;
      var fallar = function () {
        capa.querySelector('[data-err]').hidden = false;
        capa.querySelector('#c-pin').value = '';
        capa.querySelector('#c-pin').focus();
      };
      // La prueba de verdad es si el descifrado funciona: una clave mala no
      // puede abrir los datos aunque el resumen coincidiera.
      derivar(pin, g.sal).then(function (llave) {
        return descifrarCon(llave).then(function (ok) {
          if (!ok) return fallar();
          LLAVE_AES = llave;
          capa.remove();
          document.body.style.overflow = '';
          arrancarApp();
        });
      }).catch(fallar);
    });
  }

  function ponerClave() {
    var pin = prompt('Clave nueva (solo números, 4 o más):');
    if (pin == null) return;
    pin = pin.trim();
    if (!/^\d{4,}$/.test(pin)) return aviso('Tiene que ser de 4 números o más');
    if (prompt('Repetila para confirmar:') !== pin) return aviso('No coinciden');
    var sal = b64(crypto.getRandomValues(new Uint8Array(16)));
    derivar(pin, sal).then(function (llave) {
      localStorage.setItem(LLAVE_PIN, JSON.stringify({ sal: sal }));
      LLAVE_AES = llave;
      guardar();            // reescribe todo, ahora cifrado
      pintar();
      aviso('Datos protegidos');
      alert('Listo: de acá en adelante los datos quedan cifrados en el teléfono. ' +
            'Ni abriendo el navegador por dentro se pueden leer sin la clave.\n\n' +
            'Anotá la clave en algún lado. Si se te olvida NO hay forma de ' +
            'recuperarla: habría que empezar de cero con el último respaldo.');
    });
  }

  function quitarClave() {
    var g = claveGuardada();
    if (!g) return;
    var pin = prompt('Escribí la clave actual para quitarla:');
    if (pin == null) return;
    derivar(pin.trim(), g.sal).then(function (llave) {
      return descifrarCon(llave).then(function (ok) {
        if (!ok) return aviso('Clave incorrecta');
        LLAVE_AES = null;
        localStorage.removeItem(LLAVE_PIN);
        guardar();          // vuelve a quedar en claro
        pintar();
        aviso('Clave quitada');
      });
    });
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-poner-clave]')) ponerClave();
    if (e.target.closest('[data-quitar-clave]')) quitarClave();
  });

  /* ---------- conexión y service worker ---------------------------------- */

  function estadoConexion() {
    $('[data-conexion]').hidden = navigator.onLine;
  }
  window.addEventListener('online', estadoConexion);
  window.addEventListener('offline', estadoConexion);

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('sw.js').catch(function () {});
    });
  }

  /* ---------- arranque --------------------------------------------------- */

  function arrancarApp() {
    estadoConexion();
    if (!location.hash) location.hash = '#/hoy';
    pintar();
  }

  cargar();
  if (claveGuardada() || estaCifrado()) pedirClave();
  else arrancarApp();
})();
