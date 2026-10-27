#!/usr/bin/env python3
"""Object graphics ids: every number used once, none in the VAR range or past the limit, no FREE id used (T-461).

    python3 tools/check_objgfx.py            # exits non-zero on a problem; lists the FREE ids
    python3 tools/check_objgfx.py --usage    # and how often each defined id is used, for the next reclaim

WHY. The save keeps an object's graphics id in three places: the current map's object event templates, its live
object events, and the recap's (quest log's) object events. 240-255 are OBJ_EVENT_GFX_VAR_0..F, read through
VAR_OBJ_GFX_ID_0..F, and all sixteen are in use. T-460 took id 239, the last narrow one. T-461 first made room by
marking ids vanilla defined but nothing in the game uses as OBJ_EVENT_GFX_FREE_<n> (no save can hold a number nothing
ever placed), then (phase 2, 2026-10-27) widened the id to 12 bits in bytes every save held as 0: new ids run from
OBJ_EVENT_GFX_WIDE_START (256) to OBJ_EVENT_GFX_ID_LIMIT - 1, and the recap, still a u8, records each as a stand-in.

WHAT IT CHECKS, in engineGba:
  - include/constants/event_objects.h: every OBJ_EVENT_GFX_* has its own number, 0..239 with no gap and, once any
    wide id exists, 256..NUM-1 with no gap; nothing is numbered 240-255 (the VARs), and NUM is not in the VAR range or
    past OBJ_EVENT_GFX_ID_LIMIT;
  - the header's `//  FREE:` line lists exactly the OBJ_EVENT_GFX_FREE_<n> defines;
  - gObjectEventGraphicsInfoPointers has one entry for every id;
  - nothing in data/ or src/ names an OBJ_EVENT_GFX_FREE_<n> (the pointer table aside), and no map's graphics_id is
    a FREE id's bare number -- a FREE id used is a FREE id a save may now hold;
  - sTextColorTable has no two rows for the same id pair (a second [id / 2] silently re-colours the first);
  - quest_log_objects.c's sQuestLogGfxStandIns: each row is a wide id standing in as a narrow one (below the VARs),
    once. A wide id with no row records OBJ_EVENT_GFX_QL_STAND_IN; those are listed, not failed.
"""
import collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
HDR = "include/constants/event_objects.h"
PTRS = "src/data/object_events/object_event_graphics_info_pointers.h"
COLOURS = "src/dynamic_placeholder_text_util.c"
STANDINS = "src/quest_log_objects.c"
LAYOUT = {"OBJ_EVENT_GFX_VARS", "OBJ_EVENT_GFX_WIDE_START", "OBJ_EVENT_GFX_ID_LIMIT", "OBJ_EVENT_GFX_QL_STAND_IN"}


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8", errors="replace").read()


def defines(hdr=None):
    """{name: number} for every numbered OBJ_EVENT_GFX_* (the VARs are expressions and are left out, as are the
    layout constants), and NUM, VARS."""
    hdr = hdr if hdr is not None else read(HDR)
    ids = {c: int(n) for c, n in re.findall(r"^#define (OBJ_EVENT_GFX_\w+) (\d+)\b", hdr, re.M) if c not in LAYOUT}
    num = int(re.search(r"^#define NUM_OBJ_EVENT_GFX\s+(\d+)", hdr, re.M).group(1))
    var = int(re.search(r"^#define OBJ_EVENT_GFX_VARS\s+(\d+)", hdr, re.M).group(1))
    return ids, num, var


def layout(hdr=None):
    """(OBJ_EVENT_GFX_WIDE_START, OBJ_EVENT_GFX_ID_LIMIT) -- T-461 phase 2."""
    hdr = hdr if hdr is not None else read(HDR)
    return tuple(int(re.search(r"^#define %s\s+(\d+)" % c, hdr, re.M).group(1))
                 for c in ("OBJ_EVENT_GFX_WIDE_START", "OBJ_EVENT_GFX_ID_LIMIT"))


def expected_ids(num, var, wide):
    """The numbers a table of length NUM must define: 0..VARS-1, then WIDE..NUM-1 once it has grown past the VARs."""
    return list(range(min(num, var))) + list(range(wide, num))


def free_ids(hdr=None):
    ids, _, _ = defines(hdr)
    return sorted(n for c, n in ids.items() if c == "OBJ_EVENT_GFX_FREE_%d" % n)


def usage():
    """{constant: [file, ...]} for every OBJ_EVENT_GFX_* named in data/ and src/, the header and pointer table aside."""
    out = collections.defaultdict(list)
    skip = {os.path.join(GBA, HDR), os.path.join(GBA, PTRS)}
    for top in ("data", "src", "include"):
        for f in glob.glob(os.path.join(GBA, top, "**", "*"), recursive=True):
            if f in skip or not os.path.isfile(f) or not f.endswith((".c", ".h", ".inc", ".s", ".json", ".pory")):
                continue
            t = open(f, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"OBJ_EVENT_GFX_\w+", t):
                out[m.group(0)].append(os.path.relpath(f, GBA))
    return out


def check():
    bad = []
    hdr = read(HDR)
    ids, num, var = defines(hdr)
    wide, limit = layout(hdr)
    real = dict(ids)
    want = expected_ids(num, var, wide)

    if var < num <= wide:
        bad.append((HDR, "NUM_OBJ_EVENT_GFX %d stops inside the VAR range %d-%d" % (num, var, wide - 1)))
    if num > limit:
        bad.append((HDR, "NUM_OBJ_EVENT_GFX %d is past OBJ_EVENT_GFX_ID_LIMIT %d (12 bits)" % (num, limit)))
    by = collections.defaultdict(list)
    for c, n in real.items():
        by[n].append(c)
    for n, cs in sorted(by.items()):
        if len(cs) > 1:
            bad.append((HDR, "id %d is %s" % (n, " and ".join(sorted(cs)))))
        if n >= num:
            bad.append((HDR, "%s is %d, at or past NUM_OBJ_EVENT_GFX %d" % (cs[0], n, num)))
        if var <= n < wide:
            bad.append((HDR, "%s is %d, a VAR graphics id (%d-%d)" % (cs[0], n, var, wide - 1)))
    gaps = [n for n in want if n not in by]
    if gaps:
        bad.append((HDR, "no define for id(s) %s" % " ".join(map(str, gaps))))

    free = free_ids(hdr)
    m = re.search(r"^//  FREE:([^\n]*)$", hdr, re.M)
    listed = [int(x) for x in re.findall(r"\d+", m.group(1))] if m else None
    if listed is None:
        bad.append((HDR, "no `//  FREE:` line listing the free ids"))
    elif sorted(listed) != free:
        bad.append((HDR, "`//  FREE:` lists %s but the FREE defines are %s" % (listed, free)))

    ptrs = read(PTRS)
    entries = re.findall(r"^\s*\[\s*(OBJ_EVENT_GFX_\w+)\s*\]\s*=\s*&gObjectEventGraphicsInfo_\w+,", ptrs, re.M)
    have = collections.Counter(real.get(c, -1) for c in entries)
    for c in entries:
        if c not in real:
            bad.append((PTRS, "%s is not a numbered define" % c))
    for n in want:
        if have[n] != 1:
            bad.append((PTRS, "id %d (%s) has %d entries" % (n, "/".join(by.get(n, ["?"])), have[n])))

    used = usage()
    for n in free:
        c = "OBJ_EVENT_GFX_FREE_%d" % n
        for f in sorted(set(used.get(c, []))):
            bad.append((f, "uses %s -- a FREE id; give the sprite its own name with gentowns.register_one" % c))
    freeset = set(free)
    for mj in sorted(glob.glob(os.path.join(GBA, "data/maps/*/map.json"))):
        for i, o in enumerate(json.load(open(mj)).get("object_events", [])):
            g = str(o.get("graphics_id", ""))
            if g.isdigit() and int(g) in freeset:
                bad.append((os.path.relpath(mj, GBA), "object %d is graphics id %s, a FREE id" % (i + 1, g)))

    body = read(COLOURS)
    s = body.index("sTextColorTable[] =")
    rows = collections.defaultdict(list)
    for c in re.findall(r"\[\s*(OBJ_EVENT_GFX_\w+)\s*/\s*2\s*\]", body[s:body.index("};", s)]):
        if c in real:
            rows[real[c] // 2].append(c)
        else:
            bad.append((COLOURS, "sTextColorTable names %s, which is not a numbered define" % c))
    for r, cs in sorted(rows.items()):
        if len(cs) > 1:
            bad.append((COLOURS, "sTextColorTable row %d (ids %d-%d) is given twice: %s" % (r, 2 * r, 2 * r + 1, ", ".join(cs))))

    for key, val in stand_ins().items():
        if real.get(key, -1) < wide:
            bad.append((STANDINS, "sQuestLogGfxStandIns has a row for %s, which is not a wide id (%d up)" % (key, wide)))
        if val not in real or real[val] >= var:
            bad.append((STANDINS, "%s stands in as %s, which is not a narrow id (below %d)" % (key, val, var)))
    return bad


def stand_ins():
    """{wide const: narrow const} from quest_log_objects.c's sQuestLogGfxStandIns (T-461 phase 2)."""
    body = read(STANDINS)
    rows = re.findall(r"^\s*\[\s*(OBJ_EVENT_GFX_\w+)\s*-\s*OBJ_EVENT_GFX_WIDE_START\s*\]\s*=\s*(OBJ_EVENT_GFX_\w+)\s*,",
                      body, re.M)
    out = {}
    for k, v in rows:
        if k in out:
            raise SystemExit("  %s: sQuestLogGfxStandIns gives %s twice" % (STANDINS, k))
        out[k] = v
    return out


def main():
    bad = check()
    free = free_ids()
    ids, num, var = defines()
    wide, limit = layout()
    nwide = max(0, num - wide)
    print("  %d object graphics ids (0-%d%s), the VARs at %d-%d, room to %d; FREE: %s" % (
        min(num, var) + nwide, min(num, var) - 1, ", %d-%d" % (wide, num - 1) if nwide else "", var, var + 15,
        limit - 1, " ".join(map(str, free)) or "none"))
    si = stand_ins()
    plain = sorted(c for c, n in ids.items() if n >= wide and c not in si)
    if plain:
        print("  the recap shows OBJ_EVENT_GFX_QL_STAND_IN for: %s" % " ".join(plain))
    if "--usage" in sys.argv:
        used = usage()
        ids, _, _ = defines()
        for c, n in sorted(ids.items(), key=lambda kv: kv[1]):
            fs = collections.Counter(used.get(c, []))
            maps = sum(k for f, k in fs.items() if f.startswith("data/maps"))
            print("   %3d %-44s maps %3d  %s" % (n, c, maps, " ".join(
                "%s:%d" % (os.path.basename(f), k) for f, k in sorted(fs.items()) if not f.startswith("data/maps"))))
    for where, why in bad:
        print("   %-48s %s" % (where, why))
    if not bad:
        print("  every object graphics id has one number and one slot, and no FREE id is used.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
