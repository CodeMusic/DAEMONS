#!/usr/bin/env python3
"""CALLOW SCHOOL from outside: a building of its seven floors (batch 7; docs/school.md 13).

    python3 tools/gbaschoolfront.py            # report, and a preview to /tmp/schoolfront.png
    python3 tools/gbaschoolfront.py --write    # Callow's tileset, its map, the school's own door and its frames

WHY IT LOOKS LIKE THIS. Inside, the school is seven floors of poured concrete on a survey grid, a switchback
stairwell and a lift with brass doors in every floor's right-hand window. Vanilla left it outside as a cottage
with a flower box, the same cottage as the house above it. So the outside is drawn from the inside, and a player
who has climbed it can read it from the street:

    THE STAIR TOWER, left   glazed, and through the glass the flights switch back floor by floor -- up at the
                            right on one floor, up at the left on the next -- the way the stairwell inside does
    SEVEN FLOORS, middle    the ground floor, then six bands of classroom windows, each with the dark of a
                            board at the back of the room
    THE LIFT, right         a concrete shaft with one narrow window a floor, brass behind the glass
    THE DOOR                glass doors under a brass canopy, and they SLIDE: the school has a door of its own,
                            with its own three frames, where the cottage's swung open

Nothing is written on it. The building is named by its floors, and by the sign.

WHERE IT GOES, measured rather than assumed. The cottage stood at (24..28, 15..18) with its planters on row 19.
The house above opens onto row 12, so the school may rise to row 13 and no further: five cells by six, 80x96. The
planters, the path to the door and row 12 are left exactly as they were. Every cell of the tower is blocked; the
lawn it rises over (rows 13..15) was walkable and is not now, and nothing is reached only through it.

HOW IT GOES IN, as tools/gbascholar.py put the Owl's study into Brazen: every cell gets a block of Callow's own,
appended; the drawing is the top layer over plain grass, on the COVERED layer, so a sprite standing in front of
the school is drawn in front of it. Colour comes from Callow's rows 7..12 and the General rows beneath them; row 7,
which Callow's blocks use only in indices 1..4, gives eleven spare indices to concrete, glass, brass and board.
The door cell is drawn in row 8 alone, because a door's frames are played in one palette row and must match it.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SD = os.path.join(GBA, "data/tilesets/secondary/viridian_city")
PD = os.path.join(GBA, "data/tilesets/primary/general")
DOOR_PNG = os.path.join(GBA, "graphics/door_anims/callow_school.png")
LABELS = os.path.join(GBA, "include/constants/metatile_labels.h")
PREVIEW = "/tmp/schoolfront.png"
WRITE = "--write" in sys.argv
MAX_TILES = MAX_BLOCKS = 384
LAYOUT = "LAYOUT_VIRIDIAN_CITY"
AT = (24, 13)                       # the tower's top-left cell
W_CELLS, H_CELLS = 5, 6
DOOR = (1, 5)                       # the door cell, within the tower: (25, 18), where the cottage's door was
OLD_DOOR = 0x299                    # METATILE_ViridianCity_Door
GRASS = 8                           # the plain lawn block whose bottom layer the tower stands on
HOUSE_ATTR_FROM = 645               # a cottage wall block: no behaviour, the COVERED layer
DOOR_ROW = 8

#  Row 7's spare indices, 5..15.
ROW7 = {5: (232, 228, 224), 6: (213, 205, 205), 7: (170, 164, 166), 8: (123, 123, 131), 9: (58, 56, 64),
        10: (96, 128, 170), 11: (150, 186, 214), 12: (60, 80, 112), 13: (200, 166, 72), 14: (140, 110, 48),
        15: (52, 78, 64)}
CONCL, CONC, CONCD, CONCDD, INK = ROW7[5], ROW7[6], ROW7[7], ROW7[8], ROW7[9]
GLASS, GLASSL, GLASSD, BRASS, BRASSD, BOARD = ROW7[10], ROW7[11], ROW7[12], ROW7[13], ROW7[14], ROW7[15]
ROWS = tuple(range(0, 13))

#  Row 8 as the door frames will draw it; index 0 is never used, because index 0 is transparent.
R8 = None


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


# ---------------------------------------------------------------- the drawing, 80x96, None where the ground shows
FLOOR_TOP = {7: 8, 6: 20, 5: 32, 4: 44, 3: 56, 2: 68}      # each upper floor a 12-pixel band; the ground floor 80..95


def draw():
    p = [[None] * 80 for _ in range(96)]

    def px(x, y, c):
        if 0 <= x < 80 and 0 <= y < 96:
            p[y][x] = c

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px(x, y, c)

    # ---- the main block, x 16..63: a parapet, then six floors of classroom windows
    rect(16, 4, 63, 95, CONC)
    rect(16, 4, 63, 4, CONCL); rect(16, 5, 63, 6, CONC); rect(16, 7, 63, 7, CONCDD)
    for f, top in FLOOR_TOP.items():
        rect(16, top, 63, top, CONCL)                               # the slab edge, lit from above
        rect(16, top + 1, 63, top + 1, CONCD)
        rect(16, top + 2, 63, top + 9, GLASS)                       # the window band
        rect(16, top + 2, 63, top + 2, GLASSD)                      # the head in shadow
        for x in range(16, 64, 8):                                  # a mullion on every tile edge
            rect(x, top + 2, x, top + 9, CONCDD)
        for x in range(18, 63, 8):                                  # the board at the back of each room
            rect(x + 1, top + 4, x + 4, top + 6, BOARD)
        for x in range(21, 63, 8):                                  # and the light across the glass
            px(x + 1, top + 3, GLASSL); px(x, top + 4, GLASSL)
        rect(16, top + 10, 63, top + 11, CONC)                      # the spandrel
    # ---- the ground floor: a brass canopy over the door, tall glass beyond it, a plinth
    rect(16, 80, 63, 81, CONCL)
    rect(34, 83, 61, 92, GLASS); rect(34, 83, 61, 83, GLASSD)
    for x in (34, 41, 48, 55, 61):
        rect(x, 83, x, 92, CONCDD)
    for x in (37, 44, 51, 58):
        px(x, 84, GLASSL); px(x - 1, 85, GLASSL)
    rect(16, 93, 63, 95, CONCD); rect(16, 93, 63, 93, CONCL)

    # ---- the stair tower, x 0..15, glazed, the flights switching back floor by floor
    rect(0, 0, 15, 95, CONC)
    rect(0, 0, 15, 0, CONCL); rect(0, 1, 15, 2, CONC); rect(0, 3, 15, 3, CONCDD)
    rect(3, 5, 12, 91, GLASS)
    rect(3, 5, 12, 5, GLASSD)
    for f, top in list(FLOOR_TOP.items()) + [(1, 80)]:
        rect(3, top, 12, top, CONCL); rect(3, top + 1, 12, top + 1, CONCD)   # the landing at each floor
        up_right = (f % 2 == 1)                                    # 1F up at the right, 2F up at the left ...
        for k in range(10):
            x = 3 + k if up_right else 12 - k
            y = top + 11 - k if f != 1 else top + 11 - k // 2
            if top + 2 <= y <= min(top + 11, 91):
                px(x, y, CONCD); px(x, y + 1, CONCDD)
    rect(2, 5, 2, 91, CONCDD); rect(13, 5, 13, 91, CONCDD)
    rect(0, 93, 15, 95, CONCD); rect(0, 93, 15, 93, CONCL)

    # ---- the lift shaft, x 64..79: its machine room on top, a narrow window a floor with brass behind it
    rect(64, 0, 79, 95, CONC)
    rect(64, 0, 79, 0, CONCL); rect(64, 1, 79, 2, CONC); rect(64, 3, 79, 3, CONCDD)
    for x in range(67, 77, 2):                                      # the machine room's louvre
        rect(x, 5, x, 7, CONCDD)
    for f, top in FLOOR_TOP.items():
        rect(64, top, 79, top, CONCL); rect(64, top + 1, 79, top + 1, CONCD)
        rect(68, top + 3, 75, top + 9, GLASSD)
        rect(69, top + 4, 71, top + 9, BRASS); rect(72, top + 4, 74, top + 9, BRASS)
        rect(71, top + 4, 72, top + 9, BRASSD)                      # the seam between the doors
    rect(68, 83, 75, 92, GLASSD)
    rect(69, 84, 71, 92, BRASS); rect(72, 84, 74, 92, BRASS); rect(71, 84, 72, 92, BRASSD)
    rect(64, 93, 79, 95, CONCD); rect(64, 93, 79, 93, CONCL)

    # ---- the outline, and the shadow where the towers stand proud of the block
    for x0, x1, y0 in ((0, 15, 0), (16, 63, 4), (64, 79, 0)):
        rect(x0, y0, x1, y0, INK)
    rect(0, 0, 0, 95, INK); rect(79, 0, 79, 95, INK)
    rect(16, 5, 16, 95, CONCDD); rect(63, 5, 63, 95, CONCDD)
    return p


# ---------------------------------------------------------------- the door: the static cell and three frames
def door_art(gap):
    """16x16 in row 8's own colours. GAP is how far each glass leaf has slid: 0 closed, 6 fully open."""
    dark, grey, blue, lblue, pale, gold, bgold, lgrey, slate = (R8[1], R8[2], R8[3], R8[4], R8[5], R8[7], R8[8],
                                                                R8[10], R8[11])
    c = [[lgrey] * 16 for _ in range(16)]

    def rect(x0, y0, x1, y1, col):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < 16 and 0 <= y < 16:
                    c[y][x] = col

    rect(0, 0, 15, 1, gold); rect(0, 2, 15, 2, R8[6])               # the canopy's brass edge, and its shadow
    rect(1, 3, 14, 15, slate)                                       # the frame
    rect(2, 4, 13, 15, dark)                                        # the dark of the hall behind
    rect(2, 12, 13, 15, grey)                                       # its lit floor
    for k in range(4):
        rect(5 - k, 12 + k, 10 + k, 12 + k, lgrey)
    lw = 6 - gap                                                    # each leaf's visible width
    if lw > 0:
        rect(2, 4, 1 + lw, 15, blue); rect(14 - lw, 4, 13, 15, blue)
        rect(2, 4, 1 + lw, 4, lblue); rect(14 - lw, 4, 13, 4, lblue)
        if lw > 2:
            c[6][3] = pale; c[7][2 + 1] = pale; c[6][14 - lw + 1] = pale
        rect(1 + lw, 8, 1 + lw, 10, bgold); rect(14 - lw, 8, 14 - lw, 10, bgold)   # the pull handles
    rect(0, 3, 0, 15, grey); rect(15, 3, 15, 15, grey)
    return c


# ---------------------------------------------------------------- tiles, blocks, the map
def hflip(t):
    return tuple(t[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(t):
    return tuple(t[(7 - i // 8) * 8 + i % 8] for i in range(64))


def nearest(c, pal):
    return min(range(1, 16), key=lambda k: sum((c[m] - pal[k][m]) ** 2 for m in range(3)))


def main():
    global R8
    layouts = {l.get("id"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("id")}
    meta = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attr = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    pmeta = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    sheet = Image.open(os.path.join(SD, "tiles.png")); sp = sheet.load()
    pals = {r: read_pal(os.path.join(PD, "palettes/%02d.pal" % r)) for r in range(7)}
    pals.update({r: read_pal(os.path.join(SD, "palettes/%02d.pal" % r)) for r in range(7, 13)})
    for k, c in ROW7.items():
        pals[7][k] = c
    R8 = pals[DOOR_ROW]

    l = layouts[LAYOUT]; W = l["width"]
    bd = bytearray(open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read())
    cell = lambda i, j: struct.unpack_from("<H", bd, ((AT[1] + j) * W + AT[0] + i) * 2)[0]
    if cell(*DOOR) & 0x3FF != OLD_DOOR:
        print("  the school at (%d,%d) is already drawn -- the door cell is block 0x%X" % (AT[0] + DOOR[0], AT[1] + DOOR[1], cell(*DOOR) & 0x3FF))
        return 0

    # which blocks every map on Callow's tileset still uses once the tower is in, and so which tiles are taken
    used = set()
    for lay in layouts.values():
        if lay.get("secondary_tileset") != "gTileset_ViridianCity":
            continue
        d = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read(); Wl = lay["width"]
        for n in range(len(d) // 2):
            x, y = n % Wl, n // Wl
            if lay["id"] == LAYOUT and 0 <= x - AT[0] < W_CELLS and 0 <= y - AT[1] < H_CELLS:
                continue
            used.add(struct.unpack_from("<H", d, n * 2)[0] & 0x3FF)
    used.add(OLD_DOOR)                                              # the house above keeps the cottage door
    taken = {0}
    for b in used:
        if b >= 640 and (b - 640 + 1) * 16 <= len(meta):
            taken |= {(t & 0x3FF) - 640 for t in struct.unpack_from("<8H", meta, (b - 640) * 16) if (t & 0x3FF) >= 640}
    free = [n for n in range(MAX_TILES) if n not in taken]

    art = draw()
    dart = door_art(0)
    for y in range(16):                                             # the door cell is the door's own drawing
        for x in range(16):
            art[DOOR[1] * 16 + y][DOOR[0] * 16 + x] = dart[y][x]

    existing = {}
    for n in taken:
        if n < (sheet.height // 8) * 16:
            existing.setdefault(tuple(sp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64)), n)
    new_tiles, cells, err_total = {}, {}, 0
    for j in range(H_CELLS):
        for i in range(W_CELLS):
            entries = []
            for q in range(4):
                x0, y0 = i * 16 + (q % 2) * 8, j * 16 + (q // 2) * 8
                pix = [art[y0 + k // 8][x0 + k % 8] for k in range(64)]
                if all(c is None for c in pix):
                    entries.append(0); continue
                best = None
                for r in ((DOOR_ROW,) if (i, j) == DOOR else ROWS):
                    idx, err = [], 0
                    for c in pix:
                        if c is None:
                            idx.append(0); continue
                        k = nearest(c, pals[r]); idx.append(k)
                        err += sum((c[m] - pals[r][k][m]) ** 2 for m in range(3))
                    if best is None or err < best[1]:
                        best = (r, err, tuple(idx))
                r, err, idx = best; err_total += err
                ref = None
                for flip, f in ((0, lambda t: t), (0x400, hflip), (0x800, vflip), (0xC00, lambda t: hflip(vflip(t)))):
                    t = f(idx)
                    if t in existing:
                        ref = ("old", existing[t], flip); break
                    if t in new_tiles:
                        ref = ("new", new_tiles[t], flip); break
                if ref is None:
                    new_tiles[idx] = len(new_tiles); ref = ("new", new_tiles[idx], 0)
                entries.append((ref, r))
            cells[(i, j)] = entries
    print("  %d cells: %d new tiles (%d slots free), mean squared error per pixel %.1f"
          % (W_CELLS * H_CELLS, len(new_tiles), len(free), err_total / (W_CELLS * H_CELLS * 256)))
    if len(new_tiles) > len(free):
        raise SystemExit("  does not fit")
    slot = {n: free[k] for k, n in enumerate(sorted(new_tiles.values()))}

    # the blocks: plain lawn beneath, the school on top; the door keeps the door's behaviour
    nblocks = len(meta) // 16
    grass = list(struct.unpack_from("<8H", pmeta, GRASS * 16))[:4]
    wall_attr = bytes(attr[(HOUSE_ATTR_FROM - 640) * 4:(HOUSE_ATTR_FROM - 640) * 4 + 4])
    door_attr = bytes(attr[(OLD_DOOR - 640) * 4:(OLD_DOOR - 640) * 4 + 4])
    made, block_of = {}, {}
    for (i, j), entries in cells.items():
        e = grass + [0, 0, 0, 0]
        for q, ent in enumerate(entries):
            if ent != 0:
                (kind, n, flip), r = ent
                e[4 + q] = (640 + (n if kind == "old" else slot[n])) | flip | (r << 12)
        key = (tuple(e), door_attr if (i, j) == DOOR else wall_attr)
        if key not in made:
            made[key] = 640 + nblocks + len(made)
        block_of[(i, j)] = made[key]
    print("  %d new blocks (%d of %d used); the school's door is block 0x%X" % (len(made), nblocks + len(made), MAX_BLOCKS, block_of[DOOR]))
    if nblocks + len(made) > MAX_BLOCKS:
        raise SystemExit("  too many blocks")

    # the door's three frames: sliding, sliding, open
    frames = [door_art(g) for g in (2, 4, 6)]

    # preview: the drawing | as the game's rows will show it | the door's frames
    out = Image.new("RGB", (80 * 2 + 8 + 16 * 3 + 12, 96), (40, 40, 40)); o = out.load()
    inv = {v: k for k, v in new_tiles.items()}
    for (i, j), entries in cells.items():
        for q, ent in enumerate(entries):
            x0, y0 = i * 16 + (q % 2) * 8, j * 16 + (q // 2) * 8
            for k in range(64):
                c = art[y0 + k // 8][x0 + k % 8]
                o[x0 + k % 8, y0 + k // 8] = c if c else (124, 192, 104)
                v = 0
                if ent != 0:
                    (kind, n, flip), r = ent
                    tile = inv[n] if kind == "new" else next(t for t, m in existing.items() if m == n)
                    for f, fn in ((0x400, hflip), (0x800, vflip)):
                        if flip & f:
                            tile = fn(tile)
                    v = tile[k]
                o[88 + x0 + k % 8, y0 + k // 8] = pals[ent[1]][v] if ent and v else (124, 192, 104)
    for n, fr in enumerate(frames):
        for y in range(16):
            for x in range(16):
                o[172 + n * 18 + x, 80 + y] = fr[y][x]
    out.resize((out.width * 4, out.height * 4), Image.NEAREST).save(PREVIEW)
    print("  preview %s" % PREVIEW)

    if not WRITE:
        return 0
    rows = max(sheet.height // 8, (max(slot.values(), default=0) // 16) + 1)
    grown = Image.new("P", (128, rows * 8)); grown.putpalette(sheet.getpalette()); grown.paste(sheet, (0, 0)); gp = grown.load()
    for tile, n in new_tiles.items():
        s = slot[n]
        for k, v in enumerate(tile):
            gp[(s % 16) * 8 + k % 8, (s // 16) * 8 + k // 8] = v
    grown.save(os.path.join(SD, "tiles.png"))
    for (e, a), b in sorted(made.items(), key=lambda t: t[1]):
        meta += struct.pack("<8H", *e); attr += a
    open(os.path.join(SD, "metatiles.bin"), "wb").write(meta)
    open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attr)
    write_pal(os.path.join(SD, "palettes/07.pal"), pals[7])
    for (i, j), b in block_of.items():
        n = ((AT[1] + j) * W + AT[0] + i) * 2
        raw = struct.unpack_from("<H", bd, n)[0]
        if (i, j) == DOOR:
            struct.pack_into("<H", bd, n, (raw & ~0x3FF) | b)                # the door keeps its own bits
        else:
            struct.pack_into("<H", bd, n, b | (1 << 10))                     # blocked, at elevation 0
    open(os.path.join(GBA, l["blockdata_filepath"]), "wb").write(bd)
    rules = os.path.join(GBA, "tileset_rules.mk"); text = open(rules).read()
    key = "$(TILESETGFXDIR)/secondary/viridian_city/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
    if key in text:
        at = text.index(key) + len(key); old = text[at:].split()[0]
        text = text[:at] + str(rows * 16) + text[at + len(old):]
        open(rules, "w").write(text)
    # the door's frames, indexed in row 8's own order, and its label
    img = Image.new("P", (16, 48))
    flat = []
    for c in R8:
        flat += list(c)
    img.putpalette(flat + [0] * (768 - len(flat)))
    for n, fr in enumerate(frames):
        for y in range(16):
            for x in range(16):
                img.putpixel((x, n * 16 + y), R8.index(fr[y][x]))
    img.save(DOOR_PNG)
    lab = open(LABELS).read()
    line = "#define METATILE_ViridianCity_SchoolDoor  0x%X\n" % block_of[DOOR]
    if "METATILE_ViridianCity_SchoolDoor" in lab:
        lab = re.sub(r"#define METATILE_ViridianCity_SchoolDoor\s+0x[0-9A-F]+\n", line, lab)
    else:
        lab = lab.replace("#define METATILE_ViridianCity_Door  0x299\n", "#define METATILE_ViridianCity_Door  0x299\n" + line)
    open(LABELS, "w").write(lab)
    print("  written: tiles.png (%d rows), %d blocks appended, palette row 7, the map, the door's frames and label" % (rows, len(made)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
