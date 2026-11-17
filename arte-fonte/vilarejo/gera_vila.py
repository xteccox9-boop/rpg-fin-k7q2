# Fundo do Vilarejo: vila medieval ao pôr do sol, 188x406 nativo (exibido em 2x, ~375x812).
# O topo (0..195) é o que aparece; o resto fica atrás dos cards e só precisa de textura escura.
import json, math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pintor import Tela, dither

W, H = 188, 406
HOR = 104          # horizonte
CHAO = 152         # topo da praça
random.seed(7)

P = {
    # céu do topo ao horizonte
    "A": "#1b1530", "B": "#2a1d45", "C": "#45285a", "D": "#6e3560", "E": "#a3485a", "F": "#d0694c",
    "G": "#ee9a55", "H": "#fbc97a", "I": "#fff0b8",
    # nuvens
    "J": "#4a2850", "K": "#b8605a", "L": "#f3a46c",
    # morros
    "M": "#3a2448", "N": "#5a3458", "O": "#2b1f33", "P": "#3d2b3f",
    # moinho
    "R": "#3a2836", "S": "#c0704a", "T": "#24161f", "U": "#6a3f3c",
    # casas
    "a": "#c9a57e", "b": "#a4825f", "c": "#6e5242", "d": "#3e2414", "e": "#6b4223",
    "f": "#5e2420", "g": "#8a3628", "h": "#c45a3a", "i": "#5e4018", "j": "#94702e", "k": "#cfa850",
    "l": "#ffd27a", "m": "#ff9a3c", "n": "#2a1a18", "o": "#3d2412", "p": "#5a4c50", "q": "#857476",
    "r": "#6a5a72", "s": "#9a8aa0",
    # casas do fundo (mais frias e escuras)
    "Q": "#4a3346", "V": "#5e4152", "X": "#7a4a4a",
    # praça
    "t": "#2e2226", "u": "#54423f", "v": "#68534c", "w": "#86705f", "x": "#221a1e",
    # props e árvores
    "y": "#7a4f28", "z": "#3d2412", "0": "#3f3a44", "1": "#8d8792", "2": "#ffe08a", "3": "#ff8a3c",
    "4": "#120c14", "5": "#1c2a24", "6": "#2c4632", "7": "#4d6b3a", "8": "#a08a3a",
}
t = Tela(W, H)

# ---- céu em faixas com transição pontilhada ----
faixas = [(0, "A"), (18, "B"), (36, "C"), (54, "D"), (68, "E"), (80, "F"), (90, "G"), (98, "H")]
for y in range(H):
    for x in range(W):
        if y > HOR + 30: break
        cor = faixas[0][1]
        for i, (y0, c) in enumerate(faixas):
            if y >= y0: cor = c
            # 4 linhas de transição pontilhada antes de cada faixa
            if i + 1 < len(faixas) and faixas[i + 1][0] - 4 <= y < faixas[i + 1][0] and y >= y0:
                if dither(x, y, (y - (faixas[i + 1][0] - 4)) / 4):
                    cor = faixas[i + 1][1]
        t.px(x, y, cor)

# sol atrás do herói (à esquerda)
SX, SY = 44, 89
for y in range(SY - 22, SY + 8):
    for x in range(SX - 22, SX + 23):
        r = math.hypot(x + .5 - SX, (y + .5 - SY) * 1.1)
        if r < 7: t.px(x, y, "I")
        elif r < 11: t.px(x, y, "H")
        elif r < 15 and dither(x, y, (15 - r) / 4): t.px(x, y, "H")
        elif r < 22 and t.get(x, y) in "EF" and dither(x, y, (22 - r) / 9): t.px(x, y, "G")

# ---- nuvens alongadas, iluminadas por baixo ----
def nuvem(cx, cy, comp, alt):
    pts = []
    for k in range(5):
        ex = cx - comp / 2 + comp * (k + .5) / 5
        pts += t.elipse(ex, cy + (k % 2), comp / 5 + 3, alt + (k % 3), "J")
    baixo = {}
    for (x, y) in pts:
        if t.get(x, y + 1) not in "JKL": baixo[x] = max(baixo.get(x, 0), y)
    for x, yb in baixo.items():   # base iluminada sólida: 2 px claros e 1 px de meio-tom
        t.px(x, yb, "L"); t.px(x, yb - 1, "L"); t.px(x, yb - 2, "K")
nuvem(120, 34, 70, 3); nuvem(30, 52, 50, 2); nuvem(150, 66, 60, 2); nuvem(78, 76, 36, 2)

# ---- montanhas distantes ----
for x in range(W):
    topo = 90 + 5 * math.sin(x / 13) + 3 * math.sin(x / 5.3 + 1) + (4 if 60 < x < 120 else 0)
    for y in range(int(topo), HOR + 14):
        t.px(x, y, "M")
    if math.sin(x / 13 + .6) > 0: t.px(x, int(topo), "N")

# ---- morro do moinho (esquerda) e morros próximos ----
for x in range(W):
    a = 108 - 12 * math.exp(-((x - 24) / 22) ** 2) + 2 * math.sin(x / 7)
    for y in range(int(a), CHAO):
        t.px(x, y, "O")
    t.px(x, int(a), "P")
# moinho
MX, MY = 24, 82
t.poly([(MX - 6, 98), (MX + 6, 98), (MX + 4, MY), (MX - 4, MY)], "R")
t.poly([(MX - 5, MY), (MX + 5, MY), (MX, MY - 6)], "T")
for y in range(MY, 98):  # borda iluminada pelo sol (à direita do moinho)
    xs = [x for x in range(MX - 7, MX + 8) if t.get(x, y) == "R"]
    if xs: t.px(xs[-1], y, "S")
t.rect(MX - 1, 92, MX + 1, 97, "T")
for ang in (25, 115, 205, 295):
    a = math.radians(ang)
    ex, ey = MX + 15 * math.cos(a), MY + 1 + 15 * math.sin(a)
    t.linha(MX, MY + 1, ex, ey, "T")
    px_, py_ = -math.sin(a), math.cos(a)
    for k in range(5, 15):
        bx, by = MX + k * math.cos(a), MY + 1 + k * math.sin(a)
        for w_ in (1, 2, 3):
            t.px(round(bx + px_ * w_), round(by + py_ * w_), "U")
t.px(MX, MY + 1, "S")

# ---- casas do fundo (silhueta fria) ----
x = -6
while x < W:
    w_ = random.randint(16, 24); h = random.randint(12, 18); base = 134
    t.rect(x, base - h, x + w_, CHAO, "Q")
    t.poly([(x - 2, base - h), (x + w_ + 2, base - h), (x + w_ / 2, base - h - random.randint(7, 10))], "V")
    for k in range(random.randint(1, 2)):
        wx = x + 4 + k * 8
        if dither(wx, base, .7): t.rect(wx, base - h + 4, wx + 2, base - h + 6, "m")
    x += w_ + random.randint(-2, 3)

# ---- árvores entre as casas ----
def arvore(cx, base, r):
    pts = t.elipse(cx, base - r, r, r * 1.1, "6") + t.elipse(cx - r * .5, base - r * .6, r * .7, r * .7, "6")
    for (x, y) in pts:
        if t.get(x - 1, y) not in "56" or t.get(x, y - 1) not in "56":
            t.px(x, y, "8" if (x + y) % 3 else "7")
        elif (x * 7 + y * 3) % 11 == 0:
            t.px(x, y, "7")
        elif t.get(x + 1, y) not in "56" or t.get(x, y + 1) not in "56":
            t.px(x, y, "5")
    t.rect(cx - 1, base - 3, cx, base, "z")
arvore(60, 146, 9); arvore(140, 144, 8); arvore(184, 146, 10)

# ---- casas da frente (enxaimel) ----
def casa(x0, larg, alt, telhado="telha", chamine=True, porta=True):
    x1 = x0 + larg; topo = CHAO - alt; ap = topo - int(larg * .45)
    # parede
    for y in range(topo, CHAO + 1):
        for x in range(x0, x1 + 1):
            c = "b"
            if x <= x0 + 1: c = "a"
            elif x >= x1 - 1: c = "c"
            t.px(x, y, c)
    # oitão (triângulo da parede sob o telhado)
    t.poly([(x0, topo), (x1 + 1, topo), (x0 + larg / 2 + .5, ap + 4)], "b")
    # vigas do enxaimel
    for x in (x0, x1, x0 + larg // 2):
        t.rect(x, topo, x, CHAO, "d")
    t.rect(x0, topo, x1, topo, "d"); t.rect(x0, topo + alt // 2, x1, topo + alt // 2, "e")
    t.linha(x0, topo + alt // 2, x0 + larg // 2, topo, "e"); t.linha(x1, topo + alt // 2, x0 + larg // 2, topo, "e")
    # janelas acesas
    for wx in (x0 + 3, x1 - 7):
        wy = topo + alt // 2 + 3
        if wy + 5 < CHAO - 2:
            t.rect(wx - 1, wy - 1, wx + 4, wy + 5, "d")
            t.rect(wx, wy, wx + 3, wy + 4, "l"); t.rect(wx, wy + 3, wx + 3, wy + 4, "m")
            t.px(wx + 1, wy, "m"); t.rect(wx + 1, wy, wx + 2, wy + 4, "d") if larg > 30 else None
            t.rect(wx, wy + 2, wx + 3, wy + 2, "d")
    if porta:
        px0 = x0 + larg // 2 - 3
        t.rect(px0, CHAO - 9, px0 + 5, CHAO, "o"); t.rect(px0 + 1, CHAO - 10, px0 + 4, CHAO - 10, "o")
        t.px(px0 + 4, CHAO - 5, "k")
    # telhado
    rp = [(x0 - 3, topo + 1), (x1 + 4, topo + 1), (x0 + larg / 2 + .5, ap)]
    def tex(x, y):
        if telhado == "telha":
            c = "g" if (y // 2) % 2 else "f"
            if x < x0 + larg / 2 and (y // 2) % 2: c = "h"
            if (x + (y // 2) * 2) % 6 == 0: c = "f"
        else:
            c = "j" if (x + y) % 3 else "i"
            if x < x0 + larg / 2 and (x - y) % 4 == 0: c = "k"
        return c
    t.poly(rp, tex)
    t.linha(rp[0][0], rp[0][1], rp[2][0], rp[2][1], "4"); t.linha(rp[1][0], rp[1][1], rp[2][0], rp[2][1], "4")
    t.rect(rp[0][0], rp[0][1], rp[1][0], rp[1][1], "4")
    if chamine:
        cx = x1 - larg // 4
        t.rect(cx, ap + 2, cx + 3, topo - 2, "p"); t.rect(cx, ap + 2, cx, topo - 2, "q"); t.rect(cx - 1, ap + 1, cx + 4, ap + 2, "q")
        for k, (dx, dy, r) in enumerate(((2, -4, 2), (4, -9, 2.5), (7, -15, 3), (11, -21, 3.5))):
            t.elipse(cx + 1.5 + dx, ap + dy, r, r * .8, "s" if k < 2 else "r")

casa(-2, 34, 26, "palha", True, False)
casa(30, 30, 22, "telha", False, True)
casa(66, 38, 30, "telha", True, True)
casa(110, 32, 24, "palha", True, True)
casa(146, 40, 32, "telha", True, True)

# ---- praça de pedra ----
import bisect
cortes = {}
for fila in range(0, (H - CHAO) // 5 + 2):   # cada fileira tem pedras de largura irregular (5 a 10)
    rr = random.Random(fila * 31 + 5); xs = [-rr.randint(0, 6)]
    while xs[-1] < W + 10: xs.append(xs[-1] + rr.randint(5, 10))
    cortes[fila] = xs
for y in range(CHAO + 1, H):
    fila = (y - CHAO - 1) // 5
    for x in range(W):
        xs = cortes[fila]; cel = bisect.bisect_right(xs, x) - 1
        ry = (y - CHAO - 1) % 5; rx = x - xs[cel]; larg = xs[cel + 1] - xs[cel]
        h = (cel * 73 + fila * 151) % 7
        canto = (ry in (0, 3)) and (rx == 0 or rx == larg - 2)   # cantos arredondados
        if ry == 4 or rx == larg - 1 or canto: c = "t"
        elif ry == 0: c = "w" if h % 3 else "v"
        elif ry == 3: c = "u" if h % 2 else "t"
        else: c = "v" if h < 4 else "u"
        prof = (y - CHAO) / 60  # escurece para baixo
        if prof > .6 and dither(x, y, min(1, prof - .6)):
            c = {"w": "v", "v": "u", "u": "t", "t": "x"}.get(c, c)
        if y > 260: c = "x" if dither(x, y, min(1, (y - 260) / 40)) else c
        t.px(x, y, c)

# sombra longa das casas na praça (sol baixo atrás)
for y in range(CHAO + 1, CHAO + 8):
    for x in range(W):
        if dither(x, y, 1 - (y - CHAO) / 8):
            t.px(x, y, {"w": "u", "v": "u", "u": "t"}.get(t.get(x, y), t.get(x, y)))

# ---- poste com lanterna entre o herói e o quadro ----
LX = 88
t.rect(LX, 112, LX + 1, 190, "0"); t.rect(LX + 2, 112, LX + 2, 190, "4"); t.rect(LX - 1, 186, LX + 3, 190, "0")
t.rect(LX - 3, 104, LX + 4, 112, "4"); t.rect(LX - 2, 105, LX + 3, 111, "2"); t.rect(LX - 2, 109, LX + 3, 111, "3")
t.rect(LX - 4, 103, LX + 5, 103, "0"); t.px(LX, 101, "0"); t.px(LX + 1, 102, "0")
for y in range(98, 120):
    for x in range(LX - 14, LX + 16):
        r = math.hypot(x + .5 - LX - .5, y + .5 - 108)
        if 6 < r < 13 and t.get(x, y) in "bcaQV" and dither(x, y, (13 - r) / 14):
            t.px(x, y, "l")

# ---- barris no canto esquerdo ----
def barril(cx, base):
    t.elipse(cx, base - 6, 5, 7, "y")
    t.rect(cx - 5, base - 9, cx + 4, base - 8, "z"); t.rect(cx - 5, base - 3, cx + 4, base - 2, "z")
    t.rect(cx - 4, base - 12, cx - 3, base - 1, "k")
# (barris removidos: ficavam cortados pela borda do pergaminho do Resumo do Mês)

src = t.fonte("vila-por-do-sol", P)
json.dump(src, open(sys.argv[1], "w"), indent=0)
print("cores:", len(src["palette"]))
