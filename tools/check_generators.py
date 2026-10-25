#!/usr/bin/env python3
"""Every generator must still RUN (T-213).

    python3 tools/check_generators.py            # run all of them in report mode; exit 1 if any fails
    python3 tools/check_generators.py gbasprite  # just the ones whose name contains that
    python3 tools/check_generators.py --times    # also print how long each took
    python3 tools/check_generators.py --writes   # run every tool's --write in a sandbox (T-292, below)

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
    #  (gbahouses, gbamapedit and gbascholar went to tools/archive/ in T-421, which this does not scan.)
    "gbaground":  "one-shot: re-cut Kanto's ground tiles; asserts the tileset ends at vanilla's 160",
    #  TRANSCRIBERS, not generators: each needs an audio file named on the command line.
    "mp3midi":    "a transcriber: needs an .mp3 to read",
    "stems2midi": "a transcriber: needs a directory of stems",
}

#  Tools that generate one named thing at a time are run once per thing, all of them.
#  gbadocs places only the documents its --text file holds, and that file is private: run without it, its write takes
#  every placed page out of the world -- which is not drift (found 2026-10-15).
_DOCS_TEXT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "private", "notebook_docs.json")
ARGS = {
    "gbadocs":   [["--text", _DOCS_TEXT]] if os.path.exists(_DOCS_TEXT) else [],
    "genanims":  [[f] for f in ("CONTENT LOWER AFFLICT RAISE FIELD LOGIC VECTOR GROWTH FLOW ENTROPY STRATUM SIGNAL "
                                "CORRUPT CONTEXT SWARM FROZEN PROTECT OPAQUE LATENT").split()],
    "genstates": [["--wave", "1"]],
    #  T-446: gbadoors refuses a plain --write, so --writes saw nothing of it; with --approved its sandboxed write is
    #  real. (Its report needs no flag: it compares the engine with the approved write itself and exits 1 on a difference.)
    "gbadoors":  [["--approved"]],
}
#  A tool given no runs above is SKIPPED, and says so (T-421): gbadocs used to vanish from the count without a word.
SKIPPED = {name: "docs/private/notebook_docs.json is missing (private, not in git), and gbadocs without it is not a check"
           for name in ("gbadocs",) if ARGS.get(name) == []}


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


#  T-421: a report-mode preview goes to /tmp/<name> unless DAEMONS_PREVIEW_DIR says otherwise (daemonslib.preview),
#  so this run's previews go to a directory of its own, removed at exit -- not over another session's /tmp/<name>.
_PREVIEWS = None


def preview_env():
    global _PREVIEWS
    if _PREVIEWS is None:
        import atexit, shutil, tempfile
        _PREVIEWS = tempfile.mkdtemp(prefix="check_generators-previews-")
        atexit.register(shutil.rmtree, _PREVIEWS, True)
    return dict(os.environ, DAEMONS_PREVIEW_DIR=_PREVIEWS)


def run(f):
    t0 = time.time()
    code, last = 0, ""
    for extra in ARGS.get(f[:-3], [[]]):
        try:
            r = subprocess.run([sys.executable, os.path.join(TOOLS, f)] + extra, cwd=ROOT, capture_output=True,
                               text=True, timeout=LIMIT, stdin=subprocess.DEVNULL, env=preview_env())
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
        if f[:-3] in SKIPPED:
            print("  skipped %s: %s" % (f, SKIPPED[f[:-3]]))
            continue
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
    skipped = sum(1 for f in tools if f[:-3] in SKIPPED)
    excused = sum(1 for f in tools if f[:-3] in EXCUSED)
    print("  all %d generators run in report mode, exit 0, and write nothing; %d excused, each with its reason%s (%.0fs)."
          % (len(tools) - excused - skipped, excused, "; %d SKIPPED (above)" % skipped if skipped else "", total))
    return 0


# ---------------------------------------------------------------------------------------------------------------------
# --writes: EVERY TOOL'S WRITE, FOR REAL, IN A SANDBOX (2026-09-25, T-292).
#
# Report mode proves a tool still runs; it proves nothing about the write. gbaowslots.py --write stopped at a NameError
# for four days while its report passed (engine.md trap 34), and port_hearsay.py --write would quietly undo later work
# -- TM for PLUGIN, "Freezing" for FROZEN, the leaders' music cues -- because a tool's output is layered over by later
# passes and nothing compares the two (trap 32). So this makes a throwaway worktree of BOTH repos, runs every tool's
# --write there, one at a time, and resets between them. Two things are held:
#
#   CRASH  a traceback. A refusal with its own message (a one-shot that is already done) is not a crash.
#   DRIFT  the files the write would change. Drift is not always wrong -- a tool can be stale, or right about files
#          that drifted from it -- so it is compared with tools/generator_drift.json, the known state, which says for
#          each drifting tool which files and why. NEW drift fails; drift that has gone is reported, to update the file.
#
# A tool in generator_drift.json must not be run with --write on the whole tree: read what it would change first.

SANDBOX = os.path.expanduser("~/.cache/daemons/writes-sandbox")
DRIFT = os.path.join(TOOLS, "generator_drift.json")
#  Tools the sandbox cannot hold: each needs something a fresh worktree does not have. One line each.
SANDBOX_EXCUSED = {
    "romrelease":    "builds all four ROMs and files a release",
    "port_gamedata": "writes into the AI playtester's fork (engineAi), which is never sandboxed",
    "port_prompts":  "writes into the AI playtester's fork (engineAi), which is never sandboxed",
    "check_reach":   "a check, not a generator",
}


def sandbox():
    """Fresh detached worktrees of both repos at HEAD, linked as setup.sh links the real ones, with the engine's built
    helpers and link maps copied in (all gitignored, so a reset leaves them)."""
    import shutil
    d, e = os.path.join(SANDBOX, "docs"), os.path.join(SANDBOX, "engine")
    eng = os.path.realpath(os.path.join(ROOT, "engineGba"))
    for repo, path in ((ROOT, d), (eng, e)):
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", path], capture_output=True)
        subprocess.run(["git", "-C", repo, "worktree", "prune"], capture_output=True)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        subprocess.run(["git", "-C", repo, "worktree", "add", "--detach", path, "HEAD"], check=True, capture_output=True)
    #  engineAi is only READ by the tools sandboxed here (gbadreams reads its progress steps) -- the real fork is linked,
    #  and the two that write it are SANDBOX_EXCUSED (found 2026-10-15: gbadreams crashed without it).
    for link, target in (("engineGba", e), ("engine", os.path.realpath(os.path.join(ROOT, "engine"))),
                         ("engineAi", os.path.realpath(os.path.join(ROOT, "engineAi")))):
        if os.path.exists(target):
            os.symlink(target, os.path.join(d, link))
    for t in os.listdir(os.path.join(eng, "tools")):
        b = os.path.join(eng, "tools", t, t)
        if os.path.isfile(b) and os.access(b, os.X_OK):
            shutil.copy2(b, os.path.join(e, "tools", t, t))
    #  agbcc installs INTO the engine's tools/ and is gitignored, so a worktree has none; gbabudget measures the save
    #  blocks with it and, without it, silently dropped engine.md's whole save table (found 2026-10-15).
    if os.path.isdir(os.path.join(eng, "tools", "agbcc")) and not os.path.exists(os.path.join(e, "tools", "agbcc")):
        os.symlink(os.path.join(eng, "tools", "agbcc"), os.path.join(e, "tools", "agbcc"))
    #  T-421: the build writes ten headers from json (map_groups.h, layouts.h, region_map_sections.h, items.h ...) and
    #  gitignores them, so a worktree has none -- companion_export and genholidays crashed on map_groups.h. Made here
    #  as the build makes them, from the worktree's own json, by the helpers just copied in (`make generated`); they
    #  are ignored files, so a reset keeps them.
    subprocess.run(["make", "-C", e, "generated", "-j8"], check=True, capture_output=True)
    for f in os.listdir(eng):
        if f.startswith("daemonsCont") and f.endswith((".map", ".elf", ".gba")):
            shutil.copy2(os.path.join(eng, f), os.path.join(e, f))
    return d, e


def writes():
    import json
    d, e = sandbox()
    known = json.load(open(DRIFT)) if os.path.exists(DRIFT) else {}
    def reset():
        for r in (d, e):
            subprocess.run(["git", "-C", r, "checkout", "--", "."], capture_output=True)
            subprocess.run(["git", "-C", r, "clean", "-fdq", "-e", "engineGba", "-e", "engine", "-e", "engineAi", "-e", "tools/agbcc"], capture_output=True)
    crashes, drift, t0 = [], {}, time.time()
    for f in generators([]):
        name = f[:-3]
        if name in EXCUSED or name in SANDBOX_EXCUSED:
            continue
        if name in SKIPPED:
            print("  skipped %s: %s" % (name, SKIPPED[name]))
            continue
        for extra in ARGS.get(name, [[]]):
            reset()
            try:
                #  --over-later-work: a tool the record marks STALE refuses a plain --write now (driftguard.py, T-293),
                #  and this is the one place that must see what it WOULD do, to keep the record true.
                r = subprocess.run([sys.executable, os.path.join(d, "tools", f)] + extra + ["--write", "--over-later-work"], cwd=d,
                                   capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL,
                                   env=preview_env())
                if "Traceback (most recent call last)" in r.stderr:
                    crashes.append((name, extra, r.stderr.strip().splitlines()[-1]))
            except subprocess.TimeoutExpired:
                crashes.append((name, extra, "did not finish in 600s"))
            #  A change of line endings alone is not drift: the engine's .gitattributes asks CRLF of every .pal, and a
            #  tool that writes LF would read as drifting on every run (found 2026-10-15). So: content changes, and
            #  new files -- not git status.
            for repo, tag in ((d, "docs"), (e, "engine")):
                changed = subprocess.run(["git", "-C", repo, "diff", "--ignore-cr-at-eol", "--name-only"],
                                         capture_output=True, text=True).stdout.splitlines()
                new_files = subprocess.run(["git", "-C", repo, "ls-files", "--others", "--exclude-standard"],
                                           capture_output=True, text=True).stdout.splitlines()
                for path in changed + new_files:
                    if path not in ("engineGba", "engine", "engineAi"):
                        drift.setdefault(name, set()).add("%s:%s" % (tag, path))
    reset()
    new = {n: sorted(fs - set(known.get(n, {}).get("files", []))) for n, fs in drift.items()}
    new = {n: fs for n, fs in new.items() if fs}
    #  a tool that is never sandboxed cannot be seen to drift, so its entry stays (port_prompts, T-319)
    unseen = set(EXCUSED) | set(SANDBOX_EXCUSED)
    gone = sorted(n for n in known if n not in drift and n not in unseen)
    for n, extra, last in crashes:
        print("  !! %s%s --write crashes: %s" % (n, (" " + " ".join(extra)) if extra else "", last[:140]))
    for n, fs in sorted(new.items()):
        print("  !! %s --write would change what generator_drift.json does not know: %s" % (n, ", ".join(fs[:4])))
    for n in gone:
        print("  %s no longer drifts -- take it out of generator_drift.json" % n)
    print("  %d tools' writes run in a sandbox (%.0fs): %d crash, %d drift as known, %d drift anew"
          % (len(generators([])) - len(EXCUSED) - len(SANDBOX_EXCUSED), time.time() - t0, len(crashes),
             sum(1 for n in drift if n in known), len(new)))
    if "--record" in sys.argv:
        out = {n: {"why": known.get(n, {}).get("why", "UNREVIEWED"), "files": sorted(fs)} for n, fs in sorted(drift.items())}
        out.update({n: known[n] for n in known if n in unseen and n not in out})
        json.dump(out, open(DRIFT, "w"), indent=1, ensure_ascii=False)
        open(DRIFT, "a").write("\n")
        print("  recorded %d drifting tools in generator_drift.json" % len(out))
    return 1 if crashes or new else 0


if __name__ == "__main__":
    sys.exit(writes() if "--writes" in sys.argv else main())
