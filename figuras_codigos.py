"""
Figuras y tablas de los capítulos 0-8 (códigos binarios), generadas con Python.

Todo se calcula aquí mismo (palabras, distancias, clases laterales, síndromes),
así que las figuras siempre coinciden con las matemáticas. Las imágenes son SVG
en línea que usan variables CSS del sitio, por lo que se adaptan al modo claro
y al modo oscuro.
"""
import itertools
from functools import lru_cache

# ---------------------------------------------------------------------------
# Álgebra binaria básica
# ---------------------------------------------------------------------------
def vec(s):
    return tuple(int(c) for c in s)


def s2(v):
    return "".join(map(str, v))


def add(a, b):
    return tuple((x + y) % 2 for x, y in zip(a, b))


def peso(v):
    return sum(v)


def span(rows, n):
    S = {tuple([0] * n)}
    for r in rows:
        r = vec(r)
        S |= {add(s, r) for s in S}
    return S


def nucleo(H, n):
    H = [vec(h) for h in H]
    return {v for v in itertools.product([0, 1], repeat=n)
            if all(sum(a * b for a, b in zip(h, v)) % 2 == 0 for h in H)}


def dist_minima(C):
    return min(peso(c) for c in C if any(c))


def distribucion_pesos(C, n):
    d = [0] * (n + 1)
    for c in C:
        d[peso(c)] += 1
    return d


def mapa_distancias(C, n):
    D, cnt = {}, {}
    for v in itertools.product([0, 1], repeat=n):
        dd = min(peso(add(v, c)) for c in C)
        D[v] = dd
        cnt[dd] = cnt.get(dd, 0) + 1
    return D, dict(sorted(cnt.items()))


def codificar(u, G):
    c = tuple([0] * len(G[0]))
    for bit, g in zip(u, G):
        if bit == "1":
            c = add(c, vec(g))
    return c


MENSAJES4 = ["".join(m) for m in itertools.product("01", repeat=4)]

# ---------------------------------------------------------------------------
# Los casos de los capítulos 3, 4 y 5 (matrices de control H)
# ---------------------------------------------------------------------------
CASOS_V4 = [["1111"], ["1101"], ["1010", "0101"], ["1100", "0011"],
            ["1010", "1101"], ["0110", "0101"]]
CASOS_V6 = [["111111"], ["110110", "101101"], ["011100", "101010", "110001"],
            ["111000", "110100", "100010", "010001"],
            ["101000", "010100", "100010", "010001"],
            ["110000", "101000", "100100", "100010", "100001"]]
CASOS_V7 = [["1111111"], ["1110010", "0011101"],
            ["0001111", "0110011", "1010101"],
            ["0110100", "1011010", "1101001"],
            ["1110000", "1001100", "0101010", "1101001"],
            ["1100000", "0110000", "0000110", "0000011", "1001100"],
            ["1100000", "1010000", "1001000", "1000100", "1000010", "1000001"]]

# ---------------------------------------------------------------------------
# Figura: hipercubo de V4 (capítulo 3)
# ---------------------------------------------------------------------------
_ESC = 58.0       # píxeles por unidad
_OX, _OY = 40.0, 230.0


def _pos_hc(v):
    c1, c2, c3, c4 = v
    x = 2.4 * c1 + 1.2 * c3 + 5.9 * c4
    y = 2.2 * c2 + 1.0 * c3 - 1.5 * c4
    return _OX + _ESC * x, _OY - _ESC * y


def hipercubo_svg(H=None, interactivo=False, ident="hc"):
    """Hipercubo de V4 como dos cubos (c4=0 y c4=1).

    Si se da H, se resaltan las palabras del código y en rojo punteado las
    aristas que unen dos palabras del código (distancia 1)."""
    C = nucleo(H, 4) if H else set()
    verts = list(itertools.product([0, 1], repeat=4))
    out = ['<svg class="svgfig hc" id="%s" viewBox="0 0 640 330" role="img" '
           'aria-label="Hipercubo de V4">' % ident]
    rojas = []
    for a in verts:
        for b in verts:
            if a < b and peso(add(a, b)) == 1:
                i = [j for j in range(4) if a[j] != b[j]][0]
                (x1, y1), (x2, y2) = _pos_hc(a), _pos_hc(b)
                if a in C and b in C:
                    rojas.append((x1, y1, x2, y2))
                    continue
                cls = "hc-e4" if i == 3 else "hc-e3"
                out.append('<line class="%s" data-a="%s" data-b="%s" x1="%.1f" '
                           'y1="%.1f" x2="%.1f" y2="%.1f"/>'
                           % (cls, s2(a), s2(b), x1, y1, x2, y2))
    for x1, y1, x2, y2 in rojas:
        out.append('<line class="hc-red" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                   % (x1, y1, x2, y2))
    for v in verts:
        x, y = _pos_hc(v)
        cls = "hc-node cw" if v in C else "hc-node"
        out.append('<g class="%s" data-w="%s" transform="translate(%.1f,%.1f)">'
                   '<rect x="-27" y="-11" width="54" height="22" rx="5"/>'
                   '<text y="4">%s</text></g>' % (cls, s2(v), x, y, s2(v)))
    out.append('<text class="hc-lab" x="150" y="22">cubo c₄ = 0</text>')
    out.append('<text class="hc-lab" x="470" y="22">cubo c₄ = 1</text>')
    out.append("</svg>")
    return "\n".join(out)


def leyenda_hipercubo():
    return """<div class="legend">
<span><svg width="46" height="20"><rect class="lg-cw" x="1" y="2" width="44" height="16" rx="4"/></svg> palabra del código</span>
<span><svg width="46" height="20"><rect class="lg-ncw" x="1" y="2" width="44" height="16" rx="4"/></svg> palabra fuera del código</span>
<span><svg width="40" height="10"><line class="hc-e3" x1="0" y1="5" x2="40" y2="5"/></svg> arista (cambia $c_1$, $c_2$ o $c_3$)</span>
<span><svg width="40" height="10"><line class="hc-e4" x1="0" y1="5" x2="40" y2="5"/></svg> arista entre los dos cubos (cambia $c_4$)</span>
<span><svg width="40" height="10"><line class="hc-red" x1="0" y1="5" x2="40" y2="5"/></svg> arista que une dos palabras del código ($d=1$)</span>
</div>"""


def leyenda_mapa():
    return """<div class="legend">
<span><i class="sw d0"></i> en el código</span>
<span><i class="sw d1"></i> a distancia 1</span>
<span><i class="sw d2"></i> a distancia 2</span>
<span><i class="sw d3"></i> a distancia 3</span>
</div>"""


# ---------------------------------------------------------------------------
# Figura: mapa de distancias + distribución de pesos (capítulos 4 y 5)
# ---------------------------------------------------------------------------
def mapa_svg(H, n):
    C = nucleo(H, n)
    D, cnt = mapa_distancias(C, n)
    W = distribucion_pesos(C, n)
    d = dist_minima(C)
    cb = n - 3
    ncols = 2 ** cb
    cs = 30 if n == 6 else 24
    left, top = 58, 46 if n == 6 else 58
    gw = ncols * cs
    out = []
    # encabezados
    for j in range(ncols):
        lab = format(j, "0%db" % cb)
        x = left + (j + 0.5) * cs
        if n == 6:
            out.append('<text class="mono tiny" x="%.1f" y="%d" text-anchor="middle">%s</text>'
                       % (x, top - 6, lab))
        else:
            out.append('<text class="mono tiny" transform="translate(%.1f,%d) rotate(-90)">%s</text>'
                       % (x + 3, top - 5, lab))
    out.append('<text class="tiny muted" x="4" y="%d">c₁c₂c₃ \\ %s</text>'
               % (top - (22 if n == 6 else 46), "c₄c₅c₆" if n == 6 else "c₄…c₇"))
    for i in range(8):
        lab = format(i, "03b")
        y = top + i * cs
        out.append('<text class="mono tiny" x="%d" y="%.1f" text-anchor="end">%s</text>'
                   % (left - 5, y + cs / 2 + 3, lab))
        for j in range(ncols):
            v = vec(lab + format(j, "0%db" % cb))
            dd = D[v]
            x = left + j * cs
            out.append('<g class="cell d%d"><title>%s · distancia %d</title>'
                       '<rect x="%d" y="%d" width="%d" height="%d"/>'
                       '<text x="%.1f" y="%.1f">%d</text></g>'
                       % (dd, s2(v), dd, x, y, cs, cs, x + cs / 2, y + cs / 2 + 4, dd))
    gh = 8 * cs
    # leyenda con conteos
    ly = top + gh + 22
    for idx, (dd, c) in enumerate(cnt.items()):
        lab = "en el código" if dd == 0 else "a distancia %d" % dd
        x = left + (idx % 2) * (gw / 2)
        y = ly + (idx // 2) * 18
        out.append('<rect class="sw-r d%d" x="%.1f" y="%d" width="12" height="12" rx="2"/>'
                   '<text class="tiny" x="%.1f" y="%d">%d %s</text>'
                   % (dd, x, y - 10, x + 17, y, c, lab))
    out.append('<text class="figlab" x="%.1f" y="%d" text-anchor="middle">Mapa de las %d palabras de V%s</text>'
               % (left + gw / 2, ly + 46, 2 ** n, "₆" if n == 6 else "₇"))
    # barras
    gx = left + gw + 70
    bw, gap, hmax = 26, 10, 170
    base = top + gh
    mx = max(W)
    for w in range(n + 1):
        x = gx + w * (bw + gap)
        h = hmax * W[w] / mx
        cls = "bar-hi" if w == d else "bar"
        if W[w]:
            out.append('<rect class="%s" x="%d" y="%.1f" width="%d" height="%.1f" rx="2"><title>peso %d: %d palabras</title></rect>'
                       % (cls, x, base - h, bw, h, w, W[w]))
        out.append('<text class="tiny" x="%.1f" y="%.1f" text-anchor="middle">%d</text>'
                   % (x + bw / 2, base - h - 4, W[w]))
        out.append('<text class="tiny" x="%.1f" y="%d" text-anchor="middle">%d</text>'
                   % (x + bw / 2, base + 14, w))
    xe = gx + (n + 1) * (bw + gap) - gap
    out.append('<line class="axis" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (gx - 6, base, xe + 6, base))
    out.append('<text class="tiny muted" x="%.1f" y="%d" text-anchor="middle">peso w</text>' % ((gx + xe) / 2, base + 30))
    out.append('<text class="tiny muted" transform="translate(%d,%.1f) rotate(-90)" text-anchor="middle">palabras del código</text>'
               % (gx - 18, base - hmax / 2))
    out.append('<text class="figlab" x="%.1f" y="%d" text-anchor="middle">Distribución de pesos (d = %d)</text>'
               % ((gx + xe) / 2, ly + 46, d))
    W_total = xe + 20
    H_total = ly + 58
    return ('<svg class="svgfig mapa" viewBox="0 0 %d %d" role="img" '
            'aria-label="Mapa de distancias y distribución de pesos">%s</svg>'
            % (W_total, H_total, "\n".join(out)))


@lru_cache(maxsize=None)
def figura(nombre):
    """nombre: 'v4_3', 'v6_1', 'v7_5', ..."""
    esp, k = nombre.split("_")
    k = int(k)
    if esp == "v4":
        return hipercubo_svg(CASOS_V4[k - 1], ident="hc%d" % k)
    if esp == "v6":
        return mapa_svg(CASOS_V6[k - 1], 6)
    if esp == "v7":
        return mapa_svg(CASOS_V7[k - 1], 7)
    raise KeyError(nombre)


# ---------------------------------------------------------------------------
# Tablas de los capítulos 4, 6 y 7
# ---------------------------------------------------------------------------
H63 = ["011100", "101010", "110001"]
H7 = ["1101100", "1011010", "0111001"]
G7 = ["1000110", "0100101", "0010011", "0001111"]
G8 = ["10001101", "01001011", "00100111", "00011110"]


def sindrome(H, v):
    return "".join(str(sum(int(a) * b for a, b in zip(h, v)) % 2) for h in H)


def columnas(H):
    return ["".join(h[j] for h in H) for j in range(len(H[0]))]


def tab4_sindromes():
    sinds = ["000", "001", "010", "011", "100", "101", "110", "111"]
    lideres = []
    nota = ""
    for s in sinds:
        vs = [v for v in itertools.product([0, 1], repeat=6) if sindrome(H63, v) == s]
        mw = min(peso(v) for v in vs)
        L = sorted(s2(v) for v in vs if peso(v) == mw)
        if len(L) > 1:
            lideres.append(L[0] + "*")
            nota = "* líder no único: también " + " y ".join(L[1:])
        else:
            lideres.append(L[0])
    h = ['<div class="table-wrap"><table class="t-compact mono-cells">',
         "<tr><th>síndrome</th>" + "".join("<td>%s</td>" % s for s in sinds) + "</tr>",
         "<tr><th>líder</th>" + "".join("<td>%s</td>" % l for l in lideres) + "</tr>",
         "</table></div>", '<p class="tnote">%s</p>' % nota]
    return "\n".join(h)


def tab6_ecuaciones():
    cols = columnas(H7)
    filas = [("$E_1:\\ c_1+c_2+c_4+c_5=0$", "1, 2, 4, 5", H7[0]),
             ("$E_2:\\ c_1+c_3+c_4+c_6=0$", "1, 3, 4, 6", H7[1]),
             ("$E_3:\\ c_2+c_3+c_4+c_7=0$", "2, 3, 4, 7", H7[2])]
    h = ['<div class="table-wrap"><table>',
         "<thead><tr><th></th><th></th>" + "".join("<th>$c_%d$</th>" % (j + 1) for j in range(7)) + "</tr>",
         "<tr><th>Ecuación</th><th>Posiciones que revisa</th>"
         + "".join("<th>$%s$</th>" % x for x in ["u_1", "u_2", "u_3", "u_4", "p_1", "p_2", "p_3"])
         + "</tr></thead><tbody>"]
    for eq, pos, fila in filas:
        h.append("<tr><td>%s</td><td>%s</td>" % (eq, pos)
                 + "".join('<td class="c">%s</td>' % ("●" if b == "1" else "") for b in fila) + "</tr>")
    h.append('<tr class="sep"><td colspan="2">Columna $h_j$ (binario)</td>'
             + "".join('<td class="c mono">%s</td>' % c for c in cols) + "</tr>")
    h.append('<tr><td colspan="2">Columna $h_j$ (decimal)</td>'
             + "".join('<td class="c">%d</td>' % int(c, 2) for c in cols) + "</tr>")
    h.append('<tr><td colspan="2">Ecuaciones que lo vigilan</td>'
             + "".join('<td class="c">%d</td>' % c.count("1") for c in cols) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)


def tab6_part():
    C7 = [codificar(u, G7) for u in MENSAJES4]
    cols = columnas(H7)
    h = ['<div class="table-wrap"><table class="t-array">',
         "<thead><tr><th>Síndrome $s$</th><th>Líder $e$</th>"
         "<th>Las 16 palabras de la clase $e+C$</th></tr></thead><tbody>"]
    for s in ["000", "110", "101", "011", "111", "100", "010", "001"]:
        lider = [v for v in itertools.product([0, 1], repeat=7)
                 if peso(v) <= 1 and sindrome(H7, v) == s][0]
        ws = [s2(add(lider, c)) for c in C7]
        etiqueta = s if s == "000" else "%s ($h_{%d}$)" % (s, cols.index(s) + 1)
        h.append('<tr%s><td class="mono">%s</td><td class="mono">%s</td><td class="words">%s</td></tr>'
                 % (' class="row-code"' if s == "000" else "", etiqueta, s2(lider),
                    "".join("<span>%s</span>" % w for w in ws)))
    h.append("</tbody></table></div>")
    return "\n".join(h)


def _sy8(y):
    return sindrome(H7, y[:7]), sum(y) % 2


@lru_cache(maxsize=None)
def _clases8():
    C8 = [codificar(u, G8) for u in MENSAJES4]
    cols = columnas(H7)
    clases = {}
    for v in itertools.product([0, 1], repeat=8):
        clases.setdefault(_sy8(v), []).append(v)
    orden = ([("000", 0)] + [(c, 1) for c in cols] + [("000", 1)]
             + [(s, 0) for s in ["001", "010", "011", "100", "101", "110", "111"]])
    return C8, clases, orden


def tab7_array():
    C8, clases, orden = _clases8()
    h = ['<div class="table-wrap"><table class="t-array">',
         "<thead><tr><th>$s$</th><th>$\\sigma$</th><th>Representante</th><th>Tipo</th>"
         "<th>Las 16 palabras de la clase</th></tr></thead><tbody>"]
    for key in orden:
        vs = clases[key]
        mw = min(peso(v) for v in vs)
        lider = [v for v in vs if peso(v) == mw][0]
        ws = [s2(add(lider, c)) for c in C8]
        if key == ("000", 0):
            tipo = "código $C$"
        elif mw == 1:
            tipo = "1 error (bit %d)" % (lider.index(1) + 1)
        else:
            tipo = "error doble"
        cls = ' class="row-code"' if key == ("000", 0) else (' class="row-double"' if mw == 2 else "")
        h.append('<tr%s><td class="mono">%s</td><td>%d</td><td class="mono">%s</td><td>%s</td><td class="words">%s</td></tr>'
                 % (cls, key[0], key[1], s2(lider), tipo, "".join("<span>%s</span>" % w for w in ws)))
    h.append("</tbody></table></div>")
    return "\n".join(h)


def tab7_dobles():
    C8, clases, orden = _clases8()
    h = ['<div class="table-wrap"><table class="t-compact">',
         "<thead><tr><th>$s$</th><th>$\\sigma$</th><th colspan=\"4\">Los cuatro vectores de peso 2 de la clase</th></tr></thead><tbody>"]
    for key in orden:
        vs = clases[key]
        mw = min(peso(v) for v in vs)
        if mw != 2:
            continue
        cel = []
        for v in [v for v in vs if peso(v) == 2]:
            idx = [j + 1 for j in range(8) if v[j]]
            cel.append('<td><span class="mono">%s</span> $(%d,%d)$</td>' % (s2(v), idx[0], idx[1]))
        h.append('<tr><td class="mono">%s</td><td>0</td>%s</tr>' % (key[0], "".join(cel)))
    h.append("</tbody></table></div>")
    return "\n".join(h)


def _dec8(y):
    cols = columnas(H7)
    s, sg = _sy8(y)
    if s == "000" and sg == 0:
        return "acc", y
    if sg == 1:
        j = 7 if s == "000" else cols.index(s)
        return "corr", add(y, tuple(1 if i == j else 0 for i in range(8)))
    return "det", None


def _dec7(y):
    cols = columnas(H7)
    s = sindrome(H7, y)
    if s == "000":
        return "acc", y
    j = cols.index(s)
    return "corr", add(y, tuple(1 if i == j else 0 for i in range(7)))


@lru_cache(maxsize=None)
def clasificacion(n):
    """Clasifica los 2^n patrones de error por peso y resultado."""
    dec = _dec8 if n == 8 else _dec7
    zero = tuple([0] * n)
    tab = {}
    for e in itertools.product([0, 1], repeat=n):
        kind, ch = dec(e)
        if kind == "det":
            o = "detectado"
        elif ch == zero:
            o = "correcto"
        elif kind == "acc":
            o = "no detectado"
        else:
            o = "corrige mal"
        tab.setdefault(sum(e), {}).setdefault(o, 0)
        tab[sum(e)][o] += 1
    return tab


def probabilidades(n, p):
    P = {"correcto": 0.0, "detectado": 0.0, "falla": 0.0}
    for w, d in clasificacion(n).items():
        for o, c in d.items():
            k = "falla" if o in ("corrige mal", "no detectado") else o
            P[k] += c * p ** w * (1 - p) ** (n - w)
    return P


def _fmt(x):
    if x == 0:
        return "0"
    if x >= 0.01:
        return "%.6f" % x if x > 0.999 else "%.5f" % x
    m, e = ("%.2e" % x).split("e")
    return "%s\\times10^{%d}" % (m, int(e))


def tab7_prob():
    rows = []
    rows.append(("Término dominante", [
        ("decodifica bien", "\\approx1-21p^2", "\\approx1-28p^2"),
        ("detecta y pide reenvío", "0\\ \\text{(nunca detecta sin corregir)}", "\\approx28p^2"),
        ("fallo sin aviso", "\\approx21p^2", "\\approx56p^3")]))
    for p, lab in [(1e-2, "p=10^{-2}"), (1e-3, "p=10^{-3}")]:
        a, b = probabilidades(7, p), probabilidades(8, p)
        rows.append(("$%s$" % lab, [
            ("decodifica bien", _fmt(a["correcto"]), _fmt(b["correcto"])),
            ("detecta y pide reenvío", "0", _fmt(b["detectado"])),
            ("fallo sin aviso", _fmt(a["falla"]), _fmt(b["falla"]))]))
    h = ['<div class="table-wrap"><table>',
         "<thead><tr><th></th><th></th><th>$[7,4,3]$</th><th>$[8,4,4]$</th></tr></thead><tbody>"]
    for grupo, filas in rows:
        for i, (q, x, y) in enumerate(filas):
            g = '<td rowspan="3" class="grp">%s</td>' % grupo if i == 0 else ""
            h.append('<tr%s>%s<td>%s</td><td>$%s$</td><td>$%s$</td></tr>'
                     % (' class="sep"' if i == 0 else "", g, q, x, y))
    h.append("</tbody></table></div>")
    return "\n".join(h)


def tab7_ejemplos():
    cols = columnas(H7)
    c = vec("01010101")
    ejemplos = [("Sin error", ""), ("Error en información (bit 3)", "3"),
                ("Error en paridad de Hamming (bit 6)", "6"), ("Error en el bit 8", "8"),
                ("Errores dobles (bits 1 y 5)", "15"), ("Errores dobles (bits 4 y 8)", "48"),
                ("Triple error (bits 1, 2 y 3)", "123"),
                ("Cuatro errores (bits 1, 5, 6 y 8)", "1568")]
    ecs = [("s_1", [1, 2, 4, 5]), ("s_2", [1, 3, 4, 6]), ("s_3", [2, 3, 4, 7])]
    out = ['<div class="ex-grid">']
    for k, (nombre, b) in enumerate(ejemplos, 1):
        e = tuple(1 if str(i + 1) in b else 0 for i in range(8))
        y = add(c, e)
        filas, s = [], ""
        for nm, idx in ecs:
            vals = [y[i - 1] for i in idx]
            v = sum(vals) % 2
            s += str(v)
            filas.append("<tr><td>$%s$</td><td>$%s$</td><td>$%s=%d$</td></tr>"
                         % (nm, "+".join("y_%d" % i for i in idx), "+".join(map(str, vals)), v))
        sg = sum(y) % 2
        filas.append("<tr><td>$\\sigma$</td><td>$y_1+\\dots+y_8$</td><td>$\\mathrm{w}(y)=%d\\Rightarrow\\sigma=%d$</td></tr>"
                     % (sum(y), sg))
        estado = "ok"
        if s == "000" and sg == 0:
            diag, ch = "$(s,\\sigma)=(000,0)$: se acepta $y$.", y
        elif sg == 1:
            j = 8 if s == "000" else cols.index(s) + 1
            ch = add(y, tuple(1 if i == j - 1 else 0 for i in range(8)))
            diag = "$(s,\\sigma)=(%s,1)$: %sse corrige el bit %d." % (
                s, "" if s == "000" else "$s=h_{%d}$, " % j, j)
        else:
            diag, ch = "$(s,\\sigma)=(%s,0)$: error doble; se detecta y no se corrige." % s, None
            estado = "warn"
        if ch is None:
            res = "Se pide reenvío: no se entrega un dato falso."
        elif ch == c:
            res = "Resultado correcto: $\\hat c=%s$." % s2(ch) if b else "Resultado correcto."
        else:
            res = "Resultado <strong>equivocado</strong>: $\\hat c=%s\\neq c$." % s2(ch)
            estado = "bad"
        if nombre.startswith("Cuatro"):
            res += " El error $e=%s$ es una palabra del código: no se detecta." % s2(e)
        if nombre.startswith("Triple"):
            res += " Tres errores parecen uno solo."
        out.append('<div class="ex-card %s"><div class="ex-title">Ejemplo %d. %s</div>'
                   '<p class="mono-line">$e=\\texttt{%s}$, &nbsp; $y=c+e=\\texttt{%s}$</p>'
                   '<table class="t-mini">%s</table><p>%s %s</p></div>'
                   % (estado, k, nombre, s2(e), s2(y), "".join(filas), diag, res))
    out.append("</div>")
    return "\n".join(out)


TABLAS = {
    "tab4_sindromes": tab4_sindromes,
    "tab6_ecuaciones": tab6_ecuaciones,
    "tab6_part": tab6_part,
    "tab7_array": tab7_array,
    "tab7_dobles": tab7_dobles,
    "tab7_prob": tab7_prob,
    "tab7_ejemplos": tab7_ejemplos,
}
RAW = {"leyenda_hipercubo": leyenda_hipercubo, "leyenda_mapa": leyenda_mapa}


@lru_cache(maxsize=None)
def tabla(nombre):
    return TABLAS[nombre]()


def datos_clasificacion_js():
    """Conteos por peso para la calculadora de probabilidades (JS)."""
    import json
    out = {}
    for n in (7, 8):
        out[n] = {str(w): d for w, d in clasificacion(n).items()}
    return json.dumps(out)
