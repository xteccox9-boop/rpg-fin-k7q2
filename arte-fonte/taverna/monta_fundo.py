# Monta o fundo animado da Taverna (APNG) a partir dos quadros extraídos do .pxo
# e recorta a placa "A Taverna" (com correntes) do cabeçalho antigo, com fundo transparente.
import os, sys
from PIL import Image

base = os.path.dirname(os.path.abspath(__file__))
fdir = os.path.join(base, "fundo")
quadros = [Image.open(os.path.join(fdir, "quadro-%02d.png" % i)).convert("RGBA") for i in range(1, 12)]
FPS = 6
# junta quadros repetidos em sequência, somando a duração
seq, dur = [], []
for q in quadros:
    if seq and q.tobytes() == seq[-1].tobytes():
        dur[-1] += 1000 // FPS
    else:
        seq.append(q); dur.append(1000 // FPS)
apng = os.path.join(fdir, "taverna-animada.png")
seq[0].save(apng, save_all=True, append_images=seq[1:], duration=dur, loop=0, optimize=True, disposal=0, blend=0)
quadros[0].save(os.path.join(fdir, "taverna-parada.png"), optimize=True)

# placa: borda/madeira (x 49..138, y 12..43) + as duas correntes acima dela
so = Image.open(os.path.join(base, "placa", "atlas.png")).convert("RGBA")   # render de placa-source.json
placa = so.crop(so.getbbox())
placa.save(os.path.join(fdir, "placa.png"), optimize=True)
print({"quadros_unicos": len(seq), "duracoes_ms": dur,
       "apng_bytes": os.path.getsize(apng), "parada_bytes": os.path.getsize(os.path.join(fdir, "taverna-parada.png")),
       "placa": placa.size, "placa_bytes": os.path.getsize(os.path.join(fdir, "placa.png"))})
