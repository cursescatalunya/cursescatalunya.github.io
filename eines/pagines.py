#!/usr/bin/env python3
"""Genera una pàgina estàtica per cursa (cursa/<id>/index.html), sitemap.xml i robots.txt
a partir de dades.js, perquè Google pugui indexar cada cursa. Executar des de l'arrel del repositori:
    python3 eines/pagines.py
"""
import json, re, os, html, shutil, datetime
BASE = 'https://cursescatalunya.github.io'
src = open('dades.js', encoding='utf-8').read()
races = json.loads(src[src.index('['):src.rindex(']') + 1])
upd = re.search(r"UPDATED='([\d-]+)'", src).group(1)
MES = ['gener','febrer','març','abril','maig','juny','juliol','agost','setembre','octubre','novembre','desembre']
DIA = ['dilluns','dimarts','dimecres','dijous','divendres','dissabte','diumenge']
SP = {'trail':'Trail','asfalt':'Asfalt','btt':'BTT','carretera':'Bici carretera','backyard':'Backyard','canicross':'Canicròs'}
ESTAT = {'oberta':'Inscripcions obertes','aviat':'Inscripcions aviat','tancada':'Inscripcions tancades','exhaurida':'Dorsals exhaurits'}
def e(s): return html.escape(str(s), quote=True)
def llarga(iso):
    d = datetime.date.fromisoformat(iso); m = MES[d.month-1]
    return f"{DIA[d.weekday()]} {d.day} {'d’' if m[0] in 'aeiouà' else 'de '}{m} de {d.year}"
def km(m):
    if m.get('km') is None: return m.get('nom') or 'Diverses distàncies'
    s = (f"{m['km']:g}").replace('.', ',') + ' km'
    return s + (f" · +{m['dplus']} m" if m.get('dplus') else '')
if os.path.isdir('cursa'): shutil.rmtree('cursa')
urls = [(BASE + '/', upd)]
for r in races:
    any_ = r['data'][:4]
    title = f"{r['nom']} {any_} · {r['poble']} | Curses de Catalunya"
    desc = f"{SP[r['esport']]} a {r['poble']} ({r.get('comarca','')}) el {llarga(r['data'])}. Distàncies: {', '.join(m['nom'] for m in r['mods'])}. Recorregut, mapa i enllaç a les inscripcions."
    mods = ''.join(f"<li><b>{e(m['nom'])}</b> — {e(km(m))}{' · sortida '+e(m['hora'])+' h' if m.get('hora') else ''}</li>" for m in r['mods'])
    ins = ESTAT.get((r.get('insc') or {}).get('estat'), '')
    ld = {"@context": "https://schema.org", "@type": "SportsEvent", "name": f"{r['nom']} {any_}", "startDate": r['data'],
          "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "sport": SP[r['esport']], "description": r.get('desc', ''), "url": f"{BASE}/cursa/{r['id']}/",
          "location": {"@type": "Place", "name": r['poble'], "address": {"@type": "PostalAddress", "addressLocality": r['poble'], "addressRegion": "Catalunya", "addressCountry": "ES"},
                       "geo": {"@type": "GeoCoordinates", "latitude": r['lat'], "longitude": r['lng']}}}
    if r.get('web'): ld["sameAs"] = r['web']
    page = f"""<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}/cursa/{r['id']}/">
<meta property="og:title" content="{e(r['nom'])} {any_}"><meta property="og:description" content="{e(desc)}"><meta name="theme-color" content="#D4471E"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/icon-180.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>body{{margin:0;font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;background:#F1F3EE;color:#17201B}}main{{max-width:720px;margin:0 auto;padding:24px max(16px,env(safe-area-inset-left))}}a{{color:#B8391A}}h1{{font-size:2.2rem;line-height:1.1;margin:.2em 0}}.k{{color:#5B675F}}.b{{display:inline-block;background:#D4471E;color:#fff;text-decoration:none;font-weight:600;padding:12px 18px;border-radius:8px;margin:6px 8px 6px 0}}.g{{background:#fff;color:#17201B;border:1.5px solid #17201B}}
@media (prefers-color-scheme:dark){{body{{background:#111612;color:#E6EBE4}}.k{{color:#95A198}}a{{color:#F0673A}}.g{{background:#19201B;color:#E6EBE4;border-color:#E6EBE4}}}}</style></head>
<body><main><p class="k"><a href="{BASE}/">← Curses de Catalunya</a></p>
<p class="k">{e(SP[r['esport']])}{' · data provisional' if r.get('provisional') else ''}</p><h1>{e(r['nom'])}</h1>
<p><b>{e(llarga(r['data']).capitalize())}</b> · {e(r['poble'])} ({e(r.get('comarca',''))})</p>
{f'<p><b>{e(ins)}</b></p>' if ins else ''}<ul>{mods}</ul><p>{e(r.get('desc',''))}</p>
<p><a class="b" href="{BASE}/#cursa-{r['id']}">Mapa, recorregut i perfil</a><a class="b g" href="{e(r.get('web',''))}" rel="noopener">Web oficial i inscripcions</a></p>
<p class="k">Font: {e(r['font']['nom'])}. Comprova sempre data, horari i recorregut a la web de l'organització.</p></main></body></html>"""
    os.makedirs(f"cursa/{r['id']}", exist_ok=True)
    open(f"cursa/{r['id']}/index.html", 'w', encoding='utf-8').write(page)
    urls.append((f"{BASE}/cursa/{r['id']}/", upd))
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + '</urlset>\n')
open('robots.txt', 'w').write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print(len(races), 'pàgines generades')
