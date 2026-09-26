# -*- coding: utf-8 -*-
"""Genera la página de venta al por mayor (B2B).

Apunta a un espacio vacío: en las búsquedas B2B del rubro en Costa Rica no
aparece ningún productor artesanal. Los resultados son distribuidores
genéricos y sitios de Colombia, Chile y España.

    python tools/generar-mayoreo.py
"""
import io, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
SLUG = "mayoreo"

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")

TITULO = "Salsas Artesanales al Por Mayor en Costa Rica | CARLOUIS"
DESC = ("Salsas, pestos y conservas artesanales al por mayor en Costa Rica para restaurantes, "
        "sodas, hoteles y tiendas gourmet. Hechos en Alajuela, entrega a todo el país.")

PARA_QUIEN = [
    ("i-bag", "Restaurantes y sodas",
     "Salsas de mesa y de cocina con sabor propio, que no se consiguen en el supermercado. "
     "Diferencian un plato sin subir el costo por porción."),
    ("i-box", "Tiendas gourmet y delicatessen",
     "Línea completa de doce productos en cuatro categorías, con historia de marca y "
     "producción local para contar al cliente."),
    ("i-truck", "Supermercados y cadenas",
     "Producto costarricense, artesanal y diferenciado, para las góndolas de gourmet "
     "y de producto nacional."),
    ("i-flame", "Carnicerías y parrilleras",
     "Chimichurri, salsas de habanero y conservas que acompañan la venta de carne y "
     "suben el ticket promedio."),
    ("i-leaf", "Hoteles y catering",
     "Presentaciones para desayunos, tablas de bocas y servicio de banquetes."),
    ("i-chat", "Marca propia",
     "Producimos bajo su marca si el volumen lo justifica. Se conversa caso por caso."),
]

PASOS = [
    ("Nos escribe", "Cuéntenos qué negocio tiene, qué productos le interesan y qué volumen "
                    "estima al mes. Con eso ya podemos hablar de números."),
    ("Prueba de producto", "Le hacemos llegar muestras. Ningún comprador serio decide sin "
                           "probar, y nosotros preferimos que pruebe."),
    ("Cotización y condiciones", "Precio por volumen, presentaciones disponibles, plazos de "
                                 "entrega y forma de pago, por escrito."),
    ("Entrega", "Coordinamos la primera entrega y la frecuencia de reposición según su rotación."),
]

FAQ = [
    ("¿Cuál es el volumen mínimo para comprar al por mayor?",
     "Depende del producto y de la frecuencia. Trabajamos desde pedidos pequeños de tienda "
     "de barrio hasta volúmenes de cadena. Escríbanos con su estimación mensual y le damos "
     "el mínimo y el precio correspondiente."),
    ("¿Manejan precios diferenciados por volumen?",
     "Sí. El precio baja por escalones según la cantidad y la frecuencia de reposición. "
     "La cotización se hace sobre su volumen real, no sobre una lista genérica."),
    ("¿Qué presentaciones tienen para food service?",
     "Además de la presentación de venta al público, podemos producir presentaciones más "
     "grandes para cocina. Consúltenos por el producto que le interesa."),
    ("¿Producen bajo marca propia?",
     "Sí, cuando el volumen lo justifica. Se define caso por caso: receta, presentación, "
     "etiqueta y exclusividad son parte de la conversación."),
    ("¿A qué zonas del país entregan?",
     "A las siete provincias. En el Gran Área Metropolitana coordinamos entrega directa; "
     "al resto del país, por servicio de encomienda."),
    ("¿Qué documentación manejan?",
     "Estamos al día con los requisitos para operar y facturar. Si su empresa necesita "
     "documentación específica —registro sanitario, ficha técnica, código de barras o "
     "certificaciones— escríbanos y le confirmamos el estado exacto de cada producto antes "
     "de avanzar."),
    ("¿Cuánto tardan en entregar un pedido de mayoreo?",
     "Depende del volumen, porque producimos en lotes pequeños y no mantenemos inventario "
     "grande. Por eso conviene coordinar con anticipación y establecer una frecuencia fija "
     "de reposición."),
    ("¿Se puede empezar con una prueba pequeña?",
     "Es lo que recomendamos. Un primer pedido corto permite medir rotación real en su punto "
     "de venta antes de comprometer volumen."),
]

LD = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Mayoreo", "item": BASE + SLUG + ".html"}]},
        {"@type": "Service",
         "name": "Venta al por mayor de salsas y conservas artesanales",
         "serviceType": "Distribución mayorista de alimentos gourmet artesanales",
         "description": ("Suministro al por mayor de salsas de habanero, pestos, alioli, "
                         "mayonesas saborizadas y conservas artesanales para restaurantes, "
                         "sodas, hoteles, tiendas gourmet y supermercados en Costa Rica."),
         "url": BASE + SLUG + ".html",
         "provider": {"@id": BASE + "#organization"},
         "areaServed": [{"@type": "Country", "name": "Costa Rica"}],
         "audience": {"@type": "BusinessAudience",
                      "audienceType": "Restaurantes, sodas, hoteles, tiendas gourmet, supermercados y carnicerías"},
         "availableChannel": {"@type": "ServiceChannel",
                              "serviceUrl": BASE + SLUG + ".html",
                              "servicePhone": "+506-8825-2608"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}, ensure_ascii=False, indent=2)


def pagina():
    nav = HEADER.replace('<a href="mayoreo.html">', '<a href="mayoreo.html" aria-current="page">')
    # el item se agrega al menu despues de generar, por eso tambien se contempla aqui
    nav = re.sub(r'<a href="index\.html" aria-current="page">', '<a href="index.html">', nav)

    quien = "\n".join(
        f'''          <div class="value" data-reveal>
            <div class="icon-badge"><svg aria-hidden="true"><use href="#{ic}"/></svg></div>
            <h3>{t}</h3>
            <p>{d}</p>
          </div>''' for ic, t, d in PARA_QUIEN)

    pasos = "\n".join(
        f'''          <li class="step">
            <b>{t}</b>
            <p>{d}</p>
          </li>''' for t, d in PASOS)

    faqs = "\n".join(
        f'''            <details>
              <summary>{q}</summary>
              <div class="faq__answer"><p>{a}</p></div>
            </details>''' for q, a in FAQ)

    catalogo = "\n".join(
        f'            <li>{p["nombre"]}</li>' for p in PRODUCTOS)

    return f'''<!DOCTYPE html>
<html lang="es-CR" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta http-equiv="X-Content-Type-Options" content="nosniff" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <title>{TITULO}</title>
  <meta name="description" content="{DESC}" />
  <link rel="canonical" href="{BASE}{SLUG}.html" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="geo.region" content="CR-A" />
  <meta name="geo.placename" content="Alajuela, Costa Rica" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="CARLOUIS Gourmet" />
  <meta property="og:locale" content="es_CR" />
  <meta property="og:title" content="{TITULO}" />
  <meta property="og:description" content="{DESC}" />
  <meta property="og:url" content="{BASE}{SLUG}.html" />
  <meta property="og:image" content="{BASE}assets/img/og-carlouis.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{TITULO}" />
  <meta name="twitter:description" content="{DESC}" />
  <meta name="twitter:image" content="{BASE}assets/img/og-carlouis.jpg" />

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
{LD}
  </script>
</head>

<body>
  <a class="skip-link" href="#main">Saltar al contenido principal</a>

{SPRITE}
  <a class="wa-float" href="{WA}?text=Hola%2C%20represento%20un%20negocio%20y%20quiero%20consultar%20precios%20de%20mayoreo"
     target="_blank" rel="noopener" aria-label="Consultar mayoreo por WhatsApp">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Consultar mayoreo</span>
  </a>
{nav}
  <main id="main">

    <section class="section section--tight on-dark">
      <div class="container container--narrow" style="text-align:center">
        <nav class="breadcrumb" aria-label="Ruta de navegación" style="margin-bottom:1rem;font-size:.9rem">
          <a href="index.html" style="color:var(--gold-400);text-decoration:none">Inicio</a>
          <span style="color:#C4AE95"> / Mayoreo</span>
        </nav>
        <span class="eyebrow"><svg aria-hidden="true"><use href="#i-box"/></svg> Para negocios</span>
        <h1>Salsas artesanales al por mayor</h1>
        <p style="font-size:var(--step-1);max-width:62ch;margin-inline:auto">
          Somos productores, no revendedores. Elaboramos en Alajuela y le vendemos directo a
          restaurantes, sodas, hoteles, tiendas gourmet, carnicerías y supermercados de todo
          Costa Rica.
        </p>
        <div class="btn-row" style="justify-content:center;margin-top:var(--sp-6)">
          <a class="btn btn--gold" href="{WA}?text=Hola%2C%20represento%20un%20negocio%20y%20quiero%20consultar%20precios%20de%20mayoreo.%20Mi%20negocio%20es%3A%20" target="_blank" rel="noopener">
            <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir cotización
          </a>
          <a class="btn btn--ghost" href="productos.html">Ver la línea completa</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head section-head--center" data-reveal>
          <h2>A quién le vendemos</h2>
          <p>Si su negocio sirve comida o vende producto gourmet, hay una línea que le calza.</p>
        </div>
        <div class="value-grid">
{quien}
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container split">
        <div data-reveal>
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-leaf"/></svg> Por qué nosotros</span>
          <h2>Producto que no está en todos lados</h2>
          <p>
            La ventaja de trabajar con un productor artesanal es exactamente esa: el cliente no
            encuentra lo mismo en el supermercado de la esquina. Es sabor propio y es una historia
            que se puede contar.
          </p>
          <p>
            Elaboramos en lotes pequeños, con ingredientes seleccionados y sin aditivos
            artificiales. Eso condiciona los tiempos —no mantenemos inventario grande— pero es
            justamente lo que hace que el producto valga.
          </p>
          <p>
            Trabajamos con una línea de <strong>doce productos en cuatro categorías</strong>:
            picantes, pestos y salsas, cremas y mayonesas, y conservas. Se puede empezar con
            dos o tres y crecer según rote.
          </p>
          <div class="btn-row">
            <a class="btn btn--primary" href="{WA}?text=Hola%2C%20quiero%20la%20lista%20de%20precios%20de%20mayoreo" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-wa"/></svg> Pedir lista de precios
            </a>
          </div>
        </div>
        <div class="panel" data-reveal>
          <h3 style="color:var(--ember-800);margin-bottom:var(--sp-4)">La línea completa</h3>
          <ul style="display:grid;gap:.45rem;list-style:none;font-size:.96rem;color:var(--ink-soft)">
{catalogo}
          </ul>
          <p style="margin-top:var(--sp-5);font-size:.9rem;color:var(--ink-mute)">
            Consulte por presentaciones de mayor tamaño para cocina y por producción bajo marca propia.
          </p>
          <p style="margin-top:var(--sp-3);font-size:.9rem;color:var(--ink-mute)">
            ¿Compra para un supermercado o una cadena?
            <a href="proveedor-salsas-artesanales-costa-rica.html">Lea la ficha para compradores de góndola</a>.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head section-head--center" data-reveal>
          <h2>Cómo empezamos</h2>
          <p>Sin vueltas y sin compromiso de volumen en la primera conversación.</p>
        </div>
        <div class="cta on-dark" data-reveal style="text-align:left">
          <ol class="steps">
{pasos}
          </ol>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container container--narrow">
        <div class="section-head section-head--center" data-reveal>
          <h2>Preguntas de compradores</h2>
        </div>
        <div class="faq" data-reveal>
{faqs}
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="cta on-dark" data-reveal>
          <h2>Hablemos de números</h2>
          <p>
            Escríbanos qué negocio tiene y qué volumen estima al mes. Le mandamos muestras y
            una cotización concreta, no una lista genérica.
          </p>
          <div class="btn-row">
            <a class="btn btn--gold" href="{WA}?text=Hola%2C%20represento%20un%20negocio%20y%20quiero%20consultar%20mayoreo.%20Somos%3A%20" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-wa"/></svg> Escribir por WhatsApp
            </a>
            <a class="btn btn--ghost" href="contacto.html">Escribir por el formulario</a>
          </div>
          <p style="margin-top:var(--sp-5);font-size:.92rem">
            También puede llamar al <a href="tel:+50688252608" style="color:var(--gold-400)">+506 8825 2608</a>
            o escribir a <a href="mailto:luiro90@gmail.com" style="color:var(--gold-400)">luiro90@gmail.com</a>.
          </p>
        </div>
      </div>
    </section>

  </main>
{FOOTER}</body>
</html>
'''


if __name__ == "__main__":
    io.open(f"{SLUG}.html", "w", encoding="utf-8", newline="\n").write(pagina())
    print(f"  {SLUG}.html generado")
