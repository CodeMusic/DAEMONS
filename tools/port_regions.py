#!/usr/bin/env python3
"""T-48: the last two vanilla place names in the game.

    python3 tools/port_regions.py [--write]

3.1 renamed eleven cities and port_sevii named twenty-one island places. The
two CONTAINERS were never asked, so a game whose every town is ours still
said KANTO on the town map and SEVII ISLANDS in the ferry dialogue.

0.6 names them crosswise, which is the section's own device:

  KANTO  -> GAMUT        the complete range of colour a system can REPRODUCE,
                         and the famous fact about a gamut is that no device
                         covers what an eye can see. Its towns are each one
                         colour; the region is the set, and the set is
                         bounded. That is 0.2's image-making vocabulary,
                         0.4's sensation-and-perception split, and the Index's
                         own limit, in one word.

  SEVII  -> THE MARGINS  a CONTINENTAL MARGIN is the zone between the mainland
                         and the deep, which is where these islands are; the
                         MARGIN of a classifier is the band at the decision
                         boundary, WHERE THE HARD CASES LIVE; and a margin is
                         the edge of a printed page. Craft rule 3: it names
                         what was done to them, not what they are.

THE HOLDOUTS was the recommendation for a day and is DECLINED on evidence.
LOOKOUT is SENTRET/FURRET, it is edit-distance 3 from HOLDOUT, both are
<word>+OUT compounds, and LOOKOUT is ISLAND-ONLY -- Five Isle Meadow, Six
Island Water Path, Seven Island Sevault Canyon. A player standing in THE
HOLDOUTS would be catching LOOKOUTs. check_lexicon could not have caught it:
its near-collision rule is vowel-insertion only. (THE HOLDOUT is also already
a held proposal for the warden's place, which nobody noticed either.)

Three things this tool is built around, each a trap that has cost this project
time before:

  * A NAME SPLIT ACROSS TWO .string LINES IS INVISIBLE per line. "SEVII\n
    ISLANDS" does it twice. Every file is flattened before it is matched.
  * THE GENERATED HEADERS HALF-APPLY A MAPSEC RENAME (engine.md trap 11), so
    both are deleted here rather than trusted to rebuild.
  * ONE BLOCK IS A REWRITE, NOT A SUBSTITUTION. SevenIsland's naming joke is
    a folk etymology for "seven", twice over, and a find-and-replace would
    leave a man confidently explaining a number that is no longer in the name.

The ids are NOT touched. MAPSEC_SEVII_ISLE_6 and MAP_PROTOTYPE_SEVII_ISLE_6
are constants the engine refers to by hand; invariant 6's rule holds here for
the same reason it holds for types -- only the STRINGS are what a player reads.
"""
import json, os, re, sys, importlib.util

#  --write is read FIRST. The port_vocab import idiom below clobbers sys.argv,
#  and a previous tool in this repo silently dry-ran for a whole session
#  because it asked afterwards.
WRITE = "--write" in sys.argv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA  = os.path.join(ROOT, "engineGba")

def _textwidth():
    """port_vocab runs its own main() on import, so it is loaded the way
    port_sevii loads it: argv neutered, stdout swallowed, SystemExit caught."""
    import io, contextlib
    argv, sys.argv = sys.argv, ["port_vocab"]
    try:
        spec = importlib.util.spec_from_file_location("pv", os.path.join(HERE, "port_vocab.py"))
        pv = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                spec.loader.exec_module(pv)
            except SystemExit:
                pass
        return pv.textwidth
    finally:
        sys.argv = argv

textwidth = _textwidth()

CHAR_CAP  = 18     # u8 mapName[19] in region_map.c
PIXEL_CAP = 112    # the unsigned centring in map_name_popup.c
BOX_PIXELS = 196   # the message box, engine.md

JSON_PATH = os.path.join(GBA, "src", "data", "region_map", "region_map_sections.json")
GENERATED = [os.path.join(GBA, "src", "data", "region_map", f)
             for f in ("region_map_entry_strings.h", "region_map_entries.h")]
#  Every one of these is written by json_data_rules.mk and gitignored. Editing
#  an artifact is how sixteen town names once existed in one working build and
#  nowhere else. The SOURCE for items.h is items.json, swept above.
ARTIFACTS = GENERATED + [os.path.join(GBA, "src", "data", "items.h")]

#  Longest first: SEVII ISLANDS has to win over a bare SEVII, and KANTO's
#  compound has to win over the bare word.
#  THE MARGINS carries its own article, so a preceding one has to be ABSORBED
#  rather than left in front. The first run produced "the THE MARGINS" in
#  seven places -- including the ferry PASS description and the start menu.
SUBS = [
    ("the SEVII ISLANDS", "THE MARGINS"),
    ("The SEVII ISLANDS", "THE MARGINS"),
    ("THE SEVII ISLANDS", "THE MARGINS"),
    ("SEVII ISLANDS", "THE MARGINS"),
    ("SEVII ISLE",    "MARGIN ISLE"),
    ("SEVII",         "MARGIN"),
    ("KANTO",         "GAMUT"),
    ("Sevii Islands", "the Margins"),
    ("Kanto",         "Gamut"),
]

#  The one block that is authored rather than swept. Vanilla's joke is a folk
#  etymology for SEVEN, undercut, and then a grander etymology that is equally
#  unverifiable. The shape is kept exactly; only the thing being explained
#  wrongly has changed. Craft rule 2 -- both explanations are wrong in the
#  RIGHT direction, and neither is the reading the name actually carries.
AUTHORED = [(
    os.path.join(GBA, "data", "maps", "SevenIsland", "text.inc"),
    '''    .string "These islands are called the SEVII\\n"
    .string "ISLANDS because there are seven.\\p"
    .string "…Or at least that's what the young\\n"
    .string "people believe.\\p"
    .string "The truth is, these islands are so\\n"
    .string "named because they are said to\\l"
    .string "have been made in seven days.$"''',
    '''    .string "These islands are called THE\\n"
    .string "MARGINS because they are what was\\l"
    .string "left over.\\p"
    .string "…Or at least that's what the young\\n"
    .string "people believe.\\p"
    .string "The truth is, they are so named\\n"
    .string "because the mainland ran out of\\l"
    .string "paper before it ran out of islands.$"''',
)]

SENTINEL = "\x00"   # cannot appear in game text; marks a .string boundary
STRING_LINE = re.compile(r'(\.string\s+")((?:[^"\\]|\\.)*)(")')
#  src/strings.c holds five of them and they are C literals, not .string lines.
C_LITERAL   = re.compile(r'"((?:[^"\\]|\\.)*)"')
#  A literal that is a C identifier is a constant name, not player text --
#  and the test has to be the UNDERSCORE, not the case. "KANTO" is upper case
#  and IS the region string; MAPSEC_KANTO_SAFARI_ZONE is the constant. A
#  case-only test ate three of the five strings in strings.c on the first run.
IDENTIFIER  = re.compile(r'[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]*$')
#  items.json carries the RAINBOW PASS description, which names the region.
ITEMS_JSON  = os.path.join(GBA, "src", "data", "items.json")


def sweep_text(path):
    """Flatten, substitute, re-split. A name split across two .string lines is
    invisible to per-line matching, and SEVII does it twice."""
    raw = open(path, encoding="utf-8").read()
    pattern = C_LITERAL if path.endswith((".c", ".h")) else STRING_LINE
    group = 1 if pattern is C_LITERAL else 2
    pieces, spans = [], []
    for m in pattern.finditer(raw):
        if pattern is C_LITERAL and IDENTIFIER.fullmatch(m.group(1)):
            continue
        pieces.append(m.group(group)); spans.append(m.span(group))
    if not pieces:
        return raw, 0
    #  \n and \l are line breaks INSIDE one message, so a name can straddle
    #  them. Join on a sentinel that cannot appear in game text, substitute
    #  across the whole file, then put the pieces back one for one.
    flat = SENTINEL.join(pieces)
    hits = 0
    for old, new in SUBS:
        pattern = re.compile(r'\b' + r'[\x00\\nlp ]*'.join(map(re.escape, old.split(" "))) + r'\b')
        def _sub(m):
            nonlocal hits
            hits += 1
            #  Keep whatever break characters sat between the words -- and when
            #  the replacement has FEWER words than the match (absorbing an
            #  article does), keep the gaps that carry a SENTINEL first. A
            #  sentinel is a .string boundary; dropping one re-splits the file
            #  to a different number of pieces, which the guard below catches
            #  but which should not happen in the first place.
            gaps = re.findall(r'[\x00\\nlp ]+', m.group(0))
            parts = new.split(" ")
            needed = len(parts) - 1
            carriers = [g for g in gaps if SENTINEL in g]
            plain    = [g for g in gaps if SENTINEL not in g]
            chosen   = (carriers + plain)[:needed]
            #  Restore source order, so a break stays where the writer put it.
            chosen.sort(key=lambda g: gaps.index(g))
            while len(chosen) < needed:
                chosen.append(" ")
            out = parts[0]
            for i, part in enumerate(parts[1:]):
                out += chosen[i] + part
            #  Any sentinel that still has nowhere to go is re-emitted, so the
            #  piece count is conserved no matter what.
            for g in carriers:
                if g not in chosen:
                    out += SENTINEL * g.count(SENTINEL)
            return out
        flat = pattern.sub(_sub, flat)
    if not hits:
        return raw, 0
    out_pieces = flat.split(SENTINEL)
    if len(out_pieces) != len(pieces):
        raise SystemExit(f"  ABORT: {path} re-split to {len(out_pieces)} of {len(pieces)}")
    new_raw, shift = raw, 0
    for (a, b), piece in zip(spans, out_pieces):
        new_raw = new_raw[:a + shift] + piece + new_raw[b + shift:]
        shift += len(piece) - (b - a)
    return new_raw, hits


def walk():
    for base in ("data", "src"):
        for dirpath, _, files in os.walk(os.path.join(GBA, base)):
            for f in files:
                if f.endswith((".inc", ".s", ".c", ".h")):
                    yield os.path.join(dirpath, f)


def main():
    print("  T-48 -- KANTO -> GAMUT, SEVII -> THE MARGINS\n")

    #  1. the authored block first, so the sweep cannot reach it
    for path, old, new in AUTHORED:
        raw = open(path, encoding="utf-8").read()
        if new in raw:
            print(f"  authored  {os.path.relpath(path, GBA)}  already written")
        elif old not in raw:
            raise SystemExit(f"  ABORT: authored block not found in {path}")
        else:
            for line in new.splitlines():
                m = STRING_LINE.search(line)
                if m:
                    body = re.sub(r'\\[nlp]|\$$', '', m.group(2))
                    w = textwidth(body)
                    if w > BOX_PIXELS:
                        raise SystemExit(f"  ABORT: {w}px of {BOX_PIXELS}: {body}")
            widest_line = max(textwidth(re.sub(r'\\[nlp]|\$$', '', STRING_LINE.search(l).group(2)))
                              for l in new.splitlines() if STRING_LINE.search(l))
            print(f"  authored  {os.path.relpath(path, GBA)}  rewritten, "
                  f"widest line {widest_line}px of {BOX_PIXELS}")
            if WRITE:
                open(path, "w", encoding="utf-8").write(raw.replace(old, new))

    #  2. the mapsec names, in the JSON -- never in the generated header
    data = json.load(open(JSON_PATH, encoding="utf-8"))
    renamed = []
    for sec in data["map_sections"]:
        name = sec.get("name", "")
        new = name
        for old, rep in SUBS:
            new = re.sub(r'\b' + re.escape(old) + r'\b', rep, new)
        if new != name:
            if len(new) > CHAR_CAP:
                raise SystemExit(f"  ABORT: {len(new)} chars of {CHAR_CAP}: {new}")
            w = textwidth(new)
            if w > PIXEL_CAP:
                raise SystemExit(f"  ABORT: {w}px of {PIXEL_CAP}: {new}")
            renamed.append((name, new, w))
            sec["name"] = new
    widest = max((textwidth(s.get("name", "")) for s in data["map_sections"]), default=0)
    for old, new, w in renamed:
        print(f"  mapsec    {old:16} -> {new:16} {w}px")
    print(f"  {len(renamed)} mapsecs renamed, widest name in the game now {widest}px of {PIXEL_CAP}")
    if WRITE:
        with open(JSON_PATH, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

    #  3. items.json -- the RAINBOW PASS names the region in its description,
    #  and it is the SOURCE; items.h is generated and gitignored.
    items = json.load(open(ITEMS_JSON, encoding="utf-8"))
    ihits = 0
    def _walk_items(node):
        nonlocal ihits
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and k.endswith("_english"):
                    out = v
                    for old, rep in SUBS:
                        out = re.sub(r'\b' + r'[\\nlp ]*'.join(map(re.escape, old.split(" "))) + r'\b', rep, out)
                    if out != v:
                        node[k] = out; ihits += 1
                else:
                    _walk_items(v)
        elif isinstance(node, list):
            for v in node: _walk_items(v)
    _walk_items(items)
    if ihits:
        print(f"  items     src/data/items.json  ({ihits})")
        if WRITE:
            with open(ITEMS_JSON, "w", encoding="utf-8") as fh:
                json.dump(items, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    #  4. every other surface, flattened before it is matched
    total, touched = 0, []
    for path in walk():
        if os.path.abspath(path) in {os.path.abspath(p) for p in ARTIFACTS}:
            continue
        if any(os.path.abspath(path) == os.path.abspath(a[0]) for a in AUTHORED):
            continue
        try:
            new_raw, hits = sweep_text(path)
        except UnicodeDecodeError:
            continue
        if hits:
            total += hits
            touched.append((os.path.relpath(path, GBA), hits))
            if WRITE:
                open(path, "w", encoding="utf-8").write(new_raw)
    for p, n in sorted(touched):
        print(f"  swept     {p}  ({n})")
    print(f"  {total} substitutions across {len(touched)} files")

    #  5. the generated headers half-apply a rename. Delete, do not trust.
    for g in GENERATED:
        if os.path.exists(g):
            print(f"  deleting  {os.path.relpath(g, GBA)}  (engine.md trap 11)")
            if WRITE:
                os.remove(g)

    print("\n  written" if WRITE else "\n  dry run -- pass --write")


if __name__ == "__main__":
    main()
