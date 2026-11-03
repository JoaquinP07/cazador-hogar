import sys; sys.path.insert(0, ".")
from cazador.tiendas import fenicio
for c in ["ferreteria/jardin", "hogar-muebles-y-jardin/muebles-de-jardin", "hogar-muebles-y-jardin/parrillas-y-accesorios", "hogar-muebles-y-jardin/camping", "ferreteria", "hogar-muebles-y-jardin"]:
    ps = fenicio("AMV Store", "https://amvstore.com.uy", [c])
    print("AMVCAT", c, len(ps), ps[0].nombre if ps else "", ps[0].precio if ps else "", ps[0].moneda if ps else "", ps[0].url if ps else "")
