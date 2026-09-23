#!/usr/bin/env python3
"""The GROVES: hidden places entered through a tree (T-221; docs/school.md 8a).

    python3 tools/gbagrove.py            # report what each grove would add
    python3 tools/gbagrove.py --write    # layout, map, scripts, map group, includes, encounters, the tree

WHAT A GROVE IS, as built. A tree that is not part of any wall -- one standing apart in the open -- answers A: the
screen fades and you are somewhere the map never showed. A tree inside the grove takes you back. Nothing is said
either way. The player can find it blind, by pressing A on the tree that stands alone; REVEAL makes the tree twinkle
(src/reveal.c reads GROVES below from the same table this tool writes), so the driver shows which tree, and is
never the key.

HOW ONE IS MADE. A grove is a clearing LIFTED from its own forest's map: the rectangle is cut out of the parent
layout's map.bin with its collision, so it is drawn in the forest's own tiles and walks as the forest walks, and
the parent's border (trees) closes it in. It gets a map of its own, appended to its parent's map group so no map
number moves, and the parent's encounter table as a PLACEHOLDER -- the grove's resident family is the user's
choice (school.md 8a), and it replaces that table when chosen.

PROVISIONAL. Only one grove is built, to prove the mechanism: VIRIDIAN FOREST's lone tree. Where the fourteen go,
and who lives in them, are the user's; adding one is a new row in GROVES.
"""
import json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

GROVES = [
    dict(
        name="ViridianForest_Grove", parent="ViridianForest", parent_layout="LAYOUT_VIRIDIAN_FOREST",
        crop=(38, 39, 16, 17),                  # x, y, width, height out of the parent's map.bin
        enter_at=[(30, 57)],                    # the lone tree's trunk, read from (30,58) -- (28,57) hides an ANTIDOTE
        back_to=(30, 58),                       # where you stand again after leaving
        arrive=(4, 6),                          # inside the grove
        leave_at=[(7, 3), (8, 3), (9, 3)],      # the grove's own lone tree, read from below
    ),
]


def load(p):
    return json.load(open(os.path.join(GBA, p)))


def save_json(p, d):
    open(os.path.join(GBA, p), "w").write(json.dumps(d, indent=2) + "\n")


def const(name):
    return "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper().replace("__", "_")


def main():
    layouts = load("data/layouts/layouts.json")
    groups = load("data/maps/map_groups.json")
    wild = load("src/data/wild_encounters.json")
    events = open(os.path.join(GBA, "data/event_scripts.s")).read()
    changes = []
    for g in GROVES:
        name, parent = g["name"], g["parent"]
        mapc, lay_id = const(name), "LAYOUT_" + const(name)[4:]
        pl = next(l for l in layouts["layouts"] if l.get("id") == g["parent_layout"])
        W = pl["width"]
        raw = open(os.path.join(GBA, pl["blockdata_filepath"]), "rb").read()
        x0, y0, w, h = g["crop"]
        crop = b"".join(raw[((y0 + y) * W + x0) * 2:((y0 + y) * W + x0 + w) * 2] for y in range(h))
        ax, ay = g["arrive"]
        assert (struct.unpack_from("<H", crop, (ay * w + ax) * 2)[0] >> 10) & 3 == 0, "%s: the arrival cell is blocked" % name
        assert any((struct.unpack_from("<H", crop, ((ly + 1) * w + lx) * 2)[0] >> 10) & 3 == 0 for (lx, ly) in g["leave_at"]), \
            "%s: nobody can stand below the way out" % name

        ldir = "data/layouts/%s" % name
        entry = {"id": lay_id, "name": name + "_Layout", "width": w, "height": h,
                 "border_width": pl["border_width"], "border_height": pl["border_height"],
                 "primary_tileset": pl["primary_tileset"], "secondary_tileset": pl["secondary_tileset"],
                 "border_filepath": ldir + "/border.bin", "blockdata_filepath": ldir + "/map.bin"}
        have_layout = any(l.get("id") == lay_id for l in layouts["layouts"])
        pm = load("data/maps/%s/map.json" % parent)
        mdir = "data/maps/%s" % name
        mapjson = {
            "id": mapc, "name": name, "layout": lay_id, "music": pm["music"],
            "region_map_section": pm["region_map_section"], "requires_flash": False, "weather": pm["weather"],
            "map_type": pm["map_type"], "allow_cycling": pm["allow_cycling"], "allow_escaping": pm["allow_escaping"],
            "allow_running": pm["allow_running"], "show_map_name": False, "floor_number": 0,
            "battle_scene": pm["battle_scene"], "connections": None, "object_events": [], "warp_events": [],
            "coord_events": [],
            "bg_events": [{"type": "sign", "x": lx, "y": ly, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                           "script": "%s_EventScript_Leave" % name} for (lx, ly) in g["leave_at"]],
        }
        scripts = ("@ T-221: a grove -- PROVISIONAL, one built to prove the mechanism (tools/gbagrove.py writes this).\n"
                   "%s_MapScripts::\n\t.byte 0\n\n"
                   "@ The grove's own lone tree takes you back. Nothing is said.\n"
                   "%s_EventScript_Leave::\n\tlockall\n\tplayse SE_M_CUT\n\twarp %s, %d, %d\n\twaitstate\n\treleaseall\n\tend\n"
                   % (name, name, const(parent), g["back_to"][0], g["back_to"][1]))
        enter_label = "%s_EventScript_Grove" % parent
        enter = ("\n@ T-221: the tree that stands alone answers A -- the way into a grove. Nothing is said; REVEAL makes it\n"
                 "@ twinkle (src/reveal.c), and pressing A on the right tree finds it without.\n"
                 "%s::\n\tlockall\n\tplayse SE_M_CUT\n\twarp %s, %d, %d\n\twaitstate\n\treleaseall\n\tend\n"
                 % (enter_label, mapc, ax, ay))

        grp = next(k for k in groups["group_order"] if parent in groups[k])
        in_group = name in groups[grp]
        inc_s = '\t.include "data/maps/%s/scripts.inc"\n' % name
        inc_t = '\t.include "data/maps/%s/text.inc"\n' % name
        new_wild = []
        for wg in wild["wild_encounter_groups"]:
            for e in list(wg.get("encounters", [])):
                if e["map"] != const(parent):
                    continue
                label = e["base_label"].replace(parent.replace("_", ""), name.replace("_", ""), 1)
                if label != e["base_label"] and not any(x["base_label"] == label for x in wg["encounters"]):
                    ne = json.loads(json.dumps(e)); ne["map"] = mapc; ne["base_label"] = label
                    new_wild.append((wg, ne))
        pscripts = open(os.path.join(GBA, "data/maps/%s/scripts.inc" % parent)).read()
        pjson = pm
        enter_events = [b for b in pjson["bg_events"] if b.get("script") == enter_label]
        todo = []
        if not have_layout: todo.append("layout %dx%d cut from %s at (%d,%d)" % (w, h, parent, x0, y0))
        if not os.path.exists(os.path.join(GBA, mdir, "map.json")): todo.append("map %s" % mapc)
        if not in_group: todo.append("appended to %s" % grp)
        if inc_s not in events: todo.append("scripts included")
        if new_wild: todo.append("%d placeholder encounter tables (the parent's)" % len(new_wild))
        if enter_label not in pscripts: todo.append("the way in, in %s's scripts" % parent)
        if len(enter_events) != len(g["enter_at"]): todo.append("the tree's bg_event at %s" % g["enter_at"])
        print("  %s: %s" % (name, "; ".join(todo) if todo else "built, nothing to do"))
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
        for wg, ne in new_wild:
            wg["encounters"].append(ne)
        if enter_label not in pscripts:
            open(os.path.join(GBA, "data/maps/%s/scripts.inc" % parent), "a").write(enter)
        pjson["bg_events"] = [b for b in pjson["bg_events"] if b.get("script") != enter_label] + \
            [{"type": "sign", "x": ex, "y": ey, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
              "script": enter_label} for (ex, ey) in g["enter_at"]]
        save_json("data/maps/%s/map.json" % parent, pjson)
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
