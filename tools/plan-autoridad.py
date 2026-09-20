# -*- coding: utf-8 -*-
"""Plan de autoridad: por qué el sitio todavía no aparece y qué sigue.

    python tools/plan-autoridad.py

Todo lo que dice este documento se verificó contra fuentes en vivo el 20 de
setiembre de 2026: el catálogo de PROCOMER, la fecha real de cada página en el
historial de git y las cabeceras del sitio en producción.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estudio_estilo import (S, P, LI, rule, tabla, caja, panel_cifras, cifra,
                            construir, EMBER, DEEP, INK, INK2, INK3, LINE,
                            PAPER2, BASIL, GOLD, CHILI, mm, Spacer, PageBreak,
                            colors, Paragraph, KeepTogether)

A = 170 * mm


def contenido():
    f = []

    # ---------------------------------------------------------- portada --
    f += [Spacer(1, 42 * mm),
          P("PLAN DE POSICIONAMIENTO", "eyebrow"),
          P("Por qué todavía<br/>no aparecen", "ct"),
          P("Diagnóstico con datos, y las seis acciones que siguen.<br/>"
            "CARLOUIS Gourmet &middot; 20 de setiembre de 2026", "cs"),
          Spacer(1, 14 * mm), rule(EMBER, 1.6), Spacer(1, 6 * mm),
          P("Verificado contra el catálogo de proveedores de PROCOMER, el historial de "
            "publicación del sitio y las cabeceras de producción, el 20 de setiembre de 2026.",
            "small"),
          PageBreak()]

    # ------------------------------------------------------- resumen ----
    f += [P("Lo que encontré", "h1"), rule(EMBER, 1.2),
          P("La pregunta era por qué en Search Console solo aparecen cuatro consultas, todas de "
            "marca. La respuesta tiene dos partes, y solo una es problema.", "lede")]

    f += [panel_cifras([
        ("20", "DIAS VISIBLE", "el DNS se arregló el 31 de agosto", EMBER),
        ("1-3", "DIAS DE EDAD", "de las páginas de lugar y proveedor", CHILI),
        ("0", "DIRECTORIOS", "CARLOUIS no está en ninguno", DEEP),
        ("32", "COMPETIDORES", "sí están en el catálogo de PROCOMER", BASIL),
    ]), Spacer(1, 5 * mm)]

    f += [P("Parte 1: el sitio es demasiado nuevo. Esto no es un problema.", "h2"),
          P("El dominio estuvo caído para Google hasta el 31 de agosto. Son <b>20 días</b> de "
            "visibilidad real. Y el contenido que debería rankear por producto es todavía más "
            "nuevo que eso:", "p")]

    f += [tabla([
        ["Página", "Publicada", "Edad hoy"],
        ["Fichas de producto (12)", "6 de setiembre", "14 días"],
        ["Mayoreo", "17 de setiembre", "3 días"],
        ["Páginas de provincia (7)", "19 de setiembre", "1 día"],
        ["Cantones del GAM (4)", "20 de setiembre", "horas"],
        ["Proveedor para cadenas", "20 de setiembre", "horas"],
    ], [72 * mm, 50 * mm, 48 * mm]), Spacer(1, 4 * mm)]

    f += [P("Una página de un día no rankea. Ninguna. Google necesita rastrearla, entenderla, "
            "compararla con las que ya rankean y probarla con tráfico real. Para un dominio sin "
            "historial eso toma entre <b>8 y 16 semanas</b>, no días.", "p"),
          P("Que aparezcan cuatro consultas de marca es exactamente la primera señal esperada. "
            "Significa que Google ya encontró el sitio y empezó a mostrarlo. Hace tres semanas no "
            "aparecía nada.", "p")]

    f += [caja("Lo que esto quiere decir en la práctica",
               ["No hay nada roto. Revisé robots.txt, las etiquetas canónicas, la redirección del "
                "dominio sin www y las cabeceras de producción: todo correcto, nada bloquea a Google.",
                "Escribir más páginas esta semana no acelera nada. Las que ya existen todavía no "
                "han tenido oportunidad de competir."], BASIL),
          PageBreak()]

    # ---------------------------------------------------- el problema ---
    f += [P("Parte 2: el problema real", "h1"), rule(EMBER, 1.2),
          P("CARLOUIS no existe en ningún otro lugar del internet costarricense.", "lede"),
          P("Google no decide solo con el contenido de un sitio. También mira quién más habla de "
            "ese negocio: directorios, cámaras, catálogos, prensa, otros sitios que lo enlacen. A "
            "eso se le llama autoridad, y hoy CARLOUIS tiene cero.", "p")]

    f += [P("El hallazgo que lo explica todo", "h2"),
          P("PROCOMER —la agencia de comercio exterior del Estado— mantiene un catálogo público de "
            "proveedores costarricenses. En la categoría <b>salsas y aderezos</b> hay "
            "<b>32 empresas listadas</b>. CARLOUIS no es una de ellas.", "p"),
          P("Entre las que sí están:", "p"),
          LI("<b>Le Piquant La Selva</b> — su sitio web tiene 17 palabras. Lo medí."),
          LI("<b>Chile Monoloco</b> — 493 palabras, un solo tipo de dato estructurado."),
          LI("Grupo Agroindustrial El Ángel, Capitán Picante, Patica Products, Calipso, Delisur."),
          Spacer(1, 3 * mm),
          P("CARLOUIS tiene hoy <b>44 páginas</b> y datos estructurados en catorce formatos. Es, "
            "por lejos, el mejor sitio de la categoría. Y aun así pierde contra una página de 17 "
            "palabras, porque esa página está respaldada por una institución y la nuestra no está "
            "respaldada por nadie.", "p")]

    f += [caja("El resumen honesto",
               ["El sitio ya no es el cuello de botella. La autoridad sí.",
                "Todo lo que sigue en este documento es trabajo fuera del sitio. Es gratis casi "
                "todo, pero no lo puedo hacer yo: requiere la cédula jurídica, los datos de la "
                "empresa y en varios casos la firma del dueño."], EMBER),
          PageBreak()]

    # ------------------------------------------------------- acciones ---
    f += [P("Las seis acciones, en orden", "h1"), rule(EMBER, 1.2),
          P("Ordenadas por impacto sobre esfuerzo. La 1 y la 2 valen más que las otras cuatro "
            "juntas.", "lede")]

    acciones = [
        ("1", "Catálogo de proveedores de PROCOMER", "Gratis", "Alto",
         "suppliers.investincr.com",
         "Es donde están los 32 competidores. Es un dominio del Estado, lo que le da a un enlace "
         "desde ahí mucho más peso que a cualquier otro. Y es exactamente donde un comprador de "
         "Automercado o de una cadena busca proveedor nacional. Se solicita escribiendo a "
         "info@procomer.com o al 2505-4700."),

        ("2", "Perfil de Google Business al 100%", "Gratis", "Alto",
         "business.google.com",
         "El perfil ya existe. Falta llenarlo completo: los 12 productos cargados uno por uno con "
         "foto y precio, la categoría correcta, el área de servicio, horarios de feria y "
         "publicaciones cada semana. Para búsquedas locales —que es donde está la venta al "
         "detalle— este perfil pesa más que el sitio web entero."),

        ("3", "Reseñas de Google", "Gratis", "Alto",
         "g.page/r/CTFj8J32N0aUEBM/review",
         "El enlace ya lo tienen. Cada cliente de feria que deje una reseña mueve el perfil en el "
         "mapa local. Es la acción más barata y más subestimada: veinte reseñas reales cambian la "
         "posición en el paquete local de Google más que cualquier cosa que yo escriba."),

        ("4", "Registro PYME del MEIC", "Gratis", "Medio",
         "meic.go.cr",
         "El registro de empresas PYME y el registro de emprendedores son gratuitos y voluntarios. "
         "Dan presencia en listados oficiales, y además abren acceso a programas de apoyo y al "
         "sello Costa Rica Artesanal."),

        ("5", "Jinca Market", "Por confirmar", "Medio",
         "jincamarket.com",
         "Plataforma costarricense que vende producto de emprendimientos pequeños y tiene "
         "categoría de aderezos, salsas y conservas. Es venta y es enlace al mismo tiempo. Hay que "
         "preguntarles condiciones y comisión."),

        ("6", "CACIA e incubadora Pasión por el Sabor", "Por confirmar", "Medio",
         "cacia.org",
         "La Cámara Costarricense de la Industria Alimentaria tiene una incubadora para "
         "emprendimientos de salsas y aderezos, con capital semilla. Ser miembro de la cámara da "
         "presencia, contactos de industria y credibilidad ante un comprador de cadena."),
    ]

    for n, titulo, costo, impacto, url, texto in acciones:
        bloque = [
            Paragraph("%s. %s" % (n, titulo), S["h3"]),
            Paragraph("%s &middot; Impacto %s &middot; %s" % (costo, impacto.lower(), url), S["small"]),
            Spacer(1, 1.5 * mm),
            Paragraph(texto, S["p"]),
        ]
        f.append(KeepTogether(bloque))

    f += [PageBreak()]

    # --------------------------------------------------- lo bloqueante --
    f += [P("Lo que está bloqueando el mayoreo", "h1"), rule(EMBER, 1.2),
          P("Esto es aparte del SEO, y es más urgente que el SEO.", "lede")]

    f += [P("La página para compradores de cadena ya está publicada. Pero ninguna cadena codifica "
            "un proveedor sin dos papeles, y yo no sé si CARLOUIS los tiene porque nunca me lo "
            "confirmaron:", "p"),
          Spacer(1, 2 * mm)]

    f += [tabla([
        ["Requisito", "Quién lo emite", "Detalle importante"],
        ["Registro sanitario", "Ministerio de Salud",
         "Se otorga <b>por producto</b>, no por empresa. Doce productos son doce trámites."],
        ["Código de barras", "GS1 Costa Rica",
         "Necesario para codificar cada presentación en el sistema de la cadena."],
        ["Ficha técnica", "La empresa",
         "Ingredientes, alérgenos, peso neto, vida útil y almacenamiento."],
        ["Cédula jurídica y CCSS", "Registro Nacional / CCSS",
         "Al día, para poder facturar y recibir orden de compra."],
    ], [38 * mm, 38 * mm, 94 * mm]), Spacer(1, 4 * mm)]

    f += [caja("Por qué la página web no afirma tenerlos",
               ["Un comprador verifica el registro sanitario en la primera reunión. Si la web dice "
                "una cosa y el papel dice otra, se acabó la relación y no hay segunda oportunidad.",
                "La página dice hoy que se confirma el estado por escrito y por producto. En cuanto "
                "me confirmen cuáles están al día, lo cambio el mismo día y el tono de esa página "
                "pasa de prudente a contundente."], CHILI),
          Spacer(1, 4 * mm),
          P("Si los papeles no están, esa es la tarea. Ninguna página web mete un producto a "
            "Automercado sin registro sanitario, y ese trámite va antes que cualquier cosa que yo "
            "pueda escribir.", "p"),
          PageBreak()]

    # ------------------------------------------------------ calendario --
    f += [P("Qué esperar y cuándo", "h1"), rule(EMBER, 1.2),
          P("Con las acciones 1 a 4 hechas en las próximas dos semanas.", "lede")]

    f += [tabla([
        ["Plazo", "Qué debería verse en Search Console"],
        ["Semanas 1-2", "Las 44 páginas indexadas. Las consultas suben de 4 a unas 20-40, todavía "
                        "con pocos clics. El objetivo de esta etapa es cobertura, no venta."],
        ["Semanas 3-6", "Aparecen consultas de producto y de lugar: 'chimichurri argentino', "
                        "'salsas artesanales Heredia'. Posiciones de página 2 a 4. Primeros clics "
                        "que no son de marca."],
        ["Semanas 7-12", "Las páginas de lugar y las guías empiezan a entrar a página 1 en "
                         "búsquedas de cola larga, que son las que traen comprador decidido."],
        ["Mes 4 en adelante", "Competencia real por los términos de producto, si para entonces hay "
                              "reseñas y el enlace de PROCOMER está activo."],
    ], [32 * mm, 138 * mm]), Spacer(1, 5 * mm)]

    f += [P("Cómo medirlo sin engañarse", "h2"),
          P("En Search Console, la métrica que importa en esta etapa <b>no es el tráfico</b>: es el "
            "número de consultas distintas. Si esta semana son 4 y en tres semanas son 30, el "
            "sistema está funcionando aunque los clics sigan bajos. Los clics llegan después, "
            "cuando las posiciones suben de página 3 a página 1.", "p"),
          P("La segunda métrica es la posición promedio por consulta. Pasar de posición 40 a "
            "posición 15 no da ni un clic, pero es exactamente la mitad del camino.", "p")]

    f += [Spacer(1, 6 * mm), rule(EMBER, 1.2),
          P("Resumen en una línea", "h3"),
          P("El sitio ya está hecho y está bien hecho. Lo que falta es que CARLOUIS exista fuera "
            "del sitio, y eso empieza con una llamada a PROCOMER al 2505-4700 y con pedirle "
            "reseñas a los clientes de la feria del sábado.", "p")]

    return f


if __name__ == "__main__":
    salida = "Plan-Posicionamiento-CARLOUIS.pdf"
    construir(salida, contenido(), "Plan de posicionamiento — CARLOUIS Gourmet")
    print("  %s  %.0f KB" % (salida, os.path.getsize(salida) / 1024))
