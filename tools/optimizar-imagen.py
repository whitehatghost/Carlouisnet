# -*- coding: utf-8 -*-
"""Optimiza una imagen nueva para el sitio.

    python tools/optimizar-imagen.py assets/foto-nueva.jpg salsa-nueva

Genera assets/img/salsa-nueva.webp y .jpg listos para usar con <picture>.
Requiere Pillow:  pip install pillow
"""
import os, sys
from PIL import Image, ImageOps

if len(sys.argv) < 3:
    print(__doc__); raise SystemExit(1)

origen, nombre = sys.argv[1], sys.argv[2]
ancho_max = int(sys.argv[3]) if len(sys.argv) > 3 else 900

os.makedirs("assets/img", exist_ok=True)
im = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
antes = os.path.getsize(origen)

if im.width > ancho_max:
    im = im.resize((ancho_max, round(im.height * ancho_max / im.width)), Image.LANCZOS)

wp = f"assets/img/{nombre}.webp"
jp = f"assets/img/{nombre}.jpg"
im.save(wp, "WEBP", quality=80, method=6)
im.save(jp, "JPEG", quality=76, optimize=True, progressive=True)

print(f"  {origen}  {antes/1024:.0f} KB")
print(f"  -> {wp}  {os.path.getsize(wp)/1024:.0f} KB   ({im.width}x{im.height})")
print(f"  -> {jp}  {os.path.getsize(jp)/1024:.0f} KB")
print(f"""
Pegá esto en el HTML:

<picture>
  <source srcset="assets/img/{nombre}.webp" type="image/webp" />
  <img src="assets/img/{nombre}.jpg" width="{im.width}" height="{im.height}"
       loading="lazy" decoding="async" alt="Descripción real de la foto" />
</picture>
""")
