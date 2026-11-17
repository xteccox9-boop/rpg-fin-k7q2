# Gera a grade editável (formato pixel-art-studio, version 1) do ícone "escudo da Guilda", 128x128.
# Luz do topo-esquerdo, contorno escuro contínuo, rampas com sombra deslocada no matiz.
import json, math, sys
from collections import deque

W = H = 128
C = 63.5           # centro horizontal
TOP, TIP = 12, 120 # topo e ponta
HW = 46            # meia-largura
YS = 56            # onde os lados começam a fechar

PAL = {
    "o": "#17110c",  # contorno
    # dourado (mesma família da moeda do Vilarejo)
    "1": "#4a2a10", "2": "#7a4a18", "3": "#b37c26", "4": "#d9a52c", "5": "#f9dd68", "6": "#fff3b0",
    # carmesim (sombra puxada para o roxo, luz para o laranja)
    "a": "#2c0a1a", "b": "#4d1022", "c": "#7a1f2e", "d": "#9a2b36", "e": "#c4473f",
    # madeira da flecha
    "w": "#3d2412", "x": "#6d3e17", "y": "#a0703c",
    # penas
    "p": "#e0c796", "q": "#fbf3d2", "r": "#8a1a1a",
    "k": "#3a1a08",  # linha escura entre ouro e carmesim
}

def dentro(x, y):
    px, py = x + .5, y + .5
    if py < TOP or py > TIP: return False
    dx = abs(px - C)
    topo = TOP + 3.0 * (dx / HW) ** 2          # cantos de cima levemente mais baixos
    if py < topo: return False
    if py <= YS: return dx <= HW
    t = (py - YS) / (TIP - YS)
    return dx <= HW * (1 - t ** 1.8)            # lados fecham numa ponta

mask = [[dentro(x, y) for x in range(W)] for y in range(H)]

# distância (Chebyshev) até a borda, de dentro
INF = 999
dist = [[INF if mask[y][x] else 0 for x in range(W)] for y in range(H)]
q = deque((x, y) for y in range(H) for x in range(W) if not mask[y][x])
while q:
    x, y = q.popleft()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and dist[ny][nx] > dist[y][x] + 1:
                dist[ny][nx] = dist[y][x] + 1; q.append((nx, ny))

g = [["." for _ in range(W)] for _ in range(H)]
CY = 62  # centro vertical aproximado (para a luz)

def luz(x, y):
    nx, ny = (x + .5 - C), (y + .5 - CY)
    n = math.hypot(nx, ny) or 1
    return (-nx * -.7071 + -ny * -.7071) / n * -1  # >0 = virado para o topo-esquerdo

RIM = 8
for y in range(H):
    for x in range(W):
        d = dist[y][x]
        if d == 0: continue
        L = luz(x, y)
        if d <= RIM:  # aro dourado com chanfro
            if d == RIM: ch = "k"
            elif d == RIM - 1: ch = "2" if L < .2 else "3"
            elif d <= 2: ch = "6" if L > .55 else "5" if L > .1 else "4" if L > -.4 else "3"
            else: ch = "5" if L > .45 else "4" if L > -.2 else "3" if L > -.65 else "2"
        else:  # campo carmesim: metade esquerda iluminada, direita em sombra
            esq = x + .5 < C
            ch = "c" if esq else "b"
            if d <= RIM + 2:
                ch = "e" if (L > .45) else ("a" if L < -.3 else ch)
            elif esq and d <= RIM + 5 and L > .6: ch = "d"
            if not esq and abs(x + .5 - C) < 1.5: ch = "a"   # dobra central
            if esq and 0 < C - (x + .5) < 3: ch = "d"        # brilho na dobra
        g[y][x] = ch

# emblema: alvo dourado (3 anéis) no campo
EX, EY = C, 60
def ouro(xx, yy, cx, cy):
    L = (-(xx + .5 - cx) - (yy + .5 - cy))
    return "6" if L > 9 else "5" if L > 2 else "4" if L > -5 else "3"
for y in range(H):
    for x in range(W):
        if dist[y][x] <= RIM + 1: continue
        r = math.hypot(x + .5 - EX, y + .5 - EY)
        if 22.5 <= r < 27.5 or 12.5 <= r < 16.5 or r < 6.5: g[y][x] = ouro(x, y, EX, EY)
        elif 21.5 <= r < 22.5 or 27.5 <= r < 28.5 or 11.5 <= r < 12.5 or 16.5 <= r < 17.5 or 6.5 <= r < 7.5:
            g[y][x] = "k"

# flecha: haste do canto superior direito até o centro do alvo, penas saindo pela borda
# geometria ao longo da haste: u = distância a partir da cauda, v = afastamento lateral
TX, TY = 108.5, 15.5                    # cauda (fora do escudo, em cima à direita)
HX, HY = 64.0, 60.0                     # ponta cravada no centro do alvo
LEN = math.hypot(HX - TX, HY - TY)
DX, DY = (HX - TX) / LEN, (HY - TY) / LEN
PX_, PY_ = -DY, DX                       # perpendicular (v<0 = lado de cima/esquerda, iluminado)
def uv(x, y):
    rx, ry = x + .5 - TX, y + .5 - TY
    return rx * DX + ry * DY, rx * PX_ + ry * PY_
def larg_pena(u):
    if u < 2 or u > 18: return 0
    return min(7.5, 4 + (u - 2) * 1.2) if u < 6 else 7.5 - max(0, u - 13) * 0.9
def eh_pena(x, y):
    u, v = uv(x, y); return 1.5 < abs(v) <= larg_pena(u)
def eh_haste(x, y):
    u, v = uv(x, y); return -0.5 <= u <= LEN - 3 and abs(v) <= 1.6
flecha = [[eh_pena(x, y) or eh_haste(x, y) for x in range(W)] for y in range(H)]
for y in range(H):              # contorno de 1 px em volta da flecha inteira
    for x in range(W):
        if not flecha[y][x] and any(0 <= x + a < W and 0 <= y + b < H and flecha[y + b][x + a]
                                    for a in (-1, 0, 1) for b in (-1, 0, 1)):
            g[y][x] = "o"
for y in range(H):
    for x in range(W):
        if not flecha[y][x]: continue
        u, v = uv(x, y)
        if eh_haste(x, y) and abs(v) <= 1.6:
            g[y][x] = "y" if v < -.5 else ("x" if v <= .5 else "w")
        else:   # penas: lado de cima claro, de baixo em meio-tom, faixa vermelha e barbas
            ch = ("q" if abs(v) < 5 else "p") if v < 0 else "p"
            if 8 <= u <= 10.5: ch = "r"
            elif v > 0 and abs(v) > 5: ch = "y"
            elif int(u) % 4 == 0 and abs(v) > 3: ch = "p" if v < 0 else "y"
            g[y][x] = ch
# ponta cravada: um furo escuro no centro do alvo
for (a, b) in ((0, 0), (1, 0), (0, 1), (1, 1)):
    g[59 + b][63 + a] = "o"

# rebites no aro
for (x, y) in [(int(C) - 30, 17), (int(C) + 30, 17), (int(C), 15), (21, 40), (105, 40), (24, 72), (102, 72), (int(C) - 13, 104), (int(C) + 13, 104)]:
    if not (0 < x < W - 2 and 0 < y < H - 2) or g[y][x] == "." or dist[y][x] > RIM: continue
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            g[y + dy][x + dx] = "2"
    g[y][x] = "4"; g[y - 1][x - 1] = "6"; g[y + 1][x + 1] = "1"

# contorno externo contínuo (2 px) em volta de tudo que for opaco
op = [[g[y][x] != "." for x in range(W)] for y in range(H)]
for y in range(H):
    for x in range(W):
        if op[y][x]: continue
        if any(0 <= x + dx < W and 0 <= y + dy < H and op[y + dy][x + dx]
               for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2) if max(abs(dx), abs(dy)) <= 2 and abs(dx) + abs(dy) <= 3):
            g[y][x] = "o"

usadas = sorted({ch for row in g for ch in row if ch != "."})
src = {"version": 1, "name": "escudo-guilda", "canvas": [W, H],
       "palette": {k: PAL[k] for k in usadas},
       "frames": [{"name": "escudo", "duration_ms": 100, "rows": ["".join(r) for r in g]}],
       "pivot": [64, 64]}
json.dump(src, open(sys.argv[1], "w"), indent=1)
print("cores:", len(usadas), "opacos:", sum(ch != "." for row in g for ch in row))
