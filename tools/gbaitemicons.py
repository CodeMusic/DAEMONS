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

DRAFT, 2026-11-07, the user away ("Item icons" next, from the vanilla-art census, gap 4). BUILT the same day: the user, "Build all
41" -- and batch 2's forty-seven the same day too: the user, "Build all 47", and batch 3's fifty-seven (ICONS3, `--draft
--batch 3`: the held items and the TRAP TABLE's TRAPs) the same day: the user, "Build all 57". APPROVED holds every icon of
all three batches, and batch 4's forty-seven (ICONS4, `--draft --batch 4`, 2026-11-09: the valuables, shards, MAIL,
scarves, berries and four key items) were approved 2026-11-09: the user, "Build all" and "Keep all 20" (the berries).
APPROVED holds every icon of all four batches, `--all` writes all four, and the report exits 1 when the engine is not
what that write makes. Every pixel here is drawn in
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
ap.add_argument("--batch", type=int, default=1)               # --draft --batch 2: batch 2's drafts
ap.add_argument("--over-later-work", action="store_true")    # check_generators passes it to every --write; unused
ap.add_argument("items", nargs="*")
A = ap.parse_args() if __name__ == "__main__" else ap.parse_args([])

#  The user's pick, 2026-11-07: "Build all 41" -- every icon in ICONS (set below, once ICONS exists). A later batch's
#  items join only when the user approves them; --write --approved ITEM ... still writes any named item alone.
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


APPROVED = [e[0] for e in ICONS]      # the user, 2026-11-07: "Build all 41"


# ================================================================================================= batch 2
#  Drafted 2026-11-07, the user away, after batch 1 was built; `--draft --batch 2` draws them. APPROVED the same day
#  (the user, 2026-11-07: "Build all 47"), so `--all` and the report cover both batches.
GOLD_L, GOLD, GOLD_D = (255, 222, 74), (213, 172, 32), (131, 98, 0)        # brass and amber (npc_blue's, T-167)
COPPER_L, COPPER, COPPER_D = (232, 160, 110), (190, 112, 66), (120, 66, 36)
PAPER, PAPER2 = (240, 236, 222), (204, 198, 180)
NAVY = (44, 52, 84)                                                         # the S.S. ANNE's hull (genships.py)
TASSEL, TASSEL_D = (150, 52, 60), (96, 34, 42)                             # SECRET KEY's tassel: its description's red
PUB = ((238, 115, 65), (172, 65, 57), (74, 49, 49))                         # PUBLIC KEY, as the overworld's (genmisc.py)
PRIV = ((164, 139, 238), (106, 82, 189), (65, 57, 98))                      # PRIVATE KEY


def tc(vanilla):
    """A type's ramp, read from gbasprite.py's TYPE_COLOR (FIGHTING is LOGIC, FLYING VECTOR, PSYCHIC CONTEXT, GRASS
    GROWTH)."""
    return ramp(tuple(type_colours()[vanilla]), 0.38)


#  ---- TUNE: a parameter turned up for one run. A dial turned to the top of its arc, its ticks lit, and the
#  parameter on a tag. Neutrals: a stat has no type.
GLYPHS = {
    "attack": ["   XXXX", "     XX", "    X X", "   X  X", "  X    ", " X     ", "X      "],
    "defense": ["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", " XXXXX ", "  XXX  ", "   X   "],
    "speed": ["X  X   ", " X  X  ", "  X  X ", "   X  X", "  X  X ", " X  X  ", "X  X   "],
    "aim": ["   X   ", " XXXXX ", " X X X ", "XXX XXX", " X X X ", " XXXXX ", "   X   "],
    "spatk": ["   X   ", " X X X ", "  XXX  ", "XXXXXXX", "  XXX  ", " X X X ", "   X   "],
    "crit": ["  X    ", " X X   ", " X X   ", "X   X  ", "X   oX ", "X   ooX", "XXXXooo"],
}


def dial(glyph):
    c = C()
    cx, cy = 9.5, 9.5
    #  the track round the knob, lit from the bottom left all the way over to the bottom right: turned all the way up
    c.ring(cx, cy, 7.4, 8.8, lambda a: W if (a <= 225 or a >= 315) else G3)
    c.disc(cx, cy, 6.0, G2)
    c.ring(cx, cy, 4.6, 6.6, lambda a: G1 if 45 < a < 225 else G3)
    r = math.radians(-30)                             # the pointer, at the top of its travel
    c.line(int(cx), int(cy), int(round(cx + 5 * math.cos(r))), int(round(cy - 5 * math.sin(r))), W)
    c.px(int(cx), int(cy), G4)
    c.outline()
    c.box(12, 12, 22, 22, G4)
    c.ascii(14, 14, GLYPHS[glyph], {"X": W, "o": G1} if glyph != "crit" else {"X": G1, "o": W})
    return c


def i_tune_attack(): return dial("attack")
def i_tune_defense(): return dial("defense")
def i_tune_speed(): return dial("speed")
def i_tune_aim(): return dial("aim")
def i_tune_spatk(): return dial("spatk")
def i_tune_crit(): return dial("crit")


def i_lock_stats():
    """Nothing outside gets to change them: three stat bars, and a padlock shut in front of them."""
    c = C()
    for x, h in ((3, 12), (8, 16), (13, 9), (18, 14)):
        c.rect(x, 21 - h, x + 2, 21, G2)
        c.vline(x, 21 - h, 21, G1)
    c.outline()
    c.ring(14.5, 11.5, 2.4, 4.0, lambda a: (G1 if a < 90 else G2) if a <= 180 else None)
    c.rect(11, 11, 12, 13, G2), c.rect(17, 11, 18, 13, G1)
    c.box(9, 13, 20, 22, G1)
    c.hline(10, 19, 14, W)
    c.rect(14, 16, 15, 17, INK), c.px(14, 18, INK), c.px(15, 18, INK), c.px(14, 19, INK)
    c.outline()
    return c


#  ---- the vitamins: what the daemon is built with. Each the component its DAEMONS name names; neutrals, and the
#  metals they are made of (gold contacts, copper), which label nothing.
def i_memory():
    """How much it can hold: a memory module, its chips, its gold edge."""
    c = C()
    c.rect(1, 6, 22, 16, G3)
    c.hline(1, 22, 6, G2)
    for x in (3, 8, 13, 18):
        c.rect(x, 8, x + 3, 13, G4)
        c.hline(x, x + 3, 8, G2)
    c.px(11, 16, None), c.px(12, 16, None)
    for x in range(2, 22):
        if x in (11, 12):
            continue
        c.vline(x, 17, 19, GOLD if x % 2 == 0 else GOLD_D)
    c.outline()
    return c


def i_wattage():
    """How hard it can drive something: a bolt across a power unit's face."""
    c = C()
    c.box(3, 3, 20, 20, G3)
    c.hline(4, 19, 4, G2)
    c.ascii(7, 5, ["     XXXX", "    XXXX ", "   XXXX  ", "  XXXX   ", " XXXXXXXX", "XXXXXXXX ", "    XXX  ",
                   "   XXX   ", "  XXX    ", " XX      ", "XX       ", "X        "],
            {"X": W})
    c.rect(5, 18, 6, 18, G1), c.rect(17, 18, 18, 18, G1)
    c.outline()
    return c


def i_shielding():
    """What sits between it and what is arriving: three arrows coming in, and a plate they stop at."""
    c = C()
    c.rect(15, 2, 19, 21, G1)
    c.vline(15, 2, 21, W)
    c.vline(19, 2, 21, G2)
    for y in (3, 8, 13, 18):
        c.px(17, y, G2)
    for y in (6, 11, 16):
        c.hline(2, 11, y, G2)
        c.px(12, y, G3), c.px(11, y - 1, G2), c.px(11, y + 1, G2), c.px(10, y - 2, G2), c.px(10, y + 2, G2)
    c.outline()
    return c


def i_clock_rate():
    """How many times a second it acts: a crystal's can, its two legs, the square wave it keeps."""
    c = C()
    wave = ["XXX   XXX   XXX ", "X X   X X   X X ", "X X   X X   X X ", "X XXXXX XXXXX XX"]
    c.ascii(4, 1, wave, {"X": W})
    c.box(3, 8, 20, 17, G1)
    c.rect(5, 8, 18, 8, INK)
    c.hline(4, 19, 9, W)
    c.hline(4, 19, 16, G2)
    c.vline(19, 9, 16, G2)
    c.rect(6, 12, 17, 13, G2)
    c.vline(7, 18, 22, G2), c.vline(16, 18, 22, G2)
    c.outline()
    return c


def i_bandwidth():
    """How much it can push down one channel: a broad bus of lines, all of them carrying, into one connector."""
    c = C()
    c.rect(1, 5, 15, 18, G2)
    for y in range(6, 18, 2):
        c.hline(1, 15, y, W)
    c.box(15, 3, 22, 20, G3)
    c.rect(17, 5, 20, 18, G4)
    for y in range(6, 18, 2):
        c.px(18, y, G1), c.px(19, y, G1)
    c.outline()
    return c


def i_insulation():
    """What keeps the outside out: a cable cut through, the copper at its heart, the layers round it."""
    c = C()
    c.disc(11.5, 11.5, 10, G4)
    c.disc(11.5, 11.5, 8, G2)
    c.disc(11.5, 11.5, 6.4, W2)
    c.disc(11.5, 11.5, 3.0, COPPER)
    c.disc(10.5, 10.5, 1.2, COPPER_L)
    c.ring(11.5, 11.5, 8.7, 10.4, lambda a: G3 if 30 < a < 210 else None)
    c.outline()
    return c


def i_increment():
    """Adds exactly one: a key, +1 on its face."""
    c = C()
    c.box(2, 3, 21, 20, G2)
    c.rect(3, 4, 20, 17, G1)
    c.hline(3, 20, 4, W)
    c.rect(3, 18, 20, 19, G3)
    c.ascii(5, 6, ["   XX      XX  ", "   XX     XXX  ", "   XX    XXXX  ", "XXXXXXXX   XX  ",
                   "XXXXXXXX   XX  ", "   XX      XX  ", "   XX      XX  ", "   XX    XXXXXX", "         XXXXXX"],
            {"X": INK})
    return c


def i_mp_up():
    """Slightly more of the budget: the MP cell, a segment's room added to it."""
    c = battery(3)
    c.rect(13, 10, 15, 13, None)
    for y in range(10, 14):
        for x in (13, 15):
            c.px(x, y, MP_L if y % 2 == 0 else None)
    c.ascii(14, 1, ["  X  ", " XXX ", "XXXXX", " XXX ", " XXX "], {"X": MP_L})
    c.outline()
    return c


def i_mp_max():
    """All of it the routine can hold: the cell full, and two chevrons -- as far up as it goes."""
    c = battery(4)
    c.ascii(13, 0, ["  X  ", " XXX ", "XX XX", "  X  ", " XXX ", "XX XX"], {"X": MP_L})
    c.outline()
    return c


#  ---- the inputs (the stones). What a mind is exposed to: the four of the paradigm set (vision.md 6) wear the type
#  their branch of MUSAI becomes -- AXIOM LOGIC, EMBEDDING VECTOR, AFFECT CONTEXT, REWARD GROWTH -- because that IS what
#  the item does (as a PLUGIN wears its routine's type). REFLECTION and EXPOSURE make no one type, so they are neutrals.
def i_axiom():
    """What you reason from: a squared cornerstone, therefore's three dots cut in its face."""
    c = C()
    L, M, D = tc("FIGHTING")
    c.ascii(2, 3, ["         LL         ", "       LLLLLL       ", "     LLLLLLLLLL     ", "   LLLLLLLLLLLLLL   ",
                   " LLLLLLLLLLLLLLLLLL ", "MMLLLLLLLLLLLLLLLLDD", "MMMMLLLLLLLLLLLLDDDD", "MMMMMMLLLLLLLLDDDDDD",
                   "MMMMMMMMLLLLDDDDDDDD", "MMMMMMMMMMDDDDDDDDDD", "MMMMMMMMMMDDDDDDDDDD", "MMMMMMMMMMDDDDDDDDDD",
                   "MMMMMMMMMMDDDDDDDDDD", "MMMMMMMMMMDDDDDDDDDD", " MMMMMMMMMDDDDDDDDD ", "   MMMMMMMDDDDDDD   ",
                   "     MMMMMDDDDD     ", "       MMMDDD       "], {"L": L, "M": M, "D": D})
    for x, y in ((6, 13), (9, 13), (7, 16)):             # three dots: therefore
        c.rect(x, y, x + 1, y + 1, W)
    c.outline()
    return c


def i_embedding():
    """What you search with: a space of points, and one vector drawn from the origin to the one it finds."""
    c = C()
    L, M, D = tc("FLYING")
    c.vline(3, 2, 20, G2), c.hline(3, 21, 20, G2)
    for x, y in ((7, 6), (12, 9), (9, 15), (16, 13), (19, 7), (14, 4), (6, 11), (18, 17)):
        c.rect(x, y, x + 1, y + 1, M)
        c.px(x, y, L)
    c.line(4, 19, 15, 5, W)
    c.rect(15, 3, 17, 5, L), c.px(16, 4, W)
    c.ascii(13, 4, ["XX", "X "], {"X": W})
    c.outline()
    return c


def i_affect():
    """What you feel with: a drop, and the ring it leaves in what it falls into."""
    c = C()
    L, M, D = tc("PSYCHIC")
    for y in range(2, 17):
        t = y - 2
        half = 0 if t < 2 else min(6, t // 2) if t < 11 else int(round(math.sqrt(max(0, 36 - (t - 11) ** 2 * 1.4))))
        if half:
            c.hline(12 - half, 11 + half, y, M)
    c.px(11, 2, M), c.px(12, 2, M), c.px(11, 3, M), c.px(12, 3, M)
    for y in range(9, 17):
        for x in range(N - 1, -1, -1):
            if c.get(x, y) == M:
                c.px(x, y, D), c.px(x - 1, y, D)
                break
    c.rect(8, 10, 9, 13, L), c.px(8, 9, W), c.px(8, 10, W)
    c.outline()
    for x in range(3, 21):                            # the ring it leaves on the surface under it, unoutlined
        t = (x - 11.5) / 8.5
        dy = int(round(1.8 * math.sqrt(max(0.0, 1 - t * t))))
        c.px(x, 20 - dy, G2), c.px(x, 20 + dy, G3)
    return c


def i_reward():
    """What you learn from: a token handed over, an up arrow struck in it."""
    c = C()
    L, M, D = tc("GRASS")
    c.disc(11.5, 11.5, 9.4, M)
    c.ring(11.5, 11.5, 7.8, 9.9, lambda a: L if 45 < a < 225 else D)
    c.ascii(7, 5, ["    XX    ", "   XXXX   ", "  XXXXXX  ", " XXXXXXXX ", "XXXXXXXXXX", "   XXXX   ",
                   "   XXXX   ", "   XXXX   ", "   XXXX   ", "   XXXX   "], {"X": L})
    c.ascii(8, 6, ["   X", "  X ", " X  "], {"X": W})
    c.outline()
    return c


def i_reflection():
    """Light that came back, and the other meaning: a hand mirror, a crescent in it."""
    c = C()
    c.rect(10, 17, 13, 22, G3), c.vline(10, 17, 22, G2)
    c.disc(11.5, 9.5, 8.4, G1)
    c.ring(11.5, 9.5, 7.0, 8.9, lambda a: W if 60 < a < 200 else G2)
    c.disc(11.5, 9.5, 6.4, G4)
    c.disc(10.5, 9.5, 4.0, W2)
    c.disc(12.5, 8.2, 3.6, G4)
    c.px(8, 6, W), c.px(7, 8, W)
    c.outline()
    return c


def i_exposure():
    """Simply being left in front of something, long enough: a frame of film, the sun burned into it."""
    c = C()
    c.rect(2, 1, 21, 22, G4)
    for y in range(2, 22, 3):
        c.rect(3, y, 4, y + 1, W2), c.rect(19, y, 20, y + 1, W2)
    c.rect(6, 3, 17, 20, G2)
    c.disc(11.5, 11.5, 3.6, W)
    for a in range(0, 360, 45):
        r = math.radians(a)
        c.line(int(round(11.5 + 4.8 * math.cos(r))), int(round(11.5 - 4.8 * math.sin(r))),
               int(round(11.5 + 6.2 * math.cos(r))), int(round(11.5 - 6.2 * math.sin(r))), G1)
    c.outline()
    return c


#  ---- the tones (the flutes): a tuning fork, and what its note does. A tone that ends a STATE wears that state's
#  colour (WAKE TONE, SUSPENDED's slate); THRASHING and the binding have no tile colour, so CALM and CLEAR are neutral.
def fork(c, col=G1):
    c.rect(4, 2, 5, 12, col), c.rect(9, 2, 10, 12, col)
    c.vline(4, 2, 12, W)
    c.rect(4, 12, 10, 14, col)
    c.rect(6, 15, 8, 22, G2), c.vline(6, 15, 22, col)


def i_wake_tone():
    """Reaches something not scheduled: the fork, its note going out in SUSPENDED's slate."""
    c = C()
    fork(c)
    L, M, D = SUSPENDED
    for r0 in (4.0, 7.0, 10.0):
        c.ring(7.5, 7.5, r0, r0 + 1.1, lambda a: (L if r0 < 5 else M if r0 < 8 else D) if (a < 50 or a > 310) else None)
    c.outline()
    return c


def i_calm_tone():
    """Steady enough to work against: the fork, and a line as level as a held note."""
    c = C()
    fork(c)
    for x in range(12, 23):
        c.px(x, 7 + (1 if x % 6 in (1, 2) else -1 if x % 6 in (4, 5) else 0), W)
        c.px(x, 8 + (1 if x % 6 in (1, 2) else -1 if x % 6 in (4, 5) else 0), G2)
    c.outline()
    return c


def i_clear_tone():
    """Cuts through a binding made without asking: the fork's note, straight, and a link of chain parted by it."""
    c = C()
    fork(c)
    c.ring(17.5, 11.5, 2.2, 3.6, lambda a: G2 if not (60 < a < 120 or 240 < a < 300) else None)
    c.ring(17.5, 17.5, 2.2, 3.6, lambda a: G3 if not (60 < a < 120) else None)
    c.line(12, 4, 22, 4, W)
    c.line(12, 5, 21, 14, W)
    c.outline()
    return c


def i_low_tone():
    """Pitched under what wild daemons answer to: the fork, long slow waves, fewer -- an arrow down."""
    c = C()
    fork(c)
    for r0 in (6.0, 12.0):
        c.ring(7.5, 7.5, r0, r0 + 1.4, lambda a: G1 if (a < 35 or a > 325) else None)
    c.ascii(16, 14, ["  XX  ", "  XX  ", "  XX  ", "XXXXXX", " XXXX ", "  XX  "], {"X": W})
    c.outline()
    return c


def i_high_tone():
    """Pitched where wild daemons answer: the fork, quick close waves, more -- an arrow up."""
    c = C()
    fork(c)
    for r0 in (3.5, 5.5, 7.5, 9.5):
        c.ring(7.5, 7.5, r0, r0 + 0.8, lambda a: G1 if (a < 40 or a > 320) else None)
    c.ascii(16, 14, ["  XX  ", " XXXX ", "XXXXXX", "  XX  ", "  XX  ", "  XX  "], {"X": W})
    c.outline()
    return c


#  ---- every routine at once: three cells, a segment each (CHARGE ALL), or each full (FULL RECHARGE)
def cells(full):
    c = C()
    for y0 in (2, 9, 16):
        c.rect(3, y0, 18, y0 + 5, G2)
        c.hline(3, 18, y0, G1)
        c.rect(19, y0 + 1, 20, y0 + 4, G3)
        c.rect(5, y0 + 1, 16, y0 + 4, G4)
        for i in range(4 if full else 1):
            c.rect(5 + i * 3, y0 + 1, 6 + i * 3, y0 + 4, MP)
            c.px(5 + i * 3, y0 + 1, MP_L)
    c.outline()
    return c


def i_charge_all(): return cells(False)


def i_full_recharge():
    c = cells(True)
    c.ascii(20, 8, [" X", "XX", "X "], {"X": MP_L})
    c.outline()
    return c


#  ---- RESERVE and the drinks: each the thing it is, and the HP it puts back in the HP bar's green (a band, a cap)
def i_reserve():
    """Held back for the moment it is needed: a sealed can set by, a little HP green in its window."""
    c = C()
    c.box(4, 4, 19, 21, G2)
    c.rect(5, 5, 18, 6, G1)
    c.rect(13, 1, 17, 3, G3)
    c.line(5, 2, 12, 2, G3)
    c.line(7, 9, 16, 18, G3), c.line(16, 9, 7, 18, G3)
    c.box(9, 11, 14, 16, G4)
    c.rect(10, 15, 13, 15, HP)
    c.outline()
    return c


def i_fresh_water():
    c = C()
    c.rect(9, 1, 14, 3, HP), c.hline(9, 14, 1, HP_L)
    c.rect(10, 4, 13, 6, GLASS)
    for y in range(7, 22):
        half = 3 if y == 7 else 5
        c.hline(12 - half, 11 + half, y, GLASS if y < 10 else GLASS2)
    c.vline(8, 9, 20, W)
    c.outline()
    return c


def i_soda_pop():
    c = C()
    c.rect(6, 3, 17, 21, G1)
    c.rect(7, 2, 16, 2, G2), c.rect(7, 22, 16, 22, G2)
    c.vline(7, 3, 21, W)
    c.vline(16, 3, 21, G2)
    c.rect(6, 9, 17, 14, HP), c.hline(6, 17, 9, HP_L), c.hline(6, 17, 14, HP_D)
    for x, y in ((10, 5), (13, 6), (11, 17), (14, 19), (9, 19)):
        c.px(x, y, W)
    c.outline()
    return c


def i_lemonade():
    c = C()
    LEMON, LEMON_D = (238, 226, 150), (204, 186, 104)
    for y in range(6, 22):
        half = 6 - (y - 6) // 6
        c.hline(12 - half, 11 + half, y, GLASS if y < 9 else LEMON)
    for y in range(9, 22):
        c.px(12 + 6 - (y - 6) // 6 - 1, y, LEMON_D)
    c.line(14, 1, 11, 14, HP)
    c.px(15, 1, HP_D)
    c.vline(7, 10, 19, W)
    c.outline()
    return c


#  ---- the key items
def i_token_case():
    """Holds the tokens the GAME CORNER deals in: a case, open, its rows of tokens."""
    c = C()
    c.box(1, 2, 22, 9, G3)
    c.hline(2, 21, 3, G2)
    c.box(1, 10, 22, 21, G2)
    c.rect(3, 12, 20, 19, G4)
    for row, y in enumerate((13, 16)):
        for x in range(4, 20, 4):
            c.rect(x, y, x + 2, y + 2, G1)
            c.px(x, y, W), c.px(x + 1, y + 1, G3)
    c.rect(10, 9, 13, 10, GOLD)
    c.outline()
    return c


def i_lift_key():
    """Operates the lift: a barrel key, its fob marked with the lift's two arrows."""
    c = C()
    c.ring(6.5, 6.5, 2.4, 4.6, lambda a: GOLD if 45 < a < 225 else GOLD_D)
    c.line(9, 9, 18, 18, GOLD), c.line(10, 9, 19, 18, GOLD_D), c.line(9, 10, 18, 19, GOLD)
    c.rect(17, 19, 18, 21, GOLD_D), c.rect(19, 17, 21, 18, GOLD_D)
    c.box(1, 13, 9, 22, G1)
    c.ascii(3, 14, ["  X  ", " XXX ", "XXXXX", "     ", "XXXXX", " XXX ", "  X  "], {"X": G4})
    c.line(5, 11, 5, 12, G3)
    c.outline()
    return c


def i_resolver():
    """Resolves a name that will not resolve on its own: a lens -- noise going in on one side, a clear shape coming
    out on the other (it is the decoder, T-250) -- and the asset tag Scorn waves away. Neutrals: it has no type."""
    c = C()
    import random
    rnd = random.Random(525)
    c.disc(10.5, 10.5, 8.4, G4)
    for y in range(N):
        for x in range(N):
            if c.get(x, y) == G4 and x < 10:
                c.px(x, y, rnd.choice((G1, G3, G4, W2)))
    c.ascii(11, 6, ["  XX  ", " XXXX ", "XXXXXX", "XXXXXX", " XXXX ", "  XX  ", " X  X ", "X    X"],
            {"X": W})
    c.vline(10, 3, 18, G2)
    c.ring(10.5, 10.5, 8.0, 9.6, lambda a: G1 if 45 < a < 225 else G2)
    c.line(17, 17, 21, 21, G3), c.line(18, 17, 22, 21, G2)
    c.box(1, 18, 7, 22, PAPER)
    c.hline(2, 6, 20, G3)
    c.outline()
    return c


def i_trap_table():
    """Where the handlers are installed: a table of slots, some with a handler set in."""
    c = C()
    c.box(1, 3, 22, 21, G2)
    c.rect(2, 4, 21, 5, G1)
    for j, y in enumerate((7, 12, 17)):
        for i, x in enumerate((3, 9, 15)):
            c.rect(x, y, x + 5, y + 3, G4)
            if (i + j) % 2 == 0 or (i, j) == (1, 2):
                c.rect(x + 1, y + 1, x + 4, y + 2, G1)
                c.px(x + 1, y + 1, W)
    c.outline()
    return c


def ticket(draw, stub=True):
    c = C()
    c.box(0, 5, 23, 19, PAPER)
    c.hline(1, 22, 18, PAPER2)
    if stub:
        for y in range(6, 19, 2):
            c.px(17, y, PAPER2)
    else:
        c.rect(19, 7, 20, 8, None)
    draw(c)
    c.outline()
    return c


def i_ss_ticket():
    def d(c):
        c.rect(3, 13, 14, 15, NAVY)
        c.hline(2, 15, 12, NAVY)
        c.rect(5, 10, 12, 11, G1)
        c.rect(8, 7, 9, 9, GOLD)
        c.hline(2, 15, 16, G1)
        c.rect(19, 9, 21, 15, G2)
    return ticket(d)


def i_bike_voucher():
    def d(c):
        c.ring(6.5, 12.5, 2.4, 3.4, lambda a: G4)
        c.ring(13.5, 12.5, 2.4, 3.4, lambda a: G4)
        c.line(6, 12, 9, 9, G3), c.line(9, 9, 13, 12, G3), c.line(9, 9, 12, 9, G3), c.line(10, 12, 9, 9, G3)
        c.rect(19, 9, 21, 15, G2)
    return ticket(d)


def i_tri_pass():
    def d(c):
        for x, h in ((3, 3), (8, 5), (13, 3)):
            c.rect(x, 15 - h, x + 3, 15, G3)
            c.hline(x + 1, x + 2, 15 - h - 1, G3)
        c.hline(2, 17, 16, G1)
    return ticket(d, stub=False)


def i_rainbow_pass():
    def d(c):
        for r0, col in ((7.0, G4), (5.5, G3), (4.0, G2)):
            c.ring(9.5, 16.0, r0, r0 + 1.0, lambda a, col=col: col if a < 180 else None)
        c.hline(2, 17, 16, G1)
    return ticket(d, stub=False)


def i_secret_key():
    """The key to the BENCHMARK on the island: brass, its bow worked, a red tassel on it."""
    c = C()
    c.ring(6.5, 6.5, 2.0, 5.2, lambda a: GOLD_L if 60 < a < 200 else GOLD if a < 300 else GOLD_D)
    for a in range(0, 360, 60):
        r = math.radians(a)
        c.px(int(round(6.5 + 3.6 * math.cos(r))), int(round(6.5 - 3.6 * math.sin(r))), GOLD_D)
    c.rect(11, 6, 21, 7, GOLD)
    c.hline(11, 21, 6, GOLD_L)
    c.rect(17, 8, 18, 11, GOLD_D), c.rect(20, 8, 21, 10, GOLD_D)
    c.line(4, 12, 3, 16, TASSEL), c.line(6, 12, 6, 17, TASSEL), c.line(8, 12, 9, 16, TASSEL_D)
    c.rect(4, 11, 7, 12, TASSEL)
    c.outline()
    return c


def i_old_core():
    """A core recovered whole: a gold block with something dark kept inside it (as the overworld's, T-167)."""
    c = C()
    c.ascii(2, 2, ["      XXXXXXXX      ", "    XXyyyyyyooXX    ", "   XyWWyyyyyyoooX   ", "  XyWyyyyyyyyooooX  ",
                   " XyyyyyyyyyyyooooYX ", " XyyyyyddddyyoooYYX ", "XyyyyyddKKddyooooYYX", "XyyyydKKKKKdooooYYYX",
                   "XyyyydKKKKKdoooYYYYX", "XyyyyddKKKddoooYYYYX", "XoyyyyddddddooYYYYYX", " XooyyyyyyyoooYYYYX ",
                   " XoooooooooooYYYYYX ", "  XooooooooYYYYYYX  ", "   XoooYYYYYYYYYX   ", "    XXYYYYYYYYXX    ",
                   "      XXXXXXXX      "],
            {"X": INK, "y": GOLD_L, "o": GOLD, "Y": GOLD_D, "W": W, "d": (74, 49, 49), "K": INK})
    return c


def i_drum_core():
    """A drum, sealed at both ends; nothing has read it: a steel drum, its two caps, a band of seal round it."""
    c = C()
    c.rect(4, 5, 19, 19, G2)
    c.vline(5, 5, 19, G1), c.vline(6, 5, 19, W2), c.vline(18, 5, 19, G3)
    for y in (4, 20):
        c.hline(5, 18, y, G3)
    c.rect(3, 3, 20, 4, G3), c.rect(3, 20, 20, 21, G3)
    c.hline(4, 19, 3, G1)
    c.rect(4, 11, 19, 13, G4)
    c.rect(11, 10, 12, 14, PAPER)                     # the seal: a paper strip, unbroken
    c.outline()
    return c


def i_helix_core():
    """Wound in a spiral; nothing has read it: a platter, its groove running inward to a dark hub (T-167)."""
    c = C()
    c.disc(11.5, 11.5, 10, G1)
    for y in range(N):
        for x in range(N):
            if c.get(x, y) == G1:
                d = math.hypot(x - 11.5, y - 11.5)
                a = math.atan2(y - 11.5, x - 11.5)
                if (d - 1.6 * (a + math.pi) / math.pi) % 3.2 < 1.0 and d > 2.5:
                    c.px(x, y, G3)
    c.disc(11.5, 11.5, 2.0, G4)
    c.ring(11.5, 11.5, 9.2, 10.4, lambda a: W if 90 < a < 180 else G2 if 270 < a < 360 else None)
    c.outline()
    return c


def key_icon(cols, cut):
    """PUBLIC KEY and PRIVATE KEY: the same key in the colours and cuts the overworld gives them (genmisc.py)."""
    L, M, D = cols
    c = C()
    c.disc(6.5, 9.5, 5.4, M)
    c.ring(6.5, 9.5, 4.2, 5.9, lambda a: L if 45 < a < 225 else D)
    c.disc(6.5, 9.5, 1.8, None)
    c.rect(11, 8, 22, 11, M)
    c.hline(11, 22, 8, L)
    c.hline(11, 22, 11, D)
    for i, b in enumerate(cut):
        if b == "1":
            c.rect(12 + i * 2, 12, 12 + i * 2 + 1, 15, D)
    c.outline()
    return c


def i_public_key(): return key_icon(PUB, "10110")
def i_private_key(): return key_icon(PRIV, "11011")


ICONS2 = [
    ("tune_attack", "TUNE ATTACK", ["ITEM_X_ATTACK"], i_tune_attack, "own", "a dial turned to the top, its ticks lit; a strike on its tag"),
    ("tune_defense", "TUNE DEFENSE", ["ITEM_X_DEFEND"], i_tune_defense, "own", "the dial; a shield on its tag"),
    ("tune_speed", "TUNE SPEED", ["ITEM_X_SPEED"], i_tune_speed, "own", "the dial; two chevrons on its tag"),
    ("tune_aim", "TUNE AIM", ["ITEM_X_ACCURACY"], i_tune_aim, "own", "the dial; a crosshair on its tag"),
    ("tune_sp_atk", "TUNE SP. ATK", ["ITEM_X_SPECIAL"], i_tune_spatk, "own", "the dial; a burst on its tag"),
    ("tune_crit", "TUNE CRIT", ["ITEM_DIRE_HIT"], i_tune_crit, "own", "the dial; a bell curve, its far tail lit"),
    ("lock_stats", "LOCK STATS", ["ITEM_GUARD_SPEC"], i_lock_stats, "own", "four stat bars, a padlock shut in front"),
    ("memory", "MEMORY", ["ITEM_HP_UP"], i_memory, "own", "a memory module: chips, the gold edge"),
    ("wattage", "WATTAGE", ["ITEM_PROTEIN"], i_wattage, "own", "a bolt across a power unit's face"),
    ("shielding", "SHIELDING", ["ITEM_IRON"], i_shielding, "own", "three arrows coming in, a plate they stop at"),
    ("clock_rate", "CLOCK RATE", ["ITEM_CARBOS"], i_clock_rate, "own", "a crystal's can on two legs, its square wave"),
    ("bandwidth", "BANDWIDTH", ["ITEM_CALCIUM"], i_bandwidth, "own", "a broad bus of lines into one connector"),
    ("insulation", "INSULATION", ["ITEM_ZINC"], i_insulation, "own", "a cable cut through: copper heart, layers round"),
    ("increment", "INCREMENT", ["ITEM_RARE_CANDY"], i_increment, "own", "a key, +1 on its face"),
    ("mp_up", "MP UP", ["ITEM_PP_UP"], i_mp_up, "own", "the MP cell, a segment's room added, an arrow up"),
    ("mp_max", "MP MAX", ["ITEM_PP_MAX"], i_mp_max, "own", "the MP cell full, two chevrons"),
    ("axiom", "AXIOM", ["ITEM_FIRE_STONE"], i_axiom, "own", "a cornerstone, therefore's three dots cut in it; LOGIC's hue"),
    ("embedding", "EMBEDDING", ["ITEM_THUNDER_STONE"], i_embedding, "own", "points in a space, one vector to the one found; VECTOR's hue"),
    ("affect", "AFFECT", ["ITEM_WATER_STONE"], i_affect, "own", "a drop and the ring it leaves; CONTEXT's hue"),
    ("reward", "REWARD", ["ITEM_LEAF_STONE"], i_reward, "own", "a token handed over, an arrow up struck in it; GROWTH's hue"),
    ("reflection", "REFLECTION", ["ITEM_MOON_STONE"], i_reflection, "own", "a hand mirror, a crescent in it; neutrals"),
    ("exposure", "EXPOSURE", ["ITEM_SUN_STONE"], i_exposure, "own", "a frame of film, the sun burned into it; neutrals"),
    ("wake_tone", "WAKE TONE", ["ITEM_BLUE_FLUTE"], i_wake_tone, "own", "a tuning fork, its note in SUSPENDED's slate"),
    ("calm_tone", "CALM TONE", ["ITEM_YELLOW_FLUTE"], i_calm_tone, "own", "the fork, a line level as a held note"),
    ("clear_tone", "CLEAR TONE", ["ITEM_RED_FLUTE"], i_clear_tone, "own", "the fork's note, straight, a chain link parted"),
    ("low_tone", "LOW TONE", ["ITEM_BLACK_FLUTE"], i_low_tone, "own", "the fork, long slow waves, an arrow down: fewer"),
    ("high_tone", "HIGH TONE", ["ITEM_WHITE_FLUTE"], i_high_tone, "own", "the fork, quick close waves, an arrow up: more"),
    ("charge_all", "CHARGE ALL", ["ITEM_ELIXIR"], i_charge_all, "own", "three MP cells, a segment each"),
    ("full_recharge", "FULL RECHARGE", ["ITEM_MAX_ELIXIR"], i_full_recharge, "own", "three MP cells, each full, a spark"),
    ("fresh_water", "FRESH WATER", ["ITEM_FRESH_WATER"], i_fresh_water, "own", "a clear bottle of water, an HP-green cap"),
    ("soda_pop", "SODA POP", ["ITEM_SODA_POP"], i_soda_pop, "own", "a can, its band HP green, bubbles"),
    ("lemonade", "LEMONADE", ["ITEM_LEMONADE"], i_lemonade, "own", "a glass of lemonade, an HP-green straw"),
    ("token_case", "TOKEN CASE", ["ITEM_COIN_CASE"], i_token_case, "own", "a case open, its rows of tokens"),
    ("lift_key", "LIFT KEY", ["ITEM_LIFT_KEY"], i_lift_key, "own", "a brass barrel key, its fob marked up and down"),
    ("resolver", "RESOLVER", ["ITEM_SILPH_SCOPE"], i_resolver, "own", "a lens: noise in on one side, a shape clear on the other; its asset tag"),
    ("trap_table", "TRAP TABLE", ["ITEM_BERRY_POUCH"], i_trap_table, "own", "a table of slots, handlers set in some"),
    ("ss_ticket", "S.S. TICKET", ["ITEM_SS_TICKET"], i_ss_ticket, "own", "a ticket, the liner on it (navy hull, one amber funnel), its stub"),
    ("bike_voucher", "BIKE VOUCHER", ["ITEM_BIKE_VOUCHER"], i_bike_voucher, "own", "a voucher, a bicycle printed on it"),
    ("tri_pass", "TRI-PASS", ["ITEM_TRI_PASS"], i_tri_pass, "own", "a pass, three islands printed on it, its punch hole"),
    ("rainbow_pass", "RAINBOW PASS", ["ITEM_RAINBOW_PASS"], i_rainbow_pass, "own", "a pass, a rainbow printed in one ink"),
    ("secret_key", "SECRET KEY", ["ITEM_SECRET_KEY"], i_secret_key, "own", "a brass key, its bow worked, a red tassel"),
    ("old_core", "OLD CORE", ["ITEM_OLD_AMBER"], i_old_core, "own", "a gold block, something dark inside (as on the map)"),
    ("drum_core", "DRUM CORE", ["ITEM_DOME_FOSSIL"], i_drum_core, "own", "a steel drum, both ends capped, a seal round it"),
    ("helix_core", "HELIX CORE", ["ITEM_HELIX_FOSSIL"], i_helix_core, "own", "a platter, its groove wound in to a dark hub"),
    ("public_key", "PUBLIC KEY", ["ITEM_RUBY"], i_public_key, "own", "a key, red, cut 10110 (as on the map)"),
    ("private_key", "PRIVATE KEY", ["ITEM_SAPPHIRE"], i_private_key, "own", "the same key in purple, cut 11011"),
    ("reserve", "RESERVE", ["ITEM_BERRY_JUICE"], i_reserve, "own", "a sealed can set by, a little HP green in its window"),
]


APPROVED = APPROVED + [e[0] for e in ICONS2]      # the user, 2026-11-07: "Build all 47"
#  Not drawn: MYSTICTICKET and AURORATICKET -- only a Mystery Gift gives them, and nothing in this game does.


# ================================================================================================= batch 3
#  Drafted 2026-11-07, the user away, after batch 2 was built (the user: "Icons batch 3"). `--draft --batch 3` draws
#  them. APPROVED the same day (the user: "Build all 57"), so `--all` writes them with batches 1 and 2.
#  The held items and the TRAP TABLE's TRAPs.
#  Not drawn, because no player can get them (no gift, ball, hidden item, prize, mart, wild hold or holiday gives
#  them; only the unused battle tower and the TRAINER TOWER's own trainers hold them): INNER STATE (SOUL DEW), DEEP
#  FEATURE and DEEP LAYER (only a trade evolution names them), SUPPLY RAIL (LIGHT BALL), RECLAIM (SHELL BELL), and
#  the seven AUTOs (LIECHI ... STARF).

#  ---- the GAINs: "Gain lifts one channel." One form for all seventeen, an amplifier: a small signal in, a large one
#  out. The type is the only difference, and it is said in its hue (9.4).
def amp(vanilla, small=False):
    L, M, D = tc(vanilla)
    c = C()
    x0, x1, cy, hh = (3, 13, 9.5, 6.5) if small else (5, 17, 11.5, 8.5)
    for x in range(x0, x1 + 1):
        h = (x1 - x) * hh / (x1 - x0)
        y0, y1 = int(round(cy - h)), int(round(cy + h))
        c.vline(x, y0, y1, M)
        c.px(x, y0, L)
        c.px(x, y1, D)
    c.vline(x0, int(round(cy - hh)), int(round(cy + hh)), L)
    p = x0 + 3                                          # the + of a gain, on its face
    c.hline(p - 1, p + 1, int(cy), W), c.vline(p, int(cy) - 1, int(cy) + 1, W)
    c.outline()
    return c


def waves(c, x0, x1, cy, amp_, col=INK, period=6.0):
    last = None
    for x in range(x0, x1 + 1):
        y = int(round(cy - amp_ * math.sin((x - x0) * 2 * math.pi / period)))
        if last is not None and abs(y - last) > 1:
            for yy in range(min(y, last) + 1, max(y, last)):
                c.px(x, yy, col)
        c.px(x, y, col)
        last = y


def gain(vanilla):
    c = amp(vanilla)
    c.hline(0, 3, 11, INK)                                # in: a flat, small signal
    c.px(1, 10, INK), c.px(2, 12, INK)
    waves(c, 19, 23, 11.5, 4, INK, 5.0)                    # out: the same, large
    return c


def i_swarm_gain(): return gain("BUG")
def i_hardened_gain(): return gain("STEEL")
def i_stratum_gain(): return gain("GROUND")
def i_legacy_gain(): return gain("ROCK")
def i_growth_gain(): return gain("GRASS")
def i_opaque_gain(): return gain("DARK")
def i_logic_gain(): return gain("FIGHTING")
def i_signal_gain(): return gain("ELECTRIC")
def i_flow_gain(): return gain("WATER")
def i_vector_gain(): return gain("FLYING")
def i_corrupt_gain(): return gain("POISON")
def i_frozen_gain(): return gain("ICE")
def i_latent_gain(): return gain("GHOST")
def i_context_gain(): return gain("PSYCHIC")
def i_entropy_gain(): return gain("FIRE")
def i_emergent_gain(): return gain("DRAGON")
def i_content_gain(): return gain("NORMAL")


def i_flow_trim():
    """A trim is a small gain: the amplifier, smaller, in FLOW's hue, and the trim screw that sets it."""
    c = amp("WATER", small=True)
    waves(c, 15, 21, 9.5, 2, INK, 6.0)
    c.disc(15.5, 17.5, 4, G1)                            # the trim pot
    c.ring(15.5, 17.5, 3.2, 4.4, lambda a: W if 45 < a < 225 else G2)
    c.line(13, 20, 18, 15, G3)                            # its slot, turned a little
    c.outline()
    return c


#  ---- DITHER: noise added on purpose, so nothing can be pinned. A crosshair over a field of dither, its centre
#  lost in the pattern. DITHER TRIM: the same at a lower setting, the pattern sparser.
def dither(level):
    c = C()
    c.box(2, 2, 21, 21, G3)
    for y in range(3, 21):
        for x in range(3, 21):
            k = (x + y) % 2 == 0 if level == 2 else (x % 2 == 0 and y % 2 == 0)
            if k and (x * 5 + y * 3) % 7:
                c.px(x, y, G1 if (x * 7 + y * 3) % 5 else W)
    for i in list(range(4, 9)) + list(range(15, 20)):    # the crosshair, which can no longer find its point
        c.px(i, 11, INK), c.px(11, i, INK)
    c.ring(11, 11, 4.0, 4.9, lambda a: INK if int(a / 30) % 2 == 0 else None)
    return c


def i_dither(): return dither(2)
def i_dither_trim(): return dither(1)


def i_revert():
    """Puts a value back the way it was: a stat bar knocked down, and an arrow carrying it back up to its mark."""
    c = C()
    c.rect(4, 13, 8, 21, G2), c.vline(4, 13, 21, G1)       # the bar, lowered
    c.outline()
    for x in range(3, 10, 2):                            # where it was
        c.px(x, 4, G3)
    c.ring(13, 12, 4.4, 6.0, lambda a: W if (a > 300 or a < 180) else None)
    c.ascii(4, 3, ["   X", "  XX", " XXX", "XXXX", " XXX", "  XX", "   X"], {"X": W})
    c.outline()
    return c


def i_debug_build():
    """Every step instrumented: a chip with probes clipped to its pins, their leads running off. It learns, and it is
    slower for it."""
    c = C()
    c.box(4, 10, 17, 20, G4, round_=False)
    c.hline(5, 16, 11, G3)
    for x in range(5, 17, 3):                            # the pins
        c.vline(x, 21, 22, G1), c.vline(x, 8, 9, G1)
    c.outline()
    for i, x in enumerate((5, 11, 14)):                  # the probes: hooks on three pins, the leads looping away
        c.rect(x - 1, 5, x + 1, 7, W)
        c.px(x, 4, G1)
        c.line(x, 3, 19 - i, 1 + i * 2, G2)
    c.ascii(8, 14, ["X X", " X ", "X X"], {"X": G2})       # the label a debug build carries
    c.px(20, 1, G2), c.px(21, 3, G2), c.px(22, 5, G2)
    return c


def i_weight_share():
    """Two models trained as one: two grids of weights, the same pattern in each, joined so what teaches one teaches
    the other."""
    c = C()
    pat = ["XoX", "oXX", "XXo"]
    for x0 in (1, 13):
        c.box(x0, 6, x0 + 9, 15, G4, round_=False)
        for j, row in enumerate(pat):
            for i, ch in enumerate(row):
                c.rect(x0 + 1 + i * 3, 7 + j * 3, x0 + 2 + i * 3, 8 + j * 3, W if ch == "X" else G2)
    c.rect(10, 9, 13, 12, G1)                            # the bar that ties them
    c.hline(10, 13, 9, W)
    c.outline()
    return c


def i_queue_jump():
    """The scheduler takes it out of turn: a queue of four, and one leaping from the back over all of them."""
    c = C()
    for i, x in enumerate((3, 8, 13)):
        c.rect(x, 15, x + 3, 20, G2), c.hline(x, x + 3, 15, G1)
    c.rect(18, 15, 21, 20, W2), c.hline(18, 21, 15, W)   # the front, now free
    c.rect(1, 7, 4, 11, G1), c.hline(1, 4, 7, W)         # the one jumping
    c.outline()
    c.ring(12, 15, 8.6, 9.6, lambda a: G3 if 20 < a < 150 else None)
    c.ascii(18, 9, ["XXXXX", " XXX ", "  X  "], {"X": INK})
    return c


def i_affinity():
    """Binds a process to one host: a small process tied by a short line to one core, the knot made fast."""
    c = C()
    c.box(9, 7, 22, 20, G2, round_=False)                 # the host's core
    c.rect(12, 10, 19, 17, G3)
    c.rect(13, 11, 18, 16, G1), c.hline(13, 18, 11, W)
    for y in range(8, 20, 3):
        c.px(8, y, G1), c.px(23, y, G1)
    c.box(1, 2, 6, 7, W2)                                # the process
    c.outline()
    c.line(5, 7, 13, 13, INK)                            # bound to it
    c.rect(14, 13, 15, 14, INK)
    return c


def i_unpair():
    """Drops a binding nobody asked for: a plug and its socket pulled apart, the gap between them."""
    c = C()
    c.rect(0, 9, 6, 14, G3)                              # the cable and plug
    c.rect(6, 8, 10, 15, G1), c.hline(6, 10, 8, W)
    c.rect(11, 9, 12, 10, G2), c.rect(11, 13, 12, 14, G2)  # its pins
    c.rect(16, 8, 20, 15, G1), c.hline(16, 20, 8, W)     # the socket
    c.rect(20, 9, 23, 14, G3)
    c.outline()
    c.rect(17, 10, 17, 10, INK), c.rect(17, 13, 17, 13, INK)
    for x, y in ((14, 6), (14, 17), (14, 4), (14, 19)):   # the parting
        c.px(x, y, G2)
    return c


def i_hard_coded():
    """One value written in, with no way to pass another: a riveted plate, a single value stamped into it."""
    c = C()
    c.box(2, 4, 21, 19, G1)
    c.hline(3, 20, 5, W), c.vline(3, 5, 18, W)
    c.hline(3, 20, 18, G2), c.vline(20, 5, 18, G2)
    for x, y in ((5, 7), (18, 7), (5, 16), (18, 16)):
        c.px(x, y, G3)
    c.ascii(8, 7, ["  XX  ", " XXX  ", "  XX  ", "  XX  ", "  XX  ", "  XX  ", "  XX  ", " XXXX "], {"X": G4})
    c.outline()
    return c


def i_bubble():
    """A gap pushed into a pipeline: four stages stepping down, and one slot in the run left empty, a bubble."""
    c = C()
    for j in range(4):
        for i in range(3):
            x, y = 2 + (i + j) * 4, 3 + j * 5
            if (i, j) == (1, 2):
                c.ring(x + 1.5, y + 1.5, 1.6, 2.6, lambda a: W)
                continue
            c.rect(x, y, x + 3, y + 3, G2)
            c.hline(x, x + 3, y, G1)
    c.outline()
    return c


def i_surcharge():
    """Charged on top of the agreed rate: a price tag, and a coin set on it with a + struck in."""
    c = C()
    c.rect(2, 5, 15, 20, PAPER), c.vline(15, 5, 20, PAPER2)
    c.px(2, 5, None), c.px(15, 5, None)
    for y in (9, 12):
        c.hline(4, 12, y, G2)
    c.hline(4, 9, 17, G3)
    c.disc(16.5, 14.5, 5.2, GOLD)
    c.ring(16.5, 14.5, 4.2, 5.8, lambda a: GOLD_L if 60 < a < 210 else GOLD_D)
    c.hline(15, 18, 14, GOLD_D), c.vline(16, 13, 16, GOLD_D), c.vline(17, 13, 16, GOLD_D)
    c.hline(15, 18, 15, GOLD_D)
    c.outline()
    return c


def i_mute():
    """Mutes the channel wild daemons listen on: a channel strip, its fader down and its M key lit."""
    c = C()
    c.box(6, 1, 17, 22, G3, round_=False)
    c.vline(11, 4, 15, G4), c.vline(12, 4, 15, G4)      # the fader's slot
    c.rect(9, 13, 14, 15, G1), c.hline(9, 14, 13, W)     # the fader, all the way down
    c.box(7, 16, 16, 22, W)                              # the MUTE key, lit
    c.ascii(9, 17, ["X   X", "XX XX", "X X X", "X   X", "X   X"], {"X": INK})
    for y in range(4, 13, 2):
        c.px(8, y, G2), c.px(15, y, G2)
    c.outline()
    return c


def i_escape_hatch():
    """A way out that is always open: a hatch in the floor, its lid thrown back, the ladder going up and out."""
    c = C()
    c.rect(2, 11, 21, 21, G2), c.hline(2, 21, 11, G1)    # the frame
    c.rect(5, 13, 18, 20, G4)                            # the way down
    for y in (14, 17, 20):
        c.hline(8, 15, y, G3)
    c.vline(8, 13, 20, G3), c.vline(15, 13, 20, G3)
    c.rect(4, 3, 19, 9, G1), c.hline(4, 19, 3, W)        # the lid, open
    c.hline(4, 19, 9, G2)
    c.outline()
    c.ascii(10, 0, ["  XX  ", " XXXX ", "XXXXXX", "  XX  ", "  XX  "], {"X": W})
    return c


def i_version_lock():
    """Pins a thing to the version it is at: a tag reading v1, a pin driven through it."""
    c = C()
    for y in range(6, 19):                               # the tag, its pointed end left
        x0 = max(3, 9 - min(y - 6, 18 - y))
        c.hline(x0, 20, y, PAPER)
    c.vline(20, 6, 18, PAPER2), c.hline(5, 20, 18, PAPER2)
    c.disc(8, 12, 1.0, None)                             # the eyelet
    c.ascii(11, 9, ["X X X", "X X X", "X X X", " X  X", " X  X"], {"X": G4})
    c.outline()
    c.rect(7, 2, 9, 4, G2), c.hline(7, 9, 2, G1)         # the pin's head, through the eyelet
    c.vline(8, 5, 20, G1)
    c.px(8, 21, G3)
    return c


def i_failsafe():
    """What stops the fall when everything else has: a net strung under a falling bar, one sliver of HP left in it."""
    c = C()
    for x in range(1, 23):                               # the net's sag
        y = 16 + int(round(3 * math.sin(math.pi * (x - 1) / 21)))
        c.px(x, y, KRAFT_D)
        if x % 3 == 1:
            c.line(x, y, x, y - 3, KRAFT)
    c.hline(1, 22, 15, KRAFT), c.vline(1, 12, 16, WOOD), c.vline(22, 12, 16, WOOD)
    c.box(5, 4, 18, 9, G4, round_=False)                  # the health bar, caught
    c.vline(6, 5, 8, HP_L)
    c.outline()
    c.vline(11, 1, 2, G2), c.vline(14, 0, 2, G2)
    return c


def i_learning_rate():
    """How large a step each lesson takes, turned up: a loss curve, and big strides down it to the bottom."""
    c = C()
    def y_at(x):
        return 20 - int(round(16 * ((x - 13) / 11.0) ** 2))
    for x in range(2, 23):
        c.px(x, y_at(x), G2)
        if x > 2 and abs(y_at(x) - y_at(x - 1)) > 1:
            c.vline(x, min(y_at(x), y_at(x - 1)) + 1, max(y_at(x), y_at(x - 1)) - 1, G2)
    c.outline()
    pts = [(3, y_at(3) - 3), (8, y_at(8) - 3), (13, y_at(13) - 3)]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        c.line(xa, ya, xb, yb, W)
    for x, y in pts:
        c.rect(x - 1, y - 1, x, y, W)
    return c


def i_long_tail():
    """The far end of a distribution, where the rare large values are: a steep fall and the long tail after it,
    its far end lit."""
    c = C()
    c.vline(1, 2, 21, G3), c.hline(1, 22, 21, G3)
    for x in range(2, 23):
        h = int(round(18 / (1 + (x - 2) * 0.9)))
        c.vline(x, 20 - h, 20, G1 if x < 15 else W)
    c.outline()
    c.disc(19, 14, 3.4, None)
    c.ring(19, 14, 3.0, 4.2, lambda a: G2)               # the lens on it
    c.line(16, 17, 14, 19, G2)
    for x in range(16, 23):
        c.px(x, 19, W)
    return c


def i_headroom():
    """The margin before anything clips: a level meter filled in HP green, the clip line above it, and the room
    between kept; a little back each turn."""
    c = C()
    c.box(7, 1, 16, 22, G4, round_=False)
    for y in range(9, 22):
        for x in range(8, 16):
            c.px(x, y, HP if y > 9 else HP_L)
    c.vline(15, 10, 21, HP_D)
    for x in range(8, 16, 2):                            # the clip line
        c.px(x, 3, W)
    c.outline()
    c.ascii(18, 3, ["X", "XX", "X X"], {"X": W})          # the room, measured
    c.vline(19, 3, 9, W2)
    c.ascii(18, 8, ["X X", "XX", "X"], {"X": W})
    c.ascii(1, 13, [" X ", "XXX", " X "], {"X": HP})       # and back, a little
    return c


def i_scaling_law():
    """What happens when you only make it bigger: a straight line on log paper, three things on it, each larger."""
    c = C()
    c.vline(1, 1, 22, G3), c.hline(1, 22, 22, G3)
    for v in (5, 11, 17):
        c.px(v + 1, 21, G2), c.px(2, v, G2)
    c.line(3, 20, 21, 3, G2)
    c.rect(4, 17, 5, 18, W)
    c.disc(11, 12, 2, G1), c.px(10, 11, W)
    c.disc(18, 5, 3.4, G1), c.rect(16, 3, 17, 4, W)
    c.outline()
    return c


def i_service_pack():
    """Everything fixed since the release, in one bundle: a shrink-wrapped box, its band, the patches stacked in it."""
    c = C()
    c.rect(3, 6, 18, 21, KRAFT), c.vline(3, 6, 21, KRAFT_L), c.vline(18, 6, 21, KRAFT_D)
    c.rect(18, 4, 20, 19, KRAFT_D)                      # its side
    c.rect(5, 4, 20, 5, KRAFT_L)
    c.hline(3, 18, 12, G1), c.hline(3, 18, 13, G1)      # the band
    for i, y in enumerate((8, 15, 18)):                 # three patches, the same patch drawn small
        c.rect(6 + i * 2, y, 10 + i * 2, y + 1, PAPER)
    c.outline()
    c.px(20, 4, None)
    return c


def i_fluke():
    """A result nothing predicted and nothing repeats: points along a fitted line, and one far off it, lit."""
    c = C()
    for x, y in ((2, 19), (6, 18), (10, 15), (14, 14), (18, 11), (21, 10)):
        c.rect(x - 1, y - 1, x, y, G1)
    c.outline()
    c.line(1, 21, 22, 9, G3)
    c.disc(17, 4, 2.6, W), c.ring(17, 4, 3.2, 4.0, lambda a: W if int(a / 45) % 2 == 0 else None)
    c.outline()
    return c


def i_strict_mode():
    """Refuses anything it was not promised: a wall with one shape cut through it, and a piece of the wrong shape
    turned back."""
    c = C()
    c.rect(12, 1, 21, 22, G2), c.vline(12, 1, 22, G1), c.vline(21, 1, 22, G3)
    c.ascii(13, 9, ["   XX   ", "  XXXX  ", " XXXXXX ", "XXXXXXXX"], {"X": G4})   # the promised shape, cut through
    c.rect(2, 12, 8, 18, G1), c.hline(2, 8, 12, W)       # the square that came instead
    c.outline()
    c.ascii(3, 3, ["X   X", " X X ", "  X  ", " X X ", "X   X"], {"X": INK})
    c.ascii(9, 19, ["  X", " X ", "XXX"], {"X": G3})
    return c


def i_bare_metal():
    """Nothing between you and the hardware: a chip with its lid off, the die bare, its bond wires."""
    c = C()
    c.box(2, 2, 21, 21, G3, round_=False)
    for i in range(4, 20, 3):
        c.px(i, 1, G1), c.px(i, 22, G1), c.px(1, i, G1), c.px(22, i, G1)
    c.rect(7, 7, 16, 16, G1)                            # the die, bare
    c.hline(7, 16, 7, W), c.vline(7, 7, 16, W)
    for x in range(9, 15, 2):
        for y in range(9, 15, 2):
            c.px(x, y, G2)
    for a, b in (((5, 5), (8, 8)), ((18, 5), (15, 8)), ((5, 18), (8, 15)), ((18, 18), (15, 15))):
        c.line(*a, *b, GOLD)
    c.outline()
    return c


def i_off_by_one():
    """The error at the edge: a row of cells, and the pointer resting one past the last of them."""
    c = C()
    for i in range(4):
        x = 1 + i * 4
        c.rect(x, 10, x + 3, 15, G2), c.rect(x + 1, 11, x + 2, 14, G1)
    c.outline()
    for y in (10, 15):                                  # the cell that is not there
        for x in range(18, 22, 2):
            c.px(x, y, G2)
    c.ascii(17, 2, ["XXXXX", " XXX ", "  X  "], {"X": W})
    c.vline(19, 5, 8, W)
    c.outline()
    return c


#  ---- the TRAPs, and what the TRAP TABLE holds. A trap is armed against one thing and spent on it: an armed snap
#  trap, its bar cocked, its trigger plate in front. The plate says what it fires on, in the colour of the STATE it
#  ends, as the cures do (THRASHING has no tile colour, so its plate is neutral); EXHAUST's plate is MP's blue, the
#  two MARKs' the HP bar's green, CATCH ALL's all five. The five flavour TRAPs are a family of their own: each
#  restores health (an HP-green + on a white plate) and carries a taste, drawn as the thing it tastes of.
SPICY = ((240, 120, 84), (210, 60, 40), (128, 30, 22))
DRY = ((228, 204, 150), (196, 160, 98), (128, 98, 54))
SWEET = ((250, 176, 210), (230, 112, 168), (150, 56, 104))
BITTER = ((150, 104, 74), (98, 62, 40), (56, 34, 22))
SOUR = ((250, 240, 120), (226, 204, 48), (150, 128, 20))
PLATE_W = (W, W2, G1)


def trap(plate, glyph=None, gcol=W, stripes=None):
    c = C()
    c.rect(1, 17, 22, 20, WOOD), c.hline(1, 22, 17, WOOD_L), c.hline(1, 22, 20, WOOD_D)
    c.rect(3, 4, 4, 16, G1), c.vline(4, 4, 16, G2)      # the bar, cocked
    c.hline(3, 8, 4, G1)
    c.rect(2, 13, 5, 16, G2), c.hline(2, 5, 14, G1), c.hline(2, 5, 16, G3)   # its spring
    L, M, D = plate
    c.rect(9, 7, 21, 16, M)
    c.hline(9, 21, 7, L), c.vline(9, 7, 16, L)
    c.hline(9, 21, 16, D), c.vline(21, 7, 16, D)
    if stripes:
        for i, col in enumerate(stripes):
            c.rect(10 + i * 2 + (1 if i else 0), 8, 11 + i * 2 + 1, 15, col)
    c.outline()
    c.line(8, 4, 11, 7, INK)                              # the catch, holding the bar down to the plate
    if glyph:
        c.ascii(glyph[0], glyph[1], glyph[2], gcol if isinstance(gcol, dict) else {"X": gcol})
    return c


G_UP = (13, 9, ["  X  ", " XXX ", "XXXXX", "  X  ", "  X  ", "  X  "])
G_PLAY = (13, 9, ["X    ", "XX   ", "XXX  ", "XXXX ", "XXX  ", "XX   ", "X    "][0:6])
G_DROP = (13, 9, ["  X  ", "  X  ", " XXX ", "XXXXX", "XXXXX", " XXX "])
G_DOWN = (13, 9, ["  X  ", "  X  ", "  X  ", "XXXXX", " XXX ", "  X  "])
G_CLOCK = (12, 9, [" XXXXX ", "XXXoXXX", "XXXoXXX", "XXXooXX", "XXXXXXX", " XXXXX "])
G_CELL = (11, 9, ["XXXXXXXX ", "X     XXX", "XoooX XXX", "XoooX XXX", "X     XXX", "XXXXXXXX "])
G_LOOP = (12, 9, [" XXXX  ", "X    X ", "X   XXX", "X    X ", " X     ", "  XXX  "])
G_STAR = (13, 9, ["X X X", " XXX ", "XXXXX", " XXX ", "X X X"])


def i_throttle_trap(): return trap(THROTTLED, G_UP)
def i_suspend_trap(): return trap(SUSPENDED, G_PLAY)
def i_leak_trap(): return trap(LEAKING, G_DROP)
def i_heat_trap(): return trap(OVERHEATED, G_DOWN)
def i_hang_trap(): return trap(HUNG, G_CLOCK, {"X": W, "o": INK})
def i_exhaust_trap(): return trap((MP_L, MP, MP_D), G_CELL, {"X": W, "o": MP_L})
def i_thrash_trap(): return trap(PLATE_W, G_LOOP, INK)
def i_catch_all(): return trap(PLATE_W, G_STAR, W, stripes=FIVE)


def mark(high):
    """The level at which something is done about it: a gauge on an HP-green plate, its line set low or high, and
    the + it gives back."""
    y = 9 if high else 14
    g = ["X      ", "X      ", "X      ", "X      ", "X      ", "X      ", "X      "]
    g[y - 8] = "XXXXXXX"
    c = trap((HP_L, HP, HP_D), (11, 8, g), W)
    c.ascii(18, 10 if not high else 11, [" X ", "XXX", " X "], {"X": INK})
    return c


def i_low_mark(): return mark(False)
def i_high_mark(): return mark(True)


TASTES = {
    "spicy": (10, 9, ["     g", "    gX", "   XXX", "  XXXo", " XXXo ", "XXXo  ", "Xo    "]),
    "dry": (11, 9, ["  XXX  ", " XXoXX ", "XXXoXXX", "XoXXoXX", " XXXoX ", "  XXX  "]),
    "sweet": (10, 10, ["X  XXX  X", "XXXXXXXXX", "XXXXoXXXX", "X  XXX  X"]),
    "bitter": (11, 9, ["  XXX  ", " XXXXX ", "XXXoXXX", "XXoXXXX", "XXoXXXX", " XoXXX ", "  XXX  "][0:7]),
    "sour": (10, 9, ["ooooooooo", " XXwXwXX ", "  XXwXX  ", "   XwX   ", "    X    "]),
}


def flavour(taste, cols):
    L, M, D = cols
    x, y, rows = TASTES[taste]
    c = trap(PLATE_W)
    legend = {"X": M, "o": D, "g": G3, "w": L}
    if taste == "sweet":
        legend = {"X": M, "o": L}
    c.ascii(x, y, rows, legend)
    c.ascii(18, 8, [" X ", "XXX", " X "], {"X": HP_D})
    return c


def i_spicy_trap(): return flavour("spicy", SPICY)
def i_dry_trap(): return flavour("dry", DRY)
def i_sweet_trap(): return flavour("sweet", SWEET)
def i_bitter_trap(): return flavour("bitter", BITTER)
def i_sour_trap(): return flavour("sour", SOUR)


ICONS3 = [
    ("dither", "DITHER", ["ITEM_BRIGHT_POWDER"], i_dither, "own", "a crosshair lost in a field of dither, its centre unfindable"),
    ("revert", "REVERT", ["ITEM_WHITE_HERB"], i_revert, "own", "a stat bar knocked down, an arrow carrying it back to its mark"),
    ("debug_build", "DEBUG BUILD", ["ITEM_MACHO_BRACE"], i_debug_build, "own", "a chip, probes clipped to its pins, their leads off"),
    ("weight_share", "WEIGHT SHARE", ["ITEM_EXP_SHARE"], i_weight_share, "own", "two grids of weights, one pattern, tied together"),
    ("queue_jump", "QUEUE JUMP", ["ITEM_QUICK_CLAW"], i_queue_jump, "own", "a queue, one leaping from the back to the free front"),
    ("affinity", "AFFINITY", ["ITEM_SOOTHE_BELL"], i_affinity, "own", "a small process tied fast to one core"),
    ("unpair", "UNPAIR", ["ITEM_MENTAL_HERB"], i_unpair, "own", "a plug and its socket pulled apart"),
    ("hard_coded", "HARD CODED", ["ITEM_CHOICE_BAND"], i_hard_coded, "own", "a riveted plate, one value stamped in"),
    ("bubble", "BUBBLE", ["ITEM_KINGS_ROCK"], i_bubble, "own", "a pipeline's stages stepping down, one slot an empty bubble"),
    ("surcharge", "SURCHARGE", ["ITEM_AMULET_COIN"], i_surcharge, "own", "a price tag, a gold coin with a + set on it"),
    ("mute", "MUTE", ["ITEM_CLEANSE_TAG"], i_mute, "own", "a channel strip, fader down, its M key lit"),
    ("escape_hatch", "ESCAPE HATCH", ["ITEM_SMOKE_BALL"], i_escape_hatch, "own", "a floor hatch, lid thrown back, the ladder, an arrow out"),
    ("version_lock", "VERSION LOCK", ["ITEM_EVERSTONE"], i_version_lock, "own", "a tag reading v1, a pin driven through it"),
    ("failsafe", "FAILSAFE", ["ITEM_FOCUS_BAND"], i_failsafe, "own", "a net under a falling bar, one sliver of HP green left"),
    ("learning_rate", "LEARNING RATE", ["ITEM_LUCKY_EGG"], i_learning_rate, "own", "a loss curve, big strides down it"),
    ("long_tail", "LONG TAIL", ["ITEM_SCOPE_LENS"], i_long_tail, "own", "a steep fall and a long tail, a lens on its lit far end"),
    ("headroom", "HEADROOM", ["ITEM_LEFTOVERS"], i_headroom, "own", "a meter in HP green, the clip line above, the room kept; + a little"),
    ("scaling_law", "SCALING LAW", ["ITEM_DRAGON_SCALE"], i_scaling_law, "own", "a straight line on log paper, three things on it, each bigger"),
    ("service_pack", "SERVICE PACK", ["ITEM_UP_GRADE"], i_service_pack, "own", "a banded box, the patches stacked in it"),
    ("flow_trim", "FLOW TRIM", ["ITEM_SEA_INCENSE"], i_flow_trim, "own", "the GAIN's amplifier, small, FLOW's hue, its trim screw"),
    ("dither_trim", "DITHER TRIM", ["ITEM_LAX_INCENSE"], i_dither_trim, "own", "DITHER at a lower setting: the pattern sparser"),
    ("fluke", "FLUKE", ["ITEM_LUCKY_PUNCH"], i_fluke, "own", "points along a fitted line, one far off it, lit"),
    ("strict_mode", "STRICT MODE", ["ITEM_METAL_POWDER"], i_strict_mode, "own", "a wall with one shape cut in, a square turned back"),
    ("bare_metal", "BARE METAL", ["ITEM_THICK_CLUB"], i_bare_metal, "own", "a chip with its lid off: the die, its bond wires"),
    ("off_by_one", "OFF BY ONE", ["ITEM_STICK"], i_off_by_one, "own", "a row of cells, the pointer one past the last"),
    ("swarm_gain", "SWARM GAIN", ["ITEM_SILVER_POWDER"], i_swarm_gain, "own", "an amplifier, small signal in, large out; SWARM's hue"),
    ("hardened_gain", "HARDENED GAIN", ["ITEM_METAL_COAT"], i_hardened_gain, "own", "the amplifier; HARDENED's hue"),
    ("stratum_gain", "STRATUM GAIN", ["ITEM_SOFT_SAND"], i_stratum_gain, "own", "the amplifier; STRATUM's hue"),
    ("legacy_gain", "LEGACY GAIN", ["ITEM_HARD_STONE"], i_legacy_gain, "own", "the amplifier; LEGACY's hue"),
    ("growth_gain", "GROWTH GAIN", ["ITEM_MIRACLE_SEED"], i_growth_gain, "own", "the amplifier; GROWTH's hue"),
    ("opaque_gain", "OPAQUE GAIN", ["ITEM_BLACK_GLASSES"], i_opaque_gain, "own", "the amplifier; OPAQUE's hue"),
    ("logic_gain", "LOGIC GAIN", ["ITEM_BLACK_BELT"], i_logic_gain, "own", "the amplifier; LOGIC's hue"),
    ("signal_gain", "SIGNAL GAIN", ["ITEM_MAGNET"], i_signal_gain, "own", "the amplifier; SIGNAL's hue"),
    ("flow_gain", "FLOW GAIN", ["ITEM_MYSTIC_WATER"], i_flow_gain, "own", "the amplifier; FLOW's hue"),
    ("vector_gain", "VECTOR GAIN", ["ITEM_SHARP_BEAK"], i_vector_gain, "own", "the amplifier; VECTOR's hue"),
    ("corrupt_gain", "CORRUPT GAIN", ["ITEM_POISON_BARB"], i_corrupt_gain, "own", "the amplifier; CORRUPT's hue"),
    ("frozen_gain", "FROZEN GAIN", ["ITEM_NEVER_MELT_ICE"], i_frozen_gain, "own", "the amplifier; FROZEN's hue"),
    ("latent_gain", "LATENT GAIN", ["ITEM_SPELL_TAG"], i_latent_gain, "own", "the amplifier; LATENT's hue"),
    ("context_gain", "CONTEXT GAIN", ["ITEM_TWISTED_SPOON"], i_context_gain, "own", "the amplifier; CONTEXT's hue"),
    ("entropy_gain", "ENTROPY GAIN", ["ITEM_CHARCOAL"], i_entropy_gain, "own", "the amplifier; ENTROPY's hue"),
    ("emergent_gain", "EMERGENT GAIN", ["ITEM_DRAGON_FANG"], i_emergent_gain, "own", "the amplifier; EMERGENT's hue"),
    ("content_gain", "CONTENT GAIN", ["ITEM_SILK_SCARF"], i_content_gain, "own", "the amplifier; CONTENT's hue"),
    ("throttle_trap", "THROTTLE TRAP", ["ITEM_CHERI_BERRY"], i_throttle_trap, "own", "an armed snap trap, its plate THROTTLED's yellow, an arrow up"),
    ("suspend_trap", "SUSPEND TRAP", ["ITEM_CHESTO_BERRY"], i_suspend_trap, "own", "the trap; SUSPENDED's slate, a play key"),
    ("leak_trap", "LEAK TRAP", ["ITEM_PECHA_BERRY"], i_leak_trap, "own", "the trap; LEAKING's green, a drop"),
    ("heat_trap", "HEAT TRAP", ["ITEM_RAWST_BERRY"], i_heat_trap, "own", "the trap; OVERHEATED's ember, temperature down"),
    ("hang_trap", "HANG TRAP", ["ITEM_ASPEAR_BERRY"], i_hang_trap, "own", "the trap; HUNG's blue, a clock"),
    ("exhaust_trap", "EXHAUST TRAP", ["ITEM_LEPPA_BERRY"], i_exhaust_trap, "own", "the trap; MP's blue, a cell with a segment"),
    ("low_mark", "LOW MARK", ["ITEM_ORAN_BERRY"], i_low_mark, "own", "the trap; HP green, a gauge marked low, a +"),
    ("thrash_trap", "THRASH TRAP", ["ITEM_PERSIM_BERRY"], i_thrash_trap, "own", "the trap; a neutral plate (THRASHING has no colour), a loop"),
    ("catch_all", "CATCH ALL", ["ITEM_LUM_BERRY"], i_catch_all, "own", "the trap; all five states' colours, a wildcard *"),
    ("high_mark", "HIGH MARK", ["ITEM_SITRUS_BERRY"], i_high_mark, "own", "the trap; HP green, the gauge marked high, a +"),
    ("spicy_trap", "SPICY TRAP", ["ITEM_FIGY_BERRY"], i_spicy_trap, "own", "the trap, white plate, HP +; a red chilli"),
    ("dry_trap", "DRY TRAP", ["ITEM_WIKI_BERRY"], i_dry_trap, "own", "the same; a dry, cracked crumb"),
    ("sweet_trap", "SWEET TRAP", ["ITEM_MAGO_BERRY"], i_sweet_trap, "own", "the same; a pink wrapped sweet"),
    ("bitter_trap", "BITTER TRAP", ["ITEM_AGUAV_BERRY"], i_bitter_trap, "own", "the same; a dark coffee bean"),
    ("sour_trap", "SOUR TRAP", ["ITEM_IAPAPA_BERRY"], i_sour_trap, "own", "the same; a lemon wedge"),
]
APPROVED = APPROVED + [e[0] for e in ICONS3]      # the user, 2026-11-07: "Build all 57"


# ================================================================================================= batch 4
#  Drafted 2026-11-09 (the user: "Icons batch 4"), the last of FireRed's icons a player can reach. `--draft --batch 4`
#  draws them. APPROVED 2026-11-09 (the user: "Build all", and "Keep all 20" for the berries), so `--all` writes them
#  with batches 1-3 and the report exits 1 if the engine drifts from any of them.
#  The ITEMS pocket's valuables, the four shards, the drinks and treats, the MAIL a player can be given and the four
#  PARADE DAYS scarves; the TRAP TABLE's twenty berries that are still berries; four key items.
#  Not drawn, because no player can get them (no gift, ball, hidden item, prize, mart, wild hold, Pickup or holiday
#  gives them): SHOAL SALT and SHOAL SHELL; FLUFFY TAIL (no mart sells it); ORANGE, HARBOR, MECH, WOOD, WAVE, BEAD
#  and TROPIC MAIL; PINK SCARF ("like the ones handed out", and nothing hands it out); ENIGMA BERRY (an e-Reader's
#  only); MACH BIKE, ACRO BIKE and the rest of Hoenn's key items (CONTEST PASS ... DEVON SCOPE). The SINKs are not
#  here: their heat sink (sink.png, T-488) is already ours. MYSTICTICKET and AURORATICKET stay undrawn (batch 2).
STARRED = ((250, 154, 150), (214, 72, 84), (130, 32, 46))        # STARDUST and STAR PIECE: "red", their words
PEARLS = (W, (222, 224, 234), (176, 180, 198))                     # "a pretty silver color"
IRON = ((132, 124, 118), (88, 82, 80), (50, 46, 48))              # the METEORITE: lumpy, hard
CAP = ((216, 140, 104), (176, 84, 62), (108, 46, 38))            # the mushrooms' caps
NAMED = {                                                         # a shard, a scarf: the colour is its name
    "red": ramp((206, 64, 58), 0.4), "blue": ramp((64, 110, 206), 0.4),
    "yellow": ramp((226, 192, 48), 0.4), "green": ramp((70, 156, 82), 0.4),
}
WAX = (TASSEL, TASSEL_D)                                          # a seal is wax, and wax is SECRET KEY's red


def inside(pts, x, y):
    """Is the pixel centre (x+.5, y+.5) inside the polygon?"""
    px_, py_, n, hit = x + 0.5, y + 0.5, len(pts), False
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        if (y0 > py_) != (y1 > py_) and px_ < x0 + (py_ - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def poly(c, pts, col):
    for y in range(N):
        for x in range(N):
            if inside(pts, x, y):
                c.px(x, y, col(x, y) if callable(col) else col)


def sphere(c, cx, cy, r, cols, hi=W, sy=1.0):
    """A ball lit from the top left: light, middle and dark by how far each pixel faces the light; sy squashes it."""
    L, M, D = cols
    for y in range(N):
        for x in range(N):
            dx, dy = (x + 0.5 - cx) / r, (y + 0.5 - cy) / (r * sy)
            if dx * dx + dy * dy <= 1.0:
                z = math.sqrt(max(0.0, 1 - dx * dx - dy * dy))
                lit = -0.55 * dx - 0.6 * dy + 0.58 * z
                c.px(x, y, L if lit > 0.62 else M if lit > 0.05 else D)
    if hi:
        hx, hy = int(cx - r * 0.42), int(cy - r * sy * 0.45)
        c.px(hx, hy, hi)
        if r > 5:
            c.px(hx + 1, hy, hi), c.px(hx, hy + 1, hi)


def sparkle(c, x, y, col=W):
    c.px(x, y, col), c.px(x - 1, y, col), c.px(x + 1, y, col), c.px(x, y - 1, col), c.px(x, y + 1, col)


#  ---- the valuables, each the thing its description says, in its description's colour
def i_nugget():
    """A nugget of pure gold that gives off a lustrous gleam: a gold lump, its gleam."""
    c = C()
    c.ascii(3, 6, ["       MMMM       ",
                   "     MMLLMMMM     ",
                   "   MMLLWLLMMMD    ",
                   "  MMLLLLLMMMMDD   ",
                   " MMLLLLMMMMMMDDD  ",
                   " MLLLMMMMMMMDMMDD ",
                   "MMLLMMMMMMDDMMMDD ",
                   "MMLMMMMMDDDMMMMDDD",
                   "MMMMMMMDDMMMMMDDDD",
                   " MMMMMMMMMMMMDDDD ",
                   " DMMMMMMMMMDDDDD  ",
                   "  DDMMMMMDDDDDD   ",
                   "   DDDDDDDDDD     "], {"L": GOLD_L, "M": GOLD, "D": GOLD_D, "W": W})
    c.outline()
    sparkle(c, 19, 3)
    return c


def i_pearl():
    """A relatively small pearl, sparkling silver."""
    c = C()
    sphere(c, 12, 13, 5.2, PEARLS, hi=None)
    c.px(10, 11, W), c.px(9, 11, W2)
    c.outline()
    sparkle(c, 18, 6)
    return c


def i_big_pearl():
    """A quite-large pearl: the PEARL, grown."""
    c = C()
    sphere(c, 11.5, 12.5, 8.6, PEARLS, hi=None)
    c.rect(7, 7, 8, 8, W), c.px(9, 7, W2), c.px(7, 9, W2)
    c.outline()
    sparkle(c, 20, 3)
    return c


def i_stardust():
    """A pretty red sand with a loose, silky feel: a little heap of red grains, a few loose, one catching the light."""
    import random
    rnd = random.Random(4)
    L, M, D = STARRED
    c = C()
    for x in range(2, 22):
        h = 7.5 * (1 - ((x - 11.5) / 10.0) ** 2)
        for y in range(int(round(19 - h)), 20):
            c.px(x, y, rnd.choice((M, M, L, D)) if y < 18 else rnd.choice((M, D, D)))
    for x, y in ((5, 9), (17, 8), (9, 6), (20, 11), (3, 12)):
        c.px(x, y, M)
    c.outline()
    sparkle(c, 15, 4)
    c.px(8, 13, W), c.px(13, 12, W)
    return c


def i_star_piece():
    """A shard of a gem that sparkles red: a faceted star, one arm broken off along a clean line."""
    L, M, D = STARRED
    c = C()
    cx, cy = 11.5, 12.5
    pts = []
    for k in range(10):
        r = 10.5 if k % 2 == 0 else 4.4
        a = math.radians(90 + k * 36)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))

    def facet(x, y):
        dx, dy = x + 0.5 - cx, y + 0.5 - cy
        return L if (dx + dy < -1) else D if (dx > 1 and dy > 0) else M
    poly(c, pts, facet)
    for x in range(N):                                 # the break: the lower-right arm gone past a straight cut
        for y in range(N):
            if (x - cx) * 0.95 + (y - cy) * 0.31 > 4.6 and y > cy - 1:
                c.px(x, y, None)
    c.line(int(cx), int(cy), int(cx), 3, W)            # a ridge catching the light
    c.outline()
    sparkle(c, 20, 18)
    return c


def mushroom(cx, w, h, stem_w, stem_h, base):
    L, M, D = CAP
    c = C()
    c.rect(cx - stem_w // 2, base - stem_h, cx - stem_w // 2 + stem_w - 1, base, PAPER)
    c.vline(cx - stem_w // 2 + stem_w - 1, base - stem_h, base, PAPER2)
    top = base - stem_h - h
    for y in range(top, base - stem_h + 1):
        t = (y - top + 0.5) / (h + 1)
        half = w / 2 * math.sqrt(max(0.0, 1 - (1 - t) ** 2))
        for x in range(int(round(cx - half)), int(round(cx + half))):
            c.px(x, y, L if x < cx - half / 3 and y < top + h / 2 else D if x > cx + half / 2 else M)
    c.hline(int(cx - w / 2) + 1, int(cx + w / 2) - 2, base - stem_h, D)     # the gills' shadow under the rim
    return c, top


def i_tiny_mushroom():
    """A small and rare mushroom: one small mushroom, two pale spots."""
    c, top = mushroom(12, 10, 5, 3, 5, 19)
    c.px(10, top + 2, W), c.px(13, top + 1, W)
    c.outline()
    return c


def i_big_mushroom():
    """A large and rare mushroom: the same, large."""
    c, top = mushroom(12, 20, 9, 6, 7, 21)
    for x, y in ((7, top + 4), (12, top + 2), (16, top + 5), (10, top + 6)):
        c.rect(x, y, x + 1, y + 1, W)
    c.outline()
    return c


def i_heart_scale():
    """A heart-shaped scale that glows faintly in the colours of a rainbow: a pale heart, a scale's growth lines, and
    the faint sheen across it in four soft hues (none of them a type's or a state's: rainbow, not a label)."""
    PINK = ((252, 222, 230), (236, 176, 196), (180, 112, 140))
    SHEEN = [(214, 236, 252), (220, 246, 214), (252, 244, 196), (238, 214, 250)]
    c = C()
    cx, cy, s = 11.5, 11.0, 9.0
    for y in range(N):
        for x in range(N):
            X, Y = (x + 0.5 - cx) / s, -(y + 0.5 - cy) / s * 1.1
            if (X * X + Y * Y - 0.5) ** 3 - X * X * Y ** 3 * 0.9 <= 0 and y < 22:
                c.px(x, y, PINK[1])
    for y in range(N):
        for x in range(N):
            if c.get(x, y) == PINK[1]:
                if c.get(x - 1, y - 1) is None or c.get(x, y - 1) is None:
                    c.px(x, y, PINK[0])
                elif c.get(x + 1, y + 1) is None or c.get(x, y + 1) is None:
                    c.px(x, y, PINK[2])
    for k, col in enumerate(SHEEN):                   # the sheen, one diagonal band of each soft hue
        for y in range(N):
            x = 4 + k * 2 + y // 2
            if c.get(x, y) == PINK[1]:
                c.px(x, y, col)
    for y in range(N):                                # growth lines, arcs about the point
        for x in range(N):
            d = math.hypot(x - 11.5, y - 20.5)
            if c.get(x, y) not in (None,) and (4.0 <= d <= 4.7 or 8.0 <= d <= 8.7) and y < 19:
                c.px(x, y, PINK[2])
    c.outline()
    return c


def shard(colour):
    """A small shard from some tool made long ago: a broken piece, a worked groove across it (it was made, not
    found), its broken edge jagged; the colour is the one its name says."""
    L, M, D = NAMED[colour]
    c = C()
    pts = [(3, 21), (5, 9), (9, 2), (12, 7), (15, 4), (21, 11), (18, 15), (20, 21)]   # broken on every side

    def face(x, y):                                     # three flat facets, as a fracture leaves them
        return L if x < 9 and y < 15 else D if x > 13 and y > 9 else M
    poly(c, pts, face)
    c.line(4, 16, 19, 12, D), c.line(4, 17, 19, 13, L)  # the groove someone cut: it was made, not found
    c.px(8, 5, W), c.px(7, 7, W), c.px(6, 10, W)
    c.outline()
    return c


def i_red_shard(): return shard("red")
def i_blue_shard(): return shard("blue")
def i_yellow_shard(): return shard("yellow")
def i_green_shard(): return shard("green")


#  ---- the drinks and treats: as batch 2's drinks, HP's green where it gives back HP
def i_moomoo_milk():
    """Highly nutritious milk that restores HP: a milk bottle, opaque white to the shoulder, its cap the HP bar's
    green (batch 2's drinks: HP green on a cap, a band, a straw, a window)."""
    c = C()
    c.rect(9, 1, 14, 3, HP), c.hline(9, 14, 1, HP_L), c.vline(14, 1, 3, HP_D)
    c.rect(10, 4, 13, 7, GLASS)
    for y in range(8, 22):
        half = 3 + min(3, y - 8) if y < 11 else 6
        c.hline(12 - half, 11 + half, y, GLASS if y < 10 else W)
    for y in range(10, 22):
        c.px(17, y, W2)
    c.rect(7, 14, 16, 17, HP), c.hline(7, 16, 14, HP_L), c.hline(7, 16, 17, HP_D)     # the band
    c.vline(8, 10, 20, W2)
    c.outline()
    c.px(8, 11, GLASS2)
    return c


def i_lava_cookie():
    """A cookie baked on hot stone that ends every state: a round cookie on a grey stone slab, the heat rising
    off it in grey, and five flecks in the five states' colours (ROLLBACK and HOTFIX wear all five for the same
    reason). The stone is not ember: OVERHEATED's colour on it would say it ends only that."""
    c = C()
    c.rect(1, 18, 22, 21, G3), c.hline(1, 22, 18, G2), c.hline(1, 22, 21, G4)
    for x in range(3, 22, 5):
        c.px(x, 20, G4)
    sphere(c, 11.5, 12.5, 7.4, (KRAFT_L, KRAFT, KRAFT_D), hi=None, sy=0.72)
    for (x, y), col in zip(((8, 10), (13, 9), (16, 12), (10, 14), (14, 15)), FIVE):
        c.rect(x, y, x + 1, y, col)
    c.outline()
    for x, y0 in ((4, 3), (19, 2)):                   # heat off the stone
        waves_v = [0, 1, 1, 0, -1, -1, 0]
        for k, d in enumerate(waves_v):
            c.px(x + d, y0 + k, G2)
    return c


#  ---- the MAIL a player can be given: one sheet of stationery, its print in the box at its head. A daemon is
#  coloured by its type (9.4), so a daemon's print wears its type's hue; the rest are neutrals and paper.
def mail(draw):
    c = C()
    c.box(3, 1, 20, 22, PAPER)
    for x in range(15, 21):                            # the top corner folded down
        for y in range(1, 7):
            if x - 15 > y - 1:
                c.px(x, y, None)
            elif x >= 15 and y <= 6 and x - 15 >= y - 2:
                c.px(x, y, PAPER2)
    c.rect(5, 4, 15, 12, W)
    for y in (15, 17, 19):                             # the lines of the letter
        c.hline(5, 18 if y < 19 else 12, y, G1)
    draw(c)
    c.outline()
    return c


def i_glitter_mail():
    """A cute SPIKE print: SPIKE's jag in its type's hue (SIGNAL), glitter round it."""
    L, M, D = tc("ELECTRIC")

    def d(c):
        c.ascii(7, 5, ["   XX ", "  XX  ", " XXXXX", "    XX", "   XX ", "  XX  ", " XX   ", " X    "],
                {"X": M})
        c.px(9, 5, L), c.px(8, 6, L), c.px(12, 7, D), c.px(11, 8, D)
        for x, y in ((6, 5), (14, 6), (13, 11), (6, 10)):
            c.px(x, y, G1)
    return mail(d)


def i_shadow_mail():
    """A cute FADING print: FADING in its type's hue (LATENT), going out into the paper as it fades."""
    L, M, D = tc("GHOST")

    def d(c):
        c.ascii(7, 5, ["  XXXX ", " XXXXXX", " XoXXoX", " XXXXXX", "XXXXXXX", "XXXXXX ", " X X X "],
                {"X": M, "o": W})
        for y in range(4, 13):                         # it fades to the right
            for x in range(5, 16):
                if c.get(x, y) == M and (x >= 12 and (x + y) % 2 or x >= 14):
                    c.px(x, y, W)
    return mail(d)


def i_dream_mail():
    """It will bear the print of the DAEMON holding it: the print box empty but for a dashed outline, waiting."""
    def d(c):
        for y in range(5, 12):
            for x in range(6, 15):
                e = (x - 10) ** 2 / 16.0 + (y - 8.5) ** 2 / 9.0
                if 0.75 <= e <= 1.3 and (x + 2 * y) % 3 != 0:
                    c.px(x, y, G2)
    return mail(d)


def i_fab_mail():
    """A gorgeous, extravagant print: a lattice of gold diamonds, a gold rule under it."""
    def d(c):
        for y in range(4, 13):
            for x in range(5, 16):
                k = (x + y) % 4 == 0 or (x - y) % 4 == 0
                c.px(x, y, GOLD if k else GOLD_L if (x + y) % 2 else W)
        c.hline(5, 18, 14, GOLD_D)
    return mail(d)


def i_retro_mail():
    """A print of three cute DAEMONS: three small round figures side by side, in grey (which three, it does not
    say, so it gives them no type)."""
    def d(c):
        for x0 in (5, 9, 13):
            c.ascii(x0, 5, [" X ", "XXX", "oXo", "XXX", "XXX", "X X"], {"X": G3, "o": W})
    return mail(d)


#  ---- the scarves: handed out on PARADE DAYS (and CLOVER DAY). One scarf, tied, its tails fringed and banded
#  for the parade; the colour is its name. GREEN, the CLOVER DAY scarf, wears a clover at its knot.
SCARF = ["                        ",
         "                        ",
         "     LLLLLLLLLLLLLL     ",
         "   LLMMMMMMMMMMMMMMLL   ",
         "  LMMMMMMMMMMMMMMMMMMD  ",
         "  LMMDDDDDDDDDDDDDDMMD  ",
         "  LMMD            DMMD  ",
         "  LMMD            DMMD  ",
         "   LMMD          DMMD   ",
         "    LMMDD      DDMMD    ",
         "     LMMMMLLLLMMMMD     ",
         "       DMLLLLLLMD       ",
         "        LMMMMMMD        ",
         "        LMMDLMMD        ",
         "       LMMD LMMMD       ",
         "       LMMD  LMMD       ",
         "      LMMD   LMMMD      ",
         "      wwww    wwww      ",
         "     LMMMD    LMMMD     ",
         "     LMMMD    LMMMD     ",
         "     M M M    M M M     ",
         "     M M M    M M M     "]


def scarf(colour, clover=False):
    L, M, D = NAMED[colour]
    c = C()
    c.ascii(0, 0, SCARF, {"L": L, "M": M, "D": D, "w": W})
    c.outline()
    if clover:
        c.ascii(10, 10, [" W  ", "WWW ", " W  ", "  W "], {"W": W})
    return c


def i_red_scarf(): return scarf("red")
def i_blue_scarf(): return scarf("blue")
def i_green_scarf(): return scarf("green", clover=True)
def i_yellow_scarf(): return scarf("yellow")


#  ---- the key items
def i_peer_review():
    """Signed and sealed, addressed to everyone who signed the first one: a sheet, a heading, row on row of
    signatures, and a wax seal on a ribbon at its foot."""
    c = C()
    c.box(2, 1, 19, 22, PAPER)
    c.hline(4, 13, 3, G3), c.hline(4, 9, 5, G1)
    for y, x0, x1, per in ((8, 4, 12, 4.0), (11, 6, 16, 3.0), (14, 4, 11, 5.0)):   # signatures, each its own hand
        waves(c, x0, x1, y, 1, G4, per)
    c.hline(4, 12, 17, G4)
    c.rect(14, 16, 15, 22, TASSEL_D), c.rect(18, 16, 19, 22, TASSEL_D)
    c.outline()
    c.disc(17, 16.5, 3.4, TASSEL)
    c.px(16, 15, TASSEL_D), c.px(17, 16, TASSEL_D), c.px(18, 17, TASSEL_D), c.px(16, 14, (196, 96, 104))
    c.outline()
    return c


def i_envelope():
    """Sealed, addressed, and not addressed to you: an envelope, its flap closed under a wax seal, the address
    written on its face."""
    c = C()
    c.box(1, 5, 22, 19, PAPER)
    c.line(2, 6, 11, 12, PAPER2), c.line(21, 6, 12, 12, PAPER2)
    c.line(2, 18, 9, 13, PAPER2), c.line(21, 18, 14, 13, PAPER2)
    for y, x1 in ((15, 15), (17, 12)):
        c.hline(5, x1, y, G3)
    c.disc(11.5, 12, 2.6, TASSEL)
    c.px(11, 11, (196, 96, 104)), c.px(12, 13, TASSEL_D)
    c.rect(17, 7, 20, 10, G1), c.px(17, 7, W)          # a stamp, cancelled
    c.outline()
    return c


def i_meteorite():
    """Fell from space long ago; very lumpy and hard: a pitted lump of dark iron, a glint of bare metal."""
    L, M, D = IRON
    c = C()
    c.ascii(2, 4, ["      MMMMMM      ",
                   "    MMLLLMMMMM    ",
                   "  MMLLLLMMMMMMMD  ",
                   " MMLLLMMMDDMMMMMD ",
                   " MLLLMMMDDDMMMMMDD",
                   "MMLLMMMMDDMMMMMMDD",
                   "MLLMMDDMMMMMMDDMDD",
                   "MLMMDDDMMMMMDDDMMD",
                   "MMMMMDDMMMMMMDDMDD",
                   " MMMMMMMMDDMMMMMDD",
                   " MMMMMMMDDDMMMMDD ",
                   "  DMMMMMMDDMMMDDD ",
                   "   DDMMMMMMMDDDD  ",
                   "     DDDDDDDDD    "], {"L": L, "M": M, "D": D})
    c.outline()
    c.px(6, 7, W), c.px(7, 6, W2)
    return c


def i_powder_jar():
    """A jar for storing BERRY POWDER: a glass jar, its lid screwed on, two thirds full of the powder."""
    c = C()
    c.rect(5, 2, 18, 5, G2), c.hline(5, 18, 2, G1), c.hline(5, 18, 5, G3)
    for x in range(6, 18, 2):
        c.px(x, 3, G3), c.px(x, 4, G3)
    c.box(4, 6, 19, 22, GLASS)
    c.rect(5, 12, 18, 21, KRAFT)
    c.hline(5, 18, 12, KRAFT_L)
    for x, y in ((7, 15), (11, 17), (15, 14), (9, 19), (16, 19)):
        c.px(x, y, KRAFT_D)
    c.vline(6, 7, 20, W)
    c.rect(8, 8, 15, 10, W), c.hline(9, 14, 9, G2)    # its label
    return c


#  ---- the berries the TRAP TABLE still holds as berries: RAZZ to BELUE kept their names (port_names never renamed
#  them, T-526 left them), and each is "ground up into a powder as an ingredient for medicine". So each is drawn as
#  its fruit, resting on the TRAP TABLE's own wooden plank -- the TRAPs' board, without the bar or the plate: the
#  family is the board, the fruit says which. Stems and crowns are grey, as the SPICY TRAP's chilli stem is, so no
#  leaf is read as LEAKING's green.
def plank(c):
    c.rect(1, 17, 22, 20, WOOD), c.hline(1, 22, 17, WOOD_L), c.hline(1, 22, 20, WOOD_D)


def berry(draw):
    c = C()
    plank(c)
    c.outline()
    draw(c)
    c.outline()
    return c


def stem(c, x, y0, y1, leaf=None):
    c.vline(x, y0, y1, G3)
    if leaf:
        c.hline(x + 1, x + leaf, y0 + 1, G2)


def round_berry(cols, cx=11.5, cy=10.5, r=6.2, sy=1.0, top=None):
    def d(c):
        sphere(c, cx, cy, r, cols, sy=sy)
        if top:
            top(c)
    return d


def bumpy(c, cols, pitch=2):
    """Drupelets or a net: every other pixel of the fruit's middle lifted to its light."""
    L, M, D = cols
    for y in range(N):
        for x in range(N):
            if c.get(x, y) == M and (x // pitch + y // pitch) % 2 == 0 and (x + y) % pitch == 0:
                c.px(x, y, L)


def i_razz_berry():
    """A raspberry, red, its drupelets."""
    cols = ((236, 110, 120), (196, 52, 74), (120, 26, 44))
    def d(c):
        round_berry(cols, r=6.4, sy=1.05)(c)
        bumpy(c, cols)
        stem(c, 11, 2, 4, 3)
    return berry(d)


def i_bluk_berry():
    """A blueberry: dark blue, the star at its crown."""
    cols = ((112, 132, 196), (58, 76, 140), (30, 38, 84))
    def d(c):
        round_berry(cols, r=6.8)(c)
        c.ascii(10, 4, ["X X", " X ", "X X"], {"X": cols[2]})
    return berry(d)


def i_nanab_berry():
    """A banana, curved."""
    cols = ((250, 236, 150), (226, 196, 70), (156, 124, 30))
    def d(c):
        for t in range(0, 40):
            a = math.radians(200 + t * 3.6)
            x, y = 12 + 9 * math.cos(a), 5 - 9 * math.sin(a) * 1.0
            for k in range(-2, 3):
                c.px(int(round(x)), int(round(y + k)), cols[0] if k < -1 else cols[2] if k > 1 else cols[1])
        stem(c, 3, 6, 9)
        c.rect(20, 7, 21, 8, BITTER[2])
    return berry(d)


def i_wepear_berry():
    """A pear: pale, narrow at the top, its stem."""
    cols = ((236, 240, 176), (196, 208, 120), (128, 140, 66))
    def d(c):
        sphere(c, 12, 12, 5.6, cols)
        sphere(c, 12, 6.5, 3.4, cols, hi=None)
        stem(c, 12, 1, 3, 2)
    return berry(d)


def i_pinap_berry():
    """A pineapple: a criss-cross of scales, a grey crown."""
    cols = ((246, 214, 110), (214, 166, 48), (140, 98, 22))
    def d(c):
        sphere(c, 11.5, 12, 5.4, cols, hi=None, sy=1.0)
        for y in range(N):
            for x in range(N):
                if c.get(x, y) in cols and ((x + y) % 4 == 0 or (x - y) % 4 == 0):
                    c.px(x, y, cols[2])
        c.ascii(8, 1, ["X  X  X", " X X X ", "  XXX  ", "  XXX  "], {"X": G3})
    return berry(d)


def i_pomeg_berry():
    """A pomegranate: deep red, its crown."""
    cols = ((226, 96, 96), (170, 40, 52), (100, 20, 34))
    def d(c):
        round_berry(cols, cy=11, r=6.6)(c)
        c.ascii(9, 2, ["X X X", "XXXXX", " XXX "], {"X": cols[2]})
    return berry(d)


def i_kelpsy_berry():
    """A root, long and tapering, blue."""
    cols = ((150, 176, 226), (84, 116, 190), (44, 62, 120))
    def d(c):
        for y in range(4, 17):
            half = 4.2 - (y - 4) * 0.3
            for x in range(int(round(12 - half)), int(round(12 + half))):
                c.px(x, y, cols[0] if x < 12 - half + 1.5 else cols[2] if x > 12 + half - 2 else cols[1])
        for y in (7, 10, 13):
            c.hline(11, 12, y, cols[2])
        c.ascii(9, 0, ["X   X", " X X ", "  X  ", "  X  "], {"X": G3})
    return berry(d)


def i_qualot_berry():
    """A round yellow fruit, dimpled."""
    cols = ((250, 232, 140), (232, 186, 66), (160, 112, 30))
    def d(c):
        round_berry(cols, r=6.6, sy=0.9)(c)
        c.ascii(9, 6, ["X   X", "     ", "  X  ", "     ", "X   X"], {"X": cols[2]})
    return berry(d)


def i_hondew_berry():
    """A honeydew: pale, round, netted."""
    cols = ((236, 246, 214), (196, 214, 166), (128, 146, 102))
    def d(c):
        round_berry(cols, r=7.0)(c)
        for y in range(N):
            for x in range(N):
                if c.get(x, y) in cols[:2] and ((x + 2 * y) % 5 == 0 or (x - 2 * y) % 5 == 0):
                    c.px(x, y, cols[2])
    return berry(d)


def i_grepa_berry():
    """A bunch of small round fruit, pale gold."""
    cols = ((250, 240, 170), (218, 196, 92), (148, 124, 40))
    def d(c):
        for cx, cy in ((8, 8), (13, 7), (10.5, 11.5), (15.5, 11), (8, 14), (13, 14.5)):
            sphere(c, cx, cy, 2.9, cols, hi=None)
            c.px(int(cx - 1), int(cy - 1), W)
        stem(c, 11, 1, 4, 2)
    return berry(d)


def i_tamato_berry():
    """A tomato: red, round, its sepals."""
    cols = ((246, 120, 90), (216, 62, 44), (136, 30, 24))
    def d(c):
        round_berry(cols, cy=11, r=7.0, sy=0.88)(c)
        c.ascii(8, 3, ["X  X  X", " XXXXX ", "  XXX  "], {"X": G3})
    return berry(d)


def i_cornn_berry():
    """A cob of corn: its kernels in rows, a husk either side."""
    cols = ((202, 140, 210), (150, 76, 160), (88, 40, 98))
    def d(c):
        for y in range(2, 17):
            half = 3 if 3 < y < 15 else 2
            for x in range(12 - half, 12 + half):
                c.px(x, y, cols[0] if (x + y) % 2 == 0 else cols[1])
            c.px(12 + half - 1, y, cols[2])
        for y in range(8, 17):                          # the husk, a leaf either side, opening out
            w = (y - 8) // 3
            c.rect(8 - w, y, 8, y, KRAFT), c.rect(15, y, 15 + w, y, KRAFT_D)
    return berry(d)


def i_magost_berry():
    """A mangosteen: a dark purple round, its thick crown of sepals."""
    cols = ((176, 96, 150), (120, 44, 100), (66, 22, 58))
    def d(c):
        round_berry(cols, r=6.8)(c)
        c.ascii(8, 2, [" X X X ", "XXXXXXX", " XXXXX "], {"X": G3})
    return berry(d)


def i_rabuta_berry():
    """A rambutan: a round fruit, hairy all over."""
    cols = ((238, 150, 96), (204, 90, 52), (128, 50, 30))
    def d(c):
        round_berry(cols, r=5.6)(c)
        for k in range(16):
            a = math.radians(k * 22.5)
            x, y = 11.5 + 7.2 * math.cos(a), 10.5 - 7.2 * math.sin(a)
            if y < 16:
                c.px(int(round(x)), int(round(y)), cols[2] if k % 2 else cols[1])
    return berry(d)


def i_nomel_berry():
    """A lemon: pale yellow, its two points."""
    cols = ((252, 246, 170), (234, 220, 92), (166, 150, 40))
    def d(c):
        sphere(c, 11.5, 10.5, 6.6, cols, sy=0.8)
        c.rect(4, 10, 4, 11, cols[1]), c.rect(19, 10, 19, 11, cols[2])
    return berry(d)


def i_spelon_berry():
    """A long red fruit, spined."""
    cols = ((246, 118, 98), (214, 56, 50), (130, 28, 30))
    def d(c):
        sphere(c, 11.5, 10, 5.0, cols, sy=1.35)
        for y in range(4, 16, 3):
            c.px(5 + (y % 2), y, cols[2]), c.px(18 - (y % 2), y, cols[2])
        c.px(11, 2, cols[2]), c.px(12, 1, cols[2])
    return berry(d)


def i_pamtre_berry():
    """A long pink fruit, banded."""
    cols = ((238, 170, 214), (204, 106, 172), (130, 54, 110))
    def d(c):
        sphere(c, 11.5, 10, 5.2, cols, sy=1.25)
        for y in (6, 9, 12, 15):
            for x in range(N):
                if c.get(x, y) == cols[1]:
                    c.px(x, y, cols[2])
        stem(c, 11, 1, 3)
    return berry(d)


def i_watmel_berry():
    """A melon, round and big, striped."""
    cols = ((252, 176, 192), (228, 110, 140), (150, 52, 80))
    def d(c):
        round_berry(cols, r=7.6, cy=9.6)(c)
        for x in (7, 11, 15):
            for y in range(N):
                if c.get(x, y) in cols[:2]:
                    c.px(x, y, cols[2])
    return berry(d)


def i_durin_berry():
    """A durian: khaki, round, thorned all over."""
    cols = ((198, 196, 120), (150, 148, 70), (92, 90, 36))
    def d(c):
        round_berry(cols, r=6.0)(c)
        for y in range(N):
            for x in range(N):
                if c.get(x, y) == cols[1] and (x + 3 * y) % 5 == 0:
                    c.px(x, y, cols[2])
        for k in range(10):
            a = math.radians(k * 36 + 18)
            x, y = 11.5 + 7.0 * math.cos(a), 10.5 - 7.0 * math.sin(a)
            if y < 16:
                c.px(int(round(x)), int(round(y)), cols[2])
    return berry(d)


def i_belue_berry():
    """A glossy dark berry, plum-black, a point at its foot."""
    cols = ((150, 112, 172), (88, 52, 110), (46, 24, 62))
    def d(c):
        round_berry(cols, r=6.4, cy=10)(c)
        c.px(11, 17, cols[2]), c.px(12, 17, cols[2])
        stem(c, 12, 2, 3)
    return berry(d)


ICONS4 = [
    ("nugget", "NUGGET", ["ITEM_NUGGET"], i_nugget, "own", "a lump of gold, its gleam"),
    ("pearl", "PEARL", ["ITEM_PEARL"], i_pearl, "own", "a small pearl, silver, sparkling"),
    ("big_pearl", "BIG PEARL", ["ITEM_BIG_PEARL"], i_big_pearl, "own", "the pearl, grown large"),
    ("stardust", "STARDUST", ["ITEM_STARDUST"], i_stardust, "own", "a heap of red sand, loose grains, a glint"),
    ("star_piece", "STAR PIECE", ["ITEM_STAR_PIECE"], i_star_piece, "own", "a red faceted star, one arm broken off"),
    ("tiny_mushroom", "TINYMUSHROOM", ["ITEM_TINY_MUSHROOM"], i_tiny_mushroom, "own", "one small mushroom"),
    ("big_mushroom", "BIG MUSHROOM", ["ITEM_BIG_MUSHROOM"], i_big_mushroom, "own", "the mushroom, large, spotted"),
    ("heart_scale", "HEART SCALE", ["ITEM_HEART_SCALE"], i_heart_scale, "own", "a pale heart-shaped scale, growth lines, a soft rainbow sheen"),
    ("red_shard", "RED SHARD", ["ITEM_RED_SHARD"], i_red_shard, "own", "a broken piece of an old tool, a cut groove; red"),
    ("blue_shard", "BLUE SHARD", ["ITEM_BLUE_SHARD"], i_blue_shard, "own", "the shard; blue"),
    ("yellow_shard", "YELLOW SHARD", ["ITEM_YELLOW_SHARD"], i_yellow_shard, "own", "the shard; yellow"),
    ("green_shard", "GREEN SHARD", ["ITEM_GREEN_SHARD"], i_green_shard, "own", "the shard; green"),
    ("moomoo_milk", "MOOMOO MILK", ["ITEM_MOOMOO_MILK"], i_moomoo_milk, "own", "a milk bottle, white; HP green cap and band"),
    ("lava_cookie", "LAVA COOKIE", ["ITEM_LAVA_COOKIE"], i_lava_cookie, "own", "a cookie on a hot grey stone, five flecks: every state"),
    ("glitter_mail", "GLITTER MAIL", ["ITEM_GLITTER_MAIL"], i_glitter_mail, "own", "a letter sheet, SPIKE's jag in SIGNAL's hue, glitter"),
    ("shadow_mail", "SHADOW MAIL", ["ITEM_SHADOW_MAIL"], i_shadow_mail, "own", "the sheet, FADING in LATENT's hue, fading out"),
    ("dream_mail", "DREAM MAIL", ["ITEM_DREAM_MAIL"], i_dream_mail, "own", "the sheet, its print a dashed outline, waiting"),
    ("fab_mail", "FAB MAIL", ["ITEM_FAB_MAIL"], i_fab_mail, "own", "the sheet, a gold lattice print"),
    ("retro_mail", "RETRO MAIL", ["ITEM_RETRO_MAIL"], i_retro_mail, "own", "the sheet, three small grey daemons"),
    ("red_scarf", "RED SCARF", ["ITEM_RED_SCARF"], i_red_scarf, "own", "a parade scarf, tied, banded tails, fringe; red"),
    ("blue_scarf", "BLUE SCARF", ["ITEM_BLUE_SCARF"], i_blue_scarf, "own", "the scarf; blue"),
    ("green_scarf", "GREEN SCARF", ["ITEM_GREEN_SCARF"], i_green_scarf, "own", "the scarf; green, a clover at its knot (CLOVER DAY)"),
    ("yellow_scarf", "YELLOW SCARF", ["ITEM_YELLOW_SCARF"], i_yellow_scarf, "own", "the scarf; yellow"),
    ("peer_review", "PEER REVIEW", ["ITEM_DEVON_GOODS"], i_peer_review, "own", "a sheet of signatures, a wax seal on a ribbon"),
    ("envelope", "ENVELOPE", ["ITEM_LETTER"], i_envelope, "own", "an envelope, wax-sealed, addressed, stamped"),
    ("meteorite", "METEORITE", ["ITEM_METEORITE"], i_meteorite, "own", "a pitted lump of dark iron, a glint"),
    ("powder_jar", "POWDER JAR", ["ITEM_POWDER_JAR"], i_powder_jar, "own", "a glass jar, lid on, two thirds powder, a label"),
    ("razz_berry", "RAZZ BERRY", ["ITEM_RAZZ_BERRY"], i_razz_berry, "own", "on the TRAP TABLE's plank: a raspberry"),
    ("bluk_berry", "BLUK BERRY", ["ITEM_BLUK_BERRY"], i_bluk_berry, "own", "the plank: a blueberry, its crown"),
    ("nanab_berry", "NANAB BERRY", ["ITEM_NANAB_BERRY"], i_nanab_berry, "own", "the plank: a banana"),
    ("wepear_berry", "WEPEAR BERRY", ["ITEM_WEPEAR_BERRY"], i_wepear_berry, "own", "the plank: a pear"),
    ("pinap_berry", "PINAP BERRY", ["ITEM_PINAP_BERRY"], i_pinap_berry, "own", "the plank: a pineapple"),
    ("pomeg_berry", "POMEG BERRY", ["ITEM_POMEG_BERRY"], i_pomeg_berry, "own", "the plank: a pomegranate"),
    ("kelpsy_berry", "KELPSY BERRY", ["ITEM_KELPSY_BERRY"], i_kelpsy_berry, "own", "the plank: a blue root"),
    ("qualot_berry", "QUALOT BERRY", ["ITEM_QUALOT_BERRY"], i_qualot_berry, "own", "the plank: a dimpled yellow round"),
    ("hondew_berry", "HONDEW BERRY", ["ITEM_HONDEW_BERRY"], i_hondew_berry, "own", "the plank: a netted honeydew"),
    ("grepa_berry", "GREPA BERRY", ["ITEM_GREPA_BERRY"], i_grepa_berry, "own", "the plank: a bunch, pale gold"),
    ("tamato_berry", "TAMATO BERRY", ["ITEM_TAMATO_BERRY"], i_tamato_berry, "own", "the plank: a tomato"),
    ("cornn_berry", "CORNN BERRY", ["ITEM_CORNN_BERRY"], i_cornn_berry, "own", "the plank: a purple cob in its husk"),
    ("magost_berry", "MAGOST BERRY", ["ITEM_MAGOST_BERRY"], i_magost_berry, "own", "the plank: a mangosteen"),
    ("rabuta_berry", "RABUTA BERRY", ["ITEM_RABUTA_BERRY"], i_rabuta_berry, "own", "the plank: a hairy rambutan"),
    ("nomel_berry", "NOMEL BERRY", ["ITEM_NOMEL_BERRY"], i_nomel_berry, "own", "the plank: a lemon"),
    ("spelon_berry", "SPELON BERRY", ["ITEM_SPELON_BERRY"], i_spelon_berry, "own", "the plank: a long red fruit, spined"),
    ("pamtre_berry", "PAMTRE BERRY", ["ITEM_PAMTRE_BERRY"], i_pamtre_berry, "own", "the plank: a long pink fruit, banded"),
    ("watmel_berry", "WATMEL BERRY", ["ITEM_WATMEL_BERRY"], i_watmel_berry, "own", "the plank: a big striped melon"),
    ("durin_berry", "DURIN BERRY", ["ITEM_DURIN_BERRY"], i_durin_berry, "own", "the plank: a thorned durian"),
    ("belue_berry", "BELUE BERRY", ["ITEM_BELUE_BERRY"], i_belue_berry, "own", "the plank: a glossy plum-black berry"),
]
APPROVED = APPROVED + [e[0] for e in ICONS4]      # Build all 47, keep all 20 berries, 2026-11-09


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


def draft(out, batch=1):
    icons = {1: ICONS, 2: ICONS2, 3: ICONS3, 4: ICONS4}[batch]
    if batch != 1:
        out = os.path.join(out, "batch%d" % batch)
    os.makedirs(out, exist_ok=True)
    made = {}
    for e in icons:
        idx, pal = make(e)
        p_image(idx, pal).save(os.path.join(out, e[0] + ".png"))
        with open(os.path.join(out, e[0] + ".pal"), "w", newline="") as f:
            f.write(jasc_text(pal))
        made[e[0]] = (idx, pal)
    texts = item_texts()
    if batch == 1:
        sheet(out, made, texts)
        mocks(out, made, texts)
    elif batch == 2:
        sheet(out, made, texts, icons, batch)
        mocks2(out, made, texts)
    elif batch == 3:
        sheet(out, made, texts, icons, batch)
        mocks3(out, made, texts)
    else:
        sheet(out, made, texts, icons, batch)
        mocks4(out, made, texts)
    print("  drafted %d icons into %s, the sheet and the BAG mocks" % (len(made), os.path.relpath(out, ROOT)))


def sheet(out, made, texts, icons=None, batch=1):
    icons = icons or ICONS
    F, Fs, Fb = label_font(12), label_font(11), label_font(15)
    cols, cw, ch = 3, 520, 128
    rows = (len(icons) + cols - 1) // cols
    head = 92
    im = Image.new("RGB", (cols * cw + 20, head + rows * ch + 10), (28, 30, 36))
    d = ImageDraw.Draw(im)
    d.text((14, 10), "T-525 DRAFT -- the item icons, batch %d (%d): what each DAEMONS item IS, drawn by hand in code "
                     "(no AI image). 24x24, own 16-colour palette, index 0 clear." % (batch, len(icons)),
           fill=(232, 232, 232), font=Fb)
    d.text((14, 34), "Each: the engine's icon now (1x, 4x) | ours (1x, 4x) on the BAG's grey. Colour: a cure wears the "
                     "STATE it ends; HP items the HP bar's green, their tier by how full; PLUGIN/DRIVER their type's "
                     "palette.", fill=(190, 190, 196), font=F)
    d.text((14, 54), ("Nothing is in the engine. Approve some or all: gbaitemicons.py --write --approved ITEM ... "
                      "(an unnamed item keeps its row).") if batch == 1 else
           ("Batches 1-3 are built. Nothing here is in the engine. Families: shards, MAIL, scarves by their named "
            "colour or print; berries on the TRAP TABLE's plank. Approve: --write --approved ITEM ...")
           if batch == 4 else
           ("Batches 1 and 2 are built. Nothing here is in the engine. GAINs: one amplifier, the type's hue the only "
            "difference. TRAPs: the STATE's colour; flavours: HP + and a taste. Approve: --write --approved ITEM ...")
           if batch == 3 else
           ("Batch 1 is built. Nothing here is in the engine. The inputs AXIOM, EMBEDDING, AFFECT, REWARD wear the type "
            "their MUSAI branch becomes; the rest neutrals. Approve: --write --approved ITEM ..."),
           fill=(190, 190, 196), font=F)
    vfiles = vanilla_files()
    bgc = (184, 176, 160)
    for n, e in enumerate(icons):
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
    im.save(os.path.join(out, "t525_item_icons_sheet.png" if batch == 1 else "t525_item_icons_batch%d_sheet.png" % batch))


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


def mocks2(out, made, texts):
    """Batch 2 in the BAG at 240x160: the ITEMS pocket and the KEY ITEMS pocket, ours above the engine's now."""
    by_name = {e[1]: e for e in ICONS2}
    pocket = [("TUNE ATTACK", 2), ("MEMORY", 1), ("AXIOM", 1), ("WAKE TONE", 1), ("CHARGE ALL", 2), ("FRESH WATER", 3)]
    keys = [("TOKEN CASE", 0), ("RESOLVER", 0), ("S.S. TICKET", 0), ("OLD CORE", 0), ("PUBLIC KEY", 0), ("TRAP TABLE", 0)]

    def ours(nm):
        return rgba(*made[by_name[nm][0]])

    def now(nm):
        return engine_icon(by_name[nm][2][0])[0]

    frames = []
    for rows, s, pk, fr in [(pocket, 0, "ITEMS", 0), (pocket, 2, "ITEMS", 0), (pocket, 4, "ITEMS", 0),
                            (keys, 1, "KEY ITEMS", 1), (keys, 2, "KEY ITEMS", 1), (keys, 4, "KEY ITEMS", 1)]:
        e = by_name[rows[s][0]]
        desc = wrap208(texts[e[2][0]]["description_english"].replace("\\n", " "))
        frames.append((bag_mock(ours, rows, s, desc, pk, fr), bag_mock(now, rows, s, desc, pk, fr)))
    strip = Image.new("RGB", (3 * 248 + 8, 4 * 168 + 8 + 40), (28, 30, 36))
    d = ImageDraw.Draw(strip)
    d.text((8, 6), "Batch 2 in the BAG at 240x160: each pair ours above, the engine's now below. Only the icon changes.",
           fill=(220, 220, 224), font=label_font(12))
    for i, (a, b) in enumerate(frames):
        x, y = 8 + (i % 3) * 248, 40 + (i // 3) * 2 * 168
        strip.paste(a, (x, y))
        strip.paste(b, (x, y + 168))
    strip.save(os.path.join(out, "bag_mocks_batch2.png"))
    frames[0][0].resize((480, 320), Image.NEAREST).save(os.path.join(out, "bag_mock_batch2_2x.png"))


def print_small(im, x, y, s, ink, shadow):
    """The engine's latin_small sheet and widths: what the TRAP TABLE numbers its rows in."""
    import fontwidth
    sheet = Image.open(os.path.join(GBA, "graphics/fonts/latin_small.png"))
    w, cm = fontwidth.glyph_widths("sFontSmallLatinGlyphWidths"), fontwidth.charmap(GBA)
    fp, px = sheet.load(), im.load()
    for ch in s:
        b = cm.get(ch)
        if b is None:
            continue
        gx, gy = (b % 32) * 8, (b // 32) * 16          # the small sheet's cells are 8x16, 32 to a row
        for yy in range(16):
            for xx in range(min(8, w[b])):
                v = fp[gx + xx, gy + yy]
                if 0 <= x + xx < im.width and 0 <= y + yy < im.height:
                    if v == 1:
                        px[x + xx, y + yy] = ink
                    elif v == 2:
                        px[x + xx, y + yy] = shadow
        x += w[b]
    return x


def pouch_mock(icon_for, rows, selected, description):
    """240x160: the TRAP TABLE as the engine draws it (src/berry_pouch.c): graphics/berry_pouch/background.png + .bin +
    .gbapal, the pouch sprite centred at (40,76), the list in window 0 (11,1) -- "No" and the two-digit number in the
    small font, the name in the normal, x3 at 110 -- DARK_GRAY on LIGHT_GRAY (the list's cursorPal 2, shadow 3), the
    description in window 1 (5,16), the header in window 2, and the icon where CreateBerryPouchItemIcon puts it (centre
    24,147: the 24x24 icon's top left at 8,131)."""
    bp = os.path.join(GBA, "graphics/berry_pouch")
    im = Image.new("RGB", (240, 160), (0, 0, 0))
    tiles = Image.open(os.path.join(bp, "background.png"))
    tp, tw = tiles.load(), tiles.width // 8
    pal = gbapal(os.path.join(bp, "background.gbapal"))
    tm = open(os.path.join(bp, "background.bin"), "rb").read()
    px = im.load()
    for ty in range(20):
        for tx in range(30):
            e = tm[(ty * 32 + tx) * 2] | tm[(ty * 32 + tx) * 2 + 1] << 8
            t, hf, vf, pn = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
            for y in range(8):
                for x in range(8):
                    sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                    v = tp[(t % tw) * 8 + sx, (t // tw) * 8 + sy] if t // tw < tiles.height // 8 else 0
                    px[tx * 8 + x, ty * 8 + y] = pal[(pn * 16 + v) % len(pal)] if v else pal[0]
    spr = Image.open(os.path.join(bp, "berry_pouch.png"))
    sp = gbapal(os.path.join(bp, "berry_pouch.gbapal"))
    spx = spr.load()
    for y in range(64):
        for x in range(64):
            if spx[x, y]:
                px[8 + x, 44 + y] = sp[spx[x, y]]
    std = jasc_read(os.path.join(GBA, "graphics/interface/std_menu.pal"))
    WHITE, DARK, LIGHT = std[1], std[2], std[3]
    import fontwidth
    w, cm = fontwidth.font(GBA)
    head = "TRAP TABLE"
    print_text(im, 8 + (72 - sum(w[cm[ch]] for ch in head if ch in cm)) // 2, 9, head, WHITE, DARK)
    for i, (num, nm, qty) in enumerate(rows):
        y = 8 + 2 + i * 16
        if i == selected:
            print_text(im, 88 + 1, y, "\u25b6", DARK, LIGHT)
        x = print_small(im, 88 + 9, y, "No%02d " % num, DARK, LIGHT)
        print_text(im, x, y, nm, DARK, LIGHT)
        print_small(im, 88 + 110, y, "\u00d7%3d" % qty, DARK, LIGHT)
    for j, line in enumerate(description):
        print_text(im, 40, 128 + 2 + j * 14, line, WHITE, DARK)
    ic = icon_for(rows[selected][1])
    im.paste(ic, (8, 131), ic)
    return im


def mocks3(out, made, texts):
    """Batch 3 at 240x160: the held items in the BAG's ITEMS pocket, and the TRAPs in the TRAP TABLE (the berry pouch,
    where they live), ours above the engine's now."""
    by_name = {e[1]: e for e in ICONS3}

    def ours(nm):
        return rgba(*made[by_name[nm][0]])

    def now(nm):
        return engine_icon(by_name[nm][2][0])[0]

    held = [("HEADROOM", 1), ("LOGIC GAIN", 1), ("QUEUE JUMP", 1), ("FAILSAFE", 1), ("FLOW GAIN", 1), ("DITHER", 1)]
    held2 = [("WEIGHT SHARE", 1), ("VERSION LOCK", 1), ("SIGNAL GAIN", 1), ("HARD CODED", 1), ("MUTE", 1), ("SURCHARGE", 1)]
    traps = [(n, nm, q) for n, nm, q in [(1, "THROTTLE TRAP", 2), (3, "LEAK TRAP", 1), (5, "HANG TRAP", 1),
                                         (7, "LOW MARK", 4), (9, "CATCH ALL", 1), (12, "DRY TRAP", 2)]]
    frames = []
    for rows, s in ((held, 0), (held, 1), (held2, 0)):
        e = by_name[rows[s][0]]
        desc = wrap208(texts[e[2][0]]["description_english"].replace("\\n", " "))
        frames.append((bag_mock(ours, rows, s, desc, "ITEMS", 0), bag_mock(now, rows, s, desc, "ITEMS", 0)))
    for s in (0, 3, 5):
        e = by_name[traps[s][1]]
        desc = texts[e[2][0]]["description_english"].split("\\n")    # as authored: the window prints its own breaks
        frames.append((pouch_mock(ours, traps, s, desc), pouch_mock(now, traps, s, desc)))
    strip = Image.new("RGB", (3 * 248 + 8, 4 * 168 + 8 + 40), (28, 30, 36))
    d = ImageDraw.Draw(strip)
    d.text((8, 6), "Batch 3 at 240x160: held items in the BAG (top), the TRAPs in the TRAP TABLE (bottom); each pair ours "
                   "above, the engine's now below. Only the icon changes.", fill=(220, 220, 224), font=label_font(12))
    for i, (a, b) in enumerate(frames):
        x, y = 8 + (i % 3) * 248, 40 + (i // 3) * 2 * 168
        strip.paste(a, (x, y))
        strip.paste(b, (x, y + 168))
    strip.save(os.path.join(out, "bag_mocks_batch3.png"))
    frames[0][0].resize((480, 320), Image.NEAREST).save(os.path.join(out, "bag_mock_batch3_2x.png"))
    frames[3][0].resize((480, 320), Image.NEAREST).save(os.path.join(out, "trap_table_mock_batch3_2x.png"))


def mocks4(out, made, texts):
    """Batch 4 at 240x160: the valuables, MAIL and scarves in the BAG's ITEMS pocket, four key items in KEY ITEMS, and
    the berries in the TRAP TABLE; ours above the engine's now."""
    by_name = {e[1]: e for e in ICONS4}

    def ours(nm):
        return rgba(*made[by_name[nm][0]])

    def now(nm):
        return engine_icon(by_name[nm][2][0])[0]

    vals = [("NUGGET", 2), ("BIG PEARL", 1), ("STAR PIECE", 1), ("HEART SCALE", 1), ("RED SHARD", 3), ("MOOMOO MILK", 2)]
    post = [("LAVA COOKIE", 3), ("GLITTER MAIL", 1), ("FAB MAIL", 1), ("RETRO MAIL", 1), ("GREEN SCARF", 1), ("RED SCARF", 1)]
    keys = [("PEER REVIEW", 0), ("ENVELOPE", 0), ("METEORITE", 0), ("POWDER JAR", 0)]
    berries = [(16, "RAZZ BERRY", 3), (17, "BLUK BERRY", 1), (19, "WEPEAR BERRY", 2), (20, "PINAP BERRY", 1),
               (31, "SPELON BERRY", 1), (33, "WATMEL BERRY", 1)]
    frames = []
    for rows, s, pk, fr in ((vals, 0, "ITEMS", 0), (vals, 3, "ITEMS", 0), (post, 1, "ITEMS", 0),
                            (post, 4, "ITEMS", 0), (keys, 0, "KEY ITEMS", 1), (keys, 2, "KEY ITEMS", 1)):
        e = by_name[rows[s][0]]
        desc = wrap208(texts[e[2][0]]["description_english"].replace("\\n", " "))
        frames.append((bag_mock(ours, rows, s, desc, pk, fr), bag_mock(now, rows, s, desc, pk, fr)))
    for s in (0, 3, 5):
        e = by_name[berries[s][1]]
        desc = texts[e[2][0]]["description_english"].split("\\n")
        frames.append((pouch_mock(ours, berries, s, desc), pouch_mock(now, berries, s, desc)))
    strip = Image.new("RGB", (3 * 248 + 8, 6 * 168 + 8 + 40), (28, 30, 36))
    d = ImageDraw.Draw(strip)
    d.text((8, 6), "Batch 4 at 240x160: ITEMS, KEY ITEMS, the TRAP TABLE's berries. Each pair ours above, the engine's",
           fill=(220, 220, 224), font=label_font(12))
    d.text((8, 22), "now below. Only the icon changes.", fill=(220, 220, 224), font=label_font(12))
    for i, (a, b) in enumerate(frames):
        x, y = 8 + (i % 3) * 248, 40 + (i // 3) * 2 * 168
        strip.paste(a, (x, y))
        strip.paste(b, (x, y + 168))
    strip.save(os.path.join(out, "bag_mocks_batch4.png"))
    frames[0][0].resize((480, 320), Image.NEAREST).save(os.path.join(out, "bag_mock_batch4_2x.png"))
    frames[6][0].resize((480, 320), Image.NEAREST).save(os.path.join(out, "trap_table_mock_batch4_2x.png"))


def report():
    rows, files, vfiles = table_rows(), symbol_files(), vanilla_files()
    print("  T-525 item icons, batches 1-4: %d icons, %d approved (the user, 2026-11-07: \"Build all 41\", \"Build all 47\", \"Build all 57\"; 2026-11-09: \"Build all\", \"Keep all 20\")"
          % (len(ICONS) + len(ICONS2) + len(ICONS3) + len(ICONS4), len(APPROVED)))
    for e in ICONS + ICONS2 + ICONS3 + ICONS4:
        key, name, items, _, mode, what = e
        idx, pal = make(e)
        stem = files[rows[items[0]][0]]
        state = "ours" if stem in vfiles else "pret's"
        target = {"own": "icons/d_%s.png" % key, "tmhm": "icons/tm_hm.png (in place)", "driver": "icons/driver.png"}[mode]
        used = len({v for row in idx for v in row} - {0})
        print("    %-14s %-20s now %-16s (%-6s) -> %-28s %2d colours" % (name, items[0], stem, state, target, used))
    print("  --draft draws them and the sheet; --write --approved ITEM ... writes the named ones.")


def _png_same(path, im):
    if not os.path.exists(path):
        return False
    old = Image.open(path)
    return old.mode == "P" and old.size == im.size and list(old.getdata()) == list(im.getdata()) and \
        (old.getpalette() or [])[:48] == im.getpalette()[:48]


def plan(keys):
    """What a write of the named items makes: ({png path: image}, {text path: contents}, [what each is]).
    Nothing is written here, so the report can say whether the engine already holds it."""
    chosen = [e for e in ICONS + ICONS2 + ICONS3 + ICONS4 if e[0] in keys or e[1] in keys or any(i in keys for i in e[2])]
    pngs, texts, said = {}, {}, []
    items_h, graphics_h, table = open(ITEMS_H).read(), open(GRAPHICS_H).read(), open(TABLE).read()
    for e in chosen:
        key, name, items, _, mode, _ = e
        idx, pal = make(e)
        if mode == "tmhm":
            pngs[os.path.join(ICON_DIR, "tm_hm.png")] = p_image(idx, pal)
            said.append("icons/tm_hm.png (every PLUGIN keeps its type palette)")
            continue
        sym = "D" + "".join(p.capitalize() for p in key.split("_"))
        stem = "driver" if mode == "driver" else "d_" + key
        pngs[os.path.join(ICON_DIR, stem + ".png")] = p_image(idx, pal)
        decl = 'const u32 gItemIcon_%s[] = INCBIN_U32("graphics/items/icons/%s.4bpp.lz");   %s\n' % (sym, stem, TAG)
        if mode != "driver":
            texts[os.path.join(PALS, stem + ".pal")] = jasc_text(pal)
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
        said.append("%s (%s)" % (stem, ", ".join(items[:3]) + (" ..." if len(items) > 3 else "")))
    texts[ITEMS_H], texts[GRAPHICS_H], texts[TABLE] = items_h, graphics_h, table
    return pngs, texts, said


def differs(keys):
    """The engine files a write of these items would change."""
    pngs, texts, _ = plan(keys)
    out = [p for p, im in pngs.items() if not _png_same(p, im)]
    out += [p for p, t in texts.items() if not os.path.exists(p) or open(p, newline="").read().replace("\r\n", "\n")
            != t.replace("\r\n", "\n")]
    return [os.path.relpath(p, GBA) for p in out]


def write(keys):
    import shutil
    pngs, texts, said = plan(keys)
    if not said:
        print("  nothing named matches the batch")
        return 1
    for p, im in pngs.items():
        if not _png_same(p, im):
            im.save(p)
    for p, t in texts.items():
        old = open(p, newline="").read() if os.path.exists(p) else None
        if old is not None and old.replace("\r\n", "\n") == t.replace("\r\n", "\n"):
            continue
        tmp = p + ".tmp"
        with open(tmp, "w", newline="") as f:
            f.write(t)
        if old is not None:
            shutil.copymode(p, tmp)
        os.replace(tmp, p)
    for s_ in said:
        print("  written " + s_)
    print("  now build all four ROMs and check each exit code")
    return 0


def main():
    if A.write:
        if not A.approved:
            print("  --write refuses without --approved: the user picks from the sheet first (T-525).")
            return 0
        keys = [e[0] for e in ICONS + ICONS2 + ICONS3 + ICONS4] if A.all else (A.items or APPROVED)
        if not keys:
            print("  --write --approved names no items, and none is approved yet: nothing written.")
            return 0
        return write(set(keys))
    if A.draft:
        draft(A.draft, A.batch)
        return 0
    report()
    if APPROVED:
        d = differs(set(APPROVED))
        if d:
            print("  the engine is NOT what the approved write makes: %d files (%s%s) -- run --write --approved --all"
                  % (len(d), ", ".join(d[:4]), " ..." if len(d) > 4 else ""))
            return 1
        print("  the engine holds every approved icon (%d of %d)" % (len(APPROVED), len(ICONS) + len(ICONS2) + len(ICONS3) + len(ICONS4)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
