# -*- coding: utf-8 -*-
"""Contenido de las guías. Cada una ataca una búsqueda informativa que la
gente hace ANTES de comprar, y desde ahí enlaza a los productos.

Los competidores no cubren ninguna de estas: venden el frasco pero no
responden qué hacer con él.
"""

GUIAS = [
    dict(
        slug="con-que-se-come-el-chimichurri",
        titulo="Con qué se come el chimichurri: 9 formas más allá de la carne",
        h1="Con qué se come el chimichurri",
        desc="Nueve formas de usar el chimichurri además de la carne asada: papas, pan, vegetales, pastas y marinadas. Guía práctica de CARLOUIS, Costa Rica.",
        img="chimichurri", w=849, h=637,
        lede="Todo el mundo sabe que el chimichurri va con carne. Lo que casi nadie "
             "aprovecha es todo lo demás que puede hacer un buen frasco.",
        intro=[
            "El chimichurri nació como salsa de parrilla argentina y en Costa Rica se quedó "
            "encasillado ahí: sale del refrigerador cuando hay asado y vuelve a entrar hasta "
            "el siguiente. Es un desperdicio.",
            "Es una emulsión de hierbas, ajo, vinagre y aceite de oliva. Eso es exactamente lo "
            "que hace funcionar a un aliño, a una marinada y a media docena de preparaciones "
            "que no tienen nada que ver con la parrilla.",
        ],
        secciones=[
            ("Lo clásico, pero bien hecho", [
                ("Sobre la carne ya servida", "Este es el error más común: echarlo durante la cocción. El calor evapora el vinagre y quema las hierbas. El chimichurri va <strong>encima del corte ya en el plato</strong>, cuando todavía está caliente pero fuera del fuego. Una cucharada por porción."),
                ("Como marinada, aparte", "Si querés marinar, usá una porción distinta a la que vas a servir. Pollo o cerdo, dos horas mínimo en refrigeración. Nunca reutilicés la marinada como salsa."),
            ]),
            ("Donde casi nadie lo usa", [
                ("Papas asadas", "Sacá las papas del horno y revolvelas de inmediato con dos cucharadas. El calor abre las hierbas y el aceite se pega a la papa. Es de las mejores cosas que se pueden hacer con un frasco."),
                ("Pan tostado con queso fresco", "Tostada, una capa fina de queso fresco o ricotta, y chimichurri encima. Entrada de tres ingredientes que parece de restaurante."),
                ("Vegetales a la parrilla", "Berenjena, zucchini y chile dulce. Se asan a fuego fuerte y se bañan al salir. El vinagre corta la dulzura del vegetal asado."),
                ("Huevos", "Revueltos o estrellados, una cucharadita al final. Cambia por completo un desayuno de siempre."),
                ("Pastas frías", "Con pasta corta, tomate y mozzarella. Funciona como pesto pero con más acidez."),
                ("Sándwich de carne fría", "En lugar de mostaza o mayonesa. Va especialmente bien con roast beef."),
                ("Arroz", "Una cucharada al arroz blanco recién hecho, revuelto con el tenedor. El más barato de los trucos y de los que más impresiona."),
            ]),
        ],
        faq=[
            ("¿El chimichurri se calienta?",
             "No. Se sirve a temperatura ambiente sobre la comida caliente. Al calentarlo se evapora el vinagre y las hierbas se amargan."),
            ("¿Cuánto dura abierto?",
             "Refrigerado, varias semanas. Si el aceite de oliva se solidifica en frío, dejá el frasco unos minutos afuera y vuelve a su textura normal."),
            ("¿El chimichurri pica?",
             "El clásico argentino no pica: su sabor viene de las hierbas, el ajo y el vinagre. Si lo querés picante, combinalo con una salsa de habanero aparte."),
            ("¿Sirve para pescado?",
             "Sí, pero con moderación. Es una salsa intensa y puede tapar un pescado blanco suave. Va mejor con pescados grasos como el atún."),
        ],
        productos=["chimichurri-argentino", "chile-morron-asado", "alioli"],
        cta="¿Querés probar un chimichurri hecho a mano?",
    ),

    dict(
        slug="escala-de-picante",
        titulo="Escala de picante: cuál salsa elegir según lo que aguantás",
        h1="Cuál salsa picante elegir",
        desc="Guía para elegir salsa picante según tu tolerancia: del nivel 1 al 5, con qué comida va cada una. Salsas artesanales hechas en Costa Rica.",
        img="habanero-fire-160", w=1086, h=1448,
        lede="Comprar picante a ciegas es una lotería. Esta es nuestra escala del 1 al 5 y "
             "qué esperar de cada nivel.",
        intro=[
            "La mayoría de las salsas del supermercado no dicen cuánto pican, o usan palabras "
            "sin referencia: «extra hot», «suave», «picante». No sirve de nada si no sabés "
            "contra qué se compara.",
            "Nosotros clasificamos cada salsa del 1 al 5 y lo ponemos en la etiqueta y en la "
            "página. Así sabés qué estás comprando antes de abrirlo.",
        ],
        secciones=[
            ("Los cinco niveles", [
                ("Nivel 1 · Apenas se siente", "El picor aparece al final y desaparece rápido. Cualquiera lo come, incluso quien dice que no aguanta nada. Acá está la <a href='salsa-de-chile-dulce.html'>Salsa de Chile Dulce</a>."),
                ("Nivel 2 · Picante suave", "Se siente claro pero no interrumpe la comida. Es el nivel más popular porque nadie en la mesa lo rechaza. Acá está la <a href='mayonesa-de-chipotle.html'>Mayonesa de Chipotle</a>."),
                ("Nivel 3 · Picante medio", "Ya hay que respetarlo. Pica de verdad pero el sabor sigue por delante del ardor. Acá está la <a href='salsa-pina-habanero.html'>Piña Habanero</a>."),
                ("Nivel 4 · Fuerte", "Para gente acostumbrada. El picor dura y se acumula bocado a bocado."),
                ("Nivel 5 · Muy picante", "Habanero de frente, sin azúcar que lo suavice. Unas gotas alcanzan. Acá está <a href='salsa-habanero-fire.html'>Habanero Fire</a>."),
            ]),
            ("Cómo elegir sin equivocarte", [
                ("Si nunca comprás picante", "Empezá en nivel 2. Es el que más gente disfruta y el que menos se queda guardado en la refrigeradora."),
                ("Si te gusta el picante pero no sos fanático", "Nivel 3. Tiene carácter sin arruinarte el plato si te pasás con la cucharada."),
                ("Si te quejás de que nada pica", "Nivel 5 directo. Es el que hicimos para ustedes."),
                ("Si van a comer varias personas", "Llevá dos: una de nivel 2 para la mesa y una de nivel 5 aparte. Así cada quien se sirve lo suyo."),
            ]),
            ("Qué hacer si te pasaste", [
                ("Lácteos, no agua", "El agua reparte la capsaicina por toda la boca y empeora la sensación. Leche, yogur o queso la disuelven."),
                ("Algo con almidón", "Pan, arroz o tortilla absorben y bajan el ardor."),
                ("Nunca cerveza fría", "El alcohol y el frío alivian por segundos y después vuelve peor."),
            ]),
        ],
        faq=[
            ("¿Cuál es la salsa más picante de CARLOUIS?",
             "Habanero Fire, nivel 5 de 5. Está hecha con chile habanero seleccionado y sin azúcar que suavice el golpe."),
            ("¿Cuál recomiendan para alguien que no come picante?",
             "La Mayonesa de Culantro, que no pica nada, o la Salsa de Chile Dulce, que es nivel 1 y predomina el dulce."),
            ("¿El picante se puede acostumbrar?",
             "Sí. La tolerancia a la capsaicina sube con la exposición. Mucha gente que empezó en nivel 2 termina comprando nivel 5 al año siguiente."),
            ("¿Qué diferencia hay entre chipotle y habanero?",
             "El chipotle es jalapeño ahumado: pica menos y aporta sabor ahumado. El habanero pica bastante más y tiene un aroma afrutado característico."),
        ],
        productos=["salsa-habanero-fire", "salsa-pina-habanero", "mayonesa-de-chipotle"],
        cta="Elegí tu nivel y pedila",
    ),

    dict(
        slug="como-conservar-salsas-artesanales",
        titulo="Cómo conservar salsas artesanales sin preservantes",
        h1="Cómo conservar salsas artesanales",
        desc="Guía para conservar salsas, pestos y conservas artesanales sin preservantes: refrigeración, cuánto duran y cómo saber si algo se dañó.",
        img="pesto-albahaca", w=820, h=615,
        lede="Un producto sin preservantes se cuida distinto a uno de supermercado. "
             "Esto es lo que hay que saber para que te dure.",
        intro=[
            "Las salsas industriales aguantan meses en la alacena porque llevan preservantes, "
            "acidulantes y a veces conservadores químicos. Las artesanales no llevan nada de "
            "eso, y por eso saben distinto.",
            "El precio de esa diferencia es que hay que tratarlas bien. No es complicado: son "
            "tres reglas.",
        ],
        secciones=[
            ("Las tres reglas", [
                ("Refrigerar siempre después de abrir", "No es una sugerencia. Sin preservantes, el frasco abierto a temperatura ambiente empieza a cambiar en días. Cerrado y en frío, semanas."),
                ("Cuchara limpia, siempre", "Es la causa número uno de que un frasco se dañe antes de tiempo. Meter una cuchara usada introduce bacterias y restos de comida. Usá una limpia cada vez."),
                ("Mantener el producto cubierto de aceite", "En los productos conservados en aceite —<a href='tomates-deshidratados.html'>tomates deshidratados</a>, <a href='chile-morron-asado.html'>chile morrón asado</a>— el aceite es la barrera. Si algo queda asomado, se daña primero. Empujalo hacia abajo antes de guardar."),
            ]),
            ("Cuánto dura cada tipo", [
                ("Salsas picantes", "Son las más resistentes: el chile y el vinagre trabajan a favor. Refrigeradas, varias semanas sin problema."),
                ("Pestos", "Más delicados por la albahaca fresca. Consumir en un par de semanas. Se congelan muy bien: en cubetera de hielo, un cubo por porción."),
                ("Cremas y mayonesas", "Las más sensibles. Refrigeración estricta y consumo más pronto. Nunca las dejés fuera de la refri durante una comida larga."),
                ("Conservas en aceite", "Las más duraderas, siempre que el producto quede cubierto por el aceite."),
            ]),
            ("Cómo saber si algo se dañó", [
                ("El olor primero", "Es el aviso más confiable. Si huele agrio, fermentado o simplemente raro, no lo pruebes."),
                ("Burbujas o espuma", "Señal de fermentación. Se descarta."),
                ("Cambio de color notorio", "Que el pesto se oscurezca un poco en la superficie por contacto con el aire es normal. Que cambie de color en todo el frasco, no."),
                ("Ante la duda, se bota", "Un frasco cuesta menos que una intoxicación."),
            ]),
            ("Preguntas de aceite frío", [
                ("El aceite se puso sólido y blanco", "Es normal. El aceite de oliva solidifica en frío y se ve turbio o con grumos blancos. No es que se dañó. Dejá el frasco 10 minutos a temperatura ambiente y vuelve a su estado."),
                ("¿Se puede volver a refrigerar?", "Sí, cuantas veces haga falta. El aceite de oliva soporta ese ciclo sin problema."),
            ]),
        ],
        faq=[
            ("¿Por qué las salsas artesanales necesitan refrigeración y las de supermercado no?",
             "Porque las industriales llevan preservantes y conservadores que las estabilizan a temperatura ambiente. Las artesanales no llevan aditivos, así que dependen del frío."),
            ("¿Se pueden congelar?",
             "Los pestos sí, y muy bien: en cubetera de hielo, sacando un cubo por porción. Las mayonesas y cremas no se recomiendan porque la emulsión se corta al descongelar."),
            ("El aceite de mi frasco se puso blanco y sólido, ¿se dañó?",
             "No. Es el comportamiento normal del aceite de oliva en frío. Dejalo unos minutos afuera y recupera su textura."),
            ("¿Cuánto dura un frasco sin abrir?",
             "Bastante más que uno abierto, pero igual recomendamos refrigeración. Consultanos por WhatsApp por el lote específico que llevaste."),
        ],
        productos=["pesto-de-albahaca", "tomates-deshidratados", "alioli"],
        cta="Pedí productos frescos, hechos en lotes pequeños",
    ),
]
