#!/usr/bin/env python3
"""T-524: the battle UI -- the message box, the healthboxes, the level-up banner and the party row, drawn anew in the
TERMINAL family (T-523).

    python3 tools/gbabattleui.py                        # report: every file, what loads it, the slots the code
                                                        #   writes at run time, and what each direction changes
    python3 tools/gbabattleui.py --draft [DIR]          # draw both directions into DIR (gfx/drafts/t524_battle_ui/),
                                                        #   the contact sheet and a mock battle screen per direction
    python3 tools/gbabattleui.py --write --approved --main 1   # write the chosen direction into the engine.
                                                        #   Refuses without --approved, and without --main.

DRAFT, 2026-11-06, the user away ("Battle UI", the vanilla-art census's gap 3). Every pixel here is drawn in code: no AI
image, nothing traced. The engine's own files are read only to keep what this does not own byte for byte.

WHAT THE ENGINE DRAWS, AND HOW (graphics/battle_interface/, src/battle_bg.c, src/battle_interface.c)
  THE MESSAGE BOX   textbox.png (128x128), textbox.bin (32x64 map), textbox1.pal -> BG palette 0 (battle_bg.c
                    LoadBattleTextboxAndBackground; also the daycare and trade scenes). The map lays tiles 03-11 as an
                    8px ring round B_WIN_MSG (x 8-231, y 120-151): 03 04 05.. 06 07 along the top, 08 | 0c down the
                    sides, 0d 0e 0f.. 10 11 along the foot -- no flips, so the foot is its own drawing. 09-0b sit under
                    the window. The ACTION prompt reuses 03-0f on its left half.
  THE ACTION MENU   and THE MOVE MENU are NOT in this file at run time: textbox.bin's palette-1 tiles (0x12-0x1a)
  AND MOVE MENU     are overwritten by LoadBattleMenuWindowGfx -> LoadUserWindowGfx, i.e. the player's OPTIONS frame
                    -- T-523's family, TERMINAL by default -- and textbox2.pal is overwritten with that frame's
                    palette. Their text palette is BG 5, whose 12-15 the code sets (battle_bg.c) and whose 1-5 the
                    move menu writes every frame (type colours, T-415's glint, T-480's hour mark). So the menus already
                    belong to the family; nothing here touches them.
  THE HEALTHBOXES   healthbox_singles_player (128x64: two 64x64 sprites), _singles_opponent, _doubles_player,
                    _doubles_opponent (128x32: two 64x32), _safari (64x128) -- all on healthbox.pal (OBJ, tag
                    TAG_HEALTHBOX_PAL). The PNG is in 1D sprite order, not as seen: a 64-wide sprite takes 8 tiles a
                    row, so each PNG row of 16 tiles is two screen rows. The HP bar is a separate 32x8 sprite on
                    healthbar.pal laid over the box; its tiles come from healthbox_elements.png (DAEMONS's: the status
                    words, THRASHING's mark, the party slots), which this does not redraw except the party markers.
  THE LEVEL-UP      level_up_banner.png (64x40, 36 tiles laid into a 12x3 window, B_WIN_LEVEL_UP_BANNER) with its own
  BANNER            palette from the PNG -> BG palette 6. The daemon's icon covers x 0-31.
  THE PARTY ROW     party_summary_bar.png (128x8: a 64x16 sprite, healthbox.pal), and the markers -- tiles 66-69 of
                    healthbox_elements.png on healthbar.pal (whole, empty, in a state, down) -- and tile 70, the CAUGHT
                    marker on a wild daemon's box, copied into the HP bar's sprite and so on healthbar.pal too. 66-69 were redrawn as USERBOXes (a2eb623cf);
                    70 is still FireRed's POKe BALL.

THE RUN-TIME CONTRACT EACH DROP-IN KEEPS
  BG palette 0 (message box): 1 the ink, 6 its shadow, 15 the fill (sTextOnWindowsInfo B_WIN_MSG/ACTION_PROMPT); the
    frame is drawn in 9, 11, 13, 14 and here also 10 (vanilla's second magenta, which nothing in a battle writes or
    prints in: {COLOR PURPLE} is 0A only in the field's box, and the more-text arrow draws in 2, 4 and 9). Slot 12 is
    NOT free: it is RESERVED, never drawn -- T-459 C's lean (daemons_three.c sLeanPurple) and THE LENS / PATTERN's
    prompt (daemons_spellbook.c sEmerald) load their colour into it each time they print, so a frame pixel there would
    turn purple or green mid-battle; textbox1.pal keeps a magenta placeholder in it (gensense.py checks textbox.png).
    Nothing else recolours BG 0 in a battle: T-481 A tints rows 2-4 (the terrain) only, T-482's pulse rows 2-4,
    T-415's weather rows 2-4.
  healthbox.pal: 1 ink, 2 the plate the text is printed on (FillWindowPixelBuffer(PIXEL_FILL(2))) -- every text zone
    must stay 2 -- and 3 its shadow; 10 the female mark and 11 the male mark (TEXT_DYNAMIC_COLOR_1/2), 11 also the
    EXP fill; 12-15 are WRITTEN AT RUN TIME, one per battler, with the status badge's colour (sStatusIconColors,
    9.15) -- never drawn in. The level-up flash blends one entry toward RGB(20,27,31).
  healthbar.pal: 10/11 green, 12/13 yellow, 14/15 red -- the code picks the TILE set by HP (>50%, >20%), so these six
    are kept exactly; 2, 5, 6 the trough, 3, 6, 7, 8 the "HP" plate; 1, 3, 4, 5, 6 the party markers.
  Text the code writes into a box (name, level, HP numbers, status, EXP, the HP bar's cap) overwrites whole tile rows,
    so those tiles are never drawn here: a direction recolours them and redraws only frame pixels outside them.
  HALFTONE (T-430) greys every one of these palettes in the unread places; both directions hold their contrast in
    grey (light on dark or dark on light, never hue alone). SPIRITS' tone (T-519) and T-481's day and hour touch the
    daemons and the terrain, not the interface.

THE TWO DIRECTIONS
  1  TERMINAL plain    the slate rule of T-523's box, 45-degree corners, the corner bracket in the trim's teal, the
                       paper and ink of the field's message box; the boxes keep their shape, now slate on paper.
  2  TERMINAL readout  an instrument: a dark screen with phosphor text, a graticule (a tick every 8px) on every rule,
                       the HP bar's surround a meter with its quarter marks, the level in a bracketed register; the
                       status words and the gender marks stay what 9.15 made them (WORDS, not glyphs) -- lit on the screen.
"""
import argparse, importlib.util, os, shutil, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
BI = os.path.join(GBA, "graphics/battle_interface")
FONTS = os.path.join(GBA, "graphics/fonts")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t524_battle_ui")

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes really runs the write")
ap.add_argument("--main", choices="12")
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

MAIN_RECOMMENDED = "2"
APPROVED = "2"                       # the user's pick, 2026-11-06: "2 Readout"


def q5(c):
    return tuple((v >> 3) << 3 for v in c)


# ============================================================================================ the engine's own files
def load_png(p):
    import gbafont
    w, h, bd, plte, px = gbafont.png_load(p)
    pal = [tuple(plte[i:i + 3]) for i in range(0, len(plte), 3)]
    return w, h, bd, pal, px


def save_png(p, px, pal, bd=4):
    import gbafont
    n = 1 << bd
    pal = (list(pal) + [(0, 0, 0)] * n)[:n]
    #  a file whose pixels and palette already match is left alone: other tools (genthrashicon) write the same sheet
    #  with their own PNG encoder, and rewriting identical pixels only flips its bytes back and forth (2026-11-07)
    if os.path.exists(p):
        try:
            from PIL import Image
            im = Image.open(p)
            if (im.mode == "P" and im.size == (len(px[0]), len(px))
                    and [tuple(im.getpalette()[3 * i:3 * i + 3]) for i in range(n)] == [q5(c) for c in pal]
                    and list(im.getdata()) == [v for row in px for v in row]):
                return
        except Exception:
            pass
    gbafont.png_save(p, len(px[0]), len(px), bd, b"".join(bytes(q5(c)) for c in pal), px)


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


def copy(px):
    return [list(r) for r in px]


# ============================================================================================ the palettes
# T-523 A's own colours, so the battle is the same family as the field: OUT the outline, MID the rule, LIGHT the bevel,
# TEAL the corner bracket (the field's slot 14 -- the weekday's trim there; a fixed teal here, see the report).
OUT, MID, LIGHT, TEAL = (32, 40, 52), (88, 104, 120), (176, 192, 204), (112, 208, 184)
PAPER, INK, SHADE = (248, 248, 248), (96, 96, 96), (208, 208, 200)          # stdpal_0's 1, 2, 3 (the field box)
SCREEN, PHOS, PHOS_SH = (20, 32, 36), (184, 240, 208), (40, 72, 64)         # the readout's screen and its text
# BG palette 0 slot 12 is loaded at run time (T-459 C's lean, the spellbook's prompt): never drawn, and kept magenta so
# a stray pixel shows. The frame's teal is slot 10 instead.
BRACKET, LEAN_SLOT, LEAN_PLACEHOLDER = 10, 12, (248, 0, 248)

DIRS = {
    "1": dict(name="TERMINAL plain",
              said="the slate rule of the field's box, 45-degree corners, the teal bracket; paper and ink",
              # BG palette 0: 1 ink, 6 shadow, 15 fill; 9 10 11 13 14 the frame; 12 the lean's, never drawn
              box={1: INK, 6: SHADE, 15: PAPER, 9: (128, 144, 160), 10: TEAL, 11: LIGHT, 12: LEAN_PLACEHOLDER,
                   13: OUT, 14: MID},
              hb={1: (48, 56, 64), 2: (240, 244, 240), 3: (200, 208, 208), 4: LIGHT, 5: (128, 144, 160), 6: MID,
                  7: OUT, 8: (60, 72, 88), 9: TEAL, 10: (240, 128, 136), 11: (88, 184, 240)},
              bar={1: (40, 48, 56), 2: (240, 244, 240), 3: (200, 208, 208), 4: (128, 136, 144), 5: MID,
                   6: (44, 56, 68), 7: (168, 240, 216), 8: TEAL},
              banner={1: PAPER, 2: OUT, 3: OUT, 4: MID, 5: (64, 76, 92), 6: LIGHT, 7: TEAL, 8: (128, 144, 160),
                      9: (48, 58, 72)}),
    "2": dict(name="TERMINAL readout",
              said="an instrument: a dark screen, phosphor text, a graticule on every rule, the HP bar a meter, "
                   "the level a register",
              box={1: PHOS, 6: PHOS_SH, 15: SCREEN, 9: (64, 96, 96), 10: TEAL, 11: (96, 168, 152),
                   12: LEAN_PLACEHOLDER, 13: (12, 16, 20), 14: (64, 76, 92)},
              hb={1: PHOS, 2: SCREEN, 3: PHOS_SH, 4: (96, 168, 152), 5: (112, 128, 144), 6: (64, 76, 92),
                  7: (12, 16, 20), 8: (40, 48, 60), 9: TEAL, 10: (248, 144, 160), 11: (104, 200, 248)},
              bar={1: (16, 20, 24), 2: (40, 64, 64), 3: (96, 168, 152), 4: (112, 120, 128), 5: (28, 40, 44),
                   6: (12, 16, 20), 7: PHOS, 8: TEAL},
              banner={1: PHOS, 2: (12, 16, 20), 3: (12, 16, 20), 4: (64, 76, 92), 5: SCREEN, 6: (96, 168, 152),
                      7: TEAL, 8: (40, 48, 60), 9: (28, 40, 44)}),
}


def pal_of(base, over):
    p = list(base)
    for k, v in over.items():
        p[k] = v
    return [q5(c) for c in p]


def box_pal(d=None):
    base = jasc(os.path.join(BI, "textbox1.pal"))
    return pal_of(base, DIRS[d]["box"] if d else {})


def hb_pal(d=None):
    base = jasc(os.path.join(BI, "healthbox.pal"))
    return pal_of(base, DIRS[d]["hb"] if d else {})


def bar_pal(d=None):
    base = jasc(os.path.join(BI, "healthbar.pal"))
    return pal_of(base, DIRS[d]["bar"] if d else {})


def banner_pal(d=None):
    base = load_png(os.path.join(BI, "level_up_banner.png"))[3]
    base = (list(base) + [(0, 0, 0)] * 16)[:16]
    return pal_of(base, DIRS[d]["banner"] if d else {})


# ======================================================================================= the message box (textbox)
TB_W = 16                                  # textbox.png is 16 tiles wide
RING = {  # tile id: (x, y) of its 8x8 in the 240x48 box the map lays (no flips)
    0x03: (0, 0), 0x04: (8, 0), 0x05: (16, 0), 0x06: (224, 0), 0x07: (232, 0),
    0x08: (0, 8), 0x09: (8, 8), 0x0a: (16, 8), 0x0b: (224, 8), 0x0c: (232, 8),
    0x0d: (0, 40), 0x0e: (8, 40), 0x0f: (16, 40), 0x10: (224, 40), 0x11: (232, 40)}


def tb_tilemap():
    b = open(os.path.join(BI, "textbox.bin"), "rb").read()
    return struct.unpack("<%dH" % (len(b) // 2), b)


def msgbox(d):
    """The 240x48 box as the map lays it: an 8px ring round the window, the window itself the fill (15)."""
    g = [[15] * 240 for _ in range(48)]
    cut = 2
    for y in range(48):
        for x in range(240):
            xx, yy = min(x, 239 - x), min(y, 47 - y)
            dd = min(xx, yy, xx + yy - cut)
            if dd >= 8:
                continue
            if d == "1":
                ring = [0, 13, 14, 14, 11, 13, 15, 15]
            else:
                ring = [13, 14, 14, 11, 14, 13, 15, 15]
            g[y][x] = 0 if dd < 0 else ring[dd]
            if d == "1" and dd == 2 and xx < 8 and yy < 8:
                g[y][x] = BRACKET                 # the corner bracket, on the rule
            if d == "2":
                if dd in (1, 2) and xx <= 7 and yy <= 7:
                    g[y][x] = BRACKET             # the bracket, fuller on an instrument
                elif dd == 1 and ((yy < 8 and xx >= 8 and x % 8 == 4) or (xx < 8 and yy >= 8 and y % 8 == 4)):
                    g[y][x] = 11                  # the graticule: a tick every 8px
    if d == "2":
        # the prompt, on the foot's left: a '>' cut into the rule (tile 0e, x 8-15, unique)
        for x, y in ((9, 45), (10, 44), (11, 45)):
            pass
        for x, y in ((10, 43), (11, 44), (10, 45)):
            g[y][x] = BRACKET
    return g


def vanilla_msgbox():
    w, h, bd, pal, px = load_png(os.path.join(BI, "textbox.png"))
    g = [[15] * 240 for _ in range(48)]
    for t, (x0, y0) in RING.items():
        tx, ty = (t % TB_W) * 8, (t // TB_W) * 8
        xs = [x0] if t not in (0x05, 0x0a, 0x0f) else range(16, 224, 8)
        ys = [y0] if t not in (0x08, 0x09, 0x0a, 0x0b, 0x0c) else range(8, 40, 8)
        for X in xs:
            for Y in ys:
                for y in range(8):
                    for x in range(8):
                        g[Y + y][X + x] = px[ty + y][tx + x]
    return g


def textbox_png(d):
    """textbox.png with tiles 03-11 redrawn from the box; every other tile byte for byte."""
    w, h, bd, pal, px = load_png(os.path.join(BI, "textbox.png"))
    g = msgbox(d)
    for t, (x0, y0) in RING.items():
        tx, ty = (t % TB_W) * 8, (t // TB_W) * 8
        for y in range(8):
            for x in range(8):
                px[ty + y][tx + x] = g[y0 + y][x0 + x]
    return px


def check_msgbox(g):
    """The map repeats 05/0f along x and 08/0c along y: the drawing must agree with itself where it repeats."""
    bad = []
    for X in range(24, 224, 8):
        for y in list(range(0, 8)) + list(range(40, 48)):
            for x in range(8):
                if g[y][X + x] != g[y][16 + x]:
                    bad.append("x%d y%d" % (X + x, y))
    for Y in range(16, 40, 8):
        for y in range(8):
            for x in list(range(0, 8)) + list(range(232, 240)):
                if g[Y + y][x] != g[8 + y][x]:
                    bad.append("x%d y%d" % (x, Y + y))
    return bad


# ===================================================================================================== healthboxes
# name: (png tiles a row, tiles a sprite, sprite w tiles, sprite h tiles, the box's centre on screen in a single battle;
# the sprite's corner is centre - (32, 16) even at 64x64, as the shape is changed after CreateSprite set the vector), the
# tiles the code prints into (first, count), the tiles it overwrites whole, and where the HP bar sprite lies (its ")" cap
# is in the box's own art, x+64)
BOXES = {
    "healthbox_singles_player":   dict(tw=16, per=64, w=8, h=8, at=(158, 88), side="player",
                                       text=[(2, 6), (64, 1), (65, 3), (23, 1), (80, 2), (82, 2)],
                                       full=[26, 27, 28, 36, 37, 38, 39, 96, 97, 98, 99], bar=(32, 16)),
    "healthbox_singles_opponent": dict(tw=16, per=32, w=8, h=4, at=(44, 30), side="opponent",
                                       text=[(1, 7), (32, 3)], full=[17, 18, 19], bar=(24, 16)),
    "healthbox_doubles_player":   dict(tw=16, per=32, w=8, h=4, at=(159, 75), side="player",
                                       text=[(2, 6), (32, 1), (33, 3)], full=[18, 19, 20, 52], bar=(32, 16)),
    "healthbox_doubles_opponent": dict(tw=16, per=32, w=8, h=4, at=(44, 19), side="opponent",
                                       text=[(1, 7), (32, 3)], full=[17, 18, 19], bar=(24, 16)),
    "healthbox_safari":           dict(tw=8, per=64, w=8, h=8, at=(158, 88), side="player",
                                       text=[], full=[], bar=None, recolour_only=True),
}
FRAME_SLOTS = {0, 4, 5, 6, 7, 8}


def tile_xy(B, s):
    part, loc = divmod(s, B["per"])
    return part * 64 + (loc % B["w"]) * 8, (loc // B["w"]) * 8


def to_vis(px, B):
    H = B["h"] * 8
    vis = [[0] * 128 for _ in range(H)]
    n = (len(px[0]) // 8) * (len(px) // 8)
    for i in range(min(n, 2 * B["per"])):
        sx, sy = (i % B["tw"]) * 8, (i // B["tw"]) * 8
        dx, dy = tile_xy(B, i)
        for y in range(8):
            vis[dy + y][dx:dx + 8] = px[sy + y][sx:sx + 8]
    return vis


def from_vis(vis, B, px):
    px = copy(px)
    n = (len(px[0]) // 8) * (len(px) // 8)
    for i in range(min(n, 2 * B["per"])):
        sx, sy = (i % B["tw"]) * 8, (i // B["tw"]) * 8
        dx, dy = tile_xy(B, i)
        for y in range(8):
            px[sy + y][sx:sx + 8] = vis[dy + y][dx:dx + 8]
    return px


def protected(B):
    """Every pixel the code writes over at run time (text rows 5-7 and the tile row under them, whole status and EXP
    tiles), and the HP bar sprite's 64x8 over the box."""
    P = set()
    for t, n in B["text"]:
        for k in range(n):
            x0, y0 = tile_xy(B, t + k)
            for y in range(5, 8):
                for x in range(8):
                    P.add((x0 + x, y0 + y))
            x0, y0 = tile_xy(B, t + k + 8)
            for y in range(8):
                for x in range(8):
                    P.add((x0 + x, y0 + y))
    for t in B["full"]:
        x0, y0 = tile_xy(B, t)
        for y in range(8):
            for x in range(8):
                P.add((x0 + x, y0 + y))
    if B.get("bar"):
        bx, by = B["bar"]
        for y in range(by, by + 8):
            for x in range(bx, bx + 64):
                P.add((x, y))
    return P


def redraw_box(name, d):
    """The box's own shape -- it already has the family's 45-degree tail -- with its frame redrawn: the bracket at the
    plate's top-left in the trim (9), and on the readout a graticule along the top rule, the meter's quarter marks
    under the HP bar and the level's register (a rule over it and a tick after it). Only pixels outside the run-time
    tiles move, so every word still lands on the plate (2)."""
    B = BOXES[name]
    w, h, bd, pal, px = load_png(os.path.join(BI, name + ".png"))
    vis = to_vis(px, B)
    if B.get("recolour_only"):
        return vis
    P = protected(B)
    H = len(vis)
    free = lambda x, y: 0 <= x < 128 and 0 <= y < H and (x, y) not in P and vis[y][x] != 0
    out = copy(vis)
    # the plate's top-left: the first row of 2s and where it starts
    py0 = min(y for y in range(H) if 2 in vis[y])
    px0 = vis[py0].index(2)
    px1 = len(vis[py0]) - 1 - vis[py0][::-1].index(2)
    # the bracket: an L on the bevel and the band, round the plate's corner
    for k in range(6):
        for X, Y in ((px0 - 1 + k, py0 - 1), (px0 - 2, py0 + k)):
            if free(X, Y):
                out[Y][X] = 9
    if d == "2":
        for X in range(px0 + 8, px1, 8):                  # the graticule on the outline
            if free(X, py0 - 2):
                out[py0 - 2][X] = 4
        if B.get("bar"):                                  # the meter: a mark at 0, 1/4, 1/2, 3/4 and full
            bx, by = B["bar"]
            for q in range(5):
                X = min(bx + 16 + 12 * q, bx + 63)
                for Y in (by + 8, by + 9):
                    if free(X, Y) and vis[Y][X] == 2:
                        out[Y][X] = 4 if Y == by + 8 else 5
        lv = [t for t, n in B["text"] if n == 3]
        if lv:                                            # the register: a rule over the level, a tick after it
            x0, y0 = tile_xy(B, lv[0])
            for X in range(x0, x0 + 24):
                if free(X, py0 - 1):
                    out[py0 - 1][X] = 9
            for Y in range(py0 + 1, py0 + 10):
                if free(x0 + 24, Y) and vis[Y][x0 + 24] == 2:
                    out[Y][x0 + 24] = 4
    return out


def healthbox_png(name, d):
    B = BOXES[name]
    w, h, bd, pal, px = load_png(os.path.join(BI, name + ".png"))
    return from_vis(redraw_box(name, d) if d else to_vis(px, B), B, px)


# ============================================================================================ the HP and EXP bars
_ELEM = None


def elements():
    global _ELEM
    if _ELEM is None:
        _ELEM = load_png(os.path.join(BI, "healthbox_elements.png"))
    return _ELEM


def elem_tile(t, px=None):
    w, h, bd, pal, epx = elements()
    px = px or epx
    per = w // 8
    return [[v & 15 for v in row[(t % per) * 8:(t % per) * 8 + 8]] for row in px[(t // per) * 8:(t // per) * 8 + 8]]


def hp_bar(frac):
    """The 64x8 the HP bar sprite and its tiles show: "HP" (tiles 1-2) and six bar tiles, green, yellow or red by
    what is filled, exactly as MoveBattleBarGraphically picks them."""
    filled = int(48 * frac)                    # CalcBarFilledPixels floors, and > 50% / > 20% of 48 pick the set
    base = 3 if filled > 24 else (47 if filled > 9 else 56)
    tiles = [elem_tile(1), elem_tile(2)]
    for i in range(6):
        n = max(0, min(8, filled - 8 * i))
        tiles.append(elem_tile(base + n))
    return [sum((t[y] for t in tiles), []) for y in range(8)]


def exp_bar(frac):
    filled = int(round(64 * frac))
    return [sum((elem_tile(12 + max(0, min(8, filled - 8 * i)))[y] for i in range(8)), []) for y in range(8)]


# ================================================================================================ the party row
def markers(d):
    """Tiles 66-69 (healthbar.pal: whole, empty, in a state, down) and 70 (the CAUGHT marker, healthbar.pal too): a USERBOX
    seen from the front, its top-right corner cut at 45 degrees, the screen showing the state. Same slot roles as the
    USERBOXes they replace (5 the case, 3 the lit screen, 1 a line on it, 6 a state, 4 a dark screen)."""
    def box(screen, line):
        g = [[0] * 8 for _ in range(8)]
        for y in range(1, 7):
            for x in range(1, 7):
                if y in (1, 6) or x in (1, 6):
                    g[y][x] = 5
        g[1][6] = 0
        g[2][6] = 5
        g[1][5] = 5
        for y in range(2, 6):
            for x in range(2, 6):
                g[y][x] = screen
        if line:
            g[3][3], g[3][4] = line, 0 if screen == 0 else screen
            g[4][2], g[4][3], g[4][4] = line, line, line
            g[3][2] = line
        g[7][2], g[7][5] = 5, 5
        g[2][6] = 0 if False else g[2][6]
        return g
    whole = box(3, 1)
    whole[3][2], whole[3][3], whole[3][4] = 3, 3, 3
    whole[4][2], whole[4][3] = 1, 3          # a prompt: '>' and its line
    whole[3][2] = 1
    whole[5][2] = 1
    whole[4][3], whole[4][4] = 3, 1
    empty = box(0, 0)
    state = box(6, 0)
    state[3][3], state[3][4], state[4][3], state[4][4] = 3, 3, 3, 3   # a lit pixel block: the state's flag
    down = box(4, 0)
    for x in range(2, 6):
        down[4][x] = 1                        # flat: a line across a dark screen
    # 70: the USERBOX the daemon was caught into. It is copied into the HP BAR's sprite (battle_interface.c,
    # B_INTERFACE_GFX_BALL_CAUGHT -> healthBarSpriteId's tile 8), so it wears healthbar.pal, not healthbox.pal (the
    # draft assumed the latter, and the built screen lit its LED in slot 9's red -- found filming T-524): 7 the outline,
    # 5 the case, 2 the screen, 8 the LED (the trim's teal), 4 a grey key
    caught = [[0] * 8 for _ in range(8)]
    for y in range(1, 8):
        for x in range(0, 7):
            if y in (1, 7) or x in (0, 6):
                caught[y][x] = 7
            else:
                caught[y][x] = 5
    caught[1][6] = 0
    caught[2][6] = 7
    caught[1][5] = 7
    for y in range(2, 5):
        for x in range(1, 5):
            caught[y][x] = 2
    caught[6][4] = 8
    caught[6][2] = 4
    return [whole, empty, state, down], caught


def elements_png():
    """healthbox_elements.png with tiles 66-70 replaced; every other tile -- the HP and EXP bars, the status words,
    THRASHING's marks -- byte for byte."""
    w, h, bd, pal, px = elements()
    px = copy(px)
    four, caught = markers(None)
    per = w // 8
    for t, g in zip((66, 67, 68, 69, 70), four + [caught]):
        x0, y0 = (t % per) * 8, (t // per) * 8
        for y in range(8):
            px[y0 + y][x0:x0 + 8] = g[y]
    return px


def summary_bar(d):
    """party_summary_bar.png: a 64x16 sprite (two rows of 8 tiles) -- the rule the six markers sit on, rising at its
    end; and below it the fading tail. Slots 5-8 as before."""
    g = [[0] * 64 for _ in range(16)]
    # the rule: 2px, an outline (7) over a band (6), its end cut up at 45 degrees
    for x in range(0, 64):
        g[2][x] = 6
        g[3][x] = 7
    for k in range(3):
        g[2 - k][k] = 0
    for x, y in ((0, 3), (1, 2), (2, 1), (3, 0)):
        g[y][x] = 7
    g[1][3], g[0][4] = 6, 6
    if d == "2":
        for x in range(8, 64, 10):            # a tick under each marker's place (the markers are 10px apart)
            g[1][x] = 5
            g[2][x] = 8
    else:
        g[1][4], g[1][5] = 8, 8               # the bracket's foot
    # the tail: the rule fading out in steps of the family's slate
    for x in range(0, 40):
        c = 8 if x < 8 else (6 if x < 24 else 5)
        if x >= 8 and x % 2 == (1 if x < 24 else 0):
            c = {6: 8, 5: 6}[c]
        g[10][x] = c
        g[11][x] = c if x % 4 else 7 if x < 8 else c
    out = [[0] * 128 for _ in range(8)]
    for y in range(8):
        out[y][0:64] = g[y]
        out[y][64:128] = g[8 + y]
    return out


def summary_bar_vis(px):
    return [px[y][0:64] for y in range(8)] + [px[y][64:128] for y in range(8)]


# =========================================================================================== the level-up banner
def banner(d):
    """The 96x24 window (12x3 tiles): the daemon's icon on x 0-31, its name at (32, 0) and its level at (32, 10) in
    the small font, white (1) shadowed (2) on whatever is drawn -- so the ground under the words stays dark."""
    g = [[0] * 96 for _ in range(24)]
    cut = 4
    for y in range(24):
        for x in range(96):
            yy = min(y, 23 - y)
            dd = min(x, yy, x + yy - cut)          # the left end cut at 45 degrees; the right runs off the screen
            if dd < 0:
                continue
            if dd == 0:
                v = 3                              # the outline
            elif dd == 1:
                v = 6 if y < 12 else 4             # the rule: lit above, slate below
            elif y < 12:
                v = 4 if d == "1" else 5
            else:
                v = 5 if d == "1" else 9
            g[y][x] = v
    # the bracket in the trim (7) at the cut
    for k in range(6):
        for X, Y in ((5 + k, 2), (2, 5 + k)):
            if g[Y][X]:
                g[Y][X] = 7
    if d == "2":
        for x in range(36, 96, 8):                 # the graticule along the foot
            g[22][x] = 6
        for y in (11, 12):                         # the register line between name and level
            for x in range(32, 94, 2):
                g[y][x] = 8
    else:
        for x in range(4, 96):
            g[12][x] = 8 if g[12][x] else 0        # a hairline between name and level
    return g


def banner_png(d):
    w, h, bd, pal, px = load_png(os.path.join(BI, "level_up_banner.png"))
    px = copy(px)
    g = banner(d)
    per = w // 8
    for t in range(36):
        sx, sy = (t % per) * 8, (t // per) * 8
        dx, dy = (t % 12) * 8, (t // 12) * 8
        for y in range(8):
            px[sy + y][sx:sx + 8] = g[dy + y][dx:dx + 8]
    return px


def banner_vis(px):
    per = len(px[0]) // 8
    g = [[0] * 96 for _ in range(24)]
    for t in range(36):
        sx, sy = (t % per) * 8, (t // per) * 8
        dx, dy = (t % 12) * 8, (t // 12) * 8
        for y in range(8):
            g[dy + y][dx:dx + 8] = px[sy + y][sx:sx + 8]
    return g


# ===================================================================================================== the fonts
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
    """A string as glyph ids: {LV} is the small font's extra symbol 0x105."""
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


def print_idx(g, x, y, s, ink, shadow, small=False, clip=None):
    """Print into an index map, as the text printer does: the font's 1 the ink, 2 the shadow."""
    sheet, w, cm, cw, per = font(small)
    fp = sheet.load()
    for gid in glyphs(s):
        gx, gy = (gid % per) * cw, (gid // per) * 16
        for yy in range(16):
            for xx in range(min(cw, w[gid] if gid < len(w) else cw)):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, y + yy
                if 0 <= Y < len(g) and 0 <= X < len(g[0]) and (clip is None or (X, Y) in clip):
                    if v == 1:
                        g[Y][X] = ink
                    elif v == 2:
                        g[Y][X] = shadow
        x += w[gid] if gid < len(w) else cw
    return x


def print_rgb(im, x, y, s, ink, shadow, small=False):
    sheet, w, cm, cw, per = font(small)
    fp, px = sheet.load(), im.load()
    for gid in glyphs(s):
        gx, gy = (gid % per) * cw, (gid // per) * 16
        for yy in range(16):
            for xx in range(min(cw, w[gid])):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, y + yy
                if 0 <= X < im.width and 0 <= Y < im.height:
                    if v == 1:
                        px[X, Y] = ink
                    elif v == 2:
                        px[X, Y] = shadow
        x += w[gid]
    return x


# =========================================================================================== the box, filled in
def filled_box(name, d, nick, level, hp, maxhp, gender, exp=0.6):
    """A healthbox as it stands mid-battle, as an RGB image: the plate, the code's text in the small font on slot 2,
    the HP bar sprite and the EXP bar laid over."""
    B = BOXES[name]
    w, h, bd, pal, px = load_png(os.path.join(BI, name + ".png"))
    vis = redraw_box(name, d) if d else to_vis(px, B)
    vis = copy(vis)
    clip = protected(B)
    # the text windows: their rows filled with 2, then the words
    for t, n in B["text"]:
        for k in range(n):
            for tt, rows in ((t + k, range(5, 8)), (t + k + 8, range(8))):
                x0, y0 = tile_xy(B, tt)
                for y in rows:
                    for x in range(8):
                        vis[y0 + y][x0 + x] = 2
    x0, y0 = tile_xy(B, B["text"][0][0])
    end = print_idx(vis, x0, y0 + 3, nick, 1, 3, small=True, clip=clip)
    if gender:
        print_idx(vis, end, y0 + 3, gender, 11 if gender == "♂" else 10, 3, small=True, clip=clip)
    lv = [t for t, n in B["text"] if n == 3][0]
    lx, ly = tile_xy(B, lv)
    digits = str(level)
    print_idx(vis, lx + 5 * (3 - len(digits)), ly + 3, "{LV}" + digits, 1, 3, small=True, clip=clip)
    if name == "healthbox_singles_player":
        cx, cy = tile_xy(B, 23)
        print_idx(vis, cx + 4, cy + 5, "%3d/" % hp, 1, 3, small=True, clip=clip)
        mx, my = tile_xy(B, 82)
        print_idx(vis, mx, my + 5, "%3d" % maxhp, 1, 3, small=True, clip=clip)
        eb = exp_bar(exp)
        for i in range(8):
            ex, ey = tile_xy(B, (36 + i) if i < 4 else (96 + i - 4))
            for y in range(8):
                for x in range(8):
                    vis[ey + y][ex + x] = eb[y][i * 8 + x]
    for t in B["full"]:
        if t in (26, 17, 18, 19, 27, 28):
            x0, y0 = tile_xy(B, t)
            st = elem_tile(39)
            for y in range(8):
                vis[y0 + y][x0:x0 + 8] = st[y]
    hp_p, bar_p = hb_pal(d), bar_pal(d)
    im = Image.new("RGBA", (128, len(vis)), (0, 0, 0, 0))
    ip = im.load()
    for y in range(len(vis)):
        for x in range(128):
            if vis[y][x]:
                ip[x, y] = hp_p[vis[y][x]] + (255,)
    if B.get("bar"):
        bx, by = B["bar"]
        hb = hp_bar(hp / maxhp)
        for y in range(8):
            for x in range(64):
                if hb[y][x]:
                    ip[bx + x, by + y] = bar_p[hb[y][x]] + (255,)
    return im


def idx_rgba(g, pal):
    im = Image.new("RGBA", (len(g[0]), len(g)), (0, 0, 0, 0))
    p = im.load()
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x]:
                p[x, y] = pal[g[y][x]] + (255,)
    return im


def on(im, bg=(40, 44, 52)):
    box = im.getbbox()
    if box:                                    # the sprite's empty rows are not the box
        im = im.crop((0, 0, im.width, min(im.height, box[3] + 1)))
    o = Image.new("RGB", im.size, bg)
    o.paste(im, (0, 0), im)
    return o


# ===================================================================================================== the mock
def terrain():
    try:
        spec = importlib.util.spec_from_file_location("gbabattlebg", os.path.join(ROOT, "tools", "gbabattlebg.py"))
        argv, sys.argv = sys.argv, sys.argv[:1]
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        sys.argv = argv
        for num, name, png, binp, pal in m.engine_terrains():
            if name == "GRASS":
                T = m.terrain_of(name, png, binp, pal)
                return T.render(T.pal, accent=False)
    except Exception as e:                       # a mock is advice; a plain ground will do
        print("  (terrain: %s; a plain ground instead)" % e.__class__.__name__)
    return Image.new("RGB", (240, 112), (120, 168, 120))


def mon(species, which):
    d = os.path.join(GBA, "graphics/pokemon", species)
    w, h, bd, p, px = load_png(os.path.join(d, which + ".png"))
    pal = [q5(c) for c in jasc(os.path.join(d, "normal.pal"))]
    return idx_rgba(px, pal)


SAY = "DRAFT: LABEL is waiting on you."                 # vanilla's battle words are not changed; this line is a DRAFT
SAY2 = "What will LABEL do?"


def mock(d, ground):
    """240x160 as a single battle stands at "What will X do?": the terrain, PACKET (front) and LABEL (back), both
    boxes, the message box (left half the prompt) and the action menu in the default OPTIONS frame (TERMINAL)."""
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    im.paste(ground, (0, 0))
    f = mon("pidgey", "front")
    im.paste(f, (176 - 32, 40 - 32 + 10), f)
    b = mon("charmander", "back")
    im.paste(b, (72 - 32, 80 - 32 + 10), b)
    for name, nick, lv, hp, mx, g in (("healthbox_singles_opponent", "PACKET", 4, 9, 15, "♀"),
                                      ("healthbox_singles_player", "LABEL", 6, 17, 22, "♂")):
        B = BOXES[name]
        bx = filled_box(name, d, nick, lv, hp, mx, g)
        cx, cy = B["at"]
        im.paste(bx, (cx - 32, cy - 16), bx)      # the 64x32 template's corner vector, kept when 64x64
    # the bottom: the message box map, palette 0, its left 15 tiles (the prompt) and the menu frame at col 15
    g = msgbox(d) if d else vanilla_msgbox()
    pal = box_pal(d)
    p = im.load()
    for y in range(48):
        for x in range(120):
            if g[y][x]:
                p[x, 112 + y] = pal[g[y][x]]
            if x >= 8 and 120 <= 112 + y < 152:
                p[x, 112 + y] = pal[15]
    print_rgb(im, 8 + 2, 120 + 1, "What will", pal[1], pal[6])
    print_rgb(im, 8 + 2, 120 + 17, "LABEL do?", pal[1], pal[6])
    # the action menu: the OPTIONS frame 1 as T-523 built it (type1.png), palette 5 text as battle_bg.c sets it
    fr = load_png(os.path.join(GBA, "graphics/text_window/type1.png"))
    fpal = [q5(c) for c in fr[3]]
    fpx = fr[4]
    for ty in range(6):
        for tx in range(15):
            sx = 0 if tx == 0 else (2 if tx == 14 else 1)
            sy = 0 if ty == 0 else (2 if ty == 5 else 1)
            for y in range(8):
                for x in range(8):
                    v = fpx[sy * 8 + y][sx * 8 + x]
                    X, Y = 120 + tx * 8 + x, 112 + ty * 8 + y
                    if 0 < tx < 14 and 0 < ty < 5:
                        p[X, Y] = (248, 248, 248)
                    elif v:
                        p[X, Y] = fpal[v]
    grey, white, sh = (72, 72, 72), (248, 248, 248), (208, 208, 200)
    for (tx, ty, s) in ((136 + 8, 120 + 1, "ROUTINES"), (136 + 8 + 56, 120 + 1, "POOL"),
                        (136 + 8, 120 + 17, "DAEMON"), (136 + 8 + 56, 120 + 17, "DETACH")):
        print_rgb(im, tx, ty, s, grey, sh)
    # the cursor
    print_rgb(im, 136, 120 + 1, "▶", grey, sh)
    return im


def mock_message(d, ground):
    """The same screen while the box speaks: the whole message box with a DRAFT line, two lines at most 208px."""
    im = mock(d, ground)
    g = msgbox(d) if d else vanilla_msgbox()
    pal = box_pal(d)
    p = im.load()
    for y in range(48):
        for x in range(240):
            if g[y][x]:
                p[x, 112 + y] = pal[g[y][x]]
            else:
                p[x, 112 + y] = ground.getpixel((x, 111))
            if 8 <= x < 232 and 120 <= 112 + y < 152:
                p[x, 112 + y] = pal[15]
    print_rgb(im, 8 + 2, 120 + 1, "DRAFT: PACKET used SCRATCH.", pal[1], pal[6])
    print_rgb(im, 8 + 2, 120 + 17, "It's super effective!", pal[1], pal[6])
    return im


# =========================================================================================================== report
def report():
    print("T-524 battle UI -- the engine's files (%s):" % BI)
    for n in ["textbox", "healthbox_singles_player", "healthbox_singles_opponent", "healthbox_doubles_player",
              "healthbox_doubles_opponent", "healthbox_safari", "level_up_banner", "party_summary_bar",
              "healthbox_elements", "enemy_mon_shadow"]:
        w, h, bd, pal, px = load_png(os.path.join(BI, n + ".png"))
        used = sorted({v for r in px for v in r})
        print("  %-28s %3dx%-3d %3d tiles, slots drawn %s" % (n + ".png", w, h, w * h // 64, used))
    m = tb_tilemap()
    p1 = sorted({e & 0x3FF for e in m if e >> 12 == 1 and e & 0x3FF})
    print("\n  textbox.bin: palette-1 tiles %s are LoadUserWindowGfx's at run time (the OPTIONS frame), so the action"
          "\n  and move menus already wear T-523's family; palette-0 tiles 03-11 are the message box drawn here."
          % ", ".join("%02x" % t for t in p1))
    for k, D in DIRS.items():
        bad = check_msgbox(msgbox(k))
        print("  direction %s %-17s message box repeats agree: %s" % (k, D["name"], "yes" if not bad else bad[:4]))
        lean = sum(r.count(LEAN_SLOT) for r in textbox_png(k))
        print("  direction %s %-17s textbox.png pixels in slot %d (the lean's, loaded at run time): %d%s"
              % (k, D["name"], LEAN_SLOT, lean, "" if not lean else "  ! must be 0"))
        for name in BOXES:
            B = BOXES[name]
            if B.get("recolour_only"):
                continue
            w, h, bd, pal, px = load_png(os.path.join(BI, name + ".png"))
            v0, v1 = to_vis(px, B), redraw_box(name, k)
            P = protected(B)
            moved = sum(1 for y in range(len(v0)) for x in range(128) if v0[y][x] != v1[y][x])
            broke = [(x, y) for (x, y) in P if y < len(v0) and v0[y][x] != v1[y][x]]
            plate = sum(1 for y in range(len(v0)) for x in range(128) if v0[y][x] == 2 and v1[y][x] != 2)
            print("     %-28s %3d px redrawn, %d in a run-time tile (must be 0), %d marks on the plate clear of every"
                  " word" % (name, moved, len(broke), plate))
    print("\n  words measured (208px allowed in the box): %dpx %r, %dpx %r" %
          (text_width("DRAFT: PACKET used SCRATCH."), "DRAFT: PACKET used SCRATCH.",
           text_width("It's super effective!"), "It's super effective!"))


# =========================================================================================================== draft
def draft(out):
    os.makedirs(out, exist_ok=True)
    w, h, bd, epal, epx = elements()
    for k in DIRS:
        d = os.path.join(out, k)
        os.makedirs(d, exist_ok=True)
        save_png(os.path.join(d, "textbox.png"), textbox_png(k), box_pal(k))
        tp = jasc(os.path.join(BI, "textbox1.pal"))
        for s, c in DIRS[k]["box"].items():
            tp[s] = c
        write_jasc(tp, os.path.join(d, "textbox1.pal"))
        for name in BOXES:
            save_png(os.path.join(d, name + ".png"), healthbox_png(name, k), hb_pal(k))
        hp = jasc(os.path.join(BI, "healthbox.pal"))
        for s, c in DIRS[k]["hb"].items():
            hp[s] = c
        write_jasc(hp, os.path.join(d, "healthbox.pal"))
        bp = jasc(os.path.join(BI, "healthbar.pal"))
        for s, c in DIRS[k]["bar"].items():
            bp[s] = c
        write_jasc(bp, os.path.join(d, "healthbar.pal"))
        save_png(os.path.join(d, "level_up_banner.png"), banner_png(k), banner_pal(k))
        save_png(os.path.join(d, "party_summary_bar.png"), summary_bar(k), hb_pal(k))
    save_png(os.path.join(out, "healthbox_elements.png"), elements_png(), epal, bd)
    sheet(out)


def label_font(n=12):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except Exception:
        return ImageFont.load_default()


def sheet(out):
    F, FB = label_font(12), label_font(14)
    W = 1560
    parts = []
    ground = terrain()

    def strip(title, height):
        im = Image.new("RGB", (W, height), (32, 34, 40))
        dr = ImageDraw.Draw(im)
        dr.text((12, 6), title, fill=(240, 220, 160), font=F)
        return im, dr

    hdr = Image.new("RGB", (W, 64), (24, 26, 30))
    dr = ImageDraw.Draw(hdr)
    dr.text((12, 8), "T-524 DRAFT -- the battle UI in the TERMINAL family (T-523), drawn by hand in code (no AI image). "
                     "Same tiles, sizes and palette slots as the engine's; every run-time text zone left as it was.",
            fill=(230, 230, 230), font=F)
    dr.text((12, 28), "1 TERMINAL plain: slate on paper, as the field's box.   2 TERMINAL readout (recommended): a dark "
                      "screen, phosphor text, a graticule, the HP bar a meter, the level a register.",
            fill=(170, 170, 170), font=F)
    dr.text((12, 44), "The action and move menus are the OPTIONS frame at run time (already T-523's), so they are shown, "
                      "not redrawn. Words are vanilla's/DAEMONS's own; the one new line is marked DRAFT.",
            fill=(170, 170, 170), font=F)
    parts.append(hdr)
    # 1. the mocks at real size, then at 2x
    mk, dr = strip("AT REAL SIZE, 240x160 -- the engine now, 1, 2. Top: \"What will LABEL do?\" with the action menu. "
                   "Below: the box speaking (a DRAFT line). LABEL is CHARMANDER's back, PACKET is PIDGEY's front.", 380)
    for i, k in enumerate([None, "1", "2"]):
        a, b = mock(k, ground), mock_message(k, ground)
        a.save(os.path.join(out, "mock_%s.png" % (k or "engine")))
        b.save(os.path.join(out, "mock_message_%s.png" % (k or "engine")))
        x = 12 + i * 260
        dr.text((x, 22), ["THE ENGINE NOW", "1 TERMINAL plain", "2 TERMINAL readout"][i], fill=(200, 200, 200), font=F)
        mk.paste(a, (x, 40))
        mk.paste(b, (x, 210))
    dr.text((800, 40), "Run-time slots kept:", fill=(240, 220, 160), font=F)
    notes = ["BG 0: 1 ink, 6 shadow, 15 fill (the box's text)",
             "healthbox: 2 the plate under every word, 1/3 ink and shadow,",
             "  10/11 the gender marks (11 is also the EXP fill),",
             "  12-15 written per battler with the status colour",
             "healthbar: 10-15 green/yellow/red exact (the code picks tiles)",
             "level-up banner: 1/2 its text, 12-15 the gender marks",
             "BG 5 (menus) and BG 1 (the OPTIONS frame): untouched",
             "Nothing tints these at run time but HALFTONE (grey):",
             "  both directions keep light-on-dark / dark-on-light."]
    for j, s in enumerate(notes):
        dr.text((800, 60 + j * 16), s, fill=(190, 190, 190), font=F)
    parts.append(mk)
    big, dr = strip("2x: the engine now, 1 and 2", 352)
    for i, k in enumerate([None, "1", "2"]):
        big.paste(mock(k, ground).resize((480, 320), Image.NEAREST), (12 + i * 500, 26))
    parts.append(big)
    # 2. each element: engine vs 1 vs 2, at 1x and 3x
    rows = [("THE MESSAGE BOX (textbox.png tiles 03-11, BG palette 0) -- the 240x48 ring the map lays",
             lambda k: on(idx_rgba(msgbox(k) if k else vanilla_msgbox(), box_pal(k)))),
            ("THE PLAYER'S BOX (healthbox_singles_player, as seen: two 64x64 sprites) -- filled as in battle",
             lambda k: on(filled_box("healthbox_singles_player", k, "LABEL", 6, 17, 22, "♂"))),
            ("THE FOE'S BOX (healthbox_singles_opponent) -- HP at a fifth: the bar goes red by tile, as the code picks",
             lambda k: on(filled_box("healthbox_singles_opponent", k, "PACKET", 4, 3, 15, "♀"))),
            ("DOUBLES (healthbox_doubles_player, _opponent) -- frames only",
             lambda k: on(hconcat(frame_only("healthbox_doubles_player", k),
                                  frame_only("healthbox_doubles_opponent", k)))),
            ("THE LEVEL-UP BANNER (level_up_banner.png as its 12x3 window, BG palette 6) -- name and level as printed",
             lambda k: on(banner_filled(k))),
            ("THE PARTY ROW (party_summary_bar + markers 66-69 whole/empty/state/down, and 70 CAUGHT on the foe's box)",
             lambda k: on(party_row(k)))]
    for title, fn in rows:
        imgs = [fn(k) for k in (None, "1", "2")]
        k3 = 3 if imgs[0].width <= 140 else 2
        # pack the three blocks (1x, then k3x) left to right, wrapping when the sheet is full
        lines, cur, x = [], [], 12
        for i, im in enumerate(imgs):
            bw = im.width * (1 + k3) + 40
            if cur and x + bw > W:
                lines.append(cur)
                cur, x = [], 12
            cur.append((i, im, x))
            x += bw
        lines.append(cur)
        lh = max(i.height for i in imgs) * k3 + 30
        r, dr = strip(title, 22 + lh * len(lines))
        for li, line in enumerate(lines):
            y0 = 22 + li * lh
            for i, im, x in line:
                dr.text((x, y0), ["engine", "1 plain", "2 readout"][i], fill=(200, 200, 200), font=F)
                r.paste(im, (x, y0 + 18))
                r.paste(im.resize((im.width * k3, im.height * k3), Image.NEAREST), (x + im.width + 8, y0 + 18))
        parts.append(r)
    H = sum(p.height for p in parts)
    sh = Image.new("RGB", (W, H), (32, 34, 40))
    y = 0
    for p in parts:
        sh.paste(p, (0, y))
        y += p.height
    path = os.path.join(out, "t524_battle_ui_sheet.png")
    sh.save(path)
    print("  sheet -> %s" % path)


def frame_only(name, d):
    B = BOXES[name]
    g = redraw_box(name, d) if d else to_vis(load_png(os.path.join(BI, name + ".png"))[4], B)
    return idx_rgba(g, hb_pal(d))


def hconcat(a, b, gap=8):
    im = Image.new("RGBA", (a.width + gap + b.width, max(a.height, b.height)), (0, 0, 0, 0))
    im.paste(a, (0, 0))
    im.paste(b, (a.width + gap, 0))
    return im


def banner_filled(d):
    if d:
        g = banner(d)
    else:
        g = banner_vis(load_png(os.path.join(BI, "level_up_banner.png"))[4])
    g = copy(g)
    print_idx(g, 32, 0, "LABEL", 1, 2, small=True)
    print_idx(g, 32, 10, "{LV}7", 1, 2, small=True)
    im = idx_rgba(g, banner_pal(d))
    icon = load_png(os.path.join(GBA, "graphics/pokemon/charmander/icon.png"))
    ipx = icon[4]
    ipal = [q5(c) for c in jasc(os.path.join(GBA, "graphics/pokemon_icon_palettes/pal0.pal"))] \
        if os.path.exists(os.path.join(GBA, "graphics/pokemon_icon_palettes/pal0.pal")) else [q5(c) for c in icon[3]]
    ic = idx_rgba([r[:32] for r in ipx[:32]], ipal)
    im.paste(ic, (0, -6), ic)
    return im


def party_row(d):
    """The bar and six markers as SpriteCB places them: the markers 10px apart from x 24, 4px above the bar's line."""
    if d:
        bar = summary_bar_vis(summary_bar(d))
        four, caught = markers(d)
    else:
        bar = summary_bar_vis(load_png(os.path.join(BI, "party_summary_bar.png"))[4])
        four = [elem_tile(t) for t in (66, 67, 68, 69)]
        caught = elem_tile(70)
    im = Image.new("RGBA", (100, 24), (0, 0, 0, 0))
    b = idx_rgba(bar, hb_pal(d))
    im.paste(b, (8, 8), b)
    order = [0, 0, 2, 0, 3, 1]
    for i, s in enumerate(order):
        m = idx_rgba(four[s], bar_pal(d))
        im.paste(m, (8 + 2 + 10 * i, 2), m)
    c = idx_rgba(caught, bar_pal(d))
    im.paste(c, (80, 2), c)
    return im


# =========================================================================================================== write
def write(main):
    d = os.path.join(DRAFT_DEFAULT, main)
    for n in ["textbox.png", "level_up_banner.png", "party_summary_bar.png"] + [b + ".png" for b in BOXES]:
        shutil.copyfile(os.path.join(d, n), os.path.join(BI, n))
    # the palettes: only the slots the direction names move; 12-15 of healthbox.pal (run time) are kept as they are
    for n, key in (("textbox1.pal", "box"), ("healthbox.pal", "hb"), ("healthbar.pal", "bar")):
        cur = jasc(os.path.join(BI, n))
        for s, c in DIRS[main][key].items():
            cur[s] = c
        write_jasc(cur, os.path.join(BI, n))
    # the elements sheet: only tiles 66-70 are this tool's; splice them into the engine's own sheet rather than copy
    # the draft's whole, so a later write never undoes another tool's tiles (genthrashicon's 36-38, the status words)
    w, h, bd, epal, epx = elements()
    save_png(os.path.join(BI, "healthbox_elements.png"), elements_png(), epal, bd)
    print("  written direction %s into %s" % (main, BI))


def main():
    if A.write and not A.approved:
        print("  --write refuses without --approved: the user picks a direction before it is written.")
        return 1
    if A.write and not A.main:
        print("  --write needs --main 1|2: the direction the user picked.")
        return 1
    report()
    if A.draft:
        draft(A.draft)
    if A.write:
        if not os.path.isdir(os.path.join(DRAFT_DEFAULT, A.main)):
            print("  no draft for %s: run --draft first" % A.main)
            return 1
        write(A.main)
    return 0


if __name__ == "__main__":
    sys.exit(main())
