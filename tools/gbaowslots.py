#!/usr/bin/env python3
"""T-133: give every redrawn daemon's overworld object a palette slot on every map it stands on.

    python3 tools/gbaowslots.py            report the plan
    python3 tools/gbaowslots.py --write    write it (palettes, art, graphics infos, map objects)

THE PROBLEM (docs/engine.md trap 17). An object's graphics info names a palette TAG and a SLOT, and the tag's palette is
patched into that slot, so two objects on one map that share a slot with different tags repaint each other. Vanilla gives
every creature object a generic NPC palette; a redrawn daemon needs its own colours, and 26 maps had no slot to spare --
FOUR ISLAND's Lorelei's house holds thirteen daemons.

THE SCHEME (decided 2026-09-19):
  1. ONE PALETTE PER TYPE, not per daemon. Each daemon's 32x32 object is reduced to its type's ramp plus five neutrals,
     so every daemon of a type shares a palette, and Lorelei's thirteen need four.
  2. SLOTS PER MAP, AT BUILD TIME. On each map every type present takes a slot nothing else there uses: a free NPC slot,
     the special slot, or -- where no object in the owning slot stands above reflective water -- a REFLECTION slot, which
     is idle unless something reflects. The link cable club's reduced reservation never hosts a daemon.
  3. The engine patches a daemon-type tag into its slot when the object spawns (event_object_movement.c), after the map's
     generic palettes are laid down.
  A species that needs a different slot on a different map gets a VARIANT graphics id sharing its art. Anything that does
  not fit is reported and left on vanilla's art, never guessed."""
import json, glob, re, os, struct, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
sys.path.insert(0, os.path.join(ROOT, "tools"))

GI = os.path.join(E, "src/data/object_events/object_event_graphics_info.h")
PTRS = os.path.join(E, "src/data/object_events/object_event_graphics_info_pointers.h")
REF = {0x10, 0x16, 0x1A, 0x1B, 0x23}          # metatile_behavior.c: MetatileBehavior_IsReflective
NPC = ["PALSLOT_NPC_1", "PALSLOT_NPC_2", "PALSLOT_NPC_3", "PALSLOT_NPC_4"]

def read(p): return open(os.path.join(E, p) if not p.startswith("/") else p).read()

#  Species whose object is not named after them, or is not named on the map at all (found 2026-09-25: the census
#  counted DEOXYS_N as vanilla and nothing asked whether a player could meet it -- one does, on THE ANNEX once CRYSTAL
#  has gone home, where BirthIsland_Exterior's script puts it in OBJ_EVENT_GFX_VAR_0). species: (gfx id, pic stem,
#  {map: the graphics_id that map's object carries for it}).
ALIASES = {"DEOXYS": ("OBJ_EVENT_GFX_DEOXYS_N", "deoxys_n", {"BirthIsland_Exterior": "OBJ_EVENT_GFX_VAR_0"})}


def daemons_with_art():
    """Species whose battle art is ours and who have an overworld object: the gfx id is the species name, or ALIASES'."""
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*= _\("(.*?)"\)', read("src/data/text/species_names.h")))
    ptrs = dict(re.findall(r"\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&gObjectEventGraphicsInfo_(\w+)", read(PTRS)))
    out = {}
    for sp, nm in names.items():
        stem = nm.lower().replace(" ", "_")
        gfx = ALIASES[sp][0] if sp in ALIASES else "OBJ_EVENT_GFX_" + sp
        if gfx in ptrs and glob.glob(os.path.join(ROOT, "gfx/daemons/%s_front.png" % stem)):
            out[sp] = ptrs[gfx]
    return out

def species_type(sp):
    return re.search(r"\[SPECIES_%s\]\s*=.*?\.types = \{TYPE_(\w+)," % sp, read("src/data/pokemon/species_info.h"), re.S).group(1)

def tileset_behaviours(ts):
    hdr = read("src/data/tilesets/headers.h"); mt = read("src/data/tilesets/metatiles.h")
    a = re.search(r"\.metatileAttributes = (\w+)", re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % ts, hdr, re.S).group(1)).group(1)
    b = open(os.path.join(E, re.search(r"%s\[\] = INCBIN_U32\(\"(.*?)\"\)" % a, mt).group(1)), "rb").read()
    return [struct.unpack_from("<I", b, i)[0] & 0x1FF for i in range(0, len(b), 4)]

def map_behaviour(layout):
    L = {l["id"]: l for l in json.loads(read("data/layouts/layouts.json"))["layouts"] if "id" in l}[layout]
    p, s = tileset_behaviours(L["primary_tileset"]), tileset_behaviours(L["secondary_tileset"])
    b = open(os.path.join(E, L["blockdata_filepath"]), "rb").read(); w = L["width"]; h = L["height"]
    def beh(x, y):
        if not (0 <= x < w and 0 <= y < h): return 0
        m = struct.unpack_from("<H", b, 2 * (y * w + x))[0] & 0x3FF
        return p[m] if m < 640 else (s[m - 640] if m - 640 < len(s) else 0)
    any_ref = any(beh(x, y) in REF for y in range(h) for x in range(w))
    return any_ref, beh

def plan():
    gi = read(GI)
    info = {n: b for n, b in re.findall(r"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_(\w+) = \{(.*?)\};", gi, re.S)}
    slot_of = {n: (re.search(r"\.paletteSlot = (\w+)", b) or [0, "?"])[1] for n, b in info.items()}
    ptrs = dict(re.findall(r"\[(OBJ_EVENT_GFX_\w+)\]\s*=\s*&gObjectEventGraphicsInfo_(\w+)", read(PTRS)))
    dm = daemons_with_art(); dgfx = {"OBJ_EVENT_GFX_" + sp: sp for sp in dm}
    #  a map already written holds VARIANT ids; read each back as its species, so a second run plans the same thing
    for g in re.findall(r"#define (OBJ_EVENT_GFX_DAEMON_\w+) \d+", read("include/constants/event_objects.h")):
        for sp in dm:
            if g.startswith("OBJ_EVENT_GFX_DAEMON_%s_S" % sp):
                dgfx[g] = sp
    maps, misfits = {}, []
    for mj in sorted(glob.glob(os.path.join(E, "data/maps/*/map.json"))):
        j = json.load(open(mj)); objs = j.get("object_events", [])
        name = os.path.basename(os.path.dirname(mj))
        here = dict(dgfx)
        for sp, (g, _, placed) in ALIASES.items():
            if sp in dm:
                here[g] = sp
                if name in placed:
                    here[placed[name]] = sp
        mine = [o for o in objs if o.get("graphics_id") in here]
        if not mine:
            continue
        refl, beh = map_behaviour(j["layout"])
        wet = lambda o: any(beh(o["x"], o["y"] + k) in REF for k in (1, 2))
        others = [o for o in objs if o.get("graphics_id") not in here]
        used = {slot_of.get(ptrs.get(o.get("graphics_id")), "?") for o in others}
        types = {}
        for o in mine:
            types.setdefault(species_type(here[o["graphics_id"]]), []).append(o)
        order = sorted(types, key=lambda t: -len(types[t]))
        free = [s for s in NPC if s not in used] + (["PALSLOT_NPC_SPECIAL"] if "PALSLOT_NPC_SPECIAL" not in used else [])
        assign = {}
        for t in order:
            if free:
                assign[t] = free.pop(0); continue
            # a reflection slot is idle unless an object in its OWNING slot stands above reflective water
            for k, s in enumerate(NPC):
                rs = s + "_REFLECTION"
                if rs in assign.values():
                    continue
                owners = [o for o in others if slot_of.get(ptrs.get(o.get("graphics_id"))) == s] + \
                         [o for tt, ss in assign.items() if ss == s for o in types[tt]]
                if not refl or not any(wet(o) for o in owners):
                    assign[t] = rs; break
            else:
                misfits.append((name, t))
        maps[name] = {t: dict(slot=assign.get(t), species=sorted({here[o["graphics_id"]] for o in types[t]})) for t in order}
    return dm, maps, misfits

if __name__ == "__main__":
    dm, maps, misfits = plan()
    pairs = {}
    for m, ts in maps.items():
        for t, v in ts.items():
            for sp in v["species"]:
                pairs.setdefault(sp, set()).add(v["slot"])
    print("%d daemon species with an overworld object, on %d maps" % (len(dm), len(maps)))
    for m, ts in maps.items():
        print("  %-36s %s" % (m, "  ".join("%s->%s" % (t, (v["slot"] or "NONE").replace("PALSLOT_NPC_", "")) for t, v in ts.items())))
    print("species needing more than one slot:", {k: sorted(v) for k, v in pairs.items() if len(v) > 1})
    print("variant graphics ids needed:", sum(len(v) - 1 for v in pairs.values()))
    print("misfits:", misfits or "none")

# ---------------------------------------------------------------------------------------------------------------------
# WRITING. Everything below is derived; running it twice changes nothing.

NEUTRALS = [(248, 248, 248), (192, 192, 192), (128, 128, 128), (64, 64, 64), (16, 16, 16)]
TAG_BASE = 0x1180                                   # OBJ_EVENT_PAL_TAG_DAEMON_TYPE_<T> = base + the type's constant
MARK = "// T-133: gbaowslots.py"

def type_consts():
    return dict((m, int(v)) for m, v in re.findall(r"#define TYPE_(\w+)\s+(\d+)", read("include/constants/pokemon.h")))

def ow_palette(t):
    import ast
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    ns = {}
    for n in tree.body:
        #  INK too: ramp5's outline is gbasprite's true black since T-184 (2026-09-21), and without it --write stopped
        #  at a NameError for four days while report mode, which never builds a palette, went on passing (2026-09-25)
        if isinstance(n, ast.FunctionDef) and n.name == "ramp5" or isinstance(n, ast.Assign) and any(getattr(x, "id", "") in ("TYPE_COLOR", "INK") for x in n.targets):
            exec(compile(ast.Module(body=[n], type_ignores=[]), "gbasprite", "exec"), ns)
    return [(0, 0, 0)] + ns["ramp5"](*ns["TYPE_COLOR"][t]) + NEUTRALS           # index 0 transparent

def write_pal(path, cols):
    full = list(cols) + [(0, 0, 0)] * (16 - len(cols))
    open(path, "wb").write(("\r\n".join(["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in full]) + "\r\n").encode())

def frame(src_png, size, pal):
    """One object frame from a BUILT battle sprite: crop to the subject, fit to size, map to the type palette, outline."""
    from PIL import Image
    im = Image.open(src_png); p = im.getpalette()[:48]; px = im.load()
    rgba = Image.new("RGBA", im.size)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            i = px[x, y]
            if i:
                rgba.putpixel((x, y), (p[3 * i], p[3 * i + 1], p[3 * i + 2], 255))
    rgba = rgba.crop(rgba.getbbox())
    w, h = rgba.size; s = (size - 1) / max(w, h)
    small = rgba.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    out = [[0] * size for _ in range(size)]
    ox, oy = (size - small.size[0]) // 2, size - small.size[1]                       # centred, standing on the floor
    lum = lambda c: c[0] * 299 + c[1] * 587 + c[2] * 114
    for y in range(small.size[1]):
        for x in range(small.size[0]):
            r, g, b, a = small.getpixel((x, y))
            if a >= 128:
                out[oy + y][ox + x] = min(range(1, len(pal)), key=lambda i: (pal[i][0] - r) ** 2 + (pal[i][1] - g) ** 2 + (pal[i][2] - b) ** 2
                                          + (lum(pal[i]) - lum((r, g, b))) ** 2 // 4000)
    for y in range(size):                                                            # at 16px the silhouette needs its line
        for x in range(size):
            if out[y][x] and any(not (0 <= x + dx < size and 0 <= y + dy < size) or not out[y + dy][x + dx]
                                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = 5
    return out

def write_png(path, frames, pal):
    from PIL import Image
    n = len(frames); s = len(frames[0])
    im = Image.new("P", (s * n, s)); im.putpalette([v for c in pal + [(0, 0, 0)] * (16 - len(pal)) for v in c])
    for k, f in enumerate(frames):
        for y in range(s):
            for x in range(s):
                im.putpixel((k * s + x, y), f[y][x])
    im.save(path)

def write(dm, maps):
    tc = type_consts()
    # 1. one palette per type that has a daemon object
    used_types = sorted({species_type(sp) for sp in dm})
    for t in used_types:
        write_pal(os.path.join(E, "graphics/object_events/palettes/daemon_type_%s.pal" % t.lower()), ow_palette(t))
    # 2. object art from each species' built battle sprites, in its type's palette
    for sp in dm:
        t = species_type(sp); pal = ow_palette(t); d = sp.lower()
        pic = os.path.join(E, "graphics/object_events/pics/pokemon/%s.png" % (ALIASES[sp][1] if sp in ALIASES else d))
        from PIL import Image
        w, h = Image.open(pic).size
        gp = os.path.join(E, "graphics/pokemon", d)
        f, b = os.path.join(gp, "front.png"), os.path.join(gp, "back.png")
        frames = [frame(f, h, pal)] if w == h else [frame(f, h, pal), frame(b, h, pal), frame(f, h, pal)][:w // h]
        write_png(pic, frames, pal)
    # 3. graphics infos: the base keeps its id with the type's tag and the slot most maps use; the rest are variants
    need = {}
    for m, ts in maps.items():
        for t, v in ts.items():
            for sp in v["species"]:
                need.setdefault(sp, []).append(v["slot"])
    base = {sp: max(sorted(set(sl)), key=sl.count) for sp, sl in need.items()}   # ties: the lowest slot, every run
    gi = read(GI)
    for sp, info in dm.items():
        t = species_type(sp)
        body = re.search(r"(const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = \{)(.*?)(\};)" % info, gi, re.S)
        nb = re.sub(r"\.paletteTag = \w+", ".paletteTag = OBJ_EVENT_PAL_TAG_DAEMON_TYPE_%s" % t, body.group(2))
        nb = re.sub(r"\.paletteSlot = \w+", ".paletteSlot = %s" % base.get(sp, "PALSLOT_NPC_1"), nb)
        gi = gi.replace(body.group(0), body.group(1) + nb + body.group(3))
    gi = re.sub(r"\n%s variants.*" % re.escape(MARK), "", gi, flags=re.S)
    consts = read("include/constants/event_objects.h")
    #  Remove only OUR lines -- the mark and the variant defines. Ids added after this tool last ran (T-208's PLUGIN
    #  DISC, T-256's DAD) sit between them and NUM_OBJ_EVENT_GFX, and an earlier version of this line deleted them
    #  with everything else down to NUM (caught before commit, 2026-09-25).
    consts = re.sub(r"\n%s variants[^\n]*" % re.escape(MARK), "", consts)
    consts = re.sub(r"\n#define OBJ_EVENT_GFX_DAEMON_\w+ \d+", "", consts)
    first = int(re.search(r"#define OBJ_EVENT_GFX_CUE_BALL (\d+)", consts).group(1)) + 1
    ptrs = read(PTRS); ptrs = re.sub(r"\n    %s variants.*?(?=\n\};)" % re.escape(MARK), "", ptrs, flags=re.S)
    variants, vid, vdefs, vinfos, vptrs = {}, first, [], [], []
    for sp in sorted(need):
        for sl in sorted(set(need[sp]) - {base[sp]}):
            name = "%s_%s" % (sp, sl.replace("PALSLOT_NPC_", "S"))
            variants[(sp, sl)] = "OBJ_EVENT_GFX_DAEMON_" + name
            vdefs.append("#define OBJ_EVENT_GFX_DAEMON_%s %d" % (name, vid)); vid += 1
            src = re.search(r"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = \{(.*?)\};" % dm[sp], gi, re.S).group(1)
            vinfos.append("const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Daemon_%s = {%s};" %
                          (name.title().replace("_", ""), re.sub(r"\.paletteSlot = \w+", ".paletteSlot = %s" % sl, src)))
            vptrs.append("    [OBJ_EVENT_GFX_DAEMON_%s] = &gObjectEventGraphicsInfo_Daemon_%s," % (name, name.title().replace("_", "")))
    assert vid <= 240, "variants run into the dynamic gfx ids"
    anchor = re.search(r"#define OBJ_EVENT_GFX_CUE_BALL \d+\n", consts)
    consts = consts[:anchor.end()] + "\n%s variants: a daemon's object in another palette slot, same art\n%s\n" % (MARK, "\n".join(vdefs)) + consts[anchor.end():]
    consts = re.sub(r"\n{3,}", "\n\n", consts)
    ids = [int(v) for v in re.findall(r"#define OBJ_EVENT_GFX_\w+ (\d+)", consts.split("// These are dynamic")[0])]
    consts = re.sub(r"#define NUM_OBJ_EVENT_GFX\s+\d+", "#define NUM_OBJ_EVENT_GFX     %d" % (max(ids) + 1), consts)
    open(os.path.join(E, "include/constants/event_objects.h"), "w").write(consts)
    open(GI, "w").write(gi.rstrip() + "\n\n%s variants: the same art, another slot\n%s\n" % (MARK, "\n".join(vinfos)))
    ptrs = re.sub(r"\n\};\s*$", "\n    %s variants\n%s\n};\n" % (MARK, "\n".join(vptrs)), ptrs.rstrip() + "\n")
    #  the table is included BEFORE the infos, so each needs a forward declaration at the top, as vanilla's do
    ptrs = re.sub(r"^%s declarations\n(?:const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Daemon_\w+;\n)*" % re.escape(MARK), "", ptrs)
    decl = "".join("const struct ObjectEventGraphicsInfo %s;\n" % re.search(r"&(\w+),", v).group(1) for v in vptrs)
    ptrs = "%s declarations\n%s" % (MARK, decl) + ptrs
    open(PTRS, "w").write(ptrs)
    # 4. every map object points at the id whose slot that map assigned
    for m, ts in maps.items():
        p = os.path.join(E, "data/maps/%s/map.json" % m); s = open(p).read()
        for t, v in ts.items():
            for sp in v["species"]:
                want = variants[(sp, v["slot"])] if v["slot"] != base[sp] else "OBJ_EVENT_GFX_%s" % sp
                s = re.sub(r'"graphics_id": "OBJ_EVENT_GFX_(?:DAEMON_)?%s(?:_S\w+)?"' % sp, '"graphics_id": "%s"' % want, s)
        open(p, "w").write(s)
    print("wrote %d type palettes, %d objects' art, %d variants" % (len(used_types), len(dm), len(variants)))

if __name__ == "__main__" and "--write" in sys.argv:
    dm, maps, misfits = plan()
    write(dm, maps)
