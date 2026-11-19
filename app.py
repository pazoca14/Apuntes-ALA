"""
Apuntes de Álgebra Lineal Avanzada (Flask)

Estructura del proyecto
  app.py                 ensambla la página y la sirve en "/"
  contenido/capN.html    texto de cada capítulo (HTML + LaTeX para MathJax)
  figuras_codigos.py     figuras y tablas de los capítulos 0-8 (calculadas en Python)
  figuras_avanzado.py    figuras y tablas de los capítulos 9-12 (calculadas en Python)
  interactivos.py        bloques interactivos (HTML); su lógica está en static/js/site.js
  static/css/site.css    diseño (tema claro y oscuro)
  static/js/site.js      laboratorios interactivos, buscador, tema, progreso

Ya no se usan imágenes de static/dataset: todas las figuras, diagramas y tablas
se generan con código (SVG en línea), así que siempre coinciden con las cuentas.

En los textos de contenido/ hay marcadores que se sustituyen al ensamblar:
  @@FIG:nombre@@   figura SVG          @@TAB:nombre@@   tabla HTML
  @@RAW:nombre@@   bloque auxiliar     @@INTERACTIVO@@  laboratorio del capítulo
"""
import os
import re
from functools import lru_cache

from flask import Flask, Response

import figuras_avanzado
import figuras_codigos
from interactivos import lab

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))

# (número, título, subtítulo, parte)
CAPITULOS = [
    (0, "Preliminares y notación", "Bits, palabras, peso, distancia, matrices $G$ y $H$, cotas y síndrome.", "codes"),
    (1, "Códigos lineales", "Cerradura, matriz generadora y de control, los siete códigos $[3,2]$ y un $[5,2,3]$.", "codes"),
    (2, "Códigos duales", "Ortogonalidad, $\\dim C+\\dim C^{\\perp}=n$ y códigos autoduales.", "codes"),
    (3, "Códigos lineales en $V_4$", "Detectar no es corregir: seis casos vistos en el hipercubo.", "codes"),
    (4, "Códigos lineales en $V_6$", "Corregir un error con tasa $1/2$ y el corrector $[6,2,4]$.", "codes"),
    (5, "Códigos lineales en $V_7$", "Hamming perfecto, símplex y repetición: siete casos con mapas de distancias.", "codes"),
    (6, "El código de Hamming $[7,4,3]$", "Ecuaciones de paridad, clases laterales y decodificación por síndrome.", "codes"),
    (7, "El código de Hamming extendido $[8,4,4]$", "SECDED: corregir un error y detectar dos; probabilidades frente al $[7,4,3]$.", "codes"),
    (8, "El secreto de la recta (Reed–Solomon)", "Rectas, testigos y aritmética del reloj: el código de Reed–Solomon en pequeño.", "codes"),
    (9, "Descomposición en valores singulares (SVD)", "$A=U\\Sigma V^{T}$: girar, estirar y girar; pseudoinversa y compresión.", "lin"),
    (10, "Análisis de componentes principales (PCA)", "Direcciones de máxima varianza, codo, cargas y eigenfaces.", "lin"),
    (11, "Teorema fundamental del álgebra lineal", "Los cuatro subespacios, su ortogonalidad y la alternativa de Fredholm.", "lin"),
    (12, "Campos finitos", "Construcción de $\\mathbb{F}_{2^n}$, bits, logaritmos, aritmética rápida y aplicaciones.", "gf"),
]
PARTES = {"codes": ("Parte I · Teoría de códigos", "part-codes"),
          "lin": ("Parte II · Álgebra lineal numérica", "part-lin"),
          "gf": ("Parte III · Estructuras algebraicas", "part-gf")}

SOL_TOOLS = ('<div class="sol-tools"><button class="btn-ghost" data-open>Mostrar todas</button>'
             '<button class="btn-ghost" data-close>Ocultar todas</button></div>')


def _figura(nombre):
    if nombre in figuras_avanzado.FIGURAS:
        return figuras_avanzado.figura(nombre)
    return figuras_codigos.figura(nombre)


def _tabla(nombre):
    if nombre in figuras_avanzado.TABLAS:
        return figuras_avanzado.tabla(nombre)
    return figuras_codigos.tabla(nombre)


def capitulo_html(n):
    with open(os.path.join(BASE, "contenido", "cap%d.html" % n), encoding="utf-8") as f:
        html = f.read()
    html = re.sub(r"@@FIG:(\w+)@@", lambda m: _figura(m.group(1)), html)
    html = re.sub(r"@@TAB:(\w+)@@", lambda m: _tabla(m.group(1)), html)
    html = re.sub(r"@@RAW:(\w+)@@", lambda m: figuras_codigos.RAW[m.group(1)](), html)
    if "@@INTERACTIVO@@" in html:
        html = html.replace("@@INTERACTIVO@@", lab(n))
    else:
        html += lab(n)
    html = re.sub(r"(<h3>Soluciones[^<]*</h3>)", r"\1" + SOL_TOOLS, html)
    return html


HEAD = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Apuntes de Álgebra Lineal Avanzada</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/css/site.css">
<script>
try { var t = localStorage.getItem("ala-theme"); if (t) document.documentElement.setAttribute("data-theme", t); } catch (e) {}
window.MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], processEscapes: true },
  options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] },
  chtml: { scale: 1.0 }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<div id="progress"></div>
<button id="menuBtn" aria-label="Abrir índice">☰</button>
"""


def barra_lateral():
    out = ['<nav id="sidebar"><div class="brand"><a class="logo" href="#inicio"><i>Σ</i>Álgebra Lineal Avanzada</a>'
           '<small>Apuntes · Universidad Anáhuac</small></div>'
           '<div class="nav-tools"><input id="navSearch" type="search" placeholder="Buscar capítulo…">'
           '<button class="icon-btn" id="themeBtn" title="Cambiar tema claro/oscuro">🌓</button></div><div class="nav-scroll">']
    parte = None
    for n, titulo, _, p in CAPITULOS:
        if p != parte:
            if parte is not None:
                out.append("</ul>")
            out.append('<div class="nav-group">%s</div><ul>' % PARTES[p][0])
            parte = p
        out.append('<li><a href="#cap%d"><span class="n">%d</span><span>%s</span></a></li>' % (n, n, titulo))
    out.append("</ul></div></nav>")
    return "\n".join(out)


def portada():
    tarjetas = "".join(
        '<a href="#cap%d"><div class="k">CAPÍTULO %d</div><div class="t">%s</div><div class="d">%s</div></a>'
        % (n, n, t, s) for n, t, s, _ in CAPITULOS)
    deco = ('<svg class="deco" viewBox="0 0 200 200"><g fill="none" stroke="#fff" stroke-width="2">'
            '<rect x="30" y="30" width="80" height="80"/><rect x="70" y="70" width="80" height="80"/>'
            '<line x1="30" y1="30" x2="70" y2="70"/><line x1="110" y1="30" x2="150" y2="70"/>'
            '<line x1="30" y1="110" x2="70" y2="150"/><line x1="110" y1="110" x2="150" y2="150"/>'
            '<ellipse cx="100" cy="100" rx="90" ry="40" transform="rotate(-25 100 100)"/></g></svg>')
    return ("""<header class="hero" id="inicio">%s
<h1>Apuntes de Álgebra Lineal Avanzada</h1>
<p>Códigos lineales, duales y de Hamming; el secreto de la recta; SVD, PCA y el teorema fundamental; y campos finitos.
Cada capítulo trae una explicación en palabras simples, figuras generadas con código, un laboratorio interactivo y ejercicios resueltos.</p>
<div class="chips"><span>12 capítulos + preliminares</span><span>13 laboratorios interactivos</span><span>Figuras calculadas, no dibujadas a mano</span><span>Tema claro y oscuro</span></div>
<div class="credits"><strong>Créditos y autores:</strong> Melanie Victoria Robles Osorio · Mariana Itzel Gómez Contreras · José María Hurtado y Sánchez</div>
</header>
<div class="overview">%s</div>""" % (deco, tarjetas))


def seccion(n, titulo, sub, p):
    etiqueta, clase = PARTES[p]
    return ('<section class="chapter %s" id="cap%d"><div class="ch-head"><div class="ch-num">%d</div><div>'
            '<div class="part">%s · Capítulo %d</div><h2>%s</h2><p class="sub">%s</p></div></div>%s</section>'
            % (clase, n, n, etiqueta, n, titulo, sub, capitulo_html(n)))


FOOT = """<footer>Apuntes de Álgebra Lineal Avanzada · Todas las figuras, tablas y resultados se calculan con el código del sitio.</footer>
</main>
<button id="toTop" aria-label="Volver arriba">↑</button>
<script src="/static/js/site.js"></script>
</body>
</html>
"""


@lru_cache(maxsize=1)
def construir_pagina():
    partes = [HEAD, barra_lateral(), "<main>", portada()]
    partes += [seccion(*c) for c in CAPITULOS]
    partes.append(FOOT)
    return "\n".join(partes)


@app.route("/")
def home():
    html = construir_pagina() if not app.debug else construir_pagina.__wrapped__()
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True)
