# -*- coding: utf-8 -*-
"""Estudio de mercado y SEO de CARLOUIS Gourmet — documento estratégico.

Todos los datos provienen de mediciones directas contra sitios en vivo y de
ocho búsquedas reales del rubro corridas en septiembre de 2026.

    python tools/estudio-completo.py
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, HRFlowable)

F = "C:/Windows/Fonts"
for n, a in [("Cal", "calibri.ttf"), ("CalB", "calibrib.ttf"), ("CalI", "calibrii.ttf"),
             ("Geo", "georgia.ttf"), ("GeoB", "georgiab.ttf"), ("Mono", "consola.ttf")]:
    pdfmetrics.registerFont(TTFont(n, f"{F}/{a}"))

EMBER = colors.HexColor("#A82A10"); DEEP = colors.HexColor("#6B1608")
INK = colors.HexColor("#241A15");   INK2 = colors.HexColor("#5A4A40")
INK3 = colors.HexColor("#8B7A6D");  LINE = colors.HexColor("#E3D9CC")
PAPER2 = colors.HexColor("#F4EDE2"); BASIL = colors.HexColor("#4C6B3C")
GOLD = colors.HexColor("#9A6B12");  CHILI = colors.HexColor("#C2410C")

S = {}
S["h1"]  = ParagraphStyle("h1", fontName="GeoB", fontSize=21, leading=25, textColor=DEEP, spaceAfter=4)
S["h2"]  = ParagraphStyle("h2", fontName="GeoB", fontSize=13.5, leading=17, textColor=DEEP, spaceBefore=15, spaceAfter=6)
S["h3"]  = ParagraphStyle("h3", fontName="CalB", fontSize=11, leading=14, textColor=EMBER, spaceBefore=9, spaceAfter=3)
S["p"]   = ParagraphStyle("p", fontName="Cal", fontSize=9.8, leading=14, textColor=INK, spaceAfter=6)
S["li"]  = ParagraphStyle("li", fontName="Cal", fontSize=9.8, leading=14, textColor=INK, spaceAfter=3, leftIndent=10, bulletIndent=2)
S["small"] = ParagraphStyle("small", fontName="Cal", fontSize=8.3, leading=11.5, textColor=INK3)
S["lede"] = ParagraphStyle("lede", fontName="Cal", fontSize=11, leading=16, textColor=INK2, spaceAfter=8)
S["eyebrow"] = ParagraphStyle("eb", fontName="Mono", fontSize=7.2, leading=10, textColor=EMBER, spaceAfter=3)
S["cell"] = ParagraphStyle("cell", fontName="Cal", fontSize=8.2, leading=11, textColor=INK)
S["cellb"] = ParagraphStyle("cellb", fontName="CalB", fontSize=8.2, leading=11, textColor=INK)
S["th"]  = ParagraphStyle("th", fontName="CalB", fontSize=7.5, leading=9.5, textColor=colors.white)
S["ct"]  = ParagraphStyle("ct", fontName="GeoB", fontSize=30, leading=34, textColor=DEEP, spaceAfter=8)
S["cs"]  = ParagraphStyle("cs", fontName="Cal", fontSize=12.5, leading=18, textColor=INK2)

def P(t, s="p"): return Paragraph(t, S[s])
def LI(t): return Paragraph(t, S["li"], bulletText="•")
def rule(c=LINE, w=0.6): return HRFlowable(width="100%", thickness=w, color=c, spaceBefore=3, spaceAfter=7)

def tabla(datos, anchos, zebra=True, fuente=None):
    est = fuente or "cell"
    filas = [[Paragraph(str(c), S["th" if i == 0 else est]) for c in fila] for i, fila in enumerate(datos)]
    t = Table(filas, colWidths=anchos, repeatRows=1)
    cmds = [("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 4.5), ("BOTTOMPADDING", (0,0), (-1,-1), 4.5),
            ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("LINEBELOW", (0,0), (-1,-2), 0.35, LINE),
            ("BOX", (0,0), (-1,-1), 0.55, LINE),
            ("BACKGROUND", (0,0), (-1,0), DEEP)]
    if zebra:
        for i in range(1, len(datos)):
            if i % 2 == 0: cmds.append(("BACKGROUND", (0,i), (-1,i), PAPER2))
    t.setStyle(TableStyle(cmds)); return t

def caja(titulo, cuerpo, color=EMBER, fondo=PAPER2):
    inner = [Paragraph(titulo, ParagraphStyle("bt", fontName="CalB", fontSize=9.8, leading=13,
                                              textColor=color, spaceAfter=3))]
    for c in cuerpo:
        inner.append(Paragraph(c, ParagraphStyle("bc", fontName="Cal", fontSize=9.2, leading=12.8,
                                                 textColor=INK, spaceAfter=3)))
    t = Table([[inner]], colWidths=[166*mm])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), fondo),
                           ("LINEBEFORE", (0,0), (0,-1), 2.5, color),
                           ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
                           ("LEFTPADDING", (0,0), (-1,-1), 9), ("RIGHTPADDING", (0,0), (-1,-1), 9)]))
    return t

def cifra(valor, etiqueta, nota, color=INK):
    return [Paragraph(f'<font color="{color}">{valor}</font>',
                      ParagraphStyle("cv", fontName="GeoB", fontSize=17, leading=20, alignment=1)),
            Paragraph(etiqueta, ParagraphStyle("ce", fontName="Mono", fontSize=6.5, leading=9,
                                               textColor=INK3, alignment=1)),
            Paragraph(nota, ParagraphStyle("cn", fontName="Cal", fontSize=7.5, leading=10,
                                           textColor=INK3, alignment=1))]

def panel_cifras(items):
    t = Table([[cifra(*i) for i in items]], colWidths=[166*mm/len(items)]*len(items))
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                           ("BOX",(0,0),(-1,-1),0.55,LINE),
                           ("INNERGRID",(0,0),(-1,-1),0.55,LINE),
                           ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    return t

# ══════════════════════════════════════════════════════════ DATOS

BUSQUEDAS = [
 ("salsas artesanales picantes Costa Rica", "Chile Monoloco, Bendito Chile, Santísima, Green Corner, Ecomuna", "No"),
 ("comprar salsa picante artesanal Costa Rica en línea", "Walmart, Mas x Menos, Triquitraque, Ecomuna, Yaxa, Le Piquant La Selva", "No"),
 ("salsa de habanero Costa Rica comprar", "Walmart (Herdez), Triquitraque, Confites Mexicanos (El Yucateco), Ecomuna", "No"),
 ("chimichurri artesanal Costa Rica comprar", "Walmart (Magna, Maggi), PriceSmart (Camoi), Turri, Mercato, El Arreo", "No"),
 ("pesto albahaca artesanal Costa Rica", "Walmart (De Silvestri), Green Corner, Verde Salvia", "No"),
 ("productos gourmet artesanales Costa Rica conservas", "Rojas Gourmet, Liliana Gourmet, ConservadosCR, Turri, Línea Gourmet, Delika", "No"),
 ("alioli / tomates deshidratados artesanal Costa Rica", "Ningún productor costarricense. Solo importados de España, Italia y Chile", "No"),
 ("regalos gourmet canasta Costa Rica artesanal", "Café Britt, Regalos Costa Rica, Saboreando CR, Mercato, canasteros", "No"),
]

COMPETIDORES = [
 ("<b>CARLOUIS</b>", "<b>795</b>", "<b>13</b>", "<b>44</b>", "<b>HTML estático</b>", "<b>Las cinco</b>"),
 ("Green Corner", "1.591", "3", "677", "Shopify", "Pestos y picantes"),
 ("Ecomuna Market", "875", "2", "347", "WordPress", "Revende terceros"),
 ("Turri.cr", "650", "2", "136", "WordPress", "Revende terceros"),
 ("Chile Monoloco", "493", "1", "177", "WordPress", "Picantes"),
 ("Bendito Chile", "406", "0", "—", "otra", "Picantes"),
 ("Rojas Gourmet", "111", "0", "136", "Google Sites", "Conservas"),
 ("Le Piquant La Selva", "17", "0", "7", "otra", "Picantes"),
 ("Liliana Gourmet", "1", "0", "0", "otra", "Conservas"),
]

KEYWORDS_N1 = [
 ("Marca", "carlouis gourmet", "Portada y ficha de Google", "Nula"),
 ("Producto único", "salsa de piña habanero costa rica", "/salsa-pina-habanero.html", "Nula"),
 ("Producto vacío", "alioli artesanal costa rica", "/alioli.html", "Nula"),
 ("Producto vacío", "mayonesa de culantro costa rica", "/mayonesa-de-culantro.html", "Nula"),
 ("Producto vacío", "chile morrón asado en aceite costa rica", "/chile-morron-asado.html", "Nula"),
 ("Producto vacío", "tomates deshidratados artesanales costa rica", "/tomates-deshidratados.html", "Nula"),
 ("Local", "salsas gourmet alajuela", "Portada y /encuentranos.html", "Baja"),
 ("Informativa", "con qué se come el chimichurri", "/con-que-se-come-el-chimichurri.html", "Baja"),
]

KEYWORDS_N2 = [
 ("Producto", "pesto de tomate costa rica", "/pesto-de-tomate.html", "Baja"),
 ("Producto", "mayonesa de chipotle costa rica", "/mayonesa-de-chipotle.html", "Baja"),
 ("Producto", "salsa de mora costa rica", "/salsa-de-mora.html", "Baja"),
 ("Informativa", "qué salsa va con casado", "/salsas-para-comida-tica.html", "Nula"),
 ("Informativa", "cómo armar una tabla de quesos", "/tabla-de-quesos-y-bocas.html", "Media"),
 ("Informativa", "recetas con pesto", "/recetas-con-pesto.html", "Media"),
 ("Transaccional", "salsas artesanales envío costa rica", "/cobertura.html", "Media"),
]

KEYWORDS_N3 = [
 ("Categoría", "chimichurri artesanal costa rica", "/chimichurri-argentino.html", "Media"),
 ("Categoría", "pesto de albahaca artesanal costa rica", "/pesto-de-albahaca.html", "Media-alta"),
 ("Categoría", "salsa de habanero costa rica", "/salsa-habanero-fire.html", "Alta"),
 ("Estacional", "regalos gourmet costa rica", "/regalos-gourmet-costa-rica.html", "Alta"),
 ("Genérica", "salsas artesanales costa rica", "Portada", "Alta"),
 ("Genérica", "salsa picante costa rica", "Portada y /productos.html", "Muy alta"),
]


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Cal", 7.2); canvas.setFillColor(INK3)
    canvas.drawString(22*mm, 12*mm, "Estudio de mercado y SEO · CARLOUIS Gourmet · 17 de septiembre de 2026")
    canvas.drawRightString(188*mm, 12*mm, str(doc.page))
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4)
    canvas.line(22*mm, 16*mm, 188*mm, 16*mm)
    canvas.restoreState()


def build(salida):
    doc = SimpleDocTemplate(salida, pagesize=A4, leftMargin=22*mm, rightMargin=22*mm,
                            topMargin=20*mm, bottomMargin=22*mm,
                            title="Estudio de mercado y SEO — CARLOUIS Gourmet",
                            author="CARLOUIS Gourmet")
    E = []

    # ─────────────────────────────────── Portada
    E += [Spacer(1, 38*mm),
          P("DOCUMENTO ESTRATÉGICO · CONFIDENCIAL", "eyebrow"),
          Paragraph("Cómo poner a CARLOUIS<br/>de primera en Google<br/>Costa Rica", S["ct"]),
          Spacer(1, 5*mm),
          Paragraph("Estudio de mercado, análisis competitivo y plan de posicionamiento "
                    "para una marca artesanal de salsas y conservas gourmet.", S["cs"]),
          Spacer(1, 10*mm), rule(EMBER, 1.6), Spacer(1, 3*mm)]
    t = Table([[Paragraph(a, S["small"]), Paragraph(b, S["cellb"])] for a, b in [
        ("Preparado para", "CARLOUIS Gourmet · Alajuela, Costa Rica"),
        ("Sitio analizado", "www.carlouis.net"),
        ("Fecha del estudio", "17 de septiembre de 2026"),
        ("Alcance", "8 búsquedas del rubro · 9 competidores medidos · 30 páginas auditadas"),
        ("Método", "Medición directa de sitios en vivo. Sin estimaciones de terceros."),
    ]], colWidths=[36*mm, 130*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BOTTOMPADDING",(0,0),(-1,-1),4),
                           ("TOPPADDING",(0,0),(-1,-1),1)]))
    E += [t, PageBreak()]

    # ─────────────────────────────────── 1. Para qué sirve
    E += [P("Para qué sirve este documento", "h1"), rule(EMBER, 1.2),
          P("Este estudio responde tres preguntas: <b>qué tan grande es la oportunidad</b>, "
            "<b>contra quién se compite</b> y <b>qué hay que hacer, en qué orden</b>, para que "
            "CARLOUIS aparezca de primera cuando alguien en Costa Rica busca una salsa "
            "artesanal en Google.", "lede"),
          P("No es un documento de recomendaciones generales. Cada afirmación viene de una "
            "medición: ocho búsquedas reales del rubro corridas en septiembre de 2026, y los "
            "sitios de nueve competidores abiertos y medidos uno por uno."),
          Spacer(1, 3*mm)]
    E.append(caja("La conclusión, en una línea", [
        "El mercado costarricense de salsas y conservas artesanales <b>no tiene ningún "
        "especialista fuerte posicionado en Google</b>. Las primeras posiciones están repartidas "
        "entre cadenas de supermercado que venden marcas masivas e importadas, y revendedores "
        "que no fabrican nada.",
        "CARLOUIS ya tiene el mejor sitio del sector en lo técnico. Lo que falta no es programar: "
        "es hacerse visible.",
    ], BASIL, colors.HexColor("#E7EEE2")))
    E.append(PageBreak())

    # ─────────────────────────────────── 2. Metodología
    E += [P("1. Metodología, fuentes y limitaciones", "h1"), rule(EMBER, 1.2),
          P("Qué se midió y cómo", "h2"),
          tabla([["Fuente", "Qué aporta"],
                 ["Búsquedas reales en Google", "Ocho consultas del rubro para ver quién ocupa las primeras posiciones y, sobre todo, quién <b>no</b> aparece."],
                 ["Medición directa de sitios", "Se abrió el sitio de cada competidor y se midió contenido, datos estructurados, plataforma y peso."],
                 ["Auditoría del propio sitio", "30 páginas indexables revisadas: enlaces, marcado, velocidad y comportamiento en móvil."],
                 ["Consulta DNS y de cabeceras", "Verificación de que Google puede efectivamente entrar al sitio."]],
                [40*mm, 126*mm]),
          P("Limitaciones que hay que tener presentes", "h2")]
    for t_, d in [
        ("No hay datos de Search Console", "La propiedad está creada pero el sitio no acumula historial porque hasta el 31 de agosto Google no podía entrar. No se puede reportar clics ni impresiones reales."),
        ("No hay analítica instalada", "El sitio tiene la medición lista pero apagada: falta pegar el identificador de Google Analytics. Hoy <b>nadie sabe cuánta gente visita el sitio</b>."),
        ("No se usaron herramientas de volumen de búsqueda pagas", "Las estimaciones de dificultad salen de la fuerza observada de los competidores, no de un número de búsquedas mensuales."),
        ("Los conteos de reseñas no se pudieron verificar", "Google no permite leerlos de forma automatizada. Se omiten en vez de estimarlos."),
    ]:
        E.append(P(f"<b>{t_}.</b> {d}"))
    E.append(PageBreak())

    # ─────────────────────────────────── 3. Resumen ejecutivo
    E += [P("2. Resumen ejecutivo", "h1"), rule(EMBER, 1.2),
          P("Las tres cosas que deciden el resultado.", "lede")]
    E.append(caja("1 · El sitio no aparece en ninguna búsqueda del rubro", [
        "De las ocho búsquedas corridas, <b>carlouis.net apareció en cero</b>. Lo único que "
        "devuelve Google al buscar la marca es el repositorio de código en GitHub.",
        "La causa raíz ya se corrigió: hasta el 31 de agosto no existía el registro DNS de "
        "www.carlouis.net y Google recibía «Host unknown». Pero la indexación no se recupera "
        "sola: hay que pedirla página por página.",
    ], CHILI, colors.HexColor("#FBE6DC")))
    E.append(Spacer(1, 4*mm))
    E.append(caja("2 · La ventaja técnica ya está construida y es real", [
        "CARLOUIS tiene <b>13 tipos de datos estructurados</b> contra 3 del mejor competidor, y "
        "pesa <b>44 KB contra 677 KB</b> de Green Corner. Es el sitio más liviano y mejor "
        "marcado de todo el sector.",
        "Ningún competidor tiene páginas individuales por producto con preguntas frecuentes, ni "
        "contenido que explique cómo usar lo que venden.",
    ], BASIL, colors.HexColor("#E7EEE2")))
    E.append(Spacer(1, 4*mm))
    E.append(caja("3 · Seis de doce productos no tienen competencia digital alguna", [
        "Alioli, mayonesa de culantro, chile morrón asado, tomates deshidratados, pesto de "
        "tomate y piña habanero: <b>ningún productor costarricense los está posicionando</b>.",
        "En tomates deshidratados, los resultados son todos importados de España, Italia y "
        "Chile. No hay un solo productor tico compitiendo por ese término.",
    ], GOLD, colors.HexColor("#F7ECD4")))
    E.append(PageBreak())

    # ─────────────────────────────────── 4. Punto de partida
    E += [P("3. Punto de partida: qué dice Google hoy", "h1"), rule(EMBER, 1.2),
          panel_cifras([
            ("0", "DE 8 BÚSQUEDAS", "apariciones del sitio", CHILI),
            ("30", "PÁGINAS", "listas e indexables", BASIL),
            ("13.619", "PALABRAS", "de contenido propio", BASIL),
            ("0,48 s", "RESPUESTA", "bueno es bajo 0,8 s", BASIL),
          ]), Spacer(1, 5*mm),
          P("Lo que esto significa", "h2"),
          P("El sitio está completo, es rápido y está mejor construido que el de cualquier "
            "competidor. Pero <b>es invisible</b>: Google todavía no lo muestra para ninguna "
            "búsqueda del rubro, ni siquiera para la marca."),
          P("Esto no es un problema de calidad del sitio. Es un problema de antigüedad y de "
            "indexación: el sitio fue inalcanzable para Google hasta hace 17 días. Un dominio "
            "que acaba de volverse rastreable necesita que se le pida la indexación de forma "
            "explícita, y después tiempo."),
          Spacer(1, 3*mm)]
    E.append(caja("Lo más urgente de todo el documento", [
        "Entrar a Search Console y pedir indexación de las 30 URLs, empezando por la portada, "
        "el catálogo y las seis fichas de producto sin competencia.",
        "Google limita las solicitudes por día, así que son varios días de trabajo. "
        "<b>Sin esto, nada de lo demás sirve.</b>",
    ]))
    E.append(PageBreak())

    # ─────────────────────────────────── 5. El mercado
    E += [P("4. El mercado costarricense", "h1"), rule(EMBER, 1.2),
          P("Quién ocupa hoy las primeras posiciones, por tipo de jugador.", "lede"),
          tabla([["Tipo", "Quiénes son", "Su fuerza", "Su debilidad"],
                 ["Cadenas y<br/>mayoristas",
                  "Walmart, Mas x Menos, MaxiPalí, PriceSmart",
                  "Dominan los términos genéricos con marcas masivas: Magna, Maggi, Camoi, De Silvestri, Herdez",
                  "No son artesanales ni pueden decir que lo son. No compiten por «hecho a mano» ni por contenido de uso."],
                 ["Importadores<br/>de marca",
                  "El Yucateco, Herdez (vía Confites Mexicanos, Triquitraque)",
                  "Reconocimiento de marca internacional en picantes",
                  "Son producto importado. Pierden todo el terreno de «hecho en Costa Rica»."],
                 ["Marketplaces<br/>gourmet",
                  "Ecomuna Market, Turri.cr, Mercato, Línea Gourmet, Yaxa, Delika",
                  "Buen posicionamiento y catálogo amplio",
                  "Venden marcas ajenas. <b>Se les puede vender a ellos en vez de competirles.</b>"],
                 ["Productores<br/>artesanales",
                  "Green Corner, Chile Monoloco, Bendito Chile, Santísima, Le Piquant La Selva, ConservadosCR, Rojas Gourmet, Liliana Gourmet",
                  "Antigüedad de dominio y reconocimiento local",
                  "Sitios débiles o abandonados. Es el rival real y es alcanzable."]],
                [23*mm, 40*mm, 48*mm, 55*mm]),
          P("Un mercado sin líder digital", "h2"),
          P("El hallazgo más importante de las ocho búsquedas no es quién sale, sino <b>quién no "
            "sale</b>. En ninguna consulta aparece un productor artesanal costarricense con un "
            "sitio propio fuerte. El primer lugar lo ocupan supermercados vendiendo marcas "
            "industriales y revendedores que no fabrican nada."),
          P("En categorías como alioli, mayonesas saborizadas y tomates deshidratados "
            "artesanales, directamente <b>no hay ningún productor tico compitiendo</b>. Los "
            "resultados son importados.")]
    E.append(PageBreak())

    # ─────────────────────────────────── 6. Las ocho búsquedas
    E += [P("5. Las ocho búsquedas del rubro", "h1"), rule(EMBER, 1.2),
          P("Corridas en Google en septiembre de 2026. La última columna es la que importa.", "lede"),
          tabla([["Búsqueda", "Quién aparece en la primera página", "¿Sale<br/>CARLOUIS?"]] +
                [[f'<font name="Mono" size="7">{b}</font>', q,
                  f'<font color="#C2410C"><b>{s}</b></font>'] for b, q, s in BUSQUEDAS],
                [45*mm, 100*mm, 21*mm]),
          Spacer(1, 4*mm)]
    E.append(caja("Cómo leer esta tabla", [
        "<b>Ocho de ocho en «No».</b> No es que CARLOUIS salga en posición 20 o 30: no aparece "
        "en absoluto, porque el sitio todavía no está indexado.",
        "La lectura optimista: los que sí salen son vencibles. Ninguno tiene contenido de uso, "
        "ninguno responde las preguntas que hace la gente antes de comprar, y varios tienen "
        "sitios en estado de abandono.",
    ]))
    E.append(PageBreak())

    # ─────────────────────────────────── 7. Competidores medidos
    E += [P("6. Los competidores, medidos uno por uno", "h1"), rule(EMBER, 1.2),
          P("Cada sitio se abrió y se midió el 17 de septiembre de 2026. «Datos estructurados» "
            "es el marcado que Google usa para entender de qué trata un negocio y mostrar "
            "resultados enriquecidos.", "lede"),
          tabla([["Marca", "Palabras<br/>portada", "Tipos de<br/>datos estr.", "Peso<br/>(KB)", "Plataforma", "Dónde compite"]] +
                [list(c) for c in COMPETIDORES],
                [32*mm, 20*mm, 22*mm, 17*mm, 28*mm, 47*mm]),
          Spacer(1, 4*mm)]
    E.append(caja("Lo que revela la tabla", [
        "<b>Green Corner es el único rival serio:</b> 1.591 palabras y presencia en dos "
        "categorías. Pero su título de portada es solo «Green Corner», sin una sola palabra "
        "clave, y su sitio pesa 677 KB. Está posicionado por marca, no por producto.",
        "<b>Cuatro competidores tienen sitios prácticamente abandonados:</b> Liliana Gourmet "
        "carga una sola palabra y no tiene ni título ni descripción; Le Piquant La Selva, 17 "
        "palabras; Rojas Gourmet vive en un Google Sites sin título.",
        "<b>CARLOUIS tiene más del cuádruple de datos estructurados que el mejor competidor</b> "
        "y es quince veces más liviano que Green Corner.",
    ]))
    E.append(PageBreak())

    # ─────────────────────────────────── 8. Los cinco más fuertes
    E += [P("7. Los cinco más fuertes: cómo ganarles", "h1"), rule(EMBER, 1.2)]
    for nombre, perfil, debil, plan in [
        ("Green Corner",
         "El competidor de referencia. Shopify, 1.591 palabras, vende pestos y salsas picantes orgánicas, y además distribuye por Ecomuna.",
         "Título de portada sin palabras clave. Sitio pesado (677 KB). No tiene contenido de uso ni recetas. No explica cuánto pica nada.",
         "Ganarle por producto específico, no por marca. Su fuerza está en «orgánico»; la de CARLOUIS en «artesanal», «escala de picante» y «hecho en Alajuela». Las guías de uso son terreno que ellos no pisan."),
        ("Chile Monoloco",
         "Marca de picantes con identidad fuerte y buen posicionamiento por el término «salsas picantes de Costa Rica».",
         "493 palabras, un solo tipo de datos estructurados, WordPress de 177 KB. Cero contenido de apoyo.",
         "Ya se le supera en contenido y marcado. Falta que Google indexe. La escala de picante documentada es una diferencia que ellos no tienen."),
        ("Ecomuna Market",
         "Marketplace con buen posicionamiento que revende marcas artesanales, entre ellas Santísima y Green Corner.",
         "No fabrica nada. Depende de las marcas que distribuye.",
         "<b>No competirle: venderle.</b> Entrar a su catálogo genera ventas y un enlace desde un sitio con autoridad. Es la vía más rápida a un enlace de calidad."),
        ("Walmart / PriceSmart",
         "Dominan los términos genéricos como «chimichurri» o «salsa picante» con marcas masivas.",
         "No son artesanales. No pueden competir por «hecho a mano» ni por historia de producto.",
         "No pelear el genérico. Ganar el long-tail: «chimichurri artesanal», «con qué se come el chimichurri», «hecho en Costa Rica»."),
        ("Le Piquant La Selva / Liliana Gourmet / Rojas Gourmet",
         "Marcas reales con presencia en el mercado físico.",
         "Sitios abandonados o sin construir: entre 1 y 111 palabras, sin título, sin descripción, sin datos estructurados.",
         "Son los más fáciles de superar. Basta con que Google indexe CARLOUIS para pasarlos en cualquier término que compartan."),
    ]:
        E.append(KeepTogether([
            P(nombre, "h3"),
            P(f"<b>Qué es.</b> {perfil}"),
            P(f"<b>Dónde falla.</b> {debil}"),
            P(f"<b>Cómo ganarle.</b> {plan}"),
            Spacer(1, 2*mm)]))
    E.append(PageBreak())

    # ─────────────────────────────────── 9. Dónde está parada
    E += [P("8. Dónde está parada CARLOUIS hoy", "h1"), rule(EMBER, 1.2),
          P("Dónde gana", "h2")]
    for t_, d in [
        ("Amplitud de catálogo", "Doce productos en cuatro categorías. Ningún competidor artesanal cubre tanto: Chile Monoloco y Bendito Chile solo hacen picantes; Verde Salvia solo pestos."),
        ("Base técnica", "El sitio más liviano y mejor marcado del sector, con diferencia. Es una ventaja ya construida."),
        ("Contenido de uso", "Nueve guías que responden qué hacer con cada producto. Ningún competidor tiene una sola."),
        ("Presencia física", "La feria de los sábados genera prueba de producto, clientes recurrentes y material real para publicar."),
        ("Precio único nacional", "Simplifica la decisión y ningún competidor lo comunica con claridad."),
    ]:
        E.append(P(f"<b>{t_}.</b> {d}"))

    E.append(P("Dónde pierde", "h2"))
    for t_, d in [
        ("Invisible en Google", "Cero apariciones en ocho búsquedas. Es el problema número uno y todo lo demás depende de resolverlo."),
        ("Cero reseñas en Google", "La ficha existe y está enlazada al sitio, pero no acumula reseñas. Es el factor de mayor peso en resultados locales."),
        ("Sin enlaces externos", "Ningún sitio enlaza a carlouis.net. Es lo que más pesa en autoridad de dominio y lo que más tarda en construirse."),
        ("Sin medición", "La analítica está instalada pero apagada. Hoy es imposible saber si el sitio recibe visitas, y por lo tanto imposible demostrar resultados."),
        ("Marca desconocida en buscador", "Nadie busca «CARLOUIS» todavía. Esa demanda hay que crearla con presencia física, redes y contenido."),
    ]:
        E.append(P(f"<b>{t_}.</b> {d}"))
    E.append(PageBreak())

    # ─────────────────────────────────── 10. Diagnóstico técnico
    E += [P("9. Diagnóstico técnico del sitio", "h1"), rule(EMBER, 1.2),
          P("Auditoría del 17 de septiembre de 2026 sobre 30 páginas indexables. El sitio es "
            "HTML estático servido por Netlify, sin gestor de contenidos ni base de datos.", "lede"),
          tabla([["Aspecto", "Estado", "Detalle"],
                 ["Resolución DNS", "Resuelto", "Faltaba el registro de www y Google recibía «Host unknown». Corregido el 31 de agosto con un CNAME."],
                 ["Certificado HTTPS", "Correcto", "Válido, con redirección desde la versión sin www."],
                 ["Versión canónica", "Correcto", "Las cuatro variantes de cada dirección declaran bien su versión buena."],
                 ["Datos estructurados", "Correcto", "13 tipos: Organization, LocalBusiness, Product, FAQPage, Article, Event, ItemList y más."],
                 ["Velocidad", "Correcto", "0,48 s de respuesta. Imágenes en WebP: 1,48 MB en total. CSS y JS suman 84 KB."],
                 ["Móvil", "Correcto", "Verificado a 375 px: sin desbordes, áreas táctiles sobre 44 px."],
                 ["Sitemap y robots", "Correcto", "30 URLs, XML válido, servido como application/xml y declarado en robots.txt."],
                 ["Enlazado interno", "Correcto", "Cada producto enlaza a su guía y cada guía a sus productos."],
                 ["Analítica", "<b>Pendiente</b>", "Instalada pero sin identificador. Falta pegar el ID de Google Analytics en una línea."],
                 ["Formulario de contacto", "<b>Sin verificar</b>", "Tiene el marcado correcto de Netlify Forms pero nunca se probó un envío real."],
                 ["Indexación", "<b>Pendiente</b>", "Ninguna URL pedida manualmente. Es la tarea más urgente."]],
                [32*mm, 24*mm, 110*mm]),
          Spacer(1, 4*mm)]
    E.append(caja("Corregido durante este estudio", [
        "<b>El pedido pedía cinco campos obligatorios</b> —nombre, teléfono, cantón, distrito y "
        "dirección exacta— antes de permitir enviar. Quien solo quería retirar en la feria del "
        "sábado tenía que escribir su dirección de casa igual.",
        "Ahora se elige entre envío y retiro. Con retiro quedan dos campos obligatorios; con "
        "envío, tres. <b>Es la corrección de conversión más importante del documento.</b>",
    ], BASIL, colors.HexColor("#E7EEE2")))
    E.append(PageBreak())

    # ─────────────────────────────────── 11. Palabras clave
    E += [P("10. Palabras clave objetivo por nivel", "h1"), rule(EMBER, 1.2),
          P("Regla base: <b>una palabra clave principal, una dirección</b>. Las guías del blog "
            "apoyan a la ficha de producto con la que se relacionan, nunca compiten con ella.", "lede"),
          P("Nivel 1 — empezar ya (semanas)", "h2"),
          P("Competencia nula o casi nula. Son las victorias rápidas: posicionan en semanas y "
            "generan las primeras señales de autoridad.", "small"), Spacer(1, 2*mm),
          tabla([["Grupo", "Palabra clave principal", "Dirección destino", "Competencia"]] +
                [[a, f'<font name="Mono" size="7">{b}</font>', f'<font name="Mono" size="7">{c}</font>',
                  f'<font color="#4C6B3C"><b>{d}</b></font>'] for a, b, c, d in KEYWORDS_N1],
                [26*mm, 55*mm, 58*mm, 27*mm]),
          P("Nivel 2 — segundo trimestre", "h2"),
          tabla([["Grupo", "Palabra clave principal", "Dirección destino", "Competencia"]] +
                [[a, f'<font name="Mono" size="7">{b}</font>', f'<font name="Mono" size="7">{c}</font>',
                  f'<font color="#9A6B12"><b>{d}</b></font>'] for a, b, c, d in KEYWORDS_N2],
                [26*mm, 55*mm, 58*mm, 27*mm]),
          P("Nivel 3 — meta de largo plazo", "h2"),
          tabla([["Grupo", "Palabra clave principal", "Dirección destino", "Competencia"]] +
                [[a, f'<font name="Mono" size="7">{b}</font>', f'<font name="Mono" size="7">{c}</font>',
                  f'<font color="#C2410C"><b>{d}</b></font>'] for a, b, c, d in KEYWORDS_N3],
                [26*mm, 55*mm, 58*mm, 27*mm]),
          Spacer(1, 4*mm)]
    E.append(caja("Vocabulario costarricense: esto vale oro", [
        "La gente en Costa Rica no busca «salsa de ají» ni «pimiento». Busca <b>chile dulce</b>, "
        "<b>chile morrón</b>, <b>culantro</b> (no cilantro), <b>casado</b>, <b>gallo</b>, "
        "<b>chifrijo</b>, <b>patacones</b>, <b>yuca frita</b>, <b>soda</b>, <b>boca</b>.",
        "Ese vocabulario ya está usado en las guías y en las fichas. Es una barrera natural "
        "contra los competidores importados, que escriben en español neutro o mexicano.",
    ]))
    E.append(PageBreak())

    # ─────────────────────────────────── 12. Títulos propuestos
    E += [P("11. Títulos propuestos para las páginas de Nivel 1", "h1"), rule(EMBER, 1.2),
          P("El título es lo que Google muestra como enlace azul. Debe rondar los 60 caracteres "
            "e incluir la palabra clave y el país.", "lede"),
          tabla([["Dirección", "Título para Google", "Encabezado de la página"],
                 ["/", "Salsas Artesanales Gourmet en Costa Rica | CARLOUIS", "Salsas artesanales con sabor de verdad"],
                 ["/salsa-pina-habanero.html", "Salsa de Piña Habanero Artesanal | CARLOUIS Costa Rica", "Salsa de Piña con Habanero"],
                 ["/alioli.html", "Alioli Artesanal Casero | CARLOUIS Costa Rica", "Alioli artesanal"],
                 ["/mayonesa-de-culantro.html", "Mayonesa de Culantro Artesanal | CARLOUIS Costa Rica", "Mayonesa de Culantro artesanal"],
                 ["/chile-morron-asado.html", "Chile Morrón Asado Artesanal | CARLOUIS Costa Rica", "Chile Morrón Asado en aceite de oliva"],
                 ["/tomates-deshidratados.html", "Tomates Deshidratados en Aceite de Oliva | CARLOUIS", "Tomates Deshidratados en aceite de oliva"],
                 ["/encuentranos.html", "Dónde Comprar: Feria La Verbena, Alajuela | CARLOUIS", "Encuéntranos"]],
                [44*mm, 66*mm, 56*mm]),
          P("Todos estos títulos ya están puestos en el sitio. Se listan para que quede "
            "constancia de la estructura y para revisarlos si algún día se cambian.", "small")]
    E.append(PageBreak())

    # ─────────────────────────────────── 13. Lo ya hecho
    E += [P("12. Lo que ya quedó hecho", "h1"), rule(EMBER, 1.2),
          P("Trabajo ejecutado sobre el sitio entre el 27 de julio y el 17 de septiembre de 2026.", "lede"),
          tabla([["Entregable", "Qué cambia"],
                 ["Rediseño completo con sistema de diseño", "Un solo sistema de estilos en vez de cinco bloques que se peleaban. Tipografía propia, iconos vectoriales, escala de picante por producto."],
                 ["Rendimiento", "La portada pasó de 3,00 MB a 0,33 MB. Las imágenes del proyecto, de 9,27 MB a 1,48 MB en WebP."],
                 ["Corrección del DNS", "Se agregó el registro de www que faltaba. Sin esto Google no podía entrar al sitio."],
                 ["12 páginas de producto", "Cada producto tiene dirección propia, usos, preguntas frecuentes y datos estructurados de Product."],
                 ["9 guías de uso", "Contenido que captura la búsqueda previa a la compra. Ningún competidor tiene algo equivalente."],
                 ["Página de cobertura", "Las 7 provincias y 84 cantones con información real de envío."],
                 ["Sección de eventos", "Las ferias se anuncian y quedan archivadas como entradas de blog."],
                 ["Pedido por WhatsApp", "Panel que arma el pedido completo y lo manda en un solo mensaje, con los datos del cliente."],
                 ["Ficha de Google enlazada", "El sitio declara la ficha en sus datos estructurados, y hay botón de reseña en las 30 páginas."],
                 ["Datos estructurados completos", "13 tipos, contra 3 del mejor competidor."],
                 ["Sitemap, robots y canónicas", "30 URLs declaradas, XML válido, sin contenido duplicado."],
                 ["Medición preparada", "Falta solo pegar el identificador de Google Analytics."]],
                [48*mm, 118*mm])]
    E.append(PageBreak())

    # ─────────────────────────────────── 14. Plan
    E += [P("13. Plan de trabajo por etapas", "h1"), rule(EMBER, 1.2),
          P("En este orden. Saltarse la Etapa 1 invalida todo lo demás.", "lede"),
          P("Etapa 1 — Los próximos 15 días", "h2"),
          tabla([["Acción", "Quién", "Por qué importa"],
                 ["Pedir indexación de las 30 URLs en Search Console, empezando por portada, catálogo y las seis fichas sin competencia", "Cliente", "Es lo único que separa al sitio de aparecer. Google limita las solicitudes por día."],
                 ["Pegar el identificador de Google Analytics", "Cliente / desarrollo", "Sin esto no se puede saber si llega gente ni demostrar resultados."],
                 ["Probar el formulario de contacto y revisar que llegue al panel de Netlify", "Cliente", "Nunca se verificó. Si está roto, se están perdiendo consultas."],
                 ["Completar la ficha de Google: área de servicio a las 7 provincias y 15 fotos reales", "Cliente", "Es lo que más pesa en búsquedas locales."]],
                [66*mm, 26*mm, 74*mm]),
          P("Etapa 2 — Mes 1 y 2", "h2"),
          tabla([["Acción", "Quién", "Por qué importa"],
                 ["Pedir reseñas en la feria, en el momento, con el enlace directo", "Cliente", "Meta: 10 el primer mes, 25 en tres. Es el segundo factor local en peso."],
                 ["Contestar todas las reseñas, incluso las malas", "Cliente", "Google lo lee como señal de negocio activo."],
                 ["Registrarse en directorios con nombre y teléfono idénticos", "Cliente", "Confirma que el negocio es real."],
                 ["Ofrecer el catálogo a Ecomuna, Turri y Mercato", "Cliente", "Genera ventas y un enlace desde un sitio con autoridad. Es la vía más rápida a un enlace de calidad."]],
                [66*mm, 26*mm, 74*mm]),
          P("Etapa 3 — Mes 3 en adelante", "h2"),
          tabla([["Acción", "Quién", "Por qué importa"],
                 ["Una guía nueva al mes", "Desarrollo", "La estructura ya está: se edita un archivo y se corre el generador."],
                 ["Una entrada de blog por cada feria a la que asistan", "Desarrollo", "Contenido fresco y oportunidad de enlace del organizador."],
                 ["Buscar cobertura de prensa de emprendimiento", "Cliente", "Una nota en un medio vale más que meses de ajustes técnicos."],
                 ["Revisar en Search Console con qué palabras llega la gente", "Ambos", "Esa lista dice qué contenido escribir después."]],
                [66*mm, 26*mm, 74*mm])]
    E.append(PageBreak())

    # ─────────────────────────────────── 15. Expectativas
    E += [P("14. Qué esperar y cuándo", "h1"), rule(EMBER, 1.2),
          tabla([["Meta", "Plazo realista", "De qué depende"],
                 ["Aparecer al buscar «carlouis gourmet»", "1 a 2 semanas", "Solicitud de indexación"],
                 ["Liderar los 6 productos sin competencia", "1 a 3 meses", "Indexación y algo de antigüedad"],
                 ["Salir en el mapa en Alajuela", "1 a 2 meses", "Ficha completa y activa"],
                 ["Top 3 local en Alajuela y Santa Ana", "2 a 4 meses", "25 o más reseñas"],
                 ["Top 10 nacional por término de producto", "4 a 8 meses", "Contenido mensual sostenido"],
                 ["Primer lugar en «salsas artesanales Costa Rica»", "9 a 14 meses", "Enlaces, reseñas y constancia"]],
                [66*mm, 30*mm, 70*mm]),
          Spacer(1, 5*mm)]
    E.append(caja("Lo que este documento no promete", [
        "Los plazos suponen que se ejecutan las acciones de cada etapa. <b>No son garantías:</b> "
        "nadie controla el algoritmo de Google, y un competidor que invierta fuerte puede "
        "cambiar el escenario.",
        "Lo que sí está bajo control y ya está hecho: un sitio técnicamente superior al de los "
        "nueve competidores medidos. <b>Lo que falta depende de la operación diaria del "
        "negocio</b>, no del código: pedir indexación, juntar reseñas, publicar y conseguir "
        "que otros sitios enlacen.",
    ], GOLD, colors.HexColor("#F7ECD4")))
    E.append(Spacer(1, 5*mm))
    E.append(rule())
    E.append(P("Metodología: las ocho búsquedas del rubro se corrieron en Google en septiembre de "
               "2026. Los datos de los nueve competidores se obtuvieron accediendo directamente a "
               "sus sitios el 17 de septiembre de 2026 y midiendo contenido, datos estructurados, "
               "plataforma y peso. Las métricas del propio sitio provienen de una auditoría de sus "
               "30 páginas indexables y de mediciones de red contra el sitio en producción. Las "
               "estimaciones de dificultad y plazo se basan en la fuerza observada de esos "
               "competidores; no provienen de herramientas de volumen de búsqueda pagas.", "small"))

    doc.build(E, onFirstPage=lambda c, d: None, onLaterPages=pie)
    return salida


if __name__ == "__main__":
    out = build("Estudio-Mercado-SEO-CARLOUIS.pdf")
    print(f"  generado: {out}  ({os.path.getsize(out)/1024:.0f} KB)")
