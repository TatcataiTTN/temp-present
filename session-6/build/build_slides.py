"""Session 6 — Innovative Technology (Chapter 3): AI in SMEs, Blockchain, Network Platforms.
Theme: USTH-DSES light blue. Run: python3 build/build_slides.py
Source: 2026- Chapter 3- Innovation Manegement 22.10.pdf (Dr. Do Thi Hai).
Blockchain characteristics/architecture slides also draw on a classmate group's (HNUE, not our group)
database-course deck "Dac tinh chinh cua Blockchain.pptx" (Nhom 10, Khoa CNTT - DH Su Pham Ha Noi),
cited explicitly as a secondary source."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS = """
:root{--bg:#0a1626;--ink:#eef6fc;--mut:#9fb3c8;--brand:#38bdf8;--ok:#34d399;--no:#f87171;--q:#fbbf24}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#050d18;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;overflow:hidden}
#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center;background:radial-gradient(1200px 600px at 10% 0,#102a44,var(--bg));overflow:hidden}
.slide{position:absolute;inset:0;padding:46px 76px 40px;display:none;flex-direction:column}
.slide.on{display:flex;animation:in .35s ease}
@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
h1{font-size:68px;letter-spacing:-.04em;margin:0;line-height:1.05}
h2{font-size:32px;letter-spacing:-.02em;margin:0 0 6px;line-height:1.18;max-width:1120px}
.kick{color:var(--brand);font-weight:700;letter-spacing:.13em;text-transform:uppercase;margin-bottom:14px;font-size:16px}
.sub{font-size:21px;color:var(--mut);margin:12px 0 0;max-width:1020px;line-height:1.35}
.title{justify-content:center}
.section{display:inline-block;font-size:13px;color:#03202f;background:var(--brand);font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:3px 11px;border-radius:999px;margin-bottom:10px}
.eyebrow{font-size:15px;color:var(--q);font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px}
.qtext{font-size:18px;line-height:1.42;color:#d8e6f2;max-width:1120px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;min-height:0}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;flex:1;align-content:center}
.six{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:12px;flex:1;min-height:0}
.pc{background:#0e2238;border:1px solid #1e3a57;border-top:5px solid var(--t);border-radius:14px;padding:14px 18px;display:flex;flex-direction:column;min-height:0;overflow:auto}
.pc h3{margin:0 0 6px;font-size:17px}
.pc .meta{color:var(--mut);font-size:12.5px;margin:-3px 0 7px}
.pc p{margin:0 0 5px;font-size:13.5px;line-height:1.36;color:#d8e6f2}
.pc p:last-child{margin-bottom:0}
.pc ul{margin:3px 0 6px;padding-left:16px}
.pc li{font-size:13px;line-height:1.35;color:#d8e6f2;margin:2px 0}
.pc b.lbl{color:var(--q);font-weight:700}
.tablewrap table{width:100%;border-collapse:collapse;font-size:13.5px}
.tablewrap th{text-align:left;color:var(--q);font-size:11px;text-transform:uppercase;letter-spacing:.04em;padding:5px 8px;border-bottom:2px solid #1e3a57}
.tablewrap td{padding:7px 8px;border-bottom:1px solid #1e3a57;color:#d8e6f2;vertical-align:top}
.statrow{display:flex;gap:14px;margin-top:10px}
.stat{flex:1;background:#0e2238;border:1px solid #1e3a57;border-radius:12px;padding:12px 14px;text-align:center}
.stat b{display:block;font-size:30px;color:var(--brand)}
.stat span{font-size:12.5px;color:var(--mut)}
.src{font-size:12px;color:var(--mut);font-style:italic;margin-top:auto;padding-top:8px}
.examband{background:#1a1a0f;border:1px solid #3a3a1f;border-radius:12px;padding:12px 18px;font-size:15px;color:var(--q);font-weight:700;text-align:center}
#hud{position:absolute;left:0;right:0;bottom:0;height:6px;background:#0e2238;z-index:5}#hud i{display:block;height:100%;width:0;background:var(--brand);transition:width .3s}
#count{position:absolute;right:28px;bottom:16px;color:var(--mut);font-size:16px;z-index:5}
#home{position:absolute;left:28px;bottom:16px;color:var(--mut);font-size:16px;text-decoration:none;z-index:5}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:34vh;overflow:auto;background:#f0f7fc;color:#0a1626;padding:16px 28px;font-size:17px;line-height:1.6;display:none;z-index:9;border-top:4px solid var(--brand)}
#notes.on{display:block}#notes small{display:block;color:#5b7186;margin-bottom:6px}
.nb{position:fixed;top:12px;right:12px;z-index:9;display:flex;gap:8px}
.nb button{background:#0e2238;color:var(--ink);border:1px solid #27476b;border-radius:999px;padding:6px 14px;cursor:pointer;font-size:14px}
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
    var n2=notes[cur+1]||['',0];document.getElementById('notes').innerHTML='<small>Speaker notes \\u00b7 slide '+(cur+1)+'</small>'+n2[0];
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


def pc(t, title, body_html):
    return f'<div class="pc" style="--t:{t}"><h3>{title}</h3>' + body_html + '</div>'


def build():
    S, NOTES, i = [], {}, 1

    def add(cls, html_, notes, sec):
        nonlocal i
        S.append(slide(cls, html_))
        NOTES[i] = [notes, sec]
        i += 1

    add("title", '<div class="kick">USTH Innovation &middot; Session 6 &middot; Chapter 3</div>'
        '<h1>Innovative Technology</h1><p class="sub">AI in SMEs &middot; Blockchain &middot; Network Platforms</p>'
        '<div class="examband" style="margin-top:28px;max-width:640px">Science &amp; Technology Innovation Management &mdash; Dr. Do Thi Hai, USTH Master Programme</div>',
        "Chapter 3 covers three innovative-technology case studies: AI adoption by SMEs, Blockchain in enterprise and supply chains, and network platforms.", 20)

    add("", '<div class="section">1. AI in SMEs</div><h2>Three ways SMEs adopt AI</h2>'
        + '<div class="three">'
        + pc("#38bdf8", "Off-the-shelf / Cloud AI", '<p>SaaS running on cloud platforms, low upfront investment.</p><p><b class="lbl">Ex:</b> chatbots, marketing tools, AI invoice recognition.</p>')
        + pc("#fbbf24", "Embedded AI", '<p>AI features built into third-party core software.</p><p><b class="lbl">Ex:</b> predictive sales analytics in CRMs (Salesforce, HubSpot), ad-optimization on Google/Meta.</p>')
        + pc("#f87171", "Custom AI Solutions", '<p>Bespoke algorithms for unique operations.</p><p><b class="lbl">Trade-off:</b> expensive, needs dedicated data infra and ML engineers &mdash; least common in SMEs.</p>')
        + '</div>',
        "Three adoption paths, cheapest and most common to most expensive and rarest: off-the-shelf cloud AI, embedded AI inside existing software, and fully custom AI solutions.", 40)

    add("", '<div class="section">1. AI in SMEs</div><h2>Drivers, barriers, and Vietnam in numbers</h2>'
        + '<div class="two">'
        + pc("#34d399", "Strategic drivers", '<ul><li>Cost &amp; productivity: automating repetitive admin/customer-service tasks</li>'
             '<li>Decision support: forecasting demand, managing inventory/supply-chain risk</li>'
             '<li>Hyper-personalized customer experience</li></ul>')
        + pc("#f87171", "Adoption barriers", '<ul><li>Skills gap &amp; talent shortage</li>'
             '<li>Data quality: fragmented, unstructured data</li>'
             '<li>Financial constraints, unclear short-term ROI</li>'
             '<li>Legal &amp; security risk (privacy, compliance)</li></ul>')
        + '</div>'
        + '<div class="statrow"><div class="stat"><b>93%</b><span>Vietnam SMEs using &ge;1 AI tool &mdash; highest of 6 surveyed APAC markets</span></div>'
        + '<div class="stat"><b>92%</b><span>report AI improves productivity</span></div>'
        + '<div class="stat"><b>89%</b><span>report AI cuts operating cost</span></div></div>'
        + '<p class="src">Source: Deloitte Access Economics &amp; Meta (2025) survey, as cited in lecture slide 12&ndash;13; OECD (2021) policy framework, slide 11.</p>',
        "Drivers are cost, decision support, and personalization. Barriers are skills, data quality, ROI uncertainty, and legal risk. Vietnam leads the region: 93 percent of SMEs have adopted at least one AI tool.", 50)

    add("", '<div class="section">2. Blockchain</div><h2>What is Blockchain, and why it matters for supply chains</h2>'
        + '<div class="two">'
        + pc("#38bdf8", "Core idea", '<p>A distributed, decentralized ledger: data is grouped into blocks linked by cryptographic hashes, each block referencing the one before it &mdash; a continuous chain.</p>'
             '<p><b class="lbl">Characteristics:</b> transparency (visible to authorized members), immutability (recorded data cannot be altered), smart contracts (automated execution when conditions are met).</p>')
        + pc("#fbbf24", "Problem it solves", '<p>Industry reality: information is fragmented across stakeholders (Farm &rarr; Logistics &rarr; Warehouse &rarr; Supermarket); manual traceability is slow and costly.</p>'
             '<p>Blockchain does <b>not</b> replace legacy systems &mdash; it acts as a trusted verification layer connecting them.</p>')
        + '</div>',
        "Blockchain is a distributed, immutable ledger. In supply chains it fixes the fragmentation problem: no single stakeholder trusts another's records, so blockchain becomes a shared verification layer, not a replacement for existing systems.", 45)

    add("", '<div class="section">2. Blockchain</div><h2>Food traceability case: Farm to Table</h2>'
        + '<div class="tablewrap"><table><thead><tr><th>Stage</th><th>What happens on-chain</th></tr></thead><tbody>'
        '<tr><td><b>Input (Farm)</b></td><td>QR code / RFID chip + initial quality certification recorded</td></tr>'
        '<tr><td><b>Transport (Logistics)</b></td><td>IoT sensors push real-time temperature/humidity data to the chain</td></tr>'
        '<tr><td><b>Handoff (Smart contract)</b></td><td>Automated verification of storage conditions + instant payment release</td></tr>'
        '<tr><td><b>Output (Consumer)</b></td><td>Scan the QR code to see the full batch history</td></tr>'
        '</tbody></table></div>'
        '<p class="qtext" style="margin-top:10px">Impact: traceability time drops from several days of manual paperwork to seconds of a QR scan.</p>',
        "The farm-to-table case: QR/RFID at input, IoT sensors during transport, smart-contract-triggered payment at handoff, and a consumer-facing QR scan at output. Traceability time drops from days to seconds.", 45)

    add("", '<div class="section">2. Blockchain &mdash; deeper dive</div><h2>Six characteristics of blockchain as a data platform</h2>'
        + '<div class="six">'
        + pc("#38bdf8", "1. Transparency", '<p>Data visible to network members; public chains are visible to anyone.</p>')
        + pc("#34d399", "2. Immutability", '<p>Data cannot be deleted/edited &rarr; a public audit trail.</p>')
        + pc("#fbbf24", "3. Consistency", '<p>Every node holds the same ledger &mdash; one single source of truth.</p>')
        + pc("#a78bfa", "4. Equal rights", '<p>No privileged intermediary; equal read/write access across nodes.</p>')
        + pc("#f472b6", "5. Availability", '<p>Each node keeps a full copy; the system runs as long as one node survives.</p>')
        + pc("#f87171", "6. Trade-offs", '<p>Low privacy (public data) and low throughput (consensus is slow).</p>')
        + '</div>'
        + '<p class="src">Secondary source: "Đặc tính chính của Blockchain", Nhóm 10 (classmates, Dặi học Sư phạm Hà Nội, môn Cơ sở dữ liệu tiên tiến) &mdash; not our group\'s work, cited here to go beyond the lecture slide for exam depth.</p>',
        "Six characteristics from a classmate team's database-course deep dive, cited as a secondary source: transparency, immutability, consistency, equal rights, availability, and the trade-off of low privacy and low throughput that comes with all of the above.", 55)

    add("", '<div class="section">2. Blockchain &mdash; group exercise</div><h2>Worked answer: Blockchain for Health Insurance (Y Tế)</h2>'
        + '<div class="two">'
        + pc("#38bdf8", "The problem today", '<ul><li>Patient records scattered across hospitals, clinics, insurers &mdash; no shared source of truth</li>'
             '<li>Claim fraud and duplicate billing are hard to detect across fragmented systems</li>'
             '<li>Patients cannot easily prove their own treatment history when switching provider/insurer</li></ul>')
        + pc("#34d399", "The Blockchain application", '<ul><li><b class="lbl">Transparency + Consistency:</b> hospital, insurer, and patient see the same claim record &mdash; one shared ledger instead of reconciling paperwork</li>'
             '<li><b class="lbl">Immutability:</b> a treatment history/claim, once recorded, cannot be quietly altered &mdash; strong fraud deterrent</li>'
             '<li><b class="lbl">Smart contracts:</b> claim auto-approved and paid once hospital discharge + policy conditions are verified on-chain</li>'
             '<li><b class="lbl">Off-chain + on-chain hybrid:</b> sensitive medical data stays off-chain (hospital DB / encrypted storage); only a hash/proof of the record goes on-chain &mdash; keeps patient privacy (GDPR-style) while still giving an immutable audit trail</li></ul>')
        + '</div>',
        "Scenario exercise answer for healthcare: the shared ledger kills the reconciliation problem between hospitals and insurers, immutability deters claim fraud, smart contracts automate payout, and a hybrid on-chain/off-chain design keeps sensitive medical data private while still proving the record hasn't been tampered with.", 60)

    add("", '<div class="section">3. Network Platforms</div><h2>How platforms create value for SMEs</h2>'
        + '<div class="three">'
        + pc("#38bdf8", "Network effects", '<p>A growing user base lowers search and transaction costs for every participating firm.</p>')
        + pc("#fbbf24", "Global market reach", '<p>E-commerce platforms remove geographic barriers, aggregate demand, streamline supply chains.</p>')
        + pc("#a78bfa", "Functional outsourcing", '<p>SMEs outsource payments, logistics, marketing, and &quot;security-by-design&quot; cybersecurity to the platform.</p>')
        + '</div>'
        + '<p class="qtext" style="margin-top:10px">Core concept: a 5&ndash;10-person SME can sell globally or use AI without building costly internal IT &mdash; via a pay-as-you-go network platform.</p>',
        "Platforms create value for SMEs through network effects, global reach, and outsourcing core functions like payments and security, all pay-as-you-go instead of upfront IT investment.", 40)

    add("", '<div class="section">3. Network Platforms</div><h2>Models, risks, and policy response</h2>'
        + '<div class="two">'
        + pc("#34d399", "Three platform models", '<ul><li><b class="lbl">E-commerce/Marketplaces</b> (B2C/B2B): expands sales channels, lowers customer-acquisition cost</li>'
             '<li><b class="lbl">Cloud platforms</b> (SaaS/IaaS): ERP/CRM + big-data analytics without hardware investment</li>'
             '<li><b class="lbl">B2B/Industrial networks</b>: collaborative design, joint manufacturing, data sharing</li></ul>')
        + pc("#f87171", "Strategic risks &amp; response", '<ul><li>Platform lock-in: sudden algorithm/fee changes</li>'
             '<li>Data asymmetry: platform owns the customer data, not the SME</li>'
             '<li>Digital skills gap inside the SME</li>'
             '<li><b class="lbl">Response:</b> omnichannel strategy, collect first-party data, policy: data-portability rights + targeted financial incentives</li></ul>')
        + '</div>',
        "Three platform models: e-commerce, cloud, and B2B/industrial networks. The risks are lock-in, data asymmetry, and skills gaps; the policy response is omnichannel strategy, first-party data collection, and data-portability regulation.", 45)

    add("close", '<div class="section">Self-check</div><h2>Before you close the laptop</h2>'
        + '<div class="two">'
        + pc("#38bdf8", "Can you do this without looking?", '<ul>'
            '<li>Name the 3 AI adoption paths for SMEs and 1 trade-off each</li>'
            '<li>Explain why blockchain is a &quot;verification layer&quot;, not a database replacement</li>'
            '<li>Name all 6 blockchain characteristics (Transparency&hellip;Trade-offs)</li>'
            '<li>Give 1 full Blockchain application example end-to-end (e.g. health insurance)</li>'
            '<li>Name the 3 network-platform models + 2 SME risks</li></ul>')
        + pc("#fbbf24", "One sentence per technology", '<p><b class="lbl">AI:</b> boosts SME productivity but is gated by data quality and skills.</p>'
            '<p><b class="lbl">Blockchain:</b> a shared, tamper-proof verification layer for multi-party trust.</p>'
            '<p><b class="lbl">Platforms:</b> pay-as-you-go scale, at the cost of data ownership.</p>')
        + '</div>',
        "Three technologies, one sentence each: AI boosts productivity but needs clean data and skills; blockchain is a shared tamper-proof verification layer; platforms give SMEs scale at the cost of owning their own customer data.", 35)

    notes_json = json.dumps({str(k): v for k, v in NOTES.items()}, ensure_ascii=False)
    js = JS.replace("NOTES_JSON", notes_json)
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Innovative Technology &middot; Session 6 Slides</title><style>{CSS}</style></head>
<body>
<div id="stage">{"".join(S)}<a id="home" href="../index.html">&larr; Home</a><div id="count"></div><div id="hud"><i id="bar"></i></div></div>
<div class="nb"><button id="prev" aria-label="Previous slide">&lsaquo;</button><button id="next" aria-label="Next slide">&rsaquo;</button><button id="nt">Notes (N)</button><button id="fs">Full screen (F)</button></div>
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
