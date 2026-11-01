"""Descubre categorías y formatos de las tiendas candidatas (solo diagnóstico)."""
import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get, _fenicio_pagina

FENICIO = {"Arocena": "https://ferreteriaarocena.com.uy", "El Clon": "https://www.elclon.com.uy",
           "Divino": "https://www.divino.com.uy", "JYSK": "https://www.jysk.uy", "La Tentacion": "https://www.latentacion.com.uy",
           "Brillante": "https://www.brillante.com.uy", "Rustico": "https://rusticohogar.com.uy"}
for n, b in FENICIO.items():
    r = _get(b)
    rutas = sorted(set(re.findall(r'href="(?:' + re.escape(b) + r')?/([a-z0-9][a-z0-9-]+)"', r.text)))
    print(f"\n=== FENICIO {n}: {len(rutas)} rutas")
    print(" ".join(rutas)[:3000])

for n, b in {"Balton": "https://balton.com.uy", "MundoShop": "https://mundoshop.com.uy"}.items():
    r = _get(f"{b}/products.json?limit=250&page=1")
    try:
        ps = r.json().get("products", [])
        print(f"\n=== SHOPIFY {n}: HTTP {r.status_code} pag1={len(ps)}", [p['product_type'] for p in ps[:40]])
        if ps: print("  ej:", ps[0]["title"], ps[0]["variants"][0]["price"], ps[0]["variants"][0].get("compare_at_price"))
    except Exception as e:
        print(f"\n=== SHOPIFY {n}: HTTP {r.status_code} {e} {r.text[:200]}")

r = _get("https://www.arredo.com.uy/api/catalog_system/pub/category/tree/1")
print("\n=== ARREDO tree", r.status_code, r.text[:1500])
r = _get("https://www.arredo.com.uy/api/catalog_system/pub/products/search?_from=0&_to=2")
print("=== ARREDO search", r.status_code, r.headers.get("resources"), r.text[:600])

for slug in ["hogar","bazar","ferreteria","ferreteria-y-bricolaje","jardin","jardin-y-exterior","muebles","decoracion","textil-hogar","aire-libre","bano","camping","bricolaje","herramientas","hogar-y-deco","verano","piscinas","muebles-y-deco","bazar-y-cocina","cocina"]:
    v = {"first": 1, "after": "0", "sort": "price_asc", "term": "", "selectedFacets": [{"key": "category-1", "value": slug}]}
    r = _get("https://www.tata.com.uy/api/graphql", params={"operationName": "ProductsQuery", "variables": json.dumps(v)})
    try: t = r.json()["data"]["search"]["products"]["pageInfo"]["totalCount"]
    except Exception: t = "?"
    print(f"TATA {slug}: {t}")
r = _get("https://www.tata.com.uy")
print("TATA links:", " ".join(sorted(set(re.findall(r'href="/([a-z0-9-]+)"', r.text))))[:2500])

for b in ["https://www.disco.com.uy", "https://www.geant.com.uy", "https://www.devoto.com.uy"]:
    r = _get(b)
    print(f"\n=== {b}", r.status_code, "blazor" if "blazor" in r.text.lower() else "", "vtex" if "vtex" in r.text.lower() else "")
    print(" ".join(sorted(set(re.findall(r'href="(?:' + re.escape(b) + r')?/?(products/category/[a-z0-9-]+/\d+)"', r.text))))[:2500])

r = _get("https://www.sodimac.com.uy/sodimac-uy/category/cat20888/Herramientas-electricas-e-inalambricas")
print("\n=== SODIMAC", r.status_code, len(r.text))
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
if m:
    d = json.loads(m.group(1))
    pp = d.get("props", {}).get("pageProps", {})
    print("pageProps keys:", list(pp.keys())[:40])
    def buscar(o, cam=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("results", "pagination", "products") : print("  ", cam + "/" + k, type(v).__name__, (len(v) if hasattr(v, "__len__") else v))
                buscar(v, cam + "/" + k)
        elif isinstance(o, list) and o and cam.count("/") < 6:
            buscar(o[0], cam + "[0]")
    buscar(pp)
    res = pp.get("results") or []
    if res: print(json.dumps(res[0], ensure_ascii=False)[:2000])
    print("pagination:", json.dumps(pp.get("pagination"), ensure_ascii=False)[:500])
else:
    print(r.text[:1500])
r = _get("https://www.sodimac.com.uy/sodimac-uy")
print("SODIMAC cats:", " ".join(sorted(set(re.findall(r'/sodimac-uy/category/(cat\d+/[A-Za-z0-9-]+)', r.text))))[:4000])
