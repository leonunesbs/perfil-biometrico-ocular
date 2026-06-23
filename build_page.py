#!/usr/bin/env python3
"""Processa um export de SUBPÁGINA do Claude Design (ética/privacidade/termos) → arquivo do repo.

As subpáginas já são enxutas (sem PDF/bindings), com <title> próprio e lang setado em
runtime. O único ajuste necessário é o link "Voltar à página principal", que o Design
exporta apontando para o nome do arquivo do export ("Perfil Biometrico Ocular - Landing.html")
em vez de index.html — o que quebraria no site publicado.

Uso: python build_page.py "<export.html>" <saida.html>
"""
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
h = open(SRC, encoding="utf-8").read()
n = h.count("Perfil Biometrico Ocular - Landing.html")
h = h.replace("Perfil Biometrico Ocular - Landing.html", "index.html")
open(OUT, "w", encoding="utf-8").write(h)
print(f"{SRC.split('/')[-1]} → {OUT}  | back-link corrigido: {n}× → index.html")
