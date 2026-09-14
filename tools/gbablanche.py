#!/usr/bin/env python3
"""Blanche goes pale: the houses, fences, mailboxes and signs (T-55, vision.md 9.22).

    python3 tools/gbablanche.py            # preview to /tmp/blanche_pale.png
    python3 tools/gbablanche.py --write    # palettes, tiles, metatiles, the map

Blanche is the pre-colour town. CRYSTAL CLEAR's lab (T-53) keeps one line of
gold; everything built around it goes to whites, pale greys and faded roofs.
The ground, the trees, the flowers and the pond are T-56's, and are not touched.

WHAT THE HOUSES ARE DRAWN IN, measured:

  common row 2  roofs, fences, mailboxes, the two signs -- indices 1..7, 10..14
  common row 3  walls and windows                       -- indices 1..5, 7, 9..12
  Blanche row 8 the house doors, and their opening animation

Common rows are shared by about 180 maps, so they cannot be changed where they
are. Blanche's row 10 has been free since the lab moved into row 9, so:

  ROW 10 is pale row 2, index for index -- roof, fence, mailbox and sign blocks
  just point at it, and their tiles do not change.

  Row 3 shares row 2's seven greys exactly, but its indices 9..12 (a yellow and
  three window blues) collide with row 2's roof colours. So every tile drawn in
  row 3 is COPIED into new slots with those four moved: the blues to 8, 9 and
  15, which nothing in row 2 uses, and the yellow onto the roof cream at 10 --
  the two are a hair apart once paled. Copies, not edits: a tile another block
  draws is never repainted.

  ROW 8 is paled in place, so the doors and the door animation, which is drawn
  in row 8, stay one colour.

  THE SIGNS are block 2, a COMMON block used in eight other towns, so Blanche
  gets its own copy pointed at row 10 and its two cells are repointed; every
  other house, fence and mailbox block is Blanche's own and is changed in place.

PALE is desaturation toward the colour's own grey, then a lift toward white
that is gentler the darker the colour -- so a roof fades and an outline stays an
outline.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/blanche_pale.png"
WRITE = "--write" in sys.argv

ROW_PALE = 10
ROW3_MOVE = {9: 10, 10: 8, 11: 9, 12: 15}     # row 3's colliding indices, in row 10
SIGN_BLOCK = 2                                # common, used in eight other towns


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


def pale(rgb):
    r, g, b = rgb
    grey = 0.299 * r + 0.587 * g + 0.114 * b
    r, g, b = (v + (grey - v) * 0.55 for v in (r, g, b))
    lift = 0.42 if grey > 150 else 0.26 if grey > 100 else 0.12
    return tuple(max(0, min(255, round(v + (255 - v) * lift))) for v in (r, g, b))


def main():
    row2, row3 = read_pal(os.path.join(PD, "palettes/02.pal")), read_pal(os.path.join(PD, "palettes/03.pal"))
    row8_path, row10_path = os.path.join(SD, "palettes/08.pal"), os.path.join(SD, "palettes/10.pal")
    row8 = read_pal(row8_path)
    assert row2[1:8] == row3[1:8], "rows 2 and 3 no longer share their greys"

    layout = [l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l.get("name") == "PalletTown_Layout"][0]
    bd_path = os.path.join(GBA, layout["blockdata_filepath"]); bd = bytearray(open(bd_path, "rb").read())
    W, H = layout["width"], layout["height"]
    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    prim_attr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    per_attr = len(attrs) // (len(metas) // 16)
    pt, st = Image.open(os.path.join(PD, "tiles.png")), Image.open(os.path.join(SD, "tiles.png"))
    rules = open(RULES).read()
    num_tiles = int(re.search(r"secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles (\d+)", rules).group(1))

    def entries(m):
        return struct.unpack_from("<8H", prim if m < 640 else metas, (m if m < 640 else m - 640) * 16)

    cells = {}
    for y in range(H):
        for x in range(W):
            cells.setdefault(struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF, []).append((x, y))
    targets = sorted(m for m in cells if any(((t >> 12) & 0xF) in (2, 3) and t & 0x3FF for t in entries(m)))
    if WRITE and any(((t >> 12) & 0xF) == ROW_PALE for m in targets for t in entries(m)):
        raise SystemExit("  already pale: a Blanche house block already draws row %d" % ROW_PALE)

    # Row 3 tiles get copies with the colliding indices moved.
    copies, new_pixels = {}, []
    def tile_pixels(idx):
        img, i = (pt, idx) if idx < 640 else (st, idx - 640)
        x, y = (i % 16) * 8, (i // 16) * 8
        return list(img.crop((x, y, x + 8, y + 8)).getdata())
    def moved(idx):
        if idx not in copies:
            px = [ROW3_MOVE.get(v, v) for v in tile_pixels(idx)]
            copies[idx] = 640 + num_tiles + len(new_pixels)
            new_pixels.append(px)
        return copies[idx]

    new_entries = {}
    for m in targets:
        out = []
        for t in entries(m):
            p = (t >> 12) & 0xF
            if not t & 0x3FF or p not in (2, 3):
                out.append(t); continue
            idx = t & 0x3FF
            if p == 3:
                idx = moved(idx)
            out.append((t & 0x0C00) | idx | (ROW_PALE << 12))
        new_entries[m] = out

    total = num_tiles + len(new_pixels)
    assert total <= 384
    pale10 = [row2[0]] + [pale(c) for c in row2[1:8]] + [pale(row3[10]), pale(row3[11])] + [pale(c) for c in row2[10:15]] + [pale(row3[12])]
    # the yellow folded onto the roof cream: say how far apart they were
    print("  row 3's yellow %s and row 2's cream %s -> %s" % (pale(row3[9]), pale(row2[10]), pale10[10]))
    pale8 = [row8[0]] + [pale(c) for c in row8[1:]]
    print("  %d house/fence/sign blocks, %d row-3 tiles copied (slots %d..%d), -num_tiles %d"
          % (len(targets), len(new_pixels), num_tiles, total - 1, total))

    # Apply to working copies.
    grown = Image.new("P", (128, max(st.height, ((total + 15) // 16) * 8)))
    grown.putpalette(st.getpalette()); grown.paste(st, (0, 0)); gp = grown.load()
    for n, px in enumerate(new_pixels):
        slot = num_tiles + n
        for i, v in enumerate(px):
            gp[(slot % 16) * 8 + i % 8, (slot // 16) * 8 + i // 8] = v
    for m, out in new_entries.items():
        if m >= 640:
            struct.pack_into("<8H", metas, (m - 640) * 16, *out)
    sign_id = None
    if SIGN_BLOCK in new_entries:
        sign_id = 640 + len(metas) // 16
        metas += struct.pack("<8H", *new_entries[SIGN_BLOCK])
        attrs += prim_attr[SIGN_BLOCK * per_attr:(SIGN_BLOCK + 1) * per_attr]
        for x, y in cells[SIGN_BLOCK]:
            raw = struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
            struct.pack_into("<H", bd, (y * W + x) * 2, (raw & ~0x3FF) | sign_id)
        print("  the signs: common block %d copied to Blanche block %d at %s" % (SIGN_BLOCK, sign_id, cells[SIGN_BLOCK]))

    # Preview: before and after, side by side.
    def render(metas_now, tiles_now, pals_now, bd_now):
        img = Image.new("RGB", (W * 16, H * 16)); o = img.load()
        tp, tsl = pt.load(), tiles_now.load()
        for yy in range(H):
            for xx in range(W):
                m = struct.unpack_from("<H", bd_now, (yy * W + xx) * 2)[0] & 0x3FF
                e = struct.unpack_from("<8H", prim if m < 640 else metas_now, (m if m < 640 else m - 640) * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]; idx = t & 0x3FF; p = (t >> 12) & 0xF
                        src, i, hgt = (tp, idx, pt.height) if idx < 640 else (tsl, idx - 640, tiles_now.height)
                        for ty in range(8):
                            for tx in range(8):
                                sx = (i % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx)
                                sy = (i // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                                v = src[sx, sy] if sy < hgt else 0
                                if layer and v == 0:
                                    continue
                                o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pals_now[p][v]
        return img
    pals = {n: read_pal(os.path.join(PD if n < 7 else SD, "palettes/%02d.pal" % n)) for n in range(13)}
    before = render(open(os.path.join(SD, "metatiles.bin"), "rb").read(), st, pals, open(bd_path, "rb").read())
    pals_after = dict(pals); pals_after[ROW_PALE] = pale10; pals_after[8] = pale8
    after = render(metas, grown, pals_after, bd)
    sheet = Image.new("RGB", (W * 16 * 2 + 8, H * 16), (30, 30, 30))
    sheet.paste(before, (0, 0)); sheet.paste(after, (W * 16 + 8, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (before | after)" % PREVIEW)

    if WRITE:
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attrs)
        open(bd_path, "wb").write(bd)
        write_pal(row10_path, pale10)
        write_pal(row8_path, pale8)
        rules = re.sub(r"(secondary/pallet_town/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+",
                       lambda mm: mm.group(1) + str(total), rules)
        open(RULES, "w").write(rules)
        print("  written: palettes 08 and 10, tiles.png, metatiles.bin, attributes, PalletTown map.bin, -num_tiles %d" % total)


main()
