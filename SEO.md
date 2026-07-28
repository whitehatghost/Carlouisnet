# Guía SEO — CARLOUIS Gourmet

## Lo primero, sin rodeos

El sitio ya tiene **todo el SEO técnico que se puede hacer desde el código**. Pero hay que ser claro
en una cosa: **ningún cambio de código te pone de primero en Google por sí solo.**

Para búsquedas locales ("salsa picante Alajuela", "salsas gourmet Costa Rica"), Google decide el
orden con tres factores, y el código solo influye en uno:

| Factor | Peso aproximado | ¿Se resuelve con código? |
|---|---|---|
| **Google Business Profile** (ficha de empresa) | Altísimo en resultados locales | ❌ No — hay que crearla |
| **Reseñas y menciones** (reseñas de Google, directorios, prensa) | Muy alto | ❌ No — hay que conseguirlas |
| **Sitio web** (contenido, velocidad, estructura) | Medio-alto | ✅ Ya está hecho |

Traducción: **lo que ya está hecho te pone en la carrera. Lo de abajo es lo que te hace ganar.**
Sin el paso 1, no vas a salir de primero aunque el sitio sea perfecto.

---

## PASO 1 — Google Business Profile (lo más importante de todo)

Es gratis y es, con diferencia, lo que más mueve la aguja en búsquedas locales de Costa Rica.
Cuando alguien busca "salsas artesanales cerca de mí" o "chile picante Alajuela", Google muestra
primero el mapa con tres negocios. **Ahí es donde tenés que estar.**

1. Entrá a <https://business.google.com> y creá el perfil.
2. Datos que tienen que coincidir **exactamente** con el sitio (Google compara):
   - Nombre: `CARLOUIS Gourmet`
   - Teléfono: `+506 8825 2608`
   - Sitio web: `https://www.carlouis.net`
   - Dirección: Feria Orgánica La Verbena, Plaza Real Alajuela
   - Horario: Sábados 6:00 a.m. – 1:00 p.m.
3. Categoría principal: **Tienda de productos gourmet**.
   Secundarias: *Fabricante de alimentos*, *Tienda de productos orgánicos*.
4. Subí **mínimo 15 fotos reales**: los frascos, el puesto en la feria, el proceso, vos trabajando.
   Los perfiles con muchas fotos reciben bastante más clics.
5. Publicá una novedad **cada semana** (producto nuevo, que vas a estar el sábado, una receta).
   Los perfiles activos rankean mejor que los abandonados.

> Si vendés solo en feria y no tenés local fijo, registrate como **"negocio con área de servicio"**
> e indicá las provincias donde entregás. No necesitás dirección pública.

## PASO 2 — Reseñas

Objetivo realista: **25 reseñas en los primeros 3 meses**, luego 3–5 por mes de forma constante.

- Pedila **en el momento**, en la feria, cuando el cliente ya probó y le gustó.
- Mandá el link directo por WhatsApp después de cada pedido (Google te da un link corto para reseñas
  desde tu perfil).
- Contestá **todas** las reseñas, incluso las malas. Google lo toma como señal de negocio activo.
- Cuando podás, pediles que mencionen el producto y el lugar: *"la salsa de habanero, la compré en
  Alajuela"* vale mucho más que *"muy bueno"*.

⚠️ **Nunca compres reseñas.** Google las detecta y la penalización tumba el perfil entero.

## PASO 3 — Directorios y menciones (citations)

Que tu nombre, teléfono y dirección aparezcan **idénticos** en varios sitios le confirma a Google
que el negocio es real. Registrate en:

- Páginas Amarillas Costa Rica
- Yelp Costa Rica
- Facebook Business (aunque no lo uses mucho)
- Directorios de ferias orgánicas y productores locales de CR
- Grupos y directorios de emprendimientos ticos

**Clave:** escribí el nombre, teléfono y dirección **exactamente igual en todos**. Cualquier
variación (`Carlouis` vs `CARLOUIS Gourmet`) le resta fuerza.

## PASO 4 — Search Console (para saber qué está pasando)

1. Entrá a <https://search.google.com/search-console> y verificá `carlouis.net`.
2. En *Sitemaps*, enviá: `https://www.carlouis.net/sitemap.xml`
3. Usá *Inspección de URL* → *Solicitar indexación* para cada página nueva.
4. Revisalo cada 15 días: te dice **con qué palabras te están encontrando**. Esa lista es oro —
   escribí contenido sobre lo que la gente realmente busca, no sobre lo que vos creés que busca.

---

## Lo que ya quedó hecho en el sitio

- **Datos estructurados (JSON-LD)** — Google entiende el negocio, no solo lee texto:
  `Organization`, `LocalBusiness` + `FoodEstablishment` (con horario, coordenadas GPS y las 7
  provincias como área de servicio), `Product` con precios en colones, `ItemList` del catálogo,
  `FAQPage`, `BreadcrumbList` y `ContactPage`.
- **FAQs en inicio y en envíos** — son las que pueden aparecer desplegables en Google, ocupando
  más espacio en la pantalla de resultados.
- **Página de cobertura** (`cobertura.html`) — las 7 provincias con sus cantones, con información
  real de tiempos y costos. Captura búsquedas como *"envío de salsas a Guanacaste"*.
- **Velocidad** — las imágenes bajaron de 9,3 MB a 1,5 MB y las fuentes están en el propio servidor.
  Google usa la velocidad como factor de posicionamiento, sobre todo en celular.
- **Titles y descriptions** únicos y dentro del largo que Google muestra sin cortar.
- **Sitemap, robots.txt, canonical, Open Graph** y datos geográficos.
- **Textos con palabras clave naturales**: "salsas artesanales Costa Rica", "picante de habanero",
  "conservas gourmet", "Alajuela", "envíos a todo el país" — integradas en frases reales, no
  amontonadas.

## Lo que decidí NO hacer (y por qué te conviene)

- **No creé una página por cantón** ("Salsas en Escazú", "Salsas en Liberia"…). Google llama a eso
  *doorway pages* y **penaliza el sitio completo**. Es la trampa más común en SEO local. En su lugar
  hiciste una sola página de cobertura con contenido real, que es lo que Google sí premia.
- **No metí `AggregateRating` en los testimonios.** Marcar reseñas propias en tu propio sitio va
  contra las políticas de Google y puede costar una acción manual. Las estrellas en Google tienen
  que venir de reseñas reales del Business Profile.
- **No repetí palabras clave hasta saturar.** El *keyword stuffing* hace décadas que no funciona
  y hoy es motivo de penalización.

---

## Plan de contenido (esto es lo que te va a despegar a mediano plazo)

Google posiciona sitios que responden preguntas. Tu competencia son marcas grandes con presupuesto,
pero **ninguna escribe contenido útil en español tico**. Ahí está tu oportunidad.

Ideas de artículos, en orden de facilidad para posicionar:

1. *"¿Con qué se come el chimichurri? 8 formas que no se te han ocurrido"*
2. *"Escala de picante: cómo saber cuánto aguantás antes de comprar"*
3. *"Cómo conservar salsas artesanales sin preservantes"*
4. *"Recetas con tomate deshidratado para la casa"*
5. *"Qué llevar de regalo gourmet en Costa Rica"*
6. *"Ferias orgánicas en Alajuela: guía para el sábado"*

Con **un artículo al mes** durante un año, en 12 meses tenés 12 puertas de entrada más al sitio.
Es lento pero es lo que sostiene el posicionamiento a largo plazo.

## Expectativa realista de tiempos

| Momento | Qué esperar |
|---|---|
| Semanas 1–2 | Google reindexa el sitio nuevo. Podés ver movimiento raro; es normal. |
| Mes 1–2 | Con el Business Profile activo, empezás a salir en el mapa por búsquedas en Alajuela. |
| Mes 3–6 | Con 25+ reseñas, deberías competir por el top 3 local en tu zona. |
| Mes 6–12 | Con contenido publicado, empezás a posicionar a nivel nacional. |

Ser #1 en todo Costa Rica para "salsas gourmet" es una meta de **12+ meses** y depende sobre todo
de reseñas y contenido, no de código. Ser #1 en **Alajuela y alrededores** es totalmente alcanzable
en 2–4 meses si hacés el paso 1 y el paso 2 bien.

## Al publicar: revisá esto

- [ ] Que el dominio resuelva en **una sola versión** (`https://www.carlouis.net`). Si `carlouis.net`
      sin www también carga, configurá una redirección permanente. Google trata las dos como sitios
      distintos y te divide la fuerza.
- [ ] Verificar el sitio en Search Console y enviar el sitemap.
- [ ] Probar los datos estructurados en <https://search.google.com/test/rich-results>
- [ ] Medir velocidad en <https://pagespeed.web.dev>
