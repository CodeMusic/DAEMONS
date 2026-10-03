#!/usr/bin/env python3
"""THE NAME SCREEN, in our own look (T-363; the user chose mock-up A, "the terminal", 2026-10-03).

    python3 tools/gbanaming.py            # report what would change
    python3 tools/gbanaming.py --write    # graphics/naming_screen/: seven palettes, menu.png's tiles, background.bin

WHY. The keyboard where a player first types their name is the second screen of the game, and it was vanilla's:
cream stripes, a sky-blue keyboard, a blue banner. It now goes on from the title screen it follows -- the same night
navy, the title's binary drifting behind it, pale keys on ink, CAREMUSAI's pink for the cursor. Nothing is written on
it that was not there; the words are vanilla's (YOUR NAME?, the controls).

WHAT DRAWS WHAT (measured in the theatre, palette RAM on the screen itself):
    BG row 0      menu.pal -- the background tiles and the name box's frame; also the PC icon's sprite palette
    BG rows 1-3   page_swap_upper/lower/others.pal -- the keyboard panel's frame, one tint a page (and the page button,
                  the underscores and the input arrow as sprites)
    BG row 4      buttons.pal -- BACK and OK;  row 5  cursor.pal
    BG row 10     keyboard.pal -- the keys (fill 13, 14 or 15 by page) and the name box (the font's own 1, 2, 3)
    BG row 11     the banner: src/naming_screen.c loads its own row now, not the shared text-window palette
The keys used to print white (1) with a grey shadow (2), which the name box also fills and prints with; they print
in 11 and 12 now (src/naming_screen.c, sTextColorStruct), so the keys can be pale on ink while the box is a dark field.

THE BACKGROUND was one striped tile, #2, repeated. It is navy now, and the field behind the boxes is a 4x4 block of
tiles in the sheet's unused slots 30..45, a scatter of small 0s and 1s, repeated every 32 pixels.
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = os.path.join(ROOT, "engineGba/graphics/naming_screen")
WRITE = "--write" in sys.argv

NAVY, NIGHT, INK, SLATE = (24, 40, 80), (16, 24, 48), (16, 24, 48), (24, 32, 64)
PALE, STEEL1, STEEL2, STEEL3, DARK = (208, 224, 248), (56, 80, 136), (88, 120, 176), (120, 152, 208), (8, 8, 24)
DIGIT, DIGIT2 = (40, 56, 112), (56, 80, 144)

#  index -> colour, by file; an index not named keeps vanilla's
PALETTES = {
    "menu": {0: NAVY, 1: SLATE, 2: DARK, 3: STEEL1, 4: STEEL2, 5: STEEL3, 6: (152, 176, 232),
             7: (64, 104, 168), 8: (96, 136, 200), 9: (128, 168, 224),
             12: NAVY, 13: DIGIT, 14: DIGIT2, 15: NIGHT},
    "page_swap_upper":  {2: PALE, 3: (64, 88, 152), 11: (8, 16, 32), 12: (24, 40, 80), 13: INK, 14: (64, 96, 152), 15: (112, 152, 216)},
    "page_swap_lower":  {2: PALE, 3: (64, 88, 152), 11: (16, 8, 32), 12: (40, 24, 80), 13: (24, 16, 48), 14: (88, 64, 160), 15: (152, 120, 224)},
    "page_swap_others": {2: PALE, 3: (64, 88, 152), 11: (8, 24, 24), 12: (16, 48, 56), 13: (8, 32, 40), 14: (40, 120, 128), 15: (88, 192, 200)},
    "buttons": {1: (232, 240, 248), 2: DARK, 3: STEEL1, 4: STEEL3, 5: (176, 200, 240), 6: (24, 40, 80), 7: (56, 88, 152),
                8: (88, 64, 160), 9: (152, 120, 224), 10: (40, 120, 128), 11: (88, 192, 200),
                12: (40, 136, 168), 13: (96, 208, 232), 14: DARK, 15: DARK},
    "cursor": {1: (248, 96, 160), 2: (216, 72, 136), 3: (168, 48, 112), 12: (152, 176, 232), 14: (152, 176, 232)},
    "keyboard": {1: SLATE, 2: PALE, 3: STEEL1, 11: PALE, 12: DARK, 13: INK, 14: (24, 16, 48), 15: (8, 32, 40)},
}

GLYPH = {"0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"]}
#  (x, y, digit, index) inside the 32x32 block -- sparse, uneven, never touching across a repeat
SCATTER = [(2, 3, "1", 13), (13, 1, "0", 13), (24, 6, "1", 14), (7, 13, "0", 13), (19, 16, "1", 13),
           (28, 21, "0", 13), (3, 25, "1", 14), (14, 26, "0", 13)]
BLOCK_FIRST, BLOCK_W = 30, 4          # tiles 30..45, a 4x4 block
SOLID = {1: 12, 2: 12, 3: 12, 4: 12}  # the old stripes and their edges: plain navy


def read_pal(name):
    lines = open(os.path.join(NS, name + ".pal")).read().split("\n")
    return [tuple(int(v) for v in l.split()) for l in lines[3:19]]


def pal_text(cols):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols)


def main():
    changes = 0
    for name, edits in PALETTES.items():
        cols = read_pal(name)
        new = [edits.get(i, c) for i, c in enumerate(cols)]
        if new != cols:
            changes += 1
            print("  %-18s %d colour(s)" % (name + ".pal", sum(a != b for a, b in zip(cols, new))))
            if WRITE:
                open(os.path.join(NS, name + ".pal"), "w", newline="").write(pal_text(new))

    im = Image.open(os.path.join(NS, "menu.png"))
    px = im.load()
    before = im.tobytes()
    for t, idx in SOLID.items():
        tx, ty = (t % 16) * 8, (t // 16) * 8
        for y in range(8):
            for x in range(8):
                px[tx + x, ty + y] = idx
    block = [[12] * 32 for _ in range(32)]
    for x0, y0, dgt, idx in SCATTER:
        for yy, row in enumerate(GLYPH[dgt]):
            for xx, ch in enumerate(row):
                if ch == "1":
                    block[y0 + yy][x0 + xx] = idx
    for by in range(BLOCK_W):
        for bx in range(BLOCK_W):
            t = BLOCK_FIRST + by * BLOCK_W + bx
            tx, ty = (t % 16) * 8, (t // 16) * 8
            for y in range(8):
                for x in range(8):
                    px[tx + x, ty + y] = block[by * 8 + y][bx * 8 + x]
    menu = PALETTES["menu"]
    flat = []
    for i, c in enumerate(read_pal("menu")):
        flat += list(menu.get(i, c))
    im.putpalette(flat + [0] * (768 - len(flat)))
    if im.tobytes() != before:
        changes += 1
        print("  menu.png           tiles 1..4 navy, tiles %d..%d the binary block" % (BLOCK_FIRST, BLOCK_FIRST + 15))
        if WRITE:
            im.save(os.path.join(NS, "menu.png"))

    path = os.path.join(NS, "background.bin")
    bd = bytearray(open(path, "rb").read())
    n = 0
    for i in range(len(bd) // 2):
        v = struct.unpack_from("<H", bd, i * 2)[0]
        if v & 0x3FF == 2:
            x, y = i % 32, i // 32
            t = BLOCK_FIRST + (y % BLOCK_W) * BLOCK_W + (x % BLOCK_W)
            struct.pack_into("<H", bd, i * 2, (v & ~0x3FF) | t)
            n += 1
    if n:
        changes += 1
        print("  background.bin     %d cells of the old stripe tile -> the binary block" % n)
        if WRITE:
            open(path, "wb").write(bd)
    print("  %s" % ("nothing to change" if not changes else ("written" if WRITE else "run with --write to write")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
