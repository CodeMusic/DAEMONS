#!/usr/bin/env python3
"""TULIKKO, the arctic fox who sweeps the snow by STILLFALL CAVE on FOUR ISLAND (T-528 (e), vision.md 4.40).

    python3 tools/gentulikko.py            # report: is the sheet current and registered
    python3 tools/gentulikko.py --write    # tulikko.png, its spritesheet rule, and OBJ_EVENT_GFX_TULIKKO

After the Finnish revontulet, "fox fires": a fox whose tail, sweeping the snow, throws sparks into the sky. Every
person is an animal (the fable rule), and this one is an animal on four feet -- not one of the town's upright folk,
because it is doing what a fox does.

DRAWN BY HAND, IN CODE: no image is generated or traced. Each view is built from a few shapes on a 32x32 grid --
the body, the head, two ears, the snout, four legs and the great tail -- laid as masks, then given an outline where a
shape meets the empty ground, a light-grey underside, black eyes and nose. Arctic white, so it reads against FOUR
ISLAND's grass and the cave's ice alike.

NINE FRAMES, vanilla's order -- S, N, W, then S-walk x2, N-walk x2, W-walk x2 (east is west flipped by the engine).
The fox never walks: it stands at its work with MOVEMENT_TYPE_WALK_IN_PLACE_LEFT, so the "walk" frames are its
SWEEP -- the tail swung low across the snow, then high, with a puff of snow where it struck. Turned to talk, it
sweeps no more until it turns back (faceplayer, then the movement resumes).

ITS PALETTE is npc_white, in npc_white's own slot (PALSLOT_NPC_4), which every object on FOUR ISLAND that uses the slot
already holds (the item balls, the rock, the man by the cave), so it repaints no one (engine.md trap 17):
    W white  l light grey (the underside)  g grey  K the outline (npc_white's darkest grey)  B black (eyes, nose)
A wide graphics id (no FREE id is left, T-461), so the recap replays it as OBJ_EVENT_GFX_MEOWTH.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PALS = os.path.join(GBA, "graphics/object_events/palettes")
RULES = os.path.join(GBA, "spritesheet_rules.mk")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

WHITE = {".": 0, "W": 14, "l": 11, "g": 12, "K": 13, "B": 15}
N = 32


def blank():
    return [["." for _ in range(N)] for _ in range(N)]


def ellipse(c, cx, cy, rx, ry, ch="W"):
    for y in range(N):
        for x in range(N):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                c[y][x] = ch


def rect(c, x0, y0, x1, y1, ch="W"):
    for y in range(max(0, y0), min(N, y1 + 1)):
        for x in range(max(0, x0), min(N, x1 + 1)):
            c[y][x] = ch


def ear(c, x, y, up=4, lean=0):
    """a pointed ear: its tip at (x + lean, y - up), widening to three pixels at its base y"""
    for i in range(up + 1):
        w = (i * 3) // up
        tx = x + lean - (lean * i) // up
        for dx in range(-w // 2, w - w // 2 + 1):
            if 0 <= y - up + i < N and 0 <= tx + dx < N:
                c[y - up + i][tx + dx] = "W"


def under(c, rows):
    """the underside: the last ROWS filled pixels of every column go light grey"""
    for x in range(N):
        ys = [y for y in range(N) if c[y][x] == "W"]
        for y in ys[-rows:]:
            c[y][x] = "l"


def outline(c):
    out = [row[:] for row in c]
    for y in range(N):
        for x in range(N):
            if c[y][x] == ".":
                if any(0 <= y + dy < N and 0 <= x + dx < N and c[y + dy][x + dx] not in ".K"
                       for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                    out[y][x] = "K"
    return out


def put(c, pts, ch):
    for x, y in pts:
        c[y][x] = ch


def puff(c, x, y):
    """snow flicked up: three specks, after the outline, so they stand clear"""
    for dx, dy in ((0, 0), (2, -2), (-1, -3)):
        if 0 <= y + dy < N and 0 <= x + dx < N and c[y + dy][x + dx] == ".":
            c[y + dy][x + dx] = "l"


def side(tail):
    """facing west. TAIL: 0 at rest (curled behind), 1 swept low across the snow, 2 swung high"""
    c = blank()
    ellipse(c, 17, 22, 8, 4.5)                      # the body
    ellipse(c, 8.5, 17.5, 4.5, 4)                   # the head
    rect(c, 2, 18, 6, 19)                           # the snout
    ear(c, 7, 14, 4, -1); ear(c, 10, 14, 4, 0)      # the ears
    for x in (11, 14, 19, 22):                      # four legs
        rect(c, x, 25, x + 1, 29)
    if tail == 0:
        ellipse(c, 27, 21, 3.5, 5)
    elif tail == 1:
        ellipse(c, 27, 26.5, 5, 2.6)
    else:
        ellipse(c, 27, 16, 3.2, 5.5)
    under(c, 1)
    c = outline(c)
    put(c, [(7, 17)], "B")                          # the eye
    put(c, [(1, 18)], "B")                          # the nose
    if tail == 1:
        puff(c, 30, 23)
    if tail == 2:
        puff(c, 30, 27)
    return c


def front(tail):
    """facing south: the face, the chest, the forelegs; the tail at one side or the other"""
    c = blank()
    if tail == 1:
        ellipse(c, 6, 26, 5, 2.6)
    elif tail == 2:
        ellipse(c, 26, 26, 5, 2.6)
    else:
        ellipse(c, 24, 25, 4, 3)
    ellipse(c, 16, 24, 6, 5.5)                      # the body, sitting
    ellipse(c, 16, 16.5, 5.5, 4.5)                  # the head
    ear(c, 12, 13, 4, -1); ear(c, 20, 13, 4, 1)
    rect(c, 13, 27, 14, 30); rect(c, 18, 27, 19, 30)
    under(c, 1)
    c = outline(c)
    put(c, [(13, 16), (19, 16)], "B")               # eyes
    put(c, [(16, 19)], "B")                         # the nose
    put(c, [(12, 12), (20, 12)], "l")               # inside the ears
    if tail == 1:
        puff(c, 2, 24)
    if tail == 2:
        puff(c, 29, 24)
    return c


def back(tail):
    """facing north: the back of the head and the ears, the back, the tail down the middle or swung"""
    c = blank()
    ellipse(c, 16, 24, 6, 5.5)
    ellipse(c, 16, 16.5, 5.5, 4.5)
    ear(c, 12, 13, 4, -1); ear(c, 20, 13, 4, 1)
    rect(c, 13, 27, 14, 30); rect(c, 18, 27, 19, 30)
    if tail == 1:
        ellipse(c, 7, 27, 5, 2.6)
    elif tail == 2:
        ellipse(c, 25, 27, 5, 2.6)
    else:
        ellipse(c, 16, 27.5, 3, 3)
    under(c, 1)
    c = outline(c)
    put(c, [(16, 21), (16, 22)], "l")               # the spine's shadow
    if tail == 1:
        puff(c, 3, 25)
    if tail == 2:
        puff(c, 28, 25)
    return c


def frames():
    rows = lambda c: ["".join(r) for r in c]
    return [rows(front(0)), rows(back(0)), rows(side(0)),
            rows(front(1)), rows(front(2)), rows(back(1)), rows(back(2)), rows(side(1)), rows(side(2))]


def sheet(frs):
    img = Image.new("P", (N * len(frs), N), 0)
    pal = daemonslib.read_pal(os.path.join(PALS, "npc_white.pal"))
    img.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    px = img.load()
    for n, fr in enumerate(frs):
        for y, row in enumerate(fr):
            for x, ch in enumerate(row):
                px[n * N + x, y] = WHITE[ch]
    return img


CONST, CNAME, FNAME = "OBJ_EVENT_GFX_TULIKKO", "Tulikko", "tulikko"
TAG, SLOT = "OBJ_EVENT_PAL_TAG_NPC_WHITE", "PALSLOT_NPC_4"
NOTE = ("T-528 (e): TULIKKO, the arctic fox sweeping snow by STILLFALL CAVE (DAEMONS tools/gentulikko.py), npc_white; "
        "32x32, its walk frames the sweep")
STAND_IN = "OBJ_EVENT_GFX_MEOWTH"


def ensure_rule():
    target = "$(OBJEVENTGFXDIR)/people/%s.4bpp" % FNAME
    s = open(RULES).read()
    if target + ":" in s:
        return
    tmp = RULES + ".tmp"
    open(tmp, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth 4 -mheight 4\n" % target)
    os.chmod(tmp, os.stat(RULES).st_mode)
    os.replace(tmp, RULES)


def register():
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            tmp = p + ".tmp"
            open(tmp, "w").write(s2)
            os.chmod(tmp, os.stat(p).st_mode)
            os.replace(tmp, p)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    try:
        import gentowns as g                        # imported without arming anything (engine.md trap 16)
    finally:
        sys.argv = argv
    g.register_one(edit, CONST, CNAME, FNAME, TAG, NOTE, slot=SLOT, geom=g.GEOM_32x32, stand_in=STAND_IN)


def main():
    frs = frames()
    assert all(len(f) == N and all(len(r) == N for r in f) for f in frs)
    img = sheet(frs)
    path = os.path.join(PEOPLE, FNAME + ".png")
    info = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")).read()
    old = Image.open(path) if os.path.exists(path) else None
    same = old is not None and old.size == img.size and list(old.getdata()) == list(img.getdata())
    at = info.find("gObjectEventGraphicsInfo_%s =" % CNAME)
    reg = at >= 0 and TAG in info[at:info.find("};", at)] and SLOT in info[at:info.find("};", at)]
    rule = ("people/%s.4bpp:" % FNAME) in open(RULES).read()
    os.makedirs(SCRATCH, exist_ok=True)
    img.convert("RGBA").resize((img.width * 6, img.height * 6), Image.NEAREST).save(
        os.path.join(SCRATCH, "%s_preview.png" % FNAME))
    print("  %-22s sheet %s, rule %s, registered %s" % (CONST, "current" if same else "STALE",
          "present" if rule else "MISSING", "yes" if reg else "NO"))
    if same and reg and rule:
        return
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    img.save(path, bits=4)
    ensure_rule()
    register()
    print("  written: %s, %s" % (os.path.relpath(path, GBA), CONST))


if __name__ == "__main__":
    main()
