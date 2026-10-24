"""sheets2.py -- round two's sheets, t452b_*.png in the scratchpad: one per daemon, the overview, two battle mocks
at 1x, and the icons. Reads gfx/drafts/t452/b/picks2.json and b/reduced/; reads the pilot's reduced art beside it."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t452"; B = D + "/b"
SP = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
PICK = {k: v for k, v in json.load(open(B + "/picks2.json")).items() if not k.startswith("_")}
SLOT = {"rovercub": "bulbasaur", "packet": "pidgey", "spike": "pikachu", "backbone": "onix", "dangling": "gastly", "artsai": "mew"}
try:
    F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
except Exception:
    F = FS = ImageFont.load_default()
PAPER = (236, 234, 226); INKC = (30, 30, 34); GAMEBG = (205, 205, 172); PARTY = (98, 156, 131)

def sprite(path, pal_from=None):
    """indexed 4bpp, index 0 transparent; drawn through pal_from's palette when given (the engine's normal.pal)."""
    im = Image.open(path)
    if pal_from: im.putpalette(Image.open(pal_from).getpalette())
    a = im.convert("RGBA"); px = np.array(im); al = np.array(a); al[px == 0, 3] = 0
    return Image.fromarray(al)
def today(n, k="front"):
    im = Image.open(f"{R}/gfx/daemons/{n}_{k}.png").convert("RGBA")
    return im if im.width == 64 else im.resize((64, 64), Image.LANCZOS)
def on(im, bg, scale=1):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width * scale, im.height * scale), Image.NEAREST)
def big(path, s):
    return Image.open(path).convert("RGB").resize((s, s), Image.NEAREST)

def daemon_sheet(n, p):
    m = p["measured"]; red = f"{B}/reduced/{n}_front.png"
    cols = [("today front 3x", on(today(n), GAMEBG, 3)),
            ("512 draft (384)", big(f"{B}/{p['front']}", 384)),
            ("64 1x", on(sprite(red), GAMEBG, 1)),
            ("64 3x  accents %.1f%%" % m["front_accent_pct"], on(sprite(red), GAMEBG, 3))]
    if p.get("back"):
        rb = f"{B}/reduced/{n}_back.png"
        cols += [("today back 3x", on(today(n, "back"), GAMEBG, 3)),
                 ("back draft (192)", big(f"{B}/{p['back']}", 192)),
                 ("back 1x", on(sprite(rb), GAMEBG, 1)),
                 ("back 3x  %.1f%%" % m["back_accent_pct"], on(sprite(rb), GAMEBG, 3))]
    if os.path.exists(f"{B}/reduced/{n}_icon.png"):
        ic = sprite(f"{B}/reduced/{n}_icon.png").crop((0, 0, 32, 32))
        cols += [("icon 1x", on(ic, PARTY, 1)), ("icon 3x", on(ic, PARTY, 3))]
    W = sum(c[1].width for c in cols) + 20 * (len(cols) + 1); H = max(c[1].height for c in cols) + 130
    s = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 10), "%s (%s, %s) -- T-452 round two, DRAFT -- %s" % (p["name"], p["gametype"], p["type"], p["props"]), fill=INKC, font=F)
    d.text((20, 32), p.get("note", ""), fill=INKC, font=FS)
    x = 20
    for lab, im in cols:
        s.paste(im, (x, 56)); d.text((x, 62 + im.height), lab, fill=INKC, font=FS); x += im.width + 20
    s.save(SP + "t452b_%s.png" % n)

def battle(foe, plr, out):
    bg = Image.open(SP + "battle_bg_clean.png").convert("RGBA")
    f = sprite(f"{B}/reduced/{foe}_front.png"); b = sprite(f"{B}/reduced/{plr}_back.png", f"{B}/reduced/{plr}_front.png")
    bg.alpha_composite(f, (144, 8)); bg.alpha_composite(b, (40, 48))
    one = bg.convert("RGB")
    s = Image.new("RGB", (240 + 720 + 72, 520), PAPER); d = ImageDraw.Draw(s)
    s.paste(one, (24, 60)); s.paste(one.resize((720, 480), Image.NEAREST), (288, 30))
    d.text((24, 8), "MOCK, T-452 round two DRAFT: %s front vs %s back, 1x (left) and 3x" % (foe.upper(), plr.upper()), fill=INKC, font=FS)
    d.text((24, 236), "boxes and names from\n.theatre/t392f_rel_battle.png\n(POLL vs CODEMUSAI);\nonly the two sprites\nare new", fill=INKC, font=FS)
    s.save(SP + out)

def overview():
    cw = 64 + 8 + 128 + 24
    s = Image.new("RGB", (24 + 6 * cw, 600), PAPER); d = ImageDraw.Draw(s)
    d.text((24, 10), "T-452 round two, DRAFT: today (top), the pilot (middle), round two (bottom); 1x and 2x, coloured by type", fill=INKC, font=F)
    x = 24
    for n, p in PICK.items():
        d.text((x, 40), "%s  %s" % (p["name"], p["type"]), fill=INKC, font=FS)
        d.text((x, 56), "accents %.1f%%" % p["measured"]["front_accent_pct"], fill=INKC, font=FS)
        rows = [today(n), sprite(f"{D}/reduced/{n}_front.png"), sprite(f"{B}/reduced/{n}_front.png")]
        for i, im in enumerate(rows):
            y = 80 + i * 170
            s.paste(on(im, GAMEBG, 1), (x, y)); s.paste(on(im, GAMEBG, 2), (x + 72, y))
        x += cw
    s.save(SP + "t452b_overview.png")

def icons():
    cols = ["today", "pilot derived", "derived, round 2", "drawn, round 2"]
    S = 3; cw = 32 * S + 32 + 40
    s = Image.new("RGB", (160 + len(cols) * cw, 70 + 6 * (32 * S + 24)), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 10), "T-452 round two, DRAFT: party icons at 1x and 3x on the party-menu green. Shared icon palettes, so colour is the silhouette's job.", fill=INKC, font=FS)
    for j, c in enumerate(cols): d.text((160 + j * cw, 40), c, fill=INKC, font=FS)
    for i, (n, p) in enumerate(PICK.items()):
        y = 64 + i * (32 * S + 24)
        d.text((20, y + 40), p["name"], fill=INKC, font=FS)
        srcs = [f"{R}/engineGba/graphics/pokemon/{SLOT[n]}/icon.png", f"{D}/reduced/{n}_icon.png",
                f"{B}/reduced/{n}_icon_derived.png", f"{B}/reduced/{n}_icon.png"]
        for j, f in enumerate(srcs):
            x = 160 + j * cw
            if not os.path.exists(f):
                d.text((x, y + 40), "(none)", fill=INKC, font=FS); continue
            ic = sprite(f).crop((0, 0, 32, 32))
            s.paste(on(ic, PARTY, 1), (x, y + 32)); s.paste(on(ic, PARTY, S), (x + 40, y))
    s.save(SP + "t452b_icons.png")

for n, p in PICK.items(): daemon_sheet(n, p)
overview(); icons()
for foe, plr in json.load(open(B + "/picks2.json")).get("_battles", []):
    battle(foe, plr, "t452b_battle_%s_vs_%s.png" % (foe, plr))
print("sheets written")
