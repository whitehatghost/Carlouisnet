# -*- coding: utf-8 -*-
"""Genera una página por producto, con su propio JSON-LD y FAQ."""
import io, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

# El menú marca "Productos" como página actual
HEADER_P = HEADER.replace('<a href="productos.html">', '<a href="productos.html" aria-current="page">')
HEADER_P = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', HEADER_P)

POR_SLUG = {p["slug"]: p for p in PRODUCTOS}


def heat(p):
    if not p["nivel"]:
        return ""
    f = '<svg aria-hidden="true"><use href="#i-flame"/></svg>' * 5
    return (f'\n            <div class="heat" style="position:static;background:var(--paper-2);'
            f'border-color:var(--line);box-shadow:none;backdrop-filter:none">{f}'
            f'<span style="color:var(--ink-soft)">{p["nivel_txt"]}</span></div>')


def precios(p):
    filas = [f'<p class="price-tag">{p["unidad"]} <b>₡{p["precio"]}</b></p>']
    if p.get("precio2"):
        filas.append(f'<p class="price-tag">{p["unidad2"]} <b>₡{p["precio2"]}</b></p>')
    return "\n              ".join(filas)


def ofertas_ld(p):
    def of(precio, nombre):
        return ('{ "@type": "Offer", "name": "%s", "price": "%s", "priceCurrency": "CRC", '
                '"availability": "https://schema.org/InStock", "url": "%s%s.html", '
                '"seller": { "@id": "https://www.carlouis.net/#organization" }, '
                '"areaServed": { "@type": "Country", "name": "Costa Rica" } }'
                % (nombre, precio, BASE, p["slug"]))
    if p.get("precio2"):
        return "[\n          " + of(p["precio_num"], p["unidad"]) + ",\n          " + of(p["precio2_num"], p["unidad2"]) + "\n        ]"
    return of(p["precio_num"], p["unidad"])


def ld(p):
    faq = ",\n          ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in p["faq"])
    return f'''  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{BASE}" }},
          {{ "@type": "ListItem", "position": 2, "name": "Productos", "item": "{BASE}productos.html" }},
          {{ "@type": "ListItem", "position": 3, "name": {json.dumps(p["nombre"], ensure_ascii=False)}, "item": "{BASE}{p["slug"]}.html" }}
        ]
      }},
      {{
        "@type": "Product",
        "name": {json.dumps(p["nombre"] + " CARLOUIS", ensure_ascii=False)},
        "image": "{BASE}assets/img/{p["img"]}.jpg",
        "description": {json.dumps(p["desc"], ensure_ascii=False)},
        "brand": {{ "@type": "Brand", "name": "CARLOUIS" }},
        "manufacturer": {{ "@id": "https://www.carlouis.net/#organization" }},
        "countryOfOrigin": {{ "@type": "Country", "name": "Costa Rica" }},
        "category": "Salsas y conservas gourmet artesanales",
        "url": "{BASE}{p["slug"]}.html",
        "offers": {ofertas_ld(p)}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {faq}
        ]
      }}
    ]
  }}'''


def usos(p):
    return "\n".join(
        f'            <div class="uso">\n'
        f'              <h3>{t}</h3>\n'
        f'              <p>{d}</p>\n'
        f'            </div>' for t, d in p["usos"])


def faqs(p):
    return "\n".join(
        f'''            <details>
              <summary>{q}</summary>
              <div class="faq__answer"><p>{a}</p></div>
            </details>''' for q, a in p["faq"])


def relacionados(p):
    tarjetas = []
    for s in p["relacionados"]:
        r = POR_SLUG[s]
        tarjetas.append(f'''          <a class="post-card" href="{r["slug"]}.html">
            <div class="post-card__media" style="background:var(--paper-2);padding:0">
              <picture>
                <source srcset="assets/img/{r["img"]}.webp" type="image/webp" />
                <img src="assets/img/{r["img"]}.jpg" alt="{r["nombre"]} artesanal CARLOUIS"
                     width="{r["w"]}" height="{r["h"]}" loading="lazy"
                     style="width:100%;aspect-ratio:4/3;object-fit:cover" />
              </picture>
            </div>
            <div class="post-card__body">
              <h3>{r["nombre"]}</h3>
              <p>₡{r["precio"]} &middot; {r["unidad"]}</p>
              <span class="post-card__more">Ver producto <svg aria-hidden="true"><use href="#i-arrow"/></svg></span>
            </div>
          </a>''')
    return "\n".join(tarjetas)


def pagina(p):
    msg = p["nombre"].replace(" ", "%20").replace("ñ", "%C3%B1").replace("í", "%C3%AD")
    return f'''<!DOCTYPE html>
<html lang="es-CR" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';">
  <meta http-equiv="X-Content-Type-Options" content="nosniff" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <title>{p["title"]}</title>
  <meta name="description" content="{p["desc"]}" />
  <link rel="canonical" href="{BASE}{p["slug"]}.html" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="geo.region" content="CR-A" />
  <meta name="geo.placename" content="Alajuela, Costa Rica" />

  <meta property="og:type" content="product" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="{p["title"]}" />
  <meta property="og:description" content="{p["desc"]}" />
  <meta property="og:url" content="{BASE}{p["slug"]}.html" />
  <meta property="og:image" content="{BASE}assets/img/{p["img"]}.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{p["title"]}" />
  <meta name="twitter:description" content="{p["desc"]}" />
  <meta name="twitter:image" content="{BASE}assets/img/{p["img"]}.jpg" />

  <meta name="theme-color" content="#4A1206" />
  <link rel="icon" href="favicon.ico" sizes="any" />
  <link rel="icon" href="assets/img/icon-192.png" type="image/png" />
  <link rel="apple-touch-icon" href="assets/img/icon-180.png" />
  <link rel="manifest" href="site.webmanifest" />

  <link rel="preload" href="assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="assets/fonts/karla-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="assets/css/styles.css" />
  <script src="assets/js/main.js" defer></script>

  <script type="application/ld+json">
{ld(p)}
  </script>
</head>

<body>
  <a class="skip-link" href="#main">Saltar al contenido principal</a>

{SPRITE}
  <a class="wa-float" href="{WA}?text=Hola%2C%20quiero%20pedir%20{msg}" target="_blank" rel="noopener"
     aria-label="Pedí {p["nombre"]} por WhatsApp">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Pedí por WhatsApp</span>
  </a>
{HEADER_P}
  <main id="main">
    <article>

      <section class="section section--tight">
        <div class="container split" style="align-items:center">
          <div>
            <nav class="breadcrumb" aria-label="Ruta de navegación" style="margin-bottom:1rem;font-size:.9rem">
              <a href="index.html" style="color:var(--ember-700);text-decoration:none">Inicio</a>
              <span style="color:var(--ink-mute)"> / </span>
              <a href="productos.html" style="color:var(--ember-700);text-decoration:none">Productos</a>
              <span style="color:var(--ink-mute)"> / {p["nombre"]}</span>
            </nav>

            <h1>{p["h1"]}</h1>{heat(p)}

            <p style="font-size:var(--step-1);color:var(--ink-soft);margin-top:var(--sp-4)">{p["entrada"]}</p>

            <div class="price-row" style="margin-top:var(--sp-6)">
              {precios(p)}
            </div>

            <div class="btn-row">
              <a class="btn btn--primary" href="{WA}?text=Hola%2C%20quiero%20pedir%20{msg}%20de%20CARLOUIS" target="_blank" rel="noopener"
                 data-add data-name="{p["nombre"]}" data-price="{p["precio_num"]}">
                <svg aria-hidden="true"><use href="#i-plus"/></svg> Agregar al pedido
              </a>
              <a class="btn btn--ghost" href="productos.html">Ver todo el catálogo</a>
            </div>

            <p style="margin-top:var(--sp-5);font-size:.93rem;color:var(--ink-mute)">
              Hecho en Alajuela &middot; Sin aditivos artificiales &middot;
              <a href="cobertura.html" style="color:var(--ember-700)">Mismo precio en todo el país</a>
            </p>
          </div>

          <div>
            <picture>
              <source srcset="assets/img/{p["img"]}.webp" type="image/webp" />
              <img src="assets/img/{p["img"]}.jpg" alt="{p["nombre"]} artesanal CARLOUIS"
                   width="{p["w"]}" height="{p["h"]}" fetchpriority="high"
                   style="width:100%;border-radius:var(--r-xl);box-shadow:var(--sh-3);aspect-ratio:1/1;object-fit:cover" />
            </picture>
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head" data-reveal>
            <span class="eyebrow"><svg aria-hidden="true"><use href="#i-bag"/></svg> Cómo usarlo</span>
            <h2>Con qué se come {p["nombre"]}</h2>
            <p>{p["perfil"]}</p>
          </div>
          <div class="value-grid">
{usos(p)}
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Preguntas frecuentes</h2>
          </div>
          <div class="faq" data-reveal>
{faqs(p)}
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head" data-reveal>
            <h2>También te puede gustar</h2>
          </div>
          <div class="post-grid">
{relacionados(p)}
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>Pedí {p["nombre"]}</h2>
            <p>
              Escribinos por WhatsApp y coordinamos la entrega. Enviamos a las siete provincias
              al mismo precio, o retirás gratis los sábados en la feria de Alajuela.
            </p>
            <div class="btn-row">
              <a class="btn btn--gold" href="{WA}?text=Hola%2C%20quiero%20pedir%20{msg}%20de%20CARLOUIS" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir por WhatsApp
              </a>
              <a class="btn btn--ghost" href="encuentranos.html">Retirar en la feria</a>
            </div>
          </div>
        </div>
      </section>

    </article>
  </main>
{FOOTER}</body>
</html>
'''


# Estilo del bloque de usos
CSS_EXTRA = """
/* ---------- 30. Página de producto ---------------------------------------- */
.uso {
  padding: var(--sp-5); background: var(--card);
  border: 1px solid var(--line-soft); border-radius: var(--r-lg);
}
.uso h3 { font-size: 1.05rem; color: var(--ember-800); margin-bottom: 0.4rem; }
.uso p { margin: 0; color: var(--ink-soft); font-size: 0.95rem; }
"""

if __name__ == "__main__":
    for p in PRODUCTOS:
        io.open(f"{p['slug']}.html", "w", encoding="utf-8", newline="\n").write(pagina(p))
        print(f"  {p['slug']}.html")
    css = io.open("assets/css/styles.css", encoding="utf-8").read()
    if ".uso {" not in css:
        io.open("assets/css/styles.css", "a", encoding="utf-8", newline="\n").write(CSS_EXTRA)
        print("  estilos de producto agregados")
    print(f"\n  {len(PRODUCTOS)} paginas de producto generadas")
