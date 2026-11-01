import sys; sys.path.insert(0, ".")
from cazador.tiendas import _get
for u in ["https://www.sodimac.com.uy/sodimac-uy/product/1003909/x/1003909", "https://www.sodimac.com.uy/sodimac-uy/product/1003909"]:
    r = _get(u, allow_redirects=True); print("URL", u, r.status_code, r.url, "Taladro" in r.text)
