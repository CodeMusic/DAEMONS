"""T-452 round two, BUILT (the user, 2026-10-26, on the round-two sheet): what goes into gfx/daemons/, gbasprite's sources.

    build_r2.py icons     icon3 for every batch-1 icon not yet redrawn -> r/reduced/<name>_icon.png
    build_r2.py install   copy the chosen art into gfx/daemons/ (prints what it copied)

PART A    ROVERCUB's front ungrounded (r/clean), LOCUS's back turned from its front, RELAY's and BUFFER's 58-cell backs.
ICONS     every one of the 25 built in engine c0eb28f32 redone by icon3: the drawn busts (b/clean, d/clean) where there
          was one; the four muddy ones already in r/reduced; and the seven that were DERIVED from the front (LABEL,
          RUBRIC, CLUSTER, LOCUS, PENDING, SCRAPER, BUFFER: no usable bust was drawn) from their clean front, so they
          too are filed as drawn icons in icon3's three bands.
MANIFOLD  option A (e/: the folded-paper manta, t2i 4903), its back and icon.
BATCH 2   WORM to SPRAWL (e/clean fronts and backs, e/reduced icons by icon3), with hand_r2.py's three fixes
          (e/hand: FORK's split tail, PREDICTOR's horn, OUTLIER's back without ears)."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import icon3
R = "/Users/christopherhicks/Projects/DAEMONS"; T = R + "/gfx/drafts/t452"; OUT = R + "/gfx/daemons"
PILOTS = json.load(open(T + "/b/picks2.json")); B1 = json.load(open(T + "/d/picks.json")); B2 = json.load(open(T + "/e/picks.json"))
BATCH1 = [n for n in list(PILOTS) + list(B1) if not n.startswith("_") and n != "manifold"]
BATCH2 = [n for n in B2 if n != "manifold"]
MUDDY = ("roverseer", "indexer", "injector", "crawler")

def typ(n):
    return (PILOTS.get(n) or B1.get(n))["type"]

def icon_src(n):
    for d in ("b", "d"):
        f = f"{T}/{d}/clean/{n}_icon.png"
        if os.path.exists(f) and (n in PILOTS or B1[n]["icon"] != "derived"): return f
    return f"{OUT}/{n}_front.png"                    # derived before: icon3 from the clean front

def icons():
    rep = {}
    for n in BATCH1:
        if n in MUDDY: continue
        src = icon_src(n)
        rep[n] = dict(icon3.make(n, typ(n), src, f"{T}/r/reduced/{n}_icon.png"), src=os.path.relpath(src, R))
    json.dump(rep, open(T + "/r/icons.json", "w"), indent=1)
    for n, v in rep.items(): print(n, v["src"], "pal", v["icon_palette"], "ramp", v["ramp"], "size", v["size"])

def install():
    cp = []
    def put(src, name):
        shutil.copyfile(src, f"{OUT}/{name}.png"); cp.append((os.path.relpath(src, T), name))
    put(f"{T}/r/clean/rovercub_front.png", "rovercub_front")
    for n in ("locus", "relay", "buffer"): put(f"{T}/r/clean/{n}_back.png", f"{n}_back")
    for n in BATCH1: put(f"{T}/r/reduced/{n}_icon.png", f"{n}_icon")
    for n in ["manifold"] + BATCH2:
        for k in ("front", "back"):
            h = f"{T}/e/hand/{n}_{k}.png"; put(h if os.path.exists(h) else f"{T}/e/clean/{n}_{k}.png", f"{n}_{k}")
        h = f"{T}/e/hand/{n}_icon.png"; put(h if os.path.exists(h) else f"{T}/e/reduced/{n}_icon.png", f"{n}_icon")
    for s, n in cp: print("%-32s -> gfx/daemons/%s.png" % (s, n))
    print(len(cp), "files")

if __name__ == "__main__":
    {"icons": icons, "install": install}[sys.argv[1]]()
