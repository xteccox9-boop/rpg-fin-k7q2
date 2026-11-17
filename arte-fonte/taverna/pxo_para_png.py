# Converte um projeto Pixelorama (.pxo v8, já extraído do zip) em PNGs por quadro + folha de sprites.
# Uso: python pxo_para_png.py <pasta_extraida> <pasta_saida>
import json, os, sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
d = json.load(open(os.path.join(src, "data.json"), encoding="utf-8"))
W, H = d["size_x"], d["size_y"]
n = len(d["frames"])
quadros = []
for i in range(1, n + 1):
    raw = open(os.path.join(src, "image_data", "frames", str(i), "layer_1"), "rb").read()
    assert len(raw) == W * H * 4, (i, len(raw))
    im = Image.frombytes("RGBA", (W, H), raw)
    im.save(os.path.join(out, "quadro-%02d.png" % i))
    quadros.append(im)
folha = Image.new("RGBA", (W, H * n))
for i, im in enumerate(quadros):
    folha.paste(im, (0, i * H))
folha.save(os.path.join(out, "folha.png"), optimize=True)
# diferenças entre quadros (para saber o que anima)
import itertools
dif = []
for a, b in zip(quadros, quadros[1:] + quadros[:1]):
    pa, pb = a.load(), b.load()
    dif.append(sum(1 for y in range(H) for x in range(W) if pa[x, y] != pb[x, y]))
cores = len(set(quadros[0].getdata()))
alfas = sorted({p[3] for p in quadros[0].getdata()})
print(json.dumps({"tamanho": [W, H], "quadros": n, "fps": d.get("fps"), "pixels_que_mudam_por_quadro": dif,
                  "cores_no_quadro_1": cores, "alfas": alfas[:6], "folha_bytes": os.path.getsize(os.path.join(out, "folha.png"))}))
# visualização ampliada 3x do quadro 1 e mosaico dos quadros
quadros[0].resize((W * 3, H * 3), Image.NEAREST).save(os.path.join(out, "quadro-01-3x.png"))
