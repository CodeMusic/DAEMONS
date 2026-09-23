#!/usr/bin/env python3
"""Two painted labels that still said vanilla's word (2026-09-23).

    python3 tools/gbalabels.py            # report
    python3 tools/gbalabels.py --write    # summary_screen/bg.png, interface/menu_info.png

Found by the sweep that followed the storage screen's PKMN DATA (tools/genstoragelabels.py): every UI sheet
laid out on a contact sheet and read by eye, because a painted word is invisible to every text tool we have.

  TRAINER MEMO -> USER MEMO   summary_screen/bg.png, the pill over the INFO page's memo. TRAINER -> USER is
                              port_vocab's rename; the pill's own face already has E, R, M and O, SPEED gives
                              the S, and U is drawn to match O.
  PP -> MP                    interface/menu_info.png, the label in the move relearner's info pane
                              (learn_move.c, MENU_INFO_ICON_PP). The summary already says MP; its M is lifted
                              from MEMO above -- the two faces are the same 7-row face.

Both sheets are also written by other tools (gbatypes, gbabox, the states tile), so this edits IN PLACE and is
idempotent by reading what is there: a pill that already says the new word is left alone.

The outline is rebuilt, not copied: every pixel 8-adjacent to a letter takes the outline colour. Measured against
vanilla's TRAINER MEMO before writing a pixel, that rule misses one pixel of 60 and adds none.
(The card's own TRAINER: is tools/gbacard.py's, beside USER CARD and MARKS.)
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
N8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]


def glyphs(px, x0, x1, y0, h, ink):
    """Letters as lists of '#'/'.' rows, split on the empty columns between them."""
    cols = [x for x in range(x0, x1) if any(px[x, y] == ink for y in range(y0, y0 + h))]
    runs = []
    for x in cols:
        if runs and x == runs[-1][1] + 1:
            runs[-1][1] = x
        else:
            runs.append([x, x])
    return [["".join("#" if px[x, y] == ink else "." for x in range(a, b + 1)) for y in range(y0, y0 + h)]
            for a, b in runs], runs


def relabel(px, text, font, x, y0, h, span, ref, ink, edge, space=3):
    """Clear span (rows y0-1 .. y0+h) to the pill's plain rows, read at column ref; set text from x; outline it."""
    for yy in range(y0 - 1, y0 + h + 1):
        v = px[ref, yy]
        for xx in range(span[0], span[1] + 1):
            px[xx, yy] = v
    lit = set()
    for ch in text:
        if ch == " ":
            x += space
            continue
        g = font[ch]
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == "#":
                    lit.add((x + c, y0 + r))
        x += len(g[0]) + 1
    for (lx, ly) in lit:
        px[lx, ly] = ink
    for (lx, ly) in lit:
        for a, b in N8:
            p = (lx + a, ly + b)
            if p not in lit and y0 - 1 <= p[1] <= y0 + h:
                px[p] = edge
    return x - 2                                        # the last column lit


def main():
    out = []
    # ---- summary_screen/bg.png: TRAINER MEMO -> USER MEMO. Letters 0x2E on the pill's 0x2D (palette row 2).
    sp = os.path.join(GBA, "graphics/summary_screen/bg.png")
    sim = Image.open(sp); spx = sim.load()
    g, runs = glyphs(spx, 48, 128, 8, 7, 0x2E)
    font = {}
    if len(g) == 11:                                    # TRAINER MEMO
        font.update(zip("TRAINERMEMO", g))
        font["S"] = glyphs(spx, 0, 48, 196, 7, 14 + 16 * (spx[13, 196] >> 4))[0][0]  # SPEED's S, its own palette row
        font["U"] = ["#..#"] * 6 + [".##."]
        width = sum(len(font[c][0]) + 1 for c in "USERMEMO") - 1 + 3    # vanilla's word gap is 4 columns
        mid = (runs[0][0] + runs[-1][1]) // 2
        end = relabel(spx, "USER MEMO", font, mid - width // 2, 8, 7, (runs[0][0] - 1, runs[-1][1] + 1), 57, 0x2E, 0x2D)
        out.append("summary  TRAINER MEMO -> USER MEMO (x %d..%d)" % (mid - width // 2, end))
        g, runs = glyphs(spx, 48, 128, 8, 7, 0x2E)
    elif len(g) == 8:
        out.append("summary  already USER MEMO")
    else:
        raise SystemExit("summary_screen/bg.png: %d glyphs in the memo pill, expected 11 or 8" % len(g))
    M = g[-4]                                           # MEMO's M, in either state
    assert len(M[0]) == 5, M

    # ---- interface/menu_info.png: PP -> MP. Letters 0x1F on pill 0x1E, rows 115..121.
    mp = os.path.join(GBA, "graphics/interface/menu_info.png")
    mim = Image.open(mp); mpx = mim.load()
    mg, mruns = glyphs(mpx, 0, 40, 115, 7, 0x1F)
    if len(mg) == 2 and mg[0] == mg[1]:                 # PP
        end = relabel(mpx, "MP", {"M": M, "P": mg[0]}, 14, 115, 7, (mruns[0][0] - 1, mruns[-1][1] + 1), 30, 0x1F, 0x1E)
        out.append("relearner PP -> MP (x 14..%d)" % end)
    elif len(mg) == 2 and len(mg[0][0]) == 5:
        out.append("relearner already MP")
    else:
        raise SystemExit("menu_info.png: the PP pill is not PP or MP (%d glyphs)" % len(mg))

    for line in out:
        print("  " + line)
    changed = any("->" in l for l in out)
    if WRITE and changed:
        sim.save(sp)
        mim.save(mp)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
