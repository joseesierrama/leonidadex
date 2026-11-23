"""Build the dedicated GTA VI map from the same controls and engine as the homepage."""
import re


def page(shell, write, url, template, embed, base, dyn, manifest):
    section = re.search(r'<section class="block" id="mapa".*?</section>', template, re.S).group(0)
    section = section.split('    <div class="scale"', 1)[0] + '  </div>\n</section>'
    section = section.replace('<h2 id="h-mapa">Tu mapa de <em>GTA VI</em></h2>', '<h1 id="h-mapa">Mapa interactivo de <em>GTA VI</em></h1>')
    section = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">Busca un lugar, filtra la leyenda y marca lo que ya has completado. Tu progreso se guarda en este navegador.</p>', section, count=1, flags=re.S)
    section = re.sub(r'(href|src)="(?!https?://|#|/)([^"]+)"', r'\1="../\2"', section)
    helpers = template.split('  var $ = function', 1)[1].split('  var store =', 1)[0]
    common = template.split('  function arr(x)', 1)[1].split('  /* ---------------- Cielo', 1)[0]
    engine = template.split('  /* ---------------- Mapa (base: GTADB, CC BY 4.0) ---------------- */', 1)[1].split('  function renderScale()', 1)[0]
    script = ('(function () { "use strict";\n  var $ = function' + helpers
              + '  function arr(x)' + common
              + '\nvar reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;\n'
              + 'var BASE = ' + embed({key: base[key] for key in ('regiones', 'mapa_lugares', 'mapa_sin_ubicar')}) + ';\n'
              + 'var DYN = ' + embed({'mapa_lugares': dyn.get('mapa_lugares', [])}) + ';\n'
              + engine.replace('__MANI__', embed(manifest))
              + '\nmapInit();\n})();')
    body = section + '<div class="toast" id="toast" role="status" aria-live="polite"></div>'
    body += '<script src="../assets/mapa-progreso.js"></script><script>' + script + '</script>'
    result = shell(1, 'Mapa interactivo de GTA VI: leyenda y progreso | LeonidaDex',
                   'Explora solo GTA VI: leyenda por categorías, secretos con fuentes y marcas manuales de lugares completados. Guarda y lleva tu progreso con una copia.',
                   url + 'mapa/', body)
    result = result.replace('<body class="static">', '<body class="static map-page">')
    result = result.replace('</head>', '<link rel="stylesheet" href="../assets/mapa.css"></head>', 1)
    write('mapa/index.html', result)
    return url + 'mapa/'
