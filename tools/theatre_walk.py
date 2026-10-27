#!/usr/bin/env python3
"""Walk the theatre's player somewhere, reliably (the 5 October game loop).

    python3 tools/theatre_walk.py ping                   # is the theatre answering? (a few seconds at most)
    python3 tools/theatre_walk.py where                  # the map and the tile the player stands on
    python3 tools/theatre_walk.py to X Y                 # walk to (X, Y) on this map
    python3 tools/theatre_walk.py warp MAP_DEST          # walk into this map's warp to MAP_DEST
    python3 tools/theatre_walk.py edge up|down|left|right   # walk off this map's edge, onto the next
    python3 tools/theatre_walk.py flag 0x302 [0|1]       # read a flag, or set it -- to replay a scene on a scratch save
    ... --release                                         # the theatre is running the release ROM, not the debug one
    ... --timeout SECONDS                                 # give up on the whole command after this long (default 600)

WHY. Driving the theatre by held buttons alone went wrong all morning: a 16-frame hold sometimes only turns the
player and sometimes carries it two tiles, a wild battle swallows the next twenty presses, and a text box holds the
player still while the script thinks it is walking. Each of those cost a round of screenshots to notice. This plans
a path from the map's own collision (its layout's map.bin, ledges one way, the people who stand still), then takes it
ONE TILE AT A TIME, reading the player's position back after every step: a turn is pressed again, a battle is run
from (or, if it cannot be run from, fought with A), a text box is closed with B, and a step that was blocked -- a
person who walked into the way -- marks that tile and plans again.

It reads RAM through the theatre's own `peek` (tools/theatre.lua), so the theatre must be open with its script
loaded. Addresses come from the build's .map, so it follows a rebuild.

NOTHING HERE WAITS FOREVER (T-451, 2026-10-27). Every batch has a time limit worked out from the frames it holds (a
theatre that does not answer one raises TheatreDown at once, instead of run.sh's five silent minutes); every command
-- and every route stop, tools/theatre_route.py -- runs inside `limit()`, a wall clock that fails it with a message
when it runs out; every loop counts its tries. Every command begins with `ping` (a one-frame batch, PING_SECONDS),
so a theatre whose script is not running fails in seconds: "the theatre is not answering: re-run theatre.lua".

WARPS FIRE WHERE THE GAME SAYS, NOT WHERE THE PICTURE DOES (T-451). A door mat is three warp events, but only the tile
whose BEHAVIOUR is an arrow warp fires, and only on pressing the arrow's way (src/field_control_avatar.c,
TryArrowWarp): the GAME CORNER's is the mat's LEFT end (9,13), the restaurant's the middle (6,9). The walker used to
pick "the middle of the mat" and, having arrived on it sideways, press once more the way it arrived -- which on a mat
is a step off it, and back, for four hundred steps. It now walks to the tile that fires and presses the way that
fires it (`Map.fires`). The follower (src/daemons_follower.c) never mattered: it is a sprite, not an object event,
and blocks nothing, so the walker plans straight through it and the game agrees.
"""
import contextlib, json, os, re, struct, subprocess, sys, time
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
THEATRE = os.path.join(ROOT, ".theatre")
DIRS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
JUMP = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}       # MB_JUMP_EAST, WEST, NORTH, SOUTH
ICE, CRACKED_ICE = 0x23, 0x27            # MB_ICE slides you on until something stops you; cracked ice drops you a floor
#  Which warp tiles fire, and how (src/field_control_avatar.c): an arrow warp on pressing its way while standing on it
#  (TryArrowWarp), a sideways stair on pressing along it (IsDirectionalStairWarpMetatileBehavior), the rest on being
#  stepped onto (IsWarpMetatileBehavior; MB_WARP_DOOR also from below, pressing UP, TryDoorWarp). A warp event on any
#  other tile -- a mat's ends, mostly -- never fires.
PRESS_WARP = {0x62: "RIGHT", 0x63: "LEFT", 0x64: "UP", 0x65: "DOWN",        # MB_EAST/WEST/NORTH/SOUTH_ARROW_WARP
              0x6C: "RIGHT", 0x6E: "RIGHT", 0x6D: "LEFT", 0x6F: "LEFT"}     # MB_UP/DOWN_RIGHT/LEFT_STAIR_WARP
STEP_WARP = {0x60, 0x61, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x71}  # cave door, ladder, fall, warp pad, lavaridge, door,
                                                                     # escalators, union room
SURFABLE = {0x10, 0x11, 0x12, 0x13, 0x15, 0x1A, 0x1B, 0x50, 0x51, 0x52, 0x53}   # sBehaviorSurfable
SURFING = 1 << 3                         # PLAYER_AVATAR_FLAG_SURFING, gPlayerAvatar.flags
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

# -- time limits (T-451) ---------------------------------------------------------------------------------------------
PING_SECONDS = 5          # a one-frame batch: the script polls every 10 frames, so a live theatre answers in ~0.2 s
BATCH_SLACK = 10          # seconds on top of a batch's own frames ...
BATCH_FACTOR = 3          # ... and its frames counted this many times over (a theatre in the background runs slow)
LOAD_FRAMES = 600         # a `load`, `reset` or `loadstate` counted as ten seconds of frames
WALK_SECONDS = 300        # one `to` / `warp` / `edge` walk
COMMAND_SECONDS = 600     # one theatre_walk.py command, from the command line
BATTLE_SECONDS = 240      # clearing one battle


class TheatreError(RuntimeError):
    """The theatre refused a batch, or a time limit ran out: the stop fails, the route goes on."""


class TheatreTimeout(TheatreError):
    """A limit() ran out: the walk or the stop took too long."""


class TheatreDown(TheatreError):
    """A batch was not answered: nothing that follows can work, so a route stops here."""


_limits = []                                          # [(deadline, what, seconds)], innermost last


@contextlib.contextmanager
def limit(seconds, what):
    """Everything sent to the theatre inside this must finish within SECONDS of wall clock, or TheatreTimeout says
    WHAT ran out. Limits nest: the nearest deadline wins."""
    _limits.append((time.monotonic() + seconds, what, seconds))
    try:
        yield
    finally:
        _limits.pop()


def check_time():
    now = time.monotonic()
    for deadline, what, seconds in _limits:
        if now > deadline:
            raise TheatreTimeout("%s ran past its limit of %d s -- stopped there rather than wait on" % (what, seconds))


def remaining():
    """Seconds left before the nearest limit, or None with none set."""
    return min((d - time.monotonic() for d, _, _ in _limits), default=None)


def batch_frames(cmds):
    """The frames a batch holds the theatre for: its holds, waits, bursts and traces, one for anything else."""
    n = 0
    for c in cmds:
        w = c.split()
        try:
            if w[0] in ("hold", "wait"):
                n += int(w[-1])
            elif w[0] == "burst":
                n += int(w[2]) * int(w[3])
            elif w[0] in ("pburst", "trace"):
                n += int(w[2])
            elif w[0] in ("load", "reset", "loadstate", "savestate", "reload"):
                n += LOAD_FRAMES
            else:
                n += 1
        except (IndexError, ValueError):
            n += 1
    return n


def not_answering(seconds):
    """Why a batch went unanswered, as far as can be told from here."""
    try:
        procs = subprocess.run(["pgrep", "-fl", "mGBA"], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        procs = None
    if procs is not None and ".theatre" not in procs:
        return ("the theatre is not answering (nothing in %d s): no theatre mGBA is running -- start it with "
                "tools/theatre_start.sh, then run theatre.lua in it (engine.md 5)" % seconds)
    return ("the theatre is not answering (nothing in %d s): re-run theatre.lua in mGBA -- Tools > Scripting..., "
            "dofile(\"%s\") -- and check its window is not paused" % (seconds, os.path.join(ROOT, "tools", "theatre.lua")))


def send(cmds, timeout):
    """Write one batch (atomically: a half-written file once read as "0 commands"), then wait for theatre.done to
    name it -- at most TIMEOUT seconds. Returns theatre.done's line."""
    os.makedirs(THEATRE, exist_ok=True)
    bid = "%d" % time.time_ns()
    tmp, cmd, done = (os.path.join(THEATRE, f) for f in ("theatre.cmd.tmp", "theatre.cmd", "theatre.done"))
    with open(tmp, "w") as f:
        f.write("id %s\n" % bid + "".join(c + "\n" for c in cmds))
    os.replace(tmp, cmd)
    end = time.monotonic() + timeout
    while True:
        try:
            line = open(done).read()
        except OSError:
            line = ""
        if line.startswith("done %s" % bid) and (len(line) == 5 + len(bid) or line[5 + len(bid)] in " \n"):
            return line
        if time.monotonic() > end:
            return None
        time.sleep(0.05)


def run(*cmds):
    """One batch. A ROM path is made absolute before it is sent; theatre.lua refuses a relative one, and any address
    outside the GBA's memory map, and says so in theatre.done ("done N refused: ..."), raised here (2026-10-21).
    Bounded (T-451): a batch gets its own frames' worth of time, three times over plus ten seconds, and never more than
    the nearest limit() has left. Unanswered, it raises TheatreDown; past a limit, TheatreTimeout."""
    cmds = [("%s %s" % (c.split(" ", 1)[0], os.path.abspath(c.split(" ", 1)[1])))
            if c.split(" ", 1)[0] in ("load", "savestate", "loadstate") and " " in c else c for c in cmds]
    check_time()
    own = BATCH_SLACK + BATCH_FACTOR * batch_frames(cmds) / 60.0
    left = remaining()
    timeout = own if left is None else max(0.5, min(own, left))
    done = send(cmds, timeout)
    if done is None:
        check_time()                                   # the stop's own limit ran out while this batch played
        raise TheatreDown(not_answering(timeout))
    if " refused: " in done:
        raise TheatreError("theatre: " + done.strip())


def ping(seconds=PING_SECONDS):
    """A one-frame batch: answered in a fraction of a second by a live theatre, or TheatreDown in SECONDS."""
    if send(["wait 1"], seconds) is None:
        raise TheatreDown(not_answering(seconds))


def symbol(name, release):
    m = open(os.path.join(GBA, "daemonsContent.map" if release else "daemonsContent_debug.map")).read()
    hit = re.search(r"^\s+(0x[0-9a-f]+)\s+%s( = \.)?$" % re.escape(name), m, re.M)   # "= ." or a bare symbol
    if not hit:
        sys.exit("theatre_walk: no symbol %s in the build's .map -- build it first" % name)
    return int(hit.group(1), 16)


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
        self.release = release
        self.sb1 = symbol("gSaveBlock1Ptr", release)
        self.main = symbol("gMain", release)
        self.avatar = symbol("gPlayerAvatar", release)

    p = None

    def state(self):
        # gSaveBlock1Ptr moves only when a map loads: read it once, and again after the map changes (three times at
        # most: a map still loading reads as a new one each time, and the last read stands)
        for tries in range(3):
            if self.p is None:
                self.p = peek([(32, self.sb1, "sb1")])["sb1"]
            p = self.p
            s = peek([(16, p, "x"), (16, p + 2, "y"), (8, p + 4, "group"), (8, p + 5, "num"),
                      (8, self.main + 0x439, "flags"),       # gMain.inBattle is bit 1 (oamLoadDisabled is bit 0)
                      (8, self.avatar, "avatar")])           # gPlayerAvatar.flags: SURFING is bit 3
            out = {"x": s["x"], "y": s["y"], "map": (s["group"], s["num"]), "battle": bool(s["flags"] & 2),
                   "surfing": bool(s["avatar"] & SURFING)}
            moved = getattr(self, "last_map", out["map"]) != out["map"]
            self.last_map = out["map"]
            if not moved:
                break
            self.p = None                                                # a new map: read the pointer again
        return out


def map_name(group, num):
    groups = json.load(open(os.path.join(GBA, "data/maps/map_groups.json")))
    return groups[groups["group_order"][group]][num]


class Map:
    def __init__(self, name, walking=False):
        """WALKING: plan as the walker takes the path -- around every warp that fires on being stepped on (a ladder or
        a door crossed on the way would take the player off the map), and, on foot, around water (T-451: a path along
        a shore -- QUICKSILVER's -- could press into the sea a tile at a time, three refusals each). Set `on_foot` from the game."""
        self.name = name
        self.walking, self.on_foot = walking, True
        m = json.load(open(os.path.join(GBA, "data/maps", name, "map.json")))
        lay = {l["id"]: l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if l}[m["layout"]]
        self.json, self.W, self.H = m, lay["width"], lay["height"]
        self.bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read()
        self.attrs = self._attrs(lay)
        self.still = {(o["x"], o["y"]) for o in m.get("object_events") or []
                      if "WANDER" not in str(o.get("movement_type", ""))}
        # a scene's trigger tile: walked around when there is another way (CINNABAR's "The door is locked..." steps the
        # player back, and a path through it is re-planned through it forever), crossed only when there is not
        self.triggers = {(c["x"], c["y"]) for c in m.get("coord_events") or [] if c.get("type") == "trigger"}
        self.avoid_triggers = False
        self.learned = set()                                           # tiles found blocked on the way
        self.misses = {}                                               # ... and how often each refused a step
        self.warps = {(w["x"], w["y"]): w["dest_map"] for w in m.get("warp_events") or []}

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

    def fires(self, x, y):
        """How the warp event at (x, y) fires, read from its tile's behaviour as src/field_control_avatar.c does:
        ("press", DIR) -- an arrow warp or a sideways stair, pressing DIR while standing on it; ("step", None) -- on
        being stepped onto (a door also from below, pressing UP); None -- it never fires (a door mat's other tiles), or
        there is no warp here."""
        if (x, y) not in self.warps or not self.inside(x, y):
            return None
        b = self.behaviour(x, y)
        if b in PRESS_WARP:
            return ("press", PRESS_WARP[b])
        if b in STEP_WARP:
            return ("step", None)
        return None

    def open(self, x, y, goal):
        if (x, y) == goal:
            return self.inside(x, y)
        if self.avoid_triggers and (x, y) in self.triggers:
            return False
        if self.walking and self.inside(x, y):
            if (x, y) in self.warps and self.fires(x, y) == ("step", None):
                return False                                           # it would take us off the map
            if self.on_foot and self.behaviour(x, y) in SURFABLE:
                return False                                           # the sea, without SURF
        return self.inside(x, y) and not (self.cell(x, y) >> 10) & 3 and (x, y) not in self.still \
            and (x, y) not in self.learned and self.behaviour(x, y) not in JUMP and self.behaviour(x, y) != CRACKED_ICE

    def slide(self, at, dx, dy):
        """A step onto MB_ICE carries on in its direction until the next tile is not open, or the tile is not ice
        (ForcedMovement_Slip, src/field_player_avatar.c) -- so the plan must step to where it stops, not to where it
        was pressed."""
        while self.inside(*at) and self.behaviour(*at) == ICE:
            nxt = (at[0] + dx, at[1] + dy)
            if not self.open(*nxt, None):
                break
            at = nxt
        return at

    def path(self, start, goal):
        """[(dir, (x, y))] from start to goal, ledges one way -- or None. Around every scene's trigger if it can be, and
        through one only when there is no other way (the Reading Room's whole doorway is one)."""
        self.avoid_triggers = True
        try:
            around = self._path(start, goal)
        finally:
            self.avoid_triggers = False
        return around if around is not None else self._path(start, goal)

    def _path(self, start, goal):
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
                elif self.open(*n, goal):
                    n = self.slide(n, dx, dy)                           # ice: where the step actually stops
                    if n not in prev:
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
    """Run from a wild battle; if it cannot be run from (a trainer), fight it with A. Forty tries and BATTLE_SECONDS."""
    with limit(BATTLE_SECONDS, "the battle"):
        for attempt in range(40):
            s = g.state()
            if not s["battle"]:
                return
            if attempt < 2:   # RUN is the menu's bottom right (DETACH); B first to clear any text. A trainer refuses it.
                run("hold B 8", "wait 40", "hold DOWN 8", "wait 16", "hold RIGHT 8", "wait 16", "hold A 8", "wait 120",
                    "hold A 8", "wait 60", "hold A 8", "wait 40")
            else:             # fight: ROUTINES, then each of the four slots in turn (the first may be out of MP)
                slot = [[], ["RIGHT"], ["DOWN"], ["DOWN", "RIGHT"]][attempt % 4]
                run("hold B 8", "wait 30", "hold A 8", "wait 40", "hold UP 6", "wait 10", "hold LEFT 6", "wait 10",
                    *sum((["hold %s 6" % k, "wait 10"] for k in slot), []), "hold A 8", "wait 90",
                    *(["hold A 6", "wait 50"] * 4))
    sys.exit("theatre_walk: still in a battle after forty tries")


def step_toward(g, at, to):
    """One step from AT onto the neighbouring tile TO, if it is one."""
    d = next((k for k, v in DIRS.items() if (at[0] + v[0], at[1] + v[1]) == to), None)
    if d:
        run("hold %s 16" % d, "wait 30")
    return g.state()


def enter(g, m, warp, start_map):
    """Standing on a warp that has not fired. If its tile says how it fires (Map.fires), press exactly that: an arrow
    warp's way, a stair's along, a door's UP -- and nothing else, since any other press on a mat is a step off it
    (T-451). Only a warp whose tile says nothing is tried each way in turn, closed sides first, stepping back on
    whenever a press took us off. Bounded: three presses of the known way, then one of each other way."""
    s = g.state()
    if (s["x"], s["y"]) != warp:                                         # beside it: onto it first
        s = step_toward(g, (s["x"], s["y"]), warp)
        if s["map"] != start_map:
            return s
    how = m.fires(*warp)
    known = [how[1]] if how and how[0] == "press" else []    # a step-on warp fires by stepping off and back on

    def closed(d):
        n = (warp[0] + DIRS[d][0], warp[1] + DIRS[d][1])
        return not m.open(*n, None)
    rest = sorted((d for d in ("DOWN", "UP", "LEFT", "RIGHT") if d not in known), key=lambda d: not closed(d))
    for d in known * 3 + ([] if known else rest):                       # a warp wants the button held
        if (s["x"], s["y"]) != warp:
            s = step_toward(g, (s["x"], s["y"]), warp)                  # a press took us off: back on
            if s["map"] != start_map:
                return s
            if (s["x"], s["y"]) != warp:
                break
        run("hold %s 24" % d, "wait 90")
        s = g.state()
        if s["map"] != start_map:
            return s
        if s["battle"]:
            clear_battle(g)
            s = g.state()
    sys.exit("theatre_walk: the warp at %s on %s did not take me (%s; standing on %s)"
             % (warp, m.name, "pressed %s" % known[0] if known else
                "its tile's behaviour 0x%02X fires nothing: pressed every way" % m.behaviour(*warp), (s["x"], s["y"])))


def walk(g, goal, into_warp=False):
    """Walk to GOAL one tile at a time (and with INTO_WARP, through the warp there). Bounded three ways: 400 steps,
    WALK_SECONDS of wall clock, and twelve arrivals on any one tile (standing still is not an arrival) -- a walk that keeps coming back to the same place
    is going round in a circle (T-451's mat: off it and back on it for four hundred steps)."""
    s = g.state()
    m = Map(map_name(*s["map"]), walking=True)
    start_map = s["map"]
    seen, last = {}, None
    with limit(WALK_SECONDS, "walking to %s on %s" % (goal, m.name)):
        for _ in range(400):
            here = (s["x"], s["y"])
            if here != last:                                             # an arrival (standing still -- a scene holding
                seen[here] = seen.get(here, 0) + 1                       # us -- is bounded by the steps and the clock)
                last = here
            if seen[here] > 12:
                sys.exit("theatre_walk: back on %s twelve times on the way to %s on %s -- going in a circle"
                         % (here, goal, m.name))
            m.on_foot = not s["surfing"]
            if here == goal and not into_warp:
                return s
            if here == goal and into_warp:
                return enter(g, m, goal, start_map)
            route = m.path(here, goal)
            if not route and m.learned:                                  # a scene may have held us: forget, clear, retry
                m.learned.clear(); m.misses.clear()
                run(*(["hold B 6", "wait 40"] * 4))
                route = m.path(here, goal)
            if not route:
                sys.exit("theatre_walk: no way from %s to %s on %s%s" % (here, goal, m.name,
                         "" if s["surfing"] else " on foot"))
            d, nxt = route[0]
            if os.environ.get("WALK_DEBUG"):
                print("  at %s -> %s %s (%d to go)%s" % (here, d, nxt, len(route), " surfing" if s["surfing"] else ""),
                      flush=True)
            #  T-436: surfing covers a tile in 8 frames, so a 12-frame hold carried the player on past it. A 4-frame tap
            #  turns the player (the next try steps) or, facing that way already, starts exactly one tile.
            press = ("hold %s 4" % d, "wait 20") if s["surfing"] else ("hold %s 12" % d, "wait 16")
            for tries in range(4):
                run(*press)                                              # a turn, or one tile (8 frames could only turn on a mat)
                s = g.state()
                for _slide in range(64):                                 # still sliding on ice: wait it out
                    if m.behaviour(s["x"], s["y"]) != ICE or s["map"] != start_map:
                        break
                    run("wait 16")
                    t = g.state()
                    if (t["x"], t["y"]) == (s["x"], s["y"]):
                        break
                    s = t
                if s["map"] != start_map:
                    return s                                             # a warp, or the next map
                if s["battle"]:
                    clear_battle(g)
                    s = g.state()
                    break
                if (s["x"], s["y"]) != here:
                    break
            else:
                if (s["x"], s["y"]) == here:                             # held still: a box open, or blocked
                    run("hold B 6", "wait 30")
                    s = g.state()
                    if (s["x"], s["y"]) == here:                         # three refusals make a wall
                        m.misses[nxt] = m.misses.get(nxt, 0) + 1
                        if m.misses[nxt] >= 3:
                            m.learned.add(nxt)
            #  (T-451) No extra press here on reaching a warp: the next turn of the loop is enter(), which presses the
            #  way the tile fires. The press that was here repeated the arriving step -- off a mat reached sideways.
    sys.exit("theatre_walk: gave up after 400 steps")


def choose_warp(m, here, dest):
    """Of this map's warps to DEST, the one to walk into: a tile that fires (Map.fires) before one that never does,
    then the nearest. Only when no tile says it fires is the old guess kept -- the mat's middle (a warp with another
    beside it), which is right for most houses' mats and wrong for the GAME CORNER's (T-451)."""
    hits = [w for w in m.json.get("warp_events") or [] if w["dest_map"] == dest]
    if not hits:
        return None
    tiles = {(w["x"], w["y"]) for w in hits}

    def cost(w):
        p = m.path(here, (w["x"], w["y"]))
        beside = sum((w["x"] + dx, w["y"]) in tiles for dx in (-1, 1))
        return (p is None, m.fires(w["x"], w["y"]) is None, -beside, len(p or ()))
    return min(hits, key=cost)


def flag(g, f, value=None):
    """Read a flag, or set it (value 0/1) and read it back. FireRed's flags are in SaveBlock1 (+0xEE0); DAEMONS' own,
    from 0x900, in SaveBlock2 (+0xEA0)."""
    if f < 0x900:
        base, f2 = peek([(32, g.sb1, "p")])["p"] + 0xEE0, f
    else:
        base, f2 = peek([(32, symbol("gSaveBlock2Ptr", g.release), "p")])["p"] + 0xEA0, f - 0x900
    addr, bit = base + (f2 >> 3), 1 << (f2 & 7)
    byte = peek([(8, addr, "b")])["b"]
    if value is not None:
        byte = byte | bit if value else byte & ~bit
        run("poke8 %s %d" % (hex(addr), byte))
        byte = peek([(8, addr, "b")])["b"]
    return bool(byte & bit)


def main():
    args = sys.argv[1:]
    seconds = COMMAND_SECONDS
    if "--timeout" in args:
        k = args.index("--timeout")
        seconds = float(args[k + 1])
        del args[k:k + 2]
    a = [x for x in args if x != "--release"]
    try:
        ping()                                              # seconds, not minutes, when nothing is listening
    except TheatreDown as e:
        sys.exit("theatre_walk: %s" % e)
    if a and a[0] == "ping":
        print("the theatre is answering")
        return
    g = Game("--release" in args)
    try:
        with limit(seconds, "theatre_walk %s" % " ".join(a)):
            command(g, a)
    except TheatreError as e:
        sys.exit("theatre_walk: %s" % e)


def command(g, a):
    if not a or a[0] == "where":
        s = g.state()
        print("%s (%d, %d)%s%s" % (map_name(*s["map"]), s["x"], s["y"], "  IN A BATTLE" if s["battle"] else "",
                                   "  SURFING" if s["surfing"] else ""))
        return
    if a[0] == "flag":
        f = int(a[1], 0)
        print("flag %s is %s" % (hex(f), "set" if flag(g, f, int(a[2]) if len(a) > 2 else None) else "clear"))
        return
    s = g.state()
    m = Map(map_name(*s["map"]), walking=True)
    m.on_foot = not s["surfing"]
    if a[0] == "to":
        s = walk(g, (int(a[1]), int(a[2])))
    elif a[0] == "warp":
        best = choose_warp(m, (s["x"], s["y"]), a[1])
        if not best:
            sys.exit("theatre_walk: %s has no warp to %s" % (m.name, a[1]))
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
