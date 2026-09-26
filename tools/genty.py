#!/usr/bin/env python3
"""Ty's own portrait and walking sheet: a red fox in a doctor's coat (T-298, DRAFT).

    python3 tools/genty.py            # report, and a preview in the scratch dir
    python3 tools/genty.py --write    # graphics/trainers/front_pics/ty_front_pic.png, palettes/ty.pal,
                                      # graphics/object_events/pics/people/ty.png

THE FAMILY IS A PALETTE APART (vision.md 4.3): "Three foxes, a palette apart -- Crystal golden-amber, Ty darker, Al
somewhere between. Family resemblance at sprite level, zero text." So Ty is drawn FROM CRYSTAL, not beside her: her
intro portrait and her walking sheet, with the gold fur taken down to a deep red. The user asked for a red fox who
reads as a doctor without saying so (2026-09-26); her white coat already does that, and her purple shirt and tie go
to a sober slate, so the one note of colour on him is the fur.

THE WALKING SHEET costs no new colour. It stays in OBJ_EVENT_PAL_TAG_NPC_CLEARS, the family's own sixteen, which
already hold the rust and the dark brown AL's shading uses: gold -> rust, amber -> dark brown, purple -> slate.

THE PORTRAIT is CRYSTAL's 64x96 intro picture from the ears to the thigh, which is the 64x64 a battle shows, recoloured
the same way and put on sixteen colours of its own. These are drafts, for the refining sweep (T-210/T-120).
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

CRYSTAL_PIC = os.path.join(GBA, "graphics/oak_speech/oak/pic.png")
CRYSTAL_OW = os.path.join(GBA, "graphics/object_events/pics/people/prof_oak.png")
OUT_PIC = os.path.join(GBA, "graphics/trainers/front_pics/ty_front_pic.png")
OUT_PAL = os.path.join(GBA, "graphics/trainers/palettes/ty.pal")
OUT_OW = os.path.join(GBA, "graphics/object_events/pics/people/ty.png")

#  the walking sheet, index to index inside NPC_CLEARS: gold -> rust, amber -> dark brown, purple -> slate
OW_REMAP = {1: 13, 2: 3, 6: 7}
#  the portrait, colour to colour: her gold shades to his reds, her purple shirt to slate
PIC_REMAP = {
    (223, 176, 60): (196, 82, 40), (214, 167, 54): (182, 74, 36), (210, 162, 50): (170, 66, 32),
    (172, 126, 48): (122, 48, 26), (169, 148, 102): (150, 100, 82),
    (135, 103, 133): (78, 84, 100), (121, 87, 103): (60, 64, 80),
}
CROP_TOP = 4                    # the tips of the ears


def portrait():
    src = Image.open(CRYSTAL_PIC)
    pal = src.getpalette()
    bg = tuple(pal[0:3])
    rgb = Image.new("RGB", (64, 64), bg)
    for y in range(64):
        for x in range(64):
            i = src.getpixel((x, y + CROP_TOP))
            c = tuple(pal[i * 3:i * 3 + 3])
            rgb.putpixel((x, y), PIC_REMAP.get(c, c))
    #  sixteen colours, the backdrop first: quantise the figure to fifteen and put the backdrop at index 0
    fig = [c for c in set(rgb.getdata()) if c != bg]
    if len(fig) > 15:
        q = rgb.quantize(colors=16, method=Image.Quantize.MEDIANCUT)
        cols = [tuple(q.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
        near = lambda c: min(range(16), key=lambda i: sum((a - b) ** 2 for a, b in zip(cols[i], c)))
        ib = near(bg)
        order = [ib] + [i for i in range(16) if i != ib]
        cols = [bg] + [cols[i] for i in order[1:]]
        idx = {old: new for new, old in enumerate(order)}
        out = Image.new("P", (64, 64))
        out.putdata([0 if c == bg else idx[near(c)] if idx[near(c)] != 0 else 1 for c in rgb.getdata()])
    else:
        cols = [bg] + sorted(fig)
        cols += [(0, 0, 0)] * (16 - len(cols))
        where = {c: i for i, c in enumerate(cols)}
        out = Image.new("P", (64, 64))
        out.putdata([where[c] for c in rgb.getdata()])
    out.putpalette([v for c in cols for v in c] + [0] * (768 - 48))
    return out, cols


#  THE TENTH FRAME. A trainer's sheet has ten: the ninth-plus-one is ANIM_RAISE_HAND, which the field asks for after a
#  trainer battle. CRYSTAL never battles, so her sheet stops at nine, and a table of nine read the tenth from whatever
#  lay past it -- Ty came back from his battle with no picture at all (T-298). His tenth is his front frame with the
#  right paw up: a white sleeve along the edge and the rust paw above it.
RAISED = [(14, 9, 15), (15, 9, 15), (14, 10, 13), (15, 10, 15), (14, 11, 13), (15, 11, 15)] + \
         [(15, y, 14) for y in range(12, 22)] + [(14, y, 14) for y in range(17, 22)]


def sheet():
    src = Image.open(CRYSTAL_OW)
    out = Image.new("P", (src.width + 16, src.height))
    out.paste(src, (0, 0))
    out.putdata([OW_REMAP.get(i, i) for i in out.getdata()])
    out.paste(out.crop((0, 0, 16, 32)), (src.width, 0))
    for x, y, i in RAISED:
        out.putpixel((src.width + x, y), i)
    out.putpalette(src.getpalette())
    return out


def main():
    pic, cols = portrait()
    ow = sheet()
    print("  portrait: 64x64 from CRYSTAL's intro picture, %d colours" % len(set(pic.getdata())))
    print("  walking sheet: %dx%d from CRYSTAL's, in NPC_CLEARS" % ow.size)
    prev = Image.new("RGBA", (64 + 8 + ow.width, 64), (40, 40, 40, 255))
    prev.paste(pic.convert("RGBA"), (0, 0))
    prev.paste(ow.convert("RGBA"), (72, 0))
    os.makedirs(SCRATCH, exist_ok=True)
    prev.resize((prev.width * 4, prev.height * 4), Image.NEAREST).save(os.path.join(SCRATCH, "ty_preview.png"))
    if not WRITE:
        print("  report only; pass --write (preview in %s)" % SCRATCH)
        return
    pic.save(OUT_PIC, bits=4)
    with open(OUT_PAL, "w") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in cols))
    ow.save(OUT_OW, bits=4)
    print("  written")


if __name__ == "__main__":
    main()
