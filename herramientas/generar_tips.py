"""Genera /tips/ y una página por tip a partir de herramientas/tips.json.

Uso:  python herramientas/generar_tips.py
El menú, el pie, los estilos y Analytics se copian de la página de oficinas, así las páginas de tips
quedan siempre iguales al resto del sitio. Las imágenes van en sitio/images/tips/<slug>.jpg (640 px de ancho).
Para sumar un tip: agregarlo al final de tips.json, poner su imagen y volver a correr el script.
"""
import html, json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = os.path.join(RAIZ, 'sitio')
DOMINIO = 'https://limpieza-prosol.com.ar'
FECHA = '2026-10-19'
WA = 'https://wa.me/5493815009744?text=Hola%20Prosol%2C%20quisiera%20consultar%20por%20un%20presupuesto'

tips = json.load(open(os.path.join(RAIZ, 'herramientas', 'tips.json'), encoding='utf-8'))
base = open(os.path.join(SITIO, 'limpieza-de-oficinas-tucuman', 'index.html'), encoding='utf-8').read()

# Partes comunes tomadas de la página de oficinas
cabecera_comun = base[base.index('  <link rel="preconnect"'):base.index('</head>')]
menu = base[base.index('<nav>'):base.index('</nav>') + len('</nav>')]
cola = base[base.index('<footer>'):]
cola = re.sub(r'(class="wa-flotante" href=")[^"]*', lambda m: m.group(1) + WA, cola)
WA_SVG = re.search(r'<svg width="20" height="20" viewBox="0 0 24 24" fill="white">.*?</svg>', base, re.S).group(0)

CSS_TIPS = '''  <style>
    .tips-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 1.5rem; max-width: 1100px; }
    .tip-card { background: var(--blanco); border-radius: 4px; overflow: hidden; text-decoration: none; color: var(--negro); box-shadow: 0 2px 12px rgba(0,0,0,0.06); transition: transform 0.15s, box-shadow 0.15s; display: flex; flex-direction: column; }
    .tip-card:hover { transform: translateY(-3px); box-shadow: 0 8px 26px rgba(0,0,0,0.1); }
    .tip-card img { width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; display: block; }
    .tip-card span { display: block; padding: 1rem 1.1rem 1.25rem; font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.02rem; line-height: 1.35; }
    .tip-card small { display: block; padding: 0 1.1rem 1.1rem; margin-top: auto; color: var(--naranja-texto); font-weight: 600; font-size: 0.8rem; }
    .tip-layout { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 3rem; padding: 0 5vw 3rem; max-width: 1100px; align-items: start; }
    .tip-layout section.content { padding: 0 0 1.5rem; }
    .tip-figura img { width: 100%; height: auto; display: block; border-radius: 4px; box-shadow: 0 8px 28px rgba(0,0,0,0.12); }
    .tip-figura { position: sticky; top: 84px; }
    .si-no { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 0.5rem 0 2rem; }
    .si-no div { border-radius: 4px; padding: 1.25rem 1.25rem 1rem; }
    .si-no .no { background: #F6E3E1; }
    .si-no .si { background: #E4EBDD; }
    .si-no h3 { font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.6rem; }
    .si-no .no h3 { color: var(--bordo); }
    .si-no .si h3 { color: var(--verde); }
    .si-no ul { list-style: none; }
    .si-no li { font-size: 0.93rem; margin-bottom: 0.4rem; padding-left: 1.4rem; position: relative; }
    .si-no .no li::before { content: "✗"; position: absolute; left: 0; color: var(--bordo); font-weight: 700; }
    .si-no .si li::before { content: "✓"; position: absolute; left: 0; color: var(--verde); font-weight: 700; }
    .fuentes { font-size: 0.8rem; color: var(--gris); border-top: 1px solid var(--crema-dark); padding-top: 1rem; margin-top: 0.5rem; }
    .fuentes strong { color: var(--negro); }
    .fuentes ul { margin: 0.4rem 0 0 1.1rem; }
    @media (max-width: 860px) {
      .tip-layout { grid-template-columns: 1fr; gap: 1.5rem; }
      .tip-figura { position: static; max-width: 360px; }
      .si-no { grid-template-columns: 1fr; }
    }
    @media (max-width: 560px) {
      .tips-grid { grid-template-columns: 1fr 1fr; gap: 0.75rem; }
      .tip-card span { font-size: 0.88rem; padding: 0.75rem 0.75rem 0.5rem; }
      .tip-card small { padding: 0 0.75rem 0.85rem; }
    }
  </style>
'''


def e(t):
    return html.escape(t, quote=True)


def cabecera(titulo, descripcion, url, imagen, jsonld):
    bloques = ''.join('  <script type="application/ld+json">\n' + json.dumps(j, ensure_ascii=False, indent=2) + '\n  </script>\n' for j in jsonld)
    return f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(descripcion)}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" type="image/png" href="/favicon.png" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{e(titulo)}" />
  <meta property="og:description" content="{e(descripcion)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:locale" content="es_AR" />
  <meta property="og:site_name" content="Prosol" />
  <meta property="og:image" content="{imagen}" />
  <meta name="twitter:card" content="summary_large_image" />

{bloques}
{cabecera_comun}{CSS_TIPS}</head>
<body>

{menu}
'''


def migas(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def franja_final(titulo):
    return f'''<div class="cta-band">
  <h2>{e(titulo)}</h2>
  <p>Limpieza de oficinas, locales, galerías y final de obra en todo el Gran Tucumán. Presupuesto sin cargo.</p>
  <a href="{WA}" class="btn-whatsapp" target="_blank" rel="noopener">{WA_SVG} Escribinos por WhatsApp</a>
</div>


'''


def lista_pasos(pasos):
    return '  <ol class="pasos">\n' + ''.join(f'    <li>{p}</li>\n' for p in pasos) + '  </ol>\n'


def tarjeta(t):
    return (f'<a class="tip-card" href="/tips/{t["slug"]}/"><img src="/images/tips/{t["slug"]}.jpg" width="640" height="800" '
            f'loading="lazy" alt="{e(t["alt"])}" /><span>{e(t["h1"])}</span><small>Leer el tip →</small></a>')


def pagina_tip(i, t):
    url = f'{DOMINIO}/tips/{t["slug"]}/'
    img = f'{DOMINIO}/images/tips/{t["slug"]}.jpg'
    articulo = {"@context": "https://schema.org", "@type": "Article", "headline": t['h1'], "description": t['descripcion'],
                "image": img, "datePublished": FECHA, "dateModified": FECHA, "inLanguage": "es-AR", "mainEntityOfPage": url,
                "author": {"@type": "Organization", "name": "Prosol", "url": DOMINIO + '/'},
                "publisher": {"@type": "Organization", "name": "Prosol", "logo": {"@type": "ImageObject", "url": DOMINIO + '/images/logo-nav.png'}}}
    s = cabecera(t['titulo'], t['descripcion'], url, img,
                 [articulo, migas(('Inicio', DOMINIO + '/'), ('Tips de limpieza', DOMINIO + '/tips/'), (t['h1'], url))])
    s += f'''<p class="breadcrumb"><a href="/">Prosol</a> &nbsp;/&nbsp; <a href="/tips/">Tips de limpieza</a> &nbsp;/&nbsp; {e(t["corto"])}</p>

<section class="page-hero">
  <p class="page-eyebrow">Tip de limpieza #{i}</p>
  <h1 class="page-h1">{e(t["h1"])}</h1>
  <p class="page-lead">{t["intro"]}</p>
</section>

<div class="tip-layout">
  <div>
'''
    for sec in t['secciones']:
        s += f'<section class="content">\n  <h2 class="h2">{e(sec["h2"])}</h2>\n'
        for p in sec.get('parrafos', []):
            s += f'  <p class="body-text">{p}</p>\n'
        if sec.get('pasos'):
            s += lista_pasos(sec['pasos'])
        s += '</section>\n'
    if t.get('no') or t.get('si'):
        s += '<div class="si-no">\n'
        s += '  <div class="no"><h3>No</h3><ul>' + ''.join(f'<li>{e(x)}</li>' for x in t.get('no', [])) + '</ul></div>\n'
        s += '  <div class="si"><h3>Sí</h3><ul>' + ''.join(f'<li>{e(x)}</li>' for x in t.get('si', [])) + '</ul></div>\n'
        s += '</div>\n'
    s += '<div class="fuentes"><strong>Fuentes</strong><ul>' + ''.join(f'<li>{e(f)}</li>' for f in t['fuentes']) + '</ul></div>\n'
    s += f'''  </div>
  <figure class="tip-figura"><img src="/images/tips/{t["slug"]}.jpg" width="640" height="800" alt="{e(t["alt"])}" /></figure>
</div>

'''
    otros = [x for x in tips if x['slug'] != t['slug']]
    otros = (otros[i - 1:] + otros[:i - 1])[:3]  # los 3 siguientes, en ronda
    s += '<section class="otros">\n  <h2 class="h2">Más tips de limpieza</h2>\n  <div class="tips-grid">' + ''.join(tarjeta(x) for x in otros)
    s += '</div>\n  <p style="margin-top:1.5rem;"><a href="/tips/" style="color:var(--naranja-texto);font-weight:600;">Ver todos los tips →</a></p>\n</section>\n\n'
    s += franja_final('¿No tenés tiempo? Lo hacemos nosotros')
    return s + cola


def pagina_indice():
    url = DOMINIO + '/tips/'
    titulo = 'Tips de limpieza: consejos de profesionales | Prosol Tucumán'
    descripcion = 'Consejos de limpieza verificados de Prosol, empresa de limpieza en Tucumán con más de 25 años: lavandina, mármol, vidrios, microfibra y más.'
    lista = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{DOMINIO}/tips/{t["slug"]}/', "name": t['h1']} for i, t in enumerate(tips)]}
    s = cabecera(titulo, descripcion, url, DOMINIO + '/og-image.jpg', [lista, migas(('Inicio', DOMINIO + '/'), ('Tips de limpieza', url))])
    s += '''<p class="breadcrumb"><a href="/">Prosol</a> &nbsp;/&nbsp; Tips de limpieza</p>

<section class="page-hero">
  <p class="page-eyebrow">Consejos de profesionales</p>
  <h1 class="page-h1">Tips de limpieza</h1>
  <p class="page-lead">Lo que aprendimos en más de 25 años limpiando oficinas, locales y obras en Tucumán. Solo consejos verificados, con sus fuentes, y la seguridad primero.</p>
</section>

<section style="padding:0 5vw 4rem;">
  <div class="tips-grid">''' + ''.join(tarjeta(t) for t in tips) + '''</div>
</section>

'''
    s += franja_final('¿Preferís que lo hagamos nosotros?')
    return s + cola


def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    assert '—' not in texto, ruta + ': tiene guiones largos'
    open(ruta, 'w', encoding='utf-8', newline='\n').write(texto)
    print('ok', os.path.relpath(ruta, RAIZ))


for i, t in enumerate(tips, 1):
    assert os.path.exists(os.path.join(SITIO, 'images', 'tips', t['slug'] + '.jpg')), 'falta la imagen de ' + t['slug']
    escribir(os.path.join(SITIO, 'tips', t['slug'], 'index.html'), pagina_tip(i, t))
escribir(os.path.join(SITIO, 'tips', 'index.html'), pagina_indice())

# Sitemap: reemplaza las entradas de /tips/ por las actuales
ruta_sm = os.path.join(SITIO, 'sitemap.xml')
sm = open(ruta_sm, encoding='utf-8').read()
sm = re.sub(r'  <url>\s*<loc>https://limpieza-prosol\.com\.ar/tips/.*?</url>\n', '', sm, flags=re.S)
nuevas = ''.join(f'  <url>\n    <loc>{DOMINIO}/tips/{s}</loc>\n    <lastmod>{FECHA}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>\n'
                 for s, p in [('', '0.7')] + [(t['slug'] + '/', '0.6') for t in tips])
sm = sm.replace('</urlset>', nuevas + '</urlset>')
open(ruta_sm, 'w', encoding='utf-8', newline='\n').write(sm)
print('ok sitemap.xml')
