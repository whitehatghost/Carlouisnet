# -*- coding: utf-8 -*-
"""Contenido extra de las fichas de producto, para búsqueda.

Por qué existe este archivo aparte de productos.py: las fichas tenían entre
263 y 368 palabras, que es muy poco para competir, y además les faltaban los
sinónimos con los que la gente busca de verdad. Un ejemplo real: la ficha de
tomates deshidratados no decía "tomate seco" ni "tomate en aceite" ni una sola
vez, y así es como medio país los llama.

"otros_nombres" no es relleno de palabras clave: se imprime como una línea
visible y útil ("también se conoce como..."), porque el que busca "tomate seco"
y cae acá necesita confirmar en dos segundos que llegó al producto correcto.

"contexto" son tres párrafos que enseñan algo de verdad sobre el producto.
Si alguna vez hay que recortar, se recorta el número de productos cubiertos,
nunca la honestidad de lo que dicen estos párrafos.
"""

SEO = {

    "tomates-deshidratados": {
        "title": "Tomate Seco y Deshidratado en Aceite de Oliva | Costa Rica | CARLOUIS",
        "desc": ("Tomate seco artesanal conservado en aceite de oliva, hecho en Costa Rica. "
                 "También llamado tomate deshidratado o tomate en aceite. Para pastas, bruschettas "
                 "y tablas. Frasco de ₡6.000 con envío a todo el país."),
        "otros_nombres": ["tomate seco", "tomates secos", "tomate deshidratado en aceite",
                          "tomate en aceite de oliva", "tomate confitado", "sun-dried tomato"],
        "contexto_h2": "Qué es un tomate deshidratado en aceite",
        "contexto": [
            "Deshidratar un tomate no es secarlo y ya: es sacarle el agua despacio hasta que lo que "
            "queda sea puro sabor concentrado. Un tomate fresco es más del 90% agua. Cuando esa agua "
            "se va, el azúcar natural y el ácido se quedan, y el resultado es algo mucho más intenso "
            "y más dulce que el tomate del que salió. Por eso un frasco pequeño rinde tanto.",

            "Después van conservados en aceite de oliva, y ahí pasan dos cosas. La primera es que se "
            "ablandan, así que no hay que hidratarlos: se comen directo del frasco. La segunda es que "
            "el aceite se lleva parte del sabor del tomate, del ajo y de las hierbas. Ese aceite no se "
            "bota nunca: sirve para saltear, para aliñar una ensalada o para mojar pan.",

            "En Costa Rica se les dice de varias formas —tomate seco, tomate deshidratado, tomate en "
            "aceite— y son lo mismo. Lo que sí cambia entre marcas es de dónde viene el tomate y cuánto "
            "aceite de relleno lleva el frasco. Nosotros los hacemos en Alajuela, en lotes pequeños, y "
            "sin colorantes ni preservantes artificiales. Por eso hay que refrigerarlos después de "
            "abrir, y por eso también se acaban cuando se acaba el lote.",
        ],
    },

    "chimichurri-argentino": {
        "title": "Chimichurri Argentino Artesanal en Costa Rica | CARLOUIS",
        "desc": ("Chimichurri argentino artesanal hecho en Costa Rica con perejil, ajo, orégano y "
                 "aceite de oliva. Para asados, carne a la parrilla y pollo. Sin aditivos, frasco "
                 "de ₡5.000 con envío a todo el país."),
        "otros_nombres": ["chimichurri argentino", "salsa chimichurri", "chimichurri para asado",
                          "chimichurri casero", "chimichurri para carne"],
        "contexto_h2": "Qué lleva un chimichurri argentino de verdad",
        "contexto": [
            "Un chimichurri argentino es una cosa bastante simple y bastante estricta: perejil, ajo, "
            "orégano, vinagre, aceite y sal. No lleva tomate, no lleva culantro y no lleva chile "
            "picante. Todo lo que se le agregue de más deja de ser chimichurri y pasa a ser otra cosa, "
            "que puede estar muy buena, pero no es lo que pide alguien que busca chimichurri.",

            "El perejil es el que manda. Tiene que ser perejil de verdad y en cantidad, porque es lo "
            "que da el color verde y ese amargor limpio que corta la grasa de la carne. Ahí está la "
            "gracia del chimichurri: no es una salsa para tapar el sabor de un corte, es para "
            "equilibrarlo. Por eso funciona tan bien con carne gorda y con achuras.",

            "En Costa Rica el chimichurri llegó de la mano del asado argentino y se quedó, pero mucho "
            "de lo que se vende acá es industrial y viene con espesantes. El nuestro se hace en "
            "Alajuela en lotes pequeños, con aceite de oliva y sin aditivos. Si nunca lo has usado, "
            "dejalo 10 minutos sobre la carne recién salida de la parrilla antes de servir: el calor "
            "abre las hierbas y cambia por completo.",
        ],
    },

    "salsa-habanero-fire": {
        "otros_nombres": ["salsa de chile habanero", "salsa picante fuerte", "hot sauce",
                          "salsa picante artesanal", "chile habanero"],
        "contexto_h2": "Qué tan picante es un habanero",
        "contexto": [
            "El chile habanero anda entre 100.000 y 350.000 unidades Scoville. Para tener una "
            "referencia: un jalapeño anda entre 2.500 y 8.000. O sea que un habanero puede picar "
            "cuarenta veces más que un jalapeño. No es una exageración de etiqueta, es el rango real "
            "del chile.",

            "Pero el habanero no es solo ardor, y eso es lo que mucha gente no sabe hasta que lo "
            "prueba bien hecho. Tiene un aroma afrutado, casi cítrico, que aparece antes que el "
            "picante. Cuando una salsa de habanero está bien hecha uno siente primero ese perfume y "
            "después llega el golpe. Cuando está mal hecha, solo arde.",

            "Esta es la más intensa de nuestra línea: nivel 5 de 5, sin azúcar que le baje el filo. "
            "Si es tu primera vez con habanero, empezá con media cucharadita mezclada dentro de la "
            "comida en vez de ponerla encima. Y si querés el sabor sin tanto golpe, la Piña Habanero "
            "es el mismo chile con dulzor de piña que lo redondea.",
        ],
    },

    "salsa-pina-habanero": {
        "otros_nombres": ["salsa de piña picante", "salsa agridulce picante",
                          "hot sauce de piña", "salsa tropical picante"],
        "contexto_h2": "Por qué la piña y el habanero funcionan juntos",
        "contexto": [
            "El azúcar y el ácido de la piña hacen dos cosas con el picante del habanero. Primero lo "
            "redondean: el golpe llega más tarde y se va más rápido, así que no domina el plato. "
            "Segundo lo alargan: el sabor afrutado del habanero se junta con el de la piña y se "
            "amplifica, en vez de quedar tapado por el ardor.",

            "Por eso esta es la salsa que convence a quien dice que no come picante. No es que pique "
            "poco —lleva habanero de verdad— es que pica de otra forma, con algo dulce por delante "
            "que da tiempo de disfrutar el sabor antes del calor.",

            "Con qué va mejor: pescado, camarón, cerdo y pollo. Con marisco especialmente, porque la "
            "acidez cumple el mismo papel que el limón. Es la que más se pide en las provincias "
            "costeras, y tiene sentido: en Guanacaste y Puntarenas es la que se va con el ceviche y "
            "con el pescado entero.",
        ],
    },

    "alioli": {
        "title": "Alioli Artesanal de Ajo | Hecho en Costa Rica | CARLOUIS",
        "otros_nombres": ["allioli", "aioli", "ajoaceite", "salsa de ajo", "crema de ajo"],
        "contexto_h2": "Qué es el alioli y en qué se diferencia de la mayonesa",
        "contexto": [
            "Alioli viene del catalán all i oli, que significa literalmente ajo y aceite. En su "
            "versión más pura es exactamente eso: ajo machacado y aceite emulsionados a fuerza de "
            "mortero, sin huevo. Es una de las salsas más viejas del Mediterráneo y una de las más "
            "difíciles de hacer bien, porque la emulsión se corta con nada.",

            "La diferencia con la mayonesa es el protagonista. En una mayonesa el ajo es un detalle; "
            "en un alioli el ajo es el plato. Se siente el picor del ajo crudo, esa punta que raspa "
            "un poco al final, y eso es justamente lo que se busca. Un alioli que no sepa a ajo "
            "fracasó.",

            "Se usa con papas —es el acompañante clásico de las papas bravas—, con carnes a la "
            "parrilla, en un sándwich, con vegetales asados o con pan. En Costa Rica funciona "
            "particularmente bien con yuca frita y con patacones. Va en frasco, se hace en Alajuela "
            "en lotes pequeños y hay que refrigerarlo después de abrir.",
        ],
    },

    "pesto-de-albahaca": {
        "otros_nombres": ["pesto genovés", "salsa pesto", "pesto casero", "pesto verde",
                          "pesto de basilico"],
        "contexto_h2": "Qué distingue a un pesto de albahaca",
        "contexto": [
            "El pesto nació en Génova y el nombre viene de pestare, machacar. Eso importa más de lo "
            "que parece: un pesto machacado y un pesto licuado no saben igual. Al machacar se rompen "
            "las hojas y sueltan aceite; al licuar a alta velocidad el metal calienta la albahaca y "
            "la oxida, y ahí aparece ese sabor herbáceo apagado y ese color verde opaco.",

            "Los ingredientes de un pesto son pocos: albahaca, ajo, queso, fruto seco, aceite de oliva "
            "y sal. Con tan poco, no hay dónde esconder un ingrediente malo. Una albahaca vieja o un "
            "aceite flojo se notan de inmediato, y por eso el pesto es de las cosas más honestas que "
            "se pueden comprar: uno sabe enseguida si está bien hecho.",

            "Lo más importante al usarlo: el pesto no se cocina. Se mezcla con la pasta fuera del "
            "fuego, con un poco del agua de cocción para que ligue. Si lo ponés en la sartén caliente "
            "perdés el aroma, que es todo lo que estabas pagando. Lo mismo vale para pizza: va encima "
            "al salir del horno, no antes.",
        ],
    },

    "pesto-de-tomate": {
        "title": "Pesto de Tomate Artesanal | Pesto Rosso en Costa Rica | CARLOUIS",
        "otros_nombres": ["pesto rosso", "pesto rojo", "pesto de tomate seco",
                          "salsa pesto de tomate"],
        "contexto_h2": "Pesto rosso: el hermano rojo del pesto",
        "contexto": [
            "En Italia se le dice pesto rosso y es originario del sur, de Sicilia, mientras que el "
            "pesto verde es del norte. La lógica es la misma —machacar los ingredientes en vez de "
            "cocinarlos— pero el protagonista cambia: en vez de albahaca fresca, tomate concentrado.",

            "El resultado es una salsa más dulce, más densa y menos herbácea que el pesto verde. "
            "Tiene la acidez del tomate pero sin el agua, así que no aguada la pasta. Y aguanta "
            "mejor el calor que el pesto de albahaca, aunque igual recomendamos mezclarlo fuera del "
            "fuego.",

            "Dónde funciona mejor: en pastas cortas que atrapan la salsa, sobre pan tostado con queso "
            "crema o ricotta, dentro de un sándwich, o como base de una pizza en vez de salsa de "
            "tomate común. También es el que mejor recibe quien encuentra el pesto de albahaca "
            "demasiado intenso.",
        ],
    },

    "mayonesa-de-chipotle": {
        "otros_nombres": ["mayonesa chipotle", "salsa chipotle", "chipotle mayo",
                          "mayonesa ahumada", "aderezo de chipotle"],
        "contexto_h2": "Qué es el chipotle y por qué sabe a ahumado",
        "contexto": [
            "El chipotle no es una variedad de chile: es un jalapeño maduro que se dejó secar al humo. "
            "Ese es todo el truco. El jalapeño verde que uno conoce es el mismo chile joven; cuando se "
            "deja madurar se pone rojo, y cuando ese rojo se ahúma nace el chipotle. Por eso sabe a "
            "humo y por eso el picante es más redondo y menos filoso.",

            "Mezclado en una mayonesa, ese ahumado es lo que hace todo el trabajo. El picante queda en "
            "un nivel medio —cómodo para casi todo el mundo— y lo que domina es el sabor tostado, que "
            "es justo lo que le falta a un sándwich o a una hamburguesa hecha en casa.",

            "Es de las más versátiles de la línea: papas fritas, hamburguesas, sándwiches, pollo, "
            "tacos, vegetales asados, y como dip. Si buscás algo con carácter pero que nadie en la "
            "mesa deje de comer, esta es la respuesta más segura de las que tenemos.",
        ],
    },

    "mayonesa-de-culantro": {
        "title": "Mayonesa de Culantro Artesanal | Costa Rica | CARLOUIS",
        "otros_nombres": ["mayonesa de cilantro", "salsa de culantro", "cilantro mayo",
                          "aderezo de culantro", "mayonesa verde"],
        "contexto_h2": "Culantro, cilantro y culantro coyote",
        "contexto": [
            "Acá vale aclarar los nombres, porque confunden hasta a quien cocina seguido. Lo que en "
            "Costa Rica llamamos culantro es lo que en México y España llaman cilantro: la hoja "
            "pequeña y redondeada. El culantro coyote es otra planta distinta, de hoja larga y "
            "dentada, con un sabor mucho más fuerte. Esta mayonesa lleva culantro del común.",

            "El culantro tiene una cosa curiosa: hay gente que genéticamente lo percibe con sabor a "
            "jabón. Es real, está estudiado, y ronda un porcentaje pequeño de la población. Si sos de "
            "esa gente, ninguna mayonesa de culantro te va a gustar y conviene irse por el alioli o "
            "por la de chipotle.",

            "Para el resto, es probablemente la salsa que mejor calza con la comida costarricense de "
            "diario. Va con casado, con pescado, con arroz con pollo, con chifrijo, con yuca y con "
            "patacones. Es fresca y ácida, así que aligera platos pesados en vez de cargarlos más.",
        ],
    },

    "chile-morron-asado": {
        "title": "Chile Morrón Asado en Conserva | Pimiento Asado Costa Rica | CARLOUIS",
        "otros_nombres": ["pimiento asado", "pimiento morrón asado", "chile dulce asado",
                          "pimientos en conserva", "roasted pepper"],
        "contexto_h2": "Por qué asar un chile morrón le cambia el sabor",
        "contexto": [
            "Asar un chile morrón hasta que la piel se quema y se desprende hace dos cosas. La "
            "primera es que concentra el azúcar natural del chile, y ahí es donde aparece esa dulzura "
            "que el morrón crudo no tiene. La segunda es que el fuego le deja un dejo ahumado que "
            "ninguna otra técnica logra.",

            "También cambia la textura por completo. El morrón crudo es crujiente y un poco áspero; "
            "el asado y pelado queda sedoso, casi como carne. Esa textura es la razón por la que "
            "funciona tan bien en una tabla o en un sándwich, donde un vegetal crudo se sentiría "
            "fuera de lugar.",

            "No pica nada —el chile morrón, o chile dulce, no tiene capsaicina apreciable— así que "
            "entra en cualquier mesa. Con queso Turrialba fresco es de las mejores combinaciones "
            "simples que hay en el país: el dulzor ahumado del chile contra la acidez láctea del "
            "queso, con un pan decente y nada más.",
        ],
    },

    "salsa-de-chile-dulce": {
        "otros_nombres": ["salsa de pimiento", "salsa de chile dulce casera",
                          "salsa de morrón", "salsa dulce sin picante"],
        "contexto_h2": "Sabor de chile sin nada de picante",
        "contexto": [
            "Hay una confusión que vale aclarar para quien no es de acá: en Costa Rica chile dulce es "
            "el pimiento, el morrón, el bell pepper. No pica. La palabra chile en el nombre asusta a "
            "más de uno, pero esta salsa tiene cero capsaicina.",

            "Y ese es exactamente su papel en la línea. Cuando en una mesa hay gente que no come "
            "picante —niños, adultos mayores, o simplemente quien no lo disfruta— esta es la que "
            "permite que igual haya algo con sabor. Aporta el dulzor y el perfume del chile sin una "
            "gota de ardor.",

            "Funciona dentro de la comida más que encima: en un arroz, en un picadillo, en un guiso, "
            "en unos huevos revueltos. Es de las que más se piden para cocina de casa y de soda, "
            "porque se integra al plato en vez de competir con él.",
        ],
    },

    "salsa-de-mora": {
        "otros_nombres": ["salsa de frutos rojos", "salsa agridulce de mora",
                          "mermelada de mora artesanal", "blackberry sauce"],
        "contexto_h2": "Una salsa dulce que también va con salado",
        "contexto": [
            "La mora costarricense es más ácida que la mora de otros lados, y eso acá juega a favor. "
            "Una salsa de fruta demasiado dulce empalaga y solo sirve para postre; con la acidez de la "
            "mora de altura la salsa se sostiene sola y puede entrar en un plato salado sin volverlo "
            "un dulce.",

            "Ahí está lo que mucha gente no espera: esta salsa funciona con carnes. Con cerdo "
            "especialmente, y con pato, con pollo horneado y con quesos maduros o azules. Es el mismo "
            "principio de la salsa de arándano con el pavo: la fruta ácida corta la grasa y limpia el "
            "paladar entre bocado y bocado.",

            "Y claro, también hace lo obvio: sobre helado, sobre panqueques, sobre cheesecake, con "
            "yogur o con pan. Es la más versátil entre dulce y salado de toda la línea, y la que más "
            "sorprende a quien la prueba por primera vez en una tabla de quesos.",
        ],
    },
}
