# -*- coding: utf-8 -*-
"""Thành phần slide đã kiểm thử (deck_sizing.css đi kèm). Dùng cùng deck_helpers.py (slide, tbl, callout, apply_usth_theme, deck_html).
Mọi cỡ chữ >= 20 px; ảnh đặt đúng kích thước 1:1 (xem references/17-slide-sizing-fill-and-qa.md)."""
import re

def img(f, w=None, h=None, cap=None, center=True, folder="../assets/images/"):
    """Ảnh + caption 20 px. Chỉ nên đặt w (ảnh vẽ đúng px). Đặt cả w và h chỉ khi biết chắc tỉ lệ."""
    st = (f"width:{w}px;" if w else "") + (f"height:{h}px;" if h else "")
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<figure class="fig{" ctr" if center else ""}"><img src="{folder}{f}.png" alt="" style="{st}">{c}</figure>'

def card(h, t): return f'<div class="card"><div class="card-h">{h}</div><div class="card-t">{t}</div></div>'
def cards(*cs, cols=3): return f'<div class="cards" style="grid-template-columns:repeat({cols},1fr)">' + "".join(cs) + "</div>"   # .cards cao 548 px: lấp đầy slide
def ul(items, xl=False): return f'<ul class="{"xl" if xl else ""}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"            # xl = 30 px
def cols(*parts, flex=None):
    fl = flex or [1] * len(parts)
    return '<div class="cols">' + "".join(f'<div style="flex:{f}">{p}</div>' for p, f in zip(parts, fl)) + "</div>"

def table(tbl_html, size=""):
    """tbl_html = deck_helpers.tbl(head, rows). size: '' (24 px) | 'xl' (27 px, ít hàng) | 'mid' (25 px) | 'tight' (hàng sát) | 'compact' (21 px, nhiều hàng)."""
    return tbl_html.replace("<table>", f'<table class="lg {size}">')
def matrix(tbl_html, size="mid"): return tbl_html.replace("<table>", f'<table class="lg {size} matrix">')   # ô ● ○ ở giữa, cột đầu là chữ

def pill(label, cls): return f'<span class="pill {cls}">{label}</span>'                                      # cls: new | old | bor
def status(txt):                                                                                             # Done | Partly | Not found
    cls = {"Done": "st-done", "Partly": "st-part", "Not found": "st-no"}[txt]
    return f'<span class="st {cls}">{txt}</span>'

CHIP = ('<div class="logo-chip"><img src="../assets/images/usth_logo.png" alt="USTH">'
        '<img src="../assets/images/usth_dses_logo.png" alt="DSES"></div>')   # logo USTH xanh navy phải đặt trên chip TRẮNG, không đặt lên thanh tiêu đề navy

def pipeline_svg(rows, label_w=64, box_w=206, gap=22, row_h=112):
    """rows = [(id, màu, ['dòng1|dòng2', ...]), ...]. SVG rộng đúng 1160 px, chữ 20-26 px; <= 5 bước mỗi hàng, <= 4 hàng mỗi slide."""
    s = []
    for i, (pid, col, steps) in enumerate(rows):
        y = i * (row_h + 14)
        s.append(f'<rect x="0" y="{y}" width="{label_w}" height="{row_h}" rx="10" fill="{col}"/>'
                 f'<text x="{label_w/2}" y="{y+row_h/2+8}" text-anchor="middle" font-size="26" font-weight="800" fill="#fff">{pid}</text>')
        for j, st in enumerate(steps):
            x = label_w + 14 + j * (box_w + gap); a, b = (st.split("|") + [""])[:2]
            s.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{row_h}" rx="10" fill="#fff" stroke="{col}" stroke-width="2.5"/>'
                     f'<text x="{x+box_w/2}" y="{y+row_h/2-4}" text-anchor="middle" font-size="21" font-weight="700" fill="#1b2433">{a}</text>'
                     f'<text x="{x+box_w/2}" y="{y+row_h/2+24}" text-anchor="middle" font-size="20" fill="#1b2433">{b}</text>')
            if j < len(steps) - 1:
                s.append(f'<polygon points="{x+box_w+gap-3},{y+row_h/2} {x+box_w+3},{y+row_h/2-9} {x+box_w+3},{y+row_h/2+9}" fill="{col}"/>')
    H = len(rows) * (row_h + 14)
    return f'<svg width="1160" height="{H}" viewBox="0 0 1160 {H}" style="display:block;margin:0 auto;font-family:inherit" role="img">{"".join(s)}</svg>'

def tag_slides(slides, kind):
    """Gắn thẻ NEW / SAME AS ở góc tiêu đề (CSS ::after trong deck_sizing.css). kind: 'new' | 'old'. Không gắn cho bìa và slide cuối."""
    return [s.replace('<div class="mdeck-slide', f'<div class="mdeck-slide is-{kind}', 1) for s in slides]

def compose_versions(v1_builder_path):
    """Mẫu v1 -> v2 không lệch nhau: chạy phần ĐỊNH NGHĨA slide của builder v1 (trước dòng `SL = apply_...(S)`) rồi thêm slide mới.
        head, tail = split_builder(path); exec(head, g); S1 = g['S']; ...ghép danh sách...; g['S'] = S; exec(tail, g)"""
    src = open(v1_builder_path, encoding="utf-8").read()
    cut = src.index("SL = apply_")
    return src[:cut], src[cut:]
