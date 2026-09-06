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

GUIAS += [
    dict(
        slug="recetas-con-pesto",
        titulo="Recetas con pesto: 8 formas de usarlo además de la pasta",
        h1="Qué hacer con un frasco de pesto",
        desc="Ocho formas de usar el pesto además de la pasta: pizza, pollo, sándwiches, papas y sopas. Con el truco para que no se corte. Guía de CARLOUIS, Costa Rica.",
        img="pesto-albahaca", w=820, h=615,
        lede="El pesto no es solo para pasta, y además casi todo el mundo lo usa mal. "
             "Empecemos por ahí.",
        intro=[
            "El error más común con el pesto es echarlo a la olla. El calor directo separa el "
            "aceite, oscurece la albahaca y mata el aroma, que es justamente por lo que se paga "
            "un pesto bueno.",
            "La regla es simple: <strong>el pesto entra siempre con el fuego apagado</strong>. "
            "A partir de ahí, todo lo demás es fácil.",
        ],
        secciones=[
            ("El truco que cambia todo", [
                ("Guardá agua de la pasta", "Antes de escurrir, apartá media taza del agua de cocción. Tiene almidón, y ese almidón es lo que hace que el pesto se pegue al fideo en vez de resbalarse al fondo del plato."),
                ("Apagá el fuego primero", "Pasta escurrida de vuelta a la olla, fuera del fuego. Dos cucharadas de pesto por porción, un chorrito del agua reservada, y revolvés hasta que quede cremoso."),
                ("Nunca lo hiervas", "Si el pesto burbujea, ya perdiste el aroma. Lo que queda es aceite con hierbas cocidas."),
            ]),
            ("Las otras siete formas", [
                ("Pizza casera", "Como base en lugar de salsa de tomate, o en cucharadas al salir del horno. El <a href=\'pesto-de-tomate.html\'>pesto de tomate</a> funciona mejor de base porque es más espeso y no humedece la masa."),
                ("Pollo al horno", "Metelo debajo de la piel antes de hornear. Se cocina protegido y perfuma toda la carne."),
                ("Sándwiches y tostadas", "En lugar de mayonesa. Con tomate y mozzarella es un caprese en pan."),
                ("Papas", "Recién salidas del agua o del horno, revueltas en caliente. El almidón de la papa hace lo mismo que el agua de pasta."),
                ("Sopas y cremas", "Una cucharada encima de una crema de vegetales, sin revolver. Se deshace sola al comerla."),
                ("Huevos", "Revueltos, al final. O sobre un huevo poché con pan tostado."),
                ("Aderezo de ensalada", "Una cucharada de pesto, dos de aceite de oliva y el jugo de medio limón. Se bate y rinde para toda la ensaladera."),
            ]),
        ],
        faq=[
            ("¿Por qué el pesto se pone amargo al cocinarlo?",
             "Porque el calor directo degrada los aceites de la albahaca. Por eso el pesto se agrega siempre fuera del fuego, sobre la comida caliente."),
            ("¿Cuál pesto uso para pizza, el de albahaca o el de tomate?",
             "El de tomate como base, porque es más espeso y no humedece la masa. El de albahaca queda mejor agregado al salir del horno."),
            ("¿Se puede congelar el pesto?",
             "Sí, y es la mejor forma de estirar un frasco. En cubetera de hielo: un cubo por porción, se descongela a temperatura ambiente."),
            ("¿Cuánto pesto va por porción de pasta?",
             "Dos cucharadas colmadas por persona. El de tomate rinde un poco más: con una cucharada y media alcanza."),
        ],
        productos=["pesto-de-albahaca", "pesto-de-tomate", "tomates-deshidratados"],
        cta="Pedí tu pesto hecho en lotes pequeños",
    ),

    dict(
        slug="salsas-para-comida-tica",
        titulo="Qué salsa va con cada comida tica: casados, gallos y chifrijo",
        h1="Salsas para la comida tica",
        desc="Qué salsa artesanal va mejor con casados, gallos, chifrijo, tacos y ceviche. Guía de maridaje para la comida costarricense hecha por CARLOUIS.",
        img="mayo-culantro", w=772, h=579,
        lede="La comida tica pide salsas distintas a las de las recetas de afuera. "
             "Esto es lo que funciona de verdad en una mesa costarricense.",
        intro=[
            "En Costa Rica se come mucho arroz, mucho frijol y mucha carne a la plancha. Son "
            "sabores que no necesitan que los tapen: necesitan algo que los levante.",
            "Después de años en la feria escuchando qué se llevan los clientes y para qué, esto "
            "es lo que más nos funciona recomendar.",
        ],
        secciones=[
            ("Los platos de todos los días", [
                ("Casado", "La <a href=\'mayonesa-de-culantro.html\'>mayonesa de culantro</a> es la ganadora. El culantro conecta con el arroz y no pelea con el frijol. Una cucharada al lado, no encima."),
                ("Gallos de carne", "Mayonesa de <a href=\'mayonesa-de-chipotle.html\'>chipotle</a>. El ahumado hace que una carne sencilla sepa a parrilla."),
                ("Chifrijo", "Aquí sí va picante de verdad. La <a href=\'salsa-de-chile-dulce.html\'>salsa de chile dulce</a> si hay gente que no aguanta, o habanero para los que sí."),
                ("Arroz con pollo", "Mayonesa de culantro, como se sirve en las fiestas. Es la combinación que la gente ya espera."),
            ]),
            ("Fines de semana y parrilla", [
                ("Carne asada", "Chimichurri sobre el corte ya servido. Nunca durante la cocción."),
                ("Costillas de cerdo", "<a href=\'salsa-pina-habanero.html\'>Piña habanero</a> como glaseado en los últimos minutos. El azúcar de la piña caramelza y el habanero corta la grasa."),
                ("Pollo a la parrilla", "Chile dulce como glaseado, o chipotle al lado."),
                ("Chorizo", "Chimichurri, sin discusión."),
            ]),
            ("Mariscos y pescado", [
                ("Ceviche", "Nada encima: el ceviche ya tiene su punto. Pero un chile dulce al lado, para quien quiera, funciona bien."),
                ("Pescado a la plancha", "Mayonesa de culantro. Es fresca y no tapa un pescado blanco."),
                ("Camarones", "Piña habanero, salteados y terminados con una cucharada."),
                ("Tacos de pescado", "Mayonesa de culantro y encima unas gotas de habanero."),
            ]),
            ("Para picar", [
                ("Patacones", "Alioli o chipotle. Los dos funcionan; el alioli es más suave."),
                ("Yuca frita", "Alioli, sin dudarlo."),
                ("Tortilla con queso", "<a href=\'chile-morron-asado.html\'>Chile morrón asado</a> picado adentro."),
                ("Tabla de bocas", "Tres salsas de niveles distintos y que cada quien escoja. Es lo que hacemos en la feria."),
            ]),
        ],
        faq=[
            ("¿Qué salsa le pongo a un casado?",
             "La mayonesa de culantro es la que mejor funciona: el culantro va con el arroz y no compite con el frijol. Se sirve al lado, no encima."),
            ("¿Cuál es la mejor salsa para chifrijo?",
             "Depende de quién come. Si hay gente que no aguanta picante, la salsa de chile dulce. Si todos aguantan, habanero."),
            ("¿Qué salsa llevo para una parrillada?",
             "Chimichurri para las carnes rojas y piña habanero para el cerdo. Con esas dos cubrís casi todo el asado."),
            ("¿Qué salsas pongo en una tabla de bocas?",
             "Tres de niveles distintos: una sin picante, una suave y una fuerte. Así nadie se queda afuera."),
        ],
        productos=["mayonesa-de-culantro", "salsa-de-chile-dulce", "mayonesa-de-chipotle"],
        cta="Armá tu combo para la próxima comida",
    ),

    dict(
        slug="tabla-de-quesos-y-bocas",
        titulo="Cómo armar una tabla de quesos y bocas que impresione",
        h1="Cómo armar una tabla de quesos",
        desc="Guía para armar una tabla de quesos y bocas: qué llevar, cómo distribuirlo y qué conservas usar para lograr contraste. Productos artesanales de Costa Rica.",
        img="tomates", w=800, h=600,
        lede="Una tabla bien armada es la forma más barata de quedar bien con visitas. "
             "El truco está en el contraste, no en gastar más.",
        intro=[
            "La gente cree que una buena tabla depende de conseguir quesos caros. No es así. "
            "Depende de que haya <strong>contraste</strong>: algo salado contra algo dulce, algo "
            "cremoso contra algo crujiente, algo suave contra algo intenso.",
            "Con dos o tres quesos comunes y las conservas correctas se arma algo que se ve y "
            "sabe mucho mejor que la suma de sus partes.",
        ],
        secciones=[
            ("La estructura", [
                ("Tres quesos bastan", "Uno suave y cremoso, uno maduro y salado, uno azul o de sabor fuerte. Más de tres y nadie los distingue."),
                ("Un dulce", "Es lo que hace que la tabla funcione. La <a href=\'salsa-de-mora.html\'>salsa de mora</a> con un queso azul o maduro es el contraste clásico: la acidez corta la sal."),
                ("Un salado en aceite", "<a href=\'tomates-deshidratados.html\'>Tomates deshidratados</a> o <a href=\'chile-morron-asado.html\'>chile morrón asado</a>. Aportan intensidad y color, y el aceite del frasco sirve para mojar pan."),
                ("Algo crujiente", "Pan tostado, galletas saladas, tostadas. Sin esto la tabla se siente pesada."),
                ("Algo fresco", "Uvas, manzana en gajos o pera. Limpian el paladar entre bocado y bocado."),
            ]),
            ("Cómo distribuirlo", [
                ("Los quesos separados", "Cada uno en su zona, no amontonados. Si se tocan, se mezclan los sabores."),
                ("Las salsas en cuenquitos", "Nunca directo sobre la tabla: se corren y ensucian todo. Cuencos pequeños, con su cuchara."),
                ("Llenar los huecos", "Los espacios vacíos se rellenan con lo crujiente y lo fresco. Una tabla con huecos se ve incompleta."),
                ("Sacarla antes de tiempo", "Los quesos se sirven a temperatura ambiente. Sacalos de la refri 30 minutos antes: fríos no saben a nada."),
            ]),
            ("Tres combinaciones que siempre funcionan", [
                ("Queso azul con salsa de mora", "El contraste más fuerte y el que más comentarios genera."),
                ("Queso fresco con tomates deshidratados", "Con un chorrito del aceite del frasco encima."),
                ("Queso maduro con chile morrón asado", "El dulzor del morrón asado contra la sal del queso."),
            ]),
        ],
        faq=[
            ("¿Cuántos quesos necesito para una tabla?",
             "Tres alcanzan: uno suave, uno maduro y uno de sabor fuerte. Más de tres y la gente deja de distinguirlos."),
            ("¿Qué conserva va mejor con queso azul?",
             "Una salsa dulce con acidez, como la de mora. La acidez corta la sal del queso azul y equilibra el bocado."),
            ("¿Cuánto antes saco los quesos de la refrigeradora?",
             "Media hora. Un queso frío pierde aroma y textura; a temperatura ambiente sabe muchísimo mejor."),
            ("¿Se puede armar la tabla con anticipación?",
             "Los quesos y las conservas sí, hasta una hora antes. Lo crujiente y la fruta, al último momento, para que no se ablanden."),
        ],
        productos=["salsa-de-mora", "tomates-deshidratados", "chile-morron-asado"],
        cta="Pedí las conservas para tu tabla",
    ),
]
