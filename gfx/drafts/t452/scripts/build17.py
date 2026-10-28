"""T-452 batch 17 (HONEYTRAP to SHALLOWS, 355-375), built on the recommended answers (hand_b17.py),
installed on the coordinator's "go" (2026-10-28) as dir v. What goes into gfx/daemons/.

    build17.py install    copy the chosen art into gfx/daemons/ (v/hand/ -- every front, back and icon has one)
    build17.py iconpal    print gMonIconPaletteIndices' rows for the 20 (icon3's palette), and with --write set them

Then, as batches 10-16: tools/gbasprite.py --write, scripts/ground.py --write SLOT..., tools/gbaowslots.py --write,
tools/gbafollowerpal.py --write."""
import json, os, re, shutil, sys
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/v"; OUT = R + "/gfx/daemons"
NAMES = ['honeytrap', 'witness', 'mindsight', 'datagram', 'tradewind', 'fading', 'forgetting', 'laced', 'daydream', 'restless', 'mindwander', 'greedy', 'bloatware', 'transfer', 'lowbit', 'shiftleft', 'wraparound', 'bifurcate', 'deepwell', 'shallows']
P = json.load(open(F + "/picks.json"))

def install():
    for n in NAMES:
        fn = n.replace(" ", "_")
        for k, d in (("front", "clean"), ("back", "clean"), ("icon", "hand")):
            h = f"{F}/hand/{n}_{k}.png"; s = h if os.path.exists(h) else f"{F}/{d}/{n}_{k}.png"
            shutil.copyfile(s, f"{OUT}/{fn}_{k}.png"); print("%-34s -> gfx/daemons/%s_%s.png" % (os.path.relpath(s, F), fn, k))

def iconpal():
    f = R + "/engineGba/src/pokemon_icon.c"; t = open(f).read(); n0 = len(t)
    for n in NAMES:
        slot = P[n]["slot"].upper(); pi = P[n]["measured"]["icon3"]["icon_palette"]
        pat = re.compile(r"(\[SPECIES_%s\]\s*= )(\d)(,)" % slot)
        m = list(pat.finditer(t))[-1]
        print("%-10s %-12s %s -> %d" % (n, slot, m[2], pi))
        t = t[:m.start(2)] + str(pi) + t[m.end(2):]
    if "--write" in sys.argv:
        assert abs(len(t) - n0) == 0, "length changed"   # one digit for one digit: never a short write
        tmp = f + ".tmp"; open(tmp, "w").write(t); os.replace(tmp, f)   # temp then rename, never truncate in place

if __name__ == "__main__":
    {"install": install, "iconpal": iconpal}[sys.argv[1]]()
