#!/usr/bin/env python3
"""The A-to-Z word picker, sorted by the names we actually ship.

    python3 tools/port_ecsort.py [--write]

T-24. easy_chat_words_by_letter.h buckets every easy-chat word by the first
letter of its name, and it was written against Gen 3's names. We have since
renamed 151 species, 269 routines and 77 registers -- so STENCH is filed under
S and reads REPELLENT, and the picker's whole promise is broken.

Nothing here is a list. Every word is resolved to the string the game will
ACTUALLY draw, out of our own tables:

    EC_WORD_x       -> the sEasyChatWord_* string in the group files
    EC_MOVE(x)      -> gMoveNames[MOVE_x]
    EC_POKEMON(x)   -> gSpeciesNames[SPECIES_x]

The file's own two complications are honoured rather than flattened. A
"-1, N" marker means the next N entries render the SAME name -- Gen 3's way of
saying "one heading, several words" -- so a marker and its entries move as one
unit and keep their order. And numWords counts ARRAY ELEMENTS, not words, so a
marker counts two; getting that wrong is an out-of-bounds read rather than a
wrong sort.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
PATH = os.path.join(GBA, "src/data/easy_chat/easy_chat_words_by_letter.h")
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def read(rel):
    p = os.path.join(GBA, rel)
    return open(p, encoding="utf-8", errors="ignore").read() if os.path.exists(p) else ""


def names():
    """Every rendered string, keyed the way the by-letter file refers to it."""
    out = {}
    for k, v in re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]*)"\)', read("src/data/text/move_names.h")):
        out["EC_MOVE(%s)" % k] = v
        out["EC_MOVE2(%s)" % k] = v      # the second move group; same names
    sp = dict(re.findall(r'\[SPECIES_(\w+)\] = _\("([^"]*)"\)', read("src/data/text/species_names.h")))
    for k, v in sp.items():
        out["EC_POKEMON(%s)" % k] = v
        out["EC_POKEMON2(%s)" % k] = v
    #  EC_WORD_THICK_FAT is sEasyChatWord_ThickFat. Match on the letters alone
    #  rather than on a naming convention, which is one underscore away from
    #  being wrong and silent.
    words = {}
    for f in os.listdir(os.path.join(GBA, "src/data/easy_chat")):
        for sym, txt in re.findall(r'sEasyChatWord_(\w+)\[\] = _\("([^"]*)"\)',
                                   read("src/data/easy_chat/" + f)):
            words[re.sub(r'[^A-Z0-9]', '', sym.upper())] = txt
    for c in re.findall(r'#define (EC_WORD_\w+)', read("include/constants/easy_chat.h")):
        key = re.sub(r'[^A-Z0-9]', '', c[len("EC_WORD_"):])
        if key in words:
            out[c] = words[key]
    return out


def main():
    render = names()
    raw = open(PATH, encoding="utf-8").read()

    units, missing = {}, []
    for letter in LETTERS + ["Others"]:
        m = re.search(r'sEasyChatWordsByLetter_%s\[\] = \{(.*?)\n\};' % letter, raw, re.S)
        if not m:
            continue
        toks = [x.strip() for x in re.sub(r'//[^\n]*', '', m.group(1)).replace("\n", " ").split(",") if x.strip()]
        i, group = 0, []
        while i < len(toks):
            if toks[i] == "-1":                      # a heading and its N words
                n = int(toks[i + 1])
                group.append((toks[i + 2 : i + 2 + n], n + 2)); i += 2 + n
            else:
                group.append(([toks[i]], 1)); i += 1
        units.setdefault("ALL", []).extend(group)

    buckets = {k: [] for k in LETTERS + ["Others"]}
    for entries, size in units["ALL"]:
        text = render.get(entries[0])
        if text is None:
            missing.append(entries[0]); text = ""
        key = (text[:1].upper() if text[:1].isalpha() else "")
        buckets[key if key in LETTERS else "Others"].append((text.upper(), entries, size))

    if missing:
        print("  !! %d entr(ies) resolved to no name: %s" % (len(missing), ", ".join(missing[:6])))
        return 1

    moved = 0
    out = raw
    for letter in LETTERS + ["Others"]:
        rows = sorted(buckets[letter], key=lambda r: r[0]) if letter != "Others" else buckets[letter]
        body, count = [], 0
        for _, entries, size in rows:
            if len(entries) > 1:
                body.append("    -1, %d, // Doubled pokemon species name" % len(entries))
            body += ["    %s," % e for e in entries]
            count += size
        m = re.search(r'(static const u16 sEasyChatWordsByLetter_%s\[\] = \{)(.*?)(\n\};)' % letter, out, re.S)
        if not m:
            continue
        if m.group(2).strip() != "\n".join(body).strip():
            moved += 1
        out = out[:m.start(2)] + "\n" + "\n".join(body) + out[m.end(2):]
        out = re.sub(r'(\.words = sEasyChatWordsByLetter_%s,\s*\n\s*\.numWords = )\d+' % letter,
                     r'\g<1>%d' % count, out)

    print("  %d words resolved out of our own tables" % len(render))
    print("  %d of the 27 lists changed" % moved)
    if "--write" in sys.argv:
        open(PATH, "w", encoding="utf-8").write(out)
        print("  written %s" % os.path.relpath(PATH, ROOT))
    else:
        print("  (report only; pass --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
