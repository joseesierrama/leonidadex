"""Catálogo de guías, páginas paso a paso y clips externos a petición."""
import html
import hashlib
import json
import math
import re
from datetime import datetime
from urllib.parse import urlsplit

E=html.escape
ICONS={'Primeros pasos':'01','Dinero':'$','Armas':'✚','Coches':'↗','Herramientas':'⌁','Exploración':'⌖','Secretos':'?'}

def asset_name(src,name):
    stem,extension=name.rsplit('.',1)
    version=hashlib.sha256((src/'assets'/name).read_bytes()).hexdigest()[:12]
    return f'{stem}.{version}.{extension}'

def community_links():
    return ('<section class="gv-social" aria-label="La comunidad de LeonidaDex">'
            '<p class="eyebrow">Sigue explorando con nosotros</p><h2>El siguiente hallazgo, en vídeo</h2>'
            '<p>¿Te ha servido esta guía? Síguenos para encontrar más rutas, secretos y retos de GTA VI, '
            'y vuelve al mapa cuando quieras hacerlos en tu partida.</p><div class="gv-social-links">'
            '<a class="btn btn-primary" href="https://www.tiktok.com/@leonidadex.net" target="_blank" rel="noopener noreferrer">Síguenos en TikTok ↗</a>'
            '<a class="btn btn-ghost" href="https://www.youtube.com/channel/UCLL3PsFZZ8sPMsRsQgTPJhg" target="_blank" rel="noopener noreferrer">Ver nuestros Shorts ↗</a>'
            '</div><small>Perfiles oficiales de LeonidaDex. Los vídeos de otros autores incluidos en las guías mantienen su crédito.</small></section>')

def load_guides(src):
    data=json.loads((src/'guias.json').read_text('utf-8'))
    if datetime.fromisoformat(data['actualizado']).tzinfo is None:
        raise ValueError('Las guías necesitan fecha con zona horaria')
    ids=set()
    for g in data['guias']:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',g.get('id','')) or g['id'] in ids:
            raise ValueError('ID de guía inválido o duplicado')
        ids.add(g['id'])
        if any(not g.get(k) for k in ('titulo','resumen','requisitos','recompensa','pasos','fuentes')):
            raise ValueError('Guía incompleta: '+g['id'])
        if len(g['pasos'])<3 or any(not p.get('titulo') or not p.get('texto') for p in g['pasos']):
            raise ValueError('La guía necesita pasos completos: '+g['id'])
        if g.get('mapa') and not re.fullmatch(r'[a-z0-9-]+',g['mapa']):
            raise ValueError('Marcador inválido')
        for f in g['fuentes']:
            parsed=urlsplit(f.get('url',''))
            if parsed.scheme!='https' or not parsed.netloc:
                raise ValueError('Fuente de guía insegura')
        if 'video' in g:
            v=g['video']
            if not re.fullmatch(r'[A-Za-z0-9_-]{11}',v.get('id','')):
                raise ValueError('Vídeo de guía inválido')
            a,b=v.get('inicio'),v.get('fin')
            if type(a) is not int or type(b) is not int or a<0 or (b and b<=a):
                raise ValueError('Intervalo de vídeo inválido')
            if not 1<=g.get('paso_video',0)<=len(g['pasos']):
                raise ValueError('El clip debe acompañar un paso existente')
    for g in data['guias']:
        if any(x not in ids or x==g['id'] for x in g.get('relacionadas',[])):
            raise ValueError('Guía relacionada inexistente')
    return data

def minutes(g):
    words=' '.join(p['texto'] for p in g['pasos']).split()
    return max(1,math.ceil(len(words)/170))

def card(g,up=''):
    video='<span class="gh-video-badge">▶ Con vídeo</span>' if g.get('video') else '<span class="gh-text-badge">Paso a paso</span>'
    spoiler='<span class="gh-spoiler-badge">Con pistas de juego</span>' if g.get('spoiler') else ''
    search=' '.join([g['titulo'],g['resumen'],g['categoria'],g['zona']])
    return (f'<article class="gh-card" data-guide-card data-category="{E(g["categoria"])}" data-has-video="{int(bool(g.get("video")))}" data-search="{E(search)}">'
            f'<div class="gh-card-top"><span class="gh-glyph" aria-hidden="true">{ICONS.get(g["categoria"],"◆")}</span><span class="gh-category">{E(g["categoria"])}</span>{video}</div>'
            f'<h2><a href="{up}{E(g["id"])}/">{E(g["titulo"])}</a></h2><p>{E(g["resumen"])}</p>'
            f'<div class="gh-card-bottom"><span>{len(g["pasos"])} pasos · {minutes(g)} min de lectura</span>{spoiler}</div>'
            f'<a class="gh-card-link" href="{up}{E(g["id"])}/" aria-label="Abrir guía: {E(g["titulo"])}">Abrir guía <span aria-hidden="true">↗</span></a></article>')

def home_preview(data):
    selected=['primeros-pasos','alijo-loro','pistola-silenciador','registrar-coche','cajas-fuertes','taxi-viaje-rapido']
    by_id={g['id']:g for g in data['guias']}
    return ('<div class="gh-home-intro"><div><p class="eyebrow">Encuentra tu siguiente objetivo</p>'
            '<p>Dinero, armas, coches y herramientas. Abre una guía para ver requisitos, pasos, clips y qué revisar si te atascas.</p></div>'
            f'<a class="btn btn-primary" href="guias/">Ver las {len(data["guias"])} guías →</a></div>'
            '<div class="gh-grid gh-home-grid">'+''.join(card(by_id[i],'guias/') for i in selected)+'</div>'
            '<p class="note gh-home-end">Los vídeos se cargan cuando eliges reproducirlos. Cada recorrido mantiene su autor y sus fuentes.</p>')

def clip_html(v,gid):
    a,b=v['inicio'],v['fin']
    fmt=lambda n:f'{n//60}:{n%60:02}'
    interval=f'{fmt(a)}–{fmt(b)}' if b else 'Recorrido completo'
    url=f'https://www.youtube.com/watch?v={v["id"]}&t={a}s'
    return (f'<section class="gv-clip" id="clip-{E(gid)}" data-video-block data-video-id="{E(v["id"])}" data-start="{a}" data-end="{b}" data-title="{E(v["titulo"])}">'
            '<div class="gv-player" data-video-player>'
            '<div class="gv-poster"><span class="gv-play-icon" aria-hidden="true">▶</span><span class="gh-category">Así se hace</span>'
            f'<h3>{E(v["titulo"])}</h3><p>{E(v["autor"])} · {interval}</p>'
            f'<button class="btn btn-primary" type="button" data-load-video aria-label="Reproducir clip: {E(v["titulo"])}">Reproducir clip</button></div></div>'
            '<p class="gv-video-note">Al reproducir conectas con YouTube en modo de privacidad mejorada. El vídeo conserva su audio original; los pasos están explicados en español.</p>'
            f'<p class="gv-video-links"><a href="{E(url)}" target="_blank" rel="noopener noreferrer">Abrir original en YouTube ↗</a>'
            '<span data-video-reset-slot></span></p><p class="gv-video-note">Si YouTube no permite verlo aquí, usa el enlace al original.</p></section>')

def page_body(g,data):
    gid=g['id'];v=g.get('video');has_gate=bool(g.get('spoiler'))
    date=datetime.fromisoformat(g['actualizado']).strftime('%d/%m/%Y')
    top=(f'<p class="crumbs"><a href="../../">LeonidaDex</a> › <a href="../">Guías</a> › {E(g["categoria"])}</p>'
         f'<article class="gv-guide" data-guide-id="{E(gid)}"><header class="gv-header"><div class="gh-card-top">'
         f'<span class="gh-glyph" aria-hidden="true">{ICONS.get(g["categoria"],"◆")}</span><span class="gh-category">{E(g["categoria"])}</span>'
         +('<span class="gh-video-badge">▶ Vídeo dentro</span>' if v else '')+'</div>'
         f'<h1>{E(g["titulo"])}</h1><p class="lede">{E(g["resumen"])}</p><p class="gv-date">Revisada el {date} · PS5 y Xbox Series X|S · {minutes(g)} min de lectura</p>'
         '<div class="gv-actions"><a class="btn btn-primary" href="#pasos" data-reveal-guide>Ver los pasos ↓</a>'
         +(f'<a class="btn btn-ghost" href="#clip-{E(gid)}" data-reveal-guide>▶ Ver el vídeo</a>' if v else '')
         +(f'<a class="btn btn-ghost" href="../../#l={E(g["mapa"])}">Zona en el mapa ↗</a>' if g.get('mapa') else '')+'</div></header>')
    brief=('<div class="gv-brief"><section><h2>Antes de empezar</h2><ul>'+''.join(f'<li>{E(x)}</li>' for x in g['requisitos'])+'</ul></section>'
           f'<section><h2>Qué consigues</h2><p>{E(g["recompensa"])}</p></section><section><h2>Dónde</h2><p>{E(g["zona"])}</p></section></div>')
    if g.get('mapa'):
        brief+='<p class="gv-location-note">El botón del mapa abre una referencia de zona. La ficha indica su precisión; no la confundas con el punto exacto de recogida.</p>'
    steps=[]
    for n,p in enumerate(g['pasos'],1):
        controls=''
        if p.get('controles'):
            controls='<dl class="gv-controls">'+''.join(f'<div><dt>{E(k)}</dt><dd>{E(text)}</dd></div>' for k,text in p['controles'].items())+'</dl>'
        video=clip_html(v,gid) if v and n==g['paso_video'] else ''
        steps.append(f'<li id="paso-{n}" class="gv-step"><div class="gv-step-heading"><span class="gv-step-number" aria-hidden="true">{n:02}</span>'
                     f'<h3>{E(p["titulo"])}</h3><label class="gv-done"><input type="checkbox" data-step="{n}" aria-label="Completado: {E(p["titulo"])}">Hecho</label></div>'
                     f'<p>{E(p["texto"])}</p>{controls}{video}</li>')
    content='<section id="pasos"><h2 class="gv-section-heading">Paso a paso</h2><ol class="gv-steps">'+''.join(steps)+'</ol></section>'
    content+='<section id="si-no-sale" class="gv-troubleshoot"><h2>Si no te sale</h2><ul>'+''.join(f'<li>{E(x)}</li>' for x in g['problemas'])+'</ul></section>'
    if has_gate:
        content=('<details class="gv-spoilers" data-guide-spoilers><summary><span>Mostrar ubicación y pasos</span>'
                 f'<small>{E(g["spoiler"])}</small></summary>{content}</details>')
    toc=('<aside class="gv-toc"><p class="gh-category">En esta guía</p><nav aria-label="Índice de esta guía">'
         +''.join(f'<a href="#paso-{n}" data-reveal-guide>{n}. {E(p["titulo"])}</a>' for n,p in enumerate(g['pasos'],1))
         +'<a href="#si-no-sale" data-reveal-guide>Si no te sale</a><a href="#fuentes-guia">Fuentes y revisión</a></nav>'
         f'<p class="gv-progress" aria-live="polite" data-guide-progress>0 de {len(g["pasos"])} pasos marcados</p><button type="button" class="gv-reset-progress" data-reset-guide>Desmarcar pasos</button>'
         '<p class="note">Tu lista se guarda solo en este navegador.</p></aside>')
    sources='<section id="fuentes-guia" class="gv-sources"><h2>Fuentes y revisión</h2><ul>'+''.join(f'<li><a href="{E(f["url"])}" target="_blank" rel="noopener noreferrer">{E(f["nombre"])} ↗</a></li>' for f in g['fuentes'])+'</ul>'
    sources+='<p>Recopilación editorial de recorridos documentados. LeonidaDex no presenta estas rutas como pruebas propias en consola. Cada vídeo conserva su autor original.</p></section>'
    by_id={x['id']:x for x in data['guias']}
    related=g.get('relacionadas',[])[:3]
    recommendations='<section class="gv-related"><p class="eyebrow">Tu siguiente parada</p><h2>Sigue con estas guías</h2><div class="gh-grid">'+''.join(card(by_id[x],'../') for x in related)+'</div></section>' if related else ''
    return top+brief+'<div class="gv-layout"><div class="gv-main">'+content+sources+'</div>'+toc+'</div>'+community_links()+recommendations+'<a class="gv-back" href="../">← Volver a todas las guías</a></article>'

def pages(shell,write,url,src):
    data=load_guides(src);guides=data['guias'];nvideo=sum('video' in g for g in guides)
    cats=list(dict.fromkeys(g['categoria'] for g in guides))
    body=('<p class="crumbs"><a href="../">LeonidaDex</a> › Guías</p><header class="gh-hero"><div><p class="eyebrow">Juega. Descubre. Vuelve a por más.</p>'
          '<h1>¿Qué quieres hacer<br><em>en Leonida?</em></h1><p class="lede">Elige un objetivo. Te llevamos de los requisitos al último paso, con vídeos donde ayudan y soluciones para los atascos.</p>'
          '<a class="btn btn-primary" href="primeros-pasos/">Estoy empezando →</a></div>'
          f'<div class="gh-hero-stats"><div><b>{len(guides)}</b><span>guías listas</span></div><div><b>{nvideo}</b><span>con vídeo</span></div><div><b>{len(cats)}</b><span>temas para elegir</span></div></div></header>'
          '<section class="gh-catalog" aria-label="Catálogo de guías"><form class="gh-filters" data-guide-filters hidden role="search" aria-label="Buscar guías">'
          '<label class="gh-search-label" for="guide-search">Encuentra lo que necesitas<input type="search" id="guide-search" placeholder="Prueba: dinero, silenciador, coche, taxi…" autocomplete="off"></label>'
          '<div class="gh-filter-bottom"><div class="gh-category-chips" role="group" aria-label="Filtrar por tema">'
          +''.join(f'<button type="button" class="gh-filter" data-category-filter="{E(c)}" aria-pressed="{str(c=="Todas").lower()}">{E(c)}</button>' for c in ['Todas']+cats)
          +'</div><label class="gh-video-only"><input type="checkbox" id="guide-video-only">Solo con vídeo</label></div></form>'
          f'<p class="gh-result-count" role="status" data-guide-count>{len(guides)} guías disponibles</p><div class="gh-grid" data-guide-grid>'+''.join(card(g) for g in guides)+'</div>'
          '<div class="gh-empty" data-guide-empty hidden><h2>No hay guías con esos filtros</h2><p>Prueba con una palabra más corta o vuelve a mostrar todas.</p><button type="button" class="btn btn-ghost" data-clear-filters>Quitar filtros</button></div></section>'
          '<section class="gh-support"><h2>¿El problema está antes de jugar?</h2><p>Estas páginas te ayudan con instalación, idioma y acceso al juego.</p><div><a href="../reportajes/noche-de-lanzamiento/">Instalación y primera partida →</a><a href="../reportajes/gta6-no-abre-ps5/">El juego no abre en PS5 →</a><a href="../reportajes/idiomas-gta6/">Voces y subtítulos →</a><a href="../reportajes/trucos-gta6-codigos-desbloqueo/">Códigos y requisitos →</a></div></section>'+community_links())
    css_name=asset_name(src,'guias.css');js_name=asset_name(src,'guias.js')
    assets=f'<link rel="stylesheet" href="../assets/{css_name}"><script src="../assets/{js_name}" defer></script>'
    text=shell(1,'Guías de GTA 6: dinero, armas, coches y secretos | LeonidaDex','Guías de GTA 6 con pasos claros, requisitos y vídeos: dinero, armas ocultas, coches, herramientas y exploración de Leonida.',url+'guias/',body,
               {'@context':'https://schema.org','@type':'CollectionPage','name':'Guías de GTA VI','url':url+'guias/','inLanguage':'es','hasPart':[{'@type':'WebPage','name':g['titulo'],'url':url+'guias/'+g['id']+'/'} for g in guides]})
    write('guias/index.html',text.replace('</head>',assets+'</head>'))
    result=[(url+'guias/',data['actualizado'])]
    for g in guides:
        u=url+'guias/'+g['id']+'/'
        text=shell(2,g['titulo']+' | Guías de GTA 6 | LeonidaDex',g['resumen'],u,page_body(g,data),
                   {'@context':'https://schema.org','@type':'Article','headline':g['titulo'],'description':g['resumen'],'datePublished':g['actualizado'],'dateModified':g['actualizado'],'inLanguage':'es','author':{'@type':'Organization','name':'LeonidaDex'},'mainEntityOfPage':u})
        assets=f'<link rel="stylesheet" href="../../assets/{css_name}"><script src="../../assets/{js_name}" defer></script>'
        write('guias/'+g['id']+'/index.html',text.replace('</head>',assets+'</head>'))
        result.append((u,g['actualizado']))
    return result
