#!/usr/bin/env python3
"""Each BENCHMARK battles in its own town's colour (T-16; vision.md 5.3, 9.4).

    python3 tools/genbackdrops.py            # preview to /tmp/backdrops.png, and what would change
    python3 tools/genbackdrops.py --write    # eight palettes, the terrain constants, and battle_bg.c

VANILLA GAVE EVERY GYM ONE BACKDROP AND THE ELITE FOUR FIVE. All eight leaders battle on
BATTLE_TERRAIN_LEADER, chosen by TRAINER CLASS in GetBattleTerrainOverride(), and every gym trainer on
BATTLE_TERRAIN_GYM, chosen by the map's battle scene -- one pale room between them. Lorelei, Bruno,
Agatha, Lance and the Champion each get their own, and the way they get it is the finding T-16 turned on:
THE FIVE SHARE ONE TILESET AND ONE TILEMAP AND DIFFER ONLY IN PALETTE. A room of its own costs sixteen
colours times three, not a drawing.

The ticket had costed two options -- reassign an existing terrain per gym, or draw eight new tilesets --
and asked for one to be chosen before starting. The Elite Four are a third, already proven in the
cartridge, and it was chosen: each BENCHMARK's trainers and its leader battle in the shared room,
coloured as the town is (9.4, where colour carries the argument).

THE COLOUR IS READ, NOT PICKED. Each town's palette lives in `gentowns.py` (`CALLOW_PAL`, `SLATE_PAL`,
...), and a town's first three colours are its own ramp -- light, mid and dark of the town colour, before
the accents. Its KEY is the most saturated of those three, so CALLOW is its green and SLATE its stone.

THE WAY A ROOM IS TINTED IS VANILLA'S. Lorelei's palette is the pale room tinted icy blue, index by index:
each index keeps the VALUE Lorelei gives it and the SATURATION Lorelei gives it, scaled by how saturated
the town's key is against Lorelei's own, and takes the town's HUE. The scale is what keeps SLATE and
QUICKSILVER grey: a first mock kept every town at Lorelei's saturation and put SLATE and DOLDRUM in the
same blue, because a stone and a sea differ in how much colour they have, not only in which.

WHICH ROOM IS WHICH IS DERIVED TOO: `gbainterior.py` pairs each `LAYOUT_*_GYM` with the town it draws, and
the C looks the backdrop up by the MAP the battle happens on, so a BENCHMARK's trainers and its leader
share it and nothing outside the eight rooms changes.
"""
import ast, colorsys, os, re, struct, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
TOOLS = os.path.join(ROOT, "tools")
WRITE = "--write" in sys.argv
PREVIEW = "/tmp/backdrops.png"
INDOOR = os.path.join(GBA, "graphics/battle_terrain/indoor")


def read_pal(path):
    L = open(path).read().replace("\r", "").split("\n")
    return [tuple(map(int, l.split())) for l in L[3:3 + int(L[2])]]


def town_palettes():
    """TOWN_PAL = [...] out of gentowns.py -- parsed, not imported (engine.md trap 16)"""
    src = open(os.path.join(TOOLS, "gentowns.py")).read()
    out = {}
    for m in re.finditer(r"^([A-Z]+)_PAL = (\[.*?\])\n(?=\S)", src, re.S | re.M):
        out[m.group(1)] = ast.literal_eval(m.group(2))
    return out


def benchmarks():
    """(layout, TOWN) for each BENCHMARK, as gbainterior.py pairs them"""
    src = open(os.path.join(TOOLS, "gbainterior.py")).read()
    return [(lid, town.upper()) for lid, town in re.findall(r'layouts=\[\("(LAYOUT_\w+_GYM)", (\w+)\)\]', src)]


def hsv(c):
    return colorsys.rgb_to_hsv(*[v / 255 for v in c])


def snap(v):
    return round(round(max(0, min(255, v)) * 31 / 255) * 255 / 31)


def key_colour(pal):
    return max(pal[:3], key=lambda c: hsv(c)[1])


def tint(lorelei, key):
    ref = max(hsv(c)[1] for c in lorelei)            # how much colour vanilla gave its most tinted index
    kh, ks, _ = hsv(key)
    out = []
    for c in lorelei:
        _, s, v = hsv(c)
        out.append(tuple(snap(x * 255) for x in colorsys.hsv_to_rgb(kh, min(1.0, s * (ks / ref if ref else 0)), v)))
    return out


def render(P):
    tiles = Image.open(os.path.join(GBA, "graphics/battle_terrain/building/terrain.png")).convert("P")
    tp, tw = tiles.load(), tiles.width // 8
    raw = open(os.path.join(GBA, "graphics/battle_terrain/building/terrain.bin"), "rb").read()
    img = Image.new("RGB", (240, 112)); ip = img.load()
    for i, e in enumerate(struct.unpack("<%dH" % (len(raw) // 2), raw)):
        cx, cy = (i % 32) * 8, (i // 32) * 8
        if cx >= 240 or cy >= 112:
            continue
        t, hf, vf, pn = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
        tx, ty = (t % tw) * 8, (t // tw) * 8
        for y in range(8):
            for x in range(8):
                c = tp[tx + (7 - x if hf else x), ty + (7 - y if vf else y)] if ty + 8 <= tiles.height else 0
                k = (pn - 2) * 16 + c                  # the terrain palette loads at BG palette 2
                ip[cx + x, cy + y] = P[k] if 0 <= k < len(P) else (0, 0, 0)
    return img


def camel(s):
    return s.capitalize()


def register(rooms):
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            open(p, "w").write(s2)
        return s2 != s

    def constants(s):
        if "BATTLE_TERRAIN_BENCHMARK_" in s:
            return s
        anchor = "#define BATTLE_TERRAIN_CHAMPION    19\n"
        assert s.count(anchor) == 1
        lines = "".join("#define BATTLE_TERRAIN_BENCHMARK_%-12s %d\n" % (town, 20 + i) for i, (_, town) in enumerate(rooms))
        return s.replace(anchor, anchor + "// T-16: each BENCHMARK's own room, in its town's colour\n" + lines)
    edit("include/constants/battle.h", constants)

    def bg(s):
        if "sBattleTerrainPalette_Benchmark" in s:
            return s
        inc = "static const u32 sBattleTerrainPalette_Champion[] = INCBIN_U32(\"graphics/battle_terrain/indoor/champion.gbapal.lz\");\n"
        assert s.count(inc) == 1
        s = s.replace(inc, inc + "".join(
            'static const u32 sBattleTerrainPalette_Benchmark%s[] = INCBIN_U32("graphics/battle_terrain/indoor/benchmark_%s.gbapal.lz");\n'
            % (camel(t), t.lower()) for _, t in rooms))
        end = s.index("};\n", s.index("[BATTLE_TERRAIN_CHAMPION] ="))
        entries = "".join((
            "    },\n    [BATTLE_TERRAIN_BENCHMARK_%s] =\n    {\n"
            "        .tileset = sBattleTerrainTiles_Building,\n        .tilemap = sBattleTerrainTilemap_Building,\n"
            "        .entryTileset = sBattleTerrainAnimTiles_Building,\n        .entryTilemap = sBattleTerrainAnimTilemap_Building,\n"
            "        .palette = sBattleTerrainPalette_Benchmark%s\n") % (t, camel(t)) for _, t in rooms)
        close = s.rindex("    }\n", 0, end)
        s = s[:close] + entries + s[close:]
        fn = "static u8 GetBattleTerrainOverride(void)\n{\n"
        assert s.count(fn) == 1
        table = ("// T-16: a BENCHMARK's trainers and its leader battle in the town's own colour. Keyed by the MAP the\n"
                 "// battle is on, not the trainer's class, so the room is the room you met them in.\n"
                 "static const struct { u16 map; u8 terrain; } sBenchmarkRooms[] = {\n" + "".join(
                     "    {MAP_%s, BATTLE_TERRAIN_BENCHMARK_%s},\n" % (lid[len("LAYOUT_"):], t) for lid, t in rooms) + "};\n\n"
                 "static u8 GetBenchmarkRoomTerrain(void)\n{\n    u32 i;\n    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;\n"
                 "    for (i = 0; i < ARRAY_COUNT(sBenchmarkRooms); i++)\n        if (sBenchmarkRooms[i].map == map)\n"
                 "            return sBenchmarkRooms[i].terrain;\n    return 0;\n}\n\n")
        s = s.replace(fn, table + fn)
        old = "    else if (gBattleTypeFlags & BATTLE_TYPE_TRAINER)\n    {\n"
        assert s.count(old) == 1
        s = s.replace(old, "    else if ((gBattleTypeFlags & BATTLE_TYPE_TRAINER) && GetBenchmarkRoomTerrain())\n    {\n"
                           "        return GetBenchmarkRoomTerrain();\n    }\n" + old)
        return s
    edit("src/battle_bg.c", bg)


def main():
    towns, rooms = town_palettes(), benchmarks()
    assert len(rooms) == 8, "gbainterior.py names %d BENCHMARK rooms, not 8" % len(rooms)
    lorelei = read_pal(os.path.join(INDOOR, "lorelei.pal"))
    built = []
    for lid, town in rooms:
        key = key_colour(towns[town])
        pal = tint(lorelei, key)
        built.append((lid, town, key, pal))
        print("  %-28s %-12s key %-16s -> benchmark_%s.pal" % (lid, town, key, town.lower()))
    S = 2
    shots = [("LEADER, today (all eight)", read_pal(os.path.join(INDOOR, "leader.pal")))] + [(t, p) for _, t, _, p in built]
    sheet = Image.new("RGB", ((240 * S + 10) * 3, (112 * S + 16) * 3), (30, 30, 34)); d = ImageDraw.Draw(sheet)
    for i, (label, P) in enumerate(shots):
        x, y = (i % 3) * (240 * S + 10), (i // 3) * (112 * S + 16)
        sheet.paste(render(P).resize((240 * S, 112 * S), Image.NEAREST), (x, y + 14)); d.text((x + 2, y + 1), label, fill=(240, 240, 240))
    sheet.save(PREVIEW)
    print("  -> preview %s" % PREVIEW)
    if WRITE:
        for _, town, _, pal in built:
            with open(os.path.join(INDOOR, "benchmark_%s.pal" % town.lower()), "w") as fh:
                fh.write("JASC-PAL\r\n0100\r\n%d\r\n" % len(pal) + "".join("%d %d %d\r\n" % c for c in pal))
        register(rooms)
        print("  written 8 palettes; constants and battle_bg.c registered")


if __name__ == "__main__":
    main()
