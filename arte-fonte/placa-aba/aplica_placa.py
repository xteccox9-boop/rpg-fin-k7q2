# Placa com o nome da aba no topo da página (primeiro quadro do .pxo "horizontal menu"), roda redesenhada
# com a paleta da placa, nome tirado da roda e números em Jacquard 12.
# Uso: python aplica_placa.py <controle-gastos.html>
import base64, io, os, re, sys
from PIL import Image

html_path = sys.argv[1]
base = os.path.dirname(os.path.abspath(__file__))
def png_uri(im):
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
placa = Image.open(os.path.join(base, "placa.png")).convert("RGBA")
assert placa.size == (122, 35), placa.size
html = open(html_path, "rb").read().decode("utf-8")

# ---- 1) roda redesenhada: aro de ferro com rebites, friso de bronze, madeira com veio, cubo de bronze ----
RODA = r'''function roda(a){
    var c=ctx,h=CS/2,i,an,a0,a1;c.clearRect(0,0,CS,CS);c.save();c.translate(h,h);c.rotate(a);
    disco(c,0,0,94,"#2e222f");disco(c,0,0,92.5,"#3e3546");
    c.strokeStyle="#625565";c.lineWidth=1;c.beginPath();c.arc(0,0,91.6,0,7);c.stroke();
    disco(c,0,0,89.6,"#2e222f");disco(c,0,0,88.6,"#cd683d");
    for(i=0;i<SL;i++){a0=(i*STEP-STEP/2-90)*RAD;a1=(i*STEP+STEP/2-90)*RAD;c.fillStyle=i%2?"#401701":"#4a1c04";c.beginPath();c.arc(0,0,87.6,a0,a1);c.arc(0,0,79,a1,a0,true);c.closePath();c.fill();
      c.strokeStyle="#240d00";c.lineWidth=1;c.beginPath();c.arc(0,0,84,a0+.06,a1-.1);c.stroke();
      c.strokeStyle="#63290b";c.beginPath();c.arc(0,0,86.2,a0+.12,a0+(a1-a0)*.55);c.stroke();
      c.strokeStyle="#240d00";c.beginPath();c.arc(0,0,81.5,a0+(a1-a0)*.35,a1-.05);c.stroke()}
    c.strokeStyle="#2e222f";c.lineWidth=1.6;
    for(i=0;i<SL;i++){an=(i*STEP+STEP/2)*RAD;c.beginPath();c.moveTo(Math.sin(an)*79,-Math.cos(an)*79);c.lineTo(Math.sin(an)*89,-Math.cos(an)*89);c.stroke()}
    c.globalCompositeOperation="destination-out";disco(c,0,0,78,"#000");c.globalCompositeOperation="source-over";
    c.strokeStyle="#cd683d";c.lineWidth=1;c.beginPath();c.arc(0,0,79.4,0,7);c.stroke();
    c.strokeStyle="#2e222f";c.lineWidth=1.6;c.beginPath();c.arc(0,0,78.4,0,7);c.stroke();
    for(i=0;i<SL;i++){c.save();c.rotate((i*STEP+STEP/2)*RAD);c.fillStyle="#2e222f";c.fillRect(-4,-79,8,62);c.fillStyle="#401701";c.fillRect(-3,-78,6,60);
      c.fillStyle="#63290b";c.fillRect(-3,-78,1.5,60);c.fillStyle="#240d00";c.fillRect(1.5,-78,1.5,60);
      c.fillStyle="#2e222f";c.fillRect(-4,-60,8,2);c.fillStyle="#cd683d";c.fillRect(-3,-59.5,6,1);c.restore()}
    disco(c,0,0,20,"#2e222f");disco(c,0,0,18.5,"#cd683d");disco(c,0,0,17,"#e6904e");disco(c,0,0,15.5,"#2e222f");disco(c,0,0,14.5,"#625565");disco(c,0,0,10.5,"#7f708a");disco(c,0,0,6,"#2e222f");disco(c,0,0,3.5,"#3e3546");
    for(i=0;i<6;i++){an=i*60*RAD;c.fillStyle="#2e222f";c.fillRect(Math.sin(an)*12.5-2,-Math.cos(an)*12.5-2,4,4);c.fillStyle="#9babb2";c.fillRect(Math.sin(an)*12.5-1,-Math.cos(an)*12.5-1,2,2)}
    for(i=0;i<SL;i++){c.save();c.rotate(i*STEP*RAD);disco(c,0,-85,12,"#2e222f");disco(c,0,-85,10.8,"#cd683d");disco(c,0,-85,9.6,"#2e222f");disco(c,0,-85,8.8,"#240d00");c.restore()}
    for(i=0;i<SL;i++){c.save();c.rotate((i*STEP+STEP/2)*RAD);c.fillStyle="#2e222f";c.fillRect(-2,-93,4,4);c.fillStyle="#9babb2";c.fillRect(-1,-92,2,2);c.fillStyle="#2e222f";c.fillRect(-2,-89,4,3);c.fillStyle="#fbb954";c.fillRect(-1,-88.5,2,2);c.restore()}
    c.restore();limiar(c,CS,CS);
  }
'''
i = html.index("function roda(a){")
j = html.index("  var ang=0,anim=0", i)
html = html[:i] + RODA + html[j:]

# ---- 2) números em Jacquard 12 (mesma fonte dos títulos): troca a fonte "Digitos" ----
JACQ = "https://fonts.gstatic.com/s/jacquard12/v8/vm8ydRLuXETEweL79J4rGf3OWHs.woff2"
html, n = re.subn(r'@font-face\{font-family:"Digitos";src:url\([^)]*\) format\("woff2"\);unicode-range:[^;]*;size-adjust:[^;]*;',
                  '@font-face{font-family:"Digitos";src:url(' + JACQ + ') format("woff2");unicode-range:U+0030-0039;size-adjust:' + sys.argv[2] + ';' if len(sys.argv) > 2 else
                  '@font-face{font-family:"Digitos";src:url(' + JACQ + ') format("woff2");unicode-range:U+0030-0039;size-adjust:125%;', html)
assert n == 1, n

# ---- 3) placa da aba + roda sem nome ----
CSS = f"""/* ===== Placa da aba no topo ===== */
.wh-lbl{{display:none!important}}
.abaPlaca{{position:fixed;z-index:6;left:50%;top:calc(env(safe-area-inset-top,0px) + 60px);width:183px;height:52.5px;margin-left:-91.5px;
 display:grid;place-items:center;padding:0 30px 3px;box-sizing:border-box;pointer-events:none;
 background:url({png_uri(placa)}) 0 0/183px 52.5px no-repeat;image-rendering:pixelated;image-rendering:crisp-edges;
 filter:drop-shadow(0 3px 0 rgba(20,10,16,.45));transform-origin:50% -20px}}
.abaPlaca b{{font:400 24px/1 "Jacquard 12",Cinzel,serif;color:#fbb954;text-shadow:0 2px 0 #240d00;white-space:nowrap;letter-spacing:.02em}}
.abaPlaca.troca{{animation:abaBalanca .45s cubic-bezier(.3,1.6,.5,1)}}
@keyframes abaBalanca{{0%{{transform:rotate(-5deg)}}50%{{transform:rotate(2.5deg)}}100%{{transform:none}}}}
@media (prefers-reduced-motion:reduce){{.abaPlaca.troca{{animation:none}}}}
/* o balão do taverneiro desce para não encostar na placa */
.tvbalao{{top:max(calc(100vw * .3 + var(--tvEsp) - 100vw * .9),calc(env(safe-area-inset-top,0px) + 122px))!important}}
/* ===== fim Placa da aba ===== */
"""
JS = """<script>
/* ===== Placa da aba no topo: mostra o nome que a roda está apontando ===== */
(function(){
  var lbl=document.querySelector(".wh-lbl");if(!lbl)return;
  var p=document.createElement("div");p.className="abaPlaca";p.setAttribute("aria-hidden","true");
  var b=document.createElement("b");p.appendChild(b);document.body.appendChild(p);
  function poe(){var t=lbl.textContent;if(t===b.textContent)return;var ant=b.textContent;b.textContent=t;
    if(ant){p.classList.remove("troca");void p.offsetWidth;p.classList.add("troca")}}
  new MutationObserver(poe).observe(lbl,{childList:true,characterData:true,subtree:true});poe();
  /* some junto com a roda quando o teclado abre */
  var dock=document.querySelector(".dock");
  if(dock)new MutationObserver(function(){p.style.display=getComputedStyle(dock).display==="none"?"none":""}).observe(dock,{attributes:true,attributeFilter:["class","style"]});
})();
</script>
"""
def troca_bloco(txt, ini, fim, novo, ancora):
    a = txt.find(ini)
    if a >= 0:
        z = txt.index(fim, a) + len(fim); return txt[:a] + novo + txt[z:]
    k = txt.index(ancora); return txt[:k] + novo + txt[k:]
html = troca_bloco(html, "/* ===== Placa da aba no topo ===== */", "/* ===== fim Placa da aba ===== */\n", CSS, "</style>")
html = troca_bloco(html, "<script>\n/* ===== Placa da aba no topo", "</script>\n", JS, "</body>")
open(html_path, "wb").write(html.encode("utf-8"))
print("ok; arquivo", len(html.encode("utf-8")), "B")
