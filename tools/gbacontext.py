#!/usr/bin/env python3
"""CONTEXT's own Index entries (T-232): an approved draft into the CONTEXT edition, and nowhere else.

    python3 tools/gbacontext.py --text FILE            # report: what each entry would become
    python3 tools/gbacontext.py --text FILE --write    # write them into src/data/pokemon/pokedex_text_lg.h

0.4 rules that a daemon's two entries are a PAIR -- CONTENT says what it does, CONTEXT what follows from it -- and
197 of the entries this project wrote were one sentence in both files, because the Game Boy's dex text had no
edition split. The drafts are the user's to approve and are kept off the repo until they are; FILE is a JSON object
of the approved ones, by the name the game shows:

    {"ROVERCUB": "Whoever carried it chose what it knows. They did not think of it as choosing.", ...}

Each is wrapped to the entry pane (234px, four lines -- the widths the 386 entries already demonstrate) and checked
against charmap.txt. An entry is only written where CONTEXT still carries CONTENT's own sentence: one that already
differs is an authored pair, and this tool will not write over it. With no FILE it reports how many pairs remain.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
TEXT = sys.argv[sys.argv.index("--text") + 1] if "--text" in sys.argv else None
PANE_W, PANE_LINES = 234, 4

_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), _ns)
width = _ns["textwidth"]

ENTRY = re.compile(r'(const u8 g(\w+)PokedexText\[\] = _\()(.*?)(\);)', re.S)


def body(block):
    return "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', block))


def wrap(text):
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if width(cand) <= PANE_W:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def main():
    fr_path = os.path.join(GBA, "src/data/pokemon/pokedex_text_fr.h")
    lg_path = os.path.join(GBA, "src/data/pokemon/pokedex_text_lg.h")
    fr = {m.group(2).upper(): body(m.group(3)) for m in ENTRY.finditer(open(fr_path, encoding="utf-8").read())}
    lg_src = open(lg_path, encoding="utf-8").read()
    lg = {m.group(2).upper(): body(m.group(3)) for m in ENTRY.finditer(lg_src)}
    names = {v: k.replace("_", "") for k, v in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)',
             open(os.path.join(GBA, "src/data/text/species_names.h"), encoding="utf-8").read())}
    same = sorted(k for k in fr if fr[k] and fr[k] == lg.get(k))
    if not TEXT:
        import subprocess
        up = subprocess.run(["git", "-C", GBA, "show", "upstream/master:src/data/pokemon/pokedex_text_fr.h"],
                            capture_output=True, text=True).stdout
        vanilla = {m.group(2).upper(): body(m.group(3)) for m in ENTRY.finditer(up)}
        ours = [k for k in same if vanilla.get(k) != fr[k]]
        print("  %d of our entries still say the same thing in both editions (and %d of vanilla's)"
              % (len(ours), len(same) - len(ours)))
        return 0
    cm = open(os.path.join(GBA, "charmap.txt"), encoding="utf-8").read()
    chars = {m.group(1).replace("\\'", "'") for m in re.finditer(r"^'(\\'|[^'])'\s*=", cm, re.M)}
    want = json.load(open(TEXT, encoding="utf-8"))
    rc, plan = 0, {}
    for name, text in sorted(want.items()):
        key = names.get(name)
        why = None
        if not key or key not in lg:
            why = "no daemon called %s has an entry" % name
        elif fr.get(key) != lg.get(key):
            why = "CONTEXT already has its own entry; not written over"
        else:
            bad = {c for c in text if c not in chars and c not in " "}
            lines = wrap(text)
            if bad:
                why = "the game cannot print %s" % " ".join(sorted(bad))
            elif len(lines) > PANE_LINES or any(width(l) > PANE_W for l in lines):
                why = "does not fit the entry pane (%d lines)" % len(lines)
            else:
                plan[key] = lines
        print("  %-11s %s" % (name, ("!! " + why) if why else "%d lines" % len(plan[key])))
        if why and "already has" not in why:
            rc = 1
    if rc:
        print("  an entry is wrong; nothing written")
        return rc

    def repl(m):
        key = m.group(2).upper()
        if key not in plan:
            return m.group(0)
        lines = plan[key]
        inner = "\n" + "\n".join('    "%s%s"' % (l.replace('"', '\\"'), "\\n" if i < len(lines) - 1 else "")
                                 for i, l in enumerate(lines))
        return m.group(1) + inner + m.group(4)
    new = ENTRY.sub(repl, lg_src)
    print("  %d CONTEXT entr%s %s" % (len(plan), "y" if len(plan) == 1 else "ies",
          "written" if WRITE and new != lg_src else "would be written" if new != lg_src else "unchanged"))
    if WRITE and new != lg_src:
        open(lg_path, "w", encoding="utf-8").write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
