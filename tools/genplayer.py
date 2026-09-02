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

# Written out frame by frame rather than composed from parts. A first version
# built them from a shared head and a coat() helper, and the helper quietly made
# the side view the front view with a different face -- walking left looked like
# walking towards you. Art is not the place to be clever about repetition.
#
# The coat carries two of the three archetypes on its own: a lab coat and a
# wizard's robe are the same silhouette. So the hat only has to carry the third,
# and a flat brim WIDER THAN THE SHOULDERS is the widest shape on the figure and
# the one thing no vanilla NPC has. Brim the same width as the shoulders stacks
# into a mailbox; the overhang is what makes it a hat.
#
# The arms took three tries. Flush black columns read as outline -- the first
# version had no arms at all. Separating them from the torso with a transparent
# column read as a hole punched through the armpit. What works is keeping them
# INSIDE the silhouette and separating them by TONE: sleeves at level 2, torso
# at level 1, and the satchel strap a level 0 diagonal that cannot be confused
# with either.
#
# The coat is long, so the walk is the hem swinging -- but a hem alone slides.
# Without something to read a step against, the figure reads as a blob moving,
# which is exactly what it did. So the coat stops one row short of the floor and
# the shoes below it carry the stride: together when standing, apart when
# walking. One row of pixels, and it is the difference between walking and
# gliding.

HAT       = ["      ####      ", "     #::::#     ", "     #::::#     ",
             "################", "   ##########   "]
HAT_SIDE  = ["     ####       ", "    #::::#      ", "    #::::#      ",
             "##############  ", "   #########    "]
FACE      = ["   #.#....#.#   ", "   #........#   ", "    ########    "]
NAPE      = ["   #::::::::#   ", "   #:::..:::#   ", "    ########    "]
PROFILE   = ["   #.#.....#    ", "   #.......#    ", "    #######     "]

# Sleeves light, torso mid, strap black. The strap runs shoulder to opposite hip.
FRONT = ["  #..::::#:..#  ", "  #..:::#::..#  ", "  #..::#:::..#  ",
         "  #..:#::::..#  "]
# From behind it is the satchel itself, not the strap.
BACK  = ["  #..::::::..#  ", "  #..:####:..#  ", "  #..:#..#:..#  ",
         "  #..:####:..#  "]
# In profile the figure is narrower and only the near sleeve shows.
PROF  = ["   #..::::#:#   ", "   #..:::#::#   ", "   #..::#:::#   ",
         "   #..:#::::#   "]

HEM        = ["  #::::::::::#  ", " #::::::::::::# ", " ############## "]
HEM_LEFT   = [" #::::::::::#   ", "#::::::::::::#  ", "##############  "]
HEM_RIGHT  = ["   #::::::::::# ", "  #::::::::::::#", "  ##############"]
HEM_TRAIL  = ["   #:::::::::#  ", "  #::::::::::::#", "  ##############"]

FEET       = ["    ###  ###    "]   # both down
FEET_STEP  = ["   ###    ##    "]   # one out, one trailing
FEET_BACK  = ["    ##  ###     "]
FEET_PROF  = ["   ######       "]   # in profile, one shoe hides the other
FEET_STRIDE= ["  ###   ###     "]

DOWN      = HAT      + FACE    + FRONT + HEM       + FEET
DOWN_WALK = HAT      + FACE    + FRONT + HEM_LEFT  + FEET_STEP
UP        = HAT      + NAPE    + BACK  + HEM       + FEET
UP_WALK   = HAT      + NAPE    + BACK  + HEM_RIGHT + FEET_BACK
SIDE      = HAT_SIDE + PROFILE + PROF  + HEM_TRAIL + FEET_PROF
SIDE_WALK = HAT_SIDE + PROFILE + PROF  + HEM_LEFT  + FEET_STRIDE

# Provisional -- the bicycle itself is under review. Same head and same coat, so
# whatever replaces it inherits a character that already matches.
WHEEL = ["  ############  ", "  #::#::::#::#  ", "     #::::#     ",
         "     #:..:#     ", "      ####      "]
BIKE_DOWN = HAT      + FACE    + FRONT[:3] + WHEEL
BIKE_UP   = HAT      + NAPE    + BACK[:3]  + WHEEL
BIKE_SIDE = HAT_SIDE + PROFILE + PROF[:3]  + [
    "   #::::::::#   ", " ###::::::####  ", "#::#######::#   ",
    "#::#     #::#   ", " ##       ##    "]

def pedal(art):
    """The pedalling frame. Vanilla slides the whole bicycle sideways, which at
    16px reads as the rider lurching; this moves the wheels and swaps their tone,
    which is what spokes actually do."""
    return art[:12] + [r.replace(":", "\x00").replace(".", ":").replace("\x00", ".")
                       for r in art[12:]]

BIKE_DOWN_WALK = pedal(BIKE_DOWN)
BIKE_UP_WALK = pedal(BIKE_UP)
BIKE_SIDE_WALK = pedal(BIKE_SIDE)

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
