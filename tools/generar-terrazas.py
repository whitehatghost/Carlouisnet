# -*- coding: utf-8 -*-
"""Genera la página de CARLOUIS en la Feria de Culturas de Terrazas Lindora
(2, 3 y 4 de octubre de 2026). "Feria de Culturas" es el nombre con que Terrazas
la promociona ("un recorrido por el mundo, sin salir de Terrazas Lindora"), así
que es lo que la gente va a buscar.

    python tools/generar-terrazas.py

Datos confirmados por Luis y Carlina: viernes 2 a domingo 4 de octubre, de
11:00 a.m. a 7:00 p.m. No se afirma en qué punto de Terrazas queda el stand:
para eso está el WhatsApp.

Cuando pase la feria: cambiar PASADA a True y volver a correr. La página queda
como registro de "así fue", igual que Forum 2 y Ananta.
"""
import io, os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
SLUG = "feria-terrazas-lindora"
PASADA = False

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")

if PASADA:
    TITULO = "Así fue la Feria de Culturas en Terrazas Lindora | CARLOUIS"
    DESC = ("Del 2 al 4 de octubre estuvimos en la Feria de Culturas de Terrazas Lindora, "
            "Santa Ana, con degustación de salsas artesanales. Mirá dónde estamos ahora.")
    H1 = "Estuvimos en la Feria de Culturas de Terrazas Lindora"
    EYEBROW = "Feria finalizada &middot; Lindora, Santa Ana"
else:
    TITULO = "Feria de Culturas en Terrazas Lindora | CARLOUIS"
    DESC = ("CARLOUIS estará en la Feria de Culturas de Terrazas Lindora del 2 al 4 de "
            "octubre, de 11 a.m. a 7 p.m., con degustación de salsas artesanales.")
    H1 = "Nos vemos en la Feria de Culturas de Terrazas Lindora"
    EYEBROW = "Próxima feria &middot; Lindora, Santa Ana"

WAZE = "https://waze.com/ul?q=Terrazas%20Lindora%20Santa%20Ana&navigate=yes"
MAPS = "https://www.google.com/maps/search/?api=1&query=Terrazas+Lindora+Santa+Ana+Costa+Rica"
WA_APARTAR = WA + "?text=Hola%2C%20voy%20a%20pasar%20por%20Terrazas%20Lindora%20y%20quiero%20apartar%3A%20"

FAQ = [
    ("¿Qué es la Feria de Culturas de Terrazas Lindora?",
     "Es la feria con que Terrazas Lindora propone un recorrido por el mundo sin salir del centro comercial. CARLOUIS participa con su stand de salsas artesanales hechas en Costa Rica."),
    ("¿Cuándo está CARLOUIS en Terrazas Lindora?",
     "El viernes 2, el sábado 3 y el domingo 4 de octubre de 2026, de 11:00 a.m. a 7:00 p.m."),
    ("¿Dónde queda Terrazas Lindora?",
     "En Lindora, Santa Ana. Desde esta página lo abrís directo en Waze o en Google Maps. Si no das con el stand, escribinos al 8825 2608."),
    ("¿Se puede probar antes de comprar?",
     "Sí. En el stand hay degustación de las salsas, los pestos y las conservas."),
    ("¿Cómo se paga en el stand?",
     "Aceptamos SINPE Móvil al 8825 2608, transferencia y efectivo."),
    ("¿Puedo apartar productos para recogerlos en Terrazas?",
     "Sí. Escribinos por WhatsApp con lo que querés y te lo dejamos separado para que solo pasés a recogerlo."),
    ("¿Y el sorteo de los 6 años?",
     "Sorteamos una canasta con 6 frascos de pesto de tomate, alioli, salsa de chile dulce y tomates deshidratados. Se participa en Instagram (@carlouis_cr) y el sorteo es el lunes 12 de octubre."),
]

DESTACADOS = [
    ("pesto-de-tomate", "Pesto de Tomate", "Denso y concentrado. Para pasta, pizza y como dip."),
    ("alioli", "Alioli", "Cremoso, con el ajo presente. Papas, pan y mariscos."),
    ("salsa-de-chile-dulce", "Salsa de Chile Dulce", "El glaseado para pollo y cerdo."),
    ("tomates-deshidratados", "Tomates Deshidratados", "En aceite de oliva, listos para pasta, tablas y pan."),
]


def ld():
    faq = ",\n          ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False)) for q, a in FAQ)
    url = BASE + SLUG + ".html"
    return '''  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "%(base)s" },
          { "@type": "ListItem", "position": 2, "name": "Eventos", "item": "%(base)seventos.html" },
          { "@type": "ListItem", "position": 3, "name": "Terrazas Lindora", "item": "%(url)s" }
        ]
      },
      {
        "@type": "Event",
        "name": "CARLOUIS en la Feria de Culturas de Terrazas Lindora",
        "description": %(desc)s,
        "startDate": "2026-10-02T11:00:00-06:00",
        "endDate": "2026-10-04T19:00:00-06:00",
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "image": "%(base)sassets/img/carlouis-6-anos-og.jpg",
        "url": "%(url)s",
        "isAccessibleForFree": true,
        "inLanguage": "es-CR",
        "location": {
          "@type": "Place",
          "name": "Terrazas Lindora",
          "address": {
            "@type": "PostalAddress",
            "addressLocality": "Lindora, Santa Ana",
            "addressRegion": "San José",
            "addressCountry": "CR"
          }
        },
        "organizer": { "@id": "%(base)s#organization" },
        "performer": { "@type": "Organization", "name": "CARLOUIS Gourmet" },
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "CRC",
          "availability": "https://schema.org/InStock",
          "validFrom": "2026-09-29",
          "url": "%(url)s",
          "description": "Degustación gratuita."
        }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          %(faq)s
        ]
      }
    ]
  }''' % {"base": BASE, "url": url, "desc": json.dumps(DESC, ensure_ascii=False), "faq": faq}


def pagina():
    nav = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', HEADER)

    dest = "\n".join(
        '            <li><a href="%s.html"><strong>%s</strong></a> &mdash; %s</li>' % d for d in DESTACADOS)
    faqs = "\n".join(
        '''            <details>
              <summary>%s</summary>
              <div class="faq__answer"><p>%s</p></div>
            </details>''' % (q, a) for q, a in FAQ)

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
  <link rel="canonical" href="%(base)s%(slug)s.html" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="geo.region" content="CR-SJ" />
  <meta name="geo.placename" content="Lindora, Santa Ana, Costa Rica" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="%(titulo)s" />
  <meta property="og:description" content="%(desc)s" />
  <meta property="og:url" content="%(base)s%(slug)s.html" />
  <meta property="og:image" content="%(base)sassets/img/carlouis-6-anos-og.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(titulo)s" />
  <meta name="twitter:description" content="%(desc)s" />
  <meta name="twitter:image" content="%(base)sassets/img/carlouis-6-anos-og.jpg" />

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
  <a class="wa-float" href="%(wa_apartar)s"
     target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp al 8825 2608">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Apartá por WhatsApp</span>
  </a>
%(nav)s
  <main id="main">

    <article>
      <section class="section section--tight on-dark">
        <div class="container container--narrow" style="text-align:center">
          <nav class="breadcrumb" aria-label="Ruta de navegación" style="margin-bottom:1rem;font-size:.9rem">
            <a href="index.html" style="color:var(--gold-400);text-decoration:none">Inicio</a>
            <span style="color:#C4AE95"> / </span>
            <a href="eventos.html" style="color:var(--gold-400);text-decoration:none">Eventos</a>
            <span style="color:#C4AE95"> / Feria de Culturas</span>
          </nav>
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-calendar"/></svg> %(eyebrow)s</span>
          <h1>%(h1)s</h1>
          <p style="font-size:var(--step-1);max-width:62ch;margin-inline:auto">
            Del <strong>viernes 2 al domingo 4 de octubre</strong>, de <strong>11:00 a.m. a
            7:00 p.m.</strong>, estamos en la <strong>Feria de Culturas</strong> de Terrazas
            Lindora, Santa Ana, con degustación de toda la línea. Justo en la semana de nuestro
            sexto aniversario.
          </p>
          <div class="btn-row" style="justify-content:center;margin-top:var(--sp-5)">
            <a class="btn btn--gold" href="%(waze)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-nav"/></svg> Abrir en Waze
            </a>
            <a class="btn btn--ghost" href="%(maps)s" target="_blank" rel="noopener">Google Maps</a>
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container container--narrow article-body">
          <div class="article-meta">
            <span><svg aria-hidden="true"><use href="#i-calendar"/></svg> 2 &ndash; 4 de octubre de 2026</span>
            <span><svg aria-hidden="true"><use href="#i-clock"/></svg> 11:00 a.m. a 7:00 p.m.</span>
            <span><svg aria-hidden="true"><use href="#i-pin"/></svg> Lindora, Santa Ana</span>
          </div>

          <figure style="margin:0 0 var(--sp-6)">
            <picture>
              <source srcset="assets/img/feria-culturas-terrazas.webp" type="image/webp" />
              <img src="assets/img/feria-culturas-terrazas.jpg" width="1024" height="754" loading="lazy"
                   alt="Afiche de la Feria de Culturas en Terrazas Lindora: un recorrido por el mundo sin salir de Terrazas Lindora"
                   style="width:100%%;height:auto;border-radius:var(--r-lg);box-shadow:var(--sh-2)" />
            </picture>
            <figcaption style="font-size:.88rem;color:var(--ink-mute);margin-top:.5rem">Afiche de la feria, de Terrazas Lindora.</figcaption>
          </figure>

          <h2>Un recorrido por el mundo, en frascos hechos en Costa Rica</h2>
          <p>
            La feria propone darle la vuelta al mundo sin salir de Terrazas, y nuestra mesa
            calza perfecto: buena parte de lo que hacemos son recetas de otros países,
            cocinadas en Alajuela, en lotes pequeños.
          </p>
          <ul>
            <li><a href="chimichurri-argentino.html"><strong>Argentina</strong></a> &mdash; el chimichurri de parrilla, con perejil, ajo, orégano y aceite de oliva.</li>
            <li><a href="pesto-de-albahaca.html"><strong>Italia</strong></a> &mdash; el pesto de albahaca, el <a href="pesto-de-tomate.html">pesto de tomate</a> y los <a href="tomates-deshidratados.html">tomates deshidratados</a> en aceite de oliva.</li>
            <li><a href="alioli.html"><strong>El Mediterráneo</strong></a> &mdash; el alioli, que en catalán quiere decir ajo y aceite.</li>
            <li><a href="mayonesa-de-chipotle.html"><strong>México</strong></a> &mdash; el chipotle, en nuestra mayonesa ahumada.</li>
            <li><a href="salsa-habanero-fire.html"><strong>El Caribe</strong></a> &mdash; el chile habanero, en la Habanero Fire y la <a href="salsa-pina-habanero.html">Piña Habanero</a>.</li>
            <li><a href="mayonesa-de-culantro.html"><strong>Costa Rica</strong></a> &mdash; y de acá, la mayonesa de culantro y la <a href="salsa-de-mora.html">salsa de mora</a>.</li>
          </ul>

          <h2>Qué vas a probar</h2>
          <p>
            Llevamos la línea completa para que probés antes de decidir. Si es la primera vez,
            empezá por los cuatro por los que más nos conocen:
          </p>
          <ul>
%(dest)s
          </ul>
          <p>
            Además, las salsas de habanero, el chimichurri, el pesto de albahaca, las mayonesas
            de chipotle y de culantro, el chile morrón asado y la salsa de mora.
            <a href="productos.html">Mirá el catálogo con precios</a> para ir viendo qué te
            interesa.
          </p>

          <h2>Estamos cumpliendo 6 años</h2>
          <p>
            CARLOUIS cumplió seis años el 29 de setiembre, y lo celebramos con un
            <a href="carlouis-cumple-6-anos.html#sorteo">sorteo de una canasta con 6 frascos</a>
            de esos mismos cuatro: pesto de tomate, alioli, salsa de chile dulce y tomates
            deshidratados. Se participa en Instagram, en
            <a href="https://instagram.com/carlouis_cr" target="_blank" rel="noopener">@carlouis_cr</a>,
            y el sorteo es el lunes 12 de octubre.
          </p>

          <h2>Cómo llegar a Terrazas Lindora</h2>
          <p>
            Terrazas Lindora está en Lindora, Santa Ana, a pocos minutos de Escazú, Belén y la
            Radial. Tocá el botón que usés normalmente y te lleva directo:
          </p>
          <div class="btn-row" style="margin:var(--sp-5) 0">
            <a class="btn btn--waze" href="%(waze)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-nav"/></svg> Abrir en Waze
            </a>
            <a class="btn btn--maps" href="%(maps)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-pin"/></svg> Abrir en Google Maps
            </a>
          </div>
          <p>
            Si no das con el stand, escribinos por WhatsApp al
            <a href="tel:+50688252608">8825 2608</a> y te decimos exactamente dónde estamos.
          </p>

          <h2>Si no podés llegar</h2>
          <p>
            Te lo enviamos. En <a href="salsas-artesanales-santa-ana.html">Santa Ana y Lindora</a>
            y en <a href="salsas-artesanales-escazu.html">Escazú</a> la entrega es de 1 a 2 días,
            y enviamos a <a href="cobertura.html">todo el país</a>. También nos encontrás en
            <a href="eventos.html">otras ferias</a>.
          </p>

          <h2>Preguntas frecuentes</h2>
          <div class="faq" style="margin-top:var(--sp-5)">
%(faqs)s
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>Apartá lo tuyo antes de llegar</h2>
            <p>
              Escribinos por WhatsApp con lo que querés y te lo dejamos separado en el stand de
              Terrazas Lindora.
            </p>
            <div class="btn-row">
              <a class="btn btn--gold" href="%(wa_apartar)s" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Apartar por WhatsApp
              </a>
              <a class="btn btn--ghost" href="productos.html">Ver los productos</a>
            </div>
          </div>
        </div>
      </section>
    </article>

  </main>
%(footer)s</body>
</html>
''' % {
        "csp": CSP, "titulo": TITULO, "desc": DESC, "base": BASE, "slug": SLUG, "h1": H1,
        "eyebrow": EYEBROW, "ld": ld(), "sprite": SPRITE, "nav": nav, "footer": FOOTER,
        "waze": WAZE, "maps": MAPS, "wa_apartar": WA_APARTAR, "dest": dest, "faqs": faqs,
    }


if __name__ == "__main__":
    html = pagina()
    io.open(SLUG + ".html", "w", encoding="utf-8", newline="\n").write(html)
    palabras = len(re.sub(r"<[^>]+>", " ", html).split())
    print("  %s.html  %.1f KB  ~%d palabras" % (SLUG, len(html.encode()) / 1024, palabras))
