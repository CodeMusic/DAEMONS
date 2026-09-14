#!/usr/bin/env python3
"""The move menu: every move coloured by its TYPE and marked by what it DOES.

    python3 tools/gbamovemenu.py [--write] [--text-step lightest]

Decided 2026-09-13 in docs/type-chart.html, and that page is the source for
everything here -- this imports its classifier, its marks and its colour
helpers rather than keeping a second copy that could drift from what the page
tells a reader.

Two channels, because a move answers two questions:

  COLOUR IS THE TYPE. Step 4 of the type's ramp, the same step the chart gives
  a type badge's ground, written on the white battle box. ORACLE has no hue
  and keeps the box's own grey.

  A MARK IS WHAT IT DOES. A 4px glyph in front of the name: blank for a move
  that hits, and one shape each for RAISE, LOWER, AFFLICT, MEND, GUARD and
  OTHER. Four pixels because the font's own arrows are eight and would push
  fourteen names out of their slot.

WHAT IT WRITES
  engineGba/src/data/battle_move_menu.h
      the colour per type, the class per move, the glyph per class
  engineGba/graphics/fonts/latin_small.png
      seven font cells nothing in the game uses, redrawn as the marks.
      FONT_SMALL only; the build regenerates latin_small.hwlatfont from this.

--text-step lightest writes each type in its lightest colour that still clears
4.5:1 on white -- the hue itself for the dark types -- instead of step 4. The
chart measures both; this is the switch.
"""
import importlib.util, os, re, struct, sys, zlib

WRITE = "--write" in sys.argv
LIGHTEST = "--text-step" in sys.argv and sys.argv[sys.argv.index("--text-step") + 1:][:1] == ["lightest"]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA = os.path.join(ROOT, "engineGba")
HEADER = os.path.join(GBA, "src/data/battle_move_menu.h")
FONT = os.path.join(GBA, "graphics/fonts/latin_small.png")

_spec = importlib.util.spec_from_file_location("gbachart", os.path.join(HERE, "gbachart.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

CELL_W, CELL_H, PER_ROW = 8, 16, 32
GROUND_ROWS = range(1, 13)     # the rows a 4px cell fills with the text ground
GROUND_COLS = range(0, 4)
INK, SHADOW, GROUND, CLEAR = 1, 2, 3, 0


def png_load(p):
    d = open(p, "rb").read(); i = 8; idat = b""; hdr = None; plte = None
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]; t = d[i+4:i+8]; c = d[i+8:i+8+ln]
        if t == b"IHDR": hdr = struct.unpack(">IIBBBBB", c)
        elif t == b"PLTE": plte = c
        elif t == b"IDAT": idat += c
        i += 12 + ln
    w, h, bd = hdr[0], hdr[1], hdr[2]
    raw = zlib.decompress(idat); stride = (w * bd + 7) // 8
    out = bytearray(); prev = bytearray(stride); o = 0
    for _ in range(h):
        f = raw[o]; o += 1; line = bytearray(raw[o:o+stride]); o += stride
        for x in range(stride):
            a = line[x-1] if x >= 1 else 0
            b = prev[x]; c2 = prev[x-1] if x >= 1 else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pp = a + b - c2; pa, pb, pc = abs(pp-a), abs(pp-b), abs(pp-c2)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c2)) & 255
        out += line; prev = line
    per, mask = 8 // bd, (1 << bd) - 1
    px = [[(out[y*stride + x // per] >> (8 - bd - bd * (x % per))) & mask for x in range(w)]
          for y in range(h)]
    return w, h, bd, plte, px


def png_save(p, w, h, bd, plte, px):
    """AT THE ORIGINAL BIT DEPTH. gbatypes' writer saves 8-bit, which is right
    for its sheet; the font is 2-bit and the font converter is not the place
    to find out whether it minds."""
    per = 8 // bd
    raw = bytearray()
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
    open(p, "wb").write(b"\x89PNG\r\n\x1a\n"
        + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, bd, 3, 0, 0, 0))
        + ch(b"PLTE", plte) + ch(b"IDAT", zlib.compress(bytes(raw), 9)) + ch(b"IEND", b""))


def cell_pixels(cls):
    """The 8x16 cell exactly as the font's own 4px cells are laid out: ground
    in rows 1-12 of the first four columns, ink, and a shadow cast right, down
    and down-right -- the rule read off the font's own letters."""
    top, rows = C.MARK_BITMAP[cls]
    g = [[CLEAR] * CELL_W for _ in range(CELL_H)]
    for y in GROUND_ROWS:
        for x in GROUND_COLS:
            g[y][x] = GROUND
    ink = {(x, top + r) for r, line in enumerate(rows) for x, chx in enumerate(line) if chx == "#"}
    for x, y in ink:
        g[y][x] = INK
    for x, y in ink:
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in ink and nx in GROUND_COLS and ny in GROUND_ROWS:
                g[ny][nx] = SHADOW
    return g


def rgb5(c):
    return tuple(round(v * 31 / 255) for v in c)


def main():
    tn, _ = C.load_types()
    shipped, coeffs = C.load_hues(tn)
    _, cm, tables = C.load_font()
    moves = C.classify_moves(tn)
    small = tables["sFontSmallLatinGlyphWidths"]

    # ------------------------------------------------------------ colours
    colours = []
    for key, ours in tn.items():
        if ours in shipped:
            hue = shipped[ours]
            col = C.ramp_step(hue, coeffs)[3]
            how = "step 4"
            if LIGHTEST and C.contrast(C.gba(hue), C.WHITE) >= 4.5:
                col, how = hue, "hue"
            colours.append((key, ours, rgb5(col), how))
        else:
            colours.append((key, ours, rgb5(C.PLAIN_TEXT), "no hue: the box's grey"))
    missing = [o for _, o, _, h in colours if h.startswith("no hue")]
    print("  colours: %d types, %s%s" % (len(colours), "lightest readable step" if LIGHTEST else "step 4",
          ("; no hue for " + ", ".join(missing)) if missing else ""))

    # ------------------------------------------------------------- glyphs
    glyph = {}
    for cls in C.CATEGORY_ORDER:
        ch = C.CLASS_GLYPH[cls]
        code = cm.get(ch)
        if code is None:
            sys.exit("  !!  %s's glyph %r is not in charmap.txt" % (cls, ch))
        if small[code] != 4:
            sys.exit("  !!  %s's glyph %r is %dpx in FONT_SMALL, not 4" % (cls, ch, small[code]))
        glyph[cls] = code
    #  Nothing a player reads may already use these cells.
    used = {}
    for base in ("data", "src"):
        for dp, _, fs in os.walk(os.path.join(GBA, base)):
            for f in fs:
                if f.endswith((".inc", ".s", ".c", ".h", ".json")) and os.path.join(dp, f) != HEADER:
                    t = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
                    for cls, ch in C.CLASS_GLYPH.items():
                        if ch in t:
                            used.setdefault(ch, []).append(os.path.relpath(os.path.join(dp, f), GBA))
    if used:
        for ch, where in used.items():
            print("  !!  %r is already used in %s" % (ch, ", ".join(where[:3])))
        sys.exit(1)
    print("  glyphs: " + ", ".join("%s 0x%02X" % (c, glyph[c]) for c in C.CATEGORY_ORDER) + "; none used by any text")

    counts = {c: sum(1 for m in moves.values() if m[0] == c) for c in C.CATEGORY_ORDER}
    print("  moves: %d, " % len(moves) + ", ".join("%s %d" % (c, counts[c]) for c in C.CATEGORY_ORDER))

    # ------------------------------------------------------------- header
    L = ["// GENERATED by tools/gbamovemenu.py -- do not edit by hand. Decided in",
         "// docs/type-chart.html, 2026-09-13: a move's COLOUR is its type, and a",
         "// 4px MARK before its name says what it does.",
         "#ifndef GUARD_DATA_BATTLE_MOVE_MENU_H",
         "#define GUARD_DATA_BATTLE_MOVE_MENU_H",
         "",
         '#include "constants/moves.h"',
         '#include "constants/pokemon.h"',
         "",
         "enum",
         "{"]
    L += ["    MOVE_CLASS_%s," % c for c in C.CATEGORY_ORDER]
    L += ["    MOVE_CLASS_COUNT", "};", "",
          "// The glyph each class draws. These are FONT_SMALL cells nothing else uses,",
          "// redrawn as the marks; HIT's is blank so the names stay in one column.",
          "static const u8 sMoveClassGlyph[MOVE_CLASS_COUNT] =", "{"]
    L += ["    [MOVE_CLASS_%-7s] = 0x%02X," % (c, glyph[c]) for c in C.CATEGORY_ORDER]
    L += ["};", "",
          "// Each type as a word on the white battle box: %s of its ramp."
          % ("the lightest step that clears 4.5:1" if LIGHTEST else "step 4"),
          "static const u16 sMoveMenuTypeTextColor[] =", "{"]
    for key, ours, (r, g, b), how in colours:
        L.append("    [TYPE_%-8s] = RGB(%2d, %2d, %2d), // %s%s" % (key, r, g, b, ours,
                 "" if how in ("step 4", "hue") else " -- " + how))
    L += ["};", "",
          "// What every move does. A move not listed hits (MOVE_CLASS_HIT is 0).",
          "static const u8 sMoveClass[MOVES_COUNT] =", "{"]
    for mv, (cls, ty, pw, name) in sorted(moves.items()):
        if cls != "HIT":
            L.append("    [MOVE_%-16s] = MOVE_CLASS_%-7s // %s" % (mv, cls + ",", name))
    L += ["};", "", "#endif // GUARD_DATA_BATTLE_MOVE_MENU_H", ""]
    header = "\n".join(L)
    old = open(HEADER, encoding="utf-8").read() if os.path.exists(HEADER) else None
    print("  header: %s" % ("unchanged" if old == header else "would change" if not WRITE else "written"))

    # --------------------------------------------------------------- font
    w, h, bd, plte, px = png_load(FONT)
    changed = 0
    for cls in C.CATEGORY_ORDER:
        code = glyph[cls]
        cx, cy = (code % PER_ROW) * CELL_W, (code // PER_ROW) * CELL_H
        want = cell_pixels(cls)
        for y in range(CELL_H):
            for x in range(CELL_W):
                if px[cy + y][cx + x] != want[y][x]:
                    px[cy + y][cx + x] = want[y][x]; changed += 1

    if WRITE:
        open(HEADER, "w", encoding="utf-8").write(header)
        if changed:
            png_save(FONT, w, h, bd, plte, px)
        #  Read it back rather than trusting the writer.
        _, _, bd2, _, px2 = png_load(FONT)
        bad = [cls for cls in C.CATEGORY_ORDER
               if [[px2[(glyph[cls] // PER_ROW) * CELL_H + y][(glyph[cls] % PER_ROW) * CELL_W + x]
                    for x in range(CELL_W)] for y in range(CELL_H)] != cell_pixels(cls)]
        if bad or bd2 != bd:
            sys.exit("  !!  font read back wrong: %s, depth %d" % (bad, bd2))
        print("  font: %d pixels redrawn in %d cells, read back at %d-bit and verified" % (changed, len(glyph), bd2))
    else:
        print("  font: %d pixels would change" % changed)
        print("  (report only; pass --write)")


if __name__ == "__main__":
    main()
