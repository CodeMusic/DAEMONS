"""T-452 forms review sheets: today's forms (what the engine has now) beside the new ones, front / back / icon, 1x and 3x,
each through the palette the engine loads for it; the new fronts again through their shiny palette.
    sheet.py proteus OUT     sheet.py overloaded OUT"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); E = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/wtf/engine/graphics/pokemon"
G = "/Users/christopherhicks/Projects/pokefirered-daemons/graphics/pokemon"
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
PAPER = (236, 234, 226); INK = (30, 30, 34); GROUND = (205, 205, 172); PARTY = (98, 156, 131); RED = (160, 40, 40)

def readpal(p):
    l = open(p).read().split("\n")[3:19]; return [tuple(int(v) for v in r.split()[:3]) for r in l if r.strip()]
def show(path, pal=None, rows=None, crop=None):
    im = Image.open(path); idx = np.array(im)
    if rows: idx = idx[rows[0]:rows[1]]
    if crop: idx = idx[:, :crop]
    p = pal or [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    a = np.zeros(idx.shape + (4,), np.uint8)
    for i, c in enumerate(p[:16]): a[idx == i, :3] = c; a[idx == i, 3] = 255
    a[idx == 0, 3] = 0
    return Image.fromarray(a)
def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)

def cell(s, d, x, y, im, bg, label=None):
    """1x then 3x side by side; returns the width used"""
    if label: d.text((x, y - 16), label, fill=INK, font=FS)
    s.paste(on(im, bg, 1), (x, y)); s.paste(on(im, bg, 3), (x + im.width + 6, y))
    return im.width * 4 + 6

def grid_sheet(out, title, cols, rows, notes):
    """cols: column titles; rows: [(row label, [(img, bg) or None per col])]"""
    CW, RH, LW = 4 * 64 + 6 + 60, 3 * 64 + 34, 150
    s = Image.new("RGB", (LW + len(cols) * CW + 20, 70 + len(rows) * RH + 20 + 18 * len(notes)), PAPER); d = ImageDraw.Draw(s)
    import textwrap
    d.text((20, 6), "\n".join(textwrap.wrap(title, (s.width - 40) // 9)), fill=INK, font=F)
    for j, c in enumerate(cols): d.text((LW + j * CW, 46), c, fill=INK, font=FS)
    for i, (lab, cells) in enumerate(rows):
        y = 70 + i * RH
        d.text((20, y + 10), lab, fill=RED if lab.startswith("NEW") or lab.startswith("new") else INK, font=FS)
        if i and rows[i - 1][0].split()[0] != lab.split()[0]: d.line((20, y - 12, s.width - 20, y - 12), fill=INK, width=2)
        for j, c in enumerate(cells):
            if c is None: continue
            im, bg = c; cell(s, d, LW + j * CW, y + (64 - im.height // 2 if im.height < 64 else 0) if False else y, im, bg)
    notes = [w for n in notes for w in textwrap.wrap(n, (s.width - 40) // 7)]
    s2 = Image.new("RGB", (s.width, s.height + 18 * len(notes)), PAPER); s2.paste(s, (0, 0)); s = s2; d = ImageDraw.Draw(s)
    for k, n in enumerate(notes): d.text((20, s.height - 18 * (len(notes) - k) - 8), n, fill=INK, font=FS)
    s.save(out); print(out, s.size)

def proteus(out):
    tp, np_ = readpal(G + "/deoxys/normal.pal"), readpal(E + "/deoxys/normal.pal"); ns = readpal(E + "/deoxys/shiny.pal")
    def two(base, f, half, pal): return show(f"{base}/{f}.png", pal, rows=(0, 64) if half == 0 else (64, 128))
    def ic(base, f): return show(f"{base}/{f}.png", rows=(0, 32))
    T, N = G + "/deoxys", E + "/deoxys"
    rows = [("today front", [(two(T, "front", 0, tp), GROUND), (two(T, "front", 1, tp), GROUND), (two(T, "front_def", 1, tp), GROUND)]),
            ("today back", [(two(T, "back", 0, tp), GROUND), (two(T, "back", 1, tp), GROUND), (two(T, "back_def", 1, tp), GROUND)]),
            ("today icon", [(ic(T, "icon"), PARTY), (ic(T, "icon_attack"), PARTY), (ic(T, "icon_defense"), PARTY)]),
            ("NEW front", [(two(N, "front", 0, np_), GROUND), (two(N, "front", 1, np_), GROUND), (two(N, "front_def", 1, np_), GROUND)]),
            ("NEW back", [(two(N, "back", 0, np_), GROUND), (two(N, "back", 1, np_), GROUND), (two(N, "back_def", 1, np_), GROUND)]),
            ("NEW icon", [(ic(N, "icon"), PARTY), (ic(N, "icon_attack"), PARTY), (ic(N, "icon_defense"), PARTY)]),
            ("NEW shiny", [(two(N, "front", 0, ns), GROUND), (two(N, "front", 1, ns), GROUND), (two(N, "front_def", 1, ns), GROUND)])]
    grid_sheet(out, "T-452 forms -- PROTEUS (DEOXYS slot, 410), BUILT (engine tforms 87557e860): today (top) | new (bottom), 1x and 3x, through the one species palette",
               ["HOODED (the Index; sheets' top half)", "ALL EDGES (CONTENT's battle form)", "SHELL (CONTEXT's battle form)"], rows,
               ["One palette for every view (genproteus): the hooded front's. The same two orange eyes in all three forms (orange is outside PSYCHIC's hue reach).",
                "Backs: each front mirrored with the face flattened. Icons: icon3, all three on icon palette 1 (today's are on 0).",
                "Streak slots show their blank grey, as before a streak is earned."])

def overloaded(out):
    forms = ["normal", "sunny", "rainy", "snowy"]; T = G + "/castform"
    def today(f, k): return show(f"{T}/{f}/{k}.png", readpal(f"{T}/{f}/normal.pal"))
    def new(f, k, pal="normal"):
        b = E + "/castform"
        return show(f"{b}/{f}/{k}.png", readpal(f"{b}/{f}/{pal}.pal"))
    icon = show(T + "/icon.png", rows=(0, 32))
    rows = [("today front", [(today(f, "front"), GROUND) for f in forms]),
            ("today back", [(today(f, "back"), GROUND) for f in forms]),
            ("NEW front", [(new(f, "front"), GROUND) for f in forms]),
            ("NEW back", [(new(f, "back"), GROUND) for f in forms]),
            ("NEW shiny", [(new(f, "front", "shiny"), GROUND) for f in forms]),
            ("icon (one)", [(icon, PARTY), None, None, None])]
    grid_sheet(out, "T-452 forms -- OVERLOADED (CASTFORM slot, 385), BUILT (engine tforms 87557e860): today (vanilla weathers) | new, 1x and 3x, each through its own form palette",
               ["NORMAL (CONTENT; re-cleaned, top closed)", "SUNNY (FIRE / ENTROPY)", "RAINY (WATER / FLOW)", "SNOWY (ICE / FROZEN)"], rows,
               ["NORMAL: batch 18s draft re-cleaned on a keyed ground (its top closed), batch 18s hand edits again, its back flattened like the weathers. Each weather drawn from that draft by image-to-image. NEW = what tools/gencastform.py writes.",
                "Each weather in its own palette, coloured by the type Forecast gives it (sun ENTROPY, rain FLOW, hail FROZEN), as vanilla's per-form palettes do.",
                "CASTFORM has one party icon for every form (batch 18's); there are no form icons to draw. Backs: the front mirrored, face flattened."])

if __name__ == "__main__":
    {"proteus": proteus, "overloaded": overloaded}[sys.argv[1]](sys.argv[2])
