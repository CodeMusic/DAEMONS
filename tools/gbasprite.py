#!/usr/bin/env python3
"""Carry the daemon sprites into the GBA build, and give them colour.

    python3 tools/gbasprite.py [--write]

TWO DECISIONS ARE MADE HERE, and both are recorded in vision.md 9.4.

1. THE ART IS NOT UPSCALED. Our sprites are 40, 48 or 56 pixels square; Gen 3's
   frame is 64. Upscaling 40 to 64 is a 1.6x resample of hand-tuned pixel art
   and it would soften every edge the sprite doc spent weeks getting right. So
   each sprite is CENTRED in the frame at its native size. Gen 3 does not
   require a mon to fill its box either -- small species do not.

2. COLOUR IS BY TYPE, WHICH MAKES IT INFORMATION RATHER THAN DECORATION.
   Invariant 5 says greyscale is the design and colour appears once, at the
   Review Board. On a DMG the machine and the meaning agreed; on GBA they do
   not, and 9.3 flagged that as the thing that breaks. This is the answer: a
   daemon is coloured by what it IS, so the palette is another way of reading
   the chart rather than a coat of paint over it.

   Four of the anchors are not invented. Section 6 gives the Review Board its
   humours and their colours, and each humour already carries a type:

       Sanguine     red      air      VECTOR
       Choleric     yellow   fire     ENTROPY
       Melancholic  black    earth    LATENT
       Phlegmatic   water    calm     FROZEN

   The rest are extended from those, and every one of them is a claim this
   document is making rather than a fact it inherited.

Our four tones map to four palette entries: paper becomes index 0 (which Gen 3
treats as transparent), and the three inks become a light, a mid and a dark of
the type's hue. Level 0 stays nearly black -- it is the outline, and an outline
that takes the hue stops reading as an outline.
"""
import os, re, subprocess, sys, zlib, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbimg import read_png

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
import colorsys, glob
from PIL import Image
import numpy as np
from gridsample import deringe

SIZE = 64

RICH = "gfx/daemons"       # redrawn art, 9.4 as amended: hue ramp + accents
BODY_LEVELS = 5            # palette 1..5
MAX_ACCENTS = 5            # palette 6..10
SAT_ACCENT = 60            # a pixel this saturated is a marking, not body
SAT_BODY = 30              # this neutral is body; between the two is fringing

def ramp5(r, g, b):
    """Five steps of one hue: highlight, light, mid, dark, near-black outline.

    The outline keeps only a trace of the hue -- 9.4: an outline that takes
    the hue stops reading as an outline."""
    up = lambda t: tuple(min(255, int(c + (255 - c) * t)) for c in (r, g, b))
    dn = lambda t: tuple(max(0, int(c * t)) for c in (r, g, b))
    return [up(0.70), up(0.38), (r, g, b), dn(0.52), tuple(v + 10 for v in dn(0.16))]

def shift_off(accent, type_rgb):
    """A red eye on a VECTOR daemon is no eye. If an accent sits within 40
    degrees of the type's own hue, rotate it to the far side of the wheel."""
    ah = colorsys.rgb_to_hsv(*[c / 255 for c in accent])[0]
    th = colorsys.rgb_to_hsv(*[c / 255 for c in type_rgb])[0]
    d = abs(ah - th); d = min(d, 1 - d)
    if d >= 40 / 360:
        return accent
    h, sv, v = colorsys.rgb_to_hsv(*[c / 255 for c in accent])
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb((th + 0.5) % 1.0, sv, v))

def rich_src(ours, kind):
    hits = [f for f in glob.glob(os.path.join(ROOT, RICH, "%s_%s.*" % (ours.lower(), kind)))
            if not f.endswith(".txt")]
    return hits[0] if hits else None

def place_rich(path, type_rgb):
    """Redrawn art -> a 64x64 index grid and its palette.

    The body is neutral grey and becomes the type ramp; saturated pixels are
    markings and keep their own colour. JPEG ringing puts a band of weakly
    coloured pixels between the two, so anything in that band is treated as
    body -- a fringe is not a marking."""
    a = deringe(np.asarray(Image.open(path).convert("RGB")).astype(int))
    im = Image.fromarray(a.astype(np.uint8))
    sat = a.max(2) - a.min(2)
    subj = ~((a.min(2) > 232) & (sat < 24))              # not the flat paper

    ys, xs = np.where(subj)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    im = im.crop(box)
    mask = Image.fromarray((subj[box[1]:box[3], box[0]:box[2]] * 255).astype(np.uint8))
    sc = min(SIZE / im.width, SIZE / im.height)
    # 9.4 refuses to upscale, and grid sampling can now hand us art already at
    # or below target -- so clamp, and centre it small the way legacy art is.
    sc = min(sc, 1.0)
    # A ratio near 1 is the WORST case: barely shrinking lands source pixels on
    # fractional output positions and softens every edge. Snap it to 1:1.
    if sc > 0.92:
        sc = 1.0
    w, h = max(1, round(im.width * sc)), max(1, round(im.height * sc))
    if sc != 1.0:
        im = im.resize((w, h), Image.LANCZOS)
        mask = mask.resize((w, h), Image.LANCZOS).point(lambda v: 255 if v > 128 else 0)

    a = np.asarray(im).astype(int)
    m = np.asarray(mask) > 0
    sat = a.max(2) - a.min(2)
    acc = m & (sat >= SAT_ACCENT)

    pal = [BG] + ramp5(*type_rgb)
    grid = [[0] * SIZE for _ in range(SIZE)]
    ox, oy = (SIZE - w) // 2, (SIZE - h) // 2

    lum = (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000
    body = m & ~acc
    if body.any():                                        # spread over 5 steps
        lo, hi = lum[body].min(), lum[body].max()
        span = max(1, hi - lo)
        lvl = np.clip((lum - lo) * BODY_LEVELS // span, 0, BODY_LEVELS - 1)
    else:
        lvl = np.zeros_like(lum)

    accents = []
    if acc.any():
        px = Image.fromarray(a[acc].reshape(1, -1, 3).astype(np.uint8))
        n = min(MAX_ACCENTS, len(np.unique(a[acc].reshape(-1, 3), axis=0)))
        q = px.convert("P", palette=Image.ADAPTIVE, colors=n, dither=Image.NONE)
        t = q.getpalette()[:n * 3]
        cand = [shift_off(tuple(t[i*3:i*3+3]), type_rgb) for i in range(n)]
        for c in cand:      # JPEG turns one stripe into a gradient; five shades
            if all(sum((c[k]-e[k])**2 for k in range(3)) > 45*45 for e in accents):
                accents.append(c)                     # of blue look like one blue
    pal += accents

    for y in range(h):
        for x in range(w):
            if not m[y, x]:
                continue
            if acc[y, x] and accents:
                d = [sum((a[y, x, k] - c[k]) ** 2 for k in range(3)) for c in accents]
                grid[oy + y][ox + x] = 6 + d.index(min(d))
            else:
                grid[oy + y][ox + x] = BODY_LEVELS - lvl[y, x]   # light->1, dark->5
    return grid, pal

# hue anchors: (light, mid, dark)
def ramp(r, g, b):
    """A light / mid / dark ramp from one colour, and a near-black outline."""
    light = tuple(min(255, int(c + (255 - c) * 0.55)) for c in (r, g, b))
    mid = (r, g, b)
    dark = tuple(int(c * 0.30) + 8 for c in (r, g, b))
    return [light, mid, dark]

TYPE_COLOR = {
    # The four the Review Board already fixed (section 6).
    "FLYING":   (206,  70,  70),   # VECTOR   -- sanguine, red, air
    "FIRE":     (222, 158,  46),   # ENTROPY  -- choleric, yellow bile, fire
    "GHOST":    ( 92,  70, 118),   # LATENT   -- melancholic, black bile, earth
    "ICE":      (166, 206, 222),   # FROZEN   -- phlegmatic, water, calm
    # Extended from them.
    "NORMAL":   (198, 188, 168),   # CONTENT  -- bone; the undifferentiated one
    "FIGHTING": ( 96, 122, 158),   # LOGIC    -- cold steel blue
    "POISON":   (132, 118,  74),   # CORRUPT  -- something gone off
    "GROUND":   (158, 122,  78),   # STRATUM  -- the ground itself
    "ROCK":     (130, 130, 138),   # LEGACY   -- slate, and 5.1's cairn
    "BUG":      (128, 148,  72),   # SWARM    -- olive
    "WATER":    ( 70, 106, 176),   # FLOW     -- deep, moving
    "GRASS":    ( 92, 158,  96),   # GROWTH
    "ELECTRIC": ( 86, 190, 190),   # SIGNAL   -- a carrier, not a spark
    "PSYCHIC":  (176,  86, 158),   # CONTEXT  -- the thesis half
    "DRAGON":   ( 78, 168, 156),   # EMERGENT -- iridescent
}
BG = (205, 205, 172)               # what Gen 3 puts in index 0

DIR_FIX = {"NIDORAN♀": "nidoran_f", "NIDORAN♂": "nidoran_m",
           "FARFETCH'D": "farfetchd", "MR.MIME": "mr_mime",
           "MISSINGNO.": None}

def upstream(path):
    return subprocess.run(["git", "-C", GB, "show", "upstream/master:" + path],
                          capture_output=True, text=True).stdout

def renamed():
    pat = r'dname\s+"([^"]*)"'
    ours = re.findall(pat, open(os.path.join(GB, "data/pokemon/names.asm")).read())
    van = re.findall(pat, upstream("data/pokemon/names.asm"))
    return {v: o for v, o in zip(van, ours) if v != o}

def primary_type(slot_dir):
    p = os.path.join(GB, "data/pokemon/base_stats", slot_dir.replace("_", "") + ".asm")
    if not os.path.exists(p):
        return None
    # pokered writes this two ways in the same table -- "db GRASS, GRASS ; type"
    # and "db PSYCHIC_TYPE, PSYCHIC_TYPE ; type" -- and ours sometimes trails a
    # design note after the comment. Take the first token and drop the suffix.
    m = re.search(r'db\s+([A-Z_]+)\s*,\s*[A-Z_]+\s*;\s*type', open(p).read())
    if not m:
        return None
    t = m.group(1)
    return t[:-5] if t.endswith("_TYPE") else t

def write_png4(path, grid, palette, w=None, h=None):
    """4bpp indexed -- the shape Gen 3 wants. 64x64 for battle sprites; the
    derived assets pass their own size (32x32 overworld, 32x64 icon)."""
    w = w or SIZE
    h = h or SIZE
    plte = b"".join(bytes(c) for c in palette) + b"\x00\x00\x00" * (16 - len(palette))
    raw = b""
    for row in grid:
        packed = bytearray()
        for i in range(0, len(row), 2):
            packed.append((row[i] << 4) | row[i + 1])
        raw += b"\x00" + bytes(packed)
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 4, 3, 0, 0, 0))
           + chunk(b"PLTE", plte)
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)

#  DERIVED ASSETS. The overworld object and the party icon are not generated
#  separately -- they are REDUCED FROM THE FRONT SPRITE, so the creature in the
#  grass, the creature in the menu and the creature in battle are the same
#  drawing by construction rather than by luck. Three generations of the same
#  daemon would drift, and you would not notice until they sat side by side.
def _subject(grid, palette):
    """The front grid cropped to its drawn pixels, as RGB, square."""
    pts = [(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x]]
    if not pts:
        return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
    w, h = x1 - x0, y1 - y0
    n = max(w, h)
    im = Image.new("RGB", (n, n), palette[0])
    for y in range(y0, y1):
        for x in range(x0, x1):
            im.putpixel((x - x0 + (n - w) // 2, y - y0 + (n - h) // 2), tuple(palette[grid[y][x]]))
    return im

def derive_overworld(grid, palette):
    """32x32, one frame. Snorlax-class objects are static obstacles, so there
    is no walk cycle to keep consistent -- which is what makes a walking NPC
    hopeless and this straightforward."""
    im = _subject(grid, palette)
    if im is None:
        return None
    small = im.resize((32, 32), Image.NEAREST)
    idx = {tuple(c): i for i, c in enumerate(palette)}
    out = [[0] * 32 for _ in range(32)]
    for y in range(32):
        for x in range(32):
            out[y][x] = idx.get(small.getpixel((x, y)), 0)
    return out

def icon_palettes():
    out = []
    for i in range(3):
        f = os.path.join(GBA, "graphics/pokemon/icon_palettes/icon_palette_%d.pal" % i)
        cols = [tuple(int(v) for v in l.split())
                for l in open(f).read().split("\n")[3:] if l.strip()][:16]
        out.append(cols)
    return out

def derive_icon(grid, palette):
    """32x64 -- two 32x32 frames, the idle bob.

    Icons CANNOT carry the type ramp: gMonIconPaletteIndices picks one of three
    palettes shared by every species, and none of them holds the bone of NORMAL
    or most of the other ramps. So colour stops being information here and the
    silhouette carries it instead. 9.4 answers invariant 5 for front and back;
    the party menu is outside that answer, and this is where it shows.

    Mapped PER SOURCE COLOUR, not per pixel. Per-pixel nearest-colour on an
    antialiased reduction sends neighbouring body pixels to different entries
    and the result speckles. And the body is mapped among entries 1..15 only:
    entry 0 is transparent, and letting the body land there erases it."""
    im = _subject(grid, palette)
    if im is None:
        return None, None
    #  Vanilla icons do NOT fill their cell. Measured: pikachu occupies x 6-25,
    #  y 10-29 and bulbasaur x 6-25, y 12-28 -- roughly 20x20, sitting LOW with
    #  headroom above. Filling all 30x30 made DEADLOCK overflow into the party
    #  row above it, which is what the party menu actually showed.
    ICON_W, ICON_X, ICON_BOTTOM = 20, 6, 30
    small = im.resize((ICON_W, ICON_W), Image.NEAREST)
    bg = tuple(palette[0])
    src = [c for _, c in small.getcolors(4096)]
    best = None
    for pi, pal in enumerate(icon_palettes()):
        body = pal[1:]
        m, err, n = {}, 0.0, 0
        for c in src:
            if c == bg:
                m[c] = 0; continue
            j = min(range(len(body)), key=lambda k: sum((a - b) ** 2 for a, b in zip(c, body[k])))
            m[c] = j + 1
            err += sum((a - b) ** 2 for a, b in zip(c, body[j])) ** 0.5; n += 1
        err /= max(n, 1)
        if best is None or err < best[0]:
            best = (err, pi, m)
    err, pi, m = best
    out = [[0] * 32 for _ in range(64)]
    oy = ICON_BOTTOM - ICON_W              # bottom-aligned, like the vanilla ones
    for y in range(ICON_W):
        for x in range(ICON_W):
            v = m[small.getpixel((x, y))]
            out[oy + y][ICON_X + x] = v            # frame 1
            out[32 + oy + y][ICON_X + x] = v       # frame 2, the bob
    return out, (pi, err)

def write_pal(path, palette):
    lines = ["JASC-PAL", "0100", "16"]
    full = list(palette) + [(0, 0, 0)] * (16 - len(palette))
    lines += ["%d %d %d" % c for c in full]
    # JASC-PAL is a CRLF format and .gitattributes says so; writing LF makes git
    # rewrite all 66 of these on every checkout.
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())

def place(src, palette):
    """Centre the sprite in the frame, mapping our four tones to 0..3."""
    w, h, lum = read_png(src)
    g = [[0] * SIZE for _ in range(SIZE)]
    ox, oy = (SIZE - w) // 2, (SIZE - h) // 2
    for y in range(h):
        for x in range(w):
            v = min(3, lum(x, y) * 4 // 256)      # 0 dark .. 3 paper
            g[oy + y][ox + x] = 0 if v == 3 else 3 - v   # paper -> 0, dark -> 3
    return g

pairs = renamed()
done, skipped, ow_todo = 0, [], []
for vanilla, ours in sorted(pairs.items()):
    d = DIR_FIX.get(vanilla, vanilla.lower().replace(" ", "_").replace(".", ""))
    if d is None:
        continue
    outdir = os.path.join(GBA, "graphics/pokemon", d)
    if not os.path.isdir(outdir):
        skipped.append("%s (no graphics/pokemon/%s)" % (ours, d)); continue
    t = primary_type(d)
    if t not in TYPE_COLOR:
        skipped.append("%s (type %s)" % (ours, t)); continue
    legacy = [BG] + ramp(*TYPE_COLOR[t])
    palette, note = legacy, ""
    front_grid, front_pal = None, None
    for kind, src in (("front", "gfx/pokemon/front/%s.png" % d.replace("_", "")),
                      ("back",  "gfx/pokemon/back/%sb.png" % d.replace("_", ""))):
        rich = rich_src(ours, kind)
        if rich:
            grid, palette = place_rich(rich, TYPE_COLOR[t])
            note = "  redrawn (%d colours)" % len(palette)
        else:
            s = os.path.join(GB, src)
            if not os.path.exists(s):
                skipped.append("%s %s (%s)" % (ours, kind, src)); continue
            grid = place(s, legacy)
        if WRITE:
            write_png4(os.path.join(outdir, kind + ".png"), grid, palette)
        done += 1
        #  Both derived assets come off the FRONT, which is the only view that
        #  shows the whole creature.
        if kind == "front":
            front_grid, front_pal = grid, palette
    if WRITE:
        write_pal(os.path.join(outdir, "normal.pal"), palette)
        write_pal(os.path.join(outdir, "shiny.pal"), palette)

    #  Derived assets, only for daemons whose art we actually redrew -- a
    #  vanilla-sourced sprite has a vanilla icon and object already.
    extra = ""
    if front_grid is not None and note:
        ow = derive_overworld(front_grid, front_pal)
        owp = os.path.join(GBA, "graphics/object_events/pics/pokemon/%s.png" % d)
        if ow and os.path.exists(owp):
            #  The object's PNG carries INDICES; the game supplies the colours
            #  at runtime from whatever OBJ_EVENT_PAL_TAG its graphics info
            #  names. Vanilla points every creature at a generic NPC palette --
            #  NPC_BLUE for Snorlax -- and picks whichever is closest. Ours
            #  cannot do that: the indices are a type ramp, and rendering them
            #  through npc_blue is what turned DEADLOCK peach and yellow in the
            #  overworld.
            #
            #  So the ramp is written out as a palette beside the art. Per
            #  DAEMON rather than per type, because two daemons of one type can
            #  carry different accents and the palette has to match the indices
            #  exactly.
            palp = os.path.join(GBA, "graphics/object_events/palettes/daemon_%s.pal" % d)
            if WRITE:
                write_png4(owp, ow, front_pal, 32, 32)
                write_pal(palp, front_pal)
            extra += "  +overworld"
            #  The C side is NOT written here. A palette tag, a table entry and
            #  a graphics-info field are engine data, and they should appear in
            #  a diff somebody reads.
            ow_todo.append((ours, d))
        ic, info = derive_icon(front_grid, front_pal)
        if ic:
            if WRITE:
                write_png4(os.path.join(outdir, "icon.png"), ic, icon_palettes()[info[0]], 32, 64)
            #  The palette index is a per-species field, so say which one fits.
            #  It is NOT written here: gMonIconPaletteIndices is C, and editing
            #  it belongs to whoever is reading the diff.
            extra += "  +icon(pal %d, err %.0f)" % info

    print("  %-11s %-12s %-9s %s%s%s" % (ours, d, t, "written" if WRITE else "ready", note, extra))
print("  %d sprites, %d skipped" % (done, len(skipped)))
#  Only report what is actually OUTSTANDING. A checklist that keeps naming
#  finished work is one people learn to skim, and then it stops carrying the
#  one entry that matters.
def ow_wired(d):
    f = os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")
    try:
        return ("OBJ_EVENT_PAL_TAG_DAEMON_%s," % d.upper()) in open(f).read()
    except OSError:
        return False

ow_todo = [(o, d) for o, d in ow_todo if not ow_wired(d)]
if ow_todo:
    print("\n  OVERWORLD PALETTES WRITTEN -- these need three C edits each,")
    print("  or the object renders through a generic NPC palette and comes out wrong:")
    for ours, d in ow_todo:
        cap = "".join(w.capitalize() for w in d.split("_"))
        print("    %s (%s):" % (ours, d))
        print("      event_object_movement.c   #define OBJ_EVENT_PAL_TAG_DAEMON_%s  0x11xx" % d.upper())
        print("                                {gObjectEventPal_Daemon%s, OBJ_EVENT_PAL_TAG_DAEMON_%s}," % (cap, d.upper()))
        print("      object_event_graphics.h   const u16 gObjectEventPal_Daemon%s[] =" % cap)
        print("                                  INCBIN_U16(\"graphics/object_events/palettes/daemon_%s.gbapal\");" % d)
        print("      ..._graphics_info.h       .paletteTag = OBJ_EVENT_PAL_TAG_DAEMON_%s," % d.upper())
for s in skipped:
    print("     skip %s" % s)
