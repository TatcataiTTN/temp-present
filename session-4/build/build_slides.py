"""Generates slides/index.html for Session 4 (course review: Innovation Diffusion & Innovation
Management Systems, lecture pp.92-142). Run: python3 build/build_slides.py
All facts/figures come straight from the course PDF read in-session; nothing invented."""
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
e = html.escape

CSS = """
:root{--bg:#0b1512;--ink:#eef6f2;--mut:#9db3aa;--brand:#2dd4bf;--ok:#34d399;--no:#f87171;--q:#fbbf24;
  --body-bg:#050a08;--stage-1:#12332c;--panel:#10221d;--panel-border:#1f3a33;--text2:#d6e6df;
  --chrome-bg:#12221d;--chrome-border:#2a4a41;--shot-bg:#000}
:root[data-theme="light"]{--bg:#f3f6f4;--ink:#15211d;--mut:#5b6b64;--brand:#0f766e;--ok:#15803d;--no:#b91c1c;--q:#b45309;
  --body-bg:#eef2ef;--stage-1:#e4efea;--panel:#ffffff;--panel-border:#dfe5e0;--text2:#2a3b35;
  --chrome-bg:#ffffff;--chrome-border:#dfe5e0;--shot-bg:#0b1512}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--body-bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;overflow:hidden;transition:background .2s}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center;background:radial-gradient(1200px 600px at 10% 0,var(--stage-1),var(--bg));overflow:hidden}
.slide{position:absolute;inset:0;padding:52px 80px 44px;display:none;flex-direction:column}
.slide.on{display:flex;animation:in .35s ease}
@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
h1{font-size:80px;letter-spacing:-.04em;margin:0;line-height:1.05}
h2{font-size:38px;letter-spacing:-.025em;margin:0 0 8px;line-height:1.15;max-width:1100px}
.kick{color:var(--brand);font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:16px;font-size:18px}
.sub{font-size:26px;color:var(--mut);margin:14px 0 0;max-width:1000px;line-height:1.35}
.title{justify-content:center}
.section{display:inline-block;font-size:15px;color:#04211d;background:var(--brand);font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:4px 12px;border-radius:999px;margin-bottom:14px}
.eyebrow{font-size:17px;color:var(--q);font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px}
.issue{font-size:21px;line-height:1.4;color:var(--mut);max-width:1080px}
.model{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;background:#0b1512;border-radius:18px;padding:14px}
.model svg{height:470px;width:auto}
.takeaway{margin-top:auto;font-size:25px;line-height:1.4;color:var(--brand);font-weight:600;max-width:1040px}
.close.slide{justify-content:center}
.closewrap{display:flex;flex-direction:column}
.two{display:grid;grid-template-columns:1fr 1fr;gap:22px;flex:1;min-height:0}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;flex:1;align-content:center}
.four{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;flex:1;align-content:center}
.pc{background:var(--panel);border:1px solid var(--panel-border);border-top:6px solid var(--t);border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;min-height:0}
.pc h3{margin:0 0 8px;font-size:21px}
.pc .meta{color:var(--mut);font-size:14px;margin:-4px 0 8px}
.pc p{margin:0 0 6px;font-size:16px;line-height:1.38;color:var(--text2)}
.pc p:last-child{margin-bottom:0}
.pc .shot{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;background:var(--shot-bg);border-radius:10px;overflow:hidden;margin:2px 0 8px}
.pc .shot img{max-width:100%;max-height:100%;object-fit:contain}
.pc .src{display:block;margin-top:6px;font-size:12px;color:var(--mut)}
.pc ul{margin:4px 0 0;padding-left:18px}
.pc li{font-size:15px;line-height:1.4;color:var(--text2);margin:3px 0}
.pc b.lbl{color:var(--q);font-weight:700}
.card3{background:var(--panel);border:1px solid var(--panel-border);border-top:6px solid var(--t);border-radius:16px;padding:20px}
.card3 h3{margin:0 0 6px;font-size:19px}
.card3 .pct{color:var(--t);font-weight:800;font-size:15px;margin-bottom:6px}
.card3 p{margin:0;font-size:15px;line-height:1.38;color:var(--text2)}
.probe{margin-top:14px;font-size:19px;line-height:1.4;color:var(--q);font-style:italic;border-top:1px solid var(--panel-border);padding-top:14px}
.probe b{font-style:normal}
.tablewrap table{width:100%;border-collapse:collapse;font-size:16px}
.tablewrap th{text-align:left;color:var(--q);font-size:13px;text-transform:uppercase;letter-spacing:.05em;padding:6px 10px;border-bottom:2px solid var(--panel-border)}
.tablewrap td{padding:10px 10px;border-bottom:1px solid var(--panel-border);color:var(--text2);vertical-align:top}
.tablewrap tr:last-child td{border-bottom:none}
.tablewrap td b.lbl{color:var(--q)}
.mech td:first-child{color:var(--ink);font-weight:700;width:19%}
.mech td:nth-child(2){color:#f8a9a9}
.mech td:nth-child(3){color:#8fd6c4}
.mech td:last-child{color:var(--mut);font-style:italic;width:21%}
.rawlist{display:grid;grid-template-columns:1fr 1fr;gap:2px 30px;margin:10px 0 0;padding:0;list-style:none;font-size:15px}
.rawlist li{line-height:1.45;color:var(--text2);padding:5px 0 5px 20px;position:relative;border-bottom:1px dashed var(--panel-border)}
.rawlist li::before{content:"→";position:absolute;left:0;color:var(--brand);font-weight:700}
.tagf{display:inline-block;font-size:10px;font-weight:800;letter-spacing:.03em;text-transform:uppercase;padding:1px 7px;border-radius:999px;margin-left:7px;color:#04211d;vertical-align:1px}
.pickrow{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:14px}
.pick{background:#0f2420;border:1px solid #1f4a3c;border-left:5px solid var(--ok);border-radius:10px;padding:12px 16px}
.pick b{color:var(--ok)}
.pick p{margin:4px 0 0;font-size:15px;color:#d6e6df;line-height:1.4}
.checkgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 26px;flex:1;min-height:0}
.checkgrid table{width:100%;border-collapse:collapse;font-size:12.5px}
.checkgrid th{text-align:left;color:var(--q);font-size:10.5px;text-transform:uppercase;letter-spacing:.04em;padding:4px 6px;border-bottom:2px solid var(--panel-border)}
.checkgrid td{padding:6px 6px;border-bottom:1px solid var(--panel-border);color:var(--text2);vertical-align:top}
.checkgrid td.st{text-align:center;width:28px}
.checkgrid td.ex{color:var(--mut);font-size:11.5px}
#hud{position:absolute;left:0;right:0;bottom:0;height:6px;background:var(--chrome-bg);z-index:5}#hud i{display:block;height:100%;width:0;background:var(--brand);transition:width .3s}
#count{position:absolute;right:28px;bottom:16px;color:var(--mut);font-size:16px;z-index:5}
#home{position:absolute;left:28px;bottom:16px;color:var(--mut);font-size:16px;text-decoration:none;z-index:5}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:#f6f7f4;color:#15211d;padding:16px 28px;font-size:17px;line-height:1.6;display:none;z-index:9;border-top:4px solid var(--brand)}
#notes.on{display:block}#notes small{display:block;color:#5b6b64;margin-bottom:6px}
.nb{position:fixed;top:12px;right:12px;z-index:9;display:flex;gap:8px}
.nb button{background:var(--chrome-bg);color:var(--ink);border:1px solid var(--chrome-border);border-radius:999px;padding:6px 14px;cursor:pointer;font-size:14px}
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
  (function(){
    var root=document.documentElement;
    function g(k){try{return localStorage.getItem(k)}catch(e){return null}}
    function s(k,v){try{localStorage.setItem(k,v)}catch(e){}}
    var saved=g('scamper-theme');if(saved)root.setAttribute('data-theme',saved);
    document.getElementById('th').onclick=function(){
      var cur=root.getAttribute('data-theme')||'dark';
      var next=cur==='light'?'dark':'light';
      root.setAttribute('data-theme',next);s('scamper-theme',next);
    };
  })();
  addEventListener('resize',fit);addEventListener('hashchange',function(){show((parseInt(location.hash.slice(1),10)||1)-1)});fit();show((parseInt(location.hash.slice(1),10)||1)-1);
})();
"""


def slide(cls, inner):
    return f'<section class="slide {cls}">{inner}</section>'


def s_curve_svg():
    return '''<svg viewBox="0 0 1000 480" role="img" aria-label="S-curve of diffusion with three phases: emergence, growth, maturity">
<line x1="60" y1="420" x2="940" y2="420" stroke="#2a4a41" stroke-width="2"/>
<line x1="60" y1="420" x2="60" y2="30" stroke="#2a4a41" stroke-width="2"/>
<text x="60" y="22" fill="#9db3aa" font-size="18">Growth</text>
<text x="900" y="408" text-anchor="end" fill="#9db3aa" font-size="18">Time</text>
<path d="M80 395 C 260 385, 330 330, 420 230 C 520 120, 650 70, 920 55" fill="none" stroke="#2dd4bf" stroke-width="5"/>
<line x1="330" y1="40" x2="330" y2="420" stroke="#1f3a33" stroke-dasharray="6 6"/>
<line x1="620" y1="40" x2="620" y2="420" stroke="#1f3a33" stroke-dasharray="6 6"/>
<text x="195" y="450" text-anchor="middle" fill="#60a5fa" font-size="18" font-weight="700">Phase 1: Emergence</text>
<text x="195" y="474" text-anchor="middle" fill="#9db3aa" font-size="15">high cost, high uncertainty</text>
<text x="475" y="450" text-anchor="middle" fill="#fbbf24" font-size="18" font-weight="700">Phase 2: Growth / Take-off</text>
<text x="475" y="474" text-anchor="middle" fill="#9db3aa" font-size="15">inflection point, rapid capture</text>
<text x="755" y="450" text-anchor="middle" fill="#f87171" font-size="18" font-weight="700">Phase 3: Maturity / Saturation</text>
<text x="755" y="474" text-anchor="middle" fill="#9db3aa" font-size="15">needs a new S-curve next</text>
</svg>'''


def adopter_svg():
    cats = [("Innovators", "2.5%", "#2dd4bf"), ("Early Adopters", "13.5%", "#60a5fa"),
            ("Early Majority", "34%", "#fbbf24"), ("Late Majority", "34%", "#fb923c"), ("Laggards", "16%", "#f87171")]
    w = 1000
    n = len(cats)
    cw = w / n
    body = ""
    import math
    for i, (name, pct, color) in enumerate(cats):
        cx = cw * i + cw / 2
        h = [70, 220, 310, 310, 140][i]
        y = 400 - h
        body += f'<rect x="{cx-cw/2+10}" y="{y}" width="{cw-20}" height="{h}" rx="8" fill="{color}" fill-opacity=".75"/>'
        body += f'<text x="{cx}" y="{y-16}" text-anchor="middle" fill="{color}" font-size="22" font-weight="800">{pct}</text>'
        body += f'<text x="{cx}" y="430" text-anchor="middle" fill="#eef6f2" font-size="16" font-weight="700">{name}</text>'
    return f'''<svg viewBox="0 0 {w} 470" role="img" aria-label="Rogers adopter categories bell curve: Innovators 2.5%, Early Adopters 13.5%, Early Majority 34%, Late Majority 34%, Laggards 16%">
<line x1="0" y1="400" x2="{w}" y2="400" stroke="#2a4a41" stroke-width="2"/>
{body}
</svg>'''


def funnel4_svg():
    steps = [("Search", "#2dd4bf", "scan for signals, threats, opportunities"), ("Select", "#60a5fa", "strategic choice: risk, resources, fit"),
             ("Implement", "#fbbf24", "R&D, design, prototype, launch"), ("Capture Value", "#f87171", "commercialize, scale, acquire value")]
    w, bw, gap = 1020, 220, 25
    body = ""
    for i, (name, color, sub) in enumerate(steps):
        x = i * (bw + gap)
        body += (f'<rect x="{x}" y="160" width="{bw}" height="140" rx="14" fill="{color}" fill-opacity=".16" stroke="{color}" stroke-width="2.5"/>'
                  f'<text x="{x+bw/2}" y="220" text-anchor="middle" fill="#eef6f2" font-size="23" font-weight="800">{name}</text>'
                  f'<text x="{x+bw/2}" y="260" text-anchor="middle" fill="#9db3aa" font-size="14">')
        words = sub.split(" ")
        lines, line = [], ""
        for w_ in words:
            if len(line + " " + w_) > 26:
                lines.append(line); line = w_
            else:
                line = (line + " " + w_).strip()
        lines.append(line)
        for j, ln in enumerate(lines):
            body += f'<tspan x="{x+bw/2}" dy="{0 if j==0 else 18}">{ln}</tspan>'
        body += '</text>'
        if i < len(steps) - 1:
            ax = x + bw + 4
            body += f'<path d="M{ax} 230 L{ax+17} 230" stroke="#9db3aa" stroke-width="3" marker-end="url(#af)"/>'
    return f'''<svg viewBox="0 0 {w} 420" role="img" aria-label="Innovation system funnel: Search, Select, Implement, Capture Value">
{body}
<defs><marker id="af" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#9db3aa"/></marker></defs>
</svg>'''


def fourps_svg():
    return '''<svg viewBox="0 0 1260 560" role="img" aria-label="The 4Ps innovation space: Product, Process, Position, Paradigm around a center">
<ellipse cx="620" cy="270" rx="400" ry="230" fill="#10221d" stroke="#1f3a33" stroke-width="2"/>
<circle cx="620" cy="270" r="85" fill="#2dd4bf" fill-opacity=".9"/>
<text x="620" y="277" text-anchor="middle" fill="#04211d" font-size="22" font-weight="800">INNOVATION</text>
<path d="M620 185 L620 70" stroke="#fbbf24" stroke-width="3" marker-end="url(#p1)" marker-start="url(#p1)"/>
<text x="620" y="50" text-anchor="middle" fill="#fbbf24" font-size="21" font-weight="800">Product</text>
<text x="620" y="30" text-anchor="middle" fill="#9db3aa" font-size="14">what we offer</text>
<path d="M710 270 L1030 270" stroke="#f87171" stroke-width="3" marker-end="url(#p2)" marker-start="url(#p2)"/>
<text x="1045" y="265" text-anchor="start" fill="#f87171" font-size="21" font-weight="800">Process</text>
<text x="1045" y="288" text-anchor="start" fill="#9db3aa" font-size="14">how we make/deliver it</text>
<path d="M530 270 L210 270" stroke="#60a5fa" stroke-width="3" marker-end="url(#p3)" marker-start="url(#p3)"/>
<text x="195" y="265" text-anchor="end" fill="#60a5fa" font-size="21" font-weight="800">Position</text>
<text x="195" y="288" text-anchor="end" fill="#9db3aa" font-size="14">who/where we sell to</text>
<path d="M620 355 L620 490" stroke="#a78bfa" stroke-width="3" marker-end="url(#p4)" marker-start="url(#p4)"/>
<text x="620" y="515" text-anchor="middle" fill="#a78bfa" font-size="21" font-weight="800">Paradigm</text>
<text x="620" y="536" text-anchor="middle" fill="#9db3aa" font-size="14">the mental model / business model</text>
<defs>
<marker id="p1" markerWidth="9" markerHeight="9" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#fbbf24"/></marker>
<marker id="p2" markerWidth="9" markerHeight="9" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#f87171"/></marker>
<marker id="p3" markerWidth="9" markerHeight="9" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#60a5fa"/></marker>
<marker id="p4" markerWidth="9" markerHeight="9" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#a78bfa"/></marker>
</defs>
</svg>'''


def iso_svg():
    labels = ["Value realization", "Leader's future vision", "Strategic orientation", "Innovation culture",
              "Knowledge exploitation", "Risk management", "Adaptability", "Systems approach"]
    n = len(labels)
    w = 1040
    cw = w / n
    body = ""
    for i, lab in enumerate(labels):
        x = i * cw + 6
        body += (f'<rect x="{x}" y="150" width="{cw-12}" height="140" rx="10" fill="#2dd4bf" fill-opacity=".16" stroke="#2dd4bf" stroke-width="2"/>')
        words = lab.split(" ")
        lines, line = [], ""
        for w_ in words:
            if len(line + " " + w_) > 11:
                lines.append(line); line = w_
            else:
                line = (line + " " + w_).strip()
        lines.append(line)
        ty = 150 + 70 - (len(lines) - 1) * 10
        body += f'<text x="{x+(cw-12)/2}" y="{ty}" text-anchor="middle" fill="#eef6f2" font-size="14" font-weight="700">'
        for j, ln in enumerate(lines):
            body += f'<tspan x="{x+(cw-12)/2}" dy="{0 if j==0 else 18}">{ln}</tspan>'
        body += '</text>'
        body += f'<path d="M{x+(cw-12)/2} 150 L{450+ (i-3.5)*8} 100" stroke="#9db3aa" stroke-width="1.5" stroke-opacity=".6"/>'
    return f'''<svg viewBox="0 0 {w} 320" role="img" aria-label="IMS eight principles fanning out from a central box">
<rect x="340" y="20" width="360" height="60" rx="12" fill="#60a5fa" fill-opacity=".9"/>
<text x="520" y="58" text-anchor="middle" fill="#04211d" font-size="22" font-weight="800">ISO 56000: IMS 8 Principles</text>
{body}
</svg>'''


def double_scurve_svg():
    return '''<svg viewBox="0 0 1180 500" role="img" aria-label="Two competing S-curves: electric vehicles lead around 1900, gasoline cars overtake by the 1920s, electric vehicles begin a second S-curve after 2010">
<line x1="60" y1="420" x2="1040" y2="420" stroke="#2a4a41" stroke-width="2"/>
<line x1="60" y1="420" x2="60" y2="30" stroke="#2a4a41" stroke-width="2"/>
<text x="60" y="22" fill="#9db3aa" font-size="17">Market share</text>
<text x="100" y="445" text-anchor="middle" fill="#9db3aa" font-size="14">~1900</text>
<text x="220" y="445" text-anchor="middle" fill="#9db3aa" font-size="14">1920s</text>
<text x="520" y="445" text-anchor="middle" fill="#9db3aa" font-size="14">mid-1900s</text>
<text x="780" y="445" text-anchor="middle" fill="#9db3aa" font-size="14">2010s</text>
<text x="1000" y="445" text-anchor="middle" fill="#9db3aa" font-size="14">today</text>
<line x1="220" y1="40" x2="220" y2="420" stroke="#1f3a33" stroke-dasharray="6 6"/>
<line x1="780" y1="40" x2="780" y2="420" stroke="#1f3a33" stroke-dasharray="6 6"/>
<path d="M100 380 C 160 260, 190 140, 220 100 C 320 60, 450 55, 520 70 C 650 85, 720 85, 780 90 C 860 92, 950 95, 1000 100" fill="none" stroke="#f87171" stroke-width="5"/>
<path d="M100 300 C 150 360, 190 395, 220 400 C 320 403, 450 404, 520 405 C 600 404, 680 400, 780 380 C 850 320, 930 180, 1000 110" fill="none" stroke="#2dd4bf" stroke-width="5"/>
<circle cx="100" cy="300" r="6" fill="#2dd4bf"/><circle cx="220" cy="400" r="6" fill="#2dd4bf"/><circle cx="1000" cy="110" r="6" fill="#2dd4bf"/>
<text x="40" y="300" text-anchor="end" fill="#2dd4bf" font-size="15" font-weight="700">EV leads early</text>
<text x="1010" y="80" fill="#2dd4bf" font-size="16" font-weight="800">Electric</text>
<text x="1010" y="130" fill="#f87171" font-size="16" font-weight="800">Gasoline (ICE)</text>
<text x="225" y="130" fill="#f87171" font-size="15" font-weight="700">Round 1: ICE wins</text>
<text x="225" y="148" fill="#9db3aa" font-size="13">Model T + cheap oil + electric starter</text>
<text x="630" y="360" text-anchor="middle" fill="#9db3aa" font-size="14">EV nearly disappears from the mass market</text>
<text x="785" y="330" fill="#2dd4bf" font-size="15" font-weight="700">Round 2: EV’s second S-curve</text>
<text x="785" y="348" fill="#9db3aa" font-size="13">Li-ion battery breakthroughs, Tesla, VinFast</text>
<rect x="900" y="40" width="130" height="380" fill="#fbbf24" fill-opacity=".06" stroke="#fbbf24" stroke-opacity=".3" stroke-dasharray="4 4"/>
<text x="965" y="470" text-anchor="middle" fill="#fbbf24" font-size="14" font-weight="700">toward parity</text>
</svg>'''


def ev_ice_bars_svg():
    """Head-to-head bar chart: Electric vs Gasoline, at 3 verified moments. Heights are qualitative
    (no invented precise percentages beyond the one sourced figure, ~1900 EV share)."""
    groups = [
        ("~1900", "28–38% of US cars", 150, "a minority too — steam cars still common", 110, "~1900, before gasoline pulled ahead"),
        ("~1912", "$1,750 roadster, losing ground", 110, "$650 Model T — less than half the price", 230, "1912: Ford’s price cut + Kettering’s starter"),
        ("mid-1920s", "nearly every EV maker bankrupt", 25, "the new standard, continent-wide", 320, "mid-1920s: the gap closes for good"),
    ]
    w = 1080
    gw = w / len(groups)
    body = ""
    for i, (era, ev_lab, ev_h, ice_lab, ice_h, foot) in enumerate(groups):
        gx = i * gw
        bw = 90
        ev_x = gx + gw / 2 - bw - 10
        ice_x = gx + gw / 2 + 10
        base = 400
        body += f'<rect x="{ev_x}" y="{base-ev_h}" width="{bw}" height="{ev_h}" rx="8" fill="#2dd4bf" fill-opacity=".85"/>'
        body += f'<rect x="{ice_x}" y="{base-ice_h}" width="{bw}" height="{ice_h}" rx="8" fill="#f87171" fill-opacity=".85"/>'
        body += f'<text x="{ev_x+bw/2}" y="{base-ev_h-12}" text-anchor="middle" fill="#2dd4bf" font-size="13" font-weight="700">{ev_lab}</text>'
        body += f'<text x="{ice_x+bw/2}" y="{base-ice_h-12}" text-anchor="middle" fill="#f87171" font-size="13" font-weight="700">{ice_lab}</text>'
        body += f'<text x="{gx+gw/2}" y="{base+30}" text-anchor="middle" fill="#eef6f2" font-size="20" font-weight="800">{era}</text>'
        body += f'<text x="{gx+gw/2}" y="{base+52}" text-anchor="middle" fill="#9db3aa" font-size="13">{foot}</text>'
        if i < len(groups) - 1:
            body += f'<line x1="{gx+gw-6}" y1="30" x2="{gx+gw-6}" y2="400" stroke="#1f3a33" stroke-dasharray="5 5"/>'
    return f'''<svg viewBox="0 0 {w} 480" role="img" aria-label="Electric versus gasoline cars head to head at three moments: 1900, 1912, and the mid-1920s">
<line x1="0" y1="400" x2="{w}" y2="400" stroke="#2a4a41" stroke-width="2"/>
<rect x="30" y="20" width="18" height="12" rx="3" fill="#2dd4bf" fill-opacity=".85"/><text x="54" y="30" fill="#9db3aa" font-size="14">Electric</text>
<rect x="130" y="20" width="18" height="12" rx="3" fill="#f87171" fill-opacity=".85"/><text x="154" y="30" fill="#9db3aa" font-size="14">Gasoline (ICE)</text>
{body}
</svg>'''


def bertha_benz_svg():
    stops = [
        ("Mannheim", "start, before dawn", "Aug 5, 1888 — Bertha Benz leaves with sons Eugen &amp; Richard, without telling her husband Karl", "#60a5fa"),
        ("Wiesloch", "Stadt-Apotheke pharmacy", "Buys ligroin from pharmacist Willi Ockel — the only place selling fuel solvent; later called “the world’s first gas station”", "#fbbf24"),
        ("Pforzheim", "arrival", "~100 km covered, uphill sections pushed/walked, a blocked fuel line cleared with her hatpin — the car works, in public, for a full day", "#2dd4bf"),
    ]
    n = len(stops)
    w = 1080
    cw = w / n
    body = ""
    for i, (city, sub, desc, color) in enumerate(stops):
        cx = i * cw + cw / 2
        body += f'<circle cx="{cx}" cy="90" r="14" fill="{color}"/>'
        body += f'<text x="{cx}" y="50" text-anchor="middle" fill="{color}" font-size="24" font-weight="800">{city}</text>'
        body += f'<text x="{cx}" y="72" text-anchor="middle" fill="#9db3aa" font-size="14">{sub}</text>'
        words = desc.split(" ")
        lines, line = [], ""
        for wd in words:
            if len(line + " " + wd) > 34:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        ty = 140
        body += f'<text x="{cx}" y="{ty}" text-anchor="middle" fill="#d6e6df" font-size="15">'
        for j, ln in enumerate(lines):
            body += f'<tspan x="{cx}" dy="{0 if j==0 else 21}">{ln}</tspan>'
        body += '</text>'
        if i < n - 1:
            body += f'<line x1="{cx+90}" y1="90" x2="{(i+1)*cw+cw/2-90}" y2="90" stroke="#9db3aa" stroke-width="3" marker-end="url(#bb)"/>'
    return f'''<svg viewBox="0 0 {w} 320" role="img" aria-label="Bertha Benz’s August 1888 drive from Mannheim through Wiesloch to Pforzheim, the first long-distance automobile trip">
{body}
<text x="{w/2}" y="300" text-anchor="middle" fill="#fbbf24" font-size="16" font-weight="700">The trip itself was the advertisement: proof, in public, that Karl Benz’s "horseless carriage" actually worked</text>
<defs><marker id="bb" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#9db3aa"/></marker></defs>
</svg>'''


def qr_adoption_svg():
    """Single S-curve for QR payment adoption in Vietnam, annotated with real data points."""
    return '''<svg viewBox="0 0 1080 460" role="img" aria-label="S-curve of QR code payment adoption in Vietnam from 2021 launch to 2025, with real data points">
<line x1="60" y1="400" x2="1020" y2="400" stroke="#2a4a41" stroke-width="2"/>
<line x1="60" y1="400" x2="60" y2="30" stroke="#2a4a41" stroke-width="2"/>
<text x="60" y="22" fill="#9db3aa" font-size="17">Share of daily transactions</text>
<path d="M90 380 C 200 370, 280 330, 360 270 C 460 190, 560 120, 760 85 C 860 72, 950 65, 990 60" fill="none" stroke="#2dd4bf" stroke-width="5" fill-opacity="0"/>
<circle cx="150" cy="365" r="7" fill="#60a5fa"/>
<text x="150" y="340" text-anchor="middle" fill="#60a5fa" font-size="15" font-weight="700">2021</text>
<text x="150" y="420" text-anchor="middle" fill="#9db3aa" font-size="13">VietQR launched by NAPAS</text>
<circle cx="560" cy="120" r="7" fill="#fbbf24"/>
<text x="560" y="95" text-anchor="middle" fill="#fbbf24" font-size="15" font-weight="700">2024</text>
<text x="560" y="420" text-anchor="middle" fill="#9db3aa" font-size="13">+106.7% volume YoY, ~2.1M outlets</text>
<circle cx="990" cy="60" r="7" fill="#2dd4bf"/>
<text x="930" y="40" text-anchor="middle" fill="#2dd4bf" font-size="15" font-weight="700">2025</text>
<text x="900" y="420" text-anchor="middle" fill="#9db3aa" font-size="13">over half of all transactions</text>
<line x1="60" y1="280" x2="1020" y2="280" stroke="#f87171" stroke-dasharray="6 6" stroke-opacity=".5"/>
<text x="1015" y="275" text-anchor="end" fill="#f87171" font-size="13">cash: still ~30%, not zero</text>
</svg>'''


def dvorak_svg():
    """Claimed (1944 Navy study, run by Dvorak himself) vs controlled (1956 GSA Strong study) results."""
    groups = [
        ("1944 “Navy study” (run by Dvorak himself)", [("Dvorak", 330, "#2dd4bf", "claimed +74% faster"), ("QWERTY", 190, "#9db3aa", "baseline")]),
        ("1956 GSA “Strong study” (independently controlled)", [("Dvorak", 230, "#2dd4bf", "matched, not exceeded"), ("QWERTY", 225, "#9db3aa", "baseline")]),
    ]
    w = 1080
    gw = w / 2
    body = ""
    for i, (label, bars) in enumerate(groups):
        gx = i * gw
        bw = 100
        gap = 30
        total = len(bars) * bw + gap
        start = gx + (gw - total) / 2
        for j, (name, h, color, note) in enumerate(bars):
            x = start + j * (bw + gap)
            base = 380
            body += f'<rect x="{x}" y="{base-h}" width="{bw}" height="{h}" rx="8" fill="{color}" fill-opacity=".85"/>'
            body += f'<text x="{x+bw/2}" y="{base-h-24}" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{name}</text>'
            body += f'<text x="{x+bw/2}" y="{base-h-8}" text-anchor="middle" fill="#9db3aa" font-size="12">{note}</text>'
        body += f'<text x="{gx+gw/2}" y="415" text-anchor="middle" fill="#eef6f2" font-size="17" font-weight="700">{label}</text>'
    return f'''<svg viewBox="0 0 {w} 440" role="img" aria-label="Dvorak versus QWERTY: the 1944 Navy study, run by Dvorak himself, claimed a large speed advantage; the independently controlled 1956 GSA study found Dvorak only matched prior QWERTY speed">
<line x1="0" y1="380" x2="{w}" y2="380" stroke="#2a4a41" stroke-width="2"/>
<line x1="{w/2}" y1="20" x2="{w/2}" y2="380" stroke="#1f3a33" stroke-dasharray="5 5"/>
{body}
</svg>'''


def vneid_timeline_svg():
    stops = [
        ("2021", "COVID-era launch", "Ministry of Public Security launches VNeID (Sept 10) for health declarations and domestic travel during the pandemic", "#60a5fa"),
        ("2023", "Nationwide rollout", "Expands beyond pandemic use into a general digital-ID app for citizens across the country", "#2dd4bf"),
        ("2025", "Mandatory: banks &amp; business", "Jan: biometric banking tied to VNeID. Jul: Decree 69 requires businesses to use it for e-government services; foreign residents need Level 2", "#fbbf24"),
        ("2026", "Mandatory: platforms", "Decree 320 requires 12 sectors of online platforms to link accounts to VNeID by Dec 31; opens to all legal foreign entrants Sept 28", "#f87171"),
    ]
    n = len(stops)
    w = 1080
    cw = w / n
    body = ""
    for i, (year, title, desc, color) in enumerate(stops):
        cx = i * cw + cw / 2
        body += f'<circle cx="{cx}" cy="70" r="16" fill="{color}"/><text x="{cx}" y="76" text-anchor="middle" fill="#04211d" font-size="15" font-weight="800">{i+1}</text>'
        body += f'<text x="{cx}" y="118" text-anchor="middle" fill="{color}" font-size="24" font-weight="800">{year}</text>'
        body += f'<text x="{cx}" y="142" text-anchor="middle" fill="#eef6f2" font-size="16" font-weight="700">{title}</text>'
        words = desc.split(" ")
        lines, line = [], ""
        for wd in words:
            if len(line + " " + wd) > 30:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        ty = 170
        body += f'<text x="{cx}" y="{ty}" text-anchor="middle" fill="#9db3aa" font-size="13.5">'
        for j, ln in enumerate(lines):
            body += f'<tspan x="{cx}" dy="{0 if j==0 else 19}">{ln}</tspan>'
        body += '</text>'
        if i < n - 1:
            body += f'<line x1="{cx+90}" y1="70" x2="{(i+1)*cw+cw/2-90}" y2="70" stroke="#9db3aa" stroke-width="3" marker-end="url(#vn)"/>'
    return f'''<svg viewBox="0 0 {w} 320" role="img" aria-label="VNeID timeline from 2021 COVID-era launch to 2026 mandatory platform linking">
{body}
<text x="{w/2}" y="300" text-anchor="middle" fill="#fbbf24" font-size="16" font-weight="700">Diffusion forced sector by sector, by decree — not earned attribute by attribute</text>
<defs><marker id="vn" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#9db3aa"/></marker></defs>
</svg>'''


def pc(t, title, meta, body_html):
    return f'<div class="pc" style="--t:{t}"><h3>{e(title)}</h3>' + (f'<div class="meta">{e(meta)}</div>' if meta else '') + body_html + '</div>'


def build():
    S, NOTES, i = [], {}, 1

    def add(cls, html_, notes, sec):
        nonlocal i
        S.append(slide(cls, html_))
        NOTES[i] = [notes, sec]
        i += 1

    add("title", '<div class="kick">USTH Innovation · Session 4 · Course Review, pp. 92–142</div>'
        '<h1>Diffusion &amp; Innovation Systems</h1><p class="sub">From S-curve adoption to running an Innovation Management System — and the four assignments that go with it</p>',
        "Good morning. Session 4 is a review of the second half of the lecture deck: innovation diffusion, the innovation system, the levels it operates at, and how enterprises formally manage innovation through an IMS. At the end we catalogue the four assignments this material comes with, including the worked Selex Motors example.", 35)

    add("", '<div class="section">1 · Innovation Diffusion</div><h2>What is innovation diffusion?</h2>'
        '<p class="issue"><b style="color:#eef6f2">Definition.</b> Diffusion is the process by which an innovation is communicated through certain channels, over time, among members of a social system. It is distinct from invention (creating something new) and innovation (bringing it to practical use) — diffusion is what happens after that, as the market actually adopts it.</p>',
        "Let's start with the definition straight from the lecture. Diffusion is the process by which an innovation is communicated through certain channels, over time, among members of a social system. The course is careful to separate three ideas: invention is creating something new, innovation is turning that into practical use, and diffusion is the separate process of the market actually adopting it afterward.", 35)

    add("", '<div class="eyebrow">The S-Curve of Diffusion</div><h2>Three phases, one curve</h2><div class="model">' + s_curve_svg() + '</div>',
        "The classic model is the S-curve. Phase 1, emergence: high cost, high uncertainty, slow development. Phase 2, growth or take-off: the product hits an inflection point, production costs fall, and it captures the market rapidly. Phase 3, maturity or saturation: growth slows as the market approaches capacity — and this is exactly the point where, per the lecture, the enterprise must seek a new S-curve, a disruptive innovation, to replace the current one.", 45)

    sm = "".join([
        pc("#60a5fa", "Phase 1: Emergence (2008–2010)", "slow start, market penetration",
           '<p>First smartphones (original iPhone, early Android HTC) appear in Vietnam. Devices are very expensive, 3G is in its infancy, most people still use "brick phones."</p>'),
        pc("#fbbf24", "Phase 2: Growth (2012–2018)", "explosive, mass adoption",
           '<p>Affordable Xiaomi, Oppo, Samsung A-series phones flood the market. Nationwide 3G/4G plus Zalo, Facebook, Grab make a smartphone a necessity for nearly everyone.</p>'),
        pc("#f87171", "Phase 3: Maturity (2020–present)", "saturation and stability",
           '<p>Almost every adult owns a smartphone. Few first-time buyers remain; competition shifts to the high end, or to the next upgrade cycle.</p>'),
    ])
    add("", '<div class="eyebrow">Worked example from the lecture</div><h2>The S-curve in Vietnam: smartphone adoption</h2><div class="three">' + sm + '</div>',
        "The lecture grounds this in Vietnam's own smartphone adoption. Phase 1, 2008 to 2010: the first iPhones and early Android phones arrive, very expensive, while most people still carry brick phones. Phase 2, 2012 to 2018: affordable Xiaomi, Oppo and Samsung A-series phones flood the market, and with nationwide mobile data plus Zalo, Facebook and Grab, owning a smartphone becomes a necessity, not a luxury. Phase 3, 2020 to today: almost every adult already owns one, so growth shifts from first-time buyers to upgrades and the high end.", 50)

    add("", '<div class="eyebrow">Everett Rogers’ Diffusion of Innovations</div><h2>Five adopter categories</h2><div class="model">' + adopter_svg() + '</div>',
        "Rogers' model splits any market into five adopter categories by how early they buy in. Innovators, 2.5 percent, are risk-tolerant and tech-enthusiastic. Early Adopters, 13.5 percent, are opinion leaders who signal legitimacy to the broader market. Early Majority and Late Majority, 34 percent each, are pragmatic or skeptical buyers who need proof of value or an established standard. Laggards, 16 percent, are traditionalists who resist change until the old option is phased out entirely.", 45)

    attrs = "".join([
        pc("#2dd4bf", "1. Relative Advantage", "", "<p>Is it significantly better than existing solutions — on price, speed, convenience?</p>"),
        pc("#60a5fa", "2. Compatibility", "", "<p>Does it fit existing values, habits and technical infrastructure?</p>"),
        pc("#fbbf24", "3. Complexity", "", "<p>Is it hard to understand or use? Higher complexity → slower adoption.</p>"),
        pc("#f87171", "4. Trialability", "", "<p>Can users experiment with it on a limited or free basis first?</p>"),
        pc("#a78bfa", "5. Observability", "", "<p>Are the results and benefits easily visible to others?</p>"),
    ])
    add("", '<div class="eyebrow">Tidd &amp; Bessant</div><h2>5 attributes that drive the rate of adoption</h2><div class="three" style="grid-template-columns:repeat(3,1fr);grid-auto-rows:1fr">' + attrs + '</div>',
        "Why do some innovations diffuse fast and others stall? Tidd and Bessant give five attributes to analyze. Relative advantage: is it significantly better on price, speed or convenience? Compatibility: does it fit existing habits and infrastructure? Complexity: the harder it is to understand, the slower it spreads. Trialability: can people try it on a limited or free basis first? And observability: are the benefits easy for others to see, which drives word-of-mouth adoption.", 55)

    add("", '<div class="section">2 · Innovation System</div><h2>The core process: Search → Select → Implement → Capture Value</h2><div class="model">' + funnel4_svg() + '</div>',
        "Section two: Tidd and Bessant frame innovation itself as a core business process with four stages. Search: scanning the environment for technological, market, social or regulatory signals, threats and opportunities. Select: a strategic decision balancing risk, resources and fit with strategy. Implement: translating the idea into reality through R&D, design and launch. And Capture Value: commercializing, scaling and actually acquiring the financial, social or knowledge value the innovation created.", 45)

    add("", '<div class="eyebrow">The innovation space</div><h2>The "4Ps" of innovation</h2><div class="model">' + fourps_svg() + '</div>',
        "Innovation can happen along four different dimensions, often called the 4Ps. Product innovation changes what the organization offers. Process innovation changes how it is created and delivered. Position innovation changes the context or market the product is introduced into. And Paradigm innovation is a fundamental shift in the underlying mental model or business model the organization runs on. Each axis can range from incremental to radical change.", 45)

    fourp_ex = "".join([
        pc("#fbbf24", "Product", "Evolution of the Mouse", "<p>1964 wooden first mouse → 1970s–80s Xerox/Apple models → 1980s–2000 mechanical → 2000s–present wireless.</p>"),
        pc("#f87171", "Process", "Ford's assembly line", "<p>Robotic welding and moving assembly lines changed how cars are built, not what a car is.</p>"),
        pc("#60a5fa", "Position", "Apple Watch", "<p>Launched as a convenient wearable, later repositioned primarily as a health- and fitness-tracking device for a different buyer.</p>"),
        pc("#a78bfa", "Paradigm", "Netflix", "<p>From mailing DVDs to a streaming subscription business — a new business model, not just a new product.</p>"),
    ])
    add("", '<div class="eyebrow">Lecture examples</div><h2>One company, four kinds of innovation</h2><div class="four">' + fourp_ex + '</div>',
        "The lecture gives one example per axis. Product innovation: the physical evolution of the computer mouse, from Engelbart's 1964 wooden box to today's wireless mice. Process innovation: Ford's robotic assembly line, changing how cars are built, not what a car is. Position innovation: the Apple Watch, first marketed as a convenient wearable, later repositioned primarily as a health and fitness tracker for a different kind of buyer. And paradigm innovation: Netflix, moving from mailing out DVDs to a streaming subscription business — a change in business model, not just in product.", 55)

    levels = "".join([
        pc("#2dd4bf", "Firm-Level (Internal)", "",
           '<ul><li>Strategy: clear intent, supportive leadership</li><li>Flexible, agile structure</li><li>Culture that rewards creativity</li><li>Learning from success and failure</li></ul>'),
        pc("#60a5fa", "Inter-Organizational", "networks & ecosystems",
           '<ul><li>Open innovation: internal + external sources</li><li>Supply chains &amp; alliances, university partnerships</li><li>Ecosystems &amp; platforms co-creating value</li></ul>'),
        pc("#fbbf24", "National & Regional", "external environment",
           '<ul><li>Institutional setup: universities, public R&amp;D</li><li>IP protection, standards, policy</li><li>Venture capital, tax incentives</li><li>Local cluster dynamics</li></ul>'),
    ])
    add("", '<div class="section">3 · Levels of an Innovation System</div><h2>No firm innovates alone</h2><div class="three">' + levels + '</div>',
        "No firm innovates alone, so the lecture frames innovation systems at three nested levels. Firm-level: the internal strategy, structure, relationships and learning mechanisms. Inter-organizational: networks and ecosystems — open innovation, supply chains, alliances, platforms. And national or regional systems: the external environment of universities, IP law, financial infrastructure and local cluster dynamics that either enable or constrain a firm's capacity to innovate.", 45)

    add("", '<div class="section">4 · Innovation Management in Enterprises</div><h2>Why manage innovation at all?</h2><div class="two">'
        + pc("#60a5fa", "The necessity", "", '<ul><li>Align innovation with strategic direction, resources, metrics</li><li>Keep strategy flexible as opportunities change</li><li>Balance exploiting today’s process with exploring new ones</li><li>Remove barriers and mindsets that stifle initiative</li><li>Ground innovation in real market and customer needs</li></ul>')
        + pc("#fbbf24", "The roles it plays", "", '<ul><li>Focuses the enterprise on its most critical innovation activities</li><li>Lets top management define a vision and allocate resources</li><li>Builds a shared, organization-wide awareness of innovation work</li><li>Surfaces bottlenecks through assessment</li><li>Integrates with the firm’s other management systems</li></ul>')
        + '</div>',
        "Why formally manage innovation rather than leave it ad hoc? The lecture lists the necessity: align innovation activities with strategy and resourcing, keep the strategy flexible, balance exploiting existing processes with exploring new ones, remove cultural barriers that stifle initiative, and keep innovation grounded in real market needs. Management's role is then to focus effort on the most critical activities, let leadership set a vision, build shared awareness, surface bottlenecks through assessment, and integrate with the firm's other systems.", 55)

    add("", '<div class="eyebrow">Innovation Management Systems (IMS)</div><h2>The fundamental elements, and 7 evaluation principles</h2><div class="two">'
        + pc("#2dd4bf", "4 fundamental elements", "", '<ul><li><b class="lbl">Context</b> of the organization: internal/external issues relevant to objectives</li><li><b class="lbl">Leadership</b>: vision, strategy, policy, roles</li><li><b class="lbl">Planning</b>: activities that address opportunities and risks</li><li><b class="lbl">Support</b>: people, finance, tools, IP strategy</li></ul>')
        + pc("#f87171", "7 evaluation principles", "", '<ul><li>Increasing value for the business</li><li>Challenging goals &amp; strategies</li><li>Mobilizing business development</li><li>Focusing on the future</li><li>Relevance to context, best practice</li><li>Flexibility &amp; comprehensiveness</li><li>Effectiveness &amp; reliability</li></ul>')
        + '</div>',
        "An Innovation Management System has four fundamental elements: the organization's context, leadership commitment that sets vision and policy, planning that turns that vision into specific activities, and support — the people, finance, tools and IP strategy needed to run it. Evaluating whether an innovation effort is working is then judged against seven principles: does it increase business value, challenge existing goals and strategy, mobilize development, focus on the future, stay relevant to context, remain flexible and comprehensive, and prove effective and reliable.", 55)

    add("", '<div class="eyebrow">The ISO 56000 series</div><h2>A global standard, built by 40+ countries</h2><div class="model">' + iso_svg() + '</div>',
        "This isn't just the lecturer's own framework — ISO Technical Committee 279, with contributions from over 40 countries, formalized it as the ISO 56000 series: 56000 covers fundamentals and vocabulary, 56002 the management system itself, 56003 tools for innovation partnerships, 56004 assessment, and further standards in development for IP and strategic intelligence management. The series rests on eight principles, shown here: value realization, the leader's future vision, strategic orientation, innovation culture, knowledge exploitation, risk management, adaptability, and a systems approach.", 50)

    assign = """<div class="tablewrap"><table><thead><tr><th>#</th><th>Type</th><th>What's required</th></tr></thead><tbody>
<tr><td>1</td><td>Analysis (in-class)</td><td>Analyze the role of innovation management in enterprises, with illustrative examples.</td></tr>
<tr><td>2</td><td>Group activity, 30–40 min</td><td>Pick a real product (EV, air fryer, GenAI tool, QR payments). Evaluate it on the 5 attributes, place it on the S-curve / adopter spectrum, propose 1–2 strategies to cross the chasm into the Early Majority.</td></tr>
<tr><td>3</td><td>Homework (~300 words)</td><td>Reflect on why a technologically advanced product failed during its diffusion phase.</td></tr>
<tr><td>5</td><td>Presentation (graded)</td><td>Full "Analysis of an Innovation" deck — 5-part structure, worked example provided (Selex Motors).</td></tr>
</tbody></table></div>"""
    add("", '<div class="section">5 · Assignments</div><h2>Four tasks attached to this lecture, numbered 1–3 and 5</h2>' + assign,
        "That's the theory. The lecture attaches four concrete tasks to it, numbered 1 through 3 and then 5 — slide 93's warm-up poll sits between the analysis and the group activity as the lecture's own item 2, so the graded presentation is item 5, not 4. One, an in-class analysis of innovation management's role with real examples. Two — counting the warm-up poll — is a 30 to 40 minute group activity: pick a real product, score it on the five adoption attributes, place it on the S-curve, and propose strategies to cross the chasm into the Early Majority. Three is a roughly 300-word homework reflection on why a technologically advanced product failed during diffusion. And five is the graded presentation assignment, which comes with a full worked example we'll look at next.", 55)

    tmpl = """<div class="tablewrap"><table><thead><tr><th>Part</th><th>Covers</th></tr></thead><tbody>
<tr><td>1. Introduction</td><td>Title, problem statement, objective — why this innovation was chosen</td></tr>
<tr><td>2. Overview</td><td>Product/model description, type of innovation (Product/Process/Position/Paradigm), level (Disruptive/Incremental/Radical), target users</td></tr>
<tr><td>3. Core Analysis</td><td>Value proposition, key success factors, market adoption evidence</td></tr>
<tr><td>4. Impact &amp; Challenges</td><td>Positive impact, risks/barriers, full SWOT analysis</td></tr>
<tr><td>5. Conclusion</td><td>Summary, key lessons applicable elsewhere, Q&amp;A</td></tr>
</tbody></table></div>"""
    add("", '<div class="eyebrow">Assignment 5, the template</div><h2>"Analysis of an Innovation" — 5-part structure</h2>' + tmpl,
        "The presentation template has five parts. Introduction: title, problem statement, and why this innovation was chosen. Overview: what it is, its type — product, process, position or paradigm — its level, disruptive, incremental or radical, and its target users. Core analysis: value proposition, key success factors, evidence of market adoption. Impact and challenges: positive impact, risks, and a full SWOT. And conclusion: summary, key lessons, and Q&A.", 45)

    worked = "".join([
        pc("#2dd4bf", "The problem", "", '<p>Grab/Be/ShopeeFood drivers lose 3–8 hours a day charging EVs; gasoline price swings raise costs further.</p>'),
        pc("#60a5fa", "The solution", "", '<p>Selex Motors (founded 2018): smart EVs + standardized batteries + automated "2-minute battery swap" stations, Battery-as-a-Service.</p>'),
        pc("#fbbf24", "Type & level", "", '<p>Product innovation (EV + battery) combined with Business Model innovation (BaaS). Disruptive — replaces passive charging and gasoline refueling habits.</p>'),
        pc("#f87171", "Evidence of adoption", "", '<p>Hundreds of swap stations in Hanoi &amp; HCMC; &gt;90% driver satisfaction; drivers report 20–30% higher daily income from eliminated downtime.</p>'),
    ])
    add("", '<div class="eyebrow">Worked example in the lecture</div><h2>Selex Motors: EV ecosystem &amp; battery swapping</h2><div class="four">' + worked + '</div>',
        "The lecture's own worked example is Selex Motors, a Vietnamese company founded in 2018. The problem: delivery drivers lose three to eight hours a day charging electric motorbikes. Their solution: smart EVs, standardized batteries, and automated two-minute battery-swap stations sold as Battery-as-a-Service. It's classified as product innovation combined with business-model innovation, and disruptive, because it replaces the existing habit of passive charging. Evidence of adoption: hundreds of stations across Hanoi and Ho Chi Minh City, over 90 percent driver satisfaction, and drivers reporting 20 to 30 percent higher daily income once charging downtime disappears. The SWOT in the deck also flags the real risk: heavy upfront capital and the threat of big EV makers introducing their own proprietary battery standard.", 55)

    # ---- Worked answers to the 4 assignments ----------------------------
    add("", '<div class="section">6 · Worked Answers</div><h2>Completing Exercises 1, 2, 3 &amp; 5 — four different ways of thinking, one example each</h2>'
        '<div class="issue">#1 is causal analysis, the Grab case. #2 is a raw group brainstorm on QR payments, filtered down. #3 is a researched narrative on the Dvorak keyboard, with dates and names. #5 is a structured business case on VNeID, Vietnam’s national digital ID, with real figures — four different examples, deliberately, so no single running story does all the work.</div>',
        "Before the wrap-up, four worked answers — deliberately in four different formats, because these assignments ask for four different kinds of thinking, and deliberately four different examples, so no one story is doing all the work. Exercise 1 wants causal analysis: name the mechanism, name the company it broke or saved — that's Grab. Exercise 2 wants a group brainstorm, raw ideas filtered down — that's QR payments. Exercise 3 wants a researched narrative with real dates and names — that's the Dvorak keyboard. And exercise 5 wants a structured business case with real figures — that's VNeID, Vietnam's national digital identity system.", 50)

    roles5 = """<div class="tablewrap"><table><thead><tr><th>Role of innovation management</th><th>What it means in practice</th><th>Evidence from Grab (detailed next)</th></tr></thead><tbody>
<tr><td><b class="lbl">1. Creating &amp; sustaining competitive advantage</b></td><td>Not a one-time edge — an edge that keeps renewing itself against copycats</td><td>EXP: hundreds of A/B tests a month keep fine-tuning matching/pricing on the same driver network — why no SEA rival, including Uber, could out-execute Grab on its own turf</td></tr>
<tr><td><b class="lbl">2. Integrating technology, market &amp; organization</b></td><td>Tech alone, or demand alone, isn’t innovation — it has to be assembled into one working system</td><td>The super-app flywheel: EXP (tech) + 47M monthly users (market) + licenses across 8 countries (organization) fused into one loop, each side feeding the others</td></tr>
<tr><td><b class="lbl">3. Transforming ideas into real value</b></td><td>An idea is worthless until it is actually captured as revenue, not just launched</td><td>GrabMaps: built in 2022 purely to serve Grab’s own drivers, later sold B2B. And 14 years from MyTeksi to Grab’s first-ever net profit, $200M in FY2025</td></tr>
<tr><td><b class="lbl">4. Building &amp; optimizing dynamic capabilities</b></td><td>The capability to keep re-tuning the business model as the market itself matures</td><td>Incentive spend deliberately cut from 13.3% of GMV (2022) to ≈10% (2024) while users kept growing 32.7M→47.2M — optimized, not accidental</td></tr>
<tr><td><b class="lbl">5. Managing risk &amp; optimizing resources</b></td><td>Scaling fast without scaling the firm’s exposure to fraud, regulation, or bad bets</td><td>GrabDefense protected 4.5B transactions from fraud in 2024; years spent securing financial licenses market by market before launching GrabFin/GXS Bank</td></tr>
</tbody></table></div>"""
    add("", '<div class="eyebrow">Exercise 1 — slide 92</div><h2>"Analyze the role of innovation management": the 5 official roles</h2>' + roles5,
        "Exercise 1 asks for the role of innovation management, and the course names five specific roles. One, creating and sustaining competitive advantage: not a one-time edge, but one that keeps renewing itself, which is exactly what Grab's EXP system does, running hundreds of A/B tests a month on the same driver network. Two, integrating technology, market and organization: Grab's super-app flywheel only works because the technology, the forty-seven million monthly users, and licenses across eight countries are fused into one loop. Three, transforming ideas into real value: GrabMaps started as an internal tool and became a B2B product, and it took fourteen years from MyTeksi to Grab's first-ever net profit. Four, building and optimizing dynamic capabilities: incentive spend was deliberately cut from 13.3 percent of GMV to about 10 percent while users kept growing, a tuned capability, not an accident. Five, managing risk and optimizing resources: GrabDefense protected four and a half billion transactions from fraud in 2024, and Grab spent years securing financial licenses market by market before launching lending or a digital bank. The next three slides develop the Grab case behind this table in full.", 85)

    add("", '<div class="eyebrow">Exercise 1, deep case</div><h2>Grab: resources only some founders start with</h2><div class="two">'
        + pc("#2dd4bf", "Family capital & domain expertise — verified", "",
             '<ul><li>Grandfather Tan Yuet Foh co-founded Tan Chong Motor in 1957, Malaysia’s Nissan distributor; father Tan Heng Chew is its president</li>'
             '<li>Anthony Tan worked as <b class="lbl">head of supply chain and marketing</b> at Tan Chong before leaving in 2012 — real logistics-network experience, not a random MBA idea</li>'
             '<li>Family motto per his own CNBC account: "you can sleep soundly when you are dead" — documented <i>innovation culture</i> (IMS principle 4) instilled before day one</li>'
             '<li>His own retelling adds 5 years of hands-on factory work, welding and assembling seats — a self-reported detail, not independently verified beyond his interviews</li></ul>')
        + pc("#fbbf24", "Seed capital & the Select decision — verified", "",
             '<ul><li>2011: Harvard competition, 2nd place, $25k — judges said Malaysia alone was too small, think Southeast Asia — that comment became the actual regional strategy</li>'
             '<li>His mother funded his first money ("I don’t understand, but I love you, so here is some money"); he added his own savings</li>'
             '<li>MyTeksi launched Kuala Lumpur, June 2012; first institutional round, $2M+ from Vertex Ventures, June 2013</li>'
             '<li>This is the <b class="lbl">Select</b> stage of Search→Select→Implement→Capture Value, forced by outside feedback, not planned in advance</li></ul>')
        + '</div>',
        "Exercise 1 asks for a real illustrative example, so here's one developed in depth: Grab. Start with resources most founders don't have. Anthony Tan's grandfather, Tan Yuet Foh, co-founded Tan Chong Motor in 1957, Malaysia's Nissan distributor, and his father is its president today. Before Grab, Anthony himself worked as head of supply chain and marketing at Tan Chong — real logistics experience, not a random idea from an MBA student. His own retelling adds years of hands-on factory work, welding and assembling seats, which is worth noting as self-reported rather than independently verified. The family motto he's quoted repeating — you can sleep soundly when you are dead — is documented innovation culture, instilled before the company existed. Then the Select decision: in 2011, a Harvard competition judge told his team Malaysia alone was too small, think Southeast Asia — that single comment became the actual regional strategy. His mother funded his first money, he added his own savings, and the first institutional round, over two million dollars from Vertex Ventures, came a year later in June 2013.", 85)

    add("", '<div class="eyebrow">Exercise 1, deep case, continued</div><h2>Grab: the three systems behind $22.1B in GMV</h2><div class="two">'
        + pc("#60a5fa", "EXP: the Search→Capture loop, running monthly", "",
             '<ul><li>Internal A/B-testing system: drivers/riders randomly split into groups, old vs. new matching or pricing logic compared on real outcomes</li>'
             '<li>Hundreds of experiments run every month — fares and matching are continuously re-optimized on the <i>same</i> driver network, no new product launch needed</li>'
             '<li>This is <b class="lbl">Capture Value</b> treated as a repeatable monthly process, not a one-time launch event</li></ul>')
        + pc("#f87171", "The flywheel, proven in Grab’s own filed numbers", "",
             '<ul><li>Incentive spend fell from <b class="lbl">13.3% of GMV (2022) → 9.9% (2023) → ≈10% (2024)</b>, while monthly users grew 32.7M → 41.3M → 47.2M</li>'
             '<li>FY2025 (filed Feb 2026): first-ever full-year net profit, <b class="lbl">$200M</b>, on $3.37B revenue (+20%) and $22.1B GMV (+21%) — after losses of $485M (2023) and $158M (2024)</li>'
             '<li><b class="lbl">GrabMaps:</b> built in 2022 purely to route Grab’s own drivers through motorbike alleys standard maps miss — then sold B2B once it worked. An innovation nobody set out to sell.</li></ul>')
        + '</div>',
        "Continuing the Grab case, at scale: three systems, not luck. First, EXP, Grab's internal A/B-testing system — drivers and riders randomly split into groups testing old versus new matching or pricing logic, hundreds of experiments running every month, continuously re-optimizing the same driver network without any new product launch. Second, the flywheel, proven in Grab's own filed numbers: incentive spend fell from 13.3 percent of GMV in 2022, to 9.9 in 2023, to about 10 in 2024, while monthly users grew from 32.7 million to 47.2 million — which is exactly why fiscal year 2025, filed this February, is Grab's first-ever full-year net profit, 200 million dollars, on 3.37 billion in revenue and 22.1 billion in GMV, after losses of 485 million and 158 million the two years before. Third, GrabMaps: built in 2022 purely to route Grab's own drivers through motorbike alleys that standard maps miss, then sold B2B once it worked — an innovation nobody set out to sell.", 85)

    add("", '<div class="eyebrow">Exercise 1, deep case, closing the loop to Session 2</div><h2>Grab: the same discipline, seen from the driver’s seat</h2><div class="two">'
        + '<div class="pc" style="--t:#a78bfa"><h3>Drivers organize</h3><div class="shot"><img src="../assets/sources/grab-union-phammisen-2026-09-22.png" alt="Facebook post from Thong tin Chinh phu, Sept 22 2026: Pham Mi Sen, Vice Chair of the Binh Tan Tech Motorbike-Taxi Union, speaking at an official meeting while wearing a Grab jacket"></div><p>Sept 22, 2026: Phạm Mi Sên, Vice Chair of the Bình Tân Tech Motorbike-Taxi Union, speaks at an official meeting — the gig drivers Grab once empowered are now organized labor with a seat at the table.</p><span class="src">Thông tin Chính phủ, official Facebook page. Photo: Hoa Lê.</span></div>'
        + '<div class="pc" style="--t:#60a5fa"><h3>Regulators review fees</h3><div class="shot"><img src="../assets/sources/grab-fee-review-ubctqg-2026-09-12.png" alt="Facebook post from Thong tin Chinh phu, Sept 12 2026: National Competition Commission reviewing Grab pricing and fee policy complaints"></div><p>Sept 12, 2026: Vietnam’s National Competition Commission (UBCTQG) opens a review of Grab’s pricing and fee policy, and asks other ride-hailing apps for related information.</p><span class="src">Thông tin Chính phủ, official Facebook page.</span></div>'
        + '</div>',
        "And the uncomfortable half of the same case, in the government's own words, posted days apart. September 22nd, 2026: Pham Mi Sen, vice chair of the Binh Tan tech motorbike-taxi union, speaks at an official meeting wearing a Grab jacket — the gig drivers Grab once empowered with flexible income are now organized labor with a seat at the table. Ten days earlier, September 12th: Vietnam's National Competition Commission opens a review of Grab's pricing and fee policy, and asks competing ride-hailing apps for related information. These are the exact same posts already sitting on session two of this site — we now have the business mechanics, from the previous slide, that explain why both happened in the same month.", 55)

    add("", '<div class="eyebrow">Exercise 1, deep case, the analysis</div><h2>Why this is an IMS problem, not just PR</h2>'
        '<p class="issue" style="margin-bottom:0">Sept 12–13, 2026: drivers in Hanoi, Ho Chi Minh City and Da Nang organized a two-day app log-off, coordinated through a 166,000-member driver community group. Multiple outlets (VnExpress, Bloomberg, AsiaNews) report commission deductions in the <b style="color:#eef6f2">30–50% range</b>, above Grab’s stated 20–27%; exact per-ride figures vary by source and are disputed. Documented prior rounds: January 2018 (commission 20%→23.6%) and December 2020 — this is at least the third cycle of the same dispute.</p><div class="two" style="margin-top:16px">'
        + pc("#f87171", "The evaluation-principle reading", "",
             '<ul><li>2025 is the exact year the 7 evaluation principles’ first item — <i>increasing value for the business</i> — finally succeeded (slide 20)</li>'
             '<li>The same filings show no comparable discipline applied to <i>relevance to context</i>: the course’s own principle meant to weigh local stakeholder impact</li></ul>')
        + pc("#fbbf24", "The transferable lesson", "",
             '<ul><li>An IMS optimized on one evaluation principle while ignoring another doesn’t fail quietly — it produces exactly this kind of headline</li>'
             '<li>“Role of innovation management” therefore includes knowing <i>which</i> principle a firm is currently skipping, not just which one it’s winning on</li></ul>')
        + '</div>',
        "So why does this belong in an answer about the role of innovation management? Because 2025 is the exact year the first evaluation principle, increasing value for the business, finally succeeded — and the same filings show no comparable discipline applied to relevance to context, the principle meant to weigh impact on real stakeholders. The transferable lesson: an IMS optimized on one evaluation principle while ignoring another doesn't fail quietly, it produces exactly this kind of headline. So the role of innovation management isn't just applying the principles — it's knowing which one your firm is currently skipping, not just which one it's winning on.", 65)

    add("", '<div class="eyebrow">Exercise 2 — the group activity</div><h2>Chosen product: QR code payments in Vietnam</h2><div class="model">' + qr_adoption_svg() + '</div>',
        "Exercise 2 asks a group to pick a real product and place it on the S-curve, and the lecture's own suggested list includes QR payments — we picked that one, deliberately different from exercises 3 and 4, and genuinely necessary: almost every daily purchase in Vietnam's cities now touches it. NAPAS launched VietQR in 2021 as the national standard, unifying what had been a fragmented mess of bank-by-bank and wallet-by-wallet codes. By 2024, QR payment volume surged 106.7 percent year on year, across roughly 2.1 million outlets. By 2025, QR payments make up over half of all transactions in the country — genuinely fast diffusion, though cash hasn't disappeared, it's still roughly 30 percent.", 60)

    add("", '<div class="eyebrow">Exercise 2, the ecosystem</div><h2>"QR payments" is not one app — it’s several, made to interoperate</h2><div class="four">'
        + pc("#60a5fa", "NAPAS / VietQR", "the switch + the standard", '<p>Vietnam’s national payment switch. Doesn’t hold consumer accounts itself — it’s the plumbing that makes a code generated by one bank scannable by any other bank or wallet.</p>')
        + pc("#a78bfa", "MoMo", "leading e-wallet", '<p>The most widely cited wallet brand (reported user counts vary by source, roughly 31–50M). Runs its own QR, cashback and vendor-onboarding programs on top of the shared standard.</p>')
        + pc("#fbbf24", "ZaloPay & other wallets", "the rest of the field", '<p>Built on Zalo’s existing messaging user base — the same "already-installed app" advantage Grab’s super-app strategy used, from Exercise 1.</p>')
        + pc("#2dd4bf", "Bank apps", "MB, Vietcombank, TPBank, Agribank…", '<p>Most Vietnamese still hold their money in a bank account first. VietQR is what lets a bank app scan the exact same code as MoMo or ZaloPay, instead of needing its own closed network.</p>')
        + '</div>',
        "Worth being precise about what we're actually analyzing: QR payments in Vietnam isn't one app, it's several, deliberately made to interoperate. NAPAS runs VietQR, the national switch and standard — it doesn't hold consumer accounts, it's the plumbing that lets a code from one bank get scanned by any other bank or wallet. MoMo is the most widely cited e-wallet brand, though reported user counts vary by source. ZaloPay and other wallets ride the same already-installed-app advantage that Grab's super-app strategy used, from exercise one. And bank apps — MB, Vietcombank, TPBank, Agribank and others — matter because most Vietnamese still hold their money in a bank account first; VietQR is what lets those apps scan the exact same code instead of needing a separate closed network.", 55)

    add("", '<div class="eyebrow">Exercise 2, step 1a — group brainstorm</div><h2>Chosen product: QR payments. Raw ideas, compatibility &amp; complexity.</h2>'
        '<p class="issue" style="margin-bottom:0">Rule for this step: quantity over quality. 20 ideas, each tagged with the attribute it attacks, and marked ✅ already live in the market today or 💡 a new idea the group is proposing. First 10:</p>'
        '<ul class="rawlist">'
        '<li>✅ One single national QR standard (VietQR) instead of a different code per bank/wallet <span class="tagf" style="background:#60a5fa">compatibility</span></li>'
        '<li>💡 Offline/low-data fallback mode for weak-signal areas <span class="tagf" style="background:#60a5fa">compatibility</span></li>'
        '<li>✅ Static printed QR glued to the xe ôm helmet or taxi dash — scan-only, no app pairing, works even on a near-dead phone <span class="tagf" style="background:#60a5fa">compatibility</span></li>'
        '<li>💡 USSD-style QR confirmation (*101#-type menu) for feature phones, no smartphone or data plan required <span class="tagf" style="background:#60a5fa">compatibility</span></li>'
        '<li>✅ ASEAN QR interoperability so a Vietnamese tourist in Bangkok, or a visitor here, scans with their own home app <span class="tagf" style="background:#60a5fa">compatibility</span></li>'
        '<li>💡 Voice-guided scan flow for elderly or low-literacy users <span class="tagf" style="background:#2dd4bf">complexity</span></li>'
        '<li>✅ Bigger on-screen confirmation + sound cue, so the payer visibly sees it went through <span class="tagf" style="background:#2dd4bf">complexity</span></li>'
        '<li>💡 One-tap "repeat last payment" for regulars — same xé ôm driver, same bánh mì stall, every morning <span class="tagf" style="background:#2dd4bf">complexity</span></li>'
        '<li>✅ Face-unlock to confirm a payment instead of typing a PIN — one fewer step at the register <span class="tagf" style="background:#2dd4bf">complexity</span></li>'
        '<li>✅ Cashback or lucky-draw for a user’s first 10 QR payments <span class="tagf" style="background:#a78bfa">trialability</span></li>'
        '</ul>',
        "Step one, a raw brainstorm, twenty ideas total — the first ten, on compatibility and complexity. On compatibility: one national standard, an offline fallback, a static printed QR that needs no app pairing, a USSD menu for feature phones, and ASEAN-wide interoperability for travelers. On complexity: a voice-guided flow, a louder success confirmation, a one-tap repeat-payment button for regulars, and face-unlock instead of a PIN. And the first trialability idea: cashback for a user's first ten payments.", 50)

    add("", '<div class="eyebrow">Exercise 2, step 1b — group brainstorm</div><h2>Chosen product: QR payments. Raw ideas, trialability, observability &amp; advantage.</h2>'
        '<p class="issue" style="margin-bottom:0">The remaining 10 ideas — same legend: ✅ already live, 💡 new idea.</p>'
        '<ul class="rawlist">'
        '<li>✅ Market/street-vendor onboarding kiosks, free QR sticker printed on the spot <span class="tagf" style="background:#a78bfa">trialability</span></li>'
        '<li>💡 Zero-fee "QR Tết" campaign during Lunar New Year, timed to a cash-heavy ritual (lì xì envelopes) <span class="tagf" style="background:#a78bfa">trialability</span></li>'
        '<li>💡 University canteen goes QR-only one day a week — students form the habit, then teach it to parents at home <span class="tagf" style="background:#a78bfa">trialability</span></li>'
        '<li>✅ "Paid by QR" badge displayed at the stall, visible to the next customer in line <span class="tagf" style="background:#fbbf24">observability</span></li>'
        '<li>💡 Published real-time national adoption counter (“X million payments today”) <span class="tagf" style="background:#fbbf24">observability</span></li>'
        '<li>💡 Public map/leaderboard of which wet markets have gone fully QR — social proof, and a little peer pressure on the ones that haven’t <span class="tagf" style="background:#fbbf24">observability</span></li>'
        '<li>✅ No-fee guarantee for small transactions under a set amount <span class="tagf" style="background:#f87171">rel. advantage</span></li>'
        '<li>💡 Instant refund flow for failed/duplicate scans, no waiting on hold <span class="tagf" style="background:#f87171">rel. advantage</span></li>'
        '<li>💡 Loyalty points that stack across banks/wallets via VietQR, instead of a separate point balance locked inside each app <span class="tagf" style="background:#f87171">rel. advantage</span></li>'
        '<li>💡 Chargeback-style buyer protection on QR transfers, which today are treated as irreversible — closing the trust gap with card payments <span class="tagf" style="background:#f87171">rel. advantage</span></li>'
        '</ul>',
        "The remaining nine ideas. More trialability: free vendor onboarding kiosks, a zero-fee Tet campaign timed to cash-gift season, and a QR-only canteen day at universities. On observability: a visible paid-by-QR badge, a national counter, and a public leaderboard of which markets have gone fully QR. And on relative advantage: a no-fee guarantee for small transactions, instant refunds, loyalty points that stack across apps, and chargeback-style protection on transfers. Twenty ideas on the table — now we filter.", 55)

    add("", '<div class="eyebrow">Exercise 2, checklist</div><h2>All 20 ideas, compared in one table</h2>'
        '<p class="issue" style="margin-bottom:8px;font-size:15px">9 of 20 are already live somewhere in the market — the group\'s real job is spotting the 11 genuine gaps, not reinventing what VietQR, MoMo or the banks already ship.</p>'
        + '<div class="checkgrid"><table><thead><tr><th>Idea</th><th>Attr.</th><th>St.</th><th>Already done by</th></tr></thead><tbody><tr><td>National QR standard (VietQR)</td><td>Compat.</td><td class="st">✅</td><td class="ex">NAPAS, since 2021</td></tr><tr><td>Static printed QR on helmet/dash</td><td>Compat.</td><td class="st">✅</td><td class="ex">street vendors, xe ôm, today</td></tr><tr><td>ASEAN QR interoperability</td><td>Compat.</td><td class="st">✅</td><td class="ex">piloted, VN–Thailand/Cambodia</td></tr><tr><td>Offline/low-data fallback</td><td>Compat.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>USSD QR for feature phones</td><td>Compat.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>Bigger confirmation + sound</td><td>Complex.</td><td class="st">✅</td><td class="ex">most bank/wallet apps</td></tr><tr><td>Face-unlock to confirm</td><td>Complex.</td><td class="st">✅</td><td class="ex">standard biometric option</td></tr><tr><td>Voice-guided scan flow</td><td>Complex.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>One-tap repeat payment</td><td>Complex.</td><td class="st">💡</td><td class="ex">partial, saved-merchant lists</td></tr><tr><td>Cashback, first 10 payments</td><td>Trial.</td><td class="st">✅</td><td class="ex">MoMo, ZaloPay, banks</td></tr></tbody></table><table><thead><tr><th>Idea</th><th>Attr.</th><th>St.</th><th>Already done by</th></tr></thead><tbody><tr><td>Vendor onboarding kiosks</td><td>Trial.</td><td class="st">✅</td><td class="ex">MoMo/VNPay market drives</td></tr><tr><td>Zero-fee “QR Tết” campaign</td><td>Trial.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>University QR-only canteen day</td><td>Trial.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>“Paid by QR” badge at stall</td><td>Observ.</td><td class="st">✅</td><td class="ex">ubiquitous stickers today</td></tr><tr><td>National adoption counter</td><td>Observ.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>Public QR-market leaderboard</td><td>Observ.</td><td class="st">💡</td><td class="ex">—</td></tr><tr><td>No-fee small transactions</td><td>Advant.</td><td class="st">✅</td><td class="ex">VietQR P2P, typically free</td></tr><tr><td>Instant refund, failed scans</td><td>Advant.</td><td class="st">💡</td><td class="ex">dispute exists, not instant</td></tr><tr><td>Loyalty points stack across apps</td><td>Advant.</td><td class="st">💡</td><td class="ex">—, fragmented today</td></tr><tr><td>Chargeback-style protection</td><td>Advant.</td><td class="st">💡</td><td class="ex">largely absent today</td></tr></tbody></table></div>',
        "A full checklist, side by side. Nine of the twenty ideas are already live somewhere in the market: the national standard, printed QR stickers, ASEAN interoperability, bigger confirmations, face-unlock, cashback drives, vendor kiosks, the paid-by-QR badge, and fee-free small transactions. The other eleven are genuine gaps: offline fallback, feature-phone support, voice guidance, one-tap repeat payment, a Tet campaign, a QR-only campus day, a public counter and leaderboard, instant refunds, cross-app loyalty points, and real chargeback protection. The group's actual job in this exercise is spotting that second column, not re-pitching the first.", 60)

    add("", '<div class="eyebrow">Exercise 2, step 2 — filter and justify</div><h2>Why these 2 beat the other 18</h2>'
        '<p class="issue" style="margin-bottom:0">Filter rule: attack the <i>weakest</i> attribute first. The scorecard shows complexity and observability already strong — the real gap is trust (relative advantage) and reach into the remaining ~30% cash users (compatibility).</p>'
        '<div class="tablewrap"><table><thead><tr><th>Attribute</th><th>Score (VietQR, 2025)</th></tr></thead><tbody>'
        '<tr><td><b>Relative advantage</b></td><td><b>Medium — fast and free for most, but failed/duplicate scans erode trust fast</b></td></tr>'
        '<tr><td><b>Compatibility</b></td><td><b>Medium — ~30% of transactions are still cash, concentrated among older or rural users</b></td></tr>'
        '<tr><td>Complexity</td><td>Low — scan and confirm, already simple</td></tr>'
        '<tr><td>Trialability</td><td>High — nearly free to try once</td></tr>'
        '<tr><td>Observability</td><td>High — ~2.1M outlets already display a QR code</td></tr>'
        '</tbody></table></div>'
        '<div class="pickrow">'
        '<div class="pick"><b>Pick 1: Instant refund flow for failed/duplicate scans</b><p>Directly repairs relative advantage, the real soft spot — one bad scan with no clear fix is what pushes a hesitant user straight back to cash.</p></div>'
        '<div class="pick"><b>Pick 2: Street-vendor onboarding kiosks with free QR stickers</b><p>Attacks compatibility exactly where the remaining 30% lives — informal vendors, not banked urban shoppers who already converted.</p></div>'
        '</div>',
        "Step two: filter against the scorecard. Complexity and observability are already strong, trialability is high since trying it is nearly free — the real gaps are relative advantage, because one bad scan erodes trust fast, and compatibility, the thirty percent still paying cash. Pick one: an instant refund flow for failed or duplicate scans, because one unresolved bad experience is exactly what pushes a hesitant user back to cash. Pick two: street-vendor onboarding kiosks with free QR stickers printed on the spot, because that attacks compatibility exactly where the remaining thirty percent actually lives — informal vendors, not the urban shoppers who already converted.", 70)

    add("", '<div class="eyebrow">Exercise 3, part 1 — the researched reflection</div><h2>Dvorak vs. QWERTY: the “better” keyboard that never won</h2><div class="model">' + dvorak_svg() + '</div>'
        '<p class="issue" style="margin-top:10px;font-size:16px">August Dvorak patented his layout in 1936, redesigning it around letter frequency to reduce finger travel. The famous 1944 Navy study, run by Dvorak himself, claimed Dvorak typists became 74% faster and 68% more accurate. It is now considered unreliable — the 1956 GSA-commissioned Strong study, run with proper controls, found retrained Dvorak typists only matched their old QWERTY speed. They never beat it.</p>',
        "Exercise 3's reflection, part one: the keyboard almost everyone who types has never heard of. August Dvorak patented his layout in 1936, redesigning it around letter frequency specifically to reduce finger travel. The famous 1944 Navy study, which he ran himself, claimed Dvorak typists became 74 percent faster and 68 percent more accurate. It's now considered unreliable: the 1956 GSA-commissioned Strong study, run with proper controls, found that retrained Dvorak typists only matched their old QWERTY speed. They never beat it.", 55)

    add("", '<div class="eyebrow">Exercise 3, part 2 — why "better" alone didn’t matter</div><h2>Two separate failures, stacked on top of each other</h2><div class="two">'
        + pc("#f87171", "Failure 1: the proof itself was flawed", "",
             '<ul><li>Dvorak was the Navy’s own top expert in time-and-motion studies — he analyzed his own invention’s results, a textbook conflict of interest</li>'
             '<li>Liebowitz &amp; Margolis (1990) found the Dvorak and QWERTY test groups were not equally skilled to begin with</li>'
             '<li>1950s–1970s follow-up research consistently found little or no real advantage</li></ul>')
        + pc("#60a5fa", "Failure 2: switching cost, even if it had been better", "",
             '<ul><li>Touch-typing is procedural memory — millions of trained typists, retraining is slow and risky mid-career</li>'
             '<li>Every keyboard, keycap mold and typing-class curriculum was already built for QWERTY — a network effect, not a technology gap</li>'
             '<li>This is <b class="lbl">compatibility</b> failing for a totally different reason than EVs: not missing infrastructure, but locked-in human skill</li></ul>')
        + '</div>',
        "Part two: why didn't a genuinely plausible improvement take over anyway? Two separate failures stack on top of each other. First, the proof itself was flawed: Dvorak was the Navy's own top expert in time-and-motion studies, so he analyzed his own invention's results, a textbook conflict of interest, and Liebowitz and Margolis later found the test groups weren't even equally skilled to start with. Second, even setting that aside, switching cost alone would have been enough: touch-typing is procedural memory, millions of people were already trained, and every keyboard and typing class was already built for QWERTY. That's compatibility failing for a completely different reason than EVs — not missing infrastructure, but locked-in human skill.", 65)

    add("", '<div class="eyebrow">Exercise 3, part 3 — the ~300-word write-up</div><h2>Why Dvorak never diffused: the full reflection</h2>'
        '<div class="issue" style="font-size:15px;line-height:1.42;max-width:1140px">In 1936, August Dvorak patented a keyboard layout redesigned around real letter frequency, placing the most-used letters on the home row to cut finger travel. On paper it was the more advanced product. Nearly a century later, almost no one uses it, and the reason is not only technology.</p>'
        '<p style="margin-top:6px">The first problem was the evidence itself. The best-known proof, a 1944 US Navy study, was designed and run by Dvorak — the Navy’s own leading expert in time-and-motion analysis — and reported startling gains: 74% faster typing, 68% fewer errors. Economists Liebowitz and Margolis later showed the test groups were not comparably skilled to begin with. When the US government’s General Services Administration ran an independently controlled follow-up in 1956, retrained Dvorak typists only matched their prior QWERTY speed. They never exceeded it.</p>'
        '<p style="margin-top:6px">The second problem was compatibility, structural in a different way than usual: touch-typing is procedural memory, built into the hands of millions of typists over years of training. Retraining was slow, risky to a working typist’s income, and every keyboard, typewriter mold, and school curriculum already assumed QWERTY. That installed base, not a conspiracy, is what economists call a network effect.</p>'
        '<p style="margin-top:6px">The lesson generalizes beyond keyboards: sometimes a challenger fails to diffuse not because the incumbent closes a gap, but because the evidence for the challenger’s advantage was never as solid as its proponents believed — and even a real advantage can lose to the sheer cost of relearning a skill millions of people already have.</p>',
        "And the full write-up. The first problem was the evidence itself: the best-known proof, a 1944 Navy study, was designed and run by Dvorak, the Navy's own leading expert in time-and-motion analysis, reporting startling gains that economists Liebowitz and Margolis later showed came from unevenly skilled test groups. When the government's own General Services Administration ran an independently controlled follow-up in 1956, retrained Dvorak typists only matched their prior speed, never exceeded it. The second problem was compatibility in a different sense than usual: touch-typing is procedural memory built into millions of trained hands, and every keyboard and curriculum already assumed QWERTY — an installed base, not a conspiracy. The general lesson: sometimes a challenger fails to diffuse not because an incumbent closes a gap, but because the evidence for its advantage was never as solid as believed, and even a real advantage can lose to the cost of relearning a skill millions already have.", 80)

    add("", '<div class="eyebrow">Exercise 5, part 1 — Introduction</div><h2>"VNeID: Vietnam’s National Digital Identity"</h2>'
        '<p class="issue" style="margin-top:8px;font-size:16px"><b style="color:#eef6f2">Problem statement:</b> paper ID cards and in-person, agency-by-agency paperwork mean queues, duplicate data entry, and real fraud risk — and the pandemic needed a trusted digital credential immediately, not eventually. <b style="color:#eef6f2">Why now:</b> by mid-2025, over 62 million citizen accounts were already issued, with daily logins up to four times 2023 levels — this is no longer an optional app, it’s becoming mandatory infrastructure.</p>',
        "Exercise 5's presentation, in full, with a deliberately different kind of example: not a company, a government system. Introduction: paper ID cards and in-person, agency-by-agency paperwork mean queues, duplicate data entry, and real fraud risk, and the pandemic needed a trusted digital credential immediately. Why now: by mid-2025, over 62 million citizen accounts were already issued, with daily logins up to four times 2023 levels — this is no longer an optional app, it's becoming mandatory infrastructure.", 50)

    add("", '<div class="eyebrow">Exercise 5, the rollout</div><h2>Diffusion forced sector by sector, by decree</h2><div class="model">' + vneid_timeline_svg() + '</div>',
        "Worth building the presentation's timeline around, because it's the opposite strategy from every other example in this deck. 2021: launched purely as a COVID-era health-declaration and travel tool. 2023: expanded into a general nationwide digital ID. 2025: biometric banking tied to it in January, then Decree 69 made it mandatory for businesses doing government e-services in July, with foreign residents required to hold Level 2. And 2026: Decree 320 requires twelve sectors of online platforms to link accounts to it by the end of the year, and opens it to all legal foreign entrants. Each stage didn't win adoption, it mandated it.", 60)

    add("", '<div class="eyebrow">Exercise 5, part 2 — Overview, with 2025 figures</div><h2>Type, level, and who’s required to use it</h2><div class="two">'
        + pc("#fbbf24", "2. Overview", "", '<p><b class="lbl">Type:</b> Paradigm innovation (replaces the citizen–government relationship itself: one verified digital identity instead of a paper card plus a separate login per agency) combined with Process innovation (procedures move online).</p><p><b class="lbl">Level:</b> Disruptive to a century-old paper-ID and in-person dossier system; rollout is incremental, sector by sector.</p><p><b class="lbl">Two tiers:</b> Level 1 (self-service in-app, limited features) vs. Level 2 (one in-person visit for biometric capture at a police station — still required for most mandatory services, the one friction point the mandate itself can’t remove).</p>')
        + pc("#2dd4bf", "2025–26, in numbers", "", '<ul><li>Over <b class="lbl">62M</b> citizen accounts + <b class="lbl">292M+</b> organization accounts (mid-2025); daily logins 3–6M, up to 4× 2023</li>'
             '<li>PM Directive 24 (Sep 2025): 25 full-process public services moved onto VNeID; paper copies dropped for them from Oct 2025</li>'
             '<li><b class="lbl">12</b> essential document types integrated per Resolution 66.22/NQ-CP; the <b class="lbl">5</b> required for fee relief: birth certificate, bank/payment account, social-security account, phone number, e-health book</li>'
             '<li>Fee relief from Aug 2026: 34 procedures 100% free, 8 high-value transactions cut 10–50%, for citizens with 5 core documents linked</li></ul>')
        + '</div>',
        "Overview, with figures through 2026. Type of innovation: paradigm innovation, replacing the citizen-government relationship itself, combined with process innovation as procedures move online. Level: disruptive to a century-old paper-ID system, rollout incremental, sector by sector. Worth noting two tiers exist: Level 1 is self-service in-app, but Level 2, needed for most mandatory services, still requires one in-person visit for biometric capture at a police station — the one friction point even a legal mandate can't remove. In the numbers: over 62 million citizen accounts and 292 million-plus organization accounts by mid-2025, daily logins of 3 to 6 million. A prime ministerial directive in September 2025 moved 25 full-process public services onto VNeID, dropping paper copies for them from October. Twelve essential document types are integrated under Resolution 66.22, with five required for the fee relief: birth certificate, bank or payment account, social-security account, phone number, and e-health book. And from August 2026, citizens who've linked five core documents get 34 procedures fully fee-free and ten to fifty percent off eight high-value transactions.", 80)

    add("", '<div class="eyebrow">Exercise 5, part 3 — Core Analysis, Impact &amp; Challenges</div><h2>Value proposition and SWOT</h2><div class="two">'
        + pc("#60a5fa", "3–4. Core analysis, impact & SWOT", "",
             '<p><b class="lbl">Value proposition:</b> one verified identity, reusable across every agency and, increasingly, banks and platforms — fewer queues for citizens, less duplicate fraud-prone paperwork for the state.</p>'
             '<ul><li><b class="lbl">S:</b> quantified, not just adoption — by Sept 2026, 768,000 eligibility look-ups and 14,700+ fee-free dossiers saved citizens ≈232.6M VND directly</li>'
             '<li><b class="lbl">W:</b> an account can be <i>locked</i> if its linked phone number isn’t registered in the citizen’s own name (Decree 320) — a mandate with a real lockout edge</li>'
             '<li><b class="lbl">O:</b> a signed plan to link VNeID with Singapore’s and Laos’ ID systems, expanding across ASEAN — the "super app" ambition, moving</li>'
             '<li><b class="lbl">T:</b> fake-VNeID phishing apps are real — one Đà Nẵng victim lost 129M VND (Jul 2025); police run a single verified hotline, 1900.0368, precisely because trust in the brand is now worth exploiting</li></ul>')
        + pc("#f87171", "5. Conclusion", "", '<p><b class="lbl">Summary:</b> VNeID doesn’t win adoption attribute by attribute like every other example in this deck — it uses regulation to force compatibility directly, sector by sector.</p><p><b class="lbl">Key lesson, stated as a rule:</b> when a firm or state controls the channel citizens must use anyway (banking rails, e-government portals), diffusion can be legislated, not earned — but that shortcut borrows against public trust, and the bill comes due at the first major failure or breach.</p>')
        + '</div>',
        "Core analysis: the value proposition is one verified identity, reusable across every agency and, increasingly, banks and platforms. The SWOT, now quantified. Strength: by September 2026, 768,000 eligibility look-ups and over 14,700 fee-free dossiers had saved citizens about 232.6 million dong directly, not just adoption numbers. Weakness: an account can actually be locked if its linked phone number isn't registered in the citizen's own name, under Decree 320, a mandate with a real lockout edge. Opportunity: a signed plan to link VNeID with Singapore's and Laos's identity systems, expanding across ASEAN, the super-app ambition actually moving. Threat: fake VNeID phishing apps are a real, documented problem — one victim in Da Nang lost 129 million dong in July 2025 after installing a fake one — and police now run a single verified hotline precisely because the brand's trust is itself worth exploiting. Conclusion, the transferable lesson for the whole deck: VNeID doesn't win adoption attribute by attribute like Grab, QR payments or the Dvorak keyboard did — it uses regulation to force compatibility directly. When a firm or state controls the channel citizens must use anyway, diffusion can be legislated, not earned — but that shortcut borrows against public trust, and the bill comes due at the first major failure or breach.", 85)

    add("close", '<div class="closewrap"><div class="eyebrow">Wrap-up</div><h2>Diffusion is not automatic — it has to be managed</h2>'
        '<p class="takeaway">Technological excellence alone does not guarantee success; commercial victory relies on market adoption. Managers must actively design products and strategies for each adopter segment, not assume the S-curve will climb itself.</p>'
        '<div class="probe"><b>Carrying this forward.</b> HụiKeeper (Session 1) and Grab/Be/Xanh SM (Session 2) are both sitting somewhere on this same S-curve. Where would you place each one — and on which of the 5 attributes are they weakest?</div></div>',
        "To close, the lecture's own key takeaway: technological excellence alone does not guarantee success, commercial victory relies on market adoption, and diffusion is not automatic — managers must actively design products and strategies tailored to each adopter segment. It's worth carrying this forward: both HụiKeeper from session one and Grab, Be and Xanh SM from session two sit somewhere on exactly this same S-curve. Where would you place each one, and which of the five adoption attributes is each one weakest on? That's a good bridge into the group activity.", 55)

    notes_json = json.dumps({str(k): v for k, v in NOTES.items()}, ensure_ascii=False)
    js = JS.replace("NOTES_JSON", notes_json)
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Diffusion &amp; Innovation Systems · Session 4 Slides</title><style>{CSS}</style></head>
<body>
<div id="stage">{"".join(S)}<a id="home" href="../index.html">← Home</a><div id="count"></div><div id="hud"><i id="bar"></i></div></div>
<div class="nb"><button id="prev" aria-label="Previous slide">‹</button><button id="next" aria-label="Next slide">›</button><button id="nt">Notes (N)</button><button id="fs">Full screen (F)</button><button id="th" aria-label="Toggle light or dark theme">◐</button></div>
<div id="notes"></div>
<script>{js}</script>
</body></html>
'''
    (ROOT / "slides").mkdir(exist_ok=True)
    (ROOT / "slides" / "index.html").write_text(doc, encoding="utf-8")
    sec = sum(v[1] for v in NOTES.values())
    print(f"slides: {len(S)}, total seconds: {sec} ({sec//60} min)")


if __name__ == "__main__":
    build()
