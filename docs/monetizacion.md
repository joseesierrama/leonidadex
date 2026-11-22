# Preparar LeonidaDex para monetizar

## Estado comprobado el 22 de noviembre de 2026

- Menú móvil de las páginas interiores, enlaces de contacto/proyecto y favicon añadidos.
- Analytics está configurado con el identificador real y solo se carga tras aceptar la medición. Rechazarla permite usar la web.
- Privacidad y almacenamiento publicados con datos autorizados. El aviso legal se genera al completar NIF y domicilio, también autorizados para su publicación.
- El registro anterior mostraba «Preparando». Un correo de Google del 19 de noviembre rechaza la preparación del sitio para mostrar anuncios. Ese correo no detalla el motivo: remite a Sitios. El titular indica que ha vuelto a verificar el sitio el 22; no se ha confirmado el estado actual ni si se envió otra solicitud de revisión. No presentar la cuenta como aprobada ni afirmar que basta con esperar.
- Identificador real de editor configurado en `src/sitio.json`; ads.txt publicado y autorizado por Google. No hay código de anuncios ni estimaciones de ingresos reales.
- En una sesión anterior se documentó un mensaje europeo configurado en AdSense, con español, inglés, caimán y opciones de consentimiento. Su configuración actual y su funcionamiento en la web aún necesitan comprobarse. El diálogo propio de Analytics no lo sustituye. No se añade código de anuncios en esta entrega.
- La etiqueta meta de verificación se genera con el ID real en todas las páginas. No hace solicitudes a servicios publicitarios. `ads.txt` continúa publicado por separado.
- Se añaden criterios editoriales, autoría visible, una guía original para usar el mapa y accesos a recorridos relacionados. Estas mejoras no identifican por sí mismas la causa del rechazo ni garantizan aprobación.

## Activación

1. Completar los datos autorizados del titular en `src/sitio.json` y revisar las políticas y la información legal necesaria para la actividad. El código no certifica cumplimiento normativo.
2. Crear una propiedad de Analytics para `https://leonidadex.net/`, configurar retención y opciones de privacidad, copiar su ID G-… y comprobar una visita consentida en Tiempo real. Las visitas que rechacen la medición no aparecerán en esta integración.
3. En Search Console, comprobar la propiedad correcta, enviar `/sitemap.xml` y revisar la indexación de URLs concretas. La mera existencia del sitemap no acredita indexación.
4. En AdSense > Sitios > leonidadex.net, leer el motivo exacto y el estado. Corregir el problema indicado antes de solicitar revisión. Verificar propiedad y pulsar «Solicitar revisión» son pasos distintos. Si aparece «En preparación», no eliminar ni volver a añadir el sitio. Completar las verificaciones de identidad o cobro que Google solicite; un perfil de pagos completo no acredita un banco verificado.
5. Configurar el consentimiento publicitario en AdSense > Privacidad y mensajes o una CMP certificada adecuada. La aceptación de medición de esta web no autoriza publicidad.
6. Añadir el ID real de editor para generar `ads.txt`. Actualizar las políticas y añadir el código publicitario una vez revisada la integración con la CMP. No colocar anuncios en secciones vacías o pendientes, ni encima de los controles del mapa.
7. Revisar el resultado en móvil y comprobar que consentimientos, anuncios y navegación funcionan antes de aumentar anuncios.

## Revisión semanal

| Dato | Dónde consultarlo | Para qué sirve |
|---|---|---|
| Clics desde Google y consultas | Search Console | Identificar búsquedas y artículos con oportunidades |
| Páginas vistas y origen del tráfico consentido | Analytics | Entender el uso del sitio |
| Ingresos estimados y RPM de página | AdSense > Informes | Comparar rendimiento publicitario |
| Incidencias de políticas y ads.txt | AdSense | Corregir problemas de publicación |

Compara periodos equivalentes (por ejemplo, los últimos 7 días con los 7 anteriores). No compares como iguales páginas vistas de Analytics y AdSense: sus condiciones de medición difieren.

Cada mes registra: ingresos finales de publicidad, otras fuentes de ingreso, gastos reales, resultado y pagos recibidos. Un pago bancario puede corresponder a ingresos de meses anteriores; no lo vuelvas a sumar como ingreso nuevo.

RPM de página = ingresos estimados / páginas vistas de AdSense × 1.000. No es una tarifa garantizada. Evita extrapolar ingresos con pocos días de datos.

## Fuentes oficiales

- Requisitos del sitio: https://support.google.com/adsense/answer/7299563?hl=es
- Privacidad: https://support.google.com/adsense/answer/1348695?hl=es
- Consentimiento publicitario: https://support.google.com/adsense/answer/13554116?hl=es
- ads.txt: https://support.google.com/adsense/answer/12171612?hl=es
- RPM de página: https://support.google.com/adsense/answer/112030?hl=es
- Ingresos estimados y finales: https://support.google.com/adsense/answer/9745?hl=es
