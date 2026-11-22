#!/usr/bin/env python3
"""T-604 stage 1 (DRAFT): give a later form a REGION in its new part's colours, by RECOLOURING a natural part of the
drawing already there (ears, crest, tail, drawers, wings), so it visibly colours in as it learns its part (T-597).

    python3 gfx/drafts/t604/scripts/t604_regions.py               # report each form: region, slots, coverage before/after
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
    new = sorted(set(spec["slotmap"].values()))
    if spec["ramp"] == "keep6":         # slot 6 is already a light SIGNAL-ish cyan: it is the light, 9 and 10 mid and dark
        cols = {6: pal[6], 9: mid, 10: dk}
    elif spec["ramp"] == "mid":         # one slot: the mid tone, shaded by the carried dark already round it
        cols = {10: mid}
    elif spec["ramp"] == "two":         # mid and dark only: the light tone would sit within 80 of an earlier form's
        cols = {new[0]: mid, new[1]: dk}  #   lost accent and be CARRIED by gencolourbysong's "nearest to one"
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
            m = spec["slotmap"]
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
                    for i in sorted(set(FORMS[n]["slotmap"].values()))]
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
    d.text((12, 10), "T-604 stage 1 (DRAFT): a region in the new part's colours, recoloured from the drawing",
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
        b, a, ns, _, _ = summary(w, n)
        f = FORMS[n]
        d.text((12, y), n, fill=(20, 20, 24), font=big)
        txt = ["%s, %s" % ("/".join(w.sp[k]["types"]), w.rows[k]["key"]), f["region"], "colour: " + f["colour"],
               "waits, front: %.0f%% -> %.0f%%" % (100 * b[0], 100 * a[0]),
               "waits, back:  %.0f%% -> %.0f%%" % (100 * b[1], 100 * a[1]),
               "new slots: " + " ".join(str(i) for i, *_ in ns)]
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
    path = os.path.join(outdir, "t604_stage1.png")
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
            shutil.copyfile(os.path.join(OUT, n, side + ".png"), os.path.join(dst, "%s_%s.png" % (n.lower(), side)))
        #  The follower is reduced from the CLEAN drawing, which has no region (icons and followers unchanged, the
        #  user's stage 1): tools/gbafollowerpal.py remaps it onto the palette that drawing was reduced to, kept here.
        folder = w.sp[w.by_name[n]]["constant"].lower()
        for f, to in (("normal.pal", folder + ".pal"), ("shiny.pal", folder + ".shiny.pal")):
            shutil.copyfile(os.path.join(OUT, n, "base", f), os.path.join(clean, to))
        print("t604: filed %s" % n)


def main():
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
