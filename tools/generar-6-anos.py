# -*- coding: utf-8 -*-
"""Genera la entrada de blog por los 6 años de CARLOUIS (29 de setiembre de 2026).

    python tools/generar-6-anos.py

Es distinta de aniversario.html (la Caja 6 Años con precio, que no se aprobó).
Lo que Luis aprobó es un SORTEO de una sola canasta de 6 frascos con los cuatro
productos por los que más los conocen (pesto de tomate, alioli, salsa de chile dulce y tomates deshidratados): se participa en Instagram y se sortea el lunes 12 de octubre.
Después del sorteo: cambiar la sección #sorteo por el nombre de quien ganó y volver a correr.

Además de celebrar, trabaja la marca en Google: responde "desde cuándo existe",
"dónde se compra" y "dónde se hace", y pide reseñas, que es lo que más pesa en
el perfil de Google Business.
"""
import io, os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
RESENA = "https://g.page/r/CTFj8J32N0aUEBM/review"
SLUG = "carlouis-cumple-6-anos"
FECHA = "2026-09-29"
INSTAGRAM = "https://instagram.com/carlouis_cr"

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")

TITULO = "CARLOUIS cumple 6 años | Salsas artesanales desde 2020"
DESC = ("CARLOUIS cumple 6 años haciendo salsas artesanales en Alajuela, Costa Rica, y lo "
        "celebra sorteando una canasta con 6 frascos de sus favoritos. Así se participa.")

POR_SLUG = {p["slug"]: p for p in PRODUCTOS}

CATEGORIAS = [
    ("Picantes", ["salsa-habanero-fire", "salsa-pina-habanero", "salsa-de-chile-dulce"]),
    ("Pestos y salsas", ["pesto-de-albahaca", "pesto-de-tomate", "chimichurri-argentino"]),
    ("Cremas y mayonesas", ["alioli", "mayonesa-de-chipotle", "mayonesa-de-culantro"]),
    ("Conservas", ["tomates-deshidratados", "chile-morron-asado", "salsa-de-mora"]),
]

# Seis para empezar: una recomendación, no un ranking de ventas.
SEIS = [
    ("salsa-pina-habanero", "La que más sorprende la primera vez: la piña entra dulce y el habanero llega después. Para cerdo, pollo y tacos."),
    ("chimichurri-argentino", "Perejil, ajo, orégano y aceite de oliva. Para la carne, sí, pero también para papas, patacones y pan."),
    ("pesto-de-albahaca", "Albahaca y aceite de oliva, sin espesantes. Dos cucharadas a la pasta, siempre fuera del fuego."),
    ("alioli", "Cremoso y con el ajo presente. Se compra para las papas y se termina usando en todo."),
    ("tomates-deshidratados", "Tomate concentrado hasta quedar dulce, en aceite de oliva. Y el aceite del frasco también se usa."),
    ("salsa-de-mora", "La única dulce de la línea, con la acidez de la mora. Con queso maduro, helado o cerdo."),
]

FAQ = [
    ("¿Cómo participo en el sorteo de los 6 años?",
     "Seguí a @carlouis_cr en Instagram, dale like a la publicación del aniversario y etiquetá a dos amigos en los comentarios. El sorteo es el lunes 12 de octubre de 2026."),
    ("¿Qué se gana en el sorteo?",
     "Una canasta con seis frascos CARLOUIS de los cuatro productos por los que más nos conocen: pesto de tomate, alioli, salsa de chile dulce y tomates deshidratados."),
    ("¿Desde cuándo existe CARLOUIS?",
     "Desde el 29 de setiembre de 2020. En 2026 cumplimos seis años haciendo salsas, pestos y conservas artesanales en Costa Rica."),
    ("¿Dónde se hacen los productos CARLOUIS?",
     "En Alajuela, Costa Rica, en lotes pequeños y sin colorantes ni aditivos artificiales."),
    ("¿Dónde se compran los productos CARLOUIS?",
     "Todos los sábados de 6:00 a.m. a 1:00 p.m. en la Feria Orgánica La Verbena, en Plaza Real Alajuela, y por WhatsApp al 8825 2608 con envío a todo el país."),
    ("¿CARLOUIS está en supermercados?",
     "No. Vendemos directo: en feria, en ferias de temporada y por pedido con envío. Así el producto llega fresco y hablás directo con quien lo hace."),
    ("¿Cuántos productos tiene CARLOUIS?",
     "Doce, en cuatro categorías: picantes, pestos y salsas, cremas y mayonesas, y conservas."),
    ("¿Venden al por mayor?",
     "Sí, a restaurantes, sodas, hoteles y tiendas gourmet. Las condiciones están en la página de mayoreo."),
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
          { "@type": "ListItem", "position": 2, "name": "CARLOUIS cumple 6 años", "item": "%(url)s" }
        ]
      },
      {
        "@type": "BlogPosting",
        "headline": "CARLOUIS cumple 6 años",
        "description": %(desc)s,
        "image": ["%(base)sassets/img/carlouis-6-anos.jpg", "%(base)sassets/img/carlouis-6-anos-og.jpg"],
        "datePublished": "%(fecha)s",
        "dateModified": "%(fecha)s",
        "inLanguage": "es-CR",
        "mainEntityOfPage": "%(url)s",
        "author": { "@id": "%(base)s#organization" },
        "publisher": { "@id": "%(base)s#organization" },
        "about": { "@id": "%(base)s#organization" }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          %(faq)s
        ]
      }
    ]
  }''' % {"base": BASE, "url": url, "desc": json.dumps(DESC, ensure_ascii=False),
          "fecha": FECHA, "faq": faq}


def pagina():
    nav = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', HEADER)

    cats = "\n".join(
        '''          <div class="value" data-reveal>
            <h3>%s</h3>
            <ul class="chips">
%s
            </ul>
          </div>''' % (nombre, "\n".join(
            '              <li><a href="%s.html" style="color:inherit;text-decoration:none">%s</a></li>'
            % (s, POR_SLUG[s]["nombre"]) for s in slugs)) for nombre, slugs in CATEGORIAS)

    seis = "\n".join(
        '''          <a class="post-card" href="%(s)s.html" data-reveal>
            <div class="post-card__media" style="padding:0">
              <picture>
                <source srcset="assets/img/%(img)s.webp" type="image/webp" />
                <img src="assets/img/%(img)s.jpg" alt="%(n)s artesanal CARLOUIS" loading="lazy"
                     style="width:100%%;aspect-ratio:4/3;object-fit:cover" />
              </picture>
            </div>
            <div class="post-card__body">
              <span class="post-card__date">%(i)d de 6</span>
              <h3>%(n)s</h3>
              <p>%(t)s</p>
              <span class="post-card__more">Ver producto <svg aria-hidden="true"><use href="#i-arrow"/></svg></span>
            </div>
          </a>''' % {"s": s, "img": POR_SLUG[s]["img"], "n": POR_SLUG[s]["nombre"], "t": t, "i": i}
        for i, (s, t) in enumerate(SEIS, 1))

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
  <meta name="geo.region" content="CR-A" />
  <meta name="geo.placename" content="Alajuela, Costa Rica" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="%(titulo)s" />
  <meta property="og:description" content="%(desc)s" />
  <meta property="og:url" content="%(base)s%(slug)s.html" />
  <meta property="og:image" content="%(base)sassets/img/carlouis-6-anos-og.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="article:published_time" content="%(fecha)s" />
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
  <a class="wa-float" href="%(wa)s?text=Hola%%2C%%20vi%%20que%%20CARLOUIS%%20cumple%%206%%20a%%C3%%B1os%%20y%%20quiero%%20hacer%%20un%%20pedido"
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
            <span style="color:#C4AE95"> / 6 años</span>
          </nav>
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-calendar"/></svg>
            <time datetime="%(fecha)s">29 de setiembre de 2026</time> &middot; Aniversario</span>
          <h1>CARLOUIS cumple 6 años</h1>
          <p style="font-size:var(--step-1);max-width:62ch;margin-inline:auto">
            Seis años haciendo salsas, pestos y conservas artesanales en Alajuela, frasco por
            frasco y feria por feria. Lo celebramos dando las gracias y sorteando una canasta
            con <strong>seis frascos de nuestros favoritos</strong>.
          </p>
          <div class="btn-row" style="justify-content:center;margin-top:var(--sp-5)">
            <a class="btn btn--gold" href="#sorteo">Cómo participar</a>
          </div>
        </div>
      </section>

      <section class="section section--alt" id="sorteo">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <span class="eyebrow"><svg aria-hidden="true"><use href="#i-star"/></svg> Sorteo de aniversario</span>
            <h2>Una canasta con 6 frascos de lo que más nos piden</h2>
            <p>
              Seis años, seis frascos, de los cuatro por los que más nos conocen: <a href="pesto-de-tomate.html">pesto de tomate</a>, <a href="alioli.html">alioli</a>, <a href="salsa-de-chile-dulce.html">salsa de chile dulce</a> y <a href="tomates-deshidratados.html">tomates deshidratados</a>.
            </p>
          </div>
          <div class="cta on-dark" data-reveal style="text-align:left">
          <ol class="steps">
            <li class="step">
              <b>Seguí a @carlouis_cr en Instagram</b>
              <p><a href="%(ig)s" target="_blank" rel="noopener" style="color:var(--gold-400)">instagram.com/carlouis_cr</a></p>
            </li>
            <li class="step">
              <b>Dale like a la publicación de los 6 años</b>
              <p>Es la publicación del aniversario, la del 6 dorado.</p>
            </li>
            <li class="step">
              <b>Etiquetá a dos amigos en los comentarios</b>
              <p>Cada comentario con dos amigos distintos cuenta como una participación.</p>
            </li>
          </ol>
          </div>
          <p data-reveal style="text-align:center;margin-top:var(--sp-5)">
            <strong>Sorteo: lunes 12 de octubre de 2026.</strong> Anunciamos a quien gane en
            Instagram y le escribimos para coordinar la entrega. Participan personas en Costa Rica.
          </p>
          <div class="btn-row" data-reveal style="justify-content:center">
            <a class="btn btn--primary" href="%(ig)s" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-instagram"/></svg> Participar en Instagram
            </a>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container split">
          <div data-reveal>
            <span class="eyebrow"><svg aria-hidden="true"><use href="#i-leaf"/></svg> Desde 2020</span>
            <h2>Seis años, frasco por frasco</h2>
            <p>
              CARLOUIS empezó el <strong>29 de setiembre de 2020</strong> en Alajuela, con una idea
              que no ha cambiado: que una salsa de verdad no necesita colorantes, espesantes ni
              nombres impronunciables en la etiqueta. Solo buen producto, tiempo y manos que
              saben lo que hacen.
            </p>
            <p>
              Seguimos cocinando en lotes pequeños. Es más lento y no permite tener bodegas
              llenas, pero es lo que hace que el pesto huela a albahaca recién cortada, que el
              tomate deshidratado todavía sepa a tomate y que el habanero pique como debe picar.
            </p>
            <p>
              Hoy son <strong>doce productos en cuatro categorías</strong>, una mesa todos los
              sábados en la feria La Verbena, ferias de temporada en el Valle Central y
              envíos a las siete provincias. Todo eso lo construyeron las personas que nos
              probaron una vez, volvieron y nos recomendaron.
            </p>
          </div>
          <div data-reveal>
            <picture>
              <source srcset="assets/img/carlouis-6-anos.webp" type="image/webp" />
              <img src="assets/img/carlouis-6-anos.jpg" width="1080" height="1350"
                   alt="CARLOUIS cumple 6 años de salsas hechas a mano, 2020 a 2026"
                   style="border-radius:var(--r-xl);box-shadow:var(--sh-3);width:100%%;height:auto" />
            </picture>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <h2>Seis para empezar</h2>
            <p>Si nunca nos has probado, o si ya estás pensando qué escoger para tu canasta, estas son seis por donde arrancar.</p>
          </div>
          <div class="post-grid">
%(seis)s
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <h2>La línea completa, seis años después</h2>
            <p>Doce productos en cuatro categorías. Tocá cualquiera para ver cómo se usa.</p>
          </div>
          <div class="value-grid">
%(cats)s
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Dónde nos encontrás</h2>
          </div>
          <div data-reveal>
            <p>
              <strong>Todos los sábados</strong>, de 6:00 a.m. a 1:00 p.m., en la
              <a href="encuentranos.html">Feria Orgánica La Verbena, Plaza Real Alajuela</a>. Ahí
              se prueba todo antes de comprar.
            </p>
            <p>
              <strong>Del 2 al 4 de octubre</strong>, de 11:00 a.m. a 7:00 p.m., en
              <a href="feria-terrazas-lindora.html">Feria de Culturas de Terrazas Lindora</a>, en Santa Ana, con
              degustación. Es la semana del aniversario.
            </p>
            <p>
              <strong>En ferias de temporada</strong>, como la de
              <a href="feria-forum-2-lindora.html">Forum 2 en Lindora</a> o la
              <a href="feria-ananta-yoga-heredia.html">Feria Holística de Ananta Yoga en Heredia</a>.
              Las próximas las anunciamos en <a href="eventos.html">eventos</a>.
            </p>
            <p>
              <strong>Por WhatsApp</strong>, con <a href="cobertura.html">envío a todo el país</a>:
              <a href="salsas-artesanales-san-jose.html">San José</a>,
              <a href="salsas-artesanales-alajuela.html">Alajuela</a>,
              <a href="salsas-artesanales-heredia.html">Heredia</a>,
              <a href="salsas-artesanales-escazu.html">Escazú</a> y el resto de cantones.
            </p>
            <p>
              <strong>Para negocios</strong>, al <a href="mayoreo.html">por mayor</a>, para
              restaurantes, sodas, hoteles y tiendas gourmet.
            </p>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Un favor de cumpleaños</h2>
          </div>
          <div data-reveal>
            <p>
              Si en estos seis años alguna salsa nuestra te acompañó una parrillada, una pasta
              o una tabla con amigos, lo que más nos ayuda a seguir es que lo contés. Una reseña
              en Google hace que la próxima persona que busca salsas artesanales en Costa Rica
              nos encuentre.
            </p>
            <div class="btn-row">
              <a class="btn btn--primary" href="%(resena)s" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-star"/></svg> Dejar una reseña en Google
              </a>
              <a class="btn btn--ghost" href="testimonios.html">Leer lo que dicen otros</a>
            </div>
            <p style="margin-top:var(--sp-6)">Gracias por estos seis años.<br><strong>Luis y Carlina, CARLOUIS</strong></p>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Preguntas frecuentes</h2>
          </div>
          <div class="faq" data-reveal>
%(faqs)s
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>¿Celebramos con un frasco?</h2>
            <p>Escribinos por WhatsApp, te ayudamos a escoger y te lo enviamos a tu cantón.</p>
            <div class="btn-row">
              <a class="btn btn--gold" href="%(wa)s?text=Hola%%2C%%20vi%%20que%%20CARLOUIS%%20cumple%%206%%20a%%C3%%B1os%%20y%%20quiero%%20hacer%%20un%%20pedido" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir por WhatsApp
              </a>
              <a class="btn btn--ghost" href="productos.html">Ver todos los productos</a>
            </div>
          </div>
        </div>
      </section>
    </article>

  </main>
%(footer)s</body>
</html>
''' % {
        "csp": CSP, "titulo": TITULO, "desc": DESC, "base": BASE, "slug": SLUG, "fecha": FECHA,
        "ld": ld(), "ig": INSTAGRAM, "sprite": SPRITE, "nav": nav, "wa": WA, "footer": FOOTER, "resena": RESENA,
        "cats": cats, "seis": seis, "faqs": faqs,
    }


if __name__ == "__main__":
    html = pagina()
    io.open(SLUG + ".html", "w", encoding="utf-8", newline="\n").write(html)
    palabras = len(re.sub(r"<[^>]+>", " ", html).split())
    print("  %s.html  %.1f KB  ~%d palabras" % (SLUG, len(html.encode()) / 1024, palabras))
