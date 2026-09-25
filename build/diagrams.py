"""Writes diagrams/*.drawio (then export with the drawio CLI). Horizontal bands, no free-form coordinates."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "diagrams"
FONT = "fontFamily=PT Sans;"
PAL = {
    "blue": ("#dae8fc", "#6c8ebf"), "yellow": ("#fff2cc", "#d6b656"), "green": ("#d5e8d4", "#82b366"),
    "red": ("#f8cecc", "#b85450"), "purple": ("#e1d5e7", "#9673a6"), "orange": ("#ffe6cc", "#d79b00"), "gray": ("none", "#9aa8a1"),
}


class Dia:
    def __init__(self, w, h):
        self.w, self.h, self.cells, self.n = w, h, [], 1

    def _id(self):
        self.n += 1
        return f"c{self.n}"

    def box(self, x, y, w, h, text, color="blue", size=18, bold=False, dashed=False, solid=None, font_color="#1f2a26", align="center", rounded=True):
        i = self._id()
        fill, stroke = PAL[color] if color else ("none", "none")
        st = f"rounded={1 if rounded else 0};whiteSpace=wrap;html=1;{FONT}fontSize={size};fontColor={font_color};align={align};verticalAlign=middle;"
        if solid:
            st += f"fillColor={solid};strokeColor={solid};fontColor=#ffffff;fontStyle=1;"
        else:
            st += f"fillColor={fill};strokeColor={stroke};strokeWidth=2;" + ("fontStyle=1;" if bold else "")
        if dashed:
            st += "dashed=1;dashPattern=8 6;"
        v = escape(text).replace("\n", "&#10;")
        self.cells.append(f'<mxCell id="{i}" value="{v}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    def text(self, x, y, w, h, t, size=18, color="#1f2a26", bold=False, align="center"):
        i = self._id()
        st = f"text;html=1;{FONT}fontSize={size};fontColor={color};align={align};verticalAlign=middle;whiteSpace=wrap;" + ("fontStyle=1;" if bold else "")
        self.cells.append(f'<mxCell id="{i}" value="{escape(t)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    def edge(self, a, b, label="", color="#4b5b54", dashed=False, size=15, exit_xy=None, entry_xy=None):
        i = self._id()
        st = f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;{FONT}fontSize={size};strokeWidth=2.5;strokeColor={color};endArrow=block;endFill=1;labelBackgroundColor=#ffffff;"
        if dashed:
            st += "dashed=1;"
        if exit_xy:
            st += f"exitX={exit_xy[0]};exitY={exit_xy[1]};exitDx=0;exitDy=0;"
        if entry_xy:
            st += f"entryX={entry_xy[0]};entryY={entry_xy[1]};entryDx=0;entryDy=0;"
        self.cells.append(f'<mxCell id="{i}" value="{escape(label)}" style="{st}" edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    def save(self, name, title):
        xml = (f'<mxfile host="app.diagrams.net"><diagram id="{name}" name="{escape(title)}"><mxGraphModel dx="1100" dy="600" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
               + "".join(self.cells) + "</root></mxGraphModel></diagram></mxfile>")
        (OUT / f"{name}.drawio").write_text(xml, encoding="utf-8")


def market_gap():
    d = Dia(1100, 540)
    # band 1: column headers (y 10..50)
    for x, t, c in [(20, "1  Household needs", "#3b6ea5"), (380, "2  What people use today", "#a07a12"), (800, "3  What is missing", "#a3403b")]:
        d.box(x, 10, 280, 44, t, solid=c, size=19)
    # band 2: content (y 80..380)
    need1 = d.box(20, 90, 280, 84, "Save towards a lump sum", "blue", 19)
    need2 = d.box(20, 230, 280, 84, "Borrow cash quickly", "blue", 19)
    hui = d.box(380, 76, 280, 92, "Hụi and bốc bát họ\nTrust rests on one host", "yellow", 19, bold=True)
    black = d.box(380, 196, 280, 68, "Black credit", "red", 19, bold=True)
    pawn = d.box(380, 292, 280, 68, "Pawnshops", "red", 19, bold=True)
    escrow = d.box(800, 76, 280, 108, "No neutral intermediary\nthat freezes the pot\nfairly (escrow)", "red", 19, dashed=True)
    card = d.box(800, 214, 280, 146, "No channel that turns a\ncredit-card limit into a\npredictable flat-fee cost", "red", 19, dashed=True)
    d.edge(need1, hui, "", "#3b6ea5")
    d.edge(need2, black, "", "#3b6ea5")
    d.edge(need2, pawn, "", "#3b6ea5", exit_xy=(1, 0.75), entry_xy=(0, 0.5))
    d.edge(hui, escrow, "risk if host fails", "#a3403b", dashed=True, size=14)
    d.edge(black, card, "no safe option", "#a3403b", dashed=True, size=14)
    # band 3: our layer (y 410..520)
    d.box(20, 410, 1060, 104, "First layer we build: HụiKeeper 2.0\nA trusted, shared record of who paid what and when: the data any escrow or flat-fee service would need", "purple", 20, bold=True)
    return d


def architecture():
    d = Dia(1100, 540)
    d.box(8, 4, 1084, 532, "", "gray", rounded=True, dashed=True)  # device boundary (border only)
    d.text(24, 14, 1050, 30, "Everything runs on the phone (no server, no account). Arrows: presentation watches view-model, view-model uses domain, domain maps to data.", 15, "#5b6b64", True, "left")
    heads = [(24, "Presentation", "#3b6ea5"), (244, "ViewModel", "#a07a12"), (464, "Domain", "#5d8a4b"), (684, "Data", "#7a5b96")]
    for x, t, c in heads:
        d.box(x, 56, 180, 42, t, solid=c, size=19)
    d.box(904, 56, 176, 42, "Navigation", solid="#4b5b54", size=19)
    pres = [d.box(24, 118, 200, 70, "Circle list", "blue", 18), d.box(24, 208, 200, 70, "Cycle detail\n(paid, amount, note)", "blue", 18), d.box(24, 298, 200, 70, "Stats dashboard", "blue", 18)]
    vm = [d.box(240, 118, 200, 70, "CircleListNotifier", "yellow", 17), d.box(240, 208, 200, 70, "CycleNotifier", "yellow", 17), d.box(240, 298, 200, 70, "StatsProvider", "yellow", 17)]
    dom = [d.box(456, 118, 200, 70, "Circle model\ndead / live hụi", "green", 17), d.box(456, 208, 200, 70, "Payment model", "green", 17), d.box(456, 298, 200, 70, "Progress rules\npaid, remaining, %", "green", 17)]
    dat = [d.box(672, 118, 200, 70, "Drift DAOs", "purple", 18), d.box(672, 208, 200, 70, "Drift tables", "purple", 18), d.box(672, 298, 200, 70, "SQLite file\non the device", "purple", 18, bold=True)]
    d.box(890, 118, 190, 108, "GoRouter\n/circles\n/circles/:id\n/stats", "blue", 17, rounded=True)
    for a, b in zip(pres, vm):
        d.edge(a, b)
    for a, b in zip(vm, dom):
        d.edge(a, b)
    for a, b in zip(dom, dat):
        d.edge(a, b)
    # band: new in 2.0 (y 396..520)
    d.text(24, 394, 500, 28, "New in 2.0 (SCAMPER)", 18, "#b45309", True, "left")
    d.box(24, 428, 200, 84, "R: Player / host view switch", "orange", 16)
    d.box(240, 428, 200, 84, "C: Reminder scheduler\n+ payment QR", "orange", 16)
    d.box(456, 428, 200, 84, "E: Auto payout for\nlive hụi bids", "orange", 16)
    d.box(672, 428, 200, 84, "P: Savings-goal\ntable", "orange", 16)
    d.box(890, 428, 190, 84, "M: Text size and cycle\nlength settings", "orange", 16)
    return d


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    market_gap().save("market-gap", "Market gap")
    architecture().save("app-architecture", "App architecture")
    print("wrote diagrams")
