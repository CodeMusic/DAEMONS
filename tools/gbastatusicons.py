#!/usr/bin/env python3
"""The status pills: PkRS becomes MEME, and the summary screen stops saying PSN (T-258, 2026-09-24).

    python3 tools/gbastatusicons.py            # report
    python3 tools/gbastatusicons.py --write     # interface/status_icons.png, summary_screen/status_ailment_icons.png

TWO SHEETS, ONE SET OF PILLS. interface/status_icons.png is the battle's and the party menu's, and it already
reads LEK THR SUS HNG OVR PkRS HLT -- the states port_states.py named. summary_screen/status_ailment_icons.png is
the SUMMARY's, and nothing had touched it: a daemon's own page still said PSN PAR SLP FRZ BRN PkRS FNT, the one
place the player looks at one daemon's state at rest. Found 2026-09-24 laying the two sheets side by side for MEME.
Both sheets hold seven 32x8 pills in the same order, so the summary's is now BUILT from the battle's, palette and
all, and cannot drift from it again.

PkRS -> MEME (the user's decision, 2026-09-24): a unit that spreads between minds by contact, which is what the
condition does. Four letters do not fit the pill's twenty pixels with the sheet's four-wide E, so MEME is set with
a three-wide E and the pill is widened by one pixel each side; M is drawn, since no pill has one.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
BATTLE = os.path.join(GBA, "graphics/interface/status_icons.png")
SUMMARY = os.path.join(GBA, "graphics/summary_screen/status_ailment_icons.png")
WRITE = "--write" in sys.argv
PILL = 5                                  # PkRS, in both sheets
M = ["#...#", "##.##", "#.#.#", "#...#", "#...#", "#...#"]
E = ["###", "#..", "##.", "#..", "#..", "###"]


def is_meme(px):
    x0 = PILL * 32
    return all(px[x0 + 5 + c, 1 + r] % 16 == 2 for r, row in enumerate(M) for c, v in enumerate(row) if v == "#")


def draw_meme(px):
    x0 = PILL * 32
    ink = px[x0 + 11, 1] - px[x0 + 11, 1] % 16 + 2       # ink is index 2 of the pill's own sixteen
    fill = px[x0 + 10, 4]
    edge = px[x0 + 6, 0]                                   # the pill's rim colour, top row
    fill = next(px[x, 4] for x in range(x0 + 8, x0 + 24) if px[x, 4] % 16 not in (0, 2))
    rim = px[x0 + 7, 0]
    for y in range(8):                                     # the pill, one pixel wider each side: x0+5 .. x0+26
        for x in range(x0 + 4, x0 + 28):
            px[x, y] = 0
        top_or_bottom = y in (0, 7)
        a, b = (x0 + 6, x0 + 25) if top_or_bottom else (x0 + 5, x0 + 26)
        for x in range(a, b + 1):
            px[x, y] = rim if (top_or_bottom or x in (a, b)) and (top_or_bottom and x in (a, b) or not top_or_bottom) else fill
        if top_or_bottom:
            for x in range(a + 1, b):
                px[x, y] = fill
    x = x0 + 7
    for glyph in (M, E, M, E):
        for r, row in enumerate(glyph):
            for c, v in enumerate(row):
                if v == "#":
                    px[x + c, 1 + r] = ink
        x += len(glyph[0]) + 1


def main():
    b = Image.open(BATTLE)
    bpx = b.load()
    changed = []
    if not is_meme_at(bpx):
        draw_meme(bpx)
        changed.append("battle   PkRS -> MEME")
    s = Image.open(SUMMARY)
    new = Image.new("P", s.size, 0)
    new.putpalette(b.getpalette())
    npx = new.load()
    for k in range(7):
        for y in range(8):
            for x in range(32):
                npx[x, k * 8 + y] = bpx[k * 32 + x, y]
    if list(new.getdata()) != list(s.getdata()) or new.getpalette()[:48] != s.getpalette()[:48]:
        changed.append("summary  rebuilt from the battle's pills (PSN PAR SLP FRZ BRN PkRS FNT -> LEK THR SUS HNG OVR MEME HLT)")
    for c in changed or ["both sheets already read LEK THR SUS HNG OVR MEME HLT"]:
        print("  " + c)
    if WRITE and changed:
        b.save(BATTLE)
        new.save(SUMMARY)
        print("  written")
    return 0


def is_meme_at(px):
    return is_meme_shape(px)


def is_meme_shape(px):
    x0 = PILL * 32 + 7
    for glyph_x, glyph in ((0, M), (6, E), (10, M), (16, E)):
        for r, row in enumerate(glyph):
            for c, v in enumerate(row):
                if (px[x0 + glyph_x + c, 1 + r] % 16 == 2) != (v == "#"):
                    return False
    return True


if __name__ == "__main__":
    sys.exit(main())
