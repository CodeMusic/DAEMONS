#!/usr/bin/env python3
"""The landmarks, drawn from the story into their own footprints (T-447, docs/private/plan-landmarks-2026-10-24.md).

    python3 tools/gbalandmarks.py                       # report: each landmark's footprint, the tiles it owns, the
                                                        #   budget its drawing uses; nothing written
    python3 tools/gbalandmarks.py --draft [DIR]         # the drafts: per landmark gfx/drafts/landmarks/<name>/ (the
                                                        #   drawing at 1x and 3x, its cells), per tileset
                                                        #   gfx/drafts/landmarks/<tileset>/ (tiles.png, metatiles.bin,
                                                        #   metatile_attributes.bin, the map's map.bin, the new .pal rows)
    python3 tools/gbalandmarks.py --draft --sheets DIR  # and the review sheets in DIR (t447a_*.png)
    python3 tools/gbalandmarks.py --write --approved    # into the engine -- REFUSES without --approved, and writes only
                                                        #   the landmarks in APPROVED (none yet: the first pair is a draft)

THE FIRST PAIR (the user, 2026-10-24) -- QUICKSILVER IS., one tileset (secondary/cinnabar_island), one campus:

  SCORN SOLUTIONS (CinnabarIsland, 7x4 at (5,6), door (8,9)). CRYSTAL CLEAR's lab's sister, drawn in gbalab.py's hand
  -- pale stone in courses, a flat slate roof inside a parapet, tall two-pane windows on sills, a plinth -- and then
  PROCESSED, as 4.24 has the campus's intact half processed into a company that sells what it studied:
    * gold leaf laid over the parapet's front, one corner (lower right) lifting onto the paler board beneath;
    * every window half drawn with the SAME blind, to the same slat;
    * the slate ruled into boxes like a form, and one box ticked;
    * a small intake slot in the wall by the door;
    * the board SCORN SOLUTIONS over CLEAR LABORATORY kept exactly as gbaislandsigns.py drew it (T-86's gold leaf);
    * the only red is the new owner's procedure: the tick, and the slot's lip. (4.4: give him the red, never say it.)
  Its door cell is KEPT, block and tiles: METATILE_CinnabarIsland_LabDoor plays gbadoors.py's cinnabar_lab frames in
  row 3, keyed by block id, so a new door would mean new frames and a new palette row in field_door.c.

  the MANSION (CinnabarIsland, 7x4 at (5,0), door (8,3), and the porch below it). The campus's burned half, redrawn
  in its footprint, no vanilla left: the roof caved in where the work was, the racks and cooling coils standing in
  the gap like ribs, soot running UP the wall from every blown window, the colour gone to ash, quicksilver beaded and
  pooled in the gutters. The process is heat (ANNEAL, ENTROPY); nobody is blamed, and nothing on it says who.

WHERE IT GOES, measured rather than assumed (the census in the report proves each line on the real files):

  OWNED CELLS. Every cell of a landmark gets its own new block (vanilla reused one roof block across five cells), its
  attributes copied from the block it replaces and its collision and elevation bits kept -- so no footprint, door,
  or collision cell moves (T-125). The art goes in the layer vanilla drew in: the TOP layer over the ground the cell
  already had; the mansion's door (a non-animated door, MB 0x60) keeps its lintel on top so the player still passes
  under it; the lab's two sign cells keep the board's own tiles over a wall of ours.

  OWNED TILES. A secondary tile is the landmarks' to repaint when every cell, on every layout this tileset draws
  (QUICKSILVER, ROUTE 20, ROUTE 21 South, three RS Safari layouts), and every border, that draws it is one of OUR
  cells; plus the slots no block draws, 346..375. NEVER 376..383: DOOR_TILE_START, where field_door.c writes a door's
  frames into VRAM (engine.md trap 39's kind), and QUICKSILVER has an animated door. The drawing is cut into 8x8
  tiles de-duplicated with flips and placed in those slots; a run that needs more refuses.

  OWN ROWS. Rows 10 (SCORN SOLUTIONS) and 11 (the MANSION) of the tileset are unused (black), so each landmark has a
  sixteen-colour row of its own and no other block's colour moves. Row 7 is gbacivic.py's (ENTROPY's amber).

  NEIGHBOURS. ROUTE 21 South joins at the top edge and ROUTE 20 at the right; both draw with this same secondary
  tileset, so a new block draws the same from either side (engine.md trap 14).

  gbatowns.py's LANDMARKS table keeps these boxes out of T-438's town passes; OWNS below is this tool's claim on the
  same boxes, and the report fails if the two disagree (it reads the table, it does not import that tool: trap 16).
"""
import ast, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal, write_pal
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFTS = os.path.join(ROOT, "gfx", "drafts", "landmarks")
PRIMARY = os.path.join(GBA, "data/tilesets/primary/general")
RULES = os.path.join(GBA, "tileset_rules.mk")

ARGS = sys.argv[1:]
WRITE = "--write" in ARGS
APPROVED_FLAG = "--approved" in ARGS


def argval(flag, default=None):
    if flag in ARGS:
        i = ARGS.index(flag)
        if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--"):
            return ARGS[i + 1]
        return default
    return None


DRAFT = argval("--draft", DRAFTS)
SHEETS = argval("--sheets")

#  the landmarks the user has approved for --write; a draft is never written
APPROVED = set()

NUM_PRIMARY = 640
SECONDARY_TILES = 1024 - 640
DOOR_TILE_START = 1024 - 8 - 640          # 376: field_door.c's frames land in the last eight tiles of VRAM
SECONDARY_METATILES = 1024 - 640

# ============================================================================================ the palette rows
#  Each colour is named by its role; the drawing asks for roles, never numbers. Index 0 is the tileset's own
#  transparent green, as every row of this tileset has it.
TRANSPARENT = (124, 192, 104)

SCORN_ROW = 10
SCORN_COLOURS = [  # CRYSTAL's lab's row 9 (Pallet) is the parent: the same stones and slates, a little colder --
    ("WHITE",  (240, 242, 248)),   # the stone face, lit
    ("STONE",  (216, 220, 232)),   # the stone face
    ("LINE",   (182, 188, 208)),   # courses, the eave's shade, the board under the leaf
    ("PLINTH", (150, 160, 180)),   # the parapet, the plinth, the sills
    ("SLATEL", (120, 122, 140)),   # the form's rules on the slate
    ("SLATE",  (88, 90, 112)),     # the slate
    ("OUT",    (54, 60, 88)),      # outline, the darkest slate, the glass's foot
    ("GLASSL", (168, 198, 236)),   # glass catching the light
    ("GLASS",  (104, 146, 210)),   # glass
    ("BLIND",  (222, 218, 196)),   # the blind -- every one the same
    ("BLINDD", (174, 168, 146)),   # its slats' shadow
    ("LEAF",   (250, 226, 128)),   # gold leaf, bright
    ("GOLD",   (216, 174, 72)),    # gold leaf
    ("GOLDD",  (156, 108, 40)),    # gold leaf, deep; the curl's underside
    ("RED",    (198, 34, 44)),     # the new owner's procedure: the tick, the slot's lip. Nothing else.
]
MANSION_ROW = 11
MANSION_COLOURS = [
    ("ASHL",   (204, 198, 188)),   # ash, lit -- what was cream
    ("ASH",    (168, 162, 154)),   # ash
    ("ASHD",   (128, 122, 118)),   # ash in shade, the courses
    ("SOOT",   (88, 82, 84)),      # soot
    ("CHAR",   (56, 50, 56)),      # char, the blown windows
    ("VOID",   (30, 26, 34)),      # outline, the inside of the caved roof
    ("BRICK",  (132, 84, 66)),     # the roof's burnt edge, rust
    ("RUST",   (178, 118, 82)),    # rust, lit
    ("COIL",   (214, 156, 96)),    # the cooling coils, annealed copper
    ("COILL",  (240, 202, 140)),   # a coil's lit turn
    ("RACKD",  (96, 104, 122)),    # the racks' steel, in the dark
    ("RACK",   (146, 154, 170)),   # the racks' steel, lit
    ("QSD",    (112, 126, 150)),   # quicksilver, its shadow
    ("QS",     (186, 198, 216)),   # quicksilver
    ("QSL",    (246, 250, 255)),   # quicksilver's bead of light
]


def role_map(colours):
    return {name: i + 1 for i, (name, _) in enumerate(colours)}


def pal16(colours):
    return [TRANSPARENT] + [rgb for _, rgb in colours]


# ============================================================================================ drawing helpers
class Canvas:
    def __init__(self, w, h, roles):
        self.w, self.h, self.r = w, h, roles
        self.c = [[0] * w for _ in range(h)]

    def v(self, role):
        return role if isinstance(role, int) else self.r[role]

    def px(self, x, y, role):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = self.v(role)

    def get(self, x, y):
        return self.c[y][x] if 0 <= x < self.w and 0 <= y < self.h else 0

    def rect(self, x0, y0, x1, y1, role):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.c[y][x] = self.v(role)

    def hline(self, x0, x1, y, role):
        self.rect(x0, y, x1, y, role)

    def vline(self, x, y0, y1, role):
        self.rect(x, y0, x, y1, role)

    def is_(self, x, y, *roles):
        return self.get(x, y) in {self.v(r) for r in roles}


# ============================================================================================ SCORN SOLUTIONS
#  7x4 cells: 112x64. Canvas rows 0..15 are the walkable top row (the roof's back edge over the ground, which the
#  player passes behind); 16..63 the building. The door cell (canvas 48..63, 48..63) is KEPT, block and tiles.
#  THE BUDGET IS THE DESIGN: the pair has 117 tiles for 58 cells, so everything is drawn on the 8px grid -- the form's
#  boxes are one tile wide, each window is centred on a tile seam so its two halves are one tile and its mirror,
#  the courses run on tile rows -- and only what the story needs is drawn once (the tick, the curl, the slot).
SCORN = dict(name="scorn_solutions", title="SCORN SOLUTIONS", map="CinnabarIsland", x0=5, y0=6, w=7, h=4,
             door=(8, 9), keep=[(8, 9)], signs=[(9, 9), (10, 9)], row=SCORN_ROW, colours=SCORN_COLOURS)
SCORN_WINDOWS = (16, 32, 80, 96)          # each window's centre, on a tile seam


def draw_scorn():
    W, H = 112, 64
    k = Canvas(W, H, role_map(SCORN_COLOURS))
    R = k.rect
    ROOF0, ROOF1, WALL0 = 6, 33, 34

    # --- the roof, from above: a parapet round a flat slate, as hers is
    R(0, ROOF0, W - 1, ROOF1, "OUT")
    R(1, ROOF0 + 1, W - 2, ROOF1 - 1, "PLINTH")              # the parapet
    k.hline(1, W - 2, ROOF0 + 1, "LINE")                     # its lit back edge
    R(5, ROOF0 + 3, W - 6, ROOF1 - 6, "SLATE")               # the slate inside it
    k.hline(5, W - 6, ROOF0 + 3, "OUT")                      # the parapet's inner shadow, back and left
    k.vline(5, ROOF0 + 3, ROOF1 - 6, "OUT")
    k.vline(W - 6, ROOF0 + 3, ROOF1 - 6, "SLATEL")           # its lit right edge
    #  THE FORM: the slate ruled into boxes -- two rows of them, one tile wide each, a printed question (a dash) at
    #  the top of every box and the answer space empty
    top, mid, bot = 11, 19, 26
    for x in range(8, W - 8, 8):
        k.vline(x, top, bot, "SLATEL")
    for y in (top, mid, bot):
        k.hline(8, W - 8, y, "SLATEL")
    for bx in range(8, W - 8, 8):
        for by in (top, mid):
            k.hline(bx + 2, bx + 4, by + 2, "OUT")
    #  ONE box ticked, in the procedure's red (second row, sixth box from the right -- a form is filled in order)
    tx, ty = 64, mid
    for (dx, dy) in ((1, 3), (2, 4), (3, 5), (4, 4), (5, 3), (6, 2), (7, 1)):
        k.px(tx + dx, ty + dy, "RED")
        k.px(tx + dx, ty + dy + 1, "RED")
    #  the parapet's front lip, where the gold leaf is laid
    ly0, ly1 = ROOF1 - 4, ROOF1 - 1                          # 29..32
    R(1, ly0, W - 2, ly1, "PLINTH")

    #  GOLD LEAF over the lip, edge to edge, brushed on a tile's rhythm; its lower right corner lifting onto the paler
    #  board beneath (gbaislandsigns' hand: a bright rolled lip on the leaf's edge, the board's older pale under it)
    lifted = lambda x, y: (x - 94) + (y - ly0) * 3 >= 7
    for y in range(ly0, ly1 + 1):
        for x in range(1, W - 1):
            if lifted(x, y):
                k.px(x, y, "STONE")
            else:
                k.px(x, y, "LEAF" if y == ly0 else "GOLD" if y < ly1 else "GOLDD")
                if y == ly0 + 1 and x % 8 == 3:
                    k.px(x, y, "LEAF")
    for y in range(ly0, ly1 + 1):                            # the curl
        for x in range(2, W - 1):
            if lifted(x, y) and not lifted(x - 1, y):
                k.px(x - 1, y, "WHITE")
                k.px(x - 2, y, "GOLDD")
    for x, y in ((104, ly0 + 2), (104, ly0 + 3), (105, ly0 + 2), (107, ly0 + 1), (107, ly0 + 2), (107, ly0 + 3),
                 (109, ly0 + 1), (109, ly0 + 3)):
        k.px(x, y, "SLATEL")                                  # the older letters, too little of them to read
    k.hline(0, W - 1, ROOF1, "OUT")

    # --- the wall: her pale stone, in courses on the tile rows, the joints every second tile and staggered
    R(0, WALL0, W - 1, H - 1, "OUT")
    R(1, WALL0, W - 2, H - 6, "WHITE")
    k.hline(1, W - 2, WALL0, "LINE")                         # the eave's shade
    k.hline(1, W - 2, WALL0 + 1, "STONE")
    for i, y in enumerate((47, 55)):
        k.hline(1, W - 2, y, "LINE")
        for x in range(8 + 8 * (i % 2), W - 2, 16):
            k.vline(x, y - 7, y - 1, "STONE")
    R(1, H - 5, W - 2, H - 2, "PLINTH")                      # the plinth
    k.hline(1, W - 2, H - 5, "LINE")
    k.hline(0, W - 1, H - 1, "OUT")

    #  her tall two-pane windows on sills, at her rhythm -- each with the SAME blind, drawn to the SAME slat, exactly
    #  half way: the windows are no longer anyone's to look out of
    for c in SCORN_WINDOWS:
        x0, x1 = c - 6, c + 5
        wy0, wy1 = WALL0 + 4, WALL0 + 21                     # 38..55
        R(x0, wy0, x1, wy1, "SLATE")                          # frame
        R(x0 + 1, wy0 + 1, x1 - 1, wy1 - 1, "GLASS")
        k.hline(x0 + 1, x1 - 1, wy1 - 1, "OUT")
        k.hline(x0 + 1, x1 - 1, wy1 - 4, "GLASSL")           # the light on the lower pane, level
        half = (wy0 + wy1) // 2                               # 46
        for y in range(wy0 + 1, half + 1):                    # the blind, down to half
            k.hline(x0 + 1, x1 - 1, y, "BLINDD" if (y - wy0) % 3 == 0 else "BLIND")
        k.hline(x0 + 1, x1 - 1, half + 1, "BLINDD")           # its bar
        k.px(c - 1, half + 2, "BLINDD"); k.px(c, half + 2, "BLINDD")      # the pull, the same every time
        k.hline(x0 - 1, x1 + 1, wy1 + 1, "LINE")             # the sill
        k.hline(x0 - 1, x1 + 1, wy1 + 2, "PLINTH")

    #  the door's surround (the door cell itself is kept): her one line of gold above it, and the plate -- blank on
    #  hers, here leafed over like the parapet. Symmetric about the door's seam (x 56), so it is half its tiles.
    R(47, WALL0 + 6, 64, 47, "GOLDD")
    R(48, WALL0 + 7, 63, 47, "GOLD")
    R(49, WALL0 + 9, 62, 47, "OUT")                          # the transom, dark
    R(50, WALL0 + 10, 61, 46, "GLASS")
    k.hline(50, 61, WALL0 + 10, "GLASSL")
    R(50, WALL0 + 1, 61, WALL0 + 4, "GOLDD")                 # the plate
    k.hline(51, 60, WALL0 + 2, "LEAF")
    k.hline(51, 60, WALL0 + 3, "GOLD")
    #  THE INTAKE SLOT, by the door on its left: a narrow mouth in a steel plate, its lip the procedure's red
    sx0, sy0 = 39, 49
    R(sx0, sy0, sx0 + 5, sy0 + 7, "PLINTH")
    k.hline(sx0, sx0 + 5, sy0, "LINE")
    R(sx0 + 1, sy0 + 3, sx0 + 4, sy0 + 4, "OUT")             # the mouth
    k.hline(sx0 + 1, sx0 + 4, sy0 + 5, "RED")                # its lip
    k.vline(sx0 + 5, sy0 + 1, sy0 + 7, "SLATEL")
    return k


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def smoke(k, c, top, bottom, half):
    """the soot a fire leaves over an opening: a soft stain wider than the opening, darkest just above it and paling
    into the ash as it climbs to the eave, ordered-dithered (the same stain over every window: one window's tiles)"""
    n = bottom - top
    for y in range(top, bottom):
        t = (bottom - 1 - y) / max(1, n - 1)                    # 0 just above the opening, 1 at the eave
        w = half + 1 + t * 3
        for x in range(int(c - w - 1), int(c + w + 1)):
            d = abs(x - c + 0.5) / w
            if d >= 1:
                continue
            dens = (1 - 0.75 * t) * (1 - d * d)
            th = (BAYER[y % 4][x % 4] + 0.5) / 16
            if dens > 0.55 + th * 0.4:
                k.px(x, y, "SOOT")
            elif dens > th * 0.9:
                k.px(x, y, "ASHD")


# ============================================================================================ the MANSION
#  7x5 cells: 112x80. Rows 0..3 the building (all collision but the door), row 4 the porch below the door (cells
#  7..9 only; the rest of row 4 is ground and stays as it is). Drawn on the same 8px grid as SCORN SOLUTIONS: the
#  slates are one tile, the cave-in is a run of rack and coil tiles between two burnt edges that are one tile and
#  its mirror, each window and its plume is centred on a tile seam.
MANSION = dict(name="mansion", title="the MANSION", map="CinnabarIsland", x0=5, y0=0, w=7, h=5,
               door=(8, 3), keep=[], signs=[], row=MANSION_ROW, colours=MANSION_COLOURS,
               cells_only={(x, 4) for x in (7, 8, 9)} | {(x, y) for x in range(5, 12) for y in range(4)})
MANSION_WINDOWS = (16, 32, 80, 96)


def draw_mansion():
    W, H = 112, 80
    k = Canvas(W, H, role_map(MANSION_COLOURS))
    R = k.rect
    ROOF1, GUT0, WALL0, WALL1 = 23, 24, 28, 63

    # --- the roof: ash slates seen from above, in courses, one tile's pattern; the map's top edge cuts it
    def slates(x0, x1, y0, y1, body, joint, lit):
        for y in range(y0, y1 + 1):
            ph, course = y % 4, (y // 4) % 2
            for x in range(x0, x1 + 1):
                if ph == 3:
                    k.px(x, y, joint)                         # the shadow under each course
                elif x % 4 == (0 if course == 0 else 2):
                    k.px(x, y, joint if ph else lit)          # the joints, staggered course to course
                else:
                    k.px(x, y, lit if ph == 0 else body)      # each slate's lit upper edge
    R(0, 0, W - 1, ROOF1, "VOID")
    slates(1, W - 2, 0, ROOF1, "ASHD", "SOOT", "ASH")
    #  scorched: the slates either side of the hole gone to soot, one tile's width
    slates(24, 31, 0, ROOF1, "SOOT", "CHAR", "ASHD")
    slates(80, 87, 0, ROOF1, "SOOT", "CHAR", "ASHD")
    #  THE CAVE-IN, where the work was: x 32..79. Its burnt edges (one tile, and its mirror), and through it the dark
    #  with the racks and the cooling coils standing in it like ribs
    edge = [3, 3, 2, 4, 3, 5, 4, 3, 2, 3, 4, 6, 5, 4, 3, 4, 5, 6, 7, 7]    # the left edge's ragged inset, per row
    for y in range(0, 20):
        e = edge[y]
        R(32 + e, y, 79 - e, y, "VOID")
        k.px(32 + e - 1, y, "BRICK"); k.px(79 - e + 1, y, "BRICK")            # rust round the hole
        if y % 3 == 1:
            k.px(32 + e - 2, y, "RUST"); k.px(79 - e + 2, y, "RUST")
    for x in range(32 + 7, 79 - 7 + 1):                       # the front lip: the roof's last beam, burnt through
        k.px(x, 20, "BRICK" if x % 8 not in (3, 4) else "RUST")
        k.px(x, 21, "VOID")
        k.px(x, 22, "SOOT")
    #  the ribs: a rack in every other tile, a coil between, all standing to the same height
    for col, head in ((40, 6), (48, 3), (56, 2), (64, 5)):
        rack = (col // 8) % 2 == 1
        for y in range(head + 1, 20):
            if rack:                                          # a steel post with shelves, lit on the left
                k.px(col + 3, y, "RACK"); k.px(col + 4, y, "RACKD")
                if y % 4 == 2:
                    k.hline(col + 1, col + 6, y, "RACKD")
                    k.px(col + 1, y, "RACK")
            else:                                             # a copper coil: a spiral seen side on, turn by turn
                ph = y % 4
                if ph == 0:
                    k.hline(col + 1, col + 6, y, "COIL"); k.px(col + 1, y, "COILL")
                elif ph == 2:
                    k.hline(col + 2, col + 5, y, "BRICK")
                else:
                    k.px(col + 1, y, "COIL"); k.px(col + 6, y, "BRICK")
        if rack:
            k.px(col + 3, head, "QS"); k.px(col + 4, head, "QSD")    # a bead of quicksilver on each post's head
        else:
            k.hline(col + 2, col + 5, head, "COILL")

    #  one rafter fallen in from the left edge, burnt through, its end sagging onto the racks
    for i in range(0, 17):
        x, y = 35 + i, 5 + (i * 5) // 8
        k.px(x, y - 1, "RUST" if i % 4 else "COIL")           # its lit top, still glowing in places
        k.px(x, y, "BRICK")
        k.px(x, y + 1, "CHAR")

    # --- the gutter along the eave, quicksilver pooled in it, beaded where it spilled
    R(0, GUT0, W - 1, WALL0 - 1, "VOID")
    k.hline(1, W - 2, GUT0 + 1, "RACKD")
    k.hline(1, W - 2, GUT0 + 2, "SOOT")
    for c in (8, 40, 72, 104):                                 # four pools, each centred on a seam
        k.hline(c - 5, c + 4, GUT0 + 1, "QS")
        k.hline(c - 4, c + 3, GUT0 + 2, "QSD")
        k.px(c - 3, GUT0 + 1, "QSL"); k.px(c + 2, GUT0 + 1, "QSL")

    # --- the wall: ash where cream was, the courses still ruled
    R(0, WALL0, W - 1, WALL1, "VOID")
    R(1, WALL0, W - 2, WALL1 - 1, "ASH")
    for y in (WALL0, 37, 45):
        k.hline(1, W - 2, y, "ASHD")
    k.hline(1, W - 2, WALL0 + 1, "ASHL")
    #  BLOWN WINDOWS, two each side, and the soot licked UP the wall from each in tongues, darkest at the frame,
    #  the tallest in the middle reaching the eave (heat rises; the stain is the only record of it)
    for c in MANSION_WINDOWS:
        wy0, wy1 = 38, 52
        smoke(k, c, WALL0 + 1, wy0, 5)
        R(c - 5, wy0, c + 4, wy1, "SOOT")                     # the charred frame
        R(c - 4, wy0 + 1, c + 3, wy1 - 1, "VOID")             # empty
        k.hline(c - 4, c + 3, wy0 + 1, "CHAR")
        k.px(c - 4, wy1 - 2, "CHAR"); k.px(c + 3, wy1 - 2, "CHAR")      # glass teeth in the frame's foot
        k.px(c - 3, wy1 - 1, "CHAR"); k.px(c + 2, wy1 - 1, "CHAR")
        k.hline(c - 6, c + 5, wy1 + 1, "ASHD")                # the sill
        k.hline(c - 6, c + 5, wy1 + 2, "SOOT")
    #  quicksilver run off one sill, beaded down the wall (the only thing still moving)
    for y in (56, 58):
        k.px(99, y, "QS")
    k.px(99, 57, "QSD")
    #  the plinth
    R(1, 57, W - 2, WALL1 - 1, "ASHD")
    k.hline(1, W - 2, 57, "SOOT")
    k.hline(1, W - 2, 58, "ASH")
    #  the doorway: dark, its surround scorched, its lintel charred, the widest stain above it
    smoke(k, 56, WALL0 + 1, 41, 7)
    R(48, 41, 63, WALL1, "SOOT")
    R(50, 44, 61, WALL1, "VOID")
    k.hline(48, 63, 41, "CHAR")
    k.hline(49, 62, 42, "ASHD")
    k.hline(50, 61, 44, "CHAR")

    # --- the porch (row 4, cells 7..9): three steps of ash, and a pool of quicksilver at their foot
    py0 = 64
    for i, y in enumerate((py0, py0 + 3, py0 + 6)):
        R(48 - i * 2, y, 63 + i * 2, y + 2, "ASH")
        k.hline(48 - i * 2, 63 + i * 2, y, "ASHL")
        k.hline(48 - i * 2, 63 + i * 2, y + 2, "ASHD")
        k.px(48 - i * 2, y + 1, "VOID"); k.px(63 + i * 2, y + 1, "VOID")
    R(60, py0 + 9, 67, py0 + 10, "QS")
    k.px(61, py0 + 9, "QSL")
    k.hline(61, 66, py0 + 11, "QSD")
    return k


LANDMARKS_HERE = [(SCORN, draw_scorn), (MANSION, draw_mansion)]
TILESET = dict(dir="cinnabar_island", symbol="gTileset_CinnabarIsland", layout="CinnabarIsland_Layout")
#  this tool's claim; gbatowns.py's LANDMARKS keeps the same boxes out of its passes
OWNS = {"cinnabar_island": [("CinnabarIsland", 5, 0, 7, 5, "the MANSION"),
                            ("CinnabarIsland", 5, 6, 7, 4, "SCORN SOLUTIONS (the lab)")]}


# ============================================================================================ the tileset
def layouts():
    return json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]


class Tileset:
    def __init__(self, d, symbol):
        self.dir = os.path.join(GBA, "data/tilesets/secondary", d)
        self.symbol = symbol
        self.tiles = Image.open(os.path.join(self.dir, "tiles.png"))
        assert self.tiles.mode == "P", self.tiles.mode
        self.mt = bytearray(open(os.path.join(self.dir, "metatiles.bin"), "rb").read())
        self.at = bytearray(open(os.path.join(self.dir, "metatile_attributes.bin"), "rb").read())
        self.nblocks = len(self.mt) // 16
        self.per_attr = len(self.at) // self.nblocks
        self.pals = {n: read_pal(os.path.join(self.dir, "palettes/%02d.pal" % n)) for n in range(7, 13)}
        rules = open(RULES).read()
        m = re.search(r"secondary/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles (\d+)" % d, rules)
        self.num_tiles = int(m.group(1))
        self.layouts = [l for l in layouts() if l.get("secondary_tileset") == symbol]
        self.maps = {}
        for l in self.layouts:
            bd = bytearray(open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read())
            border = open(os.path.join(GBA, l["border_filepath"]), "rb").read()
            self.maps[l["name"]] = dict(w=l["width"], h=l["height"], bd=bd, path=l["blockdata_filepath"],
                                        border=[struct.unpack_from("<H", border, i * 2)[0] & 0x3FF
                                                for i in range(len(border) // 2)])
        self.grow_pixels()

    def grow_pixels(self):
        tp = self.tiles.load()
        self.px = []
        for t in range(SECONDARY_TILES):
            sx, sy = (t % 16) * 8, (t // 16) * 8
            if sy >= self.tiles.height:
                self.px.append(tuple([0] * 64))
            else:
                self.px.append(tuple(tp[sx + i % 8, sy + i // 8] for i in range(64)))

    def entries(self, b):
        return list(struct.unpack_from("<8H", self.mt, (b - NUM_PRIMARY) * 16))

    def attr(self, b):
        return bytes(self.at[(b - NUM_PRIMARY) * self.per_attr:(b - NUM_PRIMARY + 1) * self.per_attr])

    def cell(self, mapname, x, y):
        m = self.maps[mapname]
        return struct.unpack_from("<H", m["bd"], (y * m["w"] + x) * 2)[0]

    def set_cell(self, mapname, x, y, raw):
        m = self.maps[mapname]
        struct.pack_into("<H", m["bd"], (y * m["w"] + x) * 2, raw)


def footprint_cells(lm):
    cells = lm.get("cells_only") or {(x, y) for x in range(lm["x0"], lm["x0"] + lm["w"])
                                     for y in range(lm["y0"], lm["y0"] + lm["h"])}
    return sorted(cells, key=lambda p: (p[1], p[0]))


def census(ts, ours):
    """{secondary tile: True} for every tile the landmarks may repaint: drawn ONLY by our cells (every layout, every
    border), not one of the kept cells' tiles, and below DOOR_TILE_START; plus the slots nothing draws.
    Returns (owned slots, free slots, what was examined)."""
    users = {}                                   # tile -> set of (layout, x, y) / ("border", layout)
    examined = 0
    for name, m in ts.maps.items():
        for y in range(m["h"]):
            for x in range(m["w"]):
                b = ts.cell(name, x, y) & 0x3FF
                examined += 1
                if b >= NUM_PRIMARY and b - NUM_PRIMARY < ts.nblocks:
                    for e in ts.entries(b):
                        t = e & 0x3FF
                        if t >= NUM_PRIMARY:
                            users.setdefault(t - NUM_PRIMARY, set()).add((name, x, y))
        for b in m["border"]:
            if b >= NUM_PRIMARY:
                for e in ts.entries(b):
                    if (e & 0x3FF) >= NUM_PRIMARY:
                        users.setdefault((e & 0x3FF) - NUM_PRIMARY, set()).add(("border", name))
    ours_set = {(TILESET["layout"], x, y) for x, y in ours}
    #  tiles any metatile references at all (placed or not): an unplaced block's tile is free to repaint, but a slot
    #  past num_tiles that a block references must not exist -- checked, never assumed
    referenced = set()
    for b in range(ts.nblocks):
        for e in ts.entries(NUM_PRIMARY + b):
            if (e & 0x3FF) >= NUM_PRIMARY:
                referenced.add((e & 0x3FF) - NUM_PRIMARY)
    owned = sorted(t for t, u in users.items() if u <= ours_set and t < DOOR_TILE_START)
    free = [t for t in range(ts.num_tiles, DOOR_TILE_START) if t not in users]
    return owned, free, users, examined, referenced


# ============================================================================================ cutting and placing
def flips(key):
    rows = [key[i * 8:(i + 1) * 8] for i in range(8)]
    h = tuple(v for r in rows for v in r[::-1])
    v = tuple(v for r in rows[::-1] for v in r)
    hv = tuple(v for r in rows[::-1] for v in r[::-1])
    return {0: key, 1: h, 2: v, 3: hv}


class Cutter:
    """8x8 tiles out of the drawings, de-duplicated with flips, into the slots given, in order."""
    def __init__(self, slots):
        self.slots = list(slots)
        self.known = {}                          # pixels -> entry bits (slot | flips), for every flip of a placed tile
        self.placed = []                         # (slot, pixels)
        self.over = 0

    def tile(self, key, row):
        if not any(key):
            return 0
        if key in self.known:
            return self.known[key] | (row << 12)
        if len(self.placed) >= len(self.slots):
            self.over += 1                       # past the budget: a preview-only slot, never written
            slot = 400 + self.over
        else:
            slot = self.slots[len(self.placed)]
        self.placed.append((slot, key))
        for f, k in flips(key).items():
            self.known.setdefault(k, (NUM_PRIMARY + slot) | (f << 10))
        return self.known[key] | (row << 12)


def build(ts):
    """Draw every landmark here into a copy of the tileset. Returns the new state and a report."""
    drawings, cells = {}, []
    for lm, fn in LANDMARKS_HERE:
        drawings[lm["name"]] = fn()
        cells += [c for c in footprint_cells(lm) if c not in lm["keep"]]
    owned, free, users, examined, referenced = census(ts, cells)
    #  tiles the kept cells draw are never ours, whatever the census says (the lab's door, the board)
    kept_tiles = set()
    for lm, _ in LANDMARKS_HERE:
        for (x, y) in lm["keep"]:
            kept_tiles |= {(e & 0x3FF) - NUM_PRIMARY for e in ts.entries(ts.cell(TILESET["layout"], x, y) & 0x3FF)
                           if (e & 0x3FF) >= NUM_PRIMARY}
        for (x, y) in lm["signs"]:
            e = ts.entries(ts.cell(TILESET["layout"], x, y) & 0x3FF)
            kept_tiles |= {(v & 0x3FF) - NUM_PRIMARY for v in e[6:8]}
    owned = [t for t in owned if t not in kept_tiles]
    slots = owned + free
    cut = Cutter(slots)

    new_mt, new_at = bytearray(ts.mt), bytearray(ts.at)
    nblocks = ts.nblocks
    #  blocks this tool appended on an earlier write are reused in place (a re-run rewrites them, never appends more)
    first_ours = vanilla_block_count(ts)
    plan, per = [], {}
    for lm, _ in LANDMARKS_HERE:
        n0 = len(cut.placed)
        k = drawings[lm["name"]]
        row = lm["row"]
        for (x, y) in footprint_cells(lm):
            if (x, y) in lm["keep"]:
                continue
            raw = ts.cell(TILESET["layout"], x, y)
            old = raw & 0x3FF
            ox, oy = (x - lm["x0"]) * 16, (y - lm["y0"]) * 16
            art = [cut.tile(tuple(k.get(ox + qx * 8 + i % 8, oy + qy * 8 + i // 8) for i in range(64)), row)
                   for qy in (0, 1) for qx in (0, 1)]
            if old >= NUM_PRIMARY:
                e = ts.entries(old)
                attr = ts.attr(old)
            else:                                   # a primary ground cell (the porch's): ground below, art above
                e = list(struct.unpack_from("<8H", open(os.path.join(PRIMARY, "metatiles.bin"), "rb").read(), old * 16))
                attr = None
            bottom = e[:4]
            if (x, y) in lm["signs"]:               # the board's own tiles stay on top; the wall is ours, below
                entries = art + [0, 0, e[6], e[7]]
            elif (x, y) == lm["door"]:              # the mansion's doorway: all of it below, the lintel above
                lint = [cut.tile(tuple(k.get(ox + qx * 8 + i % 8, oy + qy * 8 + i // 8)
                                       if lintel(k, ox + qx * 8 + i % 8, oy + qy * 8 + i // 8) else 0
                                       for i in range(64)), row) for qy in (0, 1) for qx in (0, 1)]
                entries = art + lint
            else:
                if not any(v & 0x3FF for v in bottom):
                    bottom = ground_under(ts, lm, x, y)
                entries = bottom + art
            plan.append((x, y, raw, old, entries, attr))
        per[lm["name"]] = len(cut.placed) - n0
    #  place: a fresh block per cell, appended (or this tool's own block from an earlier write, rewritten)
    for x, y, raw, old, entries, attr in plan:
        if old >= NUM_PRIMARY + first_ours:
            bid = old
            struct.pack_into("<8H", new_mt, (bid - NUM_PRIMARY) * 16, *entries)
        else:
            bid = NUM_PRIMARY + nblocks
            nblocks += 1
            new_mt += struct.pack("<8H", *entries)
            new_at += attr if attr is not None else bytes(ts.per_attr)
        ts.set_cell(TILESET["layout"], x, y, (raw & ~0x3FF) | bid)
    assert nblocks <= SECONDARY_METATILES, "the tileset holds %d blocks" % SECONDARY_METATILES
    #  the tiles image, grown to hold every slot used
    used_top = max([s for s, _ in cut.placed] + [ts.num_tiles - 1]) + 1
    img = Image.new("P", (128, max(ts.tiles.height, ((used_top + 15) // 16) * 8)))
    img.putpalette(ts.tiles.getpalette())
    img.paste(ts.tiles, (0, 0))
    ip = img.load()
    for slot, key in cut.placed:
        sx, sy = (slot % 16) * 8, (slot // 16) * 8
        for i, v in enumerate(key):
            ip[sx + i % 8, sy + i // 8] = v
    pals = dict(ts.pals)
    for lm, _ in LANDMARKS_HERE:
        pals[lm["row"]] = pal16(lm["colours"])
    return dict(drawings=drawings, mt=new_mt, at=new_at, tiles=img, pals=pals, num_tiles=max(used_top, ts.num_tiles),
                cut=cut, owned=owned, free=free, examined=examined, nblocks=nblocks, old_nblocks=ts.nblocks,
                kept_tiles=kept_tiles, users=users, plan=plan, per=per)


def lintel(k, x, y):
    """the mansion door cell's top layer: everything that is not the dark opening (the player passes under it)"""
    return not k.is_(x, y, "VOID") or y < 48


def ground_under(ts, lm, x, y):
    """a cell vanilla left with no bottom layer: borrow the nearest footprint cell's ground in the same row"""
    for dx in range(1, 8):
        for xx in (x - dx, x + dx):
            if lm["x0"] <= xx < lm["x0"] + lm["w"]:
                b = ts.cell(TILESET["layout"], xx, y) & 0x3FF
                e = ts.entries(b) if b >= NUM_PRIMARY else [0] * 8
                if any(v & 0x3FF for v in e[:4]):
                    return e[:4]
    return [0, 0, 0, 0]


def vanilla_block_count(ts):
    """how many blocks the tileset had before this tool: vanilla's, plus every other tool's (T-86's board is 130..133)"""
    van = daemonslib.upstream(GBA, "data/tilesets/secondary/%s/metatiles.bin" % TILESET["dir"], binary=True)
    n = len(van) // 16
    #  every block after vanilla's that a landmark cell points at is ours; others' appended blocks come first
    ours = [ts.cell(TILESET["layout"], x, y) & 0x3FF for lm, _ in LANDMARKS_HERE for (x, y) in footprint_cells(lm)
            if (x, y) not in lm["keep"] and (x, y) not in lm["signs"]]
    ours = [b - NUM_PRIMARY for b in ours if b >= NUM_PRIMARY + n]
    return min(ours) if ours else ts.nblocks


# ============================================================================================ rendering
_prim = {}


def primary():
    if not _prim:
        _prim["tiles"] = Image.open(os.path.join(PRIMARY, "tiles.png")).load()
        _prim["mt"] = open(os.path.join(PRIMARY, "metatiles.bin"), "rb").read()
        _prim["pals"] = {n: read_pal(os.path.join(PRIMARY, "palettes/%02d.pal" % n)) for n in range(7)}
    return _prim


def render(ts, mt, tiles_img, pals, mapname, x0, y0, w, h):
    """the map as the GBA draws it, cells x0..x0+w-1, y0..y0+h-1 (bottom layer, then top; 0 is see-through)"""
    P = primary()
    sp = tiles_img.load()
    allp = dict(P["pals"]); allp.update(pals)
    m = ts.maps[mapname]
    out = Image.new("RGB", (w * 16, h * 16), tuple(P["pals"][0][0]))
    op = out.load()
    for cy in range(h):
        for cx in range(w):
            mx, my = x0 + cx, y0 + cy
            if not (0 <= mx < m["w"] and 0 <= my < m["h"]):
                continue
            b = struct.unpack_from("<H", m["bd"], (my * m["w"] + mx) * 2)[0] & 0x3FF
            e = struct.unpack_from("<8H", P["mt"], b * 16) if b < NUM_PRIMARY else \
                struct.unpack_from("<8H", mt, (b - NUM_PRIMARY) * 16)
            for layer in (0, 1):
                for q in range(4):
                    t = e[layer * 4 + q]
                    idx, pal, hf, vf = t & 0x3FF, (t >> 12) & 0xF, (t >> 10) & 1, (t >> 11) & 1
                    src, i = (P["tiles"], idx) if idx < NUM_PRIMARY else (sp, idx - NUM_PRIMARY)
                    hgt = 640 // 16 * 8 if idx < NUM_PRIMARY else tiles_img.height
                    for ty in range(8):
                        for tx in range(8):
                            sx = (i % 16) * 8 + (7 - tx if hf else tx)
                            sy = (i // 16) * 8 + (7 - ty if vf else ty)
                            if sy >= hgt:
                                continue
                            try:
                                v = src[sx, sy]
                            except IndexError:
                                continue
                            if v == 0:
                                continue
                            op[cx * 16 + (q % 2) * 8 + tx, cy * 16 + (q // 2) * 8 + ty] = tuple(allp.get(pal, allp[0])[v])
    return out


def drawing_rgb(k, colours, keep_mask=None):
    pal = pal16(colours)
    im = Image.new("RGBA", (k.w, k.h), (0, 0, 0, 0))
    p = im.load()
    for y in range(k.h):
        for x in range(k.w):
            if k.c[y][x]:
                p[x, y] = pal[k.c[y][x]] + (255,)
    return im


# ============================================================================================ sheets
def font(n):
    for f in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, n)
    return ImageFont.load_default()


BG, FG, DIM, GOLD = (30, 30, 36), (232, 232, 236), (150, 150, 160), (232, 196, 96)


def up(im, n):
    return im.resize((im.width * n, im.height * n), Image.NEAREST)


def sheets(ts, before, after, out):
    os.makedirs(out, exist_ok=True)
    F, Fs, Fb = font(14), font(12), font(22)
    paths = []
    for lm, _ in LANDMARKS_HERE:
        x0, y0 = lm["x0"] - 1, max(0, lm["y0"] - 1)
        w, h = lm["w"] + 2, lm["h"] + 2 - (1 if lm["y0"] == 0 else 0)
        today = render(ts, before["mt"], before["tiles"], before["pals"], TILESET["layout"], x0, y0, w, h)
        draft = render(ts, after["mt"], after["tiles"], after["pals"], TILESET["layout"], x0, y0, w, h)
        isle_t = render(ts, before["mt"], before["tiles"], before["pals"], TILESET["layout"], 0, 0, 24, 20)
        isle_d = render(ts, after["mt"], after["tiles"], after["pals"], TILESET["layout"], 0, 0, 24, 20)
        W = 40 + today.width * 3 * 2 + 40 + 40
        Hh = 110 + today.height * 3 + today.height + 30 + 344
        s = Image.new("RGB", (max(W, 24 + 384 * 2 + 16 + 24), Hh), BG)
        d = ImageDraw.Draw(s)
        d.text((24, 16), "%s  --  T-447 DRAFT (gbalandmarks.py)" % lm["title"], fill=FG, font=Fb)
        d.text((24, 48), "QUICKSILVER IS. / CinnabarIsland  |  footprint %dx%d at (%d,%d)  |  door (%d,%d)  |  row %d"
               % (lm["w"], lm["h"], lm["x0"], lm["y0"], lm["door"][0], lm["door"][1], lm["row"]), fill=DIM, font=F)
        s.paste(up(today, 3), (24, 80))
        s.paste(up(draft, 3), (24 + today.width * 3 + 24, 80))
        d.text((24, 84 + today.height * 3), "TODAY (3x)", fill=DIM, font=F)
        d.text((48 + today.width * 3, 84 + today.height * 3), "DRAFT (3x)", fill=GOLD, font=F)
        yy = 110 + today.height * 3
        s.paste(today, (24, yy)); s.paste(draft, (24 + today.width + 12, yy))
        d.text((24, yy + today.height + 4), "today | draft at 1x", fill=DIM, font=Fs)
        yy2 = yy + today.height + 30
        s.paste(isle_t, (24, yy2)); s.paste(isle_d, (24 + 384 + 16, yy2))
        d.text((24, yy2 + 322), "QUICKSILVER IS. at 1x: today", fill=DIM, font=Fs)
        d.text((24 + 400, yy2 + 322), "draft", fill=GOLD, font=Fs)
        p = os.path.join(out, "t447a_%s.png" % lm["name"])
        s.save(p)
        paths.append(p)
    # the tiles sheet: every slot the landmarks drew, 4x, numbered, in its own row's colours
    cut = after["cut"]
    n = len(cut.placed)
    cols = 16
    s = Image.new("RGB", (40 + cols * 40, 90 + ((n + cols - 1) // cols) * 48 + 40), BG)
    d = ImageDraw.Draw(s)
    d.text((24, 16), "T-447 tiles: %d drawn into %d owned + %d free slots (of %d)" %
           (n, len(after["owned"]), len(after["free"]), len(after["owned"]) + len(after["free"])), fill=FG, font=F)
    d.text((24, 40), "flipped repeats share a slot; 376..383 never used (door frames)", fill=DIM, font=Fs)
    rowof = {}
    for _, _, _, _, entries, _ in after["plan"]:
        for v in entries:
            if v & 0x3FF >= NUM_PRIMARY:
                rowof.setdefault((v & 0x3FF) - NUM_PRIMARY, (v >> 12) & 0xF)
    for i, (slot, key) in enumerate(cut.placed):
        pal = after["pals"].get(rowof.get(slot, 10), after["pals"][10])
        t = Image.new("RGB", (8, 8))
        for j, v in enumerate(key):
            t.putpixel((j % 8, j // 8), tuple(pal[v]) if v else (60, 60, 70))
        x, y = 24 + (i % cols) * 40, 70 + (i // cols) * 48
        s.paste(up(t, 4), (x, y))
        d.text((x, y + 33), str(slot), fill=DIM, font=font(10))
    p = os.path.join(out, "t447a_tiles.png"); s.save(p); paths.append(p)
    # the palette rows
    rows = [(SCORN_ROW, SCORN_COLOURS, "SCORN SOLUTIONS"), (MANSION_ROW, MANSION_COLOURS, "the MANSION")]
    s = Image.new("RGB", (40 + 16 * 64, 60 + len(rows) * 110), BG)
    d = ImageDraw.Draw(s)
    d.text((24, 16), "T-447 palette rows (secondary/cinnabar_island, rows 10 and 11 were unused)", fill=FG, font=F)
    for r, (n_, cols_, title) in enumerate(rows):
        y = 50 + r * 110
        d.text((24, y), "row %d -- %s" % (n_, title), fill=GOLD, font=F)
        for i, (name, rgb) in enumerate([("0", TRANSPARENT)] + cols_):
            d.rectangle((24 + i * 64, y + 22, 24 + i * 64 + 58, y + 70), fill=rgb)
            d.text((24 + i * 64, y + 74), name, fill=DIM, font=font(10))
    p = os.path.join(out, "t447a_palettes.png"); s.save(p); paths.append(p)
    return paths


# ============================================================================================ main
def gbatowns_landmarks():
    src = open(os.path.join(ROOT, "tools", "gbatowns.py")).read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LANDMARKS" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def main():
    if WRITE and not APPROVED_FLAG:
        raise SystemExit("  --write refuses without --approved: T-447's landmarks are drafts until the user says yes")
    gt = gbatowns_landmarks().get(TILESET["dir"], [])
    if sorted(gt) != sorted(OWNS[TILESET["dir"]]):
        raise SystemExit("  gbatowns.py's LANDMARKS and OWNS disagree for %s:\n    %s\n    %s" % (TILESET["dir"], gt, OWNS))
    ts = Tileset(TILESET["dir"], TILESET["symbol"])
    before = dict(mt=bytes(ts.mt), tiles=ts.tiles.copy(), pals=dict(ts.pals))
    before_bd = {k: bytes(v["bd"]) for k, v in ts.maps.items()}
    print("  %s: %d layouts draw it (%s); %d blocks, %d tiles (-num_tiles)" % (
        TILESET["symbol"], len(ts.layouts), ", ".join(l["name"].replace("_Layout", "") for l in ts.layouts),
        ts.nblocks, ts.num_tiles))
    for n in (SCORN_ROW, MANSION_ROW):
        if any(c != (0, 0, 0) for c in ts.pals[n][1:]) and not all(
                c == rgb for c, (_, rgb) in zip(ts.pals[n][1:], SCORN_COLOURS if n == SCORN_ROW else MANSION_COLOURS)):
            raise SystemExit("  row %d is not free and not ours: %s" % (n, ts.pals[n]))
    after = build(ts)
    cut = after["cut"]
    print("  census: %d cells examined across every layout and border" % after["examined"])
    print("  owned tiles (drawn only by our cells): %d; free slots %d..%d: %d; kept (the lab's door, the board): %d"
          % (len(after["owned"]), ts.num_tiles, DOOR_TILE_START - 1, len(after["free"]), len(after["kept_tiles"])))
    for lm, _ in LANDMARKS_HERE:
        cells = [c for c in footprint_cells(lm) if c not in lm["keep"]]
        print("  %-16s %d cells redrawn, %d kept %s; row %d; %d new tiles" % (
            lm["title"], len(cells), len(lm["keep"]), lm["keep"], lm["row"], after["per"][lm["name"]]))
    print("  drawn: %d unique tiles (flips shared) into %d slots; %s" % (
        len(cut.placed), len(after["owned"]) + len(after["free"]),
        "OVER BUDGET by %d" % cut.over if cut.over else "%d to spare" % (len(after["owned"]) + len(after["free"]) - len(cut.placed))))
    print("  blocks: %d -> %d (of %d); -num_tiles %d -> %d" % (after["old_nblocks"], after["nblocks"],
                                                             SECONDARY_METATILES, ts.num_tiles, after["num_tiles"]))
    if cut.over:
        print("  !! the drawings need %d more tiles than the landmarks own: previewed, never written" % cut.over)
        if WRITE:
            raise SystemExit("  not written")
    after_view = dict(mt=after["mt"], tiles=after["tiles"], pals=after["pals"], cut=cut, owned=after["owned"],
                      free=after["free"], plan=after["plan"])
    if DRAFT is not None:
        tsd = os.path.join(DRAFT, TILESET["dir"])
        os.makedirs(os.path.join(tsd, "palettes"), exist_ok=True)
        after["tiles"].save(os.path.join(tsd, "tiles.png"))
        open(os.path.join(tsd, "metatiles.bin"), "wb").write(after["mt"])
        open(os.path.join(tsd, "metatile_attributes.bin"), "wb").write(after["at"])
        open(os.path.join(tsd, "map.bin"), "wb").write(ts.maps[TILESET["layout"]]["bd"])
        for lm, _ in LANDMARKS_HERE:
            write_pal(os.path.join(tsd, "palettes", "%02d.pal" % lm["row"]), pal16(lm["colours"]))
            d = os.path.join(DRAFT, lm["name"])
            os.makedirs(d, exist_ok=True)
            k = after["drawings"][lm["name"]]
            im = drawing_rgb(k, lm["colours"])
            im.save(os.path.join(d, "drawing_1x.png"))
            up(im, 3).save(os.path.join(d, "drawing_3x.png"))
            json.dump(dict(title=lm["title"], map=lm["map"], footprint=[lm["x0"], lm["y0"], lm["w"], lm["h"]],
                           door=lm["door"], kept=lm["keep"], signs=lm["signs"], row=lm["row"],
                           colours={n: "%02x%02x%02x" % c for n, c in lm["colours"]},
                           cells=[dict(cell=[x, y], was=old, layer_type=(struct.unpack("<I", attr)[0] >> 29) & 3
                                       if attr else None)
                                  for x, y, raw, old, _, attr in after["plan"]
                                  if (x, y) in set(footprint_cells(lm))]),
                      open(os.path.join(d, "cells.json"), "w"), indent=1)
        json.dump(dict(tileset=TILESET["symbol"], tiles_drawn=len(cut.placed), owned=after["owned"], free=after["free"],
                       slots_used=[s for s, _ in cut.placed], blocks=[after["old_nblocks"], after["nblocks"]],
                       num_tiles=[ts.num_tiles, after["num_tiles"]]), open(os.path.join(tsd, "budget.json"), "w"), indent=1)
        print("  draft: %s (tileset) and %s" % (os.path.relpath(tsd, ROOT),
                                               ", ".join(os.path.relpath(os.path.join(DRAFT, lm["name"]), ROOT)
                                                         for lm, _ in LANDMARKS_HERE)))
        if SHEETS:
            #  today is rendered from the untouched map, the draft from the repointed one
            before_maps = {k: dict(v, bd=bytearray(before_bd[k])) for k, v in ts.maps.items()}
            paths = sheets_two(ts, before_maps, before, after_view, SHEETS)
            for p in paths:
                print("  sheet: %s" % p)
    if WRITE:
        todo = [lm for lm, _ in LANDMARKS_HERE if lm["name"] in APPROVED]
        if len(todo) != len(LANDMARKS_HERE):
            raise SystemExit("  not written: approved %s of %s -- the pair is written together, as one tileset"
                             % (sorted(APPROVED), [lm["name"] for lm, _ in LANDMARKS_HERE]))
        tsd = ts.dir
        after["tiles"].save(os.path.join(tsd, "tiles.png"))
        open(os.path.join(tsd, "metatiles.bin"), "wb").write(after["mt"])
        open(os.path.join(tsd, "metatile_attributes.bin"), "wb").write(after["at"])
        m = ts.maps[TILESET["layout"]]
        open(os.path.join(GBA, m["path"]), "wb").write(m["bd"])
        for lm, _ in LANDMARKS_HERE:
            write_pal(os.path.join(tsd, "palettes", "%02d.pal" % lm["row"]), pal16(lm["colours"]))
        rules = open(RULES).read()
        new, n = re.subn(r"(secondary/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+" % TILESET["dir"],
                         lambda mm: mm.group(1) + str(after["num_tiles"]), rules)
        assert n == 1
        open(RULES, "w").write(new)
        print("  written: tiles.png, metatiles.bin, metatile_attributes.bin, palettes 10 and 11, the map, -num_tiles %d"
              % after["num_tiles"])


def sheets_two(ts, before_maps, before, after, out):
    """sheets() with the map's two states: TODAY drawn from the untouched cells, the draft from the repointed ones"""
    class State:
        def __init__(self, maps):
            self.maps = maps
    today, draft = State(before_maps), State(ts.maps)
    global render
    base = render

    def render2(_, mt, tiles_img, pals, mapname, x0, y0, w, h):
        return base(today if mt is before["mt"] else draft, mt, tiles_img, pals, mapname, x0, y0, w, h)
    render = render2
    try:
        return sheets(ts, before, after, out)
    finally:
        render = base


if __name__ == "__main__":
    main()
