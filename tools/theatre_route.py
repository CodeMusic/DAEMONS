#!/usr/bin/env python3
"""Play a route through the theatre, stop by stop, and write what it saw (T-378, the 6 October work-day run).

    python3 tools/theatre_route.py tools/routes/field-test.json            # play every stop
    python3 tools/theatre_route.py tools/routes/field-test.json --from 4   # from the fourth stop on
    python3 tools/theatre_route.py tools/routes/field-test.json --only 2,5
    python3 tools/theatre_route.py --check tools/routes/field-test.json    # parse it and resolve every name; no theatre

A route is JSON: {"rom": "debug" | "release", "about": "...", "stops": [{"stop": "a name", "steps": [...]}]}, and each
step is one line, split like a shell line:

    goto MAP_FOLDER [X Y]      the DEBUG build's theatre warp (gDaemonsDebugWarp): to (X, Y), or the map's first warp;
                               on a RELEASE route, fly
    fly MAP_FOLDER [X Y]       GOTO there as a player does (START, DAEMON, a daemon, GOTO, the region map's cursor read
                               out of RAM and steered to the town), then walk to (X, Y) -- the town's own map only (T-384)
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
    finish                     play out whatever script is running, capturing each box (a scene a battle broke into)
    press BUTTON [N]           press it N times (default 1), forty frames apart, capturing after each
    hold BUTTON FRAMES         hold it for exact frames, capturing nothing
    wait FRAMES
    shot LABEL                 a screenshot into this stop's sheet
    load debug|release         put the built ROM in the theatre (.theatre/rom/theatre_<kind>.gba, its save kept beside
                               it) and continue the game -- no click in the theatre's window (T-386)
    continue                   from the intro, title, menu or recap to the player free on the overworld
    save                       save the game in the game (START, SAVE, YES): another ROM can continue from it
    savestate NAME             keep this moment in .theatre/states/NAME.ss (the theatre script's own, T-386)
    loadstate NAME             come back to it: a route can start there instead of playing up to it
    flag FLAG_NAME|0xNNN 0|1   set a flag on the scratch save (to replay a scene, or reach past one)
    trainer TRAINER_NAME 0|1   set a trainer's beaten flag (0: they battle again -- a leader gives the MARK again)
    flagis FLAG_NAME|0xNNN 0|1 fail the stop unless the flag is clear (0) or set (1) -- a document that files itself
    var VAR_NAME|0x40NN N      set a var
    repel [STEPS]              no wild battles for STEPS steps (default 250)
    fight                      clear a battle: run from a wild one, fight a trainer (the walker's)
    win                        DEBUG: win the battle on screen (gBattleOutcome = 1, then a turn)
    bump WHO [keep]            walk beside someone and then INTO them, pressing no A: fail unless that starts their
                               script (T-334: an unseen legend is met by walking into its place); the scene is then
                               captured to its end, its battle won on a DEBUG route -- with keep, left at the battle's
                               first "What will X do?" for the steps that follow (press L, win, finish)
    wild [past151|SPECIES_X] [N] [keep]   walk back and forth in the grass (or water) here until a wild battle
                               starts, capture its opening, and win it (DEBUG); with past151 or a species, keep going (up
                               to N battles, default 12) until the daemon met is one past the first 151 (or that one), and
                               fail if none is; keep leaves the last battle open at its first menu
    foe SPECIES_X              fail unless the battle on screen is against SPECIES_X (read from gBattleMons)
    unsaid "TEXT"              fail the stop if a box captured in it said TEXT (a gift given once is not given twice)
    friendship SLOT N          set party daemon SLOT's (0-5) friendship to N: gPlayerParty decrypted, the byte set, the
                               checksum made again and encrypted back, as the game would have written it (T-424)
    mon SLOT away|egg|hp|shiny|species VALUE   T-18 P3: the same for the rest of a party daemon -- AWAY (T-358's bit,
                               0|1), an egg (0|1), its hit points (0 HALTS it, max heals it), shiny (0|1: its OT ID set so it is, or
                               the player's own back, every secure word re-keyed), its species (SPECIES_X, a number, or back:
                               an evolution or a trade, as the follower sees one)
    coins N                    set the TOKEN CASE's count (stored XOR the save's key, src/coins.c)
    keyitem ITEM_X             put a key item in the bag if it is not there (its count stored XOR the save's key), so
                               `register` and `press SELECT` can use it -- the BICYCLE for T-18's follower
    follower shown [DX DY]|hidden|absent   T-18: fail unless the follower is drawn (and, given DX DY, stands that many
                               tiles from the player), drawn nowhere (its sprite hidden or gone), or gone (no sprite);
                               the capture's caption says where it stands
    follower grass|nograss|reflection|noreflection   T-18 P3: fail unless tall grass is drawn over its feet (or not),
                               or its reflection in the water below it (or not)
    follower talk              T-18 P2: turn to the follower (it must stand a tile away), press A, capture each box
                               until the script lets go -- `says` then checks its words
    objectat WHO X Y|back      T-18 P3: put a person's coordinates on (X, Y) -- their sprite stays -- or back
    remember NAME SPEC 8|16|32 note a RAM value (SPEC as poke's) ...
    moved NAME                 ... and fail unless it has changed since (the GAME CORNER's take after a pull, T-427)
    poke SYMBOL[+OFF] 8|16|32 VALUE   write RAM: SYMBOL from the build's .map (a static from the .elf); *SYMBOL+OFF
                               follows the pointer first (*gSaveBlock1Ptr+0x296) -- the DEBUG overrides (the date,
                               the weather, the watch) are EWRAM globals, set this way instead of through the menu
    register ITEM_X            register a key item for SELECT (gSaveBlock1Ptr->registeredItem), so `press SELECT` uses it
    play NOTES                 on the instrument: press each note's button, 1-7 (DOWN LEFT UP RIGHT B A SELECT), a
                               note a token; a token may end in + or - (hold R or L for the octave above or below)
    expect MAP_FOLDER [X Y]    fail the stop unless the player is there
    music [MUS_NAME]           fail the stop unless that song is playing (default: the one the map's map.json names)
    says "TEXT"                fail the stop unless a box captured in it said TEXT (spaces and line breaks folded)
    burst LABEL COUNT EVERY [BUTTON [FRAMES]]   T-430: hold BUTTON (6 frames by default), then COUNT captures, one
                               every EVERY frames, in one batch -- a routine in flight, a flicker
    palette BG|OBJ SLOT grey|colour   T-430: fail unless that palette slot on screen (palette RAM) is all grey, or holds
                               some colour (entry 0, the transparent one, is not counted)

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


def _numbers(header):
    out = {}
    for line in open(os.path.join(GBA, "include/constants", header)):
        m = re.match(r"#define\s+(\w+)\s+(\d+|0x[0-9A-Fa-f]+)\b", line)
        if m:
            out[m.group(1)] = int(m.group(2), 0)
    return out


def const_species(name):
    n = _numbers("species.h").get(name)
    if n is None:
        raise RouteError("no species called %s" % name)
    return n


def const_item(name):
    n = _numbers("items.h").get(name)
    if n is None:
        raise RouteError("no item called %s" % name)
    return n


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
    #  T-395: two objects on ONE tile are one place to stand (the fir before its key and after it, only one shown)
    if len(hits) > 1 and len({(objs[i]["x"], objs[i]["y"]) for i in hits}) == 1:
        hits = hits[:1]
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
    """Spaces and line breaks folded, case ignored, and the game's curly quotes read as straight ones (it prints
    "we’ll" where a route file says "we'll")."""
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
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


# ---- T-384: GOTO the game's own way, for a route on the RELEASE ROM ---------------------------------------------------
# The DEBUG build warps by poking gDaemonsDebugWarp; the ROM players get has no such thing, but every daemon offers GOTO
# (FLY) while the GOTO DRIVER is in the bag (T-199). So `fly` plays it as a player would: START, DAEMON, a daemon, GOTO,
# and then the region map, whose cursor is steered by reading it out of RAM (sMapCursor) until the town is under it.
STARTMENU_POKEMON, STARTMENU_SAVE = 1, 4                                     # src/start_menu.c's enum: DAEMON's, SAVE's


def mapsec_id(name):
    """MAPSEC_X -> its number, counted down the enum in the generated header as the compiler counts it."""
    n, out = 0, {}
    for m in re.finditer(r"^\s+(MAPSEC_\w+)\s*(?:=\s*([\w+ ]+))?,", open(os.path.join(GBA, "include/constants/region_map_sections.h")).read(), re.M):
        if m.group(2):
            v = m.group(2).strip()
            n = int(v, 0) if re.fullmatch(r"\d+|0x[0-9a-fA-F]+", v) else out.get(v, n)
        out[m.group(1)] = n
        n += 1
    if name not in out:
        raise RouteError("no %s in region_map_sections.h" % name)
    return out[name]


def fly_action():
    """GOTO's place among the party menu's actions: CURSOR_OPTION_FIELD_MOVES + FIELD_MOVE_FLY, read from the source."""
    enum = open(os.path.join(GBA, "src/data/party_menu.h")).read()
    opts = re.findall(r"^\s+(CURSOR_OPTION_\w+),", enum[enum.index("CURSOR_OPTION_SUMMARY,") - 20:], re.M)
    fly = int(re.search(r"#define FIELD_MOVE_FLY\s+(\d+)", open(os.path.join(GBA, "include/constants/party_menu.h")).read()).group(1))
    return opts.index("CURSOR_OPTION_FIELD_MOVES") + fly


def kanto_cells(sec, release):
    """Where a map section sits on Kanto's region map: the cells of sRegionMapSections_Kanto's map layer (22 x 15)."""
    at = elf_symbol("sRegionMapSections_Kanto", release) - 0x08000000
    rom = open(os.path.join(GBA, "daemonsContent.gba" if release else "daemonsContent_debug.gba"), "rb").read()
    layer = rom[at: at + 22 * 15]
    return [(i % 22, i // 22) for i, b in enumerate(layer) if b == sec]


class Runner:
    def __init__(self, route_name, release, check_build=True):
        self.g = tw.Game(release)
        self.release = release
        self.lock = elf_symbol("sLockFieldControls", release)
        self.status = elf_symbol("sGlobalScriptContextStatus", release)
        self.var4 = tw.symbol("gStringVar4", release)
        self.objects = tw.symbol("gObjectEvents", release)
        self.out = os.path.join(THEATRE, "routes", route_name)
        os.makedirs(self.out, exist_ok=True)
        if check_build:                   # a route that starts by loading its own ROM is checked after the load
            self.same_build()
        if not release:              # a debug route wins any battle the walker meets on the way, as `win` does
            tw.clear_battle = lambda g: self.win()

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

    def burst(self, label, count, every, hold):
        """T-430: COUNT frames, one every EVERY, in one batch (so the frames are exact), after holding a button."""
        name = "s%02d_%02d_b" % (self.stop_no, len(self.frames))
        cmds = ["hold %s %d" % (hold[0].upper(), int(hold[1]) if len(hold) > 1 else 6)] if hold else []
        tw.run(*cmds, "burst %s %d %d" % (name, count, every))
        for k in range(count):
            src = os.path.join(THEATRE, "%s_%02d.png" % (name, k))
            dst = os.path.join(self.stop_dir, "%s_%02d.png" % (name, k))
            if os.path.exists(src):
                shutil.move(src, dst)
                self.frames.append((dst, "%s +%d" % (label, k * every), ""))

    def palette(self, kind, slot, want):
        """T-430: fail unless palette RAM's BG or OBJ SLOT is all grey (r = g = b) or holds some colour."""
        base = 0x05000000 + (0x200 if kind == "OBJ" else 0) + 32 * slot
        got = tw.peek([(16, base + 2 * k, "c%d" % k) for k in range(1, 16)])
        cols = [got["c%d" % k] for k in range(1, 16)]
        grey = all((c & 31) == ((c >> 5) & 31) == ((c >> 10) & 31) for c in cols)
        if want == "grey" and not grey:
            raise RouteError("%s palette %d holds colour: %s" % (kind, slot, " ".join("%04x" % c for c in cols)))
        if want == "colour" and grey:
            raise RouteError("%s palette %d is all grey" % (kind, slot))

    def where(self):
        #  gSaveBlock1Ptr moves when a map loads; a pointer kept from before a warp reads the old map's location for as
        #  long as that memory is left alone, so a warp that landed looked lost (T-417 P5, MANSION B1F -> PALLET).
        self.g.p = None
        s = self.g.state()
        return tw.map_name(*s["map"]), (s["x"], s["y"])

    # the steps
    def goto(self, folder, x=None, y=None):
        if self.release:                                                  # T-384: the ROM players get goes by GOTO
            return self.fly(folder, x, y)
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
        #  T-395: everyone placed on the same tile is the same place to stand -- whichever is shown is the one meant
        lids = {lid} | {(int(o["local_id"]) if str(o.get("local_id")).isdigit() else i + 1)
                         for i, o in enumerate(map_json(folder).get("object_events") or []) if (o["x"], o["y"]) == placed}
        group, num = map_index(folder)
        reads = []
        for k in range(OBJECT_EVENTS):
            a = self.objects + k * OBJECT_EVENT
            reads += [(8, a, "f%d" % k), (8, a + 8, "id%d" % k), (8, a + 9, "n%d" % k), (8, a + 10, "g%d" % k),
                      (16, a + 0x10, "x%d" % k), (16, a + 0x12, "y%d" % k)]
        s = tw.peek(reads)
        for k in range(OBJECT_EVENTS):
            if s["f%d" % k] & 1 and s["id%d" % k] in lids and (s["n%d" % k], s["g%d" % k]) == (num, group):
                return (s["x%d" % k] - 7, s["y%d" % k] - 7)               # gObjectEvents carry MAP_OFFSET
        raise RouteError("%s is not on screen on %s (hidden by a flag?)" % (spec, folder))

    def walkto(self, spec, reaches=(1, 2)):
        folder, _ = self.where()
        m = tw.Map(folder)
        try:
            self.person(spec)
        except RouteError:                      # off screen: objects spawn only near the camera, so walk toward them
            _, placed = who(folder, spec)
            near = sorted(((abs(x - placed[0]) + abs(y - placed[1]), (x, y)) for x in range(placed[0] - 4, placed[0] + 5)
                           for y in range(placed[1] - 4, placed[1] + 5) if m.open(x, y, None)), key=lambda t: t[0])
            for _, t in near:
                if m.path(self.where()[1], t) is not None:
                    tw.walk(self.g, t)
                    break
        for attempt in range(4):
            them = self.person(spec)
            _, here = self.where()
            sides = []
            for d, (dx, dy) in tw.DIRS.items():
                for reach in reaches:                                     # 2: across a counter
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
                return d
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

    def bump(self, spec, keep=False):
        """T-334: walk into someone without pressing A, and play out what that starts."""
        d = self.walkto(spec, reaches=(1,))                               # beside them: nothing between
        tw.run("hold %s 16" % d, "wait 16")
        if self.free() and not self.g.state()["battle"]:
            raise RouteError("walking into %s started nothing" % spec)
        self.capture("walked in", read_text=False)
        if keep:
            self.to_battle_menu()
        else:
            self.boxes()

    def to_battle_menu(self):
        """Wait for a battle, then for its first "What will X do?" (the cry, the intro, the send-out)."""
        for _ in range(40):
            if self.g.state()["battle"]:
                break
            tw.run("wait 30")
        else:
            raise RouteError("no battle began")
        self.at_action_menu()
        self.capture("the battle", read_text=False)

    def at_action_menu(self):
        """Advance a battle's opening boxes with B (it chooses nothing) until the player's "What will X do?" -- the
        player controller's HandleInputChooseAction (several controllers have a static of that name: any of them)."""
        elf = os.path.join(GBA, "daemonsContent.elf" if self.release else "daemonsContent_debug.elf")
        out = subprocess.run(["arm-none-eabi-nm", elf], capture_output=True, text=True).stdout
        menus = {int(a, 16) for a in re.findall(r"^([0-9a-f]{8}) t HandleInputChooseAction$", out, re.M)}
        funcs = tw.symbol("gBattlerControllerFuncs", self.release)
        for _ in range(40):
            if tw.peek([(32, funcs, "f")])["f"] & ~1 in menus:
                tw.run("wait 20")
                return
            tw.run("hold B 6", "wait 40")
        raise RouteError("the battle never reached its first menu")

    def addr(self, spec):
        deref = spec.startswith("*")
        name, _, off = spec.lstrip("*").partition("+")
        try:
            at = tw.symbol(name, self.release)
        except (Exception, SystemExit):                                  # theatre_walk exits on a miss
            at = elf_symbol(name, self.release)
        if deref:
            at = tw.peek([(32, at, "p")])["p"]
        return at + (int(off, 0) if off else 0)

    def read(self, spec, bits):
        v = tw.peek([(bits, self.addr(spec), "v")])["v"]
        return v - (1 << bits) if bits == 32 and v >> 31 else v

    ORDERS = ["GAEM", "GAME", "GEAM", "GEMA", "GMAE", "GMEA", "AGEM", "AGME", "AEGM", "AEMG", "AMGE", "AMEG",
              "EGAM", "EGMA", "EAGM", "EAMG", "EMGA", "EMAG", "MGAE", "MGEA", "MAGE", "MAEG", "MEGA", "MEAG"]

    def friendship(self, slot, value):
        base = tw.symbol("gPlayerParty", self.release) + 100 * slot
        w = tw.peek([(32, base + 4 * k, "w%d" % k) for k in range(20)])
        words_ = [w["w%d" % k] for k in range(20)]
        pid, otid = words_[0], words_[1]
        key = pid ^ otid
        secure = [words_[8 + k] ^ key for k in range(12)]                 # 48 bytes from offset 32
        g = self.ORDERS[pid % 24].index("G")
        word = 3 * g + 2                                                  # growth: species, item, exp, ppBonuses, FRIENDSHIP
        secure[word] = (secure[word] & ~0xFF00) | (value << 8)
        halves = [h for x in secure for h in (x & 0xFFFF, x >> 16)]
        checksum = sum(halves) & 0xFFFF
        cmds = ["poke16 %s %d" % (hex(base + 28), checksum)]
        for k in (word,):
            enc = secure[k] ^ key
            cmds += ["poke16 %s %d" % (hex(base + 32 + 4 * k), enc & 0xFFFF),
                     "poke16 %s %d" % (hex(base + 32 + 4 * k + 2), enc >> 16)]
        #  T-18: the theatre writes one value a frame, so for two frames the daemon's checksum disagrees with it -- and
        #  GetMonData makes a daemon read in that frame a BAD EGG for good. The follower reads the party every few
        #  frames (sFollower's retry +35 and check +36 count down to it), so hold both off while the pokes land.
        try:
            hold = elf_symbol("sFollower", self.release)
            cmds = ["poke8 %s 255" % hex(hold + 35), "poke8 %s 255" % hex(hold + 36)] + cmds + \
                   ["poke8 %s 0" % hex(hold + 35), "poke8 %s 1" % hex(hold + 36)]
        except RouteError:
            pass                                                          # a build from before the follower
        tw.run(*cmds)

    def mon(self, slot, field, value):
        """T-18 P3: a party daemon's AWAY bit, egg bit, HP, shininess or species, written as the game would."""
        base = tw.symbol("gPlayerParty", self.release) + 100 * slot
        w = tw.peek([(32, base + 4 * k, "w%d" % k) for k in range(20)] + [(16, base + 86, "hp")])
        words_ = [w["w%d" % k] for k in range(20)]
        pid, otid = words_[0], words_[1]
        key = pid ^ otid
        secure = [words_[8 + k] ^ key for k in range(12)]
        order = self.ORDERS[pid % 24]
        flags = (words_[4] >> 24) & 0xFF                                  # byte 19: isBadEgg, hasSpecies, isEgg, ..., away
        cmds, new_otid = [], otid
        if field == "hp":                                                 # -1 ("max"): its max HP, healed
            if value < 0:
                value = tw.peek([(16, base + 88, "m")])["m"]
            tw.run("poke16 %s %d" % (hex(base + 86), value))
            return
        if field == "away":
            flags = (flags | 0x10) if value else (flags & ~0x10)
            tw.run("poke8 %s %d" % (hex(base + 19), flags))
            return
        if field == "egg":
            word = 3 * order.index("M") + 1                               # misc: ivs, isEgg (bit 30), abilityNum
            secure[word] = (secure[word] | (1 << 30)) if value else (secure[word] & ~(1 << 30))
            flags = (flags | 0x04) if value else (flags & ~0x04)
            cmds.append("poke8 %s %d" % (hex(base + 19), flags))
        elif field == "species":                                          # -2 ("back"): the one it had first
            word = 3 * order.index("G")
            first = self.__dict__.setdefault("first_species", {}).setdefault(slot, secure[word] & 0xFFFF)
            secure[word] = (secure[word] & ~0xFFFF) | (first if value == -2 else value)
        elif field == "shiny":
            at = self.addr("*gSaveBlock2Ptr+0xA")                          # playerTrainerId, 2-aligned
            t = tw.peek([(16, at, "lo"), (16, at + 2, "hi")])
            tid = t["lo"] | (t["hi"] << 16)
            if value:
                new_otid = (tid & 0xFFFF) | (((tid & 0xFFFF) ^ (pid >> 16) ^ (pid & 0xFFFF)) << 16)
            else:
                new_otid = tid
                if ((tid >> 16) ^ (tid & 0xFFFF) ^ (pid >> 16) ^ (pid & 0xFFFF)) & 0xFFFF < 8:
                    new_otid ^= 0x80000
        else:
            raise RouteError("mon: no field %s (away, egg, hp, shiny, species)" % field)
        halves = [h for x in secure for h in (x & 0xFFFF, x >> 16)]
        cmds.append("poke16 %s %d" % (hex(base + 28), sum(halves) & 0xFFFF))
        if new_otid != otid:
            cmds += ["poke16 %s %d" % (hex(base + 4), new_otid & 0xFFFF), "poke16 %s %d" % (hex(base + 6), new_otid >> 16)]
        key = pid ^ new_otid
        for k in range(12):
            enc = secure[k] ^ key
            if enc != words_[8 + k]:
                cmds += ["poke16 %s %d" % (hex(base + 32 + 4 * k), enc & 0xFFFF),
                         "poke16 %s %d" % (hex(base + 32 + 4 * k + 2), enc >> 16)]
        try:                                                              # the follower held off, as for friendship
            hold = elf_symbol("sFollower", self.release)
            cmds = ["poke8 %s 255" % hex(hold + 35), "poke8 %s 255" % hex(hold + 36)] + cmds + \
                   ["poke8 %s 0" % hex(hold + 35), "poke8 %s 1" % hex(hold + 36)]
        except RouteError:
            pass
        tw.run(*cmds)

    def objectat(self, spec, args):
        """T-18 P3: put a person's coordinates (current and previous) on a tile, or back where they were: the follower is
        not an object, so the one thing it does about somebody is notice them in its tile."""
        folder, _ = self.where()
        lid, placed = who(folder, spec)
        for i in range(OBJECT_EVENTS):
            at = self.objects + OBJECT_EVENT * i
            v = tw.peek([(8, at, "fl"), (8, at + 8, "lid"), (16, at + 0x10, "x"), (16, at + 0x12, "y")])
            if v["fl"] & 1 and v["lid"] == lid:
                break
        else:
            raise RouteError("%s is not on screen" % spec)
        keep = self.__dict__.setdefault("object_was", {})
        if args[0] == "back":
            x, y = keep.pop(lid)
        else:
            keep.setdefault(lid, (v["x"], v["y"]))
            x, y = int(args[0]) + 7, int(args[1]) + 7                     # map coordinates: MAP_OFFSET
        tw.run("poke16 %s %d" % (hex(at + 0x10), x), "poke16 %s %d" % (hex(at + 0x12), y),
               "poke16 %s %d" % (hex(at + 0x14), x), "poke16 %s %d" % (hex(at + 0x16), y))

    def foe(self):
        return tw.peek([(16, tw.symbol("gBattleMons", self.release) + 0x58, "sp")])["sp"]

    def wild(self, past151, limit, keep=False):
        """Pace two tiles of this map until a wild battle starts; past151: until the daemon met is past the first 151."""
        folder, here = self.where()
        m = tw.Map(folder)
        other = next((t for t in ((here[0] + 1, here[1]), (here[0] - 1, here[1]), (here[0], here[1] + 1),
                                  (here[0], here[1] - 1)) if m.open(*t, None)), None)
        if other is None:
            raise RouteError("nowhere to pace beside %s on %s" % (here, folder))
        self.var(const("VAR_REPEL_STEP_COUNT"), 0)
        pair = (here, other)
        met = []
        for battles in range(limit):
            for steps in range(200):
                if self.g.state()["battle"]:
                    break
                if not self.free():                     # a battle's transition, or an insight: which?
                    tw.run("wait 90")
                    if self.g.state()["battle"]:
                        break
                    if not self.free():                 # an insight, a note: read it and go on
                        self.boxes(1)
                    continue
                now = self.where()[1]
                if now not in pair:                     # a battle or a box moved us: back to the two tiles
                    tw.walk(self.g, pair[0])
                    continue
                to = pair[1] if now == pair[0] else pair[0]
                d = next(k for k, v in tw.DIRS.items() if (now[0] + v[0], now[1] + v[1]) == to)
                tw.run("hold %s 12" % d, "wait 8")
            else:
                raise RouteError("two hundred steps on %s and no wild battle" % folder)
            tw.run("wait 200")                                              # the transition, and the daemon's entry
            sp = self.foe()
            met.append(sp)
            done = not past151 or (sp > 151 if past151 == "past151" else sp == past151)
            if done and keep:
                self.at_action_menu()
                self.capture("wild battle (species %d)" % sp, read_text=False)
                return
            self.capture("wild battle (species %d)" % sp, read_text=False)
            self.win()
            tw.run("wait 60")
            if not self.free():
                self.boxes()
            if done:
                return
        raise RouteError("%d wild battles and none was %s (%s)" % (limit, past151, met))

    def keyitem(self, item):
        """The KEY ITEMS pocket is thirty {itemId, count ^ key} slots at SaveBlock1 0x3B8 (include/global.h)."""
        key = tw.peek([(16, self.addr("*gSaveBlock2Ptr+0xF20"), "k")])["k"]
        for i in range(30):
            at = "*gSaveBlock1Ptr+0x%X" % (0x3B8 + 4 * i)
            have = self.read(at, 16)
            if have == item:
                return
            if have == 0:
                self.poke(at, 16, item)
                self.poke("*gSaveBlock1Ptr+0x%X" % (0x3B8 + 4 * i + 2), 16, 1 ^ key)
                return
        raise RouteError("the KEY ITEMS pocket is full")

    SPRITE, MAX_SPRITES = 0x44, 64

    def follower_state(self):
        """T-18: sFollower (src/daemons_follower.c) holds its sprite's id at +33; the player's is gPlayerAvatar +4.
        Answers (shown|hidden|absent, dx, dy): where it is drawn, in pixels from the player (None when absent)."""
        base = elf_symbol("sFollower", self.release)
        sprites = tw.symbol("gSprites", self.release)
        v = tw.peek([(8, base + 33, "id"), (8, tw.symbol("gPlayerAvatar", self.release) + 4, "pid")])
        fid, pid = v["id"], v["pid"]
        if fid < self.MAX_SPRITES:
            f = sprites + self.SPRITE * fid
            p = sprites + self.SPRITE * pid
            w = tw.peek([(32, f + 0x1C, "cb"), (16, f + 0x3E, "fl"), (16, f + 0x20, "fx"), (16, f + 0x22, "fy"),
                         (16, p + 0x20, "px"), (16, p + 0x22, "py")])
            if w["fl"] & 1 and (w["cb"] & ~1) == elf_symbol("SpriteCB_Follower", self.release):   # a Thumb pointer is odd
                sx = lambda n: n - 0x10000 if n & 0x8000 else n
                dx, dy = sx(w["fx"]) - sx(w["px"]), sx(w["fy"]) - sx(w["py"]) - 2   # FOLLOWER_Y
                return ("hidden" if w["fl"] & 4 else "shown"), dx, dy
        return "absent", None, None

    def follower(self, args):
        state, dx, dy = self.follower_state()
        where = "" if dx is None else " at %+d,%+d px from the player" % (dx, dy)
        self.capture("follower %s%s" % (state, where), read_text=False)
        want = args[0]
        if want == "talk":
            return self.follower_talk(state, dx, dy)
        if want in ("grass", "nograss", "reflection", "noreflection"):     # T-18 P3: what it stands on
            cb = elf_symbol("SpriteCB_FollowerGrass" if "grass" in want else "SpriteCB_FollowerReflection", self.release)
            sprites = tw.symbol("gSprites", self.release)
            v = tw.peek([(32, sprites + self.SPRITE * i + 0x1C, "cb%d" % i) for i in range(self.MAX_SPRITES)] +
                        [(16, sprites + self.SPRITE * i + 0x3E, "fl%d" % i) for i in range(self.MAX_SPRITES)])
            drawn = any(v["fl%d" % i] & 1 and not v["fl%d" % i] & 4 and (v["cb%d" % i] & ~1) == cb
                        for i in range(self.MAX_SPRITES))
            if drawn != (not want.startswith("no")):
                raise RouteError("its %s is %sdrawn" % (want.replace("no", ""), "" if drawn else "not "))
            return
        if want == "hidden" and state == "shown" or want in ("shown", "absent") and state != want:
            raise RouteError("the follower is %s%s, not %s" % (state, where, want))
        if want == "shown" and len(args) >= 3:
            if where != " at %+d,%+d px from the player" % (16 * int(args[1]), 16 * int(args[2])):
                raise RouteError("the follower is%s, not %s,%s tiles" % (where, args[1], args[2]))

    FACING = {"DOWN": 1, "UP": 2, "LEFT": 3, "RIGHT": 4}                  # DIR_SOUTH..DIR_EAST

    def follower_talk(self, state, dx, dy):
        """T-18 P2: face the follower where it stands (a tap under 8 frames turns the player; none if already facing
        it, or the tap would walk into it and swap the two), press A, and capture each box until the script lets go."""
        d = {(-16, 0): "LEFT", (16, 0): "RIGHT", (0, -16): "UP", (0, 16): "DOWN"}.get((dx, dy))
        if state != "shown" or d is None:
            raise RouteError("the follower is %s, not a tile from the player to talk to" % state)
        obj = tw.peek([(8, tw.symbol("gPlayerAvatar", self.release) + 5, "o")])["o"]
        facing = tw.peek([(8, self.objects + OBJECT_EVENT * obj + 0x18, "f")])["f"] & 0xF
        if facing != self.FACING[d]:
            tw.run("hold %s 4" % d, "wait 12")
        tw.run("hold A 6", "wait 18")
        self.capture("the bubble", read_text=False)                       # it lasts a second; the box outlasts it
        tw.run("wait 24")
        self.boxes()

    def poke(self, spec, bits, value):
        at = self.addr(spec)
        if bits == 32:                                                    # the theatre writes 8 and 16 bits
            tw.run("poke16 %s %d" % (hex(at), value & 0xFFFF), "poke16 %s %d" % (hex(at + 2), value >> 16))
        else:
            tw.run("poke%d %s %d" % (bits, hex(at), value))

    NOTE_BUTTONS = {"1": "DOWN", "2": "LEFT", "3": "UP", "4": "RIGHT", "5": "B", "6": "A", "7": "SELECT"}

    def note(self, token):
        """One note on the instrument (src/play.c): its button, with R or L held for the octave above or below."""
        button = self.NOTE_BUTTONS.get(token[0])
        if not button:
            raise RouteError("no note %s (1-7, then + or -)" % token)
        octave = {"+": "R", "-": "L"}.get(token[1:2])
        if octave:
            tw.run("press %s" % octave, "wait 2", "hold %s 6" % button, "wait 4", "release %s" % octave, "wait 22")
        else:
            tw.run("hold %s 6" % button, "wait 26")

    def win(self):
        if self.release:
            raise RouteError("win pokes the battle's outcome: DEBUG routes only")
        outcome = tw.symbol("gBattleOutcome", False)
        for _ in range(30):
            if not self.g.state()["battle"]:
                return
            # the outcome is read at the end of a TURN: so take one -- ROUTINES (top left), then the first routine.
            # A on DETACH takes none ("You cannot DETACH from a USER engagement!"), and that loop never ends.
            tw.run("poke8 %s 1" % hex(outcome), "hold B 8", "wait 30", "hold UP 6", "wait 10", "hold LEFT 6", "wait 10",
                   "hold A 8", "wait 40", "hold A 8", "wait 150", "hold A 6", "wait 60")
        raise RouteError("still in a battle after thirty turns")

    def var(self, v, value):
        tw.run("poke16 %s %d" % (hex(tw.peek([(32, self.g.sb1, "p")])["p"] + 0x1000 + (v - 0x4000) * 2), value))

    def start_menu(self, entry):
        """Open START and put its cursor on ENTRY (the menu remembers its cursor, so read where it is)."""
        S = lambda n: elf_symbol(n, self.release)
        cur, num, order = S("sStartMenuCursorPos"), S("sNumStartMenuItems"), S("sStartMenuOrder")
        tw.run("hold START 6", "wait 40")
        for tries in range(6):                                            # the release menu takes longer to build
            st = tw.peek([(8, cur, "cur"), (8, num, "num")] + [(8, order + i, "o%d" % i) for i in range(12)])
            items = [st["o%d" % i] for i in range(st["num"])]
            if entry in items:
                break
            tw.run("wait 20")
        if entry not in items:
            tw.run("hold B 6", "wait 30")
            raise RouteError("the START menu has no entry %d here" % entry)
        # T-332's two columns: down the left, then the right; up and down within a column, left and right across
        rows = (len(items) + 1) // 2                                       # StartMenuRows(): always two columns here
        (c0, r0), (c1, r1) = divmod(st["cur"], rows), divmod(items.index(entry), rows)
        if c0 != c1:
            tw.run("hold RIGHT 4" if c1 > c0 else "hold LEFT 4", "wait 14")
            r0 = min(r0, (rows if c1 == 0 else len(items) - rows) - 1)
        for _ in range(abs(r1 - r0)):
            tw.run("hold %s 4" % ("DOWN" if r1 > r0 else "UP"), "wait 14")
        if tw.peek([(8, cur, "c")])["c"] != items.index(entry):
            tw.run("hold B 6", "wait 30")
            raise RouteError("the START menu's cursor did not reach entry %d" % entry)

    def continue_game(self):
        """T-386: from wherever the game is booting -- the intro, the title, the menu, the recap -- to the overworld,
        by watching gMain.callback2 (a Thumb pointer: its low bit set) rather than counting frames, which drift."""
        S = lambda n: elf_symbol(n, self.release)
        title, menu, ow = S("CB2_TitleScreenRun"), S("CB2_MainMenu"), S("CB2_Overworld")
        cb2, recap = tw.symbol("gMain", self.release) + 4, tw.symbol("gQuestLogState", self.release)
        for i in range(120):
            cb = tw.peek([(32, cb2, "cb")])["cb"] & ~1
            if cb == ow:
                self.g.p = None
                if tw.peek([(8, recap, "q")])["q"]:                     # "Previously on your quest...": it runs ON
                    tw.run("hold B 6", "wait 60")                         # the overworld, so B until it is over
                elif self.free():
                    return
                else:
                    tw.run("wait 30")
            elif cb == title:
                tw.run("hold START 6", "wait 60")
            elif cb == menu:
                tw.run("hold A 6", "wait 90")                             # CONTINUE is first
            else:
                tw.run("hold B 6", "wait 60")                             # the intro, a fade, the recap
        raise RouteError("the game never reached the overworld")

    def load(self, kind):
        """T-386: put this build's ROM in the theatre (its save beside it, kept between runs) and continue the game."""
        if kind not in ("debug", "release") or (kind == "release") != self.release:
            raise RouteError("load %s on a %s route" % (kind, "release" if self.release else "debug"))
        built = os.path.join(GBA, "daemonsContent.gba" if self.release else "daemonsContent_debug.gba")
        rom = os.path.join(THEATRE, "rom", "theatre_%s.gba" % kind)
        shutil.copyfile(built, rom)
        tw.run("load %s" % rom, "wait 120")
        self.g.p = None
        self.same_build()                                                   # the ROM now running is this build's
        self.continue_game()

    def save(self):
        """T-386: save the game in the game -- START, SAVE, YES (and YES again over an older save) -- so a save made
        on one ROM can be continued on another: the DEBUG build goes somewhere, saves, and the release ROM starts there."""
        if not self.free():
            raise RouteError("save needs the player free on the overworld")
        self.start_menu(STARTMENU_SAVE)
        tw.run("hold A 6", "wait 60", "hold A 6", "wait 90", "hold A 6", "wait 240")   # SAVE, YES, YES over the old one
        for attempt in range(20):
            if self.free():
                return
            tw.run("hold B 6", "wait 40")
        raise RouteError("the save did not finish")

    def fly(self, folder, x=None, y=None):
        """T-384: GOTO to the town FOLDER lies in, as a player does it, then walk to (X, Y) if given."""
        sec = mapsec_id(map_json(folder)["region_map_section"])
        cells = kanto_cells(sec, self.release)
        if not cells:
            raise RouteError("%s is not on Kanto's map (a SEVII island: GOTO there is not taught yet)" % folder)
        if not self.free():
            raise RouteError("fly needs the player free on the overworld")
        S = lambda n: elf_symbol(n, self.release)
        # 1. START, and to DAEMON
        self.start_menu(STARTMENU_POKEMON)
        tw.run("hold A 6", "wait 100")                                    # the party fades in
        # 2. the daemon under the cursor, and GOTO among its actions (any daemon, while the DRIVER is in the bag)
        tw.run("hold A 6", "wait 30")
        base = tw.peek([(32, S("sPartyMenuInternal"), "p")])["p"]
        acts = tw.peek([(8, base + 15 + i, "a%d" % i) for i in range(9)] + [(8, base + 24, "n")])
        actions = [acts["a%d" % i] for i in range(acts["n"])]
        if fly_action() not in actions:
            tw.run("hold B 6", "wait 30", "hold B 6", "wait 60", "hold B 6", "wait 30")
            raise RouteError("GOTO is not offered: is the GOTO DRIVER in the bag, and its MARK held?")
        for _ in range(actions.index(fly_action())):
            tw.run("hold DOWN 4", "wait 14")
        tw.run("hold A 6", "wait 120")                                    # the region map opens
        # 3. the cursor, steered cell by cell to the nearest of the town's cells
        mc = S("sMapCursor")
        for wait in range(8):                                             # the map, or "Can't use that here."
            if tw.peek([(32, mc, "p")])["p"]:
                break
            tw.run("wait 30")
        else:
            tw.run("hold B 6", "wait 40", "hold B 6", "wait 60", "hold B 6", "wait 40")
            raise RouteError("GOTO can't be used here (indoors, or a cave): walk outside first")
        for tries in range(80):
            p = tw.peek([(32, mc, "p")])["p"]
            if not p:
                tw.run("wait 20"); continue
            c = tw.peek([(16, p, "x"), (16, p + 2, "y"), (16, p + 20, "sec")])
            x0, y0 = c["x"], c["y"]
            tx, ty = min(cells, key=lambda t: abs(t[0] - x0) + abs(t[1] - y0))
            if (x0, y0) == (tx, ty):
                break
            way = "RIGHT" if tx > x0 else "LEFT" if tx < x0 else "DOWN" if ty > y0 else "UP"
            tw.run("hold %s 4" % way, "wait 16")
        else:
            tw.run("hold B 6", "wait 60")
            raise RouteError("the region map's cursor never reached %s -- on the SEVII islands the map opens on them; "
                             "GOTO from Kanto" % folder)
        tw.run("wait 10")
        if tw.peek([(16, p + 20, "sec")])["sec"] != sec:
            raise RouteError("the cursor is on %s's cell but the map names section %d" % (folder, c["sec"]))
        tw.run("hold A 6", "wait 200")                                    # the flight, and the landing's fade
        for attempt in range(60):
            self.g.p = None                         # a flight moves gSaveBlock1: the cached pointer would name the old town
            name, here = self.where()
            if mapsec_id(map_json(name).get("region_map_section", "MAPSEC_NONE")) == sec:
                if self.free():
                    break
                tw.run("wait 60")                   # the landing's fade; then a scene that runs on arrival is played
                if not self.free():                 # out, its boxes captured, as goto does (CALLOW's lock, 2026-10-07)
                    self.boxes()
                continue
            tw.run("wait 30")
        else:
            raise RouteError("GOTO did not land in %s's town" % folder)
        if x is not None:
            if name != folder:
                raise RouteError("GOTO lands in %s, not %s: walk from there with warp and to" % (name, folder))
            tw.walk(self.g, (int(x), int(y)))

    def step(self, line):
        a = words(line)
        op, args = a[0].lower(), a[1:]
        if op == "goto":
            self.goto(args[0], *(int(v) for v in args[1:3]))
        elif op == "fly":
            self.fly(args[0], *(int(v) for v in args[1:3]))
        elif op == "save":                                             # T-386
            self.save()
        elif op == "continue":
            self.continue_game()
        elif op == "load":
            self.load(args[0])
        elif op in ("savestate", "loadstate"):                         # T-386
            states = os.path.join(THEATRE, "states")
            os.makedirs(states, exist_ok=True)
            path = os.path.join(states, args[0] + ".ss")
            if op == "loadstate" and not os.path.exists(path):
                raise RouteError("no state %s -- save it first (savestate %s)" % (args[0], args[0]))
            tw.run("%s %s" % (op, path), "wait 30")
            self.g.p = None                                                # a loaded moment has its own gSaveBlock1
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
        elif op == "finish":
            if not self.free():
                self.boxes()
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
        elif op == "bump":
            self.bump(args[0], "keep" in args[1:])
        elif op == "wild":
            want = "past151" if "past151" in args else next((const_species(v) for v in args if v.startswith("SPECIES_")), None)
            self.wild(want, next((int(v) for v in args if v.isdigit()), 12), "keep" in args)
        elif op == "unsaid":
            bad = fold(" ".join(args))
            if any(bad in fold(t) for t in self.said):
                raise RouteError('a box said "%s"' % " ".join(args))
        elif op == "friendship":
            self.friendship(int(args[0]), int(args[1]))
        elif op == "objectat":
            self.objectat(args[0], args[1:])
        elif op == "mon":
            v = args[2]
            self.mon(int(args[0]), args[1], const_species(v) if v.startswith("SPECIES_") else -1 if v == "max" else -2 if v == "back" else int(v, 0))
        elif op == "coins":
            key = tw.peek([(16, self.addr("*gSaveBlock2Ptr+0xF20"), "k")])["k"]
            self.poke("*gSaveBlock1Ptr+0x294", 16, int(args[0]) ^ key)
        elif op == "keyitem":
            self.keyitem(const_item(args[0]))
        elif op == "follower":
            self.follower(args)
        elif op == "remember":
            self.memory = getattr(self, "memory", {})
            self.memory[args[0]] = (args[1], int(args[2]), self.read(args[1], int(args[2])))
            self.capture("%s = %d" % (args[0], self.memory[args[0]][2]), read_text=False)
        elif op == "moved":
            spec, bits, was = self.memory[args[0]]
            now = self.read(spec, bits)
            self.capture("%s: %d -> %d" % (args[0], was, now), read_text=False)
            if now == was:
                raise RouteError("%s is still %d" % (args[0], now))
        elif op == "foe":
            got = self.foe()
            if got != const_species(args[0]):
                raise RouteError("the battle is against species %d, not %s" % (got, args[0]))
        elif op == "poke":
            self.poke(args[0], int(args[1]), int(args[2], 0))
        elif op == "register":
            self.poke("*gSaveBlock1Ptr+0x296", 16, const_item(args[0]))
        elif op == "play":
            for note in args:
                self.note(note)
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
        elif op == "burst":                                                 # T-430
            self.burst(args[0], int(args[1]), int(args[2]), args[3:])
        elif op == "palette":                                               # T-430
            self.palette(args[0].upper(), int(args[1]), args[2].lower())
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
                    folder = a[1]                                         # an expect says where a script's warp landed
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
    first = next((st for i, st in enumerate(route["stops"], 1) if i >= start and (not only or i in only)), None)
    loads_first = bool(first and first["steps"] and words(first["steps"][0])[0].lower() == "load")
    r = Runner(name, route.get("rom") == "release", check_build=not loads_first)
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
    path = os.path.join(r.out, "report.md")
    if (only or start > 1) and os.path.exists(path):
        #  a part replayed: the stops not played keep their sections from the last report, in route order
        def sections(text):
            out = {}
            for part in re.split(r"(?m)^(?=## \d+\. )", text):
                m = re.match(r"## (\d+)\. ", part)
                if m:
                    out[int(m.group(1))] = part.rstrip("\n") + "\n"
            return out
        old, new = sections(open(path).read()), sections("\n".join(report) + "\n")
        head = "\n".join(report[:4])
        merged = [new.get(i) or old.get(i) for i in range(1, len(route["stops"]) + 1)]
        open(path, "w").write(head + "\n" + "\n".join(m for m in merged if m))
    else:
        open(path, "w").write("\n".join(report) + "\n")
    print("%d stops failed; report and sheets in %s" % (failures, os.path.relpath(r.out, ROOT)))
    sys.exit(failures)


if __name__ == "__main__":
    main()
