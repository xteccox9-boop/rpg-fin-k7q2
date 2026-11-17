# Navegação inferior da Taverna: moldura de madeira 9-fatias (normal e selecionada) e 5 ícones 16x16,
# no formato de grade da pixel-art-studio. Exibidos em 2x. Fundo transparente.
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vilarejo"))
from pintor import Tela

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
P = {
    "o": "#140c08",                                   # contorno
    "a": "#24150b", "b": "#2e1c10", "c": "#3a2414", "d": "#4a2e18",   # madeira escura
    "1": "#5a3410", "2": "#8a5a1e", "3": "#c08a3a", "4": "#e8bc5c", "5": "#fff0b0",  # bronze -> ouro
    "y": "#ffd27a", "Y": "#e0a830", "g": "#a8741c",
    "w": "#8a5a2c", "W": "#5a361a", "v": "#b07840",
    "r": "#c43a2a", "R": "#7a1818", "e": "#6bbf4a", "E": "#357a2a", "b2": "#000",
    "B": "#5a8ac8", "N": "#2e4a7a", "p": "#f0dcb0", "q": "#c8a878", "h": "#fff6d8", "i": "#9a95a4",
}
P.pop("b2")

# ---------- moldura 18x18 (fatias de 6) ----------
def moldura(sel):
    S = 18; t = Tela(S, S)
    aro = ("3", "4", "5") if sel else ("1", "2", "3")     # escuro, médio, brilho do aro
    for y in range(S):
        for x in range(S):
            borda = min(x, y, S - 1 - x, S - 1 - y)
            if borda == 0: c = "o"
            elif borda == 1: c = aro[2] if (x == 1 or y == 1) else aro[0]   # luz no topo/esquerda
            elif borda == 2: c = aro[1]
            elif borda == 3: c = "o"
            else:                                                            # madeira com veio
                c = "b" if (y // 3) % 2 else "c"
                if (x * 7 + y * 3) % 11 == 0: c = "a"
                if y == 4: c = "d"
            t.px(x, y, c)
    # cantos ornamentados: losango de bronze/ouro com brilho
    for (cx, cy) in ((2, 2), (S - 3, 2), (2, S - 3), (S - 3, S - 3)):
        for (dx, dy) in ((0, -1), (-1, 0), (1, 0), (0, 1), (0, 0)):
            t.px(cx + dx, cy + dy, aro[1])
        t.px(cx, cy, "5" if sel else "4"); t.px(cx - 1, cy - 1, "o"); t.px(cx + 1, cy + 1, "o")
    # recorte de canto em degrau (pixel) para não ficar retângulo seco
    for (x, y) in ((0, 0), (S - 1, 0), (0, S - 1), (S - 1, S - 1)):
        t.px(x, y, ".")
    return t

# ---------- ícones 16x16 ----------
ICONES = {
 "categorias": [
  "................",
  "............ooo.",
  "............oyo.",
  "........ooo.oyo.",
  "........oeo.oyo.",
  "........oeo.oYo.",
  "....ooo.oeo.oYo.",
  "....oro.oEo.oYo.",
  "ooo.oro.oEo.oYo.",
  "oBo.oro.oEo.oYo.",
  "oBo.oRo.oEo.ogo.",
  "oNo.oRo.oEo.ogo.",
  "oooooooooooooooo",
  "oWwwwwwwwwwwwwWo",
  "oooooooooooooooo",
  "................"],
 "dia": [
  "................",
  "...oio....oio...",
  "..ooooooooooooo.",
  "..orrrRrrrrRrro.",
  "..orrrrrrrrrrro.",
  "..ooooooooooooo.",
  "..opqpqpqpqpqpo.",
  "..opppppppppppo.",
  "..opqpqpqprrrpo.",
  "..opppppppryrpo.",
  "..opqpqpqprrrpo.",
  "..opppppppppppo.",
  "..opqpqpqpqpqpo.",
  "..oqqqqqqqqqqqo.",
  "..ooooooooooooo.",
  "................"],
 "metas": [
  "................",
  "................",
  ".oooooooooooooo.",
  ".ovvvvvYYvvvvvo.",
  ".owwwwwYYwwwwwo.",
  ".owwwwwYYwwwwwo.",
  ".oYYYYYYYYYYYYo.",
  ".ooooooyyoooooo.",
  ".owwwwoyyowwwwo.",
  ".owwwwoRRowwwwo.",
  ".owwwwwoowwwwwo.",
  ".oYwwwwwwwwwwYo.",
  ".oYWWWWWWWWWWYo.",
  ".oooooooooooooo.",
  "................",
  "................"],
 "relatorios": [
  "................",
  "................",
  ".oo..........oo.",
  ".ovoooooooooovo.",
  ".ovppppppppqqvo.",
  ".ovpqqqqqqppqvo.",
  ".ovpppppppppqvo.",
  ".ovpqqqqqpppqvo.",
  ".ovpppppprrpqvo.",
  ".ovpqqqpprRpqvo.",
  ".ovpppppppppqvo.",
  ".ovqqqqqqqqqqvo.",
  ".ovoooooooooovo.",
  ".oo..........oo.",
  "................",
  "................"],
}
def pizza():
    t = Tela(16, 16); cx, cy, r = 7.5, 7.5, 6.6
    fatias = [(0, 150, "Y", "y"), (150, 240, "R", "r"), (240, 310, "E", "e"), (310, 360, "N", "B")]
    for y in range(16):
        for x in range(16):
            dx, dy = x + .5 - cx, y + .5 - cy; d = math.hypot(dx, dy)
            if d <= r:
                ang = (math.degrees(math.atan2(dy, dx)) + 90) % 360
                for a0, a1, esc, clr in fatias:
                    if a0 <= ang < a1:
                        t.px(x, y, clr if (dx < 0 and dy < 0) or d < r * .5 else esc)
    for y in range(16):          # linhas entre fatias e contorno externo
        for x in range(16):
            if t.get(x, y) != "." and any(t.get(x + a, y + b) == "." for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                pass
    t.contorno("o")
    t.px(7, 7, "h")
    return t

def grade(nome, linhas):
    t = Tela(16, 16)
    for y, row in enumerate(linhas):
        assert len(row) == 16, (nome, y, len(row))
        for x, ch in enumerate(row):
            if ch != ".": t.px(x, y, ch)
    return t

def src(nome, telas):
    w, h = telas[0][1].w, telas[0][1].h
    usadas = sorted({ch for _, tl in telas for r in tl.g for ch in r if ch != "."})
    return {"version": 1, "name": nome, "canvas": [w, h], "palette": {k: P[k] for k in usadas},
            "frames": [{"name": n, "duration_ms": 100, "rows": ["".join(r) for r in tl.g]} for n, tl in telas]}

json.dump(src("moldura", [("normal", moldura(False)), ("selecionada", moldura(True))]), open(os.path.join(OUT, "moldura-source.json"), "w"), indent=0)
icones = [("categorias", grade("categorias", ICONES["categorias"])), ("dia", grade("dia", ICONES["dia"])),
          ("resumo", pizza()), ("metas", grade("metas", ICONES["metas"])), ("relatorios", grade("relatorios", ICONES["relatorios"]))]
json.dump(src("icones", icones), open(os.path.join(OUT, "icones-source.json"), "w"), indent=0)
print("ok")
