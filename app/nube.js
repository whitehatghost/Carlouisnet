/* =========================================================================
   CARLOUIS Control — sincronización entre teléfonos
   -------------------------------------------------------------------------
   Habla directo con Supabase por HTTP. No se usa la librería oficial a
   propósito: son ~120 KB para lo que acá son cuatro llamadas, y además
   obligaría a abrir la política de seguridad para cargar código de afuera.

   Cómo funciona, en corto:

     - Cada registro (cliente, pedido, gasto, ruta, feria, recordatorio) tiene
       su id y su marca de tiempo. Se suben los que cambiaron desde la última
       vez y se bajan los que cambiaron en el servidor.
     - Si el mismo registro cambió en dos teléfonos, gana el más reciente.
       Para este uso —cada quien cobra su venta, cada quien anota su cliente—
       eso no da problema, porque no editan la misma fila.
     - Nada se borra de verdad: se marca borrado. Si se borrara, el otro
       teléfono no se enteraría y lo volvería a subir.
     - Sin señal todo sigue funcionando contra el teléfono. Lo pendiente se
       sube cuando vuelve.
   ========================================================================= */
(function (global) {
  'use strict';

  var CFG = global.NUBE_CONFIG || {};
  var LLAVE_SESION = 'carlouis.nube.sesion';
  var LLAVE_RELOJ = 'carlouis.nube.desde';

  // Tipos que viajan. 'stock' va aparte porque no es una lista de registros
  // sino un solo objeto; se manda como un registro único.
  var TIPOS = ['cliente', 'pedido', 'gasto', 'ruta', 'feria', 'recordatorio'];
  var PLURAL = {
    cliente: 'clientes', pedido: 'pedidos', gasto: 'gastos',
    ruta: 'rutas', feria: 'ferias', recordatorio: 'recordatorios'
  };

  var Nube = {
    activa: function () { return !!(CFG.url && CFG.llave); },
    sesion: null,
    sincronizando: false,
    alCambiar: null,      // lo pone app.js para repintar
    alEstado: null        // avisa 'subiendo' / 'listo' / 'sin señal'
  };

  /* ---------- sesión ---------------------------------------------------- */

  function guardarSesion(s) {
    Nube.sesion = s;
    try { localStorage.setItem(LLAVE_SESION, JSON.stringify(s)); } catch (e) {}
  }

  function cargarSesion() {
    try {
      Nube.sesion = JSON.parse(localStorage.getItem(LLAVE_SESION) || 'null');
    } catch (e) { Nube.sesion = null; }
    return Nube.sesion;
  }

  Nube.entrar = function (correo, clave) {
    return fetch(CFG.url + '/auth/v1/token?grant_type=password', {
      method: 'POST',
      headers: { apikey: CFG.llave, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: correo, password: clave })
    }).then(function (r) {
      return r.json().then(function (d) {
        if (!r.ok) throw new Error(d.error_description || d.msg || 'No se pudo entrar');
        guardarSesion(d);
        return d;
      });
    });
  };

  Nube.salir = function () {
    Nube.sesion = null;
    try {
      localStorage.removeItem(LLAVE_SESION);
      localStorage.removeItem(LLAVE_RELOJ);
    } catch (e) {}
  };

  // El token dura una hora; se renueva con el de refresco antes de cada tanda.
  function refrescar() {
    if (!Nube.sesion || !Nube.sesion.refresh_token) return Promise.reject();
    return fetch(CFG.url + '/auth/v1/token?grant_type=refresh_token', {
      method: 'POST',
      headers: { apikey: CFG.llave, 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: Nube.sesion.refresh_token })
    }).then(function (r) {
      if (!r.ok) throw new Error('sesión vencida');
      return r.json();
    }).then(guardarSesion);
  }

  function pedir(ruta, opciones) {
    var o = opciones || {};
    var cabeceras = {
      apikey: CFG.llave,
      Authorization: 'Bearer ' + (Nube.sesion && Nube.sesion.access_token),
      'Content-Type': 'application/json'
    };
    Object.keys(o.headers || {}).forEach(function (k) { cabeceras[k] = o.headers[k]; });

    return fetch(CFG.url + '/rest/v1/' + ruta, {
      method: o.method || 'GET',
      headers: cabeceras,
      body: o.body
    }).then(function (r) {
      if (r.status === 401) {
        // Token vencido: se renueva y se reintenta una sola vez.
        return refrescar().then(function () {
          return pedir(ruta, Object.assign({}, o, { _reintento: true }));
        });
      }
      if (!r.ok) return r.text().then(function (t) { throw new Error(t); });
      return r.status === 204 ? null : r.json();
    });
  }

  /* ---------- convertir entre el formato local y el de la base ---------- */

  function aFilas(BD, quien) {
    var filas = [];
    TIPOS.forEach(function (tipo) {
      (BD[PLURAL[tipo]] || []).forEach(function (x) {
        if (!x.id) return;
        filas.push({
          id: tipo + ':' + x.id,
          tipo: tipo,
          contenido: x,
          borrado: !!x._borrado,
          por: quien || null
        });
      });
    });
    // El inventario es un objeto suelto, no una lista: va como un registro.
    if (BD.stock && Object.keys(BD.stock).length) {
      filas.push({ id: 'stock:unico', tipo: 'stock', contenido: BD.stock,
                   borrado: false, por: quien || null });
    }
    return filas;
  }

  // Mete lo que vino del servidor dentro de BD, respetando lo más reciente.
  function aplicar(BD, filas) {
    var cambios = 0;
    filas.forEach(function (f) {
      if (f.tipo === 'stock') {
        // Para el inventario se toma el del servidor tal cual: es un solo
        // registro y la marca de tiempo ya decidió cuál gana.
        BD.stock = f.contenido || {};
        cambios++;
        return;
      }
      var lista = BD[PLURAL[f.tipo]];
      if (!lista) return;
      var x = f.contenido;
      x._actualizado = f.actualizado;
      if (f.borrado) x._borrado = true;

      var i = -1;
      for (var k = 0; k < lista.length; k++) {
        if (lista[k].id === x.id) { i = k; break; }
      }
      if (i < 0) {
        if (!f.borrado) { lista.push(x); cambios++; }
      } else {
        var mio = lista[i]._actualizado || '';
        if ((f.actualizado || '') >= mio) {
          if (f.borrado) lista.splice(i, 1);
          else lista[i] = x;
          cambios++;
        }
      }
    });
    return cambios;
  }

  /* ---------- la tanda de sincronización -------------------------------- */

  Nube.sincronizar = function (BD, quien, guardar) {
    if (!Nube.activa() || !cargarSesion()) return Promise.resolve(0);
    if (Nube.sincronizando) return Promise.resolve(0);
    if (!navigator.onLine) {
      if (Nube.alEstado) Nube.alEstado('sin señal');
      return Promise.resolve(0);
    }

    Nube.sincronizando = true;
    if (Nube.alEstado) Nube.alEstado('subiendo');

    var desde = localStorage.getItem(LLAVE_RELOJ) || '1970-01-01T00:00:00Z';
    var ahora = new Date().toISOString();

    // Primero subir: si el otro teléfono está bajando en este momento, que
    // encuentre lo nuestro y no al revés.
    var mios = aFilas(BD, quien);
    var subir = mios.length
      ? pedir('datos', {
          method: 'POST',
          headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
          body: JSON.stringify(mios)
        })
      : Promise.resolve();

    return subir
      .then(function () {
        return pedir('datos?select=*&actualizado=gt.' + encodeURIComponent(desde) +
                     '&order=actualizado.asc');
      })
      .then(function (filas) {
        var n = aplicar(BD, filas || []);
        localStorage.setItem(LLAVE_RELOJ, ahora);
        if (n && guardar) guardar();
        if (n && Nube.alCambiar) Nube.alCambiar();
        if (Nube.alEstado) Nube.alEstado('listo');
        return n;
      })
      .catch(function (e) {
        if (Nube.alEstado) Nube.alEstado('sin señal');
        return 0;
      })
      .then(function (n) { Nube.sincronizando = false; return n; });
  };

  // Mientras la app esté abierta y visible, revisar seguido. En una feria con
  // dos teléfonos cobrando, diez segundos es la diferencia entre ver la venta
  // del otro o no verla.
  Nube.arrancarReloj = function (BD, quien, guardar) {
    if (!Nube.activa()) return;
    var tic = function () {
      if (document.visibilityState === 'visible') {
        Nube.sincronizar(BD, quien, guardar);
      }
    };
    setInterval(tic, 10000);
    document.addEventListener('visibilitychange', tic);
    window.addEventListener('online', tic);
    tic();
  };

  global.Nube = Nube;
})(window);
