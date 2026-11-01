"""Diagnóstico 3: Brillante y paginación/categorías de Sodimac."""
import json, re, sys
sys.path.insert(0, ".")
from cazador.tiendas import _get

r = _get("https://www.brillante.com.uy/herramientas?js=1&pag=1")
i = r.text.find("precio")
print("BRI len", len(r.text), "data-total" in r.text)
for m in list(re.finditer(r"<div class=['\"]it ", r.text))[:1]:
    print("BRI it:", r.text[m.start():m.start()+2500])
if not re.search(r"<div class=['\"]it ", r.text):
    print("BRI raw:", r.text[i-1500:i+1500])

def nd(url):
    r = _get(url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    return (json.loads(m.group(1))["props"]["pageProps"] if m else None), r
base = "https://www.sodimac.com.uy/sodimac-uy/category/cat20888/Herramientas-electricas-e-inalambricas"
for q in ["?page=2", "?currentpage=2", "?pageNo=2", "?page=2&store=sodimac", "?sortBy=_score&page=2"]:
    pp, r = nd(base + q)
    if pp:
        sd = pp["searchProps"]["searchData"]
        print("SOD", q, sd.get("pagination"), [x["productId"] for x in sd["results"][:3]])
pp, r = nd(base)
print("SOD endPoints", json.dumps(pp["searchProps"]["searchData"].get("endPoints"))[:800])
for u in re.findall(r'https://[a-z.]*(?:falabella|sodimac)[a-z.]*/s/[^"\\ ]{0,120}', r.text)[:10]: print("SOD api?", u)
for c in ["cat20862", "cat20002", "cat20104", "cat20228", "cat20278", "cat20322", "cat20130", "cat20204", "cat20288"]:
    pp, r = nd(f"https://www.sodimac.com.uy/sodimac-uy/category/{c}/x")
    if not pp: print("SOD", c, r.status_code, "sin datos"); continue
    sd = pp["searchProps"]["searchData"]; cd = pp["categoryProps"]["categoryData"]["results"]
    print("SOD", c, cd.get("displayName"), sd.get("pagination"), [b["name"] for b in cd.get("breadcrumbs", [])])
pp, r = nd("https://www.sodimac.com.uy/sodimac-uy")
print("SOD home keys", list((pp or {}).keys()))
txt = r.text
print("SOD roots", sorted(set(re.findall(r'"(cat\d{5})"[^{}]{0,80}"(?:name|label|displayName)":"([^"]+)"', txt)))[:60])
