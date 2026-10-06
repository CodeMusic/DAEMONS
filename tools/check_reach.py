#!/usr/bin/env python3
"""Can the player reach every person, sign and item we put in the world -- through doors that lead somewhere, past
flags something sets? (found 2026-09-25)

    python3 tools/check_reach.py          # report; exits 1 if anything we changed made something unreachable

WHY. Scorn was placed in the ROCKET WAREHOUSE on 2026-09-10 "five tiles from Ty and facing him" -- on the one
tile of the doorway into Ty's room. Nothing moves him, so for fifteen days the PAYLOAD, and with it CRYSTAL's
ending, could not be reached in play: the DEBUG kit and the JUMP page went round it, and a build, a lexicon check
and a fresh clone all passed. It was found by accident, placing a page on a wall behind another man standing in a
doorway (the CONDOMINIUMS 3F's Designer, who is vanilla's and seals off vanilla's own painting).

HOW. For every map: walk from where the player can arrive -- its warps, the warps scripts make into it, and its
edges if it joins another map -- through every tile whose collision is open, round every person who never
leaves (no flag the story can hide them by, and not a wanderer). Then every object with a script and every sign
or hidden item needs a reached tile beside it.

AND A WAY BACK (the user's playthrough, 2026-10-03: "I can't get out"). CALLOW SCHOOL rose over the lawn that was
the only way out of the strip below a ledge, and a ledge only lets a player down -- so whoever jumped it was shut in.
The walk above could not see it: it asks whether a cell can be REACHED, and that strip could. So a second walk knows
the four ledges (MB_JUMP_*: crossed in their own direction only, landing beyond), goes forward from every arrival
and back from every way out (the same warps and edges), and reports a cell that can be reached and not left -- a
trap -- when vanilla has no trap there.

THE WALK IS A FLOOR, NOT A CEILING. It knows nothing of Surf, Cut, Strength, ledges or elevation, so vanilla
itself has about 240 things it calls unreachable. So the same walk runs on a pristine pret/pokefirered checkout
(a git worktree of upstream/master, cached in ~/.cache/daemons) and only the DIFFERENCE is reported: what is
unreachable here and was reachable there, or is new and unreachable. That list should be empty.

AND WHO REPAINTS WHOM (T-365, the user, 2026-10-03: "before the owl was colourful now normal"). Two people on one map
whose palette tags share the special slot repaint each other: the slot is patched from each object's own tag as it
spawns, so whichever comes last colours the other (engine.md trap 17). The OWL and CALLOW's people did it in CALLOW
SCHOOL for eleven days -- a green and yellow OWL at the exam, brown children after it -- and every check passed. So
each map's special slot (and any slot a tag is patched into at spawn) is read here too, and a map where two tags
share one is reported unless vanilla shares it, or the two are never shown together (KNOWN_SHARED, with why).

AND WHO IS REGISTERED TWICE (T-369, trap 17's three-line check, run every time). A palette tag registered in two
slots is the bug in its general form -- whichever map shows both, one repaints the other. Every graphics info is grouped
by its tag and the slots it names are collected; a tag in two slots that vanilla does not split is reported, except the
two the engine means: the player's own forms, and the daemons' type tags, which are patched per map at spawn and kept
apart there by gbaowslots.py (REGISTERED_SPLIT, with why).

AND A NAME PRINTED BEFORE IT IS LOOKED UP (T-377, engine.md trap 43). VERA said "/235 settles." -- her line printed
{STR_VAR_1} after the party screen had drawn an HP into it and before anything put the daemon's name there. Every script
is walked along its flow for a message printing a buffer that a screen or battle overwrote and nothing refilled; VERA's
old line is planted each run, and the check fails if it stops finding it.
"""
import json, os, re, struct, subprocess, sys
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
CACHE = os.path.expanduser("~/.cache/daemons/pokefirered-upstream")


def upstream():
    """A checkout of upstream/master beside the engine, made once and moved to upstream/master each run."""
    if not os.path.exists(os.path.join(CACHE, "Makefile")):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        subprocess.run(["git", "-C", GBA, "worktree", "add", "--detach", CACHE, "upstream/master"],
                       check=True, capture_output=True)
    else:
        subprocess.run(["git", "-C", CACHE, "checkout", "--detach", "-q", "upstream/master"], check=True)
    return CACHE


def audit(root):
    """{(map, kind, x, y): what} -- everything the walk cannot stand beside."""
    load = lambda p: json.load(open(os.path.join(root, p)))
    layouts = {l["id"]: l for l in load("data/layouts/layouts.json")["layouts"] if l}
    seeds = {}
    for dp, _, fs in os.walk(os.path.join(root, "data")):
        for f in fs:
            if f.endswith(".inc"):
                for m in re.finditer(r"^\s*warp\w*\s+(MAP_\w+),\s*(?:\d+,\s*)?(-?\d+),\s*(-?\d+)",
                                     open(os.path.join(dp, f), errors="ignore").read(), re.M):
                    seeds.setdefault(m.group(1), set()).add((int(m.group(2)), int(m.group(3))))
    out = {}
    for d in sorted(os.listdir(os.path.join(root, "data/maps"))):
        path = os.path.join(root, "data/maps", d, "map.json")
        if not os.path.exists(path):
            continue
        m = json.load(open(path))
        lay = layouts.get(m.get("layout"))
        if not lay or not lay.get("blockdata_filepath"):
            continue
        W, H = lay["width"], lay["height"]
        bd = open(os.path.join(root, lay["blockdata_filepath"]), "rb").read()
        blocked = lambda x, y: (struct.unpack_from("<H", bd, (y * W + x) * 2)[0] >> 10) & 3
        objs = m.get("object_events") or []
        still = {(o["x"], o["y"]) for o in objs
                 if str(o.get("flag", "0")) == "0" and "WANDER" not in str(o.get("movement_type", ""))}
        start = {(w["x"], w["y"]) for w in m.get("warp_events") or []} | seeds.get(m["id"], set())
        if m.get("connections"):
            start |= {(x, 0) for x in range(W)} | {(x, H - 1) for x in range(W)}
            start |= {(0, y) for y in range(H)} | {(W - 1, y) for y in range(H)}
        seen = {s for s in start if 0 <= s[0] < W and 0 <= s[1] < H and not blocked(*s) and s not in still}
        todo = deque(seen)
        while todo:
            cx, cy = todo.popleft()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and not blocked(nx, ny) \
                        and (nx, ny) not in still:
                    seen.add((nx, ny))
                    todo.append((nx, ny))
        near = lambda x, y: (x, y) in seen or any(n in seen for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
        for o in objs:
            if o.get("script") not in (None, "", "0", "0x0") and not near(o["x"], o["y"]):
                out[(d, "person", o["x"], o["y"])] = o["script"]
        for b in m.get("bg_events") or []:
            if not near(b["x"], b["y"]):
                out[(d, "sign" if b.get("type") != "hidden_item" else "hidden item", b["x"], b["y"])] = \
                    b.get("script") or b.get("item")
    return out


JUMP = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}      # MB_JUMP_EAST, WEST, NORTH, SOUTH


def _tdir(root, symbol, kind):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    base = os.path.join(root, "data/tilesets", kind)
    for d in os.listdir(base):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(base, d)


def traps(root):
    """{(map, x, y)} -- open cells the player can walk to from an arrival and cannot walk back from to any way out,
    with ledges one way. Arrivals and ways out are the same set: the warps, the warps scripts make, and the edges."""
    load = lambda p: json.load(open(os.path.join(root, p)))
    layouts = {l["id"]: l for l in load("data/layouts/layouts.json")["layouts"] if l}
    attrs = {}
    def behaviour(lay, mt):
        key = (lay["primary_tileset"], lay["secondary_tileset"])
        if key not in attrs:
            pa = open(os.path.join(_tdir(root, key[0], "primary"), "metatile_attributes.bin"), "rb").read()
            sd = _tdir(root, key[1], "secondary")
            sa = open(os.path.join(sd, "metatile_attributes.bin"), "rb").read() if sd else b""
            attrs[key] = (pa, sa)
        pa, sa = attrs[key]
        a, k = (pa, mt) if mt < 640 else (sa, mt - 640)
        return struct.unpack_from("<I", a, k * 4)[0] & 0x1FF if (k + 1) * 4 <= len(a) else 0
    seeds = {}
    for dp, _, fs in os.walk(os.path.join(root, "data")):
        for f in fs:
            if f.endswith(".inc"):
                for m in re.finditer(r"^\s*warp\w*\s+(MAP_\w+),\s*(?:\d+,\s*)?(-?\d+),\s*(-?\d+)",
                                     open(os.path.join(dp, f), errors="ignore").read(), re.M):
                    seeds.setdefault(m.group(1), set()).add((int(m.group(2)), int(m.group(3))))
    out = set()
    for d in sorted(os.listdir(os.path.join(root, "data/maps"))):
        path = os.path.join(root, "data/maps", d, "map.json")
        if not os.path.exists(path):
            continue
        m = json.load(open(path))
        lay = layouts.get(m.get("layout"))
        if not lay or not lay.get("blockdata_filepath") or not lay.get("primary_tileset"):
            continue
        W, H = lay["width"], lay["height"]
        bd = open(os.path.join(root, lay["blockdata_filepath"]), "rb").read()
        cell = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
        still = {(o["x"], o["y"]) for o in m.get("object_events") or []
                 if str(o.get("flag", "0")) == "0" and "WANDER" not in str(o.get("movement_type", ""))}
        inside = lambda x, y: 0 <= x < W and 0 <= y < H
        ledge = {}
        for y in range(H):
            for x in range(W):
                b = behaviour(lay, cell(x, y) & 0x3FF)
                if b in JUMP:
                    ledge[(x, y)] = JUMP[b]
        open_ = lambda x, y: inside(x, y) and not (cell(x, y) >> 10) & 3 and (x, y) not in still \
            and (x, y) not in ledge
        def steps(x, y):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if (nx, ny) in ledge:
                    if ledge[(nx, ny)] == (dx, dy) and open_(nx + dx, ny + dy):
                        yield nx + dx, ny + dy
                elif open_(nx, ny):
                    yield nx, ny
        ends = {(w["x"], w["y"]) for w in m.get("warp_events") or []} | seeds.get(m["id"], set())
        if m.get("connections"):
            ends |= {(x, 0) for x in range(W)} | {(x, H - 1) for x in range(W)}
            ends |= {(0, y) for y in range(H)} | {(W - 1, y) for y in range(H)}
        ends = {e for e in ends if open_(*e)}
        fwd, back = set(ends), set(ends)
        todo = deque(ends)
        edges = {}
        while todo:
            c = todo.popleft()
            for n in steps(*c):
                edges.setdefault(n, set()).add(c)
                if n not in fwd:
                    fwd.add(n)
                    todo.append(n)
        for c in list(fwd):                                             # every reached cell's ways forward, reversed
            for n in steps(*c):
                edges.setdefault(n, set()).add(c)
        todo = deque(ends)
        while todo:
            c = todo.popleft()
            for p in edges.get(c, ()):
                if p not in back:
                    back.add(p)
                    todo.append(p)
        out |= {(d, x, y) for (x, y) in fwd - back}
    return out


def doors(root):
    """Every warp that leads nowhere, to a warp its map does not have, or somewhere that does not lead back."""
    maps = {}
    for d in os.listdir(os.path.join(root, "data/maps")):
        p = os.path.join(root, "data/maps", d, "map.json")
        if os.path.exists(p):
            m = json.load(open(p))
            maps[m["id"]] = (d, m)
    out = set()
    for mid, (d, m) in maps.items():
        for i, w in enumerate(m.get("warp_events") or []):
            dm, dw = w["dest_map"], str(w["dest_warp_id"])
            if dm in ("MAP_DYNAMIC", "MAP_UNDEFINED") or dw in ("127", "WARP_ID_DYNAMIC", "0x7F"):
                continue
            if dm not in maps:
                out.add((d, i, "leads to no map " + dm))
                continue
            there = maps[dm][1].get("warp_events") or []
            k = int(dw, 0) if re.match(r"^(0x)?\d+$", dw) else -1
            if not 0 <= k < len(there):
                out.add((d, i, "%s has no warp %s" % (maps[dm][0], dw)))
            elif there[k]["dest_map"] not in (mid, "MAP_DYNAMIC"):
                out.add((d, i, "one way: %s#%d leads on to %s" % (maps[dm][0], k, there[k]["dest_map"])))
    return out


#  Flags the story waits on that nothing outside the DEBUG build sets -- each one a ticket, or a bug.
KNOWN_UNSET = {"FLAG_ARTSAI_PAGE": "T-235: the Five Witnesses' reward waits on the TRANSCRIPT's words",
               "FLAG_COMPANION_LINKED": "T-370: set by the companion app's first SYNC, outside the game (companion C-21)"}


def unset_flags(root):
    """Flags a script or the C tests and nothing in normal play ever sets. The DEBUG kit and JUMP are left out on
    purpose: they are what hid T-284 for fifteen days."""
    reads, sets = set(), set()
    for dp, _, fs in os.walk(os.path.join(root, "data")):
        for f in fs:
            if f.endswith(".inc") and "debug" not in f.lower():
                t = re.sub(r"\.if\s+DAEMONS_DEBUG.*?\.endif", "", open(os.path.join(dp, f), errors="ignore").read(), flags=re.S)
                reads |= set(re.findall(r"^\s*(?:goto|call)_if_(?:un)?set\s+(FLAG_\w+)", t, re.M))
                reads |= set(re.findall(r"^\s*checkflag\s+(FLAG_\w+)", t, re.M))
                sets |= set(re.findall(r"^\s*setflag\s+(FLAG_\w+)", t, re.M))
    for dp, _, fs in os.walk(os.path.join(root, "src")):
        for f in fs:
            if f.endswith((".c", ".h")):
                t = re.sub(r"#if(?:def)?\s+DAEMONS_DEBUG.*?#endif", "", open(os.path.join(dp, f), errors="ignore").read(), flags=re.S)
                reads |= set(re.findall(r"FlagGet\((FLAG_\w+)\)", t))
                sets |= set(re.findall(r"FlagSet\((FLAG_\w+)\)", t))
    skip = ("FLAG_TEMP", "FLAG_HIDDEN_ITEM", "FLAG_DEFEATED", "FLAG_SYS_", "FLAG_BADGE", "FLAG_WORLD_MAP", "FLAG_ITEM_", "FLAG_TRAINER")
    return {f for f in reads - sets if not f.startswith(skip)}


def text_blocks(root):
    """{label: its strings joined}, for every text label in data/."""
    out = {}
    for dp, _, fs in os.walk(os.path.join(root, "data")):
        for f in fs:
            if f.endswith(".inc"):
                cur = None
                for line in open(os.path.join(dp, f), errors="ignore"):
                    m = re.match(r"^(\w+)::", line)
                    if m:
                        cur = m.group(1)
                        out.setdefault(cur, "")
                        continue
                    m = re.match(r'^\s*\.string\s+"(.*)"', line)
                    if m and cur:
                        out[cur] += m.group(1)
                    elif line.strip() and not line.strip().startswith("@"):
                        cur = None
    return out


#  What a line FILLS IN (a name from a buffer, a count) and what it PLAYS (a leader's music, a mark's fanfare). A
#  rewrite may drop the player's or rival's name on purpose; it may not drop a value the game computes, or the sound.
KEPT = re.compile(r"\{(STR_VAR_\d|B_BUFF\d|MUS_\w+|SE_\w+)\}")


def lost_values(ours, theirs):
    """Lines that print a value or play a sound in vanilla and no longer do -- the INDEX rating said "DAEMON seen
    DAEMON owned" with no numbers for three weeks (port_dialogue.py dropped Gen 1's text_decimal; 2026-09-25)."""
    out = []
    for k, v in theirs.items():
        if k in ours and v:
            want, have = KEPT.findall(v), KEPT.findall(ours[k])
            lost = sorted({x for x in want if want.count(x) > have.count(x)})
            if lost:
                out.append((k, lost))
    return sorted(out)


#  A LINE THAT ANNOUNCES WHAT THE SCRIPT ANNOUNCES. Gen 1 put "<PLAYER> got #DEX from OAK!" inside the speaker's own
#  text; Gen 3's script prints the receipt itself, with its fanfare. Carried across, four lines said it twice -- the
#  CC-7 three times in a row (found playing CONTEXT from a new game, 2026-09-25).
RECEIPT = re.compile(r"\{PLAYER\}\s*(?:got|received|obtained)\b", re.I)


def doubled_receipts(ours, theirs):
    return sorted(k for k, v in ours.items() if k in theirs and len(RECEIPT.findall(v)) > len(RECEIPT.findall(theirs[k])))


KNOWN_SHARED = {("BirthIsland_Exterior", "PALSLOT_NPC_SPECIAL"):
                "CRYSTAL stands only until she reads the PAYLOAD, and the meteorite is hidden until she has"}


# T-369: tags the engine registers in more than one slot on purpose, and why.
REGISTERED_SPLIT = {
    "OBJ_EVENT_PAL_TAG_PLAYER_RED": "the player's own forms (vanilla splits it too)",
}
SPLIT_PREFIXES = {
    "OBJ_EVENT_PAL_TAG_DAEMON_TYPE": "a daemon's type palette, patched into a slot free on its map at spawn (gbaowslots.py)",
}


def registration_splits(root):
    """{tag: slots} for every palette tag the graphics infos register in more than one slot (engine.md trap 17)."""
    text = open(os.path.join(root, "src/data/object_events/object_event_graphics_info.h")).read()
    slots = {}
    for body in re.findall(r"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_\w+ = \{(.*?)\};", text, re.S):
        tag, slot = re.search(r"\.paletteTag = (\w+)", body), re.search(r"\.paletteSlot = (\w+)", body)
        if tag and slot and tag.group(1) != "OBJ_EVENT_PAL_TAG_NONE":
            slots.setdefault(tag.group(1), set()).add(slot.group(1))
    return {t: tuple(sorted(s)) for t, s in slots.items() if len(s) > 1}


def palette_clashes(root):
    """{(map, slot): tags} for every map where two palette tags would be patched into one slot."""
    E = lambda p: open(os.path.join(root, p)).read()
    ptr = dict(re.findall(r"\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&(gObjectEventGraphicsInfo_\w+)",
                          E("src/data/object_events/object_event_graphics_info_pointers.h")))
    info = {}
    for name, body in re.findall(r"const struct ObjectEventGraphicsInfo (gObjectEventGraphicsInfo_\w+) = \{(.*?)\};",
                                 E("src/data/object_events/object_event_graphics_info.h"), re.S):
        tag, slot = re.search(r"\.paletteTag = (\w+)", body), re.search(r"\.paletteSlot = (\w+)", body)
        if tag and slot:
            info[name] = (tag.group(1), slot.group(1))
    patched = lambda tag: tag.startswith("OBJ_EVENT_PAL_TAG_DAEMON_TYPE") or tag == "OBJ_EVENT_PAL_TAG_NPC_OWL"
    out = {}
    maps = os.path.join(root, "data/maps")
    for m in sorted(os.listdir(maps)):
        try:
            j = json.load(open(os.path.join(maps, m, "map.json")))
        except (OSError, ValueError):
            continue
        slots = {}
        for o in j.get("object_events") or []:
            t = info.get(ptr.get(o.get("graphics_id", "")))
            if t and t[0] != "OBJ_EVENT_PAL_TAG_NONE":
                slots.setdefault(t[1], set()).add(t[0])
        for slot, tags in slots.items():
            if len(tags) > 1 and (slot == "PALSLOT_NPC_SPECIAL" or any(patched(t) for t in tags)):
                out[(m, slot)] = tuple(sorted(tags))
    return out


#  A NAME PRINTED BEFORE IT IS LOOKED UP (T-377, from T-376). The three string buffers are shared by everything: the
#  party screen draws each daemon's level and HP through gStringVar1 and 2, a battle prints through them all. VERA said
#  "/235 settles." because her line used {STR_VAR_1} after ChoosePartyMon and before BufferMonNickname filled it --
#  the party screen's last HP was still there. So every script is walked along its flow (gotos, branches and calls
#  followed), tracking which buffers something has OVERWRITTEN and nothing has refilled since; a message that prints
#  one of those is reported. A buffer never filled at all is not reported -- a caller may have filled it.
CLOBBERS = {   # specials that open a screen or a battle, which writes the buffers for its own drawing
    "ChoosePartyMon", "ChooseHalfPartyForBattle", "ChooseSendDaycareMon", "ChooseMonForMoveRelearner",
    "ChooseMonForMoveTutor", "SelectMoveTutorMon", "SelectMoveDeleterMove", "ShowPokemonStorageSystemPC",
    "ChooseMonForWirelessMinigame", "DoChooseMonForBattleTower",
}
CLOBBER_CMDS = re.compile(r"^(trainerbattle\w*|dowildbattle|dofirstbattle|pokemart\w*)\b")


def _special_fills(root):
    """{special: the buffers it names} -- in its own body or two calls down (the size contests fill them in a
    helper), so a special that names gStringVarN fills it."""
    names = set(re.findall(r"def_special (\w+)", open(os.path.join(root, "data/specials.inc")).read()))
    bodies = {}
    for dp, _, fs in os.walk(os.path.join(root, "src")):
        for f in fs:
            if f.endswith(".c"):
                text = open(os.path.join(dp, f), errors="ignore").read()
                for m in re.finditer(r"^\w[\w\s\*]*?\b(\w+)\([^;{)]*\)\s*\n\{", text, re.M):
                    end = text.find("\n}\n", m.end())
                    bodies.setdefault(m.group(1), text[m.end():end])
    def named(fn, depth):
        b = bodies.get(fn, "")
        got = set(re.findall(r"gStringVar([123])", b))
        if depth:
            for callee in set(re.findall(r"\b(\w+)\(", b)) & set(bodies):
                if callee != fn:
                    got |= named(callee, depth - 1)
        return got
    return {n: named(n, 2) for n in names if n not in CLOBBERS}


def stale_buffers(root):
    """{(script label, text label, STR_VAR_n)} for a message that prints a buffer something overwrote and nothing refilled."""
    body, order = {}, []
    for dp, _, fs in os.walk(os.path.join(root, "data")):
        for f in sorted(fs):
            if not f.endswith(".inc") or f == "text.inc":
                continue
            cur, seq = None, []
            for line in open(os.path.join(dp, f), errors="ignore"):
                line = line.split("@")[0].strip()
                m = re.match(r"^(\w+)::?$", line)
                if m:
                    if cur is not None:
                        seq.append(("label", m.group(1)))
                    cur = m.group(1)
                    body.setdefault(cur, None)
                    order.append(cur)
                    seq.append(("start", cur))
                elif line and cur:
                    seq.append(("cmd", line))
            # each label's commands, falling through into the next label until something ends the flow
            starts = [i for i, (k, _) in enumerate(seq) if k == "start"]
            for i in starts:
                cmds = []
                for k, v in seq[i + 1:]:
                    if k == "cmd":
                        cmds.append(v)
                    elif k == "label":
                        cmds.append("goto " + v)
                        break
                    else:
                        break
                body[seq[i][1]] = cmds
    texts = text_blocks(root)
    fills = _special_fills(root)
    found, seen = set(), set()

    def walk(label, stale, depth=0):
        key = (label, stale)
        if key in seen or depth > 40 or not body.get(label):
            return stale
        seen.add(key)
        for cmd in body[label]:
            op, _, rest = cmd.partition(" ")
            args = [a.strip() for a in rest.split(",")]
            if op.startswith("buffer") and args and args[0].startswith("STR_VAR_"):
                stale = stale - {args[0][-1]}
            elif op in ("special", "specialvar"):
                sp = args[-1]
                if sp in CLOBBERS:
                    stale = stale | {"1", "2", "3"}
                else:
                    stale = stale - fills.get(sp, set())
            elif CLOBBER_CMDS.match(op):
                stale = stale | {"1", "2", "3"}
            elif op in ("msgbox", "message") and args[0] in texts:
                for n in re.findall(r"\{STR_VAR_([123])\}", texts[args[0]]):
                    if n in stale:
                        found.add((label, args[0], "STR_VAR_" + n))
            elif op == "goto":
                walk(args[0], stale, depth + 1)
                return stale
            elif op.startswith("goto_if") or op.startswith("call"):
                target = args[-1]
                if target in body:
                    walk(target, stale, depth + 1)
            elif op in ("end", "return", "releaseall_end"):
                return stale
        return stale

    for label in order:
        walk(label, frozenset())
    stale_buffers.examined = (len(order), sum(1 for cmds in body.values() if cmds
                                               for c in cmds if c.split(" ")[0] in ("msgbox", "message")))
    return found


def _stale_buffers_fires():
    """The check proves it still fires: VERA's line before T-376, planted, must be found (trap 18)."""
    global text_blocks
    real = text_blocks
    def planted(root):
        t = real(root)
        t["PalletTown_RivalsHouse_Text_LookingNiceInNoTime"] = "{STR_VAR_1} settles.$"
        return t
    text_blocks = planted
    try:
        return ("PalletTown_RivalsHouse_EventScript_GroomMon", "PalletTown_RivalsHouse_Text_LookingNiceInNoTime",
                "STR_VAR_1") in stale_buffers(GBA)
    finally:
        text_blocks = real


def main():
    up = upstream()
    rc = 0
    ours_text, theirs_text = text_blocks(GBA), text_blocks(up)
    for k, lost in lost_values(ours_text, theirs_text):
        print("  !! %s no longer has %s" % (k, ", ".join("{%s}" % x for x in lost)))
        rc = 1
    for k in doubled_receipts(ours_text, theirs_text):
        print("  !! %s announces a receipt vanilla's script prints itself -- the player reads it twice" % k)
        rc = 1
    ours, theirs = audit(GBA), audit(up)
    worse = sorted(set(ours) - set(theirs))
    print("  %d things the walk cannot reach here, %d in vanilla (Surf, Cut, ledges -- it knows none of them)"
          % (len(ours), len(theirs)))
    if worse:
        print("  !! unreachable here and not in vanilla:")
        for k in worse:
            print("     %-36s %-11s (%d,%d)  %s" % (k[0], k[1], k[2], k[3], ours[k]))
        rc = 1
    t_ours, t_theirs = traps(GBA), traps(up)
    worse = sorted(t_ours - t_theirs)
    print("  %d cells a player can reach and not leave here, %d in vanilla" % (len(t_ours), len(t_theirs)))
    if worse:
        print("  !! a way in and no way out, and vanilla had one:")
        for k in worse:
            print("     %-36s (%d,%d)" % k)
        rc = 1
    d_ours, d_theirs = doors(GBA), doors(up)
    worse = sorted(d_ours - d_theirs)
    print("  %d odd doors here, %d in vanilla" % (len(d_ours), len(d_theirs)))
    for w in worse:
        print("  !! %s warp %d: %s" % w)
        rc = 1
    f_ours, f_theirs = unset_flags(GBA), unset_flags(up)
    worse = sorted(f_ours - f_theirs)
    for f in worse:
        if f in KNOWN_UNSET:
            print("  known: %s is tested and never set -- %s" % (f, KNOWN_UNSET[f]))
        else:
            print("  !! %s is tested and nothing outside the DEBUG build sets it" % f)
            rc = 1
    p_ours, p_theirs = palette_clashes(GBA), palette_clashes(up)
    for k in sorted(set(p_ours) - set(p_theirs)):
        if k in KNOWN_SHARED:
            print("  known: %s shares %s between %s -- %s" % (k[0], k[1], ", ".join(p_ours[k]), KNOWN_SHARED[k]))
        else:
            print("  !! %s: %s share %s, so whichever spawns last repaints the other (trap 17)"
                  % (k[0], " and ".join(p_ours[k]), k[1]))
            rc = 1
    r_ours, r_theirs = registration_splits(GBA), registration_splits(up)
    examined = len(re.findall(r"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_",
                              open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")).read()))
    print("  %d graphics infos read for their palette registration (trap 17)" % examined)   # trap 18: what was examined
    for tag in sorted(r_ours):
        why = REGISTERED_SPLIT.get(tag) or next((w for pre, w in SPLIT_PREFIXES.items() if tag.startswith(pre)), None)
        if tag in r_theirs or why:
            continue
        print("  !! %s is registered in %s -- a map showing both repaints one with the other (trap 17)"
              % (tag, " and ".join(r_ours[tag])))
        rc = 1
    if not _stale_buffers_fires():
        print("  !! the name-before-lookup check no longer finds VERA's planted line -- it has stopped working (T-377)")
        rc = 1
    s_ours = stale_buffers(GBA)
    print("  %d scripts walked, %d messages read for a name printed before it is looked up (T-377)"
          % stale_buffers.examined)                                                    # trap 18: what was examined
    s_theirs = stale_buffers(up)
    for k in sorted(s_ours - s_theirs):
        print("  !! %s prints {%s} in %s after something overwrote it and before anything refilled it (T-377)"
              % (k[0], k[2], k[1]))
        rc = 1
    if not rc:
        print("  nothing we changed made anything unreachable, any pocket a trap, any door lead nowhere, any flag wait\n"
              "  forever, any line lose a value or a sound vanilla had, any receipt get announced twice,\n"
              "  any name get printed before it is looked up,\n"
              "  or anyone repaint anyone, or any palette registered twice.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
