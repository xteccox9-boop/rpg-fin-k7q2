# Aplica o fundo animado da Taverna (vindo do projeto Pixelorama) e troca o cabeçalho pela placa sozinha.
import base64, os, re, sys
html_path = sys.argv[1]
base = os.path.dirname(os.path.abspath(__file__))
uri = lambda p: "data:image/png;base64," + base64.b64encode(open(os.path.join(base, "fundo", p), "rb").read()).decode()
html = open(html_path, "rb").read().decode("utf-8")

# 1) camada de fundo logo no início da Taverna
abre = '<div data-tab="gastos" id="tav">'
assert html.count(abre) == 1
if 'class="tavbg"' not in html:
    html = html.replace(abre, abre + '<div class="tavbg" aria-hidden="true"></div>', 1)

# 2) cabeçalho: só a placa pendurada (o título continua como texto por cima)
pat = re.compile(r'(<div class="tvhead"><img alt="" src=")data:image/png;base64,[A-Za-z0-9+/=]+(">)')
html, n = pat.subn(lambda m: m.group(1) + uri("placa.png") + m.group(2), html)
assert n == 1, "tvhead: %d" % n

# 3) CSS (bloco substituível)
css = f"""/* ===== Taverna: fundo animado (projeto Pixelorama 144x256, 9 quadros) ===== */
#tav{{position:relative;--tavAnim:url({uri("taverna-animada.png")});--tavParada:url({uri("taverna-parada.png")})}}
#pg-gastos{{background:#140c10!important}}
#tav .tavbg{{position:sticky;top:0;z-index:0;height:var(--H,100dvh);margin:0 -10px calc(-1 * var(--H,100dvh));pointer-events:none;
 background:var(--tavAnim) center top/cover no-repeat;image-rendering:pixelated;image-rendering:crisp-edges}}
#tav .tavbg::after{{content:"";position:absolute;inset:0;background:linear-gradient(rgba(12,7,10,.15),rgba(12,7,10,0) 30%,rgba(12,7,10,.35) 70%,rgba(12,7,10,.7))}}
@media (prefers-reduced-motion:reduce){{#tav .tavbg{{background-image:var(--tavParada)}}}}
#tav>*:not(.tavbg){{position:relative;z-index:1}}
#tav .tvhead{{display:flex!important;justify-content:center;padding-top:40px;margin:0 0 6px!important}}
#tav .tvhead img{{width:180px!important;height:auto;-webkit-mask-image:none!important;mask-image:none!important;filter:drop-shadow(0 4px 0 rgba(0,0,0,.45))}}
#tav .tvtit{{top:85px!important}}
/* madeira semitransparente: a taverna aparece através dos quadros; moldura, cantoneiras e texto seguem opacos */
#tav .tvp,#tav .tvm{{position:relative;isolation:isolate;background:transparent!important}}
#tav .tvp::before,#tav .tvm::before{{content:"";position:absolute;inset:6px;z-index:-1;background:var(--tvTab) 0 0/96px 32px,#2e1c10;opacity:.72;pointer-events:none}}
#tav .tvp::after{{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
 background:var(--tvCTL) 4px 4px/20px 20px no-repeat,var(--tvCTR) calc(100% - 4px) 4px/20px 20px no-repeat,var(--tvCBL) 4px calc(100% - 4px)/20px 20px no-repeat,var(--tvCBR) calc(100% - 4px) calc(100% - 4px)/20px 20px no-repeat}}
/* ===== fim fundo Taverna ===== */
"""
ini = html.find("/* ===== Taverna: fundo animado")
if ini >= 0:
    fim = html.index("/* ===== fim fundo Taverna ===== */\n", ini) + len("/* ===== fim fundo Taverna ===== */\n")
    html = html[:ini] + css + html[fim:]
else:
    i = html.index("</style>")
    html = html[:i] + css + html[i:]
open(html_path, "wb").write(html.encode("utf-8"))
print("ok; arquivo", len(html.encode("utf-8")), "B")
