# Faixa vermelha pendurada da Taverna (no lugar da placa do mês), paleta do fundo do taverneiro.
#  - pano 32x26: 9 fatias (topo 7, laterais 8, base 9); o miolo repete a cada 8 px (barra dourada e pontas).
#  - corda 14x22: prego na parede (canto sup. esquerdo) até o nó na ponta do pano; espelhada no lado direito.
import json, os, sys
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vilarejo"))
from pintor import Tela

AQUI = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(AQUI, "faixa")
os.makedirs(OUT, exist_ok=True)
P = {"o": "#2e222f", "a": "#6e2727", "b": "#b33831", "c": "#ea4f36", "d": "#f57d4a",
     "g": "#f9c22b", "G": "#cd683d", "h": "#fbb954",
     "L": "#fdcbb0", "R": "#ab947a", "D": "#966c6c", "N": "#9babb2", "n": "#625565"}

def pano():
    W, H = 32, 26; t = Tela(W, H)
    for y in range(1, 25):
        for x in range(1, W - 1):
            m = x % 8
            if y >= 22:                                   # pontas (triângulos) embaixo
                meia = {22: (1, 6), 23: (2, 5), 24: (3, 4)}[y]
                if not (meia[0] <= m <= meia[1]): continue
                c = "a" if m >= 4 else "b"
            elif y == 1: c = "d"                          # dobra da bainha
            elif y in (2, 3): c = "g" if (y == 3 and x % 4 in (1, 2)) else "b"   # costura dourada
            elif y == 4: c = "a"
            elif y in (18,): c = "h" if m in (1, 2) else "g"   # barra dourada
            elif y == 19: c = "G"
            elif y == 17: c = "a"
            else:
                c = "b"
                if m == 1 and y <= 15: c = "c"            # brilho das dobras
                if m == 5 and y >= 11: c = "a"            # sombra das dobras
                if y in (20, 21) and m == 5: c = "a"
            t.px(x, y, c)
    t.contorno("o")
    return t

def corda():
    W, H = 14, 22; t = Tela(W, H)
    t.linha(2, 2, 10, 17, "R", larg=2)
    for y in range(H):                                     # torção da corda
        for x in range(W):
            if t.get(x, y) == "R":
                k = (x + y) % 3
                t.px(x, y, "L" if k == 0 else ("D" if k == 2 else "R"))
    no = [".ooo.", "oLRRo", "oRRDo", "oRDDo", ".ooo."]     # nó na ponta do pano
    for j, row in enumerate(no):
        for i, ch in enumerate(row):
            if ch != ".": t.px(8 + i, 16 + j, ch)
    t.px(1, 1, "N"); t.px(2, 1, "n"); t.px(1, 2, "n"); t.px(2, 2, "n")   # prego
    t.contorno("o")
    return t

def png(t, nome, escala=1):
    im = Image.new("RGBA", (t.w, t.h))
    for y, row in enumerate(t.g):
        for x, ch in enumerate(row):
            if ch != ".": im.putpixel((x, y), tuple(int(P[ch][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(os.path.join(OUT, nome + ".png"))
    im.resize((t.w * 8, t.h * 8), Image.NEAREST).save(os.path.join(OUT, nome + "-8x.png"))

telas = {"pano": pano(), "corda": corda()}
for n, t in telas.items():
    png(t, n)
    usadas = sorted({ch for r in t.g for ch in r if ch != "."})
    json.dump({"version": 1, "name": n, "canvas": [t.w, t.h], "palette": {k: P[k] for k in usadas},
               "frames": [{"name": n, "duration_ms": 100, "rows": ["".join(r) for r in t.g]}]},
              open(os.path.join(OUT, n + "-source.json"), "w"), indent=0)
print("ok")
