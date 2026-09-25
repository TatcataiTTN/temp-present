"""Generates every HTML page from content.py + data/questions.json. Run: python3 build/build_site.py"""
import html, json, re
from pathlib import Path
from content import TECH, MARKET, NOTES

ROOT = Path(__file__).resolve().parent.parent
e = html.escape
NAV = [("index.html", "Home"), ("slides/", "Slides"), ("script/", "Script")]
DESC = "SCAMPER Exercise 1: improving a hụi-tracking app. Slides, diagrams, study guide, auto-graded practice and presentation script."
RING_SLIDE = 6  # 1-based index of the hụi-cycle animation slide


def page(path, title, active, body, scripts=""):
    pre = "../" * path.count("/")
    nav = "".join(f'<a href="{pre}{h}" class="{"on" if h == active else ""}">{n}</a>' for h, n in NAV)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · SCAMPER Exercise</title>
<meta name="description" content="{e(DESC)}">
<link rel="stylesheet" href="{pre}assets/style.css">
</head>
<body>
<header class="site"><div class="wrap">
  <a class="brand" href="{pre}index.html">Hụi<b>Keeper</b> 2.0</a>
  <nav class="main" aria-label="Main">{nav}</nav>
  <button class="theme" type="button" aria-label="Toggle light or dark theme">◐</button>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">USTH Innovation · Session 1 · Exercise 1 (SCAMPER). Plain HTML/JS; progress is stored only in your browser.</div></footer>
<script src="{pre}assets/app.js"></script>
{scripts}
</body></html>
'''
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def chip(t):
    return f'<span class="chip t{t["k"]}">{t["k"]}</span>'


# ---------------------------------------------------------------- slides
def slides_html():
    S = []
    T = {t["k"]: t for t in TECH}

    def sl(cls, inner):
        S.append(f'<section class="slide {cls}">{inner}</section>')

    def bullets(items):
        return '<ul class="big">' + "".join(f"<li>{e(m)}</li>" for m in items) + "</ul>"

    def pcard(t, short):
        return f'<div class="pc t{t["k"]}"><div class="ph"><span class="chip t{t["k"]}">{t["k"]}</span><b>{e(t["name"])}</b></div><p>{e(short)}</p><small>{e(t["why"])}</small></div>'

    sl("title", '<div class="kick">USTH Innovation · Session 1 · Exercise 1</div><h1>HụiKeeper 2.0</h1><p class="sub">Improving a hụi-tracking app with SCAMPER</p>')
    sl("", "<h2>A big informal market</h2>" + bullets(["Hụi and bốc bát họ circles are everywhere", "Black credit and pawnshops fill the gaps", "Formal finance does not reach many households"])
       + '<p class="tagline">High demand, little protection.</p>')
    sl("pic", '<h2>Where the gap is</h2><div class="panel"><img src="../diagrams/market-gap.png" alt="Diagram: household needs, what people use today, what is missing, and the first layer we build"></div>')
    sl("", "<h2>The product today</h2>" + bullets(["Flutter app for Android and iOS", "Fully offline: SQLite on the device", "Dead hụi (no interest) and live hụi (interest)", "Paid / unpaid, actual amount, notes", "Stats: paid, remaining, progress"]))
    sl("pic", '<h2>How it is built, and where changes land</h2><div class="panel"><img src="../diagrams/app-architecture.png" alt="Diagram: MVVM layers with Riverpod, Drift, SQLite and GoRouter, plus SCAMPER additions"></div>')
    sl("", '<h2>One hụi cycle: everyone pays, one member collects</h2><div class="anim"><svg id="ring" viewBox="-260 -240 520 480" role="img" aria-label="Ten members in a circle; the pot moves to one member per cycle"></svg><div class="cap" id="ringcap"></div></div>')
    minis = "".join(f'<div class="mini t{t["k"]}"><span class="chip t{t["k"]}">{t["k"]}</span><b>{e(t["name"])}</b><i>{e(t["q"])}</i></div>' for t in TECH)
    sl("", f'<h2>SCAMPER: seven questions for one product</h2><div class="minis">{minis}</div>')
    sl("", f'<h2>Fewer steps to record a payment</h2><div class="two">{pcard(T["S"], "One-tap “Paid” replaces typing amounts.")}{pcard(T["C"], "Ledger, reminder and payment QR on one card.")}</div>')
    sl("", f'<h2>Borrow what works, then flex it</h2><div class="two">{pcard(T["A"], "Loan-app due / overdue timeline; share receipts like a chat.")}{pcard(T["M"], "Flexible cycle length and a large-text mode.")}</div>')
    sl("", '<h2>Widen it, strip it, flip it</h2><div class="three">' + pcard(T["P"], "Savings-goal tracker and payment history.") + pcard(T["E"], "No sign-up, no internet, auto-calculated payouts.") + pcard(T["R"], "Player view first, host view one tap away.") + "</div>")
    sl("sketch", '<h2>The new version, on one screen</h2><img src="../deliverable/sketch.svg" alt="Hand-drawn sketch of HụiKeeper 2.0 with SCAMPER call-outs">')
    sl("", "<h2>What changes, and what comes next</h2>" + bullets(["Fewer taps per payment", "Reminders before every due date", "Nothing to sign up for, still offline"])
       + '<p class="tagline">Next: clickable prototype, test with 5 hụi players, explore escrow-ready records.</p>')
    assert len(S) == len(NOTES), (len(S), len(NOTES))
    return S


def words_of(sections):
    n = 0
    for s in sections:
        s = re.sub(r"<svg.*?</svg>", "", s, flags=re.S)
        s = re.sub(r"<[^>]+>", " ", s)
        n += len(re.findall(r"[\w’'-]+", html.unescape(s)))
    return n


DECK_CSS = """
:root{--bg:#0b1512;--ink:#eef6f2;--mut:#9db3aa;--brand:#2dd4bf;--S:#2dd4bf;--C:#60a5fa;--A:#a78bfa;--M:#fbbf24;--P:#f472b6;--E:#f87171;--R:#22d3ee}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#050a08;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;overflow:hidden}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center;background:radial-gradient(1200px 600px at 10% 0,#12332c,var(--bg));overflow:hidden}
.slide{position:absolute;inset:0;padding:60px 88px 50px;display:none;flex-direction:column}
.slide.on{display:flex;animation:in .35s ease}
@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
h1{font-size:104px;letter-spacing:-.04em;margin:0;line-height:1}
h2{font-size:44px;letter-spacing:-.025em;margin:0 0 30px;line-height:1.15;max-width:1050px}
.title{justify-content:center}.kick{color:var(--brand);font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:22px;font-size:20px}
.sub{font-size:34px;color:var(--mut);margin:18px 0 0}
ul.big{list-style:none;padding:0;margin:0}ul.big li{font-size:36px;line-height:1.3;padding:14px 0 14px 40px;position:relative}
ul.big li::before{content:"";position:absolute;left:0;top:30px;width:16px;height:16px;border-radius:50%;background:var(--brand)}
.tagline{margin-top:auto;font-size:26px;color:var(--brand);font-weight:600}
.pic h2{margin-bottom:18px}.panel{background:#fff;border-radius:18px;padding:14px;display:flex;justify-content:center;align-items:center;flex:1;min-height:0}
.panel img{max-width:100%;max-height:100%;object-fit:contain}
.minis{display:grid;grid-template-columns:repeat(2,1fr);gap:14px 26px}
.mini{display:grid;grid-template-columns:44px 1fr;column-gap:14px;align-items:center;padding:10px 0;border-bottom:1px solid #1f3a33}
.mini b{font-size:26px}.mini i{grid-column:2;font-style:normal;color:var(--mut);font-size:19px;line-height:1.3}
.chip{display:inline-grid;place-items:center;width:44px;height:44px;border-radius:50%;color:#04211d;font-weight:800;font-size:22px;background:var(--t)}
.tS{--t:var(--S)}.tC{--t:var(--C)}.tA{--t:var(--A)}.tM{--t:var(--M)}.tP{--t:var(--P)}.tE{--t:var(--E)}.tR{--t:var(--R)}
.two,.three{display:grid;gap:28px;flex:1;align-content:center;padding-bottom:30px}.two{grid-template-columns:1fr 1fr}.three{grid-template-columns:repeat(3,1fr)}
.pc{background:#10221d;border:1px solid #1f3a33;border-top:6px solid var(--t);border-radius:18px;padding:36px 32px}.pc small{display:block;margin-top:18px;color:var(--mut);font-size:22px;line-height:1.35}
.ph{display:flex;align-items:center;gap:14px;margin-bottom:14px}.ph b{font-size:32px}.pc p{margin:0;font-size:34px;line-height:1.35;color:#d6e6df}
.three .pc p{font-size:28px}.three .pc small{font-size:20px}
.anim{display:flex;align-items:center;gap:30px;flex:1;min-height:0}.anim svg{height:480px;width:520px;flex:none}
.cap{font-size:32px;line-height:1.4;color:#d6e6df}.cap b{color:var(--M)}
.sketch{padding:30px 88px 30px}.sketch h2{margin-bottom:10px;font-size:38px}.sketch img{height:566px;width:auto;align-self:center;border-radius:14px;background:#fffdf6}
#hud{position:absolute;left:0;right:0;bottom:0;height:6px;background:#12221d;z-index:5}#hud i{display:block;height:100%;width:0;background:var(--brand);transition:width .3s}
#count{position:absolute;right:28px;bottom:16px;color:var(--mut);font-size:16px;z-index:5}
#home{position:absolute;left:28px;bottom:16px;color:var(--mut);font-size:16px;text-decoration:none;z-index:5}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:#f6f7f4;color:#15211d;padding:16px 28px;font-size:17px;line-height:1.6;display:none;z-index:9;border-top:4px solid var(--brand)}
#notes.on{display:block}#notes small{display:block;color:#5b6b64;margin-bottom:6px}
.nb{position:fixed;top:12px;right:12px;z-index:9;display:flex;gap:8px}
.nb button{background:#12221d;color:var(--ink);border:1px solid #2a4a41;border-radius:999px;padding:6px 14px;cursor:pointer;font-size:14px}
@media print{html,body{overflow:visible;height:auto}#stage{position:static;transform:none!important;width:auto;height:auto}.slide{display:flex!important;position:relative;height:720px;page-break-after:always}.nb,#hud,#count,#home,#notes{display:none!important}}
"""

DECK_JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide')),stage=document.getElementById('stage'),cur=0,RING=RING_IDX;
  var notes=NOTES_JSON;
  function fit(){var on=document.getElementById('notes').classList.contains('on');var s=Math.min(innerWidth/1280,(innerHeight*(on?.66:1))/720);
    stage.style.transform='translate(-50%,-50%) scale('+s+')';stage.style.top=(on?33:50)+'%';}
  function show(n){cur=Math.max(0,Math.min(slides.length-1,n));slides.forEach(function(s,i){s.classList.toggle('on',i===cur)});
    document.getElementById('bar').style.width=((cur+1)/slides.length*100)+'%';document.getElementById('count').textContent=(cur+1)+' / '+slides.length;
    var n2=notes[cur+1];document.getElementById('notes').innerHTML='<small>Speaker notes · slide '+(cur+1)+' · about '+n2[1]+' s</small>'+n2[0];
    history.replaceState(null,'','#'+(cur+1));ring(cur===RING);}
  var timer=null,k=0;
  function ring(active){clearInterval(timer);if(!active)return;k=0;draw();timer=setInterval(function(){k=(k+1)%10;draw();},1400);}
  function draw(){var svg=document.getElementById('ring'),R=185,h='',i,a;var P=[];
    for(i=0;i<10;i++){a=-Math.PI/2+i*2*Math.PI/10;P.push([Math.cos(a)*R,Math.sin(a)*R]);}
    for(i=0;i<10;i++){if(i!==k)h+='<line x1="'+P[i][0]+'" y1="'+P[i][1]+'" x2="'+P[k][0]+'" y2="'+P[k][1]+'" stroke="#2dd4bf" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6"/>';}
    for(i=0;i<10;i++){var c=i===k,done=i<k;
      h+='<circle cx="'+P[i][0]+'" cy="'+P[i][1]+'" r="'+(c?38:30)+'" fill="'+(c?'#fbbf24':done?'#1f3a33':'#12221d')+'" stroke="'+(c?'#fbbf24':'#2dd4bf')+'" stroke-width="3"/>'+
        '<text x="'+P[i][0]+'" y="'+(P[i][1]+8)+'" text-anchor="middle" font-size="24" font-weight="700" fill="'+(c?'#0b1512':done?'#7fa89c':'#eef6f2')+'">'+(done?'✓':(i+1))+'</text>';}
    h+='<text x="0" y="-6" text-anchor="middle" font-size="26" fill="#9db3aa">pot</text><text x="0" y="30" text-anchor="middle" font-size="34" font-weight="700" fill="#fbbf24">→ member '+(k+1)+'</text>';
    svg.innerHTML=h;document.getElementById('ringcap').innerHTML='Cycle <b>'+(k+1)+'</b> of 10<br>Member '+(k+1)+' collects the pot.<br>The other members pay in.';}
  document.addEventListener('keydown',function(ev){var c=ev.key;
    if(c==='ArrowRight'||c==='PageDown'||c===' '){ev.preventDefault();show(cur+1)}else if(c==='ArrowLeft'||c==='PageUp'){show(cur-1)}
    else if(c==='Home'){show(0)}else if(c==='End'){show(slides.length-1)}
    else if(c==='n'||c==='N'){toggleNotes()}else if(c==='f'||c==='F'){fs()}});
  function toggleNotes(){document.getElementById('notes').classList.toggle('on');fit();}
  function fs(){if(document.fullscreenElement)document.exitFullscreen();else if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen();}
  var sx=null;document.addEventListener('touchstart',function(e){sx=e.touches[0].clientX});
  document.addEventListener('touchend',function(e){if(sx==null)return;var d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50)show(cur+(d<0?1:-1));sx=null});
  document.getElementById('prev').onclick=function(){show(cur-1)};document.getElementById('next').onclick=function(){show(cur+1)};
  document.getElementById('nt').onclick=toggleNotes;document.getElementById('fs').onclick=fs;
  addEventListener('resize',fit);fit();show((parseInt(location.hash.slice(1),10)||1)-1);
})();
"""


def build_slides():
    S = slides_html()
    notes_json = json.dumps({str(k): [v[0], v[1]] for k, v in NOTES.items()}, ensure_ascii=False)
    js = DECK_JS.replace("NOTES_JSON", notes_json).replace("RING_IDX", str(RING_SLIDE - 1))
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HụiKeeper 2.0 · SCAMPER Slides</title><style>{DECK_CSS}</style></head>
<body>
<div id="stage">{"".join(S)}<a id="home" href="../index.html">← Home</a><div id="count"></div><div id="hud"><i id="bar"></i></div></div>
<div class="nb"><button id="prev" aria-label="Previous slide">‹</button><button id="next" aria-label="Next slide">›</button><button id="nt">Notes (N)</button><button id="fs">Full screen (F)</button></div>
<div id="notes"></div>
<script>{js}</script>
</body></html>
'''
    (ROOT / "slides").mkdir(exist_ok=True)
    (ROOT / "slides" / "index.html").write_text(doc, encoding="utf-8")
    return words_of(S), len(S)


# ---------------------------------------------------------------- pages
def build_pages(slide_words, slide_count, note_words):
    total_sec = sum(v[1] for v in NOTES.values())
    desc = ("HụiKeeper 2.0 keeps the promise of the current app, a free, offline ledger for personal hụi circles, and removes the friction around it. "
            "Players see this week’s dues first and mark a payment with one tap or a receipt photo. A payment card carries a reminder and a QR code and can be shared as an image to the circle’s group. "
            "Text size, cycle length and view (player or host) are adjustable, and the same ledger can track a personal savings goal. There is no sign-up and no server: everything stays on the phone.")
    body = f'''
<div class="hero"><span class="pill">Innovation · Session 1 · Exercise 1</span>
<h1>HụiKeeper 2.0</h1>
<p class="lead">Improving a hụi-tracking app with SCAMPER: Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Rearrange/Reverse.</p>
<a class="btn" href="slides/">Open the slides</a> <a class="btn ghost" href="script/">Read the script</a></div>
<div class="kpis"><div class="kpi"><b>{slide_count}</b><span>slides</span></div><div class="kpi"><b>{total_sec // 60} min</b><span>presentation</span></div><div class="kpi"><b>7</b><span>SCAMPER techniques</span></div></div>
<h2>The new product</h2>
<div class="card"><p style="margin:0">{e(desc)}</p></div>
<h2>Sketch</h2>
<figure><img src="deliverable/sketch.svg" alt="Hand-drawn sketch of HụiKeeper 2.0 with SCAMPER call-outs"><figcaption>Each letter maps to one SCAMPER technique. <a href="deliverable/sketch.png">PNG</a> · <a href="deliverable/sketch.svg">SVG</a></figcaption></figure>
<h2>Diagrams</h2>
<div class="grid g2"><figure><img src="diagrams/market-gap.png" alt="Market gap diagram"><figcaption>Market gap. <a href="diagrams/market-gap.drawio">draw.io file</a></figcaption></figure>
<figure><img src="diagrams/app-architecture.png" alt="App architecture diagram"><figcaption>App architecture. <a href="diagrams/app-architecture.drawio">draw.io file</a></figcaption></figure></div>
'''
    page("index.html", "Home", "index.html", body)

    beats, t0 = "", 0
    for i, (txt, sec, ttl) in NOTES.items():
        a, b = t0, t0 + sec
        t0 = b
        beats += f'<div class="beat"><div class="t">{a // 60}:{a % 60:02d}–{b // 60}:{b % 60:02d}<small>Slide {i}</small></div><div><h3>{e(ttl)}</h3><p>{e(txt)}</p></div></div>'
    body = f'''
<h1>Presentation script</h1>
<p class="lead">A {total_sec // 60}-minute talk in English over {slide_count} slides (about {note_words} spoken words, with pauses on the diagrams, the animation and the sketch).</p>
<div class="callout"><b>Key message.</b> Demand for hụi and bốc bát họ is high; black credit and pawnshops are common; and there is essentially no neutral intermediary that freezes funds fairly, nor a channel that converts a credit-card limit into a flat-fee cost. Our app is the first layer: a trusted record.</div>
<div class="tablewrap" style="margin-top:20px"><div style="padding:0 20px">{beats}</div></div>
<p style="margin-top:18px"><a class="btn" href="../slides/#1">Open the slides</a> <span style="color:var(--muted)">Press N in the deck to show these notes.</span></p>'''
    page("script/index.html", "Script", "script/", body)
    (ROOT / "deliverable" / "speaker-script.md").write_text(
        "# Speaker script (English, ~10 min)\n\n" + "\n\n".join(f"**Slide {i} ({ttl}, ~{s}s)**\n\n{t}" for i, (t, s, ttl) in NOTES.items()) + "\n", encoding="utf-8")
    (ROOT / "deliverable" / "description.md").write_text("# HụiKeeper 2.0 — SCAMPER Exercise 1\n\n![sketch](sketch.png)\n\n" + desc + "\n", encoding="utf-8")


if __name__ == "__main__":
    sw, sc = build_slides()
    nw = sum(len(v[0].split()) for v in NOTES.values())
    build_pages(sw, sc, nw)
    print(f"slides: {sc}, on-slide words: {sw}, notes words: {nw}, total seconds: {sum(v[1] for v in NOTES.values())}")
