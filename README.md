# LeonidaDex

Enciclopedia de fans de GTA VI en español. No oficial: no está afiliada a Rockstar Games ni a Take-Two Interactive.

- `src/template.html`: la página (diseño y código).
- `src/base.json`: contenido fijo (personajes, regiones, reportajes, Dex…).
- `src/actualizaciones.json`: noticias y novedades. Debe actualizarse y publicarse para que cambie el contenido. El proceso de publicación de este repositorio no redacta ni verifica noticias.
- `src/tiles/`: el mapa. Teselas recortadas de «GTA VI Map Tiles» (Yanis v17) y puntos de «GTA VI Landmarks Data», ambos de https://map.gtadb.org con licencia CC BY 4.0. Cada lunes la publicación vuelve a convertir los puntos desde el repositorio de GTADB con `scripts/gtadb.py`.
- `build.py`: genera la web en `site/` (portada interactiva + páginas para Google + sitemap).
- `.github/workflows/publicar.yml`: cada cambio en `main` regenera y publica la web en GitHub Pages.

## Dominio propio
Crea un archivo `dominio.txt` con el dominio (por ejemplo `leonidadex.net`) y apunta el DNS a GitHub Pages:
registros A de `@` a 185.199.108.153, 185.199.109.153, 185.199.110.153 y 185.199.111.153, y un CNAME de `www` a `USUARIO.github.io`.

## Google
Verifica el dominio en Google Search Console y envía `https://TU-DOMINIO/sitemap.xml`.
Si Search Console te da un archivo HTML de verificación, ponlo en `src/publico/`.

## Privacidad y monetización

La configuración está en `src/sitio.json`. Los campos vacíos mantienen desactivada la medición y no generan un `ads.txt` ficticio. Nunca añadas contraseñas, claves privadas ni datos bancarios a este repositorio público.

- `responsable` y `correo_contacto`: datos reales que el titular autoriza a publicar. Al completarlos, se generan `/privacidad/` y `/cookies/` y se enlazan desde todas las páginas. Revisa estos textos con los tratamientos reales y las obligaciones aplicables antes de publicar; no sustituyen una revisión jurídica ni un aviso legal completo.
- `nif` y `domicilio`: al completar ambos, se genera `/aviso-legal/` y se enlaza desde todas las páginas. Son datos públicos del titular, autorizados expresamente para su publicación en esta web y repositorio. No los cambies ni los repongas desde una plantilla como parte de las noticias diarias.
- `ga4_id`: identificador público de una propiedad real de Google Analytics (`G-…`). Requiere los datos del titular. La integración no carga Google antes de aceptar la medición; rechazarla mantiene desactivada la etiqueta. El enlace del pie permite cambiar la decisión.
- `adsense_publisher_id`: identificador público real (`pub-…`). Solo genera `/ads.txt`: **no carga anuncios ni sustituye la aprobación de AdSense**. Antes de añadir código publicitario, configura una CMP certificada y actualiza las políticas para reflejar los anuncios y proveedores reales. El diálogo propio de medición no es una CMP certificada para publicidad.
- `fecha_privacidad`: fecha de revisión de las políticas, que debe actualizarse al cambiar su contenido.

Los horarios históricos de `actualizaciones.json` no prueban que exista una tarea externa. Si se mantiene una automatización en Claude u otro servicio, comprueba allí su ejecución y sus publicaciones.

## Trabajo con Claude o Codex

GitHub guarda la versión vigente. Antes de editar, actualiza tu copia desde `main`. Trabaja en una rama, ejecuta `python -m unittest discover -s tests` y `python build.py`, revisa móvil y escritorio y publica los cambios comprobados. No edites directamente `site/`: se regenera. Evita dos agentes editando los mismos archivos a la vez.

## Seguimiento de ingresos

Consulta `docs/monetizacion.md`. Search Console mide la presencia en Google; Analytics mide visitas consentidas; AdSense muestra ingresos y pagos. Son servicios distintos.
