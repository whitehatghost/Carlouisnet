# -*- coding: utf-8 -*-
"""Segunda tanda de cantones del GAM.

Criterio para que un cantón entre acá: que se pueda decir algo de él que no
se pueda decir de otro. Coronado es zona lechera y quesera; San Pedro es
universidad y sodas; Atenas es casa de fin de semana. Eso da páginas
distintas de verdad.

Los que NO entran, y por qué:
  - Alajuela, Heredia y Cartago centro: competirían contra su propia página
    de provincia por la misma búsqueda.
  - Cantones fuera del GAM: la entrega es por encomienda igual que en toda la
    provincia, así que la página de provincia ya los cubre sin repetirse.

Si en algún momento esto se vuelve relleno —páginas que dicen lo mismo con
otro nombre— hay que borrarlas, no seguir agregando. Google las llama
doorway pages y castiga al sitio entero, no solo a la página.
"""

CANTONES2 = [

    {
        "slug": "salsas-artesanales-coronado",
        "nombre": "Coronado",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en Coronado | Para Queso y Tabla | CARLOUIS",
        "desc": ("Conservas, pestos y salsas artesanales con entrega en Vázquez de Coronado: "
                 "San Isidro, Dulce Nombre, Patalillo y Cascajal. Lo que mejor acompaña el queso "
                 "de la zona. Entrega en 1 a 2 días."),
        "h1": "Salsas artesanales en Coronado",
        "lead": ("Entregamos en todo Vázquez de Coronado: San Isidro, Dulce Nombre, Patalillo, "
                 "Cascajal y Jesús. Normalmente en 1 o 2 días hábiles."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("San Isidro de Coronado, Dulce Nombre, Patalillo, Cascajal y Jesús son zona "
                    "de entrega directa. Se coordina por WhatsApp, sin cargo por envío."),
        "intro": [
            "Coronado es zona de lechería y de queso. Eso no es un dato de folleto: define lo que "
            "la gente de acá busca cuando compra algo para acompañar. Quien tiene queso fresco "
            "bueno a mano no necesita una salsa que tape nada, necesita algo que lo levante.",

            "Y ahí está lo que mejor calza de nuestra línea. Los tomates deshidratados en aceite de "
            "oliva y el chile morrón asado son los dos que se hicieron para eso: dulzor concentrado "
            "y algo de ahumado contra la acidez láctea del queso fresco.",
        ],
        "angulo_h2": "Queso de Coronado y qué ponerle",
        "angulo": [
            "Con queso fresco o semiduro, el chile morrón asado hace el mejor papel. No pica nada, "
            "es dulce y sedoso, y el dejo de fuego que le queda del asado es justo el contraste que "
            "le falta a un queso joven.",

            "Con queso maduro o azul, en cambio, lo que funciona es la salsa de mora. La mora de "
            "altura costarricense es más ácida que la de otros lados, y esa acidez corta la grasa "
            "del queso curado igual que lo hace una mermelada de higo. Es la combinación que más "
            "sorprende a quien la prueba por primera vez.",

            "Y para armar una tabla completa, agregue los tomates en aceite de oliva y un pan "
            "decente. Con eso y queso de la zona ya está resuelta una picada seria, sin cocinar nada.",
        ],
        "destacados": [
            ("chile-morron-asado", "Con queso fresco es la mejor combinación que hay."),
            ("salsa-de-mora", "Ácida. Para queso maduro y queso azul."),
            ("tomates-deshidratados", "En aceite de oliva. Para tabla y para pan."),
            ("alioli", "Ajo de verdad. Para papas y carnes."),
        ],
        "guias": [
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla de quesos y bocas"),
            ("regalos-gourmet-costa-rica", "Regalos gourmet: qué llevar y qué evitar"),
        ],
        "cantones": ["San Isidro de Coronado", "Dulce Nombre", "Patalillo", "Cascajal",
                     "Jesús", "San Rafael de Coronado"],
        "faq": [
            ("¿Cuánto tardan en entregar en Coronado?",
             "Normalmente 1 o 2 días hábiles. Se coordina el día por WhatsApp al 8825 2608."),
            ("¿Qué recomiendan para acompañar queso fresco?",
             "El chile morrón asado y los tomates deshidratados en aceite de oliva. Ninguno pica y "
             "los dos aportan dulzor sin tapar el sabor del queso."),
            ("¿Y para queso maduro o azul?",
             "La salsa de mora. La acidez de la mora de altura corta la grasa del queso curado, "
             "igual que lo hace una mermelada de higo."),
            ("¿Venden a lecherías o tiendas de la zona?",
             "Sí. Para tiendas, queserías y sodas manejamos precios de mayoreo desde volúmenes "
             "pequeños, con reposición coordinada."),
        ],
    },

    {
        "slug": "salsas-artesanales-san-pedro",
        "nombre": "San Pedro",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en San Pedro y Montes de Oca | CARLOUIS",
        "desc": ("Salsas, pestos y mayonesas artesanales con entrega en San Pedro, Montes de Oca, "
                 "Sabanilla y Los Yoses. Para cocina de entre semana y para sodas. Entrega en 1 a "
                 "2 días, sin cargo."),
        "h1": "Salsas artesanales en San Pedro",
        "lead": ("Entregamos en todo Montes de Oca: San Pedro, Sabanilla, Mercedes y San Rafael, "
                 "más Los Yoses y Barrio Dent. Normalmente en 1 o 2 días hábiles."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("San Pedro, Sabanilla, Mercedes, San Rafael de Montes de Oca, Los Yoses y "
                    "Barrio Dent son zona de entrega directa. Se coordina por WhatsApp."),
        "intro": [
            "San Pedro tiene una particularidad que ninguna otra zona del país tiene: la "
            "Universidad de Costa Rica al lado. Eso llena el cantón de apartamentos, de gente "
            "cocinando poco y rápido, y de una cantidad de sodas y restaurantes chiquitos que "
            "compiten por el mismo almuerzo.",

            "Las dos cosas nos sirven, pero por razones distintas, y por eso acá el pedido típico "
            "se parte en dos: el que compra para su cocina y el que compra para su negocio.",
        ],
        "angulo_h2": "Cocina de apartamento y cocina de soda",
        "angulo": [
            "El negocio de comida alrededor de la universidad vive de una cosa: que el "
            "estudiante vuelva mañana. Con almuerzos a precio parecido en cada esquina, lo que "
            "decide no es el precio sino que algo sepa mejor que al lado.",

            "Ahí una salsa de casa hace más que una campaña. La Habanero Fire y la mayonesa de "
            "chipotle son las dos que la clientela joven busca y pide por nombre, y ninguna de las "
            "dos sube el costo por porción de forma apreciable: se sirven en cucharadita.",

            "Para ese tipo de negocio manejamos mayoreo desde volúmenes chicos, con reposición "
            "cada semana o cada quince días. Un local que vende cien almuerzos al día no necesita "
            "una bodega, necesita que le llegue seguido.",
        ],
        "destacados": [
            ("pesto-de-albahaca", "Una pasta lista en lo que hierve el agua."),
            ("mayonesa-de-chipotle", "Ahumada. Para sándwich y hamburguesa."),
            ("salsa-habanero-fire", "Nivel 5 de 5, para el que come picante de verdad."),
            ("pesto-de-tomate", "Más dulce que el verde. Para pastas y panes."),
        ],
        "guias": [
            ("recetas-con-pesto", "Recetas con pesto que salen en 15 minutos"),
            ("como-conservar-salsas-artesanales", "Cómo conservar una salsa sin preservantes"),
        ],
        "cantones": ["San Pedro", "Sabanilla", "Mercedes", "San Rafael de Montes de Oca",
                     "Los Yoses", "Barrio Dent", "Cedros"],
        "faq": [
            ("¿Cuánto tardan en entregar en San Pedro?",
             "Normalmente 1 o 2 días hábiles, coordinando por WhatsApp al 8825 2608."),
            ("¿Cuál rinde más si cocino poco?",
             "Los pestos y los tomates deshidratados. Se usan de a poco y un frasco dura semanas, "
             "porque son concentrados: no se gasta medio frasco en un plato."),
            ("¿Venden a sodas y restaurantes de la zona?",
             "Sí, y es de lo que más nos interesa acá. Para sodas y restaurantes hay precios de "
             "mayoreo desde volúmenes pequeños, con reposición coordinada."),
            ("¿Tienen algo que no lleve lácteos?",
             "Varias cosas: las salsas de habanero, el chimichurri, los tomates deshidratados, el "
             "chile morrón y la salsa de chile dulce no llevan lácteos. Preguntá por el producto "
             "puntual y te decimos ingrediente por ingrediente."),
        ],
    },

    {
        "slug": "salsas-artesanales-desamparados",
        "nombre": "Desamparados",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en Desamparados | Envío sin Cargo | CARLOUIS",
        "desc": ("Salsas, conservas y mayonesas artesanales con entrega en Desamparados: San "
                 "Rafael Arriba, Gravilias, San Miguel, Patarrá y Damas. Mismo precio que en todo "
                 "el país."),
        "h1": "Salsas artesanales en Desamparados",
        "lead": ("Entregamos en todo el cantón: Desamparados centro, San Rafael Arriba y Abajo, "
                 "Gravilias, San Miguel, Patarrá, Damas y San Juan de Dios."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("Desamparados es de los cantones más grandes del país y la entrega se coordina "
                    "por distrito. Centro, San Rafael, Gravilias y Damas salen en 1 o 2 días "
                    "hábiles; a los distritos altos como Frailes y San Cristóbal conviene "
                    "coordinar con un día más."),
        "intro": [
            "Desamparados es el cantón con más gente de la provincia después de San José, y eso "
            "cambia lo que se pide. Acá no manda la tabla de quesos ni el regalo corporativo: manda "
            "la cocina de casa, la de todos los días, la que tiene que dar de comer a varios y "
            "rendir.",

            "Ese es un cliente que nos exige otra cosa. No basta que el producto sea rico: tiene "
            "que rendir y tiene que servir para lo que la familia ya come, no para un plato de "
            "revista.",
        ],
        "angulo_h2": "Lo que sirve para la comida de todos los días",
        "angulo": [
            "La salsa de chile dulce es la que más sentido hace acá. No pica nada, aporta el sabor "
            "y el perfume del chile, y se mete dentro del plato: en un arroz, en un picadillo, en "
            "unos huevos, en un guiso. No compite con la comida, la mejora.",

            "La mayonesa de culantro hace lo mismo desde otro lado: va con casado, con pescado, con "
            "yuca, con patacones y con arroz con pollo. Es fresca y ácida, así que aligera un plato "
            "pesado en vez de cargarlo más.",

            "Y para el que sí come picante, la Habanero Fire rinde muchísimo justamente porque es "
            "intensa: media cucharadita alcanza para un plato entero. Un frasco de nivel 5 dura "
            "mucho más que uno suave, porque no hay que echarle medio frasco para que se sienta.",
        ],
        "destacados": [
            ("salsa-de-chile-dulce", "No pica. Se mete dentro de la comida de siempre."),
            ("mayonesa-de-culantro", "Para casado, pescado, yuca y patacones."),
            ("salsa-habanero-fire", "Rinde: con media cucharadita basta."),
            ("chimichurri-argentino", "Para el pollo asado y la carne del domingo."),
        ],
        "guias": [
            ("salsas-para-comida-tica", "Qué salsa va con cada plato tico"),
            ("escala-de-picante", "Del 1 al 5: cuánto pica cada una"),
        ],
        "cantones": ["Desamparados centro", "San Rafael Arriba", "San Rafael Abajo", "Gravilias",
                     "San Miguel", "Patarrá", "Damas", "San Juan de Dios", "San Antonio",
                     "Frailes", "San Cristóbal", "Rosario", "Los Guido"],
        "faq": [
            ("¿Llegan a los distritos altos, como Frailes o San Cristóbal?",
             "Sí. Para esos conviene coordinar con un día más de anticipación que para el centro "
             "del cantón, pero llegamos y al mismo precio."),
            ("¿Cuál recomiendan para cocinar, no para poner encima?",
             "La salsa de chile dulce y el chile morrón asado. Los dos se integran al plato: en "
             "arroces, picadillos, guisos y huevos."),
            ("¿Cuál rinde más?",
             "La Habanero Fire, aunque suene raro. Al ser nivel 5 con media cucharadita alcanza "
             "para un plato, así que el frasco dura mucho más que uno suave."),
            ("¿Hay algo que no pique, para los niños?",
             "La mayoría de la línea no pica: los pestos, el alioli, las mayonesas, los tomates "
             "deshidratados, el chile morrón y la salsa de chile dulce. La escala de picante lo "
             "explica producto por producto."),
        ],
    },

    {
        "slug": "salsas-artesanales-moravia",
        "nombre": "Moravia",
        "provincia": "San José",
        "provincia_slug": "salsas-artesanales-san-jose",
        "geo": "CR-SJ",
        "titulo": "Salsas Artesanales en Moravia y Tibás | Producto Hecho a Mano | CARLOUIS",
        "desc": ("Salsas, pestos y conservas artesanales con entrega en Moravia, San Vicente, "
                 "Trinidad y Tibás. Producto costarricense hecho en lotes pequeños. Entrega en 1 a "
                 "2 días."),
        "h1": "Salsas artesanales en Moravia",
        "lead": ("Entregamos en Moravia y en Tibás: San Vicente, San Jerónimo, Trinidad, y en "
                 "Tibás centro, León XIII, Colima y Anselmo Llorente."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("San Vicente de Moravia, San Jerónimo, Trinidad, Tibás centro, Cinco Esquinas, "
                    "León XIII, Colima y Anselmo Llorente son zona de entrega directa, "
                    "normalmente en 1 o 2 días hábiles."),
        "intro": [
            "Moravia tiene una relación con lo hecho a mano que muy pocos cantones tienen. Las "
            "tiendas de artesanía de San Vicente llevan décadas, y a eso no se llega por "
            "casualidad: es un lugar donde la gente entiende por qué algo hecho en cantidad pequeña "
            "cuesta distinto de algo hecho en fábrica.",

            "Para nosotros eso vale. No hay que explicar por qué un frasco de pesto hecho en lotes "
            "pequeños no cuesta lo mismo que uno importado de góndola: acá eso ya se entiende.",
        ],
        "angulo_h2": "Producto de tienda y producto de casa",
        "angulo": [
            "Por el lado de tienda, la línea completa funciona como surtido: doce productos en "
            "cinco categorías, todos de marca propia y producidos en Alajuela. Para una tienda de "
            "artesanía o de producto nacional eso arma una góndola con historia verificable, no con "
            "una etiqueta genérica.",

            "Por el lado de casa, en Moravia y Tibás pesa el pedido de despensa: pesto, alioli y "
            "tomates en aceite de oliva son los que más se repiten mes a mes. Es el cliente que "
            "compra una vez, le gusta, y vuelve por lo mismo cuando se le acaba.",

            "Tibás además es de las zonas más densas del país, con muchísima soda y panadería de "
            "barrio. Para ese tipo de negocio la salsa de chile dulce y la mayonesa de culantro son "
            "las que más rotan, porque entran en la comida que ya venden.",
        ],
        "destacados": [
            ("pesto-de-albahaca", "El que más se repite en pedidos de despensa."),
            ("alioli", "Ajo de verdad. Para papas, carnes y sándwiches."),
            ("tomates-deshidratados", "En aceite de oliva. Rinden semanas."),
            ("mayonesa-de-culantro", "Fresca y ácida. Va con casi todo lo tico."),
        ],
        "guias": [
            ("regalos-gourmet-costa-rica", "Regalos gourmet: qué llevar y qué evitar"),
            ("recetas-con-pesto", "Recetas con pesto que salen en 15 minutos"),
        ],
        "cantones": ["San Vicente de Moravia", "San Jerónimo", "La Trinidad", "Tibás centro",
                     "Cinco Esquinas", "León XIII", "Colima", "Anselmo Llorente"],
        "faq": [
            ("¿Entregan también en Tibás?",
             "Sí. Tibás centro, Cinco Esquinas, León XIII, Colima y Anselmo Llorente son zona de "
             "entrega directa igual que Moravia."),
            ("¿Venden a tiendas de artesanía o de producto nacional?",
             "Sí, y es donde mejor calza la línea completa. Doce productos de marca propia, "
             "producidos en Alajuela, con precios de mayoreo desde volúmenes pequeños."),
            ("¿Qué hace distinto un producto hecho en lotes pequeños?",
             "Que no lleva preservantes ni colorantes artificiales, porque no tiene que aguantar "
             "meses de bodega. La contra es que hay que refrigerarlo después de abrir y que cuando "
             "se acaba un lote hay que esperar el siguiente."),
            ("¿Hacen canastas de regalo?",
             "Sí. Escribinos con la cantidad y la fecha; para volúmenes conviene avisar con una "
             "semana de anticipación."),
        ],
    },

    {
        "slug": "salsas-artesanales-santo-domingo",
        "nombre": "Santo Domingo",
        "provincia": "Heredia",
        "provincia_slug": "salsas-artesanales-heredia",
        "geo": "CR-H",
        "titulo": "Salsas Artesanales en Santo Domingo y Barva, Heredia | CARLOUIS",
        "desc": ("Pestos, conservas y salsas artesanales con entrega en Santo Domingo y Barva de "
                 "Heredia. Zona de café y de producto local, a 20 minutos de donde se produce."),
        "h1": "Salsas artesanales en Santo Domingo",
        "lead": ("Entregamos en Santo Domingo y en Barva: Santa Rosa, San Vicente, San Miguel, "
                 "Tures, y en Barva centro, San Pedro, San Pablo y Santa Lucía."),
        "entrega_titulo": "A 20 minutos de donde se produce",
        "entrega": ("Santo Domingo, Santa Rosa, San Vicente, San Miguel, Tures, Barva centro, San "
                    "Pedro de Barva y San Pablo son zona de entrega rápida por la cercanía con "
                    "Alajuela. Normalmente 1 día hábil."),
        "intro": [
            "Santo Domingo y Barva son zona de café, y eso importa más de lo que parece. Donde hay "
            "cultura de café hay cultura de producto de origen: gente acostumbrada a preguntar de "
            "dónde viene algo, quién lo hizo y por qué sabe distinto de otro.",

            "Ese es el cliente más fácil que tenemos, y también el más exigente. Quien distingue un "
            "café de altura de uno comercial distingue también un pesto con albahaca de verdad de "
            "uno con espesante.",
        ],
        "angulo_h2": "Café, panadería y mesa de fin de semana",
        "angulo": [
            "Hay una cantidad de cafeterías y panaderías pequeñas entre Santo Domingo, Barva y San "
            "Pedro de Barva. Para ese tipo de negocio, los tomates deshidratados en aceite de oliva "
            "y el pesto son los que entran mejor: van en un sándwich, en una tostada, en una "
            "focaccia, y suben el ticket sin complicar la cocina.",

            "Hay algo que solo pasa en zona cafetalera: el paladar entrenado en café nota la "
            "acidez. Por eso acá la salsa de mora se vende más de lo que uno esperaría —la gente "
            "le encuentra el punto ácido igual que se lo encuentra a un café lavado— y por eso el "
            "pesto se devuelve si está oxidado.",

            "Y por la cercanía, acá es de los lugares donde más fácil resulta una entrega "
            "recurrente. Si un negocio necesita reposición cada quince días, se coordina y punto: "
            "estamos a veinte minutos.",
        ],
        "destacados": [
            ("tomates-deshidratados", "En aceite de oliva. Para tostada, sándwich y focaccia."),
            ("pesto-de-albahaca", "Albahaca de verdad. Para pastas y panes."),
            ("chile-morron-asado", "No pica. Dulce y ahumado."),
            ("salsa-de-mora", "Ácida. Para queso maduro y para postre."),
        ],
        "guias": [
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla de quesos y bocas"),
            ("recetas-con-pesto", "Recetas con pesto que salen en 15 minutos"),
        ],
        "cantones": ["Santo Domingo", "Santa Rosa", "San Vicente", "San Miguel", "Tures",
                     "Barva centro", "San Pedro de Barva", "San Pablo de Barva", "Santa Lucía"],
        "faq": [
            ("¿Cuánto tardan en entregar en Santo Domingo o Barva?",
             "Es de las zonas más rápidas que tenemos por la cercanía con Alajuela: normalmente 1 "
             "día hábil."),
            ("¿Venden a cafeterías y panaderías?",
             "Sí, y es donde mejor calzan los tomates en aceite de oliva y los pestos. Manejamos "
             "precios de mayoreo con reposición coordinada, que acá es fácil por la distancia."),
            ("¿Tienen productos aptos para vegetarianos?",
             "Sí: los pestos, los tomates deshidratados, el chile morrón asado y la salsa de chile "
             "dulce. Si hay una restricción específica, preguntá y vamos ingrediente por "
             "ingrediente."),
            ("¿Van a ferias por la zona de Heredia?",
             "Sí. Estuvimos en la Feria Holística de Ananta Yoga, en Heredia centro. Anunciamos "
             "cada feria en la página de eventos."),
        ],
    },

    {
        "slug": "salsas-artesanales-grecia",
        "nombre": "Grecia",
        "provincia": "Alajuela",
        "provincia_slug": "salsas-artesanales-alajuela",
        "geo": "CR-A",
        "titulo": "Salsas Artesanales en Grecia y Sarchí | Somos de Alajuela | CARLOUIS",
        "desc": ("Salsas de habanero, chimichurri, pestos y conservas artesanales con entrega en "
                 "Grecia, Sarchí, Naranjo y Poás. Producimos en Alajuela, a media hora. Retiro sin "
                 "costo en feria."),
        "h1": "Salsas artesanales en Grecia",
        "lead": ("Somos de Alajuela, así que Grecia nos queda cerca. Entregamos en Grecia centro, "
                 "San Isidro, Tacares, Puente de Piedra, y también en Sarchí, Naranjo y Poás."),
        "entrega_titulo": "Somos del mismo cantón vecino",
        "entrega": ("Grecia centro, San Isidro, Tacares, Puente de Piedra, San Roque, Sarchí, "
                    "Naranjo y Poás son zona de entrega directa. Y como producimos en Alajuela, "
                    "también se puede retirar sin costo el sábado en la feria."),
        "intro": [
            "Grecia, Sarchí, Naranjo y Poás son zona agrícola, y eso cambia la conversación. Acá la "
            "gente sabe de producto: sabe cuándo un tomate está de temporada, sabe distinguir un "
            "chile fresco de uno viejo, y no hay que explicarle por qué el ingrediente importa.",

            "Nosotros producimos en Alajuela y conseguimos ingredientes de la zona cuando la "
            "temporada acompaña. Frente a un cliente de Grecia eso no es discurso: es algo que "
            "puede verificar probando.",
        ],
        "angulo_h2": "Feria del agricultor y parrilla de fin de semana",
        "angulo": [
            "La feria del agricultor de Grecia es de las buenas del país. Lo que compra ahí la "
            "gente —verdura fresca, carne, queso— es justo lo que nuestras salsas acompañan. Un "
            "chimichurri de verdad con carne de la feria es otra cosa que con carne de supermercado.",

            "El chimichurri es de hecho el que más se mueve en esta zona, y tiene lógica: es zona "
            "de casa con espacio, de parrilla de fin de semana y de familia grande. Perejil, ajo y "
            "orégano de verdad, sin espesantes.",

            "Y algo que solo les podemos ofrecer a los vecinos: en vez de esperar entrega, se puede "
            "reservar por WhatsApp y retirar el sábado en la Feria Orgánica La Verbena, en Plaza "
            "Real Alajuela, de 6:00 a.m. a 1:00 p.m. Desde Grecia son unos 25 minutos, y ahí se "
            "puede probar todo antes de llevárselo.",
        ],
        "destacados": [
            ("chimichurri-argentino", "El que más se mueve acá. Para la parrilla."),
            ("salsa-habanero-fire", "Nivel 5 de 5. Probalo en la feria antes de llevarlo."),
            ("salsa-pina-habanero", "Dulce y picante. Convence al que dice que no come picante."),
            ("mayonesa-de-culantro", "Va con casi todo lo que se come acá."),
        ],
        "guias": [
            ("como-hacer-una-parrillada", "Cómo armar una parrillada que salga bien"),
            ("con-que-se-come-el-chimichurri", "Con qué se come el chimichurri"),
        ],
        "cantones": ["Grecia centro", "San Isidro", "Tacares", "Puente de Piedra", "San Roque",
                     "Sarchí", "Naranjo", "Poás", "Río Cuarto"],
        "faq": [
            ("¿Puedo retirar sin pagar envío?",
             "Sí. Reservás por WhatsApp y retirás el sábado en la Feria La Verbena, Plaza Real "
             "Alajuela, de 6:00 a.m. a 1:00 p.m. Desde Grecia son unos 25 minutos."),
            ("¿Puedo probar antes de comprar?",
             "En la feria sí, y es lo que recomendamos, sobre todo con las salsas de habanero: el "
             "nivel de picante hay que sentirlo, no leerlo."),
            ("¿Cuál recomiendan para una parrillada?",
             "El chimichurri argentino. Y si en la mesa hay quien come picante, la Habanero Fire "
             "aparte, para que cada quien se sirva."),
            ("¿Llegan a Sarchí, Naranjo y Poás?",
             "Sí, los tres son zona de entrega directa, igual que Grecia."),
        ],
    },

    {
        "slug": "salsas-artesanales-atenas",
        "nombre": "Atenas",
        "provincia": "Alajuela",
        "provincia_slug": "salsas-artesanales-alajuela",
        "geo": "CR-A",
        "titulo": "Salsas Artesanales en Atenas y Orotina | CARLOUIS",
        "desc": ("Salsas de habanero, chimichurri y conservas artesanales con entrega en Atenas, "
                 "Orotina, San Mateo y Turrúcares. A 20 minutos de donde se producen. Ideales para "
                 "casa de fin de semana."),
        "h1": "Salsas artesanales en Atenas",
        "lead": ("Entregamos en Atenas, Orotina, San Mateo y Turrúcares. Estamos a unos 20 minutos, "
                 "así que es de las entregas más rápidas que hacemos."),
        "entrega_titulo": "A 20 minutos, entrega rápida",
        "entrega": ("Atenas centro, Jesús, Mercedes, Concepción, Santa Eulalia, más Orotina, San "
                    "Mateo y Turrúcares. Por la cercanía con Alajuela normalmente es 1 día hábil, "
                    "a veces el mismo día si se coordina temprano."),
        "intro": [
            "Atenas tiene fama de tener uno de los mejores climas del país, y eso le llenó el "
            "cantón de casas de fin de semana y de gente que se vino a vivir de la ciudad. Es una "
            "mezcla particular: vecinos de toda la vida y gente que llega los viernes.",

            "Para nosotros eso se traduce en dos pedidos distintos. El de la casa que vive acá todo "
            "el año, y el del que llega el viernes con visita y necesita resolver una picada y una "
            "parrilla sin ir al supermercado.",
        ],
        "angulo_h2": "Fin de semana, parrilla y piscina",
        "angulo": [
            "El pedido de fin de semana es bastante predecible y por eso funciona bien anticiparlo: "
            "chimichurri para la carne, alioli para las papas y la yuca, y tomates en aceite de "
            "oliva con algo de queso para la picada de la tarde. Con esos tres está resuelto un "
            "sábado con gente.",

            "Con el calor de Atenas, la Piña Habanero rinde distinto que en zona fría. El perfil "
            "dulce y ácido de la piña funciona mejor con clima caliente, con cerveza y con pollo o "
            "cerdo a la parrilla, que una salsa pesada.",

            "Y por la distancia corta, si se avisa con un día se puede tener el pedido en la casa "
            "antes del viernes. Es de los pocos lugares donde eso es realista: estamos a veinte "
            "minutos.",
        ],
        "destacados": [
            ("chimichurri-argentino", "Para la carne del fin de semana."),
            ("alioli", "Para papas, yuca y patacones."),
            ("salsa-pina-habanero", "Dulce y picante. Rinde bien con el calor."),
            ("tomates-deshidratados", "En aceite de oliva. Para la picada de la tarde."),
        ],
        "guias": [
            ("como-hacer-una-parrillada", "Cómo armar una parrillada que salga bien"),
            ("que-llevar-a-un-picnic", "Qué llevar a un día de piscina o de picnic"),
        ],
        "cantones": ["Atenas centro", "Jesús", "Mercedes", "Concepción",
                     "Santa Eulalia", "Orotina", "San Mateo", "Turrúcares"],
        "faq": [
            ("¿Cuánto tardan en entregar en Atenas?",
             "Normalmente 1 día hábil, y si se coordina temprano a veces el mismo día. Estamos a "
             "unos 20 minutos."),
            ("¿Puedo pedir para tenerlo antes del fin de semana?",
             "Sí, y es lo que recomendamos: avisando con un día de anticipación llega antes del "
             "viernes sin problema."),
            ("¿Cuál va mejor con el calor?",
             "La Piña Habanero. El perfil dulce y ácido funciona mejor con clima caliente, con "
             "cerveza y con pollo o cerdo a la parrilla, que una salsa pesada."),
            ("¿Llegan a Orotina y San Mateo?",
             "Sí, los dos son zona de entrega directa igual que Atenas."),
        ],
    },

    {
        "slug": "salsas-artesanales-tres-rios",
        "nombre": "Tres Ríos",
        "provincia": "Cartago",
        "provincia_slug": "salsas-artesanales-cartago",
        "geo": "CR-C",
        "titulo": "Salsas Artesanales en Tres Ríos y La Unión, Cartago | CARLOUIS",
        "desc": ("Salsas, pestos y conservas artesanales con entrega en Tres Ríos, La Unión, San "
                 "Diego, Concepción y Curridabat este. Entrega coordinada en 1 a 2 días, sin cargo."),
        "h1": "Salsas artesanales en Tres Ríos",
        "lead": ("Entregamos en todo el cantón de La Unión: Tres Ríos, San Diego, Concepción, San "
                 "Juan, San Rafael y Dulce Nombre. Normalmente en 1 o 2 días hábiles."),
        "entrega_titulo": "Entrega coordinada en 1 a 2 días",
        "entrega": ("Tres Ríos, San Diego, Concepción, San Juan, San Rafael y Dulce Nombre de La "
                    "Unión son zona de entrega directa por la cercanía con el GAM, aunque el "
                    "cantón sea de Cartago."),
        "intro": [
            "La Unión es un caso raro: pertenece a Cartago pero funciona como parte del este de "
            "San José. Tres Ríos está más cerca de Curridabat que de Cartago centro, y eso hace que "
            "sea zona de entrega directa aunque en el mapa esté en otra provincia.",

            "Es un cantón que creció rápido con condominios y casas nuevas, así que hay mucha "
            "familia joven cocinando y también bastante gente que trabaja en San José y llega "
            "tarde. Las dos cosas empujan al mismo tipo de compra: algo que resuelva rápido y sepa "
            "bien.",
        ],
        "angulo_h2": "Cerca de Cartago, con lo mejor de los dos lados",
        "angulo": [
            "Por el lado de Cartago, acá aplica lo mismo que en toda esa provincia: el queso "
            "Turrialba está a mano, y los tomates deshidratados en aceite de oliva con el chile "
            "morrón asado son el mejor acompañante simple que existe para queso fresco.",

            "Por el lado del GAM, pesa la cocina de entre semana: pestos y mayonesas saborizadas, "
            "que convierten una pasta o un sándwich en algo distinto sin cocinar nada más.",

            "Y hay un detalle de clima que vale: Tres Ríos es más frío que San José centro. El frío "
            "juega a favor del picante —se disfruta distinto cuando afuera están a 18 grados— y a "
            "favor de la comida de olla, que es donde una salsa con carácter luce más.",
        ],
        "destacados": [
            ("chile-morron-asado", "Con queso Turrialba fresco es imbatible."),
            ("pesto-de-albahaca", "Una pasta lista en lo que hierve el agua."),
            ("mayonesa-de-chipotle", "Ahumada. Para sándwich y hamburguesa."),
            ("salsa-habanero-fire", "El frío de acá le queda bien al picante."),
        ],
        "guias": [
            ("salsas-para-comida-tica", "Qué salsa va con cada plato tico"),
            ("tabla-de-quesos-y-bocas", "Cómo armar una tabla de quesos y bocas"),
        ],
        "cantones": ["Tres Ríos", "San Diego", "Concepción", "San Juan", "San Rafael",
                     "Dulce Nombre", "Río Azul"],
        "faq": [
            ("¿Tres Ríos es Cartago o San José?",
             "Es el cantón de La Unión, provincia de Cartago, aunque funcione como parte del este "
             "de San José. Para nosotros es zona de entrega directa: 1 o 2 días hábiles."),
            ("¿Qué recomiendan para acompañar queso Turrialba?",
             "Los tomates deshidratados en aceite de oliva y el chile morrón asado. Los dos son "
             "suaves y le dan acidez y dulzor sin tapar el queso fresco."),
            ("¿Llegan a los condominios de la zona?",
             "Sí. Coordinamos por WhatsApp el día y la franja; si el condominio pide dejar en "
             "caseta, también se puede."),
            ("¿Hacen envíos al resto de Cartago?",
             "Sí, a los 8 cantones. Cartago centro y La Unión son entrega coordinada; a Paraíso, "
             "Turrialba, Oreamuno y los demás va por encomienda en 2 a 4 días."),
        ],
    },
]
