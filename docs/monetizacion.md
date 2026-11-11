# Preparar LeonidaDex para monetizar

## Estado de esta entrega

- Menú móvil de las páginas interiores, enlaces de contacto/proyecto y favicon añadidos.
- Medición preparada y desactivada hasta disponer de una propiedad real y los datos del responsable.
- Privacidad y almacenamiento publicados con datos autorizados. El aviso legal se genera al completar NIF y domicilio, también autorizados para su publicación.
- AdSense creado el 11 de noviembre de 2026. Perfil de pagos completado por el titular, dominio verificado mediante ads.txt y revisión solicitada. Estado de Google: Preparando. Esto no equivale a aprobación.
- Identificador real de editor configurado en `src/sitio.json`; ads.txt publicado y autorizado por Google. No hay código de anuncios ni estimaciones de ingresos reales.
- Mensaje europeo publicado en AdSense: español predeterminado, inglés adicional, caimán y enlace a privacidad, opciones de consentir/no consentir/gestionar. La etiqueta publicitaria aún no está instalada en la web; completar las políticas y comprobar la integración antes de activar anuncios tras la aprobación del sitio.

## Activación

1. Completar los datos autorizados del titular en `src/sitio.json` y revisar las políticas y la información legal necesaria para la actividad. El código no certifica cumplimiento normativo.
2. Crear una propiedad de Analytics para `https://leonidadex.net/`, configurar retención y opciones de privacidad, copiar su ID G-… y comprobar una visita consentida en Tiempo real. Las visitas que rechacen la medición no aparecerán en esta integración.
3. En Search Console, comprobar la propiedad correcta, enviar `/sitemap.xml` y revisar la indexación de URLs concretas. La mera existencia del sitemap no acredita indexación.
4. AdSense y la solicitud de revisión ya están creados. Esperar la decisión de Google y completar las verificaciones de identidad o el método de cobro que solicite en la cuenta; el alta del perfil no implica que haya cuenta bancaria verificada.
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
