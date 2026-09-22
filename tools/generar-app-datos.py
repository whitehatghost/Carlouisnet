# -*- coding: utf-8 -*-
"""Vuelca el catálogo real a la app interna.

    python tools/generar-app-datos.py

La app de Carlouis no debe tener su propia lista de precios: si el catálogo
del sitio cambia, la app tiene que cambiar con él. Por eso este archivo se
genera y no se edita a mano.
"""
import io, os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from productos import PRODUCTOS

CATEGORIAS = {
    "picantes": "Picantes",
    "pestos": "Pestos",
    "cremas": "Cremas",
    "cremas picantes": "Cremas",
    "conservas": "Conservas",
    "especialidades": "Especialidades",
}

datos = [{
    "slug": p["slug"],
    "nombre": p["nombre"],
    "precio": int(p["precio_num"]),
    "unidad": p["unidad"],
    "cat": CATEGORIAS.get(p.get("cat", ""), p.get("cat", "Otros")),
} for p in PRODUCTOS]

os.makedirs("app", exist_ok=True)
salida = "app/productos.js"
cuerpo = (
    "// Generado por tools/generar-app-datos.py — no editar a mano.\n"
    "// Si cambia un precio, se cambia en tools/productos.py y se vuelve a correr.\n"
    "window.CATALOGO = " + json.dumps(datos, ensure_ascii=False, indent=2) + ";\n"
)
io.open(salida, "w", encoding="utf-8", newline="\n").write(cuerpo)

print("  %s  %d productos" % (salida, len(datos)))
for d in datos:
    print("     %-26s CRC %6d  %s" % (d["nombre"], d["precio"], d["cat"]))
