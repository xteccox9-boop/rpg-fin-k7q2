# Recorta o último balão (branco, canto inferior direito) do baloes.png em duas peças:
#  - corpo: 50x38, com o vão do rabinho fechado (serve de border-image 9 fatias)
#  - rabo: 11x13 (colunas 8-18, linhas 33-45 do balão), sobreposto no canto inferior esquerdo
import os, sys
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(AQUI, "baloes.png")).convert("RGBA")
b = im.crop((182, 180, 243, 239)); b = b.crop(b.getbbox())      # 50x46
assert b.size == (50, 46), b.size
corpo = b.crop((0, 0, 50, 38))
# fecha o vão: copia o trecho reto da borda de baixo (colunas 25-35) para as colunas 8-18
remendo = corpo.crop((25, 33, 36, 38))
corpo.paste(remendo, (8, 33))
rabo = b.crop((8, 33, 19, 46))
corpo.save(os.path.join(AQUI, "balao-corpo.png"))
rabo.save(os.path.join(AQUI, "balao-rabo.png"))
prova = Image.new("RGBA", (50, 46)); prova.paste(corpo, (0, 0)); prova.alpha_composite(rabo, (8, 33))
print("igual ao original:", list(prova.getdata()) == list(b.getdata()))
