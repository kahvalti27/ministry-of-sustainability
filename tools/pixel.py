"""Pixel drawing helpers shared by the scripts that draw the game's art."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
PAPER = (239, 230, 208, 255)
S = 64

PAL = {
    "line": (43, 29, 42),
    "white": (250, 247, 238), "cream": (244, 230, 200), "cream_d": (206, 186, 150),
    # skin: pale, tanned, brown (light, mid, shadow)
    "skin": (236, 190, 158), "skin2": (212, 156, 124), "skin3": (170, 112, 92),
    "tan": (220, 156, 112), "tan2": (188, 120, 84), "tan3": (142, 84, 64),
    "brown": (180, 120, 84), "brown2": (148, 92, 64), "brown3": (108, 64, 50),
    "blush": (222, 134, 116),
    # hair and metal
    "hair": (214, 214, 222), "hair_d": (156, 156, 172),
    "bhair": (96, 60, 52), "bhair_d": (66, 42, 42),
    # cloth
    "scarf": (196, 86, 58), "scarf_d": (142, 56, 44), "scarf_l": (228, 126, 86),
    "olive": (108, 124, 60), "olive_d": (72, 88, 44), "olive_l": (144, 160, 82),
    "navy": (48, 62, 102), "navy_d": (32, 42, 74), "navy_l": (72, 90, 136),
    "red": (204, 56, 56), "red_d": (150, 38, 46),
    "gold": (232, 180, 60), "gold_d": (188, 134, 40), "gold_l": (248, 216, 116),
    "sea": (64, 140, 170), "sea_d": (44, 100, 130), "sea_l": (128, 196, 214),
    "char": (62, 56, 72), "char_l": (92, 86, 104),
    "green": (86, 170, 84), "green_d": (48, 120, 64), "green_l": (146, 208, 112),
    "wood": (152, 102, 62), "wood_d": (110, 70, 48),
    "tea": (178, 62, 30), "tea_l": (224, 118, 48),
}
C = {k: v + (255,) for k, v in PAL.items()}


class Canvas:
    def __init__(self, w=S, h=S):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self.no_edge = set()  # pixels that do not get an outline (steam)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((x, y), C[c])

    def pts(self, c, points):
        for x, y in points:
            self.px(x, y, c)

    def get(self, x, y):
        return self.img.getpixel((x, y))

    def row(self, y, x0, x1, c):
        for x in range(x0, x1 + 1):
            self.px(x, y, c)

    def col(self, x, y0, y1, c):
        for y in range(y0, y1 + 1):
            self.px(x, y, c)

    def ell(self, box, c, outline=None):
        self.d.ellipse(box, fill=C[c], outline=C[outline] if outline else None)

    def poly(self, points, c, outline=None):
        self.d.polygon(points, fill=C[c], outline=C[outline] if outline else None)

    def rect(self, box, c, outline=None):
        self.d.rectangle(box, fill=C[c], outline=C[outline] if outline else None)

    def line(self, points, c, w=1):
        self.d.line(points, fill=C[c], width=w)

    def arc(self, box, a0, a1, c):
        self.d.arc(box, start=a0, end=a1, fill=C[c])

    def recolor(self, src, dst, pred):
        for y in range(self.h):
            for x in range(self.w):
                if self.get(x, y) == C[src] and pred(x, y):
                    self.px(x, y, dst)

    def shade_face(self, s, right, bottom):
        """Light from the top left: darken the right edge and the chin."""
        self.recolor(s[0], s[1], lambda x, y: x >= right - 4 or y >= bottom - 3)
        self.recolor(s[1], s[2], lambda x, y: x >= right - 1)

    def eye(self, x, y, s, tall=1, pupil=(1, 2)):
        """4 pixels wide: white, pupil, pupil, white, with a lid above."""
        self.row(y - 1, x, x + 3, s[2])
        for yy in range(y, y + tall):
            self.row(yy, x, x + 3, "white")
        for p in pupil:
            self.px(x + p, y + tall - 1, "line")
            if tall > 1 and pupil == (1, 2):
                self.px(x + p, y, "line")

    def nose(self, x, y0, y1, s):
        self.col(x, y0, y1, s[1])
        self.pts(s[2], [(x - 1, y1 + 1), (x, y1 + 1)])
        self.px(x + 1, y1 + 1, s[1])

    def outline(self):
        edge = []
        for y in range(self.h):
            for x in range(self.w):
                if self.get(x, y)[3]:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and self.get(nx, ny)[3] and (nx, ny) not in self.no_edge:
                        edge.append((x, y))
                        break
        self.pts("line", edge)

    def save(self, path, outline=True):
        if outline:
            self.outline()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.img.save(path)
        return self.img


PALE = ("skin", "skin2", "skin3")
TAN = ("tan", "tan2", "tan3")
BROWN = ("brown", "brown2", "brown3")
