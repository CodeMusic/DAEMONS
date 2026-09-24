#!/usr/bin/env python3
"""DAD, drawn from MOM (T-256; the user, 2026-09-24: "a Dad character in the house, similar to the Mom but with
black combed-back hair").

    python3 tools/gendad.py            # report (SCRATCH=dir also draws a contact sheet there)
    python3 tools/gendad.py --write     # graphics/object_events/pics/people/dad.png

The fable holds (every person is an animal), so DAD is MOM's animal: the same grey face and the same frame, drawn
from her sheet so the two are one family by construction. What changes, index by index, in her own palette:

  * hair (8, 9) above the brow becomes near-black (13) -- combed back, so nothing of it falls below the brow;
  * the long sides and the tail tip she wears in her hair colour become her grey fur (12);
  * her apron (14) becomes her shirt (6); her skirt (4) becomes dark trousers (13), its seam (10) the outline.

A DRAFT: the user sees it on the contact sheet and in the house before it is final.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
MOM = os.path.join(GBA, "graphics/object_events/pics/people/mom.png")
DAD = os.path.join(GBA, "graphics/object_events/pics/people/dad.png")
WRITE = "--write" in sys.argv
BROW = 12                                  # the last row of hair on top of the head


def draw():
    mom = Image.open(MOM)
    dad = mom.copy()
    px = dad.load()
    for y in range(mom.height):
        for x in range(mom.width):
            v = px[x, y]
            if v in (8, 9):
                px[x, y] = 13 if y <= BROW else 12
            elif v == 14:
                px[x, y] = 6
            elif v == 4:
                px[x, y] = 13
            elif v == 10:
                px[x, y] = 15
    return mom, dad


def main():
    mom, dad = draw()
    have = Image.open(DAD) if os.path.exists(DAD) else None
    changed = have is None or list(have.getdata()) != list(dad.getdata())
    print("  DAD %s" % ("to draw" if changed else "is drawn"))
    out = os.environ.get("SCRATCH")                 # a contact sheet only when asked for, and only there
    if out:
        sheet = Image.new("RGBA", (mom.width * 2 + 8, mom.height), (40, 40, 40, 255))
        sheet.paste(mom.convert("RGBA"), (0, 0))
        sheet.paste(dad.convert("RGBA"), (mom.width + 8, 0))
        sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST).save(os.path.join(out, "dad_sheet.png"))
    if WRITE and changed:
        dad.save(DAD)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
