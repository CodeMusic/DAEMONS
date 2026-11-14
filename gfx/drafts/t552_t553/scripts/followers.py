"""T-552/T-553 followers: each picked front (the ski-feet winters) reduced to T-464's follower size -- at most 20 tall and
22 wide, its lowest row on row 28 of a 32x32 frame -- by T-534's follower reduction (draw.py's mean-colour reduce, accents
kept, despeckled, light ground edges outlined), in the front's own palette. The vehicles now live in the anatomy, so no
vehicle is drawn over them. Writes followers/<key>_follower.png (RGBA) and a sheet on grass."""
import json, os, sys
from PIL import Image
R = "/Users/christopherhicks/Projects/DAEMONS"; D = R + "/gfx/drafts/t552_t553/"
sys.path.insert(0, R + "/gfx/drafts/t532_musai_seasons/followers/scripts")
import draw as F
P = json.load(open(D + "reduced/picks.json")); os.makedirs(D + "followers", exist_ok=True)
keys = list(P); bad = []
S = 6; big = Image.new("RGBA", (9 * (32 * S + 8), 3 * (32 * S + 8)), (112, 168, 104, 255))
for i, key in enumerate(keys):
    f = D + "reduced/%s%s.png" % (key, "_skifeet" if key in ("maskmusai_winter", "codemusai_winter") else "")
    im = Image.open(f); pal = [tuple(im.getpalette()[k * 3:k * 3 + 3]) for k in range(16)]; px = im.load()
    g = F.unstreak([[px[x, y] for x in range(64)] for y in range(64)])
    F.LIGHT = set(F.roles(pal)[:1])
    out = F.outline(F.place(F.reduce(g, pal)))
    w, h, low = F.bounds(out)
    if w > F.MAX_W or h > F.MAX_H or low != F.GROUND: bad.append((key, w, h, low))
    rgba = F.to_rgba(out, pal); rgba.save(D + "followers/%s_follower.png" % key)
    big.alpha_composite(rgba.resize((32 * S, 32 * S), Image.NEAREST), ((i % 9) * (32 * S + 8), (i // 9) * (32 * S + 8)))
big.save(D + "followers/sheet.png"); print("bad", bad)
