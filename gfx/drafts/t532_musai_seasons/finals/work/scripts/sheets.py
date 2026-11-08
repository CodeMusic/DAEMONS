"""T-532 finals: the review sheets. sheets.py [OUTDIR]"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import finals as FN
sys.path.insert(0, FN.R + "/gfx/drafts/t452/scripts")
OUT = FN.OUT
F = lambda z: ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", z)
PAPER = (236, 234, 226); INK = (30, 30, 34); GROUND = (205, 205, 172); PARTY = (98, 156, 131); RED = (170, 40, 40)
TINT = {"winter": (214, 226, 236), "spring": (220, 234, 212), "summer": (244, 232, 198), "autumn": (236, 214, 192)}
P = json.load(open(OUT + "/picks.json"))


def show(png, pal=None, h=64):
    im = Image.open(png)
    if pal: im.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    idx = np.array(im); a = np.array(im.convert("RGBA")); a[idx == 0, 3] = 0
    return Image.fromarray(a).crop((0, 0, im.width, h))


def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)


def art(n, s):
    """(front, back, icon, follower) RGBA images for a form; MUSAI's summer is the ROM's"""
    slot = FN.DAEMONS[n][0]; d = FN.G + slot
    if s == "summer" and n in FN.ROM_SUMMER:
        pal = FN.readpal(d + "/normal.pal")
        return (show(d + "/front.png", pal), show(d + "/back.png", pal), show(d + "/icon.png", None, 32),
                show(d + "/follower.png", None, 32), "ROM (stands)")
    k = "%s_%s" % (n, s); p = P[k]; b = "%s/reduced/%s_%d_" % (OUT, k, p["seed"])
    return (show(b + "front.png"), show(b + "back.png"), show("%s/reduced/%s_icon_%d.png" % (OUT, k, p["icon_seed"]), None, 32),
            show("%s/follower/%s_follower.png" % (OUT, k), None, 32), "seed %d / icon %d" % (p["seed"], p["icon_seed"]))


def rom(n):
    d = FN.G + FN.DAEMONS[n][0]; pal = FN.readpal(d + "/normal.pal")
    return show(d + "/front.png", pal), show(d + "/back.png", pal), show(d + "/icon.png", None, 32)


def species_sheet(n, od):
    import gbs
    slot, t, word, home, _, veh = FN.DAEMONS[n]
    sc = 3; CW = 64 * sc + 30; LW = 230; ROWS = [("FRONT", 64), ("BACK", 64), ("ICON", 32), ("FOLLOWER", 32)]
    RH = [64 * sc + 26, 64 * sc + 26, 32 * sc + 26, 32 * sc + 26]
    W = LW + 4 * CW + 40 + 64 * sc + 20; H = 110 + sum(RH) + 40
    sh = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 12), "T-532  %s -- the four seasonal forms, FINAL art (DRAFT until built; not in the ROM)" % n.upper(), fill=INK, font=F(19))
    d.rectangle((16, 44, 34, 62), fill=gbs.TYPE_COLOR[t], outline=INK)
    d.text((42, 44), "%s   %s   home season: %s" % (word, veh, home or "none (%s)" % ("it has not chosen" if n == "musai" else "all four are its")),
           fill=RED if home else INK, font=F(15))
    d.text((16, 68), "arm C (klein 4B + pixel LoRA), concept + ROM front as references; 64x64/16 colours in the type ramp; icons by icon3; "
           "followers 20x22 in the icon's palette. 3x.", fill=INK, font=F(12))
    for j, s in enumerate(FN.SEASONS):
        x = LW + j * CW
        d.rectangle((x, 90, x + CW - 10, 90 + sum(RH) + 14), fill=TINT[s])
        f, b, i, fo, lab = art(n, s)
        d.text((x + 8, 94), s.upper() + (" *home" if s == home else ""), fill=RED if s == home else INK, font=F(14))
        d.text((x + 8, 94 + sum(RH)), lab, fill=INK, font=F(11))
        y = 114
        for (row, h), im, rh in zip(ROWS, (f, b, i, fo), RH):
            bg = PARTY if h == 32 else GROUND
            sh.paste(on(im, bg, sc), (x + 8, y)); y += rh
    y = 114
    for (row, h), rh in zip(ROWS, RH):
        d.text((16, y + 10), row, fill=INK, font=F(15)); y += rh
    x0 = LW + 4 * CW + 20
    d.text((x0, 94), "ROM NOW", fill=INK, font=F(14))
    rf, rb, ri = rom(n)
    sh.paste(on(rf, GROUND, sc), (x0, 114)); sh.paste(on(rb, GROUND, sc), (x0, 114 + RH[0])); sh.paste(on(ri, PARTY, sc), (x0, 114 + RH[0] + RH[1]))
    d.text((16, H - 26), "Under the fable rule the vehicle is part of the body, never ridden. Daemons are said DAY-mons.", fill=INK, font=F(12))
    out = "%s/t532_%s_forms.png" % (od, n); sh.save(out); print(out, sh.size); return out


def battle_sheet(od):
    import armc
    homes = [(n, v[3]) for n, v in FN.DAEMONS.items() if v[3]]
    sh = Image.new("RGB", (16 + 2 * (480 + 24), 60 + len(homes) * (160 + 30) + 10 + 0), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 10), "T-532 home-season forms in battle -- real size (240x160, 1x) and 2x. Foe: the front; lead: the back. DRAFT.", fill=INK, font=F(14))
    sh = Image.new("RGB", (16 + 240 + 24 + 480 + 16, 50 + len(homes) * (320 + 30)), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 10), "T-532 home-season forms in battle: real size (240x160) and 2x. Foe = its front, lead = its back. DRAFT.", fill=INK, font=F(14))
    for i, (n, s) in enumerate(homes):
        f, b, *_ = art(n, s); y = 40 + i * 350
        bt = armc.battle(f, b)
        d.text((16, y), "%s  %s (home)" % (n.upper(), s), fill=INK, font=F(13))
        sh.paste(bt, (16, y + 20)); sh.paste(bt.resize((480, 320), Image.NEAREST), (16 + 240 + 24, y + 20))
    out = od + "/t532_home_forms_battle.png"; sh.save(out); print(out, sh.size); return out


def all_fronts(od):
    import gbs
    sc = 2; CW = 64 * sc + 24; RH = 64 * sc + 34; LW = 170
    sh = Image.new("RGB", (LW + 4 * CW + 16, 70 + 6 * RH + 20), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 10), "T-532  all 24 seasonal fronts of the MUSAI branch, FINAL art (2x). * = home season. DRAFT until built.", fill=INK, font=F(14))
    for j, s in enumerate(FN.SEASONS):
        x = LW + j * CW; d.rectangle((x, 34, x + CW - 8, 40 + 6 * RH), fill=TINT[s]); d.text((x + 6, 38), s.upper(), fill=INK, font=F(13))
    for i, (n, v) in enumerate(FN.DAEMONS.items()):
        y = 58 + i * RH
        d.text((16, y + 20), n.upper(), fill=INK, font=F(14)); d.rectangle((16, y + 44, 30, y + 58), fill=gbs.TYPE_COLOR[v[1]], outline=INK)
        d.text((36, y + 44), v[2], fill=INK, font=F(12)); d.text((16, y + 64), v[5], fill=INK, font=F(11))
        for j, s in enumerate(FN.SEASONS):
            f, *_, lab = art(n, s); x = LW + j * CW + 8
            sh.paste(on(f, GROUND, sc), (x, y + 4))
            d.text((x, y + 4 + 64 * sc + 2), (s + " *" if v[3] == s else "") + ("ROM" if "ROM" in lab else ""), fill=RED, font=F(11))
    out = od + "/t532_all_fronts.png"; sh.save(out); print(out, sh.size); return out


if __name__ == "__main__":
    od = sys.argv[1] if len(sys.argv) > 1 else OUT + "/sheets"; os.makedirs(od, exist_ok=True)
    for n in FN.DAEMONS: species_sheet(n, od)
    battle_sheet(od); all_fronts(od)
