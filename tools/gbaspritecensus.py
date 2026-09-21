#!/usr/bin/env python3
"""How far the sprites are from vanilla -- measured, never typed.

    python3 tools/gbaspritecensus.py            # report
    python3 tools/gbaspritecensus.py --write    # and rewrite docs/sprites.md

Every sprite image in the engine is compared with pret's own (upstream/master, already fetched) BY
PIXEL, not by file: a PNG re-saved by a tool with the same drawing is still vanilla. Each lands in
one of three states:

    redrawn     the drawing differs from vanilla's
    recoloured  the same drawing, a different palette in the PNG
    vanilla     identical

Images that vanilla never had (the BENCHMARK staff, the Owl) are counted as ADDED and kept out of the
percentage, which is "of the sprites vanilla shipped, how many are ours". The headline is the
people -- overworld figures and every trainer picture a player sees -- because that is what the
fable rule (vision.md 9.4) asks for; daemons and objects have their own lines.

And per town: which people sheets its maps put on screen, and how many of those are still vanilla.
A sheet shared by several towns can carry only one look, so the shared ones are listed -- a town's
own colour and theme (vision.md 3.1) needs its own sprites where it shares.
"""
import collections, glob, io, json, os, re, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DOC = os.path.join(ROOT, "docs", "sprites.md")
WRITE = "--write" in sys.argv
UPSTREAM = "upstream/master"

CATEGORIES = [   # name, glob, counts toward the people headline
    ("overworld people", "graphics/object_events/pics/people/*.png", True),
    ("trainer portraits", "graphics/trainers/front_pics/*.png", True),
    ("trainer back pics", "graphics/trainers/back_pics/*.png", True),
    ("intro portraits", "graphics/oak_speech/*/pic.png", True),
    ("hearsay portraits", "graphics/fame_checker/*.png", True),   # cursor.png and question_mark.png are UI,
                                                             # not people, and are skipped below
    ("daemon fronts", "graphics/pokemon/*/front.png", False),
    ("daemon backs", "graphics/pokemon/*/back.png", False),
    ("daemon icons", "graphics/pokemon/*/icon.png", False),
    ("overworld daemons", "graphics/object_events/pics/pokemon/*.png", False),
    ("overworld objects", "graphics/object_events/pics/misc/*.png", False),
]

TOWNS = [   # vanilla map prefix, our name, colour and theme (vision.md 3.1)
    ("PalletTown", "BLANCHE", "white, blank; home, the pre-colour state"),
    ("ViridianCity", "CALLOW", "green, unripe, untested"),
    ("PewterCity", "SLATE", "stone, a writing surface; the museum of dead hardware"),
    ("CeruleanCity", "DOLDRUM", "a becalmed sea, low spirits"),
    ("VermilionCity", "ARDOR", "flush and heat, brash zeal; the port"),
    ("LavenderTown", "HALFTONE", "dots that only look like grey; the tower"),
    ("CeladonCity", "VERDIGRIS", "green corrosion on bronze; Corpus rotting beneath"),
    ("FuchsiaCity", "LURID", "garish glow; spectacle and toxicity"),
    ("SaffronCity", "BRAZEN", "brass over base metal; corporate capture"),
    ("CinnabarIsland", "QUICKSILVER", "mercury: alive, unstable; the ruined lab"),
    ("IndigoPlateau", "UMBRA", "full shadow, all colour absorbed; the Review Board"),
]


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", GBA] + list(args), capture_output=True)
    return r.stdout if binary else r.stdout.decode()


def upstream_files():
    return set(git("ls-tree", "-r", "--name-only", UPSTREAM, "graphics").split("\n"))


def pixels(img):
    """the drawing: palette indices for a paletted image, colours otherwise"""
    if img.mode == "P":
        return ("P", img.size, img.tobytes())
    return ("RGBA", img.size, img.convert("RGBA").tobytes())


def state(path, vanilla):
    if path not in vanilla:
        return "added"
    ours = Image.open(os.path.join(GBA, path))
    theirs = Image.open(io.BytesIO(git("show", "%s:%s" % (UPSTREAM, path), binary=True)))
    if ours.size != theirs.size:
        return "redrawn"
    if ours.mode == "P" and theirs.mode == "P":
        if ours.tobytes() != theirs.tobytes():
            return "redrawn"
        return "recoloured" if ours.getpalette() != theirs.getpalette() else "vanilla"
    if pixels(ours) == pixels(theirs):
        return "vanilla"
    return "redrawn"


def gfx_to_sheet():
    """OBJ_EVENT_GFX_* -> the people sheet(s) it draws, read from the engine's own tables"""
    graphics = open(os.path.join(GBA, "src/data/object_events/object_event_graphics.h")).read()
    pics = dict(re.findall(r'const u16 (gObjectEventPic_\w+)\[\] = INCBIN_U16\("graphics/object_events/pics/(\w+/\w+)\.4bpp"\)', graphics))
    tables = open(os.path.join(GBA, "src/data/object_events/object_event_pic_tables.h")).read()
    table_pics = {}
    for name, body in re.findall(r'static const struct SpriteFrameImage (sPicTable_\w+)\[\] = \{(.*?)\};', tables, re.S):
        table_pics[name] = sorted(set(re.findall(r'(gObjectEventPic_\w+)', body)))
    info = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")).read()
    info_table = dict(re.findall(r'const struct ObjectEventGraphicsInfo (gObjectEventGraphicsInfo_\w+) = \{.*?\.images = (sPicTable_\w+),', info, re.S))
    pointers = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info_pointers.h")).read()
    out = {}
    for gfx, gi in re.findall(r'\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&(gObjectEventGraphicsInfo_\w+)', pointers):
        sheets = [pics[p] for p in table_pics.get(info_table.get(gi, ""), []) if p in pics]
        out[gfx] = ["graphics/object_events/pics/%s.png" % s for s in sheets]
    return out


def unreachable_people():
    """The people sheets nothing can put on screen, found by walking the WHOLE chain.

    T-120 kept reading as unfinished because the census said "11 still vanilla", which is true and useless if
    nothing can reach them. But reachability is not one test, it is a chain, and two shorter tests both give
    the wrong answer:

        "is its graphics id set anywhere?"   calls red_surf_run unreachable -- nothing sets RED_SURF_RUN,
                                             yet sPicTable_RedSurf reads its frames, and that is what the
                                             player is made of while crossing water
        "is its symbol in a pic table?"      calls teachy_tv_host reachable -- it has a pic table of its own
                                             and nothing ever sets the id that would use it

    So the chain is walked: a graphics id that something SETS -> its ObjectEventGraphicsInfo -> the .images
    pic table -> the gObjectEventPic_ symbols in it -> the file each symbol INCBINs. A file nothing reaches
    that way cannot appear on screen, whatever its name suggests.

    This is also how red_surf.png turns out to be art the engine never looks at: RED_SURF is set (the player
    avatar's RIDE state) but its graphics info points .images at sPicTable_RedSurf, which names RedSurfRun.
    """
    d = os.path.join(GBA, "src/data/object_events")
    #  1. every graphics id something actually sets
    setters = set()
    for mj in glob.glob(os.path.join(GBA, "data/maps/*/map.json")):
        for o in json.load(open(mj)).get("object_events", []):
            setters.add(o.get("graphics_id", ""))
    text = ""
    for pat in ("src/*.c", "data/scripts/*.inc", "data/maps/*/scripts.inc"):
        for f in glob.glob(os.path.join(GBA, pat)):
            if os.path.basename(f) != "dynamic_placeholder_text_util.c":
                text += open(f, errors="ignore").read()
    setters |= set(re.findall(r"OBJ_EVENT_GFX_\w+", text))
    #  2. id -> info, 3. info -> pic table, 4. pic table -> symbols, 5. symbol -> file
    pointers = open(os.path.join(d, "object_event_graphics_info_pointers.h"), errors="ignore").read()
    id_to_info = dict(re.findall(r"\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&(\w+)", pointers))
    infos = open(os.path.join(d, "object_event_graphics_info.h"), errors="ignore").read()
    info_to_table = dict(re.findall(r"ObjectEventGraphicsInfo (\w+) = \{(?:.*?)\.images = (\w+)", infos, re.S))
    tables = open(os.path.join(d, "object_event_pic_tables.h"), errors="ignore").read()
    table_to_syms = {m.group(1): set(re.findall(r"(gObjectEventPic_\w+)", m.group(2)))
                     for m in re.finditer(r"sPicTable_(\w+)\[\] = \{(.*?)\};", tables, re.S)}
    sym_to_file = dict(re.findall(r"const u16 (gObjectEventPic_\w+)\[\] = INCBIN_U16\(\"graphics/object_events/pics/people/(\w+)\.4bpp\"",
                                  open(os.path.join(d, "object_event_graphics.h"), errors="ignore").read()))
    live = set()
    for gfx in setters:
        table = info_to_table.get(id_to_info.get(gfx, ""), "")
        for sym in table_to_syms.get(table[len("sPicTable_"):] if table.startswith("sPicTable_") else table, ()):
            if sym in sym_to_file:
                live.add(sym_to_file[sym])
    out = set()
    for full in glob.glob(os.path.join(GBA, "graphics/object_events/pics/people/*.png")):
        if os.path.splitext(os.path.basename(full))[0] not in live:
            out.add(os.path.relpath(full, GBA))
    return out


def main():
    vanilla = upstream_files()
    dead = unreachable_people()
    results = collections.OrderedDict()
    status = {}
    for name, pattern, people in CATEGORIES:
        counts = collections.Counter()
        for full in sorted(glob.glob(os.path.join(GBA, pattern))):
            path = os.path.relpath(full, GBA)
            if os.path.basename(path) in ("cursor.png", "question_mark.png"):
                continue                       # the fame checker's UI, not one of its portraits
            s = state(path, vanilla)
            if s == "vanilla" and path in dead:
                s = "unreachable"                 # nothing places it, nothing sets it, nothing reads it
            status[path] = s
            counts[s] += 1
        results[name] = (counts, people)

    def pct(c):
        base = c["redrawn"] + c["recoloured"] + c["vanilla"]
        return (100.0 * c["redrawn"] / base) if base else 0.0, base

    lines = ["| sprites | vanilla shipped | redrawn | recoloured | still vanilla | added | done |", "|---|---|---|---|---|---|---|"]
    people_total, all_total = collections.Counter(), collections.Counter()
    for name, (c, people) in results.items():
        p, base = pct(c)
        lines.append("| %s | %d | %d | %d | %d | %d | **%.0f%%** |" % (name, base, c["redrawn"], c["recoloured"], c["vanilla"], c["added"], p))
        all_total.update(c)
        if people:
            people_total.update(c)
    pp, pbase = pct(people_total)
    ap, abase = pct(all_total)
    lines.append("| ***the people*** | %d | %d | %d | %d | %d | ***%.1f%%*** |" % (pbase, people_total["redrawn"], people_total["recoloured"], people_total["vanilla"], people_total["added"], pp))
    lines.append("| ***every sprite*** | %d | %d | %d | %d | %d | ***%.1f%%*** |" % (abase, all_total["redrawn"], all_total["recoloured"], all_total["vanilla"], all_total["added"], ap))

    # per town: the people sheets its maps (outside the BENCHMARK, already done) put on screen
    sheets_of = gfx_to_sheet()
    town_sheets = {}
    sheet_towns = collections.defaultdict(set)
    for prefix, name, _ in TOWNS:
        used = collections.Counter()
        for mp in glob.glob(os.path.join(GBA, "data/maps/%s*/map.json" % prefix)):
            for o in json.load(open(mp)).get("object_events", []):
                for sh in sheets_of.get(o.get("graphics_id", ""), []):
                    if "/people/" in sh:
                        used[sh] += 1
        town_sheets[name] = used
        for sh in used:
            sheet_towns[sh].add(name)
    town_lines = ["| town | colour and theme | people sheets on screen | still vanilla | shared with other towns | done |", "|---|---|---|---|---|---|"]
    for prefix, name, theme in TOWNS:
        used = town_sheets[name]
        van = [s for s in used if status.get(s) == "vanilla"]
        shared = [s for s in used if len(sheet_towns[s]) > 1]
        done = (100.0 * (len(used) - len(van)) / len(used)) if used else 0.0
        town_lines.append("| **%s** | %s | %d | %d | %d | %.0f%% |" % (name, theme, len(used), len(van), len(shared), done))

    report = "\n".join(lines) + "\n\n" + "\n".join(town_lines)
    print(report)
    if WRITE:
        head = git("rev-parse", "--short", "HEAD").strip()
        body = ("# Sprites — how far from vanilla\n\n"
                "**Generated by `python3 tools/gbaspritecensus.py --write`; do not edit by hand.** "
                "*Measured against pret's `%s` by pixel, at engine commit `%s`.* "
                "**Redrawn** means the drawing differs; **recoloured** is the same drawing with another palette in the PNG; "
                "**added** sprites vanilla never had and are kept out of the percentage. "
                "*The people line is the headline: every overworld figure and trainer picture a player sees, which is what 9.4's fable rule asks for.*\n\n"
                % (UPSTREAM, head) + "\n".join(lines) + "\n\n"
                "## The towns\n\n"
                "**A town's people are the sheets its maps put on screen, BENCHMARK interiors aside.** "
                "*A sheet shared with other towns can carry only one look, so a town themed to its own colour needs its own sprites where it shares* (vision.md 3.1).\n\n"
                + "\n".join(town_lines) + "\n")
        open(DOC, "w").write(body)
        print("\n  written %s" % os.path.relpath(DOC, ROOT))


if __name__ == "__main__":
    main()
