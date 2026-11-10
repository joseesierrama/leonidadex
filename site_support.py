"""Elementos compartidos y configuración explícita de privacidad y medición."""
import html
import json
import re

E = html.escape
MENU = [("", "Inicio"), ("noticias/", "Noticias"), ("reportajes/", "Reportajes"),
        ("personajes/", "Personajes"), ("leonida/", "Leonida"),
        ("preguntas-frecuentes/", "Preguntas frecuentes"), ("#mapa", "Mapa interactivo")]


def load_config(src):
    config = json.loads((src / "sitio.json").read_text("utf-8"))
    for key in ("responsable", "correo_contacto", "ga4_id", "adsense_publisher_id"):
        config[key] = str(config.get(key) or "").strip()
    if config["correo_contacto"] and not re.fullmatch(r"[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+", config["correo_contacto"]):
        raise ValueError("correo_contacto debe ser un correo real del titular")
    if config["ga4_id"] and not re.fullmatch(r"G-[A-Z0-9]{6,}", config["ga4_id"]):
        raise ValueError("ga4_id debe ser el identificador G-… de la propiedad real de Analytics")
    if config["adsense_publisher_id"] and not re.fullmatch(r"pub-\d{16}", config["adsense_publisher_id"]):
        raise ValueError("adsense_publisher_id debe ser el identificador pub-… real de AdSense")
    if (config["ga4_id"] or config["adsense_publisher_id"]) and not privacy_ready(config):
        raise ValueError("Completa responsable y correo_contacto antes de habilitar medición o ads.txt")
    return config


def privacy_ready(config):
    return bool(config["responsable"] and config["correo_contacto"])


def menu(up):
    links = "".join(f'<a href="{E(up + path)}">{label}</a>' for path, label in MENU)
    return (f'<nav class="nav" aria-label="Secciones">{links}</nav>'
            f'<details class="static-menu"><summary>Menú</summary><nav aria-label="Menú de secciones">{links}</nav></details>')


def footer(up, config):
    links = [("sobre-leonidadex/", "Sobre LeonidaDex"), ("contacto/", "Contacto")]
    if privacy_ready(config):
        links += [("privacidad/", "Privacidad"), ("cookies/", "Cookies y almacenamiento")]
    body = "".join(f'<a href="{E(up + path)}">{label}</a>' for path, label in links)
    if config["ga4_id"]:
        body += '<button type="button" data-privacy-open hidden>Preferencias de privacidad</button>'
    return '<nav class="wrap site-links" aria-label="Información del sitio">' + body + '</nav>'


def head(up, public_base):
    image = E(public_base + "assets/leonidadex-social.jpg")
    return (f'<link rel="icon" href="{E(up)}assets/caiman-32.png" type="image/png" sizes="32x32">\n'
            f'<link rel="icon" href="{E(up)}assets/caiman-192.png" type="image/png" sizes="192x192">\n'
            f'<link rel="apple-touch-icon" href="{E(up)}assets/caiman-180.png" sizes="180x180">\n'
            f'<link rel="manifest" href="{E(up)}site.webmanifest">\n'
            f'<meta property="og:image" content="{image}">\n'
            '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta property="og:image:alt" content="LeonidaDex: el caimán de Leonida y la guía de GTA VI en español">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:image" content="{image}">\n'
            f'<link rel="stylesheet" href="{E(up)}assets/sitio.css">\n')


def analytics(up, config):
    if not config["ga4_id"]:
        return ""
    return f'''<dialog class="privacy-dialog" id="privacyDialog" aria-labelledby="privacyTitle" aria-describedby="privacyDescription">
<h2 id="privacyTitle">Tu privacidad</h2>
<p id="privacyDescription">¿Permites que usemos Google Analytics para saber qué páginas resultan útiles? Es opcional. Puedes seguir usando la web si lo rechazas y cambiar tu decisión en el pie de página.</p>
<p><a href="{E(up)}privacidad/">Política de privacidad</a> · <a href="{E(up)}cookies/">Cookies y almacenamiento</a></p>
<div class="privacy-actions"><button type="button" id="privacyReject">Rechazar medición</button><button type="button" id="privacyAccept">Aceptar medición</button></div>
<button class="privacy-close" id="privacyClose" type="button">Continuar sin decidir</button>
</dialog>
<script src="{E(up)}assets/privacidad.js" data-ga4="{E(config['ga4_id'])}" defer></script>'''


def info_pages(config):
    contact = (f'<a href="mailto:{E(config["correo_contacto"])}">{E(config["correo_contacto"])}</a>'
               if config["correo_contacto"] else
               '<a href="https://github.com/joseesierrama/leonidadex/issues">incidencias del proyecto en GitHub</a>')
    pages = {
        "sobre-leonidadex": ("Sobre LeonidaDex", "Quién hace LeonidaDex y cómo se organiza su contenido.",
            '<h2>Una guía hecha por fans</h2><p>LeonidaDex reúne información en español sobre Grand Theft Auto VI. Es un proyecto independiente, sin afiliación con Rockstar Games ni Take-Two Interactive.</p>'
            '<h2>Fuentes y correcciones</h2><p>Las noticias distinguen información oficial, cobertura de prensa y rumores. Los enlaces permiten consultar las fuentes originales. Si una afirmación no está respaldada por la fuente indicada, puedes comunicarlo para su revisión.</p>'
            '<p>El mapa es una interpretación de la comunidad, no un mapa oficial. Se atribuyen los datos y la cartografía de GTADB y se indica su licencia.</p>'
            '<h2>Contenido en preparación</h2><p>Las secciones pendientes se completarán cuando haya información contrastada. Una sección anunciada no implica que su contenido ya esté disponible.</p>'
            '<p><a href="../contacto/">Contactar con el proyecto</a> · <a href="https://github.com/joseesierrama/leonidadex">Repositorio público</a></p>'),
        "contacto": ("Contacto", "Comunica errores y consultas sobre LeonidaDex.",
            f'<p>Para comunicar un error, una corrección de fuentes o una consulta sobre el proyecto, utiliza {contact}.</p>'
            '<p>Indica la dirección de la página y qué información necesita revisión. No envíes contraseñas, datos bancarios ni información de tus cuentas de juego.</p>'
            + ('<p>Las incidencias de GitHub son públicas. Utilízalas para errores de la web y evita incluir datos personales.</p>' if not config["correo_contacto"] else '')),
    }
    if not privacy_ready(config):
        return pages
    owner = E(config["responsable"])
    analytics_info = (
        '<p>Si aceptas la medición, Google Analytics recibe información sobre las páginas que visitas, el dispositivo y el uso del sitio. Se utiliza para mejorar la web. La base de este tratamiento es tu consentimiento; puedes retirarlo en «Preferencias de privacidad» del pie de página.</p>'
        '<p>No se carga Analytics antes de aceptar. Rechazarlo permite seguir navegando. Las señales de Google y la personalización publicitaria se mantienen desactivadas en esta integración. Google puede tratar datos fuera del Espacio Económico Europeo conforme a sus condiciones y garantías aplicables.</p>'
        if config["ga4_id"] else '<p>Esta versión de LeonidaDex no carga Google Analytics ni una herramienta de medición de visitas propia.</p>')
    pages["privacidad"] = ("Política de privacidad", "Información sobre el tratamiento de datos en LeonidaDex.",
        f'<p>Actualizada el {E(config["fecha_privacidad"])}.</p><h2>Responsable y contacto</h2><p>Responsable: {owner}. Contacto: {contact}.</p>'
        '<h2>Navegación y servicios externos</h2><p>El sitio se aloja en GitHub Pages. El proveedor puede tratar datos técnicos de conexión, como la dirección IP, para prestar y proteger el servicio. Las tipografías se solicitan a Google Fonts; el navegador establece una conexión con ese proveedor. Estos tratamientos se describen en sus políticas.</p>'
        '<p><a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">Privacidad de GitHub</a> · <a href="https://developers.google.com/fonts/faq/privacy">Privacidad de Google Fonts</a> · <a href="https://policies.google.com/privacy?hl=es">Privacidad de Google</a>.</p>'
        '<h2>Medición de visitas</h2>' + analytics_info +
        '<h2>Consultas y almacenamiento funcional</h2><p>Si escribes al contacto del proyecto, los datos de tu mensaje se utilizarán para atender tu consulta y se conservarán durante el tiempo necesario para resolverla y cumplir las obligaciones aplicables. No incluyas información sensible innecesaria.</p>'
        '<p>El progreso de guías, misiones y lugares descubiertos se conserva en tu navegador. La aplicación no lo envía a un servidor de cuentas. Puedes borrarlo desde los controles del sitio o los ajustes de tu navegador.</p>'
        '<h2>Publicidad</h2><p>Esta versión no incorpora anuncios de AdSense. Antes de activarlos se actualizará esta información y se configurará la gestión del consentimiento publicitario correspondiente.</p>'
        '<h2>Tus derechos</h2><p>Puedes solicitar el acceso, rectificación o supresión de tus datos, la limitación del tratamiento, la portabilidad y la oposición cuando proceda, utilizando el contacto indicado. También puedes retirar tu consentimiento y presentar una reclamación ante la <a href="https://www.aepd.es/">Agencia Española de Protección de Datos</a>.</p>')
    cookies_analytics = ('<tr><td>ld:consent:v1</td><td>Recordar la decisión de medición</td><td>180 días; se vuelve a solicitar al caducar</td></tr>'
                         '<tr><td>_ga y _ga_…</td><td>Cookies de Google Analytics, solo si aceptas</td><td>Hasta 180 días en esta integración, renovables con el uso</td></tr>' if config["ga4_id"] else '')
    pages["cookies"] = ("Cookies y almacenamiento", "Qué guarda LeonidaDex en tu navegador y cómo controlarlo.",
        '<p>La aplicación utiliza almacenamiento local para recordar el progreso que tú marcas. No es publicidad y no permite sincronizar tus datos entre dispositivos.</p>'
        '<div style="overflow-x:auto"><table><thead><tr><th>Nombre</th><th>Finalidad</th><th>Duración</th></tr></thead><tbody>'
        '<tr><td>gl:…</td><td>Progreso de mapa, misiones y listas</td><td>Hasta que lo borres desde la web o el navegador</td></tr>' + cookies_analytics + '</tbody></table></div>'
        + ('<p>La medición es opcional. Puedes aceptarla, rechazarla o cambiar tu decisión desde «Preferencias de privacidad», en el pie de página. Al retirarla se detiene la medición y se eliminan las cookies de Analytics accesibles para este sitio.</p>' if config["ga4_id"] else '<p>No se instalan cookies de Google Analytics ni de publicidad desde el código de esta versión.</p>') +
        '<p>Los servicios de alojamiento y los enlaces externos se rigen por sus propias políticas. Puedes bloquear o borrar cookies y almacenamiento en los ajustes de tu navegador. Borrar el almacenamiento funcional elimina el progreso guardado.</p><p><a href="../privacidad/">Política de privacidad y contacto</a>.</p>')
    return pages
