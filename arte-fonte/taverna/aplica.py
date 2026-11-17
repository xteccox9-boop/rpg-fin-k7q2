# Aplica na Taverna: cena nova do cabeçalho (com título em texto real) e quadros de madeira em pixel art.
import base64, re, sys
from urllib.parse import quote
html_path, cab_png = sys.argv[1], sys.argv[2]
html = open(html_path, "rb").read().decode("utf-8")
b64 = base64.b64encode(open(cab_png, "rb").read()).decode()

# 1) cabeçalho: troca a imagem e põe o título como texto por cima da placa
pat = re.compile(r'<div class="tvhead"><img alt="A Taverna" src="data:image/\w+;base64,[A-Za-z0-9+/=]+">(<b class="tvtit">A Taverna</b>)?</div>')
novo = '<div class="tvhead"><img alt="" src="data:image/png;base64,' + b64 + '"><b class="tvtit">A Taverna</b></div>'
html, n = pat.subn(novo, html)
assert n == 1, "tvhead: %d" % n

# 2) CSS: madeira em pixel art (tábuas + cantoneiras de ferro) só na Taverna
def svg(attrs, corpo):
    s = '<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges" ' + attrs + '>' + corpo + '</svg>'
    return 'url("data:image/svg+xml,' + quote(s, safe="") + '")'
TAB = svg('width="96" height="32"',
    '<rect width="96" height="32" fill="#2e1c10"/><rect y="16" width="96" height="16" fill="#29180c"/>'
    '<rect width="96" height="2" fill="#3d2614"/><rect y="16" width="96" height="2" fill="#382312"/>'
    '<rect y="14" width="96" height="2" fill="#140a05"/><rect y="30" width="96" height="2" fill="#140a05"/>'
    '<rect x="62" width="2" height="14" fill="#140a05"/><rect x="64" width="2" height="14" fill="#3a2413"/>'
    '<rect x="28" y="16" width="2" height="14" fill="#140a05"/><rect x="30" y="16" width="2" height="14" fill="#352111"/>'
    '<rect x="8" y="6" width="14" height="2" fill="#22140a"/><rect x="40" y="10" width="10" height="2" fill="#3a2413"/>'
    '<rect x="72" y="4" width="12" height="2" fill="#22140a"/><rect x="4" y="22" width="10" height="2" fill="#352111"/>'
    '<rect x="48" y="24" width="16" height="2" fill="#22140a"/><rect x="80" y="20" width="4" height="4" fill="#1a0e07"/>'
    '<rect x="82" y="20" width="2" height="2" fill="#3d2614"/>')
L = ('<rect width="24" height="8" fill="#120c14"/><rect width="8" height="24" fill="#120c14"/>'
     '<rect width="22" height="6" fill="#55505c"/><rect width="6" height="22" fill="#55505c"/>'
     '<rect width="22" height="2" fill="#9a95a4"/><rect width="2" height="22" fill="#9a95a4"/>'
     '<rect width="6" height="6" fill="#77707e"/>'
     '<rect x="12" y="2" width="4" height="4" fill="#24212a"/><rect x="12" y="2" width="2" height="2" fill="#e0dae6"/>'
     '<rect x="2" y="12" width="4" height="4" fill="#24212a"/><rect x="2" y="12" width="2" height="2" fill="#e0dae6"/>')
canto = lambda tr: svg('width="24" height="24"', '<g transform="' + tr + '">' + L + '</g>')
CTL, CTR = canto(""), canto("translate(24,0) scale(-1,1)")
CBL, CBR = canto("translate(0,24) scale(1,-1)"), canto("translate(24,24) scale(-1,-1)")

css = f"""/* ===== Taverna em pixel art: cena do cabeçalho com título em texto e quadros de tábua com cantoneiras de ferro ===== */
#tav{{--tvTab:{TAB};--tvCTL:{CTL};--tvCTR:{CTR};--tvCBL:{CBL};--tvCBR:{CBR}}}
#tav .tvhead{{max-height:none!important;overflow:visible!important;margin:0 -10px 4px!important}}
#tav .tvhead img{{margin:0!important;image-rendering:pixelated;image-rendering:crisp-edges;-webkit-mask-image:linear-gradient(#000 88%,transparent);mask-image:linear-gradient(#000 88%,transparent)}}
#tav .tvtit{{position:absolute;left:49.7%;top:43%;transform:translate(-50%,-50%);font:400 31px/1 "Jacquard 12",Cinzel,serif;color:#ffd98a;white-space:nowrap;letter-spacing:.01em;
 text-shadow:0 2px 0 #120c14,0 -2px 0 #120c14,2px 0 0 #120c14,-2px 0 0 #120c14,0 4px 0 rgba(0,0,0,.5),0 0 10px rgba(255,180,80,.35);pointer-events:none}}
#tav .tvp{{border:0!important;border-radius:0!important;padding:14px 14px 12px!important;
 background:var(--tvCTL) 4px 4px/20px 20px no-repeat,var(--tvCTR) calc(100% - 4px) 4px/20px 20px no-repeat,var(--tvCBL) 4px calc(100% - 4px)/20px 20px no-repeat,var(--tvCBR) calc(100% - 4px) calc(100% - 4px)/20px 20px no-repeat,var(--tvTab) 0 0/96px 32px,#2e1c10!important;
 box-shadow:inset 0 0 0 2px #120c14,inset 0 0 0 4px #8a5a2c,inset 0 0 0 6px #5a361a,inset 0 0 0 8px #120c14,inset 0 12px 16px rgba(0,0,0,.45),0 -2px 0 #120c14,0 2px 0 #120c14,-2px 0 0 #120c14,2px 0 0 #120c14,0 6px 0 rgba(0,0,0,.45)!important}}
#tav .tvcols .tvp{{padding:14px 10px 12px!important}}
#tav .tvm,#tav .tvnav>button{{border:0!important;border-radius:0!important;background:var(--tvTab) 0 0/96px 32px,#2e1c10!important;
 box-shadow:inset 0 0 0 2px #120c14,inset 0 0 0 4px #8a5a2c,inset 0 0 0 6px #120c14,0 -2px 0 #120c14,0 2px 0 #120c14,-2px 0 0 #120c14,2px 0 0 #120c14,0 4px 0 rgba(0,0,0,.45)!important}}
#tav .tvnav>button{{color:#ffd98a!important}}
#tav .tvnav>button:active{{transform:translateY(2px)}}
/* ===== fim Taverna ===== */
"""
ini = html.find("/* ===== Taverna em pixel art")
if ini >= 0:   # reaplicar: troca o bloco anterior
    fim = html.index("/* ===== fim Taverna ===== */\n", ini) + len("/* ===== fim Taverna ===== */\n")
    html = html[:ini] + css + html[fim:]
else:
    i = html.index("</style>")
    html = html[:i] + css + html[i:]
open(html_path, "wb").write(html.encode("utf-8"))
print("ok; cabeçalho", len(b64), "B base64; arquivo", len(html.encode("utf-8")), "B")
