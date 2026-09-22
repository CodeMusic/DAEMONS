#!/usr/bin/env python3
"""A PLUGIN should say what its routine does, in our words (T-183a; vision.md 1.6).

    python3 tools/port_plugin_text.py            # report
    python3 tools/port_plugin_text.py --write     # into src/data/items.json

WHAT THIS FOUND. The TOOLKIT prints the ITEM's description (`ItemId_GetDescription`, tm_case.c) and not the
routine's -- so all fifty PLUGINs and eight DRIVERs described themselves in VANILLA'S prose, on a screen
whose every other word is ours. PLUGIN02 said "Sharp, huge claws hook and slash the foe quickly and with
great power" while the routine it teaches says "A problem cut down to a smaller one."

It is also where 32 of the last "foe"s in the game were living, which is how it was noticed at all: T-183
swept the routine descriptions, the ability descriptions and the help system, and this is a fourth surface
nobody had looked at.

THE FIX IS NOT TO WRITE FIFTY MORE DESCRIPTIONS. The routine already has one, rewritten and fitted, and a
PLUGIN is the routine -- so the item takes the routine's own words and cannot drift from them again.

THE PANE IS WIDER HERE, which is why this is a copy and not a rewrap: tm_case.c's WIN_DESCRIPTION is
eighteen tiles (144px) against the summary screen's fifteen, and our routine lines are cut to 113.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv


def tmhm_moves():
    src = open(os.path.join(GBA, "src/data/party_menu.h"), encoding="utf-8").read()
    body = re.search(r'static const u16 sTMHMMoves\[\]\s*=\s*\{(.*?)\n\};', src, re.S).group(1)
    return re.findall(r'MOVE_(\w+)', body)


def move_descriptions():
    src = open(os.path.join(GBA, "src/move_descriptions.c"), encoding="utf-8").read()
    by_symbol = {}
    for m in re.finditer(r'const u8 gMoveDescription_(\w+)\[\] = _\((.*?)\);', src, re.S):
        by_symbol[m.group(1)] = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
    out = {}
    for m in re.finditer(r'\[MOVE_(\w+)\s*-\s*1\]\s*=\s*gMoveDescription_(\w+)', src):
        if m.group(2) in by_symbol:
            out[m.group(1)] = by_symbol[m.group(2)]
    return out


def words(text):
    return " ".join(text.replace("\\n", " ").split())


def main():
    moves, descs = tmhm_moves(), move_descriptions()
    p = os.path.join(GBA, "src/data/items.json")
    d = json.load(open(p, encoding="utf-8"))
    items = d["items"] if isinstance(d, dict) and "items" in d else d
    changed = missing = 0
    for it in items:
        iid = str(it.get("itemId", ""))
        m = re.fullmatch(r"ITEM_(?:TM(\d\d)|HM(\d\d))(?:_\w+)?", iid)
        if not m:
            continue
        n = int(m.group(1) or 0) - 1 if m.group(1) else 49 + int(m.group(2))
        if not (0 <= n < len(moves)):
            continue
        want = descs.get(moves[n])
        if not want:
            missing += 1
            continue
        #  `want` already holds the line break as the two characters backslash-n, exactly as the C
        #  literal does, and json.dumps escapes the backslash on the way out. Escaping it again here
        #  put a real backslash in the generated header and agbcc said "no mapping exists for
        #  backslash", which is a charmap error rather than a C one and reads like neither.
        #  COMPARE THE WORDS, NOT THE BREAKS. The routine's text is wrapped for the summary pane (113px, four
        #  lines); the TOOLKIT pane is vanilla's three lines at up to 198px, and port_vocab reflows these to
        #  fit it. Comparing the raw strings called every reflowed description "drifted" -- all 44 of them,
        #  2026-09-22 -- and re-copying them UNDID the reflow and left each one a line too long. The words
        #  had not changed at all. So: same words, leave it alone; different words, copy, and say to reflow.
        if words(it.get("description_english", "")) != words(want):
            print("  %-12s %-14s %s" % (it["english"], moves[n], want.replace("\\\\n", " / ")))
            it["description_english"] = want
            changed += 1
    print("\n  %d rewritten from their routine, %d with no routine description" % (changed, missing))
    if changed:
        print("  -> now run  python3 tools/port_vocab.py --write  to fit them to the TOOLKIT's three lines")
    if WRITE:
        open(p, "w", encoding="utf-8").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        print("  written src/data/items.json")


if __name__ == "__main__":
    main()
