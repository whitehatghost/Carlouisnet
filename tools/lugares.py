# -*- coding: utf-8 -*-
"""Contenido de las páginas por provincia.

La idea NO es repetir la misma página siete veces cambiando el nombre: eso es
lo que Google llama "doorway page" y lo castiga. Cada provincia trae su propia
razón de ser —lo que se cocina ahí, quién compra, cómo llega el pedido— y su
propio set de preguntas. Si alguna vez hay que recortar, se recorta cantidad de
provincias, no la profundidad de cada una.

Las promesas de envío (1-2 días GAM, 2-4 resto, mismo precio, SINPE) salen de
cobertura.html y tienen que seguir coincidiendo con esa página.
"""

PROVINCIAS = [

    # ------------------------------------------------------------------ SJ --
    {
        "slug": "salsas-artesanales-san-jose",
        "nombre": "San José",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en San José | Envío a los 20 Cantones | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega en San José: "
                 "Escazú, Santa Ana, Curridabat, Montes de Oca y los 20 cantones. Mismo precio que en "
                 "todo el país, 1 a 2 días en el GAM."),
        "h1": "Salsas artesanales en San José",
        "lead": ("Entregamos en los 20 cantones de la provincia de San José. Dentro del Gran Área "
                 "Metropolitana coordinamos la entrega en 1 o 2 días hábiles, y el precio es el "
                 "mismo que paga alguien en Limón o en Guanacaste."),
        "entrega_titulo": "Entrega directa en el GAM",
        "entrega": ("San José centro, Escazú, Santa Ana, Curridabat, Montes de Oca, Tibás, Moravia, "
                    "Goicoechea y Coronado son zona de entrega coordinada: normalmente 1 a 2 días "
                    "hábiles. A Pérez Zeledón, Puriscal, Acosta, Tarrazú y la zona de Los Santos "
                    "llegamos por encomienda, entre 2 y 4 días."),
        "intro": [
            "San José es donde más se pide, y no por casualidad: es la provincia con más restaurantes, "
            "más oficinas y más gente que ya se acostumbró a cocinar con producto que no sale del "
            "supermercado. La diferencia entre una salsa industrial y una hecha en lotes pequeños se "
            "nota más rápido cuando uno tiene con qué compararla.",

            "Nosotros producimos en Alajuela, a menos de una hora de San José centro. Eso significa que "
            "el frasco que le llega no pasó meses en una bodega ni cruzó un océano en un contenedor: "
            "salió de una cocina acá y llegó a su casa esta semana.",
        ],
        "angulo_h2": "Lo que más se pide en San José",
        "angulo": [
            "La provincia no se comporta igual en todos lados, y por eso el oeste y el este tienen "
            "página aparte: en <a href=\"salsas-artesanales-escazu.html\">Escazú</a> y "
            "<a href=\"salsas-artesanales-santa-ana.html\">Santa Ana</a> manda la picada y el regalo "
            "corporativo, mientras que en <a href=\"salsas-artesanales-curridabat.html\">Curridabat</a> "
            "manda la despensa de entre semana.",

            "En las oficinas del centro y de Sabana lo que más entra son canastas: para clientes y para "
            "equipos de trabajo, sobre todo de setiembre en adelante. Para eso conviene avisar con una "
            "semana, porque producimos en lotes pequeños y los favoritos se acaban.",

            "Y en Desamparados, Alajuelita y Aserrí el patrón es otra vez distinto: pesa la cocina de "
            "casa, y ahí lo que más sale es la salsa de chile dulce y la mayonesa de culantro, que se "
            "meten dentro del plato de todos los días en vez de ir encima.",
        ],
        "destacados": [
            ("alioli", "El más pedido de la provincia. Para papas, carnes y sándwiches."),
            ("pesto-de-albahaca", "Resuelve una pasta en lo que hierve el agua."),
            ("tomates-deshidratados", "En aceite de oliva. El que nunca falta en una tabla."),
            ("salsa-habanero-fire", "Para el que de verdad come picante. Nivel 5 de 5."),
        ],
        "guias": [
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla que no se vea improvisada"),
            ("regalos-gourmet-costa-rica", "Regalos gourmet: qué llevar y qué evitar"),
        ],
        "cantones": ["San José", "Escazú", "Desamparados", "Santa Ana", "Curridabat", "Montes de Oca",
                     "Moravia", "Tibás", "Goicoechea", "Alajuelita", "Aserrí", "Mora", "Puriscal",
                     "Acosta", "Vázquez de Coronado", "Dota", "Tarrazú", "León Cortés", "Turrubares",
                     "Pérez Zeledón"],
        "faq": [
            ("¿Hacen entregas en Escazú y Santa Ana?",
             "Sí, son de las zonas donde más entregamos. Coordinamos por WhatsApp el día y la franja "
             "horaria; normalmente es cuestión de 1 o 2 días hábiles."),
            ("¿Llegan a Pérez Zeledón?",
             "Sí. Pérez Zeledón sale por encomienda, entre 2 y 4 días hábiles, con empaque reforzado y "
             "sin ningún cargo extra: paga el mismo precio del catálogo."),
            ("¿Puedo pedir para una oficina o para regalo corporativo?",
             "Sí, y es de lo que más hacemos en San José. Escribinos con la cantidad y para cuándo lo "
             "necesitás. Si son volúmenes de empresa, mirá también las condiciones de mayoreo."),
            ("¿Tienen punto de venta físico en San José?",
             "Punto fijo no. Estamos los sábados en la Feria Orgánica La Verbena, en Plaza Real "
             "Alajuela, que para mucha gente del oeste josefino queda a 20 minutos. El resto se "
             "coordina por entrega."),
        ],
    },

    # ------------------------------------------------------------------- A --
    {
        "slug": "salsas-artesanales-alajuela",
        "nombre": "Alajuela",
        "geo": "CR-A",
        "titulo": "Salsas Artesanales en Alajuela | Acá las Hacemos | CARLOUIS",
        "desc": ("CARLOUIS produce en Alajuela. Salsas de habanero, chimichurri, pestos y conservas "
                 "artesanales con entrega en los 16 cantones y retiro sin costo los sábados en la "
                 "Feria La Verbena, Plaza Real Alajuela."),
        "h1": "Salsas artesanales en Alajuela",
        "lead": ("Acá es donde se cocina todo lo que vendemos. Si estás en Alajuela, sos la persona "
                 "que más cerca tiene el producto: entrega coordinada, o retiro sin costo el sábado "
                 "en la feria."),
        "entrega_titulo": "Nuestra base de operaciones",
        "entrega": ("Alajuela centro, Grecia, Atenas, Naranjo, Palmares, Poás, Sarchí y San Ramón son "
                    "zona de entrega coordinada. A la Zona Norte —San Carlos, Upala, Los Chiles, "
                    "Guatuso y Río Cuarto— llegamos por encomienda en 2 a 4 días hábiles."),
        "intro": [
            "CARLOUIS no es una marca que se fabrica quién sabe dónde y se distribuye acá. Se cocina en "
            "Alajuela, en lotes pequeños, y de acá sale para el resto del país. Para el cliente "
            "alajuelense eso tiene una ventaja concreta que nadie más tiene: puede venir, probar todo y "
            "llevárselo el mismo día, sin pagar envío ni esperar encomienda.",

            "Nos encontrás todos los sábados de 6:00 a.m. a 1:00 p.m. en la Feria Orgánica La Verbena, "
            "en Plaza Real Alajuela. Ahí está la línea completa y se puede probar antes de decidir, que "
            "es la mejor forma de comprar picante: nadie debería comprar un habanero a ciegas.",
        ],
        "angulo_h2": "Por qué el producto es de acá",
        "angulo": [
            "Producir en lotes pequeños es más caro y más lento que mandar a maquilar. Lo hacemos así "
            "porque es la única forma de mantener el sabor parejo y de no tener que meterle "
            "preservantes ni colorantes. La contra es que no hay inventario grande: cuando se acaba un "
            "lote, hay que esperar el siguiente.",

            "El chile habanero, la albahaca y el culantro los conseguimos de proveedores de la zona "
            "cuando la temporada acompaña. No es un discurso de marketing: es que el ingrediente fresco "
            "rinde distinto, y en una salsa de tres o cuatro ingredientes no hay dónde esconder uno malo.",

            "Si estás en Alajuela y tenés una soda, un restaurante o una tienda, esa cercanía también "
            "juega a favor para reposición frecuente. Se puede coordinar entrega recurrente sin que el "
            "producto pase días viajando.",
        ],
        "destacados": [
            ("salsa-habanero-fire", "El más vendido en feria. Probalo antes de llevártelo."),
            ("chimichurri-argentino", "Para la parrillada del domingo."),
            ("salsa-pina-habanero", "Dulce y picante. El que convence al que dice que no come picante."),
            ("mayonesa-de-culantro", "Va con casi todo lo que se come acá."),
        ],
        "guias": [
            ("escala-de-picante", "Qué tan picante es cada una, en serio"),
            ("como-hacer-una-parrillada", "Cómo armar una parrillada que salga bien"),
        ],
        "cantones": ["Alajuela", "San Ramón", "Grecia", "Atenas", "Naranjo", "Palmares", "Poás",
                     "San Mateo", "Orotina", "San Carlos", "Zarcero", "Sarchí", "Upala", "Los Chiles",
                     "Guatuso", "Río Cuarto"],
        "faq": [
            ("¿Puedo retirar sin pagar envío?",
             "Sí. Reservás por WhatsApp lo que querés y lo retirás el sábado en la Feria La Verbena, "
             "Plaza Real Alajuela, de 6:00 a.m. a 1:00 p.m. Es la opción más cómoda si vivís cerca."),
            ("¿Puedo probar antes de comprar?",
             "En la feria sí, y es lo que recomendamos. Está la línea completa abierta para degustar. "
             "Con las salsas de habanero sobre todo: el nivel de picante hay que sentirlo, no leerlo."),
            ("¿Llegan a San Carlos y a la Zona Norte?",
             "Sí. San Carlos, Upala, Los Chiles, Guatuso y Río Cuarto salen por encomienda, entre 2 y 4 "
             "días hábiles, con empaque reforzado y al mismo precio del catálogo."),
            ("¿Se puede visitar el lugar de producción?",
             "No tenemos local abierto al público: es una cocina de producción, no una tienda. El punto "
             "de encuentro es la feria de los sábados."),
        ],
    },

    # ------------------------------------------------------------------- H --
    {
        "slug": "salsas-artesanales-heredia",
        "nombre": "Heredia",
        "geo": "CR-H",
        "titulo": "Salsas Artesanales en Heredia | Envío a los 10 Cantones | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega en Heredia: "
                 "Belén, Flores, Santo Domingo, Barva, San Rafael y los 10 cantones. Mismo precio en "
                 "todo el país."),
        "h1": "Salsas artesanales en Heredia",
        "lead": ("Heredia nos queda al lado y es zona de entrega frecuente. Llegamos a los 10 cantones, "
                 "desde Belén y Flores hasta Sarapiquí, con el mismo precio que en el resto del país."),
        "entrega_titulo": "Zona de entrega frecuente",
        "entrega": ("Heredia centro, Belén, Flores, San Pablo, Santo Domingo, Barva, San Rafael, San "
                    "Isidro y Santa Bárbara son entrega coordinada, normalmente 1 a 2 días hábiles. A "
                    "Sarapiquí llegamos por encomienda, entre 2 y 4 días."),
        "intro": [
            "Heredia tiene una cosa que no tienen todas las provincias: una cultura de café y de "
            "producto local que ya está formada. La gente de Barva, de Santo Domingo y de San Rafael "
            "está acostumbrada a comprarle a productores pequeños, y eso hace que explicar por qué una "
            "salsa artesanal cuesta lo que cuesta sea mucho más fácil.",

            "Estamos a menos de media hora de Heredia centro, así que es de las provincias donde más "
            "seguido coordinamos entregas. Belén y Flores, por la cantidad de empresas, concentran "
            "buena parte de los pedidos de oficina.",
        ],
        "angulo_h2": "Nos vas a ver por acá",
        "angulo": [
            "No solo enviamos a Heredia: también vamos. El domingo 20 de setiembre estuvimos con stand "
            "en la Feria Holística de Ananta Yoga y Café, en Heredia centro, y la idea es repetir. Ese "
            "tipo de feria —producto local, gente que le importa lo que come— es exactamente donde "
            "nuestro producto se explica solo.",

            "Si tenés un café, una tienda de producto natural o un estudio con tienda en Heredia, la "
            "cercanía hace fácil la reposición frecuente. Varias de las cosas que hacemos calzan con "
            "ese tipo de negocio: los pestos y los tomates en aceite de oliva son aptos para dieta "
            "vegetariana y ninguna receta nuestra lleva colorantes ni preservantes artificiales.",
        ],
        "destacados": [
            ("pesto-de-albahaca", "El que más se repite en pedidos de Heredia."),
            ("tomates-deshidratados", "En aceite de oliva, para panes y ensaladas."),
            ("alioli", "Para papas, carnes y para untar sin pensarlo mucho."),
            ("salsa-pina-habanero", "Picante con dulzor de piña. Entrada amable."),
        ],
        "guias": [
            ("recetas-con-pesto", "Recetas con pesto que salen en 15 minutos"),
            ("como-conservar-salsas-artesanales", "Cómo conservar una salsa sin preservantes"),
        ],
        "cantones": ["Heredia", "Barva", "Santo Domingo", "Santa Bárbara", "San Rafael", "San Isidro",
                     "Belén", "Flores", "San Pablo", "Sarapiquí"],
        "faq": [
            ("¿Cada cuánto entregan en Heredia?",
             "Es de nuestras zonas más frecuentes. Escribinos por WhatsApp y te decimos la próxima "
             "ruta; casi siempre es cuestión de 1 o 2 días hábiles."),
            ("¿Llegan a Sarapiquí?",
             "Sí, por encomienda, entre 2 y 4 días hábiles. El empaque se refuerza para el trayecto y "
             "no cuesta nada adicional."),
            ("¿Van a ferias en Heredia?",
             "Sí. Estuvimos en la Feria Holística de Ananta Yoga, en Heredia centro, y la intención es "
             "volver. Anunciamos cada feria en la página de eventos y en Instagram."),
            ("¿Venden a cafeterías y tiendas en Heredia?",
             "Sí. Para cafés, tiendas de producto natural y sodas manejamos precios de mayoreo desde "
             "volúmenes pequeños, con reposición coordinada."),
        ],
    },

    # ------------------------------------------------------------------- C --
    {
        "slug": "salsas-artesanales-cartago",
        "nombre": "Cartago",
        "geo": "CR-C",
        "titulo": "Salsas Artesanales en Cartago | Envío a los 8 Cantones | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega en Cartago: "
                 "La Unión, Paraíso, Oreamuno, Turrialba, El Guarco y los 8 cantones. Mismo precio "
                 "en todo el país."),
        "h1": "Salsas artesanales en Cartago",
        "lead": ("Llegamos a los 8 cantones de Cartago, desde La Unión y Cartago centro hasta "
                 "Turrialba y Jiménez. Mismo precio que en el resto del país, sin cargo por envío."),
        "entrega_titulo": "Entrega coordinada y encomienda",
        "entrega": ("La Unión y Cartago centro son zona de entrega coordinada, normalmente 1 a 2 días "
                    "hábiles. A Paraíso, Oreamuno, Alvarado, El Guarco, Jiménez y Turrialba llegamos "
                    "por encomienda, entre 2 y 4 días."),
        "intro": [
            "Cartago es provincia de clima frío y de comida de olla: olla de carne, picadillos, "
            "gallos, cosas que se cocinan despacio. Ese tipo de cocina es donde mejor entra una salsa "
            "con carácter, porque no compite con el plato, lo levanta.",

            "Y hay algo que Cartago tiene y nadie más: el queso Turrialba. Es probablemente el mejor "
            "acompañante que existe en el país para nuestros tomates deshidratados en aceite de oliva y "
            "para el chile morrón asado. Queso fresco, tomate en aceite, un pan decente y ya está "
            "resuelta una picada seria.",
        ],
        "angulo_h2": "Lo que mejor calza con la comida cartaginesa",
        "angulo": [
            "El chile morrón asado y la salsa de chile dulce son los dos que más sentido hacen acá. No "
            "pican —ninguno de los dos— y funcionan dentro de la comida tica de siempre: en un arroz, "
            "en un picadillo, en unos huevos. Es sabor, no ardor.",

            "Para el que sí come picante, el frío de Cartago juega a favor de la Habanero Fire. Suena a "
            "chiste pero no lo es: el picante se disfruta distinto cuando afuera están a 16 grados.",

            "Y en Turrialba, con toda la escena de turismo y de rafting, varias sodas y hospedajes "
            "manejan mesa para visitante extranjero. Ahí una salsa artesanal costarricense con etiqueta "
            "propia dice más que una botella industrial importada.",
        ],
        "destacados": [
            ("chile-morron-asado", "Con queso Turrialba fresco es imbatible."),
            ("tomates-deshidratados", "En aceite de oliva, para tabla y para pan."),
            ("salsa-de-chile-dulce", "Sabor sin picante. Entra en la comida de todos los días."),
            ("salsa-habanero-fire", "Para el que come picante de verdad."),
        ],
        "guias": [
            ("salsas-para-comida-tica", "Qué salsa va con cada plato tico"),
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla de quesos y bocas"),
        ],
        "cantones": ["Cartago", "Paraíso", "La Unión", "Jiménez", "Turrialba", "Alvarado",
                     "Oreamuno", "El Guarco"],
        "faq": [
            ("¿Entregan en La Unión y Tres Ríos?",
             "Sí, es zona de entrega coordinada por la cercanía con el GAM: normalmente 1 a 2 días "
             "hábiles."),
            ("¿Llegan a Turrialba?",
             "Sí, por encomienda, entre 2 y 4 días hábiles, con empaque reforzado y al mismo precio "
             "del catálogo."),
            ("¿Qué recomiendan para acompañar queso Turrialba?",
             "Los tomates deshidratados en aceite de oliva y el chile morrón asado. Los dos son "
             "suaves, no tapan el queso fresco y le dan acidez y dulzor."),
            ("¿Tienen algo que no pique?",
             "Varias cosas: el chile morrón asado, la salsa de chile dulce, los pestos, el alioli y "
             "los tomates deshidratados no pican nada. La escala de picante explica cuál es cuál."),
        ],
    },

    # ------------------------------------------------------------------- G --
    {
        "slug": "salsas-artesanales-guanacaste",
        "nombre": "Guanacaste",
        "geo": "CR-G",
        "titulo": "Salsas Artesanales en Guanacaste | Envío a los 11 Cantones | CARLOUIS",
        "desc": ("Salsas de habanero, chimichurri y conservas artesanales con envío a Guanacaste: "
                 "Liberia, Santa Cruz, Nicoya, Carrillo, Tilarán y los 11 cantones. Empaque "
                 "reforzado, mismo precio que en todo el país."),
        "h1": "Salsas artesanales en Guanacaste",
        "lead": ("Enviamos a los 11 cantones de Guanacaste por encomienda, entre 2 y 4 días hábiles, "
                 "con empaque reforzado para el trayecto. El precio es el mismo que paga alguien en "
                 "Alajuela centro."),
        "entrega_titulo": "Encomienda con empaque reforzado",
        "entrega": ("Liberia, Santa Cruz, Nicoya, Carrillo, Bagaces, Cañas, Abangares, Tilarán, "
                    "Nandayure, La Cruz y Hojancha salen por encomienda, entre 2 y 4 días hábiles. "
                    "Cada frasco va envuelto individualmente y con material amortiguador."),
        "intro": [
            "Guanacaste es la provincia donde el envío importa más, y por eso es donde más cuidamos el "
            "empaque. Son trayectos largos, en carretera y con calor, y un frasco mal empacado no "
            "llega. Cada uno va envuelto por separado y con amortiguación; para fuera del GAM "
            "reforzamos sin cobrar nada extra.",

            "Vale decirlo claro: el precio del catálogo es el mismo. No cobramos más por estar lejos. "
            "Si una salsa dice lo que dice, eso es lo que se paga en Liberia igual que en Alajuela.",
        ],
        "angulo_h2": "Picante, mar y hotelería",
        "angulo": [
            "Acá el picante tiene otro papel. Con pescado fresco, con ceviche y con casados de playa, "
            "la mayonesa de culantro y la Piña Habanero funcionan mejor que cualquier salsa pesada: "
            "aportan acidez y frescura en vez de untar grasa sobre grasa.",

            "La Piña Habanero en particular es la que más sentido hace en Guanacaste. Es dulce y "
            "picante a la vez, y ese perfil tropical calza con marisco de una forma que el visitante "
            "extranjero entiende de inmediato.",

            "Y está el tema de hotelería. Entre Tamarindo, Nosara, Sámara, Papagayo y Liberia hay una "
            "cantidad enorme de hoteles, villas y restaurantes que buscan producto costarricense "
            "auténtico para su mesa. Un frasco artesanal hecho en Costa Rica cuenta una historia que "
            "una botella importada no puede contar. Para ese tipo de compra manejamos mayoreo con "
            "entregas recurrentes.",
        ],
        "destacados": [
            ("salsa-pina-habanero", "Dulce y picante. La que mejor va con pescado y ceviche."),
            ("mayonesa-de-culantro", "Fresca y ácida. Para marisco y casados."),
            ("salsa-habanero-fire", "Nivel 5 de 5, para el que lo busca de verdad."),
            ("chimichurri-argentino", "Para carne a la parrilla en la playa."),
        ],
        "guias": [
            ("escala-de-picante", "Cuánto pica cada una, sin adivinar"),
            ("como-conservar-salsas-artesanales", "Cómo conservarlas en clima caliente"),
        ],
        "cantones": ["Liberia", "Nicoya", "Santa Cruz", "Bagaces", "Carrillo", "Cañas", "Abangares",
                     "Tilarán", "Nandayure", "La Cruz", "Hojancha"],
        "faq": [
            ("¿Cobran más por enviar a Guanacaste?",
             "No. El precio del catálogo es el mismo para todo el país. No hay recargo por distancia "
             "ni por zona."),
            ("¿Los frascos aguantan el viaje y el calor?",
             "Sí. Cada frasco va envuelto individualmente y empacado con material amortiguador, y para "
             "envíos fuera del GAM reforzamos el empaque sin costo. Una vez abierto conviene "
             "refrigerar, porque no llevan preservantes artificiales."),
            ("¿Venden a hoteles y restaurantes de playa?",
             "Sí. Trabajamos con hotelería y restaurantes con precios de mayoreo y reposición "
             "coordinada. Escribinos con el volumen que estimás al mes."),
            ("¿Cuál recomiendan para pescado y ceviche?",
             "La Piña Habanero y la mayonesa de culantro. Las dos aportan acidez y frescura, que es "
             "justo lo que pide el marisco."),
        ],
    },

    # ------------------------------------------------------------------- P --
    {
        "slug": "salsas-artesanales-puntarenas",
        "nombre": "Puntarenas",
        "geo": "CR-P",
        "titulo": "Salsas Artesanales en Puntarenas | Envío a los 13 Cantones | CARLOUIS",
        "desc": ("Salsas de habanero, pestos y conservas artesanales con envío a Puntarenas: Quepos, "
                 "Garabito, Osa, Monteverde, Golfito, Corredores y los 13 cantones. Empaque "
                 "reforzado, mismo precio en todo el país."),
        "h1": "Salsas artesanales en Puntarenas",
        "lead": ("Enviamos a los 13 cantones de Puntarenas, del Pacífico Central al Sur y a Monteverde, "
                 "por encomienda en 2 a 4 días hábiles y al mismo precio que en todo el país."),
        "entrega_titulo": "Del Pacífico Central a la Zona Sur",
        "entrega": ("Puntarenas, Esparza, Montes de Oro, Garabito, Parrita, Quepos, Osa, Golfito, "
                    "Corredores, Coto Brus, Buenos Aires, Monteverde y Puerto Jiménez salen por "
                    "encomienda, entre 2 y 4 días hábiles, con empaque reforzado sin costo extra."),
        "intro": [
            "Puntarenas es la provincia más larga y más variada del país: en el mismo territorio hay "
            "playa de Pacífico Central, bosque nuboso en Monteverde y frontera en Corredores. Eso "
            "significa que no hay una sola manera de llegar, y por eso conviene escribirnos antes: "
            "según el cantón coordinamos el servicio que mejor funcione.",

            "A todos llegamos, y todos pagan el mismo precio del catálogo. Puerto Jiménez y Monteverde "
            "incluidos, que son los dos cantones más nuevos del país.",
        ],
        "angulo_h2": "Marisco, turismo y frontera",
        "angulo": [
            "En el Pacífico Central —Jacó, Herradura, Quepos, Manuel Antonio— la demanda es de "
            "restaurante y de casa de playa. Ahí lo que funciona es lo que acompaña pescado y camarón "
            "sin taparlos: la mayonesa de culantro, la Piña Habanero y el alioli.",

            "En Monteverde la cosa cambia por completo. Es zona de producto artesanal, de queso propio "
            "y de visitante que busca específicamente lo hecho a mano. Los pestos, los tomates "
            "deshidratados y el chile morrón asado calzan con esa mesa mucho mejor que una salsa "
            "picante.",

            "Y en la Zona Sur —Osa, Golfito, Corredores, Coto Brus— pesa más la cocina de casa y la "
            "soda. La salsa de chile dulce y el chile morrón asado entran ahí sin problema, porque no "
            "pican y se meten dentro de la comida de siempre.",
        ],
        "destacados": [
            ("mayonesa-de-culantro", "Para pescado, camarón y casados de playa."),
            ("salsa-pina-habanero", "Dulce y picante, perfil tropical."),
            ("pesto-de-tomate", "Para pastas y panes. Bien recibido en Monteverde."),
            ("chile-morron-asado", "No pica. Para cocina de casa y de soda."),
        ],
        "guias": [
            ("que-llevar-a-un-picnic", "Qué llevar a un día de playa o de picnic"),
            ("salsas-para-comida-tica", "Qué salsa va con cada plato tico"),
        ],
        "cantones": ["Puntarenas", "Esparza", "Buenos Aires", "Montes de Oro", "Osa", "Quepos",
                     "Golfito", "Coto Brus", "Parrita", "Corredores", "Garabito", "Monteverde",
                     "Puerto Jiménez"],
        "faq": [
            ("¿Llegan a Monteverde y a Puerto Jiménez?",
             "Sí, a los dos, por encomienda. Son los cantones más nuevos del país y a veces el "
             "servicio tarda del lado alto del rango, entre 3 y 4 días hábiles."),
            ("¿Entregan en Jacó, Quepos y Manuel Antonio?",
             "Sí. Toda esa zona del Pacífico Central sale por encomienda, entre 2 y 4 días hábiles, "
             "al mismo precio del catálogo."),
            ("¿Venden a restaurantes y hospedajes de playa?",
             "Sí. Para restaurantes, hoteles y hospedajes manejamos precios de mayoreo con reposición "
             "coordinada según su rotación."),
            ("¿Qué recomiendan para acompañar pescado?",
             "La mayonesa de culantro y la Piña Habanero. Las dos aportan frescura y acidez sin tapar "
             "el sabor del pescado."),
        ],
    },

    # ------------------------------------------------------------------- L --
    {
        "slug": "salsas-artesanales-limon",
        "nombre": "Limón",
        "geo": "CR-L",
        "titulo": "Salsas Artesanales en Limón | Envío a los 6 Cantones | CARLOUIS",
        "desc": ("Salsas de habanero, chimichurri y conservas artesanales con envío al Caribe: Limón, "
                 "Pococí, Siquirres, Talamanca, Matina y Guácimo. Empaque reforzado y el mismo precio "
                 "que en todo el país."),
        "h1": "Salsas artesanales en Limón",
        "lead": ("Enviamos a los 6 cantones de la provincia de Limón por encomienda, entre 2 y 4 días "
                 "hábiles, con empaque reforzado y sin recargo por distancia."),
        "entrega_titulo": "Envío al Caribe costarricense",
        "entrega": ("Limón centro, Pococí, Guácimo, Siquirres, Matina y Talamanca salen por "
                    "encomienda, entre 2 y 4 días hábiles. El empaque se refuerza para el trayecto "
                    "sin ningún costo adicional."),
        "intro": [
            "Limón es la provincia donde más respeto hay que tener al hablar de picante, porque es la "
            "única del país donde el chile ya es parte de la cocina de siempre. El rice and beans, el "
            "rondón, el pollo caribeño: ahí el picante no es un agregado, viene de fábrica.",

            "Eso nos pone una vara más alta y nos parece bien. Una salsa de habanero que se vende en "
            "Limón tiene que aguantar la comparación con lo que la gente ya hace en su casa.",
        ],
        "angulo_h2": "Picante donde el picante es tradición",
        "angulo": [
            "La Habanero Fire es la que tiene sentido acá: nivel 5 de 5, habanero seleccionado, sin "
            "azúcar que le baje el filo. Es la única de la línea que se puede poner en una mesa "
            "limonense sin quedar corta.",

            "La salsa de chile dulce cumple otro papel: aporta sabor de chile sin ardor, y funciona "
            "dentro de un arroz o de un guiso cuando en la mesa hay gente que no come picante. No "
            "compite con la tradición, la acompaña.",

            "Y el chimichurri argentino entra por otro lado. En una provincia donde la carne a la "
            "parrilla y el pollo asado son plan de fin de semana, un chimichurri de verdad —con "
            "perejil, ajo y orégano de a de veras— se gana su lugar rápido.",
        ],
        "destacados": [
            ("salsa-habanero-fire", "Nivel 5 de 5. La única que aguanta una mesa limonense."),
            ("salsa-de-chile-dulce", "Sabor de chile sin ardor, para el resto de la mesa."),
            ("chimichurri-argentino", "Para pollo asado y carne a la parrilla."),
            ("mayonesa-de-chipotle", "Ahumada y con picante medio."),
        ],
        "guias": [
            ("escala-de-picante", "Del 1 al 5: cuánto pica cada una"),
            ("con-que-se-come-el-chimichurri", "Con qué se come el chimichurri"),
        ],
        "cantones": ["Limón", "Pococí", "Siquirres", "Talamanca", "Matina", "Guácimo"],
        "faq": [
            ("¿Cuánto tarda un envío a Limón?",
             "Entre 2 y 4 días hábiles por encomienda, según el cantón. Talamanca suele ir del lado "
             "alto del rango."),
            ("¿Cobran extra por enviar al Caribe?",
             "No. El precio del catálogo es el mismo para todo el país, sin recargo por distancia."),
            ("¿Cuál es la más picante que tienen?",
             "La Habanero Fire, nivel 5 de 5. Es la más intensa de la línea y está hecha con habanero "
             "seleccionado, sin azúcar que le baje el filo."),
            ("¿Entregan en Puerto Viejo y Cahuita?",
             "Sí, esa zona entra dentro del cantón de Talamanca y sale por encomienda, entre 3 y 4 "
             "días hábiles."),
        ],
    },
]
