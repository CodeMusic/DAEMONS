#!/usr/bin/env python3
"""seasonmock.py -- T-359's mock-ups: a real map in each season, by palette, before anything is built.

    python3 tools/seasonmock.py OUT.png [MAP] [x0 y0 w h]      (default CALLOW, ViridianCity, its south-west)

It writes a picture and nothing else, and has no write mode, because nothing in the game changes until the user
approves a look (vision.md 9.21, decided 2026-10-03: "the world shows the season, by palette, with no new sprites").

HOW IT DECIDES WHAT TO RECOLOUR. Every outdoor map draws its ground and trees from gTileset_General's palette 0, and
the slots fall apart cleanly (measured on CALLOW, Routes 1 and 2 and SLATE): 1-4 are only ever tree foliage (and
the dark two also draw a flower's stem), 8 and 12-15 are the grass, 9-11 a flower's petals. So a season is
one table of up to sixteen colours that replaces palette 0's as it loads -- 32 bytes a season -- and the map,
its tiles and its people are untouched. The edges of paths and ponds draw the same greens from other palettes, as
exact copies, so the season follows the COLOUR into them, not just the slot.

AND HOW IT JOINS WHAT IS THERE. The season is what the world IS, so it goes in first; T-317's faded print and the
watch's light then fall on it exactly as they fall on summer now. The faded print and the watch below are the
engine's own sums (fieldmap.c DaemonsClarityEntries, daemons_time.c DaemonsTintForWatch), done in five-bit colour,
so what the sheet shows at dusk or in a faded print is what the cartridge would draw.

SPRING'S FLOWERS. "More flowers where flowers already grow" cannot be a palette alone: the palette can only make
the flowers there brighter. The mock-up also shows the cheap way to have more -- a fixed scatter of the plain-grass
metatiles swapped for the flower metatile as the map loads (no new art; both walk the same), never under a person
or a sign. It is shown separately so the two halves can be judged apart.
"""
import colorsys, importlib.util, json, os, struct, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
_args = sys.argv[1:]
_spec = importlib.util.spec_from_file_location("gbacivic", os.path.join(ROOT, "tools/gbacivic.py"))
C = importlib.util.module_from_spec(_spec)
sys.argv = sys.argv[:1]
_spec.loader.exec_module(C)

TREES, GRASS, PETALS = (1, 2, 3, 4), (8, 12, 13, 14, 15), (9, 10, 11)
# 0x00D is labelled METATILE_General_Plain_Grass upstream and is the TALL grass (MB_TALL_GRASS): swapping it for a
# flower would take an encounter tile away. flower_scatter also reads every candidate's behaviour, so it cannot.
PLAIN_GRASS, FLOWER = (0x001, 0x008, 0x009, 0x010, 0x011), 0x004
WATCH = {"day": ((255, 0), (255, 0), (255, 0)), "dusk": ((250, 1), (200, 0), (160, 1)),
         "night": ((112, 1), (128, 2), (176, 4)), "dawn": ((232, 1), (226, 1), (240, 3))}
FADED = {"none": 0, "18%": 46, "40%": 102}

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
except OSError:
    FONT = ImageFont.load_default()


def to5(rgb):
    return tuple(min(31, max(0, round(c * 31 / 255))) for c in rgb)


def hsv(rgb):
    return colorsys.rgb_to_hsv(*(c / 255 for c in rgb))


def rgb(h, s, v):
    return tuple(round(c * 255) for c in colorsys.hsv_to_rgb(h % 1, max(0, min(1, s)), max(0, min(1, v))))


def lift(v, k):
    return v + (1 - v) * k


# --- the three seasons, as what each does to palette 0's slots (summer is the palette as drawn) ---------------------

def autumn(i, c):
    h, s, v = hsv(c)
    if i in TREES:      # the trees turn, light to dark: gold, amber, rust, a dark russet that keeps the outline
        hue, sat, val = {1: (46, .62, 1.00), 2: (31, .72, .98), 3: (16, .70, .88), 4: (8, .62, .80)}[i]
        return rgb(hue / 360, sat, v * val + .06)
    if i in GRASS:      # the grass dries a little toward straw; it does not turn
        return rgb((h * 360 - 22) / 360, s * .82, v * .98)
    return c


def winter(i, c):
    h, s, v = hsv(c)
    if i in TREES:      # cooled toward a blue-green and frosted toward white; the darkest keeps the shape
        return rgb(158 / 360, s * .32, lift(v, .55 if i < 4 else .28))
    if i in GRASS:      # silver frost
        return rgb(165 / 360, s * .22, lift(v, .62))
    if i in PETALS:     # the flowers are gone under it: their petals take the grass's own frost
        return winter(13, PAL0[13])
    return c


def spring(i, c):
    h, s, v = hsv(c)
    if i in TREES:      # fresher: a step toward yellow-green, a little brighter
        return rgb((h * 360 - 12) / 360, s * 1.08, lift(v, .10))
    if i in GRASS:
        return rgb((h * 360 - 10) / 360, s * 1.12, lift(v, .08))
    if i in PETALS:     # the flowers that are there, brighter
        return rgb(h, s * 1.12, lift(v, .12))
    return c


SEASONS = {"summer": None, "autumn": autumn, "winter": winter, "spring": spring}


def season_table(name):
    """Palette 0 in a season, in five-bit colour: the 16 entries the cartridge would carry."""
    f = SEASONS[name]
    return [to5(f(i, c) if f else c) for i, c in enumerate(PAL0)]


# --- the engine's sums, in five-bit colour --------------------------------------------------------------------------

def faded(c5, amount):
    if not amount:
        return c5
    r, g, b = c5
    grey = (r * 77 + g * 150 + b * 29) >> 8
    q = lambda x: x + int(((grey - x) * amount + 128) / 256)   # C division truncates toward zero
    return (q(r), q(g), q(b))


def watch(c5, w):
    t = WATCH[w]
    return tuple(min(31, (c * t[k][0] >> 8) + t[k][1]) for k, c in enumerate(c5))


def to8(c5):
    return tuple(c * 255 // 31 for c in c5)


# --- the map -------------------------------------------------------------------------------------------------------

def layout_of(mapname):
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    m = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % mapname)))
    return m, next(l for l in layouts if l.get("id") == m["layout"])


def flower_scatter(m, l, bd, share=0.12):
    """Plain grass swapped for the flower metatile: a fixed scatter (the same cells every spring), never a cell a
    person, sign, warp or trigger stands on, and only plain grass that walks as the flower does (MB_NORMAL). A path's
    edge is drawn in the path's own tiles, so a flower beside one is harmless."""
    W, H = l["width"], l["height"]
    taken = {(e["x"], e["y"]) for k in ("object_events", "warp_events", "coord_events", "bg_events") for e in m.get(k) or []}
    at = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
    attrs = open(os.path.join(C.tdir(l["primary_tileset"], "primary"), "metatile_attributes.bin"), "rb").read()
    normal = lambda mt: (struct.unpack_from("<I", attrs, mt * 4)[0] & 0x1FF) == 0      # MB_NORMAL, as the flower is
    out = bytearray(bd)
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if (x, y) in taken or at(x, y) not in PLAIN_GRASS or not normal(at(x, y)):
                continue
            if ((x * 73856093) ^ (y * 19349663)) % 1000 < share * 1000:
                v = struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
                struct.pack_into("<H", out, (y * W + x) * 2, (v & ~0x3FF) | FLOWER)
    return bytes(out)


def render(l, bd, pals):
    pd, sd = C.tdir(l["primary_tileset"], "primary"), C.tdir(l["secondary_tileset"], "secondary")
    prim = open(os.path.join(pd, "metatiles.bin"), "rb").read()
    meta = open(os.path.join(sd, "metatiles.bin"), "rb").read()
    pt, st = Image.open(os.path.join(pd, "tiles.png")), Image.open(os.path.join(sd, "tiles.png"))
    ptp, stp = pt.load(), st.load()
    W, H = l["width"], l["height"]
    img = Image.new("RGB", (W * 16, H * 16))
    o = img.load()
    for yy in range(H):
        for xx in range(W):
            m = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
            buf, k = (prim, m) if m < 640 else (meta, m - 640)
            if (k + 1) * 16 > len(buf):
                continue
            ee = struct.unpack_from("<8H", buf, k * 16)
            for layer in (0, 1):
                for q in range(4):
                    t = ee[layer * 4 + q]
                    i = t & 0x3FF
                    src, jj, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
                    for ty in range(8):
                        for tx in range(8):
                            sy = (jj // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                            v = src[(jj % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                            if layer and v == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
    return img


def palettes(l, season, fade="none", w="day"):
    pd, sd = C.tdir(l["primary_tileset"], "primary"), C.tdir(l["secondary_tileset"], "secondary")
    raw = [C.read_pal(os.path.join(pd, "palettes/%02d.pal" % n)) for n in range(7)] + \
          [C.read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
    # The edges of paths and ponds draw the grass from OTHER palettes, as exact copies of palette 0's greens (CALLOW's
    # rows 1 and 5 both carry the grass at index 15): the season follows the colour, not the slot, or winter leaves a
    # summer-green seam round every pond. Index 0 is never a colour.
    table = season_table(season)
    follow = {to5(PAL0[i]): table[i] for i in TREES + GRASS + PETALS}
    out = []
    for n, pal in enumerate(raw):
        five = table if n == 0 else [c if i == 0 else follow.get(c, c) for i, c in enumerate(to5(c) for c in pal)]
        out.append([to8(watch(faded(c, FADED[fade]), w)) for c in five])
    return out


PAL0 = None


def main():
    global PAL0
    if not _args:
        print(__doc__)
        return 1
    out = _args[0]
    mapname = _args[1] if len(_args) > 1 else "ViridianCity"
    m, l = layout_of(mapname)
    crop = tuple(int(a) for a in _args[2:6]) if len(_args) >= 6 else (5, 19, 43, 21)
    PAL0 = C.read_pal(os.path.join(C.tdir(l["primary_tileset"], "primary"), "palettes/00.pal"))
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    spring_bd = flower_scatter(m, l, bd)
    box = (crop[0] * 16, crop[1] * 16, (crop[0] + crop[2]) * 16, (crop[1] + crop[3]) * 16)
    panels = [("SUMMER -- as drawn now", bd, "summer", "none", "day"),
              ("SPRING -- palette only", bd, "spring", "none", "day"),
              ("SPRING -- and the flower scatter", spring_bd, "spring", "none", "day"),
              ("AUTUMN -- the trees turn", bd, "autumn", "none", "day"),
              ("WINTER -- frost; the flowers go under it", bd, "winter", "none", "day"),
              ("AUTUMN at DUSK -- the watch on top", bd, "autumn", "none", "dusk"),
              ("WINTER at NIGHT", bd, "winter", "none", "night"),
              ("AUTUMN in the 40% faded print (T-317)", bd, "autumn", "40%", "day")]
    pw, ph = box[2] - box[0], box[3] - box[1]
    sheet = Image.new("RGB", (pw * 2 + 30, (ph + 34) * 4 + 10), (246, 244, 238))
    d = ImageDraw.Draw(sheet)
    for n, (cap, b, s, f, w) in enumerate(panels):
        x, y = 10 + (n % 2) * (pw + 10), 10 + (n // 2) * (ph + 34)
        sheet.paste(render(l, b, palettes(l, s, f, w)).crop(box), (x, y + 22))
        d.text((x, y + 2), cap, fill=(25, 25, 25), font=FONT)
    sheet.save(out)
    print("  wrote %s (%s, %d x %d tiles from %d,%d)" % (out, mapname, crop[2], crop[3], crop[0], crop[1]))
    for s in ("spring", "autumn", "winter"):
        t = season_table(s)
        print("  %-6s palette 0: %s" % (s, " ".join("%04X" % (c[0] | c[1] << 5 | c[2] << 10) for c in t)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
