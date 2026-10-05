#!/usr/bin/env python3
"""Walk the theatre's player somewhere, reliably (the 5 October game loop).

    python3 tools/theatre_walk.py where                  # the map and the tile the player stands on
    python3 tools/theatre_walk.py to X Y                 # walk to (X, Y) on this map
    python3 tools/theatre_walk.py warp MAP_DEST          # walk into this map's warp to MAP_DEST
    python3 tools/theatre_walk.py edge up|down|left|right   # walk off this map's edge, onto the next
    ... --release                                         # the theatre is running the release ROM, not the debug one

WHY. Driving the theatre by held buttons alone went wrong all morning: a 16-frame hold sometimes only turns the
player and sometimes carries it two tiles, a wild battle swallows the next twenty presses, and a text box holds the
player still while the script thinks it is walking. Each of those cost a round of screenshots to notice. This plans
a path from the map's own collision (its layout's map.bin, ledges one way, the people who stand still), then takes it
ONE TILE AT A TIME, reading the player's position back after every step: a turn is pressed again, a battle is run
from (or, if it cannot be run from, fought with A), a text box is closed with B, and a step that was blocked -- a
person who walked into the way -- marks that tile and plans again.

It reads RAM through the theatre's own `peek` (tools/theatre.lua), so the theatre must be open with its script
loaded. Addresses come from the build's .map, so it follows a rebuild.
"""
import json, os, re, struct, subprocess, sys, time
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
THEATRE = os.path.join(ROOT, ".theatre")
DIRS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
JUMP = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}       # MB_JUMP_EAST, WEST, NORTH, SOUTH


def symbol(name, release):
    m = open(os.path.join(GBA, "daemonsContent.map" if release else "daemonsContent_debug.map")).read()
    hit = re.search(r"^\s+(0x[0-9a-f]+)\s+%s = \.$" % re.escape(name), m, re.M)
    if not hit:
        sys.exit("theatre_walk: no symbol %s in the build's .map -- build it first" % name)
    return int(hit.group(1), 16)


def run(*cmds):
    subprocess.run([os.path.join(THEATRE, "run.sh"), *cmds], check=True)


def peek(reads):
    """reads: [(bits, address, name)] -> {name: value}, all in one batch."""
    path = os.path.join(THEATRE, "peek.txt")
    if os.path.exists(path):
        os.remove(path)
    run(*["peek %d %s %s" % (b, hex(a), n) for b, a, n in reads])
    out = {}
    for line in open(path):
        k, v = line.split()
        out[k] = int(v, 16)
    return out


class Game:
    def __init__(self, release):
        self.sb1 = symbol("gSaveBlock1Ptr", release)
        self.main = symbol("gMain", release)

    p = None

    def state(self):
        # gSaveBlock1Ptr moves only when a map loads: read it once, and again after the map changes
        if self.p is None:
            self.p = peek([(32, self.sb1, "sb1")])["sb1"]
        p = self.p
        s = peek([(16, p, "x"), (16, p + 2, "y"), (8, p + 4, "group"), (8, p + 5, "num"),
                  (8, self.main + 0x439, "flags")])          # gMain.inBattle is bit 1 (oamLoadDisabled is bit 0)
        out = {"x": s["x"], "y": s["y"], "map": (s["group"], s["num"]), "battle": bool(s["flags"] & 2)}
        if getattr(self, "last_map", out["map"]) != out["map"]:
            self.p = None                                                # a new map: read the pointer again
            self.last_map = out["map"]
            return self.state()
        self.last_map = out["map"]
        return out


def map_name(group, num):
    groups = json.load(open(os.path.join(GBA, "data/maps/map_groups.json")))
    return groups[groups["group_order"][group]][num]


class Map:
    def __init__(self, name):
        self.name = name
        m = json.load(open(os.path.join(GBA, "data/maps", name, "map.json")))
        lay = {l["id"]: l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l}[m["layout"]]
        self.json, self.W, self.H = m, lay["width"], lay["height"]
        self.bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read()
        self.attrs = self._attrs(lay)
        self.still = {(o["x"], o["y"]) for o in m.get("object_events") or []
                      if "WANDER" not in str(o.get("movement_type", ""))}
        self.learned = set()                                           # tiles found blocked on the way
        self.misses = {}                                               # ... and how often each refused a step

    def _attrs(self, lay):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from check_reach import _tdir                                    # the same tileset lookup check_reach uses
        out = []
        for symbol, kind in ((lay["primary_tileset"], "primary"), (lay["secondary_tileset"], "secondary")):
            d = _tdir(GBA, symbol, kind)
            f = d and os.path.join(d, "metatile_attributes.bin")
            out.append(open(f, "rb").read() if f and os.path.exists(f) else b"")
        return out

    def cell(self, x, y):
        return struct.unpack_from("<H", self.bd, (y * self.W + x) * 2)[0]

    def behaviour(self, x, y):
        mt = self.cell(x, y) & 0x3FF
        a, k = (self.attrs[0], mt) if mt < 640 else (self.attrs[1], mt - 640)
        return struct.unpack_from("<I", a, k * 4)[0] & 0x1FF if (k + 1) * 4 <= len(a) else 0

    def inside(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def open(self, x, y, goal):
        if (x, y) == goal:
            return self.inside(x, y)
        return self.inside(x, y) and not (self.cell(x, y) >> 10) & 3 and (x, y) not in self.still \
            and (x, y) not in self.learned and self.behaviour(x, y) not in JUMP

    def path(self, start, goal):
        """[(dir, (x, y))] from start to goal, ledges one way -- or None."""
        prev, todo = {start: None}, deque([start])
        while todo:
            c = todo.popleft()
            if c == goal:
                break
            for d, (dx, dy) in DIRS.items():
                n = (c[0] + dx, c[1] + dy)
                if self.inside(*n) and self.behaviour(*n) in JUMP and JUMP[self.behaviour(*n)] == (dx, dy):
                    n2 = (n[0] + dx, n[1] + dy)                         # a ledge: over it, two tiles, one way
                    if n2 not in prev and self.open(*n2, goal):
                        prev[n2] = (c, d)
                        todo.append(n2)
                elif n not in prev and self.open(*n, goal):
                    prev[n] = (c, d)
                    todo.append(n)
        if goal not in prev:
            return None
        out, c = [], goal
        while prev[c]:
            p, d = prev[c]
            out.append((d, c))
            c = p
        return out[::-1]


def clear_battle(g):
    """Run from a wild battle; if it cannot be run from (a trainer), fight it with A."""
    for attempt in range(40):
        s = g.state()
        if not s["battle"]:
            return
        if attempt < 2:       # RUN is the menu's bottom right (DETACH); B first to clear any text. A trainer refuses it.
            run("hold B 8", "wait 40", "hold DOWN 8", "wait 16", "hold RIGHT 8", "wait 16", "hold A 8", "wait 120",
                "hold A 8", "wait 60", "hold A 8", "wait 40")
        else:                 # fight: ROUTINES, then each of the four slots in turn (the first may be out of MP)
            slot = [[], ["RIGHT"], ["DOWN"], ["DOWN", "RIGHT"]][attempt % 4]
            run("hold B 8", "wait 30", "hold A 8", "wait 40", "hold UP 6", "wait 10", "hold LEFT 6", "wait 10",
                *sum((["hold %s 6" % k, "wait 10"] for k in slot), []), "hold A 8", "wait 90",
                *(["hold A 6", "wait 50"] * 4))
    sys.exit("theatre_walk: still in a battle after forty tries")


OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}


def enter(g, m, warp, start_map):
    """Standing on a warp that has not fired: a door mat fires on pressing out through it, FireRed's sideways stairs
    (the museum's) on pressing along them -- so press each way in turn, stepping back on whenever a press took us off."""
    s = g.state()
    if (s["x"], s["y"]) != warp:                                         # on the mat's end: onto its middle first
        dx, dy = warp[0] - s["x"], warp[1] - s["y"]
        if abs(dx) + abs(dy) == 1:
            run("hold %s 16" % next(d for d, v in DIRS.items() if v == (dx, dy)), "wait 30")
    # a mat or a door fires on pressing OUT through it -- toward the wall, or off the map -- so those sides first
    def closed(d):
        n = (warp[0] + DIRS[d][0], warp[1] + DIRS[d][1])
        return not m.open(*n, None)
    for d in sorted(("DOWN", "UP", "LEFT", "RIGHT"), key=lambda d: not closed(d)):
        run("hold %s 24" % d, "wait 90")                               # a warp wants the button held
        s = g.state()
        if s["map"] != start_map:
            return s
        if (s["x"], s["y"]) != warp:                                     # it stepped off: back on, try the next way
            run("hold %s 24" % OPPOSITE[d], "wait 60")
            s = g.state()
            if s["map"] != start_map:
                return s
    sys.exit("theatre_walk: the warp at %s on %s did not take me" % (warp, m.name))


def walk(g, goal, into_warp=False):
    s = g.state()
    m = Map(map_name(*s["map"]))
    start_map = s["map"]
    for _ in range(400):
        here = (s["x"], s["y"])
        if here == goal and not into_warp:
            return s
        if here == goal and into_warp:
            return enter(g, m, goal, start_map)
        route = m.path(here, goal)
        if not route and m.learned:                                      # a scene may have held us: forget, clear, retry
            m.learned.clear(); m.misses.clear()
            run(*(["hold B 6", "wait 40"] * 4))
            route = m.path(here, goal)
        if not route:
            sys.exit("theatre_walk: no way from %s to %s on %s" % (here, goal, m.name))
        d, nxt = route[0]
        if os.environ.get("WALK_DEBUG"):
            print("  at %s -> %s %s (%d to go)" % (here, d, nxt, len(route)), flush=True)
        for tries in range(4):
            run("hold %s 12" % d, "wait 16")                             # a turn, or one tile (8 frames could only turn on a mat)
            s = g.state()
            if s["map"] != start_map:
                return s                                                 # a warp, or the next map
            if s["battle"]:
                clear_battle(g)
                s = g.state()
                break
            if (s["x"], s["y"]) != here:
                break
        else:
            if (s["x"], s["y"]) == here:                                 # held still: a box open, or blocked
                run("hold B 6", "wait 30")
                s = g.state()
                if (s["x"], s["y"]) == here:                             # three refusals make a wall
                    m.misses[nxt] = m.misses.get(nxt, 0) + 1
                    if m.misses[nxt] >= 3:
                        m.learned.add(nxt)
        if into_warp and (s["x"], s["y"]) == goal:
            run("hold %s 8" % d, "wait 90")                              # on the mat or the stairs: once more
            s = g.state()
            if s["map"] != start_map:
                return s
    sys.exit("theatre_walk: gave up after 400 steps")


def main():
    a = [x for x in sys.argv[1:] if x != "--release"]
    g = Game("--release" in sys.argv)
    if not a or a[0] == "where":
        s = g.state()
        print("%s (%d, %d)%s" % (map_name(*s["map"]), s["x"], s["y"], "  IN A BATTLE" if s["battle"] else ""))
        return
    s = g.state()
    m = Map(map_name(*s["map"]))
    if a[0] == "to":
        s = walk(g, (int(a[1]), int(a[2])))
    elif a[0] == "warp":
        hits = [w for w in m.json.get("warp_events") or [] if w["dest_map"] == a[1]]
        if not hits:
            sys.exit("theatre_walk: %s has no warp to %s" % (m.name, a[1]))
        here = (s["x"], s["y"])
        # the middle of a mat (a warp with another warp beside it) fires; an end tile often does not
        tiles = {(w["x"], w["y"]) for w in hits}
        def cost(w):
            p = m.path(here, (w["x"], w["y"]))
            beside = sum((w["x"] + dx, w["y"]) in tiles for dx in (-1, 1))
            return (p is None, -beside, len(p or ()))
        best = min(hits, key=cost)
        s = walk(g, (best["x"], best["y"]), into_warp=True)
    elif a[0] == "edge":
        dx, dy = DIRS[a[1].upper()]
        here = (s["x"], s["y"])
        if dx:
            col = 0 if dx < 0 else m.W - 1
            cands = [(col, y) for y in range(m.H) if m.open(col, y, None)]
        else:
            row = 0 if dy < 0 else m.H - 1
            cands = [(x, row) for x in range(m.W) if m.open(x, row, None)]
        cands = [c for c in cands if m.path(here, c)]
        if not cands:
            sys.exit("theatre_walk: no way to the %s edge of %s" % (a[1], m.name))
        goal = min(cands, key=lambda c: len(m.path(here, c)))
        s = walk(g, goal)
        for _ in range(3):                                               # off the edge, onto the next map
            run("hold %s 8" % a[1].upper(), "wait 30")
            s = g.state()
            if map_name(*s["map"]) != m.name:
                break
    else:
        sys.exit(__doc__)
    print("%s (%d, %d)" % (map_name(*s["map"]), s["x"], s["y"]))


if __name__ == "__main__":
    main()
