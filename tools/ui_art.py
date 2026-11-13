"""The interface art, drawn by code: seven 16x16 meter icons and the 64x64 ministry seal.

Run:  python3 tools/ui_art.py
Writes assets/ui/<name>.png and art/ui_preview.png (all of them, enlarged).
"""
import math
import random

from PIL import Image

from pixel import ASSETS, PAPER, ROOT, C, Canvas

UI = ASSETS / "ui"

# One letter per colour; "." is empty.
KEY = {
    "k": "line", "w": "white", "c": "cream_d",
    "g": "gold", "G": "gold_l", "d": "gold_d",
    "r": "red", "R": "blush", "D": "red_d",
    "l": "green", "L": "green_l", "v": "green_d",
    "n": "navy_l", "N": "navy",
    "s": "scarf", "S": "scarf_d",
    "b": "sea", "B": "sea_d", "o": "wood",
}

ICONS = {
    "budget": """
................
.....kkkkkk.....
...kkggggggkk...
..kgGGggggggdk..
..kgGggkkgggdk..
.kgGggkggkgggdk.
.kgGggkgggggddk.
.kgggggkkggggdk.
.kggggggggkgddk.
.kgggkgggkgdddk.
.kggggkkkggdddk.
..kggggggggddk..
..kdggggggdddk..
...kkddddddkk...
.....kkkkkk.....
................""",
    "approval": """
................
................
..kkkk....kkkk..
.krrrrk..krrrrk.
krRRrrrkkrrrrrDk
krRrrrrrrrrrrrDk
krrrrrrrrrrrrDDk
krrrrrrrrrrrrDDk
.krrrrrrrrrrDDk.
..krrrrrrrrDDk..
...krrrrrrDDk...
....krrrrDDk....
.....krrDDk.....
......krDk......
.......kk.......
................""",
    "environment": """
................
..........kkkkk.
.......kkklllLk.
.....kklllLLLlk.
....klllllLlllk.
...kllllLLllllk.
..kllllLlllllvk.
..klllLllllllvk.
..kllLlllllvvk..
..klLlllllvvk...
..kLllllvvvk....
.kvklvvvvkk.....
.kv.kkkkk.......
kvk.............
kk..............
................""",
    "political": """
................
.......kk.......
.....kknnkk.....
...kknnnnnnkk...
.kknnnnnnnnnnkk.
knnnnnnnnnnnnnNk
kkkkkkkkkkkkkkkk
.knNk.knNk.knNk.
.knNk.knNk.knNk.
.knNk.knNk.knNk.
.knNk.knNk.knNk.
.knNk.knNk.knNk.
kkkkkkkkkkkkkkkk
knnnnnnnnnnnnNNk
kkkkkkkkkkkkkkkk
................""",
    "tourism": """
................
.....kkkkkk.....
...kkbbwwbbkk...
..kbbbwwwwbbbk..
.kwbbbwwwwbbbwk.
.kwwbbwwwwbbwwk.
kwwwbbbwwbbbwwwk
kkkkkkkookkkkkkk
.......oo.......
.......oo.......
.......oo.......
.......oo.......
.......oo.......
...kkkkookkkk...
..kggggggggggk..
..kkkkkkkkkkkk..""",
    "agriculture": """
.......kk.......
......kggk......
.....kkggkk.....
....kgkggkgk....
....kggkkggk....
.....kkggkk.....
....kgkggkgk....
....kggkkggk....
.....kkggkk.....
....kgkddkgk....
....kggkkggk....
.....kkddkk.....
......kddk......
......kddk......
......kddk......
.......kk.......""",
    "fashion": """
................
................
..kkkk....kkkk..
.ksssskkkksssSk.
kssssskwwkssssSk
ksssssskksssssSk
kkksssssssssSkkk
..kssssssssssSk.
..kssssssssssSk.
..kssssssssssSk.
..kssssssssssSk.
..kssssssssssSk.
..kssssssssssSk.
..kssssssssSSSk.
..kkkkkkkkkkkkk.
................""",
}


def icon(name):
    rows = ICONS[name].strip("\n").split("\n")
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), (name, [len(r) for r in rows])
    c = Canvas(16, 16)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                c.px(x, y, KEY[ch])
    return c.save(UI / f"{name}.png", outline=False)


def seal():
    """A round rubber stamp: sun over an olive branch, in one worn colour."""
    c = Canvas(64, 64)
    ink = "scarf"
    for box in ((1, 1, 62, 62), (2, 2, 61, 61), (8, 8, 55, 55)):
        c.d.ellipse(box, outline=C[ink])
    # tick marks between the two rings, where a real seal would carry its lettering
    for i in range(24):
        a = math.radians(i * 15)
        for r in (26.5, 27.5, 28.5) if i % 2 == 0 else (27.5,):
            c.px(round(31.5 + r * math.cos(a)), round(31.5 + r * math.sin(a)), ink)
    # sun
    c.d.ellipse((26, 14, 37, 25), fill=C[ink])
    for i in range(8):
        a = math.radians(i * 45)
        for r in (8, 9, 10):
            c.px(round(31.5 + r * math.cos(a)), round(19.5 + r * math.sin(a)), ink)
    # olive branch: a curved stem with leaves alternating above and below it
    stem = [(15 + i, round(46 - 7 * math.sin(i / 33 * math.pi))) for i in range(34)]
    for x, y in stem:
        c.px(x, y, ink)
    for n, i in enumerate(range(3, 33, 5)):
        x, y = stem[i]
        if n % 2 == 0:
            c.d.ellipse((x - 1, y - 7, x + 1, y - 2), fill=C[ink])
        else:
            c.d.ellipse((x - 1, y + 2, x + 1, y + 7), fill=C[ink])
    # wear: a rubber stamp never prints every pixel
    rng = random.Random(7)
    for y in range(64):
        for x in range(64):
            if c.get(x, y)[3] and rng.random() < 0.07:
                c.img.putpixel((x, y), (0, 0, 0, 0))
    return c.save(UI / "seal.png", outline=False)


if __name__ == "__main__":
    icons = [icon(name) for name in ICONS]
    stamp = seal()
    Z, M = 8, 16
    sheet = Image.new("RGBA", (len(icons) * (16 * Z + M) + M + 64 * 4 + M, 64 * 4 + 2 * M), PAPER)
    for i, im in enumerate(icons):
        sheet.alpha_composite(im.resize((16 * Z, 16 * Z), Image.NEAREST), (M + i * (16 * Z + M), M))
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (M + i * (16 * Z + M), M + 16 * Z + M))
    sheet.alpha_composite(stamp.resize((256, 256), Image.NEAREST), (len(icons) * (16 * Z + M) + M, M))
    sheet.save(ROOT / "art" / "ui_preview.png")
    print(f"{len(icons)} icons and the seal written to {UI.relative_to(ROOT)}")
