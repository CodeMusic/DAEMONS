#!/usr/bin/env python3
"""T-568: THE NEW GAME AND THE NAME -- the Nintendo art they still draw (batch 7 of the 2026-11-14 re-census). DRAFT.

    python3 tools/gbanewgame.py                       # report: the census, each piece's contract, APPROVED (exit 1 on drift)
    python3 tools/gbanewgame.py --draft [DIR]         # every piece's A/B/C into DIR (gfx/drafts/t568_newgame/)
    python3 tools/gbanewgame.py --sheets DIR [--frames DIR]   # today beside A/B/C at 2x, in context
    python3 tools/gbanewgame.py --write --approved    # write APPROVED's picks into engineGba (none yet: nothing is written)

A new tool beside gbanaming.py, not a mode of it: gbanaming (T-363) is the naming screen's palettes, background and
banner, and its plain --write is what check_generators runs; this batch is pixels across two scenes, written only
with --approved, as gbaevolve (T-566) is. port_oak.py is CRYSTAL's words, not her scene's art, so it stays words.

THE CENSUS (2026-11-15, engine cb00af971 against pret upstream/master, by pixels; filmed on the CONTENT debug ROM by
tools/routes/film_t568_newgame.json, a NEW GAME from reset on the theatre's scratch save, never saved):

  ALREADY OURS -- not drawn again here:
    the naming screen's background, keyboard panel, name box and banner (menu.png, background.bin, the seven .pal
    files: T-363 "the terminal"); the rival's icon (rival.png); the player's icon (their overworld sprite) and a
    daemon's (its icon); CRYSTAL, the player and the rival in the scene (oak/, red/, leaf/, rival/ pic.png); the
    intro's SEEKMUSAI (pikachu_intro/body, ears, eyes); the daemon CRYSTAL lets out (SPEAROW's slot: a daemon).
    The naming sprites below ALSO wear our colours already (T-363 recoloured buttons.pal, cursor.pal and the page
    palettes) -- only their pixels, the SHAPES, are still pret's.

  STILL PRET'S AND ON SCREEN -- drafted:
    guide     graphics/oak_speech/bg_tiles.png, palette row 3 and its tiles 16-93: the CONTROLS guide's GBA buttons
              (the pad, A, B, START, SELECT and their dots, L and R), placed by controls_guide_page_2/3.bin. Every
              NEW GAME.
    window    bg_tiles.png, palette row 2 and tiles 3-12, 94, 96-150: the panel SEEKMUSAI stands on (its frame,
              its dashed rules) and the Poke Ball watermark in its lower right, placed by pikachu_intro/tilemap.bin.
              The census's "shares its tiles with the Pikachu intro's (already ours)" is this: SEEKMUSAI is ours,
              the panel and the ball it sits on are not.
    oak_bg    graphics/oak_speech/oak_speech_bg.png (10 tiles, 2-8 placed by oak_speech_bg.bin, one per screen
              band) and bg_tiles.png's palette row 0, colours 1-8 (oak_speech.c loads bg_tiles.gbapal over row 0 for
              CRYSTAL's scene too): the mint sky and the teal floor behind CRYSTAL, the player and the rival.
    platform  graphics/oak_speech/platform.png + platform.pal: the pale ellipse under CRYSTAL, the player and the
              rival (three 32x32 sprites at x 72-168, y 96-128).
    buttons   graphics/naming_screen/back_button.png, ok_button.png: BACK / B BUTTON and OK / START, every naming.
    page_swap graphics/naming_screen/page_swap_frame.png, page_swap_button.png, page_swap_upper/lower/others.png:
              the page key, its pill (one tint a page) and its three labels (UPPER, lower, others).
    cursor    graphics/naming_screen/cursor.png, cursor_squished.png, cursor_filled.png: the key cursor and its
              press (squished, then filled, 8 frames each).
    marks     graphics/naming_screen/input_arrow.png, underscore.png: the arrow at the name and its underscores.
    pc_icon   graphics/naming_screen/pc_icon_off.png, pc_icon_on.png: the icon a BOX's naming shows (the PC's
              box menu, NAME) -- drawn offline into the naming frame; the route does not walk to a PC.

  DEAD (shown nowhere): bg_tiles tiles 13, 78, 79, 95, 128, 129, 144, 145 (drawn, but no map places them: left as
  pret's); page labels' tiles
  3-4 (each label's sheet is 0x60 bytes: only its first 24 pixels load); oak_speech_bg.png tiles 0, 1 and 9.

  NOT DRAWABLE HERE: the CONTROLS guide's blue field is not bg_tiles: it is the backdrop, colour 0 of BG row 0, which
  oak_speech.c sets from GetTextWindowPalette(2)[15] -- graphics/text_window/stdpal_2.pal, pret's, and loaded by the
  item PC, the SEAGALLOP, the slot machine and menu.c too. It stays blue until batch 1 (the menu leftovers) draws
  stdpal_2; every guide draft is drawn to sit on that blue. The guide's top-bar tiles 2, 14 and 15 are drawn with
  BG row 13 (the std menu palette), not row 3: a plain bar and two rules, left as they are.

THE RULES each draft keeps: every PNG its pret size, indexed, the same palette length (bg_tiles 64 colours, the rest
16); bg_tiles' pixels outside the piece's own tiles and its palette outside the piece's own row untouched, and every
tile keeps its row; every tilemap kept byte for byte (each tile drawn where the maps already place it, flips
included -- the panel's rules are placed flipped, so its interior patterns are symmetric top to bottom); sprite frame
layouts kept, and each draft inside pret's footprint. The naming sprites keep T-363's palettes and draw to their
indices in their roles: 14 is the BACK/OK/page outline the button flash lights, cursor colour 1 the one the cursor
flash tints. Every word drawn stays the word it was (BACK, OK, B BUTTON, START, SELECT, UPPER, lower, others, A, B,
L, R), the keys' words lettered in the game's own small font (graphics/fonts/latin_small.png, ours); the captions under
them and the page labels in a 3x5 micro font kept here, as pret's were tiny ("others" is 29px in the small font, and
a label loads only 24). No edition split anywhere in
this batch: one palette for CONTENT and CONTEXT, so the sheets show the one.
"""
import os, struct, sys
from PIL import Image

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
GBA = os.path.join(ROOT, "engineGba")
DRAFT = os.path.join(ROOT, "gfx", "drafts", "t568_newgame")
FRAMES = os.path.join(ROOT, ".theatre", "routes", "film_t568_newgame")      # tools/routes/film_t568_newgame.json
sys.path.insert(0, TOOLS)

PIECES = ["guide", "window", "oak_bg", "platform", "buttons", "page_swap", "cursor", "marks", "pc_icon"]
APPROVED = {}   # DRAFT: nothing picked yet
OS, NS = "graphics/oak_speech/", "graphics/naming_screen/"
FILES = {
    "guide":     [OS + "bg_tiles.png"],
    "window":    [OS + "bg_tiles.png"],
    "oak_bg":    [OS + "oak_speech_bg.png", OS + "bg_tiles.png"],
    "platform":  [OS + "platform.png", OS + "platform.pal"],
    "buttons":   [NS + "back_button.png", NS + "ok_button.png"],
    "page_swap": [NS + "page_swap_frame.png", NS + "page_swap_button.png", NS + "page_swap_upper.png",
                  NS + "page_swap_lower.png", NS + "page_swap_others.png"],
    "cursor":    [NS + "cursor.png", NS + "cursor_squished.png", NS + "cursor_filled.png"],
    "marks":     [NS + "input_arrow.png", NS + "underscore.png"],
    "pc_icon":   [NS + "pc_icon_off.png", NS + "pc_icon_on.png"],
}
NAMES = {
    "guide":     {"A": "KEYCAPS", "B": "WIREFRAME", "C": "GRAPH CARDS"},
    "window":    {"A": "GRAPH PAPER", "B": "RULED", "C": "SCANLINES"},
    "oak_bg":    {"A": "GRAPH PAPER", "B": "THE STAVE", "C": "NIGHT GRID"},
    "platform":  {"A": "THE PAD", "B": "THE RING", "C": "THE STAVE"},
    "buttons":   {"A": "KEYCAP", "B": "INVERSE", "C": "UNDERLINE"},
    "page_swap": {"A": "KEYCAP", "B": "INVERSE", "C": "UNDERLINE"},
    "cursor":    {"A": "BRACKETS", "B": "BLOCK", "C": "CARET BAR"},
    "marks":     {"A": "PROMPT", "B": "STEPPED", "C": "CHEVRONS"},
    "pc_icon":   {"A": "THE TERMINAL", "B": "THE DRIVE", "C": "THE TOWER"},
}
LINES = {
    "guide":     {"A": "every button a square navy keycap with a teal bevel and its letter in paper: a keyboard's keys",
                  "B": "every button a 1-pixel paper outline with its letter, nothing filled: a wireframe of the pad",
                  "C": "every button a little graph-paper card with a navy edge and its letter in navy"},
    "window":    {"A": "the panel graph paper (a faint 8-pixel grid), square corners, and the CodeMusic ring where "
                        "the Poke Ball was",
                  "B": "plain paper, the dashed rules made solid teal, and a quaver where the ball was",
                  "C": "paper with a faint band every 8 pixels, and a big 0 1 in the corner where the ball was"},
    "oak_bg":    {"A": "mint graph paper that steps down into a teal floor, the grid running through it",
                  "B": "plain paper sky, a five-line stave across the horizon, a teal floor: CRYSTAL stands on the music",
                  "C": "the title's night navy with faint scanlines, a teal glow at the horizon, a grid floor"},
    "platform":  {"A": "a mint pad ruled as graph paper, foreshortened, with a teal rim",
                  "B": "only the rim: a teal ring with tick marks, the floor showing through",
                  "C": "a mint pad with five staff lines across it"},
    "buttons":   {"A": "a square keycap: cyan face, pale bevel, the word in pale; the caption plate below",
                  "B": "a flat inverse-video block: light cyan, the word in navy",
                  "C": "the word in cyan on the dark plate, a cyan bar under it"},
    "page_swap": {"A": "the page key framed as BACK and OK's keycap A, the pill square, the label pale on its tint",
                  "B": "as B: the label dark on its tint", "C": "as C: the label pale on the dark pill, a tint bar under it"},
    "cursor":    {"A": "four square corner brackets round the key; the press pulls them in and fills",
                  "B": "a square 2-pixel box; the press squashes and fills it",
                  "C": "a bar under the key; the press lifts it and fills the key"},
    "marks":     {"A": "a > prompt and a thick underline cursor", "B": "a stepped triangle and a short bar",
                  "C": "a >> and a bracketed underline"},
    "pc_icon":   {"A": "a little monitor whose caret blinks", "B": "a disk drive whose lamp blinks",
                  "C": "a tower whose two lights blink"},
}
RECOMMENDED = {"guide": "A", "window": "A", "oak_bg": "A", "platform": "A", "buttons": "A", "page_swap": "A",
               "cursor": "A", "marks": "A", "pc_icon": "A"}

# the house colours (gbamenus.py's TERMINAL family, gbaevolve's)
SLATE_OUT, SLATE_MID, SLATE_LIGHT = (32, 40, 52), (88, 104, 120), (176, 192, 204)
TEAL, TEAL_DK, PAPER = (112, 208, 184), (40, 136, 116), (248, 248, 244)
NAVY = (24, 41, 74)


def P(path):
    return os.path.join(GBA, path)


# ================================================================================================= small helpers
def _grid(w, h, v=0):
    return [[v] * w for _ in range(h)]


def _rect(g, x0, y0, x1, y1, v):
    """Fill x0..x1, y0..y1 inclusive."""
    for y in range(max(0, y0), min(len(g), y1 + 1)):
        for x in range(max(0, x0), min(len(g[0]), x1 + 1)):
            g[y][x] = v


def _box(g, x0, y0, x1, y1, v, t=1):
    _rect(g, x0, y0, x1, y0 + t - 1, v); _rect(g, x0, y1 - t + 1, x1, y1, v)
    _rect(g, x0, y0, x0 + t - 1, y1, v); _rect(g, x1 - t + 1, y0, x1, y1, v)


def _stamp(g, rows, x0, y0, v, shadow=None):
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != "." and c != " ":
                if shadow is not None and 0 <= y0 + y + 1 < len(g) and 0 <= x0 + x + 1 < len(g[0]):
                    if g[y0 + y + 1][x0 + x + 1] != v:
                        g[y0 + y + 1][x0 + x + 1] = shadow
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != "." and c != " " and 0 <= y0 + y < len(g) and 0 <= x0 + x < len(g[0]):
                g[y0 + y][x0 + x] = v


_FONT = None


def _glyphs(s):
    """The word in the game's own small font (latin_small, ours): a list of rows of '#'/'.', cropped to its ink."""
    global _FONT
    import fontwidth
    if _FONT is None:
        _FONT = (Image.open(P("graphics/fonts/latin_small.png")), fontwidth.glyph_widths("sFontSmallLatinGlyphWidths"),
                 fontwidth.charmap(GBA))
    sheet, w, cm = _FONT
    fp = sheet.load()
    cols, x = {}, 0
    for ch in s:
        b = cm.get(ch)
        if b is None:
            continue
        gx, gy = (b % 32) * 8, (b // 32) * 16
        for yy in range(16):
            for xx in range(min(8, w[b])):
                if fp[gx + xx, gy + yy] == 1:
                    cols[(x + xx, yy)] = 1
        x += w[b]
    if not cols:
        return []
    xs = [p[0] for p in cols]; ys = [p[1] for p in cols]
    return ["".join("#" if (xx, yy) in cols else "." for xx in range(min(xs), max(xs) + 1))
            for yy in range(min(ys), max(ys) + 1)]


MICRO = {   # 3x5 (N 4 wide, l 1, w 5): the captions and the page labels, as pret's were tiny -- the small font is 29px
    "B": ["##.", "#.#", "##.", "#.#", "##."], "U": ["#.#", "#.#", "#.#", "#.#", "###"],
    "T": ["###", ".#.", ".#.", ".#.", ".#."], "O": ["###", "#.#", "#.#", "#.#", "###"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"], "S": [".##", "#..", ".#.", "..#", "##."],
    "A": [".#.", "#.#", "###", "#.#", "#.#"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "E": ["###", "#..", "##.", "#..", "###"], "L": ["#..", "#..", "#..", "#..", "###"],
    "C": [".##", "#..", "#..", "#..", ".##"], "P": ["##.", "#.#", "##.", "#..", "#.."],
    "l": ["#", "#", "#", "#", "#"], "o": ["...", ".#.", "#.#", "#.#", ".#."],
    "w": [".....", "#...#", "#.#.#", "#.#.#", ".#.#."], "e": ["...", ".#.", "###", "#..", ".##"],
    "r": ["...", "#.#", "##.", "#..", "#.."], "t": [".#.", "###", ".#.", ".#.", "..#"],
    "h": ["#..", "#..", "##.", "#.#", "#.#"], "s": ["...", ".##", "#..", "..#", "##."], " ": ["..", "..", "..", "..", ".."],
}


def _micro(s):
    rows = [""] * 5
    for i, ch in enumerate(s):
        gl = MICRO[ch]
        for y in range(5):
            rows[y] += gl[y] + ("." if i < len(s) - 1 else "")
    return rows


def _scale(rows, k):
    return ["".join(c * k for c in r) for r in rows for _ in range(k)]


def _text(g, s, cx, y0, v, shadow=None, k=1, left=None):
    rows = _scale(_glyphs(s), k)
    if not rows:
        return 0
    w = len(rows[0])
    x0 = left if left is not None else cx - w // 2
    _stamp(g, rows, x0, y0, v, shadow)
    return w


TRI = ["#..", "##.", "###", "##.", "#.."]     # the ▶ after START and SELECT


def _img(g, pal):
    h, w = len(g), len(g[0])
    im = Image.new("P", (w, h), 0)
    flat = [c for col in pal for c in col]
    im.putpalette(flat)
    im.putdata([v for row in g for v in row])
    return im


def _pal_of(im):
    p = im.getpalette()
    return [tuple(p[i * 3:i * 3 + 3]) for i in range(len(p) // 3)]


def _like(old, g, pal=None):
    """An image the size, mode and palette length of OLD, its pixels from G (indices), its palette PAL or OLD's."""
    pal = pal or _pal_of(old)
    return _img(g, pal)


def _px(im):
    w, h = im.size
    d = list(im.getdata())
    return [d[y * w:(y + 1) * w] for y in range(h)]


def _jasc(path):
    v = open(path).read().split()
    return [tuple(int(x) for x in v[3 + i * 3:6 + i * 3]) for i in range(int(v[2]))]


def _jasc_text(pal):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in pal[:16])


def _map(rel):
    d = open(P(rel), "rb").read()
    return struct.unpack("<%dH" % (len(d) // 2), d)


def _base():
    """The engine's files as they are: the base every piece draws over (and --write --approved composes on)."""
    out = {}
    for rels in FILES.values():
        for rel in rels:
            if rel not in out:
                out[rel] = open(P(rel)).read() if rel.endswith(".pal") else Image.open(P(rel))
    return out


# ================================================================================================= bg_tiles: tile fitting
def _tile_get(px, t):
    n = len(px[0]) // 8
    tx, ty = (t % n) * 8, (t // n) * 8
    return [[px[ty + y][tx + x] for x in range(8)] for y in range(8)]


def _tile_put(px, t, tile):
    tx, ty = (t % 16) * 8, (t // 16) * 8
    for y in range(8):
        for x in range(8):
            px[ty + y][tx + x] = tile[y][x]


def _fit(px, target, entries, cols, row, x_cells=0, y_cells=0, allow=None):
    """Write TARGET (a pixel grid of local indices 0-15) into bg_tiles' tiles where the map ENTRIES (COLS wide) place
    them, at palette ROW. A tile placed twice must come out the same both times (flips undone); a blank cell (tile 0)
    must stay blank. Returns the problems."""
    seen, errs = {}, []
    for i, e in enumerate(entries):
        r, c = divmod(i, cols)
        t, hf, vf = e & 0x3FF, e & 0x400, e & 0x800
        cell = [[target[(r + y_cells) * 8 + y][(c + x_cells) * 8 + x] if (r + y_cells) * 8 + y < len(target)
                 and (c + x_cells) * 8 + x < len(target[0]) else 0 for x in range(8)] for y in range(8)]
        if vf:
            cell = cell[::-1]
        if hf:
            cell = [row_[::-1] for row_ in cell]
        if t == 0:
            if any(v for rr in cell for v in rr):
                errs.append("drawn in a blank cell (%d, %d)" % (c, r))
            continue
        if allow is not None and t not in allow:
            continue
        if t in seen and seen[t] != cell:
            errs.append("tile %d placed twice, drawn two ways" % t)
            continue
        seen[t] = cell
    for t, cell in seen.items():
        _tile_put(px, t, [[(row * 16 + v) if v else 0 for v in rr] for rr in cell])
    return errs


def _bgt(base):
    im = base[OS + "bg_tiles.png"]
    return _px(im), _pal_of(im)


def _bgt_image(px, pal):
    im = Image.new("P", (128, 80), 0)
    im.putpalette([c for col in pal[:64] for c in col])
    im.putdata([v for row in px for v in row])
    return im


# ================================================================================================= guide (row 3)
GUIDE_TILES = set(range(16, 78)) | set(range(80, 94))
GUIDE_PAL = {
    "A": [(0, 74, 139), NAVY, SLATE_OUT, TEAL, TEAL_DK, PAPER, (44, 66, 108), SLATE_LIGHT],
    "B": [(0, 74, 139), PAPER, (16, 64, 112), (200, 232, 240), TEAL, PAPER, (160, 200, 220), SLATE_LIGHT],
    "C": [(0, 74, 139), NAVY, NAVY, (216, 234, 230), TEAL_DK, PAPER, (232, 242, 238), (200, 224, 218)],
}
#  roles: 1 face / ink, 2 outline, 3 bevel light, 4 bevel dark, 5 glyph, 6 face 2, 7 grid


def _key(g, x0, y0, x1, y1, d, glyph=None, k=1, gy=None):
    if d == "A":
        _rect(g, x0, y0, x1, y1, 2)
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 1)
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y0 + 1, 3); _rect(g, x0 + 1, y0 + 1, x0 + 1, y1 - 1, 3)
        _rect(g, x0 + 2, y1 - 1, x1 - 1, y1 - 1, 4); _rect(g, x1 - 1, y0 + 2, x1 - 1, y1 - 1, 4)
        ink, sh = 5, 2
    elif d == "B":
        _box(g, x0, y0, x1, y1, 5)
        _rect(g, x0 + 1, y1 + 1, x1 + 1, y1 + 1, 2); _rect(g, x1 + 1, y0 + 1, x1 + 1, y1 + 1, 2)
        ink, sh = 5, 2
    else:
        _rect(g, x0, y0, x1, y1, 2)
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 6)
        for y in range(y0 + 1, y1):
            for x in range(x0 + 1, x1):
                if (x - x0) % 3 == 0 or (y - y0) % 3 == 0:
                    g[y][x] = 7
        ink, sh = 1, None
    if glyph:
        rows = _scale(_glyphs(glyph), k)
        w, h = len(rows[0]), len(rows)
        cx, cy = (x0 + x1 + 1) // 2, (y0 + y1 + 1) // 2 if gy is None else gy
        if d == "C":
            _rect(g, cx - w // 2 - 1, cy - h // 2 - 1, cx - w // 2 + w, cy - h // 2 + h, 6)
        _stamp(g, rows, cx - w // 2, cy - h // 2, ink, sh)


def _pad(g, d):
    """The + pad in the page-2 block, 40x32 with its corners blank."""
    arms = [(14, 1, 25, 30), (3, 10, 36, 21)]
    if d == "A":
        for x0, y0, x1, y1 in arms:
            _rect(g, x0, y0, x1, y1, 2)
        for x0, y0, x1, y1 in arms:
            _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 1)
        _rect(g, 15, 2, 24, 2, 3); _rect(g, 4, 11, 13, 11, 3); _rect(g, 4, 11, 4, 20, 3); _rect(g, 15, 2, 15, 10, 3)
        _rect(g, 26, 20, 35, 20, 4); _rect(g, 15, 29, 24, 29, 4); _rect(g, 35, 11, 35, 20, 4); _rect(g, 24, 21, 24, 29, 4)
        car = 5
    elif d == "B":
        pts = [(14, 1), (25, 1), (25, 10), (36, 10), (36, 21), (25, 21), (25, 30), (14, 30), (14, 21), (3, 21),
               (3, 10), (14, 10)]
        for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
            _rect(g, min(ax, bx), min(ay, by), max(ax, bx), max(ay, by), 5)
        car = 5
    else:
        for x0, y0, x1, y1 in arms:
            _rect(g, x0, y0, x1, y1, 2)
        for x0, y0, x1, y1 in arms:
            _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 6)
        for y in range(2, 30):
            for x in range(4, 36):
                if g[y][x] == 6 and ((x - 4) % 3 == 0 or (y - 2) % 3 == 0):
                    g[y][x] = 7
        car = 1
    for rows, x, y in ((["..#..", ".###.", "#####"], 17, 4), (["#####", ".###.", "..#.."], 17, 24),
                       (["..#", ".##", "###", ".##", "..#"], 6, 13), (["#..", "##.", "###", "##.", "#.."], 31, 13)):
        _stamp(g, rows, x, y, car)


def _guide_pages(d):
    p2, p3 = _grid(40, 128), _grid(40, 128)
    _pad(p2, d)
    _key(p2, 9, 60, 30, 81, d, "A", 2)
    _key(p2, 9, 100, 30, 121, d, "B", 2)
    for y0, word in ((1, "START"), (41, "SELECT")):
        rows = _glyphs(word)
        w = len(rows[0])
        sh = 2 if d != "C" else 2
        _stamp(p3, rows, 20 - w // 2, y0 + 3, 5, sh)
        _key(p3, 13, y0 + 18, 26, y0 + 27, d)
    _key(p3, 1, 89, 17, 102, d, "L")
    _key(p3, 22, 89, 38, 102, d, "R")
    return p2, p3


def guide(d, base):
    px, pal = _bgt(base)
    p2, p3 = _guide_pages(d)
    errs = _fit(px, p2, _map(OS + "controls_guide_page_2.bin"), 5, 3, allow=GUIDE_TILES)
    errs += _fit(px, p3, _map(OS + "controls_guide_page_3.bin"), 5, 3, allow=GUIDE_TILES)
    if errs:
        sys.exit("gbanewgame: guide %s: %s" % (d, "; ".join(errs[:4])))
    for i in range(1, 8):                          # 8-15 of row 3 stay: tiles 2, 14, 15 (drawn with row 13) keep theirs
        pal[48 + i] = GUIDE_PAL[d][i]
    return {OS + "bg_tiles.png": _bgt_image(px, pal)}


# ================================================================================================= window (row 2)
WINDOW_TILES = set(range(3, 13)) | {94} | set(range(96, 151))
WIN_PAL = {   # 1 shadow, 2 inner, 3 light, 4 fill, 5 mark, 6 line, 7 strip, 8 outer, 9 faint
    "A": [None, (150, 190, 182), (200, 232, 224), TEAL, PAPER, (206, 226, 222), TEAL_DK, SLATE_OUT, NAVY,
          (232, 242, 240)],
    "B": [None, (150, 190, 182), (210, 236, 228), TEAL, PAPER, (200, 222, 216), TEAL_DK, SLATE_OUT, NAVY,
          (176, 222, 208)],
    "C": [None, (150, 190, 182), (200, 232, 224), TEAL, PAPER, (204, 224, 220), TEAL_DK, SLATE_OUT, NAVY,
          (232, 240, 238)],
}
RING = None


def _interior(d):
    """The fill tile, drawn the same under a vertical flip (tiles 11 and 12 are placed flipped)."""
    t = [[4] * 8 for _ in range(8)]
    if d == "A":
        for i in range(8):
            t[0][i] = t[7][i] = 9
            t[i][0] = t[i][7] = 9
    elif d == "C":
        for i in range(8):
            t[0][i] = t[7][i] = 9
    return t


def _window_cells(base):
    ents = _map(OS + "pikachu_intro/tilemap.bin")
    cells = [(i % 30, i // 30) for i, e in enumerate(ents) if 97 <= (e & 0x3FF) <= 150]
    xs, ys = [c for c, _ in cells], [r for _, r in cells]
    return ents, (min(xs), min(ys), max(xs), max(ys))


def _emblem(d, w, h):
    """The watermark in local indices over a W x H field: 5 its mark, 0 where the interior shows."""
    g = _grid(w, h)
    cx, cy = w / 2 - 0.5, h / 2 - 0.5
    if d == "A":                                     # the CodeMusic ring: a ring with a gap and a dot
        for y in range(h):
            for x in range(w):
                r = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if 15.5 <= r <= 20.5 and not (x > cx + 8 and abs(y - cy) < 4):
                    g[y][x] = 5
                if r <= 4.5:
                    g[y][x] = 5
    elif d == "B":                                   # a quaver: a tilted head, a stem, a flag
        for y in range(h):
            for x in range(w):
                ex, ey = (x - (cx - 6)), (y - (cy + 11))
                u, v = ex * 0.9 + ey * 0.45, -ex * 0.45 + ey * 0.9
                if (u / 9) ** 2 + (v / 6) ** 2 <= 1:
                    g[y][x] = 5
        sx = int(cx + 1)
        _rect(g, sx, int(cy - 19), sx + 2, int(cy + 9), 5)
        for i in range(12):
            _rect(g, sx + 2 + i // 2, int(cy - 19) + i, sx + 4 + i // 2, int(cy - 18) + i, 5)
    else:                                            # 0 1, the house's digits at 4x
        zero = [".111.", "1...1", "1..11", "1.1.1", "11..1", "1...1", ".111."]
        one = ["..1..", ".11..", "..1..", "..1..", "..1..", "..1..", ".111."]
        _stamp(g, _scale([r.replace("1", "#") for r in zero], 4), 4, int(cy - 14), 5)
        _stamp(g, _scale([r.replace("1", "#") for r in one], 4), 28, int(cy - 14), 5)
    return g


def window(d, base):
    px, pal = _bgt(base)
    old = [[v % 16 for v in r] for r in px]
    T = lambda t: _tile_get(old, t)
    # the frame: pret's layering kept, the four corners made square (each corner mitred from its two edges)
    top, bot, left, right = T(4), T(9), T(6), T(7)
    tiles = {4: top, 9: bot, 6: left, 7: right, 94: T(94)}
    tiles[3] = [[top[y][x] if y <= x else left[y][x] for x in range(8)] for y in range(8)]
    tiles[5] = [[top[y][x] if y <= 7 - x else right[y][x] for x in range(8)] for y in range(8)]
    tiles[8] = [[bot[y][x] if 7 - y <= x else left[y][x] for x in range(8)] for y in range(8)]
    tiles[10] = [[bot[y][x] if y >= x else right[y][x] for x in range(8)] for y in range(8)]
    fill = _interior(d)
    tiles[96] = fill
    if d == "B":                                     # pret's dashed rules, solid and full width
        r11, r12 = [rr[:] for rr in fill], [rr[:] for rr in fill]
        r11[2] = r11[3] = [9] * 8
        r12[0] = r12[1] = [9] * 8
        tiles[11], tiles[12] = r11, r12
    else:
        tiles[11], tiles[12] = fill, fill
    for t, tile in tiles.items():
        _tile_put(px, t, [[(32 + v) if v else 0 for v in rr] for rr in tile])
    ents, (c0, r0, c1, r1) = _window_cells(base)
    w, h = (c1 - c0 + 1) * 8, (r1 - r0 + 1) * 8
    em = _emblem(d, w, h)
    target = _grid(240, 160)
    for y in range(h):
        for x in range(w):
            target[r0 * 8 + y][c0 * 8 + x] = em[y][x] or fill[y % 8][x % 8]
    errs = _fit(px, target, ents, 30, 2, allow=set(range(97, 151)))
    if errs:
        sys.exit("gbanewgame: window %s: %s" % (d, "; ".join(errs[:4])))
    wp = WIN_PAL[d]
    for i in range(1, 10):
        pal[32 + i] = wp[i]
    return {OS + "bg_tiles.png": _bgt_image(px, pal)}


# ================================================================================================= oak_bg (row 0)
OAK_PAL = {
    "A": [(232, 244, 238), (212, 234, 226), (176, 216, 204), (136, 196, 180), (96, 170, 156), (64, 140, 128),
          (48, 112, 104), (36, 88, 84)],
    "B": [PAPER, (216, 232, 226), TEAL, TEAL_DK, (150, 206, 190), (96, 170, 156), (64, 140, 128), (48, 112, 104)],
    "C": [NAVY, (34, 54, 92), (32, 84, 112), (40, 112, 124), (56, 144, 136), (20, 48, 64), TEAL_DK, (16, 30, 52)],
}
#  palette-row-0 index of each colour above: 8, 7, 6, 5, 4, 3, 2, 1 (pret's ramp, light to dark)
_IDX = [8, 7, 6, 5, 4, 3, 2, 1]


def _oak_tiles(d):
    """{tile: 8x8 of row-0 indices} for the seven placed tiles: 8 sky, 7 (twice), 6, 5, 4, 3 the horizon, 2 floor."""
    t = {}
    fill = lambda v: [[v] * 8 for _ in range(8)]
    if d == "A":
        shade = {8: (8, 7), 7: (8, 7), 6: (6, 5), 5: (5, 4), 4: (4, 3), 3: (3, 2), 2: (2, 1)}
        for n, (f, ln) in shade.items():
            tl = fill(f)
            for i in range(8):
                tl[0][i] = ln
                tl[i][0] = ln
            t[n] = tl
    elif d == "B":                                   # a stave across the horizon: five lines, 4px apart
        t[8] = fill(8)
        t[7] = fill(8)
        t[7][0] = t[7][4] = [6] * 8                  # tile 7 lies on two bands: four lines
        t[6] = fill(8)
        t[6][0] = [6] * 8                            # the fifth
        t[5] = fill(8)
        t[4] = fill(7)
        t[3] = fill(4)
        t[3][0] = [5] * 8
        t[2] = fill(3)
        t[2][3][3] = 2
    else:
        t[8] = fill(8); t[8][0] = [7] * 8
        t[7] = fill(7); t[7][4] = [6] * 8
        t[6] = fill(6); t[6][0] = [5] * 8
        t[5] = fill(5); t[5][0] = [4] * 8
        t[4] = fill(4); t[4][0] = [2] * 8
        t[3] = fill(3)
        t[2] = fill(3)
        for i in range(8):
            t[2][0][i] = 2
            t[2][i][0] = 2
    return t


def oak_bg(d, base):
    im = base[OS + "oak_speech_bg.png"]
    px = _px(im)
    for n, tl in _oak_tiles(d).items():
        tx, ty = (n % 2) * 8, (n // 2) * 8
        for y in range(8):
            for x in range(8):
                px[ty + y][tx + x] = tl[y][x]
    bpx, bpal = _bgt(base)
    for col, i in zip(OAK_PAL[d], _IDX):
        bpal[i] = col
    opal = _pal_of(im)
    for col, i in zip(OAK_PAL[d], _IDX):
        opal[i] = col
    return {OS + "oak_speech_bg.png": _like(im, px, opal), OS + "bg_tiles.png": _bgt_image(bpx, bpal)}


# ================================================================================================= platform
PLAT_PAL = {   # 11 light rim, 12 highlight, 13 lines, 14 fill, 15 rim
    "A": {11: (232, 248, 240), 12: (232, 248, 240), 13: (150, 208, 190), 14: (200, 236, 222), 15: TEAL_DK},
    "B": {11: (232, 248, 240), 12: (232, 248, 240), 13: PAPER, 14: (200, 236, 222), 15: TEAL_DK},
    "C": {11: (232, 248, 240), 12: (232, 248, 240), 13: TEAL_DK, 14: (208, 238, 226), 15: TEAL_DK},
}


def platform(d, base):
    old = base[OS + "platform.png"]
    opx = _px(old)
    comp = _grid(96, 32)
    for f in range(3):
        for y in range(32):
            for x in range(32):
                comp[y][f * 32 + x] = opx[f * 32 + y][x]
    foot = {(x, y) for y in range(32) for x in range(96) if comp[y][x]}
    cx, cy, rx, ry = 47.5, 12.0, 44.0, 11.5
    g = _grid(96, 32)
    for y in range(32):
        for x in range(96):
            e = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if e > 1 or (x, y) not in foot:
                continue
            inner = ((x - cx) / (rx - 3)) ** 2 + ((y - cy) / (ry - 2)) ** 2
            if d == "B":
                if inner > 1:
                    g[y][x] = 15
                elif ((x - cx) / (rx - 4)) ** 2 + ((y - cy) / (ry - 3)) ** 2 > 1:
                    g[y][x] = 12
            else:
                g[y][x] = 15 if inner > 1 else 14
                if d == "A" and inner <= 1 and ((int(x - cx) % 8 == 0) or (int(y - cy) % 4 == 0)):
                    g[y][x] = 13
                if d == "C" and inner <= 1 and y in (4, 8, 12, 16, 20):
                    g[y][x] = 13
                if inner <= 1 and y == int(cy - ry + 2) and g[y][x] == 14:
                    g[y][x] = 12
    if d == "B":                                     # twelve ticks round the ring
        import math
        for k in range(12):
            a = k * math.pi / 6
            x, y = int(round(cx + (rx - 5) * math.cos(a))), int(round(cy + (ry - 4) * math.sin(a)))
            if (x, y) in foot:
                g[y][x] = 15
    out = _grid(32, 96)
    for f in range(3):
        for y in range(32):
            for x in range(32):
                out[f * 32 + y][x] = g[y][f * 32 + x]
    pal = _jasc(P(OS + "platform.pal"))
    for i, c in PLAT_PAL[d].items():
        pal[i] = c
    return {OS + "platform.png": _like(old, out, pal), OS + "platform.pal": _jasc_text(pal)}


# ================================================================================================= the naming sprites
def _plate(g, y0, y1, cap, arrow):
    """The caption plate under a key: 15 dark, edged 4, the caption in 1."""
    _rect(g, 3, y0, 36, y1, 15)
    rows = _micro(cap)
    w = len(rows[0]) + (5 if arrow else 0)
    x0 = 20 - w // 2
    _stamp(g, rows, x0, y0 + (y1 - y0 + 1 - len(rows)) // 2, 1)
    if arrow:
        _stamp(g, TRI, x0 + len(rows[0]) + 2, y0 + (y1 - y0 + 1 - 5) // 2, 1)


def _keyface(g, x0, y0, x1, y1, d, word=None, hollow=False):
    _box(g, x0, y0, x1, y1, 14)                       # the ring the flash lights
    if hollow:
        _box(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 15)
        return
    if d == "A":
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 12)
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y0 + 1, 13); _rect(g, x0 + 1, y0 + 1, x0 + 1, y1 - 1, 13)
        _rect(g, x0 + 2, y1 - 1, x1 - 1, y1 - 1, 6)
        ink, sh = 1, 6
    elif d == "B":
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 13)
        ink, sh = 6, None
    else:
        _rect(g, x0 + 1, y0 + 1, x1 - 1, y1 - 1, 15)
        _rect(g, x0 + 4, y1 - 2, x1 - 4, y1 - 2, 12)
        ink, sh = 13, None
    if word:
        rows = _glyphs(word)
        _stamp(g, rows, (x0 + x1 + 1) // 2 - len(rows[0]) // 2, y0 + 2 + (1 if d != "C" else 0), ink, sh)


def _button(d, word, cap, arrow, off):
    g = _grid(40, 24)
    # the plate: pret's, 3 on its left and top edge, 4 inside, 15 on the right
    _rect(g, 1, 0 + off, 38, 23 + off, 4)
    _rect(g, 1, 0 + off, 1, 23 + off, 3); _rect(g, 2, 0 + off, 37, 0 + off, 3); _rect(g, 38, 1 + off, 38, 23 + off, 15)
    _keyface(g, 3, 2 + off, 36, 14 + off, d, word)
    _plate(g, 16 + off, 22 + off, cap, arrow)
    return g


def buttons(d, base):
    out = {}
    for rel, word, cap, arrow, off in ((NS + "back_button.png", "BACK", "B BUTTON", False, 0),
                                       (NS + "ok_button.png", "OK", "START", True, -2)):
        old = base[rel]
        g = _button(d, word, cap, arrow, off)
        foot = _px(old)
        if off < 0:                                   # pret's OK sits 2 rows up: its last rows are its shadow
            _rect(g, 2, 22, 37, 22, 15)
            for y in range(23, 24):
                g[y] = [0] * 40
        out[rel] = _like(old, g)
    return out


def page_swap(d, base):
    out = {}
    old = base[NS + "page_swap_frame.png"]
    g = _grid(40, 32)
    _rect(g, 0, 3, 37, 27, 4)
    _rect(g, 0, 3, 0, 27, 15); _rect(g, 1, 3, 37, 3, 3); _rect(g, 1, 4, 1, 26, 3); _rect(g, 38, 4, 38, 26, 15)
    _rect(g, 0, 27, 37, 27, 15)
    _keyface(g, 3, 5, 36, 17, d, hollow=True)
    _rect(g, 5, 7, 34, 15, 0)                          # the pill shows through
    _plate(g, 19, 25, "SELECT", True)
    out[NS + "page_swap_frame.png"] = _like(old, g)
    old = base[NS + "page_swap_button.png"]
    g = _grid(32, 16)
    _rect(g, 3, 4, 28, 12, 13)                       # square, inside pret's rounded pill
    out[NS + "page_swap_button.png"] = _like(old, g)
    for name, word, sh in (("upper", "UPPER", 7), ("lower", "lower", 9), ("others", "others", 11)):
        old = base[NS + "page_swap_%s.png" % name]
        g = _grid(40, 8)
        rows = _micro(word)
        if len(rows[0]) > 24:
            sys.exit("gbanewgame: %s is %d pixels, its label holds 24" % (word, len(rows[0])))
        x0, y0 = max(0, min(12 - len(rows[0]) // 2, 23 - len(rows[0]))), 7 - len(rows)
        if d == "A":                                  # pret's light ground kept, the word pale with a dark shadow
            _rect(g, 0, 0, 23, 7, sh)
            _stamp(g, rows, x0, y0 - 1, 1, sh - 1)
        elif d == "B":                                # the light ground, the word dark: inverse
            _rect(g, 0, 0, 23, 7, sh)
            _stamp(g, rows, x0, y0 - 1, sh - 1)
        else:                                         # no ground (the dark pill shows), the word pale, a light bar
            _stamp(g, rows, x0, max(0, y0 - 1), 1)
            _rect(g, x0, 7, x0 + len(rows[0]) - 1, 7, sh)
        out[NS + "page_swap_%s.png" % name] = _like(old, g)
    return out


def cursor(d, base):
    frames = {}
    for name, y0, y1, filled in (("cursor", 0, 15, False), ("cursor_squished", 3, 12, True),
                                 ("cursor_filled", 0, 15, True)):
        g = _grid(16, 24)
        x0, x1 = 2, 13
        if d == "A":
            ins = 1 if name == "cursor_squished" else 0
            if filled:
                _rect(g, x0 + 1 + ins, y0 + 1, x1 - 1 - ins, y1 - 1, 3)
            for cx, cy, sx, sy in ((x0 + ins, y0, 1, 1), (x1 - ins, y0, -1, 1), (x0 + ins, y1, 1, -1),
                                   (x1 - ins, y1, -1, -1)):
                for i in range(4):
                    for t in range(2):
                        g[cy + sy * t][cx + sx * i] = 1
                        g[cy + sy * i][cx + sx * t] = 1
        elif d == "B":
            if filled:
                _rect(g, x0, y0, x1, y1, 3)
            _box(g, x0, y0, x1, y1, 1, 2)
        else:
            if filled:
                _rect(g, x0, y0 if name == "cursor_filled" else 3, x1, 13, 3)
            by = 14 if name != "cursor_squished" else 12
            _rect(g, x0, by, x1, by + 1, 1)
            _rect(g, x0, by - 2, x0, by - 1, 1); _rect(g, x1, by - 2, x1, by - 1, 1)
        frames[NS + name + ".png"] = _like(base[NS + name + ".png"], g)
    return frames


def marks(d, base):
    a, u = _grid(8, 8), _grid(8, 8)
    if d == "A":
        _stamp(a, ["##....", ".##...", "..##..", "...##.", "..##..", ".##...", "##...."], 1, 0, 2, 3)
        _rect(u, 1, 6, 6, 7, 2)
    elif d == "B":
        _stamp(a, ["##....", "####..", "######", "####..", "##...."], 1, 1, 2, 3)
        _rect(u, 2, 6, 5, 6, 2); _rect(u, 2, 7, 5, 7, 3)
    else:
        _stamp(a, ["#..#..", ".#..#.", "..#..#", ".#..#.", "#..#.."], 1, 1, 2, 3)
        _rect(u, 1, 7, 6, 7, 2); u[5][1] = u[6][1] = u[5][6] = u[6][6] = 2
    return {NS + "input_arrow.png": _like(base[NS + "input_arrow.png"], a),
            NS + "underscore.png": _like(base[NS + "underscore.png"], u)}


def pc_icon(d, base):
    out = {}
    for name, on in (("pc_icon_off", False), ("pc_icon_on", True)):
        g = _grid(16, 24)
        if d == "A":                                   # a monitor on a keyboard; the caret blinks
            _rect(g, 2, 6, 13, 16, 2); _rect(g, 3, 7, 12, 15, 5); _rect(g, 4, 8, 11, 14, 15)
            _rect(g, 5, 9, 8, 9, 4)
            _rect(g, 5, 11, 9, 11, 4)
            if on:
                _rect(g, 5, 13, 6, 13, 6)
            _rect(g, 6, 17, 9, 17, 3)
            _rect(g, 1, 18, 14, 22, 2); _rect(g, 2, 19, 13, 21, 4)
            for x in range(3, 13, 2):
                g[20][x] = 2
        elif d == "B":                                 # a disk drive; its lamp blinks
            _rect(g, 1, 8, 14, 21, 2); _rect(g, 2, 9, 13, 20, 4); _rect(g, 2, 9, 13, 10, 5)
            _rect(g, 4, 13, 11, 14, 2)
            _rect(g, 3, 17, 4, 18, 6 if on else 3)
            _rect(g, 7, 18, 12, 18, 3)
        else:                                          # a tower; its two lights blink in turn
            _rect(g, 4, 3, 11, 22, 2); _rect(g, 5, 4, 10, 21, 4); _rect(g, 5, 4, 10, 5, 5)
            _rect(g, 6, 7, 9, 7, 2); _rect(g, 6, 9, 9, 9, 2)
            _rect(g, 6, 18, 6, 18, 6 if on else 3); _rect(g, 9, 18, 9, 18, 3 if on else 6)
        out[NS + name + ".png"] = _like(base[NS + name + ".png"], g)
    return out


DRAW = {"guide": guide, "window": window, "oak_bg": oak_bg, "platform": platform, "buttons": buttons,
        "page_swap": page_swap, "cursor": cursor, "marks": marks, "pc_icon": pc_icon}


# ================================================================================================= the contract
ROWS = {"guide": (3, GUIDE_TILES), "window": (2, WINDOW_TILES), "oak_bg": (0, set())}


def check(piece, files, base):
    errs = []
    for rel, v in files.items():
        old = base[rel]
        if rel.endswith(".pal"):
            if len(v.split()) != 3 + 48:
                errs.append("%s is not 16 colours" % rel)
            continue
        if v.size != old.size:
            errs.append("%s is %s, pret's %s" % (rel, v.size, old.size))
        if v.mode != "P":
            errs.append("%s is not indexed" % rel)
        if len(v.getpalette()) != len(old.getpalette()):
            errs.append("%s has %d colours, pret's %d" % (rel, len(v.getpalette()) // 3, len(old.getpalette()) // 3))
        if rel.endswith("bg_tiles.png"):
            row, own = ROWS[piece]
            a, b = _px(old), _px(v)
            for t in range(160):
                ta, tb = _tile_get(a, t), _tile_get(b, t)
                if t not in own and ta != tb:
                    errs.append("bg_tiles tile %d is not %s's to change" % (t, piece))
                if t in own and any(x and x // 16 != row for rr in tb for x in rr):
                    errs.append("bg_tiles tile %d leaves row %d" % (t, row))
            pa, pb = _pal_of(old), _pal_of(v)
            moved = [i for i in range(64) if pa[i] != pb[i] and i // 16 != row]
            if moved:
                errs.append("bg_tiles colours %s are outside row %d" % (moved, row))
        elif max(v.getdata()) > 15:
            errs.append("%s uses index %d" % (rel, max(v.getdata())))
        elif "naming_screen" in rel or rel.endswith("platform.png"):
            foot = {i for i, x in enumerate(old.getdata()) if x}
            if rel.endswith("page_swap_button.png") or rel.endswith("platform.png"):
                out = [i for i, x in enumerate(v.getdata()) if x and i not in foot]
                if out:
                    errs.append("%s draws %d pixels outside pret's footprint" % (rel, len(out)))
    if piece == "page_swap":
        for rel in ("upper", "lower", "others"):
            im = files[NS + "page_swap_%s.png" % rel]
            if any(x for i, x in enumerate(im.getdata()) if i % 40 >= 24):
                errs.append("page_swap_%s draws past its 24 loaded pixels" % rel)
    return errs


def save(files, root):
    for rel, v in files.items():
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if isinstance(v, str):
            open(dst, "w", newline="").write(v)
        else:
            v.save(dst)
            n = len(Image.open(dst).getpalette()) // 3
            if n != len(v.getpalette()) // 3:
                sys.exit("gbanewgame: %s saved with %d colours, not %d" % (dst, n, len(v.getpalette()) // 3))


def draft(out):
    base = _base()
    for piece in PIECES:
        for d in "ABC":
            files = DRAW[piece](d, base)
            errs = check(piece, files, base)
            if errs:
                sys.exit("gbanewgame: %s %s breaks its contract: %s" % (piece, d, "; ".join(errs)))
            save(files, os.path.join(out, piece, d))
            print("  %-9s %s %-13s %s" % (piece, d, NAMES[piece][d], ", ".join(sorted(files))))
    print("  DRAFT -- nothing in the engine; recommended: %s"
          % ", ".join("%s %s" % (p, RECOMMENDED[p]) for p in PIECES))


def composed(picks, base=None):
    """The files --write --approved makes: each pick drawn over the last (bg_tiles is shared by three pieces)."""
    base = dict(base or _base())
    out = {}
    for piece in PIECES:
        if piece in picks:
            files = DRAW[piece](picks[piece], base)
            base.update(files)
            out.update(files)
    return out


def report():
    print("gbanewgame (T-568): the new game and the name. APPROVED: %s" % (APPROVED or "none -- nothing is written"))
    base = _base()
    for piece in PIECES:
        for d in "ABC":
            errs = check(piece, DRAW[piece](d, base), base)
            print("  %-9s %s %-13s %s" % (piece, d, NAMES[piece][d], "ok" if not errs else "; ".join(errs)))
    drift = []
    for rel, v in composed(APPROVED, base).items():
        dst = P(rel)
        same = open(dst).read() == v if isinstance(v, str) else (
            list(Image.open(dst).getdata()) == list(v.getdata()) and Image.open(dst).getpalette() == v.getpalette())
        if not same:
            drift.append(rel)
    for rel in drift:
        print("  DRIFT: engineGba/%s is not what --write --approved makes" % rel)
    return 1 if drift else 0


# ================================================================================================= the sheets
def _gba(c):
    return tuple(((v >> 3) << 3) | ((v >> 3) >> 2) for v in c[:3])


def _layer(img, ents, cols, rows, at, pal, pals=None):
    """A BG layer drawn from IMG's tiles by a map: (RGB, mask) on a 240x160 screen, the map's top-left at AT (tiles)."""
    px = _px(img)
    out = Image.new("RGB", (240, 160)); m = Image.new("L", (240, 160)); op, mp = out.load(), m.load()
    for i, e in enumerate(ents):
        r, c = divmod(i, cols)
        if r >= rows:
            break
        t, hf, vf, pn = e & 0x3FF, e & 0x400, e & 0x800, e >> 12
        if t == 0 or (pals is not None and pn not in pals):
            continue
        tl = _tile_get(px, t)
        for y in range(8):
            for x in range(8):
                v = tl[7 - y if vf else y][7 - x if hf else x]
                X, Y = (c + at[0]) * 8 + x, (r + at[1]) * 8 + y
                if v and 0 <= X < 240 and 0 <= Y < 160:
                    op[X, Y] = _gba(pal[pn * 16 + v % 16]); mp[X, Y] = 255
    return out, m


def _bg_swap(frame, today, new, tol=0):
    """Where the frame shows today's layer, or the bare backdrop under the layer's cells, put the new layer (or the
    backdrop where the new one is clear). The backdrop is the frame's commonest colour among today's clear pixels."""
    from collections import Counter
    fp, tp, tm, np_, nm = frame.load(), today[0].load(), today[1].load(), new[0].load(), new[1].load()
    clear = Counter(fp[x, y] for y in range(0, 160, 2) for x in range(0, 240, 2) if not tm[x, y])
    back = clear.most_common(1)[0][0] if clear else (0, 0, 0)
    out = frame.copy(); op = out.load()
    near = lambda a, b: all(abs(a[i] - b[i]) <= tol for i in range(3))
    for y in range(160):
        for x in range(240):
            shows = near(fp[x, y], tp[x, y]) if tm[x, y] else near(fp[x, y], back)
            if shows and (tm[x, y] or nm[x, y]):
                op[x, y] = np_[x, y] if nm[x, y] else back
    return out


def _sprite(im, pal):
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); op = out.load(); sp = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if sp[x, y]:
                op[x, y] = _gba(pal[sp[x, y]]) + (255,)
    return out


def sheets(out_dir, fdir):
    import gbaevolve as ev
    from PIL import ImageDraw
    os.makedirs(out_dir, exist_ok=True)
    base = _base()
    D = ["today", "A", "B", "C"]
    fr = lambda stop, name: Image.open(os.path.join(fdir, "%02d" % stop, name)).convert("RGB")
    files = {d: (base if d == "today" else dict(base, **DRAW_ALL[d])) for d in D}
    jp = lambda d, rel: _jasc(P(rel)) if d == "today" or rel not in DRAW_ALL[d] else \
        [tuple(int(x) for x in DRAW_ALL[d][rel].split()[3 + i * 3:6 + i * 3]) for i in range(16)]
    made = []

    def lab(piece):
        return ["TODAY (pret's)"] + ["%s  %s" % (d, NAMES[piece][d]) for d in "ABC"]

    def sub(piece):
        return "   ".join("%s: %s" % (d, LINES[piece][d]) for d in "ABC")[:260]

    def bg_swap(frame, d, img_rel, ents, cols, rows, at, pals, palsrc):
        t = files["today"][img_rel]; n = files[d][img_rel]
        tl = _layer(t, ents, cols, rows, at, _pal_of(files["today"][palsrc]), pals)
        nl = _layer(n, ents, cols, rows, at, _pal_of(files[d][palsrc]), pals)
        return _bg_swap(frame, tl, nl)

    # ---- the guide: pages 2 and 3
    p2, p3 = fr(2, "s02_02.png"), fr(2, "s02_03.png")
    rows = [[], [], []]
    g2 = _map(OS + "controls_guide_page_2.bin"); g3 = _map(OS + "controls_guide_page_3.bin")
    for d in D:
        a = bg_swap(p2, d, OS + "bg_tiles.png", g2, 5, 16, (1, 3), {3}, OS + "bg_tiles.png")
        b = bg_swap(p3, d, OS + "bg_tiles.png", g3, 5, 16, (1, 3), {3}, OS + "bg_tiles.png")
        strip = Image.new("RGB", (100, 128)); strip.paste(a.crop((0, 24, 50, 152)), (0, 0)); strip.paste(
            b.crop((0, 24, 50, 152)), (50, 0))
        rows[0].append(ev.X(strip, 3)); rows[1].append(ev.X2(a)); rows[2].append(ev.X2(b))
    made.append(ev._sheet(os.path.join(out_dir, "t568_guide.png"), "T-568 DRAFT: the CONTROLS guide's buttons",
                          sub("guide"), lab("guide"), rows, ["the icons at 3x", "page 2, in context, 2x",
                                                             "page 3, in context, 2x"]))

    # ---- the window: the panel SEEKMUSAI stands on
    f = fr(3, "s03_00.png")
    pk = _map(OS + "pikachu_intro/tilemap.bin")
    rows = [[], []]
    for d in D:
        a = bg_swap(f, d, OS + "bg_tiles.png", pk, 30, 19, (0, 2), {2}, OS + "bg_tiles.png")
        rows[0].append(ev.X(a.crop((120, 80, 240, 160)), 3)); rows[1].append(ev.X2(a))
    made.append(ev._sheet(os.path.join(out_dir, "t568_window.png"), "T-568 DRAFT: the intro panel and its watermark",
                          sub("window"), lab("window"), rows, ["its corner at 3x", "in context, 2x"]))

    # ---- CRYSTAL's scene: the backdrop and the platform, alone and together
    for piece in ("oak_bg", "platform"):
        rows = [[], []]
        for d in D:
            ims = []
            for name in ("s04_00.png", "s04_03.png"):
                fm = fr(4, name)
                ims.append(_scene(fm, d if piece == "oak_bg" else "today", d if piece == "platform" else "today",
                                  files, jp))
            rows[0].append(ev.X2(ims[0])); rows[1].append(ev.X2(ims[1]))
        made.append(ev._sheet(os.path.join(out_dir, "t568_%s.png" % piece), "T-568 DRAFT: CRYSTAL's scene, %s"
                              % ("the backdrop" if piece == "oak_bg" else "the platform"), sub(piece), lab(piece),
                              rows, ["CRYSTAL, in context, 2x", "the player, in context, 2x"]))
    rows = [[]]
    for d in D:
        rows[0].append(ev.X2(_scene(fr(4, "s04_01.png"), d, d, files, jp)))
    made.append(ev._sheet(os.path.join(out_dir, "t568_scene_together.png"),
                          "T-568 DRAFT: CRYSTAL's scene, the backdrop and the platform together (same letter)",
                          "each column is that letter for both pieces", ["TODAY (pret's)", "A", "B", "C"], rows,
                          ["with the daemon, 2x"]))

    # ---- the naming screen: every part in context
    up, lo, ot = fr(5, "s05_00.png"), fr(5, "s05_01.png"), fr(5, "s05_02.png")
    press = fr(5, "s05_03_b_00.png")
    names = sorted(os.listdir(os.path.join(fdir, "05")))
    okf = fr(5, [n for n in names if n.startswith("s05_") and "_b_" in n][-1])
    rows = [[], [], [], [], []]
    for d in D:
        views = [_naming(fm, d, files, jp, page) for fm, page in ((up, "upper"), (lo, "lower"), (ot, "others"))]
        views.append(_naming(press, d, files, jp, "upper", squished=True))
        views.append(_naming(okf, d, files, jp, "upper", pc=True))
        for i, v in enumerate(views):
            rows[i].append(ev.X2(v))
    made.append(ev._sheet(os.path.join(out_dir, "t568_naming.png"),
                          "T-568 DRAFT: the naming screen's parts (each column one letter for every part)",
                          "buttons, page key, cursor, marks and PC icon; T-363's palettes kept",
                          ["TODAY (pret's)", "A", "B", "C"], rows,
                          ["UPPER, 2x", "lower", "others", "a key pressed (the squish)",
                           "on OK; the PC icon a BOX's naming shows, composed offline"]))
    rows = [[]]
    for d in D:
        parts = Image.new("RGB", (250, 40), (24, 40, 80))
        x = 2
        for rel, pr in ((NS + "back_button.png", NS + "buttons.pal"), (NS + "ok_button.png", NS + "buttons.pal"),
                        (NS + "page_swap_frame.png", NS + "buttons.pal"), (NS + "cursor.png", NS + "cursor.pal"),
                        (NS + "cursor_squished.png", NS + "cursor.pal"), (NS + "cursor_filled.png", NS + "cursor.pal"),
                        (NS + "input_arrow.png", NS + "page_swap_others.pal"),
                        (NS + "underscore.png", NS + "page_swap_others.pal"),
                        (NS + "pc_icon_off.png", NS + "menu.pal"), (NS + "pc_icon_on.png", NS + "menu.pal")):
            s = _sprite(files[d][rel], _jasc(P(pr)))
            parts.paste(s, (x, 4), s)
            x += s.width + 2
        rows[0].append(ev.X(parts, 3))
    made.append(ev._sheet(os.path.join(out_dir, "t568_naming_parts.png"), "T-568 DRAFT: the naming parts at 3x",
                          "BACK, OK, the page key, the cursor and its press, the arrow, the underscore, the PC icon",
                          ["TODAY (pret's)", "A", "B", "C"], rows, ["at 3x"]))
    return made


def _scene(frame, dbg, dplat, files, jp):
    """CRYSTAL's scene with the backdrop from DBG's files and the platform from DPLAT's. The backdrop is rendered for
    both today and the draft and swapped where the frame shows it; the platform is found where today's sits (under
    whoever stands on it), and redrawn only where the frame showed the backdrop or the old platform."""
    import gbaevolve as ev
    ents = _map(OS + "oak_speech_bg.bin")
    tl = _layer(files["today"][OS + "oak_speech_bg.png"], ents, 32, 20, (0, 0), _pal_of(files["today"][OS + "bg_tiles.png"]))
    nl = _layer(files[dbg][OS + "oak_speech_bg.png"], ents, 32, 20, (0, 0), _pal_of(files[dbg][OS + "bg_tiles.png"]))
    out = _bg_swap(frame, tl, nl)

    def comp(d):
        im = files[d][OS + "platform.png"]
        pal = jp(d, OS + "platform.pal")
        s = _sprite(im, pal)
        c = Image.new("RGBA", (96, 32), (0, 0, 0, 0))
        for f in range(3):
            c.paste(s.crop((0, f * 32, 32, f * 32 + 32)), (f * 32, 0))
        return c
    old, new = comp("today"), comp(dplat)
    ox, oy = 72, 96
    fp, op, ol, nw, tp, np_ = frame.load(), out.load(), old.load(), new.load(), tl[0].load(), nl[0].load()
    for y in range(32):
        for x in range(96):
            X, Y = ox + x, oy + y
            if not (0 <= X < 240 and 0 <= Y < 160):
                continue
            was_bg = fp[X, Y] == tp[X, Y]
            was_plat = ol[x, y][3] and fp[X, Y] == ol[x, y][:3]
            if was_bg or was_plat:
                op[X, Y] = nw[x, y][:3] if nw[x, y][3] else np_[X, Y]
    return out


def _naming(frame, d, files, jp, page, squished=False, pc=False):
    """The naming frame with each part found where today's sits and redrawn from D's files."""
    import gbaevolve as ev
    out = frame.copy()
    parts = [(NS + "back_button.png", NS + "buttons.pal"), (NS + "ok_button.png", NS + "buttons.pal"),
             (NS + "page_swap_frame.png", NS + "buttons.pal"), (NS + "input_arrow.png", NS + "page_swap_others.pal")]
    for rel, pr in parts:
        old, new = _sprite(files["today"][rel], _jasc(P(pr))), _sprite(files[d][rel], _jasc(P(pr)))
        at = ev._find(out, old, tol=16, accept=0.15)
        if at:
            out = ev._replace(out, old, new, at)
    nxt = {"upper": "lower", "lower": "others", "others": "upper"}[page]
    old_l = _sprite(files["today"][NS + "page_swap_%s.png" % nxt].crop((0, 0, 24, 8)), _jasc(P(NS + "buttons.pal")))
    at = ev._find(out, old_l, tol=20, accept=0.25)
    if at:
        pc_ = list(_jasc(P(NS + "page_swap_%s.pal" % page)))
        pc_[13] = out.load()[191, 79]                      # the pill on screen (the next page's 13), beside the label
        pill_o = _sprite(files["today"][NS + "page_swap_button.png"], pc_)
        pill_n = _sprite(files[d][NS + "page_swap_button.png"], pc_)
        new_l = _sprite(files[d][NS + "page_swap_%s.png" % nxt].crop((0, 0, 24, 8)), _jasc(P(NS + "buttons.pal")))
        pat = (188, 75)                                    # naming_screen.c: the pill 32x16 centred at (204, 83)
        out = ev._replace(out, old_l, Image.new("RGBA", (24, 8), (0, 0, 0, 0)), at)
        if pat:
            out = ev._replace(out, pill_o, pill_n, pat)
        out.paste(new_l, at, new_l)
    us_o = _sprite(files["today"][NS + "underscore.png"], _jasc(P(NS + "page_swap_others.pal")))
    us_n = _sprite(files[d][NS + "underscore.png"], _jasc(P(NS + "page_swap_others.pal")))
    for _ in range(8):
        at = ev._find(out, us_o, tol=12, accept=0.0)
        if not at:
            break
        out = ev._replace(out, us_o, us_n, at)
    # the cursor: found by its pink (cursor.pal 1-3), not by shape -- it is blended and flashing
    fp = out.load()
    pink = [(x, y) for y in range(160) for x in range(240)
            if fp[x, y][0] > fp[x, y][1] + 25 and fp[x, y][0] > fp[x, y][2] + 5 and x < 180 and y > 60]
    if pink:
        x0, y0 = min(p[0] for p in pink), min(p[1] for p in pink)
        name = "cursor_squished" if squished else "cursor"
        top = 3 if squished else 0
        o = _sprite(files["today"][NS + name + ".png"], _jasc(P(NS + "cursor.pal")))
        out = ev._replace(out, o, _sprite(files[d][NS + name + ".png"], _jasc(P(NS + "cursor.pal"))), (x0 - 2, y0 - top))
    if pc:
        icon = _sprite(files[d][NS + "pc_icon_on.png"], _jasc(P(NS + "menu.pal")))
        from collections import Counter
        box = out.load()
        fill = Counter(box[x, y] for y in range(26, 54) for x in range(46, 66)).most_common(1)[0][0]
        for y in range(26, 54):
            for x in range(46, 66):
                box[x, y] = fill
        out.paste(icon, (48, 29), icon)
    return out


DRAW_ALL = {}


def _draw_all():
    base = _base()
    for d in "ABC":
        DRAW_ALL[d] = composed({p: d for p in PIECES}, base)


def main():
    a = sys.argv
    if "--write" in a:
        if "--approved" not in a:
            sys.exit("gbanewgame: --write needs --approved (it writes APPROVED, the user's picks)")
        if not APPROVED:
            print("gbanewgame: nothing approved yet (T-568 is a DRAFT); nothing written")
            return 0
        files = composed(APPROVED)
        save(files, GBA)
        for piece, d in APPROVED.items():
            print("  wrote %s %s (%s)" % (piece, d, NAMES[piece][d]))
        return 0
    if "--draft" in a:
        i = a.index("--draft")
        draft(a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else DRAFT)
    if "--sheets" in a:
        _draw_all()
        sheets(a[a.index("--sheets") + 1], a[a.index("--frames") + 1] if "--frames" in a else FRAMES)
    if "--draft" not in a and "--sheets" not in a:
        return report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
