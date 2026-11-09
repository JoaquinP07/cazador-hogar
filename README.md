# Cazador Hogar

Revisa precios de ferretería y artículos para el hogar en tiendas de Uruguay cada 15 minutos (GitHub Actions)
y avisa por Telegram con el bot **@cazador_hogar_joaquin_bot** cuando aparece un posible error de precio.
Cada aviso dice si es de 🔧 Ferretería, 🏠 Hogar o 🌿 Jardín.

**Tiendas:** Sodimac, Ferretería Arocena, El Dorado, AMV Store, El Emporio del Hogar, El Clon, Divino, JYSK, La Tentación, Rústico Hogar, Soho Deco,
Balton, MundoShop, Arredo, Multiahorro / Tata, Disco y Geant (estas dos últimas, solo 12 productos por categoría).

**Cuándo avisa:** cuando un producto baja 40% o más respecto a su precio habitual, o aparece nuevo con 60% o más
de descuento sobre su precio de lista. No repite el aviso del mismo producto durante 12 horas.
Una tienda recién agregada primero aprende los precios y recién avisa desde la revisión siguiente.

Es independiente del cazador de ofertas de electrónica (`JoaquinP07/cazador-ofertas`): tiene su propio bot,
su propio historial y su propia programación.

**Secretos:** `TELEGRAM_TOKEN` (token del bot) y `TELEGRAM_CHAT_ID` (número del chat), en
Settings → Secrets and variables → Actions.

**Revisión de prueba:** Actions → Cazador Hogar → Run workflow → tildar *prueba*. Manda un resumen por Telegram.

## Comandos por Telegram

El bot contesta en unos segundos (solo al chat configurado en `TELEGRAM_CHAT_ID`). En un grupo, escribí el comando con el nombre del bot (por ejemplo `/lista@cazador_hogar_joaquin_bot`).

- `/buscar taladro` → las 10 más baratas entre todas las tiendas. Con `oferta` al final, las que más bajaron; con `historico`, las que están en su precio mínimo registrado.
- `/agregar https://tienda.com.uy cats=seccion1,seccion2` → suma una tienda si usa Fenicio o Shopify. En las tiendas Fenicio hay que elegir las secciones.
- `/quitar nombre` y `/reanudar nombre` → sacan o pausan una tienda.
- `/lista` → tiendas que se revisan y cuántos productos tiene cada una.

Las tiendas agregadas y pausadas se guardan en `estado/control.json` (en el mismo caché que el historial).
