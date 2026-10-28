#!/usr/bin/env python3
"""T-464: the follower's own picture -- a daemon walks at a believable size beside the player.

    python3 tools/gbafollower.py            # report: what each follower is made from, what would change; FAILS (exit 1)
                                            #   on a follower over 22 tall or 24 wide, or an oversized icon left without one
    python3 tools/gbafollower.py --write    # write graphics/pokemon/<x>/follower.png and src/data/follower_gfx.h

THE BUG (the user's finding on the device, 2026-10-28: CODEMUSAI "much larger than my character sprite"). The follower
(src/daemons_follower.c) drew the lead's PARTY ICON at 1x. T-452 drew the icons as 28px busts filling the 32px cell --
right for the party menu the user chose them for -- and the follower walked behind a player whose figure is 16 wide
by 22 tall (red_normal's frame 0, rows 9-30) at 25x28, standing two rows below the player's feet. Measured then: 181
of 391 icons 24 or taller; vanilla's are 20 tall at the median and 23 at most.

THE FIX (the user chose "own small art", 2026-10-28). Every species whose icon's first frame is taller than 20, wider
than 22, or stands below row 28 gets a follower picture of its own: one 32x32 frame, the creature at most 20 tall
and 22 wide, its lowest row on row 28 -- where FOLLOWER_Y (2) puts it on the player's feet (row 30). Made, in order:

    1. SHIFTED   the icon already fits and only stands too low: its own pixels, moved up to row 28.
    2. REDUCED   a redrawn daemon (gfx/daemons/<name>_front.png): the clean front reduced again by T-452's icon3,
                 fitted to 20x22 -- the whole creature, not the party bust, since this one walks.
    3. VOTED     anything else: the icon's first frame reduced by majority vote (the outline wins a cell at 30%).

Its pixels are in the SAME shared icon palette as its icon (gMonIconPaletteIndices), because the follower's colours
are tools/gbafollowerpal.py's remap of that palette -- so nothing about its colour changes. A species with no picture
here falls back to its icon's first frame (daemons_follower.c FollowerPic). tools/gbasprite.py calls this after it
writes the icons, so a redrawn daemon's follower is never staler than its icon.
"""
import os, re, sys, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "src", "data", "follower_gfx.h")
sys.path.insert(0, os.path.join(ROOT, "gfx", "drafts", "t452", "scripts"))
from PIL import Image

MAX_H, MAX_W, GROUND = 20, 22, 28      # what a follower is made to
GUARD_H, GUARD_W = 22, 24              # what fails the check: never as tall as the player (22) plus a margin of none
OUTLINE_SHARE = 0.30                   # icon3's own rule for the outline winning a cell


def icon_rows():
    """[(SPECIES_X, icon.png path relative to GBA, shared palette index)] for every real species with an icon."""
    src = open(os.path.join(GBA, "src", "pokemon_icon.c"), encoding="utf-8").read()
    table = src.split("const u8 *const gMonIconTable[] = {", 1)[1].split("};", 1)[0]
    rows = re.findall(r"\[(SPECIES_\w+)\]\s*=\s*(gMonIcon_\w+)", table)
    idx = src.split("const u8 gMonIconPaletteIndices[] = {", 1)[1].split("};", 1)[0]
    palidx = dict(re.findall(r"\[(SPECIES_\w+)\]\s*=\s*(\d+)", idx))
    gfx = open(os.path.join(GBA, "src", "data", "graphics", "pokemon.h"), encoding="utf-8").read()
    paths = {}
    for sym, p in re.findall(r"const u8 (gMonIcon_\w+)\[\]\s*=\s*INCBIN_U8\(\s*\"([^\"]+)\"", gfx):
        paths.setdefault(sym, p)                      # DEOXYS: both editions' first frame is icon.4bpp
    out = []
    for sp, sym in rows:
        #  The follower is a party daemon: never an EGG, never an UNOWN letter (its species is SPECIES_UNOWN).
        if sp in ("SPECIES_NONE", "SPECIES_EGG") or re.match(r"SPECIES_UNOWN_", sp) or sym not in paths:
            continue
        out.append((sp, paths[sym].replace(".4bpp", ".png"), int(palidx.get(sp, 0))))
    return out


def species_names():
    t = open(os.path.join(GBA, "src", "data", "text", "species_names.h"), encoding="utf-8").read()
    return dict(re.findall(r"\[(SPECIES_\w+)\]\s*=\s*_\(\"(.*?)\"\)", t))


def icon_palettes():
    out = []
    for i in range(3):
        f = os.path.join(GBA, "graphics/pokemon/icon_palettes/icon_palette_%d.pal" % i)
        cols = [tuple(int(v) for v in l.split()) for l in open(f).read().split("\n")[3:] if l.strip()][:16]
        out.append(cols)
    return out


def frame0(path):
    im = Image.open(path)
    if im.mode != "P":
        raise SystemExit("%s: not an indexed PNG" % path)
    px = im.load()
    return [[px[x, y] for x in range(32)] for y in range(32)]


def bbox(g):
    pts = [(x, y) for y, row in enumerate(g) for x, v in enumerate(row) if v]
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def size(b):
    return (b[3] - b[1] + 1, b[2] - b[0] + 1) if b else (0, 0)


def needs(g):
    b = bbox(g)
    if not b:
        return False
    h, w = size(b)
    return h > MAX_H or w > MAX_W or b[3] > GROUND


def place(cells):
    """A creature (rows of indices, h <= 20, w <= 22) on a 32x32 frame, centred, its lowest row on row 28."""
    h, w = len(cells), len(cells[0])
    out = [[0] * 32 for _ in range(32)]
    oy, ox = GROUND + 1 - h, (32 - w) // 2
    for y in range(h):
        for x in range(w):
            out[oy + y][ox + x] = cells[y][x]
    return out


def crop(g, b):
    return [row[b[0]:b[2] + 1] for row in g[b[1]:b[3] + 1]]


def shifted(g):
    b = bbox(g)
    out = [[0] * 32 for _ in range(32)]
    dy = GROUND - b[3]
    for y in range(b[1], b[3] + 1):
        out[y + dy] = g[y][:]
    return out


def voted(g, pal):
    """The icon's first frame reduced to fit 20x22 by majority vote, the outline winning a cell at 30%."""
    b = bbox(g)
    src = crop(g, b)
    h, w = len(src), len(src[0])
    sc = min(MAX_H / h, MAX_W / w)
    while round(h * sc) > MAX_H or round(w * sc) > MAX_W:
        sc *= 0.99
    th, tw = max(1, round(h * sc)), max(1, round(w * sc))
    used = sorted({v for row in src for v in row if v})
    lum = lambda i: 0.299 * pal[i][0] + 0.587 * pal[i][1] + 0.114 * pal[i][2]
    dark = min(used, key=lambda i: (lum(i), i))
    cells = [[0] * tw for _ in range(th)]
    for y in range(th):
        for x in range(tw):
            y0, y1 = int(y / sc), max(int(y / sc) + 1, int((y + 1) / sc))
            x0, x1 = int(x / sc), max(int(x / sc) + 1, int((x + 1) / sc))
            vals = [src[yy][xx] for yy in range(y0, min(y1, h)) for xx in range(x0, min(x1, w))]
            ink = [v for v in vals if v]
            if not vals or len(ink) * 2 < len(vals):
                continue
            if ink.count(dark) >= OUTLINE_SHARE * len(ink):
                cells[y][x] = dark
            else:
                cells[y][x] = max(sorted(set(ink)), key=ink.count)
    return place(cells)


def reduced(d, name, pi):
    """The clean redrawn front, reduced again by icon3 to fit 20x22 in the icon's own shared palette; None if there is
    no clean front (a PNG with transparency) or the palette holds no ramp for the type."""
    import gbs, icon3
    src = gbs.rich_src(name, "front") if name else None
    if not src or not src.endswith(".png"):
        return None
    im = Image.open(src)
    if im.mode != "RGBA" or im.getextrema()[3][0] > 127:
        return None
    t = gbs.primary_type(d)
    if t not in gbs.TYPE_COLOR:
        return None
    r = icon3.reduce(t, src, fit=(MAX_H, MAX_W), pal_index=pi)
    if r is None:
        return None
    grid = r["grid"]
    return place([[int(v) for v in row] for row in grid])


def plan():
    """{SPECIES_X: (dir path, grid, how)} for every species that needs a follower picture."""
    names = species_names()
    pals = icon_palettes()
    out = {}
    for sp, icon, pi in icon_rows():
        p = os.path.join(GBA, icon)
        if not os.path.exists(p):
            continue
        g = frame0(p)
        if not needs(g):
            continue
        h, w = size(bbox(g))
        d = os.path.basename(os.path.dirname(p))
        if h <= MAX_H and w <= MAX_W:
            out[sp] = (os.path.dirname(icon), shifted(g), "shifted", pi)
            continue
        r = reduced(d, names.get(sp), pi)
        if r is not None:
            out[sp] = (os.path.dirname(icon), r, "reduced", pi)
        else:
            out[sp] = (os.path.dirname(icon), voted(g, pals[pi]), "voted", pi)
    return out


def render(p):
    sym = lambda sp: "sFollowerPic_" + "".join(w.capitalize() for w in sp[len("SPECIES_"):].split("_"))
    out = ["//  GENERATED by DAEMONS tools/gbafollower.py (T-464) -- do not edit; run the tool.",
           "//  The follower's own picture: one 32x32 frame, the creature at most 20 tall and 22 wide, its lowest row on",
           "//  row 28, in its icon's shared palette (so tools/gbafollowerpal.py's colours hold). A species not listed has",
           "//  an icon that already fits, and walks as its icon's first frame (daemons_follower.c FollowerPic).",
           ""]
    for sp in sorted(p):
        out.append('static const u8 %s[] = INCBIN_U8("%s/follower.4bpp");' % (sym(sp), p[sp][0]))
    out += ["", "static const u8 *const sFollowerPics[NUM_SPECIES] = {"]
    out += ["    [%s] = %s," % (sp, sym(sp)) for sp in sorted(p)]
    out.append("};")
    return "\n".join(out) + "\n"


def read_png_grid(path):
    try:
        im = Image.open(path)
    except OSError:
        return None, None
    if im.mode != "P" or im.size != (32, 32):
        return None, None
    px = im.load()
    return [[px[x, y] for x in range(32)] for y in range(32)], [tuple(c) for c in zip(*[iter(im.getpalette()[:48])] * 3)]


def write_png(path, grid, pal):
    import gbs
    tmp = path + ".tmp"
    gbs.write_png4(tmp, grid, pal, 32, 32)
    os.replace(tmp, path)


def run(write):
    p = plan()
    pals = icon_palettes()
    bad, changed, stale = [], [], []
    for sp, (d, grid, how, pi) in sorted(p.items()):
        h, w = size(bbox(grid))
        if h > GUARD_H or w > GUARD_W:
            bad.append("%s %dx%d (%s)" % (sp, w, h, how))
        path = os.path.join(GBA, d, "follower.png")
        old, oldpal = read_png_grid(path)
        if old != grid or oldpal != [tuple(c) for c in pals[pi]]:
            changed.append(sp)
            if write:
                write_png(path, grid, pals[pi])
    wanted = {os.path.join(GBA, d, "follower.png") for d, *_ in p.values()}
    for d in sorted(os.listdir(os.path.join(GBA, "graphics", "pokemon"))):
        f = os.path.join(GBA, "graphics", "pokemon", d, "follower.png")
        if os.path.exists(f) and f not in wanted:
            stale.append(d)
            if write:
                os.remove(f)
        elif os.path.exists(f):
            g, _ = read_png_grid(f)
            if g is not None and not write:
                h, w = size(bbox(g))
                if h > GUARD_H or w > GUARD_W:
                    bad.append("%s on disk %dx%d" % (d, w, h))
    text = render(p)
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if old != text and write:
        tmp = OUT + ".tmp"
        open(tmp, "w", encoding="utf-8").write(text)
        os.replace(tmp, OUT)
    hows = {}
    for sp, (_, _, how, _) in p.items():
        hows[how] = hows.get(how, 0) + 1
    print("  %d followers of their own (%s), %d bytes of tiles; the rest walk as their icon"
          % (len(p), ", ".join("%d %s" % (n, k) for k, n in sorted(hows.items())), len(p) * 512))
    if changed:
        print("  %d follower.png %s: %s" % (len(changed), "written" if write else "would change", " ".join(changed)))
    if stale:
        print("  %d stale follower.png %s: %s" % (len(stale), "removed" if write else "would be removed", " ".join(stale)))
    if old != text:
        print("  follower_gfx.h %s" % ("written" if write else "would change -- --write to write it"))
    elif not changed and not stale:
        print("  follower art and follower_gfx.h are current")
    #  THE GUARD: no follower taller than 22 or wider than 24 -- and no icon too big to follow left without a picture.
    if not write and old is not None:
        listed = set(re.findall(r"\[(SPECIES_\w+)\] = ", old))
        missing = sorted(set(p) - listed)
        if missing:
            bad.append("oversized icons with no follower picture in follower_gfx.h: " + " ".join(missing))
    if bad:
        print("  FAIL (T-464: a follower is at most %d tall and %d wide):" % (GUARD_H, GUARD_W))
        for b in bad:
            print("    " + b)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run("--write" in sys.argv))
