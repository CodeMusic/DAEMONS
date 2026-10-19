#!/usr/bin/env python3
"""T-334: the GLOBAL INDEX placement, built (approved by the user 2026-10-19: "build it as planned").

    python3 tools/gbaglobalindex.py            # report what it would write
    python3 tools/gbaglobalindex.py --write    # write it

tools/plan_global_index.py is the plan and stays a plan: it decides WHICH daemon goes to WHICH island table and in
which edition. This writes it, in two parts.

THE WILD SLOTS (src/data/wild_encounters.json). Every daemon the plan places (status "new") takes one slot of its
table in each edition it belongs to. A table has a fixed number of slots, so a slot is GIVEN, never added -- and
only a slot whose daemon is still met in that same table through another slot (a duplicate), so nothing anyone
could meet there before stops being met there. The first 151's duplicates go first, the busiest slot first; the
rod's old-rod slots are never taken (the first cast stays what it was); a daemon past 151 already met on the islands
keeps every slot it has (the plan's "already"). The level is the slot's own, raised to the level the daemon
evolves at, so a later form is never met below it. Every slot changed carries "t334_was", the slot as it stood,
which is what lets the plan read the ground it planned on and a second run change nothing. The groves' tables are
not touched (tools/gbagrove.py owns each grove's universe; the plan leaves them out).

A daemon placed must be READY -- name, art, INDEX in both editions, category, streaks (tools/gbashifts.py's own
readiness check). One that is not is LEFT_OUT, below, with why, and the report says so.

THE SIXTEEN FIXED ENCOUNTERS. The plan's FIXED rows are proposals, so this is the simplest reading of each, DRAFT:
a standing daemon on a map that already exists (objects appended to its map.json, never a new map or layout), one
script each in data/scripts/global_index.inc, and a battle with no new words in it -- the cry is the whole meeting.
Won, caught or fled, it is gone (its FLAG_HIDE_* is set by removeobject). Where it stands is DERIVED: the reachable
open floor tile farthest from every way in ("the deepest chamber", "the back room"), or for SEVAULT's top the
northernmost, never a tile whose loss would cut the map in two, never beside a door, a person or a sign.

    Seven have overworld art (RAIKOU ENTEI SUICUNE LUGIA HO-OH CELEBI DEOXYS) and are seen. The nine without it
    stand UNSEEN (MOVEMENT_TYPE_INVISIBLE): a player meets an invisible wall at the far end of a place and presses A.
    Their art is the user's call, and so is whether they stay unseen.
    LUGIA and HO-OH are vanilla's, at NAVEL ROCK; the ferry sails there once the GLOBAL INDEX is held (by hand, in
    VermilionCity/scripts.inc). DEOXYS is already at THE ANNEX. Neither is written here.
    The three beasts stand only once the GLOBAL INDEX is held, and the edition daemons only in their edition: both
    are FLAG_HIDE_* flags set on every map load by DaemonsGlobalIndexLegendFlags (src/event_data.c, by hand), and
    EnableNationalPokedex clears the beasts'. The roamer vanilla starts at CELIO is not touched.

Names, INDEX and streaks of the sixteen: readiness is checked for them too.
"""
import importlib.util, json, os, re, struct, sys
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
WILD = "src/data/wild_encounters.json"
SCRIPTS = "data/scripts/global_index.inc"
FLAGS = "include/constants/flags.h"
FLAG_BASE = 0x140                     # DAEMONS_FLAGS_START + 0x140 .. + 0x14F, this tool's block
BEGIN, END = "//  BEGIN gbaglobalindex", "//  END gbaglobalindex"

LEFT_OUT = {
    "SPECIES_BELLOSSOM": "GOLDSET's drawing carries no streak markers, so genstreaks gives it no streaks",
}

#  species -> (map dir, level, where in it, edition, art). where: "deep" = farthest from every way in; "top" = the
#  northernmost. edition: "both", "CONTENT" or "CONTEXT". LATIOS/LATIAS share one object.
FIXED = [
    ("SPECIES_ENTEI",     "OneIsland_KindleRoad",          50, "deep", "both",    "OBJ_EVENT_GFX_ENTEI"),
    ("SPECIES_RAIKOU",    "FiveIsland_Meadow",             50, "deep", "both",    "OBJ_EVENT_GFX_RAIKOU"),
    ("SPECIES_SUICUNE",   "SixIsland_WaterPath",           50, "deep", "both",    "OBJ_EVENT_GFX_SUICUNE"),
    ("SPECIES_CELEBI",    "ThreeIsland_BerryForest",       30, "deep", "both",    "OBJ_EVENT_GFX_CELEBI"),
    ("SPECIES_JIRACHI",   "FiveIsland_MemorialPillar",     30, "deep", "both",    None),
    ("SPECIES_REGIROCK",  "SevenIsland_SevaultCanyon",     40, "deep", "CONTENT", None),
    ("SPECIES_REGICE",    "FourIsland_IcefallCave_Back",   40, "deep", "both",    None),
    ("SPECIES_REGISTEEL", "MtEmber_RubyPath_B5F",          40, "deep", "both",    None),
    ("SPECIES_LATIOS",    "ThreeIsland_BondBridge",        40, "deep", "both",    None),   # LATIAS in CONTEXT
    ("SPECIES_GROUDON",   "MtEmber_RubyPath_B4F",          45, "deep", "CONTENT", None),
    ("SPECIES_KYOGRE",    "SixIsland_OutcastIsland",       45, "deep", "CONTEXT", None),
    ("SPECIES_RAYQUAZA",  "SevenIsland_SevaultCanyon",     70, "top",  "both",    None),
]
ALREADY = {"SPECIES_LUGIA": "NAVEL ROCK, the base (vanilla's; the ferry opens with the GLOBAL INDEX)",
           "SPECIES_HO_OH": "NAVEL ROCK, the summit (vanilla's), and THE NEXUS",
           "SPECIES_DEOXYS": "THE ANNEX (already)"}
UNSEEN_GFX = "OBJ_EVENT_GFX_ITEM_BALL"      # never drawn: MOVEMENT_TYPE_INVISIBLE
OPEN = {0x00, 0x08, 0x21}                    # MB_NORMAL, MB_CAVE, MB_SAND: floor a daemon can stand on
RATES = {}


def mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def label(sp):
    return "GlobalIndex_EventScript_" + "".join(w.capitalize() for w in sp[8:].split("_"))


def flag(sp):
    return "FLAG_HIDE_GLOBAL_" + sp[8:]


# ---- the wild slots -------------------------------------------------------------------------------------------------

def slot_in(mons, kind, rates, ed, met, num):
    """The slot this table can give, or None. A duplicate first -- the first 151's before a later daemon's, which
    keeps its best slot (the plan's "already") -- the busiest first, the super rod first; else a slot of the first
    151 whose daemon is met in more slots elsewhere in this edition than here. Never the old rod's, never one given."""
    count, keep = {}, {}
    for i, m in enumerate(mons):
        count[m["species"]] = count.get(m["species"], 0) + 1
        k = keep.get(m["species"])
        if k is None or rates[i] > rates[k]:
            keep[m["species"]] = i
    banned = {0, 1} if kind == "fishing_mons" else set()
    free = [i for i, m in enumerate(mons) if i not in banned and "t334_was" not in m]
    late = lambda i: num.get(mons[i]["species"], 0) > 151
    rod = (lambda i: i < 5) if kind == "fishing_mons" else (lambda i: False)
    dup = sorted((i for i in free if count[mons[i]["species"]] > 1 and keep[mons[i]["species"]] != i),
                 key=lambda i: (late(i), rod(i), -rates[i], i))
    if dup:
        return dup[0]
    rest = sorted((i for i in free if not late(i) and met.get((ed, mons[i]["species"]), 0) > count[mons[i]["species"]]),
                  key=lambda i: (-(met[(ed, mons[i]["species"])] - count[mons[i]["species"]]), -rates[i], i))
    return rest[0] if rest else None


def give_slots(plan_rows, wild, tables):
    """Returns (placements, problems, spills). Edits wild (the baseline) in place."""
    fields = {f["type"]: f for f in wild["wild_encounter_groups"][0]["fields"]}
    encs = wild["wild_encounter_groups"][0]["encounters"]
    day = {}
    for e in encs:
        if e["base_label"].endswith("_Night"):
            continue
        ed = "CONTENT" if "FireRed" in e["base_label"] else "CONTEXT" if "LeafGreen" in e["base_label"] else None
        if ed:
            day[(ed, e["map"])] = e
    num = {k: int(v) for k, v in re.findall(r"#define (SPECIES_\w+)\s+(\d+)", read("include/constants/species.h"))}
    #  {(edition, species): how many slots name it, every day and night table of that edition}
    met = {}
    for e in encs:
        ed = "CONTENT" if "FireRed" in e["base_label"] else "CONTEXT" if "LeafGreen" in e["base_label"] else None
        for k in fields:
            for m in (e.get(k) or {}).get("mons", []):
                met[(ed, m["species"])] = met.get((ed, m["species"]), 0) + 1
    placements, problems, spills = [], [], []
    for r in sorted(plan_rows, key=lambda r: r["num"]):
        if r["status"] != "new" or r["id"] in LEFT_OUT:
            continue
        kind = r["slot_kind"]
        rates = fields[kind]["encounter_rates"]
        home = next(t for t in tables if t["map"] == r["map"] and t["kind"] == kind)
        for ed in r["eds"]:
            #  the planned table first; if it has no slot to give, the plan's next one of the same habitat and kind
            #  (its own order: the stage's tier, then the nearer island) -- reported as a spill
            order = [r["map"]] + [t["map"] for t in sorted(
                (t for t in tables if t["ed"] == ed and t["kind"] == kind and t["habitat"] == home["habitat"]
                 and t["map"] != r["map"]),
                key=lambda t: (t["tier"] != home["tier"], abs(t["island"] - home["island"]), t["island"], t["map"]))]
            for mp in order:
                mons = (day.get((ed, mp)) or {}).get(kind, {}).get("mons")
                i = slot_in(mons, kind, rates, ed, met, num) if mons else None
                if i is not None:
                    break
            if i is None:
                problems.append("%s: no slot to give in any %s %s %s table" % (r["name"], ed, home["habitat"], kind))
                continue
            if mp != r["map"]:
                spills.append("%s (%s): %s was full, so %s" % (r["name"], ed, r["map"], mp))
            was = dict(mons[i])
            lo = max(was["min_level"], r["evo_lv"])
            hi = max(was["max_level"], lo)
            mons[i] = {"min_level": lo, "max_level": hi, "species": r["id"], "t334_was": was}
            met[(ed, was["species"])] -= 1
            placements.append((ed, mp, kind, i, r["id"], lo, hi, was["species"]))
    return placements, problems, spills


# ---- the fixed encounters -------------------------------------------------------------------------------------------

def floor_tile(mapdir, where, j, placed=()):
    """(x, y, elevation) for a daemon to stand on, by the rule in the docstring. placed: the tiles of this tool's
    daemons already decided on this map in this run, which stand like anyone else."""
    ows = mod("gbaowslots")
    lay = {l["id"]: l for l in json.loads(read("data/layouts/layouts.json"))["layouts"] if l}[j["layout"]]
    W, H = lay["width"], lay["height"]
    bd = open(os.path.join(GBA, lay["blockdata_filepath"]), "rb").read()
    cell = lambda x, y: struct.unpack_from("<H", bd, (y * W + x) * 2)[0]
    _, beh = ows.map_behaviour(j["layout"])
    mine = {(o["x"], o["y"]) for o in j.get("object_events") or [] if str(o.get("script", "")).startswith("GlobalIndex_")}
    objs = [o for o in j.get("object_events") or [] if (o["x"], o["y"]) not in mine]
    still = {(o["x"], o["y"]) for o in objs if "WANDER" not in str(o.get("movement_type", ""))} | set(placed)
    marks = list(placed) + [(o["x"], o["y"]) for o in objs] + [(w["x"], w["y"]) for w in j.get("warp_events") or []] \
        + [(b["x"], b["y"]) for b in j.get("bg_events") or []] + [(c["x"], c["y"]) for c in j.get("coord_events") or []]
    start = {(w["x"], w["y"]) for w in j.get("warp_events") or []}
    if j.get("connections"):
        start |= {(x, 0) for x in range(W)} | {(x, H - 1) for x in range(W)} | {(0, y) for y in range(H)} | {(W - 1, y) for y in range(H)}
    blocked = lambda x, y: (cell(x, y) >> 10) & 3 or (x, y) in still

    def walk(without=None):
        dist = {}
        q = deque()
        for s in start:
            if 0 <= s[0] < W and 0 <= s[1] < H and not blocked(*s) and s != without:
                dist[s] = 0
                q.append(s)
        while q:
            cx, cy = q.popleft()
            for n in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= n[0] < W and 0 <= n[1] < H and n not in dist and n != without and not blocked(*n):
                    dist[n] = dist[(cx, cy)] + 1
                    q.append(n)
        return dist

    dist = walk()
    ok = [t for t in dist if beh(*t) in OPEN and 1 <= cell(*t) >> 12 <= 14
          and all(abs(t[0] - m[0]) + abs(t[1] - m[1]) > 2 for m in marks)]
    if where == "top":
        ok.sort(key=lambda t: (t[1], -dist[t], t[0]))
    else:
        ok.sort(key=lambda t: (-dist[t], t[1], t[0]))
    for t in ok:
        if len(walk(without=t)) == len(dist) - 1:            # nothing behind it but itself
            return t[0], t[1], cell(*t) >> 12
    raise SystemExit("  !! %s: no floor tile a daemon can stand on" % mapdir)


def script_for(sp, level):
    lab = label(sp)
    if sp == "SPECIES_LATIOS":
        body = ("\t.ifdef FIRERED\n\tsetwildbattle SPECIES_LATIOS, %d\n\tsetvar VAR_0x8004, SPECIES_LATIOS\n\t.else\n"
                "\tsetwildbattle SPECIES_LATIAS, %d\n\tsetvar VAR_0x8004, SPECIES_LATIAS\n\t.endif\n" % (level, level))
        cry = "\tplaymoncry VAR_0x8004, CRY_MODE_ENCOUNTER\n"
    else:
        body = "\tsetwildbattle %s, %d\n\tsetvar VAR_0x8004, %s\n" % (sp, level, sp)
        cry = "\tplaymoncry %s, CRY_MODE_ENCOUNTER\n" % sp
    return ("%s::\n"
            "\tgoto_if_questlog EventScript_ReleaseEnd\n"
            "\tspecial QuestLog_CutRecording\n"
            "\tlock\n"
            "\tfaceplayer\n"
            "%s"
            "\twaitse\n"
            "%s"
            "\tdelay 40\n"
            "\twaitmoncry\n"
            "\tsetflag FLAG_SYS_SPECIAL_WILD_BATTLE\n"
            "\tspecial StartLegendaryBattle\n"
            "\twaitstate\n"
            "\tclearflag FLAG_SYS_SPECIAL_WILD_BATTLE\n"
            "\tgoto GlobalIndex_EventScript_After\n"
            "\tend\n\n") % (lab, body, cry)


def scripts_text(fixed):
    out = ["@ GENERATED by tools/gbaglobalindex.py -- T-334, the GLOBAL INDEX's fixed encounters (DRAFT). Edit the tool.\n"
           "@ Each stands where the tool derived (its map.json); the battle has no words of its own, only the cry.\n\n"
           "@ Won or caught: gone. Fled (or teleported away): gone, and the game says it fled, as vanilla's do.\n"
           "GlobalIndex_EventScript_After::\n"
           "\tspecialvar VAR_RESULT, GetBattleOutcome\n"
           "\tgoto_if_eq VAR_RESULT, B_OUTCOME_RAN, EventScript_MonFlewAway\n"
           "\tgoto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EventScript_MonFlewAway\n"
           "\tgoto EventScript_RemoveStaticMon\n"
           "\tend\n\n"]
    for sp, _, level, _, _, _ in fixed:
        out.append(script_for(sp, level))
    return "".join(out)


def flags_block(fixed):
    lines = [BEGIN + " -- T-334: each fixed encounter of the GLOBAL INDEX, once gone (removeobject sets it). The beasts'",
             "//  and the edition daemons' are also set on every map load while they may not stand (event_data.c,",
             "//  DaemonsGlobalIndexLegendFlags). Block + 0x140 .. + 0x14F is this tool's."]
    for k, (sp, *_rest) in enumerate(fixed):
        lines.append("#define %-36s (DAEMONS_FLAGS_START + 0x%03X)" % (flag(sp), FLAG_BASE + k))
    lines.append(END)
    return "\n".join(lines) + "\n"


def object_for(sp, x, y, elev, gfx):
    return {"type": "object", "graphics_id": gfx or UNSEEN_GFX, "x": x, "y": y, "elevation": elev,
            "movement_type": "MOVEMENT_TYPE_FACE_DOWN" if gfx else "MOVEMENT_TYPE_INVISIBLE",
            "movement_range_x": 1, "movement_range_y": 1, "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0", "script": label(sp), "flag": flag(sp)}


def main():
    plan = mod("plan_global_index")
    shifts = mod("gbashifts")
    rows, summary, tables, wild = plan.derive()
    todo = {}

    # readiness: every daemon this places, and the sixteen
    want = sorted({r["id"] for r in rows if r["status"] in ("new", "fixed")})
    ready = shifts.readiness(want)
    up_names = dict(re.findall(r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]*)"', shifts.upstream("src/data/text/species_names.h")))
    names = dict(re.findall(r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]*)"', read("src/data/text/species_names.h")))
    for sp in want:
        if names.get(sp) == up_names.get(sp):
            ready.setdefault(sp, []).append("name is vanilla's")
    unready = {sp: why for sp, why in ready.items() if why and sp not in LEFT_OUT}
    for sp, why in sorted(LEFT_OUT.items()):
        print("  left out: %s -- %s" % (sp, why))
    if unready:
        for sp, why in sorted(unready.items()):
            print("  !! %s is not ready: %s -- add it to LEFT_OUT or finish it" % (sp, "; ".join(why)))
        return 1

    # 1. the slots
    placements, problems, spills = give_slots(rows, wild, tables)
    for p in spills:
        print("  spill: " + p)
    for p in problems:
        print("  !! " + p)
    if problems:
        return 1
    by = {}
    for ed, mp, kind, i, sp, lo, hi, was in placements:
        isl = next(n for k, n in plan.ISLAND if k in mp)
        by.setdefault((isl, ed), set()).add(sp)
    print("  %d slots given to %d daemons (%d left out)" % (len(placements), len({p[4] for p in placements}), len(LEFT_OUT)))
    for isl in range(1, 8):
        print("    island %d: CONTENT %2d, CONTEXT %2d" % (isl, len(by.get((isl, "CONTENT"), ())), len(by.get((isl, "CONTEXT"), ()))))
    todo[WILD] = json.dumps(wild, indent=2) + "\n"

    # 2. the fixed encounters
    todo[SCRIPTS] = scripts_text(FIXED)
    fl = read(FLAGS)
    block = flags_block(FIXED)
    if BEGIN in fl:
        fl = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", lambda m: block, fl, count=1, flags=re.S)
    else:
        anchor = "\n#define DAEMONS_FLAGS_COUNT"
        assert fl.count(anchor) == 1
        fl = fl.replace(anchor, "\n" + block + anchor)
    todo[FLAGS] = fl
    es = read("data/event_scripts.s")
    inc = '\t.include "data/scripts/global_index.inc"   @ T-334, tools/gbaglobalindex.py\n'
    if inc not in es:
        anchor = '\t.include "data/scripts/static_pokemon.inc"\n'
        assert es.count(anchor) == 1
        es = es.replace(anchor, anchor + inc)
    todo["data/event_scripts.s"] = es
    placed_here = {}
    for sp, mapdir, level, where, ed, gfx in FIXED:
        rel = "data/maps/%s/map.json" % mapdir
        j = json.loads(todo.get(rel) or read(rel))
        placed = placed_here.setdefault(mapdir, [])
        x, y, elev = floor_tile(mapdir, where, j, placed)
        placed.append((x, y))
        objs = j["object_events"]
        new = object_for(sp, x, y, elev, gfx)
        at = next((k for k, o in enumerate(objs) if o.get("script") == label(sp)), None)
        if at is None:
            objs.append(new)
        else:
            objs[at] = new
        todo[rel] = json.dumps(j, indent=2) + "\n"
        print("  %-17s %-30s (%2d,%2d) lv %d  %s%s" % (sp[8:], mapdir, x, y, level, ed, "" if gfx else "  unseen"))
    for sp, where in ALREADY.items():
        print("  %-17s %s" % (sp[8:], where))

    changed = [rel for rel, text in todo.items()
               if not os.path.exists(os.path.join(GBA, rel)) or open(os.path.join(GBA, rel), encoding="utf-8").read() != text]
    if not changed:
        print("  already written")
        return 0
    print("  %s: %s" % ("writing" if WRITE else "would write", ", ".join(changed)))
    if WRITE:
        for rel in changed:
            open(os.path.join(GBA, rel), "w", encoding="utf-8").write(todo[rel])
    return 0


if __name__ == "__main__":
    sys.exit(main())
