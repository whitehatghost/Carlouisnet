# -*- coding: utf-8 -*-
"""Auditoría SEO técnica de todas las páginas públicas.

    python tools/auditar-seo.py

Revisa lo que Google mira y que se puede comprobar sin adivinar: títulos,
descripciones, un solo H1, canonical, enlaces internos rotos, imágenes sin
texto alternativo, datos estructurados válidos, páginas huérfanas (que nadie
enlaza) y contenido flaco.

No mide posiciones en Google: eso sale de Search Console, no del código.
"""
import io, os, re, json, glob, collections

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Páginas que existen pero no son para buscadores.
FUERA = {"404.html", "gracias.html", "aniversario.html"}

paginas = sorted(f for f in glob.glob("*.html") if f not in FUERA)
datos = {}
entrantes = collections.Counter()
problemas = collections.defaultdict(list)

for f in paginas:
    h = io.open(f, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    can = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    main = re.search(r"<main[^>]*>(.*?)</main>", h, re.S)
    cuerpo = re.sub(r"<[^>]+>", " ", main.group(1) if main else h)
    palabras = len(cuerpo.split())

    titulo = re.sub(r"\s+", " ", t.group(1)).strip() if t else ""
    desc = d.group(1) if d else ""
    datos[f] = {"titulo": titulo, "desc": desc, "palabras": palabras}

    if not titulo:
        problemas[f].append("sin <title>")
    elif len(titulo) > 65:
        problemas[f].append("title largo (%d car.): Google lo corta" % len(titulo))
    elif len(titulo) < 25:
        problemas[f].append("title corto (%d car.)" % len(titulo))

    if not desc:
        problemas[f].append("sin meta description")
    elif len(desc) > 165:
        problemas[f].append("description larga (%d car.)" % len(desc))
    elif len(desc) < 70:
        problemas[f].append("description corta (%d car.)" % len(desc))

    if len(h1) != 1:
        problemas[f].append("tiene %d H1 (debe ser 1)" % len(h1))

    esperado = "https://www.carlouis.net/" + ("" if f == "index.html" else f)
    if not can:
        problemas[f].append("sin canonical")
    elif can.group(1) != esperado:
        problemas[f].append("canonical apunta a otra URL: %s" % can.group(1))

    if 'name="robots" content="noindex' in h:
        problemas[f].append("tiene noindex: Google no la va a mostrar")

    for alt in re.findall(r"<img(?![^>]*\balt=)[^>]*>", h):
        problemas[f].append("imagen sin alt")
        break

    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(b)
        except Exception as e:
            problemas[f].append("JSON-LD roto: %s" % e)

    for enl in set(re.findall(r'href="([^"#?:]+\.html)', h)):
        if not os.path.exists(enl):
            problemas[f].append("enlace roto a %s" % enl)
        elif enl != f:
            entrantes[enl] += 1

    if palabras < 300 and f not in ("contacto.html",):
        problemas[f].append("contenido flaco: %d palabras" % palabras)

# Duplicados entre páginas
for campo in ("titulo", "desc"):
    vistos = collections.defaultdict(list)
    for f, v in datos.items():
        if v[campo]:
            vistos[v[campo]].append(f)
    for val, fs in vistos.items():
        if len(fs) > 1:
            for f in fs:
                problemas[f].append("%s duplicado con %s" % (
                    "title" if campo == "titulo" else "description",
                    ", ".join(x for x in fs if x != f)))

# Huérfanas: nadie las enlaza, así que Google casi no las encuentra.
for f in paginas:
    if f != "index.html" and entrantes[f] == 0:
        problemas[f].append("HUÉRFANA: ninguna otra página la enlaza")

# Sitemap
sm = io.open("sitemap.xml", encoding="utf-8").read()
en_sm = set(re.findall(r"<loc>https://www\.carlouis\.net/([^<]*)</loc>", sm))
en_sm = {("index.html" if x == "" else x) for x in en_sm}
for f in paginas:
    if f not in en_sm:
        problemas[f].append("no está en el sitemap")
for x in en_sm:
    if x not in paginas and x not in FUERA:
        problemas["sitemap.xml"].append("apunta a %s, que no existe" % x)

# Reporte
total = sum(len(v) for v in problemas.values())
print("Páginas auditadas: %d" % len(paginas))
print("Palabras promedio: %d" % (sum(v["palabras"] for v in datos.values()) // len(datos)))
print("Problemas: %d en %d páginas\n" % (total, len(problemas)))
for f in sorted(problemas):
    print("  %s" % f)
    for p in problemas[f]:
        print("      - %s" % p)

print("\nEnlaces entrantes (las menos enlazadas):")
for f in sorted(paginas, key=lambda x: entrantes[x])[:8]:
    print("  %3d  %s" % (entrantes[f], f))
