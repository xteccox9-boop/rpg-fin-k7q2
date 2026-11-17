# Aplica a vila, o herói e o retrato no controle-gastos.html (só trechos do Vilarejo).
import base64, io, re, sys
from PIL import Image

html_path, vila_png, heroi_png = sys.argv[1], sys.argv[2], sys.argv[3]
b64 = lambda im: base64.b64encode(im).decode()
def png_bytes(im):
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); return buf.getvalue()

html = open(html_path, "rb").read().decode("utf-8")

# 1) fundo: troca o data URI do .homebg pela vila
vila = open(vila_png, "rb").read()
pat = re.compile(r'(<div class="homebg" style="background-image:url\()data:image/\w+;base64,[A-Za-z0-9+/=]+(\)")')
html, n = pat.subn(lambda m: m.group(1) + "data:image/png;base64," + b64(vila) + m.group(2), html)
assert n == 1, "homebg: %d" % n

# 2) herói no palco (antes do quadro "Posso gastar"), com sombra
heroi = open(heroi_png, "rb").read()
marca = '<div class="sign">'
assert html.count(marca) == 1
tag = ('<i class="vsombra" aria-hidden="true"></i>'
       '<img class="vheroi" alt="Seu herói, um assassino encapuzado" src="data:image/png;base64,' + b64(heroi) + '">')
if 'class="vheroi"' not in html:
    html = html.replace(marca, tag + marca, 1)

# 3) retrato: busto do herói dentro da moldura do cabeçalho
im = Image.open(heroi_png).convert("RGBA")
busto = im.crop((21, 6, 49, 34))            # rosto: capuz, olhos e máscara
retr = png_bytes(busto)
marca2 = '<div class="retr"><img src="'
pat2 = re.compile(r'(<img class="retrHeroi" alt="" src=")data:image/png;base64,[A-Za-z0-9+/=]+(")')
if pat2.search(html):
    html = pat2.sub(lambda m: m.group(1) + "data:image/png;base64," + b64(retr) + m.group(2), html, 1)
else:
    assert html.count(marca2) == 1
    html = html.replace(marca2, '<div class="retr"><img class="retrHeroi" alt="" src="data:image/png;base64,' + b64(retr) + '"><img src="', 1)

open(html_path, "wb").write(html.encode("utf-8"))
print("ok; vila", len(vila), "B; herói", len(heroi), "B; retrato", len(retr), "B; arquivo", len(html.encode("utf-8")), "B")
