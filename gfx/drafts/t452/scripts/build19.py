"""T-452 batch 19 (SINGLETON to OVERTONE, 398-411 less PROTEUS -- the user: its three forms a job of their own), built on
the recommended answers (hand_b19.py), installed on the coordinator's "go" (2026-10-28) as dir x. What goes into gfx/daemons/.

    build19.py install    copy the chosen art into gfx/daemons/ (x/hand/ -- every front, back and icon has one)
    build19.py iconpal    print gMonIconPaletteIndices' rows for the 13 (icon3's palette), and with --write set them

Then, as batches 10-18: tools/gbasprite.py --write, scripts/ground.py --write SLOT..., tools/gbaowslots.py --write,
tools/gbafollowerpal.py --write."""
import json, os, re, shutil, sys
#  R: the checkout this runs from (batch 19 was built in a scratchpad worktree while a release held the main one)
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))); F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/x"; OUT = R + "/gfx/daemons"
NAMES = ['singleton', 'pairwise', 'federated', 'deucalion', 'khione', 'talos', 'pontus', 'gaia', 'ouranos', 'polydeuces', 'castor', 'elpis', 'overtone']
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
