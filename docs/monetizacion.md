# Preparar LeonidaDex para monetizar

## Estado de esta entrega

- Menú móvil de las páginas interiores, enlaces de contacto/proyecto y favicon añadidos.
- Medición preparada y desactivada hasta disponer de una propiedad real y los datos del responsable.
- Políticas preparadas en el generador; no se publican con identidades o correos inventados.
- AdSense no está creado ni activado por estos cambios. No hay anuncios ni estimaciones de ingresos reales.

## Activación

1. Completar los datos autorizados del titular en `src/sitio.json` y revisar las políticas y la información legal necesaria para la actividad. El código no certifica cumplimiento normativo.
2. Crear una propiedad de Analytics para `https://leonidadex.net/`, configurar retención y opciones de privacidad, copiar su ID G-… y comprobar una visita consentida en Tiempo real. Las visitas que rechacen la medición no aparecerán en esta integración.
3. En Search Console, comprobar la propiedad correcta, enviar `/sitemap.xml` y revisar la indexación de URLs concretas. La mera existencia del sitemap no acredita indexación.
4. Crear AdSense, añadir el dominio y completar su revisión y los pasos de identidad y pagos que pida Google. El titular debe aceptar personalmente los términos y completar sus datos de cobro.
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
