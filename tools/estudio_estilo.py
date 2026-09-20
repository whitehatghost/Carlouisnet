# -*- coding: utf-8 -*-
"""Estilo compartido de los PDF de CARLOUIS.

Se extrajo de estudio-completo.py para que cualquier documento nuevo salga con
la misma cara: mismas fuentes, misma paleta, mismas tablas y cajas. Si se
cambia acá, cambian todos los documentos que lo importen.
"""
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
    pdfmetrics.registerFont(TTFont(n, "%s/%s" % (F, a)))

EMBER = colors.HexColor("#A82A10"); DEEP = colors.HexColor("#6B1608")
INK = colors.HexColor("#241A15");   INK2 = colors.HexColor("#5A4A40")
INK3 = colors.HexColor("#8B7A6D");  LINE = colors.HexColor("#E3D9CC")
PAPER2 = colors.HexColor("#F4EDE2"); BASIL = colors.HexColor("#4C6B3C")
GOLD = colors.HexColor("#9A6B12");  CHILI = colors.HexColor("#C2410C")

S = {}
S["h1"] = ParagraphStyle("h1", fontName="GeoB", fontSize=21, leading=25, textColor=DEEP, spaceAfter=4)
S["h2"] = ParagraphStyle("h2", fontName="GeoB", fontSize=13.5, leading=17, textColor=DEEP,
                         spaceBefore=15, spaceAfter=6)
S["h3"] = ParagraphStyle("h3", fontName="CalB", fontSize=11, leading=14, textColor=EMBER,
                         spaceBefore=9, spaceAfter=3)
S["p"] = ParagraphStyle("p", fontName="Cal", fontSize=9.8, leading=14, textColor=INK, spaceAfter=6)
S["li"] = ParagraphStyle("li", fontName="Cal", fontSize=9.8, leading=14, textColor=INK,
                         spaceAfter=3, leftIndent=10, bulletIndent=2)
S["small"] = ParagraphStyle("small", fontName="Cal", fontSize=8.3, leading=11.5, textColor=INK3)
S["lede"] = ParagraphStyle("lede", fontName="Cal", fontSize=11, leading=16, textColor=INK2, spaceAfter=8)
S["eyebrow"] = ParagraphStyle("eb", fontName="Mono", fontSize=7.2, leading=10, textColor=EMBER, spaceAfter=3)
S["cell"] = ParagraphStyle("cell", fontName="Cal", fontSize=8.2, leading=11, textColor=INK)
S["cellb"] = ParagraphStyle("cellb", fontName="CalB", fontSize=8.2, leading=11, textColor=INK)
S["th"] = ParagraphStyle("th", fontName="CalB", fontSize=7.5, leading=9.5, textColor=colors.white)
S["ct"] = ParagraphStyle("ct", fontName="GeoB", fontSize=30, leading=34, textColor=DEEP, spaceAfter=8)
S["cs"] = ParagraphStyle("cs", fontName="Cal", fontSize=12.5, leading=18, textColor=INK2)


def P(t, s="p"):
    return Paragraph(t, S[s])


def LI(t):
    return Paragraph(t, S["li"], bulletText="\u2022")


def rule(c=LINE, w=0.6):
    return HRFlowable(width="100%", thickness=w, color=c, spaceBefore=3, spaceAfter=7)


def tabla(datos, anchos, zebra=True, fuente=None):
    est = fuente or "cell"
    filas = [[Paragraph(str(c), S["th" if i == 0 else est]) for c in fila]
             for i, fila in enumerate(datos)]
    t = Table(filas, colWidths=anchos, repeatRows=1)
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -2), 0.35, LINE),
            ("BOX", (0, 0), (-1, -1), 0.55, LINE),
            ("BACKGROUND", (0, 0), (-1, 0), DEEP)]
    if zebra:
        for i in range(1, len(datos)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), PAPER2))
    t.setStyle(TableStyle(cmds))
    return t


def caja(titulo, cuerpo, color=EMBER, fondo=PAPER2):
    inner = [Paragraph(titulo, ParagraphStyle("bt", fontName="CalB", fontSize=9.8, leading=13,
                                              textColor=color, spaceAfter=3))]
    for c in cuerpo:
        inner.append(Paragraph(c, ParagraphStyle("bc", fontName="Cal", fontSize=9.2, leading=12.8,
                                                 textColor=INK, spaceAfter=3)))
    t = Table([[inner]], colWidths=[166 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fondo),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.5, color),
                           ("TOPPADDING", (0, 0), (-1, -1), 7),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 9)]))
    return t


def cifra(valor, etiqueta, nota, color=INK):
    return [Paragraph('<font color="%s">%s</font>' % (color, valor),
                      ParagraphStyle("cv", fontName="GeoB", fontSize=17, leading=20, alignment=1)),
            Paragraph(etiqueta, ParagraphStyle("ce", fontName="Mono", fontSize=6.5, leading=9,
                                               textColor=INK3, alignment=1)),
            Paragraph(nota, ParagraphStyle("cn", fontName="Cal", fontSize=7.5, leading=10,
                                           textColor=INK3, alignment=1))]


def panel_cifras(items):
    t = Table([[cifra(*i) for i in items]], colWidths=[166 * mm / len(items)] * len(items))
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOX", (0, 0), (-1, -1), 0.55, LINE),
                           ("INNERGRID", (0, 0), (-1, -1), 0.55, LINE),
                           ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def construir(salida, flowables, titulo, pie_txt=None):
    """Arma el PDF. `pie_txt` es la línea del pie; por defecto usa el título."""
    texto_pie = pie_txt or titulo

    def pie(canvas, doc):
        canvas.saveState()
        canvas.setFont("Cal", 7.2)
        canvas.setFillColor(INK3)
        canvas.drawString(22 * mm, 12 * mm, texto_pie)
        canvas.drawRightString(188 * mm, 12 * mm, str(doc.page))
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(22 * mm, 16 * mm, 188 * mm, 16 * mm)
        canvas.restoreState()

    doc = SimpleDocTemplate(salida, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=20 * mm, bottomMargin=22 * mm,
                            title=titulo, author="CARLOUIS Gourmet")
    doc.build(flowables, onFirstPage=pie, onLaterPages=pie)
    return salida
