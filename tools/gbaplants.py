#!/usr/bin/env python3
"""Artificial flowers: CORPUS's plastic plants, and the CHECKPOINTS' real ones (T-381; bible 0.7).

    python3 tools/gbaplants.py            # report what would change
    python3 tools/gbaplants.py --write    # the plants' bg_events in every map, and data/scripts/plants.inc

The user, 2026-10-06, approved 2026-10-11: CORPUS's offices are full of plastic plants with a cheerful sign not to
water them, the finest in SCORN's office; the CHECKPOINTS keep real ones. Comedy as cover (craft rule 6): nobody says
what a plastic plant stands for.

WHERE. Every potted plant in FOUNDRY CO. (SilphCo_1F..11F) is found by its pot -- metatile 0x355 (a plant on the
floor) or 0x356 (against a wall), gTileset_SilphCo's -- and given a sign that reads from any side. SCORN's two on 11F,
by the couch in his office, read differently. Every CHECKPOINT on the shared layout has one plant, by the shelf at
(1,1), read from the floor below; UMBRA PLATEAU's three are down its west room's wall; ONE ISLAND's has none.

The words are the user's approved drafts (field-test page, d-t381-plants).
"""
import glob, json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
POTS = (0x355, 0x356)
SCORN = ("SilphCo_11F", {(7, 8), (11, 8)})
CHECKPOINT_LAYOUT, CHECKPOINT_PLANT = "LAYOUT_POKEMON_CENTER_1F", (1, 1)
#  UMBRA PLATEAU's CHECKPOINT is drawn on its own tileset: three tall plants down the wall of its west room, read from
#  the floor to their left.
INDIGO = ("IndigoPlateau_PokemonCenter_1F", [(8, 4), (8, 6), (8, 8)])
SCRIPTS = ("EventScript_PlasticPlant", "EventScript_ScornsPlant", "EventScript_RealPlant")

INC = """@ T-381 (the user, 2026-10-06, approved 2026-10-11; bible 0.7): ARTIFICIAL FLOWERS. tools/gbaplants.py writes this
@ file and places the signs. CORPUS's plants are plastic; the CHECKPOINTS' are real. Nobody says what either means.
EventScript_PlasticPlant::
	msgbox Text_PlasticPlant, MSGBOX_SIGN
	end

EventScript_ScornsPlant::
	msgbox Text_ScornsPlant, MSGBOX_SIGN
	end

EventScript_RealPlant::
	msgbox Text_RealPlant, MSGBOX_SIGN
	end

Text_PlasticPlant::
	.string "A tag on the pot says:\\n"
	.string "PLEASE DO NOT WATER ME!$"

Text_ScornsPlant::
	.string "The finest plant in the\\n"
	.string "building. It has never\\p"
	.string "dropped a leaf.\\n"
	.string "It has never grown one, either.$"

Text_RealPlant::
	.string "The soil is still damp.\\n"
	.string "A new leaf is coming in.$"
"""


def load(p):
    return json.load(open(os.path.join(GBA, p)))


def sign(x, y, script, facing):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def main():
    layouts = {l["id"]: l for l in load("data/layouts/layouts.json")["layouts"] if "id" in l}
    todo = {}
    count = {s: 0 for s in SCRIPTS}
    folders = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(GBA, "data/maps/*/map.json")))
    for folder in folders:
        mp = "data/maps/%s/map.json" % folder
        m = load(mp)
        want = []
        if re.fullmatch(r"SilphCo_\d+F", folder):
            l = layouts[m["layout"]]
            raw = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            W, H = l["width"], l["height"]
            for y in range(H):
                for x in range(W):
                    if struct.unpack_from("<H", raw, (y * W + x) * 2)[0] & 0x3FF in POTS:
                        scorn = folder == SCORN[0] and (x, y) in SCORN[1]
                        want.append(sign(x, y, SCRIPTS[1] if scorn else SCRIPTS[0], "BG_EVENT_PLAYER_FACING_ANY"))
        elif m.get("layout") == CHECKPOINT_LAYOUT:
            want.append(sign(*CHECKPOINT_PLANT, SCRIPTS[2], "BG_EVENT_PLAYER_FACING_NORTH"))
        elif folder == INDIGO[0]:
            want += [sign(x, y, SCRIPTS[2], "BG_EVENT_PLAYER_FACING_EAST") for x, y in INDIGO[1]]
        #  a plant nobody can stand beside (a FOUNDRY corner; someone standing in front of PEWTER's) gets no sign
        if want:
            l = layouts[m["layout"]]
            raw = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
            W, H = l["width"], l["height"]
            people = {(o["x"], o["y"]) for o in m.get("object_events") or []}
            free = lambda x, y: 0 <= x < W and 0 <= y < H and (x, y) not in people and \
                not (struct.unpack_from("<H", raw, (y * W + x) * 2)[0] >> 10) & 3
            side = {"BG_EVENT_PLAYER_FACING_NORTH": [(0, 1)], "BG_EVENT_PLAYER_FACING_EAST": [(-1, 0)],
                    "BG_EVENT_PLAYER_FACING_ANY": [(0, 1), (0, -1), (1, 0), (-1, 0)]}
            #  ...and the floor beside it must be walkable to from the map's doors, not a closed pocket
            seen = [(wp["x"], wp["y"]) for wp in m.get("warp_events") or []]
            reach, stack = set(seen), list(seen)
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (x + dx, y + dy)
                    if n not in reach and free(*n):
                        reach.add(n)
                        stack.append(n)
            want = [w for w in want if any((w["x"] + dx, w["y"] + dy) in reach for dx, dy in side[w["player_facing_dir"]])]
        if not want and not any(b.get("script") in SCRIPTS for b in (m.get("bg_events") or [])):
            continue
        keep = [b for b in (m.get("bg_events") or []) if b.get("script") not in SCRIPTS]
        taken = {(b["x"], b["y"]) for b in keep}
        #  a pot that already holds something (SilphCo_10F's keeps vanilla's hidden HP UP) keeps it, and no sign
        for w in [w for w in want if (w["x"], w["y"]) in taken]:
            print("  %s (%d,%d): something is already there; it keeps it" % (folder, w["x"], w["y"]))
        want = [w for w in want if (w["x"], w["y"]) not in taken]
        for w in want:
            count[w["script"]] += 1
        new = keep + want
        if new != (m.get("bg_events") or []):
            m["bg_events"] = new
            todo[os.path.join(GBA, mp)] = json.dumps(m, indent=2) + "\n"
    inc = os.path.join(GBA, "data/scripts/plants.inc")
    if not os.path.exists(inc) or open(inc).read() != INC:
        todo[inc] = INC
    ev = open(os.path.join(GBA, "data/event_scripts.s")).read()
    line = '\t.include "data/scripts/plants.inc"   @ T-381, tools/gbaplants.py\n'
    if line not in ev:
        anchor = '\t.include "data/scripts/tower_stones.inc"   @ T-249\n'
        assert anchor in ev
        todo[os.path.join(GBA, "data/event_scripts.s")] = ev.replace(anchor, anchor + line, 1)
    print("  plastic plants %d, SCORN's %d, real plants %d" % tuple(count[s] for s in SCRIPTS))
    for p in sorted(todo):
        print("  %s %s" % ("wrote" if WRITE else "would write", os.path.relpath(p, GBA)))
    if not todo:
        print("  every plant is placed, nothing to do")
    if WRITE:
        for p, v in todo.items():
            open(p, "w").write(v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
