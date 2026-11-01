#!/usr/bin/env python3
"""C-267: four DRAFT app icons for the DAEMONS iOS app, and a contact sheet.

Run from anywhere with the pyenv Python (PIL + numpy):
    ~/.pyenv/versions/3.12.2/bin/python3 gfx/drafts/c267_icon/draw_icons.py
Reads the companion's exported art (never writes there). Every piece of pixel art
is scaled by an integer, nearest-neighbour; every icon is 1024x1024 opaque RGB.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ART = Path.home() / "Projects/daemons-companion/server/data/art"
CURRENT = Path.home() / "Projects/daemons-companion/app/assets/icon.png"
N = 1024

GREEN = ["#a0f8e8", "#40d8c0", "#009080", "#005048"]   # title.json greenRamp
RED, PURPLE, BLUE = "#C8405A", "#B0569E", "#4F6BD8"     # the hermetic pulse


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load(p):
    return Image.open(p).convert("RGBA")


def bbox_crop(im):
    return im.crop(im.getbbox())


def nn(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def paste_center(canvas, im, cx=N // 2, cy=N // 2):
    canvas.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))


def native(p):
    """Title art is exported at scale 2; undo it exactly."""
    a = np.array(load(p))
    assert (a[::2, ::2] == a[1::2, 1::2]).all()
    return Image.fromarray(a[::2, ::2])


def logo_letter(p, idx):
    """Letter idx of a native logo, cut at its empty columns."""
    im = native(p)
    op = np.array(im)[:, :, 3] > 0
    cols = op.any(0)
    runs, s = [], None
    for i, c in enumerate(list(cols) + [False]):
        if c and s is None:
            s = i
        if not c and s is not None:
            runs.append((s, i)); s = None
    x0, x1 = runs[idx]
    return bbox_crop(im.crop((x0, 0, x1, im.height)))


# 3x5 pixel digits, for the splash's 0s and 1s
DIG = {"0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"]}


def binary_field(grid, cell, colour, alpha, seed, avoid=None):
    """A faint rain of 0/1 glyphs on a grid; returns an RGBA layer."""
    rng = np.random.default_rng(seed)
    layer = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    px = cell // 5
    for gy in range(grid):
        for gx in range(grid):
            if rng.random() < 0.45:
                continue
            ch = "01"[rng.integers(2)]
            a = int(alpha * (0.4 + 0.6 * rng.random()))
            ox, oy = gx * cell + px, gy * cell + px // 2
            for r, row in enumerate(DIG[ch]):
                for c, bit in enumerate(row):
                    if bit == "1":
                        d.rectangle([ox + c * px, oy + r * px, ox + (c + 1) * px - 1, oy + (r + 1) * px - 1],
                                    fill=rgb(colour) + (a,))
    return layer


def flat(im):
    out = Image.new("RGB", im.size, (0, 0, 0))
    out.paste(im, mask=im.split()[3])
    return out


# ---------------------------------------------------------------- (a) monogram
def icon_a():
    """The title logo's D, recoloured into the splash green ramp, on dark."""
    d = logo_letter(ART / "title/logo_content.png", 0)
    a = np.array(d).astype(int)
    lum = a[:, :, :3].sum(2)
    op = a[:, :, 3] > 0
    levels = sorted(set(lum[op].tolist()))
    dark = [l for l in levels if l < 200]           # the logo's drop-shadow / outline
    body = [l for l in levels if l >= 200]
    out = np.zeros_like(a)
    for y, x in zip(*np.nonzero(op)):
        l = lum[y, x]
        if l in dark:
            c = rgb("#02201e")
        else:
            # brightest body level -> lightest green, darker -> deeper
            t = body.index(l) / max(1, len(body) - 1)
            c = rgb(GREEN[0]) if t > 0.75 else rgb(GREEN[1]) if t > 0.3 else rgb(GREEN[2])
        out[y, x] = c + (255,)
    d = Image.fromarray(out.astype(np.uint8))
    k = 700 // d.height
    icon_a.k = k
    big = nn(d, k)
    bg = Image.new("RGBA", (N, N), rgb("#071615") + (255,))
    bg.alpha_composite(binary_field(16, 64, GREEN[3], 150, 267))
    paste_center(bg, big, N // 2 + k // 2, N // 2)
    return flat(bg)


# ------------------------------------------------------- (b) sprite on a split
def icon_b():
    """MUSAI's front sprite on a CONTENT|CONTEXT split, the two logos' colours."""
    sp = bbox_crop(load(ART / "musai.png"))
    k = 760 // max(sp.size)
    big = nn(sp, k)
    bg = Image.new("RGBA", (N, N))
    d = ImageDraw.Draw(bg)
    d.rectangle([0, 0, N // 2 - 1, N], fill=rgb("#24497a") + (255,))    # CONTENT's blue, darkened
    d.rectangle([N // 2, 0, N, N], fill=rgb("#a8400c") + (255,))         # CONTEXT's D orange, darkened
    # a soft shadow block under the feet, pixel-stepped
    paste_center(bg, big, N // 2, N // 2 + 20)
    return flat(bg)


# --------------------------------------------------------- (c) the pulse mark
def icon_c():
    """Two discs, red and blue, overlapping in purple -- drawn on a 64 grid, x16."""
    g = 64
    yy, xx = np.mgrid[0:g, 0:g] + 0.5
    r = 17.5
    L = (xx - 24) ** 2 + (yy - 32) ** 2 <= r * r
    R = (xx - 40) ** 2 + (yy - 32) ** 2 <= r * r
    im = np.zeros((g, g, 3), np.uint8)
    im[:] = rgb("#120e1c")
    im[L] = rgb(RED)
    im[R] = rgb(BLUE)
    im[L & R] = rgb(PURPLE)
    # a one-pixel lighter rim on the lens, so it reads as the place they meet
    lens = L & R
    edge = lens & ~(np.roll(lens, 1, 0) & np.roll(lens, -1, 0) & np.roll(lens, 1, 1) & np.roll(lens, -1, 1))
    im[edge] = rgb("#e08cc8")
    return Image.fromarray(im).resize((N, N), Image.NEAREST)


# ------------------------------------------------------- (d) the two title daemons, spliced
def icon_d():
    """Half CODEMUSAI, half CAREMUSAI -- the pair who swap sides between the two
    editions' title screens -- joined at one seam, on a dark that is half each."""
    a = load(ART / "codemusai.png")
    b = load(ART / "caremusai.png")
    # each sprite cut at its own centre column, so the two heads meet at the seam
    def halves(im):
        x0, y0, x1, y1 = im.getbbox()
        c = (x0 + x1) // 2
        return im.crop((x0, 0, c, 64)), im.crop((c, 0, x1, 64))
    left, _ = halves(a)
    _, right = halves(b)
    sp = Image.new("RGBA", (left.width + right.width, 64))
    sp.alpha_composite(left, (0, 0))
    sp.alpha_composite(right, (left.width, 0))
    sp = bbox_crop(sp)
    k = 760 // max(sp.size)
    big = nn(sp, k)
    bg = Image.new("RGBA", (N, N))
    d = ImageDraw.Draw(bg)
    d.rectangle([0, 0, N // 2 - 1, N], fill=rgb("#141a2c") + (255,))
    d.rectangle([N // 2, 0, N, N], fill=rgb("#26142a") + (255,))
    paste_center(bg, big, N // 2, N // 2 + 16)
    return flat(bg)


# ---------------------------------------------------------------- the sheet
def rounded(im, size):
    """iOS-ish squircle preview: a rounded rect with ~22.37% radius."""
    small = im.resize((size, size), Image.LANCZOS if size < N else Image.NEAREST)
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=int(size * 4 * 0.2237), fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tile.paste(small, mask=m)
    return tile


def font(sz):
    for p in ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc", "/Library/Fonts/Arial.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def sheet(items, path):
    col_w = 560
    big = 512
    W, H = col_w * len(items) + 40, 900
    sh = Image.new("RGB", (W, H), rgb("#e9e6df"))
    d = ImageDraw.Draw(sh)
    f, fs = font(26), font(19)
    for i, (name, label, im) in enumerate(items):
        x = 20 + i * col_w + (col_w - big) // 2
        d.text((x, 18), name, fill=(20, 20, 20), font=f)
        sh.paste(im.resize((big, big), Image.LANCZOS), (x, 60))
        y = 60 + big + 24
        sh.paste(rounded(im, 180), (x, y), rounded(im, 180))
        sh.paste(rounded(im, 60), (x + 200, y + 60), rounded(im, 60))
        sh.paste(rounded(im, 60), (x + 280, y + 60), rounded(im, 60))
        sh.paste(rounded(im, 29), (x + 360, y + 75), rounded(im, 29))
        d.text((x + 200, y + 150), "180 . 60 . 60 . 29 . dark", fill=(90, 90, 90), font=fs)
        # dark-mode 60 px
        dk = Image.new("RGB", (100, 100), (20, 20, 22))
        dk.paste(rounded(im, 60), (20, 20), rounded(im, 60))
        sh.paste(dk, (x + 400, y + 40))
        # label, wrapped
        words, line, ly = label.split(), "", y + 200
        for w in words:
            if d.textlength(line + " " + w, font=fs) > big:
                d.text((x, ly), line.strip(), fill=(30, 30, 30), font=fs); ly += 26; line = ""
            line += " " + w
        d.text((x, ly), line.strip(), fill=(30, 30, 30), font=fs)
    sh.save(path)


def main():
    icons = {"a": icon_a(), "b": icon_b(), "c": icon_c(), "d": icon_d()}
    for k, im in icons.items():
        assert im.size == (N, N) and im.mode == "RGB"
        im.save(HERE / f"icon_{k}.png")
    cur = Image.open(CURRENT).convert("RGB")
    items = [
        ("current", "The icon today: a robot dog on a navy disc.", cur),
        ("A  monogram", f"The title logo's D, its own pixels x{icon_a.k}, in the splash's green ramp over faint 0s and 1s.", icons["a"]),
        ("B  split", "MUSAI's front sprite x12 on a split: CONTENT's blue left, CONTEXT's orange right.", icons["b"]),
        ("C  pulse", "Red and blue discs meeting in purple, drawn on a 64 grid and scaled x16.", icons["c"]),
        ("D  seam", "Half CODEMUSAI, half CAREMUSAI -- the two who trade places on the two title screens -- one body, one seam.", icons["d"]),
    ]
    sheet(items, HERE / "sheet.png")


# ================================================================ round 2
# The user on the sheet (2026-11-01): A's background, with the musical notes
# coming up; the daemon from B, or the robot dog from the current icon; and
# red and blue notes that cross in purple.

NOTE_COLOURS = ["#d83078", "#f87840", "#f8d848", "#78d860", "#48a8f8", "#a870f8", "#f8a8c8"]  # title.json


def title_notes():
    """The title screen's twelve 16x16 eighth notes (play_notes.png), as RGBA cells."""
    sh = load(ART / "play_notes.png")
    return [sh.crop((0, 16 * i, 16, 16 * i + 16)) for i in range(sh.height // 16)]


def note_mask():
    a = np.array(title_notes()[0])
    return a[:, :, 3] > 0, a[:, :, :3].astype(int).sum(2)


def rising_field(seed=11):
    """A's teal field of faint 0s and 1s, with the title's notes rising through it:
    each note faint, in a noteColour, with a short dotted trail below it."""
    bg = Image.new("RGBA", (N, N), rgb("#071615") + (255,))
    bg.alpha_composite(binary_field(16, 64, GREEN[3], 150, 267))
    rng = np.random.default_rng(seed)
    m, _ = note_mask()
    k = 4
    spots = [(120, 210), (300, 90), (520, 170), (760, 110), (900, 300), (160, 520), (880, 560),
             (110, 820), (330, 700), (700, 760), (520, 900), (860, 860)]
    layer = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, (x, y) in enumerate(spots):
        c = rgb(NOTE_COLOURS[i % len(NOTE_COLOURS)])
        a = int(70 + 40 * rng.random())
        flip = rng.random() < 0.5
        cell = np.fliplr(m) if flip else m
        for yy, xx in zip(*np.nonzero(cell)):
            d.rectangle([x + xx * k, y + yy * k, x + xx * k + k - 1, y + yy * k + k - 1], fill=c + (a,))
        # the trail: three dots below, fading -- the note is going up
        hx = x + (12 if flip else 3) * k
        for t in range(3):
            ty = y + 16 * k + 10 + t * 22
            d.rectangle([hx, ty, hx + k * 2 - 1, ty + k * 2 - 1], fill=c + (int(a * (0.6 - 0.18 * t)),))
    bg.alpha_composite(layer)
    return bg


def pulse_notes(k):
    """Two of the title's eighth notes facing each other, red and blue; where
    they cross, purple. Drawn on the note's own 16-pixel grid, scaled x k."""
    m, lum = note_mask()
    W, o = 25, 9                             # red at 0, blue mirrored at +9: each flag crosses the other stem
    red = np.zeros((16, W), bool); blue = np.zeros((16, W), bool)
    red[:, 0:16] = m
    blue[:, o:o + 16] = np.fliplr(m)
    lred = np.zeros((16, W), int); lblue = np.zeros((16, W), int)
    lred[:, 0:16] = lum; lblue[:, o:o + 16] = np.fliplr(lum)
    out = np.zeros((16, W, 4), np.uint8)

    def shade(base, l):
        r, g, b = rgb(base)
        f = 0.55 if l < 200 else 1.0 if l < 520 else 1.25    # the glyph's own outline / body / shine
        return tuple(min(255, int(v * f)) for v in (r, g, b)) + (255,)
    for y in range(16):
        for x in range(W):
            if red[y, x] and blue[y, x]:
                out[y, x] = shade(PURPLE, min(lred[y, x], lblue[y, x]) if min(lred[y, x], lblue[y, x]) < 200 else 400)
            elif red[y, x]:
                out[y, x] = shade(RED, lred[y, x])
            elif blue[y, x]:
                out[y, x] = shade(BLUE, lblue[y, x])
    return nn(bbox_crop(Image.fromarray(out)), k)


def current_dog():
    """The robot dog on the current icon (drawn when it was ROVERCUB, 2026-10-04),
    recovered from its 13-pixel grid; the two blues of its disc and field dropped."""
    a = np.array(Image.open(CURRENT).convert("RGB"))
    s = a[np.ix_(np.arange(4 + 6, N, 13), np.arange(5 + 6, N, 13))]
    rgba = np.dstack([s, np.full(s.shape[:2], 255, np.uint8)])
    for c in [(20, 38, 64), (32, 64, 106)]:
        rgba[(s == c).all(2)] = 0
    return bbox_crop(Image.fromarray(rgba))


def daemon_on_field(sp, target=560, notes_k=16, notes_y=225, dy=125):
    bg = rising_field()
    notes = pulse_notes(notes_k)
    paste_center(bg, notes, N // 2, notes_y)
    big = nn(sp, max(1, target // max(sp.size)))
    paste_center(bg, big, N // 2, N // 2 + dy)
    return flat(bg)


def icon_e():
    return daemon_on_field(bbox_crop(load(ART / "musai.png")))


def icon_f():
    return daemon_on_field(current_dog(), target=600, dy=140)


def icon_g():
    return daemon_on_field(bbox_crop(load(ART / "codemusai.png")))


def main2():
    icons = {"e": icon_e(), "f": icon_f(), "g": icon_g()}
    for k, im in icons.items():
        assert im.size == (N, N) and im.mode == "RGB"
        im.save(HERE / f"icon_{k}.png")
    items = [
        ("A  monogram", "Round 1's A, for comparison.", Image.open(HERE / "icon_a.png").convert("RGB")),
        ("E  MUSAI", "B's daemon (MUSAI) under red and blue notes crossing in purple; the title's notes rising through A's field.", icons["e"]),
        ("F  the dog", "The current icon's robot dog (ROVERCUB as drawn 2026-10-04) on the same field and notes.", icons["f"]),
        ("G  CODEMUSAI", "CODEMUSAI, the name the user gave, on the same field and notes.", icons["g"]),
    ]
    sheet(items, HERE / "sheet2.png")


# ================================================================ round 3
# The user (2026-11-01): the crossing notes look like an M -- so behind the
# daemon, the whole title in A's letters and green, with the notes as its M.

def green_logo():
    """The native CONTENT logo (all capitals, DAEMONS), recoloured as A's D was."""
    a = np.array(native(ART / "title/logo_content.png")).astype(int)
    lum = a[:, :, :3].sum(2)
    op = a[:, :, 3] > 0
    body = sorted(set(lum[op & (lum >= 200)].tolist()))
    out = np.zeros_like(a)
    for y, x in zip(*np.nonzero(op)):
        l = lum[y, x]
        if l < 200:
            c = rgb("#02201e")
        else:
            t = body.index(l) / max(1, len(body) - 1)
            c = rgb(GREEN[0]) if t > 0.75 else rgb(GREEN[1]) if t > 0.3 else rgb(GREEN[2])
        out[y, x] = c + (255,)
    return Image.fromarray(out.astype(np.uint8))


def letter_runs(im):
    cols = np.array(im)[:, :, 3].any(0)
    runs, s = [], None
    for i, c in enumerate(list(cols) + [False]):
        if c and s is None:
            s = i
        if not c and s is not None:
            runs.append((s, i)); s = None
    return runs


def logo_parts():
    """(DAE, ONS) cut from the logo either side of its M, at native scale."""
    g = green_logo()
    r = letter_runs(g)                      # D A E M O N S
    return g.crop((0, 0, r[2][1], g.height)), g.crop((r[4][0], 0, g.width, g.height))


def word_with_notes(k, nk, gap):
    """D A E <notes> O N S on one line: letters x k, notes x nk, centred on the letters."""
    dae, ons = logo_parts()
    dae, ons = nn(dae, k), nn(ons, k)
    notes = pulse_notes(nk)
    h = dae.height
    w = dae.width + gap + notes.width + gap + ons.width
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.alpha_composite(dae, (0, 0))
    im.alpha_composite(notes, (dae.width + gap, (h - notes.height) // 2 - k * 2))
    im.alpha_composite(ons, (dae.width + gap + notes.width + gap, 0))
    return im


def word_behind(sp, target, dy):
    bg = rising_field()
    word = word_with_notes(3, 9, 9)          # 3 x the logo: ~750 px wide, inside the safe area
    paste_center(bg, word, N // 2, 330)
    big = nn(sp, max(1, target // max(sp.size)))
    paste_center(bg, big, N // 2, N // 2 + dy)
    return flat(bg)


def icon_h():
    return word_behind(bbox_crop(load(ART / "musai.png")), 520, 115)


def icon_i():
    return word_behind(current_dog(), 560, 120)


def icon_j():
    """The word alone, large enough to read: DAE over <notes>ONS, letters x5."""
    bg = rising_field()
    dae, ons = logo_parts()
    k = 5
    dae, ons = nn(dae, k), nn(ons, k)
    notes = pulse_notes(15)
    gap = 15
    line2 = Image.new("RGBA", (notes.width + gap + ons.width, ons.height), (0, 0, 0, 0))
    line2.alpha_composite(notes, (0, (ons.height - notes.height) // 2 - k * 2))
    line2.alpha_composite(ons, (notes.width + gap, 0))
    lead = 30
    top = (N - (dae.height + lead + line2.height)) // 2
    x2 = (N - line2.width) // 2
    bg.alpha_composite(line2, (x2, top + dae.height + lead))
    bg.alpha_composite(dae, (x2, top))          # flush left with the line below
    return flat(bg)


def main3():
    icons = {"h": icon_h(), "i": icon_i(), "j": icon_j()}
    for k, im in icons.items():
        assert im.size == (N, N) and im.mode == "RGB"
        im.save(HERE / f"icon_{k}.png")
    old = {k: Image.open(HERE / f"icon_{k}.png").convert("RGB") for k in "ef"}
    items = [
        ("E  MUSAI", "Round 2's E, for comparison.", old["e"]),
        ("F  the dog", "Round 2's F, for comparison.", old["f"]),
        ("H  MUSAI + title", "DAEMONS in the logo's letters x3 and A's green, the crossing notes as its M; MUSAI in front.", icons["h"]),
        ("I  dog + title", "The same title behind the current icon's robot dog.", icons["i"]),
        ("J  the title", "No daemon: DAE over (notes)ONS, letters x5, so the word still reads small.", icons["j"]),
    ]
    sheet(items, HERE / "sheet3.png")


if __name__ == "__main__":
    main()
    main2()
    main3()
