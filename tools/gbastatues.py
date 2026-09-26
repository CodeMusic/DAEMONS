#!/usr/bin/env python3
"""The BENCHMARK statues carry their MARKS (vision.md 5.2, 9.23).

    python3 tools/gbastatues.py            # preview to /tmp/statues.png (vanilla | ours, over each BENCHMARK's floor)
    python3 tools/gbastatues.py --write    # the eight shared Building tiles, and a top of its own in each BENCHMARK

EVERY BENCHMARK had vanilla's statue by its door -- a figure on a plinth with a grey
plaque -- drawn by eight Building tiles (256, 257, 272, 273 for the figure, 288,
289, 304, 305 for the plinth) in row 0 on each tileset's top layer. The same
eight tiles stand statues in 51 other interiors (Pokemon Tower, the Trainer Tower,
ordinary buildings), so they are redrawn once as a neutral monument: a stepped
stone plinth with a gold plaque, a plain stone orb on it.

IN A BENCHMARK THE FIGURE IS ITS MARK. The plaque already reads as a record --
LEADER, then WINNING USERS -- so what stands on it is the instrument that record
certifies (5.2): the slate, the hillside, the receptor, the fitted line, the skewed
peak, the brackets, the thermometer, the plumb bob. Each is the trainer card's
own 16x16 icon, cast in row 0's golds on a stone cap, on tiles of the BENCHMARK's
own tileset; the statue's top block there is re-pointed to them. Its plinth, its
collision and its script are the shared ones.
"""
import json, os, re, struct, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driftguard import refuse_over_later_work

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/building")
BADGES = os.path.join(GBA, "graphics/trainer_card/badges.png")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/statues.png"
WRITE = "--write" in sys.argv
TOP, BASE = (256, 257, 272, 273), (288, 289, 304, 305)
MARKS = ["SLATE", "SLOPE", "SENSE", "FIT", "SKEW", "FRAME", "HEAT", "TRUE"]
# BENCHMARK map -> (its tileset directory, its MARK, a statue cell for the preview)
GYMS = {"PewterCity_Gym": ("pewter_gym", "SLATE", (4, 12)), "CeruleanCity_Gym": ("cerulean_gym", "SLOPE", (6, 17)),
        "VermilionCity_Gym": ("vermilion_gym", "SENSE", (3, 17)), "CeladonCity_Gym": ("celadon_gym", "FIT", (4, 16)),
        "FuchsiaCity_Gym": ("fuchsia_gym", "SKEW", (4, 19)), "SaffronCity_Gym": ("saffron_gym", "FRAME", (12, 20)),
        "CinnabarIsland_Gym": ("cinnabar_gym", "HEAT", (23, 20)), "ViridianCity_Gym": ("viridian_gym", "TRUE", (15, 20))}
OUT, GREY, LIGHT, WHITE, GOLDD, GOLD, GOLDL, PALE, STONE = 1, 2, 3, 4, 5, 6, 7, 10, 15


def grid(w, h):
    return [[0] * w for _ in range(h)]


def rect(g, x0, y0, x1, y1, v):
    for y in range(max(0, y0), min(len(g), y1 + 1)):
        for x in range(max(0, x0), min(len(g[0]), x1 + 1)):
            g[y][x] = v


def plinth():
    """16x16, row 0: a stepped stone plinth, its gold plaque"""
    g = grid(16, 16)
    rect(g, 2, 0, 13, 13, OUT)
    rect(g, 3, 1, 12, 12, LIGHT); rect(g, 3, 1, 12, 1, PALE); rect(g, 12, 2, 12, 12, GREY); rect(g, 3, 2, 3, 12, PALE)
    rect(g, 4, 3, 11, 8, GOLDD); rect(g, 5, 4, 10, 7, GOLD); rect(g, 5, 4, 10, 4, GOLDL)          # the plaque
    rect(g, 6, 5, 9, 5, GOLDD); rect(g, 6, 6, 8, 6, GOLDD)                                        # two lines cut in it
    rect(g, 1, 13, 14, 15, OUT); rect(g, 2, 13, 13, 14, STONE); rect(g, 2, 13, 13, 13, LIGHT)     # the step
    return g


def cap(g):
    """the stone cap at the foot of the top cell, which the plinth's top meets"""
    rect(g, 2, 12, 13, 15, OUT); rect(g, 3, 12, 12, 14, LIGHT); rect(g, 3, 12, 12, 12, PALE); rect(g, 3, 15, 12, 15, GREY)


def neutral_top():
    """16x16, row 0: a plain stone orb on the cap -- the monument outside the BENCHMARKS"""
    g = grid(16, 16)
    cap(g)
    for y in range(1, 12):
        for x in range(3, 13):
            d = ((x + 0.5 - 8) / 5) ** 2 + ((y + 0.5 - 6.5) / 5.2) ** 2
            if d <= 1:
                g[y][x] = OUT if d > 0.78 else (PALE if (x < 7 and y < 6) else LIGHT if x < 10 else GREY)
    return g


def mark_top(icon):
    """16x16, row 0: the MARK's icon in gold on the cap. The card's roles: f outline, 4 body, 1 highlight, 3 a mark"""
    g = grid(16, 16)
    # every colour of the icon is gold -- SENSE and FRAME are drawn wholly in the card's outline colour, and in the
    # outline's ink they came out as dark silhouettes -- and a line of ink is traced round the whole shape instead
    roles = {0xF: GOLDD, 4: GOLD, 1: GOLDL, 3: GOLDD}
    # shrink the icon's 16 rows into the 12 above the cap by dropping its emptiest rows
    rows = [r for r in icon if any(r)]
    while len(rows) > 12:
        k = min(range(len(rows)), key=lambda i: sum(1 for v in rows[i] if v))
        rows.pop(k)
    top = 12 - len(rows)
    for y, r in enumerate(rows):
        for x, v in enumerate(r):
            if v:
                g[top + y][x] = roles.get(v, GOLDD)
    shape = {(x, y) for y in range(16) for x in range(16) if g[y][x]}
    for (x, y) in shape:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 16 and 0 <= ny < 12 and (nx, ny) not in shape:
                g[ny][nx] = OUT
    cap(g)
    return g


def tiles_of(g16):
    """the four 8x8 quadrants of a 16x16, in TL TR BL BR order"""
    return [tuple(g16[(q // 2) * 8 + i // 8][(q % 2) * 8 + i % 8] for i in range(64)) for q in range(4)]


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    refuse_over_later_work("gbastatues")          # T-293: its files carry later work; generator_drift.json says what
    badges = Image.open(BADGES).load()
    icons = {name: [[badges[k * 16 + x, y] for x in range(16)] for y in range(16)] for k, name in enumerate(MARKS)}
    row0 = read_pal(os.path.join(PD, "palettes/00.pal"))
    layouts = {l["id"]: l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "id" in l}
    rules = open(RULES).read()

    # the shared tiles
    ptiles = Image.open(os.path.join(PD, "tiles.png")); pp = ptiles.load()
    before = {n: tuple(pp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64)) for n in TOP + BASE}
    shared = dict(zip(TOP, tiles_of(neutral_top()))); shared.update(zip(BASE, tiles_of(plinth())))

    # per BENCHMARK: the blocks whose top layer draws the shared figure, and where its own four tiles go
    plans = []
    for mp, (sec, mark, cell) in GYMS.items():
        d = os.path.join(GBA, "data/tilesets/secondary", sec)
        meta = bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read())
        key = "$(TILESETGFXDIR)/secondary/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % sec
        at = rules.index(key) + len(key); n = int(rules[at:].split()[0])
        referenced = {(struct.unpack_from("<H", meta, i * 2)[0] & 0x3FF) - 640 for i in range(len(meta) // 2)}
        own = tiles_of(mark_top(icons[mark]))
        slots, s = [], n
        for t in own:
            slots.append(s); s += 1
        blocks = []
        for b in range(len(meta) // 16):
            e = struct.unpack_from("<8H", meta, b * 16)
            if any((e[4 + q] & 0x3FF) == TOP[q] and ((e[4 + q] >> 12) & 15) == 0 for q in range(4)):
                blocks.append(640 + b)
                for q in range(4):
                    if (e[4 + q] & 0x3FF) in TOP:
                        struct.pack_into("<H", meta, b * 16 + (4 + q) * 2, (640 + slots[TOP.index(e[4 + q] & 0x3FF)]) | (0 << 12))
        plans.append((mp, sec, mark, cell, d, meta, key, at, n, own, slots, blocks))
        print("  %-18s %-6s statue top blocks %s -> tiles %s" % (mp, mark, blocks, slots))

    # preview: each BENCHMARK's statue as it is and as it will be, over that BENCHMARK's own floor
    sheet = Image.new("RGB", (len(plans) * 44 + 8, 76), (30, 30, 30))
    for k, (mp, sec, mark, cell, d, meta, key, at, n, own, slots, blocks) in enumerate(plans):
        l = layouts[json.load(open(os.path.join(GBA, "data/maps", mp, "map.json")))["layout"]]
        floor_rgb = (200, 200, 200)
        for side, (top_px, base_px) in enumerate(((tiles_of_old(before, TOP), tiles_of_old(before, BASE)), (own, [shared[t] for t in BASE]))):
            ox, oy = 4 + k * 44 + side * 20, 6 + (0 if side == 0 else 0)
            for q in range(4):
                for part, px, dy in ((0, top_px[q], 0), (1, base_px[q], 16)):
                    for i, v in enumerate(px):
                        x, y = ox + (q % 2) * 8 + i % 8, oy + dy + (q // 2) * 8 + i // 8
                        sheet.putpixel((x, y), row0[v] if v else (110, 150, 120))
        for i, ch in enumerate(mark[:5]):
            pass
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(PREVIEW)
    print("  preview %s (each BENCHMARK: vanilla | ours)" % PREVIEW)

    if WRITE:
        for t, px in shared.items():
            for i, v in enumerate(px):
                pp[(t % 16) * 8 + i % 8, (t // 16) * 8 + i // 8] = v
        ptiles.save(os.path.join(PD, "tiles.png"))
        for mp, sec, mark, cell, d, meta, key, at, n, own, slots, blocks in plans:
            img = Image.open(os.path.join(d, "tiles.png"))
            total = max(slots) + 1
            grown = Image.new("P", (128, max(img.height, ((total + 15) // 16) * 8))); grown.putpalette(img.getpalette()); grown.paste(img, (0, 0)); gp = grown.load()
            for px, s in zip(own, slots):
                for i, v in enumerate(px):
                    gp[(s % 16) * 8 + i % 8, (s // 16) * 8 + i // 8] = v
            grown.save(os.path.join(d, "tiles.png"))
            open(os.path.join(d, "metatiles.bin"), "wb").write(meta)
            text = open(RULES).read(); at2 = text.index(key) + len(key); old_n = text[at2:].split()[0]
            open(RULES, "w").write(text[:at2] + str(total) + text[at2 + len(old_n):])
        print("  written: Building tiles %s and %s; a MARK on each BENCHMARK's statue" % (TOP, BASE))


def tiles_of_old(before, ids):
    return [before[t] for t in ids]


if __name__ == "__main__":
    main()
