#!/usr/bin/env python3
"""T-388: TRAVERSE's ride is a manta ray, not vanilla's whale (the user, 2026-10-08).

The water ride is `graphics/object_events/pics/misc/surf_blob.png` in the GBA engine: six 32x32 frames -- facing
south twice, north twice, west twice (east is west flipped) -- drawn in the PLAYER's sixteen colours, because the game
gives it palette 0 (field_effect_helpers.c). Vanilla's shape was only recoloured by T-52.

This draws the manta from the sprite server's draft (`gfx/drafts/manta/manta_round_3111.png`: seed 3111, seen from
directly above, head DOWN, toward the viewer) the way the rest of our art is drawn -- background flood-filled away, cropped, scaled to the
frame, each pixel given one of the player palette's own colours by lightness, and a dark outline around it:

  - SOUTH: head down, toward the viewer; NORTH: head up; WEST: head left (the long axis along the frame).
  - The view is three-quarter like the rest of the overworld, so the body is squashed top to bottom.
  - The second frame of each pair lifts the wingtips a pixel and draws the wings in a little -- the ripple, every 48
    frames, the same wave as GOTO's ribbon (T-387).
  - The back is the BOX's slate with the pale shoulder marks real mantas carry; its face shows facing south.

  python3 tools/gbamanta.py            # report what would change
  python3 tools/gbamanta.py --write    # write surf_blob.png (and a 4x preview beside the draft)
"""
import os
import sys
from collections import deque

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DRAFT = os.path.join(ROOT, "gfx", "drafts", "manta", "manta_round_3111.png")
OUT = os.path.join(GBA, "graphics", "object_events", "pics", "misc", "surf_blob.png")
PAL = os.path.join(GBA, "graphics", "object_events", "palettes", "player.pal")

# The player palette's indices this ride may use, darkest to lightest (player.pal):
OUTLINE = 6        # 34,34,40
RAMP = [5, 14, 14, 7]   # 52,52,60 / 100,100,112 / 100,100,112 / 156,156,166 -- the BOX's greys, as vanilla's ride was
MARK = 9           # 240,230,204: the pale shoulder marks (vanilla's ride had its highlight in the same cream)
TRANSPARENT = 0

# Each direction: (rotation of the head-up draft, width, height) of the body inside the 32x32 frame, and where it sits.
FRAMES = {
    "south": (0, 30, 17),
    "north": (180, 30, 17),
    "west": (270, 28, 15),
}


def read_pal(path):
    lines = open(path).read().split()
    n = int(lines[2])
    vals = list(map(int, lines[3:3 + 3 * n]))
    return [tuple(vals[i:i + 3]) for i in range(0, 3 * n, 3)]


def cut_out(path):
    """The draft without its background: everything flood-connected to the border and pale is cleared."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    bg = [[False] * h for _ in range(w)]
    q = deque((x, y) for x in range(w) for y in (0, h - 1))
    q.extend((x, y) for y in range(h) for x in (0, w - 1))
    while q:
        x, y = q.popleft()
        if not (0 <= x < w and 0 <= y < h) or bg[x][y]:
            continue
        r, g, b = px[x, y]
        if min(r, g, b) < 170 or max(r, g, b) - min(r, g, b) > 30:
            continue
        bg[x][y] = True
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()
    for x in range(w):
        for y in range(h):
            if not bg[x][y]:
                op[x, y] = px[x, y] + (255,)
    return out.crop(out.getbbox())


def body(art, rot, bw, bh, ripple):
    """The manta at (bw, bh), rotated; the ripple frame draws the wings in by 2 px and lifts their tips."""
    im = art.rotate(rot, expand=True)
    if ripple:
        bw -= 2
    small = im.resize((bw, bh), Image.LANCZOS)
    return small


def to_indices(small, ripple, wings_across):
    """Lightness to the ramp; alpha to transparent; then a dark outline. Returns a dict {(x, y): index}."""
    w, h = small.size
    sp = small.load()
    cells = {}
    lum = []
    for x in range(w):
        for y in range(h):
            r, g, b, a = sp[x, y]
            if a < 110:
                continue
            lum.append(0.3 * r + 0.59 * g + 0.11 * b)
    lo, hi = min(lum), max(lum)
    for x in range(w):
        for y in range(h):
            r, g, b, a = sp[x, y]
            if a < 110:
                continue
            t = ((0.3 * r + 0.59 * g + 0.11 * b) - lo) / max(1, hi - lo)
            cells[(x, y)] = MARK if t > 0.86 else RAMP[min(len(RAMP) - 1, int(t * len(RAMP)))]
    if ripple and wings_across:            # the tips lift: the outermost columns move up a pixel
        lifted = {}
        for (x, y), c in cells.items():
            edge = x < 3 or x >= w - 3
            lifted[(x, y - 1 if edge else y)] = c
        cells = lifted
    outline = {}
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in cells:
                outline[n] = OUTLINE
    cells.update(outline)
    return cells


def frame(art, direction, ripple):
    rot, bw, bh = FRAMES[direction]
    small = body(art, rot, bw, bh, ripple)
    cells = to_indices(small, ripple, direction != "west")
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    ox = (32 - w) // 2 - min(xs)
    oy = 31 - max(ys) - 1                  # sits on the frame's floor, one row up, as vanilla's did
    f = Image.new("P", (32, 32), TRANSPARENT)
    for (x, y), c in cells.items():
        if 0 <= x + ox < 32 and 0 <= y + oy < 32:
            f.putpixel((x + ox, y + oy), c)
    return f


def build():
    art = cut_out(DRAFT)
    strip = Image.new("P", (192, 32), TRANSPARENT)
    order = [("south", False), ("south", True), ("north", False), ("north", True), ("west", False), ("west", True)]
    for i, (d, rip) in enumerate(order):
        strip.paste(frame(art, d, rip), (32 * i, 0))
    pal = read_pal(PAL)
    flat = [v for c in pal for v in c]
    strip.putpalette(flat + [0] * (768 - len(flat)))
    return strip


def main():
    write = "--write" in sys.argv
    strip = build()
    old = Image.open(OUT)
    same = list(old.getdata()) == list(strip.getdata())
    print("  surf_blob.png: %s" % ("unchanged" if same else "the manta (6 frames) would replace vanilla's shape"))
    if write and not same:
        strip.save(OUT, optimize=False)
        prev = strip.convert("RGBA").resize((192 * 4, 32 * 4), Image.NEAREST)
        prev.save(os.path.join(os.path.dirname(DRAFT), "surf_blob_preview_x4.png"))
        print("  wrote %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
