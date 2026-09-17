#!/usr/bin/env python3
"""Clean a spriteforge draft into a daemon drawing gbasprite.py can build (T-131; vision.md 9.4).

    python3 tools/cleandraft.py DRAFT.png OUT.png [--streaks]

THE RECIPE IT SERVES, settled on NIBBLE 2026-09-17 (the prompts in full are in ai/README.md):

  * 512x512. The checkpoint draws on a fixed 8px grid, so 512 gives exactly 64 art pixels -- the sprite frame,
    nothing ever resampled -- in about 23s, against 37s at 640, 46s at 768 and 82-106s at 1024.
  * FRONT AND BACK ARE ONE SEED AND TWO MIRRORED PROMPTS: "front view, facing the viewer" and "rear view, facing
    away from the viewer, back of the head", each with the other's view in its negative. "seen from behind"
    alone drew NIBBLE in profile; image-to-image at 0.75 from the front kept the front's composition and redrew
    the front. Same seed, same wording otherwise, gives the same creature from both sides.
  * THE BODY IS ASKED FOR IN MID GREY, "medium grey body with light grey highlights and dark grey shading",
    with "white body, pale body" negative. Asked only for greyscale, the model draws a white animal and the
    five body steps fall 4/7/15/12/61 per cent dark to light -- the type colour then shows as its highlight
    only. Mid grey gave 16/8/7/36/33.
  * WHAT SURVIVES AS ACCENTS IS REAL: NIBBLE's 71 saturated pixels were its ear lining and nose, and
    gbasprite.py shifts them off the type's hue. "white background" is not obeyed either way (a flat grey
    comes back), which is why the background is taken by flood fill below and never by the prompt.

WHAT CLEANING DOES, each step measured on the NIBBLE draft first:

  1. ONE ART PIXEL PER 8x8 BLOCK, the median of the block's centre 4x4 -- never a block edge.
  2. THE BACKGROUND AND ITS SHADOW GO, by one flood fill from the border. The background is one flat colour
     (NIBBLE's border varied by 9 on 255); the shadow is a band a little darker than it, OUTSIDE the black
     outline; the edge can carry a one-pixel white line. The fill takes all three and stops at anything else,
     so a creature sealed by its outline is never entered.
  3. THE RESULT IS WRITTEN WITH A TRANSPARENT BACKGROUND, not on white paper. gbasprite.py used to find the
     subject by treating near-white as paper -- and NIBBLE's body IS near-white, so every white pixel of it
     would have been cut out as background. Transparency says which pixels are the creature instead of
     guessing it from their colour, and gbasprite.py now reads it when it is there.
  4. --streaks paints the four streak regions (9.4 as amended; T-132) in gbasprite.py's marker colours, one
     per move slot: four parallel diagonal strokes across a torso wide enough to keep body between them, or
     four stacked bands down a narrow one -- inside the outline, never on it. The first NIBBLE dashes were 3px
     and vanished at 1:1, so a stroke is at least 5 rows and a band the torso's width less 2px each side (3-7).
     A first placement, made the same way for every species so the contact sheet shows them consistently; a
     drawing that wants them elsewhere is adjusted by hand.

Everything it removes is counted and printed: a cleaning pass that reports only what it kept cannot be told
apart from one that did nothing.
"""
import ast, os, sys
from collections import deque
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PITCH = 8
BG_TOL = 28          # a background pixel sits within this of the border colour, per channel
OUTLINE_LUM = 60     # darker than this is the creature's outline, and the fill never crosses it


def markers():
    tree = ast.parse(open(os.path.join(ROOT, "tools/gbasprite.py")).read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets):
            return ast.literal_eval(n.value)
    raise SystemExit("gbasprite.py no longer defines STREAK_MARKERS")


def sample(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    h, w = a.shape[:2]
    assert h % PITCH == 0 and w % PITCH == 0, "%s is %dx%d, not a whole number of %dpx cells" % (path, w, h, PITCH)
    g = np.zeros((h // PITCH, w // PITCH, 3), int)
    for y in range(h // PITCH):
        for x in range(w // PITCH):
            g[y, x] = np.median(a[y * PITCH + 2:y * PITCH + 6, x * PITCH + 2:x * PITCH + 6].reshape(-1, 3), 0)
    return g


def clear_background(g):
    h, w = g.shape[:2]
    lum = (g[..., 0] * 299 + g[..., 1] * 587 + g[..., 2] * 114) // 1000
    sat = g.max(2) - g.min(2)
    border = np.concatenate([g[0], g[-1], g[:, 0], g[:, -1]])
    bg = np.median(border, 0)
    bg_lum = int((bg[0] * 299 + bg[1] * 587 + bg[2] * 114) // 1000)
    is_bg = np.abs(g - bg).max(2) <= BG_TOL
    is_shadow = (sat < 30) & (lum < bg_lum) & (lum >= OUTLINE_LUM)
    # The white line is at the canvas EDGE. Allowed anywhere, the first version walked through a gap the grid
    # left in NIBBLE's thin outline and took 204 pixels of its white body.
    rim = np.zeros((h, w), bool); rim[:4, :] = rim[-4:, :] = rim[:, :4] = rim[:, -4:] = True   # NIBBLE's back had it 4 rows up
    is_edge_white = (lum > 235) & (sat < 20) & rim
    passable = is_bg | is_shadow | is_edge_white
    gone = np.zeros((h, w), bool)
    q = deque((y, x) for y in range(h) for x in range(w) if (y in (0, h - 1) or x in (0, w - 1)) and passable[y, x])
    for y, x in q:
        gone[y, x] = True
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not gone[ny, nx] and passable[ny, nx]:
                gone[ny, nx] = True
                q.append((ny, nx))
    # A BLACK SHADOW looks exactly like outline by colour, and NIBBLE's back view cast one. By SHAPE they differ:
    # an outline pixel always touches the creature's light body, and outline is a line; a shadow is a mass that
    # touches nothing light. So dark pixels are worn away from the outside only while they touch no light body
    # pixel AND are thick (five or more of their eight neighbours dark or already gone) -- which a one-pixel
    # tail, whisker or outline never is.
    dark = lum < OUTLINE_LUM
    worn = 0
    while True:
        light_body = ~gone & ~dark
        step = []
        for y in range(h):
            for x in range(w):
                if gone[y, x] or not dark[y, x]:
                    continue
                n8 = [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx)]
                inside = [(a, b) for a, b in n8 if 0 <= a < h and 0 <= b < w]
                if any(light_body[a, b] for a, b in inside):
                    continue
                if not any(gone[a, b] for a, b in inside):
                    continue
                if sum(1 for a, b in inside if gone[a, b] or dark[a, b]) + (8 - len(inside)) >= 5:
                    step.append((y, x))
        if not step:
            break
        for y, x in step:
            gone[y, x] = True
        worn += len(step)
    # ONLY THE CREATURE'S OWN SHAPE STAYS. Anything not joined to its largest 8-connected piece -- NIBBLE's back
    # view carried a free-standing white line under it, and a whisker dot floated off the front -- is not the
    # creature, whatever colour it is.
    keep = ~gone
    label = np.zeros((h, w), int)
    sizes = {}
    for y in range(h):
        for x in range(w):
            if keep[y, x] and not label[y, x]:
                n = len(sizes) + 1
                label[y, x] = n
                q2, size = deque([(y, x)]), 0
                while q2:
                    cy, cx = q2.popleft(); size += 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and keep[ny, nx] and not label[ny, nx]:
                                label[ny, nx] = n; q2.append((ny, nx))
                sizes[n] = size
    main = max(sizes, key=sizes.get) if sizes else 0
    loose = int(sum(v for k, v in sizes.items() if k != main))
    gone |= keep & (label != main)
    counts = dict(background=int((gone & is_bg).sum()), shadow=int((gone & is_shadow & ~is_bg).sum()) + worn, loose=loose,
                  edge=int((gone & is_edge_white & ~is_bg & ~is_shadow).sum()), kept=int((~gone).sum()))
    return ~gone, counts, bg


def paint_streaks(g, subject):
    """four short PARALLEL diagonal strokes on the body, left to right, with body between them.

    Two placements failed first. Spaced across the figure's whole box, NIBBLE's tail made the box twice its
    torso and the strokes stood in empty columns. Spaced across each row's own run of body, the positions moved
    row to row and the four strokes ran into one rainbow block. So the torso's width is measured ONCE -- the
    median run over the band -- four columns are fixed across it, and each stroke leans the same way."""
    lum = (g[..., 0] * 299 + g[..., 1] * 587 + g[..., 2] * 114) // 1000
    body = subject & (lum >= OUTLINE_LUM)
    ys = np.where(body.any(1))[0]
    y0, y1 = ys.min(), ys.max()
    top = y0 + (y1 - y0) * 50 // 100
    span = max(5, (y1 - y0) // 5)                                # under 5 rows a stroke reads as a speck at 1:1
    starts, ends = [], []
    for y in range(top, min(g.shape[0], top + span)):
        xs = np.where(body[y])[0]
        if len(xs) < 5:
            continue
        runs, start = [], xs[0]
        for a, b in zip(xs, xs[1:]):
            if b != a + 1:
                runs.append((start, a)); start = b
        runs.append((start, xs[-1]))
        r0, r1 = max(runs, key=lambda r: r[1] - r[0])
        starts.append(r0); ends.append(r1)
    if not starts:
        return [0, 0, 0, 0]
    r0, r1 = int(np.median(starts)), int(np.median(ends))
    width = r1 - r0 + 1
    cols = [r0 + round((k + 0.5) * width / 4) for k in range(4)]
    marks = markers()
    painted = [0, 0, 0, 0]
    if min(b - a for a, b in zip(cols, cols[1:])) >= 3:
        for t in range(span):                                   # ACROSS: room for body between four diagonals
            y = top + t
            for k, cx in enumerate(cols):
                x = cx - t // 2
                if 0 <= y < g.shape[0] and 0 <= x < g.shape[1] and body[y, x]:
                    g[y, x] = marks[k]
                    painted[k] += 1
        return painted
    # STACKED: a torso too narrow for four diagonals with body between them (NIBBLE's is nine) gets four short
    # dashes down its middle instead, a row of body between each -- still slot 1 to 4, now top to bottom.
    cx = (r0 + r1) // 2
    #  As wide as the torso allows, keeping two px of body each side: NIBBLE's first dashes were three px and
    #  vanished at 1:1 on the contact sheet -- a streak that cannot be seen carries no move.
    dash = max(3, min(7, width - 4))
    y = y0 + (y1 - y0) * 35 // 100
    for k in range(4):
        while y < g.shape[0] and body[y, cx - dash // 2:cx - dash // 2 + dash].sum() < dash:
            y += 1
        for x in range(cx - dash // 2, cx - dash // 2 + dash):
            if 0 <= y < g.shape[0] and body[y, x]:
                g[y, x] = marks[k]
                painted[k] += 1
        y += 2
    return painted


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        raise SystemExit(__doc__)
    src, out = args
    g = sample(src)
    subject, counts, bg = clear_background(g)
    print("  %s: %dx%d art px; border colour %s; removed %d background, %d shadow, %d edge-white, %d loose; kept %d"
          % (os.path.basename(src), g.shape[1], g.shape[0], tuple(int(v) for v in bg),
             counts["background"], counts["shadow"], counts["edge"], counts["loose"], counts["kept"]))
    # A LONE SATURATED PIXEL IS SHADING, NOT A MARKING. The checkpoint shades greyscale with a cool blue tint, and on
    # NIBBLE five single blue specks were saturated enough that gbasprite.py took three of them as accent colours.
    # An accent is a nose, an eye, a stripe: two or more saturated pixels together. A saturated pixel with no
    # saturated neighbour goes back to grey at its own brightness.
    sat = g.max(2) - g.min(2)
    lumg = (g[..., 0] * 299 + g[..., 1] * 587 + g[..., 2] * 114) // 1000
    hot = subject & (sat >= 60)
    specks = 0
    for y, x in zip(*np.where(hot)):
        if not any(hot[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                   if (dy or dx) and 0 <= y + dy < g.shape[0] and 0 <= x + dx < g.shape[1]):
            g[y, x] = lumg[y, x]
            specks += 1
    print("  %d lone saturated pixel(s) returned to grey; %d saturated pixel(s) kept as accents" % (specks, int(hot.sum()) - specks))
    if "--streaks" in sys.argv:
        painted = paint_streaks(g, subject)
        print("  streak pixels painted per slot: %s" % painted)
        assert all(painted), "a streak found no body to sit on -- place it by hand"
    rgba = np.zeros(g.shape[:2] + (4,), np.uint8)
    rgba[..., :3] = g
    rgba[..., 3] = np.where(subject, 255, 0)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(out)
    ys, xs = np.where(subject)
    print("  -> %s  (subject %dx%d, transparent background)" % (out, xs.max() - xs.min() + 1, ys.max() - ys.min() + 1))


if __name__ == "__main__":
    main()
