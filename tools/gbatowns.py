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
    python3 tools/gbatowns.py --only TS,TS         # (with --draft) only these towns; no plan sheet, groups.json kept
    python3 tools/gbatowns.py --write --approved   # into the engine: the approved towns' tiles.png (CALLOW, SLATE,
                                                   #   DOLDRUM, THE UNDERTONE, approved 2026-10-23; ARDOR, HALFTONE,
                                                   #   VERDIGRIS, BRAZEN approved 2026-10-23 with the revisions below).
                                                   #   Refuses without --approved. A town with PALETTE MOVES is skipped
                                                   #   unless --palettes is given too: then its moved .pal rows and its
                                                   #   metatiles.bin are written beside its tiles.png. Batch H (LURID,
                                                   #   QUICKSILVER, the islands, DENSE WOOD) approved 2026-10-24, and
                                                   #   with --palettes THE SAME BUSH's split (SPLITS_APPROVED).

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
  * no block, layer, flip, behaviour or collision bit moves. A palette change is the user's call: the ones the user
    asked for (2026-10-23) are PALETTE MOVES, listed in MOVES below, each one checked against every block and map that
    draws the indices it changes -- so a moved colour lands only where it was meant to.

PALETTE MOVES (the user, 2026-10-23: "move palette rows so each theme comes true"). Four kinds, all in MOVES:
  * "colours": a row's colours at some indices, each written before -> after (a Town read from disk after a write is
    read back as before, so the redraw always sees one palette and a second write is a no-op). Light-to-dark order is
    kept, so every ladder, and so every drawing, is the same before and after;
  * "rerow": the entries of the named blocks that draw in one of `src` rows draw in `dst` instead -- ARDOR's harbour
    lights and truck leave general's greys (rows 2/3, every map's) for ARDOR's own free row 11;
  * "reindex": after the redraw, these tiles' pixels at one index take another -- the PORT's green strip and the
    dojo's weed move to a free index so BRAZEN's green roofs can turn brass without them;
  * "tile": a tile two objects share is copied to a new slot at the end of the tileset and the named blocks' entries
    drawn in `row` point at the copy -- HALFTONE's flat roof middle (702) is also the tower base's grey, so the roofs
    get a copy to dot. One tile row (16 slots) added; no block moves.
They go into the draft folder (palettes/NN.pal, metatiles.bin beside tiles.png) and into the engine only with
--write --approved --palettes.

A tile vanilla copied from primary/general (a ledge's end, a fence post) and drew in rows 0..6 is not redrawn here: it
takes batch C's current drawing of the same general tile, flips and all, so it matches the ground around it.

NOT TOUCHED. The LANDMARKS (SCORN SOLUTIONS, the MANSION, USER TOWER, THE ANNEX's triangle): T-447 redraws them from
the story, so every tile their cells draw is kept, as KEEP_MAPS keeps TANOBY's. A grove's TELL (T-337: gbagrove.py's SECONDARY_TELL, THE UNDERTONE's tile 10) is never redrawn here;
after every redraw it is drawn again from its source tile's new pixels, so the little door stays on top of this art.
A DOOR's tiles (field_door.c's table): gbadoors.py derives each door's animation from its closed block, so
a door is redrawn by re-running gbadoors after a town is built. LAVENDER (HALFTONE) is grey by DaemonsIsHalftone() and
keeps T-430's rules -- its look below must still read in grey. Every palette row MOVES does not name.

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
PALETTES = "--palettes" in ARGS


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
         "viridian_forest": "undertone", "vermilion_city": "ardor", "lavender_town": "halftone",
         "celadon_city": "verdigris", "saffron_city": "brazen", "fuchsia_city": "lurid",
         "cinnabar_island": "quicksilver", "sevii_islands_123": "islands123", "sevii_islands_45": "islands45",
         "sevii_islands_67": "islands67", "berry_forest": "densewood"}
DRAFTED = ["viridian_city", "pewter_city", "cerulean_city", "viridian_forest",
           #  the next four, drafted 2026-10-23 in the order a player meets them (sheets t438f2_*)
           "vermilion_city", "lavender_town", "celadon_city", "saffron_city",
           #  batch H, drafted 2026-10-24 (sheets t438h_*): the rest of the places, first met first; not approved
           "fuchsia_city", "cinnabar_island", "sevii_islands_123", "sevii_islands_45", "sevii_islands_67",
           "berry_forest"]
#  which sheet set each draft belongs to (the first four were t438f_, the next four t438f2_, revised as t438f3_)
SHEET_PREFIX = {"vermilion_city": "t438f3", "lavender_town": "t438f3", "celadon_city": "t438f3",
                "saffron_city": "t438f3", "fuchsia_city": "t438h", "cinnabar_island": "t438h",
                "sevii_islands_123": "t438h", "sevii_islands_45": "t438h", "sevii_islands_67": "t438h",
                "berry_forest": "t438h"}
#  the user, 2026-10-23: build these four (SLATE's museum roof and CALLOW's cottage roof calmed first); the rest stay
#  drafts until approved
APPROVED = ["viridian_city", "pewter_city", "cerulean_city", "viridian_forest",
            #  the user, 2026-10-23: build ARDOR, HALFTONE, VERDIGRIS and BRAZEN with the revisions (MOVES below; the
            #  roofs dotted whole; the pantiles calmed a step more)
            "vermilion_city", "lavender_town", "celadon_city", "saffron_city",
            #  the user, 2026-10-24: build batch H -- LURID (the SAFARI canopy acid chartreuse, the pens neon fuchsia:
            #  both MOVES as drafted), QUICKSILVER (its sand left as it is; the MANSION and the lab are LANDMARKS, so
            #  all that is left is one tile copied from general's), the island kit with the harbour roofs' drying net
            #  (ONE..SEVEN; USER TOWER and THE ANNEX are LANDMARKS) and DENSE WOOD
            "fuchsia_city", "cinnabar_island", "sevii_islands_123", "sevii_islands_45", "sevii_islands_67",
            "berry_forest"]
#  the palette splits the user approved, and which option (SPLITS below): THE SAME BUSH's salt scrub, option A
#  (2026-10-24); --write --approved writes its rows 7..12 beside its base (the engine's header, palette table and
#  layout were wired by hand, as gTileset_CaveUmbral's were)
SPLITS_APPROVED = {"same_bush": 0}


# ================================================================== palette moves (the user, 2026-10-23)
def _q(h):
    """a colour as the GBA keeps it: five bits a channel, read back as the .pal files write them"""
    return tuple(((int(h[k:k + 2], 16) >> 3) << 3) | (int(h[k:k + 2], 16) >> 5) for k in (0, 2, 4))


def _cols(**kw):
    """{index: (before, after)} from i<n>="before after" """
    return {int(k.lstrip("i_"), 16): tuple(v.split()) for k, v in kw.items()}


#  the harbour lights (VermilionCity, both lights at 20..21 / 25..26, 32..34) and the truck on the quay
#  (SSAnne_Exterior 55..57, 1..3): every block of each, found by the cells that draw them
ARDOR_LIGHTS = [0x28d, 0x28e, 0x28f, 0x297, 0x29f, 0x2af, 0x2cf, 0x2d7, 0x2df, 0x2e7]
ARDOR_TRUCK = [0x313, 0x314, 0x315, 0x316, 0x317, 0x318, 0x319, 0x31a]
MOVES = {
    "vermilion_city": [
        dict(kind="colours", row=11, why="ARDOR's own row 11 was empty (every index magenta, no block draws it): "
                                         "now warm iron -- vanilla's greys at 1..7 warmed to iron, the truck's teal "
                                         "box (8, 9) to rust, the lamp's red band (12) and the truck's stripe (13) "
                                         "as they were",
             colours=_cols(i1="ff00ff eee6dc", i2="ff00ff cdbfb0", i3="ff00ff ac9a88", i4="ff00ff 8f7b6a",
                           i5="ff00ff 735f52", i6="ff00ff 584840", i7="ff00ff 3e322e", i8="ff00ff 7b3a24",
                           i9="ff00ff a85634", ia="ff00ff ffcd8b", ib="ff00ff ee9473", ic="ff00ff de6a62",
                           id="ff00ff cd524a", ie="ff00ff ac2029", i_f="ff00ff 9cdcd2")),
        dict(kind="rerow", blocks=ARDOR_LIGHTS, src=(2, 3), dst=11,
             why="the harbour lights leave general's greys (rows 2/3, drawn on every map) for row 11"),
        dict(kind="rerow", blocks=ARDOR_TRUCK, src=(2,), dst=11,
             why="the truck on the quay leaves general's row 2 for row 11"),
    ],
    "saffron_city": [
        dict(kind="colours", row=11, why="the green house roofs (general's ribbed roof, drawn in BRAZEN's row 11 "
                                         "at 10..14) in brass; 15 was free and keeps the old green for the two "
                                         "things that shared it (reindex below)",
             colours=_cols(ia="acdeb4 f6e69c", ib="8bbd94 e6c55a", ic="6a9c73 c59c39", id="52835a 9c7329",
                           ie="41734a 6a4a1c", i_f="ff00ff 8bbd94")),
        dict(kind="reindex", tiles=[777, 779, 782, 1013], row=11, map={11: 15, 13: 15},
             why="the PORT's green strip under its windows (777, 779, 782) and the dojo's weed (1013) keep the "
                 "green (index 15) while their old indices turn brass"),
        dict(kind="colours", row=8, why="the tower's purple wings (row 8, 13/14: drawn by its wings and nothing "
                                        "else; the doors' purple is 7..9 and stays) in gold",
             colours=_cols(id="a483cd cd9c31", ie="cda4ff ffde6a")),
    ],
    "celadon_city": [
        dict(kind="colours", row=12, why="the apartment blocks (row 12 is theirs alone): their flat roofs (general's "
                                         "grid, drawn here) from khaki to bronze gone green -- a verdigris patina, "
                                         "the grid's seams the deepest -- and the walls' pale mint a step deeper",
             colours=_cols(i2="d5dea4 a4dcc4", i3="b4bd83 62bc9c", i4="8b945a 2f8670",
                           ia="bde6de c4ecdc", ib="94cdb4 8bd5ba", ic="73ac94 5ab496", id="6a948b 41947c")),
        dict(kind="colours", row=9, why="the mansion's bloom (row 9, 9..11: the mansion's alone) to the same "
                                        "verdigris",
             colours=_cols(i9="bde6de acecd5", ia="83bda4 52c4a0", ib="6a948b 31947b")),
    ],
    "lavender_town": [
        dict(kind="tile", src=702, blocks=[0x290, 0x291, 0x294], row=12,
             why="the roofs' flat middle (702, vanilla's, all one index) is also the tower base's grey (row 9, ten "
                 "blocks): the roofs get their own copy to dot, the tower keeps 702"),
    ],
    #  batch H (drafted 2026-10-24, the rest of the places in the order a player meets them; NOT approved)
    "fuchsia_city": [
        dict(kind="colours", row=11, why="the SAFARI's canopy (row 11, 1..4: the SAFARI trees' leaves) from leaf "
                                         "green to a sickly acid glow -- chartreuse lit, a poison green body, the "
                                         "shade kept deep. The marsh teal (9, a, e) and the bark (6..8) stay",
             colours=_cols(i1="b4ee52 e2ff4a", i2="8bd552 b8f22a", i3="5aa431 6cc818", i4="395a5a 2c5848")),
        dict(kind="colours", row=9, why="the pens' mint walls (row 9, a..e: their tops, faces and dark rims) as "
                                        "neon fuchsia -- LURID's own name for the colour, the tube lit pale, the "
                                        "face hot pink, the rims deep plum; the pens' fences and plaques (1..9) "
                                        "stay",
             colours=_cols(ia="31625a 6a1a58", ib="4a9483 b0288f", ic="52c594 ee4ec8", id="6ae6ac ff8ae8",
                           ie="a4eeac ffc8f4")),
    ],
    #  QUICKSILVER's two drafted moves (the lab's cream walls as quicksilver, row 9; the MANSION's roof scorched,
    #  row 8) are not built: both are LANDMARKS, which T-447 redraws from the story (the user, 2026-10-24)
}
for _ms in MOVES.values():                     # i_f: `if` is a keyword
    for _m in _ms:
        if "colours" in _m:
            _m["colours"] = {k: (tuple(int(a[j:j + 2], 16) for j in (0, 2, 4)), _q(b))
                             for k, (a, b) in _m["colours"].items()}


#  tiles never redrawn, whatever they match: BRAZEN's PORT sign (789, 804, 805, 807) is drawn from tiles that copy
#  general's signboard, so the general rule gave it batch C's signboard and scrambled the round sign (the first
#  draft's PORT read "EP13"; the user, 2026-10-23: keep the PORT's round sign intact)
KEEP_TILES = {"saffron_city": {789, 804, 805, 807},
              #  the dark hollows under the canopy where a path enters the trees (BOND BRIDGE, GREEN PATH): their
              #  tiles match general tiles batch C redrew for something else, and the rule flattened the hollow's
              #  leafy rim (batch H draft, 2026-10-24) -- kept as vanilla drew them
              "sevii_islands_123": {640 + 333, 640 + 336, 640 + 337, 640 + 338},
              "sevii_islands_67": {640 + 333, 640 + 336, 640 + 338}}
#  maps whose tiles are left for a later batch: every tile these maps draw is kept, wherever else it is drawn
#  (TANOBY's seven chamber doors wait for batch G, the user 2026-10-23)
KEEP_MAPS = {"sevii_islands_67": ["SevenIsland_TanobyRuins"]}
#  LANDMARKS: places T-447 redraws from the story later, so this tool leaves them exactly as they are (the user,
#  2026-10-24, building batch H). Each is a box of cells on one map (the census's object for it); every tile a block in
#  the box draws is kept, wherever else that tile is drawn, so no write of this tool can change a pixel of one -- and
#  no palette move here touches a row they draw (QUICKSILVER's two drafted moves, the lab's quicksilver walls and the
#  MANSION's ash roof, were dropped for that).
LANDMARKS = {
    "cinnabar_island": [("CinnabarIsland", 5, 0, 7, 5, "the MANSION"),
                        ("CinnabarIsland", 5, 6, 7, 4, "SCORN SOLUTIONS (the lab)")],
    "sevii_islands_67": [("SevenIsland_TrainerTower", 54, 0, 9, 9, "USER TOWER"),
                         ("BirthIsland_Exterior", 10, 7, 11, 9, "THE ANNEX's triangle")],
    #  T-447's second pair (drafted 2026-10-24): CORPUS's tower, and its copy on the crossings' layout; DAEMON TOWER,
    #  whose top is ROUTE 10's rows 72..79
    "saffron_city": [("SaffronCity", 29, 16, 9, 15, "CORPUS's tower"),
                     ("SaffronCity_Connection", 19, 9, 9, 15, "CORPUS's tower (the crossings' copy)")],
    "lavender_town": [("LavenderTown", 15, 0, 7, 7, "DAEMON TOWER"),
                      ("Route10", 15, 72, 7, 8, "DAEMON TOWER (its top, on ROUTE 10)")],
    #  T-447's third pair (drafted 2026-10-25): the REVIEW BOARD on UMBRA, and ERRATA with its annex in SLATE
    "indigo_plateau": [("IndigoPlateau_Exterior", 6, 0, 11, 7, "the REVIEW BOARD")],
    "pewter_city": [("PewterCity", 12, 0, 16, 7, "ERRATA, the museum and its annex")],
}


def grove_tell(ts):
    """T-337's grove tell in this tileset: {tile: (the tile it is drawn from, {(x, y): colour index})}, read from
    tools/gbagrove.py's SECONDARY_TELL (THE UNDERTONE's and the BERRY FOREST's big tree, a little door down its trunk).
    The tell is gbagrove's, not this tool's: its tiles are never redrawn here, and after every redraw each is drawn
    again from its source tile's NEW pixels, so the door stays on top of this tool's art (batch F redrew the trunk,
    tile 84, and left the tell a copy of vanilla's: check_generators --writes found gbagrove drifting)."""
    import gbagrove
    for sub, tiles, _ in gbagrove.SECONDARY_TELL.values():
        if sub == "secondary/" + ts:
            return tiles
    return {}


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def apply_pre(town):
    """the moves that come before the redraw: colours (read back to `before` first, then set), rerows, tile copies.
    Returns what each did, for the sheets"""
    did = []
    for mv in MOVES.get(town.ts, []):
        if mv["kind"] == "colours":
            pal = town.pals[mv["row"]]
            five = lambda c: tuple(x >> 3 for x in c)
            for i, (a, b) in mv["colours"].items():
                if five(pal[i]) not in (five(a), five(b)):
                    raise SystemExit("  !! %s row %d index %d is %s: neither the move's before nor after" % (
                        town.ts, mv["row"], i, pal[i]))
            #  every material's ladder keeps its light-to-dark order, so the redraw is the same before and after
            for mat in set(MATERIALS.get(town.ts, {}).get(mv["row"], {}).values()):
                ix = [i for i, m in MATERIALS[town.ts][mv["row"]].items() if m == mat]
                col = lambda i, k: mv["colours"][i][k] if i in mv["colours"] else pal[i]
                if sorted(ix, key=lambda i: (-lum(col(i, 0)), i)) != sorted(ix, key=lambda i: (-lum(col(i, 1)), i)):
                    raise SystemExit("  !! %s row %d: the move reorders %s's ladder" % (town.ts, mv["row"], mat))
            for i, (a, b) in mv["colours"].items():
                pal[i] = b
            did.append(mv)
        elif mv["kind"] == "rerow":
            mt = bytearray(town.mt)
            n = 0
            for blk in mv["blocks"]:
                for q in range(8):
                    o = (blk - 640) * 16 + q * 2
                    v = struct.unpack_from("<H", mt, o)[0]
                    if v >> 12 in mv["src"]:
                        struct.pack_into("<H", mt, o, (v & 0x0FFF) | (mv["dst"] << 12))
                        n += 1
            town.mt = bytes(mt)
            did.append(dict(mv, entries=n))
        elif mv["kind"] == "tile":
            src = mv["src"] - 640
            mt = bytearray(town.mt)
            new = None
            for blk in mv["blocks"]:                    # already copied (read from disk after a write)?
                for q in range(8):
                    v = struct.unpack_from("<H", mt, (blk - 640) * 16 + q * 2)[0]
                    if v >> 12 == mv["row"] and (v & 0x3FF) - 640 >= len(town.van):
                        new = (v & 0x3FF) - 640
            if new is None:
                new = len(town.now)
                town.now.append(list(town.now[src]))
                town.disk.append(list(town.disk[src]))
            while len(town.van) <= new:                 # the copy's vanilla is its source's
                town.van.append(list(town.van[src]))
            n = 0
            for blk in mv["blocks"]:
                for q in range(8):
                    o = (blk - 640) * 16 + q * 2
                    v = struct.unpack_from("<H", mt, o)[0]
                    if v >> 12 == mv["row"] and (v & 0x3FF) == mv["src"]:
                        struct.pack_into("<H", mt, o, (v & 0xFC00) | (640 + new))
                        n += 1
            town.mt = bytes(mt)
            did.append(dict(mv, new=640 + new, entries=n))
        elif mv["kind"] == "reindex":                   # done after the redraw (apply_post); listed for the sheets
            did.append(mv)
    return did


def apply_post(town, new):
    """the moves that come after the redraw: reindexed pixels. Idempotent (no target index is also a source)"""
    for mv in MOVES.get(town.ts, []):
        if mv["kind"] == "reindex":
            assert not set(mv["map"].values()) & set(mv["map"])
            for t in mv["tiles"]:
                new[t - 640] = [mv["map"].get(c, c) for c in new[t - 640]]
    for t, (src, edits) in grove_tell(town.ts).items():      # T-337: gbagrove's tell, over the new trunk
        new[t] = [edits.get((k % 8, k // 8), new[src][k]) for k in range(64)]
    return new


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

    def __init__(self, ts, moved=False):
        """moved: with the town's PALETTE MOVES applied (its colours, rerows and tile copies; reindexes come after the
        redraw). Without, the town as the engine has it today"""
        self.ts = ts
        self.dir = os.path.join(GBA, SEC + ts)
        self.im = Image.open(os.path.join(self.dir, "tiles.png"))
        self.now = tiles_of(self.im)
        self.van = tiles_of(Image.open(io.BytesIO(daemonslib.upstream(GBA, SEC + ts + "/tiles.png", binary=True))))
        self.pals = [read_pal(os.path.join(self.dir, "palettes/%02d.pal" % r)) for r in range(16)]
        self.mt = open(os.path.join(self.dir, "metatiles.bin"), "rb").read()
        self.nblocks = len(self.mt) // 16
        self.disk = [list(t) for t in self.now]
        self.mt_disk = self.mt
        self.moves = apply_pre(self) if moved else []
        sym = "gTileset_" + camel(ts)
        want = re.sub(r"[^a-z0-9]", "", ts)
        #  a palette split's maps count as its base's (THE SAME BUSH, gTileset_SameBush, draws THE UNDERTONE's tiles
        #  and metatiles), so the split leaves where each tile is drawn -- and so how it is drawn -- as it was
        self.maps = sorted(n for n, l in layouts().items()
                           if re.sub(r"[^a-z0-9]", "", daemonslib.tileset_base(GBA, l["secondary_tileset"])
                                     .replace("gTileset_", "").lower()) == want
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
        self._leftovers()

    def _leftovers(self):
        nb = lambda t: any(self.now[t])
        self.left = {t for t in range(min(len(self.van), len(self.now)))
                     if self.now[t] == self.van[t] and nb(t) and self.draws[t]}
        self.targets = self.left - self.door_tiles - {t - 640 for t in KEEP_TILES.get(self.ts, ())} - \
            set(grove_tell(self.ts)) - self.kept_by_map()

    def kept_by_map(self):
        """every tile a KEEP_MAPS map draws (TANOBY's chamber doors, batch G), and every tile a LANDMARKS box draws"""
        out = set()
        blocks = set()
        for m in KEEP_MAPS.get(self.ts, ()):
            blocks |= set(self.grid.get(m, ()))
        for m, x0, y0, w, h, _ in LANDMARKS.get(self.ts, ()):
            W = layouts()[m]["width"]
            blocks |= {self.grid[m][y * W + x] for y in range(y0, y0 + h) for x in range(x0, x0 + w)}
        for b in blocks:
            if 640 <= b < 640 + self.nblocks:
                out |= {(v & 0x3FF) - 640 for v in entries(self.mt, b - 640) if v & 0x3FF >= 640}
        return out

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
    #  the second four (drafted 2026-10-23, in the order a player meets them)
    "vermilion_city": {
        8: {2: "roof", 3: "roof", 4: "roof", 10: "wall", 11: "wall", 12: "wall"},
        12: {12: "hallroof", 13: "hallroof", 14: "hallroof", 15: "hallroof", 1: "wall", 2: "wall", 3: "wall"},
        10: {2: "crate", 3: "crate", 4: "crate", 8: "leaf", 9: "leaf", 10: "leaf"},
        9: {1: "awning", 2: "awning", 3: "awning", 4: "awning"},
        #  the harbour lights (rows 2/3, general's greys) are left: "warm iron" needs a warm colour those rows do not
        #  have -- a palette question for the user
    },
    "lavender_town": {
        8: {7: "plank", 8: "plank", 9: "plank", 10: "plank", 11: "plank", 12: "plank"},
        12: {2: "roof", 3: "roof", 4: "roof", 10: "roof", 11: "roof", 12: "roof", 13: "roof",
             8: "wall", 9: "wall", 14: "wall", 15: "wall"},
        10: {13: "roof", 14: "roof", 15: "roof", 7: "glass", 8: "glass", 9: "glass"},
        11: {7: "glass", 8: "glass", 9: "glass"},
        9: {9: "dome", 10: "dome", 11: "dome", 12: "dome", 13: "dome", 14: "dome", 15: "dome",
            3: "wall", 4: "wall"},
    },
    "celadon_city": {
        11: {7: "road", 8: "road", 10: "road"},
        12: {2: "bronze", 3: "bronze", 4: "bronze", 10: "bloom", 11: "bloom", 12: "bloom", 13: "bloom"},
        9: {12: "bronze", 13: "bronze", 15: "bronze", 9: "bloom", 10: "bloom", 11: "bloom"},
        10: {14: "trim", 15: "trim", 10: "glass", 11: "glass", 12: "glass"},
    },
    "saffron_city": {
        12: {6: "brass", 7: "brass", 9: "brass", 10: "brass", 11: "brass"},
        10: {9: "plaza", 10: "plaza", 11: "plaza", 6: "paving", 7: "paving", 8: "paving"},
        8: {13: "curtain", 14: "curtain"},
        9: {12: "curtain", 13: "curtain", 14: "curtain"},
        #  the north row's PORT roof (row 5, general's khaki) is left: its indices also draw the PORT's round sign,
        #  which a motif would scramble
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


#  ---- the second four. A motif may answer (level, other material): the pixel then takes that material's ladder in
#  the same row -- how VERDIGRIS's bronze blooms green where the rain runs off it.
def m_pantile(x, y, w, h, X, Y, b):
    """ARDOR: hot glazed pantiles, calmed a step more for 1x (the user, 2026-10-23: "closer to SLATE's calm") -- as
    SLATE's museum roof: courses eight rows tall laid in the glaze's own light, and only one step of shade -- the lap
    under each course, and a short shadow down the side of each roll in the lower half of the course. No stripe the
    course's height, no joint, nothing two steps from the body"""
    xo, yy = X % 8, Y % 8
    if yy == 7 or (xo == 7 and yy >= 4):
        return 0.34
    return 0.0


def m_pantile_deep(x, y, w, h, X, Y, b):
    """the hall's green pantiles: the same calm courses one step deeper, so the green stays green (its lightest is
    nearly white)"""
    return m_pantile(x, y, w, h, X, Y, b) + 0.33


def m_stucco(x, y, w, h, X, Y, b):
    """ARDOR's walls: sun on plaster -- a bleached top, a flat body, a warm shade along the foot"""
    if y < 2:
        return 0.0
    if y >= h - 2:
        return 1.0
    return 0.35


def m_awning_wide(x, y, w, h, X, Y, b):
    """sun-bleached canvas, stripes four wide (vanilla's were two), a shaded hem"""
    if y >= h - 1:
        return 1.0
    return 0.0 if (X // 4) % 2 == 0 else 0.67


def m_iron(x, y, w, h, X, Y, b):
    """warm iron (the harbour bollards and lights): lit from the left, a band every six rows"""
    if Y % 6 == 5:
        return 1.0
    return 0.15 + 0.6 * (x / max(w - 1, 1))


def m_dots(x, y, w, h, X, Y, b):
    """HALFTONE: a dot screen -- light dots on the dark, big where vanilla is light and small where it is dark, so
    it reads as vanilla's own tone from across the screen and as dots up close. Four-pixel pitch, every other row of
    dots shifted by two. Vanilla's darkest (the gaps between planks, the outlines inside a surface) are kept, so the
    boards stay boards"""
    if b >= 0.9:
        return b
    j = Y // 4
    cx = (X - (2 if j % 2 else 0)) % 4
    cy = Y % 4
    d = ((cx - 1.5) ** 2 + (cy - 1.5) ** 2) ** 0.5
    r = 2.26 * max(0.0, 1.0 - b) ** 0.5                # a dot's area is the light vanilla had there
    return 0.2 if d < r else 0.8


def m_dots_light(x, y, w, h, X, Y, b):
    """the dot screen on the light half only: a pale wall's louvres and panes, which are its drawing, are kept"""
    return b if b >= 0.5 else m_dots(x, y, w, h, X, Y, b)


def m_streak(x, y, w, h, X, Y, b):
    """VERDIGRIS's cycling road, THE STREAK: lanes smeared lengthwise -- long unbroken streaks a lane wide, a few
    lighter, a few darker, and the lanes marked by a dashed line every sixteen pixels. Nothing runs across, so the
    block repeats down the road without a seam"""
    if x % 16 == 0 and 0 < x < w - 1:
        return 0.0 if Y % 16 < 8 else 0.5
    k = _h(x // 3, 17)
    return 0.15 if k < 0.2 else (0.85 if k > 0.85 else 0.5)


def m_bronze(x, y, w, h, X, Y, b):
    """VERDIGRIS: bronze sheet with a standing seam every eight, furred green where the rain runs (the user,
    2026-10-23: more verdigris) -- a deep bloom along the drip edge, a run down from every seam from a third of the
    way down, and a second, shorter run beside every other one"""
    if y >= h - 3:
        return ((0.33, 0.5, 0.67)[y - (h - 3)], "bloom")
    if X % 8 == 7 and y >= h // 3:
        return (0.5, "bloom")
    if X % 8 == 6 and y >= (2 * h) // 3 and _h(X // 8, 3) < 0.6:
        return (0.33, "bloom")
    if X % 8 == 7:
        return 1.0
    if y < 2:
        return 0.0
    return 0.45


def m_patina(x, y, w, h, X, Y, b):
    """green bloom on a wall: a wash, paler at the top, with the runs the rain leaves every eight pixels"""
    if X % 8 == 3 and _h(X // 8, 5) < 0.7:
        return 1.0
    return 0.15 + 0.5 * (y / max(h - 1, 1))


def m_band(x, y, w, h, X, Y, b):
    """a bronze trim: a lit upper edge, a dark body"""
    return 0.0 if y < max(1, h // 3) else 1.0


def m_rivet(x, y, w, h, X, Y, b):
    """BRAZEN: rolled brass sheet in courses of eight -- a lit roll along the top, a dark lap at the foot, and a
    rivet every eight pixels on the second line"""
    yy = Y % 8
    if yy == 7:
        return 0.75
    if yy == 0:
        return 0.0
    if yy == 2 and X % 8 == 4:
        return 1.0
    return 0.25


def m_grid(x, y, w, h, X, Y, b):
    """the corporate grid: every slab an identical square, eight by eight, a joint one step darker on two sides
    and nothing else (a full-dark joint read as graph paper over the whole plaza)"""
    if X % 8 == 7 or Y % 8 == 7:
        return 0.5
    return 0.0


def m_curtain(x, y, w, h, X, Y, b):
    """a curtain wall: a dark mullion every eight pixels, a transom every sixteen rows, the panes level and light"""
    if X % 8 == 0 or Y % 16 == 0:
        return 1.0
    return 0.0 if Y % 16 == 1 else 0.3


def m_stamped(x, y, w, h, X, Y, b):
    """stamped panels, 16 x 8: each a raised field, lit on its top and left, dark on its bottom and right"""
    xo, yo = X % 16, Y % 8
    if yo == 7 or xo == 15:
        return 1.0
    if yo == 0 or xo == 0:
        return 0.0
    if yo == 6 or xo == 14:
        return 0.75
    return 0.4


STYLE = {
    "vermilion_city": dict(roof=m_pantile, hallroof=m_pantile_deep, wall=m_stucco, crate=m_boards, leaf=m_leaf, awning=m_awning_wide,
                           ),
    "lavender_town": dict(plank=m_dots, roof=m_dots, wall=m_dots, glass=m_dots_light, dome=m_dots),
    "celadon_city": dict(road=m_streak, bronze=m_bronze, bloom=m_patina, trim=m_band, glass=m_glass),
    "saffron_city": dict(brass=m_rivet, plaza=m_grid, paving=m_grid, curtain=m_curtain, panels=m_stamped),
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
KEEP_LIGHT_TOWN = {("viridian_city", "roof"): 0.0, ("pewter_city", "roof"): 0.0,
                   ("vermilion_city", "roof"): 0.0, ("vermilion_city", "hallroof"): 0.0,
                   ("vermilion_city", "awning"): 0.0,
                   ("celadon_city", "road"): 0.0, ("celadon_city", "bronze"): 0.0,
                   ("saffron_city", "plaza"): 0.0, ("saffron_city", "paving"): 0.0, ("saffron_city", "brass"): 0.0,
                   ("saffron_city", "curtain"): 0.0, ("saffron_city", "panels"): 0.0}
#  HALFTONE's dot screen is two-tone by design: it carries vanilla's light in the dots' size, not in a blend
for _m in ("plank", "roof", "wall", "glass", "dome"):
    KEEP_LIGHT_TOWN[("lavender_town", _m)] = 0.0


# ================================================================== batch H: the rest, in the order a player meets them
#  (drafted 2026-10-24 from the plan sheet's looks; approved and built 2026-10-24, the landmarks left out)
def _lobe(X, Y, lobes, P):
    """the nearest leaf clump on a P-pixel grid: (distance / radius, dx, dy, radius)"""
    xo, yo = X % P, Y % P
    best = None
    for cx, cy, r in lobes:
        for ox in (-P, 0, P):
            for oy in (-P, 0, P):
                dx, dy = xo - cx - ox, yo - cy - oy
                d = (dx * dx + dy * dy) ** 0.5 / r
                if best is None or d < best[0]:
                    best = (d, dx, dy, r)
    return best


LOBES_GLOSSY = [(10, 9, 11.0), (24, 12, 10.0), (8, 25, 10.0), (24, 26, 11.0)]


def m_glossy(x, y, w, h, X, Y, b):
    """LURID: the SAFARI's canopy keeps vanilla's soft leaf masses (the acid glow is the palette move) and takes a
    glossy hot spot -- a bright oval at the upper left of each of four big clumps to every 32 pixels, as if the
    leaves were lacquered. Calm at 1x: one shape per clump, nothing else redrawn"""
    if b >= 0.9:
        return b
    d, dx, dy, r = _lobe(X, Y, LOBES_GLOSSY, 32)
    lit = (dx + dy) / (2 * r)
    if d < 0.42 and lit < -0.1:
        return 0.0
    return b


LOBES_DENSE = [(4, 4, 4.2), (11, 3, 4.0), (8, 9, 4.4), (3, 12, 4.0), (13, 11, 4.2), (8, 15, 3.6)]


def m_dense(x, y, w, h, X, Y, b):
    """DENSE WOOD: THE UNDERTONE's clumps, but six smaller ones to every 16 pixels -- packed tight, each lit at its
    upper left and rimmed one step darker at its foot, the body kept in the berry trees' own warm yellow, so they read
    thicker than THE UNDERTONE's without going dark"""
    if b >= 0.9:
        return b
    d, dx, dy, r = _lobe(X, Y, LOBES_DENSE, 16)
    if d > 0.85 and dy > 0:
        return 0.6
    lit = (dx + dy) / (2 * r)
    return 0.0 if lit < -0.1 else 0.3


def m_weatherboard(x, y, w, h, X, Y, b):
    """the islands' roofs in sea-weathered board: boards eight wide running down the roof, a joint one step darker,
    one board in three bleached a step lighter by salt; vanilla's lit ridge kept (its light ribs go). Calm at 1x: one step, no stripe"""
    if b < 0.3 and y < 10:
        return b
    if X % 8 == 7:
        return 1.0
    return 0.5 if _h(X // 8, 41) < 0.3 else 0.75


def m_net(x, y, w, h, X, Y, b):
    """the harbours' red roofs as nets drying: the roof flat in its body red under a lit ridge, a net draped over
    the lower half as a loose diamond mesh one step darker; vanilla's light ribs go (a rib under a net is a stripe
    too many), its dark eave stays. A small region (the red girders beside the house) keeps
    vanilla's drawing"""
    if w < 24 or b >= 0.9:
        return b
    if y < 2:
        return 0.25
    if y > h * 0.4 and ((X + Y) % 8 == 0 or (X - Y) % 8 == 0):
        return 0.75
    return 0.5


def m_rings(x, y, w, h, X, Y, b):
    """the NET centre's roof: the bright orange body, with the dish's signal running out over it as wide rings one
    step darker, centred on the dish at the roof's foot"""
    cx, cy = (w - 1) / 2.0, h + 2.0
    r = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
    return 0.5 if int(r) % 7 == 0 else 0.0


def m_facets(x, y, w, h, X, Y, b):
    """THE ANNEX's triangle as shards: 16-pixel facets split on a diagonal, one half lit, one half a step deeper,
    the diagonal turned by cell so it reads as broken glass laid flat -- no lines drawn"""
    xo, yo = X % 16, Y % 16
    flip = _h(X // 16, Y // 16, 7) < 0.5
    up = (xo + yo < 16) if flip else (xo < yo)
    return 0.25 if up else 0.6


def m_curtain_glint(x, y, w, h, X, Y, b):
    """USER TOWER's glass curtain: a dark mullion every eight pixels, a transom every sixteen rows, the panes level,
    and a sky glint crossing them on the diagonal"""
    if X % 8 == 0 or Y % 16 == 0:
        return 1.0
    if (X + Y) % 32 in (3, 4, 5):
        return 0.2
    return 0.6


def m_cairn(x, y, w, h, X, Y, b):
    """SOMEONE'S STONE as river stones stacked: courses five rows tall, each a rounded stone lit on top and dark
    under its lip, the courses' ends turned in. Only a tall narrow region is the stone: the harbour house draws the
    same greys in its walls, and keeps vanilla's drawing"""
    if w > 40 or h < 24:
        return b
    yy = Y % 5
    if yy == 4:
        return 1.0
    edge = min(x, w - 1 - x) < 2
    return (0.0, 0.25, 0.5, 0.75)[yy] + (0.25 if edge and yy < 3 else 0.0)


def m_pebble(x, y, w, h, X, Y, b):
    """a smooth river stone: lit from the upper left, three steps"""
    t = (x / max(w - 1, 1) + y / max(h - 1, 1)) / 2
    return 0.0 if t < 0.3 else (0.5 if t < 0.7 else 1.0)


def m_mercury(x, y, w, h, X, Y, b):
    """QUICKSILVER's lab: liquid-bright metal -- a smooth body darkening down the wall, one bright sheen every
    sixteen pixels, and at the foot a pool of it, its bright meniscus bulging over the darker metal beneath"""
    top = h - 3 - (1 if _h(X // 6, 9) < 0.5 else 0)
    if y >= top:
        return 0.0 if y == top else 1.0
    if X % 16 in (3, 4):
        return 0.0
    return 0.2 + 0.45 * (y / max(h - 1, 1))


def m_scorch(x, y, w, h, X, Y, b):
    """the MANSION's roof scorched: flat ash (the soot is the palette move), the eave burnt a step deeper. No burn
    patches: the roof repeats one flat tile (34), so a blotch drawn into it repeats as stripes. Vanilla's lit edge
    kept"""
    if b < 0.2:
        return b
    return 0.67 if y >= h - 2 else 0.34


MATERIALS.update({
    "fuchsia_city": {
        11: {1: "canopy", 2: "canopy", 3: "canopy", 4: "canopy"},
        #  the pens (row 9, a..e) are not redrawn: their move is a colour, the neon (MOVES)
    },
    "cinnabar_island": {
        8: {1: "roof", 2: "roof", 3: "roof", 4: "roof"},
        9: {1: "metal", 2: "metal", 3: "metal", 4: "metal", 5: "metal"},
        #  ROUTE 20's islet rocks and ROUTE 21's jetty draw general's row 1 (the sand and rock every map shares):
        #  silvering them needs a palette this tileset cannot move -- left, a question for the user
    },
    "berry_forest": {
        11: {1: "canopy", 2: "canopy", 9: "canopy", 10: "canopy"},
    },
})
#  the island kit: ONE..SEVEN ISLAND share one look. Row 8 is the purple-roofed house in all three tilesets (the same
#  palette); the harbour house draws general's rows 2 and 3 (its red roof is row 2's a..e)
_ISLE_HOUSE = {9: "roof", 10: "roof", 11: "roof", 12: "roof", 13: "roof", 6: "siding", 7: "siding", 8: "siding"}
_ISLE_HARBOUR = {10: "net", 11: "net", 12: "net", 13: "net", 14: "net"}
MATERIALS["sevii_islands_123"] = {
    8: dict(_ISLE_HOUSE), 2: dict(_ISLE_HARBOUR),
    11: {11: "dishroof", 12: "dishroof", 13: "dishroof"},           # ONE ISLAND's NET centre
    9: {1: "glass", 2: "glass", 6: "siding", 7: "siding", 8: "siding", 9: "siding", 10: "siding"},   # TWO's shop
}
MATERIALS["sevii_islands_45"] = {
    8: dict(_ISLE_HOUSE), 2: dict(_ISLE_HARBOUR),
    10: {9: "roof", 10: "roof", 11: "roof", 12: "roof", 6: "siding", 7: "siding", 8: "siding"},     # the barn
    9: {9: "roof", 10: "roof", 11: "roof", 12: "roof", 13: "roof"},                               # the resort
    11: {9: "pebble", 10: "pebble", 11: "pebble", 12: "pebble", 13: "pebble", 14: "pebble"},      # the stones
}
MATERIALS["sevii_islands_67"] = {
    8: dict(_ISLE_HOUSE), 2: dict(_ISLE_HARBOUR),
    10: {10: "shard", 11: "shard", 12: "shard", 13: "shard", 14: "shard"},                        # THE ANNEX
    9: {7: "curtain", 8: "curtain", 9: "curtain", 10: "curtain", 14: "curtain", 15: "curtain"},   # USER TOWER
}
_ISLE_STYLE = dict(roof=m_weatherboard, siding=m_clapboard, net=m_net, dishroof=m_rings, glass=m_glass,
                   pebble=m_pebble, shard=m_facets, curtain=m_curtain_glint)
STYLE.update({
    "fuchsia_city": dict(canopy=m_glossy),
    "cinnabar_island": dict(roof=m_scorch, metal=m_mercury),
    "berry_forest": dict(canopy=m_dense),
    "sevii_islands_123": dict(_ISLE_STYLE), "sevii_islands_45": dict(_ISLE_STYLE),
    "sevii_islands_67": dict(_ISLE_STYLE),
})
for _ts in ("fuchsia_city", "cinnabar_island", "berry_forest", "sevii_islands_123", "sevii_islands_45",
            "sevii_islands_67"):
    for _m in ("canopy", "roof", "metal", "net", "dishroof", "shard", "curtain", "pebble"):
        KEEP_LIGHT_TOWN[(_ts, _m)] = 0.0
#  SOMEONE'S STONE (FIVE ISLE, row 2 -- general's greys, drawn by its pillar alone in this tileset) as a cairn
MATERIALS["sevii_islands_45"][2].update({2: "cairn", 3: "cairn", 4: "cairn", 5: "cairn", 6: "cairn"})
STYLE["sevii_islands_45"]["cairn"] = m_cairn
KEEP_LIGHT_TOWN[("sevii_islands_45", "cairn")] = 0.0


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
    town = Town(ts, moved=True)
    van = lambda t: t < len(town.van)
    cand = {t for t in range(len(town.disk)) if van(t) and town.disk[t] != town.van[t] and any(town.van[t])
            and town.draws[t] and all((a == 0) == (b == 0) for a, b in zip(town.disk[t], town.van[t]))}
    while cand:
        town = Town(ts, moved=True)
        town.as_before(cand)
        new, _ = draw(town)
        keep = {t for t in cand if new[t] == town.disk[t]}
        if keep == cand:
            return town, cand
        cand = keep
    return Town(ts, moved=True), set()


def draw(town):
    """the redraw, then the moves that come after it (reindexed pixels)"""
    new, what = redraw(town)
    return apply_post(town, new), what


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
                    if isinstance(lv, tuple):           # another material's ladder (VERDIGRIS's bloom)
                        lv, other = lv
                        lad2 = ladder(town, row, other)
                        if len(lad2) >= 2:
                            lad, keep = lad2, 0.0
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
    "vermilion_city": [("VermilionCity", 4, 1, 32, 20, "the pantiled houses and the hall"),
                       ("VermilionCity", 14, 26, 18, 12, "the S.S. ANNE pier"),
                       ("SSAnne_Exterior", 26, 0, 38, 7, "the quay and the truck")],
    "lavender_town": [("Route12", 4, 20, 16, 22, "ROUTE 12's boardwalks"),
                      ("Route10", 0, 32, 15, 12, "the KEEPALIVE PLANT"),
                      ("LavenderTown", 0, 0, 24, 19, "the houses and the tower's base"),
                      ("Route10", 12, 70, 12, 11, "ROUTE 10's domed centre")],
    "celadon_city": [("Route17", 0, 0, 20, 18, "THE STREAK (ROUTE 17)"),
                     ("CeladonCity", 4, 2, 36, 22, "the department store, the blocks, the fountain"),
                     ("CeladonCity", 28, 14, 16, 12, "the mansion")],
    "saffron_city": [("SaffronCity", 12, 7, 28, 22, "the plaza, the houses and the tower"),
                     ("SaffronCity", 33, 6, 22, 14, "the north row"),
                     ("SaffronCity", 12, 27, 42, 14, "the south row and the dojo")],
    "fuchsia_city": [("SafariZone_Center", 0, 0, 24, 16, "the SAFARI's woods and marsh"),
                     ("FuchsiaCity", 0, 0, 42, 14, "the SAFARI gate's frontage and the pens"),
                     ("SafariZone_West", 30, 0, 18, 14, "a SAFARI rest house")],
    "cinnabar_island": [("CinnabarIsland", 2, 0, 20, 14, "the MANSION's front and the lab (SCORN's)"),
                        ("Route21_South", 2, 44, 14, 8, "ROUTE 21's jetty (left: general's row 1)")],
    "sevii_islands_123": [("OneIsland", 5, 0, 20, 12, "ONE ISLAND: the NET centre and the houses"),
                          ("TwoIsland", 28, 3, 16, 9, "TWO ISLAND's shop and house"),
                          ("ThreeIsland_Port", 6, 11, 12, 9, "a harbour house (every port)")],
    "sevii_islands_45": [("FiveIsland_Meadow", 6, 14, 12, 9, "the meadow's barn"),
                         ("FiveIsland_MemorialPillar", 3, 38, 12, 12, "SOMEONE'S STONE and its stones"),
                         ("FiveIsland_ResortGorgeous", 34, 2, 12, 8, "RESORT SUBLIME's house"),
                         ("FourIsland", 20, 8, 16, 12, "FOUR ISLAND's houses")],
    "sevii_islands_67": [("BirthIsland_Exterior", 6, 3, 20, 14, "THE ANNEX's triangle"),
                         ("SevenIsland_TrainerTower", 50, 0, 16, 12, "USER TOWER"),
                         ("SixIsland", 6, 10, 18, 20, "SIX ISLAND's house and harbour"),
                         ("SevenIsland_TanobyRuins", 0, 0, 30, 10, "TANOBY: the chamber doors kept for batch G")],
    "berry_forest": [("ThreeIsland_BerryForest", 0, 0, 24, 16, "DENSE WOOD's mouth"),
                     ("ThreeIsland_BerryForest", 9, 14, 16, 10, "the clearing")],
}


def batch(ts):
    return "batch H" if SHEET_PREFIX.get(ts) == "t438h" else "batch F"


def plan_of(ts):
    return next(p for p in PLAN if p["ts"] == ts)


def grey(im):
    """DaemonsHalftoneMix's grey (fieldmap.c): 0.3 R + 0.59 G + 0.1133 B, on the GBA's five bits"""
    out = im.copy()
    o = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b = (c >> 3 for c in o[x, y])
            v = (r * 77 + g * 151 + b * 29) >> 8
            o[x, y] = (v << 3 | v >> 2,) * 3
    return out


def map_sheet(town, new, crop, path, today=None, prev=None):
    """today | the draft, 1x and 2x (and grey for HALFTONE); `today` is the town as the engine has it when the draft
    town carries palette moves; `prev`, the tiles of the draft this one revises (shown between, at 1x)"""
    name, x0, y0, w, h, what = crop
    p = plan_of(town.ts)
    a = render(today or town, name, box=(x0, y0, w, h))
    b = render(town, name, tiles=new, box=(x0, y0, w, h))
    f, F = font(13), font(17)
    D = "revised" if today is not None else "draft"
    z2 = lambda im: im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    c = render(today or town, name, tiles=prev, box=(x0, y0, w, h)) if prev else None
    rows = [_row([_label(a, "today 1x", f)] + ([_label(c, "first draft 1x (t438f2)", f)] if c else []) +
                 [_label(b, D + " 1x", f)]),
            _row([_label(z2(a), "today 2x", f), _label(z2(b), D + " 2x", f)])]
    if town.ts == "lavender_town":                    # as DaemonsIsHalftone() shows it
        g = ("grey -- as HALFTONE shows it" if name == "LavenderTown" else
             "grey -- for comparison: %s is not HALFTONE's mapsec, so it plays in colour" % name)
        rows.insert(1, _title(g, f, 1000))
        rows.insert(2, _row([_label(grey(a), "today 1x, grey", f)] +
                            ([_label(grey(c), "first draft 1x, grey", f)] if c else []) +
                            [_label(grey(b), D + " 1x, grey", f)]))
        rows.append(_row([_label(z2(grey(a)), "today 2x, grey", f), _label(z2(grey(b)), D + " 2x, grey", f)]))
    pals = ("palette moves: see the _palette sheet" if MOVES.get(town.ts) and today else "palettes unchanged")
    sheet = _col([_title("T-438 " + batch(town.ts) + " DRAFT -- %s: %s\n%s, cells %d,%d %dx%d -- footprints, blocks, collision "
                         "unchanged; %s" % (p["name"], what, name, x0, y0, w, h, pals), F,
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
    sheet = _col([_title("T-438 " + batch(town.ts) + " DRAFT -- %s: the tileset (rows unchanged)\n%s" % (
        p["name"], "\n".join(_wrap(p["look"], 110))), F, top.width), top])
    sheet.save(path)
    return path


def _swatches(pal, mark=(), Z=26, f=None):
    im = Image.new("RGB", (16 * Z, Z + 14), BG)
    d = ImageDraw.Draw(im)
    for i, c in enumerate(pal):
        d.rectangle([i * Z + 1, 1, i * Z + Z - 2, Z - 2], fill=c, outline=(220, 0, 0) if i in mark else (90, 90, 90))
        d.text((i * Z + 8, Z), "%x" % i, font=f, fill=(30, 30, 30))
    return im


def move_cells(town, row, idx=None, blocks=None, tiles=None):
    """{map: [cells]} for every reachable map: the cells whose block draws `idx` in `row` (or is one of `blocks`)"""
    G = general()
    hit = set(blocks or ())
    if idx is not None:
        src = lambda t: G["tiles"][t] if t < 640 else (tiles or town.now)[t - 640]
        for b in range(town.nblocks):
            for v in entries(town.mt, b):
                if v >> 12 == row and set(src(v & 0x3FF)) & set(idx):
                    hit.add(640 + b)
    out = {}
    for m in town.maps:
        W = layouts()[m]["width"]
        c = [(i % W, i // W) for i, v in enumerate(town.grid[m]) if v in hit]
        if c:
            out[m] = c
    return out


def palette_sheet(today, town, new, path):
    """every moved row before and after, and every map that draws what moved, before | after"""
    f, F, H = font(12), font(14), font(18)
    p = plan_of(town.ts)
    who = "proposed 2026-10-24" if batch(town.ts) == "batch H" else "the user, 2026-10-23"
    parts = [_title("T-438 %s DRAFT -- %s: the palette moves (%s)\nred: the indices that move. Under each move, "
                    "every reachable map that draws them: today | revised" % (batch(town.ts), p["name"], who),
                    H, 1400)]
    for mv in town.moves:
        k = mv["kind"]
        lines = _wrap("%s -- %s" % (k.upper(), mv["why"]), 150)
        parts.append(_title("\n".join(lines), F, 1400))
        if k == "colours":
            r = mv["row"]
            parts.append(_row([_label(_swatches(today.pals[r], mv["colours"], f=f), "row %d today" % r, f),
                               _label(_swatches(town.pals[r], mv["colours"], f=f), "row %d revised" % r, f)]))
            where = move_cells(town, r, idx=mv["colours"], tiles=new)
        elif k == "rerow":
            r = mv["dst"]
            sw = [_label(_swatches(today.palette(q), f=f), "row %d (general's, unchanged)" % q if q < 7 else
                         "row %d" % q, f) for q in mv["src"]]
            sw.append(_label(_swatches(town.pals[r], range(16), f=f), "row %d revised (they draw here now)" % r, f))
            parts.append(_row(sw))
            parts.append(_title("%d entries in %d blocks: %s" % (mv["entries"], len(mv["blocks"]), " ".join(
                "%03x" % b for b in mv["blocks"])), f, 1400))
            where = move_cells(town, r, blocks=mv["blocks"])
        elif k == "reindex":
            where = move_cells(town, mv["row"], blocks=[640 + b for b in range(town.nblocks)
                                                        if any((v & 0x3FF) in mv["tiles"]
                                                               for v in entries(town.mt, b))])
            parts.append(_title("tiles %s: %s" % (", ".join(map(str, mv["tiles"])), ", ".join(
                "%x -> %x" % kv for kv in sorted(mv["map"].items()))), f, 1400))
        else:                                           # a tile copy
            Z = 10
            t0, t1 = mv["src"] - 640, mv["new"] - 640
            pal = town.palette(mv["row"])
            ims = []
            for lbl, px in (("%d today" % mv["src"], today.now[t0]), ("%d revised" % mv["new"], new[t1])):
                im = Image.new("RGB", (8 * Z, 8 * Z))
                o = ImageDraw.Draw(im)
                for q, c in enumerate(px):
                    o.rectangle([(q % 8) * Z, (q // 8) * Z, (q % 8) * Z + Z - 1, (q // 8) * Z + Z - 1],
                                fill=pal[c])
                ims.append(_label(im, lbl, f))
            parts.append(_row(ims))
            parts.append(_title("%d entries in blocks %s now draw %d" % (mv["entries"], " ".join(
                "%03x" % b for b in mv["blocks"]), mv["new"]), f, 1400))
            where = move_cells(town, mv["row"], blocks=mv["blocks"])
        if not where:
            parts.append(_title("   (no reachable map draws it)", f, 1400))
        for m, cells in where.items():
            xs, ys = [x for x, _ in cells], [y for _, y in cells]
            l = layouts()[m]
            x0, y0 = max(0, min(xs) - 2), max(0, min(ys) - 2)
            w, h = min(max(xs) - x0 + 3, l["width"] - x0), min(max(ys) - y0 + 3, l["height"] - y0)
            if w * h > 60 * 40:
                w, h = min(w, 60), min(h, 40)
            a = render(today, m, box=(x0, y0, w, h))
            b = render(town, m, tiles=new, box=(x0, y0, w, h))
            if w * 16 < 500:
                a, b = (i.resize((i.width * 2, i.height * 2), Image.NEAREST) for i in (a, b))
            g = [] if town.ts != "lavender_town" else [_label(grey(a), "grey", f), _label(grey(b), "grey", f)]
            parts.append(_title("%s: %d cells draw it (shown: cells %d,%d %dx%d)" % (m, len(cells), x0, y0, w, h),
                                f, 1400))
            parts.append(_row([_label(a, "today", f), _label(b, "revised", f)] + g))
    sheet = _col(parts, gap=8)
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


# ================================================================== THE SAME BUSH: a palette split (batch H)
#  THE SAME BUSH (SIX ISLAND's PATTERN BUSH, "a maze where every corner looks like the last one, described honestly")
#  shares THE UNDERTONE's tileset, so it wears THE UNDERTONE's green. The user (2026-10-23): give it its own palette
#  split, with the islands -- the way batch E split UMBRAL ASCENT off the cave (gTileset_CaveUmbral): a Tileset header
#  over gTileset_ViridianForest's tiles, metatiles and attributes with rows 7..12 of its own, and the one layout
#  pointed at it; daemonslib.tileset_base() already leads every tool from the split's name to viridian_forest's folder.
#  THE SAME BUSH draws rows 0 (general's) and 8 only, so only row 8 differs: the canopy (1..5) and the bark (6..8);
#  the ground greens (12..15) stay, so its edges meet the grass as they do today. Two looks are proposed; the draft
#  folder takes A. Nothing is drawn: the tiles are THE UNDERTONE's, the grove tell included.
SPLITS = {
    "same_bush": dict(
        base="viridian_forest", symbol="gTileset_SameBush", maps=["SixIsland_PatternBush"],
        dir="viridian_forest/palettes_samebush", row=8, name="THE SAME BUSH",
        crops=[("SixIsland_PatternBush", 0, 0, 24, 14, "the mouth"), ("SixIsland_PatternBush", 30, 12, 24, 14,
                                                                      "deep in it: every corner the last one")],
        options=[
            ("A  SALT SCRUB (drafted)", "the island's own scrub: the canopy a silvery sage, as if salt spray had "
             "dried on every leaf, the bark weathered grey -- one even light, so the corners really do look alike",
             _cols(i1="ccec84 d4e6c0", i2="84bc54 9cb88c", i3="42803a 5e8070", i4="2a522c 34504a",
                   i5="397318 46644a", i6="62414a 5e5652", i7="836a52 847a6c", i8="4c362a 403a36")),
            ("B  COPY OF A COPY", "the same canopy gone faint and faintly cyan, low in contrast, like a photocopy of "
             "THE UNDERTONE -- the maze as a copy that has lost a generation of detail; the bark kept",
             _cols(i1="ccec84 c4e4b4", i2="84bc54 94c49c", i3="42803a 5c9c84", i4="2a522c 3c6c60",
                   i5="397318 4c8c74")),
        ]),
}


def split_draft(key, outdir, sheets_dir):
    """the split's proposed palettes (option A into the draft folder, as palettes_samebush/NN.pal) and its sheet"""
    sp = SPLITS[key]
    today = Town(sp["base"])
    r = sp["row"]
    looks = []
    for title, why, cols in sp["options"]:
        t = Town(sp["base"])
        for i, (a, b) in cols.items():
            five = lambda c: tuple(x >> 3 for x in c)
            if five(t.pals[r][i]) != five(tuple(int(a[j:j + 2], 16) for j in (0, 2, 4))):
                raise SystemExit("  !! %s row %d index %d is %s, not the option's before" % (key, r, i, t.pals[r][i]))
            t.pals[r][i] = _q(b)
        order = lambda pal: sorted(range(1, 6), key=lambda i: -lum(pal[i]))
        if order(t.pals[r]) != order(today.pals[r]):
            raise SystemExit("  !! %s %s reorders the canopy's light" % (key, title))
        looks.append((title, why, t))
    d = os.path.join(outdir, key, "palettes")
    os.makedirs(d, exist_ok=True)
    daemonslib.write_pal(os.path.join(d, "%02d.pal" % r), looks[0][2].pals[r])
    f, F, H = font(12), font(14), font(18)
    z2 = lambda im: im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    parts = [_title("T-438 batch H DRAFT -- %s: its own palette split (proposed 2026-10-24)\n%s draws rows 0 "
                    "(general's) and %d; a split changes rows 7..12, so only row %d moves. Tiles: THE UNDERTONE's "
                    "as built (grove tell kept)" % (sp["name"], sp["maps"][0], r, r), H, 1500)]
    sw = [_label(_swatches(today.pals[r], f=f), "row %d today (THE UNDERTONE's)" % r, f)]
    for title, why, t in looks:
        sw.append(_label(_swatches(t.pals[r], [i for i in range(16) if t.pals[r][i] != today.pals[r][i]], f=f),
                         "row %d, %s" % (r, title.split("(")[0].strip()), f))
    parts.append(_row(sw))
    for title, why, t in looks:
        parts.append(_title("%s -- %s" % (title, "\n   ".join(_wrap(why, 150))), F, 1500))
    for name, x0, y0, w, h, what in sp["crops"]:
        ims = [render(today, name, box=(x0, y0, w, h))] + [render(t, name, box=(x0, y0, w, h)) for _, _, t in looks]
        lbl = ["today 1x"] + [ti.split("(")[0].strip() + " 1x" for ti, _, _ in looks]
        parts.append(_title("%s, cells %d,%d %dx%d -- %s" % (name, x0, y0, w, h, what), F, 1500))
        parts.append(_row([_label(im, l, f) for im, l in zip(ims, lbl)]))
        parts.append(_row([_label(z2(ims[0]), "today 2x", f), _label(z2(ims[1]), lbl[1].replace("1x", "2x"), f)]))
    parts.append(_title("\n".join([
        "WIRING (as gTileset_CaveUmbral, engine 2007d739f) -- by hand, done when built (2026-10-24); the tool writes the rows:",
        "  src/data/tilesets/headers.h: gTileset_SameBush = { .tiles = gTilesetTiles_ViridianForest, .palettes = "
        "gTilesetPalettes_SameBush,",
        "      .metatiles = gMetatiles_ViridianForest, .metatileAttributes = gMetatileAttributes_ViridianForest }",
        "  src/data/tilesets/graphics.h: gTilesetPalettes_SameBush -- rows 0..6 and 13..15 viridian_forest/palettes/, "
        "7..12 %s/" % sp["dir"],
        "  data/layouts/layouts.json: SixIsland_PatternBush_Layout's secondary_tileset -> gTileset_SameBush (the only "
        "map that moves; THE UNDERTONE and its grove keep theirs)",
        "  tools: tileset_base('gTileset_SameBush') -> viridian_forest (shared metatiles); gbagrove's tell is in the "
        "shared tiles, so it holds"]), f, 1500))
    path = os.path.join(sheets_dir, "t438h_samebush.png")
    _col(parts, gap=8).save(path)
    return [path]


# ================================================================== the work
def save_tiles(town, new, path):
    """tiles.png, 4-bit with sixteen colours (the engine's own PNG palette), a tile row longer if a move added a tile"""
    im = Image.new("P", (128, ((len(new) + 15) // 16) * 8))
    im.putpalette(town.im.convert("P").getpalette()[:48])
    px = im.load()
    for t, p in enumerate(new):
        for k, v in enumerate(p):
            px[(t % 16) * 8 + k % 8, (t // 16) * 8 + k // 8] = v
    im.save(path, bits=4)


def save_moves(town, d):
    """a town's moved palette rows (palettes/NN.pal) and, if a move touched it, its metatiles.bin, into folder d.
    Returns the rows written"""
    rows = sorted({mv["row"] for mv in town.moves if mv["kind"] == "colours"})
    if rows:
        os.makedirs(os.path.join(d, "palettes"), exist_ok=True)
    for r in rows:
        daemonslib.write_pal(os.path.join(d, "palettes", "%02d.pal" % r), town.pals[r])
    if town.mt != town.mt_disk:
        open(os.path.join(d, "metatiles.bin"), "wb").write(town.mt)
    return rows


def split_pals(key, option):
    """a split's rows 7..12, {row: colours}: its base's own rows, with the option's colours in its row"""
    sp = SPLITS[key]
    base = Town(sp["base"])
    r = sp["row"]
    out = {k: list(base.pals[k]) for k in range(7, 13)}
    five = lambda c: tuple(x >> 3 for x in c)
    for i, (a, b) in sp["options"][option][2].items():
        if five(out[r][i]) != five(tuple(int(a[j:j + 2], 16) for j in (0, 2, 4))):
            raise SystemExit("  !! %s row %d index %d is %s, not the option's before" % (key, r, i, out[r][i]))
        out[r][i] = _q(b)
    return out


def write_split(key, option):
    """the split's rows 7..12 into SEC/<its dir> (the Tileset header in headers.h names them). Idempotent"""
    sp = SPLITS[key]
    d = os.path.join(GBA, SEC + sp["dir"])
    os.makedirs(d, exist_ok=True)
    rows = []
    for r, pal in split_pals(key, option).items():
        f = os.path.join(d, "%02d.pal" % r)
        if not os.path.exists(f) or read_pal(f) != pal:
            daemonslib.write_pal(f, pal)
            rows.append(r)
    if rows:
        print("  wrote %s (%s, option %s): a palette split, rows %s in %s" % (
            sp["name"], sp["symbol"], sp["options"][option][0].split()[0], rows, sp["dir"]))
    else:
        print("  %s: already written, nothing to write" % sp["name"])


def write_draft(outdir):
    os.makedirs(outdir, exist_ok=True)
    sheets_dir = SHEETS
    os.makedirs(sheets_dir, exist_ok=True)
    only = [t for t in (argval("--only") or "").split(",") if t]
    made = [] if only else [plan_sheet(census(True), os.path.join(sheets_dir, "t438f_plan.png"))]
    gj = os.path.join(outdir, "groups.json")
    info = json.load(open(gj)).get("drafted", {}) if only and os.path.exists(gj) else {}
    for ts in [t for t in (only or DRAFTED) if t not in SPLITS]:
        today = Town(ts)
        town = Town(ts, moved=True)
        new, what = draw(town)
        moved = [t for t in range(len(new)) if any((a == 0) != (b == 0) for a, b in zip(new[t], town.now[t]))]
        if moved:
            raise SystemExit("  !! %s: tiles %s change their footprint" % (ts, moved[:10]))
        d = os.path.join(outdir, ts)
        os.makedirs(d, exist_ok=True)
        prev_path = os.path.join(d, "tiles.png")
        prev = tiles_of(Image.open(prev_path)) if SHEET_PREFIX.get(ts) == "t438f3" and os.path.exists(prev_path) \
            else None
        save_tiles(town, new, prev_path)
        pals_changed = save_moves(town, d)
        a, b, added = seams(town, new)
        changed = sorted(t for t in range(len(new)) if t >= len(today.now) or new[t] != today.now[t])
        info[ts] = dict(name=plan_of(ts)["name"], look=plan_of(ts)["look"], tiles_redrawn=len(changed),
                        from_general=sorted(t for t, w in what.items() if w == "general"),
                        by_role={t: w for t, w in what.items() if w != "general"},
                        left_vanilla=sorted(town.targets - set(changed)),
                        doors_kept=sorted(town.left & town.door_tiles),
                        seams=dict(today=a, draft=b, added=added), palettes_changed=pals_changed,
                        moves=[{k: v for k, v in mv.items() if k != "colours"} for mv in town.moves])
        s = SHEET_PREFIX.get(ts, "t438f") + "_" + SHORT[ts]
        made.append(tiles_sheet(town, new, what, os.path.join(sheets_dir, "%s_tiles.png" % s)))
        for k, crop in enumerate(CROPS[ts], 1):
            made.append(map_sheet(town, new, crop, os.path.join(sheets_dir, "%s_%d.png" % (s, k)),
                                  today=today if town.moves else None, prev=prev))
        if town.moves:
            made.append(palette_sheet(today, town, new, os.path.join(sheets_dir, "%s_palette.png" % s)))
    for key in SPLITS:
        if not only or key in only:
            made += split_draft(key, outdir, sheets_dir)
            info[key] = dict(name=SPLITS[key]["name"], split_of=SPLITS[key]["base"], symbol=SPLITS[key]["symbol"],
                             maps=SPLITS[key]["maps"], options=[o[0] for o in SPLITS[key]["options"]],
                             drafted="A: palettes/%02d.pal (row %d only)" % (SPLITS[key]["row"], SPLITS[key]["row"]))
    json.dump(dict(ticket="T-438 batch F", status="CALLOW, SLATE, DOLDRUM, THE UNDERTONE approved 2026-10-23 and built by --write "
                   "--approved; ARDOR, HALFTONE, VERDIGRIS, BRAZEN drafted 2026-10-23 (t438f2_*), approved "
                   "with revisions and revised (t438f3_*: palette moves, the roofs dotted whole, the pantiles "
                   "calmed) and built (engine f8fa96614); batch H (LURID, QUICKSILVER, the islands, DENSE WOOD, THE SAME BUSH's split) "
                   "drafted 2026-10-24 (t438h_*), approved and built (engine c5078dca6) with the landmarks (SCORN SOLUTIONS, the "
                   "MANSION, USER TOWER, THE ANNEX's triangle) kept for T-447 and QUICKSILVER's two moves dropped",
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
        town = Town(ts, moved=True)
        new, what = draw(town)
        changed = sum(1 for t in range(len(new)) if new[t] != town.now[t])
        print("  draft %-18s %d tiles redrawn (%d from general's own), %d leftovers not redrawn" % (
            ts, changed, sum(1 for w in what.values() if w == "general"), len(town.targets - set(what))))


def main():
    if WRITE:
        if "--approved" not in ARGS or not APPROVED:
            print("  --write refused: --write needs --approved, and APPROVED must name the towns the user approved.")
            return 0
        for ts in APPROVED:
            if MOVES.get(ts) and not PALETTES:
                print("  %s: skipped -- it carries palette moves (MOVES), which go into the engine only with "
                      "--palettes" % ts)
                continue
            town, _ = drawn_before(ts)
            new, what = draw(town)
            if any((a == 0) != (b == 0) for t in range(len(new)) for a, b in zip(new[t], town.now[t])):
                raise SystemExit("  !! %s: a tile's footprint moved -- nothing written" % ts)
            pal_moved = any(town.pals[mv["row"]] != read_pal(os.path.join(town.dir, "palettes/%02d.pal" % mv["row"]))
                            for mv in town.moves if mv["kind"] == "colours")
            if new == town.disk and town.mt == town.mt_disk and not pal_moved:
                print("  %s: already drawn (%d tiles), nothing to write" % (ts, len(what)))
                continue
            save_tiles(town, new, os.path.join(town.dir, "tiles.png"))
            rows = save_moves(town, town.dir)
            print("  wrote %s: %d tiles%s" % (ts, sum(1 for t in range(len(new)) if t >= len(town.disk) or
                                                       new[t] != town.disk[t]),
                                              "; palette rows %s%s" % (rows, ", metatiles.bin" if town.mt !=
                                                                       town.mt_disk else "") if town.moves else ""))
        for key, option in SPLITS_APPROVED.items():
            if not PALETTES:
                print("  %s: skipped -- a palette split goes into the engine only with --palettes" % key)
                continue
            write_split(key, option)
        return 0
    if DRAFT is not None:
        for p in write_draft(DRAFT):
            print("  wrote %s" % p)
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
