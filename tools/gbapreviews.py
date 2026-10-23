#!/usr/bin/env python3
"""T-445: the map preview screens -- the picture a cave (or a forest, the tower, a hideout) shows as it is entered.

    python3 tools/gbapreviews.py                         # report: every preview, the mapsecs that show it, the name
                                                         #   the game prints on it, and which T-438 batch E covered
    python3 tools/gbapreviews.py --draft [DIR]           # draft the batch E caves' previews into DIR (gfx/drafts/t445/),
                                                         #   and the contact sheets; --sheets DIR puts the sheets elsewhere
    python3 tools/gbapreviews.py --paint [CAVE ...]      # PAINT each cave's mouth on the sprite server (spriteforge.py,
                                                         #   roverbyteseer:8008): gfx/drafts/t445/<cave>/painted.png and
                                                         #   its record, from a start image graded out of vanilla's
                                                         #   picture in the cave's colours (painted_init.png)
    python3 tools/gbapreviews.py --draft --top-down      # the old top-down drafts, even where a painting exists
    python3 tools/gbapreviews.py --write --approved      # into the engine (graphics/map_preview/<cave>/tiles.png,
                                                         #   tilemap.bin, and the -num_tiles line in graphics_file_rules.mk).
                                                         #   OTHER CAVE's light1..3.pal too. Without --approved it refuses.

HOW THE ENGINE DRAWS ONE (src/map_preview_screen.c). sMapPreviewScreenData maps a MAPSEC to three files in
graphics/map_preview/<name>/: tiles.4bpp.lz (from tiles.png, `-num_tiles N` in graphics_file_rules.mk), tilemap.bin.lz
(a 32x20 BG map, committed binary) and tiles.gbapal (from tiles.png's own 32-colour palette). MapPreview_LoadGfx loads
the palette into BG palettes 13 and 14 and the tiles to BG0 from tile 0; the picture is the screen's rows 3..16
(240x112) in palette 13, and rows 0..2 and 17..19 -- the black letterbox and the white name banner drawn in tiles --
are palette 14. Columns 30 and 31 are off screen (palette 0, tile 0).

THE NAME IS NOT IN THE PICTURE. MapPreview_CreateMapNameWindow prints GetMapName(mapsec) -- our region_map_sections
name, DEADSTACK, OTHER CAVE -- into a 13x2-tile window at (0,0) (baseBlock 0x1C2, so the picture's tiles must stay
below 450), centred in 104px, in palette 14's colours 1 (fill), 2 (text) and 3 (shadow). So a preview needs no name
drawn into it, and the DAEMONS names already show on vanilla's pictures; the sheet here prints them in the game's own
font (graphics/fonts/latin_normal.png) so the draft is seen as a player would see it. A name wider than 104px would
start off the window's left edge (xctr is u32): the report checks every one.

WHAT A DRAFT IS. Vanilla's pictures are painted landscapes; ours are drawn from the caves as they now are (T-438
batch E): the cave's map rendered from its layout with the built tilesets (reviewsheet.py's renderer, the same that
draws every map sheet), a characteristic window of it chosen -- the 15x7-metatile window of the cave's maps with the
most different blocks, the least bare floor and the least void (an 8x4 window doubled where the rooms are too
small), or the one VIEW names -- and reduced
to 15 colours in palette 13 (index 0 is left as vanilla's: BG0's colour 0 is transparent). Palette 14 and every tile
of the letterbox and banner are vanilla's, byte for byte, so the name window looks exactly as it did.

PAINTED, NOT TOP-DOWN (the user, 2026-10-23: "painted entrances, not top-down -- the sprite server paints each
cave's mouth at 512 from these views, in each cave's colours"). Where gfx/drafts/t445/<cave>/painted.png exists it is
the picture: --paint makes it. Its start image is vanilla's own painting (for the composition -- a mouth in a slope,
a sea or a sky beyond), every region of it graded through the cave's colours (PAINT's ramps, by luminance: rock,
sky, foliage, water), and the top-down view's light laid faintly into the rock so the cave's motif is in the paint
(the stack's courses, the outage's columns). The server repaints that at 1088x512 (its wide size, 512 high) with
the cave's prompt, image to image, at a denoise low enough that vanilla's composition survives. The painting is
then fitted to 240x112 and reduced as the top-down view was: 15 colours, under 450 tiles (vanilla's banner is 7
tiles, the picture at most 420, so a painting always fits).

OTHER CAVE'S FOUR LIGHTS. Its preview is ONE set of tiles and FOUR palettes 13: the teal painting's colours that
are its crystal (teal) or its rock (mauve) are moved onto each light's own ramps (the tileset's palettes_other_1..3,
by luminance), the sky and sea kept. --draft writes light1..3.pal beside tiles.png and a preview per light, and
--write writes them into graphics/map_preview/altering_cave/ (the user, 2026-10-23: the preview follows the light).
MapPreview_LoadGfx lays the light's palette over palette 13 -- and the preview runs BEFORE the map's ON_TRANSITION
steps VAR_OTHER_CAVE_LIGHT (fldeff_flash.c's CB2_DoChangeMap shows it, then CB2_LoadMap2's LoadMapFromWarp runs the
script), so the light it shows is the coming visit's, VarGet(VAR_OTHER_CAVE_LIGHT) % 4, not fieldmap.c's
(visit - 1) % 4.

WHAT IS NOT DRAFTED: DOLDRUM CAVE (cerulean_cave -- its look waits on the user, T-251) and the TANOBY chambers
(monean_chamber -- batch G), and the previews that are not caves (forests, the tower, the mansion, SILPH, the hideout
and the warehouse, the SAFARI): T-445 is the caves, and those wait on their own batches. The report lists them all.
"""
import argparse, collections, contextlib, io, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx", "drafts", "t445")
MPS = os.path.join(GBA, "graphics/map_preview")
RULES = os.path.join(GBA, "graphics_file_rules.mk")

argv, sys.argv = sys.argv, sys.argv[:1]          # reviewsheet reads sys.argv on import
try:
    with contextlib.redirect_stdout(io.StringIO()):
        import reviewsheet as RS
finally:
    sys.argv = argv
import fontwidth

ap = argparse.ArgumentParser()
ap.add_argument("--draft", nargs="?", const=DRAFT_DEFAULT)
ap.add_argument("--sheets")
ap.add_argument("--paint", nargs="*")
ap.add_argument("--top-down", action="store_true", dest="top_down")
ap.add_argument("--write", action="store_true")
ap.add_argument("--approved", action="store_true")
A = ap.parse_args()

# the caves T-438 batch E redrew (gbacaves.py: approved 2026-10-23, BUILT engine 2007d739f) -> their tileset look
BATCH_E = {
    "mt_moon": "cave (THE STACK)",
    "lost_cave": "cave (THE STACK, kept by THE WRONG WAY)",
    "victory_road": "cave/umbral (the stack in violet dusk, a palette split)",
    "digletts_cave": "digletts_cave (THE LINE)",
    "rock_tunnel": "rock_tunnel (THE OUTAGE)",
    "altering_cave": "rock_tunnel/other (the outage in OTHER CAVE's light, four of them in turn)",
    "power_plant": "power_plant (STILL RUNNING)",
    "seafoam_islands": "seafoam_islands (THE BLOOM)",
    "icefall_cave": "seafoam_islands/stillfall (the bloom gone glassy, a palette split)",
    "mt_ember": "mt_ember (EMBER UNDER ASH)",
    "dotted_hole": "navel_rock (BRAILLE)",
}
NOT_DRAFTED = {
    "cerulean_cave": "DOLDRUM CAVE: its look waits on the user (T-251, gbacaves.py), so its preview does too",
    "monean_chamber": "the TANOBY chambers (seven mapsecs share it): their tileset is batch G's",
    "viridian_forest": "a forest, not a cave (and PATTERN BUSH shares it): its own batch",
    "berry_forest": "a forest, not a cave: its own batch",
    "pokemon_tower": "the tower: its own batch",
    "pokemon_mansion": "the mansion: its own batch",
    "silph_co": "SILPH: its own batch",
    "rocket_hideout": "the hideout: its own batch",
    "rocket_warehouse": "the warehouse: its own batch",
    "safari_zone": "the SAFARI: its own batch",
}

# a view chosen by eye where the search would pick a duller one: (map, x0, y0) in metatiles, a 15x7 window at 1x
# or (map, x0, y0, 8) for an 8x4 window doubled. None of these is required; the search covers the rest.
VIEW = {
}
WIN_W, WIN_H = 15, 7          # metatiles in a 240x112 picture at 1x
LIGHT_NAMES = ["teal", "AMBER in slate", "CHRYSOPRASE in brown jasper", "ROSE QUARTZ in green schist"]


# the painted previews (T-445, the user's answer): each cave's colours as ramps, dark to light, that vanilla's
# picture is graded through by region (rock takes the light parts too unless "white" has a ramp of its own, as
# SMOULDER's steam and snow do, gone to ash); "motif" lays the cave's one idea into it (MOTIFS);
# "skygrad" lays the sky as a top-to-bottom gradient instead (dusk, night, ash haze); "tex" is how strongly the
# top-down view's light is laid into the rock. "prompt" is the cave's, "seed" and "denoise" the painting picked.
PAINT_SIZE = (1088, 512)
PAINT_STYLE = "pixel art, 16-bit game background, wide scene, %s, soft clean pixel shading"
PAINT_NEG = ("text, letters, words, watermark, signature, logo, person, character, creature, animal, frame, border, "
             "blurry, photo, 3d render, ui, slime, neon, oversaturated")
STACK = [(24, 40, 32), (40, 56, 48), (64, 88, 72), (96, 120, 104), (128, 152, 128), (168, 184, 160), (200, 208, 184)]
ASH = [(64, 52, 40), (96, 82, 64), (140, 124, 96)]
PAINT = {
    "mt_moon": dict(rock=STACK, motif=["courses"], sky=[(176, 172, 150), (226, 220, 196)], skygrad=1, leaf=ASH,
                    seed=4452, denoise=0.5,
                    prompt="a dark cave mouth in a rocky hill, the rock is layered thin slabs like stacked old circuit "
                           "boards and drive casings, thin tarnished gold connector strips along some layers, muted "
                           "sage green and dull solder mask green, ash brown dusty ground, pale hazy sky"),
    "lost_cave": dict(rock=STACK, motif=["courses"], leaf=ASH, seed=4451, denoise=0.5,
                      prompt="a dark cave mouth in a slope of layered slab rock by a calm sea, the rock layered like "
                             "stacked old circuit boards, muted sage green and solder mask green, ash brown ground, "
                             "pale sky over the sea"),
    "victory_road": dict(rock=[(40, 32, 72), (64, 56, 104), (96, 80, 136), (128, 112, 168), (160, 144, 192),
                               (192, 184, 216)],
                         sky=[(72, 56, 120), (214, 150, 160)], skygrad=1,
                         leaf=[(20, 18, 40), (40, 36, 72), (70, 62, 108)], seed=4452, denoise=0.5,
                         prompt="a cave entrance in a rocky cliff framed by a tall ruined stone gateway with pillars, "
                                "pine trees in silhouette, cold violet dusk, lavender and deep violet rock in stacked "
                                "layers, a rose glow low on the horizon, evening sky"),
    "digletts_cave": dict(rock=[(32, 24, 32), (64, 40, 32), (96, 72, 48), (136, 104, 64), (168, 128, 80),
                                (200, 152, 104), (224, 192, 136)],
                          leaf=[(48, 56, 24), (88, 96, 40), (136, 136, 64)], motif=["cable"],
                          water=[(14, 10, 14), (40, 28, 28)], seed=4453, denoise=0.5,
                          prompt="a burrow entrance under a ridge of packed earth, a bright red cable with a dark core "
                                 "running along the top edge of the earth bank, umber and ochre earth, warm brown tree "
                                 "trunks behind, ferns in front"),
    "rock_tunnel": dict(rock=[(12, 12, 30), (32, 32, 64), (48, 48, 88), (64, 64, 112), (88, 88, 136), (112, 112, 160),
                              (136, 144, 184)],
                        sky=[(10, 12, 36), (40, 48, 96)], skygrad=1,
                        leaf=[(12, 26, 34), (24, 46, 56), (40, 64, 76)], motif=["columns"], seed=4451, denoise=0.5,
                        prompt="a cave mouth at the foot of a cliff of tall basalt columns at night, deep indigo and "
                               "blue-black, cold moonless night sky, faint blue rim light, dark shrubs, no light "
                               "inside the cave"),
    "altering_cave": dict(rock=[(60, 46, 56), (108, 88, 100), (128, 106, 116), (148, 124, 132), (166, 142, 148),
                                (184, 160, 164), (214, 196, 198)], motif=["crystals"], seed=4452, denoise=0.5,
                          prompt="a cave mouth in mauve rose-grey rock by the sea, pale teal mineral crystals growing "
                                 "as columns out of the rock, glinting teal crystal clusters, blue sea and sky"),
    "power_plant": dict(rock=[(20, 26, 36), (48, 56, 72), (88, 104, 120), (120, 136, 152), (160, 176, 200),
                              (200, 212, 204)],
                        sky=[(88, 104, 120), (200, 212, 204)], leaf=[(40, 80, 40), (80, 128, 72), (128, 200, 104)],
                        motif=["lights"], seed=4452, denoise=0.5,
                        prompt="interior of an old power plant still running, machine housings and steel floor "
                               "plates, small bright green status lights on every machine, moss growing along the "
                               "seams of the floor, cool grey-blue metal and plant green, light from a high window"),
    "seafoam_islands": dict(rock=[(40, 72, 104), (64, 120, 152), (88, 152, 176), (136, 184, 192), (184, 208, 208),
                                  (236, 244, 236)],
                            leaf=[(48, 104, 112), (88, 152, 160), (150, 200, 200)], seed=4452, denoise=0.5,
                            prompt="a cave mouth in icy rocks by the sea, the ice covered with a powdery blue-green "
                                   "frosted bloom, chalky pale tops, clear deep blue-green faces, sea and sky"),
    "icefall_cave": dict(rock=[(24, 48, 88), (32, 80, 136), (48, 112, 168), (80, 152, 200), (128, 184, 216),
                               (176, 224, 240), (236, 250, 250)],
                         leaf=[(40, 88, 120), (80, 140, 180), (150, 200, 220)], motif=["mouth"],
                         mouth=(172, 112, 54, 46), seed=4455, denoise=0.5,
                         neg="icicles over the opening, closed wall",
                         prompt="a big dark cave mouth opening black at the foot of an ice cliff, right beside a "
                                "frozen waterfall, the waterfall turned to clear glassy ice hanging still down the "
                                "cliff, cold blue ice, pale winter sky, frosted shrubs"),
    "mt_ember": dict(rock=[(20, 14, 14), (40, 30, 30), (60, 46, 44), (84, 66, 60), (116, 96, 84), (170, 152, 134)],
                     white=[(150, 140, 130), (214, 204, 190)], motif=["cracks"],
                     peak=((80, 10, 200, 80), [(52, 48, 48), (84, 80, 78), (112, 106, 100), (132, 126, 118)]),
                     water=[(8, 4, 4), (28, 18, 18)], sky=[(150, 132, 120), (214, 198, 170)], skygrad=1,
                     seed=4451, denoise=0.45, neg="snow, snowy peak, snow cap, ice, white mountain",
                     prompt="a cave mouth in black cinder rock, cracks in the rock glowing low orange from inside "
                            "like banked coals, no flames, white steam rising, grey ash drifts, a smouldering "
                            "charcoal grey volcano behind, its slopes dark ash grey, under an ash haze"),
    "dotted_hole": dict(rock=[(72, 56, 48), (120, 96, 72), (160, 128, 96), (192, 168, 128), (216, 192, 160),
                              (240, 224, 192)],
                        leaf=[(80, 96, 48), (120, 136, 64), (168, 176, 96)], motif=["braille"], post=["braille"], seed=4451,
                        denoise=0.4,
                        neg="studs, pyramids, spikes, rivets, bolts, grid of squares",
                        prompt="a cave mouth in a sandstone mound framed by two pale stone pillars, lines of braille "
                               "carved on the stone, small round raised dots in separate cells of six, two columns "
                               "of three, a gap between cells, warm sandstone and shadow, clear sky"),
}


# ================================================================== reading the engine
def previews():
    """[(MPS key, MAPSEC, type, folder)] from sMapPreviewScreenData, in its order"""
    src = open(os.path.join(GBA, "src/map_preview_screen.c")).read()
    var2dir = dict(re.findall(r"static const u8 (s\w+?)MapPreviewTiles\[\] = INCBIN_U8\(\"graphics/map_preview/(\w+)/", src))
    out = []
    for key, body in re.findall(r"\[(MPS_\w+)\]\s*=\s*\{(.*?)\}", src, re.S):
        sec = re.search(r"\.mapsec = (\w+)", body).group(1)
        typ = re.search(r"\.type = (\w+)", body).group(1)
        var = re.search(r"\.tilesptr = (s\w+?)MapPreviewTiles", body).group(1)
        out.append((key, sec, typ, var2dir[var]))
    return out


def names():
    d = json.load(open(os.path.join(GBA, "src/data/region_map/region_map_sections.json")))["map_sections"]
    return {s["id"]: s.get("name", "") for s in d}


def maps_of(mapsec):
    out = []
    root = os.path.join(GBA, "data/maps")
    for m in sorted(os.listdir(root)):
        p = os.path.join(root, m, "map.json")
        if os.path.exists(p) and json.load(open(p)).get("region_map_section") == mapsec:
            out.append(m)
    return out


def name_width(s):
    w, cm = fontwidth.font()
    return sum(w[cm[c]] if c in cm and cm[c] < len(w) else 0 for c in s)


def _pret(rel):
    """a file as pret ships it (upstream/master), never the working tree's: once --write has run, the engine's own
    graphics/map_preview/<cave>/ holds OUR picture, and reading that back as 'vanilla' would make every later run
    grade, reduce and light from our own output (the tool would drift from itself)"""
    import subprocess
    r = subprocess.run(["git", "-C", os.path.realpath(GBA), "show", "upstream/master:" + rel], capture_output=True)
    if r.returncode:
        sys.exit("  !! git show upstream/master:%s failed: %s" % (rel, r.stderr.decode().strip()))
    return r.stdout


def vanilla(folder):
    """(tiles [64 indices each], tilemap entries [640], palette [32 rgb]) as pret's build makes them: its tiles.png
    cut into 8x8 tiles row by row (the first -num_tiles of them, each index's low nibble, as gbagfx keeps it), its
    tilemap.bin, and the png's palette at the GBA's 5 bits"""
    im = Image.open(io.BytesIO(_pret("graphics/map_preview/%s/tiles.png" % folder)))
    n = int(re.search(r"/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles (\d+)" % folder,
                      _pret("graphics_file_rules.mk").decode()).group(1))
    px, (W, H) = im.load(), im.size
    tiles = []
    for ty in range(H // 8):
        for tx in range(W // 8):
            tiles.append([px[tx * 8 + x, ty * 8 + y] & 15 for y in range(8) for x in range(8)])
    pal = im.getpalette()[:96]
    pal = [((pal[i] >> 3) << 3, (pal[i + 1] >> 3) << 3, (pal[i + 2] >> 3) << 3) for i in range(0, 96, 3)]
    m = list(struct.unpack("<640H", _pret("graphics/map_preview/%s/tilemap.bin" % folder)))
    return tiles[:n], m, pal


def compose(tiles, m, pal):
    """the 240x160 screen these make (palettes 13 and 14 from pal)"""
    im = Image.new("RGB", (240, 160))
    px = im.load()
    for ty in range(20):
        for tx in range(30):
            e = m[ty * 32 + tx]
            t, hf, vf, p = tiles[e & 0x3FF] if (e & 0x3FF) < len(tiles) else [0] * 64, e & 0x400, e & 0x800, e >> 12
            base = (p - 13) * 16 if p in (13, 14) else 16
            for y in range(8):
                for x in range(8):
                    c = t[(7 - y if vf else y) * 8 + (7 - x if hf else x)]
                    px[tx * 8 + x, ty * 8 + y] = pal[base + c]
    return im


# ================================================================== the font, for the sheet
_FONT = None


def draw_name(im, name, pal):
    """MapPreview_CreateMapNameWindow: a 104x16 window at (0,0) filled with colour 1 of palette 14, the name centred,
    text colour 2 and shadow 3 -- drawn with the game's own glyphs"""
    global _FONT
    if _FONT is None:
        _FONT = Image.open(os.path.join(GBA, "graphics/fonts/latin_normal.png"))
    w, cm = fontwidth.font()
    p14 = pal[16:32]
    #  the window's colours: fill TEXT_COLOR_WHITE (1), text TEXT_COLOR_RED (4 -- black in this palette), shadow
    #  TEXT_COLOR_LIGHT_GRAY (3); the font sheet draws its glyph in 1, its shadow in 2, its cell in 3
    ink = {1: p14[4], 2: p14[3]}
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 103, 15), fill=p14[1])
    x = (104 - name_width(name)) // 2
    px, fp = im.load(), _FONT.load()
    for ch in name:
        b = cm.get(ch)
        if b is None:
            continue
        gx, gy = (b % 16) * 16, (b // 16) * 16
        for yy in range(16):
            for xx in range(min(16, w[b])):
                v = fp[gx + xx, gy + yy]
                X, Y = x + xx, 2 + yy
                if v in ink and 0 <= X < 104 and Y < 16:
                    px[X, Y] = ink[v]
        x += w[b]


# ================================================================== painting (T-445: painted entrances)
def _lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def _region(c):
    """what a pixel of vanilla's painting is: rock (and the ground), white (a lit rock or a cloud), leaf, sky, water"""
    import colorsys
    h, sat, v = colorsys.rgb_to_hsv(*[x / 255 for x in c])
    h *= 360
    if sat < 0.12 and v > 0.85:
        return "white"
    if 75 <= h <= 170 and sat > 0.2:
        return "leaf"
    if 180 <= h <= 250 and sat > 0.15:
        return "sky" if v > 0.75 else "water"
    return "rock"


def _ramp(r, t):
    t = min(max(t, 0.0), 1.0) * (len(r) - 1)
    i = min(int(t), len(r) - 2)
    f = t - i
    return tuple(int(r[i][k] + (r[i + 1][k] - r[i][k]) * f) for k in range(3))


def paint_init(folder, sec):
    """the start image: vanilla's picture (rows 3..16) graded through the cave's ramps, the top-down view's light laid
    faintly into the rock, at the painting's size"""
    c = PAINT[folder]
    vt, vm, vpal = vanilla(folder)
    v = compose(vt, vm, vpal).crop((0, 24, 240, 136))
    td, _ = picture(folder, sec, painted=False)
    px, dp = v.load(), td.convert("RGB").load()
    W, H = v.size
    lums = collections.defaultdict(list)
    for y in range(H):
        for x in range(W):
            lums[_region(px[x, y])].append(_lum(px[x, y]))
    rng = {k: (min(l), max(l)) for k, l in lums.items()}
    rock_lo, rock_hi = rng["rock"][0], max(rng["rock"][1], rng.get("white", (0, 0))[1])
    dl = [_lum(dp[x, y]) for y in range(H) for x in range(W)]
    mu = sum(dl) / len(dl)
    sd = (sum((l - mu) ** 2 for l in dl) / len(dl)) ** 0.5 or 1
    out = v.copy()
    op = out.load()
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            k = _region(p)
            if k == "white":
                if c.get("white") == "keep":
                    continue
                if not isinstance(c.get("white"), list):
                    k = "rock"
            r = c.get(k)
            pk = c.get("peak")
            if pk and k in ("white", "rock") and pk[0][0] <= x < pk[0][2] and pk[0][1] <= y < pk[0][3] \
                    and _region(p) == "white":
                op[x, y] = _ramp(pk[1], (_lum(p) - 200) / 55)        # the far peak in ash, never snow
                continue
            if not r:
                continue
            if k == "sky" and c.get("skygrad"):
                op[x, y] = _ramp(r, y / H)
                continue
            lo, hi = (rock_lo, rock_hi) if k == "rock" else rng[k]
            if k == "white":
                lo = min(lo, 200)
            t = (_lum(p) - lo) / max(1, hi - lo)
            if k == "rock":
                t += c.get("tex", 0.22) * (_lum(dp[x, y]) - mu) / sd / 3
            op[x, y] = _ramp(r, t)
    for m in c.get("motif", []):
        MOTIFS[m](out, v, c)
    return out.resize(PAINT_SIZE, Image.BICUBIC)


#  the cave's one idea, laid into the start image at 2px so it survives the painting (the server's own pixel is
#  about 8px at 1088, near 2px here): what the top-down view says in tiles, said where the painting can keep it
def _rockmask(v, ymin=0):
    px = v.load()
    return lambda x, y: (0 <= x < 240 and ymin <= y < 112 and _region(px[x, y]) in ("rock", "white")
                         and _lum(px[x, y]) > 80 and px[x, y][2] <= px[x, y][0] + 6)     # not a pale sky


def _shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def motif_courses(out, v, c):
    """THE STACK: thin courses of slab, every other a shade darker, a joint now and then, a gold connector strip"""
    import random
    rnd, op, rock = random.Random(445), out.load(), _rockmask(v)
    for x in range(240):
        off = (x // 22) * 3 % 7
        for y in range(112):
            if not rock(x, y):
                continue
            ph = (y + off) % 7
            band = ((y + off) // 7) % 2
            if ph == 0:
                op[x, y] = _shade(op[x, y], 0.55)
            elif ph == 1:
                gold = (x // 11 * 7 + (y + off) // 7 * 13) % 9 == 0
                op[x, y] = (196, 164, 76) if gold else _shade(op[x, y], 1.18)
            elif band:
                op[x, y] = _shade(op[x, y], 0.9)
        if x % 22 == 0:
            for y in range(112):
                if rock(x, y) and rnd.random() < 0.5:
                    op[x, y] = _shade(op[x, y], 0.6)


def motif_cable(out, v, c):
    """THE LINE: the buried cable along the top of the bank, a red sheath over a dark core"""
    px, op = v.load(), out.load()
    for x in range(240):
        for y in range(14, 80):
            if _region(px[x, y]) == "leaf":
                for k, col in enumerate([(220, 110, 80), (192, 80, 56), (150, 56, 40), (48, 24, 24)]):
                    if y + 2 + k < 112:
                        op[x, y + 2 + k] = col
                break


def motif_columns(out, v, c):
    """THE OUTAGE: basalt cut in tall columns, a lit left edge and a dark right one; the mouth gone fully black"""
    px, op, rock = v.load(), out.load(), _rockmask(v)
    for y in range(112):
        for x in range(240):
            if _region(px[x, y]) in ("rock", "water") and _lum(px[x, y]) < 80 and y > 50:
                op[x, y] = (4, 4, 14)
            elif rock(x, y):
                ph = (x + (y // 40) * 4) % 10
                if ph in (0, 1):
                    op[x, y] = _shade(op[x, y], 1.35)
                elif ph in (8, 9):
                    op[x, y] = _shade(op[x, y], 0.5)


def motif_crystals(out, v, c):
    """OTHER CAVE: teal mineral columns grown out of the mauve rock"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v, 30)
    d = ImageDraw.Draw(out)
    placed = 0
    while placed < 14:
        x, y = rnd.randrange(130, 236), rnd.randrange(34, 104)
        if not rock(x, y):
            continue
        placed += 1
        for k in range(rnd.randint(2, 3)):
            cx, h, w = x + k * 5 - 4, rnd.randint(8, 18), 4
            top = y - h
            d.polygon([(cx, y), (cx, top + 2), (cx + w // 2, top), (cx + w, top + 2), (cx + w, y)], fill=(104, 160, 152))
            d.rectangle((cx, top + 2, cx + 1, y), fill=(168, 216, 208))
            d.line((cx + w, top + 2, cx + w, y), fill=(40, 70, 72))


def motif_cracks(out, v, c):
    """EMBER UNDER ASH: cracks that glow low orange from inside, never flame"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v, 20)
    px = v.load()
    n = 0
    while n < 16:
        x, y = rnd.randrange(0, 240), rnd.randrange(20, 112)
        if not (rock(x, y) or _region(px[x, y]) == "rock") or _lum(op[x, y]) > 70:      # the near rock, not the far
            continue
        n += 1
        for _ in range(rnd.randint(14, 30)):
            for dx, col in ((-1, (150, 56, 28)), (0, (252, 184, 72)), (1, (236, 128, 40)), (2, (150, 56, 28))):
                if 0 <= x + dx < 240 and 0 <= y < 112:
                    op[x + dx, y] = col
            x += rnd.choice((-1, 0, 1))
            y += rnd.choice((0, 1, 1))
            if not (0 <= x < 239 and y < 111):
                break


def motif_braille(out, v, c):
    """BRAILLE: lines of six-dot cells over the stone, writing for the hand -- round dots (a 4px disc, lit above, shadowed
    below), two columns of three, a wide gap between cells and between lines, so each cell reads as a cell and not a
    grid of studs; every cell has at least two dots and never all six"""
    import random
    rnd, op, rock = random.Random(4451), out.load(), _rockmask(v)
    DISC = [(1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3)]
    for cy in range(4, 96, 25):
        for cx in range(2, 230, 17):
            cell = []
            while not 2 <= len(cell) <= 5:
                cell = [(q, r) for r in range(3) for q in range(2) if rnd.random() < 0.5]
            for q, r in cell:
                x, y = cx + q * 6, cy + r * 6
                if not all(rock(x + a, y + b) for a, b in DISC):
                    continue
                base = op[x + 1, y + 1]
                for a, b in DISC:
                    op[x + a, y + b] = _shade(base, 1.2 if b < 2 and a < 3 else 0.6)
                op[x + 1, y], op[x, y + 1] = (252, 244, 220), (252, 244, 220)
                op[x + 2, y + 3], op[x + 3, y + 2] = _shade(base, 0.4), _shade(base, 0.4)


def motif_mouth(out, v, c):
    """STILLFALL: a clear cave mouth beside the frozen fall -- a ragged black opening in the ice cliff, shaded in from
    its edge, so the painting keeps an opening (vanilla's own mouth is too faint to survive the ice)"""
    import math, random
    rnd = random.Random(4454)
    cx, base, w, h = c["mouth"]
    d = ImageDraw.Draw(out)
    for k, col in enumerate([(48, 96, 150), (20, 40, 72), (6, 12, 28)]):
        s, pts = 1 - k * 0.16, []
        for i in range(25):
            t = math.pi * i / 24
            j = rnd.uniform(-3, 3) * s
            pts.append((cx - math.cos(t) * (w / 2 * s + j), base - math.sin(t) * (h * s + j)))
        d.polygon(pts + [(cx + w / 2 * s, base + 1), (cx - w / 2 * s, base + 1)], fill=col)


def motif_lights(out, v, c):
    """STILL RUNNING: a green status light on every housing, nobody connected to see it"""
    import random
    rnd, op = random.Random(4451), out.load()
    n = 0
    while n < 22:
        x, y = rnd.randrange(2, 236), rnd.randrange(8, 100)
        if not (x < 110 or x > 170) or not all(30 < _lum(op[x + a, y + b]) < 150 for a in range(3) for b in range(2)):
            continue
        n += 1
        for a in range(3):
            for b in range(2):
                op[x + a, y + b] = (200, 255, 176) if (a, b) == (0, 0) else (96, 232, 88)


MOTIFS = dict(lights=motif_lights, courses=motif_courses, cable=motif_cable, columns=motif_columns, crystals=motif_crystals,
              cracks=motif_cracks, braille=motif_braille, mouth=motif_mouth)


def paint(folder, sec, out_dir):
    """--paint: the start image, then the sprite server's painting of it, with its record"""
    import spriteforge
    d = os.path.join(out_dir, folder)
    os.makedirs(d, exist_ok=True)
    init = os.path.join(d, "painted_init.png")
    paint_init(folder, sec).save(init)
    c = PAINT[folder]
    p = dict(mode="i2i", out=os.path.join(d, "painted"), prompt=PAINT_STYLE % c["prompt"],
             negative=PAINT_NEG + (", " + c["neg"] if c.get("neg") else ""),
             seed=c["seed"], steps=28, cfg=5.5, sampler="dpmpp_2m", scheduler="karras", denoise=c["denoise"],
             stop_at=None, image=os.path.relpath(init, ROOT), size=list(PAINT_SIZE))
    return spriteforge.run(p)


def painted_path(folder):
    return os.path.join(A.draft or DRAFT_DEFAULT, folder, "painted.png")


def painted_picture(folder):
    """the painting fitted to 240x112 (cropped to the picture's shape about its middle, then filtered down)"""
    im = Image.open(painted_path(folder)).convert("RGB")
    W, H = im.size
    want = 240 / 112
    if W / H > want:
        w = int(H * want)
        im = im.crop(((W - w) // 2, 0, (W - w) // 2 + w, H))
    else:
        h = int(W / want)
        im = im.crop((0, (H - h) // 2, W, (H - h) // 2 + h))
    im = im.resize((240, 112), Image.LANCZOS)
    for m in PAINT.get(folder, {}).get("post", []):
        POSTS[m](im)
    return im


def post_braille(im):
    """THE DOTS, after the painting (the server smooths a dot this small away, or swells it into a stud): lines of
    six-dot braille cells pressed into the painted stone at the picture's own size -- a 2px dot lit at its top-left
    with a 1px shadow below-right, two columns of three at a 4px pitch, cells 9px apart and lines 14px apart, so each
    cell reads as a cell; at least two dots in a cell and never all six. Only where the stone is (warm, lit, and the
    cell's whole footprint stone), so the sky, the leaves and the dark mouth stay as painted"""
    import colorsys, random
    rnd, px = random.Random(4451), im.load()

    def stone(x, y):
        if not (0 <= x < 240 and 0 <= y < 112):
            return False
        r, g, b = px[x, y]
        h, sat, val = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return 15 <= h * 360 <= 50 and sat > 0.12 and 0.45 < val

    for cy in range(3, 104, 14):
        for cx in range(2 + (cy // 14) % 2 * 4, 234, 9):
            if cx > 160 and cy < 40:                                  # the pale clouds, sandstone-coloured
                continue
            if not all(stone(cx + a, cy + b) for a in range(-1, 8) for b in range(-1, 12)):
                continue
            cell = []
            while not 2 <= len(cell) <= 5:
                cell = [(q, r) for r in range(3) for q in range(2) if rnd.random() < 0.5]
            for q, r in cell:
                x, y = cx + q * 4, cy + r * 4
                base = px[x, y]
                px[x, y] = _shade(base, 1.22)
                px[x + 1, y] = px[x, y + 1] = _shade(base, 1.06)
                px[x + 1, y + 1] = _shade(base, 0.86)
                px[x + 2, y + 1] = px[x + 1, y + 2] = px[x + 2, y + 2] = _shade(base, 0.6)


POSTS = dict(braille=post_braille)


# ================================================================== OTHER CAVE's four lights
def light_ramps():
    """[(rock ramp, crystal ramp)] for lights 0..3: row 8 of palettes_other (teal) and palettes_other_1..3, the rock
    its indices 1..5 and the crystal 9..15, each sorted dark to light"""
    out = []
    base = os.path.join(GBA, "data/tilesets/secondary/rock_tunnel")
    for d in ("palettes_other", "palettes_other_1", "palettes_other_2", "palettes_other_3"):
        lines = open(os.path.join(base, d, "08.pal")).read().split("\n")[3:19]
        cols = [tuple(int(v) for v in l.split()) for l in lines]
        out.append((sorted(cols[1:6], key=_lum), sorted(cols[9:16], key=_lum)))
    return out


def light_of(c):
    """what a colour of the teal painting is: 'crystal' (teal), 'rock' (mauve) or None (sky, sea, foam: kept)"""
    import colorsys
    h, sat, v = colorsys.rgb_to_hsv(*[x / 255 for x in c])
    h *= 360
    if 150 <= h < 195 and sat > 0.12:
        return "crystal"
    if (h >= 280 or h < 40) and sat < 0.45:
        return "rock"
    if sat < 0.08 and v < 0.75:                                     # a near-grey shadow in the rock
        return "rock"
    return None


def light_palettes(pal13, draft=None, van=None):
    """palette 13 (index 0 then 15 colours) in each of the four lights; light 0 is the painting's own. A colour that
    lies mostly where vanilla's picture has its sky and sea (draft and van: the two screens) is the open air and
    keeps its colour in every light -- the cave's light is inside it, not over the sea"""
    ramps = light_ramps()
    out = [list(pal13)]
    air = set()
    if draft is not None:
        dp, vp = draft.load(), van.load()
        n, a = collections.Counter(), collections.Counter()
        for y in range(24, 136):
            for x in range(240):
                c = dp[x, y]
                n[c] += 1
                if _region(vp[x, y]) in ("sky", "water"):
                    a[c] += 1
        air = {c for c in n if a[c] > 0.6 * n[c]}
    #  where each teal colour sits on its own light-0 ramp, by luminance, so it lands at the same place on light k's
    for k in (1, 2, 3):
        pal = [pal13[0]]
        for c in pal13[1:]:
            role = None if c in air else light_of(c)
            if role is None:
                pal.append(c)
                continue
            r0, rk = ramps[0][0 if role == "rock" else 1], ramps[k][0 if role == "rock" else 1]
            lo, hi = _lum(r0[0]), _lum(r0[-1])
            t = (_lum(c) - lo) / max(1, hi - lo)
            pal.append(tuple((v >> 3) << 3 for v in _ramp(rk, t)))
        out.append(pal)
    return out


def write_pal(cols, path):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(cols))
        for c in cols:
            f.write("%d %d %d\n" % c)


# ================================================================== drafting
def layouts_for(folder, sec):
    out = []
    for m in maps_of(sec):
        try:
            out.append((m, RS.layout_of(m)))
        except StopIteration:
            pass
    return out


_RENDER = {}


def render(m, l):
    if m not in _RENDER:
        _RENDER[m] = RS.render(l)
    return _RENDER[m]


def best_window(cands, ww=WIN_W, wh=WIN_H):
    """the ww x wh window, over every map of the cave, scored for what a player would know the cave by: the most
    different blocks, the least of its commonest block (a bare floor), and the least black (void)"""
    best = None
    for m, l in cands:
        W, H = l["width"], l["height"]
        if W < ww or H < wh:
            continue
        bd = open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
        ids = [[struct.unpack_from("<H", bd, (y * W + x) * 2)[0] & 0x3FF for x in range(W)] for y in range(H)]
        img = render(m, l)
        lum = img.convert("L").resize((W, H), Image.BOX).load()
        n = ww * wh
        for y0 in range(0, H - wh + 1):
            for x0 in range(0, W - ww + 1):
                cells = [ids[y][x] for y in range(y0, y0 + wh) for x in range(x0, x0 + ww)]
                dark = sum(1 for y in range(y0, y0 + wh) for x in range(x0, x0 + ww) if lum[x, y] < 18)
                common = collections.Counter(cells).most_common(1)[0][1] / n
                score = len(set(cells)) + 0.25 * n * (1 - common) - 1.5 * dark
                if best is None or score > best[0]:
                    best = (score, m, x0, y0)
    return best


def picture(folder, sec, painted=None):
    """the 240x112 RGB picture for this cave, and where it was taken: the painting where there is one (unless
    --top-down), else the top-down window"""
    if painted is None:
        painted = not A.top_down and os.path.exists(painted_path(folder))
    if painted:
        rec = json.load(open(painted_path(folder)[:-4] + ".json"))
        return painted_picture(folder), "painted, seed %d, denoise %.2f" % (rec["seed"], rec["denoise"])
    cands = layouts_for(folder, sec)
    if folder in VIEW:
        v = VIEW[folder]
        m, x0, y0 = v[:3]
        l = dict(cands)[m]
        img = render(m, l)
        if len(v) > 3:                                      # a doubled 8x4 window
            crop = img.crop((x0 * 16, y0 * 16, x0 * 16 + 120, y0 * 16 + 56)).resize((240, 112), Image.NEAREST)
            return crop, "%s (%d,%d) 2x, chosen" % (m, x0, y0)
        return img.crop((x0 * 16, y0 * 16, x0 * 16 + 240, y0 * 16 + 112)), "%s (%d,%d), chosen" % (m, x0, y0)
    b = best_window(cands)
    if b:
        _, m, x0, y0 = b
        img = render(m, dict(cands)[m])
        return img.crop((x0 * 16, y0 * 16, x0 * 16 + 240, y0 * 16 + 112)), "%s (%d,%d)" % (m, x0, y0)
    b = best_window(cands, 8, 4)                            # rooms too small for 15x7 (THE WRONG WAY's are 11x11)
    if not b:
        return None, "no map of %s is 8x4 blocks" % sec
    _, m, x0, y0 = b
    img = render(m, dict(cands)[m])
    crop = img.crop((x0 * 16, y0 * 16, x0 * 16 + 120, y0 * 16 + 56)).resize((240, 112), Image.NEAREST)
    return crop, "%s (%d,%d) 2x" % (m, x0, y0)


def _fixed(pic, cols):
    """pic mapped onto exactly these colours, undithered"""
    pi = Image.new("P", (1, 1))
    flat = [v for c in cols for v in c]
    pi.putpalette(flat + flat[:3] * (256 - len(cols)))
    return pic.quantize(palette=pi, dither=Image.Dither.NONE)


def keep_accents(pic, q, n=15, rounds=3):
    """a painting's small bright accent (SMOULDER's glowing cracks, a status light, the cable) is a few hundred pixels
    and median cut spends no colour on it; where pixels sit far from every colour chosen, the two closest colours are
    merged and the accent takes the freed index"""
    cols = [tuple(q.getpalette()[i * 3:i * 3 + 3]) for i in range(n)]
    src = list(pic.getdata())
    for _ in range(rounds):
        d2 = lambda a, b: sum((a[k] - b[k]) ** 2 for k in range(3))
        far = [c for c in src if min(d2(c, k) for k in cols) > 56 ** 2]
        if len(far) < 0.002 * len(src):
            break
        acc = tuple(sorted(c[k] for c in far)[len(far) // 2] for k in range(3))
        i, j = min(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda ij: d2(cols[ij[0]], cols[ij[1]]))
        cols[i] = tuple((cols[i][k] + cols[j][k]) // 2 for k in range(3))
        cols[j] = acc
        q = _fixed(pic, cols)
    return q


def reduce(pic, vpal, accents=False):
    """15 colours into palette 13's indices 1..15 (index 0 vanilla's: BG0 colour 0 is transparent); a painting keeps
    its accents (keep_accents)"""
    q = pic.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    if accents:
        q = keep_accents(pic, q)
    qp = (q.getpalette()[:45] + [0] * 45)[:45]                      # a cave of fewer colours leaves the rest unused
    cols = [tuple(qp[i * 3:i * 3 + 3]) for i in range(15)]
    #  to the GBA's 5 bits, as the palette will hold them
    cols = [tuple((v >> 3) << 3 for v in c) for c in cols]
    order = sorted(range(15), key=lambda i: sum(cols[i]))           # dark to light, for a readable palette
    remap = {old: new + 1 for new, old in enumerate(order)}
    pal13 = [vpal[0]] + [cols[i] for i in order]
    idx = [remap[v] for v in q.getdata()]
    return idx, pal13


def build(folder, sec):
    """(tiles, tilemap, palette32, note): vanilla's letterbox and banner kept, the picture rows redrawn"""
    vt, vm, vpal = vanilla(folder)
    pic, where = picture(folder, sec)
    if pic is None:
        return None
    idx, pal13 = reduce(pic, vpal, accents=where.startswith("painted"))
    tiles, seen, m, tpal = [], {}, [0] * 640, []

    def add(t, p=14):
        k = tuple(t)
        if k not in seen:
            seen[k] = len(tiles)
            tiles.append(list(t))
            tpal.append(p)
        return seen[k]

    add(vt[0])                                                       # tile 0 stays tile 0 (columns 30, 31)
    for ty in range(20):
        for tx in range(32):
            e = vm[ty * 32 + tx]
            if tx >= 30 or not (3 <= ty <= 16):
                m[ty * 32 + tx] = (e & 0xFC00) | add(vt[e & 0x3FF], e >> 12)  # vanilla's own tile, flips and palette
    for ty in range(14):
        for tx in range(30):
            t = [idx[(ty * 8 + y) * 240 + tx * 8 + x] for y in range(8) for x in range(8)]
            m[(ty + 3) * 32 + tx] = (13 << 12) | add(t, 13)
    pal = pal13 + vpal[16:32]
    #  tiles.png's pixels: a palette-14 tile's written 16..31, as vanilla's are (gbagfx keeps the low nibble)
    png = [[v + 16 if tp == 14 else v for v in t] for t, tp in zip(tiles, tpal)]
    return tiles, m, pal, where, png


def tiles_png(tiles, pal, path):
    """tiles.png as vanilla keeps it: 8-bit indexed, 32 colours (palette 13 then 14), 15 tiles a row -- gbagfx keeps
    each index's low nibble, so a palette-14 tile's pixels are written 16..31"""
    per = 15
    rows = (len(tiles) + per - 1) // per
    im = Image.new("P", (per * 8, rows * 8))
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat)              # exactly palette 13 and 14, as vanilla's: never a 256-entry PLTE (T-442, T-444)
    px = im.load()
    for i, t in enumerate(tiles):
        for y in range(8):
            for x in range(8):
                px[(i % per) * 8 + x, (i // per) * 8 + y] = t[y * 8 + x]
    im.save(path)


def font(n):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", n)
    except OSError:
        return ImageFont.load_default()


def sheet(rows, path, title):
    Z = 2
    cw, ch = 240 * Z, 160 * Z
    W = 2 * cw + 3 * 16 + 300
    H = 40 + len(rows) * (ch + 34)
    out = Image.new("RGB", (W, H), (34, 34, 40))
    d = ImageDraw.Draw(out)
    d.text((12, 10), title, fill=(235, 235, 235), font=font(14))
    y = 40
    for r in rows:
        d.text((16, y), "VANILLA  %s" % r["folder"], fill=(170, 170, 170), font=font(12))
        d.text((32 + cw, y), "DRAFT  %s -- %s" % (r["name"], r["where"]), fill=(240, 220, 120), font=font(12))
        out.paste(r["vanilla"].resize((cw, ch), Image.NEAREST), (16, y + 16))
        out.paste(r["draft"].resize((cw, ch), Image.NEAREST), (32 + cw, y + 16))
        tx = 48 + 2 * cw
        for k, line in enumerate(r["notes"]):
            d.text((tx, y + 18 + k * 15), line, fill=(210, 210, 210), font=font(11))
        y += ch + 34
    out.save(path)
    return path


# ================================================================== main
def report():
    nm = names()
    by_folder = collections.OrderedDict()
    for key, sec, typ, folder in previews():
        by_folder.setdefault(folder, []).append((key, sec, typ))
    print("  %d preview entries, %d pictures (graphics/map_preview/)" % (sum(len(v) for v in by_folder.values()),
                                                                         len(by_folder)))
    for folder, ents in by_folder.items():
        status = ("batch E: " + BATCH_E[folder]) if folder in BATCH_E else ("not drafted: " + NOT_DRAFTED.get(folder, "?"))
        print("  %-17s %s" % (folder, status))
        for key, sec, typ in ents:
            n = nm.get(sec, "?")
            w = name_width(n)
            print("      %-22s %-34s %-16s %3dpx%s" % (key, sec, n, w, "  ** wider than the 104px window" if w > 104 else ""))
    return by_folder


def main():
    if A.write and not A.approved:
        print("  --write refuses without --approved: the user approves a preview before it is written.")
        return 1
    by_folder = report()
    if A.paint is not None:
        for folder in (A.paint or list(PAINT)):
            key, sec, typ = by_folder[folder][0]
            paint(folder, sec, A.draft or DRAFT_DEFAULT)
        if not (A.draft or A.write):
            return 0
    if not (A.draft or A.write):
        return 0
    nm = names()
    out_dir = A.draft or DRAFT_DEFAULT
    sheets = A.sheets or out_dir
    rows = []
    for folder in BATCH_E:
        key, sec, typ = by_folder[folder][0]
        made = build(folder, sec)
        if not made:
            print("  %-17s nothing drawn" % folder)
            continue
        tiles, m, pal, where, png = made
        vt, vm, vpal = vanilla(folder)
        van, dra = compose(vt, vm, vpal), compose(tiles, m, pal)
        for im in (van, dra):
            draw_name(im, nm[sec], (vpal if im is van else pal))
        notes = ["%s, %s" % (nm[sec], sec), "type %s" % typ, BATCH_E[folder], "",
                 "tiles: %d (vanilla %d; must stay < 450)" % (len(tiles), len(vt)),
                 "palette 13: 15 colours + vanilla's 0", "palette 14, letterbox, banner: vanilla's"]
        painted = where.startswith("painted")
        lights = light_palettes(pal[:16], dra, van) if folder == "altering_cave" and painted else None
        if lights:
            notes += ["", "OTHER CAVE: one set of tiles, four", "palettes 13 (teal, AMBER, CHRYSOPRASE,",
                      "ROSE QUARTZ) -- the rows below. The", "engine lays the coming visit's light",
                      "over palette 13."]
        elif folder == "altering_cave":
            notes += ["", "OTHER CAVE cycles four lights;", "this preview shows one (teal).",
                      "Following the light is engine code."]
        if len(tiles) >= 450:
            notes += ["", "** TOO MANY TILES for baseBlock 0x1C2"]
        print("  %-17s %-16s %3d tiles  from %s" % (folder, nm[sec], len(tiles), where))
        if A.draft:
            d = os.path.join(out_dir, folder)
            os.makedirs(d, exist_ok=True)
            tiles_png(png, pal, os.path.join(d, "tiles.png"))
            open(os.path.join(d, "tilemap.bin"), "wb").write(struct.pack("<640H", *m))
            dra.save(os.path.join(d, "preview.png"))
            for n, lp in list(enumerate(lights or []))[1:]:
                write_pal(lp, os.path.join(d, "light%d.pal" % n))
                li = compose(tiles, m, lp + pal[16:32])
                draw_name(li, nm[sec], pal)
                li.save(os.path.join(d, "preview_light%d.png" % n))
            json.dump({"mapsec": sec, "name": nm[sec], "from": where, "num_tiles": len(tiles)},
                      open(os.path.join(d, "draft.json"), "w"), indent=1)
        if A.write:
            d = os.path.join(MPS, folder)
            tiles_png(png, pal, os.path.join(d, "tiles.png"))
            open(os.path.join(d, "tilemap.bin"), "wb").write(struct.pack("<640H", *m))
            for n, lp in list(enumerate(lights or []))[1:]:          # OTHER CAVE: map_preview_screen.c INCBINs these
                write_pal(lp, os.path.join(d, "light%d.pal" % n))
            rules = open(RULES).read()
            rules = re.sub(r"(\$\(MAPPREVIEWGFXDIR\)/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+"
                           % folder, lambda mm: mm.group(1) + str(len(tiles)), rules)
            open(RULES, "w").write(rules)
            print("      written %s" % d)
        rows.append(dict(folder=folder, name=nm[sec], where=where, vanilla=van, draft=dra, notes=notes))
        for n, lp in enumerate(lights or []):
            if n == 0:
                continue
            li = compose(tiles, m, lp + pal[16:32])
            draw_name(li, nm[sec], pal)
            rows.append(dict(folder=folder, name="%s, light %d (%s)" % (nm[sec], n, LIGHT_NAMES[n]),
                             where=where, vanilla=van, draft=li,
                             notes=["light %d: %s" % (n, LIGHT_NAMES[n]), "the same tiles, palette 13 moved",
                                    "onto this light's rock and crystal", "ramps (palettes_other_%d)" % n]))
    if A.draft:
        os.makedirs(sheets, exist_ok=True)
        painted = any(r["where"].startswith("painted") for r in rows)
        per = 5 if painted else (len(rows) + 1) // 2
        parts = [rows[i:i + per] for i in range(0, len(rows), per)]
        for i, part in enumerate(parts, 1):
            if painted:
                p = sheet(part, os.path.join(sheets, "t445p_%d.png" % i),
                          "T-445 DRAFT -- the cave previews, vanilla (left) and PAINTED on the sprite server in each "
                          "cave's colours (right); the name is the game's, in its own font. Sheet %d of %d."
                          % (i, len(parts)))
            else:
                p = sheet(part, os.path.join(sheets, "t445_previews_%d.png" % i),
                          "T-445 DRAFT -- the cave previews, vanilla (left) and drawn from the batch E caves (right); "
                          "the name is printed by the game, shown here in its own font. Sheet %d of %d."
                          % (i, len(parts)))
            print("  sheet -> %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
