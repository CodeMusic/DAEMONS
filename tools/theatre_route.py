#!/usr/bin/env python3
"""Play a route through the theatre, stop by stop, and write what it saw (T-378, the 6 October work-day run).

    python3 tools/theatre_route.py tools/routes/field-test.json            # play every stop
    python3 tools/theatre_route.py tools/routes/field-test.json --from 4   # from the fourth stop on
    python3 tools/theatre_route.py tools/routes/field-test.json --only 2,5
    python3 tools/theatre_route.py --check tools/routes/field-test.json    # parse it and resolve every name; no theatre

A route is JSON: {"rom": "debug" | "release", "about": "...", "stops": [{"stop": "a name", "steps": [...]}]}, and each
step is one line, split like a shell line:

    goto MAP_FOLDER [X Y]      the DEBUG build's theatre warp (gDaemonsDebugWarp): to (X, Y), or the map's first warp
    to X Y                     walk there on this map (tools/theatre_walk.py)
    warp MAP_DEST              walk into this map's warp to MAP_DEST
    edge up|down|left|right    walk off this map's edge
    walkto WHO                 walk beside someone and face them
    talk WHO [N]               walkto, press A, and capture each box until the script lets go -- or only N boxes,
                               leaving the script open for the presses that follow (a YES/NO, a menu)
    look X Y [N]               the same for a sign, a shelf or a PC at (X, Y): stand where it reads, face it, press A
    trigger X Y [N]            step onto a scene's trigger tile from beside it, and capture the scene to its end
                               (its battles won on a DEBUG route, fought on a release one)
    read                       capture the box on screen now, without pressing anything
    press BUTTON [N]           press it N times (default 1), forty frames apart, capturing after each
    hold BUTTON FRAMES         hold it for exact frames, capturing nothing
    wait FRAMES
    shot LABEL                 a screenshot into this stop's sheet
    flag FLAG_NAME|0xNNN 0|1   set a flag on the scratch save (to replay a scene, or reach past one)
    trainer TRAINER_NAME 0|1   set a trainer's beaten flag (0: they battle again -- a leader gives the MARK again)
    flagis FLAG_NAME|0xNNN 0|1 fail the stop unless the flag is clear (0) or set (1) -- a document that files itself
    var VAR_NAME|0x40NN N      set a var
    repel [STEPS]              no wild battles for STEPS steps (default 250)
    fight                      clear a battle: run from a wild one, fight a trainer (the walker's)
    win                        DEBUG: win the battle on screen (gBattleOutcome = 1, then a turn)
    expect MAP_FOLDER [X Y]    fail the stop unless the player is there
    music [MUS_NAME]           fail the stop unless that song is playing (default: the one the map's map.json names)
    says "TEXT"                fail the stop unless a box captured in it said TEXT (spaces and line breaks folded)

WHO is a person on the current map: their LOCALID_ name, their script's name (or a unique part of it), or "X,Y".

What it writes, in .theatre/routes/<route>/ (gitignored): each stop's frames, one contact sheet per stop
("NN - stop.png", every capture labelled with the words the box held), and report.md -- every stop passed or failed
and why, and every box's text. A stop that fails is reported and the run goes on to the next stop, which usually
starts with a goto. Exit status is the number of stops that failed.

WHY. The field test's route was walked by hand, by screenshot, once per release. A route file makes it replayable
after every release, and reading each box's text out of gStringVar4 (where every field message is expanded before it
prints) means a stop can check the words, not only show them.
"""
import json, os, re, shlex, shutil, subprocess, sys, textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theatre_walk as tw                                                 # noqa: E402

ROOT, GBA, THEATRE = tw.ROOT, tw.GBA, tw.THEATRE
OBJECT_EVENT, OBJECT_EVENTS = 0x24, 16
CONTEXT_SHUTDOWN = 2                                                      # src/script.c's sGlobalScriptContextStatus


# ---- names -------------------------------------------------------------------------------------------------------

def _defines(*headers):
    raw = {}
    for h in headers:
        for line in open(os.path.join(GBA, "include/constants", h)):
            m = re.match(r"#define\s+(\w+)\s+(.+?)\s*(//.*)?$", line)
            if m:
                raw[m.group(1)] = m.group(2)
    return raw


DEFINES = _defines("flags.h", "vars.h", "songs.h", "opponents.h")


def const(name):
    """A flag or var by name or number: FLAG_SCHOOL_HIDE_CLASS, 0x312, (FLAG_X + 1)."""
    seen = set()
    expr = name
    while True:
        words = [w for w in re.findall(r"[A-Za-z_]\w*", expr) if w in DEFINES and w not in seen]
        if not words:
            break
        for w in words:
            seen.add(w)
            expr = re.sub(r"\b%s\b" % w, "(%s)" % DEFINES[w], expr)
    try:
        return int(eval(expr, {"__builtins__": {}}))
    except Exception:
        raise RouteError("no flag or var called %s" % name)


def map_index(folder):
    groups = json.load(open(os.path.join(GBA, "data/maps/map_groups.json")))
    for g, gname in enumerate(groups["group_order"]):
        if folder in groups[gname]:
            return g, groups[gname].index(folder)
    raise RouteError("no map called %s (a folder in data/maps/)" % folder)


def map_folder(map_id):
    """MAP_VIRIDIAN_CITY_SCHOOL_2F -> ViridianCity_School_2F"""
    for folder in os.listdir(os.path.join(GBA, "data/maps")):
        f = os.path.join(GBA, "data/maps", folder, "map.json")
        if os.path.exists(f) and json.load(open(f)).get("id") == map_id:
            return folder
    raise RouteError("no map with the id %s" % map_id)


def map_json(folder):
    return json.load(open(os.path.join(GBA, "data/maps", folder, "map.json")))


def who(folder, spec):
    """(localId, (x, y) as placed) for a person on this map."""
    objs = map_json(folder).get("object_events") or []
    if re.fullmatch(r"\d+,\d+", spec):
        x, y = map(int, spec.split(","))
        hits = [i for i, o in enumerate(objs) if (o["x"], o["y"]) == (x, y)]
    else:
        hits = [i for i, o in enumerate(objs) if str(o.get("local_id")) == spec or o.get("script") == spec]
        if not hits:
            hits = [i for i, o in enumerate(objs) if spec.lower() in str(o.get("script", "")).lower()]
    if len(hits) != 1:
        raise RouteError("%s on %s: %s" % (spec, folder, "nobody" if not hits else "%d people match" % len(hits)))
    o = objs[hits[0]]
    lid = o.get("local_id")
    lid = int(lid) if str(lid).isdigit() else hits[0] + 1                 # a LOCALID_ name is its index + 1 (mapjson)
    return lid, (o["x"], o["y"])


# ---- the charmap, backwards --------------------------------------------------------------------------------------

def _charmap():
    out = {}
    for line in open(os.path.join(GBA, "charmap.txt"), encoding="utf-8"):
        m = re.match(r"'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m:
            out.setdefault(int(m.group(2), 16), m.group(1))
    return out


CHARS = _charmap()


# gen 3's {EXT_CTRL_CODE} arguments by code (src/text.c): COLOR, HIGHLIGHT, SHADOW 1; COLOR_HIGHLIGHT_SHADOW 3;
# PALETTE, FONT 1; PAUSE 1; PLAY_BGM 2; ESCAPE, SHIFT_RIGHT, SHIFT_DOWN 1; PLAY_SE 2; CLEAR, SKIP, CLEAR_TO,
# MIN_LETTER_SPACING 1 -- and none for the rest (RESET_FONT, PAUSE_UNTIL_PRESS, WAIT_SE, FILL_WINDOW, ...)
EXT_ARGS = {0x01: 1, 0x02: 1, 0x03: 1, 0x04: 3, 0x05: 1, 0x06: 1, 0x08: 1, 0x0B: 2, 0x0C: 1, 0x0D: 1, 0x0E: 1,
            0x10: 2, 0x11: 1, 0x12: 1, 0x13: 1, 0x14: 1}


def decode(raw):
    out, i = [], 0
    while i < len(raw):
        b = raw[i]
        if b == 0xFF:
            break
        if b == 0xFE:
            out.append("\n")
        elif b in (0xFA, 0xFB):
            out.append("\n\n" if b == 0xFB else "\n")
        elif b == 0xFC and i + 1 < len(raw):                              # a control code, then its arguments
            i += 1 + EXT_ARGS.get(raw[i + 1], 0)
        elif b == 0xFD:
            i += 1
        else:
            out.append(CHARS.get(b, "?"))
        i += 1
    return "".join(out)


def fold(s):
    return " ".join(s.replace("\n", " ").split()).upper()


# ---- the runner --------------------------------------------------------------------------------------------------

class RouteError(Exception):
    pass


def elf_symbol(name, release):
    """A static (sLockFieldControls, ...) is in the .elf's symbols, not the .map."""
    elf = os.path.join(GBA, "daemonsContent.elf" if release else "daemonsContent_debug.elf")
    out = subprocess.run(["arm-none-eabi-nm", elf], capture_output=True, text=True).stdout
    m = re.search(r"^([0-9a-f]{8}) \w %s$" % re.escape(name), out, re.M)
    if not m:
        raise RouteError("no symbol %s in %s" % (name, os.path.basename(elf)))
    return int(m.group(1), 16)


class Runner:
    def __init__(self, route_name, release):
        self.g = tw.Game(release)
        self.release = release
        self.lock = elf_symbol("sLockFieldControls", release)
        self.status = elf_symbol("sGlobalScriptContextStatus", release)
        self.var4 = tw.symbol("gStringVar4", release)
        self.objects = tw.symbol("gObjectEvents", release)
        self.out = os.path.join(THEATRE, "routes", route_name)
        os.makedirs(self.out, exist_ok=True)
        self.same_build()

    def same_build(self):
        """Every address comes from the build's .map, so the theatre must be running THAT build. A rebuild that only
        grew some text moved everything in ROM after it (the song table by 16 bytes on 2026-10-06) while RAM stayed
        put -- so the walk worked and every music check read the wrong song. Compare the song table in the
        emulator with the same bytes in the built ROM."""
        rom = os.path.join(GBA, "daemonsContent.gba" if self.release else "daemonsContent_debug.gba")
        at = tw.symbol("gSongTable", self.release)
        want = open(rom, "rb").read()[at - 0x08000000: at - 0x08000000 + 32]
        got = tw.peek([(32, at + 4 * k, "w%d" % k) for k in range(8)])
        if b"".join(got["w%d" % k].to_bytes(4, "little") for k in range(8)) != want:
            raise SystemExit("theatre_route: the theatre is not running the build in engineGba/ -- copy %s over "
                             ".theatre/rom/ and reload it in the theatre's window first" % os.path.basename(rom))

    # what the screen and the script are doing
    def free(self):
        s = tw.peek([(8, self.lock, "lock"), (8, self.status, "status")])
        return not s["lock"] and s["status"] == CONTEXT_SHUTDOWN

    def text(self):
        raw = b""
        for chunk in range(4):                                            # 128 bytes a read, until the 0xFF
            base = self.var4 + chunk * 128
            got = tw.peek([(32, base + 4 * k, "w%d" % k) for k in range(32)])
            raw += b"".join(got["w%d" % k].to_bytes(4, "little") for k in range(32))
            if 0xFF in raw:
                break
        return decode(raw)

    def capture(self, label, read_text=True):
        n = len(self.frames)
        name = "s%02d_%02d" % (self.stop_no, n)
        tw.run("shot %s" % name)
        src = os.path.join(THEATRE, name + ".png")
        dst = os.path.join(self.stop_dir, name + ".png")
        shutil.move(src, dst)
        words = self.text() if read_text else ""
        if read_text and words and (not self.said or self.said[-1] != words):
            self.said.append(words)
        self.frames.append((dst, label, words))

    def where(self):
        s = self.g.state()
        return tw.map_name(*s["map"]), (s["x"], s["y"])

    # the steps
    def goto(self, folder, x=None, y=None):
        if self.release:
            raise RouteError("goto is the DEBUG build's theatre warp; a release route walks")
        group, num = map_index(folder)
        if x is None:
            warps = map_json(folder).get("warp_events") or []
            if not warps:
                raise RouteError("%s has no warp to land on: give X Y" % folder)
            x, y = warps[0]["x"], warps[0]["y"]
        w = tw.symbol("gDaemonsDebugWarp", False)
        arm = ["poke8 %s %d" % (hex(w + 1), group), "poke8 %s %d" % (hex(w + 2), num),
               "poke16 %s %d" % (hex(w + 4), int(x)), "poke16 %s %d" % (hex(w + 6), int(y)), "poke8 %s 1" % hex(w)]
        tw.run(*arm, "wait 120")
        lost = 0
        for attempt in range(120):
            name, here = self.where()
            if name == folder:
                tw.run("wait 60")                                         # the fade in
                if not self.free():                                       # someone saw us land: play it out first
                    self.boxes()
                return
            st = tw.peek([(8, self.lock, "lock"), (8, w, "armed")])
            if st["armed"]:          # waiting for the field's controls (src/overworld.c, WarpIfTheTheatreAsks)
                tw.run("hold B 6", "wait 40")
            elif st["lock"]:         # taken, and on its way: the old map's music fades out first, slowly after a scene
                tw.run("wait 60")
            else:                    # taken, free, and still here: lost -- arm it again
                lost += 1
                tw.run(*arm, "wait 60")
                if lost > 3:
                    break
        st = tw.peek([(8, self.lock, "lock"), (8, w, "armed")])
        raise RouteError("the warp to %s did not land (still on %s; controls %s, warp %s)"
                         % (folder, name, "LOCKED" if st["lock"] else "free", "still armed" if st["armed"] else "taken"))

    def person(self, spec):
        folder, _ = self.where()
        lid, placed = who(folder, spec)
        group, num = map_index(folder)
        reads = []
        for k in range(OBJECT_EVENTS):
            a = self.objects + k * OBJECT_EVENT
            reads += [(8, a, "f%d" % k), (8, a + 8, "id%d" % k), (8, a + 9, "n%d" % k), (8, a + 10, "g%d" % k),
                      (16, a + 0x10, "x%d" % k), (16, a + 0x12, "y%d" % k)]
        s = tw.peek(reads)
        for k in range(OBJECT_EVENTS):
            if s["f%d" % k] & 1 and (s["id%d" % k], s["n%d" % k], s["g%d" % k]) == (lid, num, group):
                return (s["x%d" % k] - 7, s["y%d" % k] - 7)               # gObjectEvents carry MAP_OFFSET
        raise RouteError("%s is not on screen on %s (hidden by a flag?)" % (spec, folder))

    def walkto(self, spec):
        folder, _ = self.where()
        m = tw.Map(folder)
        for attempt in range(4):
            them = self.person(spec)
            _, here = self.where()
            sides = []
            for d, (dx, dy) in tw.DIRS.items():
                for reach in (1, 2):                                      # 2: across a counter
                    t = (them[0] - dx * reach, them[1] - dy * reach)
                    if reach == 2 and m.open(them[0] - dx, them[1] - dy, None):
                        continue
                    p = [] if t == here else m.path(here, t)
                    if p is not None and m.open(*t, None) or t == here:
                        sides.append((len(p), reach, d, t))
            if not sides:
                raise RouteError("no way to stand beside %s at %s" % (spec, them))
            _, reach, d, t = min(sides)
            if t != here:
                tw.walk(self.g, t)
            if self.person(spec) == them and self.where()[1] == t:
                tw.run("hold %s 4" % d, "wait 12")                         # under 8 frames: a turn, not a step
                return
        raise RouteError("%s kept moving away" % spec)

    def talk(self, spec, n=None):
        self.walkto(spec)
        tw.run("wait 30")
        if not self.free():                                               # a trainer saw us turn: theirs first
            self.boxes()
            self.walkto(spec)
        tw.run("hold A 6", "wait 50")
        self.boxes(n)

    def beside(self, x, y, need=None):
        """Walk to the open tile beside (x, y) nearest the player -- on the side `need` faces from, if given -- and
        answer the direction that faces (x, y) from it."""
        folder, here = self.where()
        m = tw.Map(folder)
        warps = {(w["x"], w["y"]) for w in m.json.get("warp_events") or []}
        sides = []
        for d, (dx, dy) in tw.DIRS.items():
            t = (x - dx, y - dy)
            if need and d != need or not m.open(*t, None) and t != here or t in warps:
                continue                                                  # a door beside a sign would take us away
            p = [] if t == here else m.path(here, t)
            if p is not None:
                sides.append((len(p), d, t))
        if not sides:
            raise RouteError("nowhere to stand beside (%d, %d) on %s" % (x, y, folder))
        _, d, t = min(sides)
        if t != here:
            tw.walk(self.g, t)
        if self.where()[1] != t:
            raise RouteError("meant to stand at %s beside (%d, %d), stood at %s" % (t, x, y, self.where()[1]))
        return d

    def look(self, x, y, n=None):
        facing = {(b["x"], b["y"]): b.get("player_facing_dir", "") for b in map_json(self.where()[0]).get("bg_events") or []}
        need = {"BG_EVENT_PLAYER_FACING_NORTH": "UP", "BG_EVENT_PLAYER_FACING_SOUTH": "DOWN",
                "BG_EVENT_PLAYER_FACING_EAST": "RIGHT", "BG_EVENT_PLAYER_FACING_WEST": "LEFT"}.get(facing.get((x, y)))
        d = self.beside(x, y, need)
        tw.run("hold %s 4" % d, "wait 12")                                 # under 8 frames: a turn, not a step
        tw.run("hold A 6", "wait 50")
        self.boxes(n)

    def trigger(self, x, y, n=None):
        """Step onto a scene's trigger tile from beside it, then capture the scene to its end."""
        d = self.beside(x, y)
        tw.run("hold %s 12" % d, "wait 40")
        self.boxes(n)

    def boxes(self, limit=None):
        """Capture each box and press A, until the script lets go (or `limit` boxes). A battle on the way is won
        (DEBUG) or fought (the walker's), and the scene carries on after it."""
        count, battles = 0, 0
        while count < (limit or 60):
            if self.g.state()["battle"]:
                battles += 1
                self.capture("a battle")
                self.win() if not self.release else tw.clear_battle(self.g)
                tw.run("wait 60")
                if battles > 6:
                    raise RouteError("six battles in one scene")
                continue
            if limit is None and self.free():
                return
            self.capture("A")
            tw.run("hold A 6", "wait 50")
            count += 1
        if limit is None and not self.free():
            raise RouteError("the script still held the player after sixty boxes")

    def press(self, button, times=1):
        for _ in range(times):
            tw.run("hold %s 6" % button, "wait 50")
            self.capture(button)

    def win(self):
        if self.release:
            raise RouteError("win pokes the battle's outcome: DEBUG routes only")
        outcome = tw.symbol("gBattleOutcome", False)
        for _ in range(30):
            if not self.g.state()["battle"]:
                return
            tw.run("poke8 %s 1" % hex(outcome), "hold A 8", "wait 60")
        raise RouteError("still in a battle after thirty turns")

    def var(self, v, value):
        tw.run("poke16 %s %d" % (hex(tw.peek([(32, self.g.sb1, "p")])["p"] + 0x1000 + (v - 0x4000) * 2), value))

    def step(self, line):
        a = words(line)
        op, args = a[0].lower(), a[1:]
        if op == "goto":
            self.goto(args[0], *(int(v) for v in args[1:3]))
        elif op == "to":
            tw.walk(self.g, (int(args[0]), int(args[1])))
        elif op == "warp":
            folder, here = self.where()
            m = tw.Map(folder)
            hits = [w for w in m.json.get("warp_events") or [] if w["dest_map"] == args[0]]
            if not hits:
                raise RouteError("%s has no warp to %s" % (folder, args[0]))
            tiles = {(w["x"], w["y"]) for w in hits}
            best = min(hits, key=lambda w: (m.path(here, (w["x"], w["y"])) is None,
                                            -sum((w["x"] + dx, w["y"]) in tiles for dx in (-1, 1)),
                                            len(m.path(here, (w["x"], w["y"])) or ())))
            tw.walk(self.g, (best["x"], best["y"]), into_warp=True)
        elif op == "edge":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools/theatre_walk.py"), "edge", args[0]]
                           + (["--release"] if self.release else []), check=True)
        elif op == "walkto":
            self.walkto(args[0])
        elif op == "talk":
            self.talk(args[0], int(args[1]) if len(args) > 1 else None)
        elif op == "trigger":
            self.trigger(int(args[0]), int(args[1]), int(args[2]) if len(args) > 2 else None)
        elif op == "look":
            self.look(int(args[0]), int(args[1]), int(args[2]) if len(args) > 2 else None)
        elif op == "read":
            self.capture("read")
        elif op == "press":
            self.press(args[0].upper(), int(args[1]) if len(args) > 1 else 1)
        elif op == "hold":
            tw.run("hold %s %d" % (args[0].upper(), int(args[1])), "wait 20")
        elif op == "wait":
            tw.run("wait %d" % int(args[0]))
        elif op == "shot":
            self.capture(" ".join(args) or "shot", read_text=False)
        elif op == "flag":
            want = int(args[1])
            if tw.flag(self.g, const(args[0]), want) != bool(want):
                raise RouteError("%s did not take" % args[0])
        elif op == "trainer":
            want = int(args[1])
            if tw.flag(self.g, const("TRAINER_FLAGS_START") + const(args[0]), want) != bool(want):
                raise RouteError("%s's flag did not take" % args[0])
        elif op == "flagis":
            if tw.flag(self.g, const(args[0])) != bool(int(args[1])):
                raise RouteError("%s is %s" % (args[0], "clear" if int(args[1]) else "set"))
        elif op == "var":
            self.var(const(args[0]), int(args[1], 0))
        elif op == "repel":
            self.var(const("VAR_REPEL_STEP_COUNT"), int(args[0]) if args else 250)
        elif op == "fight":
            tw.clear_battle(self.g)
        elif op == "win":
            self.win()
        elif op == "expect":
            folder, here = self.where()
            if folder != args[0] or (len(args) > 2 and here != (int(args[1]), int(args[2]))):
                raise RouteError("expected %s %s, stood on %s %s" % (args[0], " ".join(args[1:]), folder, here))
        elif op == "music":
            folder, _ = self.where()
            want = args[0] if args else map_json(folder).get("music")
            table, bgm = tw.symbol("gSongTable", self.release), tw.symbol("gMPlayInfo_BGM", self.release)
            for attempt in range(8):                                      # a warp's new song fades in: let it settle
                got = tw.peek([(32, table + 8 * const(want), "want"), (32, bgm, "playing")])
                if got["want"] == got["playing"]:
                    break
                tw.run("wait 60")
            else:
                songs = sum(1 for l in open(os.path.join(GBA, "sound/song_table.inc")) if l.strip().startswith("song "))
                heads = tw.peek([(32, table + 8 * n, "h%d" % n) for n in range(songs)])     # one batch, not one a song
                k = next((n for n in range(songs) if heads["h%d" % n] == got["playing"]), None)
                name = next((w for w, v in DEFINES.items() if w.startswith("MUS_") and v.split()[0].isdigit()
                             and int(v.split()[0]) == k), "no song in the table" if k is None else "song %d" % k)
                raise RouteError("%s should play %s; %s is playing" % (folder, want, name))
        elif op == "says":
            want = fold(" ".join(args))
            if not any(want in fold(s) for s in self.said):
                raise RouteError('no box said "%s"' % " ".join(args))
        else:
            raise RouteError("no step called %s" % op)

    def play(self, no, stop):
        self.stop_no, self.frames, self.said = no, [], []
        self.stop_dir = os.path.join(self.out, "%02d" % no)
        shutil.rmtree(self.stop_dir, ignore_errors=True)
        os.makedirs(self.stop_dir)
        failed = None
        for line in stop["steps"]:
            try:
                self.step(line)
            except (RouteError, SystemExit, subprocess.CalledProcessError) as e:
                failed = "%s -- %s" % (line, e)
                try:
                    self.capture("FAILED here")
                except Exception:
                    pass
                break
        sheet = os.path.join(self.out, "%02d - %s.png" % (no, re.sub(r"[^\w ,.'-]+", "", stop["stop"])[:60]))
        contact_sheet(sheet, stop["stop"], self.frames, failed)
        return failed, sheet, list(self.said)


def contact_sheet(path, title, frames, failed, cols=3):
    from PIL import Image, ImageDraw, ImageFont
    W, H, LAB = 480, 320, 84
    font, big = ImageFont.load_default(size=15), ImageFont.load_default(size=20)
    rows = max(1, (len(frames) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * W + (cols + 1) * 8, 44 + rows * (H + LAB + 8)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    d.text((8, 12), ("FAILED  " if failed else "") + title + (("  --  " + failed) if failed else ""),
           fill=(255, 120, 120) if failed else (230, 230, 230), font=big)
    for i, (png, label, words) in enumerate(frames):
        x, y = 8 + (i % cols) * (W + 8), 44 + (i // cols) * (H + LAB + 8)
        try:
            sheet.paste(Image.open(png).convert("RGB").resize((W, H), Image.NEAREST), (x, y))
        except OSError:
            continue
        d.text((x, y + H + 4), "%d. %s" % (i + 1, label), fill=(200, 200, 120), font=font)
        if i and words == frames[i - 1][2]:
            continue                                                      # the same message, read again
        flat = " / ".join(l.strip() for l in words.split("\n") if l.strip())
        for k, line in enumerate(textwrap.wrap(flat, 60)[:3]):            # the box's words, three lines at most
            d.text((x, y + H + 24 + k * 18), line, fill=(200, 200, 200), font=font)
    sheet.save(path)


def words(line):
    """A step's words: shell-split, except a shot's label and a says's text, which are the rest of the line as written."""
    op, _, rest = line.strip().partition(" ")
    if op.lower() in ("shot", "says"):
        return [op] + ([rest.strip().strip('"')] if rest.strip() else [])
    return shlex.split(line)


def load(path):
    route = json.load(open(path))
    for i, stop in enumerate(route["stops"], 1):
        if not stop.get("steps"):
            raise RouteError("stop %d (%s) has no steps" % (i, stop.get("stop")))
    return route


def check(route):
    """Resolve every name a route uses, without the theatre: the maps, the flags and vars, the people."""
    bad, folder = [], None
    for i, stop in enumerate(route["stops"], 1):
        for line in stop["steps"]:
            a = words(line)
            try:
                if a[0] in ("goto", "expect"):
                    map_index(a[1])
                    folder = a[1] if a[0] == "goto" else folder
                    if a[0] == "goto" and len(a) > 3 and not tw.Map(a[1]).open(int(a[2]), int(a[3]), None):
                        raise RouteError("goto %s %s %s lands in a wall" % tuple(a[1:4]))
                elif a[0] in ("flag", "flagis", "var", "trainer"):
                    const(a[1])
                elif a[0] in ("talk", "walkto") and folder:
                    who(folder, a[1])
                elif a[0] == "music" and (len(a) > 1 or folder):
                    const(a[1] if len(a) > 1 else map_json(folder)["music"])
                elif a[0] == "look" and folder:
                    lay = map_json(folder)
                    if not any((b["x"], b["y"]) == (int(a[1]), int(a[2])) for b in lay.get("bg_events") or []):
                        print("  (stop %d: nothing is placed at %s,%s on %s -- a metatile, like a PC?)"
                              % (i, a[1], a[2], folder))
                elif a[0] == "edge":
                    folder = None                                         # the next map is the connection's
                elif a[0] == "warp" and folder:
                    dests = [w["dest_map"] for w in map_json(folder).get("warp_events") or []]
                    if a[1] not in dests:
                        raise RouteError("%s has no warp to %s" % (folder, a[1]))
                    folder = map_folder(a[1])
            except RouteError as e:
                bad.append("stop %d: %s" % (i, e))
    return bad


def main():
    args = sys.argv[1:]
    only = set()
    start = 1
    if "--only" in args:
        k = args.index("--only")
        only = {int(v) for v in args[k + 1].split(",")}
        del args[k:k + 2]
    if "--from" in args:
        k = args.index("--from")
        start = int(args[k + 1])
        del args[k:k + 2]
    dry = "--check" in args
    args = [a for a in args if a != "--check"]
    if not args:
        sys.exit(__doc__)
    route = load(args[0])
    bad = check(route)
    if bad or dry:
        print("\n".join(bad) or "%s: every name resolves (%d stops)" % (args[0], len(route["stops"])))
        sys.exit(1 if bad else 0)
    name = os.path.splitext(os.path.basename(args[0]))[0]
    r = Runner(name, route.get("rom") == "release")
    report = ["# %s" % name, "", route.get("about", ""), ""]
    failures = 0
    for i, stop in enumerate(route["stops"], 1):
        if i < start or (only and i not in only):
            continue
        print("%2d. %s ..." % (i, stop["stop"]), end=" ", flush=True)
        failed, sheet, said = r.play(i, stop)
        failures += bool(failed)
        print("FAILED: %s" % failed if failed else "ok")
        report += ["## %d. %s -- %s" % (i, stop["stop"], "FAILED: " + failed if failed else "ok"), "",
                   "![](%s)" % os.path.basename(sheet), ""]
        report += ["> " + s.replace("\n", "  \n> ") + "\n" for s in said]
    open(os.path.join(r.out, "report.md"), "w").write("\n".join(report) + "\n")
    print("%d stops failed; report and sheets in %s" % (failures, os.path.relpath(r.out, ROOT)))
    sys.exit(failures)


if __name__ == "__main__":
    main()
