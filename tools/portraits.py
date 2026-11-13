"""The recurring characters as 64x64 pixel portraits, drawn by code.

Run:  python3 tools/portraits.py
Writes assets/portraits/<name>.png and art/portraits_preview.png (all of them, enlarged).
"""
from PIL import Image

from pixel import ASSETS, PAPER, ROOT, S, C, Canvas, PALE, TAN, BROWN

PORTRAITS = ASSETS / "portraits"


# ============================================================================
def grandma_rose():
    c = Canvas()
    s = PALE
    # cardigan, blouse
    c.ell((4, 45, 59, 92), "olive")
    c.recolor("olive", "olive_d", lambda x, y: x >= 47 or x + y >= 104)
    c.recolor("olive", "olive_l", lambda x, y: x <= 16 and y <= 56 and x + y <= 66)
    c.poly([(25, 45), (38, 45), (31, 58)], "cream")
    c.line([(25, 45), (31, 58)], "olive_d")
    c.line([(38, 45), (31, 58)], "olive_d")
    c.recolor("cream", "cream_d", lambda x, y: x >= 33)
    c.pts("cream", [(31, 60), (31, 63)])
    # forearm across the chest
    c.poly([(8, 57), (38, 59), (40, 63), (8, 63)], "olive")
    c.line([(8, 56), (38, 58)], "olive_d")
    c.line([(9, 58), (30, 59)], "olive_l")
    c.rect((37, 59, 39, 63), "cream")
    # headscarf
    c.ell((17, 8, 47, 46), "scarf")
    c.recolor("scarf", "scarf_d", lambda x, y: x >= 44 or y >= 41)
    c.arc((19, 10, 45, 44), 195, 262, "scarf_l")
    c.arc((20, 11, 44, 43), 205, 250, "scarf_l")
    # face
    c.ell((22, 15, 42, 42), "skin", outline="scarf_d")
    c.recolor("skin", "skin2", lambda x, y: x >= 38 or y >= 39)
    c.recolor("skin2", "skin3", lambda x, y: x >= 41)
    c.recolor("skin", "hair", lambda x, y: y <= 20)
    c.recolor("skin2", "hair_d", lambda x, y: y <= 20)
    for x, y in [(31, 16), (31, 17), (30, 18), (30, 19), (29, 20), (26, 20), (34, 20), (36, 19), (24, 19)]:
        if c.get(x, y) in (C["hair"], C["hair_d"]):
            c.px(x, y, "hair_d")
    c.row(21, 24, 39, "skin2")
    # eyebrows: left flat, right raised
    c.row(25, 25, 29, "hair_d")
    c.pts("hair_d", [(34, 23), (35, 22), (36, 22), (37, 22), (38, 23)])
    # eyes: left half closed, right wide
    c.row(27, 25, 29, "skin3")
    c.pts("white", [(26, 28), (29, 28)]); c.pts("line", [(27, 28), (28, 28)])
    c.row(26, 34, 38, "skin3")
    for yy in (27, 28):
        c.pts("white", [(34, yy), (37, yy)]); c.pts("line", [(35, yy), (36, yy)])
    c.row(30, 26, 28, "skin2"); c.row(30, 35, 37, "skin3")
    # nose, cheeks, smile lines, smirk
    c.col(32, 27, 32, "skin2")
    c.pts("skin3", [(31, 33), (32, 33)]); c.pts("skin2", [(33, 33), (30, 32)])
    c.pts("blush", [(25, 32), (26, 32), (25, 33), (26, 33), (37, 32), (38, 32), (37, 33), (38, 33)])
    c.pts("skin2", [(27, 35), (27, 36)]); c.pts("skin3", [(37, 35), (37, 34)])
    c.row(37, 29, 34, "scarf_d"); c.pts("scarf_d", [(35, 36), (36, 35)])
    c.row(38, 30, 33, "skin2")
    # knot and tails
    c.poly([(29, 46), (24, 55), (28, 56), (31, 49)], "scarf")
    c.poly([(34, 46), (39, 54), (36, 56), (32, 49)], "scarf_d")
    c.ell((28, 42, 35, 48), "scarf_l", outline="scarf_d")
    for x, y in [(22, 14), (27, 11), (34, 10), (40, 13), (44, 20), (19, 24), (45, 30), (19, 33), (44, 38), (22, 41)]:
        if c.get(x, y) in (C["scarf"], C["scarf_d"], C["scarf_l"]):
            c.px(x, y, "cream")
    # tea glass on a saucer
    gx = 44
    shape = {47: (0, 6), 48: (0, 6), 49: (0, 6), 50: (1, 5), 51: (1, 5), 52: (1, 5),
             53: (0, 6), 54: (0, 6), 55: (0, 6), 56: (0, 6), 57: (1, 5)}
    for y, (a, b) in shape.items():
        c.row(y, gx + a, gx + b, "tea")
        c.px(gx + a, y, "tea_l"); c.px(gx + b, y, "scarf_d")
    c.row(46, gx, gx + 6, "white"); c.row(47, gx + 1, gx + 5, "cream")
    c.pts("tea_l", [(gx + 2, 49), (gx + 2, 54), (gx + 2, 55)])
    c.row(58, gx - 2, gx + 8, "white"); c.row(59, gx - 1, gx + 7, "cream_d")
    c.ell((gx - 4, 59, gx + 7, 66), "skin")
    c.recolor("skin", "skin2", lambda x, y: y >= 60 and x >= gx + 4)
    for x in (gx - 1, gx + 2, gx + 5):
        c.col(x, 62, 63, "skin3")
    c.pts("skin", [(gx - 3, 57), (gx - 2, 57), (gx - 3, 58)]); c.px(gx - 4, 58, "skin2")
    steam = [(46, 43), (47, 42), (47, 41), (46, 40), (49, 44), (50, 43)]
    c.pts("white", steam); c.no_edge.update(steam)
    return c.save(PORTRAITS / "grandma_rose.png")


# ============================================================================
def edward_collins(worried=False):
    """Pleased with a rising poll by default; worried=True gives the falling poll."""
    c = Canvas()
    s = PALE
    # suit
    c.ell((3, 45, 60, 94), "navy")
    c.recolor("navy", "navy_d", lambda x, y: x >= 47 or x + y >= 106)
    c.recolor("navy", "navy_l", lambda x, y: x <= 15 and x + y <= 64)
    # shirt and tie
    c.poly([(25, 45), (39, 45), (32, 61)], "white")
    c.recolor("white", "cream", lambda x, y: x >= 35)
    c.poly([(31, 48), (33, 48), (34, 57), (32, 61), (30, 57)], "red")
    c.col(33, 50, 58, "red_d")
    c.rect((31, 46, 33, 48), "red_d")
    # lapels
    c.poly([(21, 47), (25, 45), (31, 61), (25, 56)], "navy_l")
    c.poly([(43, 47), (39, 45), (33, 61), (39, 56)], "navy")
    c.line([(25, 45), (31, 61)], "navy_d"); c.line([(39, 45), (33, 61)], "navy_d")
    c.line([(21, 47), (25, 56)], "navy_d"); c.line([(43, 47), (39, 56)], "navy_d")
    c.px(24, 52, "gold"); c.px(24, 53, "gold_d")  # lapel pin
    # neck, ears
    c.rect((27, 37, 37, 45), "skin2")
    c.row(41, 27, 37, "skin3"); c.row(42, 28, 36, "skin3")
    c.ell((18, 24, 23, 31), "skin2"); c.ell((41, 24, 46, 31), "skin3")
    # hair mass, head
    c.ell((20, 6, 44, 26), "hair")
    c.ell((21, 10, 43, 41), "skin")
    c.shade_face(s, 43, 41)
    c.recolor("skin", "hair", lambda x, y: y <= 15 or (y <= 20 and x <= 22))
    c.recolor("skin2", "hair", lambda x, y: y <= 15 or (y <= 20 and x >= 41))
    c.recolor("skin3", "hair", lambda x, y: y <= 20)
    c.recolor("hair", "hair_d", lambda x, y: x >= 39 or (x <= 21 and y >= 16))
    c.pts("hair_d", [(28, 7), (27, 8), (27, 9), (26, 10), (26, 11), (25, 12), (25, 13), (24, 14), (24, 15)])  # parting
    c.pts("white", [(30, 8), (31, 8), (32, 9), (33, 9), (34, 10), (30, 11), (31, 12)])  # shine
    c.row(16, 24, 38, "skin2")
    c.row(19, 27, 36, "skin2")  # forehead line
    # brows, eyes looking down at the chart
    if worried:
        c.pts("hair_d", [(25, 22), (26, 22), (27, 21), (28, 21), (29, 20), (39, 22), (38, 22), (37, 21), (36, 21), (35, 20)])
    else:
        c.row(22, 25, 29, "hair_d"); c.row(22, 35, 39, "hair_d")
    c.eye(25, 24, s, tall=2, pupil=(2, 3))
    c.eye(35, 24, s, tall=2, pupil=(2, 3))
    c.nose(32, 25, 30, s)
    if worried:
        # clenched teeth, corners down, a drop of sweat
        c.row(34, 28, 36, "skin3")
        c.row(35, 28, 36, "white"); c.row(36, 28, 36, "skin3")
        c.pts("cream_d", [(30, 35), (32, 35), (34, 35)])
        c.pts("line", [(27, 35), (37, 35)]); c.pts("skin3", [(26, 36), (38, 36), (26, 37), (38, 37)])
        c.pts("sea_l", [(38, 17), (38, 18), (39, 18), (38, 19), (39, 19), (39, 20)]); c.px(38, 18, "white")
    else:
        # campaign grin
        c.row(34, 26, 38, "white"); c.row(35, 26, 38, "white"); c.row(36, 27, 37, "white"); c.row(37, 29, 35, "white")
        c.row(33, 26, 38, "skin3")
        c.pts("line", [(25, 34), (39, 34), (25, 33), (39, 33)])
        c.pts("skin3", [(26, 36), (38, 36), (27, 37), (28, 37), (36, 37), (37, 37)]); c.row(38, 29, 35, "skin3")
        c.pts("cream_d", [(29, 36), (32, 36), (35, 36), (29, 35), (32, 35), (35, 35)])
        c.pts("skin2", [(24, 31), (24, 32), (40, 31), (40, 32)])
    # poll chart
    c.rect((42, 45, 58, 62), "white", outline="line")
    c.col(57, 46, 61, "cream_d")
    c.col(45, 48, 58, "hair_d"); c.row(58, 45, 55, "hair_d")
    if worried:
        line = [(46, 49), (47, 49), (48, 50), (49, 51), (50, 51), (51, 53), (52, 54), (53, 55), (54, 56), (55, 56)]
        c.pts("red", line); c.pts("red", [(x, y + 1) for x, y in line[:8]])
    else:
        line = [(46, 56), (47, 56), (48, 55), (49, 54), (50, 54), (51, 52), (52, 51), (53, 50), (54, 49), (55, 49)]
        c.pts("green", line); c.pts("green", [(x, y + 1) for x, y in line[:8]])
        c.pts("green_d", [(55, 48), (54, 48), (55, 50)])  # arrow head
    # hand
    c.ell((38, 58, 47, 66), "skin")
    c.pts("skin", [(42, 56), (43, 56), (44, 56), (42, 57), (43, 57), (44, 57), (45, 57)])
    c.pts("skin3", [(40, 62), (43, 62), (40, 63), (43, 63)])
    return c.save(PORTRAITS / ("edward_collins_worried.png" if worried else "edward_collins.png"))


# ============================================================================
def margaret_hale():
    c = Canvas()
    s = TAN
    # white linen jacket
    c.ell((4, 45, 59, 92), "white")
    c.recolor("white", "cream", lambda x, y: x >= 44 or x + y >= 102)
    c.recolor("cream", "cream_d", lambda x, y: x >= 53 or x + y >= 112)
    c.poly([(25, 45), (39, 45), (32, 59)], "sea")
    c.recolor("sea", "sea_d", lambda x, y: x >= 34)
    c.line([(25, 45), (31, 60)], "cream_d"); c.line([(39, 45), (33, 60)], "cream_d")
    c.line([(20, 48), (25, 56)], "cream_d"); c.line([(44, 48), (39, 56)], "cream_d")
    c.col(32, 60, 63, "cream_d")
    c.pts("gold", [(27, 47), (28, 48), (29, 49), (30, 50), (31, 51), (32, 51), (33, 51), (34, 50), (35, 49), (36, 48), (37, 47)])
    # neck
    c.rect((28, 38, 36, 46), "tan2"); c.row(41, 28, 36, "tan3"); c.row(42, 29, 35, "tan3")
    # bob
    c.ell((16, 4, 48, 42), "gold_l")
    c.recolor("gold_l", "gold", lambda x, y: x >= 43 or y >= 37)
    for sx in (19, 21, 45):
        c.col(sx, 22, 35, "gold")
    c.recolor("gold", "gold_d", lambda x, y: x >= 46)
    # face
    c.ell((22, 13, 42, 41), "tan")
    c.shade_face(s, 42, 41)
    sweep = lambda x, y: y <= 16 + (x - 22) // 4
    c.recolor("tan", "gold_l", sweep); c.recolor("tan2", "gold", sweep); c.recolor("tan3", "gold_d", sweep)
    c.pts("gold", [(24, 14), (26, 15), (28, 15), (30, 16), (32, 17), (34, 17), (36, 18), (25, 17), (29, 18)])
    for x in range(23, 42):  # shadow under the fringe
        y = 17 + (x - 22) // 4
        if c.get(x, y) in (C["tan"], C["tan2"]):
            c.px(x, y, "tan2" if c.get(x, y) == C["tan"] else "tan3")
    # sunglasses pushed up into the hair
    c.rect((22, 8, 30, 12), "char", outline="line")
    c.rect((34, 8, 42, 12), "char", outline="line")
    c.row(9, 31, 33, "line")
    c.pts("sea_l", [(24, 10), (25, 10), (24, 11), (36, 10), (37, 10), (36, 11)])
    # brows, eyes with liner
    c.pts("wood_d", [(25, 24), (26, 23), (27, 23), (28, 23), (29, 23), (35, 23), (36, 23), (37, 23), (38, 23), (39, 24)])
    for ex in (26, 35):
        c.row(25, ex - 1, ex + 3, "line")
        c.pts("white", [(ex, 26), (ex + 3, 26)]); c.pts("line", [(ex + 1, 26), (ex + 2, 26)])
    c.nose(32, 27, 31, s)
    # lipstick smile
    c.pts("red", [(27, 34), (37, 34), (28, 35), (29, 35), (35, 35), (36, 35)])
    c.row(35, 30, 34, "white")
    c.row(36, 29, 35, "red"); c.row(37, 31, 33, "red_d")
    c.pts("blush", [(25, 31), (26, 31), (38, 31), (39, 31)])
    c.pts("sea_l", [(21, 34), (21, 35), (43, 34), (43, 35)])  # earrings
    c.pts("sea", [(21, 36), (43, 36)])
    # ship brooch
    c.row(55, 41, 49, "navy"); c.row(56, 42, 48, "navy"); c.row(57, 43, 47, "navy_d")
    c.col(45, 48, 54, "gold_d")
    c.poly([(46, 49), (46, 53), (49, 53)], "sea")
    c.poly([(44, 50), (44, 53), (42, 53)], "sea_d")
    c.px(45, 47, "red"); c.px(46, 47, "red")
    return c.save(PORTRAITS / "margaret_hale.png")


# ============================================================================
def julian_frost():
    c = Canvas()
    s = PALE
    # black turtleneck
    c.ell((4, 46, 59, 92), "char")
    c.recolor("char", "line", lambda x, y: x >= 47 or x + y >= 106)
    c.recolor("char", "char_l", lambda x, y: x <= 15 and x + y <= 64)
    c.rect((26, 37, 38, 48), "char_l")
    for x in (28, 31, 34, 37):
        c.col(x, 39, 48, "char")
    c.recolor("char_l", "char", lambda x, y: x >= 35 and 37 <= y <= 48 and 26 <= x <= 38)
    # green scarf, the only green thing he owns
    c.poly([(21, 45), (29, 48), (35, 48), (43, 45), (45, 49), (37, 53), (29, 53), (19, 49)], "green")
    c.poly([(20, 49), (28, 52), (27, 62), (19, 61)], "green")
    c.recolor("green", "green_d", lambda x, y: x >= 37 or (y >= 54 and x >= 24) or y == 52)
    c.pts("green_l", [(22, 46), (23, 46), (24, 47), (25, 47), (26, 48), (21, 51), (21, 52), (21, 53), (21, 55), (21, 56)])
    c.pts("green_l", [(20, 63), (22, 63), (24, 63), (26, 63)])
    # leaf badge
    c.poly([(40, 61), (41, 55), (46, 52), (48, 53), (47, 58), (43, 62)], "green_l", outline="green_d")
    c.line([(41, 60), (46, 54)], "green_d")
    # ears, bald head
    c.ell((18, 23, 23, 30), "skin2"); c.ell((41, 23, 46, 30), "skin3")
    c.ell((21, 8, 43, 40), "skin")
    c.shade_face(s, 43, 40)
    c.pts("white", [(27, 11), (28, 10), (29, 10), (30, 10), (27, 12)])  # shine on the scalp
    c.pts("hair_d", [(21, 19), (21, 20), (21, 21), (22, 18), (22, 19), (43, 19), (43, 20), (43, 21), (42, 18)])
    # raised brows above the frames
    c.row(16, 24, 28, "char"); c.px(23, 17, "char")
    c.row(17, 36, 40, "char"); c.px(41, 18, "char")
    # oversized glasses
    c.ell((21, 19, 31, 29), "sea_l", outline="line")
    c.ell((33, 19, 43, 29), "sea_l", outline="line")
    c.ell((22, 20, 30, 28), "sea_l", outline="line")
    c.ell((34, 20, 42, 28), "sea_l", outline="line")
    c.row(22, 31, 33, "line"); c.row(23, 31, 33, "line")
    c.row(22, 18, 21, "line"); c.row(22, 43, 45, "line")
    c.pts("white", [(24, 22), (25, 21), (36, 22), (37, 21)])
    # half-closed eyes behind them
    c.row(24, 25, 28, "line"); c.pts("line", [(26, 25), (27, 25)])
    c.row(24, 36, 39, "line"); c.pts("line", [(37, 25), (38, 25)])
    c.nose(32, 27, 31, s)
    # smug mouth
    c.row(35, 29, 35, "skin3"); c.pts("skin3", [(36, 34), (37, 33)])
    c.row(36, 30, 34, "skin2")
    c.pts("skin2", [(27, 33), (27, 34)])
    return c.save(PORTRAITS / "julian_frost.png")


# ============================================================================
def lily_carter():
    c = Canvas()
    s = BROWN
    # yellow jacket
    c.ell((5, 46, 58, 92), "gold")
    c.recolor("gold", "gold_d", lambda x, y: x >= 47 or x + y >= 104)
    c.recolor("gold", "gold_l", lambda x, y: x <= 16 and x + y <= 66)
    c.poly([(25, 46), (39, 46), (32, 57)], "white")
    c.recolor("white", "cream", lambda x, y: x >= 34)
    c.line([(25, 46), (32, 57)], "gold_d"); c.line([(39, 46), (32, 57)], "gold_d")
    c.col(32, 57, 63, "gold_d")
    # badges
    c.ell((13, 53, 18, 58), "red", outline="red_d")
    c.ell((20, 57, 25, 62), "white", outline="hair_d"); c.pts("green", [(22, 59), (23, 59), (22, 60), (23, 60)])
    c.ell((11, 60, 15, 64), "sea", outline="sea_d")
    # neck
    c.rect((28, 38, 36, 46), "brown2"); c.row(41, 28, 36, "brown3"); c.row(42, 29, 35, "brown3")
    # chain and padlock
    chain = [(26, 46), (27, 47), (27, 48), (28, 49), (29, 50), (30, 51), (38, 46), (37, 47), (37, 48), (36, 49), (35, 50), (34, 51)]
    for i, p in enumerate(chain):
        c.px(p[0], p[1], "hair" if i % 2 == 0 else "hair_d")
    c.pts("hair_d", [(31, 51), (33, 51), (31, 52), (33, 52), (32, 50)])
    c.rect((30, 53, 34, 57), "hair", outline="line")
    c.px(32, 55, "line")
    # messy hair with a bun
    c.ell((27, 1, 38, 11), "bhair")
    c.ell((16, 7, 48, 40), "bhair")
    c.ell((15, 24, 23, 47), "bhair"); c.ell((42, 24, 49, 45), "bhair")
    c.recolor("bhair", "bhair_d", lambda x, y: x >= 43 or (y >= 40))
    c.pts("bhair", [(26, 3), (26, 2), (39, 3), (39, 2), (32, 0), (33, 0), (17, 13), (16, 14), (47, 12), (48, 13)])
    c.pts("bhair_d", [(30, 4), (31, 5), (33, 4), (35, 6), (28, 9), (36, 9), (22, 11), (24, 13), (40, 12)])
    # face
    c.ell((22, 14, 42, 41), "brown")
    c.shade_face(s, 42, 41)
    fringe = lambda x, y: y <= 18 + (1 if x % 3 == 0 else 0) + (2 if x <= 24 or x >= 40 else 0)
    c.recolor("brown", "bhair", fringe); c.recolor("brown2", "bhair_d", fringe); c.recolor("brown3", "bhair_d", fringe)
    c.pts("brown2", [(26, 20), (27, 20), (29, 20), (31, 20), (32, 20), (34, 20), (35, 20), (37, 20)])
    # determined brows, big eyes
    c.pts("bhair_d", [(25, 22), (26, 22), (27, 22), (28, 23), (29, 23), (39, 22), (38, 22), (37, 22), (36, 23), (35, 23)])
    for ex in (26, 35):
        for yy in (25, 26):
            c.pts("white", [(ex, yy), (ex + 3, yy)]); c.pts("line", [(ex + 1, yy), (ex + 2, yy)])
        c.px(ex + 1, 25, "white")
    c.nose(32, 27, 31, s)
    c.pts("brown3", [(26, 30), (28, 31), (36, 31), (38, 30)])  # freckles
    # mouth open, mid-chant
    c.rect((29, 34, 35, 37), "red_d")
    c.row(34, 30, 34, "white")
    c.row(37, 31, 33, "blush")
    c.pts("brown3", [(28, 34), (36, 34)])
    # megaphone
    c.ell((40, 56, 49, 65), "brown")
    c.poly([(41, 52), (44, 49), (56, 41), (60, 57), (46, 58)], "white", outline="line")
    c.recolor("white", "cream", lambda x, y: x >= 42 and y >= 53)
    c.recolor("cream", "cream_d", lambda x, y: x >= 42 and y >= 56)
    c.line([(56, 40), (60, 58)], "red", w=2); c.line([(58, 41), (61, 57)], "red_d")
    c.rect((38, 50, 41, 57), "red", outline="line")
    c.pts("brown", [(43, 57), (44, 57), (45, 57), (46, 58), (43, 58), (44, 58), (45, 58)])
    c.pts("brown3", [(42, 61), (45, 61), (42, 62), (45, 62)])
    return c.save(PORTRAITS / "lily_carter.png")


# ============================================================================
def walter_briggs():
    c = Canvas()
    s = TAN
    # shovel over the shoulder, behind the body
    c.line([(45, 62), (55, 22)], "wood", w=3)
    c.line([(47, 62), (57, 22)], "wood_d")
    c.poly([(50, 23), (59, 25), (62, 11), (57, 3), (50, 8)], "hair")
    c.recolor("hair", "hair_d", lambda x, y: x >= 57 or y >= 22)
    c.pts("white", [(52, 9), (52, 10), (53, 8), (52, 12), (52, 13)])
    # work shirt
    c.ell((0, 44, 63, 96), "cream")
    c.recolor("cream", "cream_d", lambda x, y: x >= 49 or x + y >= 108 or (x % 7 == 3 and y % 2 == 0) or y % 8 == 2)
    # open collar
    c.poly([(26, 44), (38, 44), (32, 51)], "tan2")
    c.line([(26, 44), (32, 51)], "wood_d"); c.line([(38, 44), (32, 51)], "wood_d")
    # dungarees
    c.rect((22, 53, 42, 63), "sea_d")
    c.poly([(22, 53), (26, 53), (23, 45), (19, 46)], "sea_d")
    c.poly([(38, 53), (42, 53), (45, 46), (41, 45)], "sea_d")
    c.recolor("sea_d", "navy", lambda x, y: x >= 39)
    c.recolor("sea_d", "sea", lambda x, y: x <= 23)
    c.pts("gold", [(24, 54), (40, 54)])
    c.rect((28, 57, 36, 63), "sea_d", outline="navy")
    # neck, ears
    c.rect((25, 37, 39, 45), "tan2"); c.row(42, 25, 39, "tan3"); c.row(43, 26, 38, "tan3")
    c.ell((15, 24, 21, 32), "tan2"); c.ell((43, 24, 49, 32), "tan3")
    # head
    c.ell((19, 11, 45, 43), "tan")
    c.shade_face(s, 45, 43)
    c.recolor("tan", "hair", lambda x, y: y <= 26 and x <= 20)
    c.recolor("tan3", "hair_d", lambda x, y: y <= 26)
    # flat cap
    c.ell((17, 3, 47, 20), "wood")
    c.recolor("wood", "wood_d", lambda x, y: x >= 40 or ((x + y) % 5 == 0 and y >= 6))
    c.ell((13, 15, 40, 21), "wood_d")
    c.row(15, 18, 38, "wood")
    c.px(32, 3, "wood_d")
    c.row(22, 21, 41, "tan2")
    # heavy brows, tired eyes
    c.row(24, 24, 29, "hair_d"); c.row(25, 24, 29, "hair_d"); c.px(30, 26, "hair_d")
    c.row(24, 35, 40, "hair_d"); c.row(25, 35, 40, "hair_d"); c.px(34, 26, "hair_d")
    c.pts("white", [(25, 27), (28, 27), (36, 27), (39, 27)]); c.pts("line", [(26, 27), (27, 27), (37, 27), (38, 27)])
    c.row(29, 25, 28, "tan2"); c.row(29, 36, 39, "tan3")
    # sunburnt nose and cheeks
    c.rect((30, 27, 34, 32), "tan2")
    c.pts("blush", [(31, 29), (32, 29), (33, 29), (31, 30), (32, 30), (33, 30), (32, 31)])
    c.pts("tan3", [(30, 32), (34, 32), (31, 33), (32, 33), (33, 33)])
    c.pts("blush", [(22, 30), (23, 30), (24, 30), (22, 31), (23, 31), (24, 31), (40, 30), (41, 30), (40, 31), (41, 31)])
    # moustache
    c.row(34, 26, 38, "hair"); c.row(35, 25, 39, "hair")
    c.row(36, 25, 30, "hair_d"); c.row(36, 34, 39, "hair_d")
    c.pts("hair_d", [(25, 37), (26, 37), (38, 37), (39, 37)])
    c.pts("white", [(28, 34), (29, 34), (35, 34)])
    c.row(38, 30, 34, "tan3")
    c.pts("tan2", [(27, 40), (29, 41), (31, 40), (33, 41), (35, 40), (37, 41)])  # stubble
    return c.save(PORTRAITS / "walter_briggs.png")


# ============================================================================
if __name__ == "__main__":
    cast = [edward_collins(), edward_collins(worried=True), margaret_hale(), julian_frost(),
            lily_carter(), grandma_rose(), walter_briggs()]
    Z, M, COLS = 5, 24, 4
    cell = S * Z
    rows = -(-len(cast) // COLS)
    sheet = Image.new("RGBA", (COLS * cell + (COLS + 1) * M, rows * (cell + M) + M), PAPER)
    for i, im in enumerate(cast):
        sheet.alpha_composite(im.resize((cell, cell), Image.NEAREST), (M + (i % COLS) * (cell + M), M + (i // COLS) * (cell + M)))
    sheet.save(ROOT / "art" / "portraits_preview.png")
    print(f"{len(cast)} portraits written to {PORTRAITS.relative_to(ROOT)}")
