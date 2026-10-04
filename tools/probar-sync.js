/* Prueba de la sincronización de app/nube.js con dos (o más) teléfonos.

       node tools/probar-sync.js

   No toca la base real: levanta un servidor de mentira en memoria que se
   comporta como Supabase (pone él la hora `actualizado`, entrega máximo 1000
   filas por pedido, hace upsert por id). Cada "teléfono" carga su propia copia
   de nube.js con su propio localStorage.

   Lo que se comprueba es lo que fallaba antes:
   - que un cambio hecho en un teléfono llegue al otro y NO se devuelva,
   - que lo borrado no reaparezca,
   - que dos teléfonos vendiendo a la vez no se pisen,
   - que un reloj adelantado no haga perder datos,
   - que un teléfono nuevo baje todo aunque sean miles de registros.          */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const FUENTE = fs.readFileSync(path.join(__dirname, '..', 'app', 'nube.js'), 'utf8');

/* ---------- servidor de mentira ------------------------------------------ */
const servidor = { filas: new Map(), reloj: Date.parse('2026-10-04T12:00:00Z'), pedidos: 0, subidas: 0 };
function horaServidor() { servidor.reloj += 7; return new Date(servidor.reloj).toISOString(); }

function fetchFalso(url, o) {
  o = o || {};
  servidor.pedidos++;
  const u = new URL(url);
  const responder = (status, cuerpo) => Promise.resolve({
    ok: status >= 200 && status < 300, status,
    // Como el servidor real: al subir contesta SIN cuerpo, y leer eso como JSON revienta.
    json: () => cuerpo === null ? Promise.reject(new SyntaxError('Unexpected end of JSON input')) : Promise.resolve(cuerpo),
    text: () => Promise.resolve(cuerpo === null ? '' : JSON.stringify(cuerpo))
  });
  if (u.pathname.startsWith('/auth/')) return responder(200, { access_token: 't', refresh_token: 'r' });
  if (u.pathname === '/rest/v1/datos' && (o.method || 'GET') === 'GET') {
    const gt = (u.searchParams.get('actualizado') || '').replace(/^gt\./, '');
    const limite = Number(u.searchParams.get('limit') || 1000);
    const desde = Number(u.searchParams.get('offset') || 0);
    const todas = [...servidor.filas.values()]
      .filter(f => Date.parse(f.actualizado) > Date.parse(gt))
      .sort((a, b) => a.actualizado.localeCompare(b.actualizado) || a.id.localeCompare(b.id));
    return responder(200, JSON.parse(JSON.stringify(todas.slice(desde, desde + Math.min(limite, 1000)))));
  }
  if (u.pathname === '/rest/v1/datos' && o.method === 'POST') {
    const hora = horaServidor();               // una sola hora por tanda, como now() en Postgres
    JSON.parse(o.body).forEach(f => { servidor.subidas++; servidor.filas.set(f.id, Object.assign({}, f, { actualizado: hora })); });
    return responder(201, null);
  }
  return responder(404, {});
}

/* ---------- un teléfono --------------------------------------------------- */
const COLECCIONES = ['clientes', 'pedidos', 'gastos', 'rutas', 'ferias', 'recordatorios', 'productos', 'entradas'];

function Telefono(nombre, adelantoReloj) {
  const almacen = {};
  const ls = {
    getItem: k => (k in almacen ? almacen[k] : null),
    setItem: (k, v) => { almacen[k] = String(v); },
    removeItem: k => { delete almacen[k]; }
  };
  Object.defineProperty(ls, 'length', { get: () => Object.keys(almacen).length });
  ls.setItem('carlouis.nube.sesion', JSON.stringify({ access_token: 't', refresh_token: 'r' }));

  const caja = {
    NUBE_CONFIG: { url: 'https://falso.test', llave: 'k' },
    localStorage: ls, fetch: fetchFalso, navigator: { onLine: true },
    document: { visibilityState: 'visible', addEventListener() {} },
    addEventListener() {}, setInterval() { return 1; }, console,
    Date: adelantoReloj ? class extends Date {
      constructor(...a) { if (a.length) super(...a); else super(Date.now() + adelantoReloj); }
      static now() { return Date.now() + adelantoReloj; }
    } : Date,
    URL, Promise, JSON, Object, Math, String, Number, Array, encodeURIComponent, Error
  };
  caja.window = caja;
  // Object.keys(localStorage) debe listar las llaves guardadas (lo usa Nube.salir)
  vm.createContext(caja);
  vm.runInContext(FUENTE, caja);

  const BD = { stock: {}, _tumbas: [], invUnico: true };
  COLECCIONES.forEach(k => { BD[k] = []; });
  const huellas = {};
  const reloj = () => new caja.Date().toISOString();

  // Igual que sellar()/huella() de app.js.
  function huella(x) { const s = x._actualizado; delete x._actualizado; const h = JSON.stringify(x); if (s !== undefined) x._actualizado = s; return h; }
  function sellar() {
    const ahora = reloj();
    COLECCIONES.forEach(k => BD[k].forEach(x => {
      const h = huella(x);
      if (huellas[x.id] !== h || !x._actualizado) { huellas[x.id] = h; x._actualizado = ahora; }
    }));
  }
  caja.Nube.alRecibir = () => COLECCIONES.forEach(k => BD[k].forEach(x => { if (x._actualizado) huellas[x.id] = huella(x); }));

  return {
    nombre, BD, Nube: caja.Nube,
    red(si) { caja.navigator.onLine = si; },
    borrar(tipo, lista, id) {
      BD[lista] = BD[lista].filter(x => x.id !== id);
      BD._tumbas.push({ tipo, id, _actualizado: reloj() });
    },
    async sync() { sellar(); return caja.Nube.sincronizar(BD, nombre, () => {}, 'u'); },
    hay(slug) {
      let n = 0;
      BD.entradas.forEach(e => { if (e.slug === slug) n += e.cant; });
      BD.pedidos.forEach(p => (p.lineas || []).forEach(l => { if (l.slug === slug) n -= l.cant; }));
      return n;
    }
  };
}

/* ---------- las pruebas --------------------------------------------------- */
let fallas = 0, hechas = 0;
function espero(cond, texto) {
  hechas++;
  if (!cond) { fallas++; console.log('  FALLA  ' + texto); } else console.log('  ok     ' + texto);
}
const pausa = () => new Promise(r => setTimeout(r, 3));   // para que los sellos no empaten
const vuelta = async (...ts) => { for (const t of ts) { await t.sync(); await pausa(); } };

(async () => {
  const luis = Telefono('Luis'), carlina = Telefono('Carlina');

  console.log('\n1. Una venta de Luis le llega a Carlina');
  luis.BD.ferias.push({ id: 'f1', nombre: 'Terrazas', fecha: '2026-10-02', fechaFin: '2026-10-04', cierres: {}, cerrada: false });
  luis.BD.pedidos.push({ id: 'v1', feriaId: 'f1', fecha: '2026-10-02', lineas: [{ slug: 'alioli', cant: 2 }] });
  await vuelta(luis, carlina);
  espero(carlina.BD.pedidos.length === 1 && carlina.BD.ferias.length === 1, 'Carlina ve la feria y la venta');

  console.log('\n2. Carlina cierra el día; el cierre no se devuelve');
  carlina.BD.ferias[0].cierres['2026-10-02'] = { por: 'Carlina' };
  await vuelta(carlina, luis, carlina, luis, carlina, luis);
  espero(!!luis.BD.ferias[0].cierres['2026-10-02'], 'Luis ve el día cerrado');
  espero(!!carlina.BD.ferias[0].cierres['2026-10-02'], 'a Carlina no se le reabre');
  const antes = servidor.subidas;
  await vuelta(luis, carlina, luis, carlina);
  espero(servidor.subidas === antes, 'sin cambios nuevos no se sube nada (antes se resubía todo cada 10 s)');

  console.log('\n3. Los dos venden a la vez, sin señal, y después sincronizan');
  luis.BD.pedidos.push({ id: 'v2', feriaId: 'f1', fecha: '2026-10-03', lineas: [{ slug: 'alioli', cant: 1 }] });
  carlina.BD.pedidos.push({ id: 'v3', feriaId: 'f1', fecha: '2026-10-03', lineas: [{ slug: 'alioli', cant: 3 }] });
  await vuelta(luis, carlina, luis, carlina);
  espero(luis.BD.pedidos.length === 3 && carlina.BD.pedidos.length === 3, 'los dos tienen las tres ventas');

  console.log('\n4. Un solo inventario');
  luis.BD.entradas.push({ id: 'e1', slug: 'alioli', cant: 20 });
  await vuelta(luis, carlina);
  espero(luis.hay('alioli') === 14 && carlina.hay('alioli') === 14, 'entraron 20, se vendieron 6: los dos ven 14');
  carlina.BD.entradas.push({ id: 'e2', slug: 'alioli', cant: 12 });
  luis.BD.pedidos.push({ id: 'v4', feriaId: 'f1', fecha: '2026-10-04', lineas: [{ slug: 'alioli', cant: 4 }] });
  await vuelta(carlina, luis, carlina);
  espero(luis.hay('alioli') === 22 && carlina.hay('alioli') === 22, 'lote de Carlina y venta de Luis al mismo tiempo: los dos ven 22');

  console.log('\n5. Lo borrado no reaparece');
  luis.borrar('pedido', 'pedidos', 'v2');
  await vuelta(luis, carlina, luis, carlina, luis);
  espero(!luis.BD.pedidos.some(p => p.id === 'v2') && !carlina.BD.pedidos.some(p => p.id === 'v2'), 'la venta borrada no está en ninguno');
  espero(luis.BD._tumbas.length === 0, 'la tumba se suelta cuando la nube la recibe');
  espero(luis.hay('alioli') === 23 && carlina.hay('alioli') === 23, 'el inventario devuelve el frasco de la venta borrada');

  console.log('\n6. Los dos editan lo mismo: gana el cambio más reciente, en los dos');
  luis.BD.clientes.push({ id: 'c1', nombre: 'Doña Ana', tel: '1111' });
  await vuelta(luis, carlina);
  luis.BD.clientes[0].tel = '2222'; await luis.sync(); await pausa();
  carlina.BD.clientes[0].tel = '3333';
  await vuelta(carlina, luis, carlina, luis);
  espero(luis.BD.clientes[0].tel === '3333' && carlina.BD.clientes[0].tel === '3333', 'los dos quedan con el último teléfono');

  console.log('\n7. Un teléfono con el reloj adelantado 10 minutos no pierde datos');
  const adelantado = Telefono('Adelantado', 10 * 60 * 1000);
  await adelantado.sync();
  luis.BD.pedidos.push({ id: 'v5', feriaId: 'f1', fecha: '2026-10-04', lineas: [{ slug: 'alioli', cant: 1 }] });
  await vuelta(luis, adelantado);
  espero(adelantado.BD.pedidos.some(p => p.id === 'v5'), 'recibe la venta hecha "antes" de su hora');

  console.log('\n8. Un teléfono nuevo baja todo, aunque sean 2500 registros');
  for (let i = 0; i < 2500; i++) luis.BD.gastos.push({ id: 'g' + i, monto: 100, fecha: '2026-09-01' });
  await luis.sync();
  const nuevo = Telefono('Nuevo');
  await nuevo.sync();
  espero(nuevo.BD.gastos.length === 2500, 'bajó los 2500 (el servidor entrega de 1000 en 1000)');
  espero(nuevo.BD.pedidos.length === luis.BD.pedidos.length, 'y las ventas');
  const antes2 = servidor.subidas;
  await vuelta(nuevo, luis, nuevo);
  espero(servidor.subidas === antes2, 'el nuevo no resube lo que acaba de bajar');

  console.log('\n9. Sin señal no se pierde nada');
  carlina.red(false);
  carlina.BD.pedidos.push({ id: 'v6', feriaId: 'f1', fecha: '2026-10-04', lineas: [{ slug: 'alioli', cant: 2 }] });
  const sinRed = await carlina.sync();
  await luis.sync();
  espero(sinRed.ok === false && !luis.BD.pedidos.some(p => p.id === 'v6'), 'sin señal no sube, y la app lo sabe');
  espero(carlina.BD.pedidos.some(p => p.id === 'v6'), 'la venta sigue guardada en el teléfono de Carlina');
  carlina.red(true);
  await vuelta(carlina, luis);
  espero(luis.BD.pedidos.some(p => p.id === 'v6'), 'al volver la señal la venta llega');

  console.log('\n' + (hechas - fallas) + ' de ' + hechas + ' comprobaciones pasaron.');
  process.exit(fallas ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
