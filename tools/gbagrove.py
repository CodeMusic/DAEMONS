#!/usr/bin/env python3
"""The GROVES: hidden places entered through a tree (T-221; docs/school.md 8a).

    python3 tools/gbagrove.py            # report what each grove would add
    python3 tools/gbagrove.py --write    # layout, map, scripts, map group, includes, encounters, the tree

WHAT A GROVE IS, as built. A tree that is not part of any wall -- one standing apart in the open -- answers A: the
screen fades and you are somewhere the map never showed. A tree inside the grove takes you back. Nothing is said
either way. The player can find it blind, by pressing A on the tree that stands alone; REVEAL makes the tree twinkle
(src/reveal.c reads GROVES below from the same table this tool writes), so the driver shows which tree, and is
never the key.

FOURTEEN (the user, 2026-10-01: the table, the families and their names). Seven on the mainland, whose residents are
named in psychology's register, and one on each Sevii island, named in computing's: each world hides the other half.

HOW ONE IS MADE. Two ways:
  crop   THE UNDERTONE, the first: a clearing LIFTED from its own forest's map, with its collision.
  synth  the other thirteen: a clearing drawn in the general tileset's own trees and grass -- a ring of trees, tall
         grass where the residents live, and one tree standing alone in it, the way out. The general tileset is
         every outdoor map's primary, so a synthesised clearing looks like the route it hangs off.
The way IN is a tree that already stands alone (ROUTE 25's bush, FIVE ISLAND's meadow, SIX ISLAND's water path,
THREE ISLAND's berry forest, ROUTE 13's copse) or one PLANTED where the map has open ground: a 2x2 tree, or on a
cramped island a bush. Planting writes the parent's map.bin; check_reach proves no way was closed.

THE RESIDENTS. Each grove's encounter table is its family alone (FAMILY below), in both editions. Every one of them
is past the first 151, so -- FireRed's own rule -- its INDEX page shows and it evolves only once the GLOBAL INDEX is
held. That is the user's to keep or lift (T-221).
"""
import json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

#  The general tileset's own pieces (the primary every outdoor map shares). A tree is 2x2; which corner piece each
#  quarter takes depends on whether a tree stands beside or below it, as the routes draw them.
TREE_TOP = {(True, True): (0x01C, 0x01D), (False, True): (0x01E, 0x01D), (True, False): (0x01C, 0x01F),
            (False, False): (0x01E, 0x01F)}                                     # (tree left, tree right)
TREE_BOT_OVER_TREE = {(True, True): (0x014, 0x015), (False, True): (0x016, 0x015), (True, False): (0x014, 0x017),
                      (False, False): (0x016, 0x017)}
TREE_BOT_OVER_GROUND = {(True, True): (0x024, 0x025), (False, True): (0x026, 0x025), (True, False): (0x024, 0x027),
                        (False, False): (0x026, 0x027)}
LONE_TREE = (0x01E, 0x01F, 0x026, 0x027)                                        # top-left, top-right, bottom-left, -right
BUSH = 0x005
GRASS = ((0x008, 0x009), (0x010, 0x011))                                        # even rows, odd rows
TALL = 0x00D
COLLIDE = 0x0C00
ELEVATION = 0x3000                                                              # the routes' ground, elevation 3

#  The clearing, in 2x2 cells: T a tree, . grass, g tall grass, X the lone tree that leads out, a where you arrive.
CLEARING = [
    "TTTTTTTT",
    "T......T",
    "T..X...T",
    "Tgg..ggT",
    "Tgg.agg T".replace(" ", ""),
    "TTggggTT",
    "TTTTTTTT",
]

#  name, parent, how in, the way in (bg_events), where you stand after leaving, what lives there.
#    plant  ("tree", x, y) a 2x2 at (x,y)..(x+1,y+1), or ("bush", x, y); None where a tree already stands alone
GROVES = [
    dict(name="ViridianForest_Grove", parent="ViridianForest", parent_layout="LAYOUT_VIRIDIAN_FOREST",
         crop=(38, 39, 16, 17), enter_at=[(30, 57)], back_to=(30, 58), arrive=(4, 6),
         leave_at=[(7, 3), (8, 3), (9, 3)], family="KECLEON", levels=(6, 9)),
    dict(name="Route25_Grove", parent="Route25", synth=True, plant=None,
         enter_at=[(18, 5)], back_to=(18, 6), family="RALTS", levels=(12, 16)),
    dict(name="Route1_Grove", parent="Route1", synth=True, plant=("tree", 4, 7),
         enter_at=[(4, 8), (5, 8)], back_to=(4, 9), family="SPOINK", levels=(4, 7)),
    dict(name="Route24_Grove", parent="Route24", synth=True, plant=("tree", 6, 11),
         enter_at=[(6, 12), (7, 12)], back_to=(6, 13), family="MEDITITE", levels=(12, 16)),
    dict(name="Route8_Grove", parent="Route8", synth=True, plant=("tree", 63, 8),
         enter_at=[(63, 9), (64, 9)], back_to=(63, 10), family="DUSKULL", levels=(20, 24)),
    dict(name="Route11_Grove", parent="Route11", synth=True, plant=("tree", 55, 3),
         enter_at=[(55, 4), (56, 4)], back_to=(55, 5), family="SLAKOTH", levels=(14, 18)),
    dict(name="Route13_Grove", parent="Route13", synth=True, plant=None,
         enter_at=[(44, 10), (45, 10)], back_to=(44, 11), family="SHUPPET", levels=(24, 28)),
    dict(name="FiveIsland_Meadow_Grove", parent="FiveIsland_Meadow", synth=True, plant=None,
         enter_at=[(17, 14), (18, 14)], back_to=(17, 15), family="BELDUM", levels=(40, 44)),
    dict(name="SixIsland_WaterPath_Grove", parent="SixIsland_WaterPath", synth=True, plant=None,
         enter_at=[(21, 33), (22, 33)], back_to=(21, 34), family="NOSEPASS", levels=(42, 46)),
    dict(name="ThreeIsland_BerryForest_Grove", parent="ThreeIsland_BerryForest", synth=True, plant=None,
         enter_at=[(14, 9), (15, 9), (16, 9)], back_to=(15, 10), family="GULPIN", levels=(38, 42)),
    dict(name="OneIsland_Grove", parent="OneIsland", synth=True, plant=("bush", 16, 10),
         enter_at=[(16, 10)], back_to=(16, 11), family="WURMPLE", levels=(35, 39)),
    dict(name="TwoIsland_Grove", parent="TwoIsland", synth=True, plant=("tree", 35, 4),
         enter_at=[(35, 5), (36, 5)], back_to=(35, 6), family="CASTFORM", levels=(36, 40)),
    dict(name="FourIsland_Grove", parent="FourIsland", synth=True, plant=("tree", 10, 16),
         enter_at=[(10, 17), (11, 17)], back_to=(10, 18), family="NINCADA", levels=(40, 44)),
    dict(name="SevenIsland_Grove", parent="SevenIsland", synth=True, plant=("bush", 3, 10),
         enter_at=[(3, 10)], back_to=(3, 11), family="BALTOY", levels=(44, 48)),
]

#  Who lives in each grove: (species, share of the twelve slots, levels above the grove's floor). A family's later
#  forms live there too where they are old enough to, so a player without the GLOBAL INDEX can still meet them.
FAMILY = {
    "KECLEON":  [("SPECIES_KECLEON", 12, 0)],
    "RALTS":    [("SPECIES_RALTS", 10, 0), ("SPECIES_KIRLIA", 2, 6)],
    "SPOINK":   [("SPECIES_SPOINK", 12, 0)],
    "MEDITITE": [("SPECIES_MEDITITE", 12, 0)],
    "DUSKULL":  [("SPECIES_DUSKULL", 12, 0)],
    "SLAKOTH":  [("SPECIES_SLAKOTH", 9, 0), ("SPECIES_VIGOROTH", 3, 4)],
    "SHUPPET":  [("SPECIES_SHUPPET", 12, 0)],
    "BELDUM":   [("SPECIES_BELDUM", 7, 0), ("SPECIES_METANG", 5, 0)],
    "NOSEPASS": [("SPECIES_NOSEPASS", 12, 0)],
    "GULPIN":   [("SPECIES_GULPIN", 7, 0), ("SPECIES_SWALOT", 5, 0)],
    "WURMPLE":  [("SPECIES_WURMPLE", 4, 0), ("SPECIES_SILCOON", 2, 0), ("SPECIES_CASCOON", 2, 0),
                 ("SPECIES_BEAUTIFLY", 2, 0), ("SPECIES_DUSTOX", 2, 0)],
    "CASTFORM": [("SPECIES_CASTFORM", 12, 0)],
    "NINCADA":  [("SPECIES_NINCADA", 7, 0), ("SPECIES_NINJASK", 5, 0)],
    "BALTOY":   [("SPECIES_BALTOY", 7, 0), ("SPECIES_CLAYDOL", 5, 0)],
}
RATE = 20


def load(p):
    return json.load(open(os.path.join(GBA, p)))


def save_json(p, d):
    open(os.path.join(GBA, p), "w").write(json.dumps(d, indent=2) + "\n")


def const(name):
    return "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper().replace("__", "_")


def synth_clearing():
    """The clearing's map.bin, the cell of the tree that leads out, and where you arrive."""
    rows = [r.ljust(8, "T") for r in CLEARING]
    ch, cw = len(rows), len(rows[0])
    W, H = cw * 2, ch * 2
    tree = lambda c, r: not (0 <= c < cw and 0 <= r < ch) or rows[r][c] in "TX"
    grid = [[0] * W for _ in range(H)]
    out = arrive = None
    for r in range(ch):
        for c in range(cw):
            k = rows[r][c]
            x, y = 2 * c, 2 * r
            if k == "X":
                tl, tr, bl, br = LONE_TREE
                out = (x, y)
                for (dx, dy), m in zip(((0, 0), (1, 0), (0, 1), (1, 1)), (tl, tr, bl, br)):
                    grid[y + dy][x + dx] = m | COLLIDE | ELEVATION
            elif k == "T":
                lr = (tree(c - 1, r) and rows[r][c - 1] != "X" if c > 0 else True,
                      tree(c + 1, r) and rows[r][c + 1] != "X" if c + 1 < cw else True)
                below = tree(c, r + 1) and (r + 1 >= ch or rows[r + 1][c] != "X")
                top = TREE_TOP[lr]
                bot = (TREE_BOT_OVER_TREE if below else TREE_BOT_OVER_GROUND)[lr]
                for dx in (0, 1):
                    grid[y][x + dx] = top[dx] | COLLIDE | ELEVATION
                    grid[y + 1][x + dx] = bot[dx] | COLLIDE | ELEVATION
            else:
                for dy in (0, 1):
                    for dx in (0, 1):
                        m = TALL if k == "g" else GRASS[(y + dy) % 2][(x + dx) % 2]
                        grid[y + dy][x + dx] = m | ELEVATION
                if k == "a":
                    arrive = (x, y)
    raw = b"".join(struct.pack("<H", v) for row in grid for v in row)
    return raw, W, H, out, arrive


def plant(parent_layout, how):
    """The parent's map.bin with a tree or a bush planted; None if it already stands there."""
    path = os.path.join(GBA, parent_layout["blockdata_filepath"])
    raw = bytearray(open(path, "rb").read())
    W = parent_layout["width"]
    kind, x, y = how
    cells = [((x, y), BUSH)] if kind == "bush" else \
        [((x + dx, y + dy), m) for (dx, dy), m in zip(((0, 0), (1, 0), (0, 1), (1, 1)), LONE_TREE)]
    changed = False
    for (cx, cy), m in cells:
        old = struct.unpack_from("<H", raw, (cy * W + cx) * 2)[0]
        new = (old & 0xF000) | COLLIDE | m
        if old != new:
            assert not (old >> 10) & 3 or (old & 0x3FF) == m, "%s: (%d,%d) is not open ground" % (path, cx, cy)
            struct.pack_into("<H", raw, (cy * W + cx) * 2, new)
            changed = True
    return (path, bytes(raw)) if changed else None


def family_table(g, label):
    lo, hi = g["levels"]
    mons = []
    for species, share, up in FAMILY[g["family"]]:
        for k in range(share):
            mn = lo + up + (k % 3)
            mons.append({"min_level": mn, "max_level": min(mn + 1, hi + up), "species": species})
    assert len(mons) == 12, g["name"]
    return {"map": const(g["name"]), "base_label": label, "land_mons": {"encounter_rate": RATE, "mons": mons}}


def main():
    layouts = load("data/layouts/layouts.json")
    groups = load("data/maps/map_groups.json")
    wild = load("src/data/wild_encounters.json")
    events = open(os.path.join(GBA, "data/event_scripts.s")).read()
    changes = []
    planted = []
    for g in GROVES:
        name, parent = g["name"], g["parent"]
        mapc, lay_id = const(name), "LAYOUT_" + const(name)[4:]
        pm = load("data/maps/%s/map.json" % parent)
        pl = next(l for l in layouts["layouts"] if l.get("id") == g.get("parent_layout", pm["layout"]))
        W = pl["width"]
        if g.get("synth"):
            crop, w, h, (ox, oy), arrive = synth_clearing()
            leave_at = [(ox, oy + 1), (ox + 1, oy + 1)]
        else:
            raw = open(os.path.join(GBA, pl["blockdata_filepath"]), "rb").read()
            x0, y0, w, h = g["crop"]
            crop = b"".join(raw[((y0 + y) * W + x0) * 2:((y0 + y) * W + x0 + w) * 2] for y in range(h))
            arrive, leave_at = g["arrive"], g["leave_at"]
        ax, ay = arrive
        assert (struct.unpack_from("<H", crop, (ay * w + ax) * 2)[0] >> 10) & 3 == 0, "%s: the arrival cell is blocked" % name
        assert any((struct.unpack_from("<H", crop, ((ly + 1) * w + lx) * 2)[0] >> 10) & 3 == 0 for (lx, ly) in leave_at), \
            "%s: nobody can stand below the way out" % name
        if g.get("plant"):
            p = plant(pl, g["plant"])
            if p:
                planted.append(p)
        #  the tree stands where the player will press A, and the player can stand below it
        praw = dict(planted).get(os.path.join(GBA, pl["blockdata_filepath"])) or \
            open(os.path.join(GBA, pl["blockdata_filepath"]), "rb").read()
        bx, by = g["back_to"]
        assert not (struct.unpack_from("<H", praw, (by * W + bx) * 2)[0] >> 10) & 3, "%s: back_to is blocked" % name
        if g.get("plant"):
            for ex, ey in g["enter_at"]:
                assert (struct.unpack_from("<H", praw, (ey * W + ex) * 2)[0] >> 10) & 3, "%s: (%d,%d) is no tree" % (name, ex, ey)

        ldir = "data/layouts/%s" % name
        entry = {"id": lay_id, "name": name + "_Layout", "width": w, "height": h,
                 "border_width": pl["border_width"], "border_height": pl["border_height"],
                 "primary_tileset": pl["primary_tileset"], "secondary_tileset": pl["secondary_tileset"],
                 "border_filepath": ldir + "/border.bin", "blockdata_filepath": ldir + "/map.bin"}
        have_layout = any(l.get("id") == lay_id for l in layouts["layouts"])
        mdir = "data/maps/%s" % name
        mapjson = {
            "id": mapc, "name": name, "layout": lay_id, "music": pm["music"],
            "region_map_section": pm["region_map_section"], "requires_flash": False, "weather": pm["weather"],
            "map_type": pm["map_type"], "allow_cycling": pm["allow_cycling"], "allow_escaping": pm["allow_escaping"],
            "allow_running": pm["allow_running"], "show_map_name": False, "floor_number": 0,
            "battle_scene": pm["battle_scene"], "connections": None, "object_events": [], "warp_events": [],
            "coord_events": [],
            "bg_events": [{"type": "sign", "x": lx, "y": ly, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                           "script": "%s_EventScript_Leave" % name} for (lx, ly) in leave_at],
        }
        scripts = ("@ T-221: a grove (tools/gbagrove.py writes this).\n"
                   "%s_MapScripts::\n\t.byte 0\n\n"
                   "@ The grove's own lone tree takes you back. Nothing is said.\n"
                   "%s_EventScript_Leave::\n\tlockall\n\tplayse SE_M_CUT\n\twarp %s, %d, %d\n\twaitstate\n\treleaseall\n\tend\n"
                   % (name, name, const(parent), bx, by))
        enter_label = "%s_EventScript_Grove" % parent
        enter = ("\n@ T-221: the tree that stands alone answers A -- the way into a grove. Nothing is said; REVEAL makes it\n"
                 "@ twinkle (src/reveal.c), and pressing A on the right tree finds it without.\n"
                 "%s::\n\tlockall\n\tplayse SE_M_CUT\n\twarp %s, %d, %d\n\twaitstate\n\treleaseall\n\tend\n"
                 % (enter_label, mapc, ax, ay))

        grp = next(k for k in groups["group_order"] if parent in groups[k])
        in_group = name in groups[grp]
        inc_s = '\t.include "data/maps/%s/scripts.inc"\n' % name
        inc_t = '\t.include "data/maps/%s/text.inc"\n' % name
        #  the residents: the family, in both editions, in place of any placeholder
        wg = next(x for x in wild["wild_encounter_groups"] if x.get("label") == "gWildMonHeaders")
        tables = [family_table(g, "s%s_%s" % (name.replace("_", ""), ed)) for ed in ("FireRed", "LeafGreen")]
        have = [e for e in wg["encounters"] if e["map"] == mapc]
        same = sorted(json.dumps(e, sort_keys=True) for e in have) == sorted(json.dumps(e, sort_keys=True) for e in tables)
        pscripts = open(os.path.join(GBA, "data/maps/%s/scripts.inc" % parent)).read()
        enter_events = [b for b in pm["bg_events"] if b.get("script") == enter_label]
        layout_now = open(os.path.join(GBA, ldir, "map.bin"), "rb").read() if os.path.exists(os.path.join(GBA, ldir, "map.bin")) else None
        mapjson_now = load(mdir + "/map.json") if os.path.exists(os.path.join(GBA, mdir, "map.json")) else None
        if mapjson_now:                         # another tool's events in a grove stay (gbadocs puts a page in one)
            for k in ("object_events", "warp_events", "coord_events", "bg_events"):
                mapjson[k] = mapjson[k] + [e for e in mapjson_now.get(k) or []
                                           if e.get("script") != "%s_EventScript_Leave" % name and e not in mapjson[k]]
        todo = []
        if not have_layout: todo.append("layout %dx%d %s" % (w, h, "drawn" if g.get("synth") else "cut from %s" % parent))
        elif layout_now != crop: todo.append("the clearing redrawn")
        if mapjson_now != mapjson: todo.append("map %s" % mapc)
        if not in_group: todo.append("appended to %s" % grp)
        if inc_s not in events: todo.append("scripts included")
        if not same: todo.append("its residents (%s)" % g["family"])
        if enter_label not in pscripts: todo.append("the way in, in %s's scripts" % parent)
        if len(enter_events) != len(g["enter_at"]): todo.append("the tree's bg_event at %s" % g["enter_at"])
        if g.get("plant") and any(p[0].endswith(pl["blockdata_filepath"]) for p in planted):
            todo.append("a %s planted at %s" % (g["plant"][0], g["plant"][1:]))
        print("  %-30s %s" % (name, "; ".join(todo) if todo else "built, nothing to do"))
        changes += todo
        if not WRITE or not todo:
            continue
        os.makedirs(os.path.join(GBA, ldir), exist_ok=True)
        open(os.path.join(GBA, ldir, "map.bin"), "wb").write(crop)
        open(os.path.join(GBA, ldir, "border.bin"), "wb").write(open(os.path.join(GBA, pl["border_filepath"]), "rb").read())
        if not have_layout:
            layouts["layouts"].append(entry)
        os.makedirs(os.path.join(GBA, mdir), exist_ok=True)
        save_json(mdir + "/map.json", mapjson)
        open(os.path.join(GBA, mdir, "scripts.inc"), "w").write(scripts)
        if not os.path.exists(os.path.join(GBA, mdir, "text.inc")):
            open(os.path.join(GBA, mdir, "text.inc"), "w").write("")
        if not in_group:
            groups[grp].append(name)
        if inc_s not in events:
            events = events.replace('\t.include "data/maps/%s/scripts.inc"\n' % parent,
                                    '\t.include "data/maps/%s/scripts.inc"\n' % parent + inc_s, 1)
            events = events.replace('\t.include "data/maps/%s/text.inc"\n' % parent,
                                    '\t.include "data/maps/%s/text.inc"\n' % parent + inc_t, 1)
        if not same:
            wg["encounters"] = [e for e in wg["encounters"] if e["map"] != mapc] + tables
        if enter_label not in pscripts:
            open(os.path.join(GBA, "data/maps/%s/scripts.inc" % parent), "a").write(enter)
        pm["bg_events"] = [b for b in pm["bg_events"] if b.get("script") != enter_label] + \
            [{"type": "sign", "x": ex, "y": ey, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
              "script": enter_label} for (ex, ey) in g["enter_at"]]
        save_json("data/maps/%s/map.json" % parent, pm)
    if WRITE:
        for path, raw in planted:
            open(path, "wb").write(raw)
    # The trees REVEAL marks: every grove's way in and way out, written as a header src/reveal.c includes, so a new
    # row here needs no edit in C.
    hdr = ["// GENERATED by tools/gbagrove.py -- do not edit by hand.",
           "//",
           "// T-221: the trees that lead into a GROVE and out of one. src/reveal.c twinkles a bg_event whose script is",
           "// one of these, as it does a hidden item.",
           "#ifndef GUARD_DATA_GROVE_TREES_H",
           "#define GUARD_DATA_GROVE_TREES_H",
           ""]
    names = []
    for g in GROVES:
        names += ["%s_EventScript_Grove" % g["parent"], "%s_EventScript_Leave" % g["name"]]
    hdr += ["extern const u8 %s[];" % n for n in names]
    hdr += ["", "static const u8 *const sGroveTrees[] =", "{"] + ["    %s," % n for n in names] + \
           ["};", "", "#endif // GUARD_DATA_GROVE_TREES_H", ""]
    htext = "\n".join(hdr)
    hpath = os.path.join(GBA, "src/data/grove_trees.h")
    hold = open(hpath).read() if os.path.exists(hpath) else None
    print("  src/data/grove_trees.h: %s" % ("unchanged" if hold == htext else "written" if WRITE else "would change"))
    if WRITE and hold != htext:
        open(hpath, "w").write(htext)
    if WRITE and changes:
        save_json("data/layouts/layouts.json", layouts)
        save_json("data/maps/map_groups.json", groups)
        save_json("src/data/wild_encounters.json", wild)
        open(os.path.join(GBA, "data/event_scripts.s"), "w").write(events)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
