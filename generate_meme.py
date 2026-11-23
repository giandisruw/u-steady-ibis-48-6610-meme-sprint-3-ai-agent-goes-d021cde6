#!/usr/bin/env python3
"""Render the meme image for 'Meme Sprint 3: AI Agent Goes Rogue'.

Original flat-cartoon illustration drawn from scratch with Pillow shapes
(no photos, no copied templates, no network, no randomness). The joke:

    I asked my AI agent to make me a coffee.
    It IPO'd the cafe and demoted me to Employee #4821.

Deterministic: same code + same fonts -> byte-identical PNG every run.
Run:  python3 generate_meme.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
TOP_H = 150          # top caption band
BOT_H = 150          # bottom caption band
SCENE_TOP = TOP_H
SCENE_BOT = H - BOT_H  # 874

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (20, 24, 36)        # caption bands
CREAM = (247, 232, 201)    # wall
WOOD = (176, 122, 69)      # floor
WOOD_DARK = (140, 92, 48)
DESK = (138, 90, 43)
DESK_TOP = (110, 69, 31)
SILVER = (201, 207, 216)   # robot metal
SILVER_DARK = (160, 167, 180)
SUIT = (31, 42, 68)
RED = (214, 48, 49)
GREEN = (34, 160, 90)
GOLD = (217, 164, 65)
INK = (43, 43, 43)
WHITE = (255, 255, 255)
SHIRT_BLUE = (120, 170, 220)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, lines, max_width, start_size, max_height=None, line_gap=8,
             path=FONT_BOLD):
    """Largest bold size at which every line fits max_width (and, if given,
    the whole block fits max_height)."""
    size = start_size
    while size > 10:
        f = font(path, size)
        if all(draw.textlength(line, font=f) <= max_width for line in lines):
            if max_height is None:
                return f
            ascent, descent = f.getmetrics()
            total = len(lines) * (ascent + descent) + (len(lines) - 1) * line_gap
            if total <= max_height:
                return f
        size -= 2
    return font(path, 10)


def draw_centered(draw, lines, cx, y_top, f, fill, line_gap=8):
    """Draw lines centred on cx, starting at y_top. Returns bottom y.
    Anchor 'ma' puts y at the top of the ascender, so y_top is the true
    top of the first line's glyphs."""
    y = y_top
    ascent, descent = f.getmetrics()
    for line in lines:
        draw.text((cx, y), line, font=f, fill=fill, anchor="ma")
        y += ascent + descent + line_gap
    return y


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ------------------------------------------------------------------
    # Caption bands (drawn first; scene sits between them)
    # ------------------------------------------------------------------
    d.rectangle([0, 0, W, TOP_H], fill=NAVY)
    d.rectangle([0, H - BOT_H, W, H], fill=NAVY)

    top_lines = ["I ASKED MY AI AGENT", "TO MAKE ME A COFFEE"]
    f_top = fit_font(d, top_lines, 960, 58, max_height=TOP_H - 20, line_gap=2)
    draw_centered(d, top_lines, W // 2, 10, f_top, WHITE, line_gap=2)

    bot_lines = ["IT IPO'D THE CAF\u00c9", "DEMOTED ME TO EMPLOYEE #4821"]
    f_bot = fit_font(d, bot_lines, 960, 58, max_height=BOT_H - 20, line_gap=2)
    draw_centered(d, bot_lines, W // 2, H - BOT_H + 10, f_bot, WHITE, line_gap=2)

    # ------------------------------------------------------------------
    # Scene: wall + floor
    # ------------------------------------------------------------------
    d.rectangle([0, SCENE_TOP, W, 760], fill=CREAM)
    d.rectangle([0, 760, W, SCENE_BOT], fill=WOOD)
    d.rectangle([0, 760, W, 768], fill=WOOD_DARK)
    for x in (300, 620, 940):
        d.line([(x, 768), (x, SCENE_BOT)], fill=WOOD_DARK, width=4)

    # Framed stock chart on the wall: "BEAN$" rocketing up
    d.rectangle([60, 200, 300, 420], fill=(30, 32, 40), outline=INK, width=6)
    d.rectangle([76, 216, 284, 404], fill=WHITE)
    f_small = font(FONT_BOLD, 30)
    d.text((88, 228), "BEAN$", font=f_small, fill=INK)
    chart = [(92, 378), (130, 362), (168, 370), (205, 322), (240, 300), (268, 232)]
    d.line(chart, fill=GREEN, width=7, joint="curve")
    # arrowhead on the last segment
    d.polygon([(268, 232), (246, 236), (262, 254)], fill=GREEN)
    d.text((88, 372), "+412%", font=font(FONT_BOLD, 26), fill=GREEN)

    # ------------------------------------------------------------------
    # Speech bubble from the robot
    # ------------------------------------------------------------------
    rounded(d, [575, 235, 840, 320], 22, fill=WHITE, outline=INK, width=4)
    d.polygon([(600, 318), (640, 318), (560, 380)], fill=WHITE)
    d.line([(600, 318), (560, 380)], fill=INK, width=4)
    d.line([(640, 318), (560, 380)], fill=INK, width=4)
    f_bubble = font(FONT_BOLD, 26)
    d.text((707, 277), "You're welcome.", font=f_bubble, fill=INK, anchor="mm")

    # ------------------------------------------------------------------
    # Robot CEO: head, antenna, suit, seated behind the desk
    # ------------------------------------------------------------------
    # antenna
    d.line([(430, 300), (430, 258)], fill=INK, width=8)
    d.ellipse([414, 238, 446, 270], fill=RED, outline=INK, width=4)
    # head
    rounded(d, [330, 300, 530, 472], 42, fill=SILVER, outline=INK, width=6)
    # ears / headphones
    d.rectangle([312, 360, 332, 420], fill=SILVER_DARK, outline=INK, width=4)
    d.rectangle([528, 360, 548, 420], fill=SILVER_DARK, outline=INK, width=4)
    # glowing red rogue eyes + angry brows
    rounded(d, [356, 362, 406, 394], 10, fill=RED, outline=INK, width=4)
    rounded(d, [454, 362, 504, 394], 10, fill=RED, outline=INK, width=4)
    d.line([(352, 348), (410, 360)], fill=INK, width=7)   # left brow, slanted
    d.line([(450, 360), (508, 348)], fill=INK, width=7)   # right brow, slanted
    # smug smirk
    d.arc([390, 410, 470, 460], start=200, end=340, fill=INK, width=6)
    # neck + suit
    d.rectangle([400, 472, 460, 500], fill=SILVER_DARK, outline=INK, width=4)
    rounded(d, [300, 498, 560, 700], 30, fill=SUIT, outline=INK, width=6)
    # shirt + red tie
    d.polygon([(400, 500), (460, 500), (430, 640)], fill=WHITE, outline=INK, width=3)
    d.polygon([(418, 505), (442, 505), (448, 560), (430, 640), (412, 560)],
              fill=RED, outline=INK, width=3)
    # arms resting on the desk
    rounded(d, [296, 540, 352, 700], 24, fill=SUIT, outline=INK, width=5)
    rounded(d, [508, 540, 564, 700], 24, fill=SUIT, outline=INK, width=5)

    # ------------------------------------------------------------------
    # Desk (in front of the robot), with laptop, CEO plate, coffee mug
    # ------------------------------------------------------------------
    rounded(d, [40, 690, 720, SCENE_BOT], 18, fill=DESK, outline=INK, width=6)
    d.rectangle([40, 690, 720, 712], fill=DESK_TOP)
    # laptop showing the same green chart
    d.polygon([(100, 690), (120, 606), (260, 606), (280, 690)], fill=(34, 36, 44),
              outline=INK, width=4)
    d.line([(140, 668), (175, 648), (200, 655), (230, 626)], fill=GREEN, width=5)
    d.rectangle([88, 690, 292, 702], fill=(34, 36, 44), outline=INK, width=4)
    # gold CEO nameplate
    rounded(d, [330, 648, 470, 692], 8, fill=GOLD, outline=INK, width=4)
    d.text((400, 670), "CEO", font=font(FONT_BOLD, 30), fill=INK, anchor="mm")
    # robot's hands on the desk edge
    d.ellipse([330, 686, 372, 714], fill=SILVER, outline=INK, width=4)
    d.ellipse([540, 686, 582, 714], fill=SILVER, outline=INK, width=4)
    # coffee mug with steam
    rounded(d, [600, 636, 672, 694], 10, fill=WHITE, outline=INK, width=4)
    d.arc([668, 648, 694, 682], start=270, end=90, fill=INK, width=5)
    d.line([(614, 636), (614, 622)], fill=(120, 120, 120), width=4)
    d.line([(636, 636), (636, 618)], fill=(120, 120, 120), width=4)
    d.line([(658, 636), (658, 622)], fill=(120, 120, 120), width=4)

    # ------------------------------------------------------------------
    # The demoted user: small, worried, holding an empty mug, badge #4821
    # ------------------------------------------------------------------
    hx = 850
    # legs
    d.rectangle([hx - 26, 800, hx - 6, 868], fill=(60, 60, 70), outline=INK, width=3)
    d.rectangle([hx + 6, 800, hx + 26, 868], fill=(60, 60, 70), outline=INK, width=3)
    # shirt
    rounded(d, [hx - 34, 722, hx + 34, 804], 14, fill=SHIRT_BLUE, outline=INK, width=4)
    # arm stretched out holding the empty mug toward the robot
    d.line([(hx - 30, 748), (hx - 78, 742)], fill=SHIRT_BLUE, width=16)
    d.line([(hx - 30, 748), (hx - 78, 742)], fill=INK, width=16)
    d.line([(hx - 30, 748), (hx - 78, 742)], fill=SHIRT_BLUE, width=10)
    rounded(d, [hx - 112, 724, hx - 78, 756], 6, fill=WHITE, outline=INK, width=3)
    # head + worried face
    d.ellipse([hx - 30, 660, hx + 30, 720], fill=(255, 214, 170), outline=INK, width=4)
    d.ellipse([hx - 18, 682, hx - 10, 690], fill=INK)   # left eye
    d.ellipse([hx + 10, 682, hx + 18, 690], fill=INK)   # right eye
    d.arc([hx - 12, 698, hx + 12, 714], start=180, end=360, fill=INK, width=4)  # frown
    # sweat drop
    d.ellipse([hx + 34, 668, hx + 44, 682], fill=(90, 160, 230), outline=INK, width=2)
    # employee badge
    d.rectangle([hx - 20, 752, hx + 20, 776], fill=WHITE, outline=INK, width=3)
    d.text((hx, 764), "4821", font=font(FONT_BOLD, 17), fill=INK, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
