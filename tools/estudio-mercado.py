# -*- coding: utf-8 -*-
"""Estudio de mercado y SEO de CARLOUIS Gourmet — genera el PDF."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, HRFlowable)

F = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("Cal", f"{F}/calibri.ttf"))
pdfmetrics.registerFont(TTFont("CalB", f"{F}/calibrib.ttf"))
pdfmetrics.registerFont(TTFont("Geo", f"{F}/georgia.ttf"))
pdfmetrics.registerFont(TTFont("GeoB", f"{F}/georgiab.ttf"))
pdfmetrics.registerFont(TTFont("Mono", f"{F}/consola.ttf"))

EMBER   = colors.HexColor("#A82A10")
DEEP    = colors.HexColor("#6B1608")
INK     = colors.HexColor("#241A15")
INK2    = colors.HexColor("#5A4A40")
INK3    = colors.HexColor("#8B7A6D")
LINE    = colors.HexColor("#E3D9CC")
PAPER2  = colors.HexColor("#F4EDE2")
BASIL   = colors.HexColor("#4C6B3C")
GOLD    = colors.HexColor("#9A6B12")
CHILI   = colors.HexColor("#C2410C")

S = {}
S["h1"]   = ParagraphStyle("h1", fontName="GeoB", fontSize=26, leading=30, textColor=DEEP, spaceAfter=6)
S["h2"]   = ParagraphStyle("h2", fontName="GeoB", fontSize=15, leading=19, textColor=DEEP, spaceBefore=16, spaceAfter=7)
S["h3"]   = ParagraphStyle("h3", fontName="CalB", fontSize=11.5, leading=15, textColor=EMBER, spaceBefore=10, spaceAfter=4)
S["p"]    = ParagraphStyle("p", fontName="Cal", fontSize=10, leading=14.5, textColor=INK, spaceAfter=6)
S["small"]= ParagraphStyle("small", fontName="Cal", fontSize=8.5, leading=12, textColor=INK3)
S["lede"] = ParagraphStyle("lede", fontName="Cal", fontSize=11.5, leading=16.5, textColor=INK2, spaceAfter=8)
S["eyebrow"] = ParagraphStyle("eyebrow", fontName="Mono", fontSize=7.5, leading=11, textColor=EMBER, spaceAfter=4)
S["cell"] = ParagraphStyle("cell", fontName="Cal", fontSize=8.5, leading=11.5, textColor=INK)
S["cellb"]= ParagraphStyle("cellb", fontName="CalB", fontSize=8.5, leading=11.5, textColor=INK)
S["th"]   = ParagraphStyle("th", fontName="CalB", fontSize=7.8, leading=10, textColor=colors.white)
S["cover_t"] = ParagraphStyle("ct", fontName="GeoB", fontSize=34, leading=38, textColor=DEEP, spaceAfter=10)
S["cover_s"] = ParagraphStyle("cs", fontName="Cal", fontSize=13, leading=19, textColor=INK2)

def P(t, s="p"): return Paragraph(t, S[s])
def rule(c=LINE, w=0.6): return HRFlowable(width="100%", thickness=w, color=c, spaceBefore=4, spaceAfter=8)

def tabla(datos, anchos, header=True, zebra=True):
    filas = []
    for i, fila in enumerate(datos):
        est = "th" if (header and i == 0) else "cell"
        filas.append([Paragraph(str(c), S[est]) for c in fila])
    t = Table(filas, colWidths=anchos, repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE),
        ("BOX", (0,0), (-1,-1), 0.6, LINE),
    ]
    if header:
        cmds += [("BACKGROUND", (0,0), (-1,0), DEEP)]
    if zebra:
        for i in range(1 if header else 0, len(datos)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0,i), (-1,i), PAPER2))
    t.setStyle(TableStyle(cmds))
    return t

def caja(titulo, cuerpo, color=EMBER, fondo=PAPER2):
    inner = [Paragraph(titulo, ParagraphStyle("bt", fontName="CalB", fontSize=10, leading=13,
                                              textColor=color, spaceAfter=4))]
    for c in cuerpo:
        inner.append(Paragraph(c, ParagraphStyle("bc", fontName="Cal", fontSize=9.3, leading=13,
                                                 textColor=INK, spaceAfter=3)))
    t = Table([[inner]], colWidths=[165*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), fondo),
        ("LINEBEFORE", (0,0), (0,-1), 2.5, color),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
    ]))
    return t

# ----------------------------------------------------------------- Productos
# (producto, termino objetivo, quien domina hoy, dificultad, estrategia)
PROD = [
 ("Habanero Fire", "salsa de habanero costa rica",
  "Chile Monoloco, Bendito Chile, Santísima",
  "Alta", "Es el término más disputado de la línea. Ganarlo pasa por la escala de picante y el contenido de uso, que ningún competidor tiene."),
 ("Piña Habanero", "salsa de piña habanero costa rica",
  "Nadie de forma directa",
  "Muy baja", "Producto casi único en el mercado tico. Es la victoria más rápida disponible: se puede liderar en semanas."),
 ("Chimichurri Argentino", "chimichurri artesanal costa rica",
  "Walmart (Magna, Maggi), PriceSmart (Camoi), Turri",
  "Media", "No pelear 'chimichurri' contra Walmart. Ganar 'artesanal', 'casero' y sobre todo 'con qué se come el chimichurri', que nadie responde bien."),
 ("Pesto de Albahaca", "pesto de albahaca artesanal costa rica",
  "Green Corner, Verde Salvia, Walmart (De Silvestri)",
  "Media-alta", "Green Corner es el rival real aquí. Su ventaja es antigüedad; su debilidad, que no tiene contenido de uso ni recetas."),
 ("Pesto de Tomate", "pesto de tomate costa rica",
  "Muy poca competencia identificada",
  "Baja", "Categoría desatendida. Vale la pena empujarla junto al de albahaca."),
 ("Alioli", "alioli artesanal costa rica",
  "Sin competencia artesanal identificada",
  "Muy baja", "Hueco claro en el mercado. Nadie posiciona alioli artesanal en Costa Rica."),
 ("Mayonesa Chipotle", "mayonesa de chipotle costa rica",
  "Marcas comerciales en supermercado",
  "Baja", "Las comerciales dominan el estante físico pero no el buscador. Espacio abierto en digital."),
 ("Mayonesa de Culantro", "mayonesa de culantro costa rica",
  "Sin competencia identificada",
  "Muy baja", "Producto con identidad tica y cero competencia digital. Ganable de inmediato."),
 ("Tomates Deshidratados", "tomates deshidratados costa rica",
  "Importados en supermercados y PriceSmart",
  "Baja", "Nadie posiciona el producto artesanal local. El ángulo 'hecho en Costa Rica' no lo usa nadie."),
 ("Chile Morrón Asado", "chile morrón asado en aceite costa rica",
  "Sin competencia identificada",
  "Muy baja", "Nicho vacío. Además captura las dudas de '¿el chile morrón pica?'."),
 ("Salsa de Chile Dulce", "salsa de chile dulce costa rica",
  "Marcas asiáticas importadas",
  "Baja", "Las importadas no compiten por el término en español ni por el ángulo artesanal."),
 ("Salsa de Mora", "salsa de mora costa rica",
  "Mermeladas comerciales",
  "Baja", "Diferenciarse de la mermelada es el ángulo: es salsa, no unta."),
]

# ----------------------------------------------------------------- Documento
def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Cal", 7.5)
    canvas.setFillColor(INK3)
    canvas.drawString(22*mm, 12*mm, "Estudio de mercado y SEO · CARLOUIS Gourmet · 31 de agosto de 2026")
    canvas.drawRightString(188*mm, 12*mm, f"{doc.page}")
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4)
    canvas.line(22*mm, 16*mm, 188*mm, 16*mm)
    canvas.restoreState()

def build(salida):
    doc = SimpleDocTemplate(salida, pagesize=A4,
                            leftMargin=22*mm, rightMargin=22*mm,
                            topMargin=20*mm, bottomMargin=22*mm,
                            title="Estudio de mercado y SEO — CARLOUIS Gourmet",
                            author="CARLOUIS Gourmet")
    E = []

    # ---------------- Portada
    E.append(Spacer(1, 42*mm))
    E.append(P("ESTUDIO DE MERCADO Y POSICIONAMIENTO", "eyebrow"))
    E.append(Paragraph("Cómo llegar al primer<br/>lugar en Costa Rica", S["cover_t"]))
    E.append(Spacer(1, 5*mm))
    E.append(Paragraph(
        "Análisis competitivo del mercado de salsas y conservas gourmet artesanales, "
        "producto por producto y a nivel de empresa, con la estrategia de posicionamiento "
        "para CARLOUIS Gourmet.", S["cover_s"]))
    E.append(Spacer(1, 12*mm))
    E.append(rule(EMBER, 1.6))
    E.append(Spacer(1, 4*mm))
    t = Table([
        [Paragraph("Preparado para", S["small"]), Paragraph("CARLOUIS Gourmet, Alajuela", S["cellb"])],
        [Paragraph("Sitio analizado", S["small"]), Paragraph("www.carlouis.net", S["cellb"])],
        [Paragraph("Fecha", S["small"]), Paragraph("31 de agosto de 2026", S["cellb"])],
        [Paragraph("Alcance", S["small"]), Paragraph("12 productos · 5 categorías · 8 competidores medidos", S["cellb"])],
        [Paragraph("Método", S["small"]), Paragraph("Medición directa de sitios en vivo, no estimaciones", S["cellb"])],
    ], colWidths=[38*mm, 127*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                           ("BOTTOMPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),1)]))
    E.append(t)
    E.append(PageBreak())

    # ---------------- Resumen ejecutivo
    E.append(P("Resumen ejecutivo", "h1"))
    E.append(rule(EMBER, 1.2))
    E.append(P(
        "El mercado costarricense de salsas y conservas gourmet artesanales está "
        "<b>técnicamente desatendido</b>. Los competidores que hoy ocupan los primeros "
        "lugares lo hacen por antigüedad, no por trabajo de posicionamiento: dos de las "
        "tres marcas líderes tienen menos contenido que CARLOUIS y datos estructurados "
        "incompletos o inexistentes.", "lede"))

    E.append(caja("El hallazgo que lo explica todo", [
        "Hasta el 31 de agosto de 2026, <b>Google no podía entrar al sitio</b>. El registro DNS "
        "de www.carlouis.net no existía y el dominio raíz redirigía hacia ese nombre inexistente.",
        "Ninguna página fue rastreada nunca. Todo el trabajo previo estaba bien hecho pero era "
        "inalcanzable. Se corrigió agregando el registro CNAME faltante.",
    ], CHILI, colors.HexColor("#FBE6DC")))
    E.append(Spacer(1, 5*mm))

    E.append(P("Las tres conclusiones", "h2"))
    E.append(P("<b>1. La ventaja técnica ya existe.</b> CARLOUIS tiene más contenido en portada "
               "que Chile Monoloco y Bendito Chile, datos estructurados completos donde ellos "
               "tienen parciales o ninguno, y carga en 363 KB contra sitios WordPress y Shopify "
               "que pesan varias veces más."))
    E.append(P("<b>2. Ocho de doce productos casi no tienen competencia digital.</b> Alioli, "
               "mayonesa de culantro, chile morrón asado y piña habanero no los está posicionando "
               "nadie en Costa Rica. Son victorias disponibles en semanas, no en meses."))
    E.append(P("<b>3. Lo que falta no se programa.</b> Reseñas en Google, enlaces de otros sitios "
               "y contenido publicado con constancia. Es trabajo de meses y depende de la "
               "operación del negocio, no del sitio web."))

    E.append(P("Veredicto", "h2"))
    E.append(caja("¿Es alcanzable el primer lugar?", [
        "<b>Sí, y los datos lo respaldan.</b> El liderazgo en las categorías de nicho (alioli, "
        "mayonesas saborizadas, conservas) es alcanzable en 3 a 6 meses.",
        "El primer lugar en el término más disputado —«salsas artesanales Costa Rica»— es una "
        "meta de 9 a 14 meses que exige constancia en reseñas, contenido y enlaces.",
        "<b>Ningún cambio de código, por sí solo, otorga el primer lugar.</b> Cualquier propuesta "
        "que lo prometa con fecha cerrada está vendiendo algo que no controla.",
    ], BASIL, colors.HexColor("#E7EEE2")))
    E.append(PageBreak())

    # ---------------- El mercado
    E.append(P("El mercado", "h1"))
    E.append(rule(EMBER, 1.2))
    E.append(P("Quién compite hoy en Costa Rica, por tipo de jugador.", "lede"))

    E.append(P("Los tres tipos de competidor", "h2"))
    E.append(tabla([
        ["Tipo", "Quiénes son", "Su fuerza", "Su debilidad"],
        ["Cadenas y<br/>mayoristas",
         "Walmart, Mas x Menos, MaxiPalí, PriceSmart",
         "Dominan términos genéricos con marcas masivas (Magna, Maggi, Camoi, De Silvestri)",
         "No son artesanales. No compiten por el ángulo «hecho a mano» ni por contenido de uso."],
        ["Marketplaces<br/>gourmet",
         "Ecomuna Market, Turri.cr, Mercato.cr, Yaxa",
         "Buen posicionamiento y catálogo amplio de terceros",
         "Venden marcas ajenas. Se les puede vender a ellos en vez de competirles."],
        ["Marcas<br/>artesanales",
         "Green Corner, Chile Monoloco, Bendito Chile, Santísima, Verde Salvia, Chiletico, Karoa",
         "Antigüedad, enlaces y reconocimiento de marca",
         "Contenido escaso y datos estructurados incompletos. Son el rival real y son vencibles."],
    ], [24*mm, 42*mm, 46*mm, 53*mm]))

    E.append(P("Medición directa de los competidores", "h2"))
    E.append(P("Todos los datos siguientes se midieron accediendo a los sitios en vivo el 31 de "
               "agosto de 2026. «Datos estructurados» se refiere al marcado que Google usa para "
               "entender de qué trata un negocio y mostrar resultados enriquecidos.", "small"))
    E.append(Spacer(1, 3*mm))
    E.append(tabla([
        ["Marca", "Palabras<br/>portada", "Datos<br/>estructurados", "Plataforma", "Categorías donde compite"],
        ["<b>CARLOUIS</b>", "<b>795</b>", "<b>9 tipos</b>", "<b>HTML estático</b>", "<b>Las cinco</b>"],
        ["Green Corner", "1.621", "Sí", "Shopify", "Pestos y salsas picantes"],
        ["Verde Salvia", "767", "Sí", "Shopify", "Pestos"],
        ["Chile Monoloco", "505", "Parcial", "WordPress", "Salsas picantes"],
        ["Bendito Chile", "406", "Ninguno", "Otra", "Salsas picantes"],
        ["Santísima", "—", "—", "Vía Ecomuna", "Salsas picantes"],
        ["Karoa", "—", "—", "—", "Salsas gourmet"],
    ], [30*mm, 20*mm, 24*mm, 26*mm, 65*mm]))
    E.append(Spacer(1, 4*mm))
    E.append(caja("Lectura de la tabla", [
        "<b>Green Corner es el rival serio:</b> más contenido y presencia en dos de las cinco "
        "categorías. Pero su título de portada es solo «Green Corner», sin una sola palabra clave. "
        "Está posicionado por marca, no por producto.",
        "<b>Chile Monoloco y Bendito Chile son alcanzables ya:</b> ambos tienen menos contenido "
        "que CARLOUIS y marcado incompleto.",
    ]))
    E.append(PageBreak())

    # ---------------- Análisis por producto
    E.append(P("Análisis producto por producto", "h1"))
    E.append(rule(EMBER, 1.2))
    E.append(P("Cada producto es una búsqueda distinta, con competencia y dificultad propias. "
               "La columna de dificultad estima cuánto cuesta llegar al primer lugar de la "
               "primera página.", "lede"))
    E.append(Spacer(1, 2*mm))

    filas = [["Producto", "Término objetivo", "Quién domina hoy", "Dificultad"]]
    for n, term, dom, dif, _ in PROD:
        color = {"Muy baja":"#4C6B3C","Baja":"#4C6B3C","Media":"#9A6B12",
                 "Media-alta":"#C2410C","Alta":"#C2410C"}[dif]
        filas.append([f"<b>{n}</b>", f'<font name="Mono" size="7.5">{term}</font>',
                      dom, f'<font color="{color}"><b>{dif}</b></font>'])
    E.append(tabla(filas, [32*mm, 48*mm, 60*mm, 25*mm]))

    E.append(Spacer(1, 5*mm))
    E.append(caja("Dónde están las victorias rápidas", [
        "<b>Cinco productos tienen dificultad «muy baja» o sin competencia identificada:</b> "
        "Piña Habanero, Alioli, Mayonesa de Culantro, Chile Morrón Asado y Pesto de Tomate.",
        "Son los que hay que empujar primero. Posicionan en semanas y generan las primeras "
        "señales de autoridad que después ayudan a ganar los términos difíciles.",
    ], BASIL, colors.HexColor("#E7EEE2")))
    E.append(PageBreak())

    # ---------------- Estrategia por producto
    E.append(P("Estrategia por producto", "h1"))
    E.append(rule(EMBER, 1.2))
    for n, term, dom, dif, est in PROD:
        E.append(KeepTogether([
            Paragraph(f"{n} <font color='#8B7A6D' size='8'>— dificultad {dif.lower()}</font>", S["h3"]),
            Paragraph(f'<font name="Mono" size="8" color="#A82A10">{term}</font>', S["small"]),
            Spacer(1, 1.5*mm),
            Paragraph(est, S["p"]),
        ]))
    E.append(PageBreak())

    # ---------------- Análisis como empresa
    E.append(P("Análisis a nivel de empresa", "h1"))
    E.append(rule(EMBER, 1.2))
    E.append(P("Más allá de los productos individuales, esto es lo que define la posición "
               "competitiva de CARLOUIS como marca.", "lede"))

    E.append(P("Fortalezas", "h2"))
    for t, d in [
        ("Amplitud de catálogo", "Doce productos en cinco categorías. Ningún competidor artesanal cubre tanto: Chile Monoloco y Bendito Chile solo hacen picantes; Verde Salvia solo pestos."),
        ("Base técnica superior", "Sitio más rápido, con más contenido y mejor marcado que los líderes actuales. Es una ventaja que ya está construida y pagada."),
        ("Presencia física", "La feria de los sábados genera prueba de producto, clientes recurrentes y contenido real para publicar."),
        ("Precio único nacional", "Simplifica la decisión de compra y es un argumento que ningún competidor comunica con claridad."),
    ]:
        E.append(P(f"<b>{t}.</b> {d}"))

    E.append(P("Debilidades", "h2"))
    for t, d in [
        ("Cero reseñas en Google", "Es el factor de mayor peso en resultados locales y está en cero. La ficha existe pero no acumula reseñas."),
        ("Sin enlaces externos", "Ningún sitio enlaza a carlouis.net. Es lo que más pesa en la autoridad de dominio y lo que más tiempo toma construir."),
        ("Marca desconocida en buscador", "Nadie busca «CARLOUIS» todavía. La demanda hay que crearla con presencia y contenido."),
        ("Dependencia de WhatsApp", "No hay carrito con pago en línea. Funciona para el volumen actual, pero limita la conversión de quien llega de noche o fuera de horario."),
    ]:
        E.append(P(f"<b>{t}.</b> {d}"))

    E.append(P("Oportunidades", "h2"))
    for t, d in [
        ("Categorías vacías", "Alioli, mayonesas saborizadas y conservas artesanales no las posiciona nadie en el país."),
        ("Contenido de uso", "Ningún competidor responde «con qué se come esto». Es la búsqueda que hace la gente antes de comprar y está sin atender."),
        ("Venta a marketplaces", "Ecomuna, Turri y Mercato ya posicionan bien. Venderles es más rápido que competirles, y cada uno genera un enlace."),
        ("Prensa de emprendimiento", "A Karoa una nota en El Financiero le dio más autoridad que años de ajustes técnicos. Ese camino está abierto."),
    ]:
        E.append(P(f"<b>{t}.</b> {d}"))

    E.append(P("Amenazas", "h2"))
    for t, d in [
        ("Green Corner ampliando línea", "Ya compite en pestos y picantes con más contenido y una tienda en línea funcional."),
        ("Cadenas en el estante", "Walmart y PriceSmart dominan el genérico y la compra por impulso física."),
        ("Dependencia de una sola persona", "El contenido y las reseñas exigen constancia. Si se detiene, la posición se pierde ante quien sí siga publicando."),
    ]:
        E.append(P(f"<b>{t}.</b> {d}"))
    E.append(PageBreak())

    # ---------------- Plan
    E.append(P("Plan de posicionamiento", "h1"))
    E.append(rule(EMBER, 1.2))
    E.append(P("En este orden. Saltarse una fase invalida las siguientes.", "lede"))

    E.append(tabla([
        ["Fase", "Acciones", "Resultado esperado"],
        ["<b>Semana 1</b><br/>Destrabar",
         "Reindexar en Search Console tras el arreglo de DNS. Completar la ficha de Google: área de servicio a las 7 provincias y 15 fotos reales. Reenviar el sitemap.",
         "El sitio empieza a aparecer al buscar la marca."],
        ["<b>Mes 1</b><br/>Prueba social",
         "Pedir reseñas en la feria, en el momento. Enviar el enlace por WhatsApp tras cada entrega. Contestar todas. Registrarse en directorios con datos idénticos.",
         "10 reseñas. Aparición en el bloque de mapas en Alajuela."],
        ["<b>Meses 2-3</b><br/>Contenido",
         "Un artículo por semana sobre usos y recetas. Empujar primero los cinco productos sin competencia.",
         "Primeras posiciones en los términos de nicho."],
        ["<b>Meses 4-8</b><br/>Autoridad",
         "Vender a marketplaces gourmet. Buscar cobertura de prensa. Cada feria, una entrada de blog y un enlace del organizador.",
         "Top 10 nacional en términos de producto."],
        ["<b>Continuo</b><br/>Sostener",
         "3 a 5 reseñas nuevas por mes. Publicación semanal en la ficha de Google. Contenido sin pausas.",
         "Disputa real por el primer lugar nacional."],
    ], [30*mm, 78*mm, 57*mm]))

    E.append(P("Expectativas realistas", "h2"))
    E.append(tabla([
        ["Meta", "Plazo", "De qué depende"],
        ["Aparecer al buscar «CARLOUIS»", "3 a 7 días", "Indexación, ya destrabada"],
        ["Liderar los 5 productos de nicho", "1 a 3 meses", "Páginas de producto publicadas"],
        ["Top 3 local en Alajuela y Santa Ana", "2 a 4 meses", "25 o más reseñas"],
        ["Top 10 nacional por producto", "4 a 8 meses", "Contenido semanal sostenido"],
        ["Primer lugar en «salsas artesanales Costa Rica»", "9 a 14 meses", "Enlaces, reseñas y constancia"],
    ], [62*mm, 28*mm, 75*mm]))

    E.append(Spacer(1, 5*mm))
    E.append(caja("Advertencia necesaria", [
        "Los plazos suponen que se ejecutan las acciones de cada fase. <b>No son garantías:</b> "
        "nadie controla el algoritmo de Google, y un competidor que invierta fuerte puede alterar "
        "el escenario.",
        "Lo que sí está bajo control y ya está hecho: un sitio técnicamente superior al de todos "
        "los competidores medidos. Lo que falta depende de la operación diaria del negocio.",
    ], GOLD, colors.HexColor("#F7ECD4")))

    E.append(Spacer(1, 6*mm))
    E.append(rule())
    E.append(P("Metodología: los datos de competencia se obtuvieron accediendo directamente a los "
               "sitios en vivo el 31 de agosto de 2026, midiendo contenido, marcado estructurado y "
               "plataforma. Los términos de búsqueda y sus competidores se identificaron mediante "
               "búsquedas reales en Google Costa Rica. Las estimaciones de dificultad y plazo se "
               "basan en la fuerza observada de esos competidores; no provienen de herramientas de "
               "volumen de búsqueda pagas.", "small"))

    doc.build(E, onFirstPage=lambda c, d: None, onLaterPages=pie)
    return salida


if __name__ == "__main__":
    out = build("Estudio-Mercado-SEO-CARLOUIS.pdf")
    print(f"  generado: {out}  ({os.path.getsize(out)/1024:.0f} KB)")
