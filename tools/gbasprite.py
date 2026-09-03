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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
SIZE = 64

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

def write_png4(path, grid, palette):
    """64x64, 4bpp, indexed -- the shape Gen 3 wants."""
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
           + chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 4, 3, 0, 0, 0))
           + chunk(b"PLTE", plte)
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)

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
done, skipped = 0, []
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
    palette = [BG] + ramp(*TYPE_COLOR[t])
    for kind, src in (("front", "gfx/pokemon/front/%s.png" % d.replace("_", "")),
                      ("back",  "gfx/pokemon/back/%sb.png" % d.replace("_", ""))):
        s = os.path.join(GB, src)
        if not os.path.exists(s):
            skipped.append("%s %s (%s)" % (ours, kind, src)); continue
        if WRITE:
            write_png4(os.path.join(outdir, kind + ".png"), place(s, palette), palette)
        done += 1
    if WRITE:
        write_pal(os.path.join(outdir, "normal.pal"), palette)
        write_pal(os.path.join(outdir, "shiny.pal"), palette)
    print("  %-11s %-12s %-9s %s" % (ours, d, t, "written" if WRITE else "ready"))
print("  %d sprites, %d skipped" % (done, len(skipped)))
for s in skipped:
    print("     skip %s" % s)
