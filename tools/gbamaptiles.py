#!/usr/bin/env python3
"""Read a map's collision out of its own blockdata.

    python3 tools/gbamaptiles.py <MapName> [x y radius]

Two tickets were blocked on the same sentence -- "needs knowing which tiles are
walkable / which are display cases" -- and both were guessing at a thing the
repository already stores. A layout's map.bin is one u16 per tile: the low ten
bits are the metatile and bits 10-11 are the COLLISION, where 0 is passable.

So placing an NPC or a signpost is a lookup, not a playtest. Derive, don't
assert -- the same habit that has made every tool in here that reads the game's
own data need no revision.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")


def layout_of(mapname):
    m = json.load(open(os.path.join(GBA, "data/maps", mapname, "map.json")))
    for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]:
        if isinstance(l, dict) and l.get("id") == m["layout"]:
            return m, l
    raise SystemExit("  !! no layout for %s" % mapname)


def grid(layout):
    raw = open(os.path.join(GBA, layout["blockdata_filepath"]), "rb").read()
    w, h = layout["width"], layout["height"]
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            v = int.from_bytes(raw[2 * (y * w + x):2 * (y * w + x) + 2], "little")
            row.append((v >> 10) & 3)          # collision: 0 = you can stand here
        out.append(row)
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    mapname = sys.argv[1]
    m, layout = layout_of(mapname)
    g = grid(layout)
    taken = {(o["x"], o["y"]) for o in m.get("object_events", [])}
    print("  %s -- %dx%d, %d object(s)" % (mapname, layout["width"], layout["height"], len(taken)))
    for o in m.get("object_events", []):
        print("     %-42s at %d,%d" % (o.get("script", "-")[-42:], o["x"], o["y"]))

    if len(sys.argv) >= 4:
        cx, cy = int(sys.argv[2]), int(sys.argv[3])
        r = int(sys.argv[4]) if len(sys.argv) > 4 else 4
        print("\n  around %d,%d   . = free, # = blocked, o = an object already there" % (cx, cy))
        print("        " + "".join(str(x % 10) for x in range(max(0, cx - r), min(layout["width"], cx + r + 1))))
        for y in range(max(0, cy - r), min(layout["height"], cy + r + 1)):
            row = "".join("o" if (x, y) in taken else ("." if g[y][x] == 0 else "#")
                          for x in range(max(0, cx - r), min(layout["width"], cx + r + 1)))
            print("   %4d %s" % (y, row))
    return 0


sys.exit(main())
