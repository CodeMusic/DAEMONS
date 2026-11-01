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


if __name__ == "__main__":
    main()
