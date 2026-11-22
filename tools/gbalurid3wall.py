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

THE JOIN (the user, 2026-11-22, with the pick): 45, 46, 57 and 58 -- the low wall's own tiles beside and under these
(ours, the green still pret's scallops) -- are redrawn with the picked fill, so the wall reads as one. The same rules,
on each tile's pixels as they stand (45/46's base row and 57/58's sill tops are kept); and because both sides of every
wall-to-wall seam are now drawn together, an EDGE COLUMN pixel is no longer kept for its own sake: it takes the fill
when, in EVERY place the tile is drawn, the tile across that seam is a wall tile and its facing pixel is green. A
seam against anything else keeps the rim. --draft writes the joined sheet too (wall_joined_sheet.png), and every
report checks every seam on every map: two facing green pixels that are both fill must be one furrow (the same
across a side seam, alternating across a top one).

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
MATCH = (45, 46, 57, 58)                  # THE JOIN: the low wall's own neighbours, redrawn with the pick
APPROVED = {"pick": "B", "join": True}    # the user, 2026-11-22, by multiple choice: B TENDED BEDS, and its four
#                                           neighbours (45, 46, 57, 58) redrawn to match, no break cell to cell

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


def contexts(t, wall):
    """{(tile, side): set of across-seam neighbours} over every place a wall tile is drawn (side L/R/U/D, top layer).
    A neighbour is the wall tile's number if it is one drawn in its row unflipped; else the other tile's 64 pixels as
    drawn there (flips applied) if it is fuchsia_city's; else None -- a primary tile, nothing, or the map's edge"""
    lay = T.layouts()
    out = {}
    for m in t.maps:
        Wd = lay[m]["width"]
        g = t.grid[m]
        tg = {}
        for i, b in enumerate(g):
            if b < 640 or b - 640 >= t.nblocks:
                continue
            for k, v in enumerate(T.entries(t.mt, b - 640)[4:]):
                at = ((i % Wd) * 2 + k % 2, (i // Wd) * 2 + k // 2)
                n, fl = (v & 0x3FF) - 640, (v >> 10) & 3
                if n < 0 or n >= len(t.now):
                    continue
                if n in wall and v >> 12 == ROWS.get(n, 10) and not fl:
                    tg[at] = n
                else:
                    p = t.now[n]
                    tg[at] = tuple(p[(7 - yy if fl & 2 else yy) * 8 + (7 - xx if fl & 1 else xx)]
                                   for yy in range(8) for xx in range(8))
        for (x, y), n in tg.items():
            if not isinstance(n, int):
                continue
            for side, (dx, dy) in (("L", (-1, 0)), ("R", (1, 0)), ("U", (0, -1)), ("D", (0, 1))):
                out.setdefault((n, side), set()).add(tg.get((x + dx, y + dy)))
    return out


def bases(t, joined):
    """the pixels each tile is redrawn from: pret's for the eight, as they stand for THE JOIN's four"""
    return {n: (t.van[n] if n in TILES else t.now[n]) for n in TILES + (MATCH if joined else ())}


def rims(t, joined):
    """{tile: the green pixels kept as they are} -- a green pixel touching anything not green in its tile, and an
    edge-column green pixel unless (joined), wherever the tile is drawn, the pixel across that seam is green on a wall
    tile drawn with it (and itself free), or is not green at all (an outline, a door frame: nothing there to meet)"""
    base = bases(t, joined)
    green = lambda p, xx, yy: p[yy * 8 + xx] in (E, F)
    ctx = contexts(t, set(base) - set(FEET)) if joined else {}

    free = set()                           # (tile, x, y): edge-column pixels the fill may take
    if joined:
        free = {(n, x, y) for n in base if n not in FEET for x in (0, 7) for y in range(8) if green(base[n], x, y)}
        while True:                        # a pixel is free only while every green across from it is free too
            keep = set()
            for (n, x, y) in free:
                side, fx = ("L", 7) if x == 0 else ("R", 0)
                for m in ctx.get((n, side), {None}):
                    if m is None:
                        keep.add((n, x, y))
                    elif isinstance(m, int):
                        if green(base[m], fx, y) and (m, fx, y) not in free:
                            keep.add((n, x, y))
                    elif m[y * 8 + fx] in (E, F):
                        keep.add((n, x, y))
            if not keep:
                break
            free -= keep
    out = {}
    for n, p in base.items():
        if n in FEET:
            continue
        out[n] = {(x, y) for y in range(8) for x in range(8) if green(p, x, y) and (
            (x in (0, 7) and (n, x, y) not in free) or any(
                0 <= x + dx < 8 and 0 <= y + dy < 8 and not green(p, x + dx, y + dy)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))))}
    return out


def draw(t, fill, joined=False):
    """the option's tiles; joined: with THE JOIN (MATCH redrawn, edge columns free across wall-to-wall seams)"""
    out = {}
    base = bases(t, joined)
    rim = rims(t, joined)
    for n, p in base.items():
        if n in FEET:
            out[n] = list(FEET[n])
            continue
        new = list(p)
        edge = rim[n]
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
    joined = any(n in tiles for n in MATCH)
    base = bases(t, joined)
    for n, px in tiles.items():
        v0 = base[n]
        if any((a == 0) != (b == 0) for a, b in zip(px, v0)):
            bad.append("%d footprint" % n)
        if any((a == 1) != (b == 1) for a, b in zip(px, v0)):
            bad.append("%d outline" % n)
        if n not in FEET:
            if any((a in (E, F)) != (b in (E, F)) for a, b in zip(px, v0)):
                bad.append("%d silhouette" % n)
            if any(a != b for a, b in zip(px, v0) if b not in (E, F)):
                bad.append("%d a pixel that is not green" % n)
            if not joined and any(px[r * 8 + c] != v0[r * 8 + c] for r in range(8) for c in (0, 7)):
                bad.append("%d edge column" % n)
    if joined:
        rim = rims(t, True)
        if any(tiles[n][y * 8 + x] != base[n][y * 8 + x] for n in rim for (x, y) in rim[n]):
            bad.append("a rim pixel moved")
        bad += seams(t, tiles)[0]
    return bad


def seams(t, tiles):
    """every wall-to-wall seam on every map: (failures, breaks). Across a side seam two facing green pixels where
    either is the fill's must be the same furrow; across a top seam two facing fill pixels must alternate. A break
    is any side-seam row whose facing greens differ, the rim's own arcs included -- reported, not failed"""
    joined = any(n in tiles for n in MATCH)
    rim = rims(t, joined)
    ctx = contexts(t, set(rim))
    isg = lambda n, k: tiles[n][k] in (E, F)
    fill = lambda n, k: isg(n, k) and (k % 8, k // 8) not in rim[n]
    fails, breaks = [], set()
    for (n, side), nbs in sorted(ctx.items(), key=str):
        for m in sorted(x for x in nbs if isinstance(x, int)):
            if side == "R":
                for y in range(8):
                    a, b = y * 8 + 7, y * 8
                    if isg(n, a) and isg(m, b) and tiles[n][a] != tiles[m][b]:
                        breaks.add((n, m, y))
                        if fill(n, a) or fill(m, b):
                            fails.append("%d|%d row %d: the furrow breaks" % (n, m, y))
            if side == "D":
                for x in range(8):
                    a, b = 56 + x, x
                    if fill(n, a) and fill(m, b) and tiles[n][a] == tiles[m][b]:
                        fails.append("%d over %d column %d: two furrows run together" % (n, m, x))
    return fails, sorted(breaks)


def sheet(t, path, rows=None, title=None):
    f, fb = T.font(12), T.font(15)
    k0 = 1 if rows is None else 0           # the joined sheet shows all seven at 2x, the gatehouse too
    if rows is None:
        rows = [("TODAY (with B THE PALE built)", "pret's scallops, recoloured by T-438",
                 {n: list(t.now[n]) for n in TILES})] + [(o[0] + "  " + o[1], o[2], draw(t, o[3])) for o in OPTIONS]
    shown = [n for n in TILES + MATCH if any(n in r[2] for r in rows)]
    shots = [[L.render_with(L.tileset_with(t, r[2]), m, (x0, y0, w, h)) for (m, x0, y0, w, h, _) in PLACES]
             for r in rows]
    close = [L.render_with(L.tileset_with(t, r[2]), "FuchsiaCity", (21, 4, 8, 3)) for r in rows]
    gw, gh = shots[0][0].size
    cw, ch = close[0].size
    TW = len(shown) * 74
    W = max(24 + TW + 20 + 6 * cw + 24, 12 + sum(2 * s.size[0] + 10 for s in shots[0][k0:]) + 12)
    rowh = 6 * ch + 70
    oth = max(s.size[1] for s in shots[0][k0:])
    H = 60 + len(rows) * rowh + 30 + len(rows) * (gh + 30) + 30 + len(rows) * (oth * 2 + 40)
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((12, 8), title or ("T-445 / T-562 -- LURID's green low wall under THE WALLED GARDEN's gatehouse "
                              "(fuchsia_city 28, 29, 30, 44, 73, 74 row 10; 75, 76 row 9). DRAFT"),
           font=fb, fill=(20, 20, 20))
    d.text((12, 30), "tiles at 8x | the gate's front at 6x (FuchsiaCity 21,4 8x3), the pales above are B as built; "
                     "75/76 (the door posts' feet) are the same in every option", font=f, fill=(70, 70, 70))
    y = 60
    for (name, line, tiles), c in zip(rows, close):
        d.text((12, y), name, font=fb, fill=(30, 30, 30) if name[0] == "T" else (150, 20, 90))
        d.text((12, y + 20), line, font=T.font(11), fill=(60, 60, 60))
        yy = y + 40
        for j, n in enumerate(shown):
            d.text((24 + j * 74, yy), str(n), font=f, fill=(30, 30, 30))
            out.paste(L.tile_img(tiles.get(n, t.now[n]), t.palette(ROWS.get(n, 10)), 8), (24 + j * 74, yy + 14))
        out.paste(c.resize((cw * 6, ch * 6), Image.NEAREST), (24 + TW + 20, yy))
        y += rowh
    d.text((12, y), "the gatehouse at 1x (FuchsiaCity 16,0 16x7)", font=f, fill=(70, 70, 70))
    y += 20
    for (name, _, _), s in zip(rows, shots):
        d.text((12, y), name[:1], font=fb, fill=(30, 30, 30))
        out.paste(s[0], (40, y))
        y += gh + 10
    y += 10
    d.text((12, y), ("everywhere else" if k0 else "all seven") + ", at 2x: " + ", ".join(p[5] for p in PLACES[k0:]),
           font=f, fill=(70, 70, 70))
    y += 20
    for (name, _, _), s in zip(rows, shots):
        d.text((12, y), name, font=f, fill=(30, 30, 30))
        x = 12
        for im in s[k0:]:
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
    pick = APPROVED.get("pick")
    if pick and APPROVED.get("join"):
        o = [x for x in OPTIONS if x[0] == pick][0]
        tiles = draw(t, o[3], joined=True)
        bad = check(t, tiles)
        fails += bool(bad)
        print("  THE JOIN (%s, with %s): %s" % (pick, ", ".join(map(str, MATCH)),
                                                "rules kept, every seam one furrow" if not bad else
                                                "FAILS " + "; ".join(bad)))
        print("    side-seam rows whose greens differ, on every map: %d %s" % (
            len(seams(t, tiles)[1]), seams(t, tiles)[1]))
    if "--draft" in ARGS:
        i = ARGS.index("--draft")
        out = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else L.DRAFT_DEFAULT
        os.makedirs(out, exist_ok=True)
        for o in OPTIONS:
            L.tileset_with(t, draw(t, o[3])).save(os.path.join(out, "wall_tiles_%s.png" % o[0]))
        print("  wrote %s" % sheet(t, os.path.join(out, "wall_sheet.png")))
        if pick and APPROVED.get("join"):
            o = [x for x in OPTIONS if x[0] == pick][0]
            rows = [("TODAY", "as built: pret's scallops on the eight, our flat-filled 45/46/57/58 beside them",
                     {n: list(t.now[n]) for n in TILES + MATCH}),
                    (o[0] + "  " + o[1] + ", as picked", "the eight alone: the furrows stop at 45/46/57/58",
                     {**draw(t, o[3]), **{n: list(t.now[n]) for n in MATCH}}),
                    (o[0] + "  " + o[1] + ", JOINED", "45, 46, 57, 58 drawn to match and the wall-to-wall seams "
                                                      "freed: one wall, no break cell to cell", draw(t, o[3], True))]
            print("  wrote %s" % sheet(t, os.path.join(out, "wall_joined_sheet.png"), rows,
                                       "T-445 -- LURID's low wall, %s %s JOINED: fuchsia_city 28 29 30 44 73 74 75 76 "
                                       "and 45 46 57 58. DRAFT" % (o[0], o[1].replace(" (DRAFT)", ""))))
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED.get("pick"):
            print("  --write: refused -- nothing is approved (APPROVED is empty; DRAFT)")
            return 1
        o = [x for x in OPTIONS if x[0] == APPROVED["pick"]][0]
        tiles = draw(t, o[3], bool(APPROVED.get("join")))
        if check(t, tiles):
            print("  --write: refused -- option %s breaks a rule" % o[0])
            return 1
        L.tileset_with(t, tiles).save(os.path.join(t.dir, "tiles.png"))
        print("  wrote option %s%s into %s/tiles.png" % (o[0], " joined" if APPROVED.get("join") else "", t.dir))
    elif APPROVED.get("pick"):
        o = [x for x in OPTIONS if x[0] == APPROVED["pick"]][0]
        tiles = draw(t, o[3], bool(APPROVED.get("join")))
        same = all(t.now[n] == tiles[n] for n in tiles)
        print("  engine: %s" % ("as approved" if same else "DIFFERS from pick %s" % o[0]))
        return 0 if same and not fails else 1
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
