#!/usr/bin/env python3
"""BREATHVERSE: the islet where CONTEXT's FLUTE lies (T-417; the user, 2026-10-18; the name DRAFT).

    python3 tools/gbabreathverse.py            # report what would change
    python3 tools/gbabreathverse.py --write    # the layout, the map, its group and includes, ROUTE 2's palm

WHAT IT IS. A small grove of its own -- not one of the fourteen (no daemons, no fir, no door into THE NEXUS), its own
universe, a psychology one: breath. The way in is a lone PALM on ROUTE 2, just north of CALLOW: press A on it and you
are on the islet, as a grove's lone tree takes you into its grove (findable blind; REVEAL twinkles it, because
tools/gbagrove.py lists both palms among the trees src/reveal.c marks). On the islet the player arrives beside its
palm, which is the way home, back to ROUTE 2's. Beside the palm lies the FLUTE (tools/genflute.py), CONTEXT only: the
grove opens in both editions, and in CONTENT the islet simply has no FLUTE (the simplest reading, DRAFT).

THE MAP. An islet of sand (the general tileset's own 3x3 sand-in-water pieces, as FINDERS BEACH draws its point) in
open water to the edge of the screen; out of view, a ring of sea rocks (the general set's two 2x2 rocks, alternated),
so a player who SURFs off it later meets rocks, not the map's edge. The GBA shows 15x10 cells, the player 7 from each
side and 4 from the top, 5 from the bottom, and a scroll uncovers one more: the islet is placed so that from every
cell of it the rocks stay one cell beyond that (check_view() refuses otherwise). Primary gTileset_General with FINDERS
BEACH's secondary, gTileset_SeviiIslands123; no connections, so nothing is drawn from a neighbour (engine.md trap 14).

WHAT IS HAND-WRITTEN, not here: data/maps/Breathverse/scripts.inc and text.inc (the arrival, the FLUTE, the way home),
and ROUTE 2's palm script in data/maps/Route2/scripts.inc. This tool writes the map's bytes and its events.
"""
import json, os, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

NAME, MAPC, LAYOUT = "Breathverse", "MAP_BREATHVERSE", "LAYOUT_BREATHVERSE"
PARENT = "Route2"
W, H = 28, 24
ISLET = (11, 10, 6, 4)                                   # x, y, width, height: sand, its edges in the water
RING = (1, 1, 26, 22)                                    # the rocks' rectangle, two cells thick, in 2x2 rocks
PALM = (13, 11)                                          # the way home; the player arrives one below, facing it
ARRIVE = (13, 12)
FLUTE = (14, 11)                                         # beside the palm, CONTEXT only
#  ROUTE 2: the palm in the grass strip east of the road, five cells north of CALLOW. Nothing passes through (12,75)
#  that cannot go round it by (13,75) -- check_reach is the proof. Back from the islet, one below it.
ROUTE2_PALM = (12, 75)
ROUTE2_BACK = (12, 76)

MUSIC = "MUS_GROVE_INWARD"          # INWARD's band leads with a FLUTE (tools/gengrovemusic.py); shared, never written over
WATER = 0x12B | 0x1000              # ocean, elevation 1 -- FINDERS BEACH's own values
SAND = {"tl": 0x10C, "t": 0x10D, "tr": 0x10E, "l": 0x114, "c": 0x115, "r": 0x116, "bl": 0x11C, "b": 0x11D, "br": 0x11E}
SAND_BITS = 0x3000                  # elevation 3
ROCKS = [(0x110, 0x111, 0x118, 0x119), (0x1CB, 0x1CC, 0x1D3, 0x1D4)]
ROCK_BITS = 0x0400                  # collision
BORDER = 0x012B
SCREEN_LEFT, SCREEN_RIGHT, SCREEN_UP, SCREEN_DOWN = 7, 7, 4, 5


def path(*p):
    return os.path.join(GBA, *p)


def load(p):
    return json.load(open(path(p)))


def save_json(p, d):
    open(path(p), "w").write(json.dumps(d, indent=2) + "\n")


def draw():
    grid = [[WATER] * W for _ in range(H)]
    rx, ry, rw, rh = RING
    cells = [(x, ry) for x in range(rx, rx + rw, 2)] + [(x, ry + rh - 2) for x in range(rx, rx + rw, 2)] + \
            [(rx, y) for y in range(ry + 2, ry + rh - 2, 2)] + [(rx + rw - 2, y) for y in range(ry + 2, ry + rh - 2, 2)]
    for k, (x, y) in enumerate(cells):
        tl, tr, bl, br = ROCKS[k % 2]
        grid[y][x], grid[y][x + 1], grid[y + 1][x], grid[y + 1][x + 1] = [m | ROCK_BITS for m in (tl, tr, bl, br)]
    ix, iy, iw, ih = ISLET
    for y in range(iy, iy + ih):
        for x in range(ix, ix + iw):
            v = "t" if y == iy else "b" if y == iy + ih - 1 else ""
            h = "l" if x == ix else "r" if x == ix + iw - 1 else ""
            grid[y][x] = SAND[(v + h) or ("c" if not (v or h) else v or h)] | SAND_BITS
    return b"".join(struct.pack("<H", v) for row in grid for v in row)


def check_view():
    """From every cell of the islet, and one scroll further, the screen shows no rock and no edge of the map."""
    ix, iy, iw, ih = ISLET
    rx, ry, rw, rh = RING
    assert ix - SCREEN_LEFT - 1 > rx + 1 and ix + iw - 1 + SCREEN_RIGHT + 1 < rx + rw - 2, "a rock is in view across"
    assert iy - SCREEN_UP - 1 > ry + 1 and iy + ih - 1 + SCREEN_DOWN + 1 < ry + rh - 2, "a rock is in view up or down"
    for x, y in (PALM, ARRIVE, FLUTE):
        assert ix < x < ix + iw - 1 and iy < y < iy + ih - 1, "(%d,%d) is not on the islet's open sand" % (x, y)


def obj(gfx, xy, script, flag):
    return {"type": "object", "graphics_id": gfx, "x": xy[0], "y": xy[1], "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}


def sign(xy, script):
    #  the palm's own tile carries the same script as a sign, so REVEAL (which reads bg_events) twinkles it
    return {"type": "sign", "x": xy[0], "y": xy[1], "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": script}


def main():
    check_view()
    layouts = load("data/layouts/layouts.json")
    groups = load("data/maps/map_groups.json")
    events = open(path("data/event_scripts.s")).read()
    pm = load("data/maps/%s/map.json" % PARENT)
    pl = next(l for l in layouts["layouts"] if l.get("id") == pm["layout"])
    praw = open(path(pl["blockdata_filepath"]), "rb").read()
    for (x, y), what in ((ROUTE2_PALM, "the palm"), (ROUTE2_BACK, "the way back")):
        assert not (struct.unpack_from("<H", praw, (y * pl["width"] + x) * 2)[0] >> 10) & 3, \
            "ROUTE 2 (%d,%d), %s, is not open ground" % (x, y, what)

    raw = draw()
    border = struct.pack("<4H", *[BORDER] * 4)
    ldir = "data/layouts/%s" % NAME
    entry = {"id": LAYOUT, "name": NAME + "_Layout", "width": W, "height": H, "border_width": 2, "border_height": 2,
             "primary_tileset": "gTileset_General", "secondary_tileset": "gTileset_SeviiIslands123",
             "border_filepath": ldir + "/border.bin", "blockdata_filepath": ldir + "/map.bin"}
    mapjson = {
        "id": MAPC, "name": NAME, "layout": LAYOUT, "music": MUSIC,
        "region_map_section": pm["region_map_section"], "requires_flash": False, "weather": pm["weather"],
        "map_type": pm["map_type"], "allow_cycling": pm["allow_cycling"], "allow_escaping": pm["allow_escaping"],
        "allow_running": pm["allow_running"], "show_map_name": False, "floor_number": 0,
        "battle_scene": pm["battle_scene"], "connections": None,
        #  local ids: 1 the palm, 2 the FLUTE (its script removes it by VAR_LAST_TALKED, so order is not load-bearing)
        "object_events": [obj("OBJ_EVENT_GFX_BEACH_PALM", PALM, "%s_EventScript_Leave" % NAME, "0"),
                          obj("OBJ_EVENT_GFX_BREATH_FLUTE", FLUTE, "%s_EventScript_Flute" % NAME,
                              "FLAG_HIDE_BREATHVERSE_FLUTE")],
        "warp_events": [], "coord_events": [],
        "bg_events": [sign(PALM, "%s_EventScript_Leave" % NAME)],
    }
    enter = "%s_EventScript_Breathverse" % PARENT
    parent_obj = obj("OBJ_EVENT_GFX_BEACH_PALM", ROUTE2_PALM, enter, "0")
    parent_bg = sign(ROUTE2_PALM, enter)

    todo = []
    lpath = path(ldir, "map.bin")
    if not any(l.get("id") == LAYOUT for l in layouts["layouts"]):
        todo.append("layout %dx%d" % (W, H))
    elif next(l for l in layouts["layouts"] if l.get("id") == LAYOUT) != entry:
        todo.append("the layout's entry")
    if not os.path.exists(lpath) or open(lpath, "rb").read() != raw:
        todo.append("the islet drawn")
    if not os.path.exists(path(ldir, "border.bin")) or open(path(ldir, "border.bin"), "rb").read() != border:
        todo.append("the border")
    mpath = "data/maps/%s/map.json" % NAME
    if not os.path.exists(path(mpath)) or load(mpath) != mapjson:
        todo.append("map %s" % MAPC)
    grp = next(k for k in groups["group_order"] if PARENT in groups[k])
    if NAME not in groups[grp]:
        todo.append("appended to %s" % grp)
    inc_s = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    inc_t = '\t.include "data/maps/%s/text.inc"\n' % NAME
    if inc_s not in events or inc_t not in events:
        todo.append("scripts included")
    if parent_obj not in pm["object_events"]:
        todo.append("ROUTE 2's palm at %s" % (ROUTE2_PALM,))
    if parent_bg not in pm["bg_events"]:
        todo.append("ROUTE 2's palm's sign (REVEAL)")
    for f in ("scripts.inc", "text.inc"):
        if not os.path.exists(path("data/maps", NAME, f)):
            print("  !! data/maps/%s/%s is missing -- it is hand-written" % (NAME, f))
    if enter not in open(path("data/maps/%s/scripts.inc" % PARENT)).read():
        print("  !! %s is not in ROUTE 2's scripts -- it is hand-written" % enter)

    print("  %-30s %s" % (NAME, "; ".join(todo) if todo else "built, nothing to do"))
    if not WRITE or not todo:
        return 0
    os.makedirs(path(ldir), exist_ok=True)
    open(lpath, "wb").write(raw)
    open(path(ldir, "border.bin"), "wb").write(border)
    layouts["layouts"] = [l for l in layouts["layouts"] if l.get("id") != LAYOUT] + [entry]
    save_json("data/layouts/layouts.json", layouts)
    os.makedirs(path("data/maps", NAME), exist_ok=True)
    save_json(mpath, mapjson)
    if NAME not in groups[grp]:
        groups[grp].append(NAME)
        save_json("data/maps/map_groups.json", groups)
    if inc_s not in events:
        events = events.replace('\t.include "data/maps/%s/scripts.inc"\n' % PARENT,
                                '\t.include "data/maps/%s/scripts.inc"\n' % PARENT + inc_s, 1)
    if inc_t not in events:
        events = events.replace('\t.include "data/maps/%s/text.inc"\n' % PARENT,
                                '\t.include "data/maps/%s/text.inc"\n' % PARENT + inc_t, 1)
    open(path("data/event_scripts.s"), "w").write(events)
    if parent_obj not in pm["object_events"]:
        pm["object_events"].append(parent_obj)
    if parent_bg not in pm["bg_events"]:
        pm["bg_events"].append(parent_bg)
    save_json("data/maps/%s/map.json" % PARENT, pm)
    print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
