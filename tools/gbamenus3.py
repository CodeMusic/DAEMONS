#!/usr/bin/env python3
"""T-554: the menu leftovers -- the Nintendo art every menu still shows, after T-523 and T-530 (batch 1 of the
2026-11-14 re-census). APPROVED 2026-11-14 (the user: A for every piece; the std frame's version 1 is gbaframes').

    python3 tools/gbamenus3.py                      # report: each piece's engine files, its contract, APPROVED
    python3 tools/gbamenus3.py --draft [DIR]        # draw every piece's A/B/C into DIR (gfx/drafts/t554_menus/): the
                                                    #   files as the engine takes them (A/ B/ C/ graphics/...) and a
                                                    #   contact sheet per piece -- today beside each draft at 2x, in
                                                    #   the real screens (theatre shots when --shots names them)
    python3 tools/gbamenus3.py --draft --shots DIR  # the theatre's 'today' shots (tools/routes/t554_menus_today.json)
    python3 tools/gbamenus3.py --write --approved --all | --pick piece=A,...
                                                    # write APPROVED (empty: refuses until the user picks)

The std 3x3 frame is not here: it is a frame, so tools/gbaframes.py owns it (--std-draft, --std N, APPROVED_STD), and
it is drawn to match the user's A TERMINAL (T-523's type1). This tool draws the pieces that are not frames, each in
three directions inside the A TERMINAL family (slate rule, 45-degree corners, the teal bracket, paper, graph paper):
A the closest continuation of what T-523/T-530 built, B and C alternatives. Every pixel is drawn in code, on the
engine's own grids; the engine's files are read for their SHAPE only (which tile each map puts where, which slot
the code reads), at engine BASE3, so a write never reads its own output back.

THE PIECES, and what each drop-in keeps (report() prints it):
  bag        item_menu/bg.png: 55 tiles redrawn IN PLACE on bg.bin and bg_item_pc.bin (both kept), three palette
             rows kept as rows -- 0 the screen (bg.bin rows 0-13), 1 the description band (SetBgTilemapPalette forces
             rows 14-19 to 1), 2 the band dimmed while a menu is up (1 + the dim) -- and bg_female.pal (row 0 again:
             nobody is a boy or a girl). Kept for the text the bag prints over it (palette 15, sTextColors): the
             pocket name WHITE on a dark bar (cols 1-9, rows 1-2), the list DARK on paper (cols 11-28, rows 1-12),
             the description WHITE on the band; the icon box light under the item's icon.
  arrows     interface/red_arrow_other.png (the list's up/down and the pockets' left/right, flipped by OAM),
             red_arrow.png (the right-pointing cursor), selector_outline.png: ONE palette, red_arrow.pal
             (sRedArrowPal), shared by all three -- so they change together. 1 body, 2 edge; 3 joins (was unused
             magenta). Footprints kept (16x32, 16x16, 24x24), each frame's centre where the code puts it.
  select     interface/select_button.png: 24x16 blitted (BlitBitmapToWindow, x 0x70) beside the registered item in
             the bag's list window, so drawn in the bag's text palette 15 (bag_window_pal.pal): 13, 14, 15 are its
             own (sTextColors reads 1, 2, 3, 8, 9 only) and retinted; 1-9 kept.
  swap       interface/bag_swap.png: the line that follows an item being moved; its own palette (14 line, 15 head).
             2px line on rows 6-7 of each 16x16 frame kept (the code lays frames end to end).
  fieldicons items/icons/return_to_field_arrow.png (CLOSE BAG's icon) and question_mark.png (an item with no icon),
             24x24 each with its own icon palette, in T-525's icon family.
  keypad     fonts/keypad_icons.png: A B L R START SELECT, the d-pad four ways, up-down, left-right, none -- blitted
             into the TEXT window they sit in, so drawn in the text slots: 1 the cap's face, 2 ink, 3 the light ink,
             4 the pressed arm (red). sKeypadIcons' rects kept: x/width per icon, 12 rows tall from the cell's top,
             ink only on rows 4-11 as today (trap 38: nothing taller than the line it sits in).
  markings   misc/mon_markings.png (the 32x8 combo: 16 rows, one per on/off set, the four marks; own palette, 1/2 off,
             3/4 on) and misc/markings2.png (the MARK menu: frames 0-7 the marks off/on, 8 the cursor, 9.. the 32x32
             OK/CANCEL text laid one tile on in 1-D order; own palette). The words OK and CANCEL are kept, set in
             SCREEN's small face.
  pcparts    pokemon_storage/cursor_shadow.png (16x16 under the PAW, misc2's 8 and 15 -- shared with the PAW and the
             scroll arrows, so KEPT) and item_info_frame.png (the MOVE ITEMS info window's edge: 4 tiles, top, side,
             two corners, the top V-flipped for the bottom; palette 15 = its PNG's: 1-3 the window's text, kept;
             4, 7, 9, 10, 11 its own, retinted).

NO NEW WORDS. OK, CANCEL, SEL, START, SELECT, A, B, L, R are FireRed's words, redrawn; nothing else is painted.
"""
import argparse, os, struct, subprocess, sys, tempfile, atexit, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import gbamenus as M
from gbamenus import (q5, lum, canvas, fill, put, cut_box, retile, render_map, idx_rgba, say, text_width, contact,
                      put_files, SLATE_OUT, SLATE_MID, SLATE_LIGHT, TEAL, TEAL_DK, PAPER, AMBER, AMBER_DK)

ROOT, GBA, G = M.ROOT, M.GBA, M.G
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t554_menus")
PIECES = ("bag", "arrows", "select", "swap", "fieldicons", "keypad", "markings", "pcparts")
NAMES = {
    "bag": {"A": "TERMINAL DESK", "B": "BRASS LEDGER", "C": "READOUT"},
    "arrows": {"A": "TEAL CHEVRON", "B": "SLATE WEDGE", "C": "AMBER CARET"},
    "select": {"A": "SLATE KEY", "B": "TEAL TAG", "C": "BRACKETED"},
    "swap": {"A": "TEAL CARET", "B": "NOTCHED RULE", "C": "DASHED"},
    "fieldicons": {"A": "RETURN KEY", "B": "OPEN DOOR", "C": "INK SLIP"},
    "keypad": {"A": "KEYCAP", "B": "INVERSE", "C": "TICKET"},
    "markings": {"A": "TERMINAL MARKS", "B": "PUNCH CARD", "C": "SIGILS"},
    "pcparts": {"A": "SLAB AND RULE", "B": "DIAMOND AND SLIP", "C": "TARGET AND TRACE"},
}
OFFERED = {p: "ABC" for p in PIECES}
RECOMMENDED = {p: "A" for p in PIECES}
#  The user, 2026-11-14 (multiple choice): the bag A TERMINAL DESK, and A for every small piece (TEAL CHEVRON,
#  SLATE KEY, TEAL CARET, RETURN KEY, KEYCAP, TERMINAL MARKS, SLAB AND RULE). --write --approved --all writes these.
APPROVED = {p: "A" for p in PIECES}

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--shots", help="the theatre's today shots (a t554_menus_today route folder)")
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--pick")
ap.add_argument("--all", action="store_true")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes runs the write")
ARGS = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

SLATE_DK, SLATE_2 = (64, 76, 92), (128, 144, 160)
GRAPH, GRID = (232, 236, 240), (206, 214, 222)
SCREEN, PHOS, PHOS_DIM, PHOS_SH = (20, 32, 36), (184, 240, 208), (64, 112, 100), (40, 72, 64)
INKB, BRASS, BRASS_DK, BRASS_LT, CREAM = (40, 34, 32), (190, 150, 72), (120, 88, 40), (232, 200, 120), (252, 248, 236)

# ================================================================================================ files at BASE3
BASE3 = "a2a445435"          # origin/context-content when T-554 was drafted: every file here still pret's drawing
_B = {}


def src(rel):
    if rel not in _B:
        if "dir" not in _B:
            if subprocess.run(["git", "-C", GBA, "cat-file", "-e", BASE3 + "^{commit}"], capture_output=True).returncode:
                sys.exit("gbamenus3: the engine has no commit %s to read the shapes from" % BASE3)
            _B["dir"] = tempfile.mkdtemp(prefix="gbamenus3_")
            atexit.register(shutil.rmtree, _B["dir"], True)
        r = subprocess.run(["git", "-C", GBA, "show", "%s:graphics/%s" % (BASE3, rel)], capture_output=True)
        if r.returncode:
            _B[rel] = os.path.join(G, rel)
        else:
            q = os.path.join(_B["dir"], rel)
            os.makedirs(os.path.dirname(q), exist_ok=True)
            open(q, "wb").write(r.stdout)
            _B[rel] = q
    return _B[rel]


def png(rel):
    im = Image.open(src(rel))
    raw = im.getpalette() or []
    d = list(im.getdata())
    w, h = im.size
    return w, h, [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)], [[d[y * w + x] for x in range(w)] for y in range(h)]


def jpal(rel):
    w = open(src(rel)).read().split()
    k = int(w[2])
    v = list(map(int, w[3:3 + 3 * k]))
    return [tuple(v[3 * i:3 * i + 3]) for i in range(k)]


def map16(rel):
    d = open(src(rel), "rb").read()
    return [(e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12) for e in struct.unpack("<%dH" % (len(d) // 2), d)]


def tile_of(px, t, per):
    return [[px[(t // per) * 8 + y][(t % per) * 8 + x] & 15 for x in range(8)] for y in range(8)]


def mgba(c):
    """A colour as mGBA puts it on screen: 5 bits each, widened (c5 << 3 | c5 >> 2) -- to compare with theatre shots."""
    return tuple(((v >> 3) << 3) | ((v >> 3) >> 2) for v in c)


def glyph3(g, x, y, s, v, font=None):
    """A 3x5 (or narrower) cap word, 1px apart, at (x, y)."""
    f = font or F3
    for ch in s:
        rows = f[ch]
        for yy, r in enumerate(rows):
            for xx, c in enumerate(r):
                if c == "1":
                    put(g, x + xx, y + yy, v)
        x += len(rows[0]) + 1
    return x


F3 = {"A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
      "C": ["011", "100", "100", "100", "011"], "E": ["111", "100", "110", "100", "111"],
      "K": ["101", "101", "110", "101", "101"], "L": ["100", "100", "100", "100", "111"],
      "N": ["101", "111", "111", "111", "101"], "O": ["010", "101", "101", "101", "010"],
      "R": ["110", "101", "110", "101", "101"], "S": ["011", "100", "010", "001", "110"],
      "T": ["111", "010", "010", "010", "010"]}
F3N = dict(F3, E=["11", "10", "11", "10", "11"], L=["10", "10", "10", "10", "11"])      # SELECT in 24px


def wordw(s, font=None):
    f = font or F3
    return sum(len(f[c][0]) + 1 for c in s) - 1


# ================================================================================================ BAG
BAG = "item_menu"


def bag_shape():
    w, h, pal, px = png(BAG + "/bg.png")
    return px, w // 8, map16(BAG + "/bg.bin"), map16(BAG + "/bg_item_pc.bin"), pal


def bag_rows(direction):
    """Three rows of 16: 0 the screen, 1 the band, 2 the band dimmed. Slot 0 of row 0 is the backdrop: kept."""
    pal = bag_shape()[4]
    now = [list(pal[i * 16:i * 16 + 16]) for i in range(3)]
    if direction is None:
        return now
    r0 = [now[0][0]] + [(0, 0, 0)] * 15
    r1 = [(0, 0, 0)] * 16
    if direction == "A":
        # 1 desk, 2 desk grid, 3 plate, 4 plate light, 5 outline, 6 teal, 7 teal dark, 8 paper, 9 rule, 10 graph dot,
        # 11 plate shade, 12 bevel, 13 pad shadow, 14 bar
        for i, c in enumerate([(214, 222, 228), (194, 204, 214), SLATE_MID, SLATE_2, SLATE_OUT, TEAL, TEAL_DK, PAPER,
                               (200, 210, 218), (226, 230, 236), SLATE_DK, SLATE_LIGHT, (176, 188, 198), (40, 50, 64)],
                              start=1):
            r0[i] = c
        band = {1: (48, 60, 76), 2: TEAL, 3: SLATE_OUT, 4: PAPER, 5: SLATE_MID, 6: SLATE_LIGHT, 7: (72, 86, 104),
                8: TEAL_DK}
    elif direction == "B":
        for i, c in enumerate([(70, 60, 54), (86, 74, 66), BRASS, BRASS_LT, INKB, (168, 56, 48), BRASS_DK, CREAM,
                               (176, 188, 204), (236, 228, 208), (150, 112, 52), (240, 220, 160), (54, 46, 42),
                               (32, 28, 26)], start=1):
            r0[i] = c
        band = {1: (44, 38, 36), 2: BRASS, 3: INKB, 4: CREAM, 5: BRASS_DK, 6: BRASS_LT, 7: (64, 56, 52), 8: BRASS_DK}
    else:
        for i, c in enumerate([SCREEN, (30, 48, 52), (36, 56, 60), PHOS_DIM, (8, 14, 16), PHOS, PHOS_SH,
                               (232, 244, 236), (176, 216, 196), (212, 232, 220), (24, 40, 44), (120, 180, 156),
                               (12, 22, 24), (12, 20, 22)], start=1):
            r0[i] = c
        band = {1: (16, 28, 30), 2: PHOS, 3: (8, 14, 16), 4: (232, 244, 236), 5: PHOS_DIM, 6: (120, 180, 156),
                7: (28, 44, 48), 8: PHOS_SH}
    for k, c in band.items():
        r1[k] = c
    r2 = list(r1)
    for k in (1, 2, 3, 7, 8):                       # the band dims; the icon box (4-6) stays as it is
        r2[k] = tuple(int(v * 0.62) for v in r1[k])
    return [r0, r1, r2]


def bag_target(direction):
    """The 240x160 the bag should show, in row 0's slots for y < 112 and the band's (row 1) below."""
    g = canvas(240, 160, 1)
    # --- the desk (cols 0-9, rows 4-13: tile 0x11 everywhere, so an 8px-periodic pattern)
    for y in range(32, 112):
        for x in range(0, 80):
            if direction == "A":
                g[y][x] = 2 if (x % 8 == 7 or y % 8 == 7) else 1
            elif direction == "B":
                g[y][x] = 2 if (x + y) % 8 == 0 else 1
            else:
                g[y][x] = 4 if (x % 8 == 7 and y % 8 == 7) else (2 if (x % 8 == 7 or y % 8 == 7) and (x + y) % 2 else 1)
    # --- the pad under the bag (rows 10-12, cols 1-8; mirrored about x 39.5): a flat 45-degree octagon
    for y in range(80, 104):
        for x in range(8, 72):
            dx = min(x - 12, 67 - x)
            dy = min(y - 85, 98 - y)
            if dx >= 0 and dy >= 0 and dx + dy >= 6:
                g[y][x] = 13 if direction != "B" or (x + y) % 2 == 0 else 14
    # --- the title plate (cols 0-9, rows 0-3): its bar (cols 1-9, rows 1-2) dark for the WHITE pocket name
    rings = {"A": [5, 4, 3, 3, 3, 3, 3, 3], "B": [5, 4, 3, 3, 3, 3, 3, 3], "C": [5, 4, 3, 3, 3, 3, 3, 3]}[direction]
    for y in range(0, 32):
        for x in range(0, 80):
            d = min(x, y, x + y - 3, 31 - y)
            if d < 0:
                g[y][x] = 0
            else:
                g[y][x] = rings[min(d, 7)]
    fill(g, 8, 8, 80, 24, 14)
    for x in range(8, 80):
        g[24][x] = 11 if direction != "C" else 6
    for y in range(8, 24):                               # the bar's bottom corners at 45 degrees (tiles 0x0a)
        pass
    for k in range(3):
        g[23 - k][8 + (2 - k)] = 3 if k else 3
        g[23 - k][79 - (2 - k)] = 3
    if direction == "A":
        for k in range(5):                                # the teal bracket at the plate's top-left
            g[2][2 + k] = 6
            g[2 + k][2] = 6
    elif direction == "B":
        for x in range(4, 76, 4):                         # a gilt dotted rule under the bar
            g[27][x] = 4
    else:
        for x in range(2, 78):
            g[2][x] = 6 if x % 4 else 5
    # --- the list panel (cols 10-29, rows 0-13): frame 8px, paper cols 11-28 rows 1-12
    for y in range(0, 112):
        for x in range(80, 240):
            xx, yy = min(x - 80, 239 - x), min(y, 111 - y)
            d = min(xx, yy, xx + yy - 3)
            if d < 0:
                g[y][x] = 1 if y >= 32 or x >= 88 else g[y][x]
                continue
            if d >= 8:
                g[y][x] = 8
                continue
            if direction == "A":
                g[y][x] = [5, 4, 3, 3, 3, 3, 12, 5][d]
            elif direction == "B":
                g[y][x] = [5, 4, 3, 11, 3, 3, 4, 5][d]
            else:
                g[y][x] = [5, 6, 5, 5, 5, 5, 6, 5][d]
    # its corners: the bracket (A), rivets (B), LEDs (C) -- only on the four corner tiles, which are each used once
    for (cx, cy, sx, sy) in ((80, 0, 1, 1), (239, 111, -1, -1)):
        if direction == "A":
            for k in range(2, 7):
                put(g, cx + sx * k, cy + sy * 2, 6)
                put(g, cx + sx * 2, cy + sy * k, 6)
        elif direction == "B":
            put(g, cx + sx * 4, cy + sy * 4, 4)
            put(g, cx + sx * 5, cy + sy * 4, 4)
            put(g, cx + sx * 4, cy + sy * 5, 4)
        else:
            put(g, cx + sx * 4, cy + sy * 4, 12)
    # the paper: plain at row 1 and cols 11 / 28 (tile 0x09 is all three), the rule under each item (tile 0x0c's
    # bottom row: y 23, 39 ... 87), graph dots on the others (tile 0x10)
    for y in range(16, 96):
        for x in range(96, 224):
            r, ry = (y // 8), y % 8
            if r % 2 == 0 and ry == 7:
                g[y][x] = 9 if direction != "B" or x % 4 < 3 else 8
            elif r % 2 == 1 and ry == 7 and x % 8 == 7 and direction != "B":
                g[y][x] = 10 if direction == "A" else 9
    for x in range(88, 232):                              # row 12 (tiles 0x1d 0x1e 0x33): the paper's foot
        g[103][x] = 12 if direction != "C" else 9
    # --- row 14 (tile 0x21) and the band, rows 15-19 (palette row 1)
    for y in range(112, 160):
        for x in range(240):
            g[y][x] = 1
    for x in range(240):
        g[112][x] = 3
        g[113][x] = 2 if direction != "B" or x % 2 == 0 else 1
        g[114][x] = 7
        g[159][x] = 3
        g[158][x] = 7
    # the icon box (cols 0-4, rows 15-18 = x 0-39, y 120-151): light, a 45-degree cut, the item's icon sits in it
    for y in range(120, 152):
        for x in range(0, 40):
            xx, yy = min(x, 39 - x), min(y - 120, 151 - y)
            d = min(xx, yy, xx + yy - 3)
            if d < 0:
                continue
            g[y][x] = [3, 5, 6][d] if d < 3 else 4
    if direction == "A":
        for k in range(3, 8):
            g[123][k] = 8
            g[120 + k][3] = 8
    return g


def bag_build(direction):
    sheet, per, ents, ents_pc, pal = bag_shape()
    sheet = [[v & 15 for v in r] for r in sheet]
    if direction is None:
        return sheet, per, ents, ents_pc, bag_rows(None), 0
    tgt = bag_target(direction)
    sheet = [r[:] for r in sheet]
    miss, n = retile(sheet, per, [(ents[:32 * 20], 32, tgt_cols(tgt))], skip0=False)
    return sheet, per, ents, ents_pc, bag_rows(direction), miss


def tgt_cols(t):
    """The tilemap is 32 wide; the screen 30: two columns more, never seen, voted on by nobody."""
    return [r + [0] * 16 for r in t]


def bag_render(direction, which="bag", dim=False):
    sheet, per, ents, ents_pc, rows, miss = bag_build(direction)
    e = ents if which == "bag" else ents_pc

    def pal_of(entry):
        i = pal_of.i
        pal_of.i += 1
        r = (i // 32)
        return (2 if dim else 1) if r >= 14 else entry[3]
    pal_of.i = 0
    im = render_map(sheet, per, e[:32 * 20], 32, 20, rows, pal_of=pal_of)
    out = Image.new("RGB", (240, 160), q5(rows[0][0]))
    out.paste(im.crop((0, 0, 240, 160)), (0, 0), im.crop((0, 0, 240, 160)))
    return out


def bag_files(direction):
    sheet, per, ents, ents_pc, rows, miss = bag_build(direction)
    w, h, pal, raw = png(BAG + "/bg.png")
    flat = [c for r in rows for c in r][:len(pal)]
    return {BAG + "/bg.png": ("png", sheet, [q5(c) for c in flat], 8 if len(pal) > 16 else 4),
            BAG + "/bg_female.pal": ("pal", rows[0])}


# ================================================================================================ ARROWS
IF = "interface"


def arrows_pal(direction):
    p = jpal(IF + "/red_arrow.pal")
    if direction is None:
        return p
    p = list(p)
    p[1], p[2], p[3] = {"A": (TEAL, (20, 26, 36), (56, 68, 84)),
                        "B": (SLATE_MID, SLATE_OUT, (200, 212, 222)),
                        "C": (AMBER, (72, 44, 16), (255, 236, 176))}[direction]
    return p


def ring8(g, body, edge):
    """Every clear pixel touching `body` (eight ways) becomes `edge`."""
    h, w = len(g), len(g[0])
    out = [r[:] for r in g]
    for y in range(h):
        for x in range(w):
            if g[y][x] == 0 and any(0 <= y + dy < h and 0 <= x + dx < w and g[y + dy][x + dx] == body
                                    for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                out[y][x] = edge
    return out


def chevron(direction, kind):
    """One 16x16 frame pointing LEFT (kind 'left') or UP ('up'), its centre where vanilla's is (7.5, 7.5)."""
    g = canvas(16, 16)
    if direction == "A":                          # a 45-degree chevron two pixels thick, ringed in near-black
        for k in range(5):
            for t in range(2):
                put(g, 5 + k + t, 7 - k, 1)
                put(g, 5 + k + t, 8 + k, 1)
        g = ring8(g, 1, 2)
    elif direction == "B":                        # a solid wedge, a light face on its upper half
        for y in range(3, 13):
            half = 5 - abs(y - 7.5) // 1
            for x in range(int(10 - (5 - abs(y - 7.5))), 11):
                put(g, x, y, 3 if y < 8 and x > 5 + (abs(y - 7.5)) else 1)
        for y in range(3, 13):
            for x in range(16):
                if g[y][x]:
                    break
        g = ring8([[v if v else 0 for v in r] for r in g], 1, 2)
        g = [[(2 if v == 2 else v) for v in r] for r in g]
    else:                                         # two open carets, amber, a dark tick of shadow below each
        for off in (0, 5):
            for k in range(4):
                put(g, 4 + off + k, 7 - k, 1)
                put(g, 4 + off + k, 8 + k, 1)
                put(g, 4 + off + k, 9 + k, 2)
        put(g, 4, 7, 3)
        put(g, 4, 8, 3)
    if kind == "up":                              # the same drawing turned: left -> up (x, y) -> (y, x)
        g = [[g[x][y] for x in range(16)] for y in range(16)]
    return g


def right_cursor(direction):
    """red_arrow.png 16x16: the cursor pointing right (vanilla's x 0-14, y 0-11)."""
    g = canvas(16, 16)
    left = chevron(direction, "left")
    for y in range(16):
        for x in range(16):
            g[y][x] = left[y][15 - x]
    sh = [r[:] for r in g]                        # moved up 2 so it sits where vanilla's does (y 0-11)
    return [sh[y + 2] if y + 2 < 16 else [0] * 16 for y in range(16)]


def outline_art(direction):
    """selector_outline.png 24x24: a 16x24 box (x 0-15) and the right column's straight pieces, slot 1 (A/C) or 2."""
    w, h, pal, now = png(IF + "/selector_outline.png")
    if direction is None:
        return [[v & 15 for v in r] for r in now]
    g = canvas(24, 24)
    v = {"A": 1, "B": 2, "C": 1}[direction]
    for y in range(24):
        for x in range(16):
            xx, yy = min(x, 15 - x), min(y, 23 - y)
            d = min(xx, yy, xx + yy - 2)
            if d == 0:
                if direction == "C" and (x + y) % 3 == 2:
                    continue
                g[y][x] = v
    for x in range(16, 24):                       # the right column's pieces, where vanilla has them (y 0 and y 15)
        g[0][x] = v
        g[15][x] = v
    if direction == "A":
        for k in range(1, 4):                     # a teal bracket's inner dark tick at two corners
            g[1 + k][1] = 2
            g[1][1 + k] = 2
    return g


def arrow_files(direction):
    p = [q5(c) for c in arrows_pal(direction)]
    if direction is None:
        return {}
    other = canvas(16, 32)
    for y, r in enumerate(chevron(direction, "left")):
        other[y] = r
    for y, r in enumerate(chevron(direction, "up")):
        other[16 + y] = r
    return {IF + "/red_arrow_other.png": ("png", other, p, 4), IF + "/red_arrow.png": ("png", right_cursor(direction), p, 4),
            IF + "/selector_outline.png": ("png", outline_art(direction), p, 4), IF + "/red_arrow.pal": ("pal", arrows_pal(direction))}


def arrow_grids(direction):
    if direction is None:
        o = [[v & 15 for v in r] for r in png(IF + "/red_arrow_other.png")[3]]
        return o[:16], o[16:], [[v & 15 for v in r] for r in png(IF + "/red_arrow.png")[3]], outline_art(None)
    return chevron(direction, "left"), chevron(direction, "up"), right_cursor(direction), outline_art(direction)


# ================================================================================================ SELECT
def select_pal(direction):
    p = list(jpal(BAG + "/bag_window_pal.pal"))
    if direction:
        p[13], p[14], p[15] = {"A": (SLATE_MID, PAPER, SLATE_OUT), "B": (TEAL, SLATE_OUT, TEAL_DK),
                               "C": ((236, 240, 244), SLATE_OUT, SLATE_MID)}[direction]
    return p


def select_art(direction):
    if direction is None:
        return [[v & 15 for v in r] for r in png(IF + "/select_button.png")[3]]
    g = canvas(24, 16)
    if direction == "A":                          # a slate key: 45-degree corners, SEL in paper, one teal-less pip
        cut_box(g, 1, 2, 22, 11, 2, [15], 13)
        glyph3(g, 4, 5, "SEL", 14)
        put(g, 18, 6, 14), put(g, 19, 6, 14), put(g, 18, 7, 14), put(g, 19, 7, 14)
        for x in range(3, 21):
            put(g, x, 12, 15)
    elif direction == "B":                        # a tag pointing left at the item, its hole, SEL in dark
        for y in range(2, 13):
            for x in range(1, 23):
                d = min(x - 1 - abs(y - 7) + 4, 22 - x, y - 2, 12 - y)
                if x - 1 >= abs(y - 7.5) - 1 and d >= 0:
                    g[y][x] = 15 if (d == 0 or x - 1 < abs(y - 7.5)) else 13
        put(g, 5, 7, 0), put(g, 5, 8, 0)
        glyph3(g, 9, 5, "SEL", 14)
    else:                                         # no cap: SEL between two slate brackets, on the list's paper
        for y in range(3, 12):
            put(g, 1, y, 15), put(g, 22, y, 15)
        for k in range(1, 3):
            put(g, 1 + k, 3, 15), put(g, 1 + k, 11, 15), put(g, 22 - k, 3, 15), put(g, 22 - k, 11, 15)
        glyph3(g, 6, 5, "SEL", 14)
    return g


# ================================================================================================ SWAP LINE
def swap_pal(direction):
    p = list(png(IF + "/bag_swap.png")[2][:16])
    if direction:
        p[14], p[15] = {"A": (SLATE_MID, TEAL), "B": (SLATE_OUT, SLATE_LIGHT), "C": (AMBER_DK, AMBER)}[direction]
    return p


def swap_art(direction):
    if direction is None:
        return [[v & 15 for v in r] for r in png(IF + "/bag_swap.png")[3]]
    g = canvas(16, 32)
    for y0 in (0, 16):
        for x in range(16):
            for y in (6, 7):
                if direction == "C" and x % 4 == 3:
                    continue
                if y0 == 0 and x < 6:
                    continue
                g[y0 + y][x] = 14
    if direction == "A":                          # a teal caret pointing in, 45 degrees, two thick
        for k in range(4):
            for t in range(2):
                put(g, 2 + k + t, 3 + k, 15)
                put(g, 2 + k + t, 10 - k, 15)
    elif direction == "B":                        # the rule doubles at the head into a notch, light on the dark
        for y in range(3, 11):
            put(g, 2, y, 14)
        for k in range(3):
            put(g, 3 + k, 4 + k, 15), put(g, 3 + k, 9 - k, 15)
        for x in range(16):
            if g[6][x] == 14 and x >= 6:
                g[5][x] = 15 if x % 2 else 0
    else:
        for y in range(3, 11):
            for x in range(2, 2 + int(4 - abs(y - 6.5))):
                put(g, int(x), y, 15)
    return g


# ================================================================================================ FIELD ICONS
ICONS, ICONP = "items/icons", "items/icon_palettes"


def icon_now(stem):
    w, h, pal, px = png(ICONS + "/%s.png" % stem)
    return [[v & 15 for v in r] for r in px], jpal(ICONP + "/%s.pal" % stem)


def close_icon(direction):
    """CLOSE BAG's icon (return_to_field_arrow): 24x24, its own 16 colours."""
    if direction is None:
        return icon_now("return_to_field_arrow")
    g = canvas(24, 24)
    if direction == "A":     # a slate keycap, 45-degree corners, a teal RETURN arrow on it
        pal = [(0, 0, 0), SLATE_OUT, SLATE_MID, SLATE_2, SLATE_LIGHT, TEAL, TEAL_DK, PAPER] + [(0, 0, 0)] * 8
        cut_box(g, 2, 3, 20, 18, 3, [1, 4, 3], 2)
        for x in range(2, 22):
            put(g, x, 20, 1)
        for y in range(7, 13):
            put(g, 16, y, 5), put(g, 17, y, 5)
        for x in range(8, 18):
            put(g, x, 12, 5), put(g, x, 13, 5)
        for k in range(4):
            put(g, 8 + k, 12 - k, 5), put(g, 8 + k, 13 + k, 5)
        for x in range(9, 18):
            put(g, x, 14, 6) if g[14][x] == 2 else None
    elif direction == "B":   # an open door in a slate frame, a teal arrow leaving through it
        pal = [(0, 0, 0), SLATE_OUT, SLATE_MID, (232, 236, 240), (196, 206, 214), TEAL, TEAL_DK, PAPER] + [(0, 0, 0)] * 8
        fill(g, 4, 2, 15, 22, 1)
        fill(g, 5, 3, 14, 22, 3)
        for y in range(3, 22):                    # the door, swung open: a slanted leaf at the left
            for x in range(5, 8):
                put(g, x, y, 2 if x < 7 else 4)
        for x in range(9, 22):
            put(g, x, 12, 5), put(g, x, 13, 5)
        for k in range(4):
            put(g, 21 - k, 12 - k, 5), put(g, 21 - k, 13 + k, 5)
        for x in range(10, 21):
            put(g, x, 14, 6)
    else:                    # a paper slip, an ink arrow curling back
        pal = [(0, 0, 0), (40, 44, 52), (120, 128, 140), CREAM, (220, 212, 192), (40, 44, 52), (168, 56, 48),
               PAPER] + [(0, 0, 0)] * 8
        cut_box(g, 3, 4, 18, 16, 0, [2], 3)
        for x in range(4, 20):
            put(g, x, 19, 4)
        for y in range(8, 14):
            put(g, 16, y, 1)
        for x in range(8, 17):
            put(g, x, 13, 1)
        for k in range(3):
            put(g, 8 + k, 13 - k, 1), put(g, 8 + k, 13 + k, 1)
        put(g, 15, 8, 6), put(g, 16, 7, 6)
    return g, pal


def qmark_icon(direction):
    """question_mark.png: an item without a picture."""
    if direction is None:
        return icon_now("question_mark")
    g = canvas(24, 24)
    Q = [".XXXX.", "XX..XX", "....XX", "...XX.", "..XX..", "..XX..", "......", "..XX..", "..XX.."]
    if direction == "A":     # a slate card, a teal ? on it
        pal = [(0, 0, 0), SLATE_OUT, SLATE_MID, SLATE_2, SLATE_LIGHT, TEAL, TEAL_DK, PAPER] + [(0, 0, 0)] * 8
        cut_box(g, 4, 2, 16, 20, 3, [1, 3], 2)
        ink, sh = 5, 6
    elif direction == "B":   # a dashed outline waiting for a picture, a slate ?
        pal = [(0, 0, 0), SLATE_OUT, SLATE_MID, (232, 236, 240), SLATE_LIGHT, SLATE_OUT, SLATE_LIGHT, PAPER] + [(0, 0, 0)] * 8
        for y in range(2, 22):
            for x in range(4, 20):
                edge = x in (4, 19) or y in (2, 21)
                if edge and (x + y) % 3 != 0:
                    g[y][x] = 2
        ink, sh = 5, 4
    else:                    # a paper slip, an ink ?, a red stamp's corner
        pal = [(0, 0, 0), (40, 44, 52), (120, 128, 140), CREAM, (220, 212, 192), (40, 44, 52), (200, 196, 184),
               (168, 56, 48)] + [(0, 0, 0)] * 8
        cut_box(g, 4, 3, 16, 18, 0, [2], 3)
        put(g, 18, 4, 7), put(g, 17, 4, 7), put(g, 18, 5, 7)
        ink, sh = 5, 6
    for y, r in enumerate(Q):
        for x, c in enumerate(r):
            if c == "X":
                put(g, 9 + x, 7 + y, ink)
                if g[8 + y][9 + x] in (0, 2, 3, 4) and direction != "B" and y + 1 < len(Q) and Q[y + 1][x] != "X":
                    put(g, 9 + x, 8 + y, sh)
    return g, pal


# ================================================================================================ KEYPAD GLYPHS
KEYS = [  # (name, x, y, width, label) -- sKeypadIcons: tileOffset*8 within a 16-tile-wide sheet, 12 rows tall
    ("A", 0, 0, 8, "A"), ("B", 8, 0, 8, "B"), ("L", 16, 0, 16, "L"), ("R", 32, 0, 16, "R"),
    ("START", 48, 0, 24, "START"), ("SELECT", 72, 0, 24, "SELECT"),
    ("UP", 96, 0, 8, None), ("DOWN", 104, 0, 8, None), ("LEFT", 112, 0, 8, None), ("RIGHT", 120, 0, 8, None),
    ("UPDOWN", 0, 16, 8, None), ("LEFTRIGHT", 8, 16, 8, None), ("NONE", 16, 16, 8, None)]


def keypad_art(direction):
    w, h, pal, now = png("fonts/keypad_icons.png")
    if direction is None:
        return [[v & 15 for v in r] for r in now]
    g = canvas(128, 32)
    for name, x0, y0, w, label in KEYS:
        y4 = y0 + 4                               # ink on rows 4-11 of the cell, as today
        if label:
            if direction == "A":                  # a cap with 45-degree corners: face 1, outline 2, a foot of 3
                cut_box(g, x0, y4, w, 7, 1, [2], 1)
                for x in range(x0 + 1, x0 + w - 1):
                    put(g, x, y4 + 7, 3)
                ink = 2
            elif direction == "B":                # filled dark, letters in the face colour
                cut_box(g, x0, y4, w, 8, 1, [2], 2)
                ink = 1
            else:                                 # a ticket: square face, a notch bitten from each end
                fill(g, x0, y4, x0 + w, y4 + 7, 1)
                for y in (y4 + 3,):
                    put(g, x0, y, 0), put(g, x0 + w - 1, y, 0)
                for x in range(x0, x0 + w):
                    put(g, x, y4 + 7, 2)
                for y in range(y4, y4 + 7):
                    if y != y4 + 3:
                        put(g, x0, y, 3)
                ink = 2
            f = F3N if label == "SELECT" else F3
            ww = wordw(label, f)
            glyph3(g, x0 + (w - ww) // 2, y4 + 1, label, ink, f)
        else:
            arms = {"UP": "U", "DOWN": "D", "LEFT": "L", "RIGHT": "R", "UPDOWN": "UD", "LEFTRIGHT": "LR", "NONE": ""}[name]
            cx, cy = x0 + 3, y4 + 3                 # a plus 7x7 in the cell's x 0-6, rows 4-10
            cells = {"C": [(0, 0)], "U": [(0, -1), (0, -2), (0, -3)], "D": [(0, 1), (0, 2), (0, 3)],
                     "L": [(-1, 0), (-2, 0), (-3, 0)], "R": [(1, 0), (2, 0), (3, 0)]}
            body = {"A": 1, "B": 1, "C": 3}[direction]
            for arm, pts in cells.items():
                for dx, dy in pts:
                    v = body                      # the pressed arm keeps the face: 4 is only its pip (below),
                    put(g, cx + dx, cy + dy, v)   # as today -- slot 4 is red in a light window, not in every one
                    if direction == "B":          # arms three wide
                        for o in (-1, 1):
                            if arm in "UD":
                                put(g, cx + dx + o, cy + dy, v)
                            elif arm in "LR":
                                put(g, cx + dx, cy + dy + o, v)
            if direction == "B":
                for o in (-1, 1):
                    for o2 in (-1, 1):
                        put(g, cx + o, cy + o2, body)
            for arm in arms:                      # the pressed arm's pip, one pixel, where vanilla put it
                dx, dy = cells[arm][1]
                put(g, cx + dx, cy + dy, 4)
            # the edge: 2 on every clear pixel right of or below the plus (the cap's shadow, as today)
            cell = [[g[y][x] for x in range(x0, x0 + 8)] for y in range(y4, y4 + 8)]
            for y in range(8):
                for x in range(8):
                    if cell[y][x] == 0 and ((x and cell[y][x - 1] not in (0, 2)) or (y and cell[y - 1][x] not in (0, 2))):
                        put(g, x0 + x, y4 + y, 2)
    return g


# ================================================================================================ MARKINGS
MISC = "misc"


def mark_shape(k, direction):
    """8x8 of one marking (0 circle, 1 square, 2 triangle, 3 heart): 1 the body, 2 its edge."""
    S = {
        "A": [["..XXXX..", ".XXXXXX.", "XXXXXXXX", "XXXXXXXX", "XXXXXXXX", ".XXXXXX.", "..XXXX..", "........"],
              ["XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "........"],
              ["...XX...", "...XX...", "..XXXX..", "..XXXX..", ".XXXXXX.", ".XXXXXX.", "XXXXXXXX", "........"],
              [".XX.XX..", "XXXXXXX.", "XXXXXXX.", "XXXXXXX.", ".XXXXX..", "..XXX...", "...X....", "........"]],
        "B": [["..XXXX..", ".X....X.", "X......X", "X......X", "X......X", ".X....X.", "..XXXX..", "........"],
              ["XXXXXXX.", "X.....X.", "X.....X.", "X.....X.", "X.....X.", "X.....X.", "XXXXXXX.", "........"],
              ["...XX...", "...XX...", "..X..X..", "..X..X..", ".X....X.", ".X....X.", "XXXXXXXX", "........"],
              [".XX.XX..", "X..X..X.", "X.....X.", "X.....X.", ".X...X..", "..X.X...", "...X....", "........"]],
        "C": [["...X....", "..XXX...", ".XX.XX..", "XX...XX.", ".XX.XX..", "..XXX...", "...X....", "........"],
              ["..XXX...", "..XXX...", "XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "..XXX...", "..XXX...", "........"],
              ["X.....X.", ".X...X..", "..X.X...", "...X....", "..X.X...", ".X...X..", "X.....X.", "........"],
              ["XXXXXXX.", "........", "XXXXXXX.", "........", "XXXXXXX.", "........", "........", "........"]],
    }[direction][k]
    g = canvas(8, 8)
    for y, r in enumerate(S):
        for x, c in enumerate(r):
            if c == "X":
                g[y][x] = 1
    if direction == "A":                         # a 1px edge (2) on the body's right and foot: the bevel
        for y in range(8):
            for x in range(8):
                if g[y][x] == 1 and (x == 7 or g[y][x + 1] == 0 or y == 7 or g[y + 1][x] == 0):
                    g[y][x] = 2
    return g


def markings_pals(direction):
    p1 = list(png(MISC + "/mon_markings.png")[2][:16])
    p2 = list(png(MISC + "/markings2.png")[2][:16])
    if direction is None:
        return p1, p2
    off, off_e, on, on_e = {"A": ((176, 188, 198), (150, 162, 174), TEAL, TEAL_DK),
                            "B": ((168, 176, 186), (168, 176, 186), SLATE_OUT, SLATE_OUT),
                            "C": ((150, 162, 174), (150, 162, 174), AMBER, AMBER_DK)}[direction]
    p1[1], p1[2], p1[3], p1[4] = off, off_e, on, on_e
    # markings2: 1 the window paper, 2 ink, 3 off body, 5 the ink's shadow, 6 off edge, 7 on edge; 4 the on body
    p2[1], p2[2], p2[3], p2[4], p2[5], p2[6], p2[7] = PAPER, SLATE_OUT, off, on, (200, 204, 208), off_e, on_e
    return p1, p2


def combo_art(direction):
    if direction is None:
        return [[v & 15 for v in r] for r in png(MISC + "/mon_markings.png")[3]]
    g = canvas(32, 128)
    for row in range(16):
        for k in range(4):
            on = bool(row >> k & 1)
            m = mark_shape(k, direction)
            for y in range(8):
                for x in range(8):
                    v = m[y][x]
                    if v:
                        g[row * 8 + y][k * 8 + x] = (3 if v == 1 else 4) if on else (1 if v == 1 else 2)
    return g


def okcancel_text(direction):
    """The 32x32 OK / CANCEL sprite (markings2 tiles 9-24): SCREEN's small face, ink 2, shadow 5, on the paper (1)."""
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    say(im, 16 - text_width("OK", True) // 2, 0, "OK", (2, 2, 2), (5, 5, 5), small=True)
    say(im, 16 - text_width("CANCEL", True) // 2, 16, "CANCEL", (2, 2, 2), (5, 5, 5), small=True)
    g = canvas(32, 32, 1)
    for y in range(32):
        for x in range(32):
            r = im.getpixel((x, y))
            if r[3]:
                g[y][x] = 2 if r[0] < 4 else 5
    return g


def markings2_art(direction):
    w, h, pal, now = png(MISC + "/markings2.png")
    now = [[v & 15 for v in r] for r in now]
    if direction is None:
        return now
    g = [r[:] for r in now]
    for k in range(4):                                       # frames 0-7: each mark off, then on, on the paper
        m = mark_shape(k, direction)
        for on in (0, 1):
            t = k * 2 + on
            x0, y0 = (t % 4) * 8, (t // 4) * 8
            for y in range(8):
                for x in range(8):
                    v = m[y][x]
                    g[y0 + y][x0 + x] = 1 if not v else ((4 if v == 1 else 7) if on else (3 if v == 1 else 6))
    cur = canvas(8, 8, 1)                                    # frame 8: the cursor, a chevron in ink with its shadow
    for k in range(4):
        put(cur, 1 + k, 1 + k, 2), put(cur, 1 + k, 7 - k, 2), put(cur, 2 + k, 1 + k, 2), put(cur, 2 + k, 7 - k, 2)
    cur = [[v if v != 1 else 1 for v in r] for r in cur]
    for y in range(8):
        for x in range(8):
            g[16 + y][x] = cur[y][x]
    txt = okcancel_text(direction)                           # tiles 9-24: the 32x32 laid in 1-D order from tile 9
    for t in range(16):
        tx, ty = t % 4, t // 4
        dst = 9 + t
        dx, dy = (dst % 4) * 8, (dst // 4) * 8
        for y in range(8):
            for x in range(8):
                g[dy + y][dx + x] = txt[ty * 8 + y][tx * 8 + x]
    return g


# ================================================================================================ PC PARTS
PS = "pokemon_storage"


def shadow_art(direction):
    """cursor_shadow.png 16x16 in misc2's 8 (the rim) and 15 (the body): both kept, shared with the PAW."""
    if direction is None:
        return [[v & 15 for v in r] for r in png(PS + "/cursor_shadow.png")[3]]
    g = canvas(16, 16)
    if direction == "A":                          # a flat slab, 45-degree ends, under the PAW
        for y in range(6, 11):
            for x in range(2, 14):
                d = min(x - 2, 13 - x) + min(y - 6, 10 - y)
                if d >= 2:
                    g[y][x] = 15 if 6 < y < 10 and 3 < x < 12 and d > 2 else 8
    elif direction == "B":                        # a diamond pointing at the box below
        for y in range(4, 13):
            r = 4 - abs(y - 8)
            for x in range(8 - r * 1 - 2, 8 + r + 2):
                if 0 <= x < 16:
                    g[y][x] = 8 if abs(x - 7.5) > r + 0.5 else 15
    else:                                         # a target's four corners and a centre dot
        for (cx, cy, sx, sy) in ((2, 5, 1, 1), (13, 5, -1, 1), (2, 11, 1, -1), (13, 11, -1, -1)):
            put(g, cx, cy, 8), put(g, cx + sx, cy, 8), put(g, cx + 2 * sx, cy, 8), put(g, cx, cy + sy, 8)
        for y in (7, 8, 9):
            for x in (7, 8):
                put(g, x, y, 15)
    return g


def info_frame_pal(direction):
    p = list(png(PS + "/item_info_frame.png")[2][:16])
    if direction:
        p[4], p[7], p[9], p[10], p[11] = {"A": (SLATE_DK, SLATE_LIGHT, SLATE_MID, TEAL, SLATE_OUT),
                                          "B": (BRASS_DK, CREAM, (220, 212, 192), (168, 56, 48), (120, 112, 100)),
                                          "C": (PHOS_SH, PHOS, PHOS_DIM, (232, 244, 236), SCREEN)}[direction]
    return p


def info_frame_art(direction):
    """item_info_frame.png 32x8: tile 0 the top edge (V-flipped for the bottom), 1 the right edge, 2 the top-right
    corner, 3 the bottom-right. The window's paper (1) is inside; 11 outline, 9 band, 7 bevel, 10 accent, 4 shade."""
    if direction is None:
        return [[v & 15 for v in r] for r in png(PS + "/item_info_frame.png")[3]]
    # draw a 16x16 corner piece (the window's top-right and bottom-right), then cut the four tiles from it
    big = canvas(16, 24, 1)
    rings = {"A": [11, 9, 9, 7], "B": [11, 9, 4, 7], "C": [11, 9, 11, 7]}[direction]
    for y in range(24):
        for x in range(16):
            xx, yy = 15 - x, min(y, 23 - y)
            d = min(xx, yy, xx + yy - 2)
            if d < 0:
                big[y][x] = 0
            elif d < 4:
                big[y][x] = rings[d]
    if direction == "A":
        for k in range(3, 7):
            big[2][15 - k] = 10
            big[k][13] = 10
    elif direction == "B":
        for x in range(0, 12, 3):
            big[2][x] = 10 if x % 6 == 0 else big[2][x]
    else:
        big[2][12] = 10
    g = canvas(32, 8)
    for y in range(8):
        for x in range(8):
            g[y][x] = big[y][x]                   # tile 0: the top edge (the corner's left part)
            g[y][8 + x] = big[8 + y][8 + x]       # tile 1: the right edge
            g[y][16 + x] = big[y][8 + x]          # tile 2: top-right corner
            g[y][24 + x] = big[16 + y][8 + x]     # tile 3: bottom-right corner
    return g


# ================================================================================================ outputs
def _png(px, palette, bd=4):
    return ("png", px, [q5(c) for c in palette], bd)


def outputs(piece, direction):
    out = {}
    if piece == "bag":
        out.update(bag_files(direction))
    elif piece == "arrows":
        out.update(arrow_files(direction))
    elif piece == "select":
        p = select_pal(direction)
        out[IF + "/select_button.png"] = _png(select_art(direction), p)
        out[BAG + "/bag_window_pal.pal"] = ("pal", p)
    elif piece == "swap":
        out[IF + "/bag_swap.png"] = _png(swap_art(direction), swap_pal(direction))
    elif piece == "fieldicons":
        for stem, fn in (("return_to_field_arrow", close_icon), ("question_mark", qmark_icon)):
            g, p = fn(direction)
            out[ICONS + "/%s.png" % stem] = _png(g, p)
            out[ICONP + "/%s.pal" % stem] = ("pal", p)
    elif piece == "keypad":
        w, h, pal, now = png("fonts/keypad_icons.png")
        out["fonts/keypad_icons.png"] = _png(keypad_art(direction), pal[:16])
    elif piece == "markings":
        p1, p2 = markings_pals(direction)
        out[MISC + "/mon_markings.png"] = _png(combo_art(direction), p1)
        out[MISC + "/markings2.png"] = _png(markings2_art(direction), p2)
    elif piece == "pcparts":
        w, h, pal, now = png(PS + "/cursor_shadow.png")
        out[PS + "/cursor_shadow.png"] = _png(shadow_art(direction), pal[:16])
        out[PS + "/item_info_frame.png"] = _png(info_frame_art(direction), info_frame_pal(direction))
    return out


def check(piece, direction):
    """The drop-in's contract, asserted: sizes, slots, the 12-row keypad cells, the shared slots unused or kept."""
    errs = []
    files = outputs(piece, direction)
    for rel, payload in files.items():
        if payload[0] != "png":
            continue
        px = payload[1]
        w, h, pal, now = png(rel)
        if (len(px[0]), len(px)) != (w, h):
            errs.append("%s: %dx%d, the engine's is %dx%d" % (rel, len(px[0]), len(px), w, h))
    if piece == "select":
        used = {v for r in select_art(direction) for v in r}
        if used - {0, 13, 14, 15}:
            errs.append("select: draws outside 13-15: %r" % sorted(used - {0, 13, 14, 15}))
    if piece == "pcparts":
        used = {v for r in shadow_art(direction) for v in r}
        if used - {0, 8, 15}:
            errs.append("cursor_shadow: draws outside misc2's 8/15: %r" % sorted(used))
        used = {v for r in info_frame_art(direction) for v in r}
        if used - {0, 1, 4, 7, 9, 10, 11}:
            errs.append("item_info_frame: draws a text slot: %r" % sorted(used))
    if piece == "keypad":
        g = keypad_art(direction)
        used = {v for r in g for v in r}
        if used - {0, 1, 2, 3, 4}:
            errs.append("keypad: draws outside the text slots 1-4: %r" % sorted(used))
        for name, x0, y0, w, label in KEYS:
            for y in range(y0, y0 + 16):
                for x in range(x0, x0 + w):
                    if g[y][x] and not (y0 + 4 <= y < y0 + 12):
                        errs.append("keypad %s: ink outside rows 4-11" % name)
                        break
    if piece == "arrows":
        for g in arrow_grids(direction):
            used = {v for r in g for v in r}
            if used - {0, 1, 2, 3}:
                errs.append("arrows: a slot outside 1-3: %r" % sorted(used))
    return errs


# ================================================================================================ the real screens
def load_shots(d):
    """The theatre's today shots by caption keyword (tools/routes/t554_menus_today.json)."""
    shots = {}
    if not d or not os.path.isdir(d):
        return shots
    for root, _, files in os.walk(d):
        for f in sorted(files):
            if f.endswith(".png") and not f.startswith("sheet") and "contact" not in f:
                shots[f] = Image.open(os.path.join(root, f)).convert("RGB")
    return shots


def shot(shots, *keys):
    for name, im in shots.items():
        if all(k.lower() in name.lower() for k in keys) and im.size == (240, 160):
            return im
    return None


def bag_composite(today, direction, base=None):
    """The bag's shot with its background swapped: wherever the shot shows today's background, the draft's."""
    now, nowd = bag_render(None), bag_render(None, dim=True)
    new, newd = bag_render(direction), bag_render(direction, dim=True)
    a, b, bd, c, cd = today.load(), now.load(), nowd.load(), new.load(), newd.load()
    out = today.copy()
    o = out.load()
    for y in range(160):
        for x in range(240):
            if a[x, y] == mgba(b[x, y]) or a[x, y] == b[x, y]:
                o[x, y] = c[x, y]
            elif y >= 112 and (a[x, y] == mgba(bd[x, y]) or a[x, y] == bd[x, y]):
                o[x, y] = cd[x, y]                      # the band dimmed (row 2) while a menu is up
    return out


def find_sprite(img, grid, pal, step=1):
    """Every place `grid` (index 0 clear) sits in `img` exactly, in its palette (mGBA's colours)."""
    pts = [(x, y, mgba(q5(pal[v]))) for y, r in enumerate(grid) for x, v in enumerate(r) if v]
    if not pts:
        return []
    W, H = img.size
    p = img.load()
    gw, gh = len(grid[0]), len(grid)
    hits = []
    for y in range(-gh + 1, H):
        for x in range(-gw + 1, W):
            ok, seen = 0, 0
            for (dx, dy, c) in pts:
                X, Y = x + dx, y + dy
                if not (0 <= X < W and 0 <= Y < H):
                    continue
                seen += 1
                if p[X, Y] != c:
                    ok = -1
                    break
                ok += 1
            if ok >= 6 and ok > seen * 0.9 and seen > len(pts) * 0.4:
                hits.append((x, y))
    return hits


def swap_sprite(img, old, new, pal_old, pal_new, under=None):
    """Find `old` in the shot and put `new` there: old's pixels become what lies under them (the bag's draft
    background, or the colour most common round the sprite), then new is drawn."""
    out = img.copy()
    o = out.load()
    hits = find_sprite(img, old, pal_old)
    for (x, y) in hits:
        gw, gh = len(old[0]), len(old)
        ring = [img.getpixel((X, Y)) for X in range(max(0, x - 1), min(240, x + gw + 1))
                for Y in (max(0, y - 1), min(159, y + gh)) if 0 <= X < 240]
        bgc = max(set(ring), key=ring.count) if ring else (0, 0, 0)
        for dy, r in enumerate(old):
            for dx, v in enumerate(r):
                X, Y = x + dx, y + dy
                if v and 0 <= X < 240 and 0 <= Y < 160:
                    o[X, Y] = under.getpixel((X, Y)) if under else bgc
        for dy, r in enumerate(new):
            for dx, v in enumerate(r):
                X, Y = x + dx, y + dy
                if v and 0 <= X < 240 and 0 <= Y < 160:
                    o[X, Y] = q5(pal_new[v])
    return out, hits


def std_composite(img, direction):
    """A theatre shot with every std-frame tile on the 8px grid swapped for the draft's (gbaframes' std versions)."""
    import gbaframes as F
    now, p3 = F.std_now()
    if direction is None:
        return img.copy(), 0
    g, p_new, said = F.std_versions()[direction]
    out = img.copy()
    o = out.load()
    p = img.load()
    n = 0
    for ty in range(20):
        for tx in range(30):
            for t in (0, 1, 2, 3, 5, 6, 7, 8):
                sx, sy = (t % 3) * 8, (t // 3) * 8
                ok = True
                for y in range(8):
                    for x in range(8):
                        v = now[sy + y][sx + x]
                        if v and p[tx * 8 + x, ty * 8 + y] != mgba(q5(p3[v])):
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    continue
                n += 1
                for y in range(8):
                    for x in range(8):
                        v, w_ = g[sy + y][sx + x], now[sy + y][sx + x]
                        X, Y = tx * 8 + x, ty * 8 + y
                        if v:
                            o[X, Y] = q5(p_new[v])
                        elif w_:                            # was drawn, now clear: what lies outward of it
                            ox = X - 3 if t in (0, 3, 6) else X + 3 if t in (2, 5, 8) else X
                            oy = Y - 3 if t in (0, 1, 2) else Y + 3 if t in (6, 7, 8) else Y
                            o[X, Y] = p[min(239, max(0, ox)), min(159, max(0, oy))]
                break
    return out, n


def keypad_composite(img, direction):
    """The INDEX footer's keypad glyphs swapped: found by their SHAPE (each index one colour, 1 and 2 different), and
    the draft drawn in the colours the shot gives those indices."""
    out = img.copy()
    if direction is None:
        return out, 0
    now = keypad_art(None)
    new = keypad_art(direction)
    p = img.load()
    o = out.load()
    found = 0
    for name, x0, y0, w, label in KEYS:
        cell = [r[x0:x0 + w] for r in now[y0:y0 + 12]]
        ncell = [r[x0:x0 + w] for r in new[y0:y0 + 12]]
        pts = [(x, y, v) for y, r in enumerate(cell) for x, v in enumerate(r) if v]
        if len(pts) < 10:
            continue
        for Y0 in range(0, 160 - 12):
            for X0 in range(0, 240 - w):
                cmap, ok = {}, True
                for x, y, v in pts:
                    c = p[X0 + x, Y0 + y]
                    if cmap.setdefault(v, c) != c:
                        ok = False
                        break
                if not ok or len(set(cmap.values())) != len(cmap) or (1 in cmap and 2 in cmap and cmap[1] == cmap[2]):
                    continue
                ring = [p[X0 + x, Y0 + y] for y, r in enumerate(cell) for x, v in enumerate(r) if not v]
                bgc = max(set(ring), key=ring.count) if ring else cmap.get(1)
                cm = dict(cmap)
                cm.setdefault(3, cm.get(2))
                cm.setdefault(4, (230, 8, 8))
                cm.setdefault(1, bgc)
                for y in range(12):
                    for x in range(w):
                        v = ncell[y][x]
                        o[X0 + x, Y0 + y] = cm.get(v, bgc) if v else bgc
                found += 1
    return out, found


def zoom(img, k, bg=(36, 40, 46)):
    im = Image.new("RGB", (240, 160), bg)
    z = img.resize((img.width * k, img.height * k), Image.NEAREST)
    im.paste(z, ((240 - z.width) // 2, (160 - z.height) // 2), z if z.mode == "RGBA" else None)
    return im


def parts_plate(items, k=4, bg=(36, 40, 46)):
    """Small pieces side by side at k x on a 240x160 plate."""
    im = Image.new("RGB", (240, 160), bg)
    x = 8
    for it in items:
        z = it.resize((it.width * k, it.height * k), Image.NEAREST)
        if x + z.width > 236:
            break
        im.paste(z, (x, (160 - z.height) // 2), z if z.mode == "RGBA" else None)
        x += z.width + 8
    return im


# ------------------------------------------------------------------------------------------------ mocks per piece
def bag_shot_or_render(shots, *keys):
    s = shot(shots, *keys)
    return s if s is not None else bag_render(None)


def mock_bag(shots, d):
    s1 = shot(shots, "the bag", "first")
    s2 = shot(shots, "item's menu")
    out = []
    for s, dim in ((s1, False), (s2, True)):
        if s is None:
            out.append(bag_render(d, dim=dim))
        else:
            out.append(s if d is None else bag_composite(s, d))
    out.append(bag_render(d, which="pc"))
    return out


def mock_arrows(shots, d):
    lo, up, cur, sel = arrow_grids(None)
    p0 = arrows_pal(None)
    res = []
    s = shot(shots, "scrolled") or shot(shots, "the bag", "first")
    m = shot(shots, "VIRIDIAN MART", "BUY")
    for img in (s, m):
        if img is None:
            res.append(Image.new("RGB", (240, 160), (36, 40, 46)))
            continue
        if d is None:
            res.append(img)
            continue
        nlo, nup, ncur, nsel = arrow_grids(d)
        p1 = arrows_pal(d)
        under = bag_render(d) if img is s else None
        base = bag_composite(img, d) if img is s and False else img
        flips = [(lo, nlo), ([r[::-1] for r in lo], [r[::-1] for r in nlo]), (up, nup), (up[::-1], nup[::-1])]
        for old, new in flips:
            base, hits = swap_sprite(base, old, new, p0, p1, under=None)
        res.append(base)
    g = [arrow_grids(d)[i] for i in range(4)]
    p = arrows_pal(d)
    res.append(parts_plate([idx_rgba(g[0], p), idx_rgba([r[::-1] for r in g[0]], p), idx_rgba(g[1], p),
                            idx_rgba(g[1][::-1], p), idx_rgba(g[2], p), idx_rgba(g[3], p)], k=2, bg=(232, 236, 240)))
    return res


def mock_select(shots, d):
    """SELECT beside a registered item: blitted into the bag's list window (tilemap 11,1) at x 0x70."""
    s = shot(shots, "the bag", "first")
    base = s.copy() if s is not None else bag_render(None)
    if d is not None and s is not None:
        base = bag_composite(s, "A")             # shown on the A desk so the button reads in its likely home
    p = select_pal(d)
    g = select_art(d)
    a = idx_rgba(g, p)
    for im_ in (base,) + ((s,) if s is not None else ()):
        pass
    if s is not None:                            # a registered (key) item has no count: clear it where SELECT goes
        paper = s.getpixel((88 + 0x70 - 4, 8 + 16 + 4))
        s = s.copy()
        ImageDraw.Draw(s).rectangle([88 + 0x68, 8 + 16 + 1, 88 + 0x8f, 8 + 16 + 14], fill=paper)
        if d is not None:
            base = bag_composite(s, "A")
    base.paste(a, (88 + 0x70, 8 + 16 * 1 + 1), a)
    if s is not None and d is not None:
        base2 = s.copy()
        base2.paste(a, (88 + 0x70, 8 + 16 * 1 + 1), a)
    else:
        base2 = base
    return [base2, base, parts_plate([idx_rgba(g, p)], k=6, bg=(248, 248, 244))]


def mock_swap(shots, d):
    s = shot(shots, "swap line")
    if s is None:
        return [Image.new("RGB", (240, 160)), parts_plate([idx_rgba(swap_art(d), swap_pal(d))], k=4)]
    if d is None:
        res = [s]
    else:
        old, new = swap_art(None), swap_art(d)
        img, hits = swap_sprite(s, old[:16], new[:16], swap_pal(None), swap_pal(d))
        img, hits3 = swap_sprite(img, [r[::-1] for r in old[:16]], [r[::-1] for r in new[:16]], swap_pal(None),
                                 swap_pal(d))                    # the far end: the head, H-flipped by the code
        img, hits2 = swap_sprite(img, old[16:], new[16:], swap_pal(None), swap_pal(d))
        res = [img]
    res.append(parts_plate([idx_rgba(swap_art(d), swap_pal(d))], k=4, bg=(248, 248, 244)))
    return res


def mock_fieldicons(shots, d):
    s = shot(shots, "CLOSE BAG")
    g0, p0 = close_icon(None)
    g1, p1 = close_icon(d)
    q0, qp0 = qmark_icon(None)
    q1, qp1 = qmark_icon(d)
    res = []
    if s is not None:
        img, hits = swap_sprite(s, g0, g1, p0, p1) if d is not None else (s, [])
        res.append(img)
        # the ? in the same place: the icon box (the CLOSE BAG icon's spot)
        hits = find_sprite(s, g0, p0)
        img2 = img.copy()
        if hits:
            x, y = hits[0]
            for dy, r in enumerate(g1 if d is not None else g0):
                for dx, v in enumerate(r):
                    if v:
                        img2.putpixel((x + dx, y + dy), img.getpixel((min(239, x + 30), y + dy)) if False else
                                      img.getpixel((max(0, x - 1), y + 12)))
            q = idx_rgba(q1, qp1)
            img2.paste(q, (x, y), q)
        res.append(img2)
    res.append(parts_plate([idx_rgba(g1, p1), idx_rgba(q1, qp1)], k=4, bg=(248, 248, 244)))
    return res


def mock_keypad(shots, d):
    s = shot(shots, "INDEX")
    res = []
    if s is not None:
        img, n = keypad_composite(s, d)
        res.append(img)
    g = keypad_art(d)
    pal = [(248, 248, 248), (248, 248, 248), (98, 98, 98), (213, 213, 205), (230, 8, 8)] + [(0, 0, 0)] * 11
    halves = [r[:64] for r in g] + [r[64:] for r in g]
    res.append(zoom(idx_rgba(halves, pal, clear0=False), 2, bg=(248, 248, 248)))
    line = Image.new("RGB", (240, 160), (248, 248, 248))
    # a line of footer text as the INDEX prints it: the glyph, then words
    x = 8
    a = idx_rgba(g, pal)
    for name, x0, y0, w, label in KEYS[:6]:
        line.paste(a.crop((x0, y0, x0 + w, y0 + 12)), (x, 70), a.crop((x0, y0, x0 + w, y0 + 12)))
        x += w + 6
    res.append(line.resize((240, 160)))
    return res


def mock_markings(shots, d):
    p1, p2 = markings_pals(d)
    combo = combo_art(d)
    m2 = markings2_art(d)
    # the MARK menu, as mon_markings.c lays it at (176, 16) in the PC: a 64x128 window of the user's frame (type1),
    # the four marks at (x+28, y+12+16i), the cursor at the left, the 32x32 OK/CANCEL text from (x+16, y+72)
    import gbaframes as F
    base = M.pc_mock("A")
    fr = F.user_frame("bracket")
    tp = F.jasc(os.path.join(F.TW, "type1.pal")) if os.path.exists(os.path.join(F.TW, "type1.pal")) else None
    w, h, bd, pal1, _ = F.load_png(os.path.join(F.TW, "type1.png"))
    win = canvas(64, 128, 1)
    for ty in range(16):
        for tx in range(8):
            sx = 0 if tx == 0 else (2 if tx == 7 else 1)
            sy = 0 if ty == 0 else (2 if ty == 15 else 1)
            for y in range(8):
                for x in range(8):
                    win[ty * 8 + y][tx * 8 + x] = fr[sy * 8 + y][sx * 8 + x]
    x0, y0 = 176 - 8, 16
    wi = idx_rgba(win, pal1[:16])
    base.paste(wi, (x0, y0), wi)
    on = (1, 0, 1, 1)
    for i in range(4):
        t = i * 2 + on[i]
        tile = [r[(t % 4) * 8:(t % 4) * 8 + 8] for r in m2[(t // 4) * 8:(t // 4) * 8 + 8]]
        a = idx_rgba(tile, p2)
        base.paste(a, (x0 + 28, y0 + 12 + 16 * i), a)
    cur = [r[0:8] for r in m2[16:24]]
    a = idx_rgba(cur, p2)
    base.paste(a, (x0 + 14, y0 + 12 + 16 * 1), a)
    txt = canvas(32, 32)
    for t in range(16):
        src_t = 9 + t
        for y in range(8):
            for x in range(8):
                txt[(t // 4) * 8 + y][(t % 4) * 8 + x] = m2[(src_t // 4) * 8 + y][(src_t % 4) * 8 + x]
    a = idx_rgba(txt, p2)
    base.paste(a, (x0 + 16, y0 + 72), a)
    # the combo on the PC's DATA panel: a 32x8 sprite centred at (40, 150): row 13 (circle, triangle, heart on)
    row = combo[13 * 8:14 * 8]
    a = idx_rgba(row, p1)
    base.paste(a, (40 - 16, 150 - 4), a)
    plate = parts_plate([idx_rgba(m2, p2), idx_rgba([r for r in combo[:64]], p1)], k=2, bg=(232, 236, 240))
    return [base, plate]


def mock_pcparts(shots, d):
    import gbamenus2 as M2
    base = M2.pc_parts_mock("A")
    m1, m2 = M2.pc_pals("A")
    sh = idx_rgba(shadow_art(d), m2)
    base.paste(sh, (146 - 8, 38 + 20 - 8), sh)
    # MOVE ITEMS' info window: BG0 tiles 0x1A4-0x1A7 in palette 15, its paper the window at (0, 11)..(x, 20); x = 25
    # columns slid in fully? (itemInfoWindowOffset counts down to 0; at rest the window is 8 columns wide)
    fr = info_frame_art(d)
    fp = info_frame_pal(d)
    win = canvas(9 * 8, 10 * 8, 1)
    for tx in range(8):
        for y in range(8):
            for x in range(8):
                win[y][tx * 8 + x] = fr[y][x]
                win[72 + y][tx * 8 + x] = fr[7 - y][x]
    for ty in range(1, 9):
        for y in range(8):
            for x in range(8):
                win[ty * 8 + y][64 + x] = fr[y][8 + x]
    for y in range(8):
        for x in range(8):
            win[y][64 + x] = fr[y][16 + x]
            win[72 + y][64 + x] = fr[y][24 + x]
    wi = idx_rgba(win, fp)
    base2 = M2.pc_parts_mock("A")
    base2.paste(wi, (0, 88), wi)
    nm = "POTION"
    say(base2, 6, 96, nm, fp[2], fp[3])
    return [base, base2, parts_plate([idx_rgba(shadow_art(d), m2), idx_rgba(fr, fp)], k=4, bg=(232, 236, 240))]


MOCKS = {"bag": mock_bag, "arrows": mock_arrows, "select": mock_select, "swap": mock_swap,
         "fieldicons": mock_fieldicons, "keypad": mock_keypad, "markings": mock_markings, "pcparts": mock_pcparts}

ROWS = {
    "bag": "Rows: the bag (theatre shot, today's background swapped for the draft where it shows); the same with an "
           "item's menu up (the band dimmed, row 2); the bag opened from ITEM STORAGE (bg_item_pc.bin), rendered.",
    "arrows": "Rows: the bag with its list scrolled (the pockets' left/right and the list's up/down arrows found in "
              "the shot and redrawn); VIRIDIAN MART's BUY list; the six frames (left, right, up, down, the cursor, "
              "the selector outline) at 2x.",
    "select": "Rows: SELECT beside a registered item on today's bag; on the A desk; the button at 6x. (Placed as "
              "BlitBitmapToWindow puts it, x 0x70 of the list window, row 2; the route registered no item.)",
    "swap": "Rows: SELECT pressed in the bag (the swap line found in the shot and redrawn); its 16x32 at 4x.",
    "fieldicons": "Rows: CLOSE BAG's icon (theatre shot, the icon redrawn); the ? where an item without a picture "
                  "would show it; both at 4x.",
    "keypad": "Rows: the INDEX's footer (the glyphs found in the shot by shape and redrawn in its colours); the "
              "whole sheet at 2x; A B L R START SELECT in a line at real size.",
    "markings": "Rows: the PC's MARK menu as mon_markings.c lays it (176, 16), circle, triangle and heart on, the "
                "cursor on the square, OK/CANCEL; the combo on the DATA panel (40, 150); markings2 and the combo's "
                "first eight rows at 2x.",
    "pcparts": "Rows: the PC with the PAW's shadow under it (cursor y + 20); MOVE ITEMS' info window's frame; both "
               "at 4x.",
}


def draft(out, shots_dir=None):
    os.makedirs(out, exist_ok=True)
    shots = load_shots(shots_dir)
    made = []
    for piece in PIECES:
        for d in OFFERED[piece]:
            errs = check(piece, d)
            if errs:
                sys.exit("gbamenus3: %s %s breaks its contract: %s" % (piece, d, "; ".join(errs)))
            put_files(outputs(piece, d), os.path.join(out, d, "graphics"))
        cols = [("TODAY (the engine)", MOCKS[piece](shots, None))]
        for d in OFFERED[piece]:
            cols.append(("%s %s" % (d, NAMES[piece][d]), MOCKS[piece](shots, d)))
        notes = [ROWS[piece]] + [NOTES[piece]] + [
            "DRAFT -- drawn in code (tools/gbamenus3.py), nothing in the engine until the user picks; recommended: %s "
            "(%s). APPROVED is empty." % (RECOMMENDED[piece], NAMES[piece][RECOMMENDED[piece]])]
        made.append(contact("T-554 THE MENU LEFTOVERS -- %s -- DRAFT" % piece.upper(), cols, notes,
                            os.path.join(out, "t554_%s_sheet.png" % piece)))
    made.append(std_sheet(out, shots))
    return made


def std_sheet(out, shots):
    import gbaframes as F
    keys = [("VIRIDIAN MART", "BUY"), ("SEE YA",), ("save box",), ("Choose",)]
    imgs = [shot(shots, *k) for k in keys]
    imgs = [i for i in imgs if i is not None]
    if not imgs:
        imgs = [Image.new("RGB", (240, 160), (36, 40, 46))]
    cols = [("TODAY (pret's 9 tiles, stdpal_3)", imgs + [zoom(idx_rgba(F.std_now()[0], F.std_now()[1]), 4)])]
    for v, (g, p3, said) in F.std_versions().items():
        cols.append(("%s %s" % (v, said.split(":")[0]), [std_composite(i, v)[0] for i in imgs] +
                     [zoom(idx_rgba(g, p3), 4)]))
    notes = ["Rows: VIRIDIAN MART's BUY money box (BUDGET); the save box; the party's message box -- "
             "theatre shots with every std tile on the 8px grid found and swapped; the 24x24 at 4x.",
             "The std frame is a FRAME: drawn to match A TERMINAL (type1, the user's pick, T-523). Kept: 9 tiles "
             "(0x120 bytes), DrawStdFrameWithCustomTileAndPalette's order, tile 4 the paper; stdpal_3 is every std "
             "window's text palette and the map popup's, so version 1 leaves it as it is.",
             "Why two: stdpal_3 holds no near-black and no teal, so TERMINAL cannot be matched colour for colour "
             "inside it. 1 draws type1's pixels in stdpal_3's nearest slots (a lighter TERMINAL; std.png only). 2 is "
             "type1 exactly and needs stdpal_3's 10-15 retinted (10 is unused magenta; 11-15 also colour the map name "
             "popup's frame) -- outside the rule that stdpal_0..4 stay; offered only for that reason.",
             "DRAFT -- tools/gbaframes.py --std-draft; APPROVED_STD is None. Recommended: 1."]
    return contact("T-554 THE MENU LEFTOVERS -- THE STD FRAME (std.png) -- DRAFT", cols, notes,
                   os.path.join(out, "t554_std_sheet.png"))


NOTES = {
    "bag": "Kept: bg.bin and bg_item_pc.bin (55 tiles redrawn in place, majority vote per tile), the three rows and "
           "their roles, bg_female.pal = row 0. The pocket name's bar dark (WHITE text), the list's paper light (dark "
           "text), the band dark (WHITE description), the icon box light. A: slate desk on graph paper, the slate "
           "rule and teal bracket of the PC and party; B: T-209's INK AND PAPER, redrawn (leather, brass, a ledger); "
           "C: the battle readout's dark screen and phosphor.",
    "arrows": "Kept: red_arrow.pal is ONE palette for all three files (sRedArrowPal), so they change together; 1 body, "
              "2 edge, 3 newly used (was magenta). Frames 16x16, the drawing's centre where vanilla's is (the code "
              "flips one frame for right/down). A matches the PC's own scroll arrows (T-530 touch-ups): a teal "
              "45-degree chevron ringed in near-black.",
    "select": "Kept: 24x16, drawn only in bag_window_pal's 13-15 (SELECT's alone: the bag's text reads 1, 2, 3, 8, 9); "
              "the word SEL as FireRed has it.",
    "swap": "Kept: 16x32, two frames laid end to end by the code, the line on rows 6-7 of each; its own palette.",
    "fieldicons": "Kept: 24x24 each, own 16-colour palettes, index 0 clear; T-525's icon family (outline, 45-degree "
                  "corners where a box is drawn).",
    "keypad": "Kept: sKeypadIcons' rects (x, width 8/16/24, 12 rows), ink on rows 4-11 only, the text slots' roles "
              "(1 face, 2 ink, 3 light ink, 4 the pressed arm) because the glyphs are blitted into whatever text "
              "window holds them. Words A B L R START SELECT kept; SELECT's E and L two pixels wide to fit 24px.",
    "markings": "Kept: mon_markings' 16 rows x 4 marks (1/2 off, 3/4 on), markings2's frames 0-8 and the 32x32 text "
                "from tile 9 in 1-D order, the menu window (the user's frame, type1, already TERMINAL). B and C change "
                "the four shapes (circle, square, triangle, heart become open marks / four sigils): nothing names them "
                "in text.",
    "pcparts": "Kept: cursor_shadow in misc2's 8 and 15 only (shared with the PAW and the scroll arrows, so not "
               "retinted); item_info_frame's four tiles and their roles, its palette's 1-3 (the window's text) kept, "
               "4/7/9/10/11 its own and retinted.",
}


def report():
    print("gbamenus3 (T-554): the menu leftovers. APPROVED: %s" % (APPROVED or "none -- nothing is written"))
    bad = 0
    for piece in PIECES:
        files = sorted(outputs(piece, "A"))
        print("  %-10s %s" % (piece, ", ".join(files)))
        for d in OFFERED[piece]:
            errs = check(piece, d)
            if errs:
                bad += 1
                print("    %s %s: %s" % (d, NAMES[piece][d], "; ".join(errs)))
    sheet, per, ents, ents_pc, rows, miss = bag_build("A")
    print("  bag A: %d of the map's cells take a tile drawn for another cell (majority vote)" % miss)
    drift = differs(APPROVED)
    for rel in drift:
        print("  DRIFT: engineGba/graphics/%s is not what --write --approved --all makes" % rel)
    return 1 if bad or drift else 0


def differs(picks):
    """The files a write of `picks` would change, compared decoded (indices and q5 colours), not byte for byte."""
    import gbafont
    out = []
    for piece, d in picks.items():
        for rel, payload in outputs(piece, d).items():
            p = os.path.join(G, rel)
            if not os.path.exists(p):
                out.append(rel)
                continue
            if payload[0] == "png":
                w, h, bd, plte, px = gbafont.png_load(p)
                want = payload[1]
                cur = [[v & 15 if payload[3] == 4 else v for v in r] for r in px]
                pal_now = [tuple(q5(tuple(plte[i:i + 3]))) for i in range(0, len(plte), 3)]
                n = 16 if payload[3] == 4 else len(payload[2])
                if cur != [list(r) for r in want] or pal_now[:n] != [tuple(q5(c)) for c in payload[2]][:n]:
                    out.append(rel)
            elif payload[0] == "pal":
                if [q5(c) for c in M.jasc(p)] != [q5(c) for c in payload[1]]:
                    out.append(rel)
    return out


def main():
    if ARGS.write:
        if not ARGS.approved or not (ARGS.pick or ARGS.all):
            sys.exit("gbamenus3: --write needs --approved and --all or --pick piece=A|B|C,... (the user's picks)")
        picks = dict(kv.split("=") for kv in ARGS.pick.split(",")) if ARGS.pick else dict(APPROVED)
        if not picks:
            print("gbamenus3: nothing approved yet (T-554 is a DRAFT); nothing written")
            return 0
        for piece, d in picks.items():
            if piece not in PIECES or d not in OFFERED[piece]:
                sys.exit("gbamenus3: unknown pick %s=%s" % (piece, d))
            if APPROVED.get(piece) != d:
                sys.exit("gbamenus3: %s=%s is not APPROVED (the user's pick goes in APPROVED first)" % (piece, d))
            for p in put_files(outputs(piece, d), G):
                print("  wrote", os.path.relpath(p, ROOT))
        print("  now: build all four ROMs")
        return 0
    if ARGS.draft:
        for p in draft(ARGS.draft, ARGS.shots):
            print("  wrote", os.path.relpath(p, ROOT))
        return 0
    return report()


if __name__ == "__main__":
    sys.exit(main())
