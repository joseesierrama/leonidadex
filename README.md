# LeonidaDex

Enciclopedia de fans de GTA VI en español. No oficial: no está afiliada a Rockstar Games ni a Take-Two Interactive.

- `src/template.html`: la página (diseño y código).
- `src/base.json`: contenido fijo (personajes, regiones, reportajes, Dex…).
- `src/actualizaciones.json`: noticias y todo lo que se actualiza a diario. Lo edita la tarea automática.
- `src/tiles/`: el mapa. Teselas recortadas de «GTA VI Map Tiles» (Yanis v17) y puntos de «GTA VI Landmarks Data», ambos de https://map.gtadb.org con licencia CC BY 4.0. Cada lunes la publicación vuelve a convertir los puntos desde el repositorio de GTADB con `scripts/gtadb.py`.
- `build.py`: genera la web en `site/` (portada interactiva + páginas para Google + sitemap).
- `.github/workflows/publicar.yml`: cada cambio en `main` regenera y publica la web en GitHub Pages.

## Dominio propio
Crea un archivo `dominio.txt` con el dominio (por ejemplo `leonidadex.net`) y apunta el DNS a GitHub Pages:
registros A de `@` a 185.199.108.153, 185.199.109.153, 185.199.110.153 y 185.199.111.153, y un CNAME de `www` a `USUARIO.github.io`.

## Google
Verifica el dominio en Google Search Console y envía `https://TU-DOMINIO/sitemap.xml`.
Si Search Console te da un archivo HTML de verificación, ponlo en `src/publico/`.
