# -*- coding: utf-8 -*-
"""Genera la página para compradores de cadenas y supermercados.

    python tools/generar-proveedor.py

Es distinta de mayoreo.html a propósito. Mayoreo le habla a una soda, a un
restaurante o a una tienda: alguien que compra cajas. Esta le habla a un
comprador de cadena, que no evalúa sabor sino si el proveedor puede cumplir:
documentación, presentaciones, capacidad y reposición.

IMPORTANTE sobre la sección de documentación: acá NO se afirma tener registro
sanitario ni código de barras, porque eso no está confirmado. Se explica qué
pide una cadena y se invita a pedir el estado exacto por producto. Si algún día
se confirma, se actualiza DOCUMENTACION y se vuelve a correr este script.
"""
import io, os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS

BASE = "https://www.carlouis.net/"
WA = "https://wa.me/50688252608"
SLUG = "proveedor-salsas-artesanales-costa-rica"

INDEX = io.open("index.html", encoding="utf-8").read()
SPRITE = re.search(r'(  <!-- Sprite de iconos.*?</svg>\n)', INDEX, re.S).group(1)
HEADER = re.search(r'(\n  <header class="site-header">.*?</header>\n)', INDEX, re.S).group(1)
FOOTER = re.search(r'(\n  <footer class="site-footer">.*?</footer>\n)', INDEX, re.S).group(1)

CSP = ("default-src 'self'; img-src 'self' data: https://*.google-analytics.com "
       "https://*.googletagmanager.com; script-src 'self' https://www.googletagmanager.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none';")

TITULO = "Proveedor de Salsas Artesanales para Supermercados | Costa Rica | CARLOUIS"
DESC = ("Productor costarricense de salsas artesanales, pestos y conservas gourmet que busca "
        "espacio en góndola de supermercados y cadenas. Doce productos de marca propia, "
        "producción en Alajuela. Contacto directo con el productor.")

PORQUE = [
    ("i-flame", "Producto nacional con marca propia",
     "No somos importador ni redistribuidor. Cocinamos los doce productos en Alajuela, bajo "
     "nuestra propia marca. Para una góndola de producto costarricense eso es la diferencia "
     "entre surtir un espacio y contar una historia que el cliente puede verificar."),
    ("i-box", "Categorías donde el estante nacional está vacío",
     "En salsas picantes hay oferta nacional. En alioli, en pesto de albahaca y en tomate "
     "deshidratado en aceite, casi todo lo que hay en góndola es importado de España, Italia o "
     "Chile. Ahí es donde una marca tica compite por precio de logística, no solo por sabor."),
    ("i-leaf", "Formulación limpia",
     "Sin colorantes ni preservantes artificiales en ninguna de las doce recetas. Varios "
     "productos son aptos para dieta vegetariana. Es la ficha que pide el comprador de la "
     "categoría saludable, sin tener que reformular nada."),
    ("i-truck", "Cercanía logística",
     "Producimos a 20 minutos del Aeropuerto Juan Santamaría y dentro del GAM. Para reposición "
     "frecuente en tiendas del Área Metropolitana eso reduce el tiempo entre pedido y góndola."),
    ("i-star", "Producto ya probado en el mercado",
     "No es un lanzamiento de escritorio. Se vende todas las semanas en feria y en ferias de "
     "temporada, con degustación abierta, que es donde se ve de verdad qué rota y qué no."),
    ("i-chat", "Se habla directo con quien produce",
     "No hay intermediario ni fuerza de ventas tercerizada. La conversación de condiciones, "
     "volumen y marca propia es con quien decide."),
]

PASOS = [
    ("Nos escribe con el perfil de compra",
     "Cadena o formato, cuántos puntos de venta, qué categoría le interesa y qué rotación "
     "estima. Con eso sabemos si podemos cumplir antes de hacerle perder tiempo."),
    ("Enviamos muestras y ficha",
     "Muestras físicas de la categoría que le interesa, más la ficha de cada producto: "
     "ingredientes, presentación, peso y vida útil."),
    ("Revisamos requisitos de su cadena",
     "Cada cadena tiene su lista: documentación, codificación, presentación, empaque de "
     "transporte y condiciones comerciales. Nos la pasan y le decimos con claridad qué "
     "cumplimos hoy y qué necesitaríamos resolver, con plazos reales."),
    ("Propuesta y prueba en piso",
     "Precio por volumen, presentaciones y frecuencia de reposición por escrito. Lo sano es "
     "empezar con una prueba en pocas tiendas y medir rotación real antes de escalar."),
]

# Lo que una cadena pide. NO se afirma cumplimiento: se dice que se confirma
# por escrito y por producto. Cambiar solo cuando esté verificado de verdad.
DOCUMENTACION = [
    ("Registro sanitario del Ministerio de Salud",
     "Obligatorio para producto alimenticio en góndola, y se otorga por producto, no por "
     "empresa. Escríbanos y le confirmamos por escrito el estado exacto de cada uno de los "
     "doce antes de que usted invierta tiempo en el proceso."),
    ("Código de barras GS1",
     "Necesario para codificar en el sistema de la cadena. Le confirmamos la situación de "
     "codificación de cada presentación al momento de la consulta."),
    ("Ficha técnica por producto",
     "Ingredientes, alérgenos, peso neto, vida útil y condiciones de almacenamiento. La "
     "preparamos para los productos que le interesen."),
    ("Cédula jurídica y CCSS al día",
     "Requisito para facturar y para orden de compra. Se aporta la documentación al iniciar el "
     "proceso."),
    ("Capacidad de producción y reposición",
     "Producimos en lotes pequeños, que es lo que sostiene la calidad y también nuestro "
     "límite real. Preferimos decirlo de frente: para un piloto en pocas tiendas respondemos "
     "bien; para cobertura nacional inmediata habría que planificar el escalamiento juntos y "
     "con fechas."),
    ("Empaque de transporte",
     "Frasco de vidrio con empaque de protección individual. Para volumen de cadena definimos "
     "unidades por caja y estiba según lo que su operación requiera."),
]

FAQ = [
    ("¿Ya son proveedores de alguna cadena de supermercados?",
     "Hoy vendemos directo al consumidor, en feria y por pedido, y al por mayor a negocios de "
     "alimentación. Entrar a cadena es el paso que estamos buscando dar, y por eso esta página "
     "existe. Lo decimos claro en vez de inflar la trayectoria."),
    ("¿Tienen registro sanitario y código de barras?",
     "El registro sanitario se otorga por producto, no por empresa. Escríbanos indicando qué "
     "productos le interesan y le confirmamos por escrito el estado exacto de cada uno, sin "
     "rodeos, antes de avanzar."),
    ("¿Qué volumen pueden sostener?",
     "Depende de la categoría y del plazo. Producimos en lotes pequeños, así que para un piloto "
     "en pocas tiendas respondemos sin problema, y para volúmenes mayores planificamos el "
     "escalamiento con fechas concretas. Preferimos comprometer lo que podemos cumplir."),
    ("¿Producen bajo marca privada de la cadena?",
     "Sí, cuando el volumen lo justifica. Receta, presentación, etiqueta y exclusividad se "
     "definen caso por caso."),
    ("¿Manejan presentaciones distintas a la de venta al público?",
     "Sí. Además del frasco de consumo podemos producir presentaciones de mayor tamaño para "
     "food service. Se define según lo que la cadena necesite."),
    ("¿Qué vida útil tienen los productos?",
     "Varía por categoría: las conservas en aceite tienen mayor vida útil que las emulsiones. "
     "Al no llevar preservantes artificiales, las condiciones de conservación son parte de la "
     "ficha. Se la entregamos por producto."),
    ("¿A qué zonas del país pueden distribuir?",
     "A las siete provincias. En el Gran Área Metropolitana coordinamos entrega directa y al "
     "resto del país por encomienda. Para cadena se define la logística según sus centros de "
     "distribución."),
    ("¿Con quién se habla?",
     "Directo con el productor, al 8825 2608 o por correo. No hay intermediarios ni fuerza de "
     "ventas tercerizada."),
]

CATEGORIAS = [
    ("Salsas picantes de habanero", ["salsa-habanero-fire", "salsa-pina-habanero"]),
    ("Pestos", ["pesto-de-albahaca", "pesto-de-tomate"]),
    ("Cremas y emulsiones", ["alioli", "mayonesa-de-chipotle", "mayonesa-de-culantro"]),
    ("Conservas vegetales", ["tomates-deshidratados", "chile-morron-asado",
                             "salsa-de-chile-dulce"]),
    ("Especialidades", ["chimichurri-argentino", "salsa-de-mora"]),
]

POR_SLUG = {p["slug"]: p for p in PRODUCTOS}


def ld():
    faq = ",\n          ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in FAQ)
    url = BASE + SLUG + ".html"
    return '''  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "%(base)s" },
          { "@type": "ListItem", "position": 2, "name": "Mayoreo", "item": "%(base)smayoreo.html" },
          { "@type": "ListItem", "position": 3, "name": "Proveedor para supermercados", "item": "%(url)s" }
        ]
      },
      {
        "@type": "Service",
        "name": "Suministro de salsas artesanales y conservas gourmet para supermercados y cadenas",
        "serviceType": "Proveedor de alimentos gourmet artesanales para retail",
        "description": %(desc)s,
        "url": "%(url)s",
        "provider": { "@id": "%(base)s#organization" },
        "areaServed": [{ "@type": "Country", "name": "Costa Rica" }],
        "audience": {
          "@type": "BusinessAudience",
          "audienceType": "Supermercados, cadenas de retail, tiendas de conveniencia, distribuidores y compradores de categoría"
        },
        "availableChannel": {
          "@type": "ServiceChannel",
          "serviceUrl": "%(url)s",
          "servicePhone": "+506-8825-2608"
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
    nav = nav.replace('<a href="mayoreo.html">', '<a href="mayoreo.html" aria-current="page">')

    porque = "\n".join(
        '''          <div class="value" data-reveal>
            <div class="icon-badge"><svg aria-hidden="true"><use href="#%s"/></svg></div>
            <h3>%s</h3>
            <p>%s</p>
          </div>''' % (ic, t, d) for ic, t, d in PORQUE)

    pasos = "\n".join(
        '''          <li class="step">
            <b>%s</b>
            <p>%s</p>
          </li>''' % (t, d) for t, d in PASOS)

    docs = "\n".join(
        '''            <details>
              <summary>%s</summary>
              <div class="faq__answer"><p>%s</p></div>
            </details>''' % (t, d) for t, d in DOCUMENTACION)

    faqs = "\n".join(
        '''            <details>
              <summary>%s</summary>
              <div class="faq__answer"><p>%s</p></div>
            </details>''' % (q, a) for q, a in FAQ)

    cats = "\n".join(
        '''          <div class="value" data-reveal>
            <h3>%s</h3>
            <ul class="chips">
%s
            </ul>
          </div>''' % (nombre, "\n".join(
            '              <li><a href="%s.html" style="color:inherit;text-decoration:none">%s</a></li>'
            % (s, POR_SLUG[s]["nombre"]) for s in slugs))
        for nombre, slugs in CATEGORIAS)

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
  <a class="wa-float" href="%(wa)s?text=Hola%%2C%%20escribo%%20de%%20una%%20cadena%%2Fsupermercado%%20y%%20quiero%%20hablar%%20de%%20proveedur%%C3%%ADa"
     target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp al 8825 2608">
    <svg aria-hidden="true"><use href="#i-wa"/></svg>
    <span>Hablemos</span>
  </a>
%(nav)s
  <main id="main">

    <article>
      <section class="section section--tight on-dark">
        <div class="container container--narrow" style="text-align:center">
          <nav class="breadcrumb" aria-label="Ruta de navegación" style="margin-bottom:1rem;font-size:.9rem">
            <a href="index.html" style="color:var(--gold-400);text-decoration:none">Inicio</a>
            <span style="color:#C4AE95"> / </span>
            <a href="mayoreo.html" style="color:var(--gold-400);text-decoration:none">Mayoreo</a>
            <span style="color:#C4AE95"> / Proveedor para cadenas</span>
          </nav>
          <span class="eyebrow"><svg aria-hidden="true"><use href="#i-truck"/></svg> Para compradores de categoría</span>
          <h1>Proveedor costarricense de salsas artesanales para góndola</h1>
          <p style="font-size:var(--step-1);max-width:64ch;margin-inline:auto">
            Doce productos de marca propia, producidos en Alajuela: salsas de habanero, pestos,
            alioli, mayonesas saborizadas y conservas vegetales. Si usted evalúa producto
            nacional para su cadena, acá está lo que necesita saber para decidir si vale la
            reunión.
          </p>
          <div class="btn-row" style="justify-content:center;margin-top:var(--sp-5)">
            <a class="btn btn--gold" href="%(wa)s?text=Hola%%2C%%20escribo%%20de%%20una%%20cadena%%2Fsupermercado%%20y%%20quiero%%20hablar%%20de%%20proveedur%%C3%%ADa" target="_blank" rel="noopener">
              <svg aria-hidden="true"><use href="#i-wa"/></svg> Hablar con el productor
            </a>
            <a class="btn btn--ghost" href="contacto.html">Escribir por correo</a>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <h2>Por qué mirarnos</h2>
            <p>Seis razones concretas, sin adjetivos de más.</p>
          </div>
          <div class="value-grid">
%(porque)s
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container">
          <div class="section-head section-head--center" data-reveal>
            <h2>La línea completa</h2>
            <p>Doce productos en cinco categorías. Tocá cualquiera para ver su ficha.</p>
          </div>
          <div class="value-grid">
%(cats)s
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <span class="eyebrow"><svg aria-hidden="true"><use href="#i-check"/></svg> Sin rodeos</span>
            <h2>Requisitos de cadena: dónde estamos</h2>
            <p>
              Sabemos qué pide una cadena para codificar un proveedor nuevo. Acá está la lista y
              qué implica cada punto. Lo que no vamos a hacer es afirmar en una página web que
              cumplimos algo que usted va a verificar en la primera reunión: pídanos el estado
              exacto por producto y se lo damos por escrito.
            </p>
          </div>
          <div class="faq" data-reveal>
%(docs)s
          </div>
        </div>
      </section>

      <section class="section section--alt">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Cómo avanzamos</h2>
            <p>Cuatro pasos, sin vueltas.</p>
          </div>
          <ol class="steps">
%(pasos)s
          </ol>
        </div>
      </section>

      <section class="section">
        <div class="container container--narrow">
          <div class="section-head" data-reveal>
            <h2>Preguntas de comprador</h2>
          </div>
          <div class="faq" data-reveal>
%(faqs)s
          </div>
        </div>
      </section>

      <section class="section section--tight">
        <div class="container">
          <div class="cta on-dark" data-reveal>
            <h2>Hablemos de góndola</h2>
            <p>
              Escríbanos con su cadena, el formato y la categoría que evalúa. Respondemos con
              muestras, fichas y el estado real de documentación de los productos que le
              interesen.
            </p>
            <div class="btn-row">
              <a class="btn btn--gold" href="%(wa)s?text=Hola%%2C%%20escribo%%20de%%20una%%20cadena%%2Fsupermercado%%20y%%20quiero%%20hablar%%20de%%20proveedur%%C3%%ADa" target="_blank" rel="noopener">
                <svg aria-hidden="true"><use href="#i-wa"/></svg> WhatsApp 8825 2608
              </a>
              <a class="btn btn--ghost" href="mayoreo.html">Mayoreo para negocios</a>
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
        "porque": porque, "cats": cats, "docs": docs, "pasos": pasos, "faqs": faqs,
    }


if __name__ == "__main__":
    html = pagina()
    io.open(SLUG + ".html", "w", encoding="utf-8", newline="\n").write(html)
    palabras = len(re.sub(r"<[^>]+>", " ", html).split())
    print("  %s.html  %.1f KB  ~%d palabras" % (SLUG, len(html.encode()) / 1024, palabras))
