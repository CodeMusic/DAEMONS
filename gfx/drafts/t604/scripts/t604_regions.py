#!/usr/bin/env python3
"""T-604 stages 1, 2 and 3 (DRAFT): give a later form a REGION in its new part's colours, by RECOLOURING a natural part of the
drawing already there (ears, crest, tail, drawers, wings), so it visibly colours in as it learns its part (T-597).

    python3 gfx/drafts/t604/scripts/t604_regions.py               # report each form: region, slots, coverage before/after
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 2 ...  # the same for STAGE 2's twelve (FORMS2)
    python3 gfx/drafts/t604/scripts/t604_regions.py --stage 3 ...  # ... and STAGE 3's fifteen (FORMS3)
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
A slot freed for it by MERGE is a near-duplicate folded into its neighbour first (a handful of pixels).
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
    new = sorted(set(spec["slotmap"].values()) | set((spec.get("slotmap_back") or {}).values()))
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
                    for i in sorted(set(FORMS[n]["slotmap"].values()) | set((FORMS[n].get("slotmap_back") or {}).values()))]
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
