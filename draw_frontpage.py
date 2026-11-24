#!/usr/bin/env python3
"""THE WORLD - Tuesday 24 November 2026.

A whole day of world news on a single newspaper front page, drawn
entirely in code with Python + Pillow: 44 date-checked stories from
8 regions - 6 illustrated lead panels and 38 numbered briefs.
Output: entry.png (JPEG, 1024x1024, under 1 MiB).
"""
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 14
PAPER = (247, 240, 222)
BLACK = (26, 28, 36)
ACCENT = (148, 28, 28)
CARD = (255, 253, 245)
CARD_EDGE = (205, 193, 163)
GREY = (95, 91, 79)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS_PLAIN = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
pen = ImageDraw.Draw(canvas)

REGION_INFO = {
    "NA": ("NORTH AMERICA", (37, 99, 235)),
    "EU": ("EUROPE", (124, 58, 237)),
    "ME": ("MIDDLE EAST", (217, 119, 6)),
    "AF": ("AFRICA", (5, 150, 105)),
    "SA": ("SOUTH ASIA", (220, 38, 38)),
    "EA": ("EAST ASIA", (219, 39, 119)),
    "SEA": ("SOUTHEAST ASIA", (8, 145, 178)),
    "OC": ("OCEANIA", (101, 163, 13)),
}
REGION_ORDER = ["NA", "EU", "ME", "AF", "SA", "EA", "SEA", "OC"]


def wrap_lines(text, fnt, width):
    """Greedy word wrap measured with the real font metrics."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if pen.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def paragraph(x, y, text, fnt, width, fill=BLACK, leading=1.18, centered=False):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap_lines(text, fnt, width):
        if centered:
            lx = x + (width - pen.textlength(line, font=fnt)) / 2
        else:
            lx = x
        pen.text((lx, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def region_tag(x, y, code, fnt):
    """Small filled chip with the region code; returns its width."""
    colour = REGION_INFO[code][1]
    w = pen.textlength(code, font=fnt) + 10
    pen.rounded_rectangle([x, y, x + w, y + fnt.size + 5], 3, fill=colour)
    pen.text((x + 5, y + 2), code, font=fnt, fill=(255, 255, 255))
    return w


# ------------------------------ masthead ------------------------------
pen.rectangle([0, 0, SIZE, 5], fill=ACCENT)
f_name = font(SERIF_BOLD, 56)
name = "THE WORLD"
pen.text(((SIZE - pen.textlength(name, font=f_name)) / 2, 12),
         name, font=f_name, fill=BLACK)
f_strap = font(SANS_BOLD, 15)
pen.text((MARGIN, 80), "TUESDAY 24 NOVEMBER 2026", font=f_strap, fill=ACCENT)
counts_line = "44 date-checked stories · 8 regions"
pen.text(((SIZE - pen.textlength(counts_line, font=f_strap)) / 2, 80),
         counts_line, font=f_strap, fill=BLACK)
tail = "ONE DAY · ONE PAGE"
pen.text((SIZE - MARGIN - pen.textlength(tail, font=f_strap), 80),
         tail, font=f_strap, fill=ACCENT)
pen.line([MARGIN, 104, SIZE - MARGIN, 104], fill=BLACK, width=3)
pen.line([MARGIN, 109, SIZE - MARGIN, 109], fill=BLACK, width=1)


# --------------------------- lead scenes ---------------------------

def scene_markets(x, y, w, h):
    """Night skyline, glowing windows, a green rally line climbing."""
    pen.rectangle([x, y, x + w, y + h], fill=(15, 26, 50))
    towers = [(6, 40), (48, 62), (94, 34), (140, 74), (188, 50), (232, 66), (276, 40)]
    for bx, bh in towers:
        pen.rectangle([x + bx, y + h - bh, x + bx + 32, y + h], fill=(29, 46, 82))
        wy = y + h - bh + 7
        while wy < y + h - 7:
            pen.rectangle([x + bx + 6, wy, x + bx + 12, wy + 5], fill=(250, 204, 21))
            pen.rectangle([x + bx + 19, wy, x + bx + 25, wy + 5], fill=(147, 197, 253))
            wy += 12
    path = [(x + 6, y + h - 20), (x + 66, y + h - 40), (x + 126, y + h - 30),
            (x + 186, y + h - 62), (x + 246, y + h - 52), (x + w - 12, y + 14)]
    pen.line(path, fill=(34, 197, 94), width=5)
    for px, py in path:
        pen.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(187, 247, 208))
    hx, hy = path[-1]
    pen.polygon([(hx, hy), (hx - 16, hy + 2), (hx - 4, hy + 14)], fill=(34, 197, 94))
    f = font(SANS_BOLD, 14)
    pen.text((x + 9, y + 7), "NIKKEI +4.5% · KOSPI +7.5%", font=f, fill=(187, 247, 208))


def scene_quake(x, y, w, h):
    """Dawn sky, two small houses, a crack in the earth, M5.3 badge."""
    pen.rectangle([x, y, x + w, y + h], fill=(253, 230, 190))
    pen.rectangle([x, y + h - 30, x + w, y + h], fill=(178, 130, 84))
    for hx, hw in [(36, 66), (206, 62)]:
        pen.rectangle([x + hx, y + h - 56, x + hx + hw, y + h - 30], fill=(255, 251, 235))
        pen.polygon([(x + hx - 8, y + h - 56), (x + hx + hw / 2, y + h - 82),
                     (x + hx + hw + 8, y + h - 56)], fill=(122, 72, 40))
    pen.line([x + 245, y + h - 82, x + 254, y + h - 56], fill=(122, 72, 40), width=3)
    crack = [(x + 4, y + h - 5), (x + 66, y + h - 11), (x + 116, y + h - 4),
             (x + 178, y + h - 12), (x + 240, y + h - 5), (x + w - 6, y + h - 10)]
    pen.line(crack, fill=(70, 40, 20), width=4)
    pen.ellipse([x + w - 60, y + 7, x + w - 12, y + 55], fill=ACCENT)
    f = font(SANS_BOLD, 18)
    s = "M5.3"
    pen.text((x + w - 36 - pen.textlength(s, font=f) / 2, y + 21), s,
             font=f, fill=(255, 255, 255))
    pen.text((x + 9, y + h - 25), "07:02 · KOSHI PROVINCE",
             font=font(SANS_BOLD, 12), fill=(70, 40, 20))


def scene_strike(x, y, w, h):
    """Night city silhouette, moon, and a blast over the rooftops."""
    pen.rectangle([x, y, x + w, y + h], fill=(22, 27, 52))
    pen.ellipse([x + w - 58, y + 10, x + w - 28, y + 40], fill=(226, 232, 240))
    pen.ellipse([x + w - 50, y + 6, x + w - 22, y + 36], fill=(22, 27, 52))
    for sx, sy in [(24, 16), (84, 9), (150, 22), (206, 8)]:
        pen.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(203, 213, 225))
    base = y + h
    pen.polygon([(x, base), (x, base - 34), (x + 58, base - 34), (x + 58, base)],
                fill=(9, 12, 28))
    pen.polygon([(x + 66, base), (x + 66, base - 48), (x + 148, base - 48),
                 (x + 148, base)], fill=(9, 12, 28))
    pen.polygon([(x + 156, base), (x + 156, base - 27), (x + w, base - 27),
                 (x + w, base)], fill=(9, 12, 28))
    for wx, wy in [(14, base - 24), (88, base - 38), (118, base - 20), (196, base - 18)]:
        pen.rectangle([x + wx, wy, x + wx + 7, wy + 9], fill=(250, 204, 21))
    cx, cy = x + 224, y + 40
    for r, col in [(29, (249, 115, 22)), (20, (251, 146, 60)), (11, (254, 215, 170))]:
        pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for dx, dy in [(-36, -13), (32, -19), (-7, -34), (21, 21), (-28, 17)]:
        pen.line([cx, cy, cx + dx, cy + dy], fill=(251, 146, 60), width=3)
    pen.ellipse([cx - 50, cy + 15, cx + 6, cy + 32], fill=(100, 116, 139))
    pen.ellipse([cx - 28, cy + 7, cx + 24, cy + 26], fill=(120, 134, 155))


def scene_alert(x, y, w, h):
    """Day sky over green hills: a jet crosses, radar arcs pulse."""
    pen.rectangle([x, y, x + w, y + h], fill=(188, 226, 250))
    pen.polygon([(x, y + h), (x, y + h - 24), (x + 108, y + h - 38),
                 (x + 218, y + h - 22), (x + w, y + h - 36), (x + w, y + h)],
                fill=(21, 94, 60))
    jx, jy = x + 172, y + 40
    pen.polygon([(jx - 64, jy + 7), (jx - 16, jy - 6), (jx + 42, jy - 2),
                 (jx + 68, jy + 7), (jx + 38, jy + 13), (jx - 28, jy + 13)],
                fill=(51, 65, 85))
    pen.polygon([(jx + 36, jy - 2), (jx + 54, jy - 21), (jx + 66, jy - 19),
                 (jx + 56, jy + 2)], fill=(51, 65, 85))
    pen.polygon([(jx - 50, jy + 9), (jx - 68, jy + 24), (jx - 54, jy + 25),
                 (jx - 34, jy + 13)], fill=(51, 65, 85))
    for r in (17, 33, 49):
        pen.arc([x + 34 - r, y + h - 44 - r, x + 34 + r, y + h - 44 + r],
                start=290, end=60, fill=ACCENT, width=3)
    pen.ellipse([x + 29, y + h - 49, x + 39, y + h - 39], fill=ACCENT)
    pen.text((x + 9, y + 7), "ULLEUNG ISLAND · 07:52",
             font=font(SANS_BOLD, 12), fill=(30, 64, 110))


def scene_flood(x, y, w, h):
    """Grey valley, a mud wall pouring down, rescue helicopter above."""
    pen.rectangle([x, y, x + w, y + h], fill=(203, 213, 225))
    pen.polygon([(x, y + h), (x, y + 36), (x + 88, y + h)], fill=(100, 116, 139))
    pen.polygon([(x + w, y + h), (x + w, y + 30), (x + w - 94, y + h)],
                fill=(100, 116, 139))
    pen.polygon([(x, y + 36), (x + 21, y + 58), (x - 8, y + 60)], fill=(248, 250, 252))
    pen.polygon([(x + w, y + 30), (x + w - 23, y + 54), (x + w + 6, y + 56)],
                fill=(248, 250, 252))
    pen.polygon([(x + 58, y + h), (x + 128, y + h - 54), (x + 194, y + h - 40),
                 (x + 248, y + h - 62), (x + w - 38, y + h)], fill=(146, 104, 66))
    pen.polygon([(x + 82, y + h), (x + 148, y + h - 37), (x + 208, y + h - 27),
                 (x + w - 68, y + h)], fill=(120, 84, 50))
    rx = 12
    while rx < w - 8:
        pen.line([x + rx, y + 5, x + rx - 6, y + 22], fill=(100, 116, 139), width=2)
        rx += 25
    hx, hy = x + w - 96, y + 22
    pen.rounded_rectangle([hx, hy, hx + 44, hy + 16], 6, fill=(185, 28, 28))
    pen.line([hx - 26, hy + 1, hx + 70, hy + 1], fill=(51, 65, 85), width=4)
    pen.line([hx + 22, hy + 16, hx + 22, hy + 29], fill=(51, 65, 85), width=2)
    pen.line([hx + 44, hy + 8, hx + 58, hy + 1], fill=(51, 65, 85), width=3)


def scene_travel(x, y, w, h):
    """Blue morning: terminal block, a climbing jet, tiny travellers."""
    pen.rectangle([x, y, x + w, y + h], fill=(224, 242, 254))
    pen.ellipse([x + 14, y + 10, x + 48, y + 44], fill=(250, 204, 21))
    pen.rectangle([x, y + h - 28, x + w, y + h], fill=(71, 85, 105))
    pen.rectangle([x + 16, y + h - 60, x + 124, y + h - 28], fill=(148, 163, 184))
    pen.rectangle([x + 58, y + 5, x + 73, y + h - 60], fill=(100, 116, 139))
    for i in range(4):
        pen.rectangle([x + 26 + i * 23, y + h - 50, x + 37 + i * 23, y + h - 39],
                      fill=(224, 242, 254))
    px, py = x + 222, y + 38
    pen.polygon([(px - 60, py + 9), (px + 28, py - 6), (px + 64, py + 1),
                 (px + 28, py + 11), (px - 38, py + 15)], fill=(30, 64, 175))
    pen.polygon([(px + 20, py - 4), (px + 38, py - 23), (px + 50, py - 21),
                 (px + 40, py + 1)], fill=(30, 64, 175))
    coats = [(239, 68, 68), (34, 197, 94), (59, 130, 246), (234, 179, 8), (168, 85, 247)]
    for i, coat in enumerate(coats):
        qx = x + 170 + i * 25
        pen.ellipse([qx, y + h - 49, qx + 11, y + h - 38], fill=(71, 50, 30))
        pen.rectangle([qx + 1, y + h - 38, qx + 10, y + h - 26], fill=coat)
    pen.text((x + 82, y + 7), "52,000 FLIGHTS",
             font=font(SANS_BOLD, 13), fill=(30, 64, 110))


# --------------------------- story data ---------------------------
LEADS = [
    ("EA", scene_markets, "ASIA MARKETS ROCKET IN CHIP RALLY",
     "Tokyo +4.5%, Seoul +7.5% and Taiwan +9.1% as Jensen Huang's return to Nvidia revives the AI trade."),
    ("SA", scene_quake, "DAWN QUAKE SHAKES NEPAL",
     "A magnitude 5.3 quake hits Koshi province; tremors are felt across India, Bhutan, Bangladesh and China."),
    ("EU", scene_strike, "RUSSIAN STRIKE KILLS TWO IN ZAPORIZHZHIA",
     "An overnight attack wounds 22 people, including two children, in the frontline Ukrainian city."),
    ("EA", scene_alert, "SEOUL SOUNDS AIR ALERT OVER RUSSIAN JET",
     "An evacuation warning sounds for Ulleung Island as a Russian aircraft enters Korean airspace."),
    ("SA", scene_flood, "HIMALAYAN FLOOD LEAVES 100 MISSING",
     "A wall of mud tears down an Indian mountain valley; at least four die as the army searches."),
    ("NA", scene_travel, "AMERICA TAKES OFF FOR THANKSGIVING",
     "The FAA braces for its busiest holiday in 16 years: 81.5 million Americans on the move."),
]

BRIEFS = [
    ("NA", "Mexico will prosecute cartel boss 'El Chapo Isidro' at home, defying a US extradition bid"),
    ("NA", "FAA lifts ground stop at Chicago O'Hare after an air-traffic staffing snarl"),
    ("NA", "US lawmakers close ranks against Nvidia chief's return, pressing tighter China chip curbs"),
    ("NA", "Comedian roasts Trump at Toronto's journalists' dinner"),
    ("EU", "Ukraine says Neptune missiles struck a Russian drone plant in Rostov-on-Don"),
    ("EU", "EU loans for Ukraine will cost 55 billion euros in interest alone, a Commission paper shows"),
    ("EU", "Norway's supreme court voids oil licences in a landmark climate ruling"),
    ("EU", "France confirms a deadly bird-flu outbreak at a poultry farm"),
    ("EU", "Georgia plans a full ban on surrogacy over trafficking concerns"),
    ("EU", "Moldova survey finds voters backing the road to Europe"),
    ("EU", "Inter fall in seven-goal San Siro thriller as Tresoldi hits a hat-trick"),
    ("ME", "Israel arrests 10 after days of violent settler attacks in the West Bank"),
    ("ME", "Saudi-led strike on Hodeidah telecom building kills 10, Houthi media say"),
    ("ME", "UAE president takes call from Syria's al-Sharaa on deeper cooperation"),
    ("ME", "Drone attack wounds four security men in Syria's Suwayda countryside"),
    ("ME", "Gulf bourses slip as Saudi-Houthi clashes rattle investors"),
    ("ME", "Erdogan plans a first visit to Libya in 15 years"),
    ("AF", "Nigeria: governor orders probe as eight-year-old dies in Abia school collapse"),
    ("AF", "At least 24 civilians killed in South Sudan's Warrap state"),
    ("AF", "Ethiopia's central bank holds a $140m foreign-exchange auction"),
    ("AF", "Museveni accepts an invitation to visit Somalia after talks with Mohamud"),
    ("AF", "Sahel states restart dialogue with the West Africa bloc"),
    ("AF", "Kenya secures 293,600 Saudi job openings for its workers"),
    ("SA", "Bangladesh begins vaccinating 50 million children against typhoid"),
    ("SA", "Former MP Prajwal Revanna is sentenced to life in prison for rape"),
    ("SA", "India holds third place in the Asia Power Index; Modi ranked second leader"),
    ("SA", "New Saryu-Kamala Express train links Ayodhya with Janakpur in Nepal"),
    ("EA", "SoftBank to invest $2bn in Intel"),
    ("EA", "Japan creates a new government body on foreign-resident concerns"),
    ("EA", "Japan's factory activity quickens as manufacturing PMI climbs to 53.7"),
    ("EA", "Seoul seeks priority Qatari LNG cargoes as Hormuz shipping normalises"),
    ("SEA", "Philippine Senate opens plenary debates on the 2027 national budget"),
    ("SEA", "S&P tips the Philippines to be SE Asia's slowest-growing economy in 2026"),
    ("SEA", "SE Asia's AI data-centre boom faces Nvidia supply curbs"),
    ("SEA", "Jollibee plans 30 UK restaurants in a franchise expansion"),
    ("OC", "Severe heatwave warning issued for Queensland's Cape York Peninsula"),
    ("OC", "Australia to treat AI as a first-order foreign-policy challenge"),
    ("OC", "Australia rotate squad for Rugby League World Cup final vs New Zealand"),
]

# --------------------------- lead panels ---------------------------
PANEL_W, PANEL_H, GAP = 326, 200, 9
PANEL_Y = 114
f_headline = font(SANS_BOLD, 16)
f_summary = font(SANS_PLAIN, 12)
f_tagline = font(SANS_BOLD, 10)
for i, (code, scene, headline, summary) in enumerate(LEADS):
    px = MARGIN + (i % 3) * (PANEL_W + GAP)
    py = PANEL_Y + (i // 3) * (PANEL_H + GAP)
    pen.rounded_rectangle([px, py, px + PANEL_W, py + PANEL_H], 6,
                          fill=CARD, outline=CARD_EDGE, width=1)
    scene(px + 5, py + 5, PANEL_W - 10, 88)
    tag_y = py + 99
    region_tag(px + 10, tag_y, code, f_tagline)
    pen.text((px + 54, tag_y + 2), REGION_INFO[code][0],
             font=f_tagline, fill=GREY)
    paragraph(px + 10, tag_y + 19, headline, f_headline, PANEL_W - 20, leading=1.12)
    paragraph(px + 10, tag_y + 56, summary, f_summary, PANEL_W - 20, leading=1.22)

# --------------------------- timeline ---------------------------
TL_Y = PANEL_Y + 2 * PANEL_H + GAP + 10
pen.line([MARGIN, TL_Y, SIZE - MARGIN, TL_Y], fill=BLACK, width=2)
f_tl = font(SANS_BOLD, 11)
timeline = ("THE DAY AROUND THE WORLD — 07:02 Kathmandu quake · 07:52 Seoul air alert · "
            "Tokyo markets leap 4.5% · Zaporizhzhia struck overnight · US Thanksgiving rush peaks")
paragraph(MARGIN, TL_Y + 5, timeline, f_tl, SIZE - 2 * MARGIN, fill=ACCENT, leading=1.15)
pen.line([MARGIN, TL_Y + 32, SIZE - MARGIN, TL_Y + 32], fill=BLACK, width=2)

# --------------------------- briefs ---------------------------
BRIEF_Y = TL_Y + 44
f_brief_head = font(SANS_BOLD, 15)
pen.text((MARGIN, BRIEF_Y), "THE DAY IN BRIEF", font=f_brief_head, fill=BLACK)
pen.text((MARGIN + pen.textlength("THE DAY IN BRIEF", font=f_brief_head) + 12, BRIEF_Y + 2),
         "38 more stories, numbered 1-38", font=font(SANS_PLAIN, 11), fill=GREY)

tally = {}
for code, *_rest in LEADS:
    tally[code] = tally.get(code, 0) + 1
for code, _text in BRIEFS:
    tally[code] = tally.get(code, 0) + 1
key_x = MARGIN
f_key = font(SANS_BOLD, 10)
for code in REGION_ORDER:
    w = region_tag(key_x, BRIEF_Y + 24, code, f_key)
    label = REGION_INFO[code][0].title() + " " + str(tally[code])
    pen.text((key_x + w + 4, BRIEF_Y + 26), label, font=font(SANS_PLAIN, 10), fill=BLACK)
    key_x += w + 8 + pen.textlength(label, font=font(SANS_PLAIN, 10)) + 14

COLUMNS = [BRIEFS[0:13], BRIEFS[13:26], BRIEFS[26:38]]
COL_TOP = BRIEF_Y + 56
COL_LIMIT = 984
chosen = 9
for size in (11, 10.5, 10, 9.5, 9):
    f_try = font(SANS_PLAIN, size)
    worst = 0
    for col in COLUMNS:
        cy = COL_TOP
        for _code, txt in col:
            cy += len(wrap_lines(txt, f_try, PANEL_W - 62)) * int(size * 1.16) + 4
        worst = max(worst, cy)
    if worst <= COL_LIMIT:
        chosen = size
        break
f_brief = font(SANS_PLAIN, chosen)
f_num = font(SANS_BOLD, chosen)
for ci, col in enumerate(COLUMNS):
    cx = MARGIN + ci * (PANEL_W + GAP)
    cy = COL_TOP
    for j, (code, txt) in enumerate(col):
        number = ci * 13 + j + 1
        pen.text((cx, cy), str(number) + ".", font=f_num, fill=ACCENT)
        region_tag(cx + 24, cy, code, font(SANS_BOLD, 9))
        cy = paragraph(cx + 58, cy, txt, f_brief, PANEL_W - 62, leading=1.16) + 4

# --------------------------- footer ---------------------------
pen.line([MARGIN, 988, SIZE - MARGIN, 988], fill=BLACK, width=2)
footer = ("Every story on this page happened, or was first reported, on Tuesday 24 November 2026, "
          "checked against its source. Drawn in code - no photographs.")
paragraph(MARGIN, 994, footer, font(SANS_PLAIN, 11), SIZE - 2 * MARGIN,
          fill=GREY, centered=True)

canvas.save("entry.png", format="JPEG", quality=90)
print("entry.png bytes:", os.path.getsize("entry.png"))
