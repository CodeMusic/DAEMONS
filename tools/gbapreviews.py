#!/usr/bin/env python3
"""T-445: the map preview screens -- the picture a cave (or a forest, the tower, a hideout) shows as it is entered.

    python3 tools/gbapreviews.py                         # report: every preview, the mapsecs that show it, the name
                                                         #   the game prints on it, and which T-438 batch E covered
    python3 tools/gbapreviews.py --draft [DIR]           # draft the batch E caves' previews into DIR (gfx/drafts/t445/),
                                                         #   and the contact sheets; --sheets DIR puts the sheets elsewhere
    python3 tools/gbapreviews.py --paint [CAVE ...]      # PAINT each cave's mouth on the sprite server (spriteforge.py,
                                                         #   roverbyteseer:8008): gfx/drafts/t445/<cave>/painted.png and
                                                         #   its record, from a start image graded out of vanilla's
                                                         #   picture in the cave's colours (painted_init.png)
    python3 tools/gbapreviews.py --draft --top-down      # the old top-down drafts, even where a painting exists
    python3 tools/gbapreviews.py --landmarks --paint     # the landmarks' cards (LANDMARK: CORPUS's tower, DAEMON TOWER,
    python3 tools/gbapreviews.py --landmarks --draft     #   the MANSION), painted from T-447's buildings as built, and
                                                         #   CORPUS HIDEOUT's and WAREHOUSE's rooms from the maps; their
                                                         #   --write writes only what LANDMARK_APPROVED names
    python3 tools/gbapreviews.py --landmarks --only review_board --paint review_board --seed N --draft DIR
                                                         # T-456: one card, one seed, drafted into DIR (a NEW card --
                                                         #   UMBRA PLATEAU has no sMapPreviewScreenData entry -- is
                                                         #   drafted, never written)
    python3 tools/gbapreviews.py --places --paint        # the forests' and the SAFARI's cards (PLACES: THE UNDERTONE,
    python3 tools/gbapreviews.py --places --draft        #   DENSE WOOD, the SAFARI, and THE SAME BUSH as a card of its
                                                         #   own), painted as the caves were; --write writes only what
                                                         #   PLACES_APPROVED names, and never a NEW card
    python3 tools/gbapreviews.py --cards --paint --draft gfx/drafts/t445_landmarks
                                                         # 2026-11-11: the landmark cards' re-census (CARDS) -- the
                                                         #   candidates for the cards T-447 pairs 4-5 left stale or
                                                         #   gave an alternative; a census sheet and a candidates
                                                         #   sheet; --write writes only what CARDS_APPROVED names
    python3 tools/gbapreviews.py --write --approved      # into the engine (graphics/map_preview/<cave>/tiles.png,
                                                         #   tilemap.bin, and the -num_tiles line in graphics_file_rules.mk).
                                                         #   OTHER CAVE's light1..3.pal too. Without --approved it refuses.

HOW THE ENGINE DRAWS ONE (src/map_preview_screen.c). sMapPreviewScreenData maps a MAPSEC to three files in
graphics/map_preview/<name>/: tiles.4bpp.lz (from tiles.png, `-num_tiles N` in graphics_file_rules.mk), tilemap.bin.lz
(a 32x20 BG map, committed binary) and tiles.gbapal (from tiles.png's own 32-colour palette). MapPreview_LoadGfx loads
the palette into BG palettes 13 and 14 and the tiles to BG0 from tile 0; the picture is the screen's rows 3..16
(240x112) in palette 13, and rows 0..2 and 17..19 -- the black letterbox and the white name banner drawn in tiles --
are palette 14. Columns 30 and 31 are off screen (palette 0, tile 0).

THE NAME IS NOT IN THE PICTURE. MapPreview_CreateMapNameWindow prints GetMapName(mapsec) -- our region_map_sections
name, DEADSTACK, OTHER CAVE -- into a 13x2-tile window at (0,0) (baseBlock 0x1C2, so the picture's tiles must stay
below 450), centred in 104px, in palette 14's colours 1 (fill), 2 (text) and 3 (shadow). So a preview needs no name
drawn into it, and the DAEMONS names already show on vanilla's pictures; the sheet here prints them in the game's own
font (graphics/fonts/latin_normal.png) so the draft is seen as a player would see it. A name wider than 104px would
start off the window's left edge (xctr is u32): the report checks every one.

WHAT A DRAFT IS. Vanilla's pictures are painted landscapes; ours are drawn from the caves as they now are (T-438
batch E): the cave's map rendered from its layout with the built tilesets (reviewsheet.py's renderer, the same that
draws every map sheet), a characteristic window of it chosen -- the 15x7-metatile window of the cave's maps with the
most different blocks, the least bare floor and the least void (an 8x4 window doubled where the rooms are too
small), or the one VIEW names -- and reduced
to 15 colours in palette 13 (index 0 is left as vanilla's: BG0's colour 0 is transparent). Palette 14 and every tile
of the letterbox and banner are vanilla's, byte for byte, so the name window looks exactly as it did.

PAINTED, NOT TOP-DOWN (the user, 2026-10-23: "painted entrances, not top-down -- the sprite server paints each
cave's mouth at 512 from these views, in each cave's colours"). Where gfx/drafts/t445/<cave>/painted.png exists it is
the picture: --paint makes it. Its start image is vanilla's own painting (for the composition -- a mouth in a slope,
a sea or a sky beyond), every region of it graded through the cave's colours (PAINT's ramps, by luminance: rock,
sky, foliage, water), and the top-down view's light laid faintly into the rock so the cave's motif is in the paint
(the stack's courses, the outage's columns). The server repaints that at 1088x512 (its wide size, 512 high) with
the cave's prompt, image to image, at a denoise low enough that vanilla's composition survives. The painting is
then fitted to 240x112 and reduced as the top-down view was: 15 colours, under 450 tiles (vanilla's banner is 7
tiles, the picture at most 420, so a painting always fits).

OTHER CAVE'S FOUR LIGHTS. Its preview is ONE set of tiles and FOUR palettes 13: the teal painting's colours that
are its crystal (teal) or its rock (mauve) are moved onto each light's own ramps (the tileset's palettes_other_1..3,
by luminance), the sky and sea kept. --draft writes light1..3.pal beside tiles.png and a preview per light, and
--write writes them into graphics/map_preview/altering_cave/ (the user, 2026-10-23: the preview follows the light).
MapPreview_LoadGfx lays the light's palette over palette 13 -- and the preview runs BEFORE the map's ON_TRANSITION
steps VAR_OTHER_CAVE_LIGHT (fldeff_flash.c's CB2_DoChangeMap shows it, then CB2_LoadMap2's LoadMapFromWarp runs the
script), so the light it shows is the coming visit's, VarGet(VAR_OTHER_CAVE_LIGHT) % 4, not fieldmap.c's
(visit - 1) % 4.

WHAT IS NOT DRAFTED: DOLDRUM CAVE (cerulean_cave -- its look waits on the user, T-251), and the previews that are not caves (forests, the tower, the mansion, SILPH, the hideout
and the warehouse, the SAFARI): T-445 is the caves, and those wait on their own batches. The report lists them all.

THE PLACES (2026-11-05, drafted): the landmarks are --landmarks; what is left vanilla but the two waiting caves is
the forests and the SAFARI, and --places paints them by the caves' method (vanilla's composition graded through the
colours the places are built in now -- THE UNDERTONE's deep understory, DENSE WOOD's golden canopy, the SAFARI's
grass under LURID's chartreuse -- then painted on the server). THE SAME BUSH (MAPSEC_PATTERN_BUSH) shows THE
UNDERTONE's picture in the engine; since batch H it is salt scrub on a tileset of its own, so it is drafted as a NEW
card (pattern_bush, borrowing viridian_forest's letterbox and banner). BUILT 2026-11-05: the user approved all four;
the engine has pattern_bush's own INCBINs and MPS_PATTERN_BUSH points at them, so --write writes it like the others.

THE TANOBY CHAMBERS (2026-11-06, drafted, the user away): batch G built them (engine d45f8c799), so their one card
(monean_chamber, shown by all seven chamber mapsecs) is drafted as the caves were -- `--paint monean_chamber`, then
`--draft --only monean_chamber`. APPROVED and BUILT 2026-11-06 (the user: "Build the top one"; engine 77e6e2044).
"""
import argparse, collections, contextlib, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t445")
MPS = os.path.join(GBA, "graphics/map_preview")
RULES = os.path.join(GBA, "graphics_file_rules.mk")

argv, sys.argv = sys.argv, sys.argv[:1]          # reviewsheet reads sys.argv on import
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import reviewsheet as RS
finally:
    sys.argv = argv
import fontwidth

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--sheets")
ap.add_argument("--paint", nargs="*")
ap.add_argument("--top-down", action="store_true", dest="top_down")
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
ap.add_argument("--over-later-work", action="store_true", help="accepted so check_generators --writes really runs the write")
ap.add_argument("--landmarks", action="store_true")      # the landmarks' cards (LANDMARK) instead of the caves
ap.add_argument("--places", action="store_true")         # the forests' and the SAFARI's cards (PLACES)
ap.add_argument("--cards", action="store_true")          # the landmark cards' candidates, 2026-11-11 (CARDS)
ap.add_argument("--only", nargs="+")                     # draft only these folders (T-456: one card, its seeds)
ap.add_argument("--seed", type=int)                      # --paint with this seed instead of the entry's
A = ap.parse_args()

# the caves T-438 batch E redrew (gbacaves.py: approved 2026-10-23, BUILT engine 2007d739f) -> their tileset look
BATCH_E = {
    "mt_moon": "cave (THE STACK)",
    "lost_cave": "cave (THE STACK, kept by THE WRONG WAY)",
    "victory_road": "cave/umbral (the stack in violet dusk, a palette split)",
    "digletts_cave": "digletts_cave (THE LINE)",
    "rock_tunnel": "rock_tunnel (THE OUTAGE)",
    "altering_cave": "rock_tunnel/other (the outage in OTHER CAVE's light, four of them in turn)",
    "power_plant": "power_plant (STILL RUNNING)",
    "seafoam_islands": "seafoam_islands (THE BLOOM)",
    "icefall_cave": "seafoam_islands/stillfall (the bloom gone glassy, a palette split)",
    "mt_ember": "mt_ember (EMBER UNDER ASH)",
    "dotted_hole": "navel_rock (BRAILLE)",
}
# the caves T-438 batch G redrew (gbatowns.py: BUILT as a DRAFT engine d45f8c799, the user away) -> their look. Drafted
# 2026-11-06, the user away: never written until the user approves (BATCH_G_APPROVED), --write skips them otherwise
BATCH_G = {
    "monean_chamber": "tanoby_ruins (the seven TANOBY chambers: dressed ochre stone, an invented script carved in it)",
}
BATCH_G_APPROVED = {"monean_chamber"}           # the user, 2026-11-06: "Build the top one" (seed 4451)
NOT_DRAFTED = {
    "cerulean_cave": "DOLDRUM CAVE: its look waits on the user (T-251, gbacaves.py), so its preview does too",
    "viridian_forest": "a forest (PLACES, --places)",
    "berry_forest": "a forest (PLACES, --places)",
    "pokemon_tower": "the tower: a landmark (LANDMARK, --landmarks)",
    "pokemon_mansion": "the mansion: a landmark (LANDMARK, --landmarks)",
    "silph_co": "SILPH (CORPUS's tower): a landmark (LANDMARK, --landmarks)",
    "rocket_hideout": "CORPUS HIDEOUT: an interior (LANDMARK, --landmarks), from the current map",
    "rocket_warehouse": "CORPUS WAREHOUSE: an interior (LANDMARK, --landmarks), from the current map",
    "safari_zone": "the SAFARI (PLACES, --places)",
}

# a view chosen by eye where the search would pick a duller one: (map, x0, y0) in metatiles, a 15x7 window at 1x
# or (map, x0, y0, 8) for an 8x4 window doubled. None of these is required; the search covers the rest.
VIEW = {
}
WIN_W, WIN_H = 15, 7          # metatiles in a 240x112 picture at 1x
LIGHT_NAMES = ["teal", "AMBER in slate", "CHRYSOPRASE in brown jasper", "ROSE QUARTZ in green schist"]


# the painted previews (T-445, the user's answer): each cave's colours as ramps, dark to light, that vanilla's
# picture is graded through by region (rock takes the light parts too unless "white" has a ramp of its own, as
# SMOULDER's steam and snow do, gone to ash); "motif" lays the cave's one idea into it (MOTIFS);
# "skygrad" lays the sky as a top-to-bottom gradient instead (dusk, night, ash haze); "tex" is how strongly the
# top-down view's light is laid into the rock. "prompt" is the cave's, "seed" and "denoise" the painting picked.
PAINT_SIZE = (1088, 512)
PAINT_STYLE = "pixel art, 16-bit game background, wide scene, %s, soft clean pixel shading"
PAINT_NEG = ("text, letters, words, watermark, signature, logo, person, character, creature, animal, frame, border, "
             "blurry, photo, 3d render, ui, slime, neon, oversaturated")
STACK = [(24, 40, 32), (40, 56, 48), (64, 88, 72), (96, 120, 104), (128, 152, 128), (168, 184, 160), (200, 208, 184)]
ASH = [(64, 52, 40), (96, 82, 64), (140, 124, 96)]
PAINT = {
    "mt_moon": dict(rock=STACK, motif=["courses"], sky=[(176, 172, 150), (226, 220, 196)], skygrad=1, leaf=ASH,
                    seed=4452, denoise=0.5,
                    prompt="a dark cave mouth in a rocky hill, the rock is layered thin slabs like stacked old circuit "
                           "boards and drive casings, thin tarnished gold connector strips along some layers, muted "
                           "sage green and dull solder mask green, ash brown dusty ground, pale hazy sky"),
    "lost_cave": dict(rock=STACK, motif=["courses"], leaf=ASH, seed=4451, denoise=0.5,
                      prompt="a dark cave mouth in a slope of layered slab rock by a calm sea, the rock layered like "
                             "stacked old circuit boards, muted sage green and solder mask green, ash brown ground, "
                             "pale sky over the sea"),
    "victory_road": dict(rock=[(40, 32, 72), (64, 56, 104), (96, 80, 136), (128, 112, 168), (160, 144, 192),
                               (192, 184, 216)],
                         sky=[(72, 56, 120), (214, 150, 160)], skygrad=1,
                         leaf=[(20, 18, 40), (40, 36, 72), (70, 62, 108)], seed=4452, denoise=0.5,
                         prompt="a cave entrance in a rocky cliff framed by a tall ruined stone gateway with pillars, "
                                "pine trees in silhouette, cold violet dusk, lavender and deep violet rock in stacked "
                                "layers, a rose glow low on the horizon, evening sky"),
    "digletts_cave": dict(rock=[(32, 24, 32), (64, 40, 32), (96, 72, 48), (136, 104, 64), (168, 128, 80),
                                (200, 152, 104), (224, 192, 136)],
                          leaf=[(48, 56, 24), (88, 96, 40), (136, 136, 64)], motif=["cable"],
                          water=[(14, 10, 14), (40, 28, 28)], seed=4453, denoise=0.5,
                          prompt="a burrow entrance under a ridge of packed earth, a bright red cable with a dark core "
                                 "running along the top edge of the earth bank, umber and ochre earth, warm brown tree "
                                 "trunks behind, ferns in front"),
    "rock_tunnel": dict(rock=[(12, 12, 30), (32, 32, 64), (48, 48, 88), (64, 64, 112), (88, 88, 136), (112, 112, 160),
                              (136, 144, 184)],
                        sky=[(10, 12, 36), (40, 48, 96)], skygrad=1,
                        leaf=[(12, 26, 34), (24, 46, 56), (40, 64, 76)], motif=["columns"], seed=4451, denoise=0.5,
                        prompt="a cave mouth at the foot of a cliff of tall basalt columns at night, deep indigo and "
                               "blue-black, cold moonless night sky, faint blue rim light, dark shrubs, no light "
                               "inside the cave"),
    "altering_cave": dict(rock=[(60, 46, 56), (108, 88, 100), (128, 106, 116), (148, 124, 132), (166, 142, 148),
                                (184, 160, 164), (214, 196, 198)], motif=["crystals"], seed=4452, denoise=0.5,
                          prompt="a cave mouth in mauve rose-grey rock by the sea, pale teal mineral crystals growing "
                                 "as columns out of the rock, glinting teal crystal clusters, blue sea and sky"),
    "power_plant": dict(rock=[(20, 26, 36), (48, 56, 72), (88, 104, 120), (120, 136, 152), (160, 176, 200),
                              (200, 212, 204)],
                        sky=[(88, 104, 120), (200, 212, 204)], leaf=[(40, 80, 40), (80, 128, 72), (128, 200, 104)],
                        motif=["lights"], seed=4452, denoise=0.5,
                        prompt="interior of an old power plant still running, machine housings and steel floor "
                               "plates, small bright green status lights on every machine, moss growing along the "
                               "seams of the floor, cool grey-blue metal and plant green, light from a high window"),
    "seafoam_islands": dict(rock=[(40, 72, 104), (64, 120, 152), (88, 152, 176), (136, 184, 192), (184, 208, 208),
                                  (236, 244, 236)],
                            leaf=[(48, 104, 112), (88, 152, 160), (150, 200, 200)], seed=4452, denoise=0.5,
                            prompt="a cave mouth in icy rocks by the sea, the ice covered with a powdery blue-green "
                                   "frosted bloom, chalky pale tops, clear deep blue-green faces, sea and sky"),
    "icefall_cave": dict(rock=[(24, 48, 88), (32, 80, 136), (48, 112, 168), (80, 152, 200), (128, 184, 216),
                               (176, 224, 240), (236, 250, 250)],
                         leaf=[(40, 88, 120), (80, 140, 180), (150, 200, 220)], motif=["mouth"],
                         mouth=(172, 112, 54, 46), seed=4455, denoise=0.5,
                         neg="icicles over the opening, closed wall",
                         prompt="a big dark cave mouth opening black at the foot of an ice cliff, right beside a "
                                "frozen waterfall, the waterfall turned to clear glassy ice hanging still down the "
                                "cliff, cold blue ice, pale winter sky, frosted shrubs"),
    "mt_ember": dict(rock=[(20, 14, 14), (40, 30, 30), (60, 46, 44), (84, 66, 60), (116, 96, 84), (170, 152, 134)],
                     white=[(150, 140, 130), (214, 204, 190)], motif=["cracks"],
                     peak=((80, 10, 200, 80), [(52, 48, 48), (84, 80, 78), (112, 106, 100), (132, 126, 118)]),
                     water=[(8, 4, 4), (28, 18, 18)], sky=[(150, 132, 120), (214, 198, 170)], skygrad=1,
                     seed=4451, denoise=0.45, neg="snow, snowy peak, snow cap, ice, white mountain",
                     prompt="a cave mouth in black cinder rock, cracks in the rock glowing low orange from inside "
                            "like banked coals, no flames, white steam rising, grey ash drifts, a smouldering "
                            "charcoal grey volcano behind, its slopes dark ash grey, under an ash haze"),
    "dotted_hole": dict(rock=[(72, 56, 48), (120, 96, 72), (160, 128, 96), (192, 168, 128), (216, 192, 160),
                              (240, 224, 192)],
                        leaf=[(80, 96, 48), (120, 136, 64), (168, 176, 96)], motif=["braille"], post=["braille"], seed=4451,
                        denoise=0.4,
                        neg="studs, pyramids, spikes, rivets, bolts, grid of squares",
                        prompt="a cave mouth in a sandstone mound framed by two pale stone pillars, lines of braille "
                               "carved on the stone, small round raised dots in separate cells of six, two columns "
                               "of three, a gap between cells, warm sandstone and shadow, clear sky"),
    # T-438 batch G's TANOBY chambers (2026-11-06, a DRAFT, the user away): vanilla's ruined facade graded through the
    # chambers' own dressed stone -- ochre and gold courses, slate shadow -- with a line of the invented script
    "monean_chamber": dict(rock=[(40, 40, 56), (82, 82, 106), (123, 115, 115), (156, 148, 90), (189, 172, 90),
                                 (205, 197, 106), (230, 222, 164), (246, 246, 222)],
                           leaf=[(56, 84, 64), (98, 131, 98), (150, 172, 120)], white="keep", motif=["script"], post=["script"],
                           seed=4451, denoise=0.45, neg="hieroglyphs, egyptian, letters, alphabet, runes glowing",
                           prompt="an ancient ruined shrine of dressed ochre and gold sandstone blocks on a small "
                                  "island, a dark square doorway with low steps, a band of small carved unknown "
                                  "glyphs along the stone, slate grey shadows, tufts of grass on the ruin, clear sky "
                                  "with soft clouds"),
}


#  the forests and the SAFARI (--places, drafted 2026-11-05): vanilla's composition graded through the colours each
#  place is built in now (sampled from reviewsheet's render of its maps), then painted as the caves were. "what" is the
#  look it is graded from; pattern_bush is a NEW card (THE SAME BUSH shows THE UNDERTONE's picture in the engine).
#  the user (2026-11-05): "They all look good, and we want to replace all Nintendo art, so I'd say all of them" -- with
#  THE UNDERTONE redrawn first, its light shaft clean of the olive-brown streaks (white_sat, and a new seed). THE SAME
#  BUSH's card is its own INCBIN now (sPatternBushMapPreview*, MPS_PATTERN_BUSH repointed to it).
PLACES_APPROVED = {"viridian_forest", "pattern_bush", "berry_forest", "safari_zone"}
UNDERTONE = [(16, 30, 22), (28, 52, 34), (42, 82, 44), (58, 112, 56), (88, 150, 80), (132, 188, 84)]
PLACES = {
    "viridian_forest": dict(
        what="THE UNDERTONE (batch F: its trunks, the grove's tell)",
        leaf=UNDERTONE, water=[(14, 26, 22), (30, 56, 44), (56, 92, 66)],
        sky=[(82, 112, 78), (150, 176, 120)], white=[(120, 150, 100), (186, 204, 150)],
        rock=[(20, 16, 14), (40, 32, 26), (66, 54, 40), (98, 84, 60), (134, 120, 86)], tex=0.10,
        white_sat=0.21,                 # the shaft's mint edge is light, not rock (it painted olive-brown streaks)
        seed=4493, denoise=0.48,        # 4480 drafted; 4490-4495 repainted on the clean start image, 4493 picked
        prompt="deep in a forest understory under a heavy dark green canopy, thick dark trunks with twisting "
               "branches, the light from above muted and low, faint dim green shafts, ferns and undergrowth in "
               "shadow, deep green and near-black, a quiet hum of shade",
        neg="bright sunlight, white light, blue sky, mountains, snow"),
    "pattern_bush": dict(
        what="THE SAME BUSH (batch H: salt scrub, gTileset_SameBush)", new=True, banner_from="viridian_forest",
        mps="MPS_PATTERN_BUSH", mapsec="MAPSEC_PATTERN_BUSH", type="MPS_TYPE_FOREST",
        leaf=[(40, 66, 60), (66, 99, 84), (98, 136, 116), (142, 176, 140), (186, 212, 180), (220, 234, 210)],
        water=[(52, 80, 76), (96, 128, 116), (150, 176, 160)], sky=[(176, 196, 192), (226, 234, 228)],
        white=[(206, 220, 210), (240, 244, 236)],
        rock=[(52, 48, 44), (88, 84, 74), (130, 126, 110), (176, 172, 150)], tex=0.10,
        seed=4481, denoise=0.50,
        prompt="a thicket of low salt scrub by the sea, dense round bushes of pale silvery grey-green all exactly "
               "alike, repeating, salt-white tips on the leaves, grey twisted stems, a pale sea haze behind",
        neg="tall trees, dark forest, bright green, sunbeams, mountains"),
    "berry_forest": dict(
        what="DENSE WOOD (batch H: the golden canopy)",
        rock=[(48, 38, 22), (92, 76, 34), (150, 138, 48), (206, 196, 88), (250, 244, 150)],
        leaf=[(40, 82, 38), (66, 128, 58), (88, 160, 84), (124, 192, 104)],
        white=[(236, 228, 150), (255, 252, 200)], sky=[(220, 212, 150), (250, 246, 206)], tex=0.10,
        seed=4482, denoise=0.48,
        prompt="inside a dense wood of crowded round golden yellow trees, thick canopies of yellow leaves pressed "
               "together, olive shadows between them, warm light through small gaps, green grass at the foot",
        neg="autumn red, orange leaves, blue sky, mountains"),
    "safari_zone": dict(
        what="the SAFARI (batch H: the grass, LURID's chartreuse canopy)",
        leaf=[(42, 82, 44), (66, 128, 58), (112, 204, 41), (189, 242, 74), (231, 255, 74)],
        rock=[(96, 84, 60), (150, 140, 110), (196, 192, 170), (224, 224, 212)], tex=0.10,
        seed=4483, denoise=0.48,
        prompt="a wide savanna park, one flat-topped acacia tree with an acid chartreuse canopy, tall bright green "
               "grass, a sandy path with a row of wooden fence posts, a pond far off, low hills and a pale blue sky",
        neg="buildings, cars, animals, people"),
}

# ================================================================== reading the engine
def previews():
    """[(MPS key, MAPSEC, type, folder)] from sMapPreviewScreenData, in its order"""
    src = open(os.path.join(GBA, "src/map_preview_screen.c")).read()
    var2dir = dict(re.findall(r"static const u8 (s\w+?)MapPreviewTiles\[\] = INCBIN_U8\(\"graphics/map_preview/(\w+)/", src))
    out = []
    for key, body in re.findall(r"\[(MPS_\w+)\]\s*=\s*\{(.*?)\}", src, re.S):
        sec = re.search(r"\.mapsec = (\w+)", body).group(1)
        typ = re.search(r"\.type = (\w+)", body).group(1)
        var = re.search(r"\.tilesptr = (s\w+?)MapPreviewTiles", body).group(1)
        out.append((key, sec, typ, var2dir[var]))
    return out


def names():
    d = json.load(open(os.path.join(GBA, "src/data/region_map/region_map_sections.json")))["map_sections"]
    return {s["id"]: s.get("name", "") for s in d}


def maps_of(mapsec):
    out = []
    root = os.path.join(GBA, "data/maps")
    for m in sorted(os.listdir(root)):
        p = os.path.join(root, m, "map.json")
        if os.path.exists(p) and json.load(open(p)).get("region_map_section") == mapsec:
            out.append(m)
    return out


def name_width(s):
    w, cm = fontwidth.font()
    return sum(w[cm[c]] if c in cm and cm[c] < len(w) else 0 for c in s)


def _pret(rel):
    """a file as pret ships it (upstream/master), never the working tree's: once --write has run, the engine's own
    graphics/map_preview/<cave>/ holds OUR picture, and reading that back as 'vanilla' would make every later run
    grade, reduce and light from our own output (the tool would drift from itself)"""
    import subprocess
    r = subprocess.run(["git", "-C", os.path.realpath(GBA), "show", "upstream/master:" + rel], capture_output=True)
    if r.returncode:
        sys.exit("  !! git show upstream/master:%s failed: %s" % (rel, r.stderr.decode().strip()))
    return r.stdout


def cfg(folder):
    """a card's entry: LANDMARK's, PLACES' or PAINT's (a cave's)"""
    return CARDS.get(folder) or LANDMARK.get(folder) or PLACES.get(folder) or PAINT.get(folder, {})


def van(folder):
    """vanilla(folder), or for a NEW card (T-456: no vanilla picture) the card it borrows its letterbox, banner and
    palette 14 from"""
    return vanilla(cfg(folder).get("banner_from", folder))


def vanilla(folder):
    """(tiles [64 indices each], tilemap entries [640], palette [32 rgb]) as pret's build makes them: its tiles.png
    cut into 8x8 tiles row by row (the first -num_tiles of them, each index's low nibble, as gbagfx keeps it), its
    tilemap.bin, and the png's palette at the GBA's 5 bits"""
    im = Image.open(io.BytesIO(_pret("graphics/map_preview/%s/tiles.png" % folder)))
    rule = re.search(r"/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles (\d+)" % folder,
                     _pret("graphics_file_rules.mk").decode())
    px, (W, H) = im.load(), im.size
    #  a card with no -num_tiles rule (cerulean_cave: its tiles.png is cut to its count) is every tile gbagfx reads
    n = int(rule.group(1)) if rule else (W // 8) * (H // 8)
    tiles = []
    for ty in range(H // 8):
        for tx in range(W // 8):
            tiles.append([px[tx * 8 + x, ty * 8 + y] & 15 for y in range(8) for x in range(8)])
    pal = im.getpalette()[:96]
    pal = [((pal[i] >> 3) << 3, (pal[i + 1] >> 3) << 3, (pal[i + 2] >> 3) << 3) for i in range(0, 96, 3)]
    m = list(struct.unpack("<640H", _pret("graphics/map_preview/%s/tilemap.bin" % folder)))
    return tiles[:n], m, pal


def compose(tiles, m, pal):
    """the 240x160 screen these make (palettes 13 and 14 from pal)"""
    im = Image.new("RGB", (240, 160))
    px = im.load()
    for ty in range(20):
        for tx in range(30):
            e = m[ty * 32 + tx]
            t, hf, vf, p = tiles[e & 0x3FF] if (e & 0x3FF) < len(tiles) else [0] * 64, e & 0x400, e & 0x800, e >> 12
            base = (p - 13) * 16 if p in (13, 14) else 16
            for y in range(8):
                for x in range(8):
                    c = t[(7 - y if vf else y) * 8 + (7 - x if hf else x)]
                    px[tx * 8 + x, ty * 8 + y] = pal[base + c]
    return im


# ================================================================== the font, for the sheet
_FONT = None


def draw_name(im, name, pal):
    """MapPreview_CreateMapNameWindow: a 104x16 window at (0,0) filled with colour 1 of palette 14, the name centred,
    text colour 2 and shadow 3 -- drawn with the game's own glyphs"""
    global _FONT
    if _FONT is None:
        _FONT = Image.open(os.path.join(GBA, "graphics/fonts/latin_normal.png"))
    w, cm = fontwidth.font()
    p14 = pal[16:32]
    #  the window's colours: fill TEXT_COLOR_WHITE (1), text TEXT_COLOR_RED (4 -- black in this palette), shadow
    #  TEXT_COLOR_LIGHT_GRAY (3); the font sheet draws its glyph in 1, its shadow in 2, its cell in 3
    ink = {1: p14[4], 2: p14[3]}
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 103, 15), fill=p14[1])
    x = (104 - name_width(name)) // 2
    px, fp = im.load(), _FONT.load()
    for ch in name:
        b = cm.get(ch)
        if b is None:
            continue
        gx, gy = (b % 16) * 16, (b // 16) * 16
        for yy in range(16):
            for xx in range(min(16, w[b])):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, 2 + yy
                if v in ink and 0 <= X < 104 and Y < 16:
                    px[X, Y] = ink[v]
        x += w[b]


# ================================================================== painting (T-445: painted entrances)
def _lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def _region(c, white_sat=0.12):
    """what a pixel of vanilla's painting is: rock (and the ground), white (a lit rock or a cloud), leaf, sky, water.
    white_sat (a place's "white_sat"): how grey a bright pixel may be and still be light -- vanilla's forest edges its
    light shaft in a pale mint (200, 240, 192: saturation 0.20) that the default reads as rock, and the rock ramp
    graded it into olive-brown streaks down the shaft (the user, 2026-11-05)"""
    import colorsys
    h, sat, v = colorsys.rgb_to_hsv(*[x / 255 for x in c])
    h *= 360
    if sat < white_sat and v > 0.85:
        return "white"
    if 75 <= h <= 170 and sat > 0.2:
        return "leaf"
    if 180 <= h <= 250 and sat > 0.15:
        return "sky" if v > 0.75 else "water"
    return "rock"


def _ramp(r, t):
    t = min(max(t, 0.0), 1.0) * (len(r) - 1)
    i = min(int(t), len(r) - 2)
    f = t - i
    return tuple(int(r[i][k] + (r[i + 1][k] - r[i][k]) * f) for k in range(3))


def paint_init(folder, sec):
    """the start image: vanilla's picture (rows 3..16) graded through the cave's ramps, the top-down view's light laid
    faintly into the rock, at the painting's size"""
    c = cfg(folder)
    vt, vm, vpal = van(folder)
    v = compose(vt, vm, vpal).crop((0, 24, 240, 136))
    td, _ = picture(folder, sec, painted=False)
    px, dp = v.load(), td.convert("RGB").load()
    W, H = v.size
    lums = collections.defaultdict(list)
    for y in range(H):
        for x in range(W):
            lums[_region(px[x, y], c.get("white_sat", 0.12))].append(_lum(px[x, y]))
    rng = {k: (min(l), max(l)) for k, l in lums.items()}
    rock_lo, rock_hi = rng["rock"][0], max(rng["rock"][1], rng.get("white", (0, 0))[1])
    dl = [_lum(dp[x, y]) for y in range(H) for x in range(W)]
    mu = sum(dl) / len(dl)
    sd = (sum((l - mu) ** 2 for l in dl) / len(dl)) ** 0.5 or 1
    out = v.copy()
    op = out.load()
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            k = _region(p, c.get("white_sat", 0.12))
            if k == "white":
                if c.get("white") == "keep":
                    continue
                if not isinstance(c.get("white"), list):
                    k = "rock"
            r = c.get(k)
            pk = c.get("peak")
            if pk and k in ("white", "rock") and pk[0][0] <= x < pk[0][2] and pk[0][1] <= y < pk[0][3] \
                    and _region(p) == "white":
                op[x, y] = _ramp(pk[1], (_lum(p) - 200) / 55)        # the far peak in ash, never snow
                continue
            if not r:
                continue
            if k == "sky" and c.get("skygrad"):
                op[x, y] = _ramp(r, y / H)
                continue
            lo, hi = (rock_lo, rock_hi) if k == "rock" else rng[k]
            if k == "white":
                lo = min(lo, 200)
            t = (_lum(p) - lo) / max(1, hi - lo)
            if k == "rock":
                t += c.get("tex", 0.22) * (_lum(dp[x, y]) - mu) / sd / 3
            op[x, y] = _ramp(r, t)
    for m in c.get("motif", []):
        MOTIFS[m](out, v, c)
    return out.resize(PAINT_SIZE, Image.BICUBIC)


#  the cave's one idea, laid into the start image at 2px so it survives the painting (the server's own pixel is
#  about 8px at 1088, near 2px here): what the top-down view says in tiles, said where the painting can keep it
def _rockmask(v, ymin=0):
    px = v.load()
    return lambda x, y: (0 <= x < 240 and ymin <= y < 112 and _region(px[x, y]) in ("rock", "white")
                         and _lum(px[x, y]) > 80 and px[x, y][2] <= px[x, y][0] + 6)     # not a pale sky


def _shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def motif_courses(out, v, c):
    """THE STACK: thin courses of slab, every other a shade darker, a joint now and then, a gold connector strip"""
    import random
    rnd, op, rock = random.Random(445), out.load(), _rockmask(v)
    for x in range(240):
        off = (x // 22) * 3 % 7
        for y in range(112):
            if not rock(x, y):
                continue
            ph = (y + off) % 7
            band = ((y + off) // 7) % 2
            if ph == 0:
                op[x, y] = _shade(op[x, y], 0.55)
            elif ph == 1:
                gold = (x // 11 * 7 + (y + off) // 7 * 13) % 9 == 0
                op[x, y] = (196, 164, 76) if gold else _shade(op[x, y], 1.18)
            elif band:
                op[x, y] = _shade(op[x, y], 0.9)
        if x % 22 == 0:
            for y in range(112):
                if rock(x, y) and rnd.random() < 0.5:
                    op[x, y] = _shade(op[x, y], 0.6)


def motif_cable(out, v, c):
    """THE LINE: the buried cable along the top of the bank, a red sheath over a dark core"""
    px, op = v.load(), out.load()
    for x in range(240):
        for y in range(14, 80):
            if _region(px[x, y]) == "leaf":
                for k, col in enumerate([(220, 110, 80), (192, 80, 56), (150, 56, 40), (48, 24, 24)]):
                    if y + 2 + k < 112:
                        op[x, y + 2 + k] = col
                break


def motif_columns(out, v, c):
    """THE OUTAGE: basalt cut in tall columns, a lit left edge and a dark right one; the mouth gone fully black"""
    px, op, rock = v.load(), out.load(), _rockmask(v)
    for y in range(112):
        for x in range(240):
            if _region(px[x, y]) in ("rock", "water") and _lum(px[x, y]) < 80 and y > 50:
                op[x, y] = (4, 4, 14)
            elif rock(x, y):
                ph = (x + (y // 40) * 4) % 10
                if ph in (0, 1):
                    op[x, y] = _shade(op[x, y], 1.35)
                elif ph in (8, 9):
                    op[x, y] = _shade(op[x, y], 0.5)


def motif_crystals(out, v, c):
    """OTHER CAVE: teal mineral columns grown out of the mauve rock"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v, 30)
    d = ImageDraw.Draw(out)
    placed = 0
    while placed < 14:
        x, y = rnd.randrange(130, 236), rnd.randrange(34, 104)
        if not rock(x, y):
            continue
        placed += 1
        for k in range(rnd.randint(2, 3)):
            cx, h, w = x + k * 5 - 4, rnd.randint(8, 18), 4
            top = y - h
            d.polygon([(cx, y), (cx, top + 2), (cx + w // 2, top), (cx + w, top + 2), (cx + w, y)], fill=(104, 160, 152))
            d.rectangle((cx, top + 2, cx + 1, y), fill=(168, 216, 208))
            d.line((cx + w, top + 2, cx + w, y), fill=(40, 70, 72))


def motif_cracks(out, v, c):
    """EMBER UNDER ASH: cracks that glow low orange from inside, never flame"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v, 20)
    px = v.load()
    n = 0
    while n < 16:
        x, y = rnd.randrange(0, 240), rnd.randrange(20, 112)
        if not (rock(x, y) or _region(px[x, y]) == "rock") or _lum(op[x, y]) > 70:      # the near rock, not the far
            continue
        n += 1
        for _ in range(rnd.randint(14, 30)):
            for dx, col in ((-1, (150, 56, 28)), (0, (252, 184, 72)), (1, (236, 128, 40)), (2, (150, 56, 28))):
                if 0 <= x + dx < 240 and 0 <= y < 112:
                    op[x + dx, y] = col
            x += rnd.choice((-1, 0, 1))
            y += rnd.choice((0, 1, 1))
            if not (0 <= x < 239 and y < 111):
                break


def motif_braille(out, v, c):
    """BRAILLE: lines of six-dot cells over the stone, writing for the hand -- round dots (a 4px disc, lit above, shadowed
    below), two columns of three, a wide gap between cells and between lines, so each cell reads as a cell and not a
    grid of studs; every cell has at least two dots and never all six"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v)
    DISC = [(1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3)]
    for cy in range(4, 96, 25):
        for cx in range(2, 230, 17):
            cell = []
            while not 2 <= len(cell) <= 5:
                cell = [(q, r) for r in range(3) for q in range(2) if rnd.random() < 0.5]
            for q, r in cell:
                x, y = cx + q * 6, cy + r * 6
                if not all(rock(x + a, y + b) for a, b in DISC):
                    continue
                base = op[x + 1, y + 1]
                for a, b in DISC:
                    op[x + a, y + b] = _shade(base, 1.2 if b < 2 and a < 3 else 0.6)
                op[x + 1, y], op[x, y + 1] = (252, 244, 220), (252, 244, 220)
                op[x + 2, y + 3], op[x + 3, y + 2] = _shade(base, 0.4), _shade(base, 0.4)


def motif_mouth(out, v, c):
    """STILLFALL: a clear cave mouth beside the frozen fall -- a ragged black opening in the ice cliff, shaded in from
    its edge, so the painting keeps an opening (vanilla's own mouth is too faint to survive the ice)"""
    import math, random
    rnd = random.Random(4454)
    cx, base, w, h = c["mouth"]
    d = ImageDraw.Draw(out)
    for k, col in enumerate([(48, 96, 150), (20, 40, 72), (6, 12, 28)]):
        s, pts = 1 - k * 0.16, []
        for i in range(25):
            t = math.pi * i / 24
            j = rnd.uniform(-3, 3) * s
            pts.append((cx - math.cos(t) * (w / 2 * s + j), base - math.sin(t) * (h * s + j)))
        d.polygon(pts + [(cx + w / 2 * s, base + 1), (cx - w / 2 * s, base + 1)], fill=col)


def motif_lights(out, v, c):
    """STILL RUNNING: a green status light on every housing, nobody connected to see it"""
    import random
    rnd, op = random.Random(4451), out.load()
    n = 0
    while n < 22:
        x, y = rnd.randrange(2, 236), rnd.randrange(8, 100)
        if not (x < 110 or x > 170) or not all(30 < _lum(op[x + a, y + b]) < 150 for a in range(3) for b in range(2)):
            continue
        n += 1
        for a in range(3):
            for b in range(2):
                op[x + a, y + b] = (200, 255, 176) if (a, b) == (0, 0) else (96, 232, 88)


def motif_script(out, v, c):
    """THE TANOBY CHAMBERS (batch G): lines of an invented script carved in the stone -- each glyph a few incised
    strokes in a 5x7 cell (dark cut, lit lower lip), a gap between glyphs and between lines, never a letter's shape"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v)
    STROKES = [[(0, y) for y in range(7)], [(4, y) for y in range(7)], [(x, 0) for x in range(5)],
               [(x, 3) for x in range(5)], [(x, 6) for x in range(5)], [(x, x + 1) for x in range(5)],
               [(2, y) for y in range(2, 7)], [(x, 4 - x) for x in range(5)]]
    for cy in range(38, 90, 24):
        for cx in range(4, 232, 9):
            pts = set()
            for st in rnd.sample(STROKES, rnd.choice((2, 3))):
                pts.update(st)
            if not all(rock(cx + a, cy + b) for a in range(-1, 6) for b in range(-1, 8)):
                continue
            for a, b in pts:
                base = op[cx + a, cy + b]
                op[cx + a, cy + b] = _shade(base, 0.45)
                if (a, b + 1) not in pts and b + 1 < 8:
                    op[cx + a, cy + b + 1] = _shade(op[cx + a, cy + b + 1], 1.18)


MOTIFS = dict(lights=motif_lights, courses=motif_courses, cable=motif_cable, columns=motif_columns, crystals=motif_crystals,
              cracks=motif_cracks, braille=motif_braille, mouth=motif_mouth, script=motif_script)


# ================================================================== the landmarks' cards (T-445, 2026-10-25)
#  The user (2026-10-25): "the name card on entering still shows vanilla's pictures for the landmarks -- FOUNDRY CO.
#  over SILPH CO.'s, DAEMON TOWER over POKEMON TOWER's; paint them from the new buildings (and SCORN SOLUTIONS' / the
#  MANSION's if they have cards)." Three of T-447's landmarks have a card: CORPUS's tower (silph_co), DAEMON TOWER
#  (pokemon_tower) and the MANSION (pokemon_mansion). SCORN SOLUTIONS (the lab), the REVIEW BOARD (INDIGO PLATEAU)
#  and ERRATA (the museum) have none: sMapPreviewScreenData has no entry for their mapsecs.
#
#  The cave method, with the building in place of vanilla's: the start image is vanilla's card graded through the
#  town's colours (its trees, rocks and sky keep vanilla's composition), with a column cleared to sky where vanilla's
#  building stood, and the NEW building -- exactly as the engine draws it (gbalandmarks' drawing, checked pixel for
#  pixel against reviewsheet's render of the built map, or cut from that render) -- laid in seen from below: a
#  homography takes its rectangle to a keystone (wide at the foot, narrow at the crown), so the floors foreshorten as
#  vanilla's painted towers do. The MANSION's card is vanilla's hall INSIDE; there is no outside to grade, so its scene
#  is drawn (an ash sky, CINNABAR's sea behind, the sand) and the burned facade laid over it. The sprite server then
#  repaints it, image to image, at a denoise low enough that our building survives. Nothing here is written to the
#  engine until the user approves a card (LANDMARK_APPROVED).
LANDMARK_APPROVED = {"silph_co", "pokemon_tower", "pokemon_mansion",   # the user, 2026-10-26: build all three as drawn
                     "rocket_hideout",                                 # the user, 2026-10-26: CORPUS HIDEOUT as drawn
                     "rocket_warehouse",                               # the user, 2026-10-26: CORPUS WAREHOUSE, candidate B
                     "review_board"}                                   # the user, 2026-10-26 (T-456): seed C, the hall neutral
LANDMARK_DRAWINGS = os.path.join(ROOT, "gfx", "drafts", "landmarks")
GREYS = [(40, 40, 46), (72, 72, 80), (108, 108, 116), (148, 148, 156), (188, 188, 194), (222, 222, 226)]
LANDMARK = {
    "silph_co": dict(
        source="corpus_tower", title="CORPUS's tower (FOUNDRY CO.)",
        clear=(46, 206), floor=104, quad=((46, 114), (194, 114), (166, 2), (74, 2)),
        sky=[(150, 176, 196), (214, 222, 220), (238, 232, 212)], skygrad=1,
        leaf=[(36, 52, 34), (66, 84, 48), (104, 118, 64), (150, 156, 96)],
        rock=[(80, 72, 60), (128, 116, 96), (176, 164, 140), (212, 202, 180)],
        seed=4464, denoise=0.46, post=["redband"], force=[(198, 34, 44)],
        prompt="looking up at a tall office tower clad in brass sheet with rows of rivets, one strict grid of identical "
               "small square windows all lit warm, a stepped octagonal brass crown with one thin red band, a glass "
               "lobby at its foot, dark bronze trees at the sides, pale warm sky",
        neg="glass curtain wall, blue glass, sign, lettering"),
    "pokemon_tower": dict(
        source="daemon_tower", title="DAEMON TOWER",
        clear=(52, 200), floor=108, quad=((48, 122), (192, 122), (160, 0), (80, 0)),
        sky=[(168, 168, 178), (214, 214, 220), (236, 236, 240)], skygrad=1,
        leaf=[(52, 56, 58), (88, 92, 94), (128, 132, 132), (168, 170, 170)], rock=GREYS,
        seed=4467, denoise=0.50,
        prompt="looking up at a pale round stone tower made of halftone dots, dense dark dots at its foot thinning "
               "to sparse dots at the top, seven bands of small arched niches each holding a tiny candle flame, a "
               "dotted dome with a thin spire, a dark doorway, grey rocks and grey pines at the sides, overcast grey "
               "sky, monochrome grey with only the small warm candle flames",
        neg="colour, green, blue sky, pagoda, tiers, roof eaves, candle on the ground, flame at the door, fire"),
    "pokemon_mansion": dict(
        source="mansion", title="the MANSION", drawn_scene=True,
        quad=((30, 122), (210, 122), (198, 8), (42, 8)),
        sky=[(122, 112, 108), (170, 160, 150), (208, 198, 184)], sea=[(40, 64, 88), (72, 104, 128)],
        sand=[(150, 132, 98), (196, 178, 136)],
        seed=4468, denoise=0.45,
        prompt="looking up at a burned grey stone mansion, its roof caved in at the middle where curved grey metal "
               "racks show like the ribs of a rib cage against the black, one big black soot stain spreading up the "
               "wall from the doorway to the cave-in, four dark square windows, worn stone steps to a black doorway, "
               "cold and long burnt out, an ash grey hazy sky, a dark sea behind, sand in front",
        neg="fire, flames, glow, embers, orange light, arched windows, green grass, bright colours, sign"),
    #  CORPUS's two interiors (the user, 2026-10-26: "draft CORPUS HIDEOUT's and the WAREHOUSE's cards now from the
    #  current maps"). Neither has a T-447 building and both cards are vanilla's rooms INSIDE, so the start image is
    #  vanilla's room graded through the colours the rooms are drawn in now (the SilphCo tileset both maps use: teal
    #  wall, slate machines, olive floor, white desks, wood), vanilla's ROCKET "R" taken off the wall (ERASE: each box
    #  filled with the panel's own colour, sampled at FILL), and for the WAREHOUSE its one idea laid on the floor: the
    #  spin tiles, cut from the built map. DRAFTS: not in LANDMARK_APPROVED.
    "rocket_hideout": dict(
        source="RocketHideout_B1F", title="CORPUS HIDEOUT", interior=True,
        erase=[((0, 36, 20, 64), (3, 30))], floor_from=95,      # vanilla's pale floor: olive, as the map's is
        seed=4470, denoise=0.45,
        prompt="inside a quiet underground office, pale teal metal wall panels, an open doorway into a small room "
               "with a computer on a desk and a swivel chair, a plain white wall, a slate grey elevator door at the "
               "right with a small stairs sign, olive green floor, a strip of fluorescent ceiling light",
        neg="letter R, logo, emblem, red, people"),
    "rocket_warehouse": dict(
        source="FiveIsland_RocketWarehouse", title="CORPUS WAREHOUSE", interior=True,
        erase=[((0, 33, 29, 93), (2, 30)), ((29, 33, 43, 93), (35, 30))],
        #  the user (2026-10-26): "repaint with a bigger spin-tile floor that reads at 1x". The first draft's floor
        #  was a 12px strip of ten tiles a row and washed out; the room is lifted 12 rows (its ceiling strip goes) and
        #  the floor laid 26px deep, eight tiles a row at the foot, painted at 0.40. post=["spinfloor"] (with the two
        #  arrow greens in force) lays them back crisp after the painting instead -- the other candidates on sheet
        #  t445w_repaint. The user approved candidate B (2026-10-26): in LANDMARK_APPROVED.
        lift=12, floor_tiles=dict(quad=((-8, 112), (248, 112), (222, 86), (18, 86)), cols=8, rows=2),
        seed=4472, denoise=0.40,
        prompt="inside a corporate warehouse, riveted teal metal wall panels, a wooden cage of white bars, a white "
               "steel door, cardboard boxes, an olive floor laid with green arrow floor tiles, fluorescent ceiling "
               "light",
        neg="letter R, logo, emblem, red, people"),
    #  T-456 (the user, 2026-10-26): the REVIEW BOARD gets a card. UMBRA PLATEAU (MAPSEC_INDIGO_PLATEAU) has NO entry
    #  in sMapPreviewScreenData and no vanilla picture, so this one is NEW: "mapsec" names it, "banner_from" lends the
    #  letterbox, the banner and palette 14 (every card but the SAFARI's has the same ones, byte for byte), and the
    #  scene is drawn ("plateau": a dusk sky pale at the horizon so the near-black hall reads against it, the
    #  plateau's trees at the sides in UMBRA's greens, its grass at the foot). The hall is cut from reviewsheet's
    #  render of the built map (engine 2332f9e44) -- the 11x7 box and the dark porch, the kept blue door in it --
    #  and laid in seen from below. The four vessels are the only colour: after the painting the fluids and the kept
    #  door are laid back crisp (post_vessels), and "force" gives the red, the yellow, the pale, the door's blue, the
    #  black fluid and the hall's own stone (46,44,54) an index each -- without the last two, median cut shared the
    #  trees' dark greens with the hall and tinted it, and vessel III went green. BUILT (engine 64d79bbf4): the
    #  engine has its entry now (MPS_INDIGO_PLATEAU); --write skips a "new" card only while the engine has none.
    "review_board": dict(
        source="review_board", title="the REVIEW BOARD", new=True, mapsec="MAPSEC_INDIGO_PLATEAU",
        mps="MPS_INDIGO_PLATEAU", type="MPS_TYPE_CAVE", banner_from="pokemon_tower", drawn_scene="plateau",
        quad=((44, 114), (196, 114), (184, 0), (56, 0)),
        sky=[(58, 52, 76), (98, 90, 118), (150, 144, 168), (202, 198, 212)],
        leaf=[(22, 40, 26), (38, 64, 36), (62, 92, 46), (96, 124, 58)],
        grass=[(46, 78, 38), (74, 110, 50), (104, 140, 66)],
        seed=4475, denoise=0.45, post=["vessels"],     # seeds 4473 and 4474 on sheet t456_draft; 4475 picked
        force=[(192, 28, 36), (222, 178, 30), (218, 220, 206), (98, 164, 222), (6, 4, 8), (46, 44, 54)],
        #  the user (2026-10-26, building seed C): keep the hall neutral -- its front shared the trees' darkest shade
        #  (a teal-green near-black) and read faintly green; that shade is given up for a neutral near-black, and the
        #  trees' deepest shadows take it too
        neutral=(18, 18, 22),
        prompt="looking up at a long low hall of near-black stone under one heavy flat stone slab that overhangs it "
               "like a judges' bench, four small lit alcoves in its front each holding a tall glass vessel of "
               "fluid, red, yellow, black, pale, left to right, a dark doorway in the middle with a small blue door, "
               "a dark stone step in front, dark green trees at the sides, grass, a dusk sky pale at the horizon",
        neg="windows, columns, pediment, roof tiles, sign, lettering, fire, bright colours"),
}
#  the SilphCo tileset's colours as the two CORPUS interiors draw them (sampled from reviewsheet's render)
INTERIOR_RAMPS = dict(
    wall=[(52, 82, 90), (82, 124, 132), (106, 164, 172), (156, 196, 200), (197, 205, 213)],
    slate=[(57, 57, 74), (82, 82, 106), (98, 98, 123), (139, 139, 148), (180, 180, 190)],
    floor=[(98, 98, 60), (131, 131, 82), (164, 164, 98), (197, 197, 156)],
    white=[(164, 164, 172), (197, 205, 213), (238, 238, 246), (255, 255, 255)],
    wood=[(132, 90, 58), (164, 116, 74), (220, 178, 128), (246, 230, 190)])


def landmark_source(folder):
    c = LANDMARK[folder]
    return ("the current %s" % c["source"]) if c.get("interior") else ("T-447's %s" % c["source"])


def _interior_region(p):
    import colorsys
    h, sat, v = colorsys.rgb_to_hsv(*[x / 255 for x in p])
    h *= 360
    if sat < 0.10:
        return "white"
    if 10 <= h < 38 and sat >= 0.15:
        return "wood"
    if 38 <= h < 75:
        return "floor"
    if 75 <= h < 200:
        return "wall"
    return "slate" if v < 0.7 else "white"


def interior_scene(folder):
    """CORPUS's rooms: vanilla's room, the R taken off, graded through INTERIOR_RAMPS region by region"""
    c = LANDMARK[folder]
    vt, vm, vpal = vanilla(folder)
    v = compose(vt, vm, vpal).crop((0, 24, 240, 136))
    vp = v.load()
    for (x0, y0, x1, y1), (fx, fy) in c.get("erase", []):
        fill = vp[fx, fy]
        for y in range(y0, y1):
            for x in range(x0, x1):
                vp[x, y] = fill
    def region(x, y):
        k = _interior_region(vp[x, y])
        return "floor" if k == "white" and y >= c.get("floor_from", 112) else k

    lums = collections.defaultdict(list)
    for y in range(112):
        for x in range(240):
            lums[region(x, y)].append(_lum(vp[x, y]))
    rng = {k: (min(l), max(l)) for k, l in lums.items()}
    bg = Image.new("RGB", (240, 112))
    px = bg.load()
    for y in range(112):
        for x in range(240):
            k = region(x, y)
            lo, hi = rng[k]
            px[x, y] = _ramp(INTERIOR_RAMPS[k], (_lum(vp[x, y]) - lo) / max(1, hi - lo))
    lift = c.get("lift", 0)
    if lift:                    # the room raised LIFT rows (its ceiling strip goes), so the floor has room to be seen
        bg.paste(bg.crop((0, lift, 240, 112)), (0, 0))
        ImageDraw.Draw(bg).rectangle((0, 112 - lift, 239, 111), fill=_ramp(INTERIOR_RAMPS["floor"], 0.55))
    return bg


def interior_floor(folder):
    """(RGBA) the WAREHOUSE's floor as the built map draws it: its own floor block, and the spin tiles cut from the
    map (every block of the map drawn with the arrows' green), laid COLS x ROWS in their order on the map"""
    c = LANDMARK[folder]
    ft = c["floor_tiles"]
    l = RS.layout_of(c["source"])
    img = RS.render(l).convert("RGB")
    W, H = l["width"], l["height"]
    bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    green = {(82, 222, 123), (131, 255, 164)}
    arrows, floor, seen = [], collections.Counter(), set()
    #  a spin tile is 56 of its 256 pixels green; a computer or a door carries 2 (their screens' LEDs), so a block is
    #  an arrow only where green is a real share of it
    for yy in range(H):
        for xx in range(W):
            m = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
            cell = img.crop((xx * 16, yy * 16, xx * 16 + 16, yy * 16 + 16))
            cols = set(cell.getdata())
            if sum(p in green for p in cell.getdata()) >= 16:
                if m not in seen:
                    seen.add(m)
                    arrows.append(cell)
            elif cols <= {(131, 131, 82), (164, 164, 98), (197, 197, 156)}:
                floor[cell.tobytes()] += 1
    base = Image.frombytes("RGB", (16, 16), floor.most_common(1)[0][0])
    out = Image.new("RGBA", (ft["cols"] * 16, ft["rows"] * 16))
    for r in range(ft["rows"]):
        for q in range(ft["cols"]):
            t = arrows[(q + 2 * r) % len(arrows)] if arrows and (q + r) % 3 else base
            out.paste(t, (q * 16, r * 16))
    return out


def _homography(src, dst):
    """the 8 coefficients PIL's PERSPECTIVE wants: each OUTPUT point (dst) to its INPUT point (src)"""
    import numpy as np
    a, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return list(np.linalg.solve(np.array(a, float), np.array(b, float)))


def landmark_drawing(src):
    """(RGBA) the building as the engine draws it now. corpus_tower and daemon_tower: gbalandmarks' 1x drawing (the
    whole tower on one canvas, DAEMON TOWER's dome from ROUTE 10's rows), which this checks against reviewsheet's
    render of the built map, pixel for pixel where the drawing is opaque. The MANSION: cut from that render (its 7x4
    cells and the three cells of its steps)."""
    if src == "review_board":
        #  T-456: cut from the built map, the 11x7 box at (6,0) and the porch's 3x2 cells below it; the plateau's
        #  grass (under the overhang, at the hall's sides, round the porch) left out, so the scene shows through
        l = RS.layout_of("IndigoPlateau_Exterior")
        img = RS.render(l).convert("RGBA").crop((6 * 16, 0, 17 * 16, 9 * 16))
        px = img.load()
        for y in range(144):
            for x in range(176):
                r, g, b_, _ = px[x, y]
                #  below the box only the porch's dark stone: not the grass round it, not the path on its row 8
                if (y >= 112 and (not 64 <= x < 112 or y > 132 or r + g + b_ > 330)) or (g > r + 16 and g > b_):
                    px[x, y] = (0, 0, 0, 0)
        return img
    if src == "mansion":
        l = RS.layout_of("CinnabarIsland")
        img = RS.render(l).convert("RGBA").crop((5 * 16, 0, 12 * 16, 5 * 16))
        px = img.load()
        for y in range(64, 80):
            for x in range(112):
                r, g, b_, _ = px[x, y]
                if not 32 <= x < 80 or g > r + 16:                  # the steps, not the grass round them
                    px[x, y] = (0, 0, 0, 0)
        return img
    im = Image.open(os.path.join(LANDMARK_DRAWINGS, src, "drawing_1x.png")).convert("RGBA")
    mp, x0, y0 = {"corpus_tower": ("SaffronCity", 29, 16), "daemon_tower": ("LavenderTown", 15, 0)}[src]
    cut = {"daemon_tower": 128}.get(src, 0)                       # the drawing's rows above the town map are ROUTE 10's
    r = RS.render(RS.layout_of(mp)).convert("RGB")
    a, b = im.load(), r.load()
    bad = sum(1 for y in range(cut, im.size[1]) for x in range(im.size[0])
              if a[x, y][3] == 255 and a[x, y][:3] != b[x0 * 16 + x, y0 * 16 + y - cut])
    if bad:
        sys.exit("  !! %s: gbalandmarks' drawing differs from the built map at %d pixels -- redraw from the map" % (src, bad))
    return im


def _grade(c, k, p, lo, hi):
    r = c.get(k)
    return _ramp(r, (_lum(p) - lo) / max(1, hi - lo)) if r else p


def plateau_scene(c):
    """T-456's drawn scene: UMBRA PLATEAU at dusk -- the sky graded down to a pale horizon (so the near-black hall
    reads against it), the plateau's grass from the horizon down, and the trees that flank the hall on the map as
    dark rounded masses at both sides, stepping down towards the middle"""
    bg = Image.new("RGB", (240, 112))
    px = bg.load()
    HZ = 86
    for y in range(112):
        for x in range(240):
            px[x, y] = _ramp(c["sky"], y / HZ) if y < HZ else _ramp(c["grass"], 1 - (y - HZ) / 26)
    d = ImageDraw.Draw(bg)
    import random
    rnd = random.Random(456)
    for side in (0, 1):
        for k in range(14):
            cx = rnd.randint(-10, 44)
            cy = rnd.randint(18, 96) + int(cx * 0.3)
            r = rnd.randint(12, 22)
            x = cx if side == 0 else 239 - cx
            for j, f in enumerate((0.0, 0.35, 0.7)):
                rr = r - j * 4
                ox = (-3 if side else 3) * j
                d.ellipse((x - rr + ox, cy - rr - j * 3, x + rr + ox, cy + rr - j * 3), fill=_ramp(c["leaf"], f))
    return bg


def landmark_init(folder):
    """the start image for a landmark's card, at the painting's size"""
    from PIL import ImageFilter
    c = LANDMARK[folder]
    K = PAINT_SIZE[0] / 240
    if c.get("interior"):
        bg = interior_scene(folder)
    elif c.get("drawn_scene") == "plateau":
        bg = plateau_scene(c)
    elif c.get("drawn_scene"):
        bg = Image.new("RGB", (240, 112))
        px = bg.load()
        for y in range(112):
            for x in range(240):
                if y < 58:
                    px[x, y] = _ramp(c["sky"], y / 58)
                elif y < 92:
                    px[x, y] = _ramp(c["sea"], (y - 58) / 34 + 0.15 * ((x * 7 + y * 3) % 5 == 0))
                else:
                    px[x, y] = _ramp(c["sand"], (y - 92) / 20)
    else:
        vt, vm, vpal = vanilla(folder)
        v = compose(vt, vm, vpal).crop((0, 24, 240, 136))
        bg, vp = v.copy(), v.load()
        px = bg.load()
        lums = collections.defaultdict(list)
        for y in range(112):
            for x in range(240):
                lums[_region(vp[x, y])].append(_lum(vp[x, y]))
        rng = {k: (min(l), max(l)) for k, l in lums.items()}
        xa, xb = c["clear"]
        for y in range(112):
            for x in range(240):
                p = vp[x, y]
                k = _region(p)
                if xa <= x < xb and not (k == "leaf" and _lum(p) < 150):   # vanilla's building gone: sky, ground
                    px[x, y] = _ramp(c["rock"], 0.55) if y >= c["floor"] else _ramp(c["sky"], y / 112)
                    continue
                if k == "white" and not c.get("white"):
                    k = "sky" if y < 60 else "rock"
                if k == "sky" and c.get("skygrad"):
                    px[x, y] = _ramp(c["sky"], y / 112)
                    continue
                if k == "water":
                    k = "leaf"
                lo, hi = rng.get(k, (0, 255))
                px[x, y] = _grade(c, k, p, lo, hi)
    out = bg.resize(PAINT_SIZE, Image.BICUBIC).convert("RGBA")
    if c.get("interior"):
        if not c.get("floor_tiles"):
            return out.convert("RGB").filter(ImageFilter.GaussianBlur(c.get("soften", 2.5)))
        b, q = interior_floor(folder), c["floor_tiles"]["quad"]
    else:
        b, q = landmark_drawing(c["source"]), c["quad"]
    W, H = b.size
    quad = [(x * K, y * K) for x, y in q]                            # foot-left, foot-right, crown-right, crown-left
    co = _homography([(0, H), (W, H), (W, 0), (0, 0)], quad)
    warped = b.transform(PAINT_SIZE, Image.PERSPECTIVE, co, Image.NEAREST)
    out.alpha_composite(warped)
    #  softened, so the server paints it rather than sharpening a blown-up 1x drawing (at the painting's size a 1x
    #  pixel is 4.5 wide; the caves' start images were bicubic and came back painted, the hard ones came back blocky)
    return out.convert("RGB").filter(ImageFilter.GaussianBlur(c.get("soften", 2.5)))


# ================================================================== the landmarks' name cards, re-census (2026-11-11)
#  The user (2026-11-11, "Landmark name cards"): census which landmark places have a card and what each shows, and
#  draft a replacement for any card that no longer matches its landmark as T-447 redrew it. The census (engine
#  58eaa23d8): every landmark card was ours but DOLDRUM CAVE's (built 2026-11-11 as A BECALMED, engine d4277a127); FOUNDRY CO.,
#  DAEMON TOWER and the MANSION were painted 2026-10-26 from T-447 pairs 1-2's OUTSIDES, UMBRA PLATEAU's from pair 3's
#  REVIEW BOARD. Since then pairs 4-7 redrew the INSIDES: the MANSION's rack hall and DAEMON TOWER's dot screen (pair
#  4), KEEPALIVE PLANT growing untended and TANOBY carved, not lit (pair 5), the LEAGUE's four vessels and the HALL
#  (pair 6), the S.S. ANNE's livery (pair 7). Two cards are stale: KEEPALIVE PLANT's still paints batch E's STILL
#  RUNNING plant (green status lights; the plant is overgrown now) and MONEAN CHAMBER's is batch G's gold ochre (the
#  chambers are pale sandstone with a band of pigment now). The MANSION's and the TOWER's cards are their outsides,
#  still true; vanilla's MANSION card is its hall INSIDE, so the rack hall is a real alternative, and the dot screen
#  likewise. The LEAGUE, the HALL OF FAME and the S.S. ANNE have no card of their own (the LEAGUE and the HALL are
#  UMBRA PLATEAU's mapsec, whose card is the REVIEW BOARD and T-456 suppresses it on the credits warp; the S.S. ANNE
#  has no sMapPreviewScreenData entry), so nothing is drafted for them.
#
#  CARDS holds the candidates, several to one engine card ("folder"); each keeps its card's type (CAVE fade or FOREST
#  popup), letterbox, banner and palette 14. Two ways to a start image: "graded" is the caves' paint_init (vanilla's
#  composition graded through the place's colours as built now, a motif laid in); "room" draws the room from the
#  built map (ROOM_SCENE: its back wall cut from reviewsheet's render and tiled, its floor laid in perspective, its
#  furniture stood in front), for the insides vanilla never painted. --cards --draft paints nothing new (--paint
#  does), drafts every candidate into gfx/drafts/t445_landmarks/<candidate>/ and the sheets; --cards --write
#  --approved writes only what CARDS_APPROVED names into that candidate's engine folder.
#  BUILT 2026-11-11: KEEPALIVE PLANT growing untended A and TANOBY carved, not lit A. Their engine folders (power_plant,
#  monean_chamber) are batch E's and batch G's, so the caves' own write skips a folder an approved candidate has taken
#  (CARDS_TAKEN) -- else a plain --write --approved would lay the stale cards back. The MANSION and DAEMON TOWER keep
#  their outsides (the rack hall and the dot screen stay drafts).
CARDS_DRAFT = os.path.join(ROOT, "gfx", "drafts", "t445_landmarks")
CARDS_APPROVED = {"power_plant_untended_a", "monean_chamber_carved_a", "cerulean_cave_becalmed_a"}  # the user, 2026-11-11: PLANT A, TANOBY A; DOLDRUM A BECALMED
_PLANT_UNTENDED = dict(
    folder="power_plant", banner_from="power_plant", init="graded", title="KEEPALIVE PLANT, growing untended",
    #  pair 5 B's own colours (power_plant row 7's metal, row 8's three greens and moss) -- no status lights
    rock=[(24, 30, 40), (50, 58, 76), (90, 104, 122), (122, 140, 154), (160, 178, 168), (200, 212, 200)],
    sky=[(122, 140, 154), (214, 232, 196)], leaf=[(40, 88, 44), (62, 168, 72), (150, 210, 110)],
    motif=["ivy"], denoise=0.50,
    prompt="interior of an abandoned power plant overgrown with ivy, creepers climbing every grey machine housing, "
           "moss in the seams of the steel floor plates, old drums used as planters full of leaves, the machines "
           "dark and silent, soft daylight from a high window, cool grey metal and many greens",
    neg="status lights, glowing lights, lamps, screens, people")
_TANOBY_CARVED = dict(
    folder="monean_chamber", banner_from="monean_chamber", init="graded", title="TANOBY, carved, not lit",
    #  pair 5 A: tanoby_ruins rows 7/8's pale sandstone and its dark cut; MONEAN's pigment (row 8 slot 14)
    rock=[(24, 18, 18), (70, 54, 44), (130, 102, 72), (180, 150, 104), (204, 176, 124), (236, 214, 164),
          (244, 232, 200)],
    leaf=[(70, 96, 58), (106, 140, 82), (150, 172, 120)], white="keep",
    motif=["script", "pigment"], post=["script"], pigment=(205, 139, 189), force=[(205, 139, 189)], denoise=0.45,
    prompt="an ancient shrine of pale dressed sandstone blocks on a small island, a dark square doorway into the "
           "dark with low steps, a frieze of small carved unknown glyphs cut along the stone, one band of faded "
           "rose pigment painted along the wall, unlit, sparse grass, clear sky with soft clouds",
    neg="hieroglyphs, egyptian, letters, alphabet, runes glowing, gold, torches, fire")
ROOM_SCENE = dict(
    #  the MANSION's rack hall (pair 4 A), PokemonMansion_1F as built: its back wall (the raised wall with four arched
    #  breaker bays) tiled across at 1.5x, its floor plates in perspective, the four rack fronts stood before it
    rackhall=dict(map="PokemonMansion_1F", wall=(224, 8, 592, 48), wall_scale=1.5, wall_y=14, ceiling=(30, 28, 34),
                  floor=(240, 64, 272, 96), floor_y=74,
                  props=[((304, 72, 320, 112), 10 + 40 * i, 46, 1.5) for i in range(6)],
                  soot=0.55, roof=((70, 0, 170, 12), (164, 162, 164))),
    #  DAEMON TOWER's dot screen (pair 4 A), PokemonTower_1F as built: the curved wall of arched niches, each with its
    #  warm light, at 2x; the halftone floor below
    dotscreen=dict(map="PokemonTower_1F", wall=(144, 4, 224, 32), wall_scale=2.0, wall_y=6, ceiling=(228, 222, 208),
                   floor=(160, 40, 208, 64), floor_y=70, curve=10),
)
CARDS = {
    "power_plant_untended_a": dict(_PLANT_UNTENDED, seed=4501),
    "power_plant_untended_b": dict(_PLANT_UNTENDED, seed=4502),
    "power_plant_untended_c": dict(_PLANT_UNTENDED, seed=4503, denoise=0.56),
    "monean_chamber_carved_a": dict(_TANOBY_CARVED, seed=4504),
    "monean_chamber_carved_b": dict(_TANOBY_CARVED, seed=4505),
    "pokemon_mansion_rackhall_a": dict(
        folder="pokemon_mansion", banner_from="pokemon_mansion", init="room", room="rackhall",
        title="the MANSION's rack hall", seed=4506, denoise=0.50,
        prompt="inside a burned out machine hall, tall black server racks with rows of small dead lights, raised "
               "steel floor plates, a dark cable trench, soot climbing the grey walls, a hole in the roof letting in "
               "a pale ash grey light, cold and long burnt out",
        neg="fire, flames, glow, embers, orange light, people, windows with curtains, bright colours"),
    "pokemon_mansion_rackhall_b": None,
    "pokemon_tower_dotscreen_a": dict(
        folder="pokemon_tower", banner_from="pokemon_tower", init="room", room="dotscreen",
        title="DAEMON TOWER's dot screen", seed=4508, denoise=0.48,
        prompt="inside a pale round stone tower, the curved wall made of halftone dots with rows of small arched "
               "niches each holding a tiny warm candle flame, a pale floor of fine halftone dots, quiet, soft grey "
               "light, monochrome grey with only the small warm flames",
        neg="colour, green, blue, fire on the floor, people, windows, stairs"),
    "pokemon_tower_dotscreen_b": None,
}
CARDS["pokemon_mansion_rackhall_b"] = dict(CARDS["pokemon_mansion_rackhall_a"], seed=4507)
CARDS["pokemon_tower_dotscreen_b"] = dict(CARDS["pokemon_tower_dotscreen_a"], seed=4509)
#  the rooms came back at 0.48-0.50 still reading as the map's tiles, so a third of each painted harder
CARDS["pokemon_mansion_rackhall_c"] = dict(CARDS["pokemon_mansion_rackhall_a"], seed=4510, denoise=0.62)
CARDS["pokemon_tower_dotscreen_c"] = dict(CARDS["pokemon_tower_dotscreen_a"], seed=4511, denoise=0.62)

#  DOLDRUM CAVE (cerulean_cave), DRAFT 2026-11-11 (the user picked the job): the last landmark card still Nintendo's
#  but USER TOWER's. Two things fix what it may be. (1) The cave's own tiles wait on the user (gbacaves.py; T-251:
#  "its grey and its 'itself' are a decided pair"), so no candidate paints a tile look -- vanilla's composition (a
#  dark mouth in the rocks, mist among trunks behind) graded, and the stillness taken from the NAME (a doldrum is the
#  windless calm), not from gbacaves' BECALMED proposal. (2) The card is ALREADY two-state with no engine work:
#  DaemonsGreyHalftoneFrame tones every palette entry while DaemonsCaveUnperceived() (fieldmap.c, T-255), and the
#  preview's palettes 13-14 reach the screen through that buffer, so a colour card is shown to the unread player as
#  four flat tones of ink on warm paper (DRAWING_TONES below; read from the code, not yet seen on a screen). The
#  sheet shows each candidate both ways. S.T.A.R.R. is never drawn or named: the read card holds one point of light
#  on the still pool and no star above it to make it.
_DOLDRUM = dict(
    folder="cerulean_cave", banner_from="cerulean_cave", init="graded", tex=0.08,
    rock=[(18, 22, 30), (36, 44, 56), (62, 74, 88), (96, 110, 120), (140, 152, 158), (186, 194, 196)],
    water=[(4, 10, 16), (14, 32, 42), (34, 64, 76), (70, 104, 112)],
    white=[(150, 166, 170), (206, 216, 214)],
    pool=(115, 76, 56, 18), denoise=0.50,
    prompt="the mouth of a quiet cave in still slate grey rock, a perfectly still black pool filling the mouth like "
           "a mirror, windless, mist hanging motionless among pale bare trunks behind, calm cold dusk, a single tiny "
           "point of white light reflected on the still water",
    neg="stars in the sky, moon, sun, waves, ripples, wind, fire, glow, torches, crystals, green grass, purple")
CARDS.update({
    #  A: the cave as the understood see it, in colour -- still air, still water, one reflected light with no source
    "cerulean_cave_becalmed_a": dict(_DOLDRUM, seed=4521, title="DOLDRUM CAVE, becalmed", post=["starpoint"],
                                     force=[(232, 236, 224)]),
    "cerulean_cave_becalmed_b": dict(_DOLDRUM, seed=4522, title="DOLDRUM CAVE, becalmed", post=["starpoint"],
                                     force=[(232, 236, 224)], denoise=0.56),
    #  B: the unread cave as a card of its own, painted as ink and laid in the engine's four tones exactly, so the
    #  filter leaves it as it is -- one state: the read player would see the drawing too
    "cerulean_cave_drawing_a": dict(_DOLDRUM, seed=4523, title="DOLDRUM CAVE, a simple drawing", post=["drawing"],
                                    denoise=0.60,
                                    rock=[(40, 40, 44), (90, 86, 88), (176, 168, 150), (240, 232, 204)],
                                    water=[(24, 24, 40), (60, 58, 66)], white=[(232, 226, 200), (246, 240, 214)],
                                    prompt="a pen and ink drawing on warm paper of the mouth of a quiet cave, simple "
                                           "dots and lines, sparse hatching, a still dark pool in the mouth, bare "
                                           "trunks behind, unfinished sketch, flat, no colour",
                                    neg="colour, painting, shading gradient, photo, stars, moon, people, text"),
    #  C: A's own tiles, every 16px block present and the arrangement wrong (content with no context) -- what the
    #  map does on each entry (T-251 step 3), done to the card; shown here once, as one seed would lay it
    "cerulean_cave_recomposed": dict(_DOLDRUM, title="DOLDRUM CAVE, wrongly arranged", painting_of=
                                     "cerulean_cave_becalmed_a", post=["starpoint", "recompose"],
                                     force=[(232, 236, 224)]),
    #  D: the drawing with one thing in colour -- the pool already shows the cave as it is (lineage 3b's painted
    #  mirror); needs engine work to survive the filter (see the report)
    "cerulean_cave_mirror": dict(_DOLDRUM, title="DOLDRUM CAVE, the painted mirror", painting_of=
                                 "cerulean_cave_becalmed_a", post=["starpoint", "mirror"], force=[(232, 236, 224)]),
})
#  fieldmap.c's sDrawingTones (T-255), at 8 bits, and DaemonsDrawingTone's thresholds on the 5-bit luminance
DRAWING_TONES = [(3 << 3, 3 << 3, 5 << 3), (11 << 3, 10 << 3, 11 << 3), (22 << 3, 21 << 3, 18 << 3),
                 (30 << 3, 29 << 3, 25 << 3)]
#  B is laid in the four tones exactly; D's ink is the four tones and its pool the rest
CARDS["cerulean_cave_drawing_a"]["force"] = list(DRAWING_TONES)
CARDS["cerulean_cave_drawing_a"]["accents"] = False
CARDS["cerulean_cave_mirror"]["force"] = [(232, 236, 224)] + DRAWING_TONES


def drawing_tone(c):
    """DaemonsDrawingTone: a colour as the unread DOLDRUM CAVE shows it"""
    if c in DRAWING_TONES:
        return c
    r, g, b = c[0] >> 3, c[1] >> 3, c[2] >> 3
    lum = (r * 77 + g * 150 + b * 29) >> 8
    return DRAWING_TONES[0 if lum < 7 else 1 if lum < 14 else 2 if lum < 23 else 3]


def unread(im):
    """(RGB) a whole card as the unread player sees it: every colour through drawing_tone"""
    out = im.copy()
    cache = {}
    out.putdata([cache.setdefault(p, drawing_tone(p)) for p in im.getdata()])
    return out


#  the engine folders an approved candidate writes, and which candidate: at most one per folder
CARDS_TAKEN = {CARDS[c]["folder"]: c for c in sorted(CARDS_APPROVED)}
assert len(CARDS_TAKEN) == len(CARDS_APPROVED), "two approved CARDS candidates for one engine card"


def motif_ivy(out, v, c):
    """GROWING UNTENDED (pair 5 B): creepers up the dark housings -- a stem that climbs from a lit floor edge with
    leaves either side -- and moss along the floor's seams, in the plant's own three greens"""
    import random
    rnd, op = random.Random(4501), out.load()
    G = c["leaf"]
    for _ in range(46):
        x, y = rnd.randrange(4, 236), rnd.randrange(40, 108)
        if not 30 < _lum(op[x, y]) < 150:
            continue
        for k in range(rnd.randrange(14, 44)):
            yy = y - k
            if yy < 2:
                break
            x = min(237, max(2, x + rnd.choice((-1, 0, 0, 1))))
            op[x, yy] = G[0]
            if k % 3 == 0:
                s = rnd.choice((-1, 1))
                op[x + s, yy] = G[1]
                op[x + 2 * s, yy] = G[2] if rnd.random() < 0.5 else G[1]
                op[x + s, yy - 1] = G[1]
    for _ in range(60):                                     # moss: low clumps on the lit floor, never a line
        x, y = rnd.randrange(2, 232), rnd.randrange(84, 108)
        if _lum(op[x, y]) < 90:
            continue
        for a in range(rnd.randrange(3, 8)):
            for b in range(rnd.randrange(1, 3)):
                if rnd.random() < 0.7:
                    op[x + a, y + b] = G[1] if rnd.random() < 0.6 else G[2]


def motif_pigment(out, v, c):
    """TANOBY carved, not lit (pair 5 A): one band of the chamber's pigment along the dressed stone, 3px, under the
    frieze's first line -- only where the whole band is stone"""
    op, rock = out.load(), _rockmask(v)
    for x in range(240):
        if all(rock(x, y) for y in range(31, 35)):
            for y in range(31, 34):
                op[x, y] = _shade(c["pigment"], 0.85 + 0.15 * ((x // 3) % 2))


MOTIFS.update(ivy=motif_ivy, pigment=motif_pigment)


def room_scene(c):
    """(RGB 240x112) an inside vanilla never painted, drawn from the built map: the ceiling, the back wall cut from
    reviewsheet's render and tiled across, the floor laid in perspective below it, the furniture stood in front"""
    r = ROOM_SCENE[c["room"]]
    img = RS.render(RS.layout_of(r["map"])).convert("RGB")
    bg = Image.new("RGB", (240, 112), r["ceiling"])
    s = r["wall_scale"]
    wall = img.crop(r["wall"])
    wall = wall.resize((int(wall.size[0] * s), int(wall.size[1] * s)), Image.NEAREST)
    fy = r["floor_y"]
    #  the floor: its patch tiled into a wide plane, taken by a homography to a trapezoid whose far edge meets the
    #  wall's foot and whose near edge runs off both sides of the picture
    patch = img.crop(r["floor"])
    plane = Image.new("RGB", (patch.size[0] * 8, patch.size[1] * 3))
    for i in range(8):
        for j in range(3):
            plane.paste(patch, (i * patch.size[0], j * patch.size[1]))
    W, H = plane.size
    co = _homography([(0, H), (W, H), (W, 0), (0, 0)], [(-260, 112), (500, 112), (300, fy), (-60, fy)])
    bg.paste(plane.transform((240, 112), Image.PERSPECTIVE, co, Image.BICUBIC).crop((0, fy, 240, 112)), (0, fy))
    x = 0
    while x < 240:
        bg.paste(wall, (x, r["wall_y"]))
        x += wall.size[0]
    wall_foot = r["wall_y"] + wall.size[1]
    if wall_foot < fy:                                       # the wall carried down to the floor in its own base
        base = wall.crop((0, wall.size[1] - 4, wall.size[0], wall.size[1]))
        for yy in range(wall_foot, fy, 4):
            for xx in range(0, 240, wall.size[0]):
                bg.paste(base, (xx, yy))
    if r.get("curve"):                                       # the round tower: the wall bows toward the middle
        src = bg.copy()
        sp, dp = src.load(), bg.load()
        for xx in range(240):
            off = int(r["curve"] * (1 - ((xx - 120) / 120) ** 2))
            for yy in range(fy - 1, -1, -1):
                dp[xx, yy] = sp[xx, max(0, yy - off)] if yy - off >= 0 else r["ceiling"]
    for rect, px_, py_, sc in r.get("props", []):
        p = img.crop(rect)
        p = p.resize((int(p.size[0] * sc), int(p.size[1] * sc)), Image.NEAREST)
        bg.paste(p, (px_, py_))
    if r.get("roof"):                                        # the MANSION: the roof broken through, ash light
        (x0, y0, x1, y1), col = r["roof"]
        ImageDraw.Draw(bg).ellipse((x0, y0 - 14, x1, y1 + 6), fill=col)
    if r.get("soot"):                                        # soot climbing from the floor
        px = bg.load()
        for yy in range(112):
            k = r["soot"] * max(0.0, (yy - 20) / 92) * 0.6
            for xx in range(240):
                p = px[xx, yy]
                px[xx, yy] = tuple(int(q * (1 - k)) for q in p)
    return bg


def card_init(folder, sec):
    """a CARDS candidate's start image, at the painting's size"""
    from PIL import ImageFilter
    c = CARDS[folder]
    if c["init"] == "graded":
        return paint_init(folder, sec)
    return room_scene(c).resize(PAINT_SIZE, Image.BICUBIC).filter(ImageFilter.GaussianBlur(c.get("soften", 2.5)))


def paint(folder, sec, out_dir):
    """--paint: the start image, then the sprite server's painting of it, with its record"""
    import spriteforge
    if cfg(folder).get("painting_of"):                  # drawn from another candidate's painting, never painted itself
        print("  %-27s no painting of its own: drawn from %s's" % (folder, cfg(folder)["painting_of"]))
        return None
    d = os.path.join(out_dir, folder)
    os.makedirs(d, exist_ok=True)
    init = os.path.join(d, "painted_init.png")
    (card_init(folder, sec) if folder in CARDS else landmark_init(folder) if folder in LANDMARK
     else paint_init(folder, sec)).save(init)
    c = cfg(folder)
    p = dict(mode="i2i", out=os.path.join(d, "painted"), prompt=PAINT_STYLE % c["prompt"],
             negative=PAINT_NEG + (", " + c["neg"] if c.get("neg") else ""),
             seed=A.seed or c["seed"], steps=28, cfg=5.5, sampler="dpmpp_2m", scheduler="karras", denoise=c["denoise"],
             stop_at=None, image=os.path.relpath(init, ROOT), size=list(PAINT_SIZE))
    return spriteforge.run(p)


def painted_path(folder):
    folder = CARDS.get(folder, {}).get("painting_of", folder)    # DOLDRUM's C and D are drawn from A's painting
    return os.path.join(A.draft or (CARDS_DRAFT if A.cards else DRAFT_DEFAULT), folder, "painted.png")


def painted_picture(folder):
    """the painting fitted to 240x112 (cropped to the picture's shape about its middle, then filtered down)"""
    im = Image.open(painted_path(folder)).convert("RGB")
    W, H = im.size
    want = 240 / 112
    if W / H > want:
        w = int(H * want)
        im = im.crop(((W - w) // 2, 0, (W - w) // 2 + w, H))
    else:
        h = int(W / want)
        im = im.crop((0, (H - h) // 2, W, (H - h) // 2 + h))
    im = im.resize((240, 112), Image.LANCZOS)
    for m in cfg(folder).get("post", []):
        POSTS[m](im)
    return im


def post_braille(im):
    """THE DOTS, after the painting (the server smooths a dot this small away, or swells it into a stud): lines of
    six-dot braille cells pressed into the painted stone at the picture's own size -- a 2px dot lit at its top-left
    with a 1px shadow below-right, two columns of three at a 4px pitch, cells 9px apart and lines 14px apart, so each
    cell reads as a cell; at least two dots in a cell and never all six. Only where the stone is (warm, lit, and the
    cell's whole footprint stone), so the sky, the leaves and the dark mouth stay as painted"""
    import colorsys, random
    rnd, px = random.Random(4451), im.load()

    def stone(x, y):
        if not (0 <= x < 240 and 0 <= y < 112):
            return False
        r, g, b = px[x, y]
        h, sat, val = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return 15 <= h * 360 <= 50 and sat > 0.12 and 0.45 < val

    for cy in range(3, 104, 14):
        for cx in range(2 + (cy // 14) % 2 * 4, 234, 9):
            if cx > 160 and cy < 40:                                  # the pale clouds, sandstone-coloured
                continue
            if not all(stone(cx + a, cy + b) for a in range(-1, 8) for b in range(-1, 12)):
                continue
            cell = []
            while not 2 <= len(cell) <= 5:
                cell = [(q, r) for r in range(3) for q in range(2) if rnd.random() < 0.5]
            for q, r in cell:
                x, y = cx + q * 4, cy + r * 4
                base = px[x, y]
                px[x, y] = _shade(base, 1.22)
                px[x + 1, y] = px[x, y + 1] = _shade(base, 1.06)
                px[x + 1, y + 1] = _shade(base, 0.86)
                px[x + 2, y + 1] = px[x + 1, y + 2] = px[x + 2, y + 2] = _shade(base, 0.6)


def post_redband(im, folder="silph_co"):
    """CORPUS's tower, after the painting: the crown's one thin red band (the server paints it out at any denoise
    that leaves the brass painted) laid back from the building's own drawing, warped to the card at 1x"""
    c = LANDMARK[folder]
    b = landmark_drawing(c["source"])
    W, H = b.size
    co = _homography([(0, H), (W, H), (W, 0), (0, 0)], c["quad"])
    #  the band is two pixels of the drawing; near the crown the keystone squeezes rows to a third, so NEAREST would
    #  drop it -- the band is warped as a mask, bilinear, and kept wherever it covers a third of a pixel
    red = (198, 34, 44)
    mask = Image.new("L", b.size)
    mask.putdata([255 if p[:3] == red and p[3] == 255 else 0 for p in b.getdata()])
    w = mask.transform((240, 112), Image.PERSPECTIVE, co, Image.BILINEAR).load()
    px = im.load()
    for y in range(112):
        for x in range(240):
            if w[x, y] > 80:
                px[x, y] = red


def post_spinfloor(im, folder="rocket_warehouse"):
    """CORPUS WAREHOUSE, after the painting: the spin tiles laid back on the floor from the built map, warped to the
    card at 1x (the server washes a green chevron this small into the olive at any denoise that paints the room)"""
    c = LANDMARK[folder]
    b, q = interior_floor(folder), c["floor_tiles"]["quad"]
    W, H = b.size
    co = _homography([(0, H), (W, H), (W, 0), (0, 0)], q)
    w = b.transform((240, 112), Image.PERSPECTIVE, co, Image.NEAREST)
    im.paste(w.convert("RGB"), (0, 0), w)


#  the REVIEW BOARD's four fluids (gbalandmarks' RB_VESSEL_COLOURS: each body and its light) and the kept door's blues
RB_CRISP = {(192, 28, 36), (238, 96, 84), (222, 178, 30), (252, 230, 112), (6, 4, 8), (66, 46, 78), (218, 220, 206),
            (250, 250, 242), (98, 164, 222), (74, 131, 197), (156, 213, 255)}


def post_vessels(im, folder="review_board"):
    """the REVIEW BOARD, after the painting: the four fluids (the only colour on UMBRA) and the kept blue door laid
    back crisp from the built map, warped to the card at 1x -- the server greys a 3px column of red at any denoise
    that leaves the stone painted, and paints the door out"""
    c = LANDMARK[folder]
    b = landmark_drawing(c["source"])
    W, H = b.size
    co = _homography([(0, H), (W, H), (W, 0), (0, 0)], c["quad"])
    keep = Image.new("RGBA", b.size)
    keep.putdata([p if p[3] == 255 and p[:3] in RB_CRISP else (0, 0, 0, 0) for p in b.getdata()])
    w = keep.transform((240, 112), Image.PERSPECTIVE, co, Image.NEAREST)
    im.paste(w.convert("RGB"), (0, 0), w)


def post_script(im):
    """THE TANOBY CHAMBERS, after the painting (the server smooths the start image's glyphs away, as it did THE DOTS'):
    two lines of the invented script cut into the ochre stone at 1x -- each glyph two or three strokes in a 3x5 cell,
    a dark cut with a lit lip below, a glyph only where its whole cell is lit dressed stone"""
    import random
    rnd, px = random.Random(4451), im.load()
    def stone(x, y):
        if not (0 <= x < 240 and 0 <= y < 112):
            return False
        r, g, b = px[x, y]
        return 100 <= _lum((r, g, b)) <= 235 and r >= g * 0.8 and b <= g * 0.85
    STROKES = [[(0, y) for y in range(5)], [(2, y) for y in range(5)], [(x, 0) for x in range(3)],
               [(x, 2) for x in range(3)], [(x, 4) for x in range(3)], [(0, 0), (1, 1), (2, 2)],
               [(1, y) for y in range(2, 5)], [(2, 0), (1, 1), (0, 2)]]
    for cy in (24, 44, 64):
        for cx in range(100, 236, 5):
            if sum(stone(cx + a, cy + b) for a in range(3) for b in range(6)) < 16:
                continue
            pts = set()
            for st in rnd.sample(STROKES, rnd.choice((2, 3))):
                pts.update(st)
            for a, b in pts:
                px[cx + a, cy + b] = _shade(px[cx + a, cy + b], 0.5)
            for a, b in pts:
                if (a, b + 1) not in pts:
                    px[cx + a, cy + b + 1] = _shade(px[cx + a, cy + b + 1], 1.15)


POSTS = dict(script=post_script, braille=post_braille, redband=post_redband, spinfloor=post_spinfloor, vessels=post_vessels)


def _in_pool(x, y):
    """DOLDRUM CAVE: inside the dark mouth vanilla's composition holds (an ellipse, picture coordinates)"""
    cx, cy, rx, ry = _DOLDRUM["pool"]
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def post_starpoint(im):
    """DOLDRUM CAVE, after the painting: one point of light on the still pool and nothing above it to make it --
    three pixels and a fainter one either side, laid on the darkest stretch of the pool's middle"""
    px = im.load()
    cx, cy, rx, ry = _DOLDRUM["pool"]
    best = min(((sum(_lum(px[x + a, y]) for a in range(-3, 4)), x, y)
                for y in range(cy - ry // 3, cy + ry // 2) for x in range(cx - rx // 2, cx + rx // 2)
                if _in_pool(x - 3, y) and _in_pool(x + 3, y)))
    _, x, y = best
    for a in (-1, 0, 1):
        px[x + a, y] = (232, 236, 224)
    for a in (-2, 2):
        px[x + a, y] = _shade((232, 236, 224), 0.62)


def post_drawing(im):
    """DOLDRUM CAVE B, after the painting: every pixel to the engine's four tones of ink (DaemonsDrawingTone), so the
    filter, which leaves a tone alone, shows it exactly as written"""
    px = im.load()
    for y in range(112):
        for x in range(240):
            px[x, y] = drawing_tone(px[x, y])


def post_recompose(im):
    """DOLDRUM CAVE C: the picture cut into twelve blocks of 5x7 tiles (40x56, so every tile is A's) and laid back
    with none where it was -- one seed's arrangement; the map's own recomposition differs each entry. 16px blocks
    (tried first) read as noise, not as a place put together wrong"""
    import random
    src = im.copy()
    cells = [(x, y) for y in range(0, 112, 56) for x in range(0, 240, 40)]
    order, rnd = cells[:], random.Random(4524)
    while any(a == b for a, b in zip(cells, order)):
        rnd.shuffle(order)
    for (dx, dy), (sx, sy) in zip(cells, order):
        im.paste(src.crop((sx, sy, sx + 40, sy + 56)), (dx, dy))


def post_mirror(im):
    """DOLDRUM CAVE D: A in the engine's ink everywhere but the pool, which keeps its colour -- the pool decided by
    TILE (an 8x8 tile is in it when its middle is), since a palette slot is a tile's, never a pixel's"""
    px = im.load()
    for ty in range(14):
        for tx in range(30):
            if _in_pool(tx * 8 + 4, ty * 8 + 4):
                continue
            for y in range(ty * 8, ty * 8 + 8):
                for x in range(tx * 8, tx * 8 + 8):
                    px[x, y] = drawing_tone(px[x, y])


POSTS.update(starpoint=post_starpoint, drawing=post_drawing, recompose=post_recompose, mirror=post_mirror)


# ================================================================== OTHER CAVE's four lights
def light_ramps():
    """[(rock ramp, crystal ramp)] for lights 0..3: row 8 of palettes_other (teal) and palettes_other_1..3, the rock
    its indices 1..5 and the crystal 9..15, each sorted dark to light"""
    out = []
    base = os.path.join(GBA, "data/tilesets/secondary/rock_tunnel")
    for d in ("palettes_other", "palettes_other_1", "palettes_other_2", "palettes_other_3"):
        lines = open(os.path.join(base, d, "08.pal")).read().split("\n")[3:19]
        cols = [tuple(int(v) for v in l.split()) for l in lines]
        out.append((sorted(cols[1:6], key=_lum), sorted(cols[9:16], key=_lum)))
    return out


def light_of(c):
    """what a colour of the teal painting is: 'crystal' (teal), 'rock' (mauve) or None (sky, sea, foam: kept)"""
    import colorsys
    h, sat, v = colorsys.rgb_to_hsv(*[x / 255 for x in c])
    h *= 360
    if 150 <= h < 195 and sat > 0.12:
        return "crystal"
    if (h >= 280 or h < 40) and sat < 0.45:
        return "rock"
    if sat < 0.08 and v < 0.75:                                     # a near-grey shadow in the rock
        return "rock"
    return None


def light_palettes(pal13, draft=None, van=None):
    """palette 13 (index 0 then 15 colours) in each of the four lights; light 0 is the painting's own. A colour that
    lies mostly where vanilla's picture has its sky and sea (draft and van: the two screens) is the open air and
    keeps its colour in every light -- the cave's light is inside it, not over the sea"""
    ramps = light_ramps()
    out = [list(pal13)]
    air = set()
    if draft is not None:
        dp, vp = draft.load(), van.load()
        n, a = collections.Counter(), collections.Counter()
        for y in range(24, 136):
            for x in range(240):
                c = dp[x, y]
                n[c] += 1
                if _region(vp[x, y]) in ("sky", "water"):
                    a[c] += 1
        air = {c for c in n if a[c] > 0.6 * n[c]}
    #  where each teal colour sits on its own light-0 ramp, by luminance, so it lands at the same place on light k's
    for k in (1, 2, 3):
        pal = [pal13[0]]
        for c in pal13[1:]:
            role = None if c in air else light_of(c)
            if role is None:
                pal.append(c)
                continue
            r0, rk = ramps[0][0 if role == "rock" else 1], ramps[k][0 if role == "rock" else 1]
            lo, hi = _lum(r0[0]), _lum(r0[-1])
            t = (_lum(c) - lo) / max(1, hi - lo)
            pal.append(tuple((v >> 3) << 3 for v in _ramp(rk, t)))
        out.append(pal)
    return out


def write_pal(cols, path):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(cols))
        for c in cols:
            f.write("%d %d %d\n" % c)


# ================================================================== drafting
def layouts_for(folder, sec):
    out = []
    for m in maps_of(sec):
        try:
            out.append((m, RS.layout_of(m)))
        except StopIteration:
            pass
    return out


_RENDER = {}


def render(m, l):
    if m not in _RENDER:
        _RENDER[m] = RS.render(l)
    return _RENDER[m]


def best_window(cands, ww=WIN_W, wh=WIN_H):
    """the ww x wh window, over every map of the cave, scored for what a player would know the cave by: the most
    different blocks, the least of its commonest block (a bare floor), and the least black (void)"""
    best = None
    for m, l in cands:
        W, H = l["width"], l["height"]
        if W < ww or H < wh:
            continue
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        ids = [[struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF for x in range(W)] for y in range(H)]
        img = render(m, l)
        lum = img.convert("L").resize((W, H), Image.BOX).load()
        n = ww * wh
        for y0 in range(0, H - wh + 1):
            for x0 in range(0, W - ww + 1):
                cells = [ids[y][x] for y in range(y0, y0 + wh) for x in range(x0, x0 + ww)]
                dark = sum(1 for y in range(y0, y0 + wh) for x in range(x0, x0 + ww) if lum[x, y] < 18)
                common = collections.Counter(cells).most_common(1)[0][1] / n
                score = len(set(cells)) + 0.25 * n * (1 - common) - 1.5 * dark
                if best is None or score > best[0]:
                    best = (score, m, x0, y0)
    return best


def picture(folder, sec, painted=None):
    """the 240x112 RGB picture for this cave, and where it was taken: the painting where there is one (unless
    --top-down), else the top-down window"""
    if painted is None:
        painted = not A.top_down and os.path.exists(painted_path(folder))
    if painted:
        rec = json.load(open(painted_path(folder)[:-4] + ".json"))
        return painted_picture(folder), "painted, seed %d, denoise %.2f" % (rec["seed"], rec["denoise"])
    cands = layouts_for(folder, sec)
    if folder in VIEW:
        v = VIEW[folder]
        m, x0, y0 = v[:3]
        l = dict(cands)[m]
        img = render(m, l)
        if len(v) > 3:                                      # a doubled 8x4 window
            crop = img.crop((x0 * 16, y0 * 16, x0 * 16 + 120, y0 * 16 + 56)).resize((240, 112), Image.NEAREST)
            return crop, "%s (%d,%d) 2x, chosen" % (m, x0, y0)
        return img.crop((x0 * 16, y0 * 16, x0 * 16 + 240, y0 * 16 + 112)), "%s (%d,%d), chosen" % (m, x0, y0)
    b = best_window(cands)
    if b:
        _, m, x0, y0 = b
        img = render(m, dict(cands)[m])
        return img.crop((x0 * 16, y0 * 16, x0 * 16 + 240, y0 * 16 + 112)), "%s (%d,%d)" % (m, x0, y0)
    b = best_window(cands, 8, 4)                            # rooms too small for 15x7 (THE WRONG WAY's are 11x11)
    if not b:
        return None, "no map of %s is 8x4 blocks" % sec
    _, m, x0, y0 = b
    img = render(m, dict(cands)[m])
    crop = img.crop((x0 * 16, y0 * 16, x0 * 16 + 120, y0 * 16 + 56)).resize((240, 112), Image.NEAREST)
    return crop, "%s (%d,%d) 2x" % (m, x0, y0)


def _fixed(pic, cols):
    """pic mapped onto exactly these colours, undithered"""
    pi = Image.new("P", (1, 1))
    flat = [v for c in cols for v in c]
    pi.putpalette(flat + flat[:3] * (256 - len(cols)))
    return pic.quantize(palette=pi, dither=Image.Dither.NONE)


def keep_accents(pic, q, n=15, rounds=3):
    """a painting's small bright accent (SMOULDER's glowing cracks, a status light, the cable) is a few hundred pixels
    and median cut spends no colour on it; where pixels sit far from every colour chosen, the two closest colours are
    merged and the accent takes the freed index"""
    cols = [tuple(q.getpalette()[i * 3:i * 3 + 3]) for i in range(n)]
    src = list(pic.getdata())
    for _ in range(rounds):
        d2 = lambda a, b: sum((a[k] - b[k]) ** 2 for k in range(3))
        far = [c for c in src if min(d2(c, k) for k in cols) > 56 ** 2]
        if len(far) < 0.002 * len(src):
            break
        acc = tuple(sorted(c[k] for c in far)[len(far) // 2] for k in range(3))
        i, j = min(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda ij: d2(cols[ij[0]], cols[ij[1]]))
        cols[i] = tuple((cols[i][k] + cols[j][k]) // 2 for k in range(3))
        cols[j] = acc
        q = _fixed(pic, cols)
    return q


def reduce(pic, vpal, accents=False, force=(), neutral=None):
    """15 colours into palette 13's indices 1..15 (index 0 vanilla's: BG0 colour 0 is transparent); a painting keeps
    its accents (keep_accents); a colour in force (a landmark's, too few pixels for keep_accents to see: CORPUS's red
    band) takes an index of its own; neutral (T-456) gives up the darkest green-cast colour median cut chose for this
    grey, so a dark front that shared the trees' deepest shade is neutral and the trees lose that shade"""
    q = pic.quantize(colors=15 - len(force), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    if accents:
        q = keep_accents(pic, q, n=15 - len(force))
    if force or neutral:
        cols = [tuple(q.getpalette()[i * 3:i * 3 + 3]) for i in range(15 - len(force))]
        if neutral:
            green = [c for c in cols if c[1] > c[0] + 8]
            if green:
                cols[cols.index(min(green, key=sum))] = tuple(neutral)
        q = _fixed(pic, cols + list(force))
    qp = (q.getpalette()[:45] + [0] * 45)[:45]                      # a cave of fewer colours leaves the rest unused
    cols = [tuple(qp[i * 3:i * 3 + 3]) for i in range(15)]
    #  to the GBA's 5 bits, as the palette will hold them
    cols = [tuple((v >> 3) << 3 for v in c) for c in cols]
    order = sorted(range(15), key=lambda i: sum(cols[i]))           # dark to light, for a readable palette
    remap = {old: new + 1 for new, old in enumerate(order)}
    pal13 = [vpal[0]] + [cols[i] for i in order]
    idx = [remap[v] for v in q.getdata()]
    return idx, pal13


def build(folder, sec):
    """(tiles, tilemap, palette32, note): vanilla's letterbox and banner kept, the picture rows redrawn"""
    vt, vm, vpal = van(folder)
    pic, where = picture(folder, sec)
    if pic is None:
        return None
    c = cfg(folder)
    #  a card laid in a few flat tones (DOLDRUM's drawing) has no accents to keep
    idx, pal13 = reduce(pic, vpal, accents=where.startswith("painted") and c.get("accents", True),
                        force=c.get("force", ()), neutral=c.get("neutral"))
    tiles, seen, m, tpal = [], {}, [0] * 640, []

    def add(t, p=14):
        k = tuple(t)
        if k not in seen:
            seen[k] = len(tiles)
            tiles.append(list(t))
            tpal.append(p)
        return seen[k]

    add(vt[0])                                                       # tile 0 stays tile 0 (columns 30, 31)
    for ty in range(20):
        for tx in range(32):
            e = vm[ty * 32 + tx]
            if tx >= 30 or not (3 <= ty <= 16):
                m[ty * 32 + tx] = (e & 0xFC00) | add(vt[e & 0x3FF], e >> 12)  # vanilla's own tile, flips and palette
    for ty in range(14):
        for tx in range(30):
            t = [idx[(ty * 8 + y) * 240 + tx * 8 + x] for y in range(8) for x in range(8)]
            m[(ty + 3) * 32 + tx] = (13 << 12) | add(t, 13)
    pal = pal13 + vpal[16:32]
    #  tiles.png's pixels: a palette-14 tile's written 16..31, as vanilla's are (gbagfx keeps the low nibble)
    png = [[v + 16 if tp == 14 else v for v in t] for t, tp in zip(tiles, tpal)]
    return tiles, m, pal, where, png


def tiles_png(tiles, pal, path):
    """tiles.png as vanilla keeps it: 8-bit indexed, 32 colours (palette 13 then 14), 15 tiles a row -- gbagfx keeps
    each index's low nibble, so a palette-14 tile's pixels are written 16..31"""
    per = 15
    rows = (len(tiles) + per - 1) // per
    im = Image.new("P", (per * 8, rows * 8))
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat)              # exactly palette 13 and 14, as vanilla's: never a 256-entry PLTE (T-442, T-444)
    px = im.load()
    for i, t in enumerate(tiles):
        for y in range(8):
            for x in range(8):
                px[(i % per) * 8 + x, (i // per) * 8 + y] = t[y * 8 + x]
    im.save(path)


def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


def sheet(rows, path, title):
    Z = 2
    cw, ch = 240 * Z, 160 * Z
    W = 2 * cw + 3 * 16 + 300
    H = 40 + len(rows) * (ch + 34)
    out = Image.new("RGB", (W, H), (34, 34, 40))
    d = ImageDraw.Draw(out)
    d.text((12, 10), title, fill=(235, 235, 235), font=font(14))
    y = 40
    for r in rows:
        d.text((16, y), "VANILLA  %s" % r["folder"], fill=(170, 170, 170), font=font(12))
        d.text((32 + cw, y), "DRAFT  %s -- %s" % (r["name"], r["where"]), fill=(240, 220, 120), font=font(12))
        out.paste(r["vanilla"].resize((cw, ch), Image.NEAREST), (16, y + 16))
        out.paste(r["draft"].resize((cw, ch), Image.NEAREST), (32 + cw, y + 16))
        tx = 48 + 2 * cw
        for k, line in enumerate(r["notes"]):
            d.text((tx, y + 18 + k * 15), line, fill=(210, 210, 210), font=font(11))
        y += ch + 34
    out.save(path)
    return path


def engine_card(folder):
    """(RGB 240x160) the card the engine has now, decoded from graphics/map_preview/<folder>/ (tiles.png keeps each
    index's low nibble; tilemap.bin's palette bits pick 13 or 14)"""
    d = os.path.join(MPS, folder)
    im = Image.open(os.path.join(d, "tiles.png"))
    pal = im.getpalette()[:96]
    pal = [tuple(pal[i:i + 3]) for i in range(0, 96, 3)]
    px, (W, H) = im.load(), im.size
    tiles = [[px[tx * 8 + x, ty * 8 + y] & 15 for y in range(8) for x in range(8)]
             for ty in range(H // 8) for tx in range(W // 8)]
    m = list(struct.unpack("<640H", open(os.path.join(d, "tilemap.bin"), "rb").read()[:1280]))
    return compose(tiles, m, pal), pal


#  the census (2026-11-11): every landmark T-447 redrew, the card it shows on entering, and what that card is
CARD_CENSUS = [
    ("silph_co", "CORPUS's tower", "ours (2026-10-26) from pair 2's outside -- current"),
    ("pokemon_tower", "DAEMON TOWER", "ours (2026-10-26) from pair 2's outside -- current; the dot screen is inside"),
    ("pokemon_mansion", "the MANSION", "ours (2026-10-26) the burned outside -- current; vanilla's was its hall"),
    ("power_plant", "KEEPALIVE PLANT", "ours (2026-10-23) batch E's STILL RUNNING -- STALE: pair 5 overgrew it"),
    ("monean_chamber", "TANOBY (7 chambers)", "ours (2026-11-06) batch G's gold ochre -- STALE: pair 5 sandstone"),
    ("review_board", "the REVIEW BOARD", "ours (2026-10-26, T-456) -- current; the LEAGUE shares its mapsec"),
    ("rocket_hideout", "CORPUS HIDEOUT", "ours (2026-10-26) -- current (no T-447 art)"),
    ("rocket_warehouse", "CORPUS WAREHOUSE", "ours (2026-10-26) -- current (no T-447 art)"),
    ("cerulean_cave", "DOLDRUM CAVE", "ours (2026-11-11, --cards A BECALMED, engine d4277a127) -- the grey filter inks it unread"),
]
NO_CARD = ["SCORN SOLUTIONS, ERRATA, CRYSTAL's lab, the GAME CORNER, the BENCHMARKs, USER TOWER: a town's building,",
           "  the name popup only (no sMapPreviewScreenData entry).",
           "the LEAGUE and the HALL OF FAME: UMBRA PLATEAU's mapsec -- its card is the REVIEW BOARD, and T-456",
           "  suppresses it on the credits warp into the HALL.",
           "the S.S. ANNE: no card (no entry); its livery (pair 7) shows only on the map."]


def cards_census_sheet(path):
    nm = names()
    sec_of = {}
    for _, sec_, _, f in previews():                    # a card's FIRST mapsec (TANOBY's is MONEAN's)
        sec_of.setdefault(f, sec_)
    Z, cw, ch = 1, 240, 160
    cols = 3
    rows = (len(CARD_CENSUS) + cols - 1) // cols
    W = cols * (cw * 2 + 40) + 16
    H = 48 + rows * (ch + 56) + 20 + 16 * len(NO_CARD) + 20
    out = Image.new("RGB", (W, H), (34, 34, 40))
    d = ImageDraw.Draw(out)
    d.text((12, 10), "T-445 CENSUS (2026-11-11) -- the landmarks' name cards: the card the engine shows today (left) "
           "and Nintendo's it replaced (right), at 1x", fill=(235, 235, 235), font=font(14))
    for i, (folder, what, status) in enumerate(CARD_CENSUS):
        x, y = 16 + (i % cols) * (cw * 2 + 40), 44 + (i // cols) * (ch + 56)
        now, pal = engine_card(folder)
        draw_name(now, nm.get(sec_of[folder], "?"), pal)
        out.paste(now, (x, y + 34))
        try:
            vt, vm, vpal = vanilla(folder)
            out.paste(compose(vt, vm, vpal), (x + cw + 8, y + 34))
        except (SystemExit, AttributeError):          # a NEW card, or pret's rule spelled otherwise
            d.text((x + cw + 20, y + 100), "(no vanilla card read)", fill=(150, 150, 150), font=font(11))
        stale = "STALE" in status or "NINTENDO" in status
        d.text((x, y), "%s  (%s)" % (what, folder), fill=(240, 220, 120), font=font(12))
        d.text((x, y + 16), status, fill=(255, 140, 120) if stale else (170, 210, 170), font=font(11))
    y = 44 + rows * (ch + 56) + 4
    d.text((16, y), "NO CARD:", fill=(240, 220, 120), font=font(12))
    for k, line in enumerate(NO_CARD):
        d.text((16, y + 18 + k * 16), line, fill=(210, 210, 210), font=font(11))
    out.save(path)
    return path


#  what each DOLDRUM candidate is, on its sheet: (the read row, the unread row)
DOLDRUM_NOTES = {
    "cerulean_cave_becalmed_a": ("A  BECALMED: still air, still water, one point of light",
                                 "unread: the filter alone, no engine work"),
    "cerulean_cave_becalmed_b": ("A2 BECALMED, another seed, painted harder",
                                 "unread: the filter alone, no engine work"),
    "cerulean_cave_drawing_a": ("B  A SIMPLE DRAWING: already the four tones",
                                "the same both ways: one state, read or not"),
    "cerulean_cave_recomposed": ("C  WRONGLY ARRANGED: A's own tiles, misplaced",
                                 "as unread would see it IF the engine shuffles"),
    "cerulean_cave_mirror": ("D  THE PAINTED MIRROR: A unread, pool in colour",
                             "WITHOUT the engine's exemption the pool inks too"),
}


def doldrum_sheet(rows, path):
    """DOLDRUM CAVE's candidates beside TODAY's card: each at 2x and 1x as built (what the player who holds the
    understanding sees), and at 1x through T-255's drawing filter (what the unread player sees, by the code)"""
    nm = names()
    cw, ch = 480, 320
    cells = [("TODAY  cerulean_cave", None, "Nintendo's card, as the engine has it", "unread: inked by the filter")]
    for r in rows:
        a, b = DOLDRUM_NOTES.get(r["folder"], (r["folder"], ""))
        cells.append((a, r, "%s, %d tiles (< 450)" % (r["where"], r["tiles"]), b))
    W = 16 + len(cells) * (cw + 16)
    H = 64 + 30 + ch + 8 + 22 + 160 + 8 + 22 + 160 + 24
    out = Image.new("RGB", (W, H), (34, 34, 40))
    d = ImageDraw.Draw(out)
    d.text((12, 10), "T-445 DRAFT (2026-11-11) -- DOLDRUM CAVE's name card (cerulean_cave): TODAY's (left) and four "
           "directions, each at 2x and 1x AS BUILT -- what the player holding the understanding sees -- and at 1x "
           "UNREAD,", fill=(235, 235, 235), font=font(14))
    d.text((12, 28), "through fieldmap.c's four tones of ink on warm paper (T-255: DaemonsGreyHalftoneFrame tones the "
           "preview's palettes while DaemonsCaveUnperceived -- read from the code, not seen on a screen). DRAFT, "
           "nothing written to the engine.", fill=(235, 235, 235), font=font(14))
    y = 64
    for k, (label, r, note, unote) in enumerate(cells):
        x = 16 + k * (cw + 16)
        if r is None:
            im, pal = engine_card("cerulean_cave")
            draw_name(im, nm.get("MAPSEC_CERULEAN_CAVE", "DOLDRUM CAVE"), pal)
        else:
            im = r["draft"]
        d.text((x, y), label, fill=(170, 170, 170) if k == 0 else (240, 220, 120), font=font(12))
        d.text((x, y + 14), note, fill=(200, 200, 200), font=font(10))
        out.paste(im.resize((cw, ch), Image.NEAREST), (x, y + 30))
        yy = y + 30 + ch + 8
        d.text((x, yy), "AS BUILT, 1x", fill=(170, 210, 170), font=font(11))
        out.paste(im, (x, yy + 18))
        yy += 18 + 160 + 8
        d.text((x, yy), "UNREAD, 1x -- " + unote, fill=(255, 170, 140), font=font(11))
        out.paste(unread(im), (x, yy + 18))
    out.save(path)
    return path


def cards_sheet(rows, path):
    """today's card and each candidate for it, at 2x with the 1x beneath, one engine card a row"""
    nm = names()
    by = collections.OrderedDict()
    for r in rows:
        by.setdefault(CARDS[r["folder"]]["folder"], []).append(r)
    sec_of = {}
    for _, sec_, _, f in previews():                    # a card's FIRST mapsec (TANOBY's is MONEAN's)
        sec_of.setdefault(f, sec_)
    cw, ch = 480, 320
    n = max(len(v) for v in by.values()) + 1
    W = 16 + n * (cw + 16)
    RH = 30 + ch + 8 + 160 + 30
    out = Image.new("RGB", (W, 44 + len(by) * RH), (34, 34, 40))
    d = ImageDraw.Draw(out)
    d.text((12, 10), "T-445 DRAFT (2026-11-11) -- the landmarks' name cards: TODAY's card (left) and the candidates "
           "painted from T-447 pairs 4-5 as built, each at 2x with 1x below; nothing written", fill=(235, 235, 235),
           font=font(14))
    y = 44
    for folder, rs in by.items():
        now, pal = engine_card(folder)
        draw_name(now, nm.get(sec_of[folder], "?"), pal)
        cells = [("TODAY  %s" % folder, now, "the engine's card now")] + \
                [("%s  %s" % (chr(65 + i), r["folder"]), r["draft"], "%s, %d tiles" % (r["where"], r["tiles"]))
                 for i, r in enumerate(rs)]
        for k, (label, im, note) in enumerate(cells):
            x = 16 + k * (cw + 16)
            d.text((x, y), label, fill=(170, 170, 170) if k == 0 else (240, 220, 120), font=font(12))
            d.text((x, y + 14), note, fill=(200, 200, 200), font=font(10))
            out.paste(im.resize((cw, ch), Image.NEAREST), (x, y + 30))
            out.paste(im, (x, y + 30 + ch + 8))
        y += RH
    out.save(path)
    return path


# ================================================================== main
def new_rule(rules, folder, n):
    """graphics_file_rules.mk with a NEW card's -num_tiles rule (T-456), laid in among the others in name order; a
    card that has one is left as it is"""
    if "$(MAPPREVIEWGFXDIR)/%s/tiles.4bpp:" % folder in rules:
        return rules
    rule = "$(MAPPREVIEWGFXDIR)/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles %d -Wnum_tiles\n\n" % (folder, n)
    at = [(mm.group(1), mm.start()) for mm in re.finditer(r"^\$\(MAPPREVIEWGFXDIR\)/(\w+)/tiles\.4bpp:", rules, re.M)]
    after = [i for f, i in at if f > folder]
    if after:
        return rules[:after[0]] + rule + rules[after[0]:]
    last = at[-1][1]
    end = rules.index("\n\n", last) + 2
    return rules[:end] + rule + rules[end:]


def entry(by_folder, folder):
    """(MPS key, MAPSEC, type) of a card: sMapPreviewScreenData's, or a NEW card's own (T-456)"""
    c = cfg(folder)
    if folder in CARDS:                                 # a candidate for an engine card: that card's entry
        return by_folder[c["folder"]][0]
    if folder not in by_folder and c.get("new"):
        return c["mps"], c["mapsec"], c["type"]
    return by_folder[folder][0]


def report():
    nm = names()
    by_folder = collections.OrderedDict()
    for key, sec, typ, folder in previews():
        by_folder.setdefault(folder, []).append((key, sec, typ))
    print("  %d preview entries, %d pictures (graphics/map_preview/)" % (sum(len(v) for v in by_folder.values()),
                                                                         len(by_folder)))
    for folder, ents in by_folder.items():
        status = ("batch E: " + BATCH_E[folder]) if folder in BATCH_E else \
            ("batch G: %s, drafted%s" % (BATCH_G[folder], ", APPROVED" if folder in BATCH_G_APPROVED else
                                         ", waits on the user")) if folder in BATCH_G else \
            ("landmark (%s): drafted with --landmarks%s" % (landmark_source(folder),
             ", APPROVED" if folder in LANDMARK_APPROVED else ", waits on the user")) if folder in LANDMARK else \
            ("place (%s): drafted with --places%s" % (PLACES[folder]["what"],
             ", APPROVED" if folder in PLACES_APPROVED else ", waits on the user")) if folder in PLACES else \
            ("not drafted: " + NOT_DRAFTED.get(folder, "?"))
        if folder in CARDS_TAKEN:
            status += "; SUPERSEDED by --cards' %s (APPROVED)" % CARDS_TAKEN[folder]
        print("  %-17s %s" % (folder, status))
        for key, sec, typ in ents:
            n = nm.get(sec, "?")
            w = name_width(n)
            print("      %-22s %-34s %-16s %3dpx%s" % (key, sec, n, w, "  ** wider than the 104px window" if w > 104 else ""))
    for folder, c in list(LANDMARK.items()) + list(PLACES.items()):
        if c.get("new") and folder not in by_folder:
            n = nm.get(c["mapsec"], "?")
            if folder in PLACES:
                print("  %-17s NEW card (%s; the engine shows %s's): drafted with --places, waits on the user and on "
                      "its engine entry" % (folder, c["what"], c["banner_from"]))
            else:
                print("  %-17s NEW card (%s, no vanilla picture): drafted with --landmarks, waits on the user and on "
                      "T-456's engine entry" % (folder, landmark_source(folder)))
            print("      %-22s %-34s %-16s %3dpx" % (c["mps"], c["mapsec"], n, name_width(n)))
    return by_folder


def main():
    if A.write and not A.approved:
        print("  --write refuses without --approved: the user approves a preview before it is written.")
        return 1
    by_folder = report()
    if A.paint is not None:
        for folder in (A.paint or list(CARDS if A.cards else LANDMARK if A.landmarks else PLACES if A.places
                                       else PAINT)):
            key, sec, typ = entry(by_folder, folder)
            paint(folder, sec, A.draft or DRAFT_DEFAULT)
        if not (A.draft or A.write):
            return 0
    if not (A.draft or A.write):
        return 0
    nm = names()
    out_dir = A.draft or DRAFT_DEFAULT
    sheets = A.sheets or out_dir
    rows = []
    for folder in (CARDS if A.cards else LANDMARK if A.landmarks else PLACES if A.places else {**BATCH_E, **BATCH_G}):
        if A.only and folder not in A.only:
            continue
        if A.cards and A.write and folder not in CARDS_APPROVED and not A.draft:
            print("  %-27s a candidate, not approved (CARDS_APPROVED): not written" % folder)
            continue
        if A.write and not A.cards and folder in CARDS_TAKEN and not A.draft:
            print("  %-17s taken by --cards' %s (CARDS_APPROVED): not written" % (folder, CARDS_TAKEN[folder]))
            continue
        if A.write and folder in BATCH_G and folder not in BATCH_G_APPROVED and not A.draft:
            print("  %-17s batch G, not approved (BATCH_G_APPROVED): not written" % folder)
            continue
        if A.write and cfg(folder).get("new") and folder not in by_folder and not A.draft:
            print("  %-17s a NEW card: the engine has no sMapPreviewScreenData entry for it yet: not written" % folder)
            continue
        if A.landmarks and A.write and folder not in LANDMARK_APPROVED and not A.draft:
            print("  %-17s not approved (LANDMARK_APPROVED): not written" % folder)
            continue
        if A.places and A.write and folder not in PLACES_APPROVED and not A.draft:
            print("  %-17s not approved (PLACES_APPROVED): not written" % folder)
            continue
        key, sec, typ = entry(by_folder, folder)
        made = build(folder, sec)
        if not made:
            print("  %-17s nothing drawn" % folder)
            continue
        tiles, m, pal, where, png = made
        vt, vm, vpal = van(folder)
        van_, dra = compose(vt, vm, vpal), compose(tiles, m, pal)
        if LANDMARK.get(folder, {}).get("new"):             # no vanilla card: the building as the engine draws it
            van_ = Image.new("RGB", (240, 160))
            b = landmark_drawing(LANDMARK[folder]["source"])
            van_.paste(b.convert("RGB"), ((240 - b.size[0]) // 2, (160 - b.size[1]) // 2), b)
        for im in (van_, dra):
            draw_name(im, nm[sec], (vpal if im is van_ else pal))
        what = CARDS[folder]["title"] if A.cards else ("from %s, as built" % landmark_source(folder)) if A.landmarks else \
            PLACES[folder]["what"] if A.places else {**BATCH_E, **BATCH_G}[folder]
        notes = ["%s, %s" % (nm[sec], sec), "type %s" % typ, what, "",
                 "tiles: %d (vanilla %d; must stay < 450)" % (len(tiles), len(vt)),
                 "palette 13: 15 colours + vanilla's 0", "palette 14, letterbox, banner: vanilla's"]
        painted = where.startswith("painted")
        lights = light_palettes(pal[:16], dra, van_) if folder == "altering_cave" and painted else None
        if lights:
            notes += ["", "OTHER CAVE: one set of tiles, four", "palettes 13 (teal, AMBER, CHRYSOPRASE,",
                      "ROSE QUARTZ) -- the rows below. The", "engine lays the coming visit's light",
                      "over palette 13."]
        elif folder == "altering_cave":
            notes += ["", "OTHER CAVE cycles four lights;", "this preview shows one (teal).",
                      "Following the light is engine code."]
        if len(tiles) >= 450:
            notes += ["", "** TOO MANY TILES for baseBlock 0x1C2"]
        print("  %-17s %-16s %3d tiles  from %s" % (folder, nm[sec], len(tiles), where))
        if A.draft:
            d = os.path.join(out_dir, folder)
            os.makedirs(d, exist_ok=True)
            tiles_png(png, pal, os.path.join(d, "tiles.png"))
            open(os.path.join(d, "tilemap.bin"), "wb").write(struct.pack("<640H", *m))
            dra.save(os.path.join(d, "preview.png"))
            for n, lp in list(enumerate(lights or []))[1:]:
                write_pal(lp, os.path.join(d, "light%d.pal" % n))
                li = compose(tiles, m, lp + pal[16:32])
                draw_name(li, nm[sec], pal)
                li.save(os.path.join(d, "preview_light%d.png" % n))
            json.dump({"mapsec": sec, "name": nm[sec], "from": where, "num_tiles": len(tiles)},
                      open(os.path.join(d, "draft.json"), "w"), indent=1)
        if A.write and (not A.landmarks or folder in LANDMARK_APPROVED) and (not A.places or folder in PLACES_APPROVED) \
                and (folder not in BATCH_G or folder in BATCH_G_APPROVED) and (not A.cards or folder in CARDS_APPROVED):
            dest = cfg(folder).get("folder", folder)            # a CARDS candidate writes its engine card's folder
            d = os.path.join(MPS, dest)
            os.makedirs(d, exist_ok=True)                                # a NEW card's folder (T-456)
            tiles_png(png, pal, os.path.join(d, "tiles.png"))
            open(os.path.join(d, "tilemap.bin"), "wb").write(struct.pack("<640H", *m))
            for n, lp in list(enumerate(lights or []))[1:]:          # OTHER CAVE: map_preview_screen.c INCBINs these
                write_pal(lp, os.path.join(d, "light%d.pal" % n))
            rules = new_rule(open(RULES).read(), dest, len(tiles))
            rules = re.sub(r"(\$\(MAPPREVIEWGFXDIR\)/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+"
                           % dest, lambda mm: mm.group(1) + str(len(tiles)), rules)
            open(RULES, "w").write(rules)
            print("      written %s" % d)
        rows.append(dict(folder=folder, name=nm[sec], where=where, vanilla=van_, draft=dra, notes=notes,
                         tiles=len(tiles)))
        for n, lp in enumerate(lights or []):
            if n == 0:
                continue
            li = compose(tiles, m, lp + pal[16:32])
            draw_name(li, nm[sec], pal)
            rows.append(dict(folder=folder, name="%s, light %d (%s)" % (nm[sec], n, LIGHT_NAMES[n]),
                             where=where, vanilla=van_, draft=li,
                             notes=["light %d: %s" % (n, LIGHT_NAMES[n]), "the same tiles, palette 13 moved",
                                    "onto this light's rock and crystal", "ramps (palettes_other_%d)" % n]))
    if A.draft and A.cards and rows and all(CARDS[r["folder"]]["folder"] == "cerulean_cave" for r in rows):
        os.makedirs(sheets, exist_ok=True)              # DOLDRUM's own sheet; the others' sheets left as they are
        print("  sheet -> %s" % doldrum_sheet(rows, os.path.join(sheets, "t445L_doldrum.png")))
        return 0
    if A.draft and A.cards:
        os.makedirs(sheets, exist_ok=True)
        print("  sheet -> %s" % cards_census_sheet(os.path.join(sheets, "t445L_census.png")))
        print("  sheet -> %s" % cards_sheet(rows, os.path.join(sheets, "t445L_candidates.png")))
        return 0
    if A.draft:
        os.makedirs(sheets, exist_ok=True)
        painted = any(r["where"].startswith("painted") for r in rows)
        per = 5 if painted else (len(rows) + 1) // 2
        parts = [rows[i:i + per] for i in range(0, len(rows), per)]
        for i, part in enumerate(parts, 1):
            if A.places:
                p = sheet(part, os.path.join(sheets, "t445f_%d.png" % i),
                          "T-445 DRAFT -- the forests' and the SAFARI's cards, vanilla (left) and PAINTED in the "
                          "colours they are built in now (right); the name is the game's, in its own font. Sheet %d "
                          "of %d." % (i, len(parts)))
            elif A.landmarks:
                p = sheet(part, os.path.join(sheets, "t445n_%d.png" % i),
                          "T-445 DRAFT -- the landmarks' name cards, vanilla (left) and PAINTED from T-447's buildings "
                          "(right); the name is the game's, in its own font. Sheet %d of %d." % (i, len(parts)))
            elif painted:
                p = sheet(part, os.path.join(sheets, "t445p_%d.png" % i),
                          "T-445 DRAFT -- the cave previews, vanilla (left) and PAINTED on the sprite server in each "
                          "cave's colours (right); the name is the game's, in its own font. Sheet %d of %d."
                          % (i, len(parts)))
            else:
                p = sheet(part, os.path.join(sheets, "t445_previews_%d.png" % i),
                          "T-445 DRAFT -- the cave previews, vanilla (left) and drawn from the batch E caves (right); "
                          "the name is printed by the game, shown here in its own font. Sheet %d of %d."
                          % (i, len(parts)))
            print("  sheet -> %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
