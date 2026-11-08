#!/usr/bin/env python3
"""T-530 second pass: the menus FireRed still draws -- the TOOLKIT, the shop, the INDEX's icons and area map, the
TRAP TABLE's pocket picture, the party's hold marks and the PC's box menu, scroll arrows, waveform and DATA panel.

    python3 tools/gbamenus2.py                      # report: each screen's engine files, what the drop-in keeps, the
                                                    #   run-time colour work on it, lightness pairs and tile counts
    python3 tools/gbamenus2.py --draft [DIR]        # draw every screen into DIR (gfx/drafts/t530_menus/pass2/): the
                                                    #   files as the engine takes them (A/, B/) and a contact sheet
                                                    #   per screen -- the engine now, A (and B where one is offered),
                                                    #   each a 240x160 mock at real size with real content
    python3 tools/gbamenus2.py --write --approved --pick toolkit=A,shop=A,index=A,area=B,pouch=A,holds=A,pcparts=A
                                                    # write the chosen directions into the engine. Refuses without
                                                    #   --approved and a pick for each screen named.

DRAFT, 2026-11-08, the second pass of T-530 (the user picked "Menus, second pass"). The sibling of tools/gbamenus.py
(the first pass, built and released in v11.343.5) and drawn in its family, A TERMINAL: slate rule, 45-degree corners,
the teal bracket, paper, graph paper. Every pixel is drawn in code here: no AI image, nothing traced. The engine's
files are read for their SHAPE only -- which tile id each tilemap puts where, which palette slot the code swaps or
shares at run time -- and every drop-in keeps both, so no .bin, no .c and no slot's meaning changes.

THE SHAPE IS READ FROM ENGINE 33bc1e459 (the first pass's last commit, which none of these files had changed since
vanilla or ours), never from the working tree: reading this tool's own output back would make each write the input
of the next.

THE SCREENS, and what each drop-in keeps (report() prints the detail):
  TOOLKIT  tm_case.png's tiles redrawn in place on its two maps (menu.bin on BG2: the backdrop, the title plate, the
           list's paper, the lower band; tm_case.bin on BG1: the case, priority 0, IN FRONT of the card sprite), the
           four rows of menu_male.pal (female the same: nobody is a boy or a girl), the card sprite disc.png (frame 0 a
           PLUGIN, frame 1 a DRIVER, a card with an edge connector as the BAG draws them since T-525) and its 17 type
           rows (disc_types_1/2.pal: slots 1-8 each type's ramp, from tools/gbasprite.py TYPE_COLOR).
  SHOP     shop_menu.png redrawn in place on both maps (the normal and the PLUGIN shop share 28 tiles), its two rows
           (row 0 loaded as palette 11, row 1 as palette 6 when the description band is dimmed).
  INDEX    the 15 category icons the INDEX shows (64x48, each its own palette row 1; cat_icon_qmark is unreferenced
           and left), and the AREA page's map: map_kanto.png and the seven island maps, drawn in palette row 0 of the
           INDEX, which the INDEX itself prints with -- so the map keeps vanilla's pixel CLASSES (sea, land, route,
           town, frame) where they were, and the area markers still land on the towns they name.
  POUCH    berry_pouch.png, the TRAP TABLE's pocket picture: 64x64, its own palette.
  HOLDS    party_menu/hold_icons.png: the held-item mark and the mail mark (8x8 each), their own palette.
  PCPARTS  the box menu (choose_box_menu_center/corners, misc1 slots 4-7 with the box name in 15 on 14), the scroll
           arrows (box_scroll_arrow, misc2 13/14 with 15), the waveform (misc2 4-7 with 8) and the DATA panel
           (menu.png's 52 tiles of menu.bin columns 0-9, redrawn in place; interface.pal and
           interface_no_display_mon.pal retinted where only the panel reads them).

RUN-TIME COLOUR WORK READ BEFORE DRAWING (each one kept; report() lists it):
  HALFTONE (fieldmap.c DaemonsGreyHalftoneFrame) greys every palette at the copy to PLTT outside a few kept slots, so
  every pair that must read differs in LIGHTNESS, not only in hue; report() measures it.
  TOOLKIT  SetDescriptionWindowShade: rows 12-19 of BG2 take palette 1, or 3 while a PLUGIN is chosen (row 3 is row 1
           dimmed; the move-info paper stays paper, its ink is pokemon_types.pal 14 on 10). The description prints
           WHITE (std menu 1 on 2) on the band; the list prints dark (2 on 3) on the paper; the title WHITE on its plate.
           TintDiscpriteByType loads the card's palette from the type table per PLUGIN; sPal3Override sets 6/7 of
           palettes 13 and 15 (the cursor), not BG2's.
  SHOP     RecolorItemDescriptionBox: rows 14-19 (12-19 in the PLUGIN shop) of BG1 take palette 6 (row 1) while the
           how-many box is up; the list prints dark (palette 14, colour 1 = 2 on 3), the description WHITE (palette
           15, colour 0); the left ten columns are the overworld, seen through.
  INDEX    T-481 B writes the INDEX's BG row 0: the weekday on 8, the hour on 7. The map is drawn in row 0, so it keeps
           off 8; its sea stays on 7 (vanilla's sea is 7, and the sea darkening with the hour is kept on purpose). The
           area markers are a sprite in (63,159,208)/(211,236,248): the land is drawn light so they read on it. Each
           icon's palette is loaded into BG row 1 when its row is chosen, which nothing else on the page uses.
  PCPARTS  misc2 is shared by the PAW (1,2,3,11,12), its shadow (8, 15), the scroll arrows (13,14,15) and the
           waveform (4-8): only 4-7 and 13-14 are retinted, 8 and 15 kept. misc1 is the PAW in multi-move (1,2,3,11,12)
           and the box menu (4-7, text 15 on 14). The DATA panel's text prints in palette 3 (the scrolling backdrop's
           1/2/3, T-530's first pass kept them); pkmn_data.bin draws its label in row 0 with a mon shown and row 2
           without one.

NO NEW WORDS. Every word on these screens is printed by the game and kept; nothing here paints a word.
"""
import argparse, json, math, os, re, struct, subprocess, sys, tempfile, atexit, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import gbamenus as M
from gbamenus import (q5, lum, canvas, fill, put, cut_box, retile, render_map, idx_rgba, say, text_width,
                      contact, put_files, SLATE_OUT, SLATE_MID, SLATE_LIGHT, TEAL, TEAL_DK, PAPER, AMBER, AMBER_DK)

ROOT = M.ROOT
GBA = M.GBA
G = M.G
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t530_menus", "pass2")
SCREENS = ("toolkit", "shop", "index", "area", "pouch", "holds", "pcparts")

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--pick", help="screen=A|B,... for --write")
ap.add_argument("--all", action="store_true", help="--write the APPROVED picks")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes runs the write")
ARGS = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

#  Only the AREA map offers a B: the INDEX's map can look like the TOWN MAP (B SCORE) or like the other menus (A).
OFFERED = {"toolkit": "A", "shop": "A", "index": "A", "area": "AB", "pouch": "A", "holds": "A", "pcparts": "A"}
RECOMMENDED = {"toolkit": "A", "shop": "A", "index": "A", "area": "B", "pouch": "A", "holds": "A", "pcparts": "A"}
APPROVED = {}                                       # nothing yet: the user picks from the sheets

GRAPH, GRID = (232, 236, 240), (206, 214, 222)      # the ground: graph paper, its rule every 8px
STRIP, STRIP_LN, STRIP_DK = (44, 54, 68), (56, 68, 84), (24, 30, 40)


# ================================================================================================ files at 33bc1e459
BASE2 = "33bc1e459"
_B = {}


def src(rel):
    """graphics/<rel> as it stood at engine BASE2, in a scratch file. A file not in that commit is read as it is."""
    if rel not in _B:
        if "dir" not in _B:
            if subprocess.run(["git", "-C", GBA, "cat-file", "-e", BASE2 + "^{commit}"], capture_output=True).returncode:
                sys.exit("gbamenus2: the engine has no commit %s to read the shapes from (a shallow clone?)" % BASE2)
            _B["dir"] = tempfile.mkdtemp(prefix="gbamenus2_")
            atexit.register(shutil.rmtree, _B["dir"], True)
        r = subprocess.run(["git", "-C", GBA, "show", "%s:graphics/%s" % (BASE2, rel)], capture_output=True)
        if r.returncode:
            _B[rel] = os.path.join(G, rel)
        else:
            q = os.path.join(_B["dir"], rel)
            os.makedirs(os.path.dirname(q), exist_ok=True)
            open(q, "wb").write(r.stdout)
            _B[rel] = q
    return _B[rel]


def png(rel):
    """(w, h, pal, px): px the raw indices (8bpp sheets keep the row in the high nibble), a grey .png as 0-15."""
    im = Image.open(src(rel))
    w, h = im.size
    if im.mode == "L":
        d = list(im.getdata())
        return w, h, [(17 * i,) * 3 for i in range(16)], [[d[y * w + x] // 17 for x in range(w)] for y in range(h)]
    if im.mode != "P":
        im = im.convert("P")
    raw = im.getpalette() or []
    pal = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
    d = list(im.getdata())
    return w, h, pal, [[d[y * w + x] for x in range(w)] for y in range(h)]


def pal(rel, n=None):
    """A palette by its engine name: the JASC .pal, else the .png's own (a .gbapal is generated from one of them)."""
    stem = rel[:-len(".gbapal")] if rel.endswith(".gbapal") else rel[:-len(".pal")] if rel.endswith(".pal") else rel
    for cand in (stem + ".pal", stem + ".png"):
        p = src(cand)
        if os.path.exists(p):
            if cand.endswith(".pal"):
                w = open(p).read().split()
                k = int(w[2])
                v = list(map(int, w[3:3 + 3 * k]))
                c = [tuple(v[3 * i:3 * i + 3]) for i in range(k)]
            else:
                c = png(cand)[2]
            return c[:n] if n else c
    raise SystemExit("gbamenus2: no palette for %s" % rel)


def m16(rel):
    d = open(src(rel), "rb").read()
    return [(e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12) for e in struct.unpack("<%dH" % (len(d) // 2), d)]


def low(px):
    return [[v & 15 for v in r] for r in px]


def ramp(c, k=0.42):
    return tuple(min(255, int(v + (255 - v) * k)) for v in c), tuple(c), tuple(int(v * (1 - k)) for v in c)


def dim(c, k=0.7):
    return tuple(int(v * k) for v in c)


def rgba_of(g, palette, clear0=True):
    return idx_rgba(g, palette, clear0)


def outline(g, val, inside=lambda v: v not in (0,), x0=0, y0=0, w=None, h=None):
    """Ring every drawn pixel with `val` where it meets the clear (index 0), 4-neighbour."""
    w = w or len(g[0])
    h = h or len(g)
    add = []
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if g[y][x] == 0 and any(x0 <= x + dx < x0 + w and y0 <= y + dy < y0 + h and inside(g[y + dy][x + dx])
                                    and g[y + dy][x + dx] != val
                                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                add.append((x, y))
    for x, y in add:
        g[y][x] = val


def bracket(g, x, y, v, n=5, flip=False):
    """The teal corner bracket: an L of n pixels each way."""
    for i in range(n):
        put(g, x + (-i if flip else i), y, v)
        put(g, x, y + i, v)


def graph(g, x0, y0, x1, y1, a, b, step=8, phase=7, dotted=True):
    """Graph paper: `a` ground, `b` its rule every `step` px (dotted: every other pixel), tile-periodic."""
    for y in range(y0, y1):
        for x in range(x0, x1):
            on = (x % step == phase and (y % 2 == 0 or not dotted)) or (y % step == phase and (x % 2 == 0 or not dotted))
            put(g, x, y, b if on else a)


# ---- the game's words and data, read from the engine (no new words)
def strings_c():
    return open(os.path.join(GBA, "src/strings.c")).read()


def cstr(name, text=None):
    text = text or strings_c()
    m = re.search(r"\b%s\[\]\s*=\s*_\(\"((?:[^\"\\]|\\.)*)\"\)" % re.escape(name), text)
    return re.sub(r"\{[^}]*\}", "", m.group(1)).replace("\\n", "\n") if m else name


def items_json():
    d = json.load(open(os.path.join(GBA, "src/data/items.json")))
    return {x["itemId"]: x for x in (d["items"] if isinstance(d, dict) else d)}


def move_names():
    return dict(re.findall(r"\[MOVE_(\w+)\]\s*=\s*_\(\"([^\"]*)\"\)",
                           open(os.path.join(GBA, "src/data/text/move_names.h")).read()))


def move_data(move):
    t = open(os.path.join(GBA, "src/data/battle_moves.h")).read()
    m = re.search(r"\[MOVE_%s\]\s*=\s*\{(.*?)\}," % move, t, re.S)
    b = m.group(1)
    g = lambda k: re.search(r"\.%s\s*=\s*(\w+)" % k, b).group(1)
    return dict(power=int(g("power")), type=g("type"), accuracy=int(g("accuracy")), pp=int(g("pp")))


def item_icon_img(item):
    """An item's icon as the BAG shows it: item_icon_table.h -> graphics/items.h -> the .png and its palette."""
    t = open(os.path.join(GBA, "src/data/item_icon_table.h")).read()
    m = re.search(r"\[%s\]\s*=\s*\{(\w+),\s*(\w+)\}" % item, t)
    gi = open(os.path.join(GBA, "src/data/graphics/items.h")).read()
    ipath = re.search(r"%s\[\]\s*=\s*INCBIN_U32\(\"graphics/([^\"]+)\.4bpp" % m.group(1), gi).group(1)
    ppath = re.search(r"%s\[\]\s*=\s*INCBIN_U32\(\"graphics/([^\"]+)\.gbapal" % m.group(2), gi).group(1)
    w, h, p, px = png(ipath + ".png")
    return idx_rgba(low(px), pal(ppath + ".pal"))


def std_pal(n):
    return M.jasc(os.path.join(G, "text_window/stdpal_%d.pal" % n))


STDMENU = None


def std_menu():
    global STDMENU
    if STDMENU is None:
        STDMENU = pal("interface/std_menu.pal")
    return STDMENU


def menu_info_icon(k, width):
    """BlitMenuInfoIcon: the 4bpp bitmap from tile k on, `width` px wide and 12 tall, read as one 128px-wide sheet."""
    w, h, p, px = png("interface/menu_info.png")
    tp = pal("interface/pokemon_types.pal")
    g = canvas(width, 12)
    for y in range(12):
        for x in range(width):
            t = k + x // 8 + (y // 8) * 16
            sx, sy = (t % 16) * 8 + x % 8, (t // 16) * 8 + y % 8
            g[y][x] = px[sy][sx] & 15
    return idx_rgba(g, tp)


TYPE_ICON_OFFSET = {"NORMAL": 0x20, "FIGHTING": 0x64, "FLYING": 0x60, "POISON": 0x80, "GROUND": 0x48, "ROCK": 0x44,
                    "BUG": 0x6C, "GHOST": 0x68, "STEEL": 0x88, "FIRE": 0x24, "WATER": 0x28, "GRASS": 0x2C,
                    "ELECTRIC": 0x40, "PSYCHIC": 0x84, "ICE": 0x4C, "DRAGON": 0xA0, "DARK": 0x8C}


def type_colours():
    import ast
    s = open(os.path.join(ROOT, "tools/gbasprite.py")).read()
    m = re.search(r"^TYPE_COLOR = \{.*?^\}", s, re.S | re.M)
    return ast.literal_eval(m.group(0).split("=", 1)[1])


def cursor_tri(im, x, y, c):
    ImageDraw.Draw(im).polygon([(x, y), (x, y + 8), (x + 4, y + 4)], fill=q5(c))


# ================================================================================================ TOOLKIT
TM_TYPES = ["NORMAL", "FIRE", "WATER", "GRASS", "ELECTRIC", "ROCK", "GROUND", "ICE", "FLYING", "FIGHTING", "GHOST",
            "BUG", "POISON", "PSYCHIC", "STEEL", "DARK", "DRAGON"]          # sTMSpritePaletteOffsetByType, row k
TK_ROWS = {   # menu_male.pal's four rows: 0 the upper screen, 1 the lower band, 2 the case, 3 the lower band dimmed
    0: {1: GRAPH, 2: GRID, 3: SLATE_OUT, 4: SLATE_MID, 5: SLATE_LIGHT, 6: TEAL, 7: PAPER, 8: (200, 208, 214),
        9: (60, 72, 88), 10: TEAL_DK, 11: (96, 112, 128), 12: (236, 240, 244)},
    1: {1: SLATE_OUT, 2: SLATE_MID, 3: SLATE_OUT, 4: SLATE_LIGHT, 5: PAPER, 6: (226, 230, 234), 7: TEAL,
        8: STRIP, 9: STRIP_LN, 10: STRIP_DK, 11: GRAPH, 12: GRID},
    2: {1: SLATE_OUT, 2: SLATE_MID, 3: SLATE_LIGHT, 4: (64, 76, 92), 5: (208, 216, 224), 6: TEAL, 7: TEAL_DK,
        8: (16, 20, 26), 9: PAPER, 10: (150, 164, 178), 11: AMBER, 12: AMBER_DK},
}


def tk_rows():
    rows = [list(pal("tm_case/menu_male.pal")[i * 16:(i + 1) * 16]) for i in range(4)]
    for r, d in TK_ROWS.items():
        for k, v in d.items():
            rows[r][k] = v
    rows[3] = list(rows[1])
    for k in (1, 2, 8, 9, 10):                               # chosen: the band dims, the move-info paper stays paper
        rows[3][k] = dim(rows[1][k], 0.55)
    return rows


def tk_target_bg2():
    """The BG2 picture (menu.bin, 30x20), in the index of the row each part takes: rows 0-11 palette 0, 12-19 1.
    240 wide: the map's two columns off the screen do not vote. Every edge sits in the tiles menu.bin uses once: the
    title plate's bottom corners in 08 (col 0, and col 8 mirrored), its right rule in col 9's 03/06; the list's
    left rule and cut corners in col 9 (03, 06, 0a, 11), its rows' rule on the 0b tiles; the lower band's card in
    row 12/19 and cols 0/11 (16, 1a, 1e and 18, 1c, 20)."""
    g = canvas(240, 160, 1)
    graph(g, 0, 0, 240, 96, 1, 2)
    # the title plate (WIN_TITLE 0,1 10x2, printed WHITE): fill 9, x 0-71 (and its right rule at 72/73 above row 2)
    for y in range(0, 24):
        for x in range(0, 74):
            if y < 16 and x >= 72:
                g[y][x] = 11 if x == 72 else 3
            elif x < 72:
                d = min(x, 71 - x) + (23 - y)                # the two bottom corners cut at 45 degrees
                if d < 4:
                    g[y][x] = 1                              # plain ground under the cut: both ends mirror
                    continue
                g[y][x] = 3 if y == 23 or d == 4 else (11 if y == 22 or d == 5 else 9)
    bracket(g, 2, 2, 6)                                      # y 0-7: row 1's tile repeats across the plate
    # the list's paper (WIN_LIST 10,1 19x10, printed dark): x 75-239, y 2-85, its two left corners cut in col 9
    for y in range(2, 88):
        for x in range(75, 240):
            d = min(x - 75 + (y - 2), x - 75 + (87 - y))
            if d < 3:
                continue
            k = min(d - 3, y - 2, 87 - y)
            g[y][x] = 3 if k == 0 else (5 if k == 1 else 7)
    for i in range(3):
        put(g, 76 + i, 4 - i, 6)                             # the teal bracket on the top cut
        put(g, 77 + i, 5 - i, 6)
    for k in range(4):                                       # a dotted rule under each 16px row (the 0b tiles)
        for x in range(88, 232, 2):
            put(g, x, 23 + 16 * k, 8)
    # the lower band (palette 1/3): the rail, the move-info card (x 2-93), the description band (x 94-239)
    for y in range(96, 160):
        for x in range(240):
            g[y][x] = 9 if (y % 4 == 3 and x % 2 == 0) else 8
    for x in range(240):
        g[96][x], g[97][x] = 1, 2
    for y in range(98, 160):
        for x in range(0, 94):
            g[y][x] = 12 if ((x % 8 == 7 and y % 2 == 0) or (y % 8 == 7 and x % 2 == 0)) else 11
    cut_box(g, 2, 99, 92, 59, 3, [3, 4], 5)                  # the card: x 2-93, y 99-157
    for i in range(3):
        put(g, 5 + i, 102, 7)
        put(g, 5, 102 + i, 7) if i < 2 else None
    for y in range(98, 160):
        g[y][94], g[y][95] = 10, 10
    return g


def tk_target_case():
    """The BG1 picture (tm_case.bin): the TOOLKIT, a slate case with a slot the cards stand in. It is IN FRONT of the
    card sprite (priority 0 over 2), so nothing is drawn above the slot where a card passes (x 9-57); and its lower
    right is cut at 45 degrees where the map leaves tiles clear (7,9), (6,10), (7,10)."""
    g = canvas(240, 160, 0)
    x0, x1, top, bot = 9, 55, 58, 86
    for y in range(top, bot + 1):
        for x in range(x0, x1 + 1):
            if x > 127 - y or (y > bot - 3 and x < x0 + (y - (bot - 3))):
                continue
            g[y][x] = 2
    outline_ring = [(x, y) for y in range(top, bot + 1) for x in range(x0, x1 + 1) if g[y][x] == 2 and any(
        not (0 <= x + dx < 240 and 0 <= y + dy < 160) or g[y + dy][x + dx] == 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in outline_ring:
        g[y][x] = 1
    for x in range(x0 + 1, x1):
        if g[top + 1][x] == 2:
            g[top + 1][x] = 5                                # its lip, lit
    for x in range(x0 + 4, x1 - 3):
        g[top][x] = 8                                        # the slot the cards stand in
    for y in range(top + 3, bot - 1):                        # a shade along its cut
        x = min(x1 - 1, 126 - y)
        if g[y][x] == 2:
            g[y][x] = 4
    cut_box(g, 16, 67, 28, 11, 2, [1], 9)                    # the label plate, the teal bracket on it
    bracket(g, 18, 69, 6, 3)
    for x in range(24, 40, 2):
        put(g, x, 73, 10)
    cut_box(g, 27, 61, 8, 4, 1, [12], 11)                    # the latch
    for y in range(64, 84):                                  # a hinge at its left side
        if y % 6 < 3:
            put(g, x0 + 1, y, 7)
    return g


def tk_build(direction):
    w, h, p, px = png("tm_case/tm_case.png")
    sheet = [list(r) for r in px]
    bg2, bg1 = m16("tm_case/menu.bin"), m16("tm_case/tm_case.bin")
    if direction is None:
        rows = [list(pal("tm_case/menu_male.pal")[i * 16:(i + 1) * 16]) for i in range(4)]
        return sheet, w // 8, rows, bg2, bg1, (0, 0)
    miss = retile(sheet, w // 8, [(bg2, 32, tk_target_bg2()), (bg1, 32, tk_target_case())])
    return sheet, w // 8, tk_rows(), bg2, bg1, miss


def card_frames(direction):
    """disc.png: 32x64, frame 0 a PLUGIN, frame 1 a DRIVER. A: a card with an edge connector, as the BAG draws it
    (T-525), its type's ramp in 2/3/4, the label 5 with 6, the board 7 with gold contacts 8, the gear 9."""
    if direction is None:
        return png("tm_case/disc.png")[3]
    g = canvas(32, 64)
    for f in range(2):
        y0 = f * 32
        x0, x1, t, b = 7, 24, 2, 31
        fill(g, x0, y0 + t, x1 + 1, y0 + b - 6, 3)           # the card, its type's colour
        for y in range(t, b - 6):
            put(g, x0, y0 + y, 2)                            # lit edge
            put(g, x1, y0 + y, 4)                            # shade edge
        for x in range(x0, x1 + 1):
            put(g, x, y0 + t, 2)
        for i in range(4):                                   # its cut corner, top right
            for j in range(4 - i):
                put(g, x1 - j, y0 + t + i, 0)
        fill(g, x0 + 2, y0 + 5, x1 - 2, y0 + 15, 5)          # the label
        if f == 0:
            for yy, xe in ((8, x1 - 4), (11, x1 - 7)):
                fill(g, x0 + 4, y0 + yy, xe, y0 + yy + 1, 6)
        else:
            gear = ["  X X  ", " XXXXX ", "XXX XXX", " XX XX ", "XXX XXX", " XXXXX ", "  X X  "]
            for j, row in enumerate(gear):
                for i, ch in enumerate(row):
                    if ch == "X":
                        put(g, x0 + 5 + i, y0 + 6 + j, 9)
        fill(g, x0 + 1, y0 + b - 6, x1, y0 + b + 1, 7)       # the connector board
        for x in range(x0 + 2, x1 - 0, 2):
            fill(g, x, y0 + b - 5, x + 1, y0 + b + 1, 8)      # its contacts
        outline(g, 1, x0=0, y0=y0, w=32, h=32)
    return g


def card_pals(direction):
    """The 17 type rows (disc_types_1.pal 16 rows, disc_types_2.pal row 0 DRAGON): 1 the outline, 2-4 the type's
    ramp, 5-6 the label, 7-8 the board and contacts, 9 the gear. 10-15 kept."""
    a = pal("tm_case/disc_types_1.pal")
    b = pal("tm_case/disc_types_2.pal")
    rows = [list(a[i * 16:(i + 1) * 16]) for i in range(16)] + [list((b + [(0, 0, 0)] * 16)[:16])]
    if direction is None:
        return rows
    tc = type_colours()
    for k, t in enumerate(TM_TYPES):
        lit, mid, dk = ramp(tc[t], 0.4)
        r = rows[k]
        r[1], r[2], r[3], r[4] = (SLATE_OUT if lum(mid) > 80 else SLATE_LIGHT), lit, mid, dk
        r[5], r[6], r[7], r[8], r[9] = PAPER, SLATE_MID, (64, 76, 92), (214, 186, 96), SLATE_OUT
    return rows


TK_LIST = [("TM01", "FOCUS_PUNCH"), ("TM02", "DRAGON_CLAW"), ("TM03", "WATER_PULSE"), ("TM04", "CALM_MIND"),
           ("TM05", "ROAR")]


def tk_mock(direction, chosen=0, shade=False):
    sheet, per, rows, bg2, bg1, miss = tk_build(direction)
    s = low(sheet)
    im = Image.new("RGB", (240, 160), q5(rows[0][0]))
    b2 = render_map(s, per, bg2, 32, 20, rows, pal_of=lambda e: (3 if shade and e[3] == 1 else e[3]))
    im.paste(b2, (0, 0), b2)
    names, items = move_names(), items_json()
    sm = std_menu()
    # the card sprite (priority 2, under the case on BG1)
    num, mv = TK_LIST[chosen]
    md = move_data(mv)
    cg = card_frames(direction)
    cr = card_pals(direction)[TM_TYPES.index(md["type"].replace("TYPE_", ""))]
    tm_idx = chosen
    cx = 41 - (14 * tm_idx) // 58
    cy = 46 + (8 * tm_idx) // 58
    ci = idx_rgba(low(cg[0:32]), cr)
    im.paste(ci, (cx - 16, cy - 16), ci)
    b1 = render_map(s, per, bg1, 32, 20, rows, pal_of=lambda e: e[3])
    im.paste(b1, (0, 0), b1)
    # the title, WHITE (std menu 1 on 2) centred in WIN_TITLE (0,1 10x2)
    t = cstr("gText_TMCase")
    say(im, (80 - text_width(t)) // 2, 8 + 1, t, sm[1], sm[2])
    # the list (WIN_LIST 10,1): dark (2 on 3), item_X 8, rows 16px from upText_Y 2
    for i, (n, m) in enumerate(TK_LIST):                     # maxShowed 5: CLOSE is below, scrolled to
        y = 8 + 2 + 16 * i - 2
        if m:
            x = say(im, 88, y + 2, "No%s" % n[2:], sm[2], sm[3], small=True)
            say(im, x + 4, y, names.get(m, m), sm[2], sm[3])
        else:
            say(im, 88, y, cstr("gText_Close"), sm[2], sm[3])
        if i == chosen:
            cursor_tri(im, 81, y + 4, sm[2])
    # the description (WIN_DESCRIPTION 12,12; std menu 1 on 2, WHITE)
    d = items[{"TM01": "ITEM_TM01", "TM02": "ITEM_TM02", "TM03": "ITEM_TM03", "TM04": "ITEM_TM04",
               "TM05": "ITEM_TM05"}[num]]["description_english"].replace("\\n", "\n")
    for k, line in enumerate(d.split("\n")):
        say(im, 96 + 2, 96 + 3 + 14 * k, line, sm[1], sm[2])
    # the move's info (labels 1,13 and values 7,13; pokemon_types 14 on 10)
    tp = pal("interface/pokemon_types.pal")
    for k, off in enumerate((0xA8, 0xC0, 0xC8, 0xE0)):
        ic = menu_info_icon(off, 40)
        im.paste(ic, (8, 104 + 12 * k), ic)
    ty = menu_info_icon(TYPE_ICON_OFFSET[md["type"].replace("TYPE_", "")], 32)
    im.paste(ty, (56, 104), ty)
    for k, v in enumerate((md["power"], md["accuracy"], md["pp"])):
        say(im, 56 + 7, 104 + 12 * (k + 1) - 2, str(v) if v else "---", tp[14], tp[10])
    return im


# ================================================================================================ SHOP
SHOP_ROWS = {1: SLATE_OUT, 2: SLATE_MID, 3: SLATE_LIGHT, 4: TEAL, 5: PAPER, 6: (200, 208, 214), 7: (226, 230, 234),
             8: STRIP, 9: STRIP_LN, 10: STRIP_DK, 11: TEAL_DK, 12: (236, 240, 244), 13: (96, 112, 128)}


def shop_rows(direction):
    p = pal("shop_menu/shop_menu.pal") if os.path.exists(src("shop_menu/shop_menu.pal")) else png("shop_menu/shop_menu.png")[2]
    rows = [list(p[0:16]), list((p + [(0, 0, 0)] * 32)[16:32])]
    if direction is None:
        return rows
    for k, v in SHOP_ROWS.items():
        rows[0][k] = v
    rows[1] = list(rows[0])
    for k in (1, 2, 8, 9, 10):                              # how-many: the band dims; the paper and bay stay light
        rows[1][k] = dim(rows[0][k], 0.55)
    return rows


def shop_target(tm):
    """BG1 (shop_tilemap.bin / shop_tm_hm_tilemap.bin), all palette 11 (row 0) until the band dims (row 1). 240 wide
    (the map's off-screen columns do not vote). Every edge sits in the tiles the maps use once: the list's corners in
    02/20/0a/23 and its sides in cols 10 and 29; the bay's frame in 0d-16 (cols 0-4, rows 15-18) and the PLUGIN
    card's in 18-1f (cols 0-11, rows 13-18), whose middle tile 12 is the bay's too, so both are paper."""
    g = canvas(240, 160, 0)
    bottom = 95 if tm else 111                               # the list's paper ends with row 11 (PLUGIN shop) or 13
    cut_box(g, 82, 1, 157, bottom - 1, 4, [1, 3], 5)         # the list's paper (WIN 4: 11,1, printed dark)
    for i in range(3):
        put(g, 83 + i, 4 - i, 4)                             # the bracket, on the cut
        put(g, 84 + i, 5 - i, 4)
    for k in range(4 if tm else 5):                          # under each 16px row (the 08 tiles both maps share)
        for x in range(96, 224, 2):
            put(g, x, 31 + 16 * k, 6)
    bracket(g, 1, 1, 4, 5)                                   # tile 01: a viewfinder's corner over the overworld
    rail = 96 if tm else 112                                 # row 12 (PLUGIN shop) or 14: the rail, the band
    for y in range(rail, 160):
        for x in range(240):
            g[y][x] = 9 if y % 4 == 3 and x % 2 == 0 else 8
    for x in range(240):
        g[rail + 3][x], g[rail + 4][x] = 1, 2
    if tm:                                                   # the move's card (WIN 6: 1,14, printed dark)
        cut_box(g, 2, 106, 92, 44, 4, [1, 3], 5)
        for i in range(3):
            put(g, 5 + i, 109, 4)
            put(g, 5, 109 + i, 4)
    else:                                                    # the item's bay (the icon at 24,140)
        cut_box(g, 2, 122, 36, 28, 4, [1, 3], 5)
        for i in range(3):
            put(g, 5 + i, 125, 4)
            put(g, 5, 125 + i, 4)
    return g


def shop_build(direction):
    w, h, p, px = png("shop_menu/shop_menu.png")
    sheet = [list(r) for r in px]
    normal, tmhm = m16("shop_menu/shop_tilemap.bin"), m16("shop_menu/shop_tm_hm_tilemap.bin")
    miss = (0, 0)
    if direction is not None:
        miss = retile(sheet, w // 8, [(normal, 32, shop_target(False)), (tmhm, 32, shop_target(True))])
    return sheet, w // 8, shop_rows(direction), normal, tmhm, miss


def mart_view():
    """The overworld behind the shop's left ten columns: VIRIDIAN's MART, as tools/reviewsheet.py draws a map."""
    import reviewsheet
    mp = reviewsheet.render(reviewsheet.layout_of("ViridianCity_Mart"))
    return mp.crop((max(0, mp.width // 2 - 56), 8, max(0, mp.width // 2 - 56) + 80, 8 + 112))


SHOP_ITEMS = ["ITEM_POKE_BALL", "ITEM_POTION", "ITEM_ANTIDOTE", "ITEM_PARALYZE_HEAL"]


def shop_mock(direction, tm=False, dimmed=False):
    sheet, per, rows, normal, tmhm, miss = shop_build(direction)
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    try:
        im.paste(mart_view(), (0, 0))
    except Exception:
        pass
    band = (12 if tm else 14) * 8
    b = render_map(low(sheet), per, tmhm if tm else normal, 32, 20, rows,
                   pal_of=lambda e: 0)
    im.paste(b, (0, 0), b)
    if dimmed:
        bd = render_map(low(sheet), per, tmhm if tm else normal, 32, 20, rows, pal_of=lambda e: 1)
        im.paste(bd.crop((0, band, 240, 160)), (0, band), bd.crop((0, band, 240, 160)))
    it = items_json()
    sm = std_menu()
    w2 = std_pal(2)
    M.std_frame_box(im, 8, 8, 8, 3)                          # the money box (WIN 0, 1,1 8x3, the std frame)
    st = std_pal(0)
    say(im, 10, 10, "MONEY", st[2], st[3])
    say(im, 10, 26, "3000", st[2], st[3])
    if tm:
        names = [("ITEM_TM05", "ROAR"), ("ITEM_TM12", "TAUNT"), ("ITEM_TM16", "LIGHT_SCREEN")]
        lst = [(it[i]["english"], it[i].get("price", 0)) for i, m in names]
    else:
        lst = [(it[i]["english"], it[i].get("price", 0)) for i in SHOP_ITEMS]
    lst.append((cstr("gText_Cancel2") if "gText_Cancel2" in strings_c() else "CANCEL", None))
    for i, (n, pr) in enumerate(lst):
        y = 8 + 2 + 16 * i - 2
        say(im, 96, y, n[:18] if tm else n, sm[2], sm[3])
        if pr is not None:
            s = "%d" % pr
            say(im, 88 + 0x69 + 24 - text_width(s, True), y + 2, s, sm[2], sm[3], small=True)
        if i == 0:
            cursor_tri(im, 89, y + 4, sm[2])
    first = names[0][0] if tm else SHOP_ITEMS[0]
    d = it[first]["description_english"].replace("\\n", "\n").split("\n")
    if tm:                                                   # WIN 5 at 12,12 (WHITE); WIN 6 at 1,14: No, the move
        for k, line in enumerate(d[:3]):
            say(im, 96, 96 + 3 + 14 * k, line, w2[1], w2[2])
        say(im, 8, 112, "No05", sm[2], sm[3], small=True)
        say(im, 8, 112 + 16, move_names().get("ROAR", "ROAR"), sm[2], sm[3])
    else:                                                    # WIN 5 at 5,14 (WHITE); the icon centred on (24,140)
        for k, line in enumerate(d[:3]):
            say(im, 40, 112 + 3 + 14 * k, line, w2[1], w2[2])
        ic = item_icon_img(first)
        im.paste(ic, (12, 128), ic)
    return im


# ================================================================================================ INDEX icons
CATS = [   # (file stem, the DAEMONS words printed beside it, what the plate shows)
    ("numerical", "gText_NumericalMode", "a numbered list: three rows, each a number and its rule"),
    ("grassland", "gText_DexCategory_GrasslandPkmn", "USERLAND: the surface -- a level ground line and the short "
                  "marks that stand on it, a cursor's caret on top"),
    ("forest", "gText_DexCategory_ForestPkmn", "BRANCHING: a tree that is a graph -- a root, and branches that split "
               "into nodes"),
    ("waters_edge", "gText_DexCategory_WatersEdgePkmn", "BOUNDARY: two fields, one ruled and one dotted, and the "
                    "dashed line between them"),
    ("sea", "gText_DexCategory_SeaPkmn", "STREAM: three waves, and the bits riding them"),
    ("cave", "gText_DexCategory_CavePkmn", "KERNEL: rings round a solid core"),
    ("mountain", "gText_DexCategory_MountainPkmn", "STACK: blocks stacked into a peak"),
    ("rough_terrain", "gText_DexCategory_RoughTerrainPkmn", "FRAGMENTED: a row of blocks with gaps, and pieces broken "
                      "loose"),
    ("urban", "gText_DexCategory_UrbanPkmn", "NETWORK: nodes and the links between them"),
    ("rare", "gText_DexCategory_RarePkmn", "UNINDEXED: an entry card with no number, a dashed outline, a spark"),
    ("abc", "gText_AToZMode", "A TO Z: an A, an arrow, a Z"),
    ("type", "gText_TypeMode", "TYPE: a corner of the chart, each cell a type's own colour"),
    ("lightest", "gText_LightestMode", "LIGHTEST: a beam balance tipped, the light side up"),
    ("smallest", "gText_SmallestMode", "SMALLEST: three nested squares, the least one lit"),
    ("cancel", "gText_ClosePokedex", "CLOSE: the return key"),
]
ICON_PAL = [(0, 0, 0), PAPER, (220, 226, 232), SLATE_OUT, SLATE_MID, SLATE_LIGHT, TEAL, TEAL_DK, (140, 152, 166),
            (96, 112, 128), (236, 240, 244), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
DIG = {"0": ["XXX", "X.X", "X.X", "X.X", "XXX"], "1": [".X.", "XX.", ".X.", ".X.", "XXX"],
       "2": ["XXX", "..X", "XXX", "X..", "XXX"], "3": ["XXX", "..X", "XXX", "..X", "XXX"]}
BIGA = ["..XX..", ".XXXX.", "XX..XX", "XX..XX", "XXXXXX", "XX..XX", "XX..XX"]
BIGZ = ["XXXXXX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XXXXXX"]


def glyph(g, x, y, rows, v, s=1):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == "X":
                fill(g, x + i * s, y + j * s, x + i * s + s, y + j * s + s, v)


def line(g, x0, y0, x1, y1, v, w=1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        fill(g, x, y, x + w, y + w, v)


def disc(g, cx, cy, r, v):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r:
                put(g, x, y, v)


def cat_icon(stem):
    """A 64x48 TERMINAL plate: the slate rule cut at 45 degrees, graph paper, the teal bracket, and the category's
    pictogram in slate ink. Index 0 outside the cut corners (the INDEX's backdrop shows there, as round vanilla's
    did). Returns (grid, palette)."""
    g = canvas(64, 48)
    cut_box(g, 0, 0, 64, 48, 7, [3, 5], 1)
    for y in range(2, 46):
        for x in range(2, 62):
            if g[y][x] == 1 and ((x % 8 == 3 and y % 2 == 0) or (y % 8 == 3 and x % 2 == 0)):
                g[y][x] = 2
    for i in range(6):                                       # the bracket, inside the top-left cut
        put(g, 5 + i, 3, 6)
        put(g, 3, 5 + i, 6)
    p = list(ICON_PAL)
    S, Sm, Sl = 3, 4, 8
    if stem == "numerical":
        for k, n in enumerate(("01", "02", "03")):
            y = 8 + 12 * k
            glyph(g, 11, y, DIG[n[0]], S, 2)
            glyph(g, 19, y, DIG[n[1]], S, 2)
            fill(g, 29, y + 4, 54 - 7 * k, y + 6, 6 if k == 0 else Sm)
        fill(g, 9, 44 - 4, 55, 41, Sl)
    elif stem == "grassland":
        fill(g, 8, 34, 56, 36, S)                            # the ground line
        for i, hgt in enumerate((5, 8, 4, 10, 6, 3, 9, 5, 7, 4, 8, 6)):
            fill(g, 10 + 4 * i, 34 - hgt, 12 + 4 * i, 34, Sm if i % 3 else S)
        fill(g, 8, 37, 56, 38, Sl)
        for i in range(4):                                   # a caret above it: the user's place
            put(g, 30 + i, 12 + i, 6)
            put(g, 36 - i, 12 + i, 6)
    elif stem == "forest":
        nodes = [(32, 38), (32, 29), (20, 22), (44, 22), (14, 13), (26, 13), (38, 13), (50, 13)]
        for a, b in ((0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)):
            line(g, nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], Sm, 2)
        for i, (x, y) in enumerate(nodes):
            fill(g, x - 3, y - 3, x + 3, y + 3, S)
            fill(g, x - 2, y - 2, x + 2, y + 2, 6 if i == 0 else 10)
    elif stem == "waters_edge":
        for y in range(8, 42):
            bx = 30 + int(4 * math.sin(y / 4.0))
            for x in range(6, 58):
                if x < bx - 1 and y % 4 == 1 and g[y][x] in (1, 2):
                    g[y][x] = Sm
                elif x > bx + 1 and x % 4 == 1 and y % 4 == 1 and g[y][x] in (1, 2):
                    g[y][x] = S
            if (y // 2) % 2 == 0:
                fill(g, bx - 1, y, bx + 1, y + 1, 6)
    elif stem == "sea":
        for k in range(3):
            yc = 14 + 10 * k
            for x in range(8, 56):
                y = yc + int(round(2.5 * math.sin((x + 5 * k) / 3.2)))
                put(g, x, y, S if k != 1 else 6)
                put(g, x, y + 1, Sm if k != 1 else 7)
            for j, b in enumerate("101" if k != 1 else "010"):
                x = 12 + 15 * j + 4 * k
                y = yc - 7 + int(round(2.5 * math.sin((x + 1 + 5 * k) / 3.2)))
                glyph(g, x, y, DIG[b], Sm)
    elif stem == "cave":
        for r, v in ((17, S), (13, Sm), (9, S)):
            cut_box(g, 32 - r - 6, 24 - r + 2, 2 * r + 12, 2 * r - 4, 4, [v], None)
        fill(g, 28, 21, 36, 28, 6)
        fill(g, 29, 22, 35, 27, 7)
    elif stem == "mountain":
        for row in range(5):
            n = row + 1
            y = 12 + 5 * row
            w = 7
            x0 = 32 - n * (w + 1) // 2
            for i in range(n):
                fill(g, x0 + i * (w + 1), y, x0 + i * (w + 1) + w, y + 4, 6 if row == 0 else (S if (i + row) % 2 else Sm))
        fill(g, 10, 37, 54, 38, S)
    elif stem == "rough_terrain":
        x = 8
        for k, (w, gap) in enumerate(((6, 2), (4, 4), (8, 2), (3, 5), (6, 3), (5, 0))):
            fill(g, x, 28, x + w, 34, Sm if k % 2 else S)
            x += w + gap
        for (bx, by, w, h) in ((14, 14, 5, 4), (27, 10, 4, 5), (39, 16, 6, 4), (48, 11, 3, 3)):
            fill(g, bx, by, bx + w, by + h, Sl)
            fill(g, bx, by, bx + w, by + 1, S)
        fill(g, 32, 20, 36, 24, 6)
    elif stem == "urban":
        nodes = [(14, 14), (32, 10), (50, 16), (22, 30), (42, 32), (32, 22)]
        for a, b in ((0, 1), (1, 2), (0, 3), (3, 5), (5, 1), (5, 4), (4, 2), (3, 4)):
            line(g, nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], Sl, 1)
        for i, (x, y) in enumerate(nodes):
            fill(g, x - 3, y - 3, x + 3, y + 3, S)
            fill(g, x - 2, y - 2, x + 2, y + 2, 6 if i == 5 else 10)
    elif stem == "rare":
        for x in range(18, 46):
            if (x // 2) % 2 == 0:
                put(g, x, 9, S)
                put(g, x, 39, S)
        for y in range(9, 40):
            if (y // 2) % 2 == 0:
                put(g, 18, y, S)
                put(g, 45, y, S)
        for d in range(-9, 10):
            fill(g, 31 + d, 23, 33 + d, 25, 6 if abs(d) < 5 else 7)
            fill(g, 31, 23 + d, 33, 25 + d, 6 if abs(d) < 5 else 7)
        for d in range(-5, 6):
            put(g, 32 + d, 24 + d, 7)
            put(g, 32 + d, 24 - d, 7)
        fill(g, 31, 23, 34, 26, 1)
        fill(g, 32, 24, 33, 25, 6)
    elif stem == "abc":
        glyph(g, 10, 17, BIGA, S, 2)
        glyph(g, 41, 17, BIGZ, S, 2)
        fill(g, 25, 24, 37, 26, 6)
        for i in range(4):
            fill(g, 36 - i, 21 + i, 37 - i, 22 + i, 6)
            fill(g, 36 - i, 28 - i, 37 - i, 29 - i, 6)
    elif stem == "type":
        tc = type_colours()
        ts = ["FIGHTING", "FLYING", "FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC"]
        for k, t in enumerate(ts):
            p[9 + k] = tc[t] if k < 7 else p[9 + k]
        p[9:16] = [tc[t] for t in ts]
        cells = [[9, 10, 11], [12, 13, 14], [15, 9, 12]]
        for j in range(3):
            for i in range(3):
                x, y = 17 + 10 * i, 9 + 10 * j
                fill(g, x - 1, y - 1, x + 9, y + 9, S)
                fill(g, x, y, x + 8, y + 8, cells[j][i])
        p[10] = tc["FLYING"]
    elif stem == "lightest":
        line(g, 32, 12, 32, 36, S, 2)
        fill(g, 24, 36, 41, 38, S)
        line(g, 12, 22, 52, 14, S, 1)                        # the beam, tipped: the right side is up
        line(g, 12, 23, 52, 15, Sm, 1)
        for (x, y, h) in ((12, 22, 9), (52, 14, 7)):
            line(g, x, y, x, y + h, Sm, 1)
            fill(g, x - 6, y + h, x + 7, y + h + 1, S)
        fill(g, 7, 26, 17, 31, Sm)                           # the heavy side's weight
        line(g, 49, 17, 55, 19, 6, 1)                        # and a mark of almost nothing, lit
    elif stem == "smallest":
        for r, v in ((15, S), (10, Sm), (5, 6)):
            cut_box(g, 32 - r, 24 - r, 2 * r, 2 * r, 2 if r > 5 else 0, [v], None)
        fill(g, 29, 21, 35, 27, 6)
    elif stem == "cancel":
        fill(g, 40, 10, 45, 30, S)
        fill(g, 20, 26, 45, 31, S)
        for i in range(8):
            fill(g, 19 + i, 28 - i, 20 + i, 29 + i, S)
        fill(g, 41, 11, 44, 29, Sm)
        fill(g, 22, 27, 44, 30, Sm)
    return g, p


CAT_ORDER = ["numerical", "grassland", "forest", "waters_edge", "sea", "cave", "mountain", "rough_terrain", "urban",
             "rare", "abc", "type", "lightest", "smallest", "cancel"]


def cat_icon_now(stem):
    w, h, p, px = png("pokedex/cat_icon_%s.png" % stem)
    return low(px), pal("pokedex/cat_icon_%s.pal" % stem) if os.path.exists(src("pokedex/cat_icon_%s.pal" % stem)) else p[:16]


def dex_row0():
    return pal("pokedex/kanto_dex_bgpals.pal")[0:16]


def dex_backdrop():
    w, h, p, px = png("pokedex/kanto_dex_bgtiles.png")
    rows = [pal("pokedex/kanto_dex_bgpals.pal")[i * 16:(i + 1) * 16] for i in range(16)]
    ents = [(14, 0, 0, 0)] * (32 * 20)
    return render_map(low(px), 1, ents, 32, 20, rows)


def index_mock(direction, stem="sea"):
    """The INDEX's TABLE OF CONTENTS with one row chosen: the list (dark on the light backdrop), the counts, the
    chosen row's icon at (21,11)."""
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    bd = dex_backdrop()
    im.paste(bd, (0, 0), bd)
    rows = [pal("pokedex/kanto_dex_bgpals.pal")[i * 16:(i + 1) * 16] for i in range(16)]
    r0, r15 = rows[0], rows[15]
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 239, 15], fill=q5(r15[15]))
    d.rectangle([0, 144, 239, 159], fill=q5(r15[15]))
    t = cstr("gText_PokedexTableOfContents")
    say(im, (240 - text_width(t)) // 2, 0, t, r15[1], r15[2])
    say(im, 236 - text_width("PICK OK", True) - 20, 146, "PICK  OK", r15[1], r15[2], small=True)
    text = strings_c()
    items = [("gText_PokemonList", True), ("gText_NumericalMode", False), ("gText_PokemonHabitats", True)] + \
            [(c[1], False) for c in [x for x in CATS if x[0] not in ("numerical", "abc", "type", "lightest",
                                                                       "smallest", "cancel")]]
    first = [i for i, (n, h) in enumerate(items) if n == dict((c[0], c[1]) for c in CATS)[stem]]
    top = max(0, (first[0] if first else 0) - 4)
    for i, (n, hdr) in enumerate(items[top:top + 8]):      # 16 tiles tall: eight rows
        y = 16 + 2 + 16 * i - 2
        s = cstr(n, text)
        say(im, 8 + (0 if hdr else 12), y, s, r0[6] if hdr else r0[1], r0[5] if hdr else r0[8])
        if (top + i) in first:
            cursor_tri(im, 8 + 4, y + 4, r0[1])
    say(im, 168, 16 + 9, cstr("gText_Seen", text), r0[1], r0[8])
    say(im, 168 + 32 + 8, 16 + 21, "142", r0[1], r0[8])
    say(im, 168, 16 + 37, cstr("gText_Owned", text), r0[1], r0[8])
    say(im, 168 + 32 + 8, 16 + 49, " 98", r0[1], r0[8])
    if direction is None:
        g, p = cat_icon_now(stem)
    else:
        g, p = cat_icon(stem)
    ic = idx_rgba(g, p)
    im.paste(ic, (168, 88), ic)
    return im


def icons_plate(direction, stems):
    """All fifteen icons at 2/3 size, five across, on the INDEX's backdrop."""
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    bd = dex_backdrop()
    im.paste(bd, (0, 0), bd)
    for k, stem in enumerate(stems):
        g, p = cat_icon_now(stem) if direction is None else cat_icon(stem)
        ic = idx_rgba(g, p).resize((44, 33), Image.NEAREST)
        x, y = 4 + (k % 5) * 47, 4 + (k // 5) * 52
        im.paste(ic, (x, y), ic)
    return im


# ================================================================================================ the AREA map
AREA_MAPS = [("map_kanto", 96, 72), ("map_one_island", 32, 24), ("map_two_island", 32, 24),
             ("map_three_island", 32, 24), ("map_four_island", 32, 32), ("map_five_island", 32, 32),
             ("map_six_island", 32, 32), ("map_seven_island", 32, 32)]


def area_classes(stem):
    """Vanilla's pixel classes, where they are: F frame, O outside, L land, S sea, R route, T town, E route edge.
    A '.' (5) inside the frame is a road; four of them square is a town (vanilla's towns are 6px boxes)."""
    w, h, p, px = png("pokedex/%s.png" % stem)
    v = low(px)
    cls = [["O"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            c = v[y][x]
            cls[y][x] = {2: "F", 6: "L", 7: "S", 3: "E"}.get(c, "R" if c == 5 else "O")
    # the frame's corners and the outside (5 beyond the frame) stay outside: a 5 is a road only inside the frame
    for y in range(h):
        row = v[y]
        xs = [x for x in range(w) if row[x] == 2]
        for x in range(w):
            if row[x] == 5 and (not xs or x < min(xs) or x > max(xs) or y < 2 or y > h - 3):
                cls[y][x] = "O"
            if row[x] == 3 and (y <= 2 or y >= h - 3 or x <= 1 or x >= w - 2):
                cls[y][x] = "F"
    town = [[False] * w for _ in range(h)]
    for y in range(h - 3):
        for x in range(w - 3):
            if all(cls[y + j][x + i] == "R" for j in range(4) for i in range(4)):
                for j in range(4):
                    for i in range(4):
                        town[y + j][x + i] = True
    for y in range(h):
        for x in range(w):
            if town[y][x]:
                cls[y][x] = "T"
    return cls, v


def area_draw(stem, direction):
    """The map in the INDEX's row 0 (it prints with that row): never slot 8 (the weekday), the sea on 7 (the hour)."""
    cls, v = area_classes(stem)
    if direction is None:
        return v
    h, w = len(cls), len(cls[0])
    g = canvas(w, h, 5)
    near = lambda x, y, k: any(0 <= x + dx < w and 0 <= y + dy < h and cls[y + dy][x + dx] == k
                               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    for y in range(h):
        for x in range(w):
            c = cls[y][x]
            if c == "O":
                g[y][x] = v[y][x]
            elif c == "F":
                g[y][x] = 2 if direction == "A" else 14
            elif c == "S":
                g[y][x] = 7
                if direction == "A" and x % 4 == 2 and y % 4 == 2:
                    g[y][x] = 0
            elif c in ("L", "E"):
                if near(x, y, "S"):
                    g[y][x] = 12 if direction == "A" else 6           # the coast: a slate rule / an ink line
                elif direction == "A":
                    g[y][x] = 11 if (x % 4 == 3 and y % 2 == 0) or (y % 4 == 3 and x % 2 == 0) else 9
                else:
                    g[y][x] = 11 if (y % 12) in (1, 3, 5, 7, 9) else 9  # SCORE: the land is staff lines
            elif c == "R":
                g[y][x] = 2 if direction == "A" else 14
            elif c == "T":
                g[y][x] = 14 if direction == "A" else 9
    if direction == "A":                                     # a town: a slate square, its middle white
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if cls[y][x] == "T" and all(cls[y + dy][x + dx] == "T" for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    g[y][x] = 5
    else:                                                    # SCORE: towns are noteheads, routes barred
        seen = set()
        for y in range(h):
            for x in range(w):
                if cls[y][x] == "T" and (x, y) not in seen:
                    pts = []
                    st = [(x, y)]
                    while st:
                        a, b = st.pop()
                        if (a, b) in seen or not (0 <= a < w and 0 <= b < h) or cls[b][a] != "T":
                            continue
                        seen.add((a, b))
                        pts.append((a, b))
                        st += [(a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)]
                    cx = sum(p[0] for p in pts) / len(pts) + 0.5
                    cy = sum(p[1] for p in pts) / len(pts) + 0.5
                    for a, b in pts:
                        dx, dy = (a + 0.5 - cx), (b + 0.5 - cy)
                        u, vv = dx * 0.87 + dy * 0.5, -dx * 0.5 + dy * 0.87
                        if (u / 3.4) ** 2 + (vv / 2.4) ** 2 <= 1:
                            g[b][a] = 6
                        else:
                            g[b][a] = 9
        for y in range(h):                                   # a barline across a road every 6px
            for x in range(w):
                if cls[y][x] == "R":
                    horiz = (x + 1 < w and cls[y][x + 1] == "R") and (x - 1 >= 0 and cls[y][x - 1] == "R")
                    if horiz and x % 6 == 0:
                        for dy in (-1, 2):
                            if 0 <= y + dy < h and cls[y + dy][x] in ("E",):
                                g[y + dy][x] = 14
    return g


def area_mock(direction):
    """The AREA page: the frame vanilla draws, the map at (17,4)+4 rows, AREA, the daemon, and a species' markers
    (four of them: ROUTE 1, ROUTE 2, ROUTE 22, VIRIDIAN FOREST) as the code places them."""
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    bd = dex_backdrop()
    im.paste(bd, (0, 0), bd)
    rows = [pal("pokedex/kanto_dex_bgpals.pal")[i * 16:(i + 1) * 16] for i in range(16)]
    r0, r15 = rows[0], rows[15]
    w, h, p, px = png("pokedex/kanto_dex_bgtiles.png")
    tiles = low(px)
    frame = []
    for ty in range(20):
        for tx in range(30):
            t, hf, vf = 0, 0, 0
            if ty == 2 or ty == 17:
                t, vf = (4 if tx in (0, 29) else 5), (1 if ty == 17 else 0)
                hf = 1 if tx == 29 else 0
            elif 2 < ty < 17:
                t, hf = (6, 1 if tx == 29 else 0) if tx in (0, 29) else (1, 0)
            frame.append((t, hf, vf, 0))
    fr = render_map(tiles, 1, frame, 30, 20, rows)
    im.paste(fr, (0, 0), fr)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 239, 15], fill=q5(r15[15]))
    d.rectangle([0, 144, 239, 159], fill=q5(r15[15]))
    g = area_draw("map_kanto", direction)
    mp = idx_rgba(g, r0, clear0=False)
    im.paste(mp, (136, 64), mp)
    a = cstr("gText_Area")
    say(im, 144 + (80 - text_width(a, True)) // 2, 48 + 4, a, r0[1], r0[8], small=True)
    names = M.species_names()
    say(im, 40, 16, "No.016", r0[1], r0[8], small=True)
    say(im, 43, 28, names.get("PIDGEY", "PIDGEY"), r0[1], r0[8])
    ic = M.icon("PIDGEY")
    im.paste(ic, (8, 16), ic)
    mk = pal("pokedex/area_markers/marker.pal")
    for (kind, mx, my) in ((2, 54, 32), (2, 54, 16), (1, 40, 28), (0, 51, 20)):
        mw, mh, mp_, mpx = png("pokedex/area_markers/marker_%d.png" % kind)
        mi = idx_rgba(low(mpx), mk)
        im.paste(mi, (104 + mx, 64 + my), mi)
    return im


def area_family(direction):
    """All eight maps: KANTO at 1.5x and at real size, the seven islands at real size along the foot."""
    im = Image.new("RGB", (240, 160), (24, 26, 30))
    r0 = dex_row0()
    g = area_draw("map_kanto", direction)
    k = idx_rgba(g, r0, clear0=False)
    im.paste(k.resize((144, 108), Image.NEAREST), (4, 4))
    im.paste(k, (152, 4))
    for i, (stem, w, h) in enumerate(AREA_MAPS[1:]):
        t = idx_rgba(area_draw(stem, direction), r0, clear0=False)
        im.paste(t, (4 + 34 * i, 120))
    return im


# ================================================================================================ the TRAP TABLE's pocket
POUCH_PAL = [(0, 0, 0), SLATE_OUT, SLATE_MID, SLATE_LIGHT, (64, 76, 92), PAPER, (220, 226, 232), TEAL, TEAL_DK,
             (230, 112, 96), (168, 64, 56), (232, 184, 88), (160, 112, 40), (120, 168, 216), (64, 104, 160),
             (16, 20, 26)]


def pouch_art(direction):
    """berry_pouch.png, 64x64: the TRAP TABLE drawn as what it is -- a table of traps. A: a slate tray in 3/4 view,
    cut at 45 degrees, its bed ruled into a 3x2 table of cells, a TRAP set in four of them (a sprung jaw, in the
    traps' own hues) and two empty, the teal bracket on its rail. It stands on the plinth the T-530 page drew."""
    if direction is None:
        w, h, p, px = png("berry_pouch/berry_pouch.png")
        return low(px), p[:16]
    g = canvas(64, 64)
    # the tray's front face (y 44-55) and its bed seen from above (y 18-44, narrower at the back)
    for y in range(18, 45):
        inset = (44 - y) // 4
        for x in range(4 + inset, 60 - inset):
            g[y][x] = 6
    for y in range(18, 45):
        inset = (44 - y) // 4
        put(g, 4 + inset, y, 2)
        put(g, 59 - inset, y, 2)
    for x in range(10, 54):
        put(g, x, 18, 2)
    for y in range(45, 56):                                  # the front, cut at its bottom corners
        for x in range(4, 60):
            g[y][x] = 4 if y > 52 else 2
    for i in range(3):
        for j in range(i + 1):
            put(g, 4 + j, 55 - (2 - i), 0)
            put(g, 59 - j, 55 - (2 - i), 0)
    for x in range(5, 59):
        put(g, x, 45, 3)                                     # the front's lit rail
    bracket(g, 7, 47, 7, 4)
    # the table: 3 columns x 2 rows of cells, ruled
    cells = []
    for r, (ya, yb) in enumerate(((20, 31), (32, 43))):
        for c in range(3):
            def xat(y, f):
                inset = (44 - y) // 4
                return 4 + inset + 2 + int((56 - 2 * inset - 4) * f)
            cells.append((r, c, ya, yb, lambda y, c=c: (xat(y, c / 3.0) + 1, xat(y, (c + 1) / 3.0) - 1)))
    for y in range(20, 44):
        inset = (44 - y) // 4
        for c in (1, 2):
            x = 4 + inset + 2 + int((56 - 2 * inset - 4) * c / 3.0)
            put(g, x, y, 3)
    for x in range(8, 57):
        put(g, x, 31, 3)
    # the traps: a sprung jaw (two arcs of teeth over a plate), in four hues; two cells empty
    hues = {(0, 0): (9, 10), (0, 2): (11, 12), (1, 1): (13, 14), (1, 2): (7, 8)}
    for (r, c, ya, yb, xs) in cells:
        if (r, c) not in hues:
            continue
        a, b = xs((ya + yb) // 2)
        cx, cy = (a + b) // 2, (ya + yb) // 2
        lit, dk = hues[(r, c)]
        fill(g, cx - 4, cy + 1, cx + 5, cy + 3, 15)          # its plate, dark
        for i in range(-4, 5):
            yy = cy - 1 - int(round(2.2 * (1 - (i / 4.5) ** 2)))
            put(g, cx + i, yy, lit)
            put(g, cx + i, yy + 1, dk)
            if i % 2 == 0:
                put(g, cx + i, yy + 2, 5)                    # its teeth
        put(g, cx, cy - 4, 5)
    outline(g, 1)
    return g, POUCH_PAL


def pouch_mock(direction):
    """The TRAP TABLE screen as T-530's first pass built it (gbamenus A), with this pocket picture on its plinth."""
    sheet, per, rows, ents = M.item_build("berry", "A")
    im = Image.new("RGB", (240, 160), q5(rows[0][0]))
    b = render_map(low(sheet), per, ents, 32, 20, rows)
    im.paste(b, (0, 0), b)
    names, counts, ic, desc, (lx, ly) = M.ITEM_CONTENT["berry"]
    std = std_pal(0)
    for i, (n, c) in enumerate(zip(names, counts)):
        y = ly + 16 * i - 2
        if i == 1:
            cursor_tri(im, lx + 2, y + 4, std[2])
        say(im, lx + 9, y, n, std[2], std[3])
        if c is not None:
            say(im, lx + 136 - text_width("%d" % c) - 8, y, "x", std[2], std[3], small=True)
            say(im, lx + 136 - text_width("%d" % c), y, "%d" % c, std[2], std[3])
    w2 = std_pal(2)
    sy = M.ITEM_SCREENS["berry"]["strip_y"]
    for i, l in enumerate(desc):
        say(im, 40, sy + 2 + 14 * i, l, w2[1], w2[2])
    a, b_, c, d_ = M.ITEM_SCREENS["berry"]["icon"]
    it = M.item_icon(ic)
    im.paste(it, (a + (c - a - 24) // 2, b_ + (d_ - b_ - 24) // 2), it)
    g, p = pouch_art(direction)
    bp = idx_rgba(g, p)
    im.paste(bp, (12, 44), bp)
    say(im, 10, 6, "TRAP TABLE", std[2], std[3])
    return im


# ================================================================================================ the party's hold marks
HOLD_PAL = [(0, 0, 0), SLATE_OUT, PAPER, SLATE_LIGHT, TEAL, TEAL_DK, AMBER, AMBER_DK, (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (98, 98, 98)]


def hold_art(direction):
    """hold_icons.png, 8x16: tile 0 the held-item mark, tile 1 the mail mark. A: a teal tag with a paper eyelet, and
    a folded note (paper, a slate rim, the flap's crease, an amber seal). Both sit on the daemon's icon, on light
    cards and dark: the slate rim carries them on either."""
    if direction is None:
        w, h, p, px = png("party_menu/hold_icons.png")
        return low(px), p[:16]
    tag = ["..111111",                                       # a tag on its eyelet: teal, its shade, slate
           ".1444441",
           "14424441",
           "14444441",
           ".1555551",
           "..111111",
           "........",
           "........"]
    mail = ["11111111",                                      # a folded note: paper, the flap's crease, a seal
            "13222231",
            "12322321",
            "12266221",
            "12222221",
            "11111111",
            "........",
            "........"]
    g = canvas(8, 16)
    for y, r in enumerate(tag + mail):
        for x, ch in enumerate(r):
            g[y][x] = 0 if ch == "." else int(ch)
    return g, HOLD_PAL


def holds_mock(direction):
    """The party screen as T-530 built it, two daemons holding something: an item (slot 0) and a mail (slot 2)."""
    im = M.party_mock("A")
    g, p = hold_art(direction)
    item = idx_rgba(g[0:8], p)
    mail = idx_rgba(g[8:16], p)
    im.paste(item, (20 - 4, 50 - 4), item)
    im.paste(mail, (108 - 4, 52 - 4), mail)
    im.paste(item, (108 - 4, 100 - 4), item)
    return im


# ================================================================================================ the PC's parts
PS = "pokemon_storage"


def misc(n):
    return list(pal("%s/misc%d.pal" % (PS, n)))


def pc_pals(direction):
    m1, m2 = misc(1), misc(2)
    if direction is None:
        return m1, m2
    # misc1: the box menu's 4 (paper) 5 (rule light) 6 (rule) 7 (rule dark), its text 15 on 14
    m1[4], m1[5], m1[6], m1[7] = PAPER, SLATE_LIGHT, SLATE_MID, SLATE_OUT
    m1[14], m1[15] = (200, 204, 208), (64, 72, 84)
    # misc2: the scroll arrows' 13/14 (15 shared with the PAW's shadow: kept); the waveform's 4-7 (8 kept)
    m2[13], m2[14] = TEAL, SLATE_LIGHT
    m2[4], m2[5], m2[6], m2[7] = (20, 34, 38), TEAL, (184, 240, 208), (40, 72, 64)
    return m1, m2


def box_menu_art(direction):
    """choose_box_menu_center (64x64, a 64x64 sprite at 160,96) and _corners (16x48: 8x32 frames 0/6 at the top,
    8x16 frames 4/10 at the bottom). The box name prints in 15 on 14 at tile row 1, the count on row 3 -- on 4."""
    if direction is None:
        return low(png(PS + "/choose_box_menu_center.png")[3]), low(png(PS + "/choose_box_menu_corners.png")[3])
    # the whole popup as one picture, x 120-200, y 64-120 (the corners' reach), then cut into the two sheets
    W, H = 80, 64
    full = canvas(W, H)
    cut_box(full, 0, 0, W, 48, 5, [7, 5], 4)
    for i in range(5):
        put(full, 3 + i, 2, 6)
        put(full, 2, 3 + i, 6)
    for x in range(12, 68, 2):
        put(full, x, 23, 5)                                  # a dotted rule between the name and the count
    center = canvas(64, 64)
    for y in range(64):
        for x in range(64):
            center[y][x] = full[y][x + 8] if y < H else 0
    corners = canvas(16, 48)
    # frame 0: tiles 0-3 (8x32: x 120-128, y 64-96); frame 4: tiles 4-5 (8x16 at y 104-120); frame 6: tiles 6-9
    # (x 192-200, y 64-96); frame 10: tiles 10-11 (y 104-120). Tile n sits at ((n % 2) * 8, (n // 2) * 8).
    def put_frame(t0, ntiles, fx, fy):
        for k in range(ntiles):
            t = t0 + k
            for y in range(8):
                for x in range(8):
                    sy = fy + k * 8 + y
                    corners[(t // 2) * 8 + y][(t % 2) * 8 + x] = full[sy][fx + x] if 0 <= sy < H else 0
    put_frame(0, 4, 0, 0)
    put_frame(4, 2, 0, 40)
    put_frame(6, 4, 72, 0)
    put_frame(10, 2, 72, 40)
    return center, corners


def scroll_arrow_art(direction):
    """box_scroll_arrow.png 8x32: frame 0 (tiles 0-1) points left, frame 1 (tiles 2-3) right. A: a 45-degree
    chevron, teal (13) on a slate rule (14), outlined in 15 (kept)."""
    if direction is None:
        return low(png(PS + "/box_scroll_arrow.png")[3])
    g = canvas(8, 32)
    for f, flip in ((0, False), (1, True)):
        y0 = f * 16
        for i in range(5):
            for t in (0, 1):
                x = 2 + i + t
                for yy in (y0 + 3 + i, y0 + 12 - i):
                    if 0 <= x < 8:
                        put(g, (7 - x) if not flip else x, yy, 13 if t == 0 else 14)
        snap = [r[:] for r in g[y0:y0 + 16]]
        for y in range(16):
            for x in range(8):
                if snap[y][x] == 0 and any(0 <= x + dx < 8 and 0 <= y + dy < 16 and snap[y + dy][x + dx] in (13, 14)
                                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    g[y0 + y][x] = 15
    return g


def waveform_art(direction):
    """waveform.png 16x56, seven 16x8 frames: 0 the left meter off, 1-3 on (with 2 shared by the right), 4 the right
    off, 5-6 on. A: a dark glass (4) with a teal trace (5, its glow 7); off, a flat line."""
    if direction is None:
        return low(png(PS + "/waveform.png")[3])
    g = canvas(16, 56)
    shapes = {0: None, 1: 0.0, 2: 1.6, 3: 3.2, 4: None, 5: 4.8, 6: 0.8}
    for f in range(7):
        y0 = f * 8
        cut_box(g, 0, y0, 16, 8, 1, [8], 4)
        ph = shapes[f]
        for x in range(1, 15):
            if ph is None:
                yy = 4
            else:
                yy = 4 + int(round(2.2 * math.sin(x / 1.6 + ph) * math.sin(math.pi * x / 15)))
            put(g, x, y0 + yy, 5)
            if ph is not None and 0 < yy < 7:
                put(g, x, y0 + yy + (1 if yy < 4 else -1), 7)
    return g


DATA_SLOTS = {1: (146, 158, 172), 2: (104, 116, 130), 3: (64, 76, 92), 4: (184, 196, 208), 6: TEAL,
              12: (52, 66, 82), 13: (34, 44, 56)}
#  Row 0 (interface.pal) slot by slot: 1/2/3 the panel's greys, also the label's and CLOSE BOX's (retinted to the same
#  lightness in slate, so both stay as drawn); 4, 6, 12 and 13 are the panel's alone; 5/10/14 the label's and 8/9/11
#  CLOSE BOX's glass blue, kept. Row 2 (interface_no_display_mon.pal) is the label's with no daemon shown: 1/2/3 too.


def data_panel_target(ents, sheet, per):
    """The DATA panel (menu.bin columns 0-9, palette 0), in row 0's slots. Rows 0-1 are the label strip as drawn (its
    ends are hidden under the waveform sprites); below it a slate column with its rule, the glass the daemon stands
    in as dark graph paper with the teal bracket, and a rule round the paper window 0 prints the daemon's name on
    (0,11 9x7, palette 3: its own colours, which cover the tiles under it)."""
    g = canvas(256, 160, 0)
    for i, (t, hf, vf, pn) in enumerate(ents):
        cx, cy = (i % 32) * 8, (i // 32) * 8
        if t and cy < 16:
            blk = get_tile_low(sheet, t, per)
            for y in range(8):
                for x in range(8):
                    g[cy + y][cx + x] = blk[7 - y if vf else y][7 - x if hf else x]
    # menu.bin's own grid decides every edge: the glass's fill tiles (11c, 11d, 127, 121) are one tile repeated -- and
    # 127 is both the old right edge and the old bottom -- so the glass is one 8px-periodic fill, its edges in the
    # tiles that are each used once (10b/10e on top, 11b/120 and 11e/122 at the sides, 130/132/131/123 below).
    fill(g, 0, 16, 80, 160, 4)
    for y in range(16, 160):
        g[y][77], g[y][78], g[y][79] = 1, 2, 3               # the column's rule
    cut_box(g, 9, 18, 67, 66, 3, [3, 2], 13)                 # the glass: x 9-75, y 18-83
    for y in range(20, 82):
        for x in range(11, 74):
            if g[y][x] == 13 and ((x % 8 == 3 and y % 2 == 0) or (y % 8 == 3 and x % 2 == 0)):
                g[y][x] = 12
    for i in range(4):                                       # the bracket, in the glass's top-left corner tile
        put(g, 12 + i, 21, 6)
        put(g, 12, 21 + i, 6) if i < 3 else None
    for x in range(0, 75):                                   # the rule over window 0's paper (row 10's foot)
        g[86][x], g[87][x] = 3, 2
        g[152][x], g[153][x] = 2, 3                          # and under it (row 19; row 18 is the window's tile)
    for y in range(86, 154):
        g[y][73], g[y][74] = 2, 3
    return g


def get_tile_low(sheet, t, per):
    x0, y0 = (t % per) * 8, (t // per) * 8
    return [[sheet[y0 + y][x0 + x] & 15 for x in range(8)] for y in range(8)]


def data_build(direction):
    w, h, p, px = png(PS + "/menu.png")
    sheet = [list(r) for r in px]
    per = w // 8
    ents = [(t - 256 if t >= 256 else t, hf, vf, pn) for t, hf, vf, pn in m16(PS + "/menu.bin")]
    r0 = list(pal(PS + "/interface.pal"))
    r2 = list(pal(PS + "/interface_no_display_mon.pal"))
    if direction is None:
        return sheet, per, r0, r2, ents, (0, 0)
    label = set(e[0] - 256 if e[0] >= 256 else e[0] for e in m16(PS + "/pkmn_data.bin"))
    sub = [e if (i % 32) < 10 and e[0] not in label else (0, 0, 0, 0) for i, e in enumerate(ents)]
    miss = retile(sheet, per, [(sub, 32, data_panel_target(ents, sheet, per))])
    for k, v in DATA_SLOTS.items():
        r0[k] = v
    for k in (1, 2, 3):
        r2[k] = DATA_SLOTS[k]
    return sheet, per, r0, r2, ents, miss


def data_layer(direction, shown=True):
    """The DATA column as the engine draws it, with a daemon shown (row 0 under the label) or none (row 2)."""
    sheet, per, r0, r2, ents, miss = data_build(direction)
    label = set(e[0] - 256 if e[0] >= 256 else e[0] for e in m16(PS + "/pkmn_data.bin"))
    rows = [r0, r0, r2]
    sub = [(e[0], e[1], e[2], (0 if shown or e[0] not in label else 2)) if (i % 32) < 10 else (0, 0, 0, 0)
           for i, e in enumerate(ents)]
    return render_map(low(sheet), per, sub, 32, 20, rows)


def pc_parts_mock(direction, popup=False):
    """The PC as T-530 built it (gbamenus A) with this pass's parts: the scroll arrows by the box title, the waveform
    at the panel's top, and (popup) the box menu up."""
    im = M.pc_mock("A")
    dl = data_layer(direction)
    im.paste(dl, (0, 0), dl)
    fr = M.front("EEVEE")
    im.paste(fr, (8, 16), fr)
    sp = png(PS + "/scrolling_bg.png")[2]                   # window 0: palette 3, the backdrop's 1/2/3
    ImageDraw.Draw(im).rectangle([0, 88, 71, 143], fill=q5(sp[1]))
    nm = M.species_names().get("EEVEE", "EEVEE")
    for k, (t, x) in enumerate(((nm, 6), ("/" + nm, 6), ("{LV}34", 10))):
        say(im, x, 88 + 14 * k, t, sp[2], sp[3])
    m1, m2 = pc_pals(direction)
    ar = scroll_arrow_art(direction)
    for i, f in ((0, 0), (1, 1)):
        a = idx_rgba(ar[f * 16:f * 16 + 16], m2)
        im.paste(a, (92 + i * 136 - 4, 28 - 8), a)
    wf = waveform_art(direction)
    for i, f in ((0, 2), (1, 5)):
        a = idx_rgba(wf[f * 8:f * 8 + 8], m2)
        im.paste(a, (i * 63 + 8 - 8, 9 - 4), a)
    if popup:
        center, corners = box_menu_art(direction)
        c = idx_rgba(center, m1)
        im.paste(c, (128, 64), c)
        for t0, n, x, y in ((0, 4, 120, 64), (4, 2, 120, 104), (6, 4, 192, 64), (10, 2, 192, 104)):
            fr = canvas(8, 8 * n)
            for k in range(n):
                t = t0 + k
                for yy in range(8):
                    for xx in range(8):
                        fr[k * 8 + yy][xx] = corners[(t // 2) * 8 + yy][(t % 2) * 8 + xx]
            f = idx_rgba(fr, m1)
            im.paste(f, (x, y), f)
        s = "BOX 2"
        say(im, 128 + 1, 64 + 8 - 1, s, m1[15], m1[14])
        say(im, 128 + 24, 64 + 24 - 1, " 0/30", m1[15], m1[14])
        for i in range(2):
            a = idx_rgba(ar[i * 16:i * 16 + 16], m2)
            im.paste(a, (72 * i + 124 - 4, 88 - 8), a)
    return im


# ================================================================================================ outputs
def _png(px, palette, bd):
    return ("png", px, [q5(c) for c in palette], bd)


def outputs(screen, direction):
    out = {}
    if screen == "toolkit":
        sheet, per, rows, bg2, bg1, miss = tk_build(direction)
        out["tm_case/tm_case.png"] = _png(low(sheet), rows[0], 4)
        flat = [c for r in rows for c in r]
        out["tm_case/menu_male.pal"] = ("pal", flat)
        out["tm_case/menu_female.pal"] = ("pal", flat)
        cp = card_pals(direction)
        out["tm_case/disc.png"] = _png(card_frames(direction), [(17 * i,) * 3 for i in range(16)], 4)
        out["tm_case/disc_types_1.pal"] = ("pal", [c for r in cp[:16] for c in r])
        out["tm_case/disc_types_2.pal"] = ("pal", cp[16][:len(pal("tm_case/disc_types_2.pal"))])
    elif screen == "shop":
        sheet, per, rows, normal, tmhm, miss = shop_build(direction)
        out["shop_menu/shop_menu.png"] = _png(sheet, [c for r in rows for c in r], 8)
    elif screen == "index":
        for stem in CAT_ORDER:
            g, p = cat_icon(stem)
            out["pokedex/cat_icon_%s.png" % stem] = _png(g, p, 4)
    elif screen == "area":
        r0 = dex_row0()
        for stem, w, h in AREA_MAPS:
            out["pokedex/%s.png" % stem] = _png(area_draw(stem, direction), r0, 4)
    elif screen == "pouch":
        g, p = pouch_art(direction)
        out["berry_pouch/berry_pouch.png"] = _png(g, p, 4)
    elif screen == "holds":
        g, p = hold_art(direction)
        out["party_menu/hold_icons.png"] = _png(g, p, 4)
    elif screen == "pcparts":
        m1, m2 = pc_pals(direction)
        center, corners = box_menu_art(direction)
        out[PS + "/choose_box_menu_center.png"] = _png(center, m1, 4)
        out[PS + "/choose_box_menu_corners.png"] = _png(corners, m1, 4)
        out[PS + "/box_scroll_arrow.png"] = _png(scroll_arrow_art(direction), m2, 4)
        out[PS + "/waveform.png"] = _png(waveform_art(direction), m2, 4)
        out[PS + "/misc1.pal"] = ("pal", m1)
        out[PS + "/misc2.pal"] = ("pal", m2)
        sheet, per, r0, r2, ents, miss = data_build(direction)
        mp = list(png(PS + "/menu.png")[2])[:48]
        mp[0:16] = r0
        out[PS + "/menu.png"] = _png(sheet, mp, 8)
        out[PS + "/interface.pal"] = ("pal", r0)
        out[PS + "/interface_no_display_mon.pal"] = ("pal", r2)
    return out


# ================================================================================================ report, draft, write
NOTES = {
    "toolkit": ["Rows: a PLUGIN chosen (the card risen from the case in its type's colours); the same with the band "
                "dimmed (row 3, while USE/GIVE is up); the second PLUGIN chosen.",
                "Kept: menu.bin and tm_case.bin (tiles redrawn in place), the four palette rows and their roles (0 upper, "
                "1 lower band, 2 the case, 3 the band dimmed), the card's 2 frames and 17 type rows; the case is in "
                "front of the card (BG1 priority 0), so nothing is drawn above its slot where a card passes."],
    "shop": ["Rows: the MART (VIRIDIAN's stock, the overworld seen through at left); the same with the how-many box "
             "up (the band on palette 6); the PLUGIN shop's frame.",
             "Kept: both tilemaps (28 tiles shared, redrawn in place), row 0 as palette 11 and row 1 as 6; the list's "
             "paper light (dark ink) and the band dark (WHITE description); the item's bay and the move's card light."],
    "index": ["Rows: the TABLE OF CONTENTS with STREAM chosen (the icon at 21,11); with KERNEL chosen; all fifteen "
              "plates (shown at 2/3 size on the INDEX's backdrop).",
              "Kept: 64x48, 4bpp, each icon its own 16 colours loaded into BG row 1 (nothing else on the page uses "
              "row 1); index 0 outside the cut corners. cat_icon_qmark is unreferenced: left as it is."],
    "area": ["Rows: the AREA page with a daemon's four places (the markers where the code puts them); the eight maps "
             "(KANTO at 1.5x and at real size, the seven islands at real size).",
             "Kept: every map's size and its pixel CLASSES where vanilla had them (the frame, sea, land, routes, "
             "towns), so each marker still lands on its place; drawn in the INDEX's row 0, off slot 8 (T-481 B's "
             "weekday), the sea on 7 (the hour, as vanilla's sea)."],
    "pouch": ["Rows: the TRAP TABLE (T-530's first pass) with the pocket picture on its plinth; the picture at 2x.",
              "Kept: 64x64, its own palette, where the code places it (the plinth drawn for it in the first pass)."],
    "holds": ["Rows: the party screen (T-530), the first daemon holding an item, the third holding mail, the fifth an "
              "item; the marks at 8x.", "Kept: 8x16, two 8x8 tiles in the same order (item, mail), its own palette."],
    "pcparts": ["Rows: the PC (T-530) with the scroll arrows by the box title and the waveform at the DATA panel's top; "
                "the box menu up (BOX 2, the arrows either side).",
                "Kept: every sheet's size and frame order; misc1 4-7 and 14/15 (the box menu, its text 15 on 14); misc2 "
                "4-7 (the waveform) and 13/14 (the arrows) -- misc2 8 and 15 are the PAW's shadow's and stay; the PAW's "
                "own slots untouched. The DATA panel: menu.png's 29 tiles of menu.bin columns 0-9 redrawn in place (the label's "
                "16 tiles, pkmn_data's, are kept as drawn), interface.pal's 4/6/12/13 its own, 1/2/3 retinted to slate at "
                "the same lightness (CLOSE BOX and the label share them)."],
}


def report():
    print("T-530 second pass: APPROVED = %r" % APPROVED)
    for d in ("A",):
        sheet, per, rows, bg2, bg1, (miss, n) = tk_build(d)
        print("  TOOLKIT %s: %d tile ids redrawn in place, %d uses differ from their vote" % (d, n, miss))
        print("    title WHITE on plate: %3.0f / %3.0f   list ink on paper: %3.0f / %3.0f   description WHITE on band: "
              "%3.0f / %3.0f (dimmed %3.0f)" % (lum(std_menu()[1]), lum(rows[0][9]), lum(std_menu()[2]), lum(rows[0][7]),
                                               lum(std_menu()[1]), lum(rows[1][8]), lum(rows[3][8])))
        cp = card_pals(d)
        worst = min(abs(lum(r[3]) - lum(r[1])) for r in cp)
        print("    cards: 17 type rows; the least lightness between a card and its outline %3.0f" % worst)
        sheet, per, rows, normal, tmhm, (miss, n) = shop_build(d)
        print("  SHOP %s: %d tiles redrawn in place, %d uses differ   ink on paper %3.0f/%3.0f, WHITE on band %3.0f/%3.0f"
              % (d, n, miss, lum(std_menu()[2]), lum(rows[0][5]), lum(std_pal(2)[1]), lum(rows[0][8])))
        for stem in CAT_ORDER:
            g, p = cat_icon(stem)
            used = sorted(set(v for r in g for v in r))
            assert len(p) <= 16 and max(used) < 16
        print("  INDEX A: 15 icons, 64x48, <= 16 colours each")
    r0 = dex_row0()
    for d in ("A", "B"):
        used = set()
        for stem, w, h in AREA_MAPS:
            g = area_draw(stem, d)
            used |= set(v for r in g for v in r)
        print("  AREA %s: row-0 slots used %s%s" % (d, sorted(used), "  -- uses 8, T-481 B's weekday!" if 8 in used else ""))
    sheet, per, r0, r2, ents, (miss, n) = data_build("A")
    print("  PCPARTS A: the DATA panel's %d tiles redrawn in place (%d uses differ); the label's 16 and CLOSE BOX's kept"
          % (n, miss))
    m1, m2 = pc_pals("A")
    print("  PCPARTS A: box name %3.0f on %3.0f; misc2 8/15 kept %s/%s" % (lum(m1[15]), lum(m1[4]), m2[8], m2[15]))
    print("  RUN-TIME: HALFTONE greys all of these; TOOLKIT rows 1/3 swap (shade); SHOP rows 0/1 as palettes 11/6; "
          "INDEX row 0 slots 7/8 (T-481 B); misc1/misc2 shared with the PAW")
    return 0


def draft(out):
    os.makedirs(out, exist_ok=True)
    made = []
    for screen in SCREENS:
        for d in OFFERED[screen]:
            put_files(outputs(screen, d), os.path.join(out, d, "graphics"))

    def cols(fn, offered):
        c = [("ENGINE NOW", fn(None))]
        for d in offered:
            c.append(("%s %s" % (d, {"A": "TERMINAL", "B": "SCORE"}[d]), fn(d)))
        return c
    sheets = [
        ("toolkit", "T-530 PASS 2 -- THE TOOLKIT (TM case) -- DRAFT",
         lambda d: [tk_mock(d, 0), tk_mock(d, 0, True), tk_mock(d, 2)]),
        ("shop", "T-530 PASS 2 -- THE SHOP (MART) -- DRAFT",
         lambda d: [shop_mock(d), shop_mock(d, dimmed=True), shop_mock(d, tm=True)]),
        ("index", "T-530 PASS 2 -- THE INDEX's CATEGORY ICONS -- DRAFT",
         lambda d: [index_mock(d, "sea"), index_mock(d, "cave"), icons_plate(d, CAT_ORDER)]),
        ("area", "T-530 PASS 2 -- THE INDEX's AREA MAP -- DRAFT",
         lambda d: [area_mock(d), area_family(d)]),
        ("pouch", "T-530 PASS 2 -- THE TRAP TABLE's POCKET PICTURE -- DRAFT",
         lambda d: [pouch_mock(d), zoom(idx_rgba(*pouch_art(d)), 2)]),
        ("holds", "T-530 PASS 2 -- THE PARTY's HOLD MARKS -- DRAFT",
         lambda d: [holds_mock(d), zoom(idx_rgba(*hold_art(d)), 8)]),
        ("pcparts", "T-530 PASS 2 -- THE PC's BOX MENU, SCROLL ARROWS, WAVEFORM -- DRAFT",
         lambda d: [pc_parts_mock(d), pc_parts_mock(d, True)]),
    ]
    for screen, title, fn in sheets:
        notes = list(NOTES[screen]) + ["DRAFT -- drawn in code (tools/gbamenus2.py), nothing in the engine until the "
                                       "user picks; recommended: " + RECOMMENDED[screen]]
        made.append(contact(title, cols(fn, OFFERED[screen]), notes, os.path.join(out, "%s_sheet.png" % screen)))
    return made


def zoom(img, k):
    """A small sheet at k x, centred on a 240x160 dark plate (for the parts rows)."""
    im = Image.new("RGB", (240, 160), (36, 40, 46))
    z = img.resize((img.width * k, img.height * k), Image.NEAREST)
    im.paste(z, ((240 - z.width) // 2, (160 - z.height) // 2), z)
    return im


def main():
    if ARGS.write:
        if not ARGS.approved or not (ARGS.pick or ARGS.all):
            sys.exit("gbamenus2: --write needs --approved and --all or --pick screen=A|B,... (the user's picks)")
        picks = dict(kv.split("=") for kv in ARGS.pick.split(",")) if ARGS.pick else dict(APPROVED)
        if not picks:
            sys.exit("gbamenus2: nothing approved yet")
        for screen, d in picks.items():
            if screen not in SCREENS or d not in OFFERED[screen]:
                sys.exit("gbamenus2: unknown pick %s=%s (offered: %r)" % (screen, d, OFFERED))
            for p in put_files(outputs(screen, d), G):
                print("  wrote", os.path.relpath(p, ROOT))
        print("  now: build all four ROMs")
        return 0
    if ARGS.draft:
        for p in draft(ARGS.draft):
            print("  wrote", os.path.relpath(p, ROOT))
        return 0
    return report()


if __name__ == "__main__":
    sys.exit(main())
