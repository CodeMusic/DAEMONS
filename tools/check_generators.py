#!/usr/bin/env python3
"""Every generator must still RUN (T-213).

    python3 tools/check_generators.py            # run all of them in report mode; exit 1 if any fails
    python3 tools/check_generators.py gbasprite  # just the ones whose name contains that
    python3 tools/check_generators.py --times    # also print how long each took

T-212 sat broken for a day because a generated file is correct on disk whether or not the thing that wrote it
still works. check_lexicon reads ARTIFACTS, so it had nothing to say about a tool that raised IndexError the
moment it was called -- and the only reason that one surfaced at all was that somebody needed to extend it.

So this runs every tool in tools/ that has a --write mode, WITHOUT --write, and holds each to three things:

    1. it exits 0                  a report that crashes is a generator that cannot regenerate
    2. it finishes in LIMIT s      a check nobody can afford to run is not a check
    3. it changes nothing          report mode that writes is a trap: the next "dry run" edits the build

Which tools: every one with a --write mode, found by reading them, not a list kept by hand -- a subset chosen by
hand is the same class of thing that broke. A tool excused below says why in one line, and the excuse is itself
checked: an excused tool that starts passing is reported, so nothing stays excused out of habit.
"""
import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
LIMIT = 180
SELF = os.path.basename(__file__)

#  name -> why it may not pass in report mode. Keep this short; every line is a tool nobody is watching.
EXCUSED = {
    #  ONE-SHOT MIGRATIONS: each asserts the vanilla state it converts, and that state is gone because it ran.
    "gbaground":  "one-shot: re-cut Kanto's ground tiles; asserts the tileset ends at vanilla's 160",
    "gbahouses":  "one-shot: redrew the towns' houses; asserts Pallet still draws vanilla's row 11",
    "gbamapedit": "one-shot: T-71's first Route 1 edit; asserts the grass it put a pond on",
    "gbascholar": "one-shot: the Owl's study in Brazen; asserts the house it replaced",
    #  TRANSCRIBERS, not generators: each needs an audio file named on the command line.
    "mp3midi":    "a transcriber: needs an .mp3 to read",
    "stems2midi": "a transcriber: needs a directory of stems",
}

#  Tools that generate one named thing at a time are run once per thing, all of them.
ARGS = {
    "genanims":  [[f] for f in ("CONTENT LOWER AFFLICT RAISE FIELD LOGIC VECTOR GROWTH FLOW ENTROPY STRATUM SIGNAL "
                                "CORRUPT CONTEXT SWARM FROZEN PROTECT OPAQUE LATENT").split()],
    "genstates": [["--wave", "1"]],
}


def generators(only):
    out = []
    for f in sorted(os.listdir(TOOLS)):
        if not f.endswith(".py") or f == SELF:
            continue
        src = open(os.path.join(TOOLS, f), encoding="utf-8", errors="ignore").read()
        if "--write" not in src or "__main__" not in src and "sys.exit(main())" not in src and "main()" not in src:
            continue
        if only and not any(o in f for o in only):
            continue
        out.append(f)
    return out


def dirty():
    """Every changed or untracked path in both repos -- a report-mode run must leave this unchanged."""
    seen = set()
    for repo in (ROOT, os.path.join(ROOT, "engineGba")):
        r = subprocess.run(["git", "-C", repo, "status", "--porcelain", "-uall"], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            path = line[3:]
            st = os.path.join(repo, path)
            try:
                seen.add((repo, path, os.path.getmtime(st), os.path.getsize(st)))
            except OSError:
                seen.add((repo, path, None, None))
    return seen


def run(f):
    t0 = time.time()
    code, last = 0, ""
    for extra in ARGS.get(f[:-3], [[]]):
        try:
            r = subprocess.run([sys.executable, os.path.join(TOOLS, f)] + extra, cwd=ROOT, capture_output=True,
                               text=True, timeout=LIMIT, stdin=subprocess.DEVNULL)
            out = (r.stderr.strip() or r.stdout.strip()).splitlines()
            if r.returncode != 0:
                code, last = r.returncode, " ".join(extra) + ": " + (out[-1] if out else "")
                break
        except subprocess.TimeoutExpired:
            code, last = "timeout", "did not finish in %ds" % LIMIT
            break
    return f, code, time.time() - t0, last


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tools = generators(args)
    before = dirty()
    #  Serial, because several of these read and rewrite the same trees and a parallel run would make rule 3
    #  unanswerable -- which tool touched the file?
    bad, results = [], []
    for f in tools:
        b0 = dirty()
        f, code, secs, last = run(f)
        wrote = sorted(p for (_, p, _, _) in (dirty() - b0))
        results.append((f, code, secs))
        name = f[:-3]
        fail = None
        if code != 0:
            fail = "exit %s: %s" % (code, last[:120])
        elif wrote:
            fail = "wrote in report mode: %s" % ", ".join(wrote[:4])
        if name in EXCUSED:
            if fail is None:
                bad.append((f, "passes now -- take it out of EXCUSED (%s)" % EXCUSED[name]))
            continue
        if fail:
            bad.append((f, fail))
        if "--times" in sys.argv:
            print("  %6.1fs  %s" % (secs, f))
    if dirty() != before:
        bad.append(("(all)", "the trees changed during the run"))
    total = sum(s for _, _, s in results)
    if bad:
        print("  %d of %d generators do not run cleanly in report mode:" % (len(bad), len(tools)))
        for f, why in bad:
            print("     %-30s %s" % (f, why))
        return 1
    print("  all %d generators run in report mode, exit 0, and write nothing; %d excused, each with its reason (%.0fs)."
          % (len(tools) - sum(1 for f in tools if f[:-3] in EXCUSED), sum(1 for f in tools if f[:-3] in EXCUSED), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
