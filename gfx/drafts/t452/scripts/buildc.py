"""T-452 arm C (2026-11-06): the user's "Build the good ones" -- what goes into gfx/daemons/ from gfx/drafts/t452/c/armc/.

    buildc.py install           copy the chosen art into gfx/daemons/ (front and back cleaned, the icon icon3's)
    buildc.py iconpal [--write] gMonIconPaletteIndices' rows for every icon installed (the palette each icon is in)
    buildc.py slots             the species folders whose art changed (for ground.py, outside THE NEXUS)

BUILT: front, back and icon for 21 redraws (the worst ten less the held, batch 13 restyled less the held) and the backs
of seven mismatched backs (ENSEMBLE's icon too); 74 of the 95 drafted icons. SMUDGE keeps its ROM icon (its draft came
out pale purple). REFLECTION, LODESTAR and BASTET are THE NEXUS's: tools/gbanexus.py takes their art from the arm C
drafts itself (its REDRAWN), so nothing here writes them except their icon palette, which gbanexus also sets.

HELD (ROM unchanged, for a redraw round): ECLIPSE, CRAWLER, OVERLOADED, PERIHELION, LYUBOV, MULTIMAL, LYNX, ILLUMINED,
HEATDEATH, SEETHE; and the icons of ACQUIRE, BLOCKING, BURSTMODE, ENTRAPMENT, EPIPHANY, KEEPER, KHIONE, LENSMUSAI (still
muddy), CIRCULAR, EMERGENCE, WORM, CINDER, GRASP (drifted from their fronts) and SMUDGE.

Then: tools/gbanexus.py --write, tools/gbasprite.py --write, scripts/ground.py --write SLOT..., tools/gbaowslots.py
--write, tools/gbafollowerpal.py --write, tools/genstreaks.py / genshiny.py as they report."""
import json, os, re, shutil, sys
R = os.environ.get("DAEMONS_ROOT", "/Users/christopherhicks/Projects/DAEMONS")
A = R + "/gfx/drafts/t452/c/armc"; OUT = R + "/gfx/daemons"
P = json.load(open(A + "/picks.json"))
SPEC = json.load(open(R + "/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in SPEC.values()}

REDRAWS = ("broadcast tracer fossilnet rovercub smogstack obsession lodestar reflection bastet stump boosting canopy coinflip "
           "montecarlo lasvegas runoff alluvium delta smudge detour unbranched").split()
BACKS = "ensemble wiretap manifold monolith outlier heartbeat corefile".split()
NEXUS = {"lodestar", "reflection", "bastet"}
HELD = "eclipse crawler overloaded perihelion lyubov multimal lynx illumined heatdeath seethe".split()
NO_ICON = ("acquire blocking burstmode entrapment epiphany keeper khione lensmusai "
           "circular emergence worm cinder grasp smudge").split()
ICONS = [n for n in P if "icon_seed" in P[n] and n not in HELD and n not in NO_ICON]


def install():
    for n in REDRAWS + BACKS:
        if n in NEXUS: continue
        key = "%s_%d" % (n, P[n]["seed"])
        for k in (("back",) if n in BACKS else ("front", "back")):
            shutil.copyfile("%s/clean/%s_%s.png" % (A, key, k), "%s/%s_%s.png" % (OUT, n, k))
            print("clean/%s_%s.png -> gfx/daemons/%s_%s.png" % (key, k, n, k))
    for n in ICONS:
        if n in NEXUS: continue
        src = "%s/reduced/%s_icon_%d.png" % (A, n, P[n]["icon_seed"])
        shutil.copyfile(src, "%s/%s_icon.png" % (OUT, n)); print("%s -> gfx/daemons/%s_icon.png" % (os.path.relpath(src, A), n))
    print(len(REDRAWS), "redraws,", len(BACKS), "backs,", len(ICONS), "icons")


def slot(n):
    return BY[n]["constant"].lower()


def iconpal():
    sys.path.insert(0, R + "/tools")
    from PIL import Image
    pals = []
    for i in range(3):
        l = open(R + "/engineGba/graphics/pokemon/icon_palettes/icon_palette_%d.pal" % i).read().split()
        pals.append([int(v) for v in l[3:51]])
    f = R + "/engineGba/src/pokemon_icon.c"; t = open(f).read(); n0 = len(t)
    for n in ICONS:
        if n in NEXUS: continue
        ip = Image.open("%s/%s_icon.png" % (OUT, n)).getpalette()[:48]
        pi = [i for i, p in enumerate(pals) if p == ip]; assert len(pi) == 1, n
        pat = re.compile(r"(\[SPECIES_%s\]\s*= )(\d)(,)" % slot(n).upper())
        m = list(pat.finditer(t))[-1]
        if int(m[2]) != pi[0]: print("%-11s %-12s %s -> %d" % (n, slot(n), m[2], pi[0]))
        t = t[:m.start(2)] + str(pi[0]) + t[m.end(2):]
    if "--write" in sys.argv:
        assert len(t) == n0, "length changed"   # one digit for one digit: never a short write
        tmp = f + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, f)


def slots():
    print(" ".join(slot(n) for n in REDRAWS + BACKS if n not in NEXUS))


if __name__ == "__main__":
    {"install": install, "iconpal": iconpal, "slots": slots}[sys.argv[1]]()
