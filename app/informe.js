/* =========================================================================
   CARLOUIS · Control — informes en PDF y para imprimir

   Arma el cierre de una feria (o de un día) como PDF de verdad, en tamaño
   carta, con el logo y los colores de la marca. No usa ninguna librería ni
   servicio de afuera: dibuja cada página en un lienzo y la envuelve en un PDF
   escrito a mano. Así funciona sin internet y no cuesta nada.

   El informe llega como una lista de bloques, que es lo que arma app.js:

     { t: 'titulo', texto, sub }
     { t: 'meta',   lineas: [...] }
     { t: 'cifras', items: [[etiqueta, valor], ...] }
     { t: 'tabla',  titulo, cab: [...], alin: ['i'|'d', ...], anchos: [...],
                    filas: [[...], ...], pie: [...] }
     { t: 'nota',   texto }

   Con esos mismos bloques sale también la versión HTML para imprimir directo.
   ========================================================================= */
(function (global) {
  'use strict';

  var ANCHO = 816, ALTO = 1056;      // carta a 96 puntos por pulgada
  var DENSIDAD = 2;                  // el doble, para que imprima nítido
  var MARGEN = 58;
  var TINTA = '#241A15', SUAVE = '#5C4A3F', BRASA = '#6B1608',
      ORO = '#E0A02E', LINEA = '#DDCFBC', PAPEL = '#F6EFE4';

  function esperarFuentes() {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    return Promise.all([
      document.fonts.load('700 30px Fraunces'),
      document.fonts.load('400 15px Karla'),
      document.fonts.load('700 15px Karla')
    ]).catch(function () {});
  }

  function cargarLogo() {
    return new Promise(function (listo) {
      var im = new Image();
      im.onload = function () { listo(im); };
      im.onerror = function () { listo(null); };
      im.src = '../assets/img/logo.png';
    });
  }

  /* ---------- dibujar las páginas ---------------------------------------- */

  function dibujar(bloques, logo, pie) {
    var paginas = [], x = null, y = 0;
    var util = ANCHO - 2 * MARGEN, fondo = ALTO - MARGEN - 26;

    function letra(peso, tam, familia) {
      x.font = peso + ' ' + tam + 'px ' + (familia || 'Karla') + ', Arial, sans-serif';
    }
    function texto(s, px, py, color, alin) {
      x.fillStyle = color || TINTA;
      x.textAlign = alin === 'd' ? 'right' : alin === 'c' ? 'center' : 'left';
      x.textBaseline = 'alphabetic';
      x.fillText(s, px, py);
    }
    // Recorta con puntos suspensivos lo que no quepa en el ancho dado.
    function caber(s, ancho) {
      s = String(s == null ? '' : s);
      if (x.measureText(s).width <= ancho) return s;
      while (s.length > 1 && x.measureText(s + '…').width > ancho) s = s.slice(0, -1);
      return s + '…';
    }
    function raya(py, color, grueso) {
      x.strokeStyle = color || LINEA; x.lineWidth = grueso || 1;
      x.beginPath(); x.moveTo(MARGEN, py); x.lineTo(ANCHO - MARGEN, py); x.stroke();
    }
    function caja(px, py, w, h, r, color) {
      x.fillStyle = color;
      x.beginPath();
      x.moveTo(px + r, py); x.lineTo(px + w - r, py); x.quadraticCurveTo(px + w, py, px + w, py + r);
      x.lineTo(px + w, py + h - r); x.quadraticCurveTo(px + w, py + h, px + w - r, py + h);
      x.lineTo(px + r, py + h); x.quadraticCurveTo(px, py + h, px, py + h - r);
      x.lineTo(px, py + r); x.quadraticCurveTo(px, py, px + r, py);
      x.fill();
    }

    function nueva() {
      var c = document.createElement('canvas');
      c.width = ANCHO * DENSIDAD; c.height = ALTO * DENSIDAD;
      x = c.getContext('2d');
      x.scale(DENSIDAD, DENSIDAD);
      x.fillStyle = '#fff'; x.fillRect(0, 0, ANCHO, ALTO);
      paginas.push({ lienzo: c, ctx: x });
      y = MARGEN;
      if (logo) {
        var alto = 40, anchoLogo = logo.width * alto / logo.height;
        x.drawImage(logo, MARGEN, y - 6, anchoLogo, alto);
      } else {
        letra(700, 22, 'Fraunces'); texto('CARLOUIS', MARGEN, y + 24, BRASA);
      }
      letra(700, 11); texto('SALSAS ARTESANALES · ALAJUELA, COSTA RICA', ANCHO - MARGEN, y + 12, SUAVE, 'd');
      letra(400, 11); texto('carlouis.net · WhatsApp 8825 2608', ANCHO - MARGEN, y + 28, SUAVE, 'd');
      y += 50;
      raya(y, ORO, 3);
      y += 30;
    }
    function cabe(alto) { if (y + alto > fondo) nueva(); }

    function tabla(b) {
      var n = b.cab.length;
      var anchos = b.anchos || b.cab.map(function () { return 1; });
      var suma = anchos.reduce(function (s, a) { return s + a; }, 0);
      var cols = [], px = MARGEN;
      anchos.forEach(function (a) { var w = util * a / suma; cols.push({ x: px, w: w }); px += w; });
      var alin = b.alin || [];

      function celda(s, i, py, color) {
        var c = cols[i], der = alin[i] === 'd';
        texto(caber(s, c.w - 12), der ? c.x + c.w - 6 : c.x + 6, py, color, der ? 'd' : 'i');
      }
      function encabezado(sigue) {
        if (b.titulo) {
          letra(700, 18, 'Fraunces');
          texto(b.titulo + (sigue ? ' (sigue)' : ''), MARGEN, y + 16, BRASA);
          y += 30;
        }
        letra(700, 11);
        for (var i = 0; i < n; i++) celda(String(b.cab[i]).toUpperCase(), i, y + 12, SUAVE);
        y += 20;
        raya(y, SUAVE, 1.2);
      }

      // Si la tabla entera cabe en una página, no se parte: pasa completa a la
      // siguiente. Solo se corta cuando es más larga que una hoja.
      var altoTabla = (b.titulo ? 30 : 0) + 20 + 28 * Math.max(1, b.filas.length) + (b.pie ? 32 : 0);
      var altoHoja = fondo - (MARGEN + 80);
      cabe(altoTabla <= altoHoja ? altoTabla
                                 : (b.titulo ? 30 : 0) + 20 + 28 * Math.min(3, b.filas.length + 1));
      encabezado(false);
      b.filas.forEach(function (fila, k) {
        if (y + 28 > fondo) { nueva(); encabezado(true); }
        if (k % 2 === 1) { x.fillStyle = PAPEL; x.fillRect(MARGEN, y + 1, util, 27); }
        letra(400, 14.5);
        for (var i = 0; i < n; i++) celda(fila[i], i, y + 19, TINTA);
        y += 28;
        raya(y, LINEA, 0.6);
      });
      if (b.pie) {
        if (y + 32 > fondo) { nueva(); encabezado(true); }
        raya(y, TINTA, 1.4);
        letra(700, 15);
        for (var i = 0; i < n; i++) celda(b.pie[i], i, y + 22, TINTA);
        y += 32;
      }
      if (!b.filas.length && !b.pie) {
        letra(400, 14); texto('Sin movimientos.', MARGEN + 6, y + 20, SUAVE); y += 28;
      }
      y += 22;
    }

    nueva();
    bloques.forEach(function (b) {
      if (b.t === 'titulo') {
        cabe(70);
        letra(700, 30, 'Fraunces'); texto(caber(b.texto, util), MARGEN, y + 24, BRASA);
        y += 36;
        if (b.sub) { letra(700, 17); texto(caber(b.sub, util), MARGEN, y + 14, TINTA); y += 26; }
        y += 4;
      } else if (b.t === 'meta') {
        letra(400, 14);
        b.lineas.forEach(function (l) { cabe(20); texto(caber(l, util), MARGEN, y + 12, SUAVE); y += 20; });
        y += 14;
      } else if (b.t === 'cifras') {
        var porFila = Math.min(4, b.items.length), sep = 12;
        var w = (util - sep * (porFila - 1)) / porFila;
        for (var i = 0; i < b.items.length; i += porFila) {
          cabe(84);
          b.items.slice(i, i + porFila).forEach(function (it, k) {
            var px = MARGEN + k * (w + sep);
            caja(px, y, w, 70, 12, PAPEL);
            letra(700, 23, 'Fraunces'); texto(caber(it[1], w - 24), px + 14, y + 34, BRASA);
            letra(700, 10.5); texto(caber(String(it[0]).toUpperCase(), w - 24), px + 14, y + 54, SUAVE);
          });
          y += 82;
        }
        y += 12;
      } else if (b.t === 'tabla') {
        tabla(b);
      } else if (b.t === 'nota') {
        cabe(24); letra(400, 13); texto(caber(b.texto, util), MARGEN, y + 12, SUAVE); y += 24;
      }
    });

    // Pie de cada página, ya sabiendo cuántas son.
    paginas.forEach(function (p, i) {
      x = p.ctx;
      raya(ALTO - MARGEN + 2, LINEA, 0.8);
      letra(400, 11);
      texto(pie || '', MARGEN, ALTO - MARGEN + 20, SUAVE);
      texto('Página ' + (i + 1) + ' de ' + paginas.length, ANCHO - MARGEN, ALTO - MARGEN + 20, SUAVE, 'd');
    });
    return paginas.map(function (p) { return p.lienzo; });
  }

  /* ---------- envolver las páginas en un PDF ------------------------------ */

  function bytesDeJPEG(lienzo) {
    var b64 = lienzo.toDataURL('image/jpeg', 0.9).split(',')[1];
    var bin = atob(b64), u = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return u;
  }

  function armarPDF(lienzos) {
    var partes = [], pos = 0, donde = [];
    function txt(s) {
      var u = new Uint8Array(s.length);
      for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i) & 255;
      partes.push(u); pos += u.length;
    }
    function obj(n, cuerpo) { donde[n] = pos; txt(n + ' 0 obj\n' + cuerpo + '\nendobj\n'); }

    var n = lienzos.length, total = 2 + 3 * n;
    txt('%PDF-1.4\n%\xE2\xE3\xCF\xD3\n');
    obj(1, '<< /Type /Catalog /Pages 2 0 R >>');
    var hijos = [];
    for (var i = 0; i < n; i++) hijos.push((3 + 3 * i) + ' 0 R');
    obj(2, '<< /Type /Pages /Count ' + n + ' /Kids [' + hijos.join(' ') + '] >>');

    lienzos.forEach(function (c, k) {
      var pag = 3 + 3 * k, cont = pag + 1, img = pag + 2;
      var jpeg = bytesDeJPEG(c);
      // 612 x 792 puntos = tamaño carta.
      obj(pag, '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] ' +
               '/Resources << /XObject << /Im0 ' + img + ' 0 R >> >> /Contents ' + cont + ' 0 R >>');
      var dibujo = 'q 612 0 0 792 0 0 cm /Im0 Do Q';
      obj(cont, '<< /Length ' + dibujo.length + ' >>\nstream\n' + dibujo + '\nendstream');
      donde[img] = pos;
      txt(img + ' 0 obj\n<< /Type /XObject /Subtype /Image /Width ' + c.width + ' /Height ' + c.height +
          ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + jpeg.length +
          ' >>\nstream\n');
      partes.push(jpeg); pos += jpeg.length;
      txt('\nendstream\nendobj\n');
    });

    var xref = pos;
    txt('xref\n0 ' + (total + 1) + '\n0000000000 65535 f \n');
    for (var j = 1; j <= total; j++) txt(('0000000000' + donde[j]).slice(-10) + ' 00000 n \n');
    txt('trailer\n<< /Size ' + (total + 1) + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF\n');
    return new Blob(partes, { type: 'application/pdf' });
  }

  /* ---------- la misma información, en HTML para imprimir ----------------- */

  function e(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function aHTML(bloques, pie) {
    var h = '<div class="imp__cab"><img src="../assets/img/logo.png" alt="CARLOUIS" />' +
      '<p>Salsas artesanales · Alajuela, Costa Rica<br>carlouis.net · WhatsApp 8825 2608</p></div>';
    bloques.forEach(function (b) {
      if (b.t === 'titulo') {
        h += '<h1>' + e(b.texto) + '</h1>' + (b.sub ? '<p class="imp__sub">' + e(b.sub) + '</p>' : '');
      } else if (b.t === 'meta') {
        h += '<p class="imp__meta">' + b.lineas.map(e).join('<br>') + '</p>';
      } else if (b.t === 'cifras') {
        h += '<div class="imp__cifras">' + b.items.map(function (it) {
          return '<div><b>' + e(it[1]) + '</b><span>' + e(it[0]) + '</span></div>';
        }).join('') + '</div>';
      } else if (b.t === 'tabla') {
        var al = b.alin || [];
        var cl = function (i) { return al[i] === 'd' ? ' class="d"' : ''; };
        h += (b.titulo ? '<h2>' + e(b.titulo) + '</h2>' : '') + '<table><thead><tr>' +
          b.cab.map(function (c, i) { return '<th' + cl(i) + '>' + e(c) + '</th>'; }).join('') +
          '</tr></thead><tbody>' +
          b.filas.map(function (f) {
            return '<tr>' + f.map(function (c, i) { return '<td' + cl(i) + '>' + e(c) + '</td>'; }).join('') + '</tr>';
          }).join('') + '</tbody>' +
          (b.pie ? '<tfoot><tr>' + b.pie.map(function (c, i) {
            return '<td' + cl(i) + '>' + e(c) + '</td>'; }).join('') + '</tr></tfoot>' : '') +
          '</table>';
      } else if (b.t === 'nota') {
        h += '<p class="imp__meta">' + e(b.texto) + '</p>';
      }
    });
    return h + (pie ? '<p class="imp__pie">' + e(pie) + '</p>' : '');
  }

  global.Informe = {
    // Devuelve una promesa con el PDF listo (un Blob).
    pdf: function (bloques, pie) {
      return Promise.all([esperarFuentes(), cargarLogo()]).then(function (r) {
        return armarPDF(dibujar(bloques, r[1], pie));
      });
    },
    html: aHTML,
    // Para las pruebas: las páginas dibujadas, sin envolver.
    _paginas: function (bloques, pie) {
      return Promise.all([esperarFuentes(), cargarLogo()]).then(function (r) {
        return dibujar(bloques, r[1], pie);
      });
    }
  };
})(window);
