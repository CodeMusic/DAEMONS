#!/usr/bin/env python3
"""Play a route through the theatre, stop by stop, and write what it saw (T-378, the 6 October work-day run).

    python3 tools/theatre_route.py tools/routes/field-test.json            # play every stop
    python3 tools/theatre_route.py tools/routes/field-test.json --from 4   # from the fourth stop on
    python3 tools/theatre_route.py tools/routes/field-test.json --only 2,5
    python3 tools/theatre_route.py --check tools/routes/field-test.json    # parse it and resolve every name; no theatre
    python3 tools/theatre_route.py tools/routes/field-test.json --stop-timeout 600   # each stop's limit (default 900 s)

A route is JSON: {"rom": "debug" | "release", "about": "...", "stops": [{"stop": "a name", "steps": [...]}]}, and each
step is one line, split like a shell line. A stop may carry "timeout": SECONDS, and a route "stop_timeout": SECONDS, for
a stop that needs longer than --stop-timeout (T-451):

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
    lose                       DEBUG: lose it (gBattleOutcome = 2, then a turn) -- a white-out follows (T-431)
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
    mon SLOT away|egg|hp|shiny|species|item|status VALUE   T-18 P3 (item and status T-433): the same for the rest of a party daemon -- AWAY (T-358's bit,
                               0|1), an egg (0|1), its hit points (0 HALTS it, max heals it), shiny (0|1: its OT ID set so it is, or
                               the player's own back, every secure word re-keyed), its species (SPECIES_X, a number, or back:
                               an evolution or a trade, as the follower sees one)
    bag ITEM_X [N] [first]     T-433: put N (default 1) of an item in its pocket of the bag, or top it up to N; with
                               first, in the pocket's top slot, and the bag set to open there with its cursor on it
    open BAG|DAEMON            T-433: START, then that entry, opened (captured)
    swap SLOT SLOT             T-433: two party daemons change places (their records swapped whole)
    useitem ITEM_X             T-433, DEBUG: the item used on party daemon 1 as the party menu would (gSpecialVar_ItemId
                               poked, then GAME EVENTS -> FEELINGS -> USE THE ITEM ON SLOT 1)
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
    follower emoji EYES MOUTH TINT [grey|colour] | follower emoji bubble   T-431 P3: fail unless the last `follower
                               talk` drew that daemon-emoji (EYES calm|open|wide, MOUTH down|flat|up, TINT none|warm|hot;
                               its OBJ palette all but grey, or in colour) -- or the trainers' bubble (the !! of a hidden
                               item, or no palette slot for a face)
    palettes full|free         T-431 P3: fill every free OBJ palette slot with a placeholder tag (and give them back)
    follower probe             T-431 P3, DEBUG: press A on it and print the bubble's sprite frame by frame for 70 frames
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
    debug ROW [ROW ...]        T-458: START -> DEBUG, then each row by its START-menu name on the page it is on (ENCOUNTER,
                               DEVICE, HEAL: src/start_menu.c's STARTMENU_DBG_<ROW>), each pressed with A; the page left
                               open is captured, then B closes the lot -- `debug ENCOUNTER DEVICE` answers a SEND
    events "ROW" ["ROW" ...]   T-431: DEBUG -> GAME EVENTS, then each row by its label on the page it is on (a "NAME >"
                               row opens its page; "#N" is the page's Nth row, from 0), each pressed with A; the page
                               left open is captured, then B closes the lot. Read from src/daemons_debug_events.c.
    feelings party SLOT|box BOX POS [CHECK ...]   T-431: a daemon's feelings as the game reads them now (its record
                               decrypted, faded by the stamp's age against the clock the game last read), captioned;
                               each CHECK fails the stop unless it holds: glad|mad|sad|calm|friendship (=, <, >, <=, >=) N;
                               set=0|1 (ever pushed: its bit, even on an egg); egg=0|1; keep=NAME (note all four); half=NAME (each about half of NAME's);
                               same=NAME (each within 1 of NAME's); more=NAME:AXIS (that axis risen since NAME)
    conditions SLOT A B C D E SHEEN   T-431: write a party daemon's six contest-condition bytes raw, as an in-game trade
                               does (trade_scene.c) -- leaving its feelings' "set" bit as it is
    feel SLOT GLAD MAD SAD CALM [SLOT ...]   T-431 P2: give party daemons feelings outright -- the four values written,
                               the "set" bit and the clock's bit set, stamped NOW (the clock read by opening DEBUG ->
                               GAME EVENTS -> FEELINGS first, which the capture shows); `feel SLOT unset` clears the bit
    summary SLOT [KEY ...]     T-431 P2: START, DAEMON, the daemon in SLOT, SUMMARY; capture, then press each KEY (R, L,
                               UP, DOWN, A, B) and capture after it, each captioned with the page on screen and, on the
                               fourth page, the line it drew. Left open for `shown`; `close` leaves it
    boxsummary [KEY ...]       the same from the PC's box screen (MOVE DAEMON), its cursor on a daemon: A, SUMMARY, A
    keys KEY ...               press each KEY in the open SUMMARY, capturing after each as `summary` does
    shown [page=NAME] [line=TEXT] [cell=C,R] [grey]   fail unless the summary shows that page (INFO, SKILLS, MOVES,
                               MOVES_INFO, FEELINGS), the fourth page drew that line and put the dot in that cell
                               (0-8 across, 0-8 down) -- read from the DEBUG build's gFeelingsDebugShown
    close                      press B until the player is free again

WHO is a person on the current map: their LOCALID_ name, their script's name (or a unique part of it), or "X,Y".

What it writes, in .theatre/routes/<route>/ (gitignored): each stop's frames, one contact sheet per stop
("NN - stop.png", every capture labelled with the words the box held), and report.md -- every stop passed or failed
and why, and every box's text. A stop that fails is reported and the run goes on to the next stop, which usually
starts with a goto. Exit status is the number of stops that failed.

NOTHING WAITS FOREVER (T-451). The run starts with a ping (tools/theatre_walk.py): a theatre whose script is not running
fails in seconds -- "the theatre is not answering: re-run theatre.lua in mGBA" -- instead of after every stop's first
batch. Each stop runs inside its own wall-clock limit (STOP_SECONDS, a stop's "timeout", --stop-timeout) and fails with
"stop N ran past its limit" when it is up; each walk inside it has WALK_SECONDS, each batch its own frames' worth; every
retry loop counts its tries. A batch the theatre never answers stops the whole run there (the rest is reported "not
played"): nothing after it could have worked.

WHY. The field test's route was walked by hand, by screenshot, once per release. A route file makes it replayable
after every release, and reading each box's text out of gStringVar4 (where every field message is expanded before it
prints) means a stop can check the words, not only show them.
"""
import json, os, re, shlex, shutil, subprocess, sys, textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theatre_walk as tw                                                 # noqa: E402

STOP_SECONDS = 900                                                        # one stop's wall clock (T-451)

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


_NM = {}


def elf_symbol(name, release):
    """A static (sLockFieldControls, ...) is in the .elf's symbols, not the .map. The symbol table is read once per
    build (T-431 P3: an nm per call took longer than the follower's one-second bubble lasts)."""
    elf = os.path.join(GBA, "daemonsContent.elf" if release else "daemonsContent_debug.elf")
    key = (elf, os.path.getmtime(elf))
    if key not in _NM:
        _NM[key] = subprocess.run(["arm-none-eabi-nm", elf], capture_output=True, text=True).stdout
    out = _NM[key]
    m = re.search(r"^([0-9a-f]{8}) \w %s$" % re.escape(name), out, re.M)
    if not m:
        raise RouteError("no symbol %s in %s" % (name, os.path.basename(elf)))
    return int(m.group(1), 16)


# ---- T-384: GOTO the game's own way, for a route on the RELEASE ROM ---------------------------------------------------
# The DEBUG build warps by poking gDaemonsDebugWarp; the ROM players get has no such thing, but every daemon offers GOTO
# (FLY) while the GOTO DRIVER is in the bag (T-199). So `fly` plays it as a player would: START, DAEMON, a daemon, GOTO,
# and then the region map, whose cursor is steered by reading it out of RAM (sMapCursor) until the town is under it.
STARTMENU_POKEMON, STARTMENU_SAVE = 1, 4                                     # src/start_menu.c's enum: DAEMON's, SAVE's


def start_menu_entries():
    """{STARTMENU_X: its number}, counted down src/start_menu.c's enum (the DEBUG rows included, as the debug build has
    them): the debug pages are lists of these, like the START menu itself (T-458)."""
    src = open(os.path.join(GBA, "src/start_menu.c")).read()
    body = re.search(r"enum StartMenuOption\s*\{\s*(STARTMENU_POKEDEX.*?)MAX_STARTMENU_ITEMS", src, re.S).group(1)
    names = re.findall(r"^\s*(STARTMENU_\w+)\s*(?:=\s*0\s*)?,", body, re.M)
    return {n: i for i, n in enumerate(names)}


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
        self.stop_seconds = STOP_SECONDS
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
        if field == "status":                                             # T-433: status1 (1-7 asleep that many turns)
            tw.run("poke16 %s %d" % (hex(base + 80), value & 0xFFFF), "poke16 %s %d" % (hex(base + 82), value >> 16))
            return
        if field == "egg":
            word = 3 * order.index("M") + 1                               # misc: ivs, isEgg (bit 30), abilityNum
            secure[word] = (secure[word] | (1 << 30)) if value else (secure[word] & ~(1 << 30))
            flags = (flags | 0x04) if value else (flags & ~0x04)
            cmds.append("poke8 %s %d" % (hex(base + 19), flags))
        elif field == "item":                                             # T-433: the item it holds (0: nothing)
            word = 3 * order.index("G")
            secure[word] = (secure[word] & 0xFFFF) | (value << 16)
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
            raise RouteError("mon: no field %s (away, egg, hp, shiny, species, item, status)" % field)
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

    def swap(self, a, b):
        """T-433: swap two party daemons' whole records (each is self-contained: its own key and checksum)."""
        party = tw.symbol("gPlayerParty", self.release)
        rec = {}
        for slot in (a, b):
            w = tw.peek([(32, party + 100 * slot + 4 * k, "w%d" % k) for k in range(25)])
            rec[slot] = [w["w%d" % k] for k in range(25)]
        cmds = []
        for slot, other in ((a, b), (b, a)):
            for k in range(25):
                at, v = party + 100 * slot + 4 * k, rec[other][k]
                cmds += ["poke16 %s %d" % (hex(at), v & 0xFFFF), "poke16 %s %d" % (hex(at + 2), v >> 16)]
        hold = elf_symbol("sFollower", self.release)
        tw.run("poke8 %s 255" % hex(hold + 35), "poke8 %s 255" % hex(hold + 36), *cmds,
               "poke8 %s 0" % hex(hold + 35), "poke8 %s 1" % hex(hold + 36))

    BAG_POCKETS = {"items": (0x310, 42, 0), "key": (0x3B8, 30, 1), "balls": (0x430, 13, 2), "tmhm": (0x464, 58, None),
                   "berries": (0x54C, 43, None)}

    def bag(self, item, count, first=False):
        """T-433: put COUNT of an item in its pocket of the bag (a slot of SaveBlock1's ITEMS, KEY ITEMS, BALLS, TM CASE
        or BERRY POUCH, its count stored XOR the save's key) -- topped up to COUNT if it is there. With first, it is
        moved to the pocket's top slot (what was there swapped into its place) and the bag is set to open on that
        pocket, its cursor on it (gBagMenuState: pocket +6, itemsAbove +8, cursorPos +14)."""
        pocket = ("balls" if 1 <= item <= 12 else "berries" if 133 <= item <= 175 else "tmhm" if 289 <= item <= 346
                  else "key" if 259 <= item <= 288 or 349 <= item <= 376 else "items")
        start, n, menu = self.BAG_POCKETS[pocket]
        key = tw.peek([(16, self.addr("*gSaveBlock2Ptr+0xF20"), "k")])["k"]
        slot = lambda i: "*gSaveBlock1Ptr+0x%X" % (start + 4 * i)
        have = [(self.read(slot(i), 16), self.read("*gSaveBlock1Ptr+0x%X" % (start + 4 * i + 2), 16)) for i in range(n)]
        at = next((i for i, h in enumerate(have) if h[0] == item), None)
        if at is None:
            at = next((i for i, h in enumerate(have) if h[0] == 0), None)
        if at is None:
            raise RouteError("the %s pocket is full" % pocket)
        put = {at: (item, count ^ key)}
        if first and at != 0:
            put = {0: (item, count ^ key), at: have[0]}
        for i, (it, qty) in put.items():
            self.poke(slot(i), 16, it)
            self.poke("*gSaveBlock1Ptr+0x%X" % (start + 4 * i + 2), 16, qty)
        if first and menu is not None:
            state = tw.symbol("gBagMenuState", self.release)
            tw.run("poke16 %s %d" % (hex(state + 6), menu), "poke16 %s 0" % hex(state + 8 + 2 * menu),
                   "poke16 %s 0" % hex(state + 14 + 2 * menu))

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
        if args[0] == "emoji":                                            # T-431 P3: a check, no capture
            return self.follower_emoji(args[1:])
        state, dx, dy = self.follower_state()
        where = "" if dx is None else " at %+d,%+d px from the player" % (dx, dy)
        self.capture("follower %s%s" % (state, where), read_text=False)
        want = args[0]
        if want == "talk":
            return self.follower_talk(state, dx, dy)
        if want == "probe":                                               # T-431 P3, DEBUG
            return self.follower_probe(state, dx, dy)
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
        self.bubble_symbols()                                             # before A: the bubble lasts a second
        tw.run("hold A 6", "wait 10")
        n = len(self.frames)
        self.capture("the bubble", read_text=False)                       # it lasts a second; the box outlasts it
        self.bubble = self.bubble_state()                                 # T-431 P3: which face, in what colour
        self.frames[n] = (self.frames[n][0], "the bubble: %s" % self.bubble["caption"], "")
        with open(os.path.join(self.out, "bubbles.jsonl"), "a") as f:                     # for a close-up sheet
            f.write(json.dumps({"frame": self.frames[-1][0], "stop": self.stop_no, **self.bubble}) + "\n")
        tw.run("wait 24")
        self.boxes()

    def follower_probe(self, state, dx, dy):
        """T-431 P3, DEBUG: press A on it and print, frame by frame for 70 frames (the theatre's trace), what the
        bubble's sprite does -- in use, its callback, its anim delay -- with the face drawn (gFollowerDebugEmoji) and
        the follower's own sprite: what takes a bubble away, and when. (It showed the bubble lives its 60 frames; the
        route had been looking too late, after an nm per symbol.)"""
        d = {(-16, 0): "LEFT", (16, 0): "RIGHT", (0, -16): "UP", (0, 16): "DOWN"}.get((dx, dy))
        if state != "shown" or d is None:
            raise RouteError("the follower is %s, not a tile from the player to probe" % state)
        obj = tw.peek([(8, tw.symbol("gPlayerAvatar", self.release) + 5, "o")])["o"]
        facing = tw.peek([(8, self.objects + OBJECT_EVENT * obj + 0x18, "f")])["f"] & 0xF
        if facing != self.FACING[d]:
            tw.run("hold %s 4" % d, "wait 12")
        sprites = tw.symbol("gSprites", self.release)
        face_at = elf_symbol("gFollowerDebugEmoji", self.release)
        names = {elf_symbol(n, self.release): n for n in ("SpriteCB_FollowerEmoji", "SpriteCB_FollowerEmote",
                                                          "SpriteCB_Follower", "SpriteCallbackDummy")}
        base = elf_symbol("sFollower", self.release)
        fid = tw.peek([(8, base + 33, "fid")])["fid"]
        slot = sprites + self.SPRITE * (self.MAX_SPRITES - 4)          # CreateSpriteAtEnd's first free, below the box's
        specs = ["32:%s" % hex(slot + 0x1C), "16:%s" % hex(slot + 0x3E), "8:%s" % hex(slot + 0x2C), "8:%s" % hex(face_at),
                 "8:%s" % hex(base + 33), "32:%s" % hex(sprites + self.SPRITE * fid + 0x1C)]
        tw.run("hold A 2", "trace probe 70 " + " ".join(specs))
        lines = open(os.path.join(THEATRE, "probe.trace")).read().split("\n")
        for k, line in enumerate(lines):
            if not line.strip():
                continue
            cb, fl, delay, face, sid, fcb = [int(x, 16) for x in line.split()]
            print("   probe f%02d: sprite60 %s flags %04x delay %d face %d | follower %d %s" % (
                k, names.get(cb & ~1, hex(cb)), fl, delay & 0x3F, face - 1, sid, names.get(fcb & ~1, hex(fcb))))
        tw.run("wait 60")
        self.boxes()

    EYES, MOUTHS, TINTS = ("calm", "open", "wide"), ("down", "flat", "up"), ("none", "warm", "hot")

    def snapshot(self, reads):
        """reads: [(bits, address, name)] -> {name: value}, all from ONE frame (the theatre's `trace` for a frame).
        tw.peek runs a command a frame, so 193 reads took 193 frames -- three seconds, longer than a bubble lasts."""
        tw.run("trace snapshot 1 " + " ".join("%d:%s" % (b, hex(a)) for b, a, _ in reads))
        vals = open(os.path.join(THEATRE, "snapshot.trace")).read().split()
        return {n: int(x, 16) for (_, _, n), x in zip(reads, vals)}

    def bubble_symbols(self):
        self.bsym = (tw.symbol("gSprites", self.release), elf_symbol("SpriteCB_FollowerEmoji", self.release),
                     elf_symbol("SpriteCB_FollowerEmote", self.release), elf_symbol("gFollowerDebugEmoji", self.release))

    def bubble_state(self):
        """T-431 P3: the bubble over the follower now -- the daemon-emoji (its face from gFollowerDebugEmoji, the DEBUG
        build's last face drawn, and its OBJ palette read out of palette RAM) or the trainers' bubble, or none."""
        sprites, emoji, emote, face_at = self.bsym
        v = self.snapshot([(32, sprites + self.SPRITE * i + 0x1C, "cb%d" % i) for i in range(self.MAX_SPRITES)] +
                          [(16, sprites + self.SPRITE * i + 0x3E, "fl%d" % i) for i in range(self.MAX_SPRITES)] +
                          [(16, sprites + self.SPRITE * i + 4, "a2%d" % i) for i in range(self.MAX_SPRITES)] +
                          [(8, face_at, "face")])
        for i in range(self.MAX_SPRITES):
            if not v["fl%d" % i] & 1:
                continue
            cb = v["cb%d" % i] & ~1
            if cb == emoji:
                slot = v["a2%d" % i] >> 12
                face = v["face"] - 1
                base = 0x05000200 + 32 * slot
                got = self.snapshot([(16, base + 2 * k, "c%d" % k) for k in range(1, 16)])
                chroma = max(max(c & 31, (c >> 5) & 31, (c >> 10) & 31) - min(c & 31, (c >> 5) & 31, (c >> 10) & 31)
                             for c in (got["c%d" % k] for k in range(1, 16)))
                name = "%s %s %s" % (self.EYES[face // 3 % 3], self.MOUTHS[face % 3], self.TINTS[face // 9])
                return {"kind": "emoji", "face": name, "slot": slot, "chroma": chroma,
                        "caption": "face %d (%s), OBJ palette %d, chroma %d" % (face, name, slot, chroma)}
            if cb == emote:
                return {"kind": "bubble", "caption": "the trainers' bubble"}
        return {"kind": None, "caption": "none"}

    def follower_emoji(self, args):
        """follower emoji EYES MOUTH TINT [grey|colour] | follower emoji bubble -- what the last `follower talk` drew."""
        b = getattr(self, "bubble", None) or {"kind": None, "caption": "no talk yet"}
        if args[0] == "bubble":
            if b["kind"] != "bubble":
                raise RouteError("the bubble was %s, not the trainers' bubble" % b["caption"])
            return
        if b["kind"] != "emoji":
            raise RouteError("the bubble was %s, not a daemon-emoji" % b["caption"])
        want = " ".join(args[:3])
        if b["face"] != want:
            raise RouteError("the face was %s, not %s" % (b["face"], want))
        if len(args) > 3:                       # 5-bit channels: grey is all but flat, colour has some saturation
            if args[3] == "grey" and b["chroma"] > 4 or args[3] == "colour" and b["chroma"] < 10:
                raise RouteError("its palette is not %s: %s" % (args[3], b["caption"]))

    def poke(self, spec, bits, value):
        at = self.addr(spec)
        if bits == 32:                                                    # the theatre writes 8 and 16 bits
            tw.run("poke16 %s %d" % (hex(at), value & 0xFFFF), "poke16 %s %d" % (hex(at + 2), value >> 16))
        else:
            tw.run("poke%d %s %d" % (bits, hex(at), value))

    def palettes(self, how):
        """palettes full|free -- T-431 P3: take every FREE OBJ palette slot (sSpritePaletteTags = TAG_NONE) with a
        placeholder tag, so nothing new can load a palette; `free` gives back exactly the slots it took. Slots in use
        (the follower's, a field effect's) are never touched -- poking fixed slots once took the follower's own."""
        tags = elf_symbol("sSpritePaletteTags", self.release)
        if how == "full":
            v = tw.peek([(16, tags + 2 * i, "t%d" % i) for i in range(16)])
            self.taken = [i for i in range(16) if v["t%d" % i] == 0xFFFF]
            tw.run(*["poke16 %s %d" % (hex(tags + 2 * i), 0x7777) for i in self.taken])
        elif how == "free":
            tw.run(*["poke16 %s %d" % (hex(tags + 2 * i), 0xFFFF) for i in getattr(self, "taken", [])])
            self.taken = []
        else:
            raise RouteError("palettes full|free")

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

    def win(self, result=1):
        if self.release:
            raise RouteError("win pokes the battle's outcome: DEBUG routes only")
        outcome = tw.symbol("gBattleOutcome", False)
        for _ in range(30):
            if not self.g.state()["battle"]:
                return
            # the outcome is read at the end of a TURN: so take one -- ROUTINES (top left), then the first routine.
            # A on DETACH takes none ("You cannot DETACH from a USER engagement!"), and that loop never ends.
            tw.run("poke8 %s %d" % (hex(outcome), result), "hold B 8", "wait 30", "hold UP 6", "wait 10", "hold LEFT 6", "wait 10",
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

    # ---- T-431: GAME EVENTS by label, and a daemon's feelings read out of its record ----------------------------

    def event_pages(self):
        """{page enum: [(label or None, kind, arg)]} and the page enum's order, from src/daemons_debug_events.c."""
        src = open(os.path.join(GBA, "src/daemons_debug_events.c")).read()
        pages = re.search(r"enum \{ (PG_EVENTS[^}]*)\}", src).group(1).replace(" ", "").split(",")
        names = dict(re.findall(r'static const u8 (sName_\w+)\[\]\s*=\s*_\("([^"]*)"\)', src))
        rows_of = dict(re.findall(r"\[(PG_\w+)\]\s*=\s*\{\s*(sRows_\w+)", src))
        out = {}
        for pg, arr in rows_of.items():
            body = re.search(r"static const struct DbgRow %s\[\] = \{(.*?)\n\};" % arr, src, re.S).group(1)
            out[pg] = [(names.get(n), k, g) for n, k, g in re.findall(r"\{\s*(\w+),\s*(R_\w+),\s*([^}]+?)\s*\}", body)]
        return out, pages

    def list_cursor(self):
        """T-458: the row a ListMenu's cursor is on (its scroll + its row on screen), read from the task the list menu
        runs as (ListMenuDummyTask's data is the struct ListMenu: cursorPos at +0x18, itemsAbove at +0x1A); None when
        no list is open."""
        S = lambda n: elf_symbol(n, self.release)
        tasks, dummy = tw.symbol("gTasks", self.release), S("ListMenuDummyTask") & ~1
        st = tw.peek([(32, tasks + 40 * i, "f%d" % i) for i in range(16)] + [(8, tasks + 40 * i + 4, "a%d" % i) for i in range(16)])
        for i in range(16):
            if st["a%d" % i] and st["f%d" % i] & ~1 == dummy:
                c = tw.peek([(16, tasks + 40 * i + 8 + 0x18, "scroll"), (16, tasks + 40 * i + 8 + 0x1A, "row")])
                return c["scroll"] + c["row"]
        return None

    def events(self, labels):
        pages, order = self.event_pages()
        S = lambda n: elf_symbol(n, self.release)
        rows_at, scroll_at = S("sRow"), S("sScroll")
        tw.run(*["poke16 %s 0" % hex(a + 2 * k) for a in (rows_at, scroll_at) for k in range(len(order) - 1)])
        self.start_menu(10)                                               # STARTMENU_DEBUG
        tw.run("hold A 6", "wait 50")                                     # its main page, the cursor on GAME EVENTS
        tw.run("hold A 6", "wait 90")                                     # GAME EVENTS: the title, then the list
        page, cursor = "PG_EVENTS", 0
        for label in labels:
            rows = pages[page]
            if label.startswith("#"):
                idx = int(label[1:])
            else:
                hits = [i for i, r in enumerate(rows) if r[0] and fold(r[0]) == fold(label)]
                if len(hits) != 1:
                    raise RouteError("GAME EVENTS: no row %s on %s" % (label, page))
                idx = hits[0]
            #  T-458: read the list's own cursor and step until it is on the row -- a DOWN dropped in a 12-frame gap put
            #  A on the row above, and GLOBAL INDEX (a toggle) was taken away instead of CRYSTAL'S LINE AGAIN given
            for tries in range(3 * len(rows) + 6):
                at = self.list_cursor()
                if at is None:
                    at = cursor
                if at == idx:
                    break
                tw.run("hold %s 4" % ("DOWN" if idx > at else "UP"), "wait 20")
                if self.list_cursor() is None:
                    cursor += 1 if idx > at else -1
            if self.list_cursor() not in (idx, None):
                self.close()
                raise RouteError("GAME EVENTS: the cursor never reached %s" % label)
            tw.run("hold A 6", "wait 90")
            name, kind, arg = rows[idx]
            if kind == "R_PAGE":
                page, cursor = arg, 0
            else:
                cursor = idx
        self.capture("GAME EVENTS: " + " / ".join(labels))
        for _ in range(4):
            if self.free():
                break
            tw.run("hold B 6", "wait 60")
        if not self.free():
            raise RouteError("GAME EVENTS did not close")

    def debug(self, rows):
        """T-458: START -> DEBUG, then each row by name. The debug pages are ONE column (StartMenuIsTwoColumns), and
        each opens with its cursor on the top row; the cursor is read back before every A all the same."""
        entries = start_menu_entries()
        want = []
        for r in rows:
            name = "STARTMENU_DBG_" + r.upper()
            if name not in entries:
                raise RouteError("the DEBUG menu has no row %s" % r)
            want.append(entries[name])
        S = lambda n: elf_symbol(n, self.release)
        cur, num, order = S("sStartMenuCursorPos"), S("sNumStartMenuItems"), S("sStartMenuOrder")
        self.start_menu(entries["STARTMENU_DEBUG"])
        tw.run("hold A 6", "wait 50")
        for r, entry in zip(rows, want):
            for tries in range(4):
                st = tw.peek([(8, cur, "cur"), (8, num, "num")] + [(8, order + i, "o%d" % i) for i in range(12)])
                items = [st["o%d" % i] for i in range(st["num"])]
                if entry in items:
                    break
                tw.run("wait 20")
            if entry not in items:
                self.close()
                raise RouteError("DEBUG: no row %s on this page" % r)
            for _ in range(abs(items.index(entry) - st["cur"])):
                tw.run("hold %s 4" % ("DOWN" if items.index(entry) > st["cur"] else "UP"), "wait 14")
            if tw.peek([(8, cur, "c")])["c"] != items.index(entry):
                self.close()
                raise RouteError("DEBUG: the cursor did not reach %s" % r)
            tw.run("hold A 6", "wait 50")
        self.capture("DEBUG: " + " / ".join(rows))
        self.close()

    FADE = [round(255 * 2 ** (-d / 18)) for d in range(145)]              # src/daemons_feelings.c's sFade

    def record(self, where):
        """(base address, 80-byte record words) for ('party', slot) or ('box', box, pos)."""
        if where[0] == "party":
            base = tw.symbol("gPlayerParty", self.release) + 100 * where[1]
        else:
            base = self.addr("*gPokemonStoragePtr") + 4 + 80 * (30 * where[1] + where[2])
        w = tw.peek([(32, base + 4 * k, "w%d" % k) for k in range(20)])
        return base, [w["w%d" % k] for k in range(20)]

    def feelings_of(self, where):
        base, words_ = self.record(where)
        pid, otid = words_[0], words_[1]
        secure = [words_[8 + k] ^ pid ^ otid for k in range(12)]
        raw = b"".join(x.to_bytes(4, "little") for x in secure)
        order = self.ORDERS[pid % 24]
        e, m, g = 12 * order.index("E"), 12 * order.index("M"), 12 * order.index("G")
        cond = raw[e + 6: e + 12]
        ribbons = (int.from_bytes(raw[m + 8: m + 12], "little") >> 27) & 0xF
        egg = (int.from_bytes(raw[m + 4: m + 8], "little") >> 30) & 1
        nowv = tw.peek([(16, elf_symbol("gFeelingsDebugNow", self.release), "now"),
                        (16, elf_symbol("gFeelingsDebugNow", self.release) + 2, "clock")])
        stamp = cond[4] | (cond[5] << 8)
        ticks = (nowv["now"] - stamp) & 0xFFFF
        if bool(ribbons & 2) != bool(nowv["clock"]):
            ticks = 0xFFFF
        fade = lambda v: 0 if ticks > 144 else (v * self.FADE[ticks] + 127) // 255
        signed = cond[3] - 256 if cond[3] > 127 else cond[3]
        f = {"glad": 0, "mad": 0, "sad": 0, "calm": 0}
        if ribbons & 1 and not egg:
            f = {"glad": fade(cond[0]), "mad": fade(cond[1]), "sad": fade(cond[2]),
                 "calm": -fade(-signed) if signed < 0 else fade(signed)}
        f.update({"set": int(bool(ribbons & 1)), "friendship": raw[g + 9], "egg": egg, "stamp": stamp,
                  "ticks": ticks, "raw": list(cond), "clock": nowv["clock"]})
        return f

    def feelings(self, args):
        if args[0] == "party":
            where, checks = ("party", int(args[1])), args[2:]
        else:
            where, checks = ("box", int(args[1]), int(args[2])), args[3:]
        f = self.feelings_of(where)
        self.feel_memory = getattr(self, "feel_memory", {})
        cap = "%s: G %d M %d S %d C %d F %d%s%s, stamp %d (%s ago, %s)" % (
            " ".join(map(str, where)), f["glad"], f["mad"], f["sad"], f["calm"], f["friendship"],
            "" if f["set"] else " -- never set", " EGG" if f["egg"] else "", f["stamp"],
            "a day+" if f["ticks"] > 144 else "%d ticks" % f["ticks"], "clock" if f["clock"] else "play time")
        self.capture(cap, read_text=False)
        self.said.append(cap)
        AX = ("glad", "mad", "sad", "calm")
        for c in checks:
            m = re.fullmatch(r"(glad|mad|sad|calm|friendship|set|egg)(<=|>=|=|<|>)(-?\d+)", c)
            if m:
                k, op, n = m.group(1), m.group(2), int(m.group(3))
                ok = {"=": f[k] == n, "<": f[k] < n, ">": f[k] > n, "<=": f[k] <= n, ">=": f[k] >= n}[op]
                if not ok:
                    raise RouteError("%s is %d, not %s %d" % (k, f[k], op, n))
                continue
            k, _, name = c.partition("=")
            if k == "keep":
                self.feel_memory[name] = {a: f[a] for a in AX}
            elif k == "half":
                was = self.feel_memory[name]
                off = [a for a in AX if abs(f[a] - was[a] / 2) > 1]
                if off:
                    raise RouteError("not halved since %s: %s" % (name, ", ".join("%s %d -> %d" % (a, was[a], f[a]) for a in off)))
            elif k == "same":
                was = self.feel_memory[name]
                off = [a for a in AX if abs(f[a] - was[a]) > 1]
                if off:
                    raise RouteError("changed since %s: %s" % (name, ", ".join("%s %d -> %d" % (a, was[a], f[a]) for a in off)))
            elif k == "more":
                name, _, axis = name.partition(":")
                if not f[axis] > self.feel_memory[name][axis]:
                    raise RouteError("%s has not risen since %s (%d -> %d)" % (axis, name, self.feel_memory[name][axis], f[axis]))
            else:
                raise RouteError("feelings: no check %s" % c)

    def conditions(self, slot, values):
        """An in-game trade's six condition bytes, written raw (trade_scene.c), the feelings' bits left alone."""
        base, words_ = self.record(("party", slot))
        pid, otid = words_[0], words_[1]
        key = pid ^ otid
        secure = [words_[8 + k] ^ key for k in range(12)]
        raw = bytearray(b"".join(x.to_bytes(4, "little") for x in secure))
        e = 12 * self.ORDERS[pid % 24].index("E")
        raw[e + 6: e + 12] = bytes(values)
        secure = [int.from_bytes(raw[4 * k: 4 * k + 4], "little") for k in range(12)]
        halves = [h for x in secure for h in (x & 0xFFFF, x >> 16)]
        cmds = ["poke16 %s %d" % (hex(base + 28), sum(halves) & 0xFFFF)]
        for k in range(12):
            enc = secure[k] ^ key
            if enc != words_[8 + k]:
                cmds += ["poke16 %s %d" % (hex(base + 32 + 4 * k), enc & 0xFFFF),
                         "poke16 %s %d" % (hex(base + 32 + 4 * k + 2), enc >> 16)]
        hold = elf_symbol("sFollower", self.release)
        tw.run("poke8 %s 255" % hex(hold + 35), "poke8 %s 255" % hex(hold + 36), *cmds,
               "poke8 %s 0" % hex(hold + 35), "poke8 %s 1" % hex(hold + 36))

    # ---- T-431 P2: the SUMMARY's fourth page ---------------------------------------------------------------------

    PAGES = ["INFO", "SKILLS", "MOVES", "MOVES_INFO", "UNK4", "MOVE_DELETER", "FEELINGS"]
    PAGE_OFFSET = 0x3214                                                   # PokemonSummaryScreenData.curPageIndex

    def edit_record(self, slot, fn):
        """Decrypt party daemon SLOT's secure words, let fn change them (a bytearray, the four substructs in their
        order, and that order), and write them back with the checksum made again -- as the game would."""
        base, words_ = self.record(("party", slot))
        pid, otid = words_[0], words_[1]
        key = pid ^ otid
        secure = [words_[8 + k] ^ key for k in range(12)]
        raw = bytearray(b"".join(x.to_bytes(4, "little") for x in secure))
        fn(raw, self.ORDERS[pid % 24])
        secure = [int.from_bytes(raw[4 * k: 4 * k + 4], "little") for k in range(12)]
        halves = [h for x in secure for h in (x & 0xFFFF, x >> 16)]
        cmds = ["poke16 %s %d" % (hex(base + 28), sum(halves) & 0xFFFF)]
        for k in range(12):
            enc = secure[k] ^ key
            if enc != words_[8 + k]:
                cmds += ["poke16 %s %d" % (hex(base + 32 + 4 * k), enc & 0xFFFF),
                         "poke16 %s %d" % (hex(base + 32 + 4 * k + 2), enc >> 16)]
        hold = elf_symbol("sFollower", self.release)
        tw.run("poke8 %s 255" % hex(hold + 35), "poke8 %s 255" % hex(hold + 36), *cmds,
               "poke8 %s 0" % hex(hold + 35), "poke8 %s 1" % hex(hold + 36))

    def feel(self, args):
        """feel SLOT G M S C [SLOT G M S C ...] -- or SLOT unset."""
        self.events(["FEELINGS >"])                                       # reads the clock: gFeelingsDebugNow
        at = elf_symbol("gFeelingsDebugNow", self.release)
        nowv = tw.peek([(16, at, "now"), (16, at + 2, "clock")])
        i = 0
        while i < len(args):
            slot = int(args[i])
            if args[i + 1] == "unset":
                vals, i = None, i + 2
            else:
                vals, i = [int(v) for v in args[i + 1: i + 5]], i + 5

            def fn(raw, order, vals=vals):
                e, m = 12 * order.index("E"), 12 * order.index("M")
                word = int.from_bytes(raw[m + 8: m + 12], "little")
                ribbons = (word >> 27) & 0xF
                if vals is None:
                    ribbons &= ~1
                else:
                    g, md, s, c = vals
                    raw[e + 6: e + 12] = bytes([g, md, s, c & 0xFF, nowv["now"] & 0xFF, nowv["now"] >> 8])
                    ribbons = (ribbons & ~3) | 1 | (2 if nowv["clock"] else 0)
                word = (word & ~(0xF << 27)) | (ribbons << 27)
                raw[m + 8: m + 12] = word.to_bytes(4, "little")
            self.edit_record(slot, fn)

    def summary_state(self):
        ptr = tw.peek([(32, elf_symbol("sMonSummaryScreen", self.release), "p")])["p"]
        if not ptr:
            return None, None, None
        page = tw.peek([(8, ptr + self.PAGE_OFFSET, "pg")])["pg"]
        shown = elf_symbol("gFeelingsDebugShown", self.release)
        got = tw.peek([(32, shown, "line"), (32, shown + 4, "cell")])
        line = None
        if got["line"] >= 0x08000000:
            rom = open(os.path.join(GBA, "daemonsContent.gba" if self.release else "daemonsContent_debug.gba"), "rb").read()
            line = decode(rom[got["line"] - 0x08000000: got["line"] - 0x08000000 + 64])
        name = self.PAGES[page] if page < len(self.PAGES) else str(page)
        return name, line, (got["cell"] & 0xFF, (got["cell"] >> 8) & 0xFF)

    def summary_capture(self, what):
        page, line, cell = self.summary_state()
        cap = "%s: %s" % (what, page)
        if page == "FEELINGS":
            cap += " -- cell %d,%d -- %s" % (cell[0], cell[1], line)
            self.said.append(line)
        self.capture(cap, read_text=False)

    def summary_keys(self, keys):
        for key in keys:
            tw.run("hold %s 4" % key.upper(), "wait 60")
            self.summary_capture("after %s" % key.upper())

    def summary(self, slot, keys):
        if not self.free():
            raise RouteError("summary needs the player free on the overworld")
        S = lambda n: elf_symbol(n, self.release)
        self.start_menu(STARTMENU_POKEMON)
        tw.run("hold A 6", "wait 100")                                    # the party fades in
        at = S("gPartyMenu") + 9
        for _ in range(8):
            cur = tw.peek([(8, at, "s")])["s"]
            if cur == slot:
                break
            tw.run("hold %s 4" % ("DOWN" if cur < slot else "UP"), "wait 16")
        if tw.peek([(8, at, "s")])["s"] != slot:
            raise RouteError("the party menu's cursor did not reach slot %d" % slot)
        tw.run("hold A 6", "wait 30", "hold A 6", "wait 120")            # its actions; SUMMARY is the first
        self.summary_capture("slot %d's SUMMARY" % slot)
        self.summary_keys(keys)

    def boxsummary(self, keys):
        """From the box screen (MOVE DAEMON), its cursor on a daemon: A, SUMMARY (second in its menu), A."""
        tw.run("hold A 6", "wait 40", "hold DOWN 4", "wait 16", "hold A 6", "wait 140")
        self.summary_capture("the box daemon's SUMMARY")
        self.summary_keys(keys)

    def shown(self, checks):
        page, line, cell = self.summary_state()
        for c in checks:
            k, _, v = c.partition("=")
            if k == "page" and page != v.upper():
                raise RouteError("the summary is on %s, not %s" % (page, v.upper()))
            elif k == "line" and fold(line or "") != fold(v):
                raise RouteError('the fourth page says "%s", not "%s"' % (line, v))
            elif k == "cell" and cell != tuple(int(n) for n in v.split(",")):
                raise RouteError("the dot is in cell %d,%d, not %s" % (cell[0], cell[1], v))
            elif k not in ("page", "line", "cell"):
                raise RouteError("shown: no check %s" % c)

    def close(self):
        for _ in range(8):
            if self.free():
                return
            tw.run("hold B 6", "wait 70")
        if not self.free():
            raise RouteError("B did not bring the player back")

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
            m = tw.Map(folder, walking=True)
            m.on_foot = not self.g.state()["surfing"]
            best = tw.choose_warp(m, here, args[0])                         # the tile that fires (T-451)
            if not best:
                raise RouteError("%s has no warp to %s" % (folder, args[0]))
            tw.walk(self.g, (best["x"], best["y"]), into_warp=True)
        elif op == "edge":
            left = tw.remaining()
            try:
                subprocess.run([sys.executable, os.path.join(ROOT, "tools/theatre_walk.py"), "edge", args[0]]
                               + (["--release"] if self.release else [])
                               + (["--timeout", "%d" % max(1, left)] if left is not None else []),
                               check=True, timeout=None if left is None else max(1, left) + 15)
            except subprocess.TimeoutExpired:
                raise tw.TheatreTimeout("edge %s ran past the stop's limit" % args[0])
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
            self.mon(int(args[0]), args[1], const_species(v) if v.startswith("SPECIES_") else const_item(v) if v.startswith("ITEM_")
                     else -1 if v == "max" else -2 if v == "back" else int(v, 0))
        elif op == "bag":                                                   # T-433
            self.bag(const_item(args[0]), int(args[1]) if len(args) > 1 and args[1] != "first" else 1, "first" in args)
        elif op == "swap":                                                  # T-433
            self.swap(int(args[0]), int(args[1]))
        elif op == "open":                                                  # T-433: START -> BAG or DAEMON
            if not self.free():
                raise RouteError("open needs the player free on the overworld")
            self.start_menu({"BAG": 2, "DAEMON": 1}[args[0]])
            tw.run("hold A 6", "wait 100")
            self.capture("START: " + args[0], read_text=False)
        elif op == "useitem":                                               # T-433
            self.poke("gSpecialVar_ItemId", 16, const_item(args[0]))
            self.events(["FEELINGS >", "USE THE ITEM ON SLOT 1"])
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
        elif op == "palettes":                                              # T-431 P3
            self.palettes(args[0])
        elif op == "register":
            self.poke("*gSaveBlock1Ptr+0x296", 16, const_item(args[0]))
        elif op == "play":
            for note in args:
                self.note(note)
        elif op == "fight":
            tw.clear_battle(self.g)
        elif op == "win":
            self.win()
        elif op == "lose":                                                  # T-431: B_OUTCOME_LOST, the same way
            self.win(2)
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
        elif op == "debug":                                                 # T-458
            self.debug(args)
        elif op == "events":                                                # T-431
            self.events(args)
        elif op == "feelings":                                              # T-431
            self.feelings(args)
        elif op == "conditions":                                            # T-431
            self.conditions(int(args[0]), [int(v) for v in args[1:7]])
        elif op == "feel":                                                  # T-431 P2
            self.feel(args)
        elif op == "summary":                                               # T-431 P2
            self.summary(int(args[0]), args[1:])
        elif op == "boxsummary":
            self.boxsummary(args)
        elif op == "keys":
            self.summary_keys(args)
        elif op == "shown":
            self.shown(args)
        elif op == "close":
            self.close()
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
        failed, down = None, None
        seconds = stop.get("timeout") or self.stop_seconds
        with tw.limit(seconds, "stop %d" % no):
            for line in stop["steps"]:
                try:
                    self.step(line)
                except tw.TheatreDown as e:                              # nothing after this can work
                    failed = down = "%s -- %s" % (line, e)
                    break
                except (RouteError, SystemExit, subprocess.CalledProcessError, tw.TheatreError) as e:
                    failed = "%s -- %s" % (line, e)
                    break
        if failed and not down:
            try:
                self.capture("FAILED here")                              # outside the stop's limit: it may be spent
            except (Exception, SystemExit):
                pass
        sheet = os.path.join(self.out, "%02d - %s.png" % (no, re.sub(r"[^\w ,.'-]+", "", stop["stop"])[:60]))
        contact_sheet(sheet, stop["stop"], self.frames, failed)
        if down:
            raise tw.TheatreDown(down)
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
    bad, folder, states = [], None, {}
    for i, stop in enumerate(route["stops"], 1):
        for line in stop["steps"]:
            a = words(line)
            try:
                if a[0] == "savestate":                                   # a saved moment is where it was saved
                    states[a[1]] = folder
                elif a[0] == "loadstate":
                    folder = states.get(a[1])
                elif a[0] in ("load", "continue"):
                    folder = None                                         # wherever the save stands: not known here
                elif a[0] == "fly":                                       # GOTO lands in the town's own map
                    map_index(a[1])
                    folder = a[1]
                elif a[0] in ("goto", "expect"):
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
                elif a[0] == "debug":
                    entries = start_menu_entries()
                    for r in a[1:]:
                        if "STARTMENU_DBG_" + r.upper() not in entries:
                            raise RouteError("the DEBUG menu has no row %s" % r)
                elif a[0] == "events":
                    pages, _ = Runner.event_pages(None)
                    page = "PG_EVENTS"
                    for label in a[1:]:
                        if label.startswith("#"):
                            continue
                        hits = [r for r in pages[page] if r[0] and fold(r[0]) == fold(label)]
                        if len(hits) != 1:
                            raise RouteError("GAME EVENTS: no row %s on %s" % (label, page))
                        if hits[0][1] == "R_PAGE":
                            page = hits[0][2]
                elif a[0] == "mon" and a[2].startswith("SPECIES_"):
                    const_species(a[2])
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
    stop_seconds = None
    if "--stop-timeout" in args:
        k = args.index("--stop-timeout")
        stop_seconds = float(args[k + 1])
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
    try:
        tw.ping()                                       # seconds, not five minutes a stop, when nothing is listening
    except tw.TheatreDown as e:
        sys.exit("theatre_route: %s" % e)
    try:
        r = Runner(name, route.get("rom") == "release", check_build=not loads_first)
    except tw.TheatreError as e:
        sys.exit("theatre_route: %s" % e)
    r.stop_seconds = stop_seconds or route.get("stop_timeout") or STOP_SECONDS
    report = ["# %s" % name, "", route.get("about", ""), ""]
    failures, down = 0, None
    for i, stop in enumerate(route["stops"], 1):
        if i < start or (only and i not in only):
            continue
        if down:
            report += ["## %d. %s -- not played: the theatre stopped answering" % (i, stop["stop"]), ""]
            continue
        print("%2d. %s ..." % (i, stop["stop"]), end=" ", flush=True)
        try:
            failed, sheet, said = r.play(i, stop)
        except tw.TheatreDown as e:
            down = failed = str(e)
            sheet = os.path.join(r.out, "%02d - %s.png" % (i, re.sub(r"[^\w ,.'-]+", "", stop["stop"])[:60]))
            said = list(r.said)
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
    if down:
        print("theatre_route: the run stopped at the first batch the theatre did not answer: %s" % down, file=sys.stderr)
    sys.exit(failures)


if __name__ == "__main__":
    main()
