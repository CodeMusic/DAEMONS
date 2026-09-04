#!/usr/bin/env python3
"""Carry a renamed name table from the Game Boy build into the GBA build.

    python3 tools/port_names.py            # report only
    python3 tools/port_names.py --write

The two engines store the same table completely differently -- `dname "PING"`
in index order on one side, `[SPECIES_SPEAROW] = _("PING")` keyed by constant
on the other -- but the RENAME is the same fact in both. So this does not try
to map index to constant. It diffs our table against upstream's to learn
{vanilla name -> our name}, then substitutes on the vanilla string, which is
exact and needs no arithmetic.

Only names we actually changed are touched. Everything still vanilla stays
vanilla, so a half-ported table is obvious rather than silently mixed.
"""
import difflib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

# Some renames have nowhere to land, and that is a FACT ABOUT THE PORT rather
# than a bug. In Gen 3 badges are not items at all -- `items.h` contains the
# string BADGE zero times -- so the eight MARKS have no item slot to be renamed
# into. They live as flags and a Trainer Card display. Listing them here keeps
# them from being reported as failures every run without letting them be
# silently dropped: they are named, with the reason.
KNOWN_MISSING = {
    "src/data/items.json": (
        "badges are not items in Gen 3 -- no bag slot, no description -- but "
        "they do have NAMES; see BADGE_STRINGS below",
        {"BOULDERBADGE", "CASCADEBADGE", "THUNDERBADGE", "RAINBOWBADGE",
         "SOULBADGE", "MARSHBADGE", "VOLCANOBADGE", "EARTHBADGE"},
    ),
}

# The MARKS do land after all, just not in the item table. Gen 3 keeps the eight
# badge names as individual symbols in src/strings.c rather than as rows of
# anything, so there is no sequence to diff -- the pairing is written out.
# An earlier version of this file recorded the MARKS as unportable, which was
# wrong: "not an item" is not the same as "has no name".
BADGE_STRINGS = "src/strings.c"
BADGES = [
    ("gText_BoulderBadge", "BOULDERBADGE"), ("gText_CascadeBadge", "CASCADEBADGE"),
    ("gText_ThunderBadge", "THUNDERBADGE"), ("gText_RainbowBadge", "RAINBOWBADGE"),
    ("gText_SoulBadge", "SOULBADGE"),       ("gText_MarshBadge", "MARSHBADGE"),
    ("gText_VolcanoBadge", "VOLCANOBADGE"), ("gText_EarthBadge", "EARTHBADGE"),
]

TABLES = [
    # gb source, gb macro, gba file, name limit, format
    ("data/pokemon/names.asm",   "dname", "src/data/text/species_names.h",            10, "c"),
    ("data/items/names.asm",     "li",    "src/data/items.json",                      14, "json"),
    ("data/moves/names.asm",     "li",    "src/data/text/move_names.h",               12, "c"),
    # Town names live in the region map on GBA rather than in a flat table, but
    # the rename is still the same fact, so the same trick works.
    #
    # IT MUST BE THE JSON. region_map_entry_strings.h is generated from
    # region_map_sections.json and is GITIGNORED -- an earlier version of this
    # table wrote the header, so all sixteen town names lived only in one
    # working build and a fresh clone would have built vanilla. The renames were
    # in nobody's repository.
    ("data/maps/names.asm",      "db",    "src/data/region_map/region_map_sections.json",  16, "json:name"),
]

def _strip(v):
    return v[:-1] if v.endswith("@") else v      # Gen 1 string terminator

def gb_list(path, macro):
    return [_strip(m.group(1)) for m in
            re.finditer(r'%s\s+"([^"]*)"' % macro, open(os.path.join(GB, path)).read())]

def upstream_list(path, macro):
    txt = subprocess.run(["git", "-C", GB, "show", "upstream/master:" + path],
                         capture_output=True, text=True).stdout
    return [_strip(m.group(1)) for m in re.finditer(r'%s\s+"([^"]*)"' % macro, txt)]

rc = 0
for src, macro, dst, limit, fmt in TABLES:
    ours, van = gb_list(src, macro), upstream_list(src, macro)
    # Diff the two sequences properly rather than zipping them. A table can be
    # longer than upstream's because we ADDED something -- 2.5 added the move
    # CONSENSUS at slot 165 -- and a positional zip reads that insertion as
    # "STRUGGLE was renamed to CONSENSUS", which is false and would rename
    # Gen 3's Struggle. difflib tells an insert from a replace; zip cannot.
    renames, added = {}, []
    sm = difflib.SequenceMatcher(a=van, b=ours, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            renames.update(dict(zip(van[i1:i2], ours[j1:j2])))
        elif tag == "insert":
            added += ours[j1:j2]
        elif tag == "replace":
            print("  !! %s: %d entries became %d -- cannot pair them"
                  % (src, i2 - i1, j2 - j1)); rc = 1
    print("%s -> %s" % (src, dst))
    print("  %d renamed of %d" % (len(renames), len(ours)))
    if added:
        # An ADDED name is not a rename and has no vanilla string to substitute
        # for, so it needs a slot of its own -- but once that slot exists,
        # saying it is missing every run is just noise.
        have = open(os.path.join(GBA, dst)).read()
        placed = [a for a in added if a in have]
        want = [a for a in added if a not in have]
        if placed:
            print("  %d added, and already has a slot: %s" % (len(placed), " ".join(placed)))
        if want:
            print("  %d added, not renamed -- needs its own slot on GBA: %s"
                  % (len(want), " ".join(want)))

    too_long = {v: o for v, o in renames.items() if len(o) > limit}
    for v, o in sorted(too_long.items()):
        print("  !! %s is %d chars, limit is %d" % (o, len(o), limit)); rc = 1

    path = os.path.join(GBA, dst)
    text = open(path).read()
    reason, expected = KNOWN_MISSING.get(dst, ("", set()))
    done, missing, skipped = 0, [], []
    for v, o in sorted(renames.items()):
        if fmt == "c":
            pat, rep = r'(_\(")%s("\))' % re.escape(v), r'\g<1>%s\g<2>' % o
            already = '_("%s")' % o
        else:
            # The file stores non-ASCII escaped -- POKé is POK\\u00e9 on disk --
            # so match the way it is spelled there, not the way we read it. And
            # match case-insensitively: Gen 1 wrote OAK's PARCEL, Gen 3 writes
            # OAK'S PARCEL, and that is the same item.
            key = fmt.split(":")[1] if ":" in fmt else "english"
            esc = json.dumps(v)[1:-1]
            pat = r'("%s": ")%s(")' % (key, re.escape(esc))
            rep = r'\g<1>%s\g<2>' % json.dumps(o)[1:-1]
            already = '"%s": "%s"' % (key, json.dumps(o)[1:-1])
        flags = re.IGNORECASE if fmt.startswith("json") else 0
        text, n = re.subn(pat, rep, text, flags=flags)
        if n: done += n
        elif already in text: done += 1                # already ported
        elif v in expected: skipped.append(v)
        else: missing.append(v)
    if skipped:
        print("  %d with no slot -- %s:" % (len(skipped), reason))
        print("     " + " ".join(sorted(skipped)))
    for v in missing:
        print("  !! no slot found for vanilla name %s" % v); rc = 1
    print("  %d/%d placed" % (done, len(renames) - len(skipped)))
    if WRITE and not missing and not too_long:
        open(path, "w").write(text)
        print("  written")

    # The region-map generator builds its C symbol names OUT OF THE NAME
    # STRING -- "ROCK TUNNEL" becomes sMapsecName_ROCK_TUNNEL, "QUICKSILVER IS."
    # becomes sMapsecName_QUICKSILVER_IS_ -- so renaming a town silently renames
    # a symbol that hand-written code refers to by hand. region_map.c stopped
    # compiling the first time this ran against the JSON.
    if fmt.startswith("json") and "region_map" in dst:
        # The generator works on BYTES, not characters: é is two bytes in UTF-8 and
        # becomes TWO underscores, so POKéMON MANSION is sMapsecName_POK__MON_MANSION.
        sym = lambda x: re.sub(r'[^A-Za-z0-9]', '_', x.encode('utf-8').decode('latin-1'))
        rmc = os.path.join(GBA, "src/region_map.c")
        body = open(rmc).read()
        fixed = 0
        for v, o in renames.items():
            a, b = "sMapsecName_%s" % sym(v), "sMapsecName_%s" % sym(o)
            if a != b and a in body:
                body = re.sub(r'\b%s\b' % re.escape(a), b, body); fixed += 1
        print("  %d symbol reference(s) in region_map.c follow the rename" % fixed)
        if WRITE and fixed:
            open(rmc, "w").write(body)

# --- the MARKS ---------------------------------------------------------------
items_gb = gb_list("data/items/names.asm", "li")
items_van = upstream_list("data/items/names.asm", "li")
badge_names = {}
sm = difflib.SequenceMatcher(a=items_van, b=items_gb, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "replace" and (i2 - i1) == (j2 - j1):
        badge_names.update(dict(zip(items_van[i1:i2], items_gb[j1:j2])))
path = os.path.join(GBA, BADGE_STRINGS)
text = open(path).read()
print("%s -> %s" % ("the MARKS", BADGE_STRINGS))
placed = 0
for sym, vanilla in BADGES:
    ours = badge_names.get(vanilla)
    if not ours:
        print("  !! %s has no rename" % vanilla); rc = 1; continue
    pat = r'(const u8 %s\[\] = _\(")[^"]*("\);)' % re.escape(sym)
    text, n = re.subn(pat, r'\g<1>%s\g<2>' % ours, text)
    if n or ('_("%s")' % ours) in text:
        placed += 1
    else:
        print("  !! no %s in %s" % (sym, BADGE_STRINGS)); rc = 1
print("  %d/%d placed" % (placed, len(BADGES)))
if WRITE and placed == len(BADGES):
    open(path, "w").write(text)
    print("  written")
sys.exit(rc)
