# Cabeçalho da Taverna: interior de taverna em pixel art, 188x64 nativo (exibido em 2x).
# A placa central fica vazia: o título "A Taverna" é texto real (fonte gótica do app) por cima.
import json, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vilarejo"))
from pintor import Tela, dither

W, H = 188, 64
random.seed(3)
P = {
    "4": "#120c14",
    # parede de tábuas (escura) e luz das lanternas
    "a": "#1e120a", "b": "#2c1a0e", "c": "#3d2514", "d": "#53331b", "e": "#7a4a24",
    # viga / madeira clara do balcão e da placa
    "f": "#3a2210", "g": "#6b4223", "h": "#94603a", "i": "#c08850",
    # garrafas
    "j": "#1f4a36", "k": "#3f8a5c", "l": "#7a3c10", "m": "#c07a2a", "n": "#5e1420", "o": "#a8323c", "p": "#d8e8e0",
    # cerveja e espuma
    "q": "#b8741c", "r": "#f0b040", "s": "#efe6d0", "t": "#c8bca4",
    # ferro
    "u": "#2a2730", "v": "#5a5560", "w": "#9a95a4",
    # luz quente
    "x": "#ffd27a", "y": "#ff9a3c", "z": "#fff3c4",
    # barris
    "A": "#4a2c16", "B": "#6e4422", "C": "#94602f", "D": "#3a3540", "E": "#77707e",
}
t = Tela(W, H)

# parede de tábuas verticais
for y in range(H):
    for x in range(W):
        col = (x + (3 if (x // 9) % 2 else 0)) // 9
        rx = x % 9
        c = "c" if (col * 37) % 3 else "b"
        if rx == 0: c = "a"
        elif rx == 1 and (y + col) % 7: c = "d"
        if (x * 13 + y * 7 + col) % 23 == 0: c = "b"           # veio
        if y < 14 and dither(x, y, (14 - y) / 16): c = "a" if c != "a" else c   # fumaça no alto
        t.px(x, y, c)

# luz das lanternas na parede
LAMP = [(30, 12), (158, 12)]
for (lx, ly) in LAMP:
    for y in range(0, H):
        for x in range(lx - 26, lx + 27):
            r = math.hypot(x - lx, (y - ly - 4) * 1.2)
            cur = t.get(x, y)
            if cur in "bcd" and r < 24 and dither(x, y, (24 - r) / 30):
                t.px(x, y, {"b": "c", "c": "d", "d": "e"}[cur])

# viga do teto
t.rect(0, 0, W - 1, 4, "f"); t.rect(0, 4, W - 1, 4, "a"); t.rect(0, 1, W - 1, 1, "g")
for x in range(0, W, 23): t.px(x + 4, 2, "w")

# prateleiras com garrafas (esquerda)
def garrafa(x, base, cor1, cor2, alta=True):
    h = 8 if alta else 6
    t.rect(x, base - h, x + 2, base - 1, cor1); t.px(x, base - h + 1, cor2); t.px(x, base - h + 2, cor2)
    t.rect(x + 1, base - h - 3, x + 1, base - h - 1, cor1); t.px(x + 1, base - h - 4, "e")
for (sy, xs) in ((24, range(4, 50, 6)), (38, range(6, 48, 7))):
    t.rect(2, sy, 52, sy + 1, "g"); t.rect(2, sy + 2, 52, sy + 2, "a")
    for i, x in enumerate(xs):
        c = [("j", "k"), ("l", "m"), ("n", "o"), ("j", "p")][(i + sy) % 4]
        garrafa(x, sy, c[0], c[1], i % 3 != 1)

# barris empilhados com torneira (direita)
def barril(cx, cy, r):
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r * .8), int(cx + r * .8) + 1):
            if ((x + .5 - cx) / (r * .8)) ** 2 + ((y + .5 - cy) / r) ** 2 <= 1:
                c = "B"
                if x < cx - r * .4: c = "C"
                if x > cx + r * .45: c = "A"
                if abs(y - (cy - r * .55)) < .8 or abs(y - (cy + r * .55)) < .8: c = "D"
                t.px(x, y, c)
    t.elipse(cx, cy, r * .28, r * .28, "A"); t.px(cx - 1, cy - 1, "C")
barril(148, 44, 9); barril(166, 44, 9); barril(184, 44, 9); barril(157, 28, 9); barril(175, 28, 9)
t.rect(164, 47, 168, 48, "v"); t.rect(167, 49, 167, 51, "w")    # torneira

# lanternas penduradas
for (lx, ly) in LAMP:
    t.rect(lx, 5, lx, ly - 4, "u")
    t.rect(lx - 3, ly - 3, lx + 3, ly - 3, "v")
    t.rect(lx - 3, ly - 2, lx + 3, ly + 5, "u"); t.rect(lx - 2, ly - 1, lx + 2, ly + 4, "x")
    t.rect(lx - 1, ly, lx + 1, ly + 2, "z"); t.rect(lx - 2, ly + 3, lx + 2, ly + 4, "y")
    t.rect(lx - 3, ly + 6, lx + 3, ly + 6, "v")

# placa central pendurada por correntes (o título é texto por cima)
PX0, PX1, PY0, PY1 = 50, 137, 13, 42
for cx in (PX0 + 12, PX1 - 12):
    for y in range(5, PY0):
        t.px(cx, y, "w" if y % 3 else "v"); t.px(cx + 1, y, "u" if y % 3 else "v")
t.rect(PX0 - 1, PY0 - 1, PX1 + 1, PY1 + 1, "4")
for y in range(PY0, PY1 + 1):
    for x in range(PX0, PX1 + 1):
        fila = (y - PY0) // 7
        c = "h" if fila % 2 else "g"
        if (y - PY0) % 7 == 6: c = "f"
        if (x * 5 + y * 3 + fila * 11) % 19 == 0: c = "g" if c == "h" else "f"
        if y == PY0: c = "i"
        if x == PX0: c = "i"
        if x == PX1 or y == PY1: c = "f"
        t.px(x, y, c)
# moldura escura interna e cravos
for x in range(PX0 + 2, PX1 - 1): t.px(x, PY0 + 2, "f"); t.px(x, PY1 - 2, "f")
for y in range(PY0 + 2, PY1 - 1): t.px(PX0 + 2, y, "f"); t.px(PX1 - 2, y, "f")
for (x, y) in ((PX0 + 5, PY0 + 5), (PX1 - 5, PY0 + 5), (PX0 + 5, PY1 - 5), (PX1 - 5, PY1 - 5)):
    t.px(x, y, "w"); t.px(x + 1, y + 1, "u")
# escurece o miolo para o texto claro ter contraste
for y in range(PY0 + 3, PY1 - 2):
    for x in range(PX0 + 3, PX1 - 2):
        t.px(x, y, {"h": "g", "i": "g"}.get(t.get(x, y), t.get(x, y)))

# balcão com canecas
t.rect(0, 50, W - 1, 51, "i"); t.rect(0, 52, W - 1, 52, "h")
for y in range(53, H):
    for x in range(W):
        c = "g" if (x // 12) % 2 else "f"
        if x % 12 == 0: c = "a"
        if y == 53: c = "a"
        t.px(x, y, c)
def caneca(x, base):
    t.rect(x, base - 7, x + 5, base - 1, "q"); t.rect(x + 1, base - 7, x + 1, base - 2, "r")
    t.rect(x - 1, base - 9, x + 6, base - 8, "s"); t.px(x + 2, base - 10, "s"); t.px(x + 4, base - 10, "t")
    t.rect(x + 6, base - 6, x + 7, base - 6, "q"); t.rect(x + 8, base - 5, x + 8, base - 3, "q"); t.rect(x + 6, base - 2, x + 7, base - 2, "q")
    t.rect(x, base - 1, x + 5, base - 1, "l")
for x in (8, 24, 104, 124): caneca(x, 50)

src = t.fonte("taverna-cabecalho", P)
json.dump(src, open(sys.argv[1], "w"), indent=0)
print("cores:", len(src["palette"]))
