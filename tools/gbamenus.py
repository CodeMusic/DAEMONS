#!/usr/bin/env python3
"""T-530: the menus -- the party screen, the SUMMARY's bars, the item screens and the PC -- drawn anew, in two directions.

    python3 tools/gbamenus.py                       # report: each screen's engine files, what the drop-in keeps, and
                                                    #   the run-time colour work on it
    python3 tools/gbamenus.py --draft [DIR]         # draw both directions of every screen into DIR
                                                    #   (gfx/drafts/t530_menus/): the files as the engine takes them,
                                                    #   and a contact sheet per screen -- the engine now, A and B, each
                                                    #   a 240x160 mock at real size with real content
    python3 tools/gbamenus.py --write --approved --pick party=A,summary=B,items=A,pc=A
                                                    # write the chosen directions into the engine. Refuses without
                                                    #   --approved, and without a direction for each screen named.

DRAFT, 2026-11-07, from the vanilla-art census's gap 9 ("Menus", the user's pick). Every pixel is drawn in code here, on
the engine's own tile grids: no AI image, nothing traced. The engine's files are read for their SHAPE only -- which tile
id the code and the tilemaps put where, which palette slot the code swaps at run time -- and a drop-in keeps both, so no
.bin, no .c and no palette slot's meaning changes.

THE TWO DIRECTIONS, after the family approved on 2026-11-06 (T-523 A TERMINAL, the field's box; T-524 2 READOUT):
  A  TERMINAL   slate and paper: the field box's rule cut at 45 degrees, the teal corner bracket, ink on paper
  B  READOUT    the battle readout: a dark screen, phosphor text, a graticule, the teal bracket lit

THE SCREENS (most seen first) and what each drop-in keeps -- see SCREENS below and `report()` for the detail:
  PARTY    graphics/party_menu/bg.png: 64 tiles and 11 palette rows. bg.bin and the five slot tilemaps are kept (the
           code blits slot tiles BY ID, party_menu.c BlitBitmapToPartyWindow), so tiles are redrawn IN PLACE. The rows
           3-10 are a palette BUFFER the code copies single colours out of (data/party_menu.h): a box's 4/5/6 and
           1/7/8 per state (empty 3, multi 4, HALTED 5, picked to switch 6, current 7, current multi 8, current HALTED
           9; 1/7/8 of row 6 are the current box's rim, of row 10 the switching rim), the HP bar's 9/10 (green row 3,
           yellow 4, red 5) and the gender's 11/12 (rows 3/4). Text is printed in 3 on 2 (sFontColorTable[0]). The
           cancel button is the bg's own tiles at (23,17), palette 1, and palette 2 when it is chosen.
  SUMMARY  the HP and EXP bars (hp_bar.png, exp_bar.png: 12 sprite tiles, fill frames 0-8 and three caps), its three
           palettes (exp_bar = HP green, hp_bar_yellow, hp_bar_red: only slots 1 and 2 differ), the move cursors, the
           shiny star and the pokerus mark. And the backdrop's palette rows (bg.png's 7), retinted in place -- the
           drawing is not changed, and T-481 B's calendar slots on row 0 keep their roles (6 the line under the title,
           14 the title's pip, 2 the title bar, 3/8/10 the backdrop: data/calendar_panes.h).
  ITEMS    the TM case (TOOLKIT), the berry pouch (TRAP TABLE) and the item PC: their frames, redrawn in place, so the
           list windows the code prints into land where they did.
  PC       the sixteen wallpapers (20x18 tiles each, up to 256 tiles, palette rows 1-2 of their own .gbapal; the box
           name is printed WHITE on a 7,7,7 shadow onto the plate, pokemon_storage_system_graphics.c sBoxTitleColors)
           and the cursor (cursor.png, four 32x32 frames: point, grab, open, hold).

RUN-TIME COLOUR WORK READ BEFORE DRAWING (each one is kept; see report()):
  HALFTONE (fieldmap.c DaemonsGreyHalftoneFrame) greys every palette at the copy to PLTT outside a few kept slots, menus
  included -- so every pair here that must read (ink on paper, a fill on its track, a chosen box on an unchosen one)
  differs in LIGHTNESS, not only in hue; report() measures it.
  T-481 B (daemons_calendar_pane.c) writes the day, a holiday and the hour into the SUMMARY's row 0 (and the text box,
  START and the INDEX, not drawn here). The party, the items and the PC have no calendar pane.
  T-459's purple (palette 15 slot 10) and T-523's frame are the message box's, not these screens': the mocks draw the
  engine's own frame round the party's message.
"""
import argparse, math, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
G = os.path.join(GBA, "graphics")
FONTS = os.path.join(G, "fonts")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t530_menus")

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--pick", help="screen=A|B,... for --write")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes runs the write")
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

RECOMMENDED = {"party": "A", "summary": "A", "items": "A", "pc": "A"}
APPROVED = {}                         # nothing yet: the user picks from the sheets


def q5(c):
    return tuple((v >> 3) << 3 for v in c)


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


# ================================================================================================ files
def load_png(p):
    import gbafont
    w, h, bd, plte, px = gbafont.png_load(p)
    pal = [tuple(plte[i:i + 3]) for i in range(0, len(plte), 3)]
    return w, h, bd, pal, [list(r) for r in px]


def save_png(p, px, pal, bd=4):
    import gbafont
    n = 16 if bd == 4 else 256
    pal = (list(pal) + [(0, 0, 0)] * n)[:max(n, len(pal))]
    if bd == 4:
        pal = pal[:16]
    gbafont.png_save(p, len(px[0]), len(px), bd, b"".join(bytes(q5(c)) for c in pal), px)


def save_png_rows(p, px, rows):
    """A tile sheet whose palette is several 16-colour rows (party bg: 11), as the engine's own png is (8bpp index,
    the low nibble the colour and the high the row the art was drawn in)."""
    import gbafont
    flat = [c for r in rows for c in r]
    gbafont.png_save(p, len(px[0]), len(px), 8, b"".join(bytes(q5(c)) for c in flat), px)


def gbapal(p, n=None):
    d = open(p, "rb").read()
    k = len(d) // 2 if n is None else n
    out = []
    for i in range(k):
        c = struct.unpack_from("<H", d, 2 * i)[0]
        out.append(((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3))
    return out


def jasc(p):
    w = open(p).read().split()
    n = int(w[2])
    v = list(map(int, w[3:3 + 3 * n]))
    return [tuple(v[3 * i:3 * i + 3]) for i in range(n)]


def write_jasc(cols, p):
    with open(p, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(cols))
        for c in cols:
            f.write("%d %d %d\n" % q5(c))


def map16(p):
    d = open(p, "rb").read()
    return [(e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12) for e in struct.unpack("<%dH" % (len(d) // 2), d)]


def map8(p):
    return [(b, 0, 0, None) for b in open(p, "rb").read()]


def get_tile(px, t, per):
    x0, y0 = (t % per) * 8, (t // per) * 8
    return [[px[y0 + y][x0 + x] & 15 for x in range(8)] for y in range(8)]


def put_tile(px, t, per, blk, hi=0):
    x0, y0 = (t % per) * 8, (t // per) * 8
    for y in range(8):
        for x in range(8):
            px[y0 + y][x0 + x] = (hi << 4) | blk[y][x] if blk[y][x] else 0


# ================================================================================================ index-art helpers
def canvas(w, h, v=0):
    return [[v] * w for _ in range(h)]


def fill(g, x0, y0, x1, y1, v):
    for y in range(max(0, y0), min(len(g), y1)):
        for x in range(max(0, x0), min(len(g[0]), x1)):
            g[y][x] = v


def put(g, x, y, v):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = v


def cut_box(g, x0, y0, w, h, cut, rings, fillv=None):
    """A box with 45-degree corners `cut` px: rings[i] is the colour i px in from its edge (the field box's rule);
    inside the last ring, fillv."""
    for y in range(h):
        for x in range(w):
            xx, yy = min(x, w - 1 - x), min(y, h - 1 - y)
            d = min(xx, yy, xx + yy - cut) if cut else min(xx, yy)
            if d < 0:
                continue
            v = rings[d] if d < len(rings) else fillv
            if v is not None:
                put(g, x0 + x, y0 + y, v)


def blit(g, src, x0, y0, keep0=False):
    for y, row in enumerate(src):
        for x, v in enumerate(row):
            if v or keep0:
                put(g, x0 + x, y0 + y, v)


def retile(sheet, per, maps, label="", skip0=True):
    """Redraw tiles IN PLACE: `maps` is [(entries, width, target)], each entry (tile, hflip, vflip, _) at its cell of a
    map `width` tiles wide, target the index picture that map should show. Every tile id takes the 8x8 most of its
    uses ask for (un-flipped); the result is measured back, so a mock built from it shows what the engine would."""
    votes = {}
    for entries, w, tgt in maps:
        for i, (t, hf, vf, _) in enumerate(entries):
            cx, cy = (i % w) * 8, (i // w) * 8
            if cy + 8 > len(tgt) or cx + 8 > len(tgt[0]):
                continue
            blk = [[tgt[cy + (7 - y if vf else y)][cx + (7 - x if hf else x)] for x in range(8)] for y in range(8)]
            votes.setdefault(t, []).append(tuple(map(tuple, blk)))
    miss = 0
    for t, bl in votes.items():
        if t == 0 and skip0:
            continue                                  # tile 0 is the clear tile (not in scrolling_bg)
        best = max(set(bl), key=lambda b: (bl.count(b), -bl.index(b)))
        miss += sum(1 for b in bl if b != best)
        put_tile(sheet, t, per, [list(r) for r in best], hi=(sheet[(t // per) * 8][(t % per) * 8] >> 4))
    return miss, len(votes)


def render_map(sheet, per, entries, w, h, rows, pal_of=None, clear=None):
    """An RGBA picture of a tilemap: rows the palette rows (16 colours each); pal_of(entry) the row an entry uses."""
    im = Image.new("RGBA", (w * 8, h * 8), (0, 0, 0, 0))
    p = im.load()
    for i, e in enumerate(entries[:w * h]):
        t, hf, vf, pn = e
        r = pal_of(e) if pal_of else pn
        x0, y0 = (i % w) * 8, (i // w) * 8
        if (t // per) * 8 + 8 > len(sheet):
            continue
        blk = get_tile(sheet, t, per)
        for y in range(8):
            for x in range(8):
                v = blk[7 - y if vf else y][7 - x if hf else x]
                if v:
                    p[x0 + x, y0 + y] = q5(rows[r][v]) + (255,)
    return im


def idx_rgba(g, pal, clear0=True):
    im = Image.new("RGBA", (len(g[0]), len(g)), (0, 0, 0, 0))
    p = im.load()
    for y in range(len(g)):
        for x in range(len(g[0])):
            v = g[y][x]
            if v or not clear0:
                p[x, y] = q5(pal[v]) + (255,)
    return im


# ================================================================================================ fonts
_FONTS = {}


def font(small):
    if small not in _FONTS:
        import fontwidth
        tabs = fontwidth.all_glyph_widths(GBA)
        cm = fontwidth.charmap(GBA)
        if small:
            _FONTS[small] = (Image.open(os.path.join(FONTS, "latin_small.png")), tabs["sFontSmallLatinGlyphWidths"],
                             cm, 8, 32)
        else:
            _FONTS[small] = (Image.open(os.path.join(FONTS, "latin_normal.png")), tabs["sFontNormalLatinGlyphWidths"],
                             cm, 16, 16)
    return _FONTS[small]


def glyphs(s):
    out, i = [], 0
    cm = font(True)[2]
    while i < len(s):
        if s.startswith("{LV}", i):
            out.append(0x105)
            i += 4
            continue
        b = cm.get(s[i])
        if b is not None:
            out.append(b)
        i += 1
    return out


def text_width(s, small=False):
    sheet, w, cm, cw, per = font(small)
    return sum(w[g] if g < len(w) else 0 for g in glyphs(s))


def say(im, x, y, s, ink, shadow, small=False):
    """Print as the game's text printer does: the font's 1 the ink, 2 the shadow."""
    sheet, w, cm, cw, per = font(small)
    fp, px = sheet.load(), im.load()
    for gid in glyphs(s):
        gx, gy = (gid % per) * cw, (gid // per) * 16
        for yy in range(16):
            for xx in range(min(cw, w[gid] if gid < len(w) else cw)):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, y + yy
                if 0 <= X < im.width and 0 <= Y < im.height:
                    if v == 1:
                        px[X, Y] = tuple(q5(ink)) + ((255,) if im.mode == "RGBA" else ())
                    elif v == 2 and shadow is not None:
                        px[X, Y] = tuple(q5(shadow)) + ((255,) if im.mode == "RGBA" else ())
        x += w[gid] if gid < len(w) else cw
    return x


# ================================================================================================ the game's content
def species_names():
    return dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)',
                           open(os.path.join(GBA, "src/data/text/species_names.h")).read()))


def icon_pal_index():
    src = open(os.path.join(GBA, "src/pokemon_icon.c")).read()
    blk = src[src.index("gMonIconPaletteIndices[]"):]
    blk = blk[:blk.index("};")]
    return {k: int(v) for k, v in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*(\d+)", blk)}


def icon(species):
    w, h, bd, pal, px = load_png(os.path.join(G, "pokemon", species.lower(), "icon.png"))
    ip = icon_pal_index().get(species, 0)
    ipal = gbapal(os.path.join(G, "pokemon/icon_palettes/icon_palette_%d.gbapal" % ip))
    return idx_rgba([r[:32] for r in px[:32]], ipal)


def front(species):
    d = os.path.join(G, "pokemon", species.lower())
    w, h, bd, pal, px = load_png(os.path.join(d, "front.png"))
    return idx_rgba(px, jasc(os.path.join(d, "normal.pal")))


PARTY = [("EEVEE", 34, 102, 102), ("CHARMANDER", 31, 88, 88), ("PIDGEY", 29, 64, 81), ("PIKACHU", 30, 15, 70),
         ("ABRA", 27, 59, 59), ("GASTLY", 28, 0, 61)]                    # species, level, HP, max HP


def std_frame_box(im, x, y, wt, ht):
    """The engine's own std frame (type1, the user's chosen TERMINAL since T-523) round a wt x ht tile window, paper
    filled, as DrawStdFrameWithCustomTileAndPalette lays it."""
    w, h, bd, pal, px = load_png(os.path.join(G, "text_window/type1.png"))
    fpal = gbapal(os.path.join(G, "text_window/type1.gbapal")) if os.path.exists(
        os.path.join(G, "text_window/type1.gbapal")) else pal
    paper = jasc(os.path.join(G, "text_window/stdpal_0.pal"))[1]
    W, H = (wt + 2) * 8, (ht + 2) * 8
    g = canvas(W, H, 1)
    for ty in range(ht + 2):
        for tx in range(wt + 2):
            sx = 0 if tx == 0 else (2 if tx == wt + 1 else 1)
            sy = 0 if ty == 0 else (2 if ty == ht + 1 else 1)
            for yy in range(8):
                for xx in range(8):
                    g[ty * 8 + yy][tx * 8 + xx] = px[sy * 8 + yy][sx * 8 + xx] & 15
    fp = list(fpal) + [(0, 0, 0)] * 16
    fp[1] = paper
    b = idx_rgba(g, fp)
    im.paste(b, (x - 8, y - 8), b)


# ================================================================================================ colours
SLATE_OUT, SLATE_MID, SLATE_LIGHT, TEAL = (32, 40, 52), (88, 104, 120), (176, 192, 204), (112, 208, 184)
TEAL_DK = (40, 136, 116)
PAPER, INK, INK_SH = (248, 248, 244), (64, 72, 84), (200, 204, 208)
SCREEN, PHOS, PHOS_SH, PHOS_DIM = (20, 32, 36), (184, 240, 208), (40, 72, 64), (64, 112, 100)
AMBER, AMBER_DK = (232, 184, 88), (160, 112, 40)


# ================================================================================================ PARTY
PM = os.path.join(G, "party_menu")
# what each state's box takes, per direction: (4 light rim / strip, 5 fill, 6 shade) and (1 outline, 7 rim, 8 rim dark)
PARTY_DIRS = {
    "A": dict(
        name="TERMINAL",
        said="graph paper under a slate rail; each daemon a paper card cut at 45 degrees with the teal bracket at its "
             "corner; the one chosen ruled in teal, a switch in amber, a HALTED card greyed rose",
        field={1: SLATE_OUT, 2: (212, 218, 224), 3: (190, 198, 208), 4: SLATE_MID, 5: SLATE_LIGHT, 6: TEAL,
               7: SLATE_LIGHT, 8: (64, 76, 92), 10: (48, 58, 72), 11: (228, 232, 236), 12: (168, 178, 190),
               15: PAPER},
        field_sel={1: TEAL_DK, 7: TEAL, 15: (216, 244, 236)},
        ink={2: INK_SH, 3: INK, 13: SLATE_OUT, 14: TEAL, 15: TEAL},
        states={  # row: (4, 5, 6)
            3: ((236, 238, 240), PAPER, (208, 214, 220)),          # a box at rest
            4: ((244, 236, 212), (252, 248, 232), (220, 208, 176)),  # multi (a partner's): warm paper
            5: ((232, 216, 216), (240, 228, 228), (204, 184, 184)),  # HALTED: rose-grey paper
            6: ((212, 240, 228), (228, 248, 240), (176, 216, 200)),  # picked to switch
            7: ((208, 240, 232), (224, 248, 244), (168, 220, 208)),  # the current one
            8: ((240, 232, 200), (248, 244, 220), (208, 192, 152)),  # current, multi
            9: ((236, 208, 208), (244, 224, 224), (208, 168, 168)),  # current, HALTED
        },
        rims={3: (SLATE_OUT, SLATE_LIGHT, SLATE_MID), 4: (SLATE_OUT, SLATE_LIGHT, SLATE_MID),
              5: (SLATE_OUT, SLATE_LIGHT, SLATE_MID), 6: (TEAL_DK, TEAL, TEAL_DK), 10: (AMBER_DK, AMBER, AMBER_DK)},
        hp={3: ((80, 192, 120), (40, 136, 84)), 4: ((224, 184, 56), (168, 128, 24)), 5: ((224, 88, 72), (160, 48, 40))},
    ),
    "B": dict(
        name="READOUT",
        said="the readout's dark screen and its graticule under a register rail; each daemon a lit panel with a "
             "phosphor name, the HP bar a meter; the one chosen framed in bright teal, a switch in amber",
        field={1: (64, 76, 92), 2: (16, 26, 30), 3: (30, 50, 52), 4: (28, 40, 48), 5: (64, 96, 96), 6: TEAL,
               7: (40, 56, 64), 8: (12, 16, 20), 10: (36, 52, 60), 11: (22, 36, 40), 12: (12, 20, 24),
               15: (28, 44, 48)},
        field_sel={1: TEAL, 7: (64, 120, 108), 15: (36, 72, 68)},
        ink={2: PHOS_SH, 3: PHOS, 13: (12, 16, 20), 14: TEAL, 15: TEAL},
        states={
            3: ((40, 58, 62), (28, 42, 46), (14, 22, 26)),
            4: ((60, 56, 36), (44, 42, 28), (24, 22, 14)),
            5: ((64, 40, 44), (48, 30, 34), (26, 16, 18)),
            6: ((40, 76, 68), (30, 60, 54), (16, 34, 30)),
            7: ((44, 84, 76), (32, 66, 60), (16, 36, 32)),
            8: ((76, 68, 36), (56, 52, 28), (28, 26, 14)),
            9: ((84, 48, 52), (64, 36, 40), (32, 18, 20)),
        },
        rims={3: ((64, 76, 92), (88, 120, 120), (36, 48, 56)), 4: ((64, 76, 92), (88, 120, 120), (36, 48, 56)),
              5: ((64, 76, 92), (88, 120, 120), (36, 48, 56)), 6: (TEAL, (168, 240, 216), TEAL_DK),
              10: (AMBER, (248, 216, 136), AMBER_DK)},
        hp={3: ((120, 232, 160), (56, 160, 104)), 4: ((248, 200, 88), (184, 136, 40)), 5: ((248, 112, 104), (176, 64, 64))},
    ),
}


def party_files():
    w, h, bd, pal, px = load_png(os.path.join(PM, "bg.png"))
    rows = [pal[i * 16:(i + 1) * 16] for i in range(len(pal) // 16)]
    maps = {
        "bg": (map16(os.path.join(PM, "bg.bin")), 32, 20),
        "main": (map8(os.path.join(PM, "slot_main.bin")), 10, 7),
        "main_nohp": (map8(os.path.join(PM, "slot_main_no_hp.bin")), 10, 7),
        "wide": (map8(os.path.join(PM, "slot_wide.bin")), 18, 3),
        "wide_nohp": (map8(os.path.join(PM, "slot_wide_no_hp.bin")), 18, 3),
        "wide_empty": (map8(os.path.join(PM, "slot_wide_empty.bin")), 18, 3),
        "cancel": (map16(os.path.join(PM, "cancel_button.bin")), 7, 2),
        "confirm": (map16(os.path.join(PM, "confirm_button.bin")), 7, 2),
    }
    return px, w // 8, rows, maps


def vanilla_target(px, per, entries, w, h):
    g = canvas(w * 8, h * 8)
    for i, (t, hf, vf, _) in enumerate(entries[:w * h]):
        blk = get_tile(px, t, per)
        for y in range(8):
            for x in range(8):
                g[(i // w) * 8 + y][(i % w) * 8 + x] = blk[7 - y if vf else y][7 - x if hf else x]
    return g


def hp_overlay(g, van):
    """Keep the HP bar's track (2 inside 3) and the HP tag's letters exactly where the code fills and reads them:
    the code fills the bar rect with 9/10 at a fixed place, so the track stays put; the tag is restyled."""
    for y in range(len(g)):
        for x in range(len(g[0])):
            v = van[y][x]
            if v in (2, 3):
                g[y][x] = v
            elif v == 13:
                g[y][x] = 13
            elif v in (14, 15):
                g[y][x] = 14


def bracket(g, x0, y0, n=4):
    for i in range(n):
        put(g, x0 + i + 1, y0, 15)
        put(g, x0, y0 + i + 1, 15)


def party_slot_main(direction, hp=True, van=None):
    g = canvas(80, 56)
    # the card: vanilla's outline at y 2..53, x 0..77 (the window's 10x7 tiles); 45-degree corners, 1 the rule
    cut_box(g, 0, 2, 78, 52, 3, [1, 1], None)
    cut_box(g, 2, 4, 74, 48, 2, [4], 5)
    fill(g, 3, 31, 75, 50, 6 if direction == "A" else 4)       # the lower strip (HP)
    fill(g, 3, 31, 75, 32, 4 if direction == "A" else 6)
    fill(g, 3, 49, 75, 50, 6)
    bracket(g, 3, 5)
    if van is not None:
        hp_overlay(g, van)
    return g


def party_slot_wide(direction, hp=True, van=None, empty=False):
    g = canvas(144, 24)
    if empty:
        cut_box(g, 0, 2, 144, 22, 2, [1], None)
        for x in range(4, 140, 4):                       # an empty slot: a dotted rule inside, nothing to show
            put(g, x, 4, 7)
            put(g, x, 21, 7)
        return g
    cut_box(g, 0, 2, 144, 22, 2, [1, 7], 5)
    fill(g, 2, 16, 144, 22, 4 if direction == "A" else 4)
    fill(g, 2, 15, 144, 16, 6)
    fill(g, 1, 22, 144, 23, 8)
    bracket(g, 2, 4)
    if van is not None:
        hp_overlay(g, van)
    return g


def party_field(direction):
    """The bg.bin picture, 256x160 in row 1's slots: the rail at the left and top, the ground, the cancel button."""
    g = canvas(256, 160, 2)
    for y in range(160):                                  # the ground's 8px grain: graph paper / a graticule
        for x in range(256):
            if direction == "A":
                if (x % 8 == 7 and y % 2 == 0) or (y % 8 == 7 and x % 2 == 0):
                    g[y][x] = 3
            else:
                if x % 8 == 7 and y % 8 == 7:
                    g[y][x] = 5
                elif (x % 8 == 7 and y % 8 in (3,)) or (y % 8 == 7 and x % 8 in (3,)):
                    g[y][x] = 3
    # the left rail (cols 0-1, one tile repeated: so 8px stripes) and the top rail (row 0)
    for y in range(160):
        for x in range(16):
            g[y][x] = 4 if x % 8 < 6 else (10 if x % 8 == 6 else 5)
        if y % 8 == 3:
            for x in range(1, 4):
                g[y][x] = 6
                g[y][x + 8] = 6
    for x in range(16, 256):
        for y in range(8):
            g[y][x] = 4 if y < 5 else (10 if y == 5 else 5)
        if x % 8 == 3:
            g[2][x] = 6
    for x in range(16, 256):                              # the bottom rail (row 19)
        for y in range(152, 160):
            g[y][x] = 4 if y > 154 else (10 if y == 154 else 5)
    # the inner corners, cut at 45 degrees (tiles 04 06 09 07)
    for d in range(4):
        for k in range(4 - d):
            g[8 + d][16 + k] = 5 if k == 3 - d else 4
            g[151 - d][16 + k] = 5 if k == 3 - d else 4
    # the cancel button: (23,17) 7x2 tiles, 56x16 at (184,136); 1 rule, 7 rim, 15 face (row 2 lights it)
    cut_box(g, 184, 136, 56, 16, 3, [1, 7], 15)
    bracket(g, 186, 138, 3)
    return g


def party_button():
    g = canvas(56, 16)
    cut_box(g, 0, 0, 56, 16, 3, [1, 7], 15)
    return g


def party_rows(direction):
    """bg.png's 11 palette rows: row 0 kept, 1/2 the field and the cancel button, 3-10 the state buffer."""
    van = party_files()[2]
    d = PARTY_DIRS[direction]
    rows = [list(r) + [(0, 0, 0)] * (16 - len(r)) for r in van]
    for k, v in d["field"].items():
        rows[1][k] = v
    rows[2] = list(rows[1])
    for k, v in d["field_sel"].items():
        rows[2][k] = v
    for r in range(3, 11):
        for k, v in d["ink"].items():
            rows[r][k] = v
        if r in d["states"]:
            for k, v in zip((4, 5, 6), d["states"][r]):
                rows[r][k] = v
        if r in d["rims"]:
            for k, v in zip((1, 7, 8), d["rims"][r]):
                rows[r][k] = v
        if r in d["hp"]:
            rows[r][9], rows[r][10] = d["hp"][r]
    return rows


def party_build(direction):
    px, per, vrows, maps = party_files()
    sheet = [list(r) for r in px]
    if direction is None:
        return sheet, per, vrows, maps, (0, 0)
    tg = {}
    van = {k: vanilla_target(px, per, *maps[k]) for k in maps}
    tg["bg"] = party_field(direction)
    tg["main"] = party_slot_main(direction, True, van["main"])
    tg["main_nohp"] = party_slot_main(direction, False, van["main_nohp"])
    tg["wide"] = party_slot_wide(direction, True, van["wide"])
    tg["wide_nohp"] = party_slot_wide(direction, False, van["wide_nohp"])
    tg["wide_empty"] = party_slot_wide(direction, empty=True)
    b = party_button()
    tg["cancel"] = b
    tg["confirm"] = b
    order = ["main", "wide", "main_nohp", "wide_nohp", "wide_empty", "cancel", "confirm", "bg"]
    res = retile(sheet, per, [(maps[k][0], maps[k][1], tg[k]) for k in order])
    return sheet, per, party_rows(direction), maps, res


CANCEL_TILES = {0x0D, 0x1C, 0x14}                     # the bg's cancel button at (23,17): palette 2 when chosen


def party_mock(direction, state="choose"):
    sheet, per, rows, maps, res = party_build(direction)
    im = Image.new("RGB", (240, 160), q5(rows[0][0]))
    bgm = maps["bg"]
    cancel_sel = state == "switch"
    fieldimg = render_map(sheet, per, bgm[0], 32, 20, rows,
                          pal_of=lambda e: 2 if cancel_sel and e[0] in CANCEL_TILES else 1)
    im.paste(fieldimg, (0, 0), fieldimg)
    names = species_names()
    # the boxes: main at window (1,3), the wide ones at (12,1+3k); slot 0 the current one
    slots = [(1, 3, "main")] + [(12, 1 + 3 * k, "wide") for k in range(5)]
    for k, (tx, ty, kind) in enumerate(slots):
        sp, lv, hp, mx = PARTY[k]
        cur = (k == 0) if state == "choose" else False
        r = 7 if cur else 3
        rim = 6 if cur else 3
        if hp == 0:
            r = 9 if cur else 5
        if state == "switch" and k == 2:            # picked to switch: row 6's fill, row 10's rim
            r, rim = 6, 10
        rr = [list(x) for x in rows]
        box = list(rows[3])
        box[4], box[5], box[6] = rows[r][4], rows[r][5], rows[r][6]
        box[1], box[7], box[8] = rows[rim][1], rows[rim][7], rows[rim][8]
        frac = hp / mx
        hpr = 3 if frac > 0.5 else (4 if frac > 0.2 else 5)
        box[9], box[10] = rows[hpr][9], rows[hpr][10]
        rr[3] = box
        ent, w, h = maps[kind]
        img = render_map(sheet, per, ent, w, h, rr, pal_of=lambda e: 3)
        X, Y = tx * 8, ty * 8
        im.paste(img, (X, Y), img)
        # the code's text: FONT_SMALL, 3 on 2 (sFontColorTable[0]); rects from sPartyBoxInfoRects
        if kind == "main":
            nick, lvp, hpp, mxp, bar = (24, 11), (32, 20), (38, 36), (53, 36), (24, 35, 48)
        else:
            nick, lvp, hpp, mxp, bar = (22, 3), (32, 12), (102, 12), (117, 12), (88, 10, 48)
        ink, sh = box[3], box[2]
        say(im, X + nick[0], Y + nick[1] - 3, names.get(sp, sp), ink, sh, small=True)
        say(im, X + lvp[0], Y + lvp[1] - 3, "{LV}%d" % lv, ink, sh, small=True)
        s = "%d/%d" % (hp, mx)
        say(im, X + mxp[0] + 24 - text_width(s, True), Y + hpp[1] - 3, s, ink, sh, small=True)
        fillw = int(round(bar[2] * frac))
        d = ImageDraw.Draw(im)
        if fillw:
            d.rectangle([X + bar[0], Y + bar[1], X + bar[0] + fillw - 1, Y + bar[1] + 1], fill=q5(box[9]))
            d.rectangle([X + bar[0], Y + bar[1] + 2, X + bar[0] + fillw - 1, Y + bar[1] + 2], fill=q5(box[10]))
        # the daemon's box sprite (ours) and its icon, at sPartyMenuSpriteCoords (single layout)
        cx, cy = ((16, 40), (104, 18), (104, 42), (104, 66), (104, 90), (104, 114))[k]
        bx, by = ((16, 34), (102, 25), (102, 49), (102, 73), (102, 97), (102, 121))[k]
        ic = icon(sp)
        im.paste(ic, (cx - 16, cy - 16 - (4 if k == 0 else 0)), ic)
    # CANCEL, in the cancel window (24,17) on the button
    cr = rows[3]
    s = "CANCEL"
    say(im, 192 + (48 - text_width(s, True)) // 2, 138, s, cr[3], cr[2], small=True)
    # the message, in the engine's own frame (the T-523 TERMINAL) at (1,17) 21x2
    std_frame_box(im, 8, 136, 21, 2)
    stdp = jasc(os.path.join(G, "text_window/stdpal_0.pal"))
    say(im, 10, 137, "Choose a DAEMON." if state == "choose" else "Move to where?", stdp[2], stdp[3])
    return im


# ================================================================================================ SUMMARY
SS = os.path.join(G, "summary_screen")
# The backdrop's rows are RETINTED, not redrawn: by role on rows 0/6 (the backdrop and title bar, whose slots T-481 B
# writes) and 1/5 (the daemon's box), and on the panes (2 INFO, 3 SKILLS, 4 MOVES) each colour keeps its lightness and
# takes the direction's tint -- so every ink the code prints on a pane reads as it did.
SUM_DIRS = {
    "A": dict(name="TERMINAL",
              said="the bars become slate meters with a graticule, the HP tag cut at 45 degrees, the move cursor a "
                   "ruled frame with teal brackets; the backdrop slate paper, the title bar slate, the panes paper",
              role={1: SLATE_OUT, 2: SLATE_MID, 3: (214, 220, 228), 4: (20, 26, 34), 5: (120, 136, 152),
                    6: SLATE_LIGHT, 7: TEAL, 8: (104, 120, 138), 9: (178, 188, 200), 10: (200, 208, 218),
                    11: (178, 188, 200), 12: AMBER, 13: SLATE_MID, 15: (48, 58, 72)},
              row6={8: (196, 226, 222), 9: (160, 210, 204)},
              box=((140, 156, 172), (64, 78, 94)),          # the daemon's box: light, dark (lightness kept)
              tints={2: ((236, 226, 212), 0.55), 3: ((226, 230, 236), 0.7), 4: ((212, 230, 234), 0.6)},
              pills={13: SLATE_MID, 15: (48, 58, 72), 9: SLATE_MID, 10: (48, 58, 72)},
              bar={13: (60, 72, 88), 14: SLATE_OUT, 15: (112, 128, 146), 11: (60, 72, 88), 12: (60, 72, 88),
                   3: SLATE_OUT, 4: SLATE_MID, 5: TEAL, 6: TEAL, 7: (136, 224, 232), 8: (64, 160, 172)},
              hp=(((96, 208, 136), (48, 152, 96)), ((240, 200, 64), (176, 136, 32)), ((240, 96, 80), (168, 56, 48))),
              cursor=(TEAL_DK, AMBER_DK, TEAL, AMBER)),
    "B": dict(name="READOUT",
              said="the bars become the readout's meters, phosphor on a dark track; the backdrop and the daemon's box "
                   "the dark screen, the title bar dark with the header in white; the panes a lit paper",
              role={1: TEAL_DK, 2: (36, 52, 60), 3: (22, 34, 38), 4: (12, 16, 20), 5: (64, 96, 96), 6: (64, 96, 96),
                    7: TEAL, 8: (16, 26, 30), 9: (30, 48, 52), 10: (16, 26, 30), 11: (30, 48, 52), 12: AMBER,
                    13: (64, 76, 92), 15: (40, 48, 60)},
              row6={8: (20, 44, 44), 9: (28, 60, 58)},
              box=((44, 64, 66), (14, 22, 26)),
              tints={2: ((196, 240, 216), 0.6), 3: ((240, 228, 180), 0.55), 4: ((180, 228, 236), 0.6)},
              pills={13: (40, 88, 80), 15: (16, 40, 36), 9: (40, 88, 80), 10: (16, 40, 36)},
              bar={13: (20, 32, 36), 14: (8, 12, 16), 15: (40, 72, 64), 11: (20, 32, 36), 12: (20, 32, 36),
                   3: (8, 12, 16), 4: (28, 44, 48), 5: TEAL, 6: TEAL, 7: PHOS, 8: (96, 168, 152)},
              hp=(((120, 232, 160), (56, 160, 104)), ((248, 200, 88), (184, 136, 40)), ((248, 112, 104), (176, 64, 64))),
              cursor=(TEAL, AMBER, PHOS, (248, 216, 136))),
}


def tint_keep(c, T, k):
    """c's lightness, T's hue: mix a grey of c's lightness toward T scaled to that lightness."""
    L, LT = lum(c), max(1, lum(T))
    t = tuple(min(255, v * L / LT) for v in T)
    return tuple(int(round((1 - k) * L + k * v)) for v in t)


def summary_rows(direction):
    w, h, bd, pal, px = load_png(os.path.join(SS, "bg.png"))
    rows = [list(pal[i * 16:(i + 1) * 16]) for i in range(len(pal) // 16)]
    if direction is None:
        return rows
    d = SUM_DIRS[direction]
    for r in (0, 6):
        for k, v in d["role"].items():
            rows[r][k] = v
    for k, v in d["row6"].items():
        rows[6][k] = v
    for r in (1, 5):
        Ls = [lum(c) for c in rows[r][1:]]
        lo, hi = min(Ls), max(Ls)
        for k in range(1, 16):
            c = rows[r][k]
            if c == (255, 0, 255):
                continue
            t = (lum(c) - lo) / max(1, hi - lo)
            a, b = d["box"][1], d["box"][0]
            rows[r][k] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
        rows[r][3], rows[r][6] = (d["role"][7], d["role"][7]) if r == 5 else (rows[r][3], rows[r][6])
    for r, (T, kk) in d["tints"].items():
        for k in range(1, 16):
            c = rows[r][k]
            if c != (255, 0, 255):
                rows[r][k] = tint_keep(c, T, kk)
        for k, v in d["pills"].items():
            if rows[r][k] != (255, 0, 255) and k in (13, 15) or (r == 3 and k in (9, 10)):
                rows[r][k] = v
        if r == 3:
            rows[r][11], rows[r][12] = AMBER, AMBER_DK
    return rows


def bar_tiles(direction, exp=False):
    """12 tiles in a row (96x8): fill frames 0-8 (0 empty, 8 whole), 9 and 10 the tag, 11 the end."""
    w, h, bd, pal, van = load_png(os.path.join(SS, "exp_bar.png" if exp else "hp_bar.png"))
    if direction is None:
        return [[v & 15 for v in r] for r in van]
    g = canvas(96, 8)
    hi, lo = (7, 8) if exp else (1, 2)
    for f in range(9):
        x0 = f * 8
        for x in range(8):
            on = x < f
            g[0][x0 + x] = 14
            g[6][x0 + x] = 14
            for y in range(1, 6):
                if on:
                    g[y][x0 + x] = lo if y in (1, 5) else hi
                else:
                    g[y][x0 + x] = 15 if (x == 7 and y in (2, 3, 4)) else 13
            if not on and x == 7:
                g[1][x0 + x] = 15
    # the tag (tiles 9-10: 16x7): a 45-degree pill in 3/4, the vanilla letters kept in 5
    tag = canvas(16, 8)
    cut_box(tag, 0, 0, 16, 7, 2, [3], 4)
    for y in range(8):
        for x in range(16):
            v = van[y][72 + x] & 15
            if v in (5, 6) or (v == 15 and False):
                tag[y][x] = 5 if direction == "A" else 6
    for y in range(8):
        for x in range(16):
            g[y][72 + x] = tag[y][x]
        # the tag runs on into the track: its right edge is the meter's start
    # the end (tile 11): the track closed with a 45-degree cut
    for y in range(7):
        for x in range(8):
            if x == 0 and 1 <= y <= 5:
                g[y][88 + x] = 13
            if x == 0 and y in (0, 6):
                g[y][88 + x] = 14
            if x == 1 and 1 <= y <= 5:
                g[y][88 + x] = 14
            if x == 2 and 2 <= y <= 4:
                g[y][88 + x] = 14
    return g


def bar_pals(direction):
    base = gbapal(os.path.join(SS, "exp_bar.gbapal"), 16)
    if direction is None:
        return [base, gbapal(os.path.join(SS, "hp_bar_yellow.gbapal"), 16), gbapal(os.path.join(SS, "hp_bar_red.gbapal"), 16)]
    d = SUM_DIRS[direction]
    p = list(base)
    for k, v in d["bar"].items():
        p[k] = v
    out = []
    for hi, lo in d["hp"]:
        q = list(p)
        q[1], q[2] = hi, lo
        out.append(q)
    return out


def cursor_frames(direction):
    """move_selection_cursor_left/right.png: 64x64 each, two 64x32 frames (1 the cursor, 2 the swap cursor) -- the
    pair makes one 128x29 frame round a move."""
    L = load_png(os.path.join(SS, "move_selection_cursor_left.png"))
    R = load_png(os.path.join(SS, "move_selection_cursor_right.png"))
    if direction is None:
        return [[v & 15 for v in r] for r in L[4]], [[v & 15 for v in r] for r in R[4]], L[3]
    d = SUM_DIRS[direction]
    full = canvas(128, 64)
    for f, (rule, acc) in enumerate(((1, 3), (2, 4))):
        y0 = f * 32
        cut_box(full, 0, y0, 128, 29, 3, [rule, rule], None)
        for (cx, cy, sx, sy) in ((0, y0, 1, 1), (127, y0, -1, 1), (0, y0 + 28, 1, -1), (127, y0 + 28, -1, -1)):
            for i in range(3, 10):                        # the bracket at each corner, outside the cut
                put(full, cx + sx * i, cy + sy * 0, acc)
                put(full, cx + sx * 0, cy + sy * i, acc)
    left = [r[:64] for r in full]
    right = [r[64:] for r in full]
    pal = [(0, 0, 0), d["cursor"][0], d["cursor"][1], d["cursor"][2], d["cursor"][3]] + [(255, 0, 255)] * 11
    return left, right, pal


def star_and_mark(direction):
    if direction is None:
        s = load_png(os.path.join(SS, "shiny_star.png"))
        m = load_png(os.path.join(SS, "pokerus_cured.png"))
        return [[v & 15 for v in r] for r in s[4]], s[3], [[v & 15 for v in r] for r in m[4]], m[3]
    star = canvas(8, 16)
    for (x, y, v) in ((3, 8, 2), (3, 9, 1), (3, 10, 1), (3, 11, 1), (3, 12, 1), (3, 13, 1), (3, 14, 2),
                      (0, 11, 2), (1, 11, 1), (2, 11, 1), (4, 11, 1), (5, 11, 1), (6, 11, 2),
                      (2, 10, 2), (4, 10, 2), (2, 12, 2), (4, 12, 2)):
        star[y][x] = v
    spal = [(0, 0, 0), (248, 224, 120), (200, 152, 48)] + [(0, 0, 0)] * 13
    mark = canvas(8, 8)
    for (x, y) in ((3, 2), (2, 3), (4, 3), (3, 4), (2, 4) if False else (3, 3)):
        mark[y][x] = 2
    mpal = [(0, 0, 0), (0, 0, 0), TEAL if direction == "A" else PHOS] + [(0, 0, 0)] * 13
    return star, spal, mark, mpal


def summary_mock(direction, page="skills"):
    w, h, bd, pal, sheet = load_png(os.path.join(SS, "bg.png"))
    per = w // 8
    rows = summary_rows(direction)
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    back = render_map(sheet, per, map16(os.path.join(SS, "moves_page.bin" if page == "skills" else "moves_info_page.bin")),
                      32, 20, rows)
    im.paste(back, (0, 0), back)
    pg = render_map(sheet, per, map16(os.path.join(SS, "page_skills.bin" if page == "skills" else "page_moves.bin")),
                    32, 20, rows)
    im.paste(pg, (0, 0), pg)
    sp, lv, hp, mx = PARTY[0] if page == "skills" else PARTY[2]
    names = species_names()
    hdr = gbapal(os.path.join(SS, "text_header.gbapal"), 16)
    say(im, 4, 1, "DAEMON SKILLS" if page == "skills" else "KNOWN MOVES", hdr[1], hdr[2])
    say(im, 4, 18, "{LV}%d" % lv, hdr[1], hdr[2], small=True)
    say(im, 40, 17, names[sp], hdr[1], hdr[2])
    f = front(sp)
    im.paste(f, (28, 38), f)
    ink, sh = (80, 80, 88), (208, 208, 200)
    if page == "skills":
        s = "%d/%d" % (hp, mx)
        say(im, 236 - text_width(s), 17, s, ink, sh)
        for i, v in enumerate((41, 49, 44, 55, 52)):
            say(im, 236 - text_width(str(v)), 35 + 13 * i, str(v), ink, sh)
        say(im, 236 - text_width("5832"), 103, "5832", ink, sh)
        say(im, 236 - text_width("312"), 116, "312", ink, sh)
        say(im, 72, 127, "DETACHES", ink, sh)
        say(im, 8, 142, "Detaches from anything wild.", ink, sh)
        # the HP bar: 9 sprites from x 172 (centre), y 36; the EXP bar 9 from x 156, y 132
        for which, x0, y0, frac in (("hp", 172, 36, hp / mx), ("exp", 156, 132, 0.62)):
            g = bar_tiles(direction, which == "exp")
            pals = bar_pals(direction)
            pp = pals[0] if which == "exp" else pals[0 if frac > 0.5 else (1 if frac > 0.2 else 2)]
            whole = int(frac * 48)
            frames = [9, 10] + [min(8, max(0, whole - 8 * i)) for i in range(6)] + [11]
            for i, fr in enumerate(frames):
                t = idx_rgba([r[fr * 8:fr * 8 + 8] for r in g], pp)
                im.paste(t, (x0 + 8 * i - 4, y0 - 4), t)
    else:
        L, R, cp = cursor_frames(direction)
        mv_ink = gbapal(os.path.join(SS, "text_moves.gbapal"), 16)
        for i, (mv, pp) in enumerate((("WRITE", 35), ("SILT", 15), ("DRIFT", 35), ("FAST PATH", 30))):
            say(im, 131, 20 + 28 * i, mv, mv_ink[7], mv_ink[8])
            s = "%d/%d" % (pp, pp)
            say(im, 232 - text_width(s), 32 + 28 * i, s, mv_ink[7], mv_ink[8])
        sel = 1
        lt = idx_rgba([r for r in L[:32]], cp)
        rt = idx_rgba([r for r in R[:32]], cp)
        y = sel * 28 + 34 - 16
        im.paste(lt, (152 - 32, y), lt)
        im.paste(rt, (216 - 32, y), rt)
    return im


def summary_parts(direction):
    """The bars at every fill, three palettes, the cursor's two frames, the star and the mark: 240x160, 2x inside."""
    im = Image.new("RGB", (240, 160), (40, 44, 52))
    pals = bar_pals(direction)
    for row, exp in enumerate((False, True)):
        g = bar_tiles(direction, exp)
        for pi in range(1 if exp else 3):
            t = idx_rgba(g, pals[pi]).resize((192, 16), Image.NEAREST)
            im.paste(t, (8, 8 + row * 66 + pi * 20), t)
    L, R, cp = cursor_frames(direction)
    for f in range(2):
        lt = idx_rgba([r for r in L[f * 32:f * 32 + 32]], cp)
        rt = idx_rgba([r for r in R[f * 32:f * 32 + 32]], cp)
        im.paste(lt, (8 + f * 0, 96 + f * 0), lt) if f == 0 else None
        if f == 0:
            im.paste(rt, (72, 96), rt)
        else:
            im.paste(lt, (8, 126), lt)
            im.paste(rt, (72, 126), rt)
    s, sp, m, mp = star_and_mark(direction)
    st = idx_rgba(s, sp).resize((16, 32), Image.NEAREST)
    mk = idx_rgba(m, mp).resize((16, 16), Image.NEAREST)
    im.paste(st, (160, 100), st)
    im.paste(mk, (190, 116), mk)
    return im


# ================================================================================================ PC
PS = os.path.join(G, "pokemon_storage")
WALLPAPERS = ["FOREST", "CITY", "DESERT", "SAVANNA", "CRAG", "VOLCANO", "SNOW", "CAVE", "BEACH", "SEAFLOOR", "RIVER",
              "SKY", "STARS", "CHECKPOINT", "TILES", "SIMPLE"]       # sWallpapers' order; the names are the game's
WALL_DIRS_ = ["forest", "city", "desert", "savanna", "crag", "volcano", "snow", "cave", "beach", "seafloor", "river",
              "sky", "stars", "pokecenter", "tiles", "simple"]
# each wallpaper's tint: (A paper ground, A line) and (B line); B's ground is the readout's screen, A's ink the slate
WALL_TINT = {
    "FOREST": ((222, 232, 220), (120, 160, 128), (120, 216, 152)),
    "CITY": ((220, 224, 232), (104, 120, 144), (152, 192, 232)),
    "DESERT": ((236, 228, 210), (176, 148, 104), (232, 200, 136)),
    "SAVANNA": ((232, 230, 206), (156, 152, 96), (208, 208, 120)),
    "CRAG": ((226, 222, 218), (136, 124, 116), (200, 184, 168)),
    "VOLCANO": ((236, 222, 214), (176, 104, 88), (248, 144, 112)),
    "SNOW": ((236, 240, 244), (144, 168, 192), (208, 232, 248)),
    "CAVE": ((220, 216, 212), (112, 104, 100), (176, 168, 160)),
    "BEACH": ((236, 232, 216), (112, 176, 176), (136, 224, 216)),
    "SEAFLOOR": ((214, 224, 234), (88, 120, 160), (104, 168, 232)),
    "RIVER": ((218, 230, 238), (96, 144, 184), (120, 192, 240)),
    "SKY": ((226, 236, 244), (128, 168, 208), (176, 216, 248)),
    "STARS": ((222, 222, 236), (112, 112, 160), (216, 216, 255)),
    "CHECKPOINT": ((220, 236, 232), (72, 152, 136), TEAL),
    "TILES": ((224, 228, 232), (120, 132, 148), (168, 184, 200)),
    "SIMPLE": ((236, 238, 240), (176, 186, 198), (88, 120, 120)),
}


def _rnd(x, y, k=0):
    return ((x * 73856093) ^ (y * 19349663) ^ (k * 83492791)) & 0xFFFF


def motif(name, x, y):
    """The panel's pattern at (x, y), in 0 ground, 1 line, 2 accent -- each periodic in 8, 16 or 32 px so the
    wallpaper stays inside its 256 tiles."""
    if name == "FOREST":                                 # leaf veins: a stem every 16px, veins at 45 degrees
        u, v = x % 16, y % 16
        if u == 8:
            return 1
        if (u < 8 and (v + u) % 6 == 0 and u > 2) or (u > 8 and (v - u) % 6 == 0 and u < 14):
            return 1
        return 0
    if name == "CITY":                                    # lit and dark windows on an 8px grid
        u, v = x % 8, y % 8
        if 1 <= u <= 5 and 1 <= v <= 4:
            return 2 if _rnd(x // 8 % 4, y // 8 % 4) % 5 == 0 else 3
        return 0
    if name == "DESERT":                                  # dune contours
        w = int(round(3 * math.sin(2 * math.pi * x / 32)))
        return 1 if (y + w) % 8 == 0 else 0
    if name == "SAVANNA":                                 # grass ticks
        u, v = x % 16, y % 16
        ox = 4 if (y // 16) % 2 else 10
        if v in (6, 7) and abs(u - ox) == (7 - v) + 1 or (v == 7 and u == ox):
            return 1
        if (v == 5 and u == ox - 2) or (v == 5 and u == ox + 2):
            return 1
        return 0
    if name == "CRAG":                                    # a contour map, one 32px cell repeated
        u, v = x % 32 - 15.5, y % 32 - 15.5
        r = math.hypot(u * 1.2, v)
        return 1 if int(r) % 5 == 0 and r < 16 else 0
    if name == "VOLCANO":                                 # isotherms: dashed 45-degree lines
        d = (x + y) % 12
        return 1 if d == 0 and (x // 4) % 3 != 2 else (2 if d == 6 and (x // 2) % 4 == 0 else 0)
    if name == "SNOW":                                    # six-armed crystals on an offset 16px grid
        ox = 8 if (y // 16) % 2 else 0
        u, v = (x + ox) % 16 - 8, y % 16 - 8
        if (u == 0 and abs(v) <= 4) or (abs(v) == abs(u) and abs(u) <= 3 and u != 0) or (v == 0 and abs(u) <= 4):
            return 1
        return 0
    if name == "CAVE":                                    # stipple
        return 1 if _rnd(x % 32, y % 32, 7) % 11 == 0 else 0
    if name == "BEACH":                                   # scalloped waves
        u, v = x % 16 - 8, y % 12
        return 1 if v == int(round(4 - math.sqrt(max(0, 64 - u * u)) / 2)) + 4 else 0
    if name == "SEAFLOOR":                                # sonar rings
        u, v = x % 32 - 16, y % 32 - 16
        r = math.hypot(u, v)
        return 1 if abs(r - 6) < 0.6 or abs(r - 12) < 0.6 else (2 if u == 0 and v == 0 else 0)
    if name == "RIVER":                                   # flow lines
        w = int(round(2 * math.sin(2 * math.pi * (x + (y // 8) * 8) / 32)))
        return 1 if (y + w) % 8 == 0 and (x // 8 + y // 8) % 3 != 0 else 0
    if name == "SKY":                                     # a cloud's outline, a few per 32px
        u, v = x % 32, y % 32
        cx, cy = (16, 16)
        top = min(math.hypot(u - 12, v - 15), math.hypot(u - 18, v - 13), math.hypot(u - 23, v - 16))
        base = v == 19 and 8 <= u <= 27
        return 1 if (4.6 < top < 5.6 and v <= 18) or base else 0
    if name == "STARS":                                   # a star chart: a grid, stars and one constellation
        u, v = x % 32, y % 32
        if (u == 0 or v == 0) and (x + y) % 2 == 0:
            return 1
        for (sx, sy, big) in ((7, 9, 1), (21, 5, 0), (26, 22, 1), (12, 25, 0)):
            if (u, v) == (sx, sy) or (big and abs(u - sx) + abs(v - sy) == 1):
                return 2
        return 0
    if name == "CHECKPOINT":                              # a circuit: traces with 45-degree bends and pads
        u, v = x % 32, y % 32
        if v == 8 and u < 18 or (u - 18 == v - 8 and 8 <= v <= 16) or (v == 16 and u > 26):
            return 1
        if u == 26 and 16 <= v or (v == 24 and u < 10):
            return 1
        if abs(u - 4) + abs(v - 24) <= 1 or abs(u - 26) + abs(v - 31) <= 0:
            return 2
        return 0
    if name == "TILES":                                   # 16px tiles, bevelled
        u, v = x % 16, y % 16
        return 3 if u == 15 or v == 15 else (1 if (u == 0 or v == 0) and (u + v) % 2 == 0 else 0)
    return 1 if (x % 8 == 0 and y % 8 == 0) else 0       # SIMPLE: a dot every 8px


def wallpaper_art(name, direction):
    """160x144 in one palette row: the name plate (rows 0-2), the panel (rows 3-17)."""
    g = canvas(160, 144)
    for y in range(26, 142):
        for x in range(3, 157):
            m = motif(name, x - 3, y - 26)
            g[y][x] = {0: 1, 1: 3, 2: 4, 3: 2}[m]
    # the panel's rule, cut at 45 degrees: 5 outer, 6 inner light, the teal bracket in 7
    cut_box(g, 0, 23, 160, 121, 4, [5, 5, 6], None)
    bracket = 7
    for (cx, cy, sx, sy) in ((4, 27, 1, 1), (155, 27, -1, 1), (4, 139, 1, -1), (155, 139, -1, -1)):
        for i in range(6):
            put(g, cx + sx * i, cy, bracket)
            put(g, cx, cy + sy * i, bracket)
    # the plate (the box's name is printed on it in white, shadow 7,7,7): x 16-143, y 2-21
    cut_box(g, 16, 2, 128, 20, 3, [5, 8], 9)
    for i in range(4):
        put(g, 19 + i, 5, bracket)
        put(g, 19, 5 + i, bracket)
        put(g, 140 - i, 18, bracket)
        put(g, 140, 18 - i, bracket)
    return g


def wallpaper_pal(name, direction):
    gA, lA, lB = WALL_TINT[name]
    if direction == "A":
        acc = tuple(max(0, int(c * 0.75)) for c in lA)
        p = {1: gA, 2: tuple(int(c * 0.9) for c in gA), 3: lA, 4: acc, 5: SLATE_OUT, 6: SLATE_LIGHT, 7: TEAL,
             8: SLATE_LIGHT, 9: SLATE_MID}
    else:
        p = {1: (18, 28, 32), 2: (30, 44, 50), 3: tuple(int(c * 0.55) for c in lB), 4: lB, 5: (64, 76, 92), 6: (36, 52, 60),
             7: TEAL, 8: (64, 96, 96), 9: (32, 48, 56)}
    row = [(0, 0, 0)] * 16
    for k, v in p.items():
        row[k] = v
    return row


def tilemap_of(g, w, h):
    """Cut an index picture into deduplicated tiles (with flips), tile 0 the clear one: (tiles, entries)."""
    tiles = [tuple(tuple([0] * 8) for _ in range(8))]
    index = {tiles[0]: (0, 0, 0)}
    ents = []
    for ty in range(h):
        for tx in range(w):
            blk = tuple(tuple(g[ty * 8 + y][tx * 8 + x] for x in range(8)) for y in range(8))
            if blk not in index:
                t = len(tiles)
                tiles.append(blk)
                for hf in (0, 1):
                    for vf in (0, 1):
                        b = blk
                        if vf:
                            b = tuple(reversed(b))
                        if hf:
                            b = tuple(tuple(reversed(r)) for r in b)
                        index.setdefault(b, (t, hf, vf))
            ents.append(index[blk])
    return tiles, ents


def wallpaper_rgb(name, direction):
    if direction is None:
        d = os.path.join(PS, "wallpapers", WALL_DIRS_[WALLPAPERS.index(name)])
        w, h, bd, pal, px = load_png(os.path.join(d, "tiles.png"))
        rows = [pal[:16], pal[:16], pal[16:32]]
        ents = map16(os.path.join(d, "tilemap.bin"))
        return render_map([[v & 15 for v in r] for r in px], w // 8, ents, 20, 18, rows), None
    g = wallpaper_art(name, direction)
    tiles, ents = tilemap_of(g, 20, 18)
    return idx_rgba(g, wallpaper_pal(name, direction)), len(tiles)


def paw_cursor(direction):
    """cursor.png: four 32x32 frames (0 pointing, 1 closing, 2 open to take, 3 holding), in the slots the two
    shared sprite palettes give it (misc2 at rest, misc1 in the multi-move mode): 1 the halo, 2 the outline, 3 the
    face, 11 the shade, 12 the deep shade. The hot spot stays low at the left, where the hand's fingertip was."""
    if direction is None:
        w, h, bd, pal, px = load_png(os.path.join(PS, "cursor.png"))
        return [[v & 15 for v in r] for r in px]
    g = canvas(32, 128)
    for f in range(4):
        y0 = f * 32
        if direction == "A":                              # A PAW: a pad and four separate toes, toes down
            # (pad centre, pad radii, toe centres, toe radii) per frame: hover, closing, open, holding
            pad, pr, toes, tr = (
                ((15, 7.5), (5.6, 4.2), ((7.6, 17), (12.4, 19.6), (17.6, 19.6), (22.4, 17)), (2.2, 2.8)),
                ((15, 8), (5.6, 4.2), ((8.6, 17), (12.8, 19.4), (17.2, 19.4), (21.4, 17)), (2.0, 2.6)),
                ((15, 7), (5.6, 4.2), ((6.0, 16.4), (11.6, 20.2), (18.4, 20.2), (24.0, 16.4)), (2.3, 3.0)),
                ((15, 8), (5.6, 4.4), ((9.4, 15.8), (13.2, 17.4), (16.8, 17.4), (20.6, 15.8)), (1.7, 1.9)),
            )[f]
            shapes = [(pad[0], pad[1], pr[0], pr[1])] + [(tx, ty, tr[0], tr[1]) for tx, ty in toes]
            own = canvas(32, 32, -1)
            for y in range(32):
                for x in range(32):
                    for k, (sx, sy, sa, sb) in enumerate(shapes):
                        dx, dy = (x + 0.5 - sx) / sa, (y + 0.5 - sy) / sb
                        if dx * dx + dy * dy <= 1:
                            g[y0 + y][x] = 12 if dx * 0.6 + dy * 0.8 > 0.7 else (11 if dx * 0.6 + dy * 0.8 > 0.25 else 3)
                            own[y][x] = k
            for y in range(31):                           # where two beans meet, an outline parts them
                for x in range(31):
                    for nx, ny in ((x + 1, y), (x, y + 1)):
                        if own[y][x] >= 0 and own[ny][nx] >= 0 and own[ny][nx] != own[y][x]:
                            g[y0 + ny][nx] = 2
            for ring, val in ((1, 2), (2, 1)):
                snap = [r[:] for r in g[y0:y0 + 32]]
                for y in range(32):
                    for x in range(32):
                        if snap[y][x] == 0 and any(0 <= y + dy < 32 and 0 <= x + dx < 32 and snap[y + dy][x + dx]
                                                   and (val == 2 or snap[y + dy][x + dx] == 2)
                                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                            g[y0 + y][x] = val
            # the gaps between toes and pad: outline, so each bean reads on its own
            snap = [r[:] for r in g[y0:y0 + 32]]
        else:                                             # B THE POINTER: a chevron that closes into a bracket
            close = (0, 2, -1, 4)[f]
            for i in range(10):
                for t in range(3):
                    put(g, 6 + i + t, y0 + 22 - i, 3 if t == 1 else 11)     # the arrow's spine, 45 degrees
            for i in range(7 - max(0, close)):
                put(g, 6 + i, y0 + 22, 3)
                put(g, 6, y0 + 22 - i, 3)
            for i in range(3):
                put(g, 9 + i, y0 + 19, 12)
            snap = [r[:] for r in g[y0:y0 + 32]]
            for ring, val in ((1, 2), (2, 1)):
                snap = [r[:] for r in g[y0:y0 + 32]]
                for y in range(32):
                    for x in range(32):
                        if snap[y][x] == 0 and any(0 <= y + dy < 32 and 0 <= x + dx < 32 and snap[y + dy][x + dx]
                                                   and (val == 2 or snap[y + dy][x + dx] == 2)
                                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                            g[y0 + y][x] = val
    return g


def scrolling_bg(direction):
    """scrolling_bg.png (8 tiles) under the whole screen, redrawn in place on its own tilemap; scrolling_bg.gbapal
    (row 3) and scrolling_bg_move_items.gbapal (the MOVE ITEMS mode's) both keep their slots."""
    w, h, bd, pal, px = load_png(os.path.join(PS, "scrolling_bg.png"))
    sheet = [[v & 15 for v in r] for r in px]
    ents = map16(os.path.join(PS, "scrolling_bg.bin"))
    p = gbapal(os.path.join(PS, "scrolling_bg.gbapal"), 16)
    if direction is None:
        return sheet, ents, p
    g = canvas(256, 256, 8)
    for y in range(256):
        for x in range(256):
            u, v = x % 16, y % 16                        # 16px: the map repeats its 4x2 block shifted 16px
            if (u + v) % 16 == 0 or (u - v) % 16 == 0:
                g[y][x] = 9 if direction == "A" else 4
            if (u, v) == (8, 8) or (direction == "A" and (u, v) in ((7, 8), (9, 8), (8, 7), (8, 9))):
                g[y][x] = 4 if direction == "A" else 5
    retile(sheet, w // 8, [(ents, 32, g)], skip0=False)
    q = list(p)
    if direction == "A":
        q[8], q[9], q[4], q[5] = (204, 212, 220), (188, 198, 208), SLATE_LIGHT, TEAL
    else:
        q[8], q[9], q[4], q[5] = (14, 22, 26), (20, 32, 36), (30, 50, 52), (40, 88, 80)
    return sheet, ents, q


def pc_mock(direction, wall="FOREST", cursor_frame=0):
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    sheet, ents, sp = scrolling_bg(direction)
    rows = [sp] * 16
    b = render_map(sheet, 4, ents, 32, 20, rows, pal_of=lambda e: 0)
    im.paste(b, (0, 0), b)
    w, h, bd, pal, msh = load_png(os.path.join(PS, "menu.png"))
    mrows = [gbapal(os.path.join(PS, "interface.gbapal"), 16), pal[16:32], gbapal(os.path.join(PS, "interface_no_display_mon.gbapal"), 16)]
    ments = [(t - 256 if t >= 256 else t, hf, vf, pn) for t, hf, vf, pn in map16(os.path.join(PS, "menu.bin"))]
    mm = render_map([[v & 15 for v in r] for r in msh], w // 8, [e if e[0] else (0, 0, 0, 0) for e in ments], 32, 20, mrows)
    im.paste(mm, (0, 0), mm)
    wp, n = wallpaper_rgb(wall, direction)
    im.paste(wp, (80, 16), wp)
    title = "BOX 1"
    tw = text_width(title)
    say(im, 80 + 80 - tw // 2, 16 + 3, title, (248, 248, 248), (56, 56, 56))
    party = [p[0] for p in PARTY] + ["BULBASAUR", "SQUIRTLE", "CATERPIE", "ODDISH", "PORYGON", "MEWTWO"]
    for i, sp_ in enumerate(party[:12]):
        c, r = i % 6, i // 6
        ic = icon(sp_)
        im.paste(ic, (80 + 4 + 24 * c - 4, 16 + 28 + 24 * r - 6), ic)
    cur = paw_cursor(direction)
    pal2 = gbapal(os.path.join(PS, "misc2.gbapal"), 16)
    ci = idx_rgba(cur[cursor_frame * 32:cursor_frame * 32 + 32], pal2)
    im.paste(ci, (80 + 4 + 24 * 2 - 2, 16 + 28 - 22), ci)
    return im


def pc_family(direction):
    """All sixteen wallpapers, each at half size, in a 240x160 plate (4 x 4)."""
    im = Image.new("RGB", (240, 160), (24, 26, 30))
    for i, name in enumerate(WALLPAPERS):
        wp, n = wallpaper_rgb(name, direction)
        t = wp.convert("RGB").resize((56, 36), Image.LANCZOS)
        im.paste(t, (4 + (i % 4) * 59, 2 + (i // 4) * 40))
    return im


def pc_wall_sheet(out):
    """Every wallpaper at real size, the engine's beside A and B, with its name and tile count."""
    F = label_font(11)
    W = 3 * 168 + 16
    H = 16 * 166 + 40
    sh = Image.new("RGB", (W * 2, H // 2 + 40), (24, 26, 30))
    d = ImageDraw.Draw(sh)
    d.text((12, 8), "T-530 PC WALLPAPERS -- DRAFT: engine now | A TERMINAL | B READOUT (real size; the box name in "
                    "white on the plate as the game prints it)", fill=(232, 236, 240), font=F)
    for i, name in enumerate(WALLPAPERS):
        X = (i % 2) * W + 12
        Y = 32 + (i // 2) * 166
        d.text((X, Y), name, fill=(176, 208, 200), font=F)
        for k, dname in enumerate((None, "A", "B")):
            wp, n = wallpaper_rgb(name, dname)
            tile = wp.convert("RGB")
            say(tile, 80 - text_width(name) // 2, 3, name, (248, 248, 248), (56, 56, 56))
            sh.paste(tile, (X + k * 168, Y + 14))
            if n:
                d.text((X + k * 168 + 100, Y), "%d tiles" % n, fill=(120, 128, 140), font=F)
    sh.save(out)
    return out


# ================================================================================================ ITEMS
# The item PC and the TRAP TABLE (berry pouch): one 32x20 map each, redrawn in place. Rows 1-14 (16) use palette row 0;
# the description strip uses row 1, and row 2 when a context menu opens (item_pc.c SetBgTilemapPalette(1, 0, 14, 30, 6,
# palIdx + 1); berry_pouch.c the same at row 16): so row 2 is row 1 dimmed, and the strip is drawn in slots 7-15 only
# (rows 1/2 leave 1-6 black). The list is printed in the standard menu palette (dark ink): its paper stays light in
# both directions. The description is printed in text window palette 2 (white ink): the strip stays dark in both.
ITEM_SCREENS = {   # every rectangle sits on the vanilla tilemap's own grid: its repeated tiles (the list's row tiles,
                  # the mirrored side frames, the plinth's mirrored shadow) are why each edge is where it is
    "itempc": dict(png="item_pc/bg.png", bin="item_pc/bg.bin", strip_y=112, title=None,
                   badge=(0, 0, 50, 44), panel=(48, 2, 208, 110), rows=(23, 16, 5), lines=(64, 192),
                   scroll=(209, 8, 217, 104), icon=(6, 120, 34, 148), plinth=None, rule=None),
    "berry": dict(png="berry_pouch/background.png", bin="berry_pouch/background.bin", strip_y=128,
                  title=(1, 4, 86, 28), badge=None, panel=(89, 3, 231, 118), rows=(23, 16, 6), lines=(96, 224),
                  scroll=None, icon=(6, 130, 34, 158), plinth=(12, 98, 68, 108), rule=(84, 34, 118)),
}
ITEM_DIRS = {
    "A": dict(name="TERMINAL",
              row0={1: (212, 218, 224), 2: (190, 198, 208), 3: SLATE_OUT, 4: SLATE_MID, 5: SLATE_LIGHT, 6: TEAL,
                    7: PAPER, 8: (200, 208, 214), 9: AMBER, 10: (226, 230, 234), 11: (232, 236, 240),
                    12: (120, 136, 152), 13: TEAL_DK, 14: (236, 238, 240), 15: (176, 188, 200)},
              strip=({7: SLATE_LIGHT, 8: (220, 226, 232), 9: (236, 240, 244), 10: PAPER, 11: SLATE_LIGHT,
                      12: SLATE_OUT, 13: (20, 26, 34), 14: (100, 116, 132), 15: SLATE_MID}, 0.72)),
    "B": dict(name="READOUT",
              row0={1: (16, 26, 30), 2: (30, 50, 52), 3: (8, 12, 16), 4: (64, 76, 92), 5: (96, 168, 152), 6: TEAL,
                    7: (226, 242, 234), 8: (168, 208, 192), 9: AMBER, 10: (36, 52, 60), 11: (24, 38, 42),
                    12: (40, 72, 64), 13: TEAL, 14: (210, 232, 222), 15: (28, 44, 48)},
              strip=({7: (64, 96, 96), 8: (200, 232, 220), 9: (216, 240, 230), 10: (226, 242, 234),
                      11: (96, 168, 152), 12: (64, 76, 92), 13: (8, 12, 16), 14: (36, 56, 60), 15: (28, 44, 48)}, 0.6)),
}


def item_target(key, direction):
    sc = ITEM_SCREENS[key]
    g = canvas(256, 160, 1)
    for y in range(160):                                 # the ground's grain (graph paper / graticule), as the party's
        for x in range(256):
            if direction == "A":
                if (x % 8 == 7 and y % 2 == 0) or (y % 8 == 7 and x % 2 == 0):
                    g[y][x] = 2
            elif x % 8 == 7 and y % 8 == 7:
                g[y][x] = 5
            elif (x % 8 == 7 and y % 8 == 3) or (y % 8 == 7 and x % 8 == 3):
                g[y][x] = 2
    x0, y0, x1, y1 = sc["panel"]                         # the list's paper: the slate rule, 45 degrees, the bracket
    cut_box(g, x0, y0, x1 - x0, y1 - y0, 3, [3, 5], 7)
    ry, step, n = sc["rows"]
    for k in range(n):
        for x in range(*sc["lines"]):
            if (x // 2) % 2 == 0:
                put(g, x, ry + k * step, 8)
    for i in range(5):
        put(g, x0 + 3 + i, y0 + 2, 6)
        put(g, x0 + 2, y0 + 3 + i, 6)
    if sc["scroll"]:
        a, b, c, d = sc["scroll"]
        cut_box(g, a, b, c - a, d - b, 2, [3], 10)
        fill(g, a + 2, b + 4, c - 2, b + 24, 13)
    if sc["badge"]:                                      # the storage's badge: a slate case, two drawers, a lamp
        a, b, c, d = sc["badge"]
        cut_box(g, a - 6, b - 6, c - a + 6, d - b + 6, 5, [3, 4], 4)
        for yy in (17, 27):
            cut_box(g, 18, yy, 24, 8, 2, [3], 15)
            fill(g, 27, yy + 3, 33, yy + 5, 3)
        for xx in (35, 36):
            put(g, xx, 11, 6)
            put(g, xx, 12, 6)
    if sc["title"]:                                      # the pocket's name, printed in the menu's dark ink
        a, b, c, d = sc["title"]
        cut_box(g, a, b, c - a, d - b, 3, [3, 5], 14)
        for i in range(4):
            put(g, a + 2 + i, b + 2, 6)
            put(g, a + 2, b + 2 + i, 6)
    if sc["plinth"]:                                     # the pocket's picture (a sprite) stands on a slate plinth
        a, b, c, d = sc["plinth"]
        cut_box(g, a, b, c - a, d - b, 3, [3, 5], 4)
    if sc["rule"]:
        x, ya, yb = sc["rule"]
        for y in range(ya, yb):
            put(g, x, y, 4 if (y // 2) % 2 == 0 else 1)
    # the strip (palette row 1): slots 7-15 only
    sy = sc["strip_y"]
    for y in range(sy, 160):
        for x in range(256):
            g[y][x] = 15
            if direction == "A" and (y - sy) % 4 == 3 and x % 2 == 0:
                g[y][x] = 14
            if direction == "B" and (y - sy) % 8 == 7 and x % 8 == 7:
                g[y][x] = 11
    for x in range(256):
        g[sy][x] = 13
        g[sy + 1][x] = 12
    a, b, c, d = sc["icon"]                              # the item's icon bay
    cut_box(g, a, b, c - a, d - b, 3, [13, 7], 10)
    for i in range(4):
        put(g, a + 3 + i, b + 2, 11)
        put(g, a + 2, b + 3 + i, 11)
    return g


def item_build(key, direction):
    sc = ITEM_SCREENS[key]
    w, h, bd, pal, px = load_png(os.path.join(G, sc["png"]))
    sheet = [list(r) for r in px]
    rows = [list(pal[i * 16:(i + 1) * 16]) for i in range(3)]
    ents = map16(os.path.join(G, sc["bin"]))
    if direction is None:
        return sheet, w // 8, rows, ents
    d = ITEM_DIRS[direction]
    retile(sheet, w // 8, [(ents, 32, item_target(key, direction))])
    for k, v in d["row0"].items():
        rows[0][k] = v
    st, dim = d["strip"]
    for k, v in st.items():
        rows[1][k] = v
        rows[2][k] = tuple(int(c * dim) for c in v) if k not in (8, 9, 10) else v
    return sheet, w // 8, rows, ents


def item_icon(stem):
    w, h, bd, pal, px = load_png(os.path.join(G, "items/icons/%s.png" % stem))
    return idx_rgba(px, jasc(os.path.join(G, "items/icon_palettes/%s.pal" % stem)))


ITEM_CONTENT = {
    "itempc": (["RECOVER", "INCREMENT", "PATCH", "COOLANT", "WATCHDOG", "CANCEL"], [6, 30, 3, 2, 2, None],
               "d_recover", ["Puts back a little of what was", "lost. Restores 20 HP."], (56, 8)),
    "berry": (["LOW MARK", "LEAK TRAP", "HEAT TRAP", "HIGH MARK", "CATCH ALL", "THROTTLE TRAP", "CLOSE"],
              [4, 2, 1, 2, 1, 3, None], "d_low_mark", ["A mark set low. When health falls,", "it restores 10 HP, once."],
              (88, 8)),
}


def item_mock(key, direction, dimmed=False):
    sheet, per, rows, ents = item_build(key, direction)
    im = Image.new("RGB", (240, 160), q5(rows[0][0]))
    b = render_map([[v & 15 for v in r] for r in sheet], per, ents, 32, 20, rows,
                   pal_of=lambda e: (2 if dimmed and e[3] == 1 else e[3]))
    im.paste(b, (0, 0), b)
    names, counts, ic, desc, (lx, ly) = ITEM_CONTENT[key]
    std = jasc(os.path.join(G, "text_window/stdpal_0.pal"))
    for i, (n, c) in enumerate(zip(names, counts)):
        y = ly + 16 * i - 2
        if i == 1:
            say(im, lx + 1, y, "▶" if False else "", std[2], std[3])
            d = ImageDraw.Draw(im)
            d.polygon([(lx + 2, y + 4), (lx + 2, y + 12), (lx + 6, y + 8)], fill=q5(std[2]))
        say(im, lx + 9, y, n, std[2], std[3])
        if c is not None:
            s = "×%d" % c
            say(im, lx + (136 if key == "berry" else 140) - text_width("%d" % c) - 8, y, "x", std[2], std[3], small=True)
            say(im, lx + (136 if key == "berry" else 140) - text_width("%d" % c), y, "%d" % c, std[2], std[3])
    w2 = jasc(os.path.join(G, "text_window/stdpal_2.pal"))
    sy = ITEM_SCREENS[key]["strip_y"]
    for i, line in enumerate(desc):
        say(im, 40, sy + 2 + 14 * i, line, w2[1], w2[2])
    a, b_, c, d_ = ITEM_SCREENS[key]["icon"]
    it = item_icon(ic)
    im.paste(it, (a + (c - a - 24) // 2, b_ + (d_ - b_ - 24) // 2), it)
    if key == "berry":                                   # the pocket's picture is a sprite (berry_pouch.png), kept
        w, h, bd, pal, px = load_png(os.path.join(G, "berry_pouch/berry_pouch.png"))
        bp = idx_rgba(px, pal[:16])
        im.paste(bp, (12, 44), bp)
        say(im, 10, 6, "TRAP TABLE", std[2], std[3])
    return im


# ================================================================================================ the sheet
def label_font(n=12):
    for f in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def contact(title, columns, notes, out, scale=2):
    """columns: [(caption, [240x160 images...])]: the engine now, A, B -- each at 1x and at `scale`x."""
    F, S = label_font(14), label_font(11)
    import textwrap
    notes = [w for n in notes for w in textwrap.wrap(n, 205, subsequent_indent="    ")]
    rows = max(len(c[1]) for c in columns)
    cw = 240 * scale + 16
    W = 16 + len(columns) * cw
    H = 48 + rows * (160 * scale + 12 + 160 + 28) + 18 * len(notes) + 20
    sh = Image.new("RGB", (W, H), (24, 26, 30))
    d = ImageDraw.Draw(sh)
    d.text((16, 12), title, fill=(232, 236, 240), font=F)
    for ci, (cap, ims) in enumerate(columns):
        x = 16 + ci * cw
        y = 40
        d.text((x, y - 4), cap, fill=(176, 208, 200), font=S)
        y += 12
        for im in ims:
            sh.paste(im.convert("RGB").resize((240 * scale, 160 * scale), Image.NEAREST), (x, y))
            y += 160 * scale + 6
            sh.paste(im.convert("RGB"), (x, y))
            d.text((x + 248, y + 4), "real size", fill=(120, 128, 140), font=S)
            y += 160 + 22
    y = H - 18 * len(notes) - 12
    for n in notes:
        d.text((16, y), n, fill=(200, 204, 210), font=S)
        y += 18
    sh.save(out)
    return out


def halftone(im):
    g = im.convert("L").convert("RGB")
    return g


# ================================================================================================ the files
def _png(px, pal, bd):
    return ("png", px, [q5(c) for c in pal], bd)


def outputs(screen, direction):
    """{path under graphics/: payload} -- each file in the engine's own format: the same size, bit depth, palette
    length and (for a .bin) map size as the file it replaces. Generated .4bpp/.gbapal/.lz follow from these."""
    out = {}
    if screen == "party":
        sheet, per, rows, maps, res = party_build(direction)
        pal = [c for r in rows for c in (list(r) + [(0, 0, 0)] * 16)[:16]]
        out["party_menu/bg.png"] = _png(sheet, pal, 8)
    elif screen == "summary":
        w, h, bd, pal, px = load_png(os.path.join(SS, "bg.png"))
        rows = summary_rows(direction)
        out["summary_screen/bg.png"] = _png(px, [c for r in rows for c in r], bd)
        pals = bar_pals(direction)
        out["summary_screen/hp_bar.png"] = _png(bar_tiles(direction, False), pals[0], 4)
        out["summary_screen/exp_bar.png"] = _png(bar_tiles(direction, True), pals[0], 4)
        out["summary_screen/hp_bar_yellow.pal"] = ("pal", pals[1])
        out["summary_screen/hp_bar_red.pal"] = ("pal", pals[2])
        L, R, cp = cursor_frames(direction)
        out["summary_screen/move_selection_cursor_left.png"] = _png(L, cp, 4)
        out["summary_screen/move_selection_cursor_right.png"] = _png(R, cp, 4)
        out["summary_screen/move_selection_cursor.pal"] = ("pal", cp)
        st, sp, mk, mp = star_and_mark(direction)
        out["summary_screen/shiny_star.png"] = _png(st, sp, 4)
        out["summary_screen/pokerus_cured.png"] = _png(mk, mp, 4)
    elif screen == "items":
        for key, sc in ITEM_SCREENS.items():
            sheet, per, rows, ents = item_build(key, direction)
            out[sc["png"]] = _png(sheet, [c for r in rows for c in r], 8)
            if key == "berry":                            # nobody is a boy or a girl: the "female" row 0 is row 0
                out["berry_pouch/background_female.pal"] = ("pal", rows[0])
    elif screen == "pc":
        for name, d in zip(WALLPAPERS, WALL_DIRS_):
            g = wallpaper_art(name, direction)
            tiles, ents = tilemap_of(g, 20, 18)
            per = 8
            n = (len(tiles) + per - 1) // per
            sheet = canvas(64, n * 8)
            for t, blk in enumerate(tiles):
                for y in range(8):
                    for x in range(8):
                        sheet[(t // per) * 8 + y][(t % per) * 8 + x] = blk[y][x]
            row = wallpaper_pal(name, direction)
            out["pokemon_storage/wallpapers/%s/tiles.png" % d] = _png(sheet, row + row, 8)
            out["pokemon_storage/wallpapers/%s/tilemap.bin" % d] = (
                "bin", b"".join(struct.pack("<H", t | (hf << 10) | (vf << 11) | ((1 if t else 0) << 12))
                                for t, hf, vf in ents))
        out["pokemon_storage/cursor.png"] = _png(paw_cursor(direction),
                                                 load_png(os.path.join(PS, "cursor.png"))[3][:16], 4)
        sheet, ents, q = scrolling_bg(direction)
        out["pokemon_storage/scrolling_bg.png"] = _png(sheet, q, 4)
        mi = list(gbapal(os.path.join(PS, "scrolling_bg_move_items.gbapal"), 16))
        for k in (4, 5, 8, 9):                            # MOVE ITEMS: the same drawing, warmed toward amber
            mi[k] = tuple(min(255, int(c * 0.8 + a * 0.2)) for c, a in zip(q[k], AMBER))
        out["pokemon_storage/scrolling_bg_move_items.pal"] = ("pal", mi)
    return out


def put_files(files, root):
    import gbafont
    for rel, payload in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if payload[0] == "png":
            _, px, pal, bd = payload
            n = 16 if bd == 4 else len(pal)
            pal = (list(pal) + [(0, 0, 0)] * 16)[:max(16, n)] if bd == 8 else (list(pal) + [(0, 0, 0)] * 16)[:16]
            gbafont.png_save(p, len(px[0]), len(px), bd, b"".join(bytes(c) for c in pal), px)
        elif payload[0] == "pal":
            write_jasc(payload[1], p)
        elif payload[0] == "bin":
            open(p, "wb").write(payload[1])
    return [os.path.join(root, r) for r in files]



SHEET_NOTES = {
    "party": ["Rows: choosing (the first box current); MOVE TO WHERE? (PACKET picked to switch, the cursor on CANCEL).",
              "Kept: bg.bin and the 5 slot maps (the code blits slot tiles by id); palette rows 3-10 as the state buffer "
              "(box 4/5/6 + 1/7/8 per state, HP 9/10 green/yellow/red, gender 11/12); text 3 on 2; CANCEL palette 1/2."],
    "summary": ["Rows: DAEMON SKILLS; KNOWN MOVES with the move cursor; the parts at 2x (HP bar in its three palettes, "
                "EXP bar, the cursor's two frames, the shiny star, the pokerus mark).",
                "Kept: the backdrop's drawing (palette rows retinted only), T-481 B's slots on row 0 (6 day line, 14 pip, "
                "2/3/8/10 the hour); the bar's 12-tile frame order; the yellow/red palettes differ only in 1/2."],
    "pc": ["Rows: BOX 1 on FOREST with the cursor pointing; on CHECKPOINT holding; all sixteen wallpapers (half size). "
           "A's cursor is a PAW, B's a POINTER; both in misc2/misc1's slots (white at rest, yellow in multi-move).",
           "Kept: 20x18 maps, <=256 tiles (35-69 used), two palette rows, the plate dark for the white box name; the "
           "cursor's 4 frames; scrolling_bg's map (8 tiles in place) and its MOVE ITEMS palette."],
    "items": ["Rows: ITEM STORAGE; the same with a menu open (the strip's row 2, dimmed by the code); the TRAP TABLE.",
              "Kept: both maps (tiles redrawn in place on the vanilla grid); the strip in slots 7-15 of rows 1/2; the "
              "list's paper light (dark menu ink) and the strip dark (white description ink); the pocket's sprite."],
}

# ================================================================================================ report, draft, write
def sheet_notes(screen, dirs):
    n = list(SHEET_NOTES[screen])
    if dirs:
        n += ["%s %s: %s" % (k, v["name"], v["said"]) for k, v in dirs.items()]
    return n + ["DRAFT -- drawn in code (tools/gbamenus.py), nothing in the engine until the user picks; recommended: "
                + RECOMMENDED[screen]]


def report():
    print("T-530 the menus: drafts only until the user picks (APPROVED = %r)" % APPROVED)
    for dname in ("A", "B"):
        sheet, per, rows, maps, (miss, n) = party_build(dname)
        print("  PARTY %s %s: %d tile ids redrawn in place, %d uses that differ from their vote" %
              (dname, PARTY_DIRS[dname]["name"], n, miss))
        for r in (3, 5, 7):
            print("    row %d: ink/fill lightness %3.0f/%3.0f  shadow %3.0f  rim %3.0f  (HALFTONE reads lightness)" %
                  (r, lum(rows[r][3]), lum(rows[r][5]), lum(rows[r][2]), lum(rows[r][1])))
    for dname in ("A", "B"):
        rows = summary_rows(dname)
        print("  SUMMARY %s: row 0 slots 6 (day line) %s, 14 (pip) %s, hour on 2/3/8/10 -- the roles kept" %
              (dname, rows[0][6], rows[0][14]))
        counts = [tilemap_of(wallpaper_art(n, dname), 20, 18)[0] for n in WALLPAPERS]
        print("  PC %s: wallpapers use %d-%d tiles of 256" % (dname, min(map(len, counts)), max(map(len, counts))))
        for key in ITEM_SCREENS:
            sc = ITEM_SCREENS[key]
            w, h, bd, pal, px = load_png(os.path.join(G, sc["png"]))
            miss, n = retile([list(r) for r in px], w // 8, [(map16(os.path.join(G, sc["bin"])), 32,
                                                                item_target(key, dname))])
            print("  ITEMS %s %s: %d tiles redrawn in place, %d uses differ from their vote (the mock shows them)"
                  % (dname, key, n, miss))
    print("  RUN-TIME: HALFTONE greys menus too; T-481 B writes SUMMARY row 0 (6/14, hour 0x454C); the party's state "
          "buffer rows 3-10; the strip's row 2 (item PC, TRAP TABLE); the PC cursor in misc1/misc2's slots")


def draft(out):
    os.makedirs(out, exist_ok=True)
    made = []
    for dname in ("A", "B"):
        for screen in ("party", "summary", "items", "pc"):
            put_files(outputs(screen, dname), os.path.join(out, dname, "graphics"))
    # PARTY
    cols = []
    for dname in (None, "A", "B"):
        cols.append(("ENGINE NOW" if dname is None else "%s %s" % (dname, PARTY_DIRS[dname]["name"]),
                     [party_mock(dname), party_mock(dname, "switch")]))
    made.append(contact("T-530 PARTY -- DRAFT", cols, sheet_notes("party", PARTY_DIRS), os.path.join(out, "party_sheet.png")))
    cols = []
    for dname in (None, "A", "B"):
        cols.append(("ENGINE NOW" if dname is None else "%s %s" % (dname, SUM_DIRS[dname]["name"]),
                     [summary_mock(dname), summary_mock(dname, "moves"), summary_parts(dname)]))
    made.append(contact("T-530 SUMMARY -- DRAFT", cols, sheet_notes("summary", SUM_DIRS), os.path.join(out, "summary_sheet.png")))
    cols = []
    for dname in (None, "A", "B"):
        cols.append(("ENGINE NOW" if dname is None else "%s %s" % (dname, {"A": "TERMINAL", "B": "READOUT"}[dname]),
                     [pc_mock(dname, "FOREST", 0), pc_mock(dname, "CHECKPOINT", 3), pc_family(dname)]))
    made.append(contact("T-530 PC -- DRAFT", cols, sheet_notes("pc", None), os.path.join(out, "pc_sheet.png")))
    cols = []
    for dname in (None, "A", "B"):
        cols.append(("ENGINE NOW" if dname is None else "%s %s" % (dname, ITEM_DIRS[dname]["name"]),
                     [item_mock("itempc", dname), item_mock("itempc", dname, True), item_mock("berry", dname)]))
    made.append(contact("T-530 ITEM SCREENS (item PC, TRAP TABLE) -- DRAFT", cols, sheet_notes("items", None),
                        os.path.join(out, "items_sheet.png")))
    made.append(pc_wall_sheet(os.path.join(out, "pc_wallpapers_sheet.png")))
    return made


def main():
    if A.write:
        if not A.approved or not A.pick:
            sys.exit("gbamenus: --write needs --approved and --pick screen=A|B,... (the user's picks)")
        picks = dict(kv.split("=") for kv in A.pick.split(","))
        for screen, dname in picks.items():
            if screen not in ("party", "summary", "items", "pc") or dname not in ("A", "B"):
                sys.exit("gbamenus: unknown pick %s=%s" % (screen, dname))
            for p in put_files(outputs(screen, dname), G):
                print("  wrote", os.path.relpath(p, ROOT))
        print("  now: build all four ROMs; summary_screen/bg.png's palette changed, so re-run gbacalendar_ui.py "
              "(report) to see the SUMMARY's measured slots still hold")
    if A.draft:
        for p in draft(A.draft):
            print("  wrote", os.path.relpath(p, ROOT))
        return
    report()


if __name__ == "__main__":
    main()
