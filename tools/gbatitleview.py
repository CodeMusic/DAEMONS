#!/usr/bin/env python3
"""Render the title screen offline, exactly as the GBA composites it.

    python3 tools/gbatitleview.py content
    python3 tools/gbatitleview.py context --out /tmp/shot.png

Layout work on a screen this crowded was being done by squinting at emulator
screenshots and guessing at pixel coordinates. This composites the real assets
at the real coordinates instead, so a collision is a fact rather than an
impression, and it reports the ink bounding box of every layer.

BG0 logo (8bpp, prio 0) / BG1 subtitle (prio 1) / BG2 copyright and PRESS START
(prio 2) / BG3 the bands (prio 3), and the two face-off sprites at OBJ priority
1 -- which on this hardware puts them ABOVE BG1 and BG2 and below BG0. That
rule is the whole reason PRESS START disappeared.
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GFX = os.path.join(ROOT, "engineGba/graphics/title_screen")
W, H = 240, 160

#  Kept in step with src/title_screen.c by hand; the tool prints them so a
#  drift shows up as a collision report that does not match the emulator.
FACEOFF_LEFT_X, FACEOFF_RIGHT_X, FACEOFF_Y = 50, 190, 104

def pal(path):
    lines = open(path).read().split()
    n = int(lines[2])
    v = [int(x) for x in lines[3:3 + n * 3]]
    #  The GBA keeps 5 bits a channel; a .pal that has not been through that
    #  quantisation lies about what the screen shows.
    return [tuple((c >> 3) * 255 // 31 for c in v[i*3:i*3+3]) for i in range(n)]

def tiles(path, bpp):
    d = open(path, "rb").read()
    size = 32 if bpp == 4 else 64
    out = []
    for t in range(len(d) // size):
        b, px = d[t*size:(t+1)*size], []
        if bpp == 4:
            for byte in b:
                px += [byte & 0xF, byte >> 4]
        else:
            px = list(b)
        out.append(px)
    return out

def layer(gfx, binmap, bpp, palettes, fixed_pal=None):
    """One background, as (RGB image, alpha mask)."""
    ts = tiles(gfx, bpp)
    d = open(binmap, "rb").read()
    ents = struct.unpack("<%dH" % (len(d)//2), d)
    img = Image.new("RGB", (W, H)); a = Image.new("L", (W, H), 0)
    ip, ap = img.load(), a.load()
    for i, e in enumerate(ents):
        r, c = divmod(i, 32)
        if c * 8 >= W or r * 8 >= H:
            continue
        idx, hf, vf, pn = e & 0x3FF, e & 0x400, e & 0x800, e >> 12
        if idx >= len(ts):
            continue
        px = ts[idx]
        for y in range(8):
            for x in range(8):
                sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                v = px[sy * 8 + sx]
                if v == 0:
                    continue
                col = palettes[(fixed_pal if fixed_pal is not None else pn) * 16 + v] \
                      if bpp == 4 else palettes[v]
                ip[c*8 + x, r*8 + y] = col
                ap[c*8 + x, r*8 + y] = 255
    return img, a

def sprite(png, x, y, flip):
    im = Image.open(png).convert("RGBA")
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    #  Index 0 of a sprite's palette is transparent; the PNGs keep it as a
    #  colour, so drop whatever the top-left pixel is.
    key = Image.open(png).convert("RGB").getpixel((0, 0))
    px = im.load()
    for j in range(im.height):
        for i in range(im.width):
            if px[i, j][:3] == key:
                px[i, j] = (0, 0, 0, 0)
    return im, (x - im.width // 2, y - im.height // 2)

def box(mask, name, report):
    bb = mask.getbbox()
    report.append((name, bb))
    return bb

def main():
    ed = (sys.argv[1] if len(sys.argv) > 1 else "content").lower()
    sub = "firered" if ed == "content" else "leafgreen"
    E = os.path.join(GFX, sub)

    logo_pal = pal(os.path.join(E, "game_title_logo.pal"))
    art_pal  = pal(os.path.join(E, "box_art_mon.pal"))
    bg_pal   = pal(os.path.join(E, "background.pal"))

    #  Slots 0-12 logo, 13 subtitle, 14 and 15 both the background palette.
    four = [(0, 0, 0)] * 256
    #  BG2 draws with palette 0, which is the LOGO's first sixteen colours --
    #  so the wordmark ramp is also painting the background fill behind it.
    for i, c in enumerate(logo_pal[:208]): four[i] = c
    for i, c in enumerate(art_pal[:16]): four[13 * 16 + i] = c
    for i, c in enumerate(bg_pal[:16]):  four[14 * 16 + i] = c; four[15 * 16 + i] = c

    rep = []
    bg3, a3 = layer(os.path.join(GFX, "border_bg.4bpp"),
                    os.path.join(E, "border_bg.bin"), 4, four)
    bg2, a2 = layer(os.path.join(GFX, "copyright_press_start.4bpp"),
                    os.path.join(GFX, "copyright_press_start.bin"), 4, four)
    bg1, a1 = layer(os.path.join(E, "box_art_mon.4bpp"),
                    os.path.join(E, "box_art_mon.bin"), 4, four, fixed_pal=13)
    bg0, a0 = layer(os.path.join(E, "game_title_logo.8bpp"),
                    os.path.join(E, "game_title_logo.bin"), 8, logo_pal)

    #  The backdrop is palette entry 0, which is what shows where every layer
    #  is transparent -- the bands are partly this.
    out = Image.new("RGB", (W, H), logo_pal[0])
    for im, a in ((bg3, a3), (bg2, a2), (bg1, a1)):
        out.paste(im, (0, 0), a)

    left_png  = "codemusai.png" if ed == "content" else "caremusai.png"
    right_png = "caremusai.png" if ed == "content" else "codemusai.png"
    sprites = []
    for png, x, flip in ((left_png, FACEOFF_LEFT_X, False),
                         (right_png, FACEOFF_RIGHT_X, True)):
        im, at = sprite(os.path.join(GFX, "faceoff", png), x, FACEOFF_Y, flip)
        out.paste(im, at, im)
        sprites.append((png, at, im.size))
    out.paste(bg0, (0, 0), a0)          # BG0 is priority 0: above the sprites

    box(a0, "BG0  wordmark", rep); box(a1, "BG1  subtitle", rep)
    box(a2, "BG2  copyright + PRESS START", rep); box(a3, "BG3  bands", rep)
    print("  %s (%s)" % (ed.upper(), sub))
    for name, bb in rep:
        print("    %-30s x %3d-%-3d  y %3d-%-3d" % (name, bb[0], bb[2]-1, bb[1], bb[3]-1)
              if bb else "    %-30s empty" % name)
    for png, at, size in sprites:
        print("    %-30s x %3d-%-3d  y %3d-%-3d"
              % ("OBJ  " + png, at[0], at[0]+size[0]-1, at[1], at[1]+size[1]-1))

    dst = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv \
          else "/tmp/title_%s.png" % ed
    out.resize((W * 3, H * 3), Image.NEAREST).save(dst)
    print("    written %s" % dst)

main()
