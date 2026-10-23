# -*- coding: utf-8 -*-
"""Session 6 — Innovative Technology (Chapter 3), Science & Technology Innovation Management, USTH.
Uses the REAL usth-dses-deck engine (deck_helpers.py + deck_components.py + usth_theme.css +
deck_sizing.css), with a light-blue DSES override (dses_blue.css) instead of the default navy/red.
Source: 2026- Chapter 3- Innovation Manegement 22.10.pdf (Dr. Do Thi Hai).
Blockchain group exercise slide answers the exact prompt on the lecture slide: "Propose a Blockchain
application for a different industry (e.g., Anti-counterfeiting in Luxury Fashion, Health Insurance,
Real Estate, or Pharmaceutical Traceability)" — answered here with Health Insurance.
The six-characteristics / architecture slide also draws on a classmate team's (not our group, HNUE,
course Co so du lieu tien tien) deck "Dac tinh chinh cua Blockchain.pptx", cited as secondary source.
Run: python3 build/build_slides.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from deck_helpers import slide, divider, tbl, callout, tblock, apply_usth_theme, deck_html
from deck_components import card, cards, ul, cols, table

CHIP = ('<div class="logo-chip"><img src="../assets/images/usth_logo.png" alt="USTH">'
        '<img src="../assets/images/usth_dses_logo.png" alt="DSES"></div>')


def cards_fit(height, *cs, n=3):
    """cards() grid, with its default fixed height:548px shrunk so trailing content (a .note line)
    after the grid does not overflow the fixed 720px slide canvas (overflow:hidden clips it silently)."""
    html = cards(*cs, cols=n)
    return html.replace(
        f'style="grid-template-columns:repeat({n},1fr)"',
        f'style="grid-template-columns:repeat({n},1fr);height:{height}px;gap:14px"')

S = []

# 1. Cover
S.append(slide(
    "Innovative Technology",
    '<div class="cover-sub">AI in SMEs &middot; Blockchain &middot; Network Platforms</div>'
    '<div class="cover-meta">Science &amp; Technology Innovation Management &mdash; Chapter 3<br>'
    'Dr. Do Thi Hai &middot; USTH Master Programme</div>' + CHIP,
    kicker="SESSION 6"))

# 2. AI in SMEs — adoption paths
S.append(slide(
    "Three ways SMEs adopt AI",
    cards(
        card("Off-the-shelf / Cloud AI", "SaaS on cloud platforms, low upfront cost. Ex: support chatbots, marketing tools, AI invoice recognition."),
        card("Embedded AI", "AI features built into third-party core software. Ex: predictive sales analytics in CRMs, ad-optimization on Google/Meta."),
        card("Custom AI Solutions", "Bespoke algorithms for unique operations. Trade-off: expensive, needs dedicated data infra and ML engineers &mdash; rarest path for SMEs."),
        cols=3),
    kicker="1 &middot; AI IN SMEs"))

# 3. AI in SMEs — drivers, barriers, Vietnam data
S.append(slide(
    "Strategic drivers vs. adoption barriers",
    cols(
        ul(["<b>Cost &amp; productivity</b>: automating repetitive admin / customer-service tasks",
            "<b>Decision support</b>: forecasting demand, managing supply-chain risk",
            "<b>Hyper-personalized</b> customer experience"]),
        ul(["<b>Skills gap</b>: lack of in-house technical expertise",
            "<b>Data quality</b>: fragmented, unstructured data",
            "<b>Financial constraints</b>: unclear short-term ROI",
            "<b>Legal &amp; security risk</b>: privacy, compliance"]))
    + callout("info", "Vietnam, 2025 (Deloitte Access Economics &amp; Meta survey)",
              "93% of Vietnamese SMEs use &ge;1 AI tool &mdash; highest of 6 surveyed APAC markets &middot; 92% report higher productivity &middot; 89% report lower operating cost."),
    kicker="1 &middot; AI IN SMEs"))

# 4. Blockchain — core concept
S.append(slide(
    "What is Blockchain, and why supply chains need it",
    cols(
        '<div class="card"><div class="card-h">Core idea</div><div class="card-t">'
        'A distributed, decentralized ledger: data is grouped into blocks linked by cryptographic hashes, '
        'each block referencing the one before it. <b>Transparency</b> (visible to authorized members), '
        '<b>immutability</b> (recorded data cannot be altered), <b>smart contracts</b> (automatic execution '
        'once conditions are met).</div></div>',
        '<div class="card"><div class="card-h">Problem it solves</div><div class="card-t">'
        'Information is fragmented across stakeholders (Farm &rarr; Logistics &rarr; Warehouse &rarr; Supermarket); '
        'manual traceability is slow and costly. Blockchain does <b>not</b> replace legacy systems &mdash; '
        'it acts as a trusted verification layer connecting them.</div></div>'),
    kicker="2 &middot; BLOCKCHAIN"))

# 5. Blockchain — food traceability case
S.append(slide(
    "Case study: food traceability, Farm to Table",
    table(tbl(["Stage", "What happens on-chain"], [
        ["Input (Farm)", "QR code / RFID chip + initial quality certification recorded"],
        ["Transport (Logistics)", "IoT sensors push real-time temperature / humidity data to the chain"],
        ["Handoff (Smart contract)", "Automated verification of storage conditions + instant payment release"],
        ["Output (Consumer)", "Scan the QR code to see the full batch history"],
    ]))
    + '<div class="note">Impact: traceability time drops from several days of manual paperwork to seconds of a QR scan.</div>',
    kicker="2 &middot; BLOCKCHAIN"))

# 6. Blockchain — six characteristics (secondary source)
S.append(slide(
    "Six characteristics of Blockchain as a data platform",
    cards_fit(420,
        card("1. Transparency", "Data visible to network members; public chains visible to anyone."),
        card("2. Immutability", "Data cannot be deleted or edited &rarr; a public audit trail."),
        card("3. Consistency", "Every node holds the same ledger &mdash; one single source of truth."),
        card("4. Equal rights", "No privileged intermediary; equal read/write access across nodes."),
        card("5. Availability", "Each node keeps a full copy; the system runs as long as one node survives."),
        card("6. Trade-offs", "Low privacy (public data) and low throughput (consensus is slow)."))
    + '<div class="note" style="font-size:20px">Secondary source: &quot;Đặc tính chính của Blockchain&quot;, Nhóm 10 '
      '(classmates, Đại học Sư phạm Hà Nội, môn Cơ sở dữ liệu tiên tiến) '
      '&mdash; not our group’s work, cited to go beyond the lecture slide.</div>',
    kicker="2 &middot; BLOCKCHAIN"))

# 7. Blockchain — group exercise prompt (verbatim from lecture slide)
S.append(slide(
    "Group Discussion &amp; Scenario Exercise (20 mins)",
    '<div class="bigq">Scenario: propose a Blockchain application for a different industry '
    '(e.g., Anti-counterfeiting in Luxury Fashion, <b>Health Insurance</b>, Real Estate, or Pharmaceutical Traceability). '
    'Group presentations: 5&ndash;10 minutes per group.</div>'
    + callout("good", "Our group's answer: Health Insurance", "Worked out on the next slide."),
    kicker="2 &middot; BLOCKCHAIN &middot; GROUP ACTIVITY"))

# 8. Blockchain — worked answer: Health Insurance
S.append(slide(
    "Worked answer: Blockchain for Health Insurance",
    cols(
        '<div class="card"><div class="card-h">The problem today</div><div class="card-t">' + ul([
            "Patient records scattered across hospitals, clinics, insurers &mdash; no shared source of truth",
            "Claim fraud and duplicate billing are hard to detect across fragmented systems",
            "Patients cannot easily prove their treatment history when switching provider or insurer",
        ]) + '</div></div>',
        '<div class="card"><div class="card-h">The Blockchain application</div><div class="card-t">' + ul([
            "<b>Transparency + Consistency</b>: hospital, insurer, and patient see the same claim record on one shared ledger",
            "<b>Immutability</b>: a recorded treatment history / claim cannot be quietly altered &mdash; strong fraud deterrent",
            "<b>Smart contracts</b>: claim auto-approved and paid once discharge + policy conditions verify on-chain",
            "<b>Hybrid on/off-chain</b>: sensitive medical data stays off-chain; only a hash/proof goes on-chain &mdash; keeps privacy while proving the record is untampered",
        ]) + '</div></div>'),
    kicker="2 &middot; BLOCKCHAIN &middot; GROUP ACTIVITY"))

# 9. Network Platforms — value drivers + models
S.append(slide(
    "How network platforms create value for SMEs",
    cards_fit(420,
        card("Network effects", "A growing user base lowers search and transaction costs for every participating firm."),
        card("Global market reach", "E-commerce platforms remove geographic barriers, aggregate demand, streamline supply chains."),
        card("Functional outsourcing", "SMEs outsource payments, logistics, marketing, and &quot;security-by-design&quot; cybersecurity to the platform."))
    + '<div class="note">Core concept: a 5&ndash;10-person SME can sell globally or use AI without building costly internal IT &mdash; via a pay-as-you-go network platform.</div>',
    kicker="3 &middot; NETWORK PLATFORMS"))

# 10. Network Platforms — risks & policy + closing self-check
S.append(slide(
    "Strategic risks, and the self-check before you close the laptop",
    cols(
        ul(["<b>Platform lock-in</b>: sudden algorithm/fee changes",
            "<b>Data asymmetry</b>: platform owns the customer data, not the SME",
            "<b>Digital skills gap</b> inside the SME",
            "<b>Response</b>: omnichannel strategy, first-party data collection, data-portability regulation"]),
        ul(["Name the 3 AI adoption paths for SMEs + 1 trade-off each",
            "Explain why Blockchain is a &quot;verification layer&quot;, not a database replacement",
            "Name all 6 Blockchain characteristics (Transparency&hellip;Trade-offs)",
            "Give 1 full Blockchain application end-to-end (Health Insurance)",
            "Name the 3 network-platform models + 2 SME risks"])),
    kicker="3 &middot; NETWORK PLATFORMS &middot; SELF-CHECK"))

SL = apply_usth_theme(S)
DECK = deck_html(SL)

BASE_CSS = (HERE / "deck_sizing.css").read_text(encoding="utf-8")
THEME_CSS = (HERE / "usth_theme.css").read_text(encoding="utf-8")
BLUE_CSS = (HERE / "dses_blue.css").read_text(encoding="utf-8")
JS = (HERE / "deck.js").read_text(encoding="utf-8")

DOC = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Innovative Technology &middot; Session 6 Slides</title>
<style>{BASE_CSS}
{THEME_CSS}
{BLUE_CSS}
.mdeck-canvas-wrap{{max-width:1280px}}
a.back-home{{display:inline-block;margin:0 4px}}
</style></head>
<body>
{DECK}
<p style="text-align:center;margin:10px 0 24px"><a class="back-home" href="../index.html">&larr; Session 6 home</a></p>
<script>{JS}</script>
</body></html>
'''

(ROOT / "slides").mkdir(exist_ok=True)
(ROOT / "slides" / "index.html").write_text(DOC, encoding="utf-8")
print(f"slides: {len(S)}")
