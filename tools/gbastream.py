#!/usr/bin/env python3
"""TEACHY TV's title card, as STREAM (T-98; vision.md 9.22).

    python3 tools/gbastream.py            # preview to /tmp/stream.png (vanilla | ours)
    python3 tools/gbastream.py --write    # graphics/teachy_tv/tiles.png and title.bin

The item has been STREAM since the vocabulary port; the show's title card still
said TEACHY / TV. The card is a cloud-shaped badge drawn in BG palette 2 by
graphics/teachy_tv/title.bin, a 32x32 tilemap over tiles.png -- whose pixels for
palette 2 are stored as 32 + index.

The badge is kept, and so is its style: the top lobe's six italic letters become
STREAM (six again, in the same red with an orange shadow), and the lower lobe's
pink T and blue V become a pink PLAY mark and a blue wave, each in the same white
keyline -- a stream is something that plays as it arrives.

Re-tiling: every cell inside the badge is redrawn, its 8x8 tiles deduplicated, and
the new tiles written into the tile slots the badge used and nothing else used
(no other title cell, nothing in screen.bin). It stops if they do not fit.
"""
import os, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DIR = os.path.join(GBA, "graphics/teachy_tv")
PREVIEW = "/tmp/stream.png"
WRITE = "--write" in sys.argv
BOX = (5, 1, 26, 12)                     # the badge's cells: x0, y0, x1, y1 (exclusive)
PAL = 2
OUTLINE_KEEP = {0, 1, 3, 8}              # the cloud's own colours; the letters' (and their pale-yellow edges) are painted over with 3
LETTERS_AREA = ((54, 26, 190, 50), (82, 48, 160, 84))   # pixel boxes of TEACHY and of T V, in title-map pixels

GLYPHS = {
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
}
RED, ORANGE, WHITE, PINK, BLUE, YELLOW = 5, 7, 2, 6, 11, 3


def read_jasc(path, n):
    lines = open(path).read().replace("\r", "").split("\n")
    return [tuple(map(int, l.split())) for l in lines[3:3 + n]]


def main():
    tiles = Image.open(os.path.join(DIR, "tiles.png")); tp = tiles.load()
    title = bytearray(open(os.path.join(DIR, "title.bin"), "rb").read())
    screen = open(os.path.join(DIR, "screen.bin"), "rb").read()
    cols = read_jasc(os.path.join(DIR, "palettes.pal"), 64)
    entry = lambda buf, i: struct.unpack_from("<H", buf, i * 2)[0]
    x0, y0, x1, y1 = BOX
    inbox = lambda i: x0 <= i % 32 < x1 and y0 <= i // 32 < y1

    # the badge as it is, in palette-2 indices over title-map pixels
    W, H = (x1 - x0) * 8, (y1 - y0) * 8
    canvas = [[0] * W for _ in range(H)]
    for cy in range(y0, y1):
        for cx in range(x0, x1):
            t = entry(title, cy * 32 + cx) & 0x3FF
            for y in range(8):
                for x in range(8):
                    canvas[(cy - y0) * 8 + y][(cx - x0) * 8 + x] = tp[(t % 16) * 8 + x, (t // 16) * 8 + y] % 16
    before = [row[:] for row in canvas]

    def put(px, py, v):
        X, Y = px - x0 * 8, py - y0 * 8
        if 0 <= X < W and 0 <= Y < H:
            canvas[Y][X] = v

    def get(px, py):
        X, Y = px - x0 * 8, py - y0 * 8
        return canvas[Y][X] if 0 <= X < W and 0 <= Y < H else 0

    # 1. paint the old letters out with the badge's yellow
    for (a, b, c, d) in LETTERS_AREA:
        for py in range(b, d):
            for px in range(a, c):
                if get(px, py) not in OUTLINE_KEEP:
                    put(px, py, YELLOW)

    # 2. STREAM, italic, bold (each glyph pixel three wide and two tall, as heavy as TEACHY's), an orange shadow under the red
    def letters(text, lx, ly):
        pts = []
        for k, ch in enumerate(text):
            for gy, row in enumerate(GLYPHS[ch]):
                for gx, bit in enumerate(row):
                    if bit == "#":
                        for sy in range(2):
                            for sx in range(3):
                                pts.append((lx + k * 20 + gx * 2 + sx + (6 - gy) // 2, ly + gy * 2 + sy))
        return pts
    pts = letters("STREAM", 62, 31)
    for (px, py) in pts:
        put(px + 1, py + 1, ORANGE)
    for (px, py) in pts:
        put(px, py, RED)

    # 3. a PLAY mark and a wave, each filled and keylined in white, two pixels thick
    def keylined(mask, fill):
        edge = set()
        for (px, py) in mask:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if abs(dx) + abs(dy) <= 3:
                        edge.add((px + dx, py + dy))
        for p in edge:
            put(p[0], p[1], WHITE)
        for p in mask:
            put(p[0], p[1], fill)
    play = {(px, py) for py in range(56, 77) for px in range(92, 110) if (px - 92) * 21 <= 18 * min(py - 56, 76 - py) * 2}
    keylined(play, PINK)
    import math
    wave = set()
    for px in range(124, 153):
        cy = 66 + round(5 * math.sin((px - 124) / 28 * 2 * math.pi))
        for py in range(cy - 3, cy + 3):
            wave.add((px, py))
    keylined(wave, BLUE)

    # re-tile the box
    pool_users = {}
    for i in range(1024):
        pool_users.setdefault(entry(title, i) & 0x3FF, set()).add("box" if inbox(i) else "title")
    for i in range(len(screen) // 2):
        pool_users.setdefault(entry(screen, i) & 0x3FF, set()).add("screen")
    pool = sorted(t for t, u in pool_users.items() if u == {"box"} and t != 0)
    blank = None
    new_tiles, assign = {}, {}
    for cy in range(y0, y1):
        for cx in range(x0, x1):
            px = tuple(canvas[(cy - y0) * 8 + y][(cx - x0) * 8 + x] for y in range(8) for x in range(8))
            if not any(px):
                assign[(cx, cy)] = None
                continue
            new_tiles.setdefault(px, len(new_tiles))
            assign[(cx, cy)] = new_tiles[px]
    print("  badge: %d cells, %d distinct tiles needed, %d slots the badge alone used" % ((x1 - x0) * (y1 - y0), len(new_tiles), len(pool)))
    # an empty cell takes a tile that is empty already, as the card's background does
    for t in sorted(pool_users):
        if all(tp[(t % 16) * 8 + x, (t // 16) * 8 + y] % 16 == 0 for x in range(8) for y in range(8)):
            blank = t
            break
    assert blank is not None, "no blank tile to give the empty cells"
    if len(new_tiles) > len(pool):
        raise SystemExit("  does not fit: %d tiles for %d slots" % (len(new_tiles), len(pool)))

    # preview: before | after, in palette 2
    sheet = Image.new("RGB", (W * 2 + 8, H), (40, 40, 40))
    for k, src in enumerate((before, canvas)):
        for y in range(H):
            for x in range(W):
                v = src[y][x]
                sheet.putpixel((k * (W + 8) + x, y), cols[PAL * 16 + v] if v else (70, 100, 90))
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(PREVIEW)
    print("  preview %s (vanilla | ours)" % PREVIEW)

    if WRITE:
        slots = {n: pool[n] for n in range(len(new_tiles))}
        for px, n in new_tiles.items():
            t = slots[n]
            for i, v in enumerate(px):
                tp[(t % 16) * 8 + i % 8, (t // 16) * 8 + i // 8] = PAL * 16 + v if v else 0
        for t in pool[len(new_tiles):]:
            for y in range(8):
                for x in range(8):
                    tp[(t % 16) * 8 + x, (t // 16) * 8 + y] = 0
        for (cx, cy), n in assign.items():
            i = cy * 32 + cx
            e = entry(title, i)
            t = blank if n is None else slots[n]
            struct.pack_into("<H", title, i * 2, (e & ~0xFFF) | t)
        tiles.save(os.path.join(DIR, "tiles.png"))
        open(os.path.join(DIR, "title.bin"), "wb").write(title)
        print("  written: tiles.png and title.bin")


if __name__ == "__main__":
    main()
