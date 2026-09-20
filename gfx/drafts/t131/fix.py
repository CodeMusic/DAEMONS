#!/usr/bin/env python3
"""T-131's twelve, after cleandraft.py: the boxes, the ground strips and the coloured bodies.

    python3 gfx/drafts/t131/fix.py

Same three faults every batch since 5 has hit, and the same tools (gfx/drafts/t176/fix.py is where they were last
written down):

  A BOX THE FILL STOPPED AT. Six views came back with the whole 64x64 opaque -- pilot both ways, quota's back, and
  the backs of cache, triton and phoenix. The border flood found a colour it would not cross, so nothing was taken.
  unbox floods from a corner by tolerance, keep_largest drops what the box leaves behind, and restreak re-runs
  cleandraft on the result so the streaks land on the body rather than on the box.

  A GROUND STRIP UNDER THE FEET, which is connected to the figure and so survives keep_largest. It is cut by row:
  everything below the lowest row that still has body in it is not the daemon.

  COLOUR IN THE BODY. Batch 2's rule: a draft drawn with colour in its BODY is greyed, every pixel but gbasprite's
  four streak markers -- SOUNDING's blue, TRITON's blue, PHOENIX's purple, FAKEROOT's teal, QUOTA's green, PILOT's
  yellow dome. POLL, WATCHDOG, WARNING, CACHE and STARVED keep theirs: an orange beak and a pink nose are ACCENTS,
  which gbasprite.py shifts off the type's hue on purpose.
"""
import ast, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/Users/christopherhicks/Projects/DAEMONS"
os.chdir(ROOT)
C = "gfx/drafts/t131/clean/"

tree = ast.parse(open("tools/gbasprite.py").read())
MARKS = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "STREAK_MARKERS" for t in n.targets))
MARKS = {tuple(m) for m in (MARKS.values() if isinstance(MARKS, dict) else MARKS)}


def unbox(path, tol=16):
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    seeds = [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)]
    for seed in seeds:
        if px[seed][3] == 0:
            continue
        ref = px[seed][:3]; todo, seen = [seed], set()
        while todo:
            x, y = todo.pop()
            if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
                continue
            seen.add((x, y))
            r, g, b, a = px[x, y]
            if a == 0 or max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) > tol:
                continue
            px[x, y] = (0, 0, 0, 0)
            todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    im.save(path)


def deframe(src, dst, key=(40, 90, 200), layers=3, floor=150):
    """THE ACTUAL FAULT behind all six 'boxes', found by looking at a draft at 512 instead of at 64.

    The model drew a GREY FRAME round a near-white interior. cleandraft floods from the border, takes the frame,
    and stops at the interior because the interior is a different colour -- so the interior survives as 'subject'
    and the cleaned art is a full opaque square. Flooding 'anything light' instead eats the creature, because
    pilot and quota are near-white themselves (the pale-body failure batch 2 recorded).

    So the flood is done HERE, at 512, where the outline is eight pixels thick and has no gaps to leak through,
    and it is done in LAYERS: flood the border colour, then whatever is at the border next, while that colour is
    still lighter than `floor` -- which the creature's black outline never is. Everything taken becomes one flat
    key colour, and cleandraft then does its ordinary job on a draft with an ordinary background.
    """
    im = Image.open(src).convert("RGB"); px = im.load(); w, h = im.size
    for _ in range(layers):
        seed = None
        #  after the first layer the corners ARE the key colour, so walk inward until something else appears --
        #  the next background layer always sits immediately behind the one just taken
        for x, y, dx, dy in [(2, 2, 1, 1), (w - 3, 2, -1, 1), (2, h - 3, 1, -1), (w - 3, h - 3, -1, -1)]:
            while 0 <= x < w and 0 <= y < h and px[x, y] == key:
                x, y = x + dx, y + dy
            if 0 <= x < w and 0 <= y < h and px[x, y] != key:
                seed = (x, y); break
        if seed is None:
            break
        ref = px[seed]
        if (ref[0] * 299 + ref[1] * 587 + ref[2] * 114) // 1000 < floor:
            break
        todo, seen = [seed], set()
        while todo:
            x, y = todo.pop()
            if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
                continue
            seen.add((x, y))
            c = px[x, y]
            if c == key or max(abs(c[i] - ref[i]) for i in range(3)) > 20:
                continue
            px[x, y] = key
            todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    im.save(dst)


def by_outline(src, dst, key=(255, 0, 255), ink=200):
    """A PALE CREATURE ON A PALE GROUND is the wrong problem for a flood, and pilot, cache and triton are all three.

    (The key is MAGENTA and that matters: keyed blue, TRITON's blue-grey dragon was inside cleandraft's
    tolerance for its own background and the flood ate the whole animal, leaving 151 loose pixels.)

    Flooding asks 'what is background?' and answers by colour, which cannot separate a white body from a white
    frame; widening the tolerance until it clears the frame eats the body. So ask the other question instead:
    the model always draws a CLOSED DARK OUTLINE, so the creature is the largest dark-bordered shape with its
    holes filled. Everything outside that becomes the key colour and cleandraft proceeds normally.
    """
    from scipy import ndimage
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(int)
    lum = (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000
    dark = lum < ink
    lab, n = ndimage.label(dark)
    if n:
        sizes = ndimage.sum(dark, lab, range(1, n + 1))
        dark = lab == (int(np.argmax(sizes)) + 1)
    solid = ndimage.binary_fill_holes(dark)
    out = np.where(solid[..., None], a, np.array(key)).astype(np.uint8)
    Image.fromarray(out).save(dst)
    return solid.sum() / solid.size


def keep_largest(path):
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size; seen = set(); comps = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (x, y) not in seen:
                comp, todo = [], [(x, y)]
                while todo:
                    p = todo.pop()
                    if p in seen or not (0 <= p[0] < w and 0 <= p[1] < h) or not px[p][3]:
                        continue
                    seen.add(p); comp.append(p)
                    todo += [(p[0] + dx, p[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
                comps.append(comp)
    comps.sort(key=len)
    for c in comps[:-1]:
        for p in c:
            px[p] = (0, 0, 0, 0)
    im.save(path)


def unground(path):
    """THE STRIP THE CREATURE WAS DRAWN STANDING ON, which survives every other step because it TOUCHES the feet.

    keep_largest cannot drop it (it is one component with the animal) and the background flood cannot reach it
    (it is inside the outline's reach). It is recognisable by shape instead: a long horizontal run, low in the
    frame, with nothing but air a few rows above it. A foot is never twenty pixels wide with air over it.
    """
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    gone = 0
    for y in range(h - 1, h - 10, -1):
        if y < 3:
            break
        x = 0
        while x < w:
            if not px[x, y][3]:
                x += 1; continue
            run = x
            while run < w and px[run, y][3]:
                run += 1
            above = sum(1 for k in range(x, run) if px[k, y - 3][3])
            if run - x >= 14 and above <= (run - x) * 0.55:      # feet may stand on it; a body may not
                for k in range(x, run):
                    for yy in range(y, min(h, y + 3)):
                        if px[k, yy][3]:
                            px[k, yy] = (0, 0, 0, 0); gone += 1
            x = run
    if gone:
        im.save(path)
    return gone


def grey_but_markers(path):
    im = Image.open(path).convert("RGBA"); px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a and (r, g, b) not in MARKS:
                l = (r * 299 + g * 587 + b * 114) // 1000
                px[x, y] = (l, l, l, a)
    im.save(path)


def place_streaks(path, slots=4, length=7):
    """cleandraft's own placement, done against the MASK instead of against the drawing.

    Two views defeated it outright -- SOUNDING's back is a fish whose torso is a thin diagonal, TRITON's a dragon
    whose body is mostly wing -- and it refuses rather than paint a streak on nothing, which is right. Here the
    band is chosen from the mask: the rows where the body is widest, then the four x positions inside that band
    where the body is opaque for the whole height of the stroke. If four such positions do not exist the stroke
    shortens until they do, so this cannot paint on air either.
    """
    im = Image.open(path).convert("RGBA"); px = im.load(); w, h = im.size
    solid = [[px[x, y][3] > 0 for x in range(w)] for y in range(h)]
    marks = sorted(MARKS)
    for L in range(length, 2, -1):
        best = None
        for y in range(h - L):
            xs = [x for x in range(w) if all(solid[y + k][x] for k in range(L))]
            if len(xs) >= slots * 2:
                #  prefer the widest run, and among equals the one lowest on the body (a torso, not a head)
                if best is None or len(xs) >= len(best[1]):
                    best = (y, xs)
        if best:
            y, xs = best
            step = max(1, len(xs) // (slots + 1))
            picks = [xs[step * (i + 1)] for i in range(slots)]
            for i, x in enumerate(picks):
                for k in range(L):
                    px[x, y + k] = marks[i % len(marks)] + (255,)
            im.save(path)
            return L, picks
    return 0, []


def restreak(name, box=None):
    """cleandraft again, on the cleaned art blown back up to 512 on a ground it will certainly take"""
    im = Image.open(C + name + ".png").convert("RGBA")
    big = Image.new("RGBA", (512, 512), (40, 90, 200, 255))
    big.alpha_composite(im.resize((512, 512), Image.NEAREST))
    tmp = "/tmp/t131_%s_8x.png" % name
    big.convert("RGB").save(tmp)
    cmd = ["python3", "tools/cleandraft.py", tmp, C + name + ".png", "--streaks"]
    if box:
        cmd.append("--streak-box=%d,%d,%d,%d" % box)
    out = subprocess.run(cmd, capture_output=True, text=True)
    print("  restreak %-16s %s" % (name, (out.stdout or out.stderr).strip().splitlines()[-1]))


BOXED = ["pilot_front", "pilot_back", "quota_back", "cache_back", "triton_back", "phoenix_back"]
GREY = ["sounding_front", "sounding_back", "triton_front", "triton_back", "phoenix_front", "phoenix_back",
        "fakeroot_front", "fakeroot_back", "quota_front", "quota_back", "pilot_front", "pilot_back"]

if __name__ == "__main__":
    for name in BOXED:
        p = C + name + ".png"
        if not os.path.exists(p):
            print("  ! %s not cleaned yet" % name); continue
        unbox(p); keep_largest(p); restreak(name)
    for name in sorted({n[:-4] for n in os.listdir(C) if n.endswith(".png")}):
        n = unground(C + name + ".png")
        if n:
            print("  unground %-16s %d px of ground removed" % (name, n))
    for name in GREY:
        if os.path.exists(C + name + ".png"):
            grey_but_markers(C + name + ".png")
    print("  greyed %d coloured bodies; accents kept on the other ten views" % len(GREY))
