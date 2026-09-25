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

THE WALK IS A FLOOR, NOT A CEILING. It knows nothing of Surf, Cut, Strength, ledges or elevation, so vanilla
itself has about 240 things it calls unreachable. So the same walk runs on a pristine pret/pokefirered checkout
(a git worktree of upstream/master, cached in ~/.cache/daemons) and only the DIFFERENCE is reported: what is
unreachable here and was reachable there, or is new and unreachable. That list should be empty.
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


def main():
    up = upstream()
    rc = 0
    for k, lost in lost_values(text_blocks(GBA), text_blocks(up)):
        print("  !! %s no longer has %s" % (k, ", ".join("{%s}" % x for x in lost)))
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
    if not rc:
        print("  nothing we changed made anything unreachable, any door lead nowhere, any flag wait forever, or any line lose\n"
              "  a value or a sound vanilla had.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
