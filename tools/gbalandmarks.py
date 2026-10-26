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

THE THIRD PAIR (drafted 2026-10-25, NOT approved): the REVIEW BOARD (UMBRA, rows 7 and 8 -- its stone, and its four
vessels in seat order I-IV, red, yellow, black, pale, the user's choice; a landmark may now draw in more than one row,
each tile in the one row that holds its colours, see assign_row) and ERRATA with its annex (SLATE, row 12; the roof a
writing slate in its frame, replacing batch F's calm roof; the pediment's struck line and red caret; columns of stacked
dead hardware; the annex a pinned index card). Both doors that animate are kept by block (the Board's is primary
0x15B, the annex's METATILE_PewterCity_Door), so gbadoors has nothing to redraw. Both groups take their cells' bottom
layer from the grass (ground_always: vanilla drew both halls into both layers); SLATE's census leaves out
RS_BattleTower, a layout no map uses (skip_unused_layouts), as gbatowns' counts do.

  TWEAKED (the user, 2026-10-25: "build with tweaks"): the REVIEW BOARD's pale semicircle porch, (10..12, 7) and its
  lip on (10..12, 8), redrawn in the hall's dark stone so the kept blue door sits in black -- six cells added to the
  footprint (and to gbatowns' LANDMARKS), attributes and collision kept, their own bottom layer kept (keep_bottom);
  four faint seat places inlaid along the bench top over the four vessels. ERRATA's erratum moved up onto the slate
  roof, where it reads at 1x (the struck line on the lowest rule, the red caret standing in it, the correction's mark
  over it), with an echo on the pediment (one struck rule and a small caret, mirrored on its seam: one tile). To fit
  SLATE's 123 slots, the slate's smear of what was rubbed out is cut and the pediment's written line goes.

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
APPROVED = {"scorn_solutions", "mansion",           # the user, 2026-10-24: "build it" (second draft, e559d4eb)
            "corpus_tower", "daemon_tower",          # the user, 2026-10-25: "build both" (pair 2 with depth, a219855f)
            "review_board", "errata"}                # the user, 2026-10-25: "build pair 3" (tweaked 9283f477, chalk scrambled)

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


# ============================================================================================ pair 3: more than one row
#  A landmark may draw in more than one palette row (the REVIEW BOARD: its stone in row 7, its four vessels in row 8).
#  Its canvas names every role once; each 8x8 tile is then given the one row that holds every colour it uses, matched
#  by RGB -- so a colour two rows share (the stone round a vessel) is written into both with the same RGB. A tile no
#  single row can draw refuses. A landmark with one row is cut exactly as before.
def lm_rows(lm):
    """[(row, colours)]: the landmark's own row, then its extra rows"""
    return [(lm["row"], lm["colours"])] + list(lm.get("extra_rows", ()))


def lm_roles(lm):
    """role -> canvas index: row n's colours at 16n+1.. (a role an earlier row already names keeps that index)"""
    roles = role_map(lm["colours"])
    for i, (_, cols) in enumerate(lm.get("extra_rows", ())):
        for j, (name, _) in enumerate(cols):
            roles.setdefault(name, 16 * (i + 1) + j + 1)
    return roles


def lm_rgb(lm):
    """canvas index -> RGB, every row's"""
    return {16 * i + j + 1: rgb for i, (_, cols) in enumerate(lm_rows(lm)) for j, (_, rgb) in enumerate(cols)}


def assign_row(lm, key):
    """(the tile's pixels in its row's own indices, the row) -- the first row holding every colour the tile uses"""
    if not lm.get("extra_rows"):
        return key, lm["row"]
    rgb = lm_rgb(lm)
    want = {rgb[v] for v in key if v}
    for row, cols in lm_rows(lm):
        idx = {c: j + 1 for j, (_, c) in enumerate(cols)}
        if want <= set(idx):
            return tuple(idx[rgb[v]] if v else 0 for v in key), row
    raise SystemExit("  %s: a tile no one row can draw: %s" % (lm["title"], sorted(want)))


# ============================================================================================ the REVIEW BOARD
#  UMBRA, IndigoPlateau_Exterior 11x7 at (6,0), door (11,6). Section 6: four members, each a humour, each humour a
#  coloured fluid -- and 8.6: the one place colour is real, by contrast with darkness. So the hall is near-black stone,
#  neutral to the last pixel, under one long flat slab that overhangs it like a judges' bench; and in its front, in
#  four lit alcoves, four vessels of fluid -- red, yellow, black, pale -- in SEAT ORDER, I to IV left to right (the
#  user, 2026-10-25), each under a carved plate with its numeral. Not meeting order (IV, II, III, I): nobody remarks on
#  it. Their colour spills a little onto each alcove's sill, and nowhere else.
#  3/4: the slab is a deck seen from above (the map's top edge cuts its back) with a thick lit front edge and chamfered
#  corners; the hall under it is INSET -- a chamfered box, its left chamfer lit and its right in shade, the plateau's
#  grass showing at its sides and under the slab's overhang (cells (6,6) and (16,6) were always walkable ground).
#  THE DOOR (11,6) is METATILE_General_SlidingDoubleDoor (0x15B), a PRIMARY block every sliding door in the game draws:
#  it is kept exactly, and the portal is drawn round it.
RB_ROW, RB_ROW2 = 7, 8
RB_COLOURS = [  # row 7 (unused): the stone, all neutral -- a hint of blue in the darks, nothing else
    ("OUT",    (14, 12, 18)),      # outline; the cast shadow's core
    ("NICHE",  (24, 22, 30)),      # shadow: under the slab, inside the portal
    ("STONED", (34, 32, 40)),      # the shaded chamfer; joints
    ("STONE",  (46, 44, 54)),      # the hall's front face
    ("STONEM", (60, 58, 68)),      # the lit chamfer; the plinth
    ("STONEL", (78, 76, 88)),      # an alcove's lit back
    ("DECKD",  (52, 50, 60)),      # the slab's moulding groove
    ("DECK",   (64, 62, 74)),      # the slab, seen from above
    ("DECKL",  (80, 78, 92)),      # its sheen
    ("LIP",    (112, 110, 124)),   # the slab's lit front lip
    ("EDGE",   (90, 88, 102)),     # the slab's front edge
    ("CARVE",  (138, 136, 152)),   # the numerals, cut into each plate
]
RB_VESSEL_COLOURS = [  # row 8 (unused): the four humours, the glass, and the stone round them (the same RGB as row 7)
    ("OUT",    (14, 12, 18)),
    ("STONED", (34, 32, 40)),
    ("STONE",  (46, 44, 54)),
    ("STONEM", (60, 58, 68)),
    ("STONEL", (78, 76, 88)),
    ("GLASSL", (214, 220, 230)),   # the glass's glint
    ("GLASS",  (128, 134, 148)),   # the glass
    ("RED",    (192, 28, 36)),     # I    sanguine: blood
    ("REDL",   (238, 96, 84)),
    ("YEL",    (222, 178, 30)),    # II   choleric: yellow bile
    ("YELL",   (252, 230, 112)),
    ("BLK",    (6, 4, 8)),         # III  melancholic: black bile -- blacker than the hall
    ("BLKL",   (66, 46, 78)),      #      its sheen
    ("PALE",   (218, 220, 206)),   # IV   phlegmatic: phlegm, pale
    ("PALEL",  (250, 250, 242)),
]
RB_SEATS = ((40, "RED", "REDL", "I"), (64, "YEL", "YELL", "II"),       # (centre: a tile seam, fluid, its light, numeral)
            (112, "BLK", "BLKL", "III"), (136, "PALE", "PALEL", "IV"))
RB_SLAB = (4, 171, -40, 40, 50)          # the slab: (xa, xb, its back -- off the map -- the front edge's top, its foot)
RB_HALL = (16, 159, 50, 111)             # the hall under it: x, x, its top (in the slab's shadow), its foot
#  THE PORCH (the user, 2026-10-25): vanilla's pale semicircle in front of the door, cells (10..12, 7) and the lip
#  that runs onto (10..12, 8), redrawn in the hall's dark stone so the kept blue door sits in black. These six cells
#  are outside the 11x7 box: they join the footprint (gbatowns' LANDMARKS has them too), keep their attributes and
#  collision, and keep their own bottom layer (the grass, and on row 8 the path) -- vanilla drew the porch in the top
#  layer only, and so does this.
RB_PORCH = {(x, y) for x in (10, 11, 12) for y in (7, 8)}
RB_PORCH_DISC = (87.5, 111.5, 24.0, 20.5)  # its centre (on the door's axis, at the hall's foot), rx, ry
RB = dict(name="review_board", title="the REVIEW BOARD", map="IndigoPlateau_Exterior", x0=6, y0=0, w=11, h=7,
          door=(11, 6), keep=[(11, 6)], inplace=[], signs=[], row=RB_ROW, colours=RB_COLOURS,
          extra_rows=[(RB_ROW2, RB_VESSEL_COLOURS)],
          cells_only={(x, y) for x in range(6, 17) for y in range(7)} | RB_PORCH,
          #  every cell's bottom layer is the plateau's grass (vanilla drew the hall into both layers), so the inset
          #  shows ground; the art is the top layer. The porch keeps its own bottom layer.
          ground=lambda x, y: 0x001, ground_always=True, keep_bottom=RB_PORCH,
          crop=[("IndigoPlateau_Exterior_Layout", 5, 0, 13, 9)],
          caption=["Near-black stone, neutral to the last pixel, under one long flat slab that overhangs the hall like "
                   "a judges' bench: the slab a deck seen from above, its thick lit edge chamfered at the corners.",
                   "The hall is inset under it -- left chamfer lit, right in shade -- and the plateau's grass shows at "
                   "its sides and under the overhang (cells (6,6) and (16,6) were always walkable).",
                   "The only colour on UMBRA: four vessels of fluid in four lit alcoves, red, yellow, black, pale, in "
                   "SEAT order I-IV left to right (not meeting order), each under a plate cut with its numeral.",
                   "Their colour spills a little onto each sill and nowhere else. The black is blacker than the hall.",
                   "Tweaked (2026-10-25): four faint seat places inlaid along the bench top over the four vessels; the "
                   "pale porch redrawn in dark stone, so the kept blue door sits in black."],
          door_note=["THE DOOR (11,6): KEPT. It is 0x15B, the PRIMARY",
                     "sliding double door every such door in the game",
                     "draws, so it cannot be redrawn in place here;",
                     "the portal is drawn round it. No frames change."])


def draw_review_board():
    W, H = 176, 144                                              # the 11x7 box, and the porch's two rows below it
    k = Canvas(W, H, lm_roles(RB))
    # --- the hall: a chamfered box, inset under the slab; its chamfers' feet rise, so the grass shows below them
    hx0, hx1, htop, hbot = RB_HALL
    for x in range(hx0, hx1 + 1):
        L, side = lean(x, hx0, hx1), side_of(x, hx0, hx1)
        for yf in range(htop, hbot + 1):
            y = yf - L
            joint = (yf - 58) % 12 == 11 or (yf >= 58 and (x + (12 if (yf - 58) // 12 % 2 else 0)) % 24 == 0
                                              and side == "front")
            if side == "lit":
                role = "STONE" if joint else "STONEM"
            elif side == "shade":
                role = "NICHE" if joint else "STONED"
            else:
                role = "STONED" if joint else "STONE"
            if yf >= 105:                                       # the plinth
                role = {"lit": "STONEL", "shade": "STONE", "front": "STONEM"}[side] if yf == 105 else \
                    {"lit": "STONEM", "shade": "STONED", "front": "STONE"}[side]
            k.px(x, y, role)
        k.px(x, hbot - L, "OUT")
    for y in range(htop, hbot + 1):                              # the corners: lit where the lit chamfer meets the front
        k.px(hx0 + CHAMFER - 1, y, "STONEL" if y < 105 else "STONEM")
        k.px(hx1 - CHAMFER + 1, y, "NICHE")
    hall = {(x, y) for x in range(hx0, hx1 + 1) for y in range(htop - lean(x, hx0, hx1), hbot - lean(x, hx0, hx1) + 1)}
    outline(k, hall)

    # --- the four plates, the four alcoves, the four vessels: I-IV, seat order, left to right
    for c, fluid, light, num in RB_SEATS:
        # the plate, cut with the numeral
        k.rect(c - 6, 56, c + 5, 62, "STONED")
        k.hline(c - 6, c + 5, 62, "STONEM")
        n = {"I": [0], "II": [-1, 1], "III": [-2, 0, 2], "IV": [-3]}[num]
        for dx in n:
            k.vline(c - 1 + dx, 57, 61, "CARVE")
        if num == "IV":                                          # the V: two arms meeting at its foot
            for yy, dxs in ((57, (-1, 3)), (58, (-1, 3)), (59, (0, 2)), (60, (0, 2)), (61, (1,))):
                for dx in dxs:
                    k.px(c - 1 + dx, yy, "CARVE")
        # the alcove: a round-headed recess, its back lit, its head in shadow
        for y in range(64, 104):
            for x in range(c - 7, c + 7):
                arch = y < 67 and (x - (c - 0.5)) ** 2 + ((67 - y) * 2.2) ** 2 > 7.5 ** 2
                if arch:
                    continue
                edge = x in (c - 7, c + 6) or y == 64 or (y < 67 and not ((x - (c - 0.5)) ** 2 + ((66 - y) * 2.2) ** 2
                                                                              <= 7.5 ** 2))
                k.px(x, y, "OUT" if edge else "STONED" if y < 68 or x == c + 5 else "STONEL")
        # the sill: lit, and the vessel's colour spilt on it
        k.hline(c - 7, c + 6, 104, "STONEM")
        k.hline(c - 6, c + 5, 103, "STONEM")
        for x in range(c - 6, c + 6):
            if (x + c) % 2 == 0 or abs(x - c + 0.5) < 3:
                k.px(x, 103, light if abs(x - c + 0.5) < 2 else fluid)
            if abs(x - c + 0.5) < 4 and x % 2 == 0:
                k.px(x, 104, fluid)
        # the vessel: a stoppered glass cylinder, filled to the same mark as the others
        body = {}
        for y in range(66, 103):
            if y <= 67:
                half = 2                                         # the stopper
            elif y <= 71:
                half = 2                                         # the neck
            elif y == 72:
                half = 4                                         # the shoulder
            elif y <= 100:
                half = 5
            else:
                half = 4                                         # the foot
            for x in range(c - half, c + half):
                body[(x, y)] = True
        for (x, y) in body:
            inside = all((x + dx, y + dy) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if y <= 67:
                k.px(x, y, "STONED" if y == 67 else "GLASS")    # the stopper
            elif not inside:
                k.px(x, y, "GLASS")
            elif y >= 79:                                        # the fluid; a lit column, a meniscus
                k.px(x, y, light if (y == 79 or x in (c - 4, c - 3)) else fluid)
            else:
                k.px(x, y, "STONEL")                             # empty glass: the alcove seen through it
        k.vline(c - 3, 73, 77, "GLASSL")                         # the glint down the glass
        k.px(c - 3, 69, "GLASSL")
        k.vline(c + 3, 82, 97, "GLASS")                          # the glass's far wall, over the fluid
        k.hline(c - 4, c + 3, 101, "OUT")                        # its foot on the sill
        k.hline(c - 3, c + 2, 102, "OUT")

    # --- the portal round the kept door: two pilasters, a dark recess up to the slab's shadow, a lit lintel
    k.rect(76, 58, 99, 111, "NICHE")
    for x0 in (76, 96):
        k.rect(x0, 58, x0 + 3, 111, "STONEM")
        k.vline(x0, 58, 111, "STONEL")
        k.vline(x0 + 3, 58, 111, "STONED")
    k.hline(76, 99, 58, "LIP")
    k.hline(76, 99, 59, "EDGE")
    k.rect(80, 60, 95, 63, "OUT")                                # the recess's head, in full shadow
    k.hline(84, 91, 70, "STONED")                                # a blank transom: nothing is written over the door
    k.hline(84, 91, 82, "STONED")

    # --- the slab, last: a bench of stone over all of it. The deck seen from above, a groove along its front, its
    #  thick front edge lit on top, its chamfers lit on the left and shaded on the right; its shadow on the hall.
    xa, xb, back, top, bot = RB_SLAB
    m = box_mask(xa, xb, back, top, bot)
    for x in range(xa, xb + 1):                                  # the shadow it casts across the hall's head
        L = lean(x, hx0, hx1) if hx0 <= x <= hx1 else 0
        for y in range(bot - lean(x, xa, xb) + 1, bot - lean(x, xa, xb) + 5):
            if (x, y) in hall:
                k.px(x, y, "NICHE" if y < bot - lean(x, xa, xb) + 3 else k.get(x, y))
    for (x, y), part in m.items():
        L = lean(x, xa, xb)
        if part == "deck":
            d = top - L - y                                      # rows behind the front lip
            k.px(x, y, "LIP" if d == 1 else "DECKD" if d == 6 else "DECKL" if d in (5, 7) else "DECK")
        else:
            yf = y + L
            side = side_of(x, xa, xb)
            r = yf - top
            role = "LIP" if r == 0 else "OUT" if yf == bot else "EDGE" if r < 6 else "STONEM"
            if side == "lit" and role in ("EDGE", "STONEM"):
                role = "LIP" if role == "EDGE" else "EDGE"
            elif side == "shade" and role in ("EDGE", "STONEM", "LIP"):
                role = {"LIP": "EDGE", "EDGE": "STONEM", "STONEM": "STONE"}[role]
            k.px(x, y, role)
    for x in range(xa + 1, xb):
        k.px(x, top - lean(x, xa, xb), "LIP")
    outline(k, m)
    #  the four seat places, inlaid in the bench top over the four vessels: faint, a recess one step darker at its back
    #  and left, one step lighter at its front and right (the light from the upper left). Each is centred on its seat's
    #  tile seam, all four alike, on one tile row.
    for c, _, _, _ in RB_SEATS:
        x0, x1, y0, y1 = c - 6, c + 5, 25, 30
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x in (x0, x1)) and (y in (y0, y1)):
                    continue                                     # rounded corners
                if y == y0 or x == x0:
                    k.px(x, y, "DECKD")
                elif y == y1 or x == x1:
                    k.px(x, y, "DECKL")
    draw_rb_porch(k)
    return k


def draw_rb_porch(k):
    """the porch: vanilla's semicircle, in the hall's stone -- a dark step, its tread lit, and within it a disc of
    shadow that runs on from the portal, so the kept blue door stands in black"""
    cx, cy, rx, ry = RB_PORCH_DISC
    for y in range(112, 144):
        for x in range(64, 112):
            r = (((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2) ** 0.5
            if r > 1:
                continue
            if r > 0.92:
                role = "OUT"                                     # its edge on the grass
            elif r > 0.82:
                role = "STONED"                                  # the step's riser
            elif r > 0.77:
                role = "EDGE" if x < cx else "STONEL"            # the tread's lit nosing
            elif r > 0.64:
                role = "STONEL" if x < cx else "STONEM"          # the tread
            elif r > 0.60:
                role = "STONED"
            else:
                role = "NICHE"                                   # the black the door stands in
            k.px(x, y, role)


# ============================================================================================ ERRATA
#  SLATE, PewterCity 16x7 at (12,0): the museum (11x6 and its porch) and the annex (5x4, door (25,4)). 4.32: the
#  museum of dead hardware renamed for what a printed edition got wrong -- a legacy mind, still running the faults it
#  shipped with. So the building is a SLATE:
#    * the roof is a writing slate laid flat in its timber frame, seen from above: ruled in chalk, and wiped clean --
#      SLATE's own phrase, a clean slate -- with only the smears of what was rubbed out;
#    * the porch's pediment carries the one line still written, struck through, and a red caret above it where the
#      correction goes in (the erratum: the only red on the building);
#    * the columns are stacked dead hardware -- cases, drives, cartridges, keyboards, chips -- in strata, like
#      fossils, three stacks and their mirrors, between them the museum's glass dark as slate with a chalk glint;
#    * the annex is one big index card pinned to its roof: a red header rule, faint blue rules, a heading and two lines
#      of dashes (the card's form, KNOWN FAULTS, without a word on it), the pin, a dog-eared corner.
#  BATCH F's ROOF IS REPLACED, not built on: its calm slates were a retint of vanilla's pitched roof, and the design
#  needs the roof to be the slate itself.
#  3/4: the slate's frame has a front edge and chamfered corners; the hall under it and the annex are chamfered boxes,
#  inset, the grass showing between them and at their sides. Both doors keep their blocks: the museum's (17,6) is a
#  plain doorway (MB 0x60, no animation), drawn as the MANSION's; the annex's (25,4) is METATILE_PewterCity_Door,
#  animated from its closed block, KEPT exactly, so gbadoors has nothing to redraw.
ERRATA_ROW = 12
ERRATA_COLOURS = [  # row 12 (unused, all black)
    ("OUT",    (30, 32, 42)),      # outline; inside the doorway
    ("SLATED", (46, 54, 66)),      # the slate in shadow; the museum's dark glass
    ("SLATE",  (62, 72, 86)),      # the slate
    ("SLATEL", (88, 102, 118)),    # a slate's lit edge; the card's faint blue rules
    ("CHALKD", (132, 142, 152)),   # chalk rules; a wiped smear
    ("CHALK",  (236, 236, 226)),   # chalk; the card
    ("PAPERD", (196, 194, 180)),   # the card's shade and edge; the annex walls' shade
    ("WOODD",  (92, 62, 42)),      # the frame, in shade
    ("WOOD",   (138, 96, 60)),     # the frame
    ("WOODL",  (184, 138, 90)),    # the frame, lit
    ("RED",    (204, 40, 44)),     # the caret, the card's header rule, the pin. Corrections are red.
    ("BEIGED", (128, 120, 102)),   # dead plastic, in shade
    ("BEIGE",  (176, 168, 144)),   # dead plastic
    ("BEIGEL", (214, 208, 186)),   # dead plastic, lit; the architrave
    ("PLATE",  (154, 162, 174)),   # the slate city's stone: the stylobate, the pediment's cornice
]
ERRATA = dict(name="errata", title="ERRATA (the museum and its annex)", map="PewterCity", x0=12, y0=0, w=16, h=7,
              door=(17, 6), keep=[(25, 4)], inplace=[], signs=[], row=ERRATA_ROW, colours=ERRATA_COLOURS,
              cells_only={(x, y) for x in range(12, 23) for y in range(6)} | {(16, 6), (17, 6), (18, 6)}
              | {(x, y) for x in range(23, 28) for y in range(1, 5)},
              ground=lambda x, y: 0x001, ground_always=True,
              lintel=lambda k, x, y: not (82 <= x <= 93 and y >= 96),
              crop=[("PewterCity_Layout", 11, 0, 18, 8)],
              caption=["The museum as a SLATE: its roof a writing slate laid flat in a timber frame, seen from above, "
                       "ruled in chalk and wiped clean -- a clean slate -- with only the smear of what was rubbed out.",
                       "The porch's pediment keeps the one line still written: struck through, and a red caret above "
                       "it where the correction goes in. The building's only red is the erratum's (and the card's).",
                       "The columns are stacked dead hardware -- cases, drives, cartridges, keyboards, chips -- in "
                       "strata like fossils; between them the museum's glass, dark as slate, a chalk glint on each.",
                       "The annex is one big index card pinned to its roof: red header rule, faint blue rules, a "
                       "heading and two lines of dashes (KNOWN FAULTS, without a word), the pin, a dog-eared corner.",
                       "Batch F's calm roof is REPLACED, not built on. 3/4: both are chamfered boxes, inset; the grass "
                       "shows between them and at their sides."],
              door_note=["THE DOORS: (17,6) a plain doorway (MB 0x60, no",
                         "animation), drawn as the MANSION's -- its dark",
                         "below, the porch above the player. (25,4) the",
                         "annex's animated door, METATILE_PewterCity_Door,",
                         "KEPT exactly: gbadoors has nothing to redraw."])
ERRATA_SLATE = (2, 173, 2, 46, 52)       # the slate in its frame: (xa, xb, the back, the front edge's top, its foot)
ERRATA_HALL = (8, 167, 52, 95)
ERRATA_ANNEX = (180, 251, 20, 56, 79)    # the card on the annex: (xa, xb, the card's back, the wall's top, its foot)
ERRATA_COLS = ((16, "A", False), (32, "B", False), (48, "A", True),
               (120, "A", False), (136, "B", True), (152, "A", True))


#  the erratum on the slate: the words' letter counts (0 is the caret's gap), and the caret's centre (a tile seam, on the
#  door's axis); the line is laid out round the caret
ERRATA_ECHO = True             # the pediment's small echo of the erratum: it costs one tile, and fits
ERRATA_LINE = dict(words=(3, 2, 0, 4, 2), caret=88)
ERRATA_GLYPHS = ("n", "o", "l", "u", "n", "c", "o", "h", "u", "l")   # the marks' widths: 3 (an "l" 1) -- the layout only
#  the chalk itself is a scrawl, not shapes (the user, 2026-10-25: "scramble ERRATA's chalk line so no word can be picked
#  out (at 3x it read 'why'), same tiles"): each word's span keeps its place and width, so the same cells hold chalk,
#  and is drawn as one pen path whose height per column (0 the x-height's top .. 3 the rule) follows this sequence --
#  steps of at most two, no repeat of a glyph's outline, joined column to column so it reads as a hand, never a letter
ERRATA_SCRAWL = (2, 1, 3, 2, 0, 1, 3, 3, 1, 2, 0, 2, 3, 1, 1, 2, 3, 2, 0, 1, 2, 3, 1, 0, 2, 3, 2, 1, 3, 2, 0, 2)
ERRATA_TICKS = (5, 17, 26)     # columns of the line where the pen lifts a stroke above the x-height (one pixel)


def errata_line(k, spec, base):
    """the struck line: chalk shapes sitting on the rule under `base` (x-height base-3..base, ascenders base-4), word
    gaps 5px, the caret's gap 11px; one chalk strike through the middle, past both ends; the caret in red standing in
    its gap, the correction's mark over it"""
    marks, x, g, gap = [], 0, 0, None
    for n in spec["words"]:
        if n == 0:
            gap = x + 2                                          # the gap's centre seam, relative
            x += 4                                               # (with the word gaps either side: 12px clear)
            continue
        for _ in range(n):
            gl = ERRATA_GLYPHS[g % len(ERRATA_GLYPHS)]
            g += 1
            marks.append((x, gl))
            x += 2 if gl == "l" else 4
        x += 4
    width = x - 4
    ox = spec["caret"] - gap                                     # lay the line out round the caret
    words, w0, prev = [], None, None                             # each word's span, from its marks
    for mx, gl in marks:
        end = mx + (1 if gl == "l" else 3)
        if w0 is None or mx - prev > 1:
            if w0 is not None:
                words.append((w0, prev))
            w0 = mx
        prev = end
    words.append((w0, prev))
    col = 0
    for a, b in words:                                           # the scrawl: one pen path a word
        last = None
        for x in range(a, b):
            y = ERRATA_SCRAWL[col % len(ERRATA_SCRAWL)]
            if col in ERRATA_TICKS:
                k.px(ox + x, base - 4, "CHALK")
            col += 1
            lo, hi = (y, y) if last is None else (min(y, last), max(y, last))
            for yy in range(lo, hi + 1):
                k.px(ox + x, base - 3 + yy, "CHALK")
            last = y
    k.hline(ox - 3, ox + width + 2, base - 2, "CHALK")          # STRUCK THROUGH, past both ends
    c = spec["caret"]                                            # the caret, on a tile seam: its halves mirror
    for i in range(4):
        for dy in (0, 1):
            k.px(c - 1 - i, base - 5 + i + dy, "RED")
            k.px(c + i, base - 5 + i + dy, "RED")
    #  the correction, in chalk over the caret: a short mark, not struck
    for dx, dy in ((-4, 0), (-3, -1), (-2, 0), (-1, -1), (0, 0), (1, -1), (2, 0), (3, -1)):
        k.px(c + dx, base - 8 + dy, "CHALK")
    return ox, ox + width


def errata_stack(k, x0, y0, y1, kind, flip):
    """one column of dead hardware, 8 wide, from y0 down to y1: boxes stacked in strata, each box's top a lit line
    (seen from a little above), its left edge lit and its right in shade -- mirrored when `flip`"""
    stacks = {  # bottom to top: (height, body, detail)
        "A": [(12, "case"), (4, "floppy"), (7, "cart"), (4, "keys"), (5, "chip")],
        "B": [(10, "crt"), (5, "modem"), (6, "tape"), (3, "disk"), (3, "disk"), (5, "keys")],
        "C": [(8, "drive"), (6, "cart"), (4, "floppy"), (8, "case"), (6, "chip")],
        "D": [(12, "case"), (6, "tape"), (8, "crt"), (4, "floppy"), (6, "cart"), (5, "keys")],
        "E": [(8, "crt")],
    }[kind]
    canvas = {}
    y = y1
    for i, (h, what) in enumerate(stacks):
        if y - h + 1 < y0:
            break
        top = y - h + 1
        inset = 1 if what in ("cart", "tape", "disk", "chip") else 0   # the smaller things sit inside the column line
        for yy in range(top, y + 1):
            for xx in range(inset, 8 - inset):
                r = "BEIGE"
                if yy == top:
                    r = "BEIGEL"                                 # its top, seen from a little above
                elif xx == inset:
                    r = "BEIGEL" if what != "crt" else "BEIGE"
                elif xx == 7 - inset:
                    r = "BEIGED"
                canvas[(xx, yy)] = r
        mid = (top + y) // 2
        if what == "case":
            for xx in range(2, 6):
                canvas[(xx, top + 3)] = "OUT"                    # a drive bay
                canvas[(xx, top + 6)] = "BEIGED"
            canvas[(5, y - 2)] = "OUT"                           # the dead power light
        elif what == "floppy":
            for xx in range(1, 7):
                canvas[(xx, mid + 1)] = "OUT"
        elif what == "cart":
            for xx in range(2, 6):
                canvas[(xx, top + 2)] = "BEIGEL"                 # its label
                canvas[(xx, top + 3)] = "CHALKD"
            canvas[(1, y)] = "BEIGED"; canvas[(6, y)] = "BEIGED"
        elif what == "keys":
            for xx in range(1, 7, 2):
                canvas[(xx, top + 2)] = "BEIGED"
        elif what == "chip":
            for xx in range(1, 7):
                canvas[(xx, mid)] = "OUT"
                canvas[(xx, mid - 1)] = "OUT"
            for xx in (1, 3, 5):
                canvas[(xx, y)] = "PLATE"                        # its legs
        elif what == "crt":
            for yy in range(top + 2, y - 1):
                for xx in range(1, 6):
                    canvas[(xx, yy)] = "SLATED"                  # the dead screen, slate-dark
            canvas[(2, top + 3)] = "CHALKD"
        elif what == "modem":
            canvas[(2, mid)] = "OUT"; canvas[(4, mid)] = "OUT"
        elif what == "tape":
            canvas[(2, mid)] = "OUT"; canvas[(5, mid)] = "OUT"
            canvas[(3, mid)] = "BEIGED"; canvas[(4, mid)] = "BEIGED"
        elif what == "disk":
            canvas[(3, top + 1)] = "BEIGED"
        y = top - 1
    for (xx, yy), r in canvas.items():
        k.px(x0 + (7 - xx if flip else xx), yy, r)


def draw_errata():
    W, H = 256, 112
    k = Canvas(W, H, role_map(ERRATA_COLOURS))
    # --- the hall: a chamfered box under the slate; dark glass between the columns, the slate city's stone below
    hx0, hx1, htop, hbot = ERRATA_HALL
    hall = set()
    for x in range(hx0, hx1 + 1):
        L, side = lean(x, hx0, hx1), side_of(x, hx0, hx1)
        for yf in range(htop, hbot + 1):
            y = yf - L
            hall.add((x, y))
            if yf <= 57:
                role = "BEIGEL" if yf == 53 else "BEIGE" if yf < 57 else "BEIGED"      # the architrave
            elif yf >= 92:
                role = "PLATE" if yf == 92 else "CHALKD" if yf < 95 else "OUT"         # the stylobate
            else:
                role = "SLATED"                                                       # the glass
                if yf in (64, 80) or x % 8 == 4:
                    role = "OUT"                                                      # its frames
            if side == "lit":
                role = {"SLATED": "SLATE", "OUT": "SLATED", "BEIGE": "BEIGEL", "BEIGED": "BEIGE",
                        "CHALKD": "PLATE"}.get(role, role)
            elif side == "shade":
                role = {"SLATED": "OUT", "BEIGEL": "BEIGE", "BEIGE": "BEIGED", "PLATE": "CHALKD",
                        "CHALK": "CHALKD"}.get(role, role)
            k.px(x, y, role)
    #  a chalk glint on each pane: one short diagonal stroke, the same in every pane
    for x0 in range(hx0 + CHAMFER, hx1 - CHAMFER, 8):
        for i in range(3):
            if k.is_(x0 + 2 + i, 70 - i, "SLATED"):
                k.px(x0 + 2 + i, 70 - i, "CHALKD")
    for y in range(htop, hbot):
        k.px(hx0 + CHAMFER - 1, y, "BEIGEL" if y < 58 or y >= 92 else "SLATE")
        k.px(hx1 - CHAMFER + 1, y, "OUT")
    outline(k, hall)
    # --- the columns: stacked dead hardware, three stacks and their mirrors
    for x0, kind, flip in ERRATA_COLS:
        errata_stack(k, x0, 58, 91, kind, flip)

    # --- the porch: two taller stacks either side of the doorway, a dark recess, the pediment over it
    k.rect(64, 58, 111, 111, "SLATED")
    k.rect(72, 60, 103, 111, "OUT")                             # in the porch's shadow
    k.rect(74, 64, 101, 95, "SLATED")
    for yy in range(72, 92, 8):                                  # the inner glass, dark, a frame every tile row
        k.hline(74, 101, yy, "OUT")
    k.rect(80, 92, 95, 111, "PLATE")                             # the threshold and its step
    k.rect(82, 90, 93, 111, "OUT")                               # the doorway: dark, round-headed
    k.px(82, 90, "PLATE"); k.px(93, 90, "PLATE")
    k.hline(80, 95, 111, "CHALKD")
    k.rect(64, 104, 79, 111, "PLATE"); k.rect(96, 104, 111, 111, "PLATE")     # the porch floor either side
    k.hline(64, 79, 104, "CHALK"); k.hline(96, 111, 104, "CHALK")
    k.hline(64, 111, 111, "CHALKD")
    #  the porch's two stacks are the colonnade's A, set on the same tile rows (so they share its tiles), on a plinth,
    #  a monitor on top of each
    errata_stack(k, 64, 60, 99, "A", False)
    errata_stack(k, 104, 60, 99, "A", True)
    for x0 in (64, 104):
        k.rect(x0, 100, x0 + 7, 103, "PLATE")
        k.hline(x0, x0 + 7, 100, "CHALK")
        errata_stack(k, x0, 60, 67, "E", x0 == 104)
    k.vline(64, 58, 111, "OUT"); k.vline(111, 58, 111, "OUT")

    # --- the slate, laid flat in its frame, seen from above: drawn over the hall's head
    xa, xb, back, top, bot = ERRATA_SLATE
    m = box_mask(xa, xb, back, top, bot, c=6)
    for (x, y), part in m.items():
        L = lean(x, xa, xb, 6)
        if part == "deck":
            k.px(x, y, "WOOD")
        else:
            yf = y + L
            r = yf - top
            side = side_of(x, xa, xb, 6)
            role = "WOODL" if r == 0 else "WOOD" if r < 4 else "WOODD"
            if side == "lit":
                role = {"WOOD": "WOODL", "WOODD": "WOOD"}.get(role, role)
            elif side == "shade":
                role = {"WOODL": "WOOD", "WOOD": "WOODD", "WOODD": "OUT"}.get(role, role)
            k.px(x, y, role)
    #  the frame's grain, and its lit back and left edges (the light is from the upper left)
    for (x, y), part in m.items():
        if part == "deck" and (x % 8, y % 8) in ((1, 3), (5, 6), (6, 6)):
            k.px(x, y, "WOODD")
    k.hline(xa + 6, xb - 6, back, "WOODL")
    SX0, SX1, SY0, SY1 = 9, 166, 8, 40                           # the slate inside the frame
    k.rect(SX0, SY0, SX1, SY1, "SLATE")
    k.hline(SX0, SX1, SY0, "OUT"); k.vline(SX0, SY0, SY1, "OUT")             # the frame's shadow, back and left
    k.hline(SX0 + 1, SX1, SY0 + 1, "SLATED"); k.vline(SX0 + 1, SY0 + 1, SY1, "SLATED")
    k.hline(SX0, SX1, SY1 + 1, "WOODL"); k.vline(SX1 + 1, SY0, SY1 + 1, "WOODL")   # the frame's lit inner lip
    #  ruled in chalk, every 8 rows, on the tile rows: a clean slate
    for y in range(15, SY1, 8):
        k.hline(SX0 + 4, SX1 - 4, y, "CHALKD")
    #  THE ERRATUM (the user, 2026-10-25: moved up from the pediment, where it was too small to read at 1x): the one
    #  line still written on the clean slate, on its lowest rule, centred on the door's axis -- chalk marks in the shape
    #  of words, never letters -- struck through with one line of chalk that runs past both ends; and in it, at the
    #  insertion point, a red caret standing on the line, the correction's mark in chalk over it. The smear of what was
    #  rubbed out is cut (the budget: SLATE had two tiles to spare).
    errata_line(k, ERRATA_LINE, base=38)
    #  the chalk's ledge along the slate's foot
    k.hline(SX0 + 4, SX1 - 4, SY1 + 3, "WOODD")

    # --- the pediment over the porch: a triangle of slate, ruled, its one written line struck through and the red
    #  caret over it. The words are not words: chalk marks the shape of a line, never letters.
    PX0, PX1, PB, PA = 62, 113, 61, 40                          # its left, right, base row, apex row
    cxp = (PX0 + PX1) / 2
    tri = set()
    for y in range(PA, PB + 1):
        half = (y - PA) / (PB - PA) * (PX1 - PX0) / 2
        for x in range(PX0, PX1 + 1):
            if abs(x + 0.5 - (cxp + 0.5)) <= half + 0.5:
                tri.add((x, y))
    for (x, y) in tri:
        k.px(x, y, "SLATE")
    for (x, y) in tri:                                           # the raking cornice: lit on the left, shaded right
        if any((x + dx, y + dy) not in tri for dx, dy in ((1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1))):
            k.px(x, y, "PLATE" if x < cxp else "CHALKD")
    for (x, y) in tri:
        if (x, y - 1) not in tri and (x, y) in tri:
            pass
    k.hline(PX0, PX1, PB, "PLATE")
    k.hline(PX0, PX1, PB + 1, "CHALKD")
    k.hline(PX0, PX1, PB + 2, "OUT")
    #  the echo of the slate's erratum (tweaked 2026-10-25): no written line any more, only one struck rule and the
    #  red caret on it, on the door's axis
    if ERRATA_ECHO:
        k.hline(70, 105, 58, "CHALKD")
        for i in range(3):                                       # the caret, its halves mirrored on the seam
            for dy in (0, 1):
                k.px(87 - i, 54 + i + dy, "RED"); k.px(88 + i, 54 + i + dy, "RED")
    outline(k, tri)

    # --- the annex: a chamfered box, a flat roof seen from above, and one big card pinned flat on it -- the roof's
    #  stone showing round it, the card's shadow on the stone, so it reads as a card laid on a building
    xa, xb, back, top, bot = ERRATA_ANNEX
    m = box_mask(xa, xb, back, top, bot, c=4)
    for (x, y), part in m.items():
        L = lean(x, xa, xb, 4)
        side = side_of(x, xa, xb, 4)
        if part == "deck":
            k.px(x, y, "PLATE" if top - L - y > 1 else "CHALK")           # the roof, its lit front lip
        else:
            yf = y + L
            role = "OUT" if yf == top else "CHALK" if yf < bot else "OUT"
            if side == "lit" and role == "PAPERD":
                role = "CHALK"
            elif side == "shade" and role != "OUT":
                role = {"CHALK": "PAPERD", "PAPERD": "BEIGE"}[role]
            k.px(x, y, role)
    CX0, CX1, CY0, CY1 = 184, 247, 23, 51                       # the card: eight tiles across
    k.rect(CX0 + 2, CY0 + 2, CX1 + 2, CY1 + 2, "CHALKD")         # its shadow on the roof
    k.rect(CX0, CY0, CX1, CY1, "CHALK")
    k.hline(CX0, CX1, CY1, "PAPERD")                             # its edge
    k.vline(CX1, CY0, CY1, "PAPERD")
    #  the card's face: the header rule in red, faint blue rules on the tile rows, a heading, two lines of dashes
    k.hline(CX0 + 3, CX1 - 3, 31, "RED")
    for y in (39, 47):
        k.hline(CX0 + 3, CX1 - 3, y, "SLATEL")
    k.rect(CX0 + 4, 26, CX0 + 15, 28, "OUT")                     # the heading: a dark block, a word's shape
    for y, runs in ((37, ((0, 9), (12, 21), (24, 27), (30, 39))), (45, ((0, 9), (12, 21), (24, 27)))):
        for a, b in runs:
            k.hline(CX0 + 4 + a, CX0 + 4 + b, y, "SLATED")
    #  the pin at the card's head, centred on a tile seam: a red head, its glint, its little shadow
    k.rect(214, 21, 217, 24, "RED")
    k.hline(215, 216, 20, "OUT"); k.hline(215, 216, 25, "OUT")
    k.vline(213, 22, 23, "OUT"); k.vline(218, 22, 23, "OUT")
    k.px(215, 22, "CHALK")
    k.hline(217, 219, 26, "PAPERD")
    #  the dog-ear: the card's lower right corner folded back on itself, the roof showing where it was
    for i in range(6):
        for j in range(6 - i):
            x, y = CX1 - j, CY1 - i
            k.px(x, y, "PLATE" if j + i < 5 else "OUT")
            if j + i < 5:
                k.px(CX1 - 5 + i, CY1 - 5 + j, "PAPERD")         # the flap, folded up over the card
    #  two windows, dark as slate, each centred on a tile seam, a chalk glint on each
    for wx in (186, 234):
        k.rect(wx, 62, wx + 11, 73, "OUT")
        k.rect(wx + 1, 63, wx + 10, 72, "SLATED")
        k.vline(wx + 5, 63, 72, "OUT"); k.vline(wx + 6, 63, 72, "OUT")
        k.px(wx + 2, 66, "CHALKD"); k.px(wx + 3, 65, "CHALKD"); k.px(wx + 9, 66, "CHALKD"); k.px(wx + 8, 65, "CHALKD")
        k.hline(wx - 1, wx + 12, 74, "PAPERD")
    outline(k, m)
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
    #  pair 3 (drafted 2026-10-25): both tilesets are roomy, so the groups reuse blocks as pair 2's do and take free
    #  slots too
    dict(dir="indigo_plateau", symbol="gTileset_IndigoPlateau", layout="IndigoPlateau_Exterior_Layout",
         place="UMBRA / IndigoPlateau_Exterior", town="UMBRA", tag="t447g", pair=3,
         landmarks=[(RB, draw_review_board)], reuse_blocks=True,
         view=[("IndigoPlateau_Exterior_Layout", 0, 0, 24, 20)]),
    dict(dir="pewter_city", symbol="gTileset_PewterCity", layout="PewterCity_Layout",
         place="SLATE / PewterCity", town="SLATE", tag="t447g", pair=3,
         landmarks=[(ERRATA, draw_errata)], reuse_blocks=True, skip_unused_layouts=True,
         view=[("PewterCity_Layout", 2, 0, 36, 20)]),
]
#  this tool's claim; gbatowns.py's LANDMARKS keeps the same boxes out of its passes (by map name)
OWNS = {"cinnabar_island": [("CinnabarIsland", 5, 0, 7, 5, "the MANSION"),
                            ("CinnabarIsland", 5, 6, 7, 4, "SCORN SOLUTIONS (the lab)")],
        "saffron_city": [("SaffronCity", 29, 16, 9, 15, "CORPUS's tower"),
                         ("SaffronCity_Connection", 19, 9, 9, 15, "CORPUS's tower (the crossings' copy)")],
        "lavender_town": [("LavenderTown", 15, 0, 7, 7, "DAEMON TOWER"),
                          ("Route10", 15, 72, 7, 8, "DAEMON TOWER (its top, on ROUTE 10)")],
        "indigo_plateau": [("IndigoPlateau_Exterior", 6, 0, 11, 7, "the REVIEW BOARD"),
                           ("IndigoPlateau_Exterior", 10, 7, 3, 2, "the REVIEW BOARD's porch")],
        "pewter_city": [("PewterCity", 12, 0, 16, 7, "ERRATA, the museum and its annex")]}
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
    #  a group may leave out the layouts no map uses (SLATE's RS_BattleTower), as gbatowns' counts do: their cells
    #  are never on screen, so a tile only they share with the landmark is the landmark's to repaint
    unused = unused_layouts() if GROUP.get("skip_unused_layouts") else set()
    for name, m in ts.maps.items():
        if name in unused:
            continue
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


def unused_layouts():
    """the layouts no map's map.json names (RS_BattleTower and the other RS_* leftovers)"""
    used = set()
    for d in os.listdir(os.path.join(GBA, "data/maps")):
        p = os.path.join(GBA, "data/maps", d, "map.json")
        if os.path.exists(p):
            used.add(json.load(open(p)).get("layout"))
    return {l["name"] for l in layouts() if l.get("name") and l.get("id") not in used}


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
            if ts.cell(TILESET["layout"], x, y) & 0x3FF < NUM_PRIMARY:
                continue                         # a kept primary block (the REVIEW BOARD's sliding door) has none
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
            art = [cut.tile(*assign_row(lm, key)) for key in keys]
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
                lint = [cut.tile(*assign_row(lm, tuple(k.get(ox + qx * 8 + i % 8, oy + qy * 8 + i // 8)
                                                       if lin(k, ox + qx * 8 + i % 8, oy + qy * 8 + i // 8) else 0
                                                       for i in range(64)))) for qy in (0, 1) for qx in (0, 1)]
                entries = art + lint
            elif main and (x, y) in lm.get("keep_bottom", ()):
                entries = bottom + art                  # the cell's own bottom layer kept (the REVIEW BOARD's porch)
            else:
                if lm.get("ground_always") or not any(v & 0x3FF for v in bottom):
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
        for row, cols in lm_rows(lm):
            pals[row] = row_pal(ts, lm, row, cols)
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
        b = lm["ground"](x, y)
        if b < NUM_PRIMARY:                          # a primary ground block (UMBRA's and SLATE's grass)
            return list(struct.unpack_from("<8H", primary()["mt"], b * 16))[:4]
        return ts.entries(b)[:4]
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
    """the drawing in its colours: `colours` a row's [(role, rgb)], or a landmark's canvas index -> RGB (lm_rgb)"""
    pal = colours if isinstance(colours, dict) else pal16(colours)
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


def row_pal(ts, lm, row=None, colours=None):
    """the landmark's palette row (or one of its extra rows): its colours from index 1; a row it shares (DAEMON
    TOWER's row 7, whose 10..15 are left for the KEEPALIVE PLANT) keeps whatever stands past them"""
    row = lm["row"] if row is None else row
    colours = lm["colours"] if colours is None else colours
    cols = [rgb for _, rgb in colours]
    if len(cols) == 15:
        return pal16(colours)
    return [TRANSPARENT] + cols + list(ts.pals[row])[1 + len(cols):]


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


def row_check(ts, lm, ours, row=None, colours=None):
    """a landmark's row must be free (vanilla's unused rows are all black or all blue), already ours, or drawn by
    the landmark's cells and nothing else -- never a row another block draws"""
    row = lm["row"] if row is None else row
    colours = lm["colours"] if colours is None else colours
    cur, want = ts.pals[row], row_pal(ts, lm, row, colours)
    n = len(colours)
    if all(c in ((0, 0, 0), (0, 0, 255)) for c in cur[1:1 + n]):
        return "free"
    if list(cur[1:1 + n]) == list(want[1:1 + n]):
        return "ours"
    others = row_users(ts, row) - set(ours)
    if not others:
        return "drawn by the landmark alone"
    raise SystemExit("  row %d is not free and not ours: %d other cells draw it, e.g. %s"
                     % (row, len(others), sorted(others)[:4]))


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
        label(d, (24, 16), "%s  --  T-447 DRAFT, pair %d (gbalandmarks.py)" % (lm["title"], GROUP.get("pair", 2)), FG, Fb)
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
    rowsp = [(row, after["pals"][row], lm["title"]) for lm, _ in LANDMARKS_HERE for row, _ in lm_rows(lm)]
    s = Image.new("RGB", (max(40 + cols * 40, 840), 130 + ((n + cols - 1) // cols) * 48 + 40 + len(rowsp) * 100), BG)
    d = ImageDraw.Draw(s)
    label(d, (24, 16), "T-447 pair %d tiles -- secondary/%s" % (GROUP.get("pair", 2), GROUP["dir"]), FG, F)
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
        names = ["0"] + [nm for nm, _ in next(cols for lm, _ in LANDMARKS_HERE for row, cols in lm_rows(lm)
                                              if row == r)]
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
    for lm, _ in LANDMARKS_HERE:
        for row, cols in lm.get("extra_rows", ()):
            rowsays[(lm["name"], row)] = row_check(ts, lm, ours, row, cols)
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
                              for lm, _ in LANDMARKS_HERE)
        + "".join("; %d (%s, %d colours)" % (row, rowsays[(lm["name"], row)], len(cols))
                  for lm, _ in LANDMARKS_HERE for row, cols in lm.get("extra_rows", ())),
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
            for row, cols in lm_rows(lm):
                write_pal(os.path.join(tsd, "palettes", "%02d.pal" % row), row_pal(ts, lm, row, cols))
            d = os.path.join(DRAFT, lm["name"])
            os.makedirs(d, exist_ok=True)
            k = after["drawings"][lm["name"]]
            im = drawing_rgb(k, lm_rgb(lm) if lm.get("extra_rows") else lm["colours"])
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
            for row, cols in lm_rows(lm):
                write_pal(os.path.join(tsd, "palettes", "%02d.pal" % row), row_pal(ts, lm, row, cols))
        rules = open(RULES).read()
        new, n = re.subn(r"(secondary/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+" % g["dir"],
                         lambda mm: mm.group(1) + str(after["num_tiles"]), rules)
        assert n == 1
        open(RULES, "w").write(new)
        print("  written: tiles.png, metatiles.bin, metatile_attributes.bin, rows %s, %s, -num_tiles %d" % (
            ", ".join(str(row) for lm, _ in LANDMARKS_HERE for row, _ in lm_rows(lm)),
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
