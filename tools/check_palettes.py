#!/usr/bin/env python3
"""A palette loaded by sizeof() must be the size it means (T-444, after T-442).

    python3 tools/check_palettes.py           # exits non-zero on a palette of ours that loads more than it draws
    python3 tools/check_palettes.py --all     # and lists every vanilla one of more than 16 colours, for the record

WHY. A .gbapal made from a PNG carries the PNG's WHOLE palette: an indexed PNG saved with 256 entries makes a
512-byte .gbapal even when its pixels use sixteen. Wherever the engine loads that palette with sizeof(), it copies
all 512 bytes -- sixteen palettes -- from wherever it starts. T-438 batch B's 31 field-move sheets did exactly that:
the banner's palette ran past BG 15 into OBJ 0..14 with zeros, and every person on screen went black behind PRUNE,
SMASH and SURF (T-442). The FAME CHECKER's four portraits (T-177) did the same from OBJ 6 (T-444).

WHAT IT READS. Every `NAME[] = INCBIN_U16/U32("....gbapal")` in src/, every `sizeof(NAME)` of one of them, and the
source the .gbapal is built from (a .pal beside it if there is one, which make prefers, else the .png). A load is
WRONG when the source holds more than 16 colours but the picture draws only indices 0..15 -- a 4bpp picture carrying
a 256-colour palette. A source byte-identical to pret's is vanilla and is listed with --all, never failed: vanilla's
multi-palette screens (32, 48 ... colours) load several palettes on purpose. A source of ours is also WRONG when it
holds more colours than pret's own version of the same file.

HOLES (T-484). A map tile we redrew must not draw an index its palette row leaves UNFILLED (pret's magenta): batch
C's paving stepped one shade past vanilla's into index 9, a real grey in general's rows and magenta in UMBRA
PLATEAU's row 12, and the plateau's path showed pink specks for a week. Every block a reachable layout places, every
tile it draws (primary or secondary) in the row it draws it with: a pixel that differs from pret's tile and lands on
an unfilled colour is WRONG. A pixel vanilla drew the same way is vanilla's and is never failed.
"""
import glob, io, json, os, re, struct, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")

INCBIN = re.compile(r'\b(\w+)\s*\[\s*\]\s*=\s*INCBIN_U(?:8|16|32)\(\s*"([^"]+\.gbapal)"')
SIZEOF = re.compile(r'\bsizeof\s*\(?\s*(\w+)\s*\)?')


def jasc_count(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    try:
        return int(lines[2])
    except (IndexError, ValueError):
        return len([l for l in lines[3:] if l.strip()])


def jasc_count_bytes(data):
    lines = data.decode("utf-8", "replace").splitlines()
    try:
        return int(lines[2])
    except (IndexError, ValueError):
        return len([l for l in lines[3:] if l.strip()])


def png_info(data):
    im = Image.open(io.BytesIO(data))
    if im.mode != "P":
        return None, None
    pal = im.getpalette() or []
    return len(pal) // 3, max(im.getdata()) if im.width and im.height else 0


def upstream(rel):
    r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def scan():
    srcs = glob.glob(os.path.join(GBA, "src", "**", "*.c"), recursive=True) + \
           glob.glob(os.path.join(GBA, "src", "**", "*.h"), recursive=True)
    syms, texts = {}, {}
    for f in srcs:
        t = open(f, encoding="utf-8", errors="replace").read()
        texts[f] = t
        for name, path in INCBIN.findall(t):
            syms.setdefault(name, set()).add(path)
    loads = {}
    for f, t in texts.items():
        for m in SIZEOF.finditer(t):
            if m.group(1) in syms:
                line = t.count("\n", 0, m.start()) + 1
                loads.setdefault(m.group(1), []).append("%s:%d" % (os.path.relpath(f, GBA), line))
    found = []
    for name, where in sorted(loads.items()):
        for gp in sorted(syms[name]):
            stem = gp[:-len(".gbapal")]
            pal, png = os.path.join(GBA, stem + ".pal"), os.path.join(GBA, stem + ".png")
            if os.path.exists(pal):
                rel, n, top = stem + ".pal", jasc_count(pal), None
                data = open(pal, "rb").read()
                #  T-472: a .pal beside a picture still has to fit the picture -- make takes the .pal, but the pixels
                #  are the picture's, so a new 256-entry JASC .pal over a 4bpp picture was passing unseen (T-442's trap)
                if os.path.exists(png):
                    top = png_info(open(png, "rb").read())[1]
            elif os.path.exists(png):
                rel = stem + ".png"
                data = open(png, "rb").read()
                n, top = png_info(data)
                if n is None:
                    continue
            else:
                continue
            if n <= 16:
                continue
            up = upstream(rel)
            vanilla = up == data
            upn = None
            if up is not None and not vanilla:
                upn = jasc_count_bytes(up) if rel.endswith(".pal") else png_info(up)[0]
            #  a 4bpp picture carrying more than one palette, or a palette of ours grown past vanilla's own
            #  T-472: a .pal is judged against pret's own when there is one -- a tilemap picks palettes per tile, so a
            #  4bpp picture's pixels never pass 15 yet REGION_MAP and the intro's backgrounds load 32 to 80 colours, as
            #  vanilla does. A NEW .pal of more than 16 has no such precedent: WRONG over a 4bpp picture, or over none.
            if rel.endswith(".pal"):
                wrong = (upn is not None and n > upn) or (up is None and (top is None or top < 16))
            else:
                wrong = (top is not None and top < 16) or (upn is not None and n > upn)
            found.append({"sym": name, "src": rel, "colours": n, "top": top, "vanilla": vanilla, "wrong": wrong,
                          "where": where, "vanilla_colours": upn})
    return len(syms), sum(len(v) for v in loads.values()), found


# ================================================================== holes: a redrawn pixel on an unfilled colour
def _jasc(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    return [tuple(int(v) for v in l.split()[:3]) for l in lines[3:19]]


def _tiles(data):
    im = Image.open(io.BytesIO(data))
    w, h = im.size
    px = im.tobytes()
    return [[px[(ty * 8 + r) * w + tx * 8 + c] & 15 for r in range(8) for c in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def holes():
    """[(tileset dir, tile, row, unfilled indices, a layout that shows it)] over every reachable layout"""
    hdr = open(os.path.join(GBA, "src/data/tilesets/headers.h")).read()
    gfx = open(os.path.join(GBA, "src/data/tilesets/graphics.h")).read() + \
        open(os.path.join(GBA, "src/graphics.c")).read()          # the primaries' tiles and palettes are there
    mts = open(os.path.join(GBA, "src/data/tilesets/metatiles.h")).read()
    sets = {}

    def tileset(sym):
        if sym in sets:
            return sets[sym]
        body = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(sym or "-"), hdr, re.S)
        out = None
        if body:
            b = body.group(1)
            m = re.search(r"\.metatiles = (\w+)", b)
            t = re.search(r"\.tiles = (\w+)", b)
            p = re.search(r"\.palettes = (\w+)", b)
            md = m and re.search(r'%s\[\] = INCBIN_U16\("(data/tilesets/[^"]+)/metatiles\.bin' % re.escape(m.group(1)), mts)
            td = t and re.search(r'%s\[\] = INCBIN_U32\("(data/tilesets/[^"]+)/tiles\.' % re.escape(t.group(1)), gfx)
            pt = p and re.search(r"%s\[\]\[16\] =\s*\{(.*?)\};" % re.escape(p.group(1)), gfx, re.S)
            if md and td and pt and os.path.exists(os.path.join(GBA, td.group(1), "tiles.png")):
                rel = td.group(1) + "/tiles.png"
                up = upstream(rel)
                pals = [os.path.join(GBA, f[:-len(".gbapal")] + ".pal")
                        for f in re.findall(r'INCBIN_U16\("([^"]+)"\)', pt.group(1))]
                out = dict(dir=td.group(1), mt=open(os.path.join(GBA, md.group(1), "metatiles.bin"), "rb").read(),
                           now=_tiles(open(os.path.join(GBA, rel), "rb").read()), van=_tiles(up) if up else [],
                           pals=[_jasc(f) if os.path.exists(f) else [] for f in pals])
        sets[sym] = out
        return out

    lays = {l["id"]: l for l in json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"] if "id" in l}
    used = set()
    for mj in glob.glob(os.path.join(GBA, "data/maps/*/map.json")):
        if not os.path.basename(os.path.dirname(mj)).startswith("Prototype_"):
            used.add(json.load(open(mj)).get("layout"))
    found = {}
    for lid in sorted(used & set(lays)):
        l = lays[lid]
        pri, sec = tileset(l.get("primary_tileset")), tileset(l.get("secondary_tileset"))
        bp = os.path.join(GBA, l.get("blockdata_filepath", ""))
        if not pri or not sec or not os.path.exists(bp):
            continue
        data = open(bp, "rb").read()
        for b in set(struct.unpack_from("<%dH" % (len(data) // 2), data)):
            b &= 0x3FF
            buf, k = (pri["mt"], b) if b < 640 else (sec["mt"], b - 640)
            if (k + 1) * 16 > len(buf):
                continue
            for v in struct.unpack_from("<8H", buf, k * 16):
                t, row = v & 0x3FF, v >> 12
                ts, i = (pri, t) if t < 640 else (sec, t - 640)
                pal = (pri if row < 7 else sec)["pals"]
                if i >= len(ts["now"]) or row >= len(pal) or len(pal[row]) < 16:
                    continue
                van = ts["van"][i] if i < len(ts["van"]) else [None] * 64
                bad = sorted({a for a, w in zip(ts["now"][i], van) if a and a != w and pal[row][a] == (255, 0, 255)})
                if bad:
                    found.setdefault((ts["dir"], i, row), (bad, l["name"]))
    return [(d, i, r, bad, name) for (d, i, r), (bad, name) in sorted(found.items())]


def check():
    """For check_lexicon: [(what, why)] for every palette of ours that loads more colours than its picture draws."""
    _, _, found = scan()
    return [(f["src"], "%d colours%s, loaded by sizeof(%s) at %s -- re-save it with the colours it draws" %
             (f["colours"], ", pixels 0..%d" % f["top"] if f["top"] is not None else " (vanilla's has %s)" %
              f["vanilla_colours"], f["sym"], ", ".join(f["where"])))
            for f in found if f["wrong"] and not f["vanilla"]] + \
        [("%s/tiles.png tile %d" % (d, i), "drawn in row %d (%s) on index %s, which that row leaves unfilled (magenta) "
          "-- redraw it on a filled index (T-484)" % (r, name, ",".join(map(str, bad)))) for d, i, r, bad, name in holes()]


def main():
    nsym, nload, found = scan()
    print("  scanned %d .gbapal symbols in src/, %d sizeof() uses of them" % (nsym, nload))
    bad = [f for f in found if f["wrong"] and not f["vanilla"]]
    for f in bad:
        print("  WRONG  %-52s %3d colours, %s; sizeof(%s) at %s" %
              (f["src"], f["colours"], "pixels 0..%d" % f["top"] if f["top"] is not None else
               "vanilla's has %s" % f["vanilla_colours"], f["sym"], ", ".join(f["where"])))
    if "--all" in sys.argv[1:]:
        for f in found:
            if f in bad:
                continue
            print("  %-6s %-52s %3d colours%s; sizeof(%s) at %s" %
                  ("vanilla" if f["vanilla"] else "ours", f["src"], f["colours"],
                   ", pixels 0..%d" % f["top"] if f["top"] is not None else " (.pal)", f["sym"], ", ".join(f["where"])))
    if not bad:
        print("  every palette loaded by sizeof() is the size its picture draws (%d over 16 colours, all on purpose)"
              % len(found))
    hs = holes()
    for d, i, r, idx, name in hs:
        print("  HOLE   %s/tiles.png tile %d, row %d (%s): index %s is unfilled there" %
              (d, i, r, name, ",".join(map(str, idx))))
    if not hs:
        print("  no redrawn map tile draws an index its palette row leaves unfilled")
    return 1 if bad or hs else 0


if __name__ == "__main__":
    sys.exit(main())
