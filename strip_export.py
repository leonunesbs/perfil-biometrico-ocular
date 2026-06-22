#!/usr/bin/env python3
"""Limpa o export bruto do Claude Design -> _export_clean.html (input do build.py).

O export embute uma tabela de recursos do bundler:
    {"<uuid>":{"mime":..,"compressed":..,"data":"H4sI.."}, ...}
referenciada por um array de bindings:
    [{"id":"patientsData","uuid":..},{"id":"articlePdf","uuid":..}]

Este script ESVAZIA o array de bindings -> [] e REMOVE da tabela os recursos
apontados por ele, de modo que window.__resources fique vazio e o runtime caia
nos fallbacks corretos:
  * artigo  -> link do Drive  (religado pelo build.py em ctas())
  * pacientes -> ./patients.json  (dados reais, gerado por site/gen_patients_json.py)

O PDF (application/pdf) é ~84% do peso do export; removê-lo é o ganho principal.

Uso:  python strip_export.py "<export bruto.html>" [saida=_export_clean.html]
"""
import sys, re, json

SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "_export_clean.html"

h = open(SRC, encoding="utf-8").read()
n0 = len(h)

# 1) localizar o array de bindings (objetos {"id":..,"uuid":..}) e coletar os uuids
m = re.search(r'\[\{"id":"[^"]+","uuid":"[0-9a-f-]+"\}'
              r'(?:,\{"id":"[^"]+","uuid":"[0-9a-f-]+"\})*\]', h)
uuids = []
if m:
    binds = json.loads(m.group(0))
    uuids = [b["uuid"] for b in binds]
    h = h[:m.start()] + "[]" + h[m.end():]
    print("bindings:", [b["id"] for b in binds], "-> []")
else:
    print("AVISO: array de bindings não encontrado (formato mudou?)")

# 2) remover cada recurso da tabela (objeto sem chaves aninhadas; base64 não tem { } ")
for u in uuids:
    body = r':\{[^{}]*\}'
    removed = False
    for pat in (r',"' + re.escape(u) + r'"' + body,      # vírgula à esquerda
                r'"' + re.escape(u) + r'"' + body + r',',  # vírgula à direita (1ª entrada)
                r'"' + re.escape(u) + r'"' + body):        # entrada única
        h, k = re.subn(pat, "", h, count=1)
        if k:
            removed = True
            print(f"  recurso {u[:8]}…: removido")
            break
    if not removed:
        print(f"  recurso {u[:8]}…: NÃO encontrado")

open(OUT, "w", encoding="utf-8").write(h)
print(f"{SRC.split('/')[-1]} ({n0/1e6:.2f} MB) -> {OUT} ({len(h)/1e6:.2f} MB)")
