#!/usr/bin/env python3
"""The lioness, met four times before the ship, and the easel that holds the pair of paintings (T-493, T-494, T-496;
the user, 2026-10-30; the design in docs/private, never in a tracked file).

    python3 tools/genlioness.py            # report: are both sheets current and registered
    python3 tools/genlioness.py --write    # lioness.png + easel.png, their spritesheet rules, and the graphics ids
                                           #   OBJ_EVENT_GFX_LIONESS and OBJ_EVENT_GFX_EASEL

THE LIONESS: every person is an animal (fable-actors-animals). Drawn with the town folk's own figure (gentowns.fig,
genfolk.figure) in npc_blue: gold fur, a cream muzzle, a lavender top and indigo trousers. The same sheet every time
she is met, so a player who is looking knows her. Her ball is not on the sheet: she is met with it only once, and the
deck's lines carry it.

THE EASEL: one canvas on its stand, a meadow at night under a white moon, the moon to the left and a tree to the right.
Every frame is the same picture, so it reads the same from any side; the engine draws an object facing EAST as its
west frame flipped, so the S.S. ANNE's easel faces west and THE NEXUS's faces east, and the twin is the first one's
mirror image without a second sheet.

Each in a vanilla palette in vanilla's own slot for it, so neither can repaint anyone: the lioness in npc_blue
(PALSLOT_NPC_1), whose purples and golds are THE PAINTED MIRROR's; the easel in npc_pink (PALSLOT_NPC_2), a navy sky
and blue hills, because THE PHOENIX in THE NEXUS holds slot 1 in its type's colours (check_reach, trap 17).
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
PALS = os.path.join(GBA, "graphics/object_events/palettes")
RULES = os.path.join(GBA, "spritesheet_rules.mk")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))

# npc_blue: a cream  s skin  S skin shade  e brown  Y yellow  y gold  o dark gold  L lavender  P purple
#           D indigo  O orange  r red  n dark brown  W white  K black
BLUE = {" ": 0, ".": 0, "a": 1, "s": 2, "S": 3, "e": 4, "Y": 5, "y": 6, "o": 7, "L": 8, "P": 9, "D": 10,
        "O": 11, "r": 12, "n": 13, "W": 14, "K": 15}
# the easel's letters in npc_pink: o frame (wine)  D navy sky  Y moon (white)  P blue hill  L light blue hill
#           e brown wood  K black
PINK = {".": 0, "e": 4, "o": 7, "L": 8, "P": 9, "D": 10, "Y": 14, "K": 15}


def gentowns():
    """gentowns and genfolk, imported without arming anything (engine.md trap 16)"""
    argv, sys.argv = sys.argv, [sys.argv[0]]
    try:
        import gentowns as g, genfolk as f
    finally:
        sys.argv = argv
    return g, f


def lioness():
    g, f = gentowns()
    head = g.mammal("y", "o", "a")                       # gold fur, dark-gold ears, a cream muzzle
    front, back, side = g.fig(head, "y", "L", "D", "y", "o")
    back = g.overlay(back, g.TAIL, ["KyK", "KyK", "KyK", "KoK", " KK"], 7)     # the tail, its dark tuft
    frames = f.figure(front, back, side)
    f.check("lioness", frames, BLUE)
    return frames


# The canvas: a meadow at night (navy sky, blue hills), a white moon top left, a tree in silhouette on the right. Rows 0-31.
EASEL = [
    "................",
    "................",
    "................",
    "................",
    ".KKKKKKKKKKKKKK.",
    ".KoooooooooooooK",
    ".KoDDDDDDDDDDDoK",
    ".KoDYYDDDDDDDDoK",
    ".KoDYYYDDDDKDDoK",
    ".KoDDYDDDDKKKDoK",
    ".KoDDDDDDDKKKDoK",
    ".KoDDDDDDKKKKKoK",
    ".KoDPPDDDDDeDDoK",
    ".KoPPPPPDDDePPoK",
    ".KoLPPPPPPPPPLoK",
    ".KoLLLPPPPPLLLoK",
    ".KoLLLLLLLLLLLoK",
    ".KoooooooooooooK",
    ".KKKKKKKKKKKKKKK",
    "...KeK.....KeK..",
    "...KeK.....KeK..",
    "...KeK..K..KeK..",
    "...KeK.KeK.KeK..",
    "...KeK.KeK.KeK..",
    "..KeK..KeK..KeK.",
    "..KeK..KeK..KeK.",
    "..KeK..KeK..KeK.",
    ".KeK...KeK...KeK",
    ".KeK...KeK...KeK",
    ".KKK...KKK...KKK",
    "................",
    "................",
]


def easel():
    assert len(EASEL) == 32 and all(len(r) == 16 for r in EASEL), [len(r) for r in EASEL]
    return [EASEL] * 9


def sheet(frames, letters, pal_name):
    img = Image.new("P", (16 * len(frames), 32), 0)
    pal = daemonslib.read_pal(os.path.join(PALS, pal_name + ".pal"))
    img.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    px = img.load()
    for n, fr in enumerate(frames):
        for y, row in enumerate(fr):
            for x, ch in enumerate(row):
                px[n * 16 + x, y] = letters[ch]
    return img


SPRITES = [  # (const, cname, fname, frames, letters, palette, tag, slot, note, stand-in for the recap)
    ("OBJ_EVENT_GFX_LIONESS", "Lioness", "lioness", lioness, BLUE, "npc_blue", "OBJ_EVENT_PAL_TAG_NPC_BLUE",
     "PALSLOT_NPC_1", "T-496: the lioness, met four times before the ship (DAEMONS tools/genlioness.py), npc_blue",
     "OBJ_EVENT_GFX_NURSE"),
    ("OBJ_EVENT_GFX_EASEL", "Easel", "easel", easel, PINK, "npc_pink", "OBJ_EVENT_PAL_TAG_NPC_PINK", "PALSLOT_NPC_2",
     "T-493: the pair of paintings on their easel (DAEMONS tools/genlioness.py), npc_pink; faces west on the S.S. "
     "ANNE and east in THE NEXUS, which the engine draws mirrored", "OBJ_EVENT_GFX_SIGN"),
]


def ensure_rule(fname):
    target = "$(OBJEVENTGFXDIR)/people/%s.4bpp" % fname
    s = open(RULES).read()
    if target + ":" in s:
        return
    tmp = RULES + ".tmp"
    open(tmp, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth 2 -mheight 4\n" % target)
    os.chmod(tmp, os.stat(RULES).st_mode)
    os.replace(tmp, RULES)


def register(const, cname, fname, tag, slot, note, stand_in):
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            tmp = p + ".tmp"
            open(tmp, "w").write(s2)
            os.chmod(tmp, os.stat(p).st_mode)
            os.replace(tmp, p)
    g, _ = gentowns()
    g.register_one(edit, const, cname, fname, tag, note, slot=slot, stand_in=stand_in)


def main():
    info = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")).read()
    os.makedirs(SCRATCH, exist_ok=True)
    stale = []
    for const, cname, fname, draw, letters, pal_name, tag, slot, note, stand_in in SPRITES:
        img = sheet(draw(), letters, pal_name)
        path = os.path.join(PEOPLE, fname + ".png")
        old = Image.open(path) if os.path.exists(path) else None
        same = old is not None and old.size == img.size and list(old.getdata()) == list(img.getdata())
        at = info.find("gObjectEventGraphicsInfo_%s =" % cname)
        reg = at >= 0 and tag in info[at:info.find("};", at)] and slot in info[at:info.find("};", at)]
        rule = ("people/%s.4bpp:" % fname) in open(RULES).read()
        img.convert("RGBA").resize((img.width * 6, img.height * 6), Image.NEAREST).save(
            os.path.join(SCRATCH, "%s_preview.png" % fname))
        print("  %-22s sheet %s, rule %s, registered %s" % (const, "current" if same else "STALE",
              "present" if rule else "MISSING", "yes" if reg else "NO"))
        if not (same and reg and rule):
            stale.append((const, cname, fname, img, path, tag, slot, note, stand_in))
    if not stale:
        return
    if not WRITE:
        print("  report only; pass --write (previews in %s)" % SCRATCH)
        return
    for const, cname, fname, img, path, tag, slot, note, stand_in in stale:
        img.save(path, bits=4)
        ensure_rule(fname)
        register(const, cname, fname, tag, slot, note, stand_in)
        print("  written: %s, %s" % (os.path.relpath(path, GBA), const))


if __name__ == "__main__":
    main()
