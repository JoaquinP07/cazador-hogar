import json, re, sys, requests
sys.path.insert(0, ".")
from cazador.tiendas import _get, UA
for u in ["https://www.carlosgutierrez.com.uy", "http://www.carlosgutierrez.com.uy", "https://carlosgutierrez.com.uy/"]:
    try:
        r = requests.get(u, timeout=60, headers={"User-Agent": UA}); print("CG", u, r.status_code, r.url, len(r.text))
    except Exception as e: print("CG", u, "ERROR", type(e).__name__, str(e)[:150])
r = _get("https://amvstore.com.uy")
print("AMV", " ".join(sorted(set(re.findall(r'href="(?:https://amvstore\.com\.uy)?/([a-z0-9][a-z0-9/-]+)"', r.text)))))
for u in ["https://amvhome.com.uy", "https://www.amvhome.com.uy"]:
    try: r = _get(u); print("AMVH", u, r.status_code, r.url)
    except Exception as e: print("AMVH", u, "ERROR", type(e).__name__)
for c in ["electrodomesticos/22", "tecnologia/23", "tv-y-audio/20", "celulares-y-telefonia/21"]:
    r = _get(f"https://www.devoto.com.uy/products/category/{c}")
    print("DEVSUB", c, sorted(set(re.findall(r'products/category/([a-z0-9-]+/\d+)', r.text))))
r = _get("https://beta.devoto.com.uy/products/category/9115")
print("BETA", r.status_code, r.url, len(r.text), "__NEXT_DATA__" in r.text, sorted(set(re.findall(r'https?://[a-z0-9.-]+/(?:api|v\d)[^"\'\s<>]{0,90}', r.text)))[:15])
