#!/usr/bin/env python3
"""check_todo.py -- the record a fresh session reads first, checked (T-558).

Fails (exit 1) on any of:

  * an open ticket row (not struck through) below TODO.md's `## Closed` heading --
    sessions append to the end of the file, and the Fourth Review found eight such
    rows, the Fifth twenty-two;
  * a `Reserved: T-a to T-b` block whose ids are all taken (a stale claim);
  * a bible version stated in CLAUDE.md that is not the bible's own;
  * a "newest release" line in README.md or wiki/Home.md naming a release that is
    not the newest folder under `ROM RELEASE/`;
  * in daemons-eudaimonia's TODO.md (E-, 2026-11-20, C-411's first point), where it is linked in
    as eudaimonia/: a conflict marker, a malformed row, or an id twice;
  * in daemons-embodied's TODO.md (B-, 2026-11-25, T-617's question 8), where it is linked in as embodied/: the
    same three;
  * after the cut-over, any of the TODO files linked in here that is not Redmine's mirror.

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

# ---- daemons-eudaimonia's TODO.md (E-): one table, mirrored from Redmine like the companion's ------------------------
etodo = (ROOT / "eudaimonia").resolve() / "TODO.md"
if not etodo.exists():
    say("ok    no eudaimonia/TODO.md here (no eudaimonia/ link: a worktree or a fresh clone)")
else:
    e = etodo.read_text(encoding="utf-8").split("\n")
    marks = [i + 1 for i, l in enumerate(e) if re.match(r"^(<<<<<<<|=======|>>>>>>>)( |$)", l)]
    if marks:
        fail(f"{len(marks)} conflict-marker line(s) in eudaimonia/TODO.md, first at line {marks[0]}")
    bad = [l[:40] for l in e if re.match(r"\| (~~)?\*\*E-\d+\*\*(~~)? [^|]", l)]
    if bad:
        fail(f"{len(bad)} ticket row(s) missing the `|` after the id in eudaimonia/TODO.md: {bad[0]}...")
    ids = [m.group(1) for l in e for m in [re.match(r"\| (?:~~)?\*\*(E-\d+)\*\*", l)] if m]
    twice = sorted({k for k in ids if ids.count(k) > 1})
    if twice:
        fail(f"eudaimonia/TODO.md has an id twice: {' '.join(twice)}")
    elif not marks and not bad:
        say(f"ok    eudaimonia/TODO.md: {len(ids)} E- ticket(s), each once")

# ---- daemons-embodied's TODO.md (B-, 2026-11-25): one table, mirrored from Redmine like eudaimonia's -----------------
btodo = (ROOT / "embodied").resolve() / "TODO.md"
if not btodo.exists():
    say("ok    no embodied/TODO.md here (no embodied/ link: a worktree or a fresh clone)")
else:
    b = btodo.read_text(encoding="utf-8").split("\n")
    marks = [i + 1 for i, l in enumerate(b) if re.match(r"^(<<<<<<<|=======|>>>>>>>)( |$)", l)]
    if marks:
        fail(f"{len(marks)} conflict-marker line(s) in embodied/TODO.md, first at line {marks[0]}")
    bad = [l[:40] for l in b if re.match(r"\| (~~)?\*\*B-\d+\*\*(~~)? [^|]", l)]
    if bad:
        fail(f"{len(bad)} ticket row(s) missing the `|` after the id in embodied/TODO.md: {bad[0]}...")
    ids = [m.group(1) for l in b for m in [re.match(r"\| (?:~~)?\*\*(B-\d+)\*\*", l)] if m]
    twice = sorted({k for k in ids if ids.count(k) > 1})
    if twice:
        fail(f"embodied/TODO.md has an id twice: {' '.join(twice)}")
    elif not marks and not bad:
        say(f"ok    embodied/TODO.md: {len(ids)} B- ticket(s), each once")

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

# ---- the tickets' mirror (T-581) ------------------------------------------------------------------------------
# After the cut-over (the word `redmine` in ~/.local/share/daemons-tickets/truth) the ticket rows in the TODO files
# are Redmine's: a row edited by hand here would be overwritten by the nightly mirror, so the push stops on it.
import subprocess
truth_file = Path.home() / ".local/share/daemons-tickets/truth"
truth = truth_file.read_text().strip() if truth_file.exists() else "files"
if truth != "redmine":
    say("ok    tickets: the TODO files are still the truth (no mirror to check)")
elif not (Path.home() / ".redmine.env").exists():
    say("ok    tickets: no ~/.redmine.env here; the mirror is not checked")
else:
    r = subprocess.run([sys.executable, str(ROOT / "tools/tickets.py"), "mirror", "--from-redmine"],
                       capture_output=True, text=True, timeout=600)
    if r.returncode == 3:
        say("WARN  tickets: Redmine unreachable; the mirror is not checked")
    elif r.returncode != 0 or "differs" in r.stdout:
        fail("a TODO file is not Redmine's mirror: change tickets with tools/tickets.py, then "
             "`python3 tools/tickets.py mirror --from-redmine --write` (" + (r.stdout + r.stderr).strip()[:200] + ")")
    else:
        n = sum(1 for l in r.stdout.split("\n") if ": current" in l)
        say(f"ok    all {n} TODO files linked in here (of DAEMONS, the companion, eudaimonia, embodied) are Redmine's mirror")

if failures:
    print(f"\n{len(failures)} failure(s).")
    sys.exit(1)
print("check_todo: clean")
