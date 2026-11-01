import re, sys, requests
SITIOS = sys.argv[1:]
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "es-UY,es"}
FIRMAS = [("Fenicio", r"fenicio"), ("Shopify", r"cdn\.shopify\.com|Shopify\.theme"), ("VTEX", r"vtex"),
          ("Tiendanube", r"tiendanube|nuvemshop|mitiendanube"), ("WooCommerce", r"woocommerce|wp-content"),
          ("Magento", r"Magento|mage/"), ("PrestaShop", r"prestashop"), ("Falabella", r"falabella"),
          ("Inditex", r"inditex|itxrest"), ("Wix", r"wixstatic"), ("Jumpseller", r"jumpseller")]
for s in SITIOS:
    try:
        r = requests.get(s, headers=H, timeout=25)
        html = r.text[:400000]
        enc = [n for n, p in FIRMAS if re.search(p, html, re.I)]
        print(f"{s} | {r.status_code} | {len(html)} | {', '.join(enc) or '?'} | {r.url}")
    except Exception as e:
        print(f"{s} | ERROR | {type(e).__name__}")
