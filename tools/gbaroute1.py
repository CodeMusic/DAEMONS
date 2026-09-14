#!/usr/bin/env python3
"""Route 1 without seams (T-72, T-73; vision.md 9.22).

    python3 tools/gbaroute1.py            # preview to /tmp/route1_seams.png (now | after)
    python3 tools/gbaroute1.py --write    # Route 1's map and border, Blanche's tiles, blocks and row 10

PLAYTEST, 2026-09-14. Three things read as seams:

  THE BIRCHES DOWN BOTH SIDES stood beside coloured grass for thirty rows, and
  the two on the top row drew as Callow's buildings from inside Callow -- a
  connection draws the neighbour's cells with THIS map's tileset (gbaseams.py),
  and a birch is one of Blanche's blocks. So the trees follow the grass: every
  tree above row 30 is vanilla's again (the world's broadleaf, a primary block),
  and so is the border. Birches stay only in the pale stretch.

  THE SAND PATH WAS CUT IN HALF where the pale stretch began, gold on its top
  row and chalk on its bottom one. A path is one colour the whole way: the chalk
  path now runs up out of Blanche, along the band at rows 29..30 and up the strip
  at x 18..21, as far as the ledge you jump down at row 26 -- through coloured
  grass, so its edges are coloured grass too.

  THE GRASS changed colour along a straight row. Now it changes at a ledge: the
  pale stretch's first ledge, row 31, is coloured above its lip and pale below,
  and the crossing at row 26 is gold above its lip and chalk below. The lip is
  the line, so no colour meets another on open ground.

HOW. The chalk path over coloured grass is vanilla's own path tiles, index for
index, pointed at four unused slots of Blanche's row 10: vanilla's sand 10 ->
chalk, 11 and 12 -> chalk edge, and 13 and 15 -> vanilla's own two greens. So
the path keeps every curve vanilla drew and costs nine tiles. The ledge rows
are split by quadrant: the top two from the coloured block, the bottom two from
the pale one, so the lip -- which vanilla draws entirely in the bottom half --
belongs to the pale side.
"""
import json, os, struct, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
SD = os.path.join(GBA, "data/tilesets/secondary/pallet_town")
RULES = os.path.join(GBA, "tileset_rules.mk")
PREVIEW = "/tmp/route1_seams.png"
WRITE = "--write" in sys.argv
VANILLA = "78917336e^"                  # the commit before Blanche's roads were drawn

W, H = 24, 40
PALE_FROM = 30                          # the pale stretch's first row
TREE_COLUMNS = (0, 1, 22, 23)
CHALK_CELLS = [(x, y) for y in (29, 30) for x in range(2, 22)] + [(x, y) for y in (27, 28) for x in range(18, 22)]
LEDGE_ROW = 31                          # coloured above the lip, pale below
CROSSING = [(x, 26) for x in range(18, 22)]   # gold above the lip, chalk below

PATH_ROW = 5
ROW = 10
# vanilla row 5 index -> a slot of row 10, and the colour that slot takes
SLOTS = {10: 8, 11: 9, 12: 9, 13: 10, 15: 11}
CHALK, CHALK_EDGE = (238, 238, 230), (218, 218, 208)       # Blanche's path, row 7 indices 5 and 7


def read_pal(path):
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, cols):
    open(path, "w").write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols))


def git_bytes(path):
    return subprocess.run(["git", "-C", GBA, "show", "%s:%s" % (VANILLA, path)], capture_output=True, check=True).stdout


def main():
    layouts = {l.get("name"): l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]}
    lay = layouts["Route1_Layout"]
    bd_path, border_path = os.path.join(GBA, lay["blockdata_filepath"]), os.path.join(GBA, lay["border_filepath"])
    old_bd = open(bd_path, "rb").read(); bd = bytearray(old_bd)
    van = git_bytes(lay["blockdata_filepath"]); van_border = git_bytes(lay["border_filepath"])
    get = lambda data, x, y: struct.unpack_from("<H", data, (y * W + x) * 2)[0]
    put = lambda x, y, m: struct.pack_into("<H", bd, (y * W + x) * 2, (get(bd, x, y) & ~0x3FF) | m)

    prim = open(os.path.join(PD, "metatiles.bin"), "rb").read()
    pattr = open(os.path.join(PD, "metatile_attributes.bin"), "rb").read()
    metas = bytearray(open(os.path.join(SD, "metatiles.bin"), "rb").read())
    attrs = bytearray(open(os.path.join(SD, "metatile_attributes.bin"), "rb").read())
    old_metas = bytes(metas)
    entries = lambda m: list(struct.unpack_from("<8H", prim if m < 640 else metas, (m if m < 640 else m - 640) * 16))
    attr = lambda m: bytes(pattr[m * 4:(m + 1) * 4]) if m < 640 else bytes(attrs[(m - 640) * 4:(m - 639) * 4])

    if get(bd, 0, 0) & 0x3FF == get(van, 0, 0) & 0x3FF and any(get(bd, x, 29) & 0x3FF >= 640 for x in range(2, 22)):
        print("  Route 1 is already drawn this way"); return

    # ---- 1. every tree above the pale stretch is vanilla's, and the border
    trees = 0
    for y in range(PALE_FROM):
        for x in range(W):
            now, was = get(bd, x, y) & 0x3FF, get(van, x, y) & 0x3FF
            if now >= 640 and was < 640 and (x in TREE_COLUMNS or y < 2):
                put(x, y, was); trees += 1

    # ---- 2. chalk tiles from vanilla's path tiles
    pt = Image.open(os.path.join(PD, "tiles.png")); ptp = pt.load()
    st = Image.open(os.path.join(SD, "tiles.png")); stp = st.load()
    rule_key = "secondary/pallet_town/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles "
    rules = open(RULES).read(); at = rules.index(rule_key) + len(rule_key)
    num_tiles = int(rules[at:].split()[0])
    have = {bytes(stp[(n % 16) * 8 + i % 8, (n // 16) * 8 + i // 8] for i in range(64)): n for n in range(num_tiles)}
    new_tiles = []
    def chalk_tile(t):
        """a row-5 path tile, the same pixels in row 10's slots; flips kept."""
        i = t & 0x3FF
        px = [ptp[(i % 16) * 8 + k % 8, (i // 16) * 8 + k // 8] for k in range(64)]
        assert set(px) <= set(SLOTS), "tile %d uses row 5 indices %s" % (i, sorted(set(px) - set(SLOTS)))
        key = bytes(SLOTS[v] for v in px)
        if key not in have:
            have[key] = num_tiles + len(new_tiles); new_tiles.append(key)
        return (640 + have[key]) | (t & 0x0C00) | (ROW << 12)
    def chalk(e, quads=range(4)):
        out = list(e)
        for q in quads:
            if (e[q] >> 12) & 0xF == PATH_ROW and e[q] & 0x3FF:
                out[q] = chalk_tile(e[q])
        return out

    ids, copies = {}, 0
    def block(e, a):
        nonlocal copies
        key = (tuple(e), a)
        if key not in ids:
            found = next((640 + k for k in range(len(metas) // 16)
                          if tuple(struct.unpack_from("<8H", metas, k * 16)) == key[0] and attrs[k * 4:(k + 1) * 4] == a), None)
            if found is None:
                found = 640 + len(metas) // 16
                metas.extend(struct.pack("<8H", *e)); attrs.extend(a); copies += 1
            ids[key] = found
        return ids[key]

    for x, y in CHALK_CELLS:
        v = get(van, x, y) & 0x3FF
        assert v < 640 and (prim[v * 16 + 1] >> 4) == PATH_ROW, "(%d,%d) was not a vanilla path cell" % (x, y)
        put(x, y, block(chalk(entries(v)), attr(v)))
    for x, y in CROSSING:
        m = get(bd, x, y) & 0x3FF
        assert m < 640, "(%d,%d) is not vanilla's crossing" % (x, y)
        put(x, y, block(chalk(entries(m), quads=(2, 3)), attr(m)))
    for x in range(W):
        pale, was = get(bd, x, LEDGE_ROW) & 0x3FF, get(van, x, LEDGE_ROW) & 0x3FF
        if pale < 640 or x in TREE_COLUMNS:
            continue
        ce, pe = chalk(entries(was), quads=(0, 1)), entries(pale)
        e = [ce[0], ce[1], pe[2], pe[3], pe[4], pe[5], pe[6], pe[7]]
        put(x, LEDGE_ROW, block(e, attr(pale)))

    # ---- 3. row 10's four slots
    row10 = read_pal(os.path.join(SD, "palettes/%02d.pal" % ROW)); row5 = read_pal(os.path.join(PD, "palettes/%02d.pal" % PATH_ROW))
    want = {8: CHALK, 9: CHALK_EDGE, 10: row5[13], 11: row5[15]}
    for k in range(len(old_metas) // 16):
        for t in struct.unpack_from("<8H", old_metas, k * 16):
            if (t >> 12) & 0xF == ROW and t & 0x3FF >= 640:
                j = (t & 0x3FF) - 640
                clash = {stp[(j % 16) * 8 + i % 8, (j // 16) * 8 + i // 8] for i in range(64)} & set(want)
                assert not clash or all(row10[s] == want[s] for s in clash), "row 10 slots %s are in use by block %d" % (sorted(clash), 640 + k)
    for s, c in want.items():
        row10[s] = c

    total = num_tiles + len(new_tiles)
    print("  %d trees back to vanilla's; %d chalk cells, %d ledge cells, %d crossing cells" % (trees, len(CHALK_CELLS), W - 4, len(CROSSING)))
    print("  %d tiles added (now %d/384), %d blocks added (now %d/384)" % (len(new_tiles), total, copies, len(metas) // 16))
    assert total <= 384 and len(metas) // 16 <= 384

    grown = Image.new("P", (128, ((total + 15) // 16) * 8)); grown.putpalette(st.getpalette()); grown.paste(st, (0, 0)); gp = grown.load()
    for n, key in enumerate(new_tiles):
        s = num_tiles + n
        for i, v in enumerate(key):
            gp[(s % 16) * 8 + i % 8, (s // 16) * 8 + i // 8] = v

    # ---- preview
    pals = [read_pal(os.path.join(PD, "palettes/%02d.pal" % n)) for n in range(7)] + \
           [read_pal(os.path.join(SD, "palettes/%02d.pal" % n)) for n in range(7, 13)]
    after_pals = list(pals); after_pals[ROW] = row10
    def render(data, meta, tiles, pl):
        img = Image.new("RGB", (W * 16, H * 16)); o = img.load(); tp = tiles.load()
        for y in range(H):
            for x in range(W):
                m = get(data, x, y) & 0x3FF
                e = struct.unpack_from("<8H", prim if m < 640 else meta, (m if m < 640 else m - 640) * 16)
                for layer in (0, 1):
                    for q in range(4):
                        t = e[layer * 4 + q]; i = t & 0x3FF
                        src, j, hh = (ptp, i, pt.height) if i < 640 else (tp, i - 640, tiles.height)
                        for yy in range(8):
                            for xx in range(8):
                                sy = (j // 16) * 8 + (7 - yy if (t >> 11) & 1 else yy)
                                v = src[(j % 16) * 8 + (7 - xx if (t >> 10) & 1 else xx), sy] if sy < hh else 0
                                if layer and v == 0:
                                    continue
                                o[x * 16 + (q % 2) * 8 + xx, y * 16 + (q // 2) * 8 + yy] = pl[(t >> 12) & 0xF][v]
        return img
    a = render(old_bd, old_metas, st, pals); b = render(bytes(bd), bytes(metas), grown, after_pals)
    sheet = Image.new("RGB", (a.width * 2 + 8, a.height), (30, 30, 30)); sheet.paste(a, (0, 0)); sheet.paste(b, (a.width + 8, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(PREVIEW)
    print("  preview %s (now | after)" % PREVIEW)

    if WRITE:
        open(bd_path, "wb").write(bd)
        open(border_path, "wb").write(van_border)
        grown.save(os.path.join(SD, "tiles.png"))
        open(os.path.join(SD, "metatiles.bin"), "wb").write(metas)
        open(os.path.join(SD, "metatile_attributes.bin"), "wb").write(attrs)
        write_pal(os.path.join(SD, "palettes/%02d.pal" % ROW), row10)
        open(RULES, "w").write(rules[:at] + str(total) + rules[at:][len(str(num_tiles)):])
        print("  written: Route 1 map and border, Blanche's tiles (-num_tiles %d), blocks, row 10" % total)


if __name__ == "__main__":
    main()
