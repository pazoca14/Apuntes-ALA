/* =====================================================================
   Apuntes de Álgebra Lineal Avanzada — interactividad del sitio
   ===================================================================== */
(function () {
"use strict";
const $ = (id) => document.getElementById(id);
const fmt = (x, d = 4) => (Math.abs(x) < 1e-12 ? 0 : Number(x.toFixed(d)));
function typeset(el) {
  if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise(el ? [el] : undefined).catch(() => {});
}
function on(id, ev, fn) { const el = $(id); if (el) el.addEventListener(ev, fn); }

/* ------------------------------------------------------------------ */
/* Interfaz general                                                    */
/* ------------------------------------------------------------------ */
function initUI() {
  // tema
  const root = document.documentElement;
  let saved = null;
  try { saved = localStorage.getItem("ala-theme"); } catch (e) {}
  if (saved) root.setAttribute("data-theme", saved);
  on("themeBtn", "click", () => {
    const t = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("ala-theme", t); } catch (e) {}
  });
  // menú móvil
  on("menuBtn", "click", () => document.body.classList.toggle("menu-open"));
  document.querySelectorAll("nav#sidebar a").forEach((a) =>
    a.addEventListener("click", () => document.body.classList.remove("menu-open")));
  // búsqueda en índice
  on("navSearch", "input", (e) => {
    const q = e.target.value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    document.querySelectorAll("nav#sidebar li").forEach((li) => {
      const t = li.textContent.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      li.classList.toggle("hidden", q && !t.includes(q));
    });
  });
  // progreso, volver arriba y capítulo activo
  const links = Array.from(document.querySelectorAll("nav#sidebar li a"));
  const secs = links.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  function onScroll() {
    const h = document.documentElement;
    const p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    $("progress").style.width = (100 * p) + "%";
    $("toTop").classList.toggle("show", h.scrollTop > 700);
    let cur = null;
    for (const s of secs) if (s.getBoundingClientRect().top < 140) cur = s.id;
    links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + cur));
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  on("toTop", "click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  // botones de ejemplo que rellenan un textarea
  document.querySelectorAll("[data-fill]").forEach((b) =>
    b.addEventListener("click", () => { $(b.dataset.fill).value = b.dataset.val.replace(/&#10;/g, "\n"); }));
  // abrir / cerrar todas las soluciones de un capítulo
  document.querySelectorAll(".sol-tools").forEach((box) => {
    const sec = box.closest("section");
    box.querySelector("[data-open]").addEventListener("click", () => sec.querySelectorAll("details.sol").forEach((d) => (d.open = true)));
    box.querySelector("[data-close]").addEventListener("click", () => sec.querySelectorAll("details.sol").forEach((d) => (d.open = false)));
  });
}

/* ------------------------------------------------------------------ */
/* Álgebra binaria                                                     */
/* ------------------------------------------------------------------ */
const xor = (a, b) => a.map((x, i) => x ^ b[i]);
const wt = (v) => v.reduce((s, x) => s + x, 0);
const str = (v) => v.join("");
const dot2 = (a, b) => a.reduce((s, x, i) => s ^ (x & b[i]), 0);
function parseBits(s) { s = s.replace(/\s/g, ""); return /^[01]+$/.test(s) ? s.split("").map(Number) : null; }
function parseRows(txt) {
  const rows = txt.split(/\n/).map((r) => r.trim()).filter((r) => r.length).map(parseBits);
  if (!rows.length || rows.some((r) => !r)) return { err: "Usa sólo 0 y 1, una fila por renglón." };
  const n = rows[0].length;
  if (rows.some((r) => r.length !== n)) return { err: "Todas las filas deben tener la misma longitud." };
  return { rows, n };
}
function rref2(rows) {
  const M = rows.map((r) => r.slice()); const n = M[0].length; const piv = []; let r = 0;
  for (let c = 0; c < n && r < M.length; c++) {
    let p = -1; for (let i = r; i < M.length; i++) if (M[i][c]) { p = i; break; }
    if (p < 0) continue;
    [M[r], M[p]] = [M[p], M[r]];
    for (let i = 0; i < M.length; i++) if (i !== r && M[i][c]) M[i] = xor(M[i], M[r]);
    piv.push(c); r++;
  }
  return { R: M.slice(0, r), piv };
}
function spanList(basis, n) {
  let S = [new Array(n).fill(0)];
  for (const b of basis) S = S.concat(S.map((s) => xor(s, b)));
  return S;
}
function allVectors(n) {
  const out = [];
  for (let i = 0; i < (1 << n); i++) out.push(i.toString(2).padStart(n, "0").split("").map(Number));
  return out;
}
function bitsHTML(v, opts = {}) {
  return '<span class="bits">' + v.map((b, i) => {
    let c = "bit ro" + (b ? " one" : "");
    if (opts.diff && opts.diff[i]) c += " diff";
    return '<span class="' + c + '">' + b + (opts.labels ? "<small>" + (i + 1) + "</small>" : "") + "</span>";
  }).join("") + "</span>";
}

/* ---------------- Capítulo 0 ---------------- */
function lab0() {
  if (!$("hd-go")) return;
  function run() {
    const x = parseBits($("hd-x").value), y = parseBits($("hd-y").value);
    const out = $("hd-out");
    if (!x || !y) { out.innerHTML = '<span class="pill bad">Escribe sólo ceros y unos.</span>'; return; }
    if (x.length !== y.length) { out.innerHTML = '<span class="pill bad">Las dos palabras deben tener la misma longitud.</span>'; return; }
    const s = xor(x, y), d = wt(s);
    out.innerHTML =
      '<div class="kv"><b>x</b><span>' + bitsHTML(x, { diff: s, labels: true }) + '</span>' +
      '<b>y</b><span>' + bitsHTML(y, { diff: s }) + '</span>' +
      '<b>x + y</b><span>' + bitsHTML(s) + '</span></div>' +
      '<p>$\\mathrm{w}(x)=' + wt(x) + '$, $\\mathrm{w}(y)=' + wt(y) + '$, y difieren en <strong>' + d +
      '</strong> posiciones: $d(x,y)=\\mathrm{w}(x+y)=' + d + '$.</p>';
    typeset(out);
  }
  function dist() {
    const d = +$("hd-d").value; $("hd-dv").textContent = d;
    const t = Math.floor((d - 1) / 2);
    const pares = [];
    for (let a = 0; a <= t; a++) { const b = d - 1 - a; if (b >= a && a > 0) pares.push("(" + a + "," + b + ")"); }
    $("hd-dout").innerHTML = '<div class="kv"><b>Detecta</b><span>hasta ' + (d - 1) + ' errores</span><b>Corrige</b><span>hasta ' + t +
      ' errores</span><b>Corrige t y detecta t′ a la vez</b><span>' + (pares.length ? pares.join(", ") + " (máximos)" : "no aplica") + "</span></div>";
  }
  on("hd-go", "click", run); on("hd-d", "input", dist); run(); dist();
}

/* ---------------- Capítulo 1 ---------------- */
function lab1() {
  if (!$("gen-go")) return;
  function run() {
    const out = $("gen-out"); const P = parseRows($("gen-G").value);
    if (P.err) { out.innerHTML = '<span class="pill bad">' + P.err + "</span>"; return; }
    if (P.n > 12 || P.rows.length > 8) { out.innerHTML = '<span class="pill bad">Usa a lo más 8 filas y 12 columnas.</span>'; return; }
    const { R } = rref2(P.rows); const k = R.length, n = P.n;
    const base = R.length === P.rows.length ? P.rows : R;
    let html = "";
    if (k < P.rows.length) html += '<p><span class="pill warn">Las filas no son independientes</span> Se usa una base con ' + k + " filas.</p>";
    const words = [];
    for (let i = 0; i < (1 << k); i++) {
      const u = i.toString(2).padStart(k, "0").split("").map(Number);
      let c = new Array(n).fill(0); u.forEach((b, j) => { if (b) c = xor(c, base[j]); });
      words.push([u, c]);
    }
    const nz = words.filter((w) => wt(w[1]) > 0).map((w) => wt(w[1]));
    const d = nz.length ? Math.min(...nz) : 0;
    html += "<p>Código $[" + n + "," + k + "," + d + "]$ con $2^{" + k + "}=" + words.length + "$ palabras. Detecta " +
      Math.max(d - 1, 0) + " y corrige " + Math.max(Math.floor((d - 1) / 2), 0) + " errores. Tasa $" + k + "/" + n + "$.</p>";
    html += '<table class="res"><tr><th>u</th><th>c = uG</th><th>w(c)</th></tr>' +
      words.slice(0, 64).map((w) => "<tr><td>" + str(w[0]) + "</td><td>" + str(w[1]) + "</td><td>" + wt(w[1]) + "</td></tr>").join("") + "</table>";
    // forma estándar
    const std = base.every((r, i) => r.slice(0, k).every((x, j) => x === (i === j ? 1 : 0)));
    if (std && k < n) {
      const A = base.map((r) => r.slice(k));
      const H = [];
      for (let i = 0; i < n - k; i++) { const row = A.map((a) => a[i]); for (let j = 0; j < n - k; j++) row.push(i === j ? 1 : 0); H.push(row); }
      html += "<p>Forma estándar: $H=(A^{T}\\mid I_{" + (n - k) + "})=\\begin{pmatrix}" + H.map((r) => r.join("&")).join("\\\\") + "\\end{pmatrix}$</p>";
    } else if (k < n) html += '<p class="hint">G no está en forma estándar $(I_k\\mid A)$; usa la calculadora del capítulo 2 para obtener una matriz de control.</p>';
    out.innerHTML = html; typeset(out);
  }
  on("gen-go", "click", run); run();
}

/* ---------------- Capítulo 2 ---------------- */
function lab2() {
  if (!$("dual-go")) return;
  function run() {
    const out = $("dual-out"); const P = parseRows($("dual-G").value);
    if (P.err) { out.innerHTML = '<span class="pill bad">' + P.err + "</span>"; return; }
    if (P.n > 12) { out.innerHTML = '<span class="pill bad">Usa a lo más 12 columnas.</span>'; return; }
    const n = P.n, { R } = rref2(P.rows), k = R.length;
    const C = spanList(R, n);
    const D = allVectors(n).filter((v) => R.every((r) => dot2(r, v) === 0));
    const keyC = new Set(C.map(str));
    const I = D.filter((v) => keyC.has(str(v)));
    const dmin = (S) => { const w = S.map(wt).filter((x) => x > 0); return w.length ? Math.min(...w) : "—"; };
    const auto = I.length === C.length, autod = auto && D.length === C.length;
    const list = (S) => S.length <= 32 ? "$\\{" + S.map(str).join(",") + "\\}$" : S.length + " palabras (se muestran las primeras 32): $\\{" + S.slice(0, 32).map(str).join(",") + ",\\dots\\}$";
    out.innerHTML =
      '<div class="kv"><b>C</b><span>$[' + n + "," + k + "," + dmin(C) + "]$, " + C.length + ' palabras</span>' +
      "<b>C<sup>⊥</sup></b><span>$[" + n + "," + (n - k) + "," + dmin(D) + "]$, " + D.length + " palabras</span>" +
      "<b>Comprobación</b><span>$\\dim C+\\dim C^{\\perp}=" + k + "+" + (n - k) + "=" + n + "$ y $\\#C\\cdot\\#C^{\\perp}=2^{" + n + "}$</span></div>" +
      "<p><strong>$C^{\\perp}$:</strong> " + list(D) + "</p><p><strong>$C\\cap C^{\\perp}$:</strong> " + list(I) + "</p>" +
      "<p>" + (autod ? '<span class="pill ok">Autodual: C = C⊥</span>' : auto ? '<span class="pill ok">Autoortogonal: C ⊆ C⊥</span>' :
        I.length > 1 ? '<span class="pill warn">C y C⊥ comparten palabras no nulas</span>' : '<span class="pill">C ∩ C⊥ = {0}</span>') + "</p>";
    typeset(out);
  }
  on("dual-go", "click", run); run();
}

/* ---------------- Capítulo 3 ---------------- */
const CASOS_V4 = [["1111"], ["1101"], ["1010", "0101"], ["1100", "0011"], ["1010", "1101"], ["0110", "0101"]];
function kernel(H, n) { const Hs = H.map(parseBits); return allVectors(n).filter((v) => Hs.every((h) => dot2(h, v) === 0)); }
function lab3() {
  const svg = $("hcLive"); if (!svg) return;
  let C = [], sel = null;
  function setCase() {
    C = kernel(CASOS_V4[+$("hc-case").value], 4).map(str);
    svg.querySelectorAll(".hc-node").forEach((g) => { g.classList.toggle("cw", C.includes(g.dataset.w)); g.classList.remove("sel", "near"); });
    svg.querySelectorAll("line").forEach((l) => { l.classList.remove("flash"); l.classList.toggle("redlive", C.includes(l.dataset.a) && C.includes(l.dataset.b)); });
    const d = Math.min(...C.filter((c) => c !== "0000").map((c) => wt(parseBits(c))));
    $("hc-out").innerHTML = "Código con " + C.length + " palabras: {" + C.join(", ") + "}. Distancia mínima d = " + d +
      (d >= 2 ? ': ningún error de un bit lleva de una palabra a otra.' : ': hay aristas rojas, así que algunos errores de un bit pasan inadvertidos.');
  }
  function pick(w, extra) {
    sel = w;
    const v = parseBits(w);
    const ds = C.map((c) => [c, wt(xor(v, parseBits(c)))]);
    const m = Math.min(...ds.map((x) => x[1]));
    const near = ds.filter((x) => x[1] === m).map((x) => x[0]);
    svg.querySelectorAll(".hc-node").forEach((g) => { g.classList.toggle("sel", g.dataset.w === w); g.classList.toggle("near", m > 0 && near.includes(g.dataset.w)); });
    let t = "<strong>" + w + "</strong> " + (m === 0 ? '<span class="pill ok">es palabra del código</span>' :
      'está a distancia <strong>' + m + "</strong> del código; palabras más cercanas: " + near.join(", ") +
      (near.length > 1 ? ' <span class="pill warn">empate: se detecta, pero no se sabe cuál corregir</span>' : ' <span class="pill ok">se corregiría a ' + near[0] + "</span>"));
    $("hc-out").innerHTML = (extra || "") + t;
  }
  svg.querySelectorAll(".hc-node").forEach((g) => g.addEventListener("click", () => {
    svg.querySelectorAll("line.flash").forEach((l) => l.classList.remove("flash")); pick(g.dataset.w);
  }));
  on("hc-case", "change", setCase);
  on("hc-err", "click", () => {
    const c = C[Math.floor(Math.random() * C.length)], i = Math.floor(Math.random() * 4);
    const y = c.split(""); y[i] = y[i] === "0" ? "1" : "0"; const ys = y.join("");
    svg.querySelectorAll("line").forEach((l) => l.classList.toggle("flash", (l.dataset.a === c && l.dataset.b === ys) || (l.dataset.a === ys && l.dataset.b === c)));
    const und = C.includes(ys);
    pick(ys, "Se envió <strong>" + c + "</strong> y se dañó el bit " + (i + 1) + ": se recibió <strong>" + ys + "</strong>. " +
      (und ? '<span class="pill bad">¡Error no detectado!</span> ' : '<span class="pill ok">Error detectado</span> ') + "<br>");
  });
  setCase();
}

/* ---------------- utilidades para laboratorios de bits ---------------- */
function bitBoard(container, n, onChange, opts = {}) {
  const st = { sent: new Array(n).fill(0), y: new Array(n).fill(0) };
  function draw(fix) {
    container.innerHTML = "";
    st.y.forEach((b, i) => {
      const s = document.createElement("span");
      s.className = "bit" + (b ? " one" : "") + (b !== st.sent[i] ? " flip" : "") + (fix === i ? " fix" : "") + (opts.par && opts.par.includes(i) ? " par" : "");
      s.innerHTML = b + "<small>" + (opts.labels ? opts.labels[i] : i + 1) + "</small>";
      s.title = "Clic para cambiar este bit";
      s.addEventListener("click", () => { st.y[i] ^= 1; update(); });
      container.appendChild(s);
    });
  }
  function update() { const fix = onChange(st); draw(fix); }
  st.set = (c) => { st.sent = c.slice(); st.y = c.slice(); update(); };
  st.flip = (i) => { st.y[i] ^= 1; update(); };
  return st;
}
const ROWS = (arr) => arr.map(parseBits);
function encodeG(u, G) { let c = new Array(G[0].length).fill(0); u.forEach((b, j) => { if (b) c = xor(c, G[j]); }); return c; }
function syndrome(H, y) { return H.map((h) => dot2(h, y)); }
function columnsOf(H) { return H[0].map((_, j) => H.map((h) => h[j])); }

/* ---------------- Capítulo 4 ---------------- */
function lab4() {
  if (!$("sd-enc")) return;
  const H = ROWS(["011100", "101010", "110001"]), G = ROWS(["100011", "010101", "001110"]);
  const all = allVectors(6);
  const board = bitBoard($("sd-bits"), 6, (st) => {
    const s = syndrome(H, st.y), ss = str(s);
    const cls = all.filter((v) => str(syndrome(H, v)) === ss);
    const mw = Math.min(...cls.map(wt)); const L = cls.filter((v) => wt(v) === mw);
    const errs = wt(xor(st.y, st.sent));
    let html = '<div class="kv"><b>Errores introducidos</b><span>' + errs + "</span><b>Síndrome s = Hyᵀ</b><span>" + ss + "</span>";
    let fix = null;
    if (ss === "000") html += "<b>Decisión</b><span>se acepta y</span></div>";
    else if (L.length === 1) {
      fix = L[0].indexOf(1); const ch = xor(st.y, L[0]);
      html += "<b>Líder</b><span>" + str(L[0]) + " (columna " + (fix + 1) + " de H)</span><b>Palabra decodificada</b><span>" + str(ch) +
        "</span><b>Mensaje</b><span>" + str(ch.slice(0, 3)) + "</span></div>" +
        (str(ch) === str(st.sent) ? '<span class="pill ok">Correcto</span>' : '<span class="pill bad">Corrigió mal: hubo más de un error</span>');
    } else html += "<b>Líderes</b><span>" + L.map(str).join(", ") + "</span></div><span class=\"pill warn\">Síndrome 111: error doble detectado, no se corrige</span>";
    if (ss === "000" && errs) html += '<span class="pill bad">El error es una palabra del código: no se detecta</span>';
    $("sd-out").innerHTML = html;
    return fix;
  });
  function enc() { const u = parseBits($("sd-u").value); if (!u || u.length !== 3) { $("sd-out").innerHTML = '<span class="pill bad">El mensaje debe tener 3 bits.</span>'; return; } board.set(encodeG(u, G)); }
  on("sd-enc", "click", enc); enc();
}

/* ---------------- Capítulo 5 ---------------- */
function lab5() {
  if (!$("hb-enc")) return;
  const H = ROWS(["0001111", "0110011", "1010101"]);
  const board = bitBoard($("hb-bits"), 7, (st) => {
    const s = syndrome(H, st.y), pos = parseInt(str(s), 2);
    let html = '<div class="kv"><b>Síndrome</b><span>' + str(s) + " = " + pos + " en binario</span>";
    let fix = null;
    if (!pos) html += "<b>Decisión</b><span>sin error detectado</span></div>";
    else {
      fix = pos - 1; const ch = st.y.slice(); ch[fix] ^= 1;
      html += "<b>Decisión</b><span>cambiar la posición " + pos + "</span><b>Datos (3,5,6,7)</b><span>" + [ch[2], ch[4], ch[5], ch[6]].join("") + "</span></div>" +
        (str(ch) === str(st.sent) ? '<span class="pill ok">Error corregido</span>' : '<span class="pill bad">Hubo dos o más errores: la corrección es equivocada</span>');
    }
    $("hb-out").innerHTML = html; return fix;
  }, { par: [0, 1, 3], labels: ["p₁", "p₂", "3", "p₄", "5", "6", "7"] });
  function enc() {
    const d = parseBits($("hb-u").value); if (!d || d.length !== 4) { $("hb-out").innerHTML = '<span class="pill bad">Escribe 4 bits.</span>'; return; }
    const c = [0, 0, d[0], 0, d[1], d[2], d[3]];
    c[0] = c[2] ^ c[4] ^ c[6]; c[1] = c[2] ^ c[5] ^ c[6]; c[3] = c[4] ^ c[5] ^ c[6];
    board.set(c);
  }
  on("hb-enc", "click", enc); on("hb-rand", "click", () => board.flip(Math.floor(Math.random() * 7))); enc();
}

/* ---------------- Capítulo 6 ---------------- */
const H7 = ROWS(["1101100", "1011010", "0111001"]);
const G7 = ROWS(["1000110", "0100101", "0010011", "0001111"]);
function lab6() {
  if (!$("hs-enc")) return;
  const cols = columnsOf(H7).map(str);
  const eqs = ["c₁+c₂+c₄+c₅", "c₁+c₃+c₄+c₆", "c₂+c₃+c₄+c₇"];
  const board = bitBoard($("hs-bits"), 7, (st) => {
    const s = syndrome(H7, st.y), ss = str(s);
    let html = '<div class="eqs">' + s.map((b, i) => '<span class="' + (b ? "bad" : "good") + '">E' + (i + 1) + ": " + eqs[i] + " = " + b + (b ? " ✗" : " ✓") + "</span>").join("") + "</div>";
    let fix = null;
    if (ss === "000") html += "<p>Síndrome 000: se acepta. Mensaje " + str(st.y.slice(0, 4)) + ".</p>";
    else {
      fix = cols.indexOf(ss); const ch = st.y.slice(); ch[fix] ^= 1;
      html += "<p>Síndrome " + ss + " = columna h<sub>" + (fix + 1) + "</sub>: se cambia el bit " + (fix + 1) + " → ĉ = " + str(ch) + ", mensaje <strong>" + str(ch.slice(0, 4)) + "</strong>. " +
        (str(ch) === str(st.sent) ? '<span class="pill ok">Correcto</span>' : '<span class="pill bad">Equivocado (más de un error)</span>') + "</p>";
    }
    $("hs-out").innerHTML = html; return fix;
  }, { par: [4, 5, 6], labels: ["u₁", "u₂", "u₃", "u₄", "p₁", "p₂", "p₃"] });
  function enc() { const u = parseBits($("hs-u").value); if (!u || u.length !== 4) { $("hs-out").innerHTML = '<span class="pill bad">Escribe 4 bits.</span>'; return; } board.set(encodeG(u, G7)); }
  on("hs-enc", "click", enc); enc();
}

/* ---------------- Capítulo 7 ---------------- */
function lab7() {
  if (!$("sc-enc")) return;
  const G8 = ROWS(["10001101", "01001011", "00100111", "00011110"]); const cols = columnsOf(H7).map(str);
  const board = bitBoard($("sc-bits"), 8, (st) => {
    const s = str(syndrome(H7, st.y.slice(0, 7))), sg = wt(st.y) % 2;
    ["sc-00", "sc-01", "sc-10", "sc-11"].forEach((id) => $(id).classList.remove("hl"));
    $("sc-" + (s === "000" ? "0" : "1") + sg).classList.add("hl");
    const errs = wt(xor(st.y, st.sent));
    let html = '<div class="kv"><b>Errores introducidos</b><span>' + errs + "</span><b>(s, σ)</b><span>(" + s + ", " + sg + ")</span>";
    let fix = null, res;
    if (s === "000" && sg === 0) { res = st.y; html += "<b>Decisión</b><span>aceptar</span>"; }
    else if (sg === 1) { fix = s === "000" ? 7 : cols.indexOf(s); res = st.y.slice(); res[fix] ^= 1; html += "<b>Decisión</b><span>corregir el bit " + (fix + 1) + "</span>"; }
    else { res = null; html += "<b>Decisión</b><span>error doble: detectar y pedir reenvío</span>"; }
    html += "</div>";
    if (res === null) html += '<span class="pill warn">No se entrega un dato falso</span>';
    else if (str(res) === str(st.sent)) html += '<span class="pill ok">Resultado correcto: ' + str(res) + "</span>";
    else html += '<span class="pill bad">Fallo sin aviso: ' + str(res) + "</span>";
    $("sc-out").innerHTML = html; return fix;
  }, { par: [4, 5, 6, 7], labels: ["u₁", "u₂", "u₃", "u₄", "p₁", "p₂", "p₃", "σ"] });
  function enc() { const u = parseBits($("sc-u").value); if (!u || u.length !== 4) { $("sc-out").innerHTML = '<span class="pill bad">Escribe 4 bits.</span>'; return; } board.set(encodeG(u, G8)); }
  on("sc-enc", "click", enc); enc();
  // probabilidades
  function prob() {
    const p = Math.pow(10, +$("pr-p").value);
    $("pr-pv").textContent = p < 0.01 ? p.toExponential(2) : p.toFixed(3);
    const calc = (n) => {
      const P = { ok: 0, det: 0, fail: 0 }; const T = window.CLASIF[n];
      for (const w in T) for (const o in T[w]) {
        const pr = T[w][o] * Math.pow(p, +w) * Math.pow(1 - p, n - +w);
        if (o === "correcto") P.ok += pr; else if (o === "detectado") P.det += pr; else P.fail += pr;
      }
      return P;
    };
    const a = calc(7), b = calc(8); const f = (x) => (x === 0 ? "0" : x < 1e-3 ? x.toExponential(2) : x.toFixed(5));
    const bar = (x, cls) => '<span style="display:inline-block;height:8px;border-radius:4px;vertical-align:middle;margin-left:6px;width:' + Math.max(2, 120 * Math.min(1, x / Math.max(a.fail, b.det, b.fail, 1e-12))) + 'px;background:var(' + cls + ')"></span>';
    $("pr-out").innerHTML = '<table class="res"><tr><th></th><th>[7,4,3]</th><th>[8,4,4]</th></tr>' +
      "<tr><th>decodifica bien</th><td>" + f(a.ok) + "</td><td>" + f(b.ok) + "</td></tr>" +
      "<tr><th>detecta y pide reenvío</th><td>0</td><td>" + f(b.det) + bar(b.det, "--d2") + "</td></tr>" +
      "<tr><th>fallo sin aviso</th><td>" + f(a.fail) + bar(a.fail, "--red") + "</td><td>" + f(b.fail) + bar(b.fail, "--red") + "</td></tr></table>" +
      '<p class="hint">El fallo sin aviso del [8,4,4] es ' + (a.fail / Math.max(b.fail, 1e-300)).toFixed(0) + " veces menor que el del [7,4,3] para este p.</p>";
  }
  on("pr-p", "input", prob); prob();
}

/* ---------------- Capítulo 8 ---------------- */
function modp(a, p) { return ((a % p) + p) % p; }
function invp(a, p) { a = modp(a, p); for (let x = 1; x < p; x++) if ((a * x) % p === 1) return x; return null; }
function lab8() {
  if (!$("rs-go")) return;
  function analizar() {
    const p = +$("rs-p").value; const raw = $("rs-y").value.split(/[,\s]+/).filter((s) => s.length);
    const y = raw.map((s) => (s === "?" || s === "□" ? null : Number(s)));
    const out = $("rs-out");
    if (y.some((v) => v !== null && !isFinite(v)) || y.length < 3) { out.innerHTML = '<span class="pill bad">Escribe al menos 3 valores (números o «?»).</span>'; return; }
    if (p && y.some((v) => v !== null && (v < 0 || v >= p || v % 1))) { out.innerHTML = '<span class="pill bad">En el reloj de ' + p + " horas los valores van de 0 a " + (p - 1) + ".</span>"; return; }
    const n = y.length; const X = y.map((_, i) => i + 1);
    const known = y.map((v, i) => [i, v]).filter((t) => t[1] !== null);
    const saltos = y.slice(1).map((v, i) => (v === null || y[i] === null ? "—" : p ? modp(v - y[i], p) : +(v - y[i]).toFixed(6)));
    // recta con más coincidencias
    const lines = new Map();
    for (let s = 0; s < known.length; s++) for (let t = s + 1; t < known.length; t++) {
      const [i, yi] = known[s], [j, yj] = known[t];
      let a, b;
      if (p) { const inv = invp(j - i, p); b = modp((yj - yi) * inv, p); a = modp(yi - b * X[i], p); }
      else { b = (yj - yi) / (j - i); a = yi - b * X[i]; a = +a.toFixed(9); b = +b.toFixed(9); }
      const key = a + "|" + b;
      if (!lines.has(key)) {
        const ok = known.filter(([k, v]) => (p ? modp(a + b * X[k], p) === v : Math.abs(a + b * X[k] - v) < 1e-9)).length;
        lines.set(key, { a, b, ok });
      }
    }
    const arr = Array.from(lines.values()).sort((u, v) => v.ok - u.ok);
    let html = "<p><strong>Saltos:</strong> " + saltos.join(", ") + (p ? " (módulo " + p + ")" : "") + "</p>";
    const freq = {}; saltos.forEach((s) => { if (s !== "—") freq[s] = (freq[s] || 0) + 1; });
    const top = Object.entries(freq).sort((u, v) => v[1] - u[1])[0];
    if (top) html += "<p>Paso más repetido: <strong>" + top[0] + "</strong> (" + top[1] + " veces).</p>";
    if (!arr.length) { out.innerHTML = html + '<span class="pill bad">Hacen falta al menos dos valores conocidos.</span>'; return; }
    const best = arr[0]; const tie = arr.filter((l) => l.ok === best.ok);
    const m = known.length; const garant = Math.floor((m - 2) / 2);
    if (tie.length > 1) {
      html += '<p><span class="pill warn">Empate</span> Hay ' + tie.length + " rectas que coinciden con " + best.ok + " de " + m + " valores: " +
        tie.slice(0, 4).map((l) => "y = " + fmt(l.a) + " + " + fmt(l.b) + "x").join("; ") + ". No se puede decidir: hay demasiados errores para tan pocos testigos.</p>";
    } else {
      const fit = X.map((x) => (p ? modp(best.a + best.b * x, p) : +(best.a + best.b * x).toFixed(6)));
      const errs = known.filter(([k, v]) => fit[k] !== v).map(([k]) => k);
      const holes = y.map((v, i) => (v === null ? i : -1)).filter((i) => i >= 0);
      html += "<p>Recta con más coincidencias: <strong>y = " + fmt(best.a) + " + " + fmt(best.b) + "x</strong>" + (p ? " (mód " + p + ")" : "") +
        ", que coincide con " + best.ok + " de " + m + " valores conocidos. Mensaje (a, b) = (" + fmt(best.a) + ", " + fmt(best.b) + ").</p>";
      html += '<table class="res"><tr><th>x</th>' + X.map((x) => "<td>" + x + "</td>").join("") + "</tr><tr><th>recibido</th>" +
        y.map((v, i) => "<td" + (errs.includes(i) ? ' class="hl"' : "") + ">" + (v === null ? "?" : v) + "</td>").join("") + "</tr><tr><th>corregido</th>" +
        fit.map((v, i) => "<td" + (errs.includes(i) || holes.includes(i) ? ' class="hl"' : "") + ">" + v + "</td>").join("") + "</tr></table>";
      html += "<p>" + (errs.length ? '<span class="pill warn">' + errs.length + " error(es) en x = " + errs.map((k) => k + 1).join(", ") + "</span> " : '<span class="pill ok">Sin errores</span> ') +
        (holes.length ? '<span class="pill ok">' + holes.length + " hueco(s) rellenado(s)</span> " : "") + "</p>";
      html += '<p class="hint">Con ' + m + " valores conocidos ($d=" + (m - 1) + "$) se garantiza corregir hasta " + garant + " error(es).</p>" +
        (errs.length > garant ? '<p><span class="pill bad">Ojo:</span> hay más errores de los garantizados; la respuesta es la más probable, pero podría no ser la verdadera.</p>' : "");
    }
    out.innerHTML = html; typeset(out);
  }
  on("rs-go", "click", analizar);
  on("rs-enc", "click", () => {
    const p = +$("rs-p").value; const ab = $("rs-ab").value.split(/[,\s]+/).map(Number); const n = +$("rs-n").value;
    if (ab.length < 2 || ab.some((v) => !isFinite(v))) return;
    const vals = []; for (let x = 1; x <= n; x++) vals.push(p ? modp(ab[0] + ab[1] * x, p) : ab[0] + ab[1] * x);
    $("rs-y").value = vals.join(", "); analizar();
  });
  analizar();
}

/* ------------------------------------------------------------------ */
/* SVD                                                                 */
/* ------------------------------------------------------------------ */
function svd2(a, b, c, d) {
  const p = a * a + c * c, q = a * b + c * d, r = b * b + d * d;
  const tr = p + r, det = p * r - q * q, disc = Math.sqrt(Math.max(tr * tr / 4 - det, 0));
  const l1 = tr / 2 + disc, l2 = Math.max(tr / 2 - disc, 0);
  let v1 = Math.abs(q) > 1e-12 ? [q, l1 - p] : (p >= r ? [1, 0] : [0, 1]);
  const nv = Math.hypot(v1[0], v1[1]); v1 = [v1[0] / nv, v1[1] / nv]; if (v1[0] < 0) v1 = [-v1[0], -v1[1]];
  const v2 = [-v1[1], v1[0]]; const s1 = Math.sqrt(l1), s2 = Math.sqrt(l2);
  const u1 = s1 > 1e-12 ? [(a * v1[0] + b * v1[1]) / s1, (c * v1[0] + d * v1[1]) / s1] : [1, 0];
  const u2 = s2 > 1e-12 ? [(a * v2[0] + b * v2[1]) / s2, (c * v2[0] + d * v2[1]) / s2] : [-u1[1], u1[0]];
  return { u1, u2, s1, s2, v1, v2 };
}
// imagen de prueba generada con código
function testImage(N) {
  const cv = document.createElement("canvas"); cv.width = cv.height = N; const g = cv.getContext("2d");
  const gr = g.createLinearGradient(0, 0, 0, N); gr.addColorStop(0, "#d9e6f7"); gr.addColorStop(1, "#4a5d78");
  g.fillStyle = gr; g.fillRect(0, 0, N, N);
  g.fillStyle = "#f7e9a8"; g.beginPath(); g.arc(N * 0.74, N * 0.24, N * 0.12, 0, 7); g.fill();
  g.fillStyle = "#2c3a4f"; g.beginPath(); g.moveTo(0, N * 0.78); g.lineTo(N * 0.28, N * 0.42); g.lineTo(N * 0.5, N * 0.66);
  g.lineTo(N * 0.72, N * 0.38); g.lineTo(N, N * 0.72); g.lineTo(N, N); g.lineTo(0, N); g.fill();
  g.fillStyle = "#ffffff"; g.beginPath(); g.moveTo(N * 0.28, N * 0.42); g.lineTo(N * 0.33, N * 0.5); g.lineTo(N * 0.23, N * 0.5); g.fill();
  for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? "#111" : "#eee"; g.fillRect(N * 0.06 + i * N * 0.045, N * 0.86, N * 0.045, N * 0.08); }
  g.fillStyle = "#0b1220"; g.font = "bold " + Math.round(N * 0.2) + "px sans-serif"; g.fillText("ALA", N * 0.05, N * 0.26);
  const data = g.getImageData(0, 0, N, N).data; const A = [];
  for (let i = 0; i < N; i++) { const row = new Float64Array(N); for (let j = 0; j < N; j++) { const k = 4 * (i * N + j); row[j] = (0.299 * data[k] + 0.587 * data[k + 1] + 0.114 * data[k + 2]) / 255; } A.push(row); }
  return A;
}
// SVD por Jacobi de un lado (columnas)
function jacobiSVD(A) {
  const m = A.length, n = A[0].length;
  const U = []; for (let j = 0; j < n; j++) { const col = new Float64Array(m); for (let i = 0; i < m; i++) col[i] = A[i][j]; U.push(col); }
  const V = []; for (let j = 0; j < n; j++) { const col = new Float64Array(n); col[j] = 1; V.push(col); }
  for (let sweep = 0; sweep < 12; sweep++) {
    let off = 0;
    for (let p = 0; p < n - 1; p++) for (let q = p + 1; q < n; q++) {
      const up = U[p], uq = U[q]; let al = 0, be = 0, ga = 0;
      for (let i = 0; i < m; i++) { al += up[i] * up[i]; be += uq[i] * uq[i]; ga += up[i] * uq[i]; }
      if (Math.abs(ga) < 1e-12 * Math.sqrt(al * be) || Math.abs(ga) < 1e-15) continue;
      off = Math.max(off, Math.abs(ga) / Math.sqrt(al * be));
      const z = (be - al) / (2 * ga); const t = Math.sign(z || 1) / (Math.abs(z) + Math.sqrt(1 + z * z));
      const c = 1 / Math.sqrt(1 + t * t), s = c * t;
      for (let i = 0; i < m; i++) { const x = up[i], y = uq[i]; up[i] = c * x - s * y; uq[i] = s * x + c * y; }
      const vp = V[p], vq = V[q];
      for (let i = 0; i < n; i++) { const x = vp[i], y = vq[i]; vp[i] = c * x - s * y; vq[i] = s * x + c * y; }
    }
    if (off < 1e-10) break;
  }
  const S = U.map((col) => Math.sqrt(col.reduce((s, x) => s + x * x, 0)));
  const idx = S.map((s, i) => i).sort((i, j) => S[j] - S[i]);
  return { S: idx.map((i) => S[i]), U: idx.map((i) => U[i].map((x) => (S[i] > 1e-12 ? x / S[i] : 0))), V: idx.map((i) => V[i]) };
}
function drawRank(canvas, svd, k, N) {
  const g = canvas.getContext("2d"); const img = g.createImageData(N, N);
  const R = new Float64Array(N * N);
  for (let r = 0; r < k; r++) { const s = svd.S[r], u = svd.U[r], v = svd.V[r]; for (let i = 0; i < N; i++) { const a = s * u[i]; for (let j = 0; j < N; j++) R[i * N + j] += a * v[j]; } }
  for (let t = 0; t < N * N; t++) { const x = Math.max(0, Math.min(255, Math.round(R[t] * 255))); img.data[4 * t] = img.data[4 * t + 1] = img.data[4 * t + 2] = x; img.data[4 * t + 3] = 255; }
  g.putImageData(img, 0, 0);
}
let SVDIMG = null;
function svdImage(cb) {
  if (SVDIMG) { cb(SVDIMG); return; }
  setTimeout(() => {
    const N = 128; const A = testImage(N); const t0 = performance.now(); const svd = jacobiSVD(A);
    const tot = svd.S.reduce((s, x) => s + x * x, 0);
    SVDIMG = { N, A, svd, tot, ms: performance.now() - t0 }; cb(SVDIMG);
  }, 30);
}
function svdStrip() {
  const strip = $("svdStrip"); if (!strip) return;
  svdImage((D) => {
    strip.querySelectorAll("canvas").forEach((cv) => {
      const k = cv.dataset.k === "orig" ? D.N : +cv.dataset.k; drawRank(cv, D.svd, k, D.N);
    });
    const svg = $("svdScree"); const S = D.svd.S; const W = 320, Hh = 170, x0 = 40, y0 = 12, w = 266, h = 128;
    const lmax = Math.log10(S[0]), lmin = Math.log10(Math.max(S[S.length - 1], 1e-6 * S[0]));
    const Y = (s) => y0 + h - (Math.log10(Math.max(s, 1e-6 * S[0])) - lmin) / (lmax - lmin) * h;
    let p = "";
    S.forEach((s, i) => { p += (i ? "L" : "M") + (x0 + i / (S.length - 1) * w).toFixed(1) + "," + Y(s).toFixed(1); });
    let marks = "";
    [5, 20, 50].forEach((k) => { const x = x0 + (k - 1) / (S.length - 1) * w; marks += '<line x1="' + x + '" y1="' + y0 + '" x2="' + x + '" y2="' + (y0 + h) + '" class="guide"/><text class="lbl-s" x="' + x + '" y="' + (y0 + h + 14) + '" text-anchor="middle">k=' + k + "</text>"; });
    svg.setAttribute("viewBox", "0 0 " + W + " " + Hh);
    svg.innerHTML = '<line class="axis" x1="' + x0 + '" y1="' + (y0 + h) + '" x2="' + (x0 + w) + '" y2="' + (y0 + h) + '"/><line class="axis" x1="' + x0 + '" y1="' + y0 + '" x2="' + x0 + '" y2="' + (y0 + h) + '"/>' +
      marks + '<path d="' + p + '" fill="none" stroke="var(--accent)" stroke-width="2"/>' +
      '<text class="lbl-s" x="' + (x0 - 4) + '" y="' + (y0 + 8) + '" text-anchor="end">' + S[0].toFixed(0) + '</text><text class="lbl-s" x="' + (x0 - 4) + '" y="' + (y0 + h) + '" text-anchor="end">10^' + lmin.toFixed(0) + '</text>' +
      '<text class="lbl-s" x="' + (x0 + w) + '" y="' + (y0 + h + 14) + '" text-anchor="end">i</text>';
    const pct = (k) => (100 * D.svd.S.slice(0, k).reduce((s, x) => s + x * x, 0) / D.tot).toFixed(2);
    $("svdStatus").textContent = "SVD calculada en " + D.ms.toFixed(0) + " ms. Energía conservada: k=5 → " + pct(5) + " %, k=20 → " + pct(20) + " %, k=50 → " + pct(50) + " %.";
  });
}
function lab9() {
  if (!$("sv-svg")) return;
  function draw() {
    const a = +$("sv-a").value, b = +$("sv-b").value, c = +$("sv-c").value, d = +$("sv-d").value;
    if ([a, b, c, d].some((x) => !isFinite(x))) return;
    const S = svd2(a, b, c, d);
    const sc = Math.min(90 / Math.max(S.s1, 1), 90);
    const P = (cx, cy, x, y) => [cx + x * sc, cy - y * sc];
    let L = '<line class="axis-l" x1="20" y1="130" x2="240" y2="130"/><line class="axis-l" x1="130" y1="20" x2="130" y2="240"/>' +
      '<line class="axis-l" x1="280" y1="130" x2="500" y2="130"/><line class="axis-l" x1="390" y1="20" x2="390" y2="240"/>';
    let circ = "", ell = "";
    for (let t = 0; t <= 64; t++) {
      const th = 2 * Math.PI * t / 64, x = Math.cos(th), y = Math.sin(th);
      const p1 = P(130, 130, x, y), p2 = P(390, 130, a * x + b * y, c * x + d * y);
      circ += (t ? "L" : "M") + p1[0].toFixed(1) + "," + p1[1].toFixed(1); ell += (t ? "L" : "M") + p2[0].toFixed(1) + "," + p2[1].toFixed(1);
    }
    const arrow = (cx, cy, v, cls, mk, lab) => { const q = P(cx, cy, v[0], v[1]); return '<line class="' + cls + '" x1="' + cx + '" y1="' + cy + '" x2="' + q[0] + '" y2="' + q[1] + '" marker-end="url(#' + mk + ')"/><text class="lbl-it" x="' + (q[0] + 6) + '" y="' + (q[1] - 6) + '">' + lab + "</text>"; };
    $("sv-svg").innerHTML = '<defs><marker id="ahA2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" class="ahA"/></marker><marker id="ahB2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" class="ahB"/></marker></defs>' +
      L + '<path class="shape" d="' + circ + '"/><path class="shape" d="' + ell + '"/>' +
      arrow(130, 130, S.v1, "vecA", "ahA2", "v₁") + arrow(130, 130, S.v2, "vecB", "ahB2", "v₂") +
      arrow(390, 130, [S.s1 * S.u1[0], S.s1 * S.u1[1]], "vecA", "ahA2", "σ₁u₁") + arrow(390, 130, [S.s2 * S.u2[0], S.s2 * S.u2[1]], "vecB", "ahB2", "σ₂u₂") +
      '<text class="lbl-b" x="130" y="255" text-anchor="middle">círculo unitario</text><text class="lbl-b" x="390" y="255" text-anchor="middle">A · círculo</text>';
    const M = (r) => "\\begin{bmatrix}" + r.map((x) => x.map((y) => fmt(y, 3)).join("&")).join("\\\\") + "\\end{bmatrix}";
    $("sv-out").innerHTML = "$U=" + M([[S.u1[0], S.u2[0]], [S.u1[1], S.u2[1]]]) + "$, $\\Sigma=" + M([[S.s1, 0], [0, S.s2]]) + "$, $V=" + M([[S.v1[0], S.v2[0]], [S.v1[1], S.v2[1]]]) + "$" +
      '<div class="kv" style="margin-top:8px"><b>σ₁, σ₂</b><span>' + fmt(S.s1) + ", " + fmt(S.s2) + "</span><b>σ₁·σ₂ = |det A|</b><span>" + fmt(S.s1 * S.s2) + " = " + fmt(Math.abs(a * d - b * c)) +
      "</span><b>σ₁² + σ₂² = ‖A‖²_F</b><span>" + fmt(S.s1 * S.s1 + S.s2 * S.s2) + "</span><b>Rango</b><span>" + (S.s2 > 1e-9 ? 2 : S.s1 > 1e-9 ? 1 : 0) + "</span></div>";
    typeset($("sv-out"));
  }
  ["sv-a", "sv-b", "sv-c", "sv-d"].forEach((id) => on(id, "input", draw)); draw();
  function rank() {
    const k = +$("sv-k").value; $("sv-kv").textContent = k;
    svdImage((D) => {
      drawRank($("sv-canvas"), D.svd, k, D.N);
      const err = Math.sqrt(D.svd.S.slice(k).reduce((s, x) => s + x * x, 0) / D.tot);
      $("sv-kout").innerHTML = '<div class="kv"><b>Datos guardados</b><span>' + (100 * k * (2 * D.N + 1) / (D.N * D.N)).toFixed(1) + " %</span><b>Error relativo ‖A−A_k‖_F/‖A‖_F</b><span>" +
        (100 * err).toFixed(2) + " %</span><b>σ_{k+1} = ‖A−A_k‖₂</b><span>" + (k < D.N ? D.svd.S[k].toFixed(3) : 0) + "</span></div>";
    });
  }
  on("sv-k", "input", rank); rank();
}

/* ------------------------------------------------------------------ */
/* PCA                                                                 */
/* ------------------------------------------------------------------ */
function rng(seed) { return function () { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function lab10() {
  if (!$("pc-svg")) return;
  function run() {
    const ang = +$("pc-ang").value * Math.PI / 180, s1 = +$("pc-s1").value / 10, s2 = +$("pc-s2").value / 10, n = +$("pc-n").value;
    const R = rng(11); const pts = [];
    for (let i = 0; i < n; i++) {
      const u = Math.max(R(), 1e-9), v = R(); const z1 = Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v), z2 = Math.sqrt(-2 * Math.log(u)) * Math.sin(2 * Math.PI * v);
      const a = z1 * s1, b = z2 * s2; pts.push([a * Math.cos(ang) - b * Math.sin(ang), a * Math.sin(ang) + b * Math.cos(ang)]);
    }
    if ($("pc-out").checked) pts.push([-4.5, 3.6]);
    const N = pts.length, mx = pts.reduce((s, p) => s + p[0], 0) / N, my = pts.reduce((s, p) => s + p[1], 0) / N;
    let sxx = 0, syy = 0, sxy = 0; pts.forEach(([x, y]) => { sxx += (x - mx) ** 2; syy += (y - my) ** 2; sxy += (x - mx) * (y - my); });
    sxx /= N - 1; syy /= N - 1; sxy /= N - 1;
    const tr = sxx + syy, det = sxx * syy - sxy * sxy, disc = Math.sqrt(Math.max(tr * tr / 4 - det, 0));
    const l1 = tr / 2 + disc, l2 = tr / 2 - disc;
    let v1 = Math.abs(sxy) > 1e-12 ? [sxy, l1 - sxx] : (sxx >= syy ? [1, 0] : [0, 1]); const nv = Math.hypot(...v1); v1 = [v1[0] / nv, v1[1] / nv]; if (v1[0] < 0) v1 = [-v1[0], -v1[1]];
    const v2 = [-v1[1], v1[0]];
    const sc = 30, cx = 260, cy = 165, X = (x) => cx + x * sc, Y = (y) => cy - y * sc;
    let g = '<defs><marker id="ahA3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" class="ahA"/></marker><marker id="ahB3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" class="ahB"/></marker></defs>';
    for (let k = -8; k <= 8; k++) { g += '<line class="grid" x1="' + X(k) + '" y1="0" x2="' + X(k) + '" y2="330"/>'; if (Math.abs(k) <= 5) g += '<line class="grid" x1="0" y1="' + Y(k) + '" x2="520" y2="' + Y(k) + '"/>'; }
    g += '<line class="pcline" x1="' + X(mx - 9 * v1[0]) + '" y1="' + Y(my - 9 * v1[1]) + '" x2="' + X(mx + 9 * v1[0]) + '" y2="' + Y(my + 9 * v1[1]) + '" opacity=".5"/>';
    let err = 0;
    pts.forEach(([x, y], i) => {
      const t = (x - mx) * v1[0] + (y - my) * v1[1]; const px = mx + t * v1[0], py = my + t * v1[1]; err += (x - px) ** 2 + (y - py) ** 2;
      g += '<line class="resid" x1="' + X(x) + '" y1="' + Y(y) + '" x2="' + X(px) + '" y2="' + Y(py) + '" opacity=".55"/>';
      g += '<circle class="pt" cx="' + X(x) + '" cy="' + Y(y) + '" r="' + ($("pc-out").checked && i === N - 1 ? 6 : 3.2) + '"' + ($("pc-out").checked && i === N - 1 ? ' style="fill:var(--red)"' : "") + "/>";
    });
    const L1 = 2 * Math.sqrt(l1), L2 = 2 * Math.sqrt(Math.max(l2, 0));
    g += '<line class="vecA thick" x1="' + X(mx) + '" y1="' + Y(my) + '" x2="' + X(mx + L1 * v1[0]) + '" y2="' + Y(my + L1 * v1[1]) + '" marker-end="url(#ahA3)"/>';
    g += '<line class="vecB thick" x1="' + X(mx) + '" y1="' + Y(my) + '" x2="' + X(mx + L2 * v2[0]) + '" y2="' + Y(my + L2 * v2[1]) + '" marker-end="url(#ahB3)"/>';
    g += '<circle class="mu" cx="' + X(mx) + '" cy="' + Y(my) + '" r="5"/><text class="lbl-b" x="' + (X(mx + L1 * v1[0]) + 8) + '" y="' + Y(my + L1 * v1[1]) + '">PC1</text><text class="lbl-b" x="' + (X(mx + L2 * v2[0]) + 8) + '" y="' + Y(my + L2 * v2[1]) + '">PC2</text>';
    $("pc-svg").innerHTML = g;
    $("pc-res").innerHTML = "$\\mu=(" + fmt(mx, 3) + "," + fmt(my, 3) + ")$, $S=\\begin{bmatrix}" + fmt(sxx, 3) + "&" + fmt(sxy, 3) + "\\\\" + fmt(sxy, 3) + "&" + fmt(syy, 3) + "\\end{bmatrix}$" +
      '<div class="kv" style="margin-top:8px"><b>λ₁, λ₂</b><span>' + fmt(l1, 3) + ", " + fmt(l2, 3) + "</span><b>PC1</b><span>(" + fmt(v1[0], 3) + ", " + fmt(v1[1], 3) + "), ángulo " + fmt(Math.atan2(v1[1], v1[0]) * 180 / Math.PI, 1) + "°</span>" +
      "<b>Varianza explicada por PC1</b><span>" + (100 * l1 / tr).toFixed(1) + " %</span><b>Suma de residuos² sobre PC1</b><span>" + fmt(err, 3) + " = (n−1)·λ₂</span></div>" +
      ($("pc-out").checked ? '<p><span class="pill warn">Un solo valor atípico</span> desvía PC1: por eso existe el PCA robusto.</p>' : "");
    typeset($("pc-res"));
  }
  ["pc-ang", "pc-s1", "pc-s2", "pc-n"].forEach((id) => on(id, "input", run)); on("pc-out", "change", run); run();
  function pve() {
    const L = $("pve-l").value.split(/[,\s;]+/).filter((s) => s).map(Number).filter((x) => isFinite(x) && x >= 0).sort((a, b) => b - a);
    const th = +$("pve-t").value; const tot = L.reduce((s, x) => s + x, 0);
    if (!L.length || tot <= 0) { $("pve-out").innerHTML = '<span class="pill bad">Escribe autovalores no negativos.</span>'; return; }
    let acc = 0, k = null;
    const rows = L.map((l, i) => { const p = 100 * l / tot; acc += p; if (k === null && acc >= th - 1e-9) k = i + 1;
      return "<tr><td>PC" + (i + 1) + "</td><td>" + l + "</td><td>" + p.toFixed(2) + ' %<span style="display:inline-block;height:8px;border-radius:4px;margin-left:8px;vertical-align:middle;width:' + (1.4 * p).toFixed(0) + 'px;background:var(--brand)"></span></td><td>' + acc.toFixed(2) + " %</td><td>" + (l > 1 ? "λ > 1" : "") + "</td></tr>"; });
    $("pve-out").innerHTML = '<table class="res"><tr><th>Componente</th><th>λ</th><th>PVE</th><th>Acumulada</th><th>Kaiser</th></tr>' + rows.join("") + "</table>" +
      "<p>Para llegar al " + th + " % hacen falta <strong>" + k + "</strong> componente(s). Kaiser (datos estandarizados) conservaría " + L.filter((l) => l > 1).length + ".</p>";
  }
  on("pve-go", "click", pve); pve();
}

/* ------------------------------------------------------------------ */
/* TFAL: aritmética exacta con fracciones                              */
/* ------------------------------------------------------------------ */
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; }
function F(n, d = 1) { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); return { n: n / g, d: d / g }; }
const Fz = F(0), F1 = F(1);
const fadd = (x, y) => F(x.n * y.d + y.n * x.d, x.d * y.d), fsub = (x, y) => F(x.n * y.d - y.n * x.d, x.d * y.d);
const fmul = (x, y) => F(x.n * y.n, x.d * y.d), fdiv = (x, y) => F(x.n * y.d, x.d * y.n);
const fz = (x) => x.n === 0;
const ftex = (x) => (x.d === 1 ? String(x.n) : (x.n < 0 ? "-" : "") + "\\tfrac{" + Math.abs(x.n) + "}{" + x.d + "}");
function parseF(s) {
  s = s.trim(); if (/^-?\d+\/\d+$/.test(s)) { const [a, b] = s.split("/").map(Number); return b ? F(a, b) : null; }
  if (/^-?\d+(\.\d+)?$/.test(s)) { const k = (s.split(".")[1] || "").length; return F(Math.round(Number(s) * 10 ** k), 10 ** k); }
  return null;
}
function rrefF(M) {
  M = M.map((r) => r.slice()); const m = M.length, n = M[0].length; const piv = []; let r = 0;
  for (let c = 0; c < n && r < m; c++) {
    let p = -1; for (let i = r; i < m; i++) if (!fz(M[i][c])) { p = i; break; }
    if (p < 0) continue; [M[r], M[p]] = [M[p], M[r]];
    const pv = M[r][c]; M[r] = M[r].map((x) => fdiv(x, pv));
    for (let i = 0; i < m; i++) if (i !== r && !fz(M[i][c])) { const f = M[i][c]; M[i] = M[i].map((x, j) => fsub(x, fmul(f, M[r][j]))); }
    piv.push(c); r++;
  }
  return { R: M, piv, rank: r };
}
function nullF(M) {
  const n = M[0].length; const { R, piv } = rrefF(M); const free = []; for (let j = 0; j < n; j++) if (!piv.includes(j)) free.push(j);
  return free.map((f) => { const v = new Array(n).fill(Fz); v[f] = F1; piv.forEach((pc, i) => { v[pc] = F(-R[i][f].n, R[i][f].d); }); return v; });
}
const T = (M) => M[0].map((_, j) => M.map((r) => r[j]));
const vtex = (v) => "\\begin{bmatrix}" + v.map(ftex).join("\\\\") + "\\end{bmatrix}";
const fdot = (a, b) => a.reduce((s, x, i) => fadd(s, fmul(x, b[i])), Fz);
function lab11() {
  if (!$("fs-go")) return;
  function run() {
    const out = $("fs-out");
    const rows = $("fs-A").value.split(/\n/).map((r) => r.trim()).filter((r) => r).map((r) => r.split(/[,\s]+/).map(parseF));
    if (!rows.length || rows.some((r) => r.some((x) => !x)) || rows.some((r) => r.length !== rows[0].length)) { out.innerHTML = '<span class="pill bad">Revisa la matriz: misma cantidad de números en cada fila.</span>'; return; }
    if (rows.length > 6 || rows[0].length > 6) { out.innerHTML = '<span class="pill bad">Usa matrices de hasta 6×6.</span>'; return; }
    const A = rows, m = A.length, n = A[0].length; const { R, piv, rank: r } = rrefF(A);
    const rowB = R.slice(0, r), colB = piv.map((c) => A.map((row) => row[c])), NA = nullF(A), NAT = nullF(T(A));
    const list = (B) => (B.length ? B.map(vtex).join(",\\ ") : "\\{0\\}");
    let html = "<p>$A$ es de $" + m + "\\times" + n + "$ y tiene rango <strong>$r=" + r + "$</strong>.</p>" +
      '<table class="res"><tr><th>Subespacio</th><th>Base</th><th>dim</th></tr>' +
      "<tr><td>C(Aᵀ) ⊂ ℝ<sup>" + n + "</sup></td><td>$" + list(rowB) + "$</td><td>" + r + "</td></tr>" +
      "<tr><td>N(A) ⊂ ℝ<sup>" + n + "</sup></td><td>$" + list(NA) + "$</td><td>" + (n - r) + "</td></tr>" +
      "<tr><td>C(A) ⊂ ℝ<sup>" + m + "</sup></td><td>$" + list(colB) + "$</td><td>" + r + "</td></tr>" +
      "<tr><td>N(Aᵀ) ⊂ ℝ<sup>" + m + "</sup></td><td>$" + list(NAT) + "$</td><td>" + (m - r) + "</td></tr></table>";
    const orto = rowB.every((u) => NA.every((v) => fz(fdot(u, v)))) && colB.every((u) => NAT.every((v) => fz(fdot(u, v))));
    html += "<p>" + (orto ? '<span class="pill ok">Comprobado: C(Aᵀ) ⊥ N(A) y C(A) ⊥ N(Aᵀ)</span>' : "") + " Dimensiones: $" + r + "+" + (n - r) + "=" + n + "$ y $" + r + "+" + (m - r) + "=" + m + "$.</p>";
    const bs = $("fs-b").value.trim();
    if (bs) {
      const b = bs.split(/[,\s]+/).map(parseF);
      if (b.length !== m || b.some((x) => !x)) html += '<p><span class="pill bad">b debe tener ' + m + " componentes.</span></p>";
      else {
        const cert = NAT.find((y) => !fz(fdot(y, b)));
        if (cert) html += '<p><span class="pill bad">Ax = b no tiene solución</span> Certificado de Fredholm: $y=' + vtex(cert) + "$ cumple $A^{T}y=0$ y $y^{T}b=" + ftex(fdot(cert, b)) + "\\neq0$.</p>";
        else {
          const Ab = A.map((row, i) => row.concat([b[i]])); const RR = rrefF(Ab);
          const xp = new Array(n).fill(Fz); RR.piv.forEach((pc, i) => { if (pc < n) xp[pc] = RR.R[i][n]; });
          // x_r = x_p - proyección sobre N(A)
          let xr = xp.slice();
          if (NA.length) {
            const G = NA.map((u) => NA.map((v) => fdot(u, v))); const rhs = NA.map((u) => fdot(u, xp));
            const sol = rrefF(G.map((row, i) => row.concat([rhs[i]]))); const c = sol.R.map((row) => row[NA.length]);
            NA.forEach((v, k) => { xr = xr.map((x, i) => fsub(x, fmul(c[k], v[i]))); });
          }
          const xn = xp.map((x, i) => fsub(x, xr[i]));
          html += '<p><span class="pill ok">Ax = b tiene solución</span> porque $b\\perp N(A^{T})$. Solución de norma mínima (en el espacio fila): $x_r=' + vtex(xr) + "$." +
            (NA.length ? " Una solución particular es $x_p=" + vtex(xp) + "=x_r+x_n$ con $x_n=" + vtex(xn) + "\\in N(A)$; la solución general es $x_r+N(A)$." : " Es única porque $N(A)=\\{0\\}$.") + "</p>";
        }
      }
    }
    out.innerHTML = html; typeset(out);
  }
  on("fs-go", "click", run); run();
}

/* ------------------------------------------------------------------ */
/* Campos finitos                                                       */
/* ------------------------------------------------------------------ */
function gfmul(a, b, P, n) { let r = 0; while (b) { if (b & 1) r ^= a; b >>= 1; a <<= 1; if (a & (1 << n)) a ^= P; } return r; }
function gfpow(a, e, P, n) { let r = 1; while (e) { if (e & 1) r = gfmul(r, a, P, n); a = gfmul(a, a, P, n); e >>= 1; } return r; }
function ordOf(g, P, n) { if (!g) return 0; let x = g, k = 1; while (x !== 1 && k <= (1 << n)) { x = gfmul(x, g, P, n); k++; } return x === 1 ? k : 0; }
function polyStr(v, n) { const t = []; for (let i = n; i >= 0; i--) if ((v >> i) & 1) t.push(i === 0 ? "1" : i === 1 ? "x" : "x^{" + i + "}"); return t.length ? t.join("+") : "0"; }
function lab12() {
  if (!$("gf-go")) return;
  function run() {
    const [P, n] = $("gf-p").value.split(",").map(Number); const q = 1 << n; const hx = (v) => v.toString(16).toUpperCase();
    const pa = parseInt($("gf-a").value, 16), pb = parseInt($("gf-b").value, 16), pg = parseInt($("gf-g").value, 16);
    const out = $("gf-out");
    if ([pa, pb, pg].some((v) => isNaN(v) || v < 0 || v >= q)) { out.innerHTML = '<span class="pill bad">Los elementos van de 0 a ' + hx(q - 1) + " (hexadecimal).</span>"; return; }
    // generador para logaritmos
    let g0 = 2; while (ordOf(g0, P, n) !== q - 1) g0++;
    const log = {}; let x = 1; for (let k = 0; k < q - 1; k++) { log[x] = k; x = gfmul(x, g0, P, n); }
    const prod = gfmul(pa, pb, P, n), inv = pa ? gfpow(pa, q - 2, P, n) : null;
    // pasos del campesino ruso
    let a = pa, b = pb, r = 0; const steps = [];
    while (b) { const bit = b & 1; if (bit) r ^= a; steps.push([hx(b), bit, hx(r), hx(a)]); b >>= 1; const ov = a & (1 << (n - 1)); a = ((a << 1) ^ (ov ? P : 0)) & (q - 1); }
    const bin = (v) => v.toString(2).padStart(n, "0");
    out.innerHTML = '<div class="kv"><b>Campo</b><span>$\\mathbb{F}_{' + q + "}=\\mathbb{F}_2[x]/(" + polyStr(P, n) + ")$, P = 0x" + hx(P) + "</span>" +
      "<b>a</b><span>" + hx(pa) + " = " + bin(pa) + " = $" + polyStr(pa, n - 1) + "$</span><b>b</b><span>" + hx(pb) + " = " + bin(pb) + " = $" + polyStr(pb, n - 1) + "$</span>" +
      "<b>a + b</b><span>" + hx(pa ^ pb) + " (XOR)</span><b>a · b</b><span><strong>" + hx(prod) + "</strong>" + (pa && pb ? " · con logaritmos base " + hx(g0) + ": " + log[pa] + " + " + log[pb] + " ≡ " + (log[pa] + log[pb]) % (q - 1) + " (mód " + (q - 1) + ")" : "") + "</span>" +
      "<b>a⁻¹</b><span>" + (inv === null ? "no existe (a = 0)" : hx(inv) + " (comprobación: a·a⁻¹ = " + hx(gfmul(pa, inv, P, n)) + ")") + "</span>" +
      "<b>log a</b><span>" + (pa ? log[pa] + " (base " + hx(g0) + ")" : "—") + "</span></div>" +
      "<h5>Campesino ruso: a·b paso a paso</h5><table class=\"res\"><tr><th>b</th><th>bit menor</th><th>r</th><th>a</th></tr>" +
      steps.map((s) => "<tr><td>" + s[0] + "</td><td>" + s[1] + "</td><td" + (s[1] ? ' class="hl"' : "") + ">" + s[2] + "</td><td>" + s[3] + "</td></tr>").join("") + "</table>" +
      (ordOf(2, P, n) !== q - 1 ? '<p><span class="pill warn">x no es primitivo en este campo</span> (orden ' + ordOf(2, P, n) + "); los logaritmos usan el generador " + hx(g0) + ".</p>" : "");
    typeset(out);
    // ciclo de potencias de g
    const og = ordOf(pg, P, n); const svg = $("gf-svg");
    if (!pg) { svg.innerHTML = '<text class="lbl" x="210" y="210" text-anchor="middle">g = 0 no tiene potencias útiles</text>'; }
    else {
      const R0 = 160, cx = 210, cy = 210; let s = '<circle class="ring" cx="' + cx + '" cy="' + cy + '" r="' + R0 + '"/>';
      let v = 1; const big = og > 40;
      for (let k = 0; k < og; k++) {
        const th = -Math.PI / 2 + 2 * Math.PI * k / og, X = cx + R0 * Math.cos(th), Y = cy + R0 * Math.sin(th);
        s += big ? '<circle cx="' + X.toFixed(1) + '" cy="' + Y.toFixed(1) + '" r="3" fill="var(--brand)"/>' :
          '<g class="gfnode' + (v === 1 ? " one" : og === q - 1 ? "" : " alt") + '"><circle cx="' + X.toFixed(1) + '" cy="' + Y.toFixed(1) + '" r="15"/><text x="' + X.toFixed(1) + '" y="' + (Y + 4).toFixed(1) + '">' + hx(v) + "</text></g>";
        v = gfmul(v, pg, P, n);
      }
      s += '<text class="lbl-b" x="' + cx + '" y="' + (cy - 6) + '" text-anchor="middle">ord(' + hx(pg) + ") = " + og + '</text><text class="lbl-s" x="' + cx + '" y="' + (cy + 14) + '" text-anchor="middle">' +
        (og === q - 1 ? "primitivo: recorre los " + (q - 1) + " no nulos" : "no primitivo: " + og + " de " + (q - 1)) + "</text>";
      svg.innerHTML = s;
    }
    // LFSR
    const c = []; for (let i = 0; i < n; i++) c.push((P >> i) & 1);
    let st = new Array(n).fill(0); st[n - 1] = 1; const start = st.join(""); const seq = [start]; let per = 0;
    for (let k = 1; k <= (1 << n); k++) { let nb = 0; for (let i = 0; i < n; i++) if (c[i]) nb ^= st[i]; st = st.slice(1).concat([nb]); if (st.join("") === start) { per = k; break; } seq.push(st.join("")); }
    const rec = c.map((ci, i) => (ci ? "s_{k+" + i + "}" : null)).filter(Boolean).join("\\oplus ").replace("s_{k+0}", "s_k");
    $("gf-lfsr").innerHTML = "<h5>LFSR de " + n + " celdas: $s_{k+" + n + "}=" + rec + "$</h5><p class=\"mono\" style=\"word-break:break-all\">" + seq.slice(0, 40).join(" → ") + (seq.length > 40 ? " → …" : " → " + start) + "</p>" +
      "<p>Periodo: <strong>" + per + "</strong> " + (per === q - 1 ? '<span class="pill ok">máximo (2ⁿ − 1): polinomio primitivo</span>' : '<span class="pill warn">menor que ' + (q - 1) + ": el polinomio no es primitivo</span>") + "</p>";
    typeset($("gf-lfsr"));
  }
  on("gf-go", "click", run); on("gf-p", "change", run); run();
}

/* ------------------------------------------------------------------ */
document.addEventListener("DOMContentLoaded", () => {
  initUI();
  [lab0, lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8, lab9, lab10, lab11, lab12, svdStrip].forEach((f) => {
    try { f(); } catch (e) { console.error(f.name, e); }
  });
});
})();
