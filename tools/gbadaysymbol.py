#!/usr/bin/env python3
"""T-591: a day's symbol on each dream in the game's DREAM LOG (T-531, bible 9.21) -- the GBA half of C-407 and C-412.

    ~/.pyenv/shims/python3 tools/gbadaysymbol.py [--write] [--sheet OUT.png]

Draws the seven day symbols at 32x32 for the NOTEBOOK's dream pages, each in seven versions, one for every centre a
dream can be about (the user, 2026-11-18, by multiple choice: "B: which centre"): ring and horizon, the virtue's mark
above the line and its shadow dashed below, the centre's petals as ticks round the ring -- the paths approved on
2026-11-08 ("Keep all seven"), read from tools/gendaysymbol.py's MARKS so the game and the companion share one drawing
-- and through the ring a spine of seven dots, root at the foot and crown at the top (24 units below the line to 24
above, a step of 8, as the companion's), with the dream's own centre lit, larger, in the day's colour.

Pixel-drawn, not scaled down: at 32 pixels an anti-aliased ring breaks into dashes. Four colours: 0 clear, 1 ink,
2 the day's colour, 3 the day's colour faint. The engine (book_reader.c) sets 1 to the NOTEBOOK's ink and 2 and 3 from
the day's CHECKPOINT trim (data/day_trims.h) at the moment the page opens, so one sheet serves all seven days.

Writes, in engineGba:
  graphics/daemons/day_symbol.png  -- 49 frames, 32 wide, frame = day * 7 + centre (Sunday first; root first)
  src/data/day_symbol.h            -- the sheet's INCBIN, and each dream's centre by its save slot (flag minus
                                      FLAG_DREAM_LOG_CAIRN): 0xFF where the dream names none, so the day's own is lit.

A dream names its centre with an optional "centre" in docs/dream_log.json, docs/attendant_dreams.json or
docs/its_dreams.json: one of root, sacral, solar plexus, heart, throat, third eye, crown. None does yet; which centre a
dream is about is a writing choice, the user's. Without --write it reports what it would write.
"""
import argparse, json, math, os, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PNG = os.path.join(GBA, "graphics", "daemons", "day_symbol.png")
HDR = os.path.join(GBA, "src", "data", "day_symbol.h")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
argv, sys.argv = sys.argv, [sys.argv[0]]
import gendaysymbol as G   # noqa: E402  (the approved paths, and its path reader)
sys.argv = argv

N = 32                       # the frame
S = 11.5 / 30                # pixels per unit: the ring (30 units) at 11.5 px, the third eye's ticks (40) inside 32
C = 15.5                     # the centre, between pixels 15 and 16
CENTRES = ["root", "sacral", "solar plexus", "heart", "throat", "third eye", "crown"]
SPINE = [round(C + (24 - 8 * k) * S) for k in range(7)]   # root (24 below the line) to crown (24 above)
SPINE_X = 16
SLOTS = 64                   # FLAG_DREAM_LOG_CAIRN .. +0x3F: YOUR 0-20, HER 21-44, ITS 48-63
ITS_FIRST = 48               # FLAG_ITS_DREAM_GRASS - FLAG_DREAM_LOG_CAIRN
PALETTE = [(255, 0, 255), (28, 27, 26), (136, 51, 51), (198, 160, 150)] + [(0, 0, 0)] * 12   # 2, 3: set per day


def P(x, y):
    return (C + x * S, C + y * S)


def frame(day, centre):
    """One 32x32 frame, as colour indices."""
    _, petals, d = G.MARKS[day]
    im = Image.new("P", (N, N), 0)
    dr = ImageDraw.Draw(im)
    dr.line([P(-24, 0), P(24, 0)], fill=3, width=1)                                    # the horizon, faint
    for pts, closed in G.subpaths(d):                                                  # the shadow, dashed, faint
        pts = [(x, -y) for x, y in pts] + ([(pts[0][0], -pts[0][1])] if closed else [])
        for seg in G.dashed(pts, 5, 4):
            if len(seg) > 1:
                dr.line([P(*p) for p in seg], fill=3, width=1)
    for rad in ([30, 36] if petals == 0 else [30]):                                   # the ring, in ink
        r = rad * S
        dr.ellipse((C - r, C - r, C + r, C + r), outline=1, width=1)
    for j in range(petals):                                                            # its petals
        a = j * math.pi if petals == 2 else 2 * math.pi * j / petals - math.pi / 2
        out = 30 + (10 if petals == 2 else 6)
        dr.line([P(math.cos(a) * 30, math.sin(a) * 30), P(math.cos(a) * out, math.sin(a) * out)],
                fill=1, width=2 if petals == 2 else 1)
    for pts, closed in G.subpaths(d):                                                  # the virtue's mark
        if closed:
            dr.polygon([P(*p) for p in pts], fill=2)
        dr.line([P(*p) for p in pts + ([pts[0]] if closed else [])], fill=2, width=2)
    for k, y in enumerate(SPINE):                                                      # the spine, over all of it
        if k != centre:
            dr.point((SPINE_X, y), fill=1)
    y = SPINE[centre]                                                                  # the dream's centre, lit
    dr.rectangle((SPINE_X - 2, y - 2, SPINE_X + 2, y + 2), fill=1)
    dr.rectangle((SPINE_X - 1, y - 1, SPINE_X + 1, y + 1), fill=2)
    return im


def sheet():
    im = Image.new("P", (N, N * 49), 0)
    for day in range(7):
        for centre in range(7):
            im.paste(frame(day, centre), (0, (day * 7 + centre) * N))
    im.putpalette([c for rgb in PALETTE for c in rgb])
    return im


def centres():
    """Each dream's named centre by save slot, 0xFF where it names none."""
    out = [0xFF] * SLOTS
    named = []
    log = json.load(open(os.path.join(ROOT, "docs", "dream_log.json")))["dreams"]
    her = list(json.load(open(os.path.join(ROOT, "docs", "attendant_dreams.json")))["steps"].values())
    its = json.load(open(os.path.join(ROOT, "docs", "its_dreams.json")))["dreams"]
    assert len(log) == 21 and len(her) == 24 and len(its) == 16, (len(log), len(her), len(its))
    for base, items in ((0, log), (21, her), (ITS_FIRST, its)):
        for i, dream in enumerate(items):
            c = dream.get("centre")
            if c is None:
                continue
            if c.lower() not in CENTRES:
                sys.exit(f"gbadaysymbol: {dream.get('title', dream.get('key'))}: centre {c!r} is not one of {CENTRES}")
            out[base + i] = CENTRES.index(c.lower())
            named.append((dream.get("title", ""), c))
    return out, named


def header(table):
    rows = []
    for i in range(0, SLOTS, 16):
        rows.append("    " + ", ".join(f"0x{v:02X}" for v in table[i:i + 16]) + ",")
    return (
        "// Generated by DAEMONS tools/gbadaysymbol.py -- do not edit. T-591 (T-531, bible 9.21): the day's symbol on a dream.\n"
        "// 49 frames of 32x32, frame = day * 7 + centre (Sunday first; root, sacral, solar plexus, heart, throat,\n"
        "// third eye, crown). Colours: 1 ink, 2 the day's, 3 the day's faint -- set when the page opens.\n"
        "#define DAY_SYMBOL_FRAME_SIZE (32 * 32 / 2)\n"
        "static const u32 sDaySymbol_Gfx[] = INCBIN_U32(\"graphics/daemons/day_symbol.4bpp\");\n"
        "\n"
        "// Each dream's centre by save slot (its flag minus FLAG_DREAM_LOG_CAIRN); 0xFF: it names none, so the day's own.\n"
        f"static const u8 sDreamCentres[{SLOTS}] = {{\n" + "\n".join(rows) + "\n};\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sheet", help="a review sheet: every frame in each day's own colours, four times size")
    a = ap.parse_args()
    im = sheet()
    table, named = centres()
    text = header(table)
    changed = []
    old = Image.open(PNG) if os.path.exists(PNG) else None
    if old is None or old.mode != "P" or old.tobytes() != im.tobytes() or old.getpalette()[:48] != im.getpalette()[:48]:
        changed.append(PNG)
    if not os.path.exists(HDR) or open(HDR).read() != text:
        changed.append(HDR)
    if a.write:
        os.makedirs(os.path.dirname(PNG), exist_ok=True)
        im.save(PNG)
        with open(HDR, "w") as f:
            f.write(text)
    for p in changed:
        print(("wrote " if a.write else "would write ") + os.path.relpath(p, ROOT))
    print(f"gbadaysymbol: 49 frames; {len(named)} of 61 dreams name a centre" + (": " + ", ".join(f"{t} {c}" for t, c in named) if named else " (the day's own is lit)"))
    if a.sheet:
        week = json.load(open(G.WEEK))["days"]
        paper, ink = (244, 238, 222), PALETTE[1]
        out = Image.new("RGB", (7 * 36 * 4 + 8, 7 * 36 * 4 + 8), (200, 200, 200))
        for day in range(7):
            col = G.hexrgb(week[day]["colour"])
            faint = tuple(int(c * 0.45 + p * 0.55) for c, p in zip(col, paper))
            pal = [paper, ink, col, faint]
            for centre in range(7):
                f = frame(day, centre)
                rgb = Image.new("RGB", (N, N))
                rgb.putdata([pal[v] for v in f.getdata()])
                out.paste(rgb.resize((N * 4, N * 4), Image.NEAREST), (centre * 36 * 4 + 8, day * 36 * 4 + 8))
        out.save(a.sheet)
        print("sheet " + a.sheet)


if __name__ == "__main__":
    main()
