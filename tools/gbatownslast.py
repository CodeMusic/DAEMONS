#!/usr/bin/env python3
"""T-562: the towns' last Nintendo tiles -- batch 3 of the 2026-11-14 re-census, drawn in each town's own T-438 look.

    python3 tools/gbatownslast.py                     # report: the recount per town (tiles a reachable map places,
                                                      #   pixel-identical to pret's upstream/master, minus the tiles a
                                                      #   tile animation overwrites), what is excluded and why, and how
                                                      #   much the draft redraws
    python3 tools/gbatownslast.py --draft [DIR]       # the drafts into DIR (gfx/drafts/t562_towns/): per town
                                                      #   tiles.png (option A, or the only one), tiles_B.png / _C.png
                                                      #   where a real choice exists, VERDIGRIS's fountain frames per
                                                      #   option, draft.json, and a 4x sheet of every changed tile
    python3 tools/gbatownslast.py --write --approved  # into the engine: the towns in APPROVED, each with the option
                                                      #   the user picked (2026-11-14), drawn from BASE and laid over
                                                      #   the engine's own tiles.png; a second write is a no-op. The
                                                      #   report exits 1 when the engine differs from the picks

WHY A SECOND PASS. gbatowns.py (T-438 batch F/G/H) redrew each town's leftovers by MATERIAL: an index a town's
MATERIALS names is redrawn with that town's motif, and every other index keeps pret's pixel. What it left -- 548 tiles,
batch 3 of the re-census -- are the tiles drawn only in indices no material names (walls, rails, sills, the dept.
store's purple, the SAFARI's woods' yellows, ROUTE 23's paving) or whose motif returns pret's own level (LURID's calm
gloss). This pass gives every such index a material automatically -- the indices of one palette row a leftover tile
uses, grouped by HUE into families (grey, red, orange, yellow, green, teal, blue, purple, pink) -- and draws each
family with the motif its town already uses for that kind of surface (STYLE below), so each town continues its own
look and nothing new is imposed.

THE RULES (gbaprimary's, kept here):
  * pixels only -- no block, layer, flip, palette row, behaviour, collision or map moves; no colour changes;
  * FOOTPRINT: index 0 stays 0, a drawn pixel stays drawn;
  * OUTLINE: every row's dark line (its darkest index, when it is darker than LUM_OUTLINE), its whites, and general's
    reserved indices (row 2 idx 8, rows 4/6 idx 1: the runtime's day colour) keep pret's pixel everywhere;
  * a pixel touching transparency or a DIFFERENT family keeps pret's pixel, so every sill, eave and join -- and so
    every seam where the tile meets its neighbour -- is where it was; a family needs two indices to make a ladder;
  * a tile is drawn where it is drawn most (its home object), in that object's coordinates, so a motif runs across
    tiles; a tile drawn elsewhere carries the same pixels (it is one tile);
  * EXCLUDED, and named in the report: the door tiles (gbadoors.py derives every door's frames from them), gbatowns'
    KEEP_TILES and grove tells (gbagrove.py), every tile a LANDMARK draws -- gbatowns.LANDMARKS and the two T-447 plan
    boxes it does not carry (the GAME CORNER, KEEPALIVE PLANT's front on ROUTE 10) -- and a tile that is a copy of a
    general tile T-542 left as pret's on purpose (gbaprimary's edges 4, 301, 503).

SEAMS (engine.md trap 14) are measured with gbatowns.seams (gbaseams' own rule) before and after.
DRIFT: gbatowns.py's drawn_before() reads a tile it did not draw as not vanilla, so after this tool writes, its
leftovers shrink by these tiles and its own write stays a no-op (checked on the draft engine).
"""
import collections, colorsys, io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import gbatowns as T                      # noqa: E402  (gbatowns reads its flags at import)
sys.argv = _argv
from PIL import Image, ImageDraw          # noqa: E402

ROOT = T.ROOT
GBA = T.GBA
ARGS = sys.argv[1:]
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t562_towns")

#  the user's picks, {ts: option} -- "A"; for celadon_city two letters, the town's then the fountain's ("AB").
#  EMPTY: nothing is approved, so --write --approved writes nothing.
#  The user, 2026-11-14 (by multiple choice): LURID B THE HUM; VERDIGRIS's store A BRONZE PANELS and its fountain
#  B RINGS; BRAZEN, ARDOR, DOLDRUM, CALLOW, SLATE and QUICKSILVER as drawn; UMBRA revised first (pret's pillar-drum and
#  tan-panel shading kept, UMBRA's long shadow cut over them) -- included as revised. HALFTONE and THE UNDERTONE draw
#  nothing (their families have one index each) and are not listed.
APPROVED = {"fuchsia_city": "B", "celadon_city": "AB", "saffron_city": "A", "vermilion_city": "A",
            "cerulean_city": "A", "viridian_city": "A", "pewter_city": "A", "cinnabar_island": "A",
            "indigo_plateau": "A"}

#  THE ENGINE AS T-562 FOUND IT: every redraw starts from the tiles at this engine commit (origin/context-content,
#  2026-11-14, before T-562's write), so a write is the same pixels every time -- a second write is a no-op and the
#  report can check the engine against the picks -- and no tile any other tool drew afterwards is ever read as a
#  leftover. The fountain's frames are read from pret's upstream/master.
BASE = "7955b7bea"
_BASE_TILES = {}


def base_town(ts):
    """gbatowns' Town, its `now` tiles read from BASE"""
    town = T.Town(ts)
    if ts not in _BASE_TILES:
        _BASE_TILES[ts] = T.tiles_of(Image.open(io.BytesIO(T.daemonslib.upstream(
            GBA, T.SEC + ts + "/tiles.png", binary=True, ref=BASE))))
    town.now = [list(t) for t in _BASE_TILES[ts]]
    town._leftovers()
    return town


#  the eleven sets, largest first (the re-census's order)
TOWNS = [("fuchsia_city", "LURID CITY and the SAFARI"), ("celadon_city", "VERDIGRIS CITY and ROUTES 16-18"),
         ("saffron_city", "BRAZEN CITY"), ("lavender_town", "HALFTONE TOWN and ROUTES 8, 10, 12-14"),
         ("vermilion_city", "ARDOR CITY and ROUTES 6, 11"), ("indigo_plateau", "UMBRA PLATEAU and ROUTE 23"),
         ("cerulean_city", "DOLDRUM CITY and ROUTES 4, 5, 9, 24, 25"), ("viridian_city", "CALLOW CITY"),
         ("pewter_city", "SLATE CITY"), ("cinnabar_island", "QUICKSILVER IS."), ("viridian_forest", "THE UNDERTONE")]

#  tiles a tile animation overwrites (trap 39): VERDIGRIS's fountain, 744..751 -> secondary 104..111
ANIM = {"celadon_city": set(range(104, 112))}
FOUNTAIN = "data/tilesets/secondary/celadon_city/anim/fountain/%d.png"

#  T-447's plan boxes gbatowns.LANDMARKS does not carry (docs/private/plan-landmarks-2026-10-24.md rows 7 and 8).
#  KEEPALIVE's box is the plan's 11x7 plus the row under it, where its pylons' feet stand (the leftover object's box)
LANDMARKS_PLAN = {"celadon_city": [("CeladonCity", 31, 17, 10, 5, "the GAME CORNER (T-447 plan row 7)")],
                  "lavender_town": [("Route10", 2, 34, 11, 8, "KEEPALIVE PLANT's front (T-447 plan row 8)")]}

#  Landmarks built AFTER T-562's picks (2026-11-16): not in the plan above, because adding a box there changes the
#  families T-562's pick was cut from (and so its pixels). Instead the pick simply never writes a tile these boxes draw
#  in the engine as it stands -- they are the landmark's now (gbalandmarks).
#  the engine just before a later landmark was built: its tiles of this tool's pick are the approved pixels (the
#  family cut reads its neighbours' seams, so it no longer recomputes them byte for byte once the landmark moved in)
PICK_PIN = {"celadon_city": "4b6fa7867"}
_PIN_TILES = {}

LATER_LANDMARKS = {"celadon_city": [("CeladonCity", 9, 5, 9, 11, "VERDIGRIS DEPT. STORE (T-573)")]}


def later_landmark_tiles(ts):
    """the secondary tiles the later landmarks' cells draw in the engine now"""
    boxes = LATER_LANDMARKS.get(ts, ())
    if not boxes:
        return set()
    town = T.Town(ts)
    out = set()
    for m, x0, y0, w, h, _ in boxes:
        W = T.layouts()[m]["width"]
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                b = town.grid[m][y * W + x]
                if b >= 640:
                    out |= {(v & 0x3FF) - 640 for v in T.entries(town.mt, b - 640) if v & 0x3FF >= 640}
    return out

#  general's tiles T-542 left as pret's on purpose (gbaprimary: "4, 301 and 503, the path edges")
T542_KEPT = {4, 301, 503}
LUM_OUTLINE = 100
RESERVED = {(2, 8), (4, 1), (6, 1)}


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


#  where hue alone splits one surface: UMBRA's tan panels (13..15; ac9452 reads as orange) are one family
FAMILY = {"indigo_plateau": {(11, 13): "tan", (11, 14): "tan", (11, 15): "tan"},
          #  the SAFARI's ground greens under and between the trees (row 11's 10, 11, 13: the grass colours) are ground,
          #  not leaf -- read as leaf, the lacquer lit them into a lime line at every tree's foot (2026-11-14)
          "fuchsia_city": {(11, 10): "ground", (11, 11): "ground", (11, 13): "ground"}}


def family(c):
    r, g, b = (v / 255.0 for v in c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.16 or v < 0.12:
        return "grey"
    d = h * 360
    for name, top in (("red", 18), ("orange", 42), ("yellow", 68), ("green", 140), ("teal", 196), ("blue", 248),
                      ("purple", 290), ("pink", 340), ("red", 361)):
        if d < top:
            return name


# ================================================================== new motifs (LURID's two options, the fountain)
def m_lacquer(x, y, w, h, X, Y, b):
    """LURID A, LACQUER: the canopy as lacquered clumps -- each of the four 32-pixel clumps gets a bold hot spot at
    its upper left and a dark lip under it, the body flat between: the gloss T-438 asked for, drawn big enough to
    read at 1x"""
    if b >= 0.92:
        return b
    d, dx, dy, r = T._lobe(X, Y, T.LOBES_GLOSSY, 32)
    lit = (dx + dy) / (2 * r)
    #  the hot spot lands only where pret's leaf was already lit, the lip only where it was already in shade: so the
    #  dark rim at a tree's foot is never lit (the lime line the draft drew there, 2026-11-14)
    if d < 0.55 and lit < -0.05 and b <= 0.5:
        return 0.0
    if 0.7 < d < 1.0 and lit > 0.15 and b >= 0.3:
        return 1.0
    return b


def m_keep(x, y, w, h, X, Y, b):
    """pret's own level: the family is drawn as it was (LURID's teal ground under the trees, which is ground)"""
    return b


def m_hum(x, y, w, h, X, Y, b):
    """LURID B, THE HUM: every surface a sign that hums -- level scan bands three pixels high, a bright tube line,
    a body, a dark gap, the bands stepping a pixel every 16 across so they shimmer rather than rule"""
    k = (Y + (X // 16)) % 3
    return (0.0, 0.45, 0.9)[k]


def m_hum_wall(x, y, w, h, X, Y, b):
    """THE HUM on a frontage: one bright tube along the top, then the body, then a dark line under it"""
    if y == 1:
        return 0.0
    return 0.9 if y == h - 2 else 0.5


def m_umbra_keep(x, y, w, h, X, Y, b):
    """UMBRA, revised (the user, 2026-11-14): pret's own shading kept -- the pillars' drums and the tan panels as pret
    lit them -- and UMBRA's long shadow cut over it: past the diagonal of each 16 x 8 block, one step darker"""
    row = Y // 8
    xo, yy = (X + (8 if row % 2 else 0)) % 16, Y % 8
    return min(1.0, b + 0.4) if xo + 2 * yy > 17 else b


#  per town: family -> motif (the town's own T-438 motifs); "*" is any family not named
STYLE = {
    "viridian_city": {"red": T.m_ribs_calm, "grey": T.m_slab, "yellow": T.m_awning, "orange": T.m_boards,
                      "green": T.m_leaf, "blue": T.m_glass, "*": T.m_clapboard},
    "pewter_city": {"red": T.m_slates_calm, "blue": T.m_glass_chalk, "*": T.m_ashlar},
    "cerulean_city": {"grey": T.m_plank_long, "blue": T.m_still, "teal": T.m_still, "*": T.m_swell},
    "vermilion_city": {"red": T.m_pantile, "orange": T.m_boards, "yellow": T.m_awning_wide, "blue": T.m_glass,
                       "grey": T.m_stucco, "*": T.m_stucco},
    "lavender_town": {"blue": T.m_dots_light, "*": T.m_dots},
    "celadon_city": {"yellow": T.m_bronze, "orange": T.m_bronze, "red": T.m_band, "green": T.m_patina,
                     "teal": T.m_patina, "blue": T.m_glass, "purple": T.m_stamped, "grey": T.m_band, "*": T.m_band},
    "saffron_city": {"yellow": T.m_rivet, "orange": T.m_rivet, "grey": T.m_grid, "blue": T.m_curtain,
                     "purple": T.m_curtain, "*": T.m_stamped},
    "fuchsia_city": {"green": m_lacquer, "yellow": m_lacquer, "teal": m_keep, "ground": m_keep, "pink": T.m_stamped,
                     "purple": T.m_stamped, "*": T.m_stamped},
    "cinnabar_island": {"*": T.m_mercury},
    "indigo_plateau": {"orange": m_umbra_keep, "tan": m_umbra_keep, "*": T.m_umbra},
    "viridian_forest": {"green": T.m_canopy, "teal": T.m_canopy, "*": T.m_bark},
}
#  the real choices: {ts: [(option, DRAFT title, one line, {family: motif} overrides)]}; A is STYLE as it stands
OPTIONS = {
    "fuchsia_city": [
        ("A", "LACQUER (DRAFT)", "the SAFARI's woods as lacquered clumps, a hot spot and a dark lip each; the pens and "
                                 "rest houses in stamped panels", {}),
        ("B", "THE HUM (DRAFT)", "every frontage, pen and rest house a humming sign in level scan bands; the woods "
                                 "as A", {"pink": m_hum, "purple": m_hum, "*": m_hum_wall}),
    ],
    "celadon_city": [
        ("A", "BRONZE PANELS (DRAFT)", "the dept. store's purple front in raised stamped panels, the town's bronze "
                                       "trims and bloom around it", {}),
        ("B", "THE GREEN GLASS (DRAFT)", "the dept. store's front as a curtain wall -- mullions every eight, a "
                                         "transom every sixteen -- the rest as A", {"purple": T.m_curtain}),
    ],
}
KEEP_LIGHT = {m_umbra_keep: 0.0, m_keep: 0.0, T.m_dots: 0.0, T.m_dots_light: 0.0, m_hum: 0.0, m_hum_wall: 0.0, m_lacquer: 0.0, T.m_umbra: 0.15,
              T.m_canopy: 0.0}
FOUNTAIN_OPTIONS = [
    ("A", "THE BRONZE LIP (DRAFT)", "the basin's lip in bronze bands with a dark run every four; the jet in long "
                                    "unbroken streaks; pret's travelling ripple kept, so it moves as it did"),
    ("B", "RINGS (DRAFT)", "the jet drawn as rings that spread from its head, one step out per frame; the lip as A"),
    ("C", "STILL COLUMN (DRAFT)", "the jet as a calm column in level bands, one bright band stepping down it per "
                                  "frame (DOLDRUM's still water, in VERDIGRIS's bronze lip)"),
]


# ================================================================== the recount
def plan_boxes_tiles(town):
    out, blocks = set(), set()
    for m, x0, y0, w, h, _ in LANDMARKS_PLAN.get(town.ts, ()):
        W = T.layouts()[m]["width"]
        blocks |= {town.grid[m][y * W + x] for y in range(y0, y0 + h) for x in range(x0, x0 + w)}
    for b in blocks:
        if 640 <= b < 640 + town.nblocks:
            out |= {(v & 0x3FF) - 640 for v in T.entries(town.mt, b - 640) if v & 0x3FF >= 640}
    return out


def gen_kept_copies(town):
    """leftover tiles that are a copy (any flip) of a general tile still pret's: T-542's to decide, not ours"""
    G = town.G
    gv = {}
    for i, p in enumerate(G["van"]):
        if G["tiles"][i] != G["van"][i]:
            continue
        for f in range(4):
            q = tuple(p[(7 - k // 8 if f & 2 else k // 8) * 8 + (7 - k % 8 if f & 1 else k % 8)] for k in range(64))
            gv.setdefault(q, i)
    return {t: gv[tuple(town.van[t])] for t in town.left if tuple(town.van[t]) in gv}


def recount(ts):
    town = base_town(ts)
    left = {t for t in town.left if t not in ANIM.get(ts, ())}
    why = collections.OrderedDict()
    #  a LATER landmark's tiles (gbatowns.LANDMARKS holds it too) stay targets here, so T-562's families are cut as
    #  they were approved; picked() then never writes them
    lm = (town.kept_by_map() - later_landmark_tiles(ts)) | plan_boxes_tiles(town)
    gk = gen_kept_copies(town)
    for t in sorted(left):
        if t in town.door_tiles:
            why[t] = "door (gbadoors.py)"
        elif t + 640 in T.KEEP_TILES.get(ts, ()):
            why[t] = "kept (gbatowns KEEP_TILES)"
        elif t in T.grove_tell(ts):
            why[t] = "grove tell (gbagrove.py)"
        elif t in lm:
            why[t] = "landmark (T-447)"
        elif t in gk:
            why[t] = "general %d, left pret's by T-542" % gk[t] if gk[t] in T542_KEPT else "general %d copy" % gk[t]
    town.targets = left - set(why)
    return town, left, why


# ================================================================== the redraw
def materials(town):
    """{(row, idx): family} for every fill index a target tile uses; outlines, whites and reserved indices left out"""
    rows = collections.defaultdict(set)
    for b in range(town.nblocks):
        for v in T.entries(town.mt, b):
            t = (v & 0x3FF) - 640
            if 0 <= t < len(town.now) and t in town.targets:
                for c in set(town.van[t]) - {0}:
                    rows[v >> 12].add(c)
    out = {}
    for row, idxs in rows.items():
        pal = town.palette(row)
        dark = min(idxs, key=lambda i: lum(pal[i]))
        fam = collections.defaultdict(list)
        for i in idxs:
            if (row, i) in RESERVED or (i == dark and lum(pal[i]) < LUM_OUTLINE) or lum(pal[i]) > 246:
                continue
            fam[FAMILY.get(town.ts, {}).get((row, i)) or family(pal[i])].append(i)
        for f, ii in fam.items():
            if len(ii) >= 2:
                for i in ii:
                    out[(row, i)] = f
    return out


def ladder(town, row, mat, M):
    pal = town.palette(row)
    return sorted((i for (r, i), f in M.items() if r == row and f == mat), key=lambda i: -lum(pal[i]))


def redraw(town, style):
    new = [list(t) for t in town.now]
    what = {}
    M = materials(town)
    mat = lambda p: M.get((p[0], p[1])) if p else None
    todo = set(town.targets)
    for obj in town.objects(todo):
        if not todo:
            break
        for layer in (0, 1):
            P = T.Plane(town, obj, layer, town.van if len(town.van) == len(town.now) else
                        [town.van[i] if i < len(town.van) else town.now[i] for i in range(len(town.now))])
            region = {}
            for Y in range(P.h):
                for X in range(P.w):
                    m = mat(P.px[Y][X])
                    if m is None or (X, Y) in region:
                        continue
                    st, grp = [(X, Y)], []
                    region[(X, Y)] = None
                    while st:
                        a, c = st.pop()
                        grp.append((a, c))
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            u, v = a + dx, c + dy
                            if 0 <= u < P.w and 0 <= v < P.h and (u, v) not in region and mat(P.px[v][u]) == m:
                                region[(u, v)] = None
                                st.append((u, v))
                    xs, ys = [a for a, _ in grp], [c for _, c in grp]
                    box = (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
                    for g in grp:
                        region[g] = box
            claimed = {}
            for Y in range(P.h):
                for X in range(P.w):
                    p = P.px[Y][X]
                    if not p or p[2] is None or p[2] not in todo:
                        continue
                    row, idx, t, k = p
                    m = mat(p)
                    if m is None:
                        continue
                    edge = False
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        u, v = X + dx, Y + dy
                        if not (0 <= u < P.w and 0 <= v < P.h) or P.px[v][u] is None:
                            edge = True                     # the footprint's own edge
                            break
                        n = mat(P.px[v][u])
                        if n is not None and n != m:
                            edge = True                     # a join with another family: a sill, an eave
                            break
                    if edge:
                        continue
                    lad = ladder(town, row, m, M)
                    base = lad.index(idx) / (len(lad) - 1)
                    f = style.get(m, style["*"])
                    rx, ry, rw, rh = region[(X, Y)]
                    lv = f(X - rx, Y - ry, rw, rh, X, Y, base)
                    if isinstance(lv, tuple):
                        lv = lv[0]
                    keep = KEEP_LIGHT.get(f, 0.25)
                    lv = max(0.0, min(1.0, (1 - keep) * lv + keep * base))
                    claimed.setdefault(t, {})[k] = lad[int(round(lv * (len(lad) - 1)))]
            for t, pix in claimed.items():
                if t in what:
                    continue
                for k, v in pix.items():
                    new[t][k] = v
                what[t] = "%s @%d,%d" % (obj["map"], obj["box"][0], obj["box"][1])
        todo -= set(what)
    for t in range(len(new)):
        if any((a == 0) != (b == 0) for a, b in zip(new[t], town.now[t])):
            raise SystemExit("  !! %s tile %d: footprint moved" % (town.ts, t))
    return new, what


def styles(ts):
    base = dict(STYLE[ts])
    opts = OPTIONS.get(ts) or [("A", None, None, {})]
    return [(o[0], o[1], o[2], dict(base, **o[3])) for o in opts]


# ================================================================== the fountain (5 frames, 8 tiles each, row 8)
def fountain(option, k):
    im = Image.open(io.BytesIO(T.daemonslib.upstream(GBA, FOUNTAIN % k, binary=True))).convert("P")
    w, h = im.size
    px = im.load()
    src = [[px[x, y] & 15 for x in range(w)] for y in range(h)]
    out = [r[:] for r in src]
    JET = [5, 6, 13]                                 # the jet's own blues, light .. dark; 7 and 8 (its shaded
    LIP = [10, 11]                                   #   sides and the basin) keep pret's pixels, so it keeps its form
    jet = lambda c: c in JET or c == 1               # the bronze lip, light .. dark (12 is its blue-grey shadow)
    for y in range(h):
        for x in range(w):
            c = src[y][x]
            nb = [src[y + dy][x + dx] if 0 <= x + dx < w and 0 <= y + dy < h else 0
                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if c in LIP and all(n in LIP + [12, 3] for n in nb if n):
                out[y][x] = LIP[1] if x % 4 == 3 else LIP[0]           # bronze bands, a dark run every four
                continue
            if not jet(c) or any(n == 0 or not jet(n) for n in nb):
                continue                                               # the jet's outline and shading stay
            if option == "A":
                if c == 1:
                    continue                                           # pret's ripple, so it travels as before
                lane = T._h(x // 2, 31)
                out[y][x] = JET[2] if (x % 5 == 1 or lane < 0.2) else (JET[0] if lane > 0.75 else JET[1])
            elif option == "B":
                d = ((x - 7.5) ** 2 + ((y - 6) * 0.9) ** 2) ** 0.5
                out[y][x] = JET[int(d - 1.5 * k) % 3]
            else:
                band = y // 3
                out[y][x] = JET[0] if band == (2 + 2 * k) % 11 else (JET[1] if band % 2 else JET[2])
    o = Image.new("P", (w, h))
    o.putpalette(im.getpalette()[:48])
    o.putdata([v for r in out for v in r])
    return o, src, out


# ================================================================== pictures
def tile_img(pix, pal, Z=4):
    im = Image.new("RGB", (8, 8), (255, 0, 255))
    for k, v in enumerate(pix):
        if v:
            im.putpixel((k % 8, k // 8), pal[v])
    return im.resize((8 * Z, 8 * Z), Image.NEAREST)


def tile_sheet(town, news, path, title):
    """every changed tile at 4x, today beside each option"""
    rows = collections.Counter()
    for b in range(town.nblocks):
        for v in T.entries(town.mt, b):
            if v & 0x3FF >= 640:
                rows[((v & 0x3FF) - 640, v >> 12)] += 1 + town.placed.get(640 + b, 0)
    changed = sorted({t for _, new in news for t in range(len(new)) if new[t] != town.now[t]})
    f = T.font(11)
    cols = 6
    cell_w = 34 * (1 + len(news)) + 14
    W = cols * cell_w + 16
    H = 46 + ((len(changed) + cols - 1) // cols) * 58
    out = Image.new("RGB", (W, max(H, 80)), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), title, font=T.font(13), fill=(20, 20, 20))
    d.text((8, 24), "each cell: today | " + " | ".join(o for o, _ in news) + "   (4x, the tile's commonest palette row)",
           font=f, fill=(60, 60, 60))
    for n, t in enumerate(changed):
        row = max((r for (tt, r) in rows if tt == t), key=lambda r: rows[(t, r)], default=8)
        pal = town.palette(row)
        x, y = 8 + (n % cols) * cell_w, 46 + (n // cols) * 58
        d.text((x, y), "%d r%d" % (t, row), font=f, fill=(30, 30, 30))
        out.paste(tile_img(town.now[t], pal), (x, y + 14))
        for j, (_, new) in enumerate(news):
            out.paste(tile_img(new[t], pal), (x + 34 * (j + 1), y + 14))
    out.save(path)
    return path, len(changed)


def fountain_sheet(path):
    town = T.Town("celadon_city")
    pal = town.palette(8)
    Z = 6
    f = T.font(12)
    rows = [("today (pret's)", [fountain("A", k)[1] for k in range(5)])]
    for o, title, line in FOUNTAIN_OPTIONS:
        rows.append(("%s  %s -- %s" % (o, title, line), [fountain(o, k)[2] for k in range(5)]))
    W, H = max(5 * (16 * Z + 12) + 24, 900), len(rows) * (32 * Z + 34) + 30
    out = Image.new("RGB", (W, H), T.BG)
    d = ImageDraw.Draw(out)
    d.text((8, 6), "T-562 VERDIGRIS's fountain, 5 frames at %dx (row 8; tiles 744-751 by the animation)" % Z, font=f,
           fill=(20, 20, 20))
    y = 28
    for name, frames in rows:
        d.text((8, y), name[:150], font=T.font(11), fill=(30, 30, 30))
        for k, fr in enumerate(frames):
            im = Image.new("RGB", (16, 32), (124, 192, 104))
            for yy in range(32):
                for xx in range(16):
                    if fr[yy][xx]:
                        im.putpixel((xx, yy), pal[fr[yy][xx]])
            out.paste(im.resize((16 * Z, 32 * Z), Image.NEAREST), (12 + k * (16 * Z + 12), y + 16))
        y += 32 * Z + 34
    out.save(path)
    return path


def save_tiles(town, new, path):
    T.save_tiles(town, new, path)


# ================================================================== main
def run(draft_dir=None, seams=False):
    total = collections.Counter()
    report = {}
    for ts, name in TOWNS:
        town, left, why = recount(ts)
        opts = styles(ts)
        news = []
        for o, title, line, st in opts:
            new, what = redraw(town, st)
            news.append((o, new))
        ch = [sum(1 for t in range(len(n)) if n[t] != town.now[t]) for _, n in news]
        untouched = sorted(town.targets - {t for t in range(len(news[0][1])) if news[0][1][t] != town.now[t]})
        print("\n  %-40s %-16s %3d left (census method)  excluded %d  targets %d  redrawn %s  unchanged %d" % (
            name, ts, len(left), len(why), len(town.targets), "/".join("%s %d" % (o, c) for (o, _), c in
                                                                        zip(news, ch)), len(untouched)))
        for r, n in collections.Counter(why.values()).items():
            print("        excluded: %-40s %d" % (r, n))
        rep = dict(name=name, left=len(left), excluded={str(t): w for t, w in why.items()},
                   targets=len(town.targets), redrawn={o: c for (o, _), c in zip(news, ch)}, unchanged=untouched,
                   options=[dict(option=o, title=tt, line=ln) for o, tt, ln, _ in opts if tt])
        if seams:
            sm = {}
            for o, new in news:
                a, b, added = T.seams(town, new)
                sm[o] = dict(today=a, draft=b, added=added)
                print("        seams %s: %d today -> %d draft%s" % (o, a, b, ("; new: " + "; ".join(added[:4]))
                                                                     if added else ""))
            rep["seams"] = sm
        if draft_dir:
            d = os.path.join(draft_dir, ts)
            os.makedirs(d, exist_ok=True)
            for o, new in news:
                save_tiles(town, new, os.path.join(d, "tiles.png" if o == "A" else "tiles_%s.png" % o))
            p, n = tile_sheet(town, news, os.path.join(draft_dir, "sheets", "t562_tiles_%s.png" % ts),
                              "T-562 %s (%s): %d tiles changed -- DRAFT" % (name, ts, max(ch)))
            print("        wrote %s" % p)
        report[ts] = rep
        total["left"] += len(left)
        total["targets"] += len(town.targets)
        total["redrawn"] += ch[0]
    print("\n  all eleven: %d left, %d targets, %d redrawn in option A" % (total["left"], total["targets"],
                                                                          total["redrawn"]))
    if draft_dir:
        for o, _, _ in FOUNTAIN_OPTIONS:
            d = os.path.join(draft_dir, "celadon_city", "fountain_%s" % o)
            os.makedirs(d, exist_ok=True)
            for k in range(5):
                fountain(o, k)[0].save(os.path.join(d, "%d.png" % k), bits=4)
        print("        wrote %s" % fountain_sheet(os.path.join(draft_dir, "sheets", "t562_fountain.png")))
        json.dump(dict(ticket="T-562", status="DRAFT -- nothing approved (APPROVED is empty)", towns=report,
                       fountain=[dict(option=o, title=t, line=l) for o, t, l in FOUNTAIN_OPTIONS]),
                  open(os.path.join(draft_dir, "draft.json"), "w"), indent=1)


def picked(ts, option):
    """(town, {tile: pixels}) -- the tiles this tool draws for this pick, read from BASE, and nothing else"""
    town, _, _ = recount(ts)
    st = [s for s in styles(ts) if s[0] == option[0]][0][3]
    new, _ = redraw(town, st)
    later = later_landmark_tiles(ts)
    mine = {t: new[t] for t in range(len(new)) if new[t] != town.now[t] and t not in later}
    if ts in PICK_PIN:                                 # T-562's pixels as built, before a later landmark moved its seams
        if (ts, PICK_PIN[ts]) not in _PIN_TILES:
            _PIN_TILES[(ts, PICK_PIN[ts])] = T.tiles_of(Image.open(io.BytesIO(T.daemonslib.upstream(
                GBA, T.SEC + ts + "/tiles.png", binary=True, ref=PICK_PIN[ts]))))
        pinned = _PIN_TILES[(ts, PICK_PIN[ts])]
        mine = {t: list(pinned[t]) for t in mine}
    return town, mine


def engine_tiles(town, mine):
    """the engine's tiles.png as it stands, with this tool's tiles laid over it (every other tile is left as it is)"""
    out = [list(t) for t in town.disk]
    for t, p in mine.items():
        out[t] = list(p)
    return out


def frames_on_disk():
    out = []
    for k in range(5):
        im = Image.open(os.path.join(GBA, FOUNTAIN % k)).convert("P")
        out.append([[v & 15 for v in im.getdata()]])
    return out


def check_engine():
    """the approved picks against the engine: 0 when every approved tile and frame is in it as drawn"""
    bad = 0
    for ts, option in APPROVED.items():
        town, mine = picked(ts, option)
        miss = sorted(t for t, p in mine.items() if town.disk[t] != p)
        print("  engine %-16s pick %-2s %3d tiles%s" % (ts, option, len(mine),
                                                       "  DIFFERS at %s" % miss[:12] if miss else "  as approved"))
        bad += bool(miss)
        if ts == "celadon_city" and len(option) > 1:
            want = [[v for r in fountain(option[1], k)[2] for v in r] for k in range(5)]
            have = [f[0] for f in frames_on_disk()]
            same = want == have
            print("  engine fountain         pick %s   5 frames  %s" % (option[1], "as approved" if same else "DIFFERS"))
            bad += not same
    return bad


# ================================================================== T-438: TRAINER TOWER's interior (DRAFT)
#  TRAINER TOWER on SEVEN ISLAND (trainer_tower: the lobby, eight floors, the roof) is the USER TOWER of vision 6.x --
#  "the post-game's tests are the USER TOWER and the Review Board rematch". Its OUTSIDE is a T-447 landmark that is the
#  user's (the user's one direction so far, 2026-10-24: "progress bars, each floor a band with a teal bar"), and
#  stays out of every batch. Its INSIDE was never redrawn: 298 of 306 tiles still pret's. This drafts it as its own
#  T-438 batch with this tool's method (families by hue, each drawn in a motif; outlines, whites, joins, footprints
#  kept; no block, row, flip, behaviour, collision or map moves), three looks from what the place is:
#
#    python3 tools/gbatownslast.py --tower [DIR]       # report + drafts into DIR (gfx/drafts/t438/trainer_tower/):
#                                                      #   tiles_A/B/C.png, draft.json, a 4x sheet of every changed tile
#    python3 tools/gbatownslast.py --tower --write --approved   # APPROVED_TOWER's option into the engine. None until
#                                                      #   the user picks: refused, nothing written.
#
#  A USER climbs it against the clock, floor after floor, and the time is posted -- a run, measured. So:
#    A PROGRESS: the floors laid as rows of progress bars, each bar outlined and filled two thirds -- the climb as a
#      job running; the walls one band with a lit bar along it (the user's own words for the outside, carried in)
#    B THE LEADERBOARD: the floors ruled as a table of times, a rule every eight rows and a column every thirty-two;
#      the walls raised panels like a scoreboard's slats
#    C THE RUN: the floors as running lanes, a dashed line down every lane; the walls smeared lengthwise (THE STREAK)
#  In every look the lobby floor's three ball emblems (pret's, tiles 148-151 / 164-167) are taken up and the floor laid
#  over them; the gates' floor-count dots (one to eight, a different block per floor) are kept: they already count.
TOWER_TS = "trainer_tower"
TOWER_DRAFT = os.path.join(ROOT, "gfx", "drafts", "t438", "trainer_tower")
APPROVED_TOWER = None       # "A", "B" or "C" once the user picks -- None: --tower --write --approved writes nothing
#  the ball emblem's tiles -> the plain floor tile at the same place in the 16x16 floor (block 0x281: 1 2 / 17 18)
TOWER_EMBLEM = {148: 2, 149: 1, 150: 2, 151: 1, 164: 18, 165: 17, 166: 18, 167: 17}


#  THE FLOORS' PERIOD: the yellow floor is one 8x8 tile laid everywhere, and the lobby's blue floor four tiles that its
#  emblem blocks also lay mirrored (0x2d3 = 149 | 149 flipped), so a floor motif must repeat every eight and read the
#  same mirrored, or the emblems' places would show as seams (draft 1 did, 2026-11-18).
def m_segments(x, y, w, h, X, Y, b):
    """A: the floor as the lit segments of a progress bar -- six-pixel cells, two-pixel gaps between, a dark rule
    under each row of them"""
    xo, yo = X % 8, Y % 8
    if yo == 7:
        return 0.85
    if xo in (0, 7):
        return 0.55
    return 0.0 if 1 <= yo <= 5 else 0.3


def m_wallbar(x, y, w, h, X, Y, b):
    """A: the walls one band, a lit bar along its middle two rows (the user's words for the outside)"""
    mid = h // 2
    if y in (mid - 1, mid):
        return 0.0
    if y == mid + 1:
        return 1.0
    return 0.5


def m_table(x, y, w, h, X, Y, b):
    """B: a table of times: a rule every eight rows, the rows between plain"""
    if Y % 8 == 7:
        return 0.8
    return 0.35 if Y % 8 == 0 else 0.1


def m_lanes(x, y, w, h, X, Y, b):
    """C: running lanes eight wide, a dashed line down the middle of every lane"""
    if Y % 8 == 7:
        return 0.8
    if Y % 8 == 3 and 2 <= X % 8 <= 5:
        return 0.0
    return 0.4


for _f in (m_segments, m_wallbar, m_table, m_lanes):
    KEEP_LIGHT[_f] = 0.0
#  the families are named by role, not hue: the floors (yellow rows 8 and 12, the lobby's blue row 10) and the walls
#  (the lobby's purple, the floors' grey-blue) would otherwise share "blue". Everything else -- the pillars, stairs,
#  machines, plants -- keeps pret's drawing (m_keep); the counters (orange, red) take steel panels in every look.
FAMILY["trainer_tower"] = {}
for _r in (8, 12):
    for _i in range(9, 14):
        FAMILY["trainer_tower"][(_r, _i)] = "floor"
for _i in range(1, 6):
    FAMILY["trainer_tower"][(10, _i)] = "floor"
for _i in range(11, 16):
    FAMILY["trainer_tower"][(9, _i)] = "wall"
for _i in range(5, 9):
    FAMILY["trainer_tower"][(8, _i)] = "wall"
def m_ticks(x, y, w, h, X, Y, b):
    """A's furniture: every grey thing -- the pillars, stairs, machines, the lobby's fittings -- as a vertical progress
    meter: segments four pixels deep, a lit top edge, the body, a dark gap; pret's own light kept under it a little.
    A region two pixels wide or less (the rooms' white edge, a rail) is a line, not a thing: kept (draft 1 dotted it)"""
    if w <= 2:
        return b
    yo = Y % 4
    if yo == 3:
        return min(1.0, b + 0.5)
    if yo == 0:
        return max(0.0, b - 0.35)
    return b


def m_floorbands(x, y, w, h, X, Y, b):
    """the roof's view of the tower's own face: pret's texture kept, and across it one band a storey (sixteen rows),
    a lit bar two rows deep over a dark line -- the user's "each floor a band with a teal bar", in the face's own blues"""
    yo = Y % 16
    if yo in (6, 7):
        return 0.0
    if yo == 8:
        return 1.0
    return b


KEEP_LIGHT[m_ticks] = 0.0
KEEP_LIGHT[m_floorbands] = 0.0
#  the user, 2026-11-18 (by multiple choice): A PROGRESS; put pret's shadow under the walls back; then the furniture
#  in the same look, sheet first. B THE LEADERBOARD and C THE RUN were not picked (their drafts are in DAEMONS de5b21e9).
_TOWER_REST = {"orange": T.m_panel, "red": T.m_panel, "*": m_keep}
_TOWER_A = dict(_TOWER_REST, floor=m_segments, wall=m_wallbar)
TOWER_OPTIONS = [
    ("A", "PROGRESS (DRAFT)", "the floors as the lit segments of a progress bar, pret's shadow along the walls' foot "
                              "kept as the same segments a step or two darker; the walls a band with a lit bar along "
                              "it -- the user's words for the outside, carried in", _TOWER_A),
    ("AF", "PROGRESS, FURNISHED (DRAFT)", "A, and the furniture in the same language: every grey thing (pillars, "
                                          "stairs, machines) a vertical meter of four-pixel segments; the plants in "
                                          "bold leaves; the roof's view of the tower's own face kept as pret drew it "
                                          "(the outside is a landmark, the user's)",
     dict(_TOWER_A, grey=m_ticks, green=T.m_leaf)),
    ("AFB", "FURNISHED, THE FACE BANDED (DRAFT)", "AF, and the roof's view of the tower's face given one band a "
                                                  "storey, a lit bar over a dark line, pret's texture kept between",
     dict(_TOWER_A, grey=m_ticks, green=T.m_leaf, blue=m_floorbands)),
]
#  the shadow (A): pret drew the floor's shadow under a wall as the same tile one rank darker (3/4/19/20 for the
#  lobby's 1/2/17/18, 191 for the yellow floor's 190, and 206 half of each). Each floor pixel keeps that offset: its
#  rank in pret's tile minus its rank in the plain floor tile, laid onto the new segments
TOWER_PLAIN = {8: [190], 10: [1, 2, 17, 18]}


def tower_shadow(town, new):
    M = materials(town)
    rows = collections.defaultdict(set)
    for b in range(town.nblocks):
        for v in T.entries(town.mt, b):
            if v & 0x3FF >= 640:
                rows[(v & 0x3FF) - 640].add(v >> 12)
    n = 0
    for t in sorted(town.targets):
        r = next((r for r in sorted(rows[t]) if r in TOWER_PLAIN), None)
        if r is None:
            continue
        lad = ladder(town, r, "floor", M)
        rk = lambda c: lad.index(c) if c in lad else None
        best = min(TOWER_PLAIN[r], key=lambda P: sum(abs((rk(a) or 0) - (rk(c) or 0))
                                                   for a, c in zip(town.van[t], town.van[P])
                                                   if rk(a) is not None and rk(c) is not None))
        out = list(new[t])
        for k, (a, c) in enumerate(zip(town.van[t], town.van[best])):
            if rk(a) is None or rk(c) is None or rk(out[k]) is None:
                continue
            d = rk(a) - rk(c)
            if d > 0:
                out[k] = lad[min(len(lad) - 1, rk(out[k]) + d)]
        if out != new[t]:
            new[t] = out
            n += 1
    return n


def tower_town():
    """recount(TOWER_TS), the emblems' tiles first laid as plain floor (now and vanilla), so the floor runs over them"""
    town, left, why = recount(TOWER_TS)
    town.van = [list(p) for p in town.van]
    for t, f in TOWER_EMBLEM.items():
        town.now[t] = list(town.now[f])
        town.van[t] = list(town.van[f])
    return town, left, why


def tower_draw(option):
    town, left, why = tower_town()
    st = [o[3] for o in TOWER_OPTIONS if o[0] == option][0]
    new, what = redraw(town, st)
    tower_shadow(town, new)
    disk = [list(p) for p in town.disk]
    return town, left, why, {t: new[t] for t in range(len(new)) if new[t] != disk[t]}


def main_tower():
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED_TOWER:
            print("  --tower --write refused: --write needs --approved, and APPROVED_TOWER names no option the user "
                  "has picked. Nothing written.")
            return 0
        town, _, _, mine = tower_draw(APPROVED_TOWER)
        out = engine_tiles(town, mine)
        if out == town.disk:
            print("  %s: already drawn, nothing to write" % TOWER_TS)
        else:
            save_tiles(town, out, os.path.join(town.dir, "tiles.png"))
            print("  wrote %s (option %s): %d tiles" % (TOWER_TS, APPROVED_TOWER, len(mine)))
        return 0
    i = ARGS.index("--tower")
    d = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else None
    news, rep = [], {}
    for o, title, line, _ in TOWER_OPTIONS:
        town, left, why, mine = tower_draw(o)
        tl = [list(p) for p in town.disk]
        for t, p in mine.items():
            tl[t] = list(p)
        news.append((o, tl))
        rep[o] = dict(title=title, line=line, tiles=len(mine),
                      still_pret=sorted(t for t in town.targets if t not in mine))
    pret = sorted(t for t in left if t not in why)
    print("  TRAINER TOWER (%s): %d tiles a reachable map draws are still pret's; excluded %d (%s); targets %d" % (
        TOWER_TS, len(left), len(why), ", ".join("%s %d" % kv for kv in collections.Counter(why.values()).items()),
        len(pret)))
    for o, title, line, _ in TOWER_OPTIONS:
        print("      %-2s %-28s %3d tiles redrawn, %3d of the targets still pret's  %s" % (
            o, title, rep[o]["tiles"], len(rep[o]["still_pret"]), line[:70]))
    if d:
        os.makedirs(os.path.join(d, "sheets"), exist_ok=True)
        town = T.Town(TOWER_TS)
        for o, tl in news:
            moved = [t for t in range(len(tl)) if any((a == 0) != (b == 0) for a, b in zip(tl[t], town.disk[t]))]
            if moved:
                raise SystemExit("  !! option %s: footprints moved at %s" % (o, moved[:12]))
            save_tiles(town, tl, os.path.join(d, "tiles_%s.png" % o))
        p, n = tile_sheet(town, news, os.path.join(d, "sheets", "t438_tower_tiles.png"),
                          "T-438 TRAINER TOWER's interior: every changed tile at 4x -- DRAFT")
        print("        wrote %s" % p)
        json.dump(dict(ticket="T-438 (TRAINER TOWER's interior)", status="DRAFT -- nothing approved "
                       "(APPROVED_TOWER is None)", left=len(left), excluded={str(t): w for t, w in why.items()},
                       targets=len(pret), options=rep, emblem_floor=TOWER_EMBLEM),
                  open(os.path.join(d, "draft.json"), "w"), indent=1)
    return 0


def main():
    if "--tower" in ARGS:
        return main_tower()
    if "--write" in ARGS:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: --write needs --approved, and APPROVED names no town the user has picked. "
                  "Nothing written.")
            return 0
        for ts, option in APPROVED.items():
            town, mine = picked(ts, option)
            out = engine_tiles(town, mine)
            if out == town.disk:
                print("  %s: already drawn (%d tiles), nothing to write" % (ts, len(mine)))
            else:
                if any((a == 0) != (b == 0) for t in mine for a, b in zip(out[t], town.disk[t])):
                    raise SystemExit("  !! %s: a footprint moved -- nothing written" % ts)
                save_tiles(town, out, os.path.join(town.dir, "tiles.png"))
                print("  wrote %s (option %s): %d tiles" % (ts, option, sum(out[t] != town.disk[t]
                                                                          for t in range(len(out)))))
            if ts == "celadon_city" and len(option) > 1:
                have = [f[0] for f in frames_on_disk()]
                n = 0
                for k in range(5):
                    im, _, px = fountain(option[1], k)
                    if [v for r in px for v in r] != have[k]:
                        im.save(os.path.join(GBA, FOUNTAIN % k), bits=4)
                        n += 1
                print("  VERDIGRIS's fountain, option %s: %s" % (option[1], "%d frames written" % n if n
                                                                 else "already drawn, nothing to write"))
        return 0
    if "--draft" in ARGS:
        i = ARGS.index("--draft")
        d = ARGS[i + 1] if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--") else DRAFT_DEFAULT
        os.makedirs(os.path.join(d, "sheets"), exist_ok=True)
        run(d, seams=True)
        return 0
    run(None, seams="--seams" in ARGS)
    bad = check_engine()
    print("  the engine %s" % ("matches every approved pick" if not bad else "DIFFERS from %d approved picks" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
