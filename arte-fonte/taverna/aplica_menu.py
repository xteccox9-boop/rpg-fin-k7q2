# Taverna: cenário do taverneiro + navegação inferior com ícones em lacres de cera (sem texto),
# quadros de conteúdo em pergaminho sujo e balão de fala do taverneiro com trocadilhos.
# Uso: python aplica_menu.py <controle-gastos.html>
import base64, io, json, os, random, sys
from urllib.parse import quote
from PIL import Image

html_path = sys.argv[1]
base = os.path.dirname(os.path.abspath(__file__))
def png_uri(im):
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
def frames(pasta):
    meta = json.load(open(os.path.join(base, "menu", pasta, "atlas.json")))
    atlas = Image.open(os.path.join(base, "menu", pasta, "atlas.png")).convert("RGBA")
    return {f["name"]: atlas.crop((f["rect"][0], f["rect"][1], f["rect"][0] + f["rect"][2], f["rect"][1] + f["rect"][3])) for f in meta["frames"]}

selos = frames("selos"); ico = frames("icones")
def peca(*caminho): return png_uri(Image.open(os.path.join(base, *caminho)).convert("RGBA"))
BAL_CORPO, BAL_RABO = peca("balao", "balao-corpo.png"), peca("balao", "balao-rabo.png")
PANO, CORDA = peca("faixa", "pano.png"), peca("faixa", "corda.png")
fundo = Image.open(os.path.join(base, "fundo2", "quadro-01.png")).convert("RGBA")
fundo_uri = png_uri(fundo)
r, g, b, _ = fundo.getpixel((fundo.width // 2, fundo.height - 1))
cor_baixo = "#%02x%02x%02x" % (r, g, b)

# ---- textura de pergaminho sujo (SVG em pixels de 2px) e borda rasgada ----
rnd = random.Random(21)
manchas = []
for _ in range(26):                                    # manchas grandes e claras/escuras
    x, y = rnd.randrange(0, 96, 2), rnd.randrange(0, 96, 2)
    cor = rnd.choice(["#d8bd88", "#cdb07a", "#e9d4a6", "#c4a46c"])
    for _ in range(rnd.randint(3, 7)):
        manchas.append(f'<rect x="{(x + rnd.randrange(-6, 7, 2)) % 96}" y="{(y + rnd.randrange(-4, 5, 2)) % 96}" width="{rnd.choice([4, 6, 8])}" height="{rnd.choice([2, 4])}" fill="{cor}"/>')
for _ in range(40):                                    # sujeirinhas
    manchas.append(f'<rect x="{rnd.randrange(0, 96, 2)}" y="{rnd.randrange(0, 96, 2)}" width="2" height="2" fill="{rnd.choice(["#a8885a", "#8a6a40", "#b89868"])}"/>')
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" shape-rendering="crispEdges"><rect width="96" height="96" fill="#e1c793"/>' + "".join(manchas) + "</svg>"
PERG = 'url("data:image/svg+xml,' + quote(svg, safe="") + '")'
def borda_rasgada():
    pts = []
    for i in range(0, 101, 5):  pts.append(f"{i}% {rnd.choice([0, 2, 3, 1])}px")
    for i in range(5, 96, 6):   pts.append(f"calc(100% - {rnd.choice([0, 2, 3, 1])}px) {i}%")
    for i in range(100, -1, -5): pts.append(f"{i}% calc(100% - {rnd.choice([0, 2, 3, 1])}px)")
    for i in range(95, 4, -6):  pts.append(f"{rnd.choice([0, 2, 3, 1])}px {i}%")
    return "polygon(" + ",".join(pts) + ")"
RASGO = borda_rasgada()

html = open(html_path, "rb").read().decode("utf-8")
i = html.find("/* ===== Taverna em abas: só categorias aberto")
if i >= 0:
    j = html.index("</style>", i); html = html[:i] + html[j:]
i = html.find("<script>\n/* ===== Taverna em abas =====")
if i >= 0:
    j = html.index("</script>\n", i) + len("</script>\n"); html = html[:i] + html[j:]

css = f"""/* ===== Taverna: cenário do taverneiro + navegação inferior em pixel art ===== */
#tav{{--tavAnim:url({fundo_uri});--tavParada:url({fundo_uri});--tvSelo:url({png_uri(selos["normal"])});--tvSeloSel:url({png_uri(selos["selecionado"])});
 --tvPerg:{PERG};--tinta:#2b1a0e;--tinta2:#5a3a1e;
 --tvBalC:url({BAL_CORPO});--tvBalR:url({BAL_RABO});--tvPano:url({PANO});--tvCorda:url({CORDA});
 display:flex;flex-direction:column;
 /* espaço do cenário: até o balcão (90% da largura), mas encolhe em telas baixas para o resto caber */
 --tvEsp:min(calc(100vw * .9),calc(var(--H,100dvh) - 370px));
 --tvDock:calc(100px + env(safe-area-inset-bottom,0px));
 /* a Taverna vai até o fim da tela: o conteúdo passa por baixo da roda */
 height:var(--H,100dvh)}}
#pg-gastos{{padding-bottom:0!important}}
/* a imagem sobe junto quando o espaço encolhe, mantendo o balcão alinhado com a faixa do mês */
#tav .tavbg{{background:var(--tavAnim) center calc(var(--tvEsp) - 100vw * .9)/100% auto no-repeat,{cor_baixo}!important;
 position:absolute!important;inset:0 -10px!important;height:auto!important;margin:0!important;z-index:0}}
/* o fundo fica fora do fluxo: a faixa do mês não se mexe, seja qual for a seção aberta */
#tav{{position:relative}}
#pg-gastos{{background:{cor_baixo}!important;overflow-y:hidden}}
#tav .tavbg::after{{background:linear-gradient(rgba(12,7,10,.35),rgba(12,7,10,0) 16%)!important}}
/* o taverneiro e o balcão ficam livres; a faixa do mês fica sempre na mesma altura */
#tav .tvhead{{position:relative;flex:none;height:var(--tvEsp);padding:0!important;margin:0!important}}
#tav .tvhead>*:not(.tvbalao){{display:none!important}}
#tvBody{{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;scrollbar-width:none;display:flex;flex-direction:column;gap:12px;padding:2px 2px calc(var(--tvDock) + 80px)}}

/* faixa vermelha pendurada (no lugar da placa do mês), amarrada por cordas nas laterais */
#tav .tvnav{{flex:none;position:relative;margin:0 22px 6px!important;padding:5px 4px 16px;gap:4px;
 border-style:solid;border-width:0;border-image:var(--tvPano) 7 8 9 8 fill/14px 16px 18px 16px round;
 image-rendering:pixelated;image-rendering:crisp-edges;filter:drop-shadow(0 4px 0 rgba(20,10,16,.45))}}
#tav .tvnav::before,#tav .tvnav::after{{content:"";position:absolute;top:-32px;left:-17px;width:28px;height:44px;pointer-events:none;
 background:var(--tvCorda) 0 0/28px 44px no-repeat;image-rendering:pixelated;image-rendering:crisp-edges}}
#tav .tvnav::after{{left:auto;right:-17px;transform:scaleX(-1)}}
#tav .tvnav>.tvm{{flex:1;min-width:0;background:none!important;border:0!important;border-image:none!important;box-shadow:none!important;padding:0!important;text-align:center}}
#tav .tvnav>.tvm::before,#tav .tvnav>.tvm::after{{display:none!important}}
#tav .tvnav>.tvm b{{color:#ffd98a!important;font-size:22px!important;text-shadow:0 2px 0 #2e222f!important}}
#tav .tvnav>.tvm small{{color:#fdcbb0!important;text-shadow:0 1px 0 #2e222f!important}}
#tav .tvnav>button{{width:30px!important;height:34px!important;background:none!important;border:0!important;border-image:none!important;box-shadow:none!important;
 color:#fbb954!important;font-size:30px!important;text-shadow:0 2px 0 #2e222f!important}}
#tav .tvnav>button::before{{display:none!important}}
#tvBody::-webkit-scrollbar{{display:none}}
#tvBody{{-webkit-mask-image:linear-gradient(transparent,#000 14px);mask-image:linear-gradient(transparent,#000 14px)}}
#tav .tvcols{{display:contents}}
#tvBody .tvp{{margin:0!important}}
#tvBody .tvp:not(.tvVis){{display:none!important}}
#tvBody .tvp.tvVis{{animation:tvVem .2s ease-out}}
@keyframes tvVem{{from{{opacity:0;transform:translateY(6px)}}}}
#tav section[aria-label="Gastos por categoria"]{{display:grid;grid-template-columns:120px 1fr;column-gap:14px;align-items:center}}
#tav section[aria-label="Gastos por categoria"]>.tvh{{grid-column:1/-1}}
#tav #tvDonut{{width:120px;margin:0!important}}
#tav #tvDonut svg{{width:100%;height:auto}}

/* quadros de conteúdo: pergaminho sujo com borda rasgada e beiradas queimadas; texto em tinta escura */
#tvBody .tvp{{clip-path:{RASGO};padding:16px 16px 14px!important;color:var(--tinta)!important;text-shadow:none!important}}
#tvBody .tvp::before{{inset:0!important;opacity:1!important;background:var(--tvPerg) 0 0/96px 96px,#e1c793!important}}
#tvBody .tvp::after{{background:none!important;box-shadow:inset 0 0 0 2px #7a5430,inset 0 0 0 3px rgba(122,84,48,.35),inset 0 0 18px 6px rgba(120,76,32,.55),inset 0 -10px 16px rgba(90,56,24,.35)!important}}
#tvBody .tvp :is(b,small,span,p,h3,h4,em,div,label,i,strong){{color:inherit;text-shadow:none!important}}
#tvBody .tvp .tvh,#tvBody .tvp .tvh2{{color:#6e1a16!important}}
#tvBody .tvp small,#tvBody .tvp .tvsm,#tvBody .tvp .tvpct,#tvBody .tvp .tvleg em{{color:var(--tinta2)!important}}
#tvBody .tvp .tvk{{color:var(--tinta2)!important}}
#tvBody .tvp .tvlink{{color:#8a2a12!important}}
#tvBody .tvp .tvbadge{{color:#2b1a0e!important;background:#c8a050!important;border-color:#7a5430!important}}
#tvBody .tvp #tvDisp,#tvBody .tvp .ok,#tvBody .tvp .pos{{color:#1f6a2a!important}}
#tvBody .tvp .bad,#tvBody .tvp .neg,#tvBody .tvp .over{{color:#a01e14!important}}
#tvBody .tvp .tvbar{{background:#c4a46c!important;box-shadow:inset 0 0 0 2px #7a5430!important}}
#tvBody .tvp #tvDonut text{{fill:var(--tinta)!important}}
#tvBody .tvp .tvleg button{{color:var(--tinta)!important}}
#tvBody .tvp .tvult button,#tvBody .tvp .tvrw{{border-color:rgba(122,84,48,.35)!important}}
#tvBody .tvp .tvbtn{{color:#3a1a08!important;border-color:#7a5430!important;background:rgba(122,84,48,.15)!important}}
#tvBody .tvp input{{color:var(--tinta)!important}}

/* navegação inferior: ícones em lacres de cera, sem texto, colados na roda */
/* os lacres flutuam sobre o conteúdo: o pergaminho continua por trás deles, desfocado */
#tav>.tvmenu{{position:absolute;left:0;right:0;bottom:calc(var(--tvDock) + 2px);z-index:3;display:grid;grid-template-columns:repeat(5,1fr);justify-items:center;margin:0;padding:0}}
/* desfoque escurecido atrás dos lacres e da roda, até o fim da tela */
.tvmenu::before{{content:"";position:absolute;left:-10px;right:-10px;top:-22px;bottom:calc(-2px - var(--tvDock));z-index:-1;pointer-events:none;
 -webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);background:rgba(22,13,20,.55);
 -webkit-mask-image:linear-gradient(transparent,#000 22%);mask-image:linear-gradient(transparent,#000 22%)}}
.tvmb{{position:relative;width:60px!important;height:60px;min-height:0!important;padding:0!important;display:grid;place-items:center;border:0!important;border-radius:50%!important;
 background:var(--tvSelo) center/60px 60px no-repeat!important;box-shadow:none!important;image-rendering:pixelated;image-rendering:crisp-edges;cursor:pointer;-webkit-tap-highlight-color:transparent;
 filter:drop-shadow(0 3px 0 rgba(0,0,0,.55));transition:transform .08s ease-out,filter .15s ease-out}}
.tvmb img{{width:32px;height:32px;image-rendering:pixelated;image-rendering:crisp-edges;transition:transform .15s ease-out;pointer-events:none}}
@media (hover:hover){{.tvmb:hover{{filter:drop-shadow(0 3px 0 rgba(0,0,0,.55)) brightness(1.12)}}}}
.tvmb:active{{transform:translateY(2px) scale(.94);filter:drop-shadow(0 1px 0 rgba(0,0,0,.55)) brightness(.88)}}
.tvmb.sel{{background-image:var(--tvSeloSel)!important;transform:translateY(-3px);filter:drop-shadow(0 5px 0 rgba(0,0,0,.5))}}
.tvmb.sel:active{{transform:translateY(-1px) scale(.95)}}
.tvmb.pulso{{animation:tvPulso .24s ease-out}}
@keyframes tvPulso{{0%{{transform:scale(.9)}}60%{{transform:translateY(-4px) scale(1.06)}}100%{{transform:translateY(-3px) scale(1)}}}}
.tvmb:focus-visible{{outline:3px solid #ffd98a;outline-offset:2px}}
@media (max-height:700px){{.tvmb{{width:52px!important;height:52px}}.tvmb,.tvmb.sel{{background-size:52px 52px!important}}.tvmb img{{width:28px;height:28px}}}}

/* balão de fala do taverneiro: balão em pixel art (corpo em 9 fatias + rabinho), em 2x */
.tvbalao{{position:absolute;z-index:4;left:54%;right:3%;top:calc(100vw * .3 + var(--tvEsp) - 100vw * .9);padding:10px 14px 12px;
 background:none;color:#2e222f;font:400 12px/1.25 var(--fb);text-shadow:none;pointer-events:none;
 border-style:solid;border-width:0;border-image:var(--tvBalC) 8 fill/16px stretch;image-rendering:pixelated;image-rendering:crisp-edges;
 filter:drop-shadow(0 3px 0 rgba(20,10,16,.35));
 opacity:0;transform:translateY(6px) scale(.9);transform-origin:10% 100%;transition:opacity .18s ease-out,transform .22s cubic-bezier(.3,1.5,.5,1)}}
.tvbalao b{{display:block;margin-bottom:3px;font:400 18px/1 "Jacquard 12",Cinzel,serif;color:#6e2727}}
.tvbalao::after{{content:"";position:absolute;left:16px;bottom:-16px;width:22px;height:26px;
 background:var(--tvBalR) 0 0/22px 26px no-repeat;image-rendering:pixelated;image-rendering:crisp-edges}}
.tvbalao.on{{opacity:1;transform:none}}
/* ===== fim Taverna navegação ===== */
"""
i = html.find("/* ===== Taverna: cenário do taverneiro")
if i >= 0:
    j = html.index("/* ===== fim Taverna navegação ===== */\n", i) + len("/* ===== fim Taverna navegação ===== */\n")
    html = html[:i] + css + html[j:]
else:
    k = html.index("</style>"); html = html[:k] + css + html[k:]

icons = {k: png_uri(v) for k, v in ico.items()}
js = """<script>
/* ===== Taverna: navegação inferior (ícones em lacres de cera) =====
   Cada lacre mostra um conteúdo da Taverna e o taverneiro comenta com um trocadilho;
   Relatórios abre o relatório completo que já existe (botão da Guilda). O app continua
   preenchendo os quadros pelos mesmos ids; aqui só se escolhe qual aparece. */
(function(){
  var tav=document.getElementById("tav"),corpo=document.getElementById("tvBody"),cab=tav&&tav.querySelector(".tvhead");if(!tav||!corpo||!cab)return;
  var ICO=__ICONES__;
  var VIS={cat:['section[aria-label="Gastos por categoria"]'],dia:['section[aria-label="Últimos gastos"]'],
    res:[".tvsum",'section[aria-label="Parcelamentos e compromissos"]'],metas:["#tvSem"]};
  var FALAS={
    cat:["Categorias","Cada moeda no seu barril, aventureiro!","Separei tudo direitinho: nem o hidromel fica sem gaveta.","Me diz onde gastas, que eu te digo quem és!"],
    dia:["Gastos do dia","O que se gasta hoje, a taverna anota!","Conta de hoje não fica pra amanhã.","Hoje o caneco e a carteira esvaziaram juntos?"],
    res:["Resumo do mês","O mês inteiro num gole só!","Resumindo: menos rodada, mais moeda.","Fechei a conta do mês. Tim-tim pro orçamento!"],
    metas:["Metas","Quem guarda no baú, brinda tranquilo depois.","Meta boa é feito barril: enche devagar.","Teto é teto, aventureiro. Até pra cerveja!"],
    rel:["Relatórios","O pergaminho não mente... mas às vezes dói.","Aqui está tudo por escrito, com selo e tudo!","Lê com calma: é mais longo que a lista de fiado."]
  };
  var itens=[["cat","categorias"],["dia","dia"],["res","resumo"],["metas","metas"],["rel","relatorios"]];
  var nav=document.createElement("nav");nav.className="tvmenu";nav.setAttribute("aria-label","Seções da Taverna");
  itens.forEach(function(it){
    var b=document.createElement("button");b.type="button";b.className="tvmb";b.dataset.view=it[0];
    b.innerHTML='<img alt="" src="'+ICO[it[1]]+'">';
    b.setAttribute("aria-label",it[0]==="rel"?"Abrir relatório do mês":"Mostrar "+FALAS[it[0]][0]);b.title=FALAS[it[0]][0];
    nav.appendChild(b);
  });
  corpo.parentNode.insertBefore(nav,corpo.nextSibling);
  var balao=document.createElement("div");balao.className="tvbalao";balao.setAttribute("role","status");balao.setAttribute("aria-live","polite");
  balao.innerHTML="<b></b><span></span>";cab.appendChild(balao);
  var tmr=0,ultima={};
  function fala(v){
    var f=FALAS[v];if(!f)return;var op=f.slice(1),k;
    do{k=Math.floor(Math.random()*op.length)}while(op.length>1&&k===ultima[v]);ultima[v]=k;
    balao.querySelector("b").textContent=f[0];balao.querySelector("span").textContent=op[k];
    balao.classList.remove("on");void balao.offsetWidth;balao.classList.add("on");
    clearTimeout(tmr);tmr=setTimeout(function(){balao.classList.remove("on")},3600);
  }
  function mostra(v){
    var alvo=(VIS[v]||[]).map(function(s){return corpo.querySelector(s)});
    corpo.querySelectorAll(".tvp").forEach(function(p){p.classList.toggle("tvVis",alvo.indexOf(p)>=0)});
    corpo.scrollTop=0;
    nav.querySelectorAll(".tvmb").forEach(function(b){var on=b.dataset.view===v;b.classList.toggle("sel",on);if(b.dataset.view!=="rel")b.setAttribute("aria-pressed",String(on))});
  }
  nav.addEventListener("click",function(e){
    var b=e.target.closest(".tvmb");if(!b)return;
    b.classList.remove("pulso");void b.offsetWidth;b.classList.add("pulso");
    fala(b.dataset.view);
    if(b.dataset.view==="rel"){var r=document.getElementById("trRel");if(r)setTimeout(function(){r.click()},350);return}
    mostra(b.dataset.view);
  });
  nav.addEventListener("animationend",function(e){if(e.target.classList)e.target.classList.remove("pulso")});
  var bAba=document.querySelector('.dock>button[data-v="gastos"]');
  if(bAba)new MutationObserver(function(){if(bAba.classList.contains("on")){mostra("cat")}else{balao.classList.remove("on")}}).observe(bAba,{attributes:true,attributeFilter:["class"]});
  mostra("cat");
})();
</script>
""".replace("__ICONES__", json.dumps(icons, ensure_ascii=False))
i = html.find("<script>\n/* ===== Taverna: navegação inferior")
if i >= 0:
    j = html.index("</script>\n", i) + len("</script>\n"); html = html[:i] + js + html[j:]
else:
    k = html.index("<script>\n/* ===== Roda de moinho"); html = html[:k] + js + html[k:]

open(html_path, "wb").write(html.encode("utf-8"))
print("ok; arquivo", len(html.encode("utf-8")), "B")
