import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get, SES
Q = '{products(search:"", pageSize:3, currentPage:1){total_count items{sku name url_key url_suffix stock_status price_range{minimum_price{final_price{value currency} regular_price{value}}}}}}'
for b in ["https://www.elemporiodelhogar.com.uy", "https://www.mosca.com.uy"]:
    r = _get(f"{b}/graphql", params={"query": Q}, headers={"Content-Type": "application/json"})
    print("MAG", b, r.status_code, r.text[:700])
    r = _get(f"{b}/graphql", params={"query": '{categoryList(filters:{}){children{id name url_path product_count children{id name url_path product_count}}}}'})
    print("MAGCAT", b, r.status_code, r.text[:2500])
r = _get("https://www.eldorado.com.uy/api/catalog_system/pub/category/tree/1")
print("ELD tree", r.status_code, json.dumps([(c["id"], c["name"]) for c in r.json()], ensure_ascii=False) if r.ok else r.text[:300])
r = _get("https://www.eldorado.com.uy/api/catalog_system/pub/products/search", params={"_from": 0, "_to": 1})
print("ELD search", r.status_code, r.headers.get("resources"), r.text[:300])
r = _get("https://tecsys.com.uy/wp-json/wc/store/v1/products", params={"per_page": 2})
print("TEC", r.status_code, r.headers.get("X-WP-Total"), r.text[:500])
for b, cats in [("https://www.oportuna.com.uy", None), ("https://www.urumarket.com.uy", None)]:
    r = _get(b)
    print("FEN", b, " ".join(sorted(set(re.findall(r'href="(?:' + re.escape(b) + r')?/([a-z0-9][a-z0-9-]+)"', r.text))))[:1500])
for b in ["https://netpc.uy", "https://www.infinit.com.uy", "https://www.tiendaelectronica.uy"]:
    r = _get(b); t = r.text
    print("OTRO", b, re.findall(r'(?:generator|platform|powered)[^>]{0,120}', t, re.I)[:3], re.findall(r'src="(https?://[^"/]+)/', t)[:8])
for c in ["cat2170003", "cat910021"]:
    r = _get(f"https://www.sodimac.com.uy/sodimac-uy/category/{c}/x")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    pp = json.loads(m.group(1))["props"]["pageProps"]
    sd = pp["searchProps"]["searchData"]
    f = [x for x in sd.get("facets") or [] if "ategor" in (x.get("name") or "")]
    print("SOD", c, (sd.get("pagination") or {}).get("count"), json.dumps(f, ensure_ascii=False)[:1500])
