#!/usr/bin/env python3
"""Every door's opening, drawn to match the building it opens (T-438 batch A; the door-mat arrow too).

    python3 tools/gbadoors.py                 # report: every door animation, where it opens, does its frame fit
    python3 tools/gbadoors.py --draft DIR     # the new frames as PNGs in DIR (gfx/drafts/t438/doors/), and the
                                              #   contact sheets beside them (or --sheets DIR to put those elsewhere)
    python3 tools/gbadoors.py --write         # graphics/door_anims/*.png and the arrow into the engine -- NOT YET:
                                              #   batch A is a draft until the user has seen the sheets

HOW A DOOR OPENS ON THE GBA (src/field_door.c). A door is a block with the WARP_DOOR behaviour whose id is in
sDoorGraphics. The CLOSED door is not in the animation at all: it is the block itself, drawn from the map. The
animation is three OPEN frames -- ajar, half, open -- each 16x16 (DOOR_SIZE_1x1, the door cell) or 16x32
(DOOR_SIZE_1x2, the cell above it too), copied into the last eight tiles of VRAM and drawn on the block's BOTTOM
layer in ONE palette row per tile (sDoorAnimPalettes_*); the top layer is blanked. So a frame:

  * must match the closed block wherever the door is not moving, pixel for pixel, or the wall around the door
    jumps for a quarter of a second each time it opens -- vanilla's frames over our redrawn houses do exactly that;
  * is drawn in the palette row field_door.c names, from THAT tileset's colours, so every colour the closed block
    shows (bottom and top layer together, in whatever rows they use) has to be found in that one row;
  * is keyed by block id ALONE: GetDoorGraphics() does not ask which tileset is loaded, so a secondary id plays
    the same frames in every town whose block of that number is a door. This tool finds every such door by
    reading every layout, and reports a door id whose closed blocks look different in different places.

WHAT IS DRAWN. Each closed block is rendered from the tileset as the map draws it, and the moving part -- the
leaf -- is the rectangle DOORS below gives it, measured by eye from the closed blocks (vanilla's own frames repaint
the whole cell, so they cannot say where a leaf is). Then in our style, the way gbalab.py opened CRYSTAL's door:

  HINGED   the leaf swings in on its hinge: it narrows toward the hinge and darkens as it turns from the light,
           the room behind it is the row's darkest colour with one lit floor line at the sill, and at the end only
           the leaf's edge is left against the jamb.
  SLIDING  the leaves part and slide behind the wall either side (a double) or one way (a single); the glass's
           highlights travel with them, and the room is dark behind.
  LIFT     a lift's two steel doors part from the middle, both cells high.

Everything outside the doorway is copied from the closed block, so it cannot drift from the facade. If the row
lacks a colour the closed block uses, the row (or a row per tile) that does draw it is used instead and the door is
REPORTED: field_door.c's sDoorAnimPalettes_* must change with it, by hand, when the frames go in.

ALSO REPORTED: a block on a door's map that draws a secondary tile at 376..383, which the frames overwrite in VRAM.

THE ARROW (graphics/field_effects/pics/arrow.png, FLDEFFOBJ_ARROW): the mat's warp arrow, eight 16x16 frames
(north x2, south x2, west x2, east x2). Its template names no palette tag, so it draws in sprite palette 0 -- the
PLAYER's palette (graphics/object_events/palettes/player.pal) -- and may only use that row's colours.
"""
import collections, glob, hashlib, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from daemonslib import read_pal
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t438", "doors")
MB_WARP_DOOR = 0x69
NUM_PRIMARY = 640
TILE_START_DOOR = 1024 - 8            # DOOR_TILE_START: the last eight tiles of the BG's 1024 (secondary 376..383)

ARGS = sys.argv[1:]
WRITE = "--write" in ARGS


def argval(flag):
    if flag in ARGS:
        i = ARGS.index(flag)
        if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--"):
            return ARGS[i + 1]
        return ""
    return None


DRAFT = argval("--draft")
if DRAFT == "":
    DRAFT = DRAFT_DEFAULT
SHEETS = argval("--sheets") or DRAFT


# ================================================================== the engine, read (current or vanilla)
class Source:
    """Files from the engine as it stands (vanilla=False) or from pristine upstream (vanilla=True)."""

    def __init__(self, vanilla):
        self.vanilla = vanilla
        self._cache = {}

    def raw(self, rel):
        if rel not in self._cache:
            if self.vanilla:
                self._cache[rel] = daemonslib.upstream(GBA, rel, missing=None, binary=True)
            else:
                p = os.path.join(GBA, rel)
                self._cache[rel] = open(p, "rb").read() if os.path.exists(p) else None
        return self._cache[rel]

    def text(self, rel):
        b = self.raw(rel)
        return None if b is None else b.decode("utf-8", "replace")

    def png(self, rel):
        b = self.raw(rel)
        return None if b is None else Image.open(io.BytesIO(b))

    def pal(self, rel):
        t = self.text(rel)
        if t is None:
            return None
        L = t.replace("\r", "").split("\n")
        return [tuple(map(int, l.split()[:3])) for l in L[3:19]]


CUR, VAN = Source(False), Source(True)


class Tileset:
    def __init__(self, src, dirs):
        tdir, pdir, rel = dirs
        self.rel = rel
        self.secondary = "/secondary/" in rel
        img = src.png(tdir + "/tiles.png")
        self.ok = img is not None
        if not self.ok:
            return
        self.w = img.width
        self.ntiles = (img.width // 8) * (img.height // 8)
        self.px = img.tobytes() if img.mode == "P" else img.convert("P").tobytes()
        self.meta = src.raw(rel + "/metatiles.bin") or b""
        self.attr = src.raw(rel + "/metatile_attributes.bin") or b""
        self.pals = [src.pal(pdir + "/palettes/%02d.pal" % i) for i in range(16)]

    def tile(self, i):
        """an 8x8 tile's indices (0..15), row-major"""
        if i >= self.ntiles:
            return [0] * 64
        tx, ty = (i % (self.w // 8)) * 8, (i // (self.w // 8)) * 8
        return [self.px[(ty + y) * self.w + tx + x] & 15 for y in range(8) for x in range(8)]


class Pair:
    """A layout's two tilesets, as the GBA has them in VRAM: tile < 640 and palette row < 7 from the primary."""

    def __init__(self, prim, sec):
        self.prim, self.sec = prim, sec

    def entries(self, mid):
        ts, k = (self.prim, mid) if mid < NUM_PRIMARY else (self.sec, mid - NUM_PRIMARY)
        if (k + 1) * 16 > len(ts.meta):
            return None
        return struct.unpack_from("<8H", ts.meta, k * 16)

    def behavior(self, mid):
        ts, k = (self.prim, mid) if mid < NUM_PRIMARY else (self.sec, mid - NUM_PRIMARY)
        if (k + 1) * 4 > len(ts.attr):
            return None
        return struct.unpack_from("<I", ts.attr, k * 4)[0] & 0x1FF

    def palette(self, row):
        p = (self.prim if row < 7 else self.sec).pals[row]
        return p or [(255, 0, 255)] * 16

    def tilepx(self, t):
        idx = t & 0x3FF
        ts, i = (self.prim, idx) if idx < NUM_PRIMARY else (self.sec, idx - NUM_PRIMARY)
        px = ts.tile(i)
        if t & 0x400:
            px = [px[y * 8 + 7 - x] for y in range(8) for x in range(8)]
        if t & 0x800:
            px = [px[(7 - y) * 8 + x] for y in range(8) for x in range(8)]
        return px

    def render(self, mid):
        """a block as the map draws it: 16x16 of (row, index, rgb); bottom opaque, top's index 0 transparent"""
        e = self.entries(mid)
        out = [[None] * 16 for _ in range(16)]
        if e is None:
            return out
        for layer in (0, 1):
            for q in range(4):
                t = e[layer * 4 + q]
                row = (t >> 12) & 15
                pal = self.palette(row)
                px = self.tilepx(t)
                for y in range(8):
                    for x in range(8):
                        v = px[y * 8 + x]
                        if layer and v == 0:
                            continue
                        out[(q // 2) * 8 + y][(q % 2) * 8 + x] = (row, v, pal[v])
        return out


def labels(src):
    out = {}
    for name, val in re.findall(r"#define\s+(METATILE_\w+)\s+(0x[0-9A-Fa-f]+)", src.text("include/constants/metatile_labels.h") or ""):
        out[name] = int(val, 16)
    return out


def door_table(src):
    """sDoorGraphics, in field_door.c's order: (label, sound, size, png, palette rows)"""
    c = src.text("src/field_door.c")
    tiles = dict(re.findall(r"sDoorAnimTiles_(\w+)\[\]\s*=\s*INCBIN_U8\(\"(graphics/door_anims/\w+)\.4bpp\"\)", c))
    pals = {k: [int(x) for x in v.split(",")] for k, v in re.findall(r"sDoorAnimPalettes_(\w+)\[\]\s*=\s*\{([\d,\s]+)\}", c)}
    out = []
    for lab, snd, size, t, p in re.findall(
            r"\{(METATILE_\w+),\s*DOOR_SOUND_(\w+),\s*DOOR_SIZE_(\w+),\s*sDoorAnimTiles_(\w+),\s*sDoorAnimPalettes_(\w+)\}", c):
        out.append(dict(label=lab, sound=snd.lower(), size=size, png=tiles[t] + ".png", rows=pals[p], palsym=p, name=os.path.basename(tiles[t])))
    return out


def tileset_dirs(src):
    """gTileset_X -> (tiles dir, palettes dir, metatiles dir), as headers.h joins them: a tileset may borrow another's
    tiles and palettes (gTileset_SilphCo draws Condominiums'), so the directory of its metatiles is not enough"""
    gfx = (src.text("src/data/tilesets/graphics.h") or "") + (src.text("src/graphics.c") or "")   # primaries are in graphics.c
    tiles = dict(re.findall(r"(gTilesetTiles_\w+)\[\]\s*=\s*INCBIN_U32\(\"(data/tilesets/[^\"]+)/tiles\.4bpp", gfx))
    pals = dict(re.findall(r"(gTilesetPalettes_\w+)\[\]\[16\]\s*=\s*\{\s*INCBIN_U16\(\"(data/tilesets/[^\"]+)/palettes/", gfx))
    metas = dict(re.findall(r"(gMetatiles_\w+)\[\]\s*=\s*INCBIN_U16\(\"(data/tilesets/[^\"]+)/metatiles\.bin\"\)",
                            src.text("src/data/tilesets/metatiles.h") or ""))
    m = {}
    for sym, body in re.findall(r"const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\};", src.text("src/data/tilesets/headers.h") or "", re.S):
        f = dict(re.findall(r"\.(tiles|palettes|metatiles)\s*=\s*(\w+)", body))
        if f.get("tiles") in tiles and f.get("palettes") in pals and f.get("metatiles") in metas:
            m[sym] = (tiles[f["tiles"]], pals[f["palettes"]], metas[f["metatiles"]])
    return m


# ================================================================== the story's order, and the maps
ORDER = """PALLET_TOWN ROUTE_1 VIRIDIAN_CITY ROUTE_22 ROUTE_2 VIRIDIAN_FOREST PEWTER_CITY ROUTE_3 MT_MOON ROUTE_4
CERULEAN_CITY ROUTE_24 ROUTE_25 ROUTE_5 UNDERGROUND_PATH ROUTE_6 VERMILION_CITY S_S_ANNE ROUTE_11 DIGLETTS_CAVE ROUTE_9
ROUTE_10 ROCK_TUNNEL POWER_PLANT LAVENDER_TOWN ROUTE_8 ROUTE_7 UNDERGROUND_PATH_2 CELADON_CITY ROCKET_HIDEOUT
POKEMON_TOWER SAFFRON_CITY SILPH_CO ROUTE_12 ROUTE_13 ROUTE_14 ROUTE_15 ROUTE_16 ROUTE_17 ROUTE_18 FUCHSIA_CITY
KANTO_SAFARI_ZONE ROUTE_19 ROUTE_20 SEAFOAM_ISLANDS CINNABAR_ISLAND POKEMON_MANSION ROUTE_21 ONE_ISLAND TREASURE_BEACH
KINDLE_ROAD MT_EMBER EMBER_SPA CAPE_BRINK TWO_ISLAND THREE_ISLAND BOND_BRIDGE THREE_ISLE_PORT BERRY_FOREST
THREE_ISLE_PATH ROUTE_23 KANTO_VICTORY_ROAD INDIGO_PLATEAU POKEMON_LEAGUE FOUR_ISLAND ICEFALL_CAVE FIVE_ISLAND
FIVE_ISLE_MEADOW ROCKET_WAREHOUSE MEMORIAL_PILLAR WATER_LABYRINTH RESORT_GORGEOUS LOST_CAVE SIX_ISLAND WATER_PATH
RUIN_VALLEY DOTTED_HOLE GREEN_PATH OUTCAST_ISLAND PATTERN_BUSH ALTERING_CAVE SEVEN_ISLAND CANYON_ENTRANCE
SEVAULT_CANYON TANOBY_RUINS MONEAN_CHAMBER LIPTOO_CHAMBER WEEPTH_CHAMBER DILFORD_CHAMBER SCUFIB_CHAMBER RIXY_CHAMBER
VIAPOIS_CHAMBER TANOBY_KEY TRAINER_TOWER TRAINER_TOWER_2 CERULEAN_CAVE NEXUS NAVEL_ROCK BIRTH_ISLAND SEVII_ISLE_6
SEVII_ISLE_7 SEVII_ISLE_8 SEVII_ISLE_9 SPECIAL_AREA""".split()
RANK = {"MAPSEC_" + m: i for i, m in enumerate(ORDER)}


def maps_by_layout():
    secnames = {}
    p = os.path.join(GBA, "src/data/region_map/region_map_sections.json")
    if os.path.exists(p):
        secnames = {s["id"]: s.get("name", s["id"]) for s in json.load(open(p))["map_sections"]}
    out = collections.defaultdict(list)
    for mj in sorted(glob.glob(os.path.join(GBA, "data/maps/*/map.json"))):
        d = json.load(open(mj))
        sec = d.get("region_map_section", "")
        outdoor = d.get("map_type") in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE")
        out[d.get("layout")].append(dict(name=os.path.basename(os.path.dirname(mj)), sec=sec,
                                         place=secnames.get(sec, sec).replace("é", "e"),
                                         rank=(RANK.get(sec, 999), 0 if outdoor else 1)))
    return out


# ================================================================== where each door opens
#  a door a script sets (setmetatile) rather than a map: layout, x, y, and the block the script puts there
SCRIPTED = {"rocket_warehouse": ("FiveIsland_Meadow_Layout", 12, 21, 0x2AF)}   # FiveIsland_Meadow/scripts.inc
#  where a door that no map makes a WARP_DOOR still stands, so it can be drawn and reported
SCRIPTED_AT = {v[:3]: v[3] for v in SCRIPTED.values()}
OWN_TILESET = {"hideout_elevator": "gTileset_SilphCo", "silph_co_elevator": "gTileset_SilphCo"}

def find_doors(src, table):
    """{door name: [(rank, map, place, layout, x, y, pair, closed render key)]} for every cell whose block id is that
    door's and whose behaviour (in the tileset that block id belongs to on that map) is WARP_DOOR"""
    lab = labels(src)
    dirs = tileset_dirs(src)
    ids = {lab[d["label"]]: d["name"] for d in table if d["label"] in lab}
    layouts = json.loads(src.text("data/layouts/layouts.json"))["layouts"]
    mbl = maps_by_layout() if not src.vanilla else {}
    ts_cache = {}

    def ts(sym):
        if sym not in ts_cache:
            ts_cache[sym] = Tileset(src, dirs[sym]) if sym in dirs else None
        return ts_cache[sym]

    found = collections.defaultdict(list)
    pairs = {}
    for L in layouts:
        if "blockdata_filepath" not in L:
            continue
        prim, sec = ts(L["primary_tileset"]), ts(L["secondary_tileset"])
        if not prim or not sec or not prim.ok or not sec.ok:
            continue
        bd = src.raw(L["blockdata_filepath"])
        if not bd:
            continue
        key = (L["primary_tileset"], L["secondary_tileset"])
        pair = pairs.setdefault(key, Pair(prim, sec))
        W = L["width"]
        for n in range(len(bd) // 2):
            mid = struct.unpack_from("<H", bd, n * 2)[0] & 0x3FF
            scripted = (L["name"], n % W, n // W) in SCRIPTED_AT
            if scripted:
                mid = SCRIPTED_AT[(L["name"], n % W, n // W)]
            if mid not in ids:
                continue
            warp = pair.behavior(mid) == MB_WARP_DOOR
            own = OWN_TILESET.get(ids[mid])
            if warp or scripted or own == L["secondary_tileset"]:
                ms = mbl.get(L["id"], [])
                m = min(ms, key=lambda q: q["rank"]) if ms else dict(name=L["name"].replace("_Layout", ""), place="?", rank=(999, 9))
                found[ids[mid]].append(dict(rank=m["rank"], map=m["name"], place=m["place"], layout=L["name"],
                                            bd=bd, W=W, H=L["height"], x=n % W, y=n // W, mid=mid, pair=pair, key=key,
                                            warp=warp or scripted, scripted=scripted))
    for k in found:
        #  a door that is a WARP_DOOR somewhere is drawn from there; the own-tileset finds only stand in for a door
        #  no map lets the player open (they are reported as never animating)
        if any(o["warp"] for o in found[k]):
            found[k] = [o for o in found[k] if o["warp"]]
        found[k].sort(key=lambda o: (o["rank"], o["map"], o["y"], o["x"]))
    return found, lab


# ================================================================== rendering a place, and a door's own pixels
def block_at(o, x, y):
    if 0 <= x < o["W"] and 0 <= y < o["H"]:
        return struct.unpack_from("<H", o["bd"], (y * o["W"] + x) * 2)[0] & 0x3FF
    return None


def closed_cells(o, size):
    """the door's closed pixels as the map draws them: 16 wide, 16 or 32 tall, of (row, index, rgb)"""
    cells = [o["mid"]] if size == "1x1" else [block_at(o, o["x"], o["y"] - 1), o["mid"]]
    out = []
    for m in cells:
        out += o["pair"].render(m) if m is not None else [[None] * 16 for _ in range(16)]
    return out


def context_rgb(o, rw=3, up=3, down=1, override=None):
    """the building around a door: (2*rw+1) cells wide, from `up` rows above to `down` below, as RGB. `override`
    is a 16x(16|32) grid of rgb drawn over the door cell (and the one above, if 32 tall)."""
    W, H = (2 * rw + 1) * 16, (up + down + 1) * 16
    img = Image.new("RGB", (W, H), (0, 0, 0))
    px = img.load()
    for j in range(-up, down + 1):
        for i in range(-rw, rw + 1):
            m = block_at(o, o["x"] + i, o["y"] + j)
            if m is None:
                continue
            r = o["pair"].render(m)
            for y in range(16):
                for x in range(16):
                    if r[y][x]:
                        px[(i + rw) * 16 + x, (j + up) * 16 + y] = r[y][x][2]
    if override is not None:
        h = len(override)
        oy = (up + 1) * 16 - h
        for y in range(h):
            for x in range(16):
                if override[y][x] is not None:
                    px[rw * 16 + x, oy + y] = override[y][x]
    return img


# ================================================================== how each door opens (measured by eye from the closed blocks)
#  kind: hinged (hinge "L" or "R"), slide1 (to "L" or "R"), slide2 (leaves part from the middle), lift (slide2, two cells)
#  leaf: the moving part, (x0, y0, x1, y1) inclusive, in the frame's own pixels (16x16, or 16x32 with the door cell below)
#  Anything not listed takes DEFAULT_1x1 / DEFAULT_1x2. "ours" doors are already drawn by their own tools and are left.
DEFAULT_1x1 = dict(kind="hinged", hinge="R", leaf=(2, 1, 13, 14))
DEFAULT_1x2 = dict(kind="lift", leaf=(1, 13, 14, 29))
DOORS = {
    "oaks_lab":               dict(ours="tools/gbalab.py --door"),
    "callow_school":          dict(ours="tools/gbaschoolfront.py"),
    "pokemon_fan_club":       dict(never="its block is the S.S. ANNE's harbour warp, which is not a door: nothing plays it"),
    "general":                dict(kind="hinged", hinge="R", leaf=(2, 0, 13, 14)),
    "pallet":                 dict(kind="hinged", hinge="R", leaf=(2, 1, 13, 14)),
    "sliding_single":         dict(kind="slide1", to="R", leaf=(1, 1, 14, 14)),
    "sliding_double":         dict(kind="slide2", leaf=(1, 1, 14, 14)),
    "silph_co":               dict(kind="slide2", leaf=(1, 0, 14, 13)),
    "dept_store":             dict(kind="slide2", leaf=(1, 0, 14, 13)),
    "safari_zone":            dict(kind="slide2", leaf=(1, 0, 14, 14)),
    "joyful_game_corner":     dict(kind="slide2", leaf=(1, 0, 14, 14)),
    "one_island_poke_center": dict(kind="slide2", leaf=(1, 0, 14, 14)),
    "rocket_warehouse":       dict(kind="slide2", leaf=(2, 1, 13, 14)),
    #  T-447 (the user, 2026-10-24): SCORN SOLUTIONS' glazed door becomes a plain steel one (gbalandmarks.py redraws
    #  block 0x2AD in place, in the cinnabar tileset's row 10). Until that is built the closed door is today's glass
    #  and slides as it always has; once every pixel of the closed door is in row 10, "redrawn" is taken instead --
    #  a hinged steel leaf -- and plan() proposes row 10, so --write sets sDoorAnimPalettes_CinnabarLab to it.
    "cinnabar_lab":           dict(kind="slide1", to="R", leaf=(0, 0, 15, 13),
                                   redrawn=dict(row=10, kind="hinged", hinge="R", leaf=(2, 1, 13, 14),
                                                room_avoid=[(198, 34, 44)])),
    "ss_anne":                dict(kind="hinged", hinge="R", leaf=(2, 13, 13, 30)),
    "teleporter":             dict(kind="slide1", to="L", leaf=(2, 12, 13, 27)),
    "cable_club":             dict(kind="slide1", to="R", leaf=(2, 12, 13, 30)),
    "dept_store_elevator":    dict(kind="lift", leaf=(0, 16, 15, 28)),
}


def redrawn_spec(spec, closed):
    """a door another tool has redrawn (DOORS' "redrawn": the row its new closed block is drawn in, and how that one
    opens) opens the new way only once its closed pixels are all in that row -- before then, as it always has"""
    alt = spec.get("redrawn")
    if alt and all(c[0] == alt["row"] for line in closed for c in line if c):
        spec = dict(spec, **{k: v for k, v in alt.items() if k != "row"})
        spec.pop("to", None)
    return spec


def spec_of(d):
    s = dict(DEFAULT_1x1 if d["size"] == "1x1" else DEFAULT_1x2)
    s.update(DOORS.get(d["name"], {}))
    return s


# ================================================================== colour, in one row
def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def tile_of(x, y):
    """which of a frame's (up to) eight tiles a pixel is in: field_door.c's paletteNums order"""
    return (y // 16) * 4 + ((y % 16) // 8) * 2 + x // 8


class Row:
    """one palette row's fifteen usable colours (index 0 is transparent and never drawn into a door)"""

    def __init__(self, pal, avoid=()):
        self.pal = pal
        self.cols = [(i, pal[i]) for i in range(1, 16)]
        #  the room's colours are chosen from the row less any a door's spec keeps out of it ("room_avoid": T-447's
        #  red is the procedure's light and nothing else, so it may not be the floor of the room behind the door)
        by = sorted([ic for ic in self.cols if tuple(ic[1]) not in {tuple(a) for a in avoid}], key=lambda ic: lum(ic[1]))
        #  the room: the darkest colour, but not pure black where the row has a dark that is not -- a black hole
        #  reads as a hole in the picture, not a room
        dark = [c for _, c in by if lum(c) >= 20]
        self.void = dark[0] if dark and lum(dark[0]) < 90 else by[0][1]
        distinct = [c for _, c in by if dist(c, self.void) > 12 and lum(c) > lum(self.void)]
        self.floor = distinct[0] if distinct else self.void
        lighter = [c for _, c in by if lum(c) > lum(self.floor)] or [self.floor]
        self.spill = min(lighter, key=lambda c: abs(lum(c) - min(255, lum(self.floor) + 40)))   # light at the sill

    def nearest(self, c):
        i, n = min(self.cols, key=lambda ic: (dist(ic[1], c), ic[0]))
        return i, n, dist(n, c)

    def shade(self, c, k=0.72):
        """the row's colour nearest c turned away from the light: darker, and as near its hue as the row allows"""
        key = (c, k)
        if not hasattr(self, "_shade"):
            self._shade = {}
        if key not in self._shade:
            want = tuple(v * k for v in c)
            cands = [n for _, n in self.cols if lum(n) < lum(c) - 4] or [self.void]
            self._shade[key] = min(cands, key=lambda n: dist(n, want))
        return self._shade[key]


# ================================================================== drawing the open frames
def open_frames(closed, rows_of, spec):
    """three RGB frames (lists of rows) from the closed pixels: everything outside the leaf is the closed block's"""
    h = len(closed)
    base = [[closed[y][x][2] if closed[y][x] else rows_of(x, y).void for x in range(16)] for y in range(h)]
    x0, y0, x1, y1 = spec["leaf"]
    lw, lh = x1 - x0 + 1, y1 - y0 + 1
    #  The room is ONE room: its colours come from the row most of the leaf is drawn in, and a tile in another row
    #  shows its nearest to them. Each tile's own darkest (cable_club, 2026-10-22) drew a black square in the one
    #  tile of row 7 inside a room of row 9's slate.
    ref = collections.Counter(tuple(rows_of(x, y).pal) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)).most_common(1)[0][0]
    REF = next(rows_of(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if tuple(rows_of(x, y).pal) == ref)
    if spec.get("room_avoid"):
        REF = Row(REF.pal, avoid=spec["room_avoid"])

    def room(f):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                f[y][x] = REF.spill if y == y1 else REF.floor if y == y1 - 1 else REF.void

    out = []
    kind = spec["kind"]
    for t in (0.4, 0.75, 1.0):
        f = [r[:] for r in base]
        room(f)
        if kind == "hinged":
            w = 2 if t >= 1 else max(3, round(lw * (1 - t)))
            hinge_r = spec.get("hinge", "R") == "R"
            for c in range(w):                                   # c = 0 at the hinge, w-1 the free edge (handle and all)
                k = round(c * (lw - 1) / max(1, w - 1)) if w > 1 else 0
                sx = (x1 - k) if hinge_r else (x0 + k)
                dx = (x1 - c) if hinge_r else (x0 + c)
                drop = 1 if (t >= 0.75 and t < 1 and c >= w // 2) else 0   # the free edge recedes into the room
                for y in range(y0 + drop, y1 + 1):
                    R = rows_of(dx, y)
                    col = R.shade(base[y][sx], 0.85)              # turned a little from the light
                    if t >= 1 or (c == w - 1 and t >= 0.75):
                        col = R.shade(col)                     # edge-on, the leaf is all shadow
                    f[y][dx] = col
        elif kind == "slide1":
            g = round(lw * t)
            right = spec.get("to", "R") == "R"
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    sx = x - g if right else x + g
                    if x0 <= sx <= x1:
                        f[y][x] = base[y][sx]
        else:                                                    # slide2 and lift: two leaves part
            half = lw // 2
            g = round(half * t)
            mid = x0 + half                                      # first column of the right leaf
            for y in range(y0, y1 + 1):
                for x in range(x0, mid):
                    sx = x + g
                    if sx < mid:
                        f[y][x] = base[y][sx]
                for x in range(mid, x1 + 1):
                    sx = x - g
                    if sx >= mid:
                        f[y][x] = base[y][sx]
        out.append(f)
    return out


def quantize(frame, rows_of):
    """(indices, worst error) of an RGB frame in each tile's own row"""
    idx, worst = [], 0
    for y, line in enumerate(frame):
        r = []
        for x, c in enumerate(line):
            i, _, e = rows_of(x, y).nearest(c)
            r.append(i)
            worst = max(worst, e)
        idx.append(r)
    return idx, worst


def fit(closed, rows):
    """how well the closed block's colours are found in rows (one per tile): (pixels off, worst distance)"""
    off, worst = 0, 0
    for y, line in enumerate(closed):
        for x, c in enumerate(line):
            if c is None:
                continue
            e = rows[tile_of(x, y)].nearest(c[2])[2]
            if e > 0:
                off += 1
                worst = max(worst, e)
    return off, worst


# ================================================================== one door, measured and drawn
def plan(d, occ, vpng_cur):
    o = occ[0]
    pair = o["pair"]
    spec = spec_of(d)
    h = 16 if d["size"] == "1x1" else 32
    closed = closed_cells(o, d["size"])
    spec = redrawn_spec(spec, closed)
    looks = {}
    for q in occ:
        k = tuple(tuple(c[2] if c else None for c in r) for r in closed_cells(q, d["size"]))
        looks.setdefault(k, []).append(q)
    rows = [Row(pair.palette(r)) for r in d["rows"]]
    off, worst = fit(closed, rows)
    proposal = None
    if off:
        used = collections.Counter(c[0] for line in closed for c in line if c)
        for r in sorted(set(range(13)), key=lambda r: -used.get(r, 0)):
            if fit(closed, [Row(pair.palette(r))] * 8)[0] == 0:
                proposal = r
                break
        if proposal is not None:
            rows = [Row(pair.palette(proposal))] * 8
        else:
            # field_door.c names a row per TILE: try each tile in the row(s) its own pixels already use
            per = []
            for t in range(8 if d["size"] == "1x2" else 4):
                ys = range((t // 4) * 16 + ((t % 4) // 2) * 8, (t // 4) * 16 + ((t % 4) // 2) * 8 + 8)
                xs = range((t % 2) * 8, (t % 2) * 8 + 8)
                cnt = collections.Counter(closed[y][x][0] for y in ys for x in xs if closed[y][x])
                ok = [r for r, _ in cnt.most_common()
                      if all(Row(pair.palette(r)).nearest(closed[y][x][2])[2] == 0 for y in ys for x in xs if closed[y][x])]
                per.append(ok[0] if ok else None)
            if all(r is not None for r in per):
                proposal = per + per[-4:] * (2 - len(per) // 4) if len(per) < 8 else per
                rows = [Row(pair.palette(r)) for r in proposal]
    rows_of = lambda x, y: rows[tile_of(x, y)]
    new = open_frames(closed, rows_of, spec) if "kind" in spec and not spec.get("ours") else None
    quant = [quantize(f, rows_of) for f in new] if new else None
    # today's frames, as the game draws them: the PNG's indices in field_door.c's rows of this map
    today = []
    if vpng_cur is not None:
        vp = vpng_cur.load()
        for k in range(min(3, vpng_cur.height // h)):
            today.append([[pair.palette(d["rows"][tile_of(x, y)])[vp[x, k * h + y] & 15] for x in range(16)] for y in range(h)])
    return dict(d=d, o=o, occ=occ, spec=spec, h=h, closed=closed, looks=looks, off=off, worst=worst, proposal=proposal,
                rows=rows, new=new, quant=quant, today=today,
                closed_rgb=[[c[2] if c else (0, 0, 0) for c in r] for r in closed])


def vram_clash(p):
    """a secondary tile at 376..383 shares VRAM with the door frames (DOOR_TILE_START), so once a door opens any block
    drawing one shows a door frame until the map reloads: {(map): [(x, y, block)]} for every such cell on a map
    whose door plays these frames"""
    pair = p["o"]["pair"]
    bad = set()
    for k in range(len(pair.sec.meta) // 16):
        if any((t & 0x3FF) >= TILE_START_DOOR for t in struct.unpack_from("<8H", pair.sec.meta, k * 16)):
            bad.add(NUM_PRIMARY + k)
    hits = collections.defaultdict(list)
    seen = set()
    for q in p["occ"]:
        if q["layout"] in seen or q["pair"] is not pair:
            continue
        seen.add(q["layout"])
        for n in range(len(q["bd"]) // 2):
            m = struct.unpack_from("<H", q["bd"], n * 2)[0] & 0x3FF
            if m in bad:
                hits[q["map"]].append((n % q["W"], n // q["W"], m))
    return hits


# ================================================================== the arrow, in the player's row
ARROW_PNG = "graphics/field_effects/pics/arrow.png"
PLAYER_PAL = "graphics/object_events/palettes/player.pal"
A_FILL, A_SHADE, A_OUT = 9, 10, 6            # player.pal: cream, the cream's shadow, the near-black outline


def arrow_frames():
    """north, north, south, south, west, west, east, east -- as the template's eight frames. Two chevrons, the second
    trailing the first; the second frame steps one pixel on, so it beckons rather than bobs."""
    def chev(m, apex, step):
        for k in range(5):                                   # arm rows below the apex
            for th in range(3):
                y = apex + k + th
                for x in (7 - k, 8 + k):
                    if 0 <= y < 16 and 1 <= x <= 14:
                        m[y][x] = 1
    def north(step):
        m = [[0] * 16 for _ in range(16)]
        chev(m, 2 - step, step)
        chev(m, 7 - step, step)                              # rows 7..13: one clear row under it for the outline
        return m
    def rot(m, how):
        if how == "N":
            return m
        if how == "S":
            return m[::-1]
        if how == "W":
            return [[m[x][y] for x in range(16)] for y in range(16)]
        return [row[::-1] for row in rot(m, "W")]                   # E
    out = []
    for how in ("N", "S", "W", "E"):
        for step in (0, 1):
            m = rot(north(step), how)
            f = [[0] * 16 for _ in range(16)]
            for y in range(16):
                for x in range(16):
                    if m[y][x]:
                        below = y + 1 < 16 and m[y + 1][x]
                        f[y][x] = A_FILL if below else A_SHADE
                    elif any(0 <= y + dy < 16 and 0 <= x + dx < 16 and m[y + dy][x + dx]
                             for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        f[y][x] = A_OUT
            out.append(f)
    return out


# ================================================================== contact sheets
S = 3


def font(n):
    for f in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/SFNSMono.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def grid_img(g):
    im = Image.new("RGB", (16, len(g)))
    im.putdata([c for line in g for c in line])
    return im


def strip(p, frames):
    """closed + three frames, each in its 3-cell-wide context, at S"""
    up = 1 if p["h"] == 16 else 2
    tiles = [context_rgb(p["o"], rw=1, up=up, down=1)] + [context_rgb(p["o"], rw=1, up=up, down=1, override=f) for f in frames]
    w, h = tiles[0].width * S, tiles[0].height * S
    im = Image.new("RGB", (4 * w + 3 * 6, h), (24, 24, 28))
    for i, t in enumerate(tiles):
        im.paste(t.resize((w, h), Image.NEAREST), (i * (w + 6), 0))
    return im


def door_panel(p):
    F, f2 = font(14), font(12)
    d, o = p["d"], p["o"]
    big = context_rgb(o, rw=3, up=3 if p["h"] == 16 else 4, down=1)
    big = big.resize((big.width * S, big.height * S), Image.NEAREST)
    today = strip(p, p["today"]) if p["today"] else None
    new = strip(p, p["new"]) if p["new"] else None
    W = big.width + 24 + (new or today).width + 8
    H = 64 + max(big.height, (today.height if today else 0) + (new.height if new else 0) + 44)
    im = Image.new("RGB", (W, H), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    places = sorted({(q["rank"], q["place"]) for q in p["occ"]})
    dr.text((8, 6), "%s  (%s, %s, row %s)" % (d["name"], d["size"], d["sound"], ",".join(map(str, sorted(set(d["rows"]))))),
            fill=(250, 214, 120), font=F)
    dr.text((8, 26), "first: %s (%s) -- %d door cell%s on %d map%s; places: %s" % (
        o["map"], o["place"], len(p["occ"]), "s" if len(p["occ"]) != 1 else "", len({q["map"] for q in p["occ"]}),
        "s" if len({q["map"] for q in p["occ"]}) != 1 else "", ", ".join(pl for _, pl in places[:5]) + (" ..." if len(places) > 5 else "")),
        fill=(200, 200, 210), font=f2)
    dr.text((8, 42), notes_of(p, short=True), fill=(240, 140, 120) if (p["off"] or len(p["looks"]) > 1) else (140, 210, 150), font=f2)
    im.paste(big, (8, 62))
    x = big.width + 24
    y = 62
    if today:
        dr.text((x, y), "TODAY (vanilla frames in this map's palette): closed, ajar, half, open", fill=(200, 200, 210), font=f2)
        im.paste(today, (x, y + 16))
        y += 16 + today.height + 6
    if new:
        dr.text((x, y), "NEW (drawn here): closed, ajar, half, open", fill=(140, 210, 150), font=f2)
        im.paste(new, (x, y + 16))
    return im


def notes_of(p, short=False):
    n = []
    if p["spec"].get("ours"):
        n.append("already ours (%s)" % p["spec"]["ours"])
    if not p["o"]["warp"]:
        n.append("NEVER ANIMATES: no map makes this block a WARP_DOOR")
    if p["o"].get("scripted"):
        n.append("set by a script (setmetatile)")
    if p["off"]:
        if isinstance(p["proposal"], list):
            n.append("PALETTE: no one row draws the closed door; drawn tile by tile in rows %s -- field_door.c's rows must change to that"
                     % p["proposal"][:8 if p["h"] == 32 else 4])
        elif p["proposal"] is not None:
            n.append("PALETTE: row %s cannot draw the closed door (%d px off); drawn in row %d -- field_door.c's row must change to %d"
                     % (",".join(map(str, sorted(set(p["d"]["rows"])))), p["off"], p["proposal"], p["proposal"]))
        else:
            n.append("PALETTE: %d px of the closed door are not in its row (worst %.0f); nearest taken" % (p["off"], p["worst"]))
    if len(p["looks"]) > 1:
        n.append("%d DIFFERENT closed doors share this id; drawn from the first" % len(p["looks"]))
    if p["quant"] and max(q[1] for q in p["quant"]) > 0:
        n.append("frames off-row by %.0f" % max(q[1] for q in p["quant"]))
    if not n:
        n.append("fits its row exactly; frames match the closed block outside the leaf")
    return "; ".join(n)


def arrow_panel(frames, ppal):
    F = font(14)
    van = CUR.png(ARROW_PNG)
    vp = van.load()
    vframes = [[[vp[x, k * 16 + y] for x in range(16)] for y in range(16)] for k in range(8)]
    Z = 6
    im = Image.new("RGB", (8 * (16 * Z + 8) + 16, 2 * (16 * Z + 30) + 40), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), "the door-mat arrow (FLDEFFOBJ_ARROW), in sprite palette 0 = player.pal: N N S S W W E E",
            fill=(250, 214, 120), font=F)
    for r, (label, fr) in enumerate((("TODAY", vframes), ("NEW", frames))):
        y = 30 + r * (16 * Z + 30)
        dr.text((8, y), label, fill=(200, 200, 210), font=font(12))
        for k, f in enumerate(fr):
            cell = Image.new("RGB", (16, 16), (150, 140, 120))       # a mat-coloured ground under it
            for yy in range(16):
                for xx in range(16):
                    if f[yy][xx]:
                        cell.putpixel((xx, yy), ppal[f[yy][xx]])
            im.paste(cell.resize((16 * Z, 16 * Z), Image.NEAREST), (8 + k * (16 * Z + 8), y + 16))
    return im


def stack(panels, path):
    W = max(p.width for p in panels)
    H = sum(p.height for p in panels) + 10 * len(panels)
    im = Image.new("RGB", (W, H), (8, 8, 10))
    y = 0
    for p in panels:
        im.paste(p, (0, y))
        y += p.height + 10
    im.save(path)


# ================================================================== the tileset fixes the frames need (2026-10-22)
#  Applied to the engine by --write --approved BEFORE the frames are drawn, and in report mode to the files as read
#  (CUR's cache), so the report shows the doors as they will be.

def png_bytes(img, bits4):
    b = io.BytesIO()
    if bits4:
        img.save(b, format="PNG", bits=4)
    else:
        img.save(b, format="PNG")
    return b.getvalue()


def put(src, rel, data, changed):
    """change a file in src's cache (and so in everything read after), and remember it for --write"""
    src._cache[rel] = data
    changed[rel] = data


def tile_get(img, i):
    px, W = img.load(), img.width // 8
    return tuple(px[(i % W) * 8 + x, (i // W) * 8 + y] & 15 for y in range(8) for x in range(8))


def tile_put(img, i, t):
    px, W = img.load(), img.width // 8
    for k, v in enumerate(t):
        px[(i % W) * 8 + k % 8, (i // W) * 8 + k // 8] = v


def hflip(t):
    return tuple(t[(i // 8) * 8 + 7 - i % 8] for i in range(64))


def vflip(t):
    return tuple(t[(7 - i // 8) * 8 + i % 8] for i in range(64))


FLIPS = {0: lambda t: t, 0x400: hflip, 0x800: vflip, 0xC00: lambda t: hflip(vflip(t))}


#  ONE door whose CLOSED block was drawn in two rows: gbainterior.py's palette fitter put the cable club door's
#  bottom-right tile in row 7 and the rest of the door in row 9, so its bottom-right quarter was a shade off the rest
#  (the floor line under it a different grey) and no frame could open it in one room colour -- the dark of the
#  doorway came out a square of row 7's nearest. The tile is the door block's alone; it is re-indexed into row 9 by
#  what each colour IS in the door (its light, its glass, its teal, its frame, its sill), read off the tile beside it,
#  not by nearest colour, which would turn the glass grey.
CLOSED_FIX = {
    "cable_club": dict(tileset="data/tilesets/secondary/checkpoint", block=0x2DE, entry=3, rows=(7, 9),
                       remap={2: 1, 6: 5, 11: 14, 14: 15, 12: 12}),
}


def fix_closed(src, changed):
    out = []
    for name, f in CLOSED_FIX.items():
        mrel, trel = f["tileset"] + "/metatiles.bin", f["tileset"] + "/tiles.png"
        meta = bytearray(src.raw(mrel))
        off = ((f["block"] - NUM_PRIMARY) * 8 + f["entry"]) * 2
        e = struct.unpack_from("<H", meta, off)[0]
        if e >> 12 == f["rows"][1]:
            continue                                          # already done
        if e >> 12 != f["rows"][0]:
            raise SystemExit("  %s: block 0x%X entry %d is in row %d, not %d -- the tileset moved; look before fixing"
                             % (name, f["block"], f["entry"], e >> 12, f["rows"][0]))
        t = (e & 0x3FF) - NUM_PRIMARY
        users = [k for k in range(len(meta) // 16) for q in range(8)
                 if (struct.unpack_from("<H", meta, (k * 8 + q) * 2)[0] & 0x3FF) == e & 0x3FF]
        if users != [f["block"] - NUM_PRIMARY]:
            raise SystemExit("  %s: tile %d is drawn by other blocks too (%s) -- it cannot be re-indexed in place"
                             % (name, t, ", ".join("0x%X" % (NUM_PRIMARY + k) for k in users)))
        img = src.png(trel).copy()
        old = tile_get(img, t)
        if set(old) - set(f["remap"]):
            raise SystemExit("  %s: tile %d holds indices %s the remap does not name" % (name, t, sorted(set(old) - set(f["remap"]))))
        tile_put(img, t, tuple(f["remap"][v] for v in old))
        struct.pack_into("<H", meta, off, (e & 0x0FFF) | (f["rows"][1] << 12))
        put(src, trel, png_bytes(img, True), changed)
        put(src, mrel, bytes(meta), changed)
        out.append("  %s: the closed door's tile %d re-indexed from row %d into row %d (block 0x%X entry %d)"
                   % (name, t, f["rows"][0], f["rows"][1], f["block"], f["entry"]))
    return out


#  THE TILES THE FRAMES OVERWRITE. A door's three frames are copied into the BG's last eight tiles (secondary
#  376..383) every time it plays, so any block on that map that draws one of those tiles shows a door frame from then
#  until the map reloads. Every such tile is moved below 376 into a slot found in this order, so nothing anyone sees
#  changes, collision included (T-125):
#    1. a secondary slot no block draws;
#    2. a secondary slot whose every use another of its OWN tiles draws identically in some row (a solid colour is
#       a solid colour in any row that holds it) -- never a tile of the primary, which batches C and D redraw;
#    3. a secondary slot drawn only on BOTTOM layers of COVERED blocks (both layers under the sprites) whose top
#       layer is empty, which the tileset's own tiles redraw as a bottom and a top;
#    4. a slot of the PRIMARY that no block of it or of any secondary loaded with it draws, a leftover ink slot
#       before a blank one (tools that hunt free slots look for blank ones), never an animated one.
ANIMATED = {"gTileset_General": set(range(416, 482)) | set(range(508, 512))}


def layer_type(attr, k):
    return (struct.unpack_from("<I", attr, k * 4)[0] >> 29) & 3 if (k + 1) * 4 <= len(attr) else 0


def move_door_tiles(src, table, changed):
    found, _ = find_doors(src, table)
    dirs = tileset_dirs(src)
    layouts = json.loads(src.text("data/layouts/layouts.json"))["layouts"]
    lab = labels(src)
    protect = {lab[d["label"]] for d in table if d["label"] in lab}         # the doors themselves, and above them
    for d in table:
        if d["size"] == "1x2":
            for o in found.get(d["name"], []):
                m = block_at(o, o["x"], o["y"] - 1)
                if m is not None:
                    protect.add(m)
    pairs = sorted({o["key"] for occ in found.values() for o in occ if o["warp"]})
    out = []
    done = set()
    for prim_sym, sec_sym in pairs:
        if sec_sym in done:
            continue
        done.add(sec_sym)
        sdir, pdir = dirs[sec_sym][2], dirs[prim_sym][2]
        stiles, ptiles = dirs[sec_sym][0], dirs[prim_sym][0]
        mrel = sdir + "/metatiles.bin"
        meta = bytearray(src.raw(mrel))
        attr = src.raw(sdir + "/metatile_attributes.bin") or b""
        nb = len(meta) // 16
        E = lambda k, q: struct.unpack_from("<H", meta, (k * 8 + q) * 2)[0]
        need = sorted({E(k, q) & 0x3FF for k in range(nb) for q in range(8)
                       if TILE_START_DOOR <= (E(k, q) & 0x3FF) < 1024})
        if not need:
            continue
        others = [l for l in layouts if l.get("primary_tileset") == prim_sym and l.get("secondary_tileset") != sec_sym]
        if any(l.get("secondary_tileset") == sec_sym and l.get("primary_tileset") != prim_sym for l in layouts):
            raise SystemExit("  %s is loaded with another primary too; its slots cannot be moved safely" % sec_sym)
        simg, pimg = src.png(stiles + "/tiles.png").copy(), src.png(ptiles + "/tiles.png").copy()
        nsec = (simg.width // 8) * (simg.height // 8)
        tl = lambda i: tile_get(pimg, i) if i < NUM_PRIMARY else tile_get(simg, i - NUM_PRIMARY)
        pal = {r: (src.pal(dirs[prim_sym if r < 7 else sec_sym][1] + "/palettes/%02d.pal" % r) or [(255, 0, 255)] * 16) for r in range(13)}

        def uses_of(i):
            return [(k, q) for k in range(nb) for q in range(8) if (E(k, q) & 0x3FF) == i]

        freed, pinned, plan_lines, repoint = [], set(), [], {}
        # 1. unreferenced secondary slots
        refd = {E(k, q) & 0x3FF for k in range(nb) for q in range(8)}
        free1 = [NUM_PRIMARY + i for i in range(TILE_START_DOOR - NUM_PRIMARY) if NUM_PRIMARY + i not in refd and NUM_PRIMARY + i < NUM_PRIMARY + nsec]
        slots = [(s, "free") for s in free1]

        tcache = {}

        def colours(e):
            if e & 0x3FF not in tcache:
                tcache[e & 0x3FF] = tl(e & 0x3FF)
            t = FLIPS[e & 0xC00](tcache[e & 0x3FF])
            return tuple(pal[e >> 12][v] if v else None for v in t)

        CL = [(i | fl | (r << 12), colours(i | fl | (r << 12)))     # every way the tileset's own tiles can draw
              for i in range(NUM_PRIMARY, min(TILE_START_DOOR, NUM_PRIMARY + nsec)) for fl in FLIPS for r in range(13)]
        by_colour = collections.defaultdict(list)
        for c, v in CL:
            by_colour[v].append(c)

        if len(slots) < len(need):           # 2. a solid colour, or any tile, its own tileset draws identically
            for i in range(NUM_PRIMARY, TILE_START_DOOR):
                if len(slots) >= len(need):
                    break
                us = uses_of(i)
                if not us or i in pinned or any(NUM_PRIMARY + k in protect for k, _ in us):
                    continue
                excl = {i} | {f for f, _ in slots}
                rep = {}
                for k, q in us:
                    want = colours(E(k, q))
                    alt = next((c for c in by_colour.get(want, []) if (c & 0x3FF) not in excl), None)
                    if alt is None:
                        break
                    rep[(k, q)] = alt
                else:
                    if len(rep) == len(us):
                        repoint.update(rep)
                        pinned |= {c & 0x3FF for c in rep.values()}
                        slots.append((i, "drawn by %s instead" % ", ".join(sorted({"%d row %d" % ((c & 0x3FF) - NUM_PRIMARY, c >> 12) for c in rep.values()}))))
        if len(slots) < len(need):           # 3. a bottom and a top, in COVERED blocks with an empty top
            blank = lambda e: not any(tl(e & 0x3FF))
            for i in range(NUM_PRIMARY, TILE_START_DOOR):
                if len(slots) >= len(need):
                    break
                us = uses_of(i)
                if not us or i in pinned or i in {f for f, _ in slots}:
                    continue
                if any(NUM_PRIMARY + k in protect or q >= 4 or layer_type(attr, k) != 1 or not blank(E(k, q + 4)) for k, q in us):
                    continue
                excl = {i} | {f for f, _ in slots}
                cl = [(c, v) for c, v in CL if (c & 0x3FF) not in excl]
                tops = [(c, v) for c, v in cl if None in v and any(x is not None for x in v)]
                bots = [(c, v) for c, v in cl if None not in v]
                rep = {}
                for k, q in us:
                    want = colours(E(k, q))
                    if None in want:
                        break
                    got = None
                    for ct, vt in tops:
                        if any(x is not None and x != y for x, y in zip(vt, want)):
                            continue
                        got = next(((cb, ct) for cb, vb in bots if all(vt[n] is not None or vb[n] == want[n] for n in range(64))), None)
                        if got:
                            break
                    if not got:
                        break
                    rep[(k, q)], rep[(k, q + 4)] = got
                if len(rep) == 2 * len(us):
                    repoint.update(rep)
                    pinned |= {c & 0x3FF for c in rep.values()}
                    slots.append((i, "drawn as a bottom and a top"))
        if len(slots) < len(need):           # 4. the primary's own leftover slots
            pref = set()
            for l in [l for l in layouts if l.get("primary_tileset") == prim_sym]:
                s2 = l.get("secondary_tileset")
                if s2 in dirs:
                    b = src.raw(dirs[s2][2] + "/metatiles.bin") or b""
                    pref |= {struct.unpack_from("<H", b, n * 2)[0] & 0x3FF for n in range(len(b) // 2)}
            pb = src.raw(pdir + "/metatiles.bin") or b""
            pref |= {struct.unpack_from("<H", pb, n * 2)[0] & 0x3FF for n in range(len(pb) // 2)}
            free4 = [i for i in range(1, NUM_PRIMARY) if i not in pref and i not in ANIMATED.get(prim_sym, set())]
            free4.sort(key=lambda i: (not any(tile_get(pimg, i)), i))
            slots += [(i, "the primary's leftover slot") for i in free4[:len(need) - len(slots)]]
        if len(slots) < len(need):
            raise SystemExit("  %s: %d tiles at 376+ and only %d slots to move them to" % (sec_sym, len(need), len(slots)))
        # apply: the freed tiles' uses first, then each needed tile into its slot
        for (k, q), e in repoint.items():
            struct.pack_into("<H", meta, (k * 8 + q) * 2, e)
        moved = {}
        for n, (s, how) in zip(need, slots):
            px = tl(n)
            if s < NUM_PRIMARY:
                tile_put(pimg, s, px)
            else:
                tile_put(simg, s - NUM_PRIMARY, px)
            moved[n] = s
            plan_lines.append("    tile %d -> %s %d (%s)" % (n - NUM_PRIMARY, "primary" if s < NUM_PRIMARY else "slot", s if s < NUM_PRIMARY else s - NUM_PRIMARY, how))
        for k in range(nb):
            for q in range(8):
                e = E(k, q)
                if (e & 0x3FF) in moved:
                    struct.pack_into("<H", meta, (k * 8 + q) * 2, (e & ~0x3FF) | moved[e & 0x3FF])
        for n in need:                                   # the old slots blank, so nothing looks drawn there
            tile_put(simg, n - NUM_PRIMARY, (0,) * 64)
        put(src, mrel, bytes(meta), changed)
        put(src, stiles + "/tiles.png", png_bytes(simg, True), changed)
        if any(s < NUM_PRIMARY for s, _ in slots[:len(need)]):
            put(src, ptiles + "/tiles.png", png_bytes(pimg, True), changed)
        blocks = sorted({NUM_PRIMARY + k for k in range(nb) for q in range(8) if (E(k, q) & 0x3FF) in moved.values()})
        out.append("  %s: %d tile%s at 376+ moved below the door frames (blocks %s):" % (
            sec_sym, len(need), "s" if len(need) > 1 else "", ", ".join("0x%X" % b for b in blocks)))
        out += plan_lines
    return out


def set_door_rows(src, plans, changed):
    """field_door.c's sDoorAnimPalettes_* for every door the report says must change"""
    c = src.text("src/field_door.c")
    out = []
    for p in plans:
        prop = p["proposal"]
        if prop is None or p["spec"].get("ours"):
            continue
        rows = [prop] * 8 if isinstance(prop, int) else list(prop[:8])
        if len(rows) < 8:
            rows += rows[-4:] * ((8 - len(rows)) // 4)
        sym = p["d"]["palsym"]
        new, n = re.subn(r"(sDoorAnimPalettes_%s\[\]\s*=\s*\{)[\d,\s]+(\})" % sym, lambda m: m.group(1) + ", ".join(map(str, rows)) + m.group(2), c)
        if n != 1:
            raise SystemExit("  sDoorAnimPalettes_%s not found in field_door.c" % sym)
        if new != c:
            out.append("  field_door.c: sDoorAnimPalettes_%s %s -> %s" % (sym, p["d"]["rows"], rows))
            c = new
    if out:
        put(src, "src/field_door.c", c.encode(), changed)
    return out


# ================================================================== the run
def indexed(frames_idx, pal, h):
    im = Image.new("P", (16, h * len(frames_idx)))
    im.putpalette([v for c in pal[:16] for v in c])
    px = im.load()
    for k, f in enumerate(frames_idx):
        for y in range(h):
            for x in range(16):
                px[x, k * h + y] = f[y][x]
    return im


def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-438 batch A is a draft until the user has approved its sheets.")
        print("  (Approved 2026-10-22: --write --approved fixes the tilesets the frames need, sets field_door.c's palette rows,")
        print("   and copies the frames into graphics/door_anims/ and the arrow into graphics/field_effects/pics/.)")
        return 0
    table = door_table(CUR)
    changed = {}                                 # rel path -> bytes: the engine files --write puts back
    fixes = fix_closed(CUR, changed) + move_door_tiles(CUR, table, changed)
    found, _ = find_doors(CUR, table)
    order = {n: i for i, n in enumerate(["pallet", "general", "sliding_single", "sliding_double"])}
    plans = []
    for d in table:
        occ = found.get(d["name"])
        if not occ:
            print("  %-28s no map has it as a door -- %s" % (d["name"], spec_of(d).get("never", "nothing plays it")))
            continue
        plans.append(plan(d, occ, CUR.png(d["png"])))
    plans.sort(key=lambda p: (order.get(p["d"]["name"], 9), p["o"]["rank"], p["d"]["name"]))

    print("  %-28s %-4s %-7s %-34s %5s  %s" % ("door", "size", "row", "first seen", "cells", "notes"))
    for p in plans:
        print("  %-28s %-4s %-7s %-34s %5d  %s" % (p["d"]["name"], p["d"]["size"], ",".join(map(str, sorted(set(p["d"]["rows"])))),
                                                (p["o"]["map"] + " (" + p["o"]["place"] + ")")[:34], len(p["occ"]), notes_of(p)))
    for p in plans:
        for m, cells in vram_clash(p).items():
            print("  !! %s: %d cell%s on %s draw a tile the door frames overwrite in VRAM (first %s, block 0x%X)"
                  % (p["d"]["name"], len(cells), "s" if len(cells) > 1 else "", m, cells[0][:2], cells[0][2]))
    fixes += set_door_rows(CUR, plans, changed)
    for line in fixes:
        print(line)
    ppal = read_pal(os.path.join(GBA, PLAYER_PAL))
    arrows = arrow_frames()
    drawn = [p for p in plans if p["quant"] and not p["spec"].get("ours")]
    print("  %d doors drawn, %d already ours, the arrow in player.pal (%d frames)" % (len(drawn), sum(1 for p in plans if p["spec"].get("ours")), len(arrows)))

    if DRAFT:
        os.makedirs(DRAFT, exist_ok=True)
        os.makedirs(SHEETS, exist_ok=True)
        for p in drawn:
            pal = p["rows"][0].pal
            indexed([q[0] for q in p["quant"]], pal, p["h"]).save(os.path.join(DRAFT, p["d"]["name"] + ".png"))
        indexed(arrows, ppal, 16).save(os.path.join(DRAFT, "arrow.png"))
        panels = [door_panel(p) for p in plans if p["new"] or p["today"]]
        names = []
        for i in range(0, len(panels), 6):
            path = os.path.join(SHEETS, "t438a_doors_%d.png" % (i // 6 + 1))
            stack(panels[i:i + 6], path)
            names.append(path)
        path = os.path.join(SHEETS, "t438a_doors_arrow.png")
        arrow_panel(arrows, ppal).save(path)
        names.append(path)
        print("  drafts in %s; sheets:\n    %s" % (DRAFT, "\n    ".join(names)))

    if WRITE:
        for rel, data in sorted(changed.items()):
            open(os.path.join(GBA, rel), "wb").write(data)
            print("  written: %s" % rel)
        for p in drawn:
            pal = p["rows"][0].pal
            indexed([q[0] for q in p["quant"]], pal, p["h"]).save(os.path.join(GBA, p["d"]["png"]), bits=4)
        indexed(arrows, ppal, 16).save(os.path.join(GBA, ARROW_PNG), bits=4)
        print("  written: %d door animations and the arrow into the engine" % len(drawn))
    return 0


if __name__ == "__main__":
    sys.exit(main())
