#!/usr/bin/env python3
"""T-445: the map preview screens -- the picture a cave (or a forest, the tower, a hideout) shows as it is entered.

    python3 tools/gbapreviews.py                         # report: every preview, the mapsecs that show it, the name
                                                         #   the game prints on it, and which T-438 batch E covered
    python3 tools/gbapreviews.py --draft [DIR]           # draft the batch E caves' previews into DIR (gfx/drafts/t445/),
                                                         #   and the contact sheets; --sheets DIR puts the sheets elsewhere
    python3 tools/gbapreviews.py --write --approved      # into the engine (graphics/map_preview/<cave>/tiles.png,
                                                         #   tilemap.bin, and the -num_tiles line in graphics_file_rules.mk).
                                                         #   Without --approved it refuses: nothing is approved yet.

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


def pal_of(folder):
    raw = open(os.path.join(MPS, folder, "tiles.gbapal"), "rb").read()
    out = []
    for i in range(0, len(raw), 2):
        v = struct.unpack_from("<H", raw, i)[0]
        out.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3))
    return out


def vanilla(folder):
    """(tiles [64 indices each], tilemap entries [640], palette [32 rgb]) as the engine builds them"""
    t = open(os.path.join(MPS, folder, "tiles.4bpp"), "rb").read()
    tiles = []
    for i in range(len(t) // 32):
        px = []
        for b in t[i * 32:(i + 1) * 32]:
            px += [b & 15, b >> 4]
        tiles.append(px)
    m = list(struct.unpack("<640H", open(os.path.join(MPS, folder, "tilemap.bin"), "rb").read()))
    return tiles, m, pal_of(folder)


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


def picture(folder, sec):
    """the 240x112 RGB picture for this cave, and where it was taken"""
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


def reduce(pic, vpal):
    """15 colours into palette 13's indices 1..15 (index 0 vanilla's: BG0 colour 0 is transparent)"""
    q = pic.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
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
    idx, pal13 = reduce(pic, vpal)
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
    im.putpalette(flat + [0] * (768 - len(flat)))
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
        print("  --write refuses without --approved: T-445's drafts have not been approved by the user.")
        return 1
    by_folder = report()
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
        if folder == "altering_cave":
            notes += ["", "OTHER CAVE cycles four lights;", "this preview shows one (teal).",
                      "Following the light is engine code:", "a question for the user."]
        if len(tiles) >= 450:
            notes += ["", "** TOO MANY TILES for baseBlock 0x1C2"]
        print("  %-17s %-16s %3d tiles  from %s" % (folder, nm[sec], len(tiles), where))
        if A.draft:
            d = os.path.join(out_dir, folder)
            os.makedirs(d, exist_ok=True)
            tiles_png(png, pal, os.path.join(d, "tiles.png"))
            open(os.path.join(d, "tilemap.bin"), "wb").write(struct.pack("<640H", *m))
            dra.save(os.path.join(d, "preview.png"))
            json.dump({"mapsec": sec, "name": nm[sec], "from": where, "num_tiles": len(tiles)},
                      open(os.path.join(d, "draft.json"), "w"), indent=1)
        if A.write:
            d = os.path.join(MPS, folder)
            tiles_png(png, pal, os.path.join(d, "tiles.png"))
            open(os.path.join(d, "tilemap.bin"), "wb").write(struct.pack("<640H", *m))
            rules = open(RULES).read()
            rules = re.sub(r"(\$\(MAPPREVIEWGFXDIR\)/%s/tiles\.4bpp: %%\.4bpp: %%\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+"
                           % folder, lambda mm: mm.group(1) + str(len(tiles)), rules)
            open(RULES, "w").write(rules)
            print("      written %s" % d)
        rows.append(dict(folder=folder, name=nm[sec], where=where, vanilla=van, draft=dra, notes=notes))
    if A.draft:
        os.makedirs(sheets, exist_ok=True)
        half = (len(rows) + 1) // 2
        for i, part in enumerate((rows[:half], rows[half:]), 1):
            p = sheet(part, os.path.join(sheets, "t445_previews_%d.png" % i),
                      "T-445 DRAFT -- the cave previews, vanilla (left) and drawn from the batch E caves (right); the "
                      "name is printed by the game, shown here in its own font. Sheet %d of 2." % i)
            print("  sheet -> %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
