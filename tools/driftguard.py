#!/usr/bin/env python3
"""A tool whose --write would undo later work refuses to run it on the whole tree (T-293, 2026-09-25).

T-292 ran every tool's --write in a sandbox and found 24 that would change committed files. Some were brought level:
the tool learned what the later pass did (gbaoutline's outline, a released animation left alone, CRLF palettes).
The rest cannot be: their files carry hand work done after they last ran -- a paw redrawn on a back picture, a map
re-edited, a line rewritten -- and no tool knows it. Running one of those over the tree takes that work off again
(engine.md trap 32), and CLAUDE.md telling you to look first is a guard only for someone who reads it.

So each of them calls this first. The reason lives in ONE place, tools/generator_drift.json, which
`check_generators.py --writes` keeps honest: a tool marked STALE there refuses a whole-tree --write and says why.

    refuse_over_later_work("gbaroutes")               # at the top of the tool's main
    refuse_over_later_work("gbachar", named=bool(jobs))  # a tool that can be pointed at named jobs lets those run

`--over-later-work` writes anyway -- for the sandbox audit, or when you mean to, and then read `git diff` before
anything else.
"""
import json, os, sys

DRIFT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generator_drift.json")
OVERRIDE = "--over-later-work"


def refuse_over_later_work(name, named=False):
    if "--write" not in sys.argv or named or OVERRIDE in sys.argv:
        return
    known = json.load(open(DRIFT)).get(name) if os.path.exists(DRIFT) else None
    if not known or not known.get("why", "").startswith("STALE"):
        return
    files = known.get("files", [])
    raise SystemExit("  refused: %s --write would change %d committed file%s (%s%s) and undo later work.\n"
                     "  generator_drift.json: %s\n"
                     "  %s writes anyway -- then read git diff before anything else."
                     % (name, len(files), "" if len(files) == 1 else "s", ", ".join(f.split(":", 1)[1] for f in files[:3]),
                        ", ..." if len(files) > 3 else "", known["why"], OVERRIDE))
