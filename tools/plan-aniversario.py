# -*- coding: utf-8 -*-
"""Plan completo de los 6 años, para que Luis lo lea y decida.

    python tools/plan-aniversario.py

Va TODO: las opciones de caja con precios reales, el texto exacto de la
página, los posts de redes palabra por palabra, el de Google Business, el
calendario y lo que hace falta de ellos. Nada de resúmenes: la idea es que
pueda aprobar o corregir sin sorpresas después.

Los precios salen de tools/productos.py, no se escriben a mano, para que no
haya forma de equivocarse en una suma.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS
from estudio_estilo import (S, P, LI, rule, tabla, caja, panel_cifras, construir,
                            EMBER, DEEP, INK, INK2, INK3, LINE, PAPER2, BASIL,
                            GOLD, CHILI, mm, Spacer, PageBreak, KeepTogether, Paragraph)

POR = {p["slug"]: p for p in PRODUCTOS}


def crc(n):
    return "₡" + "{:,}".format(int(n)).replace(",", ".")


def precio(slug):
    return int(POR[slug]["precio_num"])


def nombre(slug):
    return POR[slug]["nombre"]


# --------------------------------------------------------------- las cajas --
# (clave, nombre, para quién, productos, precio de venta, por qué)
CAJAS = [
    ("A", "La Completa", "6 productos · la del aniversario",
     ["salsa-habanero-fire", "salsa-pina-habanero", "chimichurri-argentino",
      "pesto-de-albahaca", "alioli", "tomates-deshidratados"],
     24000,
     "Seis productos por seis años. La historia se cuenta sola y no hay que "
     "explicar nada. Trae uno de cada tipo, así que quien no conoce CARLOUIS lo "
     "prueba todo de una sola vez."),

    ("B", "Sin Picante", "6 productos · para regalar sin riesgo",
     ["pesto-de-albahaca", "pesto-de-tomate", "alioli", "mayonesa-de-culantro",
      "tomates-deshidratados", "chile-morron-asado"],
     26000,
     "Ninguno pica. Es la caja para regalar cuando uno no sabe si a la persona le "
     "gusta el picante, que es la duda que más frena una compra de regalo."),

    ("C", "La de Parrilla", "5 productos · la más barata para entrar",
     ["chimichurri-argentino", "salsa-habanero-fire", "alioli", "chile-morron-asado",
      "mayonesa-de-chipotle"],
     19000,
     "Menos plata de entrada, así que la compra más gente. Sirve para el que "
     "nunca ha comprado y no quiere arriesgar ₡24.000 de una."),

    ("D", "Los Doce", "toda la línea · la grande",
     [p["slug"] for p in PRODUCTOS],
     49000,
     "Todo el catálogo. Para el cliente que ya compra seguido y para regalo de "
     "empresa. Son pocas ventas pero cada una vale lo que ocho frascos sueltos."),
]


def bloque_caja(clave, nom, sub, slugs, venta, porque):
    suma = sum(precio(s) for s in slugs)
    ahorro = suma - venta
    filas = [["Producto", "Precio suelto"]]
    for s in slugs:
        filas.append([nombre(s), crc(precio(s))])
    filas.append(["<b>Suman por aparte</b>", "<b>" + crc(suma) + "</b>"])
    filas.append(["<b>Precio de la caja</b>", "<b>" + crc(venta) + "</b>"])
    filas.append(["<b>El cliente ahorra</b>",
                  "<b>" + crc(ahorro) + " (" + str(round(ahorro / suma * 100)) + "%)</b>"])

    return KeepTogether([
        Paragraph("Opción " + clave + ": " + nom, S["h2"]),
        Paragraph(sub, S["small"]),
        Spacer(1, 2 * mm),
        Paragraph(porque, S["p"]),
        Spacer(1, 2 * mm),
        tabla(filas, [118 * mm, 52 * mm]),
        Spacer(1, 6 * mm),
    ])


def post(titulo, cuando, texto, nota=None):
    inner = [Paragraph(titulo, S["h3"]), Paragraph(cuando, S["small"]), Spacer(1, 2 * mm)]
    for linea in texto.split("\n"):
        inner.append(Paragraph(linea, S["p"]) if linea.strip() else Spacer(1, 2 * mm))
    if nota:
        inner.append(Paragraph("<i>" + nota + "</i>", S["small"]))
    inner.append(Spacer(1, 4 * mm))
    return KeepTogether(inner)


def contenido():
    f = []

    # ------------------------------------------------------------ portada --
    f += [Spacer(1, 45 * mm),
          P("PLAN COMPLETO · PENDIENTE DE SU APROBACIÓN", "eyebrow"),
          P("6 años<br/>de CARLOUIS", "ct"),
          P("Todo lo que haríamos para el 29 de setiembre:<br/>"
            "la caja, la página, las redes y el calendario.", "cs"),
          Spacer(1, 12 * mm), rule(EMBER, 1.6), Spacer(1, 5 * mm),
          P("Para Luis Rodríguez y Carlina. Nada de esto está publicado ni se va a "
            "publicar hasta que ustedes den el visto bueno. Si algo no les gusta, se cambia "
            "o se quita.", "small"),
          PageBreak()]

    # ------------------------------------------------------------ la idea --
    f += [P("La idea, en corto", "h1"), rule(EMBER, 1.2),
          P("Seis años es la clase de cosa que la gente celebra tirando un descuento a "
            "todo. La propuesta es hacer lo contrario, por una razón de plata.", "lede")]

    f += [caja("Por qué no un descuento general",
               ["Un 15% en todo el catálogo también se lo lleva el cliente que ya "
                "iba a comprar de todas formas. Esa venta iba a pasar igual, y usted acaba de "
                "regalar el 15%.",
                "Una caja, en cambio, solo la compra quien decide gastar más de lo que "
                "pensaba. Alguien que iba por un frasco de ₡5.000 termina llevando "
                "₡24.000, y de paso prueba cuatro cosas que nunca había probado.",
                "Eso último es lo que más vale: el mes entrante vuelve a pedir el "
                "que le gustó, y ese ya es cliente de dos productos, no de uno."], BASIL),
          Spacer(1, 5 * mm)]

    f += [P("Lo que hay hoy para armarla", "h2"),
          P("Doce productos, cuatro categorías de tres cada una. Estos son los precios "
            "que están hoy en la página:", "p")]

    filas = [["Producto", "Precio", "Categoría", "Pica"]]
    for p in PRODUCTOS:
        cat = {"picantes": "Picantes", "pestos": "Pestos", "cremas": "Cremas",
               "cremas picantes": "Cremas", "conservas": "Conservas"}.get(
                   p.get("cat", ""), p.get("cat", ""))
        n = p.get("nivel", 0)
        filas.append([p["nombre"], crc(int(p["precio_num"])), cat,
                      ("nivel " + str(n)) if n else "no"])
    filas.append(["<b>Los doce juntos</b>", "<b>" + crc(sum(int(p["precio_num"])
                 for p in PRODUCTOS)) + "</b>", "", ""])
    f += [tabla(filas, [62 * mm, 30 * mm, 42 * mm, 36 * mm]), Spacer(1, 4 * mm)]

    f += [caja("Algo que encontré de paso, y conviene arreglar",
               ["La <b>Salsa de Chile Dulce</b> está clasificada como “Picante” en "
                "la página, pero es nivel 1 y prácticamente no pica.",
                "Quien busca algo suave la descarta al verla en esa categoría, y quien "
                "busca picante se decepciona. Está perdiendo venta por los dos lados. "
                "Con que me digan, la muevo a Conservas o a una categoría propia."], CHILI),
          PageBreak()]

    # ---------------------------------------------------------- las cajas --
    f += [P("Cuatro formas de armar la caja", "h1"), rule(EMBER, 1.2),
          P("Escojan una. Si quieren dos, que sean la A y la B: “con picante” y "
            "“sin picante” se explica en una línea. Tres o más ya confunde "
            "y la gente no decide.", "lede")]

    for c in CAJAS:
        f.append(bloque_caja(*c))

    f += [PageBreak()]

    # ------------------------------------------------- cómo escoger --
    f += [P("Cómo escoger, si me preguntan", "h1"), rule(EMBER, 1.2)]

    f += [P("Mi recomendación: la A", "h2"),
          P("Seis productos por seis años es una idea que se explica sola, y esa caja "
            "trae de las cuatro categorías. Para alguien que nunca ha comprado, es la forma "
            "de conocer toda la línea de una.", "p"),
          P("Si quieren agregar una segunda, que sea la <b>B, Sin Picante</b>. La duda de "
            "“¿y si a esta persona no le gusta el picante?” es lo que más "
            "frena una compra de regalo, y esa caja la resuelve.", "p")]

    f += [P("Tres cosas que sí o sí hay que revisar antes", "h2"),
          LI("<b>¿Deja margen?</b> Los precios de venta que puse —₡24.000, "
             "₡26.000, ₡19.000, ₡49.000— los saqué yo buscando que el "
             "descuento diera parecido en todas, como 21 o 22%. Ustedes saben el costo real. "
             "Si no da, se sube el precio y ya."),
          LI("<b>¿Alcanza la producción?</b> No metan en la caja el producto que se "
             "les acaba primero. Si el chimichurri vuela y apenas dan abasto, sacarlo de la "
             "caja y meter otro. Quedarse sin poder cumplir un pedido hace más daño "
             "que no haber hecho la promoción."),
          LI("<b>¿Cuántas cajas?</b> Yo puse 30 como ejemplo. Debería ser lo que "
             "de verdad pueden producir esa semana <i>sin</i> dejar sin inventario los pedidos "
             "normales. Si son 15, ponemos 15: un número pequeño y real funciona "
             "mejor que uno grande e inventado."),
          Spacer(1, 3 * mm)]

    f += [caja("Un consejo que va contra lo que uno pensaría",
               ["No pongan en la caja el producto que más venden.",
                "Ese ya se vende solo, a precio completo. Meterlo con descuento es regalarle "
                "plata a alguien que iba a pagarlo entero.",
                "La caja sirve para que prueben lo que <b>no</b> se está moviendo. Si hay "
                "un producto bueno que la gente no se atreve a comprar porque no sabe a qué "
                "sabe, ese es el que tiene que ir en la caja."], EMBER),
          PageBreak()]

    # ---------------------------------------------------------- la página --
    f += [P("1. La página del sitio", "h1"), rule(EMBER, 1.2),
          P("Ya está armada y probada, esperando el visto bueno. Iría en "
            "<b>carlouis.net/aniversario.html</b>", "lede"),
          P("Se llama “aniversario” y no “6-anos” a propósito: el "
            "año que viene se actualiza el contenido y la página conserva lo que haya "
            "ganado en Google. Una dirección nueva cada año empieza de cero.", "p")]

    f += [P("El título y la entrada", "h2"),
          P("<b>Seis años haciéndolas a mano</b>", "p"),
          P("CARLOUIS cumple 6 años. Para celebrarlo armamos una caja con seis productos, "
            "de las cuatro categorías, a un precio que no vamos a repetir.", "p")]

    f += [P("El texto de la historia", "h2"),
          P("Seis años es mucho tiempo para un negocio de comida hecho a mano. La "
            "mayoría no llega. Producir en lotes pequeños es más caro, más "
            "lento y más incómodo que mandar a maquilar, y cada año aparece la "
            "tentación de hacerlo más fácil: meterle un preservante para que "
            "aguante meses en bodega, un espesante para rendir más, un colorante para que "
            "se vea pareja.", "p"),
          P("CARLOUIS no hizo nada de eso, y esa es toda la historia. Las mismas manos, la misma "
            "cocina en Alajuela, los mismos lotes chiquitos. Ninguna de las doce recetas lleva "
            "colorantes ni preservantes artificiales, y por eso hay que refrigerar después "
            "de abrir y por eso cuando se acaba un lote hay que esperar el siguiente. Es la "
            "parte incómoda de hacerlo bien.", "p"),
          P("En estos seis años la línea pasó de unas pocas salsas a doce "
            "productos. Se sumaron ferias —la de los sábados en Plaza Real Alajuela es "
            "la de siempre— y hoy se envía a las siete provincias, al mismo precio en "
            "todo el país.", "p"),
          P("Lo que no cambió: quien cocina es quien contesta el WhatsApp. No hay call "
            "center ni distribuidor en el medio. Si algo sale mal, lo sabe la persona que lo "
            "hizo.", "p")]

    f += [caja("Esto lo escribí yo y me falta lo principal",
               ["Todo lo de arriba sale de lo que se puede comprobar en la propia página. "
                "No inventé nada, pero tampoco sé lo que de verdad importa.",
                "¿Cuál fue la primera receta? ¿Dónde vendieron el primer "
                "frasco? ¿En qué momento estuvieron a punto de dejarlo y por qué "
                "siguieron? Eso vale más que las cuatro párrafos míos juntos, y "
                "es lo que la gente comparte.",
                "Mándenmelo por WhatsApp aunque sea hablado y yo lo acomodo."], CHILI),
          PageBreak()]

    # ------------------------------------------------------------- redes --
    f += [P("2. Instagram y Facebook", "h1"), rule(EMBER, 1.2),
          P("Cinco publicaciones. El mismo texto sirve para las dos redes. Listas para copiar "
            "y pegar, pero cámbienlas para que suenen a ustedes.", "lede")]

    f += [post("Viernes 26 — el aviso",
               "Foto: un frasco de cerca, con la etiqueta a la vista.",
               "El lunes 29 CARLOUIS cumple 6 años.\n"
               "\n"
               "Seis años cocinando en lotes pequeños, en la misma cocina de "
               "Alajuela, sin meterle preservantes ni colorantes a ninguna receta.\n"
               "\n"
               "Estamos preparando algo para celebrarlo. Les contamos el lunes.\n"
               "\n"
               "#CARLOUIS #7años #hechoencostarica #salsasartesanales #alajuela")]

    f += [post("Domingo 28 — la víspera",
               "Foto: la cocina, las manos trabajando, un lote en proceso.",
               "Mañana cumplimos 6 años.\n"
               "\n"
               "En estos años pasamos de unas pocas salsas a doce productos. Lo que no "
               "cambió: quien cocina es quien les contesta el WhatsApp.\n"
               "\n"
               "Mañana les mostramos con qué lo celebramos. Son pocas.")]

    f += [post("Lunes 29 — el anuncio principal",
               "Foto: los seis frascos juntos, ordenados. Es LA foto de la campaña.",
               "6 años de CARLOUIS\n"
               "\n"
               "Para celebrarlo armamos la Caja 6 Años: de las cuatro categorías, los "
               "seis juntos.\n"
               "\n"
               "Habanero Fire · Piña Habanero · Chimichurri · Pesto de "
               "Albahaca · Alioli · Tomates Deshidratados · Chile Morrón "
               "Asado\n"
               "\n"
               "Por aparte suman ₡31.000. Esta semana, ₡24.000.\n"
               "\n"
               "Solo 30 cajas, hasta el domingo 5. Envío incluido a todo el país.\n"
               "\n"
               "Escribinos al 8825 2608.",
               "En la bio de Instagram poner el enlace carlouis.net/aniversario.html")]

    f += [post("Martes 30 — el pedido de reseñas",
               "Foto: el puesto en la feria, o un cliente (con su permiso).",
               "Ayer cumplimos 6 años y nos escribieron un montón. Gracias de "
               "verdad.\n"
               "\n"
               "Les queremos pedir un favor que no cuesta plata: si alguna vez nos compraron, "
               "escriban una reseña en Google. Toma menos de un minuto.\n"
               "\n"
               "Para un negocio chiquito como el nuestro eso vale más que cualquier "
               "publicidad que podamos pagar. Es lo que hace que alguien que busca "
               "“salsas artesanales” en Costa Rica nos encuentre.\n"
               "\n"
               "El enlace está en la bio.",
               "Enlace de reseñas: g.page/r/CTFj8J32N0aUEBM/review")]

    f += [post("Jueves 2 o viernes 3 — el recordatorio",
               "Mejor como historia que como publicación del feed.",
               "Quedan pocas Cajas 6 Años.\n"
               "\n"
               "Seis productos por ₡24.000 en vez de ₡31.000, hasta el domingo o "
               "hasta que se acaben.\n"
               "\n"
               "8825 2608",
               "Solo si de verdad quedan pocas. Si sobran veinte y dicen “quedan "
               "pocas”, se nota, y eso quema la confianza que costó seis años.")]

    f += [PageBreak()]

    # --------------------------------------------------- google business --
    f += [P("3. El perfil de Google", "h1"), rule(EMBER, 1.2),
          P("Esta es la parte que más vende y la que menos se usa. Una publicación en "
            "el perfil de Google Business sale en el mapa y cuando alguien busca la marca, y "
            "queda visible una semana.", "lede")]

    f += [P("El texto para el perfil", "h3"),
          P("<b>6 años · Caja Aniversario</b>", "p"),
          P("CARLOUIS cumple 6 años haciendo salsas artesanales en Alajuela. Para "
            "celebrarlo armamos la Caja 6 Años: seis productos, uno de cada "
            "categoría, por ₡24.000 en vez de ₡31.000.", "p"),
          P("Solo 30 cajas, del 29 de setiembre al 5 de octubre. Envío incluido a todo el "
            "país. Pedidos al 8825 2608.", "p"),
          Spacer(1, 2 * mm),
          P("Se pone como <b>Oferta</b>, no como novedad: la oferta muestra las fechas y un "
            "botón. Yo les paso el paso a paso cuando lo aprueben.", "small")]

    f += [Spacer(1, 4 * mm),
          P("4. La entrada de blog", "h2"),
          P("Durante la semana, una entrada más larga que la página, con la historia "
            "completa y las fotos viejas que tengan. Esa es la que puede seguir trayendo gente "
            "meses después, cuando la promoción ya terminó.", "p"),
          P("Para escribirla bien necesito lo que pedí arriba: cómo empezó de "
            "verdad. Sin eso me queda genérica y no vale la pena.", "p")]

    f += [Spacer(1, 4 * mm), rule(LINE),
          P("5. Las reseñas — lo más importante de todo", "h2"),
          P("Se los he venido diciendo y lo repito porque es la única parte de este plan "
            "que cambia las cosas de verdad a largo plazo.", "p")]

    f += [panel_cifras([
        ("52", "PÁGINAS", "que tiene el sitio hoy", INK),
        ("4", "BÚSQUEDAS", "en Google en un mes", CHILI),
        ("32", "COMPETIDORES", "en el catálogo de PROCOMER", DEEP),
        ("0", "DE ELLOS", "es CARLOUIS", EMBER),
    ]), Spacer(1, 4 * mm)]

    f += [P("Al sitio no le falta contenido, le falta que alguien más hable de ustedes. "
            "Las reseñas son la forma más rápida y barata de conseguirlo, y un "
            "aniversario es la única excusa del año para pedirlas sin que se sienta "
            "raro.", "p"),
          P("Veinte reseñas reales mueven más el mapa de Google que veinte "
            "páginas nuevas que yo escriba.", "p"),
          PageBreak()]

    # ------------------------------------------------------- calendario --
    f += [P("El calendario, día por día", "h1"), rule(EMBER, 1.2)]

    f += [tabla([
        ["Día", "Qué pasa", "Quién"],
        ["Hoy", "Luis decide la caja, el precio y cuántas son.", "Luis"],
        ["Apenas decidan", "Publico la página y le aviso a Google para que la indexe.", "Yo"],
        ["Viernes 26", "Publicación de aviso en Instagram y Facebook.", "Ustedes"],
        ["Sábado 27", "Feria La Verbena. Contarlo ahí, en persona, vale más que "
                          "cualquier publicación.", "Ustedes"],
        ["Domingo 28", "Publicación de víspera.", "Ustedes"],
        ["<b>Lunes 29</b>", "<b>El día.</b> Publicación principal + oferta en el "
                            "perfil de Google.", "Ustedes"],
        ["Martes 30", "Publicación pidiendo reseñas.", "Ustedes"],
        ["Durante la semana", "Entrada de blog con la historia completa.", "Yo"],
        ["Jueves 2 o viernes 3", "Recordatorio, solo si quedan pocas.", "Ustedes"],
        ["Sábado 4", "Feria. Llevar cajas armadas al puesto.", "Ustedes"],
        ["Lunes 6", "Cierro la oferta en la página para que no quede vencida viva.", "Yo"],
    ], [34 * mm, 104 * mm, 32 * mm]), Spacer(1, 5 * mm)]

    f += [P("Lo que necesito de ustedes", "h2"),
          LI("<b>La decisión:</b> cuál caja, a qué precio y cuántas."),
          LI("<b>Una foto de los frascos de la caja, juntos.</b> Es la foto de la campaña "
             "y la única que no puedo hacer yo. Con luz de día, fondo simple, "
             "ordenados. Tomada con el celular está bien."),
          LI("<b>La historia real</b>, aunque sea un audio de WhatsApp."),
          LI("<b>Fotos viejas</b>, si hay. La primera feria, los primeros frascos, la etiqueta "
             "anterior. Un antes y después de la etiqueta es de lo que más se "
             "comparte."),
          Spacer(1, 4 * mm)]

    f += [caja("Lo que yo no voy a hacer, para que quede claro",
               ["<b>No publico en Instagram ni en Facebook.</b> Son sus cuentas y su voz. Yo "
                "escribo los textos, ustedes copian y pegan.",
                "<b>No invento la historia.</b> Lo que no sé, no lo escribo.",
                "<b>No publicé nada todavía.</b> La página está hecha y "
                "probada, pero está guardada. Sube el día que Luis diga, con los "
                "cambios que pida."], EMBER)]

    f += [Spacer(1, 6 * mm), rule(EMBER, 1.2),
          P("Resumen en una línea", "h3"),
          P("Escojan la caja, mándenme una foto de los frascos juntos, y el resto lo "
            "tengo listo para salir el mismo día.", "p")]

    return f


if __name__ == "__main__":
    salida = "Plan-6-Anos-CARLOUIS.pdf"
    construir(salida, contenido(), "Plan 6 años — CARLOUIS Gourmet")
    print("  %s  %.0f KB" % (salida, os.path.getsize(salida) / 1024))
    for c in CAJAS:
        suma = sum(precio(s) for s in c[3])
        print("  Caja %s (%s): %d productos, suman %s, se venden en %s, ahorro %d%%"
              % (c[0], c[1], len(c[3]), crc(suma), crc(c[4]),
                 round((suma - c[4]) / suma * 100)))
