#!/usr/bin/env python3
"""Convert a daemon's art by OUR name, resolving the vanilla slot itself.

    python3 tools/sprite.py crawler
    python3 tools/sprite.py crawler --cover=0.8

Reads gfx/front/<name>.png and gfx/back/<name>-back.png, works out which
vanilla slot that daemon occupies, reads the target size off the existing
.pic, and writes both. You never type a vanilla filename.

The engine keeps pret's filenames on purpose: they are identifiers, and
renaming them would make `git pull upstream master` conflict on every gfx
rule forever. So the mapping is derived, not written down -- from
constants/pokemon_constants.asm (name -> internal index) and
data/pokemon/names.asm (internal index -> our name). It cannot go stale.

    python3 tools/sprite.py --list        every renamed daemon and its slot
"""
import sys, os, re, subprocess, tempfile, glob as _glob

# Per-daemon --cover, measured rather than guessed. Thin art wants a HIGHER
# bar: less ink means the darkest-wins pass fires on cells the outline merely
# grazes. Art that is made of ink (CLUSTR is a field of dots) wants no pass at
# all -- 1.01 disables it. Without this table the tool silently degrades
# sprites that were already tuned, which it did to ROVERCUB the first time it
# ran. Front and back can differ; give a tuple to split them.
COVER = {
    "ROVERCUB":  (0.6, 0.9),
    "ROVERSEER": 0.6,
    "ROVERBYTE": 0.6,
    "LABL":      0.9,
    "RUBRIC":    (0.6, 0.75),
    "CANON":     (0.5, 0.75),
    "CLUSTR":    1.01,
    "LOCUS":     0.75,
    "MANIFOLD":  0.6,
    "MUSAI":     0.7,
    "CODEMUSAI": 0.7,
    "SEEKMUSAI": 0.7,
    "CAREMUSAI": 0.7,
    "STARR":     (0.34, 0.7),
    # The nine wild daemons arrived as JPEG, and lossy compression already
    # blurs a hard outline into intermediate values -- so darkest-wins fires on
    # the compression halo and blackens whatever it touches. Six of the nine
    # want the pass disabled entirely. Measured by sweeping cover and keeping
    # the flattest ink distribution, not guessed.
    "NIBBLE":    (0.6, 0.34),
    "PACKET":    0.6,
    "PING":      1.01,
    "CRAWLER":   1.01,
    "PENDING":   (1.01, 0.6),
    "SCRAPER":   (1.01, 0.6),
    "BUFFER":    0.6,
    "SPIKE":     1.01,
    "SUSPEND":   0.34,
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG  = os.path.join(ROOT, "engine")

def mapping():
    """our name -> (vanilla const, front png, back png, front size, back size)"""
    # const_def starts at 0 and the first entry is NO_MON, so RHYDON is 1 and
    # names.asm's first dname lines up with it. Counting from 1 on the first
    # const shifts the whole table by one and silently maps every daemon to
    # its neighbour's sprite.
    # Two traps. const_def starts at 0 and the first entry is NO_MON, so RHYDON
    # is 1. And the file uses const_skip for the MissingNo slots, which still
    # occupy an index and still have a dname in names.asm -- counting only the
    # named consts silently maps every daemon past the first gap to a
    # neighbour's sprite, which is exactly what this tool exists to prevent.
    idx = {}
    n = 0
    for ln in open(os.path.join(ENG, "constants/pokemon_constants.asm")):
        if re.match(r'\s*const_skip', ln):
            n += 1
            continue
        m = re.match(r'\s*const\s+([A-Z0-9_]+)', ln)
        if m:
            idx[n] = m.group(1)
            n += 1
    names = []
    for ln in open(os.path.join(ENG, "data/pokemon/names.asm")):
        m = re.match(r'\s*dname "(.+)"', ln)
        if m:
            names.append(m.group(1))
    out = {}
    for i, ours in enumerate(names, 1):
        const = idx.get(i)
        if not const:
            continue
        stem = const.lower().replace("_", "")
        f = "gfx/pokemon/front/%s.png" % stem
        if not os.path.exists(os.path.join(ENG, f)):
            continue
        b = "gfx/pokemon/back/%sb.png" % stem
        def size(pic):
            p = os.path.join(ENG, pic)
            if not os.path.exists(p):
                return None
            d = open(p, "rb").read(1)[0]
            return (d >> 4) * 8
        out[ours] = (const, f, b, size(f[:-4] + ".pic"), size(b[:-4] + ".pic"))
    return out

def main():
    M = mapping()
    if "--list" in sys.argv:
        van = {n for n in M if n == M[n][0]}
        print("%-12s %-12s %-34s %s" % ("OURS", "SLOT", "FRONT", "SIZE"))
        for ours in sorted(M):
            const, f, b, fs, bs = M[ours]
            if ours == const:
                continue          # still vanilla, not ours yet
            print("%-12s %-12s %-34s %sx%s / %sx%s" % (ours, const, f, fs, fs, bs, bs))
        return
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    key = name.upper()
    if key not in M:
        sys.exit("no daemon named %s in names.asm -- rename the species first" % key)
    const, f, b, fs, bs = M[key]
    print("  %s -> %s  (front %sx%s, back %sx%s)" % (key, const, fs, fs, bs, bs))
    given = [a for a in sys.argv[2:] if a.startswith("--")]
    tuned = COVER.get(key)
    def find(pattern):
        # Generators hand back .jpeg as readily as .png. Take whatever is there.
        hits = _glob.glob(os.path.join(ROOT, pattern))
        return hits[0] if hits else None
    for which, (src, dst, sz) in enumerate(
                        ((find("gfx/front/%s.*" % name.lower()),
                          os.path.join(ENG, f), fs),
                         (find("gfx/back/%s-back.*" % name.lower()),
                          os.path.join(ENG, b), bs))):
        extra = list(given)
        if tuned is not None and not any(a.startswith("--cover") for a in extra):
            c = tuned[which] if isinstance(tuned, tuple) else tuned
            extra.append("--cover=%.2f" % c)
        if not src or not os.path.exists(src):
            print("     skipped, no source")
            continue
        if not src.lower().endswith(".png"):
            # mksprite reads PNG only. Convert losslessly to a temp file rather
            # than rewriting the source, so the original art stays as delivered.
            tmp = os.path.join(tempfile.gettempdir(),
                               os.path.basename(src).rsplit(".", 1)[0] + ".png")
            subprocess.run(["sips", "-s", "format", "png", src, "--out", tmp],
                           capture_output=True)
            src = tmp
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools/mksprite.py"),
                            src, dst, str(sz)] + extra, capture_output=True, text=True)
        print("     " + (r.stdout.strip().splitlines() or ["failed: " + r.stderr.strip()])[-1].strip())

main()
