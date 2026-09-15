#!/usr/bin/env python3
"""The CHECKPOINT inside: a rack of BOX slots, the restore arrow on the floor, and the heal (T-65, T-62; vision.md 9.23).

    python3 tools/gbacheckpoint.py            # preview to /tmp/checkpoint.png (before | after | mid-heal)
    python3 tools/gbacheckpoint.py --write    # the CHECKPOINT tileset, and the two heal sprites

THE MACHINE was a white capsule with six green lights and a red cross -- a
hospital. A CHECKPOINT restores a running process, so it is a steel rack: a cap
with a teal status strip, a dark bay of six slots exactly where the heal places
its six sprites, a column of green progress lights either side, a plain plinth
where the cross was. It is symmetric about the cell boundary it straddles, so its
left tiles are its right tiles flipped. The four blocks that draw it (682, 683,
690, 691) are re-pointed in place, so every CHECKPOINT changes at once and no map
is touched; the counter's edge and the PC terminal's shared tiles stay.

THE FLOOR carried a Poke Ball in shaded floor tiles. It carries the CHECKPOINT's
restore arrow now (tools/gbaemblems.py, T-62), three times size, in row 12's own
teals over the floor's own tile; the nine floor blocks are re-pointed in place.

THE HEAL keeps its code and its timing and changes its pictures. The glowing ball
is a BOX cartridge with a green light; the monitor that flickers on the wall is a
status panel whose three lights sweep and whose bar fills -- the flicker already
runs its frames 1, 2, 3, 2, 1, 0, which reads as a sweep. The Hall of Fame's
machine uses the same cartridge. The sprite palette's three reds, used only by
the ball, become greens.

Everything is drawn in palette indices, not colours: row 11 for the rack, row 12
for the floor, the glow palette for the sprites. New tiles go into slots no used
block will reference once these blocks are re-pointed.
"""
import importlib.util, json, os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
spec = importlib.util.spec_from_file_location("gbaemblems", os.path.join(ROOT, "tools", "gbaemblems.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
SD = os.path.join(GBA, "data/tilesets/secondary/pokemon_center")
PD = os.path.join(GBA, "data/tilesets/primary/building")
PICS = os.path.join(GBA, "graphics/field_effects/pics")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/checkpoint.png"
WRITE = "--write" in sys.argv
MAX_TILES = 384

RACK_ROW, FLOOR_ROW = 11, 12
FLOOR_TILE = 674 - 640                     # the plain floor square, row 12
# the rack's cells: (block, [(entry index, art x, art y)]) -- art is 32x32 over map pixels (80..111, 16..47)
RACK = [
    (682, [(4, 0, 0), (5, 8, 0), (6, 0, 8), (7, 8, 8)]),
    (683, [(4, 16, 0), (5, 24, 0), (6, 16, 8), (7, 24, 8)]),
    (690, [(4, 0, 16), (5, 8, 16), (2, 0, 24), (3, 8, 24)]),          # the lower half sits under the counter's edge (top 667)
    (691, [(4, 16, 16), (5, 24, 16), (2, 16, 24), (3, 24, 24)]),
]
# the floor emblem's cells: block -> (art x, art y) of its 16x16, over a 48x48
FLOOR = {649: (0, 0), 650: (16, 0), 651: (32, 0), 657: (0, 16), 658: (16, 16), 659: (32, 16), 665: (0, 32), 666: (16, 32), 667: (32, 32)}
LAYOUTS = ("LAYOUT_POKEMON_CENTER_1F", "LAYOUT_POKEMON_CENTER_2F", "LAYOUT_RS_POKEMON_CENTER_1F",
           "LAYOUT_INDIGO_PLATEAU_POKEMON_CENTER_1F", "LAYOUT_ONE_ISLAND_POKEMON_CENTER_1F", "LAYOUT_ONE_ISLAND_POKEMON_CENTER_2F")


# ---------------------------------------------------------------- the drawings, in palette indices
def rack():
    OUT, GREY, LIGHT, PALE, TEAL, TEALD, AMBER, GREEN, WHITE = 1, 2, 3, 4, 7, 8, 13, 14, 15
    g = [[0] * 32 for _ in range(32)]

    def rect(x0, y0, x1, y1, v):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                g[y][x] = v
    # the left half, then its mirror
    rect(2, 0, 15, 0, OUT)
    rect(1, 1, 15, 3, PALE); rect(3, 1, 15, 1, WHITE); rect(1, 1, 1, 27, OUT)   # the cap
    rect(2, 4, 15, 4, OUT)
    rect(2, 5, 15, 27, LIGHT); rect(2, 5, 2, 27, PALE); rect(3, 5, 3, 27, GREY) # the body, a lit edge and a shade
    rect(4, 5, 15, 6, TEALD); rect(5, 5, 8, 5, TEAL); rect(11, 5, 14, 5, TEAL)  # the status strip
    rect(4, 7, 7, 22, PALE)                                                      # the face beside the bay
    for y in (9, 14, 19):                                                        # progress lights
        rect(5, y, 6, y + 1, GREEN); g[y][5] = WHITE
    rect(8, 7, 15, 22, OUT)                                                      # the bay
    for y in (8, 12, 16, 20):                                                    # each slot's lit lip
        rect(9, y, 15, y, TEALD)
    rect(4, 23, 15, 26, PALE); rect(6, 24, 15, 24, TEAL); rect(4, 27, 15, 27, OUT)
    rect(0, 16, 1, 31, OUT)                                                      # the lower cell is solid to its edges
    rect(0, 28, 15, 31, GREY); rect(0, 28, 15, 28, LIGHT); rect(0, 31, 15, 31, OUT)   # the plinth
    rect(4, 29, 7, 30, OUT); rect(10, 29, 13, 30, OUT)                          # two vents
    g[24][4] = AMBER
    for y in range(32):
        for x in range(16):
            g[y][31 - x] = g[y][x]
    return g


def floor(tile):
    # an inlay in the floor's own colours, as vanilla's ball was: the darker tan for its outline, the palest cream for
    # its body -- a solid teal arrow at three times size read as a decal stuck on the floor rather than set into it
    OUTL, BODY = 8, 10
    roles = {"O": OUTL, "M": BODY, "L": BODY}
    em = E.emblem("CHECKPOINT", roles)
    g = [[tile[(y % 8) * 8 + x % 8] for x in range(48)] for y in range(48)]
    for y in range(16):
        for x in range(16):
            if em[y][x]:
                for dy in range(3):
                    for dx in range(3):
                        g[y * 3 + dy][x * 3 + dx] = em[y][x]
    return g


CARTRIDGE = ["........",
             ".999999.",
             ".9bbbb9.",
             ".9a66a9.",
             ".9aaaa9.",
             ".999999.",
             "........",
             "........"]


def monitor_frame(k):
    g = [[0] * 32 for _ in range(16)]

    def rect(x0, y0, x1, y1, v):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                g[y][x] = v
    rect(3, 1, 26, 13, 9); rect(4, 2, 25, 12, 4); rect(4, 2, 25, 2, 10)
    for n, x0 in enumerate((7, 13, 19)):
        lit = (n + 1) == k
        rect(x0, 5, x0 + 3, 8, 6 if lit else 5)
        if lit:
            g[5][x0] = 7
    rect(7, 10, 22, 11, 3)
    if k:
        rect(7, 10, 7 + (16 * k) // 3 - 1, 11, 15)
    return g


# ---------------------------------------------------------------- tiles
def hflip(t):
    return tuple(t[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(t):
    return tuple(t[(7 - i // 8) * 8 + i % 8] for i in range(64))


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def main():
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    meta = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    sheet = Image.open(os.path.join(SD, "tiles.png")); sp = sheet.load()
    rules = open(RULES).read()
    key = "$(TILESETGFXDIR)/secondary/pokemon_center/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
    at = rules.index(key) + len(key); num_tiles = int(rules[at:].split()[0])
    tile_px = lambda n: tuple(sp[(n % 16) * 8 + k % 8, (n // 16) * 8 + k // 8] % 16 for k in range(64))
    original = bytes(meta)

    # every entry this rewrites, with the 8x8 of indices it should draw and its row
    R = rack(); want = []
    for block, entries in RACK:
        for e, ax, ay in entries:
            want.append((block, e, tuple(R[ay + k // 8][ax + k % 8] for k in range(64)), RACK_ROW))
    F = floor(tile_px(FLOOR_TILE))
    for block, (ax, ay) in FLOOR.items():
        for q in range(4):
            x0, y0 = ax + (q % 2) * 8, ay + (q // 2) * 8
            want.append((block, q, tuple(F[y0 + k // 8][x0 + k % 8] for k in range(64)), FLOOR_ROW))
    rewritten = {(b, e) for b, e, _, _ in want}

    # tiles still referenced by every block the maps use, not counting the entries about to be rewritten
    used_blocks = set()
    for lid in LAYOUTS:
        d = open(os.path.join(GBA, layouts[lid]["blockdata_filepath"]), "rb").read()
        used_blocks |= {struct.unpack_from("<H", d, i * 2)[0] & 0x3FF for i in range(len(d) // 2)}
    taken = {0}
    for b in used_blocks:
        if b >= 640 and (b - 639) * 16 <= len(meta):
            for e, t in enumerate(struct.unpack_from("<8H", meta, (b - 640) * 16)):
                if (b, e) not in rewritten and (t & 0x3FF) >= 640:
                    taken.add((t & 0x3FF) - 640)
    existing = {}
    for n in sorted(taken):
        if n < num_tiles:
            existing.setdefault(tile_px(n), n)
    free = [n for n in range(MAX_TILES) if n not in taken]

    new, slots = {}, []
    placed = {}
    for block, e, px, row in want:
        ref = None
        if not any(px):
            ref = (0, 0)
        else:
            for flip, f in ((0, lambda t: t), (0x400, hflip), (0x800, vflip), (0xC00, lambda t: hflip(vflip(t)))):
                t = f(px)
                if t in existing:
                    ref = (640 + existing[t], flip); break
                if t in new:
                    ref = (640 + new[t], flip); break
            if ref is None:
                new[px] = free[len(new)]; ref = (640 + new[px], 0)
        n, flip = ref
        struct.pack_into("<H", meta, (block - 640) * 16 + e * 2, 0 if n == 0 else (n | flip | (row << 12)))
    print("  %d entries rewritten; %d new tiles (%d slots free)" % (len(want), len(new), len(free)))
    if len(new) > len(free):
        raise SystemExit("  does not fit")

    # the sheet as it will be
    total = max([num_tiles] + [s + 1 for s in new.values()])
    grown = Image.new("P", (128, max(sheet.height, ((total + 15) // 16) * 8))); grown.putpalette(sheet.getpalette()); grown.paste(sheet, (0, 0)); gp = grown.load()
    for px, s in new.items():
        for k, v in enumerate(px):
            gp[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] = v

    # the sprites
    glow = Image.open(os.path.join(PICS, "pokeball_glow.png")); gpal = glow.getpalette()
    for i, c in ((5, (0, 110, 90)), (6, (0, 230, 115)), (7, (170, 255, 210))):
        gpal[i * 3:i * 3 + 3] = list(c)
    new_glow = Image.new("P", glow.size); new_glow.putpalette(gpal)
    for y, row in enumerate(CARTRIDGE):
        for x, ch in enumerate(row):
            new_glow.putpixel((x, y), 0 if ch == "." else int(ch, 16))
    mon = Image.open(os.path.join(PICS, "pokemoncenter_monitor.png"))
    new_mon = Image.new("P", mon.size); new_mon.putpalette(mon.getpalette())
    for k in range(4):
        for y, row in enumerate(monitor_frame(k)):
            for x, v in enumerate(row):
                new_mon.putpixel((x, k * 16 + y), v)

    # preview: the lobby's back half, before | after | after with the heal on it
    ppals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % r)) for r in range(7)] + [read_pal(os.path.join(SD, "palettes/%02d.pal" % r)) for r in range(7, 13)]
    pmeta = open(os.path.join(PD, "metatiles.bin"), "rb").read(); ptiles = Image.open(os.path.join(PD, "tiles.png")).load()
    l = layouts["LAYOUT_POKEMON_CENTER_1F"]; W = l["width"]; bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()

    def render(mt, tiles):
        out = Image.new("RGB", (W * 16, 10 * 16)); o = out.load()
        for y in range(10):
            for x in range(W):
                m = struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF
                src, k = (pmeta, m) if m < 640 else (mt, m - 640)
                if (k + 1) * 16 > len(src):
                    continue
                ent = struct.unpack_from("<8H", src, k * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = ent[layer * 4 + q]; i = t & 0x3FF
                        for ty in range(8):
                            for tx in range(8):
                                sx = 7 - tx if t & 0x400 else tx; sy = 7 - ty if t & 0x800 else ty
                                v = ptiles[(i % 16) * 8 + sx, (i // 16) * 8 + sy] if i < 640 else tiles[((i - 640) % 16) * 8 + sx, ((i - 640) // 16) * 8 + sy]
                                v %= 16
                                if layer and v == 0:
                                    continue
                                o[x * 16 + (q % 2) * 8 + tx, y * 16 + (q // 2) * 8 + ty] = ppals[(t >> 12) & 15][v]
        return out
    before, after = render(original, sp), render(bytes(meta), gp)
    heal = after.copy(); hp = heal.load(); spal = [tuple(gpal[i * 3:i * 3 + 3]) for i in range(16)]
    for (ox, oy) in ((0, 0), (6, 0), (0, 4), (6, 4), (0, 8), (6, 8)):
        for y, row in enumerate(CARTRIDGE):
            for x, ch in enumerate(row):
                if ch != ".":
                    hp[89 + ox + x, 24 + oy + y] = spal[int(ch, 16)]
    for y, row in enumerate(monitor_frame(2)):
        for x, v in enumerate(row):
            if v:
                hp[112 + x, 8 + y] = spal[v]
    sheet_out = Image.new("RGB", (W * 16 * 3 + 16, 160), (30, 30, 30))
    for k, im in enumerate((before, after, heal)):
        sheet_out.paste(im, (k * (W * 16 + 8), 0))
    sheet_out.resize((sheet_out.width * 2, sheet_out.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after | mid-heal)" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(meta)
        if total != num_tiles:
            open(RULES, "w").write(rules[:at] + str(total) + rules[at + len(str(num_tiles)):])
        new_glow.save(os.path.join(PICS, "pokeball_glow.png"))
        new_mon.save(os.path.join(PICS, "pokemoncenter_monitor.png"))
        print("  written: the CHECKPOINT tileset (%d tiles), pokeball_glow.png, pokemoncenter_monitor.png" % total)


if __name__ == "__main__":
    main()
