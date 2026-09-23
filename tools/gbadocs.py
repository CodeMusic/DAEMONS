#!/usr/bin/env python3
"""The NOTEBOOK's other documents, placed in the world (T-224).

    python3 tools/gbadocs.py                          # report: every spot checked, what is placed
    python3 tools/gbadocs.py --write                  # flags, slots and scripts, with nothing placed
    python3 tools/gbadocs.py --write --text FILE      # place the documents FILE holds, and only those

WHY A TOOL. Twenty-four documents are designed in docs/school.md 10 and not yet in the game; 21 are drafted and
held PRIVATE until the user approves them, because several carry lines this project keeps out of public writing.
So the words never live here. FILE is a JSON object the user's approvals produce --
    {"LOOSE_PAGES_2": {"title": "HOMEWORK", "text": "First paragraph.\\n\\nSecond paragraph."}, ...}
-- and a document is placed exactly when its key is in it. Remove a key and re-run, and the document leaves the
world again: every placement is regenerated from this table, never edited by hand.

HOW A DOCUMENT IS FOUND. Each has one spot, proposed 2026-09-23 on the private field-test page:
  furniture  a bookshelf, terminal or blueprint no sign uses -- a bg_event on it, so it reads as the page
  card       an existing sign (the SORTING FRAME card): its own words first, then the page folded behind it
  silent     a line inside a scene, the way the Owl's two pages are filed -- nothing interrupts the scene
  sign       a NEW bg_event where a map has nothing free to read, optionally gated on a flag
A spot that holds several documents (the Scholar's desk) reads each one its gate allows, in number order.
Reading a page opens it full screen (Notebook_ReadFlagEntry) and files it with the NOTEBOOK's own line, so no
wording is added but the documents' own.

WHAT IT WRITES (engineGba):
  include/constants/flags.h                    FLAG_NOTEBOOK_DOC_<KEY>, 0x327-0x33E, the school's reserved block
  src/data/notebook_documents.h                every NB_DOC_<KEY> slot notebook.c's table holds -- a row, or empty
  data/scripts/notebook_documents.inc          the reading scripts, one per document and one per spot
  data/maps/<map>/map.json                     the spots' bg_events (script NotebookDoc_*)
  data/maps/<map>/scripts.inc                  the silent and card hooks, each line marked '@ gbadocs'
"""
import json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
TEXT = sys.argv[sys.argv.index("--text") + 1] if "--text" in sys.argv else None
MARK = "@ gbadocs"
FIRST_FLAG = 0x327

SECTION = {"LOOSE_PAGES": "NB_LOOSE_PAGES", "LAB_NOTES": "NB_LAB_NOTES", "RUN_LOGS": "NB_RUN_LOGS",
           "CORRESPONDENCE": "NB_CORRESPONDENCE", "THE_FILE": "NB_THE_FILE", "PROSPECTUS": "NB_PROSPECTUS",
           "PEER_REVIEW": "NB_PEER_REVIEW"}

#  key, spot. None = not drafted, on purpose (school.md 10: LOOSE PAGES 6, CORRESPONDENCE 1, PROSPECTUS 4).
#  A gate is ("set", FLAG) or ("unset", FLAG). Silent spots name the script label and the line to follow.
DOCS = [
    ("LOOSE_PAGES_2",    ("sign", "ViridianForest_Grove", 11, 15, None)),
    ("LOOSE_PAGES_4",    ("furniture", "CinnabarIsland_PokemonLab_Lounge", 3, 1)),
    ("LOOSE_PAGES_6",    None),
    ("LAB_NOTES_1",      ("furniture", "CinnabarIsland_PokemonLab_ResearchRoom", 3, 6)),
    ("LAB_NOTES_4",      ("card", "PewterCity_Museum_2F", "PewterCity_Museum_2F_EventScript_TheSortingFrame")),
    ("LAB_NOTES_6",      ("furniture", "CinnabarIsland_PokemonLab_ResearchRoom", 8, 6)),
    ("RUN_LOGS_5",       ("silent", "CeruleanCave_B1F", "CeruleanCave_B1F_EventScript_CaughtStarr", "setflag FLAG_FOUGHT_MEWTWO")),
    ("RUN_LOGS_6",       ("silent", "CeruleanCave_B1F", "CeruleanCave_B1F_EventScript_Mewtwo", "clearflag FLAG_SYS_SPECIAL_WILD_BATTLE")),
    ("CORRESPONDENCE_1", None),
    ("CORRESPONDENCE_2", ("furniture", "CeladonCity_Condominiums_3F", 0, 6)),
    ("CORRESPONDENCE_3", ("furniture", "SilphCo_3F", 6, 13)),
    ("CORRESPONDENCE_4", ("furniture", "FiveIsland_RocketWarehouse", 25, 4)),
    ("CORRESPONDENCE_5", ("silent", "FiveIsland_RocketWarehouse", "FiveIsland_RocketWarehouse_EventScript_DefeatedGideon", "setflag FLAG_TY_GAVE_PAYLOAD")),
    ("CORRESPONDENCE_6", ("sign", "SaffronCity_MrPsychicsHouse", 5, 5, ("set", "FLAG_OWL_CONCEDED"))),
    ("THE_FILE_4",       ("furniture", "SilphCo_4F", 29, 14)),
    ("THE_FILE_5",       ("furniture", "SilphCo_6F", 17, 12)),
    ("THE_FILE_6",       ("sign", "PokemonTower_3F", 11, 10, None)),
    ("PROSPECTUS_1",     ("sign", "MtMoon_B2F", 30, 11, None)),
    ("PROSPECTUS_3",     ("furniture", "SilphCo_1F", 15, 3)),
    ("PROSPECTUS_4",     None),
    ("PROSPECTUS_5",     ("sign", "PokemonTower_5F", 14, 11, None)),
    ("PROSPECTUS_6",     ("sign", "SaffronCity_Gym", 14, 9, ("set", "FLAG_DEFEATED_SABRINA"))),
    ("PEER_REVIEW_3",    ("sign", "SaffronCity_MrPsychicsHouse", 5, 5, ("unset", "FLAG_OWL_CONCEDED"))),
    ("PEER_REVIEW_4",    ("sign", "SaffronCity_MrPsychicsHouse", 5, 5, ("set", "FLAG_OWL_CONCEDED"))),
]
READABLE = {0x81, 0x83, 0x89, 0x93, 0x94, 0x95, 0x97, 0x98, 0x9A, 0xA0, 0x8F}


def flag(key):
    return "FLAG_NOTEBOOK_DOC_" + key


def section(key):
    return SECTION[key.rsplit("_", 1)[0]]


def load(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def layout(name):
    m = json.loads(load("data/maps/%s/map.json" % name))
    lay = next(l for l in json.loads(load("data/layouts/layouts.json"))["layouts"] if l and l["id"] == m["layout"])
    def attrs(sym):
        n = re.sub(r"(?<!^)(?=[A-Z])", "_", sym.replace("gTileset_", "")).lower()
        for base in ("primary", "secondary"):
            for d in os.listdir(os.path.join(GBA, "data/tilesets", base)):
                if d.replace("_", "") == n.replace("_", ""):
                    return open(os.path.join(GBA, "data/tilesets", base, d, "metatile_attributes.bin"), "rb").read()
    return m, lay, attrs(lay["primary_tileset"]), attrs(lay["secondary_tileset"])


def check_spot(spot):
    """None if the spot is usable, else why not."""
    kind, name = spot[0], spot[1]
    if not os.path.exists(os.path.join(GBA, "data/maps", name, "map.json")):
        return "no map %s" % name
    if kind in ("card", "silent"):
        src = load("data/maps/%s/scripts.inc" % name)
        body = re.search(r"^%s::\n(.*?)(?=^\w+::|\Z)" % re.escape(spot[2]), src, re.S | re.M)   # a label ends at the next
        if not body:
            return "no label %s" % spot[2]
        if kind == "silent" and spot[3] not in body.group(1):
            return "%s has no line '%s'" % (spot[2], spot[3])
        return None
    x, y = spot[2], spot[3]
    m, lay, pa, sa = layout(name)
    W, H = lay["width"], lay["height"]
    bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read()
    if not (0 <= x < W and 0 <= y + 1 < H):
        return "(%d,%d) is off the map" % (x, y)
    cell = lambda cx, cy: struct.unpack_from("<H", bd, (cy * W + cx) * 2)[0]
    v = cell(x, y)
    beh = struct.unpack_from("<I", pa if (v & 0x3FF) < 640 else sa, ((v & 0x3FF) % 640) * 4)[0] & 0x1FF
    if kind == "furniture" and beh not in READABLE:
        return "(%d,%d) is not readable furniture (behaviour 0x%x)" % (x, y, beh)
    if kind == "sign" and (v >> 10) & 3 == 0:
        return "(%d,%d) is open floor: a sign there would be read by walking into nothing" % (x, y)
    if (cell(x, y + 1) >> 10) & 3:
        return "(%d,%d) cannot be reached from below" % (x, y)
    ours = "NotebookDoc_%s_%d_%d" % (name, x, y)
    for b in m.get("bg_events") or []:
        if (b["x"], b["y"]) == (x, y) and b.get("script") != ours:
            return "(%d,%d) already has %s" % (x, y, b.get("script"))
    if any((o["x"], o["y"]) == (x, y + 1) for o in m.get("object_events") or []):
        return "(%d,%d) has somebody standing in front of it" % (x, y)
    return None


def charmap():
    """What the game can print: every single character charmap.txt maps, and every {PLACEHOLDER} it names."""
    cm = load("charmap.txt")
    chars = {m.group(1).replace("\\'", "'") for m in re.finditer(r"^'(\\'|[^'])'\s*=", cm, re.M)}
    names = set(re.findall(r"^([A-Z_0-9]+)\s*=", cm, re.M))
    return chars, names


def unprintable(text, chars, names):
    """The characters and placeholders in TEXT the game cannot print, if any."""
    bad = {"{%s}" % n for n in re.findall(r"\{(\w+)\}", text) if n not in names}
    bare = re.sub(r"\{\w+\}", "", text).replace("\\n", "")
    bad |= {c for c in bare if c not in chars and c not in "\n "}
    return bad


def c_string(text):
    """A document's words as a C string. book_reader.c reflows every line itself and breaks only at \\p, so a
    line the draft breaks on purpose -- a numbered list, a log's rows, written \\n -- becomes \\p too; left as \\n it
    would run into the line before it (found dry-running all 21 drafts, 2026-09-23)."""
    text = re.sub(r"\\n[ \t]*\n?", "\n\n", text.strip())
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    out = []
    for i, p in enumerate(paras):
        words, line, lines = p.split(" "), "", []
        for w in words:
            if line and len(line) + 1 + len(w) > 36:
                lines.append(line); line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)
        for j, ln in enumerate(lines):
            end = "\\n" if j < len(lines) - 1 else ("\\p" if i < len(paras) - 1 else "")
            out.append('    "%s%s"' % (ln.replace('"', '\\"'), end))
    return "\n".join(out)


def main():
    texts = json.load(open(TEXT)) if TEXT else {}
    unknown = set(texts) - {k for k, s in DOCS if s}
    if unknown:
        raise SystemExit("  !! --text names documents with no spot: %s" % ", ".join(sorted(unknown)))
    rc = 0
    chars, names = charmap()
    for k, t in sorted(texts.items()):
        bad = unprintable(t["title"] + "\n" + t["text"], chars, names)
        if bad:
            print("  !! %s: the game cannot print %s" % (k, " ".join(sorted(bad))))
            rc = 1
    placed = [(k, s) for k, s in DOCS if s and k in texts]
    for k, s in DOCS:
        why = check_spot(s) if s else None
        state = "not drafted" if not s else ("PLACED" if k in texts else "held")
        print("  %-17s %-12s %-44s %s" % (k, state, ("%s %s" % (s[0], s[1])) if s else "", ("!! " + why) if why else ""))
        if why:
            rc = 1
    if rc:
        print("  a spot or a page is wrong; nothing written")
        return rc

    # ---- flags, the school's reserved block
    flags_h = load("include/constants/flags.h")
    new_flags = flags_h
    for i, (k, _) in enumerate(DOCS):
        v = FIRST_FLAG + i
        want = "#define %-40s 0x%X   // T-224, tools/gbadocs.py" % (flag(k), v)
        new_flags = re.sub(r"^#define (FLAG_0x%X|%s)\s+0x%X\b.*$" % (v, flag(k), v), lambda m: want, new_flags, flags=re.M)
    # ---- the slots: a row for a placed document, empty for the rest
    h = ["// GENERATED by tools/gbadocs.py -- do not edit by hand.", "//",
         "// T-224: the NOTEBOOK's documents that are placed in the world. The words come from the user's approved",
         "// drafts (tools/gbadocs.py --text), which are never kept in the docs repo. Each NB_DOC_<KEY> is one row of",
         "// src/notebook.c's table, at its authored position, or nothing while the document is held.",
         "#ifndef GUARD_DATA_NOTEBOOK_DOCUMENTS_H", "#define GUARD_DATA_NOTEBOOK_DOCUMENTS_H", ""]
    for k, s in DOCS:
        if s and k in texts:
            t = texts[k]
            h.append("static const u8 sDocTitle_%s[] = _(\"%s\");" % (k, t["title"].upper()))
            h.append("static const u8 sDocText_%s[] = _(\n%s);" % (k, c_string(t["text"])))
            h.append("#define NB_DOC_%s { %s, NB_KIND_TEXT, 0, %s, 0, sDocTitle_%s, sDocText_%s }," % (k, section(k), flag(k), k, k))
        else:
            h.append("#define NB_DOC_%s" % k)
        h.append("")
    h.append("#endif // GUARD_DATA_NOTEBOOK_DOCUMENTS_H")
    header = "\n".join(h) + "\n"
    # ---- the reading scripts
    inc = ["@ GENERATED by tools/gbadocs.py -- do not edit by hand. T-224: the NOTEBOOK's documents, found in the world.", ""]
    for k, s in placed:
        if s[0] == "silent":
            continue
        inc += ["NotebookDoc_%s::" % k,
                "\tgoto_if_set %s, NotebookDoc_%s_Again" % (flag(k), k),
                "\tsetflag %s" % flag(k),
                "\tcall NotebookDoc_%s_Read" % k,
                "\tcall EventScript_NotebookCopied",
                "\treturn", "",
                "NotebookDoc_%s_Again::" % k,
                "\tcall NotebookDoc_%s_Read" % k,
                "\treturn", "",
                "NotebookDoc_%s_Read::" % k,
                "\tsetvar VAR_0x8004, %s" % flag(k),
                "\tfadescreen FADE_TO_BLACK",
                "\tspecial Notebook_ReadFlagEntry",
                "\twaitstate",
                "\treturn", ""]
    spots = {}
    for k, s in placed:
        if s[0] in ("furniture", "sign"):
            spots.setdefault((s[1], s[2], s[3]), []).append((k, s[4] if s[0] == "sign" else None))
        elif s[0] == "card":
            inc += ["NotebookDoc_%s_Card::" % k, "\tlockall", "\tcall NotebookDoc_%s" % k, "\treleaseall", "\tend", ""]
    for (name, x, y), docs in sorted(spots.items()):
        inc.append("NotebookDoc_%s_%d_%d::" % (name, x, y))
        inc.append("\tlockall")
        for n, (k, gate) in enumerate(docs):
            skip = "NotebookDoc_%s_%d_%d_%d" % (name, x, y, n)
            if gate:
                inc.append("\t%s %s, %s" % ("goto_if_unset" if gate[0] == "set" else "goto_if_set", gate[1], skip))
            inc.append("\tcall NotebookDoc_%s" % k)
            inc.append("%s::" % skip)
        inc += ["\treleaseall", "\tend", ""]
    script = "\n".join(inc) + "\n"
    # ---- the maps: bg_events for the spots, hook lines for silent and card
    #  Every map that holds one of ours NOW, not just those the table names: a spot that moves must not leave its
    #  old sign behind, pointing at a script that no longer exists (found moving a test spot, 2026-09-23).
    maps = {s[1] for _, s in DOCS if s}
    for d in os.listdir(os.path.join(GBA, "data/maps")):
        mj, si = os.path.join(GBA, "data/maps", d, "map.json"), os.path.join(GBA, "data/maps", d, "scripts.inc")
        if (os.path.exists(mj) and "NotebookDoc_" in open(mj, encoding="utf-8").read()) or \
           (os.path.exists(si) and MARK in open(si, encoding="utf-8").read()):
            maps.add(d)
    maps = sorted(maps)
    changes = []
    for name in maps:
        mpath = "data/maps/%s/map.json" % name
        raw = load(mpath); m = json.loads(raw)
        keep = [b for b in m.get("bg_events") or [] if not str(b.get("script", "")).startswith("NotebookDoc_")]
        add = [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                "script": "NotebookDoc_%s_%d_%d" % (name, x, y)} for (mn, x, y) in sorted(spots) if mn == name]
        new_bg = keep + add
        new_raw = raw if new_bg == (m.get("bg_events") or []) else None
        if new_raw is None:
            m["bg_events"] = new_bg
            new_raw = json.dumps(m, indent=2) + "\n"
        spath = "data/maps/%s/scripts.inc" % name
        src = load(spath)
        lines = [l for l in src.split("\n") if MARK not in l]
        for k, s in placed:
            if s[1] != name or s[0] not in ("silent", "card"):
                continue
            start = lines.index("%s::" % s[2])
            if s[0] == "silent":
                i = next(j for j in range(start + 1, len(lines)) if lines[j].strip() == s[3])
                lines.insert(i + 1, "\tsetflag %s   %s: filed without a word" % (flag(k), MARK))
            else:
                i = next(j for j in range(start + 1, len(lines)) if lines[j].strip() == "end")
                lines.insert(i, "\tgoto NotebookDoc_%s_Card   %s: the page folded behind the card" % (k, MARK))
        new_src = "\n".join(lines)
        for path, old, new in ((mpath, raw, new_raw), (spath, src, new_src)):
            if old != new:
                changes.append((path, new))
    for path, new in (("include/constants/flags.h", new_flags), ("src/data/notebook_documents.h", header),
                      ("data/scripts/notebook_documents.inc", script)):
        old = load(path) if os.path.exists(os.path.join(GBA, path)) else None
        if old != new:
            changes.append((path, new))
    print("  %d placed, %d held, %d not drafted; %s" % (len(placed), sum(1 for k, s in DOCS if s and k not in texts),
          sum(1 for _, s in DOCS if not s), ("%d file(s) %s" % (len(changes), "written" if WRITE else "would change")) if changes else "nothing to change"))
    for path, _ in changes:
        print("     " + path)
    if WRITE:
        for path, new in changes:
            open(os.path.join(GBA, path), "w", encoding="utf-8").write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
