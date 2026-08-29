#!/usr/bin/env python3
"""
Generate the BOX sprites -- the thing that replaced the ball.

    python3 tools/genbox.py

vision.md 1.3 is unambiguous about what this object is:

    A box is a machine. Not a metaphor we are imposing -- it is sysadmin
    vernacular. I sshed into the box. ... You are offering the daemon a host.

So it is a small server unit you would ssh into: hard corners, a vent, an
indicator light. NOT a crate and NOT a cube -- both of those say *container*,
which is the reading 1.3 replaced. A container shape would undo the rename.

Generated rather than drawn, for the same reason the SGB borders were: at
16x16 and 8x8 this is geometry, and downsampling a generated illustration to
three pixels of head produces mush. See docs/sprite-prompts.md.

Values are PNG levels, and rgbgfx INVERTS: level 3 -> colour index 0, which
for a sprite is TRANSPARENT. So level 3 is the background and must stay clear.

  writes  engine/gfx/sprites/poke_ball.png   16x16, the box on the ground
          engine/gfx/battle/balls.png        32x8, four throw frames
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import write_png

BG, LIGHT, MID, INK = 3, 2, 1, 0

def blank(w, h): return [[BG]*w for _ in range(h)]

def rect(g, x0, y0, x1, y1, edge=INK, fill=None):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            on_edge = x in (x0, x1) or y in (y0, y1)
            if on_edge: g[y][x] = edge
            elif fill is not None: g[y][x] = fill

def hline(g, x0, x1, y, v):
    for x in range(x0, x1+1): g[y][x] = v

def overworld(tier=0):
    """The box as it sits on the ground. tier raises the vent count -- the
    USERBOX -> ROOTBOX ladder is a parameter, not four drawings (1.3, 1.4)."""
    g = blank(16, 16)
    rect(g, 3, 4, 12, 12, edge=INK, fill=LIGHT)     # the chassis
    hline(g, 4, 11, 5, MID)                          # top bevel, so it reads solid
    vents = 2 + tier                                 # privilege shows as density
    y = 7
    for _ in range(vents):
        if y >= 11: break
        hline(g, 5, 8, y, INK)                       # vents on the left of the face
        y += 2
    g[7][10] = INK                                   # indicator, clear of the edge
    for x in (4, 5, 10, 11): g[13][x] = INK          # feet
    return g

def battle():
    """Four 8x8 frames: closed, struck, opening, dispersed. It stays the same
    object -- what changes is the seam -- so it reads as one thing opening
    rather than four unrelated shapes."""
    g = blank(32, 8)
    def chassis(ox, fill, seam=False):
        rect(g, ox+1, 1, ox+6, 6, edge=INK, fill=fill)
        hline(g, ox+2, ox+5, 2, MID)
        if seam: hline(g, ox+2, ox+5, 4, INK)

    chassis(0, LIGHT, seam=True)                     # 1 closed, seam visible

    for y in range(1, 7):                            # 2 struck: solid, the flash
        hline(g, 9, 14, y, INK)

    ox = 16                                          # 3 open: pulled apart
    rect(g, ox+1, 0, ox+6, 2, edge=INK, fill=LIGHT)
    rect(g, ox+1, 5, ox+6, 7, edge=INK, fill=LIGHT)

    for x, y in ((25,0),(30,0),(26,1),(29,1),         # 4 dispersed
                 (26,6),(29,6),(25,7),(30,7)):
        g[y][x] = INK
    return g

def show(g, label):
    print("=== %s ===" % label)
    for row in g: print('  ' + ''.join(' .:#'[3-v] for v in row))
    print()

def main():
    out_s = "engine/gfx/sprites/poke_ball.png"
    out_b = "engine/gfx/battle/balls.png"
    ow, bt = overworld(), battle()
    show(ow, "overworld box 16x16 -> %s" % out_s)
    show(bt, "battle frames 32x8 -> %s" % out_b)
    write_png(out_s, ow, 2)
    write_png(out_b, bt, 2)
    print("wrote both.")

if __name__ == "__main__":
    main()
