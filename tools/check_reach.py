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
KNOWN_UNSET = {"FLAG_ARTSAI_PAGE": "T-235: the Five Witnesses' reward waits on the TRANSCRIPT's words"}


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
    if not rc:
        print("  nothing we changed made anything unreachable, any pocket a trap, any door lead nowhere, any flag wait\n"
              "  forever, any line lose a value or a sound vanilla had, any receipt get announced twice,\n"
              "  or anyone repaint anyone.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
