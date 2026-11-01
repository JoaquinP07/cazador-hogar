import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get
for b in ["https://www.oportuna.com.uy", "https://www.urumarket.com.uy"]:
    r = _get(b)
    print("FEN", b, " ".join(sorted(set(re.findall(r'href="(?:' + re.escape(b) + r')?/([a-z0-9][a-z0-9-]+)"', r.text)))))
for b, c in [("https://www.divino.com.uy", "electro"), ("https://www.divino.com.uy", "electrodomesticos"), ("https://www.oportuna.com.uy", "celulares"), ("https://www.urumarket.com.uy", "electronica")]:
    r = _get(f"{b}/{c}?js=1&pag=1"); t = re.search(r'data-total="(\d+)"', r.text)
    print("FENCAT", b, c, r.status_code, t.group(1) if t else None)
r = _get("https://www.elemporiodelhogar.com.uy/graphql", params={"query": '{categoryList(filters:{}){children{id name url_path product_count}}}'})
print("MAG", json.dumps([(c["id"], c["name"], c["product_count"]) for c in r.json()["data"]["categoryList"][0]["children"]], ensure_ascii=False))
r = _get("https://www.eldorado.com.uy/api/catalog_system/pub/products/search", params={"_from": 0, "_to": 0, "fq": "C:/4/"})
print("ELD", r.status_code, r.headers.get("resources"))
for c in ["cat1140017", "cat1140019", "cat1140011"]:
    r = _get(f"https://www.sodimac.com.uy/sodimac-uy/category/{c}/x")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    if m:
        pp = json.loads(m.group(1))["props"]["pageProps"]
        print("SOD", c, (pp.get("categoryProps", {}).get("categoryData", {}).get("results") or {}).get("displayName"), (pp["searchProps"]["searchData"].get("pagination") or {}).get("count"))
