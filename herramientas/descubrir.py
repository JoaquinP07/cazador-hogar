import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get
FIRMAS = [("Fenicio", r"fenicio"), ("Shopify", r"cdn\.shopify\.com"), ("VTEX", r"vtex"), ("Tiendanube", r"tiendanube|nuvemshop"),
          ("WooCommerce", r"woocommerce|wp-content"), ("Magento", r"mage/cookies|Mage\.Cookies|magento"), ("Next", r"__NEXT_DATA__"), ("Blazor", r"blazor")]
for s in ["https://www.carlosgutierrez.com.uy", "https://carlosgutierrez.com.uy", "https://www.cgutierrez.com.uy"]:
    try:
        r = _get(s)
        enc = [n for n, p in FIRMAS if re.search(p, r.text[:600000], re.I)]
        t = re.search(r"<title>([^<]{0,80})", r.text)
        print(f"WEB {s} | {r.status_code} | {', '.join(enc) or '?'} | {r.url} | {t.group(1).strip() if t else ''}")
        if r.ok:
            print("RUTAS", " ".join(sorted(set(re.findall(r'href="(?:https?://[^/"]*carlosgutierrez[^/"]*)?/([a-z0-9][a-z0-9/-]{2,60})"', r.text))))[:2500])
            print("API", sorted(set(re.findall(r'https?://[a-z0-9.-]+/(?:api|graphql|_v|io)[^"\'\s]{0,80}', r.text)))[:20])
    except Exception as e:
        print(f"WEB {s} | ERROR {type(e).__name__}")
for u in ["https://www.carlosgutierrez.com.uy/products.json?limit=2", "https://www.carlosgutierrez.com.uy/api/catalog_system/pub/products/search?_from=0&_to=1",
          "https://www.carlosgutierrez.com.uy/wp-json/wc/store/v1/products?per_page=2",
          "https://www.carlosgutierrez.com.uy/graphql?query=%7Bproducts(search:%22%22,pageSize:1)%7Btotal_count%7D%7D"]:
    try:
        r = _get(u); print("PRUEBA", u, r.status_code, r.headers.get("resources"), r.text[:250].replace("\n", " "))
    except Exception as e: print("PRUEBA", u, "ERROR", type(e).__name__)
r = _get("https://www.devoto.com.uy/products/category/electrodomesticos/22")
print("DEV len", len(r.text), "items", len(re.findall(r'href="[^"]*product/[a-z0-9-]+/\d+', r.text)))
print("DEV urls", sorted(set(re.findall(r'https?://[a-z0-9.-]+/[^"\'\s<>]{0,90}', r.text)))[:60])
print("DEV rel", sorted(set(re.findall(r'(?:src|href)="(/[^"]{0,90})"', r.text)))[:60])
for u in ["https://www.devoto.com.uy/api/catalog_system/pub/products/search?_from=0&_to=1",
          "https://www.devoto.com.uy/products/category/electrodomesticos/22?page=2",
          "https://www.devoto.com.uy/products/category/electrodomesticos/22?pagina=2",
          "https://www.devoto.com.uy/products/category/electrodomesticos/22?p=2"]:
    r = _get(u); ids = re.findall(r'product/[a-z0-9-]+/(\d+)', r.text)
    print("DEVP", u, r.status_code, r.headers.get("content-type"), len(ids), ids[:3], r.text[:150].replace("\n", " ") if "api" in u else "")
