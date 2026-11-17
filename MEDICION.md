# Cómo revisar las visitas de LeonidaDex

## Enlaces de los perfiles

- TikTok: https://leonidadex.net/tiktok/
- YouTube: https://leonidadex.net/youtube/

Ambos llevan a `/retos/` con `utm_source`, `utm_medium=social`, `utm_campaign=leonida_retos` y `utm_content=perfil`. No se añade seguimiento antes del consentimiento. Las visitas sin consentimiento no aparecen en esta medición; los datos no representan a todos los visitantes.

Estos enlaces atribuyen la entrada del perfil a su red, no identifican por sí solos qué vídeo vio la persona. No se deben usar para enlaces internos: cambiarían la atribución de las campañas. Los enlaces de campañas pagadas deben conservar su etiquetado propio.

## Qué mirar en Analytics

En Informes, usa Adquisición de tráfico y la dimensión **Fuente/medio de la sesión**. Para las nuevas entradas se esperan `tiktok / social` y `youtube / social`; las visitas antiguas pueden seguir figurando como referencias o tráfico directo. Compara periodos con las mismas fechas. También puedes consultar la campaña de sesión `leonida_retos`.

En Eventos aparecen estas acciones:

| Evento | Significado |
|---|---|
| `ld_map_open` | Clic en los accesos medidos al mapa; no demuestra que se haya explorado todo |
| `ld_character_open` | Apertura de las fichas desde los retos |
| `ld_quiz_start` | Primera respuesta de un intento |
| `ld_quiz_complete` | Resultado del intento mostrado |

El parámetro `content_id` identifica `regiones`, `personajes`, `mapa` o `fichas`. `score` es una nota entre 0 y 3. No se envían respuestas escritas ni búsquedas.

`ld_quiz_complete` es un objetivo de participación: se cuenta como evento clave una vez por sesión y sin valor monetario asignado. No equivale a una venta, un ingreso ni un clic en publicidad. Los ingresos reales se consultan en AdSense una vez aprobado y activo.

## Revisión práctica

Anota para el mismo periodo las sesiones por red, retos completados, aperturas del mapa e ingresos reales menos gastos. No compares visualizaciones de TikTok con usuarios de Analytics como si fueran la misma métrica.

Las comprobaciones propias pueden aparecer como tráfico. Excluye las campañas cuyo nombre empiece por `qa_` al evaluar campañas reales. Los informes normales pueden tardar en incorporar los datos nuevos; usa Tiempo real para una primera comprobación.

La configuración de consentimiento debe conservarse al actualizar la web. No actives anuncios solo por ver un ID de editor o un archivo ads.txt: antes se necesita la aprobación de AdSense y comprobar la integración publicitaria del consentimiento.
