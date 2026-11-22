#!/usr/bin/env python3
"""T-445 / T-562's leftover, part two: the green low wall under THE WALLED GARDEN's gatehouse, in our own hand.

    python3 tools/gbalurid3wall.py                    # report: the eight tiles, every block and cell that draws them,
                                                      #   each option's checks
    python3 tools/gbalurid3wall.py --draft [DIR]      # each option's tiles.png and the sheet (gfx/drafts/t445_lurid3/
                                                      #   wall_*): the tiles at 8x, the gatehouse at 1x and 3x, and
                                                      #   every other building that draws them at 2x
    python3 tools/gbalurid3wall.py --write --approved # the picked option into the engine; refused while APPROVED is empty

WHAT THEY ARE (fuchsia_city, all still pret's pixels after gbalurid3's B was built, 2026-11-22):
  28, 29, 30   the low wall's top: the frieze's stripes running down into the green scallops (29 a whole scallop,
               28 and 30 its left and right ends against the wall's edge), palette row 10
  44           the low wall's left foot: scallop over the plinth (the 1 line and the 2 base), row 10
  73, 74       under the windows: the sill (2/8/9/8) and the scallops either side of it, over the plinth, row 10
  75, 76       the feet of the door frame's two posts on the step, row 9 (1 7 7 7 1 over an outline)

THE RULES (gbalurid3's): pixels only; footprint kept; the outline (index 1), the plinth (rows 6-7 of 44/73/74), the
stripes above the scallops and the sills are kept, so every seam with 63 (B, above), with 57/58 and 45/46 (ours,
beside and under) is where it was. The SILHOUETTE is kept: every pixel that was green stays green, and the scallop's RIM -- a green pixel touching
anything not green, and every green pixel in a tile's outermost columns -- keeps pret's 14 or 15, so the scallops
still meet 57/58/45/46's; only the green inside the rim is redrawn. 75/76 are drawn the same in
every option: each post's foot lit on its left, as the pales above it are.

Every in-game word: none. This is art. DRAFT until the user picks.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import gbalurid3 as L                     # noqa: E402
sys.argv = _argv
from PIL import Image, ImageDraw          # noqa: E402

T = L.T
ARGS = sys.argv[1:]
TILES = (28, 29, 30, 44, 73, 74, 75, 76)
ROWS = {75: 9, 76: 9}                     # every other one is row 10
E, F = 14, 15
APPROVED = {}                             # {"pick": "X"} once the user has chosen; empty: --write writes nothing

#  where they are drawn (the same buildings as gbalurid3's, every one of them)
PLACES = L.PLACES


def g(*rows):
    return L.g(*rows)


#  75/76 in every option: the post's foot, lit on its left (row 9: 8 light, 7 grey, 2 dark)
FEET = {75: g("18721000", "11111000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"),
        76: g("00018721", "00011111", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000")}


def fill_hedge(x, y, p, near):
    """A CLIPPED HEDGE: a lit crown just under the scallop's rim, then leaf clumps -- a short dark mark under every
    fourth pixel, staggered row by row, so the scallops read as clipped box, not paint"""
    if near(1):
        return F
    return E if (y % 2 == 1 and (x + (y // 2) * 2) % 4 == 1) else F


def fill_beds(x, y, p, near):
    """B TENDED BEDS: the green in level rows -- a dark furrow every other line -- the pale's rail carried into the
    garden: planted in lines, kept"""
    return E if y % 2 == 0 else F


def fill_arches(x, y, p, near):
    """C ARCHES: a lit band inside the rim, a dark core inside that, so every scallop is a double arch -- the gate's
    arches repeated small along its foot"""
    return F if near(1) else E


OPTIONS = [("A", "CLIPPED HEDGE (DRAFT)", "the scallops as clipped box: a lit crown under the rim, leaf clumps "
                                          "below -- the garden showing over its own wall", fill_hedge),
           ("B", "TENDED BEDS (DRAFT)", "the green in level furrows, the pale's rail carried into the planting: a "
                                        "garden in lines, kept", fill_beds),
           ("C", "ARCHES (DRAFT)", "a second rim inside each scallop: a row of small double arches along the gate's "
                                   "foot", fill_arches)]


def draw(t, fill):
    out = {}
    for n in TILES:
        if n in FEET:
            out[n] = list(FEET[n])
            continue
        p = t.van[n]
        new = list(p)
        green = lambda xx, yy: p[yy * 8 + xx] in (E, F)
        edge = {(x, y) for y in range(8) for x in range(8) if green(x, y) and (x in (0, 7) or any(
            0 <= x + dx < 8 and 0 <= y + dy < 8 and not green(x + dx, y + dy)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))))}
        for k, v in enumerate(p):
            x, y = k % 8, k // 8
            if v not in (E, F) or (x, y) in edge:
                continue

            def near(d, x=x, y=y):
                """the scallop's rim (a kept edge pixel) within d pixels"""
                return any((xx, yy) in edge for yy in range(y - d, y + d + 1) for xx in range(x - d, x + d + 1)
                           if (xx, yy) != (x, y))
            new[k] = fill(x, y, p, near)
        out[n] = new
    return out


def check(t, tiles):
    bad = []
    for n, px in tiles.items():
        v0 = t.van[n]
        if any((a == 0) != (b == 0) for a, b in zip(px, v0)):
            bad.append("%d footprint" % n)
        if any((a == 1) != (b == 1) for a, b in zip(px, v0)):
            bad.append("%d outline" % n)
        if n not in FEET:
            if any((a in (E, F)) != (b in (E, F)) for a, b in zip(px, v0)):
                bad.append("%d silhouette" % n)
            if any(px[r * 8 + c] != v0[r * 8 + c] for r in range(8) for c in (0, 7)):
                bad.append("%d edge column" % n)
    return bad


def sheet(t, path):
    f, fb = T.font(12), T.font(15)
    rows = [("TODAY (with B THE PALE built)", "pret's scallops, recoloured by T-438",
             {n: list(t.now[n]) for n in TILES})] + [(o[0] + "  " + o[1], o[2], draw(t, o[3])) for o in OPTIONS]
    shots = [[L.render_with(L.tileset_with(t, r[2]), m, (x0, y0, w, h)) for (m, x0, y0, w, h, _) in PLACES]
             for r in rows]
    close = [L.render_with(L.tileset_with(t, r[2]), "FuchsiaCity", (21, 4, 8, 3)) for r in rows]
    gw, gh = shots[0][0].size
    cw, ch = close[0].size
    TW = len(TILES) * 74
    W = max(24 + TW + 20 + 6 * cw + 24, 12 + sum(2 * s.size[0] + 10 for s in shots[0][1:]) + 12)
    rowh = 6 * ch + 70
    oth = max(s.size[1] for s in shots[0][1:])
    H = 60 + len(rows) * rowh + 30 + len(rows) * (gh + 30) + 30 + len(rows) * (oth * 2 + 40)
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((12, 8), "T-445 / T-562 -- LURID's green low wall under THE WALLED GARDEN's gatehouse (fuchsia_city 28, 29, "
                    "30, 44, 73, 74 row 10; 75, 76 row 9). DRAFT", font=fb, fill=(20, 20, 20))
    d.text((12, 30), "tiles at 8x | the gate's front at 6x (FuchsiaCity 21,4 8x3), the pales above are B as built; "
                     "75/76 (the door posts' feet) are the same in every option", font=f, fill=(70, 70, 70))
    y = 60
    for (name, line, tiles), c in zip(rows, close):
        d.text((12, y), name, font=fb, fill=(30, 30, 30) if name[0] == "T" else (150, 20, 90))
        d.text((12, y + 20), line, font=T.font(11), fill=(60, 60, 60))
        yy = y + 40
        for j, n in enumerate(TILES):
            d.text((24 + j * 74, yy), str(n), font=f, fill=(30, 30, 30))
            out.paste(L.tile_img(tiles[n], t.palette(ROWS.get(n, 10)), 8), (24 + j * 74, yy + 14))
        out.paste(c.resize((cw * 6, ch * 6), Image.NEAREST), (24 + TW + 20, yy))
        y += rowh
    d.text((12, y), "the gatehouse at 1x (FuchsiaCity 16,0 16x7)", font=f, fill=(70, 70, 70))
    y += 20
    for (name, _, _), s in zip(rows, shots):
        d.text((12, y), name[:1], font=fb, fill=(30, 30, 30))
        out.paste(s[0], (40, y))
        y += gh + 10
    y += 10
    d.text((12, y), "everywhere else, at 2x: " + ", ".join(p[5] for p in PLACES[1:]), font=f, fill=(70, 70, 70))
    y += 20
    for (name, _, _), s in zip(rows, shots):
        d.text((12, y), name, font=f, fill=(30, 30, 30))
        x = 12
        for im in s[1:]:
            im2 = im.resize((im.size[0] * 2, im.size[1] * 2), Image.NEAREST)
            out.paste(im2, (x, y + 16))
            x += im2.size[0] + 10
        y += oth * 2 + 40
    out.crop((0, 0, W, y + 10)).save(path)
    return path


def main():
    t = L.town()
    L.TILES = TILES
    blocks, cells = L.uses(t)
    print("fuchsia_city's low wall: tiles %s" % ", ".join(map(str, TILES)))
    for n in TILES:
        print("  tile %d (row %d): %s pret's pixels, %d draws" %
              (n, ROWS.get(n, 10), "still" if t.now[n] == t.van[n] else "NOT", t.draws[n]))
    for b, hit in sorted(blocks.items()):
        print("  block 0x%03x (placed %d): %s" % (b, t.placed.get(b, 0), hit))
    for m, c in cells.items():
        print("  %s: %d cells %s" % (m, len(c), [(x, y) for x, y, _ in c]))
    fails = 0
    for o in OPTIONS:
        bad = check(t, draw(t, o[3]))
        fails += bool(bad)
        print("  option %s %-24s %s" % (o[0], o[1], "rules kept" if not bad else "FAILS " + "; ".join(bad)))
    if "--draft" in ARGS:
        i = ARGS.index("--draft")
        out = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else L.DRAFT_DEFAULT
        os.makedirs(out, exist_ok=True)
        for o in OPTIONS:
            L.tileset_with(t, draw(t, o[3])).save(os.path.join(out, "wall_tiles_%s.png" % o[0]))
        print("  wrote %s" % sheet(t, os.path.join(out, "wall_sheet.png")))
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED.get("pick"):
            print("  --write: refused -- nothing is approved (APPROVED is empty; DRAFT)")
            return 1
        o = [x for x in OPTIONS if x[0] == APPROVED["pick"]][0]
        tiles = draw(t, o[3])
        if check(t, tiles):
            print("  --write: refused -- option %s breaks a rule" % o[0])
            return 1
        L.tileset_with(t, tiles).save(os.path.join(t.dir, "tiles.png"))
        print("  wrote option %s into %s/tiles.png" % (o[0], t.dir))
    elif APPROVED.get("pick"):
        o = [x for x in OPTIONS if x[0] == APPROVED["pick"]][0]
        tiles = draw(t, o[3])
        same = all(t.now[n] == tiles[n] for n in TILES)
        print("  engine: %s" % ("as approved" if same else "DIFFERS from pick %s" % o[0]))
        return 0 if same and not fails else 1
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
