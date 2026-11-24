#!/usr/bin/env python3
"""T-604 stages 1 to 9 (DRAFT): give a later form a REGION in its new part's colours, by RECOLOURING a natural part of the
drawing already there (ears, crest, tail, drawers, wings), so it visibly colours in as it learns its part (T-597).

    python3 gfx/drafts/t604/scripts/t604_regions.py               # report each form: region, slots, coverage before/after
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 2 ...  # the same for STAGE 2's twelve (FORMS2)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 3 ...  # ... and STAGE 3's fifteen (FORMS3)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 4 ...  # ... and STAGE 4's fifteen (FORMS4)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 5 ...  # ... and STAGE 5's fifteen (FORMS5)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 6 ...  # ... and STAGE 6's fifteen (FORMS6)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 7 ...  # ... and STAGE 7's fifteen (FORMS7)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 8 ...  # ... and STAGE 8's fifteen (FORMS8)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 9 ...  # ... and STAGE 9's fifteen (FORMS9)
    python3 gfx/drafts/t604/scripts/t604_regions.py --draft       # write the drafts into gfx/drafts/t604/<NAME>/
    python3 gfx/drafts/t604/scripts/t604_regions.py --sheet DIR   # ... and the contact sheet into DIR
    python3 gfx/drafts/t604/scripts/t604_regions.py --built --sheet DIR   # the sheet from the engine as BUILT (after
                                                                  # gbasprite --write), today from <NAME>/base/
    python3 gfx/drafts/t604/scripts/t604_regions.py --base        # file each form's pre-T-604 art into <NAME>/base/
    python3 gfx/drafts/t604/scripts/t604_regions.py --install     # APPROVED (the user, 2026-11-22): file each draft as
                                                                  # gbasprite's approved reduction, gfx/daemons/reduced/

Reads the engine's sprites; never writes the engine. The draft palettes and pictures go in gfx/drafts/t604/<NAME>/
(front.png, back.png, normal.pal), and the colour maths is tools/gencolourbysong.py's own: each draft is judged by
pointing gencolourbysong's World at the draft folder for that one form, so what the sheet shows is what the game would.

A region is: rectangles (front, back) in the 64x64 frame, the source slots inside them that are recoloured (never the
ink 5, never the streaks 11-14), and a map from each source slot to a NEW slot whose colour is a ramp of one colour --
the form's NEW TYPE where it has one (the argument: invariant 5), else a note its own part sings (the key leaned into).
A slot freed for it by MERGE is a near-duplicate folded into its neighbour first (a handful of pixels). A region of two
parts that want different slots (a ring and the coat it rings) gives the second as "extra": [dict(front, back, slotmap)].
"""
import colorsys, os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gencolourbysong as g
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(ROOT, "gfx", "drafts", "t604")
#  TODAY is the art as it stood before T-604 (engine b15b3aff5), filed in <NAME>/base/ by --base: once --install has run
#  the engine carries the drafts, and a re-run must start from what they were drawn on, never from themselves.
BASE_COMMIT = "b15b3aff5"
TYPE = {"SIGNAL": (86, 190, 190), "LATENT": (92, 70, 118), "VECTOR": (206, 70, 70), "LOGIC": (96, 122, 158)}


def ramp3(c, up=0.38, dn=0.52):
    r, gg, b = c
    return [tuple(min(255, int(x + (255 - x) * up)) for x in c), tuple(c), tuple(max(0, int(x * dn)) for x in c)]


def R(*boxes):
    return [tuple(b) for b in boxes]


#  name: why, the colour's source, the colour, rectangles (x0,y0,x1,y1 inclusive) front / back, {source slot: new slot},
#  the new slots' colours, and merges {slot: into} made first to free a slot.
FORMS = {
    "ROVERSEER": dict(
        why="ROVER line, stage 2 (starter, 8.2): every colour carried from ROVERCUB, nothing to learn",
        region="the floppy EARS and the tail tip", colour="E, a note its part sings (gold)", base=g.pc_rgb(4),
        front=R((8, 9, 17, 31), (34, 8, 45, 30), (44, 47, 54, 53)), back=R((12, 9, 23, 27), (39, 9, 48, 27)),
        slotmap={1: 7, 2: 7, 3: 8, 4: 8}, ramp="two"),
    "ROVERBYTE": dict(
        why="ROVER line, stage 3 (starter): 0.5% waits; SIGNAL is the new type, 'arriving exactly where the body does'",
        region="the DOME of the head (its cap), in SIGNAL", colour="SIGNAL, the new type", base=TYPE["SIGNAL"],
        front=R((8, 2, 48, 18)), back=R((10, 4, 54, 20)),
        slotmap={1: 6, 2: 9, 3: 10, 4: 10}, ramp="keep6"),
    "RUBRIC": dict(
        why="LABEL line, stage 2 (starter): 2.3% waits (only the pink cheeks)",
        region="the box's TOP and SIDE faces in front; the RULED GRID behind (a marking scheme, in red pen)",
        colour="C, the key's tonic (red pen)", base=g.pc_rgb(0),
        front=R((14, 9, 50, 15), (44, 9, 50, 40)), back=R((17, 13, 45, 46)),
        slotmap={2: 7, 3: 10, 4: 10}, merge={7: 6}, backonly_slots={3}, ramp=None),
    "CANON": dict(
        why="LABEL line, stage 3 (starter): every colour carried; LOGIC's blue is RUBRIC's blue, so it cannot be new",
        region="the two DRAWERS (their faces), in brass", colour="E, a note its part sings (brass)", base=g.pc_rgb(4),
        front=R((38, 17, 52, 46)), back=R((38, 11, 54, 45)),
        slotmap={1: 9, 2: 9, 3: 10, 4: 10}, ramp=None),
    "LOCUS": dict(
        why="CLUSTER line, stage 2 (starter): 1.3% waits",
        region="the curled TAIL (a locus: points that share a rule)", colour="Eb, a note its part sings (amber)",
        #  not Bb's violet: MANIFOLD would carry it, and LATENT's purple is MANIFOLD's to learn
        base=g.pc_rgb(3),
        front=R((37, 14, 53, 33)), back=R((12, 14, 28, 32)), dark=(122, 82, 12),
        slotmap={2: 6, 3: 9, 4: 10}, ramp=None),
    "MANIFOLD": dict(
        why="CLUSTER line, stage 3 (starter): every colour carried; LATENT is the new type",
        region="the wing's UNDERSIDE in front, the WING TIPS behind, in LATENT", colour="LATENT, the new type, moved to mulberry",
        #  LATENT moved toward mulberry: its own (92,70,118), and any purple near it, sits within 80 of LOCUS's navy eyes
        #  (90,96,140) and CLUSTER's dark cyan, colours MANIFOLD lost -- and gencolourbysong's "nearest to one" (CARRY_FAR)
        #  then CARRIES it, so it would never wait. (140,44,104) is the nearest LATENT-ward colour that escapes.
        base=(140, 44, 104),
        front=R((30, 35, 58, 46)), back=R((0, 24, 17, 42), (47, 24, 63, 42)), dark=(96, 12, 84),
        slotmap={1: 7, 2: 7, 3: 8, 4: 9}, ramp=None),
    "REFORGE": dict(
        why="PIXELBYTE line (the project's own: the tool that drew the bestiary, 6874): 3.4% waits",
        region="the FORGE: its chimney and its bench, glowing", colour="C#, a note its part sings (ember)",
        base=g.pc_rgb(1),
        front=R((39, 7, 50, 26), (34, 25, 57, 34), (52, 34, 57, 50)), back=R((13, 7, 24, 26), (7, 25, 30, 34), (7, 34, 12, 50)),
        slotmap={1: 10, 2: 10, 3: 10}, ramp="mid"),
    "LANGMUSAI": dict(
        why="MUSAI line (the project's own, 8.5/6874): no accent at all, only the body ramp comes in",
        region="the TAIL and the two ANTENNAE", colour="C#, a note its part sings (coral)", base=g.pc_rgb(1),
        front=R((38, 30, 55, 50), (14, 6, 20, 16), (33, 6, 42, 16)), back=R((13, 32, 25, 50), (20, 6, 27, 14), (44, 6, 50, 14)),
        slotmap={1: 7, 2: 7, 3: 8, 4: 8}, ramp="two"),
    "HOPE": dict(
        why="TRUST line ('the egg you are handed', 8.5): 4.3% waits; VECTOR is the new type",
        #  the user, 2026-11-22: the red at the WING TIPS and the long TAIL FEATHER only, softer (not the whole wing)
        region="the WING TIPS and the long TAIL FEATHER, in a soft VECTOR",
        colour="VECTOR, the new type, softened to coral", base=(226, 96, 90),
        front=R((43, 3, 53, 13), (5, 5, 12, 13), (38, 36, 58, 43)), back=R((12, 3, 22, 13), (52, 6, 61, 15), (6, 36, 26, 43)),
        slotmap={1: 6, 2: 6, 3: 8, 4: 8}, merge={6: 4}, ramp="hope"),
}
ORDER = list(FORMS)
STAGE = 1

#  STAGE 2 (the user, 2026-11-22: "T-604 stage 2"; DRAFT): twelve more, the later forms a player meets first or most
#  -- the early routes' lines (PACKET, NIBBLE, PING, CRAWLER), the gym leaders' signatures (SURGE, SMOGSTACK, STACK's
#  HEAP for BROCK, SCHEDULER for GIOVANNI), the line the story sells you (STUB at MT. MOON) and MT. MOON's own two.
#  TODAY for these is the engine as it stands (BASE2, after stage 1): no form here was drawn by stage 1.
BASE2_COMMIT = "bff3f856b"
TYPE.update({"STRATUM": (158, 122, 78)})
FORMS2 = {
    "RELAY": dict(
        why="PACKET line, stage 2 (ROUTE 1's bird; the rival's RELAY at CERULEAN): 4.6% waits",
        region="the NECK, a pigeon's sheen", colour="F, a note its part sings (green sheen)",
        base=g.pc_rgb(5),
        front=R((17, 17, 47, 27)), back=R((20, 13, 46, 26)),
        slotmap={1: 7, 2: 7, 3: 9, 4: 9}, merge={7: 8, 9: 8}, ramp="two"),
    "BROADCAST": dict(
        why="PACKET line, stage 3: 0.0% waits -- every colour carried",
        region="the raised WINGS' flight feathers", colour="E, a note its part sings (gold)", base=g.pc_rgb(4),
        front=R((3, 8, 14, 37), (36, 8, 60, 33)), back=R((3, 8, 18, 30), (42, 8, 62, 30)),
        #  its dark moved to bronze: E's own dark sits 80 from PACKET's maroon (100,11,33) and would be CARRIED
        dark=(120, 94, 20), slotmap={1: 7, 2: 7, 3: 8, 4: 10}, ramp=None),
    "OVERFLOW": dict(
        why="NIBBLE line, stage 2 (ROUTE 1's other daemon; the rival's): 3.9% waits",
        region="a golden hamster's coat: the crown and flanks in front, the shoulders behind",
        colour="D, a note its part sings (golden)", base=g.pc_rgb(2),
        front=R((14, 5, 50, 17), (2, 17, 12, 48), (52, 17, 62, 48)), back=R((14, 8, 50, 24)),
        slotmap={2: 7, 3: 7, 4: 10}, merge={7: 8}, ramp="two"),
    "FLOOD": dict(
        why="PING line, stage 2 (ROUTE 22 and 3's bird): 4.8% waits",
        region="the WINGS, a kingfisher's blue", colour="G, a note its part sings (blue)", base=g.pc_rgb(7),
        front=R((30, 16, 54, 40)), back=R((8, 12, 26, 30), (38, 12, 58, 30)),
        slotmap={1: 6, 2: 6, 3: 9, 4: 9}, merge={6: 7}, ramp="two"),
    "INDEXER": dict(
        why="CRAWLER line, stage 3 (VIRIDIAN FOREST's): 0.8% waits; VECTOR is the new type",
        region="the FOREWINGS' pale panels, a cinnabar moth's", colour="VECTOR, the new type, moved to vermilion",
        #  not HOPE's coral: it sits within 80 of PENDING's dusty rose (192,121,134), which would CARRY it
        base=(220, 80, 50),
        front=R((4, 14, 16, 30), (48, 14, 60, 30)), back=R((10, 14, 24, 28), (46, 14, 60, 28)),
        slotmap={1: 6, 2: 6, 3: 7, 4: 7}, merge={6: 7, 7: 8}, ramp="two"),
    "SURGE": dict(
        why="STATIC line, stage 3 (LT. SURGE's own): 2.7% waits",
        region="the TAIL and the dark SADDLE down its back", colour="C#, a note its part sings, moved to amber",
        #  C#'s own ember sits 41 from STATIC's red cheek (219,84,84), so it would be CARRIED; amber escapes
        base=(226, 160, 44),
        front=R((24, 26, 48, 46)), back=R((20, 16, 44, 40), (44, 20, 62, 40)),
        slotmap={3: 7, 4: 10}, merge={7: 6}, ramp="two"),
    "TRACER": dict(
        why="ECHO line, stage 2 (MT. MOON and every cave after; KOGA's): 0.6% waits",
        region="the WINGS' membranes, glowing like a tracer round", colour="Eb, a note its part sings (amber)",
        base=g.pc_rgb(3),
        front=R((0, 6, 14, 30), (45, 6, 63, 32)), back=R((0, 6, 20, 32), (44, 6, 63, 32)),
        #  its dark moved off ECHO's olive (84,92,52): E-flat's own dark sits 39 from it, the same colour, and is CARRIED
        dark=(100, 62, 10), slotmap={2: 9, 3: 9, 4: 10}, ramp="two"),
    "STACK": dict(
        why="HEAP line, stage 2 (BROCK's HEAP; ROCK TUNNEL, VICTORY ROAD): 0.8% waits",
        region="the two BOULDERS at its sides (its arms): a stratum", colour="D, a note its part sings (rust)",
        base=g.pc_rgb(2),
        front=R((5, 36, 17, 50), (46, 36, 58, 50)), back=R((5, 36, 18, 50), (45, 36, 58, 50)),
        slotmap={1: 8, 2: 8, 3: 9, 4: 10}, ramp=None),
    "SMOGSTACK": dict(
        why="EXHAUST line, stage 2 (KOGA's own; the MANSION): 4.7% waits",
        region="the SMOKE above the stack, a yellow smog", colour="Eb, a note its part sings (smog)",
        base=g.pc_rgb(3),
        front=R((26, 2, 48, 15)), back=R((26, 2, 48, 15)),
        slotmap={1: 9, 2: 9, 3: 10, 4: 10}, ramp="lomid"),
    "ESCALATE": dict(
        why="STUB line, stage 2 (the STUB sold at MT. MOON; GIOVANNI's; every rod): 4.8% waits; VECTOR is new",
        region="the BELLY PLATES, the whole length of it (a red-bellied serpent)",
        colour="VECTOR, the new type, lightened to salmon",
        #  lighter and pinker than HOPE's coral: a warmer one sits within 80 of STUB's tan (162,135,83), and is CARRIED;
        #  one slot, the palest of the body's (1), everywhere it is drawn -- a cut region read as a wound
        base=(240, 110, 120),
        front=R((0, 0, 63, 63)), back=R((0, 0, 63, 63)),
        slotmap={1: 9}, ramp="one"),
    "SCHEDULER": dict(
        why="FORK line, stage 3 (GIOVANNI's): 2.9% waits; STRATUM is the new type",
        region="the CHEST PLATE and SHOULDER PADS, in STRATUM", colour="STRATUM, the new type", base=TYPE["STRATUM"],
        front=R((4, 34, 16, 50), (48, 34, 60, 50), (24, 40, 40, 50)), back=R((6, 20, 20, 36), (44, 20, 58, 36)),
        #  its dark moved off FORK's olive (84,92,52): STRATUM's own dark sits 31 from it and is CARRIED
        dark=(96, 56, 28), slotmap={1: 7, 2: 7, 3: 10, 4: 10}, merge={7: 8}, ramp="two"),
    "ANOMALY": dict(
        why="RESIDUAL line, stage 2 (MT. MOON's; the GAME CORNER's prize): 3.4% waits",
        region="the HORNS and the WINGS", colour="E, a note its part sings (gold)", base=g.pc_rgb(4),
        front=R((14, 6, 26, 18), (38, 6, 50, 18), (6, 24, 18, 44), (46, 24, 58, 44)),
        back=R((16, 16, 26, 24), (40, 16, 50, 24), (12, 26, 22, 40), (44, 26, 54, 40)),
        slotmap={1: 9, 2: 9, 3: 8, 4: 8}, merge={9: 10, 8: 7}, ramp="two"),
}


#  STAGE 3 (the user, 2026-11-22: "T-604 stage 3"; DRAFT): fifteen more -- the rest of the gym leaders' aces (ERIKA,
#  SABRINA, BLAINE, GIOVANNI's gym), the rival's from SILPH on and the CHAMPION's, each of the ELITE FOUR's signatures,
#  and the mid-game's own (POKEMON TOWER's ghost, its MAROWAK, VICTORY ROAD's, GIOVANNI's at the HIDEOUT).
#  TODAY is the engine after stage 2 (BASE3): no form here was drawn by stage 1 or 2. Every colour is given exactly
#  ("cols"), each checked against the carry rule by the report: none may read CARRIED.
BASE3_COMMIT = "740b79ae5"
FORMS3 = {
    "TARPIT": dict(
        why="SNARE line, stage 3 (ERIKA's VICTREEBEL): 0.9% waits",
        region="the LEAVES, glazed amber as if in resin", colour="D, a note its part sings (resin amber)",
        #  not E's gold: it sits within 80 of HONEYPOT's yellow-green (194,222,105), which TARPIT lost, and is CARRIED
        base=g.pc_rgb(2),
        front=R((8, 2, 58, 21), (8, 21, 22, 30), (44, 21, 58, 30)), back=R((6, 1, 58, 15), (6, 15, 19, 26), (41, 15, 60, 28)),
        #  the light tone more orange than gold: a goldener one sits nearest HONEYPOT's yellow-green and is CARRIED
        #  the leaves' mid tone onto the mid amber, so the back (drawn darker) reads amber, not withered
        slotmap={1: 6, 2: 6, 3: 8, 4: 10}, merge={6: 7, 8: 7}, ramp="cols",
        cols={6: (236, 150, 80), 8: (201, 112, 46), 10: (120, 60, 20)}),
    "OVERDRIVE": dict(
        why="HOTPATH line, stage 2 (BLAINE's; MT. EMBER): 0.5% waits",
        region="the MANE and TAIL, burning blue-hot", colour="Ab, a note its part sings (a blue flame)",
        #  not Ab's own blue: OVERDRIVE's eye-blue (46,97,158) is HOTPATH's, and Ab sits 27 from it, CARRIED
        base=(90, 120, 235),
        front=R((10, 3, 32, 18), (18, 18, 34, 30), (44, 18, 62, 30), (48, 30, 62, 48)),
        back=R((30, 9, 54, 30), (2, 34, 16, 48)),
        #  the cream highlights (slot 1) stay: the white-hot core of the flame, and the face stays the face
        slotmap={2: 8, 3: 10, 4: 10}, merge={8: 7}, ramp="cols",
        cols={8: (140, 175, 250), 10: (70, 90, 220)}),
    "GUARDIAN": dict(
        why="SENTRY line, stage 2 (BLAINE's ace; the rival's from the CHAMPION on): 0.1% waits",
        region="the CREST of fur on its head and the TAIL's markings, an ember", colour="C#, a note its part sings (ember)",
        base=g.pc_rgb(1),
        front=R((26, 1, 58, 12), (2, 28, 26, 60)), back=R((24, 2, 60, 20), (2, 24, 24, 54)),
        #  the orange and its dark only: the cream fur stays cream, so the ember follows the drawing's own markings
        slotmap={3: 7, 4: 9}, ramp="cols",
        cols={7: (232, 120, 70), 9: (160, 60, 30)}),
    "SPYWARE": dict(
        why="RESIDENT line, stage 2 (SABRINA's; the SAFARI ZONE): 3.1% waits",
        region="the four WINGS' outer panels, a violet moth's", colour="B, a note its part sings, moved to orchid",
        #  not B's own violet: it sits within 80 of RESIDENT's blue-grey (95,123,163), which SPYWARE lost, CARRIED
        base=(170, 60, 170),
        front=R((0, 0, 20, 9), (0, 9, 14, 30), (46, 0, 63, 33), (41, 0, 46, 8)), back=R((0, 10, 20, 34), (46, 10, 63, 34)),
        #  the pale panels only (slot 1): the olive veins stay, carried, and draw the wing
        #  orchid kept saturated: a paler one sits nearest RESIDENT's grey-blue (132,168,203) and is CARRIED
        slotmap={1: 10}, slotmap_back={1: 10, 2: 10}, ramp="cols", cols={10: (195, 105, 205)}),
    "CONJECTURE": dict(
        why="HUNCH line, stage 3 (SABRINA's ace; the rival's from SILPH CO. to the CHAMPION): 0.0% waits",
        region="the TAIL and the ears' insides, a fox's turned gold", colour="E, a note its part sings (gold)",
        base=g.pc_rgb(4),
        front=R((38, 32, 60, 58), (16, 7, 27, 20), (43, 5, 57, 17)), back=R((38, 36, 62, 60)),
        slotmap={1: 8, 2: 8, 6: 8, 3: 9, 4: 9, 7: 9}, slotmap_back={1: 8, 2: 8, 3: 9, 4: 9}, ramp="cols",
        cols={8: (222, 190, 70), 9: (150, 112, 26)}),
    "MIGRATE": dict(
        why="HARDCODE line, stage 2 (GIOVANNI's ace at his gym; the CHAMPION's): 0.4% waits",
        region="the HORN and the SHOULDER SPIKES, a verdigris (old bronze)",
        colour="F#, a note its part sings, moved to verdigris",
        #  greener than F#'s own teal: that sits within 80 of HARDCODE's navy (44,70,120), which MIGRATE lost, CARRIED
        base=(70, 160, 110),
        front=R((25, 2, 39, 24), (4, 22, 20, 36), (44, 22, 60, 36)), back=R((25, 2, 39, 24), (4, 22, 20, 36), (44, 22, 60, 36)),
        slotmap={1: 9, 2: 9, 3: 10, 4: 10}, ramp="cols",
        #  the dark kept past 80 from HARDCODE's navy (44,70,120), which it would otherwise be nearest to, CARRIED
        cols={9: (110, 190, 140), 10: (40, 115, 50)}),
    "ARCHIVER": dict(
        why="HEATSINK line, stage 2 (LORELEI's lead; SEAFOAM ISLANDS): 0.0% waits; FROZEN is the new type",
        region="a FROST CAP over the crown, the tail's FLUKE and the four ice SPARKLES round it, in FROZEN", colour="FROZEN, the new type, deepened to ice cyan",
        #  FROZEN's own (166,206,222) sits 34 from HEATSINK's pale blue (199,210,231): the same colour, CARRIED
        base=(120, 210, 232),
        front=R((14, 6, 46, 19), (6, 12, 12, 18), (44, 6, 50, 12), (54, 26, 60, 32), (2, 30, 8, 36), (54, 33, 63, 40)),
        back=R((26, 6, 58, 19), (16, 6, 22, 12), (54, 12, 60, 18), (4, 26, 10, 32), (58, 30, 64, 36), (0, 33, 10, 40)),
        slotmap={1: 7, 2: 7, 3: 9, 4: 9}, ramp="cols",
        cols={7: (120, 210, 232), 9: (40, 150, 160)}),
    "LEMMA MIND": dict(
        why="PROOF line, stage 3 (BRUNO's ace): 0.9% waits",
        region="all four FISTS, in gold (gloves)", colour="Eb, a note its part sings (gold)",
        base=g.pc_rgb(3),
        front=R((4, 2, 22, 20), (42, 2, 60, 20), (2, 34, 14, 48), (50, 34, 62, 48)),
        back=R((4, 2, 22, 22), (42, 2, 60, 22), (2, 40, 14, 52), (50, 40, 62, 52)),
        #  one slot: the gold, shaded by the carried steel darks around it (the belt's darkest folded into its dark)
        slotmap={1: 10, 2: 10}, merge={10: 9}, ramp="cols", cols={10: (214, 160, 60)}),
    "HAUNTPROC": dict(
        why="DANGLING line, stage 3 (AGATHA's signature, twice): 6.0% waits",
        region="the pale BELLY in front, the HEM of the cloak behind, a ghost-light teal",
        colour="F#, a note its part sings, moved to a lighter teal",
        #  F#'s own teal sits 45 from RESPAWN's slate (85,105,149), nearer than any other: CARRIED
        base=(70, 170, 150),
        front=R((18, 28, 46, 52)), back=R((12, 42, 52, 62)),
        slotmap={1: 6, 2: 10}, slotmap_back={3: 10, 4: 10}, merge={6: 7}, ramp="cols",
        cols={6: (160, 225, 205), 10: (70, 170, 150)}),
    "SINGULAR": dict(
        why="CANARY line, stage 3 (LANCE's ace): 1.6% waits; VECTOR is the new type",
        region="the WINGS, the HORNS and the TAIL's last length, in VECTOR", colour="VECTOR, the new type, moved to flame orange",
        #  VECTOR's own red sits within 40 of CANARY's and EMERGENCE's pinks, CARRIED; orange escapes
        base=(240, 120, 60),
        front=R((38, 4, 58, 26), (50, 36, 60, 48), (18, 0, 34, 12), (44, 40, 60, 56)),
        back=R((14, 4, 30, 26), (2, 36, 14, 48), (32, 0, 58, 12), (2, 40, 20, 56)),
        slotmap={1: 8, 2: 8, 3: 9, 4: 9}, ramp="cols",
        cols={8: (240, 140, 80), 9: (170, 70, 30)}),
    "EMERGENCE": dict(
        why="CANARY line, stage 2 (LANCE's, twice; the SAFARI ZONE): 0.2% waits",
        region="the TAIL, its last length in violet", colour="B, a note its part sings (violet)",
        #  not E's gold: SINGULAR's VECTOR orange would sit nearest it and be CARRIED
        base=g.pc_rgb(11),
        front=R((40, 26, 60, 60)), back=R((0, 44, 24, 60)),
        slotmap={1: 9, 2: 9, 3: 10, 4: 10}, ramp="cols",
        cols={9: (170, 120, 215), 10: (95, 45, 135)}),
    "RESPAWN": dict(
        why="DANGLING line, stage 2 (POKEMON TOWER's ghost; AGATHA's): 1.1% waits",
        region="the two floating HANDS, lantern-lit", colour="Eb, a note its part sings (amber)",
        base=g.pc_rgb(3),
        front=R((4, 28, 20, 48), (44, 28, 62, 48)), back=R((0, 24, 14, 42), (50, 24, 64, 42)),
        slotmap={1: 7, 2: 7, 3: 8, 4: 8}, ramp="cols",
        cols={7: (230, 175, 80), 8: (150, 95, 20)}),
    "COREFILE": dict(
        why="ARTEFACT line, stage 2 (POKEMON TOWER's story; VICTORY ROAD): 0.7% waits",
        region="the two HORNS, a dusk violet", colour="B, a note its part sings (violet)",
        base=g.pc_rgb(11),
        front=R((0, 4, 17, 32), (47, 4, 63, 32)), back=R((0, 4, 17, 32), (47, 4, 63, 32)),
        slotmap={1: 7, 2: 7, 3: 8, 4: 9}, ramp="cols",
        cols={7: (190, 140, 220), 8: (138, 76, 174), 9: (72, 36, 96)}),
    "THEOREM": dict(
        why="PROOF line, stage 2 (VICTORY ROAD, CERULEAN CAVE; BRUNO's line): 0.4% waits",
        region="the SHOULDERS, indigo pauldrons", colour="A, a note its part sings (indigo)",
        #  not D's orange: LEMMA MIND's gold fists would sit within 40 of it and be CARRIED
        base=g.pc_rgb(9),
        front=R((2, 16, 18, 34), (46, 16, 62, 34)), back=R((2, 16, 18, 36), (46, 16, 62, 36)),
        slotmap={1: 7, 2: 7, 3: 10, 4: 10}, merge={10: 4, 7: 6}, ramp="cols",
        cols={7: (110, 108, 210), 10: (52, 48, 130)}),
    "PREDICTOR": dict(
        why="BRANCH line, stage 2 (GIOVANNI's at the ROCKET HIDEOUT; the SAFARI ZONE): 4.5% waits",
        region="the long EARS, outside, in violet", colour="Ab, a note its part sings, moved to violet",
        base=(120, 90, 200),
        front=R((4, 0, 24, 22), (38, 0, 60, 22)), back=R((8, 2, 32, 22), (36, 0, 58, 20)),
        slotmap={1: 9, 2: 9, 3: 10, 4: 10}, merge={9: 4}, ramp="cols",
        cols={9: (150, 125, 220), 10: (80, 55, 150)}),
}

#  STAGE 4 (the user, 2026-11-22: "T-604 stage 4"; DRAFT): fifteen more, by how often a player meets them -- the water
#  and fishing lines (SEADRA, TENTACRUEL, SEAKING, GOLDUCK), the common route and cave lines (PERSIAN, SANDSLASH,
#  PRIMEAPE, PARASECT, HYPNO), the POWER PLANT's two, the trainer-class staples (ARBOK for ROCKET, HITMONCHAN's dojo
#  line) and the rival's own (KADABRA, EXEGGUTOR). TODAY is the engine after stage 3 (BASE4): no form here was drawn
#  by stages 1-3. Every colour is given exactly ("cols"), each checked against the carry rule by the report.
BASE4_COMMIT = "954a6c817"
FORMS4 = {
    "BACKPRESS": dict(
        why="BOTTLENECK line, stage 2 (every rod from the SUPER ROD on; 18 trainers, the swimmers'): 0.0% waits",
        region="the CREST of spines behind its head and the little fins on top, sea-green",
        colour="F, a note its part sings (sea-green)", base=g.pc_rgb(5),
        front=R((6, 4, 19, 38), (22, 1, 46, 10)), back=R((22, 12, 30, 44), (30, 6, 48, 11)),
        slotmap={1: 8, 2: 8, 3: 9, 4: 10}, ramp="cols",
        cols={8: (130, 200, 140), 9: (63, 154, 85), 10: (30, 90, 50)}),
    "DRAGNET": dict(
        why="DRIFTNET line, stage 2 (the sea routes' commonest: 28 surfing tables): 4.2% waits",
        region="the BELL's crown, a moon-jelly violet", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((12, 5, 52, 14)), back=R((12, 8, 54, 15)),
        #  one tan of the rim folded into its neighbour (15 pixels) to free a slot; the navy shading stays
        slotmap={1: 7, 2: 7, 3: 10}, merge={7: 8}, ramp="cols",
        #  the light violet pinker than Bb's own: a bluer one sits within 40 of the body's blue (DRIFTNET's), CARRIED
        cols={7: (190, 135, 230), 10: (110, 75, 180)}),
    "UPSTREAM": dict(
        why="SPAWN line, stage 2 (the GOOD ROD's catch everywhere; 22 trainers): 0.0% waits",
        region="the FINS and the TAIL, a goldfish's orange", colour="C# (D-flat), a note its part sings (orange)",
        base=g.pc_rgb(1),
        front=R((46, 10, 62, 38), (20, 39, 34, 54), (18, 6, 40, 13)),
        back=R((2, 30, 20, 46), (20, 14, 46, 20), (28, 44, 34, 52), (42, 44, 50, 52)),
        slotmap={1: 7, 2: 7, 3: 10, 4: 10}, ramp="cols",
        cols={7: (245, 150, 90), 10: (200, 80, 40)}),
    "HANDLER": dict(
        why="FAULT line, stage 2 (21 tables, land and water; the SEAFOAM and SAFARI routes): 0.5% waits",
        region="the WINGS' flight feathers, a mallard's violet speculum", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((2, 17, 19, 36), (37, 17, 62, 36)), back=R((2, 17, 24, 36), (42, 17, 62, 36)),
        #  the wing-edge mauve (16 pixels) folded into the navy dark to free a slot
        slotmap={1: 7, 2: 7, 3: 8, 4: 8}, merge={7: 4}, ramp="cols",
        #  the light violet pinker than Bb's own: a bluer one sits within 40 of the body's blue (FAULT's), CARRIED
        cols={7: (185, 135, 230), 8: (95, 65, 175)}),
    "TRACKER": dict(
        why="COOKIE line, stage 2 (14 route tables; 18 trainers): 1.7% waits",
        region="a colourpoint cat: the EARS and the TAIL, and its tabby marks, in ginger",
        colour="D, a note its part sings (ginger)", base=g.pc_rgb(2),
        front=R((4, 0, 16, 13), (27, 4, 40, 15), (44, 8, 60, 42)),
        back=R((16, 4, 25, 15), (37, 4, 46, 15), (14, 48, 50, 57)),
        #  the eyes' brightest green folded into the next (8 pixels); the violet tabby marks (slot 9) turn ginger too
        slotmap={1: 6, 2: 6, 3: 9, 4: 9}, merge={6: 7}, ramp="cols",
        cols={6: (225, 150, 85), 9: (160, 85, 35)}),
    "PARTITION": dict(
        why="SECTOR line, stage 2 (ROUTE 4 and MT. MOON's side; 16 trainers): 0.0% waits",
        region="the top row of its ARMOUR PLATES, rust", colour="D, a note its part sings (rust)",
        base=g.pc_rgb(2),
        front=R((8, 8, 52, 19), (8, 19, 36, 27)), back=R((10, 4, 58, 22)),
        slotmap={1: 9, 2: 9, 3: 10}, ramp="cols",
        cols={9: (225, 150, 95), 10: (170, 85, 40)}),
    "LIVELOCK": dict(
        why="PREEMPT line, stage 2 (ROUTE 22 on; 17 trainers, the fighters'): 8.6% waits",
        region="the TRUNKS, a boxer's violet", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((14, 44, 48, 55)), back=R((14, 34, 50, 47)),
        #  the gloves' middle red folded into the bright one (a two-tone glove); one violet, the dark stays
        slotmap={2: 9, 3: 9}, merge={9: 8}, ramp="cols",
        cols={9: (125, 85, 200)}),
    "OUTBREAK": dict(
        why="WORM line, stage 2 (ROCKET's staple: 15 trainers): 1.7% waits",
        region="the HOOD: its flaps and the crown's bands, a plum marking", colour="C, a note its part sings, moved to plum",
        base=(150, 70, 150),
        front=R((2, 24, 16, 52), (48, 24, 62, 52), (18, 0, 46, 12)), back=R((12, 4, 32, 28)),
        slotmap={2: 10, 3: 10}, ramp="cols", cols={10: (150, 70, 150)}),
    "QUORUM": dict(
        why="SENTINEL line, stage 2 (the POWER PLANT's; 10 trainers): 0.0% waits, no accent at all",
        region="the three EYES' irises in front, the spheres' shadowed sides behind, in brass",
        colour="D#, a note its part sings, moved to brass",
        #  D#'s own amber sits within 80 of SENTINEL's pinks, which QUORUM lost: CARRIED. Brighter brass escapes.
        base=(195, 150, 40),
        front=R((25, 9, 39, 24), (13, 30, 29, 45), (35, 30, 51, 45)), back=R((0, 0, 63, 63)),
        #  the light brass drawn in front too (the iris's inner ring): a slot only the back draws is never greyed
        slotmap={3: 6, 4: 7}, slotmap_back={3: 6, 4: 7}, ramp="cols",
        cols={6: (235, 200, 90), 7: (195, 150, 40)}),
    "BREAKER": dict(
        why="FUSE line, stage 2 (the POWER PLANT's; 14 trainers): 8.3% waits",
        region="the CAP of its shell, a charge's violet (a two-tone ball)", colour="A#, a note its part sings (violet)",
        base=(130, 90, 210),
        front=R((6, 2, 58, 15)), back=R((6, 6, 60, 18)),
        #  one violet, the dark teal lines (its cracks) kept over it: mapping only the mid tones left it blotched
        slotmap={1: 10, 2: 10, 3: 10}, ramp="cols", cols={10: (130, 90, 210)}),
    "BUSYWAIT": dict(
        why="LULL line, stage 2 (ROUTE 11; 11 trainers, the psychics'): 0.0% waits",
        region="the EARS and the dark FLANK down its side, a hypnotist's gold", colour="D, a note its part sings, moved to gold",
        base=g.pc_rgb(4),
        front=R((12, 8, 25, 54)), back=R((38, 8, 52, 54)),
        slotmap={3: 7, 4: 9}, ramp="cols",
        cols={7: (215, 175, 60), 9: (140, 100, 25)}),
    "ROOTKIT": dict(
        why="PAYLOAD line, stage 2 (MT. MOON's and the SAFARI ZONE's, 8 tables): 0.0% waits, no accent at all",
        region="the CAP, a toadstool's amber shading (its pale spots stay)",
        colour="D#, a note its part sings, moved to amber",
        #  not PAYLOAD's red (ROOTKIT lost it): a red-orange sits within 80 of it and is CARRIED
        base=(235, 150, 60),
        front=R((6, 12, 58, 32)), back=R((4, 8, 60, 33)),
        slotmap={2: 6, 3: 7}, ramp="cols",
        cols={6: (235, 150, 60), 7: (175, 110, 30)}),
    "INFERENCE": dict(
        why="HUNCH line, stage 2 (the rival's from SS ANNE to SILPH CO.; 17 trainers): 10.0% waits",
        region="the EARS (inside in front, the tips behind) and the TAIL's brush, gold", colour="E, a note its part sings (gold)",
        base=g.pc_rgb(4),
        front=R((13, 11, 22, 21), (34, 11, 42, 21)),
        back=R((20, 4, 28, 13), (36, 4, 44, 13), (22, 46, 38, 60)),
        #  the spoon's darkest red folded into the next (12 pixels) to free a slot
        slotmap={1: 9}, slotmap_back={1: 9, 2: 9, 3: 9}, merge={9: 8}, ramp="cols", cols={9: (215, 170, 60)}),
    "ENSEMBLE": dict(
        why="BOOTSTRAP line, stage 2 (the rival's and the CHAMPION's; 10 trainers): 9.5% waits",
        region="the two side HEADS, coconut brown", colour="D, a note its part sings, moved to coconut",
        #  BOOTSTRAP's yellows and oranges are lost: a gold or orange is CARRIED. A brown 80 off them escapes.
        base=(200, 160, 130),
        front=R((6, 1, 22, 15), (38, 1, 54, 15)), back=R((8, 1, 25, 15), (38, 1, 56, 15)),
        slotmap={1: 6, 2: 6, 3: 10, 4: 10}, merge={6: 7}, ramp="cols",
        cols={6: (200, 160, 130), 10: (130, 90, 55)}),
    "REBUTTAL": dict(
        why="PREMISE line, stage 2 (the FIGHTING DOJO's prize; 12 trainers): 1.2% waits",
        region="the GLOVES, a boxer's orange", colour="D, a note its part sings (orange)",
        base=g.pc_rgb(2),
        front=R((1, 24, 15, 42), (49, 24, 63, 42)), back=R((2, 30, 14, 44), (50, 24, 63, 42)),
        #  the two carried tans folded together (15 pixels) to free a slot
        slotmap={1: 7, 2: 7, 3: 10, 4: 10}, merge={7: 6}, ramp="cols",
        cols={7: (240, 160, 90), 10: (195, 95, 40)}),
}


#  STAGE 5 (the user, 2026-11-23: "T-604 stage 5"; DRAFT): fifteen more, by how often a player meets them -- the
#  ELITE FOUR's not yet done (LORELEI's CLOYSTER, SLOWBRO and JYNX; BRUNO's HITMONLEE), the trainer staples (NIDORINA,
#  DODRIO, NINETALES, KINGLER, NIDOKING, BEEDRILL, JIGGLYPUFF, URSARING), CERULEAN CAVE's WOBBUFFET, the CHAMPION
#  rematch's TYRANITAR and HITMONLEE's sibling HITMONTOP. TODAY is the engine after stage 4 (BASE5): no form here was
#  drawn by stages 1-4. Every colour is given exactly ("cols"), each checked against the carry rule by the report.
BASE5_COMMIT = "39093823d"
FORMS5 = {
    "THREAD": dict(
        why="FORK line, stage 2 (the SAFARI ZONE's; 8 trainers): 3.6% waits",
        region="the long EARS, turning blue", colour="Ab, a note its part sings (blue)",
        base=g.pc_rgb(8),
        front=R((4, 11, 15, 38), (46, 9, 58, 42), (38, 8, 46, 12)), back=R((8, 12, 24, 30), (41, 8, 58, 30)),
        #  the eye's 3-pixel sparkle folded into its green to free a slot
        #  behind, the outer face only: the ears' insides already wait (their green and grey)
        slotmap={1: 10, 2: 10, 3: 6}, slotmap_back={1: 10, 2: 10}, merge={6: 7}, ramp="cols",
        #  the light kept saturated: a paler blue sits nearest FORK's grey-blue (161,164,186), CARRIED
        cols={10: (125, 155, 240), 6: (64, 95, 175)}),
    "AXIOMKICK": dict(
        why="PREMISE line, stage 2 (BRUNO's, both fights; the FIGHTING DOJO's and the CRUSH girls'): 1.5% waits",
        region="the kicking LEG and the FEET, a fighter's orange wraps", colour="D, a note its part sings (orange)",
        base=g.pc_rgb(2),
        front=R((44, 8, 62, 20), (48, 20, 62, 40), (16, 46, 40, 58)), back=R((14, 46, 50, 58), (2, 32, 16, 48), (48, 32, 62, 48)),
        slotmap={1: 9, 2: 9, 3: 10, 4: 10}, ramp="cols",
        cols={9: (235, 150, 85), 10: (180, 85, 35)}),
    "SHELL": dict(
        why="LATENCY line, stage 2 (LORELEI's, both fights; 9 trainers): 1.4% waits",
        region="the SHELL on its tail: its pale whorls turn violet, the blue ones stay", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        #  the shell's edge in front follows its whorl (a circle round (44,31)): above it, the head runs into the shell
        front=R((38, 12, 60, 12), (36, 13, 60, 13), (34, 14, 60, 14), (32, 15, 60, 15), (31, 16, 60, 16), (30, 17, 60, 17), (29, 18, 60, 18), (28, 19, 60, 20), (27, 21, 60, 22), (26, 23, 60, 24), (25, 25, 60, 30), (24, 31, 60, 31), (25, 32, 60, 37), (26, 38, 60, 39), (27, 40, 60, 41), (28, 42, 60, 43), (29, 44, 60, 44)),
        back=R((16, 10, 60, 42)),
        slotmap={1: 10, 2: 9}, ramp="cols",
        cols={10: (180, 140, 225), 9: (130, 95, 195)}),
    "COLDVAULT": dict(
        why="CAPSULE line, stage 2 (LORELEI's ace; 9 trainers, the swimmers'): 4.6% waits",
        region="the SHELL's outer plates, a violet clam's", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((0, 2, 63, 27), (0, 27, 15, 47), (49, 27, 63, 47)), back=R((0, 2, 63, 27), (0, 27, 15, 47), (49, 27, 63, 47)),
        slotmap={3: 7, 4: 9}, ramp="cols",
        #  the dark kept 40 off the body's navy (36,55,91), which it would otherwise be, and so CARRIED
        cols={7: (120, 85, 190), 9: (75, 30, 120)}),
    "TRIPLECORE": dict(
        why="DUAL line, stage 2 (the BIRD KEEPERS' staple, 8 trainers): 0.0% waits, every colour carried",
        region="the three BODIES' shaded plumage, a brown bird's", colour="D, a note its part sings (brown)",
        base=(195, 145, 85),
        front=R((0, 22, 63, 48)), back=R((8, 26, 58, 50)),
        #  the back's 5-pixel blue folded into its other blue to free a slot
        slotmap={3: 10, 4: 8}, slotmap_back={2: 10, 3: 10, 4: 8}, merge={8: 6}, ramp="cols",
        cols={10: (195, 145, 85), 8: (130, 85, 40)}),
    "OVERRUN": dict(
        why="FLICKER line, stage 2 (8 trainers: burglars, cooltrainers): 1.9% waits",
        region="the TAIL, a foxfire violet", colour="B, a note its part sings (violet)",
        base=g.pc_rgb(11),
        front=R((38, 20, 58, 54), (50, 14, 58, 20)), back=R((36, 18, 62, 46)),
        slotmap={1: 9, 2: 9, 3: 10}, ramp="cols",
        cols={9: (190, 150, 230), 10: (130, 80, 190)}),
    "SUSPEND": dict(
        why="STANDBY line, stage 2 (ROUTE 3's; 5 trainers): 3.1% waits",
        region="the CURL, the crown of its head and its FEET, a balloon's pink", colour="C, a note its part sings (pink)",
        base=(253, 161, 179),
        front=R((8, 4, 34, 15), (10, 15, 54, 21), (8, 45, 56, 56)), back=R((14, 8, 50, 22), (22, 47, 54, 56)),
        #  the cheeks' own pink (8) and its dark (9) are the ramp's middle and dark: one new slot, the light
        slotmap={1: 10, 2: 8, 3: 9}, ramp="cols",
        cols={10: (255, 185, 205)}),
    "INJECTOR": dict(
        why="SCRAPER line, stage 3 (the BUG CATCHERS' staple; 6 trainers): 8.8% waits",
        region="the ABDOMEN, a wasp's gold bands", colour="E, a note its part sings (gold)",
        base=g.pc_rgb(4),
        front=R((14, 36, 44, 58)), back=R((29, 30, 45, 48), (31, 26, 41, 30)),
        #  the darkest navy folded into the next (34 pixels) to free a slot; one gold, the carried olive darks shade it
        slotmap={1: 10, 2: 10}, slotmap_back={1: 10, 2: 10, 3: 10}, merge={10: 9}, ramp="cols",
        cols={10: (215, 180, 60)}),
    "CRAVING": dict(
        why="COMFORT line, stage 2 (the TAMERS'; SIX ISLAND's WATER PATH): 0.8% waits",
        region="the RING on its chest and the disc inside it, gold, and its PAWS, honey-dipped",
        colour="E, a note its part sings (gold)",
        base=g.pc_rgb(4),
        front=R((17, 26, 41, 46), (18, 48, 32, 56), (36, 48, 50, 56)), back=R((17, 26, 41, 46), (18, 48, 32, 56), (36, 48, 50, 56)),
        slotmap={1: 9, 3: 10, 4: 10}, ramp="cols",
        cols={9: (235, 205, 110), 10: (160, 120, 30)}),
    "LOCKUP": dict(
        why="ACQUIRE line, stage 2 (5 trainers, the swimmers' and cooltrainers'): 1.8% waits",
        region="the PINCERS, a crab's coral", colour="C#, a note its part sings, moved to coral",
        #  not C#'s own: an orange sits nearer ACQUIRE's tan (192,151,72) than the colour that carries it, CARRIED
        base=(235, 90, 80),
        front=R((14, 4, 28, 19), (36, 4, 52, 19), (4, 24, 15, 39), (48, 24, 60, 39)),
        back=R((8, 6, 23, 30), (8, 30, 18, 42), (42, 16, 60, 30), (50, 30, 60, 40)),
        #  its own rust cheek (7) is the dark: one new slot
        slotmap={1: 10, 2: 10, 3: 7, 4: 7}, ramp="cols",
        cols={10: (235, 90, 80)}),
    "RESENTMENT": dict(
        why="RANK line, stage 2 (CERULEAN CAVE, three floors; SIX ISLAND's RUIN VALLEY): 0.0% waits, no accent at all",
        region="the dome's RIM and its spots, turning blue", colour="G, a note its part sings (blue)",
        base=g.pc_rgb(7),
        front=R((0, 0, 63, 44)), back=R((0, 0, 63, 44)),
        slotmap={3: 7, 4: 8}, ramp="cols",
        cols={7: (80, 110, 200), 8: (40, 55, 125)}),
    "PIPELINE": dict(
        why="BRANCH line, stage 3 (4 trainers, the cooltrainers'): 1.2% waits; STRATUM is the new type",
        region="the HORN's tip and the EARS in front, the HORN and BACK PLATES behind, in STRATUM", colour="STRATUM, the new type",
        base=TYPE["STRATUM"],
        front=R((23, 2, 33, 9), (14, 8, 22, 22), (43, 8, 60, 18)), back=R((32, 2, 56, 22), (40, 22, 58, 32), (20, 12, 40, 22)),
        #  the eyes' two browns folded together (11 pixels) to free a slot
        slotmap={1: 7, 2: 7, 3: 10, 4: 9}, merge={9: 8}, ramp="cols",
        #  the light browner than STRATUM's own: a pinker one sits nearest PREDICTOR's rose (255,134,141), CARRIED
        cols={7: (185, 165, 105), 10: (158, 122, 78), 9: (96, 56, 28)}),
    "GRIEVANCE": dict(
        why="RUMINATE line, stage 3 (the CHAMPION rematch's, every starter; MT. EMBER's RUBY PATH): 0.0% waits",
        region="the HEAD's armour, crest to jaw, a mountain's green", colour="F, a note its part sings (green)",
        base=g.pc_rgb(5),
        front=R((10, 2, 52, 31)), back=R((10, 2, 52, 31)),
        #  the light kept yellower, a bluer one sits nearest PUPITAR's teal
        #  (110,165,176), CARRIED
        slotmap={1: 9, 2: 9, 3: 10}, ramp="cols",
        cols={9: (150, 210, 110), 10: (63, 154, 85)}),
    "COLDREAD": dict(
        why="TELLTALE line, stage 2 (LORELEI's, both fights): 1.0% waits",
        region="the WINGS and the FACIAL DISCS (behind, the crown), a twilight violet", colour="B, a note its part sings (violet)",
        base=g.pc_rgb(11),
        front=R((2, 24, 17, 58), (47, 24, 62, 58), (4, 0, 60, 27)),
        back=R((4, 24, 26, 50), (16, 2, 52, 22)),
        #  one violet, the carried ice-blue darks shading it
        slotmap={1: 10, 2: 10}, ramp="cols",
        cols={10: (150, 110, 210)}),
    "CIRCULAR": dict(
        why="PREMISE line, stage 2 (the CRUSH girls'; SEVAULT CANYON): 1.7% waits",
        region="the raised LEGS, spun violet", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((16, 6, 46, 34)), back=R((16, 6, 46, 34)),
        slotmap={1: 7, 2: 9, 3: 10}, ramp="cols",
        cols={7: (175, 140, 230), 9: (120, 85, 195), 10: (70, 45, 125)}),
}


#  STAGE 6 (the user, 2026-11-23: "T-604 stage 6"; DRAFT): fifteen more, by how often a player meets them -- the
#  ELITE FOUR rematch's not yet done (LORELEI's PILOSWINE, AGATHA's CROBAT, LANCE's KINGDRA), the ROCKET ADMIN's
#  HOUNDOOM, Kanto's own wild later forms (DIGLETT'S CAVE's DUGTRIO, the POWER PLANT's ELECTABUZZ, ROUTE 11's VIGOROTH),
#  the trainer staples (WIGGLYTUFF, LANTURN, FLAAFFY, CLEFABLE, POLIWRATH, GOLEM, XATU) and MT. EMBER's DONPHAN.
#  TODAY is the engine after stage 5 (BASE6): no form here was drawn by stages 1-5. Every colour is given exactly
#  ("cols"), each checked against the carry rule by the report: none may read CARRIED.
BASE6_COMMIT = "ac21d422e"
FORMS6 = {
    "TURBULENCE": dict(
        why="BOTTLENECK line, stage 3 (LANCE's rematch ace; TANOBY's water, 30%): 0.0% waits",
        region="the curled TAIL, a deep-sea violet", colour="Bb, a note its part sings (violet)",
        #  not EMERGENT's jade: BACKPRESS's lost greens (63,154,85) would CARRY it from 40
        base=g.pc_rgb(10),
        front=R((29, 33, 54, 55)), back=R((8, 40, 40, 58)),
        slotmap={1: 7, 2: 9, 3: 9, 4: 10}, ramp="cols",
        cols={7: (185, 140, 230), 9: (120, 90, 190), 10: (80, 30, 120)}),
    "IMPULSE": dict(
        why="INSTINCT line, stage 2 (LORELEI's rematch; ICEFALL CAVE, 10%): 0.1% waits; STRATUM is the new type",
        region="the shaggy MANE over its head and back, in STRATUM", colour="STRATUM, the new type",
        base=TYPE["STRATUM"],
        front=R((14, 4, 58, 17), (2, 14, 16, 28)), back=R((16, 4, 50, 30)),
        slotmap={1: 8, 2: 8, 3: 9, 4: 10}, slotmap_back={2: 8, 3: 9, 4: 10}, ramp="cols",
        cols={8: (210, 180, 125), 9: (155, 125, 75), 10: (96, 70, 40)}),
    "MULTICAST": dict(
        why="ECHO line, stage 3 (AGATHA's rematch): 0.0% waits",
        region="the upper pair of WINGS, a night blue", colour="G, a note its part sings (blue)",
        base=g.pc_rgb(7),
        front=R((0, 8, 17, 30), (47, 8, 63, 30), (0, 30, 12, 54), (52, 30, 63, 54)), back=R((0, 8, 17, 30), (47, 8, 63, 30), (0, 30, 12, 54), (52, 30, 63, 54)),
        slotmap={3: 6, 4: 10}, merge={6: 1}, ramp="cols",
        cols={6: (60, 110, 185), 10: (30, 55, 110)}),
    "OBSESSION": dict(
        why="FIXATION line, stage 2 (the ROCKET ADMIN's, SEVII): 4.8% waits",
        region="the MUZZLE and CHEST, an ember's amber", colour="D, a note its part sings (an ember amber, vanilla's tan moved off FIXATION's)",
        #  kept 83 off FIXATION's lost tan (220,172,106), which the horns' brown carries from 71
        base=(215, 120, 30),
        front=R((0, 0, 63, 50)), back=R((0, 0, 63, 32), (48, 30, 63, 52)),
        slotmap={1: 8, 2: 9}, ramp="cols",
        cols={8: (255, 205, 30), 9: (215, 120, 30)}),
    "SOUNDING": dict(
        why="PILOT line, stage 2 (a swimmer's; ICEFALL CAVE's water, 30%): 5.2% waits; SIGNAL is the new type",
        region="the LANTERN and the TAIL fin, lit in SIGNAL", colour="SIGNAL, the new type",
        base=TYPE["SIGNAL"],
        front=R((2, 25, 15, 41), (48, 38, 63, 52)), back=R((52, 25, 63, 41), (0, 38, 16, 52)),
        slotmap={1: 6, 2: 6, 3: 8, 4: 8}, merge={6: 7, 8: 7}, ramp="cols",
        cols={6: (130, 225, 210), 8: (40, 140, 140)}),
    "HIBERNATE": dict(
        why="STANDBY line, stage 3 (two BEAUTIES'): 0.0% waits",
        region="the long lop EARS and the PAWS (a colourpoint), a twilight lilac", colour="B, a note its part sings (lilac)",
        base=g.pc_rgb(11),
        front=R((4, 12, 19, 35), (44, 12, 60, 35), (16, 31, 48, 39)), back=R((8, 14, 23, 50), (41, 14, 56, 50)),
        slotmap={1: 8, 2: 8, 3: 9, 4: 10}, slotmap_back={2: 8, 3: 9, 4: 10}, ramp="cols",
        cols={8: (200, 170, 235), 9: (150, 110, 205), 10: (90, 60, 150)}),
    "BUILDUP": dict(
        why="TENSION line, stage 2 (a LADY's; SIX ISLAND's WATER PATH): 2.2% waits",
        region="the WOOL on its head and the TAIL's ball, charged gold", colour="Eb, a note its part sings (gold)",
        base=g.pc_rgb(3),
        front=R((3, 5, 40, 12), (3, 12, 24, 17), (34, 12, 40, 17), (44, 22, 58, 34)), back=R((24, 5, 61, 12), (39, 12, 61, 17), (23, 12, 29, 17), (5, 22, 19, 34)),
        slotmap={1: 8, 2: 10, 3: 10}, ramp="cols",
        cols={8: (250, 215, 110), 10: (215, 160, 50)}),
    "RESTLESS": dict(
        why="DAYDREAM line, stage 2 (ROUTE 11's grove; FIVE ISLAND's MEADOW): 0.0% waits, no accent at all",
        region="the CROWN of its head and the RUFF round its face, a restless orange", colour="D, a note its part sings (orange)",
        base=g.pc_rgb(2),
        front=R((20, 3, 46, 13), (24, 18, 44, 23)), back=R((20, 3, 46, 19)),
        slotmap={1: 6, 2: 6, 3: 7, 4: 8}, ramp="cols",
        cols={6: (245, 175, 115), 7: (210, 115, 50), 8: (130, 65, 25)}),
    "WIRETAP": dict(
        why="TAPPOINT line, stage 2 (DIGLETT'S CAVE): 8.2% waits",
        region="the FUR on the crowns of its heads, a clay terracotta", colour="C#, a note its part sings (terracotta)",
        base=g.pc_rgb(1),
        #  the pinks folded together to free two slots: 7 into 6 (9 pixels), 9 into 8 (16 pixels)
        front=R((26, 8, 42, 13), (20, 12, 46, 16)), back=R((10, 18, 62, 29)),
        slotmap={2: 7, 3: 9, 4: 9}, slotmap_back={1: 7, 3: 7, 4: 9}, merge={7: 6, 9: 8}, ramp="cols",
        #  the dark kept 75 off TAPPOINT's lost wine (125,14,37), which the body's dark carries from 65
        cols={7: (195, 100, 55), 9: (160, 75, 40)}),
    "DYNAMO": dict(
        why="CRANK line, stage 2 (the POWER PLANT): 2.1% waits",
        region="the BELLY and the head's DOME, a cold blue charge", colour="Ab, a note its part sings (blue)",
        base=g.pc_rgb(8),
        front=R((20, 38, 44, 52), (18, 10, 46, 20)), back=R((24, 16, 46, 30), (24, 34, 44, 52)),
        slotmap={1: 10}, ramp="cols",
        cols={10: (140, 165, 240)}),
    "OUTLIER": dict(
        why="RESIDUAL line, stage 3 (a BREEDER's): 0.0% waits, no accent at all",
        region="the great EYE's iris in front, the HEM behind, violet", colour="B, a note its part sings (violet)",
        base=g.pc_rgb(11),
        front=R((18, 15, 41, 36), (4, 46, 60, 58)),
        back=R((4, 40, 60, 58)),
        slotmap={3: 6, 4: 7}, slotmap_back={2: 6, 3: 7, 4: 7}, ramp="cols",
        cols={6: (138, 76, 174), 7: (95, 30, 95)}),
    "MUTEX": dict(
        why="LOOP line, stage 3 (a SWIMMER's): 0.0% waits; LOGIC is the new type, but its steel sits on the body's blue",
        region="a boxer's TRUNKS, violet", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((18, 36, 46, 48)), back=R((20, 40, 48, 56)),
        slotmap={1: 7, 2: 7, 3: 10, 4: 10}, merge={7: 6}, ramp="cols",
        cols={7: (170, 140, 225), 10: (75, 30, 115)}),
    "MONOLITH": dict(
        why="HEAP line, stage 3 (a RUIN MANIAC's): 6.0% waits; the cyan underside behind now shows in front too",
        region="the BOWL of its underside, in front as behind", colour="G, the note its underside already sings (cyan)",
        base=(64, 178, 186),
        front=R((6, 40, 58, 60)), back=R((0, 0, 0, 0)),
        slotmap={2: 7, 3: 8, 4: 8}, ramp="cols",
        cols={}),
    "PRESCIENCE": dict(
        why="VIGILANCE line, stage 2 (a PSYCHIC's): 1.6% waits; VECTOR is the new type",
        region="the WING's flight feathers, in a soft VECTOR", colour="VECTOR, the new type, moved to coral",
        base=(225, 85, 95),
        front=R((36, 30, 58, 50)), back=R((6, 30, 28, 50)),
        slotmap={2: 7, 3: 10}, merge={7: 8}, ramp="cols",
        cols={7: (245, 150, 150), 10: (225, 85, 95)}),
    "ENGRAM": dict(
        why="RECALL line, stage 2 (MT. EMBER's RUBY PATH, 20%): 9.5% waits",
        region="the great EARS' inner faces, a remembered gold", colour="E, a note its part sings (gold)",
        base=g.pc_rgb(4),
        front=R((2, 6, 13, 32), (37, 6, 54, 34)), back=R((10, 6, 27, 34), (50, 6, 62, 32)),
        slotmap={2: 10, 3: 10}, ramp="cols",
        cols={10: (207, 174, 52)}),
}


#  STAGE 7 (the user, 2026-11-23: "T-604 stage 7"; DRAFT): fifteen more, by how often a player meets them. No trainer
#  fields any of the later forms still under 10%, so it goes by the wild: first the SEVII ISLANDS a player reaches before
#  the ELITE FOUR (ONE ISLAND's TREASURE BEACH and its water, THREE ISLAND's BERRY FOREST, MT. EMBER's SUMMIT PATH and
#  RUBY PATH), then the post-game's commonest tables (the surf at 30% on SIX ISLAND's WATER PATH, GREEN PATH and OUTCAST
#  ISLAND, the WATER PATH's grass at 20%, SEVEN ISLAND's grove at 15%). TODAY is the engine after stage 6 (BASE7): no
#  form here was drawn by stages 1-6. Every colour is given exactly ("cols"), each checked against the carry rule by the
#  report: none may read CARRIED.
BASE7_COMMIT = "e2d65ea7d"
FORMS7 = {
    "SEMAPHORE": dict(
        why="SPINLOCK line, stage 3 (ONE ISLAND's TREASURE BEACH, surfing 30% in both editions): 8.2% waits",
        region="the BELLY, a frog's pale gold", colour="Eb, a note its part sings (pale gold)",
        base=g.pc_rgb(3),
        front=R((21, 42, 38, 54)), back=R((25, 42, 42, 54)),
        #  the flag's 3-pixel coral folded into its red, the feet's light lime (6 pixels) into the bright one, to free two slots
        slotmap={1: 7}, merge={7: 6, 8: 10}, ramp="cols",
        cols={7: (245, 228, 140)}),
    "KERNEL": dict(
        why="LATENCY line, stage 2 (ONE ISLAND's water, surfing 30% in CONTEXT): 7.8% waits",
        region="the ROBE below its head and the curled TAIL, a king's rose", colour="C, a note its part sings (rose)",
        base=(215, 110, 135),
        front=R((19, 44, 53, 54)), back=R((10, 44, 44, 54)),
        slotmap={1: 9, 2: 10}, ramp="cols",
        cols={9: (245, 170, 185), 10: (215, 110, 135)}),
    "POLICY": dict(
        why="SHAPING line, stage 3 (THREE ISLAND's BERRY FOREST, 10% and 20%): 7.6% waits",
        region="the far half of the TAIL's great crescent, an autumn rose", colour="C, a note its part sings (rose)",
        base=(235, 150, 180),
        front=R((44, 2, 63, 9), (42, 10, 63, 31)), back=R((0, 2, 19, 9), (0, 10, 21, 31)),
        #  the leaf-fans' darkest brown (25 pixels) folded into the next to free a slot
        slotmap={2: 9}, merge={9: 8}, ramp="cols",
        cols={9: (235, 150, 180)}),
    "CANOPY": dict(
        why="BOOSTING line, stage 3 (THREE ISLAND's BERRY FOREST, 10% in both): 4.9% waits",
        region="the CANOPY's leaves, in blossom", colour="C, a note its part sings (blossom pink)",
        base=(240, 150, 210),
        front=R((4, 0, 59, 38)), back=R((4, 0, 59, 38)),
        #  kept 86 off BOOSTING's lost cream (223,186,134): a paler pink would be the nearest to it, and CARRIED
        slotmap={2: 10}, ramp="cols",
        cols={10: (240, 150, 210)}),
    "LASVEGAS": dict(
        why="COINFLIP line, stage 3 (MT. EMBER's SUMMIT PATH, 10% in both): 0.2% waits",
        region="the WINGS, a neon violet", colour="Bb and B, notes its part sings (lilac into violet)",
        base=g.pc_rgb(11),
        front=R((40, 17, 58, 36), (5, 32, 20, 46)), back=R((5, 17, 22, 33), (42, 17, 61, 30)),
        slotmap={2: 8, 3: 9, 4: 10}, ramp="cols",
        cols={8: (175, 150, 235), 9: (138, 76, 174), 10: (80, 35, 110)}),
    "MONTECARLO": dict(
        why="COINFLIP line, stage 2 (MT. EMBER's SUMMIT PATH, 10% in both): 0.0% waits, no accent at all",
        region="the WINGS, the FEET and the crest's tuft, an ember", colour="C#, a note its part sings (ember)",
        base=g.pc_rgb(1),
        front=R((11, 31, 27, 47), (40, 32, 55, 47), (20, 53, 40, 59), (28, 3, 42, 8)), back=R((11, 31, 26, 50), (43, 32, 54, 43), (18, 53, 40, 59), (19, 3, 41, 6)),
        slotmap={2: 6, 3: 7}, ramp="cols",
        cols={6: (240, 130, 80), 7: (185, 80, 35)}),
    "CALLOUS": dict(
        why="SIMMER line, stage 2 (MT. EMBER's RUBY PATH, ROCK SMASH 10% in both): 0.6% waits",
        region="the SHELL's grooves, glowing like magma", colour="C#, a note its part sings (ember)",
        base=g.pc_rgb(1),
        front=R((10, 8, 56, 32), (10, 32, 30, 42)), back=R((34, 9, 58, 44)),
        #  the shell's 3-pixel lilac glint folded into the cream to free a slot
        slotmap={3: 6, 4: 9}, merge={6: 1}, ramp="cols",
        cols={6: (230, 120, 70), 9: (160, 60, 30)}),
    "SHIMMER": dict(
        why="SINKHOLE line, stage 2 (MT. EMBER's RUBY PATH, 20% in CONTENT): 5.4% waits",
        region="the WINGS' lower panels, iridescent periwinkle", colour="A, a note its part sings (periwinkle)",
        base=(120, 125, 215),
        front=R((7, 11, 23, 34), (34, 11, 52, 34)), back=R((11, 11, 30, 33), (41, 11, 57, 33)),
        slotmap={2: 10}, ramp="cols",
        cols={10: (120, 125, 215)}),
    "THENCASE": dict(
        why="IFTRUE line, stage 3 (ONE ISLAND's grove, 8% in both): 0.7% waits",
        region="the upper WINGS, violet", colour="B, a note its part sings (violet)",
        base=(160, 110, 225),
        #  behind, the wings run into the body without a line: the rectangles follow where the wing's outline would be
        front=R((5, 15, 23, 36), (38, 15, 58, 36)), back=R((5, 15, 24, 25), (5, 26, 20, 36), (40, 15, 58, 25), (44, 26, 58, 36)),
        #  the 3-pixel peach folded into the orange beside it to free a slot
        slotmap={1: 6}, merge={6: 7}, ramp="cols",
        #  kept 87 off IFTRUE's lost pink (228,152,191): a paler violet would be the nearest to it, and CARRIED
        cols={6: (160, 110, 225)}),
    "BLOATWARE": dict(
        why="GREEDY line, stage 2 (THREE ISLAND's BERRY FOREST grove, 15% in both): 0.0% waits, no accent at all",
        region="the DOME of its head and its flanks, a bloated violet", colour="G, the note nearest violet its part sings",
        base=(107, 75, 174),
        front=R((12, 4, 52, 13), (8, 14, 19, 27), (45, 14, 56, 27)), back=R((12, 4, 52, 15), (8, 16, 17, 19), (46, 16, 56, 19), (6, 20, 13, 26), (50, 20, 58, 26)),
        slotmap={1: 6, 2: 7, 3: 8}, ramp="cols",
        cols={6: (160, 130, 215), 7: (107, 75, 174), 8: (60, 35, 105)}),
    "PERMAFROST": dict(
        why="STOPGRAD line, stage 2 (SIX ISLAND's WATER PATH, surfing 30% in both): 3.5% waits",
        region="the WOOL on its crown, a mammoth's gold and russet", colour="E and D, notes its part sings (gold into russet)",
        base=g.pc_rgb(2),
        front=R((19, 2, 45, 13)), back=R((18, 2, 44, 13)),
        slotmap={1: 8, 2: 9, 3: 9, 4: 10}, ramp="cols",
        cols={8: (230, 200, 120), 9: (170, 105, 55), 10: (100, 60, 35)}),
    "RIPTIDE": dict(
        why="UNDERTOW line, stage 2 (SIX ISLAND's GREEN PATH, surfing 30% in both): 5.9% waits",
        region="the FINS, violet, and the BELLY, lilac", colour="Bb, a note its part sings (violet)",
        base=g.pc_rgb(10),
        front=R((19, 14, 31, 25), (29, 44, 38, 49), (8, 39, 40, 44)), back=R((32, 14, 44, 25), (24, 44, 34, 49), (24, 39, 55, 45)),
        #  the 8-pixel plum folded into the violet beside it to free a slot; the fins take the form's own waiting violet
        slotmap={4: 7, 1: 8, 3: 8}, merge={8: 7}, ramp="cols",
        cols={8: (190, 165, 230)}),
    "ARCFLASH": dict(
        why="CRACKLE line, stage 2 (SIX ISLAND's WATER PATH, 20% and 10%): 0.3% waits",
        region="the crest of SPIKES on its head and the MANE down its back, an arc's violet", colour="B, a note its part sings (violet)",
        base=g.pc_rgb(11),
        front=R((7, 3, 35, 13), (35, 17, 58, 33), (48, 26, 58, 45)), back=R((28, 3, 56, 13), (5, 17, 28, 33), (5, 26, 15, 45)),
        #  the 5-pixel grey folded into the pale cyan to free a slot
        slotmap={2: 7, 3: 7, 4: 10}, merge={7: 2}, ramp="cols",
        cols={7: (200, 150, 240), 10: (138, 76, 174)}),
    "POSTERIOR": dict(
        why="LIKELIHOOD line, stage 2 (SEVEN ISLAND's grove, 15% in both): 0.9% waits",
        region="the CAP on its head and the knobs of its shoulders, fired terracotta", colour="C# and D, notes its part sings (terracotta, its light a clay orange)",
        base=g.pc_rgb(1),
        front=R((25, 4, 42, 17), (8, 26, 14, 29), (50, 26, 57, 29)), back=R((22, 4, 39, 17), (6, 26, 13, 29), (49, 26, 56, 29)),
        #  the eyes' single-pixel cyan folded into the next
        slotmap={1: 6, 2: 8, 3: 8, 4: 10}, merge={6: 7}, ramp="cols",
        cols={6: (240, 175, 135), 8: (200, 105, 65), 10: (125, 55, 30)}),
    "OPTIMUM": dict(
        why="SADDLE line, stage 2 (SIX ISLAND's OUTCAST ISLAND, surfing 30% in both): 5.2% waits",
        region="the FEELERS and the CREST over its head, and the TAIL's curled end, a rose", colour="C, a note its part sings (rose)",
        base=(180, 75, 130),
        front=R((8, 2, 56, 9), (4, 42, 24, 58)), back=R((8, 2, 56, 9), (35, 42, 59, 58)),
        #  the 9-pixel light tan folded into the next
        slotmap={1: 6, 3: 6, 4: 10}, merge={6: 7}, ramp="cols",
        cols={6: (240, 140, 165), 10: (180, 75, 130)}),
}


#  STAGE 8 (the user, 2026-11-23: "T-604 stage 8"; DRAFT): fifteen more, by how often a player meets them. No trainer
#  fields any of the later forms still under 10%, so it goes by the wild, the highest share of any one table in either
#  edition: the surf at 30% (SEVEN ISLAND's TRAINER TOWER, FOUR ISLAND's ICEFALL CAVE), then 20% (THREE ISLAND's BERRY
#  FOREST, FIVE ISLAND's MEADOW, SIX ISLAND's PATTERN BUSH), 15% (the FOUR and FIVE ISLAND groves), and of the 10%s those
#  met in both editions or on more than one table, then MT. EMBER's (reached before the ELITE FOUR). Skipped: STEEPEST,
#  the cocoons (IFTRUE, IFFALSE, PENDING, BUFFER, and BROODING, a chrysalis), and any MUSAI, PENPHIN or UNOWN form. TODAY is
#  the engine after stage 7 (BASE8): no form here was drawn by stages 1-7. Every colour is given exactly ("cols"), each
#  checked against the carry rule by the report: none may read CARRIED.
BASE8_COMMIT = "cedc8d360"
FORMS8 = {
    "ELATION": dict(
        why="VALENCE line, stage 3 (SEVEN ISLAND's TRAINER TOWER, surfing 30% in CONTENT): 0.0% waits, every colour carried",
        region="the round LOWER BODY, lifted into lilac", colour="Bb, a note its part sings (lilac into violet)",
        base=g.pc_rgb(10),
        front=R((18, 38, 48, 58)), back=R((15, 38, 45, 58)),
        slotmap={1: 9, 2: 10}, ramp="cols",
        cols={9: (180, 150, 235), 10: (120, 85, 195)}),
    "DELTA": dict(
        why="RUNOFF line, stage 3 (FOUR ISLAND's ICEFALL CAVE, surfing 30% in CONTENT): 0.0% waits, every colour carried",
        region="the spiked GILLS at its cheeks, and the cheek below the eye, a river-mouth orange",
        colour="Eb and C, notes its part sings (amber into rust)", base=g.pc_rgb(3),
        front=R((42, 12, 60, 36), (4, 28, 22, 34)), back=R((2, 12, 18, 34), (46, 12, 62, 34)),
        slotmap={1: 8, 2: 9, 3: 10}, merge={7: 6}, ramp="cols",
        cols={8: (250, 205, 140), 9: (235, 140, 60), 10: (190, 75, 40)}),
    "SHAPING": dict(
        why="WARMUP line, stage 2 (SIX ISLAND's PATTERN BUSH, 20% in CONTEXT, 10% in CONTENT): 2.6% waits",
        region="the great LEAF it carries and the tuft of its crown, turning gold", colour="E and D, notes its part sings (gold into amber)",
        base=g.pc_rgb(4),
        front=R((40, 22, 58, 48), (12, 2, 34, 12)), back=R((6, 22, 24, 48), (30, 2, 52, 12)),
        #  the leaf-pod's two oranges (8 pixels) and its two reds (8) each folded into one, to free two slots
        slotmap={2: 7, 3: 8, 4: 8}, merge={7: 6, 8: 9}, ramp="cols",
        #  the amber kept 95 off WARMUP's lost rose-brown (176,130,116): any nearer and it would be CARRIED
        cols={7: (230, 205, 95), 8: (215, 135, 30)}),
    "DEFUNCT": dict(
        why="PREFORK line, stage 2 (THREE ISLAND's BERRY FOREST, 20% in CONTEXT): 0.3% waits; LATENT is the new type",
        region="the WINGS' panes, in LATENT", colour="LATENT, the new type (lilac, its veins plum): A and B",
        base=(150, 125, 215),
        front=R((6, 14, 22, 36), (44, 14, 60, 36)), back=R((6, 14, 22, 36), (44, 14, 60, 36)),
        slotmap={1: 8, 3: 9}, ramp="cols",
        cols={8: (150, 125, 215), 9: (95, 55, 135)}),
    "QUINE": dict(
        why="LOOPBACK line, stage 2 (FIVE ISLAND's MEADOW, 20% in CONTENT): 2.2% waits",
        region="the CROWN of its head with the ears, the TAIL and the PAWS, lavender", colour="B and A, notes its part sings (lavender into violet)",
        base=g.pc_rgb(11),
        front=R((8, 4, 38, 14), (40, 18, 63, 40), (10, 52, 50, 59)), back=R((26, 4, 56, 14), (0, 18, 24, 40), (14, 52, 54, 59)),
        slotmap={1: 6, 2: 10, 3: 10}, merge={6: 7}, ramp="cols",
        cols={6: (205, 180, 235), 10: (130, 120, 205)}),
    "ZEROSHOT": dict(
        why="FEWSHOT line, stage 2 (SIX ISLAND's PATTERN BUSH, 20% in CONTENT; BERRY FOREST, 10% in CONTEXT): 3.3% waits",
        region="the SPINES of its crown and along its tail, in bloom", colour="C and Bb, notes its part sings (blossom pink into violet)",
        base=(240, 150, 190),
        front=R((0, 0, 40, 15)), back=R((24, 0, 63, 15)),
        #  the spines' two lesser teals (13 and 7 pixels) folded into the bright one, to free two slots
        slotmap={1: 6, 2: 8, 3: 8}, merge={8: 7, 6: 7}, ramp="cols",
        extra=[dict(front=R((30, 28, 63, 46)), back=R((0, 28, 33, 46)), slotmap={3: 8, 4: 8})],
        cols={6: (240, 150, 190), 8: (150, 80, 175)}),
    "BURSTMODE": dict(
        why="PREFORK line, stage 2 (FOUR ISLAND's grove, 15% in both): 2.4% waits; VECTOR is the new type",
        region="the WINGS and the top SPEED LINE behind them, an afterburner", colour="E into VECTOR (C#), notes its part sings",
        base=TYPE["VECTOR"],
        front=R((6, 12, 24, 24), (38, 12, 56, 24), (0, 29, 21, 32), (43, 29, 63, 32)),
        back=R((6, 12, 24, 24), (38, 12, 56, 24), (0, 29, 21, 32), (43, 29, 63, 32)),
        slotmap={1: 7, 2: 10, 3: 10}, ramp="cols",
        cols={7: (245, 200, 80), 10: (210, 70, 50)}),
    "PAIRWISE": dict(
        why="SINGLETON line, stage 2 (FIVE ISLAND's MEADOW grove, 15% in both): 0.1% waits",
        region="the CLAWS it stands on, in CONTEXT", colour="CONTEXT, its type (magenta), its light a lilac: C and Bb",
        base=TYPE["CONTEXT"] if "CONTEXT" in TYPE else (176, 86, 158),
        front=R((6, 40, 60, 50)), back=R((6, 40, 60, 50)),
        slotmap={1: 6, 2: 6, 3: 10, 4: 10}, merge={6: 1}, ramp="cols",
        cols={6: (200, 160, 230), 10: (176, 86, 158)}),
    "SYLLABUS": dict(
        why="PRIMER line, stage 2 (SIX ISLAND's PATTERN BUSH, 10% in both): 0.0% waits, every colour carried",
        region="the ANTLERS and the ears' tips, gilded, and the dapples on its flank", colour="E and D, notes its part sings (gold into bronze)",
        base=g.pc_rgb(4),
        front=R((10, 4, 46, 20)), back=R((20, 4, 58, 19)),
        slotmap={1: 9, 2: 9, 3: 9, 4: 10}, merge={6: 7, 8: 7}, ramp="cols",
        extra=[dict(front=R((22, 30, 50, 46)), back=R((10, 30, 32, 46)), slotmap={1: 9})],
        cols={9: (235, 205, 95), 10: (170, 105, 40)}),
    "ECLIPSE": dict(
        why="SMUDGE line, stage 2 (FIVE ISLAND's LOST CAVE, 10% in both): 0.0% waits, no accent at all",
        region="the CORONA it stands in, gold, and the coat it shadows, indigo", colour="E and B, notes its part sings (gold; indigo)",
        base=g.pc_rgb(4),
        front=R((6, 4, 42, 36)), back=R((28, 4, 64, 36)),
        slotmap={1: 6, 2: 7}, ramp="cols",
        extra=[dict(front=R((14, 34, 54, 62)), back=R((8, 34, 48, 62)), slotmap={3: 8})],
        cols={6: (240, 210, 110), 7: (205, 150, 50), 8: (60, 35, 100)}),
    "WITHDRAWAL": dict(
        why="STARTLE line, stage 2 (SIX ISLAND's PATTERN BUSH, 10% in CONTEXT): 0.0% waits, no accent; HARDENED is the new type",
        region="the shell's PLATES, in HARDENED (the face left bare)", colour="HARDENED, the new type: E and Eb (gold into bronze)",
        base=(196, 170, 96),
        front=R((32, 6, 62, 36)), back=R((14, 14, 56, 26)),
        slotmap={1: 6, 2: 7, 3: 8}, ramp="cols",
        #  the bronze kept 52 off STARTLE's olive (128,148,72) and 85 off its lost rust (133,51,8): nearer, it is CARRIED
        cols={6: (235, 215, 145), 7: (205, 160, 75), 8: (165, 118, 50)}),
    "ATTUNE": dict(
        why="GUESSWORK line, stage 2 (FIVE ISLAND's MEMORIAL PILLAR, 10% in CONTEXT; ROUTE 25's grove in both): 2.6% waits",
        region="the TUTU, a spring green", colour="F and G, notes its part sings (mint into sea green)",
        base=g.pc_rgb(5),
        front=R((16, 30, 44, 40)), back=R((16, 30, 44, 40)),
        #  the hair's 13-pixel slate folded into the body's plum, the cheeks' peach into their pink, to free two slots
        slotmap={2: 6, 3: 8, 4: 8}, merge={8: 4, 6: 7}, ramp="cols",
        #  both kept 85 or more off GUESSWORK's lost slate (76,93,118) and grey teal (126,143,143), or they are CARRIED
        cols={6: (140, 230, 150), 8: (40, 160, 170)}),
    "SEETHE": dict(
        why="TEPID line, stage 2 (MT. EMBER's SUMMIT PATH, 10% in CONTEXT): 3.6% waits",
        region="the crest on its CROWN and the length of its TAIL, an ember (behind, the tail alone)", colour="Eb and C#, notes its part sings (amber into ember)",
        base=g.pc_rgb(1),
        front=R((46, 12, 62, 50), (36, 40, 62, 52), (14, 4, 36, 14)), back=R((16, 46, 48, 60)),
        slotmap={1: 7, 2: 7, 3: 9, 4: 10}, ramp="cols",
        cols={7: (250, 170, 90), 9: (225, 95, 50), 10: (160, 55, 30)}),
    "HEATDEATH": dict(
        why="TEPID line, stage 3 (MT. EMBER's SUMMIT PATH, 10% in CONTEXT): 1.2% waits",
        region="the gold of its BACK and crown gone to a cold violet", colour="B and Bb, notes its part sings (violet into indigo)",
        base=g.pc_rgb(11),
        front=R((32, 20, 60, 42)), back=R((28, 10, 50, 32)),
        #  the eye's 3-pixel blue folded into the navy beside it, to free a slot
        slotmap={2: 7, 3: 7, 4: 10}, merge={7: 9}, ramp="cols",
        extra=[dict(front=R((6, 12, 32, 30)), back=R(), slotmap={2: 7, 3: 7})],
        #  the indigo kept 60 off TEPID's lost navy (28,61,89): nearer, it is CARRIED
        cols={7: (150, 95, 200), 10: (70, 40, 125)}),
    "DUSTDEVIL": dict(
        why="SINKHOLE line, stage 3 (MT. EMBER's RUBY PATH, 10% in CONTENT): 0.0% waits, every colour carried",
        region="the WINGS' panes, a desert sunset inside their teal rims", colour="D and C#, notes its part sings (peach into coral)",
        base=g.pc_rgb(1),
        front=R((6, 4, 34, 20), (34, 2, 58, 22), (40, 30, 58, 48), (34, 36, 40, 48)),
        back=R((6, 2, 30, 20), (30, 4, 58, 20), (6, 36, 30, 48), (6, 30, 18, 36)),
        slotmap={1: 9, 2: 10}, ramp="cols",
        cols={9: (250, 200, 165), 10: (215, 110, 85)}),
}


#  STAGE 9 (the user, 2026-11-24: "T-604 stage 9"; DRAFT): fifteen more, by how often a player meets them, as stage 8
#  ranked them. Every later form left under 10% at 10% of a table (the rest of the 10%s: FIVE ISLAND's MEADOW, SIX
#  ISLAND's PATTERN BUSH and WATER PATH, FIVE ISLAND's LOST CAVE, SEVEN ISLAND's SEVAULT CANYON, MT. EMBER's RUBY PATH),
#  then the 5%s met in BOTH editions: SIX ISLAND's PATTERN BUSH by land, then the surf, THREE ISLAND's BOND BRIDGE
#  (reached before the ELITE FOUR) and FIVE ISLAND's. Skipped as before: STEEPEST, the cocoons (IFTRUE, IFFALSE, PENDING,
#  BUFFER, BROODING), any MUSAI, PENPHIN or UNOWN form. TODAY is the engine after stage 8 (BASE9): no form here was drawn
#  by stages 1-8. Every colour given exactly ("cols"), each checked against the carry rule by the report.
BASE9_COMMIT = "0b2411e0f"
FORMS9 = {
    "CRYWOLF": dict(
        why="WARNING line, stage 2 (FIVE ISLAND's MEADOW, 10% in CONTENT): 2.0% waits (only the mouth)",
        region="the HEAD and its ears, a wolf's tawny coming through the bulldog; behind, the ears and its coat's dapples", colour="E and D, notes its part sings (tawny into umber)",
        base=g.pc_rgb(4),
        front=R((12, 2, 60, 22)), back=R((4, 2, 60, 12)),
        #  the mouth's two pinks (14 and 18 pixels) folded into one, and the ear's two lesser reds into its red, to free 3
        slotmap={1: 6, 2: 8, 3: 10, 4: 10}, merge={6: 7, 8: 9, 10: 9}, ramp="cols",
        #  behind, the head is only its ears: the dapples of its coat go umber, a wolf's markings (a band cut straight)
        extra=[dict(front=R(), back=R((8, 12, 44, 42)), slotmap={4: 10})],
        #  the light kept 85 off WARNING's lost pink (255,153,205), the mouth's pinks folded: nearer, it is CARRIED
        cols={6: (235, 215, 150), 8: (210, 160, 90), 10: (140, 95, 50)}),
    "SIGKILL": dict(
        why="REAPER line, stage 2 (SIX ISLAND's PATTERN BUSH, 10% in CONTEXT): 2.4% waits (only the eyes); HARDENED is the new type",
        region="the DOME of its head, and the pincers' light, in HARDENED", colour="HARDENED, the new type: E and Eb (straw into bronze)",
        base=(196, 170, 96),
        front=R((18, 6, 44, 26), (2, 10, 18, 34), (44, 10, 62, 34)), back=R((18, 6, 44, 26), (2, 10, 18, 34), (44, 10, 62, 34)),
        #  the eye's 3-pixel crimson folded into its red, the 7 mauve glints into the pale olive beside them, to free two
        slotmap={1: 8, 2: 6}, merge={8: 9, 6: 2}, ramp="cols",
        cols={8: (235, 215, 145), 6: (205, 160, 75)}),
    "HEARTBEAT": dict(
        why="UPTIME line, stage 2 (SIX ISLAND's WATER PATH, 10% in CONTENT): 1.1% waits",
        region="the round LOWER BODY's shading in front, its quilted panels behind, a rose", colour="C and B, notes its part sings (blush into plum-rose)",
        base=g.pc_rgb(0),
        front=R((12, 33, 46, 52)), back=R((8, 33, 48, 56)),
        #  the 2-pixel slate folded into the dark beside it, to free a third slot
        slotmap={2: 7, 3: 8, 4: 10}, slotmap_back={2: 7, 3: 8}, merge={8: 4}, ramp="cols",
        #  the blush kept 48 off UPTIME's own greys (219,213,201): within 40 it is the same colour, CARRIED
        cols={7: (240, 170, 200), 8: (220, 120, 165), 10: (175, 90, 150)}),
    "CHECKMATE": dict(
        why="SPARRING line, stage 2 (SIX ISLAND's PATTERN BUSH, 10% in CONTENT): 9.3% waits in front, less behind; LOGIC is the new type",
        region="the CHEQUERED BOARD at its waist, in LOGIC (its dark squares indigo)", colour="LOGIC, the new type: G, its dark squares Bb",
        base=TYPE["LOGIC"],
        front=R((18, 44, 46, 56)), back=R((18, 44, 46, 56)),
        #  slot 6 (the chest's grey marks, 29 pixels) is recoloured LOGIC's mid and joins the board; 9 is the cuffs' indigo
        slotmap={1: 10, 2: 6, 4: 9}, ramp="cols",
        #  LOGIC's own (96,122,158) sits 41 off SPARRING's lost mauve (128,107,137), nearer than any colour left: CARRIED
        #  and the light kept 54 off SPARRING's white (206,225,207)
        cols={10: (170, 195, 235), 6: (70, 125, 185)}),
    "FORGETTING": dict(
        why="FADING line, stage 2 (FIVE ISLAND's LOST CAVE, 10% in CONTEXT): 0.0% waits, no accent at all",
        region="the HOOD (the face left bare), a dusk blue", colour="Ab and Bb, notes its part sings (dusk blue into indigo)",
        base=g.pc_rgb(8),
        front=R((20, 2, 44, 8), (18, 8, 25, 24), (39, 8, 46, 24)), back=R((18, 2, 46, 16)),
        slotmap={1: 7, 2: 8, 3: 9, 4: 10}, ramp="cols",
        cols={7: (170, 185, 240), 8: (120, 135, 215), 9: (80, 70, 175), 10: (45, 40, 105)}),
    "MINDWANDER": dict(
        why="DAYDREAM line, stage 3 (SIX ISLAND's WATER PATH, 10% in CONTENT): 0.2% waits",
        region="the fur of its HEAD drifting into sky blue (the face left bare), and its THOUGHT BUBBLES, lilac",
        colour="G and B, notes its part sings (sky blue; lilac)", base=g.pc_rgb(7),
        front=R((16, 4, 48, 30)), back=R((16, 4, 48, 30)),
        #  the 1-pixel slate folded into the 3-pixel one beside it, to free a slot for the bubbles
        slotmap={2: 8, 3: 9, 4: 10}, slotmap_back={2: 8, 3: 9}, merge={7: 6}, ramp="cols",
        extra=[dict(front=R((48, 2, 63, 16)), back=R((0, 2, 16, 16)), slotmap={1: 7})],
        #  the lilac kept 76 off DAYDREAM's lost pink (250,169,200), farther than the body's white (72): nearer, CARRIED
        cols={7: (190, 180, 245), 8: (165, 200, 240), 9: (100, 145, 210), 10: (55, 85, 150)}),
    "SHIFTLEFT": dict(
        why="LOWBIT line, stage 2 (SIX ISLAND's WATER PATH, 10% in CONTENT): 0.6% waits",
        region="the great EARS, brass horns", colour="E and D, notes its part sings (brass into bronze)",
        base=g.pc_rgb(4),
        front=R((6, 6, 25, 24), (39, 6, 60, 24)), back=R((6, 6, 25, 24), (39, 6, 60, 24)),
        slotmap={2: 9, 3: 10}, ramp="cols",
        #  the bronze kept 89 off LOWBIT's lost rose (194,59,76): nearer, it is CARRIED
        cols={9: (235, 210, 130), 10: (205, 145, 55)}),
    "SUBTEXT": dict(
        why="UNSPOKEN line, stage 2 (FIVE ISLAND's LOST CAVE, 10% in CONTEXT): 2.1% waits (only the eyes)",
        region="the HOOD, the teal of its eyes spreading over it", colour="F# and Ab, notes its part sings (the eyes' teal into ink blue)",
        base=g.pc_rgb(6),
        front=R((12, 8, 50, 19)), back=R((12, 8, 50, 19)),
        #  the hood takes the eyes' own teals (6 and 8), and one new ink blue for its shadow
        slotmap={1: 6, 2: 6, 3: 8, 4: 9}, ramp="cols",
        cols={9: (45, 75, 140)}),
    "BIGIRON": dict(
        why="BOOTROM line, stage 3 (SEVEN ISLAND's SEVAULT CANYON, 10% in CONTENT): 0.1% waits",
        region="the great DOME of its back, gone from straw to cold steel", colour="Ab and Bb, notes its part sings (steel into slate violet)",
        base=g.pc_rgb(8),
        front=R((18, 8, 44, 30)), back=R((18, 8, 44, 30)),
        slotmap={1: 7, 2: 8, 3: 9}, ramp="cols",
        #  no mid blue: anything between sits within 80 of BOOTROM's lost blues (87,147,193), (62,121,148) and is CARRIED
        cols={7: (205, 212, 240), 8: (175, 180, 230), 9: (60, 45, 110)}),
    "TRUNKLINE": dict(
        why="TOKENRING line, stage 2 (MT. EMBER's RUBY PATH, 10% in CONTENT): 4.6% waits (only the claws)",
        region="the HELMET and its horns, a blue-violet steel", colour="A and Bb, notes its part sings (periwinkle into violet)",
        base=g.pc_rgb(9),
        front=R((6, 6, 58, 22)), back=R((6, 6, 58, 22)),
        slotmap={2: 9, 3: 10}, ramp="cols",
        #  kept 82 off TOKENRING's lost mint (162,221,186): nearer than the body's white, it is CARRIED
        cols={9: (150, 150, 225), 10: (95, 65, 170)}),
    "GESTALT": dict(
        why="INKLING line, stage 2 (SEVEN ISLAND's SEVAULT CANYON, 10% in CONTEXT): 3.4% waits (only the eyes' rings)",
        region="the CROWN of its shell, with its hatching, lilac", colour="B and A, notes its part sings (lilac into periwinkle)",
        base=g.pc_rgb(11),
        front=R((10, 14, 54, 24)), back=R((10, 14, 54, 24)),
        slotmap={1: 9, 2: 10}, ramp="cols",
        cols={9: (200, 170, 235), 10: (130, 125, 210)}),
    "ENTRAPMENT": dict(
        why="AMBUSH line, stage 2 (SIX ISLAND's PATTERN BUSH, 5% in CONTENT and 4% in CONTEXT): 2.8% waits (only the eyes)",
        region="the WEB it sits in, gold silk (behind its body and legs, a few threads stay white)", colour="E, a note its part sings (gold)",
        base=g.pc_rgb(4),
        front=R((0, 0, 63, 17), (0, 48, 63, 63), (0, 17, 18, 28), (0, 28, 7, 47), (45, 17, 63, 28), (56, 28, 63, 47)),
        back=R((0, 0, 63, 17), (0, 48, 63, 63), (0, 17, 18, 28), (0, 28, 7, 47), (45, 17, 63, 28), (56, 28, 63, 47)),
        slotmap={1: 10}, ramp="cols",
        #  kept 59 off AMBUSH's lost peach (238,180,143), farther than the eyes' orange (43): nearer, it is CARRIED
        cols={10: (235, 215, 95)}),
    "SHALLOWS": dict(
        why="BIFURCATE line, stage 2 (THREE ISLAND's BOND BRIDGE, surfing 5% in both): 0.0% waits, the one accent carried",
        region="the FINS and the long TAIL, sea glass", colour="F, a note its part sings (sea glass into sea green)",
        base=g.pc_rgb(5),
        front=R((30, 2, 52, 32), (12, 36, 30, 58), (30, 38, 48, 46)), back=R((6, 2, 30, 32), (30, 36, 50, 58), (18, 38, 34, 46)),
        slotmap={2: 7, 3: 8}, ramp="cols",
        cols={7: (150, 220, 195), 8: (60, 170, 150)}),
    "BLACKWATER": dict(
        why="BACKFLOW line, stage 2 (FIVE ISLAND, surfing 5% in both): 0.0% waits, no accent; OPAQUE is the new type",
        region="the two halves of its SHELL, gone to an oil-black violet, a sheen at their shoulders", colour="OPAQUE, the new type, its sheen Bb",
        base=(68, 28, 108),
        front=R((10, 18, 30, 52), (34, 18, 54, 52)), back=R((10, 18, 30, 52), (34, 18, 54, 52)),
        slotmap={4: 9}, ramp="cols",
        #  the sheen on the shoulders of the shell only: all of it is 27% (too much)
        extra=[dict(front=R((10, 18, 30, 28), (34, 18, 54, 28)), back=R((10, 18, 30, 28), (34, 18, 54, 28)), slotmap={3: 10})],
        #  the black kept 47 off the body's own navy (36,55,91): within 40 it is the same colour, CARRIED
        cols={9: (68, 28, 108), 10: (110, 80, 165)}),
    "CADENCE": dict(
        why="TEMPO line, stage 2 (FIVE ISLAND's MEADOW, surfing 5% in both): 0.0% waits, every colour carried",
        region="the lily pad of its HAT (and its shoulders' leaves) coming into flower, and its BELLY blushing",
        colour="C and Bb, notes its part sings (blossom into plum)", base=g.pc_rgb(0),
        front=R((0, 0, 63, 63)), back=R((0, 0, 63, 63)),
        slotmap={6: 9, 7: 10}, ramp="cols",
        extra=[dict(front=R((24, 30, 40, 46)), back=R((24, 30, 40, 46)), slotmap={1: 9, 2: 9, 3: 10})],
        cols={9: (245, 170, 200), 10: (165, 80, 165)}),
}


def pal_of(w, k):
    return [tuple(c) for c in w.palette(k)]


def make(w, n):
    k = w.by_name[n]
    spec = FORMS[n]
    with Base(w):
        pal = pal_of(w, k)
        sides = {s: Image.open(os.path.join(w.folder(k), s + ".png")) for s in ("front", "back")}
    data = {s: list(im.getdata()) for s, im in sides.items()}
    for a, b in (spec.get("merge") or {}).items():
        for s in data:
            data[s] = [b if v == a else v for v in data[s]]
    lo, mid, dk = ramp3(spec["base"])
    dk = spec.get("dark", dk)          # a dark moved past CARRY_FAR of an earlier form's lost colour
    new = sorted(set(spec["slotmap"].values()) | set((spec.get("slotmap_back") or {}).values())
                 | {b for ex in spec.get("extra") or () for b in list(ex["slotmap"].values()) + list((ex.get("slotmap_back") or {}).values())})
    if spec["ramp"] == "keep6":         # slot 6 is already a light SIGNAL-ish cyan: it is the light, 9 and 10 mid and dark
        cols = {6: pal[6], 9: mid, 10: dk}
    elif spec["ramp"] == "mid":         # one slot: the mid tone, shaded by the carried dark already round it
        cols = {10: mid}
    elif spec["ramp"] == "two":         # mid and dark only: the light tone would sit within 80 of an earlier form's
        cols = {new[0]: mid, new[1]: dk}  #   lost accent and be CARRIED by gencolourbysong's "nearest to one"
    elif spec["ramp"] == "one":         # one slot, the colour itself
        cols = {new[0]: tuple(spec["base"])}
    elif spec["ramp"] == "lomid":       # light and mid: a pale region (smoke, a belly) keeps its lightness
        cols = {new[0]: lo, new[1]: mid}
    elif spec["ramp"] == "cols":        # stage 3: each new slot's colour given exactly (escaping CARRY_NEAR/FAR by hand)
        cols = {a: tuple(b) for a, b in spec["cols"].items()}
    elif spec["ramp"] == "hope":        # mid on slot 6, slot 8's own dark red kept as the dark
        cols = {6: tuple(spec["base"]), 8: pal[8]}
    else:
        tones = [lo, mid, dk]
        cols = {s: tones[min(i, 2)] for i, s in enumerate(new)} if len(new) <= 3 else None
    for s, c in cols.items():
        pal[s] = c
    for side in ("front", "back"):
        boxes = spec[side]
        only = spec.get("backonly_slots") if side == "back" else None
        out = []
        for i, v in enumerate(data[side]):
            x, y = i % 64, i // 64
            m = spec.get("slotmap_back", spec["slotmap"]) if side == "back" else spec["slotmap"]
            if only is not None:
                m = {a: b for a, b in m.items() if a in only}
            if v in m and any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in boxes):
                out.append(m[v])
                continue
            for ex in spec.get("extra") or ():      # a second part of the region, with its own slots
                em = ex.get("slotmap_back", ex["slotmap"]) if side == "back" else ex["slotmap"]
                if v in em and any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in ex[side]):
                    out.append(em[v])
                    break
            else:
                out.append(v)
        data[side] = out
    d = os.path.join(OUT, n)
    os.makedirs(d, exist_ok=True)
    for side, im in sides.items():
        o = Image.new("P", (64, 64))
        o.putpalette([x for c in pal for x in c] + [0] * (768 - 48))
        o.putdata(data[side])
        o.info["transparency"] = 0
        o.save(os.path.join(d, side + ".png"), transparency=0)
    with open(os.path.join(d, "normal.pal"), "w") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in pal))
    return d


class Draft:
    """gencolourbysong's World, with every stage-1 form read from its draft folder -- all at once, because a drafted
    earlier form's new colours are a later form's earlier colours (RUBRIC's red is CANON's to carry or not). Base: the
    same, from each form's base/ (today, before T-604)."""
    SUB = ""

    def __init__(self, w, n=None):
        self.w = w
        self.d = {w.by_name[m]: os.path.join(OUT, m, self.SUB) for m in ORDER
                  if os.path.exists(os.path.join(OUT, m, self.SUB, "normal.pal"))}
        self.orig = w.folder

    def __enter__(self):
        o, d = self.orig, self.d
        self.w.folder = lambda kk: d.get(kk) or o(kk)
        return self.w

    def __exit__(self, *a):
        self.w.folder = self.orig


class Base(Draft):
    SUB = "base"


def file_base(w):
    """Each form's art before T-604, out of the engine's history (BASE_COMMIT), into <NAME>/base/."""
    import subprocess
    for n in ORDER:
        k = w.by_name[n]
        rel = \
            "graphics/pokemon/" + w.sp[k]["constant"].lower()
        d = os.path.join(OUT, n, "base")
        os.makedirs(d, exist_ok=True)
        for f in ("front.png", "back.png", "normal.pal", "shiny.pal"):
            data = subprocess.run(["git", "-C", g.GBA, "show", "%s:%s/%s" % (BASE_COMMIT, rel, f)],
                                  capture_output=True, check=True).stdout
            open(os.path.join(d, f), "wb").write(data)
        print("t604: base %s from %s" % (n, BASE_COMMIT))


def area(w, k, side):
    _, t = g.ties(w, k, "A")
    idx = [v for v in Image.open(os.path.join(w.folder(k), side + ".png")).getdata() if v]
    return sum(1 for v in idx if t[v][0] in ("body", "accent") and not t[v][2]) / max(1, len(idx))


def slots_used(w, k):
    used = set()
    for s in ("front", "back"):
        used |= set(Image.open(os.path.join(w.folder(k), s + ".png")).getdata())
    return used


def summary(w, n):
    k = w.by_name[n]
    with Base(w):
        before = (area(w, k, "front"), area(w, k, "back"))
        ub = slots_used(w, k)
    with Draft(w, n):
        after = (area(w, k, "front"), area(w, k, "back"))
        pal, t = g.ties(w, k, "A")
        ua = slots_used(w, k)
        newslots = [(i, pal[i], g.name(t[i][1]), "CARRIED" if t[i][2] else "%d notes" % len(t[i][3]))
                    for i in sorted(set(FORMS[n]["slotmap"].values()) | set((FORMS[n].get("slotmap_back") or {}).values())
                                    | {b for ex in FORMS[n].get("extra") or ()
                                       for b in list(ex["slotmap"].values()) + list((ex.get("slotmap_back") or {}).values())})]
    return before, after, newslots, sorted(ua - ub), sorted(ub - ua)


def report(w):
    for n in ORDER:
        make(w, n)
    for n in ORDER:
        b, a, ns, gained, freed = summary(w, n)
        f = FORMS[n]
        print("%-10s %s\n    region: %s; colour: %s" % (n, f["why"], f["region"], f["colour"]))
        print("    waits on its own part: front %4.1f%% -> %4.1f%%   back %4.1f%% -> %4.1f%%" % (
            100 * b[0], 100 * a[0], 100 * b[1], 100 * a[1]))
        print("    new slots: %s; slots newly used %s, emptied %s%s" % (
            ", ".join("%d %s->%s %s" % (i, "%d,%d,%d" % c, p, x) for i, c, p, x in ns), gained, freed,
            "; merged %s" % f["merge"] if f.get("merge") else ""))


def sheet(w, outdir):
    os.makedirs(outdir, exist_ok=True)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
        big = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
    except OSError:
        font = big = ImageFont.load_default()
    SC, CELL, LABEL = 2, 132, 250
    cols = [("TODAY", "today", None), ("today 0%", "today", 0), ("DRAFT 0%", "draft", 0),
            ("DRAFT 50%", "draft", 128), ("DRAFT 100%", "draft", 255)]
    BG = (236, 236, 230)
    rowh = 2 * (CELL + 4) + 34
    W = LABEL + len(cols) * (CELL + 8) + 12
    H = 70 + len(ORDER) * rowh + 30
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((12, 10), "T-604 stage %d (DRAFT): a region in the new part's colours, recoloured from the drawing" % STAGE,
           fill=(20, 20, 24), font=big)
    d.text((12, 34), "% = share of the form's OWN part learned (gencolourbysong's maths, approach A: what the game shows). "
           "Front above, back below, 2x.", fill=(60, 60, 60), font=font)
    d.text((12, 50), "'waits' = pixels whose colour waits on its own part (not carried, not ink, not a streak).",
           fill=(60, 60, 60), font=font)

    def pic(k, side, share):
        pal = g.shown(w, k, "A", share) if share is not None else [tuple(c) for c in w.palette(k)]
        idx = list(Image.open(os.path.join(w.folder(k), side + ".png")).getdata())
        rgb = Image.new("RGB", (64, 64)); rgb.putdata([pal[v] for v in idx])
        m = Image.new("L", (64, 64)); m.putdata([255 if v else 0 for v in idx])
        return rgb.resize((64 * SC, 64 * SC), Image.NEAREST), m.resize((64 * SC, 64 * SC), Image.NEAREST)

    y = 70
    for n in ORDER:
        k = w.by_name[n]
        b, a, ns, gained, freed = summary(w, n)
        f = FORMS[n]
        d.text((12, y), n, fill=(20, 20, 24), font=big)
        txt = ["%s, %s" % ("/".join(w.sp[k]["types"]), w.rows[k]["key"]), f["region"], "colour: " + f["colour"],
               "waits, front: %.0f%% -> %.0f%%" % (100 * b[0], 100 * a[0]),
               "waits, back:  %.0f%% -> %.0f%%" % (100 * b[1], 100 * a[1]),
               "new slots: " + " ".join(str(i) for i, *_ in ns),
               "slots: +%s -%s%s" % (gained or "[]", freed or "[]", " merged %s" % f["merge"] if f.get("merge") else "")]
        yy = y + 24
        for t in txt:
            for chunk in [t[i:i + 32] for i in range(0, len(t), 32)]:
                d.text((12, yy), chunk, fill=(50, 50, 50), font=font)
                yy += 15
        for ci, (title, which, share) in enumerate(cols):
            x = LABEL + ci * (CELL + 8)
            for si, side in enumerate(("front", "back")):
                yy = y + 22 + si * (CELL + 4)
                with (Draft(w, n) if which == "draft" else Base(w)):
                    p, m = pic(k, side, share)
                d.rectangle([x, yy, x + CELL, yy + CELL], fill=(205, 205, 172), outline=(200, 200, 194))
                im.paste(p, (x + 2, yy + 2), m)
            d.text((x + 2, y + 4), title, fill=(70, 70, 70), font=font)
        y += rowh
    d.text((12, H - 24), "Recolours only: the drawing is unchanged; only which palette slot a region's pixels use, and those "
           "slots' colours. Icons and followers: note only.", fill=(80, 80, 80), font=font)
    path = os.path.join(outdir, "t604_stage%d.png" % STAGE)
    im.save(path)
    print("t604: wrote %s" % path)


def install():  # noqa: the World built here reads names only
    """The user approved all nine (2026-11-22; HOPE's red at the wing tips and the tail feather only): file each as
    tools/gbasprite.py's approved reduction, read there exactly (its palette the species')."""
    dst = os.path.join(ROOT, "gfx", "daemons", "reduced")
    clean = os.path.join(dst, "clean")
    os.makedirs(clean, exist_ok=True)
    w = g.World()
    for n in ORDER:
        for side in ("front", "back"):
            shutil.copyfile(os.path.join(OUT, n, side + ".png"), os.path.join(dst, "%s_%s.png" % (n.lower().replace(" ", "_"), side)))  # LEMMA MIND: gbasprite GBA_NAME
        #  The follower is reduced from the CLEAN drawing, which has no region (icons and followers unchanged, the
        #  user's stage 1): tools/gbafollowerpal.py remaps it onto the palette that drawing was reduced to, kept here.
        folder = w.sp[w.by_name[n]]["constant"].lower()
        for f, to in (("normal.pal", folder + ".pal"), ("shiny.pal", folder + ".shiny.pal")):
            shutil.copyfile(os.path.join(OUT, n, "base", f), os.path.join(clean, to))
        print("t604: filed %s" % n)


def main():
    global FORMS, ORDER, STAGE, BASE_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "2":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS2, list(FORMS2), 2, BASE2_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "3":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS3, list(FORMS3), 3, BASE3_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "4":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS4, list(FORMS4), 4, BASE4_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "5":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS5, list(FORMS5), 5, BASE5_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "6":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS6, list(FORMS6), 6, BASE6_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "7":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS7, list(FORMS7), 7, BASE7_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "8":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS8, list(FORMS8), 8, BASE8_COMMIT
    if "--stage" in sys.argv and sys.argv[sys.argv.index("--stage") + 1] == "9":
        FORMS, ORDER, STAGE, BASE_COMMIT = FORMS9, list(FORMS9), 9, BASE9_COMMIT
    w = g.World()
    if "--base" in sys.argv:
        return file_base(w)
    if "--install" in sys.argv:
        return install()
    if "--built" in sys.argv:
        Draft.SUB = "__built__"        # no such folder: every form is read from the engine as built
        return sheet(w, sys.argv[sys.argv.index("--sheet") + 1])
    report(w)
    if "--sheet" in sys.argv:
        sheet(w, sys.argv[sys.argv.index("--sheet") + 1])


if __name__ == "__main__":
    main()
