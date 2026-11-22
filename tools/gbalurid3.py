#!/usr/bin/env python3
"""T-445 / T-562's leftover: LURID's last three pret tiles on THE WALLED GARDEN's gatehouse, drawn in our own hand.

    python3 tools/gbalurid3.py                      # report: the three tiles (pret's pixels or not), every block and
                                                    #   every map cell that draws them, and each option's checks
    python3 tools/gbalurid3.py --draft [DIR]        # each option's tiles.png and the sheet (gfx/drafts/t445_lurid3/):
                                                    #   the tiles at 8x, the gatehouse front at 1x and 3x per option,
                                                    #   and every other building that draws them
    python3 tools/gbalurid3.py --write --approved   # the picked option's three tiles into the engine's fuchsia_city
                                                    #   tiles.png. Refused while APPROVED is empty

WHAT THEY ARE. fuchsia_city's secondary tiles 41, 42 and 63, all in palette row 10, still pixel for pixel pret's
(T-438 recoloured them and T-562's family cut left them as they were):

  42  the roof's EAVE: the gold roof's last shingle course (13, one 3 where tile 26's shingle line runs down) over
      a fascia (12 then 11). 41 is its left end (the outline, a cream edge). 43, the right end, is already ours.
  63  the FRIEZE: the pale vertical stripes (9 and 7, period 4) between the wall's head (13) and the window heads
      (57/58), on the gatehouse and the SECRET HOUSE only.

Where they are drawn (11 blocks, 7 buildings): the gatehouse (FuchsiaCity 22-27,3-4, warp 24,5), the SECRET HOUSE
(SafariZone_West 10-15,5-6) -- the same front -- and the eave alone on the SAFARI ZONE OFFICE (FuchsiaCity 26-31,15)
and the four rest houses (SafariZone_Center, _East, _North, _West). --draft renders every one of them.

THE RULES (gbatownslast's, which this continues): pixels only -- no block, layer, flip, palette row or colour moves;
FOOTPRINT kept (none of the three has a clear pixel); OUTLINE kept (41's index-1 column); and every SEAM a
neighbour reads is kept where it can be: 63's top row meets tile 13's stripes and its bottom row 57/58's, so both
rows keep the stripe's phase (9 at columns 0, 3, 4, 7); 42's top row continues 26's shingle line (the 3 at column
2); the fascia ends against 43's plain 11, so each option's fascia motif sits in the 11/12/13 family and stops
there without a cap. The drawing in between is new.

Every in-game word: none. This is art. DRAFT until the user picks.
"""
import io, os, shutil, struct, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import gbatowns as T                      # noqa: E402  (gbatowns and reviewsheet read their flags at import)
import reviewsheet as R                   # noqa: E402
sys.argv = _argv
from PIL import Image, ImageDraw          # noqa: E402

ROOT, GBA = T.ROOT, T.GBA
ARGS = sys.argv[1:]
TS = "fuchsia_city"
TILES = (41, 42, 63)
ROW = 10
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t445_lurid3")
APPROVED = {}                             # {"pick": "A"} once the user has chosen; empty: --write writes nothing

#  every place the three tiles are drawn: (map, x0, y0, w, h, what) -- the box shown on the sheet
PLACES = [("FuchsiaCity", 16, 0, 16, 7, "THE WALLED GARDEN's gatehouse (FuchsiaCity, warp 24,5)"),
          ("SafariZone_West", 8, 2, 10, 7, "the SECRET HOUSE (SafariZone_West, warp 12,7)"),
          ("FuchsiaCity", 24, 11, 10, 7, "the SAFARI ZONE OFFICE (FuchsiaCity, warp 28,16)"),
          ("SafariZone_Center", 27, 21, 7, 6, "the CENTER rest house"),
          ("SafariZone_East", 38, 10, 7, 6, "the EAST rest house"),
          ("SafariZone_North", 41, 4, 7, 6, "the NORTH rest house"),
          ("SafariZone_West", 17, 14, 7, 6, "the WEST rest house")]


def g(*rows):
    """an 8x8 tile from eight hex rows"""
    assert len(rows) == 8 and all(len(r) == 8 for r in rows)
    return [int(c, 16) for r in rows for c in r]


#  pret's own, for the sheet and the census
PRET = {41: g("15dcdcdc", "15dcdcdc", "15dcdcdc", "15dcdcdc", "1dcbcbcb", "1bbbbbbb", "1bbbbbbb", "1bbbbbbb"),
        42: g("dd3ddddd", "dddddddd", "dddddddd", "dddddddd", "cccccccc", "bbbbbbbb", "bbbbbbbb", "bbbbbbbb"),
        63: g("97799779", "97799779", "97799779", "97799779", "97799779", "97799779", "97799779", "97799779")}

#  row 10: 1 outline navy, 2 slate, 3 dark gold, 5 cream, 6 pale, 7 warm grey, 8 grey, 9 light stone,
#          a 8b7b31 deep gold, b a4944a gold, c cdc57b light gold, d e6d58b pale gold, e/f the low wall's greens
OPTIONS = [
    ("A", "THE HUM (DRAFT)",
     "LURID's own pick (T-562 B) carried onto the gate: the fascia is a lit tube -- a cream line over a deep gold "
     "gap -- and one level tube crosses the frieze over the windows, so the gate hums like every frontage in town",
     {41: g("15dcdcdc", "15dcdcdc", "15dcdcdc", "1dcccccc", "1d555555", "1bdddddd", "1bbbbbbb", "1aaaaaaa"),
      42: g("dd3ddddd", "dddddddd", "dddddddd", "cccccccc", "55555555", "dddddddd", "bbbbbbbb", "aaaaaaaa"),
      63: g("97799779", "97799779", "97799779", "55555555", "99999999", "88888888", "97799779", "97799779")}),
    ("B", "THE PALE (DRAFT)",
     "the walled garden's palisade: the stripes become pales, lit on their left, with dark gaps and one rail across "
     "them; the eave a cornice of dentils, the gate's crown",
     {41: g("15dcdcdc", "15dcdcdc", "15dcdcdc", "1dcccccc", "1ddddddd", "1bcdacda", "1bbcabca", "1bbbbbbb"),
      42: g("dd3ddddd", "dddddddd", "dddddddd", "cccccccc", "dddddddd", "dacddacd", "cabccabc", "bbbbbbbb"),
      63: g("97799779", "98769876", "98769876", "66666666", "77777777", "92269226", "98769876", "97799779")}),
    ("C", "THE ROPE AND TRELLIS (DRAFT)",
     "a curated door: the fascia a twisted rope (the line you wait behind), and the frieze a trellis -- a diamond "
     "lattice over the pale stone, the garden's frame without its leaves",
     {41: g("15dcdcdc", "15dcdcdc", "15dcdcdc", "1dcccccc", "1cddcbdd", "1adcbadc", "1bacbbac", "1bbbbbbb"),
      42: g("dd3ddddd", "dddddddd", "dddddddd", "cccccccc", "ddcbddcb", "dcbadcba", "cbbacbba", "bbbbbbbb"),
      63: g("97799779", "89999998", "98999989", "99899899", "99988999", "99988999", "99899899", "97799779")}),
]


def town():
    return T.Town(TS)


def uses(t):
    """{block: [(entry, tile, row, flip)]} and {map: [(x, y, block)]} for the three tiles"""
    blocks = {}
    for b in range(t.nblocks):
        hit = [(k, (v & 0x3FF) - 640, v >> 12, (v >> 10) & 3) for k, v in enumerate(T.entries(t.mt, b))
               if v & 0x3FF >= 640 and (v & 0x3FF) - 640 in TILES]
        if hit:
            blocks[640 + b] = hit
    cells = {}
    for m in t.maps:
        W = T.layouts()[m]["width"]
        c = [(i % W, i // W, v) for i, v in enumerate(t.grid[m]) if v in blocks]
        if c:
            cells[m] = c
    return blocks, cells


def check(t, opt):
    """the rules, for one option: a list of failures"""
    _, _, _, tiles = opt
    bad = []
    for n, px in tiles.items():
        if any((a == 0) != (b == 0) for a, b in zip(px, t.now[n])):
            bad.append("%d footprint" % n)
        if any(v in (0, 4) for v in px):
            bad.append("%d uses index 0 or 4" % n)
    if any(tiles[41][r * 8] != 1 for r in range(8)):
        bad.append("41 outline column")
    if tiles[42][:8] != PRET[42][:8]:
        bad.append("42 top row (26's shingle line)")
    for r in (0, 7):
        row = tiles[63][r * 8:r * 8 + 8]
        if any(row[c] != 9 for c in (0, 3, 4, 7)):
            bad.append("63 row %d leaves the stripe's phase" % r)
    return bad


def tileset_with(t, tiles):
    """the engine's fuchsia_city tiles.png with these tiles laid in (same palette, same size)"""
    im = Image.open(os.path.join(t.dir, "tiles.png")).copy()
    px = im.load()
    for n, p in tiles.items():
        for k, v in enumerate(p):
            px[(n % 16) * 8 + k % 8, (n // 16) * 8 + k // 8] = v
    return im


def render_with(im, mapname, box):
    """reviewsheet's own map render, with fuchsia_city's tiles.png swapped for `im` (a draft tileset folder)"""
    tmp = tempfile.mkdtemp(prefix="lurid3_")
    src = os.path.join(GBA, T.SEC + TS)
    shutil.copytree(os.path.join(src, "palettes"), os.path.join(tmp, "palettes"))
    im.save(os.path.join(tmp, "tiles.png"))
    real = R.gdir

    def gdir(symbol, kind):
        d = real(symbol, kind)
        return tmp if os.path.realpath(d) == os.path.realpath(src) else d
    R.gdir = gdir
    try:
        img = R.render(R.layout_of(mapname))
    finally:
        R.gdir = real
        shutil.rmtree(tmp)
    x0, y0, w, h = box
    return img.crop((x0 * 16, y0 * 16, (x0 + w) * 16, (y0 + h) * 16))


def tile_img(p, pal, Z):
    im = Image.new("RGB", (8, 8))
    im.putdata([pal[v] if v else (255, 0, 255) for v in p])
    return im.resize((8 * Z, 8 * Z), Image.NEAREST)


def sheet(t, path):
    pal = t.palette(ROW)
    f, fb = T.font(12), T.font(15)
    rows = [("PRET (today)", "pret's drawing, recoloured by T-438: the eave's flat bands and the frieze's stripes",
             {n: list(t.now[n]) for n in TILES})] + [(o[0] + "  " + o[1], o[2], o[3]) for o in OPTIONS]
    gate = PLACES[0]
    shots = [[render_with(tileset_with(t, r[2]), m, (x0, y0, w, h)) for (m, x0, y0, w, h, _) in PLACES]
             for r in rows]
    gw, gh = shots[0][0].size
    W = 24 + 3 * (64 + 10) + 20 + gw + 16 + 3 * gw + 24
    rowh = max(3 * gh, 64 + 40) + 70
    others = PLACES[1:]
    oth = max(s.size[1] for s in shots[0][1:])
    W = max(W, 12 + sum(2 * s.size[0] + 10 for s in shots[0][1:]) + 12)
    H = 60 + len(rows) * rowh + 40 + len(rows) * (oth * 2 + 40) + 20
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((12, 8), "T-445 / T-562 -- LURID's last three pret tiles: THE WALLED GARDEN's gatehouse (fuchsia_city 41, "
                    "42, 63; palette row 10). DRAFT", font=fb, fill=(20, 20, 20))
    d.text((12, 30), "tiles at 8x (41 eave's left end, 42 eave, 63 frieze) | the gatehouse at 1x | at 3x  -- "
                     "FuchsiaCity 16,0 16x7, rendered from the engine's tilesets with the option laid in",
           font=f, fill=(70, 70, 70))
    y = 60
    for (name, line, tiles), shot in zip(rows, shots):
        d.text((12, y), name, font=fb, fill=(150, 20, 90) if name[0] != "P" else (30, 30, 30))
        d.text((12, y + 20), line[:190], font=T.font(11), fill=(60, 60, 60))
        if len(line) > 190:
            d.text((12, y + 34), line[190:380], font=T.font(11), fill=(60, 60, 60))
        yy = y + 52
        for j, n in enumerate(TILES):
            out.paste(tile_img(tiles[n], pal, 8), (24 + j * 74, yy + 14))
            d.text((24 + j * 74, yy), str(n), font=f, fill=(30, 30, 30))
        x = 24 + 3 * 74 + 20
        out.paste(shot[0], (x, yy))
        out.paste(shot[0].resize((gw * 3, gh * 3), Image.NEAREST), (x + gw + 16, yy))
        y += rowh
    d.text((12, y), "everywhere else the tiles are drawn, at 2x: " + ", ".join(p[5] for p in others), font=f,
           fill=(70, 70, 70))
    y += 24
    for (name, _, _), shot in zip(rows, shots):
        d.text((12, y), name, font=f, fill=(30, 30, 30))
        x = 12
        for s in shot[1:]:
            s2 = s.resize((s.size[0] * 2, s.size[1] * 2), Image.NEAREST)
            out.paste(s2, (x, y + 16))
            x += s2.size[0] + 10
        y += oth * 2 + 40
    out = out.crop((0, 0, W, y + 10))
    out.save(path)
    return path


def main():
    t = town()
    blocks, cells = uses(t)
    print("fuchsia_city tiles %s, palette row %d" % (", ".join(map(str, TILES)), ROW))
    for n in TILES:
        print("  tile %d: %s pret's pixels, %d 8x8 draws on reachable maps" %
              (n, "still" if t.now[n] == t.van[n] else "NOT", t.draws[n]))
    for b, hit in sorted(blocks.items()):
        print("  block 0x%03x (placed %d): %s" % (b, t.placed.get(b, 0), hit))
    for m, c in cells.items():
        print("  %s: %d cells %s" % (m, len(c), [(x, y) for x, y, _ in c]))
    fails = 0
    for o in OPTIONS:
        bad = check(t, o)
        fails += bool(bad)
        print("  option %s %-28s %s" % (o[0], o[1], "rules kept" if not bad else "FAILS " + "; ".join(bad)))
    if "--draft" in ARGS:
        i = ARGS.index("--draft")
        out = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else DRAFT_DEFAULT
        os.makedirs(out, exist_ok=True)
        for o in OPTIONS:
            tileset_with(t, o[3]).save(os.path.join(out, "tiles_%s.png" % o[0]))
        print("  wrote %s" % sheet(t, os.path.join(out, "sheet.png")))
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED.get("pick"):
            print("  --write: refused -- nothing is approved (APPROVED is empty; DRAFT)")
            return 1
        o = [x for x in OPTIONS if x[0] == APPROVED["pick"]][0]
        if check(t, o):
            print("  --write: refused -- option %s breaks a rule" % o[0])
            return 1
        tileset_with(t, o[3]).save(os.path.join(t.dir, "tiles.png"))
        print("  wrote option %s into %s/tiles.png" % (o[0], t.dir))
    else:
        mine = APPROVED.get("pick")
        if mine:
            o = [x for x in OPTIONS if x[0] == mine][0]
            same = all(t.now[n] == o[3][n] for n in TILES)
            print("  engine: %s" % ("as approved" if same else "DIFFERS from pick %s" % mine))
            return 0 if same and not fails else 1
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
