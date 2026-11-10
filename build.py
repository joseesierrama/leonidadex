#!/usr/bin/env python3
"""Genera la web estática de LeonidaDex en site/ (para GitHub Pages o cualquier hosting).

- index.html: la enciclopedia interactiva con los datos integrados.
- Páginas estáticas para buscadores: noticias, reportajes (una por artículo), personajes,
  regiones de Leonida y preguntas frecuentes, con títulos, descripciones y datos estructurados.
- sitemap.xml, robots.txt, 404.html y CNAME (si existe dominio.txt).

Variables de entorno opcionales: BASE_URL (p. ej. https://leonidadex.net/), OWNER y REPO (GitHub).
No modifica los datos: la fecha de actualización la pone quien edita src/actualizaciones.json.
"""
import html
import json
import os
import pathlib
import re
import shutil
from site_support import analytics, footer as site_footer, head as site_head, info_pages, load_config, menu, privacy_ready
from content_validation import validate_content

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"
E = html.escape
CONFIG = load_config(SRC)


def base_url():
    dom = (ROOT / "dominio.txt").read_text("utf-8").strip() if (ROOT / "dominio.txt").exists() else ""
    if dom:
        return "https://" + dom.strip("/") + "/", dom
    if os.environ.get("BASE_URL"):
        return os.environ["BASE_URL"].rstrip("/") + "/", ""
    owner, repo = os.environ.get("OWNER", ""), os.environ.get("REPO", "")
    if owner and repo:
        if repo.lower() == f"{owner.lower()}.github.io":
            return f"https://{repo.lower()}/", ""
        return f"https://{owner.lower()}.github.io/{repo}/", ""
    return "/", ""


def embed(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def fecha_larga(iso):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    y, m, d = iso[:10].split("-")
    return f"{int(d)} de {meses[int(m) - 1]} de {y}"


def shell(depth, title, desc, url, body, jsonld=None, up_override=None):
    up = up_override if up_override is not None else "../" * depth
    ld = f'<script type="application/ld+json">{embed(jsonld)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(url)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{E(url)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_ES">
<meta name="theme-color" content="#120a1c">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=IBM+Plex+Mono:wght@500&family=Schibsted+Grotesk:wght@400;500;700&family=Yellowtail&display=swap">
<link rel="stylesheet" href="{up}assets/estilo.css">
<style>.static main{{padding:56px 0 80px}}.static .list{{list-style:none;margin:0;padding:0;display:grid;gap:0}}.static .list li{{padding:18px 0;border-top:1px solid var(--line)}}.static .list h2,.static .list h3{{font-size:1.4rem;margin:4px 0 6px;transform:none;text-shadow:none}}.static .prose{{max-width:72ch}}.static .prose p,.static .prose li{{line-height:1.75;color:#f0dde8}}.static .prose h2{{font-size:1.6rem;margin:30px 0 8px;transform:none;text-shadow:none;color:var(--flamingo)}}.static h1{{font:900 clamp(2.4rem,6vw,4.2rem)/.95 var(--font-display);text-transform:uppercase;margin:0 0 10px;text-wrap:balance}}.crumbs{{font:500 .75rem/1 var(--font-mono);color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px}}.crumbs a{{color:var(--muted)}}</style>
{ld}
{site_head(up, base_url()[0])}
</head>
<body class="static">
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="topbar"><div class="wrap">
  <a class="brand" href="{up}"><img class="brand-icon" src="{up}assets/caiman-192.png" width="36" height="36" alt=""><span class="b-word">LEONIDA</span><span class="b-script">Dex</span></a>
  {menu(up)}
</div></header>
<main id="contenido" tabindex="-1"><div class="wrap">
{body}
</div></main>
<footer><div class="wrap"><p class="disclaimer">LeonidaDex es una enciclopedia hecha por fans, no oficial. No está afiliada a Rockstar Games ni a Take-Two Interactive. Grand Theft Auto y GTA VI son marcas de Take-Two Interactive.</p></div>{site_footer(up, CONFIG)}</footer>
{analytics(up, CONFIG)}
</body>
</html>
"""


def fuentes(lst):
    lst = [f for f in (lst or []) if f.get("url")]
    if not lst:
        return ""
    return '<p class="src">Fuentes: ' + " · ".join(f'<a href="{E(f["url"])}" rel="noopener" target="_blank">{E(f.get("nombre", "enlace"))}</a>' for f in lst) + "</p>"


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, "utf-8")


def main():
    base = json.loads((SRC / "base.json").read_text("utf-8"))
    dyn = json.loads((SRC / "actualizaciones.json").read_text("utf-8"))
    validate_content(base, dyn)
    url, dominio = base_url()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    upd = (dyn.get("meta", {}).get("actualizado") or "")[:10]
    urls = []

    # --- index ---
    tpl = (SRC / "template.html").read_text("utf-8")
    css = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
    write("assets/estilo.css", css)
    shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
    shutil.copy(SRC / "assets" / "favicon.ico", OUT / "favicon.ico")
    write("site.webmanifest", json.dumps({"name": "LeonidaDex", "short_name": "LeonidaDex", "lang": "es",
        "start_url": "./", "scope": "./", "display": "standalone", "background_color": "#120a1c", "theme_color": "#120a1c",
        "icons": [{"src": f"assets/caiman-{size}.png", "sizes": f"{size}x{size}", "type": "image/png"} for size in (192, 512)]}, ensure_ascii=False))
    mani = json.loads((SRC / "tiles" / "mapa" / "manifest.json").read_text("utf-8"))
    idx = tpl.replace("__BASE__", embed(base)).replace("__DYN__", embed(dyn)).replace("__MANI__", embed(mani))
    head_extra = f'<link rel="canonical" href="{E(url)}">\n<meta property="og:url" content="{E(url)}">\n'
    head_extra += site_head("", url)
    idx = idx.replace("<meta name=\"theme-color\"", head_extra + "<meta name=\"theme-color\"", 1)
    links = ('<nav class="wrap" aria-label="Más en LeonidaDex" style="padding:0 0 24px;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.88rem">'
             '<a href="noticias/">Todas las noticias</a><a href="reportajes/">Reportajes</a><a href="personajes/">Personajes</a>'
             '<a href="leonida/">Regiones de Leonida</a><a href="preguntas-frecuentes/">Preguntas frecuentes</a></nav>\n</footer>')
    idx = idx.replace("</footer>", links, 1)
    idx = idx.replace("</footer>", site_footer("", CONFIG) + "</footer>", 1)
    idx = idx.replace("</body>", analytics("", CONFIG) + "\n</body>", 1)
    write("index.html", idx)
    write("datos/actualizaciones.json", json.dumps(dyn, ensure_ascii=False, indent=2) + "\n")
    # Mapa: teselas y puntos de GTADB (CC BY 4.0, https://map.gtadb.org)
    shutil.copytree(SRC / "tiles" / "mapa", OUT / "mapa")
    (OUT / "mapa" / "manifest.json").unlink()
    shutil.copy(SRC / "tiles" / "datos" / "gtadb-6.json", OUT / "datos" / "gtadb-6.json")
    urls.append((url, upd))

    # --- noticias ---
    news = sorted(dyn.get("noticias", []), key=lambda n: n.get("fecha", ""), reverse=True)
    items = "".join(
        f'<li id="{E(n["id"])}"><span class="news-date">{E(fecha_larga(n["fecha"]))} · {E(n.get("categoria", ""))}</span>'
        f'<h2>{E(n["titulo"])}</h2><span class="badge {E(n.get("estado", ""))}">{E(n.get("estado", ""))}</span><p>{E(n.get("resumen", ""))}</p>{fuentes(n.get("fuentes"))}</li>'
        for n in news)
    body = f'<p class="crumbs"><a href="../">LeonidaDex</a> › Noticias</p><div class="sec-head"><p class="eyebrow">Noticias</p><h1>Noticias de GTA VI</h1><p class="lede">Todas las novedades de Grand Theft Auto VI en español, de la más reciente a la más antigua, con su fuente. Actualizado el {E(fecha_larga(upd)) if upd else ""}.</p></div><ul class="list">{items}</ul>'
    u = url + "noticias/"
    write("noticias/index.html", shell(1, "Noticias de GTA VI en español | LeonidaDex", "Noticias de GTA VI: lanzamiento, tráileres, retrasos, reservas y jugabilidad, con enlaces a sus fuentes y fecha de actualización.", u, body,
                                       {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Noticias de GTA VI", "url": u, "inLanguage": "es"}))
    urls.append((u, upd))

    # --- proyecto, contacto y privacidad (solo con datos reales del titular) ---
    for slug, (title, desc, text) in info_pages(CONFIG).items():
        u = url + slug + "/"
        body = (f'<p class="crumbs"><a href="../">LeonidaDex</a> › {E(title)}</p>'
                f'<article class="prose"><h1>{E(title)}</h1>{text}</article>')
        write(f"{slug}/index.html", shell(1, title + " | LeonidaDex", desc, u, body))
        urls.append((u, ""))

    # --- reportajes ---
    arts = list(dyn.get("articulos_nuevos", [])) + list(base.get("articulos", []))
    lis = "".join(f'<li><span class="news-date">{E(a.get("categoria", ""))} · {a.get("lectura", 3)} min</span><h2><a href="{E(a["id"])}/">{E(a["titulo"])}</a></h2><p>{E(a.get("entradilla", ""))}</p></li>' for a in arts)
    u = url + "reportajes/"
    write("reportajes/index.html", shell(1, "Reportajes sobre GTA VI | LeonidaDex", "Reportajes en español sobre GTA VI: la historia del desarrollo, los retrasos, qué edición comprar, cómo se juega, las filtraciones y los récords.", u,
                                         f'<p class="crumbs"><a href="../">LeonidaDex</a> › Reportajes</p><div class="sec-head"><p class="eyebrow">Reportajes</p><h1>Reportajes a fondo</h1></div><ul class="list">{lis}</ul>'))
    urls.append((u, upd))
    for a in arts:
        blocks = []
        for x in a.get("cuerpo", []):
            if "h" in x:
                blocks.append(f"<h2>{E(x['h'])}</h2>")
            elif "ul" in x:
                blocks.append("<ul>" + "".join(f"<li>{E(i)}</li>" for i in x["ul"]) + "</ul>")
            else:
                blocks.append(f"<p>{E(x.get('p', ''))}</p>")
        body = (f'<p class="crumbs"><a href="../../">LeonidaDex</a> › <a href="../">Reportajes</a></p><article class="prose"><span class="badge">{E(a.get("categoria", ""))}</span>'
                f'<h1>{E(a["titulo"])}</h1><p class="lede">{E(a.get("entradilla", ""))}</p>{"".join(blocks)}{fuentes(a.get("fuentes"))}</article>')
        u = url + f"reportajes/{a['id']}/"
        write(f"reportajes/{a['id']}/index.html", shell(2, f"{a['titulo']} | LeonidaDex", a.get("entradilla", ""), u, body,
                                                        {"@context": "https://schema.org", "@type": "Article", "headline": a["titulo"], "description": a.get("entradilla", ""), "datePublished": a.get("fecha", upd), "inLanguage": "es",
                                                         "author": {"@type": "Organization", "name": "LeonidaDex"}, "publisher": {"@type": "Organization", "name": "LeonidaDex"}, "mainEntityOfPage": u}))
        urls.append((u, a.get("fecha", upd)))

    # --- personajes ---
    lis = "".join(f'<li id="{E(p["id"])}"><span class="news-date">{E(p.get("rol", ""))}</span><h2>{E(p["nombre"])}</h2><p>{E(p.get("bio", ""))}</p><p class="note">Visto en: {E(p.get("visto", ""))}</p>{fuentes(p.get("fuentes"))}</li>' for p in base.get("personajes", []))
    u = url + "personajes/"
    write("personajes/index.html", shell(1, "Personajes de GTA VI: Jason, Lucia y el resto | LeonidaDex", "Quién es quién en GTA VI: Jason Duval, Lucia Caminos y los personajes que ha presentado Rockstar, con lo que se sabe de cada uno.", u,
                                         f'<p class="crumbs"><a href="../">LeonidaDex</a> › Personajes</p><div class="sec-head"><p class="eyebrow">Personajes</p><h1>Personajes de GTA VI</h1></div><ul class="list">{lis}</ul>'))
    urls.append((u, upd))

    # --- regiones ---
    lis = "".join(f'<li id="{E(r["id"])}"><span class="news-date">Inspirada en: {E(r.get("inspiracion", ""))}</span><h2>{E(r["nombre"])}</h2><p><em>{E(r.get("lema", ""))}</em></p><p>{E(r.get("texto", ""))}</p>'
                  f'<p><strong>Lugares:</strong> {E(", ".join(r.get("lugares", [])))}. <strong>Qué hacer:</strong> {E(", ".join(r.get("actividades", [])))}.</p>{fuentes(r.get("fuentes"))}</li>' for r in base.get("regiones", []))
    u = url + "leonida/"
    write("leonida/index.html", shell(1, "Mapa de GTA VI: las regiones de Leonida | LeonidaDex", "Las seis regiones de Leonida en GTA VI: Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia y Mount Kalaga, con sus lugares confirmados.", u,
                                      f'<p class="crumbs"><a href="../">LeonidaDex</a> › Leonida</p><div class="sec-head"><p class="eyebrow">El estado de Leonida</p><h1>Las regiones de Leonida</h1><p class="lede"><a href="../#mapa">Abrir el mapa interactivo</a></p></div><ul class="list">{lis}</ul>'))
    urls.append((u, upd))

    # --- preguntas frecuentes ---
    faq = base.get("faq", [])
    lis = "".join(f'<li><h2>{E(q["q"])}</h2><p>{E(q["a"])}</p>{fuentes(q.get("fuentes"))}</li>' for q in faq)
    u = url + "preguntas-frecuentes/"
    write("preguntas-frecuentes/index.html", shell(1, "GTA VI: preguntas frecuentes (fecha, hora, precio, PC) | LeonidaDex", "Respuestas rápidas sobre GTA VI: cuándo sale en España y a qué hora, precio, ediciones, precarga, PC, online y más.", u,
                                                   f'<p class="crumbs"><a href="../">LeonidaDex</a> › Preguntas frecuentes</p><div class="sec-head"><p class="eyebrow">FAQ</p><h1>Preguntas frecuentes sobre GTA VI</h1></div><ul class="list">{lis}</ul>',
                                                   {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in faq]}))
    urls.append((u, upd))

    # --- 404, robots, sitemap, CNAME, archivos públicos ---
    write("404.html", shell(0, "Página no encontrada | LeonidaDex", "Esta página no existe.", url,
                           f'<div class="sec-head"><h1>Esta página no existe</h1><p class="lede"><a href="{E(url)}">Volver a LeonidaDex</a></p></div>', up_override=url))
    if CONFIG["adsense_publisher_id"]:
        write("ads.txt", f'google.com, {CONFIG["adsense_publisher_id"]}, DIRECT, f08c47fec0942fa0\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {url}sitemap.xml\n")
    sm = "".join(f"<url><loc>{E(u)}</loc>{f'<lastmod>{d[:10]}</lastmod>' if d else ''}</url>" for u, d in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write(".nojekyll", "")
    if dominio:
        write("CNAME", dominio + "\n")
    pub = SRC / "publico"
    if pub.exists():
        for f in pub.iterdir():
            if f.is_file():
                shutil.copy(f, OUT / f.name)
    print(f"site/ listo: {len(urls)} URLs, base {url}")
    if not privacy_ready(CONFIG):
        print("Pendiente: titular y correo de contacto. No se publican políticas incompletas ni se habilita medición.")


if __name__ == "__main__":
    main()
