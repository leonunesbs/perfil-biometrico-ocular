#!/usr/bin/env python3
"""Aplica enhancements a um export do Claude Design -> index.html.

Uso:   python3 build.py "<export.html>"
Env:   GATE=0  desativa a tela de "em construção" (padrão: GATE=1, ativa).

Injeta: SEO completo (<head> estático, lido por crawlers), e um script de runtime
que sobrevive ao swap de documento do bundle e (1) força document.title, (2) injeta
favicon, (3) religa os CTAs de download ao PDF hospedado e (4) exibe a tela de
construção quando GATE=1.
"""
import sys, os, re, json

SRC = sys.argv[1] if len(sys.argv) > 1 else "export.html"
GATE = os.environ.get("GATE", "1") == "1"
URL = "https://leonunesbs.github.io/perfil-biometrico-ocular/"
IMG = URL + "og-image.png"
PDF = "artigo-completo.pdf"
TITLE = "Perfil biométrico ocular e intervalos de referência — HGF"
DESC = ("Estudo transversal do perfil biométrico ocular — comprimento axial, ceratometria, "
        "câmara anterior, cristalino e córnea — e intervalos de referência em adultos ≥ 40 anos, "
        "avaliados por OCT swept-source (IOLMaster 700) em hospital terciário do Nordeste do Brasil.")

ld = json.dumps({
    "@context": "https://schema.org", "@type": "ScholarlyArticle",
    "headline": "Perfil biométrico ocular e intervalos de referência em adultos avaliados por OCT swept-source",
    "inLanguage": "pt-BR", "datePublished": "2026",
    "author": {"@type": "Person", "name": "Leonardo Nunes Bezerra Souza"},
    "contributor": {"@type": "Person", "name": "Dácio Carvalho Costa", "jobTitle": "Orientador"},
    "publisher": {"@type": "Organization", "name": "Hospital Geral de Fortaleza"},
    "about": ["biometria ocular", "comprimento axial", "ceratometria", "intervalos de referência",
              "IOLMaster 700", "catarata"],
    "url": URL, "image": IMG}, ensure_ascii=False)

head = f'''<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE}</title>
  <meta name="description" content="{DESC}">
  <meta name="keywords" content="biometria ocular, comprimento axial, ceratometria, intervalos de referência, IOLMaster 700, OCT swept-source, catarata, cálculo de LIO, lente intraocular, Hospital Geral de Fortaleza, Fortaleza, oftalmologia, astigmatismo corneano">
  <meta name="author" content="Leonardo Nunes Bezerra Souza">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0e1b2c">
  <link rel="canonical" href="{URL}">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Perfil Biométrico Ocular · HGF">
  <meta property="og:title" content="Perfil biométrico ocular e intervalos de referência em adultos">
  <meta property="og:description" content="{DESC}">
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="{IMG}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Perfil biométrico ocular — intervalos de referência (HGF, TCR 2026)">
  <meta property="og:locale" content="pt_BR">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Perfil biométrico ocular e intervalos de referência em adultos">
  <meta name="twitter:description" content="{DESC}">
  <meta name="twitter:image" content="{IMG}">
  <script type="application/ld+json">{ld}</script>'''

gate_js = (
    "function gate(){if(document.getElementById('__cc'))return;"
    "var o=document.createElement('div');o.id='__cc';"
    "o.setAttribute('style','position:fixed;inset:0;z-index:2147483647;background:#0e1b2c;color:#fff;"
    "display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;"
    "font-family:-apple-system,BlinkMacSystemFont,\\'Segoe UI\\',Helvetica,Arial,sans-serif');"
    "o.innerHTML='<div style=\"max-width:540px\">"
    "<div style=\"font-size:12px;letter-spacing:.2em;color:#4da3ff;font-weight:700;margin-bottom:20px\">HGF · OFTALMOLOGIA · TCR 2026</div>"
    "<div style=\"font-size:32px;font-weight:700;line-height:1.15;margin-bottom:16px\">Perfil biométrico ocular</div>"
    "<div style=\"font-size:17px;color:#cdd9e5;line-height:1.55\">Página em construção.<br>Estamos finalizando o conteúdo — volte em breve.</div>"
    "</div>';(document.body||document.documentElement).appendChild(o);}"
) if GATE else "function gate(){}"

runtime = (
    "<script>(function(){var T=" + json.dumps(TITLE, ensure_ascii=False) + ",P=" + json.dumps(PDF) + ";"
    "function ic(r,h){var l=document.querySelector('link[rel=\"'+r+'\"]');"
    "if(!l){l=document.createElement('link');l.rel=r;(document.head||document.documentElement).appendChild(l);}l.href=h;}"
    "function ctas(){var as=document.querySelectorAll('a[download]');for(var i=0;i<as.length;i++){var a=as[i];"
    "if((a.getAttribute('href')||'').slice(-4)!=='.pdf'){a.setAttribute('href',P);a.setAttribute('download','artigo-completo.pdf');}}}"
    + gate_js +
    "function s(){if(document.title!==T)document.title=T;ic('icon','favicon.ico');ic('apple-touch-icon','apple-touch-icon.png');ctas();gate();}"
    "s();var n=0,iv=setInterval(function(){s();if(++n>80)clearInterval(iv);},200);"
    "document.addEventListener('DOMContentLoaded',s);window.addEventListener('load',s);"
    "try{new MutationObserver(s).observe(document,{childList:true});}catch(e){}})();</script>"
)

h = open(SRC, encoding="utf-8").read()
h = re.sub(r'<meta charset="utf-8">\s*<title>Bundled Page</title>', head, h, count=1)
h = re.sub(r'<html\b[^>]*>', '<html lang="pt-BR">', h, count=1)
if "</body>" in h:
    h = h.replace("</body>", runtime + "</body>", 1)
else:
    h += runtime
open("index.html", "w", encoding="utf-8").write(h)
print(f"index.html gerado de {SRC!r} | GATE={'ON (em construção)' if GATE else 'OFF'} | "
      f"SEO+favicon+enforcer+CTA aplicados")
