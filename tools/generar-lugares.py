# -*- coding: utf-8 -*-
"""Genera una página por provincia. Ejecutar desde la raíz del proyecto:

    python tools/generar-lugares.py

Cada página apunta a búsquedas del tipo "salsas artesanales en <provincia>",
que hoy no captura nadie del rubro en Costa Rica. El contenido propio de cada
una vive en tools/lugares.py.
"""
import io, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lugares import PROVINCIAS
from lugares_gam import CANTONES as _C1
from lugares_gam2 import CANTONES2 as _C2

CANTONES = _C1 + _C2
from productos import PRODUCTOS
from guias import GUIAS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
POR_SLUG = {p["slug"]: p for p in PRODUCTOS}
GUIA_POR_SLUG = {g["slug"]: g for g in GUIAS}

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")


def ld(p):
    faq = ",\n          ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in p["faq"])
    cantones = ",\n              ".join(
        '{ "@type": "City", "name": %s }' % json.dumps(c, ensure_ascii=False)
        for c in p["cantones"])
    url = BASE + p["slug"] + ".html"
    _LD = '''  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "%(base)s" },
          { "@type": "ListItem", "position": 2, "name": %(padre_nom)s, "item": "%(padre_url)s" },
          { "@type": "ListItem", "position": 3, "name": %(nom)s, "item": "%(url)s" }
        ]
      },
      {
        "@type": "Service",
        "name": %(servicio)s,
        "serviceType": "Venta y entrega de salsas artesanales, pestos y conservas gourmet",
        "description": %(desc)s,
        "url": "%(url)s",
        "provider": { "@id": "%(base)s#organization" },
        "areaServed": [
          { "@type": %(tipo_area)s, "name": %(nomprov)s, "containsPlace": [
              %(cantones)s
            ]%(dentro_de)s
          }
        ],
        "availableChannel": {
          "@type": "ServiceChannel",
          "serviceUrl": "%(url)s",
          "servicePhone": "+506-8825-2608"
        },
        "offers": {
          "@type": "Offer",
          "priceCurrency": "CRC",
          "availability": "https://schema.org/InStock",
          "description": "Mismo precio de catálogo en todo el país, sin cargo por envío."
        }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          %(faq)s
        ]
      }
    ]
  }'''
    # Un cantón es una City dentro de su State; una provincia es el State.
    es_canton = bool(p.get("provincia"))
    return _LD % {
        "base": BASE, "url": url,
        "nom": json.dumps("Salsas artesanales en " + p["nombre"], ensure_ascii=False),
        "tipo_area": json.dumps("City" if es_canton else "State"),
        "nomprov": json.dumps(p["nombre"] if es_canton else "Provincia de " + p["nombre"],
                              ensure_ascii=False),
        "dentro_de": (',\n            "containedInPlace": { "@type": "State", "name": %s }'
                      % json.dumps("Provincia de " + p["provincia"], ensure_ascii=False))
                     if es_canton else "",
        "padre_nom": json.dumps(p["provincia"] if es_canton else "Envíos y cobertura",
                                ensure_ascii=False),
        "padre_url": BASE + (p["provincia_slug"] + ".html" if es_canton else "cobertura.html"),
        "servicio": json.dumps("Entrega de salsas artesanales CARLOUIS en " + p["nombre"],
                               ensure_ascii=False),
        "desc": json.dumps(p["desc"], ensure_ascii=False),
        "cantones": cantones, "faq": faq,
    }


def pagina(p):
    url = BASE + p["slug"] + ".html"
    nav = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', HEADER)
    nav = nav.replace('<a href="cobertura.html">', '<a href="cobertura.html" aria-current="page">')

    intro = "\n".join('          <p>%s</p>' % t for t in p["intro"])
    angulo = "\n".join('          <p>%s</p>' % t for t in p["angulo"])

    prods = "\n".join(
        '''          <a class="post-card" href="%(s)s.html">
            <div class="post-card__media" style="background:var(--paper-2);padding:0">
              <picture>
                <source srcset="assets/img/%(img)s.webp" type="image/webp" />
                <img src="assets/img/%(img)s.jpg" alt="%(n)s artesanal CARLOUIS, con envío a %(prov)s"
                     width="%(w)s" height="%(h)s" loading="lazy"
                     style="width:100%%;aspect-ratio:4/3;object-fit:cover" />
              </picture>
            </div>
            <div class="post-card__body">
              <h3>%(n)s</h3>
              <p>%(porque)s</p>
              <span class="post-card__more">₡%(precio)s &middot; Ver producto <svg aria-hidden="true"><use href="#i-arrow"/></svg></span>
            </div>
          </a>''' % {
            "s": s, "img": POR_SLUG[s]["img"], "n": POR_SLUG[s]["nombre"],
            "w": POR_SLUG[s]["w"], "h": POR_SLUG[s]["h"], "precio": POR_SLUG[s]["precio"],
            "porque": porque, "prov": p["nombre"],
        } for s, porque in p["destacados"])

    cantones = "\n".join(
        '            <li>%s</li>' % c for c in p["cantones"])

    guias = "\n".join(
        '            <li><a href="%s.html">%s</a></li>' % (s, t) for s, t in p["guias"])

    faqs = "\n".join(
        '''            <details>
              <summary>%s</summary>
              <div class="faq__answer"><p>%s</p></div>
            </details>''' % (q, a) for q, a in p["faq"])

    # Desde un cantón se enlaza a los otros cantones del GAM y a su provincia;
    # desde una provincia, a las otras seis.
    if p.get("provincia"):
        vecinos = [(o["slug"], o["nombre"]) for o in CANTONES if o["slug"] != p["slug"]]
        vecinos.append((p["provincia_slug"], "Toda la provincia de " + p["provincia"]))
    else:
        vecinos = [(o["slug"], o["nombre"]) for o in PROVINCIAS if o["slug"] != p["slug"]]
    otras = "\n".join(
        '            <li><a href="%s.html">%s</a></li>' % (sl, nb) for sl, nb in vecinos)

    # Una provincia del GAM anuncia los cantones que tienen página propia.
    hijos = ""
    propios = [c for c in CANTONES if c.get("provincia") == p["nombre"]]
    if propios and not p.get("provincia"):
        enlaces = ", ".join(
            '<a href="%s.html">%s</a>' % (c["slug"], c["nombre"]) for c in propios)
        hijos = ('          <p>Estos cantones tienen su propia página, con tiempos de entrega y lo '
                 'que más se pide ahí: %s.</p>' % enlaces)

    return '''<!DOCTYPE html>
<html lang="es-CR" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <meta http-equiv="Content-Security-Policy" content="%(csp)s">
  <meta http-equiv="X-Content-Type-Options" content="nosniff" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <title>%(titulo)s</title>
  <meta name="description" content="%(desc)s" />
  <link rel="canonical" href="%(url)s" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="geo.region" content="%(geo)s" />
  <meta name="geo.placename" content="%(nombre)s, Costa Rica" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="%(titulo)s" />
  <meta property="og:description" content="%(desc)s" />
  <meta property="og:url" content="%(url)s" />
  <meta property="og:image" content="%(base)sassets/img/og-carlouis.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(titulo)s" />
  <meta name="twitter:description" content="%(desc)s" />
  <meta name="twitter:image" content="%(base)sassets/img/og-carlouis.jpg" />

  <meta name="theme-color" content="#4A1206" />
  <link rel="icon" href="favicon.ico" sizes="any" />
  <link rel="icon" href="assets/img/icon-192.png" type="image/png" />
  <link rel="apple-touch-icon" href="assets/img/icon-180.png" />
  <link rel="manifest" href="site.webmanifest" />

  <link rel="preload" href="assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="assets/fonts/karla-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="assets/css/styles.css" />
  <script src="assets/js/main.js" defer></script>
  <script src="assets/js/analytics.js" defer></script>

  <script type="application/ld+json">
%(ld)s
  </script>
</head>

<body>
  <a class="skip-link" href="#main">Saltar al contenido principal</a>

%(sprite)s
  <a class="wa-float" href="%(wa)s?text=Hola%%2C%%20quiero%%20hacer%%20un%%20pedido%%20a%%20%(nombre_url)s"
     target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp al 8825 2608">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Pedí por WhatsApp</span>
  </a>
%(nav)s
  <main id="main">

    <article>
      <section class="section section--tight on-dark">
        <div class="container container--narrow" style="text-align:center">
          <nav class="breadcrumb" aria-label="Ruta de navegación" style="margin-bottom:1rem;font-size:.9rem">
            <a href="index.html" style="color:var(--gold-400);text-decoration:none">Inicio</a>
            <span style="color:#C4AE95"> / </span>
            <a href="%(padre_url)s" style="color:var(--gold-400);text-decoration:none">%(padre)s</a>
            <span style="color:#C4AE95"> / %(nombre)s</span>
          </nav>
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-pin"/></svg> %(etiqueta)s</span>
          <h1>%(h1)s</h1>
          <p style="font-size:var(--step-1);max-width:62ch;margin-inline:auto">%(lead)s</p>
          <div class="btn-row" style="justify-content:center;margin-top:var(--sp-5)">
            <a class="btn btn--gold" href="%(wa)s?text=Hola%%2C%%20quiero%%20hacer%%20un%%20pedido%%20a%%20%(nombre_url)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir por WhatsApp
            </a>
            <a class="btn btn--ghost" href="productos.html">Ver el catálogo</a>
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container container--narrow article-body">
          <div class="article-meta">
            <span><svg aria-hidden="true"><use href="#i-truck"/></svg> %(entrega_titulo)s</span>
            <span><svg aria-hidden="true"><use href="#i-check"/></svg> Mismo precio en todo el país</span>
            <span><svg aria-hidden="true"><use href="#i-phone"/></svg> SINPE, transferencia o efectivo</span>
          </div>

%(intro)s

          <h2>Cómo llega el pedido a %(nombre)s</h2>
          <p>%(entrega)s</p>
          <p>
            El precio que ves en el catálogo es el que pagás, sin cargo por envío y sin importar el
            cantón. Coordinamos todo por WhatsApp al <a href="tel:+50688252608">8825&nbsp;2608</a> y
            confirmamos el pedido apenas entra el comprobante de SINPE Móvil o transferencia.
            Podés ver <a href="cobertura.html">la cobertura completa del país</a> si necesitás
            comparar con otra provincia.
          </p>

          <h2>%(angulo_h2)s</h2>
%(angulo)s
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <h2>Los que más se piden en %(nombre)s</h2>
            <p>De los doce productos de la línea, estos cuatro son los que mejor calzan acá.</p>
          </div>
          <div class="post-grid">
%(prods)s
          </div>
          <p style="text-align:center;margin-top:var(--sp-6)">
            <a class="btn btn--primary" href="productos.html">Ver los 12 productos <svg aria-hidden="true"><use href="#i-arrow"/></svg></a>
          </p>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container container--narrow article-body">
          <h2>%(titulo_zonas)s</h2>
          <p>
            %(intro_zonas)s
          </p>
          <ul class="chips">
%(cantones)s
          </ul>
%(hijos)s

          <h2>Para leer antes de pedir</h2>
          <ul>
%(guias)s
          </ul>

          <h2>Preguntas frecuentes en %(nombre)s</h2>
          <div class="faq" style="margin-top:var(--sp-5)">
%(faqs)s
          </div>

          <h2>¿Estás en otra provincia?</h2>
          <ul>
%(otras)s
          </ul>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>Hacé tu pedido a %(nombre)s</h2>
            <p>
              Escribinos qué querés y a qué cantón va. Te confirmamos disponibilidad y tiempo de
              entrega en el momento.
            </p>
            <div class="btn-row">
              <a class="btn btn--gold" href="%(wa)s?text=Hola%%2C%%20quiero%%20hacer%%20un%%20pedido%%20a%%20%(nombre_url)s" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir por WhatsApp
              </a>
              <a class="btn btn--ghost" href="mayoreo.html">Precios de mayoreo</a>
            </div>
          </div>
        </div>
      </section>
    </article>

  </main>
%(footer)s</body>
</html>
''' % {
        "csp": CSP, "titulo": p["titulo"], "desc": p["desc"], "url": url, "base": BASE,
        "geo": p["geo"], "nombre": p["nombre"],
        "nombre_url": p["nombre"].replace(" ", "%20").replace("é", "%C3%A9"),
        "h1": p["h1"], "lead": p["lead"], "ld": ld(p), "sprite": SPRITE, "nav": nav,
        "wa": WA, "footer": FOOTER, "intro": intro, "angulo": angulo,
        "angulo_h2": p["angulo_h2"], "entrega": p["entrega"],
        "entrega_titulo": p["entrega_titulo"], "prods": prods, "cantones": cantones,
        "guias": guias, "faqs": faqs, "otras": otras, "hijos": hijos,
        "ncantones": len(p["cantones"]),
        "padre": p["provincia"] if p.get("provincia") else "Envíos",
        "padre_url": (p["provincia_slug"] + ".html") if p.get("provincia") else "cobertura.html",
        "etiqueta": ("Cantón de " + p["provincia"]) if p.get("provincia")
                    else ("%d cantones" % len(p["cantones"])),
        "titulo_zonas": ("Zonas de %s donde entregamos" % p["nombre"]) if p.get("provincia")
                        else ("Cantones de %s a los que llegamos" % p["nombre"]),
        "intro_zonas": ("Entregamos en todo el cantón. Estas son las zonas donde ya hemos dejado "
                        "pedidos:" if p.get("provincia") else
                        "Enviamos a los %d cantones de la provincia. Si el tuyo aparece, ya hemos "
                        "mandado pedidos ahí:" % len(p["cantones"])),
    }


if __name__ == "__main__":
    total = 0
    for p in PROVINCIAS + CANTONES:
        destino = p["slug"] + ".html"
        html = pagina(p)
        io.open(destino, "w", encoding="utf-8", newline="\n").write(html)
        palabras = len(re.sub(r"<[^>]+>", " ", html).split())
        print("  %-38s %5.1f KB  ~%d palabras" % (destino, len(html.encode()) / 1024, palabras))
        total += 1
    print("\n%d páginas de lugar generadas." % total)
