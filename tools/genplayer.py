#!/usr/bin/env python3
"""Draw the player's overworld sprite -- the figure you look at all game.

    python3 tools/genplayer.py [--show]

gfx/sprites/red.png is six 16x16 frames: down, up, side, then a walk frame for
each. Facing right is the side frame with OAM's x-flip, so there is no fourth
direction to draw. Level 3 is transparent; 0 is the outline, 1 and 2 the two
fills.

Hand-drawn, and it has to be. Every other pipeline in this project resamples a
large illustration down, which works at 40-56px and does not work at 16: a
generated figure loses its face, its silhouette and its walk cycle in the same
downsample. Sixteen pixels is one tile, and the sprite doc already rules out
generating anything under 16x16.

Deliberately in vanilla's idiom -- same height, same head-to-body ratio, same
two-tone shading, same outline weight. The player stands next to thirty NPC
sprites that are still vanilla's, and a figure drawn to a different set of rules
would read as a mistake rather than as a person. What changes is who it is:

    the cap sits brim-forward, not turned back
    a light strap crosses the chest, and the satchel it carries shows on the
      back when the player walks away from you

The strap is the one thing that does work at this size, and it is the right
detail to spend on: 1.3 says the box is a machine you offer a daemon as a host,
and the player is carrying one. It is on the strap in every frame that could
show it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import write_png

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
LV = {"#": 0, ":": 1, ".": 2, " ": 3}          # 3 is transparent for OBJ tiles

DOWN = [
    "     ######     ",
    "    #::::::#    ",
    "   #::::::::#   ",
    "   #::::::::#   ",
    "  ############  ",
    "   #.#....#.#   ",
    "   #........#   ",
    "  ############  ",
    "  ##:::::..:##  ",
    "  ##:::..:::##  ",
    "  ##:..:::::##  ",
    "  ##..::::::##  ",
    "   ##::::::##   ",
    "   #:##::##:#   ",
    "   #::#  #::#   ",
    "    ##    ##    ",
]
UP = [
    "     ######     ",
    "    #::::::#    ",
    "   #::::::::#   ",
    "   #::::::::#   ",
    "   #:::..:::#   ",
    "   #::::::::#   ",
    "   ##::::::##   ",
    "  ############  ",
    "  ##:#....#:##  ",
    "  ##:#....#:##  ",
    "  ##:#....#:##  ",
    "  ##::####::##  ",
    "   ##::::::##   ",
    "   #:##::##:#   ",
    "   #::#  #::#   ",
    "    ##    ##    ",
]
SIDE = [
    "      ######    ",
    "     #::::::#   ",
    "    #::::::::#  ",
    "   ##::::::::#  ",
    "  ###########   ",
    "   #.#.....##   ",
    "   #.......##   ",
    "   ##########   ",
    "   ##:::..:##   ",
    "   ##::..:###   ",
    "   ##:..::##    ",
    "   #::::::##    ",
    "   #:::::##     ",
    "   #:##::#      ",
    "   #:# #::#     ",
    "   ###  ###     ",
]
DOWN_WALK = [
    "                ",
    "     ######     ",
    "    #::::::#    ",
    "   #::::::::#   ",
    "   #::::::::#   ",
    "  ############  ",
    "   #.#....#.#   ",
    "   #........#   ",
    "  ############  ",
    "  ##:::::..:##  ",
    "  ##:::..:::##  ",
    "  ##:..:::::##  ",
    "   ##::::::##   ",
    "    #::##::#    ",
    "    ###  #::#   ",
    "         ###    ",
]
UP_WALK = [
    "                ",
    "     ######     ",
    "    #::::::#    ",
    "   #::::::::#   ",
    "   #::::::::#   ",
    "   #:::..:::#   ",
    "   ##::::::##   ",
    "  ############  ",
    "  ##:#....#:##  ",
    "  ##:#....#:##  ",
    "  ##::####::##  ",
    "   ##::::::##   ",
    "    #::##::#    ",
    "   #::#  ###    ",
    "    ###         ",
    "                ",
]
SIDE_WALK = [
    "                ",
    "      ######    ",
    "     #::::::#   ",
    "    #::::::::#  ",
    "   ##::::::::#  ",
    "  ###########   ",
    "   #.#.....##   ",
    "   #.......##   ",
    "   ##########   ",
    "   ##:::..:##   ",
    "   ##::..:###   ",
    "   ##:..::##    ",
    "   #::::::#     ",
    "  #::#::::#     ",
    " #::#  #::#     ",
    " ###    ###     ",
]

BIKE_DOWN = [
    "     ######     ",
    "    #::::::#    ",
    "   #::::::::#   ",
    "  ############  ",
    "   #.#....#.#   ",
    "   #........#   ",
    "  ############  ",
    "  ##:::::..:##  ",
    " ###::..::::### ",
    " #:#:..:::::#:# ",
    " #:##::::::##:# ",
    "  ############  ",
    "  #::#::::#::#  ",
    "     #::::#     ",
    "     #:..:#     ",
    "      ####      ",
]
BIKE_UP = [
    "     ######     ",
    "    #::::::#    ",
    "   #::::::::#   ",
    "   #:::..:::#   ",
    "   ##::::::##   ",
    "  ############  ",
    "  ##:#....#:##  ",
    "  ##:#....#:##  ",
    " ###::####::### ",
    " #:#::::::::#:# ",
    " #:##::::::##:# ",
    "  ############  ",
    "  #::#::::#::#  ",
    "     #::::#     ",
    "     #:..:#     ",
    "      ####      ",
]
BIKE_SIDE = [
    "      ######    ",
    "     #::::::#   ",
    "    #::::::::#  ",
    "  ###########   ",
    "   #.#.....##   ",
    "   #.......##   ",
    "   ##########   ",
    "   ##:::..:##   ",
    "  ###::..:####  ",
    "  #:#:..:::::#  ",
    "  ##::::::###   ",
    "  #::::::#      ",
    " ###::::####    ",
    "#::#######::#   ",
    "#::#     #::#   ",
    " ##       ##    ",
]

def wheel(art, dx, spin):
    """The bike frames differ only below the frame rail: the wheels move.

    Vanilla animates the whole bicycle sideways. At 16px that reads as the rider
    lurching, so this shifts the wheels instead and flickers their tone -- which
    is what spokes actually do."""
    out = []
    for y, row in enumerate(art):
        if y < 11:
            out.append(row); continue
        r = (" " * dx + row)[:16] if dx > 0 else (row[-dx:] + " " * -dx)
        if spin: r = r.replace(":", "\x00").replace(".", ":").replace("\x00", ".")
        out.append(r)
    return out

BIKE_DOWN_WALK = wheel(BIKE_DOWN, -1, True)
BIKE_UP_WALK = wheel(BIKE_UP, 1, True)
BIKE_SIDE_WALK = wheel(BIKE_SIDE, 0, True)

FRAMES = [("down", DOWN), ("up", UP), ("side", SIDE),
          ("down walk", DOWN_WALK), ("up walk", UP_WALK), ("side walk", SIDE_WALK)]

BIKE = [("down", BIKE_DOWN), ("up", BIKE_UP), ("side", BIKE_SIDE),
        ("down pedal", BIKE_DOWN_WALK), ("up pedal", BIKE_UP_WALK),
        ("side pedal", BIKE_SIDE_WALK)]

rows = []
for name, art in FRAMES:
    if len(art) != 16 or any(len(r) != 16 for r in art):
        sys.exit("%s is not 16x16" % name)
    rows += [[LV[c] for c in r] for r in art]
write_png(os.path.join(ENG, "gfx/sprites/red.png"), rows, 2)
print("  gfx/sprites/red.png 16x%d -- %s" % (len(rows), ", ".join(n for n, _ in FRAMES)))

rows = []
for name, art in BIKE:
    if len(art) != 16 or any(len(r) != 16 for r in art):
        sys.exit("bike %s is not 16x16" % name)
    rows += [[LV[c] for c in r] for r in art]
write_png(os.path.join(ENG, "gfx/sprites/red_bike.png"), rows, 2)
print("  gfx/sprites/red_bike.png 16x%d" % len(rows))

if "--show" in sys.argv:
    for name, art in FRAMES:
        print("\n" + name)
        for r in art: print("   " + r)
