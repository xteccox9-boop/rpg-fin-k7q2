# Lacres de cera (28x28) para os ícones da navegação da Taverna: normal (cera vermelha) e selecionado
# (cera mais viva com anel dourado). Borda irregular de cera derretida, relevo interno e luz do topo-esquerdo.
import json, math, os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vilarejo"))
from pintor import Tela

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
P = {"o": "#1a0606",
     "a": "#4a0a0e", "b": "#6e1216", "c": "#93201e", "d": "#b8342a", "e": "#dc5a44", "f": "#f48a6a",
     "A": "#5a3a08", "B": "#a8741c", "C": "#e8b84a", "D": "#fff0a8"}
S, CX, CY = 28, 13.5, 13.5
random.seed(11)
# raio irregular por ângulo (cera derretida) + duas gotas escorridas
ondas = [(random.uniform(.4, 1.0), random.randint(5, 9), random.uniform(0, 6.28)) for _ in range(3)]
def raio(ang):
    r = 11.6 + sum(a * math.sin(k * ang + f) for a, k, f in ondas) * .55
    for gota in (2.2, 4.1):                            # gotas embaixo
        d = abs((ang - gota + math.pi) % (2 * math.pi) - math.pi)
        if d < .22: r += 1.6 * (1 - d / .22)
    return min(r, 13.4)

def selo(sel):
    t = Tela(S, S)
    for y in range(S):
        for x in range(S):
            dx, dy = x + .5 - CX, y + .5 - CY; d = math.hypot(dx, dy); ang = math.atan2(dy, dx)
            R = raio(ang)
            if d > R: continue
            luz = (-dx - dy) / (d + .01)                 # >0 virado para o topo-esquerdo
            borda = R - d
            if borda < 1.2: c = "b" if luz < 0 else "c"   # beirada da cera
            elif 8.6 < d < 10.2: c = "a" if luz > 0 else "e"   # anel em baixo-relevo (sombra/luz invertidas)
            elif d <= 8.6: c = "c" if luz < .3 else "d"   # miolo liso onde fica o ícone
            else: c = "e" if luz > .45 else ("d" if luz > -.3 else "c")
            if sel:
                c = {"b": "c", "c": "d", "d": "e", "e": "f"}.get(c, c)
                if 8.6 < d < 10.2: c = "C" if luz > 0 else "B"
            t.px(x, y, c)
    # brilho especular da cera
    for (x, y) in ((8, 6), (9, 6), (7, 7), (8, 7)):
        if t.get(x, y) != ".": t.px(x, y, "f" if not sel else "D")
    t.contorno("o")
    return t

telas = [("normal", selo(False)), ("selecionado", selo(True))]
usadas = sorted({ch for _, tl in telas for r in tl.g for ch in r if ch != "."})
src = {"version": 1, "name": "selos", "canvas": [S + 2, S + 2], "palette": {k: P[k] for k in usadas},
       "frames": []}
for n, tl in telas:            # 1 px de margem para o contorno
    rows = ["." * (S + 2)] + ["." + "".join(r) + "." for r in tl.g] + ["." * (S + 2)]
    src["frames"].append({"name": n, "duration_ms": 100, "rows": rows})
json.dump(src, open(os.path.join(OUT, "selos-source.json"), "w"), indent=0)
print("ok")
