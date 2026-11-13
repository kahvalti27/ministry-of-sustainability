"""The larger pictures, drawn by code: three lose screens and the cover for the store page.

Run:  python3 tools/scenes.py
Writes assets/scenes/<meter>.png (160x80, one per way to lose) and art/cover.png (630x500).
"""
from PIL import Image

from pixel import ASSETS, ROOT, C, Canvas

SCENES = ASSETS / "scenes"
W, H = 160, 80


def person(c, x, y, coat="navy", facing=1):
    """A small figure about 24 pixels tall, feet at (x, y)."""
    c.rect((x - 3, y - 9, x - 1, y - 1), "char")          # legs
    c.rect((x + 1, y - 9, x + 3, y - 1), "char")
    c.rect((x - 4, y - 1, x - 1, y), "line"); c.rect((x + 1, y - 1, x + 4, y), "line")
    c.rect((x - 4, y - 18, x + 4, y - 9), coat)            # coat
    c.col(x + 4 * facing, y - 18, y - 9, "navy_d")
    c.ell((x - 3, y - 25, x + 3, y - 19), "skin")          # head
    c.row(y - 25, x - 2, x + 2, "hair_d"); c.row(y - 24, x - 3, x + 3, "hair_d")
    c.px(x + 1 * facing, y - 22, "line")


# ---- Approval hits 0: fired ---------------------------------------------------------
def fired():
    c = Canvas(W, H)
    c.rect((0, 0, W, H), "sea_l")                           # sky
    c.rect((0, 62, W, H), "cream_d")                        # pavement
    c.row(62, 0, W, "wood_d")
    # the Ministry: wall, columns, an open door
    c.rect((0, 6, 92, 62), "cream")
    c.rect((0, 6, 92, 10), "cream_d"); c.row(11, 0, 92, "line")
    for x in (6, 22, 62, 78):
        c.rect((x, 12, x + 7, 61), "white"); c.col(x + 7, 12, 61, "cream_d")
        c.rect((x - 1, 12, x + 8, 14), "cream_d"); c.rect((x - 1, 59, x + 8, 61), "cream_d")
    c.rect((34, 20, 57, 61), "line")                        # doorway
    c.poly([(34, 20), (40, 24), (40, 61), (34, 61)], "wood") # door swung open
    c.col(40, 24, 61, "wood_d"); c.px(38, 42, "gold")
    c.rect((30, 60, 61, 63), "white"); c.rect((26, 63, 65, 66), "cream")  # steps
    c.col(92, 6, 62, "line")
    # the former Minister, with a box of belongings
    person(c, 118, 70)
    c.rect((122, 52, 134, 60), "wood"); c.rect((122, 52, 134, 53), "wood_d")
    c.rect((121, 55, 123, 57), "skin"); c.px(128, 56, "wood_d")
    c.poly([(126, 52), (126, 46), (129, 43), (130, 47), (129, 52)], "green")  # the office plant
    c.rect((131, 48, 133, 52), "white")
    # papers on the wind
    for x, y in ((70, 40), (84, 50), (100, 34), (146, 30)):
        c.rect((x, y, x + 4, y + 3), "white"); c.px(x + 1, y + 1, "hair_d"); c.px(x + 3, y + 2, "hair_d")
    c.ell((136, 6, 150, 20), "gold_l")                      # an indifferent sun
    return c.save(SCENES / "approval.png", outline=False)


# ---- Budget hits 0: closed, temporarily ------------------------------------------------
def closed():
    c = Canvas(W, H)
    c.rect((0, 0, W, H), "cream")
    c.rect((0, 0, W, 5), "cream_d"); c.row(6, 0, W, "line")
    c.rect((0, 70, W, H), "cream_d"); c.row(70, 0, W, "wood_d")
    for x in (10, 30, 122, 142):                             # columns
        c.rect((x, 7, x + 8, 69), "white"); c.col(x + 8, 7, 69, "cream_d")
    # double door
    c.rect((50, 10, 110, 70), "line")
    c.rect((52, 12, 79, 69), "wood"); c.rect((81, 12, 108, 69), "wood")
    for x in (52, 81):
        c.rect((x + 3, 16, x + 24, 36), "wood_d"); c.rect((x + 3, 42, x + 24, 65), "wood_d")
        c.rect((x + 5, 18, x + 22, 34), "wood"); c.rect((x + 5, 44, x + 22, 63), "wood")
    # chain and padlock
    for i, x in enumerate(range(54, 107, 3)):
        c.rect((x, 38, x + 1, 40), "hair" if i % 2 else "hair_d")
    c.d.arc((74, 30, 86, 44), 180, 360, fill=C["hair_d"], width=2)
    c.rect((72, 37, 88, 50), "gold"); c.rect((72, 37, 88, 38), "gold_l"); c.col(88, 37, 50, "gold_d"); c.row(50, 72, 88, "gold_d")
    c.rect((79, 41, 81, 43), "line"); c.rect((80, 43, 80, 46), "line")
    # a notice, pinned crooked, that nobody will update
    c.poly([(58, 20), (74, 17), (76, 30), (60, 33)], "white")
    for i in range(3):
        c.line([(61 + i // 2, 23 + i * 3), (72, 21 + i * 3)], "hair_d")
    c.px(66, 19, "red")
    # neglect: a cobweb and weeds
    for pts in ([(0, 7), (22, 7)], [(0, 7), (0, 26)], [(0, 7), (16, 20)], [(8, 7), (0, 14)], [(15, 7), (0, 20)]):
        c.line(pts, "hair")
    for x in (44, 47, 112, 116, 20):
        c.line([(x, 70), (x - 1, 64)], "green_d"); c.line([(x, 70), (x + 2, 66)], "green")
    return c.save(SCENES / "budget.png", outline=False)


# ---- Environment hits 0: disaster zone ---------------------------------------------------
def disaster():
    c = Canvas(W, H)
    c.rect((0, 0, W, H), "hair_d")                          # ash sky
    for x, y, w in ((10, 8, 40), (70, 14, 50), (120, 5, 36)):
        c.rect((x, y, x + w, y + 4), "hair"); c.rect((x + 6, y - 3, x + w - 8, y), "hair")
    # factory on the horizon
    c.rect((112, 18, 118, 34), "char"); c.rect((124, 12, 130, 34), "char"); c.rect((106, 28, 138, 34), "char")
    for x, y in ((114, 14), (116, 10), (119, 7), (126, 8), (129, 4), (133, 2)):
        c.rect((x, y, x + 3, y + 2), "char_l")
    c.rect((0, 34, W, 52), "char_l")                        # a sea you would not swim in
    for x, y in ((8, 38), (30, 44), (60, 40), (92, 46), (130, 41), (146, 47), (44, 49)):
        c.row(y, x, x + 9, "char")
    c.rect((0, 52, W, H), "cream_d"); c.row(52, 0, W, "hair")  # grey sand
    for x, y in ((14, 60), (52, 72), (88, 58), (120, 74), (150, 62), (70, 66)):
        c.px(x, y, "hair_d"); c.px(x + 1, y, "hair_d")
    # a beach umbrella, knocked over
    c.d.pieslice((14, 44, 56, 86), 200, 320, fill=C["scarf"])
    c.d.pieslice((14, 44, 56, 86), 224, 248, fill=C["white"])
    c.d.pieslice((14, 44, 56, 86), 272, 296, fill=C["white"])
    c.line([(35, 65), (62, 74)], "wood_d", w=2)
    # a fish that did not make it
    c.line([(84, 68), (100, 68)], "white")
    for x in range(87, 98, 3):
        c.line([(x, 65), (x, 71)], "white")
    c.poly([(100, 68), (105, 64), (105, 72)], "white"); c.ell((80, 65, 86, 71), "white"); c.px(82, 67, "line")
    # a leaking barrel
    c.rect((126, 56, 138, 72), "char"); c.row(60, 126, 138, "char_l"); c.row(68, 126, 138, "char_l")
    c.poly([(138, 70), (150, 72), (154, 76), (132, 76), (130, 72)], "green_l")
    c.rect((140, 73, 146, 74), "green")
    return c.save(SCENES / "environment.png", outline=False)


# ---- cover ------------------------------------------------------------------------------
GLYPHS = {
    "M": "10001 11011 10101 10101 10001 10001 10001", "I": "11111 00100 00100 00100 00100 00100 11111",
    "N": "10001 11001 10101 10101 10011 10001 10001", "S": "01111 10000 10000 01110 00001 00001 11110",
    "T": "11111 00100 00100 00100 00100 00100 00100", "R": "11110 10001 10001 11110 10100 10010 10001",
    "Y": "10001 10001 01010 00100 00100 00100 00100", "O": "01110 10001 10001 10001 10001 10001 01110",
    "F": "11111 10000 10000 11110 10000 10000 10000", "U": "10001 10001 10001 10001 10001 10001 01110",
    "A": "01110 10001 10001 11111 10001 10001 10001", "B": "11110 10001 10001 11110 10001 10001 11110",
    "L": "10000 10000 10000 10000 10000 10000 11111",
}


def write(c, text, y, scale, colour):
    """Centres a line of 5x7 capitals."""
    x = (c.w - (len(text) * 6 - 1) * scale) // 2
    for ch in text:
        if ch != " ":
            for gy, bits in enumerate(GLYPHS[ch].split()):
                for gx, bit in enumerate(bits):
                    if bit == "1":
                        c.rect((x + gx * scale, y + gy * scale, x + (gx + 1) * scale - 1, y + (gy + 1) * scale - 1), colour)
        x += 6 * scale


def cover():
    c = Canvas(315, 250)
    c.rect((0, 0, 315, 250), "cream")                       # office wall
    for y in range(0, 250, 2):                               # faint wallpaper stripe
        for x in range(y % 4, 315, 12):
            c.px(x, y, "cream_d")
    for dx, dy, colour in ((2, 2, "scarf"), (0, 0, "line")):  # title with a stamped shadow
        cc = Canvas(315, 250); write(cc, "MINISTRY OF", 16, 3, colour); write(cc, "SUSTAINABILITY", 45, 3, colour)
        c.img.alpha_composite(cc.img, (dx, dy))
    # window: sea, sun and the world's largest cruise ship
    c.rect((20, 84, 152, 180), "wood_d"); c.rect((24, 88, 148, 176), "sea_l")
    c.ell((36, 96, 56, 116), "gold_l"); c.ell((39, 99, 53, 113), "gold")
    c.rect((24, 140, 148, 176), "sea")
    for x, y in ((30, 148), (58, 156), (96, 150), (124, 162), (44, 168), (84, 170), (132, 146)):
        c.row(y, x, x + 8, "sea_l")
    c.poly([(66, 128), (144, 128), (138, 144), (72, 144)], "white")      # hull
    c.row(140, 70, 140, "navy"); c.row(141, 71, 139, "navy")
    c.rect((76, 116, 136, 128), "white"); c.rect((84, 106, 130, 116), "white")
    for y in (110, 120):
        for x in range(88 if y == 110 else 80, 128 if y == 110 else 134, 6):
            c.rect((x, y, x + 2, y + 2), "sea_d")
    for x in (94, 108, 122):
        c.rect((x, 96, x + 5, 106), "red"); c.rect((x, 96, x + 5, 98), "line")
    c.rect((84, 84, 88, 180), "wood_d")                     # window bar
    c.rect((16, 180, 156, 185), "wood"); c.row(185, 16, 156, "line")  # sill
    # desk
    c.rect((0, 196, 315, 250), "wood"); c.rect((0, 196, 315, 199), "gold_d"); c.row(200, 0, 315, "wood_d")
    for y in (212, 228, 240):
        for x in range((y * 7) % 40, 315, 64):
            c.row(y, x, x + 22, "wood_d")
    # a tower of paperwork
    for i in range(9):
        x = 26 + (i * 5) % 7 - 3
        c.rect((x, 190 - i * 4, x + 44, 193 - i * 4), "white"); c.row(193 - i * 4, x, x + 44, "cream_d")
    c.rect((30, 150, 70, 157), "scarf"); c.row(157, 30, 70, "scarf_d")   # a red folder on top
    # the memo of the day, stamped
    c.poly([(92, 206), (150, 202), (158, 232), (98, 238)], "white")
    c.line([(98, 238), (158, 232)], "cream_d"); c.line([(158, 232), (150, 202)], "cream_d")
    for i in range(4):
        c.line([(100 + i, 212 + i * 5), (132 + i, 210 + i * 5)], "hair_d")
    c.d.ellipse((132, 214, 152, 232), outline=C["scarf"], width=2); c.ell((139, 220, 145, 226), "scarf")
    # the sheep, who has an appointment: drawn on its own layer so it gets a dark outline
    desk, c = c, Canvas(315, 250)
    for box in ((196, 132, 296, 206), (188, 150, 220, 186), (272, 146, 304, 190), (206, 122, 246, 152), (240, 118, 286, 150)):
        c.ell(box, "white")
    for cx, cy in ((200, 150), (214, 134), (236, 126), (262, 124), (284, 134), (298, 152), (300, 174), (290, 192), (196, 174)):
        c.ell((cx - 9, cy - 9, cx + 9, cy + 9), "white")
    c.recolor("white", "cream", lambda x, y: x >= 180 and y >= 120 and (x + y >= 474 or y >= 192))
    c.ell((206, 140, 250, 192), "char"); c.ell((210, 144, 246, 188), "char_l")       # face
    c.poly([(204, 150), (190, 144), (196, 160)], "char"); c.poly([(252, 150), (266, 144), (260, 160)], "char")  # ears
    for cx, cy in ((216, 138), (228, 132), (240, 138)):                             # woolly fringe
        c.ell((cx - 8, cy - 8, cx + 8, cy + 8), "white")
    for ex in (217, 233):
        c.ell((ex, 156, ex + 8, 166), "white"); c.rect((ex + 3, 160, ex + 6, 164), "line")
    c.rect((225, 174, 231, 177), "blush"); c.line([(228, 177), (228, 181)], "line"); c.row(181, 224, 232, "line")
    c.rect((214, 196, 222, 204), "char"); c.rect((250, 196, 258, 204), "char")       # front hooves on the desk
    c.ell((204, 190, 232, 202), "white"); c.ell((240, 190, 268, 202), "white")
    c.outline()
    desk.rect((192, 203, 300, 206), "wood_d")                                        # its shadow
    desk.img.alpha_composite(c.img)
    c = desk
    img = c.save(SCENES / "cover_small.png", outline=False)
    (SCENES / "cover_small.png").unlink()
    img.resize((630, 500), Image.NEAREST).save(ROOT / "art" / "cover.png")
    return img


if __name__ == "__main__":
    scenes = [fired(), closed(), disaster()]
    sheet = Image.new("RGBA", (W * 4, H * 4 * 3), (0, 0, 0, 0))
    for i, im in enumerate(scenes):
        sheet.alpha_composite(im.resize((W * 4, H * 4), Image.NEAREST), (0, i * H * 4))
    sheet.save(ROOT / "art" / "scenes_preview.png")
    cover()
    print(f"{len(scenes)} scenes written to {SCENES.relative_to(ROOT)}, cover to art/cover.png")
