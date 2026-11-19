"""
Bloques interactivos de cada capítulo (HTML). La lógica vive en static/js/site.js.
Cada bloque trae su título y una descripción de qué hace y cómo usarlo.
"""
from figuras_codigos import hipercubo_svg, datos_clasificacion_js


def _lab(icono, titulo, descripcion, cuerpo, ident):
    return ('<div class="lab" id="%s"><div class="lab-head"><div class="lab-ico">%s</div><div>'
            '<div class="k">Laboratorio interactivo</div><h4>%s</h4><p>%s</p></div></div>'
            '<div class="lab-body">%s</div></div>' % (ident, icono, titulo, descripcion, cuerpo))


LABS = {}

LABS[0] = _lab(
    "⇄", "Calculadora de peso y distancia de Hamming",
    "Escribe dos palabras binarias de la misma longitud. La calculadora marca en naranja los bits en que difieren, "
    "calcula los pesos, la suma $x+y$ y la distancia $d(x,y)=\\mathrm{w}(x+y)$. Debajo, mueve el control para ver "
    "cuántos errores detecta y corrige un código con distancia mínima $d$.",
    """<div class="lab-row"><label>x <input type="text" class="mono" id="hd-x" value="1011010" size="14"></label>
<label>y <input type="text" class="mono" id="hd-y" value="1110011" size="14"></label>
<button class="btn" id="hd-go">Comparar</button></div>
<div class="out" id="hd-out"></div>
<div class="lab-row" style="margin-top:14px"><label>Distancia mínima d = <span id="hd-dv">3</span></label>
<input type="range" id="hd-d" min="1" max="9" value="3"></div>
<div class="out" id="hd-dout"></div>""", "lab0")

LABS[1] = _lab(
    "⚙", "Generador de un código lineal a partir de $G$",
    "Escribe las filas de una matriz generadora $G$ (una fila por renglón, sólo 0 y 1). El laboratorio forma las $2^k$ "
    "combinaciones $uG$, calcula sus pesos y la distancia mínima, dice cuántos errores detecta y corrige y, si $G$ está "
    "en forma estándar $(I_k\\mid A)$, construye $H=(A^{T}\\mid I_{n-k})$.",
    """<div class="grid2"><div><label>Filas de G</label><br><textarea id="gen-G">10110
01011</textarea><div class="lab-row" style="margin-top:8px"><button class="btn" id="gen-go">Generar código</button>
<button class="btn alt" data-fill="gen-G" data-val="100110&#10;010101&#10;001011">Ejemplo [6,3,3]</button>
<button class="btn alt" data-fill="gen-G" data-val="101&#10;011">Paridad [3,2,2]</button></div></div>
<div class="out" id="gen-out"></div></div>""", "lab1")

LABS[2] = _lab(
    "⊥", "Calculadora del código dual",
    "Escribe una matriz generadora. Se calcula el código $C$, su dual $C^{\\perp}$ (todas las palabras ortogonales a $C$), "
    "la intersección $C\\cap C^{\\perp}$ y se comprueba $\\dim C+\\dim C^{\\perp}=n$. También indica si el código es "
    "autoortogonal ($C\\subseteq C^{\\perp}$) o autodual ($C=C^{\\perp}$).",
    """<div class="grid2"><div><label>Filas de G</label><br><textarea id="dual-G">1010
0101</textarea><div class="lab-row" style="margin-top:8px"><button class="btn" id="dual-go">Calcular dual</button>
<button class="btn alt" data-fill="dual-G" data-val="10001101&#10;01001011&#10;00100111&#10;00011110">Hamming extendido</button>
<button class="btn alt" data-fill="dual-G" data-val="1000110&#10;0100101&#10;0010011&#10;0001111">Hamming [7,4]</button></div></div>
<div class="out" id="dual-out"></div></div>""", "lab2")

LABS[3] = _lab(
    "◇", "Hipercubo interactivo de $V_4$",
    "Elige uno de los seis códigos y haz clic en cualquier vértice: verás si es palabra del código, a qué distancia queda "
    "del código y cuáles son las palabras más cercanas (contorno verde). El botón «Simular un error» toma una palabra "
    "del código al azar, cambia un bit al azar y marca en naranja la arista recorrida: así se ve cuándo el error se "
    "detecta y cuándo cae en otra palabra del código.",
    """<div class="lab-row"><label>Código <select id="hc-case">
<option value="0">1 · Paridad [4,3,2]</option><option value="1">2 · Paridad parcial [4,3,1]</option>
<option value="2">3 · Repetición [4,2,2]</option><option value="3">4 · Bits duplicados [4,2,2]</option>
<option value="4">5 · Pesos 2 y 3 [4,2,2]</option><option value="5">6 · Un bit sin protección [4,2,1]</option></select></label>
<button class="btn" id="hc-err">Simular un error</button></div>
<div class="fig">%s</div><div class="out" id="hc-out"></div>""" % hipercubo_svg(None, ident="hcLive").replace('class="svgfig hc"', 'class="svgfig hc live"'),
    "lab3")

LABS[4] = _lab(
    "⌁", "Decodificador por síndrome del Hamming acortado $[6,3,3]$",
    "Escribe un mensaje de 3 bits y pulsa «Codificar». Después haz clic en los bits para dañarlos (se marcan en rojo). "
    "El decodificador calcula el síndrome $s=Hy^{T}$, busca su líder en la tabla y corrige. Prueba con uno y con dos "
    "errores: con dos, el síndrome puede ser $111$ (se detecta) o una columna de $H$ (corrige mal).",
    """<div class="lab-row"><label>Mensaje u <input type="text" class="mono" id="sd-u" value="101" size="5"></label>
<button class="btn" id="sd-enc">Codificar</button><span class="hint">H = (Aᵀ | I₃) con columnas 011, 101, 110, 100, 010, 001</span></div>
<div class="lab-row"><span class="bits" id="sd-bits"></span></div><div class="out" id="sd-out"></div>""", "lab4")

LABS[5] = _lab(
    "№", "Laboratorio de Hamming en orden binario: el síndrome es la posición",
    "Con $H$ cuyas columnas son los números 1 a 7 en binario, los bits de paridad quedan en las posiciones 1, 2 y 4 "
    "(borde punteado). Escribe 4 bits de datos, codifica y luego haz clic en cualquier posición para introducir un error: "
    "el síndrome, leído en binario, señala exactamente la posición dañada.",
    """<div class="lab-row"><label>Datos d₁d₂d₃d₄ <input type="text" class="mono" id="hb-u" value="1011" size="6"></label>
<button class="btn" id="hb-enc">Codificar</button><button class="btn alt" id="hb-rand">Error al azar</button></div>
<div class="lab-row"><span class="bits" id="hb-bits"></span></div><div class="out" id="hb-out"></div>""", "lab5")

LABS[6] = _lab(
    "✓", "Las tres ecuaciones de paridad en acción ($[7,4,3]$ en forma estándar)",
    "Codifica un mensaje con $G=(I_4\\mid A)$ y daña bits con un clic. Cada ecuación $E_1$, $E_2$, $E_3$ se marca en verde "
    "si se cumple y en rojo si falla; el patrón de fallas es el síndrome, que coincide con una columna $h_j$ de $H$. "
    "El decodificador cambia ese bit y recupera el mensaje (o se equivoca si hubo más de un error).",
    """<div class="lab-row"><label>Mensaje u <input type="text" class="mono" id="hs-u" value="1011" size="6"></label>
<button class="btn" id="hs-enc">Codificar</button></div>
<div class="lab-row"><span class="bits" id="hs-bits"></span></div><div class="out" id="hs-out"></div>""", "lab6")

LABS[7] = _lab(
    "⛨", "Laboratorio SECDED y calculadora de probabilidades",
    "Arriba: codifica un mensaje en el $[8,4,4]$, daña bits con un clic y observa el par $(s,\\sigma)$ y la casilla de la "
    "tabla 7.2 que usa el decodificador. Abajo: mueve la probabilidad de error por bit $p$ y compara, con cálculo exacto "
    "sobre todos los patrones de error, cuántas veces cada código acierta, detecta o falla sin aviso.",
    """<div class="lab-row"><label>Mensaje u <input type="text" class="mono" id="sc-u" value="0101" size="6"></label>
<button class="btn" id="sc-enc">Codificar</button></div>
<div class="lab-row"><span class="bits" id="sc-bits"></span></div>
<div class="grid2"><div class="out" id="sc-out"></div>
<div class="out"><table class="res secded" id="sc-tab"><tr><th></th><th>σ = 0</th><th>σ = 1</th></tr>
<tr><th>s = 0</th><td id="sc-00">sin error</td><td id="sc-01">error en bit 8</td></tr>
<tr><th>s ≠ 0</th><td id="sc-10">dos errores: detectar</td><td id="sc-11">un error: corregir</td></tr></table></div></div>
<div class="lab-row" style="margin-top:16px"><label>p = <span id="pr-pv"></span></label><input type="range" id="pr-p" min="-4" max="-0.7" step="0.05" value="-2"></div>
<div class="out" id="pr-out"></div>
<script>window.CLASIF = %s;</script>""" % datos_clasificacion_js(), "lab7")

LABS[8] = _lab(
    "📏", "Detector y corrector de la recta",
    "Elige un reloj primo (o números normales), escribe la lista de valores recibidos para $x=1,2,\\dots$ (usa «?» para un "
    "hueco) y pulsa «Analizar». Se muestran los saltos, el paso más repetido y la recta que coincide con más valores; "
    "los valores que no encajan se marcan como errores y se corrigen. Si hay empate entre rectas, el laboratorio avisa "
    "que no se puede decidir (como en el reto 4).",
    """<div class="lab-row"><label>Reloj <select id="rs-p"><option value="0">números normales</option><option>7</option><option>11</option>
<option selected>13</option><option>17</option><option>19</option><option>23</option></select></label>
<label>Valores <input type="text" class="mono" id="rs-y" value="12, 8, 9, 1, 6, 11" size="26"></label>
<button class="btn" id="rs-go">Analizar</button></div>
<div class="lab-row"><label>Codificar (a, b) = <input type="text" class="mono" id="rs-ab" value="4, 9" size="6"></label>
<label>n = <input type="number" id="rs-n" value="6" min="3" max="12" style="width:64px"></label>
<button class="btn alt" id="rs-enc">Generar lista</button></div>
<div class="out" id="rs-out"></div>""", "lab8")

LABS[9] = _lab(
    "◎", "SVD en vivo: del círculo a la elipse",
    "Cambia las entradas de una matriz $2\\times2$. La figura se redibuja al instante: el círculo unitario con $v_1,v_2$ "
    "(izquierda) se transforma en la elipse $A\\cdot$círculo con semiejes $\\sigma_1u_1$ y $\\sigma_2u_2$ (derecha). "
    "Debajo, el control $k$ reconstruye la imagen de prueba con los primeros $k$ valores singulares y reporta el error "
    "relativo y el porcentaje de datos que se guardan.",
    """<div class="lab-row"><label>A =</label>
<input type="number" step="0.1" id="sv-a" value="1.4" style="width:72px"><input type="number" step="0.1" id="sv-b" value="0.3" style="width:72px">
<input type="number" step="0.1" id="sv-c" value="1.2" style="width:72px"><input type="number" step="0.1" id="sv-d" value="1.5" style="width:72px">
<span class="hint">(a b ; c d)</span></div>
<div class="grid2"><svg class="live" id="sv-svg" viewBox="0 0 520 260"></svg><div class="out" id="sv-out"></div></div>
<div class="lab-row" style="margin-top:14px"><label>k = <span id="sv-kv">10</span></label><input type="range" id="sv-k" min="1" max="128" value="10">
<canvas id="sv-canvas" width="128" height="128" style="width:160px;height:160px;border-radius:8px;border:1px solid var(--line);image-rendering:pixelated"></canvas>
<div class="out" id="sv-kout" style="min-width:220px"></div></div>""", "lab9")

LABS[10] = _lab(
    "✦", "PCA en vivo sobre una nube de puntos",
    "Ajusta la inclinación, la dispersión a lo largo y a lo ancho, y el número de puntos. El laboratorio recalcula la "
    "media, la matriz de covarianza y sus autovectores, dibuja $PC1$ y $PC2$ con los residuos sobre $PC1$ y reporta el "
    "porcentaje de varianza explicada. Activa «valor atípico» para ver lo sensible que es el PCA clásico. Abajo, la "
    "calculadora de PVE acepta cualquier lista de autovalores.",
    """<div class="lab-row"><label>Inclinación <input type="range" id="pc-ang" min="-80" max="80" value="30"></label>
<label>σ largo <input type="range" id="pc-s1" min="5" max="30" value="20"></label>
<label>σ ancho <input type="range" id="pc-s2" min="1" max="20" value="6"></label>
<label>n <input type="range" id="pc-n" min="10" max="200" value="60"></label>
<label><input type="checkbox" id="pc-out"> valor atípico</label></div>
<div class="grid2"><svg class="live" id="pc-svg" viewBox="0 0 520 330"></svg><div class="out" id="pc-res"></div></div>
<div class="lab-row" style="margin-top:14px"><label>Autovalores <input type="text" class="mono" id="pve-l" value="12, 4, 1.5, 0.5" size="22"></label>
<label>Umbral % <input type="number" id="pve-t" value="90" style="width:70px"></label><button class="btn" id="pve-go">Calcular PVE</button></div>
<div class="out" id="pve-out"></div>""", "lab10")

LABS[11] = _lab(
    "⊕", "Calculadora de los cuatro subespacios",
    "Escribe una matriz (una fila por renglón, números separados por espacios o comas; se aceptan fracciones como 1/2) "
    "y, si quieres, un vector $b$. Se escalona la matriz con aritmética exacta y se obtienen el rango, bases de "
    "$C(A^{T})$, $N(A)$, $C(A)$ y $N(A^{T})$ y sus dimensiones. Con $b$, aplica la alternativa de Fredholm: dice si "
    "$Ax=b$ tiene solución y, si no, muestra el certificado $y$ con $A^{T}y=0$ y $y^{T}b\\ne0$.",
    """<div class="grid2"><div><label>Matriz A</label><br><textarea id="fs-A">1 0 1
0 1 1</textarea>
<div class="lab-row" style="margin-top:8px"><label>b = <input type="text" class="mono" id="fs-b" value="2, 3" size="14"></label></div>
<div class="lab-row"><button class="btn" id="fs-go">Analizar</button>
<button class="btn alt" data-fill="fs-A" data-val="1 2 3&#10;2 4 6&#10;1 1 1">Ejemplo de rango 2</button></div></div>
<div class="out" id="fs-out"></div></div>""", "lab11")

LABS[12] = _lab(
    "🔢", "Calculadora de $\\mathbb{F}_{2^n}$ y simulador de LFSR",
    "Elige el polinomio que define el campo. Escribe dos elementos en hexadecimal y verás $a+b$ (XOR), $a\\cdot b$ con los "
    "pasos del campesino ruso, $a^{-1}$ y los logaritmos. El ciclo dibuja las potencias del elemento $g$ que elijas y "
    "dice si es primitivo; el LFSR muestra la secuencia de estados y su periodo.",
    """<div class="lab-row"><label>Polinomio <select id="gf-p">
<option value="7,2">x²+x+1 (𝔽₄)</option><option value="11,3">x³+x+1 (𝔽₈)</option><option value="13,3">x³+x²+1 (𝔽₈)</option>
<option value="19,4" selected>x⁴+x+1 (𝔽₁₆)</option><option value="25,4">x⁴+x³+1 (𝔽₁₆)</option><option value="31,4">x⁴+x³+x²+x+1 (𝔽₁₆)</option>
<option value="283,8">x⁸+x⁴+x³+x+1 · AES (𝔽₂₅₆)</option><option value="285,8">x⁸+x⁴+x³+x²+1 · QR (𝔽₂₅₆)</option></select></label>
<label>a = <input type="text" class="mono" id="gf-a" value="B" size="4"></label>
<label>b = <input type="text" class="mono" id="gf-b" value="D" size="4"></label>
<label>g = <input type="text" class="mono" id="gf-g" value="2" size="4"></label>
<button class="btn" id="gf-go">Calcular</button></div>
<div class="grid2"><div class="out" id="gf-out"></div><svg class="live" id="gf-svg" viewBox="0 0 420 420"></svg></div>
<div class="out" id="gf-lfsr" style="margin-top:12px"></div>""", "lab12")


def lab(n):
    return LABS.get(n, "")
