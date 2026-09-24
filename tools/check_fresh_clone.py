#!/usr/bin/env python3
"""Does a fresh clone build the ROM this machine built? (2026-09-24)

    python3 tools/check_fresh_clone.py            # clone the engine from GitHub, build both editions, compare
    python3 tools/check_fresh_clone.py --keep     # and leave the clone behind to look at

WHY. Twice this project shipped a change that lived only in a gitignored, generated file: sixteen town names in
region_map_entry_strings.h (CLAUDE.md), and the kind of edit engine.md's traps keep catching. A generated file stays
right on disk long after its source has stopped producing it, and nothing on this machine can tell -- the only
proof is a build from what is actually PUSHED. So this clones the engine's branch from origin into a temporary
directory, borrows this machine's agbcc (it installs into tools/ and never survives a clone), builds CONTENT and
CONTEXT, and compares each byte for byte with the ROMs in engineGba/.

It reports; it never writes into either repo. Run it before a release that will be published. A mismatch means
something the build needs is not in git, or the local tree is ahead of origin -- the report says which commit
each side is at, so the second is easy to rule out. About five minutes.
"""
import hashlib, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.realpath(os.path.join(ROOT, "engineGba"))
KEEP = "--keep" in sys.argv


def git(*args, cwd=GBA):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True).stdout.strip()


def sha1(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None


def main():
    url, branch = git("remote", "get-url", "origin"), git("rev-parse", "--abbrev-ref", "HEAD")
    local = git("rev-parse", "--short=9", "HEAD")
    tmp = tempfile.mkdtemp(prefix="daemons-fresh-")
    dest = os.path.join(tmp, "engine")
    print("  cloning %s (%s) ..." % (url, branch))
    if subprocess.run(["git", "clone", "-q", "-b", branch, url, dest]).returncode:
        raise SystemExit("  the clone failed")
    pushed = git("rev-parse", "--short=9", "HEAD", cwd=dest)
    os.symlink(os.path.join(GBA, "tools/agbcc"), os.path.join(dest, "tools/agbcc"))
    ok = True
    for target, rom in (("firered", "daemonsContent.gba"), ("leafgreen", "daemonsContext.gba")):
        r = subprocess.run(["make", "-C", dest, target, "-j8"], capture_output=True, text=True)
        if r.returncode:
            print("  !! `make %s` FAILED in the fresh clone -- something the build needs is not in git:\n%s"
                  % (target, (r.stdout + r.stderr)[-1500:]))
            ok = False
            continue
        a, b = sha1(os.path.join(dest, rom)), sha1(os.path.join(GBA, rom))
        same = a == b
        ok &= same
        print("  %-20s %s" % (rom, "identical to this machine's build" if same else
                               "DIFFERS  (fresh %s, local %s)" % (a[:12], (b or "none")[:12])))
    print("  origin is at %s, this machine at %s%s" % (pushed, local, "" if pushed == local else
                                                        "  -- not the same commit, so a difference may only be that"))
    if KEEP:
        print("  kept: %s" % dest)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    print("  %s" % ("a fresh clone builds the same two ROMs." if ok else "!! the pushed engine does not build what this machine built"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
