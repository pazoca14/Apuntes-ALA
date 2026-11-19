# Apuntes de Álgebra Lineal Avanzada (Flask)

Sitio con 13 secciones: preliminares (cap. 0) y 12 capítulos.

| Parte | Capítulos |
|---|---|
| I · Teoría de códigos | 0 Preliminares · 1 Códigos lineales · 2 Códigos duales · 3 V4 · 4 V6 · 5 V7 · 6 Hamming [7,4,3] · 7 Hamming extendido [8,4,4] · 8 El secreto de la recta |
| II · Álgebra lineal numérica | 9 SVD (con 5 ejemplos resueltos) · 10 PCA (con 3 ejemplos resueltos) · 11 Teorema fundamental |
| III · Estructuras algebraicas | 12 Campos finitos |

## Cómo correrlo
```bash
pip install -r requirements.txt
python app.py          # abre http://127.0.0.1:5000
```

## Estructura
- `app.py` — ensambla la página (sin Jinja) y la sirve en `/`.
- `contenido/capN.html` — texto de cada capítulo (HTML + LaTeX para MathJax) con marcadores
  `@@FIG:…@@`, `@@TAB:…@@`, `@@RAW:…@@` e `@@INTERACTIVO@@`.
- `figuras_codigos.py` — hipercubos, mapas de distancias, distribuciones de pesos y tablas de los caps. 0-8,
  todo calculado (palabras, clases laterales, síndromes, probabilidades).
- `figuras_avanzado.py` — figuras y tablas de los caps. 9-12 (SVD, PCA, TFAL, campos finitos).
- `interactivos.py` + `static/js/site.js` — un laboratorio interactivo por capítulo.
- `static/css/site.css` — diseño con tema claro y oscuro.

Las imágenes ya no se leen de `static/dataset`: todas se generan con código (SVG en línea y,
para la compresión por SVD, un `<canvas>` que calcula la SVD en el navegador). La carpeta
`static/dataset` del proyecto anterior se puede borrar.

Requiere conexión a internet para MathJax (fórmulas) y las fuentes Inter / JetBrains Mono.
