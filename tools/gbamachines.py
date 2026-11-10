#!/usr/bin/env python3
"""The desks and machines: what T-438 batch D left vanilla in primary/building, redrawn in place (T-537).

    python3 tools/gbamachines.py                    # report: every still-vanilla drawn tile of primary/building, by
                                                    #   object -- tiles, the blocks that place it, how many maps show
                                                    #   it -- which of them this ticket redraws, and the ids the
                                                    #   engine names
    python3 tools/gbamachines.py --draft [DIR]      # the three directions (A, B, C) drawn in full: per direction the
                                                    #   tiles.png and the optional blink frames, and the contact sheets
                                                    #   (gfx/drafts/t537/)
    python3 tools/gbamachines.py --write --approved --pick X
                                                    # into the engine -- refused unless X is in APPROVED ({"A"}:
                                                    #   the user, 2026-11-09). Report mode compares the engine with
                                                    #   that write and exits 1 on a difference (T-446's rule)

THE ANSWER IT FOLLOWS (the user, 2026-11-09, from the vanilla-art census): "the desks and machines" -- the pieces of
primary/building that T-438 batch D (gbabuilding.py) left for later: SILPH's two-row reception desk, the striped
desks, the boardroom table, the POWER PLANT's and the labs' machines and benches. They stand in FOUNDRY CO.'s rooms,
which T-536 has just redrawn (gbaoffice.py, C THE FOUNDRY: cast iron, bronze, a little furnace glow), AND in the labs,
the POWER PLANT, the MANSION, the SEA COTTAGE, the bike shop, the SAFARI houses and BRAZEN's copycat house -- so each
direction has to read in a foundry and in somebody's front room.

THE RULES ARE BATCH D'S (gbabuilding.py). Redrawn IN PLACE: no block, layer, flip, palette row, behaviour or collision
bit moves and no map is touched; only pixels inside tiles change, and every tile keeps its FOOTPRINT (a transparent
pixel stays transparent, a drawn one stays drawn). Primary rows 0..2 are batch D's approved timber rows and are shared
by every interior: nothing here changes a colour. Each tile is drawn in the colours of the row(s) that place it --
the reception desk's tiles are placed in rows 0 AND 1, whose indices mean different colours, so they are matched
against both at once. Tiles 262..266 (CHECKPOINT 2F's pots) are never touched.

HOW IT IS DRAWN. Each object is a canvas laid out as it stands -- from the sheet where vanilla drew it standing, or
from the one map that assembles it (the boardroom table from FOUNDRY 11F, mirrored halves and all; the reception desk
from 1F) -- and is drawn fresh in named MATERIALS inside its footprint: vanilla's silhouette says only where pixels
may go. Each direction maps the materials onto colours; every tile is then matched, pixel by pixel, to the nearest of
its own row's fifteen colours. The look is batch D's: seen from above and the south, a lit top over a darker front,
light from the upper left, bold forms that read at 1x.

THE ENGINE NAMES ONE THING HERE: METATILE_Building_PCOff/PCOn (0x062/0x063, field_specials.c) -- the PORT, already
ours (batch D), not touched. No script sets a building block below 0x280. gTileset_Building has NO animation callback
(src/data/tilesets/headers.h), so vanilla's "blinking" machines never blinked: their lights are painted. A blink is
offered as an option (the frames are drafted) and would cost engine code -- see BLINK.

Every in-game word: none. This is art.
"""
import collections, contextlib, io, json, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t537")
#  The user's pick goes here ("A", "B" or "C"); --write refuses anything not in it.
APPROVED = {"A"}                                  # the user, 2026-11-09: A Foundry stock, no blink

ARGS = sys.argv[1:]
WRITE = "--write" in ARGS

#  gbabuilding reads its own switches off sys.argv at import (engine.md trap 16): import it under a clean argv.
_argv, sys.argv = sys.argv, ["gbabuilding"]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import gbabuilding as GB
finally:
    sys.argv = _argv

GBA, PD, BPATH = GB.GBA, GB.PD, GB.B          # (B is direction B below)


def argval(flag):
    if flag in ARGS:
        i = ARGS.index(flag)
        if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--"):
            return ARGS[i + 1]
        return ""
    return None


DRAFT = argval("--draft")
if DRAFT == "":
    DRAFT = DRAFT_DEFAULT
PICK = argval("--pick")

USE = GB.scan()
VAN, CUR, BASE, PALS, NT = GB.VAN, GB.CUR, GB.BASE, GB.PALS, GB.NT


def still_vanilla():
    """every tile a map draws whose pixels are still exactly vanilla's, and which is more than one flat colour"""
    return sorted(t for t in USE if CUR[t] == VAN[t] and any(CUR[t]) and t not in GB.KEEP and len(set(CUR[t])) > 1)


# ================================================================== reading a map's blocks
_LAYOUTS = None


def _layout(mapname):
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    lid = json.load(open(os.path.join(GBA, "data/maps", mapname, "map.json")))["layout"]
    return next(l for l in _LAYOUTS if l.get("id") == lid)


def _entries(l, mid):
    if mid < 640:
        return struct.unpack_from("<8H", GB.BMT, mid * 16)
    md = GB.metatiles_dir(l["secondary_tileset"])
    return struct.unpack_from("<8H", open(os.path.join(GBA, md, "metatiles.bin"), "rb").read(), (mid - 640) * 16)


def map_layout(mapname, x0, y0, w, h, tiles):
    """the object as the map assembles it: per 8x8 cell the entry (top layer first) whose tile is one of TILES"""
    l = _layout(mapname)
    data = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    out = [[None] * (w * 2) for _ in range(h * 2)]
    for cy in range(h):
        for cx in range(w):
            mid = struct.unpack_from("<H", data, ((y0 + cy) * l["width"] + x0 + cx) * 2)[0] & 0x3FF
            e = _entries(l, mid)
            for sub in range(4):
                for k in (4 + sub, sub):
                    t = e[k] & 0x3FF
                    if t in tiles:
                        fl = ("h" if e[k] & 0x400 else "") + ("v" if e[k] & 0x800 else "")
                        out[cy * 2 + sub // 2][cx * 2 + sub % 2] = (t, fl) if fl else t
                        break
    return out


def H(t):
    return (t, "h")


# ================================================================== the canvas: materials, not indices
class Cv:
    """an object laid out as it stands; painters write MATERIAL names, never indices, and only inside the footprint"""

    def __init__(self, layout):
        self.layout = layout
        self.th, self.tw = len(layout), max(len(r) for r in layout)
        self.w, self.h = self.tw * 8, self.th * 8
        self.van = [[0] * self.w for _ in range(self.h)]
        self.hole = [[True] * self.w for _ in range(self.h)]
        for ty, r in enumerate(layout):
            for tx, spec in enumerate(r):
                if spec is None:
                    continue
                t, fl = (spec, "") if isinstance(spec, int) else spec
                for k in range(64):
                    x, y = k % 8, k // 8
                    sx = 7 - x if "h" in fl else x
                    sy = 7 - y if "v" in fl else y
                    self.van[ty * 8 + y][tx * 8 + x] = BASE[t][sy * 8 + sx]
                    self.hole[ty * 8 + y][tx * 8 + x] = False
        self.out = [[None] * self.w for _ in range(self.h)]

    def foot(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and not self.hole[y][x] and self.van[y][x] != 0

    def px(self, x, y, m):
        if self.foot(x, y):
            self.out[y][x] = m

    def rect(self, x0, y0, x1, y1, m):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, m)

    def hline(self, x0, x1, y, m):
        self.rect(x0, y, x1, y, m)

    def vline(self, x, y0, y1, m):
        self.rect(x, y0, x, y1, m)

    def fill(self, m):
        self.rect(0, 0, self.w - 1, self.h - 1, m)

    def edge(self, x, y):
        """a footprint pixel beside a transparent one (the canvas edge is not an edge: the object goes on there)"""
        return self.foot(x, y) and any(0 <= x + dx < self.w and 0 <= y + dy < self.h and not self.hole[y + dy][x + dx]
                                       and self.van[y + dy][x + dx] == 0
                                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    def rim(self, m="ol"):
        for x, y in [(x, y) for y in range(self.h) for x in range(self.w) if self.edge(x, y)]:
            self.out[y][x] = m

    def span(self, y):
        """the footprint's first and last x on row y (None if empty)"""
        xs = [x for x in range(self.w) if self.foot(x, y)]
        return (xs[0], xs[-1]) if xs else None

    def vspan(self, x):
        ys = [y for y in range(self.h) if self.foot(x, y)]
        return (ys[0], ys[-1]) if ys else None

    def bbox(self):
        pts = [(x, y) for y in range(self.h) for x in range(self.w) if self.foot(x, y)]
        return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

    def tiles(self):
        """tile id -> its 64 materials, unmirrored; the first placement of a tile wins"""
        res = {}
        for ty, r in enumerate(self.layout):
            for tx, spec in enumerate(r):
                if spec is None:
                    continue
                t, fl = (spec, "") if isinstance(spec, int) else spec
                if t in res:
                    continue
                px = [None] * 64
                for y in range(8):
                    for x in range(8):
                        sx = 7 - x if "h" in fl else x
                        sy = 7 - y if "v" in fl else y
                        px[sy * 8 + sx] = self.out[ty * 8 + y][tx * 8 + x]
                res[t] = px
        return res


def rows_of(t):
    """the palette rows a tile is placed in, weighted by how often"""
    u = USE.get(t)
    return dict(u["rows"]) if u and u["rows"] else {0: 1}


def quantize(t, mats, D):
    """the 64 indices for tile t: each material's colour matched to the nearest of the tile's rows' colours, summed
    over every row the tile is placed in; the footprint exactly (0 stays 0, drawn stays 1..15)"""
    rows = rows_of(t)
    cache = {}
    px = []
    for k, m in enumerate(mats):
        if BASE[t][k] == 0:
            px.append(0)
            continue
        if m is None:
            m = "ol"
        if m not in cache and isinstance(D["mat"][m], tuple) and D["mat"][m][0] == "idx":
            cache[m] = D["mat"][m][1]
        if m not in cache:
            c = D["mat"][m]
            cache[m] = min(range(1, 16), key=lambda i: sum(
                w * sum((a - b) ** 2 for a, b in zip(PALS[r][i], c)) for r, w in rows.items()))
        px.append(cache[m])
    return px


# ================================================================== drawing kit
def box_front(K, x0, x1, y0, y1, face="case", dark="caseD", lit="caseL"):
    """a cabinet's front: a lit left edge, a dark right edge, the face between"""
    K.rect(x0, y0, x1, y1, face)
    K.vline(x0, y0, y1, lit)
    K.vline(x1, y0, y1, dark)


def lamp(K, x, y, D, on=True):
    K.px(x, y, "lampOn" if on else "lampOff")
    if D["style"] == "A" and on:
        K.px(x, y - 1, "glow")


def grille(K, x0, y0, x1, y1, a="faceD", b="face", step=2):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            K.px(x, y, a if (y - y0) % step == 0 else b)


def rivets(K, pts):
    for x, y in pts:
        K.px(x, y, "rivet")


def grain(K, x0, y0, x1, y1, base, line, seed=0, every=3):
    """boards running left to right: a darker grain line every few rows, broken where the boards meet"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            K.px(x, y, base)
        if (y - y0 + seed) % every == every - 1:
            for x in range(x0, x1 + 1):
                if (x * 7 + y * 3 + seed) % 11 not in (0, 1):
                    K.px(x, y, line)


# ================================================================== the machines
def p_panel(K, D):
    """the instrument panel (203/204 over 219/220, foot 235/236): FOUNDRY's dials-and-lamps cabinet, on a wall"""
    s = D["style"]
    K.fill("case")
    x0, y0, x1, y1 = K.bbox()
    K.hline(x0, x1, y0, "ol"); K.hline(x0, x1, y0 + 1, "caseL"); K.hline(x0, x1, y0 + 2, "caseL")
    K.hline(x0, x1, y0 + 3, "caseD")
    box_front(K, x0, x1, y0 + 4, y1 - 9)
    if s == "A":       # cast iron, a bronze bezel, two brass gauges and a row of pilot lamps over a fire-door vent
        for cx in (x0 + 4, x1 - 4):
            K.rect(cx - 2, y0 + 5, cx + 2, y0 + 9, "trim"); K.rect(cx - 1, y0 + 6, cx + 1, y0 + 8, "face")
            K.px(cx, y0 + 7, "dialD"); K.px(cx + 1, y0 + 6, "dialD")
        for i, x in enumerate(range(x0 + 2, x1 - 1, 3)):
            lamp(K, x, y0 + 12, D, on=i % 2 == 0)
        K.hline(x0 + 1, x1 - 1, y0 + 14, "trim")
        grille(K, x0 + 2, y1 - 8, x1 - 2, y1 - 3, "faceD", "glowD")
        rivets(K, [(x0 + 1, y0 + 5), (x1 - 1, y0 + 5), (x0 + 1, y1 - 3), (x1 - 1, y1 - 3)])
    elif s == "B":     # the PORT's family: a dark screen with a cursor line, a key strip, two status lights
        K.rect(x0 + 2, y0 + 5, x1 - 2, y0 + 11, "screen")
        K.hline(x0 + 3, x0 + 8, y0 + 7, "scrL"); K.hline(x0 + 3, x0 + 6, y0 + 9, "scrL"); K.px(x0 + 7, y0 + 9, "lampOn")
        K.hline(x0 + 2, x1 - 2, y0 + 12, "caseD")
        for x in range(x0 + 2, x1 - 1, 2):
            K.px(x, y0 + 14, "key")
        lamp(K, x1 - 3, y1 - 7, D, True); lamp(K, x1 - 5, y1 - 7, D, False)
        K.rect(x0 + 2, y1 - 6, x1 - 2, y1 - 3, "trim")
    else:              # a valve set in a timber case: a cream dial window with a needle, two knobs, a cloth grille
        K.rect(x0 + 2, y0 + 5, x1 - 2, y0 + 9, "face")
        for x in range(x0 + 3, x1 - 2, 2):
            K.px(x, y0 + 6, "dialD")
        K.vline(x0 + 7, y0 + 5, y0 + 9, "lampOn")
        for cx in (x0 + 4, x1 - 4):
            K.rect(cx - 1, y0 + 11, cx + 1, y0 + 13, "trim"); K.px(cx, y0 + 12, "dialD")
        grille(K, x0 + 2, y1 - 8, x1 - 2, y1 - 3, "faceD", "cloth")
    # the foot: a plinth, the floor's shadow under it
    K.rect(x0, y1 - 2, x1, y1, "caseD")
    K.hline(x0, x1, y1 - 2, "trim" if s != "B" else "caseL")
    K.rim()


def p_console(K, D):
    """the tall console (159 over 175 over 191, beside 207 over 223 over 239): a screen beside a keypad"""
    s = D["style"]
    K.fill("case")
    x0, y0, x1, y1 = K.bbox()
    K.hline(x0, x1, y0 + 1, "caseL"); K.hline(x0, x1, y0 + 2, "caseL"); K.hline(x0, x1, y0 + 3, "caseD")
    box_front(K, x0, x1, y0 + 4, y1 - 3)
    mid = (x0 + x1) // 2
    K.vline(mid, y0 + 4, y1 - 3, "caseD")
    # left: the screen
    K.rect(x0 + 2, y0 + 6, mid - 2, y0 + 13, "screen")
    if s == "A":       # a furnace sight-glass: the glow behind iron bars
        K.rect(x0 + 3, y0 + 7, mid - 3, y0 + 12, "glowD")
        K.rect(x0 + 3, y0 + 10, mid - 3, y0 + 12, "glow")
        for x in range(x0 + 3, mid - 2, 2):
            K.vline(x, y0 + 7, y0 + 12, "screen")
        K.rect(x0 + 1, y0 + 5, mid - 1, y0 + 5, "trim"); K.rect(x0 + 1, y0 + 14, mid - 1, y0 + 14, "trim")
    elif s == "B":     # a trace and a prompt
        for x in range(x0 + 3, mid - 2):
            K.px(x, y0 + 9 + ((x // 2) % 2) * (1 if x % 4 < 2 else -1), "scrL")
        K.hline(x0 + 3, x0 + 4, y0 + 12, "scrL")
    else:              # a round cream dial with a needle
        K.rect(x0 + 2, y0 + 6, mid - 2, y0 + 13, "face")
        K.hline(x0 + 3, mid - 3, y0 + 7, "dialD")
        K.vline((x0 + mid) // 2, y0 + 8, y0 + 11, "lampOff")
        K.rect(x0 + 1, y0 + 5, mid - 1, y0 + 5, "trim")
    # left foot: a drawer or a vent
    K.hline(x0 + 2, mid - 2, y1 - 7, "caseD")
    K.hline(x0 + 2, mid - 2, y1 - 5, "caseD")
    # right: the keypad and a lamp
    for ky in range(y0 + 7, y0 + 16, 3):
        for kx in range(mid + 2, x1 - 1, 2):
            K.px(kx, ky, "key"); K.px(kx, ky + 1, "keyD")
    lamp(K, mid + 2, y0 + 5, D, True)
    lamp(K, mid + 4, y0 + 5, D, False)
    K.rect(mid + 2, y1 - 8, x1 - 2, y1 - 5, "trim" if s != "B" else "faceD")
    K.rect(x0, y1 - 2, x1, y1, "caseD")
    K.rim()


def p_server(K, D):
    """the tall cabinet against the wall (247/248 its top, 249..254 its face): FOUNDRY's records press / a rack"""
    s = D["style"]
    K.fill("case")
    x0, y0, x1, y1 = K.bbox()
    top = y0
    K.rect(x0, top, x1, top + 4, "caseL")
    K.hline(x0, x1, top + 5, "caseD")
    box_front(K, x0, x1, top + 6, y1 - 2)
    if s == "A":       # a press of cast drawers, bronze pulls, a lamp each
        for y in range(top + 8, y1 - 3, 5):
            K.hline(x0 + 1, x1 - 1, y + 3, "caseD")
            K.rect(x0 + 5, y + 1, x1 - 5, y + 1, "trim")
            lamp(K, x1 - 2, y, D, (y // 5) % 2 == 0)
        rivets(K, [(x0 + 1, top + 7), (x1 - 1, top + 7)])
    elif s == "B":     # a rack: slots with status lights, a little screen at the top
        K.rect(x0 + 2, top + 7, x1 - 2, top + 10, "screen")
        K.hline(x0 + 3, x0 + 7, top + 8, "scrL")
        for y in range(top + 13, y1 - 3, 3):
            K.hline(x0 + 2, x1 - 4, y, "faceD")
            lamp(K, x1 - 2, y, D, (y // 3) % 2 == 0)
    else:              # a tall timber cabinet: two doors, brass escutcheons, a radio set on top
        K.vline((x0 + x1) // 2, top + 6, y1 - 3, "caseD")
        K.rect((x0 + x1) // 2 - 2, top + 14, (x0 + x1) // 2 - 2, top + 15, "trim")
        K.rect((x0 + x1) // 2 + 2, top + 14, (x0 + x1) // 2 + 2, top + 15, "trim")
        K.rect(x0 + 3, top + 1, x1 - 3, top + 3, "face")
        K.hline(x0 + 4, x1 - 4, top + 2, "dialD")
    K.rect(x0, y1 - 1, x1, y1, "caseD")
    K.rim()


def p_till(K, D):
    """the bike shop's till on its counter (270/271, 286/287, 302/303, placed mirrored)"""
    s = D["style"]
    K.fill("case")
    x0, y0, x1, y1 = K.bbox()
    K.rect(x0, y0, x1, y0 + 3, "caseL")
    K.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 2, "screen" if s == "B" else "face")
    K.hline(x0 + 2, x0 + 4, y0 + 1, "scrL" if s == "B" else "dialD")
    for y in range(y0 + 6, y1 - 3, 2):
        for x in range(x0 + 2, x1 - 1, 2):
            K.px(x, y, "key")
    K.rect(x0, y1 - 3, x1, y1, "trim" if s != "B" else "caseD")
    K.hline(x0 + 3, x1 - 3, y1 - 2, "caseD")
    K.rim()


def p_desk_terminal(K, D):
    """the terminal that sits on a striped desk (189/190 over 205/206)"""
    s = D["style"]
    K.fill("case")
    x0, y0, x1, y1 = K.bbox()
    K.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 8, "screen")
    if s == "A":
        K.rect(x0 + 2, y0 + 5, x1 - 2, y0 + 7, "glowD"); K.hline(x0 + 3, x1 - 3, y0 + 6, "glow")
        K.hline(x0, x1, y0 + 9, "trim")
    elif s == "B":
        K.hline(x0 + 3, x0 + 8, y0 + 3, "scrL"); K.hline(x0 + 3, x0 + 6, y0 + 5, "scrL")
        K.px(x0 + 7, y0 + 5, "lampOn")
    else:
        K.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 8, "face"); K.hline(x0 + 2, x1 - 2, y0 + 3, "dialD")
        K.vline((x0 + x1) // 2, y0 + 4, y0 + 7, "lampOff")
    for y in range(y0 + 11, y1 - 1, 2):
        for x in range(x0 + 2, x1 - 1, 2):
            K.px(x, y, "key")
    K.hline(x0, x1, y1, "caseD")
    K.rim()


def p_ledger(K, D):
    """the open ledger lying askew on a striped desk (157/158 over 173/174)"""
    K.fill("paper")
    x0, y0, x1, y1 = K.bbox()
    cx = (x0 + x1) // 2
    for y in range(y0, y1 + 1):
        s = K.span(y)
        if not s:
            continue
        for x in range(s[0], s[1] + 1):
            if (x + y) % 3 == 0:
                K.px(x, y, "paperD")
    for y in range(y0, y1 + 1):
        K.px(cx + (y - (y0 + y1) // 2) // 3, y, "spine")
    K.rim("cover")


# ================================================================== the desks
def p_table_top(K, D):
    """the far rim of the lab table (150/151/152): its back edge, seen from above"""
    K.fill(D["deskTop"])
    x0, y0, x1, y1 = K.bbox()
    K.hline(x0, x1, y1 - 1, D["deskTopL"])
    K.hline(x0, x1, y1, D["deskTop"])
    if D["style"] == "A":
        K.hline(x0, x1, y1 - 2, "trim")
    K.rim()


def p_table_body(K, D):
    """the lab table's surface (135 left, 134 middle, 136 right; it tiles both ways)"""
    s = D["style"]
    x0, y0, x1, y1 = K.bbox()
    if s == "A":       # timber boards on an iron frame, bronze-edged
        grain(K, x0, y0, x1, y1, "top", "topD", every=4)
    elif s == "B":     # pale laminate, a ruled cutting mat
        K.fill("lam")
        for y in range(y0, y1 + 1, 4):
            K.hline(x0, x1, y, "lamD")
        for x in range(x0 + 3, x1 + 1, 8):
            K.vline(x, y0, y1, "lamD")
    else:              # the house's own timber: long boards
        grain(K, x0, y0, x1, y1, "top", "topD", every=3)
    K.rim()
    #  its left and right edges: the frame
    for y in range(y0, y1 + 1):
        sp = K.span(y)
        if sp and K.edge(sp[0], y):
            K.px(sp[0] + 1, y, "trim" if s == "A" else D["deskTopL"])


def p_legs(K, D):
    """the front of a desk: its apron and legs (243/244, placed mirrored under the lab table)"""
    s = D["style"]
    K.fill(D["deskFront"])
    x0, y0, x1, y1 = K.bbox()
    K.hline(x0, x1, y0, D["deskTopL"])
    K.hline(x0, x1, y0 + 1, D["deskFront"])
    K.hline(x0, x1, y0 + 3, D["deskFrontD"])
    if s == "A":
        K.hline(x0, x1, y0 + 2, "trim")
    for x in range(x0, x1 + 1):
        for y in range(y0 + 4, y1 + 1):
            if K.foot(x, y):
                K.px(x, y, "leg")
    K.rim()


def p_small_desk(K, D):
    """the lab's work desk (213/214 its back, 229/230 its top, 245/246 its front): a ledger and a mug on it"""
    s = D["style"]
    x0, y0, x1, y1 = K.bbox()
    top_y1 = y0 + 15
    if s == "B":
        K.rect(x0, y0, x1, top_y1, "lam")
        for y in range(y0 + 2, top_y1, 4):
            K.hline(x0, x1, y, "lamD")
    else:
        grain(K, x0, y0, x1, top_y1, "top", "topD", every=4 if s == "A" else 3)
    K.hline(x0, x1, y0, D["deskTopL"])
    # a ledger, open (left), and a mug (right)
    K.rect(x0 + 2, y0 + 3, x0 + 8, y0 + 11, "paper")
    K.vline(x0 + 5, y0 + 3, y0 + 11, "spine")
    for y in range(y0 + 5, y0 + 11, 2):
        K.hline(x0 + 3, x0 + 4, y, "ink"); K.hline(x0 + 6, x0 + 7, y, "ink")
    K.rect(x1 - 5, y0 + 6, x1 - 2, y0 + 9, "mug"); K.hline(x1 - 5, x1 - 2, y0 + 6, "paper")
    K.px(x1 - 1, y0 + 7, "mug")
    # the front
    K.rect(x0, top_y1 + 1, x1, y1, D["deskFront"])
    K.hline(x0, x1, top_y1 + 1, D["deskTopL"])
    if s == "A":
        K.hline(x0, x1, top_y1 + 2, "trim")
    K.hline((x0 + x1) // 2 - 2, (x0 + x1) // 2 + 2, top_y1 + 4, "trim" if s != "B" else "lamD")
    for y in range(top_y1 + 6, y1 + 1):
        K.hline(x0 + 1, x1 - 1, y, D["deskFrontD"])
        K.px(x0, y, "leg"); K.px(x1, y, "leg")
    K.rim()


def p_papers(K, D):
    """papers on the lab table (208/209), a note pinned up (210)"""
    K.fill("paper")
    x0, y0, x1, y1 = K.bbox()
    for y in range(y0 + 2, y1, 2):
        sp = K.span(y)
        if sp:
            K.hline(sp[0] + 1, sp[1] - 1, y, "ink" if D["style"] != "B" else "inkB")
    K.rim("paperD")


def p_rail(K, D):
    """the bench rail under the lab shelves and in the museum (185/186, mirrored)"""
    x0, y0, x1, y1 = K.bbox()
    K.fill(D["deskTop"])
    K.hline(x0, x1, y0, "ol")
    K.hline(x0, x1, y0 + 1, D["deskTopL"])
    K.hline(x0, x1, y1 - 1, D["deskFront"])
    if D["style"] == "A":
        rivets(K, [(x, y0 + 3) for x in range(x0 + 3, x1, 6)])
    K.rim()


def p_striped_desk(K, D):
    """the striped desk (461..463 over 477..479 over 493..495; the labs, the MANSION, the SAFARI office)"""
    s = D["style"]
    x0, y0, x1, y1 = K.bbox()
    front = y1 - 7
    if s == "A":       # iron-framed, a timber top, a bronze band
        grain(K, x0, y0, x1, front - 1, "top", "topD", every=4)
        K.hline(x0, x1, y0 + 1, "topL")
        K.rect(x0, front, x1, y1, "caseD"); K.hline(x0, x1, front, "trim"); K.hline(x0, x1, front + 1, "case")
        for x in range(x0 + 4, x1 - 2, 8):
            K.px(x, front + 3, "rivet")
    elif s == "B":     # laminate, a blue modesty panel, as the CHECKPOINT counters
        K.rect(x0, y0, x1, front - 1, "lam")
        for y in range(y0 + 3, front - 1, 4):
            K.hline(x0 + 1, x1 - 1, y, "lamD")
        K.rect(x0, front, x1, y1, "blue"); K.hline(x0, x1, front, "lamL"); K.hline(x0, x1, front + 1, "blueL")
    else:              # a writing desk: boards, a drawer each side
        grain(K, x0, y0, x1, front - 1, "top", "topD", every=3)
        K.hline(x0, x1, y0 + 1, "topL")
        K.rect(x0, front, x1, y1, "front"); K.hline(x0, x1, front, "topL")
        for x in range(x0 + 3, x1 - 3, 10):
            K.hline(x, x + 3, front + 3, "trim")
    for y in range(front + 4, y1 + 1):
        K.px(x0 + 1, y, "leg"); K.px(x1 - 1, y, "leg")
    K.rim()


def p_boardroom(K, D):
    """FOUNDRY 11F's boardroom table: an octagon, its halves mirrored (484..508 as 11F lays them)"""
    s = D["style"]
    x0, y0, x1, y1 = K.bbox()
    front = y1 - 9                     # the apron and legs below this row
    top, topD, lit, shade = {"A": ("top", "topD", "trimL", "trim"), "B": ("lam", "lamD", "lamL", "lamD"),
                             "C": ("top", "topD", "topL", "front")}[s]
    # the top: boards running the table's length (A, C) or a plain laminate (B)
    for y in range(y0, front):
        sp = K.span(y)
        if not sp:
            continue
        for x in range(sp[0], sp[1] + 1):
            # 488 and 491 are ONE flat tile each, repeated across the middle: the pattern repeats every 8 pixels
            line = s != "B" and y % 4 == 3 and (x + (y // 4) * 3) % 8 != 0
            K.px(x, y, topD if line else top)
    # the bevel: two pixels in from the octagon's edge, lit on the upper left, shaded on the lower right
    for y in range(y0, front):
        sp = K.span(y)
        if not sp:
            continue
        for x in range(sp[0], sp[1] + 1):
            near = min(x - sp[0], sp[1] - x, y - y0, front - 1 - y)
            if near <= 1:
                K.px(x, y, lit if (x - sp[0] < sp[1] - x and y - y0 < front - 1 - y) or y - y0 <= 1 else shade)
    #  (no inlay: the middle is two repeated flat tiles, so anything drawn there repeats every 8 pixels)
    # the apron and legs
    for y in range(front, y1 + 1):
        sp = K.span(y)
        if not sp:
            continue
        for x in range(sp[0], sp[1] + 1):
            K.px(x, y, {"A": "caseD", "B": "blue", "C": "front"}[s])
    K.hline(x0, x1, front, {"A": "trim", "B": "lamL", "C": "topL"}[s])
    K.hline(x0, x1, front + 1, {"A": "case", "B": "blueL", "C": "front"}[s])
    for y in range(front + 3, y1 + 1):
        for x in (x0 + 3, x0 + 4, x1 - 4, x1 - 3, (x0 + x1) // 2 - 6, (x0 + x1) // 2 + 6):
            K.px(x, y, "leg")
    K.rim()


def p_ornament(K, D):
    """what stands on the boardroom table (638/639 over 610/611): a casting, a terminal, or a radio"""
    s = D["style"]
    x0, y0, x1, y1 = K.bbox()
    K.fill("case")
    if s == "A":       # the first BOX cast, on a plinth: a bronze cube, its lid seam lit
        K.rect(x0 + 2, y0 + 1, x1 - 2, y1 - 4, "bronze")
        K.hline(x0 + 2, x1 - 2, y0 + 1, "trimL")
        K.hline(x0 + 2, x1 - 2, y0 + 4, "glow")
        K.rect(x0 + 1, y1 - 3, x1 - 1, y1, "caseD")
    elif s == "B":     # a desk terminal turned to the chair
        K.rect(x0 + 2, y0 + 1, x1 - 2, y1 - 5, "screen")
        K.hline(x0 + 4, x1 - 5, y0 + 4, "scrL")
        K.rect(x0 + 1, y1 - 3, x1 - 1, y1, "caseL")
    else:              # a valve radio
        K.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 2, "front")
        K.rect(x0 + 3, y0 + 3, x1 - 3, y0 + 6, "face")
        K.hline(x0 + 4, x1 - 4, y0 + 4, "dialD")
        grille(K, x0 + 3, y0 + 8, x1 - 3, y1 - 3, "faceD", "cloth")
    K.rim()


def p_reception(K, D):
    """FOUNDRY 1F's reception desk (324..374): an L of counter, its top and its front -- drawn in rows 0 and 1"""
    s = D["style"]
    x0, y0, x1, y1 = K.bbox()
    # the counter is drawn in rows 0 AND 1, so only the colours the two rows share read the same: outline, iron,
    # stone, white -- and index 7, wood in row 0 and sky in row 1. Each direction draws its counter in those.
    for y in range(K.h):
        for x in range(K.w):
            if not K.foot(x, y):
                continue
            K.px(x, y, "cTop")
    # its fronts: wherever the footprint's lower edge is, three rows of front under the top
    for x in range(K.w):
        ys = [y for y in range(K.h) if K.foot(x, y)]
        if not ys:
            continue
        bottom = ys[-1]
        for y in range(bottom - 3, bottom + 1):
            K.px(x, y, "cFront")
        K.px(x, bottom - 4, "cEdge")
    for y in range(K.h):
        sp = K.span(y)
        if sp:
            K.px(sp[1] - 1, y, "cEdge")
    if s == "A":
        for x in range(x0 + 3, x1, 6):
            K.px(x, y1 - 2, "cEdge")
    K.rim()


# ================================================================== the groups
#  key, title, layout, painter, what it is. The first placement of a tile wins, so the plain pieces come first.
GROUPS = [
    ("panel", "the instrument panel", [[203, 204], [219, 220], [235, 236]], p_panel,
     "FOUNDRY 2F-10F, the POWER PLANT, the MANSION, the CORPUS rooms: the blinking-light machine"),
    ("console", "the tall console", [[159, 207], [175, 223], [191, 239]], p_console,
     "a screen beside a keypad: FOUNDRY, the POWER PLANT, the labs"),
    ("cabinet", "the tall cabinet", [[247, 248], [249, 250], [251, 252], [253, 254]], p_server,
     "against the wall: FOUNDRY 5F's three, the SEA COTTAGE, the labs"),
    ("till", "the till", [[H(271), H(270)], [H(287), H(286)], [H(303), H(302)]], p_till, "the bike shop's counter"),
    ("terminal", "the desk terminal", [[189, 190], [205, 206]], p_desk_terminal,
     "on a striped desk: the labs, the SEA COTTAGE"),
    ("ledger", "the ledger on the desk", [[157, 158], [173, 174]], p_ledger, "an open book, askew"),
    ("table_top", "the lab table's far rim", [[150, 151, 152]], p_table_top, "its back edge"),
    ("table", "the lab table", [[135, 134, 134, 136], [135, 134, 134, 136]], p_table_body,
     "its surface: tiles both ways"),
    ("legs", "the desk front and legs", [[H(244), H(243)]], p_legs, "under the lab table, and under the PORT"),
    ("small_desk", "the work desk", [[213, 214], [229, 230], [245, 246]], p_small_desk, "a ledger and a mug"),
    ("papers", "the papers", [[208, 209]], p_papers, "on the lab table"),
    ("note", "the pinned note", [[210]], p_papers, "on the lab wall"),
    ("rail", "the bench rail", [[185, 186, H(186), H(185)]], p_rail, "under the lab shelves; the museum"),
    ("striped", "the striped desk", [[461, 462, 463], [477, 478, 479], [493, 494, 495]], p_striped_desk,
     "the labs, the MANSION, the SAFARI office, the station"),
    ("boardroom", "the boardroom table", None, p_boardroom, "FOUNDRY 11F: the octagon"),
    ("ornament", "what stands on it", None, p_ornament, "FOUNDRY 11F"),
    ("reception", "the reception desk", None, p_reception,
     "FOUNDRY 1F and 7F, the lab's lobby, the day care, the bike shop -- drawn in rows 0 and 1"),
    ("reception_lab", "the lab's front desk", None, p_reception, "the CINNABAR lab's lobby: the same counter, its end"),
]
BOARD = set(range(484, 509)) - {496, 497, 498, 499, 502}
ORN = {610, 611, 638, 639}
RECEPTION = {324, 325, 326, 340, 341, 342, 356, 357, 358, 370, 371, 372, 373, 374}


def layouts():
    out = {}
    for key, title, lay, paint, note in GROUPS:
        if lay is None:
            if key == "boardroom":
                lay = map_layout("SilphCo_11F", 7, 10, 5, 4, BOARD)
            elif key == "ornament":
                lay = map_layout("SilphCo_11F", 9, 11, 1, 1, ORN)
            elif key == "reception":
                lay = map_layout("SilphCo_1F", 0, 3, 7, 6, RECEPTION)
            elif key == "reception_lab":
                lay = map_layout("CinnabarIsland_PokemonLab_Entrance", 0, 3, 2, 5, RECEPTION)
        out[key] = lay
    return out


#  what this ticket leaves, and why: the rest of the census (item 6)
LEFT = [
    ("bed", set(range(512, 516)) | set(range(528, 532)) | set(range(544, 548)),
     "FOUNDRY 8F/9F's rest-room beds and LORELEI's house: furniture, not desks or machines"),
    ("doorway", {522, 523, 524, 538, 539, 540, 554, 555, 556},
     "the open doorways to the back rooms: a door frame, gbadoors.py's kind"),
    ("partition", {171, 172, 180, 181, 187, 188, 196, 197},
     "white partition walls seen from above (the labs, FOUNDRY): structure, not furniture"),
    ("stairs", {39, 49, 50, 54, 55, 65, 66, 67, 80, 81, 82},
     "BRAZEN's copycat house: eleven stair tiles batch D's stairs rule leaves pixel-identical -- drawn only in OUT and "
     "the three woods, which it maps onto themselves; they are timber already through rows 0's approved palette"),
    ("blinds", {420, 421, 436, 432, 433}, "the CINNABAR lab lounge's blinds"),
    ("diary", {602, 603, 618, 619}, "the MANSION's open diary: a landmark's (T-447)"),
    ("odd", {368}, "one tile of the lab lobby"),
]


# ================================================================== the directions
_COMMON = dict(ol=(82, 82, 106), rivet=(232, 212, 150), paper=(238, 226, 200), paperD=(180, 180, 164),
               ink=(84, 72, 70), inkB=(98, 122, 162), spine=(150, 76, 60), cover=(150, 76, 60), mug=(172, 86, 78),
               leg=(82, 82, 106))
A = dict(name="A", title="FOUNDRY STOCK", style="A",
         blurb="Every machine and desk in the game came out of FOUNDRY CO.'s works before CORPUS: cast-iron cases, "
               "bronze bezels and rivets, a pilot lamp and a sight-glass of furnace glow where vanilla had a strip of "
               "coloured lights; desks iron-framed with timber tops. T-536's C continued onto the furniture -- the "
               "company that made the BOXes made the machines everyone uses.",
         deskTop="top", deskTopL="topL", deskFront="caseD", deskFrontD="ol",
         mat=dict(_COMMON, case=(110, 104, 104), caseD=(84, 72, 70), caseL=(150, 144, 134), trim=(196, 150, 80),
                  trimL=(232, 200, 120), bronze=(214, 166, 112), face=(84, 72, 70), faceD=(60, 56, 64),
                  screen=(60, 56, 64), scrL=(226, 150, 84), glow=(232, 180, 90), glowD=(150, 76, 60),
                  lampOn=(240, 200, 110), lampOff=(150, 76, 60), dialD=(84, 72, 70), key=(150, 144, 134),
                  keyD=(84, 72, 70), cloth=(110, 104, 104), top=(176, 122, 76), topD=(128, 86, 54),
                  topL=(214, 166, 112), front=(84, 72, 70), lam=(180, 180, 164), lamD=(150, 144, 134),
                  lamL=(232, 224, 206), blue=(84, 72, 70), blueL=(110, 104, 104),
                  cTop=(180, 180, 164), cFront=(123, 123, 123), cEdge=(82, 82, 106)))
B = dict(name="B", title="THE PORT'S FAMILY", style="B",
         blurb="The machines are kin of the PORT (batch D) and of the game's menus -- A TERMINAL: slate cases, dark "
               "screens with a cursor and a line of text, green and sky status lights; desks pale laminate with a "
               "blue front, as the CHECKPOINT counters. Modern and quiet; it reads the same in a lab and in FOUNDRY.",
         deskTop="lam", deskTopL="lamL", deskFront="blue", deskFrontD="blueD",
         mat=dict(_COMMON, case=(180, 180, 164), caseD=(123, 123, 123), caseL=(232, 230, 226), trim=(98, 122, 162),
                  trimL=(150, 186, 204), bronze=(180, 180, 164), face=(197, 189, 213), faceD=(123, 123, 123),
                  screen=(82, 82, 106), scrL=(150, 198, 120), glow=(150, 198, 120), glowD=(82, 82, 106),
                  lampOn=(150, 198, 120), lampOff=(98, 122, 162), dialD=(82, 82, 106), key=(232, 224, 206),
                  keyD=(150, 144, 134), cloth=(180, 180, 164), top=(232, 224, 206), topD=(180, 180, 164),
                  topL=(255, 255, 255), front=(98, 122, 162), lam=(232, 224, 206), lamD=(180, 180, 164),
                  lamL=(255, 255, 255), blue=(98, 122, 162), blueL=(150, 186, 204), blueD=(74, 104, 130),
                  cTop=(255, 255, 255), cFront=(180, 180, 164), cEdge=(123, 123, 123)))
C = dict(name="C", title="THE WIRELESS", style="C",
         blurb="The machines are valve sets in timber cases -- a cream dial window and a needle, brass knobs, a "
               "cloth grille, an amber valve glowing -- and the desks are the houses' own timber (batch D's). Warmest "
               "in a front room; in FOUNDRY it reads as the company's older stock among the iron.",
         deskTop="top", deskTopL="topL", deskFront="front", deskFrontD="caseD",
         mat=dict(_COMMON, case=(176, 122, 76), caseD=(128, 86, 54), caseL=(214, 166, 112), trim=(214, 180, 98),
                  trimL=(232, 212, 150), bronze=(214, 180, 98), face=(238, 226, 200), faceD=(128, 86, 54),
                  screen=(238, 226, 200), scrL=(150, 76, 60), glow=(226, 150, 84), glowD=(150, 76, 60),
                  lampOn=(226, 150, 84), lampOff=(150, 76, 60), dialD=(84, 72, 70), key=(238, 226, 200),
                  keyD=(128, 86, 54), cloth=(214, 166, 112), top=(176, 122, 76), topD=(128, 86, 54),
                  topL=(214, 166, 112), front=(128, 86, 54), lam=(232, 224, 206), lamD=(180, 180, 164),
                  lamL=(255, 255, 255), blue=(128, 86, 54), blueL=(176, 122, 76),
                  cTop=("idx", 7), cFront=(123, 123, 123), cEdge=(82, 82, 106)))
STYLES = {"A": A, "B": B, "C": C}

#  BLINK (optional, not in --write): two more frames of the lamps. gTileset_Building has no animation callback, so a
#  blink needs one in src/tileset_anims.c (InitTilesetAnim_Building, a timer copying frames over these tiles) and the
#  header's .callback set -- engine code, and every interior loads this primary. The tiles must be the machines' own:
#  each is placed by nothing else (checked in report()), so engine.md trap 39 cannot bite the other way.
BLINK = [203, 204, 219, 220, 235, 236, 159, 207, 175, 223, 249, 250, 251, 252]


def draw(D):
    """the redrawn tile list for direction D, which group drew each tile, and the canvases"""
    new = [t[:] for t in CUR]
    owner, canv = {}, {}
    lays = layouts()
    for key, title, _, paint, note in GROUPS:
        K = Cv(lays[key])
        paint(K, D)
        canv[key] = K
        for t, mats in K.tiles().items():
            if t in GB.KEEP or t in owner:
                continue
            new[t] = quantize(t, mats, D)
            owner[t] = key
    return new, owner, canv


def blink_frames(D):
    """frame 1: the lamps swapped on/off; frame 2: all off -- the BLINK tiles only"""
    frames = []
    for swap in ("swap", "off"):
        mat = dict(D["mat"])
        if swap == "swap":
            mat["lampOn"], mat["lampOff"] = D["mat"]["lampOff"], D["mat"]["lampOn"]
            mat["glow"], mat["glowD"] = D["mat"]["glowD"], D["mat"]["glow"]
            mat["scrL"] = D["mat"]["screen"]
        else:
            mat["lampOn"] = D["mat"]["lampOff"]
            mat["glow"] = D["mat"]["glowD"]
        D2 = dict(D, mat=mat)
        new, owner, _ = draw(D2)
        frames.append({t: new[t] for t in BLINK})
    return frames


# ================================================================== the report
def census():
    van = still_vanilla()
    lays = layouts()
    mine = {}
    for key, title, _, paint, note in GROUPS:
        for row in lays[key]:
            for spec in row:
                if spec is not None:
                    t = spec if isinstance(spec, int) else spec[0]
                    mine.setdefault(t, key)
    rows = []
    for key, title, _, paint, note in GROUPS:
        ts = sorted(t for t, k in mine.items() if k == key)
        rows.append(("T-537", key, title, ts))
    for key, ts, why in LEFT:
        rows.append(("left", key, why, sorted(t for t in ts if t in USE)))
    stray = sorted(t for t in van if t not in mine and not any(t in s for _, s, _ in LEFT))
    return van, mine, rows, stray


def report():
    van, mine, rows, stray = census()
    print("  T-537: primary/building -- %d drawn tiles are still vanilla's (one colour or KEEP excluded); this ticket "
          "owns %d tiles, %d of them still vanilla's (the rest drawn by --write --approved --pick %s)" % (
              len(van), len(mine), len([t for t in mine if t in van]), "/".join(sorted(APPROVED)) or "?"))
    print("  scanned %d tiles placed by %d maps" % (len(USE), len({m for u in USE.values() for m in u["maps"]})))
    print("\n  %-6s %-11s %5s %5s %4s  %-40s %s" % ("", "object", "tiles", "draws", "maps", "blocks (first 6)", "what"))
    for who, key, title, ts in rows:
        draws = sum(USE[t]["draws"] for t in ts if t in USE)
        maps = sorted({m for t in ts if t in USE for m in USE[t]["maps"]})
        blocks = sorted({"%s:%#x" % b for t in ts if t in USE for b in USE[t]["blocks"]})
        print("  %-6s %-11s %5d %5d %4d  %-40s %s" % (who, key, len(ts), draws, len(maps), ",".join(blocks[:3])[:40],
                                                    title[:70]))
    if stray:
        print("  !! still vanilla and in no row above: %s" % stray)
    shared = [t for t in BLINK if mine.get(t) not in ("panel", "console", "cabinet")]
    print("\n  the engine names: METATILE_Building_PCOff 0x062 / PCOn 0x063 (field_specials.c) -- the PORT, batch D's, "
          "untouched. No script sets a building block below 0x280; gTileset_Building has no animation callback.")
    print("  BLINK (optional): %d tiles, %d extra frames each; all are this draft's own (%s)" % (
        len(BLINK), 2, "ok" if not shared else "!! %s" % shared))
    return van, mine, rows, stray


# ================================================================== pictures
def tile_img(px, pal, flip=""):
    return GB.tile_img(px, pal, flip)


def canvas_img(lay, tiles, scale):
    """the object as it stands, each tile in the row it is placed in most"""
    th, tw = len(lay), max(len(r) for r in lay)
    im = Image.new("RGBA", (tw * 8, th * 8), (214, 212, 200, 255))
    for ty, r in enumerate(lay):
        for tx, spec in enumerate(r):
            if spec is None:
                continue
            t, fl = (spec, "") if isinstance(spec, int) else spec
            row = GB.home_row(USE, t) or 0
            im.alpha_composite(tile_img(tiles[t], PALS[row], fl), (tx * 8, ty * 8))
    im = im.convert("RGB")
    return im.resize((im.size[0] * scale, im.size[1] * scale), Image.NEAREST)


def labelled(im, text, sub=""):
    o = Image.new("RGB", (max(im.size[0], 8 * len(text) // 1 + 4), im.size[1] + 30), GB.BG)
    d = ImageDraw.Draw(o)
    d.text((0, 0), text, fill=GB.INK, font=GB.font(12))
    if sub:
        d.text((0, 14), sub, fill=GB.SOFT, font=GB.font(10))
    o.paste(im, (0, 30))
    return o


#  the rooms each direction is shown in (map, crop in cells or None, what it shows)
ROOMS = [
    ("SilphCo_5F", (0, 0, 36, 22), "FOUNDRY 5F: the panel, the console, the three cabinets, T-536 C around them"),
    ("SilphCo_11F", None, "FOUNDRY 11F: the boardroom table and what stands on it"),
    ("SilphCo_1F", (0, 0, 16, 11), "FOUNDRY 1F: the reception desk"),
    ("CinnabarIsland_PokemonLab_ExperimentRoom", None, "a lab: striped desks, the terminal, the ledger, the work desk"),
    ("CinnabarIsland_PokemonLab_ResearchRoom", None, "a lab: the lab tables, the work desks, the bench rail"),
    ("Route25_SeaCottage", None, "a house: the SEA COTTAGE -- the cabinets and terminals on its desks"),
    ("SaffronCity_CopycatsHouse_2F", None, "a house: BRAZEN's copycat house upstairs -- the lab table as a desk"),
    ("CeruleanCity_BikeShop", None, "a shop: the till on the counter, the lab table as a work bench"),
    ("PowerPlant", (12, 22, 34, 16), "the POWER PLANT: panels and consoles in the walls"),
]
DETAIL = [("SilphCo_5F", (13, 8, 10, 6)), ("SilphCo_11F", (5, 9, 9, 6)), ("CinnabarIsland_PokemonLab_ResearchRoom",
                                                                           (1, 3, 6, 5))]


def room(R, m, tiles, crop=None):
    im = GB.render_room(R, m, tiles, GB.palettes())
    if crop:
        x, y, w, h = crop
        im = im.crop((x * 16, y * 16, min(im.size[0], (x + w) * 16), min(im.size[1], (y + h) * 16)))
    return im


def sheets(outdir, drawn):
    """per direction: rooms at 1x (today | draft), details at 3x, the objects and their tiles at 3x, the blink"""
    R = GB._reviewsheet()
    written = []
    lays = layouts()
    for X, (D, new, owner, frames) in drawn.items():
        blocks = []
        for m, crop, what in ROOMS:
            a, b = room(R, m, CUR, crop), room(R, m, new, crop)
            blocks.append(labelled(GB.panel_row([a, b], ["today", "draft %s (1x)" % X], gap=12), m, what))
        path = os.path.join(outdir, "t537_%s_rooms.png" % X)
        GB.pack(blocks, "T-537 %s %s (DRAFT) -- the desks and machines in real rooms, 1x: today | draft" % (
            X, D["title"]), maxw=1700).save(path)
        written.append(path)
        blocks = []
        for m, crop in DETAIL:
            ims = [room(R, m, t, crop) for t in (CUR, new)]
            ims = [i.resize((i.size[0] * 3, i.size[1] * 3), Image.NEAREST) for i in ims]
            blocks.append(labelled(GB.panel_row(ims, ["today, 3x", "draft %s, 3x" % X], gap=12), m))
        objs = []
        for key, title, _, paint, note in GROUPS:
            lay = lays[key]
            ims = [canvas_img(lay, VAN, 3), canvas_img(lay, new, 3)]
            objs.append(labelled(GB.panel_row(ims, ["vanilla", "draft"], gap=8), "%s -- %s" % (key, title), note[:60]))
        # the tiles themselves at 3x, in the sheet's own order
        ts = sorted(owner)
        per = 24
        tim = Image.new("RGB", (per * 26, ((len(ts) + per - 1) // per) * 40), GB.BG)
        d = ImageDraw.Draw(tim)
        for k, t in enumerate(ts):
            row = GB.home_row(USE, t) or 0
            ti = Image.new("RGBA", (8, 8), (214, 212, 200, 255))
            ti.alpha_composite(tile_img(new[t], PALS[row]))
            x, y = (k % per) * 26, (k // per) * 40
            tim.paste(ti.convert("RGB").resize((24, 24), Image.NEAREST), (x, y + 12))
            d.text((x, y), str(t), fill=GB.SOFT, font=GB.font(9))
        objs.append(labelled(tim, "the %d tiles at 3x (each in the row that places it most)" % len(ts)))
        # the blink, if the user wants one
        fr = []
        for key in ("panel", "console", "cabinet"):
            lay = lays[key]
            seq = [canvas_img(lay, new, 3)]
            for f in frames:
                t2 = list(new)
                for t, px in f.items():
                    t2[t] = px
                seq.append(canvas_img(lay, t2, 3))
            fr.append(labelled(GB.panel_row(seq, ["frame 0", "frame 1", "frame 2"], gap=6), key))
        objs.append(labelled(GB.panel_row(fr, ["", "", ""], gap=20),
                             "BLINK (optional; engine code): %d tiles x 3 frames" % len(BLINK)))
        path = os.path.join(outdir, "t537_%s_detail.png" % X)
        GB.pack(blocks + objs, "T-537 %s %s (DRAFT) -- details and objects at 3x: %s" % (
            X, D["title"], D["blurb"][:110]), maxw=1800).save(path)
        written.append(path)
    # side by side: the three directions in the two FOUNDRY rooms and a lab, 1x, and the objects at 3x
    blocks = []
    for m, crop, what in (ROOMS[0], ROOMS[1], ROOMS[3], ROOMS[5]):
        ims = [room(R, m, CUR, crop)] + [room(R, m, drawn[X][1], crop) for X in "ABC"]
        blocks.append(labelled(GB.panel_row(ims, ["today", "A " + A["title"], "B " + B["title"], "C " + C["title"]],
                                            gap=12), m, what))
    path = os.path.join(outdir, "t537_compare_rooms.png")
    GB.stack(blocks, "T-537 (DRAFT): A FOUNDRY STOCK | B THE PORT'S FAMILY | C THE WIRELESS -- 1x, beside today").save(path)
    written.append(path)
    blocks = []
    for key, title, _, paint, note in GROUPS:
        lay = lays[key]
        ims = [canvas_img(lay, VAN, 3)] + [canvas_img(lay, drawn[X][1], 3) for X in "ABC"]
        blocks.append(labelled(GB.panel_row(ims, ["vanilla", "A", "B", "C"], gap=8), "%s -- %s" % (key, title)))
    path = os.path.join(outdir, "t537_compare_objects.png")
    GB.pack(blocks, "T-537 (DRAFT): every object at 3x -- vanilla | A | B | C", maxw=1800).save(path)
    written.append(path)
    return written


def census_sheet(outdir, rows):
    """the census: the whole primary at 2x, still-vanilla tiles outlined, this draft's in their colour"""
    van = set(still_vanilla())
    S = 3
    im = Image.new("RGB", (16 * (8 * S + 1), (NT // 16) * (8 * S + 1)), (60, 60, 60))
    d = ImageDraw.Draw(im)
    col = {}
    palette = [(220, 60, 60), (60, 140, 220), (60, 180, 90), (200, 140, 40), (150, 80, 200), (40, 170, 170),
               (230, 110, 170), (120, 120, 40)]
    for who, key, title, ts in rows:
        for t in ts:
            col[t] = (220, 40, 40) if who == "T-537" else (240, 200, 60)
    for t in range(NT):
        r = GB.home_row(USE, t)
        r = 0 if r is None or r > 6 else r
        base = Image.new("RGBA", (8, 8), (214, 212, 200, 255) if t in USE else (120, 118, 110, 255))
        base.alpha_composite(tile_img(CUR[t], PALS[r]))
        x, y = (t % 16) * (8 * S + 1), (t // 16) * (8 * S + 1)
        im.paste(base.convert("RGB").resize((8 * S, 8 * S), Image.NEAREST), (x, y))
        if t in van or t in col:
            d.rectangle([x, y, x + 8 * S - 1, y + 8 * S - 1], outline=col.get(t, (255, 255, 255)), width=2)
    key = Image.new("RGB", (760, 30 + 15 * len(rows)), GB.BG)
    d = ImageDraw.Draw(key)
    d.text((0, 0), "red: this draft redraws (T-537)   yellow: left, with the reason", fill=GB.INK, font=GB.font(12))
    for k, (who, kk, title, ts) in enumerate(rows):
        draws = sum(USE[t]["draws"] for t in ts if t in USE)
        maps = len({m for t in ts if t in USE for m in USE[t]["maps"]})
        d.text((0, 22 + 15 * k), "%-6s %-11s %3d tiles %4d draws %3d maps  %s" % (who, kk, len(ts), draws, maps,
                                                                                 title[:60]),
               fill=GB.INK if who == "T-537" else GB.SOFT, font=GB.font(10))
    path = os.path.join(outdir, "t537_census.png")
    GB.panel_row([im, key], ["primary/building today, 3x", "the census (item 6 of the vanilla-art census)"],
                 gap=20).save(path)
    return path


def tiles_png(tiles):
    return GB.tiles_png(tiles)


def check_engine():
    """T-446's rule: the engine's tiles.png against `--write --approved --pick X` for the one approved X; and the tiles
    this tool owns against gbabuilding.LATER, so neither tool can draw over the other"""
    pick = next(iter(APPROVED))
    new, owner, _ = draw(STYLES[pick])
    bad = 0
    if set(owner) != GB.LATER_T537:
        print("\n  !! gbabuilding.LATER_T537 and this tool's tiles disagree: only here %s, only there %s"
              % (sorted(set(owner) - GB.LATER_T537), sorted(GB.LATER_T537 - set(owner))))
        bad = 1
    off = [t for t in range(NT) if new[t] != CUR[t]]
    if off:
        print("\n  !! the engine differs from `--write --approved --pick %s` in %d tile%s (%s) -- find which side is right"
              % (pick, len(off), "s" if len(off) > 1 else "", off[:12]))
        return 1
    print("\n  the engine matches `--write --approved --pick %s`: %d tiles, no blink (the user, 2026-11-09)"
          % (pick, len(owner)))
    return bad


def main():
    if WRITE and ("--approved" not in ARGS or PICK not in APPROVED):
        print("  --write refused: T-537 is a draft until the user has picked a direction (APPROVED = %s)."
              % (sorted(APPROVED) or "{}"))
        print("  (When they have: put it in APPROVED, then --write --approved --pick X writes only the tiles a group "
              "owns into %s/tiles.png -- never a palette, never 262..266. BLINK is engine code and is not written.)" % BPATH)
        return 0
    van, mine, rows, stray = report()
    if WRITE:
        new, owner, _ = draw(STYLES[PICK])
        changed = [t for t in owner if new[t] != CUR[t]]
        tiles_png(new).save(os.path.join(PD, "tiles.png"), bits=4)     # 4-bit, 16 colours, as the engine keeps it
        print("  wrote %d tiles of direction %s into %s/tiles.png" % (len(changed), PICK, BPATH))
        return 0
    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        drawn = {}
        for X, D in STYLES.items():
            new, owner, canv = draw(D)
            frames = blink_frames(D)
            drawn[X] = (D, new, owner, frames)
            dd = os.path.join(DRAFT, X)
            os.makedirs(dd, exist_ok=True)
            tiles_png(new).save(os.path.join(dd, "tiles.png"))
            for n, f in enumerate(frames, 1):
                t2 = list(new)
                for t, px in f.items():
                    t2[t] = px
                fim = Image.new("P", (8 * len(BLINK), 8))
                fim.putpalette([c for rgb in PALS[0] for c in rgb])
                for k, t in enumerate(BLINK):
                    for p, v in enumerate(t2[t]):
                        fim.putpixel((k * 8 + p % 8, p // 8), v)
                fim.save(os.path.join(dd, "blink_%d.png" % n))
            changed = [t for t in owner if new[t] != CUR[t]]
            print("  %s %-18s %d tiles redrawn, 0 new tiles, 0 palette changes; blink %d tiles x 2 more frames"
                  % (X, D["title"], len(changed), len(BLINK)))
        json.dump(dict(ticket="T-537", status="DRAFT -- not in the engine", approved=sorted(APPROVED),
                       groups=[dict(who=w, key=k, what=t, tiles=ts) for w, k, t, ts in rows], stray=stray,
                       blink=BLINK), open(os.path.join(DRAFT, "groups.json"), "w"), indent=1)
        print("  wrote %s" % census_sheet(DRAFT, rows))
        for p in sheets(DRAFT, drawn):
            print("  wrote %s" % p)
    if len(APPROVED) == 1:
        return check_engine()
    return 0


if __name__ == "__main__":
    sys.exit(main())
