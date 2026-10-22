#!/usr/bin/env python3
"""SCREEN, the DAEMONS typeface (T-437): our own Latin glyphs written into the engine's font sheets.

    python3 tools/gbafont.py                       # report: what would change, and every glyph checked
    python3 tools/gbafont.py --write --engine PATH  # write into that engine checkout (a draft worktree)
    python3 tools/gbafont.py --write                # write into engineGba -- refused while DRAFT (below)

DRAFT. Every glyph in gfx/fonts/screen_*.txt is new writing in pixels and unapproved: the user chose the SCREEN
direction on 2026-10-22 and asked for a draft ROM to judge on a real screen before it ships. Until then DRAFT is
True and a --write aimed at engineGba itself refuses (and exits 0, writing nothing, so check_generators' sandboxed
writes see no drift); a --write with --engine writes the checkout named. Set DRAFT = False when the user signs it
off.

The glyphs are drawn by hand, from scratch, on a grid. Nothing is traced from Nintendo's sheets; this tool reads
the existing sheets only to keep every cell it does not own exactly as it was.

WHAT IT WRITES (the engine's graphics/fonts/, 2-bit PNGs, at their own bit depth and palette)
    latin_normal.png, latin_male.png, latin_female.png   from screen_normal.txt -- one face, three identical
                                                         sheets, as FireRed ships them
    latin_small.png                                      from screen_small.txt
Only the cells of the glyphs in the source files. Every other cell -- the symbols, the F9 compressed cells, the LV
and arrow cells, the MP cell 0x106 (tools/gbamana.py) and the seven move-class marks in latin_small
(tools/gbamovemenu.py) -- is left byte for byte, and the write is read back to prove it. The space cell is not
drawn (it has nothing to draw), and neither is `$`, which is the string terminator 0xFF, not a glyph.

WHAT IT REFUSES
A drop-in: the width tables in src/text.c do not change, so every tool that measures a line (21 of them, through
tools/fontwidth.py) measures exactly what the player sees. So every glyph's ink AND its shadow must fit inside its
advance in every width table that sheet serves (normal = male = female = normal copy 1; small), and inside the
cell's ground rows (normal 0-13, small 1-12). One glyph out and nothing is written.

THE SHADOW is SCREEN's: one pixel straight below each ink pixel that has none (index 2), never to the right.
Cells: index 0 outside the glyph, 3 the ground (advance wide, the ground rows tall), 1 ink, 2 shadow.
"""
import os, re, struct, sys, zlib

DRAFT = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from fontwidth import charmap, all_glyph_widths  # noqa: E402

SRC = os.path.join(ROOT, "gfx", "fonts")
CLEAR, INK, SHADOW, GROUND = 0, 1, 2, 3

#  face -> (source, [sheets], cell width, cells per row, ground rows, width tables it must fit)
FACES = {
    "normal": ("screen_normal.txt", ["latin_normal", "latin_male", "latin_female"], 16, 16, range(0, 14),
               ["sFontNormalLatinGlyphWidths", "sFontMaleLatinGlyphWidths", "sFontFemaleLatinGlyphWidths",
                "sFontNormalCopy1LatinGlyphWidths"]),
    "small":  ("screen_small.txt", ["latin_small"], 8, 32, range(1, 13), ["sFontSmallLatinGlyphWidths"]),
}
CELL_H = 16


# ------------------------------------------------------------------------------------------------ source files
def parse(path):
    """[(char, top, rows)] from a source file: `== <char> <top>` then rows of '#' and '.'."""
    out, cur = [], None
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if line.startswith("//"):
            continue
        if line.startswith("== "):
            parts = line[3:].rsplit(" ", 1)
            if len(parts) != 2 or len(parts[0]) != 1 or not parts[1].lstrip("-").isdigit():
                sys.exit("  !!  %s:%d: a header is `== <one char> <top row>`: %r" % (path, n, line))
            cur = (parts[0], int(parts[1]), [])
            out.append(cur)
        elif line.strip():
            if cur is None or set(line) - {"#", "."}:
                sys.exit("  !!  %s:%d: a glyph row is '#' and '.' only, under a header: %r" % (path, n, line))
            cur[2].append(line)
    return out


def ink_of(top, rows):
    return {(x, top + y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "#"}


def shadow_of(ink):
    """SCREEN's shadow: straight down, under ink that has none."""
    return {(x, y + 1) for x, y in ink if (x, y + 1) not in ink}


def cell(top, rows, adv, cw, ground):
    """The cell as the sheet holds it: rows of palette indices, CELL_H x cw."""
    g = [[CLEAR] * cw for _ in range(CELL_H)]
    for y in ground:
        for x in range(min(adv, cw)):
            g[y][x] = GROUND
    ink = ink_of(top, rows)
    for x, y in shadow_of(ink):
        g[y][x] = SHADOW
    for x, y in ink:
        g[y][x] = INK
    return g


def check(face, glyphs, cm, tables):
    """Every problem with a face's glyphs, as lines; empty when it may be written."""
    _, _, cw, _, ground, names = FACES[face]
    bad, seen = [], {}
    for ch, top, rows in glyphs:
        if ch not in cm:
            bad.append("%r is not in charmap.txt" % ch)
            continue
        b = cm[ch]
        if b in seen:
            bad.append("%r and %r are the same cell, 0x%02X" % (seen[b], ch, b))
        seen[b] = ch
        ink = ink_of(top, rows)
        if not ink:
            bad.append("%r has no ink" % ch)
            continue
        px = ink | shadow_of(ink)
        for t in names:
            adv = tables[t][b]
            if max(x for x, _ in px) >= adv:
                bad.append("%r is %dpx with its shadow; %s gives it %d" % (ch, max(x for x, _ in px) + 1, t, adv))
                break
        if min(y for _, y in px) < ground[0] or max(y for _, y in px) > ground[-1]:
            bad.append("%r runs rows %d-%d; the %s ground is rows %d-%d" % (
                ch, min(y for _, y in px), max(y for _, y in px), face, ground[0], ground[-1]))
        if max(x for x, _ in px) >= cw:
            bad.append("%r is wider than the %dpx cell" % (ch, cw))
    return bad


# ----------------------------------------------------------------------------------------- 2-bit PNG, read/write
def png_load(p):
    d = open(p, "rb").read()
    i, idat, hdr, plte = 8, b"", None, None
    while i < len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        t, c = d[i + 4:i + 8], d[i + 8:i + 8 + ln]
        if t == b"IHDR":
            hdr = struct.unpack(">IIBBBBB", c)
        elif t == b"PLTE":
            plte = c
        elif t == b"IDAT":
            idat += c
        i += 12 + ln
    w, h, bd, ctype = hdr[0], hdr[1], hdr[2], hdr[3]
    if ctype != 3 or hdr[6]:
        sys.exit("  !!  %s is not a non-interlaced paletted PNG" % p)
    raw, stride = zlib.decompress(idat), (w * bd + 7) // 8
    out, prev, o = bytearray(), bytearray(stride), 0
    for _ in range(h):
        f = raw[o]; o += 1
        line = bytearray(raw[o:o + stride]); o += stride
        for x in range(stride):
            a = line[x - 1] if x else 0
            b = prev[x]
            c2 = prev[x - 1] if x else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pp = a + b - c2
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c2)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c2)) & 255
        out += line
        prev = line
    per, mask = 8 // bd, (1 << bd) - 1
    px = [[(out[y * stride + x // per] >> (8 - bd - bd * (x % per))) & mask for x in range(w)] for y in range(h)]
    return w, h, bd, plte, px


def png_save(p, w, h, bd, plte, px):
    """At the sheet's own bit depth and palette: gbagfx reads these, and is not the place to find out what it
    makes of an 8-bit font."""
    per, raw = 8 // bd, bytearray()
    for row in px:
        raw.append(0)
        for x in range(0, w, per):
            byte = 0
            for k in range(per):
                byte |= (row[x + k] if x + k < w else 0) << (8 - bd - bd * k)
            raw.append(byte)

    def ch(t, data):
        c = t + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    open(p, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, bd, 3, 0, 0, 0))
                        + ch(b"PLTE", plte) + ch(b"IDAT", zlib.compress(bytes(raw), 9)) + ch(b"IEND", b""))


# ------------------------------------------------------------------------------------------------------- the rest
def reserved(gba):
    """Cells other tools own, which no source glyph may land on: the MP cell (gbamana) and the move marks
    (gbamovemenu, whose glyphs gbachart names)."""
    out = {}
    m = re.search(r"^GLYPH\s*=\s*(0x[0-9A-Fa-f]+)", open(os.path.join(HERE, "gbamana.py"), encoding="utf-8").read(), re.M)
    if m:
        out[int(m.group(1), 16)] = "the MP cell (gbamana.py)"
    m = re.search(r"CLASS_GLYPH\s*=\s*\{(.*?)\}", open(os.path.join(HERE, "gbachart.py"), encoding="utf-8").read(), re.S)
    cm = charmap(gba)
    for cls, ch in re.findall(r'"(\w+)":\s*"(.)"', m.group(1) if m else ""):
        if ch in cm:
            out[cm[ch]] = "the %s move mark (gbamovemenu.py)" % cls
    return out


def main():
    write = "--write" in sys.argv
    gba = os.path.join(ROOT, "engineGba")
    named = "--engine" in sys.argv
    if named:
        gba = os.path.abspath(sys.argv[sys.argv.index("--engine") + 1])
    fonts = os.path.join(gba, "graphics", "fonts")
    if not os.path.isdir(fonts):
        sys.exit("  !!  no graphics/fonts in %s" % gba)
    cm, tables = charmap(gba), all_glyph_widths(gba)
    res = reserved(gba)
    print("  SCREEN (DRAFT, T-437) -> %s" % gba)

    plan, problems = [], []
    for face, (src, sheets, cw, per, ground, names) in FACES.items():
        glyphs = parse(os.path.join(SRC, src))
        bad = check(face, glyphs, cm, tables)
        bad += ["%r lands on %s" % (c, res[cm[c]]) for c, _, _ in glyphs if cm.get(c) in res]
        problems += ["%s: %s" % (face, b) for b in bad]
        widest = max(len(r) for _, _, rows in glyphs for r in rows)
        print("  %s: %d glyphs from gfx/fonts/%s, ink up to %dpx; every one inside its advance in %s"
              % (face, len(glyphs), src, widest, ", ".join(n.replace("sFont", "").replace("LatinGlyphWidths", "")
                                                              for n in names)) if not bad else
              "  %s: %d glyphs, %d problems" % (face, len(glyphs), len(bad)))
        plan.append((face, glyphs, sheets, cw, per, ground, tables[names[0]]))
    if problems:
        for p in problems:
            print("  !!  " + p)
        sys.exit("  refused: nothing written")

    if write and DRAFT and not named:
        print("  refused: SCREEN is a DRAFT until the user signs it off; engineGba was not written. Pass --engine PATH"
              " to write a draft checkout, or set DRAFT = False in this file once it is approved.")
        return 0

    for face, glyphs, sheets, cw, per, ground, adv in plan:
        cells = {cm[c]: cell(top, rows, adv[cm[c]], cw, ground) for c, top, rows in glyphs}
        for sheet in sheets:
            path = os.path.join(fonts, sheet + ".png")
            w, h, bd, plte, px = png_load(path)
            before = [row[:] for row in px]
            changed = 0
            for b, g in cells.items():
                x0, y0 = (b % per) * cw, (b // per) * CELL_H
                for y in range(CELL_H):
                    for x in range(cw):
                        if px[y0 + y][x0 + x] != g[y][x]:
                            px[y0 + y][x0 + x] = g[y][x]
                            changed += 1
            if not write:
                print("    %s.png: %d pixels in %d cells would change" % (sheet, changed, len(cells)))
                continue
            if changed:
                png_save(path, w, h, bd, plte, px)
            #  Read it back: the glyphs are what was drawn, and every cell this does not own is what it was.
            _, _, bd2, plte2, px2 = png_load(path)
            owned = {(x, y) for b in cells for y in range((b // per) * CELL_H, (b // per + 1) * CELL_H)
                     for x in range((b % per) * cw, (b % per + 1) * cw)}
            if bd2 != bd or plte2 != plte or px2 != px:
                sys.exit("  !!  %s.png read back wrong" % sheet)
            if any(px2[y][x] != before[y][x] for y in range(h) for x in range(w) if (x, y) not in owned):
                sys.exit("  !!  %s.png: a cell this does not own changed" % sheet)
            print("    %s.png: %d pixels in %d cells written, read back at %d-bit; every other cell untouched"
                  % (sheet, changed, len(cells), bd2))
    if not write:
        print("  (report only; pass --write --engine PATH)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
