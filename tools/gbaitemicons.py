#!/usr/bin/env python3
"""T-525: the item icons, drawn anew -- batch 1, the forty-one a player sees first.

    python3 tools/gbaitemicons.py                      # report: each icon in the batch, the engine file it would
                                                       #   replace, what that file is now (vanilla or ours), and the
                                                       #   palettes measured (<= 15 colours + transparent)
    python3 tools/gbaitemicons.py --draft [DIR]        # draw the batch into DIR (gfx/drafts/t525_item_icons/): one
                                                       #   24x24 PNG and JASC .pal per icon, the contact sheet, and a
                                                       #   mock of the BAG at real size (240x160)
    python3 tools/gbaitemicons.py --write --approved ITEM [ITEM ...]   # write the named items into the engine
    python3 tools/gbaitemicons.py --write --approved --all             #   (or every one); refuses without --approved

DRAFT, 2026-11-07, the user away ("Item icons" next, from the vanilla-art census, gap 4). Every pixel here is drawn in
code, by hand, on the 24x24 grid: no AI image, nothing traced. The engine's own icons are read only to show them
beside ours on the sheet.

WHAT EACH ICON DRAWS. What the DAEMONS item IS, from its DAEMONS name and its description (src/data/items.json),
never FireRed's object: RECOVER is a graduated flask filled to its first mark, PATCH a stitched patch over a crack,
WATCHDOG a stopwatch, RESUME a play key, EJECT the eject key, SITEMAP a page with one box and the boxes it branches
into (the overworld SITEMAP's drawing, T-167), ROLL CALL a handheld with a ticked list and a battery, QUERY a rod whose
line ends in a question, the PLUGIN a card with an edge connector. The table in ICONS says each one in a line.

COLOUR (vision.md 9.4: colour carries the argument and never decorates it)
  * a cure wears the colour of the STATE it ends -- the state's own tile colour in the party and battle boxes
    (tools/gbaitems.py STATES): PATCH LEAKING's green, COOLANT OVERHEATED's ember, WATCHDOG HUNG's blue, RESUME
    SUSPENDED's slate, PRIORITY THROTTLED's yellow, the four restarts HALTED's red. ROLLBACK and HOTFIX end EVERY
    state, so they wear all five.
  * anything that puts back HP is in the HP bar's green (graphics/battle_interface/healthbar.pal), and its tier is
    how full it is, not a new hue: RECOVER to the first mark, DEEP RECOVER the second, FULL RECOVER to the top.
  * the PLUGIN and the DRIVER are drawn in the slots of the engine's per-type palettes (3-9 the type's ramp,
    tools/genplugincolours.py), so each disc is still its routine's type, as the TOOLKIT teaches.
  * the TOOLKIT shows three plugin cards standing in it, in three type hues: it holds routines of every type.
  * everything else -- the bicycle, the tea, the rods -- is drawn in neutrals, because a type's hue on an untyped
    object would be a false label.
  The ink is the project's (16,16,20), as on OPUS, the NOTEBOOK and every daemon.

FORMAT. 24x24, mode "P", entry 0 transparent, at most 16 entries, the palette a JASC .pal beside the picture (CRLF, as
.gitattributes keeps JASC-PAL). The engine shares drawings between items (one potion drawing, three palettes); these
do not, because RECOVER and REBUILD are different things. So a --write gives each approved item ITS OWN files
(graphics/items/icons/d_<item>.png, icon_palettes/d_<item>.pal), adds their INCBIN lines to src/data/graphics/items.h
and externs to include/graphics.h, and repoints only that item's row in src/data/item_icon_table.h. An item not named
keeps its vanilla row untouched, so the user can approve some and not others. Two exceptions, both shared on purpose:
  PLUGIN  rewrites tm_hm.png in place (every PLUGIN row keeps its type palette; genplugincolours.py owns those palettes
          and is not touched -- this draws only in slots it does not write)
  DRIVER  adds driver.png, and the eight DRIVER rows point at it, each keeping its type palette.

GENERATORS THAT ALREADY WRITE ITEM ICONS (none of them writes a file this one does)
  gbabox.py (the five USERBOX tiers), genguide.py, gennotebookicon.py, genopusicon.py, genplayicons.py (HARP, FLUTE,
  and three table edits anchored on the GUIDE's lines), gensubtle.py (the books), gentoken.py (TOKEN),
  genplugincolours.py (slots 3-9 of the sixteen *_tm_hm.pal). This tool appends its table lines at the END of
  items.h and before graphics.h's last #endif, so it never moves an anchor theirs need.
"""
import argparse, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
ICON_DIR = os.path.join(GBA, "graphics/items/icons")
PALS = os.path.join(GBA, "graphics/items/icon_palettes")
ITEMS_H = os.path.join(GBA, "src/data/graphics/items.h")
GRAPHICS_H = os.path.join(GBA, "include/graphics.h")
TABLE = os.path.join(GBA, "src/data/item_icon_table.h")
ITEMS_JSON = os.path.join(GBA, "src/data/items.json")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t525_item_icons")
N = 24
TAG = "// T-525: DAEMONS tools/gbaitemicons.py"

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--all", action="store_true")
ap.add_argument("--over-later-work", action="store_true")    # check_generators passes it to every --write; unused
ap.add_argument("items", nargs="*")
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

#  Nothing is approved yet: the user picks from the sheet. A --write names its items itself.
APPROVED = []

# ================================================================================================= the colours
INK = (16, 16, 20)
W = (244, 242, 234)          # paper white
W2 = (214, 212, 204)
G1 = (178, 178, 184)          # greys, light to dark
G2 = (132, 134, 142)
G3 = (88, 90, 100)
G4 = (52, 54, 62)
GLASS = (210, 228, 232)
GLASS2 = (170, 196, 204)
#  the HP bar's own greens (graphics/battle_interface/healthbar.pal 7, 11, and a shade)
HP_L, HP, HP_D = (112, 248, 168), (88, 208, 128), (40, 128, 84)
#  the states' tile colours (tools/gbaitems.py STATES), each with a light and a dark step
def ramp(c, k=0.42):
    lit = tuple(min(255, int(v + (255 - v) * k)) for v in c)
    dark = tuple(int(v * (1 - k)) for v in c)
    return lit, c, dark
LEAKING = ramp((0x6f, 0x94, 0x40))
SUSPENDED = ramp((0x8a, 0x8f, 0x9c))
THROTTLED = ramp((0xc8, 0xa0, 0x20))
OVERHEATED = ramp((0xd8, 0x70, 0x3c))
HUNG = ramp((0x78, 0xa8, 0xdc))
HALTED = ramp((0xb8, 0x3c, 0x3c))
FIVE = [LEAKING[1], OVERHEATED[1], HUNG[1], SUSPENDED[1], THROTTLED[1]]
#  MP: the budget a routine spends. No type's hue: a violet blue nothing in the chart is near (CIE76 > 30 from all 18)
MP_L, MP, MP_D = (176, 186, 255), (118, 128, 236), (64, 70, 160)
WOOD_L, WOOD, WOOD_D = (214, 170, 116), (170, 120, 70), (112, 74, 40)
KRAFT_L, KRAFT, KRAFT_D = (222, 196, 150), (190, 158, 110), (138, 108, 70)


# ================================================================================================= the canvas
class C:
    """A 24x24 grid of colours (None = transparent), drawn on by hand."""
    def __init__(self):
        self.g = [[None] * N for _ in range(N)]

    def px(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < N and 0 <= y < N else None

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def box(self, x0, y0, x1, y1, c, edge=INK, round_=True):
        """A filled rectangle with a one-pixel edge; corners off when round_."""
        self.rect(x0, y0, x1, y1, edge)
        self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, c)
        if round_:
            for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                self.px(x, y, None)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        e = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * e
            if e2 >= dy:
                e += dy
                x0 += sx
            if e2 <= dx:
                e += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for y in range(N):
            for x in range(N):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + r * 0.6:
                    self.px(x, y, c)

    def ring(self, cx, cy, r0, r1, colour_at):
        """Pixels with r0 <= distance <= r1; colour_at(angle_degrees) gives each one's colour, or None to skip."""
        for y in range(N):
            for x in range(N):
                d = math.hypot(x - cx, y - cy)
                if r0 <= d <= r1:
                    a = math.degrees(math.atan2(-(y - cy), x - cx)) % 360
                    c = colour_at(a)
                    if c is not None:
                        self.px(x, y, c)

    def ascii(self, x0, y0, rows, legend):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == " ":
                    continue
                self.px(x0 + i, y0 + j, None if ch == "." else legend[ch])

    def outline(self, c=INK, diag=False):
        """Ink every empty pixel that touches a filled one (4-neighbour; 8 with diag)."""
        add = []
        nb = [(1, 0), (-1, 0), (0, 1), (0, -1)] + ([(1, 1), (1, -1), (-1, 1), (-1, -1)] if diag else [])
        for y in range(N):
            for x in range(N):
                if self.g[y][x] is None and any(self.get(x + dx, y + dy) not in (None, c) for dx, dy in nb):
                    add.append((x, y))
        for x, y in add:
            self.g[y][x] = c

    def recolour(self, frm, to, region=None):
        for y in range(N):
            for x in range(N):
                if self.g[y][x] == frm and (region is None or region(x, y)):
                    self.g[y][x] = to


def flask(level):
    """RECOVER's family: a graduated flask, filled in the HP bar's green to mark `level` of three."""
    c = C()
    c.rect(10, 3, 13, 8, GLASS)                       # the neck
    c.rect(9, 2, 14, 3, G1)                           # the lip
    c.hline(9, 14, 3, G2)
    for y in range(8, 21):                            # the body: shoulders out, then straight, rounded at the foot
        half = min(6, 2 + (y - 8) * 2) if y < 11 else 6
        if y == 20:
            half = 5
        c.hline(12 - half, 11 + half, y, GLASS)
    top = {1: 17, 2: 14, 3: 10}[level]
    for y in range(top, 21):
        for x in range(N):
            if c.get(x, y) == GLASS:
                c.px(x, y, HP)
    for x in range(N):                                # the liquid's surface catches the light
        if c.get(x, top) == HP:
            c.px(x, top, HP_L)
    for y in range(top + 1, 21):                      # and its far side is in shade
        for x in range(N - 1, -1, -1):
            if c.get(x, y) == HP:
                c.px(x, y, HP_D)
                break
    for y in (11, 14, 17):                            # the three marks, on the left of the glass
        for x in (7, 8):
            c.px(x, y, G3 if c.get(x, y) == GLASS else HP_D)
    for y in range(9, 19):                            # the glass's highlight
        if c.get(15, y) == GLASS:
            c.px(15, y, W)
    c.outline()
    return c


def i_recover():
    return flask(1)


def i_deep_recover():
    return flask(2)


def i_full_recover():
    return flask(3)


def i_rebuild():
    """From nothing: a wall of HP-green blocks built up from the ground, the last block coming down into place."""
    c = C()
    rows = [(19, [(3, 8), (10, 15), (17, 20)]), (16, [(3, 5), (7, 12), (14, 19)]), (13, [(5, 10), (12, 17)])]
    for y, bricks in rows:
        for x0, x1 in bricks:
            c.rect(x0, y - 1, x1, y + 1, HP)
            c.hline(x0, x1, y - 1, HP_L)
            c.hline(x0, x1, y + 1, HP_D)
    c.rect(8, 4, 13, 6, HP)                          # the block arriving
    c.hline(8, 13, 4, HP_L)
    c.hline(8, 13, 6, HP_D)
    c.outline()
    for x in (10, 11):                               # and the way it is going
        c.px(x, 9, W)
    c.px(9, 9, None), c.px(12, 9, None)
    return c


def i_snapshot():
    """Health and state, kept together: a print of the moment, a green bar and the five states' pips in it."""
    c = C()
    c.rect(3, 3, 20, 21, W)                         # the print's white border, wide at the foot
    c.rect(5, 5, 18, 16, G4)                        # the picture
    c.rect(6, 7, 15, 9, HP)                         # the health bar, full
    c.hline(6, 15, 7, HP_L)
    c.px(17, 8, G3)
    for i, col in enumerate(FIVE):                  # the state, every slot of it, beside it
        c.rect(6 + i * 2, 12, 6 + i * 2, 14, col)
    c.hline(3, 20, 21, W2)
    c.vline(20, 3, 21, W2)
    c.rect(15, 18, 18, 19, W2)                      # a corner written on
    c.outline()
    return c


def i_patch():
    """A patch stops a leak at its source: a square of LEAKING's green stitched down over a crack."""
    c = C()
    L, M, D = LEAKING
    c.line(2, 21, 7, 16, G3)                       # the crack it covers, showing at two corners
    c.line(21, 2, 16, 7, G3)
    c.line(20, 2, 16, 6, G3)
    c.rect(5, 5, 18, 18, M)
    c.hline(5, 18, 5, L)
    c.vline(5, 5, 18, L)
    c.hline(5, 18, 18, D)
    c.vline(18, 5, 18, D)
    for i in range(7, 17, 2):                        # the stitches, round it
        c.px(i, 7, W), c.px(i + 1, 16, W), c.px(7, i + 1, W), c.px(16, i, W)
    c.outline()
    return c


def i_coolant():
    """Draws off the heat a daemon made itself: a coolant jug, OVERHEATED's ember on the label, the arrow pointing
    down."""
    c = C()
    L, M, D = OVERHEATED
    c.rect(6, 6, 18, 21, G1)                        # the jug
    c.vline(18, 6, 21, G2)
    c.hline(6, 18, 21, G2)
    c.rect(7, 3, 10, 5, G2)                         # the cap
    c.rect(13, 4, 17, 5, G1)                        # the handle
    c.px(14, 5, None), c.px(15, 5, None), c.px(16, 5, None)
    c.rect(8, 10, 16, 18, M)                        # the label
    c.hline(8, 16, 10, L)
    c.hline(8, 16, 18, D)
    c.vline(12, 11, 15, W)                          # the temperature, down
    c.hline(10, 14, 15, W)
    c.hline(11, 13, 16, W)
    c.px(12, 17, W)
    c.outline()
    c.px(7, 7, W)
    return c


def i_watchdog():
    """A watchdog notices a process that stopped answering, and resets it: a stopwatch, its rim HUNG's blue."""
    c = C()
    L, M, D = HUNG
    c.rect(10, 1, 13, 2, G2)                        # the crown
    c.rect(11, 3, 12, 4, G3)
    c.disc(11.5, 13, 8, M)                          # the rim
    c.ring(11.5, 13, 6.5, 8.6, lambda a: L if 60 < a < 200 else (D if 240 < a < 360 else None))
    c.disc(11.5, 13, 6, W)                          # the face
    for a in range(0, 360, 90):                     # quarter marks
        x, y = 11.5 + 5 * math.cos(math.radians(a)), 13 - 5 * math.sin(math.radians(a))
        c.px(round(x), round(y), G2)
    c.vline(11, 8, 13, INK)                         # the hand, gone round to the top: time to reset
    c.px(12, 13, INK)
    c.rect(19, 5, 20, 6, G2)                        # the reset button
    c.outline()
    return c


def i_resume():
    """Puts a SUSPENDED daemon back on the schedule: a round play key, SUSPENDED's slate."""
    c = C()
    L, M, D = SUSPENDED
    c.disc(11.5, 11.5, 9, M)
    c.ring(11.5, 11.5, 7.5, 9.6, lambda a: L if 45 < a < 225 else D)
    for y in range(6, 18):                          # the triangle
        w = 6 - abs(y - 11.5)
        for x in range(9, 9 + int(round(w * 1.3)) + 1):
            c.px(x, y, W)
    c.outline()
    return c


def i_priority():
    """Scheduled ahead of whatever was starving it: a queue of three, and one in THROTTLED's yellow put at the
    front."""
    c = C()
    L, M, D = THROTTLED
    for y in (11, 15, 19):                          # the queue
        c.rect(5, y, 18, y + 1, G2)
        c.hline(5, 18, y, G1)
    c.rect(4, 6, 19, 8, M)                          # the one moved to the front
    c.hline(4, 19, 6, L)
    c.hline(4, 19, 8, D)
    c.hline(11, 12, 1, M)                           # going up
    c.hline(10, 13, 2, M)
    c.hline(9, 14, 3, M)
    c.outline()
    return c


def i_rollback():
    """Rolls back to a known-good state, and ends every state at once: an arrow turned back on itself, made of the
    five states' colours, round a tick."""
    c = C()
    def seg(a):
        if 20 < a < 70:
            return None                               # the gap the arrow turns through
        return FIVE[int(((a - 70) % 360) / 58) % 5]
    c.ring(11.5, 12, 6, 8.8, seg)
    c.ascii(13, 1, ["XXXXX", " XXXX", "  XXX", "   XX"], {"X": FIVE[4]})    # the head, pointing back (anticlockwise)
    c.ascii(7, 10, ["        ", "      WW", "     WW ", "WW  WW  ", " WWWW   ", "  WW    "], {"W": W})
    c.outline()
    return c


def i_hotfix():
    """Bitter, cheap, and it works now; clears every state: a torn paper sachet with the five states on its band."""
    c = C()
    c.rect(6, 4, 17, 21, KRAFT)
    c.vline(17, 4, 21, KRAFT_D)
    c.vline(6, 4, 21, KRAFT_L)
    for x in range(6, 18):                          # the torn top
        if x % 2:
            c.px(x, 4, None)
    for i, col in enumerate(FIVE):                  # the band
        c.rect(7 + i * 2, 11, 8 + i * 2, 15, col)
    c.hline(7, 16, 18, KRAFT_D)
    c.outline()
    c.hline(6, 17, 10, INK)
    c.hline(6, 17, 16, INK)
    return c


def i_field_patch():
    """Applied where it broke, by whoever was standing there: a roll of tape, a length of it hanging."""
    c = C()
    c.disc(10, 10, 8, G1)
    c.ring(10, 10, 6.6, 8.6, lambda a: W if 70 < a < 200 else (G2 if 250 < a < 360 else None))
    c.disc(10, 10, 3, None)
    c.ring(10, 10, 2.6, 3.8, lambda a: KRAFT)       # the cardboard core
    c.disc(10, 10, 2, None)
    c.rect(15, 13, 19, 21, G1)                      # the tail of tape
    c.vline(19, 13, 21, G2)
    for x in range(15, 20):                          # its torn end
        if x % 2 == 0:
            c.px(x, 21, None)
    c.outline()
    return c


def i_workaround():
    """Not the fix; the thing you do instead of the fix: a barrier across the way, and an arrow round it."""
    c = C()
    for y in range(9, 22):                          # the barrier, striped
        for x in range(9, 15):
            c.px(x, y, OVERHEATED[0] if ((x + y) // 2) % 2 else W)
    c.vline(14, 9, 21, G2)
    c.rect(2, 16, 4, 18, HP)                        # the way round: in, up, over, down, out
    c.rect(2, 4, 4, 16, HP)
    c.rect(2, 3, 19, 5, HP)
    c.rect(17, 3, 19, 13, HP)
    c.hline(2, 19, 3, HP_L)
    c.ascii(15, 13, ["XXXXXXX", " XXXXX ", "  XXX  ", "   X   "], {"X": HP})
    c.outline()
    return c


def type_colours():
    """tools/gbasprite.py's TYPE_COLOR, read rather than copied (as genplugincolours.py reads it)."""
    import ast
    src = open(os.path.join(ROOT, "tools/gbasprite.py")).read()
    m = re.search(r"^TYPE_COLOR = \{.*?^\}", src, re.S | re.M)
    return ast.literal_eval(m.group(0).split("=", 1)[1])


def power_symbol(c, cx, cy, r, col):
    c.ring(cx, cy, r - 1.1, r + 0.1, lambda a: None if 55 < a < 125 else col)
    c.vline(int(cx), int(cy - r - 0.5), int(cy), col)
    c.vline(int(cx) + 1, int(cy - r - 0.5), int(cy), col)


def i_restart(full=False):
    """Starts a HALTED daemon again: a power key in HALTED's red, and under it a bar half green (RESTART) or whole
    (REBOOT)."""
    c = C()
    L, M, D = HALTED
    c.disc(11.5, 9.5, 8, M)
    c.ring(11.5, 9.5, 6.6, 8.6, lambda a: L if 45 < a < 225 else D)
    power_symbol(c, 11, 10, 4.2, W)
    c.rect(4, 19, 19, 21, G4)                       # the health it comes back with
    c.rect(5, 20, 18 if full else 11, 20, HP)
    c.outline()
    return c


def i_reboot():
    return i_restart(full=True)


def i_cold_start():
    """Brought up from nothing rather than resumed: a power plug, HALTED's red, its cable coming in from cold."""
    c = C()
    L, M, D = HALTED
    c.rect(7, 2, 8, 6, G1)                          # the prongs
    c.rect(15, 2, 16, 6, G1)
    c.rect(4, 7, 19, 14, M)                         # the plug's head
    c.hline(4, 19, 7, L)
    c.rect(6, 15, 17, 16, D)
    c.rect(10, 17, 13, 21, G3)                      # the cable
    c.px(14, 21, G3)
    c.rect(9, 10, 14, 11, W)                        # the plug's grip lines
    c.outline()
    return c


def i_restart_all():
    """Every halted daemon at once, and all of them whole: four power keys together."""
    c = C()
    L, M, D = HALTED
    for cx, cy in ((6, 6), (17, 6), (6, 17), (17, 17)):
        c.disc(cx, cy, 4.5, M)
        c.ring(cx, cy, 3.6, 5.0, lambda a: L if 45 < a < 225 else D)
        c.ring(cx, cy, 1.2, 2.3, lambda a: None if 60 < a < 120 else W)
        c.vline(cx, cy - 3, cy - 1, W)
    c.outline()
    return c


def battery(cells, n=4):
    """A routine's budget: a cell with n segments, `cells` of them charged in MP's blue."""
    c = C()
    c.rect(2, 7, 19, 16, G2)
    c.hline(2, 19, 7, G1)
    c.hline(2, 19, 16, G3)
    c.rect(20, 9, 21, 14, G3)                       # the terminal
    c.rect(4, 9, 17, 14, G4)                        # the window
    for i in range(n):
        x0 = 4 + i * 4 - (0 if i == 0 else 0)
        col = MP if i < cells else (G3 if False else None)
        if col:
            c.rect(x0 + 1, 10, x0 + 2 + (1 if i == n - 1 else 0), 13, col)
            c.vline(x0 + 1, 10, 13, MP_L)
    c.outline()
    return c


def i_charge():
    return battery(1)


def i_full_charge():
    c = battery(4)
    c.ascii(9, 0, ["  XX", " XX ", "XXXX", " XX ", "XX  "], {"X": MP_L})   # and charging still: a spark over it
    c.outline()
    return c


def speaker_muted(pips):
    """Holds the channel quiet: a speaker struck silent, and under it how long -- one, two or three pips."""
    c = C()
    c.rect(3, 7, 6, 13, G2)                         # the speaker's box and its cone
    for i, x in enumerate(range(7, 12)):
        c.vline(x, 7 - i, 13 + i, G1)
    c.vline(11, 3, 17, G2)
    for i in range(5):                              # the cross: nothing comes out
        c.px(14 + i, 7 + i, INK), c.px(15 + i, 7 + i, INK)
        c.px(18 - i, 7 + i, INK), c.px(19 - i, 7 + i, INK)
    for i in range(pips):
        c.rect(4 + i * 6, 20, 7 + i * 6, 21, W)
    c.outline()
    return c


def i_suppress():
    return speaker_muted(1)


def i_long_suppress():
    return speaker_muted(2)


def i_max_suppress():
    return speaker_muted(3)


def i_eject():
    """Out, now, from wherever you are: the eject key."""
    c = C()
    c.rect(3, 3, 20, 20, G2)                        # a keycap, lit from above
    c.rect(3, 3, 20, 4, G1)
    c.rect(3, 18, 20, 20, G3)
    for y in range(6, 13):                          # the triangle
        w = y - 6
        c.hline(11 - w, 12 + w, y, W)
    c.rect(5, 14, 18, 16, W)                        # the bar
    c.outline()
    for x, y in ((3, 3), (20, 3), (3, 20), (20, 20)):
        c.px(x, y, INK)
    return c


def i_decoy():
    """Something else to attend to: a carved decoy duck, painted plainly, on the water's line."""
    c = C()
    rows = [
        "      hhh        ",
        "     hhhhh       ",
        "    bhhehh       ",
        "   bbhhhhh       ",
        "      hhhh       ",
        "      hhhh   tt  ",
        "    wwwwwwwwwttt ",
        "   wwwwwwwwwwwwt ",
        "  wwwwwwwwwwwwwww",
        "  wwwwwwwwwwwwwww",
        "  WWWWWWWWWWWWWW ",
        "   WWWWWWWWWWWW  ",
        "    WWWWWWWWWW   ",
    ]
    c.ascii(2, 4, rows, {"h": (46, 96, 70), "b": THROTTLED[1], "e": INK, "w": WOOD, "W": WOOD_D, "t": WOOD_D})
    for x in range(6, 16):                          # the painted wing line
        c.px(x, 12, WOOD_L)
    c.outline()
    for x in range(0, 24, 2):                       # the water it sits on
        c.px(x, 19, GLASS2)
    return c


def i_bicycle():
    """A folding bicycle, as it is: two wheels, a frame, a saddle."""
    c = C()
    for cx in (6, 17):
        c.ring(cx, 15, 3.6, 5.4, lambda a: G3)
        c.px(cx, 15, G2)
    f = (72, 76, 92)
    c.line(6, 15, 10, 10, f)                        # the frame
    c.line(10, 10, 16, 10, f)
    c.line(10, 15, 10, 10, f)
    c.line(10, 15, 16, 10, f)
    c.line(6, 15, 10, 15, f)
    c.line(16, 10, 17, 15, f)
    c.line(15, 6, 16, 10, f)                        # the bars
    c.hline(14, 17, 6, G4)
    c.rect(8, 8, 11, 8, WOOD_D)                     # the saddle
    c.vline(9, 9, 9, f)
    c.outline()
    return c


def i_sitemap():
    """Everywhere there is, and how they join: a page with one box and the boxes it branches into."""
    c = C()
    c.rect(4, 2, 19, 21, W)
    c.vline(19, 2, 21, W2)
    c.hline(4, 19, 21, W2)
    c.rect(16, 2, 19, 5, None)                      # the folded corner
    c.ascii(16, 2, ["W  ", "WW ", "WWW", "WWWW"], {"W": W2})
    c.rect(10, 5, 13, 7, G4)              # the root
    c.vline(11, 8, 10, G2), c.vline(12, 8, 10, G2)
    c.hline(7, 16, 10, G2)
    for x in (7, 16):
        c.vline(x, 11, 12, G2)
    c.vline(11, 11, 12, G2)
    for x0 in (6, 10, 15):                          # the three it branches into
        c.rect(x0, 13, x0 + 2, 15, G3)
    c.vline(7, 16, 17, G2)
    c.rect(6, 18, 8, 19, G2)              # and one under that
    c.outline()
    return c


def i_roll_call():
    """Asks who is listening; USERS who want to engage answer; the battery charges as you walk: a handheld, a ticked
    list on its screen and the charge under it."""
    c = C()
    c.rect(5, 1, 18, 22, G3)
    c.vline(5, 1, 22, G2)
    c.rect(7, 3, 16, 13, (24, 40, 36))              # the screen, the battle UI's readout dark
    ph = (150, 230, 190)
    for i, y in enumerate((5, 8, 11)):
        c.rect(8, y - 1, 9, y, ph if i < 2 else G2)  # a box: two ticked, one not
        c.hline(11, 15, y, ph if i < 2 else G2)
    c.rect(7, 15, 16, 17, G4)                       # the battery
    c.rect(8, 16, 12, 16, HP)
    c.rect(10, 19, 13, 20, G2)                      # a button
    c.outline()
    return c


def rod(c, deep=False):
    c.line(2, 21, 15, 3, WOOD_D)                    # the rod
    c.line(3, 21, 16, 3, WOOD)
    c.rect(2, 19, 4, 21, G3)                        # its reel
    c.px(15, 2, G2)
    c.hline(16, 20, 2, G2)                          # the line, out to the side and down
    return c


def i_query():
    """Asks a body of water what is in it: a rod whose line ends in a question."""
    c = rod(C())
    c.vline(20, 3, 9, G2)
    c.ascii(17, 9, [" XXX ", "X   X", "    X", "   X ", "  X  ", "     ", "  X  "], {"X": W})
    c.outline()
    return c


def i_deep_query():
    """The same question, further down: the line runs past three depth marks to a sounding weight."""
    c = rod(C())
    c.vline(20, 3, 17, G2)
    for y in (7, 11, 15):
        c.hline(18, 19, y, GLASS2)
    c.rect(19, 18, 21, 21, G4)
    c.px(20, 18, G3)
    c.outline()
    return c


def i_full_scan():
    """Reads the whole of it rather than asking: a sonar screen, its rings, its sweep and what it found."""
    c = C()
    c.disc(11.5, 11.5, 10, G3)
    c.disc(11.5, 11.5, 8.5, (20, 44, 44))
    ph = (150, 230, 190)
    c.ring(11.5, 11.5, 5.6, 6.3, lambda a: (60, 110, 100))
    c.ring(11.5, 11.5, 2.6, 3.3, lambda a: (60, 110, 100))
    for t in range(9):                              # the sweep
        c.px(round(11.5 + t * 0.7), round(11.5 - t * 0.7), ph)
    for x, y in ((7, 8), (15, 15), (8, 16), (16, 9)):   # everything, found
        c.px(x, y, W)
    c.outline()
    return c


def i_tea():
    """TEA, as it is: a cup on its saucer, the tea in it, steam over it."""
    c = C()
    c.rect(2, 19, 21, 20, W2)                       # the saucer
    c.hline(4, 19, 21, G1)
    for y in range(10, 19):                         # the cup
        inset = max(0, (y - 15))
        c.hline(4 + inset, 16 - inset, y, W)
    c.hline(5, 15, 10, (150, 86, 40))               # the tea
    c.hline(5, 15, 11, (190, 120, 60))
    c.vline(16, 12, 17, W2)
    c.rect(17, 12, 19, 15, W)                       # the handle
    c.rect(17, 13, 18, 14, None)
    c.hline(4, 16, 13, (120, 140, 190))             # a blue band
    for x, y in ((7, 3), (8, 4), (7, 5), (7, 6), (8, 7), (12, 2), (13, 3), (12, 4), (12, 5), (13, 6), (13, 7)):
        c.px(x, y, W2)                              # the steam, lifting
    c.outline()
    c.vline(15, 11, 17, W2)
    return c


def i_cc7():
    """A sealed module, part no. CC-7, not addressed to you: a grey module, its pins along the foot, a seal across."""
    c = C()
    c.rect(3, 4, 20, 17, G1)
    c.hline(3, 20, 4, W2)
    c.vline(20, 4, 17, G2)
    for x in range(5, 19, 2):                       # its pins
        c.vline(x, 18, 20, G2)
    c.rect(6, 7, 13, 10, W)                         # the part label, with its number ruled in
    c.hline(7, 9, 8, G3), c.hline(11, 12, 8, G3)
    c.rect(15, 4, 17, 17, HALTED[2])                # the seal tape, and its seal
    c.disc(16, 12, 2.2, HALTED[1])
    c.px(15, 11, HALTED[0])
    c.outline()
    return c


def i_interrupt():
    """Sends an interrupt; a daemon that has stopped responding will wake: a bell, and what it sends out."""
    c = C()
    for y in range(4, 16):                          # the bell
        half = 3 + (y - 4) // 2
        c.hline(12 - half, 11 + half, y, G1)
    c.hline(4, 19, 16, G2)
    c.rect(10, 2, 13, 3, G2)
    c.rect(10, 17, 13, 18, G3)                      # the clapper
    for y in range(5, 15):
        c.px(9 - (y - 4) // 4, y, W)
    c.outline()
    for p in ((2, 6), (1, 8), (1, 10), (2, 12), (21, 6), (22, 8), (22, 10), (21, 12)):   # the ring, sent out
        c.px(p[0], p[1], W)
    return c


def i_toolkit():
    """A case for PLUGINS and DRIVERS: a toolbox, and three plugin cards standing in it in three types' hues (it
    holds routines of every type)."""
    tc = type_colours()
    c = C()
    for x0, t in ((5, "FIGHTING"), (10, "FLYING"), (15, "GRASS")):   # LOGIC, VECTOR, GROWTH
        lit, mid, dark = ramp(tc[t], 0.35)
        c.rect(x0, 3, x0 + 3, 9, mid)
        c.vline(x0, 3, 9, lit)
        c.hline(x0 + 1, x0 + 2, 4, W)
    c.rect(2, 10, 21, 20, G3)                       # the case
    c.hline(2, 21, 10, G2)
    c.hline(2, 21, 20, G4)
    c.rect(10, 13, 13, 15, G1)                      # its latch
    c.outline()
    return c


def i_hearsay():
    """Holds what you were told about people, and who told you: one speech balloon behind another."""
    c = C()
    c.rect(2, 2, 14, 10, G1)                        # what was said first
    c.ascii(4, 11, ["XX", "X "], {"X": G1})
    c.rect(8, 8, 21, 17, W)                         # and what was said about it
    c.ascii(16, 18, ["XX", " X"], {"X": W})
    for x in (11, 14, 17):
        c.rect(x, 12, x + 1, 13, G3)
    c.outline()
    for x, y in ((2, 2), (14, 2), (2, 10), (21, 8), (21, 17), (8, 17)):
        c.px(x, y, INK if c.get(x, y) else None)
    return c


def i_stream():
    """Data read as it arrives; this one carries recorded lectures: a small screen, a line of signal across it."""
    c = C()
    c.rect(2, 4, 21, 17, G3)
    c.rect(4, 6, 19, 15, (24, 40, 36))
    ph = (150, 230, 190)
    ys = [11, 10, 9, 9, 10, 11, 12, 13, 13, 12, 11, 10, 9, 9, 10, 11]
    for i, y in enumerate(ys):
        c.px(4 + i, y, ph)
    c.rect(9, 18, 14, 19, G2)                       # the stand
    c.rect(6, 20, 17, 20, G3)
    c.vline(9, 1, 3, G2)                            # its aerial
    c.vline(14, 1, 3, G2)
    c.outline()
    return c


def i_grep():
    """Finds the thing that is there and not shown: a lens over lines of text, one match lit inside it."""
    c = C()
    for y in (3, 6, 9, 12, 15):                     # the lines it searches
        c.hline(2, 17 if y % 2 else 13, y, G2)
    c.disc(10, 9, 5.5, GLASS)
    c.ring(10, 9, 5.2, 6.8, lambda a: G4)
    c.hline(7, 12, 9, THROTTLED[1])                 # the match
    c.hline(6, 13, 6, G1), c.hline(7, 12, 12, G1)
    c.px(8, 5, W), c.px(7, 6, W)
    for i in range(6):                              # the handle
        c.rect(14 + i, 14 + i, 15 + i, 15 + i, G3)
    c.outline()
    return c


def i_card_key():
    """A card-type key for FOUNDRY CO.: a pale card, its chip, its stripe."""
    c = C()
    c.rect(2, 5, 21, 18, W)
    c.vline(21, 5, 18, W2)
    c.hline(2, 21, 18, W2)
    c.rect(2, 7, 21, 8, G4)                         # the stripe
    c.rect(4, 11, 8, 15, (214, 186, 96))            # the chip
    c.hline(4, 8, 13, (170, 140, 60))
    c.vline(6, 11, 15, (170, 140, 60))
    c.hline(11, 18, 12, G2), c.hline(11, 16, 15, G2)
    c.outline()
    return c


# ---- the PLUGIN and the DRIVER, in the engine's per-type palette slots (*_tm_hm.pal)
#   1 ink-dark, 2 slate, 3..9 the type's ramp light->dark, 10/11/12 greys, 13 white, 14 tint, 15 dark grey
def card(driver=False):
    """A routine you plug in: a card in its type's colour, a white label, an edge connector of contacts. The DRIVER
    is the same card with a gear on its label: the routine that drives a thing outside battle."""
    g = [[0] * N for _ in range(N)]

    def r(x0, y0, x1, y1, v):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                g[y][x] = v
    r(4, 2, 19, 16, 6)                              # the card
    r(4, 2, 19, 2, 4)
    r(4, 2, 4, 16, 5)
    r(19, 3, 19, 16, 8)
    r(5, 15, 18, 16, 7)
    r(17, 2, 19, 4, 0)                              # its cut corner
    g[3][17], g[4][18], g[5][19] = 1, 1, 1
    r(6, 4, 15, 10, 13)                             # the label
    r(6, 10, 15, 10, 14)
    if driver:
        gear = ["  X X  ", " XXXXX ", "XXX XXX", " XX XX ", "XXX XXX", " XXXXX ", "  X X  "]
        for j, row in enumerate(gear):
            for i, ch in enumerate(row):
                if ch == "X":
                    g[4 + j][7 + i] = 15
    else:
        r(7, 6, 14, 6, 11)                          # what is written on it
        r(7, 8, 12, 8, 11)
    r(5, 17, 18, 20, 12)                            # the connector board
    for x in range(6, 18, 2):
        r(x, 18, x, 20, 13)                         # the contacts
    #  the outline, in slot 1
    add = []
    for y in range(N):
        for x in range(N):
            if g[y][x] == 0 and any(0 <= x + dx < N and 0 <= y + dy < N and g[y + dy][x + dx] not in (0, 1)
                                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                add.append((x, y))
    for x, y in add:
        g[y][x] = 1
    return g


def i_plugin():
    return card(False)


def i_driver():
    return card(True)


# ================================================================================================= the batch
#  (key, DAEMONS name, item ids, function, mode, what it shows)
#  mode "own": its own files; "tmhm": tm_hm.png in place; "driver": driver.png, the HM rows repointed
ICONS = [
    ("recover", "RECOVER", ["ITEM_POTION"], i_recover, "own", "a graduated flask, HP green to the first mark"),
    ("deep_recover", "DEEP RECOVER", ["ITEM_SUPER_POTION"], i_deep_recover, "own", "the same flask, to the second mark"),
    ("full_recover", "FULL RECOVER", ["ITEM_HYPER_POTION"], i_full_recover, "own", "the same flask, full"),
    ("rebuild", "REBUILD", ["ITEM_MAX_POTION"], i_rebuild, "own", "a wall built up from the ground, its last block coming down"),
    ("snapshot", "SNAPSHOT", ["ITEM_FULL_RESTORE"], i_snapshot, "own", "a print of the moment: a full HP bar and the five states' pips"),
    ("patch", "PATCH", ["ITEM_ANTIDOTE"], i_patch, "own", "a stitched patch over a crack, LEAKING's green"),
    ("coolant", "COOLANT", ["ITEM_BURN_HEAL"], i_coolant, "own", "a coolant jug, OVERHEATED's ember label, temperature down"),
    ("watchdog", "WATCHDOG", ["ITEM_ICE_HEAL"], i_watchdog, "own", "a stopwatch run round to reset, HUNG's blue rim"),
    ("resume", "RESUME", ["ITEM_AWAKENING"], i_resume, "own", "a round play key, SUSPENDED's slate"),
    ("priority", "PRIORITY", ["ITEM_PARALYZE_HEAL"], i_priority, "own", "a queue, and one in THROTTLED's yellow moved to the front"),
    ("rollback", "ROLLBACK", ["ITEM_FULL_HEAL"], i_rollback, "own", "an arrow turned back, in all five states' colours, round a tick"),
    ("restart", "RESTART", ["ITEM_REVIVE"], i_restart, "own", "a power key in HALTED's red, half a bar of health under it"),
    ("reboot", "REBOOT", ["ITEM_MAX_REVIVE"], i_reboot, "own", "the same key, the bar whole"),
    ("hotfix", "HOTFIX", ["ITEM_HEAL_POWDER"], i_hotfix, "own", "a torn kraft sachet, the five states on its band"),
    ("field_patch", "FIELD PATCH", ["ITEM_ENERGY_POWDER"], i_field_patch, "own", "a roll of tape, a length torn off"),
    ("workaround", "WORKAROUND", ["ITEM_ENERGY_ROOT"], i_workaround, "own", "a barrier across the way, a green arrow round it"),
    ("cold_start", "COLD START", ["ITEM_REVIVAL_HERB"], i_cold_start, "own", "a power plug in HALTED's red"),
    ("restart_all", "RESTART ALL", ["ITEM_SACRED_ASH"], i_restart_all, "own", "four power keys together"),
    ("charge", "CHARGE", ["ITEM_ETHER"], i_charge, "own", "a cell with one segment of MP's blue"),
    ("full_charge", "FULL CHARGE", ["ITEM_MAX_ETHER"], i_full_charge, "own", "the cell full, a spark over it"),
    ("suppress", "SUPPRESS", ["ITEM_REPEL"], i_suppress, "own", "a speaker struck silent, one pip of how long"),
    ("long_suppress", "LONG SUPPRESS", ["ITEM_SUPER_REPEL"], i_long_suppress, "own", "the same, two pips"),
    ("max_suppress", "MAX SUPPRESS", ["ITEM_MAX_REPEL"], i_max_suppress, "own", "the same, three pips"),
    ("eject", "EJECT", ["ITEM_ESCAPE_ROPE"], i_eject, "own", "the eject key"),
    ("decoy", "DECOY", ["ITEM_POKE_DOLL"], i_decoy, "own", "a carved decoy duck on the water"),
    ("bicycle", "BICYCLE", ["ITEM_BICYCLE"], i_bicycle, "own", "a bicycle, plainly, in neutrals"),
    ("sitemap", "SITEMAP", ["ITEM_TOWN_MAP"], i_sitemap, "own", "a page: one box and the boxes it branches into"),
    ("roll_call", "ROLL CALL", ["ITEM_VS_SEEKER"], i_roll_call, "own", "a handheld, a ticked list on its screen, its charge under"),
    ("query", "QUERY", ["ITEM_OLD_ROD"], i_query, "own", "a rod whose line ends in a question"),
    ("deep_query", "DEEP QUERY", ["ITEM_GOOD_ROD"], i_deep_query, "own", "the line past three depth marks to a weight"),
    ("full_scan", "FULL SCAN", ["ITEM_SUPER_ROD"], i_full_scan, "own", "a sonar screen: rings, a sweep, all of it found"),
    ("tea", "TEA", ["ITEM_TEA"], i_tea, "own", "a cup of tea on its saucer, steaming"),
    ("cc_7", "CC-7", ["ITEM_OAKS_PARCEL"], i_cc7, "own", "a sealed grey module, pins along its foot, a seal across"),
    ("interrupt", "INTERRUPT", ["ITEM_POKE_FLUTE"], i_interrupt, "own", "a bell, ringing out"),
    ("toolkit", "TOOLKIT", ["ITEM_TM_CASE"], i_toolkit, "own", "a toolbox, three plugin cards standing in it in three types' hues"),
    ("hearsay", "HEARSAY", ["ITEM_FAME_CHECKER"], i_hearsay, "own", "one speech balloon behind another"),
    ("stream", "STREAM", ["ITEM_TEACHY_TV"], i_stream, "own", "a small screen, a line of signal across it"),
    ("grep", "GREP", ["ITEM_ITEMFINDER"], i_grep, "own", "a lens over lines of text, one match lit"),
    ("card_key", "CARD KEY", ["ITEM_CARD_KEY"], i_card_key, "own", "a pale keycard: stripe, chip"),
    ("plugin", "PLUGIN", ["ITEM_TM%02d" % i for i in range(1, 51)], i_plugin, "tmhm",
     "a card with an edge connector, in its type's palette (PLUGIN01: LOGIC)"),
    ("driver", "DRIVER", ["ITEM_HM%02d" % i for i in range(1, 9)], i_driver, "driver",
     "the same card, a gear on its label (DRIVER01: CONTENT)"),
]


# ================================================================================================= the engine's files
def jasc_read(p):
    v = [int(t) for t in open(p).read().split()[3:]]
    return [tuple(v[i:i + 3]) for i in range(0, len(v), 3)]


def jasc_text(pal):
    pal = list(pal) + [(0, 0, 0)] * (16 - len(pal))
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal)


def symbol_files():
    """{gItemIcon_X or gItemIconPalette_X: the file stem it INCBINs}, from items.h."""
    out = {}
    for m in re.finditer(r'const u32 (gItemIcon\w+)\[\]\s*=\s*INCBIN_U32\("graphics/items/(?:icons|icon_palettes)/(\w+)\.',
                         open(ITEMS_H).read()):
        out[m.group(1)] = m.group(2)
    return out


def table_rows():
    rows = {}
    for m in re.finditer(r"\[(ITEM_\w+)\]\s*=\s*\{(gItemIcon_\w+), (gItemIconPalette_\w+)\}", open(TABLE).read()):
        rows[m.group(1)] = (m.group(2), m.group(3))
    return rows


def vanilla_files():
    """The engine's icon files whose drawing is still pret's: everything the fork has not changed under graphics/items."""
    import subprocess
    try:
        ch = subprocess.run(["git", "-C", GBA, "diff", "--name-only", "upstream/master", "--", "graphics/items/icons"],
                            capture_output=True, text=True).stdout.split()
    except Exception:
        ch = []
    return {os.path.basename(p)[:-4] for p in ch if p.endswith(".png")}


def engine_icon(item):
    """(RGBA 24x24, file stem) of what the engine shows for an item now."""
    rows, files = table_rows(), symbol_files()
    gfx, pal = rows[item]
    stem, pstem = files[gfx], files[pal]
    im = Image.open(os.path.join(ICON_DIR, stem + ".png"))
    p = jasc_read(os.path.join(PALS, pstem + ".pal"))
    out = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    src = list(im.getdata())
    out.putdata([(0, 0, 0, 0) if v == 0 else p[v] + (255,) for v in src])
    return out, stem


def tm_palette(item):
    rows, files = table_rows(), symbol_files()
    return jasc_read(os.path.join(PALS, files[rows[item][1]] + ".pal"))


# ================================================================================================= quantise and render
def to_indexed(c):
    """A canvas -> (24x24 index grid, palette of up to 16 with 0 transparent). Refuses more than 15 colours."""
    cols = []
    for row in c.g:
        for v in row:
            if v is not None and v not in cols:
                cols.append(v)
    if INK in cols:                                 # the ink first, as OPUS and the NOTEBOOK keep it
        cols.remove(INK)
        cols.insert(0, INK)
    assert len(cols) <= 15, "%d colours" % len(cols)
    pal = [(0, 0, 0)] + cols
    idx = [[0 if v is None else pal.index(v) for v in row] for row in c.g]
    return idx, pal


def q5(c):
    return tuple((v >> 3) << 3 for v in c)


def make(entry):
    key, name, items, fn, mode, _ = entry
    if mode in ("tmhm", "driver"):
        return fn(), [q5(c) for c in tm_palette(items[0])]
    idx, pal = to_indexed(fn())
    return idx, [q5(c) for c in pal]


def p_image(idx, pal):
    im = Image.new("P", (N, N), 0)
    im.putpalette([v for c in (list(pal) + [(0, 0, 0)] * (16 - len(pal))) for v in c] + [0] * (768 - 48))
    im.putdata([v for row in idx for v in row])
    return im


def rgba(idx, pal):
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    im.putdata([(0, 0, 0, 0) if v == 0 else tuple(pal[v]) + (255,) for row in idx for v in row])
    return im


# ================================================================================================= the font
_FONT = None


def print_text(im, x, y, s, ink, shadow):
    """The engine's own latin_normal sheet and widths: what the BAG prints in."""
    global _FONT
    import fontwidth
    if _FONT is None:
        _FONT = (Image.open(os.path.join(GBA, "graphics/fonts/latin_normal.png")), fontwidth.font(GBA))
    sheet, (w, cm) = _FONT
    fp, px = sheet.load(), im.load()
    for ch in s:
        b = cm.get(ch)
        if b is None:
            continue
        gx, gy = (b % 16) * 16, (b // 16) * 16
        for yy in range(16):
            for xx in range(min(16, w[b])):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, y + yy
                if 0 <= X < im.width and 0 <= Y < im.height:
                    if v == 1:
                        px[X, Y] = ink
                    elif v == 2:
                        px[X, Y] = shadow
        x += w[b]
    return x


def label_font(size=12):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except Exception:
        return ImageFont.load_default()


# ================================================================================================= the BAG, at real size
def gbapal(p):
    d = open(p, "rb").read()
    out = []
    for i in range(0, len(d), 2):
        v = d[i] | d[i + 1] << 8
        out.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3))
    return out


def bag_mock(icon_for, rows, selected, description, pocket="ITEMS", frame=0):
    """240x160: the BAG's own background (graphics/item_menu/bg.png + bg.bin + bg.gbapal), its sprite at (40,68), the
    list in window 0 (11,1; 18x12 tiles; DARK_GRAY on LIGHT_GRAY, as sListItemTextColor_RegularItem), the description
    in window 1 (5,14; WHITE on DARK_GRAY), the pocket's name in window 2, and the selected item's icon where
    CreateItemMenuIcon puts it (centre 24,140: a 32x32 sprite, the 24x24 icon at its top left)."""
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    tiles = Image.open(os.path.join(GBA, "graphics/item_menu/bg.png"))
    tp = tiles.load()
    tw = tiles.width // 8
    pal = gbapal(os.path.join(GBA, "graphics/item_menu/bg.gbapal"))
    tm = open(os.path.join(GBA, "graphics/item_menu/bg.bin"), "rb").read()
    px = im.load()
    for ty in range(20):
        for tx in range(30):
            e = tm[(ty * 32 + tx) * 2] | tm[(ty * 32 + tx) * 2 + 1] << 8
            t, hf, vf, pn = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
            for y in range(8):
                for x in range(8):
                    sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                    v = tp[(t % tw) * 8 + sx, (t // tw) * 8 + sy] if t // tw < tiles.height // 8 else 0
                    c = pal[(pn * 16 + v) % len(pal)] if v else pal[0]
                    px[tx * 8 + x, ty * 8 + y] = c
    bag = Image.open(os.path.join(GBA, "graphics/interface/bag_male.png")).crop((0, 64 * frame, 64, 64 * frame + 64))
    bp = jasc_read(os.path.join(GBA, "graphics/interface/bag.pal"))
    bpx = bag.load()
    for y in range(64):
        for x in range(64):
            v = bpx[x, y]
            if v:
                px[8 + x, 36 + y] = bp[v]
    wp = jasc_read(os.path.join(GBA, "graphics/item_menu/bag_window_pal.pal"))
    WHITE, DARK, LIGHT = wp[1], wp[2], wp[3]
    name_w = 0
    import fontwidth
    w, cm = fontwidth.font(GBA)
    name_w = sum(w[cm[ch]] for ch in pocket if ch in cm)
    print_text(im, 8 + (72 - name_w) // 2, 9, pocket, WHITE, DARK)
    for i, (nm, qty) in enumerate(rows):
        y = 8 + 2 + i * 16
        if i == selected:
            print_text(im, 88 + 1, y, "▶", DARK, LIGHT)
        print_text(im, 88 + 9, y, nm, DARK, LIGHT)
        if qty:
            print_text(im, 88 + 110, y, "×%d" % qty, DARK, LIGHT)
    for j, line in enumerate(description):
        print_text(im, 40, 112 + 3 + j * 16, line, WHITE, DARK)
    ic = icon_for(rows[selected][0])
    im.paste(ic, (8, 124), ic)
    return im


# ================================================================================================= draft, sheet, write
def item_texts():
    it = {i["itemId"]: i for i in __import__("json").load(open(ITEMS_JSON))["items"]}
    return it


def draft(out):
    os.makedirs(out, exist_ok=True)
    made = {}
    for e in ICONS:
        idx, pal = make(e)
        p_image(idx, pal).save(os.path.join(out, e[0] + ".png"))
        with open(os.path.join(out, e[0] + ".pal"), "w", newline="") as f:
            f.write(jasc_text(pal))
        made[e[0]] = (idx, pal)
    texts = item_texts()
    sheet(out, made, texts)
    mocks(out, made, texts)
    print("  drafted %d icons into %s, the sheet and the BAG mocks" % (len(made), os.path.relpath(out, ROOT)))


def sheet(out, made, texts):
    F, Fs, Fb = label_font(12), label_font(11), label_font(15)
    cols, cw, ch = 3, 520, 128
    rows = (len(ICONS) + cols - 1) // cols
    head = 92
    im = Image.new("RGB", (cols * cw + 20, head + rows * ch + 10), (28, 30, 36))
    d = ImageDraw.Draw(im)
    d.text((14, 10), "T-525 DRAFT -- the item icons, batch 1 (41): what each DAEMONS item IS, drawn by hand in code "
                     "(no AI image). 24x24, own 16-colour palette, index 0 clear.", fill=(232, 232, 232), font=Fb)
    d.text((14, 34), "Each: the engine's icon now (1x, 4x) | ours (1x, 4x) on the BAG's grey. Colour: a cure wears the "
                     "STATE it ends; HP items the HP bar's green, their tier by how full; PLUGIN/DRIVER their type's "
                     "palette.", fill=(190, 190, 196), font=F)
    d.text((14, 54), "Nothing is in the engine. Approve some or all: gbaitemicons.py --write --approved ITEM ... "
                     "(an unnamed item keeps its row).", fill=(190, 190, 196), font=F)
    vfiles = vanilla_files()
    bgc = (184, 176, 160)
    for n, e in enumerate(ICONS):
        key, name, items, _, _, what = e
        x0, y0 = 10 + (n % cols) * cw, head + (n // cols) * ch
        d.rectangle([x0, y0, x0 + cw - 10, y0 + ch - 8], fill=(40, 43, 50))
        van, stem = engine_icon(items[0])
        ours = rgba(*made[key])
        for k, (ic, X) in enumerate(((van, x0 + 6), (ours, x0 + 140))):
            d.rectangle([X, y0 + 8, X + 24 + 4 + 96 + 2, y0 + 8 + 100], fill=bgc)
            im.paste(ic, (X + 2, y0 + 10), ic)
            big = ic.resize((96, 96), Image.NEAREST)
            im.paste(big, (X + 30, y0 + 10), big)
        tag = "pret's" if stem not in vfiles else "ours"
        d.text((x0 + 6, y0 + 110), "now: %s.png (%s)" % (stem, tag), fill=(150, 150, 156), font=Fs)
        d.text((x0 + 276, y0 + 8), name, fill=(240, 236, 210), font=Fb)
        d.text((x0 + 276, y0 + 28), items[0] + (" +%d" % (len(items) - 1) if len(items) > 1 else ""),
               fill=(140, 140, 150), font=Fs)
        words, line, ly = what.split(), "", y0 + 48
        for wd in words:
            if len(line) + len(wd) > 30:
                d.text((x0 + 276, ly), line, fill=(214, 214, 220), font=F)
                line, ly = "", ly + 15
            line = (line + " " + wd).strip()
        d.text((x0 + 276, ly), line, fill=(214, 214, 220), font=F)
    im.save(os.path.join(out, "t525_item_icons_sheet.png"))


def wrap208(text):
    import fontwidth
    w, cm = fontwidth.font(GBA)
    lines, cur = [], ""
    for wd in text.replace("\n", " ").split():
        t = (cur + " " + wd).strip()
        if sum(w[cm[c]] for c in t if c in cm) > 194 and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    lines.append(cur)
    return lines[:3]


def mocks(out, made, texts):
    """The BAG at 240x160 twice: the ITEMS pocket with RECOVER selected, ours and the engine's now; and a strip of
    six real-size mocks, one per selection, so each icon is seen where it will live."""
    by_name = {e[1]: e for e in ICONS}
    pocket = [("RECOVER", 6), ("DEEP RECOVER", 2), ("PATCH", 3), ("RESUME", 1), ("SUPPRESS", 4), ("EJECT", 2)]

    def ours(nm):
        return rgba(*made[by_name[nm][0]])

    def now(nm):
        return engine_icon(by_name[nm][2][0])[0]

    keys = [("BICYCLE", 0), ("SITEMAP", 0), ("ROLL CALL", 0), ("QUERY", 0), ("TOOLKIT", 0), ("TEA", 0)]
    frames = []
    for rows, s, pk, fr in [(pocket, 0, "ITEMS", 0), (pocket, 2, "ITEMS", 0), (pocket, 4, "ITEMS", 0),
                            (keys, 2, "KEY ITEMS", 1), (keys, 4, "KEY ITEMS", 1)]:
        e = by_name[rows[s][0]]
        desc = wrap208(texts[e[2][0]]["description_english"].replace("\\n", " "))
        frames.append((bag_mock(ours, rows, s, desc, pk, fr), bag_mock(now, rows, s, desc, pk, fr)))
    frames[0][0].save(os.path.join(out, "bag_mock.png"))
    frames[0][1].save(os.path.join(out, "bag_mock_engine.png"))
    strip = Image.new("RGB", (len(frames) * 248 + 8, 2 * 168 + 8 + 40), (28, 30, 36))
    d = ImageDraw.Draw(strip)
    d.text((8, 6), "The BAG at 240x160 (its own background, font, windows and words): ours on top, the engine's now "
                   "below. Only the icon changes.",
           fill=(220, 220, 224), font=label_font(12))
    for i, (a, b) in enumerate(frames):
        strip.paste(a, (8 + i * 248, 40))
        strip.paste(b, (8 + i * 248, 40 + 168))
    strip.save(os.path.join(out, "bag_mocks_real_size.png"))
    x2 = Image.new("RGB", (480 * 2 + 24, 320 + 16), (28, 30, 36))
    x2.paste(frames[0][0].resize((480, 320), Image.NEAREST), (8, 8))
    x2.paste(frames[0][1].resize((480, 320), Image.NEAREST), (496, 8))
    x2.save(os.path.join(out, "bag_mock_2x.png"))


def report():
    rows, files, vfiles = table_rows(), symbol_files(), vanilla_files()
    print("  T-525 item icons, batch 1: %d icons (DRAFT, nothing approved)" % len(ICONS))
    for e in ICONS:
        key, name, items, _, mode, what = e
        idx, pal = make(e)
        stem = files[rows[items[0]][0]]
        state = "ours" if stem in vfiles else "pret's"
        target = {"own": "icons/d_%s.png" % key, "tmhm": "icons/tm_hm.png (in place)", "driver": "icons/driver.png"}[mode]
        used = len({v for row in idx for v in row} - {0})
        print("    %-14s %-20s now %-16s (%-6s) -> %-28s %2d colours" % (name, items[0], stem, state, target, used))
    print("  --draft draws them and the sheet; --write --approved ITEM ... writes the named ones.")


def write(keys):
    import shutil
    chosen = [e for e in ICONS if e[0] in keys or e[1] in keys or any(i in keys for i in e[2])]
    if not chosen:
        print("  nothing named matches the batch")
        return 1
    items_h, graphics_h, table = open(ITEMS_H).read(), open(GRAPHICS_H).read(), open(TABLE).read()
    for e in chosen:
        key, name, items, _, mode, _ = e
        idx, pal = make(e)
        if mode == "tmhm":
            p_image(idx, pal).save(os.path.join(ICON_DIR, "tm_hm.png"))
            print("  written icons/tm_hm.png (every PLUGIN keeps its type palette)")
            continue
        sym = "D" + "".join(p.capitalize() for p in key.split("_"))
        stem = "driver" if mode == "driver" else "d_" + key
        p_image(idx, pal).save(os.path.join(ICON_DIR, stem + ".png"))
        decl = 'const u32 gItemIcon_%s[] = INCBIN_U32("graphics/items/icons/%s.4bpp.lz");   %s\n' % (sym, stem, TAG)
        if mode != "driver":
            with open(os.path.join(PALS, stem + ".pal"), "w", newline="") as f:
                f.write(jasc_text(pal))
            decl += 'const u32 gItemIconPalette_%s[] = INCBIN_U32("graphics/items/icon_palettes/%s.gbapal.lz");\n' % (sym, stem)
        if decl not in items_h:
            items_h = items_h.rstrip("\n") + "\n" + decl
        ext = "extern const u32 gItemIcon_%s[];   // T-525\n" % sym
        if mode != "driver":
            ext += "extern const u32 gItemIconPalette_%s[];\n" % sym
        if ext not in graphics_h:
            k = graphics_h.rstrip().rfind("#endif")
            graphics_h = graphics_h[:k] + ext + "\n" + graphics_h[k:]
        for item in items:
            line = [l for l in table.split("\n") if l.lstrip().startswith("[%s]" % item)]
            assert len(line) == 1, "item_icon_table.h: one row for %s" % item
            palsym = re.search(r"gItemIconPalette_\w+", line[0]).group(0) if mode == "driver" else "gItemIconPalette_" + sym
            row = "    %-22s= {gItemIcon_%s, %s},   %s" % ("[%s]" % item, sym, palsym, TAG)
            table = table.replace(line[0], row)
        print("  written %s (%s)" % (stem, ", ".join(items[:3]) + (" ..." if len(items) > 3 else "")))
    for p, s in ((ITEMS_H, items_h), (GRAPHICS_H, graphics_h), (TABLE, table)):
        if open(p).read() != s:
            tmp = p + ".tmp"
            open(tmp, "w").write(s)
            shutil.copymode(p, tmp)
            os.replace(tmp, p)
    print("  now build all four ROMs and check each exit code")
    return 0


def main():
    if A.write:
        if not A.approved:
            print("  --write refuses without --approved: the user picks from the sheet first (T-525).")
            return 0
        keys = [e[0] for e in ICONS] if A.all else (A.items or APPROVED)
        if not keys:
            print("  --write --approved names no items, and none is approved yet: nothing written.")
            return 0
        return write(set(keys))
    if A.draft:
        draft(A.draft)
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
