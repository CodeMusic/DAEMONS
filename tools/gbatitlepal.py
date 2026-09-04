#!/usr/bin/env python3
"""Author the title screen's background palette -- bank 15, and bank 14.

    python3 tools/gbatitlepal.py            # report
    python3 tools/gbatitlepal.py --write

WHAT EACH INDEX ACTUALLY IS. This palette is loaded into BG banks 14 AND 15,
and between them they paint every part of the title screen that is not the
wordmark. The roles are not documented anywhere in pokefirered; they were
recovered by rendering each index separately (tools/gbatitleview.py), and
losing them again would make this screen unmaintainable:

     1-5   PRESS START.  Task_TitleScreen_BlinkPressStart hides the text by
           writing index 6 over entries 1-5 and shows it by writing them back,
           so INDEX 6 MUST BE THE COLOUR BEHIND THE TEXT or the blink leaves a
           visible block. 1 is the letter body, 3 the outline.
     6     the two bands, y 9-30 and y 112-149 -- and therefore the blink's
           off-colour, per above.
     10    the copyright line's ink.
     11    THE STAGE, y 31-111, drawn by BG3. The daemons stand on this and the
           particles cross it.
     12    the bottom strip, y 150-159, under the copyright.
     15    the top strip, y 0-8.
     0, 7-9, 13, 14  unused; held at the band colour so a mistake is quiet.

WHY IT IS DARK NOW. It was not a palette choice before -- tools/gbastrip.py
rebuilt this layer's tilemap from tile indices alone and wrote palette bank 0
instead of 15, so PRESS START, the copyright and all four fills were reading
the WORDMARK's colour ramp. Yellow text on a yellow band. With bank 15 restored
the fills are ours to set, and a dark ground is what a bright wordmark, two
lit creatures and a bloom in the middle all need.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GFX = os.path.join(ROOT, "engineGba/graphics/title_screen")

#  CONTENT is the cold edition and its wordmark is a steel ramp; CONTEXT is the
#  spectrum. Each ground is the same hue family as its wordmark, several stops
#  down, so the letters read as lit rather than as pasted on.
EDITIONS = {
    "firered": dict(name="CONTENT", strip=(8, 12, 22), band=(14, 20, 36),
                    stage=(26, 40, 72), copy=(120, 150, 196),
                    start=[(232, 244, 255), (96, 128, 184), (132, 164, 216),
                           (176, 204, 240), (208, 228, 252)]),
    "leafgreen": dict(name="CONTEXT", strip=(14, 8, 20), band=(26, 14, 38),
                      stage=(48, 26, 68), copy=(176, 140, 200),
                      start=[(250, 238, 255), (140, 96, 180), (178, 132, 212),
                             (214, 180, 238), (236, 216, 250)]),
}

def build(e):
    p = [e["band"]] * 16
    for i, c in enumerate(e["start"]):
        p[1 + i] = c
    p[6], p[10], p[11], p[12], p[15] = e["band"], e["copy"], e["stage"], e["strip"], e["strip"]
    return p

def q(c):
    "What the GBA actually shows: five bits a channel."
    return tuple((v >> 3) * 255 // 31 for v in c)

def main():
    for sub, e in EDITIONS.items():
        p = build(e)
        print("  %s (%s)" % (e["name"], sub))
        for label, i in (("top strip", 15), ("bands / blink-off", 6),
                         ("stage", 11), ("bottom strip", 12),
                         ("PRESS START body", 1), ("PRESS START outline", 3),
                         ("copyright", 10)):
            print("    %-22s idx %2d  #%02X%02X%02X" % ((label, i) + q(p[i])))
        if "--write" in sys.argv:
            dst = os.path.join(GFX, sub, "background.pal")
            with open(dst, "w") as f:
                f.write("JASC-PAL\n0100\n16\n")
                for c in p:
                    f.write("%d %d %d\n" % c)
            print("    written %s" % os.path.relpath(dst, ROOT))
    if "--write" not in sys.argv:
        print("\n  (report only; pass --write)")

main()
