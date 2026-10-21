#!/usr/bin/env python3
"""T-431 P2: the SUMMARY's fourth page -- its frame, its colours and the grid's palette.

    python3 tools/gbafeelingspage.py            # report what would change
    python3 tools/gbafeelingspage.py --write    # write the three files below into engineGba/graphics/summary_screen/

The page (bible 4.9, docs/private/plan-feelings-2026-10-21.md section 3) draws a daemon's feelings and names none of
them: a 9x9 grid in the right pane, a dot whose place is GLAD - SAD across and CALM up, whose hue is MAD and whose
saturation is friendship, and a line of behaviour in the bottom pane. Its title bar is blank (the user, 2026-10-21).

  page_feelings.bin   its frame, made from vanilla's SKILLS frame (page_skills.bin): the same L of right and bottom
                      panels with every label and box taken out -- the right pane a plain field under a top border,
                      the bottom one a plain field over its bottom border -- and every tile moved to BG palette 5.
                      The grid and the line are drawn on top, in BG0 windows (src/pokemon_summary_screen.c).
  page_feelings.pal   BG palette 5: the SKILLS frame's sixteen colours by role, in a quiet blue-grey -- no page
                      colour of its own to read as a feeling (invariant 5: colour carries the argument, and here the
                      argument is the dot's).
  feelings_grid.pal   BG palette 9, the grid's and the line's window: paper, the cell lines, the centre cross, the
                      border, the ink and its shadow; entry 15 is the dot, rewritten for each daemon in the game.

All three are derived (the frame from vanilla's tiles, the palettes typed here once), so this is re-run, not edited.
"""
import os, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "engineGba", "graphics", "summary_screen")
W, H = 32, 20
PAL = 5                      # the frame's BG palette slot (0-4 are the summary's, 6-8 its text)

# The SKILLS frame's tiles this page keeps (bg.png's numbering, as the .bin holds them).
LEFT_EDGE = 16               # the right pane's left border (col 14)
TOP = 2                      # a top border over the striped field
FIELD = 18                   # the striped field
BOTTOM_LEFT_EDGE = 3         # the bottom pane's left border
FOOT_CORNER, FOOT, FOOT_END = 469, 471, 472   # its bottom border

# Palette 3 (SKILLS, yellow) by role -> a blue-grey. 0 is transparent; 9, 10, 13 and 15 are the greys every page
# shares; 14 is white.
FRAME = ["f800f8", "b8c0d8", "c8d0e8", "e8ecf8", "98a0c0", "f4f6fc", "f4f6fc", "d8dcec",
         "e0e4f0", "788090", "606878", "b8c0d8", "98a0c0", "788090", "f8f8f8", "606878"]
GRID = ["000000",   # 0 transparent
        "f4f6fc",   # 1 paper
        "e2e6f2",   # 2 the cell lines, faint
        "c4cadc",   # 3 the centre cross, a little less faint
        "98a0c0",   # 4 the border
        "505868",   # 5 ink
        "d0d4e0",   # 6 its shadow
        "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000",
        "8890a0"]   # 15 the dot -- rewritten per daemon (Feelings_DotColour)


def frame():
    src = open(os.path.join(DIR, "page_skills.bin"), "rb").read()
    e = list(struct.unpack("<%dH" % (len(src) // 2), src))
    out = [0] * (W * H)

    def put(c, r, tile):
        out[r * W + c] = tile | (PAL << 12)

    for r in range(H):
        for c in range(W):
            if e[r * W + c] == 0 or c >= 30:
                continue
            if r < 12:                                   # the right pane, rows 2-11
                if c == 14:
                    put(c, r, LEFT_EDGE)
                elif c >= 15:
                    put(c, r, TOP if r == 2 else FIELD)
            elif r == 12:                                # the join: vanilla's border to the left, field to the right
                put(c, r, (e[r * W + c] & 0x3FF) if c <= 14 else FIELD)
            elif r < 19:                                 # the bottom pane, rows 13-18
                put(c, r, BOTTOM_LEFT_EDGE if c == 0 else FIELD)
            else:                                        # its bottom border
                put(c, r, FOOT_CORNER if c == 0 else FOOT_END if c == 29 else FOOT)
    return struct.pack("<%dH" % len(out), *out)


def jasc(colours):
    rows = ["JASC-PAL", "0100", str(len(colours))]
    for h in colours:
        rows.append("%d %d %d" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    return ("\r\n".join(rows) + "\r\n").encode()


def main():
    write = "--write" in sys.argv
    wants = {"page_feelings.bin": frame(), "page_feelings.pal": jasc(FRAME), "feelings_grid.pal": jasc(GRID)}
    changed = 0
    for name, data in wants.items():
        path = os.path.join(DIR, name)
        old = open(path, "rb").read() if os.path.exists(path) else None
        if old == data:
            print("  %-20s up to date" % name)
            continue
        changed += 1
        print("  %-20s %s" % (name, "written" if write else ("would be written" if old is None else "would change")))
        if write:
            open(path, "wb").write(data)
    if not changed:
        print("  nothing to write.")


if __name__ == "__main__":
    main()
