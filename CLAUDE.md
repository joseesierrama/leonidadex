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

1. Ejecuta `python -m unittest discover -s tests`, `node --test tests/consent.test.cjs` y `python build.py`.
2. Revisa el cambio y que las fuentes realmente respalden las afirmaciones. Las pruebas automáticas solo validan estructura y funcionamiento, no veracidad.
3. No edites `site/` directamente: es el resultado generado.
4. Publica los cambios comprobados en GitHub. Un cambio en `main` ejecuta comprobaciones y la publicación en Pages. Comprueba que ambos trabajos terminen correctamente y verifica la web pública.

La programación diaria debe estar configurada en la tarea de Claude. El flujo de este repositorio publica cambios y actualiza el mapa semanalmente; no ejecuta Claude ni genera noticias por sí solo. Este documento orienta a Claude cuando lo lea, pero no configura su tarea externa ni garantiza que esté activa.
