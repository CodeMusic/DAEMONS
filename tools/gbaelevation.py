#!/usr/bin/env python3
"""Who floats in battle: enemy_mon_elevation.h from each daemon's drawing (T-452 follow-up, 2026-11-06).

    python3 tools/gbaelevation.py            # report, and THE CHECK: exit 1 on anything below
    python3 tools/gbaelevation.py --write    # write the engine's table from tools/daemon_float.json
    python3 tools/gbaelevation.py --stamp    # after looking at a redrawn daemon: record its drawing as decided

The engine lifts a foe by gEnemyMonElevation[species] pixels and draws a shadow under it whenever that is nonzero
(battle_gfx_sfx_util.c). The table was vanilla's -- GEODUDE 16, LUNATONE 13, SWABLU 12 -- and the redrawn roster is
mostly standing and sitting drawings, so 29 of them hung over their own shadows (docs/private/t452-roster-walk).

Each lifted slot is decided in tools/daemon_float.json from the daemon's FRONT: only a drawing that is flying,
hovering or levitating keeps a lift; standing, sitting or perched is 0, and so is doubt. The check fails when:

    a species has a lift and is not decided floating      (a drawing on its feet, over a shadow)
    a species decided floating has no lift, or another
    a floater's drawing changed since it was decided      (look again, then --stamp)
    the engine's table is not what --write would make

check_generators runs this in report mode, so the check runs with every generator.
"""
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DATA = os.path.join(ROOT, "tools", "daemon_float.json")
TABLE = os.path.join(GBA, "src/data/pokemon_graphics/enemy_mon_elevation.h")
SPECIES_H = os.path.join(GBA, "include/constants/species.h")

HEAD = """// This determines how much higher above the usual position the enemy Pokémon
// is during battle. Species that float or fly have nonzero values.
// DAEMONS: written by tools/gbaelevation.py from tools/daemon_float.json -- only a daemon DRAWN flying, hovering or
// levitating is lifted (and gets the shadow); everything standing, sitting or perched is 0. Edit the json, not this.
const u8 gEnemyMonElevation[NUM_SPECIES] =
{
"""


def front(species):
    """The front drawing a species battles as: its folder's front.png (UNOWN's is A's)."""
    d = os.path.join(GBA, "graphics/pokemon", species.lower())
    p = os.path.join(d, "front.png")
    return p if os.path.exists(p) else os.path.join(d, "a", "front.png")


def silhouette(species):
    """A hash of which pixels the front draws -- a recolour leaves it, a redraw changes it."""
    from PIL import Image
    im = Image.open(front(species))
    mask = bytes(1 if v else 0 for v in im.getdata())
    return hashlib.sha1(("%dx%d" % im.size).encode() + mask).hexdigest()[:12]


def order():
    return {a: int(b) for a, b in re.findall(r"#define SPECIES_(\w+) (\d+)\b", open(SPECIES_H).read())}


def render(rows):
    num = order()
    lifted = sorted((sp for sp, r in rows.items() if r["floats"]), key=lambda s: num[s])
    return HEAD + "".join("    [SPECIES_%s] = %d,\n" % (sp, rows[sp]["lift"]) for sp in lifted) + "};\n"


def problems(data, table_text):
    rows, bad = data["species"], []
    num = order()
    for sp, r in rows.items():
        if sp not in num:
            bad.append("%s: no such species" % sp)
        elif r["floats"] and not r.get("lift"):
            bad.append("%s (%s) is decided floating but has no lift" % (sp, r["daemon"]))
        elif not r["floats"] and r.get("lift"):
            bad.append("%s (%s) is decided grounded but carries a lift of %d" % (sp, r["daemon"], r["lift"]))
        elif r["floats"] and r.get("front") != silhouette(sp):
            bad.append("%s (%s) floats, and its front was redrawn since that was decided (%s): look at it, then --stamp"
                       % (sp, r["daemon"], "never stamped" if not r.get("front") else "was " + r["front"]))
    for sp, v in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*(\d+)", table_text):
        r = rows.get(sp)
        if int(v) and not (r and r["floats"]):
            bad.append("%s%s is lifted %spx in the engine but is not decided floating: a drawing on the ground hangs "
                       "over its shadow" % (sp, " (%s)" % r["daemon"] if r else "", v))
    if table_text != render(rows):
        bad.append("enemy_mon_elevation.h is not what --write makes from daemon_float.json")
    return bad


def main():
    data = json.load(open(DATA))
    rows = data["species"]
    if "--stamp" in sys.argv:
        for sp, r in rows.items():
            r["front"] = silhouette(sp)
        tmp = DATA + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=1)
            f.write("\n")
        os.replace(tmp, DATA)
        print("  stamped %d drawings as decided" % len(rows))
        return 0
    text = open(TABLE, encoding="utf-8").read()
    floats = sorted((r["daemon"], r["lift"]) for r in rows.values() if r["floats"])
    if "--write" in sys.argv:
        new = render(rows)
        if new != text:
            open(TABLE, "w", encoding="utf-8").write(new)
            print("  wrote %s: %d lifted" % (os.path.relpath(TABLE, ROOT), len(floats)))
        else:
            print("  %s already right: %d lifted" % (os.path.relpath(TABLE, ROOT), len(floats)))
        text = new
    bad = problems(data, text)
    print("  %d decided, %d float: %s" % (len(rows), len(floats), ", ".join("%s %d" % f for f in floats)))
    if bad:
        print("  %d problem%s:" % (len(bad), "" if len(bad) == 1 else "s"))
        for b in bad:
            print("     " + b)
        return 1
    print("  every lift in the engine belongs to a daemon drawn off the ground.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
