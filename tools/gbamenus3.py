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

T-561 (DRAFT, the field overlays: the trainers' emotes, the itemfinder, the quest log's frame and bar, the START
banner, the HELP screen) lives in its own section at the foot of this file, behind --t561; T-563 (DRAFT, the INDEX and
the map: the INDEX's own tiles, its mini card and ellipse, the town map's heads and switch cursors, HEARSAY's cursor
and ?) in the one after it, behind --t563.

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
ap.add_argument("--t561", action="store_true", help="T-561: the field overlays (DRAFT; see the section at the foot)")
ap.add_argument("--t563", action="store_true", help="T-563: the INDEX and the map (DRAFT; see the section at the foot)")
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
    if ARGS.t561:
        return t561_main()
    if ARGS.t563:
        return t563_main()
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



# ================================================================================================================
# T-561: THE FIELD OVERLAYS -- the Nintendo art drawn over the world (batch 2 of the 2026-11-14 re-census). APPROVED.
#
#     python3 tools/gbamenus3.py --t561                    # report: each piece's files, contract and APPROVED_561
#     python3 tools/gbamenus3.py --t561 --draft [DIR] [--shots DIR]   # every piece into DIR (gfx/drafts/t561_field/)
#     python3 tools/gbamenus3.py --t561 --write --approved --all | --pick piece=X,...   # APPROVED_561 (2026-11-14)
#
# genemoji.py does not own misc/emoticons.png (it writes daemon_emoji.png, the follower's own sheet with its own
# palette), so the trainers' emotes are drawn here, beside T-554's pieces, in the follower bubble's family.
#
# THE PIECES, and what each drop-in keeps:
#   emotes     misc/emoticons.png, 48x80: 15 frames of 16x16, three a row (pop, half, full), rows ! !! X smile ?
#              (sSpriteImages_Emoticons reads rows 0,2,1,3,4 for anims 0-4; the rows are kept where they are).
#              The template's paletteTag is 0xFFFF and its OAM palette 0: the emotes are drawn in the PLAYER's OBJ
#              palette (slot 0, player.pal), which the watch and the season tint with every other object. So they
#              are drawn only in player.pal's slots, the palette is not touched -- and 12 and 13 are NEVER used:
#              T-256 paints them as the shoes' sole and trim at run time. Today's ! is drawn in 12, so since MOM's
#              shoes it has been YELLOW (the theatre shows it), and black with DAD's.
#   itemfinder itemfinder/spr_tiles.png, 16x80: frames 0-3 the arrow (stored pointing LEFT; affine-rotated toward
#              the item, four tones in turn), frame 4 the "here" mark. paletteTag 0xFFFF too: player.pal, never 12/13
#              (today's frames 1 and 4 use 13, the shoes' trim).
#   questlog   text_window/quest_log.png, 40x32: the message box at every CONTINUE's recap (LoadQuestLogWindowTiles,
#              DLG tiles 0-13 laid as menu_message's, five tiles a row here), in BG palette 15 = stdpal_4 (only the
#              quest log loads it). A FRAME: drawn to match A TERMINAL -- the engine's own menu_message (T-523, the
#              user's pick), tile for tile. Tiles 14-19 kept.
#   qldesc     quest_log/description_window.png, 8x24: the recap's description bar (top, middle, bottom tile, the
#              middle repeated), stdpal_4; its text is white on 15 with a 12 shadow, so the middle stays 15 and the
#              designs live in the top tile's rows 0-2 and the bottom's 5-7 (text reaches y 3..21).
#   banner     help_system/msg_window.png, 80x16: the START menu's description banner (tiles 0 top, 5 middle, 14
#              bottom), stdpal_2 -- shared with the slots, the item PC, the SEAGALLOP and menu.c's top bar, so not
#              retinted; text white (10) with a dark grey (2) shadow on a transparent ground: the middle tile is it.
#   helpscreen help_system/bg_tiles.png, 24x24 (9 tiles 0x1F7-0x1FF: the header/footer rules, the sides, the
#              body, two scroll arrows, the clear tile) whose palette (bg_tiles.gbapal is made from the PNG) is the HELP screen's own BG palette 0
#              (entry 0 the backdrop: the page's ground). A FRAME, and its palette is its own, so TERMINAL is matched
#              exactly: 0, 10-15 retinted; 1-9 kept (the text's colours); the arrows move from 4 (red, a text colour)
#              to 11.
# ================================================================================================================
T561_DRAFT = os.path.join(ROOT, "gfx", "drafts", "t561_field")
T561_PIECES = ("emotes", "itemfinder", "questlog", "qldesc", "banner", "helpscreen")
T561_NAMES = {
    "emotes": {"A": "SMALL SCREEN", "B": "PAPER TAG", "C": "BRACKETS"},
    "itemfinder": {"A": "PROMPT CHEVRON", "B": "SLATE WEDGE", "C": "DOUBLE CARET"},
    "questlog": {"1": "TERMINAL, IN STDPAL_4", "2": "TERMINAL, EXACT"},
    "qldesc": {"A": "SLATE BAND", "B": "TICKED RULE", "C": "DASHED RULE"},
    "banner": {"A": "DARK BAND", "B": "TEAL RULE", "C": "DOUBLE RULE"},
    "helpscreen": {"1": "TERMINAL"},
}
T561_OFFERED = {p: "".join(T561_NAMES[p]) for p in T561_PIECES}
T561_RECOMMENDED = {"emotes": "A", "itemfinder": "A", "questlog": "1", "qldesc": "A", "banner": "A",
                    "helpscreen": "1"}
#  The user, 2026-11-14 (multiple choice): emotes A SMALL SCREEN, itemfinder A PROMPT CHEVRON, the quest log's frame 1
#  TERMINAL IN STDPAL_4, the description bar A SLATE BAND, the START banner A DARK BAND, the HELP screen 1 TERMINAL.
#  --t561 --write --approved --all (or --pick with these) writes them; the --t561 report exits 1 on drift from them.
APPROVED_561 = {"emotes": "A", "itemfinder": "A", "questlog": "1", "qldesc": "A", "banner": "A", "helpscreen": "1"}

OBJ_PAL = "object_events/palettes/player.pal"
SHOES = (12, 13)           # T-256: the sole and the trim, painted at run time -- never drawn in


def player_pal():
    return jpal(OBJ_PAL)


# ------------------------------------------------------------------------------------------------ the emotes
#  player.pal's slots, by role (and never 12/13):
#    6 ink (34,34,40)   5 glass (52,52,60)   14 shade (100,100,112)   7 bezel (156,156,166)   2 bezel lit (176,168,164)
#    9 paper/glow (240,230,204)   10 paper dim (202,190,160)   11 amber (188,128,72)   8 amber dark (132,84,48)
E_INK, E_GLASS, E_SHADE, E_BEZEL, E_LIT, E_PAPER, E_DIM, E_AMBER, E_AMBER_DK = 6, 5, 14, 7, 2, 9, 10, 11, 8
EMOTE_ROWS = ("excl", "excl2", "x", "smile", "q")       # the sheet's rows, top to bottom

#  The glyphs, 10 x 7, drawn on a screen's glass (A), a card (B) or bare (C). '#' the stroke.
GLYPHS = {
    "excl": ["....##....",
             "....##....",
             "....##....",
             "....##....",
             "..........",
             "....##....",
             ".........."],
    "excl2": ["..##..##..",
              "..##..##..",
              "..##..##..",
              "..##..##..",
              "..........",
              "..##..##..",
              ".........."],
    "x": ["..##..##..",
          "...####...",
          "....##....",
          "...####...",
          "..##..##..",
          "..........",
          ".........."],
    "smile": ["..........",
              "...#..#...",
              "...#..#...",
              "..........",
              "..#....#..",
              "...####...",
              ".........."],
    "q": ["...####...",
          "..##..##..",
          "......##..",
          ".....##...",
          "....##....",
          "..........",
          "....##...."],
}


def glyph_cells(kind, scale_y=1.0):
    g = GLYPHS[kind]
    return [(x, int(y * scale_y)) for y, r in enumerate(g) for x, c in enumerate(r) if c == "#"]


def emote_A(kind, f):
    """SMALL SCREEN: the follower's bubble (genemoji) as the trainers' -- a bezel, dark glass, a glint, the glyph lit
    on the glass, an amber power light (the follower's is its feeling's colour), the tail down. Frames: the screen
    switching on -- a lit line, the bezel at half height, the screen."""
    g = canvas(16, 16)
    if f == 0:                                          # a line of light, as a tube comes on
        fill(g, 3, 6, 13, 9, E_INK)
        fill(g, 4, 7, 12, 8, E_PAPER)
        put(g, 3, 6, 0), put(g, 12, 6, 0), put(g, 3, 8, 0), put(g, 12, 8, 0)
        return g
    top, bot = (0, 12) if f == 2 else (3, 11)
    for x in range(2, 14):
        put(g, x, top, E_INK), put(g, x, bot, E_INK), put(g, x, top + 1, E_LIT), put(g, x, bot - 1, E_SHADE)
    for y in range(top + 2, bot - 1):
        put(g, 0, y, E_INK), put(g, 15, y, E_INK), put(g, 1, y, E_LIT), put(g, 14, y, E_SHADE)
    for (x, y) in ((1, top + 1), (14, top + 1), (1, bot - 1), (14, bot - 1)):
        put(g, x, y, E_INK)
    fill(g, 2, top + 2, 14, bot - 1, E_GLASS)
    for (x, y) in ((2, top + 2), (13, top + 2), (2, bot - 2), (13, bot - 2)):
        put(g, x, y, E_BEZEL)
    put(g, 3, top + 2, E_PAPER), put(g, 2, top + 3, E_PAPER)          # the glint
    put(g, 12, bot - 1, E_AMBER)                                      # the power light
    put(g, 7, bot, E_SHADE), put(g, 8, bot, E_SHADE)                  # the tail
    put(g, 6, bot + 1, E_INK), put(g, 7, bot + 1, E_SHADE), put(g, 8, bot + 1, E_SHADE), put(g, 9, bot + 1, E_INK)
    put(g, 7, bot + 2, E_INK), put(g, 8, bot + 2, E_INK)
    if f == 2:
        for (x, y) in glyph_cells(kind):
            put(g, 3 + x, 3 + y, E_PAPER)
    else:                                               # the glyph half-formed: its rows squeezed, dim
        for (x, y) in glyph_cells(kind, 0.5):
            put(g, 3 + x, top + 3 + y, E_DIM)
    return g


def emote_B(kind, f):
    """PAPER TAG: A TERMINAL's frame as a tag -- paper inside a slate rule cut at 45 degrees, the amber corner
    bracket top left (the frame's bracket), the glyph in ink, a notch pointing down at whoever it is over."""
    g = canvas(16, 16)
    if f == 0:
        cut_box(g, 5, 6, 6, 5, 1, [E_INK], E_PAPER)
        return g
    x0, y0, w, h = (0, 0, 16, 13) if f == 2 else (2, 3, 12, 9)
    cut_box(g, x0, y0, w, h, 2, [E_INK, E_SHADE], E_PAPER)
    for k in range(3):                                  # the bracket
        put(g, x0 + 2 + k, y0 + 2, E_AMBER), put(g, x0 + 2, y0 + 2 + k, E_AMBER)
    by = y0 + h                                         # the notch
    put(g, 7, by - 1, E_PAPER), put(g, 8, by - 1, E_PAPER)
    put(g, 6, by - 1, E_INK), put(g, 9, by - 1, E_INK)
    put(g, 7, by, E_INK), put(g, 8, by, E_INK)
    if f == 2:
        for (x, y) in glyph_cells(kind):
            put(g, 3 + x, 3 + y, E_INK)
    else:
        for (x, y) in glyph_cells(kind, 0.5):
            put(g, 3 + x, y0 + 3 + y, E_SHADE)
    return g


def emote_C(kind, f):
    """BRACKETS: no bubble at all -- the glyph alone in paper, ringed in ink so it reads on grass, sand, snow and
    water, held between two amber terminal brackets that open out as it appears."""
    g = canvas(16, 16)
    spread = (2, 1, 0)[f]                               # the brackets close in from the middle, then open
    lx, rx, ty, by = 1 + 3 * spread, 14 - 3 * spread, 1 + 2 * spread, 12 - 2 * spread

    def bracket(x, y, dx, dy):
        for k in range(3):
            put(g, x + dx * k, y, E_AMBER), put(g, x, y + dy * k, E_AMBER)

    def ring(cells, v):
        for (x, y) in cells:
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    if g[min(15, max(0, y + oy))][min(15, max(0, x + ox))] == 0:
                        put(g, x + ox, y + oy, E_INK)
        for (x, y) in cells:
            put(g, x, y, v)

    bracket(lx, ty, 1, 1)
    bracket(rx, by, -1, -1)
    for (x, y) in [(lx, ty), (lx + 1, ty), (lx + 2, ty), (lx, ty + 1), (lx, ty + 2),
                   (rx, by), (rx - 1, by), (rx - 2, by), (rx, by - 1), (rx, by - 2)]:
        for (ox, oy) in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            if 0 <= x + ox < 16 and 0 <= y + oy < 16 and g[y + oy][x + ox] == 0:
                put(g, x + ox, y + oy, E_INK)
    if f == 2:
        ring([(3 + x, 3 + y) for (x, y) in glyph_cells(kind)], E_PAPER)
    elif f == 1:
        ring([(3 + x, 5 + y) for (x, y) in glyph_cells(kind, 0.5)], E_DIM)
    return g


EMOTE_FN = {"A": emote_A, "B": emote_B, "C": emote_C}


def emotes_art(direction):
    g = canvas(48, 80)
    for r, kind in enumerate(EMOTE_ROWS):
        for f in range(3):
            fr = EMOTE_FN[direction](kind, f)
            for y in range(16):
                for x in range(16):
                    g[r * 16 + y][f * 16 + x] = fr[y][x]
    return g


def emote_frame(g, row, f):
    return [r[f * 16:f * 16 + 16] for r in g[row * 16:row * 16 + 16]]


# ------------------------------------------------------------------------------------------------ the itemfinder
IF_TONES = (E_PAPER, E_INK, E_LIT, E_AMBER)            # today's four frames: cream, (13) dark, grey, amber -- 13 gone


def arrow_A(tone):
    """PROMPT CHEVRON: T-523's prompt chevron, pointing left -- a 45-degree '<' two pixels thick, ringed in ink (or,
    in the ink frame, in paper) so it reads over the player and the ground."""
    g = canvas(16, 16)
    edge = E_PAPER if tone == E_INK else E_INK
    body = []
    for k in range(5):
        for t in (0, 1):
            body += [(3 + k + t, 8 - k), (3 + k + t, 8 + k)]
    body += [(9, 3), (9, 13)]
    for (x, y) in body:
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if g[y + oy][x + ox] == 0:
                    put(g, x + ox, y + oy, edge)
    for (x, y) in body:
        put(g, x, y, tone)
    return g


def arrow_B(tone):
    """SLATE WEDGE: today's solid wedge kept, ringed in ink, its upper edge lit."""
    g = canvas(16, 16)
    edge = E_PAPER if tone == E_INK else E_INK
    for y in range(4, 13):
        w = 8 - abs(y - 8) * 2
        for x in range(10 - w, 11):
            put(g, x, y, tone)
    for y in range(3, 14):
        for x in range(1, 12):
            if g[y][x] == 0 and any(0 <= y + oy < 16 and g[y + oy][x + ox] not in (0, edge)
                                    for ox in (-1, 0, 1) for oy in (-1, 0, 1)):
                g[y][x] = edge
    for y in range(4, 9):
        x = 10 - (8 - abs(y - 8) * 2)
        if g[y][x + 1] == tone and tone != E_PAPER:
            put(g, x + 1, y, E_PAPER if tone != E_LIT else E_PAPER)
    return g


def arrow_C(tone):
    """DOUBLE CARET: '<<', one pixel each, ringed -- the terminal's back-history key."""
    g = canvas(16, 16)
    edge = E_PAPER if tone == E_INK else E_INK
    body = []
    for x0 in (3, 8):
        for k in range(4):
            body += [(x0 + k, 8 - k), (x0 + k, 8 + k)]
    for (x, y) in body:
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if g[y + oy][x + ox] == 0:
                    put(g, x + ox, y + oy, edge)
    for (x, y) in body:
        put(g, x, y, tone)
    return g


def here_mark(direction):
    """Frame 4: standing on it. A: a diamond in four corner brackets (the found cursor); B: a four-point spark;
    C: a crosshair ring."""
    g = canvas(16, 16)
    if direction == "A":
        for k in range(4):
            for (x, y) in ((7 - k, 4 + k), (8 + k, 4 + k), (7 - k, 11 - k), (8 + k, 11 - k)):
                put(g, x, y, E_INK)
        fill(g, 7, 5, 9, 11, E_PAPER), fill(g, 6, 6, 10, 10, E_PAPER), fill(g, 5, 7, 11, 9, E_PAPER)
        fill(g, 7, 7, 9, 9, E_AMBER)
        for (x, y, dx, dy) in ((1, 1, 1, 1), (14, 1, -1, 1), (1, 14, 1, -1), (14, 14, -1, -1)):
            for k in range(3):
                put(g, x + dx * k, y, E_AMBER), put(g, x, y + dy * k, E_AMBER)
    elif direction == "B":
        body = [(7, y) for y in range(2, 14)] + [(8, y) for y in range(2, 14)] + \
               [(x, 7) for x in range(2, 14)] + [(x, 8) for x in range(2, 14)] + [(6, 6), (9, 6), (6, 9), (9, 9)]
        for (x, y) in body:
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    if g[y + oy][x + ox] == 0:
                        put(g, x + ox, y + oy, E_INK)
        for (x, y) in body:
            put(g, x, y, E_PAPER)
        fill(g, 7, 7, 9, 9, E_AMBER)
    else:
        for y in range(16):
            for x in range(16):
                d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
                if 4.6 <= d < 5.8:
                    g[y][x] = E_PAPER
                elif 3.6 <= d < 4.6 or 5.8 <= d < 6.8:
                    g[y][x] = E_INK
        for k in (1, 2, 13, 14):
            put(g, k, 7, E_AMBER), put(g, k, 8, E_AMBER), put(g, 7, k, E_AMBER), put(g, 8, k, E_AMBER)
        fill(g, 7, 7, 9, 9, E_AMBER)
    return g


ARROW_FN = {"A": arrow_A, "B": arrow_B, "C": arrow_C}


def itemfinder_art(direction):
    g = canvas(16, 80)
    frames = [ARROW_FN[direction](t) for t in IF_TONES] + [here_mark(direction)]
    for i, fr in enumerate(frames):
        for y in range(16):
            g[i * 16 + y] = list(fr[y])
    return g


# ------------------------------------------------------------------------------------------------ the quest log
TW4 = "text_window/stdpal_4.pal"
#  stdpal_0's TERMINAL slots -> stdpal_4's nearest in lightness (version 1): the outline near-black to 10 (the darkest,
#  a slate teal), the band slate to 15, its light to 13, the bracket's teal to 14 (stdpal_4 has no teal bright enough),
#  the inner-corner flecks to 3.
QL_SLOTS_1 = {0: 0, 1: 1, 11: 3, 12: 13, 13: 15, 14: 14, 15: 10}


def dlg_tiles_from(rel, per):
    w, h, pal, px = png(rel) if rel != "text_window/menu_message.png" else _engine_png(rel)
    return {t: tile_of(px, t, per) for t in range(14)}


def _engine_png(rel):
    """The engine's file as it is NOW (the user's A TERMINAL, built by T-523) -- the frame to match, not to replace."""
    im = Image.open(os.path.join(G, rel))
    raw = im.getpalette() or []
    d = list(im.getdata())
    w, h = im.size
    return w, h, [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)], [[d[y * w + x] for x in range(w)] for y in range(h)]


def questlog_art(version):
    term = dlg_tiles_from("text_window/menu_message.png", 6)
    w, h, pal, now = png("text_window/quest_log.png")
    g = [[v & 15 for v in r] for r in now]
    if isinstance(pal, list) and not any(pal):
        pass
    for t, blk in term.items():
        x0, y0 = (t % 5) * 8, (t // 5) * 8
        for y in range(8):
            for x in range(8):
                v = blk[y][x] & 15
                g[y0 + y][x0 + x] = QL_SLOTS_1.get(v, v) if version == "1" else v
    return g


def questlog_pal(version):
    p = jpal(TW4)
    if version == "2":
        p0 = jpal("text_window/stdpal_0.pal")
        for s in (11, 12, 13, 14, 15):
            p[s] = p0[s]
    return p


def questlog_box(version, pal=None):
    """The 240x48 box the hardware draws from tiles 0-13 (gbaframes.strip), as an index grid."""
    import gbaframes as F
    g = questlog_art(version)
    q = [[0] * F.QW for _ in range(F.QH)]
    for t, (x0, y0) in F.DLG_TILES.items():
        for y in range(8):
            for x in range(8):
                q[y0 + y][x0 + x] = g[(t // 5) * 8 + y][(t % 5) * 8 + x]
    for y in range(8, F.QH):
        for x in range(16, 24):
            q[y][x] = 1
    return F.strip(q)


# ------------------------------------------------------------------------------------------------ the description bar
#  stdpal_4: 10 slate teal (dark), 11/12/13/14 greys 131..230, 15 slate (the ground), 1 white.
def qldesc_art(direction):
    top = [[15] * 8 for _ in range(8)]
    mid = [[15] * 8 for _ in range(8)]
    if direction == "A":           # SLATE BAND: a dark rule, a light hairline, then the band
        top[0], top[1] = [10] * 8, [13] * 8
    elif direction == "B":         # TICKED RULE: a light rule with a tick every 8px, as a ruler
        top[0], top[1] = [10] * 8, [14] * 8
        top[2] = [14, 15, 15, 15, 15, 15, 15, 15]
    else:                          # DASHED RULE: the dark rule broken into dashes, a tooth hanging from each
        top[0] = [10, 10, 10, 10, 10, 10, 15, 15]
        top[1] = [10, 13, 13, 13, 13, 10, 15, 15]
        top[2] = [10, 15, 15, 15, 15, 15, 15, 15]
    bot = [r[:] for r in reversed(top)]
    return top + mid + bot


def qldesc_bar(direction, pal_version="1"):
    """The description window as CopyDescriptionWindowTiles lays it: 30 tiles wide, 6 high (rows 14-19)."""
    g = qldesc_art(direction) if direction else [[v & 15 for v in r] for r in png("quest_log/description_window.png")[3]]
    rows = []
    for i in range(6):
        t = 0 if i == 0 else (2 if i == 5 else 1)
        for y in range(8):
            rows.append([g[t * 8 + y][x % 8] for x in range(240)])
    return rows


# ------------------------------------------------------------------------------------------------ the START banner
#  stdpal_2 (not retinted: the slots, the item PC, the SEAGALLOP and menu.c's bar share it): 10 white (the text),
#  11 sky (74,205,238), 12 cyan (16,172,222), 13 dark teal (0,82,115), 14 teal (0,115,139), 15 blue (0,123,197).
def banner_art(direction):
    w, h, pal, now = png("help_system/msg_window.png")
    g = [[v & 15 for v in r] for r in now]
    if direction == "A":           # DARK BAND: the darkest teal is the ground (the nearest stdpal_2 has to slate)
        top = [[13] * 8 for _ in range(8)]
        top[0], top[1], top[2] = [15] * 8, [11] * 8, [13] * 8
        mid = [[13] * 8 for _ in range(8)]
        bot = [[13] * 8 for _ in range(8)]
        bot[6], bot[7] = [14] * 8, [15] * 8
    elif direction == "B":         # TEAL RULE: teal ground, a sky rule on top with a tick every 8px, a dark foot
        top = [[14] * 8 for _ in range(8)]
        top[0], top[1] = [13] * 8, [11] * 8
        top[2] = [11, 14, 14, 14, 14, 14, 14, 14]
        mid = [[14] * 8 for _ in range(8)]
        bot = [[14] * 8 for _ in range(8)]
        bot[6], bot[7] = [13] * 8, [13] * 8
    else:                          # DOUBLE RULE: today's blue kept, two hairlines over it and a dark foot
        top = [[15] * 8 for _ in range(8)]
        top[0], top[1], top[2], top[3] = [13] * 8, [11] * 8, [15] * 8, [12] * 8
        mid = [[15] * 8 for _ in range(8)]
        bot = [[15] * 8 for _ in range(8)]
        bot[5], bot[6], bot[7] = [12] * 8, [13] * 8, [13] * 8
    for t, blk in ((0, top), (5, mid), (14, bot)):
        x0, y0 = (t % 10) * 8, (t // 10) * 8
        for y in range(8):
            for x in range(8):
                g[y0 + y][x0 + x] = blk[y][x]
    return g


def banner_strip(g):
    """The 240x40 window (30x5 tiles): row 0 tile 0, rows 1-3 tile 5, row 4 tile 14."""
    out = []
    for i in range(5):
        t = 0 if i == 0 else (14 if i == 4 else 5)
        x0, y0 = (t % 10) * 8, (t // 10) * 8
        for y in range(8):
            out.append([g[y0 + y][x0 + (x % 8)] for x in range(240)])
    return out


# ------------------------------------------------------------------------------------------------ the HELP screen
#  bg_tiles: 9 tiles, 3 a row; tile i is map tile 0x1F7 + i.
#    0 0x1F7 header rule (lighter)   1 0x1F8 footer rule (lighter)   2 0x1F9 the side columns
#    3 0x1FA the body                4 0x1FB header rule (darker)    5 0x1FC footer/row-5 rule (darker)
#    6 0x1FD scroll arrow down       7 0x1FE scroll arrow up         8 0x1FF clear (the backdrop, entry 0)
HELP_PAL_EXACT = {0: SLATE_OUT, 10: (16, 20, 28), 11: TEAL, 12: TEAL_DK, 13: SLATE_MID, 14: (48, 58, 72),
                  15: SLATE_OUT}


def helpscreen_art(version="1"):
    T = {i: canvas(8, 8, 0) for i in range(9)}
    T[0] = [[15] * 8 for _ in range(8)]
    T[0][5], T[0][6], T[0][7] = [13] * 8, [11] * 8, [14] * 8                     # header: slate, teal, the body
    T[1] = [[15] * 8 for _ in range(8)]
    T[1][0], T[1][1], T[1][2] = [14] * 8, [11] * 8, [13] * 8                     # footer: the body, teal, slate
    T[2] = [[10] * 8 for _ in range(8)]                                          # the sides: near-black
    for y in range(8):
        T[2][y][3] = 13
    T[3] = [[14] * 8 for _ in range(8)]                                          # the body
    T[4] = [[14] * 8 for _ in range(8)]
    T[4][0], T[4][1], T[4][2] = [10] * 8, [11] * 8, [13] * 8                     # the darker header rule
    T[5] = [[14] * 8 for _ in range(8)]
    T[5][5], T[5][6], T[5][7] = [13] * 8, [11] * 8, [10] * 8
    for i, up in ((6, False), (7, True)):                                        # the arrows: teal, ringed
        g = canvas(8, 8)
        for k in range(4):                                                       # k 0 the point
            y = (1 + k) if up else (6 - k)
            for x in range(3 - k, 5 + k):
                g[y][x] = 11
            put(g, 3 - k, y, 10), put(g, 4 + k, y, 10)
        for x in range(0, 8):
            put(g, x, 5 if up else 2, 10)
        put(g, 3, 0 if up else 7, 10), put(g, 4, 0 if up else 7, 10)
        T[i] = g
    T[8] = canvas(8, 8, 0)
    g = canvas(24, 24)
    for i, blk in T.items():
        for y in range(8):
            for x in range(8):
                g[(i // 3) * 8 + y][(i % 3) * 8 + x] = blk[y][x]
    return g


def helpscreen_pal(version="1"):
    p = list(png("help_system/bg_tiles.png")[2][:16])
    for k, v in HELP_PAL_EXACT.items():
        p[k] = v
    return p


def read_gbapal(rel):
    d = open(os.path.join(G, rel), "rb").read()
    return [((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3) for v in struct.unpack("<16H", d[:32])]


# ------------------------------------------------------------------------------------------------ files and checks
def t561_outputs(piece, d):
    if piece == "emotes":
        return {"misc/emoticons.png": _png(emotes_art(d), png("misc/emoticons.png")[2][:16])}
    if piece == "itemfinder":
        return {"itemfinder/spr_tiles.png": _png(itemfinder_art(d), png("itemfinder/spr_tiles.png")[2][:16])}
    if piece == "questlog":
        out = {"text_window/quest_log.png": _png(questlog_art(d), questlog_pal(d))}
        if d == "2":
            out["text_window/stdpal_4.pal"] = ("pal", questlog_pal(d))
        return out
    if piece == "qldesc":
        return {"quest_log/description_window.png": _png(qldesc_art(d), jpal(TW4))}
    if piece == "banner":
        return {"help_system/msg_window.png": _png(banner_art(d), png("help_system/msg_window.png")[2][:16])}
    if piece == "helpscreen":
        p = helpscreen_pal(d)
        return {"help_system/bg_tiles.png": _png(helpscreen_art(d), p)}      # bg_tiles.gbapal is made from the PNG
    return {}


def t561_check(piece, d):
    errs = []
    for rel, payload in t561_outputs(piece, d).items():
        if payload[0] != "png":
            continue
        g = payload[1]
        w, h, pal, now = png(rel)
        if (len(g[0]), len(g)) != (w, h):
            errs.append("%s is %dx%d, not %dx%d" % (rel, len(g[0]), len(g), w, h))
        used = {v for r in g for v in r}
        if piece in ("emotes", "itemfinder") and used & set(SHOES):
            errs.append("%s draws in %s (the shoes' slots, T-256)" % (rel, sorted(used & set(SHOES))))
        if piece == "qldesc" and any(v != 15 for r in g[8:16] for v in r):
            errs.append("the middle tile is not all 15 (the text's ground)")
        if piece == "qldesc" and any(v != 15 for r in g[3:21] for v in r[:1]) and d != "C":
            errs.append("text rows 3-20 must stay 15")
        if piece == "banner" and used - {0, 10, 11, 12, 13, 14, 15}:
            errs.append("draws outside stdpal_2's own slots 10-15")
        if piece == "helpscreen" and used & {4} :
            errs.append("draws in 4 (the HELP text's red)")
    return errs


def t561_report():
    print("gbamenus3 --t561 (T-561): the field overlays. APPROVED_561: %s" % (APPROVED_561 or "none -- nothing is written"))
    bad = 0
    for piece in T561_PIECES:
        print("  %-10s %s" % (piece, ", ".join(sorted(t561_outputs(piece, T561_RECOMMENDED[piece])))))
        for d in T561_OFFERED[piece]:
            errs = t561_check(piece, d)
            if errs:
                bad += 1
                print("    %s %s: %s" % (d, T561_NAMES[piece][d], "; ".join(errs)))
    drift = t561_differs(APPROVED_561)
    for rel in drift:
        print("  DRIFT: engineGba/graphics/%s is not what --t561 --write --approved --all makes" % rel)
    return 1 if bad or drift else 0


def t561_differs(picks):
    """The files a write of `picks` would change, compared decoded (indices and q5 colours)."""
    import gbafont
    out = []
    for piece, d in picks.items():
        for rel, payload in t561_outputs(piece, d).items():
            p = os.path.join(G, rel)
            if not os.path.exists(p):
                out.append(rel)
            elif payload[0] == "png":
                try:
                    w, h, bd, plte, px = gbafont.png_load(p)
                except BaseException:                    # pret's quest_log.png is greyscale: not ours yet
                    out.append(rel)
                    continue
                cur = [[v & 15 for v in r] for r in px]
                pal_now = [tuple(q5(tuple(plte[i:i + 3]))) for i in range(0, len(plte), 3)][:16]
                if cur != [list(r) for r in payload[1]] or pal_now != [tuple(q5(c)) for c in payload[2]][:16]:
                    out.append(rel)
            elif payload[0] == "pal" and [q5(c) for c in M.jasc(p)] != [q5(c) for c in payload[1]]:
                out.append(rel)
    return out


# ------------------------------------------------------------------------------------------------ mocks
def find_shape(img, grid, slack=6):
    """Where `grid` sits in `img` whatever its palette: the pixels of one index all one colour, different indices
    different colours (mGBA's colours are not the .pal's) -- up to `slack` pixels off, for the falling leaves and
    the weather drawn over it. The best fit, or nothing."""
    from collections import Counter
    pts = [(x, y, v) for y, r in enumerate(grid) for x, v in enumerate(r) if v]
    p = img.load()
    W, H = img.size
    gw, gh = len(grid[0]), len(grid)
    best = None
    for y in range(0, H - gh + 1):
        for x in range(0, W - gw + 1):
            by = {}
            for (dx, dy, v) in pts:
                by.setdefault(v, []).append(p[x + dx, y + dy])
            off, cols = 0, []
            for v, cs in by.items():
                c, n = Counter(cs).most_common(1)[0]
                off += len(cs) - n
                cols.append(c)
                if off > slack:
                    break
            if off <= slack and len(set(cols)) == len(cols) and (best is None or off < best[0]):
                best = (off, x, y)
    return [best[1:]] if best else []


def _blank():
    return Image.new("RGB", (240, 160), (36, 40, 46))


def _over(img, g, pal, x, y, k=1):
    """Draw index grid g (0 clear) onto img at (x, y)."""
    out = img.copy()
    o = out.load()
    for dy, r in enumerate(g):
        for dx, v in enumerate(r):
            X, Y = x + dx, y + dy
            if v and 0 <= X < out.width and 0 <= Y < out.height:
                o[X, Y] = mgba(q5(pal[v]))
    return out


def _restore(img, clean, g_old, x, y):
    out = img.copy()
    o, c = out.load(), clean.load()
    for dy, r in enumerate(g_old):
        for dx, v in enumerate(r):
            X, Y = x + dx, y + dy
            if v and 0 <= X < 240 and 0 <= Y < 160:
                o[X, Y] = c[X, Y]
    return out


def _player_pal_live(shoes="MOM"):
    """player.pal as it stands on screen once shoes are given (T-256: MOM's sole yellow, trim black)."""
    p = player_pal()
    if shoes == "MOM":
        p[12], p[13] = (240, 200, 32), (24, 24, 32)
    return p


TERRAINS = [("grass", (152, 192, 128)), ("sand", (224, 208, 160)), ("snow", (240, 244, 248)),
            ("water", (72, 136, 200)), ("night", (24, 32, 56)), ("cave", (88, 72, 64))]


def terrain_plate(frames_by_dir, pal):
    """Each direction's full ! (and ? and !!) at 1x and 3x over six grounds."""
    im = Image.new("RGB", (240, 160), (36, 40, 46))
    d = ImageDraw.Draw(im)
    for i, (name, c) in enumerate(TERRAINS):
        x0 = i * 40
        d.rectangle([x0, 0, x0 + 39, 159], fill=c)
        for j, fr in enumerate(frames_by_dir):
            z = idx_rgba(fr, pal).resize((32, 32), Image.NEAREST)
            im.paste(z, (x0 + 4, 4 + j * 52), z)
            o = idx_rgba(fr, pal)
            im.paste(o, (x0 + 12, 38 + j * 52), o)
    return im


def mock_emotes(shots, d):
    pal = _player_pal_live()
    old = emotes_art_today()
    g = emotes_art(d) if d else old
    full = emote_frame(g, 0, 2)
    imgs = []
    s = shot_any(shots, "spotted")
    if s is not None:
        hits = find_shape(s, emote_frame(old, 0, 2))
        base = s
        for (x, y) in hits[:1]:
            base = _restore(s, s, [[0]], x, y)
            # erase today's bubble with the ground round it, then draw the draft
            ring = [s.getpixel((X, Y)) for X in range(max(0, x - 1), min(240, x + 17)) for Y in (max(0, y - 1),)]
            bgc = max(set(ring), key=ring.count)
            o = base.load()
            ref = emote_frame(old, 0, 2)
            for dy in range(16):
                for dx in range(16):
                    if ref[dy][dx] and 0 <= x + dx < 240 and 0 <= y + dy < 160:
                        o[x + dx, y + dy] = bgc
            base = _over(base, full, pal, x, y)
            imgs.append(base)
            zx, zy = max(0, min(240 - 80, x - 32)), max(0, min(160 - 53, y - 10))
            imgs.append(base.crop((zx, zy, zx + 80, zy + 53)).resize((240, 160), Image.NEAREST))
        if not hits:
            imgs += [s, s]
    else:
        imgs += [_blank(), _blank()]
    imgs.append(terrain_plate([emote_frame(g, 0, 2), emote_frame(g, 4, 2), emote_frame(g, 1, 2)], pal))
    imgs.append(zoom(idx_rgba(g, pal), 2))
    return imgs


def emotes_art_today():
    return [[v & 15 for v in r] for r in png("misc/emoticons.png")[3]]


def shot_any(shots, key, n=None):
    for name, im in shots.items():
        if key.lower() in name.lower() and im.size == (240, 160):
            return im
    return None


def mock_itemfinder(shots, d):
    pal = _player_pal_live()
    old = [[v & 15 for v in r] for r in png("itemfinder/spr_tiles.png")[3]]
    g = itemfinder_art(d) if d else old
    frames = [g[i * 16:(i + 1) * 16] for i in range(5)]
    up = [[frames[0][15 - x][y] for x in range(16)] for y in range(16)]   # turned a quarter: the point up
    imgs = []
    s = shot_any(shots, "itemfinder")
    if s is not None:
        base = s.copy()
        # the player stands at screen (112, 72); the arrow sprite is drawn centred on them, pointing at the item
        base = _over(base, up, pal, 104, 60)
        imgs.append(base)
        imgs.append(base.crop((72, 36, 152, 89)).resize((240, 160), Image.NEAREST))
    else:
        imgs += [_blank(), _blank()]
    imgs.append(parts_plate([idx_rgba(f, pal) for f in frames], k=2))
    return imgs


def mock_questlog(shots, v):
    imgs = []
    if v is None:
        g = questlog_box_today()
        pal = jpal(TW4)
    else:
        g, pal = questlog_box(v), questlog_pal(v)
    s = shot_any(shots, "recap")
    base = s.copy() if s is not None else _blank()
    o = base.load()
    for y in range(48):
        for x in range(240):
            if g[y][x]:
                o[x, 112 + y] = mgba(q5(pal[g[y][x]]))
    imgs.append(base)
    imgs.append(base.crop((0, 100, 120, 160)).resize((240, 120), Image.NEAREST).crop((0, 0, 240, 120)))
    w = Image.new("RGB", (240, 160), (36, 40, 46))
    w.paste(imgs[-1], (0, 20))
    imgs[-1] = w
    return imgs


def questlog_box_today():
    import gbaframes as F
    w, h, pal, now = png("text_window/quest_log.png")
    g = [[v & 15 for v in r] for r in now]
    q = [[0] * F.QW for _ in range(F.QH)]
    for t, (x0, y0) in F.DLG_TILES.items():
        for y in range(8):
            for x in range(8):
                q[y0 + y][x0 + x] = g[(t // 5) * 8 + y][(t % 5) * 8 + x]
    for y in range(8, F.QH):
        for x in range(16, 24):
            q[y][x] = 1
    return F.strip(q)


QL_LINES = ["DRAFT: the recap's description bar,", "white on the band as the engine prints it."]


def mock_qldesc(shots, d, pal_version="1"):
    pal = questlog_pal(pal_version) if pal_version else jpal(TW4)
    rows = qldesc_bar(d)
    s = shot_any(shots, "recap")
    base = s.copy() if s is not None else _blank()
    o = base.load()
    for y in range(48):
        for x in range(240):
            o[x, 112 + y] = mgba(q5(pal[rows[y][x]]))
    for i, line in enumerate(QL_LINES):
        say(base, 2, 112 + 10 + 14 * i, line, pal[1], pal[12])
    return [base, base.crop((0, 104, 120, 160)).resize((240, 112), Image.NEAREST)]


def mock_banner(shots, d):
    pal = jpal("text_window/stdpal_2.pal")
    g = banner_art(d) if d else [[v & 15 for v in r] for r in png("help_system/msg_window.png")[3]]
    strip_ = banner_strip(g)
    s = shot_any(shots, "description banner")
    base = s.copy() if s is not None else _blank()
    o = base.load()
    for y in range(40):
        for x in range(240):
            o[x, 120 + y] = mgba(q5(pal[strip_[y][x]]))
    for i, line in enumerate(["A device that records DAEMON secrets", "upon meeting or binding them."]):
        say(base, 2, 120 + 5 + 14 * i, line, pal[10], pal[2])
    return [base, base.crop((0, 112, 120, 160)).resize((240, 96), Image.NEAREST)]


def mock_helpscreen(shots, v):
    """The HELP screen laid as help_system_util draws it: the clear backdrop, the body (rows 3-19, cols 1-28), the
    darker header and footer rules (rows 2 and 19), the side columns, the scroll arrows -- with sample text."""
    if v is None:
        w, h, pal, now = png("help_system/bg_tiles.png")
        g = [[x & 15 for x in r] for r in now]
        pal = png("help_system/bg_tiles.png")[2][:16]
    else:
        g, pal = helpscreen_art(v), helpscreen_pal(v)
    s = shot_any(shots, "HELP the screen")
    T = {i: [r[(i % 3) * 8:(i % 3) * 8 + 8] for r in g[(i // 3) * 8:(i // 3) * 8 + 8]] for i in range(9)}
    im = Image.new("RGB", (240, 160), q5(pal[0]))
    o = im.load()

    def tile(i, cx, cy):
        for y in range(8):
            for x in range(8):
                vv = T[i][y][x]
                if vv:
                    o[cx * 8 + x, cy * 8 + y] = q5(pal[vv])
    for cy in range(3, 20):
        for cx in range(1, 29):
            tile(3, cx, cy)
    for cy in range(20):
        tile(2, 0, cy), tile(2, 29, cy)
    for cx in range(1, 29):
        tile(4, cx, 2), tile(5, cx, 19), tile(5, cx, 5)
    tile(7, 28, 3), tile(6, 28, 18)
    say(im, 12, 0, "HELP", pal[1], pal[2])
    say(im, 16, 24, "DRAFT: what the HELP page", pal[1], pal[2])
    say(im, 16, 48, "says sits on the body here,", pal[1], pal[2])
    say(im, 16, 64, "the rules above and below it.", pal[1], pal[2])
    out = []
    if s is not None:                       # the theatre shot, each of the frame's colours moved to the draft's
        old = png("help_system/bg_tiles.png")[2][:16]
        swap = {mgba(q5(old[k])): q5(pal[k]) for k in (0, 10, 11, 12, 13, 14, 15)} if v else {}
        o2 = s.copy()
        q = o2.load()
        for y in range(160):
            for x in range(240):
                if q[x, y] in swap:
                    q[x, y] = swap[q[x, y]]
        out = [o2]
    return out + [im, im.crop((0, 0, 120, 80)).resize((240, 160), Image.NEAREST)]


T561_MOCKS = {"emotes": mock_emotes, "itemfinder": mock_itemfinder, "questlog": mock_questlog,
              "qldesc": mock_qldesc, "banner": mock_banner, "helpscreen": mock_helpscreen}

T561_ROWS = {
    "emotes": "Rows: Route 10, HEIDI's ! as she spots you (theatre shot, today's bubble found and the draft drawn in "
              "its place, in player.pal as on screen with MOM's shoes); the same at 3x; the full !, ? and !! over "
              "grass, sand, snow, water, night and cave at 2x and 1x; the whole sheet (15 frames) at 2x.",
    "itemfinder": "Rows: the itemfinder on Route 10 (the arrow drawn over the player as the sprite sits, rotated up "
                  "towards the berry as the affine turns it); the same at 3x; the five frames at 3x.",
    "questlog": "Rows: the recap's message box (the 240x48 the hardware draws from tiles 0-13), over the recap "
                "shot when the theatre has one; its left half at 2x.",
    "qldesc": "Rows: the recap's description bar (CopyDescriptionWindowTiles: 30x6 tiles, rows 14-19) with two "
              "lines printed as the engine prints them (white on 15, 12 shadow); its left half at 2x.",
    "banner": "Rows: the START menu with its description banner (theatre shot, the banner redrawn and its words "
              "printed again, white with the dark grey shadow, on the transparent ground); its left half at 2x.",
    "helpscreen": "Rows: today's HELP screen (theatre; for the draft, each of the frame's palette entries -- 0, "
                  "10-15 -- moved to the draft's colour, a palette-only approximation: the shot's body and ground "
                  "are both entry 0/15 today, so they take one colour); the page laid as help_system_util lays "
                  "it (body, rules, sides, scroll arrows), sample words DRAFT; its corner at 2x.",
}
T561_NOTES = {
    "emotes": "Kept: 48x80, 15 frames, three a row (pop, half, full), the rows where the code reads them; the "
              "player's OBJ palette (slot 0: the template has no palette tag), so the watch and the season tint it "
              "as before, and no palette changes. Never 12/13: T-256's shoes -- today's ! is in 12 and so has been "
              "yellow since MOM's shoes (black with DAD's). A: the follower's SMALL SCREEN (genemoji, T-431) as the "
              "trainers' -- dark glass, the glyph lit, an amber light where the follower's shows its feeling; B: A "
              "TERMINAL's frame as a paper tag, its bracket in amber; C: no bubble, the glyph ringed in ink between "
              "two amber brackets.",
    "itemfinder": "Kept: 16x80, five frames, the arrow stored pointing left with its point where today's is, four "
                  "tones in turn (frame 1 was 13, the shoes' trim: now ink ringed in paper), frame 4 the 'here' "
                  "mark. A: T-523's prompt chevron; B: today's wedge, ringed and lit; C: '<<'.",
    "questlog": "A FRAME: matched to A TERMINAL, the engine's menu_message tile for tile (T-523's, the user's pick). "
                "Kept: DLG tiles 0-13 in their places, tiles 14-19, stdpal_4 in BG palette 15 (only the quest log "
                "loads it). Why two: stdpal_4 has no near-black and no teal. 1 draws TERMINAL in stdpal_4's nearest "
                "slots (outline 10 slate teal, band 15, light 13, bracket 14, flecks 3); quest_log.png only. 2 is "
                "TERMINAL exactly and retints stdpal_4's 11-15 to stdpal_0's -- only the quest log reads stdpal_4, "
                "but 12 and 15 are also the description bar's shadow and ground, and the top and bottom bars', which "
                "go near-black with it.",
    "qldesc": "Kept: 8x24, top / middle / bottom, the middle all 15 (the text's ground); stdpal_4 as it is (shown "
              "under version 1's palette). A: a dark rule and a light hairline, the band; B: the same with a tick "
              "every 8px, as a ruler; C: the rule broken into dashes, each with a tooth (the tile repeats every 8px, so every "
              "motif here does).",
    "banner": "Kept: msg_window's 20 tiles (only 0, 5 and 14 are drawn on screen; the rest kept), stdpal_2 "
              "untouched (the slots, item PC, SEAGALLOP and menu.c's bar share it) -- so no slate: its darkest is a "
              "dark teal. A matches TERMINAL as nearly as stdpal_2 allows; an exact match needs the banner to load "
              "another palette (an engine change, not drafted).",
    "helpscreen": "A FRAME, in its own palette (bg_tiles.png's, built into bg_tiles.gbapal: only HELP loads it), so TERMINAL is matched "
                  "exactly: entry 0 (the page's ground) near-black slate, 10 near-black, 11 teal, 12 dark teal, 13 "
                  "slate, 14 the body, 15 slate; 1-9 (the text's colours) kept. The scroll arrows move from 4 (red) to "
                  "teal 11. 9 tiles in their order kept.",
}


def t561_draft(out, shots_dir=None):
    os.makedirs(out, exist_ok=True)
    shots = load_shots(shots_dir)
    made = []
    for piece in T561_PIECES:
        for d in T561_OFFERED[piece]:
            errs = t561_check(piece, d)
            if errs:
                sys.exit("gbamenus3 --t561: %s %s breaks its contract: %s" % (piece, d, "; ".join(errs)))
            put_files(t561_outputs(piece, d), os.path.join(out, d, "graphics"))
        cols = [("TODAY (the engine)", T561_MOCKS[piece](shots, None))]
        for d in T561_OFFERED[piece]:
            cols.append(("%s %s" % (d, T561_NAMES[piece][d]), T561_MOCKS[piece](shots, d)))
        notes = [T561_ROWS[piece], T561_NOTES[piece],
                 "DRAFT -- drawn in code (tools/gbamenus3.py --t561), nothing in the engine until the user picks; "
                 "recommended: %s (%s). APPROVED_561 is empty." % (T561_RECOMMENDED[piece],
                                                                  T561_NAMES[piece][T561_RECOMMENDED[piece]])]
        made.append(contact("T-561 THE FIELD OVERLAYS -- %s -- DRAFT" % piece.upper(), cols, notes,
                            os.path.join(out, "t561_%s_sheet.png" % piece)))
    return made


def t561_main():
    if ARGS.write:
        if not ARGS.approved or not (ARGS.pick or ARGS.all):
            sys.exit("gbamenus3 --t561: --write needs --approved and --all or --pick piece=X,... (the user's picks)")
        picks = dict(kv.split("=") for kv in ARGS.pick.split(",")) if ARGS.pick else dict(APPROVED_561)
        for piece, d in picks.items():
            if piece not in T561_PIECES or d not in T561_OFFERED[piece]:
                sys.exit("gbamenus3 --t561: unknown pick %s=%s" % (piece, d))
            if APPROVED_561.get(piece) != d:
                sys.exit("gbamenus3 --t561: %s=%s is not APPROVED_561 (T-561 is a DRAFT)" % (piece, d))
        for piece, d in picks.items():
            for p in put_files(t561_outputs(piece, d), G):
                print("  wrote", os.path.relpath(p, ROOT))
        return 0
    if ARGS.draft:
        out = ARGS.draft if ARGS.draft != DRAFT_DEFAULT else T561_DRAFT
        for p in t561_draft(out, ARGS.shots):
            print("  wrote", os.path.relpath(p, ROOT))
        return 0
    return t561_report()


# ================================================================================================================
# T-563: THE INDEX AND THE MAP -- the Nintendo art those screens still draw (batch 4 of the 2026-11-14 re-census).
# DRAFT: APPROVED_563 is empty, nothing is written to the engine until the user picks.
#
#     python3 tools/gbamenus3.py --t563                    # report: each piece's files, contract and APPROVED_563
#     python3 tools/gbamenus3.py --t563 --draft [DIR] [--shots DIR]   # every piece into DIR (gfx/drafts/t563_index_map/)
#     python3 tools/gbamenus3.py --t563 --write --approved --all | --pick piece=X,...   # refuses: APPROVED_563 is empty
#
# The shots are the theatre's tools/routes/t563_index_map_today.json and t563_index_map_today2.json (both folders may
# be named: --shots takes a folder and reads every PNG under it).
#
# THE PIECES, and what each drop-in keeps:
#   dexbg      pokedex/kanto_dex_bgtiles.png and national_dex_bgtiles.png, 8x256 (32 tiles each), charbase 0 of the
#              INDEX: BG3 draws from it and so does BG0 (the header and footer, tile 3 in palette 15). Every tile id
#              keeps its role, and every palette row and slot is kept (kanto/national_dex_bgpals.pal untouched):
#                0 clear; 1 solid 5 (the box paper, BG3's first fill -- and the AREA markers' window fill,
#                AREA_MARKER_TILE in src/pokedex_area_markers.c, T-530); 2 solid 3 (the habitat page's ground and
#                the lower half of its card); 3 solid 2 (the header and footer, in row 15); 4-6 the box's corner, top
#                and side (DexScreen_DrawMonDexPage and the area page: 4 and 5 flipped for the bottom); 7-11 the
#                habitat card's divider and lower corner/edge (its own, not a flip); 12 solid 7 (the entry page's
#                backdrop: T-481 B's hour on 7, kept solid); 13 solid 6; 14 the backdrop of the top menu and the
#                lists (the only tile the two editions of the sheet draw differently); 15 solid 14; 16-28 the habitat
#                page's daemon plate (page_icon_tilemap.bin, 8x8 tiles, drawn in rows 5-8 whose 2 and 8 the
#                cursor pulses: 2 the plate, 8 its rim, 3 the ground round it; 22 the fill, solid 2); 29-31 the frame
#                of the area page's NATIVE box (BG0, 0 inside: the paper shows through).
#              T-481 B: the weekday is row 0's 8 (the box's corners) and the hour its 7 (tile 12): 8 is the bracket
#              here, so the bracket is the day's trim as it is on A TERMINAL's message box; 7 stays tile 12's alone.
#              gbacalendar_ui.py index_page() reads tiles 1, 4, 5, 6 and 12 of this sheet (it follows).
#   minicard   pokedex/mini_page.png, 64x40: the habitat page's card under each daemon (CopyToWindowPixelBuffer into
#              an 8x5 window, BG1 palette 0). The engine prints over it, 0 skipped: the number at (12, 0) small, the
#              name at (2, 13), ink 1 with shadow 3, and the bound mark at (2, 3) -- so y 0-26 stays light.
#   ellipse    pokedex/blit_wide_ellipse.png, 88x16, blitted at (4, 28) of the area page's map window when a daemon
#              has no area; AREA UNKNOWN is printed over it centred, ink 1 shadow 3, at y 1 of it. Drawn in row 0.
#   heads      region_map/player_icon_red.png and player_icon_leaf.png (16x16, 4 tiles) and their .pal: the head on
#              the town map and at every GOTO. The engine picks by gSaveBlock2Ptr->playerGender, not by edition:
#              red is REASON (OBJ_EVENT_GFX_RED_NORMAL), leaf INSTINCT (GREEN_NORMAL), and both editions show the
#              same pair. Drawn from the player's own overworld frame (red_normal.png / green_normal.png, frame 0:
#              facing down) in player.pal's colours, copied into the icon's own palette (its own OBJ palette tag:
#              T-256's shoes are not painted here, so 12 and 13 are free and B uses them for the ring).
#   switch     region_map/switch_map_cursor_left.png and _right.png (32x64: two 32x32 frames, the right the left's
#              mirror, kept so) and switch_map_cursor.pal (its own): the town map's SWITCH menu's cursor.
#   famecursor fame_checker/cursor.png, 32x64, two 32x32 frames (the box round HEARSAY's chosen clue and the same
#              a pixel larger); its palette is its PNG's (cursor.gbapal), its own.
#   fameq      fame_checker/question_mark.png, 16x32: a clue not yet heard. Its template has no palette tag and
#              the code sets OBJ palette 2, which is not this screen's own -- so it is drawn in the three slots it
#              uses today (10 the face, 14 the glyph, 15 the edge) and its palette is not touched.
#
# NO NEW WORDS. Every pixel drawn in code; the engine's files read for their shape at BASE3 (pret's art there).
# ================================================================================================================
T563_DRAFT = os.path.join(ROOT, "gfx", "drafts", "t563_index_map")
T563_PIECES = ("dexbg", "minicard", "ellipse", "heads", "switch", "famecursor", "fameq")
T563_NAMES = {
    "dexbg": {"A": "GRAPH PAPER", "B": "SLATE BAND", "C": "HAIRLINE"},
    "minicard": {"A": "INDEX CARD", "B": "DOG-EAR", "C": "TICKET"},
    "ellipse": {"A": "PLATE", "B": "TAG", "C": "BRACKETS"},
    "heads": {"A": "BUST", "B": "IN A TERMINAL RING", "C": "HEAD"},
    "switch": {"A": "CUT BRACKET", "B": "PROMPT CHEVRON", "C": "AMBER TICKS"},
    "famecursor": {"A": "TEAL CUT BOX", "B": "CORNER BRACKETS", "C": "SLATE CUT BOX"},
    "fameq": {"A": "SMALL SCREEN", "B": "PAPER TAG", "C": "BARE GLYPH"},
}
T563_OFFERED = {p: "ABC" for p in T563_PIECES}
T563_RECOMMENDED = {"dexbg": "A", "minicard": "A", "ellipse": "A", "heads": "A", "switch": "A", "famecursor": "A",
                    "fameq": "A"}
APPROVED_563 = {}          # DRAFT: nothing is written until the user picks

DEXPAL = {"kanto": "pokedex/kanto_dex_bgpals.pal", "national": "pokedex/national_dex_bgpals.pal"}
DEXTILES = {"kanto": "pokedex/kanto_dex_bgtiles.png", "national": "pokedex/national_dex_bgtiles.png"}
RING_PALS = ((40, 48, 64), (56, 72, 88))   # sDexScreen_CategoryCursorPals[0..1], RGB(5,6,8) and RGB(7,9,11): at rest


def dex_rows(ed="kanto"):
    p = jpal(DEXPAL[ed])
    return [p[i * 16:(i + 1) * 16] for i in range(16)]


def dex_today(ed="kanto"):
    return [[v & 15 for v in r] for r in png(DEXTILES[ed])[3]]


def _tile_put(g, t, blk):
    for y in range(8):
        g[t * 8 + y][0:8] = list(blk[y])


def _solid(v):
    return [[v] * 8 for _ in range(8)]


def ringd(x, y, w, h, cut):
    xx, yy = min(x, w - 1 - x), min(y, h - 1 - y)
    return min(xx, yy, (xx + yy - cut) if cut else 99)


DEX_BOX = {
    #   rings from the outside in (0: the ground's 3, as pret's corner), the cut, the divider's rows, the bracket
    "A": dict(rings=[3, 14, 2], cut=2, div=[14, 2, 14], bracket=[(4, 3), (5, 3), (6, 3), (3, 4), (3, 5), (3, 6)]),
    "B": dict(rings=[3, 14, 2, 2, 12, 14], cut=2, div=[14, 2, 2, 14],
              bracket=[(4, 3), (5, 3), (6, 3), (7, 3), (3, 4), (3, 5), (3, 6), (3, 7)]),
    "C": dict(rings=[3, 3, 2], cut=3, div=[2], bracket=[(3, 3), (4, 3), (3, 4)]),
}


def box_model(d, W=5, H=7, div_row=3):
    """The habitat card as the engine lays it (5 x 7 tiles: top 4 5 5 5 4h, paper 6 1 1 1 6h, divider 7 8 8 8 7h,
    lower 9 2 2 2 9h, bottom 10 11 11 11 10h) drawn whole, so retile() cuts tiles 4-11 out of it."""
    st = DEX_BOX[d]
    w, h = W * 8, H * 8
    g = canvas(w, h, 3)
    rings = st["rings"]
    for y in range(h):
        for x in range(w):
            k = ringd(x, y, w, h, st["cut"])
            if k < 0:
                g[y][x] = 3
            elif k < len(rings):
                g[y][x] = rings[k]
            else:
                g[y][x] = 5 if y < div_row * 8 else 3
    y0 = div_row * 8
    for i, v in enumerate(st["div"]):
        for x in range(w):
            if ringd(x, y0 + i, w, h, st["cut"]) >= 1:
                g[y0 + i][x] = v
    for (bx, by) in st["bracket"]:
        for (X, Y) in ((bx, by), (w - 1 - bx, by), (bx, h - 1 - by), (w - 1 - bx, h - 1 - by)):
            g[Y][X] = 8
    if d == "C":                                   # a teal pip at each cut, the hairline's only colour
        for (X, Y) in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)):
            g[Y][X] = 15
    ents = []
    rowsT = [[(4, 0, 0)] + [(5, 0, 0)] * (W - 2) + [(4, 1, 0)]]
    rowsT += [[(6, 0, 0)] + [(1, 0, 0)] * (W - 2) + [(6, 1, 0)]] * (div_row - 1)
    rowsT += [[(7, 0, 0)] + [(8, 0, 0)] * (W - 2) + [(7, 1, 0)]]
    rowsT += [[(9, 0, 0)] + [(2, 0, 0)] * (W - 2) + [(9, 1, 0)]] * (H - div_row - 2)
    rowsT += [[(10, 0, 0)] + [(11, 0, 0)] * (W - 2) + [(10, 1, 0)]]
    for r in rowsT:
        ents += [(t, hf, vf, 0) for (t, hf, vf) in r]
    return g, ents, W


PLATE = {   # the habitat page's daemon plate, 64x64: (cut, rings from the outside in, a bracket inside the corners)
    "A": dict(cut=12, rings=[8, 2, 8], br=None),
    "B": dict(cut=6, rings=[8], br=8),
    "C": dict(cut=20, rings=[8, 8], br=None),
}


def plate_model(d):
    st = PLATE[d]
    g = canvas(64, 64, 3)
    for y in range(64):
        for x in range(64):
            k = ringd(x, y, 64, 64, st["cut"])
            if k >= 0:
                g[y][x] = st["rings"][k] if k < len(st["rings"]) else 2
    if st["br"]:
        for i in range(6):
            for (X, Y) in ((5 + i, 4), (4, 5 + i)):
                for (XX, YY) in ((X, Y), (63 - X, Y), (X, 63 - Y), (63 - X, 63 - Y)):
                    g[YY][XX] = st["br"]
    return g


FRAME = {"A": [5, 14, 2], "B": [5, 14, 2, 2], "C": [5, 5, 2]}


def frame_model(d):
    """The area page's NATIVE box frame (BG0, 29 corner, 30 top, 31 side; 0 inside), 4x4 tiles."""
    g = canvas(32, 32, 0)
    rings = FRAME[d]
    for y in range(32):
        for x in range(32):
            k = ringd(x, y, 32, 32, 2)
            if k < 0:
                g[y][x] = 5
            elif k < len(rings):
                g[y][x] = rings[k]
    if d == "B":                                   # a teal tick every 4px along the rule: a stave, as SCORE's map
        for x in range(4, 28, 4):
            g[1][x] = g[30][x] = 15
        for y in range(4, 28, 4):
            g[y][1] = g[y][30] = 15
    ents = [(29, 0, 0, 0), (30, 0, 0, 0), (30, 0, 0, 0), (29, 1, 0, 0),
            (31, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (31, 1, 0, 0),
            (31, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (31, 1, 0, 0),
            (29, 0, 1, 0), (30, 0, 1, 0), (30, 0, 1, 0), (29, 1, 1, 0)]
    return g, ents, 4


def backdrop_tile(d, ed):
    """Tile 14, the top menu's and the lists' ground: the one tile the two sheets draw differently (pret: a checker
    for Kanto, stripes for the national INDEX). Light, for the lists' dark ink; slot 4 is the one row 0 colour the
    two palettes differ in."""
    t = _solid(9)
    for y in range(8):
        for x in range(8):
            if d == "A":                           # graph paper: Kanto squared, the national INDEX ruled
                if ed == "kanto" and (x == 0 or y == 0):
                    t[y][x] = 4
                if ed == "national" and y in (0, 4):
                    t[y][x] = 4
                if ed == "kanto" and x == 0 and y == 0:
                    t[y][x] = 11
            elif d == "B":                         # a dot grid; the national INDEX's twice as fine
                if (x, y) == (0, 0):
                    t[y][x] = 11
                if ed == "national" and (x, y) in ((4, 4),):
                    t[y][x] = 11
                if ed == "kanto" and (x, y) == (4, 4):
                    t[y][x] = 4
            else:                                  # hatching, 45 degrees one way or the other
                if ed == "kanto" and (x + y) % 4 == 0:
                    t[y][x] = 4
                if ed == "national" and (x - y) % 4 == 0:
                    t[y][x] = 4
    return t


def dexbg_art(d, ed="kanto"):
    g = canvas(8, 256, 0)
    for t, v in ((1, 5), (2, 3), (3, 2), (12, 7), (13, 6), (15, 14), (22, 2)):
        _tile_put(g, t, _solid(v))
    _tile_put(g, 14, backdrop_tile(d, ed))
    bm, be, bw = box_model(d)
    M.retile(g, 1, [(be, bw, bm)])
    pm = plate_model(d)
    M.retile(g, 1, [(map16("pokedex/page_icon_tilemap.bin"), 8, pm)])
    fm, fe, fw = frame_model(d)
    M.retile(g, 1, [(fe, fw, fm)])
    for t in (1, 2, 3, 12, 13, 15, 22, 25, 26, 27):    # the solid tiles stay solid whatever the votes said; 25-27
        _tile_put(g, t, _solid({1: 5, 2: 3, 3: 2, 12: 7, 13: 6, 15: 14, 22: 2}.get(t, 2)))   # no map names: the fill
    return g


# ------------------------------------------------------------------------------------------------ the mini card
def minicard_art(d):
    g = canvas(64, 40, 0)
    if d == "A":       # INDEX CARD: slate rule cut at 45, paper, a dark rule, a ruled lower band, the bracket
        cut_box(g, 0, 0, 64, 40, 2, [2], 5)
        fill(g, 1, 26, 63, 27, 14)
        fill(g, 1, 27, 63, 39, 3)
        for y in (30, 33, 36):
            fill(g, 3, y, 61, y + 1, 11)
        for (x, y) in ((2, 2), (3, 2), (4, 2), (2, 3), (2, 4)):
            put(g, x, y, 8)
        for (x, y) in ((61, 37), (60, 37), (59, 37), (61, 36), (61, 35)):
            put(g, x, y, 8)
        cut_box(g, 0, 0, 64, 40, 2, [2])
    elif d == "B":     # DOG-EAR: the top-right corner folded at 45, slate rule, graph paper below
        cut_box(g, 0, 0, 64, 40, 1, [2], 5)
        for y in range(8):
            for x in range(64 - 8 + y, 64):
                g[y][x] = 0
            g[y][64 - 8 + y] = 2
            for x in range(56, 64 - 8 + y):
                if y < 8 and x >= 56:
                    pass
        for i in range(7):                         # the fold: a triangle of the lower band's colour
            for x in range(56, 56 + i + 1):
                g[1 + i][x] = 3 if x < 56 + i else 2
        fill(g, 1, 26, 63, 27, 2)
        fill(g, 1, 27, 63, 39, 9)
        for y in range(27, 39):
            for x in range(1, 63):
                if (x % 4 == 0) or (y - 27) % 4 == 0:
                    g[y][x] = 11
    else:              # TICKET: notches at the tear line, the tear line dashed, a teal hairline under the name
        cut_box(g, 0, 0, 64, 40, 0, [2], 5)
        fill(g, 1, 27, 63, 39, 3)
        for x in range(2, 62, 3):
            put(g, x, 26, 12)
        for (x, y) in ((0, 25), (0, 26), (0, 27), (1, 26), (63, 25), (63, 26), (63, 27), (62, 26)):
            put(g, x, y, 0)
        fill(g, 3, 37, 61, 38, 15)
    return g


# ------------------------------------------------------------------------------------------------ the ellipse
def ellipse_art(d):
    g = canvas(88, 16, 0)
    if d == "A":       # PLATE: paper on a slate rule cut at 45, the day's bracket at each end
        cut_box(g, 0, 0, 88, 16, 3, [14, 3], 5)
        for (x, y) in ((4, 2), (5, 2), (3, 3), (3, 4)):
            put(g, x, y, 8), put(g, 87 - x, 15 - y, 8)
    elif d == "B":     # TAG: pointed ends, a slate rule
        for y in range(16):
            e = abs(y * 2 - 15) // 2               # 0 at the middle rows, 7 at the top and bottom
            for x in range(e, 88 - e):
                k = min(x - e, 87 - e - x, y, 15 - y)
                g[y][x] = 2 if k == 0 else 5
    else:              # BRACKETS: open ends, two rules and a teal bracket at each end
        fill(g, 6, 1, 82, 15, 5)
        fill(g, 6, 0, 82, 1, 2), fill(g, 6, 15, 82, 16, 2)
        for x0, s in ((1, 1), (86, -1)):
            for y in range(1, 15):
                put(g, x0, y, 15)
            for i in range(3):
                put(g, x0 + s * (i + 1), 1, 15), put(g, x0 + s * (i + 1), 14, 15)
    return g


# ------------------------------------------------------------------------------------------------ the heads
PLAYER_SHEETS = {"red": "object_events/pics/people/red_normal.png", "leaf": "object_events/pics/people/green_normal.png"}
WHO = {"red": "REASON", "leaf": "INSTINCT"}


def player_frame0(which):
    w, h, pal, px = png(PLAYER_SHEETS[which])
    return [[px[y][x] & 15 for x in range(16)] for y in range(32)]


def heads_pal(d):
    p = list(jpal(OBJ_PAL))[:16]
    if d == "B":
        p[12], p[13] = TEAL, SLATE_OUT
    return p


def head_art(d, which):
    f = player_frame0(which)
    g = canvas(16, 16, 0)
    if d == "A":       # BUST: the overworld frame's rows 9-24 as they are -- hat, face, the coat's top, the tail
        for y in range(16):
            g[y] = list(f[9 + y])
    elif d == "B":     # IN A TERMINAL RING: a dark plate with a teal rim behind the head; the brim breaks it
        cut_box(g, 1, 4, 14, 12, 3, [12], 13)
        for y in range(13):
            for x in range(16):
                v = f[9 + y][x]
                if v and 1 + y < 16:
                    g[1 + y][x] = v
    else:              # HEAD: the hat and face alone, centred
        for y in range(11):
            for x in range(16):
                g[3 + y][x] = f[9 + y][x]
    return g


# ------------------------------------------------------------------------------------------------ switch cursor
SWITCH_PALS = {"A": {1: TEAL, 2: SLATE_OUT}, "B": {1: PAPER, 2: SLATE_OUT, 3: TEAL}, "C": {1: AMBER, 2: SLATE_OUT}}


def switch_pal(d):
    p = list(jpal("region_map/switch_map_cursor.pal"))[:16]
    if d:
        for k, c in SWITCH_PALS[d].items():
            p[k] = c
    return p


def _outline(g, v, under=0):
    """Ring every drawn pixel with `v` where it meets the clear, 8-neighbour."""
    h, w = len(g), len(g[0])
    add = []
    for y in range(h):
        for x in range(w):
            if g[y][x] == under:
                if any(0 <= y + dy < h and 0 <= x + dx < w and g[y + dy][x + dx] not in (under, v)
                       for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                    add.append((x, y))
    for x, y in add:
        g[y][x] = v


def switch_left(d):
    """The left half: frame 0 (rows 0-31) the bracket's outer pair, frame 1 (32-63) 2px in, as pret's."""
    g = canvas(32, 64, 0)
    for f, ins in ((0, 0), (1, 2)):
        sub = canvas(32, 32, 0)
        x0, y0, y1 = 16 + ins, 0 + ins, 31 - ins
        if d == "A":                   # an L each end, 2px, its corner cut at 45
            for k in range(2):
                for x in range(x0 + 2, 32 - ins - 1):
                    put(sub, x, y0 + 1 + k, 1), put(sub, x, y1 - 1 - k, 1)
                for y in range(y0 + 3, y0 + 8):
                    put(sub, x0 + 1 + k, y, 1), put(sub, x0 + 1 + k, y1 - (y - y0), 1)
            put(sub, x0 + 2, y0 + 2, 1), put(sub, x0 + 2, y1 - 2, 1)
            _outline(sub, 2)
        elif d == "B":                 # a chevron pointing in, with a short rule above and below
            cy = 15
            for i in range(5):
                for t in range(2):
                    put(sub, x0 + 2 + i + t, cy - 4 + i, 3), put(sub, x0 + 2 + i + t, cy + 5 - i, 3)
            for x in range(x0 + 2, x0 + 10):
                put(sub, x, y0 + 1, 1), put(sub, x, y1 - 1, 1)
            _outline(sub, 2)
        else:                          # thin ticks in amber with a slate shadow below and right
            for x in range(x0 + 1, x0 + 9):
                put(sub, x, y0 + 1, 1), put(sub, x, y1 - 2, 1)
            for y in range(y0 + 1, y0 + 6):
                put(sub, x0 + 1, y, 1), put(sub, x0 + 1, y1 - 2 - (y - y0 - 1), 1)
            sh = [r[:] for r in sub]
            for y in range(32):
                for x in range(32):
                    if sh[y][x] == 1 and y + 1 < 32 and x + 1 < 32 and sub[y + 1][x + 1] == 0:
                        sub[y + 1][x + 1] = 2
        for y in range(32):
            g[f * 32 + y] = sub[y]
    return [r[16:] + [0] * 16 if False else r for r in g]


def switch_art(d):
    left = switch_left(d)
    # pret's left half is drawn at x 0-15 of its 32 (the right half is the mirror): keep both where they were
    L = [r[16:] + r[:16] for r in left]
    return L, [r[::-1] for r in L]


# ------------------------------------------------------------------------------------------------ HEARSAY
def fame_cursor_pal(d):
    p = png("fame_checker/cursor.png")[2][:16]
    if d == "A":
        p[14], p[15] = SLATE_OUT, TEAL
    elif d == "B":
        p[14], p[15] = SLATE_OUT, TEAL
    elif d == "C":
        p[14], p[15] = (232, 236, 240), SLATE_OUT
    return p


def _bbox(g, y0, y1):
    pts = [(x, y) for y in range(y0, y1) for x, v in enumerate(g[y]) if v]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def fame_cursor_art(d):
    now = [[v & 15 for v in r] for r in png("fame_checker/cursor.png")[3]]
    g = canvas(32, 64, 0)
    for f in (0, 1):
        x0, y0, x1, y1 = _bbox(now, f * 32, f * 32 + 32)
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if d == "A":
            cut_box(g, x0, y0, w, h, 3, [14, 15, 14])
        elif d == "B":
            for k in range(6):
                for (X, Y) in ((x0 + k, y0), (x0, y0 + k), (x1 - k, y0), (x1, y0 + k),
                               (x0 + k, y1), (x0, y1 - k), (x1 - k, y1), (x1, y1 - k)):
                    put(g, X, Y, 15)
            for k in range(6):
                for (X, Y) in ((x0 + 1 + k, y0 + 1), (x0 + 1, y0 + 1 + k), (x1 - 1 - k, y0 + 1), (x1 - 1, y0 + 1 + k),
                               (x0 + 1 + k, y1 - 1), (x0 + 1, y1 - 1 - k), (x1 - 1 - k, y1 - 1), (x1 - 1, y1 - 1 - k)):
                    if g[Y][X] == 0:
                        put(g, X, Y, 14)
        else:
            cut_box(g, x0, y0, w, h, 2, [14, 15, 15, 14])
    return g


QGLYPH = [".####.", "##..##", "....##", "...##.", "..##..", "..##..", "......", "..##..", "..##.."]


def fameq_art(d):
    g = canvas(16, 32, 0)
    # pret's tile: rows 12-30, x 1-14 (14 x 19)
    if d == "A":       # SMALL SCREEN: dark glass (10) cut at 45, a 15 edge, the ? lit (14)
        cut_box(g, 1, 12, 14, 19, 3, [15], 10)
        gx, gy = 5, 17
    elif d == "B":     # PAPER TAG: the face light (14), a 15 rule, the ? in 10, a punched hole
        cut_box(g, 1, 12, 14, 19, 2, [15], 14)
        put(g, 7, 14, 15), put(g, 8, 14, 15)
        gx, gy = 5, 18
    else:              # BARE GLYPH: no plate, the ? ringed in 15
        gx, gy = 5, 17
    for y, row in enumerate(QGLYPH):
        for x, c in enumerate(row):
            if c == "#":
                put(g, gx + x, gy + y, 10 if d == "B" else 14)
    if d == "C":
        _outline(g, 15)
    return g


# ------------------------------------------------------------------------------------------------ outputs and checks
def t563_outputs(piece, d):
    if piece == "dexbg":
        return {DEXTILES[ed]: _png(dexbg_art(d, ed), dex_rows(ed)[0]) for ed in ("kanto", "national")}
    if piece == "minicard":
        return {"pokedex/mini_page.png": _png(minicard_art(d), dex_rows()[0])}
    if piece == "ellipse":
        return {"pokedex/blit_wide_ellipse.png": _png(ellipse_art(d), dex_rows()[0])}
    if piece == "heads":
        out = {}
        for which in ("red", "leaf"):
            out["region_map/player_icon_%s.png" % which] = _png(head_art(d, which), heads_pal(d))
            out["region_map/player_icon_%s.pal" % which] = ("pal", heads_pal(d))
        return out
    if piece == "switch":
        L, R = switch_art(d)
        return {"region_map/switch_map_cursor_left.png": _png(L, switch_pal(d)),
                "region_map/switch_map_cursor_right.png": _png(R, switch_pal(d)),
                "region_map/switch_map_cursor.pal": ("pal", switch_pal(d))}
    if piece == "famecursor":
        return {"fame_checker/cursor.png": _png(fame_cursor_art(d), fame_cursor_pal(d))}
    if piece == "fameq":
        return {"fame_checker/question_mark.png": _png(fameq_art(d), png("fame_checker/question_mark.png")[2][:16])}
    return {}


SIZES = {"pokedex/kanto_dex_bgtiles.png": (8, 256), "pokedex/national_dex_bgtiles.png": (8, 256),
         "pokedex/mini_page.png": (64, 40), "pokedex/blit_wide_ellipse.png": (88, 16),
         "region_map/player_icon_red.png": (16, 16), "region_map/player_icon_leaf.png": (16, 16),
         "region_map/switch_map_cursor_left.png": (32, 64), "region_map/switch_map_cursor_right.png": (32, 64),
         "fame_checker/cursor.png": (32, 64), "fame_checker/question_mark.png": (16, 32)}


def t563_check(piece, d):
    errs = []
    for rel, payload in t563_outputs(piece, d).items():
        if payload[0] != "png":
            continue
        g = payload[1]
        if (len(g[0]), len(g)) != SIZES[rel]:
            errs.append("%s is %dx%d, not %dx%d" % ((rel, len(g[0]), len(g)) + SIZES[rel]))
        used = {v for r in g for v in r}
        if piece == "dexbg":
            T = lambda t: {v for r in g[t * 8:t * 8 + 8] for v in r}
            for t, v in ((1, 5), (2, 3), (3, 2), (12, 7), (22, 2)):
                if T(t) != {v}:
                    errs.append("%s tile %d is not solid %d" % (rel, t, v))
            if any(7 in T(t) for t in range(32) if t != 12):
                errs.append("%s draws 7 (T-481 B's hour) outside tile 12" % rel)
            if any(T(t) - {2, 3, 8} for t in range(16, 29)):
                errs.append("%s: the plate (16-28) draws outside 2, 3 and 8 (rows 5-8: the cursor's pulse)" % rel)
            if T(0) != {0}:
                errs.append("%s tile 0 is not clear" % rel)
        if piece == "minicard":
            if any(v in (1,) for r in g for v in r):
                errs.append("draws in 1 (the ink)")
            if any(v not in (5, 8) for r in g[3:26] for v in r[2:54]):
                errs.append("the text's rows (3-25, x 2-53) are not paper")
        if piece == "ellipse" and any(v in (1, 7) for r in g for v in r):
            errs.append("draws in 1 (the ink) or 7 (the hour)")
        if piece == "fameq" and used - {0, 10, 14, 15}:
            errs.append("draws outside 10/14/15 (OBJ palette 2 is not this screen's)")
        if piece == "switch" and used - {0, 1, 2, 3}:
            errs.append("draws outside 1-3")
    if piece == "switch":
        L, R = switch_art(d)
        if R != [r[::-1] for r in L]:
            errs.append("the right half is not the left's mirror")
    return errs


def t563_differs(picks):
    out = []
    for piece, d in picks.items():
        for rel, payload in t563_outputs(piece, d).items():
            p = os.path.join(G, rel)
            if payload[0] == "png":
                try:
                    import gbafont
                    w, h, bd, plte, px = gbafont.png_load(p)
                    if [[v & 15 for v in r] for r in px] != [list(r) for r in payload[1]]:
                        out.append(rel)
                except BaseException:
                    out.append(rel)
            elif payload[0] == "pal" and [q5(c) for c in M.jasc(p)] != [q5(c) for c in payload[1]]:
                out.append(rel)
    return out


def t563_report():
    print("gbamenus3 --t563 (T-563): the INDEX and the map. APPROVED_563: %s" % (APPROVED_563 or "none -- nothing is written"))
    bad = 0
    for piece in T563_PIECES:
        print("  %-10s %s" % (piece, ", ".join(sorted(t563_outputs(piece, "A")))))
        for d in T563_OFFERED[piece]:
            errs = t563_check(piece, d)
            if errs:
                bad += 1
                print("    %s %s: %s" % (d, T563_NAMES[piece][d], "; ".join(errs)))
    drift = t563_differs(APPROVED_563)
    for rel in drift:
        print("  DRIFT: engineGba/graphics/%s is not what --t563 --write --approved --all makes" % rel)
    return 1 if bad or drift else 0


# ------------------------------------------------------------------------------------------------ the real screens
def _layer_from_map(sheet, entries, w, rows_of, x0=0, y0=0, layer=None):
    """Index layer (240x160 of (row, idx) or None) of a tilemap drawn at tile (x0, y0)."""
    L = layer or [[None] * 240 for _ in range(160)]
    for i, (t, hf, vf, pn) in enumerate(entries):
        cx, cy = x0 + i % w, y0 + i // w
        if not (0 <= cx < 30 and 0 <= cy < 20):
            continue
        blk = tile_of(sheet, t, 1)
        for y in range(8):
            for x in range(8):
                v = blk[7 - y if vf else y][7 - x if hf else x]
                if v:
                    L[cy * 8 + y][cx * 8 + x] = (rows_of(pn), v)
    return L


def _fill_ents(t, w, h, pn=0):
    return [(t, 0, 0, pn)] * (w * h)


def habitat_n(s):
    """How many daemons the habitat shot's page holds: the layout whose plates the shot covers best (dark there)."""
    best = None
    for n in (1, 2, 3, 4):
        o = dex_layers(dex_today(), "habitat", (n, HAB_COORDS[n]))
        pts = [(x, y) for y in range(0, 160, 2) for x in range(0, 240, 2) if o[y][x] and o[y][x][0] >= 5]
        frac = sum(1 for (x, y) in pts if sum(s.getpixel((x, y))) < 250) / max(1, len(pts))
        if best is None or frac > best[0] + 0.02:
            best = (frac, n)
    return best[1]


def card_grid(d):
    return minicard_art(d) if d else [[v & 15 for v in r] for r in png("pokedex/mini_page.png")[3]]


def dex_layers(sheet, page, extra=None, cards=None):
    """The INDEX's BG3 (and the area page's BG0 frame) as the engine lays them for `page`, from `sheet`."""
    L = [[None] * 240 for _ in range(160)]
    if page in ("top", "list"):
        L = _layer_from_map(sheet, _fill_ents(14, 30, 20), 30, lambda r: 0, layer=L)
    elif page in ("entry", "area"):
        L = _layer_from_map(sheet, _fill_ents(12, 30, 20), 30, lambda r: 0, layer=L)
        W, H, x0, y0 = 28, 14, 0, 2
        ents = []
        for y in range(H + 2):
            for x in range(W + 2):
                top, bot, lft, rgt = y == 0, y == H + 1, x == 0, x == W + 1
                if (top or bot) and (lft or rgt):
                    ents.append((4, int(rgt), int(bot), 0))
                elif top or bot:
                    ents.append((5, 0, int(bot), 0))
                elif lft or rgt:
                    ents.append((6, int(rgt), 0, 0))
                else:
                    ents.append((1, 0, 0, 0))
        L = _layer_from_map(sheet, ents, W + 2, lambda r: 0, x0, y0, L)
        if page == "area":
            W, H, x0, y0 = 10, 6, 1, 9
            ents = []
            for y in range(H + 2):
                for x in range(W + 2):
                    top, bot, lft, rgt = y == 0, y == H + 1, x == 0, x == W + 1
                    if (top or bot) and (lft or rgt):
                        ents.append((29, int(rgt), int(bot), 0))
                    elif top or bot:
                        ents.append((30, 0, int(bot), 0))
                    elif lft or rgt:
                        ents.append((31, int(rgt), 0, 0))
                    else:
                        ents.append((0, 0, 0, 0))
            L = _layer_from_map(sheet, ents, W + 2, lambda r: 0, x0, y0, L)
    elif page == "habitat":
        L = _layer_from_map(sheet, _fill_ents(2, 30, 20), 30, lambda r: 0, layer=L)
        n, coords = extra
        icon = map16("pokedex/page_icon_tilemap.bin")
        for slot in range(n):
            cx, cy, mx, my = coords[slot]
            L = _layer_from_map(sheet, icon, 8, lambda r, s=slot: 5 + s, cx, cy, L)
            if cards is not None:                       # the card is a window on BG1, over the ground
                g = card_grid(cards if cards else None)
                for y in range(40):
                    for x in range(64):
                        X, Y = mx * 8 + x, my * 8 + y
                        if g[y][x] and X < 240 and Y < 160:
                            L[Y][X] = (0, g[y][x])
    return L


HAB_COORDS = {1: [(11, 3, 11, 11)], 2: [(3, 3, 11, 3), (18, 9, 10, 11)],
              3: [(1, 2, 9, 2), (11, 9, 3, 11), (21, 3, 21, 11)],
              4: [(0, 2, 6, 3), (7, 10, 0, 12), (15, 10, 22, 11), (22, 2, 15, 4)]}


def _rgb_rows(ed="kanto"):
    rows = [list(r) for r in dex_rows(ed)]
    for r in (5, 6, 7, 8):
        rows[r][2], rows[r][8] = RING_PALS
    return rows


def relayer(shot_im, today, draft, rows, today_card=None, draft_card=None):
    """Replace, in a theatre shot, every pixel the old layer drew (the shot's colour there is the one the old
    layer's index shows elsewhere) with the draft layer's pixel. The colour of each (row, index) is read off the shot
    itself, so the hour's and the weekday's run-time colours carry over."""
    from collections import Counter
    out = shot_im.copy()
    p = out.load()
    seen = {}
    for y in range(160):
        for x in range(240):
            k = today[y][x]
            if k:
                seen.setdefault(k, Counter())[p[x, y]] += 1
    cm = {k: c.most_common(1)[0][0] for k, c in seen.items()}
    for y in range(160):
        for x in range(240):
            k, n = today[y][x], draft[y][x]
            if k and p[x, y] == cm[k]:
                if n:
                    p[x, y] = cm.get(n) or mgba(q5(rows[n[0]][n[1]]))
    return out


def render_layer(L, rows, bg=(0, 0, 0)):
    im = Image.new("RGB", (240, 160), bg)
    p = im.load()
    for y in range(160):
        for x in range(240):
            if L[y][x]:
                r, v = L[y][x]
                p[x, y] = mgba(q5(rows[r][v]))
    return im


def mock_dexbg(shots, d):
    imgs = []
    for keys, page, ed in ((("the INDEX", "the list"), "list", "kanto"), (("GLOBAL INDEX", "the list"), "list", "national"),
                           (("the INDEX", "an entry"), "entry", "kanto"), (("the area page",), "area", "kanto")):
        s = shot(shots, *keys)
        old = dex_layers(dex_today(ed), page)
        new = dex_layers(dexbg_art(d, ed), page) if d else old
        rows = _rgb_rows(ed)
        if s is not None:
            imgs.append(relayer(s, old, new, rows))
        else:
            imgs.append(render_layer(new, rows))
    # the habitat page: the plates and the cards, laid as the shot has them (1-4 daemons on the page)
    s = shot(shots, "habitat page", "plates")
    n = habitat_n(s) if s is not None else 4
    old = dex_layers(dex_today(), "habitat", (n, HAB_COORDS[n]), cards=None)
    new = dex_layers(dexbg_art(d) if d else dex_today(), "habitat", (n, HAB_COORDS[n]), cards=None)
    rows = _rgb_rows()
    imgs.append(relayer(s, old, new, rows) if s is not None else card_over(render_layer(new, rows), None, None, n))
    imgs.append(tiles_plate(d))
    return imgs


def tiles_plate(d):
    """Every tile of both sheets at 3x: Kanto above, the national INDEX below (rows 5-8's tiles in row 5)."""
    im = Image.new("RGB", (240, 160), (36, 40, 46))
    for k, ed in enumerate(("kanto", "national")):
        sheet = dexbg_art(d, ed) if d else dex_today(ed)
        r0 = _rgb_rows(ed)
        for t in range(32):
            pal_row = 15 if t == 3 else (5 if 16 <= t <= 28 else 0)
            blk = tile_of(sheet, t, 1)
            ti = Image.new("RGB", (8, 8), (255, 0, 255))
            for y in range(8):
                for x in range(8):
                    if blk[y][x]:
                        ti.putpixel((x, y), mgba(q5(r0[pal_row][blk[y][x]])))
            ti = ti.resize((24, 24), Image.NEAREST)
            im.paste(ti, (4 + (t % 9) * 26, 2 + k * 80 + (t // 9) * 26))
    return im


def card_over(base, d, which=None, n=4):
    """The mini cards laid where the habitat page puts them (rectangular window x/y), with a name printed."""
    out = base.copy()
    g = minicard_art(d) if d else [[v & 15 for v in r] for r in png("pokedex/mini_page.png")[3]]
    r0 = _rgb_rows()[0]
    names = ["ROVERCUB", "LABEL", "CANON", "LOCUS"]
    for slot in range(n):
        mx, my = HAB_COORDS[n][slot][2], HAB_COORDS[n][slot][3]
        c = idx_rgba(g, r0)
        out.paste(c, (mx * 8, my * 8), c)
        say(out, mx * 8 + 12, my * 8 - 2, "No%03d" % (slot * 3 + 1), r0[1], r0[3], small=True)
        say(out, mx * 8 + 2, my * 8 + 13 - 2, names[slot], r0[1], r0[3])
    return out


def mock_minicard(shots, d):
    s = shot(shots, "habitat page", "plates")
    imgs = []
    rows = _rgb_rows()
    if s is not None:                                    # today's cards lifted out of the shot, the draft's laid in
        n = habitat_n(s)
        old = dex_layers(dex_today(), "habitat", (n, HAB_COORDS[n]), cards="")
        new = dex_layers(dex_today(), "habitat", (n, HAB_COORDS[n]), cards=d or "")
        base = relayer(s, old, new, rows)
        mx, my = HAB_COORDS[n][0][2], HAB_COORDS[n][0][3]
        imgs.append(base)
        imgs.append(base.crop((mx * 8 - 8, my * 8 - 8, mx * 8 + 72, my * 8 + 45)).resize((240, 160), Image.NEAREST))
    else:
        one = card_over(render_layer(dex_layers(dex_today(), "habitat", (1, HAB_COORDS[1])), rows), d, None, 1)
        imgs += [one, one.crop((80, 80, 160, 133)).resize((240, 160), Image.NEAREST)]
    return imgs


def ellipse_now():
    d = open(os.path.join(G, "pokedex/blit_wide_ellipse.4bpp"), "rb").read()
    g = canvas(88, 16, 0)
    for t in range(22):
        tx, ty = t % 11, t // 11
        for i in range(32):
            b = d[t * 32 + i]
            y, x = i // 4, (i % 4) * 2
            g[ty * 8 + y][tx * 8 + x] = b & 15
            g[ty * 8 + y][tx * 8 + x + 1] = b >> 4
    return g


def mock_ellipse(shots, d):
    s = shot(shots, "the area page")
    r0 = _rgb_rows()[0]
    g = ellipse_art(d) if d else ellipse_now()
    base = s.copy() if s is not None else _blank()
    old = ellipse_now()
    #  sWindowTemplate_AreaMap_Kanto is at tile (17, 4), moved down 4 tiles unless a later island is open
    cands = [(136 + 4, (4 + v) * 8 + 28) for v in (4, 0)]
    white = mgba(q5(r0[5]))
    score = lambda c: sum(1 for yy in range(16) for xx in range(88) if old[yy][xx] == 5
                          and base.getpixel((c[0] + xx, c[1] + yy)) == white)
    x, y = max(cands, key=score)
    hits = [(x, y)] if s is not None else []
    if d and hits:                                       # lift today's off: the map under it is the sea, dark
        p = base.load()
        under = base.getpixel((x + 2, y - 2))
        for yy in range(16):
            for xx in range(88):
                if old[yy][xx]:
                    p[x + xx, y + yy] = under
        base = _over(base, g, r0, x, y)
        t = "AREA UNKNOWN"
        tw = text_width(t, True)
        say(base, x - 4 + (96 - tw) // 2, y + 1 - 2, t, r0[1], r0[3], small=True)
    return [base, base.crop((x - 20, y - 20, x + 100, y + 60)).resize((240, 160), Image.NEAREST)]


def find_by_colour(img, g, pal):
    """Where index grid g sits in img, matching each index's own colour exactly (mGBA's widening): the offset most of
    its pixels agree with -- a sprite half covered by another still lands where it is."""
    from collections import Counter
    p = img.load()
    pts = [(x, y, mgba(q5(pal[v]))) for y, r in enumerate(g) for x, v in enumerate(r) if v]
    rare = Counter(c for _, _, c in pts)
    there = Counter(p[X, Y] for Y in range(160) for X in range(240))
    cand = [t for t in pts if there[t[2]]]
    if not cand:
        return []
    ax, ay, ac = min(cand, key=lambda t: (there[t[2]], rare[t[2]]))
    best = None
    for Y in range(160):
        for X in range(240):
            if p[X, Y] != ac:
                continue
            ox, oy = X - ax, Y - ay
            n = sum(1 for (x, y, c) in pts if 0 <= ox + x < 240 and 0 <= oy + y < 160 and p[ox + x, oy + y] == c)
            if best is None or n > best[0]:
                best = (n, ox, oy)
    return [best[1:]] if best and best[0] >= 8 else []


def mock_heads(shots, d):
    """The head as the GOTO map shows it: found by its top rows (the town's GOTO ring is drawn over its lower half),
    lifted where it shows, the draft laid in under whatever covers it."""
    s = shot(shots, "GOTO map", "head")
    imgs = []
    which = "red"
    old = [[v & 15 for v in r] for r in png("region_map/player_icon_%s.png" % which)[3]]
    opal = png("region_map/player_icon_%s.png" % which)[2][:16]
    base = s.copy() if s is not None else _blank()
    cap = [[v if v == 11 else 0 for v in r] for r in old]          # the cap's red: the part the town's ring leaves
    hits = find_by_colour(base, cap, opal) if s is not None else []
    x, y = hits[0] if hits else (100, 70)
    if d and s is not None:                    # lift today's head (its 16x16, filled from the paper round it), lay
        p = base.load()                        # the draft over it whole
        ring = [base.getpixel((xx, max(0, y - 1))) for xx in range(x, x + 16)]
        under = max(set(ring), key=ring.count)
        for yy in range(16):
            for xx in range(16):
                if old[yy][xx] and base.getpixel((x + xx, y + yy)) != under and yy < 9:
                    p[x + xx, y + yy] = under
        base = _over(base, head_art(d, which), heads_pal(d), x, y)
    imgs.append(base)
    zx, zy = max(0, min(160, x - 32)), max(0, min(107, y - 18))
    imgs.append(base.crop((zx, zy, zx + 80, zy + 53)).resize((240, 160), Image.NEAREST))
    pl = []
    for w in ("red", "leaf"):
        if d:
            pl.append(idx_rgba(head_art(d, w), heads_pal(d)))
        else:
            pl.append(idx_rgba([[v & 15 for v in r] for r in png("region_map/player_icon_%s.png" % w)[3]],
                               png("region_map/player_icon_%s.png" % w)[2][:16]))
    ow = [idx_rgba(player_frame0(w), list(jpal(OBJ_PAL))[:16]) for w in ("red", "leaf")]
    imgs.append(parts_plate([pl[0], ow[0], pl[1], ow[1]], k=3, bg=(96, 112, 128)))
    return imgs


def mock_switch(shots, d):
    s = shot(shots, "SWITCH menu", "its cursor")
    old_l = [[v & 15 for v in r] for r in png("region_map/switch_map_cursor_left.png")[3]]
    old_r = [r[::-1] for r in old_l]
    L, R = switch_art(d) if d else (old_l, old_r)
    pal = switch_pal(d) if d else switch_pal(None)
    imgs = []
    base = s.copy() if s is not None else _blank()
    if s is not None:
        hits = find_shape(base, old_l[:32], slack=4)
        if hits:
            x, y = hits[0]
            hr = find_shape(base, old_r[:32], slack=4)
            xr, yr = hr[0] if hr else (x + 64, y)
            if d:
                p = base.load()
                for (ox, oy, og) in ((x, y, old_l[:32]), (xr, yr, old_r[:32])):
                    for yy in range(32):
                        for xx in range(32):
                            if og[yy][xx] and 0 <= ox + xx < 240 and 0 <= oy + yy < 160:
                                p[ox + xx, oy + yy] = base.getpixel((ox + xx, max(0, oy - 1)))
                base = _over(base, L[:32], pal, x, y)
                base = _over(base, R[:32], pal, xr, yr)
            imgs.append(base)
            imgs.append(base.crop((max(0, x - 16), max(0, y - 16), max(0, x - 16) + 120,
                                   max(0, y - 16) + 80)).resize((240, 160), Image.NEAREST))
        else:
            imgs += [base, base]
    else:                                               # the SWITCH menu not reached: laid over the GOTO map where
        g = shot(shots, "GOTO map", "head") or _blank()  # the menu's cursor sits (subsprites at x 88 and 152)
        base = g.copy()
        base = _over(base, L[:32], pal, 88 - 16, 56)       # a 32x32 sprite's x is its centre
        base = _over(base, R[:32], pal, 152 - 16, 56)
        imgs += [base, base.crop((56, 40, 216, 147)).resize((240, 160), Image.NEAREST)]
    fr = [idx_rgba(L[:32], pal), idx_rgba(R[:32], pal), idx_rgba(L[32:], pal), idx_rgba(R[32:], pal)]
    imgs.append(parts_plate(fr, k=2, bg=(72, 96, 120)))
    return imgs


def mock_famecursor(shots, d):
    s = shot(shots, "HEARSAY", "the cursor") or shot(shots, "HEARSAY", "six")
    old = [[v & 15 for v in r] for r in png("fame_checker/cursor.png")[3]]
    opal = png("fame_checker/cursor.png")[2][:16]
    g = fame_cursor_art(d) if d else old
    pal = fame_cursor_pal(d) if d else opal
    base = s.copy() if s is not None else _blank()
    hits = find_by_colour(base, old[:32], opal) if s is not None else []
    x, y = hits[0] if hits else (100, 30)
    if d and hits:                             # lift today's box: each pixel takes the one just outside the box
        p = base.load()
        x0, y0, x1, y1 = _bbox(old, 0, 32)
        for yy in range(32):
            for xx in range(32):
                if old[yy][xx]:
                    sx = x + (x0 - 1 if xx - x0 < x1 - xx else x1 + 1)
                    p[x + xx, y + yy] = base.getpixel((sx, y + yy)) if (yy - y0 > 0 and y1 - yy > 0) else \
                        base.getpixel((x + xx, y + (y0 - 1 if yy - y0 <= 0 else y1 + 1)))
        base = _over(base, g[:32], pal, x, y)
    zx, zy = max(0, min(160, x - 24)), max(0, min(107, y - 10))
    return [base, base.crop((zx, zy, zx + 80, zy + 53)).resize((240, 160), Image.NEAREST),
            parts_plate([idx_rgba(g[:32], pal), idx_rgba(g[32:], pal)], k=3, bg=(232, 208, 96))]


def mock_fameq(shots, d):
    """No ? was on film: the debug save has heard every clue. So the ? is laid where a clue's picture stands (the
    one the cursor holds in the shot), in question_mark.png's own colours -- a stand-in for OBJ palette 2's."""
    s = shot(shots, "HEARSAY", "the cursor") or shot(shots, "HEARSAY", "six")
    old = [[v & 15 for v in r] for r in png("fame_checker/question_mark.png")[3]]
    g = fameq_art(d) if d else old
    pal = png("fame_checker/question_mark.png")[2][:16]
    base = s.copy() if s is not None else _blank()
    oc = [[v & 15 for v in r] for r in png("fame_checker/cursor.png")[3]]
    hits = find_by_colour(base, oc[:32], png("fame_checker/cursor.png")[2][:16]) if s is not None else []
    cx, cy = hits[0] if hits else (100, 30)
    bx0, by0, bx1, by1 = _bbox(oc, 0, 32)
    mx, my = cx + (bx0 + bx1) // 2, cy + (by0 + by1) // 2      # the clue's picture's centre
    x, y = mx - 8, my - 21
    p = base.load()
    ground = base.getpixel((cx + bx0 - 3, my))
    for yy in range(by0 + 1, by1):                              # the clue's picture taken off, the ? in its place
        for xx in range(bx0 + 1, bx1):
            p[cx + xx, cy + yy] = ground
    base = _over(base, g, pal, x, y)
    zx, zy = max(0, min(160, x - 32)), max(0, min(107, y))
    return [base, base.crop((zx, zy, zx + 80, zy + 53)).resize((240, 160), Image.NEAREST),
            parts_plate([idx_rgba(g, pal)], k=4, bg=(232, 208, 96))]


T563_MOCKS = {"dexbg": mock_dexbg, "minicard": mock_minicard, "ellipse": mock_ellipse, "heads": mock_heads,
              "switch": mock_switch, "famecursor": mock_famecursor, "fameq": mock_fameq}

T563_ROWS = {
    "dexbg": "Rows (theatre shots, the draft's tiles laid where the engine lays them and the old ones lifted out pixel "
             "by pixel, the run-time colours read off the shot): the INDEX's list (Kanto: tile 14); the GLOBAL "
             "INDEX's ground (national_dex_bgtiles' 14, rendered: GAME EVENTS' GLOBAL INDEX did not open on film); an entry (backdrop 12, the box 4/5/6/1); the area page (the "
             "box, and the NATIVE frame 29-31 on BG0); a habitat page (ground 2, the plates 16-28 in rows 5-8 at "
             "rest, the cards over them); every tile of both sheets at 3x.",
    "minicard": "Rows: a habitat page with the cards laid where the engine puts them (the number and a name printed "
                "as DexScreen prints them, ink 1, shadow 3); one card at 3x.",
    "ellipse": "Rows: a daemon with no area (ROVERCUB): today's ellipse lifted off the map and the draft blitted where "
               "the engine blits it (4, 28 of the map window), AREA UNKNOWN printed over it; the same at 2x.",
    "heads": "Rows: the GOTO map (theatre: the head found and replaced, REASON's -- the debug save's player); the same at "
             "3x; REASON's head and his overworld frame, INSTINCT's and hers, at 3x (red_normal / green_normal).",
    "switch": "Rows: the SWITCH menu was not reached on film (the route set FLAG_SYS_SEVII_MAP_123 and walked the "
              "cursor to SWITCH, and A did not open it), so the cursor is laid over the GOTO map where the menu puts it "
              "(subsprites at x 88 and 152), as a mock; the same at 2x; the four frames (left, right, then each a "
              "breath in) at 2x.",
    "famecursor": "Rows: HEARSAY with a clue chosen (theatre: the box found and replaced); the same at 3x; both frames "
                  "at 3x on the screen's yellow.",
    "fameq": "Rows: no ? was on film (the debug save has heard every clue: the route stepped through CRYSTAL, VERA, "
             "CAIRN and BASIN), so the ? is laid in place of the clue the cursor holds, in question_mark.png's own "
             "colours as a stand-in for OBJ palette 2's (inside the today shot's orange box); the same at 3x; the "
             "draft at 4x.",
}
T563_NOTES = {
    "dexbg": "Kept: 32 tiles each, every tile's role and slot (1 solid 5 for the AREA markers' fill, 2 solid 3, 3 solid "
             "2 in row 15, 12 solid 7 for the hour, 22 solid 2), both palettes untouched, the plate in 2/3/8 only "
             "(the cursor's pulse), 7 in tile 12 alone; the two sheets differ only in tile 14, as pret's did. A: A "
             "TERMINAL's box (slate rule cut at 45, the day's bracket in 8 as the message box's), graph paper behind "
             "the lists (Kanto squared, GLOBAL ruled), the plate a dark screen with a lit inner rim; B: the message "
             "box's own six-ring rule, dot grid, a tighter-cut plate with brackets; C: a hairline with teal pips, "
             "hatching, an octagon plate.",
    "minicard": "Kept: 64x40, palette row 0 as it is, y 3-25 paper (the number and the name are printed over it, "
                "0 skipped), nothing in 1 (the ink). A: an index card -- slate rule cut at 45, a dark rule, a ruled "
                "band, the day's bracket in two corners; B: dog-eared, graph paper below; C: a ticket, its tear line "
                "dashed and notched.",
    "ellipse": "Kept: 88x16, row 0, nothing in 1 (AREA UNKNOWN's ink) or 7 (the hour). A: a paper plate on a slate "
               "rule cut at 45 with the day's bracket at each end; B: a tag with pointed ends; C: open ends, two rules, "
               "teal brackets.",
    "heads": "From the player's own overworld frame (facing down), the same grey monkey in the same hat, in player.pal's "
             "colours (copied into the icon's own palette; B adds teal and slate in 12/13, which only the shoes use "
             "on the overworld). The engine picks the head by the player's gender, not the edition: player_icon_red "
             "is REASON, player_icon_leaf INSTINCT, in both CONTENT and CONTEXT. A shows the tail too -- REASON's "
             "curls up on the left of the picture, INSTINCT's on the right -- the one thing that tells them apart; "
             "C (the head alone) makes the two the same picture.",
    "switch": "Kept: 32x64 each, two frames (the second 2px in), the right the left's mirror, its own palette "
              "(switch_map_cursor.pal: 1-3 set). A: TERMINAL's cut corner as an L, teal with a slate edge; B: a "
              "prompt chevron pointing in, a rule above and below; C: thin amber ticks with a slate shadow.",
    "famecursor": "Kept: 32x64, both frames' boxes exactly where pret's were (read from the PNG), its own palette "
                  "(14, 15 retinted). A: a teal cut-corner box between slate rules; B: corner brackets; C: a slate box "
                  "with a light inner line.",
    "fameq": "Kept: 16x32, the tile where pret's was (x 1-14, y 12-30), and ONLY slots 10, 14 and 15: the code puts it "
             "in OBJ palette 2, which this screen does not load itself, so the colours are not ours to choose (the "
             "shot shows what they are). A: a small dark screen with the ? lit, as the trainers' emotes (T-561); B: a "
             "paper tag; C: the ? alone, edged.",
}


def t563_draft(out, shots_dir=None):
    os.makedirs(out, exist_ok=True)
    shots = {}
    for d_ in (shots_dir or "").split(","):
        shots.update(load_shots(d_))
    made = []
    for piece in T563_PIECES:
        for d in T563_OFFERED[piece]:
            errs = t563_check(piece, d)
            if errs:
                sys.exit("gbamenus3 --t563: %s %s breaks its contract: %s" % (piece, d, "; ".join(errs)))
            put_files(t563_outputs(piece, d), os.path.join(out, d, "graphics"))
        cols = [("TODAY (the engine)", T563_MOCKS[piece](shots, None))]
        for d in T563_OFFERED[piece]:
            cols.append(("%s %s" % (d, T563_NAMES[piece][d]), T563_MOCKS[piece](shots, d)))
        notes = [T563_ROWS[piece], T563_NOTES[piece],
                 "DRAFT -- drawn in code (tools/gbamenus3.py --t563), nothing in the engine until the user picks; "
                 "recommended: %s (%s). APPROVED_563 is empty." % (T563_RECOMMENDED[piece],
                                                                  T563_NAMES[piece][T563_RECOMMENDED[piece]])]
        made.append(contact("T-563 THE INDEX AND THE MAP -- %s -- DRAFT" % piece.upper(), cols, notes,
                            os.path.join(out, "t563_%s_sheet.png" % piece)))
    return made


def t563_main():
    if ARGS.write:
        if not ARGS.approved or not (ARGS.pick or ARGS.all):
            sys.exit("gbamenus3 --t563: --write needs --approved and --all or --pick piece=X,... (the user's picks)")
        picks = dict(kv.split("=") for kv in ARGS.pick.split(",")) if ARGS.pick else dict(APPROVED_563)
        if not picks:
            print("gbamenus3 --t563: nothing approved yet (T-563 is a DRAFT); nothing written")
            return 0
        for piece, d in picks.items():
            if piece not in T563_PIECES or d not in T563_OFFERED[piece]:
                sys.exit("gbamenus3 --t563: unknown pick %s=%s" % (piece, d))
            if APPROVED_563.get(piece) != d:
                sys.exit("gbamenus3 --t563: %s=%s is not APPROVED_563 (T-563 is a DRAFT)" % (piece, d))
        for piece, d in picks.items():
            for p in put_files(t563_outputs(piece, d), G):
                print("  wrote", os.path.relpath(p, ROOT))
        return 0
    if ARGS.draft:
        out = ARGS.draft if ARGS.draft != DRAFT_DEFAULT else T563_DRAFT
        for p in t563_draft(out, ARGS.shots):
            print("  wrote", os.path.relpath(p, ROOT))
        return 0
    return t563_report()


if __name__ == "__main__":
    sys.exit(main())
