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
"""
import glob, io, os, re, subprocess, sys
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
            wrong = (top is not None and top < 16) or (upn is not None and n > upn)
            found.append({"sym": name, "src": rel, "colours": n, "top": top, "vanilla": vanilla, "wrong": wrong,
                          "where": where, "vanilla_colours": upn})
    return len(syms), sum(len(v) for v in loads.values()), found


def check():
    """For check_lexicon: [(what, why)] for every palette of ours that loads more colours than its picture draws."""
    _, _, found = scan()
    return [(f["src"], "%d colours%s, loaded by sizeof(%s) at %s -- re-save it with the colours it draws" %
             (f["colours"], ", pixels 0..%d" % f["top"] if f["top"] is not None else " (vanilla's has %s)" %
              f["vanilla_colours"], f["sym"], ", ".join(f["where"])))
            for f in found if f["wrong"] and not f["vanilla"]]


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
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
