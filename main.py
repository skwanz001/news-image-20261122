#!/usr/bin/env python3
"""Draw a one-page newspaper poster summing up Sunday 22 November 2026.

Writes a 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Every story was reported on 22 November 2026 (Reuters, CNN, AP, ANI wires).
Deterministic: the same bytes come out of every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
W = H = 1024
BG = (250, 247, 242)
NAVY = (20, 33, 61)
GOLD = (252, 163, 17)
INK = (26, 26, 26)
GREY = (70, 70, 70)
CARD = (255, 255, 255)
BORDER = (216, 210, 198)

WEEKDAY = "SUNDAY"
DATE = "22 NOVEMBER 2026"

PANELS = [
    ("CLIMATE", (14, 116, 144), "globe",
     "COP31 nears final deal after all-night talks in Antalya",
     "Presidents Australia and Türkiye table a package they say nearly 200 "
     "nations can accept; approval is set for Sunday."),
    ("EUROPE · NATO", (29, 78, 216), "shield",
     "NATO vows to defend every part of Poland",
     "After Russian missiles fell on Polish soil, Rutte pledges full "
     "allied defence; Estonia shuts its Russia road crossings for six "
     "months."),
    ("MIDDLE EAST", (180, 83, 9), "drone",
     "Iran claims strike on US Patriot radars in the Gulf",
     "Tehran says its missiles and drones hit two US air-defence radars, "
     "and readies tankers to defy the Hormuz blockade. Unverified."),
    ("ISRAEL", (109, 40, 217), "doc",
     "Eisenkot invites Netanyahu's Likud to coalition talks",
     "The opposition leader's Yashar party opens 'marathon' talks with "
     "the caretaker PM's party — a move that could reshape the "
     "government."),
    ("ASIA · DIPLOMACY", (4, 120, 87), "link",
     "Modi: civilisational links are peace's best guarantee",
     "India's PM tells the Shanghai Cooperation Organization summit "
     "that deep ties between peoples best guard peace amid conflict."),
    ("AFRICA · SUDAN", (185, 28, 28), "flag",
     "Sudan's Tasis Alliance seizes the key Bau region",
     "The alliance takes Bau in Blue Nile state, as a relief group accuses "
     "the RSF of killing civilians, three of them children, in West "
     "Kordofan."),
]

TICKER = ("ALSO TODAY — Zelenskyy: peace talks must bring tangible results "
          "· Tech sell-off deepens across Asia · Cyberattacks hit US "
          "agencies · 11 die from tainted alcohol in Manipur, India · "
          "South Africa mourns Mlambo-Ngcuka, 71")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def icon(draw, kind, cx, cy, r, color):
    import math
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    w = (255, 255, 255)
    if kind == "globe":
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=w, width=3)
        draw.ellipse([cx - 9, cy - 20, cx + 9, cy + 20], outline=w, width=2)
        draw.line([cx - 20, cy, cx + 20, cy], fill=w, width=2)
    elif kind == "shield":
        draw.polygon([(cx, cy - 22), (cx + 18, cy - 14), (cx + 18, cy + 4),
                      (cx, cy + 22), (cx - 18, cy + 4), (cx - 18, cy - 14)],
                     outline=w, width=3)
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            x, y = cx + 9 * math.cos(a), cy - 2 + 9 * math.sin(a)
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=w)
    elif kind == "drone":
        for dx, dy in ((-18, -14), (18, -14), (-18, 14), (18, 14)):
            draw.ellipse([cx + dx - 8, cy + dy - 4, cx + dx + 8, cy + dy + 4],
                         outline=w, width=3)
            draw.line([cx, cy, cx + dx, cy + dy], fill=w, width=3)
        draw.rectangle([cx - 7, cy - 5, cx + 7, cy + 5], fill=w)
    elif kind == "doc":
        draw.rectangle([cx - 14, cy - 20, cx + 14, cy + 20], outline=w, width=3)
        draw.line([cx - 8, cy - 10, cx + 8, cy - 10], fill=w, width=3)
        draw.line([cx - 8, cy - 2, cx + 8, cy - 2], fill=w, width=3)
        draw.line([cx - 8, cy + 8, cx - 1, cy + 15], fill=w, width=3)
        draw.line([cx - 1, cy + 15, cx + 10, cy - 4], fill=w, width=3)
    elif kind == "link":
        draw.ellipse([cx - 24, cy - 13, cx + 2, cy + 13], outline=w, width=3)
        draw.ellipse([cx - 2, cy - 13, cx + 24, cy + 13], outline=w, width=3)
    elif kind == "flag":
        draw.line([cx - 12, cy - 22, cx - 12, cy + 22], fill=w, width=4)
        draw.polygon([(cx - 12, cy - 22), (cx + 20, cy - 14), (cx - 12, cy - 6)],
                     fill=w)


def render(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Masthead: serif title block, the date set as large as the page allows.
    d.rectangle([0, 0, W, 156], fill=NAVY)
    d.text((48, 18), "THE WORLD IN ONE DAY", font=font(FB, 24), fill=GOLD)
    d.text((48, 46), f"{WEEKDAY} · {DATE}", font=font(SB, 56),
           fill=(255, 255, 255))
    d.rectangle([48, 118, W - 48, 121], fill=GOLD)
    d.text((48, 128), "The day's biggest stories, on one page",
           font=font(FR, 18), fill=(190, 198, 220))
    # Panels: 2 cols x 3 rows.
    px, py, pw, ph, gap = 32, 174, 472, 226, 14
    for i, (kicker, color, ic, head, body) in enumerate(PANELS):
        x = px + (i % 2) * (pw + gap)
        y = py + (i // 2) * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=CARD, outline=BORDER, width=1)
        d.rectangle([x, y, x + 8, y + ph], fill=color)
        icon(d, ic, x + pw - 52, y + 46, 30, color)
        d.text((x + 26, y + 18), kicker, font=font(FB, 19), fill=color)
        hy = y + 46
        for line in wrap(d, head, font(FB, 29), pw - 130)[:3]:
            d.text((x + 26, hy), line, font=font(FB, 29), fill=INK)
            hy += 34
        by = hy + 6
        for line in wrap(d, body, font(FR, 20), pw - 48)[:3]:
            d.text((x + 26, by), line, font=font(FR, 20), fill=GREY)
            by += 25
    # Ticker: two wrapped lines on a navy strip.
    ty = py + 3 * ph + 2 * gap + 12
    d.rectangle([0, ty, W, ty + 64], fill=NAVY)
    ly = ty + 10
    for line in wrap(d, TICKER, font(FB, 16), W - 64)[:2]:
        d.text((32, ly), line, font=font(FB, 16), fill=(255, 255, 255))
        ly += 24
    # Footer: name the day once more, in words.
    d.text((32, ty + 76),
           "Events that happened, or were first reported, on Sunday "
           "22 November 2026 — in any time zone.",
           font=font(FR, 17), fill=GREY)
    img.save(out_path, optimize=True)
    print(out_path, "saved")


if __name__ == "__main__":
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    render(os.path.join(out_dir, "entry.png"))
