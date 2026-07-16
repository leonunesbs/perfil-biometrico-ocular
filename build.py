#!/usr/bin/env python3
"""Aplica enhancements a um export do Claude Design -> index.html.

Uso:  python3 build.py "<export.html>"
Env:  GATE=1 ativa a tela de "em construção" (padrão: 0 = público).

Injeta SEO estático (lido por crawlers) + um script de runtime que sobrevive ao
swap de documento do bundle e: força document.title, injeta favicon, religa os CTAs
de download ao PDF, injeta CSS responsivo (header compacto no mobile + reduz padding
lateral das seções) e um footer (links do estudo + autor). HGF permanece como
instituição (vinculado à ESP-CE/SESA); o header NÃO é alterado.
"""
import sys, os, re, json

SRC = sys.argv[1] if len(sys.argv) > 1 else "export.html"
GATE = os.environ.get("GATE", "0") == "1"
URL = "https://leonunesbs.github.io/perfil-biometrico-ocular/"
IMG = URL + "og-image.png"
# Link do artigo: agora no Google Drive (o PDF saiu do repo de deploy). PLACEHOLDER abaixo —
# trocar pelo link real depois: o token __ARTIGO_PLACEHOLDER__ aparece aqui e no FOOTER.
PDF = "https://drive.google.com/__ARTIGO_PLACEHOLDER__"
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
    "publisher": {"@type": "Organization", "name": "Hospital Geral de Fortaleza",
                  "parentOrganization": {"@type": "Organization",
                                         "name": "Escola de Saúde Pública do Ceará (ESP-CE/SESA)"}},
    "about": ["biometria ocular", "comprimento axial", "ceratometria", "intervalos de referência",
              "IOLMaster 700", "catarata"],
    "url": URL, "image": IMG}, ensure_ascii=False)

head = f'''<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE}</title>
  <meta name="description" content="{DESC}">
  <meta name="keywords" content="biometria ocular, comprimento axial, ceratometria, intervalos de referência, IOLMaster 700, OCT swept-source, catarata, cálculo de LIO, lente intraocular, Hospital Geral de Fortaleza, ESP-CE, SESA, Fortaleza, oftalmologia, astigmatismo corneano">
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

# Footer: usa-se APENAS o footer do próprio design (Claude Design). A injeção do
# antigo #__ft foi removida — ela duplicava o footer do design e contribuía ~0,3 ao
# CLS (re-inserção pós-load). Os links legais (ética/privacidade/termos) agora ficam
# no footer do design. (Recuperável no git, caso o design perca o footer.)

# overflow-x:CLIP (não 'hidden'!) evita o transbordo horizontal SEM criar um scroll-container —
# preserva position:sticky (o eye-stage de scroll E o header sticky). 'overflow:hidden' criava um
# scroll-container e quebrava o sticky → era a causa da "animação de scroll inoperante" e do header
# "cortado". A responsividade de corpo/header já vem completa do próprio design (@media .lp-* em
# 520/820/1040: esconde navlinks/subtítulo, escala tipografia, empilha grids). Os antigos seletores
# data-dc-tpl deste build NÃO existem mais no export (eram regras nulas) — removidos.
CSS = "html,body{overflow-x:clip}"

gate_js = (
    "function gate(){if(document.getElementById('__cc'))return;var o=document.createElement('div');o.id='__cc';"
    "o.setAttribute('style','position:fixed;inset:0;z-index:2147483647;background:#0e1b2c;color:#fff;"
    "display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;"
    "font-family:-apple-system,BlinkMacSystemFont,\\'Segoe UI\\',Helvetica,Arial,sans-serif');"
    "o.innerHTML='<div style=\"max-width:540px\"><img src=\"apple-touch-icon.png\" width=\"104\" height=\"104\" style=\"border-radius:22px;margin-bottom:26px;box-shadow:0 8px 30px rgba(0,0,0,.45)\" alt=\"\"><div style=\"font-size:12px;letter-spacing:.2em;color:#4da3ff;"
    "font-weight:700;margin-bottom:20px\">HGF · OFTALMOLOGIA · TCR 2026</div><div style=\"font-size:32px;font-weight:700;"
    "line-height:1.15;margin-bottom:16px\">Perfil biométrico ocular</div><div style=\"font-size:17px;color:#cdd9e5;"
    "line-height:1.55\">Página em construção.<br>Estamos finalizando o conteúdo — volte em breve.</div></div>';"
    "(document.body||document.documentElement).appendChild(o);}") if GATE else "function gate(){}"

runtime = (
    "<script>(function(){var T=" + json.dumps(TITLE, ensure_ascii=False) + ",P=" + json.dumps(PDF)
    + ",CSS=" + json.dumps(CSS, ensure_ascii=False) + ";"
    "function ic(r,h){var l=document.querySelector('link[rel=\"'+r+'\"]');"
    "if(!l){l=document.createElement('link');l.rel=r;(document.head||document.documentElement).appendChild(l);}l.href=h;}"
    "function css(){var s=document.getElementById('__rs');if(!s){s=document.createElement('style');s.id='__rs';"
    "(document.head||document.documentElement).appendChild(s);}if(s.textContent!==CSS)s.textContent=CSS;}"
    "function ctas(){var as=document.querySelectorAll('a[href*=\"artigo-completo.pdf\"],a[download]');for(var i=0;i<as.length;i++){var a=as[i];"
    "a.setAttribute('href',P);a.setAttribute('target','_blank');a.setAttribute('rel','noopener');a.removeAttribute('download');}}"
    # ext(): toda <a> externa em nova aba leva rel=noopener noreferrer. Sem isso, o Safari/WebKit
    # BLOQUEIA a navegação p/ sites com COOP same-origin (Instagram/Facebook/Google) com o erro
    # 'Navigation was blocked by Cross-Origin-Opener-Policy'. Idempotente (só age se faltar noopener).
    "function ext(){var as=document.querySelectorAll('a[href^=\"http\"]');for(var i=0;i<as.length;i++){var a=as[i],h=a.getAttribute('href')||'';"
    "if(!/^https?:\\/\\//.test(h)||h.indexOf('//'+location.host)>-1)continue;"
    "var r=(a.getAttribute('rel')||'').split(/\\s+/).filter(Boolean),need=0;"
    "if(r.indexOf('noopener')<0){r.push('noopener');need=1;}if(r.indexOf('noreferrer')<0){r.push('noreferrer');need=1;}"
    "if(need)a.setAttribute('rel',r.join(' '));}}"
    # tcol(): a BARRA DE STATUS (theme-color) deve casar com o tema APLICADO. O Design usa
    # theme-color por media-query (segue só o SISTEMA) → em tema escuro por toggle manual com
    # sistema claro, a barra fica branca. Aqui removemos os por-media e setamos UM theme-color
    # = cor real pintada no topo da página (reflete toggle OU sistema). Reage a clique e ao sistema.
    "function tcol(){try{var md=document.querySelectorAll('meta[name=\"theme-color\"][media]');"
    "for(var i=0;i<md.length;i++)md[i].parentNode.removeChild(md[i]);"
    "var nm=document.querySelector('meta[name=\"theme-color\"]:not([media])');"
    "if(nm&&/rgba?\\([^)]*0?\\.\\d+\\s*\\)$/.test(nm.getAttribute('content')||'')){"
    "var c=nm.getAttribute('content').match(/(\\d+)\\D+(\\d+)\\D+(\\d+)/);if(c)nm.setAttribute('content','rgb('+c[1]+','+c[2]+','+c[3]+')');}}catch(e){}}"
    + gate_js +
    "function s(){if(document.title!==T)document.title=T;if(document.documentElement.lang!=='pt-BR')document.documentElement.lang='pt-BR';"
    "ic('icon','favicon.ico');ic('apple-touch-icon','apple-touch-icon.png');css();ctas();ext();tcol();gate();}"
    "s();var n=0,iv=setInterval(function(){s();if(++n>80)clearInterval(iv);},200);"
    "document.addEventListener('DOMContentLoaded',s);window.addEventListener('load',s);"
    "try{new MutationObserver(s).observe(document,{childList:true});}catch(e){}"
    "document.addEventListener('click',function(){setTimeout(tcol,60);setTimeout(tcol,320);});"
    "try{matchMedia('(prefers-color-scheme:dark)').addEventListener('change',tcol);}catch(e){}})();</script>"
)

# ── Correção de DADOS (só o que a fonte deixa defasado) ──────────────────────
# A fonte (Claude Design) é dona dos campos EXIBIDOS (n, mean, sd, refLo, refHi) e do
# array ASTIG — já corretos; NÃO re-injetamos (evita dupla injeção). Mas os campos
# INTERNOS do gráfico de distribuição (median/iqr/p5/p95/min/max) ficam defasados na
# fonte — aqui são forçados aos valores CERTIFICADOS do CSV (coorte senil). Também
# atualiza o período amostral. Fonte canônica: site/gerar_conteudo_lp.py (repo de dados).
CHARTFIX = {  # só campos internos do gráfico (não os exibidos)
 "AL":  {"median":"23.14","iqr0":"22.6","iqr1":"23.85","p5":"21.52","p95":"25.52","min":"19.91","max":"33.27"},
 "Km":  {"median":"44.0","iqr0":"42.9","iqr1":"45.04","p5":"41.41","p95":"46.69","min":"39.87","max":"48.13"},
 "ACD": {"median":"3.09","iqr0":"2.8","iqr1":"3.41","p5":"2.39","p95":"3.82","min":"1.31","max":"5.61"},
 "LT":  {"median":"4.46","iqr0":"4.18","iqr1":"4.72","p5":"3.79","p95":"5.15","min":"2.79","max":"5.71"},
 "WTW": {"median":"12.0","iqr0":"11.62","iqr1":"12.3","p5":"11.2","p95":"12.6","min":"10.6","max":"13.2"},
 "CCT": {"median":"523","iqr0":"499","iqr1":"549","p5":"468","p95":"597","min":"396","max":"672"},
}
PERIODO = ("janeiro–março de 2021", "janeiro a agosto de 2021")  # período amostral atualizado

def fixdata(html):
    for k, fields in CHARTFIX.items():
        m = re.search(r"\{key:'" + k + r"'[^{}]*\}", html)
        if not m:
            print(f"  fixdata {k}: OBJETO NÃO ACHADO"); continue
        obj = m.group(0); orig = obj
        for f, v in fields.items():
            obj = re.sub(r"(\b" + f + r":)[-\d.]+", r"\g<1>" + v, obj, count=1)
        html = html[:m.start()] + obj + html[m.end():]
        print(f"  fixdata {k}: {'corrigido' if obj != orig else 'já ok'}")
    html, c = re.subn(re.escape(PERIODO[0]), PERIODO[1], html)
    print(f"  fixdata período: {c}× {PERIODO[0]!r} → {PERIODO[1]!r}")
    return html

# ── Correção do HEAD estático (OG/favicon que o Design exporta quebrados) ─────
# O Design exporta no head: og:image/twitter:image com caminho RELATIVO inexistente
# (assets/og-card.png → 404) e favicon com href = UUID do bundler (404 no site). Crawlers
# leem o HTML ESTÁTICO (não rodam JS), então isso quebra preview de link e favicon inicial.
# Aqui: imagem OG absoluta (og-image.png, que existe) + og:url/canonical + favicons reais.
FAVI = ('<link rel="icon" type="image/x-icon" href="favicon.ico">'
        '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">'
        '<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">'
        '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">'
        '<link rel="icon" type="image/png" sizes="512x512" href="icon-512.png">'
        '<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">'
        '<link rel="manifest" href="manifest.webmanifest">')

def fixhead(html):
    # o Design recente deixa o <head> ESTÁTICO sem as metas de SEO (só ficam no template
    # escapado do bundle, injetado via JS) → crawlers não veem og/favicon. Reinjetamos um
    # bloco SEO completo e correto no head estático. Título: o do próprio Design (mantido).
    html = html.replace("assets/og-card.png", f"{URL}og-image.png")  # corrige refs (runtime) → arquivo real
    mt = re.search(r"<title>([^<]*)</title>", html)
    title = (mt.group(1).strip() if mt else TITLE).replace('"', "'")
    img = URL + "og-image.png"
    seo = (
        f'<meta name="description" content="{DESC}">'
        '<meta name="author" content="Leonardo Nunes Bezerra Souza">'
        '<meta name="robots" content="index, follow">'
        f'<link rel="canonical" href="{URL}">'
        '<meta property="og:type" content="article">'
        '<meta property="og:site_name" content="Perfil Biométrico Ocular · HGF">'
        f'<meta property="og:title" content="{title}">'
        f'<meta property="og:description" content="{DESC}">'
        f'<meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="{img}">'
        '<meta property="og:image:type" content="image/png">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Perfil biométrico ocular — intervalos de referência (HGF)">'
        '<meta property="og:locale" content="pt_BR">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{title}">'
        f'<meta name="twitter:description" content="{DESC}">'
        f'<meta name="twitter:image" content="{img}">'
        + FAVI
        + f'<script type="application/ld+json">{ld}</script>'
    )
    html = html.replace("</head>", seo + "</head>", 1)
    print("  fixhead: bloco SEO completo reinjetado no head estático (og/twitter/canonical/favicon/ld+json)")
    return html

# ── Correção de ALINHAMENTO (grid dos limiares biométricos) ──────────────────
# No grid "1fr auto" dos limiares (seção câmara rasa), o rótulo (19px) e o valor
# (22px) têm alturas diferentes; com align-items:center cada célula centraliza e
# seu border-bottom fica em Y distinto → a linha divisória mostra um degrau. stretch
# iguala as alturas das células e alinha as bordas. Padrão único no documento.
def fixalign(html):
    html, c = re.subn(re.escape("grid-template-columns:1fr auto;align-items:center"),
                      "grid-template-columns:1fr auto;align-items:stretch", html)
    print(f"  fixalign: {c}x grid de limiares -> align-items:stretch")
    return html

h = open(SRC, encoding="utf-8").read()
def fixicons(html):
    # Remove links de favicon do design cujo href é um UUID do bundler (404 no site).
    # O href correto já é reinjetado por fixhead/FAVI. Cobre aspas normais e escapadas.
    pat = r'<link\b[^>]*?href=(\\?")[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\1[^>]*?>'
    html, c = re.subn(pat, '', html)
    print(f"  fixicons: {c} favicon(s) UUID quebrado(s) removido(s)")
    return html

h = fixdata(h)
h = fixalign(h)
h = fixhead(h)
h = fixicons(h)
h = re.sub(r'<meta charset="utf-8">\s*<title>Bundled Page</title>', head, h, count=1)
h = re.sub(r'<html\b[^>]*>', '<html lang="pt-BR">', h, count=1)
h = h.replace("</body>", runtime + "</body>", 1) if "</body>" in h else h + runtime
open("index.html", "w", encoding="utf-8").write(h)
print(f"index.html gerado de {SRC!r} | GATE={'ON' if GATE else 'OFF'} | "
      f"SEO+favicon+enforcer+CTA+CSS+lang+hardening-de-links externos (footer = só o do design)")
