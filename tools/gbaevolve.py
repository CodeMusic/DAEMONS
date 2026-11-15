#!/usr/bin/env python3
"""T-566: EVOLVING, USING, LEARNING -- the Nintendo art they still draw (batch 6 of the 2026-11-14 re-census). DRAFT.

    python3 tools/gbaevolve.py                       # report: the census, each piece's contract, APPROVED (exit 1 on drift)
    python3 tools/gbaevolve.py --draft [DIR]         # every piece's A/B/C into DIR (gfx/drafts/t566_evolve/)
    python3 tools/gbaevolve.py --sheets DIR [--frames DIR]   # today beside A/B/C at 2x, in context
    python3 tools/gbaevolve.py --write --approved    # write APPROVED's picks into engineGba (none yet: nothing is written)

A new tool rather than a mode of gbabattleart.py: that one draws the nine terrains (argparse, terrain picks); this batch
is twelve small files across five scenes. gbabattleart's SHAPE note still holds here: the evolution scene loads
BATTLE_TERRAIN_PLAIN (BUILDING's drawing, ours since T-527) and parks BG3 at X 256, the terrain's second screen -- so
what shows around the scene before and after the moving background is already ours; only the moving background is not.

THE CENSUS (2026-11-15, engine b51f13d2f against pret upstream/master: every file below is byte-identical to pret's,
and every one is on screen -- filmed on the CONTENT debug ROM, tools/routes/film_t566_evolve.json):

  evo_bg    graphics/evolution_scene/bg.png (224 tiles) + bg.bin + bg2.bin: the evolution's moving background. BG1 and
            BG2 (two maps, 110 and 108 tiles, flipped into four quadrants about (128, 80)), blended 8/8 and circling
            in opposite phase; palette row 10 is written each step from transition.pal through sBgAnim_PalIndexes, so
            a PIXEL'S INDEX IS ITS PHASE: 13 lights first, 1 last, 14 and 15 always black. Every evolution.
  sparkle   graphics/evolution_scene/sparkle.png, 8x8: the spiral, the arc, the ring and the spray. Every evolution.
  psa_bg    graphics/pokemon_special_anim/bg.png (10 tiles) + bg.pal + bg_tm_hm.pal: the scene for an item used on a
            daemon from the bag (a candy, a vitamin, a stone, a TM): ten "levels", placed by distance from the centre
            (tile 1 the middle, 9 the corners), warm for items and cool for TMs.
  level_up  graphics/pokemon_special_anim/level_up.png, 8x16: the rising streaks of a level -- the item scene AND every
            level gained in battle (battle_controller_player.c).
  star      graphics/pokemon_special_anim/star.png, 16x16: the three stars of an item that works (the stone, filmed).
  dots      graphics/pokemon_special_anim/outward_spiral_dots.png, three 8x8: the spiral out of a used item.
  relearner graphics/interface/learn_move.png (32 tiles, 16 placed) + learn_move.bin: TWO ISLAND's ROUTINE ARCHIVIST,
            the lined mint panel behind the routine's TYPE, MP and EFFECT.
  arrows    graphics/learn_move/interface_sprites.png: its scroll arrows -- only tiles 4-7 (down, up) are ever drawn,
            and only when the list is longer than its window (none of the debug party's is: drawn offline).
  egg       graphics/pokemon/egg/front.png, icon.png, normal.pal, graphics/misc/egg_hatch.png, egg_shard.png: the EGG
            in the party (icon), its SUMMARY (front) and its hatch (the shaking egg, three cracks, four shards). Eggs
            come from FOUR ISLAND's day-care and the one handed over in the WATER LABYRINTH. T-452's lane, checked:
            nothing in docs/TODO.md, gfx/ or gfx/drafts/ plans a DAEMONS egg, so it is drafted here. The bible's line
            for it (vision.md, on an EGG): "There is nothing running in it yet."

  Dead (shown nowhere): evolution_scene/unused.pal, unused_tilemap.bin, gray_transition_intro.pal (all black, a
  fade's start); interface_sprites tiles 0-3 and 8-11 (sideways arrows and hearts no template uses). transition.pal
  is pret's ramp (black to pale blue) and stays: it is the phase table's colours, shared with nothing else.

THE RULES each draft keeps: every PNG its pret size and tile count, indexed, the same palette row and indices in their
roles; the item scene's tilemap, the relearner's map, every sprite's frame layout. No scene here has an edition split
(one palette for CONTENT and CONTEXT), so the sheets show the one. evo_bg is the one exception to "maps kept": pret's
two maps reuse its 224 tiles across the star's arms, so no other drawing fits them. A draft is an index FIELD per
layer, mirror-symmetric about (128, 80), cut into tiles each kept once (with its flips), and bg.bin and bg2.bin are
written to place them -- the same size, palette row 10, rows 20-31 as pret's, and at most 224 tiles in all (the report
prints how many); 1-13 by phase, 14 a black core. psa_bg: tile t is level t, symmetric under both flips. egg
icon: palette 1 of the shared icon palettes (pret's, shared with other daemons), so only its indices are drawn.
"""
import importlib.util, os, struct, sys
from PIL import Image, ImageDraw, ImageFont

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
GBA = os.path.join(ROOT, "engineGba")
DRAFT = os.path.join(ROOT, "gfx", "drafts", "t566_evolve")
FRAMES = os.path.join(ROOT, ".theatre", "routes", "film_t566_evolve")      # tools/routes/film_t566_evolve.json

PIECES = ["evo_bg", "sparkle", "psa_bg", "level_up", "star", "dots", "relearner", "arrows", "egg"]
APPROVED = {}          # T-566 is a DRAFT: nothing is written until the user picks
FILES = {
    "evo_bg":    ["graphics/evolution_scene/bg.png", "graphics/evolution_scene/bg.bin",
                  "graphics/evolution_scene/bg2.bin"],
    "sparkle":   ["graphics/evolution_scene/sparkle.png"],
    "psa_bg":    ["graphics/pokemon_special_anim/bg.png", "graphics/pokemon_special_anim/bg.pal",
                  "graphics/pokemon_special_anim/bg_tm_hm.pal"],
    "level_up":  ["graphics/pokemon_special_anim/level_up.png"],
    "star":      ["graphics/pokemon_special_anim/star.png"],
    "dots":      ["graphics/pokemon_special_anim/outward_spiral_dots.png"],
    "relearner": ["graphics/interface/learn_move.png"],
    "arrows":    ["graphics/learn_move/interface_sprites.png"],
    "egg":       ["graphics/pokemon/egg/front.png", "graphics/pokemon/egg/icon.png", "graphics/pokemon/egg/normal.pal",
                  "graphics/misc/egg_hatch.png", "graphics/misc/egg_shard.png"],
}
NAMES = {
    "evo_bg":    {"A": "SQUARE WAVE", "B": "OSCILLOSCOPE", "C": "BIT GRID"},
    "sparkle":   {"A": "THE BIT", "B": "THE PIXEL", "C": "THE NOTE"},
    "psa_bg":    {"A": "GRAPH PAPER", "B": "RESOLVING", "C": "SCANLINES"},
    "level_up":  {"A": "CARETS", "B": "ONES", "C": "THE STEP"},
    "star":      {"A": "THE MARK", "B": "THE CURSOR", "C": "THE QUAVER"},
    "dots":      {"A": "0 1 .", "B": "NOTES", "C": "PIXELS"},
    "relearner": {"A": "GRAPH PAPER", "B": "RULED", "C": "SCANLINES"},
    "arrows":    {"A": "CARET", "B": "CHEVRON", "C": "STEPPED"},
    "egg":       {"A": "THE SHELL", "B": "SEALED", "C": "THE STAVE"},
}
LINES = {
    "evo_bg":    {"A": "square rings on one layer, diamonds on the other: the light leaves the daemon as a square wave",
                  "B": "a mirrored sound wave on each layer, half a period apart: the change heard as it happens",
                  "C": "rings built of 8x8 cells on both, one offset by half a cell: a screen redrawn in blocks"},
    "sparkle":   {"A": "a white 1: the bits that spiral in are bits",
                  "B": "a lit pixel with a halo: one square of the screen",
                  "C": "a quaver: the notes the splash throws, thrown here too"},
    "psa_bg":    {"A": "graph paper whose crossings grow and darken away from the daemon",
                  "B": "a pixel block per cell, growing outward: the picture resolving",
                  "C": "scanlines, thicker and darker toward the edge: a CRT around the daemon"},
    "level_up":  {"A": "two stacked carets climbing: up, as a terminal draws it",
                  "B": "a column of 1s climbing", "C": "a rising staircase line: one step up"},
    "star":      {"A": "the CodeMusic ring, as the splash's star (T-564 A, approved)",
                  "B": "a block cursor with its trail (T-564 B)", "C": "the white quaver (T-564 C)"},
    "dots":      {"A": "a 0, a 1 and a dot, shrinking as they spiral out", "B": "a quaver, a note head, a dot",
                  "C": "a 4-pixel square, a 2-pixel one, one pixel"},
    "relearner": {"A": "the house paper with one dot a tile (the INDEX's graph paper) and dotted rules, a navy frame",
                  "B": "plain paper, solid teal rules under each line of the EFFECT",
                  "C": "paper with a faint scanline every fourth row, solid rules"},
    "arrows":    {"A": "the same triangle in teal with a slate outline", "B": "an open chevron, outline only",
                  "C": "a triangle in 2-pixel steps, terminal-blocky"},
    "egg":       {"A": "a paper-white shell flecked with teal 0s and 1s; it cracks along a fault",
                  "B": "a grey capsule with a seam and an unlit lamp: a process not started; the lamp lights as it opens",
                  "C": "a cream shell wrapped in a five-line stave with one note on it: music not yet played"},
}
RECOMMENDED = {"evo_bg": "A", "sparkle": "A", "psa_bg": "A", "level_up": "A", "star": "A", "dots": "A",
               "relearner": "A", "arrows": "A", "egg": "A"}

# the house colours (gbamenus.py's TERMINAL family)
SLATE_OUT, SLATE_MID, SLATE_LIGHT = (32, 40, 52), (88, 104, 120), (176, 192, 204)
TEAL, TEAL_DK, PAPER = (112, 208, 184), (40, 136, 116), (248, 248, 244)
NAVY = (24, 41, 74)


def P(path):
    return os.path.join(GBA, path)


def _pal(im):
    p = im.getpalette()
    return [tuple(p[i * 3:i * 3 + 3]) for i in range(16)]


def _jasc(path):
    v = open(path).read().split()
    return [tuple(int(x) for x in v[3 + i * 3:6 + i * 3]) for i in range(int(v[2]))]


def _jasc_text(pal):
    pal = list(pal) + [(0, 0, 0)] * (16 - len(pal))
    return "JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in pal[:16])


def _img(w, h, rows_or_px, pal):
    im = Image.new("P", (w, h), 0)
    pal = list(pal) + [(0, 0, 0)] * (16 - len(pal))
    im.putpalette([v for c in pal[:16] for v in c] + [0] * (768 - 48))
    im.putdata(rows_or_px)
    return im


def _grid(w, h, v=0):
    return [[v] * w for _ in range(h)]


def _stamp(g, rows, x0, y0, legend):
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c in legend and 0 <= y0 + y < len(g) and 0 <= x0 + x < len(g[0]):
                g[y0 + y][x0 + x] = legend[c]


def _flat(g):
    return [v for row in g for v in row]


def _map(path):
    d = open(path, "rb").read()
    return struct.unpack("<%dH" % (len(d) // 2), d)


# ================================================================================================= the evolution bg
EVO_W, EVO_ROWS = 256, 20          # the maps' visible part: 32x20 tiles, centre (128, 80)


def _band(d, step=9.0, core=3.0, core_index=14):
    if d < core:
        return core_index
    return max(1, 13 - int((d - core) / step))


def _evo_fields(d):
    import math
    f1, f2 = _grid(EVO_W, EVO_ROWS * 8), _grid(EVO_W, EVO_ROWS * 8)
    for y in range(EVO_ROWS * 8):
        for x in range(EVO_W):
            dx, dy = abs(x - 127.5), abs(y - 79.5)
            if d == "A":
                a, b = max(dx, dy), (dx + dy) * 0.72
            elif d == "B":
                ph = (int(dx) % 64) / 64.0                        # a triangle wave, period 64, slope 1: its tiles
                tri = 1 - abs(2 * ph - 1)                         # repeat along the diagonal (224 is the budget)
                env1, env2 = 32 * tri, 32 * (1 - tri)
                a, b = abs(dy - env1) * 1.5, abs(dy - env2) * 1.5
            else:
                qx, qy = (int(dx) // 8) * 8 + 4, (int(dy) // 8) * 8 + 4
                rx, ry = (int(dx + 4) // 8) * 8, (int(dy + 4) // 8) * 8
                a, b = math.hypot(qx, qy), math.hypot(rx, ry) * 1.04
            ci = 13 if d == "B" else 14          # B's trace is the first thing lit, not a black line
            f1[y][x], f2[y][x] = _band(a, core_index=ci), _band(b, core_index=ci)
    return f1, f2


def evo_bg(d):
    """Cut the two fields into tiles, each kept once (with its flips), and write the two maps that place them: the
    maps keep their size, rows 20-31 as pret's, and palette row 10. Returns ({rel: file}, tiles used of 224)."""
    old = Image.open(P("graphics/evolution_scene/bg.png"))
    tiles = [tuple([0] * 64)]
    index = {tiles[0]: (0, 0)}
    maps = {}
    for field, binf in zip(_evo_fields(d), ("bg.bin", "bg2.bin")):
        ents = list(_map(P("graphics/evolution_scene/" + binf)))
        for r in range(EVO_ROWS):
            for c in range(32):
                cut = [field[r * 8 + y][c * 8 + x] for y in range(8) for x in range(8)]
                key = tuple(cut)
                if key not in index:
                    t = len(tiles)
                    tiles.append(key)
                    for hf in (0, 1):
                        for vf in (0, 1):
                            k = tuple(cut[(7 - y if vf else y) * 8 + (7 - x if hf else x)] for y in range(8) for x in range(8))
                            index.setdefault(k, (t, (0x400 if hf else 0) | (0x800 if vf else 0)))
                t, fl = index[key]
                ents[r * 32 + c] = t | fl | (10 << 12)
        maps[binf] = struct.pack("<%dH" % len(ents), *ents)
    used = len(tiles)
    tiles += [tuple([0] * 64)] * max(0, 224 - len(tiles))
    px = []
    for ty in range(28):
        for y in range(8):
            for tx in range(8):
                px += list(tiles[ty * 8 + tx][y * 8:(y + 1) * 8]) if ty * 8 + tx < len(tiles) else [0] * 8
    return {"graphics/evolution_scene/bg.png": _img(64, 224, px, _pal(old)),
            "graphics/evolution_scene/bg.bin": maps["bg.bin"],
            "graphics/evolution_scene/bg2.bin": maps["bg2.bin"]}, used


def evo_render(png_im, stage, off1=(8, 16), off2=(8, 16), maps=None):
    """The scene's background as the hardware blends it: BG1 and BG2 8/8, palette row 10 at a phase stage."""
    trans = _jasc(P("graphics/evolution_scene/transition.pal"))
    idx = _phase_row(stage)
    pal = [trans[i] for i in idx]
    w, h = png_im.size
    raw = list(png_im.getdata())
    ts = [[raw[(ty * 8 + y) * w + tx * 8 + x] for y in range(8) for x in range(8)]
          for ty in range(h // 8) for tx in range(w // 8)]

    def layer(binf, off):
        data = (maps or {}).get(binf) or open(P("graphics/evolution_scene/" + binf), "rb").read()
        ents = struct.unpack("<%dH" % (len(data) // 2), data)
        out = Image.new("RGB", (240, 160)); op = out.load()
        for sy in range(160):
            for sx in range(240):
                X, Y = (sx + off[0]) % 256, (sy + off[1]) % 256
                e = ents[(Y // 8) * 32 + X // 8]
                t, hf, vf = e & 0x3FF, e & 0x400, e & 0x800
                x, y = X % 8, Y % 8
                v = ts[t][(7 - y if vf else y) * 8 + (7 - x if hf else x)] if t < len(ts) and (e >> 12) == 10 else 0
                op[sx, sy] = _gba(pal[v])
        return out
    return Image.blend(layer("bg.bin", off1), layer("bg2.bin", off2), 0.5)


def _phase_row(stage):
    """sBgAnim_PalIndexes' row STAGE, read from the engine's own table."""
    src = open(P("src/evolution_scene.c")).read()
    body = src[src.index("sBgAnim_PalIndexes[][16]"):]
    body = body[body.index("{") + 1:body.index("};")]
    rows = [[int(v) for v in r.split(",") if v.strip()] for r in body.replace("}", "").split("{")[1:]]
    return rows[min(stage, len(rows) - 1)]


# ================================================================================================= small sprites
def sparkle(d):
    old = Image.open(P("graphics/evolution_scene/sparkle.png"))
    g = _grid(8, 8)
    if d == "A":
        _stamp(g, ["...ff...", "..eff...", ".d.ff...", "...ff...", "...ff...", "...ff...", "..ffff..", "..dddd.."], 0, 0,
               {"f": 15, "e": 14, "d": 13})
    elif d == "B":
        _stamp(g, ["........", "...dd...", "..effe..", ".dffffd.", ".dffffd.", "..effe..", "...dd...", "........"], 0, 0,
               {"f": 15, "e": 14, "d": 13})
    else:
        _stamp(g, ["...ff...", "...fee..", "...f.ed.", "...f..d.", "...f....", ".fff....", "ffff....", ".dd....."], 0, 0,
               {"f": 15, "e": 14, "d": 13})
    return {"graphics/evolution_scene/sparkle.png": _img(8, 8, _flat(g), _pal(old))}


LEVEL_PAL = [(0, 0, 0)] * 8 + [(96, 216, 240), (0, 144, 176)] + [(0, 0, 0)] * 6


def level_up(d):
    g = _grid(8, 16)
    if d == "A":
        _stamp(g, ["...8....", "..989...", ".9...9..", "........", "...8....", "..989...", ".9...9..", "........",
                   "...8....", "..989...", ".9...9..", "........", "...8....", "..989...", ".9...9..", "........"],
               0, 0, {"8": 8, "9": 9})
    elif d == "B":
        _stamp(g, ["...8....", "..88....", "...8....", "...8....", "..888...", "........", "...9....", "..99....",
                   "...9....", "...9....", "..999...", "........", "...9....", "..99....", "...9....", "..999..."],
               0, 0, {"8": 8, "9": 9})
    else:
        _stamp(g, [".....88.", ".....8..", ".....8..", "...888..", "...8....", "...8....", ".889....", ".9......",
                   ".9......", ".9......", ".9......", ".9......", ".9......", ".9......", ".9......", "........"],
               0, 0, {"8": 8, "9": 9})
    return {"graphics/pokemon_special_anim/level_up.png": _img(8, 16, _flat(g), LEVEL_PAL)}


def _gbatitle():
    spec = importlib.util.spec_from_file_location("gbatitle", os.path.join(TOOLS, "gbatitle.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def star(d):
    """The splash's star drafts (T-564), the same objects: A is the approved one."""
    t = _gbatitle()
    im = t.t564_star(d)["graphics/intro/game_freak/star.png"]
    return {"graphics/pokemon_special_anim/star.png": _img(16, 16, list(im.getdata()), t.T564_STAR_PAL)}


_ZERO = [".111.", "1...1", "1..11", "1.1.1", "11..1", "1...1", ".111."]
_ONE = ["..1..", ".11..", "..1..", "..1..", "..1..", "..1..", ".111."]


def dots(d):
    old = Image.open(P("graphics/pokemon_special_anim/outward_spiral_dots.png"))
    g = _grid(8, 24)
    if d == "A":
        _stamp(g, _ZERO, 1, 0, {"1": 1}); _stamp(g, _ONE, 1, 8, {"1": 1}); _stamp(g, ["11", "11"], 3, 19, {"1": 1})
    elif d == "B":
        _stamp(g, ["...1.", "...11", "...1.", "...1.", ".111.", "1111.", ".11.."], 1, 0, {"1": 1})
        _stamp(g, [".11.", "1111", "1111", ".11."], 2, 10, {"1": 1})
        _stamp(g, ["1"], 4, 20, {"1": 1})
    else:
        _stamp(g, ["1111"] * 4, 2, 2, {"1": 1}); _stamp(g, ["11"] * 2, 3, 11, {"1": 1}); _stamp(g, ["1"], 4, 20, {"1": 1})
    pal = _pal(old); pal[1] = TEAL_DK                 # pret's white is lost on paper: the dots in the house teal
    return {"graphics/pokemon_special_anim/outward_spiral_dots.png": _img(8, 24, _flat(g), pal)}


ARROW_PAL = [(0, 255, 0), TEAL, TEAL_DK, (213, 0, 0), (197, 0, 0)] + [(0, 0, 0)] * 8 + [SLATE_LIGHT, SLATE_OUT, PAPER]


def arrows(d):
    """Tiles 4-7 only (the down and up arrows, 16x8 each); the dead tiles are left as they are."""
    old = Image.open(P("graphics/learn_move/interface_sprites.png"))
    px = list(old.getdata())
    if d == "A":
        down = ["................", "...eeeeeeeeee...", "...e22222222e...", "....e222222e....", ".....e2222e.....",
                "......e22e......", ".......ee.......", "................"]
    elif d == "B":
        down = ["................", "...ee......ee...", "...e2e....e2e...", "....e2e..e2e....", ".....e2ee2e.....",
                "......e22e......", ".......ee.......", "................"]
    else:
        down = ["................", "..eeeeeeeeeeee..", "..e2222222222e..", "....e222222e....", "....ee2222ee....",
                "......e22e......", "......eeee......", "................"]
    up = list(reversed(down))
    for frame, rows in ((4, down), (6, up)):
        for half in range(2):
            t = frame + half
            for y in range(8):
                for x in range(8):
                    c = rows[y][half * 8 + x]
                    px[(t * 8 + y) * 8 + x] = {"e": 14, "2": 2, "d": 13}.get(c, 0)
    return {"graphics/learn_move/interface_sprites.png": _img(8, 96, px, ARROW_PAL)}


# ================================================================================================= the item scene bg
PSA_ITEM_PAL = {
    "A": [(0, 0, 0), (250, 246, 236), (238, 242, 230), (226, 236, 226), (214, 232, 222), (202, 226, 218),
          (190, 220, 214), (0, 0, 0), (176, 214, 208), (0, 0, 0), (162, 206, 202), (146, 196, 194), (240, 242, 232)],
}
PSA_TM_PAL = {
    "A": [(0, 0, 0), (240, 244, 250), (228, 234, 246), (216, 226, 242), (204, 216, 238), (192, 208, 234),
          (180, 200, 230), (0, 0, 0), (166, 190, 226), (0, 0, 0), (152, 180, 220), (136, 168, 212), (230, 236, 246)],
}
GLYPH = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 10, 9: 11}      # tile -> its colour index (pret's roles)


def _psa_tile(d, t):
    if t == 0:
        return [0] * 64
    bg = 12 if t == 9 else 1
    g = _grid(8, 8, bg)
    if t == 1:
        return _flat(g)
    c, k = GLYPH[t], t - 1                 # k 1..8: how far out
    if d == "A":                           # graph paper: a crossing, its arms longer outward
        arm = min(3, (k + 1) // 2)
        for i in range(3 - arm + 1, 5 + arm - 1):
            g[3][i] = g[4][i] = c if k > 4 else g[3][i]
            g[i][3] = g[i][4] = c
        if k <= 4:
            for i in range(3 - arm + 1, 5 + arm - 1):
                g[3][i] = g[4][i] = c
        g[3][3] = g[3][4] = g[4][3] = g[4][4] = c
        if k <= 2:
            g = _grid(8, 8, bg); g[3][3] = g[3][4] = g[4][3] = g[4][4] = c
    elif d == "B":                         # resolving: a centred block, 2 px at the middle to 8 at the corners
        s = min(8, 2 * ((k + 1) // 2) + (2 if k > 6 else 0))
        o = (8 - s) // 2
        for y in range(o, o + s):
            for x in range(o, o + s):
                g[y][x] = c
    else:                                  # scanlines: rows from the middle out, more of them outward
        rows = [[3, 4], [3, 4], [2, 5, 3, 4], [2, 5, 3, 4], [1, 6, 3, 4], [1, 6, 2, 5, 3, 4],
                [0, 7, 2, 5, 3, 4], [0, 7, 1, 6, 2, 5, 3, 4]][k - 1]
        for y in set(rows):
            g[y] = [c] * 8
    return _flat(g)


def psa_bg(d):
    pal_i = PSA_ITEM_PAL["A"]; pal_t = PSA_TM_PAL["A"]
    px = []
    for t in range(10):
        px += _psa_tile(d, t)
    return {"graphics/pokemon_special_anim/bg.png": _img(8, 80, px, pal_i),
            "graphics/pokemon_special_anim/bg.pal": _jasc_text(pal_i),
            "graphics/pokemon_special_anim/bg_tm_hm.pal": _jasc_text(pal_t)}


# ================================================================================================= the relearner
LM_PAL = [(0, 0, 0), PAPER, (214, 222, 228), TEAL_DK, SLATE_MID, PAPER] + [(255, 0, 255)] * 7 + \
         [(123, 131, 148), (255, 255, 255), NAVY]


def relearner(d):
    """Each tile keeps its geometry by role: 15 the dark frame and shadow, 4 the right and bottom edge, 3 the top's
    light rows and the EFFECT's rules, 1 and 2 the fill (pret's stripes) -- the fill and the rules are what change."""
    old = Image.open(P("graphics/interface/learn_move.png"))
    w = old.width
    src = list(old.getdata()); out = list(src)
    rule_tiles = {0x11, 0x12, 0x13, 0x14}
    for i, v in enumerate(src):
        y, x = divmod(i, w)
        t = (y // 8) * (w // 8) + x // 8
        ty, tx = y % 8, x % 8
        if v in (1, 2):
            if d == "A":
                out[i] = 2 if (tx == 7 and ty == 7) else 1
            elif d == "B":
                out[i] = 1
            else:
                out[i] = 2 if ty % 4 == 3 else 1
        elif v == 3:
            if t in rule_tiles and d == "A":
                out[i] = 3 if tx % 2 == 0 else 1
            elif t not in rule_tiles:
                out[i] = 5 if ty in (2,) else 3      # the top's two light rows: paper over teal
    return {"graphics/interface/learn_move.png": _img(w, old.height, out, LM_PAL)}


# ================================================================================================= the egg
EGG_PAL = {
    "A": [(164, 255, 148), SLATE_OUT, (196, 202, 196), PAPER, (226, 230, 222), (184, 192, 186), TEAL, TEAL_DK,
          (88, 104, 120)],
    "B": [(164, 255, 148), SLATE_OUT, (128, 140, 152), (220, 226, 232), (186, 196, 206), (150, 162, 176), (72, 84, 96),
          (112, 208, 184), (40, 52, 64)],
    "C": [(164, 255, 148), (56, 44, 40), (200, 180, 140), (250, 242, 222), (238, 224, 190), (214, 196, 156), NAVY,
          (120, 112, 104), (96, 80, 64)],
}
ICON_ROLE = {"out": 15, "light": 3, "mid": 2, "dark": 1, "acc": 5, "acc2": 4}    # icon palette 1's own colours


def _egg_shape(w, h, cx, cy, rx, ry):
    """An egg: an ellipse, its top a little narrower. Returns {(x, y): (nx, ny)} inside, normalised."""
    inside = {}
    for y in range(h):
        for x in range(w):
            ny = (y + 0.5 - cy) / ry
            k = 1.0 - 0.13 * max(0.0, -ny)
            nx = (x + 0.5 - cx) / (rx * k)
            if nx * nx + ny * ny <= 1.0:
                inside[(x, y)] = (nx, ny)
    return inside


def _egg_draw(d, w, h, cx, cy, rx, ry, crack=0, roles=None, glyphs=True):
    R = roles or {"out": 1, "light": 3, "mid": 4, "dark": 5, "acc": 6, "acc2": 7, "seam": 8, "core": 2}
    g = _grid(w, h)
    ins = _egg_shape(w, h, cx, cy, rx, ry)
    for (x, y), (nx, ny) in ins.items():
        lit = -0.55 * nx - 0.65 * ny
        g[y][x] = R["light"] if lit > 0.35 else R["mid"] if lit > -0.35 else R["dark"]
    for (x, y) in ins:
        for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + ax, y + ay) not in ins:
                g[y][x] = R["out"]
                break
    big = rx >= 10
    if d == "A" and glyphs:
        marks = [(-0.35, -0.25, "1"), (0.3, 0.05, "0"), (-0.1, 0.45, "1"), (0.35, -0.5, "0")] if big else \
                [(-0.3, -0.1, "."), (0.3, 0.3, ".")]
        for mx, my, ch in marks:
            x0, y0 = int(cx + mx * rx), int(cy + my * ry)
            rows = {"1": [".a.", "aa.", ".a.", ".a.", "aaa"], "0": [".a.", "a.a", "a.a", "a.a", ".a."], ".": ["a"]}[ch]
            _stamp(g, rows, x0 - 1, y0 - 2, {"a": R["acc"]})
    elif d == "B":
        sy = int(cy + 0.1 * ry)
        for (x, y) in ins:
            if y == sy and g[y][x] != R["out"]:
                g[y][x] = R["seam"]
        lx, ly = int(cx + 0.35 * rx), sy - max(2, int(0.35 * ry))
        lamp = R["acc2"] if crack else R["seam"]
        if big:
            _stamp(g, [".o.", "olo", ".o."], lx - 1, ly - 1, {"o": R["out"], "l": lamp})
        else:
            g[ly][lx] = lamp
    elif d == "C" and glyphs:
        step = 3 if big else 2
        top = int(cy - 2 * step)
        for k in range(5 if big else 3):
            yy = top + k * step
            for (x, y) in ins:
                if y == yy and g[y][x] != R["out"]:
                    g[y][x] = R["acc2"] if big else R["acc"]
        if big:
            nx0 = int(cx + 0.15 * rx)
            _stamp(g, ["..a", "..a", "..a", "..a", "aaa", "aa."], nx0, top + step - 4, {"a": R["acc"]})
    if crack:
        import random
        rnd = random.Random(566 + crack)
        paths = [(int(cx - rx * 0.5), int(cy - ry * 0.15))]
        if crack >= 2:
            paths.append((int(cx + rx * 0.45), int(cy - ry * 0.45)))
        if crack >= 3:
            paths.append((int(cx), int(cy + ry * 0.5)))
        for (x, y) in paths:
            for s in range(4 + crack * 3):
                if (x, y) in ins:
                    g[y][x] = R["out"]
                x += rnd.choice((1, 1, 0, -1)) if s % 2 else 1
                y += rnd.choice((-1, 0, 1))
    return g


def egg(d):
    pal = EGG_PAL[d] + [(0, 0, 0)] * 7
    front = _egg_draw(d, 64, 64, 32, 33, 11.5, 12.5)
    hatch = []
    for f in range(4):
        hatch += _flat(_egg_draw(d, 32, 32, 16, 17, 11.5, 12.5, crack=f))
    shards = _grid(32, 8)
    R = {"out": 1, "light": 3, "mid": 4, "dark": 5}
    shapes = [["..oo....", ".oLLo...", "oLLLMo..", "oLMMMo..", ".oMMo...", "..oo...."],
              ["....oo..", "...oLLo.", "..oLLMo.", ".oLMMMo.", ".oMMDo..", "..ooo..."],
              [".oooo...", "oLLLMo..", "oLMMMDo.", ".oMMDDo.", "..oDDo..", "...oo..."],
              ["...ooo..", "..oLLMo.", ".oLMMDo.", "oMMMDo..", "oDDDo...", ".ooo...."]]
    for k, rows in enumerate(shapes):
        _stamp(shards, rows, k * 8, 1, {"o": R["out"], "L": R["light"], "M": R["mid"], "D": R["dark"]})
    old_icon = Image.open(P("graphics/pokemon/egg/icon.png"))
    icon = []
    for f, (cy, rx) in enumerate(((19.5, 6.0), (20.0, 6.5))):
        icon += _flat(_egg_draw(d, 32, 32, 16, cy, rx, 7.5 if f == 0 else 7.0, roles=dict(ICON_ROLE, seam=14, core=2),
                                glyphs=True))
    return {"graphics/pokemon/egg/front.png": _img(64, 64, _flat(front), pal),
            "graphics/misc/egg_hatch.png": _img(32, 128, hatch, pal),
            "graphics/misc/egg_shard.png": _img(32, 8, _flat(shards), pal),
            "graphics/pokemon/egg/icon.png": _img(32, 64, icon, _pal(old_icon)),
            "graphics/pokemon/egg/normal.pal": _jasc_text(pal)}


DRAW = {"evo_bg": lambda d: evo_bg(d)[0], "sparkle": sparkle, "psa_bg": psa_bg, "level_up": level_up, "star": star,
        "dots": dots, "relearner": relearner, "arrows": arrows, "egg": egg}


# ================================================================================================= the contract
def check(piece, files):
    errs = []
    for rel, v in files.items():
        if rel.endswith(".bin"):
            if len(v) != os.path.getsize(P(rel)):
                errs.append("%s is %d bytes, pret's %d" % (rel, len(v), os.path.getsize(P(rel))))
            continue
        if rel.endswith(".pal"):
            if len(v.split()) != 3 + 48:
                errs.append("%s is not 16 colours" % rel)
            continue
        old = Image.open(P(rel))
        if v.size != old.size:
            errs.append("%s is %s, pret's %s" % (rel, v.size, old.size))
        if v.mode != "P":
            errs.append("%s is not indexed" % rel)
        px = set(v.getdata())
        if max(px) > 15:
            errs.append("%s uses index %d" % (rel, max(px)))
        if piece == "sparkle" and px - {0, 13, 14, 15}:
            errs.append("sparkle draws %s: its palette's lit shades are 13-15" % sorted(px - {0, 13, 14, 15}))
        if piece == "level_up" and px - {0, 8, 9}:
            errs.append("level_up draws %s, not 8 and 9" % sorted(px - {0, 8, 9}))
        if piece == "dots" and px - {0, 1}:
            errs.append("dots draws %s, not 1" % sorted(px - {0, 1}))
        if rel.endswith("egg/icon.png") and px - {0, 1, 2, 3, 4, 5, 14, 15}:
            errs.append("egg icon uses %s outside its roles in icon palette 1" % sorted(px - {0, 1, 2, 3, 4, 5, 14, 15}))
        if piece == "arrows":
            a, b = list(old.getdata()), list(v.getdata())
            if a[:4 * 64] != b[:4 * 64] or a[8 * 64:] != b[8 * 64:]:
                errs.append("arrows changed a tile other than 4-7")
        if piece == "psa_bg" and list(v.getdata())[:64] != [0] * 64:
            errs.append("psa_bg tile 0 must stay empty")
    if piece == "evo_bg":
        n = sum(1 for t in range(224) if any(files["graphics/evolution_scene/bg.png"].crop(
            ((t % 8) * 8, (t // 8) * 8, (t % 8) * 8 + 8, (t // 8) * 8 + 8)).getdata()))
        if n + 1 > 224:
            errs.append("evo_bg needs %d tiles, 224 allowed" % (n + 1))
    return errs


def save(files, root):
    for rel, v in files.items():
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if isinstance(v, str):
            open(dst, "w").write(v)
        elif isinstance(v, bytes):
            open(dst, "wb").write(v)
        else:
            v.save(dst)


def draft(out):
    for piece in PIECES:
        for d in "ABC":
            files = DRAW[piece](d)
            errs = check(piece, files)
            if errs:
                sys.exit("gbaevolve: %s %s breaks its contract: %s" % (piece, d, "; ".join(errs)))
            save(files, os.path.join(out, d))
            note = ""
            if piece == "evo_bg" and evo_bg(d)[1] > 224:
                sys.exit("gbaevolve: evo_bg %s needs %d tiles, 224 allowed" % (d, evo_bg(d)[1]))
            if piece == "evo_bg":
                note = "  (%d of 224 tiles placed)" % evo_bg(d)[1]
            print("  %-9s %s %-13s %s%s" % (piece, d, NAMES[piece][d], ", ".join(sorted(files)), note))
    print("  DRAFT -- nothing in the engine; recommended: %s"
          % ", ".join("%s %s" % (p, RECOMMENDED[p]) for p in PIECES))


def report():
    print("gbaevolve (T-566): evolving, using, learning. APPROVED: %s" % (APPROVED or "none -- nothing is written"))
    for piece in PIECES:
        for d in "ABC":
            files = DRAW[piece](d)
            errs = check(piece, files)
            extra = (" (%d of 224 tiles placed%s)" % (evo_bg(d)[1], "" if evo_bg(d)[1] <= 224 else ": OVER")) \
                if piece == "evo_bg" else ""
            print("  %-9s %s %-13s %s%s" % (piece, d, NAMES[piece][d], "ok" if not errs else "; ".join(errs), extra))
    drift = []
    for piece, d in APPROVED.items():
        for rel, v in DRAW[piece](d).items():
            dst = P(rel)
            same = os.path.exists(dst) and (open(dst).read() == v if isinstance(v, str) else
                                             open(dst, "rb").read() == v if isinstance(v, bytes)
                                             else list(Image.open(dst).getdata()) == list(v.getdata()))
            if not same:
                drift.append(rel)
    for rel in drift:
        print("  DRIFT: engineGba/%s is not what --write --approved makes" % rel)
    return 1 if drift else 0


# ================================================================================================= the sheets
def _gba(c):
    return tuple(((v >> 3) << 3) | ((v >> 3) >> 2) for v in c[:3])


def _bg_layer(img, binf, pal, cols=32, rows=20, pals=None):
    """A 4bpp BG: (RGB, mask of drawn pixels), tile index 0 included (it may hold art)."""
    w, h = img.size
    raw = list(img.getdata())
    ts = [[raw[(ty * 8 + y) * w + tx * 8 + x] for y in range(8) for x in range(8)]
          for ty in range(h // 8) for tx in range(w // 8)]
    ents = _map(binf)
    out = Image.new("RGB", (240, 160)); m = Image.new("L", (240, 160)); op, mp = out.load(), m.load()
    for i, e in enumerate(ents):
        r, c = divmod(i, 32)
        if c >= 30 or r >= 20:
            continue
        t, hf, vf, pn = e & 0x3FF, e & 0x400, e & 0x800, e >> 12
        if t >= len(ts) or (pals is not None and pn not in pals):
            continue
        for y in range(8):
            for x in range(8):
                v = ts[t][(7 - y if vf else y) * 8 + (7 - x if hf else x)]
                if v:
                    op[c * 8 + x, r * 8 + y] = _gba(pal[v]); mp[c * 8 + x, r * 8 + y] = 255
    return out, m


def _swap(frame, today, new, tol=10):
    out = frame.copy(); fp, tp, np_, op = frame.load(), today[0].load(), new[0].load(), out.load()
    tm = today[1].load()
    for y in range(160):
        for x in range(240):
            if tm[x, y] and all(abs(fp[x, y][i] - tp[x, y][i]) <= tol for i in range(3)):
                op[x, y] = np_[x, y]
    return out


def _sprite_rgba(im, pal=None):
    pal = pal or _pal(im)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); op = out.load(); sp = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if sp[x, y]:
                op[x, y] = _gba(pal[sp[x, y]]) + (255,)
    return out


def _find(frame, spr, tol=14, accept=0.08):
    """Where a sprite (RGBA) sits in a frame: the offset where every opaque pixel matches. None if nowhere."""
    import numpy as np
    F = np.asarray(frame.convert("RGB")).astype(int)
    S = np.asarray(spr).astype(int)
    ys, xs = np.nonzero(S[:, :, 3])
    if len(ys) == 0:
        return None
    cols = S[ys, xs, :3]
    best = None
    for oy in range(-ys.min(), 160 - ys.max()):
        for ox in range(-xs.min(), 240 - xs.max()):
            diff = np.abs(F[ys + oy, xs + ox] - cols).max(axis=1)
            bad = int((diff > tol).sum())
            if best is None or bad < best[0]:
                best = (bad, ox, oy)
                if bad == 0:
                    return ox, oy
    if best and best[0] <= len(ys) * accept:
        return best[1], best[2]
    return None


def _replace(frame, old_spr, new_spr, at):
    """Erase OLD at AT (each pixel filled from the nearest pixel left of it that is not the sprite's), draw NEW."""
    out = frame.convert("RGB").copy(); op = out.load(); sp = old_spr.load()
    ox, oy = at
    for y in range(old_spr.height):
        for x in range(old_spr.width):
            if sp[x, y][3] and 0 <= ox + x < 240 and 0 <= oy + y < 160:
                k = x
                while k >= 0 and sp[k, y][3]:
                    k -= 1
                op[ox + x, oy + y] = op[max(0, ox + k), oy + y] if k >= 0 else op[max(0, ox - 1), oy + y]
    out.paste(new_spr, (ox, oy), new_spr)
    return out


def _font():
    try:
        return ImageFont.load_default(size=15), ImageFont.load_default(size=22)
    except TypeError:
        f = ImageFont.load_default(); return f, f


def _sheet(path, title, sub, cols, rows, captions):
    """cols: labels; rows[r][c] an Image. One column per today/A/B/C, rows of views."""
    font, big = _font()
    pad, head = 10, 70
    cw = [max(rows[r][c].width for r in range(len(rows))) for c in range(len(cols))]
    rh = [max(rows[r][c].height for c in range(len(cols))) for r in range(len(rows))]
    W = pad + sum(w + pad for w in cw); H = head + sum(h + 30 for h in rh) + pad
    sh = Image.new("RGB", (max(W, 900), H), (22, 22, 28)); dr = ImageDraw.Draw(sh)
    dr.text((pad, 8), title, fill=(240, 240, 240), font=big)
    dr.text((pad, 38), sub, fill=(200, 200, 210), font=font)
    y = head
    for r in range(len(rows)):
        x = pad
        for c in range(len(cols)):
            dr.text((x, y), cols[c] if r == 0 else captions[r], fill=(235, 220, 140) if r == 0 else (170, 170, 180),
                    font=font)
            sh.paste(rows[r][c], (x, y + 20))
            x += cw[c] + pad
        if r == 0:
            dr.text((x, y + 24), captions[0], fill=(150, 150, 160), font=font)
        y += rh[r] + 30
    sh.save(path)
    print("  sheet %s" % path)
    return path


X2 = lambda im: im.convert("RGB").resize((im.width * 2, im.height * 2), Image.NEAREST)
X = lambda im, k: im.resize((im.width * k, im.height * k), Image.NEAREST)


def _fr(fdir, stop, name):
    return Image.open(os.path.join(fdir, "%02d" % stop, name)).convert("RGB")


def _label(cols):
    return ["TODAY (pret's)" if d == "today" else "%s  %s" % (d, n) for d, n in cols]


def sheets(out_dir, fdir):
    os.makedirs(out_dir, exist_ok=True)
    made = []
    DS = ["today", "A", "B", "C"]

    def files(piece, d):
        return {rel: (open(P(rel)).read() if rel.endswith(".pal") else open(P(rel), "rb").read()
                      if rel.endswith(".bin") else Image.open(P(rel)))
                for rel in FILES[piece]} if d == "today" else DRAW[piece](d)

    # ---- the evolution: the moving bg at three phase stages, the sparkles, over the filmed daemon and box
    dark = _fr(fdir, 1, "s01_61_b_08.png")            # the daemon white on black, sparkles round it, the box
    box = _fr(fdir, 1, "s01_61_b_30.png")
    rows = [[], [], [], []]
    old_sp = _sprite_rgba(Image.open(P("graphics/evolution_scene/sparkle.png")))
    for d in DS:
        ff = files("evo_bg", d)
        f = ff["graphics/evolution_scene/bg.png"]
        mp = {b: ff["graphics/evolution_scene/" + b] for b in ("bg.bin", "bg2.bin")}
        sp = files("sparkle", d)["graphics/evolution_scene/sparkle.png"]
        field = Image.new("RGB", (64, 224)); fp = field.load(); src = f.load()
        for y in range(224):
            for x in range(64):
                v = src[x, y]
                fp[x, y] = (0, 0, 0) if v in (0, 14, 15) else (int(255 * v / 13), int(255 * v / 13), 255)
        rows[0].append(Image.new("RGB", (480, 320), (22, 22, 28)))
        rows[0][-1].paste(X(field, 1), (0, 0))
        rows[0][-1].paste(X(_sprite_rgba(sp).convert("RGB"), 8), (80, 0))
        for k, (stage, o1, o2) in enumerate(((12, (12, 16), (4, 16)), (24, (8, 20), (8, 12)))):
            bg = evo_render(f, stage, o1, o2, mp)
            comp = bg.copy(); cp = comp.load(); dp = dark.load()
            for y in range(160):
                for x in range(240):
                    if y >= 112 or sum(dp[x, y]) > 60:
                        cp[x, y] = dp[x, y] if y < 112 else box.load()[x, y]
            if d != "today":
                comp = _sparkles_swap(comp, dark, old_sp, _sprite_rgba(sp))
            rows[k + 1].append(X2(comp))
        rows[3].append(X2(evo_render(f, 13, (8, 16), (8, 16), mp)))
    made.append(_sheet(os.path.join(out_dir, "t566_evolution.png"),
                       "T-566 DRAFT -- the EVOLUTION: evolution_scene/bg.png (224 tiles) and sparkle.png",
                       "today (pret's) beside A/B/C, 2x; the two layers and their phase palette rendered as the hardware "
                       "does, over the filmed daemon, sparkles and box. Recommended: bg %s %s, sparkle %s %s"
                       % (RECOMMENDED["evo_bg"], NAMES["evo_bg"][RECOMMENDED["evo_bg"]], RECOMMENDED["sparkle"],
                          NAMES["sparkle"][RECOMMENDED["sparkle"]]),
                       _label([(d, NAMES["evo_bg"].get(d, "") + " / " + NAMES["sparkle"].get(d, "")) for d in DS]),
                       rows, ["the tiles as phase (1 dark .. 13 light), and the sparkle at 8x",
                              "rising (phase stage 12), the layers circling apart",
                              "the pulse (stage 24), at another point of the circle",
                              "the background alone, layers aligned (stage 13)"]))

    # ---- the item scene: bg (warm and cool), star, level-up, dots
    candy = _fr(fdir, 1, "s01_05_b_03.png"); stone = _fr(fdir, 2, "s02_05_b_10.png")
    bin_ = P("graphics/pokemon_special_anim/bg.bin")
    t_png = Image.open(P("graphics/pokemon_special_anim/bg.png"))
    t_item = _bg_layer(t_png, bin_, _jasc(P("graphics/pokemon_special_anim/bg.pal")))
    rows = [[], [], [], []]
    for d in DS:
        f = files("psa_bg", d)
        png = f["graphics/pokemon_special_anim/bg.png"]
        pi = _jasc(P("graphics/pokemon_special_anim/bg.pal")) if d == "today" else \
            [tuple(int(v) for v in f["graphics/pokemon_special_anim/bg.pal"].split()[3 + i * 3:6 + i * 3]) for i in range(16)]
        pt = _jasc(P("graphics/pokemon_special_anim/bg_tm_hm.pal")) if d == "today" else \
            [tuple(int(v) for v in f["graphics/pokemon_special_anim/bg_tm_hm.pal"].split()[3 + i * 3:6 + i * 3]) for i in range(16)]
        lay_i = _bg_layer(png, bin_, pi); lay_t = _bg_layer(png, bin_, pt)
        st = _sprite_rgba(files("star", d)["graphics/pokemon_special_anim/star.png"])
        lu = _sprite_rgba(files("level_up", d)["graphics/pokemon_special_anim/level_up.png"])
        dt = _sprite_rgba(files("dots", d)["graphics/pokemon_special_anim/outward_spiral_dots.png"])
        assets = Image.new("RGB", (480, 320), (22, 22, 28))
        assets.paste(X(png.convert("RGB"), 1), (0, 0))
        for k, im in enumerate((st, lu, dt)):
            tile = Image.new("RGB", im.size, _gba(pi[1])); tile.paste(im, (0, 0), im)
            assets.paste(X(tile, 6), (40 + k * 110, 0))
        rows[0].append(assets)
        a = _swap(candy, t_item, lay_i)
        for k, (x, y) in enumerate(((56, 70), (64, 54), (72, 70))):      # the streaks rising, placed offline
            if d != "today":
                a.paste(lu, (x + 30 * k, y), lu)
        rows[1].append(X2(a))
        b = _swap(stone, t_item, lay_i)
        if d != "today":
            for k, (ox, oy) in enumerate(((-8, -8), (6, -13), (8, -8))):
                b.paste(st, (120 + ox * 4 - 8 + k * 6, 40 + oy * 2), st)
        rows[2].append(X2(b))
        c = _swap(candy, t_item, lay_t)
        if d != "today":
            for k, (x, y) in enumerate(((150, 30), (176, 54), (186, 86), (60, 96))):
                tile = dt.crop((0, (k % 3) * 8, 8, (k % 3) * 8 + 8)); c.paste(tile, (x, y), tile)
        rows[3].append(X2(c))
    made.append(_sheet(os.path.join(out_dir, "t566_item_scene.png"),
                       "T-566 DRAFT -- an ITEM used from the bag: pokemon_special_anim bg, level_up, star, dots",
                       "today beside A/B/C, 2x; bg swapped into the filmed frames (CONTENT debug); the drafts' sprites "
                       "placed offline where the scene throws them. Recommended: bg %s, level_up %s, star %s, dots %s"
                       % tuple("%s %s" % (RECOMMENDED[p], NAMES[p][RECOMMENDED[p]]) for p in ("psa_bg", "level_up", "star", "dots")),
                       _label([(d, "bg %s / lv %s / star %s / dots %s" % tuple(NAMES[p].get(d, "") for p in
                               ("psa_bg", "level_up", "star", "dots"))) for d in DS]),
                       rows, ["bg tiles 1x; star, level-up, dots at 6x on the paper",
                              "a candy used (filmed), the level's streaks", "a stone used (filmed), its stars",
                              "a TM's cool palette, the dots spiralling out"]))

    # ---- the relearner and its arrows
    rl = _fr(fdir, 3, sorted(f for f in os.listdir(os.path.join(fdir, "03")) if "_b_00" in f)[0])
    lmb = P("graphics/interface/learn_move.bin")
    t_lm = _bg_layer(Image.open(P("graphics/interface/learn_move.png")), lmb,
                     _pal(Image.open(P("graphics/interface/learn_move.png"))), pals={0})
    rows = [[], []]
    for d in DS:
        png = files("relearner", d)["graphics/interface/learn_move.png"]
        lay = _bg_layer(png, lmb, _pal(png), pals={0})
        a = _swap(rl, t_lm, lay, tol=6)
        ar = files("arrows", d)["graphics/learn_move/interface_sprites.png"]
        apal = _pal(ar)
        down = _sprite_rgba(ar.crop((0, 32, 8, 48)), apal); up = _sprite_rgba(ar.crop((0, 48, 8, 64)), apal)

        def wide(t):        # a 16x8 sprite from two stacked 8x8 tiles
            out = Image.new("RGBA", (16, 8)); out.paste(t.crop((0, 0, 8, 8)), (0, 0)); out.paste(t.crop((0, 8, 8, 16)), (8, 0))
            return out
        b = a.copy(); b.paste(wide(up), (200 - 8, 4 - 4), wide(up)); b.paste(wide(down), (200 - 8, 108 - 4), wide(down))
        rows[0].append(X2(a)); rows[1].append(X2(b))
    made.append(_sheet(os.path.join(out_dir, "t566_relearner.png"),
                       "T-566 DRAFT -- TWO ISLAND's relearner: interface/learn_move.png and its scroll arrows",
                       "today beside A/B/C, 2x; the panel swapped into the filmed screen (CONTENT debug). Recommended: "
                       "panel %s %s, arrows %s %s" % (RECOMMENDED["relearner"], NAMES["relearner"][RECOMMENDED["relearner"]],
                                                       RECOMMENDED["arrows"], NAMES["arrows"][RECOMMENDED["arrows"]]),
                       _label([(d, NAMES["relearner"].get(d, "") + " / " + NAMES["arrows"].get(d, "")) for d in DS]),
                       rows, ["the relearner as filmed, the panel swapped", "scroll arrows placed offline (no list here is long enough)"]))

    # ---- the egg
    party = _fr(fdir, 4, "s04_00.png"); summ = _fr(fdir, 4, "s04_02.png")
    hatch_frames = [_fr(fdir, 4, n) for n in ("s04_93.png", "s04_94_b_00.png", "s04_94_b_10.png")]
    today = files("egg", "today")
    o_front = _sprite_rgba(today["graphics/pokemon/egg/front.png"])
    icon_pal = _jasc(P("graphics/pokemon/icon_palettes/icon_palette_1.pal"))
    o_icon = [_sprite_rgba(today["graphics/pokemon/egg/icon.png"].crop((0, k * 32, 32, k * 32 + 32)), icon_pal) for k in (0, 1)]
    o_hatch = [_sprite_rgba(today["graphics/misc/egg_hatch.png"].crop((0, k * 32, 32, k * 32 + 32)),
                            _jasc(P("graphics/pokemon/egg/normal.pal"))) for k in range(4)]
    at_front = _find(summ, o_front, tol=40, accept=0.35)   # the SUMMARY tints its picture a little
    if not at_front:        # placed by the egg's coloured pixels in the picture panel: pret's egg spans (20..44)
        spx = summ.load()
        pts = [(x, y) for y in range(16, 90) for x in range(8, 116) if abs(spx[x, y][1] - spx[x, y][2]) > 25]
        if pts:
            at_front = (min(p[0] for p in pts) - 21, min(p[1] for p in pts) - 21)
    at_icon = [(_find(party, s), s) for s in o_icon]
    at_icon = next(((a, s) for a, s in at_icon if a), (None, None))
    rows = [[], [], [], []]
    for d in DS:
        f = files("egg", d)
        npal = _jasc(P("graphics/pokemon/egg/normal.pal")) if d == "today" else \
            [tuple(int(v) for v in f["graphics/pokemon/egg/normal.pal"].split()[3 + i * 3:6 + i * 3]) for i in range(16)]
        fr = _sprite_rgba(f["graphics/pokemon/egg/front.png"], npal)
        hs = [_sprite_rgba(f["graphics/misc/egg_hatch.png"].crop((0, k * 32, 32, k * 32 + 32)), npal) for k in range(4)]
        sh = _sprite_rgba(f["graphics/misc/egg_shard.png"], npal)
        ic = [_sprite_rgba(f["graphics/pokemon/egg/icon.png"].crop((0, k * 32, 32, k * 32 + 32)), icon_pal) for k in (0, 1)]
        assets = Image.new("RGB", (480, 320), (60, 64, 72))
        assets.paste(X(fr, 2), (0, 0), X(fr, 2))
        for k in range(4):
            assets.paste(X(hs[k], 2), (140 + (k % 2) * 70, (k // 2) * 70), X(hs[k], 2))
        assets.paste(X(sh, 4), (0, 150), X(sh, 4))
        for k in (0, 1):
            assets.paste(X(ic[k], 3), (300 + k * 90, 150), X(ic[k], 3))
        rows[0].append(assets)
        s = summ if d == "today" or not at_front else _replace(summ, o_front, fr, at_front)
        p = party if d == "today" or not at_icon[0] else _replace(party, at_icon[1], ic[0], at_icon[0])
        rows[1].append(X2(s)); rows[2].append(X2(p))
        hf = hatch_frames[1]
        at_h = None
        for k in range(4):
            at_h = _find(hf, o_hatch[k])
            if at_h:
                kk = k; break
        if d != "today" and at_h:
            hf = _replace(hf, o_hatch[kk], hs[max(kk, 1)], at_h)
            for j, (sx, sy) in enumerate(((at_h[0] - 14, at_h[1] - 12), (at_h[0] + 34, at_h[1] - 10))):
                piece = sh.crop((j * 8, 0, j * 8 + 8, 8)); hf.paste(piece, (sx, sy), piece)
        rows[3].append(X2(hf))
    made.append(_sheet(os.path.join(out_dir, "t566_egg.png"),
                       "T-566 DRAFT -- the EGG: pokemon/egg front, icon, normal.pal; misc/egg_hatch, egg_shard",
                       "today beside A/B/C, 2x; each draft put where pret's was found in the filmed frames (CONTENT debug). "
                       "Recommended: %s %s" % (RECOMMENDED["egg"], NAMES["egg"][RECOMMENDED["egg"]]),
                       _label([(d, NAMES["egg"].get(d, "")) for d in DS]),
                       rows, ["front 2x; the hatch's four frames 2x; the shards 4x; the icon's two frames 3x",
                              "the SUMMARY (filmed)",
                              "the party (filmed)" + ("" if at_icon[0] else " -- icon not found in the frame"),
                              "the hatch, cracking, with two shards (filmed; the shards placed)"]))

    # ---- today's scenes as filmed
    strip = [(1, "s01_05_b_03.png", "a candy used: pret's bg"), (1, "s01_61_b_08.png", "evolving: pret's sparkles"),
             (1, "s01_61_b_22.png", "evolving: pret's moving bg"), (2, "s02_05_b_10.png", "a stone: pret's bg"),
             (3, os.path.basename(sorted(f for f in os.listdir(os.path.join(fdir, "03")) if "_b_00" in f)[0]),
              "the relearner: pret's panel"), (4, "s04_00.png", "the party: pret's egg icon"),
             (4, "s04_02.png", "the SUMMARY: pret's egg"), (4, "s04_94_b_00.png", "the hatch: pret's egg, cracking"),
             (4, "s04_94_b_10.png", "the hatch: its shards")]
    font, big = _font()
    ov = Image.new("RGB", (10 + 3 * 490, 70 + 3 * 350), (22, 22, 28)); od = ImageDraw.Draw(ov)
    od.text((10, 8), "T-566 -- today's scenes, filmed (CONTENT debug ROM, tools/routes/film_t566_evolve.json), 2x",
            fill=(240, 240, 240), font=big)
    od.text((10, 38), "every one still draws pret's art", fill=(200, 200, 210), font=font)
    for i, (stop, name, cap) in enumerate(strip):
        x, y = 10 + (i % 3) * 490, 70 + (i // 3) * 350
        od.text((x, y), cap, fill=(235, 220, 140), font=font)
        ov.paste(X2(_fr(fdir, stop, name)), (x, y + 22))
    path = os.path.join(out_dir, "t566_today.png"); ov.save(path); made.append(path)
    print("  sheet %s" % path)
    return made


def _sparkles_swap(comp, dark, old_sp, new_sp):
    """Every small white blob of the filmed frame (a sparkle, not the daemon) redrawn as the draft's sparkle."""
    dp = dark.load(); seen = set(); out = comp.copy()
    for y in range(112):
        for x in range(240):
            if (x, y) in seen or sum(dp[x, y]) <= 300:
                continue
            stack, blob = [(x, y)], []
            seen.add((x, y))
            while stack:
                a, b = stack.pop(); blob.append((a, b))
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (a + da, b + db)
                    if 0 <= q[0] < 240 and 0 <= q[1] < 112 and q not in seen and sum(dp[q]) > 300:
                        seen.add(q); stack.append(q)
            if len(blob) > 100:
                continue
            xs = [p[0] for p in blob]; ys = [p[1] for p in blob]
            cx, cy = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2
            op = out.load()
            for (a, b) in blob:
                op[a, b] = comp.load()[max(0, min(xs) - 1), b] if min(xs) > 0 else (0, 0, 0)
            out.paste(new_sp, (cx - 4, cy - 4), new_sp)
    return out


def main():
    a = sys.argv
    if "--write" in a:
        if "--approved" not in a:
            sys.exit("gbaevolve: --write needs --approved (it writes APPROVED, the user's picks)")
        if not APPROVED:
            print("gbaevolve: nothing approved yet (T-566 is a DRAFT); nothing written")
            return 0
        for piece, d in APPROVED.items():
            save(DRAW[piece](d), GBA)
            print("  wrote %s %s (%s)" % (piece, d, NAMES[piece][d]))
        return 0
    if "--draft" in a:
        i = a.index("--draft")
        draft(a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else DRAFT)
    if "--sheets" in a:
        sheets(a[a.index("--sheets") + 1], a[a.index("--frames") + 1] if "--frames" in a else FRAMES)
    if "--draft" not in a and "--sheets" not in a:
        return report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
