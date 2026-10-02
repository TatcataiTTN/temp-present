"""Generates slides/index.html for Session 2. Run: python3 build/build_slides.py"""
import html, json
from pathlib import Path
from content import INTRO, Q, TAKEAWAY

ROOT = Path(__file__).resolve().parent.parent
e = html.escape

CSS = """
:root{--bg:#0b1512;--ink:#eef6f2;--mut:#9db3aa;--brand:#2dd4bf;--ok:#34d399;--no:#f87171;--q:#fbbf24}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#050a08;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;overflow:hidden}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center;background:radial-gradient(1200px 600px at 10% 0,#12332c,var(--bg));overflow:hidden}
.slide{position:absolute;inset:0;padding:56px 84px 46px;display:none;flex-direction:column}
.slide.on{display:flex;animation:in .35s ease}
@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
h1{font-size:92px;letter-spacing:-.04em;margin:0;line-height:1}
h2{font-size:42px;letter-spacing:-.025em;margin:0 0 8px;line-height:1.15;max-width:1060px}
.kick{color:var(--brand);font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:18px;font-size:19px}
.sub{font-size:30px;color:var(--mut);margin:16px 0 0;max-width:950px;line-height:1.35}
.title{justify-content:center}
.eyebrow{font-size:18px;color:var(--q);font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px}
.prompt{font-size:26px;line-height:1.4;color:#d6e6df;background:#10221d;border-left:5px solid var(--brand);border-radius:0 12px 12px 0;padding:18px 24px;margin-bottom:22px}
.issue{font-size:24px;line-height:1.4;color:var(--mut);margin-bottom:6px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:26px;flex:1;min-height:0}
.side{border-radius:16px;padding:26px 28px;display:flex;flex-direction:column;gap:10px;overflow:auto}
.side.ag{background:#0f2420;border:1px solid #1f4a3c;border-top:6px solid var(--ok)}
.side.op{background:#241212;border:1px solid #4a2020;border-top:6px solid var(--no)}
.side h3{margin:0;font-size:22px}
.side.ag h3{color:var(--ok)}.side.op h3{color:var(--no)}
.side p{margin:0;font-size:22px;line-height:1.45;color:#dce9e3}
.ex{margin-top:auto;font-size:19px;padding:10px 14px;border-radius:10px;background:#0b1a16;color:var(--mut)}
.ex b{color:var(--ink)}
.probe{margin-top:22px;font-size:24px;line-height:1.4;color:var(--q);font-style:italic;border-top:1px solid #1f3a33;padding-top:18px}
.probe b{font-style:normal}
.model{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.model svg{height:480px;width:auto}
.takeaway{margin-top:26px;font-size:27px;line-height:1.4;color:var(--brand);font-weight:600;max-width:1000px}
.close.slide{justify-content:center}
.closewrap{display:flex;flex-direction:column}
.kv{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:4px}
.kv div{background:#10221d;border:1px solid #1f3a33;border-radius:12px;padding:16px 20px;font-size:21px;line-height:1.35}
.kv b{display:block;color:var(--brand);font-size:17px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.litgrid{display:grid;gap:14px;overflow:auto}
.litgrid .card{background:#10221d;border:1px solid #1f3a33;border-radius:14px;padding:18px 22px}
.lit .card b{font-size:21px}
.lit .card span{display:block;color:var(--mut);font-size:17px;margin-top:4px}
.lit .card p{margin:8px 0 0;font-size:19px;line-height:1.4;color:#d6e6df}
#hud{position:absolute;left:0;right:0;bottom:0;height:6px;background:#12221d;z-index:5}#hud i{display:block;height:100%;width:0;background:var(--brand);transition:width .3s}
#count{position:absolute;right:28px;bottom:16px;color:var(--mut);font-size:16px;z-index:5}
#home{position:absolute;left:28px;bottom:16px;color:var(--mut);font-size:16px;text-decoration:none;z-index:5}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:#f6f7f4;color:#15211d;padding:16px 28px;font-size:17px;line-height:1.6;display:none;z-index:9;border-top:4px solid var(--brand)}
#notes.on{display:block}#notes small{display:block;color:#5b6b64;margin-bottom:6px}
.nb{position:fixed;top:12px;right:12px;z-index:9;display:flex;gap:8px}
.nb button{background:#12221d;color:var(--ink);border:1px solid #2a4a41;border-radius:999px;padding:6px 14px;cursor:pointer;font-size:14px}
@media print{html,body{overflow:visible;height:auto}#stage{position:static;transform:none!important;width:auto;height:auto}.slide{display:flex!important;position:relative;height:720px;page-break-after:always}.nb,#hud,#count,#home,#notes{display:none!important}}
"""

JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide')),stage=document.getElementById('stage'),cur=0;
  var notes=NOTES_JSON;
  function fit(){var on=document.getElementById('notes').classList.contains('on');var s=Math.min(innerWidth/1280,(innerHeight*(on?.66:1))/720);
    stage.style.transform='translate(-50%,-50%) scale('+s+')';stage.style.top=(on?33:50)+'%';}
  function show(n){cur=Math.max(0,Math.min(slides.length-1,n));slides.forEach(function(s,i){s.classList.toggle('on',i===cur)});
    document.getElementById('bar').style.width=((cur+1)/slides.length*100)+'%';document.getElementById('count').textContent=(cur+1)+' / '+slides.length;
    var n2=notes[cur+1]||['',0];document.getElementById('notes').innerHTML='<small>Speaker notes · slide '+(cur+1)+' · about '+n2[1]+' s</small>'+n2[0];
    history.replaceState(null,'','#'+(cur+1));}
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
  addEventListener('resize',fit);addEventListener('hashchange',function(){show((parseInt(location.hash.slice(1),10)||1)-1)});fit();show((parseInt(location.hash.slice(1),10)||1)-1);
})();
"""

# S-curve model: incumbent (steady, then plateaus/declines) vs disruptor (slow start, overtakes).
def model_svg():
    return '''<svg viewBox="0 0 1000 520" role="img" aria-label="S-curve: a disruptor starts slow then overtakes a plateauing incumbent">
<line x1="70" y1="440" x2="900" y2="440" stroke="#2a4a41" stroke-width="2"/>
<line x1="70" y1="440" x2="70" y2="40" stroke="#2a4a41" stroke-width="2"/>
<text x="900" y="468" fill="#9db3aa" font-size="20" text-anchor="end">Time</text>
<text x="70" y="26" fill="#9db3aa" font-size="20" text-anchor="start">Value</text>
<path d="M80 380 C 310 320, 510 140, 770 115" fill="none" stroke="#60a5fa" stroke-width="5"/>
<path d="M80 430 C 330 425, 430 360, 570 250 C 690 160, 730 110, 770 75" fill="none" stroke="#2dd4bf" stroke-width="5"/>
<circle cx="570" cy="250" r="8" fill="#fbbf24"/>
<text x="570" y="282" fill="#fbbf24" font-size="19" text-anchor="middle">crossover: adoption threshold</text>
<text x="200" y="476" fill="#9db3aa" font-size="19" text-anchor="middle">Netflix streaming pivot</text>
<text x="620" y="476" fill="#f87171" font-size="19" text-anchor="middle">Blockbuster: held the old curve too long</text>
<rect x="610" y="40" width="370" height="86" rx="10" fill="#0b1a16" stroke="#1f3a33"/>
<line x1="626" y1="64" x2="654" y2="64" stroke="#60a5fa" stroke-width="5"/>
<text x="662" y="70" fill="#60a5fa" font-size="17" font-weight="700" text-anchor="start">Incumbent: slowing gains</text>
<line x1="626" y1="102" x2="654" y2="102" stroke="#2dd4bf" stroke-width="5"/>
<text x="662" y="108" fill="#2dd4bf" font-size="17" font-weight="700" text-anchor="start">Disruptor: compounding gains</text>
</svg>'''

def slide(cls, inner):
    return f'<section class="slide {cls}">{inner}</section>'

def q_slide(q):
    return slide("", f'''<div class="eyebrow">{e(q["kind"])} {q["n"]}</div><h2>{e(q["title"])}</h2>
<div class="prompt">{e(q["prompt"])}</div>
<div class="issue"><b>Core issue.</b> {e(q["issue"])}</div>
<div class="split">
<div class="side ag"><h3>{e(q["agree_label"])}</h3><p>{e(q["agree"])}</p>
<div class="ex"><b>{e(q["example"][0])}</b> — {e(q["example"][1])}</div></div>
<div class="side op"><h3>{e(q["oppose_label"])}</h3><p>{e(q["oppose"])}</p>
<div class="ex"><b>{e(q["counter_example"][0])}</b> — {e(q["counter_example"][1])}</div></div>
</div>
<div class="probe"><b>Probing question.</b> {e(q["probe"])}</div>''')

def notes_for(n, sec, text):
    return str(n), [text, sec]

def build():
    S = []
    NOTES = {}
    i = 1

    S.append(slide("title", '<div class="kick">USTH Innovation · Session 2 · Discussion Questions</div>'
        '<h1>Is Innovation Compulsory?</h1><p class="sub">Two debates: digital-age survival, and innovation’s limits on global challenges</p>'))
    NOTES[i] = ["Good morning. Session 2 steps back from building a product to question the premise behind it: that innovation is no longer optional. We will argue two questions from both sides, ground each side in a real example, and end with a model and a short literature review.", 30]; i += 1

    S.append(slide("", f'<div class="eyebrow">Framing</div><h2>Why argue both sides?</h2><div class="prompt">{e(INTRO)}</div>'
        '<div class="kv"><div><b>Method</b>Core issue → agreement case → opposing case → probing question, for each prompt.</div>'
        '<div><b>Goal</b>Expose the assumption inside an absolute claim, not just answer yes or no.</div></div>'))
    NOTES[i] = [INTRO + " We will not land on a single verdict for either question. The point is to see what each absolute claim conveniently assumes.", 35]; i += 1

    q1 = Q[0]
    S.append(q_slide(q1))
    NOTES[i] = [f"Here is question one. {q1['issue']} On the side of agreement: {q1['agree']} On the opposing side: {q1['oppose']} That leaves the probing question: {q1['probe']}", 85]; i += 1

    S.append(slide("", '<div class="eyebrow">Model</div><h2>Why Netflix crossed and Blockbuster did not: the S-curve</h2><div class="model">' + model_svg() + '</div>'))
    NOTES[i] = ["This S-curve model explains the Netflix example. An incumbent's core technology improves quickly at first, then plateaus. A disruptor's new technology starts weaker, but compounds faster once it clears the adoption threshold, marked here in yellow. Netflix accepted a dip in its DVD numbers to get onto the streaming curve early. Blockbuster kept optimizing its store-rental curve, which was already past its bend, and so never crossed.", 55]; i += 1

    q2 = Q[1]
    S.append(q_slide(q2))
    NOTES[i] = [f"Question two moves from one company to global systems. {q2['issue']} The case for innovation: {q2['agree']} The case against treating it as sufficient: {q2['oppose']} Which leads to: {q2['probe']}", 85]; i += 1

    S.append(slide("", '<div class="eyebrow">Model</div><h2>Where innovation sits in the causal chain</h2><div class="model">' + causal_svg() + '</div>'))
    NOTES[i] = ["This diagram places innovation where it actually acts: on the middle box, the technical system. It does not reach the root causes on the left, such as regulation, profit incentives or geopolitics, and it can create new side effects on the right, such as e-waste or the energy draw of training large models. Confusing the middle box for the whole chain is the techno-solutionism trap.", 55]; i += 1

    S.append(slide("lit", '<div class="eyebrow">Literature</div><h2>Grounding the debate</h2><div class="litgrid" id="lit"></div>'))
    NOTES[i] = ["Three sources anchor this discussion: a measured estimate of the carbon cost of training large NLP models, which supports the opposing case in question two; and two further open-access sources on digital transformation and on the limits of techno-solutionism, listed with their access status.", 40]; i += 1

    S.append(slide("close", '<div class="closewrap"><div class="eyebrow">Synthesis</div><h2>Closing</h2><p class="takeaway">' + e(TAKEAWAY) + '</p></div>'))
    NOTES[i] = [TAKEAWAY + " Thank you — I'm happy to open the floor for the group discussion on question two.", 35]; i += 1

    notes_json = json.dumps({str(k): v for k, v in NOTES.items()}, ensure_ascii=False)
    js = JS.replace("NOTES_JSON", notes_json)
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Is Innovation Compulsory? · Session 2 Slides</title><style>{CSS}</style></head>
<body>
<div id="stage">{"".join(S)}<a id="home" href="../index.html">← Home</a><div id="count"></div><div id="hud"><i id="bar"></i></div></div>
<div class="nb"><button id="prev" aria-label="Previous slide">‹</button><button id="next" aria-label="Next slide">›</button><button id="nt">Notes (N)</button><button id="fs">Full screen (F)</button></div>
<div id="notes"></div>
<script id="litdata" type="application/json">LIT_JSON</script>
<script>{js}
(function(){{var d=JSON.parse(document.getElementById('litdata').textContent);document.getElementById('lit').innerHTML=d.map(function(x){{
  return '<div class="card"><b>'+x.t+'</b><span>'+x.a+'</span><p>'+x.n+'</p></div>'}}).join('')}})();
</script>
</body></html>
'''
    (ROOT / "slides").mkdir(exist_ok=True)
    (ROOT / "slides" / "index.html").write_text(doc.replace("LIT_JSON", json.dumps(LIT, ensure_ascii=False)), encoding="utf-8")
    sec = sum(v[1] for v in NOTES.values())
    print(f"slides: {len(S)}, total seconds: {sec} ({sec//60} min)")


def causal_svg():
    def box(x, y, w, h, t, color):
        lines = t.split("\\n")
        ty = y + h / 2 - (len(lines) - 1) * 13
        texts = "".join(f'<tspan x="{x+w/2}" dy="{0 if j==0 else 26}">{html.escape(ln)}</tspan>' for j, ln in enumerate(lines))
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" fill-opacity=".15" stroke="{color}" stroke-width="2.5"/><text x="{x+w/2}" y="{ty}" text-anchor="middle" fill="#eef6f2" font-size="20">{texts}</text>'
    return f'''<svg viewBox="0 0 980 420" role="img" aria-label="Causal chain: root causes, the technical system innovation can reach, and new side effects">
{box(20, 140, 260, 160, "Root causes\\nregulation, profit motive,\\ngeopolitics, consumption habits", "#f87171")}
{box(360, 140, 260, 160, "Technical system\\n(where innovation acts)\\nAI models, HPC, battery tech", "#2dd4bf")}
{box(700, 140, 260, 160, "New side effects\\ne-waste, model-training\\nenergy demand", "#fbbf24")}
<path d="M280 220 L360 220" stroke="#9db3aa" stroke-width="3" marker-end="url(#ah)"/>
<text x="320" y="205" fill="#9db3aa" font-size="17" text-anchor="middle">shapes</text>
<path d="M620 220 L700 220" stroke="#9db3aa" stroke-width="3" marker-end="url(#ah)"/>
<text x="660" y="205" fill="#9db3aa" font-size="17" text-anchor="middle">creates</text>
<path d="M830 300 C 830 370, 150 370, 150 300" stroke="#f87171" stroke-width="2.5" stroke-dasharray="7 6" fill="none" marker-end="url(#ah2)"/>
<text x="490" y="400" fill="#f87171" font-size="18" text-anchor="middle">techno-solutionism treats the middle box as the whole fix</text>
<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#9db3aa"/></marker>
<marker id="ah2" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#f87171"/></marker></defs>
</svg>'''


LIT = [
    {"t": "Energy and Policy Considerations for Deep Learning in NLP", "a": "Strubell, Ganesh & McCallum · ACL 2019 · arXiv:1906.02243",
     "n": "Training one large Transformer can emit roughly as much CO₂ as five cars over their lifetimes — the quantified cost behind Q2's opposing case."},
    {"t": "AI in Supply Chain Risk Assessment: A Systematic Review and Bibliometric Analysis", "a": "Jahin, Naife, Saha & Mridha · 2024 · arXiv:2401.10895",
     "n": "Reviews 54 studies (2015–2025) showing AI/ML measurably improves supply-chain risk detection and resilience — the evidence behind Q2's agreement case."},
    {"t": "A Systematic Literature Review of Digital Transformation", "a": "Egodawele et al. · Australasian Conference on Information Systems, 2022",
     "n": "174 peer-reviewed articles (2013–2021) on digital transformation as a survival driver — the premise Q1 puts under scrutiny."},
    {"t": "“Techno-solutionism a Fact or Farce?” A Critical Assessment of GenAI in Open and Distance Education", "a": "Olojede · Journal of Ethics in Higher Education, 2024",
     "n": "Defines techno-solutionism as uncritical faith that technology is neutral and sufficient — names the bias Q2's probing question targets."},
]
if __name__ == "__main__":
    build()
