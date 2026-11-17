# Herói "Assassino" do Vilarejo: 64x104 nativo (exibido em 2x). Capuz, olhos brilhando, cachecol carmesim,
# adaga em pegada invertida e bolsa de moedas no cinto. Luz de contorno quente vinda da esquerda (sol da vila).
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pintor import Tela

W, H = 64, 104
P = {
    "4": "#120c14",
    # tecido escuro (capa, capuz, calça): escuro, base, claro, contorno de luz quente
    "A": "#191422", "B": "#272035", "C": "#3b3150", "D": "#c0703c",
    # couro
    "E": "#2e1a0e", "F": "#4e301a", "G": "#714624", "H": "#a06a38",
    # carmesim (cachecol)
    "I": "#3e0d1a", "J": "#6e1a28", "K": "#9a2b36", "L": "#d0503f",
    # metal da adaga
    "M": "#4f4a58", "N": "#9a95a4", "O": "#e8e4ee",
    # dourado
    "P": "#7a4a18", "Q": "#d9a52c", "R": "#ffe08a",
    # faixas do antebraço
    "S": "#8a7258", "T": "#c9b08a",
    # olhos
    "U": "#ffd27a", "V": "#ff8a3c",
}
RAMPAS = {  # parte -> (escuro, base, claro, borda iluminada)
    "capa": "ABCD", "capuz": "ABCD", "calca": "ABCB", "manga": "ABCD",
    "couro": "EFGH", "bota": "EFGH", "cinto": "EEFG", "bolsa": "EFGH",
    "cachecol": "IJKL", "luva": "EFFG",
}
pecas = []   # (nome, rampa, pontos) em ordem de trás para frente
t = Tela(W, H)
def parte(nome, rampa, pts):
    pecas.append((nome, rampa, set(pts)))

def poly(pts):
    tmp = Tela(W, H); return tmp.poly(pts, "x")
def elip(cx, cy, rx, ry):
    tmp = Tela(W, H); return tmp.elipse(cx, cy, rx, ry, "x")

# capa (atrás), abrindo para baixo com uma ponta esvoaçando para a esquerda
parte("capa", "capa", poly([(21, 28), (44, 28), (50, 70), (54, 96), (44, 99), (30, 97), (16, 99), (6, 94), (12, 70), (17, 40)]))
# cachecol esvoaçando (atrás do corpo)
parte("cauda", "cachecol", poly([(22, 31), (14, 33), (6, 38), (1, 44), (5, 45), (9, 41), (15, 39), (22, 37)]))
# pernas e botas
parte("pernaE", "calca", poly([(24, 64), (31, 64), (30, 88), (24, 88)]))
parte("pernaD", "calca", poly([(33, 64), (40, 64), (41, 88), (34, 88)]))
parte("botaE", "bota", poly([(23, 86), (31, 86), (31, 99), (34, 101), (22, 101)]))
parte("botaD", "bota", poly([(33, 86), (42, 86), (42, 97), (47, 99), (47, 101), (33, 101)]))
# tronco (colete de couro), cinto e bolsa de moedas
parte("tronco", "couro", poly([(22, 32), (43, 32), (42, 50), (40, 64), (24, 64), (22, 50)]))
parte("cinto", "cinto", poly([(22, 59), (42, 59), (42, 63), (22, 63)]))
parte("bolsa", "bolsa", elip(43.5, 67, 4.5, 5.5))
# braço esquerdo (do observador): pendurado, segurando a adaga
parte("mangaE", "manga", poly([(17, 33), (23, 33), (23, 50), (16, 50)]))
parte("anteE", "manga", poly([(16, 49), (23, 49), (22, 60), (16, 60)]))
parte("maoE", "luva", elip(19, 62, 3.5, 3))
# braço direito: dobrado, mão na bolsa
parte("mangaD", "manga", poly([(41, 33), (47, 34), (48, 48), (42, 49)]))
parte("anteD", "manga", poly([(42, 47), (48, 47), (46, 59), (41, 58)]))
parte("maoD", "luva", elip(43, 60, 3, 2.5))
# cachecol no pescoço (cobre a parte de baixo do rosto)
parte("cachecol", "cachecol", poly([(24, 20), (43, 20), (44, 30), (40, 35), (24, 35), (21, 30)]))
# capuz: arredondado, com a ponta caindo para trás (esquerda)
parte("capuz", "capuz", elip(33, 17, 12, 13) + poly([(22, 10), (13, 22), (16, 30), (24, 26)]))

# composição com sombreamento por parte: luz da esquerda/cima, sombra à direita/baixo
dono = {}
for i, (nome, rampa, pts) in enumerate(pecas):
    for p in pts: dono[p] = i
for (x, y), i in dono.items():
    nome, rampa, _ = pecas[i]
    esc, base, clr, borda = RAMPAS[rampa]
    viz = lambda dx, dy: dono.get((x + dx, y + dy)) == i
    c = base
    fora_esq = (x - 1, y) not in dono   # luz quente só na borda externa da silhueta
    if fora_esq and rampa in ("capa", "capuz", "manga"): c = borda
    elif not viz(-1, 0): c = clr
    elif not viz(-2, 0) or not viz(0, -1): c = clr
    elif not viz(1, 0) or not viz(0, 1) or not viz(2, 0): c = esc
    if nome == "capa" and y > 80 and c == base: c = esc if (x + y) % 9 else base   # barra da capa mais escura
    t.px(x, y, c)

# dobras da capa
for (x0, y0, x1, y1) in ((14, 74, 11, 95), (49, 72, 51, 96), (19, 80, 17, 97)):
    t.linha(x0, y0, x1, y1, "A")
# rosto na sombra do capuz e olhos brilhando
for (x, y) in elip(35, 16.5, 6.5, 5):
    if t.get(x, y) not in "IJKL": t.px(x, y, "4")
for (x, y, c) in ((31, 17, "U"), (32, 17, "U"), (31, 18, "V"), (37, 17, "U"), (38, 17, "U"), (38, 18, "V")):
    t.px(x, y, c)
# borda do capuz iluminada em volta do rosto (lado esquerdo)
for y in range(12, 24):
    for x in range(26, 32):
        if t.get(x, y) == "4" and t.get(x - 1, y) in "ABC": t.px(x - 1, y, "C")
# dobra do cachecol e brilho
t.linha(25, 29, 40, 29, "J"); t.linha(27, 21, 33, 21, "L"); t.linha(26, 25, 41, 25, "J")
# tiras cruzadas no colete (bandoleira) com bainhas
t.linha(23, 34, 41, 57, "E", 2)
for (x, y) in ((27, 39), (31, 44), (35, 49)):
    t.px(x, y, "N"); t.px(x + 1, y, "M")
# fivela dourada do cinto
t.rect(30, 59, 34, 63, "P"); t.rect(31, 60, 33, 62, "Q"); t.px(31, 60, "R")
# bolsa de moedas: amarração e moeda aparecendo
t.rect(40, 61, 47, 62, "E"); t.elipse(45, 64.5, 1.8, 1.6, "Q"); t.px(44, 63, "R")
t.px(42, 68, "H"); t.px(41, 70, "G")
# faixas no antebraço esquerdo
for y in (51, 54, 57):
    t.rect(16, y, 22, y, "T"); t.rect(16, y + 1, 22, y + 1, "S")
# adaga em pegada invertida: lâmina para baixo, guarda dourada
t.rect(17, 64, 21, 65, "Q"); t.px(17, 64, "R")
for y in range(66, 82):
    w_ = 2 if y < 78 else 1
    t.rect(19 - (1 if y < 78 else 0), y, 19 + w_ - 1, y, "N")
    t.px(18 if y < 78 else 19, y, "O")
    t.px(20 if y < 78 else 19, y, "M") if y < 78 else None
t.px(19, 82, "M")
# fivelas das botas
t.px(27, 92, "Q"); t.px(38, 92, "Q")

t.contorno("4")
src = t.fonte("heroi-assassino", P)
json.dump(src, open(sys.argv[1], "w"), indent=0)
print("cores:", len(src["palette"]))
