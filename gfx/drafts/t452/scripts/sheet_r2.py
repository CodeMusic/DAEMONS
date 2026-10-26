"""T-452 round two's contact sheets: each daemon's in-ROM art beside the draft, front / back / icon, 1x and 3x, and
the draft's shiny (genshiny.make_shiny on the draft's own palette, as gbasprite.py would make it).

    sheet_r2.py OUT.png TITLE NAME:DIR[:what changed] ...

DIR is the draft folder under gfx/drafts/t452 holding reduced/NAME_{front,back,icon}.png; a missing file draws the
in-ROM one again, marked "(unchanged)". Reads the engine tree, writes only OUT."""
import sys, os, json, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbs
sys.path.insert(0, "/Users/christopherhicks/Projects/DAEMONS/tools")
import genshiny
R = "/Users/christopherhicks/Projects/DAEMONS"; T = R + "/gfx/drafts/t452"; G = R + "/engineGba/graphics/pokemon/"
SPEC = json.load(open(R + "/companion/server/data/species.json")); BY = {v["name"].lower(): v for v in SPEC.values()}
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
PAPER = (236, 234, 226); INK = (30, 30, 34); GROUND = (205, 205, 172); PARTY = (98, 156, 131); RED = (170, 40, 40)

def readpal(f):
    l = open(f).read().splitlines()[3:19]; return [tuple(int(v) for v in x.split()) for x in l]

def show(png, pal=None, h=64):
    im = Image.open(png)
    if pal: im.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    idx = np.array(im); a = np.array(im.convert("RGBA")); a[idx == 0, 3] = 0
    return Image.fromarray(a).crop((0, 0, im.width, h))

def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)

def panel(name, d, what):
    v = BY[name]; slot = v["constant"].lower(); typ = gbs.primary_type(slot)
    rom = G + slot; npal = readpal(rom + "/normal.pal"); spal = readpal(rom + "/shiny.pal")
    nd = f"{T}/{d}/reduced/{name}_"
    def new(k):
        f = nd + k + ".png"; return f if os.path.exists(f) else None
    fpal = Image.open(new("front")).getpalette()[:48] if new("front") else None
    fpal = [tuple(fpal[i:i + 3]) for i in range(0, 48, 3)] if fpal else None
    _, shiny = genshiny.make_shiny(fpal) if fpal else (None, None)
    W = 1500; H = 352
    s = Image.new("RGB", (W, H), PAPER); dr = ImageDraw.Draw(s)
    dr.text((12, 6), "%d %s  %s / %s  DRAFT" % (v["national"], v["name"], "/".join(v["types"]), typ), fill=INK, font=F)
    dr.text((12, 26), "\n".join(textwrap.wrap(what, 200))[:400], fill=RED, font=FS)
    y = 62
    cols = [("IN ROM front", show(rom + "/front.png", npal), GROUND),
            ("back", show(rom + "/back.png", npal), GROUND),
            ("icon", show(rom + "/icon.png", None, 32), PARTY),
            ("DRAFT front", show(new("front") or rom + "/front.png", None if new("front") else npal), GROUND),
            ("back", show(new("back") or rom + "/back.png", fpal if new("back") else npal), GROUND),
            ("icon", show(new("icon") or rom + "/icon.png", None, 32), PARTY),
            ("DRAFT shiny", show(new("front") or rom + "/front.png", shiny if shiny else spal), GROUND)]
    x = 12
    for i, (lab, im, bg) in enumerate(cols):
        sc = 3; w = im.width * sc
        if i == 3: x += 30; dr.line((x - 18, y, x - 18, H - 10), fill=INK, width=2)
        dr.text((x, y), lab + ("" if (i < 3 or i == 6 or new(["front", "back", "icon"][i - 3])) else " (unchanged)"), fill=INK, font=FS)
        s.paste(on(im, bg, 1), (x, y + 18)); s.paste(on(im, bg, sc), (x, y + 18 + im.height + 8))
        x += max(w, 110) + 14
    return s

if __name__ == "__main__":
    out, title = sys.argv[1], sys.argv[2]
    ps = []
    for a in sys.argv[3:]:
        n, d, *w = a.split(":", 2); ps.append(panel(n, d, w[0] if w else ""))
    H = 40 + sum(p.height for p in ps)
    s = Image.new("RGB", (1500, H), PAPER); ImageDraw.Draw(s).text((12, 10), title, fill=INK, font=F)
    y = 40
    for p in ps: s.paste(p, (0, y)); y += p.height
    s.save(out); print(out, s.size)
