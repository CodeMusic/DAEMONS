#!/usr/bin/env python3
"""The WARDEN's TOKEN: vanilla's GOLD TEETH, as 8.6 adopted it (the user's review, 2026-08-31; built 2026-09-24).

    python3 tools/gentoken.py            # report
    python3 tools/gentoken.py --write     # graphics/items/icons/gold_teeth.png and its .pal

WHAT IT IS. The SAFARI ZONE hands out GUESTBOXes -- restricted, temporary, expiring access; a guest account (1.3).
Its WARDEN has lost his TOKEN, and without it nothing he says can be read: vanilla's toothless mumble is already the
right sound for speech that arrives and cannot be decrypted. So the item is a hardware token -- a key fob with a
little screen of digits and a ring to hang it from -- and giving it back is what lets him be understood.

EVERY PIXEL AUTHORED, as genmisc.py draws its objects; vanilla's icon is used for nothing but its size (24x24) and
its file, which keeps the item table's pointers where they are. The icon has a palette of its own, so its colours
are chosen, not inherited: greys for the casing, the tower stones' dark screen and light marks (T-249) for the
display, since both are records kept where nobody can read them without the right key.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = os.path.join(ROOT, "engineGba/graphics/items/icons/gold_teeth.png")
PAL = os.path.join(ROOT, "engineGba/graphics/items/icon_palettes/gold_teeth.pal")
WRITE = "--write" in sys.argv

COLOURS = [
    (180, 180, 180),   # . transparent, vanilla's own key colour
    (41, 41, 49),      # k outline
    (106, 110, 122),   # d casing, shade
    (148, 152, 164),   # m casing
    (196, 200, 208),   # l casing, light
    (236, 238, 242),   # h highlight
    (24, 30, 28),      # s the screen
    (150, 200, 160),   # g the digits
    (120, 124, 132),   # r the ring
] + [(0, 0, 0)] * 7
KEY = {".": 0, "k": 1, "d": 2, "m": 3, "l": 4, "h": 5, "s": 6, "g": 7, "r": 8}

ART = [
    "........................",
    "..rrrr..................",
    ".r....r.................",
    ".r....r.................",
    ".r....r.................",
    "..rr.rr.................",
    "....rkkkkkkkkkkkkkkk....",
    "....khhhhhhhhhhhhhllk...",
    "....khlllllllllllllmk...",
    "....khlkkkkkkkkkkklmk...",
    "....khlksssssssssklmk...",
    "....khlksgsgsgsggklmk...",
    "....khlksgsgsgsgsklmk...",
    "....khlksssssssssklmk...",
    "....khlkkkkkkkkkkklmk...",
    "....khllllllllllllmmk...",
    "....khllllllkkllllmmk...",
    "....khlllllkmmklllmmk...",
    "....khlllllkmmklllmdk...",
    "....khllllllkkllllmdk...",
    "....kmmmmmmmmmmmmmmdk...",
    ".....kdddddddddddddk....",
    "......kkkkkkkkkkkkk.....",
    "........................",
]


def build():
    assert len(ART) == 24 and all(len(r) == 24 for r in ART), "the icon is 24x24"
    img = Image.new("P", (24, 24), 0)
    img.putpalette([c for rgb in COLOURS for c in rgb] + [0] * (768 - 48))
    img.putdata([KEY[ch] for row in ART for ch in row])
    return img


def main():
    img = build()
    old = Image.open(ICON)
    same = list(old.getdata()) == list(img.getdata()) and old.getpalette()[:48] == img.getpalette()[:48]
    print("  the TOKEN's icon%s" % (" -- already drawn" if same else ": to draw over vanilla's GOLD TEETH"))
    if WRITE and not same:
        img.save(ICON)
        with open(PAL, "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in COLOURS))
        print("  written")
    if os.environ.get("SCRATCH"):
        img.convert("RGB").resize((96, 96), Image.NEAREST).save(os.path.join(os.environ["SCRATCH"], "token.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
