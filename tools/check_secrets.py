#!/usr/bin/env python3
"""check_secrets.py -- the four things that never go in public writing, grepped for (T-560).

CLAUDE.md names four secrets the game asks the player to work out. They live in docs/private/ (gitignored). The
2026-09-27 redaction swept them out of the tracked files once; by 2026-11-04 three of the four were readable again
in five files. This check keeps that from happening a third time.

It reads its patterns from `docs/private/secrets_patterns.txt` -- one regular expression per line, `#` comments,
`## <label>` headings naming the section each pattern belongs to -- and greps every tracked text file. On a hit it
prints the file, the line number and the section label, NEVER the matched text (a check that quoted the secret
into a log would be the leak). Where the patterns file is absent (a fresh clone, a cloud session, a worktree) it
passes quietly and says so: the check cannot carry the patterns itself, because the patterns are the secrets.

Run from the repo root; `--quiet` prints only failures. It is in the push routine's step 2.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = ROOT / "docs/private/secrets_patterns.txt"
TEXT = {".md", ".txt", ".json", ".html", ".css", ".py", ".sh", ".inc", ".c", ".h", ".s", ".yml", ".yaml", ".toml", ".mk", ".tex"}
quiet = "--quiet" in sys.argv

if not PATTERNS.exists():
    print("check_secrets: no docs/private/secrets_patterns.txt here (a fresh clone, a cloud session or a worktree); "
          "nothing checked. Run it where docs/private/ is.")
    sys.exit(0)

patterns = []
label = "SECRETS"
for raw in PATTERNS.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line:
        continue
    if line.startswith("## "):
        label = line[3:].strip()
        continue
    if line.startswith("#"):
        continue
    try:
        patterns.append((label, re.compile(line)))
    except re.error as e:
        print(f"FAIL  bad pattern under {label}: {e}")
        sys.exit(1)

files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
hits = []
for rel in files:
    if not rel or Path(rel).suffix.lower() not in TEXT or rel.startswith("docs/private/"):
        continue
    p = ROOT / rel
    if not p.is_file():
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for n, line in enumerate(text.split("\n"), 1):
        for lab, rx in patterns:
            if rx.search(line):
                hits.append((rel, n, lab))
                break

if hits:
    for rel, n, lab in hits:
        print(f"FAIL  {rel}:{n}  states {lab}")
    print(f"\n{len(hits)} line(s) state a secret in a tracked file. Sweep each to a [private: SECRETS §n] marker.")
    sys.exit(1)
if not quiet:
    print(f"check_secrets: clean ({len(patterns)} patterns, {sum(1 for f in files if f)} tracked files)")
