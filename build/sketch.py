"""Generates deliverable/sketch.svg: hand-drawn style mock-up of HụiKeeper 2.0 with SCAMPER call-outs."""
from pathlib import Path

COL = {"S": "#0f766e", "C": "#2563eb", "A": "#7c3aed", "M": "#d97706", "P": "#db2777", "E": "#dc2626", "R": "#0891b2"}
INK = "#1f2a26"


def callout(letter, y, text, ax, ay):
    c = COL[letter]
    return f'''
  <path d="M{ax} {ay} C {ax+50} {ay}, 380 {y}, 418 {y}" fill="none" stroke="{c}" stroke-width="2.2" stroke-dasharray="6 5"/>
  <circle cx="{ax}" cy="{ay}" r="5" fill="{c}"/>
  <circle cx="440" cy="{y}" r="19" fill="{c}"/>
  <text x="440" y="{y+7}" text-anchor="middle" font-size="22" font-weight="700" fill="#fff">{letter}</text>
  <text x="474" y="{y+7}" font-size="19" fill="{INK}">{text}</text>'''


def build() -> str:
    calls = "".join([
        callout("R", 70, "Reverse: player view first, host one tap away", 285, 70),
        callout("E", 150, "Eliminate: no sign-up, still 100% offline", 295, 113),
        callout("M", 230, "Modify: text size + cycle length adjustable", 295, 182),
        callout("S", 310, "Substitute: one-tap PAID replaces typing", 288, 272),
        callout("A", 390, "Adapt: loan-app style due / overdue timeline", 289, 338),
        callout("C", 470, "Combine: reminder bell + payment QR in the card", 262, 405),
        callout("P", 550, "Put to another use: savings-goal tab", 262, 566),
    ])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 640" font-family="'Bradley Hand','Segoe Print','Comic Sans MS','Marker Felt',cursive">
  <title>Sketch of HụiKeeper 2.0 with SCAMPER call-outs</title>
  <defs>
    <filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2"/>
    </filter>
  </defs>
  <rect width="960" height="640" fill="#fffdf6"/>
  <g filter="url(#rough)" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <!-- phone -->
    <rect x="60" y="24" width="260" height="592" rx="34" fill="#ffffff"/>
    <rect x="75" y="44" width="230" height="530" rx="14"/>
    <!-- R: role toggle -->
    <rect x="95" y="52" width="190" height="34" rx="17"/>
    <rect x="97" y="54" width="92" height="30" rx="15" fill="#c8f0ea"/>
    <!-- E: offline chip -->
    <rect x="196" y="98" width="100" height="26" rx="13" fill="#fde8e8"/>
    <!-- ring -->
    <circle cx="140" cy="185" r="42"/>
    <path d="M140 143 A42 42 0 1 1 103 206" stroke="{COL['S']}" stroke-width="7"/>
    <!-- M: text size slider -->
    <path d="M205 182 H288"/><circle cx="252" cy="182" r="8" fill="{COL['M']}"/>
    <!-- cards -->
    <rect x="90" y="240" width="205" height="56" rx="10"/>
    <rect x="236" y="252" width="52" height="30" rx="8" fill="#c8f0ea"/>
    <rect x="90" y="310" width="205" height="56" rx="10"/>
    <path d="M90 322 V354" stroke="{COL['E']}" stroke-width="8"/>
    <rect x="90" y="380" width="205" height="56" rx="10"/>
    <!-- bell + QR -->
    <path d="M236 402 q10 -14 20 0 v10 h-20 z"/><rect x="264" y="398" width="20" height="20"/>
    <path d="M268 402 h5 v5 h-5 z M277 411 h4 v4 h-4 z"/>
    <!-- tabs -->
    <path d="M75 520 H305"/>
    <path d="M152 520 V574 M228 520 V574"/>
    <path d="M238 562 h54" stroke="{COL['P']}" stroke-width="5"/>
  </g>
  <g fill="{INK}" font-size="15">
    <text x="112" y="74">Player</text><text x="216" y="74">Host</text>
    <text x="202" y="116" font-size="13">offline ✓</text>
    <text x="92" y="118" font-size="20" font-weight="700">This week</text>
    <text x="118" y="190" font-size="18" font-weight="700">58%</text>
    <text x="212" y="170" font-size="13">A a  A</text>
    <text x="100" y="264" font-size="15">Lan  2,000,000</text><text x="100" y="284" font-size="12" fill="#5b6b64">due Fri</text>
    <text x="240" y="273" font-size="14" font-weight="700">PAID</text>
    <text x="104" y="334" font-size="15">Minh 1,000,000</text><text x="104" y="354" font-size="12" fill="{COL['E']}">3 days late</text>
    <text x="100" y="404" font-size="15">Hoa  500,000</text><text x="100" y="424" font-size="12" fill="#5b6b64">due Sun</text>
    <text x="98" y="546" font-size="14">Week</text>
    <text x="166" y="546" font-size="14">Circles</text>
    <text x="242" y="546" font-size="14" font-weight="700">Goals</text>
  </g>
  <g font-size="19">{calls}</g>
  <text x="474" y="612" font-size="16" fill="#5b6b64">HụiKeeper 2.0 · SCAMPER Exercise 1 · sketch by hand-style SVG</text>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "deliverable" / "sketch.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out)
