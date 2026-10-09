#!/usr/bin/env python3
"""Picture sheets of what changed, for the user to review (the user, 2026-10-01: "I always get screenshots like this").

    python3 tools/reviewsheet.py daemons OUT.png NAME [NAME ...]   # front, back, name, category, both entries
    python3 tools/reviewsheet.py map OUT.png MAPNAME [x0 y0 w h]   # a map drawn from its layout and real tilesets
    python3 tools/reviewsheet.py margins OUT.png NAME [NAME ...]   # OPUS's four margins under the CONTENT entry

Everything is read from what the ROM is BUILT from -- the daemons from graphics/pokemon/<slot>/front.4bpp, back.4bpp
and normal.gbapal (so build first), the maps from their map.bin -- so a sheet shows what a player would see, not a
draft. Send the sheet with SendUserFile and put it on the field-test page. It does not need the theatre: the screen-
takeover card goes unanswered when the user is away, and these do not wait on it.
"""
import importlib.util, json, os, re, struct, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
_args = sys.argv[1:]
_spec = importlib.util.spec_from_file_location("gbacivic", os.path.join(ROOT, "tools/gbacivic.py"))
C = importlib.util.module_from_spec(_spec)
sys.argv = sys.argv[:1]
_spec.loader.exec_module(C)

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    SMALL = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
except OSError:
    FONT = SMALL = ImageFont.load_default()


def gbapal(path):
    d = open(path, "rb").read()
    out = []
    for i in range(16):
        c = struct.unpack_from("<H", d, 2 * i)[0]
        out.append(((c & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, ((c >> 10) & 31) * 255 // 31))
    return out


def picture(path, pal):
    """A 64x64 4bpp picture as the GBA lays it out: 8x8 tiles, row-major, index 0 clear."""
    d = open(path, "rb").read()
    im = Image.new("RGB", (64, 64), (236, 236, 240))
    for t in range(64):
        for y in range(8):
            for x in range(8):
                b = d[t * 32 + y * 4 + x // 2]
                v = (b >> 4) if x & 1 else b & 15
                if v:
                    im.putpixel(((t % 8) * 8 + x, (t // 8) * 8 + y), pal[v])
    return im


def species_table():
    """{OUR NAME: (slot, symbol stem, category)} from the built tables."""
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)',
                            open(os.path.join(GBA, "src/data/text/species_names.h")).read()))
    cats = dict(re.findall(r'\[NATIONAL_DEX_(\w+)\]\s*=\s*\{\s*\.categoryName = _\("([^"]*)"\)',
                           open(os.path.join(GBA, "src/data/pokemon/pokedex_entries.h")).read()))
    # T-395: a NEXUS resident's INDEX row and text are keyed by its own name (SPECIES_REFLECTION is OLD_UNOWN_C)
    alias = {b: a for a, b in re.findall(r"#define SPECIES_(\w+)\s+SPECIES_(\w+)\b",
                                         open(os.path.join(GBA, "include/constants/species.h")).read())}
    out = {}
    for slot, ours in names.items():
        key = alias.get(slot, slot)
        out[ours] = (slot, key.capitalize(), cats.get(key, ""))
    return out


def entry(path, stem):
    m = re.search(r'g%sPokedexText\[\] = _\(\n(.*?)\);' % stem, open(path).read(), re.S)
    return "".join(re.findall(r'"([^"]*)"', m.group(1))).replace("\\n", " ") if m else ""


def slot_dir(slot, name):
    """A daemon's built sprites: its slot's folder, or a NEXUS resident's own (nexus_reflection, T-395)."""
    base = os.path.join(GBA, "graphics/pokemon", slot.lower())
    return base if os.path.isdir(base) else os.path.join(GBA, "graphics/pokemon", "nexus_" + name.lower())


def daemons(out, names):
    table = species_table()
    W, H = 1400, len(names) * 150 + 10
    img = Image.new("RGB", (W, H), (250, 249, 245))
    d = ImageDraw.Draw(img)
    for i, name in enumerate(names):
        slot, stem, cat = table[name]
        y = i * 150 + 5
        base = slot_dir(slot, name)
        pal = gbapal(os.path.join(base, "normal.gbapal"))
        for k, view in enumerate(("front", "back")):
            img.paste(picture(os.path.join(base, view + ".4bpp"), pal).resize((128, 128), Image.NEAREST), (5 + 135 * k, y))
        d.text((280, y), "%s   %s DAEMON" % (name, cat), fill=(20, 20, 20), font=FONT)
        for j, (lab, ed) in enumerate((("CONTENT", "fr"), ("CONTEXT", "lg"))):
            text = entry(os.path.join(GBA, "src/data/pokemon/pokedex_text_%s.h" % ed), stem)
            for k, line in enumerate(textwrap.wrap(lab + ": " + text, 150)):
                d.text((280, y + 24 + j * 42 + k * 14), line, fill=(60, 60, 60), font=SMALL)
    img.save(out)


def margins(out, names):
    """T-356: each daemon's CONTENT entry and OPUS's four margins under it -- REASON's carried and put-away lines,
    then INSTINCT's -- read from the built src/data/opus_margins.h and broken where the pane breaks them."""
    table = species_table()
    src = open(os.path.join(GBA, "src/data/opus_margins.h")).read()
    rows = {}
    for slot, carried, neglected, ic, inn in re.findall(
            r"\{ SPECIES_(\w+),\s*(\w+), (\w+), (\w+), (\w+) \}", src):
        rows[slot] = (carried, neglected, ic, inn)
    text = dict(re.findall(r'static const u8 (sOpusMargin_\w+)\[\] = _\("(.*?)"\);', src))
    labels = ("REASON, carried", "REASON, put away", "INSTINCT, carried", "INSTINCT, put away")
    W, ROW = 1400, 196
    img = Image.new("RGB", (W, len(names) * ROW + 10), (250, 249, 245))
    d = ImageDraw.Draw(img)
    for i, name in enumerate(names):
        slot, stem, cat = table[name]
        y = i * ROW + 6
        base = slot_dir(slot, name)
        img.paste(picture(os.path.join(base, "front.4bpp"), gbapal(os.path.join(base, "normal.gbapal"))).resize((96, 96), Image.NEAREST), (6, y + 4))
        d.text((112, y), "%s   %s DAEMON" % (name, cat), fill=(20, 20, 20), font=FONT)
        entry_text = entry(os.path.join(GBA, "src/data/pokemon/pokedex_text_fr.h"), stem)
        for k, line in enumerate(textwrap.wrap("CONTENT: " + entry_text, 175)):
            d.text((112, y + 18 + k * 13), line, fill=(110, 110, 110), font=SMALL)
        for j, sym in enumerate(rows.get(slot, ())):
            x, yy = 112 + (j % 2) * 640, y + 52 + (j // 2) * 70
            d.text((x, yy), labels[j], fill=(67, 101, 139), font=SMALL)
            if sym == "NULL" or sym not in text:
                d.text((x, yy + 14), "(the REASON line)", fill=(150, 150, 150), font=SMALL)
                continue
            for k, line in enumerate(text[sym].split("\\n")):
                d.text((x, yy + 14 + k * 13), line, fill=(30, 30, 30), font=SMALL)
    img.save(out)


def layout_of(mapname):
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    m = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % mapname)))
    return next(l for l in layouts if l.get("id") == m["layout"])


def gdir(symbol, kind):
    """Where a tileset's TILES and PALETTES are, which is not always its own folder: SilphCo draws with
    Condominiums' graphics (headers.h names them), so its folder holds metatiles and nothing to draw them with."""
    own = C.tdir(symbol, kind)
    if os.path.exists(os.path.join(own, "tiles.png")):
        return own
    headers = open(os.path.join(GBA, "src/data/tilesets/headers.h")).read()
    body = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(symbol), headers, re.S)
    tiles = body and re.search(r"\.tiles = (\w+)", body.group(1))
    graphics = open(os.path.join(GBA, "src/data/tilesets/graphics.h")).read()
    path = tiles and re.search(r"%s\[\] = INCBIN_U32\(\"(data/tilesets/[^\"]+)/tiles\." % re.escape(tiles.group(1)), graphics)
    return os.path.join(GBA, path.group(1)) if path else own


def render(l, bd=None):
    pd, sd = C.tdir(l["primary_tileset"], "primary"), C.tdir(l["secondary_tileset"], "secondary")
    prim = open(os.path.join(pd, "metatiles.bin"), "rb").read()
    meta = open(os.path.join(sd, "metatiles.bin"), "rb").read()
    pd, sd = gdir(l["primary_tileset"], "primary"), gdir(l["secondary_tileset"], "secondary")
    pals = [C.read_pal(os.path.join(pd, "palettes/%02d.pal" % n)) for n in range(7)] + \
           [C.read_pal(os.path.join(sd, "palettes/%02d.pal" % n)) for n in range(7, 13)]
    pt, st = Image.open(os.path.join(pd, "tiles.png")), Image.open(os.path.join(sd, "tiles.png"))
    ptp, stp = pt.load(), st.load()
    W, H = l["width"], l["height"]
    bd = bd or open(os.path.join(GBA, l["blockdata_filepath"]), "rb").read()
    img = Image.new("RGB", (W * 16, H * 16))
    o = img.load()
    for yy in range(H):
        for xx in range(W):
            m = struct.unpack_from("<H", bd, (yy * W + xx) * 2)[0] & 0x3FF
            buf, k = (prim, m) if m < 640 else (meta, m - 640)
            if (k + 1) * 16 > len(buf):
                continue
            ee = struct.unpack_from("<8H", buf, k * 16)
            for layer in (0, 1):
                for q in range(4):
                    t = ee[layer * 4 + q]
                    i = t & 0x3FF
                    src, jj, hh = (ptp, i, pt.height) if i < 640 else (stp, i - 640, st.height)
                    for ty in range(8):
                        for tx in range(8):
                            sy = (jj // 16) * 8 + (7 - ty if (t >> 11) & 1 else ty)
                            v = src[(jj % 16) * 8 + (7 - tx if (t >> 10) & 1 else tx), sy] if sy < hh else 0
                            if layer and v == 0:
                                continue
                            o[xx * 16 + (q % 2) * 8 + tx, yy * 16 + (q // 2) * 8 + ty] = pals[(t >> 12) & 0xF][v]
    return img


def main():
    if len(_args) < 3:
        print(__doc__)
        return 1
    kind, out = _args[0], _args[1]
    if kind == "daemons":
        daemons(out, _args[2:])
    elif kind == "margins":
        margins(out, _args[2:])
    elif kind == "map":
        img = render(layout_of(_args[2]))
        if len(_args) == 7:
            x0, y0, w, h = map(int, _args[3:7])
            img = img.crop((x0 * 16, y0 * 16, (x0 + w) * 16, (y0 + h) * 16))
        img.save(out)
    else:
        print(__doc__)
        return 1
    print("  wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
