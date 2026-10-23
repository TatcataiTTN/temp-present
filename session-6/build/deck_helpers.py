# -*- coding: utf-8 -*-
"""Helper dựng deck HTML slide — bản USTH-DSES, nhân bản từ `templates/hust-deck/deck_helpers.py`
(cùng kiến trúc deck đã dùng cho deck 73 slide + deck Q&A Hadoop của HUST, đổi theme sang USTH).
Dùng:  from deck_helpers import *   rồi  SL = [slide(...), ...]; SL = apply_usth_theme(SL); DECK = deck_html(SL)

QUY ƯỚC BẮT BUỘC (bug thật đã gặp):
 - Công thức KaTeX trong chuỗi Python THƯỜNG: viết `\\tilde` (2 gạch) -> runtime `\tilde`. Viết 4 gạch -> `\\tilde` -> KaTeX hiểu `\\` là XUỐNG DÒNG, chữ lộ ra thành "tilde O" bị ngắt dòng.
   Trong f-string, ngoặc nhọn của KaTeX phải nhân đôi: `m^{{\\beta}}`.
 - Tiêu đề slide là CỤM DANH TỪ, không đặt câu hỏi ("Cơ chế nhân bản (replication)", không phải "Replication hoạt động ra sao?").
 - Không chèn thuyết minh về nguồn gốc nội dung kiểu "diễn giải thêm, không phải trích nguyên văn", "nguồn duy nhất là...".
"""
import re

def slide(title, body, kicker=None):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    return f'<div class="mdeck-slide">{k}<h2>{title}</h2>{body}</div>'

def divider(idx, total, title, bullets):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return (f'<div class="mdeck-slide part-divider"><div class="kicker">PHẦN {idx}/{total}</div>'
            f'<div class="part-num">{idx:02d}</div><h2>{title}</h2><ul class="part-list">{lis}</ul></div>')

def tbl(head, rows, dense=False):
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table{" class=\"dense\"" if dense else ""}><tr>{h}</tr>{r}</table>'

def callout(kind, label, text):          # kind: good | warn | info
    return f'<div class="callout {kind}"><div class="lbl">{label}</div>{text}</div>'

def tblock(header, items):
    return (f'<div class="tblock"><div class="tblock-h">{header}</div><ol>'
            + "".join(f"<li>{x}</li>" for x in items) + "</ol></div>")

def logo_img(f, h=40):                   # logo công nghệ trong bảng/ô: luôn đặt trên chip trắng để nhìn được ở nền tối
    return (f'<img src="../assets/images/logos/{f}" alt="" style="height:{h}px;max-width:150px;width:auto;object-fit:contain;'
            f'vertical-align:middle;background:#fff;border-radius:6px;padding:3px 6px;border:1px solid var(--border)">')

def figslide(title, img, src, rows, side=True, img_w="56%"):
    """Slide HÌNH GỐC cắt từ bài báo + bảng đối chiếu 'trong bài báo' -> 'trong hệ thống thực'. Luôn ghi nguồn dưới hình."""
    im = (f'<figure style="margin:0"><img src="../assets/images/papers/{img}" alt="{title}" style="width:100%;height:auto;'
          f'border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.78rem;'
          f'color:var(--muted);margin-top:4px">{src}</figcaption></figure>')
    tb = tbl(["Trong bài báo gốc", "Trong hệ thống thực"], rows, dense=True)
    if side:
        return slide(title, f'<div style="display:flex;gap:22px;align-items:flex-start"><div style="flex:0 0 {img_w}">{im}</div><div style="flex:1">{tb}</div></div>')
    return slide(title, f'<div style="max-width:{img_w};margin:0 auto 12px">{im}</div>{tb}')

def imgs_slide(title, items, body_after="", gap=18, maxh=None):
    """Nhiều ảnh cắt xếp ngang; items = [(file, chú thích, flex)]. maxh (px) để ảnh dọc không làm tràn khung."""
    st = f"max-height:{maxh}px;width:auto;max-width:100%;" if maxh else ""
    cells = "".join(f'<figure style="margin:0;flex:{fl}"><img src="../assets/images/papers/{f}" alt="" style="width:100%;height:auto;{st}'
                    f'border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.76rem;'
                    f'color:var(--muted);margin-top:4px">{cap}</figcaption></figure>' for f, cap, fl in items)
    return slide(title, f'<div style="display:flex;gap:{gap}px;align-items:flex-start;justify-content:center">{cells}</div>{body_after}')

def pre(code):
    code = code.strip("\n").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<pre class="qa-pre">{code}</pre>'

def cols(*parts):
    return '<div class="qa-cols">' + "".join(f"<div>{p}</div>" for p in parts) + "</div>"

def apply_usth_theme(slides, logo_for=(), secondary_logo=None):
    """Bản USTH của apply_hust_theme — dùng usth_theme.css (băng màu CSS thuần, không ảnh nền baked).
    logo_for: như apply_hust_theme (logo công nghệ/paper theo tiêu đề). secondary_logo: tên file logo phụ
    (vd 'usth_dses_logo.png') nếu muốn 2 logo như kiểu HUST — đặt None nếu chỉ dùng 1 logo chính."""
    part, out = -1, list(slides)
    for i, s in enumerate(out):
        m = re.search(r"<h2>(.*?)</h2>", s)
        if i == 0: cls = "cover"
        elif i == len(out) - 1: cls = "endcard"
        elif "part-divider" in s[:90]: part += 1; continue
        else: cls = f"th{max(part, 0) % 4}"
        extra = ""
        if m and cls.startswith("th"):
            for pref, f in logo_for:
                if m.group(1).startswith(pref):
                    extra = f' has-logo'; s = s.replace("</h2>", f'</h2><img class="tech-logo" src="../assets/images/logos/{f}" alt="">', 1); break
        s = re.sub(r'<div class="mdeck-slide( [^"]*)?">', lambda mm: f'<div class="mdeck-slide{mm.group(1) or ""}{extra} {cls}">', s, count=1)
        if cls.startswith("th"):
            s = s.replace("</h2>", '</h2><img class="usth-emblem" src="../assets/images/usth_logo.png" alt="USTH">', 1)
            if secondary_logo:
                s = s.replace("</h2>", f'</h2><img class="usth-emblem-secondary" src="../assets/images/{secondary_logo}" alt="">', 1)
        out[i] = s
    return out

def deck_html(slides):
    return ('<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">' + "".join(slides) + '</div></div>'
            '<div class="mdeck-bar"><button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>'
            '<span class="mdeck-count"></span><div class="mdeck-dots"></div><button class="mdeck-fs">⛶ Toàn màn hình</button></div></div>')
