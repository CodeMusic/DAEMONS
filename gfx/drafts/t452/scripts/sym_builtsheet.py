"""T-452 SYMBOL, as BUILT: every picture decoded from the engine's .4bpp tiles and .gbapal palettes (what the ROM is
built from), not from the PNGs: front, back, party icon, and the follower in its follower palette beside red_normal."""
import sys, os, re, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont
E = sys.argv[1]; OUT = sys.argv[2]
FORMS = [chr(c) for c in range(97, 123)] + ["exclamation_mark", "question_mark"]
CONST = {f: "UNOWN_" + f.upper() for f in FORMS}; CONST.update({"a": "UNOWN", "exclamation_mark": "UNOWN_EMARK", "question_mark": "UNOWN_QMARK"})
GLY = {f: f.upper() for f in FORMS}; GLY.update({"exclamation_mark": "!", "question_mark": "?"})
c15 = lambda v: ((v & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v >> 10 & 31) * 255 // 31)
def gbapal(p): d = open(p, "rb").read(); return [c15(struct.unpack("<H", d[i:i+2])[0]) for i in range(0, 32, 2)]
def tiles(p, w, h):
    d = open(p, "rb").read(); a = np.zeros((h, w), int); t = 0
    for ty in range(h // 8):
        for tx in range(w // 8):
            for y in range(8):
                for x in range(4):
                    b = d[t * 32 + y * 4 + x]; a[ty*8+y, tx*8+x*2] = b & 15; a[ty*8+y, tx*8+x*2+1] = b >> 4
            t += 1
    return a
def img(a, pal, bg):
    o = np.zeros(a.shape + (3,), np.uint8); o[:] = bg
    for i in range(1, 16): o[a == i] = pal[i]
    return Image.fromarray(o)
P = E + "/graphics/pokemon/unown"; npal = gbapal(P + "/normal.gbapal"); spal = gbapal(P + "/shiny.gbapal")
ipal = [gbapal(E + "/graphics/pokemon/icon_palettes/icon_palette_%d.gbapal" % i) for i in range(3)]
src = open(E + "/src/pokemon_icon.c").read().split("gMonIconPaletteIndices[] = {", 1)[1]
pidx = dict(re.findall(r"\[SPECIES_(\w+)\]\s*= (\d)", src))
fp = dict((k, [c15(int(v, 16)) for v in vs.split(", ")]) for k, vs in re.findall(r"\[SPECIES_(\w+)\] = \{([^}]*)\}", open(E + "/src/data/follower_palettes.h").read().split("sFollowerShiny")[0]))
red = Image.open(E + "/graphics/object_events/pics/people/red_normal.png"); rp = [tuple(red.getpalette()[i:i+3]) for i in range(0, 48, 3)]
ra = np.array(red)[:, :16]
coords = {}
for k in ("front", "back"):
    t = open(E + "/src/data/pokemon_graphics/%s_pic_coordinates.h" % k).read()
    for c, w, h, y in re.findall(r"\[SPECIES_(UNOWN\w*)\] =\s*\{\s*\.size = MON_COORDS_SIZE\((\d+), (\d+)\),\s*\.y_offset = (\d+)", t): coords[(k, c)] = (int(w), int(h), int(y))
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
GB, PT, GR = (205, 205, 172), (98, 156, 131), (120, 176, 96)
CW, RH, per = 128*2 + 64*2 + 40 + 64 + 30, 170, 4
s = Image.new("RGB", (20 + per * CW, 50 + 7 * RH), (236, 234, 226)); d = ImageDraw.Draw(s)
d.text((20, 10), "T-452 SYMBOL's 28 forms AS BUILT (decoded from the engine's .4bpp + .gbapal, branch tsym): front, back (2x), shiny front (1x), party icon (2x), follower beside red_normal (2x, its follower palette)", fill=(0,0,0), font=F)
for i, f in enumerate(FORMS):
    x = 20 + (i % per) * CW; y = 34 + (i // per) * RH; C = CONST[f]
    d.text((x, y), "%s %s  front %s back %s icon pal %s" % (GLY[f], C, coords[("front", C)], coords[("back", C)], pidx[C]), fill=(0,0,0), font=F)
    fr = img(tiles(P + "/%s/front.4bpp" % f, 64, 64), npal, GB); bk = img(tiles(P + "/%s/back.4bpp" % f, 64, 64), npal, GB)
    s.paste(fr.resize((128, 128), Image.NEAREST), (x, y + 18)); s.paste(bk.resize((128, 128), Image.NEAREST), (x + 132, y + 18))
    s.paste(img(tiles(P + "/%s/front.4bpp" % f, 64, 64), spal, GB), (x + 264, y + 18))
    ic = img(tiles(P + "/%s/icon.4bpp" % f, 32, 64)[:32], ipal[int(pidx[C])], PT); s.paste(ic.resize((64, 64), Image.NEAREST), (x + 264, y + 86))
    fo = tiles(P + "/%s/follower.4bpp" % f, 32, 32); g = np.zeros((32, 52, 3), np.uint8); g[:] = GR
    for j in range(1, 16): g[:, :32][fo == j] = fp[C][j]
    for j in range(1, 16): g[:, 34:50][ra == j] = rp[j]
    s.paste(Image.fromarray(g).resize((104, 64), Image.NEAREST), (x + 332, y + 18))
s.save(OUT); print(OUT, s.size)
