# Actualizaciones diarias de LeonidaDex

GitHub es la fuente de la versión vigente. Consulta la rama `main` actual antes de editar; no repongas plantillas antiguas ni sobrescribas cambios de otros colaboradores.

## Contenido diario

- Actualiza `src/actualizaciones.json` para noticias, eventos y las listas de novedades. Mantén el formato existente, IDs únicos y estables y `meta.actualizado` con fecha, hora y zona horaria reales.
- Comprueba cada fuente antes de publicar. Una etiqueta «oficial» necesita respaldo de Rockstar o Take-Two o una atribución clara y verificable. Tener un enlace no prueba el hecho.
- No inventes detalles, fuentes, precios, fechas ni artículos para rellenar secciones. Si no hay novedades, no finjas una revisión o una fecha de actualización del contenido.
- `src/base.json` contiene datos de referencia y artículos de fondo. Revísalos cuando cambie un hecho: el contenido fijo no se actualiza por cambiar noticias.
- Si un rumor se confirma o se desmiente, conserva su fecha original y añade una corrección fechada con la fuente nueva. Revisa la FAQ, fichas de lanzamiento y reportajes relacionados para evitar contradicciones.
- Las fuentes opcionales de FAQ, personajes, regiones, sistemas y música se muestran al publicar. `fuentes_secciones` enlaza referencias por sección. Mantén estas atribuciones y distingue versión nativa, streaming y datos de avances.
- Si completas una guía o misión, revisa también cualquier descripción estática que todavía la anuncie como pendiente. Evita duplicar IDs de `base.json` en listas nuevas.

## Conservar la configuración del sitio

- Mantén el menú móvil de las páginas interiores, el favicon, los enlaces de proyecto/contacto y la configuración de `src/sitio.json`.
- No añadas identificadores de Analytics o AdSense inventados ni actives seguimiento sin la configuración y consentimiento adecuados.
- El diálogo de medición propio no es una CMP certificada de publicidad. No actives AdSense antes de integrar una CMP apropiada y actualizar privacidad/cookies.
- No modifiques datos del titular, privacidad, publicidad ni pago como parte de una actualización de noticias.
- El titular eligió el caimán ilustrado sin gafas. Conserva los iconos `src/assets/caiman-*.png`, `favicon.ico`, la imagen social y sus referencias salvo petición expresa. El SVG LD fue una propuesta descartada.

## Antes de publicar

1. Ejecuta `python -m unittest discover -s tests`, `node --test tests/consent.test.cjs tests/guides.test.cjs` y `python build.py`.
2. Revisa el cambio y que las fuentes realmente respalden las afirmaciones. Las pruebas automáticas solo validan estructura y funcionamiento, no veracidad.
3. No edites `site/` directamente: es el resultado generado.
4. Publica los cambios comprobados en GitHub. Un cambio en `main` ejecuta comprobaciones y la publicación en Pages. Comprueba que ambos trabajos terminen correctamente y verifica la web pública.

La programación diaria debe estar configurada en la tarea de Claude. El flujo de este repositorio publica cambios y actualiza el mapa semanalmente; no ejecuta Claude ni genera noticias por sí solo. Este documento orienta a Claude cuando lo lea, pero no configura su tarea externa ni garantiza que esté activa.

## Redes y retos

- Conserva `promotion_pages.py`, los retos de `/retos/` y las entradas `/tiktok/` y `/youtube/`. Estas dos entradas añaden etiquetas UTM solo al llegar desde redes; no añadas UTM a enlaces internos.
- Los eventos `ld_map_open`, `ld_character_open`, `ld_quiz_start` y `ld_quiz_complete` se envían únicamente con consentimiento de medición. No añadas textos de búsquedas, nombres o correos a sus parámetros.
- El reto debe funcionar también cuando se rechaza la medición. Revisa las preguntas contra fuentes oficiales si cambian las fichas.
- Conserva la apertura del reto con `?reto=regiones` o `?reto=personajes`, los botones para compartir el resultado y `src/assets/retos-social.jpg`. Solo el visitante elige destinatario y confirma un envío; no añadas envíos automáticos. Las etiquetas UTM de compartir se usan en enlaces externos, no en la navegación interna.


## Especial de críticas publicado el 18 de noviembre

- Los reportajes `criticas-y-notas-gta6` y `primeras-horas-gta6` están en `src/actualizaciones.json`. Mantén fuentes, escalas originales y separación entre notas de crítica y usuarios. Las partidas de un crítico no son mediciones propias ni garantizan duración o rendimiento universal.
- El bloque `.review-spotlight` de `src/template.html` y su fecha deben actualizarse junto con las medias del reportaje y la noticia correspondiente, solo tras volver a consultar Metacritic y OpenCritic. No presentes las cifras del 18 de noviembre a las 14:00 CET como una consulta posterior.
- Conserva `fecha` como fecha original de los reportajes revisados y añade `actualizado` con fecha y zona horaria reales. El constructor utiliza este campo en dateModified y en el sitemap.
- La revisión del mapa del 18 de noviembre compara 3.340 puntos y 136 áreas con la copia del 16: seis altas, cinco registros modificados (dos con nuevas coordenadas) y ninguna baja. No equivale a un mapa oficial verificado dentro del juego.


## Guías de secretos, historia y trucos del 18 de noviembre

- Los reportajes con campo `spoiler` ocultan su cuerpo bajo un desplegable nativo cerrado, tanto en la URL individual como en el lector de la portada. Mantén títulos, entradillas y noticias sin soluciones de historia. Nunca abras esos desplegables por defecto.
- Los tres trucos actuales coinciden en PC Gamer y PowerPyx; son códigos publicados por prensa, no probados por LeonidaDex. Conserva requisitos y aviso sobre guardado/trofeos. No rellenes combinaciones que la fuente marque como desconocidas.
- La actividad temprana procede de la guía de meditación de PowerPyx. Su posible requisito para Positive Mental Attitude sigue pendiente de confirmación; no lo conviertas en un trofeo perdible seguro.
- Las guías de dinero para progreso y taxi se atribuyen a PowerPyx. No extrapoles el objetivo de un capítulo a cualquier bloqueo ni presentes el suplemento de viaje rápido como precio total.
- No hay hallazgos paranormales comprobados en esta revisión. Solo añade secretos con evidencia del juego y su procedencia; las hipótesis siguen siendo teorías.


## Lanzamiento del 19 de noviembre

- La portada y `meta.fase` indican que el juego nativo ya está disponible. Conserva las fechas históricas de noticias y reportajes; `actualizado` registra revisiones reales.
- El mapa del día 19 contiene 3.651 puntos y 137 áreas de GTADB. La comparación con el día 18 da 311 altas, 45 registros revisados, 32 cambios de coordenadas y ninguna baja. Mantén la licencia y el alcance comunitario: no son comprobaciones propias ni cartografía oficial.
- El especial y la portada recogen 99/100 en Metacritic (PS5) y 99/100 en OpenCritic, consultados el 19. Actualiza ambos juntos tras volver a leer las fuentes; no confundas medias de crítica con notas de usuarios.
- Los seis códigos coinciden en dos guías. Los requisitos que PC Gamer deja en blanco se atribuyen a PowerPyx. Guarda las advertencias sobre guardado y trofeos.
- Las nuevas guías de Kirk y dinero conservan `spoiler`; no muestres sus cuerpos en búsquedas ni abras los desplegables por defecto. La guía de Kirk explica el inicio y no el desenlace.
- El estado de PSN es una observación puntual fechada. No lo muestres como una monitorización en directo ni atribuyas cualquier error local a una caída.
- La página de música aún mostraba Pre-Save en esta consulta; no convertir una fecha anunciada en una confirmación de disponibilidad de todos los temas.

## Descubrimientos del 21 de noviembre

- Se conserva el mapa interactivo y sus teselas comunitarias. Los 3.663 puntos y 139 áreas de GTADB no equivalen a cartografía oficial ni a comprobaciones propias en consola. La comparación normaliza nombres de área antes de comparar índices: 12 altas, 23 registros revisados, 9 cambios de coordenadas y ninguna baja frente al día 19.
- La capa «Pistas y secretos» empieza oculta. Sus ocho marcadores son referencias de área: `exacta:false`, ancla GTADB y campo `precision` explican dónde buscar y qué falta por situar. No los conviertas en coordenadas exactas de recogida. No asignes posiciones aleatorias a secretos sin coordenadas.
- Conserva las fuentes y el aviso de spoilers de los cuatro reportajes nuevos. No prometas dinero infinito, cantidades constantes, apariciones garantizadas ni una confirmación oficial del supuesto homenaje del Penumbra FF.
- El W-22 de Fishing Shacks y el Laird 350 del Manatee Motel son armas distintas. El huevo pintado está documentado por xGarbett, pero su torre aún no está georreferenciada en este mapa: no añadas un icono al azar.

## Catálogo de guías y vídeos

- `src/guias.json` es la fuente del catálogo `/guias/`, sus páginas individuales y las tarjetas de la portada. `base.guias` y `actualizaciones.guias_nuevas` quedan como contenido histórico y ya no alimentan el catálogo. Publica las nuevas guías en el archivo nuevo.
- Cada guía necesita requisitos, zona, resultado, pasos con título y explicación, problemas frecuentes y fuentes. `guide_pages.py` genera las páginas; no edites `site/`. Los enlaces de portada, menú, búsqueda global, reportajes y fichas del mapa llevan a estas páginas.
- Los clips son reproductores originales de sus autores, con marcas de inicio y fin en segundos absolutos del vídeo. No uses un vídeo de otro lugar como demostración de una recogida. Un fin igual a cero conserva el recorrido completo. Verifica el autor y lo mostrado antes de añadir un clip.
- `src/assets/guias.js` solo crea el iframe de youtube-nocookie.com tras pulsar Reproducir. No cargues miniaturas, reproductores ni solicitudes de YouTube antes de esa elección. Mantén el crédito, el enlace al original y el botón para cerrar el reproductor.
- Los pasos de guías con `spoiler` empiezan en un desplegable cerrado. El visitante los abre desde Ver los pasos, Ver el vídeo, el índice o el desplegable. No abras las soluciones sin esa acción ni añadas sus cuerpos al buscador global.
- Los pasos marcados se guardan bajo `ldx-guia:…`, solo en ese navegador; no envíes ese progreso ni búsquedas escritas a Analytics.
- Corrección del 21 de noviembre: la guía actual de PC Gamer distingue cajas con códigos fijos y otras que parecen variables. El reportaje anterior y el nuevo paso a paso deben mantener esa distinción.
- Robar un vehículo y registrarlo son pasos distintos. La guía de registro conserva el requisito de progreso con Moses y no promete registro disponible desde el capítulo 1.

## Revisión editorial y AdSense del 22 de noviembre

- Conserva `/criterios-editoriales/`, su enlace del pie y la autoría visible de reportajes y guías. Una atribución a un medio no equivale a una prueba propia. Las fechas de revisión editorial tampoco acreditan una nueva comprobación de todos los hechos.
- La guía `mapa-interactivo` documenta la web, no una partida en consola. Mantén su campo `plataformas`, su nota de fuentes propia y la diferencia entre nombre oficial y coordenada aproximada. El catálogo contiene ahora 21 guías.
- `guias_relacionadas` permite a un reportaje enlazar recorridos concretos; todos los IDs deben existir en `src/guias.json`. No dupliques explicaciones solo para aumentar palabras.
- La etiqueta `google-adsense-account` se deriva del ID real ya configurado. Solo verifica propiedad: no activa anuncios ni cambia el estado de revisión de Google. Mantén la ausencia de solicitudes publicitarias hasta comprobar aprobación, consentimiento e información correspondiente.
- La revisión del 19 de noviembre fue rechazada por Google según el correo. El titular indica que volvió a verificar el sitio el 22; no se ha podido confirmar su estado actual ni el motivo exacto en el panel. No describas «ads.txt autorizado» como aprobación y no elimines ni vuelvas a añadir un sitio en preparación.
- Las pruebas de navegación comprueban también archivos de scripts/imágenes, destinos y anclas internas. Consérvalas al modificar la estructura.

## Novedades del 23 de noviembre

- El catálogo contiene 25 guías. Las cuatro nuevas son `granero-rojo-apollo`, `bandito-moses`, `casa-belville` y `sombrero-arthur`; los recorridos originales de BennyCentral, Trophy Tom, xGarbett e IGN conservan su crédito e intervalos.
- La descarga actual de GTADB y la copia anterior coinciden: 3.663 puntos, 139 áreas y cero cambios. No anuncies nuevos puntos comunitarios. Se añadieron tres referencias propias de área para las guías nuevas; las once pistas empiezan ocultas. La casa de Belville sigue sin georreferencia contrastada: se incluye en lugares sin ubicar y no se coloca un icono arbitrario.
- El Bandito se mueve y requiere el encargo de Moses. El vídeo de Trophy Tom muestra una alternativa con enfrentamiento; no lo presentes como una demostración del diálogo descrito por PC Gamer y PowerPyx. La entrega y el registro para quedarse un coche son acciones distintas.
- El Genuine Cowboy Hat tiene importes distintos documentados por PC Gamer y GamesRadar. No conviertas 5 o 35 dólares en un precio universal ni confirmes teorías sobre la vendedora.
- El granero documenta recogida y venta. El respawn por guardado/carga se atribuye a Insider Gaming; no se certifica dinero infinito, cifras fijas ni funcionamiento en todas las versiones.
- El conversor de GTADB usa UTF-8 explícito tanto al leer como al escribir para mantener el mismo resultado en Windows y Linux.
