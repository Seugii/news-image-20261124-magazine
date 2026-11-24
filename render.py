#!/usr/bin/env python3
"""Render the make.fun 24 Nov 2026 magazine-cover entry (1024x1024).

Magazine concept: bold red masthead with the date, one dominant cover photo
(Trump + Netanyahu) with the cover headline, 8 feature tiles with photos and
short descriptions, and an ALSO ON strip. All facts come from the verified
research file (research-20261124.md). Photos: Wikimedia Commons, free licences.
Deterministic: no timestamps, no randomness.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
M = 24                      # side margin
CW = W - 2 * M              # 976 content width

PAPER = (255, 248, 231)     # warm cream
INK = (20, 20, 20)
GRAY = (85, 85, 85)
RED = (210, 16, 52)
DARKRED = (143, 10, 34)
YELLOW = (255, 199, 0)
BLUE = (0, 87, 184)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover_crop(img, tw, th):
    """Centre-crop an image to exactly tw x th (cover behaviour)."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def paste_photo(canvas, name, box):
    """Paste a photo centre-cropped into box (x, y, w, h)."""
    x, y, w, h = box
    img = Image.open(os.path.join(PHOTOS, name)).convert("RGB")
    canvas.paste(cover_crop(img, w, h), (x, y))


# ---------------------------------------------------------------- content
MASTHEAD = "THE WORLD TODAY"
DATE_LINE_1 = "TUESDAY"
DATE_LINE_2 = "24 NOVEMBER 2026"

COVER_KICKER = "COVER STORY  •  IRAN"
COVER_HEAD = ["NETANYAHU URGES TRUMP:", "STRIKE IRAN WITHOUT DELAY"]
COVER_DECK = (
    "Netanyahu pressed Trump for fresh strikes on Iran \u201cas soon as possible\u201d, "
    "Kan reports. Trump has not decided and is said to be reluctant; IDF "
    "intelligence warns of a multi-front war."
)

# (label, label colour, photo or None for stat tile, headline, description)
TILES = [
    ("WAR IN UKRAINE", RED, "russia_lyman.jpg",
     "700,000 RUSSIAN DEAD",
     "Leaked state data put the war's Russian death toll past 700,000 \u2014 "
     "Moscow's deadliest war since WWII."),
    ("UKRAINE", BLUE, "zaporizhzhia.jpg",
     "BOMBS HIT ZAPORIZHZHIA",
     "Guided bombs wound at least 11 and partly collapse a five-storey "
     "block in overnight strikes."),
    ("INDONESIA", (242, 107, 33), None,
     "CANDY FACTORY FIRE TOLL",
     "24 confirmed dead and about 30 still missing after the blaze at the "
     "Milkita plant in Banten."),
    ("MARKETS", (0, 137, 123), "bitcoin.jpg",
     "BITCOIN HOLDS $60,000",
     "Briefly past $64,000 overnight, then back to ~$60,500 \u2014 still 24% "
     "down in a month."),
    ("TECH", (106, 31, 181), "huang.jpg",
     "NVIDIA SOARS 30%",
     "Shares jump after Jensen Huang's return as CEO \u2014 a comeback pressed "
     "by Trump himself."),
    ("LIBYA", (26, 35, 126), "merkury.jpg",
     "UN SEEKS LIBYA PROBE",
     "Kyiv's sea drones sank the Russian corvette Merkury off Benghazi; "
     "the UN wants answers."),
    ("ASIA", (46, 125, 50), "nepal.jpg",
     "QUAKE SHAKES NEPAL",
     "A 5.6-magnitude tremor strikes Koshi province near the Chinese border."),
    ("SPACE", (120, 20, 20), "falcon9.jpg",
     "$3.5TN SPACEX\u2013TESLA TALKS",
     "Directors race to finalise a giant merger by year-end, the FT reports."),
]

ALSO_ON = [
    ("PATRIOTS DELAYED", "US holds back 60 interceptors for Ukraine."),
    ("HORMUZ", "UK logs record Iranian attacks in the strait."),
    ("ESTONIA", "Russia: neighbour's moves \u201cverge of open war\u201d."),
    ("GROK SUED", "Oregon & Virginia sue SpaceX over AI abuse images."),
    ("GAZA", "Israeli strikes kill at least 3, incl. UNRWA worker."),
    ("ROHINGYA", "14 nations back ICJ genocide ruling on Myanmar."),
    ("MEASLES", "Pennsylvania records a 9th death in the outbreak."),
    ("HOUTHIS", "Saudi airstrike kills 17 in Hodeida, Yemen."),
]

FOOTER = ("Photos: Wikimedia Commons \u2014 White House (public domain); CC BY / CC BY-SA / CC0. "
          "Tuesday 24 November 2026.")


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top yellow rule -------------------------------------------------
    d.rectangle([0, 0, W, 6], fill=YELLOW)

    # --- masthead ---------------------------------------------------------
    d.rectangle([0, 6, W, 88], fill=RED)
    f_title = font(SERIF_B, 54)
    d.text((M, 24), MASTHEAD, font=f_title, fill=WHITE)
    f_d1 = font(SANS_B, 25)
    f_d2 = font(SANS_B, 25)
    w1 = d.textlength(DATE_LINE_1, font=f_d1)
    w2 = d.textlength(DATE_LINE_2, font=f_d2)
    d.text((W - M - w1, 16), DATE_LINE_1, font=f_d1, fill=YELLOW)
    d.text((W - M - w2, 46), DATE_LINE_2, font=f_d2, fill=WHITE)

    # --- cover photo ------------------------------------------------------
    paste_photo(img, "cover_trump_netanyahu.jpg", (M, 88, CW, 332))
    # headline strip inside the bottom of the photo
    strip_y = 88 + 332 - 96
    d.rectangle([M, strip_y, M + CW, 88 + 332], fill=DARKRED)
    f_kick = font(SANS_B, 15)
    d.text((M + 14, strip_y + 7), COVER_KICKER, font=f_kick, fill=YELLOW)
    f_head = font(SANS_B, 32)
    draw_lines(d, COVER_HEAD, M + 14, strip_y + 27, f_head, WHITE, 36)

    # --- cover deck -------------------------------------------------------
    f_deck = font(SANS, 16)
    draw_lines(d, wrap(d, COVER_DECK, f_deck, CW), M, 428, f_deck, INK, 20)

    # --- section label ----------------------------------------------------
    f_sec = font(SANS_B, 16)
    d.text((M, 476), "INSIDE TODAY", font=f_sec, fill=RED)
    d.line([(M + 150, 486), (W - M, 486)], fill=RED, width=2)

    # --- feature grid: 4 cols x 2 rows ------------------------------------
    tile_w = 238
    tile_h = 192
    gap_x = 8
    gap_y = 6
    grid_y = 500
    f_label = font(SANS_B, 12)
    f_th = font(SANS_B, 18)
    f_td = font(SANS, 12)
    for i, (label, colour, photo, head, desc) in enumerate(TILES):
        col, row = i % 4, i // 4
        x = M + col * (tile_w + gap_x)
        y = grid_y + row * (tile_h + gap_y)
        # photo (or stat block for the fire tile)
        if photo:
            paste_photo(img, photo, (x, y, tile_w, 84))
        else:
            d.rectangle([x, y, x + tile_w, y + 84], fill=YELLOW)
            f_big = font(SANS_B, 62)
            d.text((x + 12, y + 4), "24", font=f_big, fill=RED)
            f_stat = font(SANS_B, 15)
            d.text((x + 108, y + 22), "DEAD", font=f_stat, fill=INK)
            d.text((x + 108, y + 44), "~30 MISSING", font=f_stat, fill=INK)
        # label bar
        ly = y + 84
        d.rectangle([x, ly, x + tile_w, ly + 18], fill=colour)
        d.text((x + 6, ly + 3), label, font=f_label, fill=WHITE)
        # headline + description
        ty = ly + 22
        head_lines = wrap(d, head, f_th, tile_w - 4)[:2]
        ty = draw_lines(d, head_lines, x + 2, ty, f_th, INK, 21)
        desc_lines = wrap(d, desc, f_td, tile_w - 4)[:3]
        draw_lines(d, desc_lines, x + 2, ty + 2, f_td, GRAY, 15)

    # --- ALSO ON ----------------------------------------------------------
    ay = 896
    f_ao = font(SANS_B, 17)
    d.text((M, ay), "ALSO ON TODAY", font=f_ao, fill=RED)
    d.line([(M + 172, ay + 10), (W - M, ay + 10)], fill=RED, width=2)
    f_kw = font(SANS_B, 12)
    f_tx = font(SANS, 12)
    col_w = (CW - 16) // 2
    for i, (kw, tx) in enumerate(ALSO_ON):
        col, row = i % 2, i // 2
        x = M + col * (col_w + 16)
        y = ay + 26 + row * 20
        kw_text = kw + " \u2014 "
        d.text((x, y), kw_text, font=f_kw, fill=INK)
        kx = x + d.textlength(kw_text, font=f_kw)
        # shrink the sentence until it fits the column
        sent = tx
        while d.textlength(sent, font=f_tx) > col_w - (kx - x) and len(sent) > 10:
            sent = sent[:-1]
        if sent != tx:
            sent = sent.rstrip(" .,") + "\u2026"
        d.text((kx, y), sent, font=f_tx, fill=GRAY)

    # --- footer -----------------------------------------------------------
    f_ft = font(SANS, 9)
    d.text((M, 1004), FOOTER, font=f_ft, fill=GRAY)

    # --- save: PNG first, JPEG fallback if over 1 MiB ----------------------
    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    if size > 1048576:
        img.save(OUT, "JPEG", quality=88, optimize=True)
        size = os.path.getsize(OUT)
    print(f"saved {OUT} {img.size[0]}x{img.size[1]} {size} bytes")
    return size


if __name__ == "__main__":
    render()
