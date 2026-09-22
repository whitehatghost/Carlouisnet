/* Prueba del optimizador de rutas contra fuerza bruta.
 *
 *     node tools/probar-rutas.js
 *
 * Saca las funciones reales de app/app.js —no una copia— y compara su
 * resultado contra TODAS las permutaciones posibles. Con 8 paradas son 40.320
 * rutas: se pueden revisar una por una y saber con certeza cuál es la mejor.
 *
 * Esto mide distancia en línea recta, que es lo que la app puede calcular sin
 * internet. No mide calles ni presas: para eso haría falta un servicio de
 * ruteo, que cuesta y no funcionaría sin señal.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, '..', 'app', 'app.js'), 'utf8');

function extraer(re, nombre) {
  const m = src.match(re);
  if (!m) throw new Error('No encontré la función ' + nombre + ' en app.js');
  return m[0];
}

const codigo = [
  extraer(/function dist\(a, b\) \{[\s\S]*?\n  \}/, 'dist'),
  extraer(/function largoRuta\(pts, origen\) \{[\s\S]*?\n  \}/, 'largoRuta'),
  extraer(/function pulir\(orden, origen\) \{[\s\S]*?\n    return orden;\n  \}/, 'pulir'),
  extraer(/function optimizar\(pts, origen\) \{[\s\S]*?\n    return mejorOrden;\n  \}/, 'optimizar')
].join('\n');

const sandbox = {};
new Function('exports', codigo + '\nexports.optimizar = optimizar; exports.largoRuta = largoRuta;')(sandbox);
const { optimizar, largoRuta } = sandbox;

function* permutaciones(a) {
  if (a.length <= 1) { yield a; return; }
  for (let i = 0; i < a.length; i++) {
    const resto = a.slice(0, i).concat(a.slice(i + 1));
    for (const p of permutaciones(resto)) yield [a[i]].concat(p);
  }
}

// Coordenadas dentro del Gran Área Metropolitana, que es donde se usa.
function puntoGAM() {
  return { lat: 9.90 + Math.random() * 0.30, lng: -84.35 + Math.random() * 0.35 };
}

const ORIGEN = { lat: 10.0162, lng: -84.2117 };   // Alajuela centro
let exactos = 0, fallos = 0, peor = 0;
const PRUEBAS = 60;
const t0 = Date.now();

for (let t = 0; t < PRUEBAS; t++) {
  const n = 5 + Math.floor(Math.random() * 4);     // 5 a 8 paradas
  const pts = Array.from({ length: n }, puntoGAM);
  const mio = largoRuta(optimizar(pts, ORIGEN), ORIGEN);
  let mejor = Infinity;
  for (const p of permutaciones(pts)) {
    const l = largoRuta(p, ORIGEN);
    if (l < mejor) mejor = l;
  }
  const desvio = (mio - mejor) / mejor * 100;
  if (desvio < 0.01) exactos++;
  else { fallos++; peor = Math.max(peor, desvio); }
}
const ms = (Date.now() - t0) / PRUEBAS;

// Rutas grandes: que no se trabe el teléfono.
const grande = Array.from({ length: 20 }, puntoGAM);
const t1 = Date.now();
optimizar(grande, ORIGEN);
const msGrande = Date.now() - t1;

console.log('  Pruebas contra fuerza bruta : ' + PRUEBAS + ' rutas de 5 a 8 paradas');
console.log('  Dio el óptimo exacto        : ' + exactos + ' de ' + PRUEBAS);
console.log('  No óptimo                   : ' + fallos +
            (fallos ? ' (peor desvío ' + peor.toFixed(2) + '%)' : ''));
console.log('  Tiempo por ruta             : ' + ms.toFixed(1) + ' ms');
console.log('  Ruta de 20 paradas          : ' + msGrande + ' ms');

if (fallos > 0) {
  console.log('\n  ATENCIÓN: el optimizador dejó de dar el óptimo. Revisar pulir()/optimizar().');
  process.exit(1);
}
console.log('\n  Todo bien.');
