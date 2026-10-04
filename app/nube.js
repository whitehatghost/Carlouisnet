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
  var TIPOS = ['cliente', 'pedido', 'gasto', 'ruta', 'feria', 'recordatorio', 'producto', 'entrada'];
  var PLURAL = {
    cliente: 'clientes', pedido: 'pedidos', gasto: 'gastos',
    ruta: 'rutas', feria: 'ferias', recordatorio: 'recordatorios',
    producto: 'productos', entrada: 'entradas'
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
        Nube.sesionVencida = false;
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
      Object.keys(localStorage).forEach(function (k) {
        if (k.indexOf('carlouis.nube2.') === 0) localStorage.removeItem(k);
      });
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
      // 400/401/403: el permiso guardado ya no sirve y hay que volver a entrar.
      // Antes esto se veía igual que "sin señal" y nadie se enteraba.
      if (!r.ok) {
        if (r.status >= 400 && r.status < 500) Nube.sesionVencida = true;
        throw new Error('sesión vencida');
      }
      Nube.sesionVencida = false;
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
        // Token vencido: se renueva y se reintenta una sola vez. Si aun con el
        // permiso nuevo no deja, hay que volver a entrar.
        if (o._reintento) {
          Nube.sesionVencida = true;
          throw new Error('sesión vencida');
        }
        return refrescar().then(function () {
          return pedir(ruta, Object.assign({}, o, { _reintento: true }));
        });
      }
      if (!r.ok) return r.text().then(function (t) { throw new Error(t); });
      // Al subir, el servidor contesta "listo" SIN cuerpo (201 o 204). Antes eso
      // se leía como JSON, reventaba, y la tanda se cortaba justo antes de bajar
      // lo de los demás: cada teléfono subía lo suyo y nunca recibía nada.
      return r.text().then(function (t) { return t ? JSON.parse(t) : null; });
    });
  }

  /* ---------- convertir entre el formato local y el de la base ---------- */

  /* Cómo se decide qué viaja y quién gana.

     Cada registro lleva en su contenido un sello `_actualizado`: la hora en que
     ESE registro cambió de verdad en algún teléfono. Con eso:

     - Solo se sube lo que cambió acá desde la última vez (no todo, siempre).
       Antes cada teléfono resubía su copia completa cada 10 segundos, y la
       copia vieja de uno le pisaba los cambios nuevos del otro.
     - Al bajar, gana el sello más reciente, no "el último que subió".
     - Lo borrado viaja como una tumba (BD._tumbas) hasta que el servidor la
       tiene; antes los borrados nunca salían del teléfono.
     - El punto desde donde se baja es la hora del SERVIDOR de lo último
       recibido, no el reloj del teléfono, y se guarda por perfil.            */

  function aFilas(BD, quien) {
    var filas = [];
    TIPOS.forEach(function (tipo) {
      (BD[PLURAL[tipo]] || []).forEach(function (x) {
        if (!x.id) return;
        filas.push({ id: tipo + ':' + x.id, tipo: tipo, contenido: x,
                     borrado: false, por: quien || null });
      });
    });
    (BD._tumbas || []).forEach(function (t) {
      if (!PLURAL[t.tipo] || !t.id) return;
      filas.push({ id: t.tipo + ':' + t.id, tipo: t.tipo,
                   contenido: { id: t.id, _borrado: true, _actualizado: t._actualizado },
                   borrado: true, por: quien || null });
    });
    return filas;
  }

  function sello(f) { return (f.contenido && f.contenido._actualizado) || ''; }

  // Mete lo que vino del servidor dentro de BD. `subidos` recuerda, por
  // registro, cuál sello tiene el servidor: lo que no coincida se vuelve a subir.
  function aplicar(BD, filas, subidos) {
    var cambios = 0;
    filas.forEach(function (f) {
      if (f.tipo === 'stock') {
        // Contador viejo de inventario. Solo le sirve a un teléfono que
        // todavía no pasó al inventario único.
        if (!BD.invUnico) { BD.stock = f.contenido || {}; cambios++; }
        return;
      }
      var lista = BD[PLURAL[f.tipo]];
      if (!lista) return;
      var x = f.contenido || {};
      if (!x.id) return;
      var remoto = x._actualizado || f.actualizado || '';
      x._actualizado = remoto;

      // ¿Lo borramos acá y todavía no se había avisado?
      var tumbas = BD._tumbas || [], it = -1;
      for (var q = 0; q < tumbas.length; q++) {
        if (tumbas[q].tipo === f.tipo && tumbas[q].id === x.id) { it = q; break; }
      }
      if (it >= 0) {
        if (f.borrado) { tumbas.splice(it, 1); subidos[f.id] = remoto; return; }
        if (remoto <= (tumbas[it]._actualizado || '')) return;   // gana nuestro borrado
        tumbas.splice(it, 1);                                    // lo editaron después: vuelve
      }

      var i = -1;
      for (var k = 0; k < lista.length; k++) {
        if (lista[k].id === x.id) { i = k; break; }
      }

      if (f.borrado) {
        if (i >= 0) {
          if (remoto >= (lista[i]._actualizado || '')) { lista.splice(i, 1); cambios++; }
          else { delete subidos[f.id]; return; }                 // acá es más nuevo: se resube
        }
        subidos[f.id] = remoto;
        return;
      }
      if (i < 0) { lista.push(x); subidos[f.id] = remoto; cambios++; return; }

      var local = lista[i]._actualizado || '';
      if (remoto > local) { lista[i] = x; subidos[f.id] = remoto; cambios++; }
      else if (remoto === local) subidos[f.id] = remoto;
      else delete subidos[f.id];                                 // acá es más nuevo: se resube
    });
    return cambios;
  }

  /* ---------- sincronizar ----------------------------------------------- */

  var EPOCA = '1970-01-01T00:00:00.000Z';

  function leerJSON(k) {
    try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; }
  }

  function estado(e) { Nube.estado = e; if (Nube.alEstado) Nube.alEstado(e); }

  Nube.sincronizar = function (BD, quien, guardar, perfil) {
    var nada = { ok: false, cambios: 0 };
    if (!Nube.activa() || !cargarSesion()) return Promise.resolve(nada);
    if (Nube.sincronizando) return Promise.resolve(nada);
    if (!navigator.onLine) { estado('sin señal'); return Promise.resolve(nada); }

    Nube.sincronizando = true;
    estado('subiendo');

    var K = 'carlouis.nube2.' + (perfil || 'x') + '.';
    var cursor = localStorage.getItem(K + 'cursor') || EPOCA;
    var subidos = leerJSON(K + 'subidos');
    var cambios = 0, subidas = 0, maxMs = Date.parse(cursor) || 0;

    // Bajar por páginas: el servidor entrega máximo 1000 filas por pedido.
    function bajar(desde, juntas) {
      return pedir('datos?select=*&actualizado=gt.' + encodeURIComponent(cursor) +
                   '&order=actualizado.asc,id.asc&limit=1000&offset=' + desde)
        .then(function (filas) {
          filas = filas || [];
          juntas = juntas.concat(filas);
          if (filas.length === 1000 && desde < 100000) return bajar(desde + 1000, juntas);
          return juntas;
        });
    }

    return bajar(0, [])
      .then(function (filas) {
        filas.forEach(function (f) {
          var ms = Date.parse(f.actualizado) || 0;
          if (ms > maxMs) maxMs = ms;
        });
        cambios = aplicar(BD, filas, subidos);
        if (cambios && Nube.alRecibir) Nube.alRecibir();

        // Subir solo lo que acá es distinto de lo que tiene el servidor.
        var sucias = aFilas(BD, quien).filter(function (f) {
          return !sello(f) || subidos[f.id] !== sello(f);
        });
        var cadena = Promise.resolve();
        var tanda = function (grupo) {
          return function () {
            return pedir('datos', {
              method: 'POST',
              headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
              body: JSON.stringify(grupo)
            }).then(function () {
              grupo.forEach(function (f) {
                subidos[f.id] = sello(f);
                subidas++;
                if (f.borrado) {
                  // La tumba ya llegó: se puede soltar.
                  BD._tumbas = (BD._tumbas || []).filter(function (t) {
                    return !(t.tipo === f.tipo && t.id === f.contenido.id);
                  });
                }
              });
            });
          };
        };
        for (var i = 0; i < sucias.length; i += 400) {
          cadena = cadena.then(tanda(sucias.slice(i, i + 400)));
        }
        return cadena;
      })
      .then(function () {
        // 5 segundos de traslape: volver a bajar algo repetido no hace daño,
        // saltarse algo sí.
        var nuevo = new Date(Math.max(Date.parse(cursor) || 0, maxMs - 5000)).toISOString();
        localStorage.setItem(K + 'cursor', nuevo);
        localStorage.setItem(K + 'subidos', JSON.stringify(subidos));
        if ((cambios || subidas) && guardar) guardar();
        if (cambios && Nube.alCambiar) Nube.alCambiar();
        Nube.ultima = Date.now();
        estado('listo');
        return { ok: true, cambios: cambios, subidas: subidas };
      })
      .catch(function (e) {
        // Lo que alcanzó a subir o bajar queda anotado para no repetirlo.
        try { localStorage.setItem(K + 'subidos', JSON.stringify(subidos)); } catch (x) {}
        if (cambios && guardar) guardar();
        if (cambios && Nube.alCambiar) Nube.alCambiar();
        estado(Nube.sesionVencida ? 'sesion' : 'sin señal');
        return { ok: false, cambios: cambios };
      })
      .then(function (r) { Nube.sincronizando = false; return r; });
  };

  // `tarea` es la función de la app que sincroniza. Se corre cada 10 segundos
  // con la app a la vista, al volver a ella y al recuperar señal.
  Nube.arrancarReloj = function (tarea) {
    if (!Nube.activa() || Nube._reloj) return;
    var tic = function () {
      if (document.visibilityState === 'visible') tarea();
    };
    Nube._reloj = setInterval(tic, 10000);
    document.addEventListener('visibilitychange', tic);
    window.addEventListener('online', tic);
    tic();
  };

  global.Nube = Nube;
})(window);
