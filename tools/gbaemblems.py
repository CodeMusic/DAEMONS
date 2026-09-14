#!/usr/bin/env python3
"""The three emblems of 9.23, drawn once (T-62, vision.md 9.23).

    python3 tools/gbaemblems.py     # preview to /tmp/emblems.png

A symbol per kind replaces the Poke Ball wherever it stood -- over the door, on
the sign, on the CHECKPOINT floor:

    CHECKPOINT   a circular restore arrow      teal
    THE REPO     a branch glyph                golden amber   (it was a package until T-66)
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
    "REPO": [                                   # the version-control branch: a trunk, a fork, three commits
        "................",
        "....OOO.........",
        "...OLLLO........",
        "...OLTLO...OOO..",
        "...OLLLO..OLLLO.",
        "....OMO...OLTLO.",
        "....OMO...OLLLO.",
        "....OMO....OMO..",
        "....OMO...OMMO..",
        "....OMOOOOMMO...",
        "....OMMMMMMO....",
        "...OLLLOOOO.....",
        "...OLTLO........",
        "...OLLLO........",
        "....OOO.........",
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
    "REPO": {"O": (80, 56, 30), "L": (238, 214, 140), "M": (170, 120, 54), "T": (250, 244, 220)},
    "BENCHMARK": {"O": (52, 58, 72), "W": (232, 236, 242), "T": (120, 128, 146), "N": (52, 58, 72),
                  "G": (214, 176, 70), "S": (150, 160, 178)},
}


# a 3x5 face for the plates beside the doors (T-66)
FONT = {
    "A": ("010", "101", "111", "101", "101"), "E": ("111", "100", "110", "100", "111"),
    "K": ("101", "101", "110", "101", "101"), "M": ("101", "111", "111", "101", "101"),
    # K was 101/110/100/110/101, which read as an E on the MARK plate (T-79)
    "O": ("111", "101", "101", "101", "111"), "P": ("110", "101", "110", "100", "100"),
    "R": ("110", "101", "110", "101", "101"),
    # for the marks' names on the BENCHMARK frieze (T-79): SLATE SLOPE SENSE FIT SKEW FRAME HEAT TRUE
    "S": ("111", "100", "111", "001", "111"), "L": ("100", "100", "100", "100", "111"),
    "T": ("111", "010", "010", "010", "010"), "N": ("111", "101", "101", "101", "101"),
    "F": ("111", "100", "110", "100", "100"), "I": ("111", "010", "010", "010", "111"),
    "H": ("101", "101", "111", "101", "101"), "U": ("101", "101", "101", "101", "111"),
    "W": ("101", "101", "111", "111", "101"),
    "C": ("011", "100", "100", "100", "011"),             # for SCORN on Quicksilver's board (T-86)
}
CHECK = ["......",                                 # a checkmark for the CHECKPOINT's plate
         ".....1",
         "....11",
         "1..11.",
         "1111..",
         ".11..."]


def word(text):
    """rows of 0/1, three pixels a letter and one between."""
    rows = [[] for _ in range(5)]
    for k, ch in enumerate(text):
        for y in range(5):
            rows[y] += [int(b) for b in FONT[ch][y]] + ([0] if k < len(text) - 1 else [])
    return rows


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
