"""beforeafter.py OUT.png [BATTLE.png]: the redrawn T-532 forms, old finals beside new, as the ROM would get them --
front/back/icon through genmusaiseasons.final_files (gbasprite place_rich in the type ramp; the icon in the base's shared
icon palette), the follower as drawn. 1x and 2x. A battle mock for MASKMUSAI winter and SEEKMUSAI autumn, old and new."""
import contextlib, io, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = "/Users/christopherhicks/Projects/DAEMONS"
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.dirname(os.path.dirname(HERE)) + "/finals"
OLD = R + "/gfx/drafts/t532_musai_seasons/finals"
sys.path.insert(0, R + "/tools"); sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import genmusaiseasons as GM
import armc
#  the tool now gates finals on APPROVED_FINAL; for this sheet (memory only) every redrawn form is read as a final
GM.APPROVED_FINAL = set(GM.APPROVED_FINAL) | {(k.split('_')[0].upper(), k.split('_')[1]) for k in ['maskmusai_winter', 'maskmusai_spring', 'maskmusai_autumn', 'seekmusai_autumn', 'lensmusai_autumn', 'codemusai_winter', 'codemusai_autumn']}
F = lambda z: ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", z)
PAPER = (236, 234, 226); INK = (30, 30, 34); GROUND = (205, 205, 172); PARTY = (98, 156, 131); RED = (170, 40, 40)
KEYS = ["maskmusai_winter", "maskmusai_spring", "maskmusai_summer", "maskmusai_autumn", "seekmusai_autumn",
        "lensmusai_autumn", "codemusai_winter", "codemusai_autumn"]


def rgba(grid, pal):
    g = np.array(grid); p = np.array(list(pal) + [(0, 0, 0)] * 16)[:16].astype(np.uint8)
    a = np.zeros(g.shape + (4,), np.uint8); a[..., :3] = p[g]; a[..., 3] = np.where(g > 0, 255, 0)
    return Image.fromarray(a, "RGBA")


def art(folder, k):
    name, season = k.split("_")
    GM.FINALS = folder
    f = next((x for x in GM.forms() if x[0].lower() == name and x[5] == season), None)
    if f is None:   # summer: not a form id; reduce it the same way through the species' own ramp
        G = GM._G(); t = dict((b[0].lower(), b[4]) for b in GM.BRANCH)[name]
        fr, pal = G.place_rich("%s/%s_front.png" % (folder, k), G.TYPE_COLOR[t])
        bk, _ = G.place_rich("%s/%s_back.png" % (folder, k), G.TYPE_COLOR[t], shared=pal)
        ic, (pi, _e) = G.drawn_icon("%s/%s_icon.png" % (folder, k))
        out = (rgba(fr, pal), rgba(bk, pal), rgba(ic, G.icon_palettes()[pi]).crop((0, 0, 32, 32)))
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            ff = GM.final_files(f)
        fr, pal, _, _ = ff["front.png"][1]; bk = ff["back.png"][1][0]; ic, ipal, _, _ = ff["icon.png"][1]
        out = (rgba(fr, pal), rgba(bk, pal), rgba(ic, ipal).crop((0, 0, 32, 32)))
    fo = Image.open("%s/%s_follower.png" % (folder, k)); idx = np.array(fo); fo = fo.convert("RGBA"); a = np.array(fo); a[idx == 0, 3] = 0
    return out + (Image.fromarray(a),)


def on(im, bg, s):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width * s, im.height * s), Image.NEAREST)


def block(sh, d, x, y, ims, label):
    """front, back at 1x then 2x; icon and follower at 1x and 2x"""
    d.text((x, y), label, fill=RED if label == "NEW" else INK, font=F(13)); y += 18
    f, b, i, fo = ims; cx = x
    for im in (f, b):
        sh.paste(on(im, GROUND, 1), (cx, y)); sh.paste(on(im, GROUND, 2), (cx, y + 70)); cx += 136
    for im in (i, fo):
        sh.paste(on(im, PARTY, 1), (cx, y)); sh.paste(on(im, PARTY, 2), (cx, y + 70)); cx += 72
    return cx


def main(out, bout):
    BW = 2 * 136 + 2 * 72; RH = 18 + 70 + 128 + 24
    sh = Image.new("RGB", (220 + 2 * BW + 40, 60 + len(KEYS) * RH), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 10), "T-532 REDRAW -- the weak seasonal forms, old finals beside new (as the ROM gets them: type ramp, 16 colours)."
           " 1x above, 2x below. DRAFT.", fill=INK, font=F(14))
    d.text((16, 30), "front, back on the ground colour; icon and follower on the party green. Not in the ROM.", fill=INK, font=F(12))
    for r, k in enumerate(KEYS):
        y = 56 + r * RH
        d.text((16, y + 40), k.replace("_", "\n").upper(), fill=INK, font=F(15))
        block(sh, d, 220, y, art(OLD, k), "OLD")
        block(sh, d, 220 + BW + 30, y, art(NEW, k), "NEW")
    sh.save(out); print(out, sh.size)
    B = Image.new("RGB", (16 + 2 * (480 + 20), 40 + 2 * (340 + 20)), PAPER); d = ImageDraw.Draw(B)
    d.text((16, 10), "T-532 REDRAW in battle (2x of 240x160; foe = front, lead = back). Left OLD, right NEW. DRAFT.", fill=INK, font=F(14))
    for r, k in enumerate(("maskmusai_winter", "seekmusai_autumn")):
        for c, (lab, fol) in enumerate((("OLD", OLD), ("NEW", NEW))):
            f, b, *_ = art(fol, k); x = 16 + c * 500; y = 36 + r * 360
            d.text((x, y), "%s  %s (home)  %s" % (k.split("_")[0].upper(), k.split("_")[1], lab), fill=RED if lab == "NEW" else INK, font=F(13))
            B.paste(armc.battle(f, b).resize((480, 320), Image.NEAREST), (x, y + 18))
    B.save(bout); print(bout, B.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
