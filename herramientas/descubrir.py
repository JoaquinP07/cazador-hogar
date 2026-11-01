import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get
FIRMAS = [("Fenicio", r"fenicio"), ("Shopify", r"cdn\.shopify\.com"), ("VTEX", r"vtex"), ("Tiendanube", r"tiendanube|nuvemshop"),
          ("WooCommerce", r"woocommerce|wp-content"), ("Magento", r"Magento|mage/cookies|Mage\.Cookies"), ("PrestaShop", r"prestashop"),
          ("Wix", r"wixstatic"), ("Jumpseller", r"jumpseller"), ("Next", r"__NEXT_DATA__"), ("Blazor", r"blazor")]
for s in sys.argv[1:]:
    try:
        r = _get(s)
        enc = [n for n, p in FIRMAS if re.search(p, r.text[:600000], re.I)]
        t = re.search(r"<title>([^<]{0,70})", r.text)
        print(f"WEB {s} | {r.status_code} | {', '.join(enc) or '?'} | {r.url} | {t.group(1).strip() if t else ''}")
    except Exception as e:
        print(f"WEB {s} | ERROR {type(e).__name__}")
for c in ["cat20288", "cat20278", "cat20214", "cat20300", "cat20322"]:
    r = _get(f"https://www.sodimac.com.uy/sodimac-uy/category/{c}/x")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    cd = json.loads(m.group(1))["props"]["pageProps"]["categoryProps"]["categoryData"]["results"]
    print("SOD", c, [(b["categoryId"], b["name"]) for b in cd.get("breadcrumbs", [])])
for c in ["cat20276", "cat20286", "cat20296", "cat20312", "cat20320"]:
    r = _get(f"https://www.sodimac.com.uy/sodimac-uy/category/{c}/x")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    if m:
        pp = json.loads(m.group(1))["props"]["pageProps"]
        print("SODX", c, pp["categoryProps"]["categoryData"]["results"].get("displayName"), (pp["searchProps"]["searchData"].get("pagination") or {}).get("count"))
