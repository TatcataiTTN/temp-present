"""Generates slides/index.html for Session 4 (course review: Innovation Diffusion & Innovation
Management Systems, lecture pp.92-142). Run: python3 build/build_slides.py
All facts/figures come straight from the course PDF read in-session; nothing invented."""
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
e = html.escape

CSS = """
:root{--bg:#0b1512;--ink:#eef6f2;--mut:#9db3aa;--brand:#2dd4bf;--ok:#34d399;--no:#f87171;--q:#fbbf24}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#050a08;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;overflow:hidden}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center;background:radial-gradient(1200px 600px at 10% 0,#12332c,var(--bg));overflow:hidden}
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
.model{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.model svg{height:470px;width:auto}
.takeaway{margin-top:auto;font-size:25px;line-height:1.4;color:var(--brand);font-weight:600;max-width:1040px}
.close.slide{justify-content:center}
.closewrap{display:flex;flex-direction:column}
.two{display:grid;grid-template-columns:1fr 1fr;gap:22px;flex:1;min-height:0}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;flex:1;align-content:center}
.four{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;flex:1;align-content:center}
.pc{background:#10221d;border:1px solid #1f3a33;border-top:6px solid var(--t);border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;min-height:0}
.pc h3{margin:0 0 8px;font-size:21px}
.pc .meta{color:var(--mut);font-size:14px;margin:-4px 0 8px}
.pc p{margin:0 0 6px;font-size:16px;line-height:1.38;color:#d6e6df}
.pc p:last-child{margin-bottom:0}
.pc ul{margin:4px 0 0;padding-left:18px}
.pc li{font-size:15px;line-height:1.4;color:#d6e6df;margin:3px 0}
.pc b.lbl{color:var(--q);font-weight:700}
.card3{background:#10221d;border:1px solid #1f3a33;border-top:6px solid var(--t);border-radius:16px;padding:20px}
.card3 h3{margin:0 0 6px;font-size:19px}
.card3 .pct{color:var(--t);font-weight:800;font-size:15px;margin-bottom:6px}
.card3 p{margin:0;font-size:15px;line-height:1.38;color:#d6e6df}
.probe{margin-top:14px;font-size:19px;line-height:1.4;color:var(--q);font-style:italic;border-top:1px solid #1f3a33;padding-top:14px}
.probe b{font-style:normal}
.tablewrap table{width:100%;border-collapse:collapse;font-size:16px}
.tablewrap th{text-align:left;color:var(--q);font-size:13px;text-transform:uppercase;letter-spacing:.05em;padding:6px 10px;border-bottom:2px solid #1f3a33}
.tablewrap td{padding:10px 10px;border-bottom:1px solid #1f3a33;color:#d6e6df;vertical-align:top}
.tablewrap tr:last-child td{border-bottom:none}
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
<tr><td>4</td><td>Presentation (graded)</td><td>Full "Analysis of an Innovation" deck — 5-part structure, worked example provided (Selex Motors).</td></tr>
</tbody></table></div>"""
    add("", '<div class="section">5 · Assignments</div><h2>Four tasks attached to this lecture</h2>' + assign,
        "That's the theory. The lecture attaches four concrete tasks to it. One, an in-class analysis of innovation management's role with real examples. Two, a 30 to 40 minute group activity: pick a real product, score it on the five adoption attributes, place it on the S-curve, and propose strategies to cross the chasm into the Early Majority. Three, a roughly 300-word homework reflection on why a technologically advanced product failed during diffusion. And four, the graded presentation assignment, which comes with a full worked example we'll look at next.", 55)

    tmpl = """<div class="tablewrap"><table><thead><tr><th>Part</th><th>Covers</th></tr></thead><tbody>
<tr><td>1. Introduction</td><td>Title, problem statement, objective — why this innovation was chosen</td></tr>
<tr><td>2. Overview</td><td>Product/model description, type of innovation (Product/Process/Position/Paradigm), level (Disruptive/Incremental/Radical), target users</td></tr>
<tr><td>3. Core Analysis</td><td>Value proposition, key success factors, market adoption evidence</td></tr>
<tr><td>4. Impact &amp; Challenges</td><td>Positive impact, risks/barriers, full SWOT analysis</td></tr>
<tr><td>5. Conclusion</td><td>Summary, key lessons applicable elsewhere, Q&amp;A</td></tr>
</tbody></table></div>"""
    add("", '<div class="eyebrow">Assignment 4, the template</div><h2>"Analysis of an Innovation" — 5-part structure</h2>' + tmpl,
        "The presentation template has five parts. Introduction: title, problem statement, and why this innovation was chosen. Overview: what it is, its type — product, process, position or paradigm — its level, disruptive, incremental or radical, and its target users. Core analysis: value proposition, key success factors, evidence of market adoption. Impact and challenges: positive impact, risks, and a full SWOT. And conclusion: summary, key lessons, and Q&A.", 45)

    worked = "".join([
        pc("#2dd4bf", "The problem", "", '<p>Grab/Be/ShopeeFood drivers lose 3–8 hours a day charging EVs; gasoline price swings raise costs further.</p>'),
        pc("#60a5fa", "The solution", "", '<p>Selex Motors (founded 2018): smart EVs + standardized batteries + automated "2-minute battery swap" stations, Battery-as-a-Service.</p>'),
        pc("#fbbf24", "Type & level", "", '<p>Product innovation (EV + battery) combined with Business Model innovation (BaaS). Disruptive — replaces passive charging and gasoline refueling habits.</p>'),
        pc("#f87171", "Evidence of adoption", "", '<p>Hundreds of swap stations in Hanoi &amp; HCMC; &gt;90% driver satisfaction; drivers report 20–30% higher daily income from eliminated downtime.</p>'),
    ])
    add("", '<div class="eyebrow">Worked example in the lecture</div><h2>Selex Motors: EV ecosystem &amp; battery swapping</h2><div class="four">' + worked + '</div>',
        "The lecture's own worked example is Selex Motors, a Vietnamese company founded in 2018. The problem: delivery drivers lose three to eight hours a day charging electric motorbikes. Their solution: smart EVs, standardized batteries, and automated two-minute battery-swap stations sold as Battery-as-a-Service. It's classified as product innovation combined with business-model innovation, and disruptive, because it replaces the existing habit of passive charging. Evidence of adoption: hundreds of stations across Hanoi and Ho Chi Minh City, over 90 percent driver satisfaction, and drivers reporting 20 to 30 percent higher daily income once charging downtime disappears. The SWOT in the deck also flags the real risk: heavy upfront capital and the threat of big EV makers introducing their own proprietary battery standard.", 55)

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
<div class="nb"><button id="prev" aria-label="Previous slide">‹</button><button id="next" aria-label="Next slide">›</button><button id="nt">Notes (N)</button><button id="fs">Full screen (F)</button></div>
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
