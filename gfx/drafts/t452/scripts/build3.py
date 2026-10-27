"""T-452 batch 3, BUILT (the user, 2026-10-27, approving the batch-3 sheet): what goes into gfx/daemons/.

    build3.py install    copy the chosen art into gfx/daemons/ (hand/ where hand3.py drew, else clean/ and reduced/)
    build3.py iconpal    print gMonIconPaletteIndices' rows for the 22 (icon3's palette), and with --write set them

Then, as round two: tools/gbasprite.py --write, scripts/ground.py --write SLOT..., tools/gbaowslots.py --write,
tools/gbafollowerpal.py --write."""
import json, os, re, shutil, sys
R = "/Users/christopherhicks/Projects/DAEMONS"; F = R + "/gfx/drafts/t452/f"; OUT = R + "/gfx/daemons"
NAMES = ("skew badseed payload rootkit resident spyware tappoint wiretap cookie tracker fault handler preempt livelock "
         "sentry guardian loop spinlock mutex hunch inference conjecture").split()
P = json.load(open(F + "/picks.json"))

def install():
    for n in NAMES:
        for k, d in (("front", "clean"), ("back", "clean"), ("icon", "reduced")):
            h = f"{F}/hand/{n}_{k}.png"; s = h if os.path.exists(h) else f"{F}/{d}/{n}_{k}.png"
            shutil.copyfile(s, f"{OUT}/{n}_{k}.png"); print("%-34s -> gfx/daemons/%s_%s.png" % (os.path.relpath(s, F), n, k))

def iconpal():
    f = R + "/engineGba/src/pokemon_icon.c"; t = open(f).read()
    for n in NAMES:
        slot = P[n]["slot"].upper(); pi = P[n]["measured"]["icon3"]["icon_palette"]
        pat = re.compile(r"(\[SPECIES_%s\]\s*= )(\d)(,)" % slot)
        m = [m for m in pat.finditer(t) if "gMonIconPaletteIndices" in t[:m.start()][-20000:]]
        m = list(pat.finditer(t))[-1]
        print("%-10s %-12s %s -> %d" % (n, slot, m[2], pi))
        t = t[:m.start(2)] + str(pi) + t[m.end(2):]
    if "--write" in sys.argv: open(f, "w").write(t)

if __name__ == "__main__":
    {"install": install, "iconpal": iconpal}[sys.argv[1]]()
