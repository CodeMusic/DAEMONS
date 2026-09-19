#!/usr/bin/env python3
"""The trial as the game would show it: objects cleaned (cleandraft's flood fill), fitted to their size and quantized
into the palette they already draw in; people sampled back to 16x32 frames, their hues kept (the building pilot's
lesson), and quantized into their own palette. Writes sheet.png."""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
T = "gfx/drafts/t164/people"; M = "engineGba/graphics/object_events/pics"
def pal_of(png):
    im = Image.open(png); p = im.getpalette()[:48]; return [tuple(p[i:i+3]) for i in range(0, 48, 3)]
def quant(rgba, pal):
    a = np.asarray(rgba.convert("RGBA")).astype(int); out = np.zeros(a.shape[:2], int); P = np.array(pal[1:], float)
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x, 3] >= 128:
                out[y, x] = 1 + int(((P - a[y, x, :3]) ** 2).sum(1).argmin())
    img = Image.new("RGB", (a.shape[1], a.shape[0]), (214, 211, 190)); px = img.load()
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if out[y, x]: px[x, y] = pal[out[y, x]]
    return img
def shown(png):
    im = Image.open(png); pal = pal_of(png); a = im.load(); img = Image.new("RGB", im.size, (214, 211, 190)); px = img.load()
    for y in range(im.height):
        for x in range(im.width):
            if a[x, y]: px[x, y] = pal[a[x, y]]
    return img
rows = []
for name in ("sign", "fossil", "town_map", "lapras_doll"):
    ref = "%s/misc/%s.png" % (M, name); W, H = Image.open(ref).size; pal = pal_of(ref)
    row = [("now", shown(ref))]
    for s in (1917, 42, 88):
        c = "%s/clean_obj_%s_%d.png" % (T, name, s)
        subprocess.run(["python3", "tools/cleandraft.py", "%s/obj_%s_%d.png" % (T, name, s), c], capture_output=True)
        im = Image.open(c).convert("RGBA"); im = im.crop(im.getbbox()); f = min((W - 1) / im.width, (H - 1) / im.height)
        small = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
        canvas = Image.new("RGBA", (W, H)); canvas.paste(small, ((W - small.width) // 2, H - small.height)); row.append((str(s), quant(canvas, pal)))
    rows.append((name, row))
from skimage import color
for name in ("cameraman", "rich_boy", "town_doldrum_child"):
    ref = "%s/people/%s.png" % (M, name); pal = pal_of(ref); orig = Image.open(ref); mask = np.asarray(orig) != 0
    now = np.asarray(shown(ref)).astype(float)
    row = [("now", shown(ref))]
    for dn in ("40", "55"):
        a = np.asarray(Image.open("%s/ppl_%s_%s.png" % (T, name, dn)).convert("RGB")).astype(int)
        h, w = orig.height, orig.width
        nat = np.array([[np.median(a[y*8+2:y*8+6, x*8+2:x*8+6].reshape(-1, 3), axis=0) for x in range(w)] for y in range(h)]).astype(float)
        L = color.rgb2lab(nat / 255); L[..., 1:] = color.rgb2lab(now / 255)[..., 1:]; nat = np.clip(color.lab2rgb(L) * 255, 0, 255)
        rgba = np.dstack([nat, mask * 255]).astype(np.uint8)
        row.append((dn, quant(Image.fromarray(rgba, "RGBA"), pal)))
    rows.append((name, row))
S = 4; x0 = 150
sh = Image.new("RGB", (x0 + 4 * (144 * S + 10), sum(max(i.height for _, i in r) * S + 20 for _, r in rows)), (40, 40, 44)); d = ImageDraw.Draw(sh); y = 0
for name, row in rows:
    hh = max(i.height for _, i in row) * S; d.text((4, y + hh // 2), name, fill=(230, 230, 230)); x = x0
    for lab, im in row:
        d.text((x, y + 2), lab, fill=(200, 200, 200)); sh.paste(im.resize((im.width * S, im.height * S), Image.NEAREST), (x, y + 14)); x += im.width * S + 10
    y += hh + 20
sh.save("%s/sheet.png" % T)
