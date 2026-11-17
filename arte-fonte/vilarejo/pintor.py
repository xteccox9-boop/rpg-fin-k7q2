# Pequeno "pincel" de pixel art: tela de caracteres (formato de grade da pixel-art-studio).
import math, random

class Tela:
    def __init__(s, w, h):
        s.w, s.h = w, h
        s.g = [["." for _ in range(w)] for _ in range(h)]

    def px(s, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < s.w and 0 <= y < s.h and c:
            s.g[y][x] = c

    def get(s, x, y):
        return s.g[y][x] if 0 <= x < s.w and 0 <= y < s.h else "."

    def rect(s, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                s.px(x, y, c)

    def poly(s, pts, c, mask=None):
        """Preenche o polígono pelos centros dos pixels. c pode ser função (x, y) -> char."""
        ys = [p[1] for p in pts]
        out = []
        for y in range(max(0, int(min(ys))), min(s.h, int(max(ys)) + 1)):
            cy = y + .5
            xs = []
            n = len(pts)
            for i in range(n):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
                if (y0 <= cy < y1) or (y1 <= cy < y0):
                    xs.append(x0 + (cy - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                for x in range(max(0, math.ceil(a - .5)), min(s.w, math.floor(b - .5) + 1)):
                    out.append((x, y))
                    s.px(x, y, c(x, y) if callable(c) else c)
        return out

    def elipse(s, cx, cy, rx, ry, c):
        out = []
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                    out.append((x, y))
                    s.px(x, y, c(x, y) if callable(c) else c)
        return out

    def linha(s, x0, y0, x1, y1, c, larg=1):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) or 1
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
            for dx in range(larg):
                for dy in range(larg):
                    s.px(round(x - larg / 2 + dx + .5), round(y - larg / 2 + dy + .5), c)

    def contorno(s, cor, alvo=None):
        """Contorno de 1 px em volta dos pixels opacos (ou só dos chars em `alvo`)."""
        op = [[(s.g[y][x] != "." and (alvo is None or s.g[y][x] in alvo)) for x in range(s.w)] for y in range(s.h)]
        for y in range(s.h):
            for x in range(s.w):
                if s.g[y][x] == "." and any(0 <= x + a < s.w and 0 <= y + b < s.h and op[y + b][x + a]
                                            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    s.g[y][x] = cor

    def fonte(s, nome, paleta):
        usadas = sorted({ch for r in s.g for ch in r if ch != "."})
        falta = [c for c in usadas if c not in paleta]
        if falta:
            raise SystemExit("cores sem paleta: " + "".join(falta))
        return {"version": 1, "name": nome, "canvas": [s.w, s.h],
                "palette": {k: paleta[k] for k in usadas},
                "frames": [{"name": nome, "duration_ms": 100, "rows": ["".join(r) for r in s.g]}]}

def dither(x, y, t):
    """Bayer 4x4: True quando o limiar t (0..1) cobre este pixel."""
    b = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    return (b[y % 4][x % 4] + .5) / 16 < t
