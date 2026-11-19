"""
Figuras y tablas de los capítulos 9-12 (SVD, PCA, TFAL y campos finitos).

Todo se genera con Python puro (sin numpy) como SVG en línea. Los datos de
cada figura se calculan aquí: la SVD de la matriz de ejemplo, el PCA de la nube
de puntos, las proyecciones del TFAL y la aritmética de los campos finitos.
"""
import math
import random
from functools import lru_cache

# ---------------------------------------------------------------------------
# Utilidades de dibujo
# ---------------------------------------------------------------------------
def _svg(w, h, cuerpo, clase="svgfig", label="Figura"):
    return ('<svg class="%s" viewBox="0 0 %d %d" role="img" aria-label="%s">'
            '<defs>'
            '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
            '<marker id="ahA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahA"/></marker>'
            '<marker id="ahB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahB"/></marker>'
            '<marker id="ahR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahR"/></marker>'
            '</defs>%s</svg>' % (clase, w, h, label, cuerpo))


def _t(x, y, txt, cls="lbl", anchor="middle", extra=""):
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (cls, x, y, anchor, extra, txt)


def _flecha(x1, y1, x2, y2, cls="vecA", marker="ahA"):
    return ('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" marker-end="url(#%s)"/>'
            % (cls, x1, y1, x2, y2, marker))


# ---------------------------------------------------------------------------
# Álgebra 2x2
# ---------------------------------------------------------------------------
def svd2(A):
    """SVD de una matriz 2x2: devuelve (U, (s1, s2), V) con columnas u_i, v_i."""
    a, b = A[0]
    c, d = A[1]
    # A^T A
    p, q, r = a * a + c * c, a * b + c * d, b * b + d * d
    tr, det = p + r, p * r - q * q
    disc = math.sqrt(max(tr * tr / 4 - det, 0))
    l1, l2 = tr / 2 + disc, max(tr / 2 - disc, 0)
    if abs(q) > 1e-12:
        v1 = (q, l1 - p)
    else:
        v1 = (1, 0) if p >= r else (0, 1)
    nv = math.hypot(*v1)
    v1 = (v1[0] / nv, v1[1] / nv)
    if v1[0] < 0:
        v1 = (-v1[0], -v1[1])
    v2 = (-v1[1], v1[0])
    s1, s2 = math.sqrt(l1), math.sqrt(l2)
    Av1 = (a * v1[0] + b * v1[1], c * v1[0] + d * v1[1])
    u1 = (Av1[0] / s1, Av1[1] / s1)
    Av2 = (a * v2[0] + b * v2[1], c * v2[0] + d * v2[1])
    u2 = (Av2[0] / s2, Av2[1] / s2) if s2 > 1e-12 else (-u1[1], u1[0])
    return (u1, u2), (s1, s2), (v1, v2)


A_SVD = [[1.4, 0.3], [1.2, 1.5]]


def svd_circulo():
    (u1, u2), (s1, s2), (v1, v2) = svd2(A_SVD)
    paneles = []
    R = 30.0  # radio en px de la unidad

    def ang(v):
        return math.atan2(v[1], v[0])

    estados = [
        ("Inicio", "círculo unitario", (1, 1), 0.0, v1, v2, "v₁", "v₂"),
        ("1. Rotación Vᵀ", "alinea v₁, v₂ con los ejes", (1, 1), 0.0, (1, 0), (0, 1), "e₁", "e₂"),
        ("2. Escalamiento Σ", "estira: elipse σ₁e₁, σ₂e₂", (s1, s2), 0.0, (s1, 0), (0, s2), "σ₁e₁", "σ₂e₂"),
        ("3. Rotación U", "orienta: semiejes σ₁u₁, σ₂u₂", (s1, s2), ang(u1), (s1 * u1[0], s1 * u1[1]), (s2 * u2[0], s2 * u2[1]), "σ₁u₁", "σ₂u₂"),
    ]
    W, Hh = 200, 236
    cuerpo = []
    for i, (tit, sub, (ax, by), rot, a, b, la, lb) in enumerate(estados):
        cx, cy = 20 + i * (W + 30) + W / 2, 130
        g = ['<g>']
        g.append('<rect class="panel" x="%.1f" y="20" width="%d" height="%d" rx="10"/>' % (cx - W / 2, W, Hh - 30))
        g.append('<line class="axis-l" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cx - 80, cy, cx + 80, cy))
        g.append('<line class="axis-l" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cx, cy - 72, cx, cy + 72))
        g.append('<ellipse class="shape" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.2f %.1f %.1f)"/>'
                 % (cx, cy, ax * R, by * R, -math.degrees(rot), cx, cy))
        for vv, lab, cls, mk in [(a, la, "vecA", "ahA"), (b, lb, "vecB", "ahB")]:
            x2, y2 = cx + vv[0] * R, cy - vv[1] * R
            g.append(_flecha(cx, cy, x2, y2, cls, mk))
            nx, ny = vv[0], vv[1]
            nn = math.hypot(nx, ny) or 1
            lx, ly = x2 + 15 * nx / nn, y2 - 15 * ny / nn + 4
            if abs(ny / nn) < 0.2:      # vector horizontal: etiqueta debajo de la punta
                lx, ly = x2 - 6, y2 + 18
            g.append(_t(lx, ly, lab, "lbl-it"))
        g.append(_t(cx, 42, tit, "lbl-b"))
        g.append(_t(cx, Hh - 18, sub, "lbl-s"))
        g.append("</g>")
        cuerpo.append("".join(g))
        if i < 3:
            xa = cx + W / 2 + 4
            cuerpo.append(_flecha(xa, cy, xa + 22, cy, "arrow-step", "ah"))
    cap = "A = [[%.1f, %.1f], [%.1f, %.1f]],  σ₁ = %.3f,  σ₂ = %.3f" % (A_SVD[0][0], A_SVD[0][1], A_SVD[1][0], A_SVD[1][1], s1, s2)
    cuerpo.append(_t(4 * (W + 30) / 2 + 5, Hh + 14, cap, "lbl-s"))
    return _svg(4 * (W + 30) + 10, Hh + 24, "".join(cuerpo), label="Transformación del círculo unitario por la SVD")


def svd_bloques():
    """A(m×n) = U Σ Vᵀ con bloques activos (rango r) y nulos."""
    u = 18  # px por unidad
    m, n, r = 6, 4, 2
    cuerpo = []

    def caja(x, y, w, h, cls, txt=None):
        s = '<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>' % (cls, x, y, w, h)
        if txt:
            s += _t(x + w / 2, y + h / 2 + 5, txt, "lbl-b")
        return s

    y0 = 40
    x = 20
    # A
    cuerpo.append(caja(x, y0, n * u, m * u, "blk-a", "A"))
    cuerpo.append(_t(x + n * u / 2, y0 + m * u + 18, "m × n", "lbl-s"))
    x += n * u + 30
    cuerpo.append(_t(x - 15, y0 + m * u / 2 + 6, "=", "lbl-big"))
    # U = [U_r | U_{m-r}]
    cuerpo.append(caja(x, y0, r * u, m * u, "blk-on", "Uᵣ"))
    cuerpo.append(caja(x + r * u, y0, (m - r) * u, m * u, "blk-off", "U₀"))
    cuerpo.append(_t(x + m * u / 2, y0 + m * u + 18, "U: m × m", "lbl-s"))
    x += m * u + 18
    # Sigma
    cuerpo.append(caja(x, y0, n * u, m * u, "blk-zero"))
    cuerpo.append(caja(x, y0, r * u, r * u, "blk-on", "Σᵣ"))
    cuerpo.append(_t(x + n * u * 0.62, y0 + m * u * 0.68, "0", "lbl-s"))
    cuerpo.append(_t(x + n * u / 2, y0 + m * u + 18, "Σ: m × n", "lbl-s"))
    x += n * u + 18
    # V^T
    cuerpo.append(caja(x, y0, n * u, r * u, "blk-on", "Vᵣᵀ"))
    cuerpo.append(caja(x, y0 + r * u, n * u, (n - r) * u, "blk-off", "V₀ᵀ"))
    cuerpo.append(_t(x + n * u / 2, y0 + m * u + 18, "Vᵀ: n × n", "lbl-s"))
    xend = x + n * u
    cuerpo.append(_t((20 + xend) / 2, 24, "Factorización completa", "lbl-b"))
    # truncada
    x = xend + 60
    cuerpo.append(_t(x + 120, 24, "Versión reducida (rango r)", "lbl-b"))
    cuerpo.append(caja(x, y0, n * u, m * u, "blk-a", "A"))
    x += n * u + 30
    cuerpo.append(_t(x - 15, y0 + m * u / 2 + 6, "=", "lbl-big"))
    cuerpo.append(caja(x, y0, r * u, m * u, "blk-on", "Uᵣ"))
    cuerpo.append(_t(x + r * u / 2, y0 + m * u + 18, "m × r", "lbl-s"))
    x += r * u + 14
    cuerpo.append(caja(x, y0, r * u, r * u, "blk-on", "Σᵣ"))
    cuerpo.append(_t(x + r * u / 2, y0 + r * u + 18, "r × r", "lbl-s"))
    x += r * u + 14
    cuerpo.append(caja(x, y0, n * u, r * u, "blk-on", "Vᵣᵀ"))
    cuerpo.append(_t(x + n * u / 2, y0 + r * u + 18, "r × n", "lbl-s"))
    xend2 = x + n * u
    # leyenda
    ly = y0 + m * u + 44
    cuerpo.append(caja(20, ly - 11, 16, 14, "blk-on") + _t(42, ly, "bloques activos (guardan la información)", "lbl-s", "start"))
    cuerpo.append(caja(330, ly - 11, 16, 14, "blk-off") + _t(352, ly, "bloques que multiplican ceros", "lbl-s", "start"))
    cuerpo.append(caja(580, ly - 11, 16, 14, "blk-zero") + _t(602, ly, "ceros de Σ", "lbl-s", "start"))
    return _svg(max(xend2 + 20, 720), ly + 16, "".join(cuerpo), label="Dimensiones de U, Σ y V")


# ---------------------------------------------------------------------------
# PCA
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def datos_pca():
    rnd = random.Random(7)
    pts = []
    ang = math.radians(32)
    for _ in range(70):
        a, b = rnd.gauss(0, 2.1), rnd.gauss(0, 0.65)
        pts.append((4.5 + a * math.cos(ang) - b * math.sin(ang), 3.2 + a * math.sin(ang) + b * math.cos(ang)))
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts) / (n - 1)
    syy = sum((p[1] - my) ** 2 for p in pts) / (n - 1)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts) / (n - 1)
    tr, det = sxx + syy, sxx * syy - sxy * sxy
    disc = math.sqrt(tr * tr / 4 - det)
    l1, l2 = tr / 2 + disc, tr / 2 - disc
    v1 = (sxy, l1 - sxx)
    nv = math.hypot(*v1)
    v1 = (v1[0] / nv, v1[1] / nv)
    if v1[0] < 0:
        v1 = (-v1[0], -v1[1])
    v2 = (-v1[1], v1[0])
    return pts, (mx, my), (l1, l2), (v1, v2), ((sxx, sxy), (sxy, syy))


def _ejes_pca(px, py, x0, y0, w, h, xmin, xmax, ymin, ymax):
    def X(x):
        return x0 + (x - xmin) / (xmax - xmin) * w

    def Y(y):
        return y0 + h - (y - ymin) / (ymax - ymin) * h
    return X, Y


def pca_nube():
    pts, (mx, my), (l1, l2), (v1, v2), S = datos_pca()
    X, Y = _ejes_pca(0, 0, 50, 20, 420, 300, 0, 9, 0, 6.4)
    c = ['<rect class="panel" x="40" y="10" width="440" height="320" rx="10"/>']
    for gx in range(1, 9):
        c.append('<line class="grid" x1="%.1f" y1="20" x2="%.1f" y2="320"/>' % (X(gx), X(gx)))
    for gy in range(1, 7):
        c.append('<line class="grid" x1="50" y1="%.1f" x2="470" y2="%.1f"/>' % (Y(gy), Y(gy)))
    # elipse de 2 desviaciones
    angd = math.degrees(math.atan2(v1[1], v1[0]))
    sx = (X(1) - X(0))
    sy = (Y(0) - Y(1))
    c.append('<ellipse class="ell" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f %.1f %.1f)"/>'
             % (X(mx), Y(my), 2 * math.sqrt(l1) * sx, 2 * math.sqrt(l2) * sy, -angd, X(mx), Y(my)))
    for x, y in pts:
        c.append('<circle class="pt" cx="%.1f" cy="%.1f" r="3.4"/>' % (X(x), Y(y)))
    L1, L2 = 2 * math.sqrt(l1), 2 * math.sqrt(l2)
    c.append(_flecha(X(mx), Y(my), X(mx + L1 * v1[0]), Y(my + L1 * v1[1]), "vecA thick", "ahA"))
    c.append(_flecha(X(mx), Y(my), X(mx + L2 * v2[0]), Y(my + L2 * v2[1]), "vecB thick", "ahB"))
    c.append('<circle class="mu" cx="%.1f" cy="%.1f" r="5.5"/>' % (X(mx), Y(my)))
    c.append(_t(X(mx) - 10, Y(my) + 22, "μ", "lbl-it"))
    c.append(_t(X(mx + L1 * v1[0]) + 26, Y(my + L1 * v1[1]), "PC1", "lbl-b"))
    c.append(_t(X(mx + L2 * v2[0]) - 6, Y(my + L2 * v2[1]) - 10, "PC2", "lbl-b"))
    tot = l1 + l2
    c.append(_t(500, 60, "λ₁ = %.2f" % l1, "lbl", "start"))
    c.append(_t(500, 82, "λ₂ = %.2f" % l2, "lbl", "start"))
    c.append(_t(500, 112, "PC1 explica %.1f %%" % (100 * l1 / tot), "lbl-s", "start"))
    c.append(_t(500, 132, "PC2 explica %.1f %%" % (100 * l2 / tot), "lbl-s", "start"))
    c.append(_t(500, 166, "Flecha larga: dirección", "lbl-s", "start"))
    c.append(_t(500, 184, "de máxima varianza.", "lbl-s", "start"))
    c.append(_t(500, 206, "Flecha corta: perpendicular", "lbl-s", "start"))
    c.append(_t(500, 224, "(varianza restante).", "lbl-s", "start"))
    c.append(_t(500, 256, "Elipse: 2 desviaciones", "lbl-s", "start"))
    c.append(_t(500, 274, "estándar en cada eje.", "lbl-s", "start"))
    return _svg(700, 340, "".join(c), label="Nube de puntos con ejes principales")


def pca_proyeccion():
    pts, (mx, my), (l1, l2), (v1, v2), S = datos_pca()
    X, Y = _ejes_pca(0, 0, 50, 20, 560, 280, -0.2, 9.2, -0.4, 6.4)
    c = ['<clipPath id="clipP"><rect x="40" y="10" width="580" height="300" rx="10"/></clipPath>',
         '<rect class="panel" x="40" y="10" width="580" height="300" rx="10"/>', '<g clip-path="url(#clipP)">']
    t0, t1 = -6.5, 6.5
    c.append('<line class="pcline" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
             % (X(mx + t0 * v1[0]), Y(my + t0 * v1[1]), X(mx + t1 * v1[0]), Y(my + t1 * v1[1])))
    sel = pts[::3]
    for x, y in sel:
        t = (x - mx) * v1[0] + (y - my) * v1[1]
        px, py = mx + t * v1[0], my + t * v1[1]
        c.append('<line class="resid" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(x), Y(y), X(px), Y(py)))
        c.append('<circle class="proj" cx="%.1f" cy="%.1f" r="3"/>' % (X(px), Y(py)))
        c.append('<circle class="pt" cx="%.1f" cy="%.1f" r="3.6"/>' % (X(x), Y(y)))
    # angulo recto de ejemplo
    x, y = sel[4]
    t = (x - mx) * v1[0] + (y - my) * v1[1]
    px, py = mx + t * v1[0], my + t * v1[1]
    d = 0.18
    sgn = 1 if (x - px) * v2[0] + (y - py) * v2[1] > 0 else -1
    q1 = (px - d * v1[0], py - d * v1[1])
    q2 = (q1[0] + sgn * d * v2[0], q1[1] + sgn * d * v2[1])
    q3 = (px + sgn * d * v2[0], py + sgn * d * v2[1])
    c.append('<polyline class="rightang" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (X(q1[0]), Y(q1[1]), X(q2[0]), Y(q2[1]), X(q3[0]), Y(q3[1])))
    c.append("</g>")
    c.append(_t(X(mx + 3.6 * v1[0]) + 4, Y(my + 3.6 * v1[1]) - 14, "recta PC1", "lbl-b", "end"))
    c.append('<circle class="mu" cx="%.1f" cy="%.1f" r="5"/>' % (X(mx), Y(my)))
    err = sum(((x - mx) * v2[0] + (y - my) * v2[1]) ** 2 for x, y in pts)
    c.append('<circle class="pt" cx="70" cy="330" r="4"/>' + _t(80, 334, "dato original", "lbl-s", "start"))
    c.append('<circle class="proj" cx="180" cy="330" r="4"/>' + _t(190, 334, "proyección sobre PC1", "lbl-s", "start"))
    c.append('<line class="resid" x1="320" y1="330" x2="350" y2="330"/>' + _t(356, 334, "residuo (suma de cuadrados = %.1f, lo que PCA minimiza)" % err, "lbl-s", "start"))
    return _svg(660, 344, "".join(c), label="Proyección ortogonal sobre PC1 y residuos")


SCREE = [5.2, 2.1, 0.9, 0.45, 0.22, 0.13]


def pca_scree():
    tot = sum(SCREE)
    pct = [100 * l / tot for l in SCREE]
    acc = [sum(pct[:i + 1]) for i in range(len(pct))]
    x0, y0, w, h = 70, 30, 480, 250
    c = ['<rect class="panel" x="20" y="10" width="620" height="320" rx="10"/>']

    def Y(v):
        return y0 + h - v / 100 * h
    c.append('<rect class="band" x="%d" y="%.1f" width="%d" height="%.1f"/>' % (x0, Y(95), w, Y(90) - Y(95)))
    c.append(_t(x0 + w + 6, Y(92.5) + 4, "90–95 %", "lbl-s", "start"))
    for v in range(0, 101, 20):
        c.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (x0, Y(v), x0 + w, Y(v)))
        c.append(_t(x0 - 8, Y(v) + 4, "%d %%" % v, "lbl-s", "end"))
    k = len(SCREE)
    bw = w / k
    pts = []
    for i in range(k):
        bx = x0 + i * bw + bw * 0.2
        c.append('<rect class="bar" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"><title>PC%d: %.1f %%</title></rect>'
                 % (bx, Y(pct[i]), bw * 0.6, Y(0) - Y(pct[i]), i + 1, pct[i]))
        c.append(_t(bx + bw * 0.3, Y(pct[i]) - 6, "%.1f" % pct[i], "lbl-s"))
        c.append(_t(bx + bw * 0.3, y0 + h + 18, "PC%d" % (i + 1), "lbl-s"))
        pts.append((bx + bw * 0.3, Y(acc[i])))
    c.append('<polyline class="cum" points="%s"/>' % " ".join("%.1f,%.1f" % p for p in pts))
    for i, (px, py) in enumerate(pts):
        cls = "cumpt hit" if acc[i] >= 90 and (i == 0 or acc[i - 1] < 90) else "cumpt"
        c.append('<circle class="%s" cx="%.1f" cy="%.1f" r="4.5"><title>acumulado: %.1f %%</title></circle>' % (cls, px, py, acc[i]))
    kk = next(i for i in range(k) if acc[i] >= 90)
    c.append(_t(pts[kk][0] + 14, pts[kk][1] + 34, "con %d componentes: %.1f %%" % (kk + 1, acc[kk]), "lbl-b", "start"))
    c.append(_t(x0 + w / 2, y0 + h + 40, "Barras: % de varianza de cada componente · Línea: % acumulado (codo en PC2–PC3)", "lbl-s"))
    return _svg(660, 340, "".join(c), label="Gráfica de codo y varianza acumulada")


# ---------------------------------------------------------------------------
# TFAL
# ---------------------------------------------------------------------------
def tfal_cuatro():
    """Esquema clásico de los cuatro subespacios (dos rectángulos por lado en ángulo recto)."""
    c = []
    W, H = 760, 420
    oy = 236
    ox1, ox2 = 205, 555
    k = math.sqrt(0.5)
    up_r, up_l = (k, -k), (-k, -k)          # direcciones en pantalla
    dn_r, dn_l = (k, k), (-k, k)

    def rect(o, a, la, b, lb):
        p0 = o
        p1 = (o[0] + a[0] * la, o[1] + a[1] * la)
        p2 = (p1[0] + b[0] * lb, p1[1] + b[1] * lb)
        p3 = (o[0] + b[0] * lb, o[1] + b[1] * lb)
        pts = [p0, p1, p2, p3]
        cen = (sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4)
        return " ".join("%.1f,%.1f" % p for p in pts), cen
    O1, O2 = (ox1, oy), (ox2, oy)
    fila, cf = rect(O1, up_l, 150, up_r, 100)
    nulo, cn = rect(O1, dn_r, 120, up_r, 100)
    col, cc = rect(O2, up_r, 150, up_l, 100)
    lnul, cl = rect(O2, dn_l, 120, up_l, 100)
    c.append('<polygon class="sub-row" points="%s"/>' % fila)
    c.append('<polygon class="sub-null" points="%s"/>' % nulo)
    c.append('<polygon class="sub-col" points="%s"/>' % col)
    c.append('<polygon class="sub-lnull" points="%s"/>' % lnul)
    for o, sgn in [(O1, 1), (O2, -1)]:
        d = 12
        p1 = (o[0] + sgn * 0 + up_r[0] * d * sgn, o[1] + up_r[1] * d)
        c.append('<polyline class="rightang" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>'
                 % (o[0] + up_r[0] * d * sgn, o[1] + up_r[1] * d,
                    o[0] + up_r[0] * d * sgn + (dn_r[0] if sgn > 0 else dn_l[0]) * d, o[1] + up_r[1] * d + dn_r[1] * d,
                    o[0] + (dn_r[0] if sgn > 0 else dn_l[0]) * d, o[1] + dn_r[1] * d))
        del p1
    def etiqueta(cen, a, b, cdim):
        return (_t(cen[0], cen[1] - 8, a, "lbl-b") + _t(cen[0], cen[1] + 9, b, "lbl-s") + _t(cen[0], cen[1] + 24, cdim, "lbl-s"))
    c.append(etiqueta((cf[0], cf[1] + 4), "C(Aᵀ)", "espacio fila", "dim r"))
    c.append(etiqueta((cn[0] + 6, cn[1] + 4), "N(A)", "espacio nulo", "dim n − r"))
    c.append(etiqueta((cc[0], cc[1] + 4), "C(A)", "espacio columna", "dim r"))
    c.append(etiqueta((cl[0] - 6, cl[1] + 4), "N(Aᵀ)", "nulo izquierdo", "dim m − r"))
    c.append(_t(ox1 - 20, 24, "ℝⁿ (dominio)", "lbl-b"))
    c.append(_t(ox2 + 20, 24, "ℝᵐ (codominio)", "lbl-b"))
    c.append('<circle class="dot" cx="%d" cy="%d" r="4"/>' % O1)
    c.append('<circle class="dot" cx="%d" cy="%d" r="5"/>' % O2)
    c.append(_t(ox2 + 14, oy + 18, "0", "lbl-b", "start"))
    xr = (cf[0] + 18, cf[1] - 44)
    b = (cc[0] - 18, cc[1] - 44)
    c.append('<circle class="dot a" cx="%.1f" cy="%.1f" r="4.5"/>' % xr)
    c.append(_t(xr[0] - 8, xr[1] - 8, "xᵣ", "lbl-it", "end"))
    c.append('<circle class="dot a" cx="%.1f" cy="%.1f" r="4.5"/>' % b)
    c.append(_t(b[0] + 8, b[1] - 8, "Axᵣ = b", "lbl-it", "start"))
    c.append('<path class="map-a" d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" marker-end="url(#ahA)"/>'
             % (xr[0] + 6, xr[1] - 3, 330, 30, 430, 30, b[0] - 8, b[1] - 4))
    c.append(_t(380, 58, "A: C(Aᵀ) → C(A) es biyectiva", "lbl-s"))
    xn = (cn[0] + 28, cn[1] + 40)
    c.append('<circle class="dot b" cx="%.1f" cy="%.1f" r="4.5"/>' % xn)
    c.append(_t(xn[0] + 4, xn[1] + 20, "xₙ", "lbl-it"))
    c.append('<path class="map-b" d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" marker-end="url(#ahB)"/>'
             % (xn[0] + 6, xn[1] + 2, 380, 400, 500, 360, ox2 - 6, oy + 7))
    c.append(_t(430, 368, "A xₙ = 0", "lbl-s"))
    c.append(_t(380, 410, "x = xᵣ + xₙ   ⟹   Ax = Axᵣ + Axₙ = b + 0 = b", "lbl"))
    return _svg(W, H + 6, "".join(c), label="Los cuatro subespacios fundamentales")


A_TFAL = [[1, 0, 1], [0, 1, 1]]
X_TFAL = (2.2, 0.6, 0.4)


def _proy_tfal():
    # base ortonormal del espacio fila y vector nulo
    import itertools  # noqa
    r1, r2 = A_TFAL
    def dot(a, b): return sum(x * y for x, y in zip(a, b))
    def sub(a, b): return tuple(x - y for x, y in zip(a, b))
    def mul(k, a): return tuple(k * x for x in a)
    def nrm(a): return math.sqrt(dot(a, a))
    e1 = mul(1 / nrm(r1), r1)
    w = sub(r2, mul(dot(r2, e1), e1))
    e2 = mul(1 / nrm(w), w)
    nvec = (1, 1, -1)
    nn = mul(1 / nrm(nvec), nvec)
    x = X_TFAL
    xr = tuple(dot(x, e1) * a + dot(x, e2) * b for a, b in zip(e1, e2))
    xn = sub(x, xr)
    return e1, e2, nn, x, xr, xn


def tfal_3d():
    e1, e2, nn, x, xr, xn = _proy_tfal()
    az, el = math.radians(110), math.radians(25)

    def P(v):
        X, Y, Z = v
        x2 = X * math.cos(az) - Y * math.sin(az)
        y2 = (X * math.sin(az) + Y * math.cos(az)) * math.sin(el) + Z * math.cos(el)
        return 330 + 78 * x2, 215 - 78 * y2
    c = []
    k = 1.9
    esq = [tuple(a * s + b * t for a, b in zip(e1, e2)) for s, t in [(-k, -k), (k, -k), (k, k), (-k, k)]]
    L = 2.4
    a, b = P(tuple(-L * t for t in nn)), P(tuple(L * t for t in nn))
    O = P((0, 0, 0))
    # parte trasera de la recta, el plano encima, y la parte delantera
    c.append('<line class="nline" stroke-dasharray="5 4" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (a + O))
    c.append('<polygon class="plane" points="%s"/>' % " ".join("%.1f,%.1f" % P(p) for p in esq))
    c.append('<line class="nline" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (O + b))
    c.append('<circle class="dot" cx="%.1f" cy="%.1f" r="4"/>' % O)
    px, pr, pn = P(x), P(xr), P(xn)
    c.append('<line class="guide" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (px + pr))
    c.append('<line class="guide" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (px + pn))
    for q, cls, mk in [(pr, "vecA thick", "ahA"), (pn, "vecB thick", "ahB"), (px, "vecX thick", "ah")]:
        c.append(_flecha(O[0], O[1], q[0], q[1], cls, mk))
    c.append(_t(px[0] + 10, px[1] - 8, "x", "lbl-it", "start"))
    c.append(_t(pr[0] + 10, pr[1] + 18, "xᵣ ∈ C(Aᵀ)", "lbl-it", "start"))
    c.append(_t(pn[0] - 10, pn[1] - 6, "xₙ ∈ N(A)", "lbl-it", "end"))
    pp = P(tuple(-1.6 * a_ + 1.5 * b_ for a_, b_ in zip(e1, e2)))
    c.append(_t(pp[0], pp[1], "plano C(Aᵀ)", "lbl-b"))
    c.append(_t(b[0] - 6, b[1] + 18, "recta N(A)", "lbl-b", "start"))
    txt1 = "A = [[1,0,1],[0,1,1]],   x = (%.1f, %.1f, %.1f) = xᵣ + xₙ" % x
    txt2 = "xᵣ = (%.2f, %.2f, %.2f),   xₙ = (%.2f, %.2f, %.2f),   xᵣ · xₙ = 0" % (xr + xn)
    c.append(_t(330, 392, txt1, "lbl-s"))
    c.append(_t(330, 410, txt2, "lbl-s"))
    return _svg(660, 420, "".join(c), label="Descomposición ortogonal x = xr + xn")


# ---------------------------------------------------------------------------
# Campos finitos: aritmética
# ---------------------------------------------------------------------------
def gf_mul(a, b, poly, n):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & (1 << n):
            a ^= poly
    return r


def orden_x(poly, n):
    x, k = 2, 1
    while x != 1:
        x = gf_mul(x, 2, poly, n)
        k += 1
        if k > (1 << n):
            return None
    return k


def es_irreducible(poly, n):
    # prueba por división con todos los polinomios de grado 1..n/2
    def deg(p): return p.bit_length() - 1

    def mod(a, b):
        db = deg(b)
        while a and deg(a) >= db:
            a ^= b << (deg(a) - db)
        return a
    for d in range(1, n // 2 + 1):
        for q in range(1 << d, 1 << (d + 1)):
            if mod(poly, q) == 0:
                return False
    return True


def poli_tex(bits_int, n, var="x"):
    t = []
    for i in range(n, -1, -1):
        if (bits_int >> i) & 1:
            t.append("1" if i == 0 else (var if i == 1 else "%s^{%d}" % (var, i)))
    return "+".join(t) if t else "0"


def potencias(poly, n):
    """lista de (k, valor) para alpha^k, k = 0..orden-1"""
    out, x, k = [], 1, 0
    while True:
        out.append((k, x))
        x = gf_mul(x, 2, poly, n)
        k += 1
        if x == 1:
            break
    return out


# ---------------------------------------------------------------------------
# Campos finitos: figuras
# ---------------------------------------------------------------------------
def gf_ciclo():
    c = []
    pot = potencias(0b10011, 4)
    cx, cy, R = 200, 228, 140
    c.append('<circle class="ring" cx="%d" cy="%d" r="%d"/>' % (cx, cy, R))
    c.append(_t(cx, 26, "α primitivo en 𝔽₁₆ (x⁴+x+1): orden 15", "lbl-b"))
    for i, (k, v) in enumerate(pot):
        a = -math.pi / 2 + 2 * math.pi * i / 15
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        a2 = -math.pi / 2 + 2 * math.pi * (i + 1) / 15
        x2, y2 = cx + R * math.cos(a2), cy + R * math.sin(a2)
        mx, my = cx + R * math.cos((a + a2) / 2), cy + R * math.sin((a + a2) / 2)
        c.append('<path class="ring-arc" d="M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f" marker-end="url(#ah)"/>'
                 % (x + 14 * math.cos(a + 1.57), y + 14 * math.sin(a + 1.57), R, R, x2 - 14 * math.cos(a2 + 1.57), y2 - 14 * math.sin(a2 + 1.57)))
        cls = "gfnode one" if v == 1 else "gfnode"
        c.append('<g class="%s"><circle cx="%.1f" cy="%.1f" r="17"/><text x="%.1f" y="%.1f">%X</text></g>' % (cls, x, y, x, y + 4, v))
        lx, ly = cx + (R + 32) * math.cos(a), cy + (R + 32) * math.sin(a)
        c.append(_t(lx, ly + 4, "α<tspan baseline-shift='super' font-size='70%%'>%d</tspan>" % k, "lbl-s"))
        del mx, my
    c.append(_t(cx, cy - 6, "15 elementos", "lbl-b"))
    c.append(_t(cx, cy + 14, "no nulos (hex)", "lbl-s"))
    # gamma de orden 5
    pot5 = potencias(0b11111, 4)
    cx2, R2 = 560, 80
    c.append('<circle class="ring alt" cx="%d" cy="%d" r="%d"/>' % (cx2, cy, R2))
    c.append(_t(cx2, 26, "γ en x⁴+x³+x²+x+1: orden 5", "lbl-b"))
    for i, (k, v) in enumerate(pot5):
        a = -math.pi / 2 + 2 * math.pi * i / 5
        x, y = cx2 + R2 * math.cos(a), cy + R2 * math.sin(a)
        cls = "gfnode one" if v == 1 else "gfnode alt"
        c.append('<g class="%s"><circle cx="%.1f" cy="%.1f" r="17"/><text x="%.1f" y="%.1f">%X</text></g>' % (cls, x, y, x, y + 4, v))
        lx, ly = cx2 + (R2 + 30) * math.cos(a), cy + (R2 + 30) * math.sin(a)
        c.append(_t(lx, ly + 4, "γ<tspan baseline-shift='super' font-size='70%%'>%d</tspan>" % k, "lbl-s"))
    c.append(_t(cx2, cy + 4, "γ⁵ = 1", "lbl-b"))
    c.append(_t(cx2, 360, "Sólo visita 5 de los 15 elementos no nulos:", "lbl-s"))
    c.append(_t(cx2, 378, "irreducible, pero NO primitivo.", "lbl-s"))
    return _svg(720, 410, "".join(c), label="Ciclo multiplicativo y elemento primitivo")


def gf_diccionario():
    c = []
    # palabra 1011 -> polinomio -> hex
    bits = "1011"
    x0 = 30
    c.append(_t(360, 24, "Una palabra de n bits = un polinomio de grado < n = un número", "lbl-b"))
    for i, b in enumerate(bits):
        c.append('<g class="bitcell %s"><rect x="%d" y="44" width="40" height="40" rx="6"/><text x="%d" y="70">%s</text></g>'
                 % ("on" if b == "1" else "", x0 + 44 * i, x0 + 44 * i + 20, b))
        c.append(_t(x0 + 44 * i + 20, 100, "x<tspan baseline-shift='super' font-size='70%%'>%d</tspan>" % (3 - i), "lbl-s"))
    c.append(_flecha(210, 64, 262, 64, "arrow-step", "ah"))
    c.append('<rect class="panel" x="268" y="40" width="200" height="48" rx="8"/>')
    c.append(_t(368, 70, "x³ + x + 1", "lbl-big2"))
    c.append(_flecha(474, 64, 526, 64, "arrow-step", "ah"))
    c.append('<rect class="panel" x="532" y="40" width="160" height="48" rx="8"/>')
    c.append(_t(612, 70, "0xB  (= 11)", "lbl-big2"))
    # desplazamiento y reducción
    y = 150
    c.append(_t(360, y - 14, "Multiplicar por x en 𝔽₁₆ (P = x⁴+x+1 = 10011): desplazar << 1 y, si se desborda, XOR con P", "lbl-b"))
    filas = [("a = α⁶", "01100", ""), ("a << 1", "11000", "bit 4 encendido → desborda"),
             ("XOR P", "10011", ""), ("α⁷", "01011", "= x³ + x + 1 = 0xB")]
    for j, (lab, bb, nota) in enumerate(filas):
        yy = y + 8 + j * 40
        c.append(_t(150, yy + 22, lab, "lbl", "end"))
        for i, b in enumerate(bb):
            cls = "bitcell on" if b == "1" else "bitcell"
            if i == 0 and j in (1, 2):
                cls += " ovf"
            c.append('<g class="%s"><rect x="%d" y="%d" width="32" height="32" rx="5"/><text x="%d" y="%d">%s</text></g>'
                     % (cls, 170 + 36 * i, yy, 170 + 36 * i + 16, yy + 21, b))
        if nota:
            c.append(_t(360, yy + 21, nota, "lbl-s", "start"))
        if j == 2:
            c.append('<line class="axis" x1="166" y1="%d" x2="350" y2="%d"/>' % (yy + 37, yy + 37))
    return _svg(720, 330, "".join(c), label="Diccionario polinomio, bits y hexadecimal")


def gf_reticulo():
    c = []
    # cadena F2 ⊂ F4 ⊂ F16
    c.append(_t(150, 24, "𝔽₂ ⊂ 𝔽₄ ⊂ 𝔽₁₆", "lbl-b"))
    nodos = [("𝔽₁₆", 150, 70, "2⁴"), ("𝔽₄", 150, 170, "2²"), ("𝔽₂", 150, 270, "2¹")]
    for i in range(2):
        c.append('<line class="lat" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (150, nodos[i][2] + 22, 150, nodos[i + 1][2] - 22))
    for nm, x, y, o in nodos:
        c.append('<g class="latnode"><circle cx="%d" cy="%d" r="24"/><text x="%d" y="%d">%s</text></g>' % (x, y, x, y + 5, nm))
        c.append(_t(x + 34, y + 5, "orden " + o, "lbl-s", "start"))
    c.append(_t(150, 318, "𝔽₈ ⊄ 𝔽₁₆ porque 3 ∤ 4", "lbl-s"))
    # retículo de F_{2^12}
    c.append(_t(520, 24, "Subcampos de 𝔽₂¹² (divisores de 12)", "lbl-b"))
    pos = {12: (520, 60), 4: (440, 140), 6: (600, 140), 2: (440, 220), 3: (600, 220), 1: (520, 300)}
    for a in pos:
        for b in pos:
            if a != b and a % b == 0 and not any(m != a and m != b and a % m == 0 and m % b == 0 for m in pos):
                c.append('<line class="lat" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (pos[a] + pos[b]))
    for m, (x, y) in pos.items():
        c.append('<g class="latnode"><circle cx="%d" cy="%d" r="24"/><text x="%d" y="%d">𝔽<tspan baseline-shift="sub" font-size="68%%">2%s</tspan></text></g>' % (x, y, x, y + 5, "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(ch)] for ch in str(m))))
    c.append(_t(520, 340, "Hay una arista 𝔽₂ᵐ ⊂ 𝔽₂ⁿ exactamente cuando m | n.", "lbl-s"))
    return _svg(720, 356, "".join(c), label="Retículo de subcampos")


def _lfsr_estados(poly_taps, n=4, s0=(0, 0, 0, 1)):
    """s_{k+4} = combinación XOR según taps; devuelve lista de estados hasta repetir"""
    estados = [tuple(s0)]
    s = list(s0)
    while True:
        nuevo = 0
        for t in poly_taps:
            nuevo ^= s[t]
        s = s[1:] + [nuevo]
        if tuple(s) == tuple(s0):
            break
        estados.append(tuple(s))
    return estados


def gf_lfsr():
    c = []
    c.append(_t(360, 22, "LFSR de 4 celdas con x⁴ + x + 1:  s₍ₖ₊₄₎ = s₍ₖ₊₁₎ ⊕ sₖ", "lbl-b"))
    x0, y0 = 150, 50
    for i in range(4):
        c.append('<g class="bitcell"><rect x="%d" y="%d" width="70" height="44" rx="6"/><text x="%d" y="%d">s%s</text></g>'
                 % (x0 + 80 * i, y0, x0 + 80 * i + 35, y0 + 28, "₀₁₂₃"[i]))
    for i in range(3):
        c.append(_flecha(x0 + 80 * (i + 1) - 2, y0 + 22, x0 + 80 * i + 72, y0 + 22, "arrow-step", "ah"))
    c.append(_flecha(x0 - 2, y0 + 22, x0 - 52, y0 + 22, "arrow-step", "ah"))
    c.append(_t(x0 - 60, y0 + 26, "salida", "lbl-s", "end"))
    # XOR
    xx, yy = x0 + 75, y0 + 110
    c.append('<g class="xor"><circle cx="%d" cy="%d" r="15"/><text x="%d" y="%d">⊕</text></g>' % (xx, yy, xx, yy + 6))
    c.append('<path class="fb" d="M%d,%d L%d,%d" marker-end="url(#ah)"/>' % (x0 + 35, y0 + 44, xx - 11, yy - 9))
    c.append('<path class="fb" d="M%d,%d L%d,%d" marker-end="url(#ah)"/>' % (x0 + 115, y0 + 44, xx + 11, yy - 9))
    c.append('<path class="fb" d="M%d,%d L%d,%d L%d,%d" marker-end="url(#ah)"/>' % (xx + 15, yy, x0 + 80 * 3 + 35, yy, x0 + 80 * 3 + 35, y0 + 46))
    c.append(_t(xx + 90, yy - 6, "realimentación", "lbl-s"))
    # estados
    prim = _lfsr_estados([0, 1])            # x^4+x+1
    noprim = _lfsr_estados([0, 1, 2, 3])    # x^4+x^3+x^2+x+1
    y1 = 220
    c.append(_t(20, y1, "x⁴+x+1 (primitivo): periodo %d = 2⁴ − 1" % len(prim), "lbl-b", "start"))
    for i, st in enumerate(prim):
        c.append('<g class="state"><rect x="%d" y="%d" width="40" height="24" rx="4"/><text x="%d" y="%d">%s</text></g>'
                 % (20 + 46 * i, y1 + 10, 40 + 46 * i, y1 + 27, "".join(map(str, st))))
    y2 = 290
    c.append(_t(20, y2, "x⁴+x³+x²+x+1 (irreducible, no primitivo): periodo %d" % len(noprim), "lbl-b", "start"))
    for i, st in enumerate(noprim):
        c.append('<g class="state alt"><rect x="%d" y="%d" width="40" height="24" rx="4"/><text x="%d" y="%d">%s</text></g>'
                 % (20 + 46 * i, y2 + 10, 40 + 46 * i, y2 + 27, "".join(map(str, st))))
    c.append(_t(20 + 46 * len(noprim) + 6, y2 + 27, "↺ regresa a 0001 y se corta el ciclo", "lbl-s", "start"))
    return _svg(720, 340, "".join(c), label="LFSR primitivo frente a no primitivo")


def gf_flujo():
    c = []
    c.append(_t(180, 24, "Paso a paso: xtime / campesino ruso — O(n)", "lbl-b"))
    pasos = ["a, b ∈ 𝔽₂ⁿ", "¿bit menor de b = 1?  →  r ⊕= a", "b >>= 1", "a = xtime(a)  (<<1, XOR P si desborda)", "repetir n veces → r = a·b"]
    for i, p in enumerate(pasos):
        y = 44 + i * 56
        c.append('<rect class="flowbox" x="20" y="%d" width="320" height="40" rx="8"/>' % y)
        c.append(_t(180, y + 25, p, "lbl"))
        if i < len(pasos) - 1:
            c.append(_flecha(180, y + 40, 180, y + 54, "arrow-step", "ah"))
    c.append('<path class="loop" d="M340,%d C390,%d 390,%d 340,%d" marker-end="url(#ah)"/>' % (44 + 3 * 56 + 20, 44 + 3 * 56 + 20, 44 + 56 + 20, 44 + 56 + 20))
    c.append(_t(540, 24, "Con tablas log / exp — O(1)", "lbl-b"))
    pasos2 = ["precalcular exp[k] = αᵏ y log[αᵏ] = k", "a·b = exp[(log a + log b) mod (q−1)]", "a⁻¹ = exp[(q−1) − log a]", "a/b = exp[log a − log b]"]
    for i, p in enumerate(pasos2):
        y = 44 + i * 70
        c.append('<rect class="flowbox alt" x="380" y="%d" width="320" height="44" rx="8"/>' % y)
        c.append(_t(540, y + 27, p, "lbl"))
        if i == 0:
            c.append(_flecha(540, y + 44, 540, y + 68, "arrow-step", "ah"))
    c.append(_t(540, 330, "Una suma de enteros y dos consultas a tabla:", "lbl-s"))
    c.append(_t(540, 348, "sin divisiones polinomiales (tablas < 1 KB en 𝔽₂₅₆)", "lbl-s"))
    return _svg(720, 360, "".join(c), label="Aritmética rápida en computadora")


# ---------------------------------------------------------------------------
# Campos finitos: tablas
# ---------------------------------------------------------------------------
def tabla_operaciones():
    filas = [
        ("Suma / resta", "suma de coeficientes mód 2", "$a \\oplus b$ (XOR, 1 instrucción)", "$a+a=0$, por eso $-a=a$"),
        ("Multiplicación por $x$", "subir un grado; si llega a grado $n$, restar $P$", "$a \\ll 1$ y, si el bit $n$ se enciende, XOR con $P$ (<em>xtime</em>)", "$O(1)$"),
        ("Cuadrado $a^2$", "$(a+b)^2=a^2+b^2$: es lineal (Frobenius)", "intercalar ceros entre los bits y reducir", "sin multiplicaciones"),
        ("Multiplicación general", "producto de polinomios y reducción mód $P$", "campesino ruso: $n$ pasos de xtime y XOR; o tablas log/exp", "$O(n)$ frente a $O(1)$"),
        ("Inverso $a^{-1}$", "Euclides extendido: $ua+vP=1$", "tabla: $a^{-1}=\\alpha^{(q-1)-\\log a}$; Fermat: $a^{-1}=a^{q-2}$", "$O(n^2)$, $O(\\log q)$ o $O(1)$"),
    ]
    h = ['<div class="table-wrap"><table>',
         "<thead><tr><th>Operación</th><th>En polinomios</th><th>En bits (máquina)</th><th>Costo / nota</th></tr></thead><tbody>"]
    for f in filas:
        h.append("<tr>" + "".join("<td>%s</td>" % x for x in f) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)


def _tabla_campo(poly, n, var="\\alpha"):
    q = 1 << n
    pot = potencias(poly, n)
    log = {v: k for k, v in pot}
    h = ['<div class="table-wrap"><table class="t-compact">',
         "<thead><tr><th>Potencia</th><th>Polinomio</th><th>Bits</th>%s<th>$\\log_\\alpha a$</th><th>$a^{-1}$</th></tr></thead><tbody>"
         % ("<th>Hex</th>" if n == 4 else "<th>Entero</th>")]
    for k, v in pot:
        inv = pot[(q - 1 - k) % (q - 1)][1]
        h.append('<tr><td>$%s^{%d}$</td><td>$%s$</td><td class="mono">%s</td><td class="mono">%s</td><td>%d</td><td class="mono">%s</td></tr>'
                 % (var, k, poli_tex(v, n - 1, var), format(v, "0%db" % n),
                    ("%X" % v) if n == 4 else str(v), log[v],
                    ("%X" % inv) if n == 4 else str(inv)))
    h.append("</tbody></table></div>")
    return "\n".join(h)


def tabla_potencias():
    partes = []
    for nombre, poly, n in [("$\\mathbb{F}_4=\\mathbb{F}_2[x]/(x^2+x+1)$, regla $\\alpha^2=\\alpha+1$", 0b111, 2),
                            ("$\\mathbb{F}_8=\\mathbb{F}_2[x]/(x^3+x+1)$, regla $\\alpha^3=\\alpha+1$", 0b1011, 3),
                            ("$\\mathbb{F}_{16}=\\mathbb{F}_2[x]/(x^4+x+1)$, regla $\\alpha^4=\\alpha+1$", 0b10011, 4)]:
        partes.append('<div class="tcol"><div class="tcap">%s</div>%s</div>' % (nombre, _tabla_campo(poly, n)))
    return '<div class="tgrid">%s</div>' % "".join(partes)


def tabla_producto(poly, n):
    q = 1 << n
    fmt = (lambda v: "%X" % v) if n == 4 else str
    h = ['<div class="table-wrap"><table class="t-mult">', "<tr><th>·</th>" + "".join("<th>%s</th>" % fmt(b) for b in range(1, q)) + "</tr>"]
    for a in range(1, q):
        h.append("<tr><th>%s</th>" % fmt(a) + "".join('<td%s>%s</td>' % (' class="one"' if gf_mul(a, b, poly, n) == 1 else "", fmt(gf_mul(a, b, poly, n))) for b in range(1, q)) + "</tr>")
    h.append("</table></div>")
    return "\n".join(h)


IRREDUCIBLES = [
    (2, 0b111, "único irreducible de grado 2"),
    (3, 0b1011, "el más usado para 𝔽₈"),
    (3, 0b1101, "recíproco del anterior"),
    (4, 0b10011, "estándar para 𝔽₁₆"),
    (4, 0b11001, "recíproco de x⁴+x+1"),
    (4, 0b11111, "raíces quintas de la unidad: (x⁵−1)/(x−1)"),
    (8, 0x11B, "AES (FIPS-197); allí el generador es 0x03"),
    (8, 0x11D, "códigos QR y Reed–Solomon"),
    (8, 0x12B, "otro primitivo de grado 8"),
]


def tabla_irreducibles():
    h = ['<div class="table-wrap"><table>',
         "<thead><tr><th>Grado $n$</th><th>Polinomio</th><th>Hex</th><th>¿Irreducible?</th><th>$\\mathrm{ord}(x)$</th><th>¿Primitivo? ($\\mathrm{ord}=2^n-1$)</th><th>Uso / comentario</th></tr></thead><tbody>"]
    for n, p, nota in IRREDUCIBLES:
        irr = es_irreducible(p, n)
        o = orden_x(p, n)
        prim = o == (1 << n) - 1
        h.append('<tr><td class="c">%d</td><td>$%s$</td><td class="mono">0x%X</td><td class="c">%s</td><td class="c">%d</td><td class="c %s">%s</td><td>%s</td></tr>'
                 % (n, poli_tex(p, n), p, "sí" if irr else "no", o, "yes" if prim else "no",
                    "sí" if prim else "no (orden %d &lt; %d)" % (o, (1 << n) - 1), nota))
    h.append("</tbody></table></div>")
    return "\n".join(h)


def tabla_aplicaciones():
    filas = [
        ("AES (cifrado simétrico)", "$\\mathbb{F}_{256}$, $x^8+x^4+x^3+x+1$ (0x11B)", "Caja-S = inverso $a^{-1}$ + afín; MixColumns = matriz $4\\times4$ sobre el campo"),
        ("GCM (TLS 1.3)", "$\\mathbb{F}_{2^{128}}$, $x^{128}+x^7+x^2+x+1$", "GHASH: evaluar un polinomio en $H$; un polinomio de grado $m$ tiene $\\le m$ raíces"),
        ("Reed–Solomon / códigos QR / RAID-6", "$\\mathbb{F}_{256}$, $x^8+x^4+x^3+x^2+1$ (0x11D)", "Evaluar polinomios de grado $&lt;k$ en $n$ puntos; $d=n-k+1$ (MDS); RAID-6: $P=\\oplus D_i$, $Q=\\oplus\\alpha^iD_i$"),
        ("LFSR (GPS, CDMA, pruebas BIST)", "$\\mathbb{F}_{2^n}$ con polinomio primitivo", "Periodo máximo $2^n-1$ (m-secuencias)"),
        ("Compartición de secretos de Shamir", "$\\mathbb{F}_q$ (p. ej. $\\mathbb{F}_{256}$)", "Polinomio aleatorio de grado $k-1$; interpolación de Lagrange con $k$ puntos"),
        ("Llave pública (Diffie–Hellman, curvas elípticas, McEliece)", "$\\mathbb{F}_p^*$, $\\mathbb{F}_{2^m}$, $\\mathbb{F}_{2^{13}}$", "Logaritmo discreto difícil; inversos del campo; códigos de Goppa"),
        ("CRC (Ethernet, ZIP, PNG)", "$\\mathbb{F}_2[x]$", "Residuo de una división de polinomios (no requiere irreducible)"),
    ]
    h = ['<div class="table-wrap"><table>',
         "<thead><tr><th>Aplicación</th><th>Campo y polinomio</th><th>Estructura que usa</th></tr></thead><tbody>"]
    for f in filas:
        h.append("<tr>" + "".join("<td>%s</td>" % x for x in f) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)


def tabla_campos16():
    filas = [(2, "2¹", 2, "$\\mathbb{Z}/(2)$"), (3, "3¹", 3, "$\\mathbb{Z}/(3)$"), (4, "2²", 2, "$\\mathbb{F}_2[x]/(x^2+x+1)$"),
             (5, "5¹", 5, "$\\mathbb{Z}/(5)$"), (7, "7¹", 7, "$\\mathbb{Z}/(7)$"), (8, "2³", 2, "$\\mathbb{F}_2[x]/(x^3+x+1)$"),
             (9, "3²", 3, "$\\mathbb{F}_3[x]/(x^2+1)$"), (11, "11¹", 11, "$\\mathbb{Z}/(11)$"), (13, "13¹", 13, "$\\mathbb{Z}/(13)$"),
             (16, "2⁴", 2, "$\\mathbb{F}_2[x]/(x^4+x+1)$")]
    h = ['<div class="table-wrap"><table class="t-compact">', "<thead><tr><th>$q$</th><th>forma</th><th>car</th><th>construcción</th></tr></thead><tbody>"]
    for f in filas:
        h.append('<tr><td class="c">%d</td><td class="c">%s</td><td class="c">%d</td><td>%s</td></tr>' % f)
    h.append("</tbody></table></div>")
    return "\n".join(h)


FIGURAS = {
    "svd_circulo": svd_circulo, "svd_bloques": svd_bloques,
    "pca_nube": pca_nube, "pca_proyeccion": pca_proyeccion, "pca_scree": pca_scree,
    "tfal_cuatro": tfal_cuatro, "tfal_3d": tfal_3d,
    "gf_ciclo": gf_ciclo, "gf_diccionario": gf_diccionario, "gf_reticulo": gf_reticulo,
    "gf_lfsr": gf_lfsr, "gf_flujo": gf_flujo,
}
TABLAS = {
    "gf_operaciones": tabla_operaciones, "gf_potencias": tabla_potencias,
    "gf_irreducibles": tabla_irreducibles, "gf_aplicaciones": tabla_aplicaciones,
    "gf_campos16": tabla_campos16,
    "gf_prod8": lambda: tabla_producto(0b1011, 3),
    "gf_prod16": lambda: tabla_producto(0b10011, 4),
}


@lru_cache(maxsize=None)
def figura(nombre):
    return FIGURAS[nombre]()


@lru_cache(maxsize=None)
def tabla(nombre):
    return TABLAS[nombre]()
