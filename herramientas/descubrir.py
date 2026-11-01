"""Diagnóstico 2: Tata hogar, Sodimac y Fenicio."""
import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get, _fenicio_pagina

for slug in ["hogar-y-bazar","bazar-y-hogar","textil","textiles","textil-y-hogar","blanqueria","muebles-y-decoracion","jardin-y-aire-libre","aire-libre-y-jardin","aire-libre","automovil","ferreteria-y-automovil","camping-y-playa","deportes-y-aire-libre","muebles-y-jardin","exterior","organizacion","iluminacion","bazar-cocina-y-mesa","bazar-y-cocina","mascotas","hogar-y-limpieza","limpieza-y-hogar","decoracion-y-hogar","muebles-y-colchones","colchones","cama-y-bano","dormitorio","libreria-y-papeleria","jugueteria","juguetes","deportes"]:
    v = {"first": 1, "after": "0", "sort": "price_asc", "term": "", "selectedFacets": [{"key": "category-1", "value": slug}]}
    r = _get("https://www.tata.com.uy/api/graphql", params={"operationName": "ProductsQuery", "variables": json.dumps(v)})
    try: t = r.json()["data"]["search"]["products"]["pageInfo"]["totalCount"]
    except Exception: t = "?"
    if t: print(f"TATA {slug}: {t}")
for u in ["https://www.tata.com.uy/sitemap.xml", "https://www.tata.com.uy/sitemap/category-0.xml", "https://www.tata.com.uy/robots.txt"]:
    r = _get(u); print("TATA", u, r.status_code, r.text[:800].replace("\n", " "))

def nd(url):
    r = _get(url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    return r.status_code, (json.loads(m.group(1))["props"]["pageProps"] if m else None)
st, pp = nd("https://www.sodimac.com.uy/sodimac-uy/category/cat20888/Herramientas-electricas-e-inalambricas")
sd = pp["searchProps"]["searchData"]
print("SOD pagination", json.dumps(sd.get("pagination")), "keys", list(sd.keys()))
print("SOD item", json.dumps(sd["results"][0], ensure_ascii=False)[:2500])
cd = pp["categoryProps"]["categoryData"]["results"]
print("SOD cat", json.dumps(cd, ensure_ascii=False)[:1500])
st2, pp2 = nd("https://www.sodimac.com.uy/sodimac-uy/category/cat20888/Herramientas-electricas-e-inalambricas?page=2")
print("SOD p2", st2, [x.get("productId") for x in pp2["searchProps"]["searchData"]["results"][:3]] if pp2 else None, [x.get("productId") for x in sd["results"][:3]])
r = _get("https://www.sodimac.com.uy/sodimac-uy")
txt = r.text
for m in re.finditer(r'"(?:label|name|title)":"([^"]{3,40})","(?:link|url|href)":"(/sodimac-uy/category/cat\d+/[^"?]+)', txt):
    print("SODMENU", m.group(1), m.group(2))
print("SOD top", sorted(set(re.findall(r'/sodimac-uy/category/(cat\d{4,5}/[A-Za-z0-9-]+)', txt)))[:80])

for b, c in [("https://ferreteriaarocena.com.uy","herramientas"),("https://www.elclon.com.uy","hogar"),("https://www.divino.com.uy","living"),("https://www.jysk.uy","dormitorio"),("https://www.latentacion.com.uy","hogar"),("https://www.brillante.com.uy","herramientas"),("https://rusticohogar.com.uy","living")]:
    r = _get(f"{b}/{c}?js=1&pag=1")
    t = re.search(r'data-total="(\d+)"', r.text)
    ps = _fenicio_pagina(r.text, "x")
    print("FEN", b, c, r.status_code, t.group(1) if t else None, len(ps), ps[0].nombre if ps else "", ps[0].precio if ps else "", ps[0].precio_lista if ps else "", ps[0].url if ps else "")
