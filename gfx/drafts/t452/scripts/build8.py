"""T-452 batch 8, BUILT (on the user's answers, 2026-10-27: PROMETHEUS's crimson crest, DEADLOCK as two, STARR's star, PUNCHCARD's holes,
mirrored backs, grounds off, two icons darker -- hand_b8.py): what
goes into gfx/daemons/.

    build8.py install    copy the chosen art into gfx/daemons/ (hand/ where hand4.py drew, else clean/ and reduced/)
    build8.py iconpal    print gMonIconPaletteIndices' rows for the 20 (icon3's palette), and with --write set them

Then, as batch 3: tools/gbasprite.py --write, scripts/ground.py --write SLOT..., tools/gbaowslots.py --write,
tools/gbafollowerpal.py --write. A daemon's file name is its INDEX art's ."""
import json, os, re, shutil, sys
R = "/Users/christopherhicks/Projects/DAEMONS"; F = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452") + "/k"; OUT = R + "/gfx/daemons"
NAMES = ["drum", "punchcard", "fossilnet", "deadlock", "orpheus", "asclepius", "prometheus", "canary", "emergence", "singular",
         "starr", "primer", "syllabus", "curriculum", "tepid", "seethe", "heatdeath", "learnrate", "momentum", "steepest"]
P = json.load(open(F + "/picks.json"))

def install():
    for n in NAMES:
        fn = n.replace(" ", "_")
        for k, d in (("front", "clean"), ("back", "clean"), ("icon", "reduced")):
            h = f"{F}/hand/{n}_{k}.png"; s = h if os.path.exists(h) else f"{F}/{d}/{n}_{k}.png"
            shutil.copyfile(s, f"{OUT}/{fn}_{k}.png"); print("%-34s -> gfx/daemons/%s_%s.png" % (os.path.relpath(s, F), fn, k))

def iconpal():
    f = R + "/engineGba/src/pokemon_icon.c"; t = open(f).read()
    for n in NAMES:
        slot = P[n]["slot"].upper(); pi = P[n]["measured"]["icon3"]["icon_palette"]
        pat = re.compile(r"(\[SPECIES_%s\]\s*= )(\d)(,)" % slot)
        m = list(pat.finditer(t))[-1]
        print("%-10s %-12s %s -> %d" % (n, slot, m[2], pi))
        t = t[:m.start(2)] + str(pi) + t[m.end(2):]
    if "--write" in sys.argv: open(f, "w").write(t)

if __name__ == "__main__":
    {"install": install, "iconpal": iconpal}[sys.argv[1]]()
