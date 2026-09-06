#!/usr/bin/env python3
"""Draw the BOX -- the object that replaced the ball -- at every size.

    python3 tools/gbabox.py [--write]

vision 1.3: a box is a MACHINE. Sysadmin vernacular, *I sshed into the box*.
You are not trapping a daemon, you are offering it a host, and it stays if
that host grants the privileges it needs.

So the object is a compute unit with a SCREEN, and the screen is the whole
argument: a container says the daemon is inside, a screen says the daemon is
RUNNING. That is also why the crate was wrong -- genbox.py banned cubes for
saying *container*, and glass is precisely what defeats that reading.

FOUR FEATURES KEEP IT OFF THE HANDHELD READING, deliberately: feet, a small
screen set HIGH rather than a large centred one, no buttons, and roughly
cubic proportions. Slate's museum of dead hardware is where that rhyme is
allowed to land -- on the exhibits, never on the object in your hand.

PRIVILEGE IS PIPS ON THE GLASS. USERBOX one, ROOTBOX four; GUESTBOX gets a
single DIM pip, because restricted temporary access is not zero access. This
replaces genbox.py's vent-density ladder, which never worked -- overworld()
breaks at y >= 11 before the third vent, so all four tiers rendered
byte-identical.

AND THE PNG DOES NOT CARRY THE COLOURS. Item icons take theirs from
graphics/items/icon_palettes/<name>.pal and trainers from palettes/<name>.pal
-- writing the PNG alone leaves the new art wearing the old object's palette.
The interface/ball throw sprites are the exception: they have no .pal and
gbagfx builds their .gbapal from the PNG itself.

  writes  graphics/items/icons/{poke,great,ultra,master,safari}_ball.png  24x24
          graphics/items/icon_palettes/<same>.pal
          graphics/interface/ball/{poke,great,ultra,master,safari}.png    16x48
          graphics/object_events/pics/misc/item_ball.png                  16x16
          graphics/trade/pokeball.png                                     16x192
          graphics/interface/ball_open.png                                16x16
          graphics/pokedex/caught_marker.png                              8x8
"""
import os, sys, math
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

# greyscale, invariant 5. 0 transparent, then outline / shadow / face / bevel,
# then the glass dark and the glass lit.
KEY, INK, DARK, FACE, LIT, GLASS, PIP = 0, 1, 2, 3, 4, 5, 6
PAL = {
    KEY:   (115, 197, 164),      # what vanilla puts in the transparent slot
    INK:   ( 24,  24,  28),
    DARK:  ( 82,  86,  90),
    FACE:  (140, 145, 150),
    LIT:   (198, 203, 208),      # the top bevel
    GLASS: ( 44,  48,  54),
    PIP:   (226, 232, 236),
}

# USERBOX -> ADMINBOX -> SUPERBOX -> ROOTBOX, plus the Safari Zone's GUESTBOX.
TIERS = {"poke": 1, "great": 2, "ultra": 3, "master": 4, "safari": 0}

def blank(w, h): return np.zeros((h, w), dtype=np.uint8)

def box(g, x0, y0, x1, y1, pips, sw=None, sh=None, vent=None, dim=False):
    """A chassis with a bevelled top and a small screen set HIGH.

    NO SEAM, and that is section 8 rather than a preference: the carried box
    has "no seam anywhere that would let it open", because 1.3 calls it a
    machine you offer a daemon as a host and a seam says CONTAINER. A daemon
    does not come out of the box -- it RUNS on it.

    A vent line takes the seam's place on the lower face. It says machine
    where the seam said lid, and it still stops the face being a blank slab."""
    g[y0:y1+1, x0:x1+1] = FACE
    g[y0:y0+2, x0+1:x1] = LIT                          # bevel -> reads solid
    g[y1-1, x0+1:x1] = DARK                            # shaded underside
    g[y0, x0:x1+1] = g[y1, x0:x1+1] = INK              # outline
    g[y0:y1+1, x0] = g[y0:y1+1, x1] = INK
    if vent is not None:
        for i in (0, 2):
            g[y0+vent+i, x0+2:x1-1] = DARK
    if sw is None:
        return
    sx0 = x0 + (x1 - x0 + 1 - sw) // 2                 # centred horizontally
    sy0 = y0 + 2 + max(1, (y1 - y0) // 8)              # HIGH, not centred
    g[sy0:sy0+sh, sx0:sx0+sw] = GLASS
    row, step = sy0 + sh // 2, 2
    span = max(1, pips) * step - 1
    px = sx0 + (sw - span + 1) // 2                        # pips centred on the glass
    for i in range(max(1, pips)):
        g[row, px + i * step] = DARK if (dim or not pips) else PIP

def feet(g, x0, x1, y):
    for x in (x0+1, x0+2, x1-2, x1-1): g[y, x] = INK

def icon(tier):
    """24x24 bag icon -- the size that teaches the player what the object is."""
    g = blank(24, 24)
    box(g, 4, 4, 19, 20, pips=tier, sw=10, sh=5, vent=12, dim=(tier == 0))
    feet(g, 4, 19, 21)
    return g

def overworld():
    """16x16, the box waiting on the ground. No pips -- nothing is running."""
    g = blank(16, 16)
    box(g, 3, 4, 12, 13, pips=0, sw=6, sh=3, vent=7)
    feet(g, 3, 12, 14)
    return g

def throw(tier):
    """16x48: three 16x16 frames, the third blank as in vanilla.

    Vanilla spins a ball, which looks the same from every angle. A box does
    not -- so frame 1 is the FACE and frame 2 is the SIDE, same footprint and
    same height. Keeping the size identical is what sells it as one object
    turning rather than two objects; only the screen goes away."""
    g = blank(16, 48)
    box(g[0:16], 3, 3, 12, 12, pips=tier, sw=6, sh=4, vent=7, dim=(tier == 0))
    box(g[16:32], 4, 3, 11, 12, pips=0, vent=7)          # side: no glass
    return g

def opened():
    """16x16, graphics/interface/ball_open.png -- the box OPEN.

    pokeball.c decompresses this straight into VRAM behind whatever ball
    palette is already loaded, so its indices have to be ours: it inherits
    interface/ball/poke.gbapal, which gbagfx builds from the PNG this tool
    writes. Same table, or it renders as confetti.

    The silhouette is unchanged and the SEAM is what opens -- the light comes
    from the gap, not the glass, which is the rule the 8x8 throw frames
    forced. The screen is lit here because this is the frame where something
    starts running."""
    g = blank(16, 16)
    box(g, 3, 1, 12, 14, pips=1, sw=6, sh=3, vent=None)
    g[8:10, 4:12] = PIP                                # the gap, spilling
    g[10, 4:12] = LIT
    feet(g, 3, 12, 15)
    return g

def spin():
    """16x192: twelve 16x16 frames, the bouncing box in the intro.

    src/oak_speech.c calls CreateTradePokeballSprite, so the object in
    Crystal's hand is the TRADE ball -- a separate graphic from the throw
    sprites, and one that spins through a full turn.

    A ball looks the same from every angle and a box does not, which makes
    this honest rather than harder: the front face narrows to an edge as it
    turns, then the BACK comes round with no screen on it. Height never
    changes, because a cube turning about a vertical axis does not get
    taller."""
    g = blank(16, 192)
    for i in range(12):
        c = math.cos(i * math.pi / 6)
        w = max(2, int(round(11 * abs(c))))
        x0 = 8 - w // 2
        f = g[i*16:(i+1)*16]
        sw = max(2, w - 4) if (c > 0.35 and w >= 6) else None
        box(f, x0, 4, x0 + w - 1, 15, pips=1,
            sw=sw, sh=3 if sw else None, vent=8)
    return g

def marker(lit):
    """8x8 Index marker. Bound = the screen is LIT, which is not a symbol for
    'caught' -- it is the daemon running on the host you gave it."""
    g = blank(8, 8)
    g[1:7, 0:8] = FACE
    g[1, 0:8] = g[6, 0:8] = INK
    g[1:7, 0] = g[1:7, 7] = INK
    g[3:6, 2:6] = PIP if lit else GLASS
    return g

def png(path, g, pal=PAL):
    im = Image.new("P", (g.shape[1], g.shape[0]))
    im.putdata(g.flatten().tolist())
    full = [0] * 768
    for i, c in pal.items(): full[i*3:i*3+3] = list(c)
    im.putpalette(full)
    return im

def jasc(path, pal, n=16):
    rows = [pal.get(i, (0, 0, 0)) for i in range(n)]
    with open(path, "w") as f:
        f.write("JASC-PAL\n0100\n%d\n" % n)
        for c in rows: f.write("%d %d %d\n" % c)

def show(g, label):
    print("  %s" % label)
    ch = {KEY:' ', INK:'#', DARK:'+', FACE:'=', LIT:'-', GLASS:'%', PIP:'o'}
    for row in g: print('    ' + ''.join(ch[v] for v in row))
    print()

def main():
    jobs = []
    for name, tier in TIERS.items():
        jobs.append(("graphics/items/icons/%s_ball.png" % name, icon(tier),
                     "graphics/items/icon_palettes/%s_ball.pal" % name))
        jobs.append(("graphics/interface/ball/%s.png" % name, throw(tier), None))
    # NOT this one -- see the remap below.
    jobs.append(("graphics/trade/pokeball.png", spin(), None))
    jobs.append(("graphics/interface/ball_open.png", opened(), None))

    show(icon(1), "USERBOX 24x24 bag icon")
    show(icon(4), "ROOTBOX 24x24 bag icon")
    show(overworld(), "on the ground 16x16")
    show(marker(False), "Index, unbound 8x8"); show(marker(True), "Index, BOUND 8x8")

    prev = Image.new("RGB", (24*8*7, 48*8), (20, 20, 24))
    for i, (rel, g, pal) in enumerate(jobs + [("marker", marker(True), None)]):
        im = png(None, g).convert("RGB")
        prev.paste(im.resize((im.width*8, im.height*8), Image.NEAREST), ((i%7)*24*8, 0))
    prev.save("/tmp/box.png")

    for rel, g, pal in jobs:
        print("  %-52s %dx%d%s" % (rel, g.shape[1], g.shape[0], "  +.pal" if pal else ""))
        if WRITE:
            png(None, g).save(os.path.join(GBA, rel))
            if pal: jasc(os.path.join(GBA, pal), PAL)

    # THE OVERWORLD BOX SHARES A PALETTE WITH EVERY NPC. Its graphics_info
    # gives paletteTag = OBJ_EVENT_PAL_TAG_NPC_WHITE, so the colours come from
    # object_events/palettes/npc_white.gbapal and our indices 1..5 landed on
    # skin tones -- the lab tables came out tan boxes with rust lids. That
    # palette does carry greys further along, so the box is remapped into
    # them: 15 black, 13 dark, 12 mid, 11 light, 14 white.
    ow = os.path.join(GBA, "graphics/object_events/pics/misc/item_ball.png")
    src_ow = Image.open(ow)
    NPC = {KEY: 0, INK: 15, DARK: 13, FACE: 12, LIT: 11, GLASS: 15, PIP: 14}
    g = np.vectorize(lambda v: NPC.get(v, 12))(overworld()).astype(np.uint8)
    print("  %-52s 16x16 (npc_white, indices only)"
          % "graphics/object_events/pics/misc/item_ball.png")
    if WRITE:
        im = Image.new("P", (16, 16)); im.putdata(g.flatten().tolist())
        im.putpalette(src_ow.getpalette()); im.save(ow)

    # the caught marker keeps the Index's OWN palette -- indices only
    mp = os.path.join(GBA, "graphics/pokedex/caught_marker.png")
    src = Image.open(mp)
    m = marker(True)
    remap = {KEY:0, INK:6, FACE:3, GLASS:6, PIP:2}       # into the Index's palette
    out = np.vectorize(lambda v: remap.get(v, 3))(m).astype(np.uint8)
    print("  %-52s 8x8   (Index palette, indices only)"
          % "graphics/pokedex/caught_marker.png")
    if WRITE:
        im = Image.new("P", (8, 8)); im.putdata(out.flatten().tolist())
        im.putpalette(src.getpalette()); im.save(mp)
        print("\n  written.")
    print("  preview   /tmp/box.png")

main()
