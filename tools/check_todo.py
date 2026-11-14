#!/usr/bin/env python3
"""check_todo.py -- the record a fresh session reads first, checked (T-558).

Fails (exit 1) on any of:

  * an open ticket row (not struck through) below TODO.md's `## Closed` heading --
    sessions append to the end of the file, and the Fourth Review found eight such
    rows, the Fifth twenty-two;
  * a `Reserved: T-a to T-b` block whose ids are all taken (a stale claim);
  * a bible version stated in CLAUDE.md that is not the bible's own;
  * a "newest release" line in README.md or wiki/Home.md naming a release that is
    not the newest folder under `ROM RELEASE/`.

Run from the repo root. `--quiet` prints only failures.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
quiet = "--quiet" in sys.argv
failures = []


def say(msg):
    if not quiet:
        print(msg)


def fail(msg):
    failures.append(msg)
    print("FAIL  " + msg)


# ---- TODO.md ------------------------------------------------------------------
todo = (ROOT / "docs/TODO.md").read_text(encoding="utf-8").split("\n")
closed_at = next((i for i, l in enumerate(todo) if l.startswith("## Closed")), None)
if closed_at is None:
    fail("docs/TODO.md has no `## Closed` heading")
else:
    open_below = [
        re.match(r"\| \*\*(T-\d+)\*\*", l).group(1)
        for l in todo[closed_at:]
        if re.match(r"\| \*\*T-\d+\*\*", l) and "~~" not in l[:40]
    ]
    if open_below:
        fail(f"{len(open_below)} open row(s) below `## Closed` in docs/TODO.md: {' '.join(open_below)}")
    else:
        say("ok    no open row below Closed")

taken = set()
for l in todo:
    for m in re.finditer(r"\*\*T-(\d+)\*\*", l):
        taken.add(int(m.group(1)))
for l in todo:
    for m in re.finditer(r"Reserved: T-(\d+) to T-(\d+)", l):   # every block on the line, not the first
        lo, hi = int(m.group(1)), int(m.group(2))
        if all(i in taken for i in range(lo, hi + 1)):
            fail(f"reservation T-{lo} to T-{hi} is spent (every id taken) and still stands in docs/TODO.md")
        else:
            say(f"ok    reservation T-{lo} to T-{hi} still has free ids")

# conflict markers left by a merge (two blocks of them rode on the branch for a day, 2026-11-11)
markers = [i + 1 for i, l in enumerate(todo) if re.match(r"^(<<<<<<<|=======|>>>>>>>)( |$)", l)]
if markers:
    fail(f"{len(markers)} conflict-marker line(s) in docs/TODO.md, first at line {markers[0]}")

# malformed rows: an id cell with no closing pipe (T-519's, 2026-11-11)
bad = [l[:40] for l in todo if re.match(r"\| (~~)?\*\*T-\d+\*\*(~~)? [^|]", l)]
if bad:
    fail(f"{len(bad)} ticket row(s) missing the `|` after the id: {bad[0]}...")

# ---- the bible's version vs CLAUDE.md -------------------------------------------
vision = (ROOT / "docs/vision.md").read_text(encoding="utf-8")
vm = re.search(r"living design bible, v(\d+\.\d+)", vision)
bible = vm.group(1) if vm else None
claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
cm = re.search(r"carries a version \(v(\d+\.\d+)", claude)
if cm and bible and cm.group(1) != bible:
    fail(f"CLAUDE.md says the bible is v{cm.group(1)}; docs/vision.md is v{bible}")
elif cm:
    say(f"ok    CLAUDE.md and the bible agree on v{bible}")
else:
    say("ok    CLAUDE.md states no bible version (nothing to drift)")

# ---- the newest release ------------------------------------------------------------
def vkey(s):
    return [int(x) for x in re.findall(r"\d+", s)]


rel = ROOT / "ROM RELEASE"
groups = sorted((d.name for d in rel.iterdir() if d.is_dir() and re.match(r"v\d+\.\d+\.x$", d.name)), key=vkey)
newest = None
if groups:
    g = rel / groups[-1]
    rels = sorted((d.name for d in g.iterdir() if d.is_dir() and re.match(r"v\d+\.\d+\.\d+$", d.name)), key=vkey)
    newest = rels[-1] if rels else None
if newest:
    for f in ("README.md", "wiki/Home.md"):
        text = (ROOT / f).read_text(encoding="utf-8")
        m = re.search(r"(?:newest release is|the newest is) \*\*(v\d+\.\d+\.\d+)\*\*", text)
        if not m:
            say(f"ok    {f} has no newest-release line")
        elif m.group(1) != newest:
            fail(f"{f} says the newest release is {m.group(1)}; ROM RELEASE/ has {newest}")
        else:
            say(f"ok    {f} names {newest}")
else:
    say("ok    no release folders found (fresh clone?)")

if failures:
    print(f"\n{len(failures)} failure(s).")
    sys.exit(1)
print("check_todo: clean")
