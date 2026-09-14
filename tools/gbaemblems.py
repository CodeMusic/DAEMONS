#!/usr/bin/env python3
"""The three emblems of 9.23, drawn once (T-62, vision.md 9.23).

    python3 tools/gbaemblems.py     # preview to /tmp/emblems.png

A symbol per kind replaces the Poke Ball wherever it stood -- over the door, on
the sign, on the CHECKPOINT floor:

    CHECKPOINT   a circular restore arrow      teal
    THE REPO     a stacked package             golden amber
    BENCHMARK    a gauge with one needle       slate, a gold pivot

Each is 16x16 in roles, not colours: O outline, L light, M mid, D dark, T a
highlight, W the dial face, S its base, N the needle, G gold. Whichever tool
places an emblem maps the roles onto the palette row the building is drawn in,
so one drawing serves the door, the sign and the floor.
"""
from PIL import Image

EMBLEMS = {
    "CHECKPOINT": [
        "................",
        ".....OOOOOO.....",
        "...OOLLLLLLO....",
        "..OLMMMMMMMLO...",
        ".OLMOOOOOOOMMO..",
        ".OLMO.....OOLMOO",
        "OLMO.......OOOOO",
        "OLMO.....OLLLLMO",
        "OLMO......OLMMO.",
        "OLMO.......OMO..",
        ".OLMO.......O...",
        ".OLMMO..........",
        "..OLMMOOOOOO....",
        "...OOLMMMMMO....",
        ".....OOOOOO.....",
        "................"],
    "REPO": [
        "................",
        ".....OOOOOO.....",
        "....OLLLLLMO....",
        "....OLLTLLMO....",
        "....OMMTMMDO....",
        "....OOOOOOOO....",
        "..OOOOOOOOOOOO..",
        ".OLLLLLMOLLLLLMO",
        ".OLLTLLMOLLLTLMO",
        ".OMMTMMDOMMMTMDO",
        ".OMMTMMDOMMMTMDO",
        ".OMMMMMDOMMMMMDO",
        ".ODDDDDDODDDDDDO",
        ".OOOOOOOOOOOOOO.",
        "................",
        "................"],
    "BENCHMARK": [
        "................",
        ".....OOOOOO.....",
        "...OOWWWWWWOO...",
        "..OWWTWWWWTWWO..",
        ".OWTWWWWWWWWTWO.",
        ".OWWWWWWWWWNWWO.",
        "OWTWWWWWWWNWWTWO",
        "OWWWWWWWWNWWWWWO",
        "OWWWWWWWNWWWWWWO",
        "OWWWWWWGOGGWWWWO",
        ".OWWWWWGGGWWWWO.",
        ".OWSSSSSSSSSSSO.",
        "..OSSSSSSSSSSO..",
        "...OOOOOOOOOO...",
        "................",
        "................"],
}

# nominal colours, for previews only
PREVIEW_COLOURS = {
    "CHECKPOINT": {"O": (36, 70, 76), "L": (156, 220, 210), "M": (96, 184, 176), "D": (58, 138, 140)},
    "REPO": {"O": (80, 56, 30), "L": (238, 214, 140), "M": (212, 168, 82), "D": (170, 120, 54), "T": (250, 244, 220)},
    "BENCHMARK": {"O": (52, 58, 72), "W": (232, 236, 242), "T": (120, 128, 146), "N": (52, 58, 72),
                  "G": (214, 176, 70), "S": (150, 160, 178)},
}


def emblem(kind, roles):
    """16x16 of palette indices (0 = transparent), given {role: index}."""
    return [[roles.get(ch, 0) if ch != "." else 0 for ch in row] for row in EMBLEMS[kind]]


def main():
    sheet = Image.new("RGB", (16 * 3 + 16, 16), (124, 192, 104))
    for k, kind in enumerate(EMBLEMS):
        for y, row in enumerate(EMBLEMS[kind]):
            for x, ch in enumerate(row):
                if ch != ".":
                    sheet.putpixel((k * 24 + x, y), PREVIEW_COLOURS[kind][ch])
    sheet.resize((sheet.width * 12, sheet.height * 12), Image.NEAREST).save("/tmp/emblems.png")
    print("  preview /tmp/emblems.png")


if __name__ == "__main__":
    main()
