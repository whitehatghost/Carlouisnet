# -*- coding: utf-8 -*-
"""Avisa a Bing (y a Yandex, Seznam, Naver) que hay URLs nuevas o modificadas.

IndexNow es un ping: en vez de esperar a que el buscador vuelva a pasar, uno le
dice "mirá esto ahora". Bing suele indexar en horas. Google NO participa en
IndexNow: para Google sigue siendo Search Console.

Uso:

    python tools/indexnow.py                      # manda todo el sitemap
    python tools/indexnow.py feria-x.html a.html  # manda solo esas paginas

La llave vive en la raiz del repo como <llave>.txt y tiene que estar publicada
en https://www.carlouis.net/<llave>.txt  (el buscador la verifica antes de
aceptar el envio). No es un secreto: es publica a proposito.
"""
import io, os, re, sys, glob, json
import urllib.request

HOST = "www.carlouis.net"
BASE = "https://" + HOST + "/"
ENDPOINT = "https://api.indexnow.org/indexnow"

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)


def llave():
    cand = [f for f in glob.glob("*.txt")
            if re.fullmatch(r"[0-9a-f]{8,128}\.txt", f)]
    if not cand:
        raise SystemExit("No encontre el archivo de llave <hex>.txt en la raiz.")
    k = os.path.splitext(cand[0])[0]
    guardada = io.open(cand[0], encoding="ascii").read().strip()
    if guardada != k:
        raise SystemExit("El archivo %s debe contener exactamente '%s'." % (cand[0], k))
    return k


def urls_del_sitemap():
    xml = io.open("sitemap.xml", encoding="utf-8").read()
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)


def main():
    k = llave()
    if len(sys.argv) > 1:
        urls = [a if a.startswith("http") else BASE + a.lstrip("/") for a in sys.argv[1:]]
    else:
        urls = urls_del_sitemap()

    cuerpo = json.dumps({
        "host": HOST,
        "key": k,
        "keyLocation": BASE + k + ".txt",
        "urlList": urls,
    }, ensure_ascii=False).encode("utf-8")

    print("llave      :", k)
    print("verificable:", BASE + k + ".txt")
    print("URLs       :", len(urls))
    for u in urls:
        print("   ", u)

    req = urllib.request.Request(
        ENDPOINT, data=cuerpo,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("\nrespuesta  : HTTP %s %s" % (r.status, r.reason))
            eco = r.read().decode("utf-8", "replace").strip()
            if eco:
                print("cuerpo     :", eco[:400])
    except urllib.error.HTTPError as e:
        print("\nrespuesta  : HTTP %s %s" % (e.code, e.reason))
        print("cuerpo     :", e.read().decode("utf-8", "replace")[:400])
        print("\n200/202 = aceptado. 403 = la llave no se pudo verificar.")
        print("422 = las URLs no son de este host. 429 = demasiados envios.")
        raise SystemExit(1)

    print("\nListo. 200 o 202 significa aceptado; la indexacion no es instantanea.")


if __name__ == "__main__":
    main()
