#!/usr/bin/env python3
"""The landmarks, drawn from the story into their own footprints (T-447, docs/private/plan-landmarks-2026-10-24.md).

    python3 tools/gbalandmarks.py                       # report: each landmark's footprint, the tiles it owns, the
                                                        #   budget its drawing uses; nothing written
    python3 tools/gbalandmarks.py --draft [DIR]         # the drafts: per landmark gfx/drafts/landmarks/<name>/ (the
                                                        #   drawing at 1x and 3x, its cells), per tileset
                                                        #   gfx/drafts/landmarks/<tileset>/ (tiles.png, metatiles.bin,
                                                        #   metatile_attributes.bin, the map's map.bin, the new .pal rows)
    python3 tools/gbalandmarks.py --draft --sheets DIR  # and the review sheets in DIR (t447b_*.png)
    python3 tools/gbalandmarks.py --only saffron_city ...  # one tileset's group only
    python3 tools/gbalandmarks.py --write --approved    # into the engine -- REFUSES without --approved, and writes only
                                                        #   the landmarks in APPROVED (the first pair, approved 2026-10-24)

THE FIRST PAIR (the user, 2026-10-24) -- QUICKSILVER IS., one tileset (secondary/cinnabar_island), one campus:

  SCORN SOLUTIONS (CinnabarIsland, 7x4 at (5,6), door (8,9)). CRYSTAL CLEAR's lab's sister, drawn in gbalab.py's hand
  -- pale stone in courses, a flat slate roof inside a parapet, tall two-pane windows on sills, a plinth -- and then
  PROCESSED, as 4.24 has the campus's intact half processed into a company that sells what it studied:
    * gold leaf laid over the parapet's front, one corner (lower right) lifting onto the paler board beneath;
    * every window half drawn with the SAME blind, to the same slat;
    * the slate ruled like a form into six big boxes, and the first one ticked (second draft: fewer, bigger boxes, so
      the tick reads at 1x);
    * a small intake slot in the wall by the door;
    * her glazed door replaced by a plain steel one, the procedure's red light over it (second draft);
    * the board SCORN SOLUTIONS over CLEAR LABORATORY kept exactly as gbaislandsigns.py drew it (T-86's gold leaf);
    * the only red is the new owner's procedure: the tick, the slot's lip, the light. (4.4: give him the red, never
      say it.)
  THE DOOR. field_door.c finds a door's frames by block id alone, so the door cell keeps its block,
  METATILE_CinnabarIsland_LabDoor (0x2AD), and only that block's four top-layer tiles are redrawn, in place, in row
  10. Its frames are not this tool's: gbadoors.py's DOORS["cinnabar_lab"] carries a "redrawn" spec (a hinged steel
  leaf, the room kept clear of the red) that it takes up only once the closed door draws in row 10 -- so after this
  tool's --write, `gbadoors.py --write --approved` redraws graphics/door_anims/cinnabar_lab.png from the new door and
  sets sDoorAnimPalettes_CinnabarLab 3 -> 10 (its plan() proposes the row). The old frames cannot stay: they repaint
  the whole cell with a glass door sliding, so the steel door would turn to glass for a quarter second.

  the MANSION (CinnabarIsland, 7x4 at (5,0), door (8,3), and the porch below it). The campus's burned half, redrawn
  in its footprint, no vanilla left: the roof caved in where the work was, the racks and cooling coils standing in
  the gap curved like a rib cage on a copper spine, ONE soot stain rising from the doorway up the facade into the
  cave-in (second draft: in place of a stain over each window), the colour gone to ash, quicksilver beaded and
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

THE SECOND PAIR (drafted 2026-10-24, NOT approved; GROUPS below, one per tileset). The first draft was flat slabs;
the user (2026-10-24): redraw both with 3/4 overworld depth. Both are now chamfered boxes seen from the south and
above (box_mask, lean): the front square on, the left chamfer lit and the right shaded, every roof a deck seen from
above with a stepped outline, and the silhouette INSET so the ground shows at the sides, as vanilla's did.

  CORPUS's tower (BRAZEN, SaffronCity 9x15 at (29,16), and its copy on SaffronCity_Connection at (19,9)). Riveted
  brass a step deeper than BRAZEN's houses, outlined near-black; one grid of identical windows, small and amber, carried
  round onto both chamfers; a stepped crown (the shaft's deck and two tiers, each casting its shadow) with one thin
  red band round the top tier; a full-width glass lobby through which the dark plate in the floor is seen -- with no
  words on it, ever. Its cells had no bottom layer (vanilla drew the paving into the tower's own tiles), so they take
  BRAZEN's paving block as their bottom layer and the inset costs no tile. THE DOOR (33,30) is redrawn IN PLACE,
  block 0x2BC kept by id, its pixels in row 9 on the bottom layer, so the plate continues through its glass; its
  frames are gbadoors.py's: the build adds CORPUS_DOOR as DOORS["silph_co"]["redrawn"], whose --write then redraws
  graphics/door_anims/silph_co.png and sets sDoorAnimPalettes_SilphCo 3 -> 9 (corpus_door_preview() shows them).
  Row 9 is drawn by the tower alone, so the tower takes all of it. BRAZEN has no free tile: the tower owns 55 (its
  53 and the old door's two) and draws 55.

  DAEMON TOWER (HALFTONE, LavenderTown 7x7 at (15,0) + ROUTE 10's rows 72..79, its top). A chamfered drum in black
  halftone dots on white, the DOT SIZE the shading: specks on the lit chamfer, heavy dots on the shaded one, sparse at
  the top and dense at the foot. Vanilla's dome kept as a silhouette on a rounder octagonal deck, drawn in the dot
  screen, a mast with one light over it. Seven bands of arched niches cut straight into the dots, no shelves, a small
  amber light in each. The doorway (18,6) is drawn as the MANSION's. Its cells keep their own bottom layer (the cliff
  and grass), which shows through the inset. Row 7 (unused) indices 1..9; 10..15 and the free slots past -num_tiles
  are left for the KEEPALIVE PLANT.

  Both pair-2 groups REUSE blocks: identical cells share a block, written first over the blocks only the landmark drew
  (never one metatile_labels.h names), so a big footprint does not eat the tileset's 384.

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
APPROVED = {"scorn_solutions", "mansion"}           # the user, 2026-10-24: "build it" (second draft, e559d4eb)

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
             door=(8, 9), keep=[], inplace=[(8, 9)], signs=[(9, 9), (10, 9)], row=SCORN_ROW, colours=SCORN_COLOURS)
#  The door cell is redrawn IN PLACE: its block keeps its id (0x2AD, METATILE_CinnabarIsland_LabDoor), because
#  field_door.c finds a door's frames by block id alone; only its four top-layer tiles change (bottom stays empty, as
#  vanilla's is, and the frames draw there). The leaf, in the cell's own pixels, is gbadoors.py's DOORS entry for
#  cinnabar_lab ("redrawn"), which it takes up only once the closed door draws in this row.
SCORN_DOOR = dict(block=0x2AD, kind="hinged", hinge="R", leaf=(2, 1, 13, 14))
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
    #  THE FORM: the slate ruled into a few big boxes -- six of them, two tiles square, a printed question (a dash) in
    #  each box's corner and the answer space empty. The user (2026-10-24): fewer, bigger boxes, so the one tick reads
    #  at 1x. Every box is the same four tiles; the ticked one is the only four of its own.
    top, bot = 10, 26
    for x in range(8, W - 7, 16):
        k.vline(x, top, bot, "SLATEL")
    for y in (top, bot):
        k.hline(8, W - 8, y, "SLATEL")
    for bx in range(8, W - 8, 16):
        k.hline(bx + 2, bx + 5, top + 2, "OUT")
    #  ONE box ticked, in the procedure's red: the first (a form is filled in order), the rest waiting. Two pixels
    #  thick and ten wide, so it is the brightest thing on the roof at real size.
    tx, ty = 8, top
    for (dx, dy) in ((3, 8), (4, 9), (5, 10), (6, 11), (7, 10), (8, 9), (9, 8), (10, 7), (11, 6), (12, 5), (13, 4)):
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

    #  the plate over the door -- blank on hers, here leafed over like the parapet
    R(50, WALL0 + 1, 61, WALL0 + 4, "GOLDD")
    k.hline(51, 60, WALL0 + 2, "LEAF")
    k.hline(51, 60, WALL0 + 3, "GOLD")
    #  THE DOOR (the user, 2026-10-24): her glazed entry gone for a plain steel door, and over it the procedure's red
    #  light. The light is in the cell above, so it never moves when the door opens; the door is the door cell's
    #  block (METATILE_CinnabarIsland_LabDoor, kept by id, redrawn in place) and opens on gbadoors.py's hinge.
    R(54, 41, 57, 44, "OUT")                                  # the lamp's housing
    R(55, 42, 56, 43, "RED")                                  # the light
    R(48, 47, 63, 47, "LINE")                                 # the lintel's shade
    R(49, 48, 62, 62, "SLATE")                                # the frame
    R(50, 49, 61, 62, "PLINTH")                               # the leaf: steel, plain -- DOOR_LEAF in cell pixels
    k.vline(50, 49, 62, "LINE")                               # its lit edge
    k.hline(50, 61, 49, "LINE")
    k.vline(61, 50, 62, "SLATEL")                             # its shaded edge
    k.hline(51, 60, 59, "SLATEL")                             # the kick plate
    k.px(52, 54, "OUT"); k.px(52, 55, "OUT"); k.px(53, 54, "LINE")      # the handle, opposite the hinge
    #  THE INTAKE SLOT, by the door on its left: a narrow mouth in a steel plate, its lip the procedure's red
    sx0, sy0 = 39, 49
    R(sx0, sy0, sx0 + 5, sy0 + 7, "PLINTH")
    k.hline(sx0, sx0 + 5, sy0, "LINE")
    R(sx0 + 1, sy0 + 3, sx0 + 4, sy0 + 4, "OUT")             # the mouth
    k.hline(sx0 + 1, sx0 + 4, sy0 + 5, "RED")                # its lip
    k.vline(sx0 + 5, sy0 + 1, sy0 + 7, "SLATEL")
    return k


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


RIBS = ((0, 11), (4, 15), (8, 18), (12, 17))      # (root row on the spine, half-span) -- longest in the middle
RIB_DROP = 7                                        # how far each rib falls from root to tip
RIB_EXP = 3                                         # how late it falls: higher keeps it level longer, then turns it down


def stain(k, top, bottom):
    """the one soot stain: from under the cave-in (wide, y = top) down the facade to the doorway (narrow, y = bottom),
    its edge licking in and out, darkest along its middle, ordered-dithered into the ash. Symmetric about x 56 -- the
    dither too -- so its right half costs no tiles of its own."""
    import math
    for y in range(top, bottom + 1):
        t = (y - top) / max(1, bottom - top)                  # 0 under the hole, 1 at the doorway's foot
        w = STAIN_TOP - (STAIN_TOP - STAIN_FOOT) * t ** 0.55 + 1.6 * math.sin(y * 0.8)   # the half-width, licking
        for x in range(0, 56):
            d = (55.5 - x) / w                                 # 0 on the seam, 1 at the stain's edge
            if d >= 1:
                continue
            dens = 1 - d ** 3
            th = (BAYER[y % 4][x % 4] + 0.5) / 16
            role = "CHAR" if dens > 0.80 + th * 0.18 else "SOOT" if dens > 0.40 + th * 0.4 else \
                "ASHD" if dens > th * 0.7 else None
            if role:
                k.px(x, y, role)
                k.px(111 - x, y, role)


STAIN_TOP, STAIN_FOOT = 26, 11                      # the stain's half-width under the hole and at the doorway


# ============================================================================================ the MANSION
#  7x5 cells: 112x80. Rows 0..3 the building (all collision but the door), row 4 the porch below the door (cells
#  7..9 only; the rest of row 4 is ground and stays as it is). Drawn on the same 8px grid as SCORN SOLUTIONS: the
#  slates are one tile, the cave-in is a run of rack and coil tiles between two burnt edges that are one tile and
#  its mirror, each window and its plume is centred on a tile seam.
MANSION = dict(name="mansion", title="the MANSION", map="CinnabarIsland", x0=5, y0=0, w=7, h=5,
               door=(8, 3), keep=[], inplace=[], signs=[], row=MANSION_ROW, colours=MANSION_COLOURS,
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
    #  THE RIB CAGE (the user, 2026-10-24: the racks curved like a rib cage). A spine of annealed copper -- the coils'
    #  copper, in vertebrae -- down the middle of the hole, and the racks' steel curving out and down from it either
    #  side like ribs, longest in the middle, a bead of quicksilver at each tip. Mirrored about the door's seam (x 56),
    #  so the right half is the left half's tiles flipped.
    for y in range(0, 20):
        if y % 4 == 0:
            k.hline(54, 57, y, "COILL")
        elif y % 4 == 1:
            k.hline(54, 57, y, "COIL")
        else:
            k.hline(55, 56, y, "BRICK")
    for r, L in RIBS:
        for dx in range(2, L + 1):
            yy = r + round(RIB_DROP * (dx / L) ** RIB_EXP)
            for x in (56 - dx, 55 + dx):
                if yy + 1 >= 20 or x <= 32 + edge[yy] or x >= 79 - edge[yy]:
                    continue
                k.px(x, yy, "RACK")
                k.px(x, yy + 1, "RACKD")
        yy = r + RIB_DROP
        for x in (56 - L - 1, 55 + L + 1):
            if yy < 20 and 32 + edge[yy] < x < 79 - edge[yy]:
                k.px(x, yy, "QS")

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
    #  ONE STAIN (the user, 2026-10-24: one big soot stain rising from the cave-in down the facade, in place of a stain
    #  over every window). It is widest under the hole, where the fire broke through, and narrows down the wall to the
    #  doorway it came out of; the windows are only blown, not stained. Mirrored about the door's seam.
    stain(k, WALL0 + 1, 56)
    for c in MANSION_WINDOWS:
        wy0, wy1 = 38, 52
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
    #  the doorway: dark, its surround scorched, its lintel charred -- the stain's root
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


# ============================================================================================ 3/4 depth (pair 2, redrawn)
#  The user (2026-10-24) on the first pair-2 drafts: flat slabs. Both towers are now drawn as vanilla's buildings
#  are: a plan with CHAMFERED corners, seen from the south and above, so the front face is square on, the two chamfer
#  faces either side of it lean back (their edges rise 1px in 2), the left one lit and the right one shaded, and each
#  roof is a plane seen from above with its own stepped outline. The silhouette is INSET: the ground (BRAZEN's
#  paving, HALFTONE's cliff) shows at the sides as it did round vanilla's. Every horizontal on a face is drawn once,
#  as if on the front, and FACE_SIDE turns it to the lit or shaded side's colour where it lands on a chamfer.
CHAMFER = 8                       # one tile column: a chamfer face is one tile wide, so it costs one tile a row


def lean(x, xa, xb, c=CHAMFER):
    """how far a chamfer face's edges rise at x (0 across the front face): 1px in 2, from the corner outwards"""
    if x < xa + c:
        return (xa + c - x) // 2
    if x > xb - c:
        return (x - (xb - c)) // 2
    return 0


def side_of(x, xa, xb, c=CHAMFER):
    return "lit" if x < xa + c else "shade" if x > xb - c else "front"


def box_mask(xa, xb, back, top, bot, c=CHAMFER, cb=None):
    """an octagonal box seen from the south and above: {(x, y): "deck" | "face"} -- the deck from its back edge (its
    back corners stepped in as the front's are, or by `cb` for a rounder plan) down to the face's top edge, the face
    down to its foot"""
    m = {}
    for x in range(xa, xb + 1):
        L = lean(x, xa, xb, c)
        for y in range(back + lean(x, xa, xb, cb or c), top - L):
            m[(x, y)] = "deck"
        for y in range(top - L, bot - L + 1):
            m[(x, y)] = "face"
    return m


def outline(k, m, role="OUT"):
    for (x, y) in m:
        if any((x + dx, y + dy) not in m for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            k.px(x, y, role)


# ============================================================================================ CORPUS's tower
#  9x15 cells: 144x240. Canvas rows 0..15 are the walkable row behind the crown (SaffronCity y 16); 16..239 the tower.
#  THE BUDGET IS THE DESIGN: BRAZEN's tileset is full -- the tower owns 53 tiles and there is not one free slot -- so
#  everything that repeats is on the 8px grid: one window module (8x16) fourteen across and seven floors up, the same
#  module carried round onto the chamfers (lit on the left, shaded on the right), one deck sheet, one cornice.
#  Under the inset (the paving at its sides) the cells had no bottom layer -- vanilla drew its paving into the
#  building's own tiles -- so the tower's cells take BRAZEN's paving block (0x2E9) as their bottom layer: no new tile.
#  THE DOOR (33,30) is redrawn IN PLACE, block 0x2BC (METATILE_SaffronCity_SilphCoDoor) kept by id, so field_door.c
#  still finds its frames: its glass now shows the lobby, and the dark plate continues through it. Its pixels move
#  from the bottom layer of primary row 3 into row 9 (bottom layer still, top empty, as vanilla's), so its frames
#  must follow: gbadoors.py's DOORS["silph_co"] needs a "redrawn" spec (CORPUS_DOOR below) and --write then redraws
#  graphics/door_anims/silph_co.png from the new door and sets sDoorAnimPalettes_SilphCo 3 -> 9.
CORPUS_ROW = 9
CORPUS_COLOURS = [  # row 9 is drawn by the tower and by nothing else on either layout, so the tower takes all of it.
    #  The brass is a step deeper than BRAZEN's house brass (row 11) and the whole tower has a near-black outline, so
    #  at 1x it is the darkest, heaviest thing in the city and never one of its yellow houses.
    ("BRASSL", (236, 206, 124)),   # the decks, seen from above: brass catching the sky
    ("BRASS",  (204, 160, 72)),    # the lit chamfer; a floor's lip
    ("BRASSM", (162, 118, 46)),    # the front face
    ("BRASSD", (116, 80, 34)),     # the shaded chamfer; seams, reveals
    ("BRONZE", (78, 52, 28)),      # the base metal: the plinth, the shaded side's seams
    ("OUT",    (40, 26, 20)),      # the outline
    ("LIGHTL", (255, 226, 150)),   # a lit window -- every one, all night: amber, small, square
    ("LIGHT",  (226, 164, 78)),    # its lower pane; the shaded side's windows; the lobby's back wall
    ("RED",    (198, 34, 44)),     # the one thin band (4.4: his red, never named)
    ("GLASSL", (156, 213, 255)),   # the lobby's glass and the door's
    ("GLASS",  (115, 189, 246)),
    ("GLASSD", (74, 131, 197)),
    ("PLATE",  (24, 20, 30)),      # the plate cast into the floor -- the darkest colour, so it is the room behind the
                                   #   door when it opens (gbadoors' room). No words: nothing is drawn on it
    ("FLOOR",  (214, 206, 184)),   # the lobby floor
    ("FLOORD", (160, 150, 130)),   # its seams
]
CORPUS_LIT = {"BRASSM": "BRASS", "BRASS": "BRASSL", "BRASSD": "BRASSM", "BRONZE": "BRASSD"}
CORPUS_SHADE = {"BRASSL": "BRASS", "BRASS": "BRASSM", "BRASSM": "BRASSD", "BRASSD": "BRONZE", "BRONZE": "OUT",
                "LIGHTL": "LIGHT", "LIGHT": "BRASSM"}
#  gbadoors.py's spec for the redrawn door (the build adds it to DOORS["silph_co"] as "redrawn"): the two glass leaves
#  part from the middle (x 1..14 of the cell, the threshold below them kept)
CORPUS_DOOR = dict(block=0x2BC, row=CORPUS_ROW, kind="slide2", leaf=(1, 0, 14, 14))
CORPUS = dict(name="corpus_tower", title="CORPUS's tower", map="SaffronCity", x0=29, y0=16, w=9, h=15,
              door=(33, 30), keep=[], inplace=[(33, 30)], inplace_layer="bottom", signs=[], row=CORPUS_ROW,
              colours=CORPUS_COLOURS,
              #  the paving under the inset: BRAZEN's own (0x2E9 round the tower; the plaza's 0x2EC on the street row)
              ground=lambda x, y: 0x2EC if y >= 30 else 0x2E9,
              #  SaffronCity_Connection is the city again, offset (10, 7), drawn when the player stands on a crossing
              #  route: its tower cells are pointed at the same new blocks, so the two can never disagree
              mirrors=[("SaffronCity_Connection_Layout", 10, 7)],
              crop=[("SaffronCity_Layout", 27, 15, 13, 17)],
              caption=["Riveted brass in 3/4: a chamfered tower, the front square on, the left chamfer lit and the "
                       "right in shade, each roof a deck seen from above; BRAZEN's paving shows at its sides.",
                       "One grid of identical windows, small and amber, every one lit (running unattended), carried "
                       "round onto both chamfers. A deeper brass and a dark outline: never one of the yellow houses.",
                       "A stepped crown, three tiers, and one thin red band round the top one: the tower's only red.",
                       "At street level a glass lobby, and through it -- and now through the door's glass too -- "
                       "the dark plate cast into the floor. Nothing is written on it."],
              door_note=["THE DOOR (33,30): REDRAWN in place, block 0x2BC kept",
                         "by id; its glass shows the lobby, the plate",
                         "running on through it. Row 3 -> 9, so the build",
                         "also needs gbadoors' silph_co frames redrawn",
                         "(\"redrawn\" spec) and sDoorAnimPalettes_SilphCo",
                         "{3 x8} -> {9 x8}. Frames below, as it will open."])
#  the boxes, widest first: (xa, xb, the deck's back edge, the face's top, the face's foot)
CORPUS_SHAFT = (8, 135, 40, 80, 239)
CORPUS_TIERS = ((32, 111, 24, 56, 71), (48, 95, 8, 32, 47))
CORPUS_F0, CORPUS_F1 = 96, 207            # the seven floors of windows
CORPUS_LOBBY = (16, 127, 214)             # the glass lobby: x0, x1, the glass's top


def corpus_face(k, xa, xb, y0, y1, fn):
    """paint a face as if square on: fn(x, yf) gives the role at front-row yf; on a chamfer it lands lean(x) higher
    and in the lit or shaded side's colour"""
    for x in range(xa + 1, xb):
        L, side = lean(x, xa, xb), side_of(x, xa, xb)
        for yf in range(y0, y1 + 1):
            role = fn(x, yf)
            if role is None:
                continue
            if side == "lit":
                role = CORPUS_LIT.get(role, role)
            elif side == "shade":
                role = CORPUS_SHADE.get(role, role)
            k.px(x, yf - L, role)


def corpus_box(k, box, face_fn):
    xa, xb, back, top, bot = box
    m = box_mask(xa, xb, back, top, bot)
    for (x, y), part in m.items():
        if part == "deck":                                   # the deck: brass sheet from above, its back lip lit
            k.px(x, y, "BRASSL")
    corpus_face(k, xa, xb, top, bot, face_fn)
    for x in range(xa + 1, xb):                              # the eave: a dark crease where the deck meets the face
        k.px(x, top - lean(x, xa, xb), "OUT")
    #  the corners, each in its chamfer's own tile column: the lit one catching the light, the shaded one dark
    k.vline(xa + CHAMFER - 1, top + 1, bot, "BRASSL")
    k.vline(xb - CHAMFER + 1, top + 1, bot, "BRONZE")
    outline(k, m)
    return m


def corpus_shadow(k, box, dx=4, dy=3):
    """an upper tier's shadow, cast down and to the right onto the deck below it"""
    xa, xb, back, top, bot = box
    m = box_mask(xa, xb, back, top, bot)
    for (x, y) in m:
        sx, sy = x + dx, y + dy
        if (sx, sy) not in m and k.is_(sx, sy, "BRASSL"):
            k.px(sx, sy, "BRASS")
        elif (sx, sy) not in m and k.is_(sx, sy, "BRASS"):
            k.px(sx, sy, "BRASSM")


def draw_corpus():
    W, H = 144, 240
    k = Canvas(W, H, role_map(CORPUS_COLOURS))

    def shaft(x, yf):
        if yf < CORPUS_F0:                                   # the cornice: a lit lip, riveted brass, a seam
            r = yf - CORPUS_SHAFT[3]
            if r == 1:
                return "BRASS"
            if r == 7 and x % 8 in (3, 4):
                return "BRASS"
            if r == 8 and x % 8 in (3, 4):
                return "BRASSD"
            return "BRASSD" if r >= 14 else "BRASSM"
        if yf <= CORPUS_F1:                                  # the window module, 8x16, the same everywhere
            my, mx = (yf - CORPUS_F0) % 16, (x - 16) % 8
            if my == 0:
                return "BRASS"
            if my == 15:
                return "BRASSD"
            if 2 <= my <= 8 and 1 <= mx <= 5:
                if my == 2 or mx == 1:
                    return "BRASSD"                          # the reveal, in shadow at its top and left
                return "LIGHTL" if my <= 6 else "LIGHT"
            if my == 9 and 1 <= mx <= 6:
                return "BRASS"                               # the sill
            if my == 12 and mx in (3, 4):
                return "BRASS"                               # a rivet under each window
            if my == 13 and mx in (3, 4):
                return "BRASSD"
            return "BRASSM"
        r = yf - (CORPUS_F1 + 1)                             # the base: a fascia, riveted piers, a bronze plinth
        if r == 0:
            return "BRASS"
        if r == 5:
            return "BRASSD"
        if yf >= 232:
            return "BRASSD" if yf == 232 else "BRONZE"
        if (yf - 214) % 8 == 3 and x % 8 in (3, 4):
            return "BRASS"
        if (yf - 214) % 8 == 4 and x % 8 in (3, 4):
            return "BRASSD"
        return "BRASSM"

    corpus_box(k, CORPUS_SHAFT, shaft)
    for i, t in enumerate(CORPUS_TIERS):
        top = t[3]

        def fn(x, yf, top=top, last=(i == len(CORPUS_TIERS) - 1), bot=t[4]):
            r = yf - top
            if r == 1:
                return "BRASS"
            if last and r in (4, 5):
                return "RED"                                 # THE ONE THIN RED BAND, round the top tier only
            if yf == bot - 1:
                return "BRASSD"
            if not last and r == 7 and x % 8 in (3, 4):
                return "BRASS"
            if not last and r == 8 and x % 8 in (3, 4):
                return "BRASSD"
            return "BRASSM"
        corpus_shadow(k, t)
        corpus_box(k, t, fn)

    # --- THE LOBBY: the whole front at street level, set back under the fascia: glass, and through the glass the lit
    #  hall and the plate in its floor. Mirrored about the door's seam (x 72), so its right half is its left half's
    #  tiles flipped; its mullions stand in pairs on the cell seams, so every pane between them is one tile and its flip.
    L0, L1, G0 = CORPUS_LOBBY
    k.rect(L0, G0, L1, 238, "LIGHT")                          # the lit hall's back wall
    k.hline(L0, L1, G0, "BRASSD")                            # the fascia's shadow on the glass's head
    k.hline(L0, L1, G0 + 1, "GLASSL")
    k.hline(L0, L1, G0 + 2, "GLASS")
    FL = 226                                                  # where the floor meets the back wall
    k.rect(L0, FL, L1, 238, "FLOOR")
    k.hline(L0, L1, FL, "FLOORD")
    #  THE PLATE: a long dark slab cast into the floor, its rim worn, set in a joint -- seen from the street through the
    #  glass, and now through the door's glass too. Nothing is written on it.
    P0, P1, PY0, PY1 = 36, 107, 229, 236
    k.rect(P0 - 1, PY0 - 1, P1 + 1, PY1 + 1, "OUT")
    k.rect(P0, PY0, P1, PY1, "BRONZE")
    k.rect(P0 + 1, PY0 + 1, P1 - 1, PY1, "PLATE")
    for x in range(L0 + 15, L1, 16):
        k.vline(x, G0 + 1, 238, "GLASSD")                     # the mullions, in pairs on the cell seams
        k.vline(x + 1, G0 + 1, 238, "GLASSD")
    k.vline(L0, G0, 238, "BRASSD")                           # the reveals: the glass is set back in the brass
    k.vline(L1, G0, 238, "BRASSD")
    #  the door: two glass leaves meeting at the cell's middle, framed, a glint on each, the plate seen on through them
    k.hline(64, 79, 224, "GLASSD")
    for x in (71, 72):
        k.vline(x, 225, 238, "GLASSD")
    for i in range(4):
        k.px(66 + i, 231 - i, "GLASSL")
        k.px(74 + i, 231 - i, "GLASSL")
    k.hline(L0, L1, 239, "OUT")                               # the threshold
    return k


# ============================================================================================ DAEMON TOWER
#  7x15 cells: 112x240, ONE tower on two maps -- canvas cell rows 0..7 are ROUTE 10's rows 72..79 (its top: vanilla's
#  dome, which ROUTE 10 draws and LAVENDER shows over the seam), 8..14 LAVENDER's rows 0..6. Rows 72-73 are walkable:
#  the mast and the dome's crown stand over the ground there, as vanilla's did. The door (18,6) is a plain doorway
#  (MB 0x60, no animation): redrawn, its dark below and its frame above, as the MANSION's.
#  HALFTONE greys the whole palette while the town is unperceived (DaemonsIsHalftone), so it must read in grey alone,
#  and it does it the way a halftone does: the DOT SIZE is the shading. Sparse specks at the top, dense at the foot;
#  smaller on the lit chamfer, bigger on the shaded one. The screen is a 45 degree lattice whose rows sit in the tile
#  rows (centres in one row, on the seams in the next), so a row of dots is ONE tile across, and its chamfers one each.
#  Its cells keep their own bottom layer -- ROUTE 10's and LAVENDER's cliff and grass -- so the inset shows the cliff.
DTOWER_ROW = 7
DTOWER_COLOURS = [  # indices 1..9 of row 7 (unused, all 0000ff); 10..15 are left for the KEEPALIVE PLANT (same tileset)
    ("PAPER",  (238, 236, 242)),   # the paper: the tower's white
    ("PAPERS", (204, 200, 214)),   # paper turned from the light: the shaded chamfer, the deck
    ("INK",    (40, 36, 52)),      # the dots
    ("OUT",    (22, 20, 30)),      # outline; the doorway's dark
    ("NICHE",  (62, 56, 78)),      # inside a niche
    ("MID",    (140, 134, 154)),   # the parapet's inner shadow, the dome's foot, a niche's arch
    ("GLOW",   (252, 206, 120)),   # the light in each niche: a candle, or a status lamp
    ("GLOWD",  (178, 124, 70)),    # its warmth on the niche's floor
    ("PAPERL", (252, 252, 255)),   # paper in full light: the lit chamfer, the parapet's lip
]
DTOWER = dict(name="daemon_tower", title="DAEMON TOWER", map="LavenderTown", x0=15, y0=0, w=7, h=7, door=(18, 6),
              keep=[], inplace=[], signs=[], row=DTOWER_ROW, colours=DTOWER_COLOURS, cy0=8,
              #  the tower's top is ROUTE 10's (rows 72..79), drawn into the same canvas above
              parts=[("Route10_Layout", 15, 72, 7, 8, 0, 0)],
              lintel=lambda k, x, y: not (50 <= x <= 61 and y >= 227),
              crop=[("Route10_Layout", 14, 70, 9, 10), ("LavenderTown_Layout", 14, 0, 9, 8)],
              caption=["Halftone in 3/4: a chamfered drum, the lit chamfer in specks, the shaded one in heavy dots, "
                       "the front between -- the dot size is the shading, so it reads in grey alone.",
                       "Dense at the foot, sparse at the top; vanilla's dome kept as a silhouette and drawn in the dot "
                       "screen, a mast with one light over it. The cliff shows at its sides.",
                       "Seven bands of arched niches cut straight into the dots -- no shelves -- a small amber light "
                       "in each: a columbarium as much as a rack.",
                       "One tower on two maps: its top is ROUTE 10's rows 72..79, redrawn with it.",
                       "Grey while HALFTONE is unperceived (DaemonsHalftoneMix); its colours only after INIT. Row 7, "
                       "1..9 only: 10..15 are the KEEPALIVE PLANT's."],
              door_note=["THE DOOR (18,6): a plain doorway (MB 0x60,",
                         "no animation), drawn as the MANSION's -- its dark",
                         "below, its frame above the player. No frames."])
DTOWER_DRUM = (8, 103, 36, 96, 239)
DTOWER_BACK_CHAMFER = 26                 # the deck's back corners: vanilla's octagon, rounder than the drum's       # the drum: (xa, xb, the deck's back edge, the face's top, its foot)
DTOWER_NICHES = (104, 120, 136, 152, 168, 184, 200)   # the seven bands, each one tile row
DTOWER_DOME = (56.0, 72, 42, 46, 13)      # centre x (the tile seam), the equator's y, rx, the crown's ry, the foot's ry


def dtower_r(y):
    """the dot's radius on the front at height y: specks under the dome, merging toward the foot"""
    t = min(1.0, max(0.0, (y - 96) / (236 - 96)))
    return 0.9 + 3.7 * t ** 1.25


def dot_ink(x, y, r, y_lo=None, y_hi=None):
    """is pixel (x, y) inside a dot of radius r on the 45 degree lattice? Each lattice row sits in one tile row: centres
    at x 8i+4 in even tile rows, on the seams (8i) in odd ones -- clipped to its tile row, so dots merge sideways only"""
    j = y // 8
    cy = j * 8 + 4
    cxs = (4,) if j % 2 == 0 else (0, 8)
    lx = x % 8
    return any(((lx + 0.5 - c) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5 <= r for c in cxs)


def draw_dtower():
    W, H = 112, 240
    k = Canvas(W, H, role_map(DTOWER_COLOURS))
    xa, xb, back, top, bot = DTOWER_DRUM
    # --- the drum's top, seen from above: a deck inside a parapet, its octagon stepped like the drum below it
    m = box_mask(xa, xb, back, top, bot, cb=DTOWER_BACK_CHAMFER)
    for (x, y), part in m.items():
        if part == "deck":
            k.px(x, y, "PAPERS")
    for x in range(xa, xb + 1):                               # the parapet: a lit lip, its inner shadow on the deck
        L = lean(x, xa, xb)
        Lb = lean(x, xa, xb, DTOWER_BACK_CHAMFER)
        k.px(x, back + Lb + 1, "PAPERL")
        k.px(x, back + Lb + 2, "MID")
        k.px(x, top - L - 1, "PAPERL")                        # the front lip, over the face
    for y in range(back, top):
        for x in (xa + 1, xb - 1):
            if (x, y) in m and m[(x, y)] == "deck" and (x, y - 1) in m:
                k.px(x, y, "PAPERL" if x == xa + 1 else "MID")
    # --- the face: halftone, the dot size by height and by side
    for (x, y), part in m.items():
        if part != "face":
            continue
        L = lean(x, xa, xb)
        yf = y + L                                             # the front row this pixel is drawn as
        side = side_of(x, xa, xb)
        r = dtower_r(yf)
        #  the chamfers' dots step in whole levels, so a level repeats down the side (two tile rows share a tile)
        if side == "lit":
            r, paper = max(0.5, int(r - 0.6) + 0.5), "PAPERL"
        elif side == "shade":
            r, paper = int(r + 1.4) + 0.5, "PAPERS"
        else:
            paper = "PAPER"
        k.px(x, y, "INK" if dot_ink(x, yf, r) else paper)
    #  THE NICHES: seven bands of arched niches cut straight into the dots -- no shelf, no band -- each with a small
    #  amber light. Every niche the same, one per tile, on the front only; the paper round each arch is kept clear.
    for b in DTOWER_NICHES:
        for x0 in range(xa + CHAMFER + 1, xb - CHAMFER, 8):   # 16, 24, .. 88: ten across
            for ly in range(8):
                for lx in range(8):
                    x, y = x0 + lx, b + ly
                    arch = (2 <= lx <= 5 and 2 <= ly <= 7) or (3 <= lx <= 4 and ly == 1)
                    margin = (1 <= lx <= 6 and 1 <= ly <= 7) or (2 <= lx <= 5 and ly == 0)
                    if arch:
                        k.px(x, y, "NICHE")
                    elif margin:
                        k.px(x, y, "PAPER")
            k.px(x0 + 2, b + 2, "MID"); k.px(x0 + 5, b + 2, "MID")    # the arch's springing
            k.hline(x0 + 3, x0 + 4, b + 5, "GLOW")                    # the light
            k.hline(x0 + 3, x0 + 4, b + 6, "GLOWD")
            k.hline(x0 + 2, x0 + 5, b + 7, "GLOWD")                   # its warmth on the niche's floor
    #  the corners: a lit edge where the lit chamfer meets the front, a dark one where the shaded one does
    for y in range(top + 1, bot + 1):
        k.px(xa + CHAMFER - 1, y - lean(xa + CHAMFER - 1, xa, xb) + 0, "PAPERL")
        k.px(xb - CHAMFER + 1, y - lean(xb - CHAMFER + 1, xa, xb), "MID")
    for x in range(xa + 1, xb):                                # the eave: the parapet's shadow on the face's head
        k.px(x, top - lean(x, xa, xb), "OUT")
    outline(k, m)
    # --- THE DOME: vanilla's silhouette -- a dome on the drum, its crown up over ROUTE 10's walkable row -- in the
    #  dot screen: specks at its crown, heavier toward its foot. Symmetric about the tile seam at x 56.
    cx, eq, rx, ryt, ryb = DTOWER_DOME
    dome = set()
    for y in range(eq - ryt, eq + ryb + 1):
        for x in range(W):
            ry = ryt if y < eq else ryb
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - eq) / ry) ** 2 <= 1:
                dome.add((x, y))
    for (x, y) in dome:
        t = max(0.0, (y - (eq - ryt)) / (ryt + ryb))
        r = 0.35 + 2.4 * t ** 1.6
        k.px(x, y, "INK" if dot_ink(x, y, r) else "PAPER")
    for (x, y) in dome:
        if (x, y + 1) not in dome and y > eq:
            k.px(x, y, "MID")                                  # its foot on the deck
            k.px(x, y + 1, "MID")
    outline(k, dome)
    # --- the mast on its crown, one light at its tip (a vigil, or an aircraft lamp)
    k.rect(55, 6, 56, eq - ryt, "INK")
    k.hline(54, 57, 14, "INK")
    k.hline(55, 56, 3, "GLOW"); k.hline(55, 56, 4, "GLOWD")
    # --- the doorway: a white frame in the dark foot, and the dark inside
    k.rect(46, 223, 65, 239, "PAPERL")
    k.hline(46, 65, 223, "OUT")
    k.vline(46, 223, 239, "OUT"); k.vline(65, 223, 239, "OUT")
    k.rect(50, 227, 61, 239, "OUT")
    k.hline(50, 61, 237, "MID")                               # the threshold
    k.hline(50, 61, 238, "PAPERS")
    return k


# ============================================================================================ the tilesets
#  One group per secondary tileset: its landmarks are drawn, cut and placed together, because they share its tiles,
#  blocks and rows. The first pair keeps exactly the behaviour it was built with (a fresh block per cell, appended);
#  the second pair's tilesets are fuller, so their groups REUSE blocks: identical cells share one block, and the
#  blocks only the landmark drew (on every layout and border) are rewritten in place before any is appended.
GROUPS = [
    dict(dir="cinnabar_island", symbol="gTileset_CinnabarIsland", layout="CinnabarIsland_Layout",
         place="QUICKSILVER IS. / CinnabarIsland", town="QUICKSILVER IS.", tag="t447b",
         landmarks=[(SCORN, draw_scorn), (MANSION, draw_mansion)], reuse_blocks=False,
         view=[("CinnabarIsland_Layout", 0, 0, 24, 20)]),
    dict(dir="saffron_city", symbol="gTileset_SaffronCity", layout="SaffronCity_Layout",
         place="BRAZEN / SaffronCity", town="BRAZEN", tag="t447e", landmarks=[(CORPUS, draw_corpus)],
         reuse_blocks=True, view=[("SaffronCity_Layout", 17, 9, 32, 26)]),
    dict(dir="lavender_town", symbol="gTileset_LavenderTown", layout="LavenderTown_Layout",
         place="HALFTONE / LavenderTown (+ ROUTE 10's rows 72..79)", town="HALFTONE", tag="t447e",
         landmarks=[(DTOWER, draw_dtower)], reuse_blocks=True, halftone=True,
         #  the free slots past -num_tiles are shared with the KEEPALIVE PLANT: the tower draws into its own tiles
         #  only, and 702 (gbatowns' source for the roofs' copy, batch F) is never repainted
         free_slots=False, avoid={702 - NUM_PRIMARY},
         view=[("Route10_Layout", 0, 66, 24, 14), ("LavenderTown_Layout", 0, 0, 24, 20)]),
]
#  this tool's claim; gbatowns.py's LANDMARKS keeps the same boxes out of its passes (by map name)
OWNS = {"cinnabar_island": [("CinnabarIsland", 5, 0, 7, 5, "the MANSION"),
                            ("CinnabarIsland", 5, 6, 7, 4, "SCORN SOLUTIONS (the lab)")],
        "saffron_city": [("SaffronCity", 29, 16, 9, 15, "CORPUS's tower"),
                         ("SaffronCity_Connection", 19, 9, 9, 15, "CORPUS's tower (the crossings' copy)")],
        "lavender_town": [("LavenderTown", 15, 0, 7, 7, "DAEMON TOWER"),
                          ("Route10", 15, 72, 7, 8, "DAEMON TOWER (its top, on ROUTE 10)")]}
GROUP = TILESET = LANDMARKS_HERE = None


def use(g):
    """make `g` the group every function below works on"""
    global GROUP, TILESET, LANDMARKS_HERE
    GROUP, TILESET, LANDMARKS_HERE = g, g, g["landmarks"]


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


def cells_of(lm):
    """every cell the landmark draws: (layout, x, y, canvas cell x, canvas cell y) -- the main layout's footprint
    (canvas row lm["cy0"] onwards), then each extra part on another layout (DAEMON TOWER's top is ROUTE 10's)"""
    cy0 = lm.get("cy0", 0)
    out = [(TILESET["layout"], x, y, x - lm["x0"], y - lm["y0"] + cy0) for x, y in footprint_cells(lm)]
    for layout, x0, y0, w, h, cx0, cy0p in lm.get("parts", ()):
        out += [(layout, x, y, x - x0 + cx0, y - y0 + cy0p) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    return out


def mirror_cells(lm, x, y):
    """the same cell on the layouts that copy the main one (SaffronCity_Connection: the city again, offset)"""
    return [(layout, x - dx, y - dy) for layout, dx, dy in lm.get("mirrors", ())]


def ours_of(landmarks):
    """every (layout, x, y) the landmarks redraw, mirrors included (kept cells are not ours)"""
    out = set()
    for lm, _ in landmarks:
        for layout, x, y, _, _ in cells_of(lm):
            if layout == TILESET["layout"] and (x, y) in lm["keep"]:
                continue
            out.add((layout, x, y))
            if layout == TILESET["layout"]:
                out |= set(mirror_cells(lm, x, y))
    return out


def census(ts, ours):
    """{secondary tile: True} for every tile the landmarks may repaint: drawn ONLY by our cells (every layout, every
    border), not one of the kept cells' tiles, and below DOOR_TILE_START; plus the slots nothing draws.
    Returns (owned slots, free slots, what was examined)."""
    users = {}                                   # tile -> set of (layout, x, y) / ("border", layout)
    examined = 0
    ours_set = set(ours)
    #  the blocks this tool appended are drawn only by our cells: the three RS Safari layouts (unused by any map) carry
    #  block ids past vanilla's count that were nothing before a --write and are ours after it -- counted as users,
    #  they made a second --write see its own tiles as shared and refuse (2026-10-24)
    limit = vanilla_block_count(ts)
    for name, m in ts.maps.items():
        for y in range(m["h"]):
            for x in range(m["w"]):
                b = ts.cell(name, x, y) & 0x3FF
                examined += 1
                if b - NUM_PRIMARY >= limit and (name, x, y) not in ours_set:
                    continue
                if b >= NUM_PRIMARY and b - NUM_PRIMARY < ts.nblocks:
                    for e in ts.entries(b):
                        t = e & 0x3FF
                        if t >= NUM_PRIMARY:
                            users.setdefault(t - NUM_PRIMARY, set()).add((name, x, y))
        for b in m["border"]:
            if b >= NUM_PRIMARY and b - NUM_PRIMARY < limit:
                for e in ts.entries(b):
                    if (e & 0x3FF) >= NUM_PRIMARY:
                        users.setdefault((e & 0x3FF) - NUM_PRIMARY, set()).add(("border", name))
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
    cells = ours_of(LANDMARKS_HERE)
    owned, free, users, examined, referenced = census(ts, cells)
    if not GROUP.get("free_slots", True):
        free = []                                # this tileset's free slots are another landmark's to share
    owned = [t for t in owned if t not in GROUP.get("avoid", ())]
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
        for (layout, x, y, cx, cy) in cells_of(lm):
            main = layout == TILESET["layout"]
            if main and (x, y) in lm["keep"]:
                continue
            raw = ts.cell(layout, x, y)
            old = raw & 0x3FF
            ox, oy = cx * 16, cy * 16
            keys = [tuple(k.get(ox + qx * 8 + i % 8, oy + qy * 8 + i // 8) for i in range(64))
                    for qy in (0, 1) for qx in (0, 1)]
            if lm.get("parts") and old < NUM_PRIMARY and not any(any(key) for key in keys):
                continue                            # plain ground the drawing leaves alone (the mast's neighbours)
            art = [cut.tile(key, row) for key in keys]
            if old >= NUM_PRIMARY:
                e = ts.entries(old)
                attr = ts.attr(old)
            else:                                   # a primary ground cell (the porch's): ground below, art above
                e = list(struct.unpack_from("<8H", open(os.path.join(PRIMARY, "metatiles.bin"), "rb").read(), old * 16))
                attr = None
            bottom = e[:4]
            lin = lm.get("lintel", lintel)
            if main and (x, y) in lm["inplace"] and lm.get("inplace_layer") == "bottom":
                entries = art + [0, 0, 0, 0]        # a door drawn in its bottom layer (CORPUS's): art below, top empty
            elif main and (x, y) in lm["inplace"]:  # the door block, kept by id: its empty bottom kept, art on top
                entries = bottom + art
            elif main and (x, y) in lm["signs"]:      # the board's own tiles stay on top; the wall is ours, below
                entries = art + [0, 0, e[6], e[7]]
            elif main and (x, y) == lm["door"]:     # a plain doorway: all of it below, the lintel above
                lint = [cut.tile(tuple(k.get(ox + qx * 8 + i % 8, oy + qy * 8 + i // 8)
                                       if lin(k, ox + qx * 8 + i % 8, oy + qy * 8 + i // 8) else 0
                                       for i in range(64)), row) for qy in (0, 1) for qx in (0, 1)]
                entries = art + lint
            else:
                if not any(v & 0x3FF for v in bottom):
                    bottom = ground_under(ts, lm, x, y, layout)
                entries = bottom + art
            plan.append((x, y, raw, old, entries, attr, main and (x, y) in lm["inplace"], layout,
                         mirror_cells(lm, x, y) if main else []))
        per[lm["name"]] = len(cut.placed) - n0
    #  place: a fresh block per cell, appended (or this tool's own block from an earlier write, rewritten)
    reuse = owned_blocks(ts, cells, users_of_blocks(ts)) if GROUP.get("reuse_blocks") else None
    shared = {}                                     # (entries, attributes) -> the block every such cell shares
    for x, y, raw, old, entries, attr, inplace, layout, mirrors in plan:
        if inplace:                                 # a block kept by id: rewritten where it is, attributes untouched
            struct.pack_into("<8H", new_mt, (old - NUM_PRIMARY) * 16, *entries)
            continue
        if reuse is not None:
            a = attr if attr is not None else bytes(ts.per_attr)
            key = (tuple(entries), a)
            if key not in shared:
                if reuse:
                    bid = reuse.pop(0)
                else:
                    bid = NUM_PRIMARY + nblocks
                    nblocks += 1
                    new_mt += bytes(16)
                    new_at += bytes(ts.per_attr)
                o = bid - NUM_PRIMARY
                struct.pack_into("<8H", new_mt, o * 16, *entries)
                new_at[o * ts.per_attr:(o + 1) * ts.per_attr] = a
                shared[key] = bid
            bid = shared[key]
            ts.set_cell(layout, x, y, (raw & ~0x3FF) | bid)
            for ml, mx, my in mirrors:
                ts.set_cell(ml, mx, my, (ts.cell(ml, mx, my) & ~0x3FF) | bid)
            continue
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
        pals[lm["row"]] = row_pal(ts, lm)
    return dict(drawings=drawings, mt=new_mt, at=new_at, tiles=img, pals=pals, num_tiles=max(used_top, ts.num_tiles),
                cut=cut, owned=owned, free=free, examined=examined, nblocks=nblocks, old_nblocks=ts.nblocks,
                kept_tiles=kept_tiles, users=users, plan=plan, per=per)


def users_of_blocks(ts):
    """{secondary block id: every (layout, x, y) and ("border", layout) that draws it}"""
    users = {}
    for name, m in ts.maps.items():
        for y in range(m["h"]):
            for x in range(m["w"]):
                users.setdefault(ts.cell(name, x, y) & 0x3FF, set()).add((name, x, y))
        for b in m["border"]:
            users.setdefault(b, set()).add(("border", name))
    return users


def labelled_blocks():
    """this tileset's block ids the engine names (include/constants/metatile_labels.h, METATILE_<Tileset>_*): code or
    a script may draw them by id, so they are never rewritten as something else"""
    src = open(os.path.join(GBA, "include/constants/metatile_labels.h")).read()
    pre = GROUP["symbol"][len("gTileset_"):]
    return {int(v, 16) for v in re.findall(r"#define METATILE_%s_\w+\s+(0x[0-9A-Fa-f]+)" % pre, src)}


def owned_blocks(ts, ours, users):
    """the blocks only the landmark's cells draw (every layout, every border) and the engine never names: the
    landmark's to rewrite, lowest first. A rerun finds the same blocks in the same order (they are ours by then)."""
    named = labelled_blocks()
    return [b for b in sorted(users) if NUM_PRIMARY <= b < NUM_PRIMARY + ts.nblocks and b not in named
            and users[b] <= set(ours)]


def lintel(k, x, y):
    """the mansion door cell's top layer: everything that is not the dark opening (the player passes under it)"""
    return not k.is_(x, y, "VOID") or y < 48


def ground_under(ts, lm, x, y, layout=None):
    """a cell vanilla left with no bottom layer: the landmark's own ground block if it names one (CORPUS's paving),
    else borrow the nearest footprint cell's ground in the same row"""
    layout = layout or TILESET["layout"]
    if lm.get("ground"):
        return ts.entries(lm["ground"](x, y))[:4]
    for dx in range(1, 8):
        for xx in (x - dx, x + dx):
            if lm["x0"] <= xx < lm["x0"] + lm["w"]:
                b = ts.cell(layout, xx, y) & 0x3FF
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
            if (x, y) not in lm["keep"] and (x, y) not in lm["signs"] and (x, y) not in lm["inplace"]]
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


SHEET_TAG = "t447b"                 # the second draft (the user's answers, 2026-10-24); t447a was the first
BG, FG, DIM, GOLD = (30, 30, 36), (232, 232, 236), (150, 150, 160), (232, 196, 96)


def up(im, n):
    return im.resize((im.width * n, im.height * n), Image.NEAREST)


def door_preview(k):
    """SCORN SOLUTIONS' steel door opening, as gbadoors.py will draw it once the closed door is built: its own
    open_frames() on the closed cell in row 10, with DOORS' "redrawn" spec. Imported the house way (engine.md trap
    16): argv swapped round the import, so its --write can never be armed from here. Returns (frames, spec, fit)."""
    import contextlib, io as _io
    argv, sys.argv = sys.argv, ["gbadoors"]
    try:
        with contextlib.redirect_stdout(_io.StringIO()):
            import gbadoors
    finally:
        sys.argv = argv
    pal = pal16(SCORN_COLOURS)
    ox, oy = (SCORN["door"][0] - SCORN["x0"]) * 16, (SCORN["door"][1] - SCORN["y0"]) * 16
    closed = [[(SCORN_ROW, k.get(ox + x, oy + y), pal[k.get(ox + x, oy + y)]) for x in range(16)] for y in range(16)]
    spec = gbadoors.redrawn_spec(dict(gbadoors.DOORS["cinnabar_lab"]), closed)
    row = gbadoors.Row(pal)
    off, _ = gbadoors.fit(closed, [row] * 4)
    frames = gbadoors.open_frames(closed, lambda x, y: row, spec)
    return [[[c[2] for c in line] for line in closed]] + frames, spec, off


def corpus_door_preview(k):
    """CORPUS's door opening, as gbadoors.py will draw it once its DOORS["silph_co"] carries CORPUS_DOOR as its
    "redrawn" spec and the closed door is built in row 9: its own redrawn_spec(), fit() and open_frames() on the
    closed cell, imported the house way (argv swapped round the import, so its --write can never be armed from here).
    Returns (frames: closed + ajar, half, open; the spec taken; pixels of the closed door not in row 9)."""
    import contextlib, io as _io
    argv, sys.argv = sys.argv, ["gbadoors"]
    try:
        with contextlib.redirect_stdout(_io.StringIO()):
            import gbadoors
    finally:
        sys.argv = argv
    pal = pal16(CORPUS_COLOURS)
    ox, oy = (CORPUS["door"][0] - CORPUS["x0"]) * 16, (CORPUS["door"][1] - CORPUS["y0"]) * 16
    closed = [[(CORPUS_ROW, k.get(ox + x, oy + y), pal[k.get(ox + x, oy + y)]) for x in range(16)] for y in range(16)]
    assert all(c[1] for line in closed for c in line), "the door cell must be opaque: its frames repaint all of it"
    spec = dict(gbadoors.DOORS["silph_co"])
    spec.setdefault("redrawn", {n: v for n, v in CORPUS_DOOR.items() if n != "block"})
    spec = gbadoors.redrawn_spec(spec, closed)
    row = gbadoors.Row(pal)
    off, _ = gbadoors.fit(closed, [row] * 4)
    frames = gbadoors.open_frames(closed, lambda x, y: row, spec)
    return [[[c[2] for c in line] for line in closed]] + frames, spec, off


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
        if lm is SCORN:
            frames, spec, off = door_preview(after["drawings"]["scorn_solutions"])
            assert spec["kind"] == SCORN_DOOR["kind"] and tuple(spec["leaf"]) == SCORN_DOOR["leaf"] and off == 0, spec
            assert [tuple(c) for c in spec.get("room_avoid", [])] == [dict(SCORN_COLOURS)["RED"]], spec   # red: the light's only
            assert all(c != dict(SCORN_COLOURS)["RED"] for f in frames for line in f for c in line), "red in the door"
            xx = 24 + 384 * 2 + 16 + 24 - 4 * (16 * 5 + 8)
            yd = yy
            d.text((xx, yd - 4), "the door (gbadoors' frames, row 10):", fill=GOLD, font=Fs)
            for i, f in enumerate(frames):
                im = Image.new("RGB", (16, 16))
                im.putdata([c for line in f for c in line])
                s.paste(up(im, 5), (xx + i * (16 * 5 + 8), yd + 12))
                d.text((xx + i * (16 * 5 + 8), yd + 96), ("closed", "ajar", "half", "open")[i], fill=DIM, font=Fs)
        p = os.path.join(out, SHEET_TAG + "_%s.png" % lm["name"])
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
    for entries in (p[4] for p in after["plan"]):
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
    p = os.path.join(out, SHEET_TAG + "_tiles.png"); s.save(p); paths.append(p)
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
    p = os.path.join(out, SHEET_TAG + "_palettes.png"); s.save(p); paths.append(p)
    return paths


# ============================================================================================ main
def gbatowns_landmarks():
    src = open(os.path.join(ROOT, "tools", "gbatowns.py")).read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LANDMARKS" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def row_pal(ts, lm):
    """the landmark's palette row: its colours from index 1; a row it shares (DAEMON TOWER's row 7, whose 10..15 are
    left for the KEEPALIVE PLANT) keeps whatever stands past them"""
    cols = [rgb for _, rgb in lm["colours"]]
    if len(cols) == 15:
        return pal16(lm["colours"])
    return [TRANSPARENT] + cols + list(ts.pals[lm["row"]])[1 + len(cols):]


def row_users(ts, row):
    """every (layout, x, y) that draws a tile in palette row `row` (secondary or primary tiles)"""
    pmt = primary()["mt"]
    out = set()
    for name, m in ts.maps.items():
        for y in range(m["h"]):
            for x in range(m["w"]):
                b = ts.cell(name, x, y) & 0x3FF
                e = struct.unpack_from("<8H", pmt, b * 16) if b < NUM_PRIMARY else \
                    ts.entries(b) if b - NUM_PRIMARY < ts.nblocks else []
                if any(v & 0x3FF and v >> 12 == row for v in e):
                    out.add((name, x, y))
    return out


def row_check(ts, lm, ours):
    """a landmark's row must be free (vanilla's unused rows are all black or all blue), already ours, or drawn by
    the landmark's cells and nothing else -- never a row another block draws"""
    cur, want = ts.pals[lm["row"]], row_pal(ts, lm)
    n = len(lm["colours"])
    if all(c in ((0, 0, 0), (0, 0, 255)) for c in cur[1:1 + n]):
        return "free"
    if list(cur[1:1 + n]) == list(want[1:1 + n]):
        return "ours"
    others = row_users(ts, lm["row"]) - set(ours)
    if not others:
        return "drawn by the landmark alone"
    raise SystemExit("  row %d is not free and not ours: %d other cells draw it, e.g. %s"
                     % (lm["row"], len(others), sorted(others)[:4]))


# ============================================================================================ pair 2's sheets
class MapState:
    def __init__(self, maps):
        self.maps = maps


def render_pieces(state, mt, tiles_img, pals, pieces):
    """map boxes rendered and stacked top to bottom (DAEMON TOWER: ROUTE 10's foot over LAVENDER's head)"""
    ims = [render(state, mt, tiles_img, pals, *p) for p in pieces]
    out = Image.new("RGB", (max(i.width for i in ims), sum(i.height for i in ims)))
    y = 0
    for im in ims:
        out.paste(im, (0, y))
        y += im.height
    return out


def halftone_grey(im):
    """DaemonsHalftoneMix(c, 0) (fieldmap.c): Q_8_8 0.3 R + 0.59 G + 0.1133 B on the GBA's five bits"""
    out = im.copy()
    o = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b = (c >> 3 for c in o[x, y][:3])
            v = (r * 76 + g * 151 + b * 29) >> 8
            o[x, y] = (v << 3 | v >> 2,) * 3
    return out


def crop_of(lm):
    if lm.get("crop"):
        return lm["crop"]
    y0 = max(0, lm["y0"] - 1)
    return [(TILESET["layout"], lm["x0"] - 1, y0, lm["w"] + 2, lm["y0"] + lm["h"] + 1 - y0)]


def label(d, xy, text, fill, f):
    d.text(xy, text, fill=fill, font=f)


def sheets_pair2(ts, before_maps, before, after, out):
    """per landmark: TODAY | DRAFT at 3x (and in HALFTONE's grey), both at 1x, the town at 1x; then the tileset's
    tiles, rows and budget"""
    os.makedirs(out, exist_ok=True)
    F, Fs, Fb = font(14), font(12), font(22)
    today_s, draft_s = MapState(before_maps), MapState(ts.maps)
    ht = GROUP.get("halftone")
    paths = []
    for lm, _ in LANDMARKS_HERE:
        pieces = crop_of(lm)
        t = render_pieces(today_s, before["mt"], before["tiles"], before["pals"], pieces)
        d_ = render_pieces(draft_s, after["mt"], after["tiles"], after["pals"], pieces)
        tv = render_pieces(today_s, before["mt"], before["tiles"], before["pals"], GROUP["view"])
        dv = render_pieces(draft_s, after["mt"], after["tiles"], after["pals"], GROUP["view"])
        rows3 = [("", t, d_)] + ([(" in HALFTONE's grey", halftone_grey(t), halftone_grey(d_))] if ht else [])
        one = [t, d_] + ([halftone_grey(t), halftone_grey(d_)] if ht else [])
        towns = [(tv, dv)] + ([(halftone_grey(tv), halftone_grey(dv))] if ht else [])
        cap = lm.get("caption", [])
        W = max(24 + t.width * 3 * 2 + 24 + 24 + 520, 24 + (tv.width + 16) * 2 * (2 if ht else 1) + 24)
        Hh = 96 + 18 * len(cap) + len(rows3) * (t.height * 3 + 34) + t.height + 34 + tv.height + 50
        s = Image.new("RGB", (W, Hh), BG)
        d = ImageDraw.Draw(s)
        label(d, (24, 16), "%s  --  T-447 DRAFT, pair 2 (gbalandmarks.py)" % lm["title"], FG, Fb)
        label(d, (24, 48), "%s  |  footprint %dx%d at (%d,%d)%s  |  door (%d,%d)  |  row %d" % (
            GROUP["place"], lm["w"], lm["h"], lm["x0"], lm["y0"],
            "".join(" + %s %dx%d at (%d,%d)" % (l.replace("_Layout", ""), w, h, x, y)
                    for l, x, y, w, h, _, _ in lm.get("parts", ())), lm["door"][0], lm["door"][1], lm["row"]), DIM, F)
        y = 72
        for line in cap:
            label(d, (24, y), line, FG, Fs)
            y += 18
        y += 8
        for what, a, b in rows3:
            s.paste(up(a, 3), (24, y))
            s.paste(up(b, 3), (24 + a.width * 3 + 24, y))
            label(d, (24, y + a.height * 3 + 4), "TODAY (3x)%s" % what, DIM, F)
            label(d, (48 + a.width * 3, y + a.height * 3 + 4), "DRAFT (3x)%s" % what, GOLD, F)
            y += a.height * 3 + 34
        x = 24
        for i, im in enumerate(one):
            s.paste(im, (x, y))
            x += im.width + 12
        label(d, (24, y + t.height + 4), "at 1x: today | draft" + (" | today grey | draft grey" if ht else ""), DIM, Fs)
        y += t.height + 34
        x = 24
        for a, b in towns:
            s.paste(a, (x, y)); s.paste(b, (x + a.width + 16, y))
            x += (a.width + 16) * 2
        label(d, (24, y + tv.height + 6), "%s at 1x: today | draft%s" % (
            GROUP["town"], ("   ||   in grey: today | draft" if ht else "")), DIM, Fs)
        #  the door, beside the 3x pair
        xx, yy = 24 + t.width * 6 + 72, 80 + 18 * len(cap)
        for line in lm.get("door_note", []):
            label(d, (xx, yy), line, GOLD if line is lm["door_note"][0] else DIM, Fs)
            yy += 18
        if lm is CORPUS:                                    # the redrawn door's frames, as gbadoors will draw them
            frames, spec, off = corpus_door_preview(after["drawings"]["corpus_tower"])
            assert spec["kind"] == CORPUS_DOOR["kind"] and tuple(spec["leaf"]) == CORPUS_DOOR["leaf"] and off == 0, spec
            yy += 8
            for i, f in enumerate(frames):
                im = Image.new("RGB", (16, 16))
                im.putdata([c for line in f for c in line])
                s.paste(up(im, 5), (xx + i * 88, yy))
                label(d, (xx + i * 88, yy + 84), ("closed", "ajar", "half", "open")[i], DIM, Fs)
        p = os.path.join(out, "%s_%s.png" % (GROUP["tag"], lm["name"]))
        s.save(p)
        paths.append(p)
    # the tiles, the rows, the budget
    cut = after["cut"]
    n = len(cut.placed)
    cols = 16
    rowsp = [(lm["row"], after["pals"][lm["row"]], lm["title"]) for lm, _ in LANDMARKS_HERE]
    s = Image.new("RGB", (max(40 + cols * 40, 840), 130 + ((n + cols - 1) // cols) * 48 + 40 + len(rowsp) * 100), BG)
    d = ImageDraw.Draw(s)
    label(d, (24, 16), "T-447 pair 2 tiles -- secondary/%s" % GROUP["dir"], FG, F)
    for i, line in enumerate(after["budget"]):
        label(d, (24, 40 + i * 18), line, DIM, Fs)
    rowof = {}
    for entries in (p[4] for p in after["plan"]):
        for v in entries:
            if v & 0x3FF >= NUM_PRIMARY:
                rowof.setdefault((v & 0x3FF) - NUM_PRIMARY, (v >> 12) & 0xF)
    y0 = 40 + len(after["budget"]) * 18 + 12
    for i, (slot, key) in enumerate(cut.placed):
        pal = after["pals"].get(rowof.get(slot, rowsp[0][0]), rowsp[0][1])
        tim = Image.new("RGB", (8, 8))
        for j, v in enumerate(key):
            tim.putpixel((j % 8, j // 8), tuple(pal[v]) if v else (60, 60, 70))
        x, y = 24 + (i % cols) * 40, y0 + (i // cols) * 48
        s.paste(up(tim, 4), (x, y))
        label(d, (x, y + 33), str(slot), DIM, font(10))
    y = y0 + ((n + cols - 1) // cols) * 48 + 16
    for r, pal, title in rowsp:
        label(d, (24, y), "row %d -- %s" % (r, title), GOLD, F)
        names = ["0"] + [nm for nm, _ in next(lm for lm, _ in LANDMARKS_HERE if lm["row"] == r)["colours"]]
        for i, rgb in enumerate(pal):
            d.rectangle((24 + i * 40, y + 22, 24 + i * 40 + 34, y + 56), fill=tuple(rgb))
            label(d, (24 + i * 40, y + 60), names[i] if i < len(names) else "(left)", DIM, font(9))
        y += 100
    p = os.path.join(out, "%s_tiles_%s.png" % (GROUP["tag"], GROUP["dir"]))
    s.save(p)
    paths.append(p)
    return paths


# ============================================================================================ main
def run_group(g):
    use(g)
    gt = gbatowns_landmarks().get(g["dir"], [])
    if sorted(gt) != sorted(OWNS[g["dir"]]):
        raise SystemExit("  gbatowns.py's LANDMARKS and OWNS disagree for %s:\n    %s\n    %s" % (g["dir"], gt, OWNS[g["dir"]]))
    ts = Tileset(g["dir"], g["symbol"])
    before = dict(mt=bytes(ts.mt), tiles=ts.tiles.copy(), pals=dict(ts.pals))
    before_bd = {k: bytes(v["bd"]) for k, v in ts.maps.items()}
    print("  %s: %d layouts draw it (%s); %d blocks, %d tiles (-num_tiles)" % (
        g["symbol"], len(ts.layouts), ", ".join(l["name"].replace("_Layout", "") for l in ts.layouts),
        ts.nblocks, ts.num_tiles))
    ours = ours_of(LANDMARKS_HERE)
    rowsays = {lm["name"]: row_check(ts, lm, ours) for lm, _ in LANDMARKS_HERE}
    after = build(ts)
    cut = after["cut"]
    print("  census: %d cells examined across every layout and border" % after["examined"])
    print("  owned tiles (drawn only by our cells): %d; free slots %d..%d: %d; kept (doors, boards): %d"
          % (len(after["owned"]), ts.num_tiles, DOOR_TILE_START - 1, len(after["free"]), len(after["kept_tiles"])))
    for lm, _ in LANDMARKS_HERE:
        cells = [c for c in cells_of(lm) if not (c[0] == g["layout"] and (c[1], c[2]) in lm["keep"])]
        mine = [p for p in after["plan"] if (p[7], p[0], p[1]) in {c[:3] for c in cells}]
        print("  %-16s %d cells redrawn%s, %d kept %s; row %d (%s); %d new tiles" % (
            lm["title"], len(mine), " (+%d on its copies)" % sum(len(p[8]) for p in mine) if lm.get("mirrors") else "",
            len(lm["keep"]), lm["keep"], lm["row"], rowsays[lm["name"]], after["per"][lm["name"]]))
    room = len(after["owned"]) + len(after["free"])
    print("  drawn: %d unique tiles (flips shared) into %d slots; %s" % (
        len(cut.placed), room, "OVER BUDGET by %d" % cut.over if cut.over else "%d to spare" % (room - len(cut.placed))))
    used_blocks = sorted({ts.cell(l, x, y) & 0x3FF for (l, x, y) in ours})
    after["budget"] = [
        "tiles: %d drawn (flips shared) into %d owned%s slots -- %s" % (
            len(cut.placed), len(after["owned"]),
            " + %d free" % len(after["free"]) if after["free"] else
            " (free slots left to the KEEPALIVE PLANT)" if not GROUP.get("free_slots", True) else " (no free slot in the tileset)",
            "OVER by %d" % cut.over if cut.over else "%d to spare" % (room - len(cut.placed))),
        "blocks: %d distinct cells' blocks; tileset %d -> %d (of %d); -num_tiles %d -> %d" % (
            len(used_blocks), after["old_nblocks"], after["nblocks"], SECONDARY_METATILES, ts.num_tiles,
            after["num_tiles"]),
        "rows: " + "; ".join("%d (%s, %d colours)" % (lm["row"], rowsays[lm["name"]], len(lm["colours"]))
                              for lm, _ in LANDMARKS_HERE),
    ]
    for line in after["budget"][1:]:
        print("  " + line)
    if cut.over:
        print("  !! the drawings need %d more tiles than the landmarks own: previewed, never written" % cut.over)
        if WRITE:
            raise SystemExit("  not written")
    after_view = dict(mt=after["mt"], tiles=after["tiles"], pals=after["pals"], cut=cut, owned=after["owned"],
                      free=after["free"], plan=after["plan"], drawings=after["drawings"], budget=after["budget"])
    changed = [k for k, v in ts.maps.items() if bytes(v["bd"]) != before_bd[k]]
    if DRAFT is not None:
        tsd = os.path.join(DRAFT, g["dir"])
        os.makedirs(os.path.join(tsd, "palettes"), exist_ok=True)
        after["tiles"].save(os.path.join(tsd, "tiles.png"))
        open(os.path.join(tsd, "metatiles.bin"), "wb").write(after["mt"])
        open(os.path.join(tsd, "metatile_attributes.bin"), "wb").write(after["at"])
        open(os.path.join(tsd, "map.bin"), "wb").write(ts.maps[g["layout"]]["bd"])
        for k in changed:
            if k != g["layout"]:
                open(os.path.join(tsd, "%s.map.bin" % k.replace("_Layout", "")), "wb").write(ts.maps[k]["bd"])
        for lm, _ in LANDMARKS_HERE:
            write_pal(os.path.join(tsd, "palettes", "%02d.pal" % lm["row"]), row_pal(ts, lm))
            d = os.path.join(DRAFT, lm["name"])
            os.makedirs(d, exist_ok=True)
            k = after["drawings"][lm["name"]]
            im = drawing_rgb(k, lm["colours"])
            im.save(os.path.join(d, "drawing_1x.png"))
            up(im, 3).save(os.path.join(d, "drawing_3x.png"))
            mine = {c[:3] for c in cells_of(lm)}
            cells = []
            for p in after["plan"]:
                if (p[7], p[0], p[1]) not in mine:
                    continue
                c = dict(cell=[p[0], p[1]], was=p[3], layer_type=(struct.unpack("<I", p[5])[0] >> 29) & 3
                         if p[5] else None)
                if p[7] != g["layout"]:
                    c["layout"] = p[7]
                cells.append(c)
            json.dump(dict(title=lm["title"], map=lm["map"], footprint=[lm["x0"], lm["y0"], lm["w"], lm["h"]],
                           door=lm["door"], kept=lm["keep"], signs=lm["signs"], row=lm["row"],
                           colours={n: "%02x%02x%02x" % c for n, c in lm["colours"]}, cells=cells),
                      open(os.path.join(d, "cells.json"), "w"), indent=1)
        json.dump(dict(tileset=g["symbol"], tiles_drawn=len(cut.placed), owned=after["owned"], free=after["free"],
                       slots_used=[s for s, _ in cut.placed], blocks=[after["old_nblocks"], after["nblocks"]],
                       num_tiles=[ts.num_tiles, after["num_tiles"]]), open(os.path.join(tsd, "budget.json"), "w"), indent=1)
        print("  draft: %s (tileset) and %s" % (os.path.relpath(tsd, ROOT),
                                               ", ".join(os.path.relpath(os.path.join(DRAFT, lm["name"]), ROOT)
                                                         for lm, _ in LANDMARKS_HERE)))
        if SHEETS:
            #  today is rendered from the untouched maps, the draft from the repointed ones
            before_maps = {k: dict(v, bd=bytearray(before_bd[k])) for k, v in ts.maps.items()}
            if g["dir"] == "cinnabar_island":
                paths = sheets_two(ts, before_maps, before, after_view, SHEETS)
            else:
                paths = sheets_pair2(ts, before_maps, before, after_view, SHEETS)
            for p in paths:
                print("  sheet: %s" % p)
    if WRITE:
        names = [lm["name"] for lm, _ in LANDMARKS_HERE]
        ok = [n for n in names if n in APPROVED]
        if not ok:
            print("  not written: %s %s a draft (not in APPROVED)" % (", ".join(names), "is" if len(names) == 1 else "are"))
            return
        if len(ok) != len(names):
            raise SystemExit("  not written: approved %s of %s -- a tileset's landmarks are written together"
                             % (sorted(ok), names))
        tsd = ts.dir
        after["tiles"].save(os.path.join(tsd, "tiles.png"))
        open(os.path.join(tsd, "metatiles.bin"), "wb").write(after["mt"])
        open(os.path.join(tsd, "metatile_attributes.bin"), "wb").write(after["at"])
        for k in set(changed) | {g["layout"]}:
            m = ts.maps[k]
            open(os.path.join(GBA, m["path"]), "wb").write(m["bd"])
        for lm, _ in LANDMARKS_HERE:
            write_pal(os.path.join(tsd, "palettes", "%02d.pal" % lm["row"]), row_pal(ts, lm))
        rules = open(RULES).read()
        new, n = re.subn(r"(secondary/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+" % g["dir"],
                         lambda mm: mm.group(1) + str(after["num_tiles"]), rules)
        assert n == 1
        open(RULES, "w").write(new)
        print("  written: tiles.png, metatiles.bin, metatile_attributes.bin, rows %s, %s, -num_tiles %d" % (
            ", ".join(str(lm["row"]) for lm, _ in LANDMARKS_HERE),
            ", ".join(sorted(set(changed) | {g["layout"]})), after["num_tiles"]))


def main():
    if WRITE and not APPROVED_FLAG:
        raise SystemExit("  --write refuses without --approved: T-447's landmarks are drafts until the user says yes")
    only = argval("--only")
    for g in GROUPS:
        if only and only != g["dir"]:
            continue
        print("%s (secondary/%s)" % (g["town"], g["dir"]))
        run_group(g)


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
