# Cazador Hogar

Revisa precios de ferretería y artículos para el hogar en tiendas de Uruguay cada 15 minutos (GitHub Actions)
y avisa por Telegram con el bot **@cazador_hogar_joaquin_bot** cuando aparece un posible error de precio.
Cada aviso dice si es de 🔧 Ferretería o 🏠 Hogar.

**Tiendas:** Sodimac, Ferretería Arocena, El Clon, Divino, JYSK, La Tentación, Brillante, Rústico Hogar,
Balton, MundoShop, Arredo, Multiahorro / Tata, Disco y Geant (estas dos últimas, solo 12 productos por categoría).

**Cuándo avisa:** cuando un producto baja 40% o más respecto a su precio habitual, o aparece nuevo con 60% o más
de descuento sobre su precio de lista. No repite el aviso del mismo producto durante 12 horas.
Una tienda recién agregada primero aprende los precios y recién avisa desde la revisión siguiente.

Es independiente del cazador de ofertas de electrónica (`JoaquinP07/cazador-ofertas`): tiene su propio bot,
su propio historial y su propia programación.

**Secretos:** `TELEGRAM_TOKEN` (token del bot) y `TELEGRAM_CHAT_ID` (número del chat), en
Settings → Secrets and variables → Actions.

**Revisión de prueba:** Actions → Cazador Hogar → Run workflow → tildar *prueba*. Manda un resumen por Telegram.
