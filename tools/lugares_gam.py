# -*- coding: utf-8 -*-
"""Cantones del Gran Área Metropolitana.

Solo se incluyen cantones que NO repiten el nombre de una provincia. Una
página "Alajuela cantón" competiría contra la página "Alajuela provincia" por
exactamente la misma búsqueda, así que esas no se hacen: se refuerza la
provincia. Estos cuatro sí son mercado propio y se pueden describir distinto
de verdad, que es lo único que separa una página útil de una doorway page.

Mismo esquema que PROVINCIAS en lugares.py, más "provincia" y "provincia_slug"
para la miga de pan.
"""

CANTONES = [

    {
        "slug": "salsas-artesanales-escazu",
        "nombre": "Escazú",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en Escazú | Entrega a Domicilio | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega a domicilio "
                 "en Escazú: San Rafael, San Antonio y centro. Entrega en 1 a 2 días."),
        "h1": "Salsas artesanales en Escazú",
        "lead": ("Entregamos en los tres distritos de Escazú —San Rafael, San Antonio y Escazú "
                 "centro— normalmente en 1 o 2 días hábiles, coordinando por WhatsApp."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("Escazú es zona de entrega directa: San Rafael, San Antonio y Escazú centro. "
                    "Coordinamos día y franja horaria por WhatsApp. Sin cargo por envío y al mismo "
                    "precio del catálogo que en cualquier otro cantón del país."),
        "intro": [
            "Escazú es, junto con Santa Ana, la zona donde más rápido se entiende lo que hacemos. Hay "
            "costumbre de producto importado y de delicatessen, y eso juega a favor: quien ya compró "
            "un pesto italiano de frasco sabe distinguir cuando uno está hecho con albahaca de verdad "
            "y cuando está hecho con aceite barato y espesante.",

            "La diferencia es que lo nuestro no viajó. Se cocina en Alajuela, a media hora de acá, en "
            "lotes pequeños. Un pesto importado lleva meses de bodega y de contenedor antes de llegar "
            "a la góndola; el nuestro lleva días.",
        ],
        "angulo_h2": "Lo que más se pide en Escazú",
        "angulo": [
            "Pesan los pedidos para recibir gente. El alioli, los tomates deshidratados en aceite de "
            "oliva y el pesto de albahaca salen casi siempre juntos: es el combo de tabla de quesos y "
            "picada, y funciona porque los tres son suaves y no compiten entre ellos.",

            "También pesa el regalo. Canastas gourmet para clientes, para equipos de trabajo y para "
            "fin de año. Para eso conviene avisar con una semana de anticipación: producimos en lotes "
            "pequeños y no mantenemos inventario grande, así que los favoritos se acaban.",

            "Y hay un tercer grupo, el que compra picante en serio. La Habanero Fire es nivel 5 de 5 y "
            "en Escazú se vende más de lo que uno esperaría, sobre todo entre gente que conoció el "
            "habanero afuera y no lo encuentra acá con el sabor correcto.",
        ],
        "destacados": [
            ("alioli", "Ajo de verdad. Para papas, carnes y para untar."),
            ("tomates-deshidratados", "En aceite de oliva. El que nunca falta en una tabla."),
            ("pesto-de-albahaca", "Resuelve una pasta en lo que hierve el agua."),
            ("salsa-habanero-fire", "Nivel 5 de 5, para el que lo busca de verdad."),
        ],
        "guias": [
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla que no se vea improvisada"),
            ("regalos-gourmet-costa-rica", "Regalos gourmet: qué llevar y qué evitar"),
        ],
        "cantones": ["Escazú centro", "San Rafael de Escazú", "San Antonio de Escazú",
                     "Bello Horizonte", "Guachipelín", "Trejos Montealegre", "Anonos", "Bebedero"],
        "faq": [
            ("¿Cuánto tardan en entregar en Escazú?",
             "Normalmente 1 o 2 días hábiles. Coordinamos el día y la franja por WhatsApp al "
             "8825 2608."),
            ("¿Cobran envío en Escazú?",
             "No. El precio del catálogo es el mismo para todo el país y no hay cargo por entrega."),
            ("¿Hacen canastas de regalo para empresas?",
             "Sí, y es de lo que más se pide acá. Escribinos con la cantidad y la fecha; para "
             "volúmenes de empresa conviene avisar con al menos una semana."),
            ("¿Dónde puedo probarlas antes de comprar?",
             "Los sábados en la Feria Orgánica La Verbena, en Plaza Real Alajuela, de 6:00 a.m. a "
             "1:00 p.m. Desde Escazú son unos 25 minutos por la autopista."),
        ],
    },

    {
        "slug": "salsas-artesanales-santa-ana",
        "nombre": "Santa Ana",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en Santa Ana y Lindora | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega en Santa Ana, "
                 "Lindora, Pozos y Piedades. 1 a 2 días, sin cargo por envío."),
        "h1": "Salsas artesanales en Santa Ana",
        "lead": ("Entregamos en todo el cantón: Santa Ana centro, Pozos, Lindora, Piedades, Brasil y "
                 "Salitral. Normalmente en 1 o 2 días hábiles."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("Santa Ana centro, Pozos, Lindora, Piedades, Brasil y Salitral son zona de "
                    "entrega directa. Coordinamos por WhatsApp, sin cargo por envío y al mismo "
                    "precio del catálogo que en el resto del país."),
        "intro": [
            "Santa Ana ya nos conoce de cerca: estuvimos con stand y degustaciones en Forum 2 Parque "
            "Empresarial, en Lindora, y ahí se acercó bastante gente del cantón que hoy nos pide "
            "directo. Ese es el patrón que más nos gusta, porque nació de que probaron el producto "
            "antes de comprarlo.",

            "Es una zona con mucha oficina y mucha casa con espacio, y eso define lo que se pide: "
            "entre semana pesa lo práctico —un pesto que resuelve una cena— y el fin de semana pesa "
            "la parrilla y la picada.",
        ],
        "angulo_h2": "Parrilla, oficina y picada",
        "angulo": [
            "El chimichurri argentino es el que más se mueve en Santa Ana, y tiene lógica: es zona de "
            "casa con jardín, de parrilla de fin de semana y de asado con gente. Un chimichurri de "
            "verdad —perejil, ajo, orégano, sin espesantes— cambia por completo un corte de carne.",

            "En Lindora, con toda la concentración de parques empresariales, lo que más entra son "
            "pedidos de oficina: alguien compra para la casa, le gusta, y a las dos semanas pide para "
            "el equipo. Para ese tipo de compra conviene mirar los precios de mayoreo, porque desde "
            "volúmenes pequeños ya cambia el precio.",

            "Y para picada, el mismo trío que en Escazú: alioli, tomates en aceite de oliva y chile "
            "morrón asado. Los tres son suaves, no pican nada y arman una tabla en cinco minutos.",
        ],
        "destacados": [
            ("chimichurri-argentino", "Para la parrilla del fin de semana."),
            ("alioli", "Ajo de verdad, para carnes y papas."),
            ("chile-morron-asado", "No pica. Dulce y ahumado, para tabla y sándwich."),
            ("mayonesa-de-chipotle", "Ahumada, picante medio. La más versátil."),
        ],
        "guias": [
            ("como-hacer-una-parrillada", "Cómo armar una parrillada que salga bien"),
            ("con-que-se-come-el-chimichurri", "Con qué se come el chimichurri"),
        ],
        "cantones": ["Santa Ana centro", "Pozos", "Lindora", "Piedades", "Brasil", "Salitral",
                     "Uruca de Santa Ana"],
        "faq": [
            ("¿Entregan en Lindora?",
             "Sí, Lindora es parte del cantón de Santa Ana y es zona de entrega directa: normalmente "
             "1 o 2 días hábiles."),
            ("¿Ya han estado en ferias por acá?",
             "Sí. Estuvimos con stand y degustaciones en Forum 2 Parque Empresarial, en Lindora. "
             "Anunciamos cada feria en la página de eventos."),
            ("¿Venden para oficinas y empresas?",
             "Sí. Es común acá por la cantidad de parques empresariales. Para pedidos de equipo o "
             "canastas manejamos precios de mayoreo desde volúmenes pequeños."),
            ("¿Cuál recomiendan para un asado?",
             "El chimichurri argentino, sin duda. Y si en la mesa hay quien come picante, la Habanero "
             "Fire aparte, para que cada quien se sirva."),
        ],
    },

    {
        "slug": "salsas-artesanales-curridabat",
        "nombre": "Curridabat",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en Curridabat y Granadilla | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega en "
                 "Curridabat, Granadilla, Sánchez y Tirrases. 1 a 2 días, sin cargo por envío."),
        "h1": "Salsas artesanales en Curridabat",
        "lead": ("Entregamos en los cuatro distritos del cantón: Curridabat centro, Granadilla, "
                 "Sánchez y Tirrases. Normalmente en 1 o 2 días hábiles."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("Curridabat centro, Granadilla, Sánchez y Tirrases son zona de entrega directa. "
                    "Se coordina por WhatsApp y no hay cargo por envío: el precio del catálogo es el "
                    "mismo en todo el país."),
        "intro": [
            "Curridabat, con San Pedro y Montes de Oca al lado, es zona de cocina de diario. Mucha "
            "casa, mucho apartamento y bastante gente que cocina entre semana y quiere resolver algo "
            "rico sin meterle una hora.",

            "Eso define el pedido típico de acá, y es distinto del de Escazú: menos tabla de quesos y "
            "más despensa. El que compra una vez suele volver al mes por lo mismo, porque se le acabó.",
        ],
        "angulo_h2": "Cocina de entre semana",
        "angulo": [
            "Los pestos son los que más se repiten. Un pesto de albahaca resuelve una pasta en lo que "
            "hierve el agua, y el de tomate hace lo mismo con un perfil más dulce. Los dos se mezclan "
            "fuera del fuego, nunca en la sartén: ahí está todo el secreto de que no pierdan el aroma.",

            "Después vienen las mayonesas saborizadas. La de chipotle para sándwich y hamburguesa, la "
            "de culantro para casado y pescado. Son las que convierten algo que uno ya iba a comer en "
            "algo que sabe distinto, sin cocinar nada más.",

            "Y los tomates deshidratados en aceite de oliva, que rinden muchísimo: un frasco dura "
            "semanas porque se usan de a poco, picados sobre una ensalada o una pasta. El aceite del "
            "frasco tampoco se bota, sirve para saltear.",
        ],
        "destacados": [
            ("pesto-de-albahaca", "Una pasta lista en lo que hierve el agua."),
            ("mayonesa-de-chipotle", "Ahumada. Para sándwich y hamburguesa."),
            ("tomates-deshidratados", "Rinden semanas. En aceite de oliva."),
            ("mayonesa-de-culantro", "Fresca y ácida. Va con casi todo lo tico."),
        ],
        "guias": [
            ("recetas-con-pesto", "Recetas con pesto que salen en 15 minutos"),
            ("como-conservar-salsas-artesanales", "Cómo conservar una salsa sin preservantes"),
        ],
        "cantones": ["Curridabat centro", "Granadilla", "Sánchez", "Tirrases"],
        "faq": [
            ("¿Cuánto tardan en entregar en Curridabat?",
             "Normalmente 1 o 2 días hábiles. Se coordina por WhatsApp al 8825 2608."),
            ("¿Cuál dura más una vez abierto?",
             "Los tomates deshidratados y el chile morrón asado, porque el aceite los protege. Las "
             "mayonesas y el alioli hay que consumirlos más rápido: no llevan preservantes "
             "artificiales, así que todo va refrigerado después de abrir."),
            ("¿Cuál recomiendan para empezar?",
             "Si cocinás entre semana, el pesto de albahaca y la mayonesa de chipotle son los dos que "
             "más se usan y los que menos se quedan guardados."),
            ("¿Hay algo que no pique?",
             "La mayoría. Los pestos, el alioli, los tomates, el chile morrón y la salsa de chile "
             "dulce no pican nada. La escala de picante lo explica producto por producto."),
        ],
    },

    {
        "slug": "salsas-artesanales-belen",
        "nombre": "Belén",
        "provincia": "Heredia",
        "provincia_slug": "salsas-artesanales-heredia",
        "geo": "CR-H",
        "titulo": "Salsas Artesanales en Belén, Heredia | CARLOUIS",
        "desc": ("Salsas de habanero, pestos, alioli y conservas artesanales con entrega en Belén: San "
                 "Antonio, La Ribera y La Asunción. A 15 minutos de Alajuela."),
        "h1": "Salsas artesanales en Belén",
        "lead": ("Belén nos queda a 15 minutos. Entregamos en San Antonio, La Ribera y La Asunción, "
                 "normalmente en 1 o 2 días hábiles y sin cargo por envío."),
        "entrega_titulo": "A 15 minutos de donde se produce",
        "entrega": ("San Antonio de Belén, La Ribera y La Asunción son zona de entrega directa y de "
                    "las más rápidas que tenemos, por la cercanía con Alajuela. Se coordina por "
                    "WhatsApp, al mismo precio del catálogo."),
        "intro": [
            "De todos los cantones del GAM, Belén es probablemente el que más cerca tiene el "
            "producto: estamos a unos 15 minutos. Eso hace que sea de los lugares donde más rápido "
            "coordinamos y donde más fácil resulta una entrega recurrente para un negocio.",

            "Es además un cantón con mucha empresa —zonas francas, corporativos, hotelería— y "
            "bastante casa de familia. Las dos cosas se notan en lo que se pide.",
        ],
        "angulo_h2": "Empresa, hotel y casa",
        "angulo": [
            "Por el lado corporativo, Belén concentra multinacionales y hoteles. Ahí lo que entra son "
            "canastas de regalo para clientes y para colaboradores, y producto para servicio de "
            "alimentación. Para eso está la página de mayoreo: trabajamos desde volúmenes pequeños y "
            "con reposición coordinada.",

            "Por el lado de casa, es el mismo perfil que Heredia en general: gente acostumbrada a "
            "comprarle a productores pequeños, que entiende por qué un frasco artesanal cuesta lo que "
            "cuesta. Los pestos y los tomates en aceite de oliva son los que más se repiten.",

            "Y algo que sirve para los dos casos: ninguno de nuestros productos lleva colorantes ni "
            "preservantes artificiales, y los pestos y las conservas vegetales son aptos para dieta "
            "vegetariana. Si hay una restricción específica, preguntá y vamos ingrediente por "
            "ingrediente.",
        ],
        "destacados": [
            ("pesto-de-albahaca", "El que más se repite en pedidos de Heredia."),
            ("tomates-deshidratados", "En aceite de oliva, para panes y ensaladas."),
            ("alioli", "Ajo de verdad. Para papas, carnes y sándwiches."),
            ("salsa-pina-habanero", "Dulce y picante. Entrada amable al habanero."),
        ],
        "guias": [
            ("regalos-gourmet-costa-rica", "Regalos gourmet: qué llevar y qué evitar"),
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla de quesos y bocas"),
        ],
        "cantones": ["San Antonio de Belén", "La Ribera", "La Asunción", "Cariari",
                     "Zona franca de Belén"],
        "faq": [
            ("¿Cuánto tardan en entregar en Belén?",
             "Es de las zonas más rápidas que tenemos por la cercanía: normalmente 1 día hábil, a "
             "veces el mismo día si se coordina temprano."),
            ("¿Hacen canastas para empresas en Belén?",
             "Sí, es de lo que más se pide acá por la cantidad de corporativos. Escribinos con la "
             "cantidad y la fecha; para volúmenes conviene avisar con una semana."),
            ("¿Venden a hoteles y restaurantes?",
             "Sí. Manejamos precios de mayoreo con reposición coordinada según la rotación del "
             "negocio. Por la cercanía, Belén es de los lugares donde más fácil resulta."),
            ("¿Tienen productos aptos para vegetarianos?",
             "Sí. Los pestos, los tomates deshidratados, el chile morrón asado y la salsa de chile "
             "dulce lo son. Si tenés una restricción específica, preguntá y te decimos ingrediente "
             "por ingrediente."),
        ],
    },
]
