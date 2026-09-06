# -*- coding: utf-8 -*-
"""Genera las guías y su índice. Ejecutar desde la raíz del proyecto:

    python tools/generar-guias.py
"""
import io, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guias import GUIAS
from productos import PRODUCTOS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
POR_SLUG = {p["slug"]: p for p in PRODUCTOS}

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")


def cabeza(titulo, desc, ruta, img, activo="guias.html", ld=""):
    ldb = f'\n  <script type="application/ld+json">\n{ld}\n  </script>\n' if ld else ""
    nav = HEADER.replace(f'<a href="{activo}">', f'<a href="{activo}" aria-current="page">')
    nav = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', nav)
    return f'''<!DOCTYPE html>
<html lang="es-CR" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta http-equiv="X-Content-Type-Options" content="nosniff" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <title>{titulo}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{BASE}{ruta}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="geo.region" content="CR-A" />
  <meta name="geo.placename" content="Alajuela, Costa Rica" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="{titulo}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{BASE}{ruta}" />
  <meta property="og:image" content="{BASE}assets/img/{img}.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{titulo}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{BASE}assets/img/{img}.jpg" />

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
{ldb}</head>

<body>
  <a class="skip-link" href="#main">Saltar al contenido principal</a>

{SPRITE}
  <a class="wa-float" href="{WA}?text=Hola%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20productos%20CARLOUIS"
     target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp al 8825 2608">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Pedí por WhatsApp</span>
  </a>
{nav}
  <main id="main">
'''


def ld_guia(g):
    faq = ",\n          ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in g["faq"])
    return f'''  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{BASE}" }},
          {{ "@type": "ListItem", "position": 2, "name": "Guías", "item": "{BASE}guias.html" }},
          {{ "@type": "ListItem", "position": 3, "name": {json.dumps(g["h1"], ensure_ascii=False)}, "item": "{BASE}{g["slug"]}.html" }}
        ]
      }},
      {{
        "@type": "Article",
        "headline": {json.dumps(g["titulo"], ensure_ascii=False)},
        "description": {json.dumps(g["desc"], ensure_ascii=False)},
        "image": "{BASE}assets/img/{g["img"]}.jpg",
        "datePublished": "{g["fecha"]}",
        "dateModified": "{g["fecha"]}",
        "inLanguage": "es-CR",
        "mainEntityOfPage": "{BASE}{g["slug"]}.html",
        "author": {{ "@type": "Organization", "name": "CARLOUIS Gourmet", "url": "{BASE}" }},
        "publisher": {{
          "@type": "Organization", "name": "CARLOUIS Gourmet",
          "logo": {{ "@type": "ImageObject", "url": "{BASE}assets/img/logo.png" }}
        }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {faq}
        ]
      }}
    ]
  }}'''


def guia(g):
    secciones = ""
    for titulo, items in g["secciones"]:
        cuerpo = "\n".join(
            f'            <div class="uso">\n'
            f'              <h3>{t}</h3>\n'
            f'              <p>{d}</p>\n'
            f'            </div>' for t, d in items)
        secciones += f'''
          <h2>{titulo}</h2>
          <div class="value-grid" style="margin-bottom:var(--sp-7)">
{cuerpo}
          </div>
'''

    faqs = "\n".join(
        f'''            <details>
              <summary>{q}</summary>
              <div class="faq__answer"><p>{a}</p></div>
            </details>''' for q, a in g["faq"])

    prods = "\n".join(
        f'''          <a class="post-card" href="{POR_SLUG[s]["slug"]}.html">
            <div class="post-card__media" style="background:var(--paper-2);padding:0">
              <picture>
                <source srcset="assets/img/{POR_SLUG[s]["img"]}.webp" type="image/webp" />
                <img src="assets/img/{POR_SLUG[s]["img"]}.jpg" alt="{POR_SLUG[s]["nombre"]} artesanal CARLOUIS"
                     width="{POR_SLUG[s]["w"]}" height="{POR_SLUG[s]["h"]}" loading="lazy"
                     style="width:100%;aspect-ratio:4/3;object-fit:cover" />
              </picture>
            </div>
            <div class="post-card__body">
              <h3>{POR_SLUG[s]["nombre"]}</h3>
              <p>₡{POR_SLUG[s]["precio"]} &middot; {POR_SLUG[s]["unidad"]}</p>
              <span class="post-card__more">Ver producto <svg aria-hidden="true"><use href="#i-arrow"/></svg></span>
            </div>
          </a>''' for s in g["productos"])

    intro = "\n".join(f'          <p>{p}</p>' for p in g["intro"])

    return (cabeza(g["titulo"], g["desc"], g["slug"] + ".html", g["img"], ld=ld_guia(g)) + f'''
    <article>
      <section class="section section--tight on-dark">
        <div class="container container--narrow" style="text-align:center">
          <nav class="breadcrumb" aria-label="Ruta de navegación" style="margin-bottom:1rem;font-size:.9rem">
            <a href="index.html" style="color:var(--gold-400);text-decoration:none">Inicio</a>
            <span style="color:#C4AE95"> / </span>
            <a href="guias.html" style="color:var(--gold-400);text-decoration:none">Guías</a>
          </nav>
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-calendar"/></svg> {g["fecha_txt"]}</span>
          <h1>{g["h1"]}</h1>
          <p style="font-size:var(--step-1);max-width:60ch;margin-inline:auto">{g["lede"]}</p>
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow article-body">
{intro}
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
{secciones}
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Preguntas frecuentes</h2>
          </div>
          <div class="faq" data-reveal>
{faqs}
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head" data-reveal>
            <h2>Productos de esta guía</h2>
          </div>
          <div class="post-grid">
{prods}
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>{g["cta"]}</h2>
            <p>
              Todo se hace en Alajuela, en lotes pequeños y sin aditivos artificiales.
              Enviamos a las siete provincias al mismo precio.
            </p>
            <div class="btn-row">
              <a class="btn btn--gold" href="productos.html">
                <svg aria-hidden="true"><use href="#i-bag"/></svg> Ver el catálogo
              </a>
              <a class="btn btn--ghost" href="{WA}?text=Hola%2C%20quiero%20hacer%20un%20pedido%20CARLOUIS" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir por WhatsApp
              </a>
            </div>
          </div>
        </div>
      </section>
    </article>
  </main>
{FOOTER}</body>
</html>
''')


def indice():
    ld = '''  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Guías de CARLOUIS Gourmet",
    "description": "Guías prácticas sobre cómo usar y conservar salsas, pestos y conservas artesanales.",
    "url": "%sguias.html",
    "inLanguage": "es-CR"
  }''' % BASE

    tarjetas = "\n".join(
        f'''          <a class="post-card" href="{g["slug"]}.html" data-reveal>
            <div class="post-card__media" style="background:var(--paper-2);padding:0">
              <picture>
                <source srcset="assets/img/{g["img"]}.webp" type="image/webp" />
                <img src="assets/img/{g["img"]}.jpg" alt="{g["h1"]}"
                     width="{g["w"]}" height="{g["h"]}" loading="lazy"
                     style="width:100%;aspect-ratio:16/9;object-fit:cover" />
              </picture>
            </div>
            <div class="post-card__body">
              <span class="post-card__date">
                <svg aria-hidden="true"><use href="#i-calendar"/></svg>
                <time datetime="{g["fecha"]}">{g["fecha_txt"]}</time>
              </span>
              <h3>{g["h1"]}</h3>
              <p>{g["lede"]}</p>
              <span class="post-card__more">Leer la guía <svg aria-hidden="true"><use href="#i-arrow"/></svg></span>
            </div>
          </a>''' for g in GUIAS)

    return (cabeza("Guías: cómo usar y conservar salsas artesanales | CARLOUIS",
                   "Guías prácticas de CARLOUIS: con qué se come el chimichurri, cómo elegir "
                   "salsa picante según tu tolerancia y cómo conservar productos sin preservantes.",
                   "guias.html", "chimichurri", ld=ld) + f'''
    <section class="section section--tight on-dark">
      <div class="container container--narrow" style="text-align:center">
        <span class="eyebrow"><svg aria-hidden="true"><use href="#i-leaf"/></svg> Para sacarles provecho</span>
        <h1>Guías</h1>
        <p style="font-size:var(--step-1);max-width:60ch;margin-inline:auto">
          Comprar el frasco es la parte fácil. Acá está lo que hacemos nosotros con cada producto,
          y lo que nos preguntan en la feria todos los sábados.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="post-grid">
{tarjetas}
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="cta on-dark" data-reveal>
          <h2>¿Tenés una duda que no está acá?</h2>
          <p>Escribinos por WhatsApp. Lo que más nos preguntan termina convertido en guía.</p>
          <div class="btn-row">
            <a class="btn btn--gold" href="{WA}?text=Hola%2C%20tengo%20una%20consulta%20sobre%20los%20productos" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-wa"/></svg> Preguntar por WhatsApp
            </a>
            <a class="btn btn--ghost" href="productos.html">Ver el catálogo</a>
          </div>
        </div>
      </div>
    </section>
  </main>
{FOOTER}</body>
</html>
''')


if __name__ == "__main__":
    for g in GUIAS:
        io.open(f"{g['slug']}.html", "w", encoding="utf-8", newline="\n").write(guia(g))
        print(f"  {g['slug']}.html")
    io.open("guias.html", "w", encoding="utf-8", newline="\n").write(indice())
    print("  guias.html")
    print(f"\n  {len(GUIAS)} guias + indice generados")
