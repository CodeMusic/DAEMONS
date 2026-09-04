#!/usr/bin/env python3
"""Rewrite the title screen's copyright strip.

    python3 tools/gbastrip.py [--write]

The line under PRESS START still read (c)2004 GAME FREAK inc. It shares one
asset with PRESS START -- copyright_press_start is a 64-tile atlas, a 32x20
tilemap and one palette bank -- so it cannot be edited as a picture, and it
cannot be edited carelessly either:

  * PRESS START BLINKS by toggling BG palette bank 15, entries ONE TO FIVE,
    between the background and their real colours. The copyright text uses
    6 to 14 and so does not blink. Anything drawn here must stay out of 1-5
    or it starts flashing along with PRESS START.
  * the atlas holds SIXTY-FOUR tiles. Vanilla uses 62 of them.

So: reconstruct the screen through the tilemap, erase the old line off its red
band without disturbing the band, draw ours in the same white the old one used,
and deduplicate back down. The typeface is gencopyright.py's -- the same one
the boot screen uses -- so the two copyright lines in this game are visibly the
same object saying the same thing.
"""
import importlib.util, os, struct, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv

spec = importlib.util.spec_from_file_location("gc", os.path.join(HERE, "gencopyright.py"))
gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)

PNG = os.path.join(GBA, "graphics/title_screen/copyright_press_start.png")
BIN = os.path.join(GBA, "graphics/title_screen/copyright_press_start.bin")
TEXT = "@'11-'26  CODEMUSIC"
BAND = 12                         # the dark red the line sits on
# EVERY TILE ON THIS LAYER IS PALETTE BANK 15, and the high nibble of a map
# entry is where that lives. The first version of this tool rebuilt the map
# from tile indices alone and wrote bank 0, which is a silent, total change of
# meaning: bank 15 is the BACKGROUND palette and bank 0 is the LOGO's, so
# PRESS START, the copyright line and the band fills all started taking their
# colours from the wordmark's ramp -- yellow text on a yellow band -- and the
# blink stopped working, because Task_TitleScreen_BlinkPressStart writes
# entries 1-5 of bank 15 and nothing was reading them any more.
PALBANK = 15
# The old line is WHITE with a BLACK OUTLINE, and that black is index 6 -- the
# same index as the plain black above the band. Erasing 6 everywhere would take
# the black band with it, so the erase is confined to the rows the red owns.
TEXT_IDX = {6, 7, 8, 9, 10, 14}
INK, MAXTILES, ATLAS_W = 10, 64, 16

def glyph(ch):
    return None if ch == " " else gc.F['(c)' if ch == '@' else ch]

atlas = Image.open(PNG)
apx = atlas.load()
tmap = list(struct.unpack("<640H", open(BIN, "rb").read()))

# --- reconstruct the screen through the map -------------------------------
scr = [[0] * 256 for _ in range(160)]
for ty in range(20):
    for tx in range(32):
        t = tmap[ty * 32 + tx] & 0x3FF
        bx, by = (t % ATLAS_W) * 8, (t // ATLAS_W) * 8
        for y in range(8):
            for x in range(8):
                scr[ty * 8 + y][tx * 8 + x] = apx[bx + x, by + y]

# --- PRESS START moves down one tile row ----------------------------------
# It sat at y 129-135 and the face-off sprites reach y 135, so whichever
# creature stands on the left stood on the words. One tile row down clears the
# sprites with two pixels to spare and still leaves seven before the copyright
# band. It is a whole tile row, so nothing has to be redrawn -- the row is
# copied and the one it left is refilled with the band it was sitting on.
# It was also 33px left of the copyright's centre, because vanilla centred it
# under box art that is not there any more. Its ink is x 43-131, 89 wide, and
# (240-89)/2 is 75 -- a shift of exactly four tiles, so this stays tile-aligned
# and no glyph has to be redrawn.
# This tool rebuilds the screen from its own output, so the move has to be
# idempotent or a second run shifts PRESS START off the row it already moved
# to and erases it. The rows it occupies are the test: entries 1-5 are the
# text and nothing else on this layer uses them.
PS_FROM, PS_TO, PS_DX, BAND_IDX = 16, 17, 32, 6
PS_INK = {1, 2, 3, 4, 5}
if not any(v in PS_INK for y in range(8) for v in scr[PS_FROM * 8 + y]):
    print("  PRESS START is already on tile row %d -- left alone" % PS_TO)
else:
  for y in range(8):
      row = scr[PS_FROM * 8 + y]
      scr[PS_TO * 8 + y] = [BAND_IDX] * PS_DX + row[:256 - PS_DX]
      scr[PS_FROM * 8 + y] = [BAND_IDX] * 256
  print("  PRESS START moved to tile row %d (y %d-%d), %d px right"
        % (PS_TO, PS_TO * 8, PS_TO * 8 + 7, PS_DX))

# --- erase the old line, keeping the band it sits on ----------------------
# The old line STRADDLES the band's top edge -- its upper half sits on the
# black above it and its lower half on the red -- so erasing only the red rows
# left the tops of the letters behind. Each row is cleared to whatever that row
# is made of.
# The band is its FIRST AND LAST row, not the rows that happen to be mostly
# red. Testing membership in the sparse list said row 153 was not in the band,
# because the old text covered enough of it to fail the count -- so exactly the
# rows with text on them were the rows that did not get cleared.
rows = [y for y in range(160) if scr[y].count(BAND) > 128]
band = range(rows[0], rows[-1] + 1)
BLACK = 6
for y in range(band[0] - 8, band[-1] + 1):
    ground = BAND if y in band else BLACK
    for x in range(256):
        if scr[y][x] in TEXT_IDX and scr[y][x] != ground:
            scr[y][x] = ground
print("  the red band is rows %d-%d; cleared from %d" % (band[0], band[-1], band[0] - 8))

# --- draw ours, centred on the band ---------------------------------------
width = sum(4 if glyph(c) is None else len(glyph(c)[0]) + 1 for c in TEXT)
# Centred on the 240 the GBA shows, not on the 256 the tilemap is wide -- the
# extra sixteen columns are off the right edge, and centring on them pushed the
# line eight pixels right of centre.
x0 = (240 - width) // 2
y0 = band[0] + (len(band) - 8) // 2
x = x0
for ch in TEXT:
    rows = glyph(ch)
    if rows is None:
        x += 4; continue
    for r, row in enumerate(rows):
        for i, p in enumerate(row):
            if p == '#':
                scr[y0 + r][x + i] = INK
    x += len(rows[0]) + 1
print("  \"%s\"  %dpx wide, from x=%d" % (TEXT.replace('@', '(c)'), width, x0))

# --- deduplicate back into the atlas --------------------------------------
tiles, index, newmap = [], {}, [0] * 640
for ty in range(20):
    for tx in range(32):
        t = tuple(scr[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8))
        if t not in index:
            if len(tiles) >= MAXTILES:
                sys.exit("  !! more than %d tiles -- the atlas cannot hold it" % MAXTILES)
            index[t] = len(tiles); tiles.append(t)
        newmap[ty * 32 + tx] = index[t] | (PALBANK << 12)
print("  %d of %d atlas tiles used" % (len(tiles), MAXTILES))

if WRITE:
    out = Image.new("P", atlas.size, 0)
    out.putpalette(atlas.getpalette())
    op = out.load()
    for i, t in enumerate(tiles):
        bx, by = (i % ATLAS_W) * 8, (i // ATLAS_W) * 8
        for k, v in enumerate(t):
            op[bx + k % 8, by + k // 8] = v
    out.save(PNG)
    with open(BIN, "wb") as f:
        for v in newmap:
            f.write(bytes((v & 0xFF, (v >> 8) & 0xFF)))
    print("  written: atlas and tilemap")
