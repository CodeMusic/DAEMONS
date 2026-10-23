#!/usr/bin/env python3
"""Each town's leftover vanilla art, and the forests (T-438 batch F): redrawn in code, in the town's own style.

    python3 tools/gbatowns.py                      # report: every town secondary and both forests -- how much of what
                                                   #   a player sees is still Nintendo's drawing, object by object, in
                                                   #   the order a player meets them; what is drafted; seams
    python3 tools/gbatowns.py --draft [DIR]        # the drafted towns' tiles.png and groups.json in DIR
                                                   #   (gfx/drafts/t438/towns/), and the sheets in --sheets DIR (the
                                                   #   draft folder when not given): the plan, and per drafted town the
                                                   #   tiles and two or three real map crops, today beside the draft
    python3 tools/gbatowns.py --sheets DIR         # (with --draft) where the sheets go
    python3 tools/gbatowns.py --write --approved   # into the engine: the approved towns' tiles.png (CALLOW, SLATE,
                                                   #   DOLDRUM, THE UNDERTONE, approved 2026-10-23). Refuses without
                                                   #   --approved.

WHAT IS LEFT. Batches A-E took the doors, field effects, the general ground, every interior and the caves. A town's
SECONDARY tileset is part ours already -- gbacivic/gbacivictown (CHECKPOINTS, THE REPO, the BENCHMARKS), gbahouse,
gbarestyle (DOLDRUM's houses), gbaschoolfront (CALLOW SCHOOL), gbagrove -- and part still vanilla: a tile is LEFT when
its pixels are byte-identical to pret's and a map a player can reach draws it (layouts no map uses -- RS_BattleTower,
the Prototype Sevii isles -- are left out of every count). Each town's leftovers are grouped into OBJECTS: the cells on
a map that draw one, joined where they touch, so the plan can say "the museum: 352 tile draws" instead of "92 tiles".

HOW IT IS DRAWN (batches C-E's lessons): bold forms that read at 1x, never speckle; draw by ROLE so the palettes can
follow. Every index a leftover object uses in each palette row is given a MATERIAL (roof, wall, glass, plank...) in
MATERIALS below, and each town gives each material a MOTIF -- CALLOW's roofs are new leaf-scale shingles, SLATE's are
slates, DOLDRUM's are long becalmed swells. A tile is redrawn where it is drawn MOST (its home object, on the map that
shows it most), in that object's own coordinates, so a motif runs on across tiles and blocks; within a material the
motif picks a rank light..dark and the material's own indices, sorted by their colour, supply it. So:

  * FOOTPRINT: a transparent pixel (index 0) stays transparent and a drawn one stays drawn -- every top-layer tile
    still shows the ground where it did, and the roof still covers the player where it did;
  * SILHOUETTE: a pixel of one material that touches another material, or nothing, keeps vanilla's index, so every
    outline, eave, sill and join is vanilla's and agrees with the tile beside it;
  * an index no material names (outlines, whites, the little red door, bikes, lamps) keeps vanilla's pixel;
  * no block, layer, flip, palette row, behaviour or collision bit moves, and no palette changes. A palette change is
    the user's call; the roles make one cheap later.

A tile vanilla copied from primary/general (a ledge's end, a fence post) and drew in rows 0..6 is not redrawn here: it
takes batch C's current drawing of the same general tile, flips and all, so it matches the ground around it.

NOT TOUCHED. A DOOR's tiles (field_door.c's table): gbadoors.py derives each door's animation from its closed block, so
a door is redrawn by re-running gbadoors after a town is built. LAVENDER (HALFTONE) is grey by DaemonsIsHalftone() and
keeps T-430's rules -- its look below must still read in grey. The palettes of every row.

SEAMS (engine.md trap 14). A block within seven cells of a connection to another tileset must draw the same in both;
the draft is checked with gbaseams.py's own comparison, run once on today's tiles and once on the draft, and any cell
the draft newly breaks is reported (and listed in groups.json).
"""
import collections, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t438", "towns")
GEN = "data/tilesets/primary/general"
SEC = "data/tilesets/secondary/"

ARGS = sys.argv[1:]
WRITE = "--write" in ARGS


def argval(flag):
    if flag in ARGS:
        i = ARGS.index(flag)
        if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--"):
            return ARGS[i + 1]
        return ""
    return None


DRAFT = argval("--draft")
if DRAFT == "":
    DRAFT = DRAFT_DEFAULT
SHEETS = argval("--sheets") or DRAFT

# ================================================================== the plan, in the order a player meets each place
#  ts, the DAEMONS name, what the bible makes of it (vision.md 3.1/3.2/3.3, 2.10), the look proposed for its leftovers,
#  and the leftover OBJECTS by name: "Map@x,y" is the top-left cell of the object as the census finds it.
PLAN = [
    dict(ts="viridian_city", name="CALLOW CITY", theme="green, and unripe: untested (3.1); the school town",
         look="NEW GROWTH, in the kit CALLOW's own green houses already set: the ribbed roof with a lit ridge cap, "
              "boards laid level with a lit top edge, a striped awning, paving slabs, a fir cut as tiers of fronds",
         objects={"Route22@4,0": "ROUTE 22's gate to UMBRA: roof, boarded wall, awning, porch, two firs",
                  "ViridianCity@25,8": "the green house's roof hatch",
                  "ViridianCity@26,19": "the tower block's planters",
                  "*": "ledge ends by the pond and on ROUTE 22 (kept: they read as batch C's ledge)"}),
    dict(ts="viridian_forest", name="THE UNDERTONE", theme="green half-light; the first real maze (3.2)",
         look="HALF-LIGHT: every canopy a heap of bold leaf clumps, lit on top, sinking to a deep undertone green "
              "underneath; bark in long vertical lines. Same trees, same maze",
         objects={"ViridianForest@0,9": "the canopy (every tree; one drawing tiled)",
                  "ViridianForest@12,0": "the canopy (east half)",
                  "SixIsland_PatternBush@0,0": "THE SAME BUSH shares the tileset (SIX ISLAND)",
                  "SixIsland_PatternBush@6,24": "THE SAME BUSH's south edge",
                  "ViridianForest_Grove@*": "the first grove's trees", "ViridianForest@*": "the canopy",
                  "*": "flowers, stumps, the grove's edge"}),
    dict(ts="pewter_city", name="SLATE CITY", theme="stone, a writing surface, a clean slate; the museum of dead "
                                                    "hardware (ERRATA, 4.32)",
         look="SLATE: every roof laid in real slates, staggered, a shade apart; walls in dressed stone courses; the "
              "museum's glass dark like a slate with a chalk-stroke glint",
         objects={"PewterCity@12,0": "the ERRATA museum and its annex: roof, colonnade, porch, steps",
                  "PewterCity@32,8": "a slate-roofed house (NE)", "PewterCity@8,27": "a slate-roofed house (SW)"}),
    dict(ts="cerulean_city", name="DOLDRUM CITY", theme="the becalmed sea; gradient descent stuck with no slope "
                                                       "(3.1); BENCHMARK 2 is FLOW",
         look="BECALMED: long bleached planks laid along the bridges, no wave in them; roofs as slow flat swells; the "
              "bike shop's skylight as still water in level bands; a tide line along every skirt",
         objects={"Route24@9,17": "ROUTE 24's long bridge", "CeruleanCity@10,23": "the bike shop and its rack",
                  "CeruleanCity@21,0": "the north bridge", "Route25@49,1": "the sea cottage (ROUTE 25)",
                  "Route5@21,24": "ROUTE 5's house: door arch and base", "*": "house doors (door cells, kept)"}),
    dict(ts="vermilion_city", name="ARDOR CITY", theme="flush, heat and brash zeal; the port (3.1)",
         look="HEAT: roofs in hot glazed pantiles, the dock's planking sun-bleached, the cargo truck and planters "
              "redrawn, the harbour bollards as warm iron",
         objects={"VermilionCity@8,14": "the orange-roofed houses and the green-roofed hall",
                  "VermilionCity@20,32": "the S.S. ANNE pier: lighthouses, awning, quay",
                  "SSAnne_Exterior@55,1": "the truck on the quay",
                  "SSAnne_Exterior@*": "the quay: awnings, planters", "Route6@2,26": "ROUTE 6's pond edge",
                  "*": "orange-roofed houses, awnings, planters"}),
    dict(ts="lavender_town", name="HALFTONE TOWN", theme="dots that only look like grey; the tower (3.1); grey "
                                                        "by DaemonsIsHalftone(), T-430",
         look="HALFTONE: every surface as a dot screen -- roofs, the boardwalks' planks, the KEEPALIVE PLANT's walls "
              "-- big dots on light, small on dark, so it reads as tone in grey and as dots up close",
         objects={"Route12@8,22": "ROUTE 12's boardwalks (three stretches)", "Route10@2,34": "the KEEPALIVE PLANT", "Route12@*": "ROUTE 12's boardwalks (three stretches)",
                  "Route13@*": "ROUTE 13's trees and boardwalk", "LavenderTown@*": "the purple-roofed houses",
                  "Route13@46,0": "ROUTE 13's trees and boardwalk", "LavenderTown@15,0": "the tower's base",
                  "Route10@15,72": "ROUTE 10's domed centre", "LavenderTown@3,13": "the purple-roofed houses",
                  "*": "houses, fences"}),
    dict(ts="celadon_city", name="VERDIGRIS CITY", theme="green corrosion on bronze; CORPUS rotting beneath (3.1)",
         look="VERDIGRIS: bronze roofs and trims furred with green bloom where the rain runs; ROUTE 17's cycling "
              "road as a long streak of smeared lanes (THE STREAK)",
         objects={"Route17@1,0": "THE STREAK: the cycling road", "CeladonCity@7,4": "the department store",
                  "CeladonCity@31,17": "the mansion", "CeladonCity@12,18": "the fountain", "Route17@*": "THE STREAK: the cycling road",
                  "CeladonCity@*": "rooftops and small bits",
                  "*": "rooftops, the gym's hedges, small bits"}),
    dict(ts="saffron_city", name="BRAZEN CITY", theme="brass over base metal, unhidden; corporate capture (3.1, "
                                                     "4.4)",
         look="BRASS: plating works -- roofs in stamped brass panels, walls in rolled sheet with rivet lines, the "
              "tower's glass in a gold curtain wall; the plaza laid in a corporate grid",
         objects={"SaffronCity@14,9": "the plaza, houses and the tower (SILPH)",
                  "SaffronCity@35,8": "the north row", "SaffronCity@25,35": "the south row and the dojo",
                  "SaffronCity_Connection@*": "SaffronCity_Connection (a copy of the city for the crossings)",
                  "*": "the gym, the dojo, small bits"}),
    dict(ts="fuchsia_city", name="LURID CITY", theme="garish glow, shocking; spectacle and toxicity (3.1)",
         look="LURID: the SAFARI's woods and LURID's frontages in saturated glow -- neon trims, sickly bright "
              "foliage, signs that hum",
         objects={"SafariZone_East@0,0": "the SAFARI ZONE's woods, ponds, rest houses (four areas)",
                  "FuchsiaCity@2,0": "the SAFARI gate's frontage", "FuchsiaCity@5,6": "the west pens",
                  "FuchsiaCity@31,6": "the east pens",
                  "SafariZone_North@*": "the SAFARI ZONE's woods, ponds, rest houses (four areas)",
                  "SafariZone_West@*": "the SAFARI ZONE's woods, ponds, rest houses (four areas)",
                  "SafariZone_Center@*": "the SAFARI ZONE's woods, ponds, rest houses (four areas)",
                  "SafariZone_East@*": "the SAFARI ZONE's woods, ponds, rest houses (four areas)",
                  "Route15@*": "ROUTE 15 / 19 bits", "Route19@*": "ROUTE 15 / 19 bits", "*": "small bits"}),
    dict(ts="cinnabar_island", name="QUICKSILVER IS.", theme="mercury: alive, unstable, poisonous; the ruined lab "
                                                            "(3.1)",
         look="MERCURY: the lab's walls as liquid-bright metal pooling at the base; the mansion's roof scorched; "
              "the shore's sand silvered",
         objects={"CinnabarIsland@5,0": "the MANSION's front", "CinnabarIsland@5,6": "the lab (SCORN's)",
                  "Route21_South@5,48": "ROUTE 21's jetty", "Route20@66,3": "ROUTE 20's islet",
                  "*": "safari-zone leftovers (unused layouts excluded)"}),
    dict(ts="sevii_islands_123", name="ONE / TWO / THREE ISLAND", theme="the islands (2.10): FINDERS BEACH, THE "
                                                                       "OVERLOOK, LONGCROSS",
         look="ISLAND KIT: the purple-roofed houses in sea-weathered board, the harbours' red roofs as nets drying, "
              "the NET centre's dish",
         objects={"OneIsland@11,0": "ONE ISLAND's NET centre", "TwoIsland@32,6": "TWO ISLAND's shop and house",
                  "ThreeIsland_Port@9,14": "the harbour houses (every port)", "*": "purple-roofed houses"}),
    dict(ts="sevii_islands_45", name="FOUR / FIVE ISLAND", theme="RESORT SUBLIME, SOMEONE'S STONE, FIVE ISLE "
                                                                "MEADOW (2.10)",
         look="as ONE..THREE's kit (one look for the islands), and SOMEONE'S STONE's cairn as stacked river stones",
         objects={"FiveIsland@9,15": "the harbour houses", "FiveIsland_Meadow@9,17": "the meadow's barn",
                  "FiveIsland_MemorialPillar@*": "SOMEONE'S STONE and its stones", "*": "purple-roofed houses"}),
    dict(ts="sevii_islands_67", name="SIX / SEVEN ISLAND", theme="USER TOWER, LONG DROP, TANOBY, THE ANNEX (2.10)",
         look="as the islands' kit; USER TOWER's glass curtain; TANOBY's doors wait for batch G",
         objects={"BirthIsland_Exterior@10,7": "THE ANNEX's triangle", "SevenIsland_TrainerTower@54,0": "USER TOWER",
                  "SevenIsland_TanobyRuins@*": "TANOBY's chamber doors (x7)", "*": "harbour and houses"}),
    dict(ts="berry_forest", name="DENSE WOOD", theme="THREE ISLAND's forest (2.10)",
         look="as THE UNDERTONE, but denser: the berry trees' own drawing in the same clumps",
         objects={"ThreeIsland_BerryForest@0,0": "the canopy", "*": "stumps, flowers, the clearing"}),
]
SHORT = {"viridian_city": "callow", "pewter_city": "slate", "cerulean_city": "doldrum",
         "viridian_forest": "undertone"}
DRAFTED = ["viridian_city", "pewter_city", "cerulean_city", "viridian_forest"]
#  the user, 2026-10-23: build these four (SLATE's museum roof and CALLOW's cottage roof calmed first); the rest stay
#  drafts until approved
APPROVED = ["viridian_city", "pewter_city", "cerulean_city", "viridian_forest"]


# ================================================================== reading the engine
def tiles_of(im):
    w, h = im.size
    px = im.tobytes()
    return [[px[(ty * 8 + r) * w + tx * 8 + c] & 15 for r in range(8) for c in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def entries(buf, i):
    return struct.unpack_from("<8H", buf, i * 16)


_LAYOUTS = None
_USED = None


def layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {l["name"][:-len("_Layout")]: l for l in
                    json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "name" in l}
    return _LAYOUTS


def used_layouts():
    """layout name -> the maps that use it; a layout no map uses (RS_*) and the Prototype isles are not reachable"""
    global _USED
    if _USED is None:
        ids = {l["id"]: n for n, l in layouts().items()}
        _USED = collections.defaultdict(list)
        for d in sorted(os.listdir(os.path.join(GBA, "data/maps"))):
            p = os.path.join(GBA, "data/maps", d, "map.json")
            if os.path.exists(p) and not d.startswith("Prototype_"):
                j = json.load(open(p))
                if j.get("layout") in ids:
                    _USED[ids[j["layout"]]].append(d)
    return _USED


_GEN = {}


def general():
    if not _GEN:
        d = os.path.join(GBA, GEN)
        _GEN.update(tiles=tiles_of(Image.open(os.path.join(d, "tiles.png"))),
                    van=tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, GEN + "/tiles.png", binary=True)))),
                    pals=[read_pal(os.path.join(d, "palettes/%02d.pal" % r)) for r in range(16)],
                    mt=open(os.path.join(d, "metatiles.bin"), "rb").read())
    return _GEN


def camel(ts):
    return "".join(w.title() for w in ts.split("_")).replace("Islands", "Islands")


def door_blocks(ts):
    """the block ids (secondary, from 640) field_door.c animates in this tileset"""
    labels = dict(re.findall(r"#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+)",
                             open(os.path.join(GBA, "include/constants/metatile_labels.h")).read()))
    fd = open(os.path.join(GBA, "src/field_door.c")).read()
    sym = "gTileset_" + camel(ts)
    pre = re.sub(r"[^a-z0-9]", "", sym.replace("gTileset_", "").lower())
    out = set()
    for name in re.findall(r"\{(METATILE_\w+),\s*DOOR_SOUND", fd):
        owner = name[len("METATILE_"):].rsplit("_", 1)[0]
        own = re.sub(r"[^a-z0-9]", "", owner.lower())
        if name in labels and (own == pre or own.startswith(pre)):
            v = int(labels[name], 16)
            if v >= 640:
                out.add(v)
    return out


class Town:
    """one secondary tileset: its tiles as the engine has them, vanilla's, and where each is drawn"""

    def __init__(self, ts):
        self.ts = ts
        self.dir = os.path.join(GBA, SEC + ts)
        self.im = Image.open(os.path.join(self.dir, "tiles.png"))
        self.now = tiles_of(self.im)
        self.van = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, SEC + ts + "/tiles.png", binary=True))))
        self.pals = [read_pal(os.path.join(self.dir, "palettes/%02d.pal" % r)) for r in range(16)]
        self.mt = open(os.path.join(self.dir, "metatiles.bin"), "rb").read()
        self.nblocks = len(self.mt) // 16
        sym = "gTileset_" + camel(ts)
        want = re.sub(r"[^a-z0-9]", "", ts)
        self.maps = sorted(n for n, l in layouts().items()
                           if re.sub(r"[^a-z0-9]", "", l["secondary_tileset"].replace("gTileset_", "").lower()) == want
                           and n in used_layouts())
        self.sym = sym
        self.placed = collections.Counter()
        self.grid = {}
        for m in self.maps:
            l = layouts()[m]
            d = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            g = [struct.unpack_from("<H", d, k * 2)[0] & 0x3FF for k in range(len(d) // 2)]
            self.grid[m] = g
            for v in g:
                self.placed[v] += 1
        self.doors = door_blocks(ts)
        door_tiles = set()
        for b in self.doors:
            if (b - 640) < self.nblocks:
                door_tiles |= {(v & 0x3FF) - 640 for v in entries(self.mt, b - 640) if v & 0x3FF >= 640}
        self.door_tiles = door_tiles
        self.draws = collections.Counter()          # tile -> placements on reachable maps (8x8 draws)
        for b in range(self.nblocks):
            w = self.placed.get(640 + b, 0)
            if not w:
                continue
            for v in entries(self.mt, b):
                t = v & 0x3FF
                if t >= 640:
                    self.draws[t - 640] += w
        self.disk = [list(t) for t in self.now]
        self._leftovers()

    def _leftovers(self):
        nb = lambda t: any(self.now[t])
        self.left = {t for t in range(min(len(self.van), len(self.now)))
                     if self.now[t] == self.van[t] and nb(t) and self.draws[t]}
        self.targets = self.left - self.door_tiles

    def as_before(self, tiles):
        """read these tiles as vanilla's again (what they were before this tool drew them)"""
        for t in tiles:
            self.now[t] = list(self.van[t])
        self._leftovers()

    def share(self):
        """(vanilla draws, all draws) over every non-blank secondary tile a reachable map draws"""
        tot = sum(n for t, n in self.draws.items() if t < len(self.now) and any(self.now[t]))
        return sum(self.draws[t] for t in self.left), tot

    def objects(self, tiles=None):
        """every group of touching cells, on every reachable map, that draws one of `tiles` (the leftovers)"""
        V = self.left if tiles is None else tiles
        out = []
        for m in self.maps:
            l = layouts()[m]
            W, H = l["width"], l["height"]
            g = self.grid[m]
            cell = {}
            for y in range(H):
                for x in range(W):
                    b = g[y * W + x]
                    if b < 640 or b - 640 >= self.nblocks:
                        continue
                    n = sum(1 for v in entries(self.mt, b - 640) if (v & 0x3FF) - 640 in V)
                    if n:
                        cell[(x, y)] = n
            seen = set()
            for p in sorted(cell):
                if p in seen:
                    continue
                st, grp = [p], []
                seen.add(p)
                while st:
                    q = st.pop()
                    grp.append(q)
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            r = (q[0] + dx, q[1] + dy)
                            if r in cell and r not in seen:
                                seen.add(r)
                                st.append(r)
                xs, ys = [a for a, _ in grp], [b for _, b in grp]
                out.append(dict(map=m, box=[min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1],
                                cells=sorted(grp), draws=sum(cell[c] for c in grp)))
        out.sort(key=lambda o: -o["draws"])
        return out

    def palette(self, row):
        return general()["pals"][row] if row < 7 else self.pals[row]


# ================================================================== drawing by role
#  MATERIALS: per town, per palette row, index -> material. Only an index named here is ever redrawn; every other one
#  (outlines, whites, a door's red, the bikes, lamps) keeps vanilla's pixel. Read from what each leftover object uses
#  (the census's index counts) and checked on the sheets.
MATERIALS = {
    "viridian_city": {
        12: {2: "roof", 15: "roof", 3: "roof", 7: "wall", 8: "wall", 9: "wall", 12: "glass", 13: "glass",
             14: "glass"},
        9: {11: "awning", 12: "awning", 13: "awning", 2: "slab", 3: "slab", 4: "slab"},
        0: {1: "fir", 2: "fir", 3: "fir", 4: "fir"},
        8: {6: "wood", 7: "wood", 8: "wood"},
        10: {5: "wood", 6: "wood", 7: "wood", 9: "leaf", 10: "leaf", 11: "leaf"},
    },
    "pewter_city": {
        10: {12: "roof", 13: "roof", 14: "roof", 15: "roof", 8: "stone", 9: "stone", 10: "stone",
             2: "column", 3: "column", 4: "column"},
        8: {5: "slates", 6: "slates", 7: "slates", 2: "siding", 3: "siding", 4: "siding", 13: "siding",
            8: "glass", 9: "glass", 10: "glass"},
        9: {8: "glass", 9: "glass", 10: "glass"},
        11: {5: "glass", 6: "glass", 12: "glass"},
    },
    "cerulean_city": {
        5: {8: "plank", 9: "plank", 10: "plank"},
        8: {1: "skylight", 2: "skylight", 3: "skylight", 4: "skylight", 11: "panel", 13: "panel", 14: "panel"},
        9: {1: "awning", 3: "awning", 6: "awning", 2: "awning", 4: "awning", 5: "awning"},
        11: {10: "roof", 11: "roof", 12: "roof", 13: "roof", 14: "roof", 2: "siding", 4: "siding", 8: "siding",
             9: "siding"},
        12: {11: "skirt", 12: "skirt", 13: "skirt", 14: "skirt"},
        10: {2: "siding", 3: "siding", 4: "siding", 8: "glass", 9: "glass"},
    },
    "viridian_forest": {
        8: {1: "canopy", 2: "canopy", 3: "canopy", 4: "canopy", 5: "canopy", 6: "bark", 7: "bark", 8: "bark"},
    },
}


def _h(*a):
    """a small deterministic hash -> 0..1"""
    v = 2166136261
    for x in a:
        v = ((v ^ (x & 0xFFFF)) * 16777619) & 0xFFFFFFFF
    return (v >> 8) / float(1 << 24)


#  A motif: (x, y) inside its region, the region's (w, h), the object's (X, Y), and vanilla's level there (0 light ..
#  1 dark, within the material) -> a level. Bold shapes, two or three steps, never a lone pixel of noise.
def m_ribs(x, y, w, h, X, Y, b):
    """CALLOW: the ribbed roof CALLOW's own green houses already have -- a lit cap along the ridge, then standing
    seams every four pixels, each a lit edge, a body and a dark groove"""
    if y < 3:
        return 0.0 if y < 2 else 0.5
    if X % 4 == 3:
        return 1.0
    return 0.0 if X % 4 == 0 else 0.5


def m_ribs_calm(x, y, w, h, X, Y, b):
    """CALLOW's cottage roof (ROUTE 22's gate), calmed for 1x (the user, 2026-10-23): the same standing-seam roof,
    but a seam every eight pixels instead of four, and one step of shade instead of three -- a pale sheet with a
    soft groove, under the lit ridge cap"""
    if y < 2:
        return 0.0
    if y == 2:
        return 0.5
    return 0.5 if X % 8 == 7 else 0.0


def m_clapboard(x, y, w, h, X, Y, b):
    """boards laid level: a lit top edge, the body, a dark under-lap"""
    yy = Y % 4
    return (0.0, 0.4, 0.5, 1.0)[yy]


def m_awning(x, y, w, h, X, Y, b):
    if y >= h - 1:
        return 1.0
    return 0.0 if (X // 4) % 2 == 0 else 0.6


def m_slab(x, y, w, h, X, Y, b):
    """big paving slabs, lit on their top and left edges"""
    xo, yo = (X + (4 if (Y // 8) % 2 else 0)) % 8, Y % 8
    if yo == 7 or xo == 7:
        return 1.0
    if yo == 0 or xo == 0:
        return 0.0
    return 0.45


def m_fir(x, y, w, h, X, Y, b):
    """a fir as tiers of fronds: each tier a lit chevron over a dark underside"""
    if b >= 0.85:
        return b                                   # the trunk's and the shadow's darks stay
    yy = Y % 4
    cx = abs(x - (w - 1) / 2.0)
    if yy == 3:
        return 1.0 if cx < w / 2.0 - 1 else 0.66
    if yy == 0 or (yy == 1 and cx < 2):
        return 0.0
    return 0.33 + 0.33 * (cx > w / 4.0)


def m_boards(x, y, w, h, X, Y, b):
    yy = Y % 4
    return (0.0, 0.4, 0.5, 1.0)[yy] if h > 3 else 0.2 + 0.6 * (y / max(h - 1, 1))


def m_leaf(x, y, w, h, X, Y, b):
    """small bold leaves: a light crown and a dark heel"""
    xo, yo = X % 4, Y % 4
    if yo == 0 and xo in (1, 2):
        return 0.0
    if yo == 3:
        return 1.0
    return 0.5


def m_glass(x, y, w, h, X, Y, b):
    """a pane: dark below, lighter above, one bold diagonal glint"""
    if (x + y) % 8 in (1, 2) and y <= h * 0.6:
        return 0.0
    return 0.35 + 0.65 * (y / max(h - 1, 1))


def m_glass_chalk(x, y, w, h, X, Y, b):
    """SLATE's glass: dark as a slate, one pale chalk stroke across it"""
    if (x + 2 * y) % 8 in (2, 3) and 0 < y < h - 1:
        return 0.0
    return 0.75 + 0.25 * (y / max(h - 1, 1))


def m_slates(x, y, w, h, X, Y, b):
    """SLATE: real slates, 8 x 4, staggered by half; one in three a shade darker"""
    row = Y // 4
    xo, yy = (X + (4 if row % 2 else 0)) % 8, Y % 4
    if yy == 3:
        return 1.0
    if xo == 0:
        return 0.85
    tone = 0.5 if _h(row, (X + (4 if row % 2 else 0)) // 8) < 0.67 else 0.75
    return 0.2 if yy == 0 else tone


def m_slates_calm(x, y, w, h, X, Y, b):
    """SLATE's museum roof, calmed for 1x (the user, 2026-10-23): wide slates, 16 x 8 staggered by half, laid in
    the body's own shade with only their lower edge and joints a step darker; vanilla's lit ridge band stays lit"""
    if b < 0.5:
        return b
    row = Y // 8
    xo, yy = (X + (8 if row % 2 else 0)) % 16, Y % 8
    if yy == 7 or (xo == 0 and yy < 7):
        return 1.0
    return 2.0 / 3


def m_ashlar(x, y, w, h, X, Y, b):
    """dressed stone in courses, 16 x 4 staggered by half, lit top-left, dark joints"""
    row = Y // 4
    xo, yy = (X + (8 if row % 2 else 0)) % 16, Y % 4
    if yy == 3 or xo == 15:
        return 1.0
    if yy == 0 or xo == 0:
        return 0.0
    return 0.5


def m_flutes(x, y, w, h, X, Y, b):
    """a column's flutes: lit and dark in pairs, top to bottom"""
    return (0.0, 0.5, 1.0, 0.5)[X % 4]


def m_plank_long(x, y, w, h, X, Y, b):
    """DOLDRUM: long planks laid along the span, eight pixels wide, no joint and no wave in them (a bridge repeats
    one tile along its length, so a joint would repeat every 16 pixels)"""
    along_y = h >= w
    a = X if along_y else Y
    if a % 8 == 7:
        return 1.0
    return 0.0 if a % 8 == 0 else (0.35 if a % 8 < 4 else 0.5)


def m_swell(x, y, w, h, X, Y, b):
    """DOLDRUM's roofs: slow flat swells, one long low crest every eight rows"""
    yy = (Y + int(2 * _wave(X))) % 8
    return (0.0, 0.0, 0.45, 0.45, 0.45, 0.45, 0.45, 1.0)[yy] * 0.75 + 0.25 * (y / max(h - 1, 1))


def _wave(X):
    return (0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)[X % 16]


def m_still(x, y, w, h, X, Y, b):
    """the bike shop's skylight as still water: level bands, darker toward the bottom"""
    yy = y % 4
    if yy == 0:
        return 0.0
    return 0.25 + 0.6 * (y / max(h - 1, 1))


def m_panel(x, y, w, h, X, Y, b):
    """steel panels with a vertical seam every 8"""
    if X % 8 == 7:
        return 1.0
    if X % 8 == 0:
        return 0.0
    return 0.45


def m_tide(x, y, w, h, X, Y, b):
    """a tide line along the skirt: pale over dark"""
    return 0.0 if y < h / 2.0 else 1.0


LOBES = [(5, 5, 6.0), (12, 6, 5.5), (4, 13, 5.5), (12, 13, 6.0)]


def m_canopy(x, y, w, h, X, Y, b):
    """THE UNDERTONE: a canopy heaped in four bold leaf clumps to every 16 pixels (the trees are drawn on that grid and
    repeat one drawing, so every tree gets the same clumps), each in three bands -- a lit crown at its upper left,
    the body, and its lower rim sunk in the undertone. Vanilla's two darkest greens are kept where they are: they
    are what separates one tree from the next, so the maze still reads as trees"""
    if b >= 0.74:
        return b
    xo, yo = X % 16, Y % 16
    best = None
    for cx, cy, r in LOBES:
        for ox in (-16, 0, 16):
            for oy in (-16, 0, 16):
                dx, dy = xo - cx - ox, yo - cy - oy
                d = (dx * dx + dy * dy) ** 0.5 / r
                if best is None or d < best[0]:
                    best = (d, dx, dy, r)
    d, dx, dy, r = best
    if d > 0.85 and dy > 0:
        return 0.75                                 # the rim under a clump: the undertone
    lit = (dx + dy) / (2 * r)                       # -1 upper left .. +1 lower right
    return 0.0 if lit < -0.3 else (0.25 if lit < 0.1 else 0.5)


def m_bark(x, y, w, h, X, Y, b):
    return (0.0, 0.6, 1.0)[X % 3] if b < 0.9 else 1.0


STYLE = {
    "viridian_city": dict(roof=m_ribs_calm, wall=m_clapboard, glass=m_glass, awning=m_awning, slab=m_slab, fir=m_fir,
                          wood=m_boards, leaf=m_leaf),
    "pewter_city": dict(roof=m_slates_calm, slates=m_slates, stone=m_ashlar, siding=m_ashlar, column=m_flutes,
                        glass=m_glass_chalk),
    "cerulean_city": dict(plank=m_plank_long, skylight=m_still, panel=m_panel, awning=m_awning, roof=m_swell,
                          siding=m_clapboard, skirt=m_tide, glass=m_glass),
    "viridian_forest": dict(canopy=m_canopy, bark=m_bark),
}
#  how much of vanilla's own light a material keeps (0: the motif alone; 0.5: half and half)
KEEP_LIGHT = {"canopy": 0.0, "fir": 0.0, "glass": 0.2, "roof": 0.25, "slates": 0.2}
#  ... and per town, where a calmed motif sets its own shades (it keeps vanilla's light itself, or none)
KEEP_LIGHT_TOWN = {("viridian_city", "roof"): 0.0, ("pewter_city", "roof"): 0.0}


def ladder(town, row, mat):
    """this material's indices in this row, light to dark"""
    plan = MATERIALS[town.ts].get(row, {})
    pal = town.palette(row)
    ix = [i for i, m in plan.items() if m == mat]
    return sorted(ix, key=lambda i: -(0.30 * pal[i][0] + 0.59 * pal[i][1] + 0.11 * pal[i][2]))


# ================================================================== where each tile is drawn, and redrawing it there
class Plane:
    """one object, one layer: every pixel's (row, index, tile, pixel-in-tile), in the object's own coordinates"""

    def __init__(self, town, obj, layer, tiles):
        m = obj["map"]
        l = layouts()[m]
        W, H = l["width"], l["height"]
        x0, y0, w, h = obj["box"]
        x0, y0 = max(0, x0 - 1), max(0, y0 - 1)
        w, h = min(w + 2, W - x0), min(h + 2, H - y0)
        self.x0, self.y0, self.w, self.h = x0, y0, w * 16, h * 16
        self.px = [[None] * self.w for _ in range(self.h)]
        G = general()
        g = town.grid[m]
        for cy in range(h):
            for cx in range(w):
                b = g[(y0 + cy) * W + x0 + cx]
                buf, k = (G["mt"], b) if b < 640 else (town.mt, b - 640)
                if (k + 1) * 16 > len(buf):
                    continue
                e = entries(buf, k)
                for q in range(4):
                    v = e[layer * 4 + q]
                    t, row = v & 0x3FF, v >> 12
                    src = G["tiles"][t] if t < 640 else (tiles[t - 640] if t - 640 < len(tiles) else [0] * 64)
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if v & 0x400 else tx
                            sy = 7 - ty if v & 0x800 else ty
                            c = src[sy * 8 + sx]
                            if c == 0:
                                continue
                            X, Y = cx * 16 + (q % 2) * 8 + tx, cy * 16 + (q // 2) * 8 + ty
                            self.px[Y][X] = (row, c, t - 640 if t >= 640 else None, sy * 8 + sx)


def drawn_before(ts):
    """a Town read as it was before this tool wrote it, and the tiles this tool drew there. A tile it drew no longer
    matches vanilla's, so a second --write would see fewer leftovers, group them into smaller objects and draw them
    differently; so the tiles whose pixels are exactly what this tool would draw over vanilla are read as vanilla
    again -- found as a fixed point, since which tiles are leftovers decides how each is drawn -- and a second write
    is a no-op (batch D's lesson)."""
    town = Town(ts)
    van = lambda t: t < len(town.van)
    cand = {t for t in range(len(town.disk)) if van(t) and town.disk[t] != town.van[t] and any(town.van[t])
            and town.draws[t] and all((a == 0) == (b == 0) for a, b in zip(town.disk[t], town.van[t]))}
    while cand:
        town = Town(ts)
        town.as_before(cand)
        new, _ = redraw(town)
        keep = {t for t in cand if new[t] == town.disk[t]}
        if keep == cand:
            return town, cand
        cand = keep
    return Town(ts), set()


def redraw(town):
    """{tile: new pixels} for every leftover tile: general's copies take batch C's drawing; the rest are redrawn in
    their home object by role. Returns (tiles, what) -- `what` names how each changed tile was drawn."""
    new = [list(t) for t in town.now]
    what = {}
    G = general()
    rows = collections.defaultdict(collections.Counter)
    for b in range(town.nblocks):
        for v in entries(town.mt, b):
            if v & 0x3FF >= 640:
                rows[(v & 0x3FF) - 640][v >> 12] += 1 + town.placed.get(640 + b, 0)
    #  1. general's own tiles, copied into the town: take batch C's drawing
    gvan = {}
    for i, p in enumerate(G["van"]):
        for f in range(4):
            q = tuple(p[(7 - k // 8 if f & 2 else k // 8) * 8 + (7 - k % 8 if f & 1 else k % 8)] for k in range(64))
            gvan.setdefault(q, (i, f))
    for t in sorted(town.targets):
        hit = gvan.get(tuple(town.van[t]))
        if hit and all(r < 7 for r in rows[t]) and G["tiles"][hit[0]] != G["van"][hit[0]]:
            i, f = hit
            src = G["tiles"][i]
            new[t] = [src[(7 - k // 8 if f & 2 else k // 8) * 8 + (7 - k % 8 if f & 1 else k % 8)] for k in range(64)]
            what[t] = "general"
    #  2. the rest, by role, each where it is drawn most
    style = STYLE.get(town.ts)
    if not style:
        return new, what
    plan = MATERIALS[town.ts]
    todo = {t for t in town.targets if t not in what}
    for obj in town.objects(todo):
        if not todo:
            break
        for layer in (0, 1):
            P = Plane(town, obj, layer, town.van if len(town.van) == len(town.now) else
                      [town.van[i] if i < len(town.van) else town.now[i] for i in range(len(town.now))])
            mat = lambda p: plan.get(p[0], {}).get(p[1]) if p else None
            region = {}
            #  regions: 4-connected pixels of one material in this layer
            for Y in range(P.h):
                for X in range(P.w):
                    p = P.px[Y][X]
                    m = mat(p)
                    if m is None or (X, Y) in region:
                        continue
                    st, grp = [(X, Y)], []
                    region[(X, Y)] = None
                    while st:
                        a, c = st.pop()
                        grp.append((a, c))
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            u, v = a + dx, c + dy
                            if 0 <= u < P.w and 0 <= v < P.h and (u, v) not in region and mat(P.px[v][u]) == m:
                                region[(u, v)] = None
                                st.append((u, v))
                    xs, ys = [a for a, _ in grp], [c for _, c in grp]
                    box = (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
                    for g in grp:
                        region[g] = box
            claimed = {}
            for Y in range(P.h):
                for X in range(P.w):
                    p = P.px[Y][X]
                    if not p or p[2] is None or p[2] not in todo:
                        continue
                    row, idx, t, k = p
                    m = mat(p)
                    if m is None:
                        continue
                    edge = any(not (0 <= X + dx < P.w and 0 <= Y + dy < P.h) or mat(P.px[Y + dy][X + dx]) != m
                               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if edge:
                        continue
                    lad = ladder(town, row, m)
                    if len(lad) < 2:
                        continue
                    base = lad.index(idx) / (len(lad) - 1)
                    rx, ry, rw, rh = region[(X, Y)]
                    lv = style[m](X - rx, Y - ry, rw, rh, X, Y, base)
                    keep = KEEP_LIGHT_TOWN.get((town.ts, m), KEEP_LIGHT.get(m, 0.35))
                    lv = max(0.0, min(1.0, (1 - keep) * lv + keep * base))
                    claimed.setdefault(t, {})[k] = lad[int(round(lv * (len(lad) - 1)))]
            for t, pix in claimed.items():
                for k, v in pix.items():
                    new[t][k] = v
                what[t] = "%s %s" % (obj["map"], "@%d,%d" % tuple(obj["box"][:2]))
        todo -= set(what)
    return new, what


# ================================================================== seams (engine.md trap 14), by gbaseams' own rule
def seams(town, new):
    """(cells wrong today, cells wrong with the draft, the lines the draft adds) across every connection"""
    import contextlib
    saved = sys.argv
    sys.argv = [saved[0]]
    try:
        import gbaseams as S
    finally:
        sys.argv = saved
    S.FILTER = ""
    orig = S.Tileset.__init__

    def run(override):
        def init(self, symbol):
            orig(self, symbol)
            if override is not None and os.path.basename(S.tdir(symbol)) == town.ts:
                img = Image.new("P", (self.w, self.h))
                o = img.load()
                for t, p in enumerate(override):
                    for k, v in enumerate(p):
                        x, y = (t % 16) * 8 + k % 8, (t // 16) * 8 + k // 8
                        if y < self.h:
                            o[x, y] = v
                self.px = o
        S.Tileset.__init__ = init
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                n = S.main()
        finally:
            S.Tileset.__init__ = orig
        return n, set(l.rstrip() for l in buf.getvalue().splitlines() if l.strip() and "draw wrong" not in l)

    a, la = run(None)
    b, lb = run(new)
    return a, b, sorted(lb - la)


# ================================================================== pictures
def render(town, mapname, tiles=None, box=None):
    l = layouts()[mapname]
    G = general()
    tl = tiles or town.now
    allp = [G["pals"][r] for r in range(7)] + [town.pals[r] for r in range(7, 16)]
    W, H = l["width"], l["height"]
    g = town.grid[mapname]
    x0, y0, w, h = box or (0, 0, W, H)
    w, h = min(w, W - x0), min(h, H - y0)
    img = Image.new("RGB", (w * 16, h * 16), allp[0][0])
    o = img.load()
    for yy in range(h):
        for xx in range(w):
            m = g[(y0 + yy) * W + x0 + xx]
            buf, k = (G["mt"], m) if m < 640 else (town.mt, m - 640)
            if (k + 1) * 16 > len(buf):
                continue
            e = entries(buf, k)
            for layer in (0, 1):
                for q in range(4):
                    v = e[layer * 4 + q]
                    t, row = v & 0x3FF, v >> 12
                    src = G["tiles"][t] if t < 640 else (tl[t - 640] if t - 640 < len(tl) else [0] * 64)
                    for ty in range(8):
                        for tx in range(8):
                            sx = 7 - tx if v & 0x400 else tx
                            sy = 7 - ty if v & 0x800 else ty
                            c = src[sy * 8 + sx]
                            if c:
                                o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = allp[row][c]
    return img


def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


BG = (236, 234, 226)


def _label(im, text, f, pad=4):
    lines = text.split("\n")
    h = (f.size + 3) * len(lines) + pad * 2
    out = Image.new("RGB", (max(im.width, 10), im.height + h), BG)
    d = ImageDraw.Draw(out)
    for k, l in enumerate(lines):
        d.text((pad, pad + k * (f.size + 3)), l, font=f, fill=(30, 30, 30))
    out.paste(im, (0, h))
    return out


def _row(ims, gap=12):
    out = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1), max(i.height for i in ims)), BG)
    x = 0
    for i in ims:
        out.paste(i, (x, 0))
        x += i.width + gap
    return out


def _col(ims, gap=12, pad=12):
    out = Image.new("RGB", (max(i.width for i in ims) + pad * 2, sum(i.height for i in ims) + gap * (len(ims) - 1)
                            + pad * 2), BG)
    y = pad
    for i in ims:
        out.paste(i, (pad, y))
        y += i.height + gap
    return out


def _title(text, f, w):
    lines = text.split("\n")
    im = Image.new("RGB", (w, (f.size + 5) * len(lines) + 6), BG)
    d = ImageDraw.Draw(im)
    for k, l in enumerate(lines):
        d.text((2, 3 + k * (f.size + 5)), l, font=f, fill=(20, 20, 20))
    return im


def _wrap(text, n):
    out, line = [], ""
    for w in text.split():
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


#  the crops each drafted town is shown on: (map, x, y, w, h, what)
CROPS = {
    "viridian_city": [("Route22", 0, 0, 16, 10, "ROUTE 22's gate to UMBRA"),
                      ("ViridianCity", 20, 5, 14, 17, "the green house's hatch, the tower block's planters")],
    "pewter_city": [("PewterCity", 10, 0, 28, 13, "the ERRATA museum and its annex"),
                    ("PewterCity", 4, 24, 16, 9, "a slate-roofed house")],
    "cerulean_city": [("Route24", 5, 14, 14, 26, "ROUTE 24's long bridge"),
                      ("CeruleanCity", 6, 20, 14, 12, "the bike shop"),
                      ("Route25", 44, 0, 14, 7, "the sea cottage")],
    "viridian_forest": [("ViridianForest", 0, 0, 26, 16, "THE UNDERTONE's mouth"),
                        ("ViridianForest", 14, 28, 24, 18, "deep in the maze"),
                        ("SixIsland_PatternBush", 0, 0, 24, 14, "THE SAME BUSH (SIX ISLAND) shares it")],
}


def plan_of(ts):
    return next(p for p in PLAN if p["ts"] == ts)


def map_sheet(town, new, crop, path):
    name, x0, y0, w, h, what = crop
    p = plan_of(town.ts)
    a = render(town, name, box=(x0, y0, w, h))
    b = render(town, name, tiles=new, box=(x0, y0, w, h))
    f, F = font(13), font(17)
    z2 = lambda im: im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    rows = [_row([_label(a, "today 1x", f), _label(b, "draft 1x", f)]),
            _row([_label(z2(a), "today 2x", f), _label(z2(b), "draft 2x", f)])]
    sheet = _col([_title("T-438 batch F DRAFT -- %s: %s\n%s, cells %d,%d %dx%d -- footprints, blocks, collision, "
                         "palettes unchanged" % (p["name"], what, name, x0, y0, w, h), F,
                         max(r.width for r in rows))] + rows)
    sheet.save(path)
    return path


def atlas(town, tiles, mark=None, Z=3):
    n = len(tiles)
    rows = collections.defaultdict(collections.Counter)
    for b in range(town.nblocks):
        for v in entries(town.mt, b):
            if v & 0x3FF >= 640:
                rows[(v & 0x3FF) - 640][v >> 12] += 1
    im = Image.new("RGB", (16 * 8 * Z, ((n + 15) // 16) * 8 * Z), (255, 0, 255))
    o = im.load()
    for t in range(n):
        r = rows[t].most_common(1)[0][0] if rows[t] else 8
        pal = town.palette(r)
        for k, v in enumerate(tiles[t]):
            if v:
                x, y = (t % 16) * 8 + k % 8, (t // 16) * 8 + k // 8
                for a in range(Z):
                    for c in range(Z):
                        o[x * Z + a, y * Z + c] = pal[v]
    if mark:
        d = ImageDraw.Draw(im)
        for t in mark:
            x, y = (t % 16) * 8 * Z, (t // 16) * 8 * Z
            d.rectangle([x, y, x + 8 * Z - 1, y + 8 * Z - 1], outline=(220, 0, 0))
    return im


def tiles_sheet(town, new, what, path):
    f, F = font(12), font(17)
    p = plan_of(town.ts)
    changed = sorted(t for t in range(len(new)) if new[t] != town.now[t])
    by = collections.Counter("general (batch C's)" if w == "general" else "by role" for w in what.values())
    top = _row([_label(atlas(town, town.now, town.targets), "tiles.png today -- red: still vanilla, drawn "
                       "by a reachable map", f),
                _label(atlas(town, new, changed), "draft: %d tiles redrawn (%s)" % (
                    len(changed), ", ".join("%s %d" % kv for kv in sorted(by.items()))), f)])
    sheet = _col([_title("T-438 batch F DRAFT -- %s: the tileset (rows unchanged)\n%s" % (
        p["name"], "\n".join(_wrap(p["look"], 110))), F, top.width), top])
    sheet.save(path)
    return path


def plan_sheet(census, path):
    """every town in the order a player meets it: what is left, by object, and the look proposed"""
    f, F, H = font(13), font(15), font(20)
    blocks = []
    for k, p in enumerate(PLAN, 1):
        c = census[p["ts"]]
        lines = ["%d. %s (%s)%s -- %d%% of what its maps draw from it is still vanilla: %d tiles, %d objects" % (
            k, p["name"], p["ts"], "  [DRAFTED here]" if p["ts"] in DRAFTED else "", c["pct"], c["tiles"],
            c["nobj"])]
        lines += ["     " + l for l in _wrap("theme: " + p["theme"], 120)]
        lines += ["     " + l for l in _wrap("look:  " + p["look"], 120)]
        for name, draws in c["named"]:
            lines.append("       - %-70s %5d tile draws" % (name, draws))
        blocks.append(_title("\n".join(lines), f, 1180))
        if c.get("thumbs"):
            blocks.append(_row(c["thumbs"], gap=8))
    sheet = _col([_title("T-438 batch F -- the town leftovers and the forests: the plan (re-measured against "
                         "engine HEAD)\nin the order a player meets them; 'objects' are touching cells that draw a "
                         "leftover tile;\ndoors stay (gbadoors derives them); unused layouts (RS_*, Prototype isles) "
                         "are not counted", H, 1180)] + blocks, gap=8)
    sheet.save(path)
    return path


# ================================================================== the census
def census(thumbs=False):
    out = {}
    for p in PLAN:
        town = Town(p["ts"])
        v, tot = town.share()
        objs = town.objects()
        named = collections.OrderedDict()
        for o in objs:
            key = "%s@%d,%d" % (o["map"], o["box"][0], o["box"][1])
            nm = p["objects"].get(key) or p["objects"].get(o["map"] + "@*") or p["objects"].get("*", "other")
            named[nm] = named.get(nm, 0) + o["draws"]
        th = []
        if thumbs:
            for o in objs[:6]:
                x, y, w, h = o["box"]
                w, h = min(w + 2, 16), min(h + 2, 10)
                th.append(render(town, o["map"], box=(max(0, x - 1), max(0, y - 1), w, h)))
        out[p["ts"]] = dict(pct=round(100 * v / max(tot, 1)), tiles=len(town.left), nobj=len(objs),
                            doors=len(town.left & town.door_tiles), named=list(named.items()), thumbs=th,
                            maps=town.maps)
    return out


# ================================================================== the work
def write_draft(outdir):
    os.makedirs(outdir, exist_ok=True)
    sheets_dir = SHEETS
    os.makedirs(sheets_dir, exist_ok=True)
    made = [plan_sheet(census(True), os.path.join(sheets_dir, "t438f_plan.png"))]
    info = {}
    for ts in DRAFTED:
        town = Town(ts)
        new, what = redraw(town)
        moved = [t for t in range(len(new)) if any((a == 0) != (b == 0) for a, b in zip(new[t], town.now[t]))]
        if moved:
            raise SystemExit("  !! %s: tiles %s change their footprint" % (ts, moved[:10]))
        d = os.path.join(outdir, ts)
        os.makedirs(d, exist_ok=True)
        im = town.im.copy().convert("P")
        flat = [c for rgb in town.pals[8] for c in rgb]
        im.putpalette(flat)
        px = im.load()
        for t, p in enumerate(new):
            for k, v in enumerate(p):
                px[(t % 16) * 8 + k % 8, (t // 16) * 8 + k // 8] = v
        im.save(os.path.join(d, "tiles.png"), bits=4)
        a, b, added = seams(town, new)
        changed = sorted(t for t in range(len(new)) if new[t] != town.now[t])
        info[ts] = dict(name=plan_of(ts)["name"], look=plan_of(ts)["look"], tiles_redrawn=len(changed),
                        from_general=sorted(t for t, w in what.items() if w == "general"),
                        by_role={t: w for t, w in what.items() if w != "general"},
                        left_vanilla=sorted(town.targets - set(changed)),
                        doors_kept=sorted(town.left & town.door_tiles),
                        seams=dict(today=a, draft=b, added=added), palettes_changed=[])
        s = SHORT[ts]
        made.append(tiles_sheet(town, new, what, os.path.join(sheets_dir, "t438f_%s_tiles.png" % s)))
        for k, crop in enumerate(CROPS[ts], 1):
            made.append(map_sheet(town, new, crop, os.path.join(sheets_dir, "t438f_%s_%d.png" % (s, k))))
    json.dump(dict(ticket="T-438 batch F", status="CALLOW, SLATE, DOLDRUM, THE UNDERTONE approved 2026-10-23 and built by --write "
                   "--approved; the rest are drafts",
                   drafted=info, plan=[{k: v for k, v in p.items()} for p in PLAN]),
              open(os.path.join(outdir, "groups.json"), "w"), indent=1, default=list)
    return made


def report():
    print("T-438 batch F -- the town leftovers and the forests (approved and built: %s)" % ", ".join(APPROVED))
    c = census()
    for k, p in enumerate(PLAN, 1):
        r = c[p["ts"]]
        print("\n  %2d. %-26s %-18s %3d%% vanilla of its draws, %3d tiles left, %2d objects, %d door tiles kept%s" % (
            k, p["name"], p["ts"], r["pct"], r["tiles"], r["nobj"], r["doors"],
            "  DRAFTED" if p["ts"] in DRAFTED else ""))
        for name, n in r["named"][:6]:
            print("        %-72s %6d draws" % (name, n))
        print("        look: " + "\n              ".join(_wrap(p["look"], 100)))
    print("\n  scanned %d maps" % sum(len(v["maps"]) for v in c.values()))
    for ts in DRAFTED:
        town = Town(ts)
        new, what = redraw(town)
        changed = sum(1 for t in range(len(new)) if new[t] != town.now[t])
        print("  draft %-18s %d tiles redrawn (%d from general's own), %d leftovers not redrawn" % (
            ts, changed, sum(1 for w in what.values() if w == "general"), len(town.targets - set(what))))


def main():
    if WRITE:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: --write needs --approved, and APPROVED must name the towns the user approved.")
            return 0
        for ts in APPROVED:
            town, _ = drawn_before(ts)
            new, what = redraw(town)
            if any((a == 0) != (b == 0) for t in range(len(new)) for a, b in zip(new[t], town.now[t])):
                raise SystemExit("  !! %s: a tile's footprint moved -- nothing written" % ts)
            if new == town.disk:
                print("  %s: already drawn (%d tiles), nothing to write" % (ts, len(what)))
                continue
            im = town.im.copy()
            px = im.load()
            for t, p in enumerate(new):
                for k, v in enumerate(p):
                    px[(t % 16) * 8 + k % 8, (t // 16) * 8 + k // 8] = v
            im.save(os.path.join(town.dir, "tiles.png"), bits=4)
            print("  wrote %s: %d tiles" % (ts, sum(1 for t in range(len(new)) if new[t] != town.disk[t])))
        return 0
    if DRAFT is not None:
        for p in write_draft(DRAFT):
            print("  wrote %s" % p)
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
