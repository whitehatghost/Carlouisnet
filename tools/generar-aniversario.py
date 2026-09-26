# -*- coding: utf-8 -*-
"""Página de aniversario. Ejecutar desde la raíz del proyecto:

    python tools/generar-aniversario.py

Se llama aniversario.html y no 6-anos.html a propósito: el año que viene se
actualiza el contenido y la página conserva los enlaces y el historial que
haya ganado. Una URL nueva cada año empieza de cero.

Sobre la historia: acá NO se inventa nada. Solo va lo que se puede verificar
en el propio sitio —producción en Alajuela, lotes pequeños, sin aditivos, la
feria de los sábados, doce productos—. Si algún día Luis y Carlina cuentan
cómo empezó de verdad, eso vale más que cualquier cosa que yo escriba y hay
que reemplazarlo.
"""
import io, os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
SLUG = "aniversario"
RESENA = "https://g.page/r/CTFj8J32N0aUEBM/review"

POR_SLUG = {p["slug"]: p for p in PRODUCTOS}

# Los seis de la caja cubren todas las categorías y suman exactamente 31.000.
CAJA = ["salsa-habanero-fire", "salsa-pina-habanero", "chimichurri-argentino",
        "pesto-de-albahaca", "alioli", "tomates-deshidratados"]
PRECIO_CAJA = 24000
CAJAS = 30
DESDE, HASTA = "2026-09-29", "2026-10-05"

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")

TITULO = "6 años de CARLOUIS | Caja Aniversario de Edición Limitada"
DESC = ("CARLOUIS cumple 6 años haciendo salsas artesanales en Alajuela. Caja Aniversario con "
        "6 productos por ₡24.000 en vez de ₡31.000, solo 30 cajas, del 29 de setiembre al 5 de "
        "octubre. Envío a todo el país.")

SUMA = sum(int(POR_SLUG[s]["precio_num"]) for s in CAJA)

HISTORIA = [
    "Seis años es mucho tiempo para un negocio de comida hecho a mano. La mayoría no llega. "
    "Producir en lotes pequeños es más caro, más lento y más incómodo que mandar a maquilar, y "
    "cada año aparece la tentación de hacerlo más fácil: meterle un preservante para que aguante "
    "meses en bodega, un espesante para rendir más, un colorante para que se vea parejo.",

    "CARLOUIS no hizo nada de eso, y esa es toda la historia. Las mismas manos, la misma cocina "
    "en Alajuela, los mismos lotes chiquitos. Ninguna de las doce recetas lleva colorantes ni "
    "preservantes artificiales, y por eso hay que refrigerar después de abrir y por eso cuando se "
    "acaba un lote hay que esperar el siguiente. Es la parte incómoda de hacerlo bien.",

    "En estos seis años la línea pasó de unas pocas salsas a doce productos en cuatro categorías: "
    "picantes, pestos y salsas, cremas y mayonesas, y conservas. Se sumaron ferias "
    "—la de los sábados en Plaza Real Alajuela es la de siempre— y hoy se envía a las siete "
    "provincias, al mismo precio en todo el país.",

    "Lo que no cambió: quien cocina es quien contesta el WhatsApp. No hay call center ni "
    "distribuidor en el medio. Si algo sale mal, lo sabe la persona que lo hizo.",
]

GRACIAS = [
    "Nada de esto pasa sin la gente que vuelve. El cliente que se llevó un frasco en la feria, lo "
    "probó, y al mes volvió por dos. La soda que decidió poner una salsa de casa en la mesa en vez "
    "de una industrial. El que regaló una caja y después escribió preguntando cuál era la del "
    "chile morrón.",

    "A ese cliente le queremos pedir una sola cosa por el aniversario, y no es que compre: "
    "que escriba una reseña en Google. Para una marca chiquita eso pesa más que cualquier "
    "publicidad que podamos pagar, y toma menos de un minuto.",
]

FAQ = [
    ("¿Qué trae la Caja 6 Años?",
     "Seis productos, de las cuatro categorías de la línea: Habanero Fire, Piña Habanero, "
     "Chimichurri Argentino, Pesto de Albahaca, Alioli y Tomates Deshidratados. Comprados por separado suman ₡31.000."),
    ("¿Cuánto cuesta y hasta cuándo?",
     "₡24.000, del 29 de setiembre al 5 de octubre de 2026, o hasta que se acaben las 30 cajas. "
     "Lo que pase primero."),
    ("¿Por qué solo 30 cajas?",
     "Porque se producen en lotes pequeños y eso es lo que alcanza sin dejar desabastecido el "
     "resto del catálogo. No es una cifra de mercadeo: es lo que hay."),
    ("¿Se puede cambiar algún producto de la caja?",
     "La caja va armada así para que salga a ese precio. Si querés otra combinación, se puede "
     "hacer un pedido normal del catálogo y te lo cotizamos."),
    ("¿El envío tiene costo?",
     "No. El precio es el mismo para todo el país, sin cargo por envío. Dentro del Gran Área "
     "Metropolitana normalmente 1 o 2 días hábiles, al resto del país de 2 a 4."),
    ("¿Sirve para regalo?",
     "Es de lo que más se pide. Avisanos si es regalo y la preparamos para entregar, con una nota "
     "si querés incluir un mensaje."),
]


def ld():
    url = BASE + SLUG + ".html"
    faq = ",\n          ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in FAQ)
    incluye = ",\n            ".join(
        '{ "@type": "Product", "name": %s }' % json.dumps(POR_SLUG[s]["nombre"], ensure_ascii=False)
        for s in CAJA)
    return '''  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "%(base)s" },
          { "@type": "ListItem", "position": 2, "name": "6 años de CARLOUIS", "item": "%(url)s" }
        ]
      },
      {
        "@type": "Product",
        "name": "Caja 6 Años CARLOUIS",
        "description": "Caja de aniversario con seis productos artesanales CARLOUIS, de las cuatro categorías. Edición limitada a 30 cajas.",
        "image": "%(base)sassets/img/og-carlouis.jpg",
        "brand": { "@type": "Brand", "name": "CARLOUIS" },
        "category": "Canastas y cajas gourmet",
        "isRelatedTo": [
            %(incluye)s
        ],
        "offers": {
          "@type": "Offer",
          "price": "%(precio)d",
          "priceCurrency": "CRC",
          "availability": "https://schema.org/LimitedAvailability",
          "inventoryLevel": { "@type": "QuantitativeValue", "value": %(cajas)d },
          "validFrom": "%(desde)s",
          "priceValidUntil": "%(hasta)s",
          "url": "%(url)s",
          "seller": { "@id": "%(base)s#organization" }
        }
      },
      {
        "@type": "BlogPosting",
        "headline": "Seis años haciendo salsas a mano en Alajuela",
        "description": "CARLOUIS cumple seis años. La historia de una marca que decidió no facilitarse las cosas.",
        "datePublished": "2026-09-25",
        "dateModified": "2026-09-25",
        "inLanguage": "es-CR",
        "image": "%(base)sassets/img/og-carlouis.jpg",
        "mainEntityOfPage": "%(url)s",
        "author": { "@type": "Organization", "name": "CARLOUIS Gourmet", "url": "%(base)s" },
        "publisher": {
          "@type": "Organization",
          "name": "CARLOUIS Gourmet",
          "logo": { "@type": "ImageObject", "url": "%(base)sassets/img/logo.png" }
        }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          %(faq)s
        ]
      }
    ]
  }''' % {"base": BASE, "url": url, "precio": PRECIO_CAJA, "cajas": CAJAS,
          "desde": DESDE, "hasta": HASTA, "faq": faq, "incluye": incluye}


def pagina():
    nav = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', HEADER)

    caja = "\n".join(
        '''          <a class="post-card" href="%(s)s.html">
            <div class="post-card__media" style="background:var(--paper-2);padding:0">
              <picture>
                <source srcset="assets/img/%(img)s.webp" type="image/webp" />
                <img src="assets/img/%(img)s.jpg" alt="%(n)s artesanal CARLOUIS"
                     width="%(w)s" height="%(h)s" loading="lazy"
                     style="width:100%%;aspect-ratio:4/3;object-fit:cover" />
              </picture>
            </div>
            <div class="post-card__body">
              <h3>%(n)s</h3>
              <p>%(perfil)s</p>
              <span class="post-card__more">₡%(precio)s por aparte</span>
            </div>
          </a>''' % {
            "s": s, "img": POR_SLUG[s]["img"], "n": POR_SLUG[s]["nombre"],
            "w": POR_SLUG[s]["w"], "h": POR_SLUG[s]["h"],
            "precio": POR_SLUG[s]["precio"],
            "perfil": POR_SLUG[s]["perfil"].split(".")[0] + ".",
        } for s in CAJA)

    historia = "\n".join('          <p>%s</p>' % t for t in HISTORIA)
    gracias = "\n".join('          <p>%s</p>' % t for t in GRACIAS)
    faqs = "\n".join(
        '''            <details>
              <summary>%s</summary>
              <div class="faq__answer"><p>%s</p></div>
            </details>''' % (q, a) for q, a in FAQ)

    texto_wa = ("Hola! Quiero la Caja 6 A%C3%B1os de aniversario "
                "(%E2%82%A124.000). Mi nombre es: ")

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
  <meta name="geo.region" content="CR-A" />
  <meta name="geo.placename" content="Alajuela, Costa Rica" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="%(titulo)s" />
  <meta property="og:description" content="%(desc)s" />
  <meta property="og:url" content="%(base)s%(slug)s.html" />
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
  <a class="wa-float" href="%(wa)s?text=%(texto)s"
     target="_blank" rel="noopener" aria-label="Pedir la Caja 6 Años por WhatsApp">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Pedir la caja</span>
  </a>
%(nav)s
  <main id="main">

    <article>
      <section class="section section--tight on-dark">
        <div class="container container--narrow" style="text-align:center">
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-star"/></svg>
            29 de setiembre de 2026</span>
          <h1>Seis años<br>haciéndolas a mano</h1>
          <p style="font-size:var(--step-1);max-width:58ch;margin-inline:auto">
            CARLOUIS cumple 6 años. Para celebrarlo armamos una caja con seis productos,
            de las cuatro categorías, a un precio que no vamos a repetir.
          </p>
          <div class="btn-row" style="justify-content:center;margin-top:var(--sp-5)">
            <a class="btn btn--gold" href="%(wa)s?text=%(texto)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir la Caja 6 Años
            </a>
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal style="background:var(--ember-800)">
            <span class="eyebrow"><svg aria-hidden="true"><use href="#i-box"/></svg> Edición limitada</span>
            <h2>Caja 6 Años</h2>
            <p style="font-size:var(--step-1)">
              Seis productos. Por aparte suman <b>₡%(suma)s</b>.<br>
              Esta semana, <b style="font-size:1.4em;color:var(--gold-400)">₡%(precio)s</b>
            </p>
            <ul class="chips" style="justify-content:center">
              <li>Solo %(cajas)d cajas</li>
              <li>Del 29 de setiembre al 5 de octubre</li>
              <li>Envío incluido a todo el país</li>
            </ul>
            <div class="btn-row">
              <a class="btn btn--gold" href="%(wa)s?text=%(texto)s" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Apartar la mía
              </a>
              <a class="btn btn--ghost" href="productos.html">Ver el catálogo</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <h2>Qué trae la caja</h2>
            <p>Las cuatro categorías de la línea. Si nunca has probado CARLOUIS, esta es la
              forma de conocerlo todo de una.</p>
          </div>
          <div class="post-grid">
%(caja)s
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container container--narrow article-body">
          <h2>Seis años haciendo lo difícil</h2>
%(historia)s

          <h2>Gracias, y un favor</h2>
%(gracias)s
          <div class="btn-row" style="margin:var(--sp-5) 0">
            <a class="btn btn--gold" href="%(resena)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-star"/></svg> Dejar una reseña en Google
            </a>
          </div>

          <h2>Preguntas sobre la caja</h2>
          <div class="faq" style="margin-top:var(--sp-5)">
%(faqs)s
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>Son %(cajas)d cajas</h2>
            <p>
              Cuando se acaban, se acaban: producimos en lotes pequeños y eso es lo que hay
              sin dejar desabastecido el resto del catálogo.
            </p>
            <div class="btn-row">
              <a class="btn btn--gold" href="%(wa)s?text=%(texto)s" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Apartar la mía
              </a>
              <a class="btn btn--ghost" href="cobertura.html">Ver cobertura de envíos</a>
            </div>
          </div>
        </div>
      </section>
    </article>

  </main>
%(footer)s</body>
</html>
''' % {
        "csp": CSP, "titulo": TITULO, "desc": DESC, "base": BASE, "slug": SLUG,
        "ld": ld(), "sprite": SPRITE, "nav": nav, "wa": WA, "footer": FOOTER,
        "caja": caja, "historia": historia, "gracias": gracias, "faqs": faqs,
        "suma": "{:,}".format(SUMA).replace(",", "."),
        "precio": "{:,}".format(PRECIO_CAJA).replace(",", "."),
        "cajas": CAJAS, "resena": RESENA, "texto": texto_wa,
    }


if __name__ == "__main__":
    if SUMA != 31000:
        print("  OJO: la caja suma %d, no 31.000. Revisar la lista." % SUMA)
    html = pagina()
    io.open(SLUG + ".html", "w", encoding="utf-8", newline="\n").write(html)
    print("  %s.html  %.1f KB  ~%d palabras" % (SLUG, len(html.encode()) / 1024,
                                                len(re.sub(r"<[^>]+>", " ", html).split())))
    print("  caja: %d productos, suman %s, se venden en %s" % (
        len(CAJA), "{:,}".format(SUMA).replace(",", "."),
        "{:,}".format(PRECIO_CAJA).replace(",", ".")))
