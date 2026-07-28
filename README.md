# CARLOUIS Gourmet — www.carlouis.net

Sitio de la marca costarricense de salsas artesanales, picantes de habanero, pestos y conservas
gourmet. HTML y CSS estáticos, sin frameworks ni paso de compilación: se edita y se sube.

## Estructura

```
index.html            Portada
productos.html        Catálogo con filtros y escala de picante
testimonios.html      29 testimonios de clientes
encuentranos.html     Feria La Verbena + mapa
cobertura.html        Envíos por provincia y cantón (clave para SEO local)
contacto.html         Formulario + datos de contacto
gracias.html          Confirmación del formulario (noindex)
404.html              Página de error

assets/css/styles.css  Design system completo (tokens, componentes, responsive)
assets/js/main.js      Nav móvil, carrusel, filtros, animaciones de entrada
assets/fonts/          Fraunces + Karla en woff2, autoalojadas
assets/img/            Imágenes optimizadas en WebP + respaldo JPG
assets/                Imágenes originales sin tocar + los dos recetarios en PDF

sitemap.xml  robots.txt  site.webmanifest  favicon.ico  _headers
SEO.md                 Guía de posicionamiento — leela, tiene los pasos pendientes
```

## Cómo editar

**Agregar un producto:** copiá un bloque `<article class="card">` completo dentro de
`productos.html` y cambiá imagen, nombre, `data-category`, `data-level` (0 a 5 de picante),
descripción, precio y el texto del enlace de WhatsApp.

**Cambiar colores o tipografía:** todo está en las variables de `:root`, arriba de
`assets/css/styles.css`. Cambiando ahí se actualiza el sitio entero.

> ⚠️ **Regla de color:** el dorado (`--gold-500`) no se puede usar como texto sobre fondo claro —
> el contraste queda en 2,1:1 y es ilegible. Va como fondo de chip con texto oscuro, o como texto
> sobre el rojo profundo. El resto de la paleta cumple WCAG AA o AAA.

**El encabezado y el pie están repetidos en cada página** (es el precio de no tener compilación).
Si cambiás uno, cambialos en los 8 archivos.

## Optimizar una imagen nueva

Las imágenes van a `assets/` y su versión optimizada a `assets/img/`. Con Python y Pillow:

```bash
python -c "from PIL import Image; im=Image.open('assets/foto.jpg').convert('RGB'); im.thumbnail((900,900)); im.save('assets/img/foto.webp','WEBP',quality=80,method=6); im.save('assets/img/foto.jpg',quality=76,optimize=True,progressive=True)"
```

Después se usan juntas, con WebP primero y JPG de respaldo:

```html
<picture>
  <source srcset="assets/img/foto.webp" type="image/webp" />
  <img src="assets/img/foto.jpg" width="900" height="675" loading="lazy" decoding="async" alt="Descripción real de la foto" />
</picture>
```

## Pedido por WhatsApp (armar varios productos en un solo mensaje)

Antes, cada botón "Pedir" abría WhatsApp con **un** producto: quien quería cuatro cosas tenía que
mandar cuatro mensajes. Ahora los botones dicen **Agregar** y arman un pedido.

Cómo funciona: el pedido se guarda en `localStorage` del navegador (no hay servidor). Aparece un
botón flotante abajo a la izquierda con el conteo y se abre un panel lateral de **dos pasos**:

1. **Tu pedido** — se ajustan cantidades y se ve el total en colones.
2. **Tus datos** — nombre, teléfono, cantón, distrito y dirección (obligatorios) más correo
   electrónico (opcional). No se puede enviar sin completar los obligatorios.

Al enviar se genera **un solo mensaje** con todo:

```
Hola CARLOUIS, quiero hacer este pedido:

• 2 x Piña Habanero — ₡10.000
• 1 x Tomates Deshidratados — ₡6.000

Total estimado: ₡16.000

--- Mis datos ---
Nombre: Luis Rodríguez
Teléfono: 8825 2608
Cantón: Santa Ana
Distrito: Pozos
Dirección: 200m sur de la iglesia, casa blanca
Correo: luis@correo.com
```

Los datos del cliente quedan guardados **en su propio navegador**, así que en el siguiente pedido
ya vienen llenos y solo elige productos. El pedido se vacía después de enviarlo; los datos no.

> **Ojo:** hoy los datos llegan solo por WhatsApp, no se guardan en ninguna base de datos.
> Cuando quieras acumular la lista de clientes hay que conectar un backend (Google Sheets,
> Netlify Forms o similar) — y en ese momento conviene agregar una casilla de consentimiento,
> porque la Ley 8968 de Costa Rica exige consentimiento informado para almacenar datos personales
> y usarlos para enviar promociones.

**Para que un producto entre al pedido**, su botón necesita estos tres atributos:

```html
<a class="btn btn--primary btn--sm" href="https://wa.me/50688252608?text=..."
   data-add data-name="Piña Habanero" data-price="5000">
```

`data-price` va **sin puntos** (`5000`, no `5.000`). Si falta cualquiera de los tres atributos, el
botón sigue funcionando como enlace normal de WhatsApp — no se rompe nada.

También hay **lightbox** para ampliar la foto de cualquier producto y botón de **volver arriba**;
ambos se generan solos, no hay que tocar el HTML.

## Notas técnicas

- **CSP estricta** (`script-src 'self'`): no se puede poner JavaScript dentro del HTML. Todo script
  va en un archivo aparte dentro de `assets/js/`. El JSON-LD sí puede ir en el HTML porque el
  navegador no lo ejecuta.
- **`_headers`** trae las cabeceras de seguridad y caché para Netlify o Cloudflare Pages.
  `frame-ancestors` y HSTS solo funcionan como cabecera real, no como `<meta>`. En GitHub Pages
  este archivo se ignora.
- **El formulario** usa Netlify Forms y redirige a `gracias.html`. Si el sitio no está en Netlify,
  hay que cambiarlo por Formspree o similar — el botón de WhatsApp sigue funcionando igual.
- Toda la interfaz respeta `prefers-reduced-motion`.

## Peso de la portada

| | Antes | Ahora |
|---|---|---|
| Primera carga | 3,00 MB | **0,33 MB** |
| Imágenes del proyecto | 9,27 MB | **1,47 MB** (WebP) |

Y eso incluyendo 90 KB de tipografías propias que antes no había.
