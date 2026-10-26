"""T-452 round two, by hand (the user, 2026-10-26): the two keys no draft drew, and OUTLIER's ears.

    hand_r2.py      writes gfx/drafts/t452/e/hand/{fork,predictor}_{front,back,icon}.png and outlier_back.png

FORK       a split tail -- a short stalk that forks into two prongs, one up and one straight out -- drawn on the back
           in place of the round puff, on the front poking out from behind the body (painted only where the front is
           empty, so the body stays in front of it), and on the icon at its right side.
PREDICTOR  a horn on its brow in place of the tuft: tapering from three cells to one, banded like a spiral; seen
           from behind it stands above the head between the ears; on the icon between the ears.
OUTLIER    the back's two pointed ears shaved off and the head given a round dome to match the one-eyed front, which
           has none. The pale ground strip under its feet and the pale gap between its legs (the ground showing
           through) were taken off too, as ROVERCUB's ellipse was (round2.unground).
GROUNDS    three more drafts stood on a baked ground (seen on the built sheet, 2026-10-26): SCHEDULER's front on a grey
           ellipse and BRANCH's back on a pale one -- taken off by round2.unground -- and OVERRUN's back on an orange
           strip (too saturated for unground's flood): its rows below the feet cleared, the soles kept.

Fronts and backs are drawn in the clean drafts' own greys (gbasprite.place_rich turns value into the type's ramp);
the icons in the indices icon3 chose for them (picks.json's icon3 ramp) and 15 for the outline, frame 2 redrawn
from frame 1 one row lower (the bob)."""
import os, json
import numpy as np
from PIL import Image
T = "/Users/christopherhicks/Projects/DAEMONS/gfx/drafts/t452"; E = T + "/e"; H = E + "/hand"
os.makedirs(H, exist_ok=True)
INK = (16, 16, 20, 255)
L, M, D = (238, 238, 240, 255), (186, 186, 192, 255), (124, 124, 134, 255)
TL, TM, TD = (196, 200, 208, 255), (150, 154, 164, 255), (110, 114, 124, 255)   # the tail in the body's own greys
K = {"#": INK, "L": L, "M": M, "D": D, "l": TL, "m": TM, "d": TD}

def stamp(a, x0, y0, rows, behind=False):
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == ".": continue
            y, x = y0 + dy, x0 + dx
            if behind and a[y, x, 3] > 127: continue
            a[y, x] = K[ch]

TAIL = ["....#....#...",          # a Y: two prongs, then the stalk down to the body
        "...#l#..#l#..",
        "...#l#..#l#..",
        "...#lm##lm#..",
        "....#lmlm#...",
        ".....#lm#....",
        "....#lm#.....",
        "...#lm#......",
        "..#lm#.......",
        ".#lm#........",
        "#lm#.........",
        "#md#.........",
        "####........."]

def fork():
    b = np.array(Image.open(E + "/clean/fork_back.png").convert("RGBA"))
    b[49:58, 44:] = 0                                  # the round puff off
    for y in range(49, 57):
        if b[y, 43, 3] > 127: b[y, 43] = INK
    stamp(b, 43, 41, TAIL, behind=True)
    Image.fromarray(b).save(H + "/fork_back.png")
    f = np.array(Image.open(E + "/clean/fork_front.png").convert("RGBA"))
    stamp(f, 42, 42, TAIL, behind=True)
    Image.fromarray(f).save(H + "/fork_front.png")

def icon_edit(n, cells):
    im = Image.open(E + "/reduced/%s_icon.png" % n); g = np.array(im)
    for (x, y), v in cells.items():
        if v[1] and g[y, x] != 0: continue             # behind: only where empty
        g[y, x] = v[0]
    g[32:] = 0; g[33:64] = g[0:31]                     # frame 2: frame 1 one row lower
    out = Image.fromarray(g.astype(np.uint8), "P"); out.putpalette(im.getpalette()); out.save(H + "/%s_icon.png" % n)

def ramp(n):
    return json.load(open(E + "/picks.json"))[n]["measured"]["icon3"]["ramp"]

def fork_icon():
    dk, md, lt = ramp("fork")
    rows = {19: ".#.#.", 20: "#L#L#", 21: "#LLL#", 22: ".#L#.", 23: "#L#..", 24: "L#...", 25: "#...."}
    c = {}
    for y, r in rows.items():
        for i, ch in enumerate(r):
            if ch == ".": continue
            c[(25 + i, y)] = ({"#": 15, "L": lt}[ch], True)
    icon_edit("fork", c)

HORN = {11: (32, "#"), 12: (31, "#L#"), 13: (31, "#L#"), 14: (31, "#D#"), 15: (31, "#L#"), 16: (30, "#LL#"),
        17: (30, "#DL#"), 18: (30, "#LM#"), 19: (30, "#LD#"), 20: (29, "#LLM#"), 21: (29, "#DLM#"), 22: (29, "#LLD#")}

def predictor():
    f = np.array(Image.open(E + "/clean/predictor_front.png").convert("RGBA"))
    f[11:22, 27:37] = 0                                # the tuft off
    f[22, 33:35] = INK
    for y, (x0, r) in HORN.items(): stamp(f, x0, y, [r])
    Image.fromarray(f).save(H + "/predictor_front.png")
    b = np.array(Image.open(E + "/clean/predictor_back.png").convert("RGBA"))
    back = {15: (33, ".#"), 16: (32, "#M#"), 17: (32, "#M#"), 18: (32, "#MD#"), 19: (32, "#MD#"), 20: (32, "#MD#"),
            21: (32, "#MD#"), 22: (32, "#MD#")}
    for y, (x0, r) in back.items(): stamp(b, x0, y, [r], behind=True)
    Image.fromarray(b).save(H + "/predictor_back.png")
    dk, md, lt = ramp("predictor")
    rows = {8: (15, "f"), 9: (14, "fLf"), 10: (14, "fLf"), 11: (14, "fMf"), 12: (13, "fLLf"), 13: (13, "fLMf"),
            14: (13, "fLLf"), 15: (14, "LL")}
    c = {}
    for y, (x0, r) in rows.items():
        for i, ch in enumerate(r): c[(x0 + i, y)] = ({"f": 15, "L": lt, "M": md}[ch], False)
    icon_edit("predictor", c)

def outlier():
    a = np.array(Image.open(E + "/clean/outlier_back.png").convert("RGBA"))
    head = tuple(int(v) for v in a[20, 30])            # the head's own mid grey
    hi = tuple(int(v) for v in a[19, 25])              # and its lighter grey
    dome = {11: (29, 35), 12: (26, 38), 13: (24, 40), 14: (23, 41), 15: (22, 42), 16: (22, 42), 17: (22, 43)}
    a[:11] = 0
    for y, (x0, x1) in dome.items():
        a[y, :x0] = 0; a[y, x1 + 1:] = 0
        for x in range(x0 + 1, x1):
            Lv = 0.299 * a[y, x, 0] + 0.587 * a[y, x, 1] + 0.114 * a[y, x, 2]
            if a[y, x, 3] < 128 or Lv < 175: a[y, x] = hi if (y < 15 and x < 30) else head
        a[y, x0] = INK; a[y, x1] = INK
    a[11, 29:36] = INK
    op = a[..., 3] > 127                               # the dome's edge: any cell with empty above or beside it
    for y in range(11, 18):
        for x in range(1, 63):
            if op[y, x] and (not op[y - 1, x] or not op[y, x - 1] or not op[y, x + 1]): a[y, x] = INK
    a[55:] = 0                                         # the ground strip
    a[52:55, 28:36] = 0                                # the ground between the legs
    Image.fromarray(a).save(H + "/outlier_back.png")

def grounds():
    import round2
    for n, k in (("scheduler", "front"), ("branch", "back")):
        out = H + f"/{n}_{k}.png"; gone = round2.unground(E + f"/clean/{n}_{k}.png", out)
        a = np.array(Image.open(out).convert("RGBA")); op = a[..., 3] > 127
        for y, x in zip(*np.where(op)):                # a lone cell of the ellipse's own outline
            if not any(0 <= y + dy < 64 and 0 <= x + dx < 64 and op[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx):
                a[y, x] = 0
        Image.fromarray(a).save(out); print(n, k, gone, "ground cells off")
    a = np.array(Image.open(E + "/clean/overrun_back.png").convert("RGBA"))
    sole = a[56].copy(); a[56:] = 0
    for x in range(15, 29):
        if sole[x, 3] > 127 and sole[x, :3].sum() < 180: a[56, x] = sole[x]
    Image.fromarray(a).save(H + "/overrun_back.png")

if __name__ == "__main__":
    fork(); fork_icon(); predictor(); outlier(); grounds()
    print("written", sorted(os.listdir(H)))
